tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# CI-PACKET-LOOP-NHANH r2 — gate-packet-loop từ ~2 giờ xuống tối đa 5 phút

- packet_id: CI-PACKET-LOOP-NHANH; revision: 2;

| trường | giá trị |
|---|---|
| `packet_issue` | #1343 |
| `nguon_cap_viec` | Chủ kho (16-11-2026), trong phiên điều phối #1206 `session_015GtxrZk6gmfQKo7g4BfMBS`: "chỉ muốn chạy nó trong vòng dưới 5 phút"; trả lời AskUserQuestion "Làm cả 3". Chỉ đạo đứng #1206 issuecomment-6918292696: CI hậu merge không chạy test dài, không chạy CI Windows. |
| `review_class` | `sensitive` (sửa cổng CI bắt buộc) |
| `base` | nhánh mặc định lúc cấp lease (`9c1661f`) |

## 0. Vấn đề (đo 16-11-2026, log job `133226220846`, run `43845962754`, push master `9c1661f`)

- Bước `packet-loop selftest` (`python .claude/dev/packet_loop_test.py`) chạy từ 10:08:14Z tới 12:29:46Z, tức **2 giờ 21 phút**.
  - Bộ ca: 10:08 → 11:22, **74 phút**, in `nền: 1493/1493 đạt · BỎ QUA: 1`. Nhiều ca tự dựng bản sao đột biến (`mut_*`) bên trong.
  - Bảng đột biến (`AC 19` trở đi): 11:22 → 12:29, **67 phút**.
- Cùng 23 job, các job còn lại xong trong khoảng 20 phút. Cả lượt CI bị job này kéo dài.
- Ruleset master đòi các check `gate (ubuntu-latest)`, `gate-packet-loop (ubuntu-latest)`, `gate-ops (ubuntu-latest)`, `gate-cong-cu-gop (ubuntu-latest)`. Đổi tên hay xoá job `gate-packet-loop` sẽ làm mọi PR kẹt `blocked`.
- `packet_loop_test.py` không có cờ chọn ca: một tham số lạ như `--help` cũng chạy trọn bộ. Tệp này đang bị lease `wp1315-r5-g7-claude` (#1315) giữ, nên packet này **không sửa nó**.
- Đường nhanh có sẵn: `ops/ci_duong_nhanh.py` chọn `che_do=duong_nhanh` khi diff chỉ gồm `ops/{land,leases,reviews,specs}/**`; khi đó bước selftest đã bị bỏ qua.

## 1. `write_set`

```
.github/workflows/ci.yml
ops/ci_duong_nhanh.py
ops/ci_duong_nhanh_test.py
.claude/dev/packet_loop_test_manh.py
.claude/dev/ci_dang_ky_test.py
.github/workflows/packet-loop-dot-bien.yml
```

`packet_loop_test_manh.py` là tệp MỚI: bộ chạy bọc ngoài, import `packet_loop_test` rồi chọn ca theo mảnh và theo cờ. `ci_dang_ky_test.py` chỉ được sửa nếu chốt đăng ký job hoặc mảnh của nó đòi; không sửa thì thôi.

## 2. `ngoai_pham_vi`

- Không sửa `.claude/dev/packet_loop_test.py` hay `.claude/dev/packet_loop.py`.
- Không xoá ca nào, không đổi khẳng định nào của bộ ca.
- Không đổi ruleset của GitHub. Tên check bắt buộc `gate-packet-loop (ubuntu-latest)` giữ nguyên.
- Không chạm các job khác ngoài phần cần thiết để gom hoặc bỏ qua.

## 3. `muc_tieu`

| # | mục tiêu |
|---|---|
| M1 | **Chỉ chạy khi liên quan.** `ci_duong_nhanh.py` thêm một đầu ra riêng, ví dụ `packet_loop=chay\|bo_qua`. Giá trị là `chay` chỉ khi diff chạm tập phụ thuộc của bộ ca: tối thiểu `.claude/dev/packet_loop*.py`, `.claude/dev/packet_loop_test_manh.py`, `docs/PROTOCOL_DA_PHIEN.md`, `docs/adr/**`, `.claude/skills/**`, `AGENTS.md`, `CLAUDE.md`, `CONTEXT.md`, `.github/workflows/ci.yml`, cộng mọi tệp mà bộ ca đọc hoặc import. Executor phải ĐO tập này (import thật, `open`/`read_text` thật, tệp mà `ROOT`-relative path trỏ tới), ghi danh sách vào chú thích và vào test, không đoán. Không xác định được thì `chay` (fail-closed). |
| M2 | **Push lên master: bỏ qua** (chỉ đạo chủ kho). `workflow_dispatch` vẫn chạy được đủ. |
| M3 | **Tách bảng đột biến.** Cổng bắt buộc chỉ chạy bộ ca. Bảng đột biến chạy ở workflow RIÊNG `.github/workflows/packet-loop-dot-bien.yml` (`schedule` hằng đêm + `workflow_dispatch`, chỉ Ubuntu, không bắt buộc, có thể chia mảnh), cùng khuôn `ci-dot-bien-du.yml`. Không đặt `schedule` vào `ci.yml`. Bộ bọc bật hoặc tắt pha đột biến bằng cách đặt `MUTANTS` rỗng hoặc đầy đủ, không sửa tệp gốc. |
| M4 | **Chia mảnh.** Job ma trận `gate-packet-loop-manh` có N mảnh (N ≤ 16; chọn N sao cho mảnh chậm nhất ≤ 5 phút trên `ubuntu-latest`, đo thật). Mảnh i chạy các ca có chỉ số `k % N == i`, theo thứ tự đăng ký. Ca tốn thời gian dồn một chỗ thì cân bằng theo thời lượng đo được. |
| M5 | **Job gom giữ tên bắt buộc.** `gate-packet-loop` thành job gom (`needs:` mọi mảnh). Job gom ĐỎ khi: một mảnh đỏ; một mảnh bị bỏ qua hoặc huỷ trong lúc `packet_loop=chay`; hoặc **hợp các ca đã chạy khác tập ca đăng ký** (mỗi mảnh xuất danh sách tên ca đã chạy, gom so tập, thiếu hay trùng đều ĐỎ). Khi `packet_loop=bo_qua`, job gom xanh và in rõ lý do bỏ qua. |
| M6 | **Bộ bọc giữ chốt của `main()` gốc.** Chốt `WP1174_REQUIRED`/`missing` và carrier Linux không được thành ĐỎ giả chỉ vì ca nằm ở mảnh khác, cũng không được im lặng tắt. Kiểm `missing` trên tập toàn bộ, mỗi mảnh chỉ chấm phần của mình. Executor đọc `main()` và `_legacy_main()` của `packet_loop_test.py` rồi chứng minh bằng ca test. |

## 4. `nghiem_thu`

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| N1 | Test đơn vị của `ci_duong_nhanh` cho M1/M2: diff chỉ ở `scripts/**` ⇒ `bo_qua`; diff chạm từng phần tử của tập phụ thuộc ⇒ `chay`; push master ⇒ `bo_qua`; diff rỗng hoặc lỗi git ⇒ `chay`. | Đột biến: luôn trả `bo_qua` ⇒ ca đỏ. Bỏ một phần tử khỏi tập phụ thuộc ⇒ ca của phần tử đó đỏ. |
| N2 | Bộ bọc: hợp các mảnh với N bất kỳ ∈ {1, 4, 16} bằng đúng tập ca đăng ký, không trùng. N=1 với pha đột biến bật cho kết quả giống chạy tệp gốc (cùng số ca, cùng `TỔNG`). | Đột biến: lệch chỉ số mảnh (`k % N == i+1`) ⇒ ca so tập đỏ. |
| N3 | Job gom ĐỎ khi mảnh đỏ, mảnh thiếu, hoặc tập ca lệch: có ca test mô phỏng đầu vào của gom. | Đột biến: gom chỉ đọc `result` của needs mà không so tập ⇒ ca "tập thiếu" đỏ. |
| N4 | `actionlint` trên `ci.yml` rc 0 hoặc delta 0 so base. Các chốt sẵn có về workflow (`ops/lease_publish_test.py` t161/t162, `.claude/dev/ci_dang_ky_test.py`) xanh, chạy nhắm đích. | rc khác 0 hoặc delta > 0. |
| N5 | **Đo thật trên CI** của PR: mảnh chậm nhất ≤ 5 phút; `gate-packet-loop` xanh; hợp ca = 1493 + ca mới (nếu có). Ghi run id và thời lượng từng mảnh vào thân PR. | Mảnh > 5 phút, hoặc tập lệch. |
| N6 | `adr-song`, `doctrine-scan` rc 0. Ruff `--select F` delta 0 trên các tệp `.py` trong write set. | rc khác 0 hoặc delta > 0. |

Chỉ chạy test nhắm đích (chỉ đạo chủ kho). KHÔNG chạy trọn `packet_loop_test.py` trên máy executor trừ khi cần đo N2 với N=1; khi đó chạy một lần.

## 5. Kích thước và trần

Trần `ADR-0053`: ≤ 6 tệp, ≤ 450 dòng thêm (đo `git diff --numstat <base>...HEAD`). Lời gọi Codex theo `ADR-0055`. Windows: **không** (chỉ đạo chủ kho; packet chỉ đổi CI Linux).

## 6. `luat_dung`

- Vượt trần thì dừng, gửi numstat cho điều phối.
- Mảnh không xuống được 5 phút với N=16 thì dừng, báo thời lượng từng ca chậm nhất; không tự tăng N quá 16.
- Phát hiện cần sửa `packet_loop_test.py` thì dừng và báo; tệp đang bị lease khác giữ.

## 7. `pham_vi_e`

Chạm E4 (cổng CI bắt buộc): giảm thời gian, không giảm tập ca trên PR liên quan. Đổi chủ ý mức bảo đảm, do chủ kho duyệt: PR không chạm tập phụ thuộc thì không chạy bộ ca; push master không chạy; bảng đột biến không chặn merge.

## 8. `hinh_dang_ke_thua`

Cùng họ `gate-cong-cu` (chia mảnh + `gate-cong-cu-gop`) và `ci_duong_nhanh` (#674). Bài học CLAUDE.md "ca có MẶT khác ca có ĐO": job gom phải so TẬP ca, không chỉ đọc kết luận của mảnh.

## 9. `chua_do_duoc`

- `.claude/dev/chay-cong-windows_test.ps1` ghim dấu vân job `gate-packet-loop` (`5546b9244930`) và gương bước `gate*`. Đổi job sẽ làm t32 của tệp ấy ĐỎ trên Windows. Tệp nằm ngoài write set (trần 6 tệp) và không chạy trong CI; ghi nợ `GHIM-LAI-CHAY-CONG-WINDOWS-SAU-1343` cho packet sau.

- Thời lượng từng ca: chưa có (bộ ca không in thời lượng). Executor đo khi cân bằng mảnh.
- Tập tệp mà bộ ca đọc: chưa đo; M1 bắt executor đo.

## 10. Thay đổi so với r1

r1 sha256 `7e7c4a42fd1dcb156236a5a158b7c3526124bbb60b5dd1ad9945ace3f8b09653`. Executor g1 báo (preflight 16:46Z): Actions không có `if` mức workflow, nên đặt `schedule` vào `ci.yml` sẽ kéo cả 23 job mỗi đêm. r2 thêm MỘT tệp workflow mới vào write set cho M3 (6 tệp, đúng trần) và ghi nợ ps1. Không đổi gì khác.
