import base64
import tkinter as tk
from tkinter import messagebox, scrolledtext

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import dh


def generate_dh_parameters():
    return dh.generate_parameters(generator=2, key_size=2048)


def generate_server_key_pair(parameters):
    private_key = parameters.generate_private_key()
    public_key = private_key.public_key()
    return private_key, public_key


def generate_client_key_pair(parameters):
    private_key = parameters.generate_private_key()
    public_key = private_key.public_key()
    return private_key, public_key


class DhKeyPairApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mo rong C02 - UI Bai 02")
        self.parameters = None
        self.server_private_key = None
        self.server_public_key = None
        self.client_private_key = None
        self.client_public_key = None

        tk.Button(root, text="Tao khoa Server", command=self.create_server_key).pack(pady=8)
        tk.Button(root, text="Tao khoa Client va Shared Secret", command=self.create_client_key).pack(pady=8)

        self.output = scrolledtext.ScrolledText(root, width=90, height=24)
        self.output.pack(padx=10, pady=10)

    def write_output(self, message):
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, message)

    def create_server_key(self):
        self.parameters = generate_dh_parameters()
        self.server_private_key, self.server_public_key = generate_server_key_pair(self.parameters)

        pem_data = self.server_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode("utf-8")
        self.write_output("Server Public Key:\n" + pem_data)

    def create_client_key(self):
        if self.server_public_key is None:
            messagebox.showerror("Loi", "Hay tao khoa server truoc")
            return

        parameters = self.server_public_key.parameters()
        self.client_private_key, self.client_public_key = generate_client_key_pair(parameters)
        shared_secret = self.client_private_key.exchange(self.server_public_key)

        client_pem = self.client_public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        ).decode("utf-8")
        shared_secret_text = base64.b16encode(shared_secret).decode("utf-8")

        result = (
            "Client Public Key:\n"
            + client_pem
            + "\nShared Secret:\n"
            + shared_secret_text
        )
        self.write_output(result)


def main():
    root = tk.Tk()
    app = DhKeyPairApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
