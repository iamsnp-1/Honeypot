import yaml
import os
from .agent_state import AgentPhase
from .prompts import SYSTEM_PROMPT, build_prompt

# Cache persona to avoid repeated file loading
_persona_cache = None

def load_persona():
    """Load persona from YAML file with caching"""
    global _persona_cache
    if _persona_cache is None:
        persona_path = os.path.join(os.path.dirname(__file__), 'persona.yaml')
        with open(persona_path, 'r') as f:
            _persona_cache = yaml.safe_load(f)
    return _persona_cache

def generate_reply(conversation_history, current_phase, llm):
    """
    Generate reply using offline rule-based system
    conversation_history: list of dicts [{sender, text}]
    current_phase: AgentPhase
    llm: offline LLM (rule-based or mock)
    """
    persona = load_persona()
    
    # Build context for rule-based system
    prompt = build_prompt(
        persona=persona,
        phase=current_phase.value,
        conversation=conversation_history
    )
    
    # Generate response using offline system
    response = llm.generate(
        system=SYSTEM_PROMPT,
        prompt=prompt,
        max_tokens=60
    )
    
    return response.strip()
