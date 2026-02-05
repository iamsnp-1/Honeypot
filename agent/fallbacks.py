def needs_correction(reply: str) -> bool:
    red_flags = [
        "according to policy",
        "I cannot assist",
        "this seems fraudulent"
    ]
    return any(flag in reply.lower() for flag in red_flags)


def corrective_reply():
    return "Sorry, I’m getting confused… can you explain again?"
