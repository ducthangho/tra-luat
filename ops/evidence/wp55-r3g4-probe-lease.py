#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Đo DANH SÁCH ĐÓNG hình dạng `lease` sai — AC 21.

Mỗi hình dạng phải có MÃ THOÁT CÓ KIỂM SOÁT (khác 0, khác 1) và KHÔNG traceback.
Chiều bắt oan: một state HỢP LỆ không được bị chặn.
"""
import json
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCRIPT = Path(sys.argv[1]).resolve()
PKT = 9003


def _sau(**kw) -> str:
    return (datetime.now(timezone.utc) + timedelta(**kw)).strftime("%Y-%m-%dT%H:%M:%SZ")

# (id, mô tả, giá trị lease, kỳ vọng: "chan" = phải chặn, "qua" = phải cho qua)
CA = [
    ("L0", "lease ĐỦ và hợp lệ (hạn +4h) — PHẢI CHO QUA",
     {"lease_id": "x", "granted_by": "ducthangho", "evidence": "e",
      "expires_utc": _sau(hours=4)}, "qua"),
    ("L0b", "hạn +300 ngày, TRONG cửa sổ — PHẢI CHO QUA",
     {"lease_id": "x", "granted_by": "ducthangho", "evidence": "e",
      "expires_utc": _sau(days=300)}, "qua"),
    ("L0c", "granted_by có hoa/khoảng trắng thừa — PHẢI CHO QUA",
     {"lease_id": "x", "granted_by": "  DUCTHANGHO  ", "evidence": "e",
      "expires_utc": _sau(hours=4)}, "qua"),
    ("L25", "hạn +400 ngày, NGOÀI cửa sổ 366",
     {"lease_id": "x", "granted_by": "ducthangho", "evidence": "e",
      "expires_utc": _sau(days=400)}, "chan"),

    ("L1", "thiếu HẲN lease (null)", None, "chan"),
    ("L2", "dict RỖNG", {}, "chan"),
    ("L3", "CHỈ có expires_utc — bypass P1-B",
     {"expires_utc": "2099-01-01T00:00:00Z"}, "chan"),
    ("L4", "thiếu lease_id",
     {"granted_by": "ducthangho", "evidence": "e",
      "expires_utc": "2099-01-01T00:00:00Z"}, "chan"),
    ("L5", "thiếu granted_by",
     {"lease_id": "x", "evidence": "e", "expires_utc": "2099-01-01T00:00:00Z"}, "chan"),
    ("L6", "thiếu evidence",
     {"lease_id": "x", "granted_by": "ducthangho",
      "expires_utc": "2099-01-01T00:00:00Z"}, "chan"),
    ("L7", "thiếu expires_utc",
     {"lease_id": "x", "granted_by": "ducthangho", "evidence": "e"}, "chan"),

    ("L8", "lease là CHUỖI", "stolen", "chan"),
    ("L9", "lease là SỐ", 12345, "chan"),
    ("L10", "lease là MẢNG", [1, 2], "chan"),
    ("L11", "lease là bool", True, "chan"),

    ("L12", "expires_utc RỖNG",
     {"lease_id": "x", "granted_by": "ducthangho", "evidence": "e",
      "expires_utc": ""}, "chan"),
    ("L13", "expires_utc SAI DẠNG",
     {"lease_id": "x", "granted_by": "ducthangho", "evidence": "e",
      "expires_utc": "not-a-date"}, "chan"),
    ("L14", "expires_utc THIẾU MÚI GIỜ",
     {"lease_id": "x", "granted_by": "ducthangho", "evidence": "e",
      "expires_utc": "2099-01-01T00:00:00"}, "chan"),
    ("L15", "expires_utc là SỐ",
     {"lease_id": "x", "granted_by": "ducthangho", "evidence": "e",
      "expires_utc": 99}, "chan"),
    ("L16", "expires_utc năm 9999",
     {"lease_id": "x", "granted_by": "ducthangho", "evidence": "e",
      "expires_utc": "9999-01-01T00:00:00Z"}, "chan"),
    ("L17", "expires_utc TRƯỚC 1970",
     {"lease_id": "x", "granted_by": "ducthangho", "evidence": "e",
      "expires_utc": "1960-01-01T00:00:00Z"}, "chan"),
    ("L18", "expires_utc là null",
     {"lease_id": "x", "granted_by": "ducthangho", "evidence": "e",
      "expires_utc": None}, "chan"),

    ("L19", "granted_by là PROVIDER — tự cấp lease",
     {"lease_id": "x", "granted_by": "claude", "evidence": "e",
      "expires_utc": "2099-01-01T00:00:00Z"}, "chan"),
    ("L20", "granted_by NGOÀI danh sách cho phép",
     {"lease_id": "x", "granted_by": "codex-dispatcher", "evidence": "e",
      "expires_utc": "2099-01-01T00:00:00Z"}, "chan"),
    ("L21", "granted_by là SỐ",
     {"lease_id": "x", "granted_by": 7, "evidence": "e",
      "expires_utc": "2099-01-01T00:00:00Z"}, "chan"),
    ("L22", "lease_id RỖNG",
     {"lease_id": "", "granted_by": "ducthangho", "evidence": "e",
      "expires_utc": "2099-01-01T00:00:00Z"}, "chan"),
    ("L23", "evidence RỖNG",
     {"lease_id": "x", "granted_by": "ducthangho", "evidence": "   ",
      "expires_utc": "2099-01-01T00:00:00Z"}, "chan"),
    ("L24", "lease_id là MẢNG",
     {"lease_id": ["x"], "granted_by": "ducthangho", "evidence": "e",
      "expires_utc": "2099-01-01T00:00:00Z"}, "chan"),
]


def do(lease, tmp: Path, ten: str):
    sd = tmp / ten
    sd.mkdir(parents=True, exist_ok=True)
    subprocess.run([sys.executable, str(SCRIPT), "--state-dir", str(sd), "init",
                    "--packet", str(PKT), "--mission", "54",
                    "--executor", "claude", "--reviewer", "codex"],
                   capture_output=True)
    p = sd / f"wp{PKT}.json"
    st = json.loads(p.read_text(encoding="utf-8"))
    st["state"] = "leased"
    st["lease"] = lease
    p.write_text(json.dumps(st, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                 encoding="utf-8")
    r = subprocess.run([sys.executable, str(SCRIPT), "--state-dir", str(sd),
                        "begin-attempt", "--packet", str(PKT), "--provider", "claude"],
                       capture_output=True)
    err = r.stderr.decode("utf-8", "replace")
    return r.returncode, "Traceback" in err


def main() -> int:
    lot, tb, oan, ok = [], [], [], 0
    with tempfile.TemporaryDirectory(prefix="probe_lease_") as td:
        tmp = Path(td)
        print(f"{'id':<5} {'rc':<4} {'tb':<4} {'đòi':<6} kết  mô tả")
        print("-" * 92)
        for cid, mota, lease, doi in CA:
            rc, has_tb = do(lease, tmp, cid)
            if doi == "qua":
                if rc == 0 and not has_tb:
                    ket = "ok  "; ok += 1
                else:
                    ket = "OAN "; oan.append(cid)
            else:
                if rc == 0:
                    ket = "LỌT "; lot.append(cid)
                elif has_tb or rc == 1:
                    ket = "TRBK"; tb.append(cid)
                else:
                    ket = "ok  "; ok += 1
            print(f"{cid:<5} {rc:<4} {'Y' if has_tb else '-':<4} {doi:<6} {ket} {mota}")
    print("-" * 92)
    print(f"đạt {ok}/{len(CA)} · LỌT: {lot or 'không'} · TRACEBACK: {tb or 'không'} "
          f"· BẮT OAN: {oan or 'không'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
