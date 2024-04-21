from JangLexer import JangLexer as JL
from JangStructs import *
from JangTokens import J_TOKENS 

class Cursor:
    def __init__(self, tokens):
        self.tokens = tokens
        self.numTokens = len(tokens)
        self.index = 0

    def isTokensLeft(self):
        return self.index < self.numTokens
    
    def getToken(self):
        return self.tokens[self.index]

    def advanceToken(self):
        self.index += 1
        if self.isTokensLeft():
            return self.tokens[self.index]
        return None


class JangParser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.cursor = Cursor

        self.variables = {}

    def Parse(self, tokens):
        self.cursor = Cursor(tokens)
        while self.cursor.isTokensLeft():
            token = self.cursor.getToken()
            if token.type == 'NEWLINE' or token.type == 'EOF':
                self.cursor.advanceToken()
            if token.type == 'FUNC_DCL':
                # self.parse_function_declaration()
                pass
            elif token.type == 'IMPORT':
                # self.parse_import_statement()
                pass
            elif token.type == 'VAR_DCL':
                self.parseVariableDeclaration()
            elif token.type == 'VAR_CHANGE':
                # self.parse_variable_change()
                pass
            elif token.type == 'RETURN':
                # self.parse_return_statement()
                pass
            elif token.type == 'PRINT':
                # self.parse_print_statement()
                pass
            elif token.type == 'CLASS':
                # self.parse_class_declaration()
                pass
            elif token.type == 'IDENTIFIER':
                # if the first token is an identifier, its most likely a function call
                # self.parse_function_call()
                pass
            elif token.type == 'IF':
                # self.parse_conditional()
                pass
            else:
                self.cursor.advanceToken()  # Move past unrecognized tokens

    def parseVaribleDeclaration(self, body):
        type_ = self.cursor.advanceToken().value
        nextToken = self.cursor.advanceToken()
        if nextToken.type == 'THIS':
            name = self.cursor.advanceToken().value
        else:
            name = nextToken.value

        if self.cursor.advanceToken().value != 'be':
            raise RuntimeError('Expected "be" in variable declaration')
        
        value = self.cursor.advanceToken().value
        self.variables[name] = (type_, value)