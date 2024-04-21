import JangTokens as jt
import string

identStart = string.ascii_letters
identChars = string.ascii_letters + "_" + string.digits
breakCharacters = ["(", ")", '"', "{", "}", "[", "]", "'", ";", ":"]

class Lexer:
    def __init__(self):
        self.words = []
        
    def wordSplit(self, filepath):
        text = open(filepath, 'r').read()
        tokens = []
        temptext = ""
        inStringLit = False
        for char in text:
            if inStringLit:
                if char == '"':
                    tokens.append(temptext)
                    tokens.append('"')
                    temptext = ""
                    inStringLit = False
                    continue
                temptext += char
            else:
                if char == '"':
                    inStringLit = True
                    if temptext != "":
                        tokens.append(temptext)
                        temptext = ""
                    tokens.append(char)
                    continue
                if char in string.whitespace:
                    continue
                if char in breakCharacters:
                    if temptext != "":
                        tokens.append(temptext)
                        temptext = ""
                    tokens.append(char)
                else:
                    temptext += char
                    if temptext in jt.tokens.keys():
                        tokens.append(temptext)
                        temptext = ""
        self.words = tokens
    
    def defineTokens(self):
        tokens = []
        index = 0
        while index < len(self.words):
            word = self.words[index]
            type = jt.getType(word)
            if type == "kwdTag":
                index += 2
                type = jt.getType(self.words[index-1])
                tokens.append(Token("julio " + self.words[index-1], type))
                if type == "FUNC_DEC":
                    index += 1
                    type = jt.getType(self.words[index-1])
                    tokens.append(Token(self.words[index-1], type))
                    index += 1
                    type = jt.getType(self.words[index-1])
                    tokens.append(Token(self.words[index-1], "FUNC_NAME"))
                continue
            
            if type == "STRINGDEF":
                tokens.append(Token('"', "STRINGDEF"))
                tokens.append(Token(self.words[index+1], "STRING_LITERAL"))
                tokens.append(Token('"', "STRINGDEF"))
                index += 3
                continue
            tokens.append(Token(self.words[index], type))
            index += 1
        self.tokens = tokens
        
    def tokenize(self, filepath):
        self.wordSplit(filepath)
        print(self.words)
        self.defineTokens()
        for token in self.tokens:
            print(token.type, end=", ")
            print(token.value)

class Token:
    def __init__(self, value, Type):
        self.value = value
        self.type = Type
        
lexer = Lexer()
lexer.tokenize("LexerTest.jang")