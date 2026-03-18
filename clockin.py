import tkinter as tk
import threading
import keyring
import os
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

load_dotenv()
SITE_URL        = os.getenv("URL")
KEYRING_SERVICE = os.getenv("KEYRING_SERVICE")
EMAIL_FIELD     = os.getenv("EMAIL_FIELD")
PASSWORD_FIELD  = os.getenv("PASSWORD_FIELD")
LOGIN_BUTTON    = os.getenv("LOGIN_BUTTON")
TYPE_INPUT      = os.getenv("TYPE_INPUT")
REGISTER_BUTTON = os.getenv("REGISTER_BUTTON")


def register_time():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(SITE_URL)

        type_input = page.locator(TYPE_INPUT)

        if not type_input.is_visible():
            username = keyring.get_password(KEYRING_SERVICE, "username")
            password = keyring.get_password(KEYRING_SERVICE, "password")
            page.fill(EMAIL_FIELD, username)
            page.fill(PASSWORD_FIELD, password)
            page.click(LOGIN_BUTTON)
            page.wait_for_load_state("networkidle")

        type_input = page.locator(TYPE_INPUT)
        type_input.triple_click()
        type_input.fill("In")
        page.keyboard.press("Enter")
        page.wait_for_timeout(500)

        page.click(REGISTER_BUTTON)
        page.wait_for_load_state("networkidle")

        browser.close()


def on_clock_in():
    btn_clockin.config(state="disabled")
    btn_dismiss.config(state="disabled")
    label.config(text="Clocking in...")
    threading.Thread(target=run_and_close, daemon=True).start()


def run_and_close():
    register_time()
    root.after(0, root.destroy)


root = tk.Tk()
root.overrideredirect(True)
root.attributes("-topmost", True)
root.attributes("-alpha", 0.95)
root.configure(bg="#1e1e2e")

popup_w, popup_h = 260, 90
x = root.winfo_screenwidth() - popup_w - 20
y = root.winfo_screenheight() - popup_h - 60
root.geometry(f"{popup_w}x{popup_h}+{x}+{y}")

label = tk.Label(root, text="Ready to clock in?", fg="#cdd6f4", bg="#1e1e2e",
                 font=("Segoe UI", 11, "bold"))
label.pack(anchor="w", padx=16, pady=(12, 6))

btn_frame = tk.Frame(root, bg="#1e1e2e")
btn_frame.pack(anchor="w", padx=16)

btn_clockin = tk.Button(btn_frame, text="Clock in", command=on_clock_in,
                        bg="#89b4fa", fg="#1e1e2e", bd=0, padx=10, pady=4,
                        font=("Segoe UI", 9, "bold"), cursor="hand2")
btn_clockin.pack(side="left")

btn_dismiss = tk.Button(btn_frame, text="Dismiss", command=root.destroy,
                        bg="#313244", fg="#cdd6f4", bd=0, padx=10, pady=4,
                        font=("Segoe UI", 9), cursor="hand2")
btn_dismiss.pack(side="left", padx=(8, 0))

root.mainloop()
