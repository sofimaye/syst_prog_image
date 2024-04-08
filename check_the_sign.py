from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec


def verify_signature(file_path, signature_path, public_key_path):
    # Завантаження публічного ключа
    with open(public_key_path, "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())

    # Читання вмісту файлу
    with open(file_path, "rb") as f:
        data = f.read()

    # Читання підпису
    with open(signature_path, "rb") as f:
        signature = f.read()

    # Спроба верифікації підпису
    try:
        public_key.verify(
            signature,
            data,
            ec.ECDSA(hashes.SHA256())
        )
        print("Підпис вірний.")
    except InvalidSignature:
        print("Підпис невірний.")
# Шлях до файлу, який було підписано
file_path = "ukr.txt"

# Шлях до файлу підпису
signature_path = "ukr.txt.sig"

# Шлях до публічного ключа
public_key_path = "public_key.pem"

# Виклик функції для перевірки підпису
verify_signature(file_path, signature_path, public_key_path)
