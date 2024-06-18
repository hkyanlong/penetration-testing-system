import nmap
from scapy.all import *
from scapy.layers.inet import *
from scapy.layers.l2 import ARP
import concurrent.futures
import threading
import time
import sys
import socket
import random
from colorama import init, Fore
init(autoreset=True)  # 初始化colorama，设置autoreset=True以便在每次打印后自动重置颜色


# 创建一个线程锁
print_lock = threading.Lock()


SIGNS = (
    #协议 | 版本 | 关键字
    b'smb|smb|^\0\0\0.\xffSMBr\0\0\0\0.*',
    b"xmpp|xmpp|^<?xml version='1.0'?>",
    b'netbios|netbios|^\x79\x08.*BROWSE',
    b'netbios|netbios|^\x79\x08.\x00\x00\x00\x00',
    b'netbios|netbios|^\x05\x00\x0d\x03',
    b'netbios|netbios|^\x82\x00\x00\x00',
    b'netbios|netbios|\x83\x00\x00\x01\x8f',
    b'backdoor|backdoor|^500 Not Loged in',
    b'backdoor|backdoor|GET: command',
    b'backdoor|backdoor|sh: GET:',
    b'bachdoor|bachdoor|[a-z]*sh: .* command not found',
    b'backdoor|backdoor|^bash[$#]',
    b'backdoor|backdoor|^sh[$#]',
    b'backdoor|backdoor|^Microsoft Windows',
    b'db2|db2|.*SQLDB2RA',
    b'dell-openmanage|dell-openmanage|^\x4e\x00\x0d',
    b'finger|finger|^\r\n	Line	  User',
    b'finger|finger|Line	 User',
    b'finger|finger|Login name: ',
    b'finger|finger|Login.*Name.*TTY.*Idle',
    b'finger|finger|^No one logged on',
    b'finger|finger|^\r\nWelcome',
    b'finger|finger|^finger:',
    b'finger|finger|^must provide username',
    b'finger|finger|finger: GET: ',
    b'ftp|ftp|^220.*\n331',
    b'ftp|ftp|^220.*\n530',
    b'ftp|ftp|^220.*FTP',
    b'ftp|ftp|^220 .* Microsoft .* FTP',
    b'ftp|ftp|^220 Inactivity timer',
    b'ftp|ftp|^220 .* UserGate',
    b'ftp|ftp|^220.*FileZilla Server',
    b'ldap|ldap|^\x30\x0c\x02\x01\x01\x61',
    b'ldap|ldap|^\x30\x32\x02\x01',
    b'ldap|ldap|^\x30\x33\x02\x01',
    b'ldap|ldap|^\x30\x38\x02\x01',
    b'ldap|ldap|^\x30\x84',
    b'ldap|ldap|^\x30\x45',
    b'ldp|ldp|^\x00\x01\x00.*?\r\n\r\n$',
    b'rdp|rdp|^\x03\x00\x00\x0b',
    b'rdp|rdp|^\x03\x00\x00\x11',
    b'rdp|rdp|^\x03\0\0\x0b\x06\xd0\0\0\x12.\0$',
    b'rdp|rdp|^\x03\0\0\x17\x08\x02\0\0Z~\0\x0b\x05\x05@\x06\0\x08\x91J\0\x02X$',
    b'rdp|rdp|^\x03\0\0\x11\x08\x02..}\x08\x03\0\0\xdf\x14\x01\x01$',
    b'rdp|rdp|^\x03\0\0\x0b\x06\xd0\0\0\x03.\0$',
    b'rdp|rdp|^\x03\0\0\x0b\x06\xd0\0\0\0\0\0',
    b'rdp|rdp|^\x03\0\0\x0e\t\xd0\0\0\0[\x02\xa1]\0\xc0\x01\n$',
    b'rdp|rdp|^\x03\0\0\x0b\x06\xd0\0\x004\x12\0',
    b'rdp-proxy|rdp-proxy|^nmproxy: Procotol byte is not 8\n$',
    b'msrpc|msrpc|^\x05\x00\x0d\x03\x10\x00\x00\x00\x18\x00\x00\x00\x00\x00',
    b'msrpc|msrpc|\x05\0\r\x03\x10\0\0\0\x18\0\0\0....\x04\0\x01\x05\0\0\0\0$',
    b'mssql|mssql|^\x05\x6e\x00',
    b'mssql|mssql|^\x04\x01',
    b'mssql|mysql|;MSSQLSERVER;',
    b'mysql|mysql|mysql_native_password',
    b'mysql|mysql|^\x19\x00\x00\x00\x0a',
    b'mysql|mysql|^\x2c\x00\x00\x00\x0a',
    b'mysql|mysql|hhost \'',
    b'mysql|mysql|khost \'',
    b'mysql|mysql|mysqladmin',
    b'mysql|mysql|whost \'',
    b'mysql|mysql|^[.*]\x00\x00\x00\n.*?\x00',
    b'mysql-secured|mysql|this MySQL server',
    b'mysql-secured|MariaDB|MariaDB server',
    b'mysql-secured|mysql-secured|\x00\x00\x00\xffj\x04Host',
    b'db2jds|db2jds|^N\x00',
    b'nagiosd|nagiosd|Sorry, you \\(.*are not among the allowed hosts...',
    b'nessus|nessus|< NTP 1.2 >\x0aUser:',
    b'oracle-tns-listener|\\(ERROR_STACK=\\(ERROR=\\(CODE=',
    b'oracle-tns-listener|\\(ADDRESS=\\(PROTOCOL=',
    b'oracle-dbsnmp|^\x00\x0c\x00\x00\x04\x00\x00\x00\x00',
    b'oracle-https|^220- ora',
    b'rmi|rmi|\x00\x00\x00\x76\x49\x6e\x76\x61',
    b'rmi|rmi|^\x4e\x00\x09',
    b'postgresql|postgres|Invalid packet length',
    b'postgresql|postgres|^EFATAL',
    b'rpc-nfs|rpc-nfs|^\x02\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00',
    b'rpc|rpc|\x01\x86\xa0',
    b'rpc|rpc|\x03\x9b\x65\x42\x00\x00\x00\x01',
    b'rpc|rpc|^\x80\x00\x00',
    b'rsync|rsync|^@RSYNCD:',
    b'smux|smux|^\x41\x01\x02\x00',
    b'snmp-public|snmp-public|\x70\x75\x62\x6c\x69\x63\xa2',
    b'snmp|snmp|\x41\x01\x02',
    b'socks|socks|^\x05[\x00-\x08]\x00',
    b'ssl|ssl|^..\x04\0.\0\x02',
    b'ssl|ssl|^\x16\x03\x01..\x02...\x03\x01',
    b'ssl|ssl|^\x16\x03\0..\x02...\x03\0',
    b'ssl|ssl|SSL.*GET_CLIENT_HELLO',
    b'ssl|ssl|^-ERR .*tls_start_servertls',
    b'ssl|ssl|^\x16\x03\0\0J\x02\0\0F\x03\0',
    b'ssl|ssl|^\x16\x03\0..\x02\0\0F\x03\0',
    b'ssl|ssl|^\x15\x03\0\0\x02\x02\\.*',
    b'ssl|ssl|^\x16\x03\x01..\x02...\x03\x01',
    b'ssl|ssl|^\x16\x03\0..\x02...\x03\0',
    b'sybase|sybase|^\x04\x01\x00',
    b'telnet|telnet|Telnet',
    b'telnet|telnet|^\xff[\xfa-\xff]',
    b'telnet|telnet|^\r\n%connection closed by remote host!\x00$',
    b'rlogin|rlogin|login: ',
    b'rlogin|rlogin|rlogind: ',
    b'rlogin|rlogin|^\x01\x50\x65\x72\x6d\x69\x73\x73\x69\x6f\x6e\x20\x64\x65\x6e\x69\x65\x64\x2e\x0a',
    b'tftp|tftp|^\x00[\x03\x05]\x00',
    b'uucp|uucp|^login: password: ',
    b'vnc|vnc|^RFB',
    b'imap|imap|^\\* OK.*?IMAP',
    b'pop|pop|^\\+OK.*?',
    b'smtp|smtp|^220.*?SMTP',
    b'smtp|smtp|^554 SMTP',
    b'ftp|ftp|^220-',
    b'ftp|ftp|^220.*?FTP',
    b'ftp|ftp|^220.*?FileZilla',
    b'ssh|ssh|^SSH-',
    b'ssh|ssh|connection refused by remote host.',
    b'rtsp|rtsp|^RTSP/',
    b'sip|sip|^SIP/',
    b'nntp|nntp|^200 NNTP',
    b'sccp|sccp|^\x01\x00\x00\x00$',
    b'webmin|webmin|.*MiniServ',
    b'webmin|webmin|^0\\.0\\.0\\.0:.*:[0-9]',
    b'websphere-javaw|websphere-javaw|^\x15\x00\x00\x00\x02\x02\x0a',
    b'smb|smb|^\x83\x00\x00\x01\x8f',
    b'docker-daemon|docker-daemon|^\x15\x03\x01\x00\x02\x02',
    b'mongodb|mongodb|MongoDB',
    b'Rsync|Rsync|@RSYNCD:',
    b'Squid|Squid|X-Squid-Error',
    b'mssql|Mssql|MSSQLSERVER',
    b'Vmware|Vmware|VMware',
    b'iscsi|iscsi|\x00\x02\x0b\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
    b'redis|redis|^-ERR unknown command',
    b'redis|redis|^-ERR wrong number of arguments',
    b'redis|redis|^-DENIED Redis is running',
    b'memcached|memcached|^ERROR\r\n',
    b'websocket|websocket|Server: WebSocket',
    b'https|https|Instead use the HTTPS scheme to access'
    b'https|https|HTTPS port',
    b'https|https|Location: https',
    b'http|http|^HTTP',
    b'http|topsec|^\x15\x03\x03\x00\x02\x02',
    b'SVN|SVN|^\\( success \\( 2 2 \\( \\) \\( edit-pipeline svndiff1',
    b'dubbo|dubbo|^Unsupported command',
    b'http|elasticsearch|cluster_name.*elasticsearch',
    b'RabbitMQ|RabbitMQ|^AMQP\x00\x00\t\x01',
)


def get_service_info(dst_ip, dst_port):
    # 使用python-nmap来获取端口服务信息
    nm = nmap.PortScanner()
    nm.scan(hosts=dst_ip, arguments=f"-p {dst_port} -sV")
    service_info = nm[dst_ip]['tcp'][dst_port]
    return service_info['name']



def get_http_banner(host, port):

    payload1 = (
            'GET / HTTP/1.1\r\nHOST: %s\r\nUser-Agent: Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; '
            'QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)\r\nAccept: text/html\r\nCookie: adminUser=123\r\n\r\n'
            % host)
    try:
        with socket.create_connection((host, port), timeout=1) as s:
            s.sendall(payload1.encode())
            response = s.recv(4096)
            for pattern in SIGNS:
                pattern = pattern.split(b'|')     # 拆分出协议和正则表达式
                if re.search(pattern[-1], response, re.IGNORECASE):     # 匹配正则表达式
                    proto = pattern[1].decode()    # 获取协议
                    break
            # 直接打印二进制数据
            #print('proto:',proto, end='')
            #print('\t\tbanner:',response.split(b'\r\n'))

            return [proto, response.split(b'\r\n\r\n')]
    except:
        return [get_service_info(host, port)]







def get_mac(dst_ip):
    arp_request = ARP(pdst=dst_ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet_arp = ether / arp_request
    arp_response = srp(packet_arp, timeout=1, verbose=0)[0]
    # 提取目标主机的 MAC 地址
    for sent, received in arp_response:
        return 1
    return -1




# 端口扫描功能
def portscan_of_syn_send(src_ip, src_port, dst_ip, dst_port):
    # 构造ip头
    ip = IP(src=src_ip, dst=dst_ip)  # 设置源IP地址与目的IP地址
    # 构造TCP头，并设置源端口与目的端口和设置SYN标志位
    tcp = TCP(sport=src_port, dport=dst_port, flags="S")
    # 添加数据到TCP载荷
    tcp_payload = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    # 组合构造数据包
    packet_of_send = ip / tcp / tcp_payload
    # 发送数据
    tcp_response = sr1(packet_of_send, timeout=1, verbose=0)
    with print_lock:
        if tcp_response is None:
            # print(f"Port {dst_port} is not open")
            return -1
        if tcp_response.haslayer(TCP):
            if tcp_response[TCP].flags == "SA":
                # 获取http协议的banner信息
                proto = get_http_banner(dst_ip, dst_port)
                print(Fore.BLUE + f"Port {dst_port} is open, Service: {proto}")
                # return "dst_port"
            return -1



def portscan_of_ack_send(src_ip, src_port, dst_ip, dst_port):
    # 构造IP头
    ip = IP(src=src_ip, dst=dst_ip)
    # 构造TCP头，并设置源端口与目的端口和设置ACK标志位
    tcp = TCP(sport=src_port, dport=dst_port, flags="A")
    # 组合构造数据包
    packet = ip / tcp

    # 发送数据并等待响应
    answered = sr1(packet, timeout=4, verbose=0)

    if answered is not None:
        with print_lock:
            if answered.haslayer(ICMP):
                icmp_type = answered[ICMP].type
                icmp_code = answered[ICMP].code
                if icmp_type == 3 and icmp_code in [1, 2, 3, 9, 10, 13]:
                    print(Fore.BLUE + f"Port {dst_port} is filtered")
                    return "filtered"
            elif answered.haslayer(TCP):
                if answered[TCP].flags == "R":  # 可能同时设置了RST和ACK
                    #print(Fore.GREEN + f"Port {dst_port} is unfiltered")
                    return "unfiltered"
                else:
                    # 这里可以添加对其他TCP响应的处理
                    #print(Fore.YELLOW + f"Port {dst_port} is unfiltered")
                    return "unexpected"
    else:
        with print_lock:
            print(Fore.BLUE + f"Port {dst_port} is filtered")
        return "no_response"




def portscan_of_udp_send(src_ip, src_port, dst_ip, dst_port,retries=3):
    # 设置源IP和目标IP
    ip = IP(src=src_ip, dst=dst_ip)
    # 构造空的UDP数据包
    udp = UDP(dport=dst_port)
    # 组合IP和UDP数据包
    packet = ip / udp

    # 初始化结果
    result = None

    # 发送数据包并重试retries次
    for _ in range(retries):
        # 发送数据包并等待响应
        answered = sr1(packet, timeout=1, verbose=0)

        if answered is not None:
            if answered.haslayer(ICMP):
                icmp_type = answered[ICMP].type
                icmp_code = answered[ICMP].code
                if icmp_type == 3:  # ICMP类型3表示目的不可达
                    if icmp_code == 3:  # 端口不可达，端口关闭
                        result = "closed"
                        break
                    elif icmp_code in [1, 2, 9, 10, 13]:  # 其他ICMP不可到达错误，端口被过滤
                        result = "filtered"
                        break

            elif answered.haslayer(UDP):
                result = "open"
                break


                        # 如果没有收到任何响应或明确的关闭/过滤响应，保持初始结果
    if result is None:
        result = "open|filtered"

    with print_lock:
        if result == filter or result == "open|filtered" or result == "open":
            print(Fore.BLUE + f"Port {dst_port} is {result}")




def portscan_of_syn(src_ip, src_port, dst_ip, dst_port1, dst_port2, thread):
    # 获取mac地址
    # if get_mac(dst_ip) == -1:
    # print("The target IP address is not online")
    # return -1
    # 循环发送测试
    with concurrent.futures.ThreadPoolExecutor(max_workers=thread) as executor:
        futures = [executor.submit(portscan_of_syn_send, src_ip, src_port, dst_ip, dst_port)
                   for dst_port in range(dst_port1, dst_port2 + 1)]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()


def portscan_of_ack(src_ip, src_port, dst_ip, dst_port1, dst_port2, thread):
    # 获取mac地址
    # if get_mac(dst_ip) == -1:
    # print("The target IP address is not online")
    # return -1
    # 循环发送测试
    with concurrent.futures.ThreadPoolExecutor(max_workers=thread) as executor:
        futures = [executor.submit(portscan_of_ack_send, src_ip, src_port, dst_ip, dst_port)
                   for dst_port in range(dst_port1, dst_port2 + 1)]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()


def portscan_of_udp(src_ip, src_port, dst_ip, dst_port1, dst_port2, thread):
    # 获取mac地址
    # if get_mac(dst_ip) == -1:
    # print("The target IP address is not online")
    # return -1
    # 循环发送测试
    with concurrent.futures.ThreadPoolExecutor(max_workers=thread) as executor:
        futures = [executor.submit(portscan_of_udp_send, src_ip, src_port, dst_ip, dst_port)
                   for dst_port in range(dst_port1, dst_port2 + 1)]
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
























































