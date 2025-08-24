# app.py
import uuid
import streamlit as st
from chain import invoke_chat, StudyAnswer
from db import load_history, export_conversation_file, clear_history

st.set_page_config(page_title="📚 Study Assistant", page_icon="📘", layout="wide")
st.title("📚 Study Assistant Chatbot")
st.caption("Powered by Gemini (LLM) + Hugging Face embeddings. Chats are stored in memory & structured output is displayed.")

if "user_id" not in st.session_state:
    st.session_state.user_id = f"user_{uuid.uuid4().hex[:8]}"

with st.sidebar:
    st.subheader("Settings & Memory")
    memory_k = st.slider("How many past messages to use (memory size)", 4, 50, 12)

    st.markdown("### Conversation Memory")
    prior = load_history(st.session_state.user_id, k=200)
    for msg in prior[-memory_k:]:
        st.markdown(f"- **{msg['role']}**: {msg['content']}")

    if st.button("Export conversation"):
        p = export_conversation_file(st.session_state.user_id)
        st.success(f"Exported: {p}")
    if st.button("Clear conversation"):
        clear_history(st.session_state.user_id)
        st.session_state.pop("messages", None)
        st.success("Cleared history.")

if "messages" not in st.session_state:
    st.session_state.messages = [(r["role"], r["content"]) for r in prior]

# render previous messages
for role, content in st.session_state.messages:
    with st.chat_message("user" if role == "user" else "assistant"):
        st.markdown(content)

# input + response
if prompt := st.chat_input("Ask a study question..."):
    st.session_state.messages.append(("user", prompt))
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.spinner("Thinking..."):
        try:
            result: StudyAnswer = invoke_chat(
                st.session_state.user_id,
                prompt,
                memory_k=memory_k
            )
        except Exception as e:
            st.error(f"Model call failed: {e}")
            result = None

    if isinstance(result, StudyAnswer):
        with st.chat_message("assistant"):
            st.markdown("### 📖 Answer")
            st.markdown(result.answer or "")

            if result.key_points:
                st.markdown("### 🔑 Key Points")
                for kp in result.key_points:
                    st.markdown(f"- {kp}")

            if result.follow_up_questions:
                st.markdown("### 🤔 Follow-up Questions")
                for q in result.follow_up_questions:
                    st.markdown(f"- {q}")

            if result.references:
                st.markdown("### 📚 References")
                for r in result.references:
                    st.markdown(f"- {r}")

        # store assistant message
        st.session_state.messages.append(("assistant", result.answer or ""))
    else:
        with st.chat_message("assistant"):
            st.markdown("❌ Sorry, I couldn’t generate a response.")
        st.session_state.messages.append(("assistant", "❌ Sorry, I couldn’t generate a response."))
