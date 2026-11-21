# CAI-APT-BACKOFF r1: `cai_cong_cu.sh` thử lại apt tối đa 3 lần có giãn cách (đặc tả đóng băng)

- **Packet:** #1479. Revision 1, generation 1. Role `executor` (Claude), Review Class `sensitive`. Lý do `sensitive`: `cai_cong_cu.sh` là
  bước cài của 4 job CI và của hook phiên; một lỗi ở đây làm đỏ hoặc treo mọi gate.
- **Căn cứ:** Issue #1479, có số đo: 5/500 lượt `ci.yml` từ 01-11 phải chạy lại, cả 5 đỏ gốc ở bước "cài rg cho G5" vì mirror
  `security.ubuntu.com` sập vài phút; nhánh thử lại 1 lần tức thì của wp1404 cũng hỏng. Chủ kho, ngày 21-11-2026:
  *"Đồng ý, mở packet retry backoff cho cai_cong_cu.sh"*.

## 1. Hành vi
Áp cho đúng nhánh thử lại hiện có: lần cài đầu lỗi (`RC_CAI ≠ 0`) VÀ `LENH` chứa `apt-get install`. Công thức không phải apt thì
giữ nguyên (không thử lại).
1. **Số lần:** thử lại tối đa `N` lần, mặc định **3**. Tổng số lần cài tối đa là `N + 1`. Dừng ngay ở lần đầu tiên `RC_CAI = 0`.
2. **Giãn cách:** trước lần thử lại thứ `k` (1-based) chờ `CHO × 2^(k−1)` giây, `CHO` mặc định **15** ⇒ 15 s, 30 s, 60 s.
3. **Mỗi lần thử lại** giữ đúng các chốt wp1404:
   - in ĐÚNG MỘT dòng lên stderr: `cai_cong_cu: '<TEN>' cai loi (rc=<rc lần vừa hỏng>); cho <s>s, apt-get update roi thu lai lan <k>/<N>`;
   - `sleep <s>`, rồi `apt-get update -qq` qua `sudo` nếu `LENH` bắt đầu bằng `sudo apt-get`, gọi thẳng nếu không. stdout của
     update đi sang stderr. Update lỗi thì in dòng bỏ qua và vẫn thử lại;
   - kênh kết quả MỚI cho lần ấy (`$TAM_CAI/kq-thu-lai-<k>`, `export -n`, tạo rỗng), xoá `$TAM_CAI/stdout`;
   - chạy lại `_wp1404_chay_cong_thuc "$@"`.
4. **Mã thoát** là mã của lần cài CUỐI CÙNG. Các nhánh sau đó (bat_buoc:false trong `--bat-buoc`, đọc kênh, kiểm cuối) giữ nguyên.
5. **Biến điều chỉnh** (đọc từ môi trường, để test rút ngắn và để người gọi chọn):
   - `CAI_CONG_CU_THU_LAI`: số lần thử lại, 0..9;
   - `CAI_CONG_CU_CHO_GIAY`: giây chờ cơ sở, 0..600.
   Giá trị không phải số nguyên thập phân, có quá 3 chữ số, hoặc ngoài khoảng ⇒ dùng mặc định. Phải ép thập phân (`10#`), vì
   `08` là lỗi số bát phân trong `$(( ))` và làm chết script (bài học #1474 F1474-05).
6. **Không để biến lọt ra shell gọi:** lượt `source` của `--bat-buoc` chạy script trong shell CHA. Vòng thử lại phải nằm trong
   một HÀM dùng `local`, tên biến có tiền tố riêng (`_tl1479_`), để không đụng biến của shell gọi (kể cả biến `readonly`: ca (g)
   của `r1404_thu_lai_chot_chi_tiet`).

## 2. Ngoài phạm vi
- Thử lại ở tầng kết quả test: không làm.
- Phân loại lỗi theo stderr của apt: không làm ở r1. Stderr của trình cài đi thẳng ra stderr của script; muốn bắt nó phải đổi
  luồng ra, sẽ đụng các chốt kênh/stdout của wp868. Mọi lỗi apt đều được thử lại như wp1404 đang làm.
- Không sửa `ops/cong_cu.yaml`, `ops/cong_cu.py`, `ci.yml`, `ops/cong_cu_test.py` (lease `wp1448-r4-g4-claude` đang giữ tệp này).
  Đã đo: các fixture của tệp này dùng công thức không qua apt, và các đột biến `t5_thoat_som`, `t23_bo_cat_CR_ten_cong_cu` neo
  vào dòng nằm ngoài nhánh thử lại.
- Hook phiên (`cong-cu-ban-ke`, #1474) cắt mỗi lần cài ở 180 s. Lỗi apt kéo dài sẽ bị cắt trước khi hết 3 lần (15+30+60 = 105 s
  chờ, cộng thời gian cài). Chấp nhận; lần đo lại của hook sẽ báo `CHUA DAT`.

## 3. Test (`.claude/dev/launcher_test.py`)
Bộ đồ giả mặc định đặt `CAI_CONG_CU_CHO_GIAY=0`, để các ca cũ không ngủ thật. Đặt ở các helper chạy `cai_cong_cu.sh`
(`_wp831_chay_cai_rg`, `_wp868_chay`) hoặc ở `_wp802_bash_env`. Cập nhật các kỳ vọng cũ "đúng một lần thử lại" thành hành vi mới.
Ít nhất các ca:
1. Lỗi đến lần cài thứ 3, lần 4 được ⇒ rc 0, nhật ký apt `install,update,install,update,install,update,install`, ba dòng báo
   thử lại `1/3`, `2/3`, `3/3`.
2. Luôn lỗi ⇒ đúng 3 lần thử lại (4 lần install), rc = rc của lần cuối (lần cuối trả mã KHÁC các lần trước để phân biệt).
3. Được ngay ⇒ 0 update, 0 dòng thử lại.
4. Giãn cách: một `sleep` giả ghi đối số (chỉ đặt trong ca này) ⇒ `15 30 60` khi mặc định; `CAI_CONG_CU_CHO_GIAY=2` ⇒ `2 4 8`.
5. `CAI_CONG_CU_THU_LAI=1` ⇒ đúng 1 lần thử lại. `=0` ⇒ không thử lại.
6. Biến hỏng (`abc`, `08`, `1234`, rỗng) ⇒ dùng mặc định. Riêng `08` cho `CHO_GIAY` ⇒ 8, không chết script.
7. Công thức không phải apt (brew) lỗi ⇒ không `apt-get`, không `sleep`.
8. Các chốt wp1404 cũ (ca `r1404_thu_lai_chot_chi_tiet` (a)–(i)) vẫn đạt với hành vi mới: kênh mới mỗi lần, stdout mới, `sudo` đúng
   nhánh, `source` từ shell có `readonly`, allexport.

Đột biến (bảng `DOT_BIEN_HOOK`, đích `cai_sh`). Mỗi đột biến làm đỏ đúng ca đích:
- bỏ giãn cách;
- giãn cách hằng số (không nhân đôi);
- số lần thử lại cố định 1;
- thử lại cả khi lần trước đã được;
- bỏ `10#`;
- bỏ kiểm khoảng;
- kênh dùng chung cho mọi lần thử lại;
- bỏ `local`, để biến lọt ra shell gọi.
Các đột biến `wp1404_sh_*` cũ mất neo thì neo lại vào cấu trúc mới, không xoá.

Chạy tại chỗ: các ca `r1404_*`, `r858_*`, `r868_*`, `r831_*` (đi qua `cai_cong_cu.sh`), cả bộ `launcher_test.py`,
`ops/cong_cu_test.py` (chỉ đọc, xác nhận không hồi quy), `shellcheck`, `bash -n`.

## 4. Review và CI
- Codex offline qua `launcher.py run`, tối đa 2 lời gọi. P0–P2 chặn merge. Thêm connector Codex trên PR.
- CI của PR (đổi `ops/cai_*` kích hoạt `gate-cong-cu` đủ bán kính). Không gọi Windows CI.

## 5. Write set (không glob)
- `ops/cai_cong_cu.sh`
- `.claude/dev/launcher_test.py`
- `ops/specs/cai-apt-backoff-r1.md`
- `ops/leases/cai-apt-backoff-r1-g1-claude.yaml`
- `ops/acceptance/cai-apt-backoff/r1/VERDICT.md`
