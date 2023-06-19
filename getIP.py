import socket

# Obtém o endereço IP do computador local
def get_local_ip():
    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    return ip_address

local_ip = get_local_ip()
print("Endereço IP do computador local:", local_ip)