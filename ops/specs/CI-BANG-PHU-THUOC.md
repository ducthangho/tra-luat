# ĐẶC TẢ ĐÓNG BĂNG — `CI-BANG-PHU-THUOC`

> Đặc tả này **không cấp việc**. Phải có Issue + lease còn hiệu lực (`docs/PROTOCOL_DA_PHIEN.md`
> §3.2, §4) mới được bắt tay. Phiên nào đọc rồi tự làm là tự cấp việc cho mình.
>
> Sửa đặc tả đã có băm ⇒ đi qua **bản sửa đổi mới**. Sửa đè là làm `spec_sha256` trong lease trỏ
> vào một thứ không còn tồn tại.

`packet_id`: `CI-BANG-PHU-THUOC`
`packet_issue`: `CHUA_CO` — người giữ kho chưa mở. **Không bịa số.**

## `nguon_cap_viec`

**KHÔNG phải packet khắc phục.** Không có tiền nhiệm thất bại. Đây là việc phát hiện bằng **quan
sát vận hành**: người giữ kho hỏi ngày 2026-08-22 vì sao một bản vá thuần văn bản vẫn phải chờ CI
chạy đủ, và các phép đo trả lời câu hỏi đó lộ ra rằng **kho chưa có chỗ nào ghi bước CI nào phụ
thuộc thư mục nào**. Packet này ghi bảng ấy và dựng cỗ máy tự kiểm nó.

Không trỏ `ops/HANG_DOI_PACKET.md`: tệp ấy **chưa có trên `master`** (`#229` còn mở), nên trỏ vào
là dựng con trỏ chết — đúng bệnh `docs/PROTOCOL_DA_PHIEN.md` §20 sinh ra để chặn. Khi `#229` land
thì thêm một lane; đó là việc một dòng, không phải điều kiện của packet này.

`review_class`: **`sensitive`** — `docs/PROTOCOL_DA_PHIEN.md:571` liệt kê thẳng *"workflow/CI
authority"*. Packet này **chưa** sửa `ci.yml`, nhưng nó sinh ra dữ liệu mà `ci.yml` sẽ tin, nên
phân lớp fail-closed theo hệ quả chứ không theo đường dẫn bị chạm.

## Bằng chứng — ĐO, không suy

Mọi số neo `master` = `195a478d7f083b67900777c6f4e8ada0860b3707`, đo 2026-08-22.

### B1. Chi phí từng bước — vì sao có packet này

Đọc từ API Actions, lượt `master` `9864c778` (`gate`, run `32560564983`):

| bước | ubuntu | windows |
|---|---|---|
| `tl selftest` | **106s** | **155s** |
| gate chạy trong cgroup (Linux) | 82s | — |
| `determinism-audit` | 33s | 67s |
| `golden-test` | 26s | 53s |
| `don-nhanh selftest` | 24s | — |
| `eol-policy selftest` | 19s | 45s |
| 16 bước còn lại | 39s | 114s |
| **TỔNG** | **331s** | **429s** |

Windows tính tiền **×2** ⇒ một lượt `master` = **19,8 phút**; một lượt PR thường = **5,5 phút**.

Tái lập: MCP `x/actions`, `actions_list` `method=list_workflow_jobs`, tham số tên là
**`resource_id`** (KHÔNG phải `run_id`), payload lồng **hai** tầng `{"jobs": {"jobs": [...]}}`.

### B2. Tập ĐỌC — đo bằng audit hook, KHÔNG bằng đột biến chú thích

`sitecustomize.py` cài `sys.addaudithook` bắt `open`/`os.open`/`io.open`, nạp qua `PYTHONPATH`
nên tiến trình chạy y như thật và **mọi tiến trình con cũng kế thừa**.

| bước | tổng tệp | `ops/` | `docs/` | `CLAUDE.md` | `.claude/` | `.githooks/` | `.github/` |
|---|---|---|---|---|---|---|---|
| `tl selftest` (1698/1698) | 440 | **0** | **69** | **1** | 1 (`agents/`) | **0** | 1 (`ci.yml`) |
| `doc-claims-check` | 243 | **0** | **69** | **1** | **0** | **0** | **0** |
| `workflow-audit` | 67 | **0** | **0** | **0** | **0** | **0** | **0** |
| `golden-test` | 107 | **0** | **0** | **0** | **0** | **0** | **0** |

Nguồn của phụ thuộc `docs/`: `scripts/tl_core/workflow.py:862` quét `("docs/adr","*.md"), (".","*.md")`
cho chốt *"tệp nằm trong gói mà không đường nào dẫn tới"*. Thêm một ADR mà không workflow card nào
trỏ tới ⇒ chốt ấy ĐỎ. **Phụ thuộc này THẬT và phải giữ.**

### B3. Tập BĂM — DẪN XUẤT từ mã, không kê tay

`scripts/tl_core/release.py`: `_RELEASE_EXCLUDE_DIRS` chứa `ops` `docs` `.claude` `.codex`
`.githooks` `.github` `rasoat` `changelog_archive` `claude-code-best-practice`;
`_RELEASE_EXCLUDE_NAMES_ANYWHERE` chứa `CLAUDE.md`. Tệp không vào gói thì không đổi băm gói ⇒
`release-bundle` / `release-verify` / `release-check` độc lập với chúng **theo kiến trúc**.

Tái lập:
```
python3 -c "import sys; sys.path.insert(0,'scripts'); from tl_core import release as R; \
print(sorted(R._RELEASE_EXCLUDE_DIRS)); print(sorted(R._RELEASE_EXCLUDE_NAMES_ANYWHERE))"
```

### B4. Fast-path sẽ bắn bao nhiêu lần — phân bố 40 merge gần nhất

| nhóm | số | % |
|---|---|---|
| A — chỉ chạm `ops/**` | 17 | 42% |
| B — ngoài CẢ tập đọc lẫn tập băm | 5 | 12% |
| C — chạm tập đọc, không chạm tập băm | 10 | 25% |
| D — chạm tập băm ⇒ chạy hết | 8 | 20% |

**A+B = 54%** bỏ được trọn nhóm runtime; **+C = 80%** bỏ được ít nhất nhóm băm.

### B5. Ba lần phép dò YẾU cho kết quả SAI — lý do tồn tại của packet này

Dò bằng "thêm một dòng chú thích rồi xem đầu ra có đổi không" chỉ bắt được bước **băm nội dung**.
Ba bước chạy **hành vi** đều cho `.` (nghĩa là "an toàn để bỏ") trong khi phép đo mạnh cho thấy
ngược lại: `tl selftest` đọc `docs/` **69 tệp**; `doc-claims-check` đọc `docs/` **69 tệp**;
và một lượt còn khai `determinism-audit` phụ thuộc `ops/` — hoá ra là hai khoá **tự trôi**
(`cases[12].raw_sha256`, `raw_stable`) mà khung golden **đã tự khai** bằng trường `raw_stable: False`.

**Một bảng do người gõ sẽ mang đúng ba cái sai ấy.** Đó là lý do bảng phải do máy dựng lại.

## `write_set`

- `.github/checks/ci_phamvi.py`
- `.github/checks/ci_phamvi_test.py`

## `ngoai_pham_vi`

| thứ | vì sao |
|---|---|
| **`.github/workflows/ci.yml`** | Packet này **không đổi hành vi CI**. Công tắc thuộc `CI-FASTPATH-THEO-DIFF`, mọc trên packet này đã land. Tách theo **thứ tự rủi ro**: bảng là dây an toàn, công tắc là đạp ga — dây an toàn phải chạy vài lượt trước khi có ai dựa vào nó. |
| **bước `cgroup`** (82s = 25% ubuntu) | Không phải kiểm nội dung mà là chứng minh **cô lập gate lifecycle**. Hạ nó là hạ một bảo đảm an toàn, khác lớp với "bỏ bước đo lại thứ không đổi". Chưa đo phụ thuộc của nó. |
| **`tl selftest` theo phạm vi** | Đòn bẩy lớn nhất (106s/155s cho 1698 ca) nhưng đòi selftest khai được tập đọc **từng ca**. Packet riêng. |
| **`launcher-windows.yml`** | Đã có `paths:` riêng và cơ chế khác; không trộn. |

## `muc_tieu`

| # | mục tiêu | đường dẫn |
|---|---|---|
| M1 | Khai bảng phụ thuộc thành **dữ liệu đọc được bằng máy**: mỗi bước gate ⇒ tập nhóm đường dẫn nó ĐỌC, và cờ nó có băm gói hay không. | `.github/checks/ci_phamvi.py` |
| M2 | Dẫn xuất vế **BĂM** từ `_RELEASE_EXCLUDE_*` thay vì kê tay; lệch ⇒ ĐỎ. | `.github/checks/ci_phamvi.py` |
| M3 | Dựng lại vế **ĐỌC** bằng audit hook và so với bảng; đọc thêm một nhóm chưa khai ⇒ ĐỎ. | `.github/checks/ci_phamvi.py` |
| M4 | Ba trạng thái, không phải hai: `phụ thuộc` · `độc lập` · **`không đo được`** — cái thứ ba làm cổng ĐỎ. | `.github/checks/ci_phamvi.py` |
| M5 | Phản chứng cho từng luật, cộng **đột biến** giết đúng ca của nó. | `.github/checks/ci_phamvi_test.py` |

## `nghiem_thu`

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| N1 | `ci_phamvi.py --kiem-bam` xanh trên master hiện tại | Đột biến `adr_style`: thêm `ops` vào bảng ở vế băm **rồi xoá `ops` khỏi `_RELEASE_EXCLUDE_DIRS`** ⇒ phải ĐỎ. Không có đột biến này thì không biết cổng đang đọc mã hay đọc bảng. |
| N2 | `ci_phamvi.py --kiem-doc --buoc tl-selftest` xanh | Đột biến: xoá `docs/` khỏi tập ĐỌC khai cho `tl-selftest` ⇒ ĐỎ, và thông điệp phải **in ra tên nhóm thiếu**. |
| N3 | Trạng thái thứ ba có răng | Ca `khong_do_duoc_thi_do`: audit hook không cài được (thiếu `PYTHONPATH`) ⇒ rc khác 0 **và** in `KHONG DO DUOC`. Đột biến đổi nhánh ấy thành `return 0` ⇒ ca ĐỎ. |
| N4 | Bảng không nhận nhóm bịa | Ca `nhom_khong_ton_tai_thi_do`: khai một nhóm đường dẫn không có trên đĩa ⇒ ĐỎ (con trỏ chết, cùng luật §20). |
| N5 | Chiều **BẮT OAN** có ca riêng | Ca `ops_van_doc_lap`: `ops/**` phải ở trạng thái `độc lập` với cả 4 bước. Ca chiều-tha KHÔNG chết được bằng đột biến **gỡ chốt** — thứ giết nó là đột biến **SIẾT THÊM**, một loại khác hẳn. Đột biến đích: `bao_gio_cung_phu_thuoc` — cho hàm phân loại trả `phụ thuộc` vô điều kiện ⇒ N5 ĐỎ trong khi N1–N4 vẫn xanh. Không có đột biến này thì N5 chỉ là một lời khẳng định `rc=0`, không phải phép đo. |
| N6 | Delta so `origin/master` = 0 ĐỎ | Chạy `packet_loop_test.py` và `lease_publish_test.py` **trong worktree của chính kho** (`git worktree add --detach`). Chép tệp ra thư mục rỗng cho **4 ĐỎ giả** — đã sập một lần, ghi ra để không lặp. |

## `hinh_dang_ke_thua`

`khong_ap_dung` — không phải packet khắc phục, không có biên nhận tiền nhiệm để chép bộ đếm.

Nhưng **có một bộ đếm phải mang sang** vì nó sinh trong chính lượt soạn spec này: **hình dạng
"phép dò yếu cho kết quả an toàn giả" đã đếm được BA lần** (B5). Chạm ba là ngưỡng `CLAUDE.md`
đặt để hỏi *"có nên làm việc này không"* — ở đây câu trả lời là **có**, nhưng chỉ vì packet đổi
sang phép dò mạnh. Nếu phiên thi hành thấy mình quay lại dò bằng đột biến chú thích, đó là dấu
hiệu đã trượt về hình dạng cũ.

## `chua_do_duoc`

- **Tập đọc đo trên Linux, chưa đo trên Windows.** `tl selftest` có ca phụ thuộc nền; tập đọc trên
  `windows-latest` có thể khác. Packet phải khai điều này trong bảng thay vì ngầm coi hai nền như một.
- **Audit hook chỉ bắt `open`/`os.open`/`io.open`.** Thư viện C-level đi thẳng syscall sẽ lọt. Chưa
  có phản chứng cho ca ấy.
- **`tl selftest` KHÔNG chạy được trong container remote nếu `cryptography` hệ thống hỏng** —
  `pyo3_runtime.PanicException` qua `pypdf`. Đo 2026-08-22: hook phiên báo *"môi trường còn khớp"*
  trong khi thư viện bắt buộc panic ngay lúc import. **"Khớp requirements" không phải "chạy được".**
  Chữa bằng `pip install --upgrade cryptography`. Phiên thi hành phải kiểm TRƯỚC khi tin bất kỳ
  phép đo tập-đọc nào; một lượt nền hỏng cho `rc=1` mà vẫn in ra được vài dòng trông như số liệu.
- **`bo ca gate chay TRONG cgroup`** chưa đo phụ thuộc — cố ý ngoài phạm vi.
