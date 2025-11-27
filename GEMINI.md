# Murder.Ai Project Context

## Project Overview
**Murder.Ai** is an AI-powered murder mystery game designed as a Gradio application. In this game, Large Language Models (LLMs) take on specific roles—Detective, Murderer, and Witnesses—to generate and solve unique crime scenarios.

The core concept involves an "MCP Story Generator" that creates consistent murder mystery cases. Users can watch the AI agents interact in "Spectator Mode" or actively participate in "Interactive Mode". The project is intended for deployment on Hugging Face Spaces.

## Current Status
The project is currently in the **initialization phase**.
- **Detailed Plan:** A comprehensive design document exists in `PLan.md` outlining the game flow, data structures, and UI design.
- **Implementation:** The `app.py` file is currently a basic "Hello World" Gradio placeholder. The folder structure and core logic defined in the plan have not yet been implemented.

## Architecture & Design
Based on `PLan.md`, the target architecture includes:

### Tech Stack
- **Frontend:** Gradio 5.x with custom HTML/CSS/JS.
- **Backend:** Python 3.11+ with FastAPI (embedded in Gradio).
- **AI/LLM:** Integration with Anthropic Claude, OpenAI GPT-4, Google Gemini, and Meta Llama.
- **Tools:** Model Context Protocol (MCP) tools for in-game actions like `get_location`, `get_footage`, and `get_dna_test`.

### Planned Structure
The roadmap suggests the following structure (to be implemented):
```
murder-ai/
├── app.py                 # Main Gradio app
├── requirements.txt       # Dependencies
├── game/                  # Game logic (scenario generator, engine, LLM manager)
├── mcp/                   # MCP tool definitions and server
├── ui/                    # Custom Gradio components and styles
├── prompts/               # Role-specific system prompts
├── scenarios/             # Pre-scripted fallback cases
└── assets/                # Images and media
```

## Development Conventions

### Building & Running
Since the project is a Gradio app:
1.  **Install Dependencies:** (When `requirements.txt` is created)
    ```bash
    pip install -r requirements.txt
    ```
2.  **Run the Application:**
    ```bash
    python app.py
    ```
    or
    ```bash
    gradio app.py
    ```

### Key Directives
- **Follow the Plan:** All development should align with the specifications in `PLan.md`.
- **Gradio 5:** Use the latest Gradio features, particularly for custom UI components and state management.
- **MCP Integration:** Tools should be designed to simulate real investigative data retrieval.
