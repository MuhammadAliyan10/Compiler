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

    


# code = "x = 10 + 20;"
# tokens = list(tokenize(code))
# parser = Parser(tokens)
# ast = parser.parse()  # This returns a single AssignNode

# generator = CodeGenerator()
# generated_code = generator.generate(ast)  # Directly pass the ast (AssignNode) here
# print("Generated Code:")
# print(generated_code)