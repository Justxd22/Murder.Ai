import time

def find_suspect_by_phone(case_data, phone_number):
    """Helper to find a suspect ID by their phone number."""
    for suspect in case_data["suspects"]:
        if suspect["phone_number"] == phone_number:
            return suspect["id"]
    return None

def get_suspect_name(case_data, suspect_id):
    """Helper to get a suspect's name by ID."""
    for suspect in case_data["suspects"]:
        if suspect["id"] == suspect_id:
            return suspect["name"]
    return "Unknown"

def get_location(case_data, phone_number: str, timestamp: str) -> dict:
    """Query the case database for location data."""
    
    # Find which suspect has this phone number
    suspect_id = find_suspect_by_phone(case_data, phone_number)
    
    if not suspect_id:
        return {"error": "Phone number not associated with any suspect."}

    # Look up their location at this time
    # Structure: case_data["evidence"]["location_data"][f"{suspect_id}_phone"][timestamp]
    phone_key = f"{suspect_id}_phone"
    location_data = case_data.get("evidence", {}).get("location_data", {}).get(phone_key, {}).get(timestamp)
    
    if not location_data:
        return {"error": f"No location data found for {phone_number} at {timestamp}."}
    
    return {
        "timestamp": timestamp,
        "coordinates": f"{location_data['lat']}, {location_data['lng']}",
        "description": location_data['location'],
        "accuracy": "Cell tower triangulation ±50m"
    }

def get_footage(case_data, location: str, time_range: str) -> dict:
    """Query case database for camera footage."""
    
    footage = case_data.get("evidence", {}).get("footage_data", {}).get(location, {}).get(time_range)
    
    if not footage:
        return {"error": "No camera footage available at this location/time."}
    
    return {
        "location": location,
        "time_range": time_range,
        "visible_people": footage["visible_people"],
        "quality": footage["quality"],
        "key_details": footage.get("key_frame", "No significant events")
    }

def get_dna_test(case_data, evidence_id: str) -> dict:
    """Query case database for DNA/fingerprint evidence."""
    
    dna = case_data.get("evidence", {}).get("dna_evidence", {}).get(evidence_id)
    
    if not dna:
        return {"error": "Evidence not found or not testable."}
    
    # Simulate processing time
    # time.sleep(1) 
    
    primary_match_name = get_suspect_name(case_data, dna.get("primary_match"))
    
    return {
        "evidence_id": evidence_id,
        "primary_match": primary_match_name,
        "confidence": dna["confidence"],
        "notes": dna["notes"]
    }

def call_alibi(case_data, phone_number: str) -> dict:
    """Call an alibi witness."""
    
    # Find alibi in database
    alibi = None
    for suspect_alibi in case_data.get("evidence", {}).get("alibis", {}).values():
        if suspect_alibi.get("contact") == phone_number:
            alibi = suspect_alibi
            break
    
    if not alibi:
        return {"error": "Number not found."}
    
    # If alibi is truthful, confirm story
    if alibi["truth"].startswith("Telling truth"):
        response = f"Yes, I can confirm they were with me at that time."
    else:
        # Lying/Uncertain
        response = f"Uh... yes, they were with me. Definitely."
    
    return {
        "contact_name": alibi.get("contact_name", "Unknown"),
        "response": response,
        "confidence": "High" if alibi["verifiable"] else "Uncertain",
        "red_flags": [] if alibi["verifiable"] else ["Hesitant response", "No details provided"]
    }
