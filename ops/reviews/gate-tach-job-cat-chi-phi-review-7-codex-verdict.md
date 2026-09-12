verdict: changes_requested
P1: 0
P2: 4
P3: 1

Review đã hoàn tất; các khối dưới đây được giữ theo thứ tự ghi tăng dần trong lúc đo.

Kết quả: **changes_requested**, 9 hướng săn, 5 lớp finding (4 P2, 1 P3). Hai lớp ops phải đi packet riêng. Đối chiếu A: VÁ SINH LỖI MỚI; B/C: chưa chứng nhận vá trọn trên head; D: ĐÃ VÁ THẬT trong r19; E: CHƯA VÁ.

## Neo và phép đo nền

reviewed_sha: 201bd7a46a948f9ed0a4cb51263f9f236bf5a5d7
reviewed_tree: 1949403d2a76ea6b96d7a0b255a44af1c1dc1cd6
provider: openai_codex; execution_surface: Codex service; transport: machine; vai trò: reviewer độc lập.
model: GPT-6 theo chỉ dẫn phiên; exact model ID/effort không có phép tự xác minh qua tool. Lease yêu cầu gpt-6-astra/xhigh là ý định được ghi trong gói, không được dùng thay receipt danh tính thực tế.

`python .claude/dev/ci_dang_ky_test.py`: rc=0; PHẢN CHỨNG: 91/91 đỏ đúng
TỔNG: ĐẠT

`ruff check --select F .claude/dev/ci_dang_ky_test.py`: All checks passed!

`git diff --numstat origin/master...HEAD`: 284	88	.claude/dev/ci_dang_ky_test.py; 154	6	.github/workflows/ci.yml;  ⇒ 2 đường dẫn, 438 additions, hơn trần 430 đúng 8; chốt A8 ở chủ kho, không là finding chất lượng mã.

SHA256 r19: `c9d3f716fe4c737963a0e8164b6f3e42cac13c986ac55ed818e8044190a5b531`; khớp lease. Log nền đầy đủ: `do-review/logs/`; dữ liệu: `do-review/baseline.json`.
A1/A5: KHÔNG ĐO ĐƯỢC theo lệnh cấm CI. Không dùng doc-claims-check sandbox để chứng nhận kho thật.

## ĐỐI CHIẾU LƯỢT TRƯỚC

### LỚP A

VÁ SINH LỖI MỚI — các ca cấm có sẵn bị chặn; 10 phép bỏ phần tử đều siết cổng và bị chiều NHẬN bắt. Nhưng lời gọi hợp lệ `python -m ruff --version` bị coi là cài đặt không phân tích được, làm CI đủ pin/probe/registry vẫn đỏ. Chiều cấm ngoài khuôn shell chưa được chứng minh đóng hết.

Lệnh: `python do-review/review_lop.py A`

Output tự đo:
```text
pin ('GHIM', 'python -m pip install ruff==0.15.15')
cli ('KHONG', None)
module ('KHONG_PHAN_TICH_DUOC', 'python -m ruff --version')
CMD: python -m ruff --version 
rc= 0
ruff 0.15.15
pin/probe/registry intact + module diagnostic: (["CI không ghim Ruff 0.15.15 (job: ['gate-registry'])"], 3)
remove _TIEN_TO_CAI ['pip'] => KHONG_PHAN_TICH_DUOC phan_chung= False failed= ['nhan-tien-to-pip', 'tap-tien-to-khop-ky-vong']
remove _TIEN_TO_CAI ['pip3'] => KHONG_PHAN_TICH_DUOC phan_chung= False failed= ['nhan-tien-to-pip3', 'tap-tien-to-khop-ky-vong']
remove _TIEN_TO_CAI ['python', '-m', 'pip'] => KHONG_PHAN_TICH_DUOC phan_chung= False failed= ['nhan-ghim-chuan', 'nhan-tuy-chon-quiet', 'nhan-tuy-chon-q', 'nhan-tuy-chon-no-cache-dir', 'nhan-tuy-chon-disable-pip-version-check', 'nhan-tuy-chon-no-input', 'nhan-ten-hoa-thuong', 'nhan-extras', 'nhan-noi-dong', 'nhan-khong-ghim', 'nhan-toan-tu-lon-hon', 'nhan-toan-tu-la', 'nhan-extras-khong-ghim', 'tap-tien-to-khop-ky-vong', 'ruff-ci-chua-tach-tuong-thich-lui', 'ruff-ci-da-tach-dung']
remove _TIEN_TO_CAI ['python3', '-m', 'pip'] => KHONG_PHAN_TICH_DUOC phan_chung= False failed= ['nhan-tien-to-python3', 'tap-tien-to-khop-ky-vong']
remove _TIEN_TO_CAI ['uv', 'pip'] => KHONG_PHAN_TICH_DUOC phan_chung= False failed= ['nhan-tien-to-uv-pip', 'tap-tien-to-khop-ky-vong']
remove _TUY_CHON_AN_TOAN '--disable-pip-version-check' => KHONG_PHAN_TICH_DUOC phan_chung= False failed= ['nhan-tuy-chon-disable-pip-version-check', 'tap-tuy-chon-khop-ky-vong']
remove _TUY_CHON_AN_TOAN '--no-cache-dir' => KHONG_PHAN_TICH_DUOC phan_chung= False failed= ['nhan-tuy-chon-no-cache-dir', 'tap-tuy-chon-khop-ky-vong']
remove _TUY_CHON_AN_TOAN '--no-input' => KHONG_PHAN_TICH_DUOC phan_chung= False failed= ['nhan-tuy-chon-no-input', 'tap-tuy-chon-khop-ky-vong']
remove _TUY_CHON_AN_TOAN '--quiet' => KHONG_PHAN_TICH_DUOC phan_chung= False failed= ['nhan-tuy-chon-quiet', 'tap-tuy-chon-khop-ky-vong', 'ruff-ci-chua-tach-tuong-thich-lui', 'ruff-ci-da-tach-dung']
remove _TUY_CHON_AN_TOAN '-q' => KHONG_PHAN_TICH_DUOC phan_chung= False failed= ['nhan-tuy-chon-q', 'tap-tuy-chon-khop-ky-vong']
existing negative/positive fixtures: True PHẢN CHỨNG: 91/91 đỏ đúng
```

### LỚP B

CHƯA VÁ trên reviewed_sha — công cụ và commit sửa không nằm trên nhánh. Đo bổ sung e7a271b từ mirror: t10 chặn đúng; tệp vẫn tự khai chỉ kiểm một mẫu Markdown, không chứng minh chỉ có một nghĩa vụ trần. Khai giới hạn không đồng nghĩa đóng gốc regex.

Lệnh: `python do-review/review_lop.py B`

Output tự đo:
```text
CMD: git merge-base --is-ancestor e7a271b HEAD 
rc= 1

CMD: git cat-file -e HEAD:ops/kiem_hop_dong_packet.py 
rc= 128
fatal: path 'ops/kiem_hop_dong_packet.py' does not exist in 'HEAD'
CMD: git branch -a --contains e7a271b 
rc= 0
  remotes/origin/ops/cap-lease-463
CMD: python /tmp/claude-0/-home-user-tra-luat/d706aae3-d737-5ec6-8390-ae296d24c1a2/scratchpad/rv463b/do-review/bo-hop-dong/kiem_hop_dong_packet_test.py 
rc= 0
ĐẠT   t1-cap-khop-phai-DAT                         rc=0 (mong 0)
ĐẠT   t2-revision-truong-lech-tieu-de              rc=2 (mong 2)
ĐẠT   t3-dac-ta-neu-tran-HAI-lan                   rc=3 (mong 3)
ĐẠT   t4-lease-CHEP-nguong-vao-muc-A8              rc=4 (mong 4)
ĐẠT   t5-spec_hash-khong-khop                      rc=5 (mong 5)
ĐẠT   t6-thieu-truong-revision-o-lease             rc=6 (mong 6)
ĐẠT   t8-dinh-danh-ADR-KHONG-bi-bat                rc=0 (mong 0)
ĐẠT   t9-ADR-tha-nhung-nguong-cung-muc-VAN-bi-bat  rc=4 (mong 4)
ĐẠT   t10-tham-chieu-cung-so-voi-nguong            rc=4 (mong 4)
ĐẠT   t11-vi-pham-CHI-o-dieu_kien_dung             rc=4 (mong 4)
ĐẠT   t7-tham-chieu-trong-muc-A8-KHONG-bi-bat      rc=0 (mong 0)
ĐẠT   dot-bien-noi-danh-sach-CHO-PHEP              rc=0 (nới danh sách ⇒ t4 phải THÔI đỏ; nếu vẫn 4 thì t4 đang đo thứ khác)
ĐẠT   dot-bien-bo-khoi-nghia-vu                    rc=4 (bo mot khoi ⇒ chot 5 phai CHAN [4])

PHẢN CHỨNG CỔNG: 13/13 đạt
CMD: python /tmp/claude-0/-home-user-tra-luat/d706aae3-d737-5ec6-8390-ae296d24c1a2/scratchpad/rv463b/do-review/bo-hop-dong/kiem_hop_dong_packet.py --spec /tmp/claude-0/-home-user-tra-luat/d706aae3-d737-5ec6-8390-ae296d24c1a2/scratchpad/rv463b/tai-lieu/SPEC-r19.md --lease /tmp/claude-0/-home-user-tra-luat/d706aae3-d737-5ec6-8390-ae296d24c1a2/scratchpad/rv463b/tai-lieu/LEASE-exec-2r8.yaml --nghiem-ngat 
rc= 0
DAT: SPEC-r19.md + LEASE-exec-2r8.yaml — 0 chot bo qua, phan con lai khop
GIOI HAN: chot 2 dem DUNG MOT mau Markdown; mot nghia vu tran viet khac cach (vd "Cot additions khong duoc vuot 400 dong.") KHONG duoc dem. Day la kiem DINH DANG, KHONG phai bang chung 'dac ta chi co mot nghia vu tran'.
```

### LỚP C

CHƯA VÁ trọn lớp trên reviewed_sha — cổng hợp đồng không có trên head. Bản phụ e7a271b bắt cả hai phép bỏ khối; không tìm thấy runner/trạng thái GIET O GATE NEN để đo lại F07: KHÔNG ĐO ĐƯỢC nhánh này.

Lệnh: `python do-review/review_lop.py C`

Output tự đo:
```text
CMD: git cat-file -e HEAD:ops/kiem_hop_dong_packet_test.py 
rc= 128
fatal: path 'ops/kiem_hop_dong_packet_test.py' does not exist in 'HEAD'
supplementary branch, original: ([], [])
remove viec_trong_lease ([(4, "KHOI_NGHIA_VU ('dieu_kien_dung',) lech ky vong ('viec_trong_lease', 'dieu_kien_dung')")], [])
remove dieu_kien_dung ([(4, "KHOI_NGHIA_VU ('viec_trong_lease',) lech ky vong ('viec_trong_lease', 'dieu_kien_dung')")], [])
runner literal GIET O GATE NEN in snapshot: []
```

### LỚP D

ĐÃ VÁ THẬT trong hợp đồng r19 — ngân sách giữ trần N=2, phân bổ tại A1; A2=2×2=4, A5=1×2=2, tổng 6. Bản r12 trong cây không dùng để phủ nhận bản sửa được ghim bằng hash.

Lệnh: `python do-review/review_lop.py D`

Output tự đo:
```text
sha256= c9d3f716fe4c737963a0e8164b6f3e42cac13c986ac55ed818e8044190a5b531
SPEC-r19.md 210 228
210: bắt đúng chỗ đó — cùng lớp "nhắc lại một hằng số ở hai chỗ" mà r17 đã đóng cho trần `A8`.)*
211: Mỗi lần chi ghi `run_id` vào biên nhận. **Vượt `N` ⇒ revision**, không tự chi thêm. Lượt `pull_request` tự bắn là
212: **cổng**, không tính vào `N`. **Cấm tuyệt đối lượt "chạy thử xem sao".**
213: Căn cứ: G8 — **965,10** phút tính tiền (**48,3 %** hạn mức tháng) bị **8** lượt `cancelled` tiêu mà
214: **không lượt nào cho một kết quả hoàn tất hợp lệ**. *(Nói vậy chứ không nói "thu 0 thông tin":
215: chính các bước bị cắt đang được dùng làm chẩn đoán trong đặc tả này.)*
216: 
217: **Điều kiện dừng (chỉ thị chủ kho 11-09-2026).** `review_class = sensitive` ⇒ packet chỉ đóng khi
218: cross-review **`approve`** tường minh. **"0 P1 + 0 P2" KHÔNG đủ**: *"vắng mặt vì sạch"* và *"vắng mặt
219: vì chưa nhìn tới"* nhìn giống hệt nhau, `approve` mới phân biệt được.
220: **Chống lách:** một vòng làm finding biến mất bằng cách **thu hẹp phạm vi** phải khai thẳng — thu hẹp
221: phạm vi là một mục `chua_do_duoc`, **không** phải một bản vá.
222: 
223: ---
224: 
225: **A1 (M1) — job dài nhất giảm, đo bằng PHÚT TƯỜNG CỦA JOB.**
226: Đòi `max(thời lượng job)` trên `windows-latest` **≤ 0,60 × `timeout-minutes`** — hôm nay
227: `timeout-minutes: 60` ⇒ **≤ 36,00 phút**.
228: 
SPEC-r19.md 267 281
267: mọi bước tiền nhiệm đều xanh**. Ngoài miền ấy hành vi **CÓ ĐỔI**, và đổi có lợi lẫn có hại: `success()`
268: ngầm phụ thuộc các bước trước **trong cùng job**, mà `packet-loop selftest` mất **3** tiền nhiệm và
269: `test registry` mất **5** khi dời sang job riêng. Nếu `codex credential selftest` đỏ thì **trước** tách
270: cả hai bị `skipped`, **sau** tách hai job độc lập vẫn chạy. Đó là **thay đổi hợp đồng**, không phải
271: bypass: cổng tổng vẫn có job đỏ. Khai thẳng ở đây để không ai đọc *"độ phủ không đổi"* rộng hơn phép
272: đo. Ca khoá bắt buộc: **một tiền nhiệm đỏ** cùng **đối chứng mọi tiền nhiệm xanh**.
273: Lấy `(job, tên bước, nền, conclusion)` của lượt TRƯỚC và lượt SAU; **bỏ cột `job`**, so **tập**
274: `(tên bước, nền, conclusion)`. Hai tập phải **bằng nhau**. Làm HAI lần:
275: 
276: - **lane `workflow_dispatch` — CÓ ĐIỀU KIỆN, vì nền của nó là nền `KHÔNG ĐO ĐƯỢC` của `A1`.**
277:   Lượt SAU tách (cả hai nền) so lượt TRƯỚC tách trên CÙNG nhánh tại `start_from_sha`. Lượt SAU là
278:   lượt `A1` đã chi; lượt TRƯỚC **không được chi thêm** — job Windows tiền-tách chạm trần nên nó
279:   không cho một nền hợp lệ (xem `A1`). Không có nền dispatch ⇒ lane này đi **nhánh nền KHÔNG hợp
280:   lệ** ở dưới, trạng thái `ĐẠT CÓ ĐIỀU KIỆN`; **không** được ghi `ĐẠT` trơn.
281: - lượt `pull_request` của chính PR packet so lượt `pull_request` gần nhất mà `ci.yml` nền **BẰNG
SPEC-r19.md 485 505
485: **Chiều sai, khai cho đúng:** nền hụt làm **tỉ lệ tăng trông LỚN HƠN** thực, tức sai về phía **bất
486: lợi** cho packet. Điều đó không làm `r12` đúng trở lại; nó chỉ nói rủi ro nằm ở đâu.
487: 
488: **`A5` KHÔNG cấp nền cho `A1`.** Nền `A5` nay chỉ Ubuntu, nên nó không cho thời lượng
489: `windows-latest` cho bất kỳ nghĩa vụ nào của `A1`. Hai tiêu chí đo hai đại lượng trên hai lane; xem
490: `A1` cho ngưỡng tuyệt đối và cho nền `KHÔNG ĐO ĐƯỢC` của nó.
491: 
492: **(4) Ca âm phải nhắm một instance THỰC SỰ TỒN TẠI trên lane đang đo.** Ca âm bắt buộc của `A5(1)`
493: là *"bỏ một instance BẤT KỲ thuộc tập kỳ vọng CỦA CHÍNH LANE ẤY"* — trên lane PR đó là một job
494: ubuntu; trên lane dispatch, một job Windows. **Không** được ghi cứng *"bỏ một job Windows"*: trên
495: lane PR không nhãn `windows` có **0** job Windows nên phép ấy **không đổi dữ liệu**, tức không thể
496: làm tiêu chí đỏ. Đo được: PR `expected = 3`, bỏ Windows xoá **0** instance, `equality = True`; đối
497: chứng dispatch `expected = 6`, bỏ **1** ⇒ `equality = False`.
498: 
499: **(5) MỘT MANIFEST CHO MỖI `(tiêu chí, lane, trước/sau)` — `A2` và `A5` KHÔNG dùng chung.** Mỗi
500: manifest ghi `run_id`, `run_attempt`, tập job, SHA định nghĩa workflow. Ràng buộc *"cùng một mẫu"*
501: áp **trong** một ô ấy, **không** bắc cầu sang ô khác.
502: **Khoá đúng số ô, vì bản r15 đầu ghi *"`A2` đọc lane dispatch"* và như thế là bỏ mất nửa nghĩa vụ
503: của `A2`** (cross-review lượt 3 `R3-F04`): `A2` đo trên **CẢ HAI** lane (xem `A2`), `A5` chỉ lane PR.
504: **Số ô SUY TỪ CHIỀU, không khai rời:** `A2` = 2 lane × {trước, sau} = **4** ô (cặp dispatch có thể
505: `KHÔNG ĐO ĐƯỢC` theo `A1`); `A5` = 1 lane × {trước, sau} = **2** ô; tổng **6**. Một manifest dùng
A2 cells = 4 ; A5 cells = 2 ; total = 6
```

### LỚP E

CHƯA VÁ — EVIDENCE và commit khai 93/93, phép chạy thực tế là 91/91; tổng ĐẠT và số ca đúng là hai khẳng định khác nhau.

Lệnh: `python do-review/review_lop.py E`

Output tự đo:
```text
EVIDENCE claim: | `python .claude/dev/ci_dang_ky_test.py` | `TỔNG: ĐẠT` (phản chứng 93/93 theo commit message) |
actual named cases= 91 ; unique= 91
ĐĂNG KÝ: 21/21
RUFF CI: 3/3 hợp đồng
PHẢN CHỨNG: 91/91 đỏ đúng
TỔNG: ĐẠT
CMD: git show -s --format=%B HEAD 
rc= 0
fix(#463 LOP A): dao ba danh sach CAM thanh MOT khuon duoc cong nhan, fail-close

Cross-review luot 6 (verdict request-changes, reviewed 058c050): R6-F01 + R6-F02.
Gop hai finding ay lam MOT LOP, vi ca hai cung mot goc: bo phan loai la DANH SACH CAM
khop bang TOKEN, nen fail-open voi moi thu ngoai danh sach.

Do duoc truoc khi va — ca reviewer chi lan tu liet ke:
  --target=tmp · -ttmp · --prefix=tmp · --root=tmp · --python=tmp   -> GHIM   (R6-F01)
  --install-option=--prefix=/x                                       -> GHIM   (tu tim)
  pdm remove ruff · rye remove ruff · hatch env remove ruff          -> GHIM   (tu tim)
va 20 dot bien "bo mot phan tu khoi tap" song sot tren ba tap (_TOAN_TU 10 · dong tu 3 ·
tien to 5, cong 5+15 da bat o luot truoc).

VA THEO LOP, khong va tung cua: BO HAN ba tap cam. Nay mot dong cham `ruff` phai la
  (1) LOI GOI ruff (`ruff check .`), hoac
  (2) khuon `<tien to> install [<tuy chon an toan>...] ruff<rang buoc>`,
con lai deu KHONG_PHAN_TICH_DUOC. Hai danh sach con lai (`_TIEN_TO_CAI` 5,
`_TUY_CHON_AN_TOAN` 5) la CHO PHEP: bo mot phan tu lam cong CHAT hon, va ca bat no la
chieu NHAN — khac han danh sach cam, noi bo mot phan tu lam cong HO ma khong ca nao thay.
Khong con danh sach toan tu: ten goi tach bang ky tu ten PEP 508, phan con lai la rang buoc.

Kem mot lop nua tu do ra: ky vong cua fixture THO hon hanh vi no canh. Ca cu chi doi
`_loi >= 1` nen dot bien doi KHONG_PHAN_TICH_DUOC thanh KHONG_GHIM van xanh (`bo-chot-goi-khac`
song sot). Nay 31 ca di qua BANG NHAN, doi DUNG nhan phan loai.

BANG CHUNG DUONG:
- phan chung          93/93 do dung · TONG: DAT
- bang nhan           19/19 dat ca hai chieu (5 dang co cua R6-F01 · 3 trinh ngoai khuon ·
                      2 toan tu ngoai danh sach cu · 9 ca NHAN phai giu nguyen)
- dot bien lop A      11/11 giet · 0 song · 0 tin dung gia
                      (8 giet boi ca dich; 3 giet o GATE NEN — hop dong tren ci.yml THAT do,
                       main dung truoc phan_chung. Do la R6-F07: ban truoc dan nhan chung la
                       LOI VO CAN, tuc THIEU tin dung chu khong phai tin dung gia. Bo chay
                       nay co trang thai thu tu `GIET O GATE NEN`, phan biet bang
                       `RUFF CI: n/3` voi n<3 va KHONG co traceback.)
- ruff --select F     All checks passed

A8 = 439 dong them, VUOT tran 430 dung 9. CHUA DAY — dung va hoi chu kho theo luat cua
packet. Ghi commit de khong mat viec khi doi nhanh.

Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01UN8WRS5Bc5pBBzYPDqs9Dx
```

## BẢNG SĂN

Các hướng cũ chỉ dùng cho đối chiếu, không tính N: token cờ cài Ruff; động từ gỡ pdm/rye/hatch; PEP 440; bảng nhãn fixture; bỏ phần tử tập; regex văn xuôi; trạng thái GIET O GATE NEN; hằng số nhắc hai chỗ. Các hướng mới dưới đây ghi rõ biến thể và có probe/lệnh riêng. HƯỚNG 9 được bổ sung sau khi full suite làm lộ lỗi môi trường.

HƯỚNG 1: Thiếu Ruff sau tiền tố thiết lập: giá trị báo không tìm thấy
  giả thuyết : nếu mọi fixture thiếu Ruff đều đặt registry ở chỉ số 0 thì đổi giá trị không tìm thấy thành 0 vẫn xanh, dù bố cục thật lọt
  lệnh       : python do-review/san_moi.py 1
  output     :
```text
mutant: ruff_i default -1 -> 0; main rc= 0
RUFF CI: 3/3 hợp đồng
PHẢN CHỨNG: 91/91 đỏ đúng
TỔNG: ĐẠT
registry index after removing only install= 8
original on missing-install real layout: ["CI không provision Ruff trước test registry trong cùng job (job chạy test registry: ['gate-registry'])"]
mutant on missing-install real layout: []
prefix_count= 0 original= 1 mutant= 1
prefix_count= 1 original= 1 mutant= 0
prefix_count= 2 original= 1 mutant= 0
```
  kết luận   : LỖI

HƯỚNG 2: Thứ tự và phụ thuộc thiết lập khi dời hai bước sang job mới
  giả thuyết : nếu phép dời mất hoặc đảo một bước thiết lập thì cùng tập tên vẫn che được sai thứ tự/phụ thuộc
  lệnh       : python do-review/san_moi.py 2
  output     :
```text
before steps= 40 ; after per job= {'gate': 38, 'gate-registry': 10, 'gate-packet-loop': 10}
full 9-step prefix equal, including command/env/with/shell= True
gate-registry prefix= ['Force LF checkout (hash parity với manifest)', 'actions/checkout@v4', 'actions/setup-python@v5', 'cài PyYAML + jsonschema (cổng đăng lease + validator verdict cần)', 'cài actionlint cho G5', 'cài shellcheck cho G5 (cài xong đo lại)', 'cài rg cho G5 (cài xong đo lại)', 'G5 kiem ban ke cong cu + T1..T8 (packet', 'cài Ruff 0.15.15 và in probe dương'] ; tail= ['test registry (phạm vi + các bộ chưa được nối)']
gate-registry swap setup-python <-> pip prerequisite => False
gate-packet-loop prefix= ['Force LF checkout (hash parity với manifest)', 'actions/checkout@v4', 'actions/setup-python@v5', 'cài PyYAML + jsonschema (cổng đăng lease + validator verdict cần)', 'cài actionlint cho G5', 'cài shellcheck cho G5 (cài xong đo lại)', 'cài rg cho G5 (cài xong đo lại)', 'G5 kiem ban ke cong cu + T1..T8 (packet', 'cài Ruff 0.15.15 và in probe dương'] ; tail= ['packet-loop selftest']
gate-packet-loop swap setup-python <-> pip prerequisite => False
test registry (phạm vi + các bộ chưa được nối) before= 1 after= 1 all step fields equal= True
packet-loop selftest before= 1 after= 1 all step fields equal= True
remaining gate order/fields identical= True
```
  kết luận   : KHÔNG PHẢI LỖI

HƯỚNG 3: Ngữ cảnh matrix, if, env và runner của bước sau khi dời
  giả thuyết : nếu job mới chỉ chép lệnh mà mất ngữ cảnh thực thi thì phạm vi nền hoặc điều kiện chạy đổi
  lệnh       : python do-review/san_moi.py 3
  output     :
```text
complete job context equal (matrix, runner, env, timeout, no extra needs/defaults)= True
step name/if sets= 40 40 ; equal= True
workflow on/concurrency unchanged= True
mutate matrix => complete job context equal= False
mutate env => complete job context equal= False
mutate job-if => complete job context equal= False
gate-registry moved step if= None ; interpolation= False
gate-packet-loop moved step if= None ; interpolation= False
```
  kết luận   : KHÔNG PHẢI LỖI

HƯỚNG 4: Thứ tự probe và install bên trong cùng một run
  giả thuyết : nếu nhãn GHIM chỉ tổng hợp cả bước thì probe đặt trước install vẫn được tính là bằng chứng phiên bản vừa cài
  lệnh       : python do-review/san_moi.py 4
  output     :
```text
only reverse two existing lines in install step:
ruff --version
python -m pip install --quiet ruff==0.15.15
loi_ruff_ci= []
install_index= 1 ; probe_index= 0 ; probe follows installation= False
original order= ['python -m pip install --quiet ruff==0.15.15', 'ruff --version'] ; errors= []
```
  kết luận   : LỖI

HƯỚNG 5: Cấu hình pip qua env ngoài token lệnh
  giả thuyết : nếu chỉ kiểm argv thì PIP_TARGET ở bước/job/workflow đổi nơi cài mà cổng vẫn xác nhận provisioning
  lệnh       : python do-review/san_moi.py 5
  output     :
```text
PIP_TARGET at step => loi_ruff_ci= []
PIP_TARGET at job => loi_ruff_ci= []
PIP_TARGET at workflow => loi_ruff_ci= []
pip actual parser: target_dir= tmp-ruff-review ; requirement= ['ruff==0.15.15']
original workflow errors= []
```
  kết luận   : LỖI

HƯỚNG 6: Vòng đời kênh kết quả khi đo lại cùng một bản sao
  giả thuyết : nếu tên kênh chỉ theo số lần thử và writer append thì số đo cũ làm lần đo mới bị từ chối dù đầu vào không đổi
  lệnh       : python do-review/san_moi.py 6
  output     :
```text
same physical directory call 1 => ('GIET', '', 1)
same physical directory call 2 => ('GIET', '', 2)
same physical directory call 3 => ('KHONG_DO_DUOC', "ban ghi khong neo dung luot: T1 | rc_con=1 | stderr[-200:]=''", 2)
fresh directory control => ('GIET', '', 1)
channel lines= {'.ket-qua-2.jsonl': 18, '.ket-qua-1.jsonl': 27}
```
  kết luận   : LỖI

HƯỚNG 7: Xác thực kiểu qua writer và reader thật của nhanh_don_duoc
  giả thuyết : nếu dữ liệu mô tả có kiểu bất thường thì reader có thể cấp GIET hoặc ném ngoại lệ thay vì KHONG_DO_DUOC
  lệnh       : python do-review/san_moi.py 7
  output     :
```text
normal => ('GIET', '')
non-string-detail => ('KHONG_DO_DUOC', 'chi tiet khong phai chuoi cho ca T1')
unhashable-target => ('KHONG_DO_DUOC', "bo doc kenh nem TypeError: unhashable type: 'list'")
iterator-target => ('GIET', '')
numeric-target => ('KHONG_DO_DUOC', 'dich co ten ca KHONG ton tai: [1]')
```
  kết luận   : KHÔNG PHẢI LỖI

HƯỚNG 8: YAML hợp cú pháp nhưng sai cấu trúc tại biên consumer
  giả thuyết : nếu safe_load nhận scalar/list thì cổng có thể trả sạch vì lọc mất toàn bộ job/bước
  lệnh       : python do-review/san_moi.py 8
  output     :
```text
None => (['CI không ghim Ruff 0.15.15 (job: không job nào cài Ruff)', 'CI không in probe Ruff --version (job: không job nào cài Ruff)', 'CI không provision Ruff trước test registry trong cùng job (job chạy test registry: KHÔNG CÓ)'], 3)
[] => (['CI không ghim Ruff 0.15.15 (job: không job nào cài Ruff)', 'CI không in probe Ruff --version (job: không job nào cài Ruff)', 'CI không provision Ruff trước test registry trong cùng job (job chạy test registry: KHÔNG CÓ)'], 3)
1 => RAISE AttributeError 'int' object has no attribute 'get'
{'jobs': []} => (['CI không ghim Ruff 0.15.15 (job: không job nào cài Ruff)', 'CI không in probe Ruff --version (job: không job nào cài Ruff)', 'CI không provision Ruff trước test registry trong cùng job (job chạy test registry: KHÔNG CÓ)'], 3)
{'jobs': 1} => RAISE AttributeError 'int' object has no attribute 'items'
{'jobs': ['gate']} => RAISE AttributeError 'list' object has no attribute 'items'
{'jobs': {'gate': {'steps': 1}}} => RAISE TypeError 'int' object is not iterable
{'jobs': {'gate': {'steps': [None, 'run']}}} => (['CI không ghim Ruff 0.15.15 (job: không job nào cài Ruff)', 'CI không in probe Ruff --version (job: không job nào cài Ruff)', 'CI không provision Ruff trước test registry trong cùng job (job chạy test registry: KHÔNG CÓ)'], 3)
```
  kết luận   : KHÔNG PHẢI LỖI

## Chốt actionlint của A3 (không tính vào số hướng săn)

Cùng môi trường: actionlint 1.7.12, shellcheck 0.9.0. `actionlint -no-color -format '{{json .}}' do-review/actionlint/{before,after}.yml`: ci.yml trước/sau rc=0/0, hai đa tập chẩn đoán đều rỗng.

Phản chứng trên workflow có sẵn lỗi `ops-don-ref.yml`: bỏ dấu nháy ở đúng đối số của `test -n` có sẵn; không chạy workflow. Hai vế cùng rc=1; đa tập mới thêm: {('shellcheck', 'shellcheck reported issue in this script: SC2086:info:11:9: Double quote to prevent globbing and word splitting'): 1}. Vì sửa một đối số không dời dòng, chẩn đoán cũ giữ nguyên cả thân run; không cần loại số dòng mới so được. JSON đầy đủ ở `do-review/actionlint/`.

Bổ sung HƯỚNG 4 — không gọi pip/mạng vì shell dừng ngay lệnh đầu:
```text
H4 kiểm thứ tự với runner chưa có Ruff: PATH là thư mục trống, bash -e chạy hai dòng đảo từ workflow; rc=127
/bin/bash: line 1: ruff: command not found
```

## Đo riêng bộ nhanh_don_duoc trên bản đã land

Lệnh: `TMPDIR=<sandbox>/do-review/tmp python ops/nhanh_don_duoc_test.py` trong `cay-kho`. Chạy bộ test cục bộ có sẵn; các kho bare và commit/ref fixture đều nằm trong thư mục tạm của sandbox, không commit/push nhánh đang duyệt.

```text
nhanh_don_duoc_test.py full: rc=1, elapsed=261.189s
DOT BIEN TU KIEM tu-kiem-gop-hai-lop-ngoai-le | r516 | 1/1
DOT BIEN TU KIEM tu-kiem-bo-ghi-nhan-loi-vo-can | r516 | 1/1
TU KIEM co dot bien rieng: 23/23 nhom bat buoc · dot bien giet 74/76
8/8
MUTANT: giet = 10 · khong giet = 0 · khong do duoc = 0 / tong 10
```
Log đầy đủ: `do-review/logs/nhanh-full.log`.

## Thử hướng vá trên mô-đun/cây scratch

Lệnh: `python do-review/thu_va.py`. Không sửa nhánh packet.

```text
C: add existing _khac before _reg in missing-install fixture; rc= 0
PHẢN CHỨNG: 91/91 đỏ đúng
TỔNG: ĐẠT
C: same sentinel mutant after fixture fix; rc= 1
ĐỘT BIẾN ruff-ci-da-tach-thieu-ruff: LỌT
PHẢN CHỨNG: 90/91 đỏ đúng
TỔNG: ĐỎ
A candidate: original main rc= 0
PHẢN CHỨNG: 91/91 đỏ đúng
TỔNG: ĐẠT
A candidate: module diagnostic errors= []
A candidate: reversed probe errors= ["CI không in probe Ruff --version (job: ['gate-registry'])"]
A candidate: PIP_TARGET step errors= ["CI không ghim Ruff 0.15.15 (job: ['gate-registry'])", "CI không in probe Ruff --version (job: ['gate-registry'])", "CI không provision Ruff trước test registry trong cùng job (job chạy test registry: ['gate-registry'])"]
A candidate: PIP_TARGET job errors= ["CI không ghim Ruff 0.15.15 (job: ['gate-registry'])", "CI không in probe Ruff --version (job: ['gate-registry'])", "CI không provision Ruff trước test registry trong cùng job (job chạy test registry: ['gate-registry'])"]
A candidate: PIP_TARGET workflow errors= ["CI không ghim Ruff 0.15.15 (job: ['gate', 'gate-packet-loop', 'gate-registry'])", "CI không in probe Ruff --version (job: ['gate', 'gate-packet-loop', 'gate-registry'])", "CI không provision Ruff trước test registry trong cùng job (job chạy test registry: ['gate-registry'])"]
A candidate LIMIT: only measured module/order/declared-env cases, not a complete shell recognizer.
F candidate: repeated directory call 1 => ('GIET', '', 1)
F candidate: repeated directory call 2 => ('GIET', '', 1)
F candidate: repeated directory call 3 => ('GIET', '', 1)
F candidate: selftests rc= 0 ; TU KIEM: 23/23
```
Các thay đổi này là thí nghiệm định hướng, không phải gói vá đã hoàn tất. Nhãn: **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. File ops chỉ được xử lý bằng packet riêng.

HƯỚNG 9: Cô lập cấu hình Git cho ca r521 và hai tự đột biến ký commit
  giả thuyết : nếu r521 kế thừa cấu hình Git trong lúc mutant tắt chốt ký thì nó chết ngoài chốt dù bản thân nghĩa vụ iterator không đổi
  lệnh       : python do-review/kiem_nhanh_do.py
  output     :
```text
old-reviewed selected mutants= ['go-tat-ky-o-kho-mutant', 'src-tat-ky-khong-chay']
old-reviewed git-config-clean= False => (0, 2)
DOT BIEN TU KIEM go-tat-ky-o-kho-mutant | r506 | TIN DUNG GIA: ca chet vi loi VO CAN ['r521']
DOT BIEN TU KIEM src-tat-ky-khong-chay | r506 | TIN DUNG GIA: ca chet vi loi VO CAN ['r521']
old-reviewed git-config-clean= True => (2, 0)
DOT BIEN TU KIEM go-tat-ky-o-kho-mutant | r506 | 1/1
DOT BIEN TU KIEM src-tat-ky-khong-chay | r506 | 1/1
head selected mutants= ['go-tat-ky-o-kho-mutant', 'src-tat-ky-khong-chay']
head git-config-clean= False => (0, 2)
DOT BIEN TU KIEM go-tat-ky-o-kho-mutant | r506 | TIN DUNG GIA: ca chet vi loi VO CAN ['r521']
DOT BIEN TU KIEM src-tat-ky-khong-chay | r506 | TIN DUNG GIA: ca chet vi loi VO CAN ['r521']
head git-config-clean= True => (2, 0)
DOT BIEN TU KIEM go-tat-ky-o-kho-mutant | r506 | 1/1
DOT BIEN TU KIEM src-tat-ky-khong-chay | r506 | 1/1
DOT BIEN TU KIEM go-tat-ky-o-kho-mutant | r506 | 0 — ca do THUC TE: r506,r519
DOT BIEN TU KIEM src-tat-ky-khong-chay | r506 | 0 — ca do THUC TE: r506,r519
r521 isolated; inherited environment; result= (0, 2)
head ops file byte-equal origin/master= True
ops SHA256= b56636d9c26d9b0f7b537d71e9a7edc7ef446e8c51ef0466fbc849a064497134
```
  kết luận   : LỖI

Lỗi có sẵn ngoài write set #463; đi bằng packet riêng. Hai mutant hỏng do cùng một gốc cô lập môi trường, chỉ là một finding.

## Chỗ có thể nén A8 mà không mất răng

Lệnh: `python do-review/nen_a8.py`.

Ghép 8 cặp chú thích, bắt đầu ở dòng [141, 143, 145, 147, 649, 656, 697, 708] tại HEAD, giữ mọi từ. AST trước/sau bằng nhau; không bỏ ca/chốt/lời giải thích. Đổi lại: dòng dài hơn, kém tiện đọc trên màn hẹp.

```json
{
  "pair_start_lines": [
    141,
    143,
    145,
    147,
    649,
    656,
    697,
    708
  ],
  "same_ast": true,
  "python_additions": 276,
  "python_deletions": 88,
  "packet_additions": 430,
  "main_rc": 0,
  "main_summary": "PHẢN CHỨNG: 91/91 đỏ đúng\nTỔNG: ĐẠT"
}
```
Đây là phép thử nén trong `do-review/nen-a8/`, không tự quyết chốt A8 ở chủ kho. Chưa bao gồm phần thêm của các bản sửa nội dung còn phải làm.

Bổ sung HƯỚNG 9: liệt kê các lối gọi trước khi vá trọn lớp: `r502:804`, `r506:1000`, `r514:1390/1414` đã cô lập; `r519:1860` (no-op), `r519:1875` (đếm đích), `r521:2071` (iterator) là ba lối chưa cô lập. Chỉ vá r521 vẫn đỏ ở r519; vá cả ba mới đủ.

```text
3 isolation sites fixed, selected mutants=(2, 0)
DOT BIEN TU KIEM go-tat-ky-o-kho-mutant | r506 | 1/1
DOT BIEN TU KIEM src-tat-ky-khong-chay | r506 | 1/1
```

## Phép kiểm hợp đồng cục bộ bổ sung (không tính N)

```text
A7 actual pre-split source= ([], 3)
A4 per-job timeout= {'gate': 60, 'gate-registry': 60, 'gate-packet-loop': 60}
A4 step timeout overrides= 0
A4 remove timeout at gate => False
A4 remove timeout at gate-registry => False
A4 remove timeout at gate-packet-loop => False
A3 on: correct parser key is boolean True; remove workflow_dispatch => equality= False
EOL rc= 0 output= {'checked': 2060, 'mode': 'all', 'ok': True, 'scanned': 2082, 'schema': 'eol_policy.v1', 'skipped': 22, 'violations': []}
```

Thử đủ bộ trên bản sao có ba điểm cô lập Git và tên kênh theo dấu phiên; chỉ đo local, chưa chạy trên cây thật:
```text
Combined scratch candidate full: rc=0, elapsed=274.454s
DOT BIEN TU KIEM tu-kiem-gop-hai-lop-ngoai-le | r516 | 1/1
DOT BIEN TU KIEM tu-kiem-bo-ghi-nhan-loi-vo-can | r516 | 1/1
TU KIEM co dot bien rieng: 23/23 nhom bat buoc · dot bien giet 76/76
8/8
MUTANT: giet = 10 · khong giet = 0 · khong do duoc = 0 / tong 10
```

## BẢNG ĐO

Mọi số dưới đây là phép đo local của lượt này, trừ cột lời khai. Output theo từng ca và từng lệnh nằm ở các khối đối chiếu/BẢNG SĂN phía trên; số liệu máy đọc được ở `do-review/measurements.json`. Các biến thể đo cùng gốc được gom một hàng, không giấu số khớp.

| Khẳng định / phép đo | PR/gói khai hoặc kỳ vọng | Tự đo | Khớp / phạm vi |
|---|---|---|---|
| Exact SHA và trạng thái cây | `201bd7a46a948f9ed0a4cb51263f9f236bf5a5d7`; sạch | cùng SHA; porcelain rỗng đầu/cuối | Khớp |
| Tree | bản sao đúng head | `1949403d2a76ea6b96d7a0b255a44af1c1dc1cd6` | Neo đã đo |
| Ref nhánh / clone | 361; đầy đủ lịch sử; abbrev 7 | 361 nhánh + 1 ref HEAD; shallow=false; abbrev=7 | Khớp; không xác minh GitHub trực tiếp |
| Revision đặc tả/lease | r19 | 19/19; hash khớp | Khớp |
| **Băm đặc tả r19** | `c9d3f716fe4c737963a0e8164b6f3e42cac13c986ac55ed818e8044190a5b531` | `c9d3f716fe4c737963a0e8164b6f3e42cac13c986ac55ed818e8044190a5b531` | Khớp `spec_hash` và `spec_sha256` lease |
| **Số đường dẫn diff** | 2 | **2** | Khớp |
| Python diff | +284/−88 | +284/−88 | Khớp |
| Workflow diff | +154/−6 | +154/−6 | Khớp |
| **A8 additions so trần** | 438; trần 430 | **438 > 430, vượt 8** | Khớp EVIDENCE; chốt treo ở chủ kho; không là finding chất lượng mã |
| A8 trong commit message | 439 | 438 | Lệch lời khai 1 dòng |
| **ci_dang_ky_test TỔNG** | ĐẠT | **rc=0; TỔNG: ĐẠT** | Khớp; không chạy `--chay` |
| Đăng ký / launcher / Ruff contract | bảng cổng xanh | 21/21; 4/4; 3/3 | Khớp |
| Phản chứng | 93/93 | **91/91**, 91 tên phân biệt | Không khớp lời khai; các ca thực chạy đều đạt |
| Bảng nhãn trong commit | nhắc 31 và 19 | **28** dòng `nhan-` | Không khớp |
| **Ruff F** | All checks passed | **rc=0; All checks passed!** | Khớp |
| Phiên bản Ruff gọi bằng module | lời gọi hợp lệ | rc=0; **0.15.15** | Nhưng consumer gán KPT và thêm 1 lỗi |
| Lớp A, bỏ phần tử allowlist | 5 tiền tố + 5 tùy chọn | **10/10** siết cổng; chiều NHẬN và chốt tập bắt được | Khớp bản chất bản vá |
| Lớp B/C ở e7a271b | công cụ đã vá | ancestor rc=1; hai path vắng ở HEAD (rc=128); nhánh phụ **13/13**, strict rc=0, 0 chốt bỏ qua | Phần đo phụ khớp, không chứng nhận head có công cụ |
| B/C, bỏ từng khối nghĩa vụ ở bản phụ | phải chặn cả 2 | cả 2 CHAN [4] | Khớp; runner F07 không có để đo |
| D, phân bổ/các ô | N=2; A2=4, A5=2 | trần 2; phân bổ tại A1; 2×2=4, 1×2=2, tổng 6 | Đã vá trong r19; không chạy CI để tính billing |
| H1, mutant sentinel trên main | phải bị bắt | rc=0; 91/91; 3/3 Ruff | Lọt |
| H1, thiếu cài ở chỉ số 0/1/2/8 | nguyên gốc phải chặn | số lỗi nguyên gốc/mutant: 1/1, 1/0, 1/0, 1/0 | Fixture chỉ số 0 che mất lỗi |
| H1 sau sửa fixture | nền xanh, mutant đỏ | nền rc=0, 91/91; mutant rc=1, 90/91 | Đạt chốt riêng, số ca không tăng |
| H2, bước trước/sau | tập và lệnh không đổi | 40 → 38+10+10=58 lượt khai bước; tập 40 tên; 2 bước dời mỗi bước vẫn 1 bản | Khớp cấu trúc; 18 bản sao thiết lập |
| H2, tiền tố thiết lập | 9 bước mỗi job mới | 9/9 khớp toàn bộ field ở cả 2 job; đảo setup tại mỗi job ⇒ false | Đã kiểm cả thứ tự |
| H3, ngữ cảnh/matrix/if | không đổi | 3 job bằng context gate nền; tập tên/if 40=40; 3 đột biến matrix/env/job-if đều đỏ | Khớp cấu trúc |
| A3 on/concurrency | không đổi, phải có ca âm on | bằng nhau; bỏ workflow_dispatch ở khóa `True` ⇒ false | Parser không so hai None |
| A3 actionlint + shellcheck | delta chẩn đoán rỗng | 1.7.12 + 0.9.0; ci.yml rc=0/0; 0/0 chẩn đoán | Khớp trên môi trường này |
| A3 phản chứng đa tập | thêm lỗi phải đổi tập dù rc cùng đỏ | rc=1/1; 1→2 chẩn đoán, thêm đúng 1 SC2086; SC1003 cũ còn | Đạt |
| A4 timeout | mỗi job 60; không có ở bước | 3/3 là 60; 0 override bước; xóa từng khóa làm 3/3 ca âm đỏ | Khớp |
| A7 source thật trước tách | tương thích lùi | 0 lỗi / 3 chốt | Khớp |
| H4, probe trước install | không đủ bằng chứng | consumer 0 lỗi; chỉ số install=1, probe=0; bash chưa có Ruff rc=127 | Lọt thứ tự trong bước |
| H5, PIP_TARGET ở 3 cấp | không đủ provisioning | 3/3 trả 0 lỗi; parser pip xác nhận target_dir đổi | Lọt ngữ cảnh env |
| H6, gọi lại cùng thư mục | đo lại được như thư mục mới | GIET/1, GIET/2, KDD/2; đối chứng GIET/1; log cũ 27/18 dòng | Lỗi vòng đời kênh |
| H7, 5 kiểu dữ liệu | hợp lệ nhận; không hợp lệ KDD | 2 GIET (tuple/iterator); 3 KDD; 0 ngoại lệ thoát ra | Khớp |
| H8, 8 dạng YAML sai cấu trúc | không cấp sạch | 4 trả lỗi, 4 ném ngoại lệ; 0 trả sạch | Fail-close; không tính exception thành finding mới |
| File ops được giao đọc | cùng bản đã land | hai bản SHA256 `b56636d9c26d9b0f7b537d71e9a7edc7ef446e8c51ef0466fbc849a064497134`; head=master bằng byte | Khớp |
| Delta ops so bản review trước | nghĩa vụ đọc phần chưa được review | `94c416d`→`3c7df6d`: +25/−1; đã đọc diff và các lối liên quan | Không nằm trong diff #463 |
| Full nhanh_don_duoc nguyên gốc | gói khai chưa chạy trong sandbox | **rc=1; 261,189 s**; ca **8/8**, mutant **10/10**, tự kiểm **23/23**, tự đột biến **74/76** | Đã đo bổ sung; 2 mục hỏng cùng gốc G |
| H9, 2 mutant trước/sau | kỳ vọng chỉ r506 đỏ | cả hai mốc: kế thừa 0/2, config sạch 2/2 | Lỗi có sẵn, phụ thuộc môi trường |
| H9 vá từng phần / trọn đường vào | phải hết lỗi ngoài chốt | chỉ r521 còn 0/2; đủ 3 lối r519/r521 ⇒ 2/2 | Cần đóng cả 3 lối |
| Candidate tên kênh | hết nhiễm lượt trước | 3/3 gọi lại GIET/1; tự kiểm 23/23 rc=0 | Khớp ca riêng F |
| Candidate ops gộp F/G, full | giữ mọi ca/mutant | **rc=0; 274,454 s; 8/8; 10/10; 23/23; 76/76** | Chỉ trên scratch, chưa áp cây thật |
| Nén A8 | chỉ ra chỗ giữ răng | ghép 8 cặp chú thích; cùng AST; +276/−88 Python, tổng **430**; rc=0, 91/91 | Mất tiện đọc dòng ngắn; không mất chữ/chốt/ca |
| Doctrine-scan / ADR | sạch; 47/47 | rc=0; quét 7 tệp, 0 chỗ chép; 47/47, ngoại lệ trạng thái ADR-0016 được công cụ tha | Khớp trong phạm vi cổng |
| EOL toàn cây | ok=true | rc=0; scanned=2082, checked=2060, skipped=22; 0 vi phạm | Khớp |
| **A1 / A5** | cấm chạy CI lượt này | **KHÔNG ĐO ĐƯỢC** | Theo thiết kế, không là finding |
| CI dispatch / thao tác GitHub | không được chạy | 0 / 0 | Tuân thủ |
| Số hướng săn / finding | ≥7 hướng, gộp theo gốc | **9 hướng; 5 finding: 0 P1, 4 P2, 1 P3** | Hai finding ops đi packet riêng |

## Finding theo gốc

Có 5 lớp được nêu thành finding: 4 P2 và 1 P3. Trong write set #463: A, C, E; hai lớp F/G thuộc nghĩa vụ đọc `ops/nhanh_don_duoc_test.py`, phải đi bằng packet riêng. Không tính mỗi biến thể đầu vào thành một finding. Tình trạng chưa chứng nhận được trọn lớp B và phần F07 của lớp C nằm ở đối chiếu, không nhân thành finding mới chỉ vì thiếu hiện vật trên head.

### ruff-khuon-chua-chung-minh-provisioning  [P2]  Khuôn lệnh còn nhầm sự xuất hiện của Ruff với bằng chứng cài và probe thành công

LỚP: A — cùng gốc mô hình ngữ nghĩa chưa đủ: chứng nhận provisioning từ nhãn của dòng và sự hiện diện của probe, chưa gắn với cách gọi, ngữ cảnh và thứ tự thực thi. Kế tiếp `R6-F01`/`R6-F02`; không phải ba finding rời.

TỆP/DÒNG: `cay-kho/.claude/dev/ci_dang_ky_test.py:179` (`_loai_mot_dong`), `:207` (tổng hợp dòng), `:250` (phân loại bước), `:268` (probe).

VẤN ĐỀ: Bản đồ các đường vào đã đo gồm lời gọi trực tiếp/module, thứ tự install/probe trong cùng `run`, và môi trường ở ba cấp workflow/job/step. Có cả chiều nhận sai lẫn chặn oan:

- `python -m ruff --version` chạy tại chỗ rc=0, in `ruff 0.15.15`, nhưng bị gán `KHONG_PHAN_TICH_DUOC`. Thêm đúng lời gọi chẩn đoán này sau registry, giữ đủ pin/probe trước registry, khiến cổng báo không ghim Ruff.
- Chỉ đảo hai dòng có sẵn của bước cài thành probe trước install, cổng vẫn trả `[]`. Chạy nguyên hai dòng đảo bằng bash `-e` với PATH trống để mô phỏng chưa có Ruff dừng ngay dòng đầu, rc=127; lệnh cài chưa được thực thi. Regex hiện chỉ đòi probe có mặt.
- Thêm `PIP_TARGET` lần lượt ở ba cấp env, giữ nguyên argv của bước cài, cả ba đều trả `[]`. Parser pip thật xác nhận cùng argv nay có `target_dir=tmp-ruff-review`; vị trí cài không còn được chứng minh là môi trường sẽ chạy registry. Biến thể này đi qua cấu hình môi trường, khác các cờ `--target` đã săn ở lượt trước.

ĐÃ THỬ VÁ: Có, trên mô-đun scratch: nhận lời gọi module, đòi probe sau install, xét env khai báo theo khuôn dương các giá trị đã biết. Cổng nền vẫn 91/91; chẩn đoán module được nhận; đảo thứ tự bị chặn; cả ba lối env bị chặn. Đây mới là thử định hướng cho những ca đã đo, chưa phải bản vá trọn ngữ nghĩa shell.

Hướng vá: Tách nhận diện lời gọi Ruff khỏi chứng nhận provisioning; chỉ cấp chứng nhận khi **toàn bộ** lệnh được hỗ trợ, môi trường hiệu lực được kiểm, và install/probe theo thứ tự cần thiết trước registry. Đừng sửa bằng một danh sách cấm biến môi trường hoặc toán tử mới. Ca khóa phải có đối chứng giữ nguyên bước cài hợp lệ, lời gọi module vô hại, đảo thứ tự nội bộ, và từng cấp env độc lập. Rủi ro: khuôn quá hẹp sẽ chặn oan lệnh/env hợp lệ; nhận chỉ theo tiền tố lại bỏ lọt phần đuôi lệnh. Không thêm điều kiện chạy vào workflow.

ĐÃ THỬ NGHIỆM: `python do-review/review_lop.py A`; `python do-review/san_moi.py 4`; `python do-review/san_moi.py 5`; `python do-review/thu_va.py`. Log `lop-A.log`, `huong-4*.log`, `huong-5.log`, `thu-va.log` trong `do-review/logs/` ghi output thật.

ĐỘ TIN: cao đối với các biểu hiện đã đo; chưa chứng nhận đóng hết ngữ nghĩa shell.

### ruff-fixture-thieu-cai-che-mat-chi-so  [P2]  Fixture thiếu Ruff không phân biệt được không tìm thấy với vị trí bước đầu tiên

LỚP: C — miền đầu vào của phép đo làm hai trạng thái khác nhau trở thành tương đương. Biểu hiện mới của lớp thiếu ca phân biệt, không phải lặp đột biến bỏ phần tử lượt trước.

TỆP/DÒNG: `cay-kho/.claude/dev/ci_dang_ky_test.py:644` (fixture `da-tach-thieu-ruff`); điểm cần được canh ở `:277` (giá trị mặc định của `ruff_i`).

VẤN ĐỀ: Fixture thiếu cài chỉ còn `[_reg]`, nên `gate_i=0`. Đổi duy nhất sentinel của `ruff_i` từ `-1` thành `0` vẫn khiến `0 < 0` sai: ca âm ấy tiếp tục xanh và **toàn main vẫn rc=0, 91/91**. Trên bố cục thật, bỏ bước cài giữ tám bước thiết lập khiến `gate_i=8`; chính mutant đó trả sạch dù job không có bước cài Ruff. Hàm nguyên gốc chặn đúng; đây là lỗ của phản chứng bảo vệ M7.

ĐÃ THỬ VÁ: Có. Dùng `_khac` đã có sẵn, đổi fixture thành `[_khac, _reg]`. Nền vẫn rc=0, 91/91; cùng mutant nay làm đúng ca đó `LỌT`, main rc=1, 90/91. Không phải thêm một bộ kiểm khác hoặc tăng số fixture.

Hướng vá: Giữ một tiền tố vô hại trong ca thiếu cài; nếu giữ cả hai hình dạng, phải đo riêng chỉ số 0 và chỉ số dương. Khóa đúng lỗi thiếu provisioning, tránh để một lỗi pin/probe không liên quan che mất phép so vị trí. Rủi ro: fixture mới bị làm đỏ bởi chốt khác sẽ tái tạo điểm mù; đối chứng hai consumer nguyên gốc/mutant trong HƯỚNG 1 phân biệt được điều đó.

ĐÃ THỬ NGHIỆM: `python do-review/san_moi.py 1`: prefix 0 cho nguyên gốc/mutant 1/1 lỗi; prefix 1 và 2 cho 1/0 lỗi; bố cục thật chỉ số 8 cũng 1/0. `python do-review/thu_va.py`: sửa fixture giết đúng mutant.

ĐỘ TIN: cao.

### nhanh-tu-kiem-chua-co-lap-cau-hinh-git  [P2]  Ba lối dựng kho trong tự kiểm còn phụ thuộc cấu hình Git của máy

LỚP: G — fixture không cô lập môi trường của chính phép đo. Hai mutant ký commit cùng hỏng do một gốc, chỉ nộp một finding. **Ngoài write set #463; đi bằng packet riêng.**

TỆP/DÒNG: `cay-kho/ops/nhanh_don_duoc_test.py:1860` (r519/no-op), `:1875` (r519/đếm đích), `:2071` (r521/iterator); đối chiếu các lối đã cô lập `:804`, `:1000`, `:1390`, `:1414`.

VẤN ĐỀ: Hai mutant `go-tat-ky-o-kho-mutant` và `src-tat-ky-khong-chay` chỉ được kỳ vọng làm r506 đỏ. Dưới cấu hình Git kế thừa, chúng còn kéo r521 chết ngoài chốt và làm r519 đỏ; bộ đầy đủ thật thoát 1, chỉ 74/76 tự đột biến được công nhận. Dùng `_git_config_sach()` có sẵn thì cả hai đạt đúng r506. Lỗi không do packet tách job: hai mutant cho cùng kết quả ở `94c416d` và HEAD; tệp ops ở HEAD bằng byte với `origin/master`.

ĐÃ THỬ VÁ: Có. Vá riêng r521 vẫn hỏng ở r519 — đã đo và giữ output, không khai vá trọn. Liệt kê đủ bảy vị trí gọi `chay_dot_bien` trong các ca tự kiểm rồi cô lập cả ba lối thiếu bằng context manager có sẵn. Cả hai mutant nay được công nhận đúng `(2, 0)` trong môi trường kế thừa. Bản sao gộp với sửa tên kênh đã chạy full: rc=0, 274,454 s, ca 8/8, mutant sản phẩm 10/10, tự kiểm 23/23, tự đột biến 76/76. Log: `do-review/logs/nhanh-all-isolated-full.log`.

Hướng vá: Cô lập cấu hình ở đúng các fixture cần đo no-op/đếm đích/iterator, giữ phép đo cấu hình thật ở r506. Ca khóa: từng mutant với cấu hình kế thừa và cấu hình sạch; ca r519/no-op, r519/đếm đích, r521/iterator phải phân biệt được độc lập. Rủi ro: ép cấu hình sạch ở tầng toàn suite có thể vô tình vô hiệu hóa bài kiểm ký; không nới tập đích để hợp thức hóa lỗi ngoài chốt.

ĐÃ THỬ NGHIỆM: `python ops/nhanh_don_duoc_test.py`: rc=1, 261,189 s, ca 8/8, mutant sản phẩm 10/10, tự kiểm 23/23, tự đột biến 74/76. `python do-review/kiem_nhanh_do.py`: trước/sau cùng `(0,2)` khi kế thừa, `(2,0)` khi cô lập; sau sửa ba lối `(2,0)` khi kế thừa. Log `nhanh-full.log`, `nhanh-doi-chung.log`, `nhanh-all-isolated-selected.log`.

ĐỘ TIN: cao trong môi trường local đã đo. Không suy kết quả Windows/CI từ phép đo này.

### kenh-mutant-tai-su-dung-giua-cac-luot  [P2]  Tên kênh chỉ theo số lần thử làm log của lần đo trước phá lần đo mới

LỚP: F — vòng đời hiện vật không gắn với danh tính lượt đo. **Ngoài write set #463; đi bằng packet riêng.**

TỆP/DÒNG: `cay-kho/ops/nhanh_don_duoc_test.py:506` (tên `.ket-qua-{lan_thu}.jsonl`), `:74` (writer mở append).

VẤN ĐỀ: Gọi lại `chay_mot_mutant` trên cùng thư mục hợp lệ tạo dấu phiên mới nhưng dùng lại hai tên tệp. Lần đầu `GIET` ở lần thử 1; lần gọi thứ hai phải sang lần thử 2; lần gọi thứ ba `KHONG_DO_DUOC` sau cả hai lần vì gặp bản ghi của phiên cũ. Đối chứng thư mục mới lập tức `GIET` ở lần thử 1. Reader từ chối log cũ là đúng; lỗi ở việc caller tự chọn lại kênh đã chứa dữ liệu. Luồng `chay_dot_bien` bình thường tạo thư mục mới nên chưa gặp lỗi này; phạm vi finding là tái đo cùng bản sao qua helper.

ĐÃ THỬ VÁ: Có. Trên bản sao thêm dấu phiên đã sinh vào tên kênh, giữ nguyên kiểm neo và chế độ append. Ba lần gọi đều `GIET` ở lần thử 1; 23/23 tự kiểm vẫn đạt. Bản sao gộp với vá cô lập Git được đo đủ bộ theo log cuối.

Hướng vá: Một kênh riêng cho mỗi lần phóng, dùng cùng đường dẫn đã chuẩn hóa cho writer/reader; giữ hiện vật cũ cho chẩn đoán. Ca khóa: gọi ít nhất ba lượt trên cùng thư mục, đối chứng thư mục mới, rồi kiểm kênh thuộc phiên cũ vẫn bị reader từ chối. Rủi ro: thêm file cần chính sách dọn trong phạm vi scratch; không sửa bằng cách bỏ xác thực dấu phiên hoặc xóa dữ liệu chưa thuộc lượt đang đo.

ĐÃ THỬ NGHIỆM: `python do-review/san_moi.py 6`: `GIET/1 → GIET/2 → KHONG_DO_DUOC/2`; hai tệp cũ có 27 và 18 dòng. `python do-review/thu_va.py`: sau sửa `GIET/1` cả ba lần, selftest rc=0, 23/23.

ĐỘ TIN: cao cho việc tái dùng cùng thư mục; không khai rằng mọi lần chạy CLI bình thường đều hỏng.

### bang-chung-chep-tay-lech-so-dem  [P3]  Số phản chứng trong bằng chứng không được sinh từ lượt chạy trên SHA đang duyệt

LỚP: E — số chép tay trôi khỏi nguồn đo. Tiếp tục lớp còn mở `R6-F06`.

TỆP/DÒNG: `EVIDENCE.md:20`; đối chứng log `do-review/logs/registry-baseline.log`; commit message của `201bd7a` là lời khai, không phải phép đo.

VẤN ĐỀ: EVIDENCE và commit khai 93/93, nhưng head này chạy đúng **91/91**, không trùng tên, `TỔNG: ĐẠT`. Đếm riêng bảng nhãn được **28** ca trong khi commit nhắc cả 31 lẫn 19. Commit còn khai A8=439; diff thật và EVIDENCE đúng là 438. Không có bằng chứng bộ 93 ca từng chạy trên bytes hiện tại. Cổng xanh là đúng; các số kèm theo không vì thế trở thành đúng.

ĐÃ THỬ VÁ: Có ở tầng báo cáo: lưu stdout/rc và sinh các số trong BẢNG ĐO từ lượt đo hiện tại. Không sửa đầu vào EVIDENCE đóng băng, không sửa lịch sử commit.

Hướng vá: Sinh hàng bằng chứng từ cùng stdout có tập tên ca, rc, exact SHA và câu tổng kết. Khóa trường hợp số ca đổi hoặc suite dừng trước phần phản chứng; không tái dùng số từ commit hoặc đếm ca tĩnh trong mã. Rủi ro: một parser báo cáo chỉ đọc dòng xanh cuối vẫn có thể bỏ sót phần không chạy; phải giữ đầy đủ nguồn và trạng thái thiếu dữ liệu.

ĐÃ THỬ NGHIỆM: `python do-review/review_lop.py E`; đếm `ĐỘT BIẾN ` và `ĐỘT BIẾN nhan-` trên log lần chạy gốc. Bảng đo ghi cả các con số khớp, không chỉ số lệch.

ĐỘ TIN: cao.

## Hướng nêu bằng lời, chưa đo

Chiều CẤM bổ sung của lớp A: `_loai_mot_dong` trả `KHONG` ngay khi token đầu được coi là Ruff, chưa kiểm phần đuôi. Công thức để phiên điều phối đo: lấy dòng cài/probe chuẩn có sẵn, rồi trong một dòng logic đặt lời gọi Ruff có sẵn trước một toán tử nối lệnh và một lệnh thay đổi/gỡ Ruff đã có trong fixture; hỏi cả classifier và consumer trên cùng job. Phải phân biệt trường hợp lời gọi Ruff đơn thuần với trường hợp có lệnh tiếp theo. Tôi không soạn chuỗi payload, không chạy phép này, không tính nó vào 9 hướng đã đo và không dùng nó làm một finding riêng.

## Giới hạn và phạm vi kết luận

- A1/A5: **KHÔNG ĐO ĐƯỢC** theo lệnh cấm chạy CI; không coi là finding, không ghi đạt. A2 chỉ kiểm được bảo toàn cấu trúc, không có tập conclusion của lượt CI. A6/ruleset và trạng thái GitHub trực tiếp không đo được offline.
- Không chạy `ci_dang_ky_test.py --chay` hay toàn bộ CI; chỉ chạy từng bộ cục bộ được ghi rõ. Không chạy `packet_loop_test` hoặc suite runtime dài còn lại. Không suy từ `doc-claims-check` của sandbox sang kho nguồn đã được EVIDENCE khai lệch.
- B: bản sửa `e7a271b` không nằm trên reviewed_sha. Đo nhánh phụ chứng minh t10 và chốt tập nghĩa vụ hoạt động; lời khai giới hạn regex không chứng minh đã đóng R6-F08. Không yêu cầu đưa công cụ ops vào write set hai đường của #463. C/F07: không có runner của trạng thái `GIET O GATE NEN` trong gói để tự đo, nên không công nhận lời khai 11/11 là phép đo của reviewer.
- Không giao gói vá hoàn tất: các thay đổi trong `do-review/` là thí nghiệm định hướng, tách khỏi snapshot. Nhãn áp dụng: **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Các hunk gate phải được executor tự dẫn xuất theo §8 của `tai-lieu/PROTOCOL-trich-8-12-13.md`; hai lỗi ops cần packet riêng. Không mở đường dẫn thứ ba, không đổi timeout/điều kiện chạy/composite.
- A8 vẫn là chốt treo ở chủ kho. Phép nén thử đạt 430 giữ nguyên AST chỉ là một lựa chọn có số đo, chưa bao gồm các sửa nội dung cần làm, không phải quyền tự thông qua chốt.
- Sai lệch thủ tục của reviewer: trước khi đọc được phạm vi đóng trong PROMPT, lệnh liệt kê khởi động đã in tên đường dẫn từ thư mục cha. Không đọc nội dung các tệp ngoài ấy và không dùng chúng làm bằng chứng. Từ khi đọc PROMPT, các nguồn, scratch và phép đo đều nằm trong gói; sai lệch này không tính thành finding sản phẩm.

Kết luận: `changes_requested` cho #463 vì các lớp A/C/E còn tồn tại; F/G được chuyển bằng mô tả sang packet riêng. Không có commit/push nhánh đang duyệt hay thao tác GitHub; các commit/ref trong bộ test có sẵn chỉ thuộc kho fixture tạm của chính sandbox. Verdict này neo đúng SHA nêu đầu tệp, không tự tạo approval/merge authority.

verdict: changes_requested
