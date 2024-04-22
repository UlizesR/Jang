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
        while self.current_token_index < len(self.tokens):
            token = self.tokens[self.current_token_index]
            if token.type == 'NEWLINE' or token.type == 'EOF':
                self.advance()
            if token.type == 'FUNC_DCL':
                self.parse_function_declaration()
            elif token.type == 'IMPORT':
                self.parse_import_statement()
            elif token.type == 'VAR_DCL':
                self.parse_variable_declaration()
            elif token.type == 'VAR_CHANGE':
                self.parse_variable_change()
            elif token.type == 'RETURN':
                self.parse_return_statement()
            elif token.type == 'PRINT':
                self.parse_print_statement()
            elif token.type == 'CLASS':
                self.parse_class_declaration()
            elif token.type == 'IDENTIFIER':
                # if the first token is an identifier, its most likely a function call
                self.parse_function_call()
            elif token.type == 'IF':
                self.parse_conditional()
            else:
                self.advance()  # Move past unrecognized tokens

    def parse_function_call(self):
        """Parse a function call."""
        name = self.tokens[self.current_token_index].value
        if self.tokens[self.current_token_index + 1].type != 'LPAREN':
            raise RuntimeError('Expected LPAREN after function name')
        if self.tokens[-1].type != 'RPAREN':
            raise RuntimeError('Expected RPAREN at the end of the function call')
        if name not in self.functions:
            raise RuntimeError(f'Function {name} does not exist')
        self.ast.append(JangFunctionCall(name))
        
    def parse_conditional(self):
        """Parse a conditional statement."""
        self.advance()  # Consume ( token
        condition = self.parse_expression(tok_type_check='RPAREN', tok_to_check=')')
        if self.advance().type != 'FR':
            raise RuntimeError('Expected FR after conditional')
        body = self.parse_body()
        else_body = self.parse_body() if self.tokens[self.current_token_index].type == 'ELSE' else None
        self.ast.append(JangConditional(condition, body, else_body, 4))

    def parse_function_declaration(self, c_body = None, method = False):
        # print(self.advance().value)  # Assume FUNC_DCL token is consumed before calling
        return_type = self.advance().value
        name = self.advance().value
        if self.advance().type != 'LPAREN':
            raise RuntimeError('Expected LPAREN after function name')
        next_token = self.advance()
        if next_token.type == 'RPAREN':
            args = []
        else:
            args = self.parse_arguments()
        f_body = self.parse_body()
        self.functions[name] = {
            'return_type': return_type,
            'args': args,
            'body': f_body 
        }
        # add function to the AST
        if method and c_body != None:
            c_body.append(JangFunction(name, return_type, args, f_body, 4))
        else:
            self.ast.append(JangFunction(name, return_type, args, f_body, 2))

    def parse_class_declaration(self):

        # Actual class parsing logic
        name = self.advance().value
        self.advance()  # Consume LBRACE

        c_body = []

        while self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index].type != 'RBRACE':
            next_tok = self.advance()
            if next_tok is None:
                raise RuntimeError(f'next_tok is None, prev token: {self.tokens[self.current_token_index - 1].type}')
            if next_tok.type == 'FUNC_DCL':
                self.parse_function_declaration(c_body, True)
            # else:
                # self.advance()
        self.advance()  # Consume RBRACE

        # add class to the classes dictionary
        self.classes[name] = c_body
        # add class to the AST
        self.ast.append(JangClass(name, c_body))

    def parse_arguments(self):
        args = []
        while self.tokens[self.current_token_index].type != 'RPAREN':
            type_token = self.tokens[self.current_token_index]
            if type_token is None or type_token.type != 'TYPE':
                raise RuntimeError(f'Expected type, got {type_token.type if type_token else "None"}')
            name_token = self.advance()
            if name_token is None or name_token.type != 'IDENTIFIER':
                raise RuntimeError(f'Expected variable name, got {name_token.type if name_token else "None"}')
            args.append(JangArgs(type_token.value, name_token.value))
            self.advance()  # Consume COMMA or RPAREN
            if self.tokens[self.current_token_index].type == 'COMMA':
                self.advance()  # Consume COMMA
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
            elif token.type == 'PRINT':
                self.parse_print_statement(body, True)
            elif token.type == 'RETURN':
                self.parse_return_statement(body)
            elif token.type == 'IF':
                self.parse_conditional(True)

            else:
                self.advance()  # Move past unrecognized tokens
            #     print(self.tokens[self.current_token_index].type)
            # print(self.tokens[self.current_token_index].value)
        self.advance()  # Consume RBRACE
        return body

    def parse_import_statement(self):
        self.advance()  # Consume IMPORT token
        # Actual import parsing logic

    def parse_return_statement(self, body = None):
        # Actual return parsing logic
        expr = self.parse_expression(tok_type_check='SEMICOLON', tok_to_check=';')
        value = expr
        if body != None:
            body.append(f"return {value}")

    def parse_print_statement(self, body = None, block = False):
        # Actual print parsing logic
        expr = self.parse_expression(block, 'SEMICOLON', ';')
        value = expr
        if body != None:
            body.append(f"print({value})")
        if not block:
            # add the body to the AST
            self.ast.append(JangPrint(value))

    def parse_expression(self, block = None, tok_type_check = None, tok_to_check = None):
        # Actual expression parsing logic
        expr = []
        expr_s = ''
        while self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index].type != tok_type_check:
            tok = self.advance()
            if tok.value == tok_to_check:
                continue
            expr_s += tok.value
        expr.append(expr_s)
        return expr
    
    def parse_variable_declaration(self, body = None):
        type_ = self.advance().value
        next_tok = self.advance()
        if next_tok.type == 'THIS':
            name = self.advance().value
        else:
            name = next_tok.value
        if self.advance().value != 'be':
            raise RuntimeError('Expected "be" in variable declaration')
        expr = self.parse_expression()
        value = expr 
        # if self.advance().type != 'SEMICOLON':
        #     raise RuntimeError('Expected SEMICOLON at the end of the variable declaration')
        self.variables[name] = (type_, value)
        if body != None:
            body.append(f"{type_} {name} = {value}")

    def parse_variable_change(self, body = None):
        name = self.advance().value
        next_tok = self.advance()
        if next_tok.type == 'THIS':
            name = self.advance().value
        else:
            name = next_tok.value
        if name not in self.variables:
            raise RuntimeError('Variable not declared')
        if self.advance().value != 'to':
            raise RuntimeError('Expected "to" in variable change')
        expr = self.parse_expression()
        value = expr 
        # if self.advance().type != 'SEMICOLON':
        #     raise RuntimeError('Expected SEMICOLON at the end of the variable change')
        self.variables[name] = (self.variables[name][0], value)
        if body != None:
            body.append(f"{name} = {value}")


# test the parser
if __name__ == '__main__':
    lexer = JL.JangLexer()
    parser = JangParser(lexer)

    text = """is (True == yuh) fr {
            julio says "Hello World";
            julio says "Goodbye World";
        } otherwise {
            julio says "Goodbye World";
        }

    """
    tokens = lexer.tokenize(text)
    parser.parse_tokens(tokens)

    # print the AST
    for code in parser.ast:
        print(code)