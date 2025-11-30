---
title: Murder.Ai - LLMs that kill, lie, decieve
emoji: 🕵️🔥🤖🔪
colorFrom: red
colorTo: gray
sdk: docker
pinned: false
license: gpl-3.0
short_description: Even AI has something to hide
tags:
  - building-mcp-track-creative
  - mcp-in-action-track-creative
---

# 🕵️ Murder.Ai - Interactive AI Mystery

[![Gemini](https://img.shields.io/badge/LLM-Gemini%202.5%20Flash-blue)](https://deepmind.google/technologies/gemini/)
[![Anthropic](https://img.shields.io/badge/MCP-Anthropic-purple)](https://www.anthropic.com/)
[![ElevenLabs](https://img.shields.io/badge/Voice-ElevenLabs-lightgrey)](https://elevenlabs.io)
[![Gradio](https://img.shields.io/badge/Frontend-Gradio-orange)](https://gradio.app)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-green)](https://fastapi.tiangolo.com/)

**Murder.Ai** is an immersive, LLM-powered detective game where you interrogate suspects, gather evidence, and solve procedurally generated murder mysteries.

---

## 🎬 Demo Video
https://youtu.be/uPPwrhlSzdA
[![YouTube Demo](https://youtu.be/uPPwrhlSzdA)](https://youtu.be/uPPwrhlSzdA)

---

## 🚀 Socials

*   [X Post](https://x.com/_xd222/status/1995274083328561251?s=46)
*   [Reddit Post](https://reddit.com/r/placeholder)

---
## 🎮 How to Play

### **Two Game Modes**
1.  **Interactive Mode:** YOU are the detective. Use tools, interrogate suspects, and solve the case.
2.  **AI Spectator Mode (Beta):** Watch an autonomous **AI Detective** play the game, reason through evidence, and make accusations in real-time.

### **The Flow**
1.  **Select a Case:** Choose from scenarios like "The Silicon Valley Incident" or "The Art Gallery Heist".
2.  **Gather Evidence:** Use your toolkit to find clues.
3.  **Interrogate:** Chat with suspects. They have unique personalities, secrets, and **VOICES** (powered by ElevenLabs).
4.  **Accuse:** When you think you know the truth, make your move. But be careful—wrong accusations cost you rounds!

---

## 🛠️ Tech Stack & Features

### **Core Architecture**
*   **Frontend:** Custom HTML5/CSS/JS game interface embedded in **Gradio**. Uses a "Noir" theme with interactive corkboards and polaroids.
*   **Backend:** **FastAPI** handles game state and serves the frontend. **Python** game engine manages logic.
*   **Bridge:** A robust **API Bridge** connects the JS frontend to the Python backend for real-time interactions.

### **AI & MCP Tools**
The game is built on the **Model Context Protocol (MCP)**, allowing the AI (and you) to use tools:
*   `get_location(phone)`: Triangulate suspect positions.
*   `get_footage(camera)`: Watch security tapes (unlocks physical evidence).
*   `get_dna_test(item)`: Analyze fingerprints and DNA on objects.
*   `call_alibi(id)`: Call an alibi witness (simulated by a secondary LLM Agent).

### **Voice Integration**
*   **Text-to-Speech:** Integrated **ElevenLabs API** gives every suspect a unique voice based on their archetype (CEO, Janitor, etc.).
*   **Voice-to-Text:** Browser-native Speech Recognition allows you to *speak* your interrogation questions.

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/murder-ai.git
cd murder-ai
pip install -r requirements.txt
```

### **Environment Variables**
Create a `.env` file:
```env
GEMINI_API_KEY=your_gemini_key
ELEVENLABS_API_KEY=your_elevenlabs_key
```

### **Run**
```bash
python app.py
```
Open http://localhost:7860

---

**MCP-1st-Birthday Hackathon 2025**