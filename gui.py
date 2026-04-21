import tkinter as tk
from core import generate_password, get_temp_email

def update_fields():
    pass_entry.delete(0, tk.END)
    pass_entry.insert(0, generate_password())
    
    email_entry.delete(0, tk.END)
    email_entry.insert(0, get_temp_email())

app = tk.Tk()
app.title("EphemeralKey v1.0")
app.geometry("400x250")

tk.Label(app, text="Contraseña Segura:").pack(pady=5)
pass_entry = tk.Entry(app, width=40)
pass_entry.pack()

tk.Label(app, text="Correo Temporal:").pack(pady=5)
email_entry = tk.Entry(app, width=40)
email_entry.pack()

tk.Button(app, text="Generar Todo", command=update_fields, bg="#3498db", fg="white").pack(pady=20)

app.mainloop()