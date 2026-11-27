# HANDOFF executor — wp1466 (#1466) r11 g3, lượt 4 (bản đầy đủ do lượt 4b viết)

**TRẠNG THÁI TỆP: BẢN ĐẦY ĐỦ.** Tệp này thay bản ghi sớm lúc 02:36Z của lượt 4. Bản ghi sớm giữ nguyên ở `out/l4/HANDOFF-l4.ban-som.md`.

Handoff theo protocol §7. Nó không phải lease, cũng không phải approval. Executor không push, không mở PR, không gọi API ghi và không gọi reviewer.
Giờ ghi theo UTC, ngày 27-11-2026, lấy từ đồng hồ container. Mọi số đo đều trên commit cục bộ `c5d44c93b4aa9326fa087af0bd07cbe918c2adc2`.

## Ai viết gì

- **Toàn bộ mã của H do Claude Fable 5.2 viết, qua lượt 1 đến lượt 4.** Gồm bốn commit trên base, mọi bản vá ở `out/l*/`, và mọi script đo ở `out/sc/` mà bảng dưới dẫn tới.
- **Lượt 4 dừng vì API hết credit.** Kết quả cuối của `out/l4/run-l4.json` là `"terminal_reason":"api_error"`, `"api_error_status":400`,
  `"result":"Credit balance is too low"` (session `62e0dbab-96e1-4ec2-82c3-c8a4bbea7516`). Lượt 4 kịp commit `c5d44c9`, kịp ghi bản sớm, và kịp chạy xong mọi phép đo nặng. Nó chưa kịp chạy job gom và chưa viết bản đầy đủ.
- **Lượt 4b do Claude Opus 5.5 chạy, theo quyết định E2 của chủ kho (#1466, issuecomment-7209430125). Lượt này chỉ đo và viết handoff.**
  Nó không sửa tệp nào trong `kho/`, không commit, không gọi reviewer. Lượt 4b bắt đầu lúc 04:00:02Z (`out/l4/start-l4b.txt`).
  Chỉ thị nằm ở `PROMPT-exec-l4b.md`, sha256 `43949547…bfd44c6`, khớp `out/l4/PROMPT-l4b.sha256`.
  Lượt 4b tự chạy bốn phép đo, log mang tiền tố `l4b-`: job gom, ruff trên commit, vế âm của N3, và quét cả lớp P3 trên H.
  Mọi ô còn lại đọc từ log lượt 4 (`out/log/l4-*.log`, `out/manh-h4/`). Lượt 4b đọc từng log ấy, không chép lời khai của bản sớm.

## 0. Handoff máy đọc (§7)

```yaml
schema_version: 1
packet_id: wp1466
generation: 3
spec_hash: 9a41aa6c9d25f3bf884bc293284e3aa2f05613232c7cce8b6b2640c942dbd910
provider: claude
model_family: claude
execution_surface: claude_code
transport: machine/local
role: executor
session_id: 62e0dbab-96e1-4ec2-82c3-c8a4bbea7516   # phiên lượt 4 (Fable 5.2, viết mã); lượt 4b (Opus 5.5, đo + handoff) là phiên claude -p khác; phiên điều phối: session_015GtxrcdabvDuhzgezMEE89
base_sha: 6a4f52dde37582df5c6a562e988d9551f45ae150
head_sha: c5d44c93b4aa9326fa087af0bd07cbe918c2adc2
status: needs_followup
summary: >-
  Ba commit của lượt 1–3 được cherry-pick sạch lên base r11 6a4f52d. Sau đó lượt 4 thêm một commit (c5d44c9), áp bằng git apply.
  Commit này làm hai việc. Một: ADR-0068 bằng từng byte khối adr r11, gồm đoạn Q3, mục Nợ INV-KHOA-BAN-SAO-DINH-CHU và dòng Trạng thái dẫn r11.
  Hai: thêm 38 ca doctrine_inv_ và 14 đột biến inv_id_ ở cụm G8 để đóng lớp P3 ca-id-chi-do-mot-gia-tri.
  numstat so với 6a4f52d: 4 tệp, +478 −4, dưới trần 500. 16 mảnh có tổng nền 1861/1861 đạt; gom ĐẠT, 1899 ca bắt buộc.
  selftest 1789/1789. 43/43 đột biến mới, 21/21 đột biến cũ. doc-claims-check "ok": true, flags rỗng. ruff F delta 0.
  P3: 14/14 đột biến inv_id_ mới bị giết (inv_id_chi_nhan_99 giết 30 ca mới); quét cả lớp 41 biến thể trên H: SỐNG 0 (trước bản vá: 24 sống).
  P2 phep-dem-ban-sao-khong-phu-ca-tep chuyển sang #1469, nợ INV-KHOA-BAN-SAO-DINH-CHU (E3); không ghi là đã vá.
  N13–N16 KHÔNG ĐO ĐƯỢC. Mã do Fable 5.2 viết; lượt 4b (Opus 5.5) chỉ đo và viết handoff.
changed_paths:
  - .claude/dev/packet_loop.py
  - .claude/dev/packet_loop_test.py
  - docs/PROTOCOL_DA_PHIEN.md
  - docs/adr/0068-bat-bien-protocol-va-review-theo-lop.md
tests:
  - {name: "N1 ADR = khối adr r11", status: passed, evidence: "rc 0, `N1: ĐẠT`, 14918 byte, sha256 e15b048d…90bb; sáu số 0·11·0·0·0·0; đối chứng a1305ac (ADR r9) rc 1 `N1: KHÔNG ĐẠT`; log l4-n1-adr, l4-n1-doi-chung-head-cu"}
  - {name: "N2 protocol = nền + sáu khối", status: passed, evidence: "rc 0, 17/17 dòng ĐẠT, numstat 46 2; log l4-n2-protocol"}
  - {name: "N3 adr-song", status: passed, evidence: "H `67 ADR trên đĩa, 67 dòng`; nền 66/66; bỏ dòng ADR-0068 ⇒ rc 9 (lượt 4b đo); log l4-adr-song, l4-adr-song-nen, l4b-n3-am"}
  - {name: "N4 doctrine-scan", status: passed, evidence: "rc 0, `doctrine-scan: sạch — đã quét 12 tệp, 0 chỗ chép doctrine`; log l4-doctrine-scan"}
  - {name: "N5 tự băm độc lập", status: passed, evidence: "rc 0, 7/7 dòng → ĐẠT; log l4-n5-khoa"}
  - {name: "N6 tập bắt buộc + so-dang-ky", status: passed, evidence: "57 ca + 26 đột biến có mặt; `SỔ ĐĂNG KÝ: ĐẠT`, CASES 1804→1902, T 98, MUTANTS 2077→2120, mutants_cu_doi []; log l4-tap-bat-buoc, l4-so-dang-ky"}
  - {name: "N6(e) 16 mảnh + gom", status: passed, evidence: "16/16 bản ghi rc 0, mỗi log `TỔNG: ĐẠT`; cộng 16 dòng `nền: 1861/1861 đạt`, BỎ QUA 38; `GOM: mọi mảnh khớp phân hoạch` · `GOM: ĐẠT · 16 mảnh · 1899 ca bắt buộc`; carrier ở đúng mảnh 0; log l4-manh-tho-0/1/2, manh-h4/log, l4b-manh-gom"}
  - {name: "N7 vòng đột biến mới (43)", status: passed, evidence: "rc 0, `nền: 101/101 đạt · BỎ QUA: 0`, 43/43 dòng `ok … 3 đối chứng khác họ còn sống`, `TỔNG: ĐẠT`; log l4-db-moi"}
  - {name: "N8 do-pham-vi ma/test", status: passed, evidence: "`PHẠM VI [ma]: ĐẠT` · `PHẠM VI [test]: ĐẠT`, blob nền = 6a4f52d (sha256 khớp); log l4-n8-ma, l4-n8-test"}
  - {name: "N9 vòng đột biến cũ", status: passed, evidence: "rc 0, `nền: 132/132 đạt`, 21/21 ok, `TỔNG: ĐẠT`; log l4-db-cu"}
  - {name: "N10 ruff --select F", status: passed, evidence: "delta 0 trên commit c5d44c9 (lượt 4b) và trên index (lượt 4); log l4b-ruff-commit, l4-ruff-index"}
  - {name: "N11 tl.py --selftest", status: passed, evidence: "rc 0, `== tl selftest 1789/1789 ==`, 443 s, clone ve6/h tách khỏi clone chạy mảnh; log l4-n11-selftest"}
  - {name: "N12 numstat", status: passed, evidence: "4 tệp, +478 −4 ≤ 500 (78/1 · 201/1 · 46/2 · 153/0); log l4-numstat"}
  - {name: "doc-claims-check --strict --json", status: passed, evidence: "rc 0, \"ok\": true, \"flags\": [], files_scanned 132, claims_flagged 392 = nền; log l4-doc-claims-h, l4-doc-claims-so"}
  - {name: "quét cả lớp P3 trên H (41 biến thể)", status: passed, evidence: "rc 0, `NỀN (mã không đổi): 51/51 đạt`, `TỔNG: 41 biến thể · SỐNG 0: []` (trước bản vá trên ve4/h: SỐNG 24); lượt 4b đo; log l4b-quet-id-h, l4-quet-truoc-da4e876"}
  - {name: "hai ca CA_DAI", status: not_run, evidence: "lượt 4 không chạy; CI chạy ở packet-loop-dot-bien.yml"}
  - {name: "ci_dang_ky_test --chay, idiom_py_test, gate_lifecycle_test, bien_nhan_v2_test, chon_reviewer_test, ci_phamvi", status: not_run, evidence: "lượt 4 không chạy trên c5d44c9; chỉ eol_policy chạy (ok true, 0 vi phạm)"}
  - {name: "N13 CI PR, N14 ci-dot-bien-du, N15 kiem-merge, N16 sau land", status: not_run, evidence: "cần push/PR/CI/land, ngoài quyền"}
  - {name: "Windows", status: not_run, evidence: "chủ kho miễn (C3, E2)"}
test_selection:
  gate_tier: T2
  selector_policy_sha: null
  tested_sha: c5d44c93b4aa9326fa087af0bd07cbe918c2adc2
  selected_groups: [doc-claims-check, "doctrine_inv_* (T = 98)", họ doctrine cũ, "packet_loop_test: 16 mảnh + gom (1899 ca)", tl selftest, "quét lớp P3"]
  full_fallback_reason: "packet sensitive ⇒ chạy bộ ca packet_loop_test theo cách của CI (16 mảnh + gom), thiếu hai ca CA_DAI; bảng đột biến đầy đủ 2120 để CI (K7)"
remaining_work:
  - review mã exact-H bởi Codex trên c5d44c9 (lease ghi trần còn 1 lời gọi)
  - chủ kho audit exact-H (E5); push + PR draft + CI (N13), ci-dot-bien-du.yml (N14), kiem-merge (N15), hồ sơ sau land (N16)
  - P2 phep-dem-ban-sao-khong-phu-ca-tep ở #1469 (nợ INV-KHOA-BAN-SAO-DINH-CHU)
next_role: reviewer
manual_next_action: "Phiên điều phối: dựng mirror ghim core.abbrev 7 tại c5d44c9 (bundle out/l4/wp1466-r11-g3-c5d44c9.bundle), gọi review mã Codex theo .claude/skills/cross-review/SKILL.md; reviewer nên biết handoff này do Opus 5.5 viết trên log của Fable 5.2"
copyable_prompt: null
failure: {fingerprint: null, category: null}
successors: []
```

## 1. Kiểm đầu tiên và thẩm quyền

| phép kiểm | lệnh | kết quả |
|---|---|---|
| HEAD của `kho/` (lượt 4b) | `git rev-parse HEAD` · `git branch --show-current` | `c5d44c93b4aa9326fa087af0bd07cbe918c2adc2` trên `claude/wp1466-r11-g3`, khớp chỉ thị |
| băm đặc tả r11 | `git show 6a4f52d:ops/specs/wp1466.md \| sha256sum` | `9a41aa6c9d25f3bf884bc293284e3aa2f05613232c7cce8b6b2640c942dbd910`, khớp. Lượt 4 đo lần đầu, lượt 4b đo lại (log `l4-khoi`: 172209 byte) |
| lease | `git show ca001f8:ops/leases/wp1466-r11-g3-claude.yaml` (lượt 4b đọc object có sẵn, không fetch) | `lease_id wp1466-r11-g3-claude`, r11 g3, `thay_the_cho: [wp1466-r9-g2-claude]`, `base_sha 6a4f52d…`, nhánh `claude/wp1466-r11-g3`, write set đúng 4 tệp, `nang_tran` ≤ 6 tệp / ≤ 500 dòng thêm, hạn `2026-11-30T01:45:00Z`, `spec_blob 6969cbf0…` |
| bốn tệp write set giữa `695916e` và `6a4f52d` | `git diff --stat --exit-code 695916e 6a4f52d -- <bốn tệp>` | rc 0, output rỗng (log `l4-4tep-hai-nen`). Giữa hai base chỉ đổi `ops/**` (13 tệp, log `l4-diff-hai-nen`) |
| tài liệu phải đọc nguyên văn (lượt 4b) | Read | `.claude/skills/work-packet/SKILL.md` và `docs/PROTOCOL_DA_PHIEN.md` §7, đọc nguyên văn trong `kho/` ở `c5d44c9` |

Ba mốc §3.2.1:
- **baseline nghiệm thu** = **continuation base** = `6a4f52dde37582df5c6a562e988d9551f45ae150`, tree `92073972532b85671805a9cf7888375b4a6ab833`.
- **candidate đưa ra review** = `c5d44c93b4aa9326fa087af0bd07cbe918c2adc2`, tree `d2f22ad619c51a0bab1cd6241615d6ba6bf7ad33`.

## 2. Head, tree, numstat

HEAD = `c5d44c9`, tree `d2f22ad`, chưa push. Bốn commit trên base (log `l4-log-nhanh`):

| commit | tree | nguồn |
|---|---|---|
| `243effdadd56eaaf019ba9e804619829b1219a59` | `899aa200…` | cherry-pick `a85db94` (lượt 1, subject còn ghi r8 g1) |
| `51d1fa690b4695791fa99654610d084ffb89d920` | `78f3d0b2…` | cherry-pick `d5d96e7` (lượt 2) |
| `a1305ac552cd8e2dc5b2717e388d585b3522436e` | `2b4e3c2b…` | cherry-pick `da4e876` (lượt 3) |
| `c5d44c93b4aa9326fa087af0bd07cbe918c2adc2` | `d2f22ad6…` | lượt 4: `git apply out/l4/wp1466-l4.patch`, rồi `git commit -F out/l4/COMMIT_MSG.txt` |

Blob của H: `packet_loop.py` `0294d136…`, `packet_loop_test.py` `885d1f8e…`, protocol `dcf248b9…`, ADR `f8fe6408…`. Cả bốn mode `100644` (log `l4-blob-4-tep`).
Bundle: `out/l4/wp1466-r11-g3-c5d44c9.bundle`, sha256 `8ae02fe2…f575364`. `git bundle verify` cho `is okay`, ref `c5d44c9`, cần `6a4f52d` (log `l4-bundle-verify`).

`git diff --numstat 6a4f52d c5d44c9` (lượt 4 đo ở log `l4-numstat`; lượt 4b đo lại, cùng số):

```
78	1	.claude/dev/packet_loop.py
201	1	.claude/dev/packet_loop_test.py
46	2	docs/PROTOCOL_DA_PHIEN.md
153	0	docs/adr/0068-bat-bien-protocol-va-review-theo-lop.md
```

Tổng **+478 −4, 4 tệp**. Trần theo khối `nang_tran` là ≤ 500 dòng thêm và ≤ 6 tệp, nên **đạt, còn 22 dòng**.
Riêng lượt 4 so với `da4e876`: `packet_loop_test.py` +31 −0, ADR +6 −2 (log `l4-diff-da4e876`). `packet_loop.py` và protocol không đổi.

## 3. Cách dựng nhánh

1. `git switch -c claude/wp1466-r11-g3 origin/master` tại `6a4f52d` cho rc 0 (log `l4-tao-nhanh`).
2. `git cherry-pick a85db94 d5d96e7 da4e876` cho rc 0, **sạch, không xung đột** (log `l4-cherry-pick`): ra `243effd` (+443 −4), `51d1fa6` (+17 −17), `a1305ac` (+1 −1).
   `git diff --stat --exit-code da4e876 HEAD -- <bốn tệp>` cho rc 0, rỗng: sau cherry-pick, bốn tệp trùng byte với `da4e876` (log `l4-sau-cherry-pick-tree`).
3. Bản vá lượt 4 dựng thành tệp `out/l4/wp1466-l4.patch` (72 dòng, sha256 `913222d5…6af7e1`) bằng `out/sc/sua_l4.py`. Nó qua `git apply --check`, rồi được áp bằng **`git apply --verbose`** với rc 0: `Applied patch … cleanly` cho cả hai tệp (log `l4-apply-check`, `l4-apply`).
   Theo log, không có `git hash-object -w`, `git update-index --cacheinfo` hay `git checkout-index`. Hai bản thử trước đó (`out/l4/thu-1.patch`, `thu-2.patch`) chỉ áp vào cây thử `out/l4/thu`, không áp vào `kho/`.
4. Trước commit, `git status` chỉ có hai tệp `M`, cộng `.claude/.packet_state/` bị ignore (log `l4-status-truoc-commit`). `git diff --check` trên index và trên `6a4f52d..c5d44c9` đều rc 0 và rỗng.
   `git commit` cho `2 files changed, 37 insertions(+), 2 deletions(-)` (log `l4-commit`).
   Theo `COMMIT_MSG.txt`, hai dòng cuối của message là `Co-Authored-By: Claude Fable 5.2 …` và `Claude-Session: …session_015GtxrcdabvDuhzgezMEE89`.

## 4. `doc-claims-check`

Lệnh `python3 -B scripts/tl.py doc-claims-check --strict --json` chạy trong hai clone sạch `out/ve5/h` và `out/ve5/nen`. Cả hai dựng bằng `sc/dung_hai_ve.py`: `.git` là thư mục, không bẩn, không shallow, `core.abbrev` = 7 (lượt 4b đọc lại config).

| vế | rc | `"ok"` | `flags` | `strict` | `files_scanned` | `claims_flagged` | `advisory_count` |
|---|---|---|---|---|---|---|---|
| nền `6a4f52d` | 0 | `true` | `[]` | `true` | 131 | 392 | 392 |
| H `c5d44c9` | 0 | `true` | `[]` | `true` | 132 | 392 | 392 |

- Ở cả hai vế, `by_layer` cho mọi lớp L1…L9 và L12 bằng 0.
- So tập advisory sau khi bỏ số dòng: 0 mục chỉ có ở H, 0 mục chỉ có ở nền. Dòng kết `DOC_CLAIMS: ĐẠT` (log `l4-doc-claims-so`).
- Lượt 4b đọc thẳng JSON thô ở `l4-doc-claims-h.log`: dòng 6 `"ok": true`, dòng 18 `"flags": []`, header `# rc: 0`.

## 5. Bảng N1–N16

- Mọi lệnh chạy qua `out/sc/chay.py <nhãn>`, ghi lệnh, cwd, giờ, rc và output nguyên văn vào `out/log/<nhãn>.log`.
- "clone H" là `out/ve5/h`; "clone nền" là `out/ve5/nen`; selftest chạy ở `out/ve6/h`, cũng tại `c5d44c9`, tree `d2f22ad`.
- Cột "người đo" cho biết ai chạy lệnh: L4 là Fable 5.2, L4b là Opus 5.5. Khi ô ghi L4, lượt 4b đã đọc lại log.

| # | lệnh (rút gọn) | rc | người đo | kết quả |
|---|---|---|---|---|
| N1 | `sc/do_adr.py . c5d44c9 so` | 0 | L4 | **ĐẠT.** ADR bằng từng byte khối `adr` r11 sau khi thay 7 chỗ trống: 14918 byte, sha256 `e15b048dfc6b4f47…4f90bb`, cả hai vế. Sáu số cưỡng chế là `0·11·0·0·0·0`. Dòng Trạng thái là ngày `2026-11-27`, `spec_hash` r11, `r11`, `issuecomment-7206141143`. Phép đo có răng: chạy trên `a1305ac` (ADR r9) cho rc 1 và `N1: KHÔNG ĐẠT`, lệch ở dòng 3 và dòng 47 trở đi (log `l4-n1-doi-chung-head-cu`). Khối `adr` r9→r11 chỉ đổi ở đoạn Q3 và mục *Nợ* (log `l4-khoi`) |
| N2 | `sc/do_protocol.py . 6a4f52d c5d44c9` | 0 | L4 | **ĐẠT.** 17/17 dòng `ĐẠT`, numstat `46 2`, 28 dòng `INV-01`…`INV-28`, 18 con trỏ `ca:` không backtick. Protocol của H có sha256 `3453ab9b…e29a` |
| N3 | `adr-song --root .` trên clone H, trên clone nền, và `sc/do_n3_am.py ve5/h` | 0 · 0 · 0 | L4 · L4 · **L4b** | **ĐẠT.** H cho `67 ADR trên đĩa, 67 dòng trong §20, khớp 1–1`; nền cho 66/66. Vế âm do lượt 4b đo (log `l4b-n3-am`): `ĐÚNG nguyen_trang: rc=0` và `ĐÚNG bo_dong_ADR_0068_cua_muc_20: rc=9 (kỳ vọng 9)` |
| N4 | `doctrine-scan --root .` trên clone H | 0 | L4 | **ĐẠT.** `doctrine-scan: sạch — đã quét 12 tệp, 0 chỗ chép doctrine`. Các ca đòi rc 9 có trong T và đạt ở N7 |
| N5 | `sc/khoa_doc_lap.py <protocol H> l4/spec-r11.md <packet_loop.py H>` | 0 | L4 | **ĐẠT.** 7/7 dòng `→ ĐẠT`: băm tự tính = khối `khoa` = hằng trong mã, mỗi khoá đúng 1 bản hiển thị. `K01` = `987f952747e26847…` ở dòng 49–82. Vế "reviewer tự băm" KHÔNG ĐO ĐƯỢC ở vai executor |
| N6 | (a) `sc/do_tap_bat_buoc.py`; (b)(c)(f) `khoi-r11/so_dang_ky.py ve5/nen ve5/h`; (d) như N7; (e) `sc/chay_manh.py ve5/h manh-h4 tho k 3` ×3, rồi `… gom` | 0 | L4; gom: **L4b** | (a) **ĐẠT**: 57 ca và 26 đột biến bắt buộc đều có ở H; không cặp (tìm, thay) nào đổi; không ca đích nào bị bớt. (b) **ĐẠT**: `T_dung_tien_to: true`. (c) **ĐẠT**: \|T\| = 98 = 1902 − 1804 = 1901 − 1803 (`T_bang_hai_hieu: true`). (d) chế độ `ca-moi` riêng KHÔNG chạy ở lượt 4. Thay vào đó, lượt nền của N7 chạy đúng tập T + hai ca G9 + ca kiểm mốc: 101/101 đạt, 0 bỏ qua. (e) **ĐẠT**, xem dưới. (f) **ĐẠT**: `SỔ ĐĂNG KÝ: ĐẠT`, CASES 1804→1902, MUTANTS 2077→2120, `mutants_cu_doi: []`, `mutants_cu_giu_nguyen: true` |
| N6 (e) | 16 mảnh rồi gom | 0 | mảnh: L4; gom: **L4b** | **ĐẠT.** Ba thợ chạy từ 02:33Z, rc 0, xong lúc 03:06Z, 03:17Z và 03:07Z. Lượt 4b đọc 16 log `manh-h4/log/manh-*.log` và 16 bản ghi `manh-h4/manh/*.json`: cả 16 có rc 0 và đúng một dòng `TỔNG: ĐẠT`. Cộng 16 dòng `nền:` ra **`1861/1861 đạt`**, `BỎ QUA: 38`. Carrier WP1174 chạy ở **đúng mảnh 0** (`carrier: true`); 15 mảnh còn lại in `WP1174 carrier: KHÔNG chạy ở mảnh này`. Job gom do lượt 4b chạy lúc 04:01:23Z (log `l4b-manh-gom`, rc 0). Nó in `bản ghi mảnh: 16/16 · rc từng mảnh: [0 ×16] · tổng ca: 1899 · carrier ở mảnh: [0]`, rồi in **`GOM: mọi mảnh khớp phân hoạch`** và **`GOM: ĐẠT · 16 mảnh · 1899 ca bắt buộc (sổ 1901 − CA_DAI; CA_DAI chạy ở workflow packet-loop-dot-bien)`**. Tổng 1899 = 1861 đạt + 38 bỏ qua. So với lượt 2: 1861 − 1823 = 38 = 98 − 60, đúng số ca T mới. Hai ca `CA_DAI`: KHÔNG ĐO ĐƯỢC (mục 8) |
| N7 | `sc/chay_ca.py ve5/h ve5/nen tmp/l4-chay-ca db-moi` (không lọc tiền tố) | 0 | L4 | **ĐẠT.** `nền: 101/101 đạt · BỎ QUA: 0`. Có **43/43** dòng `ok <tên> → giết N ca đích · 3 đối chứng khác họ còn sống`: 29 đột biến cũ của T và 14 đột biến `inv_id_*` mới. Chữ "ĐỎ" chỉ xuất hiện trong dòng tiêu đề. AC 19 cho `78/78 lớp lách`; AC 18 cho `0 ngoại lệ`; dòng kết `TỔNG: ĐẠT`. Bộ đếm `lượt đột biến=42` của `manh.chay` ít hơn 43 vì đột biến `t1466_fixture_ve_trung_tinh` thuộc `MUTANTS_NHAM_TEST`: nó sửa bản sao tệp test (log in `SyntaxWarning` từ `mut_…/packet_loop_test.py` ngay trước dòng của nó), không đi qua `chay_suite` của lượt đột biến. Lượt 2 cũng lệch đúng 1 như vậy (29 dòng `ok`, `lượt đột biến=28`). Đột biến P3 ở mục 7 |
| N8 | `khoi-r11/do_pham_vi.py ma\|test l4/blob/nen/<tệp> ve5/h/<tệp>` | 0 · 0 | L4 | **ĐẠT.** `PHẠM VI [ma]: ĐẠT` và `PHẠM VI [test]: ĐẠT`. Lượt 4b đo sha256 của `l4/blob/nen/packet_loop.py` (`e339eb42…`) và `packet_loop_test.py` (`732b70ec…`): bằng `git show 6a4f52d:<tệp>` |
| N9 | `sc/chay_ca.py … db-cu` | 0 | L4 | **ĐẠT.** `nền: 132/132 đạt · BỎ QUA: 0` (họ doctrine cũ), 21/21 dòng `ok … 3 đối chứng khác họ còn sống`, `TỔNG: ĐẠT`. Hai chế độ riêng `ca-cu` (132 ca + ca mốc) và `adr` (40 ca `adr_song_*`) KHÔNG chạy ở lượt 4. Các ca ấy chạy trong 16 mảnh và đạt ở đó |
| N10 | `sc/do_ruff_ky_tu.py ../kho 6a4f52d c5d44c9` | 0 | **L4b** (L4 đo trên index) | **ĐẠT.** Delta 0 (mục 6) |
| N11 | `python3 -u -B scripts/tl.py --selftest` ở `ve6/h`; `git diff --check` | 0 · 0 | L4 | **ĐẠT.** `== tl selftest 1789/1789 ==`, 443 s, 02:33:24Z–02:40:47Z. Selftest chạy trong clone **khác** với clone chạy mảnh 0, đúng chỉ thị. `git diff --check 6a4f52d c5d44c9` không in gì |
| N12 | `git diff --numstat 6a4f52d c5d44c9` | 0 | L4, L4b đo lại | **ĐẠT.** 4 tệp, +478 −4 ≤ 500 |
| N13 | CI PR trên H | — | — | **KHÔNG ĐO ĐƯỢC.** Cần push và PR, mà cả hai bị cấm |
| N14 | `ci-dot-bien-du.yml` trên H (K7) | — | — | **KHÔNG ĐO ĐƯỢC.** Cần CI trên H đã đẩy, và không được `workflow_dispatch`. Tại chỗ chỉ đo được 43 + 21 trên tổng 2120 đột biến |
| N15 | `kiem-merge` | — | — | **KHÔNG ĐO ĐƯỢC.** Cần PR, CI, verdict review, và comment `windows: <H> mien` neo đúng H |
| N16 | sau land | — | — | **KHÔNG ĐO ĐƯỢC** |

### 5b. Bước khác của `ci.yml` đã thử tại chỗ trên `c5d44c9`

| bước | lệnh | rc | bằng chứng |
|---|---|---|---|
| job `gate`: `doc-claims-check strict` | mục 4 | 0 | `"ok": true`, `flags: []` |
| job `gate`: selftest | N11 | 0 | `1789/1789` |
| job `gate`: `eol-policy survey` | `python3 -B .githooks/eol_policy.py --all --json` trên clone H | 0 | `"ok": true`, `violations: []`, `scanned` 19035, `checked` 18102 (log `l4-eol`) |
| job `gate-ops`: `doctrine-scan` | N4 | 0 | `sạch — đã quét 12 tệp` |
| job `gate-packet-loop-manh` + `gate-packet-loop` | N6 (e) | 0 | `nền: 1861/1861`, `GOM: ĐẠT · 16 mảnh · 1899 ca bắt buộc` |

Các bước lượt 2 từng thử nhưng lượt 4 **không** chạy lại trên `c5d44c9` được liệt kê ở mục 8.

## 6. Ruff delta (N10) và ký tự lạ

Dùng `ruff 0.15.15` (bản ghim của CI), `--select F --no-cache --isolated`. Hai vế lấy từ `git show <rev>:<tệp>`.
Lượt 4b đo trên commit `c5d44c9` (log `l4b-ruff-commit`, rc 0). Lượt 4 đã đo trên index trước commit (log `l4-ruff-index`) và ra cùng số.

| tệp | nền `6a4f52d` | H `c5d44c9` | mới | mất |
|---|---|---|---|---|
| `packet_loop.py` | 3 (F841 ×3) | 3 (F841 ×3) | 0 | 0 |
| `packet_loop_test.py` | 13 (F401 ×8, F811 ×3, F541 ×2) | 13 (như nền) | 0 | 0 |

**Delta = 0.** Ký tự lạ: `packet_loop.py` có 0 ở nền và 0 ở H; `packet_loop_test.py` có 12 ở nền và 12 ở H, cùng phân bố.

## 7. Bảng lớp

### 7.1 `ca-id-chi-do-mot-gia-tri` · P3 · **đóng** (theo phép đo của executor; nhãn cuối do reviewer đặt)

- **Nguồn:** review mã exact-H lượt 1 trên `da4e876` (verdict `out/l4/VERDICT-ma-h-l1.md`, F02).
- **Biểu hiện:** sáu ca G8 đều quy về `INV-99`, nên đột biến chỉ nhận 99 sống.
- **Thẩm quyền:** r11 mục 8.3 dòng G8, cùng trần 500 (E2). Không có dòng `mien_p3`.

**Đường vào.** Lượt 4 lấy đường vào là mọi phần tử cú pháp của định nghĩa ID trần `INV-[0-9]{2}(?![0-9A-Za-z-])`, cộng mọi vế của dòng chốt ID trong `_inv_kiem_protocol`. Script `out/sc/l4_quet_id.py` liệt kê 41 biến thể. Script này không đọc sổ `MUTANTS`: nó tự dựng bản sao `packet_loop.py` cho từng biến thể, rồi chạy `chay_suite` thật của cây.

**Quét trước bản vá.** Quét trên `out/ve4/h`, tức H cũ với bộ ca của `da4e876`: 13 ca, nền 13/13 đạt, **24 trên 41 biến thể SỐNG** (log `l4-quet-truoc-da4e876`, rc 1 vì có biến thể sống).
Biến thể sống gồm: hàng chục, hàng đơn vị, tập ID, số chữ số, ba vế của luật hậu tố, tiền tố, bản che, và nơi áp chuẩn hoá.

**Ca thêm vào T ở cụm G8: 38 ca.** Danh sách lấy từ `out/l4/wp1466-l4.patch`.

| nhóm ca | số | kỳ vọng | đường vào khoá |
|---|---|---|---|
| `doctrine_inv_dong_inv_ngoai_id_00` … `_id_28`, `_id_98` | 30 | rc 9 `nằm ngoài tiểu mục` | 28 ID thật `INV-01`…`INV-28` và các biên `00`, `01`, `09`, `10`, `28`, `98`. Phủ hàng chục 0, 1, 2, 9 và hàng đơn vị 0–9 |
| `doctrine_inv_dong_khong_id_mot_chu_so_van_xanh` (`INV-9`) | 1 | rc 0 | số chữ số: một chữ số không phải ID |
| `doctrine_inv_dong_khong_id_ba_chu_so_van_xanh` (`INV-120`) | 1 | rc 0 | luật hậu tố: chữ số |
| `doctrine_inv_dong_khong_id_hau_to_chu_hoa_van_xanh` (`INV-12A`) | 1 | rc 0 | luật hậu tố: chữ hoa |
| `doctrine_inv_dong_khong_id_hau_to_chu_thuong_van_xanh` (`INV-12a`) | 1 | rc 0 | luật hậu tố: chữ thường |
| `doctrine_inv_dong_khong_id_ten_no_van_xanh` (`INV-12-CONG-VERDICT-THEO-LOP`) | 1 | rc 0 | luật hậu tố: gạch nối. Đây là đối chứng tên nợ |
| `doctrine_inv_dong_khong_id_tien_to_van_xanh` (`XNV-12 IXV-12 INX-12 INV_12 IV-12 IN-12 INV12 inv-12`) | 1 | rc 0 | tiền tố: từng chữ cái, gạch nối, có hay không, hoa hay thường |
| `doctrine_inv_dong_inv_ngoai_gach_dung_toan_khoang` (`INV-99 ｜ x ｜ …`) | 1 | rc 9 | nơi áp chuẩn hoá: điều kiện `\|` xét trên dạng hiển thị |
| `doctrine_inv_dong_inv_trong_rao_ma_van_xanh` (`INV-07` trong rào mã) | 1 | rc 0 | bản che: dòng trong rào mã không phải dạng hiển thị |

**Đột biến mới: 14, đều đăng ký trong `MUTANTS`.** Kết quả lấy từ log `l4-db-moi` trên H; mỗi dòng đều là `ok … · 3 đối chứng khác họ còn sống`.

| đột biến | thay `_INV_ID_TRAN` hay dòng chốt thành | ca đích | giết |
|---|---|---|---|
| `inv_id_chi_nhan_99` | `INV-99…`, **đột biến do G8 đòi** | 30 ca `id_*` | **30** |
| `inv_id_hang_chuc_chi_9` | `INV-9[0-9]…` | 29 ca `id_*` có hàng chục ≠ 9 | 29 |
| `inv_id_hang_don_vi_chi_9` | `INV-[0-9]9…` | 28 ca `id_*` có hàng đơn vị ≠ 9 | 28 |
| `inv_id_chi_id_hien_hanh` | `INV-(?:0[1-9]\|1[0-9]\|2[0-8])…` | `id_00`, `id_98` và sáu ca `INV-99` cũ | 8 |
| `inv_id_nhan_mot_chu_so` | `INV-[0-9]{1,2}…` | `khong_id_mot_chu_so` | 1 |
| `inv_id_bo_hau_to_so` | `(?![A-Za-z-])` | `khong_id_ba_chu_so` | 1 |
| `inv_id_bo_hau_to_chu_hoa` | `(?![0-9a-z-])` | `khong_id_hau_to_chu_hoa` | 1 |
| `inv_id_bo_hau_to_chu_thuong` | `(?![0-9A-Z-])` | `khong_id_hau_to_chu_thuong` | 1 |
| `inv_id_bo_hau_to_gach` | `(?![0-9A-Za-z])` | `khong_id_ten_no`, `doctrine_scan_repo_that_sach` | 2 |
| `inv_id_khong_phan_biet_hoa_thuong` | `(?i)INV-…` | `khong_id_tien_to` | 1 |
| `inv_id_tien_to_ky_tu_bat_ky` | `INV.[0-9]{2}…` | `khong_id_tien_to` | 1 |
| `inv_id_tien_to_tuy_chon` | `INV-?[0-9]{2}…` | `khong_id_tien_to` | 1 |
| `inv_id_gach_dung_khong_chuan_hoa` | `"\|" in x` thay cho `"\|" in nhin(x)` | `dong_inv_ngoai_gach_dung_toan_khoang` | 1 |
| `inv_id_doc_ca_vung_che` | đọc dòng thô thay cho dòng đã che | `dong_inv_trong_rao_ma_van_xanh` | 1 |

Ba đột biến G8 cũ vẫn bị giết trên H: `inv_bo_kiem_id_ngoai` giết 6, `inv_id_chi_dang_chuan` giết 2, `inv_id_khong_chuan_hoa` giết 3. Như vậy:
- **Đột biến "chỉ nhận 99" bị chính các ca mới giết**, đủ 30 ca `id_*`.
- **Ba đối chứng khác họ còn sống** ở mọi dòng.
- Đối chứng tên nợ và luật hậu tố được giữ: ca `ten_no` đòi xanh, và `inv_id_bo_hau_to_gach` giết nó.

**Quét cả lớp trên H cuối `c5d44c9`** do lượt 4b chạy (log `l4b-quet-id-h`, rc 0, 04:03:43Z–04:28:36Z, 1493 s). Tập ca có 51 ca: 37 ca ID đòi đỏ, 12 ca xanh họ `doctrine_inv`, 2 ca G9. Kết quả: `NỀN (mã không đổi): 51/51 đạt`, 41 dòng `chết`, và dòng kết **`TỔNG: 41 biến thể · SỐNG 0: []`**.
- Trước bản vá có 24 biến thể sống; trên H, cả 24 đều chết.
- Lượt thử giữa chừng (log `l4-quet-thu-1b`, cây `l4/thu`, 17 biến thể) còn 8 biến thể sống: sáu biến thể tiền tố từng chữ, `id_doc_dong_tho`, và `gach_dung_tren_dong_chua_chuan_hoa`. Trên H, cả tám đều chết, nhờ ba ca thêm ở bản thử thứ hai: `khong_id_tien_to`, `trong_rao_ma`, `gach_dung_toan_khoang`.
- `git status --short --ignored` của `ve5/h` sau phép quét: rỗng.
- Lưu ý cho reviewer: chỉ 14 trong 41 biến thể có đột biến đăng ký trong `MUTANTS`. 27 biến thể còn lại chỉ do script quét đo, và CI không chạy script này. Đó là các dạng khác của cùng đường vào, ví dụ `chuc_0_den_8`, `I_bat_ky`, `N_tuy_chon`, `dung_ba`. Mỗi đường vào ở bảng ca trên có ít nhất một đột biến đăng ký giết nó. Riêng hàng đơn vị chỉ có `inv_id_hang_don_vi_chi_9` được đăng ký, còn `don_vi_khong_0` và `don_vi_0_den_8` chỉ do script quét đo. Executor không tự xếp đây là lỗ hở; nhãn do reviewer đặt.

**Không sinh biểu hiện mới.** 16 mảnh (1861/1861) và vòng đột biến cũ (132/132, 21/21) đều xanh. `doctrine-scan` vẫn sạch trên repo thật. `packet_loop.py` không đổi so với `da4e876`.

### 7.2 `phep-dem-ban-sao-khong-phu-ca-tep` · P2 · **CHUYỂN sang #1469**, không phải đã vá

- **Nguồn:** executor lượt 1 (Q3); review mã exact-H lượt 1 trên `da4e876`, F01.a–d. Reviewer đo được 23 trên 43 biến thể bản sao nguyên byte không đứng thành đơn vị vẫn cho rc 0.
- **Thẩm quyền:** quyết định Q3 (E3) ở issuecomment-7201538748; r10 và r11 mục 0, mục 8.3; `INV-KHOA-BAN-SAO-DINH-CHU` (giao Issue #1469).
- **Đã làm trên H:** thu hẹp **lời hứa**, không đổi mã.
  - ADR-0068 nay nói phép (3) chỉ đếm bản sao "đứng thành đơn vị cùng loại (trọn mục, hay khối)".
  - Mục *Nợ* có thêm dòng `INV-KHOA-BAN-SAO-DINH-CHU`.
  - Cả hai bằng từng byte khối `adr` r11 (N1).
  - Mã phép (3) trong `packet_loop.py` không đổi: blob giống `da4e876` (log `l4-diff-da4e876` không có dòng `packet_loop.py`).
- Theo protocol §8.3, chuyển biểu hiện ra ngoài phạm vi **không** tính là vá. Lớp này nằm ở bảng (ii), và executor **không** ghi nó là đã vá. Phần chưa đo thuộc #1469.

### 7.3 Các lớp cũ

| slug | nguồn | trạng thái trên `c5d44c9` | phép đo | phần chưa đo |
|---|---|---|---|---|
| `con-tro-trong-backtick-bi-cong-khac-doc` | đặc tả r9 mục 19 (Q0) | Bản vá r9 giữ nguyên byte: protocol của H bằng nền cộng sáu khối (N2); 18 con trỏ `ca:` không backtick | `doc-claims-check --strict`: `"ok": true`, `flags: []`, mọi lớp 0, tập advisory trùng nền (mục 4) | CI thật (N13). Nhãn do reviewer đặt |
| `khoa-khong-neo-vi-tri-va-duy-nhat` | P1 của review đặc tả (họ lịch sử của 7.2) | Không đổi so với lượt 2: bảy khoá theo địa chỉ, duy nhất, đúng băm (N5 7/7); ba ca và ba đột biến "phần đầu tệp" còn đó (N6 (a), N7) | N7: `inv_bo_dem_truoc_tieu_de_dau` giết 2, `inv_truoc_tieu_de_chi_khoi_dau` giết 1, `inv_truoc_tieu_de_bo_bien_tieu_de` giết 1 | Phần bản sao không đứng thành đơn vị: xem 7.2 |
| `thieu-khoi-nang-tran-kich-thuoc` | P3 của review đặc tả lượt 10 (r10) | Đặc tả r11 thêm khối `nang_tran` ở mục 10, và lease g3 chép khối ấy. Phía executor chỉ có nghĩa vụ đo numstat | N12: +478 ≤ 500, 4 ≤ 6 tệp | Chưa có cổng máy đọc `nang_tran` (nợ `INV-28-TRAN-KICH-THUOC` trong ADR) |

- Không có `hint_provenance` khai riêng.
- Hướng của 7.1 trùng gợi ý F02 của reviewer: thêm ca cho ID hiện hành và biên, thêm đột biến chỉ nhận 99. Executor lượt 4 đã tự dẫn xuất lại và tự đo, gồm phép quét 41 biến thể độc lập với sổ, cùng 13 đột biến ngoài gợi ý. Lượt 4b không khẳng định thêm điều gì về ý định của lượt 4.
- Phía executor, không lớp nào lặp tới lần thứ ba trong lượt 4.

## 8. Những gì chưa đo, và sai lệch môi trường

- **Hai ca `CA_DAI`** (`wp1303_target_human_chain`, `wp1303_target_supported_pairs`): **KHÔNG ĐO ĐƯỢC** trên `c5d44c9`. Lượt 4 không chạy chúng, và lượt 4b không chạy vì hai lý do: chỉ thị chỉ giao đo phần còn thiếu của các ô đã khai, và `human_chain` ước ~85 phút. `wp1303_target_human_chain` chưa từng được executor đo trên H nào. Trên CI, hai ca chạy ở `packet-loop-dot-bien.yml`.
- **Bảng đột biến đầy đủ 2120**, tức lệnh nguyên văn `python .claude/dev/packet_loop_test.py` một tiến trình: KHÔNG chạy, như mọi lượt trước. Thuộc N14 (K7).
- **Các bước CI lượt 2 đã thử mà lượt 4 không chạy lại trên `c5d44c9`:**
  - `.claude/dev/ci_dang_ky_test.py --chay` (job `gate-registry`; lượt 2 cũng chưa có rc, xem HANDOFF-l3 mục 5)
  - `.claude/dev/idiom_py_test.py`
  - `.claude/dev/gate_lifecycle_test.py`
  - `ops/bien_nhan_v2_test.py`
  - `.claude/dev/chon_reviewer_test.py`
  - `.github/checks/ci_phamvi.py --kiem-bam` và `ci_phamvi_test.py`

  Cả sáu: **KHÔNG ĐO ĐƯỢC** ở lượt 4 và 4b. Ghi chú: giữa `d5d96e7` (nơi lượt 2 đo chúng đạt) và `c5d44c9`, `packet_loop.py` và protocol không đổi; chỉ `packet_loop_test.py` (+31) và ADR đổi. Base cũng đổi `695916e`→`6a4f52d`, nhưng chỉ ở `ops/**`. Đây là lọc theo tệp, không phải phép đo hành vi.
- Các bước CI chưa thử ở lượt nào: như HANDOFF-l2 mục 8.
- **Chạy chung clone `ve5/h`.** Trong lúc 16 mảnh chạy ở `ve5/h` (02:33Z–03:17Z), lượt 4 còn chạy trong chính clone ấy N4, N3, N8, so-dang-ky, tập bắt buộc, N7, N9, doc-claims và eol. Mảnh 0 (carrier) xong lúc 02:43Z và đạt `carrier=có`, rc 0. `git status --short --ignored` của `ve5/h` rỗng lúc 02:41Z (log `l4-ve5-h-status`), rỗng sau job gom, và rỗng sau phép quét của lượt 4b. Selftest chạy riêng ở `ve6/h`, nên lỗi carrier của lượt 2 không lặp lại.
- **`kho/` có ba thư mục `__pycache__` bị ignore** (`scripts/`, `scripts/_fallback/`, `scripts/tl_core/`), mtime 04:00:06–04:00:09Z. Đó là lúc hook phiên của lượt 4b chạy: dấu `session-start.ran` ghi 04:00:03Z, và hook có bước bootstrap cred `gws`/`nlm`. Thư mục `scripts/__pycache__` chứa đúng sáu tệp `gas`, `gws_bridge`, `gws_cred_store`, `mcp_bridge`, `tl_gws`, `transport`. Executor lượt 4b không tự chạy Python trong `kho/`; mọi lệnh Python của nó chạy ở `out/` hoặc `out/ve5/h`. Chúng không vào index; `git status --short` (không `--ignored`) của `kho/` rỗng.
- **Python**: máy đo chỉ có 3.13.18, còn `ci.yml` ghim 3.12. **Windows**: không đo (miễn theo C3).
- **Model và effort thật sự phục vụ**: lượt 4 có `modelUsage` `claude-fable-5-2` trong `run-l4.json`. Lượt 4b tự nhận `claude-opus-5-5`. Effort của cả hai: `KHONG_DO_DUOC` từ bên trong.
- **`SyntaxWarning: invalid escape sequence '\d'`** ở `packet_loop_test.py:3811` xuất hiện trong mọi log. Đó là dòng của nền, không thuộc diff.
- **Ngày và URL của comment duyệt băm r11** (`issuecomment-7206141143`, `created_at` `2026-11-27T00:04:02Z`): theo phép đo REST của phiên điều phối, ghi ở chỉ thị lượt 4. Executor không đo lại bằng REST.

## 9. Câu hỏi cho chủ kho

| # | mã E | câu hỏi | khuyến nghị |
|---|---|---|---|
| Q5 | E2 | Có cần một lượt đo bổ sung trước khi tiêu lời gọi Codex cuối cùng không? Lượt ấy sẽ chạy `ci_dang_ky_test --chay`, năm bước CI ở mục 8, và hai ca `CA_DAI` trên `c5d44c9`. Lease ghi trần lời gọi Codex còn 1 | Không chặn review. `packet_loop.py` và protocol không đổi kể từ lần các bước ấy đạt; hai ca `CA_DAI` chạy ở CI (`packet-loop-dot-bien.yml`), ngoài cổng bắt buộc. Nếu muốn chắc, chạy trước `ci_dang_ky_test --chay`: nó đọc sổ `CASES`/`MUTANTS`, mà sổ đã đổi |
| Q6 | E5 | Handoff này do Opus 5.5 viết trên log của Fable 5.2; mã của H do Fable 5.2 viết. Khi chủ kho audit `human_audited`, có cần ghi nhận gì riêng về việc tác giả handoff khác tác giả mã không? | Ghi nhận trong comment audit. Mọi số trong tệp này đều dẫn tới log có header `# rc:`, nên reviewer đọc lại được |

Không có câu hỏi mã E1, E3, E4.

## 10. Hiện vật ở `out/`

- **Lượt 4:**
  - `l4/COMMIT_MSG.txt` · `l4/wp1466-l4.patch` · `l4/thu-1.patch`, `l4/thu-2.patch` (bản thử, chỉ áp vào `l4/thu`)
  - `l4/spec-r11.md` · `khoi-r11/` (khối chép nguyên byte từ r11) · `l4/blob/nen/` (blob nền `6a4f52d`)
  - `l4/wp1466-r11-g3-c5d44c9.bundle` · `l4/run-l4.json`, `l4/run-l4.stderr`
  - `ve5/h`, `ve5/nen`, `ve6/h`, `ve6/nen` · `manh-h4/` · `log/l4-*.log`
  - script: `sc/l4_khoi.py`, `sc/sua_l4.py`, `sc/l4_quet_id.py`, cộng các script cũ
- **Lượt 4b:**
  - `HANDOFF-l4.md` (tệp này) · `l4/HANDOFF-l4.ban-som.md` (bản sớm)
  - `log/l4b-manh-gom.log` · `log/l4b-ruff-commit.log` · `log/l4b-n3-am.log` · `log/l4b-quet-id-h.log`
  - `tmp/l4b-*` (thư mục tạm)
  - Lượt 4b không thêm hay sửa script nào trong `sc/`.

HEAD=c5d44c93b4aa9326fa087af0bd07cbe918c2adc2 TEST=1861/1861 NUMSTAT=+478 -4 TRAN=dat DOC_CLAIMS=ok P3=dong
