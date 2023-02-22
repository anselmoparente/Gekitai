import socket 

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect(('localhost', 8888))

finish = False
print('Digite "quit" para terminar o chat')

while not finish:
    client.send(input('Mensagem: ').encode('utf-8'))
    message = client.recv(1024).decode('utf-8')
    if message == 'quit':
        finish = True
    else:
        print(message)
    
client.close()
