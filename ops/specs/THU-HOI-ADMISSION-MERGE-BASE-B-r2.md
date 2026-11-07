# Đặc tả packet — `THU-HOI-ADMISSION-MERGE-BASE-B` (revision 2)

- `packet_id`: **THU-HOI-ADMISSION-MERGE-BASE-B** · `revision`: **2** · trạng thái: nháp, chờ chủ kho duyệt băm.
  Thay `ops/specs/THU-HOI-ADMISSION-MERGE-BASE-B-r1.md` (sha256
  `a4e4a7aad7a885acccfd48c513644467a0b048833d50a0cb101992e400cf9ddf`, chưa được duyệt); r1 giữ nguyên trong kho để verdict
  review lượt 1 vẫn tra được theo băm. Thay đổi so với r1: mục 10.
- `packet_issue`: **#1266** (sub-issue của Mission #1264). Issue không tự cấp việc (protocol §3.2, §4).
- **Phụ thuộc:** packet `THU-HOI-ADMISSION-MERGE-BASE-A` #1265 (ADR-0066 và dòng §20, đặc tả
  `ops/specs/THU-HOI-ADMISSION-MERGE-BASE-A-r2.md`) đã land. Base của B phải chứa commit land của A; đo bằng
  `git merge-base --is-ancestor <land A> <base B>` ⇒ rc 0, không đo được ⇒ chưa cấp lease.
- `nguon_cap_viec`: như packet A — quyết định chủ kho trong phiên soạn spec 06-11-2026, vòng 1 Q1–Q7 và vòng 2
  Q8–Q13, cả hai *"Theo khuyến nghị"*; căn cứ tài liệu https://claude.ai/artifact/Au5vgKvAZWdqGDHMvkU4cW. Bản ghi
  bền ở thân Mission #1264 (phiên soạn spec đăng theo yêu cầu chủ kho); thẩm quyền ràng buộc là comment duyệt băm
  đặc tả này do chính chủ kho đăng trên #1266.
- `review_class`: **sensitive** — `ops/lease_publish.py` là cổng đọc lease (`ADR-0047`); chạm `.github/workflows/**`
  và `.claude/dev/**` (protocol §8).
- Base dự kiến: `origin/master` lúc cấp lease, sau khi A land (đo 01:14Z 07-11-2026: master `9607e3eb`, A chưa land).
- Executor **Claude**; reviewer **Codex** độc lập; `human_audited` trên exact head trước merge (vòng 1 Q6). Điều
  kiện merge theo `ADR-0060`.
- Windows: `required` theo `ADR-0060` M3, vì diff chạm `.github/workflows/**` và `.claude/dev/**` (mục 6).
- `full_mutant_audit`: bắt buộc theo M9/K7, vì diff chạm `ops/**/*.py`, `.claude/dev/**` và `.github/workflows/**`.
- Ngân sách đóng của packet (CI, M9, Windows, lời gọi model): mục 8.

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

```yaml
nang_tran:
  ai_nang: chủ kho ducthangho — vòng 1 Q7 của phiên soạn spec 06-11-2026 ("Theo khuyến nghị") cho trần 600; r2 đề xuất 700, chủ kho chốt trong comment duyệt băm trên Issue
  can_cu: >-
    Ước lượng r2 520–680 dòng thêm, chưa đo: mã bộ kiểm ~100–150; test bộ kiểm ~300–400 (r1 có 12 ca, r2 thêm B1b, tách
    B8 thành B8a/B8b, B3b có đột biến riêng); validator C1a1a và test ~120–130 (thêm ba ca bảng, fixture v2 cho ca_tinh).
    So sánh gần nhất PR #620 (+204 dòng, 2 tệp; review lượt 1 đo lại: workflow +42, test +162). Receipt v2 và validator
    chấp nhận v2 là một thay đổi hợp đồng, land cùng nhau để không có khoảng nào bên này nói v2 mà bên kia chỉ hiểu v1.
  tran_cu: "≤ 6 tệp / ≤ 450 dòng thêm (ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab)"
  tran_moi: "≤ 6 tệp / ≤ 700 dòng thêm, đo bằng git diff --numstat origin/master...HEAD; vượt thì dừng ở checkpoint chủ kho, không tự bỏ ca của mục 5"
```

## 0. Vấn đề

Như mục 0 của packet A. Tóm lại: `lenh_kiem_thu_hoi_github` gọi `kho.to_tien(S, H)` và trả 12 khi S không phải tổ
tiên của H. Packet A chỉ đăng ký `ADR-0066` và dòng §20; luật mới có hiệu lực từ commit land của **packet này** trên
first-parent master, trước đó luật cũ giữ nguyên (ADR-0066, mục Hiệu lực). Packet này thi hành luật trong mã.

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
r2 không quét lại. Người cấp lease đo lại cả năm đường dẫn ngay trước khi cấp (L5).

## 2. ngoai_pham_vi

- Luật theo ID lease (R3/R4) và việc kiểm lại lúc land (R5): thuộc A1b (#656) và bên kiểm lúc land (#499 C1,
  #1179), vòng 1 Q5. Packet này chỉ ghi vào receipt dữ kiện để R5 dùng.
- `SO_THU_HOI_KICH_HOAT` giữ `False`; luật "chế độ chưa kích hoạt đòi tập revocation rỗng ở S và T" giữ nguyên.
- Chuyển tiếp Q13 (marker mới đòi `base_sha_before_add == S`) giữ nguyên. PR thêm tệp policy và marker vẫn cần S
  đúng bằng base của sự kiện; đó là việc của A1, rất hiếm, không phải nguồn sync hằng ngày.
- Các lệnh khác của `ops/lease_publish.py` (`check`, `body`, `kiem-github`, `ai-dang-giu`) và các bước của workflow.
- Vùng so sánh **không** gồm `ops/leases/**` (vòng 2 Q8). A1b phải mở rộng vùng khi bộ kiểm bắt đầu đọc lease.
- Đặc tả đã đóng băng (r9 của `THU-HOI-LEASE-VA-CAP-LAI`, r5 của `LAND-DOC-RECEIPT-THU-HOI-C1a1a`) và đặc tả #1179.
- WP1174 (#1174, bộ duyệt C6 chờ chủ kho, đo 15:0xZ 06-11-2026: chưa cấp lease) sửa `kiem-merge` trong
  `.claude/dev/packet_loop.py`. Packet này không thích nghi trước với thay đổi ấy: nếu WP1174 land trước khi B merge,
  điều kiện merge của B được đánh giá bằng mã canonical tại thời điểm merge.
- Ngoại lệ closure `ADR-0032` kiểu WP1174: không xin. Đo 01:14Z 07-11-2026 trên `origin/master` `9607e3eb` bằng
  `git grep -n -E '^\s*(ngoai_le_closure|closure_exception)\s*:' origin/master -- ops/leases`: trong **179** tệp lease,
  **3** tệp có khối `ngoai_le_closure` (`wp741-r3-g3-claude-20261015.yaml`, `wp741-r3-g4-claude-20261015.yaml`,
  `wp741-r3-g5-claude-20261016.yaml`, đều ở dòng 51), cả ba có `expiry: '2026-10-22T00:00:00Z'` nên **0** khối còn
  hiệu lực lúc đo. "Có khai báo" và "còn hiệu lực" là hai số khác nhau; số thứ hai đo theo `expiry` so với giờ đo.

## 3. Bảng ba trạng thái — đóng, mọi bước mới phải theo

Bài học của lớp `phan-loai-vang-va-khong-do-duoc` (mục 7): "không thấy" và "không đo được" phải là hai nhánh khác
nhau trong mã, mỗi nhánh có ca test riêng.

| bước | kết quả "có" | kết quả "không" (đo được) | không đo được ⇒ rc 12 |
|---|---|---|---|
| quan hệ S→H | đi parent từ H gặp S ⇒ `to_tien`, ghi số cạnh; **dừng ở đây**, không đọc vùng, không tính merge-base | duyệt hết tổ tiên của H trong ngân sách mà không gặp S ⇒ sang bước merge-base | vượt `max_parent_path_edges` hoặc `max_unique_objects`, thiếu object, object băm không khớp tên, hết deadline reader |
| tập merge-base | ≥ 1 merge-base, tính trọn trong ngân sách | 0 merge-base (lịch sử không chung gốc) ⇒ rc 12, thông báo có nhãn `KHONG_CO_MERGE_BASE` | vượt `max_commits_merge_base` hoặc `max_unique_objects`, thiếu object, object hỏng |
| so vùng (chỉ chế độ `merge_base`) | mọi merge-base có vùng bằng vùng tại S ⇒ đi tiếp các phép kiểm cũ trên T | một merge-base lệch ⇒ rc 12, thông báo có nhãn `VUNG_LECH`, SHA của merge-base, đường dẫn lệch đầu tiên | `tim`/`namespace` gặp tổ tiên không phải thư mục, đọc object lỗi |

`refs/replace` và graft của kho nguồn **không có hiệu lực** với mọi bước trên: `KhoObject` đọc bằng
`cat-file --batch --no-replace-objects` trong `GIT_DIR` tạm cô lập và lấy cạnh từ bytes đã băm (đo 07-11-2026 trên
`9607e3eb`: `ops/lease_publish.py` dòng 1616 và 1913; ca t129 khẳng định cạnh gốc đọc đúng khi có replace). Kho nguồn
shallow ⇒ 12 ngay khi dựng `KhoObject` (dòng 1838), như hiện có. Bộ tính merge-base mới phải dùng cùng bộ đọc ấy.

Không bước mới nào được trả 0 khi một phép đo của nó không đo được, và không lỗi đọc vùng nào được đổi thành bản đồ
rỗng hay "vắng".

## 4. muc_tieu

1. `ops/lease_publish.py` — hàm ba trạng thái cho quan hệ S→H (trả số cạnh, hoặc "không phải tổ tiên", hoặc ném
   rc 12 khi không đo được) dùng chung bộ đọc có băm của `KhoObject`. `KhoObject.to_tien` giữ nguyên hành vi bên
   ngoài (ném 12 với thông báo *"không phải tổ tiên"* khi không phải tổ tiên) cho mọi chỗ gọi hiện có, gồm t129.
2. `ops/lease_publish.py` — tính **mọi** merge-base của (S, H) bằng bộ đọc có băm: giao tập tổ tiên của hai phía,
   lấy các phần tử cực đại. Khoá ngân sách mới `max_commits_merge_base` = **50.000** commit đã đọc cho một lần tính
   (cả hai phía) trong `NGAN_SACH_MAC_DINH`. Căn cứ: #1179 đo toàn lịch sử master **5.444** commit, 8.480.418 byte,
   0,34 giây (07:23Z 06-11-2026 trên `889334fb`), tức trần dư khoảng 9 lần; review lượt 1 đo lại cùng số commit và
   byte, 0,393 giây trên máy khác. Không gọi `git merge-base` hay Git plumbing nào khác.
3. `ops/lease_publish.py` — hàm vùng của một commit: bản đồ `ops/thu-hoi/**` qua `KhoObject.namespace`, cộng mục
   `PATH_POLICY_CLOSURE` qua `KhoObject.tim` (vắng ⇒ không có khoá; tổ tiên không phải thư mục ⇒ 12, như hành vi
   hiện có). Hàm này **chỉ** được gọi ở chế độ `merge_base`, cho S và cho từng merge-base; so theo bảng mục 3. Ở chế
   độ `to_tien` bộ kiểm không đọc vùng tại S hay tại merge-base nào.
4. `ops/lease_publish.py` — `lenh_kiem_thu_hoi_github` dùng mục tiêu 1–3 thay cho `kho.to_tien(S, H)`; mọi phép
   kiểm còn lại (append-only S→T, validator namespace T, Q13, chế độ chưa kích hoạt) giữ nguyên thứ tự và mã thoát.
   **Bất biến tương thích:** với mọi đầu vào mà S là tổ tiên của H, rc và các dòng thông báo của bộ kiểm mới bằng
   của bộ kiểm nền, trừ trường `quan_he=` mới trên dòng `THU_HOI_ADMISSION` và các khoá receipt mới.
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
   (sẽ là 9); executor tìm đủ bằng `rg -n 'ngan_sach|schema_version|canh_ancestry' ops/lease_publish_test.py` và ghi
   danh sách chốt đã sửa vào handoff.
6. `.github/workflows/ops-thu-hoi-admission.yml` — trong khối chú thích đầu tệp, thay câu cũ *"Bộ kiểm còn đòi S là
   tổ tiên của H — đó là thiết kế fail-close giữ nguyên theo quyết định chủ kho cho #618 (đường (a)), không phải
   dương tính giả."* bằng **đúng** câu mới sau (chép nguyên văn, được ngắt dòng tuỳ ý):
   *"Bộ kiểm không còn đòi S là tổ tiên của H (ADR-0066): khi S không phải tổ tiên của H, vùng bộ kiểm đọc phải giống
   hệt tại S và tại mọi merge-base của (S, H), rồi mọi phép kiểm chạy trên T = tree(H)."*
   Không đổi dòng nào ngoài khối chú thích; không viết cú pháp biểu thức Actions trong chú thích.
7. `.claude/dev/doc_receipt_thu_hoi.py` — nhận receipt v1 (đúng 38 khoá như hiện nay, đo 07-11-2026 trên `9607e3eb`)
   **và** v2 (đúng 41 khoá), mỗi phiên bản là một tập khoá đóng riêng. Luật riêng của v2: `quan_he_S_H` thuộc hai giá
   trị trên; `merge_bases` là danh sách SHA40 không rỗng, không trùng, sắp tăng; `to_tien` ⇒ `merge_bases == [S]`,
   `canh_ancestry` là số nguyên ≥ 0 và `vung_tai_S` là `null`; `merge_base` ⇒ `canh_ancestry` là `null`, S không nằm
   trong `merge_bases` và `vung_tai_S` là dict khoá chuỗi, mỗi giá trị là danh sách đúng 3 phần tử: mode thuộc
   `100644` `100755` `120000` `160000` `040000`, kiểu thuộc `blob` `tree` `commit`, OID là SHA40. Module giữ thuần JSON:
   không git, không mạng; tập import cho phép giữ nguyên như `ca_tinh` đang kiểm (`argparse`, `json`, `re`, `sys`).
8. `.claude/dev/doc_receipt_thu_hoi_test.py` — các ca B11, B12 ở mục 5; thêm fixture v2 (`to_tien` và `merge_base`)
   vào đầu vào của `ca_tinh`; thêm đột biến từng trường cho ba khoá mới vào bảng sẵn có (`_theo_truong`).

## 5. nghiem_thu

Mọi ca "đỏ" kèm một đột biến làm ca đổi màu (L3). Fixture dựng đồ thị Git thật trong thư mục tạm, như t133, và gọi
bộ kiểm qua đúng lối vào CLI mà t133 dùng (`_goi_main(mod, "kiem-thu-hoi-github", …)`), để cùng một ca chạy được trên
mã nền lẫn mã ứng viên. Ngân sách nhỏ và seam `sau_cat_file` được tiêm qua thuộc tính module, như t133 tiêm
`DESCRIPTOR_Q13_SHA256` (API nội bộ, không có đường CLI); seam `sau_cat_file` dùng theo khuôn của t130. "Thông báo có nhãn X" nghĩa là stderr chứa nguyên chuỗi X.

| # | ca | kỳ vọng | đột biến phải làm ca đổi màu |
|---|---|---|---|
| B1 | S là tổ tiên H | rc 0; receipt v2, `quan_he_S_H = to_tien`, `merge_bases = [S]`, `canh_ancestry` số nguyên, `vung_tai_S = null` | `amb-m01` luôn đi nhánh merge-base ⇒ `quan_he_S_H` khác ⇒ ca đỏ |
| B1b | S có `.github/coordination` là **tệp thường**; H là con của S và xoá tệp ấy; S là tổ tiên H | rc 0, `to_tien`, `vung_tai_S = null` (nền cũng rc 0 — bất biến tương thích của mục tiêu 4) | `amb-m13` luôn đọc vùng tại S ⇒ `tim` gặp tổ tiên không phải thư mục ⇒ rc 12 ⇒ ca đỏ |
| B2 | H rẽ từ B, master đi tiếp và đổi tệp ngoài vùng | rc 0; `merge_base`, `merge_bases = [B]`, `canh_ancestry = null`, `vung_tai_S` là dict | `amb-m02` bắt lại `to_tien` ⇒ rc 12 ⇒ ca đỏ |
| B3 | Master thêm `.github/coordination/change-impact.v1.json` sau B | rc 12, nhãn `VUNG_LECH`, không receipt | `amb-m03` bỏ cổng so vùng ⇒ rc khác 12 hoặc thiếu nhãn ⇒ ca đỏ |
| B3b | Master thêm một bản ghi thu hồi vào `ops/thu-hoi/` sau B; H không có nó | rc 12, nhãn `VUNG_LECH`, không receipt | `amb-m03` bỏ cổng so vùng ⇒ append-only S→T chạy trước và trả **8** (bản ghi ở S vắng ở T) ⇒ ca đỏ |
| B4 | B và S có cùng một bản ghi; H **xoá** bản ghi ấy; S không là tổ tiên H | rc 8, thông báo có `append-only` | `amb-m04` bỏ phép append-only ⇒ tới chốt chưa kích hoạt, rc 12 ⇒ ca đỏ |
| B5 | Criss-cross: hai merge-base, merge-base đứng đầu theo thứ tự sắp có vùng bằng S, cái còn lại lệch (review lượt 1 đã dựng được topology này) | rc 12, nhãn `VUNG_LECH`, thông báo nêu SHA của merge-base lệch | `amb-m05` chỉ so merge-base đầu ⇒ rc 0 ⇒ ca đỏ |
| B6 | S và H không chung gốc | rc 12, nhãn `KHONG_CO_MERGE_BASE` | `amb-m06` coi "0 merge-base" là đạt ⇒ rc 0 ⇒ ca đỏ |
| B7 | `max_commits_merge_base` nhỏ hơn số commit phải đọc | rc 12, thông báo nêu `max_commits_merge_base` | `amb-m07` nuốt lỗi vượt ngân sách ⇒ rc 0 ⇒ ca đỏ |
| B8a | Kho nguồn có một `refs/replace` làm `git merge-base --all` (vốn theo replace) trả một commit có vùng bằng S, trong khi merge-base thật trên đồ thị đã băm có vùng lệch | rc 12, nhãn `VUNG_LECH`, thông báo nêu SHA của merge-base **thật** | `amb-m08` tính merge-base bằng `git merge-base --all` trên kho nguồn ⇒ rc 0 ⇒ ca đỏ |
| B8b | Một commit chỉ tới được từ phía S (không thuộc tổ tiên của H) bị seam `sau_cat_file` đổi bytes, nên băm không khớp tên | rc 12, thông báo băm lệch của bộ đọc nêu OID ấy; nhật ký seam cho thấy mọi tổ tiên của H đã được đọc **trước** OID ấy, tức bước S→H đã xong và lỗi chỉ lộ trong phần duyệt merge-base | `amb-m14` phần duyệt merge-base đọc cha bằng đường không băm lại ⇒ không thấy lỗi băm ⇒ ca đỏ |
| B9 | Vượt ngân sách **trong lúc** xét S→H (trước bước merge-base) | rc 12, thông báo vượt ngân sách, **không** có `KHONG_CO_MERGE_BASE` hay `VUNG_LECH` | `amb-m09` xếp "vượt ngân sách" vào nhánh "không phải tổ tiên" ⇒ đi tiếp merge-base ⇒ rc 0 ⇒ ca đỏ |
| B10 | Chú thích workflow, đo trên văn bản đã nối dòng từng đoạn (bỏ `#` và khoảng trắng đầu mỗi dòng chú thích, dòng `#` trống ngắt đoạn, gộp khoảng trắng): vế dương có nguyên câu mới ở mục tiêu 6; vế âm không còn cụm *"Bộ kiểm còn đòi S là tổ tiên của H"* | cả hai vế đạt | `amb-m10` ghi lại câu cũ ⇒ vế âm đỏ; bỏ *"không còn"* khỏi câu mới ⇒ vế dương đỏ; đổi *"mọi merge-base"* thành *"một merge-base"* ⇒ vế dương đỏ; cắt hậu tố *", rồi mọi phép kiểm chạy trên T = tree(H)."* ⇒ vế dương đỏ; ngắt dòng lại giữ nguyên chữ ⇒ vẫn đạt |
| B11 | `doc_receipt_thu_hoi`: v1 hiện có ⇒ `ok`; v2 `to_tien` ⇒ `ok`; v2 `merge_base` ⇒ `ok`; mỗi ca sau ⇒ `do`: v2 thiếu `merge_bases`, thừa một khoá, `to_tien` với `merge_bases ≠ [S]`, `merge_base` với `canh_ancestry` số, `to_tien` với `vung_tai_S` là dict, `merge_base` với `vung_tai_S = null`, `vung_tai_S` có giá trị 2 phần tử, `schema_version = 3` | như cột trái | `amb-m11` bỏ kiểm tập khoá v2 ⇒ ca thiếu/thừa khoá thành `ok` ⇒ ca đỏ; đột biến từng trường của `_theo_truong` cho ba khoá mới |
| B12 | `ca_tinh` chạy trên fixture v1 **và** hai fixture v2: tập import ⊆ {`argparse`, `json`, `re`, `sys`}, audit hook không ghi sự kiện nào, kết quả tất định | ca đạt | `amb-m12` thêm `import subprocess` ⇒ tập import lệch ⇒ ca đỏ; `amb-m12b` thêm một lời gọi `open(...)` chỉ trong nhánh xử lý v2 ⇒ audit hook ghi sự kiện ⇒ ca đỏ (đột biến này chỉ bị bắt khi fixture v2 có trong `ca_tinh`) |
| B13 | Toàn bộ `ops/lease_publish_test.py` và `.claude/dev/doc_receipt_thu_hoi_test.py` trên CI Linux của exact head báo `N/N` với hai số bằng nhau | lệch | — (bằng chứng dương, không tin `rc=0` một mình) |
| B14 | Windows, mục 6 | xanh theo `ADR-0060` M3 (a)–(c) | — |
| B15 | `ci-dot-bien-du.yml` thành công trên exact head, mọi job `success` (K7) | thiếu hoặc đỏ | — |
| B16 | Kích thước theo `nang_tran`: ≤ 6 tệp, ≤ 700 dòng thêm; không tệp ngoài `write_set` | vượt hoặc tệp lạ | thêm một tệp ⇒ đỏ |
| B17 | Hiệu năng trên kho thật, trước merge: chọn PR thật đầu tiên thoả **mọi** tiền đề đo độc lập dưới đây, rồi chạy bộ kiểm với S = tip master và H = head của PR ấy | rc 0, `merge_base`; ghi thời gian, `so_object_da_doc`, `tong_bytes`; không chạm trần | rc 12 khi mọi tiền đề thoả ⇒ đỏ |
| B18 | Canary sau land: PR thật đầu tiên mà sự kiện `pull_request_target` của nó thoả **mọi** tiền đề dưới đây (S = `base.sha` của sự kiện) | check `thu-hoi` success; receipt đọc lại có `quan_he_S_H = merge_base` | **chưa đo được** tới khi có PR ấy; người land ghi run ID, S, H, tập merge-base, vùng và receipt đã đọc lại |

**Tiền đề của B17 và B18**, đo bằng công cụ độc lập với bộ kiểm (Git thường, trên một clone không có `refs/replace`:
`git for-each-ref refs/replace` rỗng), ghi lệnh và kết quả từng cái: (i) `git merge-base --is-ancestor S H` rc 1;
(ii) `git merge-base --all S H` ra ≥ 1 commit; (iii) với từng commit X ở (ii) và với S, `git ls-tree -r X --
ops/thu-hoi .github/coordination/change-impact.v1.json` ra cùng một output; (iv) tại H, `ops/thu-hoi/` vắng hoặc
rỗng và không có tệp policy (đúng điều kiện chế độ chưa kích hoạt). PR không thoả một tiền đề thì **không phải** ca
đo: bộ kiểm trả 12 cho nó là từ chối đúng luật, ghi lại nhưng không tính là đạt hay đỏ, và đi tìm PR kế tiếp. Không có
PR nào thoả ⇒ B17/B18 ở trạng thái `chưa đo được`, không thay bằng một phép đo khác.

**Năm vế L6 cho các tiêu chí khớp chuỗi:**

| tiêu chí | (a) dương / âm | (b) trọn mệnh đề, nối đoạn | (c) từng vị trí | (d) chữ / số | (e) đủ vị trí cổng |
|---|---|---|---|---|---|
| B10 | có cả hai vế | vế dương trọn câu mới, nối đoạn; vế âm dùng cụm lõi ngắn hơn câu cũ, chặt hơn chép nguyên câu | một khối chú thích | không có ngưỡng số | không phải lời khai về cổng |
| B12 | không còn là phép khớp chuỗi: r2 dùng `ca_tinh` đo hành vi (import, audit hook); bỏ phép đếm từ của r1 | không áp | không áp | không áp | không áp |
| nhãn `VUNG_LECH`, `KHONG_CO_MERGE_BASE` | dương trên thông báo mới; âm ở B9 (không được có hai nhãn) | nhãn là một token, không ngắt dòng | mỗi ca một nhãn | không có số | không áp |

Chạy thử trên nền:

- B10 (07-11-2026, `9607e3eb`): trên văn bản chú thích đã nối dòng từng đoạn, câu cũ có mặt **1** lần, cụm lõi
  *"Bộ kiểm còn đòi S là tổ tiên của H"* **1** lần, `ADR-0066` **0** lần — cả hai vế đỏ, đúng màu "chưa làm".
- B1b: review lượt 1 dựng đúng fixture này trên mã nền: bộ kiểm nền rc 0, `TAP_THU_HOI_RONG`, `canh_ancestry = 1`;
  gọi `KhoObject.tim(tree_S, PATH_POLICY_CLOSURE)` trên cùng tree ném `Chan` mã 12. Ca B1b trên nền đỏ vì receipt v1
  thiếu `quan_he_S_H` — đúng màu "chưa làm"; rc nền 0 là bất biến phải giữ.
- B6: review lượt 1 đo trên mã nền: hai gốc rời ⇒ rc 12 *"S không phải tổ tiên của H"*, `git merge-base --all` rc 1.
  Ca B6 trên nền đỏ vì thiếu nhãn `KHONG_CO_MERGE_BASE` — đúng màu "chưa làm".
- B2, B3, B3b, B5, B7, B8a, B9: trên nền đều rc 12 với *"không phải tổ tiên"*, thiếu nhãn hoặc sai rc so với kỳ vọng
  ⇒ đỏ đúng màu (đọc từ mã; phải chạy để xác nhận ngay sau khi viết fixture, trước khi sửa bộ kiểm).
- B12: `ca_tinh` hiện có xanh trên nền với fixture v1; răng mới nằm ở `amb-m12b`.
- B13: chưa chạy toàn bộ suite trên nền ở phiên này; số ca nền lấy từ CI của base khi cấp lease.

### 5.1 Kho ID đóng băng

Danh tính của một ca là **hậu tố tên** dưới đây, không phải số thứ tự. Trong `ops/lease_publish_test.py` mọi ca đăng ký
bằng decorator `@ca` vào danh sách `CA` (`CA` ở dòng 72, hàm `ca` ở dòng 79–81). Đo 01:14Z 07-11-2026 trên `origin/master` `9607e3eb` bằng AST
(hàm có decorator `ca`): **285** ca, 285 tên duy nhất, số lớn nhất `t237`. Tên có dạng `t<số>[chữ]_…`: 280 tên khớp
`t[0-9]+_`, 5 tên có hậu tố chữ sau số (`t02b_…`, `t02c_…`, `t02d_…`, `t55a_…`, `t55b_…`). Đếm ca thì đếm `CA`, không
đếm theo mẫu tên. Executor chọn số kế tiếp còn trống trên base của lease, giữ nguyên hậu tố. Mỗi hậu tố phải khớp
**đúng một** hàm; không khớp hoặc khớp hai ⇒ runner đỏ. Mỗi đột biến có ID riêng, đăng ký vào bảng đột biến sẵn có
của tệp test tương ứng.

| ca | tệp | hậu tố / tên ca | ID đột biến | nền |
|---|---|---|---|---|
| B1 | `ops/lease_publish_test.py` | `_amb01_to_tien_giu_nguyen` | `amb-m01-luon-di-merge-base` | cả hai |
| B1b | `ops/lease_publish_test.py` | `_amb01b_to_tien_khong_doc_vung_S` | `amb-m13-luon-doc-vung-S` | cả hai |
| B2 | `ops/lease_publish_test.py` | `_amb02_merge_base_vung_bang_nhau` | `amb-m02-bat-lai-to-tien` | cả hai |
| B3 | `ops/lease_publish_test.py` | `_amb03_policy_lech_sau_merge_base` | `amb-m03-bo-cong-so-vung` | cả hai |
| B3b | `ops/lease_publish_test.py` | `_amb03b_thu_hoi_moi_tren_master` | `amb-m03-bo-cong-so-vung` (cùng đột biến, ca đích thứ hai) | cả hai |
| B4 | `ops/lease_publish_test.py` | `_amb04_append_only_qua_merge_base` | `amb-m04-bo-append-only` | cả hai |
| B5 | `ops/lease_publish_test.py` | `_amb05_criss_cross_mot_base_lech` | `amb-m05-chi-so-base-dau` | cả hai |
| B6 | `ops/lease_publish_test.py` | `_amb06_khong_chung_goc` | `amb-m06-rong-la-dat` | cả hai |
| B7 | `ops/lease_publish_test.py` | `_amb07_vuot_ngan_sach_merge_base` | `amb-m07-nuot-vuot-ngan-sach` | cả hai |
| B8a | `ops/lease_publish_test.py` | `_amb08a_replace_khong_doi_merge_base` | `amb-m08-git-merge-base-thay-bo-doc` | cả hai |
| B8b | `ops/lease_publish_test.py` | `_amb08b_bam_lech_chi_tren_nhanh_S` | `amb-m14-duyet-merge-base-khong-bam-lai` | cả hai |
| B9 | `ops/lease_publish_test.py` | `_amb09_vuot_ngan_sach_khi_xet_to_tien` | `amb-m09-vuot-ngan-sach-thanh-khong-to-tien` | cả hai |
| B10 | `ops/lease_publish_test.py` | `_amb10_chu_thich_workflow_adr0066` | `amb-m10-ghi-lai-cau-cu` | cả hai |
| t133 | `ops/lease_publish_test.py` | tên hiện có, ca con "S không tổ tiên H" đổi kỳ vọng (mục tiêu 5) | `amb-m02-bat-lai-to-tien` | cả hai |
| B11 | `.claude/dev/doc_receipt_thu_hoi_test.py` | ca bảng `v2_to_tien`, `v2_merge_base`, `v2_thieu_merge_bases`, `v2_thua_khoa`, `v2_to_tien_base_khac_S`, `v2_merge_base_canh_so`, `v2_to_tien_co_vung`, `v2_merge_base_vung_null`, `v2_vung_hai_phan_tu`, `schema_3`; ca v1 hiện có giữ nguyên | `amb-m11-bo-tap-khoa-v2` | cả hai |
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
   `9607e3eb`), và review lượt 1 chạy được bộ kiểm nền trên Windows của chủ kho với một fixture đồ thị; nên không giả
   định trước là ca nào không chạy được.
2. **Đóng băng tập bắt buộc** và đăng lên #1266 **trước** lượt ứng viên. Tập ấy gồm:
   - **luôn có**: toàn bộ `doc_receipt_thu_hoi_test.py` (gồm B11, B12) và `_amb10_chu_thich_workflow_adr0066`;
   - **có điều kiện**: t133 và các ca `_amb01`…`_amb09` (gồm `_amb01b`, `_amb03b`, `_amb08a`, `_amb08b`) — vào tập
     bắt buộc nếu t133 chạy native được ở bước 1; ca nào loại ra phải kèm lý do **đo được** ở bước 1 (lệnh, output),
     không kèm lý do suy từ tài liệu.

   Sau khi đã đăng, tập bắt buộc chỉ được **thêm** ca, không được bớt.
3. **Runner tập trung** là một script nằm ngoài kho (không thuộc write set); sha256 của script ghi vào JSON kết quả.
   Nó so mã nền với mã ứng viên bằng **cùng một tệp test của H**:
   - Dựng hai clone dùng một lần, trong **cùng một lệnh**, ngoài checkout nguồn: `nen` ở base SHA và `ung_vien` ở H.
     Checkout nguồn không bị đụng.
   - **Lớp phủ:** chép đúng hai tệp test tại H (`ops/lease_publish_test.py`, `.claude/dev/doc_receipt_thu_hoi_test.py`)
     vào cùng đường dẫn trong `nen`, ghi OID blob của từng tệp (`git rev-parse H:<path>`). Vì tệp test nạp mã sản phẩm
     từ chính thư mục của nó (`SCRIPT = HERE / "lease_publish.py"`, dòng 29–30; `MODUN = GOC / "doc_receipt_thu_hoi.py"`,
     dòng 22–23; đo 07-11-2026 trên `9607e3eb`), test của H chạy với mã sản phẩm của base.
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
   quả (M3 a). Ca bắt buộc bị `skipped`/`not_run` ⇒ không xanh.
5. Tiến trình test không được thấy credential LIVE: `TL_TOKEN`, `TL_WEBAPP`, `TL_MASTER_KEY`,
   `TL_AGENT_CREDS_FILEID` và các biến Drive/GAS/NLM khác phải vắng. Runner kiểm sự vắng mặt bằng giá trị đúng/sai,
   không in giá trị.

## 7. hinh_dang_ke_thua

Chép từ đặc tả #1179 r1 §7 (nhánh `claude/spec-1179-c1a1b`, commit `7cfb4d7`) và quyết định chủ kho ở #1179 lúc
07:58Z 06-11-2026:

| lớp | số đếm | nguồn | chốt ở packet này |
|---|---|---|---|
| `phan-loai-vang-va-khong-do-duoc` | **4** (đã chạm chốt dừng ở #1179) | #1179 r1 lượt 1 F4 | bảng đóng ở mục 3; ca B6, B7, B9; câu cấm đổi lỗi đọc vùng thành bản đồ rỗng |
| `mo-rong-module-pha-hop-dong-json-thuan` | 3 | #1179 review draft0–2 | mục tiêu 7 giữ thuần JSON; ca B12 (`ca_tinh` có fixture v2) |
| `nguon-duoc-tin-ma-chua-xac-minh` | 7 (chuỗi thu hồi) | spec C1a1a r5 §6 | merge-base chỉ tính bằng bộ đọc có băm; ca B8a, B8b |

Review lượt 1 không ghi biểu hiện mới nào của ba lớp này, và cảnh báo: chữa F01 bằng cách coi lỗi đọc vùng là vùng
rỗng sẽ là biểu hiện mới của lớp thứ nhất. r2 chữa F01 bằng cách **không đọc** vùng ở chế độ `to_tien` (mục tiêu 3),
còn ở chế độ `merge_base` lỗi đọc vẫn ⇒ 12. Một biểu hiện mới của **bất kỳ** lớp nào trên ở bất kỳ lượt review nào
(đặc tả hay PR thi công) ⇒ DỪNG, Review Rescue Checkpoint (`ADR-0037`), báo chủ kho; không vá tiếp theo chỗ bị chỉ.

## 8. Review và ngân sách đóng

**Review đặc tả, trước khi chủ kho duyệt băm:** review độc lập của chính đặc tả này (Codex, ≤ 2 lời gọi, tính trên PR
đưa đặc tả vào kho, chung cho A và B). Finding P0–P2 ⇒ sửa đặc tả và tính băm mới trước khi duyệt. Lịch sử và cách đếm
lượt 0: mục 6 của đặc tả A r2. Review r2 chỉ chạy khi chủ kho cho phép.

**Review mã:** reviewer Codex độc lập, phiên riêng; trần 10 lời gọi theo dòng khai `ADR-0055` ở đầu tệp, đếm
**trước** mỗi lời gọi. Ngân sách mềm 4 lời gọi; hai lượt liên tiếp chưa approve ⇒ Review Rescue Checkpoint.
Reviewer **chạy** các ca và **đột biến bản vá** để đo răng; hướng thử cần soạn nội dung nhạy cảm thì mô tả bằng lời
cho phiên điều phối viết. Human audit theo `human_exact_head_audit.v1` (`ADR-0063`) trên exact head trước merge.

**Ngân sách đóng của PR mã** (đề xuất trong đặc tả; chủ kho chốt khi duyệt băm):

| hạng mục | trần | ghi chú |
|---|---|---|
| Lượt CI Ubuntu trên PR (head hoặc attempt) | 2 | rerun cũng tính; khớp `ADR-0060` M5 (một lần push chính) |
| Lượt `ci-dot-bien-du.yml` đầy đủ | 1 | lượt thứ 2 chỉ khi head đổi sau rework, cần checkpoint chủ kho |
| Lượt Windows native tập trung | 2 | mỗi lượt gồm nền và ứng viên trong một lệnh; tổng ≤ 60 phút |
| Phiên executor | 2 | checkpoint chủ kho nếu một phiên chạy quá 120 phút chủ động mà chưa có H |
| Lời gọi Codex review mã | 10 | mềm 4, như trên |

Không trong packet này: gắn nhãn `windows` lên PR; gọi tay `ci.yml` (cả hai `runner_set` đều có Windows); Windows
CI; full mutant trên Windows; mua credits. Hết một trần, hoặc không biết mức đã dùng ⇒ dừng ở checkpoint chủ kho;
không vay ngân sách của packet khác.

## 9. chua_do_duoc

- Kết quả `ai-dang-giu` (mục 1) đúng tới lúc đo trong ngày 06-11-2026; nó cũ đi theo từng nhánh mới, nên người cấp
  lease phải đo lại cả năm đường dẫn.
- Ca nào của t129/t133/t137/t151 chạy được trên Windows native: chưa đo (mục 6 bước 1).
- Runner tập trung (mục 6 bước 3): chưa dựng, chưa chạy lần nào; lớp phủ chưa được thử trên một ca thật.
- Các trần ở mục 8 là đề xuất; chưa có số đo mức dùng thực của một packet cỡ này để biện hộ từng con số.
- Hiệu năng thật của phép tính merge-base trên kho này (B17): mới có số đo duyệt toàn lịch sử master của #1179,
  chưa đo phép giao hai phía.
- Canary B18: chỉ đo được sau land.
- Số dòng thực tế: mới là ước lượng (khối `nang_tran`); trần 700 là đề xuất của r2, chưa được chủ kho chốt.

## 10. Thay đổi so với r1

| nguồn | thay đổi |
|---|---|
| F01 `receipt-moi-lam-doi-nhanh-cu` (P2) | `vung_tai_S = null` ở chế độ `to_tien`; hàm vùng chỉ gọi ở chế độ `merge_base` (mục tiêu 3, 4); bất biến tương thích; validator theo chế độ (mục tiêu 7); ca B1b và đột biến `amb-m13` dùng đúng fixture của review |
| F02 `dem-ca-bang-mau-ten` (P2) | 285 ca đếm theo `CA` bằng AST, kèm 5 tên có hậu tố chữ (mục 5.1); runner nói 285 |
| F03 `nghiem-thu-do-nham-chot` (P2) | B3b có đột biến `amb-m03` (đổi 12 thành 8); B6 đòi nhãn `KHONG_CO_MERGE_BASE` nên đỏ trên nền; bỏ "graft hoặc `refs/replace` ⇒ 12" khỏi bảng mục 3 vì bộ đọc vốn bỏ qua chúng; B8 tách thành B8a (replace, so với `git merge-base`) và B8b (băm lệch chỉ trên nhánh S, chứng minh đã qua bước S→H) |
| F04 `runner-nen-thieu-test-moi` (P2) | mục 6 bước 3: hai clone dùng một lần, lớp phủ tệp test của H lên clone nền, kiểm trạng thái chính xác, phân loại lỗi trên nền |
| F05 `phep-khop-khong-phu-menh-de` (P2) | câu mới của B10 đóng băng nguyên văn ở mục tiêu 6; B10 thêm đột biến lượng từ và hậu tố; vế âm dùng cụm lõi |
| F06 `canary-thieu-dieu-kien-chon` (P2) | B17/B18 chọn PR theo bốn tiền đề đo độc lập; PR không thoả là từ chối đúng luật, không tính đỏ |
| F07 `dem-sai-ngoai-le-closure` (P2) | mục 2: 3/179 có khai báo, 0 còn hiệu lực, kèm lệnh |
| F08 `moc-hieu-luc-khong-thong-nhat` (P3) | mục 0: luật có hiệu lực từ land B |
| ghi chú review: chốt cố định đếm khoá | mục tiêu 5 nêu t138 dòng 7061 (8 thành 9) và cách tìm đủ |
| ghi chú review: B12 ba từ chưa chứng minh thuần JSON | B12 dùng `ca_tinh` với fixture v2 và đột biến `amb-m12b` |
| ghi chú review: lý do Windows B:198–199 đã cũ | mục 6 bỏ lý do suy từ tài liệu, đòi lý do đo được |
| thêm ca | `nang_tran` đề xuất 700 dòng (r1: 600), chờ chủ kho chốt |
