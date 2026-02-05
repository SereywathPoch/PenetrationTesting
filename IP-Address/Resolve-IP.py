import socket

def clean_url(url):
    url = url.strip()
    if url.startswith("http://"):
        url = url.replace("http://", "")
    elif url.startswith("https://"):
        url = url.replace("https://", "")
    if url.startswith("www."):
        url = url.replace("www.", "")
    return url.split("/")[0]

url = input("Enter a URL: ")
domain = clean_url(url)

try:
    ip = socket.gethostbyname(domain)
    print(f"IP Address of {domain}: {ip}")
except:
    print("Could not resolve the domain")
# How to run: python Resolve-IP.py