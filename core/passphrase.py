import secrets
import os

def generate_passphrase(words_count: int = 4, separator: str = "-") -> str:
    """Genera una passphrase facil de recordar pero matematicamente segura"""
    path = os.path.join(os.path.dirname(__file__), '..', 'data', 'wordlist.txt')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            words = [w.strip() for w in f.readlines() if w.strip()]
        if not words: raise ValueError("Wordlist empty")
        return separator.join(secrets.choice(words) for _ in range(words_count))
    except FileNotFoundError:
        return f"error{separator}wordlist{separator}not{separator}found"
