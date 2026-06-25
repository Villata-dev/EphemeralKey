import customtkinter as ctk
import secrets
import string
import requests
import threading
import time
import math
import os
from tkinter import filedialog, messagebox

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

# --- INTERFAZ GRÁFICA V3.0 ---

class EphemeralKeyApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("EphemeralKey | Privacy Suite V3.0")
        self.geometry("550x780")
        self.resizable(False, False)
        
        self.configure(fg_color="#090B10")
        ctk.set_appearance_mode("dark")

        self.current_email = ""
        self.inbox_thread_active = False
        self.clipboard_timer = None

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
        self.entry_pass.bind("<KeyRelease>", self.evaluate_entropy)

        self.btn_gen_pass = ctk.CTkButton(self.pass_input_frame, text="⚡ Gen", width=60, font=self.font_bold, fg_color="transparent", border_width=1, border_color="#00E5FF", text_color="#00E5FF", hover_color="#0F3846", command=self.update_password)
        self.btn_gen_pass.grid(row=0, column=1, padx=5)

        self.btn_copy_pass = ctk.CTkButton(self.pass_input_frame, text="📋", width=40, font=self.font_bold, fg_color="#1E2430", hover_color="#2A3241", command=lambda: self.secure_copy_to_clipboard(self.entry_pass.get(), "Contraseña"))
        self.btn_copy_pass.grid(row=0, column=2, padx=5)

        # NUEVO: Medidor de Entropía
        self.entropy_frame = ctk.CTkFrame(self.pass_frame, fg_color="transparent")
        self.entropy_frame.pack(pady=(5, 10), fill="x", padx=20)
        
        self.lbl_entropy = ctk.CTkLabel(self.entropy_frame, text="ENTROPÍA: -- BITS", font=self.font_mono, text_color="#4B5563")
        self.lbl_entropy.pack(side="left")
        
        self.prog_entropy = ctk.CTkProgressBar(self.entropy_frame, width=150, height=8, progress_color="#4B5563", fg_color="#0F1219")
        self.prog_entropy.pack(side="right", pady=8)
        self.prog_entropy.set(0)

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

        self.btn_copy_mail = ctk.CTkButton(self.mail_input_frame, text="📋", width=40, font=self.font_bold, fg_color="#1E2430", hover_color="#2A3241", command=lambda: self.secure_copy_to_clipboard(self.entry_mail.get(), "Correo", auto_purge=False))
        self.btn_copy_mail.grid(row=0, column=2, padx=5)

        # --- BANDEJA DE ENTRADA (CONSOLA) ---
        self.lbl_inbox = ctk.CTkLabel(self.mail_frame, text=">_ INBOX MONITOR (Auto-refresh 10s)", font=self.font_mono, text_color="#4B5563")
        self.lbl_inbox.pack(pady=(10, 0))

        self.txt_inbox = ctk.CTkTextbox(self.mail_frame, height=160, width=450, font=self.font_mono, fg_color="#090B10", text_color="#D1D5DB", border_width=1, border_color="#2A3241", state="disabled")
        self.txt_inbox.pack(pady=(5, 10), padx=15)

        # --- ACCIONES GLOBALES ---
        self.action_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.action_frame.pack(pady=5)

        self.btn_export = ctk.CTkButton(self.action_frame, text="💾 Exportar Identidad", width=200, font=self.font_bold, fg_color="transparent", border_width=1, border_color="#F59E0B", text_color="#F59E0B", hover_color="#B45309", command=self.export_identity)
        self.btn_export.pack()

        # --- BARRA DE ESTADO ---
        self.lbl_status = ctk.CTkLabel(self, text="SYS_STATUS: READY.", text_color="#5C6B89", font=self.font_mono)
        self.lbl_status.pack(side="bottom", pady=10)

        # Iniciar datos iniciales
        self.update_password()

    # --- FUNCIONES DE SEGURIDAD Y UI ---

    def evaluate_entropy(self, event=None):
        """Calcula la entropía de Shannon de la contraseña actual"""
        password = self.entry_pass.get()
        if not password:
            self.lbl_entropy.configure(text="ENTROPÍA: -- BITS", text_color="#4B5563")
            self.prog_entropy.set(0)
            self.prog_entropy.configure(progress_color="#4B5563")
            return

        # Calcular pool de caracteres posibles
        pool = 0
        if any(c.islower() for c in password): pool += 26
        if any(c.isupper() for c in password): pool += 26
        if any(c.isdigit() for c in password): pool += 10
        if any(c in string.punctuation for c in password): pool += 32

        # Entropía = L * log2(R)
        entropy = len(password) * math.log2(pool) if pool > 0 else 0

        if entropy < 40:
            color, tag = "#EF4444", "DÉBIL"
            val = min(entropy / 100, 0.3)
        elif entropy < 70:
            color, tag = "#F59E0B", "MODERADA"
            val = min(entropy / 100, 0.6)
        elif entropy < 100:
            color, tag = "#10B981", "FUERTE"
            val = min(entropy / 100, 0.9)
        else:
            color, tag = "#00E5FF", "MILITAR"
            val = 1.0

        self.lbl_entropy.configure(text=f"ENTROPÍA: {int(entropy)} BITS [{tag}]", text_color=color)
        self.prog_entropy.set(val)
        self.prog_entropy.configure(progress_color=color)

    def update_password(self):
        new_pass = generate_secure_password(24) # Aumentado a 24 por defecto para mayor seguridad
        self.entry_pass.delete(0, 'end')
        self.entry_pass.insert(0, new_pass)
        self.evaluate_entropy()
        self.lbl_status.configure(text="SYS_STATUS: NEW SECURE CREDENTIAL GENERATED.", text_color="#00E5FF")

    def secure_copy_to_clipboard(self, text, item_name, auto_purge=True):
        if text:
            self.clipboard_clear()
            self.clipboard_append(text)
            
            if auto_purge:
                self.lbl_status.configure(text=f"SYS_STATUS: {item_name.upper()} COPIED. PURGE IN 15S.", text_color="#F59E0B")
                # Resetear el timer si ya había uno corriendo
                if self.clipboard_timer and self.clipboard_timer.is_alive():
                    self.clipboard_timer.cancel()
                self.clipboard_timer = threading.Timer(15.0, self.purge_clipboard)
                self.clipboard_timer.start()
            else:
                self.lbl_status.configure(text=f"SYS_STATUS: {item_name.upper()} COPIED TO CLIPBOARD.", text_color="#10B981")

    def purge_clipboard(self):
        """Purga el portapapeles del SO por seguridad"""
        try:
            self.clipboard_clear()
            self.clipboard_append("")
            self.lbl_status.configure(text="SYS_STATUS: CLIPBOARD PURGED FOR SECURITY.", text_color="#5C6B89")
        except Exception:
            pass

    def export_identity(self):
        """Exporta las credenciales efímeras a un archivo de texto"""
        pwd = self.entry_pass.get()
        mail = self.entry_mail.get()
        
        if not pwd and not mail:
            messagebox.showwarning("Export Error", "No hay identidad generada para exportar.")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile="ephemeral_identity.txt",
            title="Guardar Identidad Efímera",
            filetypes=[("Text Files", "*.txt")]
        )
        
        if filepath:
            try:
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write("=== EPHEMERAL IDENTITY EXPORT ===\n")
                    f.write(f"DATE: {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                    f.write("-" * 35 + "\n")
                    f.write(f"EMAIL   : {mail if mail else 'None'}\n")
                    f.write(f"PASSWORD: {pwd if pwd else 'None'}\n")
                    f.write("-" * 35 + "\n")
                    f.write("DESTROY THIS FILE AFTER USE.\n")
                
                self.lbl_status.configure(text="SYS_STATUS: IDENTITY EXPORTED SUCCESSFULLY.", text_color="#10B981")
            except Exception as e:
                messagebox.showerror("IO Error", f"Error guardando el archivo: {e}")

    def update_email(self):
        self.lbl_status.configure(text="SYS_STATUS: NEGOTIATING SECURE MAILBOX...", text_color="#F59E0B")
        self.update()
        
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

            if not self.inbox_thread_active:
                self.inbox_thread_active = True
                threading.Thread(target=self.monitor_inbox, daemon=True).start()
        else:
            self.lbl_status.configure(text="SYS_STATUS: API CONNECTION FAILED.", text_color="#EF4444")

    def monitor_inbox(self):
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
                        
                        full_msg = read_message(self.current_email, mail_id)
                        body = full_msg.get('textBody', '') if full_msg else ''
                        
                        log_entry = f"\n[{date}]\nFROM: {sender}\nSUBJECT: {subject}\nCONTENT: {body[:150]}...\n{'-'*45}\n"
                        
                        self.txt_inbox.configure(state="normal")
                        self.txt_inbox.insert("end", log_entry)
                        self.txt_inbox.see("end")
                        self.txt_inbox.configure(state="disabled")
                        self.lbl_status.configure(text="SYS_STATUS: NEW MESSAGE INTERCEPTED!", text_color="#8B5CF6")
            time.sleep(10)

if __name__ == "__main__":
    app = EphemeralKeyApp()
    app.mainloop()