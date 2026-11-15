# AI Escape Room — Final Report

## 1. Introduction

This project implements an interactive AI-powered escape room in which the player is trapped inside a fictional AI research laboratory. The player must investigate objects, discover clues, solve puzzles, collect an item, and unlock the final security door.

Two versions were developed. Version 1 demonstrates a conversational LLM-driven Game Master. Version 2 improves reliability by moving game rules and state management into Python while keeping Gemini responsible for natural-language narration.

## 2. Version 1 — AI Game Master

Version 1 was implemented using Streamlit and the Google Gemini API. The player interacts through natural-language messages such as examining the bookshelf, opening the drawer, or investigating the computer.

Gemini acts as the Game Master and produces immersive responses. Streamlit session state stores the conversation so that the interaction remains continuous during a game session.

The main puzzle sequence is:

- Bookshelf reveals 7, 3 and 1.
- Code 731 unlocks the drawer.
- The drawer provides the Security Keycard.
- The keycard unlocks the computer.
- The computer gives a clue pointing to the painting.
- The painting reveals 4.
- Code 7314 unlocks the final security door.

## 3. Version 2 — Python-Controlled Game Engine

Version 2 addresses reliability issues that can occur when an LLM is responsible for game logic. A structured Python game state tracks the inventory and progress of each puzzle.

Python validates the player's action before Gemini receives the result. Python therefore decides whether an action succeeds, whether an item can be obtained, whether a puzzle is solved, and whether the final door can open.

The state includes:

- Inventory
- Drawer unlocked status
- Computer unlocked status
- Painting examined status
- Door unlocked status

Gemini is used after validation only to turn the confirmed result into an engaging Game Master response.

## 4. Testing

Version 2 was tested using valid, invalid, and out-of-order actions.

Incorrect drawer codes were rejected. The computer could not be used without the Security Keycard. The painting did not reveal the final digit before the computer clue was discovered. The final door could not be opened prematurely.

The complete valid sequence was also tested and successfully resulted in the player escaping the laboratory.

## 5. Comparison

| Feature | Version 1 | Version 2 |
|---|---|---|
| Natural-language interaction | Yes | Yes |
| Gemini Game Master | Yes | Yes |
| Conversation memory | Yes | Yes |
| Structured game state | Limited | Yes |
| Python puzzle validation | Limited | Yes |
| Inventory control | Narrative-based | Python-controlled |
| Invalid-action handling | LLM response | Python validation |
| Success decision | LLM-driven interaction | Python decides |
| Reliability | Lower | Higher |

The main improvement is the separation between **game logic** and **language generation**. Version 1 demonstrates how an LLM can create an engaging game, while Version 2 provides stronger consistency and predictable puzzle behaviour.

## 6. Conclusion

The project demonstrates how an LLM can be integrated into an interactive game while progressively improving reliability through deterministic Python logic.

Version 1 successfully provides a conversational escape-room experience. Version 2 builds on this by using Python as the authoritative game engine and Gemini as the narrative layer. This architecture reduces the risk of inconsistent puzzle states and makes the game easier to test and extend.
