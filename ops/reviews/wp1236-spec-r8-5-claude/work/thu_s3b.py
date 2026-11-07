"""Reviewer Claude vòng 5: biến đổi `run` ở ĐƯỜNG GỌI (trước khi gọi cu_phap_run nguyên văn) — vế (5) của A14-S0 không thấy khi biến đổi
đặt trên dict bước. Đo: mẫu A14-S3b (mỗi 1/300 đầu vào theo thứ tự sinh_r8.main + 3 vế đặt tên) có bắt được không; kèm A14-S3 (2 thân),
A14 (i)/(i′), 7 vế dương. Chạy: python3 -I thu_s3b.py"""
import json, os, sys
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.join(D, "soan"))
import sinh_r8 as S, gram, probes_r8 as PR
th = S.kho()
vao = [(t + lf, sh) for t in th for sh in S.SHELL for lf in ("", "\n")]
mau = [v for i, v in enumerate(vao) if i % 300 == 0] + [PR.AM[k] for k in ("g_bom_dau", "g_python_hoa", "g_hoac_hai_cham")]
khac = [PR.AM["l9_05_hoac_hoac"], (PR.AM["l8_10_set_sau_ong"][0], "bash"),
        ("python .claude/dev/packet_loop_test.py | python ops/tee_test.py", "bash"), ("python .claude/dev/packet_loop_test.py | python ops/tee_test.py", None)] \
    + list(PR.DUONG.values())
BD = {
    "strip": lambda r: r.strip(),
    "rstrip": lambda r: r.rstrip(),
    "rstrip_lf": lambda r: r.rstrip("\n"),
    "bo_bom": lambda r: r.lstrip("﻿"),
    "ha_chu": lambda r: r[:1].lower() + r[1:],
    "suffix_hoac_hai_cham": lambda r: r.removesuffix(" || :"),
    "suffix_va_nen": lambda r: r.removesuffix(" &").removesuffix(" &\n"),
    "prefix_phu_dinh": lambda r: r.removeprefix("! "),
    "crlf": lambda r: r.replace("\r\n", "\n"),
    "tab_cach": lambda r: r.replace("\t", " "),
    "gop_cach": lambda r: " ".join(r.split(" ")) if False else " ".join(r.split()),
    "dong_dau": lambda r: r.split("\n")[0],
    "suffix_exit0": lambda r: r.removesuffix(" || exit 0"),
}
kq = {}
for ten, f in BD.items():
    def b(r, s):
        return gram.cu_phap_run(f(r) if type(r) is str else r, s)
    l_mau = sum(b(r, s) != gram.cu_phap_run(r, s) for r, s in mau)
    l_khac = sum(b(r, s) != gram.cu_phap_run(r, s) for r, s in khac)
    l_toan = sum(b(r, s) != gram.cu_phap_run(r, s) for r, s in vao)
    l_am = sum(b(r, s) != gram.cu_phap_run(r, s) for r, s in list(PR.AM.values()))
    kq[ten] = {"mau_A14_S3b": l_mau, "ca_kiem_khac": l_khac, "toan_kho_A14_S6": l_toan, "AM_neu_qua_kiem": l_am}
    print(f"{ten:22} mau_S3b={l_mau:4}/{len(mau)} kiem_khac={l_khac}/{len(khac)} toan_kho={l_toan:5}/{len(vao)} AM={l_am}/112")
json.dump(kq, open(os.path.join(D, "thu_s3b.json"), "w"), ensure_ascii=False, indent=1)
