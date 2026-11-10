"""Preserve canonical UTF-8 packet bytes on Windows; never normalize silently."""
import hashlib
from pathlib import Path

def verify(path, expected_sha256):
    actual = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    if actual != expected_sha256:
        raise ValueError('FROZEN_PACKET_BYTE_HASH_MISMATCH')
    return actual

def freeze(path, text, expected_sha256):
    data = text.encode('utf-8')
    if hashlib.sha256(data).hexdigest() != expected_sha256:
        raise ValueError('CANONICAL_PACKET_INPUT_HASH_MISMATCH')
    # Binary mode prevents Windows newline translation. Existing frozen artifacts
    # are immutable: create a fresh path instead of replacing the reviewed bytes.
    with Path(path).open('xb') as stream:
        stream.write(data)
    return verify(path, expected_sha256)
