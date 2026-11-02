from pathlib import Path
import re
import os
import subprocess
import sys
import tempfile
from record import ROOT, REPO, ENV, record

def fixture(label, files, flags=(), directory=None):
    with tempfile.TemporaryDirectory(prefix='rv1040-r11-fixture-') as raw:
        tmp = Path(raw)
        def git(*args):
            r = subprocess.run(['git','-C',str(tmp),*args],
                               env=dict(ENV, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_SYSTEM=os.devnull),
                               capture_output=True,text=True)
            assert r.returncode == 0, r.stderr
        git('init','-q','-b','master')
        tm = tmp/'ops/reviews'
        tm.mkdir(parents=True)
        for name, body in files.items():
            (tm/name).write_bytes(body.encode())
        if directory:
            (tm/directory).mkdir()
        git('add','-A')
        git('-c','user.name=reviewer','-c','user.email=reviewer@local','commit','-qm','fixture','--allow-empty')
        r = subprocess.run([sys.executable,str(REPO/'ops/bien_nhan_v2.py'),'--root',str(tmp),*flags],
                           env=ENV,capture_output=True,text=True,encoding='utf-8')
        out = f'{label}: files={list(files)!r}, directory={directory!r}, flags={flags!r}\nrc={r.returncode}\nSTDOUT:\n{r.stdout}STDERR:\n{r.stderr}'
        text = r.stdout+r.stderr
        total = re.findall(r'· tổng (\d+)$',r.stdout,re.M)
        if label == 'C1a':
            assert total == ['2'] and 'x.RECEIPT.YAML' in text and r.returncode != 0 and 'TỔNG: ĐẠT' not in text
        elif label == 'C1a-only-upper':
            assert total == ['1'] and 'không có tệp' not in text
        elif label == 'C1b':
            assert r.returncode == 2 and 'x.RECEIPT.YAML' in r.stderr and 'Traceback' not in text
        elif label == 'sinh-no-upper':
            assert r.returncode == 0 and '"x.RECEIPT.YAML"' in r.stdout and '# 1 tệp' in r.stderr
        elif label == 'directory-upper':
            assert r.returncode == 2 and directory in r.stderr and 'Traceback' not in text
        elif label == 'empty-receipts':
            assert r.returncode == 2 and 'không có tệp `*.receipt.yaml` nào (so đuôi không phân biệt hoa thường)' in r.stderr
        return out

cases = [('C1a',{'y.receipt.yaml':'a: 1\n','x.RECEIPT.YAML':'b: 2\n'},(),None),
         ('C1a-only-upper',{'x.RECEIPT.YAML':'b: 2\n'},(),None),
         ('C1b',{'y.receipt.yaml':'a: 1\n','x.RECEIPT.YAML':'b: [\n'},(),None),
         ('sinh-no-upper',{'x.RECEIPT.YAML':'b: 2\n'},('--sinh-no',),None),
         ('directory-upper',{'y.receipt.yaml':'a: 1\n'},(),'X.RECEIPT.YAML'),
         ('empty-receipts',{'ignore.yaml':'a: 1\n'},(),None)]
record('h04','CLI thật trên fixture Git độc lập: C1a/C1b, sinh nợ, thư mục và thông báo rỗng',
       'PYTHONDONTWRITEBYTECODE=1 python3 evidence/fixtures.py',
       '\n\n'.join(fixture(*c) for c in cases))
