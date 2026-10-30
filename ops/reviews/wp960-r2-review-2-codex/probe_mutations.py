"""Offline reviewer mutations, using the existing test harness on a copy."""
import importlib.util
import json
import sys
import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path('/tmp/wp960-r2-l2-copy')

MUTATIONS = {
    'r1-commit-case': ('_RE_SAU_COMMIT = re.compile(r"\\bcommit\\s*\\Z", re.IGNORECASE)',
                       '_RE_SAU_COMMIT = re.compile(r"\\bcommit\\s*\\Z")'),
    'r2-commit-boundary': ('r"\\bcommit\\s*\\Z"', 'r"commit\\s*\\Z"'),
    'r3-commit-adjacent': ('r"\\bcommit\\s*\\Z"', 'r"\\bcommit\\s*"'),
    'r4-backtick-close': ('if truoc.endswith("`") and sau.startswith("`"):',
                          'if truoc.endswith("`"):'),
    'r5-provider-boundary': ('r"\\bprovider\\b"', 'r"provider"'),
    'r6-window-next': ('cua = dong_tep[max(0, j - 1):j + 2]',
                       'cua = dong_tep[max(0, j - 1):j + 1]'),
    'r7-window-prev': ('cua = dong_tep[max(0, j - 1):j + 2]',
                       'cua = dong_tep[j:j + 2]'),
    'r8-receipt-encoding': ('except (UnicodeDecodeError, OSError) as ex:\n            raise KhongDoDuoc',
                            'except OSError as ex:\n            raise KhongDoDuoc'),
    'r9-rethrow-alias': ('        except KhongDoDuoc:\n            raise\n', ''),
}

for name in (sys.argv[1:] if __name__ == '__main__' else []):
    old, new = MUTATIONS[name]
    failures = []
    with tempfile.TemporaryDirectory(prefix='wp960-valid-mutant-') as temp:
        mutant_root = Path(temp)/'repo'
        subprocess.run(['git','clone','--shared','--no-checkout','--quiet',str(ROOT),str(mutant_root)], check=True)
        subprocess.run(['git','-C',str(mutant_root),'checkout','--quiet','--detach','ae0d06c23fb777545fd7547a07d9f368e4122f49'],check=True)
        source = mutant_root/'ops/bien_nhan_v2.py'
        original = source.read_text(encoding='utf-8')
        assert original.count(old) == 1, (name, original.count(old))
        source.write_text(original.replace(old,new),encoding='utf-8')
        spec = importlib.util.spec_from_file_location('review_'+name, mutant_root/'ops/bien_nhan_v2_test.py')
        t = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(t)
        for fn in t.CA:
            state, detail = t._chay_1(fn)
            if state != 'qua':
                failures.append((fn.__name__, state, detail))
                print(json.dumps({'mutation': name, 'failed': failures[-1]}, ensure_ascii=False), flush=True)
        print(json.dumps({'mutation': name, 'cases': len(t.CA), 'passed': len(t.CA)-len(failures),
                          'red': failures, 'old': old, 'new': new}, ensure_ascii=False), flush=True)
