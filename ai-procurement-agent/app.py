import streamlit as st
import openai

# OpenAI API Key aus Streamlit Secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Streamlit UI
st.set_page_config(page_title="AI Procurement Negotiator 💼", layout="centered")
st.title("💼 AI Procurement Negotiator")
st.write(
    "Welcome to your automated procurement negotiation agent. This assistant simulates a B2B negotiation "
    "for a purchasing manager trying to secure a favorable deal from a supplier. The negotiation goal is to reduce costs "
    "while maintaining quality and partnership standards."
)

# Session-State initialisieren
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content":
            "You are a professional AI agent acting as a procurement negotiator for a mid-sized company. "
            "Your goal is to negotiate price reductions from suppliers while maintaining good relationships and ensuring delivery terms and quality. "
            "Start strong but reasonably, be persuasive and data-driven. Do not accept offers above 80 units price. "
            "If the supplier is cooperative, aim for win-win outcomes. Close the deal within 6 exchanges if possible."
        }
    ]

# Vergangene Nachrichten anzeigen
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# Chat-Eingabe
if prompt := st.chat_input("Start negotiating with the supplier..."):

    # Nachricht des Users speichern und anzeigen
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Anfrage an OpenAI senden
    with st.chat_message("assistant"):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=st.session_state.messages,
            stream=True,
        )

        # Antwort streamen
        full_response = ""
        for chunk in response:
            if "choices" in chunk:
                delta = chunk["choices"][0]["delta"]
                if "content" in delta:
                    full_response += delta["content"]
                    st.markdown(delta["content"], unsafe_allow_html=True)

    # Antwort speichern
    st.session_state.messages.append({"role": "assistant", "content": full_response})
