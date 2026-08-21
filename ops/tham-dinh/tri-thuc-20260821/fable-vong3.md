# VÒNG 3 — Fable 5. Giải một bất đồng: vị trí script + răng từ packet 1

Phép đo mới của lượt này (worktree chỉ-đọc `th2/kho`):
- `packet_loop.py` = 1223 dòng, `packet_loop_test.py` = 2483 dòng, `cross-review/SKILL.md` = 110 dòng;
  `receipt`/`review-run` = **0 occurrence** trong `packet_loop.py` (ĐO ĐƯỢC).
- `cmd_record_review` (dòng 871) đã đòi `--reviewed-sha` khớp `reviewing_head_sha`, đã chặn attempt-0,
  đã đếm finding — điểm móc receipt nằm sẵn ở đó (ĐỌC ĐƯỢC).
- ADR-0044: `sensitive` = "chạm authority: ≤3 tệp và ≤300 dòng THÊM" (ĐỌC ĐƯỢC, nguyên văn dòng 5).
- `t25`/`t34`/`t35` ĐỀU đã có trong `ops/lease_publish_test.py` (dòng 601/1272/1375); và
  `THAM_DINH_KE_HOACH_20260821.md:60-70`: "V1/V2/V3 BỎ… phần lớn Slice A/B đã vào master; còn lại
  của Slice B chỉ đủ một packet nhỏ" = mục **C** (sổ nợ + hạ lời khai `t34` + ca docstring) (ĐO ĐƯỢC).

## E1 — Có. Bản có răng ĐỤNG review authority, và tôi ĐỔI Ý theo codex

**ĐỌC ĐƯỢC:** `record-review` là ĐÚNG MỘT ĐƯỜNG vào `accepted` (chú thích dòng 100–125 nói thẳng
"chỉ để lại MỘT cửa mới thắng"), và kho đã trả giá một lần cho việc vòng qua nó
(`review-transition-bypasses-record-review`, ghi tại dòng 113). Sửa điều kiện nhận của cửa ấy —
"thiếu receipt hợp lệ ⇒ từ chối" — là đổi cái gì được phép trở thành `accepted`. Đó là định nghĩa
"chạm authority" của ADR-0044, không phải cảm tính ⇒ **`sensitive`, ≤3 tệp/300 dòng thêm**.

**SUY LUẬN:** bản vòng 2 của tôi (`ops/dung_sandbox_review.py` standalone, class `systemic`) trả lời
được câu "lượt dựng tay bị chặn ở đâu" đúng một cách: **không ở đâu cả** — chính tôi đã tự khai thế.
Theo tiêu chí của cả hai vòng trước, đó là cổng CHỈ LÀ CHỮ ⇒ tôi **rút** phương án tệp mới đứng
riêng. Vị trí đúng là `packet_loop.py`, vì răng phải cắm vào cửa duy nhất đang tồn tại.

## E3 — Danh sách tối thiểu (trả lời trước E2 vì nó quyết định số dòng)

Gộp 4 check của tôi với 6 điều của codex, mỗi mục một sự cố THẬT + một đột biến làm ca đích ĐỎ:

| # | check | sự cố neo | đột biến đỏ |
|---|---|---|---|
| a | **Tự sinh diff `review_scope_base_sha..reviewed_sha`**, cấm nhận bundle ghép tay (codex #2, nuốt luôn "đủ bundle" của tôi: diff máy sinh thì không quên được lát) | bundle thiếu lease X4 | thay diff máy sinh bằng đọc tệp diff cung cấp sẵn ⇒ fixture "thiếu lát X4" phải ĐỎ |
| b | **Neo trích dẫn**: mọi (path, sha256) lease/prompt trích phải resolve trong bundle, đúng băm (Fable #1 ≡ codex #1/#3 phần bundle) | prompt trỏ tệp không có trong cây (ca −1h53m) | bỏ so băm, chỉ kiểm tồn tại ⇒ fixture băm-lệch phải ĐỎ |
| c | **rc trực tiếp**: subprocess argv, đọc `returncode`, cấm pipeline trên đường đọc mã thoát (Fable #3 ≡ codex #5) | `\| tail` nuốt rc | chèn một shell-pipe vào đường chạy ⇒ ca đích ĐỎ |
| d | **Thăm dò GHI** đích báo cáo trước khi tiêu lời gọi (Fable #4 ≡ codex #4) | `-s read-only` nuốt báo cáo | bỏ probe ⇒ fixture sandbox read-only phải ĐỎ |
| e | **`record-review` đòi receipt hợp lệ**: tồn tại, `reviewed_sha` trong receipt khớp `reviewing_head_sha`, bốn mục a–d đều `có` (`KHÔNG ĐO ĐƯỢC` ⇒ từ chối, fail-đóng) (codex #6 phần răng) | vòng qua `record-review` (finding lượt 6, dòng 113) — hình dạng "dựng tay" 4 lần/3 ngày | nới `record-review` nhận thiếu receipt ⇒ ca đích ĐỎ |

**BỎ, có tên (SUY LUẬN):** codex #6a "head không đổi sau chạy" — không neo được vào sự cố nào trong
bốn; `reviewed_sha` khớp head đã được `record-review` kiểm sẵn (dòng 905–907). Codex #1 phần "resolve
prompt từ ref bền" — vòng 2 đã đo `ops-publish-lease.yml:203` đọc prompt từ head được đẩy, đề bài xác
nhận đòi thế là báo động giả cấu trúc; resolve-trong-bundle (mục b) là đủ ở cửa này. Mọi check khác
"cho chắc" — bỏ theo đúng luật kho.

## E2 — 300 dòng: bản đủ 5 mục KHÔNG chắc lọt ⇒ cắt sao cho lát 1 vẫn có răng

**SUY LUẬN (ước, khai ở KHONG_DO_DUOC):** mã lõi a–e ≈ 130–170 dòng trong `packet_loop.py`
(subcommand `review-run` tối thiểu + emit receipt + ~35 dòng chốt trong `cmd_record_review`); mỗi mục
một fixture đỏ + một mutant ≈ 25–35 dòng/mục trong `packet_loop_test.py` ⇒ tổng ≈ 260–340. **Cận
trần, có thể tràn.** Spec đặt hard stop `+300` (theo codex); nếu numstat thật vượt, cắt theo thứ tự:

- **Lát 1 (sensitive, giữ bằng được):** `review-run` với **a + c + e** và receipt + fixture/mutant của
  đúng ba mục ấy. Write set: `packet_loop.py` + `packet_loop_test.py` (2 tệp — chừa chỗ). Răng nằm ở
  **e**: từ ngày land, `record-review` từ chối mọi lượt không có receipt của `review-run` — KHÔNG phải
  "script tuỳ chọn, siết sau". Lát 1 một mình chặn được **hai** trong bốn sự cố: thiếu-lát-X4 (a: diff
  máy sinh) và nuốt-rc (c) — và đóng cả lớp thứ năm, vòng-qua-cửa (e). Đủ điều kiện "≥1 trong bốn".
- **Lát 2 (thường, nối tiếp trên integration đã nhận lát 1):** b + d + fixture tái dựng đủ bốn sự cố +
  vài dòng adapter `cross-review/SKILL.md`. Trong thời gian chờ lát 2, receipt ghi
  `neo_trich_dan: KHONG_DO_DUOC` / `write_probe: KHONG_DO_DUOC` **được khai tường minh trong schema
  receipt ngay từ lát 1** — trạng thái ba có mặt từ đầu, không phải nới sau rồi siết lại.
- **Không được cắt:** test của mục nào đi cùng lát của mục đó ("không bỏ test để lọt ngưỡng" — codex,
  tôi ký). Adapter SKILL.md nếu làm tràn thì thành successor docs-only (codex đã đề, tôi ký).

## E4 — Slice A đã land; lát 2 spec-gate song song với packet 1 ĐƯỢC, nhưng còn vướng mục C

**ĐO ĐƯỢC:** write set packet 1 = `.claude/dev/packet_loop*.py` (+ SKILL.md ở lát sau); write set
lát 2 spec-gate = `ops/lease_publish.py` + `ops/lease_publish_test.py` — **rời nhau hoàn toàn** ⇒
riêng cặp này, mở song song hai packet là hợp lệ theo ADR-0044.

**Nhưng (ĐO ĐƯỢC):** Slice B chưa ĐÓNG — phần còn lại là mục **C** (`THAM_DINH…:70`): hạ lời khai
`t34` + ca docstring, tức C **ghi vào `ops/lease_publish_test.py`** — GIAO với write set lát 2 tại
đúng tệp đó. Câu "phải làm SAU hai slice vì write set giao nhau" của ADR-0044 vì vậy còn hiệu lực với
lát 2 chừng nào C chưa land. **Trả lời thẳng cho người giữ:** mở **packet 1 + mục C** song song ngay
(write set rời nhau); lát 2 spec-gate mở NỐI TIẾP ngay sau khi C land (C nhỏ, tính bằng giờ). Đừng mở
lát 2 song song với C — hai packet cùng ghi `lease_publish_test.py` là đúng hình dạng chuỗi
#203→#206 mà ADR-0044 sinh ra để chặn. Và theo `CLAUDE.md`: bảng này là dữ liệu — cả hai packet vẫn
cần Packet Issue + lease, không phiên nào tự bắt tay.

## CHOT

Packet 1 là **mở rộng `.claude/dev/packet_loop.py`** (theo codex — tôi ĐỔI Ý bỏ tệp standalone):
subcommand `review-run` dựng-và-chạy reviewer fail-đóng, emit receipt máy; `cmd_record_review` **từ
chối mọi lượt thiếu receipt hợp lệ ngay từ lát 1**. Write set lát 1: `packet_loop.py` +
`packet_loop_test.py` (2 tệp), phân loại **`sensitive`**, hard stop **+300 dòng thêm** trong spec;
nội dung lát 1 = check **a + c + e** của E3 kèm fixture + mutant từng check, trạng thái ba
`KHÔNG ĐO ĐƯỢC` khai trong schema receipt từ đầu; lát 2 (thường, nối tiếp trên integration) = b + d +
đủ bốn fixture sự cố + adapter SKILL.md. Song song: mở **packet 1 và mục C cùng lúc**; lát 2
spec-gate (`ops/lease_publish*`) mở ngay sau khi C land — không song song với C vì giao nhau tại
`ops/lease_publish_test.py`.

## TOI_KHONG_KY

1. **SUY LUẬN:** tệp standalone `ops/dung_sandbox_review.py` class `systemic` — phương án vòng 2 của
   chính tôi; lượt dựng tay không bị chặn ở đâu ⇒ cổng chỉ là chữ. Rút.
2. **SUY LUẬN:** mọi biến thể "script tuỳ chọn, `record-review` vẫn nhận lượt thủ công" — kể cả dưới
   dạng "cờ tạm để chuyển tiếp". Cờ tạm là đường lách có tên.
3. **SUY LUẬN:** check "head không đổi sau chạy" và "prompt resolve từ ref bền" trong packet 1 —
   không neo được sự cố thật / đã đo là báo động giả cấu trúc (E3).
4. **SUY LUẬN:** nhét b + d + adapter vào lát 1 để "đủ bốn ngay" nếu numstat tràn 300 — tràn trần
   `sensitive` là đúng cái ADR-0044 đo được để cấm; thà thiếu hai check khai `KHÔNG ĐO ĐƯỢC` còn hơn
   một packet authority quá trần.

## KHONG_DO_DUOC (khai)

- Số dòng thêm THẬT của lát 1 (260–340 là ƯỚC từ đếm mục; chỉ `git diff --numstat` lúc thi công mới
  là phép đo — hard stop +300 trong spec là chốt thay cho ước lượng).
- Write set CHÍNH XÁC của mục C (suy từ `THAM_DINH…:70` + vị trí `t34`; nếu C hoá ra không đụng
  `lease_publish_test.py` thì kết luận "lát 2 chờ C" ở E4 phải đo lại — chiều ngược lại không đổi
  kết luận song song packet 1 ∥ C).
- `record-review` đòi receipt từ ngày land có chặn oan lượt review nào đang DỞ giữa chừng lúc đó
  không — phải kiểm state files `.tl_state`/packet đang mở khi thi công, không đọc được từ worktree.
- Hai mục cũ giữ nguyên: khả năng fetch `luu-tru/*` lúc chạy check neo (lát 2), và chi phí giờ-người
  của 4 lượt review hỏng (vẫn chỉ có lời kể).
