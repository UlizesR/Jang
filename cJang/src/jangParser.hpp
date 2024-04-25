// jangParser.hpp
#ifndef JANGPARSER_H
#define JANGPARSER_H

#include "jangLexer.hpp"

#include <string>
#include <vector>

// AST Node
struct Node
{
    std::string value;
    std::vector<Node> children;
};


class JangParser
{
private: 
    Token advance();
    int currentTokenIndex;
    Token currentToken;

    // AST
    Node root;

public:
    JangParser();
    ~JangParser();

    void parse(std::vector<Token> tokens, JangLexer lexer);

    std::vector<Token> tokens;

};

#endif // JANGPARSER_H