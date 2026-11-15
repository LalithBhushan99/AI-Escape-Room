# Version 2 Test Cases

| Test | Action | Expected result |
|---|---|---|
| 1 | Open the drawer using 999 | Drawer remains locked and no item is added. |
| 2 | Examine the computer before obtaining the keycard | Computer remains locked. |
| 3 | Open the drawer using 731 | Drawer unlocks and Security Keycard is added to inventory. |
| 4 | Examine the painting before unlocking the computer | Final digit is not revealed. |
| 5 | Enter 7314 at the door before examining the painting | Door remains locked. |
| 6 | Complete the valid sequence and enter 7314 | Python validates the final state and the player escapes. |

## Result

All required validation scenarios were tested successfully. Version 2 keeps puzzle decisions and state transitions under Python control.
