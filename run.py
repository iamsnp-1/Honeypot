import json
import time
import random
from state import ConversationState
from engine import generate_reply
from storage import save_conversation
from scenario import SCENARIOS

state_store = {}

def handle_input(input_json):
    session_id = input_json["session_id"]
    message = input_json["message"]

    if session_id not in state_store:
        state_store[session_id] = ConversationState(session_id)

    state = state_store[session_id]

    # Simulate human typing delay for initial response
    typing_delay = state.memory.get_typing_delay(len(message))
    print(f"[Typing for {typing_delay:.1f} seconds...]")
    time.sleep(min(typing_delay, 3.0))  # Cap at 3 seconds for testing

    reply = generate_reply(state, message)

    # Handle multiple messages with delays
    if "\n" in reply:  # Multiple messages
        messages = reply.split("\n")
        full_response = []
        
        for i, msg in enumerate(messages):
            if i > 0:  # Add delay between follow-up messages
                follow_up_delay = random.uniform(1.0, 3.0)  # 1-3 seconds between messages
                print(f"[Typing follow-up for {follow_up_delay:.1f} seconds...]")
                time.sleep(follow_up_delay)
            
            print(f"Agent: {msg}")
            full_response.append(msg)
        
        # Save to history
        state.history.append({"sender": "scammer", "message": message})
        state.history.append({"sender": "agent", "message": reply})
        save_conversation(state)
        
        return " | ".join(full_response)  # Return combined for function result
    else:
        # Single message
        state.history.append({"sender": "scammer", "message": message})
        state.history.append({"sender": "agent", "message": reply})
        save_conversation(state)
        return reply

if __name__ == "__main__":
    print("Agent started. Enter JSON input.\n")
    
    while True:
        raw = input("JSON Input: ").strip()
        if not raw:
            print("Please enter valid JSON.\n")
            continue

        try:
            data = json.loads(raw)
        except json.JSONDecodeError:
            print("Invalid JSON format. Try again.\n")
            continue

        result = handle_input(data)
        
        # Only print if it's a single message (multiple messages already printed)
        if " | " not in result:
            print("Agent:", result)
