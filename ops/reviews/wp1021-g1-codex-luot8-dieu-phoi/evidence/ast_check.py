import ast
import hashlib
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT / 'cay-kho'
OLD = 'c8a493c0bb8afe0cfb8448e9220b661ed0f6aaa8'
NEW = '356a27e1378b2162bbc0be2ec06ff08fdacbdead'

def git(*args):
    return subprocess.check_output(['git', '-C', str(REPO), *args])

class StripDocs(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        return self.strip(node)
    visit_AsyncFunctionDef = visit_FunctionDef
    def visit_ClassDef(self, node):
        return self.strip(node)
    def visit_Module(self, node):
        return self.strip(node)
    def strip(self, node):
        self.generic_visit(node)
        if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant) and isinstance(node.body[0].value.value, str):
            node.body = node.body[1:]
        return node

result = {'head': git('rev-parse', 'HEAD').decode().strip(), 'files': [], 'changed_docs': []}
assert result['head'] == NEW
for rel in ('ops/bien_nhan_v2.py', 'ops/bien_nhan_v2_test.py'):
    old = git('show', f'{OLD}:{rel}')
    new = git('show', f'{NEW}:{rel}')
    assert new == (REPO / rel).read_bytes()
    trees = [ast.parse(x) for x in (old, new)]
    docs = [{n.name: (n.lineno, ast.get_docstring(n, clean=False)) for n in ast.walk(t) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))} for t in trees]
    for name, (line, doc) in docs[1].items():
        if name in docs[0] and docs[0][name][1] != doc:
            result['changed_docs'].append({'file': rel, 'function': name, 'line': line, 'old': docs[0][name][1], 'new': doc})
    dumps = [ast.dump(StripDocs().visit(t), include_attributes=False) for t in trees]
    same = dumps[0] == dumps[1]
    assert same, rel
    result['files'].append({'path': rel, 'source_sha256': hashlib.sha256(new).hexdigest(), 'ast_equal_without_docstrings': same, 'ast_sha256': hashlib.sha256(dumps[1].encode()).hexdigest()})
assert git('diff', OLD, NEW) == (ROOT / 'diff-tu-luot7.patch').read_bytes()
assert git('diff', 'b29da0bfe3bfb7a7be69136a1c5c40f82c088a93', NEW) == (ROOT / 'diff.patch').read_bytes()
print(json.dumps(result, ensure_ascii=False, indent=2))
