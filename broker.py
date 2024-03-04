import socket

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
        available_servers[client_address] = server_info
        print(f"Registered server: {client_address}")
        
    # Client request
    elif data == b'REQUEST_SERVER': 
        if available_servers:      
            for server_address, server_info in available_servers.items():
                print(server_address)
                discovery_socket.sendto(server_info.encode('utf-8'), client_address)
        else:
            discovery_socket.sendto(b'NO_SERVERS_AVAILABLE', client_address)
