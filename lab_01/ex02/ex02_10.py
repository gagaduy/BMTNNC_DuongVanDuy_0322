def dao_nguoc_chuoi(chuoi):
    return chuoi[::-1]

input_string = input("Nhập chuỗi muốn đảo ngược: ")
print("Chuỗi đảo ngược của", input_string, "là", dao_nguoc_chuoi(input_string))