import datetime as dt
import hashlib
import json
from pathlib import Path
import re
import subprocess

B = Path(__file__).resolve().parents[1]
R = B / 'cay-kho'
O = B / 'do-review12'
SHA = '02b0b86bf64a89b561a75ff060164332792fb73d'


def git(*args):
    return subprocess.check_output(['git', '-C', str(R), *args]).decode().strip()


state = {'utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'head': git('rev-parse', 'HEAD'),
         'tree': git('rev-parse', 'HEAD^{tree}'), 'status': git('status', '--porcelain'),
         'tracked_diff': git('diff', '--name-only'), 'index_diff': git('diff', '--cached', '--name-only'),
         'new_commits': int(git('rev-list', '--count', SHA + '..HEAD'))}
assert state['head'] == SHA
assert state['tree'] == 'cee08e8eeecbb581c36a2058153b43dc29724b0a'
assert not any(state[k] for k in ['status', 'tracked_diff', 'index_diff', 'new_commits'])
files = [B / 'VERDICT.md'] + [p for p in O.rglob('*') if p.is_file() and not p.is_symlink()
                             and 'tmp' not in p.relative_to(O).parts]
if O / 'final-check.json' not in files:
    files.append(O / 'final-check.json')
files = sorted(set(files), key=lambda p: str(p.relative_to(B)))
state['artifact_count'] = len(files)
p = B / 'VERDICT.md'
s = p.read_text()
assert s.count('__FINAL_CHECK__') == 1
s = s.replace('__FINAL_CHECK__',
              f"Kiểm cuối **{state['utc']}**: HEAD/tree đúng như bảng; status, diff tracked và index đều rỗng; **0 commit** sau reviewed_sha. Kết quả ở `do-review12/final-check.json`. "
              f"`ARTIFACTS.sha256` bao phủ **{len(files)} tệp thường** gồm VERDICT và hiện vật mới; không liệt kê symlink hoặc bất kỳ thành phần đường dẫn tương đối `tmp`. Đã kiểm lại bằng `sha256sum -c ARTIFACTS.sha256`.")
s = s.replace('verdict: dang-do', 'verdict: changes_requested')
assert s.endswith('verdict: changes_requested\n')
findings = re.findall(r'^### ([a-z0-9-]+)  \[(P[123])\]', s, re.M)
assert len(findings) == 4 and sum(x[1] == 'P1' for x in findings) == 2 and sum(x[1] == 'P2' for x in findings) == 2
for _, block in re.findall(r'(^### [^\n]+\n)(.*?)(?=^### |^## |\Z)', s, re.M | re.S):
    assert all(label in block for label in ['TỆP/DÒNG:', 'VẤN ĐỀ:', 'ĐÃ THỬ VÁ:', 'ĐÃ THỬ NGHIỆM:', 'ĐỘ TIN:'])
for slug in ['bia-mo-mot-ref-khong-thu-hoi-moi-ban', 'bien-do-khac-head-khong-phai-nhieu-runner',
             'manifest-luot8-liet-ke-hien-vat-khong-duoc-giao']:
    assert slug in s.split('## BẢNG ĐO')[0]
assert 'dang-do' not in s and '__FINAL_CHECK__' not in s
p.write_text(s)
state['findings'] = findings
state['verdict_sha256'] = hashlib.sha256(p.read_bytes()).hexdigest()
(O / 'final-check.json').write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n')
lines = []
for f in files:
    assert f.is_file() and not f.is_symlink()
    rel = f.relative_to(B)
    assert 'tmp' not in rel.parts
    lines.append(hashlib.sha256(f.read_bytes()).hexdigest() + '  ' + rel.as_posix())
(B / 'ARTIFACTS.sha256').write_text('\n'.join(lines) + '\n')
run = subprocess.run(['sha256sum', '-c', 'ARTIFACTS.sha256'], cwd=B, capture_output=True, text=True)
assert run.returncode == 0, run.stderr
ok = sum(line.endswith(': OK') for line in run.stdout.splitlines())
assert ok == len(files)
print(json.dumps(state, ensure_ascii=False, indent=2))
print(f'ARTIFACTS.sha256: {ok}/{len(files)} OK; rc={run.returncode}; regular only, no tmp/symlink.')
