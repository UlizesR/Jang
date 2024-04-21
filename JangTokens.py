import re
tokens = {
    "julio": "kwdTag",
    "wants": "FUNC_DEC",
    "gets": "RETURN",
    "says": "PRINT",
    "none": "TYPE",
    # Symbols
    "{": "LBRACE",
    "}": "RBRACE",
    "(": "LPAREN",
    ")": "RPAREN",
    ";": "SEMICOLON",
    '"': "STRINGDEF",
    "'": "STRINGDEF"
    
}

def getType(value):
    return tokens.get(value, None)