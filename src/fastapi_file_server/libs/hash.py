from cryptography.fernet import Fernet

from fastapi_file_server.config import get_config


config = get_config()

PASSWORD_SECRET_KEY = config.password_secret_key
pass_encrypter = Fernet(PASSWORD_SECRET_KEY)


def get_password_hash(password : str) -> str:
    hashed_password = pass_encrypter.encrypt(password.encode())
    return hashed_password.decode()


def verify_password(plain_password : str, hashed_password : str) -> bool:
    hashed_password = hashed_password.encode()
    decrypt_password = pass_encrypter.decrypt(hashed_password)
    return plain_password == decrypt_password.decode()