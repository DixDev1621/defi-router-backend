from flask import Flask, request, jsonify
from flask_cors import CORS
from auth import auth_bp
import requests
import os

app = Flask(__name__)
app.register_blueprint(auth_bp, url_prefix="/api/auth")
CORS(app)

# ✅ Etherscan V2 API key (Polygon supported)
API_KEY = "12ZRKG2A616KXZXHYUHBFCBX1D1PKGM8WN"

def get_transactions(wallet):
    # ✅ Correct Etherscan V2 endpoint for Polygon
    url = (
        "https://api.etherscan.io/v2/api"
        f"?chain=polygon"
        f"&module=account"
        f"&action=txlist"
        f"&address={wallet}"
        f"&sort=desc"
        f"&apikey={API_KEY}"
    )

    try:
        res = requests.get(url, timeout=10)
        data = res.json()

        print("🔍 API RAW RESPONSE:", data)  # DEBUG

        if isinstance(data.get("result"), list):
            return data["result"]
        else:
            return []

    except Exception as e:
        print("❌ API ERROR:", e)
        return []


@app.route("/check_wallet", methods=["POST"])
def check_wallet():
    data = request.get_json()
    wallet = data.get("walletAddress", "").strip().lower()

    if not wallet:
        return jsonify({"error": "No wallet address provided"}), 400

    txs = get_transactions(wallet)

    if not txs:
        return jsonify({
            "message": "⚠ No transaction data found (new wallet / API delay)",
            "risk": "low",
            "incoming": 0,
            "outgoing": 0,
            "tx_count": 0
        })



    total_incoming = 0
    total_outgoing = 0

    for tx in txs[:30]:  # last 30 transactions
        try:
            value = int(tx.get("value", "0")) / 1e18
            if tx.get("to", "").lower() == wallet:
                total_incoming += value
            if tx.get("from", "").lower() == wallet:
                total_outgoing += value
        except:
            continue

    tx_count = len(txs)

    # ✅ AI-style rule-based risk scoring
    if total_incoming > 100 or tx_count > 50:
        risk = "high"
        message = "🚨 High Risk: Unusual volume or excessive transactions detected!"
    elif total_incoming > 10 or total_outgoing > 10 or tx_count > 20:
        risk = "medium"
        message = "⚠ Medium Risk: Moderate wallet activity observed."
    else:
        risk = "low"
        message = "✅ Low Risk: Normal wallet behavior."

    return jsonify({
        "message": message,
        "risk": risk,
        "incoming": round(total_incoming, 3),
        "outgoing": round(total_outgoing, 3),
        "tx_count": tx_count
    })


@app.route("/")
def home():
    return jsonify({"message": "AI Risk Detection Backend Running 🚀"})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

HIGH_RISK_LIST = [
    "0x1111111111111111111111111111111111111111"
]

def calculate_risk(receiver, amount):
    score = 0

    if receiver.lower() in HIGH_RISK_LIST:
        score += 80

    if float(amount) > 5:
        score += 20

    return min(score, 100)


@app.route("/api/risk-check", methods=["POST"])
def risk_check():
    data = request.json
    sender = data.get("sender")
    receiver = data.get("receiver")
    amount = data.get("amount")

    risk_score = calculate_risk(receiver, amount)

    return jsonify({
        "risk_score": risk_score,
        "status": "safe" if risk_score < 70 else "high_risk"
    })
