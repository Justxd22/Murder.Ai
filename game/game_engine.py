import uuid
from .scenario_generator import generate_crime_scenario
from .llm_manager import LLMManager
from mcp import tools

class GameInstance:
    def __init__(self, difficulty="medium"):
        self.id = str(uuid.uuid4())
        self.scenario = generate_crime_scenario(difficulty)
        self.llm_manager = LLMManager()
        self.round = 1
        self.max_rounds = 5
        self.points = 10
        self.evidence_revealed = [] # List of strings or result dicts
        self.logs = [] # Chat logs
        self.game_over = False
        self.verdict_correct = False
        
        # Initialize Agents
        self._init_agents()
        
    def _init_agents(self):
        # 1. Detective
        detective_context = {
            "victim_name": self.scenario["victim"]["name"],
            "time_of_death": self.scenario["victim"]["time_of_death"],
            "location": self.scenario["evidence"]["location_data"].get("suspect_1_phone", {}).get("8:47 PM", {}).get("location", "Unknown"), # Approximate
            "investigation_state": "Initial briefing."
        }
        self.llm_manager.create_agent("detective", "detective", detective_context)
        
        # 2. Suspects
        for suspect in self.scenario["suspects"]:
            role = "murderer" if suspect["is_murderer"] else "witness"
            
            # Context for prompt
            context = {
                "name": suspect["name"],
                "victim_name": self.scenario["victim"]["name"],
                "alibi_story": suspect["alibi_story"],
                "bio": suspect["bio"],
                "true_location": suspect["true_location"],
                "phone_number": suspect.get("phone_number", "Unknown"), # Add phone number to context
                
                # Murderer specific
                "method": self.scenario["title"], # Placeholder, scenario doesn't explicitly list 'method' field in plan, using title/weapon logic implied
                "location": self.scenario["victim"].get("location", "the scene"), # Using generic
                "motive": suspect["motive"]
            }
            
            self.llm_manager.create_agent(suspect["id"], role, context)

    def log_event(self, speaker, message):
        self.logs.append({"speaker": speaker, "message": message})

    def question_suspect(self, suspect_id, question):
        if self.game_over:
            return "Game Over"
            
        suspect_name = next((s["name"] for s in self.scenario["suspects"] if s["id"] == suspect_id), "Unknown")
        
        # 1. Detective asks (simulated log)
        self.log_event("Detective", f"To {suspect_name}: {question}")
        
        # 2. Suspect responds
        response = self.llm_manager.get_response(suspect_id, question)
        self.log_event(suspect_name, response)
        
        return response

    def use_tool(self, tool_name, **kwargs):
        if self.points <= 0:
            return {"error": "Not enough investigation points!"}
            
        cost = 0
        result = {}
        
        # Map tool names to functions
        if tool_name == "get_location":
            cost = 2
            result = tools.get_location(self.scenario, kwargs.get("phone_number"), kwargs.get("timestamp"))
        elif tool_name == "get_footage":
            cost = 2
            result = tools.get_footage(self.scenario, kwargs.get("location"), kwargs.get("time_range"))
        elif tool_name == "get_dna_test":
            cost = 3
            result = tools.get_dna_test(self.scenario, kwargs.get("evidence_id"))
        elif tool_name == "call_alibi":
            cost = 1
            result = tools.call_alibi(self.scenario, kwargs.get("phone_number"))
        else:
            return {"error": f"Unknown tool: {tool_name}"}
            
        if "error" in result:
             return result # Don't deduct points for errors
             
        self.points -= cost
        self.evidence_revealed.append(result)
        self.log_event("System", f"Used {tool_name}. Cost: {cost} pts. Result: {str(result)}")
        return result

    def advance_round(self):
        if self.round < self.max_rounds:
            self.round += 1
            return True
        else:
            self.game_over = True
            return False

    def make_accusation(self, suspect_id):
        self.game_over = True
        
        # Check if correct
        murderer = next((s for s in self.scenario["suspects"] if s["is_murderer"]), None)
        
        if murderer and murderer["id"] == suspect_id:
            self.verdict_correct = True
            msg = f"CORRECT! {murderer['name']} was the murderer."
        else:
            self.verdict_correct = False
            msg = f"INCORRECT. The true murderer was {murderer['name'] if murderer else 'Unknown'}."
            
        self.log_event("System", f"FINAL ACCUSATION: {suspect_id}. Result: {msg}")
        return msg

# Global Session Store
SESSIONS = {}

def start_game(difficulty="medium"):
    game = GameInstance(difficulty)
    SESSIONS[game.id] = game
    return game.id, game

def get_game(session_id):
    return SESSIONS.get(session_id)
