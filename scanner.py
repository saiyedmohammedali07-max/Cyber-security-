# import requests

# def scan_target(url):
#     results = []

#     try:
#         # SQL Injection test
#         r = requests.get(url + "?id=1'")
#         if "error" in r.text.lower():
#             results.append("SQL Injection Vulnerability")

#         # XSS test
#         r = requests.get(url + "?q=<script>alert(1)</script>")
#         if "<script>" in r.text:
#             results.append("XSS Vulnerability")

#     except:
#         results.append("Scan failed")

#     return results
import requests

SQL_PAYLOADS = ["' OR '1'='1", "' OR 1=1 --"]
XSS_PAYLOADS = ["<script>alert(1)</script>"]

def scan_website(url):
    results = []

    for payload in SQL_PAYLOADS:
        try:
            r = requests.get(url + payload)
            if "sql" in r.text.lower():
                results.append("SQL Injection Vulnerability Found")
        except:
            pass

    for payload in XSS_PAYLOADS:
        try:
            r = requests.get(url + payload)
            if payload in r.text:
                results.append("XSS Vulnerability Found")
        except:
            pass

    return results if results else ["No vulnerabilities detected"]