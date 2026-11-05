# A13-K1-CANARY r2 — canary đo K1 trên kho thật

Đặc tả này là đặc tả của chính packet canary, và nó cố ý KHÔNG có dòng khai điều kiện merge
theo ADR-0060: con số dòng khai bằng 0 chính là thứ được đo. Vì vậy trong tệp này, tên trường ấy chỉ
xuất hiện giữa dòng, trong dấu nháy ngược, không bao giờ ở đầu dòng. Một dòng bắt đầu bằng tên trường
ấy sẽ làm canary chết (A1 đỏ hoặc K1 đếm 1 dòng). Tệp cũng không khai dòng `tran_*` nào; lý do ở mục
`review_class`.

## Định danh

- `packet_id`: `A13-K1-CANARY`; revision 2; generation dự kiến 1.
- Thay thế: `ops/specs/A13-K1-CANARY-r1.md` (sha256 `78e31ecb0a818048936356c561239e03d8e7823bab16394b7c3740daff46f82b`,
  commit `06e4b0c1c74fa3dfa3784b58bab5e6b50ee3a94e`). r1 chưa từng được duyệt hay neo vào lease nào; nó giữ
  nguyên byte trên nhánh `ops/a13-k1-canary-spec` làm lịch sử. Lý do ra r2: mục *Phản biện r1 → r2* ở cuối.
- `packet_issue`: Issue mở cùng lượt đóng băng này (số Issue ghi trong thân Issue và trong comment
  bàn giao; đặc tả không tự chứa số Issue của mình để khỏi phải đổi băm).
- Packet cha của tiêu chí: #1124 `ADR-0060-MAC-DINH`, đã land qua PR #1186, merge commit
  `1f0941e9bba1d1d517eda4174167b81963c06bd5`.

## nguon_cap_viec

- Tiêu chí A13 của #1124, giống nhau từ r1 tới r6. Bản dẫn được: `ops/specs/ADR-0060-MAC-DINH-r2.md`,
  dòng A13: *"packet đầu tiên sau land có đặc tả KHÔNG mang dòng `dieu_kien_merge` chạy `kiem-merge`
  qua K1"*. Trạng thái trước packet này: `not_measured`.
- Chỉ thị chủ kho ngày 04-11-2026: *"Mở phiên mới soạn đặc tả cho A13 để chuẩn bị triển khai."*, giao
  qua phiên `session_015GtxramaGcW4MVoHByjp3Z`.
- Các quyết định thiết kế Q1–Q10 được chủ kho duyệt trong phiên soạn đặc tả ngày 04→05-11-2026
  (*"Đồng ý tất cả."*, hai vòng). Bảng quyết định ở mục cuối.
- Đặc tả KHÔNG phải lease. Thi công chỉ bắt đầu khi có Packet Issue cùng lease còn hiệu lực neo
  `spec_hash` của tệp này (`docs/PROTOCOL_DA_PHIEN.md` §3.2, §4).

## Vì sao cần

Ca `cong_c_k1_khong_dong` trong `.claude/dev/packet_loop_test.py` chỉ đo K1 trên kho git giả. A13 là
lần đầu K1 được đo trên kho thật: blob đặc tả nằm tại head của một PR thật, `spec_hash` lấy từ một lease
thật trên nhánh `ops/**`, khuôn lease và đặc tả do người thật viết. Nếu K1 đỏ oan thì phải SỬA CỔNG,
không được chèn lại dòng khai để lách. Chèn lại thì canary chết.

## Số đo nền (đo 04-11 15:36–15:40Z và 05-11 02:01Z)

- K1 nằm trong `cmd_kiem_merge`, `.claude/dev/packet_loop.py` (dòng 3197 tại `1f0941e`). Nó đọc
  `git show H:<--spec>`, so sha256 với `spec_hash` của `--lease`, rồi đếm các dòng khớp
  `^dieu_kien_merge:`. 0 dòng thì đạt. 1 dòng thì OID phải qua ba phép đo của M10. Từ 2 dòng trở lên thì đỏ.
- **K1 đạt không in gì.** `_dk` chỉ in `THIẾU K1 hiệu lực M10: …` khi đỏ. `kiem-merge` chạy hết K0–K7
  rồi gom chỗ thiếu, nên K1 đo được ngay khi đã có PR head và lease, kể cả khi K2–K7 còn thiếu (lúc đó
  rc chung là 12).
- `packet_loop.py` trên master `1813bfd4513704cf792a272a86b22e5e08893b9a` (05-11 02:01Z) giống hệt
  `1f0941e`: `git diff --stat` rỗng.
- Packet #1187 `PR1184-MERGE-CONTRACT` (cấp 04-11 10:56Z, base `1f0941e`) **sửa K1** và đang giữ
  `.claude/dev/packet_loop.py`. `ai-dang-giu` cho tệp đó trả rc=11, `NGƯỜI_GIỮ 1:
  pr1184-merge-contract-r2-g2-codex` (04-11 15:39Z). Đặc tả r2 của #1187 (sha256 `975c5d31…`) có 0
  dòng khai, và tiêu chí A9 của nó đòi *"canonical legacy K1 qua"*. Như vậy #1187 cũng có thể đo K1
  0 dòng trước canary này (xem Q1, Q10).
- OID land của ADR-0060 trên first-parent master: `36d7c5dcdcbbb27176b75135125b9009f9fe0587`
  (merge PR #1087, 31-10-2026). Tìm bằng `git log --first-parent --diff-filter=A origin/master --
  docs/adr/0060-dieu-kien-merge-va-moc-ready.md`.
- Đồng bộ ref (05-11 02:01Z): 842 tên trên máy chủ, 842 tên cục bộ, không thiếu tên nào (so TẬP tên,
  đã loại `HEAD`).

## review_class

`routine`. Lý do: write set của PR thi công chỉ có một tệp đặc tả Markdown trong `ops/specs/`, không
đổi authority hay security boundary (`docs/PROTOCOL_DA_PHIEN.md` §8). Classifier của dispatcher vẫn có
quyền nâng lớp; executor không được hạ lớp.

Các hệ quả, đo trên mã tại `1f0941e`:
- K6 Windows (ADR-0060 M3): `_phan_loai_windows` trả `not_required`, vì mọi tệp đều là `.md`.
- K7 `full_mutant_audit` (ADR-0060 M9): `_cham_m9` trả sai, vì diff không chạm `.claude/dev/**`,
  `ops/**/*.py` hay `.github/workflows/**`.
- Không khai `tran_loi_goi_codex` hay `tran_kich_thuoc_sensitive`: packet không phải `sensitive` và
  không dùng Codex review (Q9).

## write_set

**Pha thi công (PR canary), đúng 1 đường dẫn:**
1. `ops/specs/A13-K1-CANARY-r2.md` — chính tệp này, nguyên byte. K1 đọc nó tại H.

**Pha ghi sổ land (PR riêng sau merge), đúng 1 đường dẫn:**
2. `ops/land/a13-k1-canary-evidence.yaml`

Hồ sơ đo KHÔNG được nằm trong H của PR canary. K1 đo blob tại H, nên thêm tệp hồ sơ vào H sẽ sinh H′
và phép đo phải chạy lại mãi (Q8).

Ngoài hai tệp trên, packet còn ghi lên GitHub (không phải tệp trong kho): M8 trên Packet Issue và một
comment backlink trên #1124.

Người giữ: `ai-dang-giu ops/specs/A13-K1-CANARY-r1.md` cho `NGƯỜI_GIỮ 0` (04-11 15:39Z); đường dẫn r2 đo
  lúc đóng băng r2, kết quả ghi trong comment đóng băng trên Packet Issue.
`ops/land/a13-k1-canary-evidence.yaml` chưa đo. Hai đường dẫn đều phải đo lại TRƯỚC khi cấp lease, sau
khi so tập ref.

## ngoai_pham_vi

- Sửa `.claude/dev/packet_loop.py` hoặc `.claude/dev/packet_loop_test.py`, kể cả để thêm dấu hiệu dương
  cho K1. #1187 đang giữ tệp đó; thiếu dấu hiệu dương được ghi thành nợ (M5).
- Sửa cổng khi K1 đỏ oan. Việc đó thuộc packet riêng (Q5).
- Đẩy lên kho các đặc tả phụ dùng cho ca phản chứng. Ba ca đó chạy trên commit cục bộ (Q3).
- Sửa `docs/PROTOCOL_DA_PHIEN.md` (do #1187 giữ) và các ADR đã Accepted.
- Ghi đè trạng thái A13 trong hồ sơ #1124 (`ops/specs/ADR-0060-MAC-DINH-*`, `ops/land/` của #1124).
  Packet này chỉ thêm backlink.
- Đo thay cho #1187 hoặc sửa đặc tả và lease của #1187.
- Lớp lỗi "đặc tả vắng hoặc lệch ở H" (lớp #1184 đã gặp, #1187 đang vá). Canary luôn đặt S tại H nên
  không bao giờ đi qua lớp ấy; A1 xanh KHÔNG nói gì về packet thật để đặc tả ở nhánh `ops/**`.

## muc_tieu

Đánh số theo tiêu chí ở mục `nghiem_thu`. Mỗi mục chiếu vào một đường dẫn của `write_set` (L2).

- **M1** — Đưa đặc tả 0 dòng khai lên head H của một PR thật, lease thật neo `spec_hash`; chạy
  `kiem-merge` bằng `packet_loop.py` GHIM tại `1f0941e` và ghi kết quả của K1.
  → `ops/specs/A13-K1-CANARY-r2.md` (blob được đo), kết quả ghi vào `ops/land/a13-k1-canary-evidence.yaml`.
- **M2** — Đo lại độc lập hai thứ K1 dựa vào (băm blob, số dòng khai), không qua `packet_loop.py`.
  → `ops/land/a13-k1-canary-evidence.yaml`.
- **M3** — Sáu ca phản chứng, mỗi ca đóng răng cho đúng một phần của K1: A2b (sai `spec_hash`, H thật);
  A3 (1 dòng OID land thật), A4 / A4b / A4c (1 dòng, mỗi ca làm hỏng đúng một trong ba vế M10), A5 (2
  dòng) trên commit cục bộ H′, không đẩy lên kho. → `ops/land/a13-k1-canary-evidence.yaml`.
- **M4** — Nếu master lúc đo khác `1f0941e` ở `.claude/dev/packet_loop.py`, chạy lại M1 và M3 bằng bản
  master hiện hành và so từng ca. → `ops/land/a13-k1-canary-evidence.yaml`.
- **M5** — Ghi bằng chứng, ghi nợ "K1 không có dấu hiệu dương", và đăng backlink về #1124.
  → `ops/land/a13-k1-canary-evidence.yaml` (cùng M8 và comment trên GitHub).
- **M6** — PR canary qua đủ K0–K7 rồi land; sau land chạy `kiem-dong-wp` và lập M8.
  → `ops/specs/A13-K1-CANARY-r2.md` (H) và `ops/land/a13-k1-canary-evidence.yaml`.

## nghiem_thu

Ký hiệu dùng chung:
- `PL0` = `<thư mục tạm>/.claude/dev/packet_loop.py`, sau khi xuất **cả thư mục** `.claude/dev` tại
  commit ghim: `git archive --format=tar -o <tạm>.tar 1f0941e9bba1d1d517eda4174167b81963c06bd5
  .claude/dev` rồi `tar -xf <tạm>.tar -C <thư mục tạm>`. Lấy riêng MỘT tệp `packet_loop.py` là KHÔNG
  chạy được: dòng `from launcher import ky_ban_ghi_luot` đòi `launcher.py` nằm cùng thư mục (đo 05-11
  02:08Z: rc=1, `ModuleNotFoundError`, lệnh chết trước K0). Executor đối chiếu `git hash-object PL0`
  với `git rev-parse 1f0941e:.claude/dev/packet_loop.py` (`f5a4bb11fc6529999bb5ab60a5e9d60f90c04a44`).
  Lệnh chạy với `--root .` ở gốc kho thật, không chạy trong thư mục tạm.
- `H` = head của PR canary đọc qua `git ls-remote origin refs/pull/<N>/head`.
- `L` = tệp lease đã đăng của packet, đọc từ nhánh `ops/**` của nó, không phải bản nháp.
- `S` = `ops/specs/A13-K1-CANARY-r2.md`.
- "dòng K1" = mọi dòng stderr của `kiem-merge` mà sau tiền tố `  THIẾU  ` bắt đầu bằng `K1`.

Mỗi tiêu chí ghi phép đo, phép làm nó ĐỎ (L3), và trạng thái lúc đóng băng.

- **A1 (M1) — K1 qua trên kho thật, bằng PL0.** Chạy
  `python PL0 kiem-merge --root . --repo ducthangho/tra-luat --pr <N> --head H --base <base lease>
  --spec S --lease L` cùng các đối số bắt buộc còn lại; tệp nào chưa có thì trỏ đường dẫn không tồn
  tại và chấp nhận các K đó báo THIẾU.
  ĐẠT khi cả ba điều sau cùng đúng:
  (a) stderr có dòng `CHƯA ĐỦ ĐIỀU KIỆN MERGE` hoặc stdout có `ĐỦ ĐIỀU KIỆN MERGE trên H`, nghĩa là lệnh
  đã chạy tới phần tổng kết, không chết ở bước đọc đối số;
  (b) số dòng K1 bằng 0;
  (c) nếu rc khác 0 thì mọi dòng `THIẾU` đều thuộc K khác K1.
  ĐỎ khi có bất kỳ dòng K1 nào, hoặc rc=2 (`RC_ARG`, lỗi đối số), hoặc lệnh không tới phần tổng kết
  (ví dụ rc=1 vì traceback, như lần chạy thử đầu với PL0 lấy riêng một tệp). rc chấp nhận được là 0
  hoặc 12 (`RC_GATE`).
  Đột biến đổi màu: chèn một dòng `dieu_kien_merge: ADR-0060@sai` vào bản sao cục bộ của S trên H′ ⇒ phải
  có dòng K1 (chính là ca A4).
  Lúc đóng băng: `chưa đo được` (chưa có PR, chưa có lease). Đã chạy thử trên commit cục bộ (mục cuối).
- **A2 (M2) — Đo lại độc lập.** `git show H:S | sha256sum` phải bằng `spec_hash` trong L, và
  `git show H:S | grep -c '^dieu_kien_merge:'` phải in `0`.
  Thêm: giá trị `spec_hash` đọc từ L bằng `yaml.safe_load` phải có kiểu `str` và khớp `^[0-9a-f]{64}$`.
  Lý do (phản biện Q2): YAML 1.1 đọc một chuỗi hex toàn chữ số thập phân thành `int` (đo 05-11: `"1"*64`
  ⇒ `int`; băm thật kiểu `78e31ecb…` ⇒ `str`), khi đó K1 đỏ vì so `str != int`. Xác suất cỡ (10/16)^64,
  nhưng nếu xảy ra thì đó là LỖI LEASE (sửa lease, viết nháy), KHÔNG phải K1 đỏ oan.
  ĐỎ khi băm lệch, số đếm khác 0, hoặc kiểu/định dạng `spec_hash` sai. Đột biến: đổi một byte của S trên H′
  ⇒ băm lệch.
  Lúc đóng băng, đo trên bản làm việc: số đếm là `0`; băm là giá trị in ra khi đóng băng.
- **A2b (M3) — sai `spec_hash` ⇒ K1 đỏ.** H thật, S thật, nhưng một lease cục bộ có `spec_hash` là 64
  ký tự hex KHÁC băm thật (ví dụ 64 chữ `0`). Chạy PL0 như A1 với `--lease` ấy.
  ĐẠT khi có đúng một dòng K1 chứa `không khớp spec_hash`. ĐỎ khi không có dòng K1.
  Đột biến mà CHỈ ca này bắt (đo 05-11 02:21Z): xoá vế `or hashlib.sha256(spec).hexdigest() !=
  lease.get("spec_hash")` khỏi K1 ⇒ A1, A3, A4, A5 vẫn đúng màu, còn A2b mất dòng K1.
- **A3 (M3) — 1 dòng hợp lệ ⇒ K1 qua.** Trên H′ = H + một tệp đặc tả phụ (ngoài `ops/specs/`, ví dụ
  `a13-phu/mot-dong-dung.md`, commit cục bộ, KHÔNG đẩy) có đúng một dòng
  `dieu_kien_merge: ADR-0060@36d7c5dcdcbbb27176b75135125b9009f9fe0587`, kèm một lease cục bộ có
  `spec_hash` là băm của tệp phụ. Chạy PL0 với `--head H′ --spec <tệp phụ> --lease <lease cục bộ>`.
  ĐẠT khi số dòng K1 bằng 0 (K0 được phép đỏ vì H′ không phải PR head).
  ĐỎ khi có dòng K1. Lưu ý: kho phải KHÔNG nông, vì K1 đòi `--is-shallow-repository` bằng `false`.
- **A4 (M3) — 1 dòng OID sai ⇒ K1 đỏ.** Như A3 nhưng OID là một SHA 40 hex KHÔNG phải commit land
  ADR-0060 (ví dụ `1f0941e9bba1d1d517eda4174167b81963c06bd5`, vì ADR-0060 đã có từ trước commit đó).
  ĐẠT khi có đúng một dòng K1 chứa `1 dòng khai`. ĐỎ khi không có dòng K1.
  Ca này chỉ làm hỏng vế (ii) "cha thứ nhất của OID chưa có tệp ADR-0060". Hai vế còn lại cần ca riêng.
- **A4b (M3) — 1 dòng, OID chưa có tệp ADR-0060 ⇒ K1 đỏ (vế (i)).** Như A4 với OID là commit gốc
  `394e93468fc8d84ec20938e6df8fb7ab72b2cc37` (`git rev-list --max-parents=0 origin/master`).
  ĐẠT khi có dòng K1 chứa `1 dòng khai`. ĐỎ khi không có.
  Đột biến mà CHỈ ca này bắt (đo 05-11 02:21Z): xoá vế `cat-file -e {oid}:{ADR0060_TEP}` ⇒ A3, A4, A4c
  vẫn đúng màu, A4b mất dòng K1.
- **A4c (M3) — 1 dòng, OID có tệp nhưng KHÔNG trên first-parent master ⇒ K1 đỏ (vế (iii)).** Như A4 với
  OID `5c47a8aa7cea163787a7d12e2a4a9affa2bc632e` — commit thêm `docs/adr/0060-…` trên nhánh của PR #1087,
  được merge vào master qua `36d7c5dc…` nhưng tự nó không thuộc first-parent (`git rev-list --first-parent
  origin/master | grep -c` ⇒ `0`, đo 05-11).
  ĐẠT khi có dòng K1 chứa `1 dòng khai`. ĐỎ khi không có.
  Đột biến mà CHỈ ca này bắt (đo 05-11 02:21Z): xoá vế `oid.encode() in fp[1].split()` ⇒ A3, A4, A4b vẫn
  đúng màu, A4c mất dòng K1.
  Executor phải đo lại hai tiền đề trước khi chạy: `5c47a8aa…` có tệp ADR-0060 và cha thứ nhất của nó
  không có; nếu tiền đề trôi thì ghi `KHÔNG ĐO ĐƯỢC`, không thay OID khác mà không ghi lại lý do.
- **A5 (M3) — 2 dòng ⇒ K1 đỏ.** Như A3 nhưng tệp phụ có hai dòng hợp lệ y hệt nhau.
  ĐẠT khi có dòng K1 chứa `2 dòng khai`. ĐỎ khi không có dòng K1.
  A2b, A3, A4, A4b, A4c, A5 cùng nhau là phép chứng minh A1 có khả năng đỏ trên kho thật, không chỉ trên
  kho giả: mỗi phần của K1 (phép so băm, vế (i), vế (ii), vế (iii), đếm ≥2 dòng) có đúng một ca giết đột
  biến xoá nó. Vế kho-không-nông chưa có ca riêng: cần một clone nông, ghi `chua_do_duoc`.
- **A6 (M4) — Hai bản K1.** Nếu `git diff --quiet 1f0941e <master lúc đo> -- .claude/dev/packet_loop.py`
  trả khác 0, chạy lại A1, A2b, A3, A4, A4b, A4c, A5 bằng bản master hiện hành và ghi bảng bảy ca × hai
  bản, mỗi ô là `có dòng K1` hoặc `không dòng K1` (hoặc `KHÔNG ĐO ĐƯỢC`).
  ĐỎ khi hai bản cho kết quả khác nhau ở BẤT KỲ ca nào, với cùng H/H′, cùng lease, cùng đối số. Không có
  miễn trừ bằng lời giải thích (phản biện Q5: câu "trừ khi nêu lý do" luôn tự làm xanh được). Khi ĐỎ thì
  dừng và hỏi chủ kho. Nếu `git diff` bằng 0 thì ghi `khong_ap_dung` kèm lệnh và rc của phép so.
  Lúc đóng băng: `chưa đo được`.
- **A7 (M5) — Bằng chứng.** `ops/land/a13-k1-canary-evidence.yaml` chứa cho mỗi ca A1/A2b/A3/A4/A4b/A4c/A5 (và A6
  nếu có): lệnh đầy đủ, rc, toàn bộ dòng `THIẾU`, dòng K1 (hoặc ghi rõ không có), H hoặc H′, tree của
  head đó, sha256 của PL0, `spec_hash`, `lease_id`, base, và thời điểm đo (UTC). Thêm kết quả của A2.
  ĐỎ khi thiếu bất kỳ trường nào cho bất kỳ ca nào, hoặc thiếu thời điểm đo.
  Tệp còn phải có một mục nợ tên `K1-KHONG-CO-DAU-HIEU-DUONG`: K1 đạt mà không in gì nên phép đo dương
  phải dựng từ sự vắng mặt; ghi nợ này cho packet sau khi #1187 nhả `packet_loop.py`.
- **A8 (M5) — Backlink.** Một comment trên #1124 trỏ tới M8 của packet này và tới tệp hồ sơ tại commit
  land của PR ghi sổ, ghi trạng thái A13 mới (`measured` kèm màu). Comment kết thúc bằng footer của kho.
  Đọc lại comment sau khi đăng. ĐỎ khi comment không tồn tại, không trỏ đúng commit, hoặc trạng thái ghi
  trong comment khác với tệp hồ sơ.
- **A9 (M6) — Land.** `kiem-merge` (bản canonical trên master lúc merge) in `ĐỦ ĐIỀU KIỆN MERGE trên H`
  với rc=0 trước khi merge; sau land `kiem-dong-wp` đạt; M8 khai đủ bốn mốc §10.2.2. Mốc nào chưa đo thì
  `not_measured` và `landed: false` (bài học `CLAUDE.md`: gate xanh theo REST chỉ là mốc run).
  ĐỎ khi rc khác 0, hoặc M8 khai `landed: true` mà thiếu mốc.
- **A10 (M1) — Đặc tả nguyên byte.** Blob của S tại H bằng blob tại commit đóng băng trên nhánh
  `ops/a13-k1-canary-spec`. ĐỎ khi khác byte. Cần đổi nội dung thì phải ra revision mới, không sửa đè.

## Khi K1 đỏ oan (Q5)

"Đỏ oan" nghĩa là A1 có dòng K1 trong khi A2 đạt (băm khớp, 0 dòng khai). Khi đó:

1. Canary DỪNG ngay tại phép đo. Packet chuyển `blocked`. Không merge, không sửa S, không chèn dòng khai.
2. Ghi rc và nguyên văn dòng K1 vào M8 tạm (comment trên Packet Issue) và comment trên #1124.
3. Lý do đỏ thuộc đúng lớp #1187 đang vá (đặc tả vắng hoặc lệch ở H, nguồn đặc tả) thì CHUYỂN cho #1187,
   không mở nợ trùng. Lý do khác thì mở Issue nợ để sửa cổng trong một packet riêng, cấp sau khi lease
   của #1187 trên `packet_loop.py` hết hiệu lực.

Nếu A2 đỏ thì đó KHÔNG phải đỏ oan; đó là lỗi của packet (băm hoặc nội dung). Sửa bằng revision mới.

## hinh_dang_ke_thua

`khong_ap_dung`. Đây không phải packet khắc phục. Ghi chú để đối chiếu: #1187 đã đo một biểu hiện
`k1-spec-source-tree-vs-frozen-metadata` ở #1184 (log rc=12, phiên này không đọc được). Biểu hiện đó
thuộc #1187, không chép bộ đếm sang đây.

## chua_do_duoc

- A1, A2 (trên H thật), A6, A7, A8, A9: chưa có PR, chưa có lease. Người đo là executor của packet này,
  sau khi PR mở và lease đăng. Đọc lại từ: `refs/pull/<N>/head`, tệp lease trên nhánh `ops/**`, tệp hồ sơ
  tại commit land, comment trên #1124.
- Log `kiem-merge` của #1184 ("K1 đỏ vì spec tại H không có") nằm ở `/workspace/scratch/pr1184/` trên
  máy Codex Desktop. Phiên soạn đặc tả không đọc được nên không dùng làm bằng chứng.
- Đường review offline (K4) bằng Claude: container soạn đặc tả đo `claude` CHUA_XAC_THUC (05-11 02:00Z).
  Chưa biết phiên thi công có đường Claude xác thực được hay không; không có thì dừng và hỏi (Q9).
- Thứ tự với #1187: chưa biết bên nào chạy `kiem-merge` trước. Nếu #1187 chạy trước thì kết quả của nó
  được chép vào A7 làm phép đo thứ hai, còn A13 chuẩn vẫn là A1 của packet này (Q1, Q10).
- Người giữ của `ops/land/a13-k1-canary-evidence.yaml`: chưa đo.

## Bảng quyết định (chủ kho duyệt 04→05-11-2026)

| # | câu hỏi | quyết định |
|---|---|---|
| Q1 | ai mang A13 | canary riêng, chỉ tài liệu, land đầy đủ; nếu #1187 chạy trước thì ghi thêm như phép đo thứ hai |
| Q2 | bản K1 được đo | `packet_loop.py` ghim tại `1f0941e`; master khác thì đo thêm bản master |
| Q3 | phản chứng | 1 dòng đúng, 1 dòng OID sai, 2 dòng; trên commit cục bộ H′, không đẩy |
| Q4 | bằng chứng dương | vắng dòng K1 khi có tổng kết + đo lại băm và số dòng + phản chứng đỏ; nợ dấu hiệu dương |
| Q5 | K1 đỏ oan | dừng `blocked`, ghi, chuyển #1187 hoặc mở nợ; không chèn dòng khai |
| Q6 | lớp, cổng | `routine`; K6 `not_required`; K7 không chạm; không khai `tran_*` |
| Q7 | định danh | `A13-K1-CANARY` r1, nhánh `ops/a13-k1-canary-spec`, Issue `coord:packet` + `state:proposed` |
| Q8 | diff của PR | chỉ tệp đặc tả; hồ sơ ở PR ghi sổ land riêng |
| Q9 | người làm | executor là phiên Claude Code mới; K4 do phiên Claude mới độc lập hoặc human; không nâng sang Codex |
| Q10 | thứ tự với #1187 | base là master lúc cấp lease; luôn đo bản ghim; base chứa #1187 thì đo cả hai và so |
| Q11 | r2 | tiếp thu phản biện Q2, Q3, Q5, Q6 (và ghi giới hạn Q4) theo bảng *Phản biện r1 → r2* |

## Phản biện r1 → r2 (chủ kho duyệt 05-11-2026)

r1 được gửi phản biện qua Proxima (VM `tra-luat-win`) bằng 6 câu hỏi hẹp kèm mã K1 nguyên văn; prompt
sha256 `0f763d3f85f73b8e6b74aa5313e80e149c2b227e2fbe9769c0089c82f2287b39`. Trả lời dùng được: `chatgpt:gpt-6-thinking`
(request `4ceb84d38b1041f8a52819ba48994c7e`). `gemini:3-1-pro` (request `ad5d2f16ba6f4848838f418c3f1d8523`)
chỉ trả 656 ký tự tóm tắt suy nghĩ, không trả lời câu nào; không gửi lại. Mỗi phát hiện được tiếp thu chỉ
sau khi đo lại bằng đột biến trên kho thật:

| câu | phát hiện | đo lại | thay đổi trong r2 |
|---|---|---|---|
| Q1 | không có đường K1 đạt mà không kiểm | đồng ý | không |
| Q2 | `spec_hash` toàn chữ số thập phân ⇒ YAML `int` | đúng, xác suất ~10^-13 | A2 thêm kiểm kiểu |
| Q3 | vế (i), (iii) của M10 không có phản chứng | đúng: hai đột biến sống | thêm A4b, A4c |
| Q4 | canary chỉ-đặc-tả không mất lớp lỗi K1 nào | đúng về mã; bỏ sót lớp "đặc tả vắng ở H" | thêm vào `ngoai_pham_vi` |
| Q5 | A6 tự làm xanh được bằng lời giải thích | đúng | A6 bỏ miễn trừ |
| Q6 | thiếu ca sai `spec_hash` | đúng: đột biến xoá phép so băm sống | thêm A2b |

## Chạy thử trước khi đóng băng

Kết quả chạy thử bảy ca A1/A2b/A3/A4/A4b/A4c/A5 trên commit cục bộ (không phải PR, không phải lease thật) được
ghi trong comment đóng băng trên Packet Issue, kèm lệnh và rc. Ghi ở đó thay vì ghi trong tệp này vì
kết quả phụ thuộc chính băm của tệp này.
