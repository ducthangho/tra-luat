#!/usr/bin/env python3
"""Build an exact-head suggestion exclusively in /tmp, then emit a git-applicable diff."""
import difflib
import shutil
from pathlib import Path
src = Path('/tmp/rv812-r4-suite')
dst = Path('/tmp/rv812-r4-hint2')
if not dst.exists():
    shutil.copytree(src, dst, symlinks=True)
p = dst / '.claude/dev/packet_loop.py'
s = (src / '.claude/dev/packet_loop.py').read_text()
def sub(a, b):
    global s
    assert s.count(a) == 1, (a, s.count(a))
    s = s.replace(a, b, 1)
sub('    except yaml.YAMLError:', '    except (yaml.YAMLError, RecursionError):')
sub('def _giao(a: str, b: str) -> bool:', '''def _bieu_dien_duong(p: str, root: Path) -> set[str]:
    """§5: kiểm mọi đường, cả khi không có đối thủ; giữ cả tên khai và đích symlink/parent."""
    q = p.removeprefix("planned:").strip().replace("\\\\", "/")
    if "." in q.split("/"):
        raise ValueError(f"đường dẫn có thành phần '.': {p!r}")
    if any(c in q for c in "*?[]"):
        raise ValueError(f"write set không nhận glob: {p!r}")
    ten = _chuan_duong(p)  # kiểm absolute/.. TRƯỚC phép resolve
    goc = root.resolve()
    dich = (goc / q).resolve(strict=False).relative_to(goc)
    return {ten, _chuan_duong(dich.as_posix())}


def _giao(a: str, b: str) -> bool:''')
sub('or type(l.get("write_set")) is not list \\\n', 'or type(l.get("write_set")) is not list or not l["write_set"] \\\n')
a = '''            giao_nhau = sorted({f"{m['ref']}:{m['path']}" for m in cac if lpm._lease_id_quet(m["lease"].get("lease_id")) != lid
                           and lpm._phan_loai_lease(m["lease"]) == "CÒN_HẠN" and lpm._bia_mo_doi_xung(m["lease"], cac) is not True
                           and any(_giao(x, y) for x in ws for y in giu(m["lease"]))})'''
b = '''            # Đối xứng: write_set ∪ effective_write_set của CẢ HAI bên, không để effective che tập khai.
            own = set().union(*(_bieu_dien_duong(x, root) for x in giu(l)))
            giao_nhau = []
            for m in cac:
                other = m["lease"]
                if lpm._lease_id_quet(other.get("lease_id")) == lid or lpm._phan_loai_lease(other) != "CÒN_HẠN" or lpm._bia_mo_doi_xung(other, cac) is True:
                    continue
                paths = set().union(*(_bieu_dien_duong(x, root) for x in giu(other)))
                if any(_giao(x, y) for x in own for y in paths):
                    giao_nhau.append(f"{m['ref']}:{m['path']}")
            giao_nhau = sorted(set(giao_nhau))'''
sub(a,b)
sub('''                    and nc[v]["provider"] in PROVIDERS and nc[v]["model_family"] in MODEL_FAMILIES for v in ("executor", "reviewer"))''', '''                    and nc[v]["provider"] in PROVIDERS and nc[v]["model_family"] in MODEL_FAMILIES
                    and (nc[v]["execution_surface"] is None or type(nc[v]["execution_surface"]) is str
                         and nc[v]["execution_surface"] in RUNTIME_CAPABILITIES[nc[v]["provider"]])
                    and (nc[v]["transport"] is None or type(nc[v]["transport"]) is str
                         and nc[v]["transport"] in {t for surface, ts in RUNTIME_CAPABILITIES[nc[v]["provider"]].items()
                                                   if nc[v]["execution_surface"] in (None, surface) for t in ts}) for v in ("executor", "reviewer"))''')
a = '''        kieu_sai = [f"{vai}.{k}" for vai, x in (("reviewer", mri), ("executor", mei), ("", d)) for k in (
            ("executor_provider",) if not vai else ("provider", "surface", "transport", "model_family", "ho_model", "canonical_model", "model", "model_evidence"))
                    if k in x and (type(x[k]) is not str or not x[k].strip())]'''
b = '''        # Dùng ĐÚNG bảng nguồn mà canon tra cho cả hai vai, kể cả fallback top-level và bí danh.
        kieu_sai = [f"{vai}.{pre}{k}" for vai in ("reviewer", "executor") for x, pre in bnv._nguon_tra_model(d, vai)[1]
                    for k in ("provider", "surface", "transport", "model_family", "ho_model", "canonical_model", "model", "model_evidence",
                              "bang_chung_model", "model_evidence_ref", "telemetry_path", "nguoi_audit", "audit_actor")
                    if pre + k in x and (type(x[pre + k]) is not str or not x[pre + k].strip())]
        kieu_sai += [f"model_{vai}_identity" for vai in ("reviewer", "executor")
                     if f"model_{vai}_identity" in d and type(d[f"model_{vai}_identity"]) is not dict]
        if type(d.get("schema_version")) is not int:
            kieu_sai.append("schema_version")'''
sub(a,b)
p.write_text(s)

p = dst / '.claude/dev/packet_loop_test.py'
s = (src / '.claude/dev/packet_loop_test.py').read_text()
needle = '_R812_KHAC = lambda **x:'
i = s.index(needle)
new_tests = '''def case_r812_r4_yaml_deep(c: Ctx):
    def mutate(w):
        import yaml
        _g(w, "checkout", "-qb", "ops/wp55-spec", "refs/remotes/origin/ops/wp55-spec")
        p = w / "ops/leases/l.yaml"
        l = yaml.safe_load(p.read_bytes())
        p.write_text(yaml.safe_dump(l) + "extra: " + "[" * 700 + "0" + "]" * 700 + "\\n")
        _g(w, "add", "-A"), _g(w, "commit", "-qm", "nested ordinary metadata"), _g(w, "push", "-q", "origin", "ops/wp55-spec")
        _g(w, "checkout", "-q", "master"), _g(w, "branch", "-q", "-D", "ops/wp55-spec")
    _r812_ca("lease", 2, truoc_lease=mutate)(c)


def case_r812_r4_symlink_scope(c: Ctx):
    def mutate(w, conflict):
        (w / "x").mkdir()
        (w / "x/a.py").write_text("a = 1\\n")
        (w / "alias").symlink_to("x", target_is_directory=True)
        assert (w / "alias/a.py").resolve() == (w / "x/a.py").resolve()
        _g(w, "add", "-A"), _g(w, "commit", "-qm", "alias inside fixture"), _g(w, "push", "-q", "origin", "master")
        _r812_doi_lease(w, {}, (lambda l: {"other.yaml": {**l, "lease_id": "other-lease", "write_set": ["alias/a.py"]}}) if conflict else None)
    for conflict in (False, True):
        (d := c.tmp / str(conflict)).mkdir()
        _r812_ca("lease", 7 if conflict else 0, None if conflict else {"state": "leased"},
                 truoc_lease=lambda w: mutate(w, conflict))(Ctx(c.script, d))


def case_r812_r4_context_executor_surface(c: Ctx):
    rc, sd, e, before = _r812(c, "review")
    _doi(0, rc, e, "baseline H thật")
    st = json.loads(before)
    st["ngu_canh_lease"]["executor"]["execution_surface"] = []
    (sd / "wp55.json").write_text(json.dumps(st))
    raw = (sd / "wp55.json").read_bytes()
    _doi(8, *run(c.script, ["status", "--packet", 55], sd)[::2], "context sai kiểu")
    if raw != (sd / "wp55.json").read_bytes():
        raise AssertionError("I4: state đổi")


'''
s = s[:i] + new_tests + s[i:]
needle = 'MUTANTS.update({\n    "r812_bo_so_ls_remote"'
i = s.index(needle)
extra = '''CASES += [
    ("r812_r4_own_union_conflict", _r812_ca("lease", 7, truoc_lease=lambda w: _r812_doi_lease(
        w, {"effective_write_set": ["y/b.py"]}, lambda l: {"other.yaml": {**l, "lease_id": "other-lease", "write_set": ["x/"], "effective_write_set": ["x/"]}}))),
    ("r812_r4_own_dot", _r812_ca("lease", 7, truoc_lease=lambda w: _r812_doi_lease(w, {"write_set": ["./x/a.py"]}))),
    ("r812_r4_own_parent", _r812_ca("lease", 7, truoc_lease=lambda w: _r812_doi_lease(w, {"effective_write_set": ["x/../y/b.py"]}))),
    ("r812_r4_own_glob", _r812_ca("lease", 7, truoc_lease=lambda w: _r812_doi_lease(w, {"write_set": ["x/*.py"]}))),
    ("r812_r4_empty_declared", _r812_ca("lease", 2, truoc_lease=lambda w: _r812_doi_lease(w, {"write_set": [], "effective_write_set": ["x/a.py"]}))),
    ("r812_r4_top_family", _r812_ca("review", 11, bn={"model_family": []})),
    ("r812_r4_executor_identity", _r812_ca("review", 11, bn={"model_executor_identity": False})),
    ("r812_r4_duplicate_slug", _r812_ca("review", 11, lop=(("a-b", "P3"), ("a-b", "P3")))),
]
'''
s = s[:i] + extra + s[i:]
# A validation of dot components replaces normalization of that invalid spelling.
old = '''    "r812_bo_cham_gach": ('if x not in ("", ".")]', 'if x != ""]', ["r812_nguoi_giu_cham_gach"]),'''
new = '''    "r812_bo_cham_gach": ('    if "." in q.split("/"):', '    if False:', ["r812_r4_own_dot"]),'''
assert old in s
s = s.replace(old,new,1)
old = '''    "r812_bo_dau_cheo_nguoc": ('.strip().replace("\\\\\\\\", "/")', ".strip()", ["r812_nguoi_giu_dau_cheo_nguoc"]),'''
new = '''    "r812_bo_dau_cheo_nguoc": (('.strip().replace("\\\\\\\\", "/")', '.strip().replace("\\\\\\\\", "/")'),
                                    (".strip()", ".strip()"), ["r812_nguoi_giu_dau_cheo_nguoc"]),'''
assert old in s
s = s.replace(old,new,1)
# Existing closure mutants must weaken the new symmetric union, preserving their intended meaning.
old = '''"r812_bo_effective_nguoi_khac": ('for k in ("write_set", "effective_write_set")', 'for k in ("write_set",)', ["r812_nguoi_giu_effective_giao_nhau"]),'''
assert old in s
# Same anchor continues to weaken both sides and remains detectable by the other-side case.
needle = '\n\n\ndef chay_suite('
i = s.index(needle)
extra = '''

MUTANTS.update({
    "r812_r4_bo_chan_yaml_sau": ('except (yaml.YAMLError, RecursionError):', 'except yaml.YAMLError:', ["r812_r4_yaml_deep"]),
    "r812_r4_bo_resolve": ('return {ten, _chuan_duong(dich.as_posix())}', 'return {ten}', ["r812_r4_symlink_scope"]),
    "r812_r4_own_chi_effective": ('for x in giu(l)))', 'for x in ws))', ["r812_r4_own_union_conflict"]),
    "r812_r4_bo_glob": ('    if any(c in q for c in "*?[]"):', '    if False:', ["r812_r4_own_glob"]),
    "r812_r4_bo_parent": (' or ".." in parts', '', ["r812_r4_own_parent"]),
    "r812_r4_cho_declared_rong": (' or not l["write_set"]', '', ["r812_r4_empty_declared"]),
    "r812_r4_bo_schema_bn": ('        if kieu_sai:  # có mặt', '        if False:  # có mặt', ["r812_r4_top_family", "r812_r4_executor_identity"]),
    "r812_r4_bo_schema_surface": (('                    and (nc[v]["execution_surface"] is None or type(nc[v]["execution_surface"]) is str',
                                    '                    and (nc[v]["transport"] is None or type(nc[v]["transport"]) is str'),
                                   ('                    and (True or type(nc[v]["execution_surface"]) is str',
                                    '                    and (True or type(nc[v]["transport"]) is str'), ["r812_r4_context_executor_surface"]),
    "r812_r4_bo_unique_slug": ('and len({x["slug"] for x in lop}) == len(lop)', '', ["r812_r4_duplicate_slug"]),
    "r812_r4_init_tu_cap": ('"state": "awaiting_lease",', '"state": "leased",', ["r812_duong_cu_luon_false"]),
    "r812_r4_bo_dep_vang": ('            if rc != 0 or not b:', '            if False:', ["r812_canon_vang_phu_thuoc"]),
    "r812_r4_bo_neo_path": ('+ neo[0] + neo[1] +', '+', ["r812_verdict_path_khong_ton_tai"]),
    "r812_r4_chan_am_hop_le": ('("slug-ngoai-bang", lop_ok and set(a.finding_id or []) <= {x["slug"] for x in lop})',
                               '("slug-ngoai-bang", lop_ok and not a.finding_id)', ["r812_verdict_am_dung_bang_lop"]),
})
MUTANTS["r812_bo_h_check"][2].append("r812_prompt_path_thu_muc")
'''
s = s[:i]+extra+s[i:]
p.write_text(s)
with Path('HINT.patch').open('w') as f:
    for rel in ('.claude/dev/packet_loop.py','.claude/dev/packet_loop_test.py'):
        a,b = (src/rel).read_text().splitlines(True),(dst/rel).read_text().splitlines(True)
        f.write('diff --git a/'+rel+' b/'+rel+'\n')
        f.writelines(difflib.unified_diff(a,b,fromfile='a/'+rel,tofile='b/'+rel))
print(dst)
