import JangLexer as JL
from JangStructs import * 

class JangParser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = []
        self.current_token_index = 0

        self.variables = {}
        self.functions = {}
        self.classes = {}

    def advance(self):
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            return self.tokens[self.current_token_index]
        return None

    def parse_tokens(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        while self.current_token_index < len(self.tokens):
            token = self.tokens[self.current_token_index]
            if token.type == 'FUNC_DCL':
                self.parse_function_declaration()
            elif token.type == 'IMPORT':
                self.parse_import_statement()
            elif token.type == 'VAR_DCL':
                self.parse_variable_declaration()
            elif token.type == 'VAR_CHANGE':
                self.parse_variable_change()
            elif token.type == "WHILE":
                self.parse_while_loop()
            elif token.type == "FOR":
                self.parse_for_loop()
            else:
                self.advance()  # Move past unrecognized tokens

    def parse_function_declaration(self):
        # print(self.advance().value)  # Assume FUNC_DCL token is consumed before calling
        return_type = self.advance().value
        name = self.advance().value
        if self.advance().type != 'LPAREN':
            raise RuntimeError('Expected LPAREN after function name')
        args = self.parse_arguments()
        body = self.parse_body()
        self.functions[name] = {
            'return_type': return_type,
            'args': args,
            'body': body
        }

    def parse_arguments(self):
        args = []
        while self.tokens[self.current_token_index].type != 'RPAREN':
            type_ = self.advance().value
            name = self.advance().value
            args.append((name, type_))
            comma = self.advance()
            if comma is None:
                raise RuntimeError('Expected Comma')
        self.advance()  # Consume RPAREN
        return args
    
    def parse_body(self):
        body = []
        while self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index].type != 'RBRACE':
            token = self.tokens[self.current_token_index]
            if token.type == 'VAR_DCL':
                self.parse_variable_declaration(body)
            elif token.type == 'VAR_CHANGE':
                self.parse_variable_change(body)
            else:
                self.advance()  # Move past unrecognized tokens
        self.advance()  # Consume RBRACE
        return body

    def parse_import_statement(self):
        self.advance()  # Consume IMPORT token
        # Actual import parsing logic

    def parse_return_statement(self):
        # Actual return parsing logic
        pass

    def parse_print_statement(self, body = None):
        # Actual print parsing logic
        while self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index].type != 'SEMICOLON':
            self.advance()

    def parse_expression(self):
        # Actual expression parsing logic
        expr = []
        while self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index].type != 'SEMICOLON':
            if self.advance().type == 'IDENTIFIER':
                expr.append(self.tokens[self.current_token_index].value)
            else:
                expr.append(self.tokens[self.current_token_index].value)

    def parse_variable_declaration(self, body = None):
        type_ = self.advance().value
        arrCheck = self.advance()
        if arrCheck.type == "LBRACKET":
            type_ += "Array"
            if self.advance().type != "RBRACKET":
                raise RuntimeError('Missing close bracket')
            name = self.advance().value
            nt = self.advance()
            if nt.type != "RBRACKET":
                if nt.type != "SEMICOLON":
                    raise RuntimeError("Either create an empty array or assign to a hardcoded array!")
        else:
            name = arrCheck.value
        beCheck = self.advance()
        if beCheck.value != 'be':
            raise RuntimeError('Expected "be" in variable declaration')
        value = self.advance().value
        if self.advance().type != 'SEMICOLON':
            raise RuntimeError('Expected SEMICOLON at the end of the variable declaration')
        self.variables[name] = (type_, value) 
        if body != None:
            body.append(f"{type_} {name} = {value}")

    def parse_variable_change(self, body = None):
        name = self.advance().value
        if name not in self.variables:
            raise RuntimeError('Variable not declared')
        if self.advance().value != 'to':
            raise RuntimeError('Expected "to" in variable change')
        value = self.advance().value
        if self.advance().type != 'SEMICOLON':
            raise RuntimeError('Expected SEMICOLON at the end of the variable change')
        self.variables[name] = (self.variables[name][0], value)
        if body != None:
            body.append(f"{name} = {value}")

    def parse_while_loop(self, body = None):
        pass
    
    def parse_for_loop(self, body = None):
        forVar = self.advance().value
        if self.advance().value != 'in':
            raise RuntimeError('Expected "in" following temp variable declaration')
        # check for iterable value
            # Valid options: array, variable holding array
        iterator = self.advance()
        itVal = iterator.value
        itType = iterator.type
        pass
        

# test the parser
if __name__ == '__main__':
    lexer = JL.JangLexer()
    parser = JangParser(lexer)
    text = 'make int[] x;'
    tokens = lexer.tokenize(text)
    parser.parse_tokens(tokens)
    print(parser.variables)
    text = 'change x[4] to 20;'
    tokens = lexer.tokenize(text)
    print(tokens)
    parser.parse_tokens(tokens)
    print(parser.variables)

    text = 'julio wants int add(int x, int y) { make int z be x ; }'
    tokens = lexer.tokenize(text)
    parser.parse_tokens(tokens)
    print(parser.functions)
