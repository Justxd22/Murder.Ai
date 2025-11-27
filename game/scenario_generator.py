import json
import random
import os

# Path to scenarios directory
SCENARIOS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "scenarios")

def load_scenario(filename):
    """Loads a scenario from a JSON file."""
    path = os.path.join(SCENARIOS_DIR, filename)
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: Scenario file {filename} not found at {path}")
        return None
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {filename}")
        return None

def generate_crime_scenario(difficulty="medium"):
    """
    Currently picks a pre-scripted scenario based on difficulty or random.
    In future, this will call an LLM to generate unique JSON.
    """
    
    # For prototype, map difficulty to specific files or random
    # We have: silicon_valley.json (Medium), coffee_shop.json (Easy), art_gallery.json (Hard)
    
    if difficulty.lower() == "easy":
        chosen_file = "coffee_shop.json"
    elif difficulty.lower() == "hard":
        chosen_file = "art_gallery.json"
    else:
        chosen_file = "silicon_valley.json"
        
    # Or just pick random for variety if difficulty not strictly enforced
    # chosen_file = random.choice(["silicon_valley.json", "coffee_shop.json", "art_gallery.json"])
    
    scenario = load_scenario(chosen_file)
    
    if not scenario:
        # Fallback
        return load_scenario("silicon_valley.json")
        
    return scenario
