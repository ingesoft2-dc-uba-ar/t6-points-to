"""Helper module to run SWI-Prolog programs from Python via subprocess."""

import os
import re
import shutil
import subprocess
import tempfile


class PrologError(Exception):
    """Raised when SWI-Prolog is not found or a Prolog program fails."""
    pass


def _find_swipl() -> str:
    """Find the swipl executable.

    Search order:
    1. SWIPL_PATH environment variable
    2. PATH (via shutil.which)
    3. Common Windows install locations
    """
    # 1. env var
    env_path = os.environ.get("SWIPL_PATH")
    if env_path and os.path.isfile(env_path):
        return env_path

    # 2. PATH
    found = shutil.which("swipl")
    if found:
        return found

    # 3. common Windows paths
    for prog_dir in [os.environ.get("ProgramFiles", r"C:\Program Files"),
                     os.environ.get("ProgramFiles(x86)", r"C:\Program Files (x86)")]:
        if prog_dir:
            candidate = os.path.join(prog_dir, "swipl", "bin", "swipl.exe")
            if os.path.isfile(candidate):
                return candidate

    raise PrologError(
        "No se encontró SWI-Prolog (swipl).\n"
        "Instrucciones de instalación:\n"
        "  - Linux:   sudo apt-get install swi-prolog\n"
        "  - macOS:   brew install swi-prolog\n"
        "  - Windows: descargar desde https://www.swi-prolog.org/download/stable\n"
        "También se puede definir la variable de entorno SWIPL_PATH con la ruta al ejecutable."
    )


def quote_atom(s: str) -> str:
    """Quote a string as a Prolog atom if needed.

    Atoms that start with uppercase or contain special characters
    need to be quoted with single quotes in Prolog.
    Examples: 'Obj0', 'Carlos', but x stays as x.
    """
    if not s:
        return "''"
    # already quoted
    if s.startswith("'") and s.endswith("'"):
        return s
    # safe atoms: start with lowercase letter or underscore, contain only alnum/underscore
    if re.match(r'^[a-z_][a-zA-Z0-9_]*$', s):
        return s
    # need quoting: escape internal single quotes
    escaped = s.replace("\\", "\\\\").replace("'", "\\'")
    return f"'{escaped}'"


def parse_output(raw: str, prefix: str) -> list[tuple]:
    """Parse pipe-delimited output lines that start with a given prefix.

    Example input line: "POINTS_TO|x|Obj0"
    With prefix="POINTS_TO" returns [("x", "Obj0")]
    """
    results = []
    for line in raw.splitlines():
        line = line.strip()
        if not line or not line.startswith(prefix + "|"):
            continue
        parts = line.split("|")
        # first element is the prefix, rest are the tuple values
        results.append(tuple(parts[1:]))
    return results


class PrologRunner:
    """Runs SWI-Prolog programs via subprocess."""

    def __init__(self):
        self._swipl = _find_swipl()

    def run(self, new_facts, assign_facts, store_facts, load_facts,
            rules_file: str) -> tuple[list[tuple], list[tuple]]:
        """Run points-to analysis using Prolog.

        Args:
            new_facts: list of (var, obj) tuples
            assign_facts: list of (dest, src) tuples
            store_facts: list of (var, field, var) tuples
            load_facts: list of (var, var, field) tuples
            rules_file: path to the .pl file containing points_to/heap_field rules

        Returns:
            (points_to, heap_field) where each is a list of tuples
        """
        lines = []

        # declare fact predicates as dynamic so empty cases don't error
        lines.append(":- dynamic new/2, assign/2, store/3, load/3.")
        lines.append("")

        # inline the rules file content
        with open(rules_file) as f:
            lines.append(f.read())
        lines.append("")

        # facts
        for x, o in new_facts:
            lines.append(f"new({quote_atom(x)}, {quote_atom(o)}).")
        for x, y in assign_facts:
            lines.append(f"assign({quote_atom(x)}, {quote_atom(y)}).")
        for x, f, y in store_facts:
            lines.append(f"store({quote_atom(x)}, {quote_atom(f)}, {quote_atom(y)}).")
        for x, y, f in load_facts:
            lines.append(f"load({quote_atom(x)}, {quote_atom(y)}, {quote_atom(f)}).")

        lines.append("")

        # query harness: use ~a to print atoms without quotes
        lines.append(":- forall(points_to(X, O),")
        lines.append("    format('POINTS_TO|~a|~a~n', [X, O])).")
        lines.append(":- forall(heap_field(O1, F, O2),")
        lines.append("    format('HEAP_FIELD|~a|~a|~a~n', [O1, F, O2])).")
        lines.append(":- halt.")

        program = "\n".join(lines)
        raw = self._execute(program)

        points_to = parse_output(raw, "POINTS_TO")
        heap_field = parse_output(raw, "HEAP_FIELD")
        return points_to, heap_field

    def run_program(self, source: str) -> str:
        """Run an arbitrary Prolog program and return stdout.

        Used by standalone examples like abuelo.py and conocido.py.
        """
        return self._execute(source)

    def _execute(self, program: str) -> str:
        """Write program to a temp file and execute swipl."""
        tmp = None
        try:
            tmp = tempfile.NamedTemporaryFile(
                mode="w", suffix=".pl", delete=False, encoding="utf-8"
            )
            tmp.write(program)
            tmp.close()

            result = subprocess.run(
                [self._swipl, "-q", "-l", tmp.name],
                capture_output=True, text=True, timeout=10,
            )

            if result.returncode != 0:
                raise PrologError(
                    f"SWI-Prolog terminó con código {result.returncode}.\n"
                    f"stderr: {result.stderr}\n"
                    f"programa:\n{program}"
                )

            return result.stdout

        except subprocess.TimeoutExpired:
            raise PrologError("SWI-Prolog excedió el tiempo límite de 10 segundos.")
        finally:
            if tmp and os.path.exists(tmp.name):
                os.unlink(tmp.name)
