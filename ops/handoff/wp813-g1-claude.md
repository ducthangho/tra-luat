# Handoff — wp813-r2-g1-claude (`MAY-ADR-0054-b`), packet #813 r2 g1

Trạng thái: **DỪNG — same_failure_limit = 2 chạm** sau Codex lượt 2/8. Hỏi chủ kho trên #813. Nhánh code `agent/wp813-g1-claude`
**chưa đẩy** (chỉ đẩy một lần khi approve); bản vá đầy đủ nằm cuối tệp này (`git am` được), sha256 `fe9b4cc5bcbe75f22a13bec88b2d05f4ae7a89f574f3949b4f20864c9f175a75`.

- Base `f577ab5b467510f3fa7ed27107dc2eab539d3bef` (= `origin/master` lúc làm). Head ứng viên `79bbbdc16bd873f319ab70885039413735ee2fb3`.
- Diff: `.claude/dev/packet_loop.py` 153+/11−, `.claude/dev/packet_loop_test.py` 203+/3− ⇒ 2 đường dẫn, 356 dòng thêm (≤ 450).
- `doctrine-scan` rc=0, `adr-song` rc=0 trên head.
- Nền đầy đủ trên base: 938/938 (939 ca, BỎ QUA 1), 1306 đột biến, `TỔNG: ĐẠT`, 66 phút.
- Suite đầy đủ trên `79bbbdc` trong clone ghim: đang chạy lúc ghi tệp này; kết quả cập nhật ở comment #813.
- Có chọn lọc trên head: `r813_*` + `r834_*` + codepage + mốc đột biến 103/103; mọi đột biến `r813_*` và các đột biến #812/#834 có mốc đổi hoặc
  thêm ca đích: lỗi 0.

## Cross-review Codex (`gpt-6-astra`, xhigh, qua `launcher.py run`) — 2/8 lời gọi

| lượt | head | thời lượng | verdict | lớp |
|---|---|---|---|---|
| 1 | `d789393` | 1046 s rc0 | request_changes | 4 P2: `ci-reopen-run-context-unbound`, `checkpoint-spec-context-unbound`, `checkpoint-nested-scope-unvalidated`, `r813-mutation-evidence-incomplete` |
| 2 | `79bbbdc` | 885 s rc0 | request_changes | 2 P2 còn mở, CÙNG slug: `ci-reopen-run-context-unbound`, `r813-mutation-evidence-incomplete`; 2 lớp đã đóng |

Ngoài ra có MỘT lời gọi `codex exec "Reply with exactly: OK"` lúc chủ kho đăng nhập (03:24Z), chỉ để chứng minh xác thực, không phải review.

Hiện vật: `ops/reviews/wp813-g1-codex-luot{1,2}/{PROMPT.md,VERDICT.md,run.json}`.

## Hai lớp còn mở (hướng vá executor đề xuất, CHƯA làm)

1. `ci-reopen-run-context-unbound` (lượt 2): ở nhánh đỏ `_kiem_ci(..., ket=CI_DO_THAT)` bỏ `cmd_kiem_gate`, nên mất phép so
   `head_sha` của check-run. Vá: thêm `r["head_sha"] != h` vào chốt đỏ (cạnh `if do and (r["status"] ...`), ca check-run sai head + đột biến.
2. `r813-mutation-evidence-incomplete` (lượt 2): thêm ca M5 `repository.full_name` sai kiểu ở run mới hơn và ca hai checkpoint
   `cho_phep_day` hợp lệ khác hash (quyền phải theo hiện vật MỚI NHẤT), mỗi ca một đột biến đúng predicate. Không đổi mã sản phẩm.

## Đối chiếu đặc tả với code hiện hành

- `_doc_connector` (#834) từ chối P0–P2. Packet thêm tham số tuỳ chọn `p0p2` (list gom); `accept` không truyền ⇒ hợp đồng cũ giữ nguyên
  (63/63 `r834_*` đạt, Codex lượt 1–2 xác nhận).
- `_kiem_ci` thêm tham số `ket` (mặc định `("success",)`); ba mốc đột biến #834 đổi theo (`r834_bo_attempt_moi_nhat`, `r834_bo_job_xanh`) — cùng ngữ nghĩa.
- Thêm state `cho_chu_kho` KHÔNG làm chốt đối chiếu protocol nào đỏ; `docs/PROTOCOL_DA_PHIEN.md` không đụng.
- Slug ngoài biên nhận: executor khai `--finding-id`, phải bằng tập slug của bảng lớp biên nhận H (dùng lại `slug-ngoai-bang` +
  `thieu-lop-am` của `_du_dieu_kien_approve`). Bộ đếm chỉ đếm slug của bảng lớp.
- Hiện vật checkpoint `ops/checkpoints/*.yaml` (JSON/YAML): `packet_issue, generation, spec_hash, head_sha, pham_vi, nguoi_quyet, neo`.

## Lỗi khác lộ ra (ngoài packet)

- Hai script trợ giúp reviewer của phiên (chọn ca/đột biến) ban đầu không đặt mã thoát theo kết quả — đã sửa trước lượt 2; không thuộc kho.

## Bản vá (`git format-patch f577ab5..79bbbdc`)

<details><summary>wp813.patch — 880 dòng</summary>

```diff
From 427f8c7ad3e822a97a7f695812c5479cdaa8bded Mon Sep 17 00:00:00 2001
From: Claude <noreply@anthropic.com>
Date: Tue, 27 Oct 2026 04:00:18 +0000
Subject: [PATCH 1/3] packet_loop(#813 r2): mo-lai, chu-kho-duyet, state
 cho_chu_kho, va no #834 (M5)

M1: `_xet_dung` chan cua di tiep (begin-attempt, mo-lai, chu-kho-duyet) khi bo dem same-failure da cham; cua khep
khong bi chan. Goi sau khi moi dau vao da xac thuc.
M2: `mo-lai --nguyen-nhan ci-do|connector` tu approved_pending (head = pending_sha), slug tu bang lop bien nhan H
(I11), tap finding khac rong (I3). ci-do: check do that, connector khong P0-P2 => running. connector: refs phu bang dung
P0-P2 tren head => cho_chu_kho, ke ca tu running da mo lai bang ci-do cung generation, cung head. Quyen `mo_lai_tu` bi
thay moi lan (I6). `_doc_connector` nhan tham so gom P0-P2; accept khong truyen nen hop dong giu nguyen.
M3: `chu-kho-duyet` doc checkpoint tu origin/master sau fetch + ls-remote; cho_phep_va roi cho_chu_kho (tieu thu
mo_lai_tu), cho_phep_day ghi quyen rieng checkpoint_day o approved_pending; moi (hien vat, pham vi) dung mot lan.
M5: `_kiem_ci` kiem path/head_sha/repository cua moi workflow run TRUOC khi loc.

Ca r813_* + dot bien rieng cho tung chot.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_015GtxraWJkPicJiadY4vXJK
---
 .claude/dev/packet_loop.py      | 148 ++++++++++++++++++++++++++++-
 .claude/dev/packet_loop_test.py | 160 ++++++++++++++++++++++++++++++++
 2 files changed, 303 insertions(+), 5 deletions(-)

diff --git a/.claude/dev/packet_loop.py b/.claude/dev/packet_loop.py
index 9b2410e1..5b6ba4cd 100644
--- a/.claude/dev/packet_loop.py
+++ b/.claude/dev/packet_loop.py
@@ -210,6 +210,8 @@ CHUYEN_HOP_LE = {
     "reviewing": (),
     # #812 M2: packet áp ADR-0054 — `record-review` (biên nhận H) vào; cửa ra `accept` thuộc #834.
     "approved_pending": (),
+    # #813 M2/M3: vào bằng `mo-lai --nguyen-nhan connector`, ra CHỈ bằng `chu-kho-duyet` — không cạnh `transition` nào.
+    "cho_chu_kho": (),
     "accepted": (),
     "blocked": (),
 }
@@ -217,7 +219,7 @@ CHUYEN_HOP_LE = {
 # Các state chỉ được ghi bởi luồng review, không bao giờ bởi `transition`.
 # `reviewing` không nằm đây vì nó VÀO được bằng `transition` (từ `running`); thứ bị
 # cấm là đường RA. Bảng `CHUYEN_HOP_LE` ở trên đã cưỡng chế điều đó.
-STATE_CHI_DO_REVIEW_GHI = ("accepted", "approved_pending")
+STATE_CHI_DO_REVIEW_GHI = ("accepted", "approved_pending", "cho_chu_kho")
 
 # --- (a) same-failure theo ID ỔN ĐỊNH ----------------------------------------
 # Vì sao không dùng vân tay văn xuôi: ba lượt review liên tiếp lách được nó bằng
@@ -667,7 +669,8 @@ def _load(state_dir: Path, packet: int) -> dict:
                    and type(st.get("finding_counts")) is dict and all(type(n) is int and n >= 0 for n in st["finding_counts"].values())),
             ("posts", type(posts) is dict and all(type(r) is dict and type(r["for"]) is str and (r["consumed_by"] is None or type(r["consumed_by"]) is str) for r in posts.values())),
             ("anchor", anchor is None or type(anchor) is dict and type(anchor["attempt"]) is int and type(anchor["consumed"]) is bool and re.fullmatch(r"[0-9a-f]{32}", anchor["nonce"]) and re.fullmatch(r"[0-9a-f]{64}", st["hmac_key"])),
-            ("findings", st["finding_counts"] == {fid: sum(fid in r.get("finding_ids", []) for r in st["reviews"]) for r in st["reviews"] for fid in r.get("finding_ids", [])}),
+            ("findings", st["finding_counts"] == {fid: sum(fid in r.get("finding_ids", []) for r in so) for so in [[*st["reviews"], *(  # #813: + sự kiện `mo_lai`
+                h for h in st["history"] if h.get("event") == "mo_lai")]] for r in so for fid in r.get("finding_ids", [])}),
             ("loi-goi", all(set(g) == {"run_id", "head", "da_dung"} and RUN_ID_RE.match(g["run_id"])
                             and SHA_RE.match(g["head"]) and type(g["da_dung"]) is bool for g in goi)),
             ("dem-goi", len({g["run_id"] for g in goi}) == len(goi) <= st["codex_review_calls_used"] >= can_duoi + sum(not g["da_dung"] for g in goi)),
@@ -675,6 +678,8 @@ def _load(state_dir: Path, packet: int) -> dict:
             ("adr0054", type(st.get("luat_adr0054", False)) is bool and (st.get("luat_adr0054") is not True or type(st.get("ngu_canh_lease")) is dict)
                         and (st["state"] != "approved_pending" or st["luat_adr0054"] and SHA_RE.match(str(st.get("pending_sha"))) and type(st.get("bien_nhan_approve")) is dict)
                         and (st.get("luat_adr0054") is not True or _nc_hop_le(st["ngu_canh_lease"]))),
+            ("mo-lai", _quyen_hop_le(st.get("mo_lai_tu"), "nguyen_nhan", NGUYEN_NHAN_MO_LAI) and _quyen_hop_le(st.get("checkpoint_day"), "sha256", None)
+                       and (st["state"] != "cho_chu_kho" or st.get("luat_adr0054") is True and (st.get("mo_lai_tu") or {}).get("nguyen_nhan") == "connector")),
             ("checkpoint", pending == (st.get("ly_do") == "rescue_required")), ("truc", st.get("ly_do") != "rescue_required" or st["state"] == "blocked" and st["truc"] in TRUC_TRAN and st["truc"] == next(  # mốc chạm trần MỚI NHẤT
                 h["truc"] for h in reversed(st["history"]) if h.get("event") == "blocked_rescue_required"))) if not dung]
     except (ValueError, TypeError, KeyError, AttributeError, StopIteration) as e:
@@ -2793,11 +2798,12 @@ def _neo_connector(k: str, x: dict, head: str, biet: set):
     return "hong" if len(phia) > 1 else "hien" if phia == {True} else "cu"
 
 
-def _doc_connector(duong: str, repo: str, pr: int, head: str) -> tuple:
+def _doc_connector(duong: str, repo: str, pr: int, head: str, p0p2: list | None = None) -> tuple:
     """I7 — neo MỘT kho + MỘT PR + MỘT head; đủ trang theo tập id của TỪNG endpoint. Dạng: {"repo","pr","head_sha", <endpoint>: trang
     {"total_count","items"}}. Xong = review hoàn tất (không PENDING) trên head, hoặc kết luận `Reviewed commit:` neo head; finding đọc ở
     CẢ BA endpoint, hạng miền đóng (I3); mục của head cũ hợp lệ được bỏ qua, neo thiếu/sai/mơ hồ thì không đạt.
-    Trả ((endpoint, id) P3 còn mở, mốc id lớn nhất theo endpoint)."""
+    Trả ((endpoint, id) P3 còn mở, mốc id lớn nhất theo endpoint). #813 `mo-lai` truyền `p0p2` (list): P0–P2 trên head được GOM vào đó thay vì
+    từ chối, và connector chưa xong không phải lỗi; `accept` không truyền nên giữ đúng hợp đồng cũ."""
     d, _ = _doc_json(duong, RC_GATE)
     if not isinstance(d, dict) or (d.get("repo"), d.get("pr"), d.get("head_sha")) != (repo, pr, head):
         _die(RC_GATE, f"readback connector không neo đúng ({repo}, PR {pr}, {head})")
@@ -2811,7 +2817,7 @@ def _doc_connector(duong: str, repo: str, pr: int, head: str) -> tuple:
     if hong := [(k, x["id"]) for k, v in cua.items() for x, n in v if n == "hong"]:
         _die(RC_GATE, f"connector: mục của {BOT_CONNECTOR} có neo head thiếu/sai/mơ hồ {hong}")
     if not (any(n == "hien" for _, n in cua["issue_comments"])
-            or any(n == "hien" and x.get("state") in ("APPROVED", "COMMENTED", "CHANGES_REQUESTED") for x, n in cua["reviews"])):
+            or any(n == "hien" and x.get("state") in ("APPROVED", "COMMENTED", "CHANGES_REQUESTED") for x, n in cua["reviews"])) and p0p2 is None:
         _die(RC_GATE, f"connector chưa xong trên {head}: không review hoàn tất/kết luận nào của {BOT_CONNECTOR}")  # I3: bằng chứng dương rỗng
     p3 = []
     for k in EP_CONNECTOR:
@@ -2822,6 +2828,9 @@ def _doc_connector(duong: str, repo: str, pr: int, head: str) -> tuple:
             if n == "hien" and (hang or k == "review_comments" or x.get("state") == "CHANGES_REQUESTED"):
                 if len(hang) != 1 or not hang <= set(HANG_LOP):
                     _die(RC_GATE, f"connector {k} {x['id']}: hạng ngoài miền {HANG_LOP}: {sorted(hang)}")
+                if p0p2 is not None and hang != {"P3"}:
+                    p0p2.append((k, x["id"]))
+                    continue
                 if hang != {"P3"}:
                     _die(RC_GATE, f"connector {k} {x['id']} còn {sorted(hang)} trên {head} — DỪNG, hỏi chủ kho")
                 p3.append((k, x["id"]))
@@ -2833,6 +2842,9 @@ def _kiem_ci(a, nc: dict, h: str, state_dir: Path) -> dict:
     trỏ đúng check-run (cùng kho, app, suite), check-run ấy là bản MỚI NHẤT cùng tên trong suite, và luật `kiem-gate` xanh trên nó."""
     wr, sha_wr = _doc_json(a.workflow_runs, RC_GATE)
     runs = _trang_du(wr, "workflow_runs", "workflow_runs")
+    if not all(type(r.get("path")) is str and type(r.get("head_sha")) is str and isinstance(r.get("repository"), dict)
+               and type(r["repository"].get("full_name")) is str for r in runs):  # #813 M5: TRƯỚC lọc — run hỏng không được rơi khỏi bộ lọc
+        _die(RC_GATE, "KHÔNG ĐO ĐƯỢC: workflow_runs: mọi run phải có path/head_sha là chuỗi và repository là object có full_name chuỗi")
     moi_tep = [j for f in a.workflow_jobs for j in _trang_du(_doc_json(f, RC_GATE)[0], "jobs", f"workflow_jobs {f}")]  # đủ trang THEO TỪNG tệp
     jobs = _trang_du({"total_count": len({j["id"] for j in moi_tep}), "jobs": moi_tep}, "jobs", "workflow_jobs (gộp các tệp)")
     if not all(type(j.get("run_id")) is int and type(j.get("run_attempt")) is int and j["run_attempt"] > 0
@@ -2916,6 +2928,113 @@ def cmd_accept(a, state_dir: Path) -> int:
     return RC_OK
 
 
+# --- #813 MAY-ADR-0054-b (`ops/specs/wp813-r2.md` + phần chung): `mo-lai` (approved_pending → running | cho_chu_kho) · `chu-kho-duyet`.
+NGUYEN_NHAN_MO_LAI, CI_DO_THAT, PHAM_VI_CHECKPOINT = ("ci-do", "connector"), ("failure", "timed_out", "startup_failure"), ("cho_phep_va", "cho_phep_day")
+CUA_DI_TIEP = ("begin-attempt", "mo-lai", "chu-kho-duyet")  # I5: cửa đưa packet đi tiếp mà bộ đếm same-failure đã chạm phải chặn
+KHOA_CHECKPOINT = {"packet_issue": int, "generation": int, "head_sha": str, "pham_vi": list, "nguoi_quyet": str, "neo": str}
+
+
+def _quyen_hop_le(q, khoa: str, mien) -> bool:
+    """I6: quyền phái sinh (`mo_lai_tu`, `checkpoint_day`) neo (nguyên nhân | sha256 hiện vật, generation, sha) — hoặc vắng."""
+    return q is None or (type(q) is dict and set(q) == {khoa, "generation", "sha"} and type(q[khoa]) is str and (mien is None or q[khoa] in mien)
+                         and type(q["generation"]) is int and type(q["sha"]) is str and bool(SHA_RE.match(q["sha"])))
+
+
+def cmd_mo_lai(a, state_dir: Path) -> int:
+    """M2 — `ci-do`: từ approved_pending (head = pending_sha), mọi check khai trong biên nhận là check ĐỎ THẬT trên head và connector không
+    còn P0–P2 ⇒ running. `connector`: (endpoint, id) của biên nhận phủ BẰNG ĐÚNG P0–P2 connector trên head ⇒ cho_chu_kho, từ approved_pending
+    hoặc từ running khi quyền mở lại hiện hành là `ci-do` cùng generation, cùng head. Slug từ bảng lớp biên nhận H (I11), cộng bộ đếm
+    same-failure; quyền `mo_lai_tu` bị THAY (I6). Mọi đầu vào xác thực TRƯỚC `_xet_dung` và lần ghi duy nhất (I4/I5)."""
+    st = _load(state_dir, a.packet)
+    nc, ml, connector = st.get("ngu_canh_lease"), st.get("mo_lai_tu"), a.nguyen_nhan == "connector"
+    tu_ci = connector and st["state"] == "running" and ml is not None and ml["nguyen_nhan"] == "ci-do" and ml["generation"] == (nc or {}).get("generation")
+    if st.get("luat_adr0054") is not True or not (st["state"] == "approved_pending" or tu_ci):
+        _die(RC_STATE, f"mo-lai {a.nguyen_nhan} không chạy từ {st['state']!r} (đòi approved_pending của packet áp ADR-0054"
+                       + (", hoặc running mở lại bằng ci-do cùng generation)" if connector else ")"))
+    h = ml["sha"] if tu_ci else st["pending_sha"]
+    if not a.finding_id:
+        _die(RC_ARG, "mo-lai phải có ít nhất một --finding-id (I3: tập bằng chứng dương rỗng ⇒ không đạt)")
+    bn = _du_dieu_kien_approve(st, argparse.Namespace(root=a.root, bien_nhan=a.bien_nhan, verdict="changes_requested", reviewed_sha=h, finding_id=a.finding_id))
+    khoa = "connector_refs" if connector else "check_refs"
+    dung = (lambda r: type(r) is list and len(r) == 2 and r[0] in EP_CONNECTOR and type(r[1]) is int) if connector else (lambda r: type(r) is str and r.strip())
+    refs = [tuple(r) if connector else r for x in bn["lop"] for r in (x.get(khoa) if type(x.get(khoa)) is list else [None]) if dung(r)]
+    if any(type(x.get(khoa)) is not list or not x[khoa] or connector and x["hang"] not in HANG_LOP[:3] for x in bn["lop"]) \
+            or len(refs) != sum(len(x[khoa]) for x in bn["lop"]) or len(set(refs)) != len(refs):
+        _die(RC_BIEN_NHAN, f"bảng lớp H: mỗi lớp phải có `{khoa}` khác rỗng, đúng dạng, không lặp" + (" và hạng P0–P2" if connector else ""))
+    p02 = []
+    _doc_connector(a.connector, nc["repo"], a.pr, h, p02)
+    if connector and sorted(refs) != sorted(p02):
+        _die(RC_BIEN_NHAN, f"connector: `connector_refs` phải phủ BẰNG ĐÚNG P0–P2 trên {h}: {sorted(p02)}")
+    if not connector and p02:
+        _die(RC_GATE, f"ci-do: connector còn P0–P2 {sorted(p02)} trên {h} — dùng --nguyen-nhan connector")
+    sha_cr = None
+    if not connector:
+        if not a.check_runs:
+            _die(RC_ARG, "mo-lai ci-do phải có --check-runs (trang check-runs của head, `filter=all`)")
+        _doc_check_runs(a.check_runs)
+        cr, sha_cr = _doc_json(a.check_runs, RC_GATE)
+        cr = _trang_du(cr, "check_runs", "check_runs")
+        for ten in refs:  # lượt MỚI NHẤT của đúng tên, đúng head, đúng kho, app `github-actions` — kết luận thuộc danh sách cho phép
+            r = max((r for r in cr if r["name"] == ten and r["head_sha"] == h and r.get("url") == f"{API_GH}{nc['repo']}/check-runs/{r['id']}"
+                     and (r.get("app") if isinstance(r.get("app"), dict) else {}).get("slug") == APP_CHECK), key=lambda r: r["id"], default={})
+            if r.get("status") != "completed" or r.get("conclusion") not in CI_DO_THAT:
+                _die(RC_GATE, f"ci-do: {ten!r} không phải check đỏ thật trên {h} (lượt mới nhất phải completed + {CI_DO_THAT})")
+    slugs = sorted({x["slug"] for x in bn["lop"]})
+    moi = {**st, "state": "cho_chu_kho" if connector else "running", "attempt_open": False, "reviewing_head_sha": None,
+           "mo_lai_tu": {"nguyen_nhan": a.nguyen_nhan, "generation": nc["generation"], "sha": h},
+           "finding_counts": {**st["finding_counts"], **{s: st["finding_counts"].get(s, 0) + 1 for s in slugs}},
+           "history": [*st["history"], {"event": "mo_lai", "nguyen_nhan": a.nguyen_nhan, "sha": h, "generation": nc["generation"], "finding_ids": slugs,
+                                        "refs": [list(r) if connector else r for r in refs], "bien_nhan_sha256": bn["sha256"],
+                                        "connector_sha256": _doc_json(a.connector, RC_GATE)[1], "check_runs_sha256": sha_cr}]}
+    _xet_dung(state_dir, moi, "mo-lai")  # bộ đếm vừa ghi chạm trần ⇒ ghi sổ đủ rồi blocked (I4)
+    _save(state_dir, moi)
+    print(f"mo-lai {a.nguyen_nhan} trên {h} — finding {slugs}, state {moi['state']}")
+    return RC_OK
+
+
+def cmd_chu_kho_duyet(a, state_dir: Path) -> int:
+    """M3 (Đ): hiện vật checkpoint đọc từ `origin/master` SAU khi máy tự fetch và khớp `ls-remote` — chỉ thứ chủ kho đã merge. `cho_phep_va`:
+    rời cho_chu_kho về running, head = sha đã mở lại (tiêu thụ `mo_lai_tu`). `cho_phep_day`: ở approved_pending, head = pending_sha ⇒ ghi
+    quyền riêng `checkpoint_day` cho #816, không đổi state. Mỗi (hiện vật, phạm vi) dùng MỘT lần (I6)."""
+    import yaml
+    st, root = _load(state_dir, a.packet), Path(a.root)
+    pv = {"cho_chu_kho": "cho_phep_va", "approved_pending": "cho_phep_day"}.get(st["state"])
+    if st.get("luat_adr0054") is not True or pv is None:
+        _die(RC_STATE, f"chu-kho-duyet chỉ chạy ở cho_chu_kho / approved_pending của packet áp ADR-0054 (đang {st['state']!r})")
+    p = PurePosixPath(a.checkpoint_path)
+    if p.parts[:2] != ("ops", "checkpoints") or len(p.parts) < 3 or ".." in p.parts or p.suffix != ".yaml":
+        _die(RC_ARG, f"--checkpoint-path phải là ops/checkpoints/<tên>.yaml: {a.checkpoint_path!r}")
+    m = "refs/remotes/origin/master"
+    if _git_do(root, "fetch", "-q", "origin", f"+refs/heads/master:{m}")[0]:
+        _die(RC_GUARD, "KHÔNG ĐO ĐƯỢC: `git fetch origin master` không chạy được")
+    xa, gan = _git_do(root, "ls-remote", "origin", "refs/heads/master"), _git_do(root, "rev-parse", "-q", "--verify", f"{m}^{{commit}}")
+    if xa[0] or gan[0] or xa[1].split() != [gan[1].strip(), b"refs/heads/master"]:
+        _die(RC_GUARD, "origin/master cục bộ lệch ls-remote — không đọc checkpoint từ ref chưa đo")
+    rc, raw = _git_do(root, "show", f"{gan[1].decode().strip()}:{a.checkpoint_path}")
+    try:
+        d = yaml.safe_load(raw) if rc == 0 else None
+    except (yaml.YAMLError, RecursionError):
+        d = None
+    if rc or type(d) is not dict or set(d) != set(KHOA_CHECKPOINT) or any(type(d[k]) is not t for k, t in KHOA_CHECKPOINT.items()):
+        _die(RC_GUARD, f"checkpoint {a.checkpoint_path} không có trên origin/master hoặc sai lược đồ {sorted(KHOA_CHECKPOINT)}")
+    ml, sha = st.get("mo_lai_tu"), hashlib.sha256(raw).hexdigest()
+    h = ml["sha"] if pv == "cho_phep_va" else st["pending_sha"]
+    loi = [ten for ten, dung in (
+        ("packet", d["packet_issue"] == st["packet"]), ("generation", d["generation"] == st["ngu_canh_lease"]["generation"]),
+        ("head_sha", d["head_sha"] == h), ("nguoi_quyet", d["nguoi_quyet"] in NGUOI_CO_THAM_QUYEN),
+        ("neo", bool(REPO_RE.fullmatch(d["neo"]))), ("pham_vi", bool(d["pham_vi"]) and set(d["pham_vi"]) <= set(PHAM_VI_CHECKPOINT) and pv in d["pham_vi"]),
+        ("da_dung", not any(x.get("event") == "chu_kho_duyet" and (x.get("sha256"), x.get("pham_vi")) == (sha, pv) for x in st["history"]))) if not dung]
+    if loi:
+        _die(RC_GUARD, f"checkpoint {a.checkpoint_path} không mở được {pv} trên {h}: {loi}")
+    su_kien = {"event": "chu_kho_duyet", "pham_vi": pv, "sha256": sha, "head_sha": h, "checkpoint_path": a.checkpoint_path}
+    moi = {**st, "history": [*st["history"], su_kien], **({"state": "running", "mo_lai_tu": None} if pv == "cho_phep_va" else
+                                                           {"checkpoint_day": {"sha256": sha, "generation": d["generation"], "sha": h}})}
+    _xet_dung(state_dir, moi, "chu-kho-duyet")
+    _save(state_dir, moi)
+    print(f"chu-kho-duyet {pv} trên {h} — state {moi['state']}")
+    return RC_OK
+
+
 def _xet_dung(state_dir: Path, st: dict, cua: str, a=None, cham_tran=()) -> None:
     """I5 (M4): hàm DUY NHẤT xét MỌI điều kiện dừng (trần lượt, trần vòng, same-failure, rescue sau review), gọi SAU khi đầu vào của cửa
     đã được xác thực (I4). `a`/`cham_tran` = đối số review + finding chạm trần, khi kết quả lượt đã ghi sổ. Packet áp ADR-0054 không bị trần vòng chặn
@@ -2927,6 +3046,8 @@ def _xet_dung(state_dir: Path, st: dict, cua: str, a=None, cham_tran=()) -> None
     if cua == "record-review" and a is None and st.get("luat_adr0054") is not True:
         if st["review_rounds_used"] >= st["review_rounds_limit"]:  # review MỚI khi trần vòng đã chạm (state v1 cũ / sửa tay) ⇒ rescue, kể cả approve
             _vao_rescue(state_dir, st, "vong_review", "review vượt trần vòng")
+    if cua in CUA_DI_TIEP and not cham_tran:  # #813 M1: bộ đếm đã chạm (kể cả vừa cộng ở `mo-lai`) chặn cửa đi tiếp; cửa khép không ở đây
+        cham_tran = sorted(f for f, n in st["finding_counts"].items() if n >= st["same_failure_limit"])
     if cham_tran:
         st.update(state="blocked", history=[*st["history"], {"event": "blocked_same_failure", "finding_ids": cham_tran}])
         _save(state_dir, st)
@@ -3147,6 +3268,23 @@ def build_parser() -> argparse.ArgumentParser:
     q.add_argument("--quyet-dinh-p3", help="JSON list {nguon: offline|connector, khoa: slug, ten_no, owner, huong, ly_do}")
     q.set_defaults(fn=cmd_accept)
 
+    q = sub.add_parser("mo-lai", help="#813: approved_pending → running (ci-do) | cho_chu_kho (connector); slug từ biên nhận H, readback R trên head")
+    q.add_argument("--packet", type=int, required=True)
+    q.add_argument("--root", default=".")
+    q.add_argument("--pr", type=int, required=True)
+    q.add_argument("--nguyen-nhan", required=True, choices=NGUYEN_NHAN_MO_LAI)
+    q.add_argument("--bien-nhan", required=True, help="biên nhận H verdict changes_requested trên head: bang_lop[].connector_refs | check_refs")
+    q.add_argument("--finding-id", action="append", help="slug của bảng lớp biên nhận; khai ĐỦ mọi lớp, ít nhất một")
+    q.add_argument("--connector", required=True, help="JSON như `accept --connector`, neo đúng head")
+    q.add_argument("--check-runs", help="trang check-runs của head, `filter=all` (bắt buộc với ci-do)")
+    q.set_defaults(fn=cmd_mo_lai)
+
+    q = sub.add_parser("chu-kho-duyet", help="#813: rời cho_chu_kho (cho_phep_va) | ghi quyền cho_phep_day — checkpoint trên origin/master")
+    q.add_argument("--packet", type=int, required=True)
+    q.add_argument("--root", default=".")
+    q.add_argument("--checkpoint-path", required=True, help="ops/checkpoints/<tên>.yaml, đọc tại origin/master sau khi máy tự fetch")
+    q.set_defaults(fn=cmd_chu_kho_duyet)
+
     q = sub.add_parser("bien-nhan",
                        help="đếm biên nhận review; ĐỎ khi packet có 0 biên nhận reviewer")
     q.add_argument("--root", default=".")
diff --git a/.claude/dev/packet_loop_test.py b/.claude/dev/packet_loop_test.py
index fda3b94f..d68bcf3c 100644
--- a/.claude/dev/packet_loop_test.py
+++ b/.claude/dev/packet_loop_test.py
@@ -8811,6 +8811,166 @@ MUTANTS.update({"r834_bo_attempt_jobs_moi": (' or any(j["run_id"] == run["id"] a
                 "r834_refs_theo_tap": (" or sorted(refs) != sorted(p3):", " or set(refs) != set(p3):", ["r834_refs_lap"]), "r834_qd_thieu_truong_lot": ("set(q) == truong", "set(q) <= truong", ["r834_qd_thieu_truong"]), "r834_bo_run_id_job": ('(j.get("run_id"), j.get("run_attempt"), j.get("head_sha"), j.get("name")) == (run["id"], run["run_attempt"], h, ten_j)', '(j.get("run_attempt"), j.get("head_sha"), j.get("name")) == (run["run_attempt"], h, ten_j)', ["r834_job_run_id_khac"]), "r834_bo_ref_hong": (' or len(refs) != sum(len(x["connector_refs"]) for x in lop)', "", ["r834_refs_phan_tu_hong"]), "r834_bo_kieu_gia_tri_qd": ("all(type(v) is str and v.strip() for v in q.values())", "True", ["r834_qd_gia_tri_khong_chuoi"])})  # Codex lượt 6 (F2)
 
 
+# --- #813 MAY-ADR-0054-b: nền approved_pending THẬT (`_r812`), rồi chuỗi lệnh thật (`mo-lai`, `chu-kho-duyet`, begin/review); readback R
+# và biên nhận H dựng ở mỗi bước. Mỗi ca đổi ĐÚNG một yếu tố so với nền dương; ca âm đòi rc + lý do + state nguyên byte (I4).
+_N813, _G813 = __import__("itertools").count(), "gate (ubuntu-latest)"
+CI813, LCI813, P1_813, LCN813 = [(_G813, "failure")], [("ci-gate", "P1", [_G813])], [(11, "P1")], [("cn-bug", "P1", [["review_comments", 11]])]
+
+
+def _h813(sd):
+    st = _st(sd)
+    return st["mo_lai_tu"]["sha"] if st["state"] in ("running", "cho_chu_kho") and st.get("mo_lai_tu") else st["pending_sha"]
+
+
+def _ml813(c, sd, nn, lop, cn=(), xong=True, cr=(), ids=None):
+    """`mo-lai` thật trên head hiện hành. lop [(slug, hạng, refs)] · cn [(id, hạng)] review comment connector · cr [(tên, kết luận)]."""
+    w, h, n = c.tmp / "kho" / "w", _h813(sd), next(_N813)
+    trang = lambda k, v: {"total_count": len({i["id"] for i in v}), k: list(v)}  # noqa: E731
+    ghi = lambda ten, d: ((c.tmp / f"{n}{ten}").write_text(d if isinstance(d, str) else json.dumps(d)), c.tmp / f"{n}{ten}")[1]  # noqa: E731
+    bn = {"verdict": "changes_requested", "bang_lop": [{"slug": s, "hang": g, "connector_refs" if nn == "connector" else "check_refs": r} for s, g, r in lop]}
+    ic = [{"id": 20, "user": {"login": _CN834}, "body": f"Reviewed commit: `{h[:10]}`", "issue_url": f"{_API834}issues/55"}][:int(xong)]
+    rcm = [{"id": i, "user": {"login": _CN834}, "body": f"![{g} Badge] x", "commit_id": hh or h, "pull_request_url": f"{_API834}pulls/55"} for i, g, *hh in cn for hh in [hh[0] if hh else None]]
+    crs = [{"id": 300 + i, "name": t, "head_sha": h, "status": "completed", "conclusion": k, "check_suite": {"id": 500}, "app": {"slug": "github-actions"},
+            "url": f"{_API834}check-runs/{300 + i}", **(x[0] if x else {})} for i, (t, k, *x) in enumerate(cr)]
+    return _buoc813(c, sd, "mo-lai", "--pr", 55, "--nguyen-nhan", nn, "--bien-nhan", ghi("bn.yaml", __import__("yaml").safe_dump(_bn812(w, h, _st(sd)["ngu_canh_lease"]["spec_hash"], bn=bn))),
+                    *(x for s in ([s for s, *_ in lop] if ids is None else ids) for x in ("--finding-id", s)),
+                    "--connector", ghi("cn.json", {"repo": "o/r", "pr": 55, "head_sha": h, "reviews": trang("items", []), "review_comments": trang("items", rcm),
+                                                   "issue_comments": trang("items", ic)}), *(("--check-runs", ghi("cr.json", trang("check_runs", crs))) if cr else ()))
+
+
+def _buoc813(c, sd, lenh, *args, root=True):
+    truoc = (sd / "wp55.json").read_bytes()
+    rc, _, e = run(c.script, [lenh, "--packet", 55, *(("--root", c.tmp / "kho" / "w") if root else ()), *args], sd)
+    if _co_banner(e):
+        raise CliSapDo(f"r813 {lenh} SẬP: rc={rc}; stderr={_txt(e)[-300:]!r}")
+    return rc, e, truoc
+
+
+def _ck813(c, sd, pham_vi, nhanh="master", **doi):
+    """Hiện vật checkpoint đúng mọi trường (`doi` đổi một) đẩy lên `nhanh` của origin; HEAD cục bộ GIỮ commit ấy (đột biến đọc ref tuỳ ý thấy nó)."""
+    w, n = c.tmp / "kho" / "w", next(_N813)
+    d = {"packet_issue": 55, "generation": 1, "head_sha": _h813(sd), "pham_vi": pham_vi, "nguoi_quyet": "ducthangho",
+         "neo": "https://github.com/o/r/issues/55#issuecomment-6432755983", **doi}
+    _g(w, "checkout", "-qf", "-B", f"t813-{n}", "refs/remotes/origin/master"), (w / "ops/checkpoints").mkdir(parents=True, exist_ok=True)
+    (w / f"ops/checkpoints/c{n}.yaml").write_text(json.dumps(d)), _g(w, "add", "-A"), _g(w, "commit", "-qm", "ck"), _g(w, "push", "-q", "origin", f"HEAD:{nhanh}")
+    return _buoc813(c, sd, "chu-kho-duyet", "--checkpoint-path", f"ops/checkpoints/c{n}.yaml")
+
+
+def _sua813(sd, **kv):
+    (sd / "wp55.json").write_text(json.dumps({**_st(sd), **kv}))
+
+
+def _vao_review813(c, sd, moi=True):
+    """running → (commit mới nếu `moi`) → reviewing trên đầu nhánh lease."""
+    w = c.tmp / "kho" / "w"
+    if moi:
+        _g(w, "checkout", "-qf", "-B", "t813h", "refs/remotes/origin/agent/wp55-g1-claude"), (w / "x/b.py").write_text(f"b = {next(_N813)}\n")
+        _g(w, "add", "-A"), _g(w, "commit", "-qm", "va"), _g(w, "push", "-q", "origin", "HEAD:agent/wp55-g1-claude")
+    c.den_reviewing(sd, 55, 2, head=_g(w, "rev-parse", "refs/remotes/origin/agent/wp55-g1-claude"))
+
+
+def _approve813(c, sd):
+    """Cửa KHÉP lượt: approve bằng biên nhận H thật trên head đang review ⇒ approved_pending."""
+    w, h, g = c.tmp / "kho" / "w", _st(sd)["reviewing_head_sha"], f"g{next(_N813)}"
+    (c.tmp / f"{g}.yaml").write_text(__import__("yaml").safe_dump(_bn812(w, h, _st(sd)["ngu_canh_lease"]["spec_hash"])))
+    _doi(0, *run(c.script, ["record-codex-call", "--packet", 55, "--head", h, "--run-id", g], sd)[::2], "r813 codex-call")
+    return _buoc813(c, sd, "record-review", "--provider", "codex", "--verdict", "approve", "--reviewed-sha", h, "--codex-call", g, "--bien-nhan", c.tmp / f"{g}.yaml")
+
+
+def _ca813(*buoc, rc_doi=0, phai="", **muon):
+    """Mỗi bước nhận (c, sd) — bước giữa phải rc=0; bước CUỐI đòi `rc_doi` + `phai`; `muon` kiểm state, vắng ⇒ ca âm đòi state nguyên byte."""
+    def ca(c):
+        rc, sd, e, _ = _r812(c, "review")
+        _doi(0, rc, e, "r813 nền approved_pending")
+        for i, b in enumerate(buoc):
+            rc, e, truoc = b(c, sd) or (0, b"", None)
+            _doi(rc_doi if i == len(buoc) - 1 else 0, rc, e, f"r813 bước {i}")
+        if phai not in _txt(e):
+            raise AssertionError(f"r813: rc đúng mà lý do khác — đòi {phai!r}, stderr={_txt(e)!r}")
+        if muon:
+            _kiem(sd, "r813", **muon)
+        elif truoc is not None and (sd / "wp55.json").read_bytes() != truoc:
+            raise AssertionError("I4: state đổi sau khi bị từ chối")
+    return ca
+
+
+_CI813 = lambda c, sd, **k: _ml813(c, sd, "ci-do", LCI813, cr=CI813, **k)  # noqa: E731
+_CN813 = lambda c, sd, **k: _ml813(c, sd, "connector", LCN813, cn=P1_813, **k)  # noqa: E731
+_GH813 = lambda lim: lambda c, sd: _sua813(sd, same_failure_limit=lim)  # noqa: E731
+_VA813 = lambda c, sd: _ck813(c, sd, ["cho_phep_va"])  # noqa: E731
+CASES += [
+    ("r813_ci_do_running", _ca813(_CI813, state="running", finding_counts={"ci-gate": 1})),
+    ("r813_connector_cho_chu_kho", _ca813(_CN813, state="cho_chu_kho", finding_counts={"cn-bug": 1})),
+    ("r813_khong_finding", _ca813(lambda c, sd: _ml813(c, sd, "connector", [], ids=[]), rc_doi=2, phai="ít nhất một")),
+    ("r813_slug_ngoai_bien_nhan", _ca813(lambda c, sd: _CI813(c, sd, ids=["ci-gate", "tu-dat"]), rc_doi=11, phai="slug-ngoai-bang")),
+    ("r813_connector_tap_con", _ca813(lambda c, sd: _ml813(c, sd, "connector", LCN813, cn=[(11, "P1"), (12, "P2")]), rc_doi=11, phai="BẰNG ĐÚNG")),
+    ("r813_ci_va_p1_cung_head", _ca813(lambda c, sd: _ml813(c, sd, "ci-do", LCI813, cr=CI813, cn=P1_813), rc_doi=12, phai="dùng --nguyen-nhan connector")),
+    ("r813_ci_khong_do", _ca813(lambda c, sd: _ml813(c, sd, "ci-do", LCI813, cr=[(_G813, "success")]), rc_doi=12, phai="không phải check đỏ thật")),
+    ("r813_connector_sau_ci", _ca813(lambda c, sd: _CI813(c, sd, xong=False), _CN813, state="cho_chu_kho", finding_counts={"ci-gate": 1, "cn-bug": 1})),
+    ("r813_cham_tran_mo_lai", _ca813(_GH813(1), _CI813, rc_doi=3, state="blocked", finding_counts={"ci-gate": 1})),
+    ("r813_xet_dung_sau_dau_vao", _ca813(_CI813, _GH813(1), lambda c, sd: _ml813(c, sd, "connector", LCN813, cn=[(11, "P1"), (12, "P2")]), rc_doi=11, phai="BẰNG ĐÚNG")),
+    ("r813_begin_attempt_cham", _ca813(_CI813, _GH813(1), lambda c, sd: _buoc813(c, sd, "begin-attempt", "--provider", EXECUTOR, root=False), rc_doi=3, state="blocked")),
+    ("r813_cua_khep_khong_chan", _ca813(_CI813, lambda c, sd: _vao_review813(c, sd, moi=False), _GH813(1), _approve813, state="approved_pending")),
+    ("r813_cung_slug_hai_id", _ca813(_CN813, _VA813, _vao_review813, _approve813,
+                                     lambda c, sd: _ml813(c, sd, "connector", [("cn-bug", "P1", [["review_comments", 13]])], cn=[(11, "P1", "0" * 40), (13, "P1")]),
+                                     rc_doi=3, state="blocked", finding_counts={"cn-bug": 2})),
+    ("r813_hai_slug_doc_lap", _ca813(_CN813, _VA813, _vao_review813, _approve813,
+                                     lambda c, sd: _ml813(c, sd, "connector", [("cn-khac", "P1", [["review_comments", 13]])], cn=[(11, "P1", "0" * 40), (13, "P1")]),
+                                     state="cho_chu_kho", finding_counts={"cn-bug": 1, "cn-khac": 1})),
+    ("r813_checkpoint_va", _ca813(_CN813, _VA813, state="running", mo_lai_tu=None)),
+    ("r813_checkpoint_nhanh_khac", _ca813(_CN813, lambda c, sd: _ck813(c, sd, ["cho_phep_va"], nhanh="ops/x"), rc_doi=7, phai="không có trên origin/master")),
+    ("r813_checkpoint_packet_khac", _ca813(_CN813, lambda c, sd: _ck813(c, sd, ["cho_phep_va"], packet_issue=56), rc_doi=7, phai="['packet']")),
+    ("r813_va_lam_quyen_day", _ca813(_VA813, rc_doi=7, phai="['pham_vi']")),
+    ("r813_checkpoint_day", _ca813(lambda c, sd: _ck813(c, sd, ["cho_phep_day"]), state="approved_pending")),
+    ("r813_checkpoint_day_dung_lai", _ca813(lambda c, sd: _ck813(c, sd, ["cho_phep_day"]), lambda c, sd: _ck813(c, sd, ["cho_phep_day"]), rc_doi=7, phai="['da_dung']")),
+    ("r813_chu_kho_cham_tran", _ca813(_CN813, _GH813(1), _VA813, rc_doi=3, state="blocked")),
+    ("r813_ci_do_app_khac", _ca813(lambda c, sd: _ml813(c, sd, "ci-do", LCI813, cr=[(_G813, "failure", {"app": {"slug": "evil-app"}})]), rc_doi=12, phai="không phải check đỏ thật")),
+    ("r813_ci_do_chay_lai_xanh", _ca813(lambda c, sd: _ml813(c, sd, "ci-do", LCI813, cr=[*CI813, (_G813, "success")]), rc_doi=12, phai="không phải check đỏ thật")),
+    ("r813_connector_lop_p3", _ca813(lambda c, sd: _ml813(c, sd, "connector", [("cn-bug", "P3", [["review_comments", 11]])], cn=P1_813), rc_doi=11, phai="hạng P0–P2")),
+    ("r813_checkpoint_head_lech", _ca813(_CN813, lambda c, sd: _ck813(c, sd, ["cho_phep_va"], head_sha="0" * 40), rc_doi=7, phai="['head_sha']")),
+    ("r813_checkpoint_generation", _ca813(_CN813, lambda c, sd: _ck813(c, sd, ["cho_phep_va"], generation=2), rc_doi=7, phai="['generation']")),
+    ("r813_checkpoint_nguoi_quyet", _ca813(_CN813, lambda c, sd: _ck813(c, sd, ["cho_phep_va"], nguoi_quyet="claude"), rc_doi=7, phai="['nguoi_quyet']")),
+    ("r813_state_cho_chu_kho_mat_quyen", _ca813(_CN813, lambda c, sd: _sua813(sd, mo_lai_tu=None), lambda c, sd: _buoc813(c, sd, "status", root=False), rc_doi=8, phai="mo-lai")),
+    ("r813_m5_run_moi_thieu_repository", _r834_ca(12, lambda x, w, h: x["runs"].append(
+        {**{k: v for k, v in x["runs"][0].items() if k != "repository"}, "id": 101, "status": "in_progress", "conclusion": None}), "KHÔNG ĐO ĐƯỢC: workflow_runs")),
+    ("r813_m5_run_head_sai_kieu", _r834_ca(12, lambda x, w, h: x["runs"].append({**x["runs"][0], "id": 101, "head_sha": None}), "KHÔNG ĐO ĐƯỢC: workflow_runs")),
+]
+MUTANTS.update({
+    "r813_bo_ci_do": ('    if not connector and p02:\n', '    if False:\n', ["r813_ci_va_p1_cung_head"]),
+    "r813_ci_do_nhan_xanh": ('            if r.get("status") != "completed" or r.get("conclusion") not in CI_DO_THAT:', '            if False:', ["r813_ci_khong_do"]),
+    "r813_bo_tap_rong": ('    if not a.finding_id:\n        _die(RC_ARG, "mo-lai', '    if False:\n        _die(RC_ARG, "mo-lai', ["r813_khong_finding"]),
+    "r813_slug_tu_dat": ('reviewed_sha=h, finding_id=a.finding_id))', 'reviewed_sha=h, finding_id=None))', ["r813_slug_ngoai_bien_nhan"]),
+    "r813_tap_con_lot": ("    if connector and sorted(refs) != sorted(p02):", "    if connector and not set(refs) <= set(p02):", ["r813_connector_tap_con"]),
+    "r813_chi_tu_approved": ('    tu_ci = connector and st["state"] == "running"', '    tu_ci = False and st["state"] == "running"', ["r813_connector_sau_ci"]),
+    "r813_ci_do_doi_connector_xong": (' for x, n in cua["reviews"])) and p0p2 is None:', ' for x, n in cua["reviews"])):', ["r813_connector_sau_ci"]),
+    "r813_dem_theo_id": ('    slugs = sorted({x["slug"] for x in bn["lop"]})', '    slugs = sorted({f"id-{r[1]}" if connector else x["slug"] for x in bn["lop"] for r in x[khoa]})', ["r813_cung_slug_hai_id"]),
+    "r813_mo_lai_khong_xet": ('CUA_DI_TIEP = ("begin-attempt", "mo-lai", "chu-kho-duyet")', 'CUA_DI_TIEP = ("begin-attempt", "chu-kho-duyet")', ["r813_cham_tran_mo_lai"]),
+    "r813_begin_khong_xet": ('CUA_DI_TIEP = ("begin-attempt", "mo-lai", "chu-kho-duyet")', 'CUA_DI_TIEP = ("mo-lai", "chu-kho-duyet")', ["r813_begin_attempt_cham"]),
+    "r813_chu_kho_khong_xet": ('CUA_DI_TIEP = ("begin-attempt", "mo-lai", "chu-kho-duyet")', 'CUA_DI_TIEP = ("begin-attempt", "mo-lai")', ["r813_chu_kho_cham_tran"]),
+    "r813_chan_cua_khep": ('CUA_DI_TIEP = ("begin-attempt", "mo-lai", "chu-kho-duyet")', 'CUA_DI_TIEP = ("begin-attempt", "mo-lai", "chu-kho-duyet", "record-review")', ["r813_cua_khep_khong_chan"]),
+    "r813_xet_truoc_dau_vao": (('    st = _load(state_dir, a.packet)\n    nc, ml, connector', '    _xet_dung(state_dir, moi, "mo-lai")  # bộ đếm'),
+                               ('    st = _load(state_dir, a.packet)\n    _xet_dung(state_dir, st, "mo-lai")\n    nc, ml, connector', '    pass  # bộ đếm'), ["r813_xet_dung_sau_dau_vao"]),
+    "r813_checkpoint_ref_tuy_y": ('    rc, raw = _git_do(root, "show", f"{gan[1].decode().strip()}:{a.checkpoint_path}")', '    rc, raw = _git_do(root, "show", f"HEAD:{a.checkpoint_path}")',
+                                  ["r813_checkpoint_nhanh_khac"]),
+    "r813_bo_packet_checkpoint": ('("packet", d["packet_issue"] == st["packet"])', '("packet", True)', ["r813_checkpoint_packet_khac"]),
+    "r813_moi_pham_vi_la_du": (' and pv in d["pham_vi"]),', '),', ["r813_va_lam_quyen_day"]),
+    "r813_checkpoint_dung_lai": ('        ("da_dung", not any(', '        ("da_dung", True or not any(', ["r813_checkpoint_day_dung_lai"]),
+    "r813_va_ve_running_khong_tieu": ('{"state": "running", "mo_lai_tu": None}', '{"state": "running"}', ["r813_checkpoint_va"]),
+    "r813_m5_bo_repository": (' and isinstance(r.get("repository"), dict)\n               and type(r["repository"].get("full_name")) is str for r in runs):', " for r in runs):",
+                              ["r813_m5_run_moi_thieu_repository"]),
+    "r813_ci_do_bo_app": (' and (r.get("app") if isinstance(r.get("app"), dict) else {}).get("slug") == APP_CHECK), key=lambda r: r["id"], default={})', '), key=lambda r: r["id"], default={})',
+                          ["r813_ci_do_app_khac"]),
+    "r813_ci_do_luot_cu": ('APP_CHECK), key=lambda r: r["id"], default={})', 'APP_CHECK), key=lambda r: -r["id"], default={})', ["r813_ci_do_chay_lai_xanh"]),
+    "r813_lop_bo_hang": (' or connector and x["hang"] not in HANG_LOP[:3] for x in bn["lop"])', ' for x in bn["lop"])', ["r813_connector_lop_p3"]),
+    "r813_bo_head_checkpoint": ('("head_sha", d["head_sha"] == h)', '("head_sha", True)', ["r813_checkpoint_head_lech"]),
+    "r813_bo_generation_checkpoint": ('("generation", d["generation"] == st["ngu_canh_lease"]["generation"])', '("generation", True)', ["r813_checkpoint_generation"]),
+    "r813_bo_nguoi_quyet": ('("nguoi_quyet", d["nguoi_quyet"] in NGUOI_CO_THAM_QUYEN)', '("nguoi_quyet", True)', ["r813_checkpoint_nguoi_quyet"]),
+    "r813_cho_chu_kho_khong_quyen": (' and (st["state"] != "cho_chu_kho" or st.get("luat_adr0054") is True and (st.get("mo_lai_tu") or {}).get("nguyen_nhan") == "connector")),', '),',
+                                     ["r813_state_cho_chu_kho_mat_quyen"]),
+    "r813_m5_bo_head_sha": ('    if not all(type(r.get("path")) is str and type(r.get("head_sha")) is str and ', '    if not all(type(r.get("path")) is str and ', ["r813_m5_run_head_sai_kieu"]),
+})
+
+
 def chay_suite(script: Path, tmp: Path, chi_chay=None):
     ket = {}
     for ten, fn in CASES:
-- 
2.43.0


From d7893933b0e02d6cebd1d7f5e17df05ea2a8de04 Mon Sep 17 00:00:00 2001
From: Claude <noreply@anthropic.com>
Date: Tue, 27 Oct 2026 04:23:23 +0000
Subject: [PATCH 2/3] packet_loop(#813): moc dot bien #812 khop dung mot cho;
 ma tran codepage phu mo-lai, chu-kho-duyet

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_015GtxraWJkPicJiadY4vXJK
---
 .claude/dev/packet_loop.py      |  2 +-
 .claude/dev/packet_loop_test.py | 24 +++++++++++++++---------
 2 files changed, 16 insertions(+), 10 deletions(-)

diff --git a/.claude/dev/packet_loop.py b/.claude/dev/packet_loop.py
index 5b6ba4cd..45e87949 100644
--- a/.claude/dev/packet_loop.py
+++ b/.claude/dev/packet_loop.py
@@ -3013,7 +3013,7 @@ def cmd_chu_kho_duyet(a, state_dir: Path) -> int:
     rc, raw = _git_do(root, "show", f"{gan[1].decode().strip()}:{a.checkpoint_path}")
     try:
         d = yaml.safe_load(raw) if rc == 0 else None
-    except (yaml.YAMLError, RecursionError):
+    except (RecursionError, yaml.YAMLError):  # thứ tự khác `_record_lease_ref` để mốc đột biến #812 khớp đúng một chỗ
         d = None
     if rc or type(d) is not dict or set(d) != set(KHOA_CHECKPOINT) or any(type(d[k]) is not t for k, t in KHOA_CHECKPOINT.items()):
         _die(RC_GUARD, f"checkpoint {a.checkpoint_path} không có trên origin/master hoặc sai lược đồ {sorted(KHOA_CHECKPOINT)}")
diff --git a/.claude/dev/packet_loop_test.py b/.claude/dev/packet_loop_test.py
index d68bcf3c..51a7206d 100644
--- a/.claude/dev/packet_loop_test.py
+++ b/.claude/dev/packet_loop_test.py
@@ -1791,7 +1791,13 @@ def _kich_ban_in(c: Ctx, codepage: str):
     sd_r = _reviewing(c, "--codex-review-calls-limit", 1)  # #775: rescue cần state đã chạm trần, dựng ngoài kịch bản
     _pl(c, sd_r, _goi("r1", _H1), _goi("r2", _H1, 3))
     buoc += [([b[1], "--packet", 55, *b[2:]], sd_r) for b in (_nang(0, tran=2), _rescue(0, "nang_tran"))]
-    da_phu = {"accept"}
+    c2 = Ctx(c.script, c.tmp / "cp813")  # #813: `mo-lai` rồi `chu-kho-duyet` in tiếng Việt lúc thành công — nền approved_pending riêng
+    c2.tmp.mkdir(parents=True, exist_ok=True)
+    rc, sd2, e, _ = _r812(c2, "review", env=env)
+    for ten, (rc, e, _, o) in (("mo-lai", _ml813(c2, sd2, "connector", LCN813, cn=P1_813, env=env)), ("chu-kho-duyet", _ck813(c2, sd2, ["cho_phep_va"], env=env))):
+        if rc or not o.strip():
+            raise AssertionError(f"[{codepage}] {ten} phải rc=0 và có stdout, được rc={rc}; stderr={_txt(e)!r}")
+    da_phu = {"accept", "mo-lai", "chu-kho-duyet"}
     for args, state_dir in buoc:
         rc, o, e = run(c.script, args, state_dir, env_extra=env)
         ten = args[0]
@@ -8822,7 +8828,7 @@ def _h813(sd):
     return st["mo_lai_tu"]["sha"] if st["state"] in ("running", "cho_chu_kho") and st.get("mo_lai_tu") else st["pending_sha"]
 
 
-def _ml813(c, sd, nn, lop, cn=(), xong=True, cr=(), ids=None):
+def _ml813(c, sd, nn, lop, cn=(), xong=True, cr=(), ids=None, env=None):
     """`mo-lai` thật trên head hiện hành. lop [(slug, hạng, refs)] · cn [(id, hạng)] review comment connector · cr [(tên, kết luận)]."""
     w, h, n = c.tmp / "kho" / "w", _h813(sd), next(_N813)
     trang = lambda k, v: {"total_count": len({i["id"] for i in v}), k: list(v)}  # noqa: E731
@@ -8835,25 +8841,25 @@ def _ml813(c, sd, nn, lop, cn=(), xong=True, cr=(), ids=None):
     return _buoc813(c, sd, "mo-lai", "--pr", 55, "--nguyen-nhan", nn, "--bien-nhan", ghi("bn.yaml", __import__("yaml").safe_dump(_bn812(w, h, _st(sd)["ngu_canh_lease"]["spec_hash"], bn=bn))),
                     *(x for s in ([s for s, *_ in lop] if ids is None else ids) for x in ("--finding-id", s)),
                     "--connector", ghi("cn.json", {"repo": "o/r", "pr": 55, "head_sha": h, "reviews": trang("items", []), "review_comments": trang("items", rcm),
-                                                   "issue_comments": trang("items", ic)}), *(("--check-runs", ghi("cr.json", trang("check_runs", crs))) if cr else ()))
+                                                   "issue_comments": trang("items", ic)}), *(("--check-runs", ghi("cr.json", trang("check_runs", crs))) if cr else ()), env=env)
 
 
-def _buoc813(c, sd, lenh, *args, root=True):
+def _buoc813(c, sd, lenh, *args, root=True, env=None):
     truoc = (sd / "wp55.json").read_bytes()
-    rc, _, e = run(c.script, [lenh, "--packet", 55, *(("--root", c.tmp / "kho" / "w") if root else ()), *args], sd)
+    rc, o, e = run(c.script, [lenh, "--packet", 55, *(("--root", c.tmp / "kho" / "w") if root else ()), *args], sd, env)
     if _co_banner(e):
         raise CliSapDo(f"r813 {lenh} SẬP: rc={rc}; stderr={_txt(e)[-300:]!r}")
-    return rc, e, truoc
+    return rc, e, truoc, o
 
 
-def _ck813(c, sd, pham_vi, nhanh="master", **doi):
+def _ck813(c, sd, pham_vi, nhanh="master", env=None, **doi):
     """Hiện vật checkpoint đúng mọi trường (`doi` đổi một) đẩy lên `nhanh` của origin; HEAD cục bộ GIỮ commit ấy (đột biến đọc ref tuỳ ý thấy nó)."""
     w, n = c.tmp / "kho" / "w", next(_N813)
     d = {"packet_issue": 55, "generation": 1, "head_sha": _h813(sd), "pham_vi": pham_vi, "nguoi_quyet": "ducthangho",
          "neo": "https://github.com/o/r/issues/55#issuecomment-6432755983", **doi}
     _g(w, "checkout", "-qf", "-B", f"t813-{n}", "refs/remotes/origin/master"), (w / "ops/checkpoints").mkdir(parents=True, exist_ok=True)
     (w / f"ops/checkpoints/c{n}.yaml").write_text(json.dumps(d)), _g(w, "add", "-A"), _g(w, "commit", "-qm", "ck"), _g(w, "push", "-q", "origin", f"HEAD:{nhanh}")
-    return _buoc813(c, sd, "chu-kho-duyet", "--checkpoint-path", f"ops/checkpoints/c{n}.yaml")
+    return _buoc813(c, sd, "chu-kho-duyet", "--checkpoint-path", f"ops/checkpoints/c{n}.yaml", env=env)
 
 
 def _sua813(sd, **kv):
@@ -8883,7 +8889,7 @@ def _ca813(*buoc, rc_doi=0, phai="", **muon):
         rc, sd, e, _ = _r812(c, "review")
         _doi(0, rc, e, "r813 nền approved_pending")
         for i, b in enumerate(buoc):
-            rc, e, truoc = b(c, sd) or (0, b"", None)
+            rc, e, truoc, *_ = b(c, sd) or (0, b"", None)
             _doi(rc_doi if i == len(buoc) - 1 else 0, rc, e, f"r813 bước {i}")
         if phai not in _txt(e):
             raise AssertionError(f"r813: rc đúng mà lý do khác — đòi {phai!r}, stderr={_txt(e)!r}")
-- 
2.43.0


From 79bbbdc16bd873f319ab70885039413735ee2fb3 Mon Sep 17 00:00:00 2001
From: Claude <noreply@anthropic.com>
Date: Tue, 27 Oct 2026 04:51:15 +0000
Subject: [PATCH 3/3] packet_loop(#813): va 4 lop P2 Codex luot 1

ci-reopen-run-context-unbound: ci-do dung chung phep chon ngu canh cua _kiem_ci (run/attempt/job/check-run moi nhat, app,
kho, suite) voi tap ket luan do; check_refs = [workflow, job]. accept truyen mac dinh (success) nen hop dong giu nguyen.
checkpoint-spec-context-unbound: checkpoint co spec_hash, so voi ngu canh lease (I10).
checkpoint-nested-scope-unvalidated: pham_vi kiem mien dong tung phan tu truoc moi phep so.
r813-mutation-evidence-incomplete: dot bien slug go dung predicate; them doi chung hai nguyen nhan, oracle checkpoint_day,
generation quyen ci-do, refs lap, kieu path M5.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_015GtxraWJkPicJiadY4vXJK
---
 .claude/dev/packet_loop.py      | 54 +++++++++++-----------
 .claude/dev/packet_loop_test.py | 80 +++++++++++++++++++++++----------
 2 files changed, 86 insertions(+), 48 deletions(-)

diff --git a/.claude/dev/packet_loop.py b/.claude/dev/packet_loop.py
index 45e87949..1af27c08 100644
--- a/.claude/dev/packet_loop.py
+++ b/.claude/dev/packet_loop.py
@@ -2837,9 +2837,11 @@ def _doc_connector(duong: str, repo: str, pr: int, head: str, p0p2: list | None
     return p3, {k: max((x["id"] for x in v), default=None) for k, v in ep.items()}
 
 
-def _kiem_ci(a, nc: dict, h: str, state_dir: Path) -> dict:
+def _kiem_ci(a, nc: dict, h: str, state_dir: Path, ket=("success",)) -> dict:
     """I7 — CI: check bắt buộc = (app, workflow, job); chỉ attempt MỚI NHẤT của run MỚI NHẤT trên head, đúng kho; job của attempt ấy
-    trỏ đúng check-run (cùng kho, app, suite), check-run ấy là bản MỚI NHẤT cùng tên trong suite, và luật `kiem-gate` xanh trên nó."""
+    trỏ đúng check-run (cùng kho, app, suite), check-run ấy là bản MỚI NHẤT cùng tên trong suite, và luật `kiem-gate` xanh trên nó.
+    #813 `mo-lai ci-do` dùng CHÍNH phép chọn ngữ cảnh này với `ket = CI_DO_THAT` (kết luận đỏ, miền đóng) thay cho xanh."""
+    do, nhan = ket != ("success",), "chưa xanh" if ket == ("success",) else "không đỏ thật"
     wr, sha_wr = _doc_json(a.workflow_runs, RC_GATE)
     runs = _trang_du(wr, "workflow_runs", "workflow_runs")
     if not all(type(r.get("path")) is str and type(r.get("head_sha")) is str and isinstance(r.get("repository"), dict)
@@ -2858,8 +2860,8 @@ def _kiem_ci(a, nc: dict, h: str, state_dir: Path) -> dict:
         suite, ten_bb = run.get("check_suite_id"), [j for w, j in nc["required_checks"] if w == wf]
         if type(suite) is not int or type(run.get("run_attempt")) is not int or run["run_attempt"] < 1:
             _die(RC_GATE, f"VẮNG: không run {wf} nào trên {h} trong {nc['repo']} (hoặc thiếu check_suite_id/run_attempt)")
-        if (run.get("status"), run.get("conclusion")) != ("completed", "success") or any(j["run_id"] == run["id"] and j["run_attempt"] > run["run_attempt"] for j in jobs):
-            _die(RC_GATE, f"{wf}: run {run['id']} attempt {run['run_attempt']} chưa xanh hoặc jobs có attempt mới hơn: {run.get('status')}/{run.get('conclusion')}")
+        if run.get("status") != "completed" or run.get("conclusion") not in ket or any(j["run_id"] == run["id"] and j["run_attempt"] > run["run_attempt"] for j in jobs):
+            _die(RC_GATE, f"{wf}: run {run['id']} attempt {run['run_attempt']} {nhan} hoặc jobs có attempt mới hơn: {run.get('status')}/{run.get('conclusion')}")
         for ten_j in ten_bb:
             jj = [j for j in jobs if (j.get("run_id"), j.get("run_attempt"), j.get("head_sha"), j.get("name")) == (run["id"], run["run_attempt"], h, ten_j)]
             if not jj:
@@ -2867,14 +2869,18 @@ def _kiem_ci(a, nc: dict, h: str, state_dir: Path) -> dict:
             job = max(jj, key=lambda j: j["id"])
             m = re.fullmatch(rf"{re.escape(API_GH + nc['repo'])}/check-runs/([1-9][0-9]*)", job["check_run_url"])
             r = next((x for i, x in cr.items() if str(i) == m[1]), None) if m else None  # so CHUỖI: không `int()` trên số chữ số tuỳ ý
-            if (job.get("status"), job.get("conclusion")) != ("completed", "success") or r is None or r["name"] != ten_j or r["check_suite"]["id"] != suite:
-                _die(RC_GATE, f"{wf} / {ten_j!r}: job attempt mới nhất chưa xanh hoặc không trỏ check-run của suite {suite} trong {nc['repo']}")
+            if job.get("status") != "completed" or job.get("conclusion") not in ket or r is None or r["name"] != ten_j or r["check_suite"]["id"] != suite:
+                _die(RC_GATE, f"{wf} / {ten_j!r}: job attempt mới nhất {nhan} hoặc không trỏ check-run của suite {suite} trong {nc['repo']}")
             if r.get("url") != f"{API_GH}{nc['repo']}/check-runs/{r['id']}":
                 _die(RC_GATE, f"{wf} / {ten_j!r}: check-run {r['id']} thuộc kho khác {nc['repo']}")
             if (r.get("app") if isinstance(r.get("app"), dict) else {}).get("slug") != APP_CHECK:
                 _die(RC_GATE, f"{wf} / {ten_j!r}: check-run {r['id']} không từ app {APP_CHECK!r}")
             if r["id"] != max(x["id"] for x in cr.values() if x["name"] == ten_j and x["check_suite"]["id"] == suite):
                 _die(RC_GATE, f"{wf} / {ten_j!r}: suite {suite} có check-run mới hơn {r['id']} không thuộc job của attempt mới nhất")
+            if do and (r["status"] != "completed" or r["conclusion"] not in ket):
+                _die(RC_GATE, f"{wf} / {ten_j!r}: check-run {r['id']} {nhan}: {r['status']}/{r['conclusion']}")
+        if do:
+            continue
         cmd_kiem_gate(argparse.Namespace(head=h, check_suite=str(suite), bat_buoc=ten_bb, check_runs=a.check_runs), state_dir)
     return {"workflow_runs_sha256": sha_wr, "check_runs_sha256": _doc_json(a.check_runs, RC_GATE)[1],
             "workflow_jobs_sha256": [_doc_json(f, RC_GATE)[1] for f in a.workflow_jobs]}
@@ -2931,7 +2937,7 @@ def cmd_accept(a, state_dir: Path) -> int:
 # --- #813 MAY-ADR-0054-b (`ops/specs/wp813-r2.md` + phần chung): `mo-lai` (approved_pending → running | cho_chu_kho) · `chu-kho-duyet`.
 NGUYEN_NHAN_MO_LAI, CI_DO_THAT, PHAM_VI_CHECKPOINT = ("ci-do", "connector"), ("failure", "timed_out", "startup_failure"), ("cho_phep_va", "cho_phep_day")
 CUA_DI_TIEP = ("begin-attempt", "mo-lai", "chu-kho-duyet")  # I5: cửa đưa packet đi tiếp mà bộ đếm same-failure đã chạm phải chặn
-KHOA_CHECKPOINT = {"packet_issue": int, "generation": int, "head_sha": str, "pham_vi": list, "nguoi_quyet": str, "neo": str}
+KHOA_CHECKPOINT = {"packet_issue": int, "generation": int, "spec_hash": str, "head_sha": str, "pham_vi": list, "nguoi_quyet": str, "neo": str}
 
 
 def _quyen_hop_le(q, khoa: str, mien) -> bool:
@@ -2956,8 +2962,9 @@ def cmd_mo_lai(a, state_dir: Path) -> int:
         _die(RC_ARG, "mo-lai phải có ít nhất một --finding-id (I3: tập bằng chứng dương rỗng ⇒ không đạt)")
     bn = _du_dieu_kien_approve(st, argparse.Namespace(root=a.root, bien_nhan=a.bien_nhan, verdict="changes_requested", reviewed_sha=h, finding_id=a.finding_id))
     khoa = "connector_refs" if connector else "check_refs"
-    dung = (lambda r: type(r) is list and len(r) == 2 and r[0] in EP_CONNECTOR and type(r[1]) is int) if connector else (lambda r: type(r) is str and r.strip())
-    refs = [tuple(r) if connector else r for x in bn["lop"] for r in (x.get(khoa) if type(x.get(khoa)) is list else [None]) if dung(r)]
+    dung = (lambda r: type(r) is list and len(r) == 2 and r[0] in EP_CONNECTOR and type(r[1]) is int) if connector else (
+        lambda r: type(r) is list and len(r) == 2 and all(type(y) is str and y.strip() for y in r))  # ci-do: [workflow, job] — định danh I7
+    refs = [tuple(r) for x in bn["lop"] for r in (x.get(khoa) if type(x.get(khoa)) is list else [None]) if dung(r)]
     if any(type(x.get(khoa)) is not list or not x[khoa] or connector and x["hang"] not in HANG_LOP[:3] for x in bn["lop"]) \
             or len(refs) != sum(len(x[khoa]) for x in bn["lop"]) or len(set(refs)) != len(refs):
         _die(RC_BIEN_NHAN, f"bảng lớp H: mỗi lớp phải có `{khoa}` khác rỗng, đúng dạng, không lặp" + (" và hạng P0–P2" if connector else ""))
@@ -2967,25 +2974,18 @@ def cmd_mo_lai(a, state_dir: Path) -> int:
         _die(RC_BIEN_NHAN, f"connector: `connector_refs` phải phủ BẰNG ĐÚNG P0–P2 trên {h}: {sorted(p02)}")
     if not connector and p02:
         _die(RC_GATE, f"ci-do: connector còn P0–P2 {sorted(p02)} trên {h} — dùng --nguyen-nhan connector")
-    sha_cr = None
+    sha_ci = {}
     if not connector:
-        if not a.check_runs:
-            _die(RC_ARG, "mo-lai ci-do phải có --check-runs (trang check-runs của head, `filter=all`)")
-        _doc_check_runs(a.check_runs)
-        cr, sha_cr = _doc_json(a.check_runs, RC_GATE)
-        cr = _trang_du(cr, "check_runs", "check_runs")
-        for ten in refs:  # lượt MỚI NHẤT của đúng tên, đúng head, đúng kho, app `github-actions` — kết luận thuộc danh sách cho phép
-            r = max((r for r in cr if r["name"] == ten and r["head_sha"] == h and r.get("url") == f"{API_GH}{nc['repo']}/check-runs/{r['id']}"
-                     and (r.get("app") if isinstance(r.get("app"), dict) else {}).get("slug") == APP_CHECK), key=lambda r: r["id"], default={})
-            if r.get("status") != "completed" or r.get("conclusion") not in CI_DO_THAT:
-                _die(RC_GATE, f"ci-do: {ten!r} không phải check đỏ thật trên {h} (lượt mới nhất phải completed + {CI_DO_THAT})")
+        if not (a.workflow_runs and a.workflow_jobs and a.check_runs):
+            _die(RC_ARG, "mo-lai ci-do phải có --workflow-runs, --workflow-jobs, --check-runs (readback như `accept`, trên head)")
+        sha_ci = _kiem_ci(a, {**nc, "required_checks": [list(r) for r in refs]}, h, state_dir, CI_DO_THAT)  # I7: run/attempt/job/check-run mới nhất
     slugs = sorted({x["slug"] for x in bn["lop"]})
     moi = {**st, "state": "cho_chu_kho" if connector else "running", "attempt_open": False, "reviewing_head_sha": None,
            "mo_lai_tu": {"nguyen_nhan": a.nguyen_nhan, "generation": nc["generation"], "sha": h},
            "finding_counts": {**st["finding_counts"], **{s: st["finding_counts"].get(s, 0) + 1 for s in slugs}},
            "history": [*st["history"], {"event": "mo_lai", "nguyen_nhan": a.nguyen_nhan, "sha": h, "generation": nc["generation"], "finding_ids": slugs,
-                                        "refs": [list(r) if connector else r for r in refs], "bien_nhan_sha256": bn["sha256"],
-                                        "connector_sha256": _doc_json(a.connector, RC_GATE)[1], "check_runs_sha256": sha_cr}]}
+                                        "refs": [list(r) for r in refs], "bien_nhan_sha256": bn["sha256"],
+                                        "connector_sha256": _doc_json(a.connector, RC_GATE)[1], **sha_ci}]}
     _xet_dung(state_dir, moi, "mo-lai")  # bộ đếm vừa ghi chạm trần ⇒ ghi sổ đủ rồi blocked (I4)
     _save(state_dir, moi)
     print(f"mo-lai {a.nguyen_nhan} trên {h} — finding {slugs}, state {moi['state']}")
@@ -3015,14 +3015,16 @@ def cmd_chu_kho_duyet(a, state_dir: Path) -> int:
         d = yaml.safe_load(raw) if rc == 0 else None
     except (RecursionError, yaml.YAMLError):  # thứ tự khác `_record_lease_ref` để mốc đột biến #812 khớp đúng một chỗ
         d = None
-    if rc or type(d) is not dict or set(d) != set(KHOA_CHECKPOINT) or any(type(d[k]) is not t for k, t in KHOA_CHECKPOINT.items()):
+    if rc or type(d) is not dict or set(d) != set(KHOA_CHECKPOINT) or any(type(d[k]) is not t for k, t in KHOA_CHECKPOINT.items()) \
+            or not d["pham_vi"] or not all(type(x) is str and x in PHAM_VI_CHECKPOINT for x in d["pham_vi"]):  # I3: miền đóng TỪNG phần tử
         _die(RC_GUARD, f"checkpoint {a.checkpoint_path} không có trên origin/master hoặc sai lược đồ {sorted(KHOA_CHECKPOINT)}")
     ml, sha = st.get("mo_lai_tu"), hashlib.sha256(raw).hexdigest()
     h = ml["sha"] if pv == "cho_phep_va" else st["pending_sha"]
     loi = [ten for ten, dung in (
         ("packet", d["packet_issue"] == st["packet"]), ("generation", d["generation"] == st["ngu_canh_lease"]["generation"]),
+        ("spec_hash", d["spec_hash"] == st["ngu_canh_lease"]["spec_hash"]),  # I10: đủ (packet, generation, sha, spec_hash)
         ("head_sha", d["head_sha"] == h), ("nguoi_quyet", d["nguoi_quyet"] in NGUOI_CO_THAM_QUYEN),
-        ("neo", bool(REPO_RE.fullmatch(d["neo"]))), ("pham_vi", bool(d["pham_vi"]) and set(d["pham_vi"]) <= set(PHAM_VI_CHECKPOINT) and pv in d["pham_vi"]),
+        ("neo", bool(REPO_RE.fullmatch(d["neo"]))), ("pham_vi", pv in d["pham_vi"]),
         ("da_dung", not any(x.get("event") == "chu_kho_duyet" and (x.get("sha256"), x.get("pham_vi")) == (sha, pv) for x in st["history"]))) if not dung]
     if loi:
         _die(RC_GUARD, f"checkpoint {a.checkpoint_path} không mở được {pv} trên {h}: {loi}")
@@ -3273,9 +3275,11 @@ def build_parser() -> argparse.ArgumentParser:
     q.add_argument("--root", default=".")
     q.add_argument("--pr", type=int, required=True)
     q.add_argument("--nguyen-nhan", required=True, choices=NGUYEN_NHAN_MO_LAI)
-    q.add_argument("--bien-nhan", required=True, help="biên nhận H verdict changes_requested trên head: bang_lop[].connector_refs | check_refs")
+    q.add_argument("--bien-nhan", required=True, help="biên nhận H verdict changes_requested trên head: bang_lop[].connector_refs | check_refs [[workflow, job], ...]")
     q.add_argument("--finding-id", action="append", help="slug của bảng lớp biên nhận; khai ĐỦ mọi lớp, ít nhất một")
     q.add_argument("--connector", required=True, help="JSON như `accept --connector`, neo đúng head")
+    q.add_argument("--workflow-runs", help="như `accept` (bắt buộc với ci-do)")
+    q.add_argument("--workflow-jobs", action="append", help="như `accept`; lặp mỗi run (bắt buộc với ci-do)")
     q.add_argument("--check-runs", help="trang check-runs của head, `filter=all` (bắt buộc với ci-do)")
     q.set_defaults(fn=cmd_mo_lai)
 
diff --git a/.claude/dev/packet_loop_test.py b/.claude/dev/packet_loop_test.py
index 51a7206d..2677bc6e 100644
--- a/.claude/dev/packet_loop_test.py
+++ b/.claude/dev/packet_loop_test.py
@@ -8651,7 +8651,7 @@ MUTANTS.update({
     "r834_job_vang_bo_qua": ("            if not jj:\n", "            if not jj:\n                continue\n            if False:\n", ["r834_check_vang"]),
     "r834_bo_app": ("get(\"slug\") != APP_CHECK:", "get(\"slug\") != APP_CHECK and False:", ["r834_check_app_khac"]),
     "r834_bo_path_workflow": ('r.get("path") == wf and ', "", ["r834_check_workflow_khac"]),
-    "r834_bo_attempt_moi_nhat": (('        if (run.get("status"), run.get("conclusion")) != ("completed", "success") or any(',
+    "r834_bo_attempt_moi_nhat": (('        if run.get("status") != "completed" or run.get("conclusion") not in ket or any(',
                                   '(j.get("run_id"), j.get("run_attempt"), j.get("head_sha"), j.get("name")) == (run["id"], run["run_attempt"], h, ten_j)'),
                                  ("        if False and any(", '(j.get("run_id"), j.get("head_sha"), j.get("name")) == (run["id"], h, ten_j)'),
                                  ["r834_rerun_dang_chay"]),  # phối hợp: run mới nhất chưa xanh VÀ job phải thuộc attempt mới nhất — hai lớp cùng chặn
@@ -8794,7 +8794,7 @@ CASES += [
 MUTANTS.update({
     "r834_xet_dung_truoc_h": (('    _xet_dung(state_dir, st, "accept")\n', "    slug_cn = _slug_connector("),
                               ("", '    _xet_dung(state_dir, st, "accept")\n    slug_cn = _slug_connector('), ["r834_xet_dung_sau_h"]),
-    "r834_bo_job_xanh": ('(job.get("status"), job.get("conclusion")) != ("completed", "success") or r is None', "r is None", ["r834_job_chua_xanh"]),
+    "r834_bo_job_xanh": ('job.get("status") != "completed" or job.get("conclusion") not in ket or r is None', "r is None", ["r834_job_chua_xanh"]),
     "r834_bo_p1_review_comment": (('                if hang != {"P3"}:\n', '                p3.append((k, x["id"]))\n'),
                                   ('                if hang != {"P3"} and k != "review_comments":\n', '                p3 += [(k, x["id"])] * (hang == {"P3"})\n'),
                                   ["r834_review_comment_p1"]),  # hai hunk cùng một ngữ nghĩa: bỏ chặn P1 VÀ không biến P1 thành P3
@@ -8820,7 +8820,20 @@ MUTANTS.update({"r834_bo_attempt_jobs_moi": (' or any(j["run_id"] == run["id"] a
 # --- #813 MAY-ADR-0054-b: nền approved_pending THẬT (`_r812`), rồi chuỗi lệnh thật (`mo-lai`, `chu-kho-duyet`, begin/review); readback R
 # và biên nhận H dựng ở mỗi bước. Mỗi ca đổi ĐÚNG một yếu tố so với nền dương; ca âm đòi rc + lý do + state nguyên byte (I4).
 _N813, _G813 = __import__("itertools").count(), "gate (ubuntu-latest)"
-CI813, LCI813, P1_813, LCN813 = [(_G813, "failure")], [("ci-gate", "P1", [_G813])], [(11, "P1")], [("cn-bug", "P1", [["review_comments", 11]])]
+_W813 = ".github/workflows/ci.yml"
+LCI813, P1_813, LCN813 = [("ci-gate", "P1", [[_W813, _G813]])], [(11, "P1")], [("cn-bug", "P1", [["review_comments", 11]])]
+
+
+def _ci813(x, h, run=100, suite=500, wf=_W813, ket="failure", n=0):
+    """Một run (đủ 5 job bắt buộc, check-run trỏ đúng suite) trên head; job `gate` mang kết luận `ket`, run cũng vậy."""
+    x["runs"].append({"id": run, "path": wf, "head_sha": h, "repository": {"full_name": "o/r"}, "run_attempt": 1, "status": "completed",
+                      "conclusion": ket, "check_suite_id": suite})
+    for i, j in enumerate(_J834):
+        k, cid = ket if j == _G813 else "success", 300 + n + i
+        x["jobs"].append({"id": 200 + n + i, "run_id": run, "run_attempt": 1, "name": j, "head_sha": h, "status": "completed", "conclusion": k,
+                          "check_run_url": f"{_API834}check-runs/{cid}"})
+        x["cr"].append({"id": cid, "name": j, "head_sha": h, "status": "completed", "conclusion": k, "check_suite": {"id": suite},
+                        "app": {"slug": "github-actions"}, "url": f"{_API834}check-runs/{cid}"})
 
 
 def _h813(sd):
@@ -8828,20 +8841,21 @@ def _h813(sd):
     return st["mo_lai_tu"]["sha"] if st["state"] in ("running", "cho_chu_kho") and st.get("mo_lai_tu") else st["pending_sha"]
 
 
-def _ml813(c, sd, nn, lop, cn=(), xong=True, cr=(), ids=None, env=None):
-    """`mo-lai` thật trên head hiện hành. lop [(slug, hạng, refs)] · cn [(id, hạng)] review comment connector · cr [(tên, kết luận)]."""
+def _ml813(c, sd, nn, lop, cn=(), xong=True, ci=None, ids=None, env=None):
+    """`mo-lai` thật trên head hiện hành. lop [(slug, hạng, refs)] · cn [(id, hạng)] review comment connector · ci(x, h) dựng readback CI."""
     w, h, n = c.tmp / "kho" / "w", _h813(sd), next(_N813)
     trang = lambda k, v: {"total_count": len({i["id"] for i in v}), k: list(v)}  # noqa: E731
     ghi = lambda ten, d: ((c.tmp / f"{n}{ten}").write_text(d if isinstance(d, str) else json.dumps(d)), c.tmp / f"{n}{ten}")[1]  # noqa: E731
     bn = {"verdict": "changes_requested", "bang_lop": [{"slug": s, "hang": g, "connector_refs" if nn == "connector" else "check_refs": r} for s, g, r in lop]}
     ic = [{"id": 20, "user": {"login": _CN834}, "body": f"Reviewed commit: `{h[:10]}`", "issue_url": f"{_API834}issues/55"}][:int(xong)]
     rcm = [{"id": i, "user": {"login": _CN834}, "body": f"![{g} Badge] x", "commit_id": hh or h, "pull_request_url": f"{_API834}pulls/55"} for i, g, *hh in cn for hh in [hh[0] if hh else None]]
-    crs = [{"id": 300 + i, "name": t, "head_sha": h, "status": "completed", "conclusion": k, "check_suite": {"id": 500}, "app": {"slug": "github-actions"},
-            "url": f"{_API834}check-runs/{300 + i}", **(x[0] if x else {})} for i, (t, k, *x) in enumerate(cr)]
+    x = {"runs": [], "jobs": [], "cr": []}
+    (ci or (lambda *_: None))(x, h)
     return _buoc813(c, sd, "mo-lai", "--pr", 55, "--nguyen-nhan", nn, "--bien-nhan", ghi("bn.yaml", __import__("yaml").safe_dump(_bn812(w, h, _st(sd)["ngu_canh_lease"]["spec_hash"], bn=bn))),
                     *(x for s in ([s for s, *_ in lop] if ids is None else ids) for x in ("--finding-id", s)),
                     "--connector", ghi("cn.json", {"repo": "o/r", "pr": 55, "head_sha": h, "reviews": trang("items", []), "review_comments": trang("items", rcm),
-                                                   "issue_comments": trang("items", ic)}), *(("--check-runs", ghi("cr.json", trang("check_runs", crs))) if cr else ()), env=env)
+                                                   "issue_comments": trang("items", ic)}), *(("--workflow-runs", ghi("wr.json", trang("workflow_runs", x["runs"])), "--workflow-jobs", ghi("wj.json", trang("jobs", x["jobs"])),
+                        "--check-runs", ghi("cr.json", trang("check_runs", x["cr"]))) if ci else ()), env=env)
 
 
 def _buoc813(c, sd, lenh, *args, root=True, env=None):
@@ -8855,7 +8869,7 @@ def _buoc813(c, sd, lenh, *args, root=True, env=None):
 def _ck813(c, sd, pham_vi, nhanh="master", env=None, **doi):
     """Hiện vật checkpoint đúng mọi trường (`doi` đổi một) đẩy lên `nhanh` của origin; HEAD cục bộ GIỮ commit ấy (đột biến đọc ref tuỳ ý thấy nó)."""
     w, n = c.tmp / "kho" / "w", next(_N813)
-    d = {"packet_issue": 55, "generation": 1, "head_sha": _h813(sd), "pham_vi": pham_vi, "nguoi_quyet": "ducthangho",
+    d = {"packet_issue": 55, "generation": 1, "spec_hash": _st(sd)["ngu_canh_lease"]["spec_hash"], "head_sha": _h813(sd), "pham_vi": pham_vi, "nguoi_quyet": "ducthangho",
          "neo": "https://github.com/o/r/issues/55#issuecomment-6432755983", **doi}
     _g(w, "checkout", "-qf", "-B", f"t813-{n}", "refs/remotes/origin/master"), (w / "ops/checkpoints").mkdir(parents=True, exist_ok=True)
     (w / f"ops/checkpoints/c{n}.yaml").write_text(json.dumps(d)), _g(w, "add", "-A"), _g(w, "commit", "-qm", "ck"), _g(w, "push", "-q", "origin", f"HEAD:{nhanh}")
@@ -8883,7 +8897,7 @@ def _approve813(c, sd):
     return _buoc813(c, sd, "record-review", "--provider", "codex", "--verdict", "approve", "--reviewed-sha", h, "--codex-call", g, "--bien-nhan", c.tmp / f"{g}.yaml")
 
 
-def _ca813(*buoc, rc_doi=0, phai="", **muon):
+def _ca813(*buoc, rc_doi=0, phai="", kiem=None, **muon):
     """Mỗi bước nhận (c, sd) — bước giữa phải rc=0; bước CUỐI đòi `rc_doi` + `phai`; `muon` kiểm state, vắng ⇒ ca âm đòi state nguyên byte."""
     def ca(c):
         rc, sd, e, _ = _r812(c, "review")
@@ -8893,6 +8907,8 @@ def _ca813(*buoc, rc_doi=0, phai="", **muon):
             _doi(rc_doi if i == len(buoc) - 1 else 0, rc, e, f"r813 bước {i}")
         if phai not in _txt(e):
             raise AssertionError(f"r813: rc đúng mà lý do khác — đòi {phai!r}, stderr={_txt(e)!r}")
+        if kiem and not kiem(_st(sd)):
+            raise AssertionError(f"r813: nội dung quyền sai: {_st(sd)}")
         if muon:
             _kiem(sd, "r813", **muon)
         elif truoc is not None and (sd / "wp55.json").read_bytes() != truoc:
@@ -8900,7 +8916,8 @@ def _ca813(*buoc, rc_doi=0, phai="", **muon):
     return ca
 
 
-_CI813 = lambda c, sd, **k: _ml813(c, sd, "ci-do", LCI813, cr=CI813, **k)  # noqa: E731
+_CI813 = lambda c, sd, **k: _ml813(c, sd, "ci-do", LCI813, ci=_ci813, **k)  # noqa: E731
+_CIX813 = lambda f: lambda c, sd: _ml813(c, sd, "ci-do", LCI813, ci=f)  # noqa: E731
 _CN813 = lambda c, sd, **k: _ml813(c, sd, "connector", LCN813, cn=P1_813, **k)  # noqa: E731
 _GH813 = lambda lim: lambda c, sd: _sua813(sd, same_failure_limit=lim)  # noqa: E731
 _VA813 = lambda c, sd: _ck813(c, sd, ["cho_phep_va"])  # noqa: E731
@@ -8910,8 +8927,8 @@ CASES += [
     ("r813_khong_finding", _ca813(lambda c, sd: _ml813(c, sd, "connector", [], ids=[]), rc_doi=2, phai="ít nhất một")),
     ("r813_slug_ngoai_bien_nhan", _ca813(lambda c, sd: _CI813(c, sd, ids=["ci-gate", "tu-dat"]), rc_doi=11, phai="slug-ngoai-bang")),
     ("r813_connector_tap_con", _ca813(lambda c, sd: _ml813(c, sd, "connector", LCN813, cn=[(11, "P1"), (12, "P2")]), rc_doi=11, phai="BẰNG ĐÚNG")),
-    ("r813_ci_va_p1_cung_head", _ca813(lambda c, sd: _ml813(c, sd, "ci-do", LCI813, cr=CI813, cn=P1_813), rc_doi=12, phai="dùng --nguyen-nhan connector")),
-    ("r813_ci_khong_do", _ca813(lambda c, sd: _ml813(c, sd, "ci-do", LCI813, cr=[(_G813, "success")]), rc_doi=12, phai="không phải check đỏ thật")),
+    ("r813_ci_va_p1_cung_head", _ca813(lambda c, sd: _ml813(c, sd, "ci-do", LCI813, ci=_ci813, cn=P1_813), rc_doi=12, phai="dùng --nguyen-nhan connector")),
+    ("r813_ci_khong_do", _ca813(_CIX813(lambda x, h: _ci813(x, h, ket="success")), rc_doi=12, phai="không đỏ thật")),
     ("r813_connector_sau_ci", _ca813(lambda c, sd: _CI813(c, sd, xong=False), _CN813, state="cho_chu_kho", finding_counts={"ci-gate": 1, "cn-bug": 1})),
     ("r813_cham_tran_mo_lai", _ca813(_GH813(1), _CI813, rc_doi=3, state="blocked", finding_counts={"ci-gate": 1})),
     ("r813_xet_dung_sau_dau_vao", _ca813(_CI813, _GH813(1), lambda c, sd: _ml813(c, sd, "connector", LCN813, cn=[(11, "P1"), (12, "P2")]), rc_doi=11, phai="BẰNG ĐÚNG")),
@@ -8927,11 +8944,21 @@ CASES += [
     ("r813_checkpoint_nhanh_khac", _ca813(_CN813, lambda c, sd: _ck813(c, sd, ["cho_phep_va"], nhanh="ops/x"), rc_doi=7, phai="không có trên origin/master")),
     ("r813_checkpoint_packet_khac", _ca813(_CN813, lambda c, sd: _ck813(c, sd, ["cho_phep_va"], packet_issue=56), rc_doi=7, phai="['packet']")),
     ("r813_va_lam_quyen_day", _ca813(_VA813, rc_doi=7, phai="['pham_vi']")),
-    ("r813_checkpoint_day", _ca813(lambda c, sd: _ck813(c, sd, ["cho_phep_day"]), state="approved_pending")),
+    ("r813_checkpoint_day", _ca813(lambda c, sd: _ck813(c, sd, ["cho_phep_day"]), state="approved_pending", kiem=lambda st: set(st.get("checkpoint_day") or {}) == {"sha256", "generation", "sha"}
+                                   and (st["checkpoint_day"]["generation"], st["checkpoint_day"]["sha"]) == (1, st["pending_sha"]) and len(st["checkpoint_day"]["sha256"]) == 64)),
     ("r813_checkpoint_day_dung_lai", _ca813(lambda c, sd: _ck813(c, sd, ["cho_phep_day"]), lambda c, sd: _ck813(c, sd, ["cho_phep_day"]), rc_doi=7, phai="['da_dung']")),
     ("r813_chu_kho_cham_tran", _ca813(_CN813, _GH813(1), _VA813, rc_doi=3, state="blocked")),
-    ("r813_ci_do_app_khac", _ca813(lambda c, sd: _ml813(c, sd, "ci-do", LCI813, cr=[(_G813, "failure", {"app": {"slug": "evil-app"}})]), rc_doi=12, phai="không phải check đỏ thật")),
-    ("r813_ci_do_chay_lai_xanh", _ca813(lambda c, sd: _ml813(c, sd, "ci-do", LCI813, cr=[*CI813, (_G813, "success")]), rc_doi=12, phai="không phải check đỏ thật")),
+    ("r813_ci_do_app_khac", _ca813(_CIX813(lambda x, h: _ci813(x, h) or x["cr"][0].update(app={"slug": "evil-app"})), rc_doi=12, phai="không từ app")),
+    ("r813_ci_do_run_moi_xanh", _ca813(_CIX813(lambda x, h: (_ci813(x, h), _ci813(x, h, run=101, suite=501, ket="success", n=50))), rc_doi=12, phai="không đỏ thật")),
+    ("r813_ci_do_workflow_khac", _ca813(_CIX813(lambda x, h: (_ci813(x, h, ket="success"), _ci813(x, h, run=101, suite=501, wf=".github/workflows/khac.yml", n=50))),
+                                        rc_doi=12, phai="không đỏ thật")),
+    ("r813_ci_do_check_xanh_job_do", _ca813(_CIX813(lambda x, h: _ci813(x, h) or x["cr"][0].update(conclusion="success")), rc_doi=12, phai="không đỏ thật")),
+    ("r813_quyen_ci_khac_generation", _ca813(_CI813, lambda c, sd: _sua813(sd, mo_lai_tu={**_st(sd)["mo_lai_tu"], "generation": 2}), _CN813, rc_doi=8, phai="cùng generation")),
+    ("r813_refs_lap", _ca813(lambda c, sd: _ml813(c, sd, "ci-do", [("ci-gate", "P1", [[_W813, _G813]] * 2)], ci=_ci813), rc_doi=11, phai="không lặp")),
+    ("r813_checkpoint_spec_lech", _ca813(_CN813, lambda c, sd: _ck813(c, sd, ["cho_phep_va"], spec_hash="0" * 64), rc_doi=7, phai="['spec_hash']")),
+    ("r813_checkpoint_pham_vi_la", _ca813(_CN813, lambda c, sd: _ck813(c, sd, ["cho_phep_va", "la"]), rc_doi=7, phai="sai lược đồ")),
+    ("r813_checkpoint_pham_vi_long", _ca813(_CN813, lambda c, sd: _ck813(c, sd, [["cho_phep_va"]]), rc_doi=7, phai="sai lược đồ")),
+    ("r813_m5_run_path_sai_kieu", _r834_ca(12, lambda x, w, h: x["runs"].append({**x["runs"][0], "id": 101, "path": 5}), "KHÔNG ĐO ĐƯỢC: workflow_runs")),
     ("r813_connector_lop_p3", _ca813(lambda c, sd: _ml813(c, sd, "connector", [("cn-bug", "P3", [["review_comments", 11]])], cn=P1_813), rc_doi=11, phai="hạng P0–P2")),
     ("r813_checkpoint_head_lech", _ca813(_CN813, lambda c, sd: _ck813(c, sd, ["cho_phep_va"], head_sha="0" * 40), rc_doi=7, phai="['head_sha']")),
     ("r813_checkpoint_generation", _ca813(_CN813, lambda c, sd: _ck813(c, sd, ["cho_phep_va"], generation=2), rc_doi=7, phai="['generation']")),
@@ -8941,11 +8968,21 @@ CASES += [
         {**{k: v for k, v in x["runs"][0].items() if k != "repository"}, "id": 101, "status": "in_progress", "conclusion": None}), "KHÔNG ĐO ĐƯỢC: workflow_runs")),
     ("r813_m5_run_head_sai_kieu", _r834_ca(12, lambda x, w, h: x["runs"].append({**x["runs"][0], "id": 101, "head_sha": None}), "KHÔNG ĐO ĐƯỢC: workflow_runs")),
 ]
+for _m, _t in (("r812_bo_slug_trong_bang", "r813_slug_ngoai_bien_nhan"), ("r834_bo_app", "r813_ci_do_app_khac"), ("r834_run_cu_nhat", "r813_ci_do_run_moi_xanh"),
+               ("r834_bo_path_workflow", "r813_ci_do_workflow_khac")):  # cùng chốt dùng chung ở cửa mới: đột biến gỡ chốt ấy phải giết cả ca #813
+    MUTANTS[_m][2].append(_t)
 MUTANTS.update({
     "r813_bo_ci_do": ('    if not connector and p02:\n', '    if False:\n', ["r813_ci_va_p1_cung_head"]),
-    "r813_ci_do_nhan_xanh": ('            if r.get("status") != "completed" or r.get("conclusion") not in CI_DO_THAT:', '            if False:', ["r813_ci_khong_do"]),
+    "r813_ci_do_nhan_xanh": ('h, state_dir, CI_DO_THAT)  # I7', 'h, state_dir, (*CI_DO_THAT, "success"))  # I7', ["r813_ci_khong_do"]),
+    "r813_ci_do_bo_check_do": ('            if do and (r["status"] != "completed" or r["conclusion"] not in ket):', '            if False:', ["r813_ci_do_check_xanh_job_do"]),
+    "r813_gop_nguyen_nhan": ('    slugs = sorted({x["slug"] for x in bn["lop"]})', '    slugs = ["gop"] * bool(bn["lop"])', ["r813_hai_slug_doc_lap"]),
+    "r813_bo_ghi_quyen_day": ('{"checkpoint_day": {"sha256": sha, "generation": d["generation"], "sha": h}}', "{}", ["r813_checkpoint_day"]),
+    "r813_bo_generation_quyen_ci": (' and ml["generation"] == (nc or {}).get("generation")', "", ["r813_quyen_ci_khac_generation"]),
+    "r813_bo_refs_duy_nhat": (" or len(set(refs)) != len(refs):", ":", ["r813_refs_lap"]),
+    "r813_bo_spec_hash_checkpoint": ('("spec_hash", d["spec_hash"] == st["ngu_canh_lease"]["spec_hash"])', '("spec_hash", True)', ["r813_checkpoint_spec_lech"]),
+    "r813_bo_mien_pham_vi": (' \\\n            or not d["pham_vi"] or not all(type(x) is str and x in PHAM_VI_CHECKPOINT for x in d["pham_vi"]):', ":", ["r813_checkpoint_pham_vi_la"]),
+    "r813_m5_bo_path": ('    if not all(type(r.get("path")) is str and type(r.get("head_sha"))', '    if not all(type(r.get("head_sha"))', ["r813_m5_run_path_sai_kieu"]),
     "r813_bo_tap_rong": ('    if not a.finding_id:\n        _die(RC_ARG, "mo-lai', '    if False:\n        _die(RC_ARG, "mo-lai', ["r813_khong_finding"]),
-    "r813_slug_tu_dat": ('reviewed_sha=h, finding_id=a.finding_id))', 'reviewed_sha=h, finding_id=None))', ["r813_slug_ngoai_bien_nhan"]),
     "r813_tap_con_lot": ("    if connector and sorted(refs) != sorted(p02):", "    if connector and not set(refs) <= set(p02):", ["r813_connector_tap_con"]),
     "r813_chi_tu_approved": ('    tu_ci = connector and st["state"] == "running"', '    tu_ci = False and st["state"] == "running"', ["r813_connector_sau_ci"]),
     "r813_ci_do_doi_connector_xong": (' for x, n in cua["reviews"])) and p0p2 is None:', ' for x, n in cua["reviews"])):', ["r813_connector_sau_ci"]),
@@ -8959,21 +8996,18 @@ MUTANTS.update({
     "r813_checkpoint_ref_tuy_y": ('    rc, raw = _git_do(root, "show", f"{gan[1].decode().strip()}:{a.checkpoint_path}")', '    rc, raw = _git_do(root, "show", f"HEAD:{a.checkpoint_path}")',
                                   ["r813_checkpoint_nhanh_khac"]),
     "r813_bo_packet_checkpoint": ('("packet", d["packet_issue"] == st["packet"])', '("packet", True)', ["r813_checkpoint_packet_khac"]),
-    "r813_moi_pham_vi_la_du": (' and pv in d["pham_vi"]),', '),', ["r813_va_lam_quyen_day"]),
+    "r813_moi_pham_vi_la_du": ('("pham_vi", pv in d["pham_vi"])', '("pham_vi", True)', ["r813_va_lam_quyen_day"]),
     "r813_checkpoint_dung_lai": ('        ("da_dung", not any(', '        ("da_dung", True or not any(', ["r813_checkpoint_day_dung_lai"]),
     "r813_va_ve_running_khong_tieu": ('{"state": "running", "mo_lai_tu": None}', '{"state": "running"}', ["r813_checkpoint_va"]),
     "r813_m5_bo_repository": (' and isinstance(r.get("repository"), dict)\n               and type(r["repository"].get("full_name")) is str for r in runs):', " for r in runs):",
                               ["r813_m5_run_moi_thieu_repository"]),
-    "r813_ci_do_bo_app": (' and (r.get("app") if isinstance(r.get("app"), dict) else {}).get("slug") == APP_CHECK), key=lambda r: r["id"], default={})', '), key=lambda r: r["id"], default={})',
-                          ["r813_ci_do_app_khac"]),
-    "r813_ci_do_luot_cu": ('APP_CHECK), key=lambda r: r["id"], default={})', 'APP_CHECK), key=lambda r: -r["id"], default={})', ["r813_ci_do_chay_lai_xanh"]),
     "r813_lop_bo_hang": (' or connector and x["hang"] not in HANG_LOP[:3] for x in bn["lop"])', ' for x in bn["lop"])', ["r813_connector_lop_p3"]),
     "r813_bo_head_checkpoint": ('("head_sha", d["head_sha"] == h)', '("head_sha", True)', ["r813_checkpoint_head_lech"]),
     "r813_bo_generation_checkpoint": ('("generation", d["generation"] == st["ngu_canh_lease"]["generation"])', '("generation", True)', ["r813_checkpoint_generation"]),
     "r813_bo_nguoi_quyet": ('("nguoi_quyet", d["nguoi_quyet"] in NGUOI_CO_THAM_QUYEN)', '("nguoi_quyet", True)', ["r813_checkpoint_nguoi_quyet"]),
     "r813_cho_chu_kho_khong_quyen": (' and (st["state"] != "cho_chu_kho" or st.get("luat_adr0054") is True and (st.get("mo_lai_tu") or {}).get("nguyen_nhan") == "connector")),', '),',
                                      ["r813_state_cho_chu_kho_mat_quyen"]),
-    "r813_m5_bo_head_sha": ('    if not all(type(r.get("path")) is str and type(r.get("head_sha")) is str and ', '    if not all(type(r.get("path")) is str and ', ["r813_m5_run_head_sai_kieu"]),
+    "r813_m5_bo_head_sha": ('is str and type(r.get("head_sha")) is str and isinstance', 'is str and isinstance', ["r813_m5_run_head_sai_kieu"]),
 })
 
 
-- 
2.43.0

```

</details>
