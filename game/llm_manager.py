import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure the API
API_KEY = os.getenv("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

class GeminiAgent:
    def __init__(self, model_name="gemini-2.5-flash", system_instruction=None):
        self.model_name = model_name
        self.system_instruction = system_instruction
        self.chat_session = None
        self.history = []
        
        if API_KEY:
            self.model = genai.GenerativeModel(
                model_name=model_name,
                system_instruction=system_instruction
            )
            self.chat_session = self.model.start_chat(history=[])
        else:
            print("Warning: No GEMINI_API_KEY found. Agent will run in mock mode.")
            self.model = None

    def generate_response(self, user_input):
        if not self.model:
            return f"[MOCK] I received: {user_input}. (Set GEMINI_API_KEY to get real responses)"
        
        try:
            response = self.chat_session.send_message(user_input)
            return response.text
        except Exception as e:
            return f"Error generating response: {str(e)}"

class LLMManager:
    def __init__(self):
        self.agents = {}
        self.prompts = self._load_prompts()

    def _load_prompts(self):
        prompts = {}
        prompt_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "prompts")
        for filename in ["murderer.txt", "witness.txt", "detective.txt"]:
            key = filename.replace(".txt", "")
            try:
                with open(os.path.join(prompt_dir, filename), "r") as f:
                    prompts[key] = f.read()
            except FileNotFoundError:
                print(f"Warning: Prompt file {filename} not found.")
                prompts[key] = ""
        return prompts

    def create_agent(self, agent_id, role, context_data):
        """
        Creates a new GeminiAgent for a specific character.
        
        agent_id: Unique ID (e.g., 'suspect_1', 'detective')
        role: 'murderer', 'witness', 'detective'
        context_data: Dict to fill in the prompt templates (name, victim_name, etc.)
        """
        
        # Select base prompt template
        if role == "murderer":
            base_prompt = self.prompts.get("murderer", "")
        elif role == "detective":
            base_prompt = self.prompts.get("detective", "")
        else:
            base_prompt = self.prompts.get("witness", "")
            
        # Fill template
        try:
            system_instruction = base_prompt.format(**context_data)
        except KeyError as e:
            print(f"Warning: Missing key {e} in context data for {agent_id}")
            system_instruction = base_prompt # Fallback
            
        # Create agent
        agent = GeminiAgent(system_instruction=system_instruction)
        self.agents[agent_id] = agent
        return agent

    def get_agent(self, agent_id):
        return self.agents.get(agent_id)

    def get_response(self, agent_id, user_input):
        agent = self.get_agent(agent_id)
        if agent:
            return agent.generate_response(user_input)
        return "Error: Agent not found."
