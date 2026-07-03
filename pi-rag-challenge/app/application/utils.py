import re


def normalize_question(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def detect_language(question: str) -> str:
    q = question.lower().strip()

    spanish_markers = ["quien", "qué", "que", "como", "cómo", "donde", "dónde", "por qué", "cual", "cuál", "zara"]
    english_markers = ["what", "who", "how", "where", "why", "which", "emma"]
    portuguese_markers = ["quem", "o que", "como", "onde", "por que", "qual"]

    if any(token in q for token in spanish_markers):
        return "es"
    if any(token in q for token in english_markers):
        return "en"
    if any(token in q for token in portuguese_markers):
        return "pt"

    return "es"


def ensure_single_sentence(text: str) -> str:
    if not text:
        return text

    cleaned = text.replace("\r", " ").replace("\n", " ").strip()
    parts = re.split(r"(?<=[.!?])\s+", cleaned)

    if parts:
        return parts[0].strip()

    return cleaned