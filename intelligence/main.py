import os
import yaml
import logging

from extraction.data_loader import load_all_conversations
from extraction.regex_extractor import extract_phone_numbers, extract_upi_ids
from validation.validators import validate_phone_numbers, validate_upi_ids
from storage.json_storage import save_to_json
from extraction.llm_extractor import ai_extract_insights
from extraction.scam_classifier import classify_scam
from extraction.regex_extractor import extract_phishing_links
from extraction.keyword_extractor import extract_suspicious_keywords





def load_config():
    with open("configs/config.yaml", "r") as file:
        return yaml.safe_load(file)


def setup_logging(log_path):
    os.makedirs(log_path, exist_ok=True)
    logging.basicConfig(
        filename=os.path.join(log_path, "system.log"),
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


def main():
    print("Starting Scam Intelligence Extraction System...")

    config = load_config()
    setup_logging(config["paths"]["logs"])

    raw_data_path = config["paths"]["raw_data"]

    conversations = load_all_conversations(raw_data_path)

    print(f"Loaded {len(conversations)} conversation(s)")
    logging.info(f"Loaded {len(conversations)} conversation(s)")

    for file_name, messages in conversations.items():
        raw_phones = extract_phone_numbers(messages)
        raw_upis = extract_upi_ids(messages)

        phones = validate_phone_numbers(raw_phones)
        upis = validate_upi_ids(raw_upis)

        ai_insights = ai_extract_insights(messages)

        links = extract_phishing_links(messages)
        suspicious_keywords = extract_suspicious_keywords(messages)


        scam_label = classify_scam(messages, ai_insights)

        api_payload = {
            "sessionId": file_name.replace(".txt", "-session-id"),
            "scamDetected": True,
            "totalMessagesExchanged": len(messages),
            "extractedIntelligence": {
                "bankAccounts": [],
                "upiIds": upis,
                "phishingLinks": links,
                "phoneNumbers": phones,
                "suspiciousKeywords": suspicious_keywords
            },
            "agentNotes": "Scammer used urgency tactics and payment redirection"
        }

        save_to_json(
            api_payload,
            "data/processed",
            file_name.replace(".txt", ".json")
        )

        print(f"Saved output for {file_name}")

        print(f"\nConversation: {file_name}")
        print("Phone Numbers:", phones)
        print("UPI IDs:", upis)

        print("Messages:")
        for msg in messages:
            print(msg)


if __name__ == "__main__":
    main()
