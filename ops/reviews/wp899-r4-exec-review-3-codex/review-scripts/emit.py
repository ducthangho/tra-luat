from pathlib import Path
from pathlib import Path
print((Path(__file__).resolve().parent / 'suite.stdout.txt').read_text(), end='')
