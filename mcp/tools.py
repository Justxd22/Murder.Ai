import time
import re
from game.llm_manager import LLMManager

def normalize_phone(phone):
    """Strips non-digit characters from phone number for comparison."""
    if not phone:
        return ""
    return re.sub(r"\D", "", phone)

def find_suspect_by_phone(case_data, phone_number):
    """Helper to find a suspect ID by their phone number (fuzzy match)."""
    target_digits = normalize_phone(phone_number)
    if not target_digits:
        return None
        
    for suspect in case_data["suspects"]:
        suspect_digits = normalize_phone(suspect["phone_number"])
        # Check if one ends with the other (to handle +1 vs no +1)
        if target_digits.endswith(suspect_digits) or suspect_digits.endswith(target_digits):
            return suspect["id"]
    return None

def get_suspect_name(case_data, suspect_id):
    """Helper to get a suspect's name by ID."""
    for suspect in case_data["suspects"]:
        if suspect["id"] == suspect_id:
            return suspect["name"]
    return "Unknown"

def get_location(case_data, phone_number: str, timestamp: str = None) -> dict:
    """
    Query the case database for location data.
    If timestamp is missing, searches for the time of death or returns all data.
    """
    
    # Find which suspect has this phone number
    suspect_id = find_suspect_by_phone(case_data, phone_number)
    
    if not suspect_id:
        return {"error": f"Phone number {phone_number} not associated with any suspect."}

    phone_key = f"{suspect_id}_phone"
    location_data_map = case_data.get("evidence", {}).get("location_data", {}).get(phone_key, {})
    
    if not location_data_map:
         return {"error": f"No location history found for {phone_number}."}

    # If timestamp provided, look for exact match first
    if timestamp:
        location_data = location_data_map.get(timestamp)
        if location_data:
             return {
                "timestamp": timestamp,
                "coordinates": f"{location_data['lat']}, {location_data['lng']}",
                "description": location_data['location'],
                "accuracy": "Cell tower triangulation ±50m"
            }
        else:
             return {"error": f"No data for {timestamp}. Available times: {list(location_data_map.keys())}"}
    
    # If no timestamp, return ALL data points found (or just the murder time one)
    # Let's return the one closest to murder time (usually 8:47 PM in our main scenario)
    # Or just return a list of all known locations.
    
    results = []
    for time_key, loc in location_data_map.items():
        results.append(f"{time_key}: {loc['location']}")
        
    return {
        "info": "Location History Found",
        "history": results
    }

def get_footage(case_data, location: str, time_range: str = None) -> dict:
    """Query case database for camera footage."""
    
    # Fuzzy match location keys
    target_loc_key = None
    footage_data = case_data.get("evidence", {}).get("footage_data", {})
    
    for loc_key in footage_data.keys():
        if location.lower() in loc_key.lower() or loc_key.lower() in location.lower():
            target_loc_key = loc_key
            break
            
    if not target_loc_key:
        return {"error": "No camera footage available at this location."}
    
    # If time_range not provided, return the first one found or all
    loc_footage = footage_data[target_loc_key]
    
    if time_range:
        footage = loc_footage.get(time_range)
        if not footage:
             return {"error": f"No footage for time {time_range}. Available: {list(loc_footage.keys())}"}
    else:
        # Return the first available clip info
        # keys() might include "unlocks", so filter for time-like keys? 
        # Actually, logic assumes keys are time ranges. 
        # "unlocks" is a key but not a time range.
        # We should find a key that contains ":" or is not "unlocks"
        
        valid_keys = [k for k in loc_footage.keys() if k != "unlocks"]
        if not valid_keys:
             return {"error": "No footage clips available."}
             
        first_key = valid_keys[0]
        footage = loc_footage[first_key]
        time_range = first_key # Update for return
    
    return {
        "location": target_loc_key,
        "time_range": time_range,
        "visible_people": footage.get("visible_people", []),
        "quality": footage.get("quality", "Unknown"),
        "key_details": footage.get("key_frame", "No significant events"),
        "unlocks": loc_footage.get("unlocks", []) # Fix: Get form camera level
    }

def get_dna_test(case_data, evidence_id: str) -> dict:
    """Query case database for DNA/fingerprint evidence."""
    
    dna = case_data.get("evidence", {}).get("dna_evidence", {}).get(evidence_id)
    
    if not dna:
        return {"error": "Evidence not found or not testable."}
    
    # Handle single match
    if "primary_match" in dna:
        primary_match_name = get_suspect_name(case_data, dna.get("primary_match"))
        return {
            "evidence_id": evidence_id,
            "primary_match": primary_match_name,
            "confidence": dna.get("confidence", "Unknown"),
            "notes": dna.get("notes", "")
        }
        
    # Handle multiple/mixed matches
    elif "matches" in dna:
        match_names = [get_suspect_name(case_data, mid) for mid in dna["matches"]]
        return {
            "evidence_id": evidence_id,
            "primary_match": "Mixed/Inconclusive",
            "matches": match_names,
            "confidence": "N/A (Multiple sources)",
            "notes": dna.get("notes", "")
        }
        
    return {"error": "Inconclusive test result."}

def call_alibi(case_data, alibi_id: str = None, question: str = None, phone_number: str = None) -> dict:
    """
    Call an alibi witness using an LLM agent.
    Requires `alibi_id` and `question`.
    """
    print(f"Calling alibi with alibi_id={alibi_id}, phone_number={phone_number}, question={question}")
    # 1. Find suspect with this alibi_id
    target_suspect = None
    if alibi_id:
        for s in case_data["suspects"]:
            if s.get("alibi_id") == alibi_id:
                target_suspect = s
                break
    
    if not target_suspect:
        # Fallback: Try phone number for legacy support or wrong input
        if phone_number:
             # (Legacy logic skipped for brevity, encourage Alibi ID)
             return {"error": "Please use the unique Alibi ID provided by the suspect."}
        return {"error": "Invalid Alibi ID."}

    if not question:
        return {"error": "You must ask a question."}

    # 2. Get alibi details
    alibi_key = f"{target_suspect['id']}_alibi"
    alibi_data = case_data.get("evidence", {}).get("alibis", {}).get(alibi_key)

    if not alibi_data:
        return {"error": "No alibi contact record found for this suspect."}

    # 3. Create LLM Agent for Alibi
    llm = LLMManager()
    
    context = {
        "suspect_name": target_suspect["name"],
        "truth_context": alibi_data.get("truth", "Unknown"),
        "suspect_story": target_suspect.get("alibi_story", "Unknown"),
        "relationship": alibi_data.get("contact_name", "Acquaintance"),
        "question": question
    }
    
    # Create a temporary agent
    agent_id = f"alibi_{alibi_id}"
    # Ensure LLMManager supports 'alibi_agent' role (update _load_prompts if needed)
    llm.create_agent(agent_id, "alibi_agent", context)
    
    response = llm.get_response(agent_id, question)
    
    return {
        "contact_name": alibi_data.get("contact_name", "Unknown"),
        "response": response,
        "confidence": "High" if alibi_data.get("verifiable") else "Uncertain"
    }
