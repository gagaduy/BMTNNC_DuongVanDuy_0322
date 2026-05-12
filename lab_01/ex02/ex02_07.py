print("Nhập dòng văn bản muốn chuyển thành in hoa (Nhập 'done' để kết thúc): ")
lines = []
while True:
    line = input()
    if line.lower() == 'done':
        break
    lines.append(line)
    
print("Các dòng văn bản đã chuyển thành in hoa:")
for line in lines:
    print(line.upper())