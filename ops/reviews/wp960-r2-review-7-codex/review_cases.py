import sys
from review_common import case, emit, invoke, load_tests

t = load_tests()
original_measure = t._kiem_cau
original_cli = t._chay_cli


def measure(*args, **kw):
    rc, errors, stats = original_measure(*args, **kw)
    emit(probe='kiem', rc=rc, debt=bool(kw.get('no') or (len(args) > 2 and args[2])),
         errors=errors, unknown=stats.get('chua_do'), debts=stats.get('no_cau'))
    return rc, errors, stats


def cli(*args, **kw):
    rc, stderr = original_cli(*args, **kw)
    emit(probe='CLI', rc=rc, debt=bool(kw.get('no_cau') or (len(args) > 2 and args[2])), stderr=stderr)
    return rc, stderr


t._kiem_cau, t._chay_cli = measure, cli
groups = {
    'acceptance': ['c69', 'c70', 'c71', 'c72', 'c73', 'c74', 'c75', 'c78', 'c79', 'c83', 'c86', 'c87', 'c88'],
    'closure': ['c77', 'c82', 'c84', 'c89', 'c90', 'c91', 'c92', 'c93', 'c94', 'c95', 'c96'],
}
results = [invoke(t, p)[0] for p in groups[sys.argv[1]]]
emit(group=sys.argv[1], passed=results.count('qua'), total=len(results))
assert set(results) == {'qua'}
