import sys
import os
sys.path.append(os.path.dirname(__file__))

import json
from Agent import agent_controller
from Agent.agent_state import AgentPhase
from offline_llm import RuleBasedLLM

def run_scenario(path):
    with open(path, 'r') as f:
        data = json.load(f)
    phase = AgentPhase(data["initial_phase"])
    history = []

    # Use offline rule-based LLM - no external API calls
    llm = RuleBasedLLM()

    print("\n==============================")
    print(f"SCENARIO: {data['name']}")
    print("==============================")

    for scammer_text in data["conversation"]:
        history.append({"sender": "scammer", "text": scammer_text})

        reply = agent_controller.generate_reply(
            conversation_history=history,
            current_phase=phase,
            llm=llm
        )

        print(f"\nScammer: {scammer_text}")
        print(f"Agent ({phase.value}): {reply}")
        
        history.append({"sender": "agent", "text": reply})

if __name__ == "__main__":
    run_scenario("tests/scenarios/scenario_bank_threat.json")
