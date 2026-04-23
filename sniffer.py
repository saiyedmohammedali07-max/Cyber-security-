from scapy.all import sniff, IP, TCP, UDP
import time

packet_count = 0
last_time = time.time()

def process_packet(pkt):
    global packet_count
    packet_count += 1

def start_sniffing():
    sniff(prn=process_packet, store=False, count=20)

def get_packet_data():
    global packet_count, last_time

    start_sniffing()

    current_time = time.time()
    rate = packet_count

    packet_count = 0

    return {
        "packet_count": rate,
        "src_ip": "Live",
        "protocol": "Mixed"
    }