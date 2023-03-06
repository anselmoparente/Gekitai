import socket
import threading
import pickle

class Server():
    def __init__(self):
        # Configurações de conexão
        self.host = 'localhost'
        self.port = 9000

        self.clients = []
        self.clientsColors = ['red', 'blue']
        self.sock = []

        # Conecta ao servidor
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Vincula o socket ao endereço e porta
        self.sock.bind((self.host, self.port))

        # Espera por conexões
        self.sock.listen()

        # Lista de clientes conectados
        while True:
            # Aceita conexões de clientes
            if (len(self.clients) < 2):

                client_socket, client_address = self.sock.accept()

                if (len(self.clients) == 0): 
                    indexColor = 0
                else: 
                    indexColor = 1

                colorUser = self.clientsColors[indexColor]
                data = [colorUser, False, False]
                data_arr = pickle.dumps(data)

                print(f'Cliente conectado: {client_address}')

                client_socket.send(data_arr)

                # Inicia uma nova thread para lidar com a conexão do cliente
                thread = threading.Thread(target=self.handle_client, args=(client_socket, client_address))
                thread.start()
            else:
                break

    def handle_client(self, client_socket, client_address):
        # Adiciona o cliente à lista de clientes conectados
        self.clients.append(client_socket)

        # Loop principal do chat
        while True:
            # Recebe a mensagem do cliente
            message = client_socket.recv(1024)
            try:
                message = message.decode('utf-8')
            except:
                message = pickle.loads(message)
            
            if message[0] == False:
                buildArray = [False, message[1], message[2]]
                buildArray = pickle.dumps(buildArray)

            elif message[0] == 'quit':
                self.clients.remove(client_socket)
                client_socket.close()
                break
            
            # Envia a mensagem para todos os clientes conectados (exceto o remetente)
            for client in self.clients:
                if client != client_socket:
                    client.sendall(buildArray)

        print(f'Cliente desconectado: {client_address}')

if __name__ == "__main__":
    Server()