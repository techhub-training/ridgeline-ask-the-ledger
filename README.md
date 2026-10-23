# Ask the ledger: solution

The worked solution to TechHub challenge 413, **Ask the Ledger in Plain English** (https://techhub.byuaccounting.net/t/413-genai-ask-the-ledger-in-plain-english/9413/).
The starter that students copy is on the `main` branch of https://github.com/techhub-training/ridgeline-ask-the-ledger.

Run it: put `ANTHROPIC_API_KEY = "sk-ant-..."` in `.streamlit/secrets.toml`, then `streamlit run app.py`.
The model is `claude-haiku-5-5`; set `ANTHROPIC_MODEL` in secrets to try another.

* **The prompt** gives Claude the `CREATE TABLE` statements and a few notes the schema can't say (credit memos are
  negative; what each status means). Without the notes, "not fully paid" and "open" are guesses.
* **`is_safe`** allows one statement, starting with `SELECT` or `WITH`, with no data-changing keywords. It is a
  second lock: `run()` opens the database with `mode=ro`, so even a query that slips past can't change anything.
* **The answers:** 2 inactive vendors; 325,475.41 balance due (172 invoices and credit memos not fully paid);
  Wasatch Lumber Supply (104,922.66 in Q3); 16 open purchase orders; 396.63 in discounts taken.

Where it goes wrong: "spend" summed with credit memos, "Q3" read as a fiscal quarter, "open" read as "not received
in full" (that also counts partially received POs). The SQL on screen is how you catch it.

## Where your data goes (Level 2, Processing on a server)

| Question | Answer |
|---|---|
| Who runs the code? | Streamlit Community Cloud runs `app.py`. |
| Where does the data go? | The ledger ships with the app as a database file opened read-only. Each question, with the table descriptions, goes to Anthropic (the Claude API) to be turned into SQL: that part leaves the app. The answers are kept nowhere. |
| Who can reach it? | Anyone with the link spends your API credit. The key lives only in Streamlit Secrets; keep a low spending limit. |

