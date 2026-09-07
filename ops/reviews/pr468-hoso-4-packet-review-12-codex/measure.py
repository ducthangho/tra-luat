import copy
import datetime as dt
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import yaml

sys.dont_write_bytecode = True
B = Path(__file__).resolve().parents[1]
R = B / 'cay-kho'
O = B / 'do-review12'
os.environ['TMPDIR'] = str(O / 'tmp')
os.environ['PYTHONDONTWRITEBYTECODE'] = '1'


def git(*args):
    return subprocess.check_output(['git', '-C', str(R), *args])


def save(name, value):
    (O / name).write_text(json.dumps(value, ensure_ascii=False, indent=2, default=str) + '\n')


def note(text):
    p = B / 'VERDICT.md'
    s = p.read_text()
    assert s.endswith('verdict: dang-do\n')
    p.write_text(s[:-len('verdict: dang-do\n')] + text + '\n\nverdict: dang-do\n')


def snapshot():
    spec = importlib.util.spec_from_file_location('lease_review12', R / 'ops/lease_publish.py')
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    # Disable only server readback: no fake network or claims about live GitHub.
    rows = m._quet_lease_toan_kho(R, doi_chieu_ref=False)
    now = dt.datetime.now(dt.timezone.utc)
    ids = ['mutant-khong-chay-tren-windows-exec-1-claude-20260906'] + [
        f'gate-tach-job-cat-chi-phi-exec-{x}-claude-20260906' for x in ['1', '1r2', '1r3', '1r4']]
    local = [yaml.safe_load((R / f'ops/leases/{x}.yaml').read_text()) for x in ids]
    edges = []
    for old, new in zip(local, local[1:]):
        edges.append({'old': old['lease_id'], 'new': new['lease_id'],
                      'forward': old.get('da_bi_thay_the') == new['lease_id'],
                      'backward': old['lease_id'] in m._danh_sach_thay_the_cho(new['thay_the_cho'])})
    def holders(data, when):
        result = {}
        for path in ['.github/workflows/ci.yml', '.claude/dev/ci_dang_ky_test.py']:
            active = []
            for row in data:
                lease = row['lease']
                if not m._lease_cham_duong(lease, path):
                    continue
                if m._phan_loai_lease(lease, when) != 'CÒN_HẠN':
                    continue
                tombstone = m._bia_mo_doi_xung(lease, data)
                assert tombstone is not False, row
                if tombstone is None:
                    active.append({k: row[k] for k in ['ref', 'path', 'blob']} | {'lease_id': lease['lease_id']})
            result[path] = {'count': len({x['lease_id'] for x in active}), 'active': active}
        return result
    times = [now] + [dt.datetime.fromisoformat(f'2026-09-07T14:30:{sec}+00:00') for sec in ['06', '07', '08']]
    model = copy.deepcopy(rows)
    for row in model:
        if row['lease']['lease_id'] == ids[0]:
            row['lease']['da_bi_thay_the'] = ids[1]
    old_path = f'ops/leases/{ids[0]}.yaml'
    old_blob = git('rev-parse', f'origin/master:{old_path}').decode().strip()
    refs = git('for-each-ref', '--format=%(refname)', 'refs/heads', 'refs/remotes').decode().splitlines()
    old_refs = []
    for ref in refs:
        if ref.endswith('/HEAD'):
            continue
        out = git('ls-tree', ref, '--', old_path).decode()
        if out and out.split()[2] == old_blob:
            old_refs.append(ref)
    result = {'utc': now.isoformat(), 'head': git('rev-parse', 'HEAD').decode().strip(),
              'snapshot_pairs': len(rows), 'chain_edges': edges,
              'holders': {t.isoformat(): holders(rows, t) for t in times},
              'all_copies_tombstoned_model': holders(model, now), 'old_master_blob': old_blob,
              'old_blob_refs_excluding_HEAD': old_refs,
              'remote_branch_names': [x.removeprefix('refs/remotes/origin/') for x in refs if x.startswith('refs/remotes/origin/') and not x.endswith('/HEAD')],
              'rows': rows}
    save('snapshot.json', result)
    short = {t: {p: d['count'] for p, d in v.items()} for t, v in result['holders'].items()}
    print(json.dumps({'utc': result['utc'], 'snapshot_pairs': len(rows), 'holders': short, 'old_refs': old_refs}, ensure_ascii=False, indent=2))
    note('Kết luận nhỏ — `bia-mo-mot-ref-khong-thu-hoi-moi-ban`: **CHƯA VÁ VỀ MÁY** tại ' + now.isoformat() + '. Tự quét ' + str(len(rows)) + ' cặp blob/path; số người giữ hiện tại và mô phỏng: `' + json.dumps(short, ensure_ascii=False) + '`. Chuỗi thay thế được kiểm từng cạnh; dữ liệu và mô hình đặt bia mộ mọi bản ở `do-review12/snapshot.json`.')


def artifacts():
    root = R / 'ops/reviews'
    p8 = root / 'pr468-hoso-4-packet-review-8-codex'
    p9 = root / 'pr468-hoso-4-packet-review-9-codex/artifact-repair'
    p11 = root / 'pr468-hoso-4-packet-review-11-codex'
    # Recreate documented relative layout using regular copies, no symlinks.
    mapped = O / 'manifest11-layout'
    mapped.mkdir(exist_ok=True)
    shutil.copyfile(root / 'pr468-hoso-4-packet-review-11-codex-verdict.md', mapped / 'VERDICT.md')
    shutil.copyfile(p11 / 'ARTIFACTS.sha256', mapped / 'ARTIFACTS.sha256')
    for line in (p11 / 'ARTIFACTS.sha256').read_text().splitlines():
        _, name = line.split('  ', 1)
        if name == 'VERDICT.md':
            continue
        assert name.startswith('do-review10/') and '..' not in Path(name).parts
        src = p11 / name.removeprefix('do-review10/')
        assert src.is_file() and not src.is_symlink()
        dst = mapped / name
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
    results = []
    for name, path in [('manifest8', p8), ('manifest9-artifact-repair', p9), ('manifest11', mapped)]:
        run = subprocess.run(['sha256sum', '-c', 'ARTIFACTS.sha256'], cwd=path, capture_output=True, text=True)
        (O / f'{name}.stdout').write_text(run.stdout)
        (O / f'{name}.stderr').write_text(run.stderr)
        lines = (path / 'ARTIFACTS.sha256').read_text().splitlines()
        regular = all((path / line.split('  ', 1)[1]).is_file() and not (path / line.split('  ', 1)[1]).is_symlink() for line in lines)
        result = {'name': name, 'rc': run.returncode, 'listed': len(lines),
                  'ok': sum(x.endswith(': OK') for x in run.stdout.splitlines()), 'all_regular': regular}
        results.append(result)
        save('artifacts.json', results)
        note('Kết luận nhỏ — kiểm manifest: `' + json.dumps(result, ensure_ascii=False) + '`; đã chạy `sha256sum -c` thật, lượt 11 ánh xạ đường theo `DOC-MANIFEST.md`.')
    print(json.dumps(results, ensure_ascii=False, indent=2))


def billing():
    path = 'ops/leases/gate-tach-job-cat-chi-phi-exec-1r4-claude-20260906.yaml'
    old = yaml.safe_load(git('show', 'c43347d:' + path))
    new = yaml.safe_load((R / path).read_bytes())
    diff = []
    def walk(a, b, at=''):
        if type(a) is not type(b):
            diff.append({'path': at, 'old': a, 'new': b})
        elif isinstance(a, dict):
            for key in sorted(a.keys() | b.keys()):
                if key not in a or key not in b:
                    diff.append({'path': at + '/' + key, 'old': a.get(key), 'new': b.get(key)})
                else:
                    walk(a[key], b[key], at + '/' + key)
        elif isinstance(a, list):
            if len(a) != len(b):
                diff.append({'path': at, 'old_length': len(a), 'new_length': len(b)})
            else:
                for i, (x, y) in enumerate(zip(a, b)):
                    walk(x, y, at + '/' + str(i))
        elif a != b:
            diff.append({'path': at, 'old': a, 'new': b})
    walk(old, new)
    run = subprocess.run([sys.executable, '-B', 'ops/lease_publish.py', 'check', path], cwd=R, capture_output=True, text=True)
    (O / 'lease-check.stdout').write_text(run.stdout)
    (O / 'lease-check.stderr').write_text(run.stderr)
    result = {'yaml_changed_leaves': diff, 'check_rc': run.returncode, 'check_positive': 'ĐĂNG ĐƯỢC' in run.stdout,
              'projection_equal': (R / path).read_bytes() == (B / 'tai-lieu' / Path(path).name).read_bytes(),
              'old_yaml_keys': len(old), 'new_yaml_keys': len(new)}
    save('billing.json', result)
    (O / 'billing.diff').write_bytes(git('diff', 'c43347d', 'HEAD', '--', path))
    print(json.dumps(result, ensure_ascii=False, indent=2))
    note('Kết luận nhỏ — `bien-do-khac-head-khong-phai-nhieu-runner`: YAML đổi ' + str(len(diff)) + ' giá trị lá (' + ', '.join(x['path'] for x in diff) + '), các trường khác nguyên trạng; `check` rc=' + str(run.returncode) + ', có bằng chứng ĐĂNG ĐƯỢC=' + str(result['check_positive']) + '. Dữ liệu ở `do-review12/billing.json`, diff nguyên văn ở `do-review12/billing.diff`; còn đọc header/provenance trước kết luận cuối.')


if __name__ == '__main__':
    {'snapshot': snapshot, 'artifacts': artifacts, 'billing': billing}[sys.argv[1]]()
