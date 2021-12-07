class StackUnderflow(Exception):
    """Thrown on stack underflow"""
    pass

class StackOverflow(Exception):
    """Thrown on stack overflow"""
    pass

class ParserUnknownCommand(Exception):
    """Thrown if Parser.errorOnUnknownCommand == True and command is unknown"""
    pass

class ParserError(Exception):
    """Thrown if Parser.parse encounters unknown error"""
    pass

def clamp(val, *, low = None, high = None):
    ret = val
    if(low != None):
        ret = max(low, ret)
    if(high != None):
        ret = min(high, ret)
    return ret

class Tape:
    """Tape module"""
    def __init__(self, *, length = 2048, autoAppend = True):
        self.tape = []
        for i in range(length):
            self.tape.append(0)
        self.autoAppend = autoAppend
        self.index = 0
        self.length = length
    def mov(self, offset):
        if(not self.autoAppend):
            self.index = clamp(low=0, high=self.length-1, val=self.index + offset)
        else:
            if(self.index + offset > self.length-1):
                for i in range((self.index + offset) - (self.length - 1)):
                    self.tape.append(0)
                    self.length += 1
                self.index = self.length-1;
            else:
                self.index = clamp(low=0, high=self.length-1, val=self.index + offset)
    def get(self):
        return self.tape[self.index]
    def set(self, val):
        self.tape[self.index] = val
    def getIndex(self):
        return self.index

class Stack:
    """Stack module"""
    def __init__(self, *, maxSize = 256, lifo=True):
        self.stack = []
        self.lifo = lifo
        self.maxSize = maxSize
    def push(self, *val):
        for i in val:
            if(len(self.stack)<self.maxSize):
                self.stack.append(i)
            else:
                raise StackOverflow()
    def pop(self):
        ret = 0
        try:
            if(not self.lifo):
                ret = self.stack.pop(0)
            else:
                ret = self.stack.pop()
        except IndexError:
            raise StackUnderflow()
        else:
            return ret

class Parser:
    """Parser module"""
    def __init__(self, commandDict, *, byLine = True, delim = '\n', argumentSeperator = " ", errorOnUnknownCommand = True):
        """commandDict has format {"command":functionReference}"""
        self.byLine = byLine
        self.delim = delim
        self.argSep = argumentSeperator
        self.eouc = errorOnUnknownCommand
        self.commandDict = commandDict
        self.parsedCommands = []
    def parse(self, command):
        if(self.byLine):
            parts = command.split(self.argSep)
            cmd = parts[0]
            args = parts[1:]
            try:
                self.parsedCommands.append({"cmd":self.commandDict[cmd], "args":args})
            except KeyError:
                if(self.eouc):
                    raise ParserUnknownCommand()
                else:
                    pass
            except:
                raise ParserError()
        else:
            for cmd in command:
                try:
                    self.parsedCommands.append(self.commandDict[cmd])
                except KeyError:
                    if(self.eouc):
                        raise ParserUnknownCommand()
                    else:
                        pass
                except:
                    raise ParserError()
    def parseFile(self, filename):
        try:
            with open(filename, "r") as file:
                data = file.read()
        except:
            raise ParserError()
        lines = data.split(self.delim)
        for line in lines:
            self.parse(line)
    def run(self):
        for cmd in self.parsedCommands:
            if(self.byLine):
                cmd["cmd"](cmd["args"])
            else:
                cmd()
