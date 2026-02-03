from intents import detect_intent
from replies import REPLIES
import re
import random

def extract_info(text, state):
    """Extract and store information from scammer's message"""
    text_lower = text.lower()
    
    # Extract name patterns
    name_match = re.search(r'(?:i am|i\'m|my name is|this is)\s+([a-zA-Z\s]+)', text_lower)
    if name_match:
        state.extracted_info['name'] = name_match.group(1).strip().title()
    
    # Extract full names (multiple words)
    if len(text.split()) >= 2 and not any(word in text_lower for word in ['send', 'money', 'help', 'hospital']):
        words = text.split()
        if all(word.isalpha() for word in words) and len(words) <= 4:
            state.extracted_info['full_name'] = text.title()
    
    # Extract organization claims
    if 'rbi' in text_lower:
        state.extracted_info['organization'] = 'RBI'
    elif 'bank' in text_lower:
        state.extracted_info['organization'] = 'Bank'
    
    # Extract phone numbers
    phone_match = re.search(r'\b\d{10,12}\b', text)
    if phone_match:
        state.extracted_info['phone'] = phone_match.group()
    
    # Extract location/address
    if any(word in text_lower for word in ['live', 'stay', 'address', 'from']):
        location_match = re.search(r'(?:live|stay|from|address)\s+(?:in|at|is)?\s*([a-zA-Z\s]+)', text_lower)
        if location_match:
            state.extracted_info['location'] = location_match.group(1).strip().title()
    
    # Extract college/education info
    if 'college' in text_lower:
        college_match = re.search(r'([a-zA-Z\s]+)\s*college', text_lower)
        if college_match:
            state.extracted_info['college'] = college_match.group(0).title()

def should_skip_question(question, state):
    """Check if we should skip asking a question based on known info"""
    info = state.extracted_info
    
    if 'name' in question.lower() and ('name' in info or 'full_name' in info):
        return True
    if 'address' in question.lower() and 'location' in info:
        return True
    if 'college' in question.lower() and 'college' in info:
        return True
    if 'organization' in question.lower() and 'organization' in info:
        return True
    
    return False

def get_followup_messages(intent, phase, state):
    """Get follow-up messages that humans typically send"""
    followups = {
        "money_request": [
            "Wait...",
            "This is strange",
            "I'm confused",
            "Hold on"
        ],
        "friend_scam": [
            "Hmm...",
            "Let me think",
            "This is weird",
            "I don't remember"
        ],
        "urgency_threat": [
            "What?!",
            "That's scary",
            "Oh no",
            "Really?"
        ],
        "authority_claim": [
            "Official?",
            "From bank?",
            "Government?",
            "Are you sure?"
        ]
    }
    return followups.get(intent, ["Hmm...", "Wait", "What?"])

def get_followup_questions(intent, state):
    """Get follow-up questions humans ask"""
    questions = {
        "friend_scam": [
            "What's your last name again?",
            "Which batch were you in?",
            "Do you have Facebook?",
            "Can you send your photo?"
        ],
        "money_request": [
            "How much exactly?",
            "When do you need it?",
            "What happened exactly?",
            "Are you okay?"
        ],
        "medical_emergency": [
            "Which doctor?",
            "How serious is it?",
            "Are you in pain?",
            "Who is with you?"
        ],
        "authority_claim": [
            "What's your badge number?",
            "Which office?",
            "Can I call back?",
            "Is this urgent?"
        ]
    }
    return questions.get(intent, ["Can you explain more?", "What exactly?", "Are you sure?"])

def infer_intent_from_history(state):
    """
    If scammer sends vague replies like 'ok', 'yes', etc.,
    reuse the most recent meaningful intent.
    """
    for intent in reversed(state.recent_intents):
        if intent != "unknown":
            return intent
    return "unknown"

def generate_reply(state, scammer_text: str) -> str:
    # Step 0: Extract information from scammer's message
    extract_info(scammer_text, state)
    
    # Step 1: Detect intent from current message
    detected_intent = detect_intent(scammer_text)

    # Step 2: Fallback to previous intent if message is vague
    if detected_intent == "unknown":
        intent = infer_intent_from_history(state)
    else:
        intent = detected_intent

    # Step 3: Save intent to history
    state.add_intent(intent)

    phase = state.phase.value

    # Step 4: Get reply pools for intent
    pools = REPLIES.get(intent, REPLIES["unknown"])

    # Step 5: Try phase-specific replies
    options = pools.get(phase)

    # Step 6: Fallbacks (IMPORTANT)
    if not options:
        options = pools.get("clarification")

    if not options:
        options = REPLIES["default_by_phase"][phase]

    # Step 7: Filter out questions we already know answers to
    filtered_options = [opt for opt in options if not should_skip_question(opt, state)]
    if filtered_options:
        options = filtered_options

    # Step 8: Generate human-like responses
    replies = []
    
    # Main reply
    main_reply = state.memory.choose(options)
    replies.append(main_reply)
    
    # Maybe send multiple messages (human behavior)
    if state.memory.should_send_multiple():
        follow_up_options = get_followup_messages(intent, phase, state)
        if follow_up_options:
            follow_up = random.choice(follow_up_options)
            replies.append(follow_up)
    
    # Maybe ask follow-up question
    if state.memory.should_ask_followup() and len(replies) == 1:
        followup_questions = get_followup_questions(intent, state)
        if followup_questions:
            question = random.choice(followup_questions)
            replies.append(question)
    
    # Step 9: Update state
    state.turns += 1
    state.advance_phase()
    
    # Return single reply or multiple replies joined
    if len(replies) > 1:
        return "\n".join(replies)  # Multiple messages
    else:
        return replies[0]