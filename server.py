import socket
import threading

def listen(sock):
    sock.listen()

def accept_conn(sock):
    conn, address = sock.accept() 
    return conn, address

def handle_receive(conn, addr, conn_dict):
    while True:
        try:
            message = conn.recv(1024).decode("utf-8")
            for addr_conn in conn_dict.items():
                if addr_conn[0] != addr:
                    addr_conn[1].send(message.encode('utf-8'))
            if message == "quit":
                conn.close()
                break

            print(f"""Enviada por: {addr}/
                    Mensagem: {message}""")
        except:
            conn.close()
            break

def main():
    conn_dict = {}
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('localhost', 8888))
    listen(sock)
    try:
        while True:
            conn, addr = accept_conn(sock)
            conn_dict[addr] = conn
            print(f"Connection started from client address: {addr}")
            receive_thread = threading.Thread(target=handle_receive, args=[conn, addr, conn_dict])
            receive_thread.start()
    except KeyboardInterrupt:
        conn.close()
        sock.close()

if __name__ == "__main__":
    main()