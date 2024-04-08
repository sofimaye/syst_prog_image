from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization

# Генерація приватного ключа
private_key = ec.generate_private_key(ec.SECP384R1())

# Експорт приватного ключа
private_key_bytes = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

# Збереження приватного ключа в файл
with open("private_key.pem", "wb") as f:
    f.write(private_key_bytes)

# Генерація публічного ключа
public_key = private_key.public_key()

# Експорт публічного ключа
public_key_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Збереження публічного ключа в файл
with open("public_key.pem", "wb") as f:
    f.write(public_key_bytes)
