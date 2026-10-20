# Ask the ledger

TechHub challenge 413: **Ask the Ledger in Plain English**. Full instructions, data dictionary and hints: https://techhub.byuaccounting.net/t/413-genai-ask-the-ledger-in-plain-english/9413/

*Ridgeline series:* you work in accounting at Ridgeline Home & Tool, a home-improvement retailer with eleven stores
in Utah and Idaho and a distribution center.

The AP manager answers the same questions every week by asking someone to write SQL. This app lets anyone ask in plain English: Claude writes one SQL query from the database's table definitions, the app shows the query, runs it against a **read-only** copy of `data/ridgeline_ap.db`, and shows the result. Showing the SQL matters: you check it before you trust the answer.

## Get your own copy

Click **Use this template › Create a new repository**. Keep the name `ridgeline-ask-the-ledger` and make it **Public**.
(Or open it straight in a codespace: https://codespaces.new/techhub-training/ridgeline-ask-the-ledger?quickstart=1.) Work in your copy, not this one.

## Open it

**In your browser (nothing to install):** on your copy of this repository, click **Code › Codespaces › Create codespace on main**.
The app installs and starts by itself, and a preview opens in a few minutes. Stop the codespace when you're done
(github.com/codespaces › ••• › Stop) so it doesn't use your free hours.

**On your computer:** you need Python 3.10 or newer and Git.

```
git clone https://github.com/<you>/ridgeline-ask-the-ledger.git
cd ridgeline-ask-the-ledger
python -m venv .venv
source .venv/bin/activate          # Windows PowerShell: .venv\Scripts\Activate.ps1
pip install -r requirements.txt
streamlit run app.py
```
## Your Anthropic API key goes in secrets

The app calls Claude through the Anthropic API, which needs a key (from console.anthropic.com, with a few dollars of
credit and a **spending limit** set). A question costs a fraction of a cent with the default model.

Create `.streamlit/secrets.toml` (`.gitignore` already keeps it out of Git) with:

```toml
ANTHROPIC_API_KEY = "sk-ant-..."
```

Never put the key in `app.py`: a key in a public repository is found by bots within minutes and spent.


## Your task

1. Put your Anthropic key in secrets (above).
2. **TODO 1** in `app.py`: write the system prompt. Give Claude the schema (`schema()`), the `NOTES` about the data, and clear
   instructions to reply with exactly one SQLite `SELECT` statement and nothing else. Strip any code fences it adds anyway.
3. **TODO 2**: write `is_safe(sql)`. Return `True` only for a single statement that starts with `SELECT` (or `WITH`) and
   contains none of the words that change data (`INSERT`, `UPDATE`, `DELETE`, `DROP`, `ALTER`, `CREATE`, ...).
   Test it: ask *"Delete every credit memo"*. The app should refuse to run what comes back. (The database is opened
   read-only too, so a bad query fails either way. Two locks are better than one.)
4. Ask your app these questions. For each, read the SQL and make sure it answers the question asked:
   * How many vendors are inactive?
   * What is the total balance due on invoices and credit memos that are not fully paid?
   * Which vendor had the most invoice spend (invoices only, not credit memos) from July through September 2026?
   * How many purchase orders are open, with nothing received yet?
   * What is the total early-payment discount Ridgeline has taken?
5. Optional: publish it on Streamlit Community Cloud with the key in the app's secrets. It's then public, so anyone can
   spend your credit: keep the spending limit low, or leave this one running only on your computer.



## Check your answer

Enter the five answers in the TechHub checker. Checker: https://techhub.byuaccounting.net/check/?c=413

The worked solution is on the [`solution` branch](https://github.com/techhub-training/ridgeline-ask-the-ledger/tree/solution). Try it yourself first.
