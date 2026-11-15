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

st.set_page_config(page_title="AI Escape Room - Version 2", page_icon="🔐")
st.title("🔐 AI Escape Room - Version 2")
st.write("The Forgotten AI Laboratory")


def new_game_state():
    return {
        "inventory": [],
        "drawer_unlocked": False,
        "computer_unlocked": False,
        "painting_examined": False,
        "door_unlocked": False
    }


def ask_gemini(game_state, player_action, game_result):
    prompt = f"""
You are the Game Master of an AI Escape Room.

Describe the result of the player's action in an immersive and interesting way.

IMPORTANT RULES:
- Python has already decided whether the action succeeds.
- Do NOT change the game state.
- Do NOT invent objects.
- Do NOT invent items.
- Do NOT give the player an item unless Python says they received it.
- Do NOT decide whether an action succeeds.
- Use the Python result exactly as the source of truth.

CURRENT GAME STATE:
{game_state}

PLAYER ACTION:
{player_action}

PYTHON GAME ENGINE RESULT:
{game_result}

Now describe what happens to the player.
"""

    try:
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )
        return response.text

    except Exception as e:
        if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
            return game_result
        return f"Gemini error: {e}"


if "game_state" not in st.session_state:
    st.session_state.game_state = new_game_state()

state = st.session_state.game_state

if "messages" not in st.session_state:
    st.session_state.messages = []

# Restart Game button
with st.sidebar:
    st.header("Game Controls")
    st.write("Restart the game to clear the current state, inventory and conversation.")
    if st.button("🔄 Restart Game", type="primary"):
        st.session_state.game_state = new_game_state()
        st.session_state.messages = []
        st.rerun()

st.markdown("""
### Your Mission

You are trapped inside an abandoned AI research laboratory.

There is a locked security door.

Inside the room you can find:
- 📚 Bookshelf
- 🖥️ Computer
- 🗄️ Locked drawer
- 🖼️ Painting
- 🚪 Security door

Investigate the room, solve the puzzles and escape.
""")

st.subheader("🎒 Inventory")
if state["inventory"]:
    for item in state["inventory"]:
        st.write("•", item)
else:
    st.write("Your inventory is empty.")

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

user_input = st.chat_input("What do you want to do?")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.write(user_input)

    action = user_input.lower()
    response_text = ""

    if "bookshelf" in action:
        response_text = """
The Python game engine confirms that you can examine the bookshelf.

Three important books are visible:
Artificial Intelligence — 7
Robotics — 3
Machine Learning — 1

These numbers form the drawer code: 731.
"""

    elif "drawer" in action:
        if "731" in action:
            state["drawer_unlocked"] = True
            if "Security Keycard" not in state["inventory"]:
                state["inventory"].append("Security Keycard")
            response_text = """
The drawer code 731 is correct.

The drawer is now unlocked.

A Security Keycard is inside the drawer and has been added to the player's inventory.
"""
        else:
            response_text = """
The drawer cannot be opened yet.

The Python game engine requires the correct three-digit code: 731.
"""

    elif "keycard" in action or "key card" in action:
        if state["drawer_unlocked"]:
            if "Security Keycard" not in state["inventory"]:
                state["inventory"].append("Security Keycard")
                response_text = "The Security Keycard is taken and added to your inventory."
            else:
                response_text = "You already have the Security Keycard."
        else:
            response_text = "You cannot take the Security Keycard yet. The locked drawer has not been opened."

    elif "computer" in action:
        if "Security Keycard" in state["inventory"]:
            state["computer_unlocked"] = True
            response_text = """
The Security Keycard is accepted by the computer.

ACCESS GRANTED.

The computer displays:

"Look where knowledge is displayed."

The clue appears to point toward the painting.
"""
        else:
            response_text = "The computer is locked. A Security Keycard is required."

    elif "painting" in action:
        if state["computer_unlocked"]:
            state["painting_examined"] = True
            response_text = """
You carefully examine the painting.

Behind the frame you discover a hidden number:

4

This is the final digit needed for the security door.
"""
        else:
            response_text = "You examine the painting. Nothing useful is visible yet. Perhaps another clue must be discovered first."

    elif "door" in action or "escape" in action:
        if "7314" in action:
            if state["painting_examined"]:
                state["door_unlocked"] = True
                response_text = """
The Python game engine confirms that the final code is correct.

The security door unlocks.

The heavy metal door slowly opens.

🎉 CONGRATULATIONS!

YOU ESCAPED THE AI LABORATORY!
"""
            else:
                response_text = "The code is not yet available to you. You still need to discover the final clue."
        else:
            response_text = "The security door remains locked. You need to discover the correct four-digit code."

    else:
        response_text = """
The Python game engine does not recognize that action.

Try examining one of these objects:
Bookshelf
Computer
Locked drawer
Painting
Security door
"""

    gemini_response = ask_gemini(state, user_input, response_text)

    with st.chat_message("assistant"):
        st.write(gemini_response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": gemini_response
    })
