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

        # Dubizzle üzerindeki ilan arama linki
        search_url = f"https://www.dubizzle.com/property-for-rent/apartmentflat/?q={area}"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        res = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        # Sayfada fiyatları yakala (örnek: AED 80,000 veya 6,500 AED)
        prices_text = soup.get_text()
        prices = re.findall(r"AED\s?[\d,]+", prices_text)

        numbers = []
        for p in prices:
            num = int(re.sub(r"[^\d]", "", p))
            if 1000 < num < 500000:
                numbers.append(num)

        if not numbers:
            return jsonify({"area": area, "average_rent": 0, "count": 0})

        avg_rent = int(statistics.mean(numbers))
        return jsonify({
            "area": area,
            "average_rent": avg_rent,
            "count": len(numbers)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
