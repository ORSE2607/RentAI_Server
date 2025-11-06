from flask import Flask, request, jsonify
import requests
from bs4 import BeautifulSoup
import re
import statistics

app = Flask(__name__)

@app.route("/fetch_rent", methods=["GET"])
def fetch_rent():
    try:
        area = request.args.get("area", "").strip()
        if not area:
            return jsonify({"error": "area parameter is missing"}), 400

        # Dubizzle araması (Google üzerinden)
        query = f"{area} rent site:dubizzle.com"
        url = f"https://www.google.com/search?q={query}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        # Google sonuçlarından olası fiyatları bul (örnek: AED 80,000, AED 6,500 etc.)
        prices = re.findall(r"AED\s?[\d,]+", soup.text)

        numbers = []
        for p in prices:
            num = int(re.sub(r"[^\d]", "", p))
            # mantıksız büyük veya küçük değerleri filtrele
            if 1000 < num < 500000:
                numbers.append(num)

        if not numbers:
            return jsonify({"area": area, "average_rent": 0, "count": 0})

        avg_rent = int(statistics.mean(numbers))
        return jsonify({"area": area, "average_rent": avg_rent, "count": len(numbers)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
