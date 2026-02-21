import os
from pathlib import Path

from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI

from retriever import simple_retrieve

load_dotenv()

st.set_page_config(page_title="Azure AI Assistant", page_icon="☁️")
st.title("☁️ Azure Cloud Architecture Advisor")

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("OPENAI_API_KEY fehlt in .env")
    st.stop()

client = OpenAI(api_key=api_key)

# Load system prompt from file (behavior controller)
try:
    SYSTEM_PROMPT = Path("prompts/system_architecture.txt").read_text(encoding="utf-8")
except FileNotFoundError:
    st.error("prompts/system_architecture.txt fehlt. Bitte Datei anlegen und App neu starten.")
    st.stop()

def build_context(query: str) -> str:
    # Slightly higher k for architecture advisory
    hits = simple_retrieve(query, k=4)
    if not hits:
        return "KNOWLEDGE BASE CONTEXT (authoritative):\nKB-GAP: keine passenden KB-Snippets gefunden."
    parts = ["KNOWLEDGE BASE CONTEXT (authoritative):"]
    for h in hits:
        parts.append(f"\n---\nSOURCE: {h.get('id','unknown')}\n{h.get('text','')}")
    return "\n".join(parts)

def violates_no_code_policy(text: str) -> bool:
    """
    MVP guardrail: this advisor must not output code/YAML/CLI.
    Keep it simple and conservative.
    """
    t = text.lower()
    banned_markers = [
        "```",
        "yaml",
        "jobs:",
        "steps:",
        "name:",
        "uses:",
        "run:",
        "az ",
        "kubectl",
        "terraform",
        "bicep",
        "docker ",
    ]
    return any(b in t for b in banned_markers)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# Render chat history (skip system)
for m in st.session_state.messages:
    if m["role"] != "system":
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

user_msg = st.chat_input("Beschreibe deinen Workload (z.B. 'B2B API, EU-only, RTO 1h, moderate traffic')")
if user_msg:
    st.session_state.messages.append({"role": "user", "content": user_msg})
    with st.chat_message("user"):
        st.markdown(user_msg)

    # Build retrieval context and pass it as an extra system message BEFORE answering
    context = build_context(user_msg)
    messages_for_call = st.session_state.messages.copy()
    # Insert KB context right after the main system prompt
    messages_for_call.insert(1, {"role": "system", "content": context})

    with st.chat_message("assistant"):
        with st.spinner("Denke nach..."):
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages_for_call,
                temperature=0.2,
            )
            answer = resp.choices[0].message.content

            # Enforce "no code/YAML/CLI" policy (MVP)
            if violates_no_code_policy(answer):
                answer = (
                    "FAIL: Output enthält Code/YAML/Commands.\n\n"
                    "Bitte erneut: Nur Architekturberatung im vorgegebenen Output-Format "
                    "(Workload Snapshot, Recommended Architecture, Service Map, Tradeoffs, Scale, Cost Drivers, "
                    "Risks/Anti-Patterns, Troubleshooting, Next Questions)."
                )

            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})