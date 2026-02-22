import os
import traceback
from pathlib import Path

from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI

from retriever import simple_retrieve

load_dotenv()

# ----------------------------
# Page
# ----------------------------
st.set_page_config(
    page_title="Azure Architecture Advisor",
    page_icon="☁️",
    layout="wide",
)

# ----------------------------
# ChatGPT-like Light Azure Theme (minimal + readable)
# ----------------------------
st.markdown(
    """
<style>
:root{
  /* Light azure canvas */
  --bg0:#F7FBFF;
  --bg1:#EAF4FF;

  /* Surfaces */
  --surface:#FFFFFF;
  --surface2: rgba(255,255,255,0.92);

  /* Text */
  --text:#0B1220;
  --muted: rgba(11,18,32,0.62);

  /* Borders */
  --border: rgba(15,23,42,0.12);

  /* Accents */
  --azure:#0078D4;
  --royal:#7C3AED;
  --focus: rgba(0,120,212,0.18);

  --radius:14px;
}

/* App background */
.stApp{
  background:
    radial-gradient(900px 650px at 15% 10%, rgba(0,120,212,0.10), transparent 60%),
    radial-gradient(900px 650px at 85% 12%, rgba(124,58,237,0.08), transparent 62%),
    linear-gradient(180deg, var(--bg0), var(--bg1));
  color: var(--text);
}

/* Hide Streamlit chrome */
#MainMenu {visibility:hidden;}
header {visibility:hidden;}
footer {visibility:hidden;}

/* Layout: center content like chat apps */
.block-container{
  max-width: 980px;
  padding-top: 1.0rem;
  padding-bottom: 2.4rem;
}

/* Sidebar: subtle, light */
section[data-testid="stSidebar"]{
  background: rgba(255,255,255,0.70);
  border-right: 1px solid var(--border);
  backdrop-filter: blur(10px);
}
section[data-testid="stSidebar"] .block-container{
  padding-top: 1rem;
}

/* Global text */
html, body, [class*="st-"], p, li, span, div{
  color: var(--text);
}
h1,h2,h3,h4{ color: var(--text) !important; }

/* Minimal top header */
.az-topbar{
  background: rgba(255,255,255,0.86);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 14px 16px;
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:12px;
  box-shadow: 0 10px 30px rgba(15,23,42,0.06);
}
.az-brand{
  display:flex;
  align-items:center;
  gap:10px;
  min-width: 0;
}
.az-dot{
  width:10px; height:10px; border-radius:999px;
  background: linear-gradient(90deg, var(--azure), var(--royal));
}
.az-title{
  font-size: 16px;
  font-weight: 750;
  letter-spacing: 0.2px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.az-sub{
  margin-top: 2px;
  font-size: 12px;
  color: var(--muted);
}

/* Sidebar cards */
.az-card{
  background: rgba(255,255,255,0.86);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 14px 14px;
  box-shadow: 0 10px 26px rgba(15,23,42,0.05);
}

/* Buttons */
.stButton button{
  border-radius: 12px !important;
  border: 1px solid rgba(0,0,0,0.06) !important;
  color: white !important;
  background: linear-gradient(90deg, var(--azure), var(--royal)) !important;
  padding: 0.52rem 0.85rem !important;
}
.stButton button:hover{ filter: brightness(1.05); }

/* Inputs */
.stTextInput input, .stTextArea textarea{
  background: rgba(255,255,255,0.98) !important;
  border: 1px solid rgba(15,23,42,0.14) !important;
  color: var(--text) !important;
  border-radius: 12px !important;
}
.stTextInput input:focus, .stTextArea textarea:focus{
  box-shadow: 0 0 0 3px var(--focus) !important;
  border-color: rgba(0,120,212,0.40) !important;
}

/* Chat area spacing */
div[data-testid="stChatMessage"]{
  padding-top: 0.1rem;
  padding-bottom: 0.1rem;
}

/* Chat bubbles (ChatGPT-ish) */
div[data-testid="stChatMessage"] [data-testid="stChatMessageContent"]{
  background: rgba(255,255,255,0.95) !important;
  border: 1px solid rgba(15,23,42,0.10) !important;
  border-radius: 14px !important;
  padding: 0.85rem 1.0rem !important;
  color: var(--text) !important;
  box-shadow: 0 8px 22px rgba(15,23,42,0.05);
}

/* Ensure markdown inside bubbles stays dark */
div[data-testid="stChatMessage"] [data-testid="stChatMessageContent"] *{
  color: var(--text) !important;
}

/* User bubble slightly tinted azure */
div[data-testid="stChatMessage"][aria-label="Chat message from user"] [data-testid="stChatMessageContent"]{
  background: rgba(0,120,212,0.10) !important;
  border-color: rgba(0,120,212,0.22) !important;
}

/* Assistant bubble neutral + subtle purple edge */
div[data-testid="stChatMessage"][aria-label="Chat message from assistant"] [data-testid="stChatMessageContent"]{
  background: rgba(255,255,255,0.96) !important;
  border-color: rgba(124,58,237,0.18) !important;
}

/* Chat input (bottom) - readable and clean */
div[data-testid="stChatInput"]{
  background: transparent !important;
}
div[data-testid="stChatInput"] textarea{
  background: rgba(255,255,255,0.98) !important;
  border: 1px solid rgba(15,23,42,0.16) !important;
  color: var(--text) !important;
  border-radius: 14px !important;
}
div[data-testid="stChatInput"] textarea::placeholder{
  color: rgba(11,18,32,0.45) !important;
}
div[data-testid="stChatInput"] textarea:focus{
  box-shadow: 0 0 0 3px var(--focus) !important;
  border-color: rgba(0,120,212,0.45) !important;
}

/* Code blocks */
pre{
  background: rgba(15,23,42,0.06) !important;
  border: 1px solid rgba(15,23,42,0.10) !important;
  border-radius: 12px !important;
}
code{ color: var(--text) !important; }

/* Links */
a{ color: rgba(0,120,212,0.95) !important; }
</style>
""",
    unsafe_allow_html=True,
)

# ----------------------------
# Header (ChatGPT-like minimal, no right column)
# ----------------------------
st.markdown(
    """
<div class="az-topbar">
  <div class="az-brand">
    <div class="az-dot"></div>
    <div style="min-width:0;">
      <div class="az-title">Azure Architecture Advisor</div>
      <div class="az-sub">Ask for architectures, tradeoffs, security, reliability, cost</div>
    </div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

st.write("")

# ----------------------------
# Sidebar
# ----------------------------
with st.sidebar:
    st.markdown(
        """
<div class="az-card">
  <div style="font-size:12px; letter-spacing:0.08em; color: rgba(11,18,32,0.55); text-transform: uppercase;">
    Controls
  </div>
  <div style="margin-top:10px; font-size:13px; color: rgba(11,18,32,0.78); line-height:1.45;">
    Advisor mode: <b>Azure Architecture</b><br/>
    Default lens: <b>Security → Reliability → Cost</b>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.write("")

    example = st.selectbox(
        "Example prompts",
        [
            "B2B API, EU-only, sensitive data, moderate traffic, small team, RTO 1h",
            "Startup SaaS, global users, spiky traffic, budget-sensitive, low-ops team",
            "Healthcare internal system, GDPR, EU-only, RTO 1h, strict security & audit",
        ],
        index=0,
    )

    colA, colB = st.columns(2)
    with colA:
        if st.button("Insert"):
            st.session_state["_prefill"] = example
    with colB:
        if st.button("Clear chat"):
            st.session_state.messages = []
            st.rerun()

    st.write("")
    st.caption("Tip: Add constraints (region, RTO/RPO, identity, data sensitivity, throughput, budget).")

# ----------------------------
# OpenAI Key (hardened)
# ----------------------------
api_key = (os.getenv("OPENAI_API_KEY") or "").strip()
if not api_key:
    st.error("OPENAI_API_KEY fehlt als Environment Variable.")
    st.stop()

client = OpenAI(api_key=api_key)

# ----------------------------
# System Prompt
# ----------------------------
try:
    SYSTEM_PROMPT = Path("prompts/system_architecture.txt").read_text(encoding="utf-8")
except FileNotFoundError:
    SYSTEM_PROMPT = """You are an Azure Cloud Architecture Advisor.
You produce concise, high-signal recommendations with clear tradeoffs.

Output format:
1) Workload Snapshot
2) Recommended Architecture (1 paragraph)
3) Service Map (bullets)
4) Key Design Decisions & Tradeoffs (bullets)
5) Security & Compliance (bullets)
6) Reliability & DR (RTO/RPO assumptions)
7) Cost Drivers & Optimizations
8) Risks / Anti-patterns
9) Next Questions

Use Azure services and best practices. When helpful, include small diagrams in plain text and short code snippets (Bicep/Terraform/YAML) ONLY if the user asks or it clarifies the design.
"""

def build_context(query: str) -> str:
    """Retrieve KB context (optional RAG) and attach as authoritative context."""
    try:
        hits = simple_retrieve(query, k=4)
    except Exception:
        hits = []
    if not hits:
        return "KNOWLEDGE BASE CONTEXT (authoritative):\nKB-GAP: no matching KB snippets found."
    parts = ["KNOWLEDGE BASE CONTEXT (authoritative):"]
    for h in hits:
        parts.append(f"\n---\nSOURCE: {h.get('id','unknown')}\n{h.get('text','')}")
    return "\n".join(parts)

# ----------------------------
# Session
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# Show chat history
for m in st.session_state.messages:
    if m["role"] != "system":
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

# ----------------------------
# Input (prefill support)
# ----------------------------
prefill = st.session_state.pop("_prefill", None)
user_msg = st.chat_input("Message Azure Architecture Advisor...")

# Streamlit can't truly prefill st.chat_input; this makes the insert act like "send once".
if prefill and not user_msg:
    st.info(f"Inserted: {prefill}")
    user_msg = prefill

if user_msg:
    st.session_state.messages.append({"role": "user", "content": user_msg})
    with st.chat_message("user"):
        st.markdown(user_msg)

    context = build_context(user_msg)
    messages_for_call = st.session_state.messages.copy()
    # Insert KB context right after the system prompt
    messages_for_call.insert(1, {"role": "system", "content": context})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                resp = client.chat.completions.create(
                    model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
                    messages=messages_for_call,
                    temperature=0.2,
                )
                answer = resp.choices[0].message.content
            except Exception as e:
                st.error(f"OpenAI call failed: {type(e).__name__}: {e}")
                st.code(traceback.format_exc())
                st.stop()

            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})