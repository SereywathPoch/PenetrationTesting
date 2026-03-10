// File: URL-Features.cpp
#include <iostream>
#include <string>
#include <cctype>

struct UrlFeatures {
    int length;
    int digits;
    int special_chars;
    int subdomain_count;
};

UrlFeatures extract_features(const std::string& url) {
    UrlFeatures f = {0,0,0,0};
    std::string hostname;
    size_t pos1 = url.find("://");
    size_t start = (pos1 == std::string::npos) ? 0 : pos1 + 3;
    size_t pos2 = url.find("/", start);
    hostname = url.substr(start, pos2 - start);

    for (char c : url) {
        f.length++;
        if (isdigit(c)) f.digits++;
        if (c == '.' || c == '-' || c == '_') f.special_chars++;
    }

    int dots = 0;
    for (char c : hostname) if (c == '.') dots++;
    f.subdomain_count = (dots > 1) ? dots - 1 : 0;

    return f;
}

int main() {
    std::string urls[] = {
        "http://paypal-security-login.xyz",
        "https://www.google.com",
        "http://secure-bank-login.fake"
    };

    for (auto& url : urls) {
        UrlFeatures f = extract_features(url);
        std::cout << "URL: " << url 
                  << " | Length: " << f.length
                  << " | Digits: " << f.digits
                  << " | Special: " << f.special_chars
                  << " | Subdomains: " << f.subdomain_count
                  << std::endl;
    }
}