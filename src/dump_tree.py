import javalang

def dump_javalang_tree(node: javalang.ast.Node, indent: int=0) -> None:
    """Procesa un AST. Llama a funciones auxiliares para procesar las asignaciones y declaraciones"""

    # proceso el nodo
    print(f"{'  ' * indent}{type(node).__name__}")
    if isinstance(node, javalang.tree.Assignment):
        print_code_assignment(node, indent)
    elif isinstance(node, javalang.tree.VariableDeclarator):
        print_code_declaration(node, indent)

    # itero los sub-nodos
    for child in node.children:
        if isinstance(child, javalang.ast.Node): # tengo 1 solo hijo
            dump_javalang_tree(child, indent + 1)
        elif isinstance(child, list): # proceso la lista de hijos
            for item in child:
                if isinstance(item, javalang.ast.Node):
                    dump_javalang_tree(item, indent + 1)

def print_code_assignment(node: javalang.ast.Node, indent: int=0):
    """Procesa el sub-arbol de una asignacion"""
    if node.value and isinstance(node.value, javalang.tree.ClassCreator):
        print(' ' * 4 * indent + f"** member={node.expressionl.member}")

def print_code_declaration(node: javalang.ast.Node, indent: int=0):
    """Procesa el sub-arbol de una declaracion"""
    if node.initializer and isinstance(node.initializer, javalang.tree.ClassCreator):
        print(' ' * 4 * indent + f"** initializer={node.initializer}")
        print(' ' * 4 * indent + f"** name={node.name}")


if __name__ == '__main__':
    filename = 'java_samples/Target1.java'
    java_code = open(filename).read()
    tree = javalang.parse.parse(java_code)
    dump_javalang_tree(tree)
