tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab
dieu_kien_merge: ADR-0060@36d7c5dcdcbbb27176b75135125b9009f9fe0587

# ASSURANCE-81-MODEL-EFFORT-TUY-CHON r1: model/effort phục vụ của reviewer thành trường "ghi nếu đo được"

**Trạng thái của tệp: BẢN TRÌNH DUYỆT.** Mục *Câu hỏi mở* có hai câu (Q1, Q2) mà đáp án đổi danh sách hồi tố
và đổi văn bản §8. Các mục dưới đây viết theo đáp án khuyến nghị. Chủ kho trả lời khác khuyến nghị thì
phải ra r2; không sửa đè tệp này. Lease chỉ được neo băm của tệp này khi chủ kho đã xác nhận cả hai đáp án
khuyến nghị.

## Định danh

- `packet_id`: `ASSURANCE-81-MODEL-EFFORT-TUY-CHON`; revision 1; generation dự kiến 1.
- `packet_issue`: #1240.
- Hiện vật kèm: `ops/specs/assurance-81-model-effort-tuy-chon-r1-hoi-to.py`, sha256
  `a673b35f218302c9c1c0da8f52724a4bc58585740f8b49e58b4cf8af8140536d`. Đây là bộ phân loại hồi tố (mục
  *Hồi tố*). Nó chỉ đọc, không phải deliverable của packet, và không vào write set.

## nguon_cap_viec

- Chỉ thị chủ kho ngày 05-11-2026 trong phiên điều phối `session_015GtxraXfMD1t2FJLzzGDr4`: *"điều chỉnh để
  từ sau model và effort chỉ là optional, không phải bắt buộc"* (thuật lại trong thân Issue #1240).
- Hai quyết định của chủ kho, comment
  https://github.com/ducthangho/tra-luat/issues/1240#issuecomment-6662892793: *"(a) hồi tố, (b) không bắt buộc"*.
  (b) áp cho MỌI packet, kể cả packet đòi "reviewer cùng model, effort cao hơn".
- Ba ràng buộc của phiên điều phối tổng `session_015GtxrYPjZCTZeRiazdssgq`, chuyển qua phiên điều phối ngày
  05-11: giữ nguyên `_url_hop_le` (vì #1210); không đưa `.claude/dev/packet_loop.py` và
  `.claude/dev/packet_loop_test.py` vào write set; đo danh sách hồi tố lúc cấp lease.
- Đặc tả KHÔNG phải lease. Thi công chỉ bắt đầu khi có lease còn hiệu lực neo `spec_hash` của tệp này
  (`docs/PROTOCOL_DA_PHIEN.md` §3.2, §4).

## Số đo nền (05-11-2026, 16:15–16:21Z, `origin/master` = `b255b0b7131da7f6e026639f6b0da0a06cc68a44`, kho đã unshallow)

### Chỗ đang bắt buộc model/effort

| vị trí | đọc model/effort? | đo bằng |
|---|---|---|
| `docs/PROTOCOL_DA_PHIEN.md` §8.1, dòng 760–766 | CÓ, văn bản. Câu *"Evidence fallback hoặc không đủ nhận dạng thì chưa nhận assurance"* là căn cứ của mọi hồ sơ `CHUA_DAT`. Câu *"Nếu Packet đòi reviewer cùng model nhưng effort cao hơn, phải đối chiếu…"* trái quyết định (b). | đọc tệp |
| `docs/PROTOCOL_DA_PHIEN.md` §8 mục 1 (dòng 618) | gián tiếp. `cross_approved` neo vào họ model phục vụ lượt chạy, có mức `khong_do_duoc`. 13 hồ sơ bị hạ ở r24 vì *"họ model reviewer khong_do_duoc"*. | đọc tệp + bộ phân loại |
| `docs/PROTOCOL_DA_PHIEN.md` dòng 10, 278, 499 | không bắt buộc thêm. Dòng 10 đã gán Claude Code ⇒ họ `claude`, Codex ⇒ họ `openai`. Dòng 499 viết *"model/effort quan sát được"*. | đọc tệp |
| `docs/PROTOCOL_DA_PHIEN.md` §10.2.4 (dòng 984–1057) | KHÔNG nói tới model/effort của reviewer | `rg -n -i "model\|effort"` trên dòng 984–1057: 1 dòng, là dòng 1045 (*"`land apply` … không gọi model"*), không liên quan |
| `ops/land_evidence_nguon.py` luật L7 (`L7_KHOA = ("model", "effort", "sandbox_mode")`, dòng 106, dùng ở dòng 319–320) | CÓ, **cổng máy**. Hồ sơ khai `reviewer_assurance_81: DAT` mà `thuc_thi.model` hoặc `thuc_thi.effort` không phải lời khai `measured` thì ĐỎ. | đọc mã; `ops/land_evidence_nguon.py --root .` ⇒ `96 ĐẠT · 25/28 miễn trừ · 0 vi phạm`, rc 0; test ⇒ `DOT BIEN: 106/106` |
| `ops/kiem_ho_so_land.py` (L-6) | KHÔNG. Chỉ đọc `authorized_head_sha`, `authorization_url`, khối `landed_<ngày>`. | `rg -n "model\|effort\|assurance" ops/kiem_ho_so_land.py`: 0 dòng |
| `.claude/dev/packet_loop.py` `kiem-merge` K4 (dòng 3376–3391) | KHÔNG. Đòi `head`, `trang_thai == "xong"`, `ma_thoat == 0`, `stdout_sha256`, dòng cuối `KET_LUAN: approve`. | đọc mã |
| `ops/bien_nhan_v2.py` (ADR-0050) | KHÔNG đòi model đo được. Không khai đè thì họ model lấy từ `HO_MODEL_MAC_DINH[provider]` (dòng 193, 719); chỉ chặn khi biên nhận TỰ khai mức `khong_do_duoc` (dòng 786). | đọc mã |
| `.claude/dev/launcher.py` (dòng 1831–1841) | GHI `model_phuc_vu*`, `effort_phuc_vu*`. Không đổi. | đọc mã |
| `.claude/skills/cross-review`, `land-packets`, `work-packet` | KHÔNG đòi. `$MODEL`/`$EFFORT` là cấu hình yêu cầu. | `rg -n "chưa nhận assurance\|model_phuc_vu\|effort_phuc_vu" .claude/skills`: 0 dòng |
| ngoài `ops/land`, `ops/reviews`, `ops/specs` | `rg -n "model_phuc_vu\|effort_phuc_vu\|reviewer_assurance_81\|assurance_81"` chỉ ra hai tệp: `ops/land_evidence_nguon.py` (13 dòng), `ops/land_evidence_nguon_test.py` (62 dòng) | lệnh ghi bên trái |

Kết luận: hai chỗ phải sửa là văn bản §8/§8.1 và luật L7. K4 và L-6 đã không đòi model/effort.

### Kích thước dự kiến

4 tệp, khoảng 220 dòng thêm: ADR khoảng 90, protocol khoảng 15 thêm và 8 bớt, `land_evidence_nguon.py` khoảng 20,
test khoảng 95. Trần `ADR-0053` (sensitive): ≤ 6 tệp / ≤ 450 dòng thêm. Đạt, còn dư.

### `ai-dang-giu` cho write set (16:16Z, sau khi fetch đủ ref: `comm -23` máy chủ/cục bộ = 0/747 nhánh)

| đường dẫn | kết quả |
|---|---|
| `docs/PROTOCOL_DA_PHIEN.md` | `NGƯỜI_GIỮ 1: wp1099-cloud-setup-p3b-r11-g1-claude` (nhánh `ops/cap-lease-1099-g1`, `lease_expires_at_utc: 2026-11-05T16:40:00Z`). Packet #1099 đã merge ở `b255b0b`. Lease này tự hết hạn lúc 16:40Z. |
| `docs/adr/0065-model-effort-phuc-vu-tuy-chon.md` | `NGƯỜI_GIỮ 0` |
| `ops/land_evidence_nguon.py` | `NGƯỜI_GIỮ 0` |
| `ops/land_evidence_nguon_test.py` | `NGƯỜI_GIỮ 0` |

Không nhánh nào khác dự kiến thêm `docs/adr/0065-*` (quét `docs/adr/006[5-9]*` trên mọi ref `origin/*`: 0 tệp).
Spec #1210, #1221, #1237 không đặt các đường dẫn trên vào write set; spec #1210 chỉ ĐỌC `ops/kiem_ho_so_land.py`.

## review_class

`sensitive`. Packet đổi luật assurance và một cổng land (`docs/PROTOCOL_DA_PHIEN.md` §8, `ops/land_evidence_nguon.py`),
tức *review/land authority* theo §8 (dòng 729). Approval cần đúng assurance `cross_approved` hoặc `human_audited`.

## Windows (ADR-0060 M3)

Diff không chạm đường dẫn ở bước 2, và có tệp `*.py` nên không vào bước 3. Kết quả dự kiến: `unknown` ở bước 4.
Reviewer chốt. Đề xuất `not_required`, với điều kiện A9 đạt: không dòng thêm nào trong hai tệp `*.py` chứa
`os.name`, `sys.platform`, `platform.system`, `subprocess`, `encoding=`, `os.sep`, `pathlib`. A9 đỏ thì M3 bước 2
cho `required`, và agent không được hạ.

## write_set

- `docs/adr/0065-model-effort-phuc-vu-tuy-chon.md` (mới)
- `docs/PROTOCOL_DA_PHIEN.md`
- `ops/land_evidence_nguon.py`
- `ops/land_evidence_nguon_test.py`

## ngoai_pham_vi

- **Mở lại hồ sơ land (hồi tố).** Làm ở packet riêng, sau khi packet này land. Lý do và cách chia ở mục *Hồi tố*.
- **`ops/kiem_ho_so_land.py`.** Không đọc model/effort. Giữ nguyên hành vi và chữ ký `_url_hop_le`, vì #1210
  (D1, đã duyệt, chưa land) có ca G2 nạp hàm này qua `importlib` và đòi tập URL của D1 là tập con của tập L-6
  nhận. Bất biến A8 đo việc này. Packet này không đổi tệp ấy nên không phụ thuộc thứ tự land với #1210.
- **`.claude/dev/packet_loop.py`, `.claude/dev/packet_loop_test.py`.** Đang thuộc write set #1210/#1211/#1212.
  K4 cũng đã không đòi model/effort, nên không có gì phải sửa.
- **`.claude/dev/launcher.py`.** Vẫn đo và ghi `model_phuc_vu*`, `effort_phuc_vu*` như cũ.
- **`ops/bien_nhan_v2.py`.** Đã lấy họ model từ provider khi không khai đè (ADR-0050 mục 3). Không sửa.
- **Ba hồ sơ trong `MIEN_TRU_L7`.** Giữ nguyên miễn trừ và băm. Luật mới nới L7 nên chúng không bị siết thêm.
- **Hồ sơ #1105** (`ops/land/pr1231-wp1105-land-evidence.yaml`, hiện chỉ ở nhánh `claude/ghi-so-land-1231`). Đã ghi
  `landed: true` với `reviewer_assurance_81: DAT_THEO_MIEN_CHU_KHO` theo miễn trừ riêng của chủ kho. Không viết lại.
  Bộ phân loại bỏ qua nó (`landed` khác `false`).
- **`AGENTS.md`** dòng 55, *"khai đúng model, provider, execution surface và transport thực tế"*. Không sửa. Ghi
  `KHONG_DO_DUOC` khi không đo được vẫn là khai đúng.
- **Skill adapter** (`.claude/skills/*`). Không có câu nào bắt buộc model/effort (đo ở bảng trên).

## muc_tieu

1. `docs/adr/0065-model-effort-phuc-vu-tuy-chon.md`: ADR mới, `Trạng thái: Accepted` kèm URL comment quyết định.
   Nội dung:
   - (i) model/effort phục vụ của reviewer là trường ghi nếu đo được, ở mọi packet, không ngoại lệ;
   - (ii) `KHONG_DO_DUOC` ở hai trường ấy không làm assurance §8.1 thành `CHUA_DAT` và không chặn `landed`;
   - (iii) các mốc vẫn bắt buộc: exact SHA, `ma_thoat`, `stdout_sha256`, verdict, sandbox mode;
   - (iv) theo Q1: model phục vụ không đo được thì họ model lấy theo identity provider (protocol dòng 10,
     ADR-0050 mục 3). Provider không gắn một họ duy nhất (`google_antigravity`) vẫn phải khai `model_family`;
   - (v) hồi tố theo quyết định (a), với quy tắc nhóm của mục *Hồi tố* (gồm Q2);
   - (vi) launcher không đổi.
2. `docs/PROTOCOL_DA_PHIEN.md`:
   - §8.1: viết lại đoạn dòng 760–766 theo (i)–(iii), bỏ câu *"Nếu Packet đòi reviewer cùng model nhưng effort
     cao hơn…"*, và thu hẹp câu *"Evidence fallback hoặc không đủ nhận dạng…"* về provider, execution surface,
     transport, session/run ID và sandbox;
   - §8 mục 1: thêm một câu theo (iv);
   - §20: thêm dòng `ADR-0065`, cột cổng là `ops/land_evidence_nguon.py` (L7).
3. `ops/land_evidence_nguon.py`, luật L7. Khi khai `DAT`:
   - `thuc_thi.sandbox_mode` vẫn bắt buộc là lời khai `measured`;
   - `thuc_thi.model` và `thuc_thi.effort` được vắng. Nếu có mặt thì phải là chuỗi khớp `RE_KHAI_DO` (`measured …`)
     hoặc khớp một mẫu mới cho `not_measured …`. Giá trị khác (rỗng, `DAT`, sai kiểu) vẫn ĐỎ;
   - cập nhật docstring L7 và hằng `L7_KHOA`. `MIEN_TRU_L7` giữ nguyên.
4. `ops/land_evidence_nguon_test.py`: ca hai chiều và đột biến cho mục tiêu 3 (A4–A6). Bộ đột biến hiện có vẫn
   giết hết.

## nghiem_thu

Mọi phép đo văn bản chạy trên đoạn đã nối dòng: gộp khoảng trắng trong từng đoạn, không nối qua dòng trống
(L6 b). Đoạn §8.1 là mọi dòng từ tiêu đề `### 8.1` tới tiêu đề `### 8.2`.

| # | tiêu chí | phép đo | đỏ khi / đột biến |
|---|---|---|---|
| A1 | ADR-0065 tồn tại và có trong §20 | `python3 .claude/dev/packet_loop.py adr-song --root .` rc 0; `rg -c '^\| \`ADR-0065\`' docs/PROTOCOL_DA_PHIEN.md` = 1 | Trên nền: ADR vắng ⇒ đếm 0. Đột biến: xoá dòng §20 ⇒ `adr-song` ĐỎ. |
| A2 | §8.1, vế dương | đoạn §8.1 đã nối dòng chứa đúng 1 lần mỗi cụm: `model và effort phục vụ của reviewer là trường ghi nếu đo được` · `KHONG_DO_DUOC ở hai trường này không làm assurance thành CHUA_DAT` · `exact SHA, ma_thoat, stdout_sha256, verdict và sandbox mode` (so sau khi bỏ dấu nháy ngược) | Trên nền: 0/3. Đột biến: đổi `ghi nếu đo được` thành `bắt buộc` ⇒ cụm 1 = 0. |
| A3 | §8.1, vế âm (văn bản cũ) | đoạn §8.1 đã nối dòng chứa 0 lần `Nếu Packet đòi reviewer cùng model nhưng effort cao hơn` và 0 lần `Evidence fallback hoặc không đủ nhận dạng thì chưa nhận assurance` | Trên nền: 1 và 1 ⇒ ĐỎ (đúng màu "chưa làm"). A2 chặn đường xoá trắng. |
| A4 | L7 nhận model/effort `not_measured` | ca mới: hồ sơ tạm khai `DAT`, `sandbox_mode: "measured — x.json …"` (tệp nguồn có thật), `model: "not_measured — …"`, `effort: "not_measured — …"` ⇒ 0 vi phạm L7 | Trên nền: 2 vi phạm. Đột biến m1: đưa `"model", "effort"` về lại danh sách bắt buộc ⇒ ca ĐỎ. |
| A5 | L7 nhận model/effort vắng; sandbox vẫn bắt buộc | ca (a): `thuc_thi` chỉ có `sandbox_mode` measured ⇒ 0 vi phạm. Ca (b): `thuc_thi` có model/effort measured, thiếu `sandbox_mode` ⇒ đúng 1 vi phạm có chuỗi `thuc_thi.sandbox_mode` | Đột biến m2: bỏ `sandbox_mode` khỏi khoá bắt buộc ⇒ ca (b) ĐỎ. Đột biến m1 ⇒ ca (a) ĐỎ. |
| A6 | L7 vẫn bắt giá trị rác ở model/effort | ca: `model: "DAT"` ⇒ 1 vi phạm; `effort: ""` ⇒ 1 vi phạm; `model: 5` ⇒ 1 vi phạm | Đột biến m3: chấp nhận mọi giá trị khi khoá có mặt ⇒ ca ĐỎ. |
| A7 | Cổng trên cây thật không đổi màu | `python3 ops/land_evidence_nguon.py --root .` ⇒ `0 vi phạm`, rc 0. Số `ĐẠT`/miễn trừ khớp nền (96 · 25/28) hoặc lệch có giải thích. `python3 ops/land_evidence_nguon_test.py` ⇒ `TONG: DAT`, dòng `DOT BIEN: N/N` hai số bằng nhau, N ≥ 109 (106 nền + m1–m3) | Đột biến m1–m3 phải nằm trong bảng đột biến của test và bị giết đúng lý do. |
| A8 | Bất biến `_url_hop_le` (ràng buộc #1210) | `git diff --exit-code <base>..HEAD -- ops/kiem_ho_so_land.py` rc 0; `git rev-parse HEAD:ops/kiem_ho_so_land.py` bằng blob trên base. Chạy lại cả trên head ứng viên cuối. | ĐỎ khi diff chạm tệp. Phép đo hai blob này không có đột biến riêng: nó so bằng nhau trực tiếp. |
| A9 | M3: dòng thêm trong `*.py` không chứa token nền | `git diff -U0 <base>..HEAD -- '*.py' \| rg '^\+' \| rg -c 'os\.name\|sys\.platform\|platform\.system\|subprocess\|encoding=\|os\.sep\|pathlib'` = 0 | Đột biến: thêm `encoding="utf-8"` vào một dòng test ⇒ đếm 1 ⇒ M3 thành `required`. |
| A10 | Cổng chung | `python3 .claude/dev/packet_loop.py doctrine-scan --root .` rc 0; `python3 -m ruff check --select F ops/land_evidence_nguon.py ops/land_evidence_nguon_test.py`: delta so base = 0; `python scripts/tl.py --selftest` N/N hai số bằng nhau; `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` `ok=true` (write set nằm ngoài manifest; lệnh này canh bất biến) | Các cổng này xanh sẵn trên nền; răng của chúng đến từ đột biến riêng của từng cổng. |
| A11 | ADR khai đủ (i)–(vi) | Trên ADR đã nối dòng, mỗi cụm khớp ≥ 1: `ghi nếu đo được` · `không chặn landed` · `sandbox mode` · `identity provider` · `hồi tố` · `launcher` | Trên nền: tệp vắng ⇒ ĐỎ. Đột biến: xoá câu (iv) ⇒ cụm `identity provider` = 0. |

## Hồi tố (quyết định (a))

### Bộ phân loại

`ops/specs/assurance-81-model-effort-tuy-chon-r1-hoi-to.py` (sha256 ở mục *Định danh*), chạy bằng
`python3 -I <tệp> --root <kho>`. Nó chỉ đọc.

**Tập xét:** `ops/land/*-land-evidence.yaml`, không đệ quy. Chỉ lấy hồ sơ có `landed` (ở `trang_thai_packet.landed`
nếu có khoá ấy, không thì ở mức gốc) đúng bằng `False`, và không có khối `landed_<8 số>` nào mang `landed: true`.

**Nhóm:**

- **G1 — chỉ thiếu model/effort/họ model.** Hai đường vào:
  - (r24) có `dinh_chinh_r24` với `landed_truoc: true` và `lo` bắt đầu bằng `A` (*"họ model reviewer
    khong_do_duoc"*), và không điều kiện `(n)` nào trong `landed_dieu_kien` (ngoài §8.1) mang dấu chưa đạt;
  - (gốc) `assurance_81.reviewer_assurance_81` chuẩn hoá ra `CHUA_DAT`, có tín hiệu model/effort không đo được, và
    không có lý do khác: sandbox (chỉ xét khi có `thuc_thi`), `review_exact_sha`, `snapshot_82`, điều kiện `(n)`.
- **G2 — có tín hiệu model/effort nhưng còn thiếu điều kiện khác.** Giữ nguyên.
- **G3 — không phân loại được** (KHÔNG_ĐO_ĐƯỢC): không có khối assurance xét được mà vẫn có chuỗi nói model/effort
  không đo được; hoặc cấu trúc lạ. Packet hồi tố phải đọc tay từng tệp.
- **N0 — model/effort không phải nguyên nhân.** Ngoài phạm vi.

**Đột biến của bộ phân loại** (đo 16:21Z): cho `lo` nhận cả `B` ⇒ `pr672-wp574` (lô B, human audit) rơi vào G1,
G1 13 → 14. Bộ phân loại phân biệt được lô A với lô B.

### Ảnh chụp lúc soạn (05-11-2026 16:21Z, `b255b0b`). Đây không phải danh sách hồi tố.

62 hồ sơ trong tập xét: **G1 13 · G2 6 · G3 15 · N0 28**.

- **G1 (13):** pr679-wp678 · pr779-wp775 · pr791-wp782 · pr792-wp484 · pr793-wp784 · pr800-wp794 · pr801-wp795 ·
  pr818-wp788 · pr823-wp802 · pr832-wp831 · pr836-wp812 · pr848-wp744 · pr873-wp868. Cả 13 đều đi đường r24.
  Lưu ý riêng pr792: `landed_dieu_kien` ghi *"bf10fab/288ad3e chua Codex review"* nhưng không đánh dấu điều kiện chưa
  đạt. Chủ kho đã ghi `landed: true` kèm ghi chú ấy trước r24. Packet hồi tố phải đọc lại tệp này.
- **G2 (6):** pr888-wp886 · pr907-wp906 · pr908-no-p3-spec-r4 · pr913-wp910 · pr917-wp910 · pr932-wp748-r26. Lý do
  chung: điều kiện (1), gate hậu merge chưa đủ bốn mốc §10.2.2. pr932 còn thiếu sandbox. pr913 còn thiếu (2).
- **G3 (15):** pr1046-wp1030-r6 · pr759-no-p3-ho-so · pr772-wp766 · pr846-wp845 · pr849-wp748 · pr851-wp822 ·
  pr862-wp748-r21 · pr869-wp748-r22 · pr872-wp871 · pr877-wp854 · pr880-wp878 · pr882-wp748-r23 · pr883-wp879 ·
  pr894-wp748-r24 · pr895-wp892.
- Hồ sơ #1105 chưa có trên master. Trên nhánh `claude/ghi-so-land-1231` nó mang `landed: true`, nên không vào tập xét.

Cả 13 hồ sơ G1 chỉ là G1 nếu Q1 = có. Nếu Q1 = không thì họ model vẫn bắt buộc, và lô r24 thành N0 (không được mở).
Nếu Q2 = tính sandbox vắng là thiếu thì cả 13 thành G2 (đo bằng biến thể: G1 0 · G2 19 · G3 0 · N0 43).

### Đo lúc cấp lease (ràng buộc 3 của phiên điều phối tổng)

Danh sách hồi tố chính thức đo trên `origin/master` **lúc cấp lease** của packet hồi tố, KHÔNG lấy ảnh chụp trên.
Các hồ sơ đang ghi (pr1197-wp1099, pr1231-wp1105, sắp có pr1234-wp1221 và #1237) có thể lên master giữa hai lúc.
Người cấp lease chạy bộ phân loại (băm phải khớp), ghi lệnh, OID master, giờ UTC và đầu ra JSON vào lease hoặc
comment Issue. Băm lệch, hoặc không chạy được, thì không cấp.

### Đề xuất: packet riêng, chia theo trần

- **Tách khỏi #1240.** Mở lại một hồ sơ là thêm khối `landed_<ngày>`. L-6 đòi khối ấy có
  `quyet_dinh_chu_kho.trang_thai: da_duyet` và `comment` là URL comment GitHub. Vậy mỗi lô cần một comment duyệt
  của chủ kho, và comment ấy chỉ viết được sau khi ADR-0065 đã land. Gộp vào #1240 thì vòng lặp duyệt không đóng.
- **Chia lô.** Dự kiến mỗi hồ sơ thêm 12–20 dòng. 13 hồ sơ G1 cộng hồ sơ G3 được xác nhận sau khi đọc tay vượt
  trần `ADR-0053` (≤ 6 tệp) nếu packet hồi tố là `sensitive`. Khuyến nghị: lô ≤ 6 tệp, mỗi lô một comment duyệt
  của chủ kho phủ đúng danh sách tệp của lô. Với 13 hồ sơ G1 là 3 lô. Class của packet hồi tố do đặc tả riêng của
  nó chốt theo §8, không chốt ở đây.

## hinh_dang_ke_thua

`khong_ap_dung`. Đây không phải packet khắc phục của một packet khác: nó đổi luật theo chỉ thị chủ kho. Tiền nhiệm
gần nhất về nội dung là đợt hạ cấp r24 (#748, `dinh_chinh_r24`, uỷ quyền
https://github.com/ducthangho/tra-luat/issues/748#issuecomment-6365380273). Đợt ấy là quyết định, không phải biên
nhận có bộ đếm hình dạng lỗi.

## chua_do_duoc

- Bộ phân loại đọc văn xuôi (`landed_dieu_kien`, `ly_do`) bằng regex. G1 là tín hiệu để đọc tay, không phải phán
  quyết. Packet hồi tố phải đọc từng tệp trước khi đề nghị chủ kho duyệt.
- Với lô r24, chưa đo việc lượt review của từng hồ sơ có provider đúng là Codex hay Claude Code, tức có gán được
  họ model theo dòng 10 không. Packet hồi tố phải đọc biên nhận từng hồ sơ.
- `ai-dang-giu` trên `docs/PROTOCOL_DA_PHIEN.md` cho `NGƯỜI_GIỮ 1` tới 16:40Z hôm nay. Phải đo lại lúc cấp lease.
- Q1, Q2 chưa có đáp án. Xem mục dưới.

## Câu hỏi mở cho chủ kho

**Q1 — Họ model khi model phục vụ không đo được.** §8 mục 1 neo `cross_approved` vào họ model đã phục vụ lượt
chạy. 13 hồ sơ (lô r24) bị hạ chỉ vì *"họ model reviewer khong_do_duoc"*. Nếu model là tuỳ chọn mà họ model vẫn
bắt buộc đo, thì một lượt Codex không đo được model sẽ không bao giờ thành `cross_approved`, và (b) chỉ có trên giấy.

➡️ Khuyến nghị: **có.** Model không đo được thì họ model lấy theo identity provider: Claude Code ⇒ `claude`,
Codex ⇒ `openai` (protocol dòng 10, ADR-0050 mục 3, `ops/bien_nhan_v2.py` đã làm vậy). `google_antigravity` và
provider nhiều họ khác vẫn phải khai `model_family`.

**Q2 — Hồ sơ từ trước khi có luật sandbox.** L7 (đòi `sandbox_mode`) có từ 27-10-2026. Lô r24 được ghi trước đó
và không có trường sandbox nào.

➡️ Khuyến nghị: **không tính sandbox vắng là thiếu ở hồ sơ không có khối `thuc_thi`.** Lý do: lúc hạ cấp r24,
nguyên nhân duy nhất là họ model. Thêm điều kiện sandbox cho các hồ sơ ấy là siết hồi tố, trong khi quyết định (a)
là nới hồi tố. Hồ sơ đã có `thuc_thi` vẫn bị đòi sandbox. Bộ phân loại đã viết theo khuyến nghị này.

Hai câu này quyết định lô r24 có được mở lại không. Phần còn lại của đặc tả không phụ thuộc chúng, trừ câu (iv)
của ADR và câu §8 mục 1.
