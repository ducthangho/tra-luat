# wp1463 (PR2) — kết quả đo, attempt 1 của lease `wp1463-r11-g1-claude`

Trạng thái: **DỪNG theo protocol §12** ở việc ĐẦU TIÊN (SPEC r11, đoạn "Vùng trước lease (revision 10)"). Lần chạy sớm của
`vung` ra `KHONG_DO_DUOC`, nên chưa có mã nào khác: `ops/ci_provenance_test.py` còn nguyên blob base; `ab`, `registry`,
`tu-kiem`, `tu-kiem --dot-bien` CHƯA hiện thực và CHƯA có đầu ra. Tệp này chỉ ghi phép đo của lần chạy sớm.

Điều kiện đo: 2026-11-26 03:09Z–03:32Z, phiên cloud Linux, 4 CPU, Python 3.13.18, có `actionlint` và `shellcheck`.
Cây đo: clone cục bộ của base `4a96ccd2774b67406b8cd4110f7e574cfa82bc6d` cộng ĐÚNG bốn thay đổi dữ liệu mục 3
(`core.abbrev 7`). Tệp đã chạy:
- `ops/ci_provenance_test.py` sha256 `e381a5974537c413ffa1f908c7bf87b5c78f3f18b14870c8b97f44302cbcbd51` (blob base, chưa sửa)
- `.claude/dev/ci_dang_ky_test.py` sha256 `92516f3f45fef47bfee810a26f53bd1f36724af0cd0d0e0a95ab629b6cc834d2`

Trong lúc đo, máy còn chạy song song một probe và ba lời gọi `phan_chung()` khác của chính phiên này, nên số giây dưới đây
là số có tải, không phải số sạch.

## 1. `do_pr2.py vung` (lần chạy sớm) — `KET_LUAN_VUNG: KHONG_DO_DUOC`, rc 3

```
PHEP bo_day_du: SACH · rc=0 · (1) khac rong=True · (2) nhan chung ops/ci_provenance.py=True · (3) ngoai vung=[] · Python con/dong khoi dong=562/563
  tap (5): ['.claude/dev/ci_dang_ky_test.py', '.github/workflows/ops-do-workflow-definition.yml', 'ops/bash_nen.py', 'ops/ci_provenance.py', 'ops/ci_provenance_test.py']
  khoi cuoi: ['CA: 77/77 dat', 'DOT BIEN: 485/485 bi giet dung ly do', 'TU KIEM PHAN HANG: DAT (2 dot bien)', 'TONG: DAT']
PHEP phan_chung_nguyen: KHONG_DO_DUOC · rc=0 · (1) khac rong=True · (2) nhan chung .github/workflows/ci.yml=True · (3) ngoai vung=[] · Python con/dong khoi dong=79/92
  tap (7): ['.claude/dev/ci_dang_ky_test.py', '.github/workflows/ci-dot-bien-du.yml', '.github/workflows/ci.yml', '.github/workflows/launcher-windows.yml', 'ops/bash_nen.py', 'ops/specs/wp1460-r1/hop_dong/bien_nhan_audit.v1.schema.json', 'ops/specs/wp1460-r1/hop_dong/fixture.json']
  danh tinh: che_do=nguyen truoc={NHE, MAU_DAY_DU, MAU_NHE, VUNG_THEM: True; so_vung_them: 7} sau=(như trước) phan_chung=True hang=30/30
  KHONG DO DUOC: Python con khong co hook: pid 3662: sinh 2 Python con [python3 -c "import time;time.sleep(60)"], chi 1 dong khoi dong co PID cha ay ·
                 pid 3703: sinh 1, chi 0 · pid 3705: sinh 1, chi 0
PHEP phan_chung_go_bon_khoa: KHONG_DO_DUOC · rc=0 · (1) khac rong=True · (2) nhan chung .github/workflows/ci.yml=True · (3) ngoai vung=[] · Python con/dong khoi dong=79/92
  tap (7): (đúng bảy tệp như phép trên)
  danh tinh: che_do=go_bon_khoa truoc={bốn khoá: True; so_vung_them: 7} sau={bốn khoá: False; so_vung_them: 0} phan_chung=True hang=30/30
  KHONG DO DUOC: Python con khong co hook: pid 4234: sinh 2 ..., chi 1 · pid 4273: sinh 1, chi 0 · pid 4275: sinh 1, chi 0
KET_LUAN_VUNG: KHONG_DO_DUOC
```

(Các dòng trên rút gọn phần lặp; bản nguyên văn nằm ngoài kho, trong thư mục nháp của phiên executor.)

Đọc kết quả:
- **Không có tệp nào ngoài vùng** ở cả ba phép. Hai probe mở đúng bảy tệp như mốc `d0868db` của đặc tả; lượt đủ mở năm tệp.
  Điều kiện (1), (2), (3) đạt ở cả ba phép; bảng 30 hàng khớp `ke_hoach` thật; dấu vết danh tính đúng từng chế độ.
- **Cả hai probe không đo được ở chốt "Độ phủ quan sát" của revision 11** (đối chiếu Python con với dòng khởi động hook THEO
  TỪNG tiến trình sinh).

## 2. Vì sao hai probe không đo được — nguyên nhân nằm trong `phan_chung()`, không ở vùng

Bản `vung` này đối chiếu chặt hơn chữ đặc tả (theo cặp PID cha và argv). Để khỏi kết luận từ luật của riêng nó, một lượt
`phan_chung_nguyen` thứ hai được chạy giữ nhật ký và đối chiếu bằng ĐÚNG phép đếm của đặc tả ("số Python con mà P sinh
trực tiếp ≤ số dòng khởi động có PID cha = P"):

```
tong Python con 79 tong dong khoi dong 92
THIEU o P=19127 (python3 -c import subprocess as s,sys;print(s.Popen([sy…): sinh 1, dong khoi dong co PID cha = P: 0
    sinh: python3 -c import time;time.sleep(60)
THIEU o P=19129 (python3 -c import subprocess as s,sys;print(s.Popen([sy…): sinh 1, dong khoi dong co PID cha = P: 0
    sinh: python3 -c import time;time.sleep(60)
```

Hai tiến trình sinh ấy là hai phản chứng CÓ SẴN của registry, `p637-A3c-con-chau-song-sau-khi-bo-thoat-la-do` và
`p637-A3c-chau-setsid-thoat-nhom-van-bi-bat` (`.claude/dev/ci_dang_ky_test.py`, khối `if os.name != "nt"` của A3c): mỗi cái
khởi một Python trung gian, Python ấy sinh một Python cháu `time.sleep(60)` rồi thoát NGAY. Khi hook của cháu khởi động thì
cha nó đã chết, nên `os.getppid()` không còn là P (hoặc cháu bị giết trước khi hook kịp ghi). Luật revision 11 nói thẳng
trường hợp này là không đo được ("thiếu ở bất kỳ P nào ⇒ phép ấy KHÔNG ĐO ĐƯỢC"; dòng của tiến trình khác không được bù).
Với phép đếm GỘP của revision 9 thì 92 ≥ 79 và phép qua — đó là số (79, 91) đặc tả ghi ở mốc `d0868db`.

Lặp lại được: 5/5 lượt probe trong phiên (hai lượt thử trước lần chạy sớm, hai chế độ của lần chạy sớm, một lượt giữ nhật ký)
đều thiếu ở đúng hai tiến trình sinh ấy. Cùng nền ấy còn một Python con thứ ba không bao giờ có dòng khởi động: lời gọi
`_chay_co_lap([... "time.sleep(60)"], gioi_han="x")` bị giết ngay; phép đếm theo P không lộ nó vì dòng khởi động khác có
cùng PID cha bù vào, phép đối chiếu theo argv thì lộ ("sinh 2 … chi 1").

KHÔNG ĐO ĐƯỢC ở đây: cháu ấy bị mồ côi hay bị giết trước khi hook chạy (nhật ký không phân biệt hai trường hợp).

## 3. Số đo thứ hai, liên quan K8: `phan_chung()` nay mất khoảng 5 phút một lời gọi

Đo trên cây làm việc (base + bốn thay đổi dữ liệu), KHÔNG hook, một tiến trình, nạp registry với `__file__` là tệp thật rồi
`del` khoá tại chỗ như K8 mô tả:

| khoá đã gỡ | `phan_chung()` | giây (có tải) | kiểm lọt |
|---|---|---|---|
| `NHE`, `MAU_DAY_DU`, `MAU_NHE`, `VUNG_THEM` | `True`, `PHẢN CHỨNG: 1677/1677 đỏ đúng` | 291,9 | (không) |
| chỉ `NHE` | `False`, 1675/1677 | 331,1 | `p643-A1-chi-bo-trong-NHE`, `p647-M2-mau-nhe-chi-cho-bo-trong-NHE` |
| `NHE`, `MAU_NHE` | `False`, 1676/1677 | 309,7 | `p643-A1-chi-bo-trong-NHE` |

Ba vế của K8 cho đúng kết quả đặc tả mô tả. Nhưng đặc tả ghi "≈ 8 s" cho một lời gọi (đo ở `e2f28fb`); sau B1a, kiểm
`wp1460-hop-dong-lenh-kiem-480-va-dot-bien-249` chạy một tiến trình con `lenh_kiem_hop_dong.py --dot-bien` chiếm gần trọn
thời gian ấy (thấy nó ở 99 % CPU sau 170 s). Hệ quả chưa được đặc tả tính tới: ca K8 cần ba lời gọi (≈ 15 phút có tải), trong
khi `chay_con`/`chay_con_ban_test` giới hạn MỖI ca 300 s, và ca nền chạy ở CẢ lượt nhẹ.

## 4. Chưa đo

- Nghiệm thu 1, 2, 3, 5, 6, 7 và `tu-kiem`: chưa có hiện thực nên chưa có số.
- `python .claude/dev/ci_dang_ky_test.py` (`TỔNG`) trên base + bốn thay đổi dữ liệu: chưa chạy trọn; chỉ có `phan_chung()` trả
  `True` ở bản nạp nguyên (probe) và ở bản đã gỡ bốn khoá.
- Thời gian `phan_chung()` trên máy không tải.
