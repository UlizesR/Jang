import JangLexer as jl
import JangParser as jp
import sys

if __name__ == "__main__":
    lexer = jl.JangLexer()
    parser = jp.JangParser(lexer)

    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        try:
            with open(filepath, 'r') as file:
                text = file.read()
        except Exception as e:
            print(f"Failed to read file {filepath}: {e}")

        tokens = lexer.tokenize(text)
        parser.parse(tokens)
        print(parser.ast)
