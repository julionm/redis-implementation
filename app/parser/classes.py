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
    args = []

    def __init__ (self, command: str = "", args: List[str] = []):
        self.command = command
        self.arg = args

    def getCommand (self):
        return self.command
    
    def getArgs (self):
        return self.args
