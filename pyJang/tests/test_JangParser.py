import sys
import unittest

sys.path.append('../src')
from JangLexer import JangLexer as JL
from JangParser import JangParser as JP

"""
Done:
- variable declarations
- function declarations
    - arguments
    - body

- variable reassignment
- syntax error

TODO
- expressions
"""

class TestJangParser(unittest.TestCase):
    def setUp(self):
        self.lexer = JL()
        self.parser = JP(self.lexer)

    def tokenize_and_parse(self, text):
        tokens = self.lexer.tokenize(text)
        self.parser.parse_tokens(tokens)
        return tokens
    
    def test_parse_arguments(self):
        text = "julio wants int test(int a, string b) { }"
        self.tokenize_and_parse(text)
        self.assertIn('test', self.parser.functions)
        self.assertEqual(self.parser.functions['test']['args'], [('a', 'int'), ('b', 'string')])

    def test_parse_body(self):
        text = "{ make int x be 10; change x to 20; }"
        tokens = self.lexer.tokenize(text)
        self.parser.tokens = tokens
        self.parser.current_token_index = 1  # Start just after the opening brace
        
        expected_body = [
            "int x = 10",
            "x = 20"
        ]
        body = self.parser.parse_body()
        
        self.assertEqual(body, expected_body)
        self.assertEqual(self.parser.tokens[self.parser.current_token_index - 1].type, 'RBRACE')
    
    def test_function_declaration(self):
        text = "julio wants int add(int x, int y) { make int z be x ; }"
        self.tokenize_and_parse(text)
        self.assertIn('add', self.parser.functions)
        expected = {
            'return_type': 'int',
            'args': [('x', 'int'), ('y', 'int')],
            'body': ['int z = x']
        }
        self.assertEqual(self.parser.functions['add'], expected)

    def test_variable_declaration(self):
        text = "make int x be 10;"
        self.tokenize_and_parse(text)
        self.assertIn('x', self.parser.variables)
        self.assertEqual(self.parser.variables['x'], ('int', '10'))

    def test_variable_change(self):
        text = 'make int x be 10; change x to 20;'
        self.tokenize_and_parse(text)
        self.assertIn('x', self.parser.variables)
        self.assertEqual(self.parser.variables['x'], ('int', '20'))

    def test_syntax_error(self):
        text = "make int x 10;"  # Missing 'be'
        with self.assertRaises(RuntimeError):
            self.tokenize_and_parse(text)

# To run the tests
if __name__ == '__main__':
    unittest.main()