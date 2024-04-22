class JangVariable:
    def __init__(self, name, type_, value=None, indent=0):
        self.name = name
        self.type = type_
        self.value = value
        self.indent = indent

    def __repr__(self):
        indent_str = ' ' * self.indent
        return f"{indent_str}{self.type} : {self.name} = {self.value}"

class JangArgs:
    def __init__(self, type_, name, indent=0):
        self.type = type_
        self.name = name
        self.indent = indent

    def __repr__(self):
        indent_str = ' '
        return f"{indent_str}{self.type} : {self.name}"

class JangClass:
    def __init__(self, name, body, indent=1):
        self.name = name
        self.body = body
        self.indent = indent

    def __repr__(self):
        indent_str = ' ' * self.indent
        body_repr = ',\n'.join([repr(stmt) for stmt in self.body])
        return f"{indent_str}Class: '{self.name}',\n{indent_str}body: [\n{body_repr}\n{indent_str}]"

class JangFunction:
    def __init__(self, name, return_type, args, body, indent=2):
        self.name = name
        self.return_type = return_type
        self.args = [JangArgs(arg.type, arg.name, indent + 1) for arg in args]
        self.body = [stmt if isinstance(stmt, str) else stmt.__class__(stmt.value, indent=indent+1) for stmt in body]
        self.indent = indent

    def __repr__(self):
        indent_str = ' ' * self.indent
        args_repr = ', '.join([repr(arg) for arg in self.args])
        body_repr = f',\n{indent_str * 2}'.join([repr(stmt) for stmt in self.body])
        return f"{indent_str}Function: '{self.name}',\n{indent_str}args: [{args_repr}],\n{indent_str}return_type: {self.return_type},\n{indent_str}body: [\n{indent_str*2}{body_repr}\n{indent_str}]"

class JangConditional:
    def __init__(self, condition, body, else_body=None, indent=0):
        self.condition = condition
        self.body = [stmt.__class__(stmt.value, indent=indent+1) for stmt in body]
        self.else_body = [stmt.__class__(stmt.value, indent=indent+1) for stmt in else_body] if else_body else None
        self.indent = indent

    def __repr__(self):
        indent_str = ' ' * self.indent
        body_repr = ',\n'.join([repr(stmt) for stmt in self.body])
        else_body_repr = ',\n'.join([repr(stmt) for stmt in self.else_body]) if self.else_body else ''
        conditional_str = f"{indent_str}Conditional: {self.condition},\n{indent_str}body: [\n{body_repr}\n{indent_str}]"
        if else_body_repr:
            conditional_str += f"\n{indent_str}else_body: [\n{else_body_repr}\n{indent_str}]"
        return conditional_str
    
class JangLoop:
    def __init__(self, condition, body, indent=0):
        self.condition = condition
        self.body = [stmt.__class__(stmt.value, indent=indent+1) for stmt in body]
        self.indent = indent

    def __repr__(self):
        indent_str = ' ' * self.indent
        body_repr = ',\n'.join([repr(stmt) for stmt in self.body])
        return f"{indent_str}Loop: {self.condition},\n{indent_str}body: [\n{body_repr}\n{indent_str}]"
    
class JangFunctionCall:
    def __init__(self, name, args=None, indent=0):
        self.name = name
        self.args = args
        self.indent = indent

    def __repr__(self):
        indent_str = ' ' * self.indent
        args_repr = ', '.join([repr(arg) for arg in self.args]) if self.args else ''
        return f"{indent_str}FunctionCall: '{self.name}', args: [{args_repr}]"

class JangReturn:
    def __init__(self, value, indent=0):
        self.value = value
        self.indent = indent

    def __repr__(self):
        indent_str = ' ' * self.indent
        return f"{indent_str}Return: {self.value}"

class JangPrint:
    def __init__(self, value, indent=0):
        self.value = value
        self.indent = indent

    def __repr__(self):
        indent_str = ' ' * self.indent
        return f"{indent_str}Print: {self.value}"
