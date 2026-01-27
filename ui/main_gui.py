import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
import os
import sys
import random
import string
import requests
from PIL import Image, ImageTk

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
os.makedirs(DATA_DIR, exist_ok=True)
USER_DB = os.path.join(DATA_DIR, 'user.db')

# Ensure user DB exists
conn = sqlite3.connect(USER_DB)
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT,
        email TEXT,
        code TEXT
    )
''')
conn.commit()
conn.close()

def get_ip():
    try:
        return requests.get("https://ipinfo.io/json").json().get("ip", "Unavailable")
    except:
        return "Unavailable"

def generate_user_code(username):
    conn = sqlite3.connect(USER_DB)
    cursor = conn.cursor()
    existing = cursor.execute("SELECT COUNT(*) FROM users WHERE username LIKE ?", (f"{username}%",)).fetchone()[0]
    conn.close()
    return f"{username}{str(existing+1).zfill(3)}"

class AuthApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("CyberSecure Auth")
        self.root.attributes("-fullscreen", True)

        self.canvas = tk.Canvas(self.root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
        self.canvas.pack(fill="both", expand=True)

        self.set_background()
        self.show_main_menu()

    def set_background(self):
        try:
            bg_image = Image.open("bg.jpg")
            bg_image = bg_image.resize((self.root.winfo_screenwidth(), self.root.winfo_screenheight()))
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        except:
            self.canvas.configure(bg="black")

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ip = get_ip()
        nav = tk.Label(self.canvas, text=f"Time: {now} | IP: {ip}", font=("Helvetica", 12), bg="#1e1e2e", fg="white")
        nav.place(x=20, y=10)

    def show_main_menu(self):
        self.clear_widgets()

        title = tk.Label(self.canvas, text="Welcome to CyberSecure Logger", font=("Helvetica", 28, "bold"), bg="black", fg="#00ffc6")
        title.place(relx=0.5, rely=0.2, anchor="center")

        login_btn = tk.Button(self.canvas, text="Login", command=self.show_login_screen, width=20, bg="#1e90ff", fg="white")
        login_btn.place(relx=0.5, rely=0.35, anchor="center")

        signup_btn = tk.Button(self.canvas, text="Sign Up", command=self.show_signup_screen, width=20, bg="#28a745", fg="white")
        signup_btn.place(relx=0.5, rely=0.42, anchor="center")

        admin_btn = tk.Button(self.canvas, text="Admin Login", command=lambda: messagebox.showinfo("Coming Soon", "Admin Portal is Coming Soon..."), width=20, bg="#444", fg="white")
        admin_btn.place(relx=0.5, rely=0.49, anchor="center")

    def show_login_screen(self):
        self.clear_widgets()

        title = tk.Label(self.canvas, text="Login to CyberSecure Logger", font=("Helvetica", 26, "bold"), bg="black", fg="#89CFF0")
        title.place(relx=0.5, rely=0.2, anchor="center")

        tk.Label(self.canvas, text="Username", bg="black", fg="white").place(relx=0.4, rely=0.35, anchor="center")
        tk.Label(self.canvas, text="Password", bg="black", fg="white").place(relx=0.4, rely=0.42, anchor="center")

        self.username_entry = tk.Entry(self.canvas)
        self.username_entry.place(relx=0.5, rely=0.35, anchor="center")

        self.password_entry = tk.Entry(self.canvas, show="*")
        self.password_entry.place(relx=0.5, rely=0.42, anchor="center")

        login_btn = tk.Button(self.canvas, text="Login", command=self.login_user, width=20, bg="#1e90ff", fg="white")
        login_btn.place(relx=0.5, rely=0.5, anchor="center")

        back_btn = tk.Button(self.canvas, text="Back", command=self.show_main_menu, width=20, bg="#444", fg="white")
        back_btn.place(relx=0.5, rely=0.56, anchor="center")

    def show_signup_screen(self):
        self.clear_widgets()

        title = tk.Label(self.canvas, text="Sign Up for CyberSecure Logger", font=("Helvetica", 26, "bold"), bg="black", fg="#89CFF0")
        title.place(relx=0.5, rely=0.2, anchor="center")

        tk.Label(self.canvas, text="Username", bg="black", fg="white").place(relx=0.4, rely=0.32, anchor="center")
        tk.Label(self.canvas, text="Email", bg="black", fg="white").place(relx=0.4, rely=0.39, anchor="center")
        tk.Label(self.canvas, text="Password", bg="black", fg="white").place(relx=0.4, rely=0.46, anchor="center")

        self.signup_username = tk.Entry(self.canvas)
        self.signup_email = tk.Entry(self.canvas)
        self.signup_password = tk.Entry(self.canvas, show="*")

        self.signup_username.place(relx=0.5, rely=0.32, anchor="center")
        self.signup_email.place(relx=0.5, rely=0.39, anchor="center")
        self.signup_password.place(relx=0.5, rely=0.46, anchor="center")

        signup_btn = tk.Button(self.canvas, text="Sign Up", command=self.register_user, width=20, bg="#28a745", fg="white")
        signup_btn.place(relx=0.5, rely=0.53, anchor="center")

        back_btn = tk.Button(self.canvas, text="Back to Menu", command=self.show_main_menu, width=20, bg="#444", fg="white")
        back_btn.place(relx=0.5, rely=0.59, anchor="center")

    def register_user(self):
        username = self.signup_username.get().strip()
        email = self.signup_email.get().strip()
        password = self.signup_password.get().strip()

        if not username or not email or not password:
            messagebox.showwarning("Incomplete", "Please fill in all fields")
            return

        conn = sqlite3.connect(USER_DB)
        cursor = conn.cursor()

        try:
            code = generate_user_code(username)
            cursor.execute("INSERT INTO users (username, password, email, code) VALUES (?, ?, ?, ?)", (username, password, email, code))
            conn.commit()
            messagebox.showinfo("Success", f"Account created! Your code is: {code}")
            self.show_login_screen()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")
        finally:
            conn.close()

    def login_user(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        conn = sqlite3.connect(USER_DB)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            messagebox.showinfo("Login", f"Welcome {username}! Your Code: {user[4]}")
            self.root.destroy()
            import main
            main.Keylogger(username, user[4]).run()
        else:
            messagebox.showerror("Login Failed", "Invalid credentials")

    def clear_widgets(self):
        for widget in self.canvas.winfo_children():
            widget.destroy()

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = AuthApp()
    app.run()
