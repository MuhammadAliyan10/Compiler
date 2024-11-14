import re

# Lexical Analysis (Tokenization)
token_specification = [
    ('NUMBER', r'\d+(\.\d*)?'), #! Integer or decimal number
    ('ASSIGN',r'='), #! Assignment Operator
    ('END',r';'), #! End of statement
    ('ID',r'[A-Za-z]+'), #! Identifier
    ('OP',r'[+\-*/]'), #! Operators
    ('WHITESPACE',r'[ \t]+'), #! Whitespace
    ('MISMATCH',r'.'), #! Any other character
]

token_regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in token_specification)

def tokenize(code):
    for match in re.finditer(token_regex, code):
        kind = match.lastgroup
        value = match.group(kind)
        if kind == 'WHITESPACE':
            continue
        elif kind == 'MISMATCH':
            raise RuntimeError(f"f'Unexpected character {value}")
        yield kind, value


# code = " x =    20 + 10;"
# tokens = list(tokenize(code))
# print(tokens)
# print(len(tokens))