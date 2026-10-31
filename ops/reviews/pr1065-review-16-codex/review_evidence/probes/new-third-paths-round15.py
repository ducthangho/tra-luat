from pathlib import Path
import subprocess, json, shutil

r = Path(__file__).resolve().parents[1]
rows = []
for mode in ['control', 'post-rc9', 'post-empty', 'post-cannot-start']:
    log = r/'evidence'/f'new-post-{mode}.json'
    fixture = r/'fixtures'/f'new-post-{mode}'
    shutil.rmtree(fixture, ignore_errors=True)
    for suffix in ['', '.native.jsonl', '.install.jsonl', '.independent.jsonl']:
        Path(str(log)+suffix).unlink(missing_ok=True)
    cmd = [str(r/'pwsh/pwsh'), '-NoProfile', '-File', str(r/'probes/system-post-failure.ps1'),
           '-Mode', mode, '-Log', str(log), '-FixtureRoot', str(fixture)]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=90)
    (r/'evidence'/f'new-post-{mode}.log').write_text(p.stdout+p.stderr)
    d = json.loads(log.read_text())
    native = [json.loads(x) for x in Path(str(log)+'.native.jsonl').read_text().splitlines()]
    installs = [json.loads(x) for x in Path(str(log)+'.install.jsonl').read_text().splitlines()]
    direct = []
    for x in installs:
        exe = Path(x['target'])
        try:
            q = subprocess.run([str(exe), '--version'], capture_output=True, text=True,
                               env={**__import__('os').environ, 'REVIEW_NULL_MODE': mode,
                                    'REVIEW_SYSTEM_LOG': str(log)+'.independent.jsonl'})
            direct.append(dict(exists=exe.exists(), marker=Path(str(exe)+'.installed').exists(), rc=q.returncode, stdout=q.stdout.strip()))
        except OSError as e:
            direct.append(dict(exists=exe.exists(), marker=Path(str(exe)+'.installed').exists(), rc=None, error=type(e).__name__))
    good = mode == 'control'
    tools = [x for x in d['ket_qua'] if x['cong_cu'] != 'commander']
    assert p.returncode == (0 if good else 1) and d['ok'] == good
    assert d['loi'] == (0 if good else 4) and len(tools) == 4
    assert all(x['hanh_dong'] == ('nang_cap' if good else 'loi') for x in tools)
    assert len(installs) == 4 and all(x['verified'] for x in installs)
    assert all(x['exists'] and x['marker'] for x in direct)
    assert len([x for x in native if x['rc'] == 0]) >= 4
    if mode == 'post-rc9':
        assert all(x['rc'] == 9 and x['stdout'] for x in direct)
    elif mode == 'post-empty':
        assert all(x['rc'] == 0 and x['stdout'] == '' for x in direct)
    elif mode == 'post-cannot-start':
        assert all(x['rc'] is None and x['error'] == 'PermissionError' for x in direct)
    else:
        assert all(x['rc'] == 0 and x['stdout'] for x in direct)
    row = dict(mode=mode, rc=p.returncode, ok=d['ok'], errors=d['loi'], installs=len(installs),
               rows=[(x['cong_cu'], x['hanh_dong']) for x in tools], direct=direct)
    rows.append(dict(command=cmd, summary=row))
    print(json.dumps(row, ensure_ascii=False), flush=True)
    shutil.rmtree(fixture, ignore_errors=True)
(r/'evidence/new-third-paths-round15.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2))
print('New post-install native failures: 4/4 PASS; control upgrades, rc9/empty/cannot-start each 4 loi')
with (r/'evidence/legacy-verdict-discard.md').open('a') as f:
    f.write('\nHƯỚNG 9: đường thứ ba — native chỉ hỏng SAU installer thành công\n'
            '  giả thuyết : rc0 của installer hoặc phiên bản trước còn sót làm hậu cài HeThong được ĐẠT dù getter sau cài thất bại.\n'
            '  lệnh       : python3 -u probes/new-third-paths-round15.py > evidence/new-third-paths-round15.log 2>&1\n'
            '  output     : New post-install native failures: 4/4 PASS; control exit0/4nang_cap; post-rc9 (in đúng token nhưng rc9), post-empty (rc0), post-cannot-start (tệp còn nhưng chmod -x) đều exit1/ok=false/4loi. Mỗi ca có4installer, băm đo lại tại spawn đều đúng,4marker; đo trực tiếp ngoài sản phẩm xác nhận lỗi hậu cài.\n'
            '  kết luận   : KHÔNG PHẢI LỖI ở đường mới đã đo. Getter/so đích/main-tail sản phẩm nguyên byte; lỗi được kích hoạt bởi installer marker, không giả Add-KetQua. HTTP/ACL/MSI/tasks là mô hình ngoại tuyến; native/file/rc là thật trên Linux, không chứng nhận Windows.\n')
