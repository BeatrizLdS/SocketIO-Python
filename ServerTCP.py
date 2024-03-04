import socket

# socket TCP (server)
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('0.0.0.0', 1100)
tcp_socket.bind(server_address)
tcp_socket.listen(2) #  Number of conections for listen

print("TCP server started and waiting for connections...")

# brocker register
discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
discovery_address = ('0.0.0.0', 1050)
discovery_socket.sendto(b'REGISTER_SERVER', discovery_address)
print("Registering with the broker")

while True:
    connection, client_address = tcp_socket.accept()
    print(f"Connection established with {client_address}")   
    try:
        while True:
            data = connection.recv(1024)
            if data:
                print(f"Recebido: {data}")   
                connection.send(b'Mensagem que precisa ser enviada')
                # connection.close() - Cliente só recebe quando descomenta isso
    finally:
        print("Alguma coisa deu errado")
        connection.close()
    
# while True:
#     connection, client_address = tcp_socket.accept()
#     try:
#         print(f"Conexão estabelecida com {client_address}")
#         while True:
#             data = connection.recv(1024)
#             if data:
#                 # Processar os dados recebidos
#                 print(f"Recebido: {data}")
#                 connection.sendall(data) # Enviar os dados de volta ao cliente
#             else:
#                 break
#     finally:
#         connection.close()
