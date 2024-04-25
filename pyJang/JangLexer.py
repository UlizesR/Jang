from JangTokens import J_TOKENS

import re

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

        # print(self.compile_tk)

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
                    # if the token is TAB or NEWLINE, do nothing
                    if token == 'TAB':
                        pass
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
                raise RuntimeError(f'Invalid token: line {line_number} column {self.pos}')
        return self.tokens