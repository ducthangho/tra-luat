# Regression suggestions for #812 r2. Insert before the CASES r812 registration.
def _r812_doi_lease_review(w, doi, them=None):
    import yaml
    _g(w, "checkout", "-qb", "ops/wp55-spec", "refs/remotes/origin/ops/wp55-spec")
    p = w / "ops/leases/l.yaml"
    lease = yaml.safe_load(p.read_bytes())
    lease.update(doi)
    p.write_text(yaml.safe_dump(lease))
    if them:
        for ten, nd in them(lease).items():
            (w / "ops/leases" / ten).write_text(yaml.safe_dump(nd))
    _g(w, "add", "-A"), _g(w, "commit", "-qm", "single-factor review regression")
    _g(w, "push", "-q", "origin", "ops/wp55-spec"), _g(w, "checkout", "-q", "master")
    _g(w, "branch", "-q", "-D", "ops/wp55-spec")


def case_r812_bia_mo_snapshot_co_git(c: Ctx):
    def doi(w):
        _r812_doi_lease_review(w, {"thay_the_cho": ["old-lease"]}, lambda l: {
            "old.yaml": {**l, "lease_id": "old-lease", "thay_the_cho": [], "da_bi_thay_the": l["lease_id"]}})
    rc, sd, e, _ = _r812(c, "lease", truoc_lease=doi)
    _doi(0, rc, e, "bia mộ hai chiều tại lease OID phải được H check đọc")
    _kiem(sd, "lease thay thế hợp lệ", state="leased", luat_adr0054=True)


def case_r812_nguoi_giu_prefix_giao_nhau(c: Ctx):
    def doi(w):
        _r812_doi_lease_review(w, {}, lambda l: {
            "other.yaml": {**l, "lease_id": "other-lease", "write_set": ["x/"]}})
    _r812_ca("lease", 7, truoc_lease=doi)(c)


def case_r812_nguoi_giu_effective_giao_nhau(c: Ctx):
    def doi(w):
        _r812_doi_lease_review(w, {}, lambda l: {
            "other.yaml": {**l, "lease_id": "other-lease", "write_set": ["y/b.py"],
                           "effective_write_set": ["y/b.py", "x/a.py"]}})
    _r812_ca("lease", 7, truoc_lease=doi)(c)


def case_r812_nguoi_giu_planned_hop_le(c: Ctx):
    _r812_ca("lease", 0, {"state": "leased", "luat_adr0054": True},
             truoc_lease=lambda w: _r812_doi_lease_review(w, {"write_set": ["planned:x/a.py"]}))(c)


def case_r812_family_falsy_khong_tu_mac_dinh(c: Ctx):
    _r812_ca("lease", 2, truoc_lease=lambda w: _r812_doi_lease_review(w, {"model_family": False}))(c)


def case_r812_provider_bi_danh_canon(c: Ctx):
    _r812_ca("lease", 0, {"state": "leased", "luat_adr0054": True}, truoc_lease=lambda w:
             _r812_doi_lease_review(w, {"provider": "anthropic_claude", "executor": "anthropic_claude"}))(c)


def case_r812_executor_provider_lech_lease(c: Ctx):
    _r812_ca("review", 11, bn={"executor_provider": "google_antigravity", "model_executor_identity": {
        "model_family": "claude", "model_evidence": "do_may", "model_evidence_ref": "r"}})(c)


def case_r812_schema_H_khong_duoc_bo(c: Ctx):
    _r812_ca("review", 11, bn={"github_submitter_identity": False})(c)


def case_r812_review_tran_vong_phai_khep(c: Ctx):
    # Start with the same genuine-H positive fixture, restore its pre-review state,
    # and change only the round-cap context, with its historical ledger consistent.
    rc, sd, e, raw = _r812(c, "review")
    _doi(0, rc, e, "baseline H thật")
    st = json.loads(raw)
    st.update(review_rounds_limit=1, review_rounds_used=1, codex_review_calls_used=2,
              reviews=[{"attempt": 1, "provider": "codex", "verdict": "changes_requested",
                        "reviewed_sha": st["reviewing_head_sha"], "finding_ids": [], "finding_descs": []}])
    (sd / "wp55.json").write_text(json.dumps(st))
    rc, _, e = run(c.script, ["record-review", "--packet", 55, "--provider", "codex", "--verdict", "approve",
        "--reviewed-sha", st["reviewing_head_sha"], "--codex-call", "g1", "--bien-nhan", c.tmp / "bn.yaml",
        "--root", c.tmp / "kho/w"], sd)
    _doi(0, rc, e, "cửa khép ADR-0054 ở trần vòng")
    _kiem(sd, "đã ghi kết quả", state="approved_pending", review_rounds_used=2, attempt_open=False)


