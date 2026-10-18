from pathlib import Path
import shutil, subprocess
src=Path('/tmp/rv812-r5-suite');dst=Path('/tmp/rv812-r5-hint-final')
if not dst.exists():shutil.copytree(src,dst,symlinks=True)
p=dst/'.claude/dev/packet_loop.py';s=p.read_text()
def change(a,b):
 global s
 assert s.count(a)==1,(a,s.count(a));s=s.replace(a,b,1)
change('    spec.loader.exec_module(m := importlib.util.module_from_spec(spec))\n    return m', '''    try:
        spec.loader.exec_module(m := importlib.util.module_from_spec(spec))
    except Exception as ex:  # loader canon: lỗi nguồn phải có mã thoát được kiểm soát
        _die(RC_STATE, f"KHÔNG ĐO ĐƯỢC: nạp validator canon {ten}: {type(ex).__name__}")
    api = ("PROVIDER_NGUON_HONG", "ASSURANCE_CAN_DOC_LAP", "HO_MODEL_CHO_PHEP", "_thieu", "_neo_git",
           "_nguon_tra_model", "_giai_ho_model_reviewer", "_giai_ho_model_executor", "_chuoi", "_chuan_hoa_provider")
    if ten == "bien_nhan_v2" and any(not hasattr(m, k) for k in api):
        _die(RC_STATE, f"KHÔNG ĐO ĐƯỢC: validator canon {ten} thiếu giao diện")
    return m''')
change('except (OSError, subprocess.SubprocessError):\n        return -1, b""','except (OSError, subprocess.SubprocessError, ValueError):\n        return -1, b""')
change('or int(mr[2]) != st["packet"]','or mr[2].lstrip("0") != str(st["packet"])')
change('        if l["assurance_target"] not in _nap(td, "bien_nhan_v2").ASSURANCE_CAN_DOC_LAP:', '''        bnv_lease = _nap(td, "bien_nhan_v2")
        if bnv_lease.PROVIDER_NGUON_HONG is not None:
            _die(RC_STATE, f"KHÔNG ĐO ĐƯỢC: nguồn canon hỏng: {bnv_lease.PROVIDER_NGUON_HONG}")
        if l["assurance_target"] not in bnv_lease.ASSURANCE_CAN_DOC_LAP:''')
change('        if type(d.get("schema_version")) is not int:', '''        # `_thieu` còn đọc các tham chiếu CÓ tiền tố ngay bên trong khối executor.
        kieu_sai += [f"executor.{k}" for k in ("executor_model_evidence_ref", "executor_telemetry_path", "executor_nguoi_audit", "executor_audit_actor")
                     if k in mei and (type(mei[k]) is not str or not mei[k].strip())]
        kieu_sai += [f"reviewer.{k}" for k in ("che_do", "session_run_id", "KHONG_do_duoc")
                     if k in mri and (type(mri[k]) is not str or not mri[k].strip())]
        if "phien_doc_lap" in mri and type(mri["phien_doc_lap"]) is not bool:
            kieu_sai.append("reviewer.phien_doc_lap")
        if type(d.get("schema_version")) is not int:''')
change('        ho = lambda vai: HO_CANON[nc[vai]["model_family"]]', '''        # Chỉ chuẩn hoá bản chiếu dùng để SO; schema/Git/hash vẫn đo biên nhận nguyên byte.
        import ast
        cay = ast.parse((td / ".claude/dev/launcher.py").read_text(encoding="utf-8"))
        bd_bm = dict(next(ast.literal_eval(n.value) for n in cay.body if isinstance(n, ast.Assign)
                          and len(n.targets) == 1 and getattr(n.targets[0], "id", "") == "_BE_MAT_BI_DANH"))
        p_chuan = lambda x: _ten_provider(bnv._chuan_hoa_provider(bnv._chuoi(x) or ""))  # noqa: E731
        bm_chuan = lambda x: bd_bm.get(bnv._chuoi(x), bnv._chuoi(x))  # noqa: E731
        ho = lambda vai: HO_CANON[nc[vai]["model_family"]]''')
change('_ten_provider(mri.get("provider")) == nc["reviewer"]["provider"]','p_chuan(mri.get("provider")) == nc["reviewer"]["provider"]')
change('_ten_provider(mei.get("provider", d.get("executor_provider"))) == nc["executor"]["provider"]','p_chuan(mei.get("provider", d.get("executor_provider"))) == nc["executor"]["provider"]')
change('mri.get("surface") == nc["reviewer"]["execution_surface"]','bm_chuan(mri.get("surface")) == nc["reviewer"]["execution_surface"]')
change('mri.get("transport") == nc["reviewer"]["transport"]','bnv._chuoi(mri.get("transport")) == nc["reviewer"]["transport"]')
change('all(mei.get(k, nc["executor"][f]) == nc["executor"][f] for k, f in','all((bm_chuan(mei[k]) if k == "surface" else bnv._chuoi(mei[k])) == nc["executor"][f] for k, f in')
change('(("surface", "execution_surface"), ("transport", "transport"))))','(("surface", "execution_surface"), ("transport", "transport")) if k in mei))')
p.write_text(s)
# Test hints use real H fixture and compare byte state on every rejection.
p=dst/'.claude/dev/packet_loop_test.py';s=p.read_text()
s=s.replace('("r812_canon_thieu_nguon", _r812_ca("review", 11, bien="thieu_nguon")),','("r812_canon_thieu_nguon", _r812_r5_canon_hong_sau_lease),')
addition='''
def _r812_r5_canon_hong_sau_lease(c: Ctx):
    rc, sd, e, before = _r812(c, "review")
    _doi(0, rc, e, "baseline H thật")
    (sd / "wp55.json").write_bytes(before)
    w = c.tmp / "kho/w"
    (w / "AGENTS.md").write_text("# nguồn hỏng\\n")
    _g(w, "add", "AGENTS.md"), _g(w, "commit", "-qm", "source invalid after valid lease")
    _g(w, "push", "-q", "origin", "master"), _g(w, "fetch", "-q", "origin")
    rc, _, e = run(c.script, ["record-review", "--packet", 55, "--provider", "codex", "--verdict", "approve",
        "--reviewed-sha", json.loads(before)["reviewing_head_sha"], "--codex-call", "g1", "--bien-nhan", c.tmp / "bn.yaml", "--root", w], sd)
    _doi(11, rc, e, "review không được dùng nguồn canon hỏng")
    if (sd / "wp55.json").read_bytes() != before:
        raise AssertionError("I4: state đổi")

'''
s=s.replace('_R812_KHAC = lambda **x:',addition+'_R812_KHAC = lambda **x:',1)
newcases='''
def _r812_r5_source_module(w, content):
    (w / "ops/bien_nhan_v2.py").write_text(content)
    _g(w, "add", "ops/bien_nhan_v2.py"), _g(w, "commit", "-qm", "invalid canon module")
    _g(w, "push", "-q", "origin", "master")

# #812 lượt 5: nguồn suy giảm ở lease, mọi nguồn tham chiếu, chuẩn hoá tuple và lỗi argv.
CASES += [
    ("r812_r5_lease_canon_hong", _r812_ca("lease", 8, bien="thieu_nguon")),
    ("r812_r5_source_api_missing", _r812_ca("lease", 8, truoc_lease=lambda w: _r812_r5_source_module(w, "# missing API\\n"))),
    ("r812_r5_source_syntax", _r812_ca("lease", 8, truoc_lease=lambda w: _r812_r5_source_module(w, "ordinary invalid syntax\\n"))),
    ("r812_r5_instruction_long", _r812_ca("lease", 2, truoc_lease=lambda w: _r812_doi_lease(w, {
        "granted_on_instruction": "https://github.com/o/r/issues/" + "5" * 4400 + "#issuecomment-1"}))),
    ("r812_r5_spec_path_zero", _r812_ca("lease", 2, truoc_lease=lambda w: _r812_doi_lease(w, {"spec_path": "ops/specs/wp55\\x00.md"}))),
]
for k in ("executor_model_evidence_ref", "executor_telemetry_path", "executor_nguoi_audit", "executor_audit_actor"):
    CASES.append(("r812_r5_nested_" + k, _r812_ca("review", 11, bn={"model_executor_identity": {
        "model_family": "claude", "model_evidence": "do_may", "model_evidence_ref": "r", k: []}})))
for k, val in (("che_do", []), ("KHONG_do_duoc", []), ("phien_doc_lap", "false")):
    CASES.append(("r812_r5_reviewer_" + k, _r812_ca("review", 11, bn={"model_reviewer_identity": {
        "provider": "openai_codex", "surface": "codex_cli", "transport": "machine", "session_run_id": "s1", k: val}})))
CASES.append(("r812_r5_session_list", _r812_ca("review", 11, bn={"model_reviewer_identity": {
    "provider": "openai_codex", "surface": "codex_cli", "transport": "machine", "session_run_id": [], "phien_doc_lap": True, "KHONG_do_duoc": "ordinary explanation"}})))
for k, val in (("provider", " openai_codex "), ("surface", " codex_cli "), ("transport", " machine ")):
    CASES.append(("r812_r5_padded_" + k, _r812_ca("review", 0, {"state": "approved_pending"}, bn={"model_reviewer_identity": {
        "provider": "openai_codex", "surface": "codex_cli", "transport": "machine", "session_run_id": "s1", k: val}})))
CASES += [
    ("r812_r5_alias_surface", _r812_ca("review", 0, {"state": "approved_pending"}, bn={"model_executor_identity": {"surface": "claude_code_cli", "transport": "machine/local"}})),
    ("r812_r5_prefixed_reference_valid", _r812_ca("review", 0, {"state": "approved_pending"}, bn={"model_executor_identity": {
        "model_family": "claude", "model_evidence": "do_may", "executor_model_evidence_ref": "r"}})),
]
MUTANTS.update({
    "r812_r5_no_loader_guard": ('    except Exception as ex:  # loader canon:', '    except OSError as ex:  # loader canon:', ["r812_r5_source_syntax"]),
    "r812_r5_no_api_guard": ('if ten == "bien_nhan_v2" and any(not hasattr(m, k) for k in api):', 'if False:', ["r812_r5_source_api_missing"]),
    "r812_r5_lease_degraded": ('        if bnv_lease.PROVIDER_NGUON_HONG is not None:', '        if False:', ["r812_r5_lease_canon_hong"]),
    "r812_r5_unbounded_int": ('mr[2].lstrip("0") != str(st["packet"])', 'int(mr[2]) != st["packet"]', ["r812_r5_instruction_long"]),
    "r812_r5_argv_valueerror": ('except (OSError, subprocess.SubprocessError, ValueError):', 'except (OSError, subprocess.SubprocessError):', ["r812_r5_spec_path_zero"]),
    "r812_r5_ignore_bad_attestations": ('        if kieu_sai:  # có mặt', '        if False:  # có mặt',
        ["r812_r5_nested_executor_model_evidence_ref", "r812_r5_reviewer_che_do", "r812_r5_reviewer_phien_doc_lap", "r812_r5_reviewer_KHONG_do_duoc", "r812_r5_session_list"]),
    "r812_r5_raw_provider": ('bnv._chuan_hoa_provider(bnv._chuoi(x) or "")', 'bnv._chuan_hoa_provider(x or "")', ["r812_r5_padded_provider"]),
    "r812_r5_raw_surface": ('bm_chuan(mri.get("surface")) ==', 'mri.get("surface") ==', ["r812_r5_padded_surface"]),
    "r812_r5_raw_transport": ('bnv._chuoi(mri.get("transport")) ==', 'mri.get("transport") ==', ["r812_r5_padded_transport"]),
})

'''
s=s.replace('def chay_suite(script: Path, tmp: Path, chi_chay=None):',newcases+'def chay_suite(script: Path, tmp: Path, chi_chay=None):',1)
# Existing mutations retain their original intent on the normalized projections.
s=s.replace("'((\"surface\", \"execution_surface\"), (\"transport\", \"transport\"))', '((\"surface\", \"execution_surface\"),)'", "'((\"surface\", \"execution_surface\"), (\"transport\", \"transport\"))', '((\"surface\", \"execution_surface\"),)'")
s=s.replace("'(\"provider-executor\", _ten_provider('","'(\"provider-executor\", p_chuan('").replace("'(\"provider-executor\", True or _ten_provider('","'(\"provider-executor\", True or p_chuan('")
s=s.replace('_nap(td, "bien_nhan_v2").ASSURANCE_CAN_DOC_LAP', 'bnv_lease.ASSURANCE_CAN_DOC_LAP')
p.write_text(s)
for rel in ('.claude/dev/packet_loop.py','.claude/dev/packet_loop_test.py'):
 compile((dst/rel).read_text(),rel,'exec')
patch=subprocess.check_output(['git','-C',str(dst),'diff','--', '.claude/dev/packet_loop.py','.claude/dev/packet_loop_test.py'])
Path('HINT.patch').write_bytes(patch)
print('hint',len(patch),'bytes')
