from core.network import get_secure_session
import sys

def check_apis():
    session = get_secure_session()
    print("[*] Verificando 1secmail...")
    r1 = session.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1")
    print("[*] Verificando HIBP...")
    r2 = session.get("https://api.pwnedpasswords.com/range/00000")
    
    if r1.status_code == 200 and r2.status_code == 200:
        print("[+] Todos los sistemas externos operativos.")
        sys.exit(0)
    print("[-] Sistemas degradados.")
    sys.exit(1)

if __name__ == "__main__":
    check_apis()
