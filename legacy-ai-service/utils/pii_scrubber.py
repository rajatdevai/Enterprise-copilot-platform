import re

class PIIScrubber:
    def __init__(self):
        # Regex patterns for common PII
        self.patterns = {
            "EMAIL": r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+',
            "PHONE": r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b',
            "SSN": r'\b\d{3}-\d{2}-\d{4}\b',
            "CREDIT_CARD": r'\b(?:\d[ -]*?){13,16}\b'
        }

    def scrub(self, text: str) -> str:
        """
        Masks PII before data leaves the internal network.
        """
        scrubbed_text = text
        for label, pattern in self.patterns.items():
            scrubbed_text = re.sub(pattern, f"<{label}_REDACTED>", scrubbed_text)
        return scrubbed_text

# Singleton for easy access
pii_scrubber = PIIScrubber()
