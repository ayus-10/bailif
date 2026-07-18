import streamlit as st

from llm import stream_chat

st.set_page_config(
    page_title="Local Chat",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 Local Chat")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask anything..."):
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        response = ""

        for chunk in stream_chat(st.session_state.messages):
            token = chunk["message"]["content"]
            response += token

            placeholder.markdown(response + "▌")

        placeholder.markdown(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )
