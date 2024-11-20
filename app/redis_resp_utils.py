def encode_resp_string (response: str) -> str:
    return "+{arg}\r\n".format(arg=response)

def get_resp_formatting (data: str) -> bytes:
    return bytes(encode_resp_string(data), "utf-8")
