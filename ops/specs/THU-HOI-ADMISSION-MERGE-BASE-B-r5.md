# Đặc tả packet — `THU-HOI-ADMISSION-MERGE-BASE-B` (revision 5)

- `packet_id`: **THU-HOI-ADMISSION-MERGE-BASE-B** · `revision`: **5** · trạng thái: nháp, chờ chủ kho duyệt băm.
  Thay `ops/specs/THU-HOI-ADMISSION-MERGE-BASE-B-r4.md` (sha256
  `cc5cfc5c038a7544ce9d9f330a8a395a205f1c488d43eab2e9cb12f303c7e4ff`), r3 (sha256
  `f366fda5c61705ec9915d026c43db40f9aeda404965d7d7f6957fbd3977cdbdd`), r2 (sha256
  `3f002496d380119c9093c072dda3c690afbfa140c21d6ddfdd792590c17dac69`) và r1 (sha256
  `a4e4a7aad7a885acccfd48c513644467a0b048833d50a0cb101992e400cf9ddf`); cả bốn chưa từng được duyệt và giữ nguyên trong
  kho để verdict của từng lượt review vẫn tra được theo băm. Thay đổi so với r4: mục 10.
- Review Rescue Checkpoint (`ADR-0037`), ba lần trong ngày 07-11-2026: lần 1 sau review lượt 2 (F11) — chủ kho chọn
  sửa thành r3, giữ merge-base; lần 2 sau review lượt 3 (F14, lần thứ ba của hình dạng `canary-thieu-dieu-kien-chon`) —
  chủ kho chọn r4, đổi gốc của canary; lần 3 sau review lượt 4 (F16, lần thứ tư của hình dạng canary và biểu hiện thứ
  sáu của lớp kế thừa `phan-loai-vang-va-khong-do-duoc`) — chủ kho chọn **r5 theo phương án đã ghi sẵn ở r4**: B17/B18
  **không còn đoán trước** kết quả của bộ kiểm; B17 dùng đầu vào tự dựng trên lịch sử thật, và cả hai xếp kết quả theo
  nguyên nhân, có xác nhận độc lập bằng Git (mục 5).
- `packet_issue`: **#1266** (sub-issue của Mission #1264). Issue không tự cấp việc (protocol §3.2, §4).
- **Phụ thuộc:** packet `THU-HOI-ADMISSION-MERGE-BASE-A` #1265 (ADR-0066 và dòng §20, đặc tả
  `ops/specs/THU-HOI-ADMISSION-MERGE-BASE-A-r5.md`) đã land. Base của B phải chứa commit land của A; đo bằng
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
  ai_nang: chủ kho ducthangho — vòng 1 Q7 của phiên soạn spec 06-11-2026 ("Theo khuyến nghị") cho trần 600; r2–r5 đề xuất 700, chủ kho chốt trong comment duyệt băm trên Issue
  can_cu: >-
    Ước lượng r5 550–700 dòng thêm, chưa đo: mã bộ kiểm ~120–160 (tô màu hai phía có luật ứng viên chưa stale, đọc giờ
    commit, lọc cực đại, hàm vùng, tích hợp, receipt); test bộ kiểm ~340–420 (19 hàng nghiệm thu nhóm B1–B12 ở mục 5,
    trong đó 17 hàng thuộc tệp này; r1 có 13 hàng, r2 có 15, r3 có 16, r4 có 18); validator C1a1a và test ~90–120.
    Runner của B17 nằm ngoài kho, không tính. So sánh gần nhất PR #620 (+204 dòng, 2 tệp; review lượt 1 đo lại:
    workflow +42, test +162). Receipt v2 và validator chấp nhận v2 land cùng nhau trong packet này; nếu phải tách thì
    validator (consumer) land trước bộ kiểm (producer) là thứ tự an toàn, vì không có khoảng nào v2 được phát ra mà
    chưa ai hiểu — việc tách ấy cần packet mới và quyết định chủ kho.
  tran_cu: "≤ 6 tệp / ≤ 450 dòng thêm (ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab)"
  tran_moi: "≤ 6 tệp / ≤ 700 dòng thêm, đo bằng git diff --numstat origin/master...HEAD; vượt thì dừng ở checkpoint chủ kho, không tự bỏ ca của mục 5"
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
- Số commit phía S mà bước tô màu phải đọc khi H tụt sau master N commit first-parent (đo 09:43Z 07-11-2026, S =
  `132d376c`, `git rev-list --count S~N..S`): N = 10 ⇒ 70; N = 50 ⇒ 292; N = 100 ⇒ 581; N = 200 ⇒ 1.119; N = 500 ⇒ 3.818.
  Với khoảng 39 ms một object trên Windows, N ≥ 200 sát hoặc vượt deadline 60 giây — đó là lý do mức nghiệm thu của B17
  ở mục 5 khác nhau theo N và theo nền.

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
r2–r5 không quét lại. Người cấp lease đo lại cả năm đường dẫn ngay trước khi cấp (L5).

## 2. ngoai_pham_vi

- Luật theo ID lease (R3/R4) và việc kiểm lại lúc land (R5): thuộc A1b (#656) và bên kiểm lúc land (#499 C1,
  #1179), vòng 1 Q5. Packet này chỉ ghi vào receipt dữ kiện để R5 dùng.
- `SO_THU_HOI_KICH_HOAT` giữ `False`; luật "chế độ chưa kích hoạt đòi tập revocation rỗng ở S và T" giữ nguyên.
- Chuyển tiếp Q13 (marker mới đòi `base_sha_before_add == S`) giữ nguyên. PR thêm tệp policy và marker vẫn cần S
  đúng bằng base của sự kiện; đó là việc của A1, rất hiếm, không phải nguồn sync hằng ngày.
- Các lệnh khác của `ops/lease_publish.py` (`check`, `body`, `kiem-github`, `ai-dang-giu`) và các bước của workflow.
- Đổi `KhoObject.doc` sang một tiến trình `cat-file --batch` dùng chung: không làm ở packet này; hiệu năng đạt bằng
  cách đọc ít object hơn (mục tiêu 1), đo ở B17.
- Hiệu năng trên đồ thị criss-cross dài, và trên PR tụt sau master từ khoảng 200 commit first-parent trở lên khi chạy
  trên Windows: không bảo đảm. Bước lọc cực đại chỉ chạy khi có ≥ 2 ứng viên và chịu chung ngân sách; chạm trần ⇒ 12,
  PR hoà base là hết. Tính đúng của criss-cross do B5 đo; B17 dựng H một cha nên chỉ có một merge-base; B18 chỉ xét PR
  có đúng một merge-base.
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
| so vùng (chỉ chế độ `merge_base`) | mọi merge-base có vùng bằng vùng tại S ⇒ đi tiếp các phép kiểm cũ trên T | một merge-base lệch ⇒ rc 12, nhãn `VUNG_LECH`, SHA của merge-base, đường dẫn lệch đầu tiên | `tim`/`namespace` gặp tổ tiên không phải thư mục, đọc object lỗi, tree có entry không hợp lệ (tên không phải UTF-8, trùng, mode lạ) |

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
   `quan_he=<giá trị>`.
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
| B1 | S là tổ tiên H | rc 0; receipt v2, `quan_he_S_H = to_tien`, `merge_bases = [S]`, `canh_ancestry` số nguyên, `vung_tai_S = null` | `amb-m01` luôn đi chế độ `merge_base` ⇒ `quan_he_S_H` khác ⇒ ca đỏ |
| B1b | S có `.github/coordination` là **tệp thường**; H là con của S và xoá tệp ấy; S là tổ tiên H | rc 0, `to_tien`, `vung_tai_S = null` (nền cũng rc 0 — trong miền của bất biến tương thích) | `amb-m13` gọi hàm vùng cả ở chế độ `to_tien` ⇒ `tim` gặp tổ tiên không phải thư mục ⇒ rc 12 ⇒ ca đỏ |
| B1c | S là tổ tiên H qua đồ thị `B → R_bad → S → H`, mọi tree rỗng; `R_bad` là commit có giây trong dòng `committer` không phải số nguyên, lưu bằng `git hash-object -t commit --literally -w` (ngoài miền của bất biến tương thích) | rc 12, thông báo nêu dòng `committer` hỏng và OID của `R_bad` (nền rc 0 — chặt hơn nền có chủ đích, mục tiêu 4) | `amb-m18` chỉ kiểm giờ commit khi lấy commit ra khỏi hàng đợi, không kiểm khi đọc để xếp hàng ⇒ `R_bad` chỉ được xếp hàng rồi bước tô màu dừng ⇒ rc 0 ⇒ ca đỏ |
| B2 | H rẽ từ B, master đi tiếp và đổi tệp ngoài vùng | rc 0; `merge_base`, `merge_bases = [B]`, `canh_ancestry = null`, `vung_tai_S` là dict | `amb-m02` bắt lại `to_tien` ⇒ rc 12 ⇒ ca đỏ |
| B3 | Master thêm `.github/coordination/change-impact.v1.json` sau B | rc 12, nhãn `VUNG_LECH`, không receipt | `amb-m03` bỏ cổng so vùng ⇒ rc khác 12 hoặc thiếu nhãn ⇒ ca đỏ |
| B3b | Master thêm một bản ghi thu hồi vào `ops/thu-hoi/` sau B; H không có nó | rc 12, nhãn `VUNG_LECH`, không receipt | `amb-m03` bỏ cổng so vùng ⇒ append-only S→T chạy trước và trả **8** (bản ghi ở S vắng ở T) ⇒ ca đỏ |
| B4 | B và S có cùng một bản ghi; H **xoá** bản ghi ấy; S không là tổ tiên H | rc 8, thông báo có `append-only` | `amb-m04` bỏ phép append-only ⇒ tới chốt chưa kích hoạt, rc 12 ⇒ ca đỏ |
| B5 | Criss-cross: hai merge-base, merge-base đứng đầu theo thứ tự sắp có vùng bằng S, cái còn lại lệch (review lượt 1 đã dựng được topology này) | rc 12, nhãn `VUNG_LECH`, thông báo nêu SHA của merge-base lệch | `amb-m05` chỉ so merge-base đầu ⇒ rc 0 ⇒ ca đỏ |
| B5b | Giờ commit lệch: đồ thị `H→Y→C`, `S→C`, `C→R`, committer time H = 10, Y = 1, S = 5, C = 4, R = 3 (Y cũ hơn chính tổ tiên của nó); không có tệp vùng nào | rc 0, `merge_base`, `merge_bases = [C]`, bằng tập mà `GIT_NO_REPLACE_OBJECTS=1 git merge-base --all S H` trả trên cùng fixture | `amb-m15` không đưa lại vào hàng đợi commit đã xử lý khi nó nhận thêm cờ ⇒ C không bao giờ thành ứng viên ⇒ tập khác `[C]` ⇒ ca đỏ |
| B5c | Cha thứ nhất của S (phía S, không là tổ tiên của H) là commit có dòng `committer` mà phần giây không phải số nguyên, lưu bằng `git hash-object -t commit --literally -w`; không có tệp vùng nào | rc 12, thông báo nêu dòng `committer` hỏng và OID ấy | `amb-m16` lấy giờ mặc định 0 khi không đọc được ⇒ bước tô màu chạy tiếp, vùng vắng ở mọi nơi ⇒ rc 0 ⇒ ca đỏ |
| B5d | Gọi thẳng hàm tô màu: `R0…R9` tuyến tính (committer time 100…109), B là con của R9 (110), S là con của B (120), X là một gốc riêng (1), H (130) có hai cha B và X | danh sách ứng viên trước khi lọc đúng bằng `[B]`; tập merge-base `[B]` | `amb-m17` ghi cả commit đã `STALE` có đủ hai cờ làm ứng viên ⇒ danh sách trước lọc thành `[B, R9, R8, …, R0]` ⇒ ca đỏ (tập sau lọc vẫn `[B]`, nên ca phải đo danh sách trước lọc) |
| B6 | S và H không chung gốc | rc 12, nhãn `KHONG_CO_MERGE_BASE` | `amb-m06` coi "0 merge-base" là đạt ⇒ rc 0 ⇒ ca đỏ |
| B7 | `max_commits_merge_base` nhỏ hơn số commit bước tô màu phải đọc | rc 12, thông báo nêu `max_commits_merge_base` | `amb-m07` nuốt lỗi vượt ngân sách ⇒ rc 0 ⇒ ca đỏ |
| B8a | Kho nguồn có một `refs/replace` làm `git merge-base --all` (vốn theo replace) trả một commit có vùng bằng S, trong khi merge-base thật trên đồ thị đã băm có vùng lệch | rc 12, nhãn `VUNG_LECH`, thông báo nêu SHA của merge-base **thật** | `amb-m08` tính merge-base bằng `git merge-base --all` trên kho nguồn ⇒ rc 0 ⇒ ca đỏ |
| B8b | Cha thứ nhất của S (thuộc phía S, mới hơn merge-base, không là tổ tiên của H) bị seam `sau_cat_file` đổi bytes, nên băm không khớp tên | rc 12, thông báo băm lệch của bộ đọc nêu OID ấy | `amb-m14` bước tô màu đọc cha bằng đường không băm lại ⇒ không có thông báo băm lệch ⇒ ca đỏ |
| B9 | S là tổ tiên H; `max_parent_path_edges` nhỏ hơn số cạnh của đường witness | rc 12, thông báo `đường parent > … cạnh`, **không** có `KHONG_CO_MERGE_BASE` hay `VUNG_LECH`, không receipt | `amb-m09` nuốt lỗi ngân sách của bước đếm cạnh rồi đi tiếp chế độ `merge_base` ⇒ rc 0 ⇒ ca đỏ |
| B10 | Chú thích workflow, đo trên văn bản đã nối dòng từng đoạn (bỏ `#` và khoảng trắng đầu mỗi dòng chú thích, dòng `#` trống ngắt đoạn, gộp khoảng trắng): vế dương có nguyên câu mới ở mục tiêu 6; vế âm không còn cụm *"Bộ kiểm còn đòi S là tổ tiên của H"* | cả hai vế đạt | `amb-m10` ghi lại câu cũ ⇒ vế âm đỏ; bỏ *"không còn"* khỏi câu mới ⇒ vế dương đỏ; đổi *"mọi merge-base"* thành *"một merge-base"* ⇒ vế dương đỏ; cắt hậu tố *", rồi mọi phép kiểm chạy trên T = tree(H)."* ⇒ vế dương đỏ; ngắt dòng lại giữ nguyên chữ ⇒ vẫn đạt |
| B11 | `doc_receipt_thu_hoi`: v1 hiện có ⇒ `ok`; v2 `to_tien` ⇒ `ok`; v2 `merge_base` ⇒ `ok`; mỗi ca sau ⇒ `do`: v2 thiếu `merge_bases`, thừa một khoá, `to_tien` với `merge_bases ≠ [S]`, `merge_base` với `canh_ancestry` số, `to_tien` với `vung_tai_S` là dict, `merge_base` với `vung_tai_S = null`, `vung_tai_S` có giá trị 2 phần tử, `merge_bases` chưa sắp tăng, `merge_bases` có phần tử trùng, `merge_base` với S nằm trong `merge_bases`, `canh_ancestry = true`, `canh_ancestry = -1`, `schema_version = 3` | như cột trái | `amb-m11` bỏ kiểm tập khoá v2 ⇒ ca thiếu/thừa khoá thành `ok` ⇒ ca đỏ; mỗi đột biến vị từ con của mục tiêu 8 làm đúng ca tương ứng thành `ok`; đột biến từng trường của `_theo_truong` cho ba khoá mới |
| B12 | `ca_tinh` chạy trên fixture v1 **và** hai fixture v2: tập import ⊆ {`argparse`, `json`, `re`, `sys`}, audit hook không ghi sự kiện nào, kết quả tất định | ca đạt | `amb-m12` thêm `import subprocess` ⇒ tập import lệch ⇒ ca đỏ; `amb-m12b` thêm một lời gọi `open(...)` chỉ trong nhánh xử lý v2 ⇒ audit hook ghi sự kiện ⇒ ca đỏ (đột biến này chỉ bị bắt khi fixture v2 có trong `ca_tinh`) |
| B13 | Toàn bộ `ops/lease_publish_test.py` và `.claude/dev/doc_receipt_thu_hoi_test.py` trên CI Linux của exact head báo `N/N` với hai số bằng nhau | lệch | — (bằng chứng dương, không tin `rc=0` một mình) |
| B14 | Windows, mục 6 | xanh theo `ADR-0060` M3 (a)–(c) | — |
| B15 | `ci-dot-bien-du.yml` thành công trên exact head, mọi job `success` (K7) | thiếu hoặc đỏ | — |
| B16 | Kích thước theo `nang_tran`: ≤ 6 tệp, ≤ 700 dòng thêm; không tệp ngoài `write_set` | vượt hoặc tệp lạ | thêm một tệp ⇒ đỏ |
| B17 | Hiệu năng trên **lịch sử thật**, trước merge, với đầu vào **tự dựng** theo mục "Đầu vào của B17" dưới đây; kết quả xếp theo "Bảng xếp nguyên nhân" | loại **đạt** cho mọi N bắt buộc: N ∈ {10, 50, 100} trên Linux và trên `tra-luat-win`; N = 500 trên Linux ghi lại, không nghiệm thu | một N bắt buộc ra loại **đỏ — hiệu năng** hoặc **đỏ — sai** ⇒ đỏ |
| B18 | Canary sau land: PR thật đầu tiên mà sự kiện `pull_request_target` của nó có S = `base.sha` không là tổ tiên của H và `GIT_NO_REPLACE_OBJECTS=1 git merge-base --all S H` ra đúng một commit; kết quả xếp theo "Bảng xếp nguyên nhân" | loại **đạt**: check `thu-hoi` success, receipt đọc lại có `quan_he_S_H = merge_base` | **chưa đo được** tới khi có PR ấy; loại **đỏ — hiệu năng** hoặc **đỏ — sai** ⇒ đỏ; loại **đầu vào không dùng được** ⇒ ghi lại, chờ PR kế tiếp. Người land ghi run ID, S, H, merge-base, loại và bằng chứng xác nhận |

**Đầu vào của B17.** B17 không chọn PR thật và không đoán trước kết quả của bộ kiểm: runner tự dựng H trên lịch sử
thật, rồi xếp kết quả theo nguyên nhân.

- Kho đo: một clone thường, không shallow, không `info/grafts`, không `refs/replace`; mọi lệnh Git của runner chạy với
  `GIT_NO_REPLACE_OBJECTS=1`. Ghi SHA của S và tree của từng H.
- S = tip `origin/master` lúc đo. Với mỗi N: B = `S~N` (đi theo first-parent); H = một commit runner tạo bằng
  `git commit-tree`, **cha duy nhất là B**, tree = tree(B) cộng đúng một tệp mới ở gốc cây tên `amb-b17-<N>.txt` (ASCII),
  nội dung ASCII một dòng, mode `100644`. Tệp ấy nằm ngoài vùng của bộ kiểm.
- Vì H có một cha là B và B là tổ tiên của S, (S, H) có đúng một merge-base là B, và S không là tổ tiên của H. Đây là
  tính chất của cách dựng; runner vẫn đo lại bằng `git merge-base --all S H` (phải ra đúng B) và
  `git merge-base --is-ancestor S H` (phải rc 1) trước khi chạy bộ kiểm. Đo lại sai ⇒ lượt ấy **không đo được**.
- Chạy bộ kiểm mới `kiem-thu-hoi-github H --canonical-base S` trên kho đo; ghi rc, toàn bộ stderr, dòng
  `THU_HOI_ADMISSION`, receipt, thời gian, `so_object_da_doc`, `tong_bytes`, số commit bước tô màu đã đọc.
- Đã thử cách dựng (phiên soạn spec, 07-11-2026, trên một clone tạm, S = `9607e3eb`, N = 10): `git hash-object -w`
  cho blob, `git mktree` từ `git ls-tree` của tree(B) cộng một dòng, `git commit-tree -p B`; kết quả
  `git merge-base --all S H` = B (`825eb356`), `git merge-base --is-ancestor S H` rc 1, `git diff --name-status B H` chỉ
  có `A amb-b17-10.txt`, phía S có 69 commit.

**Bảng xếp nguyên nhân** (đóng; dùng cho B17 và B18). Mỗi kết quả rơi vào đúng một loại:

| loại | điều kiện | hệ quả |
|---|---|---|
| **đạt** | rc 0, `quan_he_S_H = merge_base`, `merge_bases` đúng bằng merge-base đã đo bằng Git, không chạm trần nào | ghi số đo |
| **đỏ — hiệu năng** | rc 12 và thông báo nêu vượt một khoá trong `NGAN_SACH_MAC_DINH` hoặc hết deadline reader | nghiệm thu đỏ |
| **đầu vào không dùng được** | rc ≠ 0, thông báo nêu một khiếm khuyết của **dữ liệu** thuộc một dòng của bảng xác nhận dưới đây, **và** lệnh Git độc lập của dòng ấy xác nhận đúng khiếm khuyết đó trên đúng object hoặc đường dẫn mà thông báo nêu | ghi lại cả thông báo lẫn output xác nhận; với B17 thử N + 1, ba lần liền không dùng được ⇒ N ấy `chưa đo được`; với B18 chờ PR kế tiếp |
| **đỏ — sai** | mọi kết quả khác — kể cả thông báo nêu khiếm khuyết dữ liệu mà lệnh Git độc lập **không** xác nhận, và mọi nhãn hay mã thoát không có dòng xác nhận | nghiệm thu đỏ |

Bảng xác nhận độc lập (đóng; lệnh chạy trên cùng kho đo, `GIT_NO_REPLACE_OBJECTS=1`):

| khiếm khuyết bộ kiểm nêu | lệnh xác nhận | xác nhận khi |
|---|---|---|
| tree `<oid>` có entry không hợp lệ (tên không phải UTF-8, tên rỗng/`.`/`..`/có `/`/`.git`, tên trùng, mode lạ, entry cụt) | `git ls-tree -z <oid>`, rồi kiểm từng entry bằng một hàm viết riêng trong runner theo đúng các luật ấy | ít nhất một entry vi phạm đúng luật được nêu |
| commit `<oid>` có header hỏng hoặc dòng `committer` hỏng | `git cat-file -p <oid>` | header trước dòng trống đầu tiên thiếu `tree`, có `parent` sai dạng, hoặc không có đúng một dòng `committer` cấp đầu có giây là số nguyên |
| object `<oid>` thiếu hoặc băm lệch | `git cat-file -e <oid>`; `git fsck --no-dangling` | `cat-file -e` rc ≠ 0, hoặc `fsck` nêu đúng OID ấy |
| `VUNG_LECH` tại merge-base `<B>`, đường dẫn `<p>` | `git ls-tree <B> -- ops/thu-hoi/` cộng `git ls-tree <B> -- .github/coordination/change-impact.v1.json`, so với cùng hai lệnh tại S | hai output khác nhau ở đúng `<p>` |
| chế độ chưa kích hoạt đòi tập revocation rỗng | `git ls-tree <S> -- ops/thu-hoi/` và `git ls-tree <H> -- ops/thu-hoi/` | có entry revocation ở S hoặc ở H |
| policy hoặc marker Q13 (policy hỏng, thiếu marker, marker mới) | `git ls-tree <H> -- .github/coordination/change-impact.v1.json ops/thu-hoi/` | có policy hoặc marker tại H |

Không có dòng xác nhận cho `KHONG_CO_MERGE_BASE` và `append-only`: với đầu vào của B17 cả hai không thể đúng (B là tổ
tiên chung; vùng của H bằng vùng của B), nên chúng rơi vào **đỏ — sai**; với B18, `KHONG_CO_MERGE_BASE` cũng là đỏ vì
PR đã được chọn có đúng một merge-base, còn `append-only` thì xác nhận bằng `git ls-tree` thấy entry có ở S mà vắng hoặc
khác ở H — nếu có, PR là **đầu vào không dùng được** (đó là chính luật mà bộ kiểm phải giữ).

**Năm vế L6 cho các tiêu chí khớp chuỗi:**

| tiêu chí | (a) dương / âm | (b) trọn mệnh đề, nối đoạn | (c) từng vị trí | (d) chữ / số | (e) đủ vị trí cổng |
|---|---|---|---|---|---|
| B10 | có cả hai vế | vế dương trọn câu mới, nối đoạn; vế âm dùng cụm lõi ngắn hơn câu cũ, chặt hơn chép nguyên câu | một khối chú thích | không có ngưỡng số | không phải lời khai về cổng |
| B12 | không còn là phép khớp chuỗi: dùng `ca_tinh` đo hành vi (import, audit hook) | không áp | không áp | không áp | không áp |
| nhãn `VUNG_LECH`, `KHONG_CO_MERGE_BASE` | dương trên thông báo mới; âm ở B9 (không được có hai nhãn) | nhãn là một token, không ngắt dòng | mỗi ca một nhãn | không có số | không áp |
| bảng xếp nguyên nhân | mỗi loại có điều kiện riêng; "đỏ — sai" là phần bù, nên không loại nào bị bỏ trống | khớp thông báo theo mẫu của từng dòng, không theo từ khoá lẻ | từng dòng xác nhận một khiếm khuyết | N là danh sách số cụ thể | không áp |

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
- B17 trên nền: nền không có chế độ `merge_base`, nên với đầu vào của B17 nền trả 12 *"không phải tổ tiên"* — rơi vào
  **đỏ — sai** đúng như phải thế; không dùng nền làm thước cho B17.
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
thì đếm hàng của bảng mục 5, kể cả hàng có hậu tố chữ (B1b, B1c, B3b, B5b, B5c, B5d, B8a, B8b). Executor chọn số kế
tiếp còn trống trên base của lease, giữ nguyên hậu tố. Mỗi hậu tố phải khớp **đúng một** hàm; không khớp hoặc khớp hai
⇒ runner đỏ. Mỗi đột biến có ID riêng, đăng ký vào bảng đột biến sẵn có của tệp test tương ứng.

| ca | tệp | hậu tố / tên ca | ID đột biến | nền |
|---|---|---|---|---|
| B1 | `ops/lease_publish_test.py` | `_amb01_to_tien_giu_nguyen` | `amb-m01-luon-di-merge-base` | cả hai |
| B1b | `ops/lease_publish_test.py` | `_amb01b_to_tien_khong_doc_vung_S` | `amb-m13-luon-goi-ham-vung` | cả hai |
| B1c | `ops/lease_publish_test.py` | `_amb01c_to_tien_committer_hong_o_commit_doc_them` | `amb-m18-khong-kiem-committer-khi-xep-hang` | cả hai |
| B2 | `ops/lease_publish_test.py` | `_amb02_merge_base_vung_bang_nhau` | `amb-m02-bat-lai-to-tien` | cả hai |
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
| B9 | `ops/lease_publish_test.py` | `_amb09_vuot_ngan_sach_khi_dem_canh` | `amb-m09-nuot-ngan-sach-dem-canh` | cả hai |
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
     với N ∈ {10, 50, 100} trên clone thật của kho;
   - **có điều kiện**: t133 và các ca `_amb01`…`_amb09` (gồm `_amb01b`, `_amb01c`, `_amb03b`, `_amb05b`, `_amb05c`,
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
   `ung_vien` (một clone của kho thật nên có lịch sử master), dựng H như mục "Đầu vào của B17", với S là cùng SHA như
   lượt B17 trên Linux nếu hai lượt cách nhau dưới 24 giờ; commit H mà runner tạo chỉ nằm trong object store của clone
   dùng một lần, không làm đổi `git status`.
5. Tiến trình test không được thấy credential LIVE: `TL_TOKEN`, `TL_WEBAPP`, `TL_MASTER_KEY`,
   `TL_AGENT_CREDS_FILEID` và các biến Drive/GAS/NLM khác phải vắng. Runner kiểm sự vắng mặt bằng giá trị đúng/sai,
   không in giá trị.

## 7. hinh_dang_ke_thua

Chép từ đặc tả #1179 r1 §7 (nhánh `claude/spec-1179-c1a1b`, commit `7cfb4d7`), quyết định chủ kho ở #1179 lúc
07:58Z 06-11-2026, và bốn lượt review đặc tả của Mission này:

| lớp | số đếm | nguồn | chốt ở packet này |
|---|---|---|---|
| `phan-loai-vang-va-khong-do-duoc` | **6**: 4 từ #1179, cộng F11 (review lượt 2) và F16 (review lượt 4) — cả hai là điều kiện chọn canary coi "Git không thấy" là đủ trong khi bộ đọc báo không đo được | #1179 r1 lượt 1 F4; verdict lượt 2 và 4 của PR #1268 | bảng đóng ở mục 3; ca B1c, B5c, B6, B7, B9; câu cấm đổi lỗi đọc vùng thành bản đồ rỗng; B17/B18 xếp "không đo được" của bộ đọc vào loại riêng, chỉ khi Git xác nhận độc lập |
| `mo-rong-module-pha-hop-dong-json-thuan` | 3 | #1179 review draft0–2 | mục tiêu 7 giữ thuần JSON; ca B12 (`ca_tinh` có fixture v2) |
| `nguon-duoc-tin-ma-chua-xac-minh` | 7 (chuỗi thu hồi) | spec C1a1a r5 §6 | merge-base chỉ tính bằng bộ đọc có băm; ca B8a, B8b |

Các hình dạng lỗi riêng của Mission này (đếm theo verdict lượt 4):

| hình dạng | các lần | chốt ở r5 |
|---|---|---|
| `canary-thieu-dieu-kien-chon` | F06, F11, F14, **F16** (bốn lần ⇒ checkpoint lần 2 và 3) | gốc rễ là đoán trước rc 0 của bộ kiểm từ điều kiện Git; r5 bỏ hẳn việc đoán: B17 dùng đầu vào tự dựng, B17/B18 xếp kết quả theo nguyên nhân với bảng xác nhận độc lập đóng |
| `ngan-sach-tien-xu-ly-pha-tuong-thich` | F15, F17 | mục tiêu 4: miền của bất biến (mọi phép đọc và xác minh thành công, đủ ngân sách) và phép chiếu receipt viết tường minh; ca B1c cho phần ngoài miền |
| `receipt-moi-lam-doi-nhanh-cu` | F01, F09 | mục tiêu 3 tách phép đọc thêm khỏi ba phép đọc cũ |
| `nghiem-thu-do-nham-chot` | F03, F10 | mục 5 chỉ ghi màu nền đã đo |
| `dem-ca-bang-mau-ten` | F02, F13 | đơn vị "hàng nghiệm thu" đếm cả hàng có hậu tố chữ |
| `dem-sai-ngoai-le-closure` | F07, F12 | mẫu số tách 175 tệp được xét và 4 tệp nháp |

Một biểu hiện mới của **bất kỳ** lớp kế thừa nào ở bất kỳ lượt review nào (đặc tả hay PR thi công) ⇒ DỪNG, Review
Rescue Checkpoint (`ADR-0037`), báo chủ kho; không vá tiếp theo chỗ bị chỉ. Một hình dạng đang ở hai lần mà xuất hiện
**lần thứ ba**, hoặc `canary-thieu-dieu-kien-chon` xuất hiện **lần thứ năm**, ⇒ cũng DỪNG và chủ kho xét lại cách làm.
Ở r5 không còn điều kiện chọn ca nào đoán trước kết quả, nên một lần thứ năm của canary nghĩa là bảng xếp nguyên nhân
hay bảng xác nhận có lỗ — lúc ấy phương án còn lại là bỏ B17/B18 khỏi nghiệm thu và chỉ giữ số đo hiệu năng làm thông
tin, do chủ kho quyết.

## 8. Review và ngân sách đóng

**Review đặc tả, trước khi chủ kho duyệt băm:** Codex, tính trên PR đưa đặc tả vào kho, chung cho A và B; trần ban đầu
≤ 2 lời gọi, chủ kho nâng thành 3 rồi 4; **đã dùng hết** (lượt 1–4 trên r1–r4; lượt 0 không tính theo chủ kho). Lịch
sử: mục 6 của đặc tả A r5. Review r5 cần chủ kho nâng trần trước lời gọi; chưa có lời gọi nào cho r5.

**Review mã:** reviewer Codex độc lập, phiên riêng; trần 10 lời gọi theo dòng khai `ADR-0055` ở đầu tệp, đếm
**trước** mỗi lời gọi. Ngân sách mềm 4 lời gọi; hai lượt liên tiếp chưa approve ⇒ Review Rescue Checkpoint.
Reviewer **chạy** các ca và **đột biến bản vá** để đo răng; hướng thử cần soạn nội dung nhạy cảm thì mô tả bằng lời
cho phiên điều phối viết. Mọi lời gọi `codex exec` chạy với tính năng `memories` của Codex đã tắt. Human audit theo
`human_exact_head_audit.v1` (`ADR-0063`) trên exact head trước merge.

**Ngân sách đóng của PR mã** (đề xuất trong đặc tả; chủ kho chốt khi duyệt băm):

| hạng mục | trần | ghi chú |
|---|---|---|
| Lượt CI Ubuntu trên PR (head hoặc attempt) | 2 | rerun cũng tính; khớp `ADR-0060` M5 (một lần push chính) |
| Lượt `ci-dot-bien-du.yml` đầy đủ | 1 | lượt thứ 2 chỉ khi head đổi sau rework, cần checkpoint chủ kho |
| Lượt Windows native tập trung | 2 | mỗi lượt gồm nền, ứng viên và B17 trong một lệnh; tổng ≤ 60 phút |
| Phiên executor | 2 | checkpoint chủ kho nếu một phiên chạy quá 120 phút chủ động mà chưa có H |
| Lời gọi Codex review mã | 10 | mềm 4, như trên |

Không trong packet này: gắn nhãn `windows` lên PR; gọi tay `ci.yml` (cả hai `runner_set` đều có Windows); Windows
CI; full mutant trên Windows; mua credits. Hết một trần, hoặc không biết mức đã dùng ⇒ dừng ở checkpoint chủ kho;
không vay ngân sách của packet khác.

## 9. chua_do_duoc

- Kết quả `ai-dang-giu` (mục 1) đúng tới lúc đo trong ngày 06-11-2026; nó cũ đi theo từng nhánh mới, nên người cấp
  lease phải đo lại cả năm đường dẫn.
- Ca nào của t133/t137/t151 chạy được trên Windows native: chưa đo (mục 6 bước 1); t129 đã chạy native ở review lượt 2.
- Runner tập trung (mục 6 bước 3): chưa dựng bản thật; cơ chế lớp phủ mới được review lượt 2 thử trên clone tạm.
- B17 với **mã sản phẩm**: chưa đo. Số đo hiện có: số commit phía S theo N (mục 0) và mô phỏng thuật toán với bộ đọc
  nền thật trên PR #1268 ở review lượt 3–4. Thời gian thực cho N = 100 trên Windows (khoảng 581 commit) là ước lượng từ
  39 ms một object, chưa đo.
- Hàm xác nhận entry tree của runner (bảng xác nhận độc lập): chưa viết.
- Màu nền của các ca mới ngoài những ca ghi ở mục 5: chưa đo.
- Các trần ở mục 8 là đề xuất; chưa có số đo mức dùng thực của một packet cỡ này để biện hộ từng con số.
- Canary B18: chỉ đo được sau land.
- Số dòng thực tế: mới là ước lượng (khối `nang_tran`); trần 700 là đề xuất, chưa được chủ kho chốt.
- r5 chưa được review; trần review đặc tả đã dùng hết (mục 8).

## 10. Thay đổi so với r4

Thay đổi r1→r2, r2→r3, r3→r4 ghi ở mục 10 của từng revision ấy. Từ r4 sang r5 (verdict lượt 4 trên `d73af7a5`):

| nguồn | thay đổi |
|---|---|
| F16 `canary-thieu-dieu-kien-chon`, lần thứ tư, và biểu hiện thứ sáu của `phan-loai-vang-va-khong-do-duoc` (P2) — checkpoint lần 3 | bỏ điều kiện "vùng vắng hẳn" và bảng "vì sao suy ra rc 0"; B17 dùng đầu vào tự dựng trên lịch sử thật (H một cha là `S~N`, thêm một tệp ASCII ở gốc cây), N ∈ {10, 50, 100} trên hai nền, N = 500 trên Linux chỉ ghi lại; B17/B18 xếp kết quả theo bảng nguyên nhân đóng với bảng xác nhận độc lập bằng Git; khiếm khuyết dữ liệu chỉ được coi là "đầu vào không dùng được" khi Git xác nhận đúng object hay đường dẫn |
| F17 `ngan-sach-tien-xu-ly-pha-tuong-thich`, lần thứ hai (P2) | mục tiêu 4: miền của bất biến (mọi phép đọc và xác minh cũ lẫn mới thành công, đủ ngân sách), phép chiếu receipt tường minh (`schema_version`, hai bộ đếm, `thoi_diem_utc`, ba khoá mới bỏ; `ngan_sach` so sau khi bỏ đúng khoá mới), phần ngoài miền nêu cả lỗi xác minh của commit đọc thêm; ca mới B1c với đột biến `amb-m18`; câu R5 và mục tiêu 1d của A r5 sửa cùng ý |
| ghi chú review lượt 4: header nhiều dòng | mục tiêu 1 nói rõ dòng `committer` là header cấp đầu trước dòng trống, dòng tiếp nối không phải header mới, và phép kiểm áp cho cả commit chỉ đọc để xếp hàng |
| ghi chú review lượt 4: bảng ba trạng thái chưa nêu lỗi entry tree | mục 3 thêm tree có entry không hợp lệ vào cột "không đo được" của bước so vùng |
| số đo mới cho B17 | mục 0 ghi số commit phía S theo N trên `132d376c`; mục 2 ghi rõ không bảo đảm hiệu năng từ khoảng N = 200 trên Windows |
| checkpoint lần 3 | đầu tệp; mục 7 đếm lại (lớp kế thừa 6, canary bốn lần, F17 là lần hai), chốt canary chuyển sang lần thứ năm kèm phương án; mục 8 ghi trần 4 đã hết |
