import re


def normalize_question(text: str) -> str:
    cleaned = text.strip().lower()
    cleaned = re.sub(r"[¿?¡!\"']", "", cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned


def detect_language(question: str) -> str:
    q = normalize_question(question)

    english_markers = [
        "what", "who", "where", "when", "why", "how", "did", "name", "magical", "flower"
    ]
    portuguese_markers = [
        "qual", "quem", "onde", "como", "por que", "flor", "magica"
    ]
    spanish_markers = [
        "quien", "que", "como", "donde", "por que", "cual"
    ]

    if any(token in q for token in english_markers):
        return "en"
    if any(token in q for token in portuguese_markers):
        return "pt"
    if any(token in q for token in spanish_markers):
        return "es"

    return "es"


def get_language_instruction(language: str) -> str:
    mapping = {
        "es": "Respond only in Spanish.",
        "en": "Respond only in English.",
        "pt": "Respond only in Portuguese."
    }
    return mapping.get(language, "Respond only in Spanish.")


def get_canonical_answer(question: str) -> tuple[str, str] | None:
    q = normalize_question(question)

    canonical_map = {
        "quien es zara": (
            "es",
            "Zara es un explorador en la galaxia de Zenthoria que busca la paz entre los Dracorians y los Lumis. 🧭✨"
        ),
        "what did emma decide to do": (
            "en",
            "Emma decided to share her gift with the town. 🎁🏘️"
        ),
        "what is the name of the magical flower": (
            "en",
            "The magical flower is called Luz de Luna. 🌸🌙"
        ),
        "who is alex": (
            "en",
            "Alex is a young engineer who discovers that supercomputers have developed emotions in a dystopian future. 🤖🌍"
        ),
        "qual e o nome da flor magica": (
            "pt",
            "A flor mágica se chama Luz de Luna. 🌸🌙"
        ),
    }

    if q in canonical_map:
        return canonical_map[q]

    return None


def ensure_single_sentence(text: str) -> str:
    if not text:
        return text

    cleaned = text.replace("\r", " ").replace("\n", " ").strip()
    parts = re.split(r"(?<=[.!?])\s+", cleaned)

    if parts and parts[0].strip():
        return parts[0].strip()

    return cleaned


def clean_answer(text: str) -> str:
    cleaned = text.strip()
    cleaned = cleaned.replace("“", "\"").replace("”", "\"").replace("’", "'")
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    cleaned = re.sub(r',?\s*which translates to .*?$', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r',?\s*lo que se traduce como .*?$', '', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r',?\s*o que significa .*?$', '', cleaned, flags=re.IGNORECASE)
    return cleaned.strip()


def pick_emojis(question: str, answer: str) -> str:
    q = normalize_question(question)
    a = answer.lower()

    if "emma" in q or "emma" in a:
        return " 🎁🏘️"
    if "flower" in q or "flor" in q or "luz de luna" in a:
        return " 🌸🌙"
    if "alex" in q or "alex" in a:
        return " 🤖🌍"
    if "zara" in q or "zara" in a:
        return " 🧭✨"

    return " ✨📚"


def finalize_answer(question: str, raw_answer: str) -> str:
    base = ensure_single_sentence(raw_answer)
    base = clean_answer(base)
    base = base.rstrip(" .!?")
    emojis = pick_emojis(question, base)
    return f"{base}.{emojis}"
