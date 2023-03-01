import socket
import asyncio

async def handle_server_messages(client):
    try:
        message = await client.recv(1024).decode('utf-8')
        print(message)
        if message == 'quit':
            client.close()
    except:
        pass

async def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect(('localhost', 9000))

    print('Digite "quit" para terminar o chat')

    while True:
        try:
            client.send(input('Mensagem: ').encode('utf-8'))
            asyncio.ensure_future(handle_server_messages(client))
        except Exception as e:
            print(e)
            break
    try:
        client.close()
    except:
        exit(0)

if __name__ == "__main__":
    asyncio.run(main())