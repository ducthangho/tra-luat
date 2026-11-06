# Đặc tả packet `LAUNCHER-READONLY-IGNORED` r1: `launcher.py run --chup-workspace` chụp sha256 toàn workspace trước/sau lượt chạy

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab
dieu_kien_merge: ADR-0060@36d7c5dcdcbbb27176b75135125b9009f9fe0587
windows: required

| trường | giá trị |
|---|---|
| packet_id | `LAUNCHER-READONLY-IGNORED`, revision 1, generation 1 |
| packet_issue | #1252 |
| nguon_cap_viec | Issue #1252 (nợ mở từ connector P1 [4485646628](https://github.com/ducthangho/tra-luat/pull/1251#discussion_r4485646628) trên PR #1251). Ngày 06-11-2026 ~05:58Z, chủ kho chọn *"Soạn spec ngay (Khuyến nghị)"* qua câu hỏi của phiên `session_015GtxraXfMD1t2FJLzzGDr4`. Vòng câu hỏi Q1–Q9 được trả lời ~06:10Z, nguyên văn *"Theo khuyến nghị"* |
| review_class | `sensitive`: diff chạm `.claude/dev/**`, tức bằng chứng assurance của lượt review (§8.2) |
| base | `origin/master` lúc cấp lease. Lúc soạn đo được `12e5b36` (06:06Z 06-11) |
| depends_on | không có. Lúc soạn (06:00Z và 06:03Z 06-11) không lease nào giữ hai tệp đích, xem §3 |
| executor | `anthropic_claude`: Claude Code remote chạy Linux, cộng máy Windows của chủ kho qua Desktop Commander cho A10 |
| reviewer | `openai_codex` chạy offline qua `launcher.py run`, neo SHA ứng viên (`ADR-0060` M12), cộng connector `@codex review` trên PR draft |

## 1. Vì sao: số đo

| # | sự kiện | số đo | đơn vị / thời điểm |
|---|---|---|---|
| S1 | lượt review offline 4 của #1224 (run `a8d7350a`, head `4dc4fe9`) ghi vào workspace | reviewer tự khai đã cập nhật **11** tệp ignored; `run.json` vẫn ghi `worktree_sach: true` và mọi bộ đếm `sandbox_lech` = 0 | đơn vị: TỆP; theo nội dung Issue #1252 |
| S2 | lượt review offline 1 của #1240 (run `bc004964`, head `ecd3073`) ghi vào workspace | **20** tệp ignored; lượt bị loại khỏi hồ sơ land | đơn vị: TỆP; hồ sơ `ops/land/pr1249-wp1240-land-evidence.yaml` |
| S3 | `launcher.py run` hiện chỉ đo trạng thái worktree ở MỘT mốc, TRƯỚC khi sinh tiến trình con | `chay_cac_chot` gọi `chot_sach` (tức `git status`) một lần rồi ghi `worktree_sach`; sau khi con thoát không đo lại; tệp ignored và `.git` không nằm trong phép đo | đọc `.claude/dev/launcher.py` trên `12e5b36`, 06:03Z |
| S4 | hai lượt thay thế (#1224 l5 `4e47e737`, #1240 l2 `7801b46a`) chỉ được nhận nhờ phiên điều phối TỰ chụp sha256 toàn cây trước và sau | diff 0 dòng ở cả hai lượt; hiện vật ở `ops/land/pr1230-wp1224-provenance/review-offline-l5/` và `ops/land/pr1249-wp1240-provenance/review-offline-l2/snapshot-{truoc,sau,diff}.txt` | đơn vị: LƯỢT |
| S5 | chi phí một lần chụp, bộ đệm ẤM | clone mới `12e5b36`: **12.707** tệp, **400.818.299** byte (gồm `.git`, không có tệp ignored) ⇒ **0,65 s** và **0,67 s** ở hai lần chạy liền | đơn vị: TỆP, BYTE, GIÂY; đo ~06:16Z 06-11; lệnh, rc và output: `ops/specs/launcher-readonly-ignored-r1-do/` (`do_s5.py`, `s5-out.txt`) |
| S5b | chi phí một lần chụp, bộ đệm LẠNH | chưa đo được: không xoá được bộ đệm trang trong container. Một lần đo tay lúc soạn trên checkout phiên soạn (17.437 tệp, 474 MB, có tệp ngoài kho) ra ~23 s, nhưng không lưu hiện vật ⇒ **chưa xác minh**, chỉ để định hướng | xem §6 |
| S6 | lệnh git chỉ đọc có ghi lại `.git/index` hay không | clone mới `12e5b36`, sau `sleep 2`: 6 lệnh (`git status --short`, `git log --oneline -3`, `git diff --stat HEAD~1 HEAD`, `git show --stat HEAD`, `git rev-parse HEAD`, `git ls-files -s README.md`) đều rc 0 và **không** đổi sha256 của `.git/index`. Sau khi `touch -m` một tệp tracked, `git status --short` **có** ghi lại `.git/index` (băm đổi `a04e4ee2…` ⇒ `e01b530f…`), dù nội dung tệp không đổi | đơn vị: LỆNH; đo ~06:17Z 06-11; `ops/specs/launcher-readonly-ignored-r1-do/` (`do_s6.sh`, `s6-out.txt`). Bản trước của dòng này khai ngược ("touch rồi chạy vẫn không đổi"), không có hiện vật; đã rút |

Hệ quả: theo §8.2 protocol, read-only phải chứng minh bằng snapshot đầu/cuối gồm tệp ignored. Hiện việc chụp
này do người làm bằng tay, và đã hai lần nó là thứ duy nhất bắt được một lượt ghi vào checkout.

S6 chỉ phủ 6 lệnh git chỉ đọc trên Linux. Từ S6 KHÔNG suy ra được "mọi lệnh git chỉ đọc đều không ghi `.git`".
Thứ S6 cho thấy là: `git status` làm mới bộ đệm stat trong `.git/index` khi mtime của một tệp tracked đổi. Vì vậy
§2.3 đòi bộ đệm ấy đã được làm mới TRƯỚC mốc chụp đầu; `chot_sach` của launcher đã làm việc này.

## 2. Thay đổi

### 2.1 Cờ mới (Q2)

`launcher.py run` nhận thêm cờ `--chup-workspace` (mặc định TẮT). Khi tắt, mọi hành vi và mọi khoá của `run.json`
giữ nguyên như base, trừ khoá `chup_workspace` được ghi `false` (A7). Bắt buộc dùng cờ này cho lượt review là việc
của một packet khác (§5).

### 2.2 Phạm vi chụp (Q3)

Một bản chụp là danh sách đã sắp xếp theo đường dẫn. Mỗi phần tử có dạng `(đường dẫn tương đối POSIX, loại, giá trị)`,
áp cho mọi mục dưới `kq["workspace"]`:

- loại `F` (tệp thường): giá trị là sha256 của nội dung. Đọc theo khối, không đi theo symlink;
- loại `L` (symlink): giá trị là sha256 của chuỗi đích (`os.readlink`). Không đi vào đích;
- loại `D` (thư mục, kể cả thư mục rỗng): giá trị rỗng;
- loại `?` (không đọc được, ví dụ `PermissionError`, hoặc tệp biến mất giữa lúc liệt kê và lúc đọc): giá trị là tên
  lớp ngoại lệ. Có ≥ 1 phần tử `?` thì bản chụp ấy `khong_do_duoc` (§2.4).

Gồm cả `.git/**`, tệp untracked và tệp ignored. Loại trừ **đúng một** cây con: `--run-root` đã `resolve()`, khi nó
nằm trong workspace, vì chính launcher ghi `run.json`, log và bản chụp prompt vào đó. Ngoài ra không loại trừ gì,
kể cả `__pycache__`, `.ruff_cache` hay `.pytest_cache`: §8.2 đòi các thứ đó nằm ngoài checkout.

Băm bản chụp (`snapshot_*_sha256`) là sha256 của **biểu diễn chuẩn**. Mỗi phần tử là đúng một dòng, sinh bằng
`json.dumps([loai, gia_tri, duong_dan_hex], separators=(",", ":"))` cộng `"\n"`, mã hoá UTF-8:
- `duong_dan_hex` là `os.fsencode(duong_dan_tuong_doi).hex()`, với dấu phân cách là `/` trên mọi nền. Mọi đường
  dẫn đều mã hoá hex theo MỘT quy tắc, không có nhánh "đường dẫn UTF-8 hợp lệ thì ghi chữ". Như vậy tên chứa xuống
  dòng, tab, hay trùng chữ với một tiền tố nào đó đều không thể sinh cùng dòng với một tên khác;
- các dòng sắp theo byte của đường dẫn (`bytes.fromhex(duong_dan_hex)`).

Biểu diễn chuẩn được sinh bởi một hàm thuần (không đọc hệ tệp) nhận danh sách phần tử. Cả bộ ghi tệp chụp, phép băm
và phép so `tep_doi` đều đi qua đúng hàm ấy. Trong `tep_doi`, `duong_dan` là `os.fsdecode(bytes)` để người đọc được.

### 2.3 Thời điểm chụp và phép chứng minh cây đã chết

- **Làm mới bộ đệm stat (S6):** không thêm bước riêng. `chay_cac_chot` đã LUÔN gọi `chot_sach`, tức
  `git status --porcelain=v1 --untracked-files=all`, kể cả khi không bật `--require-clean`
  (`launcher.py:1347–1355, 1399–1400` trên `12e5b36`). Lệnh ấy làm mới bộ đệm stat trong `.git/index` trước mốc
  chụp đầu (connector review lượt 2, P2 `4489640552`, đo trên Linux/Git 2.43.0). Packet này KHÔNG được đổi `chot_sach`
  sang chế độ không ghi index (ví dụ `--no-optional-locks`) và KHÔNG được dời mốc chụp đầu lên trước `chay_cac_chot`;
  A17 khoá cả hai.
- **Trước:** sau mọi chốt và mọi probe (`chay_cac_chot`, `chay_cac_probe`), sau khi đã ghi bản chụp prompt, ngay
  trước `subprocess.Popen`.
- **Sau:** sau khi con thoát và sau `sandbox.ket_thuc` / `bo_loc.ket_thuc`, trước khi chốt `trang_thai`.

Mốc sau chỉ có giá trị khi đã **chứng minh** không còn hậu duệ nào sống. Phép chứng minh theo nền:

| nền | đã chứng minh cây chết khi | nguồn trong `launcher.py` |
|---|---|---|
| Linux, Darwin | `_thanh_vien_nhom(p.pid) == []` | hàm đã có, dùng cho xoá bản chụp prompt |
| Windows | `job is not None` **và** `_pid_trong_job(job) == []` | `_job_windows`, `_pid_trong_job` đã có |
| nền khác, hoặc mọi trường hợp còn lại (kể cả `None` = không đo được, `job is None`) | không bao giờ | |

`p.poll() is not None` (tiến trình mẹ đã thoát) KHÔNG phải bằng chứng. Chưa chứng minh được thì vẫn chụp, nhưng kết
quả so là `khong_do_duoc` với lý do `cay_chua_chung_minh_chet`.

Giới hạn đã biết của phép chứng minh, khai trong `snapshot_gioi_han` (§2.4): trên POSIX, cháu tự `setsid()` đã rời
nhóm tiến trình nên `_thanh_vien_nhom` không thấy; trên Windows, cháu sinh ra trước lúc con được gán vào job thì
nằm ngoài job (khe đã ghi ở docstring `_job_windows`).

### 2.4 Kết quả so và trạng thái (Q4, Q5)

`run.json` có thêm các khoá sau. Khi bật cờ, các khoá luôn có mặt, kể cả khi sạch:

| khoá | giá trị |
|---|---|
| `chup_workspace` | `true` (bật cờ) hoặc `false` (không bật cờ; khi đó không có khoá nào khác trong bảng này) |
| `snapshot_truoc_sha256`, `snapshot_sau_sha256` | 64 hex, hoặc `null` nếu lần chụp ấy ném lỗi |
| `snapshot_so_muc` | `{"truoc": int, "sau": int}` |
| `snapshot_ket_qua` | `sach` · `ghi_workspace` · `khong_do_duoc` |
| `snapshot_ly_do` | `null` khi `sach`; khi khác `sach` là một chuỗi trong tập cố định: `tep_doi`, `muc_khong_doc_duoc`, `cay_chua_chung_minh_chet`, `chup_loi` |
| `tep_doi` | danh sách tối đa **50** phần tử `{"duong_dan": str, "doi": "them"\|"xoa"\|"sua"\|"doi_loai"}`, sắp theo đường dẫn |
| `tep_doi_tong` | int: tổng số đường dẫn đổi, không bị cắt |
| `tep_doi_bi_cat` | bool: `tep_doi_tong > 50` |
| `snapshot_gioi_han` | câu cố định chứa nguyên văn hai cụm `chi so hai moc truoc/sau; ghi roi hoan nguyen giua hai moc thi khong thay` và `chau tu setsid hoac sinh truoc khi gan job thi khong chung minh duoc` |

Danh sách đầy đủ của hai bản chụp được ghi vào `snapshot-truoc.txt` và `snapshot-sau.txt` trong thư mục lượt chạy,
quyền `0600`, đúng dạng biểu diễn chuẩn ở §2.2. Băm `snapshot_*_sha256` phải bằng sha256 của đúng tệp tương ứng.

Thứ tự phân loại:
1. có lần chụp lỗi ⇒ `khong_do_duoc` / `chup_loi`;
2. chưa chứng minh được cây đã chết (§2.3) ⇒ `khong_do_duoc` / `cay_chua_chung_minh_chet`;
3. có phần tử `?` ở bất kỳ bản chụp nào ⇒ `khong_do_duoc` / `muc_khong_doc_duoc`;
4. hai bản chụp khác nhau ⇒ `ghi_workspace` / `tep_doi`;
5. còn lại ⇒ `sach`.

Tác động lên `trang_thai` và mã thoát chỉ xảy ra khi `trang_thai` lẽ ra là `xong`; `qua_han`, `bi_ngat`, `da_dung`
giữ nguyên và chỉ ghi thêm các khoá ở bảng trên:

| `snapshot_ket_qua` | `trang_thai` | mã thoát của launcher |
|---|---|---|
| `sach` | `xong` | như base (mã của con, chuẩn hoá vào 0..255) |
| `ghi_workspace` | `ghi_workspace` | **16** (`MA_GHI_WORKSPACE`, mới) |
| `khong_do_duoc` | `khong_do_duoc_workspace` | **17** (`MA_KHONG_DO_WORKSPACE`, mới) |

`ma_thoat` trong `run.json` vẫn là mã THẬT của con. Hai hằng mới được thêm vào bảng mã thoát ở đầu tệp và vào
`--help`. Khi chọn số, đo trên base: không hằng `MA_*` nào đang dùng 16 hay 17 (lúc soạn: dãy dùng là 0, 2–15,
124, 125).

## 3. Write set

```yaml
write_set:
  - .claude/dev/launcher.py
  - .claude/dev/launcher_test.py
  - ops/handoff/wp1252-g1-claude.md
```

Ba tệp. `ops/handoff/wp1252-g1-claude.md` chỉ sống trên nhánh lease/handoff, không vào diff PR (diff PR: 2 tệp).
`launcher_test.py` đã có trong sổ đăng ký `.claude/dev/ci_dang_ky_test.py`: không thêm tệp test, không chạm sổ.

Xung đột đo lúc soạn, bằng `ops/lease_publish.py ai-dang-giu` sau khi fetch `+refs/heads/*` và dọn nhánh cục bộ
tụt sau: 06:03Z 06-11 `.claude/dev/launcher.py` ⇒ `NGƯỜI_GIỮ 0`, `.claude/dev/launcher_test.py` ⇒ `NGƯỜI_GIỮ 0`.
Phiên điều phối đo độc lập lúc 06:00Z, cùng kết quả. Phiên cấp lease phải đo lại.

```yaml
nang_tran:
  ai_nang: ducthangho   # chủ kho; Q6 vòng 1 phiên soạn 06-11-2026, nguyên văn "Theo khuyến nghị"
  can_cu: >-
    Ước tính lúc soạn: launcher.py khoảng 250 dòng thêm (hàm chụp, hàm so, ghép vào lenh_run, hai mã thoát, cờ),
    launcher_test.py khoảng 350 dòng thêm (năm ca A2–A6, ca A7, đột biến cho từng vế). Tổng khoảng 600, vượt 450.
    Tiền lệ cùng hai tệp: #1105 r3 land ở +525/-18 trên 2 tệp (fe84620), trần nâng lên 850.
    Không tách được: tách chốt khỏi phản chứng là land một chốt chưa có răng.
  tran_cu: "ADR-0053@8ab1007: <= 6 tệp / <= 450 dòng thêm"
  tran_moi: "<= 2 tệp trong diff PR / <= 800 dòng thêm"
```

Trần lời gọi Codex: dòng khai `ADR-0055` ⇒ trần **10**. Ngân sách mềm như #1105 (Q8): dùng tối đa **4**. Hai lượt
liên tiếp chưa approve ⇒ Review Rescue Checkpoint (`ADR-0037`), hỏi chủ kho trước lời gọi kế tiếp. Lượt bị cắt sau
khi đã sinh output vẫn tính một lời gọi.

## 4. Nghiệm thu (mỗi dòng: phép đo, nền, và đột biến làm nó ĐỎ)

Tên ca mới mang tiền tố `r1252_`; tên dưới đây là bắt buộc. "Đột biến" là mục mới trong `DOT_BIEN` của
`launcher_test.py`, chạy bằng `--dot-bien`, và phải giết ĐÚNG ca đích (tín hiệu `TinHieuChotCa` của ca đó, không
phải lỗi vô can). Mọi ca dưới đây chạy `launcher.py run` THẬT với một lệnh con Python ngắn, trong một kho git tạm
dựng tại chỗ (không dùng checkout đang chạy test).

| # | tiêu chí | nền | đột biến làm ĐỎ (ca đích) |
|---|---|---|---|
| A1 | `python .claude/dev/launcher_test.py` ra `N/N`, hai số BẰNG NHAU; `--dot-bien` ra `M/M` bị giết, hai số bằng nhau | linux | (cổng tổng) |
| A2 | `r1252_ghi_tep_ignored`: kho tạm có `.gitignore` chứa `.tl_state/`; con ghi `.tl_state/x` ⇒ `trang_thai == "ghi_workspace"`, rc launcher **16**, `ma_thoat == 0`, `tep_doi == [{"duong_dan": ".tl_state/x", "doi": "them"}]`, `tep_doi_tong == 1`. Cùng ca, vế sửa: tệp ignored có sẵn, con ghi đè nội dung ⇒ `doi == "sua"` | linux + windows | `r1252_bo_tep_ignored` (chỉ chụp tệp `git ls-files`) ⇒ ĐỎ |
| A3 | `r1252_ghi_trong_git`: con ghi `.git/x` ⇒ `ghi_workspace`, `tep_doi` chứa `.git/x` | linux + windows | `r1252_bo_thu_muc_git` (bỏ `.git` khỏi phép chụp) ⇒ ĐỎ |
| A4 | `r1252_khong_ghi_thi_sach`: con chỉ đọc (in nội dung một tệp tracked) ⇒ `trang_thai == "xong"`, rc 0, `snapshot_ket_qua == "sach"`, `snapshot_truoc_sha256 == snapshot_sau_sha256`, `tep_doi == []`; sha256 của `snapshot-truoc.txt` bằng `snapshot_truoc_sha256`; quyền tệp `0600` (chỉ kiểm quyền trên POSIX) | linux + windows | `r1252_luon_bao_lech` (so luôn ra khác) ⇒ ĐỎ · `r1252_bam_khac_tep` (băm một chuỗi khác nội dung tệp đã ghi) ⇒ ĐỎ |
| A5 | `r1252_run_root_trong_workspace_bi_loai`: `--run-root` là một thư mục con của kho tạm, con không ghi gì ⇒ `sach` (launcher tự ghi `run.json`/log vào đó mà không bị tính). Vế đối chứng cùng ca: con ghi một tệp NGOÀI `--run-root`, cạnh nó ⇒ `ghi_workspace` | linux + windows | `r1252_khong_loai_run_root` ⇒ vế thứ nhất ĐỎ · `r1252_loai_ca_thu_muc_cha` (loại cả thư mục chứa `--run-root`) ⇒ vế đối chứng ĐỎ |
| A6 | `r1252_khong_do_duoc`: ba vế. (a) Một tệp trong kho tạm không đọc được (`chmod 000`; trên Windows, hoặc khi chạy root mà đọc vẫn được, ca dựng lỗi đọc bằng cách thay hàm đọc của bộ chụp trong tiến trình test, có ghi rõ trong ca) ⇒ `khong_do_duoc_workspace`, rc **17**, `snapshot_ly_do == "muc_khong_doc_duoc"`. (b) Con sinh một cháu còn sống khi con thoát (POSIX: cháu cùng nhóm tiến trình; Windows: cháu sinh sau khi con đã vào job) ⇒ `khong_do_duoc` / `cay_chua_chung_minh_chet`. (c) Lệnh chụp ném lỗi ⇒ `khong_do_duoc` / `chup_loi`, launcher không traceback. (d) Đối chứng của (b) trên CÙNG nền: con thoát, không để lại cháu ⇒ KHÔNG ra `cay_chua_chung_minh_chet` (trên Windows là bằng chứng job rỗng thật, không phải `None`). (e) Phép liệt kê hậu duệ KHÔNG đo được: chạy `m.lenh_run` trong tiến trình test (như các ca hiện có đã làm), con thoát sạch như (d), nhưng hàm liệt kê của nền đang chạy được thay để trả `None` (`_thanh_vien_nhom` trên POSIX, `_pid_trong_job` trên Windows) ⇒ rc **17**, `snapshot_ly_do == "cay_chua_chung_minh_chet"`. (b) và (d) vẫn chạy với tiến trình/job thật; chỉ (e) dùng phép thay hàm | linux + windows (a, b, c, d, e) | `r1252_nuot_muc_loi` (bỏ qua phần tử `?`) ⇒ (a) ĐỎ · `r1252_tin_me_chet` (dùng `p.poll() is not None` làm bằng chứng cây chết) ⇒ (b) ĐỎ trên cả hai nền · `r1252_none_la_chet` (coi `None` của `_thanh_vien_nhom`/`_pid_trong_job` là rỗng, ví dụ `not members` thay cho `members == []`) ⇒ (e) ĐỎ · `r1252_windows_khong_dung_job` (Windows luôn trả "không chứng minh được") ⇒ (d) ĐỎ trên Windows · `r1252_dao_thu_tu_phan_loai` (xét `tep_doi` trước `muc_khong_doc_duoc`) ⇒ (a) ĐỎ, vì ca (a) có cả một tệp đổi |
| A7 | `r1252_tat_co_giu_nguyen`: không bật cờ, con ghi `.tl_state/x` ⇒ `trang_thai == "xong"`, rc 0, `run.json` có `chup_workspace == false` và KHÔNG có khoá nào khác của bảng §2.4. Cùng ca: `--help` của `run` có `--chup-workspace`; hai hằng 16, 17 nằm trong bảng mã thoát và tên của chúng có trong `launcher.py --help` | linux + windows | `r1252_mac_dinh_bat` (mặc định bật) ⇒ ĐỎ |
| A8 | `r1252_trang_thai_khac_khong_bi_de`: bật cờ, con ngủ quá `--deadline-utc` và ghi một tệp trước khi bị giết ⇒ `trang_thai == "qua_han"` (không thành `ghi_workspace`), rc 124 hoặc 125 như base, và vẫn có `snapshot_ket_qua` (`ghi_workspace` hoặc `khong_do_duoc`) | linux | `r1252_de_trang_thai` (luôn đặt `ghi_workspace` khi lệch) ⇒ ĐỎ |
| A9 | `r1252_gioi_han_khai`: chuỗi `snapshot_gioi_han` trong `run.json` có nguyên văn CẢ HAI cụm §2.4, mỗi cụm kiểm riêng (vế dương, đo trên giá trị chuỗi đã đánh giá nên không bị ngắt dòng, L6(b)). Vế âm: khi không bật cờ, khoá ấy vắng | linux + windows | `r1252_cat_hau_to_gioi_han` (cắt `thi khong thay`) ⇒ ĐỎ · `r1252_bo_cum_setsid` (bỏ cụm thứ hai) ⇒ ĐỎ |
| A15 | `r1252_cat_50`: hai vế trong cùng ca. (a) Con tạo đúng **50** tệp mới ⇒ `tep_doi_tong == 50`, `tep_doi_bi_cat is False`, `len(tep_doi) == 50`. (b) Con tạo đúng **51** tệp mới ⇒ `tep_doi_tong == 51`, `tep_doi_bi_cat is True`, `len(tep_doi) == 50`, và `tep_doi` bằng đúng 50 đường dẫn ĐẦU theo thứ tự byte; `snapshot-sau.txt` có đủ 51 dòng tương ứng (cắt chỉ áp cho `run.json`, không áp cho tệp chụp) | linux + windows | `r1252_bo_cat` (không cắt) ⇒ (b) ĐỎ · `r1252_tong_sau_cat` (tổng tính sau khi cắt) ⇒ (b) ĐỎ · `r1252_bi_cat_luon_false` ⇒ (b) ĐỎ · `r1252_cat_49` (cắt ở 49) ⇒ (a) ĐỎ · `r1252_cat_ca_tep_chup` (cắt luôn `snapshot-sau.txt`) ⇒ (b) ĐỎ |
| A16 | `r1252_bieu_dien_khong_nhap_nhang`: gọi THẲNG hàm thuần biểu diễn chuẩn (§2.2) trên danh sách phần tử dựng sẵn, không đọc hệ tệp, nên chạy được trên mọi nền. Hai cặp phải ra hai biểu diễn (và hai sha256) khác nhau: (i) một tệp tên byte `b"\xff"` so với một tệp tên `hex:ff`; (ii) một thư mục tên `a\nD\t\tb` so với hai thư mục `a` và `b`. Cùng ca: biểu diễn của một danh sách đã xáo trộn bằng biểu diễn của danh sách đã sắp (thứ tự byte) | linux + windows | `r1252_ghi_chu_khi_utf8` (đường dẫn UTF-8 hợp lệ ghi chữ, còn lại ghi `hex:`) ⇒ (i) ĐỎ · `r1252_tab_xuong_dong` (quay về định dạng `<loại>\t<giá trị>\t<đường dẫn>`) ⇒ (ii) ĐỎ · `r1252_khong_sap` ⇒ vế xáo trộn ĐỎ |
| A17 | `r1252_bo_dem_stat_lam_moi_truoc_chup`: kho tạm có một tệp tracked; TRƯỚC khi gọi launcher, ca đặt mtime của tệp ấy mới hơn mtime ghi trong `.git/index` mà KHÔNG đổi nội dung (dựng lại đúng điều kiện của S6), rồi chạy `run --chup-workspace` với con là `git status --short` ⇒ `snapshot_ket_qua == "sach"`. Đối chứng cùng ca: con tự đổi mtime tệp ấy (qua `os.utime`) rồi chạy `git status --short` ⇒ `ghi_workspace`, `tep_doi` chứa `.git/index` | linux + windows | `r1252_chup_truoc_chot` (dời mốc chụp đầu lên trước `chay_cac_chot`) ⇒ vế thứ nhất ĐỎ · `r1252_chot_sach_khong_ghi_index` (thêm `--no-optional-locks` vào lệnh của `chot_sach`) ⇒ vế thứ nhất ĐỎ. Người thi hành phải chạy cả hai đột biến và thấy vế thứ nhất ra `ghi_workspace`; nếu vế ấy vẫn `sach` dưới đột biến thì fixture chưa dựng đúng S6 và ca chưa đạt |
| A10 | Windows theo `ADR-0060` M3, trên máy chủ kho qua Desktop Commander, theo `ADR-0057`/`0058`/`0059` (khoá, kiểm tải, thư mục riêng, sổ đo). Đây là lượt **TẬP TRUNG**, không phải trọn bộ: theo chỉ thị chủ kho (không CI Windows, không full mutant trên Windows, chỉ Windows tập trung), chạy `--lap-ca` cho đúng mười CA `r1252_*` có nền "windows" ở A2–A7, A9, A15, A16, A17 (đếm theo tên ca), trên ứng viên. Mọi ca phải `qua`, không ca nào bị bỏ qua, kể cả năm vế (a)–(e) của A6 | windows (local) | ca nào trong danh sách bị bỏ qua hoặc đỏ ⇒ ĐỎ; máy không `Online` quá 24 giờ ⇒ packet `blocked` (không tự miễn) |
| A11 | `full_mutant_audit` theo `ADR-0060` M9: **bắt buộc** (diff chạm `.claude/dev/**`), chạy bằng dispatch `ci-dot-bien-du.yml` trên Ubuntu | linux (CI) | thiếu receipt, hoặc thiếu waiver `owner_waived` đúng scope §10.2.3, khi merge |
| A12 | Gate phụ trên ứng viên: `python -m ruff check --select F` cho hai tệp, DELTA so nền = 0 (đo nền và ứng viên trong cùng một lệnh); `python .claude/dev/packet_loop.py doctrine-scan --root .` rc 0; `git diff --check` rc 0 | linux | (cổng canh bất biến; xanh sẵn trên nền là đúng) |
| A13 | `git diff --numstat <base_oid> <candidate_oid>` chỉ gồm `.claude/dev/launcher.py` và `.claude/dev/launcher_test.py`; tổng dòng thêm ≤ 800 (khối `nang_tran` §3). Trước khi tính, kiểm staged/unstaged/untracked rỗng | (không phụ thuộc nền) | thêm tệp thứ ba vào diff ⇒ ĐỎ; vượt 800 ⇒ dừng, checkpoint chủ kho |
| A14 | **Canary**: lượt cross-review Codex offline trên SHA ứng viên cuối (`ADR-0060` M12) chạy bằng `launcher.py` CỦA CHÍNH ứng viên, có `--chup-workspace`, trên một clone mới ⇒ `run.json` có `snapshot_ket_qua` (giá trị nào cũng được ghi nhận đúng như đo). Bằng chứng: sha256 của `launcher.py` đã chạy, đo bằng `sha256sum` trên đường dẫn đã truyền cho lệnh, khớp blob `<candidate_oid>:.claude/dev/launcher.py`. Nếu `snapshot_ket_qua != "sach"` thì lượt đó không được dùng làm bằng chứng read-only, và hồ sơ ghi đúng như đo | linux | sha256 không khớp ⇒ không tính (ĐỎ); thiếu khoá `snapshot_ket_qua` ⇒ ĐỎ |

Chạy thử trên nền `12e5b36` lúc soạn (06:0xZ): `rg -c chup_workspace .claude/dev/launcher.py` = 0 và
`rg -c r1252_ .claude/dev/launcher_test.py` = 0, tức A2–A9 chưa làm (đúng màu). A1, A10–A14 đo khi thi hành.

## 5. Ngoài phạm vi

- Bắt lượt review phải có `snapshot_ket_qua == "sach"`: kiểm ở `kiem-merge`, `land_evidence_nguon` hay hồ sơ land.
  Phải là packet riêng vì chạm tệp khác. Khi land packet này, phiên land mở Issue nợ cho việc ấy.
- Bind-mount read-only / overlay (Q1 phương án b).
- Phát hiện ghi rồi hoàn nguyên giữa hai mốc (Issue #1252, ghi nhận phụ): chỉ khai trong `snapshot_gioi_han`.
- Bật cờ mặc định (Q2).
- Sửa `docs/PROTOCOL_DA_PHIEN.md` §8.2, prompt mẫu cross-review, hay các hồ sơ land cũ.

## 6. `chua_do_duoc`

- Chi phí chụp với bộ đệm LẠNH (S5b): chưa đo. S5 chỉ là chi phí ấm. Lượt A14 ghi `thoi_luong_giay` của cả lượt;
  hai lần chụp chưa được đo riêng.
- Trên Windows: thời gian chụp, tệp bị khoá (`PermissionError` khi một tiến trình khác giữ tệp), và đường dẫn dài.
  Chỉ biết sau A10.
- S6 phủ 6 lệnh git chỉ đọc, chỉ trên Linux. Các lệnh khác (`git fetch`, `git gc --auto` mà git tự kích hoạt,
  `git worktree`), và mọi lệnh trên Windows, có ghi vào `.git` hay không thì chưa đo. Nếu có, lượt ấy ra
  `ghi_workspace`: đây là chủ ý, vì §8.2 đòi kiểm cả `.git`. Hệ quả vận hành ghi ở A14.
- Kích thước sau khi thêm A15–A17: ước tính lại khoảng 300 dòng thêm ở `launcher.py` và 450 ở `launcher_test.py`,
  tức khoảng 750, sát trần 800 của §3. Vượt thì dừng ở A13, không tự cắt tiêu chí.
- Máy Windows của chủ kho có `Online` trong lúc thi hành hay không: chỉ biết lúc đo (`list_devices`).

## 7. hinh_dang_ke_thua

| lớp | biểu hiện | nguồn | quan hệ với packet này |
|---|---|---|---|
| `reviewer-readonly-write-undetected` | **2**: #1224 lượt offline 4 (`a8d7350a`, 11 tệp ignored); #1240 lượt offline 1 (`bc004964`, 20 tệp ignored) | Issue #1252; hồ sơ land `pr1230-wp1224` và `pr1249-wp1240` | packet này là bản vá theo kiến trúc cho lớp: biến phép chụp tay thành trường máy ghi |

Bộ đếm hình dạng bắt đầu ở **2**. Biểu hiện thứ **3** của lớp này, tức một lượt review ghi vào workspace mà
`run.json` của ứng viên KHÔNG bắt được, xuất hiện trong bất kỳ lượt review nào của packet ⇒ DỪNG, báo phiên điều
phối để chủ kho quyết. Ngưỡng ba lần lặp theo CLAUDE.md.

## 8. Bản đồ quyết định (phiên soạn, 06-11-2026)

| câu | quyết định | nằm ở |
|---|---|---|
| Q1 | snapshot sha256 hai mốc, không dùng bind-mount | §2, §5 |
| Q2 | cờ `--chup-workspace`, mặc định tắt; bắt buộc ở consumer là packet riêng | §2.1, §5, A7 |
| Q3 | gồm `.git` và tệp ignored; symlink không đi theo; chỉ loại `--run-root`; mục không đọc được ⇒ không đo được | §2.2, A3, A5, A6 |
| Q4 | `trang_thai` riêng, mã thoát riêng, `ma_thoat` giữ mã thật của con | §2.4, A2, A6 |
| Q5 | khoá `run.json`, `tep_doi` ≤ 50 kèm tổng và cờ cắt, hai tệp chụp `0600`, câu giới hạn | §2.4, A4, A9, A15 |
| Q6 | `nang_tran` ≤ 2 tệp / ≤ 800 dòng thêm | §3, A13 |
| Q7 | `windows: required`, chỉ chạy tập trung các ca `r1252_*` | A10 |
| Q8 | `ADR-0055`, ngân sách mềm 4 | §3 |
| Q9 | năm ca có đột biến; thêm A7–A9 khi viết, A15–A17 sau connector review lượt 1 | §4 |

Các điểm phiên soạn tự thêm khi viết. Chủ kho duyệt bằng cách duyệt `spec_hash`. Điểm 1–4 có từ bản đầu (blob
`da478a61`); điểm 5–9 thêm sau connector review lượt 1 trên `67a4d9c` (P1 `4489586568`, P2 `4489586575`,
`4489586571`, `4489586579`) và một lỗi phiên soạn tự phát hiện khi đo lại S6; điểm 9 sửa lại và điểm 10 thêm sau
connector review lượt 2 trên `cef84ed`:

1. Mã **17** riêng cho `khong_do_duoc` (Q4 chỉ nói "một mã thoát riêng" cho `ghi_workspace`).
2. Vế `cay_chua_chung_minh_chet` (§2.3): chưa chứng minh được hậu duệ đã chết lúc chụp sau ⇒ không đo được.
3. `qua_han` / `bi_ngat` / `da_dung` không bị đè thành `ghi_workspace` (A8).
4. Mục loại `D` cho thư mục, để tạo thư mục rỗng cũng tính là ghi.
5. Phép chứng minh cây chết theo nền, Windows dùng job object (§2.3, A6 (b)(d)); P1 `4489586568`.
6. S5, S6 neo vào hiện vật trong `ops/specs/launcher-readonly-ignored-r1-do/`; số 23 s cũ hạ thành chưa xác minh;
   P2 `4489586575`.
7. Biên cắt 50/51 (A15); P2 `4489586571`.
8. Biểu diễn chuẩn bằng JSON + hex cho mọi đường dẫn (§2.2, A16); P2 `4489586579`.
9. S6 bản đầu khai sai: `git status` CÓ ghi lại `.git/index` sau khi mtime tệp tracked đổi. Phiên soạn tự phát
   hiện khi đo lại S6 có hiện vật. Ở `cef84ed`, bản sửa thêm một bước `update-index -q --refresh`; connector review
   lượt 2 (P2 `4489640552`) chỉ ra `chot_sach` đã làm mới bộ đệm stat nên bước ấy thừa và đột biến của A17 không đỏ.
   Bản này bỏ bước riêng, giữ thứ tự `chay_cac_chot` → mốc chụp đầu, và A17 khoá thứ tự ấy (§2.3, A17).
10. A6 thêm vế (e) tiêm `None` vào hàm liệt kê hậu duệ; P2 `4489640557` (connector review lượt 2).
