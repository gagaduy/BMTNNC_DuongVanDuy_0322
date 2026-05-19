from flask import Flask, request, jsonify
from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
app = Flask(__name__)
cipher = CaesarCipher()
vigenere_cipher = VigenereCipher()

@app.route('/api/caesar/encrypt', methods=['POST'])
def encrypt():
    data = request.get_json()
    plaintext = data.get('plaintext')
    shift = data.get('shift')
    if plaintext is None or shift is None:
        return jsonify({'error': 'Missing plaintext or shift'}), 400
    ciphertext = cipher.encrypt(plaintext, shift)
    return jsonify({'ciphertext': ciphertext})

@app.route('/api/caesar/decrypt', methods=['POST'])
def decrypt():
    data = request.get_json()
    ciphertext = data.get('ciphertext')
    shift = data.get('shift')
    if ciphertext is None or shift is None:
        return jsonify({'error': 'Missing ciphertext or shift'}), 400
    plaintext = cipher.decrypt(ciphertext, shift)
    return jsonify({'plaintext': plaintext})

@app.route('/api/vigenere/encrypt', methods=['POST'])
def vigenere_encrypt():
    data = request.get_json()
    plaintext = data.get('plaintext')
    key = data.get('key')
    if plaintext is None or key is None:
        return jsonify({'error': 'Missing plaintext or key'}), 400
    ciphertext = vigenere_cipher.vigenre_encrypt(plaintext, key)
    return jsonify({'ciphertext': ciphertext})

@app.route('/api/vigenere/decrypt', methods=['POST'])
def vigenere_decrypt():
    data = request.get_json()
    ciphertext = data.get('ciphertext')
    key = data.get('key')
    if ciphertext is None or key is None:
        return jsonify({'error': 'Missing ciphertext or key'}), 400
    plaintext = vigenere_cipher.vigenere_decrypt(ciphertext, key)
    return jsonify({'plaintext': plaintext})

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=5000, debug=True)