from typing import List
from classes import *

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

def parse_command (data: str) -> RedisCommand:
    token = parse_to_token(data)

    if token.getType() == RedisValues.ARRAY:
        children = token.getValue()

        command = children[0].getValue() if len(children) >= 1 and isinstance(children[0], RedisString) else "" 
        args = children[1].getValue() if len(children) >= 2 and isinstance(children[1], RedisString) else "" 

        return RedisCommand(command, args)
    
    elif token.getType() == RedisValues.STRING:
        command = token.getValue()

        return RedisCommand(command)
    
    else:
        print("something went wrong")
        return RedisCommand()
        