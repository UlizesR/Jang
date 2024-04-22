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
    VAR_DECL,           // 2
    VAR_CHNG,           // 3
    FUNC_DECL,          // 4
    PRINT,              // 5
    CONDITIONAL,        // 6
    ARRAY,              // 7
    WHILE_LOOP,         // 8 
    FOR_LOOP,           // 9
    FILE_READ,          // 10
    FILE_WRITE,         // 11
    BOOL,               // 12
    IMPORT,             // 13
    ASSIGN,             // 14
    OPERATOR,           // 15
    RELATIONAL,         // 16       
    NOT,                // 17
    L_CBRAKET,          // 18
    R_CBRAKET,          // 19
    LPAREN,             // 20
    RPAREN,             // 21
    L_BRAKET,           // 22
    R_BRAKET,           // 23
    TYPE,               // 24
    CLASS,              // 25
    KEYWORD,            // 26
    LITERAL,            // 27
    IDENTIFIER,         // 28
    COMMA,              // 29
    SEMMICOLON,         // 30
    UNKNOWN             // 31
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
