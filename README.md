# AI Chatbot for University Enquiries (Bahria University, H-11 Campus)

A beginner-level admission assistant built with **Python** and **Streamlit**. It answers from a
prepared FAQ file (`faq.txt`) using keyword matching. No paid AI service or API key is needed.

## What is in this folder

| File | What it does |
|---|---|
| `faq.txt` | The knowledge base: Question / Keywords / Answer entries |
| `chatbot.py` | The logic: cleans text, matches keywords, returns an answer or a fallback |
| `app.py` | The Streamlit chat window |
| `test_chatbot.py` | Runs 24 sample questions and saves `test_results.csv` |
| `test_results.csv` | Ready-made test table for your report (24 of 24 passed) |
| `requirements.txt` | The one package to install (`streamlit`) |

## Part 1: Run it on your computer (first time)

1. **Install Python 3.10 or newer** from https://www.python.org/downloads/ . On the first installer
   screen, tick **"Add Python to PATH"**.
2. **Install VS Code** from https://code.visualstudio.com/ . In VS Code choose
   *File > Open Folder* and open this `university_chatbot` folder.
3. Open the terminal in VS Code (*Terminal > New Terminal*) and run:

   ```
   pip install -r requirements.txt
   ```
4. Start the chatbot:

   ```
   streamlit run app.py
   ```
   Your browser opens the chat window automatically. Press `Ctrl + C` in the terminal to stop it.

If `pip` or `streamlit` is "not recognized", try `python -m pip install -r requirements.txt` and
`python -m streamlit run app.py`.

## Part 2: Test it (Stage 7 of the proposal)

```
python test_chatbot.py
```

This runs 24 questions in three groups: 8 normal, 11 rephrased or misspelled, and 5 out-of-scope.
It prints PASS or FAIL for each and saves `test_results.csv` with the expected answer, actual answer
and result, which is exactly the table your proposal promises. Open the CSV in Excel and paste it
into your report.

You can also chat in the terminal without Streamlit: `python chatbot.py`.

## Part 3: How the code works (for your viva or demo)

The flow is the same as the flowchart in your proposal:

1. **The user types a question** in the Streamlit chat box (`app.py`).
2. **`clean_text()`** makes it lowercase and removes punctuation. **`tokenize()`** drops filler
   words such as "the", "is", "how" and shortens words with **`stem()`**, so "documents" and
   "document" match.
3. **`_fix_spelling()`** uses Python's `difflib` to repair small spelling mistakes
   ("documnts" becomes "documents").
4. **`score_entry()`** gives each FAQ entry a score. Matching a rare keyword (like "hostel") counts
   more than a common one (like "admission"), and matching a whole phrase (like "last date") earns
   a bonus.
5. **`find_answer()`** picks the highest-scoring entry. If the score is at least `MIN_SCORE`, it
   returns that answer. Otherwise it returns the **polite fallback message** and never guesses.
6. **`app.py`** shows the reply and keeps the history in `st.session_state` for the session.

Topics that you do not have confirmed facts for (transport, library timings, attendance,
installments) have FAQ entries that say so honestly and point to the right office extension.

## Part 4: Keep the information up to date

Open `faq.txt` and edit the text after `Answer:`. Save, then refresh the page. Each entry must have
exactly this shape:

```
Question: ...
Keywords: word, another word, a phrase
Answer: ...
```

- **Before every admission season**, update the dates and fees (the first entries and the fee entry).
- If the bot gives a wrong answer, add missing words to that entry's `Keywords:` line.
- If it says "I could not find an answer" too often, lower `MIN_SCORE` in `chatbot.py` (for example
  to `1.5`). If it answers wrongly too often, raise it (for example to `2.5`).

## Part 5: GitHub backup (project setup role)

1. Create a free account at https://github.com and click **New repository** (name it
   `university-admission-chatbot`).
2. In the VS Code terminal:

   ```
   git init
   git add .
   git commit -m "University admission chatbot"
   git branch -M main
   git remote add origin https://github.com/YOUR-USERNAME/university-admission-chatbot.git
   git push -u origin main
   ```

## Part 6: Put it online (optional)

1. Push the project to GitHub (Part 5).
2. Go to https://share.streamlit.io and sign in with GitHub.
3. Click **Create app**, choose your repository, set the main file to `app.py`, and click **Deploy**.

## Part 7: Suggested 5-minute demo script (Stage 8)

1. **Introduce the problem** (30 sec): applicants ask the same questions again and again; offices
   close at 5 PM.
2. **Start the app** with `streamlit run app.py` and say hello to the bot.
3. **Normal questions** (1 min): "What is the last date to apply for BS programs?", "Which documents
   are required for admission?", "Is there an entry test?"
4. **Rephrased and misspelled** (1 min): "Wat documnts do i need for admision?", "Is there a hostal
   for girls?"
5. **Unknown question** (30 sec): "Can you recommend a good pizza place?" The bot refuses to guess
   and points to the admission office.
6. **Show the knowledge base** (1 min): open `faq.txt` and edit an answer live, then refresh.
7. **Show testing** (45 sec): run `python test_chatbot.py` and open `test_results.csv`.
8. **State the limitations** (30 sec): only answers what is in the FAQ, needs manual updates, no
   generative AI.

## Team roles from the proposal, mapped to files

- **Syeda Wehaj Gilani**: requirement analysis, writing `faq.txt`, text processing and keyword
  matching in `chatbot.py`.
- **Amna Ishtiaq**: data collection, running `test_chatbot.py` and recording results, `app.py` and
  integration.
- **Emaan Batool**: project setup and GitHub, `find_answer()`/fallback/history, final report and demo.

## Known limitations

- It only knows what is written in `faq.txt` and may miss unusual wording.
- A very generic question (for example just "fee") can fall back instead of answering.
- Fees are listed per program for the Fall 2026 / Spring 2027 intake; the fee table does not always
  say which Islamabad campus a row applies to, so the answer asks users to confirm with the Fee
  Section.
