from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec


def sign_file(file_path, private_key_path):
    # Завантаження приватного ключа
    with open(private_key_path, "rb") as f:
        private_key = serialization.load_pem_private_key(
            f.read(),
            password=None,
        )

    # Читання вмісту файлу
    with open(file_path, "rb") as f:
        data = f.read()

    # Генерація підпису
    signature = private_key.sign(
        data,
        ec.ECDSA(hashes.SHA256())
    )

    # Збереження підпису в файл
    with open(file_path + ".sig", "wb") as f:
        f.write(signature)

    print("Файл успішно підписано.")

# Виклик функції sign_file з вашим файлом та приватним ключем
sign_file("ukr.txt", "private_key.pem")
