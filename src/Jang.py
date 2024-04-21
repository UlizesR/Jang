import JangParser2 as JP
import JangLexer as JL
import sys
import os

# test the parser
# if __name__ == '__main__':
#     lexer = JL.JangLexer()
#     parser = JangParser(lexer)
#     text = 'make int x be 10;'
#     tokens = lexer.tokenize(text)
#     parser.parse_tokens(tokens)
#     print(parser.variables)
#     text = 'change x to 20;'
#     tokens = lexer.tokenize(text)
#     parser.parse_tokens(tokens)
#     print(parser.variables)

#     text = """julio wants int add(int x, int y) { 
#         make int z be x + 1; 
#         change z to y + 1; 
#         julio gets z; 
#     } 
#     julio says add(1, 2);"""
#     tokens = lexer.tokenize(text)
#     parser.parse_tokens(tokens)
#     for code in parser.ast:
#         print(code)

#     # text = 'julio wants none print(int x) { julio gets x; }'
#     # tokens = lexer.tokenize(text)
#     # parser.parse_tokens(tokens)
#     # print(parser.functions)



if __name__ == '__main__':
    lexer = JL.JangLexer()
    parser = JP.JangParser(lexer)

    # read a test file and tokenize it
    # get the path to the Samples folder
    path = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(path, 'Samples')
    with open(os.path.join(path,'helloworld.jang')) as file:
        text = file.read()

    tokens = lexer.tokenize(text)
    parser.parse_tokens(tokens)

    # print the AST
    for code in parser.ast:
        print(code)
