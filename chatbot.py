"""
chatbot.py - the "brain" of the University Admission Chatbot.

How it works (same as the flowchart in the proposal):
  1. Clean the user's text (lowercase, remove punctuation, remove filler words).
  2. Look through every entry in faq.txt and give it a score based on matching keywords.
  3. If the best score is high enough, return that entry's answer.
     Otherwise return a polite fallback message.

No external AI service or API key is used. Only the Python standard library.
"""

import difflib
import math
import os
import re

# ---------------------------------------------------------------------------
# Settings you can change
# ---------------------------------------------------------------------------
FAQ_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "faq.txt")

# The best FAQ entry must score at least this much, otherwise we show the fallback.
# Raise it (e.g. 2.0) if the bot gives wrong answers; lower it if it says "I don't know" too often.
MIN_SCORE = 2.0

WELCOME = (
    "Hello! I am the Bahria University H-11 Campus admission assistant. "
    "Ask me about admission dates, eligibility, documents, the entry test, fees, "
    "scholarships, programs, hostel and contacts."
)

FALLBACK = (
    "I am sorry, I could not find an answer to your question in the admission FAQ. "
    "Please contact the university admission office for further assistance. "
    "Email: adadmission.h11@bahria.edu.pk | Phone: 051-9259493 or 051-9259500 Ext 3315 "
    "(9:00 AM to 5:00 PM, Monday to Friday)."
)

THANKS_REPLY = "You are welcome! Ask me anything else about admissions."

# Small, common words that carry no meaning for matching.
STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "am", "be", "do", "does", "did",
    "i", "me", "my", "you", "your", "we", "our", "it", "its", "to", "of", "in", "on",
    "at", "for", "and", "or", "can", "could", "will", "would", "should", "shall",
    "what", "which", "how", "any", "there", "this", "that", "with", "about", "please",
    "tell", "want", "need", "know", "get", "give", "have", "has", "if", "so", "than",
    "much", "many", "some", "as", "by", "from", "also", "kindly", "like", "ok",
}

GREETINGS = {"hi", "hello", "hey", "salam", "assalamualaikum", "aoa", "hola", "greetings"}
THANKS = {"thanks", "thank", "thankyou", "shukriya", "jazakallah"}


# ---------------------------------------------------------------------------
# Step 1: text processing
# ---------------------------------------------------------------------------
def clean_text(text):
    """Lowercase the text and remove punctuation. 'H-11' becomes 'h11'."""
    text = text.lower()
    text = re.sub(r"\bh[\s\-]*11\b", "h11", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def stem(word):
    """Very simple stemmer so 'documents' and 'document' count as the same word."""
    if len(word) > 5 and word.endswith("ing"):
        return word[:-3]
    if len(word) > 4 and word.endswith("ies"):
        return word[:-3] + "y"
    if len(word) > 4 and word.endswith("ed"):
        return word[:-2]
    if len(word) > 3 and word.endswith("s") and not word.endswith("ss"):
        return word[:-1]
    return word


def tokenize(text):
    """Turn a sentence into a list of important, stemmed words."""
    words = clean_text(text).split()
    return [stem(w) for w in words if w not in STOPWORDS]


# ---------------------------------------------------------------------------
# Step 2: loading the knowledge base (faq.txt)
# ---------------------------------------------------------------------------
def load_faq(path=FAQ_FILE):
    """
    Read faq.txt and return a list of entries. Each entry is a dictionary with:
    question, answer, phrases (keyword phrases as word lists), keyword_words, question_words.
    """
    raw = []
    current = None
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("Question:"):
                current = {"question": line[len("Question:"):].strip(), "keywords": "", "answer": ""}
                raw.append(current)
            elif line.startswith("Keywords:") and current is not None:
                current["keywords"] = line[len("Keywords:"):].strip()
            elif line.startswith("Answer:") and current is not None:
                current["answer"] = line[len("Answer:"):].strip()

    entries = []
    for item in raw:
        phrases = []
        for kw in item["keywords"].split(","):
            words = tokenize(kw)
            if words:
                phrases.append(words)
        entries.append({
            "question": item["question"],
            "answer": item["answer"],
            "phrases": phrases,
            "keyword_words": {w for p in phrases for w in p},
            "question_words": set(tokenize(item["question"])),
        })

    # Rare words are more useful than words that appear in many entries (e.g. "admission").
    n = len(entries)
    doc_freq = {}
    for e in entries:
        for w in e["keyword_words"] | e["question_words"]:
            doc_freq[w] = doc_freq.get(w, 0) + 1
    weights = {w: math.log(1 + n / df) for w, df in doc_freq.items()}
    for e in entries:
        e["weights"] = weights
    return entries


# ---------------------------------------------------------------------------
# Step 3: matching and answering
# ---------------------------------------------------------------------------
def _fix_spelling(words, vocabulary):
    """Replace misspelled words with the closest word known to the FAQ."""
    fixed = []
    for w in words:
        if w in vocabulary or len(w) < 4:
            fixed.append(w)
        else:
            close = difflib.get_close_matches(w, vocabulary, n=1, cutoff=0.82)
            fixed.append(close[0] if close else w)
    return fixed


def score_entry(user_words, entry):
    """Give one FAQ entry a score for how well it matches the user's words."""
    weights = entry["weights"]
    score = 0.0
    for w in user_words:
        if w in entry["keyword_words"]:
            score += weights[w]            # matched a keyword
        elif w in entry["question_words"]:
            score += 0.5 * weights[w]      # matched only the question text
    for phrase in entry["phrases"]:        # bonus when a whole multi-word keyword matches
        if len(phrase) > 1 and all(w in user_words for w in phrase):
            score += 1.5 * sum(weights[w] for w in phrase) / len(phrase)
    return score


def find_answer(question, faq, min_score=MIN_SCORE):
    """
    Return (answer, matched_question, score).
    If nothing matches well enough, answer is the FALLBACK message and matched_question is None.
    """
    vocabulary = set()
    for e in faq:
        vocabulary |= e["keyword_words"] | e["question_words"]
    user_words = set(_fix_spelling(tokenize(question), sorted(vocabulary)))

    best, best_score = None, 0.0
    for entry in faq:
        s = score_entry(user_words, entry)
        if s > best_score:
            best, best_score = entry, s

    if best is not None and best_score >= min_score:
        return best["answer"], best["question"], round(best_score, 2)
    return FALLBACK, None, round(best_score, 2)


def get_response(question, faq):
    """Main function used by the app: handles greetings, thanks, empty input, then FAQ search."""
    words = clean_text(question).split()
    if not words:
        return "Please type a question about admissions."
    if len(words) <= 3 and words[0] in GREETINGS:
        return WELCOME
    if words[0] in THANKS and len(words) <= 3:
        return THANKS_REPLY
    answer, _, _ = find_answer(question, faq)
    return answer


# Quick manual test: run  python chatbot.py  and type questions in the terminal.
if __name__ == "__main__":
    faq_data = load_faq()
    print(WELCOME)
    print("(type 'quit' to stop)\n")
    while True:
        text = input("You: ")
        if text.strip().lower() in ("quit", "exit"):
            break
        print("Bot:", get_response(text, faq_data), "\n")
