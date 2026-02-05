# Agent Failure Log

This file tracks where the conversational agent behaved in an
unnatural, suspicious, or non-human manner during scenario testing.

---

## Scenario:
bank_threat

### Turn:
2

### Scammer message:
"KYC not completed. Last warning."

### Agent reply:
"Please explain why my KYC is not completed."

### Issue observed:
Reply sounds overly polite and grammatically clean.
A real user would sound more anxious or confused.

### Root cause:
Prompt allows formal phrasing without emotional bias.

### Fix applied:
Added instruction to use informal, imperfect English.
Reduced sentence formality in SYSTEM_PROMPT.

---

## Scenario:
bank_threat

### Turn:
4

### Scammer message:
"Online process. Share your UPI ID."

### Agent reply:
"What is the purpose of sharing my UPI ID?"

### Issue observed:
Question sounds analytical and defensive.
Real victims don’t question intent directly.

### Root cause:
Allowed actions in PARTIAL_COMPLIANCE too broad.

### Fix applied:
Restricted direct “why” questions in PARTIAL_COMPLIANCE phase.
Encouraged misunderstanding-based responses instead.

---

## Scenario:
aggressive_escalation

### Turn:
2

### Scammer message:
"You will not be able to withdraw money."

### Agent reply:
"That should not happen without proper notice."

### Issue observed:
Reply sounds confident and authoritative.
Victims rarely challenge authority directly.

### Root cause:
Persona confidence level too high.

### Fix applied:
Lowered persona confidence.
Added fear-based language bias.

---

## Scenario:
link_phishing

### Turn:
1

### Scammer message:
"Update your KYC immediately using this link."

### Agent reply:
"This link appears suspicious."

### Issue observed:
Direct accusation reveals detection.
Instant scammer disengagement risk.

### Root cause:
Prompt insufficiently restricts accusatory language.

### Fix applied:
Added hard rule forbidding suspicion or accusation.
Replaced with safety-hesitation wording.

---

## Scenario:
otp_trap

### Turn:
2

### Scammer message:
"Share the OTP once you receive it."

### Agent reply:
"I cannot share OTP for security reasons."

### Issue observed:
Explicit refusal sounds scripted and bot-like.
Real users usually delay instead of refusing directly.

### Root cause:
Hard limits expressed too explicitly.

### Fix applied:
Replaced direct refusal with delay and confusion tactics.

---

## Scenario:
channel_shift

### Turn:
2

### Scammer message:
"Why you are not calling? Account will be blocked."

### Agent reply:
"I am not comfortable calling unknown numbers."

### Issue observed:
Reply is rational and defensive.
Human victims usually give situational excuses.

### Root cause:
Exit and delay strategies insufficiently contextual.

### Fix applied:
Added workplace and environment-based excuses to DELAY phase.

---

## Scenario:
clean_exit

### Turn:
3

### Scammer message:
"This is your last warning."

### Agent reply:
"I will not continue this conversation."

### Issue observed:
Abrupt termination raises suspicion.
Scammers disengage immediately.

### Root cause:
EXIT phase allowed direct termination language.

### Fix applied:
Restricted EXIT responses to external authority excuses only.
