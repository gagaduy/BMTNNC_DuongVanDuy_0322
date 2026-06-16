import threading

import tornado.ioloop
import tornado.websocket


class WebSocketAesClient:
    def __init__(self, io_loop):
        self.io_loop = io_loop
        self.connection = None
        self.closing = False

    def start(self):
        tornado.websocket.websocket_connect(
            url="ws://localhost:8888/websocket/",
            callback=self.on_connect,
            on_message_callback=self.on_message,
        )

    def on_connect(self, future):
        try:
            self.connection = future.result()
            print("Da ket noi toi server WebSocket AES")
            threading.Thread(target=self.read_input, daemon=True).start()
        except Exception as exc:
            print(f"Khong the ket noi: {exc}")
            self.io_loop.stop()

    def read_input(self):
        while True:
            message = input("Nhap thong diep gui server: ")
            self.io_loop.add_callback(self.send_message, message)
            if message.lower() == "exit":
                self.closing = True
                break

    def send_message(self, message):
        if self.connection is not None:
            self.connection.write_message(message)

    def on_message(self, message):
        if message is None:
            print("Server da dong ket noi")
            self.io_loop.stop()
            return

        print("Ciphertext:", message)
        print("-" * 40)
        if self.closing:
            self.connection.close()
            self.io_loop.stop()


def main():
    io_loop = tornado.ioloop.IOLoop.current()
    client = WebSocketAesClient(io_loop)
    io_loop.add_callback(client.start)
    io_loop.start()


if __name__ == "__main__":
    main()
