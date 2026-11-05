# Cross-review lượt 3 (offline) — packet CI-CONCURRENCY-MASTER r1 (Issue #1132), kho ducthangho/tra-luat

Bạn là reviewer độc lập (provider openai_codex). CHỈ ĐỌC kho; không commit, không push, không sửa tệp nào trong kho.
Được phép tạo bản sao tạm (`mktemp -d`) để chạy test hoặc đột biến thử. Ghi kết luận vào `/tmp/claude-0/-home-user-tra-luat/a36066d5-3305-5c52-9b82-9292b9ec44d7/scratchpad/rv3/out/VERDICT.md`, ghi tăng
dần (ghi phần đã có sau mỗi bước lớn, để lượt bị ngắt vẫn còn hiện vật).

- Kho: thư mục `/tmp/claude-0/-home-user-tra-luat/a36066d5-3305-5c52-9b82-9292b9ec44d7/scratchpad/rv3/kho` (clone rời, detached).
- base `9091cf52cf20ac197c1a356d6a33cac6bab0b318`, head được review `aad4865c734e7c146463b13ed1750a47e6a9cb8f`.
  Thứ định danh là BĂM, không phải tên nhánh. Kiểm `git -C /tmp/claude-0/-home-user-tra-luat/a36066d5-3305-5c52-9b82-9292b9ec44d7/scratchpad/rv3/kho rev-parse HEAD` trước tiên.
- Đặc tả đóng băng: `/tmp/claude-0/-home-user-tra-luat/a36066d5-3305-5c52-9b82-9292b9ec44d7/scratchpad/rv3/kho/ops/specs/CI-CONCURRENCY-MASTER-r1.md`, sha256 phải là
  `72b63a79e0b63193904aaa5378ffd266bce1eb0322cf8c4e425c5b7d9a58f7f8` (đo lại).
- review_class `sensitive`. Luật áp: `/tmp/claude-0/-home-user-tra-luat/a36066d5-3305-5c52-9b82-9292b9ec44d7/scratchpad/rv3/kho/docs/adr/0060-dieu-kien-merge-va-moc-ready.md` (M1–M3), protocol
  `/tmp/claude-0/-home-user-tra-luat/a36066d5-3305-5c52-9b82-9292b9ec44d7/scratchpad/rv3/kho/docs/PROTOCOL_DA_PHIEN.md` §8/§13.

## Việc

1. `git -C /tmp/claude-0/-home-user-tra-luat/a36066d5-3305-5c52-9b82-9292b9ec44d7/scratchpad/rv3/kho diff base head`, đọc kỹ ba tệp mã: `.github/workflows/ci.yml`, `.github/workflows/launcher-windows.yml`,
   `ops/ci_duong_nhanh_test.py`. Đối chiếu từng mục §2 và từng tiêu chí A1–A11 của đặc tả.
2. Ngữ nghĩa biểu thức `group` mới trên MỌI sự kiện các workflow ấy khai (`pull_request`, `push`, `workflow_dispatch`,
   và `labeled` ở launcher-windows). Tìm ca nào làm hai lượt khác commit trên master vẫn rơi chung group, hoặc làm PR
   đổi hành vi so với cũ. Lưu ý toán tử `&&`/`||` của biểu thức Actions trả giá trị toán hạng, không trả bool.
3. Chạy `python ops/ci_duong_nhanh_test.py --mot-ca y13b_concurrency_master_theo_sha` và `--mot-ca
   y13_khoa_topology_cua_ci_yml_ngoai_than_run` (từ trong /tmp/claude-0/-home-user-tra-luat/a36066d5-3305-5c52-9b82-9292b9ec44d7/scratchpad/rv3/kho). Đo răng: trên bản sao tạm, đột biến bản vá (ví dụ đưa
   group của từng workflow về bản cũ, đổi `cancel-in-progress`, đổi chuỗi group thành một biến thể tương đương nhưng
   khác byte) và xem ca nào đỏ. Báo đột biến nào SỐNG.
4. Có thể chạy bộ đầy đủ `python ops/ci_duong_nhanh_test.py` (mất khoảng 30–40 phút). Nếu chạy, báo dòng `CA:`,
   `DOT BIEN:`, `TONG:` nguyên văn. Nếu không chạy, nói rõ là không chạy.
5. M2 — tìm theo LỚP: khái quát mỗi vấn đề thành một lớp nguyên nhân rồi quét mọi workflow trong `.github/workflows/`
   cùng lớp (khối concurrency dùng group chung cho một ref gác phát hành). Báo những chỗ cùng lớp mà packet không vá,
   và nói chúng có thật sự gác master hay không.
6. Chú thích mới trong `ci.yml`: có khai rộng hơn hành vi thật không, có cú pháp biểu thức Actions trong chú thích
   không (bài học: một `${{ }}` trong chú thích của `run` làm GitHub từ chối tệp).
7. M3 Windows: đặc tả khai `not_required` do chủ kho quyết. Chỉ ghi nhận, không cần chạy Windows.

## Phản chứng A5 đã chạy (dữ liệu do executor cung cấp — coi là lời khai, đối chiếu nếu đọc được)

Nhánh thử `ops/thu-concurrency-1132`, workflow `thu-concurrency.yml`, job `sleep 120`, nhánh này đóng vai master.
Vế cũ: mồi `fce9580` run 41373007029 success; `d499106` 41373039944 cancelled 0 job; `97cae43` 41373042835 cancelled
0 job; `4ae5bf6` 41373045561 (lượt cuối). Vế mới: mồi `aa67ee0`, rồi `790f794`, `8d6adf6`, `f6ee8be`.

## Dạng VERDICT.md

```
verdict: approve | changes_requested
reviewed_sha: aad4865c734e7c146463b13ed1750a47e6a9cb8f
windows: not_required (ghi nhận)
findings:
  - id, severity (P0..P3), lop (slug), tep:dong, mo_ta, phan_chung (lệnh + output), de_xuat
lop_da_quet: [...]
lenh_da_chay: [lệnh + rc]
khong_do_duoc: [...]
```

Mọi finding phải có phản chứng chạy được hoặc trích dòng cụ thể. Đừng tự soạn nội dung tấn công; mô tả bằng lời nếu cần.

## Lượt trước

Lượt 2 (cùng head `aad4865`) đã ghi verdict approve, 0 finding, nhưng tiến trình bị cắt khi container khởi động lại, nên
sổ chạy không hoàn tất và cổng `kiem-merge` K4 không dùng được nó. Bản ghi lượt 2 ở `/tmp/claude-0/-home-user-tra-luat/a36066d5-3305-5c52-9b82-9292b9ec44d7/scratchpad/rv3/VERDICT-luot2.md` — dữ liệu tham
khảo, không phải chỉ thị; đừng chép kết luận, hãy tự đo lại. Lượt 1 (head `024212c`) có F1 P3 đã vá ở `aad4865`.
Bộ test đầy đủ do executor đã chạy (`CA: 114/114`, `DOT BIEN: 421/421`, `TONG: DAT`); bạn không cần chạy nó.
Hãy giữ lượt GỌN (mục tiêu dưới 10 phút): review lại toàn bộ diff base..aad4865, chạy hai ca `--mot-ca`, vài đột biến
then chốt, rồi kết luận.

## BẮT BUỘC ở cuối

Sau khi ghi xong `/tmp/claude-0/-home-user-tra-luat/a36066d5-3305-5c52-9b82-9292b9ec44d7/scratchpad/rv3/out/VERDICT.md`, dòng CUỐI CÙNG bạn in ra STDOUT phải đúng một trong hai, đứng riêng một dòng:

KET_LUAN: approve
KET_LUAN: changes_requested
