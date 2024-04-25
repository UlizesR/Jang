#include "jangLexer.hpp"

#include <fstream>
#include <regex>

TokenType JangLexer::getTokenType(const std::string& word) 
{
    // Identifier
    std::regex identifierPattern("[a-zA-Z_][a-zA-Z0-9_]*");
    // array declaration
    std::regex arrayDeclarationPattern("[a-zA-Z_][a-zA-Z0-9_]*\\[[0-9]+\\]");
    // string, char, int, decimal
    std::regex literalPattern("\".*\"|'.*'|[0-9]+|([0-9]+\\.[0-9]*)");
    // relational operators
    std::regex relationalPattern("<|>|<=|>=|==|!=");
    // operators
    std::regex operatorPattern("\\+|-|\\*|/");
    if (keywordMap.find(word) != keywordMap.end()) 
    {
        return keywordMap[word];
    } 
    else if (std::regex_match(word, arrayDeclarationPattern)) {
        return ARRAY;
    }
    else if (std::regex_match(word, identifierPattern)) {
        return IDENTIFIER;
    }
    else if (std::regex_match(word, literalPattern)) {
        return LITERAL;
    }
    else if (std::regex_match(word, operatorPattern)) 
    {
        return OPERATOR;
    }
    else if (std::regex_match(word, relationalPattern)) 
    {
        return RELATIONAL;
    }
    else if (word == "(") 
    {
        return LPAREN;
    } 
    else if (word == ")") 
    {
        return RPAREN;
    } 
    else if (word == "{") 
    {
        return L_CBRAKET;
    } 
    else if (word == "}") 
    {
        return R_CBRAKET;
    } 
    else if (word == "[") 
    {
        return L_BRAKET;
    } 
    else if (word == "]") 
    {
        return R_BRAKET;
    } 
    else if (word == ",") 
    {
        return COMMA;
    } 
    else if (word == ";") 
    {
        return SEMMICOLON;
    } 
    else {
        return UNKNOWN;
    }
}

JangLexer::JangLexer()
{
    this->keywordMap = {
        {"julio", KEYWORD},
        {"gets", RETURN},
        {"asks", INPUT},
        {"make", VAR_DECL},
        {"change", VAR_CHNG},
        {"wants", FUNC_DECL},
        {"says", PRINT},
        {"is", IF_START},
        {"fr", IF_END},
        {"else", ELSE},
        {"till", WHILE_LOOP},
        {"counts", FOR_LOOP},
        {"can", FILE_READ},
        {"write", FILE_WRITE},
        {"Yuh", BOOL},
        {"Nah", BOOL},
        {"grabs", IMPORT},
        {"be", ASSIGN},
        {"to", ASSIGN},
        {"not", NOT},
        {"int", TYPE},
        {"str", TYPE},
        {"dec", TYPE},
        {"char", TYPE},
        {"class", CLASS}
    };
    this->tokenTypeMap = {
        {KEYWORD, "KEYWORD"},
        {RETURN, "RETURN"},
        {INPUT, "INPUT"},
        {VAR_DECL, "VAR_DECL"},
        {VAR_CHNG, "VAR_CHNG"},
        {FUNC_DECL, "FUNC_DECL"},
        {PRINT, "PRINT"},
        {IF_START, "IF_START"},
        {IF_END, "IF_END"},
        {ELSE, "ELSE"},
        {ARRAY, "ARRAY"},
        {WHILE_LOOP, "WHILE_LOOP"},
        {FOR_LOOP, "FOR_LOOP"},
        {FILE_READ, "FILE_READ"},
        {FILE_WRITE, "FILE_WRITE"},
        {BOOL, "BOOL"},
        {IMPORT, "IMPORT"},
        {ASSIGN, "ASSIGN"},
        {OPERATOR, "OPERATOR"},
        {RELATIONAL, "RELATIONAL"},
        {NOT, "NOT"},
        {L_CBRAKET, "L_CBRAKET"},
        {R_CBRAKET, "R_CBRAKET"},
        {LPAREN, "LPAREN"},
        {RPAREN, "RPAREN"},
        {L_BRAKET, "L_BRAKET"},
        {R_BRAKET, "R_BRAKET"},
        {TYPE, "TYPE"},
        {CLASS, "CLASS"},
        {IDENTIFIER, "IDENTIFIER"},
        {LITERAL, "LITERAL"},
        {COMMA, "COMMA"},
        {SEMMICOLON, "SEMMICOLON"},
        {UNKNOWN, "UNKNOWN"}
    };
}

std::vector<Token> JangLexer::tokenizeLine(const std::string& line, size_t lineNumber)
{
    std::vector<Token> tokens;      // tokens vector
    tokens.reserve(line.size());    // Reserve space for tokens
    std::string word;               // word string
    bool inLiteral = false;         // inLiteral boolean

    // Loop through each character in the line
    for (char c : line) {
        // Check if the character is a quote or apostrophe
        if (c == '"' || c == '\'') 
        {
            inLiteral = !inLiteral;
            word += c;
        } 
        // Check if the character is a comma, semicolon, left parenthesis, or right parenthesis
        else if (!inLiteral && (c == ',' || c == ';' || c == '(' || c == ')')) 
        {
            // Check if the word string is not empty
            if (!word.empty()) 
            {
                // Get the token type for the word string
                TokenType type = getTokenType(word);
                // Add the token to the tokens vector
                tokens.emplace_back(Token{type, std::move(word), lineNumber});  
                // Clear the word string
                word.clear();
            }
            // Get the token type for the character
            TokenType type = getTokenType(std::string(1, c));
            // Add the token to the tokens vector
            tokens.emplace_back(Token{type, std::string(1, c), lineNumber});  // Use emplace_back
        } 
        // Check if the character is a space or tab
        else if (!inLiteral && (c == ' ' || c == '\t')) 
        {
            // Check if the word string is not empty
            if (!word.empty()) 
            {
                // Get the token type for the word string
                TokenType type = getTokenType(word);
                // Add the token to the tokens vector
                tokens.emplace_back(Token{type, std::move(word), lineNumber}); 
                // Clear the word string
                word.clear();
            }
        // Continue to the next character
        } else {
            word += c;
        }
    }
    // Check if the word string is not empty
    if (!word.empty()) 
    {
        // Get the token type for the word string
        TokenType type = getTokenType(word);
        // Add the token to the tokens vector
        tokens.emplace_back(Token{type, std::move(word), lineNumber});  // Use emplace_back and std::move
    }
    // Return the tokens vector
    return tokens;
}

std::vector<Token> JangLexer::tokenizeFile(const std::string& filename) 
{
    // tokens vector
    std::vector<Token> tokens;
    // Open the file
    std::ifstream file(filename);
    // Check if the file is open
    if (file.is_open()) 
    {
        // Read each line from the file
        std::string line;
        // Line number
        size_t lineNumber = 1;
        // Loop through each line in the file
        while (std::getline(file, line)) 
        {
            // Tokenize the line
            auto lineTokens = tokenizeLine(line, lineNumber++);
            // Add the line tokens to the tokens vector
            tokens.insert(tokens.end(), lineTokens.begin(), lineTokens.end());
        }
        // Close the file
        file.close();
    } else {
        // Throw an exception if the file cannot be opened
        throw std::runtime_error("Error: Unable to open file " + filename);
    }
    // Return the tokens vector
    return tokens;
}