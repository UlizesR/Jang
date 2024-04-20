import re 
from JangTokens import J_TOKENS

class JangTokens:
    def __init__(self, type_, value=None, pos=None):
        self.type = type_
        self.value = value
        self.pos = pos
    
    def __repr__(self):
        if self.value: return f'{self.type}: {self.value}'
        return f'{self.type}'

class JangLexer:
    # Initialize the lexer
    def __init__(self):
        self.pos = 0                # current position in the text
        self.current_tk = None      # current token being processed
        self.tokens = []            # list of tokens

        # compile the regular expressions for each token
        self.compile_tk = {tok: re.compile(regex) for tok, regex in J_TOKENS.items()}

    # Tokenize a given text
    def tokenize(self, text, line_number=1):
        self.tokens = []        # reset the list of tokens
        self.pos = 0            # reset the position

        # loop through the text
        while (self.pos < len(text)):
            match = None        # match for the current token

            # loop through the tokens
            for token, regex in self.compile_tk.items():
                # match the token
                match = regex.match(text, self.pos)
                # if a match is found
                if match:
                    # get the value of the token
                    value = match.group(0)
                    # check the token type
                    # if the token is SKIP, do nothing
                    if token == 'SKIP':
                        pass
                    # if the token is NEWLINE, add a newline token
                    elif token == 'NEWLINE':
                        self.tokens.append(JangTokens('NEWLINE'))
                    # if the token is EOF, add an EOF token
                    elif token == 'EOF':
                        self.tokens.append(JangTokens('EOF'))
                    # if the token is MISMATCH, raise an error
                    elif token == 'MISMATCH':
                        raise RuntimeError(f'Token {value} not recognized: line {line_number} column {self.pos}')
                    # otherwise, add the token to the list of tokens
                    else:
                        self.tokens.append(JangTokens(token, value, self.pos))
                    # update the position
                    self.pos = match.end(0)
                    break
            if not match:
                # if no match is found, raise an error
                raise RuntimeError(f'Could not match any token at position {self.pos}')
        return self.tokens
    
    def __repr__(self):
        return f'{self.tokens}'
    
# test the lexer
if __name__ == '__main__':
    lexer = JangLexer()
    # text = 'make int x be 10;'
    # tokens = lexer.tokenize(text)
    # print(tokens)
    # text = 'is (x < 10) fr { julio says yuh; }'
    # tokens = lexer.tokenize(text)
    # print(tokens[0].type, tokens[0].value, tokens[0].pos)

    text = "julio says \"Hello, World!\";"
    tokens = lexer.tokenize(text)
    if tokens[0].type == 'PRINT':
        # remove the "" from the string value and print it
        print(tokens[1].value[1:-1])