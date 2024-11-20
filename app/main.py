import socket  # noqa: F401
import threading

from parser.index import parse_command
from parser.classes import RedisCommand
from redis_resp_utils import format_simple_string, format_bulk_string

def handle_connection (connection: socket.socket):
    while True:
        data = connection.recv(1024)
        
        if not data:
            return
                
        command: RedisCommand = parse_command(data)

        store = dict()

        match (command.getCommand().lower()):
            case "echo":
                connection.sendall(format_simple_string(command.getArgs()[0]))
            case "ping":
                connection.sendall(format_simple_string("PONG"))
            case "set":
                key = command.getArgs()[0]
                value = command.getArgs()[1]

                store[key] = value

                connection.sendall(format_simple_string("OK"))
            case "get":
                key = command.getArgs()[0]
                value: str = store[key]

                connection.sendall(format_bulk_string(value))


def main():
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)

    while True:
        connection, _ = server_socket.accept()
        thread = threading.Thread(target=handle_connection, args=[connection])
        thread.start()


if __name__ == "__main__":
    main()
