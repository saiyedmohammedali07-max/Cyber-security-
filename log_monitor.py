logs = []

def add_log(log):
    logs.append(log)

    # anomaly detection
    if log["value"] > 250:
        logs.append({
            "time": log["time"],
            "event": "Anomaly Detected",
            "protocol": "-",
            "src_ip": log["src_ip"],
            "value": log["value"]
        })

    if len(logs) > 100:
        logs.pop(0)

def get_logs():
    return logs