import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind(('localhost', 8888))

server.listen()
client, address = server.accept()

finish = False 

while not finish:
    message = client.recv(1024).decode('utf-8')
    if message == 'quit':
        finish = True
    else:
        print(message)
    client.send(input('Mensagem: ').encode('utf-8'))

client.close()
server.close()
