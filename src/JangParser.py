import JangLexer as JL
from JangStructs import *
from JangTokens import J_TOKENS 

class JangParser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.tokens = []
        self.current_token_index = 0

        self.variables = {}
        self.functions = {}
        self.classes = {}
        self.ast = []
    
    def advance(self):
        self.current_token_index += 1
        if self.current_token_index < len(self.tokens):
            return self.tokens[self.current_token_index]
        return None
    
    def parse_tokens(self, tokens):
        self.tokens = tokens
        self.current_token_index = 0
        while self.current_token_index < len(tokens):
            token = self.tokens[self.current_token_index]
            if token.type == 'NEWLINE' or token.type == 'EOF':
                self.advance()
            if token.type == "FUNC_DCL":
                self.parse_function_declaration()
            if token.type == "VAR_DCL":
                self.parse_var_declaration()
                
    
    def parse_function_declaration(self, c_body = None, method = False):
        returnType = self.advance().value
        name = self.advance().value
        if self.advance().type != 'LPAREN':
            raise RuntimeError('Expected LPAREN after function name')
        nextToken = self.advance()
        if nextToken.type == "RPAREN":
            args = []
        else:
            args = self.parse_arguments()
        f_body = self.parse_body()
        self.functions[name] = {
            'return_type': returnType,
            'args': args,
            'body': f_body 
        }
        # add function to the AST
        if method and c_body != None:
            c_body.append(JangFunction(name, returnType, args, f_body, 4))
        else:
            self.ast.append(JangFunction(name, returnType, args, f_body, 2))
 
    
    def parse_arguments(self):
        args = []
        while self.tokens[self.current_token_index].type != 'RPAREN':
            typetoken = self.advance()
            if typetoken.type == "ARRAY" or typetoken.type == "TYPE":
                argtype = typetoken.type
            else:
                raise RuntimeError("Expected argument type")
            argident = self.advance()
            if argident is None or argident.type != 'IDENTIFIER':
                raise RuntimeError(f'Expected variable name, got {argident.type if name_token else "None"}')
            args.append(JangArgs(argtype, argident.value))
            self.advance()  # Consume COMMA or RPAREN
            if self.tokens[self.current_token_index].type == 'COMMA':
                self.advance()  # Consume COMMA
        self.advance()  # Consume RPAREN
        return args
    
    def parse_var_declaration(self, body = None):
        type = self.advance().value
        print(type)

if __name__ == '__main__':
    lexer = JL.JangLexer()
    parser = JangParser(lexer)
    text = 'make int[] x;'
    tokens = lexer.tokenize(text)
    parser.parse_tokens(tokens)
    # print(parser.variables)
    # text = 'change x[4] to 20;'
    # tokens = lexer.tokenize(text)
    # print(tokens)
    # parser.parse_tokens(tokens)
    # print(parser.variables)

    # text = 'julio wants int add(int x, int y) { make int z be x ; }'
    # tokens = lexer.tokenize(text)
    # parser.parse_tokens(tokens)

    # print the AST
    for code in parser.ast:
        print(code)