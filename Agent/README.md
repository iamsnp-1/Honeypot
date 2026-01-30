Status: Feature-complete. Agent behavior frozen.

# Agentic Honeypot — Agent Module

This module implements the conversational AI agent used to
engage suspected scammers in a human-like manner.

## Scope
- Simulates a realistic human persona
- Handles multi-turn conversations
- Operates using fixed behavioral phases
- Does NOT detect scams
- Does NOT extract intelligence
- Does NOT store session data

## Files
- persona.yaml — Fixed human persona definition
- agent_state.py — Conversation phases
- phase_rules.py — Allowed behaviors per phase
- prompts.py — LLM prompt constraints
- agent_controller.py — Reply generation interface
- fallbacks.py — Self-correction logic

## Usage
This module exposes a single interface:

generate_reply(conversation_history, current_phase, llm)

The caller is responsible for:
- Detecting scam intent
- Managing session state
- Advancing conversation phases
- Extracting intelligence

## Testing Strategy (No External APIs)

Due to hackathon constraints on external API usage,
the agent module was tested using:

- Deterministic MockLLM for structural validation
- Human-in-the-loop role-play testing for realism

Scam scenarios were manually simulated while strictly
enforcing persona constraints, phase rules, and safety limits.
Observed failures were logged and corrected iteratively.
