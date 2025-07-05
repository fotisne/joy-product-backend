from flask import Flask, jsonify, request
import unicodedata
import json
import os

app = Flask(__name__)

# 🔹 Normalize helper (χωρίς τόνους, πεζά, χωρίς σημεία στίξης)
def normalize(text):
    return ''.join(
        c for c in unicodedata.normalize("NFD", text.lower())
        if unicodedata.category(c) != 'Mn'
    )

# 🔹 Φορτώνουμε το τοπικό JSON μία φορά
with open("products-full.json", "r", encoding="utf-8") as f:
    LOCAL_PRODUCTS = json.load(f)

@app.route("/search")
def search():
    query = request.args.get("query", "")
    if not query:
        return jsonify([])

    keywords = [normalize(k) for k in query.split()]
    results = []

    for product in LOCAL_PRODUCTS:
        fields_to_search = [
            product.get("name", ""),
            product.get("short_description", ""),
            product.get("description", ""),
            product.get("color", ""),
            " ".join(product.get("categories", [])),
            " ".join(product.get("available_sizes", []))
        ]

        combined_text = normalize(" ".join(fields_to_search))

        if all(k in combined_text for k in keywords):
            results.append({
                "id": product.get("id"),
                "name": product.get("name"),
                "color": product.get("color"),
                "permalink": product.get("permalink")
            })

    return jsonify(results)

@app.route("/health")
def health():
    return jsonify({"status": "ok", "products_loaded": len(LOCAL_PRODUCTS)})

# 🔧 ΕΔΩ ΕΙΝΑΙ Η ΣΩΣΤΗ ΕΚΔΟΣΗ για Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
