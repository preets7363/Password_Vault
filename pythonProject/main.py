import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import ttk

root = tk.Tk()
root.tk_setPalette(background='#242424', foreground='white', activeBackground='#565656', activeForeground='white')


conn = sqlite3.connect('password_vault.db')
c = conn.cursor()


c.execute('''CREATE TABLE IF NOT EXISTS passwords
             (id INTEGER PRIMARY KEY AUTOINCREMENT,
              service TEXT NOT NULL,
              username TEXT NOT NULL,
              password TEXT NOT NULL)''')


def add_password():
    service = simpledialog.askstring("Service", "Enter the name of the service:")
    username = simpledialog.askstring("Username", "Enter your username for " + service + ":")
    password = simpledialog.askstring("Password", "Enter your password for " + service + ":")
    c.execute("INSERT INTO passwords (service, username, password) VALUES (?, ?, ?)", (service, username, password))
    conn.commit()


def view_passwords():
    passwords = ""
    for row in c.execute("SELECT * FROM passwords"):
        passwords += "Service: " + row[1] + "\n"
        passwords += "Username: " + row[2] + "\n"
        passwords += "Password: " + row[3] + "\n\n"
    if passwords == "":
        passwords = "No passwords found."
    messagebox.showinfo("Passwords", passwords)


menu = tk.Menu(root)
root.config(menu=menu)
file_menu = tk.Menu(menu)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Exit", command=root.quit)
password_menu = tk.Menu(menu)
menu.add_cascade(label="Password", menu=password_menu)
password_menu.add_command(label="Add", command=add_password)
password_menu.add_command(label="View", command=view_passwords)


add_button = ttk.Button(root, text="Add Password", command=add_password)
add_button.pack(pady=10)
view_button = ttk.Button(root, text="View Passwords", command=view_passwords)
view_button.pack(pady=10)

root.mainloop()

conn.close()
