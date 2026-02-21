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
# Minimal Futuristic (Azure Advisor) Theme
# ----------------------------
st.markdown(
    """
<style>
:root{
  --bg0:#060814;
  --bg1:#080B1A;
  --panel: rgba(255,255,255,0.06);
  --panel2: rgba(255,255,255,0.08);
  --border: rgba(180,190,255,0.16);
  --border2: rgba(170,120,255,0.22);
  --text: rgba(235,238,255,0.92);
  --muted: rgba(235,238,255,0.70);
  --muted2: rgba(235,238,255,0.58);
  --accent1:#3AA9FF;  /* azure-ish blue */
  --accent2:#8A5CFF;  /* neon purple */
  --accent3:#2EF2FF;  /* cyan glow */
  --radius: 18px;
}

/* App background: clean, premium, purple/blue blobs */
.stApp{
  color: var(--text);
  background:
    radial-gradient(900px 700px at 18% 12%, rgba(58,169,255,0.16), transparent 60%),
    radial-gradient(900px 700px at 82% 18%, rgba(138,92,255,0.18), transparent 62%),
    radial-gradient(900px 900px at 50% 95%, rgba(46,242,255,0.10), transparent 60%),
    linear-gradient(180deg, var(--bg0) 0%, var(--bg1) 100%);
}

/* Subtle scanlines + vignette overlay */
.stApp::before{
  content:"";
  position: fixed;
  inset: 0;
  pointer-events: none;
  background:
    repeating-linear-gradient(
      0deg,
      rgba(255,255,255,0.03) 0px,
      rgba(255,255,255,0.03) 1px,
      rgba(0,0,0,0) 2px,
      rgba(0,0,0,0) 6px
    );
  opacity: 0.10;
  mix-blend-mode: overlay;
}
.stApp::after{
  content:"";
  position: fixed;
  inset: 0;
  pointer-events: none;
  background: radial-gradient(1200px 900px at 50% 15%, rgba(0,0,0,0.0), rgba(0,0,0,0.55));
  opacity: 0.65;
}

/* Layout spacing */
.block-container{
  padding-top: 1.1rem;
  padding-bottom: 2.0rem;
  max-width: 1200px;
}

/* Headers */
h1, h2, h3, h4{
  color: var(--text) !important;
  letter-spacing: 0.2px;
}

/* Hide footer */
footer { visibility: hidden; }

/* Sidebar */
section[data-testid="stSidebar"]{
  background: rgba(6,8,20,0.72);
  border-right: 1px solid rgba(180,190,255,0.10);
  backdrop-filter: blur(10px);
}
section[data-testid="stSidebar"] .block-container{
  padding-top: 1rem;
}

/* Card / Panel utility */
.az-card{
  background: var(--panel);
  border: 1px solid var(--border);
  border-radius: var(--radius);
  padding: 14px 16px;
  backdrop-filter: blur(12px);
  box-shadow:
    0 0 0 1px rgba(138,92,255,0.06),
    0 12px 34px rgba(0,0,0,0.38);
}
.az-card--border{
  position: relative;
}
.az-card--border::before{
  content:"";
  position:absolute;
  inset:-1px;
  border-radius: var(--radius);
  padding: 1px;
  background: linear-gradient(120deg, rgba(58,169,255,0.55), rgba(138,92,255,0.55));
  -webkit-mask:
    linear-gradient(#000 0 0) content-box,
    linear-gradient(#000 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  pointer-events:none;
  opacity: 0.55;
}

/* Small badge */
.az-badge{
  display:inline-flex;
  align-items:center;
  gap:8px;
  padding: 6px 10px;
  border-radius: 999px;
  background: rgba(255,255,255,0.06);
  border: 1px solid rgba(180,190,255,0.16);
  color: var(--muted);
  font-size: 12px;
}
.az-dot{
  width: 8px; height: 8px; border-radius: 999px;
  background: radial-gradient(circle at 30% 30%, var(--accent3), var(--accent1));
  box-shadow: 0 0 16px rgba(46,242,255,0.35);
  animation: pulse 1.6s ease-in-out infinite;
}
@keyframes pulse{
  0%,100%{ transform: scale(1.0); opacity: 0.85; }
  50%{ transform: scale(1.35); opacity: 1.0; }
}

/* Divider */
.az-hr{
  height: 1px;
  border: 0;
  background: linear-gradient(90deg, transparent, rgba(58,169,255,0.55), rgba(138,92,255,0.55), transparent);
  margin: 0.85rem 0 1.0rem 0;
  opacity: 0.9;
}

/* Buttons */
.stButton button{
  background: linear-gradient(120deg, rgba(58,169,255,0.92), rgba(138,92,255,0.92)) !important;
  border: 1px solid rgba(255,255,255,0.14) !important;
  color: white !important;
  border-radius: 12px !important;
  padding: 0.56rem 0.95rem !important;
  transition: transform 120ms ease, filter 120ms ease;
}
.stButton button:hover{
  transform: translateY(-1px);
  filter: brightness(1.04);
}

/* Inputs */
.stTextInput input, .stTextArea textarea{
  background: rgba(255,255,255,0.06) !important;
  border: 1px solid rgba(180,190,255,0.18) !important;
  color: var(--text) !important;
  border-radius: 12px !important;
}

/* Chat input */
div[data-testid="stChatInput"] textarea{
  background: rgba(255,255,255,0.07) !important;
  border: 1px solid rgba(180,190,255,0.20) !important;
  color: var(--text) !important;
  border-radius: 14px !important;
}

/* Chat bubbles */
.stChatMessage{
  border-radius: 16px;
}
.stChatMessage [data-testid="stChatMessageContent"]{
  border-radius: 16px !important;
}
.stChatMessage[data-testid="stChatMessage"]{
  background: transparent !important;
}

/* Try to give assistant/user different bubble feels */
div[data-testid="stChatMessage"]:has(img[alt="assistant"]) [data-testid="stChatMessageContent"]{
  background: rgba(255,255,255,0.06) !important;
  border: 1px solid rgba(180,190,255,0.14) !important;
  box-shadow: 0 10px 28px rgba(0,0,0,0.28);
}
div[data-testid="stChatMessage"]:has(img[alt="user"]) [data-testid="stChatMessageContent"]{
  background: rgba(58,169,255,0.08) !important;
  border: 1px solid rgba(58,169,255,0.18) !important;
  box-shadow: 0 10px 28px rgba(0,0,0,0.22);
}

/* Code blocks */
pre, code{
  border-radius: 12px !important;
}
pre{
  background: rgba(0,0,0,0.35) !important;
  border: 1px solid rgba(180,190,255,0.14) !important;
}

/* Links */
a{ color: rgba(140, 200, 255, 0.95) !important; }
</style>
""",
    unsafe_allow_html=True,
)

# ----------------------------
# Header
# ----------------------------
st.markdown(
    """
<div class="az-card az-card--border">
  <div style="display:flex; align-items:flex-start; justify-content:space-between; gap:14px;">
    <div style="min-width: 260px;">
      <div class="az-badge">
        <span class="az-dot"></span>
        <span>Azure Architecture Advisor</span>
      </div>
      <div style="font-size:28px; font-weight:750; line-height:1.10; margin-top:10px;">
        Cloud Architecture Guidance<br/>for real-world tradeoffs
      </div>
      <div style="margin-top:8px; font-size:13px; color: rgba(235,238,255,0.72);">
        Clear recommendations · Security-first · Cost-aware · Portfolio-ready output
      </div>
    </div>

    <div style="text-align:right;">
      <div style="font-size:12px; color: rgba(235,238,255,0.60);">Status</div>
      <div style="font-size:14px; font-weight:650; color: rgba(46,242,255,0.92);">READY</div>
      <div style="margin-top:8px; font-size:12px; color: rgba(235,238,255,0.60);">Output format</div>
      <div style="font-size:12px; color: rgba(235,238,255,0.74);">Snapshot · Services · Tradeoffs · Risks · Next</div>
    </div>
  </div>
</div>
<hr class="az-hr"/>
""",
    unsafe_allow_html=True,
)

# ----------------------------
# Sidebar
# ----------------------------
with st.sidebar:
    st.markdown(
        """
<div class="az-card az-card--border">
  <div style="font-size:12px; letter-spacing:1.0px; color: rgba(235,238,255,0.70); text-transform: uppercase;">
    Controls
  </div>
  <div style="margin-top:10px; font-size:13px; color: rgba(235,238,255,0.74); line-height:1.35;">
    Advisor mode: <b>Azure Architecture</b><br/>
    Default lens: <b>Security → Reliability → Cost</b>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown("")

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

    st.markdown("")
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
    # Sensible fallback so the app still runs (portfolio-friendly)
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