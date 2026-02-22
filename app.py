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
# Minimal Azure + Royal Purple Theme (stable Streamlit CSS)
# ----------------------------
st.markdown(
    """
<style>
/* --------- Design Tokens --------- */
:root{
  --bg: #0b0f19;            /* near-black */
  --panel: #111827;         /* slate panel */
  --panel2: #0f172a;        /* deeper */
  --text: rgba(255,255,255,0.92);
  --muted: rgba(255,255,255,0.68);
  --border: rgba(255,255,255,0.10);

  --azure: #0078D4;         /* Azure blue */
  --royal: #7C3AED;         /* royal purple */
  --focus: rgba(0,120,212,0.35);

  --radius: 14px;
}

/* --------- App Background --------- */
.stApp{
  background: var(--bg);
  color: var(--text);
}

/* Keep layout predictable */
.block-container{
  max-width: 1180px;
  padding-top: 1.0rem;
  padding-bottom: 2.0rem;
}

/* Hide Streamlit chrome */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}

/* --------- Sidebar --------- */
section[data-testid="stSidebar"]{
  background: #0a0e17;
  border-right: 1px solid var(--border);
}
section[data-testid="stSidebar"] .block-container{
  padding-top: 1rem;
}

/* --------- Typography --------- */
h1,h2,h3,h4{
  color: var(--text) !important;
}

/* --------- Cards --------- */
.az-card{
  background: linear-gradient(180deg, rgba(255,255,255,0.04), rgba(255,255,255,0.03));
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 14px 16px;
}

.az-header{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap:16px;
}

.az-title{
  font-size: 26px;
  font-weight: 750;
  line-height: 1.15;
  margin-top: 6px;
}

.az-sub{
  margin-top: 6px;
  font-size: 13px;
  color: var(--muted);
}

.az-badge{
  display:inline-flex;
  align-items:center;
  gap:8px;
  padding: 6px 10px;
  border-radius: 999px;
  border: 1px solid var(--border);
  background: rgba(255,255,255,0.03);
  color: var(--muted);
  font-size: 12px;
}

.az-dot{
  width: 8px;
  height: 8px;
  border-radius: 99px;
  background: linear-gradient(90deg, var(--azure), var(--royal));
}

.az-meta{
  text-align:right;
  font-size: 12px;
  color: var(--muted);
}
.az-meta strong{
  color: var(--text);
  font-weight: 650;
}

/* --------- Buttons --------- */
.stButton button{
  border-radius: 12px !important;
  border: 1px solid rgba(255,255,255,0.14) !important;
  color: white !important;
  background: linear-gradient(90deg, var(--azure), var(--royal)) !important;
  padding: 0.56rem 0.95rem !important;
}
.stButton button:hover{
  filter: brightness(1.05);
}

/* --------- Inputs --------- */
.stTextInput input, .stTextArea textarea{
  background: rgba(255,255,255,0.03) !important;
  border: 1px solid rgba(255,255,255,0.12) !important;
  color: var(--text) !important;
  border-radius: 12px !important;
}
.stTextInput input:focus, .stTextArea textarea:focus{
  box-shadow: 0 0 0 3px var(--focus) !important;
  border-color: rgba(0,120,212,0.55) !important;
}

/* Chat input (bottom) */
div[data-testid="stChatInput"] textarea{
  background: rgba(255,255,255,0.03) !important;
  border: 1px solid rgba(255,255,255,0.14) !important;
  color: var(--text) !important;
  border-radius: 14px !important;
}
div[data-testid="stChatInput"] textarea:focus{
  box-shadow: 0 0 0 3px var(--focus) !important;
  border-color: rgba(0,120,212,0.55) !important;
}

/* --------- Chat bubbles (simple + robust) --------- */
div[data-testid="stChatMessage"] [data-testid="stChatMessageContent"]{
  border-radius: 14px !important;
  border: 1px solid rgba(255,255,255,0.10) !important;
  background: rgba(255,255,255,0.03) !important;
}

/* Make user messages slightly tinted (no :has selector -> stable) */
div[data-testid="stChatMessage"][aria-label="Chat message from user"] [data-testid="stChatMessageContent"]{
  background: rgba(0,120,212,0.10) !important;
  border-color: rgba(0,120,212,0.22) !important;
}

/* Assistant messages subtle purple edge */
div[data-testid="stChatMessage"][aria-label="Chat message from assistant"] [data-testid="stChatMessageContent"]{
  background: rgba(255,255,255,0.03) !important;
  border-color: rgba(124,58,237,0.18) !important;
}

/* Code blocks */
pre{
  background: rgba(0,0,0,0.30) !important;
  border: 1px solid rgba(255,255,255,0.10) !important;
  border-radius: 12px !important;
}

/* Links */
a{ color: rgba(140, 200, 255, 0.95) !important; }
</style>
""",
    unsafe_allow_html=True,
)

# ----------------------------
# Header (minimal)
# ----------------------------
st.markdown(
    """
<div class="az-card">
  <div class="az-header">
    <div>
      <div class="az-badge"><span class="az-dot"></span><span>Azure Architecture Advisor</span></div>
      <div class="az-title">Cloud Architecture Guidance</div>
      <div class="az-sub">Security-first · Reliability-aware · Cost-conscious</div>
    </div>
    <div class="az-meta">
      <div>Status: <strong>READY</strong></div>
      <div style="margin-top:6px;">Format: <strong>Snapshot · Services · Tradeoffs · Risks · Next</strong></div>
    </div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

st.write("")  # spacing

# ----------------------------
# Sidebar
# ----------------------------
with st.sidebar:
    st.markdown(
        """
<div class="az-card">
  <div style="font-size:12px; letter-spacing:0.08em; color: rgba(255,255,255,0.70); text-transform: uppercase;">
    Controls
  </div>
  <div style="margin-top:10px; font-size:13px; color: rgba(255,255,255,0.76); line-height:1.45;">
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
user_msg = st.chat_input("Describe your workload (e.g., region, RTO/RPO, data sensitivity, traffic, team size)")

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