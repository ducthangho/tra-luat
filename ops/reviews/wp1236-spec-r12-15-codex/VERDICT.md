# wp1236 r12 — review đặc tả vòng 15

**Verdict: approve** — 0 P0/P1/P2/P3 mở trong đặc tả.

- Reviewed SHA: `26436102171819ff5a11ecf4b2ff3a4b4d09daf1`.
- Tree: `9a305239b523e58aac2f2d50824d9e34b3582834`.
- Spec SHA-256: `4589daf1fd666b03a68b7d7dcd5c60903c10e946963fd324c9ee6185ed8e2dc7`.
- Provider/surface/transport: `openai_codex / codex_cli / machine`. Model và effort phục vụ: `KHONG_DO_DUOC`; nguồn identity: `run/1c496e60/run.json`. Checkout chỉ đọc; mọi phép đo/scratch trong `work/`; không mạng.

**AE01: ĐÃ VÁ THẬT.** Oracle toàn biểu thức, sau tiền xử lý và có assertion/tập TOKEN, khớp **10.134/10.134** vector qua hàm lá và consumer. `measured\n` được token nhận; consumer vẫn đòi tệp đánh giá. LF đầu/giữa bị từ chối. Có đối chứng casefold một và nhiều ký tự (`ſ`, `K`, `ß`, `ẞ`). Không thấy hồi quy của lớp đã đóng AD02/AD03.

| Lớp đặc tả còn mở ở vòng 14 | Nhãn vòng 15 | Bằng chứng |
|---|---|---|
| `test-thieu-chot` | ĐÃ VÁ THẬT | `contract_probes.json`, `token_sweep.json`: oracle khớp; 3 ca lazy đạt, greedy phản chứng đỏ |
| `nghiem-thu-khong-co-lap-chot-dich` | ĐÃ VÁ THẬT, alias cùng lớp | Giữ luật 1/2/4/6/7, thứ tự B→A→ngoài và băm đủ hạt giống/phép chiếu/125 ô |

Hội tụ **14→15 = 1/1**, đếm alias một lần. Giữ lịch sử lớp lặp; không tính việc đổi scope r12 là vá mã. Các finding mã S01/S02 vẫn mang nghĩa vụ riêng trong `prior_code_status` của JSON; verdict này không đóng hay miễn chúng.

**Miền nghiệm thu:** ngôn ngữ regex vẫn vô hạn; chỉ tập vector và A∪B là hữu hạn. Đã đối chiếu 10 regex module + 2 D2b, đủ **sáu** vị trí văn bản tự do. Hai lần `sinh` trên mã `0d814877…` cho **780** mutant, **24** toán tử, manifest giống từng byte. Kho B có **201 ID = 186 + 15** đúng băm. Trong 15 `r11_*`: **9 tương đương**, **6 còn phải GIET**; từng ID/proof ở `pairs11_projection.json`. Thay ký hiệu regex không đủ cho `CHOT_DA_BO`. Luật 9 không hạ mức lỗi hành vi của mã gốc thành P3; P3 ngoài bảng vẫn cần đóng hoặc miễn neo exact SHA.

**Tác động dữ liệu thật tại base `8048551a9b1eb886c126d2a1a4df0f95fb285964`:**

- **66** tệp: giữ **47 passed / 10 failed / 9 not_measured**, 0 delta cả trạng thái lẫn lý do.
- **170** hồ sơ: giữ **25 miễn cutover / 56 đỏ / 39 đạt / 50 không lời khai**, 0 delta; landed 94→94.
- **2.504** URL trong bản ghi thụ động, **1.797** URL sau decode **2.812** JSON readback: 0 ngoài lớp mới. URL không khớp duy nhất khi quét mọi tệp là template `{PR_GHI_SO}` trong mã nháp, không phải hồ sơ/readback thật.

**Số liệu:** 30 ca sàn, 9 luật, 50 m-ID; 125 ô và bốn hash fixture khớp. Numstat r11 **1+343+1641=1985**; trần đề nghị giữ **2100**, dự toán r12 **1950–2080** khai là ước. Chưa có số đo mã r12.

Các lệnh đo cuối đều rc=0 và có positive evidence trong `da_do_khop`. Hai lỗi dựng probe đã sửa được ghi riêng, không tính là finding sản phẩm. Không chạy full suite mã r12, `do/HOAN_TAT`, CI hoặc Windows; chưa có implementation r12 và đây là review đặc tả. Bản projection chỉ dùng đo tác động. Chủ kho vẫn cần duyệt hash r12 theo E5; verdict không cấp quyền thi công hoặc merge.

Validator: **HOP_LE (§8.3): 0 finding, 3 lop** (`rc=0`, `kiem_verdict.txt`). Snapshot đầu/cuối khớp HEAD/tree, tracked bytes, index, untracked và ignored.

KET_LUAN: approve
