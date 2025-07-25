from pathlib import Path
import argparse
from typing import List
from enum import Enum
import sys
import re


ALPHA_NUMERIC_PATTERN = r"[a-zA-Z_][a-zA-Z_0-9]*"

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


class Token:
    def __init__(
        self, type_: TokenType, lexeme: str, line_no: int, literal_value: str
    ):
        self.type_ = type_
        self.lexeme: str = lexeme
        self.line_no: int = line_no
        self.literal_value = literal_value

    def __repr__(self):
        return f"Token(type_={self.type_}, \
            lexeme={self.lexeme}, \
            line_no={self.line_no}, \
            literal_value={self.literal_value})"

def throw_error(error_type: str, line_no: int, context: str):
    print(f"{error_type} at line {line_no}")
    print(context)

def read_file(file: Path) -> List[str]:
    try:
        with open(file, "r") as f:
            line_list: List[str] = f.readlines()
    except Exception as e:
        print(e)
    return line_list


def tokenize(raw_text_list) -> List[Token]:

    for line_no, text in enumerate(raw_text_list, 1):
        tokenized_line = []
        for char in text:
            match char:
                case r"(": 
                    tokenized_line.append(Token(TokenType.LEFT_PAREN), r"(", None, line_no)
                case r")": 
                    tokenized_line.append(Token(TokenType.RIGHT_PAREN), r")", None, line_no)
                case r"{": 
                    tokenized_line.append(Token(TokenType.LEFT_BRACE), r"{", None, line_no)
                case r"}": 
                    tokenized_line.append(Token(TokenType.RIGHT_BRACE), r"}", None, line_no)
                case r",": 
                    tokenized_line.append(Token(TokenType.COMMA), r",", None, line_no)
                case r".": 
                    tokenized_line.append(Token(TokenType.DOT), r".", None, line_no)
                case r"-": 
                    tokenized_line.append(Token(TokenType.MINUS), r"-", None, line_no)
                case r"+": 
                    tokenized_line.append(Token(TokenType.PLUS), r"+", None, line_no)
                case r";": 
                    tokenized_line.append(Token(TokenType.SEMICOLON), r";", None, line_no)
                case r"*": 
                    tokenized_line.append(Token(TokenType.STAR), r"*", None, line_no)
            if istype(re.Match, re.search(ALPHA_NUMERIC_PATTERN, char):
                tokenized_line.append(Token(TokenType.STAR), r"char", None, line_no)
                if 
            else:
                error_context = "".join(raw_text_list[max(0, line_no-2):min(line_no+2, len(raw_text_list))])
                throw_error("InvalidCharacter", line_no, error_context)
        print(text)
    return [TokenType.NULL for _ in range(len(raw_text_list))]


def execute_program(tokens: List[Token]) -> int:  # exit code
    for i, token in enumerate(tokens):
        print(f"Token {i}: {str(token)}")
    return 0


def main():
    parser = argparse.ArgumentParser(description="A simple script with arguments.")
    parser.add_argument("file", help="file to interpret")
    parser.add_argument("-l", "--log", default=False, help="save build logs to a file")
    args = parser.parse_args()

    lines = read_file(args.file)
    tokens = tokenize(lines)
    exit_code = execute_program(tokens)
    print(exit_code)  # would be nice to have a build log ¯\_(ツ)_/¯
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
