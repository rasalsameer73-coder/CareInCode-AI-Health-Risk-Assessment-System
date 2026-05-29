from cryptography.fernet import Fernet
from app.core.config import settings

if not settings.ENCRYPTION_KEY:
    raise ValueError("ENCRYPTION_KEY is not set in environment variables.")

FERNET_KEY = settings.ENCRYPTION_KEY.encode()
cipher = Fernet(FERNET_KEY)


def encrypt_data(
    text: str
):

    encrypted = cipher.encrypt(
        text.encode()
    )

    return encrypted.decode()


def decrypt_data(
    encrypted_text: str
):

    decrypted = cipher.decrypt(
        encrypted_text.encode()
    )

    return decrypted.decode()