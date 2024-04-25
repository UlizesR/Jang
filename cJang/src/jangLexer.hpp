// JangLexer.h
#ifndef JANGLEXER_H
#define JANGLEXER_H

#include <vector>
#include <string>
#include <unordered_map>
#include <iostream>
#include <sstream>

// Define token types
enum TokenType 
{
    RETURN,             // 0
    INPUT,              // 1
    VAR_DECL,
    VAR_CHNG,
    FUNC_DECL,
    PRINT,
    EOF_TKN,  
    IF_START,
    IF_END,
    ELSE,
    ARRAY,
    WHILE_LOOP, 
    FOR_LOOP,
    FILE_READ,
    FILE_WRITE,
    BOOL,
    IMPORT,
    ASSIGN,
    OPERATOR,
    RELATIONAL,
    NOT,
    L_CBRAKET,
    R_CBRAKET,
    LPAREN,
    RPAREN,
    L_BRAKET,
    R_BRAKET,
    TYPE,
    CLASS,
    KEYWORD,
    LITERAL,
    IDENTIFIER,
    COMMA,
    SEMMICOLON,
    UNKNOWN
};

// Token structure
struct Token 
{
    TokenType type;
    std::string lexeme;
    size_t line;
};

class JangLexer 
{
private:
     // map to map a number to its corresponding token type
    std::unordered_map<std::string, TokenType> keywordMap;

    // Get token type for a given word
    // Get token type for a given word
    TokenType getTokenType(const std::string& word);

public:
    JangLexer();
    std::vector<Token> tokenizeLine(const std::string& line, size_t lineNumber);
    std::vector<Token> tokenizeFile(const std::string& filename);

    std::unordered_map<TokenType, std::string> tokenTypeMap;
};

#endif // JANGLEXER_H
