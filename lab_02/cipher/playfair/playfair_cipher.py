class PlayfairCipher:
    def __init__(self) -> None:
        pass
    
    def create_matrix(self, key):
        # 1. Chuẩn hóa key: Viết hoa, chuyển J thành I, lọc bỏ ký tự không phải chữ cái
        key = key.upper().replace("J", "I")
        clean_key = [c for c in key if c.isalpha()]
        
        # 2. Loại bỏ các ký tự trùng lặp trong key nhưng vẫn giữ nguyên thứ tự xuất hiện
        seen = set()
        matrix_letters = []
        for char in clean_key:
            if char not in seen:
                seen.add(char)
                matrix_letters.append(char)
        
        # 3. Điền các chữ cái còn lại trong bảng chữ cái (loại bỏ J) vào ma trận
        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"
        for char in alphabet:
            if char not in seen:
                seen.add(char)
                matrix_letters.append(char)
                
        # 4. Chuyển mảng phẳng 25 phần tử thành ma trận 5x5 (Đặt ngoài vòng lặp)
        playfair_matrix = [matrix_letters[i:i+5] for i in range(0, 25, 5)]
        return playfair_matrix
    
    def find_letter_coords(self, matrix, letter):
        for i in range(5):
            for j in range(5):
                if matrix[i][j] == letter:
                    return (i, j)
        return None
    
    def playfair_encrypt(self, plaintext, matrix):
        # Chuẩn hóa plaintext: chỉ giữ lại chữ cái và xử lý J -> I
        plaintext = plaintext.upper().replace("J", "I")
        plaintext = [c for c in plaintext if c.isalpha()]
        
        ciphertext = ""
        i = 0
        
        while i < len(plaintext):
            letter1 = plaintext[i]
            
            # Xử lý cặp ký tự trùng nhau hoặc ký tự cuối cùng bị lẻ
            if i + 1 < len(plaintext):
                letter2 = plaintext[i + 1]
                if letter1 == letter2:
                    letter2 = 'X'
                    i += 1  # Chỉ tiến 1 bước vì letter2 thực chất là ký tự chèn thêm 'X'
                else:
                    i += 2  # Tiến 2 bước bình thường
            else:
                letter2 = 'X'
                i += 1
            
            coords1 = self.find_letter_coords(matrix, letter1)
            coords2 = self.find_letter_coords(matrix, letter2)
            
            if coords1 and coords2:
                if coords1[0] == coords2[0]:  # Cùng hàng
                    ciphertext += matrix[coords1[0]][(coords1[1] + 1) % 5]
                    ciphertext += matrix[coords2[0]][(coords2[1] + 1) % 5]
                elif coords1[1] == coords2[1]:  # Cùng cột
                    ciphertext += matrix[(coords1[0] + 1) % 5][coords1[1]]
                    ciphertext += matrix[(coords2[0] + 1) % 5][coords2[1]]
                else:  # Tạo thành hình chữ nhật
                    ciphertext += matrix[coords1[0]][coords2[1]]
                    ciphertext += matrix[coords2[0]][coords1[1]]
        
        return ciphertext
    
    def playfair_decrypt(self, ciphertext, matrix):
        ciphertext = ciphertext.upper().replace("J", "I")
        ciphertext = [c for c in ciphertext if c.isalpha()]
        
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
                if coords1[0] == coords2[0]:  # Cùng hàng
                    plaintext += matrix[coords1[0]][(coords1[1] - 1) % 5]
                    plaintext += matrix[coords2[0]][(coords2[1] - 1) % 5]
                elif coords1[1] == coords2[1]:  # Cùng cột
                    plaintext += matrix[(coords1[0] - 1) % 5][coords1[1]]
                    plaintext += matrix[(coords2[0] - 1) % 5][coords2[1]]
                else:  # Tạo thành hình chữ nhật
                    plaintext += matrix[coords1[0]][coords2[1]]
                    plaintext += matrix[coords2[0]][coords1[1]]
            
            i += 2
        
        return plaintext