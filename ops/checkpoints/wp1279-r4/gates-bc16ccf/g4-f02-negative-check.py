from pathlib import Path,PureWindowsPath
import json
from g4_native_evidence import verify_nested
D=Path('/workspace/scratch/proxima-p1-s2-20261108/g4-f02-negative-private-copy/proof')
W=PureWindowsPath('C:\\tl-win\\wp1279-r4-g4\\final-bc16ccff3601')
rep=json.loads((D/'measurement.json').read_text(encoding='utf-8-sig'))['phases']['candidate-ps51']['report']
def mapped(p):return D.joinpath(*PureWindowsPath(p).relative_to(W).parts)
verify_nested(rep,mapped,True)
