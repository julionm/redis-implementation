import socket  # noqa: F401
import threading
from enum import Enum
from typing import List

class RedisValues (Enum):
    ARRAY = 1
    STRING = 1

class RedisToken:
    def setValue (self, value):
        pass

    def setSize (self, size):
        pass

    def setType (self, type):
        pass

    def getValue (self):
        pass

    def getSize (self):
        pass

    def getType (self):
        pass


class RedisArray(RedisToken):

    value = []
    size = 0
    type = RedisValues.ARRAY

    def __init__ (self, value=[], size=0):
        self.value = value
        self.size = size

    def getValue (self) -> List[RedisToken]:
        return self.value

    def getSize (self):
        return self.size

    def getType (self):
        return self.type

    def setValue(self, value: list):
        self.value = value

    def setSize (self, size):
        self.size = size

    def setType (self, type: RedisValues):
        self.type = type
    
    def addChildren (self, child: RedisToken):
        self.value.append(child)


class RedisString(RedisToken):

    value = ""
    size = 0
    type = RedisValues.STRING

    def __init__ (self, value="", size=0):
        self.value = value
        self.size = size

    def getValue (self) -> str:
        return self.value

    def getSize (self):
        return self.size
    
    def getType (self):
        return self.type

    def setValue(self, value: str):
        self.value = value

    def setSize (self, size):
        self.size = size

    def setType (self, type: RedisValues):
        self.type = type


class RedisCommand:
    command = ""
    arg = ""

    def __init__ (self, command: str = "", arg: str = ""):
        self.command = command
        self.arg = arg

    def getCommand (self):
        return self.command
    
    def getArg (self):
        return self.arg


def parse_redis_bulk_string (chunks: List[str]) -> tuple[RedisToken, List[str]] | None:
    if chunks[0].startswith("*"):
        # ? *2\r\n$5\r\nECHO\r\nhello\r\n
    
        array_size = int(chunks[0][1:])

        token = RedisArray(size=array_size)

        remaining_str = chunks[1:]

        for _ in range(array_size):
            (child_token, rest) = parse_redis_bulk_string(remaining_str)

            remaining_str = rest

            if child_token == None:
                break
            
            token.addChildren(child_token)

        # * chunks[1] -> chunks[n] = arguments

        return (token, remaining_str)

    elif chunks[0].startswith("$"):
        # ? $4\r\nPING\r\n
        buffer_size = int(chunks[0][1:])

        token = RedisString(size=buffer_size)

        if buffer_size > 0:
            token.setValue(chunks[1])

        return (token, chunks[2:])

    else:
        return (None, chunks[1:])

def parse_to_token (data: bytes) -> RedisToken:
    encoded_data = data.decode("UTF-8")
    chunks = encoded_data.split("\r\n")

    (token, remaining_chunks) = parse_redis_bulk_string(chunks)

    if len(remaining_chunks) == 0:
        print("parsing was completed")
    else:
        print("there's still some stuff to parse: {}", remaining_chunks)

    return token

def parse_command (token: RedisToken) -> RedisCommand:
    if token.getType() == RedisValues.ARRAY:
        children = token.getValue()

        command = children[0].getValue() if len(children) >= 1 and isinstance(children[0], RedisString) else "" 
        arg = children[1].getValue() if len(children) >= 2 and isinstance(children[1], RedisString) else "" 

        return RedisCommand(command, arg)
    
    elif token.getType() == RedisValues.STRING:
        command = token.getValue()

        return RedisCommand(command)
    
    else:
        print("something went wrong")
        return RedisCommand()
    
def handle_connection (connection: socket.socket):
    while True:
        data = connection.recv(1024)
        
        if not data:
            return
                
        command: RedisCommand = parse_command(parse_to_token(data))

        match (command.getCommand().lower()):
            case "echo":
                print("the sender sent an echo")
                response = "+{arg}\r\n"
                connection.sendall(bytes(response.format(arg=command.getArg()), "utf-8"))
            case "ping":
                print("the sender sent a ping")
                connection.sendall(b"+PONG\r\n")

def main():
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)

    while True:
        connection, _ = server_socket.accept()
        thread = threading.Thread(target=handle_connection, args=[connection])
        thread.start()


if __name__ == "__main__":
    main()
