from scapy.all import sniff, IP, TCP, UDP
from datetime import datetime
import signal
import sys

print("Python Packet Sniffer Running...\n")


def handle_packet(packet):
    if IP not in packet:
        return

    time = datetime.now().strftime("%H:%M:%S")
    src = packet[IP].src
    dst = packet[IP].dst

    if packet.haslayer(TCP):
        print(f"[{time}] TCP {src}:{packet[TCP].sport} -> {dst}:{packet[TCP].dport}")

    elif packet.haslayer(UDP):
        print(f"[{time}] UDP {src}:{packet[UDP].sport} -> {dst}:{packet[UDP].dport}")


# CTRL+C handler
def stop_sniffer(signal_received, frame):
    print("\nStopping sniffer safely...")
    sys.exit(0)


signal.signal(signal.SIGINT, stop_sniffer)

sniff(filter="ip", prn=handle_packet, store=False)