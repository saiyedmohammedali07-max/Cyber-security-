import os

SUSPICIOUS_EXT = [".exe", ".bat", ".sh", ".js"]

def check_file(filename):
    ext = os.path.splitext(filename)[1].lower()

    if ext in SUSPICIOUS_EXT:
        return "⚠️ Suspicious file detected"
    return "✅ File is safe"