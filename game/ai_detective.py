import json
import re
from .llm_manager import LLMManager

class AIDetective:
    def __init__(self, game_instance):
        self.game = game_instance
        self.llm = LLMManager()
        # We reuse the LLMManager but we need to register the new prompt role dynamically
        # or just load it manually.
        self.prompt_template = self._load_prompt()
        self.history = []
        self.memory = [] # Store structured past actions

    def _load_prompt(self):
        try:
            with open("prompts/detective_player.txt", "r") as f:
                return f.read()
        except:
            return "Error loading prompt."

    def record_result(self, action_type, result):
        """Records the outcome of an action to memory."""
        entry = f"Action: {action_type}\nResult: {json.dumps(result)}"
        self.memory.append(entry)
        # Keep prompt focused (last 5 turns)
        if len(self.memory) > 5:
            self.memory.pop(0)

    def decide_next_move(self):
        """
        Analyzes game state and returns a JSON action.
        """
        # 1. Construct Context
        evidence_list = [f"{e.get('title', e.get('info', 'Evidence'))}: {e.get('html_content', e.get('description', str(e)))}" for e in self.game.evidence_revealed]
        evidence_summary = "; ".join(evidence_list) if evidence_list else "None"
        
        suspect_status = []
        suspect_phones = []
        for s in self.game.scenario["suspects"]:
            status = "Active"
            if s["id"] in self.game.eliminated_suspects:
                status = "Eliminated"
            suspect_status.append(f"{s['name']} ({s['id']}): {status}")
            suspect_phones.append(f"{s['name']}: {s.get('phone_number', 'Unknown')}")
            
        history_str = "\n---\n".join(self.memory) if self.memory else "No previous actions."
        
        # Tool Options
        cameras = list(self.game.scenario["evidence"]["footage_data"].keys())
        unlocked_items = self.game.unlocked_evidence if self.game.unlocked_evidence else ["None"]
        
        prompt = self.prompt_template.format(
            victim_name=self.game.scenario["victim"]["name"],
            time_of_death=self.game.scenario["victim"]["time_of_death"],
            location=self.game.scenario["victim"].get("location", "Unknown"),
            round=self.game.round,
            points=self.game.points,
            evidence_summary=evidence_summary,
            suspect_status="\n".join(suspect_status),
            history=history_str,
            # Tool Hints
            cameras=", ".join(cameras),
            suspect_phones="\n".join(suspect_phones),
            unlocked_items=", ".join(unlocked_items)
        )
        
        # 2. Call LLM
        # We treat this as a one-shot or maintain simple history
        # Using a unique agent ID for the detective player
        agent_id = "ai_detective_player"
        
        # We need to inject the prompt into the agent creation if it doesn't exist
        if agent_id not in self.llm.agents:
            # We cheat a bit and use 'detective' role but override instructions in the message
            # because LLMManager expects a fixed role.
            # Actually, let's just pass the full prompt as the "user input" to a generic agent 
            # or create a custom agent.
            pass

        # Direct generation using the underlying model logic would be cleaner, 
        # but we'll use the existing abstraction.
        # We will send the ENTIRE prompt as the message.
        response_text = self.llm.get_response_raw(prompt)
        
        # 3. Parse JSON
        try:
            # Extract JSON from code blocks if present
            json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
            if json_match:
                response_text = json_match.group(0)
            
            action = json.loads(response_text)
            return action
        except Exception as e:
            print(f"AI Detective Error: {e} | Response: {response_text}")
            # Fallback action
            return {
                "thought": "I am confused. I will check the footage.",
                "action": "use_tool",
                "tool_name": "get_footage",
                "args": {"location": "10th_floor_camera"}
            }
