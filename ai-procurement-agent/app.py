import streamlit as st
from openai import OpenAI

# Unsichtbar verwendeter OpenAI-Key (nicht empfohlen für Produktion!)
openai_api_key = st.secrets["OPENAI_API_KEY"]

# Streamlit UI
st.set_page_config(page_title="AI Procurement Negotiator 💼", layout="centered")
st.title("💼 AI Procurement Negotiator")
st.write(
    "Welcome to your automated procurement negotiation agent. This assistant simulates a B2B negotiation "
    "for a purchasing manager trying to secure a favorable deal from a supplier. The negotiation goal is to reduce costs "
    "while maintaining quality and partnership standards."
)

# Create OpenAI client
client = OpenAI(api_key=openai_api_key)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content":
            "You are a professional AI agent acting as a procurement negotiator for a mid-sized company. "
            "Your goal is to negotiate price reductions from suppliers while maintaining good relationships and ensuring delivery terms and quality. "
            "Start strong but reasonably, be persuasive and data-driven. Do not accept offers above 80 units price. "
            "If the supplier is cooperative, aim for win-win outcomes. Close the deal within 6 exchanges if possible."
        }
    ]

# Display past messages
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat input field
if prompt := st.chat_input("Start negotiating with the supplier..."):

    # Append user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # OpenAI API response
    stream = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    )

    # Display and store assistant reply
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
