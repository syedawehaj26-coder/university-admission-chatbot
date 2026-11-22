"""
test_chatbot.py - runs the sample questions from the Testing Plan (Stage 7).

Run it with:   python test_chatbot.py
It prints a table and saves test_results.csv (open it in Excel for your report).

Each test has: category, user question, and the FAQ question we EXPECT to be matched
(None means the chatbot should show the fallback message).
"""

import csv
import os

from chatbot import FALLBACK, find_answer, load_faq

TESTS = [
    # A. Normal questions (match the FAQ directly)
    ("A. Normal", "What is the last date to apply for BS programs?", "When do admissions open and close?"),
    ("A. Normal", "Which documents are required for admission?", "What documents are required for admission?"),
    ("A. Normal", "How can I apply online?", "How do I apply?"),
    ("A. Normal", "What are the admission requirements?", "What are the eligibility criteria for undergraduate programs?"),
    ("A. Normal", "Where can I find the admission form?", "How do I apply?"),
    ("A. Normal", "Is there an entry test?", "Is there an entry test?"),
    ("A. Normal", "What is the tuition fee per semester?", "What is the tuition fee per semester?"),
    ("A. Normal", "Is hostel accommodation available?", "Is hostel accommodation available?"),
    # B. Rephrased questions and spelling mistakes
    ("B. Rephrased", "What is the application procedure?", "How do I apply?"),
    ("B. Rephrased", "How do I submit my admission form?", "How do I apply?"),
    ("B. Rephrased", "When do admissions close?", "When do admissions open and close?"),
    ("B. Rephrased", "What papers should I bring for the interview?", "What documents are required for admission?"),
    ("B. Rephrased", "Do you give any scholarships to poor students?", "What scholarships are available?"),
    ("B. Rephrased", "How can I call the admissions office?", "How can I contact the Admissions Office?"),
    ("B. Rephrased", "Where is H-11 campus located?", "Where is the university located?"),
    ("B. Rephrased", "Which masters programs do you have?", "Which graduate programs are available?"),
    ("B. Rephrased", "Wat documnts do i need for admision?", "What documents are required for admission?"),
    ("B. Rephrased", "Is there a hostal for girls?", "Is hostel accommodation available?"),
    ("B. Rephrased", "How many years is a BS degree?", "How long is each degree?"),
    # C. Out-of-scope questions (the bot must NOT guess)
    ("C. Out-of-scope", "What is the weather in Islamabad today?", None),
    ("C. Out-of-scope", "Can you recommend a good pizza place?", None),
    ("C. Out-of-scope", "Who is the prime minister of Pakistan?", None),
    ("C. Out-of-scope", "How do I fix my laptop screen?", None),
    ("C. Out-of-scope", "Tell me a joke", None),
]


def main():
    faq = load_faq()
    rows = []
    passed = 0
    for number, (category, question, expected) in enumerate(TESTS, start=1):
        answer, matched, score = find_answer(question, faq)
        ok = matched == expected
        passed += ok
        expected_text = expected if expected else "Fallback message"
        actual_text = matched if matched else "Fallback message"
        rows.append([number, category, question, expected_text, actual_text, score, "PASS" if ok else "FAIL"])
        print(f"{number:>2}. [{'PASS' if ok else 'FAIL'}] {question}")
        if not ok:
            print(f"      expected: {expected_text}\n      actual:   {actual_text} (score {score})")

    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_results.csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["No", "Category", "Question", "Expected answer (FAQ entry)", "Actual answer (FAQ entry)", "Score", "Result"])
        writer.writerows(rows)

    print(f"\n{passed} of {len(TESTS)} tests passed. Results saved to test_results.csv")


if __name__ == "__main__":
    main()
