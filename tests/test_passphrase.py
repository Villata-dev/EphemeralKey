from core.passphrase import generate_passphrase

def test_passphrase_format():
    phrase = generate_passphrase(words_count=5, separator="-")
    assert len(phrase.split("-")) == 5
