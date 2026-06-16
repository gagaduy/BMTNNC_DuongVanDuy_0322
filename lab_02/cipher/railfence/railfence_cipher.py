class RailfenceCipher:
    def __init__(self):
        pass

    def encrypt(self, plaintext, num_rails):
        rails = [[] for _ in range(num_rails)]
        rail = 0
        direction = 1

        for char in plaintext:
            if char.isalpha():
                rails[rail].append(char)
                rail += direction
                if rail == 0 or rail == num_rails - 1:
                    direction *= -1

        return ''.join(''.join(rail) for rail in rails)

    def decrypt(self, ciphertext, num_rails):
        rail_lengths = [0] * num_rails
        rail = 0
        direction = 1

        for i in range(len(ciphertext)):
            rail_lengths[rail] += 1
            if rail == 0:
                direction = 1
            elif rail == num_rails - 1:
                direction = -1
            rail += direction

        rails = []
        start = 0
        for i in rail_lengths:
            rails.append(list(ciphertext[start:start + i]))
            start += i
        decrypted_text = ''
        rail_index = 0
        direction = 1
        for _ in range(len(ciphertext)):
            decrypted_text += rails[rail_index].pop(0)
            if rail_index == 0:
                direction = 1
            elif rail_index == num_rails - 1:
                direction = -1
            rail_index += direction

        return decrypted_text   