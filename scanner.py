import requests

def scan_target(url):
    results = []

    try:
        # SQL Injection test
        r = requests.get(url + "?id=1'")
        if "error" in r.text.lower():
            results.append("SQL Injection Vulnerability")

        # XSS test
        r = requests.get(url + "?q=<script>alert(1)</script>")
        if "<script>" in r.text:
            results.append("XSS Vulnerability")

    except:
        results.append("Scan failed")

    return results