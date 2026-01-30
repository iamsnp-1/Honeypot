#!/usr/bin/env python3
"""
Simple test for communication and JSON functionality
"""

import json
import os
from agent.agent_controller import generate_reply
from agent.agent_state import AgentPhase
from mock_llm import MockLLM

def test_communication():
    """Test communication and JSON functionality"""
    
    print("TESTING COMMUNICATION & JSON FUNCTIONALITY")
    print("=" * 45)
    
    # Test 1: Basic Communication
    print("\n1. COMMUNICATION TEST")
    print("-" * 20)
    
    llm = MockLLM()
    phase = AgentPhase.HOOK
    conversation = []
    
    test_messages = [
        "Your account will be blocked",
        "Share your UPI ID", 
        "This is urgent",
        "Click this link"
    ]
    
    print("Testing agent responses:")
    for i, msg in enumerate(test_messages, 1):
        conversation.append({"sender": "scammer", "text": msg})
        
        try:
            response = generate_reply(conversation, phase, llm)
            conversation.append({"sender": "agent", "text": response})
            
            print(f"Turn {i}: {response}")
            
        except Exception as e:
            print(f"Turn {i}: ERROR - {e}")
    
    # Test 2: JSON Creation
    print("\n\n2. JSON FUNCTIONALITY TEST")
    print("-" * 25)
    
    test_data = {
        "session_info": {
            "session_id": "test_session",
            "total_turns": len(test_messages)
        },
        "conversation": conversation
    }
    
    test_file = "test_output.json"
    try:
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, indent=2, ensure_ascii=False)
        
        print(f"JSON file created: {test_file}")
        print(f"File size: {os.path.getsize(test_file)} bytes")
        
        # Validate JSON
        with open(test_file, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
        
        print("JSON validation:")
        print(f"- Session info: OK" if 'session_info' in loaded_data else "- Session info: MISSING")
        print(f"- Conversation: OK" if 'conversation' in loaded_data else "- Conversation: MISSING")
        print(f"- Total entries: {len(loaded_data['conversation'])}")
        
        # Clean up
        os.remove(test_file)
        
    except Exception as e:
        print(f"JSON error: {e}")
    
    # Test 3: Check existing files
    print("\n\n3. EXISTING FILES CHECK")
    print("-" * 20)
    
    if os.path.exists("test_outputs"):
        files = [f for f in os.listdir("test_outputs") if f.endswith('.json')]
        print(f"Found {len(files)} JSON files in test_outputs")
        
        if files:
            sample_file = os.path.join("test_outputs", files[0])
            try:
                with open(sample_file, 'r') as f:
                    data = json.load(f)
                print(f"Sample file structure: OK")
                print(f"Sample has {len(data.get('conversation', []))} conversation turns")
            except:
                print("Sample file: ERROR reading")
    else:
        print("No test_outputs directory found")
    
    print("\n" + "=" * 45)
    print("TEST COMPLETED")
    
    return True

if __name__ == "__main__":
    test_communication()