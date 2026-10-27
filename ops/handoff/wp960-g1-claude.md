# Handoff wp960 g1 — executor `claude` (phiên cloud), 27-10-2026

- Packet #960 `NO-CAU-LICH-SU-BIEN-NHAN` r1 · lease `ops/leases/wp960-r1-g1-claude.yaml` @ `b1dfd02` · đặc tả
  `ops/specs/NO-CAU-LICH-SU-BIEN-NHAN.md` sha256 `69394c7658db28196b72e3a1b00f4f6931ad9aba8b9fdcf76563fab33edaa671` (đo lại: khớp).
- Phiên executor: `session_015GtxrbeTfDyFKdj7rb72Uq`.
- Nhánh code `agent/wp960-g1-claude`. PR #976 do chủ kho merge ở `20a2e2b` (2026-10-27T12:33:27Z), head lúc merge `71f8b59`.
- **Kết thúc ở trạng thái DỪNG theo `hinh_dang_ke_thua`.** Lượt review cuối là `changes_requested`. Chủ kho merge PR và đồng ý mở
  packet tiếp nối cho 7 finding còn mở. Điều kiện M-1 của lease (verdict approve trên head cuối) KHÔNG đạt.

## Lịch sử nhánh (PR #976)
| commit | nội dung |
|---|---|
| `7208fe0` | M1–M5: ba luật L-REVIEW · L-ANCESTRY · L-SURFACE, nợ `NO_CAU_LICH_SU` 66 mục, ca c69–c76, đột biến m73–m82 |
| `7ae7fc1` | merge `origin/master` `e139e55` (`thu-hoi` đòi master là tổ tiên) |
| `acedecb` | vá 4 P2 connector + 5 finding codex lượt 1; gỡ 2 nợ L-SURFACE trích dẫn (còn 64) |
| `33d331b` | ghim ngày commit trong fixture (`c74` chập chờn theo SHA ngẫu nhiên trên CI run 40479809106) |
| `916a60a` | khoá r1/r2/r3/r5 của reviewer (m90–m93); tách assertion A3 theo trường |
| `71f8b59` | merge master `09db703` (#980 gỡ đỏ L7 của master) |

## Đo trên `71f8b59` (clone thường, `core.abbrev 7`, không nông)
- `python ops/bien_nhan_v2_test.py`: **85/85 ca · 95/95 đột biến thường CÓ RĂNG · 2/2 TỰ KIỂM** · `TỔNG: ĐẠT`.
- `python ops/bien_nhan_v2.py --root .`: `TỔNG: ĐẠT` · nợ L-REVIEW 1 · L-ANCESTRY 60 · L-SURFACE 3 · L-SURFACE chua_do_duoc 0.
- Nợ rỗng ⇒ rc=1 với đúng `len(NO_CAU_LICH_SU)` dòng ba luật (ca `c76`).
- ruff F: delta 0 hai tệp · doctrine-scan sạch · `git diff --check` sạch · CI PR 24/24 xanh.
- Kích thước: +1037/−12 so master, **vượt** ngưỡng 1.000 dòng của ADR-0044 (packet không chạm authority). Phần tăng chủ yếu là ca
  test/đột biến reviewer đòi, cộng hai bản danh sách nợ.

## Review — 2/8 lời gọi codex CLI (trần ADR-0052)
| lượt | head | verdict | P0/P1/P2/P3 | biên nhận |
|---|---|---|---|---|
| connector | `7ae7fc1` | 4 P2 | — | trả lời 4 luồng trên PR #976, vá ở `acedecb` |
| 1 | `7ae7fc1` | `changes_requested` | 0/6/2/0 | `ops/reviews/wp960-review-1-codex-verdict.receipt.yaml` (PR #985) |
| 2 | `916a60a` | `changes_requested` | 0/6/1/0 | `ops/reviews/wp960-review-2-codex-verdict.receipt.yaml` (PR #985) |

Lượt 2 kết luận về finding cũ: 7 ĐÃ ĐÓNG · 4 ĐÓNG MỘT PHẦN · 1 CHƯA ĐÓNG (A3 `>-`).

## Vì sao DỪNG — ba hình dạng lặp ở ba lượt review
| hình dạng | connector `7ae7fc1` | codex lượt 1 | codex lượt 2 |
|---|---|---|---|
| lỗi ĐO thành sạch/vi phạm | run.json hỏng | surface hỏng, alias vòng | lịch sử hỏng, I/O khi băm, OID thiếu |
| bộ chọn ứng viên (regex) bỏ sót/bắt nhầm | OID toàn số, dòng trích dẫn | OID toàn chữ, khai báo thứ hai | tham chiếu miễn nhầm, ba nợ trích dẫn |
| nguồn gốc câu cho mốc `dung_tai` | blame cả scalar | đổi khoảng trắng | đổi tên tệp |

## Nợ chuyển sang packet tiếp nối (7 finding lượt 2, đều CÓ trên master)
1. `doi-ten-tep-tay-trang-cau-cu` P1 — đổi tên receipt ⇒ `git log -- <tên mới>` mất lịch sử ⇒ mốc muộn được nhận.
2. `lich-su-hong-bi-doc-thanh-khong-co-cau` P1 — YAML/`git show` lỗi ở phiên bản cũ bị bỏ qua; alias vòng trong lịch sử thoát
   `_AliasVong` ra ngoài `main`. `HINT.patch` lượt 2 có hunk tham khảo (dry-run sạch trên `916a60a`).
3. `oid-thieu-thuan-chu-so-bi-bo-qua` P1 — OID không tra được, thuần chữ/thuần số (kể cả 40 ký tự có nhãn Commit) ⇒ sạch.
4. `tham-chieu-truoc-khai-bao-mien-nham-surface` P1 — `_RE_TRICH_DAN` trước khai báo miễn luôn lời tự khai đứng sau.
5. `receipt-khong-doc-duoc-thoat-1` P1 — `_bam(p)` ngoài khối bắt lỗi ⇒ traceback rc=1 (có từ TRƯỚC packet). Hunk tham khảo trong
   `HINT.patch` lượt 2.
6. `a3-mutant-van-chet-boi-literal` P2 — khối `>-` do bộ phân tích YAML gấp trước khi cổng thấy; chưa có đột biến làm riêng nó xanh.
7. `ba-no-surface-con-lai-la-trich-dan` P1 — 3 mục nợ L-SURFACE (pr896-review-2/3/7) là lời trích, không phải tự khai. Thêm bằng
   chứng: hai verdict của CHÍNH packet này cũng bị L-SURFACE bắt nhầm (biên nhận phải mang caveat `VERDICT-KHAI-SAI-EXECUTION-SURFACE`
   ghi rõ là dương tính giả).

## Đề xuất cho packet tiếp nối (chủ kho đã đồng ý hướng; cần spec mới qua `soan-spec`)
- **Bỏ mốc `dung_tai`**: câu ứng viên có OID đã là tổ tiên ⇒ luôn vi phạm, sửa câu. Cả lớp nguồn gốc câu chết theo kiến trúc
  (finding 1, 2 phần lịch sử) cùng `_commit_them_cau`/`_co_cau`/`_moc_*`.
- **Mọi lỗi đo ⇒ KHÔNG ĐO ĐƯỢC** theo một biên duy nhất (finding 2 phần còn lại, 5).
- **OID không tra được ⇒ KHÔNG ĐO ĐƯỢC chỉ khi có ngữ cảnh rõ** (40 hex, hoặc đứng sau `commit`/trong backtick); còn lại bỏ qua (finding 3).
- **L-SURFACE chỉ đọc dòng tự khai ở phần đầu verdict** thay vì cả văn bản; sinh lại nợ (finding 4, 7). Phải giữ ca khai sai thật.
- A3 `>-`: đổi đặc tả nghiệm thu (chốt thuộc thư viện YAML, không thuộc cổng) hoặc chỉ ra chốt cụ thể để đột biến (finding 6).
- Write set dự kiến: `ops/bien_nhan_v2.py`, `ops/bien_nhan_v2_test.py`; sinh lại `NO_CAU_LICH_SU` cả hai bản; gỡ caveat dương tính giả
  khỏi `wp960-review-{1,2}` nếu L-SURFACE mới không còn bắt (biên nhận nằm ngoài write set ấy — cần khai thêm).

## Không làm
Không land, không deploy, không force-push nhánh của người khác, không xoá ref. `ops/land_evidence_nguon.py` và `ci.yml` không chạm.
