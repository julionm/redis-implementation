from typing import List
from functools import reduce

def encode_simple_string (response: str) -> str:
    return "+{arg}\r\n".format(arg=response)

def encode_bulk_string (response: str) -> str:
    if len(response) == 0:
        return "$-1\r\n"

    return "${}\r\n{}\r\n".format(len(response), response)

def format_simple_string (data: str) -> bytes:
    return bytes(encode_simple_string(data), "utf-8")

def format_bulk_string (data: str) -> bytes:
    return bytes(encode_bulk_string(data), "utf-8")

def format_bulk_array (data: List[str]) -> str:
    return bytes(reduce(lambda acc, cur: acc + cur, data, f"${len(data)}\r\n"), "utf-8")
