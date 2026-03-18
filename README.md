# clock-in

A startup automation script for clocking in to a web-hosted time registration system.

On login, it shows a **"Clocking in!"** toast notification while Playwright runs headlessly in the background to log in and register your time. The toast closes automatically when done.

---

## Dependencies

```
pip install playwright keyring python-dotenv
playwright install chromium
```

---

## Configuration

All sensitive configuration lives in a `.env` file in the project root. This file is **not checked in** — you must create it yourself.

Create a `.env` file with the following keys:

```env
URL=<login page URL>
KEYRING_SERVICE=<a name for storing credentials, e.g. "work-timer">

EMAIL_FIELD=<CSS selector for the email input>
PASSWORD_FIELD=<CSS selector for the password input>
LOGIN_BUTTON=<CSS selector for the login button>
TYPE_INPUT=<CSS selector for the registration type dropdown>
REGISTER_BUTTON=<CSS selector for the register button>
```

---

## Store credentials

Run `store_credentials.py` once to securely save your username and password to Windows Credential Manager:

```
python store_credentials.py
```

You will be prompted to enter your email and password interactively — nothing is written to disk. Delete the file when done.

To verify saved credentials, open a Python terminal and run:

```python
import keyring
print(keyring.get_password("your-keyring-service", "username"))
print(keyring.get_password("your-keyring-service", "password"))
```

To update credentials, simply run `store_credentials.py` again.

---

## Usage

```
python clockin.py
```

---

## Package as .exe

```
pyinstaller --onefile --noconsole clockin.py
```

Output: `dist\clockin.exe`

---

## Run on Windows startup

### Option A — Startup Folder
1. Press **Win + R**, type `shell:startup`, press Enter
2. Paste a shortcut to `dist\clockin.exe` into that folder

### Option B — Registry
1. Press **Win + R**, type `regedit`, press Enter
2. Navigate to `HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run`
3. Right-click → **New → String Value**
4. Name: `TimeRegistration`
5. Value: full path to `clockin.exe`

---

## Security notes

- Credentials are stored in **Windows Credential Manager** via `keyring` — never on disk
- The `.env` file is gitignored — never check it in
- No sensitive data (URL, selectors, credentials) is present in the checked-in code
