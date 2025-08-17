from pathlib import Path
import argparse
from typing import List
import sys
import re
from data_definitions import Token, TokenType


ALPHA_NUM_PATTERN = r"[a-zA-Z_][a-zA-Z_0-9]*"


keyword_dict = {
    "and": TokenType.AND,
    "class": TokenType.CLASS,
    "else": TokenType.ELSE,
    "False": TokenType.FALSE,
    "if": TokenType.IF,
    "elif": TokenType.ELIF,
    "or": TokenType.OR,
    "None": TokenType.NULL,
    "print": TokenType.PRINT,
    "return": TokenType.RETURN,
    "super": TokenType.SUPER,
    "self": TokenType.SELF,
    "True": TokenType.TRUE,
    "var": TokenType.VAR,
    "while": TokenType.WHILE,
}


def throw_error(error_type: str, line_no: int, context: str):
    print(error_type + " at line " + str(line_no))
    print(context)


def read_file(file: Path) -> List[str]:
    try:
        with open(file, "r") as f:
            line_list: List[str] = f.read()
    except Exception as e:
        print(e)
    return line_list


def is_digit(char: str):
    if char in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
        return True
    return False


def is_identifier(char: str):
    if re.search(ALPHA_NUM_PATTERN, char) is not None:
        return True
    return False


def tokenize(raw_text: List[str]) -> List[Token]:
    line_no: int = 1
    tokens: List[Token] = []
    char_index: int = 0
    while char_index < len(raw_text):
        match raw_text[char_index]:
            case "(":
                tokens.append(Token(TokenType.LEFT_PAREN, r"(", None, line_no))
            case ")":
                tokens.append(Token(TokenType.RIGHT_PAREN, r")", None, line_no))
            case "[":
                tokens.append(Token(TokenType.LEFT_SQR_BRACKET, r"[", None, line_no))
            case "]":
                tokens.append(Token(TokenType.RIGHT_SQR_BRACKET, r"]", None, line_no))
            case "{":
                tokens.append(Token(TokenType.LEFT_BRACE, r"{", None, line_no))
            case "}":
                tokens.append(Token(TokenType.RIGHT_BRACE, r"}", None, line_no))
            case ",":
                tokens.append(Token(TokenType.COMMA, r",", None, line_no))
            case ".":
                tokens.append(Token(TokenType.DOT, r".", None, line_no))
            case "-":
                tokens.append(Token(TokenType.MINUS, r"-", None, line_no))
            case "+":
                tokens.append(Token(TokenType.PLUS, r"+", None, line_no))
            case ";":
                tokens.append(Token(TokenType.SEMICOLON, r";", None, line_no))
            case "*":
                tokens.append(Token(TokenType.STAR, r"*", None, line_no))
            case "/":
                tokens.append(Token(TokenType.SLASH, r"/", None, line_no))
            case "!":
                if raw_text[char_index + 1] == "=":
                    char_index += 1
                    tokens.append(Token(TokenType.BANG_EQUAL, r"!=", None, line_no))
                else:
                    tokens.append(Token(TokenType.BANG, r"!", None, line_no))
            case "=":
                if raw_text[char_index + 1] == "=":
                    char_index += 1
                    tokens.append(Token(TokenType.EQUAL_EQUAL, r"!=", None, line_no))
                else:
                    tokens.append(Token(TokenType.EQUAL, r"=", None, line_no))
            case "<":
                if raw_text[char_index + 1] == "=":
                    char_index += 1
                    tokens.append(Token(TokenType.LESS_EQUAL, r"<=", None, line_no))
                else:
                    tokens.append(Token(TokenType.LESS, r"<", None, line_no))
            case ">":
                if raw_text[char_index + 1] == "=":
                    char_index += 1
                    tokens.append(Token(TokenType.GREATER_EQUAL, r">=", None, line_no))
                else:
                    tokens.append(Token(TokenType.GREATER, r">", None, line_no))
            case "#":  # comment case
                while raw_text[char_index] != r"\n":
                    char_index += 1
            case "\n":  # newline case
                line_no += 1
            case " " | "\r" | "\t":  # whitespace case
                pass
            case '"':  # string literal w/ "
                str_lit: str = ""
                char_index += 1
                while raw_text[char_index] != '"':
                    str_lit += raw_text[char_index]
                    char_index += 1
                tokens.append(Token(TokenType.STRING, str_lit, None, line_no))
            case "'":  # string literal w/ '
                str_lit: str = ""
                char_index += 1
                while raw_text[char_index] != "'":
                    str_lit += raw_text[char_index]
                    char_index += 1
                tokens.append(Token(TokenType.STRING, str_lit, None, line_no))
            case _:
                if is_identifier(raw_text[char_index]):  # variables aka identifiers
                    ident_lit: str = ""
                    while is_identifier(raw_text[char_index]) or is_digit(
                        raw_text[char_index]
                    ):
                        ident_lit += raw_text[char_index]
                        char_index += 1
                    tokens.append(Token(TokenType.IDENTIFIER, ident_lit, None, line_no))
                elif is_digit(raw_text[char_index]):  # numbers
                    num_lit: str = ""
                    while raw_text[char_index] not in [" ", r"\r", r"\t"]:
                        if (
                            is_digit(raw_text[char_index])
                            or raw_text[char_index] == "."
                        ):
                            num_lit += raw_text[char_index]
                        char_index += 1
                    tokens.append(Token(TokenType.NUMBER, num_lit, None, line_no))
                else:
                    error_context = "".join(
                        raw_text[max(0, line_no - 2) : min(line_no + 2, len(raw_text))]
                    )
                    throw_error("InvalidCharacter", line_no, error_context)
        char_index += 1

    for token in tokens:
        token.type_ = keyword_dict.get(token.literal_value, token.type_)

    return tokens


def execute_program(tokens: List[Token]) -> int:  # exit code
    print("\n".join(f"Token {i}: {token}" for i, token in enumerate(tokens)))
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="~~~~~  Typhoon Python Interpreter  ~~~~~"
    )
    parser.add_argument("file", help="file to interpret")
    parser.add_argument("-l", "--log", default=False, help="save build logs to a file")
    args = parser.parse_args()

    lines = read_file(args.file)
    tokens = tokenize(lines)
    exit_code = execute_program(tokens)
    print(
        f"Program Exited with code '{exit_code}'"
    )  # would be nice to have a build log ¯\_(ツ)_/¯
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
