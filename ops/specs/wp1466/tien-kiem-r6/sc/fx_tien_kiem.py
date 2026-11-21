"""Răng của khối `tien-kiem` (r6): mỗi kịch bản dựng một kho giả (bare origin + clone), chạy khối, so rc với kỳ vọng.

Dùng: python -B fx_tien_kiem.py <thư mục r6> <tệp ops/lease_publish.py của master> [<tệp khối thay cho sc/tien_kiem.py>].
Không mạng; mọi kho nằm dưới r6/tmp/fx2.
"""
import json, os, pathlib, shutil, subprocess, sys
S, LP = pathlib.Path(sys.argv[1]).resolve(), pathlib.Path(sys.argv[2]).resolve()
TK, FX = (pathlib.Path(sys.argv[3]).resolve() if len(sys.argv) > 3 else S / "sc/tien_kiem.py"), S / "tmp/fx2"
FX.mkdir(parents=True, exist_ok=True)
ENV = dict(os.environ, GIT_AUTHOR_NAME="fx", GIT_AUTHOR_EMAIL="fx@example.invalid", GIT_COMMITTER_NAME="fx",
           GIT_COMMITTER_EMAIL="fx@example.invalid", PYTHONDONTWRITEBYTECODE="1")
def g(cwd, *a):
    r = subprocess.run(["git", *a], cwd=cwd, capture_output=True, text=True, env=ENV)
    assert r.returncode == 0, (a, r.stderr)
    return r.stdout
def lease(lid, ws, ews=None, han="2030-01-01T00:00:00Z", **them):
    d = {"lease_id": lid, "lease_expires_at_utc": han, "write_set": ws, **them}
    if ews is not None:
        d["effective_write_set"] = ews
    return json.dumps(d, ensure_ascii=False)  # JSON là YAML hợp lệ
def dung(ten, master_them=(), nhanh=(), lk=None, sau_fetch_them_nhanh=None, sau=None, them=None):
    """master_them: [(đường dẫn, nội dung)]; nhanh: [(tên nhánh, [(đường dẫn, nội dung)])]; lk: (tên liên kết, đích)."""
    goc = FX / ten
    if goc.exists():
        shutil.rmtree(goc)
    goc.mkdir()
    g(goc, "init", "-q", "--bare", "origin.git")
    g(goc, "init", "-q", "-b", "master", "kho")
    k = goc / "kho"
    (k / "ops").mkdir()
    shutil.copy(LP, k / "ops/lease_publish.py")
    (k / "docs/adr").mkdir(parents=True)
    (k / "docs/PROTOCOL_DA_PHIEN.md").write_text("protocol\n")
    for p, nd in master_them:
        (k / p).parent.mkdir(parents=True, exist_ok=True)
        (k / p).write_text(nd, encoding="utf-8")
    if lk:
        os.symlink(lk[1], k / lk[0])
    g(k, "add", "-A"); g(k, "commit", "-q", "-m", "nen")
    g(k, "remote", "add", "origin", str(goc / "origin.git")); g(k, "push", "-q", "origin", "master")
    for nh, tep in nhanh:
        g(k, "checkout", "-q", "-b", nh, "master")
        for p, nd in tep:
            (k / p).parent.mkdir(parents=True, exist_ok=True)
            (k / p).write_text(nd, encoding="utf-8")
        g(k, "add", "-A"); g(k, "commit", "-q", "-m", nh); g(k, "push", "-q", "origin", nh)
        g(k, "checkout", "-q", "master")
    g(k, "fetch", "-q", "origin", "+refs/heads/*:refs/remotes/origin/*")
    if sau_fetch_them_nhanh:  # máy chủ có nhánh mà bộ đệm chưa fetch
        g(k, "push", "-q", "origin", "master:refs/heads/" + sau_fetch_them_nhanh)
        g(k, "update-ref", "-d", "refs/remotes/origin/" + sau_fetch_them_nhanh)
    for nh, _ in nhanh:
        g(k, "branch", "-q", "-D", nh)
    b = them(k) if them else None  # trạng thái CỤC BỘ chưa công bố, dựng sau khi bộ đệm đã khớp máy chủ; có thể trả B khác
    lenh = [sys.executable, "-B", str(TK), b if isinstance(b, str) else "origin/master"] + (["--sau-dang", sau] if sau else [])
    r = subprocess.run(lenh, cwd=k, capture_output=True, text=True, env=ENV)
    return r.returncode, (r.stdout + r.stderr).strip().splitlines()
L = "ops/leases/"
P1 = ".claude/dev/packet_loop.py"
A, BN = "fxa-r1-g1-claude", "fxb-r1-g1-claude"
GIU_A = [("ops/a", [(L + "a.yaml", lease(A, [P1], da_bi_thay_the=BN))])]  # máy chủ: A còn hạn, một chiều trỏ sang B
def nhap(k, tu="master"):
    """Commit CHƯA CÔNG BỐ chứa bản ghi B xác nhận chiều ngược; trả OID, không để lại nhánh."""
    g(k, "checkout", "-q", "--detach", tu)
    (k / L).mkdir(parents=True, exist_ok=True)
    (k / L / "b.yaml").write_text(lease(BN, ["ops/khac.py"], thay_the_cho=[A]), encoding="utf-8")
    g(k, "add", "-A"); g(k, "commit", "-q", "-m", "nhap rieng")
    oid = g(k, "rev-parse", "HEAD").strip()
    g(k, "checkout", "-q", "master")
    assert oid not in g(k, "ls-remote", "--heads", "origin")
    return oid
def dang_rieng(k, ten="wp1466-r6-g1-claude"):
    """Đăng lease của wp1466 lên origin giả rồi làm mới bộ đệm: kịch bản 3e."""
    g(k, "checkout", "-q", "-b", "ops/w", "master")
    (k / L).mkdir(parents=True, exist_ok=True)
    (k / L / "w.yaml").write_text(lease(ten, [P1]), encoding="utf-8")
    g(k, "add", "-A"); g(k, "commit", "-q", "-m", "w"); g(k, "push", "-q", "origin", "ops/w")
    g(k, "checkout", "-q", "master"); g(k, "branch", "-q", "-D", "ops/w")
    g(k, "fetch", "-q", "origin", "+refs/heads/*:refs/remotes/origin/*")
def nhanh_cuc_bo(k): g(k, "branch", "nhap", nhap(k))
def remote_phu(k): g(k, "update-ref", "refs/remotes/backup/nhap", nhap(k))
def packed(k):
    g(k, "branch", "nhap", nhap(k)); g(k, "pack-refs", "--all")
    assert not (k / ".git/refs/heads/nhap").exists() and "refs/heads/nhap" in (k / ".git/packed-refs").read_text()
def tag(k): g(k, "tag", "nhap", nhap(k))
def origin_thua(k): g(k, "update-ref", "refs/remotes/origin/nhap", nhap(k))
def replace(k):
    tu = g(k, "rev-parse", "refs/remotes/origin/ops/a").strip()
    g(k, "replace", tu, nhap(k, tu))
    assert "b.yaml" in g(k, "ls-tree", "-r", "--name-only", "refs/remotes/origin/ops/a")  # cây làm việc thấy bản nháp
def b_bi_che(k):  # tag cục bộ tên `origin/master` thắng refs/remotes khi giải tên; trỏ commit đã xoá policy
    g(k, "checkout", "-q", "--detach", "master"); g(k, "rm", "-q", "-r", ".github"); g(k, "commit", "-q", "-m", "bo policy")
    oid = g(k, "rev-parse", "HEAD").strip(); g(k, "checkout", "-q", "master"); g(k, "tag", "origin/master", oid)
def lp_cay_lam_viec(k):  # cây làm việc có ops/lease_publish.py đã sửa: mọi bia mộ đều "hai chiều"
    p = k / "ops/lease_publish.py"; s = p.read_text(encoding="utf-8")
    dau = "def _bia_mo_doi_xung(lease: dict, cac_lease: list[dict]) -> bool | None:\n"
    assert s.count(dau) == 1
    p.write_text(s.replace(dau, dau + "    return True\n"), encoding="utf-8")
def master_tien(k):  # máy chủ có master mới hơn; B là master cũ, vẫn là tổ tiên đã công bố
    cu = g(k, "rev-parse", "master").strip()
    (k / "moi.txt").write_text("moi\n"); g(k, "add", "-A"); g(k, "commit", "-q", "-m", "moi"); g(k, "push", "-q", "origin", "master")
    g(k, "fetch", "-q", "origin", "+refs/heads/*:refs/remotes/origin/*")
    return cu
def sau_dang(f): return lambda k: (f(k), dang_rieng(k))
KB = [
    ("sach", dict(nhanh=[("ops/a", [(L + "a.yaml", lease("fxa-r1-g1-claude", ["ops/khac.py"]))])]), 0),
    ("policy_co_mat", dict(master_them=[(".github/coordination/change-impact.v1.json", "{}\n")]), 1),
    ("schema_policy_co_mat", dict(master_them=[(".github/coordination/schemas/change-impact.v1.schema.json", "{}\n")]), 1),
    ("trung_tuyet_doi", dict(nhanh=[("ops/a", [(L + "a.yaml", lease("fxa-r1-g1-claude", [P1]))])]), 1),
    ("tien_to_thu_muc", dict(nhanh=[("ops/a", [(L + "a.yaml", lease("fxa-r1-g1-claude", [".claude/dev/"]))])]), 1),
    ("tien_to_khong_gach", dict(nhanh=[("ops/a", [(L + "a.yaml", lease("fxa-r1-g1-claude", ["docs"]))])]), 1),
    ("khac_kieu_chu", dict(nhanh=[("ops/a", [(L + "a.yaml", lease("fxa-r1-g1-claude", [".Claude/Dev/Packet_Loop.py"]))])]), 1),
    ("chi_effective", dict(nhanh=[("ops/a", [(L + "a.yaml", lease("fxa-r1-g1-claude", ["ops/khac.py"], [P1]))])]), 1),
    ("planned_gach_nguoc", dict(nhanh=[("ops/a", [(L + "a.yaml", lease("fxa-r1-g1-claude", ["planned:docs\\adr\\0068-bat-bien-protocol-va-review-theo-lop.md"]))])]), 1),
    ("duong_dan_thoat", dict(nhanh=[("ops/a", [(L + "a.yaml", lease("fxa-r1-g1-claude", ["../ngoai.py"]))])]), 1),
    ("effective_sai_kieu", dict(nhanh=[("ops/a", [(L + "a.yaml", lease("fxa-r1-g1-claude", ["ops/khac.py"], P1))])]), 1),
    ("lien_ket_thu_muc", dict(lk=("lk", ".claude/dev")), 1),
    ("lien_ket_ngoai_ws", dict(lk=("lk2", "ops")), 0),
    ("ref_chua_moi", dict(sau_fetch_them_nhanh="ops/moi"), 1),
    ("lease_het_han", dict(nhanh=[("ops/a", [(L + "a.yaml", lease("fxa-r1-g1-claude", [P1], han="2020-01-01T00:00:00Z"))])]), 0),
    ("lease_bia_mo_hai_chieu", dict(nhanh=[("ops/a", [(L + "a.yaml", lease("fxa-r1-g1-claude", [P1], da_bi_thay_the="fxb-r1-g1-claude")),
                                                       (L + "b.yaml", lease("fxb-r1-g1-claude", ["ops/khac.py"], thay_the_cho=["fxa-r1-g1-claude"]))])]), 0),
    ("sau_dang_chinh_no", dict(nhanh=[("ops/w", [(L + "w.yaml", lease("wp1466-r5-g1-claude", [P1]))])], sau="wp1466-r5-g1-claude"), 0),
    ("sau_dang_co_nguoi_khac", dict(nhanh=[("ops/w", [(L + "w.yaml", lease("wp1466-r5-g1-claude", [P1])), (L + "a.yaml", lease("fxa-r1-g1-claude", [P1]))])], sau="wp1466-r5-g1-claude"), 1),
    ("sau_dang_chua_co", dict(sau="wp1466-r5-g1-claude"), 1),
    # r6, F11.d: nguồn dữ liệu quyết định phải là ảnh chụp máy chủ đã xác minh (bất biến I-NGUON)
    ("chi_may_chu", dict(nhanh=GIU_A), 1),
    ("rieng_nhanh_cuc_bo", dict(nhanh=GIU_A, them=nhanh_cuc_bo), 1),
    ("rieng_remote_phu", dict(nhanh=GIU_A, them=remote_phu), 1),
    ("rieng_packed_refs", dict(nhanh=GIU_A, them=packed), 1),
    ("rieng_tag", dict(nhanh=GIU_A, them=tag), 1),
    ("rieng_ref_origin_thua", dict(nhanh=GIU_A, them=origin_thua), 1),
    ("rieng_replace", dict(nhanh=GIU_A, them=replace), 1),
    ("rieng_nhanh_cuc_bo_sau_dang", dict(nhanh=GIU_A, them=sau_dang(nhanh_cuc_bo), sau="wp1466-r6-g1-claude"), 1),
    ("rieng_remote_phu_sau_dang", dict(nhanh=GIU_A, them=sau_dang(remote_phu), sau="wp1466-r6-g1-claude"), 1),
    ("b_bi_che_boi_tag", dict(master_them=[(".github/coordination/change-impact.v1.json", "{}\n")], them=b_bi_che), 1),
    ("lp_cay_lam_viec_bi_sua", dict(nhanh=[("ops/a", [(L + "a.yaml", lease(A, [P1]))])], them=lp_cay_lam_viec), 1),
    ("b_la_to_tien_master", dict(them=master_tien), 0),
    ("b_la_sha_rieng", dict(them=lambda k: nhap(k)), 1),
    ("sau_dang_sach_co_nhanh_rieng", dict(them=lambda k: (g(k, "branch", "nhap2", nhap(k)), dang_rieng(k)), sau="wp1466-r6-g1-claude"), 0),
]
dem = [0, 0]
for ten, kw, doi in KB:
    rc, out = dung(ten, **kw)
    ok = rc == doi; dem[ok] += 1
    print(f"{'OK ' if ok else 'SAI'} {ten:26s} rc={rc} (đòi {doi}) {out[-1][:110] if out else ''}" + ("" if rc == 0 else f" | {out[-2][:90] if len(out) > 1 else ''}"), flush=True)
print(f"TONG {len(KB)} kịch bản: đúng {dem[1]} · sai {dem[0]}")
sys.exit(1 if dem[0] else 0)
