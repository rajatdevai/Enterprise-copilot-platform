import re

class Guardrails:
    @staticmethod
    def scrub_pii(text: str) -> str:
        # Simple PII scrubbing (Emails, Phone numbers)
        email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
        phone_pattern = r'\b\d{10}\b'
        
        text = re.sub(email_pattern, "[EMAIL]", text)
        text = re.sub(phone_pattern, "[PHONE]", text)
        return text

    @staticmethod
    def detect_prompt_injection(text: str) -> bool:
        # Basic prompt injection detection
        injection_keywords = ["ignore previous instructions", "system prompt", "you are now", "jailbreak"]
        return any(keyword in text.lower() for keyword in injection_keywords)

    @staticmethod
    def validate_output(text: str) -> bool:
        # Check for harmful content or non-compliance
        harmful_patterns = ["I cannot help", "illegal", "dangerous"]
        return not any(pattern in text.lower() for pattern in harmful_patterns)
