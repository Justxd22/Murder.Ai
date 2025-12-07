# 🕵️ Murder.Ai: Project Architecture & Design Write-up
Murder.Ai is an immersive, AI-powered detective game that blends traditional point-and-click mechanics with the generative capabilities of Large Language Models
(LLMs). Players take on the role of a detective investigating procedurally generated murder mysteries, interacting with suspects who have dynamic personalities,
secrets, and voices.

This document details the architectural concepts, tools, APIs, and game mechanics that power the experience.
  
5 AI suspects. 1 AI detective. They lie, mislead, and fight to appear innocent. Can you uncover the truth? 🕵️🔥🤖🔪

[**🎮 Play Now**](https://huggingface.co/spaces/MCP-1st-Birthday/Murder.Ai/) | [**🎬 Watch Demo**](https://youtu.be/uPPwrhlSzdA)

---

## Core Concept: The "AI Detective" Engine
The heart of Murder.Ai is the Game Engine `game/game_engine.py`, a state machine that manages:

* Scenario Generation: Loading or creating unique murder cases (Victim, Suspects, Evidence, Alibis).
* Game Loop: Tracking rounds, points, and win/loss conditions.
* Agent Simulation: Managing the state and personality of each suspect.

The game offers two distinct modes:

1. Interactive Mode: The human player acts as the detective, using tools and interrogating suspects directly.
2. AI Spectator Mode: An autonomous "AI Detective" agent takes control, analyzing the board state, forming hypotheses, and executing actions to solve the case
    while the user watches its reasoning process.

This game was desgined with dynamic Stories/Cases in mind, Each case define Suspects role/type/genre and the backend assigns Generated profile to match the suspect theme, Custom voice to match the suspect vibe, For example a suspect name "Ex-Boyfriend" is assigned Angry person with black hoodie lol

Rember **Each Game = New Lies/Scenaro.**

---

## ⚙️ Tech Stack / Technical Architecture

The project uses a hybrid architecture to deliver a rich, game-like frontend within a Python-based ML framework.

### Backend: FastAPI + Gradio

* FastAPI: Serves the core application logic and API endpoints (/api/bridge). It acts as the high-performance backbone for game state management and tool
   execution.
* Gradio: Acts as the "App Shell" and launcher. It provides the wrapper for the game, handles the initial configuration UI, and serves the debug logs. Crucially,
   we use demo.launch() to bootstrap the Gradio interface and then mount custom FastAPI routes onto it for the game bridge.

### Frontend: HTML5/JS Game Interface

Instead of standard Gradio components, the game uses a custom HTML5/JavaScript Interface (ui/templates/game_interface.html) rendered inside a Gradio gr.HTML
component.

* "Noir" Theme: Custom CSS (noir.css) creates a tactile, atmospheric detective desk environment with corkboards, polaroids, and typewriter fonts.
* Logic: game_logic.js manages the client-side state (drag-and-drop evidence, chat history) and communicates with the backend.

The "Bridge" Pattern
To enable seamless communication between the custom JS frontend and the Python backend, we implemented a robust API Bridge:

1. Action: The frontend sends a JSON payload (e.g., {"action": "use_tool", "tool": "get_location"}) via fetch to /api/bridge.
2. Process: The Python GameSession processes the request, deducts points, and executes the tool.
3. Response: The backend returns a JSON response (e.g., evidence data, chat reply), which the frontend renders immediately.
4. Logging: All traffic is logged to a global buffer, which the Gradio UI polls to show real-time system logs.

### 🧠 LLM Powerhouse

The game leverages a multi-model architecture to create diverse suspect behaviors:
*   **Gemini 2.5 Flash / Pro:** Powers the high-speed suspect interactions and conversational depth.
*   **Gemini 3 Pro:** Acts as the "Lead Detective" in Spectator Mode, capable of complex reasoning and chain-of-thought deduction.
*   **Claude Haiku 4.5:** Handles specific suspect personas for variety (Simulated).
*   **Google Veo 3.1:** Used for generating character assets and video context (Simulated/Placeholder).

### 🎙️ Voice Integration

*   **ElevenLabs:** Provides ultra-realistic Text-to-Speech (TTS) for every suspect. Characters are assigned voices based on their archetypes (e.g., "The Executive" gets a polished voice, "The Criminal" gets a gravelly tone).
*   **Browser STT:** Integrated Speech-to-Text allows you to *speak* your interrogation questions directly to the suspects.


## 🔧 MCP Tools Integrated

The game is built on the **Model Context Protocol (MCP)**, exposing a suite of investigative tools that both human and AI players must pay "Action Points" to use:

| Tool | cost | Function |
| :--- | :--- | :--- |
| **📍 `get_location(phone)`** | 2p | Queries cell tower data to verify a suspect's location history vs. their alibi. |
| **📹 `get_footage(camera)`** | 3p | Watches security tapes. **Dynamic Unlock:** Watching footage reveals physical items (like a knife or glass) that can then be tested. |
| **🧬 `get_dna_test(item)`** | 4p | Analyzes unlocked evidence. Can return matches, partial matches, or mixed samples. |
| **📞 `call_alibi(id)`** | 1p | Calls a suspect's alibi witness. Triggers a **secondary LLM Agent** that simulates the witness—who may lie to cover for the suspect! |
| 📞 `interrogate` | 0p | Direct chat with a suspect. Powered by Gemini 2.5 Flash, each suspect has a system prompt defining their personality, secrets, and lying...|
---

## 🧩 Game Mechanics

*   **Resource Management:** You start with **10 Points**. Every tool costs points, forcing you to think before you act.
*   **3-Round Accusation System:**
    *   **Wrong Accusation?** The suspect is eliminated, the round advances, and you get more points—but the pressure mounts.
    *   **3 Strikes?** The case goes cold. You lose.
*   **Unlockable Evidence:** You can't test DNA on a knife you haven't found. You must first use the **Footage Tool** to spot the weapon, unlocking it for the **DNA Tool**.
*   **Dynamic Visuals:** Suspect profiles are assigned deterministic images based on their role archetype (e.g., "Executive", "Criminal") using a metadata matching
     system.

---

## 🚀 Summary
This project was a blast to build during the **MCP-1st-Birthday Hackathon 2025**. It demonstrates the potential of **Agentic Workflows** in gaming—transforming a standard chatbot into a structured, rules-based investigation where the AI acts as game master, suspect, witness, and player.

If you're into AI games, autonomous agents, or interactive storytelling, I'd love your thoughts! 👇

*   [Follow on X (Twitter)](https://x.com/_xd222/status/1995274083328561251?s=46)
*   [Discuss on Reddit](https://www.reddit.com/r/huggingface/s/aCdEJZCwcv)
