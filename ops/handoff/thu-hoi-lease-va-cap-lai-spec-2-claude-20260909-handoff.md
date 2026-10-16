# Bàn giao — soạn spec `THU-HOI-LEASE-VA-CAP-LAI` (PR #475), phiên 2 → phiên thi công A0 (khi có lease), 09-09-2026

**Vai phiên 2:** điều phối cross-review + vá spec (KHÔNG executor). Kết thúc theo lệnh chủ kho `5578460203`
("review tới hết P1" ⇒ Packet Issue ⇒ DỪNG xin lease). **Phiên 2 không thi công** (ADR-0046: cắt ở biên packet).

## 1. Neo — đo 09:5xZ 09-09-2026

```yaml
nhanh: claude/spec-thu-hoi-lease-va-cap-lai-20260907
head: 5ff6cd5a66fc5929b0c37a9f245d896b7dd0e7c2      # r9 đóng băng; commit bàn giao này nằm NGAY SAU
base_nhanh: b416830ef2a509d60203d55552ce17950afcf67c
origin_master_luc_do: 585c7d510e026b4ea5a2b395c69581f24c1d8fa0   # 48 commit sau base; nhánh spec KHÔNG merge master
pr: 475                                             # draft; cong ĐỎ theo thiết kế (comment 5571673973)
packet_issue_A0: 488                                # proposed, CHƯA lease
spec: ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md
spec_revision: 9
spec_hash: 465538364b1a3f9477782fba79869bbd1c9351140e3fa9df50451baae22f9c79
spec_r9_da_review: true                             # lượt 8 (lời gọi 9, VERDICT 85d10868…) đọc r9 + ADR: 0 P1; S11/P2 chỉ ở Issue #488
adr: docs/adr/0047-nguon-tin-cay-cho-cong-doc-lease.md   # Proposed, sha256 b9975929… (đồng bộ S10)
loi_goi_review_da_dung: 9                           # 1,2,3,4a(chết),4b,5,6(=7),7(=8),8(=9); 7a chết preflight KHÔNG tính
comment_neo: [5571673973, 5575587924, 5576397733, 5578460203, 5598741255, 5600001299]
hien_vat: ops/reviews/thu-hoi-lease-va-cap-lai-spec/   # luot1..7 VERDICT/HINT/PROMPT/EVIDENCE, spec-r1..r8, 4a/7a chết, README
```

## 2. Kết quả vòng review (phiên 2)

| lượt | lời gọi | bản | VERDICT | P1 còn |
|---|---|---|---|---|
| 6 | 7 | r6 `f78135cf…` | `9090aadd…` (2889 s) | 3 (S1, S3, S7 mới) + 3 P2 (S5, S6, S8 mới) |
| 7a | — | r8 | chết preflight `refresh_token_invalidated` | không tính |
| 7 | 8 | r8 `48ea894a…` | `f28b7d0c…` (1377 s) | **0**; 2 P2 (S8 một phần, S10 mới) ⇒ vá r9 |
| 8 | 9 | r9 `46553836…` + ADR | `85d10868…` (1431 s) | **0**; S8/S10 ĐÓNG; S11/P2 = hồ sơ Issue #488 (đã sửa: `wp488`, `land_obligations` đề xuất) |

Chi tiết từng ô: spec §0.4 (r6→r8) và §0.5 (r8→r9).

## 3. Còn của CHỦ KHO (không phải finding — reviewer lượt 7 xác nhận)

1. **Lease cho #488** (`--granted-by` chủ kho; phiên agent KHÔNG tự cấp); xác nhận `mission_issue: null` (standalone) và ghim `land_obligations` (S11).
2. **Nền thực thi được tin** (runner/image) + **người duyệt** mỏ neo `PROFILE_ADAPTER_DA_DUYET` ⇒ ghi ADR-0047 lớp 2.
3. Q7 (ngoại lệ dòng ADR-0044 cho A0 — ước 560–780 là TRƯỚC vá lượt 6, executor đo numstat trước ready), Q8 (lệnh
   thu hồi r2 trên #461), Q9 (nhận bản ghi cho lease hết hạn), Q10 facts (chỉ A1).
4. `body_sha256` của comment `5575587924` (descriptor Q13) — readback rồi ghim vào mã A1, không bịa.
5. Dependency `LAND-DOC-RECEIPT-THU-HOI` (consumer receipt trong `land-packets`) — chưa có Issue; phải land TRƯỚC
   cửa sổ bootstrap A0 (spec M9/Q7).

## 4. Việc của phiên thi công A0 (chỉ sau khi có lease)

0. Mở phiên: `sed -n '1,140p' .claude/dev/launcher.py` → `doctor` → `chuan-bi`. **`CODEX_AUTH_JSON` mới chỉ tới container
   MỚI**; trong phiên đang chạy chỉ còn `codex login --device-auth` (chủ kho nhập mã, ~15 phút). Ảnh chụp >36 h coi như chết.
1. `git fetch --unshallow` nếu shallow; **so tập tên** `ls-remote` vs `for-each-ref` (CLAUDE.md); `ai-dang-giu` cho cả
   ba đường write set A0 — phải NGƯỜI_GIỮ 0 hoặc đúng lease của mình.
2. Đọc spec r9 §write_set/A0, M1–M4/M6/M9, A2/A6/A7/A8/A11/A12, ADR-0047; `spec_hash` trong lease phải = `46553836…`.
3. Ca âm S1/S2/A6 (env bẩn, executable giả, bytes lệch OID) do **điều phối dựng** — reviewer bị cấm tự soạn (lượt 4a chết).
4. Cross-review: khuôn `luot7-PROMPT.md`; GIỮ đoạn "Phân công như lượt 4b — CẤM tuyệt đối tự soạn …"; codex
   `gpt-6-astra` xhigh; chạy `setsid nohup … < /dev/null &`; đợi `run.json` `trang_thai == "xong"`; băm lại VERDICT sau run.

## 5. Bẫy đã trả giá trong phiên 2

- **CI đỏ do ratchet `r291_docs_ngoai_goi`** khi thêm ADR (docs/**/*.md 71→72): ba cổng `adr-song`/`doctrine-scan`/
  `doc-claims-check` xanh KHÔNG bắt được; chỉ `tl selftest` đỏ. Thêm tệp `docs/` ⇒ chạy selftest TRƯỚC khi đẩy; sửa
  `scripts/tl_selftest.py` ⇒ tái sinh `RELEASE_MANIFEST.json` (file_count không đổi 180).
- **Mirror `git clone --mirror` + clone lại chỉ cho 42 ref** (heads cục bộ + tag); phải fetch thêm
  `+refs/remotes/origin/*:refs/remotes/origin/*` vào cay-kho ⇒ 310 ref theo công thức spec.
- **`pgrep -af`/`ps -eo args` in NGUYÊN prompt** (đối số codex) — đừng dùng trong phiên; và `pkill -f 'codex login'`
  giết cả shell chứa chuỗi ấy (exit 144).
- **HINT của reviewer áp lên bản đã sửa §0 sẽ gãy hunk** (2/7 ở lượt 6) — áp lên bản r-được-review rồi vá tay.
- **`ai-dang-giu` rc=12 "cache thiếu nhánh máy chủ"** khi có nhánh mới (#482/#483 cấp 03:32Z 08-09) — đó là fail-close
  đúng; fetch rồi đo lại, đừng đọc thành lỗi.
- API check-runs qua MCP trả 403 (PAT) — kết quả `gate` phải đọc trên GitHub UI hoặc chờ sự kiện PR.
