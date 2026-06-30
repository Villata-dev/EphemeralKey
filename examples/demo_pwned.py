from core.pwned import check_password_breach

if __name__ == "__main__":
    test_pass = "password123"
    leaks = check_password_breach(test_pass)
    print(f"La contrasena '{test_pass}' se ha filtrado {leaks} veces en la dark web.")
