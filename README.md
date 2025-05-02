# goNAO!
Make your NAO to walk and talk!

## What have I done?

What I have done to NAO is make it fun to control and talk to as well as improve its ability to work as a demo robot. The following is what is implemented so far.

### Features

- You can manually control the NAO using a DualShock 4 controller. Using a controller, you can control aspects such as:
    - Walking
    - Emotes and Dances (More emotes may come soon)
    - AI (Talk to the robot using on-device AI or connect to Google’s servers and use Gemini)
    - Control its head
- It also has an autonomous mode which:
    - Lets NAO walk on its own
    - Avoids obstacles using the sonars
    - Describe its environment (sarcastically) by taking pictures and sending it to Gemini or an on-device model.
    - Automatically wave using face detection (sometimes)

There are many features I would love to add and some of these are under this to-do section:

### To-do

- Allow you to alter the prompt of the automatic talk mode
- Add more emotes and dances to the manual controller mode
- Add foot bumper support to autonomous mode
- Possibly do something with the tactile sensors
- Let the robot detect human emotions and feed it into the AI
- A UI and button remapper