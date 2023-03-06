import socket
import threading

class Client():
    def __init__(self):
        # Configurações de conexão
        HOST = 'localhost'
        PORT = 9000

        # Conecta ao servidor
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((HOST, PORT))

        # Função que lida com as mensagens recebidas do servidor
        def handle_server():
            while True:
                # Recebe a mensagem do servidor
                message = sock.recv(1024).decode('utf-8')

                # Imprime a mensagem
                print(message)

        # Inicia uma nova thread para lidar com as mensagens recebidas do servidor
        thread = threading.Thread(target=handle_server)
        thread.start()

        # Loop principal do cliente
        while True:
            # Lê a mensagem do usuário
            message = input()

            # Envia a mensagem para o servidor
            sock.sendall(message.encode('utf-8'))