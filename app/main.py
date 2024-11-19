import socket  # noqa: F401
import threading

def handle_connection (connection: socket.socket):
    while True:
        data = connection.recv(1024)
        
        if not data:
            return
                
        connection.sendall(b"+PONG\r\n")

def main():
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)

    while True:
        connection, _ = server_socket.accept()
        thread = threading.Thread(target=handle_connection, args=[connection])
        thread.start()


if __name__ == "__main__":
    main()
