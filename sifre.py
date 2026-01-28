import random
import hashlib
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)   # ← İŞTE BURASI ÇOK ÖNEMLİ

@app.route("/sifrele", methods=["POST"])
def sifrele():
    data = request.json

    metin = data["metin"]
    anahtar = data["anahtar"]
    option = data["option"]  # "sifrele" | "coz"

    # ASCII 32–126
    harfler = [chr(i) for i in range(32, 126)]

    try:
        key = int(anahtar)
    except:
        h = hashlib.sha256(anahtar.encode()).digest()
        key = int.from_bytes(h[:8], "big", signed=True)

    random.seed(key)

    karisikHarfler = harfler.copy()
    random.shuffle(karisikHarfler)

    sonuc = ""

    if option == "sifrele":
        run = 0
        for harf in metin:
            run += 1
            sonuc += karisikHarfler[ord(harf) - 32]
            if run % 10 == 0 and random.randint(1, 2) == 1:
                random.shuffle(karisikHarfler)

    elif option == "coz":
        run = 0
        for harf in metin:
            run += 1
            index = karisikHarfler.index(harf)
            sonuc += harfler[index]
            if run % 10 == 0 and random.randint(1, 2) == 1:
                random.shuffle(karisikHarfler)

    return jsonify({"sonuc": sonuc})

if __name__ == "__main__":
    app.run(debug=True)
