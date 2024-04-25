
class JangNodes:
    def __init__(self, token):
        self.token = token
        self.child_nodes = []

    def add_child(self, node):
        self.child_nodes.append(node)

    def __repr__(self, indent=0):
        return f"{'    ' * indent}({self.token})"
    
class JangFuncNode(JangNodes):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.return_type = None
        self.name = None
        self.body = []

    def __repr__(self, indent=0):
        child_nodes_str = ',\n'.join(node.__repr__(indent + 1) for node in self.child_nodes)
        return f"{'    ' * indent}(FUNC_SMT)[\n{child_nodes_str}\n{'    ' * indent}]"
    
class JangParamNode(JangNodes):
    def __init__(self, tokens):
        super().__init__(tokens)

    def __repr__(self, indent=0):
        child_nodes_str = ',\n'.join(node.__repr__(indent + 1) for node in self.child_nodes)
        return f"{'    ' * indent}(PARAM_SMT)[\n{child_nodes_str}\n{'    ' * indent}]"

class JangBodyNode(JangNodes):
    def __init__(self, tokens):
        super().__init__(tokens)

    def __repr__(self, indent=0):
        child_nodes_str = ',\n'.join(node.__repr__(indent + 1) for node in self.child_nodes)
        return f"{'    ' * indent}(BODY_SMT)[\n{child_nodes_str}\n{'    ' * indent}]"

class JangPrintNode(JangNodes):
    def __init__(self, tokens):
        super().__init__(tokens)
    
    def __repr__(self, indent=0):
        child_nodes_str = ',\n'.join(node.__repr__(indent + 1) for node in self.child_nodes)
        return f"{'    ' * indent}(PRINT_SMT)[\n{child_nodes_str}\n{'    ' * indent}]"
    
class JangVarNode(JangNodes):
    def __init__(self, tokens):
        super().__init__(tokens)

    def __repr__(self, indent=0):
        child_nodes_str = ',\n'.join(node.__repr__(indent + 1) for node in self.child_nodes)
        return f"{'    ' * indent}(VAR_SMT)[\n{child_nodes_str}\n{'    ' * indent}]"
    
class JangReturnNode(JangNodes):
    def __init__(self, tokens):
        super().__init__(tokens)

    def __repr__(self, indent=0):
        child_nodes_str = ',\n'.join(node.__repr__(indent + 1) for node in self.child_nodes)
        return f"{'    ' * indent}(RETURN_SMT)[\n{child_nodes_str}\n{'    ' * indent}]"
    
class JangWhileNode(JangNodes):
    def __init__(self, tokens):
        super().__init__(tokens)

    def __repr__(self, indent=0):
        child_nodes_str = ',\n'.join(node.__repr__(indent + 1) for node in self.child_nodes)
        return f"{'    ' * indent}(WHILE_SMT)[\n{child_nodes_str}\n{'    ' * indent}]"

class BinOpNode(JangNodes):
    def __init__(self, left, token, right):
        super().__init__(token)
        self.left_node = left
        self.right_node = right

    def __repr__(self, indent=0):
        return f'({self.left_node}, {self.token.type}, {self.right_node})'
    
class UnaryOpNode(JangNodes):
    def __init__(self, token, node):
        super().__init__(token)
        self.node = node

    def __repr__(self, indent=0):
        return f'({self.token.type}, {self.node})'
    
class JangExprNode(JangNodes):
    def __init__(self, tokens):
        super().__init__(tokens)
        self.node = None

    def __repr__(self, indent=0):
        child_nodes_str = ',\n'.join(node.__repr__(indent + 1) for node in self.child_nodes)
        return f"{'    ' * indent}(EXPR_SMT: {self.node})[\n{child_nodes_str}\n{'    ' * indent}]"
