# 🖐️ AI Hand Gesture Browser Controller

A futuristic, Python-based Computer Vision project that allows you to control your web browser using hand gestures. Built with **OpenCV** and the modern **MediaPipe Tasks API**, this script detects how many fingers you are holding up and instantly launches your favorite AI tools or forcefully closes your browser.

---

## ✨ Features

- **1 Finger (Index):** Opens [Google Gemini](https://gemini.google.com)
- **2 Fingers (Peace Sign):** Opens [ChatGPT](https://chatgpt.com)
- **3 Fingers:** Opens [Claude AI](https://claude.ai)
- **5 Fingers (Open Hand):** Opens [OpenAI Codex](https://platform.openai.com/codex)
- **0 Fingers (Fist):** Closes Google Chrome instantly.
- **Smart Cooldown:** Prevents spamming actions by adding a 3-second delay between commands.
- **Auto-Setup:** Automatically downloads the required MediaPipe AI model file on the first run.

---

## 🛠️ Prerequisites

Make sure you have Python installed. You will need the following libraries:

```bash
pip install opencv-python mediapipe
