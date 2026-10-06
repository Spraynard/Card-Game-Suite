"""Convert camelCase identifiers and filenames in a Python project to snake_case."""

import ast
import io
import re
import subprocess
import tokenize
from collections import Counter
from pathlib import Path

ROOT = Path(".")
SKIP_DIRS = {".git", ".venv", "venv", "__pycache__", ".idea"}

CAMEL_RE = re.compile(r"[a-z][a-zA-Z0-9]*[A-Z][a-zA-Z0-9]*$")


def to_snake(name: str) -> str:
    # handles "myVar", "getHTTPResponse" etc. (classic two-pass regex)
    name = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
    return name.lower()

    # --- Step 1: collect names DEFINED by the project -------------------------------


def collect_names(tree):
    names = set()

    class V(ast.NodeVisitor):
        def visit_FunctionDef(self, node):
            names.add(node.name)
            args = node.args
            for a in (*args.posonlyargs, *args.args, *args.kwonlyargs):
                names.add(a.arg)
            if args.vararg:
                names.add(args.vararg.arg)
            if args.kwarg:
                names.add(args.kwarg.arg)
            self.generic_visit(node)

        visit_AsyncFunctionDef = visit_FunctionDef

        def _target(self, t):
            if isinstance(t, ast.Name):
                names.add(t.id)
            elif isinstance(t, (ast.Tuple, ast.List)):
                for e in t.elts:
                    self._target(e)

        def visit_Assign(self, node):
            for t in node.targets:
                self._target(t)
            self.generic_visit(node)

        def visit_AnnAssign(self, node):
            self._target(node.target)
            self.generic_visit(node)

        def visit_Attribute(self, node):
            # only attributes you ASSIGN (e.g. self.myAttr = ...) get renamed
            if isinstance(node.ctx, ast.Store):
                names.add(node.attr)
            self.generic_visit(node)

    V().visit(tree)
    return names


pyfiles = [p for p in ROOT.rglob("*.py") if not SKIP_DIRS & set(p.parts)]

defined = set()
for p in pyfiles:
    try:
        defined |= collect_names(ast.parse(p.read_text(encoding="utf-8")))
    except SyntaxError as e:
        print(f"SKIPPED {p }: {e }")

        # Classes (PascalCase) and constants (SCREAMING_SNAKE) are excluded by CAMEL_RE
renames = {n: to_snake(n) for n in sorted(defined) if CAMEL_RE.fullmatch(n)}

# Collision check: myVar and my_var can't both become my_var
dupes = [s for s, c in Counter(renames.values()).items() if c > 1]
if dupes:
    raise SystemExit(f"Collision after conversion, fix manually: {dupes }")

    # --- Step 2: rewrite NAME tokens only (strings/comments/docstrings untouched) ---


def rewrite(src: str) -> str:
    toks = tokenize.generate_tokens(io.StringIO(src).readline)
    out = [
        (
            tokenize.NAME if t.string in renames else t.type,
            renames.get(t.string, t.string),
        )
        for t in toks
    ]
    return tokenize.untokenize(out)


for p in pyfiles:
    src = p.read_text(encoding="utf-8")
    new = rewrite(src)
    if new != src:
        p.write_text(new, encoding="utf-8")
        print(f"rewrote {p }")

        # --- Step 3: rename files (imports already fixed by step 2) --------------------
for p in sorted(pyfiles, key=lambda x: -len(x.parts)):  # deepest first
    if re.search(r"[A-Z]", p.name):
        new = p.with_name(to_snake(p.stem) + p.suffix)
        subprocess.run(["git", "mv", str(p), str(new)], check=True)
        print(f"renamed {p } -> {new }")
