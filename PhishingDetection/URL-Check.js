// File: URL-Check.js
const suspiciousKeywords = ["login", "secure", "account", "verify", "bank", "update"];
const maxSubdomains = 3;

function analyzeUrl(url) {
    let alerts = [];

    try {
        let parsed = new URL(url);

        // Check HTTPS
        if (parsed.protocol !== "https:") {
            alerts.push("No HTTPS");
        }

        // Check suspicious keywords
        for (let kw of suspiciousKeywords) {
            if (parsed.hostname.includes(kw)) {
                alerts.push("Suspicious keyword in domain");
                break;
            }
        }

        // Check subdomain count
        let parts = parsed.hostname.split(".");
        if (parts.length - 2 >= maxSubdomains) {
            alerts.push("Too many subdomains");
        }

    } catch (e) {
        alerts.push("Invalid URL");
    }

    if (alerts.length > 0) {
        console.warn(`[PHISHING ALERT] ${url} -> ${alerts.join("; ")}`);
    } else {
        console.log(`[SAFE] ${url}`);
    }
}

// Example usage
const urls = [
    "http://paypal-security-login.xyz",
    "https://www.google.com",
    "http://secure-bank-login.fake"
];

urls.forEach(analyzeUrl);