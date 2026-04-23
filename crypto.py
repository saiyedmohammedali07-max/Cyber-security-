# from cryptography.fernet import Fernet

# key = Fernet.generate_key()
# cipher = Fernet(key)

# def encrypt_data(data):
#     return cipher.encrypt(data.encode())

# def decrypt_data(data):
#     return cipher.decrypt(data).decode()
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