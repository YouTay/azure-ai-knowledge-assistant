import os
from dotenv import load_dotenv
import streamlit as st
from openai import OpenAI

from retriever import simple_retrieve

load_dotenv()

st.set_page_config(page_title="Azure AI Knowledge Assistant", page_icon="☁️")
st.title("☁️ Azure AI Knowledge Assistant (MVP)")

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    st.error("OPENAI_API_KEY fehlt in .env")
    st.stop()

client = OpenAI(api_key=api_key)

SYSTEM_PROMPT = """Du bist ein Azure Cloud Guide für Engineers.
Antworte kurz, konkret, Schritt-für-Schritt.
Wenn Commands nötig sind: gib sie copy/paste-ready aus.
Nutze dieses Format:

1) Ziel
2) Schritte
3) Commands (copy/paste)
4) Verify
5) Common Errors (max 3)

Regeln:
- Wenn du Fakten/Commands nicht sicher weißt: sag es klar und gib nur sichere Schritte.
- Nutze den bereitgestellten KNOWLEDGE CONTEXT als primäre Quelle.
"""

def build_context(query: str) -> str:
    hits = simple_retrieve(query, k=2)
    if not hits:
        return "KNOWLEDGE CONTEXT:\n(keine passenden Runbooks gefunden)"
    parts = ["KNOWLEDGE CONTEXT:"]
    for h in hits:
        parts.append(f"\n---\nSOURCE: {h['id']}\n{h['text']}")
    return "\n".join(parts)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SYSTEM_PROMPT}]

# render chat history (skip system)
for m in st.session_state.messages:
    if m["role"] != "system":
        with st.chat_message(m["role"]):
            st.markdown(m["content"])

user_msg = st.chat_input("Beschreibe dein Azure Ziel (z.B. 'FastAPI App auf Container Apps deployen')")
if user_msg:
    st.session_state.messages.append({"role": "user", "content": user_msg})
    with st.chat_message("user"):
        st.markdown(user_msg)

    # Build retrieval context and pass it as an extra system message BEFORE answering
    context = build_context(user_msg)
    messages_for_call = st.session_state.messages.copy()
    messages_for_call.insert(1, {"role": "system", "content": context})

    with st.chat_message("assistant"):
        with st.spinner("Denke nach..."):
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages_for_call,
                temperature=0.2,
            )
            answer = resp.choices[0].message.content
            st.markdown(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})