import os
import traceback
import re
import streamlit.components.v1 as components
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
# UI Theme: "Google AI Studio / modern SaaS" inspired
# ----------------------------
st.markdown(
    """
<style>
:root{
  /* Canvas */
  --bg0:#F6F8FF;
  --bg1:#EEF3FF;

  /* Surfaces */
  --surface:#FFFFFF;
  --surface2: rgba(255,255,255,0.86);
  --surface3: rgba(255,255,255,0.72);

  /* Text */
  --text:#0B1220;
  --muted: rgba(11,18,32,0.60);

  /* Borders / Shadows */
  --border: rgba(15,23,42,0.12);
  --shadow: 0 18px 50px rgba(15,23,42,0.08);

  /* Accents */
  --azure:#2563EB;      /* more "modern azure" */
  --azure2:#3B82F6;
  --violet:#7C3AED;
  --violet2:#A855F7;

  --radius-xl: 26px;
  --radius-lg: 18px;
  --radius-md: 14px;
}

/* App background */
.stApp{
  background:
    radial-gradient(900px 650px at 18% 8%, rgba(37,99,235,0.14), transparent 60%),
    radial-gradient(900px 650px at 82% 10%, rgba(124,58,237,0.14), transparent 62%),
    radial-gradient(900px 650px at 70% 90%, rgba(168,85,247,0.10), transparent 64%),
    linear-gradient(180deg, var(--bg0), var(--bg1));
  color: var(--text);
}

/* Hide Streamlit chrome */
#MainMenu {visibility:hidden;}
header {visibility:hidden;}
footer {visibility:hidden;}

/* Make content feel like a rounded "app card" */
.block-container{
  max-width: 1220px;
  padding-top: 1.1rem;
  padding-bottom: 2.2rem;
}

/* Sidebar styling */
section[data-testid="stSidebar"]{
  background: rgba(255,255,255,0.60);
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

/* "App frame" container card look */
.az-frame{
  background: rgba(255,255,255,0.55);
  border: 1px solid rgba(15,23,42,0.10);
  border-radius: var(--radius-xl);
  box-shadow: var(--shadow);
  padding: 20px 20px 16px 20px;
}

/* Top bar inside frame */
.az-topbar{
  display:flex;
  align-items:center;
  justify-content:space-between;
  gap: 12px;
  margin-bottom: 8px;
}
.az-brand{
  display:flex;
  align-items:center;
  gap: 12px;
  min-width: 0;
}
.az-logo{
  width: 44px;
  height: 44px;
  border-radius: 16px;
  display:flex;
  align-items:center;
  justify-content:center;
  color: white;
  background: linear-gradient(135deg, var(--azure), var(--violet));
  box-shadow: 0 14px 30px rgba(37,99,235,0.20);
}
.az-brand-title{
  font-weight: 800;
  letter-spacing: 0.2px;
  font-size: 18px;
  line-height: 1.05;
}
.az-brand-sub{
  font-size: 12.5px;
  color: var(--muted);
  margin-top: 2px;
}

/* "Share" button (cosmetic) */
.az-share{
  border: 1px solid rgba(15,23,42,0.10);
  background: rgba(255,255,255,0.70);
  border-radius: 999px;
  padding: 8px 12px;
  color: rgba(11,18,32,0.80);
  font-size: 12.5px;
}

/* Sidebar cards */
.az-card{
  background: rgba(255,255,255,0.80);
  border: 1px solid rgba(15,23,42,0.10);
  border-radius: var(--radius-lg);
  padding: 14px 14px;
  box-shadow: 0 12px 28px rgba(15,23,42,0.06);
}
.az-card-title{
  font-size: 11px;
  letter-spacing: 0.12em;
  color: rgba(11,18,32,0.55);
  text-transform: uppercase;
  margin-bottom: 10px;
}
.az-kv{
  font-size: 13px;
  color: rgba(11,18,32,0.80);
  line-height: 1.55;
}

/* Buttons */
.stButton button{
  border-radius: 14px !important;
  border: 1px solid rgba(15,23,42,0.10) !important;
  background: linear-gradient(90deg, var(--azure), var(--violet)) !important;
  color: white !important;
  padding: 0.55rem 0.9rem !important;
  box-shadow: 0 14px 30px rgba(37,99,235,0.18);
}
.stButton button:hover{ filter: brightness(1.05); }

/* Secondary/ghost buttons: we fake via markdown + Streamlit is limited.
   We'll just keep primary buttons consistent. */

/* Selectbox look */
div[data-baseweb="select"] > div{
  border-radius: 14px !important;
  background: rgba(255,255,255,0.92) !important;
  border: 1px solid rgba(15,23,42,0.12) !important;
}

/* Chat bubbles */
div[data-testid="stChatMessage"]{
  padding-top: 0.15rem;
  padding-bottom: 0.15rem;
}
div[data-testid="stChatMessage"] [data-testid="stChatMessageContent"]{
  background: rgba(255,255,255,0.90) !important;
  border: 1px solid rgba(15,23,42,0.10) !important;
  border-radius: 18px !important;
  padding: 0.9rem 1.05rem !important;
  box-shadow: 0 10px 24px rgba(15,23,42,0.06);
}
div[data-testid="stChatMessage"] [data-testid="stChatMessageContent"] *{
  color: var(--text) !important;
}

/* User bubble tinted */
div[data-testid="stChatMessage"][aria-label="Chat message from user"] [data-testid="stChatMessageContent"]{
  background: rgba(37,99,235,0.10) !important;
  border-color: rgba(37,99,235,0.20) !important;
}

/* Assistant bubble slight violet edge */
div[data-testid="stChatMessage"][aria-label="Chat message from assistant"] [data-testid="stChatMessageContent"]{
  background: rgba(255,255,255,0.92) !important;
  border-color: rgba(124,58,237,0.16) !important;
}

/* Chat input */
div[data-testid="stChatInput"]{
  background: transparent !important;
}
div[data-testid="stChatInput"] textarea{
  background: rgba(255,255,255,0.94) !important;
  border: 1px solid rgba(15,23,42,0.12) !important;
  color: var(--text) !important;
  border-radius: 18px !important;
  padding-top: 0.65rem !important;
}
div[data-testid="stChatInput"] textarea:focus{
  box-shadow: 0 0 0 4px rgba(37,99,235,0.16) !important;
  border-color: rgba(37,99,235,0.32) !important;
}
div[data-testid="stChatInput"] textarea::placeholder{
  color: rgba(11,18,32,0.45) !important;
}

/* Quick action chips (markdown buttons look) */
.az-chips{
  display:flex;
  gap: 10px;
  flex-wrap: wrap;
  justify-content: center;
  margin-top: 10px;
}
.az-chip{
  display:inline-flex;
  align-items:center;
  gap: 8px;
  padding: 10px 14px;
  border-radius: 999px;
  background: rgba(255,255,255,0.72);
  border: 1px solid rgba(15,23,42,0.10);
  color: rgba(11,18,32,0.82);
  font-size: 13px;
  box-shadow: 0 10px 22px rgba(15,23,42,0.05);
}

/* Hero state */
.az-hero{
  display:flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 28px 10px 14px 10px;
  text-align:center;
}
.az-hero-icon{
  width: 88px;
  height: 88px;
  border-radius: 28px;
  display:flex;
  align-items:center;
  justify-content:center;
  color: white;
  background: linear-gradient(135deg, var(--azure2), var(--violet2));
  box-shadow: 0 18px 45px rgba(124,58,237,0.18);
  margin-bottom: 14px;
  font-size: 34px;
}
.az-hero-title{
  font-size: 40px;
  font-weight: 900;
  letter-spacing: -0.6px;
  line-height: 1.02;
  margin: 0;
}
.az-hero-sub{
  margin-top: 8px;
  font-size: 14px;
  color: var(--muted);
}

/* Small helpers */
.az-tip{
  font-size: 12px;
  color: rgba(11,18,32,0.55);
}
</style>
""",
    unsafe_allow_html=True,
)

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



def extract_mermaid(md: str):
    """Extract first ```mermaid``` block and return (code_without_fence, remaining_markdown)."""
    pattern = re.compile(r"```mermaid\s*(.*?)```", re.DOTALL | re.IGNORECASE)
    m = pattern.search(md or "")
    if not m:
        return None, (md or "")
    code = (m.group(1) or "").strip()
    remaining = ((md or "")[: m.start()] + (md or "")[m.end() :]).strip()
    return code, remaining


def mermaid_fallback_diagram(user_query: str) -> str:
    """Minimal fallback diagram if the model fails to include Mermaid."""
    # Keep labels simple for GitHub/mermaid compatibility
    return """flowchart LR
    User --> Edge[Front Door]
    Edge --> APIM[API Management]
    APIM --> App[App Service]
    App --> Data[SQL Database]
    App --> KV[Key Vault]
    App --> Mon[Monitor]
"""


def render_mermaid(code: str, height: int = 420):
    """Render Mermaid diagram in Streamlit using a small HTML component."""
    safe = (code or "").strip()
    if not safe:
        return
    html = f"""
    <div class='mermaid'>
    {safe}
    </div>
    <script type='module'>
      import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
      mermaid.initialize({{ startOnLoad: true, securityLevel: 'strict', theme: 'default' }});
    </script>
    """
    components.html(html, height=height, scrolling=True)


# ----------------------------
# Session
# ----------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# ----------------------------
# Sidebar
# ----------------------------
with st.sidebar:
    # Brand block
    st.markdown(
        """
<div class="az-card" style="padding:14px 14px 12px 14px;">
  <div style="display:flex; align-items:center; gap:10px;">
    <div class="az-logo" style="width:42px; height:42px; border-radius:16px;">☁️</div>
    <div style="min-width:0;">
      <div style="font-weight:900; letter-spacing:0.2px;">AZURE-G</div>
      <div style="font-size:12px; color: rgba(11,18,32,0.55); margin-top:2px;">Azure Architecture Advisor</div>
    </div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.write("")

    st.markdown(
        """
<div class="az-card">
  <div class="az-card-title">Controls</div>
  <div class="az-kv">
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
            st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]
            st.rerun()

    st.write("")
    st.caption("Tip: Add constraints (region, RTO/RPO, identity, data sensitivity, throughput, budget).")

# ----------------------------
# Main Frame (topbar + hero/chat)
# ----------------------------
st.markdown(
    """
<div class="az-frame">
  <div class="az-topbar">
    <div class="az-brand">
      <div class="az-logo">☁️</div>
      <div style="min-width:0;">
        <div class="az-brand-title">Azure Architecture Advisor</div>
        <div class="az-brand-sub">Ask for architectures, tradeoffs, security, reliability, cost</div>
      </div>
    </div>
    <div class="az-share">Share</div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

st.write("")

# ----------------------------
# Hero state (only system message exists)
# ----------------------------
only_system = len(st.session_state.messages) == 1

if only_system:
    st.markdown(
        """
<div class="az-frame">
  <div class="az-hero">
    <div class="az-hero-icon">☁️</div>
    <div class="az-hero-title">Azure Architecture Advisor</div>
    <div class="az-hero-sub">Ask for architectures, tradeoffs, security, reliability, cost</div>
    <div class="az-chips" style="margin-top:14px;">
      <div class="az-chip">🗂️ Architecture</div>
      <div class="az-chip">🛡️ Security</div>
      <div class="az-chip">☁️ Deployment</div>
      <div class="az-chip">👥 Governance</div>
    </div>
    <div class="az-tip" style="margin-top:12px;">
      Tip: Add constraints (region, RTO/RPO, identity, data sensitivity, throughput, budget).
    </div>
  </div>
</div>
""",
        unsafe_allow_html=True,
    )
    st.write("")

# ----------------------------
# Show chat history
# ----------------------------
for m in st.session_state.messages:
    if m["role"] == "system":
        continue
    role = m.get("role", "assistant")
    content = m.get("content", "")
    with st.chat_message(role):
        mermaid_code, remaining = extract_mermaid(content)
        # Always show a diagram for assistant messages
        if role == "assistant":
            if not mermaid_code:
                mermaid_code = mermaid_fallback_diagram("")
            # height scales a bit with number of lines
            h = max(320, min(640, 260 + 18 * (len((mermaid_code or "").splitlines()))))
            render_mermaid(mermaid_code, height=h)
        if remaining:
            st.markdown(remaining)

# ----------------------------
# Input (prefill support)
# ----------------------------
prefill = st.session_state.pop("_prefill", None)
user_msg = st.chat_input("Message Azure Architecture Advisor...")

# Streamlit can't truly prefill st.chat_input; we emulate "insert then send once".
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
                    max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "650")),
                )
                answer = resp.choices[0].message.content
            except Exception as e:
                st.error(f"OpenAI call failed: {type(e).__name__}: {e}")
                st.code(traceback.format_exc())
                st.stop()

            mermaid_code, remaining = extract_mermaid(answer)
            if not mermaid_code:
                mermaid_code = mermaid_fallback_diagram(user_msg)
                answer = f"DIAGRAM:\n```mermaid\n{mermaid_code}\n```\n\n" + answer
            h = max(320, min(640, 260 + 18 * (len((mermaid_code or "").splitlines()))))
            render_mermaid(mermaid_code, height=h)
            if remaining:
                st.markdown(remaining)

    st.session_state.messages.append({"role": "assistant", "content": answer})