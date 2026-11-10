"""Canonical bytes pass; newline/content drift and overwrites must fail."""
import hashlib,tempfile
from pathlib import Path
from freeze_packet import freeze,verify

def rejects(fn):
    try:fn()
    except (ValueError,FileExistsError):return
    raise AssertionError('expected failure was accepted')

with tempfile.TemporaryDirectory() as temp:
    root=Path(temp);text='Hồ sơ\nline two\n';digest=hashlib.sha256(text.encode()).hexdigest()
    freeze(root/'canonical',text,digest)
    assert (root/'canonical').read_bytes()==text.encode()
    (root/'crlf').write_bytes(text.replace('\n','\r\n').encode())
    rejects(lambda:verify(root/'crlf',digest))
    rejects(lambda:freeze(root/'wrong','different',digest))
    rejects(lambda:freeze(root/'canonical',text,digest))
    print('FROZEN_PACKET_CONTROLS 4/4 PASS')
