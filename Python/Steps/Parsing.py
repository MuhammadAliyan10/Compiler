class NumberNode:
    def __init__(self, value):
         self.value = value
    def __repr__(self):
        return f"NumberNode(value={self.value})"
        
class BinOpNode:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
    def __repr__(self):
        return f"BinOpNode(left={self.left}, operator='{self.operator}', right={self.right})"

class AssignNode:
    def __init__(self, variable, value):
        self.variable = variable
        self.value = value
    def __repr__(self):
        return f"AssignNode({self.variable} = {self.value})"

class Parser:
    def __init__(self, tokens) -> None:
        self.tokens = tokens
        self.pos = 0
    def parse(self):
        return self.assignment()
    def assignment(self):
        variable = self.consume('ID')
        self.consume('ASSIGN')
        value = self.expr()
        self.consume('END')
        return AssignNode(variable, value)
    
    def expr(self):
        left = self.term()
        while self.match('OP'):
            op = self.consume('OP')
            right = self.term()
            left = BinOpNode(left, op, right)
        return left
    
    def term(self):
        if self.match('NUMBER'):
            return NumberNode(self.consume("NUMBER"))
        else:
            raise RuntimeError("Unexpected token")
        
    def consume(self, expected_type):
        token_type, token_value = self.tokens[self.pos]
        if token_type == expected_type:
            self.pos += 1
            return token_value
        raise RuntimeError(f'Expected {expected_type}, got {token_type}')
    
    def match(self, expected_type):
        if self.pos < len(self.tokens) and self.tokens[self.pos][0] == expected_type:
            return True
        return False
    

# code = "x = 10 + 20;"
# tokens = list(tokenize(code))
# parser = Parser(tokens)
# ast = parser.parse()
# print(ast)