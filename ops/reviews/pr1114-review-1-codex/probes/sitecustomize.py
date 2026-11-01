"""Measurement only: record actual spawns and stdin sizes; no argv or payload content."""
import functools
import json
import os
import subprocess
import sys

_log = os.environ.get('REVIEW_AUDIT_LOG')
_run = subprocess.run

def record(kind, args, input_value=None):
    if not _log:
        return
    if isinstance(args, (str, bytes)):
        argv = [os.fsdecode(args)]
    else:
        argv = [os.fsdecode(a) for a in args]
    line = subprocess.list2cmdline(argv)
    stack = []
    frame = sys._getframe(1)
    while frame:
        filename = frame.f_code.co_filename
        if filename != __file__ and '/lib/python' not in filename:
            stack.append([filename, frame.f_lineno, frame.f_code.co_name])
        frame = frame.f_back
    row = {'kind': kind, 'pid': os.getpid(), 'argc': len(argv),
           'executable': argv[0], 'arg_chars': [len(a) for a in argv],
           'quoted_chars': len(line),
           'utf16_units_with_nul': len(line.encode('utf-16-le')) // 2 + 1,
           'input_bytes': len(input_value.encode() if isinstance(input_value, str) else input_value or b''),
           'stack': stack,
           'mutation': {k: os.environ[k] for k in ('CAC_MA', 'CAC_HOOK', 'CAC_GS', 'CAC_SETTINGS') if k in os.environ}}
    data = (json.dumps(row) + '\n').encode()
    fd = os.open(_log, os.O_WRONLY | os.O_CREAT | os.O_APPEND, 0o600)
    try:
        os.write(fd, data)
    finally:
        os.close(fd)

def audit(event, args):
    if event == 'subprocess.Popen':
        record('spawn', args[1])

@functools.wraps(_run)
def run(*args, **kwargs):
    record('run', args[0] if args else kwargs['args'], kwargs.get('input'))
    return _run(*args, **kwargs)

if _log:
    sys.addaudithook(audit)
    subprocess.run = run
