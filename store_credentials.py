import keyring
import getpass
import os
from dotenv import load_dotenv

load_dotenv()
KEYRING_SERVICE = os.getenv("KEYRING_SERVICE")

keyring.set_password(KEYRING_SERVICE, "username", input("Email: "))
keyring.set_password(KEYRING_SERVICE, "password", getpass.getpass("Password: "))

print("Credentials saved securely!")
