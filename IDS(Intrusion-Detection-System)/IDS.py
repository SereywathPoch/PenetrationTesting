# File: IDS.py
from scapy.all import sniff, TCP, ARP, IP
from collections import defaultdict
import time
import csv

# -------------------------------
# Configurations
# -------------------------------
PORT_SCAN_THRESHOLD = 10   # number of ports in TIME_WINDOW
SYN_FLOOD_THRESHOLD = 20   # SYN packets without ACK
TIME_WINDOW = 10           # seconds
LOG_FILE = "ids_alerts.csv"

# -------------------------------
# Data Structures
# -------------------------------
connections = defaultdict(list)   # For port scan detection
syn_packets = defaultdict(list)   # For SYN flood detection
arp_cache = {}                    # For ARP spoofing detection

# Initialize log file
with open(LOG_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Time", "Alert_Type", "Source_IP", "Details"])

# -------------------------------
# Helper Functions
# -------------------------------
def log_alert(alert_type, src_ip, details):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"[ALERT] {timestamp} | {alert_type} | {src_ip} | {details}")
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([timestamp, alert_type, src_ip, details])

# -------------------------------
# Detection Functions
# -------------------------------
def detect_port_scan(pkt):
    if pkt.haslayer(TCP) and pkt.haslayer(IP):
        src_ip = pkt[IP].src
        dst_port = pkt[TCP].dport
        timestamp = time.time()
        
        connections[src_ip].append((dst_port, timestamp))
        # Clean old entries
        connections[src_ip] = [(p, t) for (p, t) in connections[src_ip] if timestamp - t < TIME_WINDOW]
        
        # Check if scanned many ports
        if len(set([p for p, t in connections[src_ip]])) > PORT_SCAN_THRESHOLD:
            log_alert("Port Scan", src_ip, f"Scanned {len(set([p for p, t in connections[src_ip]]))} ports")

def detect_syn_flood(pkt):
    if pkt.haslayer(TCP) and pkt.haslayer(IP):
        src_ip = pkt[IP].src
        flags = pkt[TCP].flags
        timestamp = time.time()
        
        if flags == "S":  # SYN packet
            syn_packets[src_ip].append(timestamp)
        elif flags == "A":  # ACK packet, remove SYN record
            if src_ip in syn_packets and syn_packets[src_ip]:
                syn_packets[src_ip].pop(0)
        
        # Clean old entries
        if src_ip in syn_packets:
            syn_packets[src_ip] = [t for t in syn_packets[src_ip] if timestamp - t < TIME_WINDOW]
        
        if src_ip in syn_packets and len(syn_packets[src_ip]) > SYN_FLOOD_THRESHOLD:
            log_alert("SYN Flood", src_ip, f"{len(syn_packets[src_ip])} SYN packets without ACK")

def detect_arp_spoof(pkt):
    if pkt.haslayer(ARP):
        src_ip = pkt[ARP].psrc
        src_mac = pkt[ARP].hwsrc
        
        if src_ip in arp_cache:
            if arp_cache[src_ip] != src_mac:
                log_alert("ARP Spoofing", src_ip, f"MAC changed from {arp_cache[src_ip]} to {src_mac}")
        
        arp_cache[src_ip] = src_mac

# -------------------------------
# Packet Sniffing
# -------------------------------
def monitor_network():
    print("Starting Mini IDS... Press Ctrl+C to stop")
    sniff(prn=lambda pkt: [detect_port_scan(pkt), detect_syn_flood(pkt), detect_arp_spoof(pkt)], store=False)

# -------------------------------
# Main
# -------------------------------
if __name__ == "__main__":
    monitor_network()