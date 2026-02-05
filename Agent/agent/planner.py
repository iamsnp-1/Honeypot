from .scenarios import SCENARIOS
from .phases import Phase
from .intents import detect_intent
import random


class AgentPlanner:
    def __init__(self):
        pass

    def detect_intent(self, text):
        return detect_intent(text)

    # ---------------- BAIT LOGIC ---------------- #

    def generate_bait_question(self, state):
        intel = state.intelligence.to_dict()

        if not intel.get("upiIds"):
            return "Which UPI ID was this payment sent to?"

        if not intel.get("phoneNumbers"):
            return "Is this linked to my registered mobile number?"

        if not intel.get("bankAccounts"):
            return "Can you confirm which bank account this is showing?"

        if not intel.get("phishingLinks"):
            return "The link you sent didn’t open. Can you resend it?"

        return None

    # ---------------- STRATEGY SELECTION ---------------- #

    def choose_strategy(self, state):
        phase = state.phase
        fear = state.persona.get("fear_level", 0.3)

        if phase == Phase.HOOK:
            return "feign_confusion"

        if phase == Phase.CLARIFICATION:
            return "probe_cause"

        if phase == Phase.PROBING:
            return "probe_solution"

        if phase == Phase.DELAY:
            return "delay_payment"

        return "feign_confusion"

    # ---------------- REPLY GENERATION ---------------- #

    def generate_reply(self, strategy, state):
        # 🔥 PRIORITY: Extract intelligence
        bait = self.generate_bait_question(state)
        if bait:
            return bait

        responses = {
            "feign_confusion": [
                "Sorry, I didn’t understand that.",
                "Who is this?",
                "What is this regarding?"
            ],
            "probe_cause": [
                "What exactly was flagged?",
                "Which transaction are you referring to?",
                "When did this happen?"
            ],
            "probe_solution": [
                "How am I supposed to fix this?",
                "What do I need to do now?",
                "What’s the process to resolve this?"
            ],
            "delay_payment": [
                "I need some time to check this.",
                "Let me speak to my family.",
                "Can we do this later?"
            ]
        }

        return random.choice(responses.get(strategy, responses["feign_confusion"]))

    # ---------------- SCENARIO SELECTION ---------------- #

    def select_scenario_from_evidence(self, text, intent):
        text = text.lower()

        if any(k in text for k in ["bank", "account", "upi", "kyc", "blocked"]):
            return next(s for s in SCENARIOS if s.name == "bank_freeze")

        if any(k in text for k in ["delivery", "courier", "package"]):
            return next(s for s in SCENARIOS if s.name == "delivery_customs")

        if intent == "authority_claim":
            return next(s for s in SCENARIOS if s.name == "bank_freeze")

        return None
