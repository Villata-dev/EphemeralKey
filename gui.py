import customtkinter as ctk
import secrets
import string
import requests
import threading
import time
import tkinter as tk
from tkinter import messagebox

# --- LÓGICA CORE (Integrada y Optimizada) ---

def generate_secure_password(length=18):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

def get_temp_email():
    try:
        response = requests.get("https://www.1secmail.com/api/v1/?action=genRandomMailbox&count=1", timeout=5)
        if response.status_code == 200:
            return response.json()[0]
    except Exception:
        pass
    return None

def check_inbox(email):
    try:
        user, domain = email.split('@')
        url = f"https://www.1secmail.com/api/v1/?action=getMessages&login={user}&domain={domain}"
        response = requests.get(url, timeout=5)
        return response.json() if response.status_code == 200 else []
    except Exception:
        return []

def read_message(email, mail_id):
    try:
        user, domain = email.split('@')
        url = f"https://www.1secmail.com/api/v1/?action=readMessage&login={user}&domain={domain}&id={mail_id}"
        response = requests.get(url, timeout=5)
        return response.json() if response.status_code == 200 else None
    except Exception:
        return None

# --- INTERFAZ GRÁFICA V2.0 ---

class EphemeralKeyApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("EphemeralKey | Privacy Suite V2.0")
        self.geometry("550x700")
        self.resizable(False, False)
        
        self.configure(fg_color="#090B10")
        ctk.set_appearance_mode("dark")

        self.current_email = ""
        self.inbox_thread_active = False

        self.font_title = ctk.CTkFont(family="Consolas", size=24, weight="bold")
        self.font_bold = ctk.CTkFont(family="Consolas", size=13, weight="bold")
        self.font_mono = ctk.CTkFont(family="Consolas", size=12)

        # --- CABECERA ---
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.header_frame.pack(pady=(20, 10))
        
        self.lbl_title = ctk.CTkLabel(self.header_frame, text="[ 🔑 EPHEMERAL-KEY ]", font=self.font_title, text_color="#8B5CF6")
        self.lbl_title.pack()
        self.lbl_sub = ctk.CTkLabel(self.header_frame, text="GHOST IDENTITY & SECURE CREDENTIALS", font=self.font_mono, text_color="#5C6B89")
        self.lbl_sub.pack()

        # --- SECCIÓN: PASSWORD FORGE ---
        self.pass_frame = ctk.CTkFrame(self, fg_color="#151A22", corner_radius=4, border_width=1, border_color="#2A3241")
        self.pass_frame.pack(pady=10, padx=20, fill="x")

        self.lbl_pass_title = ctk.CTkLabel(self.pass_frame, text="[ CREDENTIAL GENERATOR ]", font=self.font_bold, text_color="#00E5FF")
        self.lbl_pass_title.pack(pady=(10, 5))

        self.pass_input_frame = ctk.CTkFrame(self.pass_frame, fg_color="transparent")
        self.pass_input_frame.pack(pady=5)

        self.entry_pass = ctk.CTkEntry(self.pass_input_frame, width=280, height=35, font=self.font_mono, fg_color="#0F1219", border_color="#374151")
        self.entry_pass.grid(row=0, column=0, padx=5)

        self.btn_gen_pass = ctk.CTkButton(self.pass_input_frame, text="⚡ Gen", width=60, font=self.font_bold, fg_color="transparent", border_width=1, border_color="#00E5FF", text_color="#00E5FF", hover_color="#0F3846", command=self.update_password)
        self.btn_gen_pass.grid(row=0, column=1, padx=5)

        self.btn_copy_pass = ctk.CTkButton(self.pass_input_frame, text="📋", width=40, font=self.font_bold, fg_color="#1E2430", hover_color="#2A3241", command=lambda: self.copy_to_clipboard(self.entry_pass.get(), "Contraseña"))
        self.btn_copy_pass.grid(row=0, column=2, padx=5)

        # --- SECCIÓN: GHOST MAIL ---
        self.mail_frame = ctk.CTkFrame(self, fg_color="#151A22", corner_radius=4, border_width=1, border_color="#2A3241")
        self.mail_frame.pack(pady=10, padx=20, fill="x")

        self.lbl_mail_title = ctk.CTkLabel(self.mail_frame, text="[ DISPOSABLE INBOX ]", font=self.font_bold, text_color="#10B981")
        self.lbl_mail_title.pack(pady=(10, 5))

        self.mail_input_frame = ctk.CTkFrame(self.mail_frame, fg_color="transparent")
        self.mail_input_frame.pack(pady=5)

        self.entry_mail = ctk.CTkEntry(self.mail_input_frame, width=280, height=35, font=self.font_mono, fg_color="#0F1219", border_color="#374151", state="readonly")
        self.entry_mail.grid(row=0, column=0, padx=5)

        self.btn_gen_mail = ctk.CTkButton(self.mail_input_frame, text="🌐 New", width=60, font=self.font_bold, fg_color="transparent", border_width=1, border_color="#10B981", text_color="#10B981", hover_color="#064E3B", command=self.update_email)
        self.btn_gen_mail.grid(row=0, column=1, padx=5)

        self.btn_copy_mail = ctk.CTkButton(self.mail_input_frame, text="📋", width=40, font=self.font_bold, fg_color="#1E2430", hover_color="#2A3241", command=lambda: self.copy_to_clipboard(self.entry_mail.get(), "Correo"))
        self.btn_copy_mail.grid(row=0, column=2, padx=5)

        # --- BANDEJA DE ENTRADA (CONSOLA) ---
        self.lbl_inbox = ctk.CTkLabel(self.mail_frame, text=">_ INBOX MONITOR (Auto-refresh 10s)", font=self.font_mono, text_color="#4B5563")
        self.lbl_inbox.pack(pady=(10, 0))

        self.txt_inbox = ctk.CTkTextbox(self.mail_frame, height=200, width=450, font=self.font_mono, fg_color="#090B10", text_color="#D1D5DB", border_width=1, border_color="#2A3241", state="disabled")
        self.txt_inbox.pack(pady=(5, 15), padx=15)

        # --- BARRA DE ESTADO ---
        self.lbl_status = ctk.CTkLabel(self, text="SYS_STATUS: READY.", text_color="#5C6B89", font=self.font_mono)
        self.lbl_status.pack(side="bottom", pady=10)

        # Iniciar datos iniciales
        self.update_password()

    # --- FUNCIONES DE LA UI ---

    def update_password(self):
        new_pass = generate_secure_password()
        self.entry_pass.delete(0, 'end')
        self.entry_pass.insert(0, new_pass)
        self.lbl_status.configure(text="SYS_STATUS: NEW SECURE CREDENTIAL GENERATED.", text_color="#00E5FF")

    def update_email(self):
        self.lbl_status.configure(text="SYS_STATUS: NEGOTIATING SECURE MAILBOX...", text_color="#F59E0B")
        self.update() # Refrescar UI
        
        new_mail = get_temp_email()
        if new_mail:
            self.current_email = new_mail
            self.entry_mail.configure(state="normal")
            self.entry_mail.delete(0, 'end')
            self.entry_mail.insert(0, new_mail)
            self.entry_mail.configure(state="readonly")
            self.lbl_status.configure(text=f"SYS_STATUS: MAILBOX AQUIRED [{new_mail}]", text_color="#10B981")
            
            self.txt_inbox.configure(state="normal")
            self.txt_inbox.delete("1.0", "end")
            self.txt_inbox.insert("end", "[ SYSTEM ] Listening for incoming traffic...\n")
            self.txt_inbox.configure(state="disabled")

            # Iniciar el hilo de monitoreo si no está activo
            if not self.inbox_thread_active:
                self.inbox_thread_active = True
                threading.Thread(target=self.monitor_inbox, daemon=True).start()
        else:
            self.lbl_status.configure(text="SYS_STATUS: API CONNECTION FAILED.", text_color="#EF4444")

    def monitor_inbox(self):
        """Hilo en segundo plano que revisa el correo cada 10 segundos"""
        known_emails = set()
        while self.inbox_thread_active and self.current_email:
            emails = check_inbox(self.current_email)
            if emails:
                for mail in emails:
                    mail_id = mail.get('id')
                    if mail_id not in known_emails:
                        known_emails.add(mail_id)
                        sender = mail.get('from', 'Unknown')
                        subject = mail.get('subject', 'No Subject')
                        date = mail.get('date', '')
                        
                        # Fetch full message content
                        full_msg = read_message(self.current_email, mail_id)
                        body = full_msg.get('textBody', '') if full_msg else ''
                        
                        log_entry = f"\n[{date}] FROM: {sender}\nSUBJECT: {subject}\nCONTENT: {body[:100]}...\n{'-'*40}\n"
                        
                        self.txt_inbox.configure(state="normal")
                        self.txt_inbox.insert("end", log_entry)
                        self.txt_inbox.see("end")
                        self.txt_inbox.configure(state="disabled")
                        self.lbl_status.configure(text="SYS_STATUS: NEW MESSAGE INTERCEPTED!", text_color="#8B5CF6")
            time.sleep(10)

    def copy_to_clipboard(self, text, item_name):
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)
            self.lbl_status.configure(text=f"SYS_STATUS: {item_name.upper()} COPIED TO CLIPBOARD.", text_color="#F59E0B")

if __name__ == "__main__":
    app = EphemeralKeyApp()
    app.mainloop()