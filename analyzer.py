import re

# -----------------------------
# Check if QR data is a URL
# -----------------------------
def is_url(data):
    pattern = re.compile(
        r'^(https?://)?([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}(/.*)?$'
    )
    return bool(pattern.match(data))


# -----------------------------
# Analyze Website URL
# -----------------------------
def analyze_url(url):

    risk_score = 0
    reasons = []

    # HTTPS Check
    if url.startswith("https://"):
        reasons.append("✅ Secure HTTPS connection detected.")
    else:
        risk_score += 20
        reasons.append("❌ Website is not using HTTPS.")

    # IP Address Check
    ip_pattern = r'(\d{1,3}\.){3}\d{1,3}'

    if re.search(ip_pattern, url):
        risk_score += 25
        reasons.append("⚠ Website uses an IP Address.")

    # URL Shorteners
    shorteners = [
        "bit.ly",
        "tinyurl.com",
        "t.co",
        "goo.gl",
        "ow.ly",
        "is.gd",
        "buff.ly",
        "rb.gy"
    ]

    for short in shorteners:
        if short in url.lower():
            risk_score += 20
            reasons.append("⚠ URL Shortener detected.")
            break

    # Suspicious Keywords
    keywords = [
        "login",
        "signin",
        "verify",
        "update",
        "password",
        "account",
        "bank",
        "paypal",
        "wallet",
        "gift",
        "reward",
        "security",
        "confirm"
    ]

    found = False

    for word in keywords:
        if word in url.lower():
            risk_score += 10
            reasons.append(f"⚠ Suspicious keyword: {word}")
            found = True

    if not found:
        reasons.append("✅ No suspicious keywords found.")

    # Long URL
    if len(url) > 80:
        risk_score += 10
        reasons.append("⚠ URL is unusually long.")

    # Too Many Subdomains
    if url.count(".") > 3:
        risk_score += 10
        reasons.append("⚠ Multiple subdomains detected.")

    # '@' Symbol
    if "@" in url:
        risk_score += 15
        reasons.append("⚠ '@' symbol detected.")

    # Double Slash
    temp = url.replace("https://", "").replace("http://", "")

    if "//" in temp:
        risk_score += 10
        reasons.append("⚠ Suspicious double slash detected.")

    # Normalize Score
    if risk_score > 100:
        risk_score = 100

    # Threat Level
    if risk_score <= 20:
        level = "🟢 SAFE"

    elif risk_score <= 50:
        level = "🟡 MEDIUM RISK"

    elif risk_score <= 80:
        level = "🟠 HIGH RISK"

    else:
        level = "🔴 CRITICAL"

    return risk_score, level, reasons