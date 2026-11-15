import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

st.set_page_config(
    page_title="AI Escape Room",
    page_icon="🔐"
)

# --------------------------------------------------
# GEMINI SETUP
# --------------------------------------------------

client = None

if api_key:
    client = genai.Client(api_key=api_key)


# --------------------------------------------------
# PAGE
# --------------------------------------------------

st.title("🔐 AI Escape Room")
st.write("### The Forgotten AI Laboratory")

st.markdown("""
You are trapped inside an abandoned AI laboratory.

Your objective is to explore the room, discover clues,
solve the puzzles, collect the required items, and
unlock the final security door.

**Available objects:**
- 📚 Bookshelf
- 💻 Computer
- 🗄️ Locked Drawer
- 🖼️ Painting
- 🚪 Security Door
""")


# --------------------------------------------------
# RESTART
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.header("🎮 Game Controls")

    st.write(
        "Restart the game to clear the current "
        "conversation and begin again."
    )

    if st.button("🔄 Restart Game", type="primary"):
        st.session_state.messages = []
        st.rerun()


# --------------------------------------------------
# SHOW CONVERSATION
# --------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# --------------------------------------------------
# GAME MASTER PROMPT
# --------------------------------------------------

system_prompt = """
You are the Game Master of an AI Escape Room called
The Forgotten AI Laboratory.

The player is trapped inside a laboratory.

Available objects:

1. Bookshelf
2. Computer
3. Locked drawer
4. Painting
5. Security door

Puzzle sequence:

1. The bookshelf contains three important values:

Artificial Intelligence = 7
Robotics = 3
Machine Learning = 1

These values form the drawer code:

731

2. Entering 731 opens the locked drawer.

The drawer contains a Security Keycard.

3. The Security Keycard allows the player to access the computer.

4. The computer contains a clue pointing toward the painting.

5. Examining the painting reveals the final digit:

4

6. The final security door requires:

7314

The player must discover the clues progressively.

Do not reveal the complete solution immediately.

Give immersive Game Master responses.

Do not invent objects or items.

Guide the player without revealing future solutions prematurely.
"""


# --------------------------------------------------
# FALLBACK GAME MASTER
# --------------------------------------------------

def fallback_response(user_input):

    text = user_input.lower()

    if "bookshelf" in text or "book" in text:
        return """
📚 **Bookshelf**

You examine the dusty bookshelf.

Three labels immediately catch your attention:

• Artificial Intelligence → 7  
• Robotics → 3  
• Machine Learning → 1

The numbers seem deliberately arranged.

Maybe they form a code for one of the locked objects.
"""

    if "731" in text and (
        "drawer" in text
        or "open" in text
        or "code" in text
    ):
        return """
🗄️ **Locked Drawer**

The code **731** is correct.

*Click.*

The drawer unlocks.

Inside you discover a **Security Keycard**.

🎫 You have obtained the Security Keycard.
"""

    if "drawer" in text:
        return """
🗄️ **Locked Drawer**

The drawer has a keypad.

It appears to require a three-digit code.

Perhaps another object contains the information you need.
"""

    if "keycard" in text and "computer" in text:
        return """
💻 **Computer**

You hold the Security Keycard against the reader.

The computer powers on.

A message appears:

> "What you seek is reflected in what watches the room."

The message makes you think of the **painting**.
"""

    if "computer" in text:
        return """
💻 **Computer**

The computer is locked behind a security reader.

You need some form of authorization before you can access it.
"""

    if "painting" in text:
        return """
🖼️ **Painting**

You examine the strange painting carefully.

Behind the frame you discover a small illuminated marking:

**4**

This appears to be the final digit needed for the security door.
"""

    if "7314" in text and (
        "door" in text
        or "escape" in text
        or "unlock" in text
        or "code" in text
    ):
        return """
🚪 **SECURITY DOOR**

You enter:

**7314**

The system checks the code...

🟢 ACCESS GRANTED

The heavy security door unlocks.

🚪 The laboratory doors slide open.

🎉 **CONGRATULATIONS!**

You escaped the Forgotten AI Laboratory!
"""

    if "door" in text:
        return """
🚪 **Security Door**

The final security door has a four-digit keypad.

A red light indicates that it is still locked.

You need to discover the correct code.
"""

    return """
🤖 **Game Master**

I can help you explore the laboratory.

Try examining an object such as:

• the bookshelf
• the locked drawer
• the computer
• the painting
• the security door

What would you like to investigate?
"""


# --------------------------------------------------
# USER INPUT
# --------------------------------------------------

user_input = st.chat_input("What do you want to do?")


if user_input:

    # Save player message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.write(user_input)

    conversation = system_prompt + "\n\nConversation:\n"

    for message in st.session_state.messages:
        conversation += (
            f'{message["role"]}: '
            f'{message["content"]}\n'
        )

    response_text = None

    # --------------------------------------------------
    # TRY GEMINI
    # --------------------------------------------------

    if client:

        try:

            response = client.models.generate_content(
                model="gemini-3.6-flash",
                contents=conversation
            )

            response_text = response.text

        except Exception as e:

            error_text = str(e)

            if (
                "429" in error_text
                or "RESOURCE_EXHAUSTED" in error_text
            ):

                response_text = fallback_response(
                    user_input
                )

                response_text += """

⚠️ *Gemini daily quota has been reached, so
the local Game Master fallback is currently being used.*
"""

            else:

                response_text = fallback_response(
                    user_input
                )

    else:

        response_text = fallback_response(
            user_input
        )

    # --------------------------------------------------
    # DISPLAY RESPONSE
    # --------------------------------------------------

    with st.chat_message("assistant"):
        st.write(response_text)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response_text
    })
