import math

class TranspositionCipher:
    def __init__(self):
        pass

    def get_key_order(self, key: str) -> list:
        key_list = list(key.upper())
        indexed_key = [(key_list[i], i) for i in range(len(key_list))]
        sorted_key = sorted(indexed_key, key=lambda x: x[0])
        order = [0] * len(key)
        
        for rank, (char, original_index) in enumerate(sorted_key):
            order[original_index] = rank
        return order

    def encrypt(self, plaintext: str, key: str) -> str:
        plaintext = "".join(plaintext.upper().split())
        key = key.upper()
        
        key_len = len(key)
        msg_len = len(plaintext)
        
        row_count = math.ceil(msg_len / key_len)
        
        padding_len = (row_count * key_len) - msg_len
        plaintext += 'X' * padding_len
        
        grid = [plaintext[i:i+key_len] for i in range(0, len(plaintext), key_len)]
        
        key_order = self.get_key_order(key)
        
        ciphertext = ""
        for i in range(key_len):
            col_index = key_order.index(i)
            for row in grid:
                ciphertext += row[col_index]
                
        return ciphertext

    def decrypt(self, ciphertext: str, key: str) -> str:
        key = key.upper()
        key_len = len(key)
        cipher_len = len(ciphertext)
        
        row_count = math.ceil(cipher_len / key_len)
        
        grid = [['' for _ in range(key_len)] for _ in range(row_count)]
        
        key_order = self.get_key_order(key)
        
        char_idx = 0
        for i in range(key_len):
            col_index = key_order.index(i)
            for r in range(row_count):
                if char_idx < cipher_len:
                    grid[r][col_index] = ciphertext[char_idx]
                    char_idx += 1
                    
        plaintext = ""
        for r in range(row_count):
            plaintext += "".join(grid[r])
            
        return plaintext
