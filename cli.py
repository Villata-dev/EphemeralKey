import argparse
import secrets
import string
import requests
import sys
import time

def generate_password(length):
    chars = string.ascii_letters + string.digits + string.punctuation
    pwd = ''.join(secrets.choice(chars) for _ in range(length))
    print(f"\n[+] CREDENCIAL GENERADA (Entropía aprox: {length * 6} bits):")
    print(f"    > {pwd}\n")

def generate_email():
    try:
        print("[*] Negociando buzón efímero...")
        r = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1", timeout=5)
        if r.status_code == 200:
            email = r.json()[0]
            print(f"\n[+] IDENTIDAD ADQUIRIDA:")
            print(f"    > {email}\n")
            print("Para revisar la bandeja, usa: python cli.py --check " + email)
        else:
            print("[-] Error: La API rechazó la solicitud.")
    except Exception as e:
        print(f"[-] Error de conexión: {e}")

def check_inbox(email):
    try:
        user, domain = email.split('@')
        print(f"[*] Interceptando tráfico para {email}...")
        r = requests.get(f"https://www.1secmail.com/api/v1/?action=getMessages&login={user}&domain={domain}", timeout=5)
        
        messages = r.json() if r.status_code == 200 else []
        if not messages:
            print("[-] Bandeja vacía. No hay paquetes entrantes.")
            return

        print(f"\n[+] {len(messages)} MENSAJE(S) ENCONTRADO(S):\n")
        for msg in messages:
            print(f"    ID     : {msg['id']}")
            print(f"    FROM   : {msg['from']}")
            print(f"    ASUNTO : {msg['subject']}")
            print(f"    FECHA  : {msg['date']}")
            print("-" * 50)
            
            # Auto-leer el contenido del último mensaje
            read_r = requests.get(f"https://www.1secmail.com/api/v1/?action=readMessage&login={user}&domain={domain}&id={msg['id']}", timeout=5)
            if read_r.status_code == 200:
                body = read_r.json().get('textBody', '')
                print(f"{body.strip()}\n")
            print("=" * 50)

    except Exception as e:
        print(f"[-] Error al consultar la bandeja: {e}")

def main():
    parser = argparse.ArgumentParser(description="EphemeralKey Headless CLI - Privacy Suite")
    
    parser.add_argument('-p', '--password', action='store_true', help='Genera una contraseña criptográficamente segura')
    parser.add_argument('-l', '--length', type=int, default=24, help='Longitud de la contraseña (por defecto: 24)')
    parser.add_argument('-e', '--email', action='store_true', help='Genera una dirección de correo temporal')
    parser.add_argument('-c', '--check', type=str, metavar='EMAIL', help='Revisa la bandeja de entrada de un correo generado')

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    print("\n--- EPHEMERAL-KEY CLI ---")
    if args.password:
        generate_password(args.length)
    
    if args.email:
        generate_email()
        
    if args.check:
        check_inbox(args.check)

if __name__ == '__main__':
    main()