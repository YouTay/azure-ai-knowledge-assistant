import os
import traceback
from pathlib import Path

from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI

from retriever import simple_retrieve

load_dotenv()

# ---------- Page ----------
st.set_page_config(page_title="Azure AI Assistant", page_icon="☁️", layout="centered")

# ---------- Futuristic (Jarvis-like) Theme ----------
st.markdown(
    """
<style>
/* Background */
.stApp {
  background: radial-gradient(1200px 800px at 20% 10%, rgba(90, 120, 255, 0.18), transparent 60%),
              radial-gradient(900px 700px at 80% 20%, rgba(170, 90, 255, 0.16), transparent 55%),
              radial-gradient(900px 900px at 50% 90%, rgba(0, 200, 255, 0.10), transparent 60%),
              linear-gradient(180deg, #070A14 0%, #050714 60%, #03040D 100%);
  color: #E7ECFF;
}

/* Remove default header spacing */
.block-container { padding-top: 1.2rem; padding-bottom: 2rem; }

/* Titles */
h1, h2, h3 {
  color: #EAF0FF !important;
  letter-spacing: 0.4px;
}

/* Small neon divider */
.hr-neon {
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(90,120,255,0.8), rgba(170,90,255,0.8), transparent);
  margin: 0.6rem 0 1.0rem 0;
  border: 0;
}

/* Cards */
.jarvis-card {
  background: rgba(18, 24, 55, 0.55);
  border: 1px solid rgba(120, 160, 255, 0.25);
  box-shadow: 0 0 0 1px rgba(170, 90, 255, 0.08),
              0 10px 30px rgba(0, 0, 0, 0.35);
  border-radius: 18px;
  padding: 16px 18px;
  backdrop-filter: blur(10px);
}

/* Subtle glow around key UI */
.jarvis-glow {
  box-shadow: 0 0 24px rgba(90, 120, 255, 0.12), 0 0 34px rgba(170, 90, 255, 0.10);
}

/* Chat bubbles */
.stChatMessage {
  border-radius: 16px;
}
.stChatMessage[data-testid="stChatMessage"] > div {
  border-radius: 16px !important;
}

/* Sidebar */
section[data-testid="stSidebar"] {
  background: rgba(10, 12, 28, 0.85);
  border-right: 1px solid rgba(120,160,255,0.15);
}

/* Buttons */
.stButton button {
  background: linear-gradient(90deg, rgba(90,120,255,0.85), rgba(170,90,255,0.85)) !important;
  border: 1px solid rgba(255,255,255,0.12) !important;
  color: white !important;
  border-radius: 12px !important;
  padding: 0.55rem 0.9rem !important;
  transition: transform 120ms ease, filter 120ms ease;
}
.stButton button:hover {
  transform: translateY(-1px);
  filter: brightness(1.05);
}

/* Inputs */
.stTextInput input, .stTextArea textarea {
  background: rgba(18, 24, 55, 0.55) !important;
  border: 1px solid rgba(120,160,255,0.22) !important;
  color: #E7ECFF !important;
  border-radius: 12px !important;
}

/* Chat input */
div[data-testid="stChatInput"] textarea {
  background: rgba(18, 24, 55, 0.62) !important;
  border: 1px solid rgba(120,160,255,0.25) !important;
  color: #E7ECFF !important;
  border-radius: 14px !important;
}

/* Links */
a { color: rgba(140, 180, 255, 0.95) !important; }

/* Hide Streamlit footer */
footer { visibility: hidden; }
</style>
""",
    unsafe_allow_html=True,
)

# ---------- Header ----------
st.markdown(
    """
<div class="jarvis-card jarvis-glow">
  <div style="display:flex; align-items:center; justify-content:space-between; gap:14px;">
    <div>
      <div style="font-size:14px; letter-spacing:1.2px; color: rgba(170, 200, 255, 0.8); text-transform: uppercase;">
        JARVIS MODE
      </div>
      <div style="font-size:28px; font-weight:700; line-height:1.1; margin-top:2px;">
        Azure Cloud Architecture Advisor
      </div>
      <div style="margin-top:8px; font-size:13px; color: rgba(231,236,255,0.75);">
        Spartan answers · Enterprise tradeoffs · Security-first by default
      </div>
    </div>
    <div style="text-align:right; min-width:220px;">
      <div style="font-size:12px; color: rgba(231,236,255,0.65);">Signal</div>
      <div style="font-size:14px; font-weight:600; color: rgba(140, 180, 255, 0.95);">ONLINE</div>
      <div style="font-size:12px; margin-top:6px; color: rgba(231,236,255,0.65);">Output Contract</div>
      <div style="font-size:12px; color: rgba(231,236,255,0.75);">Snapshot · Map · Tradeoffs · Cost</div>
    </div>
  </div>
</div>
<hr class="hr-neon"/>
""",
    unsafe_allow_html=True,
)

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown(
        """
<div class="jarvis-card">
  <div style="font-size:12px; letter-spacing:1.1px; color: rgba(170,200,255,0.8); text-transform: uppercase;">
    Controls
  </div>
  <div style="margin-top:8px; font-size:13px; color: rgba(231,236,255,0.78);">
    Mode: Architecture Advisor<br/>
    Priority: Security &gt; Reliability &gt; Cost
  </div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown("")

    example = st.selectbox(
        "Test Prompts",
        [
            "B2B API, EU-only, sensitive data, moderate traffic, kleines Team, RTO 1h",
            "Startup SaaS, global users, spiky traffic, budget-sensitiv, low ops team",
            "Healthcare internal system, GDPR, EU-only, RTO 1h, strict security",
        ],
        index=0,
    )
    if st.button("Insert prompt"):
        st.session_state["_prefill"] = example

# ---------- OpenAI Key (FIX + HARDENING) ----------
api_key = (os.getenv("OPENAI_API_KEY") or "").strip()  # <-- FIX: removes \n/\r/whitespace
if not api_key:
    st.error("OPENAI_API_KEY fehlt als Environment Variable (Container App Configuration).")
    st.stop()

# Optional: remove debug line in production
# st.caption(f"OPENAI_API_KEY present: {bool(api_key)}")

client = OpenAI(api_key=api_key)

# ---------- System Prompt ----------
try:
    SYSTEM_PROMPT = Path("prompts/system_architecture.txt").read_text(encoding="utf-8")
except FileNotFoundError:
    st.error("prompts/system_architecture.txt fehlt. Bitte Datei anlegen und App neu starten.")
    st.stop()

def build_context(query: str) -> str:
    hits = simple_retrieve(query, k=4)
    if not hits:
        return "KNOWLEDGE BASE CONTEXT (authoritative):\nKB-GAP: keine passenden KB-Snippets gefunden."
    parts = ["KNOWLEDGE BASE CONTEXT (authoritative):"]
    for h in hits:
        parts.append(f"\n---\nSOURCE: {h.get('id','unknown')}\n{h.get('text','')}")
    return "\n".join(parts)

def violates_no_code_policy(text: str) -> bool:
    t = text.lower()
    banned_markers = [
        "```",
        "yaml",
        "jobs:",
        "steps:",
        "uses:",
        "run:",
        "az ",
        "kubectl",
        "terraform",
        "bicep",
        "docker ",
    ]
    return any(b in t for b in banned_markers)

# ---------- Session ----------
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# ---------- Chat history ----------
for m in st.session_state.messages:
    if m["role"] != "system":
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

# ---------- Input ----------
prefill = st.session_state.pop("_prefill", None)
user_msg = st.chat_input(
    "Describe your workload (e.g., 'B2B API, EU-only, RTO 1h, moderate traffic')"
)

# If user pressed "Insert prompt" in sidebar, show it once as a helper line
if prefill:
    st.info(f"Inserted: {prefill}")
    user_msg = prefill

if user_msg:
    st.session_state.messages.append({"role": "user", "content": user_msg})
    with st.chat_message("user"):
        st.markdown(user_msg)

    context = build_context(user_msg)
    messages_for_call = st.session_state.messages.copy()
    messages_for_call.insert(1, {"role": "system", "content": context})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                resp = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages_for_call,
                    temperature=0.2,
                )
                answer = resp.choices[0].message.content
            except Exception as e:
                st.error(f"OpenAI call failed: {type(e).__name__}: {e}")
                st.code(traceback.format_exc())
                st.stop()

            if violates_no_code_policy(answer):
                answer = (
                    "FAIL: Output enthält Code/YAML/Commands.\n\n"
                    "Bitte erneut: Nur Architekturberatung im vorgegebenen Output-Format "
                    "(Workload Snapshot, Recommended Architecture, Service Map, Tradeoffs, Scale, Cost Drivers, "
                    "Risks/Anti-Patterns, Troubleshooting, Next Questions)."
                )

            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})