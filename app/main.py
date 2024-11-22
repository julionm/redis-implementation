import socket  # noqa: F401
import threading
import time
import argparse
import sys

from app.redis_resp_utils import format_simple_string, format_bulk_string, format_bulk_array
from app.parser.index import parse_command
from app.parser.classes import RedisCommand

configuration = {}

def handle_connection (connection: socket.socket):
    store = dict()

    while True:
        data = connection.recv(1024)
        
        if not data:
            return
                
        command: RedisCommand = parse_command(data)

        match (command.getCommand().lower()):
            case "echo":
                connection.sendall(format_simple_string(command.getArgs()[0]))
            case "ping":
                connection.sendall(format_simple_string("PONG"))
            case "set":
                args = command.getArgs()
                
                key = args[0]
                value = args[1]

                expiry_date = float('inf')

                if len(args) > 2 and args[2].lower() == "px":
                    expiry_date = time.time() + float(args[3]) / 1000

                store[key] = {
                    "value": value,
                    "expiry_date": expiry_date 
                }
                
                connection.sendall(format_simple_string("OK"))
            case "get":
                key = command.getArgs()[0]
                res = store[key]
                value = res["value"] if res["expiry_date"] > time.time() else ""

                connection.sendall(format_bulk_string(value))
            case "config":
                args = command.getArgs()
                config_command = args[0]

                match (config_command.lower()):
                    case "get":
                        key = args[1]
                        value = ""

                        match (key):
                            case "dir":
                                value = configuration.dir
                            case "dbfilename":
                                value = configuration.dbfilename

                        connection.sendall(format_bulk_array([
                            format_bulk_string(key),
                            format_bulk_string(value)
                        ]))



def main():

    parser = argparse.ArgumentParser(
        prog="My Redis",
        description="Crafted using a redids",
        epilog="A program created by Julio Negri"
    )

    parser.add_argument("-dir", "--dir")
    parser.add_argument("-dbfilename", "--dbfilename")

    configuration = parser.parse_args(sys.argv[1:])

    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)

    while True:
        connection, _ = server_socket.accept()
        thread = threading.Thread(target=handle_connection, args=[connection])
        thread.start()


if __name__ == "__main__":
    main()
