import socket
import subprocess
import platform

# -------------------------
# HOST SCAN (PING)
# -------------------------
def host_scan(target):
    print(f"\nHost Scan: {target}")
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", target]

    result = subprocess.run(command, stdout=subprocess.DEVNULL)
    if result.returncode == 0:
        print("Host is UP")
        return True
    else:
        print("Host is DOWN")
        return False

# -------------------------
# PORT SCAN
# -------------------------
def port_scan(target):
    print("\nPort Scan (Web-related ports)")
    ports = [80, 443, 5000, 8000, 8080]

    for port in ports:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            result = s.connect_ex((target, port))
            if result == 0:
                print(f"Port {port} OPEN")
            s.close()
        except:
            pass

# -------------------------
# MAIN
# -------------------------
def main():
    print("WEBSITE SCANNER")


    target = input("Enter target (default: 127.0.0.1): ").strip()
    if not target:
        target = "127.0.0.1"

    if host_scan(target):
        port_scan(target)

if __name__ == "__main__":
    main()
