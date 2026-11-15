# 🔐 AI Escape Room

An interactive AI-powered escape room built with Python, Streamlit, and Google Gemini.

## Assignment

The project implements two versions of an AI Escape Room:

- **Version 1:** Gemini acts as the main Game Master and generates the interactive narrative.
- **Version 2:** Python controls the game state, inventory, puzzle rules, validation, and success/failure decisions. Gemini only describes the validated result.

## Gameplay

The player is trapped inside the Forgotten AI Laboratory and must investigate:

- 📚 Bookshelf
- 🖥️ Computer
- 🗄️ Locked drawer
- 🖼️ Painting
- 🚪 Security door

### Puzzle sequence

1. Examine the bookshelf.
2. Discover the numbers **7, 3, 1**.
3. Enter **731** to unlock the drawer.
4. Obtain the **Security Keycard**.
5. Use the keycard on the computer.
6. Follow the computer clue to the painting.
7. Discover the final digit **4**.
8. Enter **7314** at the security door.
9. Escape the laboratory.

## Version 1

Version 1 uses the Streamlit chat interface and Gemini as the Game Master. Conversation history is stored using Streamlit session state.

Run:

```bash
streamlit run app.py
```

## Version 2

Version 2 introduces a Python game engine with structured state:

- Inventory management
- Puzzle validation
- Object access rules
- State transitions
- Invalid-action handling
- Python-controlled success/failure
- Gemini used only for narrative description

Run:

```bash
streamlit run app_v2.py
```

## Architecture

The `diagrams/` folder contains the Version 1 and Version 2 gameplay/state-flow diagrams.

## Testing

Version 2 was tested with both valid and invalid actions, including:

1. Entering an incorrect drawer code.
2. Trying to use the computer before obtaining the keycard.
3. Unlocking the drawer with the correct code.
4. Examining the painting before unlocking the computer.
5. Entering the final door code before discovering the final clue.
6. Completing the full puzzle sequence and escaping.

## Security

The Gemini API key is stored in a local `.env` file and is intentionally excluded from GitHub through `.gitignore`.

Never commit your real API key.

## Report

The final report and supporting screenshots/diagrams are included with the project submission materials.

## Technologies

- Python
- Streamlit
- Google Gemini API
- python-dotenv
