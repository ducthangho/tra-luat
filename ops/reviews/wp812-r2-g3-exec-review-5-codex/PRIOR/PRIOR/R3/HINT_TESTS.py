# TEST hint only; insert before _R812_XOA_DAC_TA in packet_loop_test.py.
# chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit


def _r812_r3_pair(c, den, expect, **changes):
    for label, rc, kw in (("positive", 0, {}), ("one-factor", expect, changes)):
        d = c.tmp / label
        d.mkdir()
        cc = Ctx(c.script, d)
        actual, sd, err, before = _r812(cc, den, **kw)
        _doi(rc, actual, err, f"r812 r3 {label}")
        if rc and (sd / "wp55.json").read_bytes() != before:
            raise AssertionError("I4: rejected input changed state bytes")


def case_r812_r3_holder_casefold(c):
    _r812_r3_pair(c, "lease", 7, truoc_lease=lambda w: _r812_doi_lease(
        w, {}, lambda l: {"other.yaml": {**l, "lease_id": "other", "write_set": ["X/"]}}))


def case_r812_r3_holder_separator(c):
    _r812_r3_pair(c, "lease", 7, truoc_lease=lambda w: _r812_doi_lease(
        w, {}, lambda l: {"other.yaml": {**l, "lease_id": "other", "write_set": ["x\\a.py"]}}))


def case_r812_r3_holder_unicode(c):
    _r812_r3_pair(c, "lease", 7, truoc_lease=lambda w: _r812_doi_lease(
        w, {"write_set": ["café/a.py"]}, lambda l: {"other.yaml": {**l, "lease_id": "other", "write_set": ["cafe\u0301/"]}}))


def case_r812_r3_effective_expansion(c):
    _r812_r3_pair(c, "lease", 0, truoc_lease=lambda w: _r812_doi_lease(w, {"effective_write_set": ["x/a.py", "y/b.py"]}))


def case_r812_r3_empty_branch(c):
    _r812_r3_pair(c, "lease", 2, truoc_lease=lambda w: _r812_doi_lease(w, {"branch": ""}))


def case_r812_r3_receipt_provider_type(c):
    _r812_r3_pair(c, "review", 11, bn={"model_reviewer_identity": {
        "provider": [], "surface": "codex_cli", "transport": "machine", "session_run_id": "s1"}})


def case_r812_r3_receipt_family_type(c):
    _r812_r3_pair(c, "review", 11, bn={"model_reviewer_identity": {
        "provider": "openai_codex", "surface": "codex_cli", "transport": "machine", "session_run_id": "s1", "model_family": []}})


def case_r812_r3_receipt_sha(c):
    # V is a REAL commit, so H schema/anchor stay valid; only the candidate SHA differs.
    _r812_r3_pair(c, "review", 11, bn={"reviewed_sha": "{V}"})


def case_r812_r3_receipt_lease_id(c):
    _r812_r3_pair(c, "review", 11, bn={"lease_id": "different-lease"})


def case_r812_r3_executor_transport(c):
    _r812_r3_pair(c, "review", 11, bn={"model_executor_identity": {"transport": "human"}})


def case_r812_r3_dependency_absent(c):
    def remove_dependency(w):
        _g(w, "rm", "AGENTS.md"), _g(w, "commit", "-qm", "missing canonical dependency"), _g(w, "push", "-q", "origin", "master")
    _r812_r3_pair(c, "lease", 8, truoc_lease=remove_dependency)


def case_r812_r3_ag_families_cli(c):
    import yaml
    for family, receipt_family in (("gemini", "gemini"), ("openai", "gpt")):
        d = c.tmp / family
        d.mkdir()
        cc = Ctx(c.script, d)
        w = _kho812(cc)
        _r812_doi_lease(w, {"provider": "google_antigravity", "executor": "google_antigravity", "model_family": family,
            "execution_surface": "antigravity", "reviewer": "claude", "reviewer_model_family": "claude",
            "reviewer_execution_surface": "claude_code", "reviewer_transport": "machine/local"})
        sd = cc.sd()
        _doi(0, *cc.init(sd, executor="google_antigravity", reviewer="claude", lease=False,
            extra=("--executor-model-family", family, "--executor-execution-surface", "antigravity", "--executor-transport", "machine/local"))[::2], "init AG")
        (d / "cm.json").write_text(json.dumps([{"user": {"login": "github-actions[bot]"}, "body": "lease_id: wp55-r1-g1-claude",
            "issue_url": "https://api.github.com/repos/o/r/issues/55"}]))
        h = _g(w, "rev-parse", "refs/remotes/origin/agent/wp55-g1-claude")
        for args in (
            ["record-lease", "--packet", 55, "--lease-ref", "origin/ops/wp55-spec", "--lease-path", "ops/leases/l.yaml", "--lease-comments", d / "cm.json", "--root", w],
            ["begin-attempt", "--packet", 55, "--provider", "google_antigravity", "--model-family", family, "--execution-surface", "antigravity", "--transport", "machine/local"],
            ["record-post", "--packet", 55, "--for", "reviewing", "--comment-id", "9000055002"],
            ["transition", "--packet", 55, "--to", "reviewing", "--comment-id", "9000055002", "--head-sha", h],
        ):
            _doi(0, *run(c.script, args, sd)[::2], f"AG setup {args[0]}")
        sh = _st(sd)["ngu_canh_lease"]["spec_hash"]
        (d / "bn.yaml").write_text(yaml.safe_dump(_bn812(w, h, sh, bn={"executor_provider": "google_antigravity",
            "model_executor_identity": {"model_family": receipt_family, "model_evidence": "do_may", "model_evidence_ref": "r"},
            "model_reviewer_identity": {"provider": "anthropic_claude", "surface": "claude_code", "transport": "machine/local", "session_run_id": "s"}})))
        _doi(0, *run(c.script, ["record-review", "--packet", 55, "--provider", "claude", "--verdict", "approve", "--reviewed-sha", h,
            "--bien-nhan", d / "bn.yaml", "--root", w], sd)[::2], f"AG/{family} valid H")
        _kiem(sd, "AG clean approval", state="approved_pending")
