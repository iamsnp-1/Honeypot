from scam_detection.detector import detect_scam as core_detect_scam

def detect_scam(text: str, session: dict):
    """
    Adapter for teammate-1 scam detection
    DO NOT change the model — only normalize output
    """

    result = core_detect_scam(text, session.get("messages", []))

    # 👇 MAP YOUR OUTPUT HERE
    scam_detected = False
    confidence = 0.0

    # CASE 1: label based
    if isinstance(result, dict):
        if result.get("label") == "scam":
            scam_detected = True
            confidence = result.get("risk", 0.9)

        # CASE 2: boolean based
        if result.get("is_scam") is True:
            scam_detected = True
            confidence = result.get("score", 0.9)

    return {
        "scamDetected": scam_detected,
        "confidence": confidence
    }
