tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# LEASE-TRUONG-KHAI-NGHIA r1 — `heartbeat_at` là lời khai, hạn nào có cổng, `reviewed_sha_required` là mỏ neo xuất phát

- packet_id: LEASE-TRUONG-KHAI-NGHIA; revision: 1;

| trường | giá trị |
|---|---|
| `packet_issue` | #646 |
| `nguon_cap_viec` | Issue #646 (ghi hộ chủ kho 26-09-2026), mục 2 và mục 3 của bảng "Phạm vi đề xuất". Chủ kho duyệt hướng xử lý trong phiên điều phối 18-11-2026: chỉ sửa văn bản protocol, không thêm cổng. Với mục 2, hướng được duyệt NGƯỢC với đề xuất gốc của #646: cho phép `reviewed_sha_required` bằng base, không từ chối nó. Mục 4 của #646 đã lỗi thời (#643/#705 thay). |
| `review_class` | `sensitive`: `docs/PROTOCOL_DA_PHIEN.md` không có trong `_BANG_LOP` (`ops/lease_publish.py:59–67`, bảng chỉ có bảy tiền tố, đều `sensitive`), nên `_tinh_lop_tu_write_set` (`ops/lease_publish.py:376`) rơi về mặc định fail-closed `sensitive`. Đo 2026-11-18T04:48:54Z bằng cách nạp đúng tệp ấy của `origin/master` và gọi `_tinh_lop_tu_write_set(["docs/PROTOCOL_DA_PHIEN.md"])` ⇒ `sensitive`. Đối chiếu lại bằng `lease_publish check` khi cấp lease. |
| `base` | `641108cb997872b0ef2a277ea9c8faf8b82532bb` (`origin/master` lúc soạn, đo 2026-11-18T04:47:54Z); lease ghi OID base thật lúc cấp. |

## 0. Hiện trạng (đo 2026-11-18T04:47Z–04:58Z trên `641108c`, Linux, clone không shallow)

Số dòng dưới đây là của blob trên base và trôi khi tệp đổi. Vì vậy văn bản protocol mới dẫn TỆP và TÊN HÀM/LỆNH, không dẫn
số dòng (L5: neo vào bất biến).

- `docs/PROTOCOL_DA_PHIEN.md` §4 (dòng 241): khối YAML lease ở dòng 260–276 (17 dòng, tính cả hai rào; sha256 của khối kể cả
  dòng cuối `` ``` `` và ký tự xuống dòng sau nó: `28fe56a370bf264bdc4604c54374f5700de528171794faefff803a37f2e1df68`) liệt kê
  `heartbeat_at: <timestamp>` (dòng 273) và `lease_until: <timestamp>` (dòng 274). Văn xuôi ngay sau khối (từ dòng 278) không
  nói trường nào có cổng đọc. Câu sẵn có ở dòng 290–291 đặt `lease_until` làm hạn tuyệt đối. Cả tệp có 0 dòng chứa
  `lease_expires_at_utc` và 0 dòng chứa `reviewed_sha_required`.
- Bảng §20 (dòng 1537) ghi `ADR-0056` ở cột cổng: **0 cổng**, "không có controller ngoài, phiên điều phối áp tay". Ngưỡng
  360 phút chỉ áp cho lease mới cấp sau mốc kích hoạt `ADR-0056` (§4 dòng 286–289).
- `heartbeat_at`: đếm bằng `git grep -n -Fw heartbeat_at`. Trên sáu vị trí cổng mà §20 liệt kê (L6(e)), mỗi tệp 0 hit:
  `ops/lease_publish.py`, `.claude/dev/packet_loop.py`, `.claude/dev/launcher.py`, `.claude/dev/gate_lifecycle.py`,
  `.github/workflows/ci.yml`, `.github/workflows/ops-publish-lease.yml`. Trên `':(glob).claude/dev/*.py' ':(glob)ops/*.py'`
  có đúng 1 hit, là fixture `.claude/dev/packet_loop_test.py:7809` (trong `case_pl_m6_state_v1`). Phép đo này không phủ toàn
  kho. Ngoài phạm vi ấy, tên trường còn xuất hiện trong script đo bằng chứng của reviewer (`ops/reviews/pr468-*`), trong tài
  liệu và trong hiện vật lease/land. Không chỗ nào trong số đó là cổng. Kết luận chỉ đúng cho snapshot đã đo: trong kho,
  `heartbeat_at` là lời khai và không cổng nào đọc trực tiếp trường này.
- `lease_expires_at_utc` có cổng, nhưng có điều kiện gọi:
  - Trường thuộc `BAT_BUOC` (`ops/lease_publish.py:292–298`).
  - `kiem()` (`ops/lease_publish.py:1028`) đọc trường qua `_doc_han` (dòng 459–472). Khi chốt hạn bật (`bo_qua_han` mặc định
    `False`), nó chặn `rc=8` nếu hạn đã qua (dòng 1125–1131).
  - `_phan_loai_lease` (dòng 783) dùng trường để phân `CÒN_HẠN`/`HẾT_HẠN` cho `ai-dang-giu`.
  - Hai đường bỏ riêng chốt hạn. `kiem_github` (dòng 1246) gọi `kiem(..., bo_qua_han=True)` ở dòng 1299, cho nhánh lease đã
    đăng (idempotent `rc=9`). `kiem_lease` của `ops/ci_duong_nhanh.py` (dòng 689) đọc trường ở dòng 713 và chạy
    `kiem(bo_qua_han=True)` cho lease lịch sử đã hết hạn (dòng 715–717).
  - `.claude/dev/packet_loop.py` cũng đọc trường ở `_verify_lease_ref` (dòng 2784) và trên đường WP1174
    (`_1174_owner_policy` dòng 4502, `_1174_resolve_snapshot` dòng 4625/4656, `_1174_source_resolve` dòng 6286).
- `lease_until`: chỉ một cổng đọc là `cmd_kiem_dong_wp` (`.claude/dev/packet_loop.py:3617`), ở điều kiện D4 (dòng 3646, 3651).
  Lease truyền qua `--lease` phải có `lease_until` dạng `%Y-%m-%dT%H:%M:%SZ` và **đã qua**, cùng `lease_id`, packet và
  generation khớp biên bản. Nếu không, D4 thiếu và WP không đóng được; parse hỏng thì `het = False`, nên D4 cũng thiếu. Tức
  trong mã, `lease_until` là điều kiện ĐÓNG WP, không phải chốt dừng thi công. `ops/lease_publish.py` không đọc trường này
  (0 hit).
- `reviewed_sha_required`: `ops/lease_publish.py` đòi trường có mặt (`BAT_BUOC`) và đúng dạng 40 hex thường sau `strip()`
  (`kiem()`, dòng 1104–1109). Dòng 2579 chỉ in trường vào biên nhận. Không có phép so trường này với `base_sha`, với head PR
  hay với một git object. `.claude/dev/packet_loop.py` không đọc trường này (0 hit). Head chính xác do hai chỗ khác đo:
  - `cmd_kiem_merge` (`.claude/dev/packet_loop.py:3506`):
    - K0 (`k0`, dòng 3517–3522) đòi `--head` bằng `refs/pull/<pr>/head` qua `ls-remote` tại lúc gọi.
    - K3 (`_doc_connector(..., h)`, dòng 3602) ràng buộc review connector với cùng repo/PR/head.
    - K4 (`k4`, dòng 3537–3553) có hai nhánh trên cùng head: `run.json` của review offline có `head == h`, hoặc human audit
      qua `_human_merge` (dòng 3441).
  - `cmd_record_review` (`.claude/dev/packet_loop.py:1180`): `--reviewed-sha` bắt buộc, đúng 40 hex, và phải bằng
    `reviewing_head_sha` của state (dòng 1211–1221). `transition` ghi `reviewing_head_sha` từ `--head-sha` (dòng 1330).
- Quy ước hiện hành, đo 2026-11-18T04:49:21Z bằng `git archive origin/master ops/leases`; đơn vị là TỆP lease `.yaml`:
  - Có 175 tệp. Cả 175 có `reviewed_sha_required` và `lease_expires_at_utc`.
  - So `reviewed_sha_required` với `base_sha`: 58 tệp bằng, 86 tệp khác, 31 tệp không có trường `base_sha`. Con số 58 chỉ
    chứng minh quan hệ bằng nhau có xảy ra. Điều kiện "khi chưa có head ứng viên" là quy ước do đặc tả này chọn, theo hướng
    chủ kho duyệt.
  - 29/175 tệp có `heartbeat_at`, 29/175 có `lease_until`. Cả 29 tệp có `lease_until` ghi cùng giá trị với
    `lease_expires_at_utc` (đo 04:57Z).
- Write set không giao lease nào còn hiệu lực. `python ops/lease_publish.py ai-dang-giu docs/PROTOCOL_DA_PHIEN.md` cho
  `NGƯỜI_GIỮ 0`, rc 0 (2026-11-18T04:51:17Z). So tập ref `ls-remote --heads` với `for-each-ref refs/remotes/origin`
  (04:51:22Z): máy chủ có 306 nhánh, thiếu cục bộ 0, thừa cục bộ 1. Reviewer lượt 1 không đo lại phép này (không có mạng).
- `doc-claims-check` có quét tệp này: `_DOC_CLAIMS_DEFAULT_PATHS` gồm `docs` (`scripts/tl_core/workflow.py:817`), và tệp không
  thuộc `_DOC_CLAIMS_HISTORICAL`. Trên base, `python scripts/tl.py doc-claims-check --strict --json` cho rc 0, `ok: true`,
  `flags: 0`, quét 131 tệp (04:49:45Z). Tệp này có đúng 2 advisory `PATH_MISSING_MIEN_TRU` (dòng 324, 325). Miễn trừ L1 khoá
  theo cặp (tệp, đường dẫn) (`_DOC_CLAIMS_MIEN_TRU_L1`, dòng 1143), nên một đường dẫn mới không tồn tại sẽ thành cờ
  `PATH_MISSING`. Giới hạn đã đo: L1 **không quét trong khối mã có rào**. Chèn `` `ops/khong_ton_tai_dot_bien.py` `` vào trong
  khối YAML §4 của bản sao base thì không có cờ; chèn ngay sau rào đóng thì có cờ `PATH_MISSING` ở dòng 278, rc 2.
- `doctrine-scan --root .` rc 0 ("đã quét 12 tệp, 0 chỗ chép doctrine") và `adr-song --root .` rc 0 ("66 ADR trên đĩa, 66 dòng
  trong §20"), đo 04:51:29Z. `doctrine-scan` quét adapter và dùng protocol làm nguồn đối chiếu. Hai ca phản chứng có sẵn:
  `case_doctrine_scan_chep_tron_5_1_bi_chan` (`.claude/dev/packet_loop_test.py:1576`, đăng ký dòng 3122) và
  `case_adr_song_thieu_dong_thi_do` (dòng 2904, đăng ký dòng 3546).
- Bản thử N5 (allowlist) trên bản sao, xong lúc 05:37Z: bản thử H là base chèn đúng khối 14 dòng của §3 (numstat `14	0`).
  Ma trận 31 ca, cả 31 ra đúng rc kỳ vọng:
  - rc 0: H đúng khối; và ca giới hạn "câu thêm ở §5" (N5 không phủ, nhưng N1 đỏ: đếm dòng ra `16 0`).
  - rc 1, lệch byte vùng đích: base (0 byte); H ngắt 60 cột; gộp thành hai đoạn; ba đột biến đảo nghĩa (mệnh đề 1, 3, 6); CRLF
    trong vùng; dời khối ra cuối tệp hay sang §5 (vùng 0 byte); bọc rào; thụt lề 4; comment HTML giữa dòng; blockquote chứa
    rào; code span hai backtick; danh sách; bốn ca lượt 5 (thuộc tính HTML `<span title='…'>`, link reference definition,
    setext heading, ô tiêu đề bảng); ca lượt 5 ngắt dòng ngay trước `#646.`; thêm câu không tên trường trong vùng; thêm câu
    đảo nghĩa trong vùng; dòng trống thừa; khoảng trắng cuối dòng; câu thêm sát trước ``Lease `role: reviewer` ``.
  - rc 1, YAML: một byte `0D` trong khối YAML (lệch băm); CRLF toàn tệp (mất neo).
  - rc 1, đầu vào: `MD` rỗng; `MD` bị sửa (lệch `MD_SHA`).
  - Đột biến "bằng" → "chứa": 5 ca âm đổi sang rc 0, còn 26/31 (N5).
  - `pandoc --sandbox --wrap=none -f gfm` 3.1.3 trên riêng khối bảy đoạn: đúng 7 dòng `<p>…</p>`, 0 phần tử khác.
  - `doc-claims-check --path` trên bản thử: không có cờ nào trong vùng dòng 270–300.
- Bản thử N1 trên rig git tạm ngoài kho (xong lúc 09:00Z): base là blob `7aebad643e2f…` của `docs/PROTOCOL_DA_PHIEN.md` trên
  master (mode `100644`), tệp kỳ vọng dựng bằng `--ky-vong` trùng từng byte bản thử H. Ma trận và đột biến từng chốt ghi ở
  cột phải của N1; mọi ca ra đúng rc kỳ vọng. Ma trận N5 với script hiện hành: 31/31; đột biến "chứa": 26/31.
## 1. `write_set`

```
docs/PROTOCOL_DA_PHIEN.md
```

## 2. `ngoai_pham_vi`

- Không thêm, không sửa cổng nào. Không có cổng mới cưỡng chế `heartbeat_at`. Không có cổng mới so `reviewed_sha_required` với
  `base_sha` hay với head; đề xuất gốc của #646 mục 2 đã bị chủ kho bác ngày 18-11-2026. Không đổi ngữ nghĩa của D4,
  K0/K3/K4, `record-review`, `kiem()`, `kiem_github`, `kiem_lease` hay `_phan_loai_lease`.
- Không sửa khối YAML §4: giữ nguyên từng byte dòng 260–276 của base, kể cả hai rào. Văn bản mới là văn xuôi đặt sau rào
  đóng. Lý do: không đổi schema lease, và L1 của `doc-claims-check` không quét bên trong rào (§0).
- Không sửa câu sẵn có ở §4 về `lease_until` là hạn tuyệt đối. Không sửa `ADR-0056` hay bảng §20; dòng `ADR-0056` vẫn ghi
  "0 cổng".
- Không chép doctrine vào adapter (`.claude/skills/**`, `.agents/**`).
- #646 mục 4 (spec r2 cho `CI-SONG-SONG-REGISTRY-G5-MOT-LAN`): lỗi thời, #643/#705 đã thay.
- #646 mục 1 (cổng tiền-land neo exact head): không làm ở đây. K0 chứng minh head PR tại lúc gọi `kiem-merge`; K3/K4 ràng
  buộc bằng chứng review với head đó; `record-review` ràng buộc verdict với head trong state. Các phép ấy đủ để M3 dẫn đúng
  nơi đo exact head, nhưng chưa chứng minh lần gọi merge dùng chính head đã kiểm. Muốn bảo đảm đến thời điểm merge thì phải
  đặc tả và kiểm riêng đường land, kèm cơ chế từ chối khi head đổi. Đó là việc của packet khác và vượt write set tài liệu này.
- Lease không tự chết khi land: thuộc #488, như #646 đã ghi.

## 3. `muc_tieu`

Văn bản mới được CHỐT NGUYÊN VĂN, không do executor viết lại. Bảy mệnh đề dưới đây, mỗi mệnh đề MỘT đoạn nằm trọn trên
MỘT dòng (không ngắt dòng bên trong), hai đoạn liền nhau cách đúng một dòng trống. Không có câu dẫn, câu nối hay câu nào
khác. Mỗi tên hàm, lệnh hoặc tệp trong mệnh đề là đối tượng của N4.

Bảy mệnh đề, mỗi dòng một mệnh đề; sha256 của khối này (bảy dòng, mỗi dòng kết thúc bằng LF) là
`MD_SHA = 27c00e50f6aaa1d63482f7be1f9b894e3d985eeb3a875603d6ac11bff14c87a8`:

```
`heartbeat_at` là lời khai: trong kho không có cổng nào đọc trực tiếp trường này.
Ngưỡng thu hồi 360 phút cho lease mới thuộc hiệu lực `ADR-0056` do phiên điều phối áp tay, theo bảng §20.
Theo protocol, `lease_until` là hạn tuyệt đối; trong mã, chỉ `kiem-dong-wp` của `.claude/dev/packet_loop.py` đọc trường này, ở điều kiện D4: `lease_until` phải đã qua thì mới đóng được WP.
Khi kiểm lease để công bố với chốt hạn bật, `kiem()` của `ops/lease_publish.py` dùng `lease_expires_at_utc` để từ chối lease đã hết hạn; `ai-dang-giu` dùng cùng trường để phân loại hạn.
Đường kiểm idempotent (`kiem_github`) và đường kiểm lease lịch sử trong CI (`ops/ci_duong_nhanh.py`) bỏ riêng phép chặn hết hạn.
`reviewed_sha_required` là mỏ neo xuất phát, được phép bằng `base_sha` khi chưa có head ứng viên; `kiem()` chỉ đòi trường có mặt và đúng dạng 40 hex thường.
Exact head không đọc từ lease: `kiem-merge` neo head PR ở K0, kiểm review connector ở K3, và kiểm review offline hoặc human audit trên cùng head ở K4; `record-review` so `--reviewed-sha` với head đã ghi khi vào `reviewing`.
```

Cách chèn: trên base, sau dòng rào đóng ```` ``` ```` của khối YAML §4 là đúng một dòng trống, rồi tới dòng mở đầu bằng
``Lease `role: reviewer` ``. Chèn 14 dòng ngay sau dòng trống ấy: bảy dòng mệnh đề xen sáu dòng trống, rồi một dòng trống
trước ``Lease `role: reviewer` ``. Vùng đích là các byte từ đầu dòng ngay sau rào đóng YAML tới trước ký tự xuống dòng đứng
ngay trước ``Lease `role: reviewer` ``. Trên H, vùng ấy phải là đúng 1297 byte, bằng LF + bảy mệnh đề nối bằng `LF LF` + LF,
sha256 `VUNG_SHA = 6c4ec88cb1e15fd43556f6ed5e8304da613814b825a283e445d0ba33db8b8215`. Trên base vùng ấy rỗng (0 byte). Khối
14 dòng sẽ chèn, nguyên văn:

```
`heartbeat_at` là lời khai: trong kho không có cổng nào đọc trực tiếp trường này.

Ngưỡng thu hồi 360 phút cho lease mới thuộc hiệu lực `ADR-0056` do phiên điều phối áp tay, theo bảng §20.

Theo protocol, `lease_until` là hạn tuyệt đối; trong mã, chỉ `kiem-dong-wp` của `.claude/dev/packet_loop.py` đọc trường này, ở điều kiện D4: `lease_until` phải đã qua thì mới đóng được WP.

Khi kiểm lease để công bố với chốt hạn bật, `kiem()` của `ops/lease_publish.py` dùng `lease_expires_at_utc` để từ chối lease đã hết hạn; `ai-dang-giu` dùng cùng trường để phân loại hạn.

Đường kiểm idempotent (`kiem_github`) và đường kiểm lease lịch sử trong CI (`ops/ci_duong_nhanh.py`) bỏ riêng phép chặn hết hạn.

`reviewed_sha_required` là mỏ neo xuất phát, được phép bằng `base_sha` khi chưa có head ứng viên; `kiem()` chỉ đòi trường có mặt và đúng dạng 40 hex thường.

Exact head không đọc từ lease: `kiem-merge` neo head PR ở K0, kiểm review connector ở K3, và kiểm review offline hoặc human audit trên cùng head ở K4; `record-review` so `--reviewed-sha` với head đã ghi khi vào `reviewing`.

```

`pandoc --sandbox --wrap=none -f gfm -t html` 3.1.3 dựng riêng khối bảy đoạn này thành đúng bảy dòng `<p>…</p>`, không phần
tử nào khác (đo 05:37Z): đó là bằng chứng khối là văn xuôi cấp ngoài cùng.

**Đã bỏ cam kết "ngắt dòng tự do" của các lượt trước, và vì sao.** Năm lượt review liên tiếp (1–5) tìm ra cùng một hình dạng
lỗi: N5 dựa vào một danh sách CẤM các dạng Markdown không phải văn xuôi (rào, thụt lề, comment HTML, blockquote, code span,
rồi thuộc tính HTML, link reference definition, setext heading, ô tiêu đề bảng), và mỗi lượt có thêm một dạng lọt. Lượt 5
còn cho thấy danh sách cấm đỏ oan đúng ca ngắt dòng mà nó hứa cho phép (dòng bắt đầu bằng `#646.`). Danh sách cấm thua từ
thiết kế (CLAUDE.md, bài học "danh sách CẤM không bao giờ đủ"), nên N5 đảo thành danh sách CHO PHÉP gồm đúng một phần tử: khối
đã chốt, so từng byte. Giá phải trả: mọi cách ngắt dòng hay diễn đạt khác đều đỏ, và đó là chủ đích.

| # | mục tiêu | tệp |
|---|---|---|
| M1 | Mệnh đề 1–2: `heartbeat_at` là lời khai và không cổng nào trong kho đọc trực tiếp trường này. Ngưỡng 360 phút cho lease mới thuộc hiệu lực `ADR-0056`, do phiên điều phối áp tay theo §20. Không dùng chữ "cưỡng chế" cho trường này. | `docs/PROTOCOL_DA_PHIEN.md` |
| M2 | Mệnh đề 3–5, theo phạm vi: protocol vẫn coi `lease_until` là hạn tuyệt đối. Trong mã, chỉ D4 của `kiem-dong-wp` đọc `lease_until`, như điều kiện đóng WP. Khi chốt hạn bật, `kiem()` dùng `lease_expires_at_utc` để từ chối lease hết hạn, và `ai-dang-giu` phân loại hạn theo cùng trường. Đường idempotent và đường CI lịch sử bỏ riêng chốt hạn. Câu sẵn có "hết `lease_until` thì lease hết dù còn trong 6 giờ" giữ nguyên chữ. | `docs/PROTOCOL_DA_PHIEN.md` |
| M3 | Mệnh đề 6–7: `reviewed_sha_required` là mỏ neo xuất phát, được phép bằng `base_sha` khi chưa có head ứng viên (quy ước đặc tả chọn). `kiem()` chỉ đòi trường có mặt và đúng dạng 40 hex thường. Exact head do `kiem-merge` đo: K0 neo head PR; K3 kiểm review connector; K4 kiểm review offline hoặc human audit, cả hai trên cùng head. `record-review` so với head đã ghi khi vào `reviewing`. | `docs/PROTOCOL_DA_PHIEN.md` |

## 4. `nghiem_thu`

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| N1 | Script `n1.sh` dưới bảng, gọi `bash n1.sh <đường-kho> <base> <H> <script-N5>`. rc 0: H đúng; rc 1: nội dung sai; rc 2: **lỗi môi trường** (không mở được kho, object thiếu, thiếu python3, đối số sai), tức KHÔNG ĐO ĐƯỢC, không phải kết luận về nội dung. Chốt môi trường: mọi lệnh git chạy dạng `git -C <đường-kho>`, sau khi `unset` `GIT_DIR` `GIT_WORK_TREE` `GIT_OBJECT_DIRECTORY` `GIT_ALTERNATE_OBJECT_DIRECTORIES` `GIT_INDEX_FILE` `GIT_COMMON_DIR` `GIT_NAMESPACE` `GIT_REPLACE_REF_BASE` `GIT_GRAFT_FILE` `GIT_SHALLOW_FILE` `GIT_CONFIG` `GIT_CONFIG_PARAMETERS` `GIT_CONFIG_COUNT`, và với `GIT_NO_REPLACE_OBJECTS=1` `GIT_CONFIG_NOSYSTEM=1` `GIT_CONFIG_GLOBAL=/dev/null` `GIT_ATTR_NOSYSTEM=1` `-c diff.ignoreSubmodules=none`. `git rev-parse --git-dir` phải chạy được trước mọi phép đo. Chốt nội dung: (a) `B`, `H` là OID 40 hex và `git cat-file -t` cho `commit`; dòng `tree` của object commit H thô khớp `rev-parse H^{tree}`. (b) `git diff-tree -r --no-renames --ignore-submodules=none --raw --no-abbrev <base> H` in đúng một dòng `:100644 100644 <oid base> <oid H> M<TAB>docs/PROTOCOL_DA_PHIEN.md`. (c) Đếm dòng thêm/xoá bằng `difflib` trên byte hai blob trích qua `git cat-file blob`: đúng `14 0` (trong trần `ADR-0053`). (d) Blob H bằng `git hash-object --no-filters` của tệp kỳ vọng (`script-N5 --ky-vong` trên blob base). (e) Script N5 chạy trên đúng blob H vừa trích, tức N5 cũng đọc qua đường không replace. **Phạm vi độc lập môi trường chỉ đúng như đã đo** (cột phải): replace refs, config hệ thống/toàn cục, thuộc tính, `diff.*`, các biến `GIT_*` đã liệt kê. **Giả định tin cậy, không đóng:** config cục bộ và alternates trong `.git/objects/info` của kho đích do phiên kiểm tự dựng (clone mới); SHA-1 không va chạm, nên alternates không đổi được nội dung của một OID. Grafts chỉ đổi cha của commit, không đổi cây, nên không chạm phép so cây B với H. Trên base (H = base): rc 1 ở (b). | Rig git tạm ngoài kho (đo 08:59Z, base là blob `7aebad64…` của master), mọi ca đúng kỳ vọng. rc 0: H đúng; H đúng dưới `diff.ignoreSubmodules=all`, dưới `* -diff`, dưới `.git/info/grafts`, khi người gọi đặt `GIT_DIR`, `GIT_WORK_TREE`, `GIT_OBJECT_DIRECTORY` hay `GIT_ALTERNATE_OBJECT_DIRECTORIES` sai; H đúng khi kho có replace ref của object khác. rc 1: `chmod +x`; H = base; thêm tệp thứ hai; gitlink (cả dưới `diff.ignoreSubmodules=all`); thêm dòng ở §5 (cả dưới `* -diff`); sửa một dòng khác; chèn sai vị trí; CRLF toàn tệp; **`git replace H_bad H_đúng`** với H_bad thêm tệp ngoài write set (cả khi người gọi đặt `GIT_NO_REPLACE_OBJECTS=` rỗng); **`git replace` blob xấu bằng blob đúng**; H_bad dưới grafts; H là một tree. rc 2: `core.abbrev=bogus` trong config cục bộ; đường kho không tồn tại; OID không có trong kho. Đối chứng `n1.sh` lượt trước trên cùng rig: replace commit ⇒ rc 0 (xanh giả); `GIT_DIR` sai ⇒ rc 1 "base không có tệp" (kết luận nội dung sai); `GIT_OBJECT_DIRECTORY` sai ⇒ rc 1; `core.abbrev=bogus` ⇒ rc 1. Đột biến từng chốt: bỏ `GIT_NO_REPLACE_OBJECTS=1` ⇒ ca replace commit rc 0; bỏ `unset` ⇒ ca `GIT_DIR` sai thành rc 2 thay vì đo được; bỏ (b) ⇒ ca `chmod +x` và ca thêm tệp rc 0; bỏ đồng thời (c), (d), (e) ⇒ ca thêm dòng và ca chèn sai vị trí rc 0; bỏ đồng thời (d), (e) ⇒ ca chèn sai vị trí rc 0. **Không có răng độc lập** (khai thẳng, là lớp phòng thủ chồng): kiểm `--git-dir` (bỏ đi thì `cat-file -t` vẫn cho rc 2), kiểm kiểu commit (bỏ đi thì vẫn rc 1 ở bước sau), kiểm dòng `tree` thô (dưới replace, `cat-file` cũng trả object đã thay nên không bắt được; răng nằm ở `GIT_NO_REPLACE_OBJECTS`), và mỗi chốt trong (c), (d), (e) khi bỏ riêng lẻ. |
| N2 | `python .claude/dev/packet_loop.py doctrine-scan --root .` và `python .claude/dev/packet_loop.py adr-song --root .` cho rc 0 trên H, kèm dòng kết luận dương (`sạch`, và `N ADR … N dòng` với hai số bằng nhau). Cả hai xanh sẵn trên base (§0). | Phản chứng định danh, chạy trên bản sao thử của H, không commit: (a) chép một đoạn doctrine §5.1 của protocol vào một adapter thuộc tập quét ⇒ `doctrine-scan` rc khác 0; (b) bỏ một dòng ADR hiện hành khỏi bảng §20 ⇒ `adr-song` rc khác 0. Hai ca mẫu đã có: `case_doctrine_scan_chep_tron_5_1_bi_chan` và `case_adr_song_thieu_dong_thi_do` trong `.claude/dev/packet_loop_test.py`. Executor ghi lệnh, rc và dòng lỗi của cả hai phản chứng. |
| N3 | `python scripts/tl.py doc-claims-check --strict --json` trên H: rc 0, `ok: true`, `flags: 0`. Advisory của `docs/PROTOCOL_DA_PHIEN.md` vẫn đúng 2 `PATH_MISSING_MIEN_TRU` (số dòng được phép dịch theo số dòng thêm). Ghim `core.abbrev 7` trước khi chạy. Phải lấy exit code từ chính CLI, không từ lõi scanner. | Trên bản sao H, thêm vào đoạn văn mới (ngoài rào) một đường dẫn không tồn tại, ví dụ `` `ops/khong_ton_tai_dot_bien.py` `` ⇒ cờ `PATH_MISSING` ở đúng dòng ấy, rc 2. Đã chạy trên bản sao base (§0). Đột biến đặt trong rào thì KHÔNG đỏ, nên phải đặt ngoài rào. |
| N4 | Mỗi tên trong bảy mệnh đề được đối chiếu với đúng tệp trên H bằng `git grep -n -Fw` hoặc mẫu `-E` neo vào khai báo. Báo cáo ghi lệnh, số hit và exit code của từng phép. Số hit kỳ vọng, đo trên base 04:57Z: (i) `-Fw heartbeat_at` trên từng tệp trong sáu vị trí cổng §20 ⇒ 0 hit mỗi tệp (`rc=1`). (ii) `-Fw heartbeat_at` trên `':(glob).claude/dev/*.py' ':(glob)ops/*.py'` ⇒ đúng 1 hit, ở `.claude/dev/packet_loop_test.py`. (iii) Trong `ops/lease_publish.py`, mỗi mẫu sau 1 hit: `^BAT_BUOC = \(`, `^def kiem\(`, `^def kiem_github\(`, `^def _phan_loai_lease\(`, `add_parser\("ai-dang-giu"`; mẫu `-Fw lease_until` ⇒ 0 hit. Thêm các mẫu DƯƠNG neo vào câu lệnh đọc/kiểm trường, dùng `git grep -n -F -e '<chuỗi>'`, mỗi mẫu 1 hit: `han = _doc_han(lease["lease_expires_at_utc"])` (đọc hạn trong `kiem()`), `if not bo_qua_han and han <= datetime.now(timezone.utc):` (chốt hạn), `han = _doc_han(lease.get("lease_expires_at_utc"))` (`_phan_loai_lease`), `sha = str(lease["reviewed_sha_required"]).strip()` và `if not SHA40.match(sha):` (kiểm dạng), `kiem(lease, tep, goc, bo_qua_han=True)` (lời gọi thật của `kiem_github`). (iv) `ops/ci_duong_nhanh.py`: `^def kiem_lease\(` 1 hit; mẫu `-F`, mỗi mẫu 1 hit: `han = _han_lease(lease.get("lease_expires_at_utc"))`, `lenh = [sys.executable, "-B", "-c", MA_KIEM_HET_HAN, duong]`, và lời gọi thật trong chuỗi `MA_KIEM_HET_HAN`: `lp.kiem(lp._doc_yaml(sys.argv[1]), sys.argv[1], '.', bo_qua_han=True)`. Không đếm `bo_qua_han=True` trần: trên base nó ra 4 hit, gồm cả docstring và thông báo in. (v) Trong `.claude/dev/packet_loop.py`, mỗi mẫu sau 1 hit: `^def cmd_kiem_dong_wp\(`, `add_parser\("kiem-dong-wp"`, `D4 lease`, `str(ls.get("lease_until"))` (mẫu `-F`, câu đọc của D4), `^def cmd_kiem_merge\(`, `add_parser\("kiem-merge"`, `_dk\("K0 `, `_dk\("K3 `, `_dk\("K4 `, `^def _human_merge\(`, `^def cmd_record_review\(`, `add_parser\("record-review"`, `a\.reviewed_sha != st\["reviewing_head_sha"\]`; mẫu `-Fw reviewed_sha_required` ⇒ 0 hit. Khi mã đổi giữa base và lúc thi công, số hit lệch là lý do đi revision (§6), không phải lý do tự sửa mệnh đề. | Dẫn sai một tên ⇒ phép neo khai báo hoặc `-Fw` cho 0 hit, rc 1. Ví dụ `cmd_kiem_dong` (trên base, `-F` cho 2 hit, `rc=0`, tức xanh giả; `-Fw` cho `rc=1`), hay `BAT_BUOC_LEASE`. Một tên trong mệnh đề mà không có phép grep nào ⇒ reviewer đối chiếu danh sách và báo thiếu. Một vị trí cổng có hit `heartbeat_at` ⇒ mệnh đề 1 sai, đỏ. Gỡ câu đọc hạn hay câu kiểm dạng khỏi mã (bản sao) ⇒ mẫu dương tương ứng 0 hit, đỏ; mẫu trần `bo_qua_han=True` ở CI vẫn còn hit từ docstring nên không dùng được làm phản chứng. |
| N5 | Script tự chứa dưới bảng, một đối số là `docs/PROTOCOL_DA_PHIEN.md` của H, đọc ở dạng BYTES. (0) Bảy mệnh đề nhúng trong script phải đúng 7 dòng khác rỗng, sha256 bằng `MD_SHA`; khối dựng từ chúng phải có sha256 bằng `VUNG_SHA` (§3). (1) Định vị §4 (`## 4. ` tới `## 5. `), neo `Lease gồm:` + rào ```` ```yaml ````, cắt khối YAML từ rào mở tới hết dòng rào đóng, so sha256 trên bytes với băm base `28fe56a3…f2e1df68` (§0). (2) Cắt vùng đích như §3 định nghĩa; thiếu neo nào ⇒ đỏ. (3) Vùng đích phải BẰNG TỪNG BYTE khối đã chốt; khác một byte cũng đỏ. Đây là danh sách CHO PHÉP một phần tử, không còn danh sách cấm nào. Trên base: rc 1 (vùng 0 byte). | Ma trận 31 ca (đo 05:37Z, §0), 31/31 đúng kỳ vọng. Mọi biến thể của khối đều đỏ, kể cả biến thể giữ nghĩa (ngắt 60 cột, gộp thành hai đoạn): đó là chủ đích. Đột biến bắt buộc, chứng minh ca đang đo đúng allowlist: nới phép so từ "bằng" (`vung!=ky_vong`) thành "chứa" (`ky_vong not in vung`) ⇒ 5 ca âm đổi sang rc 0 (bọc rào, thêm câu không tên trường trong vùng, thêm câu đảo nghĩa trong vùng, dòng trống thừa, câu thêm sát trước ``Lease `role: reviewer` ``), tổng còn 26/31. |

Script đo N5 (đặt NGOÀI kho; `n5.py <H>` kiểm vùng đích, `n5.py --ky-vong <base> <ra>` dựng tệp kỳ vọng cho N1; bảy mệnh đề, `MD_SHA` và `VUNG_SHA` nhúng sẵn):

```
import sys,re,hashlib
BASE_YAML='28fe56a370bf264bdc4604c54374f5700de528171794faefff803a37f2e1df68'
MD=(
    '`heartbeat_at` là lời khai: trong kho không có cổng nào đọc trực tiếp trường này.',
    'Ngưỡng thu hồi 360 phút cho lease mới thuộc hiệu lực `ADR-0056` do phiên điều phối áp tay, theo bảng §20.',
    'Theo protocol, `lease_until` là hạn tuyệt đối; trong mã, chỉ `kiem-dong-wp` của `.claude/dev/packet_loop.py` đọc trường này, ở điều kiện D4: `lease_until` phải đã qua thì mới đóng được WP.',
    'Khi kiểm lease để công bố với chốt hạn bật, `kiem()` của `ops/lease_publish.py` dùng `lease_expires_at_utc` để từ chối lease đã hết hạn; `ai-dang-giu` dùng cùng trường để phân loại hạn.',
    'Đường kiểm idempotent (`kiem_github`) và đường kiểm lease lịch sử trong CI (`ops/ci_duong_nhanh.py`) bỏ riêng phép chặn hết hạn.',
    '`reviewed_sha_required` là mỏ neo xuất phát, được phép bằng `base_sha` khi chưa có head ứng viên; `kiem()` chỉ đòi trường có mặt và đúng dạng 40 hex thường.',
    'Exact head không đọc từ lease: `kiem-merge` neo head PR ở K0, kiểm review connector ở K3, và kiểm review offline hoặc human audit trên cùng head ở K4; `record-review` so `--reviewed-sha` với head đã ghi khi vào `reviewing`.',
)
MD_SHA='27c00e50f6aaa1d63482f7be1f9b894e3d985eeb3a875603d6ac11bff14c87a8'
VUNG_SHA='6c4ec88cb1e15fd43556f6ed5e8304da613814b825a283e445d0ba33db8b8215'
def chet(ly_do): print('DO:',ly_do); sys.exit(1)
if len(MD)!=7 or not all(m.strip() for m in MD) or hashlib.sha256(('\n'.join(MD)+'\n').encode()).hexdigest()!=MD_SHA:
    chet('bay menh de nhung trong script khong khop MD_SHA cua dac ta')
ky_vong=('\n'+'\n\n'.join(MD)+'\n').encode()
if hashlib.sha256(ky_vong).hexdigest()!=VUNG_SHA: chet('khoi chot dung tu MD khong khop VUNG_SHA cua dac ta')
# Hai cách gọi: `n5.py <H>` kiểm vùng đích của H; `n5.py --ky-vong <base> <ra>` ghi ra tệp kỳ vọng = base chèn khối (cho N1).
dung=len(sys.argv)==4 and sys.argv[1]=='--ky-vong'
if not (dung or len(sys.argv)==2): chet('cach goi: n5.py <H>  hoac  n5.py --ky-vong <base> <ra>')
b=open(sys.argv[2] if dung else sys.argv[1],'rb').read()
s4=b.find(b'\n## 4. '); s5=b.find(b'\n## 5. ')
if s4<0 or s5<s4: chet('khong dinh vi duoc §4/§5')
neo=b.find('Lease gồm:\n\n```yaml\n'.encode(),s4,s5)
if neo<0: chet('khong thay "Lease gồm:" + rao yaml trong §4')
y0=neo+len('Lease gồm:\n\n'.encode())
dong=b.find(b'\n```',y0+7)
if dong<0: chet('khong thay rao dong yaml')
y1=b.find(b'\n',dong+4)+1
h=hashlib.sha256(b[y0:y1]).hexdigest()
if h!=BASE_YAML: chet('khoi YAML lech byte: '+h)
r1=b.find('\nLease `role: reviewer`'.encode(),y1,s5)
if r1<0: chet('khong thay doan "Lease `role: reviewer`" trong §4 sau khoi YAML')
vung=b[y1:r1]
if dung:
    if vung!=b'': chet('base khong co vung dich rong: '+str(len(vung))+' byte')
    open(sys.argv[3],'wb').write(b[:y1]+ky_vong+b[y1:]); print('da_ghi_ky_vong',sys.argv[3]); sys.exit(0)
# ALLOWLIST: vùng đích phải BẰNG TỪNG BYTE khối đã chốt; mọi thứ khác đều đỏ.
if vung!=ky_vong: chet(f'vung dich lech khoi da chot: {len(vung)} byte, sha256 {hashlib.sha256(vung).hexdigest()}')
print('vung_dich_khop_khoi_chot',VUNG_SHA,'yaml_sha',h)
```

Script `n1.sh` (đặt NGOÀI kho; đối số đầu là đường tới kho, không phụ thuộc cwd):

```
#!/usr/bin/env bash
# N1: `bash n1.sh <đường-kho> <B> <H> <script-N5>`. rc 0: H = base + khối đã chốt, cùng mode, không gì khác.
# rc 1: nội dung sai. rc 2: LỖI MÔI TRƯỜNG (kho, git, python, đối số) — không kết luận gì về nội dung.
# Phạm vi độc lập môi trường ĐÃ ĐO: bỏ qua replace refs, config hệ thống/toàn cục, thuộc tính hệ thống, biến GIT_DIR/
# GIT_WORK_TREE/GIT_OBJECT_DIRECTORY/GIT_ALTERNATE_OBJECT_DIRECTORIES/GIT_INDEX_FILE/GIT_COMMON_DIR, diff.* và .gitattributes
# của kho. GIẢ ĐỊNH tin cậy, không đóng: kho đích (config cục bộ, alternates trong .git/objects/info) do chính phiên kiểm
# dựng, và SHA-1 không va chạm (cùng OID ⇒ cùng nội dung, nên alternates không đổi được nội dung theo OID).
set -u
[ $# -eq 4 ] || { echo "N1 MOI_TRUONG: can 4 doi so"; exit 2; }
R=$1; B=$2; H=$3; N5=$4; P=docs/PROTOCOL_DA_PHIEN.md
unset GIT_DIR GIT_WORK_TREE GIT_OBJECT_DIRECTORY GIT_ALTERNATE_OBJECT_DIRECTORIES GIT_INDEX_FILE GIT_COMMON_DIR \
      GIT_NAMESPACE GIT_REPLACE_REF_BASE GIT_GRAFT_FILE GIT_SHALLOW_FILE GIT_CONFIG GIT_CONFIG_PARAMETERS GIT_CONFIG_COUNT
export GIT_NO_REPLACE_OBJECTS=1 GIT_CONFIG_NOSYSTEM=1 GIT_CONFIG_GLOBAL=/dev/null GIT_ATTR_NOSYSTEM=1
T=$(mktemp -d) || { echo "N1 MOI_TRUONG: mktemp"; exit 2; }
do_(){ echo "N1 DO: $1"; rm -rf "$T"; exit 1; }
mt(){ echo "N1 MOI_TRUONG: $1"; rm -rf "$T"; exit 2; }
g(){ git -C "$R" -c diff.ignoreSubmodules=none -c core.quotePath=true "$@"; }
command -v python3 >/dev/null || mt "khong co python3"
gd=$(g rev-parse --git-dir 2>&1) || mt "khong mo duoc kho $R: $gd"
for x in "$B" "$H"; do
  [[ $x =~ ^[0-9a-f]{40}$ ]] || mt "B/H phai la OID 40 hex: $x"
  ty=$(g cat-file -t "$x" 2>&1) || mt "khong doc duoc object $x: $ty"
  [ "$ty" = commit ] || do_ "$x la $ty, khong phai commit"
done
# Cây của H đọc thẳng từ object commit thô, đối chiếu với rev-parse (chốt dự phòng cho replace).
tr=$(g cat-file commit "$H" | sed -n '1s/^tree //p') || mt "khong doc duoc commit H"
[ "$tr" = "$(g rev-parse "$H^{tree}")" ] || do_ "cay H lech giua object tho va rev-parse"
oB=$(g rev-parse --verify -q "$B:$P") || do_ "base khong co $P"
oH=$(g rev-parse --verify -q "$H:$P") || do_ "H khong co $P"
raw=$(g diff-tree -r --no-renames --ignore-submodules=none --raw --no-abbrev "$B" "$H") || mt "diff-tree loi"
[ "$raw" = "$(printf ':100644 100644 %s %s M\t%s' "$oB" "$oH" "$P")" ] \
  || do_ "diff-tree khac dung mot dong M 100644->100644 cho $P: $(printf '%s' "$raw" | head -2 | tr '\t\n' ' |')"
g cat-file blob "$oB" > "$T/base.md" && g cat-file blob "$oH" > "$T/h.md" || mt "khong doc duoc blob"
dem=$(python3 -I -c '
import sys,difflib
a=open(sys.argv[1],"rb").read().split(b"\n"); b=open(sys.argv[2],"rb").read().split(b"\n")
t=x=0
for op,i1,i2,j1,j2 in difflib.SequenceMatcher(None,a,b,autojunk=False).get_opcodes():
    if op!="equal": x+=i2-i1; t+=j2-j1
print(t,x)' "$T/base.md" "$T/h.md") || mt "khong dem duoc dong"
[ "$dem" = "14 0" ] || do_ "dong them/xoa = $dem, can 14 0"
python3 -I "$N5" --ky-vong "$T/base.md" "$T/kv.md" >/dev/null || do_ "khong dung duoc blob ky vong tu base"
kv=$(g hash-object --no-filters "$T/kv.md") || mt "hash-object loi"
[ "$oH" = "$kv" ] || do_ "blob H $oH khac blob ky vong $kv"
# N5 chạy trên đúng blob H vừa trích (cùng đường trích không replace).
python3 -I "$N5" "$T/h.md" >/dev/null || do_ "N5 do tren blob H"
echo "N1 DAT: blob $oH, mode 100644, them/xoa $dem"; rm -rf "$T"
```

## 5. `pham_vi_e`

Không chạm E4, không chạm E5. Văn bản chỉ mô tả hành vi của các cổng hiện có; không đổi quyền, không đổi cổng.

## 6. `luat_dung`

- Trần lời gọi Codex theo dòng khai `ADR-0055`. Chạm trần ⇒ Review Rescue Checkpoint. Xin tăng trần là **E2**, mang theo
  những gì `ADR-0067` đòi: lượng đã dùng, phần quyền còn thiếu, mục đích.
- N5 chỉ khoá vùng đích. Phần còn lại của tệp do N1 khoá (đúng một dòng `M` trong `diff-tree`, đếm dòng `14 0`, blob bằng blob kỳ vọng), nên câu thêm ở chỗ khác cũng đỏ. N1 và N5
  không chứng minh bảy mệnh đề ĐÚNG với mã; việc ấy là của N4 và của reviewer. Reviewer đọc diff, xác nhận bằng chữ trong
  verdict rằng diff đúng là khối 14 dòng ở §3 và không có gì khác; có thì là finding, executor đi revision.
- Dừng triển khai và đi revision đặc tả khi: một mệnh đề ở §3 không còn được mã trên exact base của lease chống đỡ (số hit N4
  lệch, hoặc một cổng đã đổi hành vi so với §0); cần thêm khẳng định về mã ngoài bảy mệnh đề; hoặc cần sửa ngoài write set.
  Trước khi viết, executor đo lại mọi dòng §0 trên exact base của lease.
- Đặc tả không thuộc Mission, nên chờ chủ kho duyệt băm theo `ADR-0067`: **E2**. Câu hỏi mang theo ba thứ `ADR-0067` đòi
  cho E2, ghi ngay tại điểm chờ này, không mở thêm một lần hỏi nào:
  - mức đã dùng: đến lượt 8, có 8 lượt review độc lập Codex trên đặc tả, cả 8 `request_changes` (đếm 2026-11-18 từ stdout
    lưu của từng lượt); trần theo dòng khai `ADR-0055` là 10 lượt, tức còn 2. Lúc hỏi, đọc lại số này từ biên nhận review,
    không chép từ dòng này;
  - còn thiếu: đúng một quyền, là comment duyệt băm của chủ kho neo `spec_sha256` của bản cuối. Agent không có quyền ấy, vì
    quyết định 2 của `ADR-0067` (người soạn tự đóng băng) chỉ áp cho đặc tả thuộc Mission đã duyệt hướng, mà #646 không gắn
    Mission nào (chưa đo được có Mission nào nhận #646 hay không, §8);
  - để làm gì: có băm đóng băng thì mới cấp được lease `LEASE-TRUONG-KHAI-NGHIA` g1 neo `spec_sha256` ấy, write set một tệp
    `docs/PROTOCOL_DA_PHIEN.md`.

## 7. `hinh_dang_ke_thua`

`khong_ap_dung`: packet làm rõ văn bản protocol, không phải packet khắc phục một bản vá cũ.

## 8. `chua_do_duoc`

- Lý do 31/175 lease thiếu `base_sha` và 146/175 lease thiếu `heartbeat_at`/`lease_until`: không đo được. Các con số chỉ dùng
  để ghi quy ước, không chống đỡ quyết định nào.
- Có controller hay phiên nào NGOÀI kho đọc `heartbeat_at` không: không đo được. §20 khai "không có controller ngoài"; mệnh
  đề 1 chỉ nói về trong kho.
- PR đang mở nào sửa `docs/PROTOCOL_DA_PHIEN.md`: không đo, chỉ đo lease qua `ai-dang-giu`. Lease và ref chỉ phiên soạn đo, có
  mạng; reviewer lượt 1 không đo lại. Phải đo lại trước khi cấp lease.
- Kích thước thật: bản thử cho đúng 14 dòng thêm, 0 dòng xoá (khối §3); N1 đo lại trên H trước khi công bố.
- Các số dòng ở §0 là của blob trên `641108c` và trôi khi `docs/PROTOCOL_DA_PHIEN.md`, `ops/lease_publish.py`,
  `ops/ci_duong_nhanh.py` hay `.claude/dev/packet_loop.py` đổi.
- Model phục vụ của reviewer lượt 1: reviewer tự khai là chưa đo được.

## 9. `lich_su_sua_doi_truoc_duyet`

Băm chưa được chủ kho duyệt, nên vẫn là revision 1. Bản đầu `7c081f98…` sửa theo review độc lập Codex lượt 1
(`request_changes`, 4 P2 + 2 P3; toàn văn ở stdout của lượt chạy, 2026-11-18T04:56:47Z):

- P2 N5: phép đếm token thay bằng đối chiếu bảy mệnh đề nguyên văn (§3) trên đoạn đã gộp khoảng trắng. Thêm ba đột biến đảo
  nghĩa (heartbeat tự thu hồi, D4 đòi chưa qua, phải khác `base_sha`) và phép so byte toàn khối YAML kể cả rào bằng băm base.
  Thêm script đo, và ghi kết quả chạy thử ở §0.
- P2 N4: chuyển sang `git grep -n -Fw` hoặc mẫu neo khai báo, kèm số hit kỳ vọng và exit code cho từng phép. Tách 0 hit ở sáu
  vị trí cổng khỏi 1 hit của fixture. Dẫn ca xanh giả `-F cmd_kiem_dong`.
- P2 M2 (§0, M2): hạn được mô tả có phạm vi. Protocol giữ `lease_until` là hạn tuyệt đối; D4 đọc nó như điều kiện đóng WP;
  `kiem()` dùng `lease_expires_at_utc` khi chốt hạn bật; `ai-dang-giu` phân loại theo cùng trường. Hai đường `kiem_github` và
  `ops/ci_duong_nhanh.py` bỏ chốt hạn. Thêm số đo 29/29 lease có `lease_until` bằng `lease_expires_at_utc`.
- P2 N2: thêm phản chứng định danh (chép doctrine §5.1 vào adapter; bỏ một dòng §20), dẫn hai ca
  `case_doctrine_scan_chep_tron_5_1_bi_chan` và `case_adr_song_thieu_dong_thi_do`.
- P3 M1: thu hẹp phạm vi grep cho đúng phép đo (kèm các hit ngoài phạm vi). Ghi rõ ngưỡng 360 phút chỉ áp cho lease mới thuộc
  hiệu lực `ADR-0056`.
- P3 M3: nêu đủ hai nhánh K4 (review offline hoặc human audit `_human_merge`) và dạng 40 hex thường. Ghi rằng số 58 chỉ chứng
  minh quan hệ bằng nhau, còn điều kiện "chưa có head ứng viên" là quy ước do đặc tả chọn.
- §2: thêm lý do giữ #646 mục 1 ngoài phạm vi: đường land kiểm head tại lúc merge là việc của packet khác. N1 thêm phép đo độc
  lập cho trần 450 dòng. §6 thêm thứ `ADR-0067` bắt mang theo khi hỏi E2.

Bản sau lượt 1 (`dd1ff3ce…`) sửa theo review độc lập Codex lượt 2 (`request_changes`, 2 P2 + 1 P3; sáu finding lượt 1 đã đóng):

- P2 N5 byte: script đọc và băm lát cắt YAML trên bytes thay vì `open(..., encoding='utf-8')` (chế độ văn bản chuẩn hoá xuống
  dòng nên một byte `0D` lọt). Thêm phản chứng LF → CRLF.
- P2 N5 vị trí: chỉ đối chiếu trong vùng từ sau rào đóng YAML §4 tới đoạn ``Lease `role: reviewer` ``, đòi vùng là văn xuôi
  (không rào, không comment HTML, không thụt lề mã). Thêm các ca dời đoạn ra cuối tệp, vào khối mã, sang §5, và bọc rào/thụt
  lề trong vùng; cả năm ca đỏ.
- P3 N4: thêm mẫu dương `-F` neo vào câu đọc `lease_expires_at_utc` (`kiem()`, `_phan_loai_lease`, `kiem_lease` của CI), chốt
  hạn, câu kiểm dạng `reviewed_sha_required`, câu đọc `lease_until` của D4, và lời gọi thật trong `MA_KIEM_HET_HAN`. Bỏ mẫu
  trần `bo_qua_han=True` (4 hit trên base, gồm docstring).
- §0 ghi lại kết quả chạy script mới trên base, bản thử H và mọi đột biến.

Bản sau lượt 2 (`f1950382…`) sửa theo review độc lập Codex lượt 3 (`request_changes`; đã đóng P2 CRLF và P3 mẫu dương N4):

- P2 N5 comment HTML: script loại mọi vùng `<!-- … -->` (kể cả mở giữa dòng, nhiều dòng) trước khi đối chiếu, đỏ khi còn
  comment không đóng. Thêm ca "bảy mệnh đề trong `Van dan <!-- … -->`" (rc 1) và ca comment không đóng (rc 1).
- P3 N5 đầu vào: bỏ tệp `menh_de.txt`; bảy mệnh đề nhúng trong script, kèm chốt đúng 7 dòng khác rỗng và sha256 bằng `MD_SHA`
  ghi ở §3. Thêm ca làm rỗng và ca sửa một mệnh đề (đều rc 1).
- P3 N5 khẳng định thêm: thêm mẫu âm (phần còn lại của vùng không được nhắc bốn tên trường), §3 cấm câu nối nhắc các tên ấy.
  Ca thêm câu đảo nghĩa có tên trường nay rc 1. Khai thẳng trong N5 và §6 rằng câu khẳng định không nhắc tên trường vẫn rc 0,
  và reviewer phải đọc diff để xác nhận.
- §0 ghi lại toàn bộ ma trận chạy trên bản thử (05:15Z).

Bản sau lượt 3 (`cba72fda…`) sửa theo review độc lập Codex lượt 4 (`request_changes`; ba finding lượt 3 đã đóng; giới hạn câu
thêm không nhắc tên trường được chấp nhận với điều kiện §6 được thực hiện):

- P2 N5 mệnh đề nằm trong mã: script chỉ nhận đoạn văn xuôi cấp ngoài cùng (chặn blockquote, danh sách, tiêu đề, bảng, thẻ
  HTML, mọi comment HTML trong vùng), và dựng code span theo CommonMark trước khi đối chiếu, nên span định danh của §3 vẫn
  khớp còn span bao trọn mệnh đề thì không. Khoá bằng hai ca xanh giả reviewer dựng (blockquote chứa rào, code span hai
  backtick giữa dòng), ba ca cùng họ (blockquote văn xuôi, danh sách, tiêu đề), và các ca dương (H, H 60 cột, quét 30–160
  cột). Ma trận 27/27 đúng kỳ vọng; script lượt trước cho rc 0 ở năm ca ấy.
- P3 §6: điểm chờ duyệt băm E2 nay ghi mức đã dùng, phần còn thiếu và mục đích, ngay tại điểm chờ.

Bản sau lượt 4 (`79fdd57d…`) sửa theo review độc lập Codex lượt 5 (`request_changes`; ba finding lượt 4 đã đóng; hai P2 mới
cùng một gốc). Đổi THIẾT KẾ, không vá thêm:

- Gốc rễ: N5 dựa vào danh sách CẤM dạng Markdown. Lượt 5 cho bốn dạng lọt mới (thuộc tính HTML, link reference definition,
  setext heading, ô tiêu đề bảng) và một ca đỏ oan (ngắt dòng ngay trước `#646.`). Đây là lượt thứ năm cùng hình dạng lỗi.
- Thiết kế mới: §3 chốt nguyên văn khối 14 dòng (bảy mệnh đề, mỗi mệnh đề một đoạn một dòng), kèm `VUNG_SHA`. N5 đòi vùng
  đích bằng từng byte khối ấy (allowlist một phần tử). N1 siết thành numstat đúng `14	0`, nên mọi thay đổi ngoài vùng cũng
  đỏ. Bỏ cam kết ngắt dòng tự do và ghi lý do ở §3. Bỏ mẫu âm theo tên trường và phép dựng code span, vì không còn cần.
- Ma trận 31 ca gồm ca cũ, bốn ca lượt 5 và ca `#646`; 31/31 đúng kỳ vọng. Đột biến "bằng" → "chứa" làm 5 ca âm xanh. pandoc
  xác nhận khối là bảy `<p>`.
- §6: giới hạn N5 viết lại theo cặp N1 + N5.

Bản sau lượt 5 (`15b17a01…`) sửa theo review độc lập Codex lượt 6 (`request_changes`; hai P2 lượt 5 đã đóng, thiết kế
allowlist được chấp nhận):

- P2 N1 bỏ lọt đổi mode: N1 thành script `n1.sh` năm chốt. Thêm `git diff --summary` rỗng, mode `100644` giữ nguyên qua
  `git ls-tree`, và blob tại H bằng `git hash-object --no-filters` của tệp kỳ vọng dựng từ blob base. Script N5 thêm chế độ
  `--ky-vong` để dựng tệp ấy. Thêm ca `chmod +x` và ca chèn sai vị trí cùng numstat `14 0`. Đột biến từng chốt cho thấy mỗi chốt
  có răng.
- P3 §6: điểm chờ E2 ghi số lượt thật (sáu lượt, cả sáu `request_changes`). §8 sửa 13 thành 14 dòng.

Bản sau lượt 6 (`24091c02…`) sửa theo review độc lập Codex lượt 7 (`request_changes`; mode và §8 đã đóng):

- P2 + P3 cùng gốc, `n1.sh` kế thừa cấu hình và thuộc tính Git: gitlink lọt dưới `diff.ignoreSubmodules=all`, còn `* -diff`
  làm numstat đỏ oan. `n1.sh` viết lại chỉ bằng plumbing: `diff-tree --raw --no-abbrev --ignore-submodules=none` đòi đúng một
  dòng `M` mode `100644`→`100644`; đếm dòng thêm/xoá bằng `difflib` trên byte blob; giữ chốt blob kỳ vọng. Mọi lệnh chạy
  dưới `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_ATTR_NOSYSTEM=1`, `-c diff.ignoreSubmodules=none`. Thêm
  phản chứng gitlink + `diff.ignoreSubmodules=all` (đỏ) và `* -diff` với H đúng (xanh).
- P3 §6: mức đã dùng ghi "đến lượt 7, 7 `request_changes`, đọc lại từ biên nhận lúc hỏi"; bỏ "lượt approve sắp tới".

Bản sau lượt 7 (`0c9c005b…`) sửa theo review độc lập Codex lượt 8 (`request_changes`; ba finding lượt 7 đã đóng; đã dùng
8/10 lượt, nên sửa trọn lớp chứ không vá điểm):

- P2 `git replace`: mọi lệnh git trong `n1.sh` chạy dưới `GIT_NO_REPLACE_OBJECTS=1`; N5 nay được `n1.sh` gọi trên chính blob
  H trích qua đường ấy. Rà cả lớp cơ chế đổi cách đọc object: replace (đóng bằng biến); grafts (không chạm phép so cây, có ca
  đo); `GIT_OBJECT_DIRECTORY`, `GIT_ALTERNATE_OBJECT_DIRECTORIES` và các biến `GIT_*` khác (đóng bằng `unset`); alternates
  trong kho và config cục bộ (khai là giả định tin cậy). Thêm chốt `cat-file -t` = commit và dòng `tree` thô. Thêm ca replace
  commit và replace blob.
- P3 môi trường: ghim kho bằng `git -C <đường>`, kiểm `rev-parse --git-dir` trước, tách rc 2 (LỖI MÔI TRƯỜNG) khỏi rc 1 (nội
  dung). Câu cam kết "độc lập môi trường" thu hẹp về đúng phạm vi đã đo.
- Đột biến từng chốt chạy lại; khai thẳng các chốt chồng lớp không có răng độc lập.
- §6: mức đã dùng ghi đến lượt 8.
