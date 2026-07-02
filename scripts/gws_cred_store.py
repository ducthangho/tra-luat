#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gws_cred_store.py — mã hoá/giải mã gws credential bằng STDLIB (không phụ thuộc lib ngoài).

Mô hình bảo mật: khoá DẪN XUẤT từ webapp token (PBKDF2-HMAC-SHA256) — token này đã là "master secret"
của skill (trong config). Cred KHÔNG nằm plaintext trong zip; lưu DẠNG MÃ HOÁ trên Drive riêng, giải mã
chỉ trong sandbox ephemeral. Encrypt-then-MAC: keystream = HMAC-SHA256-CTR; toàn vẹn = HMAC-SHA256.
Đây là defense-in-depth (Drive private + webapp-token-gating + mã hoá) — bằng đúng mức tin cậy webapp token.
"""
from __future__ import annotations
import hashlib, hmac, os, struct

MAGIC = b"GWSC1"          # nhận dạng định dạng + version
_KDF_ITERS = 200_000
_SALT_N, _NONCE_N, _TAG_N = 16, 16, 32


def _derive(token: str, salt: bytes) -> tuple[bytes, bytes]:
    dk = hashlib.pbkdf2_hmac("sha256", (token or "").encode("utf-8"), salt, _KDF_ITERS, dklen=64)
    return dk[:32], dk[32:]          # (enc_key, mac_key)


def _keystream(enc_key: bytes, nonce: bytes, n: int) -> bytes:
    out = bytearray()
    ctr = 0
    while len(out) < n:
        out += hmac.new(enc_key, nonce + struct.pack(">Q", ctr), hashlib.sha256).digest()
        ctr += 1
    return bytes(out[:n])


def encrypt(plaintext: bytes, token: str) -> bytes:
    salt, nonce = os.urandom(_SALT_N), os.urandom(_NONCE_N)
    enc_key, mac_key = _derive(token, salt)
    ks = _keystream(enc_key, nonce, len(plaintext))
    ct = bytes(p ^ k for p, k in zip(plaintext, ks))
    body = MAGIC + salt + nonce + ct
    tag = hmac.new(mac_key, body, hashlib.sha256).digest()
    return body + tag


def decrypt(blob: bytes, token: str) -> bytes:
    if blob[:len(MAGIC)] != MAGIC:
        raise ValueError("gws_cred_store: định dạng không hợp lệ (thiếu magic)")
    body, tag = blob[:-_TAG_N], blob[-_TAG_N:]
    off = len(MAGIC)
    salt = blob[off:off + _SALT_N]
    nonce = blob[off + _SALT_N:off + _SALT_N + _NONCE_N]
    ct = blob[off + _SALT_N + _NONCE_N:-_TAG_N]
    enc_key, mac_key = _derive(token, salt)
    if not hmac.compare_digest(tag, hmac.new(mac_key, body, hashlib.sha256).digest()):
        raise ValueError("gws_cred_store: HMAC sai — webapp token giải mã KHÔNG khớp lúc stage, hoặc dữ liệu hỏng")
    ks = _keystream(enc_key, nonce, len(ct))
    return bytes(c ^ k for c, k in zip(ct, ks))


def selftest() -> bool:
    tok = "tl_TEST_0123456789abcdef0123456789ab"
    pt = b'{"refresh_token":"1//abc","client_secret":"GOCSPX-xyz","type":"authorized_user"}'
    blob = encrypt(pt, tok)
    ok = (decrypt(blob, tok) == pt) and (blob[:5] == MAGIC) and (blob != pt)
    try:
        decrypt(blob, tok + "x"); ok = False           # sai token PHẢI raise
    except ValueError:
        pass
    try:
        bad = bytearray(blob); bad[-1] ^= 1
        decrypt(bytes(bad), tok); ok = False            # đổi 1 bit PHẢI raise (HMAC)
    except ValueError:
        pass
    return ok


if __name__ == "__main__":
    print("gws_cred_store selftest:", "OK" if selftest() else "FAIL")
