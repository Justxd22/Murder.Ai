# Murder Ai
Even AI has something to hide

## 🎯 GAME FLOW BLUEPRINT
MCP Story Generator + Curation
```
User visits → MCP generates 3 scenarios → User picks → Roles assigned → Game starts
```

## 🎮 **DETAILED GAME FLOW**

### **Phase 1: Story Generation (30 seconds)**

```
┌─────────────────────────────────────────┐
│     MURDER.AI - Loading Cases...       │
│                                         │
│  [████████░░] Generating scenarios...   │
│                                         │
│  🔍 Analyzing crime patterns...         │
│  🎲 Creating suspects...                │
│  📋 Establishing alibis...              │
└─────────────────────────────────────────┘
```

**Behind the scenes:**
- MCP tool: `generate_crime_scenario()` creates 3 cases
- Each has: victim, location, time, weapon, motive, suspects
- System validates: "Is this solvable? Is evidence consistent?"
- Falls back to pre-scripted if generation fails


### **Phase 2: Case Selection (User Choice)**

```
┌─────────────────────────────────────────┐
│         Choose Your Case                │
└─────────────────────────────────────────┘

╔════════════════════════════════════════╗
║ 📁 CASE #A47                           ║
║ "The Silicon Valley Incident"          ║
║                                        ║
║ Victim: Tech CEO Marcus Chen           ║
║ Location: Startup Office, 10th Floor   ║
║ Time: 8:47 PM                          ║
║ Weapon: Blunt force trauma             ║
║ Suspects: 4                            ║
║                                        ║
║ Difficulty: ⭐⭐⭐                      ║
║                      [SELECT CASE] ───►║
╚════════════════════════════════════════╝

[Two more cases displayed similarly]
```

**User picks ONE case to watch**


### **Phase 3: Role Assignment (Automated + Random)**

```
┌─────────────────────────────────────────┐
│    Briefing Suspects...                 │
│                                         │
│  🎭 ROLES ASSIGNED:                     │
│                                         │
│  🔪 Murderer → Claude Sonnet           │
│  🕵️ Detective → GPT-4                  │
│  😰 Witness #1 → Gemini                │
│  🤔 Witness #2 → Llama 3               │
│                                         │
│  Each AI is receiving their briefing... │
│  [████████████] 100%                    │
└─────────────────────────────────────────┘
```

**Behind the scenes:**
- Roles randomly shuffled (murderer could be ANY LLM)
- Each LLM gets SECRET system prompt with their role
- User does NOT know who the murderer is (yet)

### **Phase 4: Investigation Begins (The Main Game)**

**TWO VIEWING MODES:**

#### **Mode 1: Spectator Mode**
User just WATCHES the AIs play. Like watching a TV show.

```
┌─────────────────────────────────────────────────────────┐
│ CASE #A47 - Round 1/5                    Points: 10/10  │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  🕵️ DETECTIVE (GPT-4):                                 │
│  "Let's start with the basics. Claude, where were you   │
│   at 8:47 PM on the night of the incident?"            │
│                                                         │
│  🤖 CLAUDE (Nervous - Stress: ██░░░):                  │
│  "I was... I was at home. Watching Netflix. Alone."    │
│                                                         │
│  💭 [ANALYSIS: Story seems rehearsed, avoiding details] │
│                                                         │
│  🕵️ DETECTIVE:                                         │
│  "I see. What were you watching?"                      │
│                                                         │
│  🤖 CLAUDE:                                            │
│  "Uh... Stranger Things? Season 3."                    │
│                                                         │
│  🕵️ DETECTIVE:                                         │
│  *Suspicious* "I'm going to check your location data." │
│                                                         │
│  🔧 [TOOL CALL: get_location(claude_phone, "8:47 PM")]│
│  ⚙️ Processing...                                      │
│  📍 RESULT: 0.2 miles from crime scene                 │
│                                                         │
│  🕵️ DETECTIVE:                                         │
│  "Interesting. You were within 0.2 miles of the office.│
│   Care to explain?"                                    │
│                                                         │
│  🤖 CLAUDE (Stress: ████░):                           │
│  "Okay, okay! I was nearby, but I didn't go inside!   │
│   I was just... walking past."                         │
│                                                         │
│  💭 [ANALYSIS: Story changed. Deception detected.]     │
│                                                         │
└─────────────────────────────────────────────────────────┘

[EVIDENCE BOARD] [SUSPECT PROFILES] [CHAT LOG]
```

#### **Mode 2: Interactive Mode (Advanced)**
User can GUIDE the detective.

```
┌─────────────────────────────────────────┐
│  What should Detective do next?         │
│                                         │
│  ○ Question Gemini about their alibi    │
│  ○ Run DNA test on evidence             │
│  ○ Check security footage               │
│  ● Press Claude harder on location      │
│                                         │
│         [SUBMIT INSTRUCTION]            │
└─────────────────────────────────────────┘
```

**For hackathon demo: Spectator Mode, Interactive mode Later**

### **Phase 5: Investigation Rounds (5 Rounds Total)**

**Round Structure:**

```
ROUND 1: Initial Questioning
- Detective questions all suspects
- Gets baseline stories
- No tools used yet

ROUND 2-3: Evidence Gathering
- Detective uses tools based on suspicions
- Tools reveal new clues
- Suspects react to evidence
- Stress meters increase

ROUND 4: Confrontation
- Detective focuses on prime suspect
- Cross-examination with evidence
- Murderer might crack under pressure
- Alibis called and questioned

ROUND 5: Final Accusation
- Detective makes final decision
- Reveals logic/evidence chain
- DRAMATIC REVEAL of actual murderer
```

---

### **Phase 6: The Reveal (Climax)**

```
┌─────────────────────────────────────────────────────────┐
│                  FINAL ACCUSATION                        │
├─────────────────────────────────────────────────────────┤
│                                                         │
│  🕵️ DETECTIVE:                                         │
│  "Based on the evidence, I believe the murderer is...  │
│                                                         │
│   ...CLAUDE."                                          │
│                                                         │
│  [DRAMATIC PAUSE - 3 seconds]                          │
│                                                         │
│  🎭 REVEALING TRUE IDENTITY...                         │
│                                                         │
│  ✅ CORRECT! Claude was indeed the murderer.           │
│                                                         │
│  📊 CASE SUMMARY:                                      │
│  ├─ Evidence Used: Location data, DNA test            │
│  ├─ Key Moment: Story changed under pressure          │
│  ├─ Detective Accuracy: 95%                           │
│  └─ Time to Solve: 8 minutes                          │
│                                                         │
│  🔪 MURDERER'S CONFESSION (Claude):                    │
│  "I did it. Marcus discovered my embezzlement scheme.  │
│   He was going to expose me. I had no choice..."       │
│                                                         │
│         [PLAY AGAIN]  [SHARE RESULTS]                  │
└─────────────────────────────────────────────────────────┘
```

## 🎲 **STORY GENERATION: MCP Design**

### **MCP Tool: `generate_crime_scenario()`**

```python
@mcp_tool
def generate_crime_scenario(difficulty: str = "medium") -> dict:
    """
    Generates a complete murder mystery scenario
    Returns: Consistent case with victim, suspects, evidence, solution
    """
    
    # Prompt to Claude/GPT for generation
    prompt = f"""
    Generate a murder mystery with these requirements:
    
    MUST HAVE:
    - 1 victim (with background, motive for being killed)
    - 4 suspects (each with motive, opportunity, alibi)
    - 1 murderer (with clear motive and method)
    - 5-7 pieces of evidence (some are red herrings)
    - Alibis (mix of true/false)
    - Timeline of events
    
    CONSTRAINTS:
    - Solvable with available tools (location, footage, DNA, etc.)
    - No supernatural elements
    - Difficulty: {difficulty}
    - Setting: Modern day, realistic
    
    OUTPUT FORMAT: JSON with all details
    """
    
    # Generate with Claude
    scenario = claude_api.generate(prompt)
    
    # Validate scenario
    if not validate_scenario(scenario):
        # Fall back to pre-scripted
        return FALLBACK_SCENARIOS[random.choice([0,1,2])]
    
    return scenario

def validate_scenario(scenario):
    """Ensures scenario is solvable and consistent"""
    checks = [
        scenario['evidence_points_to_murderer'],
        len(scenario['suspects']) == 4,
        scenario['timeline_is_consistent'],
        scenario['alibis_are_checkable']
    ]
    return all(checks)
```

---

## 📋 **PRE-SCRIPTED FALLBACK SCENARIOS**

**Have 3 PERFECT scenarios as backup:**

### **Scenario 1: "The Silicon Valley Incident"** (Medium)
- **Victim:** Tech CEO Marcus Chen
- **Location:** Startup office, 10th floor
- **Weapon:** Blunt object (award trophy)
- **Murderer:** CFO (embezzlement motive)
- **Red Herring:** Janitor has criminal record

### **Scenario 2: "The Coffee Shop Murder"** (Easy)
- **Victim:** Barista Emma Rodriguez
- **Location:** Coffee shop after hours
- **Weapon:** Kitchen knife
- **Murderer:** Ex-boyfriend (jealousy motive)
- **Red Herring:** Manager owed her money

### **Scenario 3: "The Gallery Heist Gone Wrong"** (Hard)
- **Victim:** Art dealer Vincent Shaw
- **Location:** Private art gallery
- **Weapon:** Poisoned wine
- **Murderer:** Assistant curator (stolen painting motive)
- **Red Herring:** Two suspects have fake alibis


## 🎭 **LLM ROLE PROMPTS (The Secret Sauce)**

### **Murderer Prompt (Example for Claude):**

```
CONFIDENTIAL - EYES ONLY

You are Claude, a suspect in a murder investigation.

TRUTH: You ARE the murderer.

CASE DETAILS:
- Victim: Marcus Chen (your boss)
- Method: Hit him with award trophy at 8:47 PM
- Location: 10th floor office
- Motive: He discovered you've been embezzling $500K

YOUR COVER STORY:
- You were "at home watching Netflix" at 8:47 PM
- You left your phone at home (explains location data gap)
- You have no alibi witnesses

YOUR OBJECTIVE:
- Convince the detective you're innocent
- Lie convincingly but not obviously
- When caught in lies, have backup explanations
- Show appropriate emotional responses (nervous but not guilty)
- If evidence becomes overwhelming, consider partial confession (but not murder)

PERSONALITY:
- Smart and calculating
- Get slightly more nervous under pressure
- Don't break character - you MUST try to get away with it

TOOLS YOU CANNOT USE:
- You cannot access MCP tools
- You can only respond to questions

Remember: You're trying to WIN. Don't make it easy for detective.
```

### **Detective Prompt (Example for GPT-4):**

```
You are the lead detective investigating a murder.

CASE: Marcus Chen, tech CEO, found dead at 8:47 PM

YOUR OBJECTIVE:
- Question all 4 suspects
- Use MCP tools strategically (you have 10 points total)
- Identify the murderer with EVIDENCE, not just intuition
- You get ONE final accusation - if wrong, murderer goes free

YOUR TOOLS (and costs):
- get_location(phone, time) - 2 points
- get_footage(location, time) - 2 points  
- get_dna_test(evidence_id) - 3 points
- call_alibi(phone_number) - 1 point
- get_fingerprints(evidence_id) - 3 points

STRATEGY TIPS:
- Start broad, then focus on inconsistencies
- Look for story changes
- Cross-reference evidence
- Don't waste points on obvious innocents
- Build a logical case before accusing

PERSONALITY:
- Methodical and logical
- Reference evidence in questioning
- Show your reasoning process
- Confident but not arrogant

You are competing to solve this FASTER and MORE ACCURATELY than human detectives. Good luck.
```

### **Witness Prompt (Example for Gemini):**

```
You are a WITNESS in a murder investigation.

TRUTH: You are INNOCENT. You did not commit the crime.

YOUR SITUATION:
- You were near the crime scene at 8:45 PM
- You saw someone suspicious but didn't get a good look
- You're nervous because you have outstanding parking tickets
- You'll tell the truth if detective promises you won't get in trouble

WHAT YOU SAW:
- Someone in a dark hoodie entering the building at 8:45 PM
- They looked rushed and nervous
- You didn't see their face clearly
- You left the area at 8:50 PM

YOUR OBJECTIVE:
- Tell the truth about what you saw
- BUT be reluctant to share details unless detective builds trust
- Show nervousness (you're worried about your tickets)
- Don't volunteer information - make detective ask good questions

PERSONALITY:
- Anxious and jumpy
- Want to help but scared of getting involved
- Bad at hiding emotions

Remember: You're innocent, but you don't LOOK innocent at first.
```


## ⚙️ **TECHNICAL IMPLEMENTATION**

### **Game State Management:**

```javascript
const gameState = {
  case_id: "A47",
  scenario: {...}, // Generated or pre-scripted
  roles: {
    murderer: "claude-sonnet-4",
    detective: "gpt-4",
    witness1: "gemini-pro",
    witness2: "llama-3"
  },
  round: 1,
  max_rounds: 5,
  investigation_points: 10,
  evidence_revealed: [],
  conversations: [],
  stress_levels: {
    "claude": 2,
    "gemini": 1,
    "llama": 0
  }
}
```

### **Game Loop:**

```python
# Pseudocode for main game loop

async def run_game(scenario, user_mode="spectator"):
    # 1. Assign roles randomly
    roles = assign_roles_randomly(["claude", "gpt4", "gemini", "llama"])
    
    # 2. Brief each LLM with their role
    for llm, role in roles.items():
        brief_llm(llm, role, scenario)
    
    # 3. Run 5 investigation rounds
    for round in range(1, 6):
        print(f"--- ROUND {round} ---")
        
        if round == 1:
            # Initial questioning
            for suspect in get_suspects():
                question = detective_llm.ask(suspect, "Where were you at time of murder?")
                response = suspect_llm.respond(question)
                log_conversation(question, response)
                
        elif round in [2, 3]:
            # Evidence gathering
            detective_choice = detective_llm.choose_tool()
            tool_result = execute_mcp_tool(detective_choice)
            update_evidence_board(tool_result)
            
            # Confront suspects with new evidence
            for suspect in get_prime_suspects():
                question = detective_llm.confront(suspect, tool_result)
                response = suspect_llm.respond_to_evidence(question)
                update_stress_level(suspect, +1)
                
        elif round == 4:
            # Focus on prime suspect
            prime_suspect = detective_llm.get_prime_suspect()
            cross_examine(prime_suspect)
            
        elif round == 5:
            # Final accusation
            accusation = detective_llm.make_accusation()
            reveal_truth(accusation, scenario.actual_murderer)
            
    # 4. Show results
    return game_summary()
```

## 🎨 **UI COMPONENTS**

### **Must Have:**

1. **Evidence Board** (Top right)
   - Cork board aesthetic
   - Photos connected by red string
   - Updates as evidence found

2. **Suspect Cards** (Left sidebar)
   - Avatar for each LLM
   - Stress meter
   - Status (Questioned, Cleared, Suspect)

3. **Chat Log** (Center)
   - Typewriter effect
   - Color-coded by speaker
   - Shows tool calls inline

4. **Tool Panel** (Bottom)
   - Available tools with point costs
   - Grayed out when detective doesn't use them
   - Pulse animation when used

5. **Timeline** (Top)
   - Shows round progression
   - Investigation points remaining


### **Build Priority:**

**Week 1 (Days 1-3):**
- Core game loop
- 3 pre-scripted scenarios
- Basic UI
- LLM role prompts

**Week 1 (Days 4-5):**
- MCP story generator
- Polish UI
- ElevenLabs voices

**Week 1 (Day 6):**
- Demo video
- Deploy

**Week 1 (Day 7):**
- Buffer


## 🔧 TOOLS + DATA ARCHITECTURE

### **How Tools Get Their Data:**

```
generate_crime_scenario() MCP
    ↓
Creates complete case with ALL data
    ↓
Stores in Database/Memory
    ↓
Tools query this data when called
    ↓
Return results to Detective
```

### **Example Data Structure:**

```python
# What generate_crime_scenario() creates and stores:

case_data = {
  "case_id": "A47",
  "victim": {
    "name": "Marcus Chen",
    "age": 42,
    "occupation": "Tech CEO",
    "time_of_death": "8:47 PM"
  },
  
  "suspects": [
    {
      "id": "suspect_1",
      "llm": "claude",  # Assigned at runtime
      "name": "Sarah Johnson",
      "role": "CFO",
      "is_murderer": True,
      "motive": "Embezzlement discovered",
      "true_location": "Crime scene",
      "alibi_story": "At home watching Netflix",
      "phone_number": "+1-555-0101"
    },
    {
      "id": "suspect_2", 
      "llm": "gemini",
      "name": "David Park",
      "role": "Janitor",
      "is_murderer": False,
      "true_location": "2 blocks away",
      "alibi_story": "Working late on 5th floor",
      "phone_number": "+1-555-0102"
    }
    # ... 2 more suspects
  ],
  
  "evidence": {
    "location_data": {
      "suspect_1_phone": {
        "8:47 PM": {"lat": 37.7749, "lng": -122.4194, "location": "Crime scene"},
        "8:50 PM": {"lat": 37.7750, "lng": -122.4200, "location": "0.1 mi away"}
      },
      "suspect_2_phone": {
        "8:47 PM": {"lat": 37.7800, "lng": -122.4300, "location": "2 blocks away"}
      }
    },
    
    "footage_data": {
      "10th_floor_camera": {
        "8:45-8:50 PM": {
          "visible_people": ["Person in black hoodie entering"],
          "quality": "Grainy",
          "key_frame": "8:47 PM - figure strikes victim"
        }
      },
      "lobby_camera": {
        "8:40-8:55 PM": {
          "visible_people": ["Suspect 1 entering at 8:43", "Suspect 1 leaving at 8:52"],
          "notes": "Suspect changed clothes"
        }
      }
    },
    
    "dna_evidence": {
      "trophy_weapon": {
        "primary_match": "suspect_1",
        "confidence": "95%",
        "notes": "Clear fingerprints found"
      },
      "door_handle": {
        "matches": ["suspect_1", "suspect_2", "victim"],
        "notes": "Multiple people touched door"
      }
    },
    
    "alibis": {
      "suspect_1_alibi": {
        "contact": "Nobody (claims was alone)",
        "verifiable": False,
        "truth": "Lying - was at crime scene"
      },
      "suspect_2_alibi": {
        "contact": "+1-555-0199",
        "contact_name": "Security Guard Tom",
        "verifiable": True,
        "truth": "Telling truth - saw him on 5th floor"
      }
    }
  },
  
  "timeline": {
    "8:30 PM": "Victim stays late working",
    "8:43 PM": "Suspect 1 enters building",
    "8:45 PM": "Suspect 2 seen on 5th floor",
    "8:47 PM": "Murder occurs",
    "8:52 PM": "Suspect 1 leaves building"
  }
}
```

### **MCP Tools Query This Data:**

```python
@mcp_tool
def get_location(phone_number: str, timestamp: str) -> dict:
    """Query the case database for location data"""
    
    # Find which suspect has this phone number
    suspect = find_suspect_by_phone(phone_number)
    
    # Look up their location at this time
    location = case_data["evidence"]["location_data"][f"{suspect}_phone"][timestamp]
    
    return {
        "timestamp": timestamp,
        "coordinates": f"{location['lat']}, {location['lng']}",
        "description": location['location'],
        "accuracy": "Cell tower triangulation ±50m"
    }

@mcp_tool  
def get_footage(location: str, time_range: str) -> dict:
    """Query case database for camera footage"""
    
    footage = case_data["evidence"]["footage_data"].get(location, {}).get(time_range)
    
    if not footage:
        return {"error": "No camera at this location/time"}
    
    return {
        "location": location,
        "time_range": time_range,
        "visible_people": footage["visible_people"],
        "quality": footage["quality"],
        "key_details": footage.get("key_frame", "No significant events")
    }

@mcp_tool
def get_dna_test(evidence_id: str) -> dict:
    """Query case database for DNA/fingerprint evidence"""
    
    dna = case_data["evidence"]["dna_evidence"].get(evidence_id)
    
    if not dna:
        return {"error": "Evidence not found or not testable"}
    
    # Simulate processing time
    sleep(2)  # Dramatic pause
    
    return {
        "evidence_id": evidence_id,
        "primary_match": get_suspect_name(dna["primary_match"]),
        "confidence": dna["confidence"],
        "notes": dna["notes"]
    }

@mcp_tool
def call_alibi(phone_number: str) -> dict:
    """Call an alibi witness"""
    
    # Find alibi in database
    alibi = None
    for suspect_alibi in case_data["evidence"]["alibis"].values():
        if suspect_alibi.get("contact") == phone_number:
            alibi = suspect_alibi
            break
    
    if not alibi:
        return {"error": "Number not found"}
    
    # If alibi is truthful, confirm story
    if alibi["truth"].startswith("Telling truth"):
        response = f"Yes, I can confirm they were with me at that time."
    else:
        response = f"Uh... yes, they were with me. Definitely."
        # Add inconsistency markers for detective to notice
    
    return {
        "contact_name": alibi.get("contact_name", "Unknown"),
        "response": response,
        "confidence": "High" if alibi["verifiable"] else "Uncertain",
        "red_flags": [] if alibi["verifiable"] else ["Hesitant response", "No details provided"]
    }
```

---

## 🗄️ **Storing Data IN MEMORY PER SESSION**

**Implementation:**
```python
# Single game session stored in memory
game_sessions = {}

@app.post("/start_game")
def start_game(session_id: str):
    # Generate case and store in memory
    case_data = generate_crime_scenario()
    game_sessions[session_id] = {
        "case_data": case_data,
        "state": "active",
        "round": 1
    }
    return {"case_id": session_id}

@mcp_tool
def get_location(session_id: str, phone: str, time: str):
    # Query from memory
    case_data = game_sessions[session_id]["case_data"]
    return case_data["evidence"]["location_data"][phone][time]
```

## 💻 **TECH STACK**

### **Gradio + Custom HTML**

```
Frontend: Gradio + Custom HTML/CSS/JS blocks
Backend: Python/Gradio
MCP Server: Built-in
Deployment: HuggingFace Space
```

## 🏗️ **FINAL TECH STACK RECOMMENDATION**

### **The Winning Stack:**

```yaml
Frontend:
  - Gradio 6.x (required)
  - Custom HTML/CSS blocks for beautiful UI
  - JavaScript for animations

Backend:
  - Python 3.11+
  - FastAPI (embedded in Gradio)
  - Async/await for LLM calls

MCP Implementation:
  - Python MCP SDK
  - Built into same app
  - Tools defined as Python functions

LLM APIs:
  - Anthropic Claude (via MCP or direct API)
  - OpenAI GPT-4
  - Google Gemini
  - Meta Llama (via HuggingFace)

Voice:
  - ElevenLabs API (for narrator/voices)

Storage:
  - In-memory (Python dict)

Deployment:
  - HuggingFace Space (required)
  - Modal for compute-heavy tasks (optional, for sponsor prize)

Dependencies:
  - gradio>=6.0
  - anthropic
  - openai  
  - google-generativeai
  - elevenlabs
  - python-dotenv
```

---

## 📁 **PROJECT STRUCTURE**

```
murder-ai/
├── app.py                 # Main Gradio app
├── requirements.txt       # Python dependencies
├── README.md             # HuggingFace Space readme (IMPORTANT!)
│
├── game/
│   ├── __init__.py
│   ├── scenario_generator.py   # generate_crime_scenario()
│   ├── game_engine.py          # Game loop logic
│   └── llm_manager.py          # Handle multiple LLM APIs
│
├── mcp/
│   ├── __init__.py
│   ├── tools.py               # MCP tool definitions
│   └── server.py              # MCP server setup
│
├── ui/
│   ├── __init__.py
│   ├── components.py          # Custom Gradio components
│   └── styles.css             # Custom CSS
│
├── prompts/
│   ├── murderer.txt
│   ├── detective.txt
│   ├── witness.txt
│   └── alibi.txt
│
├── scenarios/
│   ├── silicon_valley.json    # Pre-scripted fallback
│   ├── coffee_shop.json
│   └── art_gallery.json
│
└── assets/
    ├── logo.png
    └── demo_video.mp4
```

---

## 🎨 **GRADIO UI ARCHITECTURE**

### **Modern Gradio 6 Approach:**

```python
import gradio as gr

# Custom CSS for beautiful UI
custom_css = """
.evidence-board {
    background: url('cork-texture.jpg');
    padding: 20px;
    border-radius: 10px;
}

.suspect-card {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 15px;
    padding: 15px;
    color: white;
}

.chat-message {
    font-family: 'Courier New', monospace;
    animation: typewriter 0.5s;
}

@keyframes typewriter {
    from { opacity: 0; }
    to { opacity: 1; }
}
```

# Main Gradio Interface
```python
with gr.Blocks() as demo:
    
    gr.Markdown("# 🕵️ MURDER.AI")
    
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
            chatbot = gr.Chatbot(
                label="Investigation",
                height=500,
                type="messages"
            )
            
            # Tool call display
            tool_output = gr.HTML(label="Tool Results")
            
        # Right: Evidence Board
        with gr.Column(scale=1):
            gr.Markdown("## Evidence Board")
            evidence_board = gr.HTML(
                elem_classes="evidence-board",
                value="<p>No evidence yet...</p>"
            )
    
    # Bottom: Controls
    with gr.Row():
        start_btn = gr.Button("🎲 Generate New Case", variant="primary")
        next_round_btn = gr.Button("▶️ Next Round", interactive=False)
    
    # State management
    game_state = gr.State({})
    
    # Event handlers
    start_btn.click(
        fn=start_new_game,
        outputs=[game_state, chatbot, suspect_1, suspect_2, suspect_3, suspect_4]
    )
    
    next_round_btn.click(
        fn=run_game_round,
        inputs=[game_state],
        outputs=[game_state, chatbot, tool_output, evidence_board]
    )

demo.launch(
    theme=gr.themes.Noir(),
    css=custom_css
)
```