from flask import Flask, request, jsonify
import requests, re
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/fetch_rent", methods=["GET"])
def fetch_rent():
    try:
        area = area.split("-")[0].strip()
        search_url = f"https://www.bayut.com/to-rent/apartments/dubai/?q={area}+1+bedroom"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        response = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Sayfadaki AED fiyatlarını yakala
        prices = re.findall(r"(\d{4,6})", response.text)
        prices = [int(p) for p in prices if 2000 < int(p) < 20000]

        avg = int(sum(prices) / len(prices)) if prices else 0

        return jsonify({"area": area, "average_rent": avg, "count": len(prices)})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
