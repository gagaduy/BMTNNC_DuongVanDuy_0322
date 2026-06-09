import hashlib
import tkinter as tk
from tkinter import messagebox, scrolledtext

from Crypto.Hash import SHA3_256


def left_rotate(value, shift):
    return ((value << shift) | (value >> (32 - shift))) & 0xFFFFFFFF


def md5_manual(message):
    a = 0x67452301
    b = 0xEFCDAB89
    c = 0x98BADCFE
    d = 0x10325476

    original_length = len(message)
    message += b"\x80"
    while len(message) % 64 != 56:
        message += b"\x00"
    message += original_length.to_bytes(8, "little")

    for i in range(0, len(message), 64):
        block = message[i:i + 64]
        words = [int.from_bytes(block[j:j + 4], "little") for j in range(0, 64, 4)]
        a0, b0, c0, d0 = a, b, c, d

        for j in range(64):
            if j < 16:
                f = (b & c) | ((~b) & d)
                g = j
            elif j < 32:
                f = (d & b) | ((~d) & c)
                g = (5 * j + 1) % 16
            elif j < 48:
                f = b ^ c ^ d
                g = (3 * j + 5) % 16
            else:
                f = c ^ (b | (~d))
                g = (7 * j) % 16

            temp = d
            d = c
            c = b
            b = b + left_rotate((a + f + 0x5A827999 + words[g]) & 0xFFFFFFFF, 3)
            a = temp

        a = (a + a0) & 0xFFFFFFFF
        b = (b + b0) & 0xFFFFFFFF
        c = (c + c0) & 0xFFFFFFFF
        d = (d + d0) & 0xFFFFFFFF

    return "{:08x}{:08x}{:08x}{:08x}".format(a, b, c, d)


def calculate_md5(text):
    md5_hash = hashlib.md5()
    md5_hash.update(text.encode("utf-8"))
    return md5_hash.hexdigest()


def calculate_sha256(text):
    sha256_hash = hashlib.sha256()
    sha256_hash.update(text.encode("utf-8"))
    return sha256_hash.hexdigest()


def calculate_sha3(text):
    sha3_hash = SHA3_256.new()
    sha3_hash.update(text.encode("utf-8"))
    return sha3_hash.hexdigest()


def calculate_blake2(text):
    blake2_hash = hashlib.blake2b(digest_size=64)
    blake2_hash.update(text.encode("utf-8"))
    return blake2_hash.hexdigest()


class HashApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mo rong C03 - UI Bai 03")

        tk.Label(root, text="Nhap chuoi can bam:").pack(pady=(10, 4))
        self.input_entry = tk.Entry(root, width=80)
        self.input_entry.pack(padx=10, fill="x")

        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="MD5 Tu Cai Dat", command=self.run_md5_manual).pack(side="left", padx=4)
        tk.Button(button_frame, text="MD5 Thu Vien", command=self.run_md5_library).pack(side="left", padx=4)
        tk.Button(button_frame, text="SHA-256", command=self.run_sha256).pack(side="left", padx=4)
        tk.Button(button_frame, text="SHA-3", command=self.run_sha3).pack(side="left", padx=4)
        tk.Button(button_frame, text="BLAKE2", command=self.run_blake2).pack(side="left", padx=4)

        self.output = scrolledtext.ScrolledText(root, width=95, height=18)
        self.output.pack(padx=10, pady=(0, 10))

    def get_input(self):
        text = self.input_entry.get()
        if not text:
            messagebox.showerror("Loi", "Hay nhap chuoi can bam")
            return None
        return text

    def show_result(self, title, value):
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, f"{title}:\n{value}")

    def run_md5_manual(self):
        text = self.get_input()
        if text is not None:
            self.show_result("MD5 Tu Cai Dat", md5_manual(text.encode("utf-8")))

    def run_md5_library(self):
        text = self.get_input()
        if text is not None:
            self.show_result("MD5 Thu Vien", calculate_md5(text))

    def run_sha256(self):
        text = self.get_input()
        if text is not None:
            self.show_result("SHA-256", calculate_sha256(text))

    def run_sha3(self):
        text = self.get_input()
        if text is not None:
            self.show_result("SHA-3", calculate_sha3(text))

    def run_blake2(self):
        text = self.get_input()
        if text is not None:
            self.show_result("BLAKE2", calculate_blake2(text))


def main():
    root = tk.Tk()
    app = HashApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
