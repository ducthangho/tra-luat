# Review mã bo-sinh-bat-bien r1/g1 — lượt 2

**changes_requested — 1 finding P3, cùng 1 lớp. R1-01 và R1-02 đã vá thật trong phạm vi cụ thể; lớp VA_MOT_PHAN vì R2-01 còn mở. Không phát hiện P0/P1/P2.**

- HEAD `ef82ed9a7c26f085fa567021fea1d0baaf15c75b`; tree `30d8b599d30f7552e5b1c00b51008d4efec09c66`.
- Base `a89c83acf998008caecba9084a7d295845bf1976`; spec SHA-256 `bdde0a9bdba79a19fbbc77cfee8311e209b0c91cc16612bb8029167cca186577` đã tự kiểm.
- Reviewer độc lập `openai_codex / codex_cli / machine/local`, run `866eb42659994d88b5bc3da44d2af062`; Linux, Python3.13.18, Unicode15.1, Ruff0.15.15, core.abbrev7. Header CLI gpt-6-astra/high; model/effort phục vụ KHONG_DO_DUOC.
- Wrapper run.json khai local_process/subprocess/machine; reviewer process được neo bởi executable codex.js và header OpenAI Codex0.172.0. Không dùng wrapper generic để suy model phục vụ.
- Chỉ đọc checkout, mọi sửa/đột biến ở work/. Diff2 tệp+201/-6 trong trần320. Hai module sản phẩm byte-identical base.

## Bảng lớp và đối chiếu lượt trước

| Lớp | R1-01 | R1-02 | Biểu hiện mở | Nhãn / mức |
|---|---|---|---|---|
| `nghiem-thu-khong-co-lap-chot-dich` | DA_VA_THAT | DA_VA_THAT | R2-01: exact count bị nới thành sàn mà suite vẫn xanh | VA_MOT_PHAN / P3 |

Cách vá chung: đối chứng phải phân biệt các chiều sai của bất biến với giá trị đúng, qua cùng consumer/cache, cô lập khỏi chốt lân cận. Đóng lớp khi mutant `==→>=` bị c40 bắt, witness thừa phần tử bị c36 chặn,14 phép gỡ và các bằng chứng cũ giữ kết quả; gates/thời gian vẫn đạt.

Lịch sử giữ B02 wp1236 lượt4 → ded4128 lượt1 → ef82ed9 lượt2. Đóng2/2 biểu hiện cũ không thành đóng lớp: U=1,F=0, tỷ lệ0/1; không có lớp mới. P3-only rework không giảm số lớp: dừng vá tự động và trả checkpoint điều phối theo M1, không tự gọi lượt3 dù trần4 còn dư.

R1-01: gỡ tổng158/648 nay đều rc3 DO:c39. Trace37 âm c37 đều rc3 DO:c37 và0 ô; hai dương rc0/648 ô. Guard witnesses dùng ky8 thật xác nhận648 ô và647 khi cố ý bỏ chốt. R1-02: đúng cặp outside-mutant làm c36 rc3 `35 phần tử KHÁC NHAU (đặc tả: đúng36)`; tám ca và cache đã đo riêng.

# R2-01 — P3 — c40 chưa khoá chiều thừa của chốt số phần tử chính xác

Lớp giữ nguyên: `nghiem-thu-khong-co-lap-chot-dich`. Vị trí: `ops/land_evidence_nguon_test.py:1001` (bảng phản chứng c40), chốt đích ở dòng879.

Đặc tả 2.2.1 đòi số phần tử qua main→L8 **BẰNG ĐÚNG** từng kỳ vọng và bỏ chốt sàn. Đây là tính chất cần khoá trong miền đặc tả, khác giới hạn mục8 về thay một ô bằng ô mới cùng số lượng.

Đột biến một mệnh đề, neo xuất hiện đúng một lần trên bản sao:

```python
bang(rc == 0 and dem[0] - truoc == mong,
# thành
bang(rc == 0 and dem[0] - truoc >= mong,
```

`excess_probe.py` đã chạy cả hai vế. c40 nguyên vẹn và c40 với sàn đều rc0. Mọi nhánh c40 hiện có dùng N bằng hoặc nhỏ hơn kỳ vọng, nên không phân biệt được `==` với `>=`.

Chứng nhân độc lập: thêm một bản sao `kiem(dong, ten_goc)` vào a129 (không thay một ô khác). Số phần tử qua main→L8 thành37, số khác nhau giữ36, category và ngoàiBMP không đổi. C36 HEAD trả rc3:

`DO:c36_l8_ngu_phap_luat_8_qua_bang_cua_dot_a:a129_ten_job_lazy_qua_ho_so qua main → L8: 37 phần tử (đặc tả: đúng 36), rc=0 `

C36 với sàn lại rc0. a129 nguyên vẹn đều rc0. Không có rc4. Cặp nguồn/thay nguyên văn và cả sáu kết quả ở `excess-probe.json`. Phép full suite của mutant một-mệnh-đề đã đạt rc0: CA40/40, DOT BIEN145/145, TU KIEM PHAN HANG DAT (2), TONG DAT (`floor-full-B.log`, `floor-full-B.json`). Không ghép chứng nhân thêm ô vào mutant full suite ấy: chỉ một phép đổi `==`→`>=` đã sống qua cả bộ.

Đây là lỗ trong cơ chế nghiệm thu hồi quy của test, không phải khẳng định HEAD nguyên vẹn đã đếm sai, nên P3 `ngoai_bang_dong`, không nâng P2. Gỡ nguyên mệnh đề vẫn làm c40 đỏ không đóng được hướng thừa: chốt khác/sai thông điệp có thể làm phép gỡ đỏ trong khi nới thành sàn vẫn xanh.

Hướng vá: thêm vào c40 một phản chứng THÊM bản sao ô, giữ số khác nhau/category/BMP, qua chính main→L8 và đòi rc3 DO:c36 với tổng lớn hơn kỳ vọng; giữ control nguyên vẹn cùng đường cache. Có thể dùng a126 rẻ hơn, nhưng executor cần tự dẫn xuất và đo. Phép khoá: đổi `==`→`>=` phải làm c40 đỏ; bản nguyên vẹn và14 phép gỡ cũ vẫn đạt hợp đồng; không suy từ tổng bộ test xanh. Rủi ro: thêm đường a129 có I/O provenance lớn; phải đo lại cặp thời gian với ngưỡng B+30s, không sửa fixture hoặc nới chốt để né chi phí.

Tái lập (từ repo, chỉ ghi work/):

```bash
PYTHONDONTWRITEBYTECODE=1 TMPDIR="$PWD/../work/tmp" python3 -B ../work/excess_probe.py
# full suite trên clone riêng; dùng thư mục floor mới khi chạy lại
PYTHONDONTWRITEBYTECODE=1 TMPDIR="$PWD/../work/tmp" python3 -B ../work/excess_full.py
```

## Cổng tự chạy và thời gian

| Phép đo | rc | Bằng chứng |
|---|---:|---|
| base-B | 0 | CA: 38/38 dat; DOT BIEN: 145/145 bi giet dung ly do; TU KIEM PHAN HANG: DAT (2 dot bien); TONG: DAT |
| head-B | 0 | CA: 40/40 dat; DOT BIEN: 145/145 bi giet dung ly do; TU KIEM PHAN HANG: DAT (2 dot bien); TONG: DAT |
| base-A | 0 | CA: 51/51 dat; DOT BIEN: 158/158 bi giet dung ly do; TU KIEM PHAN HANG: DAT (2 dot bien); TONG: DAT |
| head-A | 0 | CA: 53/53 dat; DOT BIEN: 158/158 bi giet dung ly do; TU KIEM PHAN HANG: DAT (2 dot bien); TONG: DAT |
| head-land | 0 | TỔNG: ĐẠT |
| head-ci | 0 | RUFF CI: 3/3 hợp đồng; PHẢN CHỨNG: 1677/1677 đỏ đúng; TỔNG: ĐẠT |
| base-selftest | 1 | == tl selftest 1773/1789 == |
| head-selftest | 1 | == tl selftest 1773/1789 == |
| base-ruff | 0 | All checks passed! |
| head-ruff | 0 | All checks passed! |

Command/cwd/rc/thời gian/hash trong VERDICT.json và gates.json; log tên từng dòng. Các lệnh đúng assignment: hai suite, land --root ., ci_dang_ky_test.py, selftest, ruff --no-cache --select F hai tệp. diff --check rc0; numstat rc0+201/-6; Ruff bare lint delta0, pin/probe riêng RUFF CI3/3. Không có skipped được coi pass.

Đo tuần tự cùng lệnh/máy: B 276.26→305.21s, Δ+28.95s≤30; A 336.07→333.13s, Δ-2.94s≤5. Executor ghi B310.5→328.2 (+17.7), A337.0→336.9 (-0.1). Cả hai phép đo đều trong trần; chỉ một mẫu mỗi vế, không khẳng định độ biến động hay Windows. Không dùng thời gian các probe song song để so.

## Phản chứng, hằng và tín dụng

14/14 phép gỡ nguyên mệnh đề trả rc3 DO đúng ca; thêm một phép legacy sửa hai vế cũng rc3 nhưng không tính vào14. Mỗi dòng đầy đủ ở probes.json:

| Chốt gỡ | rc | DO quan sát |
|---|---:|---|
| c36-count | 3 | `DO:c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o:bộ test đợt A bỏ Mn (a129) mà c36 không ĐỎ đúng chốt: rc=3 DO:c36_l8_ngu_phap_luat_8_qua_bang_cua_dot_a:a129_ten_job_lazy_qua_ho_so qua main → L8: 35 phần tử KHÁC NHAU (đặc tả: đúng 36)` |
| c36-category | 3 | `DO:c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o:bộ test đợt A Mn thành ký tự Mc KHÁC (a126) mà c36 không ĐỎ đúng chốt: rc=0` |
| c36-BMP | 3 | `DO:c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o:bộ test đợt A ngoài BMP thành ký tự BMP KHÁC (a126) mà c36 không ĐỎ đúng chốt: rc=0` |
| c37-total-literal | 3 | `DO:c39_c37_do_khi_bo_sinh_lech_mien:lặp CHÍNH ký tự ngoài BMP cuối mà c37 không ĐỎ đúng chốt với đúng 0 ô: rc=3, 0 ô, DO:c37_l8_van_ban_tu_do_tep_danh_gia_qua_cong:số ô lệch đặc tả: 652 (đúng 648)` |
| c37-distinct | 3 | `DO:c39_c37_do_khi_bo_sinh_lech_mien:Lu thành ASCII 'A' mà c37 không ĐỎ đúng chốt với đúng 0 ô: rc=0, 648 ô,` |
| c37-category | 3 | `DO:c39_c37_do_khi_bo_sinh_lech_mien:Mn thành ký tự Mc KHÁC mà c37 không ĐỎ đúng chốt với đúng 0 ô: rc=0, 648 ô,` |
| c37-648 | 3 | `DO:c39_c37_do_khi_bo_sinh_lech_mien:c37 mất một ô rời mà c37 không ĐỎ đúng chốt với đúng 0 ô: rc=0, 647 ô,` |
| c36-distinct | 3 | `DO:c40_c36_do_khi_bang_cua_dot_a_mat_mien_hoac_o:bộ test đợt A Mn thành bản sao Mc (a126) mà c36 không ĐỎ đúng chốt: rc=3 DO:c36_l8_ngu_phap_luat_8_qua_bang_cua_dot_a:a126_mien_ascii_qua_ho_so qua main → L8: thiếu general category ['Mn']` |
| a135-so_phan_tu | 3 | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh bo Mn: rc=3 DO:a135_bo_sinh_dung_mien_dac_ta:bộ sinh('—', ()) lệch đặc tả: ['category_vang']` |
| a135-category_vang | 3 | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh bo Mn: rc=3 DO:a135_bo_sinh_dung_mien_dac_ta:bộ sinh('—', ()) lệch đặc tả: ['so_phan_tu']` |
| a135-lap_category | 3 | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh Mn thanh ban sao Mc: rc=3 DO:a135_bo_sinh_dung_mien_dac_ta:bộ sinh('—', ()) lệch đặc tả: ['category_vang']` |
| a135-thuoc_cam | 3 | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh bo loc cam: rc=3 DO:a135_bo_sinh_dung_mien_dac_ta:bộ sinh('\n\r\x0b\x0c\x1c\x1d\x1e\x85\u2028\u2029 \t', ()) lệch đặc tả: ['so_phan_tu', 'category_vang']` |
| a135-tu_0080 | 3 | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh Lu thanh ASCII: rc=0` |
| a135-cuoi_ngoai_bmp | 3 | `DO:a136_a135_do_khi_bo_sinh_lech_mien:bộ sinh bo ngoai BMP: rc=3 DO:a135_bo_sinh_dung_mien_dac_ta:bộ sinh('—', ()) lệch đặc tả: ['so_phan_tu']` |

Trace hiện có: c39=37 âm+2 dương; c40=7 âm+2 dương; a136=6 âm+1 dương:50 âm rc3 DO đúng đích,5 dương rc0,0 rc4. c38 thêm24/24 âm inventory đúng chốt. Xem trace-v2.json. Riêng gỡ chốt khác nhau làm c40 đỏ đầu tiên ở biến thể Mn thành bản sao Mc; hai witness cấu trúc a126/a129 cùng được khoá. distinct-target.json đo trực tiếp: còn chốt đều rc3 DO:c36 (51/52 và35/36); gỡ riêng chốt đều rc0.

Bản sao nap_sua: neo vắng/lặp đều bị TinHieuChotCa; control cùng đường chưa đủ nếu đứng riêng, nhưng audit nguồn cùng mọi hàm/code/constant/metadata, inventory, A_CA/LOAI/paths đều trùng (nap-code-audit.json); c37 của bản sao được dispatch đúng. Marshal byte ban đầu không khớp; chưa cô lập nguyên nhân biểu diễn, nhưng kiểm code equality và mọi thuộc tính/constant lồng nhau đều khớp, không dùng raw marshal làm kết luận. c39 chỉ đo chốt trước vòng ô; consumer được c37 thật/guard witnesses đo.

Cache bật/tắt: chín nhánh c40,SHA256 của402 bộ byte hồ sơ/provenance thực vào main và toàn bộ rc/DO trùng (cache-audit.json). Khoá theo input/kwargs, trả deepcopy; SafeLoader riêng của sản phẩm không bị thay.

| Ca | Tổng | Khác nhau | Gặp lại |
|---|---:|---:|---:|
| a124 | 1733 | 1649 | 84 |
| a125 | 3840 | 3769 | 71 |
| a126 | 52 | 52 | 0 |
| a129 | 36 | 36 | 0 |
| a131 | 1 | 1 | 0 |
| a132 | 1280 | 1265 | 15 |
| a133 | 1136 | 1108 | 28 |
| a134 | 318 | 318 | 0 |

Từng số hạng tự suy từ mã trong [independent_counts.md](independent_counts.md); count-audit.json ghi các cặp gặp lại, tổng8396, gặp lại198, khác nhau theo từng ca8198. Chỉ đếm tổng không thay phân rã. Bỏ provenance làm a125 chỉ1/3769 khác nhau; bỏ hồ sơ làm a124 chỉ1/1649; quên clear làm a1255418/3769 — cả ba rc3 DO:c36 (fingerprint-scan.json).

Unicode: Python3.12/15.0 và3.13/15.1 có đúng cùng năm miền đại diện và19 whitespace. Các hằng lặp theo cấu trúc cùng giao9 L/N,1 Nd,3 whitespace; có phụ thuộc thuộc tính Unicode ở giao này nhưng không đổi giữa hai phiên bản đã đo, không cam kết mọi phiên bản tương lai. c36,c39,c40,a135,a136 trên Python3.12 local đều rc0.

## Hai phản chứng B02 và full probes

- `omit-category-Mn` / `c36_l8_ngu_phap_luat_8_qua_bang_cua_dot_a`: rc3, `DO:c36_l8_ngu_phap_luat_8_qua_bang_cua_dot_a:a124_token_ascii_qua_ho_so qua main → L8: 1723 phần tử (đặc tả: đúng 1733), rc=0 `
- `omit-category-Mn` / `c37_l8_van_ban_tu_do_tep_danh_gia_qua_cong`: rc3, `DO:c37_l8_van_ban_tu_do_tep_danh_gia_qua_cong:vũ trụ ký tự lệch đặc tả: 157 ký tự (157 khác nhau), category lệch ['Mn'], 1 ngoài BMP`
- `omit-lazy-backtracking` / `c36_l8_ngu_phap_luat_8_qua_bang_cua_dot_a`: rc3, `DO:c36_l8_ngu_phap_luat_8_qua_bang_cua_dot_a:a129_ten_job_lazy_qua_ho_so qua main → L8: 35 phần tử (đặc tả: đúng 36), rc=0 `

| Full probe trên bản sao | rc | Dòng hợp đồng |
|---|---:|---|
| B02-omit-category-Mn-B | 1 | CA: 36/40 dat; DOT BIEN: 143/145 bi giet dung ly do; TU KIEM PHAN HANG: DAT (2 dot bien); TONG: DO |
| B02-omit-category-Mn-A | 1 | CA: 51/53 dat; DOT BIEN: 158/158 bi giet dung ly do; TU KIEM PHAN HANG: DAT (2 dot bien); TONG: DO |
| B02-omit-lazy-backtracking-B | 1 | CA: 38/40 dat; DOT BIEN: 144/145 bi giet dung ly do; TU KIEM PHAN HANG: DAT (2 dot bien); TONG: DO |
| outside-duplicate-structural-A | 0 | CA: 53/53 dat; DOT BIEN: 158/158 bi giet dung ly do; TU KIEM PHAN HANG: DAT (2 dot bien); TONG: DAT |
| outside-duplicate-structural-B | 1 | CA: 38/40 dat; DOT BIEN: 144/145 bi giet dung ly do; TU KIEM PHAN HANG: DAT (2 dot bien); TONG: DO |

Rc1 của suite mutant là tổng, không nhầm với tín hiệu rc3 của ca đích. Nguyên văn DO của mọi lượt lưu probes.json/b02-targeted.json/guard-witnesses.json. probes.py được sao từ lượt1, thêm đúng chốt mới; khoá same-run chỉ tránh queue chạy lặp, không bỏ phép nào.

# Phạm vi và lập luận kiểm tra

## `nap_sua` và tín dụng cho 648

`nap_sua` đọc `HERE/ten` UTF-8, đòi `nguon.count(cu)==1` rồi compile toàn bộ nguồn với đúng một phép replace. Trong c39, bản sao nguyên vẹn dùng `cu==moi`; bản thiếu ô chỉ xoá `(nhan,"",dung)`, giữ nguyên vũ trụ. Hai bản đều gọi `mod.chay_ca`, patch globals của `mod.CA[c37]`, không gọi nhầm c37 của module mẹ. Gỡ chốt trên tệp bản sao ở work/mut làm cả đường nạp in-memory mất chốt; vì vậy ca c39 phải đỏ. Không suy từ việc control xanh đơn lẻ rằng mọi bản sao tuỳ ý tương đương: phải kiểm nguồn tạo bản sao, mã ca đăng ký và đường dispatch. `nap-code-audit.json` đo tính bằng nhau của code/constant và `nap-sua.json` đo inventory/globals/neo, còn guard-witnesses đo 648 ô với ky8 thật.

c39 cố ý thay ky8 bằng bộ đếm vì kiểm hai chốt trước vòng ô. Nó không chứng nhận consumer. c37 thật trong suite và guard_witnesses mới đo consumer. Phản chứng phải có rc3 DO:c37, đúng thông điệp, 0 ô; hai control phải rc0 và648 ô. Thiếu ô nhưng thực chạy647 mà c39 vẫn xanh sẽ là tín dụng giả; phản chứng gỡ chốt kiểm riêng điều đó.

## Cache YAML

Khoá gồm tên hàm, toàn nội dung input (str/bytes hoặc pickle cho cấu trúc), kwargs đã sort; safe_load và safe_dump không dùng chung namespace. Trả deepcopy để biến thể đổi provenance không làm nhiễm bản gốc. Context patch kết thúc ở mỗi hàng; cache giữ giá trị theo input, không giữ đối tượng có thể bị sửa. `nap_yaml` sản phẩm dựng lớp SafeLoader riêng, không đi qua wrapper safe_load. `cache_audit.py` bỏ cache chỉ trong bản in-memory của test, vẫn chạy toàn chín nhánh c40, ghi SHA256 từng bộ byte hồ sơ/provenance tại đầu `main` thật và từng rc/DO của c36. Chỉ khi hai chuỗi dữ liệu/đầu ra trùng mới nhận cache giữ nguyên thứ được đo.

## Phần ngoài đặc tả

Mục 2.2.1 đòi số phần tử đúng; 2.2.2 đòi CHỨA category bắt buộc và có ngoài BMP; 2.2.3 giữ24 phản chứng registry. Mục3 P5 đòi bỏ một lời gọi cấu trúc phải đỏ. Không có điều khoản ghim nội dung/ID từng ô cấu trúc; mục8 đã khai rõ thay một ô bằng ô khác cùng số lượng/category là giới hạn. R1-02 cụ thể (thay bằng bản sao ô đầu) phải được đóng bằng đo lại; bản thay KHÔNG trùng còn sống không tự mở lại finding đó.

`scope_scan.py` gồm hai minh hoạ: thay marker `[khong khop]` bằng `[khac]` giữ cả nghĩa; và thay ô ấy bằng `kiem(dong + " ", ten_goc)` có thể làm mất chính ví dụ delimiter sớm nhưng vẫn36 phần tử khác nhau, miền category/non-BMP không đổi. Đã đo cả hai ca A/c36 qua L8 đều xanh; đây minh hoạ đúng giới hạn đã khai, không phải mất category, thiếu số phần tử, thiếu ngoài BMP hoặc sai648 thuộc mục2–3. Không dùng lập luận 'mutant sống' để mở rộng đặc tả; cũng không dùng giới hạn này để miễn mutant bỏMn hay bỏ lời gọi (chúng thuộcP4/P5).

## M3 và E

M3 **required**, bước2: dòng thêm `nap_sua(...).read_text(encoding="utf-8")`; không phải làn lưu trữ. Kế thừa required từ lượt1; diff lượt2 vẫn có dòng mã `encoding=`. Windows local base/head và CI chưa chạy trong review offline. Đặc tả giao điều phối chạy Windows; không tự miễn hoặc coi Linux thay Windows.

E1–E5 đối với diff đều **khong**: chỉ test, không đổi điều kiện land ở module sản phẩm, lease/merge gate, authority, workflow hoặc LIVE. Không suy đây là quyền merge. M9 full_mutant_audit vẫn cần exact head vì chạm ops/**/*.py.

## Luật9

Module A/B byte-identical base (product-identical.json). Không chạy lại bốn lượt full theo chỉ thị. Bước8 trên ef82ed9 **chua_do_duoc**, ghi not_run ở review này. Kết quả lượt1 trên ded4128 không chuyển sang SHA mới. Điều kiện chấp nhận: handoff bổ sung neo ef82ed9/tree, đủ hai cặp module/test trên base/head, đúng công cụ/kho/Python, manifest và dấu HOAN_TAT, so từng ID không có GIET-base→hạng khác-head; giữ riêng nợ SONG/VO_CAN và không tính không áp dụng thành GIET. Việc chưa đo không tự tạo finding mã, nhưng không thể ghi nghiệm thu bước8 đạt.

## Selftest và giới hạn

Hai vế selftest: base rc1, head rc1; 16 ID đỏ giống nhau, delta0. Giữ **failed**, không gọi N/N. Origin/master có trong cả hai clone scratch.

- `r973_bootstrap_khong_kiem_khoa`
- `r973_bootstrap_ba_trang_thai`
- `r973_bootstrap_require_agent_creds`
- `r973_bootstrap_giu_auth_json_moi_hon`
- `r973_bootstrap_last_refresh_hong_khong_pha`
- `r973_bootstrap_auth_json_nguyen_tu`
- `r973_bootstrap_sai_dinh_dang_khong_nap`
- `r973_bootstrap_khong_export_khong_ghi_gemini`
- `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim`
- `r268_l2_trichotomy_theo_trang_thai_object`
- `wp433_gws_cred_dich_ngoai_kho`
- `wp433_gws_cred_dich_ngoai_kho_b`
- `wp433_gws_cred_no`
- `wp433_gws_cred_win_reparse`
- `wp433_nlm_gws_dich_ngoai_kho`
- `wp727_tl_gws_refresh`

Chẩn đoán một phần: mini-repo fixture git init/add rc0, commit rc128 vì signer gọi loopback bị sandbox từ chối, rev-parse HEAD rc128. Đây là căn cứ cho hai ca r226/r268, không suy lỗi ref origin/master. Predicate _trong_kho_git trên work/tmp trả /tmp do marker /tmp/.git; phản chứng chỉ trong mô hình read-only không có marker trả None. Không sửa marker, không đọc/ghi credential thật, không thay signer. Các lỗi bootstrap/credential có đường chốt này nhưng chưa cô lập nhân quả từng ID; xem selftest-summary.json, selftest-diagnostic-excerpts.json và log. Ví dụ trace wp433_nlm_gws_dich_ngoai_kho báo w6_chi_config_ngoai_kho: duong và d5_khong_claude: codex_da_nap; giữ nguyên lỗi quan sát thay vì đoán pass.

## Chưa chạy / phạm vi kết luận

- Bốn lượt full Luật9/bước8 trên ef82ed9: không chạy lại theo assignment; chờ handoff bổ sung exact SHA.
- Windows local base/head và Windows CI: not_run; M3 required.
- GitHub CI/connector/full_mutant_audit M9, audit uỷ quyền, push/merge/land: not_run, không được review này chứng nhận.
- Cô lập nhân quả đầy đủ từng ID selftest dưới môi trường không có /tmp/.git và signer hoạt động: not_run; không có quyền thay môi trường ngoài work/.

- Không chốt nội dung từng ô cấu trúc: hai mutant minh hoạ trong scope-scan.json khớp giới hạn §8, không là findings.
- Selftest vẫn failed trong sandbox ở cả hai vế, delta0 không phải N/N; chẩn đoán chỉ một phần, không suy nguyên nhân tất cả16 ID từ /tmp/.git.
- Không gọi GitHub/web/network để lấy authority hoặc CI. Selftest và fixture Git có signer thừa kế thử loopback, bị sandbox từ chối; không truy cập thành công, không đổi cấu hình để vượt chặn.
- Model/effort thực phục vụ KHONG_DO_DUOC; header CLI công bố gpt-6-astra/high không chứng minh mọi request.
- Read-only là kỷ luật: sandbox workspace-write. Snapshot hai mốc không chứng minh mọi sự kiện trung gian. Repo nguồn ngoài checkout được cấp không nằm trong phạm vi quan sát.
- So thời gian chỉ một lượt mỗi vế. Python3.12 local dùng Unicode15.0/PyYAML6.0.1, không phải bằng chứng full CI hay Windows.
- So marshal.dumps ban đầu không trùng; chưa cô lập chi tiết biểu diễn của marshal, không dùng nó kết luận code khác. nap-code-audit.json so Python code equality và mọi thuộc tính/constant lồng nhau: đều trùng.

Snapshot đầu/cuối ở snapshot-start.json / snapshot-end.json, kiểm lại HEAD/tree và mọi byte tệp quan sát được trong repo. Verdict không phải quyền push/merge/land. CHƯA ĐỦ ĐIỀU KIỆN MERGE: R2-01 P3 mở, Luật9 exact SHA, Windows và các gate/audit còn thiếu.

KET_LUAN: changes_requested
