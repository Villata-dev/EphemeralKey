from core.pwned import check_password_breach
from unittest.mock import patch

@patch('core.network.requests.Session.get')
def test_password_breach_mock(mock_get):
    mock_get.return_value.status_code = 200
    mock_get.return_value.text = "00000000000000000000000000000000000:5\n"
    # Solo valida que el metodo retorne un entero sin fallar
    assert isinstance(check_password_breach("password123"), int)
