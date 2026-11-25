import copy, json, sys, unicodedata
from pathlib import Path
import kv
H = "a" * 40
def mau(**doi):
    d = {"schema_version": 2, "packet_id": "wp1466", "generation": 1, "doi_tuong": "ma", "doi_tuong_sha256": None, "luot": 1,
         "provider": "codex", "role": "reviewer", "model_family": "openai", "execution_surface": "codex_cli", "transport": "machine",
         "session_id": "s1", "model_reviewer_identity": "openai/gpt/s1", "github_submitter_identity": None, "reviewed_sha": H,
         "independent_from_executor_session": True, "review_axes": ["spec", "standards_security"], "tests": [], "findings": [],
         "bang_lop": [], "doi_chieu_luot_truoc": [], "verdict": "approve", "assurance": "cross_approved", "evidence_url": None}
    d.update(doi); return d
F = lambda i, s, h="P3": {"finding_id": i, "class_slug": s, "severity": h, "path": None, "line": None, "evidence": "e",
                          "goi_y_va": {"va_o_dau": "a", "va_the_nao": "b", "ca_khoa": "c", "co_the_de_ra": "d"}}
L = lambda s, h, ids: {"slug": s, "hang": h, "finding_ids": ids, "nguon": "luot 1", "cach_va_chung": "x", "phep_kiem_dong": "y"}
D = lambda i, s, n: {"finding_id": i, "class_slug": s, "nhan": n, "bang_chung": "b"}
def chay(ten, d, doi, **kw):
    try:
        kv._kiem_verdict_lop(d, Path("root"), doi_tuong=kw.pop("doi_tuong", "ma"), reviewed_sha=H, **kw); kq = "DAT"
    except kv.VerdictHong as e:
        kq = "TU_CHOI: " + str(e)[:90]
    print(("OK  " if kq.startswith(doi) else "LECH"), ten, "=>", kq)
chay("sach luot 1", mau(), "DAT")
chay("approve P3 co bang", mau(findings=[F("f1", "lop-a")], bang_lop=[L("lop-a", "P3", ["f1"])]), "DAT")
chay("thieu class_slug", mau(findings=[{k: v for k, v in F("f1", "lop-a").items() if k != "class_slug"}], bang_lop=[L("lop-a", "P3", ["f1"])]), "TU_CHOI")
chay("thieu bang_lop", {k: v for k, v in mau().items() if k != "bang_lop"}, "TU_CHOI")
chay("finding ngoai bang", mau(findings=[F("f1", "lop-a")], bang_lop=[]), "TU_CHOI")
chay("lop trung", mau(findings=[F("f1", "lop-a")], bang_lop=[L("lop-a", "P3", ["f1"]), L("lop-a", "P3", ["f1"])]), "TU_CHOI")
chay("hang lop ha", mau(verdict="changes_requested", findings=[F("f1", "lop-a", "P1")], bang_lop=[L("lop-a", "P3", ["f1"])]), "TU_CHOI")
chay("approve con P1", mau(findings=[F("f1", "lop-a", "P1")], bang_lop=[L("lop-a", "P1", ["f1"])]), "TU_CHOI")
chay("luot 2 thieu hoi_tu", mau(luot=2), "TU_CHOI")
chay("luot 2 du", mau(luot=2, doi_chieu_luot_truoc=[D("f1", "lop-a", "ĐÃ VÁ THẬT")], hoi_tu={"U": ["lop-a"], "F": ["lop-a"]}), "DAT")
chay("luot 2 nhan tu dat", mau(luot=2, doi_chieu_luot_truoc=[D("f1", "lop-a", "DA_VA_THAT")], hoi_tu={"U": ["lop-a"], "F": ["lop-a"]}), "TU_CHOI")
chay("luot 2 nhan NFD", mau(luot=2, doi_chieu_luot_truoc=[D("f1", "lop-a", unicodedata.normalize("NFD", "ĐÃ VÁ THẬT"))], hoi_tu={"U": ["lop-a"], "F": ["lop-a"]}), "TU_CHOI")
chay("luot 2 CHUA VA ma lop bien mat", mau(luot=2, doi_chieu_luot_truoc=[D("f1", "lop-a", "CHƯA VÁ")], hoi_tu={"U": ["lop-a"], "F": []}), "TU_CHOI")
chay("luot 2 F doi tra", mau(luot=2, verdict="changes_requested", findings=[F("f2", "lop-a", "P2")], bang_lop=[L("lop-a", "P2", ["f1", "f2"])],
     doi_chieu_luot_truoc=[D("f1", "lop-a", "VÁ HỜ")], hoi_tu={"U": ["lop-a"], "F": ["lop-a"]}), "TU_CHOI")
chay("luot 2 con mo dung", mau(luot=2, verdict="changes_requested", findings=[F("f2", "lop-a", "P2")], bang_lop=[L("lop-a", "P2", ["f1", "f2"])],
     doi_chieu_luot_truoc=[D("f1", "lop-a", "VÁ HỜ")], hoi_tu={"U": ["lop-a"], "F": []}), "DAT")
chay("luot 1 co doi chieu", mau(doi_chieu_luot_truoc=[D("f1", "lop-a", "CHƯA VÁ")]), "TU_CHOI")
chay("dac_ta thieu sha", mau(doi_tuong="dac_ta"), "TU_CHOI", doi_tuong="dac_ta", sha256="b" * 64)
chay("dac_ta du", mau(doi_tuong="dac_ta", doi_tuong_sha256="b" * 64), "DAT", doi_tuong="dac_ta", sha256="b" * 64)
chay("dac_ta lech sha", mau(doi_tuong="dac_ta", doi_tuong_sha256="c" * 64), "TU_CHOI", doi_tuong="dac_ta", sha256="b" * 64)
chay("sha xuong dong", mau(reviewed_sha=H + "\n"), "TU_CHOI")
chay("slug xuong dong", mau(findings=[F("f1", "lop-a\n")], bang_lop=[L("lop-a\n", "P3", ["f1"])]), "TU_CHOI")
chay("changes_requested 0 finding", mau(verdict="changes_requested"), "TU_CHOI")
# trich khoi
t = "mo dau\n```json review_verdict.v2\n" + json.dumps(mau(), ensure_ascii=False) + "\n```\nKET_LUAN: approve\n"
print("trich 1 khoi:", kv._khoi_verdict(t)["verdict"])
for ten, vb in (("0 khoi", "KET_LUAN: approve\n"), ("2 khoi", t + t), ("khoa trung", t.replace('{"schema_version": 2', '{"luot": 1, "schema_version": 2')), ("NaN", t.replace('"luot": 1', '"luot": NaN'))):
    try: kv._khoi_verdict(vb); print("LECH", ten)
    except kv.VerdictHong as e: print("OK  ", ten, "=>", str(e)[:70])
