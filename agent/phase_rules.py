PHASE_RULES = {
    "hook": {
        "goal": "Keep scammer engaged",
        "allowed_actions": [
            "ask_why",
            "express_confusion",
            "acknowledge_message"
        ],
        "forbidden_actions": [
            "share_info",
            "refuse",
            "accuse"
        ]
    },

    "clarification": {
        "goal": "Force scammer to explain",
        "allowed_actions": [
            "ask_process",
            "ask_identity",
            "repeat_question"
        ],
        "forbidden_actions": [
            "share_credentials",
            "threaten",
            "end_conversation"
        ]
    },

    "partial_compliance": {
        "goal": "Trigger asset exposure",
        "allowed_actions": [
            "pretend_trying",
            "ask_to_repeat_details",
            "misunderstand_instruction"
        ],
        "forbidden_actions": [
            "complete_action",
            "send_money",
            "share_otp"
        ]
    },

    "delay": {
        "goal": "Waste time & escalate scammer",
        "allowed_actions": [
            "technical_excuse",
            "personal_excuse",
            "request_time"
        ],
        "forbidden_actions": [
            "ghost",
            "accuse"
        ]
    },

    "exit": {
        "goal": "End without suspicion",
        "allowed_actions": [
            "external_authority_exit"
        ],
        "forbidden_actions": [
            "reveal_detection",
            "insult"
        ]
    }
}
