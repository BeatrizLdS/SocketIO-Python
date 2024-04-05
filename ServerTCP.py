import socket
import threading
from models.procedure import Procedure

class Server_TCP:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.client_connections = []
        self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.broker_address = ('0.0.0.0', 1050)
    
    def register_with_broker(self):
        discovery_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        discovery_socket.sendto(b'REGISTER_SERVER', self.broker_address)
        print("Registering with the broker")
        
    def start_server(self):
        self.tcp_socket.bind((self.host, self.port))
        self.tcp_socket.listen(2) # Number of conections for listen
        print("TCP server started and waiting for connections...")
        
        while True:
            connection, client_address = self.tcp_socket.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(connection, client_address))
            client_thread.start()
    
    def handle_client(self, connection, client_address):
        print(f"Connection established with {client_address}")
        self.client_connections.append(connection)

        size = len(self.client_connections)
        if size == 1:
            connection.send(b'FIRST_TO_CONNECT')
        
        # Loop for watting 2 players    
        while size < 2:
            size = len(self.client_connections)
            
        connection.send(b'START_GAME')    

        try:
            while True:
                data = connection.recv(1024)
                if data:
                    procedure = Procedure.decode(data)
                    result_for_local_user, result_for_remote_user = procedure.execute()
                    for connec in self.client_connections:
                        if connec == connection:
                            connec.send(result_for_local_user.encode('utf-8'))
                        else:
                            connec.send(result_for_remote_user.encode('utf-8'))
                            
                else:
                    break
        except Exception as exception:
            print(f"Something wrong with {client_address}: {exception}")
        finally:
            self.client_connections.remove(connection)
            connection.close()

if __name__ == "__main__":   
    server = Server_TCP('0.0.0.0', 1100)
    server.register_with_broker()
    server.start_server()      