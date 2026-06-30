from core.crypto import generate_complex_password

def test_password_length():
    pwd = generate_complex_password(32)
    assert len(pwd) == 32

def test_no_ambiguous_chars():
    pwd = generate_complex_password(100, exclude_ambiguous=True)
    for char in 'l1O0I':
        assert char not in pwd
