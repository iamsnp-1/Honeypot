#!/usr/bin/env python3
"""
Test communication and JSON saving functionality only
"""

import json
import os
from auto_save_agent import AutoSaveScamAgent
from offline_llm import RuleBasedLLM

def test_communication_and_json():
    """Test agent communication and JSON saving"""
    
    print("=" * 50)
    print("TESTING COMMUNICATION & JSON FUNCTIONALITY")
    print("=" * 50)
    
    # Test 1: Agent Communication
    print("\n1. TESTING AGENT COMMUNICATION")
    print("-" * 30)
    
    agent = AutoSaveScamAgent()
    session_id = agent.start_new_call()
    print(f"Session started: {session_id}")
    
    test_inputs = [
        "Hello sir, this is from bank",
        "Your account has problem", 
        "Please provide details",
        "This is urgent matter"
    ]
    
    responses = []
    for i, msg in enumerate(test_inputs, 1):
        response = agent.respond_to_scammer(msg)
        responses.append(response)
        print(f"Turn {i}: {response}")
    
    json_file = agent.end_call("test_complete")
    print(f"Call ended, saved to: {json_file}")
    
    # Test 2: JSON Structure Validation
    print("\n\n2. TESTING JSON STRUCTURE")
    print("-" * 25)
    
    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        print("JSON Structure Check:")
        print(f"✓ Session ID: {data['session_info']['session_id']}")
        print(f"✓ Total turns: {data['session_info']['total_turns']}")
        print(f"✓ Duration: {data['session_info']['duration_seconds']:.3f}s")
        print(f"✓ Conversation entries: {len(data['conversation'])}")
        
        # Validate each conversation turn
        for turn in data['conversation']:
            required_fields = ['timestamp', 'turn', 'scammer_input', 'agent_response']
            if all(field in turn for field in required_fields):
                print(f"✓ Turn {turn['turn']}: Valid structure")
            else:
                print(f"✗ Turn {turn['turn']}: Missing fields")
    
    # Test 3: Offline LLM Communication
    print("\n\n3. TESTING OFFLINE LLM")
    print("-" * 25)
    
    llm = RuleBasedLLM()
    
    test_prompts = [
        "Scammer: Your bank account is blocked",
        "Scammer: Share your UPI details", 
        "Scammer: Click this link now",
        "Scammer: Send OTP immediately"
    ]
    
    for prompt in test_prompts:
        response = llm.generate("", prompt, 60)
        print(f"Input: {prompt.split(': ')[1]}")
        print(f"Response: {response}")
        print()
    
    # Test 4: JSON File System
    print("\n4. TESTING JSON FILE SYSTEM")
    print("-" * 25)
    
    scam_logs_dir = "scam_logs"
    if os.path.exists(scam_logs_dir):
        json_files = [f for f in os.listdir(scam_logs_dir) if f.endswith('.json')]
        print(f"✓ Total JSON files: {len(json_files)}")
        
        # Check file sizes
        total_size = sum(os.path.getsize(os.path.join(scam_logs_dir, f)) for f in json_files)
        print(f"✓ Total storage: {total_size} bytes")
        
        # Validate JSON format of all files
        valid_files = 0
        for json_file in json_files:
            try:
                with open(os.path.join(scam_logs_dir, json_file), 'r', encoding='utf-8') as f:
                    json.load(f)
                valid_files += 1
            except:
                pass
        
        print(f"✓ Valid JSON files: {valid_files}/{len(json_files)}")
    
    print("\n" + "=" * 50)
    print("COMMUNICATION & JSON TEST COMPLETED")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    test_communication_and_json()