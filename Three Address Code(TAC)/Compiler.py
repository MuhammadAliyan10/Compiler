import ast

class ThreeAddressCode(ast.NodeVisitor):
    def __init__(self):
        self.tempCount = 0
        self.code = []

    def newTemp(self):
        self.tempCount += 1
        return f't{self.tempCount}'

    def visit_BinOp(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        temp = self.newTemp()
        operator = self.getOperator(node.op)
        self.code.append(f"{temp} = {left} {operator} {right}")
        return temp

    def visit_Num(self, node):
        return str(node.n)

    def visit_Assign(self, node):
        value = self.visit(node.value)
        for target in node.targets:
            self.code.append(f"{target.id} = {value}")

    def visit_Module(self, node):
        for stmt in node.body:
            self.visit(stmt)

    def getOperator(self, operator):
        if isinstance(operator, ast.Add):
            return '+'
        elif isinstance(operator, ast.Sub):
            return '-'
        elif isinstance(operator, ast.Mult):
            return '*'
        elif isinstance(operator, ast.Div):
            return '/'
        else:
            raise ValueError(f"Unsupported operation: {operator}")

    def generate(self, code):
        tree = ast.parse(code)
        self.visit(tree)
        return self.code


# Example usage
code = """
x = 5 + 3 * 2
y = x - 1
"""

generator = ThreeAddressCode()
tac = generator.generate(code)

for line in tac:
    print(line)