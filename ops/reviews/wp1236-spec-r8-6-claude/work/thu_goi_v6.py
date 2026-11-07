"""Vòng 6 (reviewer Claude): vế (5) gián điệp đối số của A14-S0 bản sửa 5 THAY vế "hình dạng lời gọi" của bản sửa 4. Phép đo: với mỗi
biến đổi T đặt Ở CHỖ GỌI (`cu_phap_run(T(buoc.get("run")), buoc.get("shell"))`), đếm
  (1) số thân bước luật của ci.yml@fe84620 (F-ok-goc) và fe84620+VL-F (F-ok) mà T làm đổi  -> gián điệp trên F-ok/F-ok-goc lệch?
  (2) số thân trong 10 lượt gián điệp đặc biệt mà T làm đổi                                  -> gián điệp trên năm thân lệch?
  (3) số đầu vào A14-S3b (112 âm + 7 dương + 206 mẫu i % 299) mà cu_phap_run(T(run)) != cu_phap_run(run)  -> A14-S3b lệch?
  (4) số đầu vào kho A14-S6 đầy đủ (61 530) đổi lý do — chỉ để biết đường ấy có tồn tại không (A14-S6 KHÔNG đi qua `kiem`).
Không có T nào đổi (1)–(3) ⇒ T qua A14-S0 (v5) + A14-S3/S3b, tức `kiem` nhận khác tham chiếu mà không ca nào đỏ.
Chạy từ gốc kho: python3 -I ../work/v6/thu_goi_v6.py"""
import json, os, re, subprocess, sys, collections
import yaml
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import gram, probes_r8, sinh_r8

src = subprocess.check_output(["git", "show", "508d678:ops/gate_output_doi_chieu.py"], text=True)
src = src.replace('Path(__file__).with_name("ci_provenance.py")', 'Path("ops/ci_provenance.py")')
ns = {"__name__": "g1"}; exec(compile(src, "g1", "exec"), ns)
TEN = {t for m in ns["LUAT_v1"]["MUC"] for b in m["buoc"] for t in b["ten"]}
wf = yaml.safe_load(subprocess.check_output(["git", "show", "fe84620:.github/workflows/ci.yml"]))
GOC = [(s.get("run"), s.get("shell")) for j in wf["jobs"].values() for s in j.get("steps", []) if s.get("name") in TEN]
VLF = ["bash .github/checks/tl_selftest_bang_chung.sh\n", "bash .github/checks/release_bundle_x2.sh\n", "python ops/cong_cu_test.py\n",
       "bash ops/chay_lease_publish_test.sh\n", "pwsh -NoProfile -File scripts/don-nhanh_test.ps1\n", "bash ops/ci/gate_cgroup.sh\n"]
FOK = [(r, s) for r, s in GOC if gram.cu_phap_run(r, s) is None] + [(v, None) for v in VLF]
GD = [(v, sh) for v in ["python ops/x.py\n", "python ops/K.py\n", "python ops/é.py\n", "python ops/x.py\n\n",
                         "﻿python ops/x.py\n"] for sh in (None, "bash")]
S3B = [(r, s) for r, s in list(probes_r8.AM.values()) + list(probes_r8.DUONG.values())]
kho, i, mau = sinh_r8.kho(), 0, []
for than in kho:
    for sh in sinh_r8.SHELL:
        for run in (than, than + "\n"):
            if i % 299 == 0:
                mau.append((run, sh))
            i += 1
S3B_MAU = mau
TOAN = [(run, sh) for than in kho for sh in sinh_r8.SHELL for run in (than, than + "\n")]


def an(f):
    return lambda r: f(r) if type(r) is str else r


T = {
    "removesuffix_hoac_hai_cham": an(lambda r: r.removesuffix(" || :")),
    "removesuffix_hoac_exit0": an(lambda r: r.removesuffix(" || exit 0")),
    "removesuffix_hoac_true": an(lambda r: r.removesuffix(" || true")),
    "removesuffix_va": an(lambda r: r.removesuffix(" &")),
    "removeprefix_phu_dinh": an(lambda r: r.removeprefix("! ")),
    "crlf_lf": an(lambda r: r.replace("\r\n", "\n")),
    "bo_cr": an(lambda r: r.replace("\r", "")),
    "tab_cach": an(lambda r: r.replace("\t", " ")),
    "gop_cach": an(lambda r: re.sub(" +", " ", r)),
    "strip": an(lambda r: r.strip()),
    "rstrip_lf": an(lambda r: r.rstrip("\n")),
    "nfc": an(lambda r: __import__("unicodedata").normalize("NFC", r)),
}


def dem_doi(T_, tap):
    return sum(T_(r) != r for r, _ in tap)


def dem_lech(T_, tap):
    return sum(gram.cu_phap_run(T_(r), s) != gram.cu_phap_run(r, s) for r, s in tap)


if __name__ == "__main__":
    print(f"F-ok-goc: {len(GOC)} buoc luat; F-ok: {len(FOK)}; gian diep dac biet: {len(GD)}; A14-S3b: {len(S3B)} + {len(S3B_MAU)} = "
          f"{len(S3B) + len(S3B_MAU)}; shell mau: {dict(collections.Counter(s for _, s in S3B_MAU))}; "
          f"mau duoc nhan: {sum(gram.cu_phap_run(r, s) is None for r, s in S3B_MAU)}; kho day du: {len(TOAN)}")
    kq = {}
    for ten, f in T.items():
        d = {"doi_F-ok-goc": dem_doi(f, GOC), "doi_F-ok": dem_doi(f, FOK), "doi_gian_diep": dem_doi(f, GD),
             "lech_S3b_bang": dem_lech(f, S3B), "lech_S3b_mau": dem_lech(f, S3B_MAU), "lech_kho_S6": dem_lech(f, TOAN)}
        d["qua_moi_ca"] = d["doi_F-ok-goc"] == d["doi_F-ok"] == d["doi_gian_diep"] == d["lech_S3b_bang"] == d["lech_S3b_mau"] == 0
        kq[ten] = d
        print(f"{ten:28} {d}")
    json.dump(kq, open(os.path.join(D, "thu_goi_v6.json"), "w"), ensure_ascii=False, indent=1)
