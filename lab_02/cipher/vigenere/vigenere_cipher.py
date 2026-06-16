class VigenereCipher:
    def __init__(self):
        pass

    def vigenre_encrypt(self, plaintext, key):
        ciphertext = ""
        key_index = 0
        for i, char in enumerate(plaintext):
            if char.isalpha():
                shift = ord(key[key_index % len(key)].lower()) - ord('a')
                if char.islower():
                    encrypted_char = chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
                else:
                    encrypted_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
                ciphertext += encrypted_char
                key_index += 1
            else:
                ciphertext += char
        return ciphertext

    def vigenere_decrypt(self, ciphertext, key):
        plaintext = ""
        key_index = 0
        for i, char in enumerate(ciphertext):
            if char.isalpha():
                shift = ord(key[key_index % len(key)].lower()) - ord('a')
                if char.islower():
                    decrypted_char = chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
                else:
                    decrypted_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
                plaintext += decrypted_char
                key_index += 1
            else:
                plaintext += char
        return plaintext