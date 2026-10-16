"""wp685 r28 g5 attempt 2 — phản chứng chạy được cho comparator D (VERDICT lượt 1, D65-control-catalog-not-validated).
Dùng: python3.1x -B phan_chung_d.py <bang_chung_aw_d.py> <.claude/dev ứng viên> <thư mục tạm> <đặc tả r28>
Chạy bang_chung_aw_d.py chế độ `d` một lần SẠCH (phải rc=0, 65/65) rồi một lần cho MỖI phản chứng (phải rc!=0 VÀ in
đúng dấu lý do). rc=0 chỉ khi bản sạch xanh và MỌI phản chứng đỏ đúng lý do."""
import os
import subprocess
import sys
from pathlib import Path

SCRIPT, DEV, TAM, SPEC = sys.argv[1:5]
TAM = Path(TAM)
TAM.mkdir(parents=True, exist_ok=True)
CA = [  # (tên, mô tả, các dấu phải có trong đầu ra)
    ("", "ban sach", ["D danh muc: 65 khoa", "D ban dung: XANH", "TONG D: control 65/65 do dung; dao 6/6; hong=0"]),
    ("lap", "thay control cuoi bang control dau (65 dong / 64 khoa) — phan chung cua reviewer",
     ["D DANH MUC DO", "so dong=65 so khoa=64 lap=['nhan:B1'] thieu=['tieu:B2-nhanh-cu/vang-decode']"]),
    ("thua", "them mot control ngoai danh muc (66 dong)", ["D DANH MUC DO", "thua=['tieu:B2-parse/p9']"]),
    ("thua_trung", "them mot dong trung khoa (66 dong / 65 khoa)", ["D DANH MUC DO", "so dong=66 so khoa=65 lap=['nhan:B1']"]),
    ("thieu", "bo control cuoi (64 dong)", ["D DANH MUC DO", "so dong=64", "thieu=['tieu:B2-nhanh-cu/vang-decode']"]),
    ("khoa_cu", "khoa kieu attempt 1 `noi_mac_dinh:*` thay `nhan:*`", ["D DANH MUC DO", "thua=['noi_mac_dinh:B1'"]),
    ("quan_sat_tieu_la", "quan sat them don vi `B2-parse p9` ngoai dac ta", ["D ban dung: DO", "thua=[('B2-parse', None)]"]),
    ("quan_sat_nhan_la", "quan sat them nhan la `B9-la`", ["D ban dung: DO", "thua=[('?', 'B9-la ngoai spec')]"]),
    ("quan_sat_tieu_thieu", "quan sat `B2-doc-hong` khong tieu nhan", ["D ban dung: DO", "thua=[('B2-doc-hong', None)]"]),
]
hong = 0
for ten, mo_ta, dau in CA:
    env = dict(os.environ, D_PHAN_CHUNG=ten, PYTHONDONTWRITEBYTECODE="1")
    nhan = ten or "sach"
    p = subprocess.run([sys.executable, "-B", SCRIPT, DEV, str(TAM / nhan), "d", SPEC, str(TAM / f"bang_D_{nhan}.json")],
                       env=env, capture_output=True, text=True, timeout=900, stdin=subprocess.DEVNULL)
    ra = p.stdout + p.stderr
    (TAM / f"phan_chung_{nhan}.out").write_text(ra, encoding="utf-8")
    thieu_dau = [x for x in dau if x not in ra]
    can_rc0 = ten == ""
    dat = (p.returncode == 0) == can_rc0 and not thieu_dau
    hong += not dat
    print(f"{'DAT' if dat else 'HONG'} [{nhan}] {mo_ta}: rc={p.returncode} (ky vong {'0' if can_rc0 else '!=0'}) "
          f"dau thieu={thieu_dau}", flush=True)
    for d in ra.splitlines():
        if d.startswith(("D DANH MUC DO", "D ban dung", "TONG D", "KET LUAN")):
            print(f"    | {d[:300]}", flush=True)
print(f"PHAN CHUNG D: {len(CA) - hong}/{len(CA)} dat; rc={'0' if hong == 0 else '1'}")
sys.exit(1 if hong else 0)
