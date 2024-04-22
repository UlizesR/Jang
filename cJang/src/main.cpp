#include <iostream>
#include <string>
#include <vector>

#include "jangLexer.hpp"

int main() {
    // Test the lexer
    JangLexer lexer;
    std::vector<Token> tokens = lexer.tokenizeFile("../Samples/main.jang");

    // Print tokens
    for (const auto& token : tokens) 
    {
        std::cout << "Token: " << token.lexeme << "\t Type: " << lexer.tokenTypeMap[token.type] << "\t Line: " << token.line << std::endl;
    }

    return 0;
}