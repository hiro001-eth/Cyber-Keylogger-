# ui/user_guide.py

import tkinter as tk
from tkinter import messagebox
import os
from datetime import datetime

CONSENT_LOG_PATH = 'logs/consent.log'

CONSENT_MESSAGE = (
    "This computer is monitored for security and compliance purposes.\n"
    "All keystrokes, clipboard, and application usage may be logged.\n\n"
    "By continuing, you acknowledge and consent to this monitoring.\n"
    "For more information, contact your administrator."
)

HELP_MESSAGE = (
    "CyberKeylogger Professional Edition\n\n"
    "Features:\n"
    "- Keystroke, clipboard, mouse, and screen logging\n"
    "- Script and anomaly detection\n"
    "- Privacy and compliance by design\n\n"
    "For support, contact your IT administrator."
)

def log_consent(user=None):
    os.makedirs(os.path.dirname(CONSENT_LOG_PATH), exist_ok=True)
    with open(CONSENT_LOG_PATH, 'a', encoding='utf-8') as f:
        f.write(f"{datetime.utcnow().isoformat()} | user: {user or 'unknown'} | consent: accepted\n")

def show_consent_dialog(user=None):
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("Monitoring Consent", CONSENT_MESSAGE)
    log_consent(user)
    root.destroy()

def show_help_dialog():
    root = tk.Tk()
    root.withdraw()
    messagebox.showinfo("About CyberKeylogger", HELP_MESSAGE)
    root.destroy()

if __name__ == "__main__":
    show_consent_dialog(user="testuser")
    show_help_dialog()
