from pathlib import Path

root = Path(__file__).resolve().parents[1]
path = root / 'copies/head/ops/cloud_agent_creds_test.py'
source = path.read_text()
for name, old, new in (
    ('probe_no_input.py', ', input=json.dumps({"tep": base64.b64encode(tep).decode(), "prop": prop, "p": p or {}, **st}).encode()', ''),
    ('probe_argv_read.py', "require('fs').readFileSync(0, 'utf8')", 'process.argv[2]'),
):
    assert source.count(old) == 1
    target = path.with_name(name)
    mutated = source.replace(old, new)
    if target.exists():
        assert target.read_text() == mutated
    else:
        target.write_text(mutated, encoding='utf-8')
    print(name, 'exactly_one_replacement=True')
