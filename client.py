import socket
import threading

def handle_server_messages(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            print(message)
            if message == 'quit':
                client.close()
                break
        except:
            break

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect(('localhost', 8888))

    print('Digite "quit" para terminar o chat')

    while True:
        try:
            handle_thread = threading.Thread(target=handle_server_messages, args=[client])
            handle_thread.start()
            client.send(input('Mensagem: ').encode('utf-8'))

        except:
            break
    try:
        client.close()
    except:
        exit(0)

if __name__ == "__main__":
    main()