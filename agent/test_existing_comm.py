#!/usr/bin/env python3
"""
Simple test for existing communication and JSON functionality
"""

import json
import os
from agent.agent_controller import generate_reply
from agent.agent_state import AgentPhase
from mock_llm import MockLLM

def test_existing_functionality():
    """Test existing communication and JSON saving"""
    
    print("=" * 50)
    print("TESTING EXISTING COMMUNICATION & JSON")
    print("=" * 50)
    
    # Test 1: Agent Communication
    print("\n1. TESTING AGENT COMMUNICATION")
    print("-" * 30)
    
    llm = MockLLM()
    phase = AgentPhase.HOOK
    conversation = []
    
    test_messages = [
        "Your account will be blocked",
        "Share your UPI ID now", 
        "This is urgent matter",
        "Click this link"
    ]
    
    responses = []
    for i, msg in enumerate(test_messages, 1):
        conversation.append({"sender": "scammer", "text": msg})
        
        try:
            response = generate_reply(conversation, phase, llm)
            conversation.append({"sender": "agent", "text": response})
            responses.append(response)
            
            print(f"Turn {i}:")
            print(f"  Scammer: {msg}")
            print(f"  Agent: {response}")
            
        except Exception as e:
            print(f"  ERROR: {e}")
            responses.append("ERROR")
    
    # Test 2: JSON Structure Check
    print("\n\n2. TESTING JSON OUTPUT STRUCTURE")
    print("-" * 35)
    
    # Create test JSON structure
    test_data = {
        "session_info": {
            "session_id": "test_20260130",
            "total_turns": len(test_messages),
            "status": "completed"
        },
        "conversation": []
    }
    
    for i, (msg, resp) in enumerate(zip(test_messages, responses), 1):
        test_data["conversation"].append({
            "turn": i,
            "scammer_input": msg,
            "agent_response": resp,
            "phase": phase.value
        })
    
    # Save test JSON
    test_file = "test_communication.json"
    try:
        with open(test_file, 'w', encoding='utf-8') as f:
            json.dump(test_data, f, indent=2, ensure_ascii=False)
        
        print(f"✓ JSON file created: {test_file}")
        print(f"✓ File size: {os.path.getsize(test_file)} bytes")
        
        # Validate JSON
        with open(test_file, 'r', encoding='utf-8') as f:
            loaded_data = json.load(f)
        
        print("✓ JSON structure validation:")
        print(f"  - Session info: {'✓' if 'session_info' in loaded_data else '✗'}")
        print(f"  - Conversation: {'✓' if 'conversation' in loaded_data else '✗'}")
        print(f"  - Total turns: {len(loaded_data['conversation'])}")
        
    except Exception as e:
        print(f"✗ JSON error: {e}")
    
    # Test 3: Check existing JSON files
    print("\n\n3. CHECKING EXISTING JSON FILES")
    print("-" * 30)
    
    test_dir = "test_outputs"
    if os.path.exists(test_dir):
        json_files = [f for f in os.listdir(test_dir) if f.endswith('.json')]
        print(f"✓ Found {len(json_files)} existing JSON files")
        
        # Check one file structure
        if json_files:
            sample_file = os.path.join(test_dir, json_files[0])
            try:
                with open(sample_file, 'r', encoding='utf-8') as f:
                    sample_data = json.load(f)
                
                print(f"✓ Sample file: {json_files[0]}")
                print(f"  - Has scenario_info: {'✓' if 'scenario_info' in sample_data else '✗'}")
                print(f"  - Has conversation: {'✓' if 'conversation' in sample_data else '✗'}")
                print(f"  - Conversation turns: {len(sample_data.get('conversation', []))}")
                
            except Exception as e:
                print(f"✗ Error reading sample: {e}")
    else:
        print("✗ No test_outputs directory found")
    
    print("\n" + "=" * 50)
    print("ANALYSIS COMPLETE")
    print("=" * 50)
    
    # Clean up
    if os.path.exists(test_file):
        os.remove(test_file)
    
    return True

if __name__ == "__main__":
    test_existing_functionality()