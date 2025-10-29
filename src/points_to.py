import os
import glob

import javalang
import networkx as nx
import matplotlib.pyplot as plt
from pyDatalog import pyDatalog


FOLDER_FACTS = "facts"
FOLDER_JAVA_SAMPLES = "java_samples"
FOLDER_IMAGES = "images"


# los terms de pyDatalog solo se pueden definir a nivel de modulo :-/
pyDatalog.create_terms('PointsTo, New, Assign, Store, Load, HeapField, X, Y, F, O1, O2') # COMPLETAR


class PointsToAnalyzer:
    def analyze(self, filename: str) -> None:
        """Metodo principal: hace el analisis de points to del archivo Java filename."""
        new_facts, assign_facts, store_facts, load_facts = self.extract_facts(filename)
        points_to, heap_field = self.infer_from_facts(new_facts, assign_facts, store_facts, load_facts)
        self.display(points_to, heap_field)

    def extract_facts(self, filename: str) -> tuple[list, list, list, list]:
        """Extrae los facts de un AST. Solo considera las operaciones relevantes."""
        print(f"Analizando {filename}")

        with open(filename) as f:
            java_code = f.read()
        tree = javalang.parse.parse(java_code)
        self.dump_javalang_tree(tree) # para debug

        assign_facts = []
        new_facts = []
        store_facts = []
        load_facts = []

        # declaraciones
        for _, node in tree.filter(javalang.tree.VariableDeclarator):
            if node.initializer and isinstance(node.initializer, javalang.tree.ClassCreator):
                # Obj a = New Obj();
                new_facts.append((node.name, f"Obj{len(new_facts)}"))
            # elif ...
                # Obj a = b;
                # Obj a = b.f;
                # COMPLETAR

        # asignaciones
        for _, node in tree.filter(javalang.tree.Assignment):
            pass
                # COMPLETAR
                #   a.f = b;
                #   a = b.f
                #   a = New Obj();
                #   a = b;

        # guardo los facts en disco
        self.write_facts_to_disk(filename, new_facts, assign_facts, store_facts, load_facts)

        return new_facts, assign_facts, store_facts, load_facts

    def infer_from_facts(self, new_facts, assign_facts, store_facts, load_facts) -> tuple[list, list]:
        # si no tengo facts agrego valores dummy (para evitar que el analisis de datalog falle)
        assign_facts = assign_facts or [(None, None)]
        new_facts = new_facts or [(None, None)]
        load_facts = load_facts or [(None, None, None)]
        store_facts = store_facts or [(None, None, None)]

        # genero los facts en datalog
        # (el orden no importa porque es flow-insensitive)
        for x, o in new_facts:
            print(f"new_fact={x} -> {o}")
            +New(x, o)

        for x, y in assign_facts:
            print(f"assign={x} -> {y}")
            +Assign(x, y)

        for x, y, f in load_facts:
            print(f"load={x} -> {y}.{f}")
            +Load(x, y, f)

        for x, f, y in store_facts:
            print(f"store={x}.{f} -> {y}")
            +Store(x, f, y)

        try:
            points_to = [(str(a), str(b)) for (a, b) in PointsTo(X, Y).data if a and b]
        except:
            points_to = [] # por si falla la evaluacion de datalog

        try:
            heap_field = [(str(a), str(f), str(b)) for (a, f, b) in HeapField(X, F, Y).data if a and f and b]
        except:
            heap_field = [] # por si falla la evaluacion de datalog

        return points_to, heap_field

    def display(self, points_to: set, heap_field: set) -> None:
        self.display_text(points_to, heap_field)
        self.display_matplotlib(points_to, heap_field)

    def display_text(self, points_to: set, heap_field: set) -> None:
        """Muestra las relaciones por pantalla"""
        print("\n=== Relación PointsTo ===")
        for a, b in points_to:
            print(f"{a} → {b}")

        print("\n=== Relación HeapField ===")
        for a, f, b in heap_field:
            print(f"{a}.{f} → {b}")

    def display_matplotlib(self, points_to: set, heap_field: set) -> None:
        """Genera un grafico usando matplotlib y lo muestra por pantalla"""
        G = nx.DiGraph()

        # Variables → Objetos
        for src, tgt in points_to:
            G.add_edge(src, tgt, label='', color='black')

        # Campos en el heap
        for o1, f, o2 in heap_field:
            G.add_edge(o1, o2, label=str(f), color='green')
            print(f"Added {o1}.{f} -> {o2}")

        # agrego los nodos y los ejes al grado
        fig = plt.figure()
        pos = nx.spring_layout(G, seed=41, k=1, iterations=100)  # para que siempre se vea igual
        edge_colors = [G[u][v]['color'] for u, v in G.edges()]
        edge_labels = nx.get_edge_attributes(G, 'label')
        nx.draw_networkx_nodes(G, pos, node_size=100, node_color='lightblue', node_shape='o')
        nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=1, arrows=True, arrowstyle='-|>', connectionstyle="arc3,rad=0.2")
        nx.draw_networkx_labels(G, pos, font_size=10, font_color='black')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=9, font_color='green')
        fig.canvas.manager.set_window_title(filename)

        # grabo a disco
        img_filename = f"{FOLDER_IMAGES}/{os.path.basename(filename)}"
        img_filename = img_filename.replace('.java', '.jpg')
        plt.savefig(img_filename)

        # muestro por pantalla
        plt.show()

    def dump_javalang_tree(self, node: javalang.ast.Node, indent: int=0) -> None:
        """Metodo auxiliar que muestra por pantalla el AST"""
        print(f"{'  ' * indent}{type(node).__name__}")
        for child in node.children:
            if isinstance(child, javalang.ast.Node): # tengo 1 solo hijo
                self.dump_javalang_tree(child, indent + 1)
            elif isinstance(child, list): # proceso la lista de hijos
                for item in child:
                    if isinstance(item, javalang.ast.Node):
                        self.dump_javalang_tree(item, indent + 1)

    def write_facts_to_disk(self, filename, new_facts, assign_facts, store_facts, load_facts) -> None:
        """Guarda los facts en archivos en el folder /facts"""
        fn = os.path.basename(filename)
        fn = os.path.join(FOLDER_FACTS, fn)

        with open(fn + ".new.facts", 'w') as f:
            [f.write(f"{a} {b}\n") for (a, b) in new_facts]

        with open(fn + ".assign.facts", 'w') as f:
            [f.write(f"{a} {b}\n") for (a, b) in assign_facts]

        with open(fn + ".store.facts", 'w') as f:
            [f.write(f"{a}.{field} {b}\n") for (a, field, b) in store_facts]

        with open(fn + ".load.facts", 'w') as f:
            [f.write(f"{a} {b}.{field}\n") for (a, b, field) in load_facts]

    def read_facts_from_disk(self, filename: str) -> list[tuple]:
        """Lee facts de un archivo. Los elementos estan separados por espacio"""
        with open(filename) as f:
            return [tuple(line.strip().split()) for line in f if line.strip()]


if __name__ == '__main__':
    pta = PointsToAnalyzer()
    for filename in glob.glob(f"{FOLDER_JAVA_SAMPLES}/*.java"):
        pyDatalog.clear() # limpio lo que pueda haber quedado de la iteracion anterior

        # agrego las reglas de points-to
        PointsTo(X, O1) <= New(X, O1)
        HeapField(O1, F, O2) <= Store(X, F, Y) # INCOMPLETO!
        # COMPLETAR

        # corro el analisis
        pta.analyze(filename)
