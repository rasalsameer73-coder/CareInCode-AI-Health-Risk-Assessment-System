from cryptography.fernet import Fernet
from app.core.config import settings

if not settings.ENCRYPTION_KEY:
    raise ValueError("ENCRYPTION_KEY is not set in environment variables.")

cipher = None

def _get_cipher():
    global cipher
    if cipher is None:
        FERNET_KEY = settings.ENCRYPTION_KEY.encode()
        cipher = Fernet(FERNET_KEY)
    return cipher


def encrypt_data(
    text: str
):
    cipher_obj = _get_cipher()
    encrypted = cipher_obj.encrypt(
        text.encode()
    )

    return encrypted.decode()


def decrypt_data(
    encrypted_text: str
):
    cipher_obj = _get_cipher()
    decrypted = cipher_obj.decrypt(
        encrypted_text.encode()
    )

    return decrypted.decode()