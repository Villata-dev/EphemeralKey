import tkinter as tk
from tkinter import messagebox
from core import generate_password

def get_new_pass():
    password = generate_password()
    entry_pass.delete(0, tk.END)
    entry_pass.insert(0, password)

root = tk.Tk()
root.title("EphemeralKey Desktop")
root.geometry("300x200")

label = tk.Label(root, text="Tu Llave Segura:", pady=10)
label.pack()

entry_pass = tk.Entry(root, font=("Arial", 12), width=25)
entry_pass.pack(pady=5)

btn_gen = tk.Button(root, text="Generar Nueva", command=get_new_pass, bg="#2ecc71", fg="white")
btn_gen.pack(pady=20)

root.mainloop()