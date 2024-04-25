#include "jangParser.hpp"
#include "jangLexer.hpp"

JangParser::JangParser()
{
    this->currentTokenIndex = 0;
    
}

JangParser::~JangParser()
{
}

Token JangParser::advance()
{
    this->currentTokenIndex++;
    if (this->currentTokenIndex < this->tokens.size())
    {
        return this->currentToken = this->tokens[this->currentTokenIndex];
    }
    // Throw an exception when out of range
    throw std::out_of_range("Token index out of range"); 
}

void JangParser::parse(std::vector<Token> tokens, JangLexer lexer)
{
    this->tokens = tokens;
    this->currentToken = this->tokens[0];
    for (auto token : tokens)
    {
        // std::cout << "Token: " << token.lexeme << "\t Type: " << lexer.tokenTypeMap[token.type] << "\t Line: " << token.line << std::endl;

        // build the AST
        
    }
}