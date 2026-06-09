import queue
import socket
import threading
import tkinter as tk
from tkinter import messagebox, scrolledtext

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


def encrypt_message(key, message):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(message.encode(), AES.block_size))
    return cipher.iv + ciphertext


def decrypt_message(key, encrypted_message):
    iv = encrypted_message[:AES.block_size]
    ciphertext = encrypted_message[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    decrypted_message = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return decrypted_message.decode()


class ServerThread(threading.Thread):
    def __init__(self, log_queue):
        super().__init__(daemon=True)
        self.log_queue = log_queue
        self.server_key = RSA.generate(2048)
        self.clients = []
        self.running = False
        self.server_socket = None

    def log(self, message):
        self.log_queue.put(message)

    def stop(self):
        self.running = False
        if self.server_socket:
            try:
                self.server_socket.close()
            except OSError:
                pass
        for client_socket, _ in list(self.clients):
            try:
                client_socket.close()
            except OSError:
                pass

    def run(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(("localhost", 12345))
        self.server_socket.listen(5)
        self.server_socket.settimeout(1)
        self.running = True
        self.log("Server da khoi dong tai localhost:12345")

        while self.running:
            try:
                client_socket, client_address = self.server_socket.accept()
            except socket.timeout:
                continue
            except OSError:
                break
            threading.Thread(
                target=self.handle_client,
                args=(client_socket, client_address),
                daemon=True,
            ).start()

        self.log("Server da dung")

    def handle_client(self, client_socket, client_address):
        aes_key = None
        try:
            self.log(f"Ket noi tu {client_address}")
            client_socket.send(self.server_key.publickey().export_key(format="PEM"))
            client_received_key = RSA.import_key(client_socket.recv(2048))

            aes_key = get_random_bytes(16)
            cipher_rsa = PKCS1_OAEP.new(client_received_key)
            encrypted_aes_key = cipher_rsa.encrypt(aes_key)
            client_socket.send(encrypted_aes_key)

            self.clients.append((client_socket, aes_key))

            while self.running:
                encrypted_message = client_socket.recv(1024)
                if not encrypted_message:
                    break
                decrypted_message = decrypt_message(aes_key, encrypted_message)
                self.log(f"Nhan tu {client_address}: {decrypted_message}")

                for client, key in list(self.clients):
                    if client != client_socket:
                        try:
                            encrypted = encrypt_message(key, decrypted_message)
                            client.send(encrypted)
                        except OSError:
                            pass

                if decrypted_message == "exit":
                    break
        except Exception as exc:
            self.log(f"Loi server: {exc}")
        finally:
            if aes_key is not None:
                entry = (client_socket, aes_key)
                if entry in self.clients:
                    self.clients.remove(entry)
            try:
                client_socket.close()
            except OSError:
                pass
            self.log(f"Da dong ket noi {client_address}")


class ClientThread(threading.Thread):
    def __init__(self, log_queue):
        super().__init__(daemon=True)
        self.log_queue = log_queue
        self.client_socket = None
        self.client_key = None
        self.aes_key = None
        self.running = False

    def log(self, message):
        self.log_queue.put(message)

    def connect(self):
        if self.running:
            return
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(("localhost", 12345))
        self.client_key = RSA.generate(2048)

        server_public_key = RSA.import_key(self.client_socket.recv(2048))
        self.client_socket.send(self.client_key.publickey().export_key(format="PEM"))

        encrypted_aes_key = self.client_socket.recv(2048)
        cipher_rsa = PKCS1_OAEP.new(self.client_key)
        self.aes_key = cipher_rsa.decrypt(encrypted_aes_key)
        self.running = True
        self.start()
        self.log("Client da ket noi server")

    def send_message(self, message):
        if not self.running or not self.aes_key:
            raise ConnectionError("Client chua ket noi")
        encrypted_message = encrypt_message(self.aes_key, message)
        self.client_socket.send(encrypted_message)
        self.log(f"Da gui: {message}")
        if message == "exit":
            self.close()

    def close(self):
        self.running = False
        if self.client_socket:
            try:
                self.client_socket.close()
            except OSError:
                pass

    def run(self):
        while self.running:
            try:
                encrypted_message = self.client_socket.recv(1024)
                if not encrypted_message:
                    break
                decrypted_message = decrypt_message(self.aes_key, encrypted_message)
                self.log(f"Nhan duoc: {decrypted_message}")
            except OSError:
                break
            except Exception as exc:
                self.log(f"Loi client: {exc}")
                break
        self.running = False
        self.log("Client da ngat ket noi")


class AesRsaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mo rong C01 - UI Bai 01")
        self.log_queue = queue.Queue()
        self.server_thread = None
        self.client_thread = None

        self.log_area = scrolledtext.ScrolledText(root, width=80, height=20, state="disabled")
        self.log_area.pack(padx=10, pady=10)

        controls = tk.Frame(root)
        controls.pack(fill="x", padx=10)

        tk.Button(controls, text="Khoi dong Server", command=self.start_server).pack(side="left", padx=5)
        tk.Button(controls, text="Ket noi Client", command=self.connect_client).pack(side="left", padx=5)

        self.message_entry = tk.Entry(root, width=60)
        self.message_entry.pack(padx=10, pady=10, fill="x")

        tk.Button(root, text="Gui thong diep", command=self.send_message).pack(pady=(0, 10))

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)
        self.root.after(100, self.process_logs)

    def append_log(self, message):
        self.log_area.configure(state="normal")
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)
        self.log_area.configure(state="disabled")

    def process_logs(self):
        while not self.log_queue.empty():
            self.append_log(self.log_queue.get())
        self.root.after(100, self.process_logs)

    def start_server(self):
        if self.server_thread and self.server_thread.running:
            messagebox.showinfo("Thong bao", "Server dang chay")
            return
        self.server_thread = ServerThread(self.log_queue)
        self.server_thread.start()

    def connect_client(self):
        if self.client_thread and self.client_thread.running:
            messagebox.showinfo("Thong bao", "Client da ket noi")
            return
        self.client_thread = ClientThread(self.log_queue)
        try:
            self.client_thread.connect()
        except Exception as exc:
            messagebox.showerror("Loi", str(exc))

    def send_message(self):
        message = self.message_entry.get().strip()
        if not message:
            return
        if not self.client_thread or not self.client_thread.running:
            messagebox.showerror("Loi", "Client chua ket noi")
            return
        try:
            self.client_thread.send_message(message)
            self.message_entry.delete(0, tk.END)
        except Exception as exc:
            messagebox.showerror("Loi", str(exc))

    def on_close(self):
        if self.client_thread:
            self.client_thread.close()
        if self.server_thread:
            self.server_thread.stop()
        self.root.destroy()


def main():
    root = tk.Tk()
    app = AesRsaApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
