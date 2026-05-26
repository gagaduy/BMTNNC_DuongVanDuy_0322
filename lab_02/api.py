from flask import Flask, request, jsonify
from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
from cipher.railfence import RailfenceCipher
from cipher.playfair import PlayfairCipher
from cipher.transposition import TranspositionCipher

app = Flask(__name__)
cipher = CaesarCipher()
vigenere_cipher = VigenereCipher()
railfence_cipher = RailfenceCipher()
playfair_cipher = PlayfairCipher()
transposition_cipher = TranspositionCipher()

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

@app.route('/api/railfence/encrypt', methods=['POST'])
def railfence_encrypt():
    data = request.get_json()
    plaintext = data.get('plaintext')
    num_rails = data.get('num_rails')
    if plaintext is None or num_rails is None:
        return jsonify({'error': 'Missing plaintext or num_rails'}), 400
    ciphertext = railfence_cipher.encrypt(plaintext, num_rails)
    return jsonify({'ciphertext': ciphertext})

@app.route('/api/railfence/decrypt', methods=['POST'])
def railfence_decrypt():
    data = request.get_json()
    ciphertext = data.get('ciphertext')
    num_rails = data.get('num_rails')
    if ciphertext is None or num_rails is None:
        return jsonify({'error': 'Missing ciphertext or num_rails'}), 400
    plaintext = railfence_cipher.decrypt(ciphertext, num_rails)
    return jsonify({'plaintext': plaintext})

@app.route('/api/playfair/create_matrix', methods=['POST'])
def playfair_create_matrix():
    data = request.get_json()
    key = data.get('key')
    if key is None:
        return jsonify({'error': 'Missing key'}), 400
    matrix = playfair_cipher.create_matrix(key)
    return jsonify({'matrix': matrix})

@app.route('/api/playfair/encrypt', methods=['POST'])
def playfair_encrypt():
    data = request.get_json()
    plaintext = data.get('plaintext')
    key = data.get('key')
    if plaintext is None or key is None:
        return jsonify({'error': 'Missing plaintext or key'}), 400
    matrix = playfair_cipher.create_matrix(key)
    ciphertext = playfair_cipher.playfair_encrypt(plaintext, matrix)
    return jsonify({'ciphertext': ciphertext})

@app.route('/api/playfair/decrypt', methods=['POST'])
def playfair_decrypt():
    data = request.get_json()
    ciphertext = data.get('ciphertext')
    key = data.get('key')
    if ciphertext is None or key is None:
        return jsonify({'error': 'Missing ciphertext or key'}), 400
    matrix = playfair_cipher.create_matrix(key)
    plaintext = playfair_cipher.playfair_decrypt(ciphertext, matrix)
    return jsonify({'plaintext': plaintext})

@app.route('/api/transposition/encrypt', methods=['POST'])
def transposition_encrypt():
    data = request.get_json()
    plaintext = data.get('plaintext')
    key = data.get('key')
    if plaintext is None or key is None:
        return jsonify({'error': 'Missing plaintext or key'}), 400
    ciphertext = transposition_cipher.encrypt(plaintext, key)
    return jsonify({'ciphertext': ciphertext})

if __name__ == '__main__':
    app.run(host= '0.0.0.0', port=5000, debug=True)