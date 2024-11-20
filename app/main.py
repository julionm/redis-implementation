import socket  # noqa: F401
import threading

from parser.index import parse_command
from parser.classes import RedisCommand
from redis_resp_utils import get_resp_formatting

def handle_connection (connection: socket.socket):
    while True:
        data = connection.recv(1024)
        
        if not data:
            return
                
        command: RedisCommand = parse_command(data)

        match (command.getCommand().lower()):
            case "echo":
                connection.sendall(get_resp_formatting(command.getArgs()[0]))
            case "ping":
                connection.sendall(get_resp_formatting("PONG"))
            case "set":
                key = command.getArgs()[0]
                value = command.getArgs()[1]
                connection.sendall(get_resp_formatting("OK"))

def main():
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)

    while True:
        connection, _ = server_socket.accept()
        thread = threading.Thread(target=handle_connection, args=[connection])
        thread.start()


if __name__ == "__main__":
    main()
