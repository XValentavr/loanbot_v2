from werkzeug.security import generate_password_hash, check_password_hash


class Encryptor:
    @staticmethod
    def generate_encrypted_password(characters: str):
        return generate_password_hash(str(characters))

    @staticmethod
    def compare_password(encrypted, decrypted):
        return check_password_hash(encrypted, str(decrypted))


encryptor = Encryptor()
