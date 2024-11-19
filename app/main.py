import socket  # noqa: F401
import threading
import concurrent.futures

def create_connection_reader (connection):
    def handle_read ():
        while True:
            data = connection.recv(1024)
            
            if not data:
                return
                    
            connection.sendall(b"+PONG\r\n")

    return handle_read

def main():
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)

    pool = concurrent.futures.ThreadPoolExecutor(max_workers=2)

    while True:
        connection, _ = server_socket.accept()

        pool.submit(create_connection_reader(connection))


if __name__ == "__main__":
    main()
