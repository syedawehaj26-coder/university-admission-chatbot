"""
app.py - the Streamlit chat window.

Run it with:   streamlit run app.py
"""

import streamlit as st

from chatbot import WELCOME, get_response, load_faq

st.set_page_config(page_title="University Admission Assistant", page_icon="🎓")


@st.cache_data
def get_faq():
    """Load faq.txt once and keep it in memory."""
    return load_faq()


faq = get_faq()

# ----- Page header -----
st.title("🎓 University Admission Assistant")
st.caption("Bahria University, H-11 Campus, Islamabad. Ask me anything about admissions.")

# ----- Sidebar -----
EXAMPLES = [
    "What is the last date to apply?",
    "Which documents are required for admission?",
    "How can I apply online?",
    "Is there an entry test?",
    "What scholarships are available?",
    "Is hostel accommodation available?",
]
with st.sidebar:
    st.header("Try asking")
    clicked = None
    for example in EXAMPLES:
        if st.button(example, use_container_width=True):
            clicked = example
    st.divider()
    if st.button("Clear chat", use_container_width=True):
        st.session_state.messages = [{"role": "assistant", "content": WELCOME}]
        st.rerun()
    st.caption(
        "Answers come from a prepared FAQ file. For anything not covered, please contact the "
        "admission office. Information was checked in November 2026."
    )

# ----- Conversation history (kept for the current session) -----
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": WELCOME}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ----- New question -----
typed = st.chat_input("Ask your admission question here...")
question = clicked or typed

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    answer = get_response(question, faq)
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)
