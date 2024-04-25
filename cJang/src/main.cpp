#include <iostream>
#include <string>
#include <vector>

#include "jangLexer.hpp"
#include "jangParser.hpp"

int main() {
    // Test the lexer
    JangLexer lexer;
    JangParser parser;
    std::vector<Token> tokens = lexer.tokenizeFile("../Samples/main.jang");

    parser.parse(tokens, lexer);

    return 0;
}