import socket

def get_server_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Socket UDP
    s.connect(("8.8.8.8", 80))  # Connect to Google DNS Server
    server_ip = s.getsockname()[0]  # Get real local IP
    s.close()
    return server_ip

# Socket UDP
discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
discovery_address = ('0.0.0.0', 1050)
discovery_socket.bind(discovery_address)

available_servers = {}

print("Discovery server started...")

while True:
    data, client_address = discovery_socket.recvfrom(1024)
    
    # Server register
    if data == b'REGISTER_SERVER': 
        server_info = client_address[0]
        if server_info == '127.0.0.1':
            server_info = get_server_ip()
            available_servers[client_address] = server_info
            print(f"Registered server: {server_info}")
        else:
            available_servers[client_address] = server_info
            print(f"Registered server: {server_info}")
        
    # Client request
    elif data == b'REQUEST_SERVER': 
        if available_servers:      
            for server_address, server_info in available_servers.items():
                print(client_address)
                discovery_socket.sendto(server_info.encode('utf-8'), client_address)
        else:
            discovery_socket.sendto(b'NO_SERVERS_AVAILABLE', client_address)
