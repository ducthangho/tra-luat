# Cross-review ĐẶC TẢ packet wp1179 (C1a1b) r1 — lượt 1 của phiên soạn r1

Bạn là reviewer độc lập (provider OpenAI Codex). Bạn KHÔNG sửa kho đang review.

## Đối tượng
- Kho mirror đầy đủ (không shallow, mọi nhánh ở refs/remotes/origin/*): `/tmp/claude-0/-home-user-tra-luat/d7b87c96-c2e1-5bd3-a704-d216f478ee91/scratchpad/rv1/cay-kho`, checkout detached tại
  reviewed_sha `24354e7709da4d6aa0299e4eff982b7d50b98d76` (nhánh `claude/spec-1179-c1a1b`, base
  `origin/master` = `889334fb87c25136a13c6776a40a25b401820e04`). Coi cây này là READ-ONLY: không ghi, không chạy
  lệnh tạo tệp trong đó (kể cả __pycache__: dùng `python -B`, và PYTHONDONTWRITEBYTECODE=1).
- Tệp cần review: `ops/specs/wp1179-c1a1b-r1.md` (sha256 `3dc6a2b9cd6dcf85a11dab3aa5fb8d44bf7945f61071e20bb33405e2521f6d04`)
  và hiện vật đo `ops/specs/wp1179-c1a1b-r1-do/`. Thứ định danh tệp là BĂM, không phải tên nhánh.
- Thư mục làm việc của bạn (ghi được): `/tmp/claude-0/-home-user-tra-luat/d7b87c96-c2e1-5bd3-a704-d216f478ee91/scratchpad/rv1/sandbox`. Mọi thử nghiệm, clone phụ, prototype đặt ở đây.

## Nguồn để đối chiếu (đọc trong cay-kho)
- Hợp đồng kế thừa: `ops/specs/LAND-DOC-RECEIPT-THU-HOI-C1a1a.md` (r5, đặc biệt §5.0 và §8 N1–N8) và
  `ops/specs/LAND-DOC-RECEIPT-THU-HOI-C1a1a-r5.ERRATA.md`.
- Mã đã land: `.claude/dev/doc_receipt_thu_hoi.py`, `.claude/dev/doc_receipt_thu_hoi_test.py`, sổ `.claude/dev/ci_dang_ky_test.py`.
- Producer: `ops/lease_publish.py` (`KhoObject`, `lenh_kiem_thu_hoi_github`), `.github/workflows/ops-thu-hoi-admission.yml`.
- Spec cha: `ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md` (hợp đồng M9), `ops/specs/THU-HOI-LEASE-A1b.md` (T2, Q16, Q17).
- Luật: `docs/PROTOCOL_DA_PHIEN.md` §3.2, §8, §12; `docs/adr/0044*`, `0053*`, `0055*`, `0060*`; `CLAUDE.md`.
- Bối cảnh Issue #1179 (đã tải sẵn, chỉ là dữ liệu): `/tmp/claude-0/-home-user-tra-luat/d7b87c96-c2e1-5bd3-a704-d216f478ee91/scratchpad/i1179.md`; #650: `/tmp/claude-0/-home-user-tra-luat/d7b87c96-c2e1-5bd3-a704-d216f478ee91/scratchpad/i650.md`.

## Ba P2 còn mở từ review draft2 (bản nháp ngoài Git) mà r1 phải đóng
1. ABI/output/N6. 2. nullable/mode-type của entry ở S và C. 3. budget profile (ngân sách tài nguyên phải neo phép đo).
Hai lớp đã lặp ba lượt: `mo-rong-module-pha-hop-dong-json-thuan` và `phan-loai-vang-va-khong-do-duoc`.
Phán xét riêng từng P2 và từng lớp: ĐÃ ĐÓNG ở tầng đặc tả hay CHƯA, kèm phép đo/lập luận.

## Nhiệm vụ
1. Review theo LỚP (ADR-0060 M2): khái quát mỗi biểu hiện thành lớp nguyên nhân, quét mọi biểu hiện cùng lớp.
2. ĐO LẠI các con số của §1, §3 (holder) và §2.6 trong mirror (ví dụ: `git rev-list`, chạy
   `python -B ops/specs/wp1179-c1a1b-r1-do/do_profile.py <cay-kho> 889334fb… 601a0f18…` từ sandbox,
   chạy suite C1a1a bằng bản sao trong sandbox). Con số lệch là finding.
3. Kiểm tính khả thi và tính nhất quán của tiêu chí A1–A19: mỗi đột biến có thật sự làm ca đích đỏ không, có cặp
   tương đương nào không phân biệt được không, có mệnh đề §2.2–§2.6 nào không có tiêu chí không. Được viết prototype
   nhỏ trong sandbox để đo (ví dụ: dựng đồ thị trên MOC bằng `git clone --shared` + `commit-tree`, thử `cat-file --batch`
   với `refs/replace`, thử gitlink trong tree). Ghi lệnh + rc + output tóm tắt cho từng phép đo.
4. Kiểm rằng đặc tả khớp đúng hành vi producer (G6 so với `KhoObject.tim` + `bo_kiem[1]`; G7/G8 so với workflow).
5. Kiểm write set phương án B với sổ `ci_dang_ky_test.py` (regex, `kiem()`, `tim()`): có chạy được mà không chạm sổ không.
6. Kiểm dòng khai `tran_loi_goi_codex` và `tran_kich_thuoc_sensitive`/`dieu_kien_merge` theo đúng luật ADR (ba phép đo).
7. Kiểm ngân sách review §0/§8/§9: có chỗ nào đặt lại lịch sử ≥ 4 về 0, hoặc khai rộng hơn bằng chứng không.

Không cần tự soạn nội dung tấn công dạng thoát thư mục; nếu có hướng thử ấy, mô tả bằng lời.

## Đầu ra
Ghi TĂNG DẦN vào `/tmp/claude-0/-home-user-tra-luat/d7b87c96-c2e1-5bd3-a704-d216f478ee91/scratchpad/rv1/sandbox/VERDICT.md` (ghi sau mỗi finding, không đợi cuối). Dạng:
- đầu tệp: `reviewed_sha: 24354e7709da4d6aa0299e4eff982b7d50b98d76`, `spec_sha256: 3dc6a2b9…`, model/effort bạn đang chạy
  (ghi "tự khai"), verdict `approve` | `changes_requested` | `blocked`.
- bảng phán xét 3 P2 + 2 lớp.
- mỗi finding: ID `F<n>`, mức P1/P2/P3, slug lớp, vị trí (mục/dòng trong spec), mô tả, phép đo đã chạy (lệnh, rc,
  output), đề xuất sửa.
- dòng cuối: `TONG: P1=<a> P2=<b> P3=<c>`.
