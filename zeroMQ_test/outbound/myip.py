import socket

host_name = socket.gethostname()
print(host_name)

host_ip = socket.gethostbyname(host_name)
print(host_ip)

socket_open = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_open.connect(('www.google.co.kr', 443))
inner_ip = socket_open.getsockname()[0]
print(inner_ip)