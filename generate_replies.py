def generate_reply(state, scammer_text):
    detected = detect_intent(scammer_text)

    if detected == "unknown":
        intent = infer_intent_from_history(state)
    else:
        intent = detected

    state.add_intent(intent)

    phase = state.phase.value
    pools = REPLIES.get(intent, REPLIES["unknown"])

    # Phase-safe fallback
    options = pools.get(phase) or pools.get("clarification") or REPLIES["unknown"]["clarification"]

    reply = state.memory.choose(options)

    state.turns += 1
    state.advance_phase()

    return reply
