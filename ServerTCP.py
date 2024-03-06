import socket
import threading

client_connections = []

def handle_client(connection, client_address):
    print(f"Connection established with {client_address}")
    client_connections.append(connection)
    
    size = len(client_connections)
    print(size)
    if size == 1:
        connection.send(b'FIRST_TO_CONNECT')
        print("Enviou Mensagem 1")
    
    while size < 2:
        size = len(client_connections)
        
    connection.send(b'START_GAME')    
    
    try:
        while True:
            data = connection.recv(1024)
            if data:
                print(f"Received data: {data}")
                for connec in client_connections:
                    if connec != connection:
                        connec.send(data)
            else:
                break
    except Exception as exception:
        print(f"Something wrong with {client_address}: {exception}")
    finally:
        client_connections.remove(connection)
        connection.close()
    
# socket TCP (server)
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('0.0.0.0', 1100)
tcp_socket.bind(server_address)
tcp_socket.listen(2) #  Number of conections for listen

# brocker register
discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
discovery_address = ('192.168.0.7', 1050) ## Real broker address
discovery_socket.sendto(b'REGISTER_SERVER', discovery_address)

print("Registering with the broker")
print("TCP server started and waiting for connections...")

while True:
    connection, client_address = tcp_socket.accept()
    client_thread = threading.Thread(target=handle_client, args=(connection, client_address))
    client_thread.start()
