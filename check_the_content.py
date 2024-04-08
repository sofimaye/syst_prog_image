from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

def encrypt_file(file_path, public_key_path):
    # Завантаження публічного ключа
    with open(public_key_path, "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())

    # Читання вмісту файлу
    with open(file_path, "rb") as f:
        data = f.read()

    # Шифрування даних
    encrypted = public_key.encrypt(
        data,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    # Зберігання зашифрованих даних
    with open(file_path + ".encrypted", "wb") as f:
        f.write(encrypted)
    print("Файл зашифровано.")
