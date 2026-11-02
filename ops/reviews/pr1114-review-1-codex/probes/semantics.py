import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
REAL_RUN = subprocess.run
rows = {}
for version in ('base', 'head'):
    path = ROOT / 'copies' / version / 'ops/cloud_agent_creds_test.py'
    spec = importlib.util.spec_from_file_location('review_' + version, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    observations = []

    def run(args, **kw):
        wire = kw.get('input') if version == 'head' else args[2].encode('utf-8')
        decoded = json.loads(wire.decode('utf-8'))
        observations.append({'argc': len(args), 'wire_bytes': len(wire),
                             'utf8_decode_ok': True, 'ascii_only': wire.isascii(),
                             'blob_bytes': len(m.base64.b64decode(decoded['p'].get('b64', ''))),
                             'quoted_chars': len(subprocess.list2cmdline(args))})
        return REAL_RUN(args, **kw)

    cases = [
        ('p_none', {}, {'ok': False, 'error': 'AGENT_CREDS_FILEID_MISMATCH'}),
        ('p_empty', {'p': {}}, {'ok': False, 'error': 'AGENT_CREDS_FILEID_MISMATCH'}),
        ('blob_empty', {'p': m._p(b'')}, {'ok': False, 'error': 'BLOB_SIZE'}),
        ('old_file_empty', {'p': m._p(b'new', md5=hashlib.md5(b'').hexdigest()), 'tep': b''}, None),
        ('binary_unicode', {'p': m._p(bytes(range(256)), fid='tệp-🙂-漢字'), 'prop': 'tệp-🙂-漢字'}, None),
        ('throw_unicode', {'p': m._p(), 'nem': True}, {'nem': 'ghi lỗi'}),
        ('boundary_65536', {'p': m._p(b'x' * 65536)}, None),
        ('boundary_65537', {'p': m._p(b'x' * 65537)}, {'ok': False, 'error': 'BLOB_SIZE'}),
    ]
    outputs = {}
    with mock.patch.object(m.subprocess, 'run', run):
        for name, kwargs, expected in cases:
            k = m.chay_b(**kwargs)
            if expected is not None:
                assert k.ra == expected, (name, k.ra)
            else:
                assert k.ra['ok'] is True and k.ghi == 1, (name, k.ra)
            if name == 'binary_unicode':
                assert k.sha == hashlib.sha256(bytes(range(256))).hexdigest()
            outputs[name] = vars(k)
            print(version, name, json.dumps({'ra': k.ra, **observations[-1]}, ensure_ascii=False))
    rows[version] = outputs
    print(version, 'CA_IDS', len(m.CA), 'MUTATION_IDS', len(m.DOT_BIEN))
    (ROOT / 'evidence' / (version + '-case-ids.json')).write_text(json.dumps({
        'cases': list(m.CA), 'mutations': [x[0] for x in m.DOT_BIEN]}, indent=2))

assert rows['base'] == rows['head']
print('BASE_HEAD_SEMANTICS_EQUAL=8/8')
body = m._trich_gs() + m.JS_CHAY
hits = re.findall(r'process\s*\.\s*stdin|\bstdin\b|readFileSync|readSync|require\s*\(|process\s*\.\s*argv', body)
assert not hits, hits
print('EXTRACTED_GS_PLUS_JS_CHAY_STDIN_OR_ARGV_HITS=' + str(hits))
guard = r'''
const fsReview = require('fs');
let stdinReadCount = 0, consumed = false;
const originalReadFileSync = fsReview.readFileSync;
fsReview.readFileSync = function(fd, ...args) {
  if (fd === 0 && ++stdinReadCount > 1) throw new Error('SECOND_STDIN_READ');
  const result = originalReadFileSync.call(this, fd, ...args);
  if (fd === 0) consumed = true;
  return result;
};
for (const method of ['readSync', 'read', 'readv', 'readvSync']) {
  const original = fsReview[method];
  fsReview[method] = function(fd, ...args) {
    if (fd === 0 && consumed) throw new Error('STDIN_ALREADY_CONSUMED');
    return original.call(this, fd, ...args);
  };
}
Object.defineProperty(process, 'stdin', {get() { throw new Error('PROCESS_STDIN_ACCESS'); }});
'''
with tempfile.TemporaryDirectory(prefix='review_semantics_') as tmp:
    js = Path(tmp) / 'b.js'
    js.write_text(guard + m.JS_GIA + body + '\nconsole.error("FD0_READS=" + stdinReadCount);\n', encoding='utf-8')
    payload = {'tep': m.base64.b64encode(m.TEP0).decode(), 'prop': 'tệp-🙂-漢字',
               'p': m._p(bytes(range(256)), fid='tệp-🙂-漢字')}
    wire = json.dumps(payload, ensure_ascii=False).encode('utf-8')
    r = REAL_RUN([m._node(), str(js)], input=wire, capture_output=True, timeout=60)
    assert r.returncode == 0 and b'FD0_READS=1' in r.stderr
    assert json.loads(r.stdout)['sha'] == hashlib.sha256(bytes(range(256))).hexdigest()
    print('RAW_NONASCII_UTF8', 'input_bytes=' + str(len(wire)), 'rc=' + str(r.returncode), r.stderr.decode().strip(), 'binary_sha_matches=True')
    r = REAL_RUN([m._node(), str(js)], input=b'', capture_output=True, timeout=60)
    assert r.returncode == 1 and b'SyntaxError: Unexpected end of JSON input' in r.stderr
    print('EMPTY_STDIN', 'rc=' + str(r.returncode), 'SyntaxError: Unexpected end of JSON input')
    payload['p'] = {}
    r = REAL_RUN([m._node(), str(js)], input=json.dumps(payload).encode(), capture_output=True, timeout=60)
    assert r.returncode == 0 and json.loads(r.stdout)['ra']['error'] == 'AGENT_CREDS_FILEID_MISMATCH'
    print('EMPTY_P_WITH_STDIN_GUARD', 'rc=0', r.stderr.decode().strip(), 'AGENT_CREDS_FILEID_MISMATCH')
print('SEMANTICS_PROBES=PASS')
