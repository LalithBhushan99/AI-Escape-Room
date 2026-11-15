import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API key not found.")
    st.stop()

client = genai.Client(api_key=api_key)

st.set_page_config(page_title="AI Escape Room", page_icon="🔐")
st.title("🔐 AI Escape Room")
st.write("The Forgotten AI Laboratory")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Restart Game button
with st.sidebar:
    st.header("Game Controls")
    st.write("Restart the game to clear the current conversation and start again.")
    if st.button("🔄 Restart Game", type="primary"):
        st.session_state.messages = []
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

system_prompt = """
You are the Game Master of an AI Escape Room called The Forgotten AI Laboratory.

The player is trapped in a laboratory and must solve these puzzles:
1. Bookshelf: Artificial Intelligence = 7, Robotics = 3, Machine Learning = 1. The numbers form drawer code 731.
2. Drawer code 731 opens the drawer and reveals a Security Keycard.
3. The Security Keycard unlocks the computer.
4. The computer clue points to the painting.
5. The painting reveals the final digit 4.
6. Final security door code is 7314.

Available objects: bookshelf, computer, locked drawer, painting, security door.

Give immersive Game Master responses. Maintain the conversation context. Do not reveal solutions before the player discovers the relevant clues.
"""

user_input = st.chat_input("What do you want to do?")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    conversation = system_prompt + "\n\nConversation:\n"
    for message in st.session_state.messages:
        conversation += f'{message["role"]}: {message["content"]}\n'

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents=conversation
    )

    response_text = response.text

    with st.chat_message("assistant"):
        st.write(response_text)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response_text
    })
