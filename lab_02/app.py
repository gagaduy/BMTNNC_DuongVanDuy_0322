from flask import Flask, render_template, request
# Import tất cả các lớp Cipher từ thư mục gói cipher của bạn
from cipher.caesar import CaesarCipher
from cipher.vigenere import VigenereCipher
from cipher.railfence import RailfenceCipher
from cipher.playfair import PlayfairCipher
from cipher.transposition import TranspositionCipher

app = Flask(__name__)

# ==========================================
# 0. ROUTER TRANG CHỦ (MENU CHÍNH)
# ==========================================
@app.route("/")
def home():
    return render_template('index.html')


# ==========================================
# 1. ROUTER CHO CAESAR CIPHER
# ==========================================
@app.route("/caesar")
def caesar():
    return render_template('caesar.html')

@app.route("/encrypt", methods=['POST'])
def caesar_encrypt():
    text = request.form['inputPlainText']
    key = int(request.form['inputKeyPlain'])
    Caesar = CaesarCipher()
    encrypted_text = Caesar.encrypt(text, key)
    return render_template('caesar.html', origin_plaintext=text, origin_key=key, encrypted_text=encrypted_text)

@app.route("/decrypt", methods=['POST'])
def caesar_decrypt():
    text = request.form['inputCipherText']
    key = int(request.form['inputKeyCipher'])
    Caesar = CaesarCipher()
    decrypted_text = Caesar.decrypt(text, key)
    return render_template('caesar.html', origin_ciphertext=text, origin_key=key, decrypted_text=decrypted_text)


# ==========================================
# 2. ROUTER CHO VIGENERE CIPHER
# ==========================================
@app.route("/vigenere")
def vigenere_page():
    return render_template('vigenere.html')

@app.route("/vigenere/encrypt", methods=['POST'])
def vigenere_encrypt():
    text = request.form['plaintext']
    key = request.form['key']
    cipher = VigenereCipher()
    encrypted_text = cipher.vigenre_encrypt(text, key)
    return render_template('vigenere.html', origin_plaintext=text, origin_key=key, encrypted_text=encrypted_text)

@app.route("/vigenere/decrypt", methods=['POST'])
def vigenere_decrypt():
    text = request.form['ciphertext']
    key = request.form['key']
    cipher = VigenereCipher()
    decrypted_text = cipher.vigenere_decrypt(text, key)
    return render_template('vigenere.html', origin_ciphertext=text, origin_key=key, decrypted_text=decrypted_text)


# ==========================================
# 3. ROUTER CHO RAIL FENCE CIPHER
# ==========================================
@app.route("/railfence")
def railfence_page():
    return render_template('railfence.html')

@app.route("/railfence/encrypt", methods=['POST'])
def railfence_encrypt():
    text = request.form['plaintext']
    key = int(request.form['key'])
    cipher = RailfenceCipher()
    encrypted_text = cipher.encrypt(text, key)
    return render_template('railfence.html', origin_plaintext=text, origin_key=key, encrypted_text=encrypted_text)

@app.route("/railfence/decrypt", methods=['POST'])
def railfence_decrypt():
    text = request.form['ciphertext']
    key = int(request.form['key'])
    cipher = RailfenceCipher()
    decrypted_text = cipher.decrypt(text, key)
    return render_template('railfence.html', origin_ciphertext=text, origin_key=key, decrypted_text=decrypted_text)


# ==========================================
# 4. ROUTER CHO PLAYFAIR CIPHER
# ==========================================
@app.route("/playfair")
def playfair_page():
    return render_template('playfair.html')

@app.route("/playfair/encrypt", methods=['POST'])
def playfair_encrypt_route():
    text = request.form['plaintext']
    key = request.form['key']
    cipher = PlayfairCipher()
    matrix = cipher.create_matrix(key)
    encrypted_text = cipher.playfair_encrypt(text, matrix)
    return render_template('playfair.html', origin_plaintext=text, origin_key=key, encrypted_text=encrypted_text)

@app.route("/playfair/decrypt", methods=['POST'])
def playfair_decrypt_route():
    text = request.form['ciphertext']
    key = request.form['key']
    cipher = PlayfairCipher()
    matrix = cipher.create_matrix(key)
    decrypted_text = cipher.playfair_decrypt(text, matrix)
    return render_template('playfair.html', origin_ciphertext=text, origin_key=key, decrypted_text=decrypted_text)


# ==========================================
# 5. ROUTER CHO TRANSPOSITION CIPHER
# ==========================================
@app.route("/transposition")
def transposition_page():
    return render_template('transposition.html')

@app.route("/transposition/encrypt", methods=['POST'])
def transposition_encrypt_route():
    text = request.form['plaintext']
    key = int(request.form['key'])
    cipher = TranspositionCipher()
    encrypted_text = cipher.encrypt(text, key)
    return render_template('transposition.html', origin_plaintext=text, origin_key=key, encrypted_text=encrypted_text)

@app.route("/transposition/decrypt", methods=['POST'])
def transposition_decrypt_route():
    text = request.form['ciphertext']
    key = int(request.form['key'])
    cipher = TranspositionCipher()
    decrypted_text = cipher.decrypt(text, key)
    return render_template('transposition.html', origin_ciphertext=text, origin_key=key, decrypted_text=decrypted_text)


# ==========================================
# CHẠY ỨNG DỤNG FLASK
# ==========================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)