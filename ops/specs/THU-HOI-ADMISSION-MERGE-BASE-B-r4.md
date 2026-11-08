# Đặc tả packet — `THU-HOI-ADMISSION-MERGE-BASE-B` (revision 4)

- `packet_id`: **THU-HOI-ADMISSION-MERGE-BASE-B** · `revision`: **4** · trạng thái: nháp, chờ chủ kho duyệt băm.
  Thay `ops/specs/THU-HOI-ADMISSION-MERGE-BASE-B-r3.md` (sha256
  `f366fda5c61705ec9915d026c43db40f9aeda404965d7d7f6957fbd3977cdbdd`), r2 (sha256
  `3f002496d380119c9093c072dda3c690afbfa140c21d6ddfdd792590c17dac69`) và r1 (sha256
  `a4e4a7aad7a885acccfd48c513644467a0b048833d50a0cb101992e400cf9ddf`); cả ba chưa từng được duyệt và giữ nguyên trong
  kho để verdict của từng lượt review vẫn tra được theo băm. Thay đổi so với r3: mục 10.
- Review Rescue Checkpoint (`ADR-0037`), hai lần trong ngày 07-11-2026: lần 1 sau review lượt 2 (F11) — chủ kho chọn
  sửa thành r3, giữ merge-base; lần 2 sau review lượt 3 (F14 là lần thứ ba của hình dạng `canary-thieu-dieu-kien-chon`)
  — chủ kho chọn **sửa thành r4, đổi gốc của canary**: B17/B18 chọn PR theo điều kiện "vùng vắng hẳn" (mục 5), không
  còn bộ tiền đề đoán kết quả của bộ kiểm.
- `packet_issue`: **#1266** (sub-issue của Mission #1264). Issue không tự cấp việc (protocol §3.2, §4).
- **Phụ thuộc:** packet `THU-HOI-ADMISSION-MERGE-BASE-A` #1265 (ADR-0066 và dòng §20, đặc tả
  `ops/specs/THU-HOI-ADMISSION-MERGE-BASE-A-r4.md`) đã land. Base của B phải chứa commit land của A; đo bằng
  `git merge-base --is-ancestor <land A> <base B>` ⇒ rc 0, không đo được ⇒ chưa cấp lease.
- `nguon_cap_viec`: như packet A — quyết định chủ kho trong phiên soạn spec 06-11-2026, vòng 1 Q1–Q7 và vòng 2
  Q8–Q13, cả hai *"Theo khuyến nghị"*; căn cứ tài liệu https://claude.ai/artifact/Au5vgKvAZWdqGDHMvkU4cW. Bản ghi
  bền ở thân Mission #1264 (phiên soạn spec đăng theo yêu cầu chủ kho); thẩm quyền ràng buộc là comment duyệt băm
  đặc tả này do chính chủ kho đăng trên #1266.
- `review_class`: **sensitive** — `ops/lease_publish.py` là cổng đọc lease (`ADR-0047`); chạm `.github/workflows/**`
  và `.claude/dev/**` (protocol §8).
- Base dự kiến: `origin/master` lúc cấp lease, sau khi A land (đo 08:44Z 07-11-2026: master `9607e3eb`, A chưa land).
- Executor **Claude**; reviewer **Codex** độc lập; `human_audited` trên exact head trước merge (vòng 1 Q6). Điều
  kiện merge theo `ADR-0060`.
- Windows: `required` theo `ADR-0060` M3, vì diff chạm `.github/workflows/**` và `.claude/dev/**` (mục 6).
- `full_mutant_audit`: bắt buộc theo M9/K7, vì diff chạm `ops/**/*.py`, `.claude/dev/**` và `.github/workflows/**`.
- Ngân sách đóng của packet (CI, M9, Windows, lời gọi model): mục 8.

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

```yaml
nang_tran:
  ai_nang: chủ kho ducthangho — vòng 1 Q7 của phiên soạn spec 06-11-2026 ("Theo khuyến nghị") cho trần 600; r2–r4 đề xuất 700, chủ kho chốt trong comment duyệt băm trên Issue
  can_cu: >-
    Ước lượng r4 540–700 dòng thêm, chưa đo: mã bộ kiểm ~120–160 (tô màu hai phía có luật ứng viên chưa stale, đọc giờ
    commit, lọc cực đại, hàm vùng, tích hợp, receipt); test bộ kiểm ~330–420 (18 hàng nghiệm thu nhóm B1–B12 ở mục 5,
    trong đó 16 hàng thuộc tệp này; r1 có 13 hàng, r2 có 15, r3 có 16); validator C1a1a và test ~90–120. So sánh gần
    nhất PR #620 (+204 dòng, 2 tệp; review lượt 1 đo lại: workflow +42, test +162). Receipt v2 và validator chấp nhận v2
    land cùng nhau trong packet này; nếu phải tách thì validator (consumer) land trước bộ kiểm (producer) là thứ tự an
    toàn, vì không có khoảng nào v2 được phát ra mà chưa ai hiểu — việc tách ấy cần packet mới và quyết định chủ kho.
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
- Review lượt 3 chạy mô phỏng bước tô màu với **bộ đọc nền thật** trên cùng snapshot (S = `9607e3eb`, H = `8f2224ac`):
  chỉ nhận ứng viên chưa stale ⇒ đúng merge-base `d26b36f5`, 33 object, 30.732 byte, **1,553 giây**, rc 0; nhận cả ứng
  viên đã stale rồi lọc từng cặp ⇒ 1.645 object, **hết deadline** ở 59,833 giây. Luật ứng viên ở mục tiêu 1 vì thế là
  một phần của hợp đồng, không phải chi tiết thi công.

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
r2–r4 không quét lại. Người cấp lease đo lại cả năm đường dẫn ngay trước khi cấp (L5).

## 2. ngoai_pham_vi

- Luật theo ID lease (R3/R4) và việc kiểm lại lúc land (R5): thuộc A1b (#656) và bên kiểm lúc land (#499 C1,
  #1179), vòng 1 Q5. Packet này chỉ ghi vào receipt dữ kiện để R5 dùng.
- `SO_THU_HOI_KICH_HOAT` giữ `False`; luật "chế độ chưa kích hoạt đòi tập revocation rỗng ở S và T" giữ nguyên.
- Chuyển tiếp Q13 (marker mới đòi `base_sha_before_add == S`) giữ nguyên. PR thêm tệp policy và marker vẫn cần S
  đúng bằng base của sự kiện; đó là việc của A1, rất hiếm, không phải nguồn sync hằng ngày.
- Các lệnh khác của `ops/lease_publish.py` (`check`, `body`, `kiem-github`, `ai-dang-giu`) và các bước của workflow.
- Đổi `KhoObject.doc` sang một tiến trình `cat-file --batch` dùng chung: không làm ở packet này; hiệu năng đạt bằng
  cách đọc ít object hơn (mục tiêu 1), đo ở B17.
- Hiệu năng trên đồ thị criss-cross dài: không bảo đảm. Bước lọc cực đại chỉ chạy khi có ≥ 2 ứng viên và chịu chung
  ngân sách; chạm trần ⇒ 12, PR hoà base là hết. Tính đúng của criss-cross do B5 đo; B17/B18 không dùng PR criss-cross.
- Vùng so sánh **không** gồm `ops/leases/**` (vòng 2 Q8). A1b phải mở rộng vùng khi bộ kiểm bắt đầu đọc lease.
- Đặc tả đã đóng băng (r9 của `THU-HOI-LEASE-VA-CAP-LAI`, r5 của `LAND-DOC-RECEIPT-THU-HOI-C1a1a`) và đặc tả #1179.
- WP1174 (#1174, bộ duyệt C6 chờ chủ kho, đo 15:0xZ 06-11-2026: chưa cấp lease) sửa `kiem-merge` trong
  `.claude/dev/packet_loop.py`. Packet này không thích nghi trước với thay đổi ấy: nếu WP1174 land trước khi B merge,
  điều kiện merge của B được đánh giá bằng mã canonical tại thời điểm merge.
- Ngoại lệ closure `ADR-0032` kiểu WP1174: không xin. Đo 02:43Z 07-11-2026 trên `origin/master` `9607e3eb`: dưới
  `ops/leases` có **179** tệp, gồm **175** tệp `.yaml`/`.yml` mà bộ quét lease xét và **4** tệp nháp `.yaml.nhap` mà
  bộ quét bỏ qua. `git grep -n -E '^\s*(ngoai_le_closure|closure_exception)\s*:' origin/master -- ops/leases` ra **3**
  tệp có khối `ngoai_le_closure` (`wp741-r3-g3-claude-20261015.yaml`, `wp741-r3-g4-claude-20261015.yaml`,
  `wp741-r3-g5-claude-20261016.yaml`, đều ở dòng 51, đều thuộc 175 tệp được xét), cả ba có
  `expiry: '2026-10-22T00:00:00Z'` nên **0** khối còn hiệu lực lúc đo. "Có khai báo" và "còn hiệu lực" là hai số khác
  nhau; số thứ hai đo theo `expiry` so với giờ đo, không chứng nhận quyền LIVE.

## 3. Bảng ba trạng thái — đóng, mọi bước mới phải theo

Bài học của lớp `phan-loai-vang-va-khong-do-duoc` (mục 7): "không thấy" và "không đo được" phải là hai nhánh khác
nhau trong mã, mỗi nhánh có ca test riêng.

| bước | kết quả "có" | kết quả "không" (đo được) | không đo được ⇒ rc 12 |
|---|---|---|---|
| tô màu hai phía (S, H) | tập merge-base cực đại đúng bằng `[S]` ⇒ S là tổ tiên H ⇒ chế độ `to_tien` | tập cực đại khác `[S]`: có ≥ 1 phần tử ⇒ chế độ `merge_base`; rỗng (lịch sử không chung gốc) ⇒ rc 12, nhãn `KHONG_CO_MERGE_BASE` | vượt `max_commits_merge_base` hoặc `max_unique_objects`, hết deadline reader, thiếu object, object băm không khớp tên, header commit hỏng, thiếu dòng `committer`, có hơn một dòng `committer`, hoặc giây trong dòng ấy không phải số nguyên |
| đếm cạnh (chỉ chế độ `to_tien`) | `KhoObject.to_tien(S, H)` như nền ⇒ `canh_ancestry` | — (bước trước đã chứng minh S là tổ tiên) | vượt `max_parent_path_edges` và mọi lỗi bộ đọc, như nền |
| so vùng (chỉ chế độ `merge_base`) | mọi merge-base có vùng bằng vùng tại S ⇒ đi tiếp các phép kiểm cũ trên T | một merge-base lệch ⇒ rc 12, nhãn `VUNG_LECH`, SHA của merge-base, đường dẫn lệch đầu tiên | `tim`/`namespace` gặp tổ tiên không phải thư mục, đọc object lỗi |

`refs/replace` và graft của kho nguồn **không có hiệu lực** với mọi bước trên: `KhoObject` đọc bằng
`cat-file --batch --no-replace-objects` trong `GIT_DIR` tạm cô lập và lấy cạnh từ bytes đã băm (đo 07-11-2026 trên
`9607e3eb`: `ops/lease_publish.py` dòng 1616 và 1913; ca t129 khẳng định cạnh gốc đọc đúng khi có replace; review lượt 2
dựng được replace làm Git chọn merge-base khác mà bộ đọc vẫn đọc cạnh thật). Kho nguồn shallow ⇒ 12 ngay khi dựng
`KhoObject` (dòng 1838), như hiện có. Mọi bước mới dùng cùng bộ đọc ấy.

Không bước mới nào được trả 0 khi một phép đo của nó không đo được, và không lỗi đọc vùng nào được đổi thành bản đồ
rỗng hay "vắng".

## 4. muc_tieu

1. `ops/lease_publish.py` — hàm **tô màu hai phía** cho (S, H) trên bộ đọc có băm của `KhoObject`. Hợp đồng, viết đủ
   để thi công không phải đoán (review lượt 3 đã mô phỏng đúng văn bản này trên 150 cặp DAG ngẫu nhiên có giờ lệch và
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
   - **Giờ commit.** Đọc từ đúng một dòng `committer <tên> <email> <giây> <múi giờ>` trong phần header của bytes đã băm;
     thiếu dòng, nhiều hơn một dòng, hay `<giây>` không phải số nguyên ⇒ 12 (B5c). Không lấy mặc định 0, không để
     `ValueError` hay lỗi Python khác thoát ra ngoài `Chan`.
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
   **Bất biến tương thích, phạm vi toàn pipeline.** Với mọi đầu vào mà S là tổ tiên của H:
   - nếu bộ kiểm mới không chạm trần ngân sách nào ở bất kỳ bước nào, thì rc, nhãn kết luận và mọi khoá receipt v1
     **trừ** `so_object_da_doc`, `tong_bytes` bằng của bộ kiểm nền; thông báo lỗi (khi rc ≠ 0) bằng của nền;
   - các con số đo tài nguyên — `object đã băm=` trên dòng `THU_HOI_ADMISSION`, `so_object_da_doc`, `tong_bytes` — được
     phép **lớn hơn** nền, vì bước tô màu đọc thêm commit (review lượt 3 đo: 3 thành 4 trên đồ thị `R→S→H`); dòng
     `THU_HOI_ADMISSION` thêm trường `quan_he=`;
   - ngân sách của `KhoObject` dùng chung cho mọi bước, nên bộ kiểm mới có thể chạm trần ở **bất kỳ** bước nào, kể cả
     phần sau bước tô màu, trong khi nền không chạm; khi ấy rc 12 — chặt hơn nền, không bao giờ lỏng hơn.
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
| B1b | S có `.github/coordination` là **tệp thường**; H là con của S và xoá tệp ấy; S là tổ tiên H | rc 0, `to_tien`, `vung_tai_S = null` (nền cũng rc 0 — bất biến tương thích của mục tiêu 4) | `amb-m13` gọi hàm vùng cả ở chế độ `to_tien` ⇒ `tim` gặp tổ tiên không phải thư mục ⇒ rc 12 ⇒ ca đỏ |
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
| B17 | Hiệu năng trên kho thật, trước merge, trên **cả** Linux lẫn `tra-luat-win`: PR thật đầu tiên **đủ điều kiện** theo điều kiện "vùng vắng hẳn" dưới đây; chạy bộ kiểm với S = tip master và H = head của PR ấy | rc 0, `merge_base`, không chạm trần nào trong `NGAN_SACH_MAC_DINH` kể cả `max_reader_wall_seconds` = 60; ghi thời gian, `so_object_da_doc`, `tong_bytes`, số commit bước tô màu đã đọc | trên PR đủ điều kiện, **mọi** kết quả khác (kể cả rc 12 vì hết deadline) ⇒ đỏ |
| B18 | Canary sau land: PR thật đầu tiên mà sự kiện `pull_request_target` của nó **đủ điều kiện** (S = `base.sha` của sự kiện) | check `thu-hoi` success; receipt đọc lại có `quan_he_S_H = merge_base` | **chưa đo được** tới khi có PR ấy; người land ghi run ID, S, H, merge-base, kết quả từng điều kiện và receipt đã đọc lại; PR đủ điều kiện mà check thất bại ⇒ đỏ |

**Điều kiện "vùng vắng hẳn" cho B17 và B18.** Đo bằng Git thường, độc lập với bộ kiểm; mọi lệnh chạy với
`GIT_NO_REPLACE_OBJECTS=1`, trên một clone không shallow, không có `info/grafts`; ghi lệnh và output từng điều kiện.

- (i) `git merge-base --is-ancestor S H` rc 1.
- (ii) `git merge-base --all S H` ra **đúng một** commit, gọi là B. Không dùng PR criss-cross cho B17/B18 (mục 2).
- (iii) Với mỗi X thuộc {S, B, H}: đi từ gốc cây theo hai chuỗi `ops` → `ops/thu-hoi` và `.github` →
  `.github/coordination` → `.github/coordination/change-impact.v1.json`, dừng ở thành phần **vắng** đầu tiên của mỗi
  chuỗi. Một thành phần **vắng** khi thành phần đứng trước nó (hoặc gốc cây) là `tree` và
  `git ls-tree X -- <đường dẫn>` không in gì. Một thành phần **có mặt** mà không phải phần tử cuối của chuỗi thì
  `git cat-file -t X:<đường dẫn>` phải là `tree`. Đạt khi, tại cả ba commit, `ops/thu-hoi` vắng và
  `.github/coordination/change-impact.v1.json` vắng.

Kết quả của điều kiện: **đủ điều kiện** (cả ba đo được và đúng); **không đủ điều kiện** (một điều kiện đo được và
sai); **không đo được** (một lệnh Git lỗi hoặc rc ngoài tập dự kiến). Hai kết quả sau đều làm PR không phải ca đo: bộ
kiểm trả gì cho PR ấy cũng chỉ ghi lại, không tính đạt hay đỏ, và đi tìm PR kế tiếp. Không có PR nào đủ điều kiện ⇒
B17/B18 ở trạng thái `chưa đo được`, không thay bằng một phép đo khác.

**Vì sao điều kiện này suy ra rc 0 cho toàn bộ bộ kiểm**, đối chiếu từng phép kiểm của `lenh_kiem_thu_hoi_github` trên
`9607e3eb` theo thứ tự chạy, không chỉ phép so vùng:

| bước (dòng trên `9607e3eb`) | với PR đủ điều kiện |
|---|---|
| dựng `KhoObject` (2359) | clone không shallow ⇒ không ném |
| bước tô màu (thay 2361) | (i) và (ii) ⇒ chế độ `merge_base`, `merge_bases = [B]`; nằm trong ngân sách — đây chính là thứ B17 đo |
| so vùng (mới) | vùng vắng tại S và B ⇒ bằng nhau |
| `namespace(tree_S)`, `namespace(tree_T)` (2364–2365) | `ops/thu-hoi` vắng, cha là `tree` hoặc vắng ⇒ hai bản đồ rỗng |
| append-only S→T (2367–2369) | bản đồ S rỗng ⇒ không có entry để kiểm |
| policy tại T (2371–2380) | tệp policy vắng, cha là `tree` hoặc vắng ⇒ `policy_T = None` |
| vòng lặp entry của T (2383–2405) | bản đồ T rỗng ⇒ không chạy |
| policy mà thiếu marker (2406) | `policy_T = None` ⇒ không áp |
| chế độ chưa kích hoạt (2408) | hai tập revocation rỗng ⇒ không áp |
| `tim(tree_S, PATH_BO_KIEM)` (2411) | trả entry hoặc `None`, không ném |

Vùng của bộ kiểm chưa từng được commit first-parent nào trên master chạm tới (đo 01:14Z 07-11-2026), nên kỳ vọng phần
lớn PR không criss-cross mà nhánh không tự thêm `ops/thu-hoi` hay tệp policy sẽ đủ điều kiện; điều kiện vẫn phải đo
cho **từng** PR, vì một commit ngoài first-parent (ví dụ trong nhánh đã merge) có thể từng chứa vùng. Với PR đủ điều
kiện, mọi kết quả khác rc 0 là đỏ, kể cả hết deadline.
Đo 07:45Z 07-11-2026: chính PR #1268 (S = `9607e3eb`, H = `8f2224ac`) đủ điều kiện — (i) rc 1; (ii) đúng một
merge-base `d26b36f5`; (iii) tại cả ba commit `ops`, `.github`, `.github/coordination` là `tree`, còn `ops/thu-hoi` và
tệp policy vắng; kho đo không có `refs/replace`, không shallow, không `info/grafts`.

**Năm vế L6 cho các tiêu chí khớp chuỗi:**

| tiêu chí | (a) dương / âm | (b) trọn mệnh đề, nối đoạn | (c) từng vị trí | (d) chữ / số | (e) đủ vị trí cổng |
|---|---|---|---|---|---|
| B10 | có cả hai vế | vế dương trọn câu mới, nối đoạn; vế âm dùng cụm lõi ngắn hơn câu cũ, chặt hơn chép nguyên câu | một khối chú thích | không có ngưỡng số | không phải lời khai về cổng |
| B12 | không còn là phép khớp chuỗi: dùng `ca_tinh` đo hành vi (import, audit hook) | không áp | không áp | không áp | không áp |
| nhãn `VUNG_LECH`, `KHONG_CO_MERGE_BASE` | dương trên thông báo mới; âm ở B9 (không được có hai nhãn) | nhãn là một token, không ngắt dòng | mỗi ca một nhãn | không có số | không áp |

**Màu trên nền.** Chỉ ghi màu đã **đo**; không suy màu nền từ đọc mã.

- B10 (07-11-2026, `9607e3eb`): câu cũ **1** lần, cụm lõi **1** lần, `ADR-0066` **0** lần — cả hai vế đỏ, đúng màu.
- B1b (review lượt 2 và 3 đo trên mã nền): rc 0, `TAP_THU_HOI_RONG`, `canh_ancestry = 1`. Ca B1b trên nền đỏ vì receipt v1
  thiếu `quan_he_S_H`; rc nền 0 là bất biến phải giữ.
- B5b (review lượt 3 đo): CLI nền rc 12 *"không phải tổ tiên"* — đỏ đúng màu (ca đòi rc 0). Oracle Git trả C; mô phỏng có
  đưa lại vào hàng đợi cho `[C]`, bỏ đưa lại cho `[]` (phiên soạn spec và review lượt 3 đo độc lập).
- B5d (phiên soạn spec đo 07-11-2026 bằng mô phỏng thuật toán theo đúng mục tiêu 1, ngoài kho): danh sách ứng viên
  trước lọc `[B]`; với đột biến `amb-m17` là `[B, R9, …, R0]`; số commit đọc như nhau (14) ở hai bản, nên ca phải đo
  danh sách ứng viên, không đo số object. Trên mã nền hàm tô màu chưa tồn tại ⇒ "không đo được trên nền", đúng loại.
- B5c (phiên soạn spec đo 07-11-2026): `git hash-object -t commit --literally -w` lưu được commit có giờ hỏng;
  `git --no-replace-objects cat-file --batch` đọc ra nguyên bytes; `git fsck` báo `badDate`. Màu nền của B5c chưa đo.
- B6 (review lượt 1 và 2 đo trên mã nền): rc 12 *"S không phải tổ tiên của H"*, thiếu nhãn `KHONG_CO_MERGE_BASE` — đỏ.
- B9 (review lượt 2 và 3 đo trên mã nền, `max_parent_path_edges = 1`): rc 12, `đường parent > 1 cạnh`, không nhãn mới —
  **xanh trên nền**, kể cả khi bước tô màu chạy trước; răng là `amb-m09` trên ứng viên.
- B12: `ca_tinh` hiện có xanh trên nền với fixture v1 (review lượt 1–3 đo); răng mới nằm ở `amb-m12b`.
- Mọi ca còn lại: **chưa đo** màu nền. Executor đo ngay sau khi viết fixture, trước khi sửa bộ kiểm, và ghi vào
  handoff. Ca xanh trên nền là bất biến, răng của nó phải đến từ đột biến; ca đỏ trên nền phải đỏ bằng assertion của
  chính ca (không vì lỗi nạp module hay thiếu thuộc tính), trừ B5d vốn gọi một hàm chưa có trên nền.
- B13: chưa chạy toàn bộ suite trên nền ở phiên này; số ca nền lấy từ CI của base khi cấp lease.

### 5.1 Kho ID đóng băng

Danh tính của một ca là **hậu tố tên** dưới đây, không phải số thứ tự. Trong `ops/lease_publish_test.py` mọi ca đăng ký
bằng decorator `@ca` vào danh sách `CA` (`CA` ở dòng 72, hàm `ca` ở dòng 79–81). Đo 01:14Z 07-11-2026 trên
`origin/master` `9607e3eb` bằng AST (hàm có decorator `ca`), review lượt 2 và 3 đo lại bằng `len(CA)`: **285** ca, 285
tên duy nhất, số lớn nhất `t237`. Tên có dạng `t<số>[chữ]_…`: 280 tên khớp `t[0-9]+_`, 5 tên có hậu tố chữ sau số
(`t02b_…`, `t02c_…`, `t02d_…`, `t55a_…`, `t55b_…`). Đếm ca thì đếm `CA`, không đếm theo mẫu tên; đếm hàng nghiệm thu
thì đếm hàng của bảng mục 5, kể cả hàng có hậu tố chữ (B1b, B3b, B5b, B5c, B5d, B8a, B8b). Executor chọn số kế tiếp còn
trống trên base của lease, giữ nguyên hậu tố. Mỗi hậu tố phải khớp **đúng một** hàm; không khớp hoặc khớp hai ⇒ runner
đỏ. Mỗi đột biến có ID riêng, đăng ký vào bảng đột biến sẵn có của tệp test tương ứng.

| ca | tệp | hậu tố / tên ca | ID đột biến | nền |
|---|---|---|---|---|
| B1 | `ops/lease_publish_test.py` | `_amb01_to_tien_giu_nguyen` | `amb-m01-luon-di-merge-base` | cả hai |
| B1b | `ops/lease_publish_test.py` | `_amb01b_to_tien_khong_doc_vung_S` | `amb-m13-luon-goi-ham-vung` | cả hai |
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
     trên clone thật của kho;
   - **có điều kiện**: t133 và các ca `_amb01`…`_amb09` (gồm `_amb01b`, `_amb03b`, `_amb05b`, `_amb05c`, `_amb05d`,
     `_amb08a`, `_amb08b`) — vào tập bắt buộc nếu t133 chạy native được ở bước 1; ca nào loại ra phải kèm lý do **đo
     được** ở bước 1 (lệnh, output), không kèm lý do suy từ tài liệu.

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
   `ung_vien`, với cùng S/H và cùng kết quả điều kiện "vùng vắng hẳn" như lượt B17 trên Linux.
5. Tiến trình test không được thấy credential LIVE: `TL_TOKEN`, `TL_WEBAPP`, `TL_MASTER_KEY`,
   `TL_AGENT_CREDS_FILEID` và các biến Drive/GAS/NLM khác phải vắng. Runner kiểm sự vắng mặt bằng giá trị đúng/sai,
   không in giá trị.

## 7. hinh_dang_ke_thua

Chép từ đặc tả #1179 r1 §7 (nhánh `claude/spec-1179-c1a1b`, commit `7cfb4d7`), quyết định chủ kho ở #1179 lúc
07:58Z 06-11-2026, và ba lượt review đặc tả của Mission này:

| lớp | số đếm | nguồn | chốt ở packet này |
|---|---|---|---|
| `phan-loai-vang-va-khong-do-duoc` | **5**: 4 từ #1179, cộng F11 của review lượt 2 (tiền đề canary đọc output `git ls-tree -r` rỗng thành "vắng" trong khi bộ đọc báo không đo được); review lượt 3 không thêm | #1179 r1 lượt 1 F4; verdict lượt 2 và 3 của PR #1268 | bảng đóng ở mục 3; ca B5c, B6, B7, B9; câu cấm đổi lỗi đọc vùng thành bản đồ rỗng; điều kiện "vùng vắng hẳn" có trạng thái "không đủ điều kiện" riêng cho thành phần cha không phải thư mục |
| `mo-rong-module-pha-hop-dong-json-thuan` | 3 | #1179 review draft0–2 | mục tiêu 7 giữ thuần JSON; ca B12 (`ca_tinh` có fixture v2) |
| `nguon-duoc-tin-ma-chua-xac-minh` | 7 (chuỗi thu hồi) | spec C1a1a r5 §6 | merge-base chỉ tính bằng bộ đọc có băm; ca B8a, B8b |

Các hình dạng lỗi riêng của Mission này (đếm theo verdict lượt 3):

| hình dạng | các lần | chốt ở r4 |
|---|---|---|
| `canary-thieu-dieu-kien-chon` | F06, F11, **F14** (ba lần ⇒ checkpoint lần 2) | gốc rễ là đoán kết quả của bộ kiểm từ tiền đề rời; r4 chọn PR theo điều kiện "vùng vắng hẳn" và đối chiếu điều kiện ấy với **từng** phép kiểm của bộ kiểm (bảng ở mục 5) |
| `receipt-moi-lam-doi-nhanh-cu` | F01, F09 | mục tiêu 3 tách phép đọc thêm khỏi ba phép đọc cũ |
| `nghiem-thu-do-nham-chot` | F03, F10 | mục 5 chỉ ghi màu nền đã đo |
| `dem-ca-bang-mau-ten` | F02, F13 | đơn vị "hàng nghiệm thu" đếm cả hàng có hậu tố chữ |
| `dem-sai-ngoai-le-closure` | F07, F12 | mẫu số tách 175 tệp được xét và 4 tệp nháp |
| `ngan-sach-tien-xu-ly-pha-tuong-thich` | F15 | mục tiêu 4: bất biến tương thích phạm vi toàn pipeline; telemetry được tăng; trần ở bất kỳ bước nào ⇒ 12 |

Một biểu hiện mới của **bất kỳ** lớp kế thừa nào ở bất kỳ lượt review nào (đặc tả hay PR thi công) ⇒ DỪNG, Review
Rescue Checkpoint (`ADR-0037`), báo chủ kho; không vá tiếp theo chỗ bị chỉ. Một hình dạng đang ở hai lần mà xuất hiện
**lần thứ ba**, hoặc `canary-thieu-dieu-kien-chon` xuất hiện **lần thứ tư**, ⇒ cũng DỪNG và chủ kho xét lại cách làm.
Phương án đã biết cho lần thứ tư của canary: bỏ hẳn B17/B18 dạng chọn PR thật, đo hiệu năng bằng một kho sao chép
lịch sử thật mà không cần đoán kết quả của bộ kiểm.

## 8. Review và ngân sách đóng

**Review đặc tả, trước khi chủ kho duyệt băm:** Codex, tính trên PR đưa đặc tả vào kho, chung cho A và B; trần ban đầu
≤ 2 lời gọi, chủ kho nâng thành 3; **đã dùng hết** (lượt 1 trên r1, lượt 2 trên r2, lượt 3 trên r3; lượt 0 không tính
theo chủ kho). Lịch sử: mục 6 của đặc tả A r4. Review r4 cần chủ kho nâng trần trước lời gọi; chưa có lời gọi nào cho r4.

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
- Số object và thời gian của bước tô màu trên kho thật (B17) với **mã sản phẩm**: chưa đo; số đo hiện có là mô phỏng
  thuật toán với bộ đọc nền thật ở review lượt 3 (33 object, 1,553 giây, mục 0).
- Màu nền của B5c và các ca mới khác ngoài những ca ghi ở mục 5: chưa đo.
- Các trần ở mục 8 là đề xuất; chưa có số đo mức dùng thực của một packet cỡ này để biện hộ từng con số.
- Canary B18: chỉ đo được sau land.
- Số dòng thực tế: mới là ước lượng (khối `nang_tran`); trần 700 là đề xuất, chưa được chủ kho chốt.
- r4 chưa được review; trần review đặc tả đã dùng hết (mục 8).

## 10. Thay đổi so với r3

Thay đổi r1→r2 ghi ở mục 10 của r2; r2→r3 ở mục 10 của r3. Từ r3 sang r4 (verdict lượt 3 trên `8f2224ac`):

| nguồn | thay đổi |
|---|---|
| F14 `canary-thieu-dieu-kien-chon`, lần thứ ba (P2) — checkpoint lần 2 | bỏ bộ tiền đề năm điều; B17/B18 chọn PR theo điều kiện "vùng vắng hẳn" tại S, merge-base duy nhất B và H; thêm bảng đối chiếu điều kiện ấy với **từng** phép kiểm của bộ kiểm (dòng 2359–2411); đo PR #1268 đủ điều kiện |
| F15 `ngan-sach-tien-xu-ly-pha-tuong-thich` (P2) | mục tiêu 4: bất biến tương thích phạm vi toàn pipeline — kết quả nghiệp vụ bằng nền khi không chạm trần; telemetry được tăng; trần ở bất kỳ bước nào ⇒ 12. Câu R2 của A r4 sửa cùng ý |
| ghi chú review lượt 3: văn bản thuật toán chưa đủ để thi công đúng | mục tiêu 1 viết hợp đồng đầy đủ: cờ và phép OR, đưa lại vào hàng đợi, **chỉ ứng viên chưa stale**, điều kiện dừng, lọc cực đại chỉ khi ≥ 2 ứng viên, đọc giờ từ đúng một dòng `committer`, đơn vị đếm ngân sách |
| ghi chú review lượt 3: nhận ứng viên stale làm hết deadline trên PR thật | mục 0 ghi số đo (33 object, 1,553 s so với hết deadline); ca B5d với đột biến `amb-m17`, đã đo bằng mô phỏng rằng đột biến đổi danh sách ứng viên |
| ghi chú review lượt 3: parser `committer` chưa có | bảng mục 3 nêu ba dạng hỏng ⇒ 12; ca B5c với đột biến `amb-m16`, fixture đã thử dựng được |
| ghi chú review lượt 3: 5.462 là số của `d26b36f`, không phải master | mục 0 ghi 5.481 commit trên `9607e3eb` |
| ghi chú review lượt 3: hiệu năng criss-cross | mục 2 ghi rõ không bảo đảm; B17/B18 đòi đúng một merge-base |
| checkpoint lần 2 | đầu tệp; mục 7 đếm lại hình dạng (canary ba lần, F15 một lần), chốt "lần thứ tư" kèm phương án đã biết; mục 8 ghi trần 3 đã hết |
