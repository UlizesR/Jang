import JangNodes as jn
import JangLexer as jl
from JangTokens import J_TOKENS

class JangParser:
    def __init__(self, lexer):
        self.lexer = lexer  
        self.tokens = []
        self.ast = []

        self.functions = {}
        self.variables = {}
        self.classes = {}


    def advance(self):
        self.current_token_index += 1
        if self.current_token_index >= len(self.tokens):
            raise RuntimeError(f'Unexpected end of file at line {self.line_number}. Closing bracket or parenthesis may be missing.')
        return self.tokens[self.current_token_index]

    def parse_func(self):
        func_node = jn.JangFuncNode(self.tokens[self.current_token_index])
        self.expect_token_type('TYPE', func_node)
        self.expect_token_type('IDENTIFIER', 'function name', func_node)
        self.expect_token_type(expected_type='LPAREN', expected_tk='(')
        if self.current_token_index < len(self.tokens) and self.tokens[self.current_token_index].type != 'RPAREN':
            func_node.add_child(self.parse_param())
        # check that the current token is a RPAREN
        if self.current_token_index >= len(self.tokens) or self.tokens[self.current_token_index].type != 'RPAREN':
            raise RuntimeError(f'Expected a RPAREN at line {self.line_number} but None was found')
        if self.advance().type == 'NEWLINE':
            self.line_number += 1
        self.expect_token_type('LBRACE', '{')
        func_node.add_child(self.parse_body())
        # check that the current token is a RBRACE
        if self.current_token_index >= len(self.tokens) or self.tokens[self.current_token_index].type != 'RBRACE':
            raise RuntimeError("Expected a '}' at line {} but None was found".format(self.line_number))

        return func_node

    def parse(self, tokens):
        self.tokens = tokens
        self.line_number = 1
        self.current_token_index = 0

        while self.current_token_index < len(self.tokens):
            token = self.tokens[self.current_token_index]
            if token.type == 'FUNC':
                func_node = self.parse_func()
                self.ast.append(func_node)
            if token.type == 'NEWLINE':
                self.line_number += 1
                self.advance()
            self.current_token_index += 1
        # print(self.ast)

    def parse_func(self):
        func_node = jn.JangFuncNode(self.tokens[self.current_token_index])
        self.expect_token_type('TYPE', func_node)
        self.expect_token_type('IDENTIFIER', 'function name', func_node)
        self.expect_token_type(expected_type='LPAREN', expected_tk='(')
        if self.tokens[self.current_token_index].type != 'RPAREN':
            func_node.add_child(self.parse_param())
        # check that the current token is a RPAREN
        if self.tokens[self.current_token_index].type != 'RPAREN':
            raise RuntimeError(f'Expected a RPAREN at line {self.line_number} but None was found')
        if self.advance().type == 'NEWLINE':
            self.line_number += 1
        self.expect_token_type('LBRACE', '{')
        func_node.add_child(self.parse_body())
        # check that the current token is a RBRACE
        if self.tokens[self.current_token_index].type != 'RBRACE':
            raise RuntimeError("Expected a '}' at line {} but None was found".format(self.line_number))

        
        return func_node

    def parse_param(self):
        param_node = jn.JangParamNode(self.tokens[self.current_token_index])
        i = 1
        while self.tokens[self.current_token_index].type != 'RPAREN':
            if i % 3 == 0 and self.tokens[self.current_token_index].type == 'COMMA':
                self.expect_token_type('COMMA', ',')
            if self.tokens[self.current_token_index].type != 'LPAREN':
                param_node.add_child(jn.JangNodes(self.tokens[self.current_token_index]))
            self.advance()
            i += 1
        return param_node
    
    def parse_body(self):
        body_node = jn.JangBodyNode(self.tokens[self.current_token_index])
        while self.tokens[self.current_token_index].type != 'RBRACE':
            if self.tokens[self.current_token_index].type == 'PRINT':
                body_node.add_child(self.parse_print())
            elif self.tokens[self.current_token_index].type == 'VAR':
                body_node.add_child(self.parse_var_dcl())
            elif self.tokens[self.current_token_index].type == 'VAR_CHANGE':
                body_node.add_child(self.parse_var_change())
            elif self.tokens[self.current_token_index].type == 'RETURN':
                body_node.add_child(self.parse_ret())
            elif self.tokens[self.current_token_index].type == 'WHILE':
                body_node.add_child(self.parse_while())
            elif self.tokens[self.current_token_index].type == 'NEWLINE':
                self.line_number += 1
            self.advance()
        return body_node
    
    
    def parse_print(self):
        print_node = jn.JangPrintNode(self.tokens[self.current_token_index])
        self.advance()
        # advance to the next token until a ; is found
        while self.tokens[self.current_token_index].type != 'SEMICOLON':
            if self.tokens[self.current_token_index].type == 'NEWLINE':
                self.line_number += 1
                raise RuntimeError(f'Expected a ; at line {self.line_number} but None was found')
            # if self.tokens[self.current_token_index].type == 'IDENTIFIER':
            if self.tokens[self.current_token_index].type not in ['STRING_LITERAL', 'INT_LITERAL', 'FLOAT_LITERAL']:
                # self.advance()
                print(self.tokens[self.current_token_index])
                print_node.add_child(jn.JangNodes(self.parse_expression()))
            else:
                print_node.add_child(jn.JangNodes(self.tokens[self.current_token_index]))
                self.advance()
        return print_node
    
    def parse_var_dcl(self):
        var_node = jn.JangVarNode(self.tokens[self.current_token_index])
        self.expect_token_type('TYPE', 'variable type', var_node)
        # check if the next token is an identifier or an array
        if self.advance().type != 'ARRAY':
            var_node.add_child(jn.JangNodes(self.tokens[self.current_token_index]))
            self.expect_token_type('ASSIGN', 'be')
        else:
            var_node.add_child(jn.JangNodes(self.tokens[self.current_token_index]))
            self.advance()
        # advance to the next token until a ; is found
        while self.tokens[self.current_token_index].type != 'SEMICOLON':
            if self.tokens[self.current_token_index].type == 'NEWLINE':
                self.line_number += 1
                raise RuntimeError(f'Expected a ; at line {self.line_number} but None was found')

            self.advance()
            var_node.add_child(jn.JangNodes(self.parse_expression()))
        return var_node
    
    def parse_var_change(self):
        var_node = jn.JangVarNode(self.tokens[self.current_token_index])
        # check if the next token is an identifier or an array
        self.advance()
        var_node.add_child(jn.JangNodes(self.tokens[self.current_token_index]))
        self.expect_token_type('ASSIGN', 'to')
        while self.tokens[self.current_token_index].type != 'SEMICOLON':
            if self.tokens[self.current_token_index].type == 'NEWLINE':
                self.line_number += 1
                raise RuntimeError(f'Expected a ; at line {self.line_number} but None was found')

            self.advance()
            var_node.add_child(jn.JangNodes(self.parse_expression()))
        return var_node
    
    def parse_while(self):
        while_node = jn.JangWhileNode(self.tokens[self.current_token_index])
        # self.advance()
        self.expect_token_type('LPAREN', '(')
        self.advance()
        while self.tokens[self.current_token_index].type != 'RPAREN':
            if self.tokens[self.current_token_index].type == 'NEWLINE':
                self.line_number += 1
                raise RuntimeError(f'Expected a ) at line {self.line_number} but None was found')

            while_node.add_child(jn.JangNodes(self.tokens[self.current_token_index]))
            self.advance()
        if self.tokens[self.current_token_index].type != 'RPAREN':
            raise RuntimeError(f'Expected a ) at line {self.line_number} but None was found')
        self.expect_token_type('IF', 'if')
        self.expect_token_type('FR', 'fr')
        # new line
        self.advance()
        if self.tokens[self.current_token_index].type == 'NEWLINE':
            self.line_number += 1
        self.expect_token_type('LBRACE', '{')
        while_node.add_child(self.parse_body())
        if self.tokens[self.current_token_index].type != 'RBRACE':
            raise RuntimeError("Expected a '}' at line {} but None was found".format(self.line_number))
        
        return while_node

    def parse_ret(self):
        ret_node = jn.JangReturnNode(self.tokens[self.current_token_index])
        self.advance()
        while self.tokens[self.current_token_index].type != 'SEMICOLON':
            if self.tokens[self.current_token_index].type == 'NEWLINE':
                self.line_number += 1
                raise RuntimeError(f'Expected a ; at line {self.line_number} but None was found')

            ret_node.add_child(jn.JangNodes(self.tokens[self.current_token_index]))
            self.advance()
        return ret_node


    def expect_token_type(self, expected_type, expected_tk=None, node=None):
        c_token = self.advance()
        if c_token.type == expected_type:
            if node:
                node.add_child(jn.JangNodes(c_token))
        else:
            raise RuntimeError(f'Expected a {expected_tk} at line {self.line_number} but None was found')
        
    def parse_factor(self):
        token = self.tokens[self.current_token_index]

        if token and token.type in ['INT_LITERAL', 'FLOAT_LITERAL', 'IDENTIFIER']:
            node = jn.JangNodes(token)
            self.advance()
            return (node)

        elif token and token.type == 'LPAREN':
            self.advance()
            expr_res = self.parse_expression()
            if self.tokens[self.current_token_index] and self.tokens[self.current_token_index].type == 'RPAREN':
                self.advance()
                return expr_res
            else:
                raise RuntimeError(f"Expected ')' at line {self.line_number} but None was found")

        raise RuntimeError(f"Expected a factor at line {self.line_number} but None was found")

    def parse_term(self):
        return self.bin_op(self.parse_factor, ['TIMES', 'DIVIDE'])

    def parse_expression(self):
        return self.bin_op(self.parse_term, ['PLUS', 'MINUS'])

    def bin_op(self, func, ops):
        left = func()

        while self.tokens[self.current_token_index] and self.tokens[self.current_token_index].type in ops:
            op_token = self.tokens[self.current_token_index]
            self.advance()
            right = func()
            left = jn.BinOpNode(left, op_token, right)

        return left
