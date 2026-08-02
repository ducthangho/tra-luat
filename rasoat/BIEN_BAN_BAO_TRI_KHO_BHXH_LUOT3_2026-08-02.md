# BIÊN BẢN — lượt bảo trì kho BHXH, LƯỢT 3 (02-08-2026)

Phạm vi lượt này = **đúng hai việc bàn giao** của prompt lượt 3: **VIỆC 3** (khiếm khuyết THẬT chưa
xử) và **VIỆC 4** (hai việc sổ sách). VIỆC 1 và VIỆC 2 đã đóng ở lượt 2 — **không đụng lại**.

Cây: worktree sạch `D:\Quốc hội\luot3_wt`. Land ở **r325 / v1.36.57**.

---

## 0. ★ KẾT QUẢ QUAN TRỌNG NHẤT: VIỆC 3 bị PHIÊN KHÁC làm TRƯỚC và làm RỘNG HƠN — tôi GỠ bản trùng

Tôi đã vá xong VIỆC 3 và đo trọn (số đo giữ ở §1 vì nó vẫn là bằng chứng độc lập). Nhưng khi đo lại
`origin` **ngay trước lúc commit** — đúng luật thường trực `kiem-trung-truoc-khi-commit` — thì:

* `origin/master` đã nhảy lên `e8134a2` = **r322/v1.36.54** (RAS-18, land GIỮA phiên tôi đang làm);
* và **PR #18 đang MỞ**: `r323 (v1.36.55) — khối đuôi VBHN đọng trong THÂN ĐIỀU CUỐI`, nhánh
  `claude/r323-tach-duoi-vbhn`, tạo lúc 16:34Z — **cùng khuyết tật, phạm vi RỘNG HƠN**.

**Mở diff của họ ra đo, không tin mô tả** — bản của họ tốt hơn ở hai điểm cụ thể:

1. Họ tách **CẢ bảng «XÁC THỰC VĂN BẢN HỢP NHẤT»**, tôi chỉ tách khối `[n]`. Chính đầu ra của tôi
   chứng minh tôi còn sót: thân Điều 79 của `89-2026` sau bản vá của tôi vẫn là
   `«Điều 79. Quy định chi tiết … XÁC THỰC VĂN BẢN HỢP NHẤT / CHỦ NHIỆM / Lê Quang Mạnh»`
   = **150 ký tự**, trong khi quy phạm thật chỉ **94** (số của họ).
2. Họ đo được `[n]` xuất hiện **inline trong 9/141 Điều** của `19-2026`. Phép đo của tôi ra
   **0 inline** vì tôi đo trên **thân Điều đã qua đường nạp** (đã bóc `[[n]](url)`), không phải trên
   `raw`. ⇒ tiền đề hiệu chỉnh neo của tôi hẹp hơn thực tế.

⇒ **GỠ TRỌN bản vá trùng của tôi**: `verify_deep.chu_thich_start`/`extract_chu_thich`/`CHU_THICH_PAT`,
nhánh trong `normalize_document`, 3 ca test, và đoạn thêm vào `DOCTRINE_APPENDIX.md`.
Cùng doctrine với `c2971dd` («GỠ bản vá TRÙNG của tôi — phiên khác đã vá cùng lỗi, và tốt hơn»).

**Cái tôi GIỮ LẠI là phần họ KHÔNG làm** — xem §2.

---

## 1. Số đo VIỆC 3 (giữ lại làm bằng chứng độc lập, dù bản vá đã gỡ)

Prompt lượt 3 nêu 2 record (19-2026, 89-2026). Đo trên **cả 11 record cache đang phục vụ** thì có
**3 record dính**, và record thứ ba **chưa từng được nêu trong bất kỳ prompt/sổ nào**:

| record | Điều cuối | thân | khối đuôi | tỷ lệ |
|---|---|---|---|---|
| 19-2026-vbhn-vpqh | Điều 141 | 8.573 | 4.014 | 46,8% |
| **40-2026-vbhn-vpqh** | **Điều 52** | **40.637** | **40.349** | **99,3%** |
| 89-2026-vbhn-vpqh | Điều 79 | 1.124 | 973 | 86,6% |

8 record còn lại: **0 dính**. Kết luận này **khớp độc lập** với bảng của PR #18 (họ đo
40.406/40.637 vì tách thêm khối xác thực) — hai phép đo riêng, cùng kết luận, kể cả việc
`40-2026` là record nặng nhất.

Phụ trợ đã đo: khối chú thích chứa **0** heading `Điều N.` mà `ART_SPLIT` bắt được ⇒ **không** đẻ
Điều MA; dãy Điều 1..N của cả 3 record **không đứt** ⇒ bản vá (dù của ai) **không đổi số Điều**.

---

## 2. r325 — LỖ CÒN LẠI SAU r323, phần PR #18 KHÔNG làm ✅ ĐÃ VÁ

### 2.1 Lỗ

PR #18 tách hai khối đuôi ra `xac_thuc`/`chu_thich` nhưng **không đụng**
`scripts/tl_core/extract_cache.py`. Đã kiểm bằng cách **đọc thẳng tệp trên nhánh của họ**
(`git show FETCH_HEAD:scripts/tl_core/extract_cache.py`), không suy từ danh sách tệp:
`_consolidated_text` của họ vẫn chỉ nối `khoi_dau + articles + phu_luc`.

Mà đó là đường **dựng lại TOÀN VĂN từ record** — nuôi `doc-text` mặc định và **ghi đè khoá cache
chuẩn `extract_<id>.txt`** (nguồn nuôi corpus/NLM). Tách ra trường riêng mà không nối lại ở đó =
**im lặng đánh rơi** — **ĐÚNG BẪY r215** đã trả giá với `phu_luc` (khi đó mất 6.030 ký tự phụ lục mà
record VẪN CÓ lưu, và mất luôn khối đầu ⇒ «văn bản không có danh tính»).

Quy mô nếu để nguyên: `40-2026` mất **40.406 ký tự** chú thích; và `xac_thuc` chính là **bằng chứng
danh tính** (VPQH + «Số:») — thứ mà r215 sinh ra để bảo vệ.

### 2.2 Vá

`_consolidated_text` nối lại **cả hai** khối, thứ tự theo bố cục đo được (phụ lục → **xác thực** →
**chú thích**); `rep` thêm hai cờ; dòng nhãn `doc-text` khai thêm «xác thực»/«chú thích».

★**Forward-compatible, KHÔNG phụ thuộc thứ tự merge**: record dựng trước r323 không có hai khoá ⇒
cả hai rỗng ⇒ chuỗi ra **Y HỆT** bản cũ. An toàn kể cả khi r323 không bao giờ land.

Ca khoá `r325_dung_lai_khong_danh_roi_duoi_vbhn` — 5 vế: nối đủ + đúng thứ tự · không mất ký tự ·
**chiều ngược** record-cũ-bất-động · khoá rỗng không đẻ dấu nối thừa · chỉ có MỘT trong hai khối.

---

## 3. VIỆC 4.2 — WARN LOUD khi `--profile` ≠ nền mà `registryDocId` rỗng ✅ ĐÃ VÁ

### 3.1 Lỗ đúng ở đâu

Bàn giao mô tả chính xác: `reg-query` đã trả `scope` + cờ `BASE_SCOPE_HIT` (r179 T7), nhưng cờ đó
chỉ nói được **khi đã có dòng trả về**. Ca chết lặng là: profile **có thật** trong config mà
`registryDocId` **rỗng** ⇒ `_apply_profile_env` không đặt `TL_REGISTRY_DOC_ID` ⇒ webapp `regSS_` rơi
nhánh auto-discover = **sổ NỀN**, và người dùng đọc thấy dòng nền dưới nhãn profile đang chọn mà
không hề biết `--profile` đã thành NO-OP.

Đường **GHI** đã fail-closed từ **1.23.21** (`PROFILE_REGISTRY_ID_EMPTY_WOULD_CLOBBER_BASE`, rc=2) —
bản vá cho đúng sự cố 2026-06-30. Đường **ĐỌC** tới nay vẫn im.

### 3.2 Bản vá

`_apply_profile_env` in `PROFILE_REGISTRY_ID_EMPTY` ra **stderr**, nêu đích danh profile + sổ nền sẽ
bị rơi về + cách sửa. **Chỉ cảnh báo, không chặn** (đọc trên sổ nền là hợp lệ; cái sai là làm nó im
lặng). Ồn **1 lần / profile / process**.

Ba chiều ngược cố ý giữ IM: nền `vbqppl` để rỗng là **bình thường** (webapp tự tìm Sheet theo tên) ·
profile có `registryDocId` đủ · người dùng tự `export TL_REGISTRY_DOC_ID`. Không chồng lên
`PROFILE_NOT_FOUND`.

### 3.3 Chứng minh trên ĐƯỜNG SẢN XUẤT (không chỉ qua bind)

Dựng config tạm 3 profile rồi chạy `tl --config … --profile … profile-info --json` thật:

```
p_thieu_registry → [tl] ⚠ PROFILE_REGISTRY_ID_EMPTY: profile 'p_thieu_registry' KHÔNG có
                   `registryDocId` ⇒ mọi lệnh ĐỌC registry rơi về SỔ NỀN 'vbqppl' …
p_du_registry    → im
vbqppl (nền)     → im
```

6 ca khoá: `r325_warn_khi_registry_id_rong` · `r325_du_registry_id_thi_im` ·
`r325_nen_rong_khong_bao` · `r325_khong_chong_profile_not_found` ·
`r325_env_nguoi_dung_dat_thi_im` · `r325_warn_chi_mot_lan`.

---

## 4. VIỆC 4.1 — đính chính §4.2 biên bản lượt 1 ✅ ĐÃ GHI

Đã chèn khối **⛔ ĐÍNH CHÍNH** ngay dưới tiêu đề §4.2 của
`rasoat/BIEN_BAN_BAO_TRI_KHO_BHXH_2026-08-02.md`.

### 4.1 Đo lần ba ĐỘC LẬP — xác nhận đính chính, và bắt được MẪU SỐ SAI của cả hai sổ trước

Tệp 89-2026 **vẫn còn** ở `C:\Users\admin\Downloads\89_VBHN-VPQH_699557.docx`. sha256
`f84637a1…8573234` **khớp tuyệt đối** `source.sha256` của record cache đang phục vụ ⇒ đúng tệp đã nạp:

```
tổng entry            : 10
entry có backslash    :  0      ← lượt 1 khai 30
word/document.xml     : có      ← lượt 1 khai KHÔNG có
python-docx mở thẳng  : OK, 775 đoạn
```

⇒ đính chính **được xác nhận độc lập**, không chỉ chép của lượt 2.

★ **Nhưng mẫu số của CẢ HAI sổ trước đều sai**: lượt 1 «30/**37**», lượt 2 «0/**37**» — tệp này chỉ
có **10** entry. Con số `/37` **không đến từ tệp này**. Giả thuyết khớp với kết luận «hỏng ở đường
tải»: lượt 1 đo trên tệp lấy qua **đường tải container web** (tệp KHÁC, 37 entry), lượt 2 đo đúng
tệp lành nhưng **bê nguyên mẫu số 37** ⇒ ra «0/37». Không chứng minh được vì tệp hỏng kia không còn.
**Số đáng tin duy nhất: 0/10.** Vế «0/40» của 19-2026/40-2026 vẫn **chưa** có phép đo độc lập.

★Đo bằng tệp `.py` + `chr(92)` — truyền backslash qua `bash -c` bị nuốt, đúng cái làm lượt 1 sai.

**Cái KHÔNG bị đính chính:** nửa sau tiêu đề (`scan_file` fail-open) là khuyết tật THẬT, độc lập —
**bản vá r316 giữ nguyên, vẫn đúng vì lý do riêng của nó**.

---

## 5. Bẫy đã dính trong lượt này (ghi để lượt sau không trả giá lại)

1. ★★ **`Path.write_text()` trên Windows DỊCH `\n` → `\r\n`.** Dùng nó để sửa MỘT dòng ⇒ cả tệp đổi
   kết dòng, `git diff` **1.061 dòng** thay vì 45, mà CI có bước *«Force LF checkout (hash parity với
   manifest)»*. Phát hiện vì diff-stat vô lý, không phải vì công cụ báo. **Sửa tệp mã bằng
   `write_bytes`**, hoặc `open(..., newline="")`.
2. ★★ **Kho này kết dòng TRỘN THEO TỆP** — `verify_deep.py`/`extract_cache.py`/`profile_env.py`/
   `CHANGELOG.md` là **LF**, còn `tl_selftest.py`/`tl.py`/`SKILL.md` là **CRLF**. Quy tắc «ép hết về
   LF» là **SAI** và tự nó đẻ ra diff 55.797 dòng. Đúng: nắn theo **blob của chính tệp đó**
   (`git show HEAD:<f>` rồi so đa số CRLF/LF).
3. **`VERSION` khai ở BA nơi**: `VERSION` · `scripts/tl.py:104` · `SKILL.md` dòng 18. Quên một chỗ
   thì `r65_bundle_export_meta_and_guard` (đòi `version_forked == VERSION`) và
   `skill_md_version_matches_VERSION` bắt — nhưng chỉ khi CHẠY selftest, gate khác im.
4. **nbsp nguyên literal trong mã nguồn là ký tự VÔ HÌNH** — dùng escape `\u00a0` tường minh.
5. **Số tuyệt đối của ruff vô nghĩa ở kho này** (4.665 finding có sẵn) và **CI KHÔNG chạy ruff**
   (không config, không step). Phải so **DELTA theo TỆP + THEO MÃ LỖI**.
6. **Không so số ca selftest GIỮA HAI CÂY**: cây canonical và worktree cho tổng khác nhau vì một số
   ca đăng ký theo điều kiện môi trường. Baseline phải đo **trong chính cây đang sửa**.
7. ⚠ **`git stash` + selftest trong MỘT lệnh = mất việc khi timeout**: selftest ở máy này có bước
   retry mạng (backoff 1,5s→15s) nên có lượt vượt 10 phút; lệnh bị cắt SAU `stash push` mà TRƯỚC
   `stash pop` ⇒ toàn bộ thay đổi nằm trong stash. Chạy selftest **nền**, đừng ghép với stash.

---

## 6. Trạng thái đóng

* VIỆC 3: **đóng bằng cách nhường** cho PR #18 (rộng hơn) + **bù đúng lỗ họ để lại** (r325 §2).
* VIỆC 4.1 và VIỆC 4.2: **đóng**.

## 7. Còn nợ NGƯỜI

1. ★ **Thứ tự merge — BA nhánh cùng đợt**: PR **#18** = `r323/v1.36.55` · PR **#19** =
   `r324/v1.36.56` (`claude/rel05-nlm08`, REL-05+NLM-08) · nhánh này = `r325/v1.36.57`.
   Theo luật «bản số THẤP merge trước rồi rebase bản cao lên»: **#18 → #19 → nhánh này**.
   Bản vá §2 **không hỏng** nếu thứ tự ngược lại (hai khoá vắng ⇒ no-op), chỉ là chưa có tác dụng.
   ★**Số bị chiếm HAI LẦN trong một phiên**: tôi đặt `r322` lúc đầu (khi còn trống) → bị PR #17
   chiếm; đổi sang `r324` → bị PR #19 chiếm lúc 18:00Z; chốt `r325`. **`git fetch` + `gh pr list
   --state open` phải chạy NGAY TRƯỚC `git add`** — PR đang mở chiếm số mà `git log origin/master`
   KHÔNG thấy.
2. **Nạp lại 3 record VBHN** (19-2026 · 40-2026 · 89-2026) sau khi r323 land, để `xac_thuc`/
   `chu_thich` được tách trong cache đang phục vụ. Bản vá chỉ đổi **đường nạp**; record cũ giữ
   nguyên tới khi ingest lại. Không tự chạy vì đó là ghi vào kho dữ liệu thật.
3. **Vế 19-2026/40-2026 của đính chính §4.2** («0/40») vẫn chưa có phép đo độc lập — tệp tạm
   `tra_luat_ingest_*.docx` đã mất.
4. Nếu muốn bỏ 1 dòng nhãn mục ở khối đầu `54-2025`: đi nguồn `.doc`/`.docx` Công báo, **không**
   dùng PDF — và phải quyết `method_rank 95→50` trước (nguyên văn kết luận lượt 2, chưa đụng).
