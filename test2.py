import socket

# 创建UDP socket
udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# 绑定端口，这里的端口号可以根据需要更改
port = 998
udp_socket.bind(('', port))

print(f"UDP Port {port} is now listening.")

# 循环以接收数据
while True:
    data, addr = udp_socket.recvfrom(1024)  # Buffer size is 1024 bytes
    print(f"Received message: {data} from {addr}")