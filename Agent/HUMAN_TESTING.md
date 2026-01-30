# Human-in-the-Loop Testing Protocol

To validate conversational realism without external LLM APIs,
scam interactions were tested using constrained role-play.

Procedure:
1. One participant role-played the scammer using predefined scenarios.
2. Another participant role-played the agent.
3. Agent replies strictly followed:
   - persona.yaml
   - phase_rules.py
   - hard safety limits
4. Any reply that felt unnatural, overly intelligent, or unsafe
   was logged as a failure.
5. Fixes were applied and the scenario replayed.

This process continued until agent behavior was consistently
hesitant, boring, and believable.
