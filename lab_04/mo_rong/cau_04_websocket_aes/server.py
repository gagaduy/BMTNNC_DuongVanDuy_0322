import base64

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad
import tornado.ioloop
import tornado.web
import tornado.websocket


AES_KEY = get_random_bytes(16)


def encrypt_message(key, message):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(message.encode("utf-8"), AES.block_size))
    return cipher.iv, ciphertext


class WebSocketAesServer(tornado.websocket.WebSocketHandler):
    def on_message(self, message):
        iv, ciphertext = encrypt_message(AES_KEY, message)
        encrypted_text = base64.b64encode(iv + ciphertext).decode("utf-8")
        self.write_message(encrypted_text)
        if message.lower() == "exit":
            self.close()


def main():
    app = tornado.web.Application([(r"/websocket/", WebSocketAesServer)])
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    main()
