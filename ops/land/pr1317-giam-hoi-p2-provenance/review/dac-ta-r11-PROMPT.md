# Review đặc tả GIAM-HOI-P2-ADR-E1-E5 r11 (thay r10) — phiên mới, chỉ đọc

Bạn là reviewer đặc tả độc lập, phiên mới. **Chỉ đọc** với mọi kho git: không sửa, không commit, không đổi HEAD hay ref của
`D:/tlx/rv-p2/cay-kho` và `D:/tlbuild.git`. Được ghi trong thư mục hiện tại (`D:/tlx/rvs-r11`), nhất là `scratch/`. Sandbox
cấm ghi thư mục tên `.git`. Không dùng mạng, không đọc `~/.codex`. Ổ D: còn ít chỗ (dưới 600 MB): không tạo bản sao làm việc
đầy đủ của kho. Lượt này là review ĐẶC TẢ trước khi chủ kho duyệt băm, không phải review mã của PR thi công.

## Bối cảnh

- Đặc tả r10 (`SPEC-r10.md`, sha256 `1a5786cca5bcf8a72d8d93ecb9f8edbfbe021c5ef69b68f78ac642bc15698d1f`) đã được review 9 lượt
  và chủ kho duyệt băm. Ứng viên thi công dựng đúng byte từ r10 (H `093acd430da9328725e5a91d177e4b45338137cc`, tree
  `c51b7960ee1aa92d1b85ff6e63f4bef5f88f1f49`, base `c0b8e11d7099f756e65db8bd9a81493cde789a6f`) làm đỏ bước
  `python scripts/tl.py doc-claims-check --strict --json` của job `gate` trong `.github/workflows/ci.yml`: rc 2, một cờ L1 ở
  dòng 288 của ADR (`doc-claims-H-r10-toan-kho.json`).
- Chủ kho chọn sửa văn bản bằng đặc tả r11 (`SPEC-r11.md`, sha256
  `4d94f1fedd198547901cd310f04c83fa8984f310d9c3be72609e8c36d692a6e9`). Diff: `diff-spec-r10-r11.patch`. Mục 21 của r11 ghi
  lý do và phạm vi thay đổi.
- Hiện vật của phiên điều phối:
  - `D:/tlbuild.git` (kho bare, chỉ đọc): ref `p2-exp` = ứng viên dựng từ r10 (`d68a97a…`), `p2-exp-r11` = ứng viên dựng từ
    r11 (`f0374961b55fe9912f1fb1d9bf6bdd5bfbc6a5af`, HEAD trỏ vào đây), `ops/spec-giam-hoi-p2-r11` = commit đặc tả r11
    (`d26151370b9a86eb495457193e1a440e0bbeb764`, cha là base). Hai ứng viên dùng ngày Trạng thái `2026-11-14`; ứng viên r11 dùng
    URL giữ chỗ `…/issues/1292#issuecomment-1` vì comment duyệt băm r11 chưa có.
  - `ADR-0067-ung-vien-r10.md`, `ADR-0067-ung-vien-r11.md`: tệp ADR của hai ứng viên.
  - `doc-claims-ung-vien-r11-toan-kho.json`: `doc-claims-check --strict --json` toàn kho với ADR r11 thay vào cây làm việc đầy
    đủ (rc 0, `flags: []`).
  - `D:/tlx/rv-p2/cay-kho`: checkout thưa ở H (r10); không có phần lớn `ops/` và `references/` trong cây làm việc.

## Việc

1. **Diff đặc tả:** xác nhận r11 khác r10 đúng những chỗ mục 21 kê (định danh r10→r11, hàng `packet_id`, hàng `base`, một ô
   của khối `adr`, A9, mục 21) và không gì khác; đặc biệt các khối `cu`/`moi`/`thay` của mục 2 không đổi byte nào. Tìm mọi chỗ
   còn ghi r10 mà lẽ ra là r11 (và ngược lại: chỗ nhắc r10 có chủ đích là lịch sử).
2. **Tái lập lỗi và cách sửa:** trong `D:/tlx/rv-p2/cay-kho` chạy
   `python scripts/tl.py doc-claims-check --path docs/adr/0067-danh-sach-dong-va-uy-quyen-thuong-truc.md --strict --json`
   (kỳ vọng rc 2, một cờ) và `… --path D:/tlx/rvs-r11/ADR-0067-ung-vien-r11.md --strict --json` (kỳ vọng rc 0). Đọc
   `scripts/tl_core/workflow.py` (`_doc_claims_scan_one`, lớp L1) và xác nhận hay bác lời giải thích nguyên nhân ở mục 21.
   Xác nhận tệp adapter Codex `land-packets` có trên base (`git -C D:/tlx/rv-p2/cay-kho ls-tree c0b8e11 …`).
3. **Vị từ và định danh:** trích khối ```python mục 4 của `SPEC-r11.md` thành `scratch/kiem_p2.py`; chạy với cwd
   `D:/tlbuild.git` (HEAD = ứng viên r11): `python scratch/kiem_p2.py SPEC-r11.md c0b8e11d7099f756e65db8bd9a81493cde789a6f`
   (đường dẫn tuyệt đối khi cần) ⇒ kỳ vọng ĐẠT. Chạy cùng vị từ trên ứng viên r10 (ví dụ một `GIT_DIR`/worktree nhỏ trong
   `scratch/`, hoặc kho bare riêng `git clone --bare --shared D:/tlbuild.git scratch/q.git` rồi đổi HEAD trong bản sao ấy) ⇒ kỳ
   vọng ĐỎ. Gọi `_spec_merge` của `D:/tlx/rv-p2/cay-kho/.claude/dev/packet_loop.py` với lease giả (`packet_id`
   `GIAM-HOI-P2-ADR-E1-E5`, `revision` 11, `spec_path` `ops/specs/GIAM-HOI-P2-ADR-E1-E5-r11.md`, `spec_ref`
   `refs/heads/ops/spec-giam-hoi-p2-r11@d26151370b9a86eb495457193e1a440e0bbeb764`, `spec_hash` như trên), root `D:/tlbuild.git`,
   h = ứng viên r11 ⇒ kỳ vọng không lỗi; với `revision` 10 ⇒ kỳ vọng lỗi.
4. **Standards:** dòng A9 có đúng bước CI thật không (đọc `.github/workflows/ci.yml` ở cay-kho), đột biến của A9 có làm đỏ thật
   không; viết đường dẫn không dấu nháy ngược có làm sai nghĩa hay sai quy ước nào của kho không; mục 21 có lời khai nào rộng hơn
   phép đo không; còn chỗ nào khác trong khối `adr` (hay các khối `moi` vào `docs/`) có thể làm đỏ một bước CI khác không (quét
   cùng lớp: mọi đường dẫn có dấu chấm đầu trong span backtick của các tệp `docs/` mà ứng viên ghi).

Khái quát mỗi biểu hiện thành một lớp và quét mọi biểu hiện cùng lớp trước khi báo.

## Đầu ra

Ghi `VERDICT.md` (thư mục hiện tại), mở đầu:

```
verdict: approve | changes_requested | blocked
spec: GIAM-HOI-P2-ADR-E1-E5 r11
spec_sha256: <đo được>
```

rồi bảng lệnh đã chạy kèm rc và dòng kết luận, rồi finding `S11-01`… (mức P0–P3, slug lớp, vị trí, bằng chứng chạy được, hướng
sửa), rồi những gì không đo được. DÒNG CUỐI CÙNG của câu trả lời cuối của bạn (stdout) PHẢI đúng một trong:
`KET_LUAN: approve` · `KET_LUAN: changes_requested` · `KET_LUAN: blocked`. `changes_requested` chỉ khi có P0–P2 có bằng chứng
chạy được.
