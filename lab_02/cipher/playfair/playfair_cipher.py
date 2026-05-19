class PlayfairCipher:
    def __init__(self) -> None:
        pass
    
    def __init__(self):
        pass
    
    def create_matrix(self, key):
        key = key.replace("J", "I")
        key = key.upper()
        key_set = set(key)
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        remaining_letters = [c for c in alphabet if c not in key_set]
        matrix = list(key)
        
        for letter in remaining_letters:
            matrix.append(letter)
            if len(matrix) == 25:
                break
            playfair_matrix = [matrix[i:i+5] for i in range(0, 25, 5)]
        return playfair_matrix
    
    def find_letter_coords(self, matrix, letter):
        for i in range(5):
            for j in range(5):
                if matrix[i][j] == letter:
                    return (i, j)
        return None
    
    def playfair_encrypt(self, plaintext, matrix):
        plaintext = plaintext.replace("J", "I")
        plaintext = plaintext.upper()
        ciphertext = ""
        i = 0
        
        while i < len(plaintext):
            letter1 = plaintext[i]
            if i + 1 < len(plaintext):
                letter2 = plaintext[i + 1]
            else:
                letter2 = 'X'
            
            if letter1 == letter2:
                letter2 = 'X'
                i += 1
            else:
                i += 2
            
            coords1 = self.find_letter_coords(matrix, letter1)
            coords2 = self.find_letter_coords(matrix, letter2)
            
            if coords1 and coords2:
                if coords1[0] == coords2[0]:  # Same row
                    ciphertext += matrix[coords1[0]][(coords1[1] + 1) % 5]
                    ciphertext += matrix[coords2[0]][(coords2[1] + 1) % 5]
                elif coords1[1] == coords2[1]:  # Same column
                    ciphertext += matrix[(coords1[0] + 1) % 5][coords1[1]]
                    ciphertext += matrix[(coords2[0] + 1) % 5][coords2[1]]
                else:  # Rectangle
                    ciphertext += matrix[coords1[0]][coords2[1]]
                    ciphertext += matrix[coords2[0]][coords1[1]]
        
        return ciphertext
    
    def playfair_decrypt(self, ciphertext, matrix):
        ciphertext = ciphertext.replace("J", "I")
        ciphertext = ciphertext.upper()
        plaintext = ""
        i = 0
        
        while i < len(ciphertext):
            letter1 = ciphertext[i]
            if i + 1 < len(ciphertext):
                letter2 = ciphertext[i + 1]
            else:
                letter2 = 'X'
            
            coords1 = self.find_letter_coords(matrix, letter1)
            coords2 = self.find_letter_coords(matrix, letter2)
            
            if coords1 and coords2:
                if coords1[0] == coords2[0]:  # Same row
                    plaintext += matrix[coords1[0]][(coords1[1] - 1) % 5]
                    plaintext += matrix[coords2[0]][(coords2[1] - 1) % 5]
                elif coords1[1] == coords2[1]:  # Same column
                    plaintext += matrix[(coords1[0] - 1) % 5][coords1[1]]
                    plaintext += matrix[(coords2[0] - 1) % 5][coords2[1]]
                else:  # Rectangle
                    plaintext += matrix[coords1[0]][coords2[1]]
                    plaintext += matrix[coords2[0]][coords1[1]]
            
            i += 2
        
        return plaintext