# Đặc tả packet — `THU-HOI-ADMISSION-MERGE-BASE-B` (revision 13)

- `packet_id`: **THU-HOI-ADMISSION-MERGE-BASE-B** · `revision`: **13** · trạng thái: nháp, chờ chủ kho duyệt băm.
  Thay `ops/specs/THU-HOI-ADMISSION-MERGE-BASE-B-r12.md` (sha256
  `fc5d749442f203c5acbaa7596494ef5eef3354b8659369679639b81037d49480`), r11 (sha256
  `27f2097149bb5607b25ce3f38adbef889673aa54288ec1c17a7efcb39bcb8ddb`), r10 (sha256
  `a71e04196fa7f8c9aa0131920509477b26c4c65bdb863755298be2e8a104b35c`), r9 (sha256
  `99965d5f02e4934694d4ab82ee4089ca787d51729af81ff92ff821d432295df1`), r8 (sha256
  `908a4a46cbe72bb97dbb21ab72eb5e4ff21862cab165c6975f803948fd08c566`), r7 (sha256
  `f3c27ed8245ed4aa08bc2074e900efe2d9e21e55ca8f916dfe383ca3415c73f3`), r6 (sha256
  `b05e2f07cb2103c9e6bc38de5e33290e3bd128ea7284edfb77c600a1a0618646`), r5 (sha256
  `9cdd308ebfaa3804fcb7c5712f4321016294003ee1cb6929929dc3531da091b7`), r4 (sha256
  `cc5cfc5c038a7544ce9d9f330a8a395a205f1c488d43eab2e9cb12f303c7e4ff`), r3 (sha256
  `f366fda5c61705ec9915d026c43db40f9aeda404965d7d7f6957fbd3977cdbdd`), r2 (sha256
  `3f002496d380119c9093c072dda3c690afbfa140c21d6ddfdd792590c17dac69`) và r1 (sha256
  `a4e4a7aad7a885acccfd48c513644467a0b048833d50a0cb101992e400cf9ddf`); cả mười hai chưa từng được duyệt và giữ nguyên trong
  kho để verdict của từng lượt review vẫn tra được theo băm. Thay đổi so với r12: mục 10.
- Review Rescue Checkpoint (`ADR-0037`), ba lần trong ngày 07-11-2026 và một lần ngày 08-11-2026: lần 1 sau review lượt 2 (F11) — chủ kho chọn
  sửa thành r3, giữ merge-base; lần 2 sau review lượt 3 (F14, lần thứ ba của hình dạng `canary-thieu-dieu-kien-chon`) —
  chủ kho chọn r4, đổi gốc của canary; lần 3 sau review lượt 4 (F16, lần thứ tư của hình dạng canary và biểu hiện thứ
  sáu của lớp kế thừa `phan-loai-vang-va-khong-do-duoc`) — chủ kho chọn **r5 theo phương án đã ghi sẵn ở r4**: B17/B18
  **không còn đoán trước** kết quả của bộ kiểm; B17 dùng đầu vào tự dựng trên lịch sử thật, và cả hai xếp kết quả theo
  nguyên nhân, có xác nhận độc lập bằng Git.
- Sau review lượt 5 (F18 là lần thứ năm của hình dạng canary; F19 là hình dạng mới), **phiên soạn spec tự quyết, không
  hỏi chủ kho**, theo chỉ đạo chủ kho trong phiên ngày 07-11-2026: *"chỉ hỏi những vấn đề thực sự quan trọng như hướng
  đi bế tắc, không đủ tài nguyên để chạy, hoặc có phát hiện đảo ngược chỉ đạo của tôi"*. Lý do không thuộc ba loại ấy:
  F19 đo lại trên Linux cho thấy thiết kế merge-base chạy được trên đường thật (CI Ubuntu), nên không đảo quyết định giữ
  merge-base; F18 có lối ra đã đo được (đầu vào ghim, mục 5) giữ B17 làm tiêu chí nghiệm thu như quyết định đổi canary ở
  lần 2. Chủ kho có quyền bác quyết định này khi duyệt băm. Cùng ngày chủ kho nâng trần review đặc tả lên **10** lời
  gọi mà không cần hỏi lại từng lượt (mục 8).
- Sau review lượt 6 (F20, lần thứ sáu của hình dạng canary: B17 đem receipt CLI 27 khoá so với validator của receipt
  workflow 41 khoá), phiên soạn spec lại tự quyết theo luật dừng ở mục 7; gốc rễ chung và phương án ghi ở mục 7 và 10.
  Hai điểm của r6 bị đảo lại: B18 **trở lại là tiêu chí nghiệm thu** sau land (r6 hạ nó thành quan sát; review lượt 6
  chỉ ra đó là cắt phạm vi nghiệm thu, không phải bản vá, và việc bỏ canary sau land không có quyết định chủ kho nào
  chống đỡ), và câu "hình dạng này không còn chỗ tái phát" của r6 bị bỏ vì mạnh hơn bằng chứng.
- Sau review lượt 7 (F21, lần thứ bảy của hình dạng canary: vị từ r7 nhận giá trị giờ có LF cuối, và 14 đột biến không
  phát hiện được việc bỏ hẳn một điều; F22: B18 chưa giao người đo), phiên soạn spec xét lại **cách kiểm chính vị từ**,
  không chỉ vá chỗ LF: B17 so JSON chuẩn hoá nguyên khối, và vị từ phải qua ba phép kiểm chứng của nó (mục 5). B18 có
  người đo, mốc và nơi ghi bằng chứng.
- Sau review lượt 8 (F23, lần thứ tám của hình dạng canary: văn bản ghi `[0-9]` còn script dùng `\d` nên nhận chữ số
  Unicode, và bốn cách làm yếu chốt con lọt bộ kiểm chứng), phiên soạn spec xét lại gốc rễ: vị từ tồn tại ở **hai dạng**
  (văn xuôi và script) nên lệch nhau, và bề mặt của nó rộng hơn việc B17 cần đo. r9 giữ **một dạng**: mã vị từ chép
  nguyên văn vào mục 5, ghim sha256; bỏ khỏi B17 các điều về giá trị của ba khoá biến thiên (đã do validator C1a1a kiểm ở
  B11 và B18); kiểm chứng theo **danh sách chốt đóng**, mỗi chốt có nhân chứng cô lập và đột biến bỏ chốt.
- **Checkpoint lần 4** (08-11-2026), trước lời gọi review thứ 9: một phép tấn công độc lập (phiên Claude riêng, không
  tính là lượt review) vẫn tìm được kẽ hở ở vị từ r9, sau tám lần cùng hình dạng, khi chỉ còn 2/10 lời gọi. Phiên soạn
  spec hỏi chủ kho vì đây là hướng đi bế tắc và sắp hết tài nguyên; chủ kho chọn *"Rút về đo hiệu năng"* — phương án đã
  ghi sẵn từ r5. B17 nay chỉ đo hiệu năng trên lịch sử thật, kèm ba điều tối thiểu (mục 5); tính đúng của receipt và các
  phép kiểm thuộc B1–B12 và B18.
- Sau review lượt 9 trên r10 (F24, P2: sau khi rút B17, không ca nào đo **giá trị** `vung_tai_S` và token `quan_he=` mà
  bộ kiểm phát ra; đây là lần thứ ba của hình dạng `nghiem-thu-do-nham-chot`), phiên soạn spec xét lại theo luật dừng ở
  mục 7: không vá riêng từng trường, mà lập **ma trận nghĩa vụ đầu ra mới** (mục 5), mỗi đầu ra có một ca đo giá trị do
  producer phát ra bằng oracle độc lập và một đột biến tại chỗ phát. Thêm ca B2b (vùng không rỗng).
- Sau review lượt 10 trên r11 — lời gọi cuối của trần 10 (F26, P2: ma trận mượn đột biến đổi luồng như `amb-m01`,
  `amb-m02`, `amb-m05`, `amb-m06` làm bằng chứng cho khẳng định giá trị, và chưa ca nào đo đường dẫn lệch trong thông báo
  `VUNG_LECH`; lần thứ tư của `nghiem-thu-do-nham-chot`. F27, P3: số chưa đồng bộ), phiên soạn spec xét lại theo luật dừng:
  ma trận tách **đột biến chỉ đổi giá trị phát ra** khỏi **đột biến chức năng**, và mỗi khẳng định giá trị phải có ít
  nhất một đột biến loại đầu. Trần 10 đã hết; chủ kho chọn *"Nâng trần +1"* (08-11-2026) để review r12 bằng Codex (mục 8).
- Sau review lượt 11 trên r12 (F28, P2, lần thứ năm của `nghiem-thu-do-nham-chot`: hai vế âm của B9 — thông báo lỗi
  **không** mang nhãn `VUNG_LECH` hay `KHONG_CO_MERGE_BASE` — chưa có đột biến chỉ đổi giá trị; F26, F27 đã sửa; không có
  P3), phiên soạn spec sửa đúng cách reviewer đề nghị: hai đột biến mới `amb-m34`, `amb-m35`, mỗi cái chỉ chèn một nhãn vào
  thông báo lỗi của B9. Trần 11 đã hết; r13 chưa được review bằng Codex (mục 8).
- `packet_issue`: **#1266** (sub-issue của Mission #1264). Issue không tự cấp việc (protocol §3.2, §4).
- **Phụ thuộc:** packet `THU-HOI-ADMISSION-MERGE-BASE-A` #1265 (ADR-0066 và dòng §20, đặc tả
  `ops/specs/THU-HOI-ADMISSION-MERGE-BASE-A-r13.md`) đã land. Base của B phải chứa commit land của A; đo bằng
  `git merge-base --is-ancestor <land A> <base B>` ⇒ rc 0, không đo được ⇒ chưa cấp lease.
- `nguon_cap_viec`: như packet A — quyết định chủ kho trong phiên soạn spec 06-11-2026, vòng 1 Q1–Q7 và vòng 2
  Q8–Q13, cả hai *"Theo khuyến nghị"*; căn cứ tài liệu https://claude.ai/artifact/Au5vgKvAZWdqGDHMvkU4cW. Bản ghi
  bền ở thân Mission #1264 (phiên soạn spec đăng theo yêu cầu chủ kho); thẩm quyền ràng buộc là comment duyệt băm
  đặc tả này do chính chủ kho đăng trên #1266.
- `review_class`: **sensitive** — `ops/lease_publish.py` là cổng đọc lease (`ADR-0047`); chạm `.github/workflows/**`
  và `.claude/dev/**` (protocol §8).
- Base dự kiến: `origin/master` lúc cấp lease, sau khi A land (đo 09:43Z 07-11-2026: master `132d376c`, A chưa land).
- Executor **Claude**; reviewer **Codex** độc lập; `human_audited` trên exact head trước merge (vòng 1 Q6). Điều
  kiện merge theo `ADR-0060`.
- Windows: `required` theo `ADR-0060` M3, vì diff chạm `.github/workflows/**` và `.claude/dev/**` (mục 6).
- `full_mutant_audit`: bắt buộc theo M9/K7, vì diff chạm `ops/**/*.py`, `.claude/dev/**` và `.github/workflows/**`.
- Ngân sách đóng của packet (CI, M9, Windows, lời gọi model): mục 8.

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

```yaml
nang_tran:
  ai_nang: chủ kho ducthangho — vòng 1 Q7 của phiên soạn spec 06-11-2026 ("Theo khuyến nghị") cho trần 600; r2–r10 đề xuất 700, r11 đề xuất 760, r12 đề xuất 780; chủ kho chốt trong comment duyệt băm trên Issue
  can_cu: >-
    Ước lượng r12 600–780 dòng thêm, chưa đo: mã bộ kiểm ~120–160 (tô màu hai phía có luật ứng viên chưa stale, đọc giờ
    commit, lọc cực đại, hàm vùng, tích hợp, receipt); test bộ kiểm ~390–500 (20 hàng nghiệm thu nhóm B1–B12 ở mục 5,
    trong đó 18 hàng thuộc tệp này; r1 có 13 hàng, r2 có 15, r3 có 16, r4 có 18, r5–r10 có 19, r11 và r12 có 20; r11
    thêm ca B2b và chín đột biến, r12 thêm sáu đột biến chỉ đổi giá trị và khẳng định đường dẫn lệch); validator C1a1a và
    test ~90–120.
    Runner của B17 nằm ngoài kho, không tính. So sánh gần nhất PR #620 (+204 dòng, 2 tệp; review lượt 1 đo lại:
    workflow +42, test +162). Receipt v2 và validator chấp nhận v2 land cùng nhau trong packet này; nếu phải tách thì
    validator (consumer) land trước bộ kiểm (producer) là thứ tự an toàn, vì không có khoảng nào v2 được phát ra mà
    chưa ai hiểu — việc tách ấy cần packet mới và quyết định chủ kho.
  tran_cu: "≤ 6 tệp / ≤ 450 dòng thêm (ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab)"
  tran_moi: "≤ 6 tệp / ≤ 780 dòng thêm, đo bằng git diff --numstat origin/master...HEAD; vượt thì dừng ở checkpoint chủ kho, không tự bỏ ca của mục 5"
```

## 0. Vấn đề

Như mục 0 của packet A. Tóm lại: `lenh_kiem_thu_hoi_github` gọi `kho.to_tien(S, H)` và trả 12 khi S không phải tổ
tiên của H. Packet A chỉ đăng ký `ADR-0066` và dòng §20; luật mới có hiệu lực từ commit land của **packet này** trên
first-parent master, trước đó luật cũ giữ nguyên (ADR-0066, câu R6). Packet này thi hành luật trong mã.

Ràng buộc hiệu năng đo được, quyết định thiết kế ở mục 4:

- Review lượt 2 chạy bộ đọc nền trên PR #1268 thật (S không là tổ tiên H) trên Windows của chủ kho: bước
  `KhoObject.to_tien` duyệt tổ tiên của H và **hết deadline 60 giây** sau 1.539 object (2.439.154 byte), khoảng 39 ms một
  object, vì `KhoObject.doc` mở một tiến trình `cat-file` cho mỗi object. Kết luận "không phải tổ tiên" bằng cách duyệt
  hết tổ tiên của H vì thế không dùng được; master có 5.481 commit (đo 07-11-2026 trên `9607e3eb`).
- Review lượt 3 và 4 chạy mô phỏng bước tô màu với **bộ đọc nền thật** trên PR #1268 (S = `9607e3eb`): chỉ nhận ứng
  viên chưa stale ⇒ đúng merge-base `d26b36f5`, 33–34 object, 1,3–1,6 giây, rc 0; nhận cả ứng viên đã stale rồi lọc
  từng cặp ⇒ 1.645 object, **hết deadline** ở 59,833 giây. Luật ứng viên ở mục tiêu 1 vì thế là một phần của hợp đồng.
- Chi phí của bước tô màu, với S = `132d376c` và H dựng như mục "Đầu vào của B17" (H có một cha `S~N`). Đơn vị là
  **số commit bước tô màu thật sự đọc**; con số này khác `git rev-list --count S~N..S`, vì bước tô màu còn phải đọc B và
  các tổ tiên chung để truyền cờ stale tới mọi nhánh còn chờ trong hàng đợi:

  | N | `rev-list --count S~N..S` (thống kê lịch sử, không phải chi phí) | commit bước tô màu đọc | Linux: giây | Linux: ms/object |
  |---:|---:|---:|---:|---:|
  | 10 | 70 | 169 | 1,1 | 6,5 |
  | 50 | 292 | 367 | 2,4 | 6,5 |
  | 100 | 581 | 2.874 | 19,4 | 6,8 |
  | 200 | 1.119 | 2.874 | 18,7 | 6,5 |
  | 500 | 3.818 | 3.828 | 24,6 | 6,4 |

  Nguồn: cột `rev-list` đo 09:43Z 07-11-2026; số commit đọc do review lượt 5 đo bằng hai mô phỏng độc lập trên Windows
  và phiên soạn spec đo lại khớp từng số trên Linux (WSL2, nhân `6.18.33.2-microsoft-standard-WSL2`, Git 2.43.0, Python 3.12.3, `nproc` 12, 07-11-2026),
  cả hai dùng mô phỏng tô màu theo mục tiêu 1 với `KhoObject` thật; mọi lượt ra `merge_bases = [S~N]`, bằng
  `git merge-base --all`. Trên Windows, review lượt 5 đo `KhoObject` thật với N = 100: hết deadline 60 giây sau 1.035
  object (59,853 giây, khoảng 58 ms một object); N = 10 xong trong 6,3–7,9 giây (169 object). Bộ kiểm admission thật
  chạy trên `ubuntu-latest` (`.github/workflows/ops-thu-hoi-admission.yml`); tốc độ của runner GitHub chưa đo.
- Giờ commit lệch làm chi phí tăng: phiên soạn spec dựng H có giờ commit năm 2023 (cũ hơn mọi commit trên master) ⇒ bước
  tô màu đọc **5.487** commit, tức cả lịch sử, trong 40–41 giây trên Linux, cả với N = 10 lẫn N = 50 (vẫn rc 0, merge-base
  đúng); H cũ hơn B một ngày ⇒ 242 commit, 1,5 giây.

## 1. write_set

- `ops/lease_publish.py`
- `ops/lease_publish_test.py`
- `.github/workflows/ops-thu-hoi-admission.yml` — chỉ khối chú thích ở đầu tệp; không đổi bước nào.
- `.claude/dev/doc_receipt_thu_hoi.py`
- `.claude/dev/doc_receipt_thu_hoi_test.py`

Điều kiện cấp lease: không lease nào còn hiệu lực giữ một đường dẫn trên (đo như packet A). Đo 06-11-2026 trên kho
có `refs/heads/*` khớp máy chủ: `ops/lease_publish.py`, `ops/lease_publish_test.py` và
`.github/workflows/ops-thu-hoi-admission.yml` ⇒ `NGƯỜI_GIỮ 0`. `.claude/dev/doc_receipt_thu_hoi.py` ⇒ `NGƯỜI_GIỮ 0`
(lượt quét bắt đầu 16:54Z) và `.claude/dev/doc_receipt_thu_hoi_test.py` ⇒ `NGƯỜI_GIỮ 0` (17:01Z). Hai lượt trước đó
bị chốt fail-close chặn vì máy chủ thêm nhánh giữa lượt quét; làm mới cache rồi chạy lại ngay thì ra kết quả trên.
r2–r10 không quét lại. Người cấp lease đo lại cả năm đường dẫn ngay trước khi cấp (L5).

## 2. ngoai_pham_vi

- Luật theo ID lease (R3/R4) và việc kiểm lại lúc land (R5): thuộc A1b (#656) và bên kiểm lúc land (#499 C1,
  #1179), vòng 1 Q5. Packet này chỉ ghi vào receipt dữ kiện để R5 dùng.
- `SO_THU_HOI_KICH_HOAT` giữ `False`; luật "chế độ chưa kích hoạt đòi tập revocation rỗng ở S và T" giữ nguyên.
- Chuyển tiếp Q13 (marker mới đòi `base_sha_before_add == S`) giữ nguyên. PR thêm tệp policy và marker vẫn cần S
  đúng bằng base của sự kiện; đó là việc của A1, rất hiếm, không phải nguồn sync hằng ngày.
- Các lệnh khác của `ops/lease_publish.py` (`check`, `body`, `kiem-github`, `ai-dang-giu`) và các bước của workflow.
- Đổi `KhoObject.doc` sang một tiến trình `cat-file --batch` dùng chung: không làm ở packet này; hiệu năng đạt bằng
  cách đọc ít object hơn (mục tiêu 1), đo ở B17.
- Hiệu năng không bảo đảm ở ba chỗ: đồ thị criss-cross dài; bộ kiểm chạy trên Windows với H tụt sau master từ khoảng
  100 commit first-parent trở lên (mục 0: 2.874 commit phải đọc, khoảng 58 ms một object); và H có giờ commit cũ hơn
  nhiều so với lịch sử master (mục 0: đọc cả lịch sử, chi phí lớn dần theo master). Bước lọc cực đại chỉ chạy khi có
  ≥ 2 ứng viên và chịu chung ngân sách. Chạm trần hay hết deadline ⇒ 12; PR hoà base, hoặc commit lại với giờ hiện
  tại, là hết. Tính đúng của criss-cross do B5 đo; B17 dựng H một cha nên chỉ có một merge-base.
- Vùng so sánh **không** gồm `ops/leases/**` (vòng 2 Q8). A1b phải mở rộng vùng khi bộ kiểm bắt đầu đọc lease.
- Đặc tả đã đóng băng (r9 của `THU-HOI-LEASE-VA-CAP-LAI`, r5 của `LAND-DOC-RECEIPT-THU-HOI-C1a1a`) và đặc tả #1179.
- WP1174 (#1174, bộ duyệt C6 chờ chủ kho, đo 15:0xZ 06-11-2026: chưa cấp lease) sửa `kiem-merge` trong
  `.claude/dev/packet_loop.py`. Packet này không thích nghi trước với thay đổi ấy: nếu WP1174 land trước khi B merge,
  điều kiện merge của B được đánh giá bằng mã canonical tại thời điểm merge.
- Ngoại lệ closure `ADR-0032` kiểu WP1174: không xin. Đo 02:43Z 07-11-2026 trên `origin/master` `9607e3eb`: dưới
  `ops/leases` có **179** tệp, gồm **175** tệp `.yaml`/`.yml` mà bộ quét lease xét và **4** tệp nháp `.yaml.nhap` mà
  bộ quét bỏ qua (09:43Z trên `132d376c`: vẫn 179). `git grep -n -E '^\s*(ngoai_le_closure|closure_exception)\s*:'
  origin/master -- ops/leases` ra **3** tệp có khối `ngoai_le_closure` (`wp741-r3-g3-claude-20261015.yaml`,
  `wp741-r3-g4-claude-20261015.yaml`, `wp741-r3-g5-claude-20261016.yaml`, đều ở dòng 51, đều thuộc 175 tệp được xét),
  cả ba có `expiry: '2026-10-22T00:00:00Z'` nên **0** khối còn hiệu lực lúc đo. "Có khai báo" và "còn hiệu lực" là hai
  số khác nhau; số thứ hai đo theo `expiry` so với giờ đo, không chứng nhận quyền LIVE.

## 3. Bảng ba trạng thái — đóng, mọi bước mới phải theo

Bài học của lớp `phan-loai-vang-va-khong-do-duoc` (mục 7): "không thấy" và "không đo được" phải là hai nhánh khác
nhau trong mã, mỗi nhánh có ca test riêng.

| bước | kết quả "có" | kết quả "không" (đo được) | không đo được ⇒ rc 12 |
|---|---|---|---|
| tô màu hai phía (S, H) | tập merge-base cực đại đúng bằng `[S]` ⇒ S là tổ tiên H ⇒ chế độ `to_tien` | tập cực đại khác `[S]`: có ≥ 1 phần tử ⇒ chế độ `merge_base`; rỗng (lịch sử không chung gốc) ⇒ rc 12, nhãn `KHONG_CO_MERGE_BASE` | vượt `max_commits_merge_base` hoặc `max_unique_objects`, hết deadline reader, thiếu object, object băm không khớp tên, header commit hỏng, thiếu dòng `committer`, có hơn một dòng `committer`, hoặc giây trong dòng ấy không phải số nguyên |
| đếm cạnh (chỉ chế độ `to_tien`) | `KhoObject.to_tien(S, H)` như nền ⇒ `canh_ancestry` | — (bước trước đã chứng minh S là tổ tiên) | vượt `max_parent_path_edges` và mọi lỗi bộ đọc, như nền |
| so vùng (chỉ chế độ `merge_base`) | mọi merge-base có vùng bằng vùng tại S ⇒ đi tiếp các phép kiểm cũ trên T | một merge-base lệch ⇒ rc 12, nhãn `VUNG_LECH`, SHA của merge-base lệch đầu tiên và đường dẫn lệch đầu tiên của nó ("đầu tiên" theo thứ tự sắp tăng: SHA theo chuỗi hex, đường dẫn theo chuỗi) | `tim`/`namespace` gặp tổ tiên không phải thư mục, đọc object lỗi, tree có entry không hợp lệ (tên không phải UTF-8, trùng, mode lạ) |

`refs/replace` và graft của kho nguồn **không có hiệu lực** với mọi bước trên: `KhoObject` đọc bằng
`cat-file --batch --no-replace-objects` trong `GIT_DIR` tạm cô lập và lấy cạnh từ bytes đã băm (đo 07-11-2026 trên
`9607e3eb`: `ops/lease_publish.py` dòng 1616 và 1913; ca t129 khẳng định cạnh gốc đọc đúng khi có replace; review lượt 2
dựng được replace làm Git chọn merge-base khác mà bộ đọc vẫn đọc cạnh thật). Kho nguồn shallow ⇒ 12 ngay khi dựng
`KhoObject` (dòng 1838), như hiện có. Mọi bước mới dùng cùng bộ đọc ấy.

Không bước mới nào được trả 0 khi một phép đo của nó không đo được, và không lỗi đọc vùng nào được đổi thành bản đồ
rỗng hay "vắng".

## 4. muc_tieu

1. `ops/lease_publish.py` — hàm **tô màu hai phía** cho (S, H) trên bộ đọc có băm của `KhoObject`. Hợp đồng, viết đủ
   để thi công không phải đoán (review lượt 4 đã mô phỏng đúng văn bản này trên 350 cặp DAG 100 commit có giờ lệch và
   các góc đồ thị, không lệch `git merge-base --all` cặp nào):
   - **Cờ.** Mỗi commit mang tập cờ con của {`P_H`, `P_S`, `STALE`}. Khởi đầu H nhận `P_H`, S nhận `P_S` (S = H thì nhận
     cả hai). Cờ truyền từ một commit xuống **mọi** cha bằng phép hợp (OR), không bao giờ xoá cờ đã có.
   - **Hàng đợi.** Ưu tiên theo committer timestamp, mới trước. Một commit được đưa vào hàng đợi mỗi khi nó **nhận thêm**
     cờ mới (kể cả khi đã được xử lý trước đó), nên giờ lệch chỉ ảnh hưởng hiệu năng, không ảnh hưởng tập kết quả (B5b).
   - **Ứng viên.** Khi lấy một commit ra: nếu nó có cả `P_H` lẫn `P_S` và **chưa** có `STALE` thì ghi nó là ứng viên rồi
     thêm `STALE` cho chính nó; commit có đủ hai cờ mà đã `STALE` **không** được ghi là ứng viên (B5d). Sau đó truyền tập
     cờ hiện tại của nó xuống các cha.
   - **Dừng** khi trong hàng đợi không còn commit nào chưa `STALE` (hàng đợi rỗng cũng dừng).
   - **Lọc cực đại.** Một ứng viên ⇒ nó là merge-base duy nhất. Từ hai ứng viên trở lên ⇒ bỏ ứng viên là tổ tiên của
     một ứng viên khác, kiểm bằng cùng bộ đọc trong cùng ngân sách, không dùng timestamp để suy quan hệ tổ tiên.
   - **Giờ commit.** Đọc từ đúng một dòng header cấp đầu `committer <tên> <email> <giây> <múi giờ>` trước dòng trống
     đầu tiên của bytes đã băm; dòng tiếp nối (bắt đầu bằng dấu cách, như trong `gpgsig`, `mergetag`) không phải dòng
     header mới. Thiếu dòng, nhiều hơn một dòng, hay `<giây>` không phải số nguyên ⇒ 12 (B5c, B1c). Không lấy mặc định
     0, không để `ValueError` hay lỗi Python khác thoát ra ngoài `Chan`. Phép kiểm này áp cho **mọi** commit được đọc,
     kể cả commit chỉ đọc để xếp vào hàng đợi.
   - **Ngân sách.** Khoá mới `max_commits_merge_base` = **50.000** trong `NGAN_SACH_MAC_DINH`, đếm số commit **phân biệt
     đã đọc** trong một lần tô màu cộng lọc, kể cả commit chỉ đọc để lấy timestamp; kiểm trước khi đọc commit kế tiếp;
     vượt ⇒ 12 nêu tên khoá. Căn cứ: #1179 đo toàn lịch sử master **5.444** commit, 8.480.418 byte (07:23Z 06-11-2026
     trên `889334fb`; review lượt 2 đo lại cùng hai số), tức trần dư khoảng 9 lần.
   - Hàm trả cả danh sách ứng viên **trước** khi lọc, để B5d đo luật ứng viên.

   Kết quả ba trạng thái theo bảng mục 3. Không gọi `git merge-base` hay Git plumbing nào khác.
2. `ops/lease_publish.py` — `KhoObject.to_tien` giữ nguyên hành vi bên ngoài (ném 12 với thông báo *"không phải tổ
   tiên"* khi không phải tổ tiên) cho mọi chỗ gọi hiện có, gồm t129. Trong `lenh_kiem_thu_hoi_github`, nó **chỉ** được
   gọi sau khi bước tô màu ra chế độ `to_tien`, để lấy `canh_ancestry` như nền.
3. `ops/lease_publish.py` — hàm vùng của một commit: bản đồ `ops/thu-hoi/**` qua `KhoObject.namespace` (entry trực
   tiếp, bộ `(mode, kiểu, OID)`), cộng mục `PATH_POLICY_CLOSURE` qua `KhoObject.tim` (vắng ⇒ không có khoá; tổ tiên
   không phải thư mục ⇒ 12). `tim` trả `(mode, OID, kiểu)` còn `namespace` và receipt dùng `(mode, kiểu, OID)`:
   hàm vùng phải đổi về một thứ tự trước khi so. Hàm này **chỉ** được gọi ở chế độ `merge_base`, cho S và cho từng
   merge-base. Ở chế độ `to_tien` bộ kiểm không gọi hàm vùng; ngoài các phép đọc của bộ kiểm nền, nó chỉ đọc thêm các
   commit của bước tô màu. Ba phép đọc tại S của bộ kiểm nền giữ nguyên ở **cả hai** chế độ (đo 07-11-2026 trên
   `9607e3eb`): `kho.namespace(tree_S, THU_MUC_SO)` cho append-only (dòng 2364), `kho.tim(tree_S, PATH_POLICY_CLOSURE)`
   khi T có marker mới theo Q13 (dòng 2400), `kho.tim(tree_S, PATH_BO_KIEM)` cho receipt (dòng 2411).
4. `ops/lease_publish.py` — `lenh_kiem_thu_hoi_github` thay dòng `canh = kho.to_tien(S, H)` (dòng 2361) bằng mục tiêu
   1–3; mọi phép kiểm còn lại (append-only S→T, validator namespace T, Q13, chế độ chưa kích hoạt) giữ nguyên thứ tự
   và mã thoát.
   **Bất biến tương thích — miền và phép chiếu viết tường minh.**
   - *Miền:* S là tổ tiên của H; **mọi** phép đọc và xác minh của bộ kiểm mới — cả các phép đọc của nền lẫn các commit
     đọc thêm ở bước tô màu — đều thành công; và không chạm trần ngân sách nào ở bất kỳ bước nào.
   - *Trên miền ấy,* bộ kiểm mới và bộ kiểm nền cho cùng: rc; thông báo lỗi khi rc ≠ 0; dòng `THU_HOI_ADMISSION` sau
     khi bỏ trường `quan_he=` và **giá trị** của `object đã băm=`; và receipt sau phép chiếu dưới đây.
   - *Phép chiếu receipt:* bỏ `schema_version` (nền 1, mới 2), `so_object_da_doc`, `tong_bytes`, `thoi_diem_utc` và ba
     khoá mới; với `ngan_sach`, dict mới bỏ đúng khoá `max_commits_merge_base` phải bằng dict của nền. Mọi khoá v1 còn
     lại phải bằng nhau. Khi cần so nguyên văn trên cùng một đầu vào thì cố định đồng hồ, như review lượt 4 đã làm.
   - *Ngoài miền ấy,* bộ kiểm mới có thể trả 12 ở chỗ nền trả 0: do chạm trần ở **bất kỳ** bước nào, hoặc do một commit
     đọc thêm không qua xác minh — băm lệch, thiếu object, header hay dòng `committer` hỏng (ca B1c). Tức chặt hơn nền,
     không bao giờ lỏng hơn, vì mọi phép kiểm của nền vẫn chạy.
   Receipt lên `schema_version` **2** với ba khoá mới:
   - `quan_he_S_H`: `"to_tien"` hoặc `"merge_base"`;
   - `merge_bases`: danh sách SHA40 không trùng, sắp tăng; chế độ `to_tien` ⇒ đúng `[S]`;
   - `vung_tai_S`: chế độ `to_tien` ⇒ `null` (không đo, vì không cần); chế độ `merge_base` ⇒ bản đồ vùng đã so, khoá
     là đường dẫn, giá trị `[mode, kiểu, OID]`.

   `canh_ancestry`: số nguyên ở chế độ `to_tien`, `null` ở chế độ `merge_base`. Dòng in `THU_HOI_ADMISSION …` thêm
   **một token** `quan_he=<giá trị>` đứng riêng, cách phần còn lại của dòng bằng khoảng trắng.
5. `ops/lease_publish_test.py` — sửa ca con của t133 đang khẳng định *"S không tổ tiên H phải 12"* (đo 07-11: dòng
   6580 trên `9607e3eb`): ca ấy thành "S không tổ tiên H, vùng bằng nhau ⇒ rc 0, `merge_base`", và thêm một ca
   vùng lệch ⇒ 12. Thêm các ca ở mục 5, mỗi đột biến đăng ký vào bảng đột biến sẵn có của tệp (cùng khuôn với mục
   `C1-tim-to-tien-non-tree-la-vang`). Cập nhật phép kiểm tĩnh của workflow (t137) cho B10. Sửa mọi chốt cố định đếm
   khoá ngân sách hoặc khoá receipt cho khớp khoá mới — đo 07-11-2026: t138 dòng 7061 đòi `len(d["ngan_sach"]) == 8`
   (sẽ là 9), tập khoá receipt ở t138 dòng 7053–7057 (một phép kiểm tập con, không phải tập đóng); executor tìm đủ bằng
   `rg -n 'ngan_sach|schema_version|canh_ancestry' ops/lease_publish_test.py` và ghi danh sách chốt đã sửa vào handoff.
6. `.github/workflows/ops-thu-hoi-admission.yml` — trong khối chú thích đầu tệp, thay câu cũ *"Bộ kiểm còn đòi S là
   tổ tiên của H — đó là thiết kế fail-close giữ nguyên theo quyết định chủ kho cho #618 (đường (a)), không phải
   dương tính giả."* bằng **đúng** câu mới sau (chép nguyên văn, được ngắt dòng tuỳ ý):
   *"Bộ kiểm không còn đòi S là tổ tiên của H (ADR-0066): khi S không phải tổ tiên của H, vùng bộ kiểm đọc phải giống
   hệt tại S và tại mọi merge-base của (S, H), rồi mọi phép kiểm chạy trên T = tree(H)."*
   Không đổi dòng nào ngoài khối chú thích; không viết cú pháp biểu thức Actions trong chú thích.
7. `.claude/dev/doc_receipt_thu_hoi.py` — nhận receipt v1 (đúng 38 khoá như hiện nay, đo 07-11-2026 trên `9607e3eb`)
   **và** v2 (đúng 41 khoá), mỗi phiên bản là một tập khoá đóng riêng. Luật riêng của v2: `quan_he_S_H` thuộc hai giá
   trị trên; `merge_bases` là danh sách SHA40 không rỗng, không trùng, sắp tăng; `to_tien` ⇒ `merge_bases == [S]`,
   `canh_ancestry` là số nguyên (không phải `bool`) ≥ 0 và `vung_tai_S` là `null`; `merge_base` ⇒ `canh_ancestry` là
   `null`, S không nằm trong `merge_bases` và `vung_tai_S` là dict khoá chuỗi, mỗi giá trị là danh sách đúng 3 phần tử:
   mode thuộc `100644` `100755` `120000` `160000` `040000`, kiểu thuộc `blob` `tree` `commit`, OID là SHA40. Module giữ
   thuần JSON: không git, không mạng; tập import cho phép giữ nguyên như `ca_tinh` đang kiểm (`argparse`, `json`,
   `re`, `sys`).
8. `.claude/dev/doc_receipt_thu_hoi_test.py` — các ca B11, B12 ở mục 5; thêm fixture v2 (`to_tien` và `merge_base`)
   vào đầu vào của `ca_tinh`; thêm đột biến từng trường cho ba khoá mới vào bảng sẵn có (`_theo_truong`), và đột biến
   riêng cho từng vị từ con của `merge_bases` và `canh_ancestry` (sắp tăng, không trùng, S không nằm trong tập, không
   phải `bool`, không âm).

## 5. nghiem_thu

Mọi ca "đỏ" kèm một đột biến làm ca đổi màu (L3). Fixture dựng đồ thị Git thật trong thư mục tạm, như t133, và gọi
bộ kiểm qua đúng lối vào CLI mà t133 dùng (`_goi_main(mod, "kiem-thu-hoi-github", …)`), để cùng một ca chạy được trên
mã nền lẫn mã ứng viên; riêng B5d gọi thẳng hàm tô màu (mục tiêu 1) vì nó đo danh sách ứng viên trước khi lọc. Ngân
sách nhỏ và seam `sau_cat_file` được tiêm qua thuộc tính module, như t133 tiêm `DESCRIPTOR_Q13_SHA256` (API nội bộ,
không có đường CLI); seam `sau_cat_file` dùng theo khuôn của t130. "Thông báo có nhãn X" nghĩa là stderr chứa nguyên
chuỗi X.

| # | ca | kỳ vọng | đột biến phải làm ca đổi màu |
|---|---|---|---|
| B1 | S là tổ tiên H; H là con trực tiếp của S | rc 0; receipt có `schema_version` = 2 (số nguyên), `quan_he_S_H = to_tien`, `merge_bases = [S]`, `canh_ancestry` = 1, `vung_tai_S = null`, `ngan_sach.max_commits_merge_base` = 50000; dòng `THU_HOI_ADMISSION` có đúng một token `quan_he=to_tien` | `amb-m01` luôn đi chế độ `merge_base` ⇒ `quan_he_S_H` khác ⇒ ca đỏ; các đột biến đầu ra ở ma trận mục 5 |
| B1b | S có `.github/coordination` là **tệp thường**; H là con của S và xoá tệp ấy; S là tổ tiên H | rc 0, `to_tien`, `vung_tai_S = null` (nền cũng rc 0 — trong miền của bất biến tương thích) | `amb-m13` gọi hàm vùng cả ở chế độ `to_tien` ⇒ `tim` gặp tổ tiên không phải thư mục ⇒ rc 12 ⇒ ca đỏ |
| B1c | S là tổ tiên H qua đồ thị `B → R_bad → S → H`, mọi tree rỗng; `R_bad` là commit có giây trong dòng `committer` không phải số nguyên, lưu bằng `git hash-object -t commit --literally -w` (ngoài miền của bất biến tương thích) | rc 12, thông báo nêu dòng `committer` hỏng và OID của `R_bad` (nền rc 0 — chặt hơn nền có chủ đích, mục tiêu 4) | `amb-m18` chỉ kiểm giờ commit khi lấy commit ra khỏi hàng đợi, không kiểm khi đọc để xếp hàng ⇒ `R_bad` chỉ được xếp hàng rồi bước tô màu dừng ⇒ rc 0 ⇒ ca đỏ |
| B2 | H rẽ từ B, master đi tiếp và đổi tệp ngoài vùng; vùng vắng ở S và B | rc 0; `schema_version` = 2, `merge_base`, `merge_bases = [B]`, `canh_ancestry = null`, `vung_tai_S = {}` (oracle: `git ls-tree` của hai đường dẫn vùng tại S rỗng); dòng `THU_HOI_ADMISSION` có đúng một token `quan_he=merge_base` | `amb-m02` bắt lại `to_tien` ⇒ rc 12 ⇒ ca đỏ; các đột biến đầu ra ở ma trận mục 5 |
| B2b | Vùng **không rỗng** và bằng nhau ở S và B: dùng S2 của fixture t133 (`_mau_t133`: policy `.github/coordination/change-impact.v1.json` là JSON object, marker `ops/thu-hoi/_ngoai-le-closure.retired.yaml` đã có ở S2) làm B; S' là con của S2 đổi một tệp ngoài vùng; H là con của S2 đổi một tệp ngoài vùng (như `H_them_tren_S2`) | rc 0, `merge_base`, `merge_bases = [S2]`, và `vung_tai_S` **bằng đúng** bản đồ dựng từ `git ls-tree S' -- ops/thu-hoi/ .github/coordination/change-impact.v1.json`: khoá là đường dẫn đầy đủ, giá trị `[mode, kiểu, OID]` (hai khoá) | `amb-m19-vung-tai-S-sai-tuple` (tại chỗ phát receipt, đổi OID của một entry thành OID của entry kia) ⇒ ca đỏ |
| B3 | Master thêm `.github/coordination/change-impact.v1.json` sau B | rc 12, nhãn `VUNG_LECH`, thông báo nêu đường dẫn `.github/coordination/change-impact.v1.json` (oracle: `git diff --name-only B S -- ops/thu-hoi/ .github/coordination/change-impact.v1.json` ra đúng đường ấy), không receipt | `amb-m03` bỏ cổng so vùng ⇒ rc khác 12 hoặc thiếu nhãn ⇒ ca đỏ (chức năng); các đột biến chỉ đổi giá trị ở ma trận mục 5 |
| B3b | Master thêm một bản ghi thu hồi vào `ops/thu-hoi/` sau B; H không có nó | rc 12, nhãn `VUNG_LECH`, thông báo nêu đường dẫn của bản ghi ấy (oracle như B3), không receipt | `amb-m03` bỏ cổng so vùng ⇒ append-only S→T chạy trước và trả **8** (bản ghi ở S vắng ở T) ⇒ ca đỏ |
| B4 | B và S có cùng một bản ghi; H **xoá** bản ghi ấy; S không là tổ tiên H | rc 8, thông báo có `append-only` | `amb-m04` bỏ phép append-only ⇒ tới chốt chưa kích hoạt, rc 12 ⇒ ca đỏ |
| B5 | Criss-cross: hai merge-base, merge-base đứng đầu theo thứ tự sắp có vùng bằng S, cái còn lại lệch (review lượt 1 đã dựng được topology này) | rc 12, nhãn `VUNG_LECH`, thông báo nêu SHA của merge-base lệch | `amb-m05` chỉ so merge-base đầu ⇒ rc 0 ⇒ ca đỏ |
| B5b | Giờ commit lệch: đồ thị `H→Y→C`, `S→C`, `C→R`, committer time H = 10, Y = 1, S = 5, C = 4, R = 3 (Y cũ hơn chính tổ tiên của nó); không có tệp vùng nào | rc 0, `merge_base`, `merge_bases = [C]`, bằng tập mà `GIT_NO_REPLACE_OBJECTS=1 git merge-base --all S H` trả trên cùng fixture | `amb-m15` không đưa lại vào hàng đợi commit đã xử lý khi nó nhận thêm cờ ⇒ C không bao giờ thành ứng viên ⇒ tập khác `[C]` ⇒ ca đỏ |
| B5c | Cha thứ nhất của S (phía S, không là tổ tiên của H) là commit có dòng `committer` mà phần giây không phải số nguyên, lưu bằng `git hash-object -t commit --literally -w`; không có tệp vùng nào | rc 12, thông báo nêu dòng `committer` hỏng và OID ấy | `amb-m16` lấy giờ mặc định 0 khi không đọc được ⇒ bước tô màu chạy tiếp, vùng vắng ở mọi nơi ⇒ rc 0 ⇒ ca đỏ |
| B5d | Gọi thẳng hàm tô màu: `R0…R9` tuyến tính (committer time 100…109), B là con của R9 (110), S là con của B (120), X là một gốc riêng (1), H (130) có hai cha B và X | danh sách ứng viên trước khi lọc đúng bằng `[B]`; tập merge-base `[B]` | `amb-m17` ghi cả commit đã `STALE` có đủ hai cờ làm ứng viên ⇒ danh sách trước lọc thành `[B, R9, R8, …, R0]` ⇒ ca đỏ (tập sau lọc vẫn `[B]`, nên ca phải đo danh sách trước lọc) |
| B6 | S và H không chung gốc | rc 12, nhãn `KHONG_CO_MERGE_BASE` | `amb-m06` coi "0 merge-base" là đạt ⇒ rc 0 ⇒ ca đỏ |
| B7 | `max_commits_merge_base` nhỏ hơn số commit bước tô màu phải đọc | rc 12, thông báo nêu `max_commits_merge_base` | `amb-m07` nuốt lỗi vượt ngân sách ⇒ rc 0 ⇒ ca đỏ |
| B8a | Kho nguồn có một `refs/replace` làm `git merge-base --all` (vốn theo replace) trả một commit có vùng bằng S, trong khi merge-base thật trên đồ thị đã băm có vùng lệch | rc 12, nhãn `VUNG_LECH`, thông báo nêu SHA của merge-base **thật** | `amb-m08` tính merge-base bằng `git merge-base --all` trên kho nguồn ⇒ rc 0 ⇒ ca đỏ |
| B8b | Cha thứ nhất của S (thuộc phía S, mới hơn merge-base, không là tổ tiên của H) bị seam `sau_cat_file` đổi bytes, nên băm không khớp tên | rc 12, thông báo băm lệch của bộ đọc nêu OID ấy | `amb-m14` bước tô màu đọc cha bằng đường không băm lại ⇒ không có thông báo băm lệch ⇒ ca đỏ |
| B9 | S là tổ tiên H; `max_parent_path_edges` nhỏ hơn số cạnh của đường witness | rc 12, thông báo `đường parent > … cạnh`, **không** có `KHONG_CO_MERGE_BASE` hay `VUNG_LECH`, không receipt | `amb-m09` nuốt lỗi ngân sách của bước đếm cạnh rồi đi tiếp chế độ `merge_base` ⇒ rc 0 ⇒ ca đỏ (chức năng); `amb-m34`, `amb-m35` chỉ chèn một nhãn vào thông báo lỗi ⇒ ca đỏ ở đúng vế âm tương ứng (ma trận mục 5) |
| B10 | Chú thích workflow, đo trên văn bản đã nối dòng từng đoạn (bỏ `#` và khoảng trắng đầu mỗi dòng chú thích, dòng `#` trống ngắt đoạn, gộp khoảng trắng): vế dương có nguyên câu mới ở mục tiêu 6; vế âm không còn cụm *"Bộ kiểm còn đòi S là tổ tiên của H"* | cả hai vế đạt | `amb-m10` ghi lại câu cũ ⇒ vế âm đỏ; bỏ *"không còn"* khỏi câu mới ⇒ vế dương đỏ; đổi *"mọi merge-base"* thành *"một merge-base"* ⇒ vế dương đỏ; cắt hậu tố *", rồi mọi phép kiểm chạy trên T = tree(H)."* ⇒ vế dương đỏ; ngắt dòng lại giữ nguyên chữ ⇒ vẫn đạt |
| B11 | `doc_receipt_thu_hoi`: v1 hiện có ⇒ `ok`; v2 `to_tien` ⇒ `ok`; v2 `merge_base` ⇒ `ok`; mỗi ca sau ⇒ `do`: v2 thiếu `merge_bases`, thừa một khoá, `to_tien` với `merge_bases ≠ [S]`, `merge_base` với `canh_ancestry` số, `to_tien` với `vung_tai_S` là dict, `merge_base` với `vung_tai_S = null`, `vung_tai_S` có giá trị 2 phần tử, `merge_bases` chưa sắp tăng, `merge_bases` có phần tử trùng, `merge_base` với S nằm trong `merge_bases`, `canh_ancestry = true`, `canh_ancestry = -1`, `schema_version = 3` | như cột trái | `amb-m11` bỏ kiểm tập khoá v2 ⇒ ca thiếu/thừa khoá thành `ok` ⇒ ca đỏ; mỗi đột biến vị từ con của mục tiêu 8 làm đúng ca tương ứng thành `ok`; đột biến từng trường của `_theo_truong` cho ba khoá mới |
| B12 | `ca_tinh` chạy trên fixture v1 **và** hai fixture v2: tập import ⊆ {`argparse`, `json`, `re`, `sys`}, audit hook không ghi sự kiện nào, kết quả tất định | ca đạt | `amb-m12` thêm `import subprocess` ⇒ tập import lệch ⇒ ca đỏ; `amb-m12b` thêm một lời gọi `open(...)` chỉ trong nhánh xử lý v2 ⇒ audit hook ghi sự kiện ⇒ ca đỏ (đột biến này chỉ bị bắt khi fixture v2 có trong `ca_tinh`) |
| B13 | Toàn bộ `ops/lease_publish_test.py` và `.claude/dev/doc_receipt_thu_hoi_test.py` trên CI Linux của exact head báo `N/N` với hai số bằng nhau | lệch | — (bằng chứng dương, không tin `rc=0` một mình) |
| B14 | Windows, mục 6 | xanh theo `ADR-0060` M3 (a)–(c) | — |
| B15 | `ci-dot-bien-du.yml` thành công trên exact head, mọi job `success` (K7) | thiếu hoặc đỏ | — |
| B16 | Kích thước theo `nang_tran`: ≤ 6 tệp, ≤ 780 dòng thêm; không tệp ngoài `write_set` | vượt hoặc tệp lạ | thêm một tệp ⇒ đỏ |
| B17 | **Hiệu năng** trên **lịch sử thật**, trước merge, với đầu vào **ghim** theo mục "Đầu vào của B17" dưới đây; không phải tiêu chí về tính đúng của receipt (checkpoint lần 4) | **đạt** theo ba điều ở mục ấy cho mọi N bắt buộc: N ∈ {10, 50, 100} trên Linux; N ∈ {10, 50} trên `tra-luat-win`. N = 500 trên Linux, N = 100 và 500 trên Windows: ghi số đo, không nghiệm thu | một N bắt buộc không **đạt** ⇒ đỏ, bất kể lý do |
| B18 | Canary sau land, trên PR thật đầu tiên mà sự kiện `pull_request_target` của nó có S = `base.sha` không là tổ tiên của H (`git merge-base --is-ancestor S H` rc 1, `GIT_NO_REPLACE_OBJECTS=1`) | **đạt** khi đủ cả bốn: check `thu-hoi` success; receipt trong artifact của run qua validator C1a1a phiên bản mới (`kiem_json`, hợp đồng receipt workflow 41 khoá) với kết quả `ok`; `quan_he_S_H = merge_base`; `merge_bases` bằng danh sách đã sắp của `git merge-base --all S H` | **chưa đo được** tới khi có PR ấy. Mọi kết quả khác "đạt" ⇒ B18 đỏ, mở Issue điều tra kèm run ID, S, H, merge-base, rc, receipt và output validator; tiêu chí không tự xếp nguyên nhân. Người điều tra kết luận nguyên nhân; B18 chỉ đạt khi có một PR đạt. Người đo, mốc, cách gọi validator và nơi ghi: mục "Thi hành B18" dưới bảng |

**Đầu vào của B17 — ghim, không tuỳ thời điểm đo.** B17 không chọn PR thật, không đoán kết quả, và không phân loại
nguyên nhân: đầu vào cố định trên lịch sử bất biến, và kết quả đúng của nó đã được **đo** trước (bên dưới). Vì vậy mọi
kết quả khác "đạt" đều là đỏ.

- Kho đo: một clone thường của kho, không shallow, không `info/grafts`, không `refs/replace`, có commit S; mọi lệnh Git
  của runner chạy với `GIT_NO_REPLACE_OBJECTS=1`.
- S = `132d376cbbfea0692ff6db284753b33f437c637a` (cố định). Với mỗi N, B = `S~N` theo first-parent, và H là commit runner
  tạo bằng `git commit-tree`, **cha duy nhất là B**: tree = tree(B) cộng đúng một entry `100644 blob <oid>` tên
  `amb-b17-<N>.txt` ở gốc cây, blob là bytes ASCII `amb-b17 N=<N>` cộng một LF; tác giả và người commit đều là
  `amb-b17 <amb-b17@example.invalid>`, giờ `@1794042814 +0000` (giờ commit của S cộng 60 giây); thông điệp commit là
  `amb-b17 N=<N>` cộng một LF. Blob tạo bằng `git hash-object -w --stdin` (bytes giữ nguyên, không qua chuyển dòng),
  tree bằng `git mktree -z` từ `git ls-tree -z B` cộng một entry; commit tạo với `-c i18n.commitEncoding=UTF-8`, nên
  object commit không có header `encoding` (review lượt 6 đo: `i18n.commitEncoding=ISO-8859-1` thêm header ấy và đổi H).
- OID phải ra đúng như bảng dưới; lệch ở bất kỳ cột nào ⇒ runner dựng sai ⇒ lượt ấy đỏ, sửa runner rồi chạy lại.

  | N | B = `S~N` | H | T = tree(H) |
  |---:|---|---|---|
  | 10 | `8dc07047ffc00637c3ee9353b84c3c5abac189e9` | `3253b5406a0bedacabdc294d9b2b5f7c44270e25` | `7cfa8e36a888bdd3b385da7000e1fa875f4f8821` |
  | 50 | `ec1b18a2a007fc2e697249c727a2ca8391ab209e` | `a6d6cbb26c80f8dbcbeab04e443d31926f24a28f` | `13b707af2be2a961920a570b21a95f78153fca8d` |
  | 100 | `4397ee616273a97c1503e8359452aef4e78cd75a` | `0157f8bcc37e71972cecc2efdd1746635f061792` | `f47c13d701112fa42ed9be38cfb070aa1c4a56c1` |
  | 500 | `32a440cf3477f8953bef3dcd5ffe2c1803bf8a20` | `8d3a6a6bbfe034bf486bf348838ac3854dea74d2` | `1bf2d4a82dd25337281296cce21a9e4a98e1817a` |

- **Kết quả đúng đã đo** (phiên soạn spec, 07-11-2026, Linux như mục 0, mã nền `ops/lease_publish.py` blob tại
  `a98c8023`, bằng blob trên `origin/master` lúc đo). Ba phép đo này phủ mọi object bộ kiểm mới sẽ đọc với đầu vào ghim:
  1. Bước tô màu: mô phỏng theo mục tiêu 1 với `KhoObject` thật ⇒ `merge_bases = [B]` ở cả bốn N, khớp
     `git merge-base --all S H`; `git merge-base --is-ancestor S H` rc 1; số commit đọc như bảng mục 0.
  2. Phía S: bộ kiểm nền trên cặp tuyến tính (S, con của S có tree(S)) ⇒ rc 0, `TAP_THU_HOI_RONG`, 6 object.
  3. Vùng tại B và mọi phép kiểm trên T: bộ kiểm nền trên cặp tuyến tính (B, H) ⇒ rc 0, `TAP_THU_HOI_RONG`, 7 object, ở
     cả bốn N. Vùng tại S và tại B: `git ls-tree` của `ops/thu-hoi` và `.github/coordination/change-impact.v1.json` rỗng ở
     cả hai, tức vùng vắng và bằng nhau.

  Ba thành phần là số đo; rc 0 của bộ kiểm mới (chưa viết) là kết luận ghép từ chúng, chưa phải một lần chạy chương
  trình ấy. Review lượt 6 ghép cả ba trên cùng một `KhoObject` và một deadline, trên Windows: rc 0 ở N = 10 (176 object,
  7,3 giây) và N = 50 (375 object, 16,8 giây), và không object nào của đường ghép nằm ngoài ba phép đo.
- **Đạt**, cho mỗi N bắt buộc. B17 là **phép đo hiệu năng trên lịch sử thật** (checkpoint lần 4, đầu tệp). Runner chạy
  bộ kiểm mới `kiem-thu-hoi-github H --canonical-base S --nhanh-mac-dinh master --receipt <tệp>` trên kho đo. Đạt khi
  đủ ba điều:
  1. mã thoát 0;
  2. tệp receipt đọc được theo đúng cách `kiem_json` của validator C1a1a đọc receipt (`.claude/dev/doc_receipt_thu_hoi.py`:
     bytes không mở đầu bằng BOM UTF-8, giải mã UTF-8 strict, `json.loads` trên chuỗi đã giải mã), thêm điều kiện khoá
     trùng ⇒ lỗi, và kết quả là một object;
  3. trong object ấy, `quan_he_S_H` bằng chuỗi `merge_base` và `merge_bases` bằng mảng đúng một phần tử là chuỗi B của
     N ấy (so `==` trên giá trị JSON đã đọc).

  Mọi kết quả khác là đỏ, kể cả mã thoát 12 vì hết deadline hay vượt ngân sách. Không có loại "đầu vào không dùng được".
  B17 không dùng stdout để quyết định đạt; stdout vẫn được thu để ghi kèm (dưới đây).
- **B17 không bảo đảm** tính đúng của các trường khác trong receipt hay của các phép kiểm cũ trên T, và không thử khả
  năng bác đầu vào sai. Các bảo đảm ấy chia theo vai: **producer** (bộ kiểm phát đúng giá trị) — ma trận dưới đây và các
  ca chức năng B1–B9; **consumer** (validator C1a1a kiểm hình dạng và quan hệ nội tại) — B11; **tính thuần** của
  validator — B12; **run thật** — B18. Consumer, tính thuần và run thật không thay cho phép đo giá trị producer.

  **Ma trận nghĩa vụ đầu ra mới** (r11, sửa ở r12). Mỗi đầu ra mới hay đổi của bộ kiểm v2 (mục tiêu 3–4 và bảng ba
  trạng thái) có ca đo **giá trị** do producer phát ra, bằng oracle độc lập với mã ứng viên (không dùng hàm vùng hay bước
  tô màu của ứng viên làm oracle). Luật đột biến: mỗi khẳng định giá trị có ít nhất một đột biến **chỉ đổi giá trị phát
  ra** — sửa đúng giá trị ấy sau khi kết quả đã tính, giữ nguyên mã thoát, luồng xử lý và mọi trường khác — và đột biến
  ấy phải làm ca đỏ **ở chính khẳng định ấy**. Đột biến **chức năng** (đổi luồng hay mã thoát) giữ ở cột riêng; chúng đo
  hành vi, không được dùng làm bằng chứng cho khẳng định giá trị.

  | đầu ra | chế độ | ca đo giá trị | oracle | đột biến chỉ đổi giá trị phát ra | đột biến chức năng liên quan |
  |---|---|---|---|---|---|
  | `schema_version` = 2 | cả hai | B1, B2 | hằng số hợp đồng, so cả kiểu số nguyên | `amb-m22-schema-van-1` | — |
  | `quan_he_S_H` | `to_tien` / `merge_base` | B1 / B2, B2b | chế độ do fixture dựng | `amb-m28-phat-quan-he-nguoc` (phát giá trị của chế độ kia, giữ rc 0) | `amb-m01`, `amb-m02` |
  | `merge_bases` | `to_tien` | B1 (`[S]`) | S | `amb-m29-phat-merge-bases-H` (phát `[H]`, giữ rc 0 và `to_tien`) | `amb-m01` |
  | `merge_bases` | `merge_base` | B2 (`[B]`), B2b (`[S2]`) | `GIT_NO_REPLACE_OBJECTS=1 git merge-base --all S H` trên fixture | `amb-m25-merge-bases-phat-S` (phát `[S]`, giữ rc 0) | `amb-m15` (B5b, thuật toán) |
  | `vung_tai_S` | `to_tien` | B1, B1b (`null`) | hợp đồng | `amb-m26-vung-to-tien-khong-null` (phát `{}`) | `amb-m13` (B1b) |
  | `vung_tai_S` | `merge_base` | B2 (`{}`), B2b (hai khoá) | `git ls-tree` của hai đường dẫn vùng tại S trên fixture | `amb-m20-vung-tai-S-them-entry` (B2), `amb-m19-vung-tai-S-sai-tuple` (B2b) | — |
  | `canh_ancestry` | `to_tien` / `merge_base` | B1 (= 1) / B2 (`null`) | độ dài đường parent mà fixture dựng | `amb-m23-canh-hang-0` / `amb-m24-canh-so-o-merge-base` (phát 0) | — |
  | `ngan_sach.max_commits_merge_base` = 50000 | cả hai | B1 | hằng số hợp đồng | `amb-m27-receipt-bo-khoa-ngan-sach-moi` | — |
  | token `quan_he=<giá trị>` trên dòng `THU_HOI_ADMISSION` | cả hai | B1 (`quan_he=to_tien`), B2 (`quan_he=merge_base`) | chế độ do fixture dựng; tách dòng theo khoảng trắng, đếm đúng một token | `amb-m21-bo-token-quan-he` | — |
  | nhãn `VUNG_LECH` | `merge_base`, thất bại; vắng ở mọi lỗi khác | B3, B3b, B5, B8a; âm: B9 | vùng lệch do fixture dựng; B9 là lỗi ngân sách đếm cạnh ở chế độ `to_tien` | `amb-m30-doi-nhan-vung-lech` (thay nhãn bằng chuỗi khác, giữ rc 12, SHA và đường dẫn); `amb-m34-chen-nhan-vung-lech-vao-loi-b9` (chèn `VUNG_LECH` vào thông báo lỗi ngân sách, giữ rc 12, luồng, phần còn lại của thông báo và việc không có receipt) | `amb-m03`, `amb-m05`, `amb-m08` |
  | nhãn `KHONG_CO_MERGE_BASE` | thất bại; vắng ở mọi lỗi khác | B6; âm: B9 | đồ thị không chung gốc do fixture dựng; B9 như hàng trên | `amb-m31-doi-nhan-khong-co-merge-base` (B6; giữ rc 12); `amb-m35-chen-nhan-khong-co-merge-base-vao-loi-b9` (B9; chèn nhãn, giữ như `amb-m34`) | `amb-m06`, `amb-m09` |
  | SHA merge-base lệch trong thông báo | thất bại | B5, B8a | `GIT_NO_REPLACE_OBJECTS=1 git merge-base --all S H` trên fixture, chọn cái lệch | `amb-m33-thong-bao-sai-sha` (thay SHA bằng SHA của S, giữ nhãn và rc) | `amb-m05`, `amb-m08` |
  | đường dẫn lệch đầu tiên trong thông báo | thất bại | B3, B3b | `git diff --name-only B S -- ops/thu-hoi/ .github/coordination/change-impact.v1.json` trên fixture (ra đúng một đường ở cả hai ca) | `amb-m32-thong-bao-sai-duong-dan` (thay đường dẫn bằng chuỗi khác, giữ nhãn, SHA và rc) | `amb-m03` |

  Ba phép đọc tại S và các khoá v1 còn lại giữ hợp đồng của nền (bất biến tương thích, mục tiêu 4); ma trận này chỉ
  phủ phần v2 thêm hay đổi: mười một nhóm đầu ra, gồm hai nhãn lỗi mới và hai phần của thông báo `VUNG_LECH`.
- Ghi kèm: rc, toàn bộ stderr, dòng `THU_HOI_ADMISSION`, receipt, thời gian, `so_object_da_doc`, `tong_bytes`, số commit
  bước tô màu đã đọc, nền, phiên bản Python và Git.

**Thi hành B18.**

- **Người đo:** phiên điều phối đang giữ Mission #1264, hay phiên kế nhiệm được ghi trong handoff của nó. Người land
  packet này ghi B18 vào hồ sơ land ở trạng thái `chua_do_duoc`, kèm tên phiên nhận việc; chưa có người nhận thì việc
  land chưa xong (protocol §13.1).
- **Mốc:** mỗi lần phiên ấy làm việc, nó liệt kê các run của `ops-thu-hoi-admission.yml` kể từ commit land của packet
  này, và chọn PR đầu tiên thoả điều kiện ở hàng B18. Đo ngay khi run của PR ấy hoàn tất.
- **Gọi validator:** `kiem_json(<receipt trong artifact>, kho="ducthangho/tra-luat", nhanh="master",
  base_hien_hanh=<base SHA đọc lại từ PR>, head_hien_hanh=<head SHA đọc lại từ PR>)`; hai SHA đọc từ PR, không lấy từ
  receipt. Run dừng trước bước tải artifact (bộ kiểm rc khác 0) thì ghi rõ artifact không có và vì sao, không dựng
  output validator.
- **Nơi ghi và đọc lại:** một comment trên #1266 gồm run ID, attempt, check run ID, tên artifact, S, H, kết quả
  `git merge-base --all S H`, rc, output validator và kết luận đạt hay đỏ; phiên đọc lại comment ấy sau khi đăng. Đỏ ⇒
  chính phiên ấy mở Issue điều tra, trỏ về comment.
- Mission #1264 đóng trước khi có PR thoả điều kiện ⇒ nghĩa vụ B18 chuyển sang handoff của phiên điều phối kế tiếp; không
  được ghi B18 là đạt hay miễn.

**Năm vế L6 cho các tiêu chí khớp chuỗi:**

| tiêu chí | (a) dương / âm | (b) trọn mệnh đề, nối đoạn | (c) từng vị trí | (d) chữ / số | (e) đủ vị trí cổng |
|---|---|---|---|---|---|
| B10 | có cả hai vế | vế dương trọn câu mới, nối đoạn; vế âm dùng cụm lõi ngắn hơn câu cũ, chặt hơn chép nguyên câu | một khối chú thích | không có ngưỡng số | không phải lời khai về cổng |
| B12 | không còn là phép khớp chuỗi: dùng `ca_tinh` đo hành vi (import, audit hook) | không áp | không áp | không áp | không áp |
| nhãn `VUNG_LECH`, `KHONG_CO_MERGE_BASE` | dương trên thông báo mới; âm ở B9 (không được có hai nhãn) | nhãn là một token, không ngắt dòng | mỗi ca một nhãn | không có số | không áp |
| B17 "đạt" | dương: mã thoát 0 và hai trường đúng; âm: mọi kết quả khác | so giá trị JSON đã đọc, không khớp chuỗi trên stdout | từng N; hai trường riêng rẽ | `merge_bases` so nguyên mảng, OID 40 ký tự | không áp |

**Màu trên nền.** Chỉ ghi màu đã **đo**; không suy màu nền từ đọc mã.

- B10 (07-11-2026, `9607e3eb`): câu cũ **1** lần, cụm lõi **1** lần, `ADR-0066` **0** lần — cả hai vế đỏ, đúng màu.
- B1b (review lượt 2–4 đo trên mã nền): rc 0, `TAP_THU_HOI_RONG`, `canh_ancestry = 1`. Ca B1b trên nền đỏ vì receipt v1
  thiếu `quan_he_S_H`; rc nền 0 là bất biến phải giữ.
- B1c (review lượt 4 đo trên mã nền với đồ thị `B → R_bad → S → H`): nền rc 0; mô phỏng bước tô màu theo mục tiêu 1 ra
  rc 12 nêu dòng `committer` hỏng và OID của `R_bad`. Ca B1c trên nền đỏ đúng màu (ca đòi rc 12).
- B5b (review lượt 3 đo): CLI nền rc 12 *"không phải tổ tiên"* — đỏ đúng màu. Oracle Git trả C; mô phỏng có đưa lại vào
  hàng đợi cho `[C]`, bỏ đưa lại cho `[]` (phiên soạn spec, review lượt 3 và 4 đo độc lập).
- B5c (review lượt 4 đo): CLI nền rc 12 vì bước `to_tien` (S không là tổ tiên H) — đỏ đúng màu nhưng vì lý do khác
  thông báo kỳ vọng; mô phỏng ra 12 nêu `committer` và OID; đột biến giờ 0 ra rc 0.
- B5d (phiên soạn spec và review lượt 4 đo bằng mô phỏng): ứng viên trước lọc `[B]`; với `amb-m17` là
  `[B, R9, …, R0]`; 14 commit đọc ở cả hai. Trên mã nền hàm tô màu chưa tồn tại ⇒ "không đo được trên nền", đúng loại.
- B6 (review lượt 1 và 2 đo trên mã nền): rc 12 *"S không phải tổ tiên của H"*, thiếu nhãn `KHONG_CO_MERGE_BASE` — đỏ.
- B9 (review lượt 2–4 đo trên mã nền, `max_parent_path_edges = 1`): rc 12, `đường parent > 1 cạnh`, không nhãn mới —
  **xanh trên nền**, kể cả khi bước tô màu chạy trước; răng là `amb-m09` trên ứng viên.
- B12: `ca_tinh` hiện có xanh trên nền với fixture v1 (review lượt 1–4 đo); răng mới nằm ở `amb-m12b`.
- B17 trên nền: nền không có chế độ `merge_base`, nên với đầu vào của B17 nền trả 12 *"không phải tổ tiên"* — đỏ đúng
  như phải thế. Kết quả đúng của B17 lấy từ ba phép đo ở mục "Đầu vào của B17", không lấy từ nền chạy trên (S, H).
- Mọi ca còn lại: **chưa đo** màu nền. Executor đo ngay sau khi viết fixture, trước khi sửa bộ kiểm, và ghi vào
  handoff. Ca xanh trên nền là bất biến, răng của nó phải đến từ đột biến; ca đỏ trên nền phải đỏ bằng assertion của
  chính ca (không vì lỗi nạp module hay thiếu thuộc tính), trừ B5d vốn gọi một hàm chưa có trên nền.
- B13: chưa chạy toàn bộ suite trên nền ở phiên này; số ca nền lấy từ CI của base khi cấp lease.

### 5.1 Kho ID đóng băng

Danh tính của một ca là **hậu tố tên** dưới đây, không phải số thứ tự. Trong `ops/lease_publish_test.py` mọi ca đăng ký
bằng decorator `@ca` vào danh sách `CA` (`CA` ở dòng 72, hàm `ca` ở dòng 79–81). Đo 01:14Z 07-11-2026 trên
`origin/master` `9607e3eb` bằng AST (hàm có decorator `ca`), review lượt 2–4 đo lại bằng `len(CA)`: **285** ca, 285 tên
duy nhất, số lớn nhất `t237`. Tên có dạng `t<số>[chữ]_…`: 280 tên khớp `t[0-9]+_`, 5 tên có hậu tố chữ sau số
(`t02b_…`, `t02c_…`, `t02d_…`, `t55a_…`, `t55b_…`). Đếm ca thì đếm `CA`, không đếm theo mẫu tên; đếm hàng nghiệm thu
thì đếm hàng của bảng mục 5, kể cả hàng có hậu tố chữ (B1b, B1c, B2b, B3b, B5b, B5c, B5d, B8a, B8b). Executor chọn số kế
tiếp còn trống trên base của lease, giữ nguyên hậu tố. Mỗi hậu tố phải khớp **đúng một** hàm; không khớp hoặc khớp hai
⇒ runner đỏ. Mỗi đột biến có ID riêng, đăng ký vào bảng đột biến sẵn có của tệp test tương ứng. Các đột biến chỉ đổi
giá trị của ma trận mục 5 (`amb-m19`…`amb-m35`) đăng ký cho đúng các ca đích ghi ở ma trận; một ID có thể có nhiều ca
đích, và với mỗi ca đích, ca phải đỏ ở chính khẳng định giá trị mà ma trận gán.

| ca | tệp | hậu tố / tên ca | ID đột biến | nền |
|---|---|---|---|---|
| B1 | `ops/lease_publish_test.py` | `_amb01_to_tien_giu_nguyen` | `amb-m01-luon-di-merge-base`, `amb-m21-bo-token-quan-he`, `amb-m22-schema-van-1`, `amb-m23-canh-hang-0`, `amb-m26-vung-to-tien-khong-null`, `amb-m27-receipt-bo-khoa-ngan-sach-moi` | cả hai |
| B1b | `ops/lease_publish_test.py` | `_amb01b_to_tien_khong_doc_vung_S` | `amb-m13-luon-goi-ham-vung` | cả hai |
| B1c | `ops/lease_publish_test.py` | `_amb01c_to_tien_committer_hong_o_commit_doc_them` | `amb-m18-khong-kiem-committer-khi-xep-hang` | cả hai |
| B2 | `ops/lease_publish_test.py` | `_amb02_merge_base_vung_bang_nhau` | `amb-m02-bat-lai-to-tien`, `amb-m20-vung-tai-S-them-entry`, `amb-m24-canh-so-o-merge-base`, `amb-m25-merge-bases-phat-S` (cùng `amb-m21`, `amb-m22` ở ca đích thứ hai) | cả hai |
| B2b | `ops/lease_publish_test.py` | `_amb02b_merge_base_vung_khong_rong` | `amb-m19-vung-tai-S-sai-tuple` | cả hai |
| B3 | `ops/lease_publish_test.py` | `_amb03_policy_lech_sau_merge_base` | `amb-m03-bo-cong-so-vung` | cả hai |
| B3b | `ops/lease_publish_test.py` | `_amb03b_thu_hoi_moi_tren_master` | `amb-m03-bo-cong-so-vung` (cùng đột biến, ca đích thứ hai) | cả hai |
| B4 | `ops/lease_publish_test.py` | `_amb04_append_only_qua_merge_base` | `amb-m04-bo-append-only` | cả hai |
| B5 | `ops/lease_publish_test.py` | `_amb05_criss_cross_mot_base_lech` | `amb-m05-chi-so-base-dau` | cả hai |
| B5b | `ops/lease_publish_test.py` | `_amb05b_lech_gio_dua_lai_hang_doi` | `amb-m15-khong-dua-lai-hang-doi` | cả hai |
| B5c | `ops/lease_publish_test.py` | `_amb05c_committer_hong` | `amb-m16-committer-hong-thanh-0` | cả hai |
| B5d | `ops/lease_publish_test.py` | `_amb05d_khong_nhan_ung_vien_stale` | `amb-m17-nhan-ung-vien-stale` | cả hai |
| B6 | `ops/lease_publish_test.py` | `_amb06_khong_chung_goc` | `amb-m06-rong-la-dat` | cả hai |
| B7 | `ops/lease_publish_test.py` | `_amb07_vuot_ngan_sach_merge_base` | `amb-m07-nuot-vuot-ngan-sach` | cả hai |
| B8a | `ops/lease_publish_test.py` | `_amb08a_replace_khong_doi_merge_base` | `amb-m08-git-merge-base-thay-bo-doc` | cả hai |
| B8b | `ops/lease_publish_test.py` | `_amb08b_bam_lech_chi_tren_nhanh_S` | `amb-m14-to-mau-khong-bam-lai` | cả hai |
| B9 | `ops/lease_publish_test.py` | `_amb09_vuot_ngan_sach_khi_dem_canh` | `amb-m09-nuot-ngan-sach-dem-canh`, `amb-m34-chen-nhan-vung-lech-vao-loi-b9`, `amb-m35-chen-nhan-khong-co-merge-base-vao-loi-b9` | cả hai |
| B10 | `ops/lease_publish_test.py` | `_amb10_chu_thich_workflow_adr0066` | `amb-m10-ghi-lai-cau-cu` | cả hai |
| t133 | `ops/lease_publish_test.py` | tên hiện có, ca con "S không tổ tiên H" đổi kỳ vọng (mục tiêu 5) | `amb-m02-bat-lai-to-tien` | cả hai |
| B11 | `.claude/dev/doc_receipt_thu_hoi_test.py` | ca bảng `v2_to_tien`, `v2_merge_base`, `v2_thieu_merge_bases`, `v2_thua_khoa`, `v2_to_tien_base_khac_S`, `v2_merge_base_canh_so`, `v2_to_tien_co_vung`, `v2_merge_base_vung_null`, `v2_vung_hai_phan_tu`, `v2_merge_bases_chua_sap`, `v2_merge_bases_trung`, `v2_merge_base_chua_S`, `v2_canh_bool`, `v2_canh_am`, `schema_3`; ca v1 hiện có giữ nguyên | `amb-m11-bo-tap-khoa-v2` cùng các đột biến vị từ con của mục tiêu 8 | cả hai |
| B12 | `.claude/dev/doc_receipt_thu_hoi_test.py` | ca `tinh` hiện có, đầu vào thêm fixture v2 | `amb-m12-them-subprocess`, `amb-m12b-open-trong-nhanh-v2` | cả hai |

Cột "nền" là ý định; nền thật của từng ca do bước đo nền ở mục 6 quyết. Ca đã ghi "cả hai" mà không chạy được trên
Windows native phải khai lý do trên #1266 trước lượt ứng viên (mục 6 bước 2), không lặng lẽ bỏ.

## 6. Windows (vòng 2 Q12)

Máy: `tra-luat-win`, Desktop Commander device `f7281f27-f79f-40a2-a2f5-b454b58a166a`, tài khoản `tlcommander`.
Không dùng device khác của cùng VM chạy dưới tài khoản quản trị để lấy quyền cao hơn. Clone thường, có thư mục `.git`
riêng; H chưa lên GitHub thì đưa sang bằng git bundle và kiểm commit, tree, cha khớp từng hash (`ADR-0060` M4).
Output, cache, thư mục tạm đặt ngoài checkout. Giữ `KHOA.txt` theo `ADR-0057`–`0059`; không đụng tiến trình hay khoá
của packet khác.

1. **Đo nền**, trước khi sửa mã: chạy trên base tập ứng viên gồm toàn bộ `.claude/dev/doc_receipt_thu_hoi_test.py`,
   cùng các ca t129, t133, t137, t151 của `ops/lease_publish_test.py`. Ghi ca nào chạy native được, kèm lệnh và output.
   Bộ đọc admission có nhánh tìm Git riêng cho Windows (`_git_windows`, `ops/lease_publish.py` dòng 1497 trên
   `9607e3eb`), và review lượt 2 chạy t129 native trên Windows của chủ kho (1/1); nên không giả định trước là ca nào
   không chạy được.
2. **Đóng băng tập bắt buộc** và đăng lên #1266 **trước** lượt ứng viên. Tập ấy gồm:
   - **luôn có**: toàn bộ `doc_receipt_thu_hoi_test.py` (gồm B11, B12), `_amb10_chu_thich_workflow_adr0066`, và B17
     với N ∈ {10, 50} trên clone thật của kho (N = 100 và 500 chạy và ghi số đo, không nghiệm thu: mục 0 cho thấy
     N = 100 vượt deadline trên Windows với bộ đọc mỗi object một tiến trình);
   - **có điều kiện**: t133 và các ca `_amb01`…`_amb09` (gồm `_amb01b`, `_amb01c`, `_amb02b`, `_amb03b`, `_amb05b`, `_amb05c`,
     `_amb05d`, `_amb08a`, `_amb08b`) — vào tập bắt buộc nếu t133 chạy native được ở bước 1; ca nào loại ra phải kèm lý
     do **đo được** ở bước 1 (lệnh, output), không kèm lý do suy từ tài liệu.

   Sau khi đã đăng, tập bắt buộc chỉ được **thêm** ca, không được bớt.
3. **Runner tập trung** là một script nằm ngoài kho (không thuộc write set); sha256 của script ghi vào JSON kết quả.
   Nó so mã nền với mã ứng viên bằng **cùng một tệp test của H**:
   - Dựng hai clone dùng một lần, trong **cùng một lệnh**, ngoài checkout nguồn: `nen` ở base SHA và `ung_vien` ở H.
     Checkout nguồn không bị đụng.
   - **Lớp phủ:** chép đúng hai tệp test tại H (`ops/lease_publish_test.py`, `.claude/dev/doc_receipt_thu_hoi_test.py`)
     vào cùng đường dẫn trong `nen`, ghi OID blob của từng tệp (`git rev-parse H:<path>`). Vì tệp test nạp mã sản phẩm
     từ chính thư mục của nó (`SCRIPT = HERE / "lease_publish.py"`, dòng 29–30; `MODUN = GOC / "doc_receipt_thu_hoi.py"`,
     dòng 22–23; đo 07-11-2026 trên `9607e3eb`), test của H chạy với mã sản phẩm của base. Review lượt 2 đã dựng thử cơ
     chế này trên hai clone tạm: mã sản phẩm ở `nen` vẫn là của base, HEAD không đổi, status đúng hai dòng ` M`.
   - Kiểm trạng thái **trước và sau** lượt chạy: `git rev-parse HEAD` của `nen` bằng base SHA, của `ung_vien` bằng H;
     `git status --porcelain` của `ung_vien` rỗng; của `nen` đúng hai dòng ` M` cho hai tệp phủ, không hơn không kém.
   - Tệp test của H không được import ở mức module một tên chỉ có trong mã mới (tên mới chỉ dùng trong thân ca), để
     module nạp được trên mã nền. Nạp hỏng ở `nen` là **không đo được** ⇒ runner đỏ.
   - Chạy **cùng một danh sách ID** ở cả hai clone: `main(chon=[...])` của `ops/lease_publish_test.py` với các hàm tìm
     theo hậu tố ở mục 5.1, và `chay_ca(m, path, chi=[...])` của `doc_receipt_thu_hoi_test.py`. Không gọi `main()`
     không đối số, vì nó chạy cả 285 ca cũ.
   - Kỳ vọng màu: ở `ung_vien` mọi ID bắt buộc đạt; ở `nen` các ca không đổi (t129, t151) đạt, các ca mới hoặc đã đổi
     kỳ vọng ghi màu thật kèm loại ngoại lệ (`AssertionError` của ca, hay lỗi khác). Ca mới đỏ trên nền vì lỗi không
     phải assertion của chính ca ấy thì ghi là "không đo được trên nền", không tính là "đỏ đúng màu".
   - Kiểm nền thật (`platform.system()`), phiên bản Python và Git; đỏ khi một ID không khớp đúng một hàm; coi
     `BỎ QUA`, skip, timeout, lỗi hạ tầng là **không đạt**.
   - Ghi JSON gồm base SHA, H, tree của cả hai, OID blob hai tệp phủ, sha256 của runner, nền, danh sách ID, kết quả và
     loại ngoại lệ từng ID ở từng clone, rc; kèm sha256 của tệp JSON.

   Cùng runner ấy chạy trên Linux trước full gate, để có kết quả tập trung nhanh.
4. Lượt nền và lượt ứng viên là hai nửa của **cùng một lệnh** runner ở bước 3, cùng máy, có danh sách ID ca và kết
   quả (M3 a). Ca bắt buộc bị `skipped`/`not_run` ⇒ không xanh. B17 trên Windows chạy trong cùng lượt, chỉ trên
   `ung_vien` (một clone của kho thật nên có lịch sử master và commit S ghim), dựng H như mục "Đầu vào của B17" và phải
   ra đúng OID ghim; commit H mà runner tạo chỉ nằm trong object store của clone dùng một lần, không làm đổi
   `git status`.
5. Tiến trình test không được thấy credential LIVE: `TL_TOKEN`, `TL_WEBAPP`, `TL_MASTER_KEY`,
   `TL_AGENT_CREDS_FILEID` và các biến Drive/GAS/NLM khác phải vắng. Runner kiểm sự vắng mặt bằng giá trị đúng/sai,
   không in giá trị.

## 7. hinh_dang_ke_thua

Chép từ đặc tả #1179 r1 §7 (nhánh `claude/spec-1179-c1a1b`, commit `7cfb4d7`), quyết định chủ kho ở #1179 lúc
07:58Z 06-11-2026, và bốn lượt review đặc tả của Mission này:

| lớp | số đếm | nguồn | chốt ở packet này |
|---|---|---|---|
| `phan-loai-vang-va-khong-do-duoc` | **6**: 4 từ #1179, cộng F11 (review lượt 2) và F16 (review lượt 4) — cả hai là điều kiện chọn canary coi "Git không thấy" là đủ trong khi bộ đọc báo không đo được | #1179 r1 lượt 1 F4; verdict lượt 2 và 4 của PR #1268 | bảng đóng ở mục 3; ca B1c, B5c, B6, B7, B9; câu cấm đổi lỗi đọc vùng thành bản đồ rỗng; B17 không còn loại "không đo được" nào: mọi kết quả khác "đạt" là đỏ |
| `mo-rong-module-pha-hop-dong-json-thuan` | 3 | #1179 review draft0–2 | mục tiêu 7 giữ thuần JSON; ca B12 (`ca_tinh` có fixture v2) |
| `nguon-duoc-tin-ma-chua-xac-minh` | 7 (chuỗi thu hồi) | spec C1a1a r5 §6 | merge-base chỉ tính bằng bộ đọc có băm; ca B8a, B8b |

Các hình dạng lỗi riêng của Mission này (đếm theo verdict lượt 11):

| hình dạng | các lần | chốt ở r13 |
|---|---|---|
| `canary-thieu-dieu-kien-chon` | F06, F11, F14, F16, F18, F20, F21, F23 (tám lần ⇒ checkpoint lần 2, 3, 4; lượt 5–8 xét lại theo luật mục 7; phép tấn công trước lời gọi thứ 9 tìm thêm kẽ hở ở vị từ r9) | cơ chế chung: **oracle của canary chưa tương đương hợp đồng toàn đường**, và một oracle so cả receipt trên lịch sử thật có bề mặt quá rộng để đóng hết bằng các bản vá cục bộ. Ở checkpoint lần 4 chủ kho chọn rút B17 về đo hiệu năng: B17 chỉ còn ba điều tối thiểu (mã thoát 0, đọc được receipt, hai trường), tính đúng thuộc các ca fixture B1–B12 và canary B18. B18 vẫn là chỗ hình dạng có thể tái phát vì chỉ đo được sau land |
| `canary-sau-land-thieu-nguoi-do` | **F22** (một lần) | mục 5 "Thi hành B18": người đo, mốc, cách gọi validator, nơi ghi và đọc lại, chuyển giao khi Mission đóng |
| `uoc-luong-doc-do-thi-bang-hieu-tap-commit` | **F19** (một lần) | mục 0 đo số commit bước tô màu thật sự đọc, bằng mô phỏng với `KhoObject` thật trên hai nền; `rev-list --count` chỉ còn là cột thống kê có nhãn rõ |
| `ngan-sach-tien-xu-ly-pha-tuong-thich` | F15, F17 | mục tiêu 4: miền của bất biến (mọi phép đọc và xác minh thành công, đủ ngân sách) và phép chiếu receipt viết tường minh; ca B1c cho phần ngoài miền |
| `receipt-moi-lam-doi-nhanh-cu` | F01, F09 | mục tiêu 3 tách phép đọc thêm khỏi ba phép đọc cũ |
| `nghiem-thu-do-nham-chot` | F03, F10, F24, F26, **F28** (năm lần ⇒ luật dừng) | mục 5 chỉ ghi màu nền đã đo; r11 lập ma trận nghĩa vụ đầu ra mới; r12 xét lại gốc chung của bốn lần — **dùng kết quả quan sát một chốt để chứng nhận chốt khác** — và đặt luật đột biến: mỗi khẳng định giá trị có đột biến chỉ đổi giá trị phát ra, giữ mã thoát và luồng, làm ca đỏ ở chính khẳng định ấy; đột biến chức năng tách cột riêng; r13 áp luật ấy cho cả **vế âm** (B9: hai đột biến chỉ chèn nhãn) |
| `cap-nhat-revision-khong-dong-bo` | F27 (một lần) | đồng bộ trần đề xuất (780) ở khối `nang_tran`, B16 và mục 9; A mục 5 đếm mỗi hình dạng ở đúng một chỗ |
| `mo-ta-thu-thap-lan-voi-dieu-kien-dat` | F25 (một lần) | mục 5 nói rõ B17 không dùng stdout để quyết định đạt, nhưng vẫn thu để ghi kèm |
| `dem-ca-bang-mau-ten` | F02, F13 | đơn vị "hàng nghiệm thu" đếm cả hàng có hậu tố chữ |
| `dem-sai-ngoai-le-closure` | F07, F12 | mẫu số tách 175 tệp được xét và 4 tệp nháp |

Luật dừng (từ r6, theo chỉ đạo chủ kho 07-11-2026 ghi ở đầu tệp): một biểu hiện mới của **bất kỳ** lớp kế thừa nào, hay
lần thứ ba của một hình dạng (`ADR-0037`), ở bất kỳ lượt review nào (đặc tả hay PR thi công) ⇒ **dừng vá theo chỗ bị
chỉ** và xét lại cách làm: phiên đang giữ việc ghi vào revision kế tiếp (hay vào handoff, với PR thi công) gốc rễ chung
của các lần, phương án chọn và phép đo chống đỡ phương án. Chỉ hỏi chủ kho khi một trong ba điều sau đúng: không còn
phương án nào có phép đo chống đỡ (hướng đi bế tắc); không đủ tài nguyên (trần lời gọi, ngân sách CI, máy, quota);
hoặc phương án sẽ đảo một quyết định của chủ kho (Q1–Q13 ở Mission #1264, các lựa chọn ở checkpoint 1–3). r5 trở về
trước đòi báo chủ kho ở mọi lần chạm luật; r6 thay luật ấy vì chỉ đạo mới, và chủ kho có quyền đặt lại khi duyệt băm.

## 8. Review và ngân sách đóng

**Review đặc tả, trước khi chủ kho duyệt băm:** Codex, tính trên PR đưa đặc tả vào kho, chung cho A và B; trần ban đầu
≤ 2 lời gọi, chủ kho nâng thành 3 rồi 4, rồi **10** ngày 07-11-2026 mà không hỏi lại từng lượt; đã dùng 11/11 (lượt 1–11 trên
r1–r8, r10, r11 và r12; lượt 0 không tính theo chủ kho). Lịch sử: mục 6 của đặc tả A r13. Trần 10 hết; chủ kho
nâng thành **11** ngày 08-11-2026 (*"Nâng trần +1"*); lời gọi thứ 11 đã dùng cho r12. r13 chưa được review bằng Codex. Mọi lượt chạy offline trên commit cục bộ; nhánh
đặc tả chỉ được đẩy lại khi review approve.

**Review mã:** reviewer Codex độc lập, phiên riêng; trần 10 lời gọi theo dòng khai `ADR-0055` ở đầu tệp, đếm
**trước** mỗi lời gọi. Không có ngân sách mềm: lượt thứ hai trở đi được gọi theo điều kiện của `ADR-0052` (còn P0/P1,
finding cắt ngang, hoặc cần xác minh lại bản vá), không cần hỏi chủ kho; Review Rescue Checkpoint khi hết trần mà chưa
approve (`ADR-0037`), hoặc theo luật dừng ở mục 7.
Reviewer **chạy** các ca và **đột biến bản vá** để đo răng; hướng thử cần soạn nội dung nhạy cảm thì mô tả bằng lời
cho phiên điều phối viết. Mọi lời gọi `codex exec` chạy với tính năng `memories` của Codex đã tắt. Human audit theo
`human_exact_head_audit.v1` (`ADR-0063`) trên exact head trước merge.

**Ngân sách đóng của PR mã** (đề xuất trong đặc tả; chủ kho chốt khi duyệt băm):

| hạng mục | trần | ghi chú |
|---|---|---|
| Lượt CI Ubuntu trên PR (head hoặc attempt) | 2 | rerun cũng tính; khớp `ADR-0060` M5 (một lần push chính) |
| Lượt `ci-dot-bien-du.yml` đầy đủ | 1 | lượt thứ 2 chỉ khi head đổi sau rework; vượt trần là việc tài nguyên, hỏi chủ kho |
| Lượt Windows native tập trung | 2 | mỗi lượt gồm nền, ứng viên và B17 trong một lệnh; tổng ≤ 60 phút |
| Phiên executor | 2 | phiên chạy quá 120 phút chủ động mà chưa có H thì ghi lý do vào handoff; chỉ hỏi chủ kho khi cần phiên thứ 3 |
| Lời gọi Codex review mã | 10 | không có ngân sách mềm, như trên |

Không trong packet này: gắn nhãn `windows` lên PR; gọi tay `ci.yml` (cả hai `runner_set` đều có Windows); Windows
CI; full mutant trên Windows; mua credits. Hết một trần, hoặc không biết mức đã dùng ⇒ dừng ở checkpoint chủ kho;
không vay ngân sách của packet khác.

## 9. chua_do_duoc

- Kết quả `ai-dang-giu` (mục 1) đúng tới lúc đo trong ngày 06-11-2026; nó cũ đi theo từng nhánh mới, nên người cấp
  lease phải đo lại cả năm đường dẫn.
- Ca nào của t133/t137/t151 chạy được trên Windows native: chưa đo (mục 6 bước 1); t129 đã chạy native ở review lượt 2.
- Runner tập trung (mục 6 bước 3): chưa dựng bản thật; cơ chế lớp phủ mới được review lượt 2 thử trên clone tạm.
- B17 với **mã sản phẩm**: chưa đo. Số đo hiện có: mô phỏng bước tô màu với `KhoObject` thật trên đầu vào ghim (mục 0,
  hai nền); ba phép đo kết quả đúng ở mục 5 (Linux, và review lượt 6 trên Windows ở N = 10 và 50); receipt v2 mô hình
  của review lượt 7 và 8 có `quan_he_S_H = merge_base` và `merge_bases = [B]` ở N = 10, 50.
- B17 trên Windows: review lượt 6 đo đường ghép với bộ đọc thật, N = 10 xong 7,3 giây và N = 50 xong 16,8 giây, dư
  43–52 giây trước deadline.
- Tốc độ của runner `ubuntu-latest` của GitHub: chưa đo; B18 ghi lại khi có PR đầu tiên.
- Màu nền của các ca mới ngoài những ca ghi ở mục 5: chưa đo.
- Các trần ở mục 8 là đề xuất; chưa có số đo mức dùng thực của một packet cỡ này để biện hộ từng con số.
- Canary B18: chỉ đo được sau land.
- Số dòng thực tế: mới là ước lượng (khối `nang_tran`); trần 780 là đề xuất, chưa được chủ kho chốt.
- r13 chưa được review bằng Codex; trần 11 đã hết (mục 8).

## 10. Thay đổi so với r12

Thay đổi r1→r2 … r11→r12 ghi ở mục 10 của từng revision ấy. Từ r12 sang r13 (verdict lượt 11 trên `efed1036`):

| nguồn | thay đổi |
|---|---|
| F28 `nghiem-thu-do-nham-chot`, lần thứ năm (P2): hai vế âm của B9 (không nhãn `VUNG_LECH`, không nhãn `KHONG_CO_MERGE_BASE`) chưa có đột biến chỉ đổi giá trị; `amb-m31` chỉ đổi nhãn ở B6, `amb-m09` đổi luồng | hai đột biến mới `amb-m34-chen-nhan-vung-lech-vao-loi-b9`, `amb-m35-chen-nhan-khong-co-merge-base-vao-loi-b9`, mỗi cái chỉ chèn một nhãn vào thông báo lỗi ngân sách của B9, giữ rc 12, luồng, phần còn lại và việc không có receipt; ma trận ghi B9 là ca đích âm ở hai hàng nhãn; `amb-m31` chỉ đích B6; `amb-m09` ở cột chức năng; mục 5.1 đăng ký hai đột biến cho B9 |
