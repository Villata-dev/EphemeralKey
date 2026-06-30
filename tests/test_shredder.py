import os
from core.shredder import secure_delete

def test_secure_delete(tmp_path):
    test_file = tmp_path / "secret.txt"
    test_file.write_text("sensitivedata")
    secure_delete(str(test_file))
    assert not test_file.exists()
