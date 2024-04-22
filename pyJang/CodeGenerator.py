import JangLexer as JL
import JangParser as JP
from JangStructs import *

class CodeGenerator:
    def __init__(self, parser):
        self.parser = parser
        self.generated_code = []

    def generate_code(self):
        
        # Go through each stored variable and generate initialization code
        for var_name, (var_type, var_value) in self.parser.variables.items():
            self.generated_code.append(f"{var_name} = {var_value}")

        # Return the generated code as a single string
        return '\n'.join(self.generated_code)

# Example
if __name__ == '__main__':
    lexer = JL.JangLexer()
    parser = JP.JangParser(lexer)
    
    # Code snippet
    text = '''
    make int x be 10;
    '''
    tokens = lexer.tokenize(text)
    parser.parse_tokens(tokens)
    
    code_gen = CodeGenerator(parser)
    python_code = code_gen.generate_code()
    print(python_code)