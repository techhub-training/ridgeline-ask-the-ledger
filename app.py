"""Ask the ledger: plain-English questions about Ridgeline's accounts payable (TechHub challenge 413, solution).

Claude writes the SQL; the app shows it, checks it is a single read-only SELECT, and runs it against a read-only copy
of the database. You check the SQL before you trust the answer.
Secrets (.streamlit/secrets.toml on your computer; Settings > Secrets on Streamlit Community Cloud):
    ANTHROPIC_API_KEY = "sk-ant-..."
"""
import re
import sqlite3
import anthropic
import pandas as pd
import streamlit as st

DB = "data/ridgeline_ap.db"
MODEL = "claude-haiku-5-5"   # small and inexpensive; a question costs a fraction of a cent

st.set_page_config(page_title="Ask the ledger", layout="wide")
st.title("Ask the ledger")
st.caption("Ridgeline Home & Tool accounts payable, April to September 2026 (data as of September 30, 2026)")


@st.cache_data
def schema() -> str:
    """The CREATE TABLE statements, so Claude knows the tables and columns."""
    with sqlite3.connect(f"file:{DB}?mode=ro", uri=True) as db:
        return "\n".join(r[0] for r in db.execute("SELECT sql FROM sqlite_master WHERE type = 'table'"))


NOTES = """Notes about the data:
- invoices.type is 'invoice' or 'credit_memo'; credit memos have negative amounts.
- invoices.status is open, partially_paid or paid; balance_due = amount - amount_paid - discount_taken.
- Dates are text in YYYY-MM-DD form. Money is in US dollars.
- purchase_orders.status is open (nothing received), partially_received or received.
- Vendor names are in vendors.name, store names in stores.name."""


def write_sql(question: str) -> str:
    """Ask Claude for one SQLite SELECT statement that answers the question."""
    client = anthropic.Anthropic(api_key=st.secrets["ANTHROPIC_API_KEY"])
    msg = client.messages.create(
        model=st.secrets.get("ANTHROPIC_MODEL", MODEL), max_tokens=600,
        system=("You write SQLite queries for an accountant. Reply with exactly one SELECT statement and nothing else: "
                "no explanation, no code fences. Use only the tables and columns in this schema.\n\n" + schema() + "\n\n" + NOTES),
        messages=[{"role": "user", "content": question}],
    )
    # newer models may send a "thinking" block first: take the first text block
    sql = next(b.text for b in msg.content if b.type == "text").strip()
    return re.sub(r"^```(?:sql)?\s*|\s*```$", "", sql).strip()


def is_safe(sql: str) -> bool:
    """One statement, starting with SELECT (or WITH), and no words that change data."""
    body = sql.strip().rstrip(";")
    if ";" in body:
        return False
    if not re.match(r"(?is)^\s*(select|with)\b", body):
        return False
    return not re.search(r"(?i)\b(insert|update|delete|drop|alter|create|replace|attach|pragma|vacuum)\b", body)


def run(sql: str) -> pd.DataFrame:
    with sqlite3.connect(f"file:{DB}?mode=ro", uri=True) as db:   # read-only: even a bad query can't change the data
        return pd.read_sql_query(sql.strip().rstrip(";"), db)


question = st.text_input("Your question", placeholder="Which vendor had the largest invoice spend in August 2026?")
if st.button("Ask", disabled=not question.strip()):
    try:
        sql = write_sql(question)
    except Exception as ex:   # a missing key, no credit left, a network problem
        st.error(f"Claude could not answer: {ex}")
        st.stop()
    st.subheader("The SQL Claude wrote")
    st.code(sql, language="sql")
    if not is_safe(sql):
        st.error("Not run: the app only runs a single read-only SELECT.")
    else:
        try:
            st.subheader("Result")
            st.dataframe(run(sql), hide_index=True)
            st.caption("Check the SQL: does it filter, join and add up what the question asked?")
        except Exception as ex:
            st.error(f"The query failed: {ex}")

with st.expander("Tables and columns"):
    st.code(schema(), language="sql")
