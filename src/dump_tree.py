import javalang

TAB_SPACE = 2

class Colors:
    BLUE = '\033[94m'
    GREY = '\033[37m'
    GREEN = '\033[32m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

def print_color(msg: str, color: Colors, indent:int=0):
    """Imprime un mensaje por pantalla usando colores"""
    print(' ' * TAB_SPACE * indent + f"{color}{msg}{Colors.RESET}")

def dump_javalang_tree(node: javalang.ast.Node, java_code, indent: int=0) -> None:
    """Procesa un AST. Llama a funciones auxiliares para procesar las asignaciones y declaraciones"""
    # imprimo el codigo fuente asociado al nodo, si tiene posicion
    if node.position:
        position = node.position
        line = java_code.splitlines()[position.line - 1]
        print_color(f"Line {position.line}: {line.strip()}", Colors.GREEN, indent)

    # proceso el nodo
    print(f"{'  ' * indent}{type(node).__name__}")
    if isinstance(node, javalang.tree.Assignment):
        print_code_assignment(node, indent)
    elif isinstance(node, javalang.tree.VariableDeclarator):
        print_code_declaration(node, indent)

    # itero los sub-nodos
    for child in node.children:
        if isinstance(child, javalang.ast.Node): # tengo 1 solo hijo
            dump_javalang_tree(child, java_code, indent + 1)
        elif isinstance(child, list): # proceso la lista de hijos
            for item in child:
                if isinstance(item, javalang.ast.Node):
                    dump_javalang_tree(item, java_code, indent + 1)

def print_code_assignment(node: javalang.ast.Node, indent: int=0):
    """Procesa el sub-arbol de una asignacion"""
    if isinstance(node, javalang.tree.Assignment):
        print_color(f"** member={node.expressionl.member}", Colors.BLUE, indent)
        print_color(f"** value={node.value}", Colors.BLUE, indent)

def print_code_declaration(node: javalang.ast.Node, indent: int=0):
    """Procesa el sub-arbol de una declaracion"""
    if node.initializer and isinstance(node.initializer, javalang.tree.ClassCreator):
        print_color(f"** initializer={node.initializer}", Colors.YELLOW, indent)
        print_color(f"** name={node.name}", Colors.YELLOW, indent)


if __name__ == '__main__':
    filename = './java_samples/Target1.java'
    java_code = open(filename).read()
    tree = javalang.parse.parse(java_code)
    dump_javalang_tree(tree, java_code)