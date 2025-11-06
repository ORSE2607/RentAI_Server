from flask import Flask, request, jsonify
import requests, re
from bs4 import BeautifulSoup
import statistics

app = Flask(__name__)

@app.route("/fetch_rent", methods=["GET"])
def fetch_rent():
    try:
        area = request.args.get("area", "").strip()
        if not area:
            return jsonify({"error": "area parameter is missing"}), 400

        # "Murjan 5 - JBR" gibi ifadelerde yalnızca ilk kısmı al
        area = re.split(r"[-–,]", area)[0].strip()

        # Bayut üzerinde arama linki
       search_url = f"https://www.dubizzle.com/property-for-rent/residential/apartmentflat/?keywords={area}&page=1"

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }
        res = requests.get(search_url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")

        # Sayfa içeriğinde fiyatları bul
        text = soup.get_text()
        prices = re.findall(r"AED\s?([\d,]+)", text)
        prices = [int(p.replace(",", "")) for p in prices if 1000 < int(p.replace(",", "")) < 200000]

        if not prices:
            return jsonify({"area": area, "average_rent": 0, "count": 0})

        avg_rent = int(statistics.mean(prices))
        return jsonify({
            "area": area,
            "average_rent": avg_rent,
            "count": len(prices)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)


