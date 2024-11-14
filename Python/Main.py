import re


# Lexical Analysis (Tokenization)
token_specification = [
    ('NUMBER', r'\d+(\.\d*)?'), #! Integer or decimal number
    ('ASSIGN',r'='), #! Assignment Operator
    ('END',r';'), #! End of statement
    ('ID',r'[A-Za-z]+'), #! Identifier
    ('OP',r'[+\-*/]'), #! Operators
    ('LPAREN', r'\('),          #! Left Parenthesis
    ('RPAREN', r'\)'),          #! Right Parenthesis
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


#! Step 2: Syntax Analysis (Parsing)

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
    
class IfNode:
    def __init__(self, condition, true_branch, false_branch=None):
        self.condition = condition
        self.true_branch = true_branch
        self.false_branch = false_branch
    def __repr__(self):
        return f"IfNode(condition={self.condition}, true_branch={self.true_branch}, false_branch={self.false_branch})"


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
        elif self.match('LPAREN'):
            self.consume('LPAREN')  
            expr = self.expr()  
            self.consume('RPAREN') 
            return expr
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



#! Step 3: Evaluation

class Evaluator:
    def __init__(self):
        self.environment = {}
    def evaluate(self,node):
        if isinstance(node, NumberNode):
            return self.eval_number(node)
        elif isinstance(node, BinOpNode):
            return self.eval_binOp(node)
        elif isinstance(node, AssignNode):
            return self.eval_assign(node)
        else:
            raise RuntimeError(f"Unsupported node type: {type(node)}")
        
    def eval_number(self,node):
        return int(node.value)
    def eval_binOp(self, node):
        leftValue = self.evaluate(node.left)
        rightValue = self.evaluate(node.right)
        if node.operator == '+':
            return leftValue + rightValue
        elif node.operator == '-':
            return leftValue - rightValue
        elif node.operator == '*':
            return leftValue * rightValue
        elif node.operator == '/':
            if rightValue == 0:
                raise ZeroDivisionError("Division by zero")
            return leftValue / rightValue
        else:
            raise RuntimeError(f"Unsupported operator: {node.operator}")
        
    def eval_assign(self, node):
        value = self.evaluate(node.value)
        self.environment[node.variable] = value
        return value
    


# code = "x = 10 + 20;"
# tokens = list(tokenize(code))
# parser = Parser(tokens)
# ast = parser.parse()

# evaluator = Evaluator()
# result = evaluator.evaluate(ast)
# print(f"Result: {result}")
# print(f"Environment: {evaluator.environment}")


#! Step 4: Code Generation to Python Code


class CodeGenerator:
    def generate(self, node):
        if isinstance(node, NumberNode):
            return self.generate_number(node)
        elif isinstance(node, BinOpNode):
            return self.generate_binOp(node)
        elif isinstance(node, AssignNode):
            return self.generate_assign(node)
        else:
            raise RuntimeError(f"Unknown node type: {type(node)}")

    def generate_number(self, node):
        return str(node.value)

    def generate_binOp(self, node):
        left = self.generate(node.left)
        right = self.generate(node.right)
        return f"{left} {node.operator} {right}"

    def generate_assign(self, node):
        variable = node.variable
        value = self.generate(node.value)
        return f"{variable} = {value}"

    


code = "x = 10 + 20;"
tokens = list(tokenize(code))
parser = Parser(tokens)
ast = parser.parse()  # This returns a single AssignNode

generator = CodeGenerator()
generated_code = generator.generate(ast)  # Directly pass the ast (AssignNode) here
print("Generated Code:")
print(generated_code)


