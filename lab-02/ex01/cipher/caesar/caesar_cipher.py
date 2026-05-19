from cipher.caesar import ALPHABET

class CaesarCipher:
    def __init__(self):
        self.alphabet = ALPHABET
        
    def encrypt(self, plaintext, shift):
        ciphertext = ""
        for char in plaintext:
            if char.upper() in self.alphabet:
                index = self.alphabet.index(char.upper())
                shifted_index = (index + shift) % len(self.alphabet)
                ciphertext += self.alphabet[shifted_index]
            else:
                ciphertext += char
        return ciphertext

    def decrypt(self, ciphertext, shift):
        plaintext = ""
        for char in ciphertext:
            if char.upper() in self.alphabet:
                index = self.alphabet.index(char.upper())
                shifted_index = (index - shift) % len(self.alphabet)
                plaintext += self.alphabet[shifted_index]
            else:
                plaintext += char
        return plaintext