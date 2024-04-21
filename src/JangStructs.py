class JangArgs:
    def __init__(self, type, name):
        self.type = type
        self.name = name

    def __repr__(self):
        indent_str = ' '
        return f"{indent_str}{self.type} : {self.name}"