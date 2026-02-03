from phases import Phase
from memory import ReplyMemory

class ConversationState:
    def __init__(self, session_id):
        self.session_id = session_id
        self.phase = Phase.HOOK
        self.turns = 0
        self.memory = ReplyMemory()
        self.history = []
        self.recent_intents = []   # ← ADD THIS
        self.extracted_info = {}   # Store scammer's claims

    def add_intent(self, intent):
        self.recent_intents.append(intent)
        if len(self.recent_intents) > 3:
            self.recent_intents.pop(0)

    def advance_phase(self):
        if self.turns >= 2 and self.phase == Phase.HOOK:
            self.phase = Phase.CLARIFICATION
        elif self.turns >= 4 and self.phase == Phase.CLARIFICATION:
            self.phase = Phase.PROBING
        elif self.turns >= 6 and self.phase == Phase.PROBING:
            self.phase = Phase.DELAY
        elif self.turns >= 8:
            self.phase = Phase.EXIT
