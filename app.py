"""
app.py - the Streamlit chat window (navy blue and white theme).

Run it with:   streamlit run app.py
"""

import streamlit as st

from chatbot import WELCOME, get_response, load_faq

st.set_page_config(page_title="University Admission Assistant", page_icon="🎓", layout="centered")

# ---------------------------------------------------------------------------
# Theme: navy blue (#0b1f4d) and white. Change the colours here if you like.
# ---------------------------------------------------------------------------
THEME_CSS = """
<style>
  .stApp { background: #ffffff; }
  header[data-testid="stHeader"] { background: transparent; }
  [data-testid="stToolbar"], [data-testid="stDecoration"], #MainMenu, footer { display: none !important; }
  .block-container { max-width: 820px; padding-top: 1.4rem; padding-bottom: 6rem; }

  /* Header banner */
  .hero { background: linear-gradient(135deg, #0b1f4d 0%, #1b3f94 100%); border-radius: 16px;
          padding: 26px 28px; margin-bottom: 18px; }
  .hero-title { color: #ffffff; font-size: 1.85rem; font-weight: 700; line-height: 1.2; margin: 0 0 6px; }
  .hero-sub { color: #cfe0ff; font-size: 1rem; margin: 0; }

  /* Chat bubbles: assistant = light blue with navy text, user = navy with white text */
  [data-testid="stChatMessage"] { background: #eef3fb; border: 1px solid #d3deef; border-radius: 14px;
          padding: 14px 16px; margin-bottom: 10px; }
  [data-testid="stChatMessage"] p, [data-testid="stChatMessage"] li { color: #0b1f4d; }
  [data-testid="stChatMessage"] a { color: #1b3f94; }
  [data-testid="stChatMessage"]:has([data-testid*="user" i]) { background: #0b1f4d; border-color: #0b1f4d; }
  [data-testid="stChatMessage"]:has([data-testid*="user" i]) * { color: #ffffff !important; }

  /* Typing box: white box, navy text, readable even if the browser is in dark mode */
  [data-testid="stBottom"], [data-testid="stBottom"] > div { background: #ffffff !important; }
  [data-testid="stChatInput"], [data-testid="stChatInput"] > div,
  [data-testid="stChatInput"] [data-baseweb="textarea"], [data-testid="stChatInput"] [data-baseweb="base-input"],
  [data-testid="stChatInput"] textarea { background: #ffffff !important; }
  [data-testid="stChatInput"] { border: 2px solid #0b1f4d !important; border-radius: 14px; }
  [data-testid="stChatInput"] textarea { color: #0b1f4d !important; -webkit-text-fill-color: #0b1f4d !important;
          caret-color: #0b1f4d; }
  [data-testid="stChatInput"] textarea::placeholder { color: #6b7a99 !important; -webkit-text-fill-color: #6b7a99 !important; opacity: 1; }
  [data-testid="stChatInputSubmitButton"] { background: #0b1f4d !important; color: #ffffff !important; border-radius: 10px; }
  [data-testid="stChatInputSubmitButton"] svg { fill: #ffffff !important; color: #ffffff !important; }

  /* Sidebar */
  [data-testid="stSidebar"] { background: #0b1f4d; }
  [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3,
  [data-testid="stSidebar"] [data-testid="stCaptionContainer"], [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p
  { color: #e6eeff !important; }
  [data-testid="stSidebar"] hr { border-color: rgba(255, 255, 255, 0.25); }
  [data-testid="stSidebar"] .stButton button { background: #ffffff; border: 1px solid #ffffff; border-radius: 10px;
          text-align: left; }
  [data-testid="stSidebar"] .stButton button, [data-testid="stSidebar"] .stButton button p { color: #0b1f4d !important; }
  [data-testid="stSidebar"] .stButton button:hover { background: #dbe7ff; border-color: #dbe7ff; }
</style>
"""
st.markdown(THEME_CSS, unsafe_allow_html=True)


@st.cache_data
def get_faq():
    """Load faq.txt once and keep it in memory."""
    return load_faq()


faq = get_faq()

# ----- Page header -----
st.markdown(
    """
    <div class="hero">
      <div class="hero-title">🎓 University Admission Assistant</div>
      <p class="hero-sub">Bahria University, H-11 Campus, Islamabad. Ask me anything about admissions.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

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
        "Student project, not an official Bahria University service. Answers come from a "
        "prepared FAQ file checked in November 2026. For anything not covered, please contact "
        "the admission office."
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
