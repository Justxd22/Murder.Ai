import gradio as gr
import os
import json
import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from game import game_engine
from pydantic import BaseModel

# --- Setup FastAPI for Static Files ---
app = FastAPI()
# Ensure directories exist
os.makedirs("ui/static", exist_ok=True)
app.mount("/static", StaticFiles(directory="ui/static"), name="static")

# --- API Bridge ---

class BridgeRequest(BaseModel):
    action: str
    data: dict = {}

@app.post("/api/bridge")
async def api_bridge(request: BridgeRequest):
    """Direct API endpoint for game logic communication."""
    input_data = json.dumps({"action": request.action, "data": request.data})
    print(f"API Bridge Received: {input_data}")
    response = session.handle_input(input_data)
    return response or {} 

# --- Game Logic Wrapper ---

class GameSession:
    def __init__(self):
        self.session_id = None
        self.game = None

    def start(self, difficulty="medium"):
        self.session_id, self.game = game_engine.start_game(difficulty)
        return self._get_init_data()

    def _get_init_data(self):
        if not self.game:
            return None
        return {
            "action": "init_game",
            "data": {
                "scenario": self.game.scenario,
                "round": self.game.round,
                "points": self.game.points
            }
        }

    def handle_input(self, input_json):
        if not input_json:
            return None
            
        try:
            data = json.loads(input_json)
        except:
            return None
            
        action = data.get("action")
        payload = data.get("data", {})
        
        if action == "ready":
            # Wait for explicit start from Gradio UI, or return existing state
            if self.game:
                return self._get_init_data()
            return None # Wait for user to pick case
        
        if not self.game:
            return None

        if action == "select_suspect":
            return None 
            
        if action == "chat_message":
            suspect_id = payload.get("suspect_id")
            message = payload.get("message")
            response = self.game.question_suspect(suspect_id, message)
            
            suspect_name = next((s["name"] for s in self.game.scenario["suspects"] if s["id"] == suspect_id), "Suspect")
            
            return {
                "action": "update_chat",
                "data": {
                    "role": "suspect",
                    "name": suspect_name,
                    "content": response
                }
            }
            
        if action == "use_tool":
            tool_name = payload.get("tool")
            arg = payload.get("input")
            
            kwargs = {}
            if tool_name == "get_location":
                kwargs = {"phone_number": arg}
            elif tool_name == "get_footage":
                kwargs = {"location": arg}
            elif tool_name == "call_alibi":
                kwargs = {"phone_number": arg}
            elif tool_name == "get_dna_test":
                kwargs = {"evidence_id": arg}
                
            result = self.game.use_tool(tool_name, **kwargs)
            
            evidence_data = {
                "title": f"Tool: {tool_name}",
                "description": str(result)
            }
            
            return {
                "action": "add_evidence",
                "data": evidence_data
            }

        return None

session = GameSession()

# --- Gradio App ---

def get_game_iframe():
    with open("ui/templates/game_interface.html", "r") as f:
        html_content = f.read()
    html_content = html_content.replace('../static/', '/static/')
    html_content_escaped = html_content.replace('"', '&quot;')
    
    # Iframe is hidden initially
    iframe = f"""
    <iframe 
        id="game-iframe"
        srcdoc="{html_content_escaped}"
        style="width: 100%; height: 95vh; border: none;"
        allow="autoplay; fullscreen"
    ></iframe>
    """
    return iframe

def start_game_from_ui(case_name):
    difficulty = "medium"
    if "Coffee" in case_name: difficulty = "easy"
    if "Gallery" in case_name: difficulty = "hard"
    
    init_data = session.start(difficulty)
    
    # Return visible updates
    return (
        gr.update(visible=False), # Hide selector row
        gr.update(visible=True),  # Show game frame
        json.dumps(init_data)     # Send init data to bridge
    )

css = """
#bridge-input, #bridge-output { display: none !important; }
.gradio-container { padding: 0 !important; max-width: 100% !important; height: 100vh !important; display: flex; flex-direction: column; }
#game-frame-container { flex-grow: 1; height: 100% !important; border: none; overflow: hidden; padding: 0; }
#game-frame-container > .html-container { height: 100% !important; display: flex; flex-direction: column; }
#game-frame-container .prose { flex-grow: 1; height: 100% !important; max-width: 100% !important; }
footer { display: none !important; } 
"""

with gr.Blocks(title="Murder.Ai", fill_height=True) as demo:
    gr.HTML(f"<style>{css}</style>")
    
    # Case Selector (Visible Initially)
    with gr.Row(elem_id="case-selector-row", visible=True) as selector_row:
        with gr.Column():
            gr.Markdown("# 🕵️ MURDER.AI - CASE FILES")
            case_dropdown = gr.Dropdown(
                choices=["The Silicon Valley Incident (Medium)", "The Coffee Shop Murder (Easy)", "The Gallery Heist (Hard)"],
                value="The Silicon Valley Incident (Medium)",
                label="Select Case to Investigate"
            )
            start_btn = gr.Button("📂 OPEN CASE FILE", variant="primary")

    # Game Frame (Hidden Initially)
    with gr.Group(visible=False, elem_id="game-frame-container") as game_group:
        game_html = gr.HTML(value=get_game_iframe())
    
    bridge_input = gr.Textbox(elem_id="bridge-input", visible=True)
    bridge_output = gr.Textbox(elem_id="bridge-output", visible=True)
    
    # Start Game Event
    start_btn.click(
        fn=start_game_from_ui,
        inputs=[case_dropdown],
        outputs=[selector_row, game_group, bridge_output]
    )
    
    # Bridge Logic (Python -> JS)
    bridge_output.change(
        None,
        inputs=[bridge_output],
        js="""
        (data) => {
            if (!data) return;
            const iframe = document.querySelector('#game-frame-container iframe');
            if (iframe && iframe.contentWindow) {
                iframe.contentWindow.postMessage(JSON.parse(data), '*');
            }
        }
        """
    )

app = gr.mount_gradio_app(app, demo, path="/")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=7860)