from game import game_engine
import time

def test_game_logic():
    print("Starting game test...")
    session_id, game = game_engine.start_game("medium")
    print(f"Game started. Session ID: {session_id}")
    print(f"Scenario: {game.scenario['title']}")
    
    # Test Agent Creation
    print("Checking agents...")
    for suspect in game.scenario["suspects"]:
        agent = game.llm_manager.get_agent(suspect["id"])
        if agent:
            print(f"Agent created for {suspect['name']}")
        else:
            print(f"FAILED to create agent for {suspect['name']}")
            
    # Test Questioning (Mock mode likely if no key)
    print("\nTesting Questioning...")
    suspect_id = game.scenario["suspects"][0]["id"]
    response = game.question_suspect(suspect_id, "Where were you?")
    print(f"Response from {suspect_id}: {response}")
    
    # Test Tools
    print("\nTesting Tools...")
    # Use a valid phone number from scenario
    phone = game.scenario["suspects"][0]["phone_number"]
    res = game.use_tool("get_location", phone_number=phone, timestamp="8:47 PM")
    print(f"Tool Result: {res}")
    
    if "error" in res:
        print("Tool test FAILED (unless expected error)")
        
    # Test Round Advance
    print("\nTesting Round Advance...")
    print(f"Current Round: {game.round}")
    game.advance_round()
    print(f"New Round: {game.round}")
    
    print("\nTest Complete.")

if __name__ == "__main__":
    test_game_logic()
