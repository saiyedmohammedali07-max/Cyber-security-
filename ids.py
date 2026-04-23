failed_logins = 0

def detect(packet):
    alerts = []

    if packet["packet_count"] > 300:
        alerts.append(("DoS Attack Detected", "Critical"))

    if packet["packet_count"] > 200:
        alerts.append(("Port Scanning Activity", "High"))

    # Simulated brute force
    global failed_logins
    failed_logins += 1

    if failed_logins > 5:
        alerts.append(("Brute Force Attempt", "High"))
        failed_logins = 0

    return alerts