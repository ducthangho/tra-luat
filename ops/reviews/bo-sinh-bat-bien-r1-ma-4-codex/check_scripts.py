from pathlib import Path
import ast
w=Path(__file__).resolve().parent
for p in w.glob('*.py'):
 ast.parse(p.read_text());print('PARSE_OK',p.name)
