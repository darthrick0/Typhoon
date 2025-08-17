from enum import Enum
from typing import final, override


class TokenType(Enum):
    # Single-character tokens.
    LEFT_PAREN = "LEFT_PAREN"
    RIGHT_PAREN = "RIGHT_PAREN"
    LEFT_BRACE = "LEFT_BRACE"
    RIGHT_BRACE = "RIGHT_BRACE"
    COMMA = "COMMA"
    DOT = "DOT"
    MINUS = "MINUS"
    PLUS = "PLUS"
    SEMICOLON = "SEMICOLON"
    SLASH = "SLASH"
    STAR = "STAR"

    # One or two character tokens.
    BANG = "BANG"
    BANG_EQUAL = "BANG_EQUAL"
    EQUAL = "EQUAL"
    EQUAL_EQUAL = "EQUAL_EQUAL"
    GREATER = "GREATER"
    GREATER_EQUAL = "GREATER_EQUAL"
    LESS = "LESS"
    LESS_EQUAL = "LESS_EQUAL"

    # Literals.
    IDENTIFIER = "IDENTIFIER"
    STRING = "STRING"
    NUMBER = "NUMBER"

    # Keywords.
    AND = "AND"
    CLASS = "CLASS"
    ELSE = "ELSE"
    FALSE = "FALSE"
    IF = "IF"
    ELIF = "ELIF"
    OR = "OR"
    NULL = "NULL"
    PRINT = "PRINT"
    RETURN = "RETURN"
    SUPER = "SUPER"
    SELF = "SELF"
    TRUE = "TRUE"
    VAR = "VAR"
    WHILE = "WHILE"

    EOF = "EOF"

@final
class Token:
    def __init__(self, type_: TokenType, literal_value: str, lexeme: str, line_no: int):
        self.type_ = type_
        self.lexeme: str = lexeme
        self.line_no: int = line_no
        self.literal_value = literal_value
    
    @override
    def __repr__(self) -> str:
        return f"Token({self.type_=}, {self.lexeme=}, {self.line_no=}, {self.literal_value=})"

