# Handoff wp923 g1 — dư âm trần 150, pha A (executor `wp923-r1-g1-claude`)

Packet #923 · spec `ops/specs/wp923.md` sha256 `65db5e381ce9c7539f5bf9fb3b7d116ba3822a4914f3725e7a9ba98a484e4513`
(`ops/wp923-spec@480341d`, băm lại trong phiên: khớp) · lease `ops/wp923-r1-g1-lease@76ccfe9`, đã đăng
issuecomment-6393189637. Nhánh `agent/wp923-g1-claude`, base `1a269f5`, head `7574c39` — PR #924 (DRAFT).
KHÔNG merge/land/deploy — việc của chủ kho. Không bump VERSION, không tái sinh manifest (`.claude/` `.github/` ngoài manifest).

## Đã làm (diff PR: 2 tệp, +8/−5)
| tệp | việc |
|---|---|
| `.claude/dev/chay-cong-windows.ps1` | `[int]$HanGiay = 6300` → `9000`; chú thích `.PARAMETER HanGiay` liền kề (câu nêu 6300) nối mốc mới, giữ chuỗi lịch sử 6300/5400/3600/900. `ValidateRange(1, 86400)` giữ nguyên. |
| `.github/workflows/ci.yml` | CHỈ chú thích: `:734` (`gate-ops` "trần 25 phút của job" → "trần job lúc đo (25 phút; #910 pha A, PR #913: `gate-ops` 60 → 150)"); `:953` giữ nguyên câu #705, nối dòng `#910 pha B (PR #917, a7da463): 105 → 150`; `:954` (câu không mốc "Timeout KHÁC `gate`/`gate-packet-loop` (vẫn 60)") viết lại thành câu có mốc: trước #910 khác có chủ đích (`gate` 60, `gate-packet-loop` 120), #910 (PR #913 + #917) đưa cả ba lên 150. |

Nguồn lịch sử đã đo: `git log -G'timeout-minutes: 150'` ⇒ `3818bd4` (#849 `gate-cong-cu` 45→150), `6e09f4b` (#910 pha A,
merge PR #913: `gate` 60→150, `gate-ops` 60→150, `gate-packet-loop` 120→150), `a7da463` (#910 pha B, merge PR #917:
`gate-nhanh-manh` 30→150, `gate-registry` 105→150).

## Quét chú thích `ci.yml` — câu khẳng định `timeout-minutes` cấp job
Quét `grep -n -iE 'timeout|trần [0-9]|[0-9]+ ?phút|\b(25|30|60|90|105|120|150)\b'` trên các dòng bắt đầu bằng `#`, rồi đọc
từng khối quanh mọi `timeout-minutes:` cấp job. Giá trị trên base: `chuan-bi` 20 · `gate` `gate-cong-cu` `gate-ops`
`gate-nhanh-manh` `gate-registry` `gate-packet-loop` 150 · `gate-cong-cu-gop` `gate-nhanh-gop` 10.

| dòng (base) | job | câu | phân loại | việc |
|---|---|---|---|---|
| 111–117, 120–124 | `gate` | khối r391 (25→45, số đo 29-08-2026) | lịch sử có mốc | giữ |
| 118–119 | `gate` | "Nâng tiếp 45 -> 60 … Trần 60 là chỗ trống cho lần ĐO SAU" | lịch sử (khối r391; `7657bfd` thêm câu cùng lúc đổi YAML 45→60) | giữ — Codex đồng ý |
| 535–536 | `gate-cong-cu` | "WP748 r20 (PR #849): 45 -> 150" | lịch sử có mốc, khớp hiện tại | giữ |
| 640 | `gate-ops` | "Ma trận/`timeout`/`env` bằng đúng `gate`" | hiện tại, ĐÚNG (cả hai 150) | giữ |
| 734 | `gate-ops` | "không đáng kể so với trần 25 phút của job" | hiện tại, SAI | **sửa** |
| 945–946 | `gate-registry` | "Cùng ma trận/`timeout-minutes`/… với `gate`" | hiện tại, ĐÚNG (cả hai 150; sai trong khoảng #593→#910) | giữ |
| 949–952 | `gate-registry` | #593 60→90, #705 90→105 | lịch sử có mốc | giữ |
| 953 | `gate-registry` | "105 vẫn cỡ theo UBUNTU, KHÔNG bảo đảm Windows" | thuộc câu #705 | giữ, **nối** mốc #910 pha B |
| 954 | `gate-registry` | "Timeout KHÁC `gate`/`gate-packet-loop` (vẫn 60)" | hiện tại, SAI (và đã sai trước #910: `gate-packet-loop` 120) | **sửa** |
| 1028–1029 | `gate-packet-loop` | "WP856 (PR #866): 60 -> 120" | lịch sử có mốc; job nay 150, không có câu mốc #910 riêng | giữ — Codex đồng ý; ai muốn thêm mốc thì là việc chú thích của packet sau |
| 76 | `chuan-bi` (bước) | `timeout-minutes` riêng của BƯỚC | không phải trần job | giữ |

`gate-nhanh-manh` (150) và hai job gom (10) không có chú thích nêu trần.

## Tiêu chí hoàn tất
- **N1 ĐẠT.** `yaml.safe_load(git show 1a269f5:.github/workflows/ci.yml) == yaml.safe_load(head)` ⇒ `True`.
  `bam_gate_nhanh`/`bam_gate_registry` nạp từ chính `.claude/dev/ci_dang_ky_test.py` trên head ⇒ khớp `BAM_GATE_NHANH`
  và `BAM_GATE_REGISTRY` (`True True`).
- **N2 ĐẠT.** `git diff -U0 1a269f5 -- .github/workflows/ci.yml`: 5 dòng (2 `-`, 3 `+`), cả 5 sau `lstrip` bắt đầu `#`.
- **N3 ĐẠT.** `actionlint` 1.7.7: base rc=0, head rc=0. `shellcheck` **VẮNG** ⇒ actionlint bỏ luật shellcheck ở cả hai vế
  (CLAUDE.md: thiếu shellcheck thì phép đo yếu hơn; delta vẫn 0).
- **N4 ĐẠT** — PowerShell **7.4.6** thật (tải `powershell-7.4.6-linux-x64.tar.gz` vào scratch), ba clone sạch dựng trong
  MỘT lệnh (`git clone` + `checkout` + `core.abbrev 7`), chạy `pwsh -NoProfile -File .claude/dev/chay-cong-windows_test.ps1`:

  | vế | mặc định | dòng tổng | ca ĐỎ |
  |---|---:|---|---|
  | base `1a269f5` | 6300 | `chay-cong-windows: 33/36 dat` (rc=1) | t9, t30, t32 |
  | head `7574c39` | 9000 | `chay-cong-windows: 34/36 dat` (rc=1) | t30, t32 |
  | đột biến 8999 (trên clone head) | 8999 | `chay-cong-windows: 33/36 dat` (rc=1) | t9, t30, t32 |

  t9 base: `HanGiay mac dinh 6300 s < 9000 s cua job CI`; đột biến: `8999 s < 9000 s` ⇒ ĐỎ đúng. Delta head−base = chỉ t9.
  Codex đo độc lập (ba clone riêng, TMPDIR riêng) ra cùng delta, nhưng dòng tổng 32/33/32 vì **t15 ra `KHONG DO DUOC`**
  (*"khong dung duoc tep khong xoa duoc tren nen nay"*) ở cả ba vế của lượt Codex, còn lượt phiên này t15 ĐẠT ở cả ba.
  Không ảnh hưởng delta; ghi để người sau khỏi đọc 32/36 với 33/36 thành hồi quy — t15 phụ thuộc môi trường chạy.
- **N5 ĐẠT** — xem mục cuối.
- **N6 ĐẠT.** `python3 -B .claude/dev/ci_dang_ky_test.py` (không `--chay`, không sửa) trên head: rc=0, `PHẢN CHỨNG:
  1070/1070 đỏ đúng`, `TỔNG: ĐẠT`.

## Review
Codex lời gọi **1/2** (trần spec Q1 + lease `budget.codex_review_calls.pr_wp923_g1.limit: 2`) qua `launcher.py run`,
`gpt-6.1-sol` effort `xhigh` (header CLI + `model_phuc_vu` toàn `gpt-6.1-sol`, `DO_DUOC`), run `fd021cb7`, 532,9 s, `ma_thoat 0`.
Verdict **approve**, `reviewed_sha 7574c39d98459c9caf1365a7dd092747335ae4e8`, không P0–P3:
`ops/reviews/wp923-g1-claude-review-1-codex-verdict.md` (sha256 `b2b3bbcf…093e91`), prompt
`…-prompt.md` (sha256 `0db9f753…152239` = `prompt_sha256` của run), receipt `…-run.json`.
Connector `chatgpt-codex-connector[bot]` (PR chuyển ready bởi chủ kho 05:03Z) review `7574c39`: `completed`,
`has_any_findings: false` (comment 6393722670) — không thread nào cần trả lời.
Một lượt phóng TRƯỚC đó bị launcher chặn `CHAN [11]` (clone review có `origin` là đường dẫn cục bộ) TRƯỚC khi codex
được gọi ⇒ không tính lời gọi.

## Lỗi khác lộ ra (Q5 — ghi, KHÔNG vá)
- **t30** (`chay-cong-windows_test.ps1`) ĐỎ sẵn trên base: khoá `env` của job `gate*` không có trong script —
  `CI_DANG_KY_GOP_KQ`, `CONG_CU_TEST_GOP_CHE_DO`, `NHANH_DON_DUOC_DICH`, `NHANH_DON_DUOC_DICH_DU`, `NHANH_DON_DUOC_DICH_RA`.
- **t32** ĐỎ sẵn trên base: gương `chay-cong-windows.ps1` lệch `ci.yml` — bước `chạy mảnh nhanh_don_duoc`/`gộp mảnh
  nhanh_don_duoc` chưa có gương; dấu vân job đổi/chưa ghim: `gate-cong-cu` 527d4291b599→3d82f41a1eb5, `gate-cong-cu-gop`
  4f1198c4ace4→ade3f0565731, `gate-nhanh-gop` mới (aabc4334c5fa), `gate-nhanh-manh` mới (50de26459f1c), `gate-registry`
  b836a4f366e1→2292303e2a91. Dấu vân giống hệt ở base và head ⇒ thay đổi chú thích của packet này không chạm dấu vân.
  Hai ca này nghĩa là gương Windows đã trôi khỏi `ci.yml` nhiều packet; cần một packet riêng.
- **t15** phụ thuộc môi trường (xem N4).
- `git rev-parse --is-shallow-repository` = `true` lúc mở phiên; đã `fetch --unshallow` trước mọi phép so lịch sử.
- Pha B (chú thích `.claude/dev/ci_dang_ky_test.py:755`/`:804`) KHÔNG làm — tệp do `wp899-r4-g3-claude` giữ.

## N5 — CI lượt PR — ĐẠT (đo 25-10-2026 05:34Z, check run trên `7574c39`, không `get_status`)
Workflow `gate` run `40163483016`, `head_sha 7574c39`, `completed/success` (04:52:42Z → 05:33:54Z). Check run trên head:
26 — 25 `success`, 1 `skipped` (`launcher` của `launcher-windows.yml`, có `paths:`, không đụng). PR #924
`mergeable_state: clean`. Nền đo: chỉ `ubuntu-latest` (nhãn job) — KHÔNG có lượt Windows; t9 là ca PowerShell nên
bằng chứng PowerShell của packet là N4 (pwsh 7.4.6 trên Linux), không phải CI.
Master tiến lên `0dbb4c2` (#922, chỉ thêm 10 tệp `ops/land/`, merge thử sạch) trong lúc chạy; KHÔNG merge vào nhánh
vì không đụng write set và sẽ làm mất neo verdict `7574c39`.
