Review mã wp1236 đợt B, lượt 1/4: **changes_requested — B01, một lớp P2**.

Ứng viên `f4e93b366d7014e3efd464b2018e8ec7a4f8576c`, tree `ef68fdd1000127174203f3213f19a69ca20be936`; base `f602325574c62184caf16309631f5f680ca5cee2`. Đặc tả r12 SHA-256 `4589daf1fd666b03a68b7d7dcd5c60903c10e946963fd324c9ee6185ed8e2dc7`, generation 1, lease `wp1236-b-r12-g1-claude-20261124`. Reviewer `openai_codex / codex_cli / machine`, run `a7819b048f5741019ff1ac00fec0aed7`; model/effort phục vụ không đo được từ receipt hiện có. Linux, Python 3.13.18, Ruff 0.15.15. Không gọi mạng; repository giữ read-only, scratch trong `work/`.

| Lớp | Biểu hiện | Mức mở | Sửa chung và phép đóng |
|---|---|---|---|
| `nghiem-thu-khong-co-lap-chot-dich` | B01: ma trận miễn; khóa/token/landed; ngữ pháp dòng đánh giá chưa đủ qua L8 | P2 | Bảng dữ liệu theo luật 4 → L8, oracle độc lập, đối chứng dương/âm và hai lỗi để khóa thứ tự; ledger từng miền; chạy lại suite và luật 9. |

**B01 — Luật 4 chưa được đo đủ qua consumer L8.** Vị trí chính: `ops/land_evidence_nguon_test.py:706–715` (`c32`), cùng `c27`. Luật 4 của SPEC yêu cầu đủ phần tử dương/âm của các miền nêu rõ, đi qua L8 ở đợt B. Luật 9 giữ các ca này bắt buộc độc lập với miền đột biến. Đây là thiếu ca nghiệm thu, không phải nâng một đột biến ngoài manifest lên P2.

Phép đo `audit_matrix.py` chạy các ca c24–c32 trên mã nguyên vẹn và ghi đầu vào/đầu ra tại biên L8: 9/9 ca đạt, 181 lời gọi module thật. Chỉ có **3** lời khai `owner_waived`, cả ba dừng tại `waiver_khong_co_can_cu:url`: hai từ tập base của c24 và một từ c32. Không có ca một URL hợp lệ, hai URL, miễn hợp lệ cho hồ sơ landed, `strip`/khớp trọn dòng miễn, hay hai lỗi đồng thời để khóa thứ tự. Toàn bộ tệp test chỉ có chữ `owner_waived` ở dòng 713. Bằng chứng: [matrix-observed.json](matrix-observed.json), [log](logs/matrix-observed.log).

Quét cùng lớp trên toàn bộ test còn cho thấy: chỉ một trong ba khóa phi-lời-khai có đối chứng; thiếu khóa giữ chữ số (`gate2output`); chưa có bảng đủ dấu phân cách; thiếu cặp `True`/`1` của cả ba dạng landed qua L8; không có bảng biến thể ngữ pháp từng loại dòng đánh giá qua consumer này. Ca c24 chỉ so tập ĐỎ, không so riêng các lý do; các ca L1–L7 dùng module câm. Test module A đo consumer của A, không thay nghĩa vụ L8 mà luật 4 chỉ định.

Reviewer chạy thêm **27/27** đối chứng qua `main`/L8 trên mã nguyên vẹn, gồm miễn hợp lệ, hai URL, strip/fullmatch, ưu tiên html_url→tác giả, hạn→OS, OS→SHA, ba khóa phi-lời-khai, khóa có số, dấu phân cách và ba dạng landed True/1. Mã hiện tại trả đúng các kỳ vọng này. Đây là bằng chứng các ô thiếu có thể đo trực tiếp, **không phải bằng chứng test ứng viên đã chứa chúng**, cũng không phải finding hành vi sản phẩm. Xem [probe_matrix.py](probe_matrix.py), [kết quả 27 ô](matrix-probes.json).

Bổ sung **4/4 đối chứng ngữ pháp dữ liệu** qua L8: bản hợp lệ rc 0; header sai → `dau_tep_sai`; dòng job sai → `dong_la`; dòng tổng sai → `dong_la,thieu_moc`, đều rc 1 với đúng dòng L8. Xem [probe_grammar.py](probe_grammar.py), [kết quả](grammar-probes.json). Đây là biến thể dữ liệu, không đột biến mã.

Tái lập từ repository, toàn bộ tệp tạm ở scratch:

```sh
TMPDIR="$PWD/../work/tmp" PYTHONDONTWRITEBYTECODE=1 python3 -B ../work/audit_matrix.py
TMPDIR="$PWD/../work/tmp" PYTHONDONTWRITEBYTECODE=1 python3 -B ../work/probe_matrix.py
TMPDIR="$PWD/../work/tmp" PYTHONDONTWRITEBYTECODE=1 python3 -B ../work/probe_grammar.py
```

Đề nghị bổ sung hoặc tái sử dụng bảng dữ liệu cho các miền hữu hạn luật 4, qua `main`/L8 với kỳ vọng độc lập. Không cần thêm miền ngoài đặc tả. Đóng B01 khi ledger từng miền/ô chỉ ra ca thực đo, đủ đối chứng và thứ tự chốt, suite xanh, delta luật 9 đạt và không hồi quy kế thừa.

Các phần đã xác nhận:

| Phép kiểm | rc | Bằng chứng |
|---|---:|---|
| Test đợt B | 0 | 33/33 ca; 140/140 đột biến chết đúng lý do; tự kiểm DAT (2); TONG DAT |
| Cổng cây thật | 0 | 174 hồ sơ: 149 DAT, 25/28 cutover miễn, 0 vi phạm, 0 không đo được |
| Đo tập ĐỎ base | 0 | 56 mục/93 vi phạm; khớp tên+băm hằng L8, 0 giao cutover; 56/56 byte khớp cả 8048551 |
| Ruff F head/base | 0/0 | Cả hai All checks passed; delta 0; no-cache |
| Đăng ký test CI | 0 | 1226/1226 phản chứng; TONG DAT |
| diff --check | 0 | Không lỗi |
| numstat | 0 | 2 tệp, 342 dòng thêm ≤ 6/450 |
| Manifest và hồi quy | 0 | 624 = 548 kế thừa + 76 delta; 550 base, 548 áp được, 2 return cũ đổi neo |

B1–B8 đều có ca đích: B1 c11/c24, B2 c25, B3 c29, B4 c30, B5 c28, B6 c26, B7 c27, B8 c31. Harness kiểm baseline trước, mutant rc3 với đúng dấu `DO:<ca>:`; 140/140 đạt bao gồm các mutant mB1–mB8. Kết quả này không đóng B01.

L8 chạy sau L5, dùng dữ liệu đã nạp và provenance đúng hồ sơ, giữ từng lý do khi thêm tiền tố L8. `importlib` + `exec(compile)` đọc đúng module của `--root`, không qua pyc; nạp trước miễn L8 vẫn giữ fail-closed và không vượt chốt cutover. Bắt `SystemExit` ngăn thoát 0 giả. B5 dùng vân tay độc lập của tập tên+băm; reviewer đo lại khớp. Không tìm thấy lỗi hành vi trong phần nối L8 và các phép đo đã nêu.

**M3 Windows: required.** Bước 1 không phải làn lưu trữ; bước 2 khớp các dòng thêm `encoding=` và `subprocess.run` trong tệp Python (92, 302, 573, 678); dừng ở bước 2. Windows local chưa chạy, do điều phối đo trên exact head/base. Windows CI được chủ kho miễn theo assignment; không suy miễn local.

**Luật 9 đã đo lại đầy đủ:** cả hai lệnh `do` rc 0 và có `HOAN_TAT`; baseline head 33/33, base 23/23. Head: **624 = 438 GIẾT + 173 SỐNG + 13 vô can**, 0 lỗi chạy. Base: **550 = 335 GIẾT + 187 SỐNG + 28 vô can**, 0 lỗi chạy. Băm manifest, module, test/shim, bộ quét, kho rỗng và Python khớp handoff.

Theo E3 (DELTA + không hồi quy), **76/76 delta GIẾT**, mỗi ID có ca và assertion `DO:`; không có delta tương đương cần chứng minh. **548 ID kế thừa: 0 hồi quy GIẾT → không GIẾT**. Hai ID base không áp được là `c2:kiem_ho_so:340:4` và `f:kiem_ho_so:340:4`; thay thế cùng nghĩa ở dòng 408 đều GIẾT bởi c14. Toàn bộ 173 SỐNG và 13 vô can ở head thuộc kế thừa, không báo thành finding của B. Kho (B) rỗng; không dựng thêm đột biến ngoài manifest.

Bằng chứng đầy đủ: [tóm tắt và neo](luat9-summary.json), [76 ID delta](delta-ledger.json), [bảng 548 ID base↔head](inherited-ledger.md), [log head](logs/do-head.log), [log base](logs/do-base.log). `finish_luat9.py` kiểm tập ID, sha256 từng mutant, baseline, dấu hoàn tất và từng hàng hồi quy; rc 0. Đây là nghiệm thu luật 9; **không thay việc bổ sung ca luật 4 còn thiếu ở B01**.

Lệnh, rc, hash log, trạng thái và các lỗi setup/fixture đã sửa nằm trong [VERDICT.json](VERDICT.json). `not_run`: Windows local, CI/connector/full_mutant_audit, selftest toàn kho và thử ghép master; không có test skipped trong các suite đã đo. Snapshot đầu/cuối khớp HEAD/tree và băm 17938 tệp tracked; diff/index rỗng, không có untracked file. Ignored chỉ có mount `.codex/` rỗng. Hai mốc không chứng minh toàn bộ lịch sử ghi. Ruff pin/probe riêng đạt `RUFF_CONTRACT 3 []`, rc 0. Bản này là review mã offline; chưa cấp quyền push/merge/land.

Kiểm schema cuối: `python3 ../kiem_verdict_lop.py ../work/VERDICT.json --vong 1` → `HOP_LE (§8.3): 1 finding, 1 lop`, rc 0; stdout ở [kiem_verdict.txt](kiem_verdict.txt).

KET_LUAN: changes_requested
