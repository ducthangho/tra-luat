Review mã wp1236 đợt B, lượt **2/4**: **changes_requested — B01, một lớp P2; VA_MOT_PHAN**.

HEAD `58bfa5f0bd5bf69b2003ac2524ea455447711bab`, tree `f25b7ca1b85eeaf842b64fc1aa62d2ab7229c62e`; base `f602325574c62184caf16309631f5f680ca5cee2`. Đặc tả r12 SHA-256 `4589daf1fd666b03a68b7d7dcd5c60903c10e946963fd324c9ee6185ed8e2dc7`, generation 1, lease `wp1236-b-r12-g1-claude-20261124`. Reviewer `openai_codex / codex_cli / machine`, run `46f0188f5f80485f9ea1c7110041c091`; model/effort phục vụ `KHONG_DO_DUOC` (high là yêu cầu, không phải bằng chứng đo). Linux/Python 3.13.18/Ruff 0.15.15. Không gọi mạng; repository chỉ đọc; mọi đầu ra và tệp tạm ở `work/`.

| Lớp | Đối chiếu lượt 1 | Mức mở | Phép đóng lớp |
|---|---|---|---|
| `nghiem-thu-khong-co-lap-chot-dich` | **VA_MOT_PHAN**: các ví dụ cụ thể đã bổ sung; miền ngữ pháp hữu hạn qua L8 còn thiếu | P2 — B01 | Ledger toàn bộ miền/mệnh đề luật 4/8 → ca L8, oracle độc lập, đủ đối chứng dương/âm; suite và luật 9 đạt |

**B01 — Bảng mới chưa bao hết miền ngữ pháp bắt buộc.** Vị trí: `ops/land_evidence_nguon_test.py:721` (c32), `:744` (c34), `:766` (c35); căn cứ SPEC luật 4, phần cụ thể hóa ngữ pháp luật 8 và đoạn cuối luật 9. Luật 4 chỉ định consumer **L8 cho B**; ca leaf/consumer A không tự thay ca L8. Không yêu cầu B chạy lại toàn bộ phép vét cạn hàm lá A hay sao mọi lý do K1–K8.

Đã đóng các ví dụ lượt 1: ba khóa phi-lời-khai, `gate2output`, ba dạng landed `True`/`1`, tập dấu phân cách, URL 0/1/2, miễn hợp lệ thường/landed, strip/fullmatch và bảy cặp lỗi khả thi. Probe lịch sử **27/27 + 4/4** đạt. Script audit lịch sử giữ nguyên phạm vi c24–c32: **9/9 ca, 244 lời gọi module thật**; c34/c35 được đo riêng bằng ledger.

Ledger executor đã chạy lại: **159/159 ô**, đối tượng JSON bằng hoàn toàn bản nộp; c27=14, c32=67, c34=50, c35=19. Kỳ vọng từng bảng là literal suy từ luật; c24 dùng bản tham chiếu đặc tả tại base bất biến. Đây là bằng chứng các ô hiện có đúng, chưa phải bằng chứng đủ miền.

Các biểu hiện cùng cơ chế còn mở:

- **Dòng miễn:** audit 50 ô c34 thấy `ly_do` chỉ mang một giá trị ASCII hợp lệ: `job huy theo chi thi`. Thiếu ca rỗng/space/tab, tách dòng readback, general category đi được qua JSON (gồm Cs và ngoài BMP), điểm kết thúc ` han=`. Miền lớp ký tự URL/SHA/OS/ngày cũng chưa có bảng consumer.
- **Tệp đánh giá:** 19 ô c35 đã có các loại dòng và CR/LF, nhưng thiếu mệnh đề tên job không rỗng, nhãn không chứa `]`, delimiter sớm không khớp/hai hậu tố cùng khớp, văn bản tự do theo category và các vị trí số/hex. Tất cả fixture c35 ghi `str` bằng UTF-8, chưa đo byte sai UTF-8 qua L8.
- **Các vị trí ngữ pháp khác:** c32 không có đối chứng casefold `ſ`/`K`, Unicode âm theo category/non-BMP; miền số của tên khối landed và miền ký tự token tên tệp chưa có bảng consumer tương ứng. Chi tiết toàn miền và giới hạn: [scope-domain-review.json](scope-domain-review.json).

Phép đo tái lập: [audit_scope.py](audit_scope.py) quan sát 150 ô của bốn bảng, lưu [scope-summary.json](scope-summary.json) và [scope-observed.json](scope-observed.json). [probe_scope.py](probe_scope.py) chạy **23/23** đối chứng qua `main`/L8 với oracle độc lập: token casefold/Unicode, các dạng `ly_do`, byte UTF-8 sai, header sai độ dài/chữ số toàn độ, tên job rỗng/nhãn sai và lazy matching. Mã hiện tại trả đúng tất cả; [scope-probes.json](scope-probes.json) ghi riêng rc và dòng L8 mong/đo. **Đây là dữ liệu fixture trên mã nguyên vẹn, không phải đột biến ngoài manifest; không áp P3 `ngoai_bang_dong`.** Ca reviewer chạy không trở thành ca đã có trong candidate.

```sh
TMPDIR="$PWD/../work/tmp" PYTHONDONTWRITEBYTECODE=1 python3 -B ../work/audit_scope.py
TMPDIR="$PWD/../work/tmp" PYTHONDONTWRITEBYTECODE=1 python3 -B ../work/probe_scope.py
```

Cách vá chung: trong write set test, dùng bảng theo vị trí/mệnh đề, tái sử dụng fixture/generator đợt A nếu phù hợp và đưa qua `main`/L8; hỗ trợ byte cho đối chứng UTF-8. Giữ kỳ vọng từ đặc tả, không lấy output thực tế làm oracle; ledger phải map miền→ô, không chỉ đếm 159 dòng. Đo lại suite, mutant đích và luật 9. Không mở rộng write set hoặc vượt trần **450 dòng thêm** (hiện 414); không sửa module A để làm bảng xanh.

| Mục executor khai chưa đo | Xử lý phạm vi |
|---|---|
| Symlink qua L8 | Không bắt buộc sao các ca filesystem riêng A theo luật 4 B; giữ giới hạn chưa đo, không nhận là Windows pass |
| Tệp đánh giá không UTF-8 | Miền ngữ pháp chung luật 4/8; ca candidate còn thiếu, thuộc B01 |
| Mọi lý do K1–K8 phía provenance | Không đòi sao toàn bộ danh sách luật 1 của A sang B; ngoại lệ này không loại các mệnh đề ngữ pháp tệp |
| Cặp doc_readback→html_url | JSON hỏng chưa có đối tượng html_url để tạo lỗi ngữ nghĩa độc lập; không đòi ô bất khả thi; hai ca riêng đã có |
| head khác None | Ngoài B theo luật 4 tường minh; thuộc A trực tiếp và D2b C |

**Quét lỗi do bản vá:** không phát hiện oracle lấy từ output, phụ thuộc thứ tự hoặc rò tệp tạm trong phạm vi đo. Năm ca đổi chạy đảo thứ tự đều đạt; ba mutant mới baseline rc0, mutant rc3 với `DO:` đúng c24/c34/c35; thư mục tạm riêng rỗng. [patch-check.json](patch-check.json) giữ raw output. Một lần wrapper reviewer tự đỏ vì đọc diagnostic bị cắt 200 ký tự; đã sửa capture raw và chạy lại, không quy thành lỗi candidate.

| Phép kiểm | rc | Bằng chứng dương |
|---|---:|---|
| Suite đợt B | 0 | 35/35 ca; 143/143 mutant; tự kiểm DAT (2); TONG DAT |
| Cổng cây thật | 0 | 174 hồ sơ; 149 DAT; 25/28 cutover miễn; 0 vi phạm/không đo được |
| MIEN_TRU_L8 độc lập | 0 | 56 tên+băm; 93 lý do; khớp bản tham chiếu, 0 giao cutover |
| Ruff F head/base | 0/0 | Hai tệp cùng xanh, delta 0; no-cache |
| Ruff pin/probe contract | 0 | RUFF_CONTRACT 3 [] |
| Đăng ký test CI | 0 | 1226/1226 phản chứng, TỔNG ĐẠT |
| Diff/check/kích thước | 0 | Module không đổi so lượt 1; đúng 2 tệp; +414 ≤450; không lỗi whitespace |

**Luật 9:** hai lệnh `do` đã chạy lại đến `HOAN_TAT`, đủ ID/hash và baseline (head 35/35, base 23/23). Head **624 = 438 GIET + 173 SONG + 13 VO_CAN**; base **550 = 335 GIET + 187 SONG + 28 VO_CAN**. Theo E3, **76/76 delta GIET đúng ca**, **548 ID kế thừa, 0 hồi quy GIET→không GIET**. Hai return cũ đổi neo có replacement cùng nghĩa ở dòng 408, đều GIET bởi c14. Không có delta tương đương cần chứng minh; kho B rỗng. Nợ sống/vô can của mã L1–L7 kế thừa không thành finding B. Xem [luat9-summary.json](luat9-summary.json), [delta-ledger.json](delta-ledger.json), [inherited-ledger.md](inherited-ledger.md), [log head](logs/do-head.log), [log base](logs/do-base.log).

**M3 vẫn required.** Windows local chưa chạy, do điều phối đo exact head/base; miễn Windows CI trong assignment không miễn local. GitHub CI/connector/full_mutant_audit, selftest toàn kho và thử ghép master không được reviewer chạy, ghi `not_run`, không coi pass. Review này chưa cấp quyền push/merge/land.

Hội tụ B/1→B/2: **0/1 lớp đóng thật**, không có lớp mới. Cùng slug đã lặp nhiều lần trong lịch sử đặc tả/đợt A; không reset lịch sử bằng tên đợt B. Cần xem lại cách dựng bảng miền theo §12; verdict không tự cấp lượt tiếp. Snapshot đầu/cuối giữ nguyên HEAD/tree và **17938 tệp tracked**, diff/index rỗng, không untracked/ignored file (chỉ mount `.codex/` rỗng). Hai mốc không chứng minh toàn bộ lịch sử ghi.

Lệnh, rc, trạng thái, hash log và giới hạn đều ở [VERDICT.json](VERDICT.json). Kiểm schema bắt buộc lưu tại [kiem_verdict.txt](kiem_verdict.txt).

KET_LUAN: changes_requested
