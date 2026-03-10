# File: Main.py
import requests, tldextract, whois, ssl, socket, time, csv
from urllib.parse import urlparse

LOG_FILE = "phishing_alerts.csv"
SUSPICIOUS_KEYWORDS = ["login", "secure", "account", "verify", "bank", "update"]

# -------------------------------
# Logging
# -------------------------------
def log_alert(url, alert_type, details):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"[ALERT] {timestamp} | {alert_type} | {url} | {details}")
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, alert_type, url, details])

# -------------------------------
# Detection Functions
# -------------------------------
def check_https(url):
    try:
        parsed = urlparse(url)
        host = parsed.netloc
        context = ssl.create_default_context()
        with socket.create_connection((host, 443), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                cert = ssock.getpeercert()
                return True, cert.get('subject')
    except Exception:
        return False, None

def check_domain_age(url):
    try:
        domain = tldextract.extract(url).registered_domain
        w = whois.whois(domain)
        if w.creation_date:
            if isinstance(w.creation_date, list):
                creation_time = min([c.timestamp() for c in w.creation_date])
            else:
                creation_time = w.creation_date.timestamp()
            age_years = (time.time() - creation_time) / (365*24*3600)
            return age_years
        return 0
    except:
        return 0

def suspicious_keywords(url):
    return any(k in url.lower() for k in SUSPICIOUS_KEYWORDS)

def many_subdomains(url):
    subdomains = tldextract.extract(url).subdomain
    return len(subdomains.split('.')) >= 3

# -------------------------------
# Main Analyzer
# -------------------------------
def analyze_url(url):
    alerts = []

    https_valid, cert_subject = check_https(url)
    if not https_valid:
        alerts.append("No valid HTTPS certificate")

    age = check_domain_age(url)
    if age < 1:
        alerts.append("Newly registered domain")

    if suspicious_keywords(url):
        alerts.append("Suspicious keywords in URL")

    if many_subdomains(url):
        alerts.append("Too many subdomains")

    if alerts:
        log_alert(url, "PHISHING ALERT", "; ".join(alerts))
    else:
        print(f"[SAFE] {url}")

# -------------------------------
# Entry Point
# -------------------------------
if __name__ == "__main__":
    # Initialize log file
    with open(LOG_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["Time", "Alert_Type", "URL", "Details"])

    urls = [
        "http://paypal-security-login.xyz",
        "https://www.google.com",
        "http://secure-bank-login.fake"
    ]
    for u in urls:
        analyze_url(u)