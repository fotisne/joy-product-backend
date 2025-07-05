from flask import Flask, request, jsonify
import json
import unicodedata

app = Flask(__name__)

# Φόρτωση προϊόντων από το αρχείο
with open("products-full.json", encoding="utf-8") as f:
    PRODUCTS = json.load(f)

def normalize(text):
    return ''.join(
        c for c in unicodedata.normalize("NFD", text.lower())
        if unicodedata.category(c) != 'Mn'
    )

@app.route("/search")
def search_products():
    query = request.args.get("query", "").strip().lower()
    if not query:
        return jsonify([])

    norm_query = normalize(query)
    keywords = norm_query.split()

    results = []
    for product in PRODUCTS:
        search_fields = [
            product.get("name", ""),
            product.get("short_description", ""),
            product.get("description", ""),
            product.get("color", ""),
            " ".join(product.get("categories", []))
        ]
        combined_text = normalize(" ".join(search_fields))

        if all(k in combined_text for k in keywords):
            results.append({
                "id": product.get("id"),
                "name": product.get("name"),
                "color": product.get("color"),
                "sizes": product.get("available_sizes"),
                "price": product.get("price"),
                "image": product.get("image"),
                "permalink": product.get("permalink")
            })

    return jsonify(results)

@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "products_loaded": len(PRODUCTS)
    })

if __name__ == "__main__":
    app.run(debug=True)
