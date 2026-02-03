INTENT_KEYWORDS = {
    "otp_request": ["otp", "one time", "code", "kode", "password", "pasword"],
    "upi_request": ["upi", "google pay", "phonepe", "paytm", "gpay", "bhim", "paise", "paisa", "rupaye", "rupya"],
    "authority_claim": ["bank", "rbi", "employee", "officer", "police", "government", "income tax", "customs", "cbi", "sarkar", "adhikari", "afsar"],
    "urgency_threat": ["blocked", "freeze", "urgent", "final", "immediately", "today", "arrest", "legal action", "band", "block", "jaldi", "turant", "abhi", "aaj", "pakad", "giraftar"],
    "send_link": ["link", "click", "update", "download", "install", "app", "click karo", "dabao", "press karo"],
    "channel_shift": ["call", "whatsapp", "telegram", "video call", "phone karo", "call karo", "whatsapp pe"],
    "reward_claim": ["reward", "cashback", "won", "lottery", "prize", "congratulations", "selected", "jeet", "jeeta", "inaam", "badhai", "mubarak"],
    "money_request": ["send money", "need money", "rs", "rupees", "help me", "paise bhejo", "paise bhej", "paisa chahiye", "madad", "help", "money send", "paisa send"],
    "medical_emergency": ["emergency", "medical", "accident", "hospital", "emergency hai", "hospital mein", "doctor", "operation", "treatment"],
    "friend_scam": ["friend", "college", "school", "know each other", "remember me", "classmate", "dost", "yaar", "bhai"],
    "job_offer": ["job", "work from home", "earn money", "part time", "data entry", "typing work", "income", "kaam", "naukri", "ghar se kaam", "paisa kamao", "typing ka kaam"],
    "investment_scam": ["investment", "trading", "profit", "returns", "stock", "crypto", "bitcoin", "double money", "nivesh", "fayda", "munafa", "share", "trading karo", "paisa double"],
    "tech_support": ["computer", "virus", "malware", "microsoft", "windows", "technical support", "infected", "laptop", "mobile", "phone", "kharab", "problem", "virus aaya"],
    "romance_scam": ["love", "marry", "relationship", "lonely", "beautiful", "handsome", "meet you", "pyaar", "mohabbat", "shaadi", "milna", "sundar", "khubsurat"],
    "fake_delivery": ["delivery", "courier", "package", "parcel", "shipping", "customs duty", "fedex", "dhl", "saman", "packet", "delivery boy", "courier boy"]
}

def detect_intent(text: str) -> str:
    text = text.lower()
    for intent, words in INTENT_KEYWORDS.items():
        if any(w.lower() in text for w in words):
            return intent
    return "unknown"
