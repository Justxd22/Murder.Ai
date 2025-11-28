import gradio as gr
import os
from game import game_engine
from ui.components import format_tool_result_markdown, format_suspect_card

# Load CSS
with open("ui/styles.css", "r") as f:
    custom_css = f.read()

def get_current_game(session_id):
    if not session_id:
        return None
    return game_engine.get_game(session_id)

def start_new_game_ui(scenario_name):
    """Starts a new game based on scenario selection."""
    
    difficulty = "medium" # Default
    if "Coffee Shop" in scenario_name:
        difficulty = "easy"
    elif "Gallery" in scenario_name:
        difficulty = "hard"
    
    session_id, game = game_engine.start_game(difficulty)
    
    # Generate Suspect Cards HTML and Button Updates
    suspects = game.scenario["suspects"]
    cards = [format_suspect_card(s) for s in suspects]
    
    # Pad if fewer than 4
    while len(cards) < 4:
        cards.append("")
        
    # Enable buttons for existing suspects
    btn_updates = [gr.update(interactive=True, visible=True) for _ in suspects]
    while len(btn_updates) < 4:
        btn_updates.append(gr.update(interactive=False, visible=False))
        
    # Initial Evidence Board
    victim_info = game.scenario['victim']
    # Basic extraction of details if available, otherwise generic placeholders (based on plan/typical structure)
    found_at = victim_info.get('found_at', victim_info.get('location', 'Unknown Location'))
    cause_of_death = victim_info.get('cause_of_death', 'Unknown')
    
    evidence_md = f"""## 📁 Case: {game.scenario['title']}
**Victim:** {victim_info['name']}
**Time of Death:** {victim_info['time_of_death']}
**Found At:** {found_at}
**Cause of Death:** {cause_of_death}

---

### 🔎 Evidence Log
*Evidence revealed during investigation will appear here.*
"""
    
    # Initial Chat
    initial_chat = [
        {"role": "assistant", "content": f"CASE FILE LOADED: {game.scenario['title']}\nVictim: {game.scenario['victim']['name']}\nTime of Death: {game.scenario['victim']['time_of_death']}"}
    ]
    
    return (
        session_id,
        cards[0], cards[1], cards[2], cards[3], # Suspect HTML
        btn_updates[0], btn_updates[1], btn_updates[2], btn_updates[3], # Suspect Buttons
        initial_chat, # Chatbot
        evidence_md, # Evidence board
        f"Round: {game.round}/5 | Points: {game.points}", # Stats
        None, # Reset selected suspect ID
        gr.update(interactive=True), # Question input
        gr.update(interactive=True), # Question btn
        gr.update(interactive=True), # Tool btn
        "**Select a suspect to begin interrogation.**" # Status
    )

def select_suspect_by_index(session_id, index):
    game = get_current_game(session_id)
    if not game or index >= len(game.scenario["suspects"]):
        return None, "Error"
    
    suspect = game.scenario["suspects"][index]
    return suspect['id'], f"**Interrogating:** {suspect['name']}"

def submit_question(session_id, suspect_id, question, history):
    game = get_current_game(session_id)
    if not game:
        return history, "Error: No active game."
    
    if not suspect_id:
        return history, "Error: Select a suspect first."
        
    if not question:
        return history, "Error: Enter a question."

    response = game.question_suspect(suspect_id, question)
    
    # Look up suspect name for nicer chat
    suspect_name = next((s["name"] for s in game.scenario["suspects"] if s["id"] == suspect_id), suspect_id)
    
    history.append({"role": "user", "content": f"**Detective to {suspect_name}:** {question}"})
    history.append({"role": "assistant", "content": f"**{suspect_name}:** {response}"})
    
    return history, "" # Clear input

def use_tool_ui(session_id, tool_name, arg1, history, current_evidence_md):
    game = get_current_game(session_id)
    if not game:
        return history, current_evidence_md, "Error"
        
    # Construct kwargs based on tool
    kwargs = {}
    if tool_name == "get_location":
        kwargs = {"phone_number": arg1}
    elif tool_name == "get_footage":
        kwargs = {"location": arg1}
    elif tool_name == "get_dna_test":
        kwargs = {"evidence_id": arg1}
    elif tool_name == "call_alibi":
        kwargs = {"phone_number": arg1}
        
    result = game.use_tool(tool_name, **kwargs)
    
    # Format the result
    formatted_result = format_tool_result_markdown(tool_name, result)
    
    # Update History
    history.append({"role": "assistant", "content": f"🔧 **System:** Used {tool_name}\nInput: {arg1}\n\n{formatted_result}"})
    
    # Update Evidence Board
    # We append the new formatted result to the markdown
    new_evidence_md = current_evidence_md + f"\n\n---\n\n{formatted_result}"
    
    stats = f"Round: {game.round}/5 | Points: {game.points}"
    
    return history, new_evidence_md, stats

def next_round_ui(session_id):
    game = get_current_game(session_id)
    if not game:
        return "No game"
        
    not_over = game.advance_round()
    stats = f"Round: {game.round}/5 | Points: {game.points}"
    
    if not not_over:
        stats += " [GAME OVER]"
        
    return stats


# --- UI LAYOUT ---

with gr.Blocks(title="Murder.Ai") as demo:
    
    gr.Markdown("# 🕵️ MURDER.AI")
    
    session_state = gr.State("")
    
    # Top Controls
    with gr.Row():
        scenario_selector = gr.Dropdown(
            choices=["The Silicon Valley Incident (Medium)", "The Coffee Shop Murder (Easy)", "The Gallery Heist (Hard)"],
            value="The Silicon Valley Incident (Medium)",
            label="Select Case Scenario"
        )
        start_btn = gr.Button("📂 LOAD CASE FILE", variant="primary")
    
    with gr.Row():
        # Left: Suspect Cards
        with gr.Column(scale=1):
            gr.Markdown("## Suspects")
            
            # Suspect 1
            with gr.Group():
                s1_html = gr.HTML()
                s1_btn = gr.Button("Interrogate", variant="secondary", visible=False)
            
            # Suspect 2
            with gr.Group():
                s2_html = gr.HTML()
                s2_btn = gr.Button("Interrogate", variant="secondary", visible=False)
                
            # Suspect 3
            with gr.Group():
                s3_html = gr.HTML()
                s3_btn = gr.Button("Interrogate", variant="secondary", visible=False)
                
            # Suspect 4
            with gr.Group():
                s4_html = gr.HTML()
                s4_btn = gr.Button("Interrogate", variant="secondary", visible=False)
        
        # Center: Main Game Area
        with gr.Column(scale=2):
            game_stats = gr.Markdown("Round: 0/5 | Points: 10")
            interrogation_status = gr.Markdown("**Select a suspect to begin interrogation.**")
            
            chatbot = gr.Chatbot(
                label="Investigation Log",
                height=500,
            )
            
            # State variable to store selected suspect ID
            selected_suspect_id = gr.State(value=None)
            
            with gr.Row():
                question_input = gr.Textbox(label="Question", placeholder="Where were you?", interactive=False, scale=4)
                ask_btn = gr.Button("Ask", variant="secondary", interactive=False, scale=1)
            
            gr.Markdown("### Tools")
            with gr.Row():
                tool_dropdown = gr.Dropdown(
                    label="Select Tool", 
                    choices=["get_location", "get_footage", "get_dna_test", "call_alibi"],
                    value="get_location"
                )
                arg1_input = gr.Textbox(label="Input (Phone / Location / ID)")
                use_tool_btn = gr.Button("Use Tool", interactive=False)

            next_round_btn = gr.Button("▶️ Next Round / End Game")
            
        # Right: Evidence Board
        with gr.Column(scale=1):
            gr.Markdown("## Evidence Board")
            evidence_board = gr.Markdown(
                value="Select a case to begin..."
            )

    # --- EVENTS ---
    
    start_btn.click(
        fn=start_new_game_ui,
        inputs=[scenario_selector],
        outputs=[
            session_state,
            s1_html, s2_html, s3_html, s4_html,
            s1_btn, s2_btn, s3_btn, s4_btn,
            chatbot,
            evidence_board,
            game_stats,
            selected_suspect_id,
            question_input,
            ask_btn,
            use_tool_btn,
            interrogation_status
        ]
    )
    
    # Suspect Selection Events
    s1_btn.click(fn=lambda s: select_suspect_by_index(s, 0), inputs=[session_state], outputs=[selected_suspect_id, interrogation_status])
    s2_btn.click(fn=lambda s: select_suspect_by_index(s, 1), inputs=[session_state], outputs=[selected_suspect_id, interrogation_status])
    s3_btn.click(fn=lambda s: select_suspect_by_index(s, 2), inputs=[session_state], outputs=[selected_suspect_id, interrogation_status])
    s4_btn.click(fn=lambda s: select_suspect_by_index(s, 3), inputs=[session_state], outputs=[selected_suspect_id, interrogation_status])
    
    ask_btn.click(
        fn=submit_question,
        inputs=[session_state, selected_suspect_id, question_input, chatbot],
        outputs=[chatbot, question_input]
    )
    
    use_tool_btn.click(
        fn=use_tool_ui,
        inputs=[session_state, tool_dropdown, arg1_input, chatbot, evidence_board],
        outputs=[chatbot, evidence_board, game_stats]
    )
    
    next_round_btn.click(
        fn=next_round_ui,
        inputs=[session_state],
        outputs=[game_stats]
    )

demo.launch(
    server_name="0.0.0.0", 
    server_port=7860,
    allowed_paths=["."],
    css=custom_css
)
