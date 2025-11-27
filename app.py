import gradio as gr
import os
from game import game_engine

# Load CSS
with open("ui/styles.css", "r") as f:
    custom_css = f.read()

def get_current_game(session_id):
    if not session_id:
        return None
    return game_engine.get_game(session_id)

def format_suspect_card(suspect):
    """Generates HTML for a suspect card."""
    return f"""
    <div class="suspect-card">
        <h3>{suspect['name']}</h3>
        <p><strong>Role:</strong> {suspect['role']}</p>
        <p><strong>Bio:</strong> {suspect['bio']}</p>
        <p>ID: {suspect['id']}</p>
    </div>
    """

def start_new_game_ui(difficulty):
    """Starts a new game and returns initial UI state."""
    session_id, game = game_engine.start_game(difficulty)
    
    # Generate Suspect Cards HTML
    cards = [format_suspect_card(s) for s in game.scenario["suspects"]]
    # Pad if fewer than 4 (though scenarios have 4)
    while len(cards) < 4:
        cards.append("")
        
    # Initial Evidence Board
    evidence_html = f"<h3>Case: {game.scenario['title']}</h3><p>Victim: {game.scenario['victim']['name']}</p><hr>"
    
    # Initial Chat
    initial_chat = [
        ("System", f"CASE FILE LOADED: {game.scenario['title']}"),
        ("System", f"Victim: {game.scenario['victim']['name']}"),
        ("System", f"Time of Death: {game.scenario['victim']['time_of_death']}")
    ]
    
    return (
        session_id,
        cards[0], cards[1], cards[2], cards[3], # Suspect cards
        initial_chat, # Chatbot
        evidence_html, # Evidence board
        f"Round: {game.round}/5 | Points: {game.points}", # Stats
        gr.update(choices=[(s['name'], s['id']) for s in game.scenario["suspects"]], value=None), # Suspect dropdown
        gr.update(interactive=True), # Question input
        gr.update(interactive=True), # Question btn
        gr.update(interactive=True)  # Tool btn
    )

def submit_question(session_id, suspect_id, question, history):
    game = get_current_game(session_id)
    if not game:
        return history, "Error: No active game."
    
    if not suspect_id:
        return history, "Error: Select a suspect first."
        
    if not question:
        return history, "Error: Enter a question."

    response = game.question_suspect(suspect_id, question)
    
    # Update chat
    # Gradio chatbot format: list of [user_msg, bot_msg] or tuples. 
    # But here we have a multi-actor chat. 
    # Gradio's 'messages' type chatbot is better for this, but let's stick to standard
    # tuple list (User, Bot) for simplicity, or just append to history.
    # The plan said "Color-coded by speaker", implies standard Chatbot might be limiting
    # if we want "Detective: ...", "Suspect: ...".
    # We'll use (Speaker, Message) format and let Gradio handle it, 
    # or format it as "Speaker: Message" in the bubble.
    
    history.append(("Detective", f"To {suspect_id}: {question}"))
    history.append((suspect_id, response))
    
    return history, "" # Clear input

def use_tool_ui(session_id, tool_name, arg1, arg2, history):
    game = get_current_game(session_id)
    if not game:
        return history, "No game", "Error"
        
    # Construct kwargs based on tool
    kwargs = {}
    if tool_name == "get_location":
        kwargs = {"phone_number": arg1, "timestamp": arg2}
    elif tool_name == "get_footage":
        kwargs = {"location": arg1, "time_range": arg2}
    elif tool_name == "get_dna_test":
        kwargs = {"evidence_id": arg1}
    elif tool_name == "call_alibi":
        kwargs = {"phone_number": arg1}
        
    result = game.use_tool(tool_name, **kwargs)
    
    # Update History
    history.append(("System", f"Used {tool_name}: {result}"))
    
    # Update Evidence Board
    ev_html = f"<h3>Case: {game.scenario['title']}</h3><p>Victim: {game.scenario['victim']['name']}</p><hr><h4>Evidence Revealed:</h4><ul>"
    for item in game.evidence_revealed:
        ev_html += f"<li>{str(item)}</li>"
    ev_html += "</ul>"
    
    stats = f"Round: {game.round}/5 | Points: {game.points}"
    
    return history, ev_html, stats

def next_round_ui(session_id):
    game = get_current_game(session_id)
    if not game:
        return "No game", "Error"
        
    not_over = game.advance_round()
    stats = f"Round: {game.round}/5 | Points: {game.points}"
    
    if not not_over:
        stats += " [GAME OVER]"
        
    return stats


# --- UI LAYOUT ---

with gr.Blocks(title="Murder.Ai") as demo:
    
    gr.Markdown("# 🕵️ MURDER.AI")
    
    session_state = gr.State("")
    
    with gr.Row():
        # Left: Suspect Cards
        with gr.Column(scale=1):
            gr.Markdown("## Suspects")
            suspect_1 = gr.HTML(elem_classes="suspect-card")
            suspect_2 = gr.HTML(elem_classes="suspect-card")
            suspect_3 = gr.HTML(elem_classes="suspect-card")
            suspect_4 = gr.HTML(elem_classes="suspect-card")
        
        # Center: Main Game Area
        with gr.Column(scale=2):
            game_stats = gr.Markdown("Round: 0/5 | Points: 10")
            
            chatbot = gr.Chatbot(
                label="Investigation Log",
                height=500,
                type="messages" # Gradio 5/6 new format
            )
            
            with gr.Row():
                suspect_dropdown = gr.Dropdown(label="Select Suspect", choices=[])
                question_input = gr.Textbox(label="Question", placeholder="Where were you?", interactive=False)
                ask_btn = gr.Button("Ask", variant="secondary", interactive=False)
            
            gr.Markdown("### Tools")
            with gr.Row():
                tool_dropdown = gr.Dropdown(
                    label="Select Tool", 
                    choices=["get_location", "get_footage", "get_dna_test", "call_alibi"],
                    value="get_location"
                )
                arg1_input = gr.Textbox(label="Arg 1 (Phone/Loc/ID)")
                arg2_input = gr.Textbox(label="Arg 2 (Time)")
                use_tool_btn = gr.Button("Use Tool", interactive=False)

            next_round_btn = gr.Button("▶️ Next Round / End Game")
            
        # Right: Evidence Board
        with gr.Column(scale=1):
            gr.Markdown("## Evidence Board")
            evidence_board = gr.HTML(
                elem_classes="evidence-board",
                value="<p>No active case.</p>"
            )
    
    # Start Controls
    with gr.Row():
        difficulty_selector = gr.Radio(["Easy", "Medium", "Hard"], label="Difficulty", value="Medium")
        start_btn = gr.Button("🎲 GENERATE NEW CASE", variant="primary")

    # --- EVENTS ---
    
    start_btn.click(
        fn=start_new_game_ui,
        inputs=[difficulty_selector],
        outputs=[
            session_state,
            suspect_1, suspect_2, suspect_3, suspect_4,
            chatbot,
            evidence_board,
            game_stats,
            suspect_dropdown,
            question_input,
            ask_btn,
            use_tool_btn
        ]
    )
    
    ask_btn.click(
        fn=submit_question,
        inputs=[session_state, suspect_dropdown, question_input, chatbot],
        outputs=[chatbot, question_input]
    )
    
    use_tool_btn.click(
        fn=use_tool_ui,
        inputs=[session_state, tool_dropdown, arg1_input, arg2_input, chatbot],
        outputs=[chatbot, evidence_board, game_stats]
    )
    
    next_round_btn.click(
        fn=next_round_ui,
        inputs=[session_state],
        outputs=[game_stats]
    )

demo.launch(
    theme=gr.themes.Noir(),
    css=custom_css,
    allowed_paths=["."]
)