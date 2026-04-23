from flask import Flask, jsonify, render_template
from datetime import datetime
import random
import time
import math

app = Flask(__name__)

logs = []
alerts = []
packet_history = []

THREAT_TYPES = [
    {"type": "High Traffic (Possible DoS)", "severity": "Critical"},
    {"type": "Port Scan Detected", "severity": "High"},
    {"type": "Brute Force Attempt", "severity": "High"},
    {"type": "Suspicious Outbound DNS", "severity": "Medium"},
    {"type": "Unusual Login Time", "severity": "Medium"},
    {"type": "Failed Auth x5", "severity": "Low"},
]

SOURCE_IPS = [
    "192.168.1.14", "10.0.0.55", "172.16.8.3",
    "203.0.113.42", "198.51.100.9", "185.220.101.5"
]

PROTOCOLS = ["TCP", "UDP", "ICMP", "HTTP", "HTTPS", "DNS"]


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/data")
def get_data():
    global logs, alerts, packet_history

    # 🔥 REALISTIC TRAFFIC (wave + randomness)
    t = time.time()
    packet_count = int(150 + 100 * math.sin(t / 5) + random.randint(-30, 30))
    packet_count = max(10, min(packet_count, 320))

    src_ip = random.choice(SOURCE_IPS)
    protocol = random.choice(PROTOCOLS)

    now_str = datetime.now().strftime("%H:%M:%S")
    ts_full = str(datetime.now())

    # 📊 Packet history (last 30)
    packet_history.append({"time": now_str, "value": packet_count})
    if len(packet_history) > 30:
        packet_history = packet_history[-30:]

    # 📝 Logs
    logs.append({
        "time": now_str,
        "event": "Traffic Capture",
        "protocol": protocol,
        "src_ip": src_ip,
        "value": packet_count,
    })
    if len(logs) > 50:
        logs = logs[-50:]

    # 🚨 Smart alert logic
    new_alert = None

    if packet_count > 280:
        threat = THREAT_TYPES[0]  # Critical DoS
    elif packet_count > 230:
        threat = random.choice(THREAT_TYPES[1:3])  # High
    elif packet_count > 180:
        threat = random.choice(THREAT_TYPES[3:5])  # Medium
    elif random.random() < 0.05:
        threat = THREAT_TYPES[5]  # Rare low
    else:
        threat = None

    if threat:
        new_alert = {
            "time": now_str,
            "ts_full": ts_full,
            "type": threat["type"],
            "severity": threat["severity"],
            "src_ip": src_ip,
            "protocol": protocol,
            "packets": packet_count,
        }
        alerts.append(new_alert)
        if len(alerts) > 100:
            alerts = alerts[-100:]

    # 📈 Stats
    total_alerts = len(alerts)
    critical_count = sum(1 for a in alerts if a["severity"] == "Critical")
    high_count = sum(1 for a in alerts if a["severity"] == "High")

    return jsonify({
        "packet_count": packet_count,
        "packet_history": packet_history,
        "alerts": alerts[-8:],
        "logs": logs[-12:],
        "new_alert": new_alert,
        "stats": {
            "total_alerts": total_alerts,
            "critical_count": critical_count,
            "high_count": high_count,
            "packets_today": sum(p["value"] for p in packet_history),
        }
    })


@app.route("/api/clear", methods=["POST"])
def clear_data():
    global logs, alerts, packet_history
    logs, alerts, packet_history = [], [], []
    return jsonify({"status": "cleared"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, threaded=True)