
class JangVariable:
    def __init__(self, name, type_, value=None):
        self.name = name
        self.type = type_
        self.value = value

    def __repr__(self):
        return f"{self.type} {self.name} = {self.value}"
    
class JangArgs:
    def __init__(self, type_, name):
        self.type = type_
        self.name = name

    def __repr__(self):
        return f"{self.type} {self.name}"
    
class JangFunction:
    def __init__(self, name, return_type, args, body):
        self.name = name
        self.return_type = return_type
        self.args = args
        self.body = body

    def __repr__(self):
        args_repr = ', '.join([str(arg) for arg in self.args])
        body_repr = ', '.join([str(stmt) for stmt in self.body])
        return f"[Function: '{self.name}', args: [{args_repr}], return_type: {self.return_type}, body: [{body_repr}]]"
    
class JangConditional:
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body

    def __repr__(self):
        body_repr = ', '.join([str(stmt) for stmt in self.body])
        return f"conditional: {self.condition}, body: [{body_repr}]"
    