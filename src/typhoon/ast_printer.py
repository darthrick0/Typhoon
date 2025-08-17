import os

expressions_path = os.path.join(os.path.dirname(__file__), "expressions.py")

structs: list[dict[str, str | list[str]]] = [
    {
        "class_name": "Binary",
        "data": [
            "left: Expr",
            "operator: Token",
            "right: Expr",
        ]
    },
    {
        "class_name": "Grouping",
        "data": [
            "expression: Expr",
        ]
    },
    {
        "class_name": "Literal",
        "data": [
            "value: object",
        ]
    },
    {
        "class_name": "Unary",
        "data": [
            "operator: Token",
            "right: Expr",
        ]
    },
]


with open(expressions_path, mode="w") as f:

    import_block ="""from abc import ABC
from typing import final, override
from data_definitions import Token
"""
    _ = f.write(import_block)
    # Base Classes
    expr_class = """
class Expr(ABC):
    
    def __init__(self):
        pass

    def accept(self, visitor: object) -> None:
        raise NotImplementedError(f"{self.__class__.__name__} method {__name__} not implemented")

"""

    _ = f.write(expr_class) # basedpyright has problems with not using returned values :(

    # Base Visitor Class
    base_visitor_class = """
class Visitor(ABC):

    def __init__(self):
        pass
"""
    _ = f.write(base_visitor_class)
    for struct in structs:
        arg_str = ', '.join([arg for arg in struct["data"]])
        func_def = f"    def visit_{struct['class_name'].lower()}({arg_str}):\n"
        p = "       pass\n\n"
        _ = f.write(func_def)
        _ = f.write(p)



    # Printer Visitor Class
    printer_visitor_class = """
@final
class PrettyPrinter(Visitor):

    def __init__(self):
        super().__init__()
        print("Pretty Printer Activate!!!!!!")

"""
    _ = f.write(printer_visitor_class)
    for struct in structs:
        arg_str = ', '.join([arg for arg in struct["data"]])
        func_def = f"    def visit_{struct['class_name'].lower()}({arg_str}):\n"
        p = "       pass\n\n"
        _ = f.write(func_def)
        _ = f.write(p)





    # Expression Classes
    for struct in structs:
        arg_str = ', '.join([arg for arg in struct["data"]])
        assignment_str = '\n        '.join([f'self.{arg} = {arg.split(": ")[0]}' for arg in struct["data"]])
        repr_str = ""
        for arg in struct['data']:
            repr_str += "{repr(self." + str(arg.split(": ")[0]) + ")}, " 
        repr_str = f"f'{struct['class_name']}(" + repr_str[:-2] + ")'"

        class_template = f"""
@final
class {struct['class_name']}(Expr):

    @override
    def __init__(self, {arg_str}):
        super().__init__()
        {assignment_str}

    @override
    def accept(self, visitor: object):
        visitor.visit_{struct['class_name'].lower()}(self)

    def __repr__(self):
        return {repr_str}

"""
        _ = f.write(class_template)















