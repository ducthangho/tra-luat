# Handoff wp858 — executor claude, lease `wp858-r1-g2-claude` (kế thừa g1)

```yaml
schema_version: 1
packet_id: wp858
generation: 2
spec_hash: 5a61e959281f852592b2a5420b4618718d2364db8fa6320934d2651bbb7d4c54
provider: claude
model_family: claude
execution_surface: claude_code
transport: machine/local
role: executor
session_id: session_012ZJ73eyfSWoNKcmQWQpoiQ
base_sha: 3a3a3caca5de4934ff53851feb6994c2c7b84ad5     # merge master (Q7): merge-base 637f78029f5a5fe56d35199dd0f75c50274f2c0f
head_sha: 521efebab226fe3a92b2ccce4a59c27dd638edff     # PR #864
status: blocked
summary: >-
  L1: 12 cong thuc git/python/shellcheck/bash goi chon_thu_muc_chay_duoc (ops/cai_cong_cu.sh) — ung vien Q2 dau tien ma
  cong_cu.py kiem-tra --chi DAT; ten tran DAT => khong doi PATH, in /dev/null tren dong rieng; moi buoc hong return 1.
  L2: goc DO DUOC — codex-linux-sandbox gan tmpfs ro len /tmp/.git => _KhoCodex tu choi moi home duoi /tmp; t86 chon goc
  tam khong .git o to tien. L3: mkdtemp rieng. Ratchet goi 189->190, manifest. Codex 5/5 da dung; luot 5 changes_requested
  vi F858-08 (P2 do phu vong duyet ung vien, KHONG loi runtime) — chua co quyet dinh chu kho; tran diff 450/450.
changed_paths: [ops/cong_cu.yaml, ops/cai_cong_cu.sh, .claude/dev/launcher_test.py, scripts/tl_selftest.py,
                RELEASE_MANIFEST.json, changelog.d/wp-858.md]
tests:   # tren 521efeb; hai ve nen 637f780 / head dung trong MOT lenh, /tmp/.git VANG
  - {name: launcher_test, status: passed, evidence: "nen 234/234, head 242/242 (co va khong CODEX_AUTH_JSON gia)"}
  - {name: launcher_test --dot-bien, status: passed, evidence: "Linux 296/296 (4 khong do duoc); Windows 216/216 (84 khong do duoc, 72% >= san 70%)"}
  - {name: tl.py --selftest, status: passed, evidence: "1731/1731"}
  - {name: release-verify --strict, status: passed, evidence: "ok=true, expected=checked=190"}
  - {name: cong_cu_test (CONG_CU_TEST_BAN_KINH=manh), status: passed, evidence: "61 ca, loi dot bien 0, cong cay that DAT"}
  - {name: ruff F delta, status: passed, evidence: "4409 = 4409 so nen"}
  - {name: doctrine-scan / doc-claims-check --strict / actionlint / bash -n, status: passed, evidence: "sach / ok:true / rc 0 / ok"}
  - {name: ci.yml, status: passed, evidence: "gate 39730024192 success tren 521efeb"}
  - {name: launcher-windows.yml (workflow_dispatch), status: passed, evidence: "39732838734 success tren 521efeb; 204/204 qua, 40 BO QUA (5 r858_* hanh vi: shell POSIX), dot-bien 216/216"}
  - {name: N5 t86 song song, status: passed, evidence: "khi /tmp/.git CO MAT: nen 637f780 t86 0/3; head 2 tien trinh x10 = 10/10 + 10/10"}
  - {name: Codex cross-review, status: failed, evidence: "luot 5/5 (0265f964) changes_requested: F858-08 P2 moi; F858-03 mo co quyet dinh chu kho"}
test_selection:
  gate_tier: T3
  selector_policy_sha: null
  tested_sha: 521efebab226fe3a92b2ccce4a59c27dd638edff
  selected_groups: [launcher_test, dot-bien, selftest, release-verify, cong_cu_test, ruff, doctrine-scan, doc-claims, actionlint]
  full_fallback_reason: "sensitive; chay du bo cong cua spec muc Cong"
remaining_work:
  - "F858-08 (P2, Codex luot 5): vong duyet ung vien khong co ca khoa — dot bien 'chi duyet hai ung vien dau' va 'bo break' song. Va: ca Windows chi ung vien thu ba (Git/usr/bin) tot => DAT dung thu muc; ca hai ung vien cung tot => chon ung vien DAU. Can >0 dong them (vuot tran 450) va >=1 luot Codex (ngan sach 5/5 het)."
next_role: human
manual_next_action: "Chu kho quyet F858-08 tren #858: (A) nhan no co ten 'vong-duyet-ung-vien-chua-khoa' => du M-1..M-5; hoac (B) nang_tran + them ngan sach Codex de va."
copyable_prompt: null
failure: {fingerprint: null, category: content}
successors: []
```

## Bảng ba mốc (§3.2.1)
| Mốc | SHA |
|---|---|
| base lúc cấp lease g1 | `3a3a3caca5de4934ff53851feb6994c2c7b84ad5` |
| merge-base sau merge master (Q7) | `637f78029f5a5fe56d35199dd0f75c50274f2c0f` |
| head cuối đề nghị review | `521efebab226fe3a92b2ccce4a59c27dd638edff` |

## Review — 5 lượt Codex (`gpt-6.1-sol`, `xhigh`, qua `.claude/dev/launcher.py run`)
| Lượt | Head | Run | Verdict | sha256 tệp verdict |
|---|---|---|---|---|
| 1 | `bfbd273` | `b2296219` | changes_requested (F858-01/02/03) | `7446cb63…a88` |
| 2 | `97544b5` | `0ecfade9` | changes_requested (03 mở lại, 04, 05) | `af2b6196…b01` |
| 3 | `8733f0a` | `63192262` | changes_requested (03 mở lại, 06) | `79c5f24d…1ad` |
| 4 | `93fd69f` | `b31b149a` | changes_requested (03 writer muộn, 07) | `9990e3ae…bc9` |
| 5 | `521efeb` | `0265f964` | changes_requested (08 mới; 03 mở có quyết định) | `44bc30cc…187` |

Tệp: `ops/reviews/wp858-g1-luot{1..5}-codex-verdict.md` trên nhánh này.

## Nợ có tên
- `python-probe-khong-theo-PATH` — chủ kho chọn (a), #858 issuecomment-6312034981.
- `cai-stdout-writer-muon` — F858-03 đường writer muộn; chủ kho chọn A, #858 issuecomment-6333879879.
- `rg-installer-stdout-khong-LF` — công thức `rg` (bộ chọn riêng, Q1) nối dòng khi trình cài không kết thúc bằng LF;
  Codex lượt 4 đồng ý ngoài phạm vi Q1/Q8. Packet tách kênh chỉ mở khi chủ kho yêu cầu.
- `r484_*` đỏ khi có Codex chạy song song (cùng cơ chế `/tmp/.git` của L2) — packet khác (Q8), không vá.
- Thứ tự commit: manifest là commit cuối của head `521efeb`; `release-verify --strict` 190/190.

## Bài học đo được (đề nghị ghi CLAUDE.md qua packet có quyền)
- **Sandbox Codex Linux tạo `/tmp/.git` trên máy chủ trong lúc chạy** (bwrap mount point; `/proc/<pid>/mountinfo`:
  `/tmp/.git ro … tmpfs`; biến mất khi phiên kết thúc). Mọi phép đo có kiểm "tổ tiên có `.git`" chạy song song với một
  lượt Codex sẽ đỏ giả — đó là gốc thật của "`t86` đỏ khi chạy song song" ở #831.
- **Một kênh mang hai loại dữ liệu là lỗi thiết kế** (bài học "BẢY phát hiện cùng MỘT đường"): F858-03 mở lại 4 lần, mỗi
  bản vá đúng nhưng hẹp, vì kết quả hàm và log trình cài chung stdout. Đếm hình dạng lỗi sớm hơn thì đã hỏi chủ kho từ lượt 2.
