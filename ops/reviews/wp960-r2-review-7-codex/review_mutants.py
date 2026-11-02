import hashlib
import shutil
import sys
from review_common import HEAD, SCRATCH, case, emit, invoke, load_tests

t = load_tests()
mutants = {
    'v1': (' or ra[0] != oid40', '', 'c94'),
    'v2': (' or ra[1] not in ("commit", "tag", "tree", "blob")', '', 'c94'),
    'v3': ('if len(x) == 40 or _oid_tron(x):', 'if len(x) == 40:', 'c87'),
    'n1-window-before': ('cua = dong_tep[max(0, j - 1):j + 2]', 'cua = dong_tep[j:j + 2]', 'c88'),
    'n2-commit-case': ('_RE_SAU_COMMIT = re.compile(r"\\bcommit\\s*\\Z", re.IGNORECASE)',
                       '_RE_SAU_COMMIT = re.compile(r"\\bcommit\\s*\\Z")', 'c87'),
    'n3-review-round-order': ('lon = sorted(t for t, lu in sau if lu > luot_nay)',
                              'lon = sorted(t for t, lu in sau if lu < luot_nay)', 'c69'),
    'n4-provider-next-boundary': ('cua = dong_tep[max(0, j - 1):j + 2]',
                                'cua = dong_tep[max(0, j - 1):j + 3]', 'c88'),
    'n5-citation-line-digit': ('_RE_TRICH_DAN = re.compile(r"[\\w./-]+\\.[A-Za-z0-9]+:\\d+")',
                              '_RE_TRICH_DAN = re.compile(r"[\\w./-]+\\.[A-Za-z0-9]+:\\d{2,}")', 'c88'),
    'n6-luot-bool': ('isinstance(v, int) and not isinstance(v, bool)', 'isinstance(v, int)', 'c70'),
    'n7-citation-current-only': ('any(_RE_TRICH_DAN.search(x) for x in cua)',
                               '_RE_TRICH_DAN.search(dong)', 'c88'),
    'n8-provider-prev-boundary': ('cua = dong_tep[max(0, j - 1):j + 2]',
                                 'cua = dong_tep[max(0, j - 2):j + 2]', 'c88'),
}
name = sys.argv[1]
old, new, target = mutants[name]
emit(mutant=name, old=old, new=new, target=target)
if '--all' in sys.argv:
    root = SCRATCH / ('whole-' + name)
    shutil.copytree(HEAD, root)
    product = root / 'ops/bien_nhan_v2.py'
    text = product.read_text()
    assert text.count(old) == 1
    product.write_text(text.replace(old, new))
    digest = hashlib.sha256(product.read_bytes()).hexdigest()
    t = load_tests(root)
else:
    t._dot_bien_tep(old, new)
state, message = invoke(t, target)
control = t._sach_hoan_toan(case(t, 'c18'))
emit(mutant=name, control=control, file=t.CONG)
if '--all' in sys.argv:
    states = [(fn.__name__, *t._chay_1(fn)) for fn in t.CA]
    emit(mutant=name, passed=sum(s[1] == 'qua' for s in states), total=len(states),
         red=[s for s in states if s[1] != 'qua'])
    assert hashlib.sha256(product.read_bytes()).hexdigest() == digest
    emit(mutant=name, persisted_sha256=digest)
