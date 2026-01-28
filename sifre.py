import random
import hashlib
import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# -------------------------------------------------
# ROOT ROUTE (404 SORUNUNU ÇÖZER)
# -------------------------------------------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "ok",
        "message": "Şifreleme API çalışıyor 🚀",
        "endpoint": "/sifrele (POST)"
    })


# -------------------------------------------------
# ŞİFRELE / ÇÖZ ENDPOINT
# -------------------------------------------------
@app.route("/sifrele", methods=["POST"])
def sifrele():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "JSON body gerekli"}), 400

    if not all(k in data for k in ("metin", "anahtar", "option")):
        return jsonify({"error": "metin, anahtar ve option zorunlu"}), 400

    metin = data["metin"]
    anahtar = data["anahtar"]
    option = data["option"]

    if option not in ("sifrele", "coz"):
        return jsonify({"error": "option 'sifrele' veya 'coz' olmalı"}), 400

    # ASCII 32–126
    harfler = [chr(i) for i in range(32, 127)]

    # Anahtar oluşturma
    try:
        key = int(anahtar)
    except:
        h = hashlib.sha256(str(anahtar).encode()).digest()
        key = int.from_bytes(h[:8], "big", signed=True)

    random.seed(key)

    karisikHarfler = harfler.copy()
    random.shuffle(karisikHarfler)

    sonuc = ""
    run = 0

    if option == "sifrele":
        for harf in metin:
            if harf not in harfler:
                sonuc += harf
                continue

            run += 1
            sonuc += karisikHarfler[ord(harf) - 32]

            if run % 10 == 0 and random.randint(1, 2) == 1:
                random.shuffle(karisikHarfler)

    else:  # coz
        for harf in metin:
            if harf not in karisikHarfler:
                sonuc += harf
                continue

            run += 1
            index = karisikHarfler.index(harf)
            sonuc += harfler[index]

            if run % 10 == 0 and random.randint(1, 2) == 1:
                random.shuffle(karisikHarfler)

    return jsonify({"sonuc": sonuc})


# -------------------------------------------------
# APP START
# -------------------------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
