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