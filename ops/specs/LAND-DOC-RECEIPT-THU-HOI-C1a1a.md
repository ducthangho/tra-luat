# ĐẶC TẢ — `LAND-DOC-RECEIPT-THU-HOI-C1a1a` — **revision 1**

| trường | giá trị |
|---|---|
| `packet_id` | `LAND-DOC-RECEIPT-THU-HOI-C1a1a`. Lát **đầu** của C1 (`#499` §C1): bộ kiểm receipt `thu-hoi` gồm các luật **thuần trên JSON**, không gọi git, không gọi mạng |
| `packet_issue` | **CHƯA ĐĂNG**. Đặc tả không cấp việc (soan-spec §5); phải có Issue và lease còn hiệu lực mới được giao |
| `nguon_cap_viec` | `#499` §C1 · nghĩa vụ S≠C từ `#618`, chuyển sang tại `#499` comment `5819877014` · hợp đồng M9 của spec cha `ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md` d.439–477 · quyết định chủ kho ở §0 |
| `review_class` | **`sensitive`**. Đây là bộ kiểm mà `land-packets` sẽ dựa vào để chấp nhận land (protocol §8 d.680: *review/land authority*) |
| `thay_the_cho` | không có. Bản nháp `LAND-DOC-RECEIPT-THU-HOI-C1a1` (commit cục bộ `21e92702`, sha256 `664bdc0d…`) **chưa từng đóng băng, chưa công bố, chưa lease nào neo**. Bản nháp ấy bị thay vì review lượt 1 đo được nó vượt trần ADR-0044 (§0 vòng 3) |

**GIỚI HẠN LỜI KHAI:** mọi khẳng định trong tệp này chỉ chứng minh được tới đúng phép đo ghi kèm.
**Ba trạng thái:** có · không · **KHÔNG ĐO ĐƯỢC**. Trạng thái thứ ba làm cổng ĐỎ, không được làm tròn thành một trong hai trạng thái kia.

---

## 0. Quyết định của chủ kho

Mỏ neo: `#499` comment `5825988768` (Q1/Q3, biên giới A1a, "soạn spec C1"). Các câu dưới đây được chủ kho
trả lời trong phiên 25-09-2026; phiên agent ghi lại đúng lựa chọn đã bấm.

| vòng | câu | chọn, nguyên văn | hệ quả trong tệp này |
|---|---|---|---|
| 1 | Chia C1 | **"Tách C1a / C1b"** | C1a = kiểm offline · C1b = fetch API thật và nối vào `land-packets` |
| 1 | Luật S/C | **"S ≤ C ≤ master"** | thuộc **C1a1b** (§8) |
| 1 | Receipt cũ thiếu trường | **"Thiếu trường ⇒ 12"** | M2 |
| 1 | Assurance khi codex hết quota | **"Same-provider + human audit"** | §9 |
| 2 | C1a ~500 dòng > trần 300 | **"Tách tiếp C1a1 / C1a2"** | C1a2 = kiểm chuỗi join API từ response thô |
| 3 | C1a1 ước 450–570 dòng > trần 300 | **"Tách: không-git / đồ thị git"** | tệp này = **C1a1a** (không git). **C1a1b** = luật trên đồ thị git |

Chỉ thị reviewer, như chủ kho gõ trong phiên 25-09-2026 (không có bản trên GitHub): *"Do codex đã hết quota,
thay cross review bằng same provider reviewer với effort hoặc mô hình ở mức cao hơn"*.

## 1. Số đo — `origin/master` `0e2fe847`, đo **04:08Z 25-09-2026**

**Receipt thật làm mẫu hình dạng.** PR #589 head `af6b54cd…`, check-run `thu-hoi` `107905495884` success,
run `36081907282` attempt 1, artifact `10842182657` `thu-hoi-receipt-af6b54cd…-1`: zip **1102 byte**
(digest `sha256:43ee2205…918a90d`, hết hạn 2026-12-24), chứa đúng một tệp `receipt.json` **1863 byte**,
không BOM. Đo lúc 03:05Z–04:0xZ.

Kiểu của **38** khoá trong receipt ấy (đo bằng `json.loads` + `type()`), và nơi producer ghi nó:

| nhóm | khoá | kiểu đo được | nguồn producer |
|---|---|---|---|
| hex 40 | `S` `H` `T` `tree_S` `oid_bo_kiem_tai_S` | `str` | `ops/lease_publish.py` d.1877–1890 |
| hex 40 | `checkout_commit` `bo_kiem_da_chay_commit` `workflow_definition_commit` `oid_bo_kiem_da_chay` `workflow_definition_blob` | `str` | workflow d.152–164 |
| hex 64 | `workflow_definition_sha256` | `str` | workflow |
| số nguyên | `schema_version` `canh_ancestry` `so_object_da_doc` `tong_bytes` | `int` | `lease_publish.py` |
| số nguyên | `pull_request` `run_id` `run_attempt` `check_run_id` `job_id` `checker_rc` | `int` | workflow |
| chuỗi hằng | `event` = `thu_hoi_admission_receipt` · `che_do` = `chua_kich_hoat` · `ket_luan` = `TAP_THU_HOI_RONG` | `str` | `lease_publish.py` |
| chuỗi danh tính | `repository` = `ducthangho/tra-luat` · `kho_canonical` = `github.com/ducthangho/tra-luat` · `nhanh_mac_dinh` = `master` · `workflow_ref` = `ducthangho/tra-luat/.github/workflows/ops-thu-hoi-admission.yml@refs/heads/master` | `str` | hai nơi |
| thời điểm | `thoi_diem_utc` = `2026-09-25T01:25:14Z` | `str` | `lease_publish.py` `strftime("%Y-%m-%dT%H:%M:%SZ")` |
| tự do | `discovery` | `str` | `lease_publish.py` |
| có thể `null` | `descriptor_q13_ghim` · `policy_T` · `profile_digest` | `null` ở mẫu | `lease_publish.py` (`descriptor_q13_ghim` sẽ thành hex 64 khi A1a r2 ghim Q3) |
| cấu trúc | `so_thu_hoi_S` `so_thu_hoi_T` (`dict`) · `metadata_T` `thu_hoi_moi` (`list`) · `ngan_sach` (`dict`) | như ghi | `lease_publish.py` |

Ghi thêm từ mã producer: `oid_bo_kiem_tai_S` có thể là `None` (`bo_kiem[1] if bo_kiem else None`), và `job_id`
lấy bằng `khop[0].get("id")` nên về lý thuyết có thể là `null`. Receipt mẫu có cả hai ở dạng giá trị.

**Producer phát `ket_luan` nào:** `grep TAP_THU_HOI_RONG ops/lease_publish.py` ra **2** dòng: d.1631 là
chú thích, d.1890 là phép gán duy nhất. Tức producer chỉ gán đúng một giá trị.

**Producer không đổi giữa `601a0f18` và `0e2fe847`:** `git diff --stat 601a0f18 origin/master --
ops/lease_publish.py .github/workflows/ops-thu-hoi-admission.yml` rỗng (04:08Z).

| đường dẫn | `ai-dang-giu` 04:08Z (fetch `--prune`, `master` cục bộ khớp remote) |
|---|---|
| `.claude/dev/doc_receipt_thu_hoi.py` (MỚI) | `rc=0` · NGƯỜI_GIỮ 0 |
| `.claude/dev/doc_receipt_thu_hoi_test.py` (MỚI) | `rc=0` · NGƯỜI_GIỮ 0 |
| `.claude/dev/ci_dang_ky_test.py` | `rc=0` · NGƯỜI_GIỮ 0 |

Hai lần đo trước đó trả `rc=12` vì phía đo, không phải vì có người giữ: một lần cache thiếu nhánh máy chủ
mới, một lần nhánh spec cục bộ phân kỳ sau khi master tiến 14 commit. Fetch lại và rebase xong thì đo ra `rc=0`.

**Vì sao cần `ci_dang_ky_test.py`:** tệp test mới dưới `.claude/dev/` phải có mặt trong sổ `MOI`
(`ci_dang_ky_test.py` d.29) thì CI mới chạy và đối chiếu N/N; xoá dòng đăng ký thì `kiem()` báo test sống
chưa đăng ký (review lượt 1 đo).

**Mật độ tham chiếu cho trần dòng:** ca `t155_618` của #620 (đồ thị git thật, 5 ca + 4 đột biến) dài **132**
dòng; toàn bộ phần test của #620 là **+162** dòng (review lượt 1 đo, 03:48Z).

## 2. `write_set`

```
.claude/dev/doc_receipt_thu_hoi.py
.claude/dev/doc_receipt_thu_hoi_test.py
.claude/dev/ci_dang_ky_test.py
```

Đúng ba đường, không ký tự đại diện. Hiện vật review và bookkeeping (`ops/reviews/**`, `CHANGELOG.md`,
`RELEASE_MANIFEST.json`) **KHÔNG** nằm trong write set.

## 3. `ngoai_pham_vi`

| thứ CỐ Ý không làm | lý do |
|---|---|
| Mọi luật cần **git**: S ≤ C, C trên first-parent của master, S ≤ H, mốc định dạng, OID `ops/lease_publish.py` tại C, blob/sha256 workflow tại C, tree(H) = T, tree(S) = `tree_S` | **C1a1b** (§8). C1a1a không mở tiến trình con nào |
| Gọi API GitHub, tải artifact, kiểm chuỗi join check-run → suite → run → attempt jobs → artifact | C1a2 và C1b |
| Nối vào `.claude/skills/land-packets/SKILL.md` hoặc `packet_loop.py` | C1b |
| Sửa producer (`ops-thu-hoi-admission.yml`, `ops/lease_publish.py`) | ngoài write set. `ops/lease_publish.py` còn đang bị lease của #579 (PR #589) giữ |
| Sửa §M9 của spec cha | spec cha là snapshot đã đóng băng; chuỗi C1 **thay** vế consumer của nó |
| Diễn giải nội dung `so_thu_hoi_*`, `thu_hoi_moi`, `metadata_T`, `policy_T`, `ngan_sach`, `discovery` | ngữ nghĩa sổ thu hồi thuộc A1a/A1b. C1a1a chỉ kiểm **kiểu** (M3) |
| CI, full CI, CI Windows, `workflow_dispatch`, rerun tay | chỉ thị chủ kho: không chạy tới khi đủ điều kiện merge · `manual_ci_budget: 0` · không Windows |

## 4. `muc_tieu` — mỗi dòng chiếu vào MỘT đường dẫn (L2)

M1–M6 thuộc `.claude/dev/doc_receipt_thu_hoi.py`. M7 thuộc `…_test.py`. M8 thuộc `ci_dang_ky_test.py`.

| # | mục tiêu | nguồn |
|---|---|---|
| **M1** | Hàm thuần `kiem_json(raw: bytes, *, kho: str, nhanh: str, base_hien_hanh: str, head_hien_hanh: str) -> dict` trả `{"ok": bool, "luat": {"K1": "qua"\|"do", …}, "ly_do": [str, …]}`, và CLI `kiem-json --receipt <tệp> --kho <owner/repo> --nhanh-mac-dinh <tên> --base-hien-hanh <oid> --head-hien-hanh <oid>` in đúng dict ấy thành **một dòng JSON**. Thoát **0** khi `ok`; **12** khi có luật `do`; **2** khi tham số sai hoặc không đọc được tệp (`OSError`). Bốn tham số chuỗi phải khác rỗng; `--base/--head` phải hex thường 40 ký tự, sai ⇒ 2. Mọi luật đều được chạy và ghi trạng thái (không dừng ở luật đỏ đầu tiên), trừ khi K1 đỏ thì K2–K5 ghi `do` với lý do "K1 đỏ" | L3 |
| **M2** | **K1 — hình dạng.** (a) Ba byte đầu là `EF BB BF` ⇒ đỏ. Kiểm **trước** `json.loads`, vì `json.loads(bytes)` tự nuốt BOM (review lượt 1 đo). (b) Giải mã UTF-8 **strict**; `UnicodeDecodeError` ⇒ đỏ. (c) `json.loads`; `JSONDecodeError` ⇒ đỏ. (d) Kết quả phải là `dict`. (e) Tập khoá **khít đúng 38 khoá** ở §1: thiếu một khoá ⇒ đỏ, thừa một khoá ⇒ đỏ. (f) `schema_version == 1` và là `int` không phải `bool`. (g) `event == "thu_hoi_admission_receipt"` | chọn "thiếu trường ⇒ 12" |
| **M3** | **K2 — kiểu.** Theo đúng bảng §1: nhóm hex 40 là `str` khớp `^[0-9a-f]{40}$`, riêng `oid_bo_kiem_tai_S` được thêm `null`. `workflow_definition_sha256` khớp `^[0-9a-f]{64}$`. Nhóm số nguyên là `int` và **không phải** `bool`; `job_id` **không** được `null`. `thoi_diem_utc` khớp `^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$`. `descriptor_q13_ghim` là `null` hoặc hex 64. `policy_T` là `null` hoặc `dict`. `profile_digest` là `null` hoặc `str`. `discovery` là `str`. `so_thu_hoi_S` `so_thu_hoi_T` `ngan_sach` là `dict`; `metadata_T` `thu_hoi_moi` là `list`. Ba trường C phải **bằng nhau**: `checkout_commit == bo_kiem_da_chay_commit == workflow_definition_commit` | producer §1 |
| **M4** | **K3 — danh tính kho.** Lấy từ **tham số**, không từ receipt: `repository == kho`; `kho_canonical == "github.com/" + kho`; `nhanh_mac_dinh == nhanh`; `workflow_ref == kho + "/.github/workflows/ops-thu-hoi-admission.yml@refs/heads/" + nhanh` | review lượt 1, lớp `tieu-chi-mau-thuan-luat-hoac-producer` |
| **M5** | **K4 — stale.** `S == base_hien_hanh` và `H == head_hien_hanh`. Lệch một trong hai ⇒ đỏ ("receipt stale, chạy lại"). Hợp đồng với caller ghi ở §8 | nghĩa vụ #618 mục 3 |
| **M6** | **K5 — kết luận bộ kiểm.** `checker_rc == 0` (đã là `int` không `bool` nhờ K2); `ket_luan` thuộc tập đóng `{"TAP_THU_HOI_RONG"}`; `che_do == "chua_kich_hoat"`. Giá trị lạ ⇒ đỏ; mở rộng tập phải qua revision. Khi A1b đổi `che_do`, bộ kiểm này **phải** đỏ tới khi có revision, và đó là chủ ý | producer §1 |
| **M7** | `.claude/dev/doc_receipt_thu_hoi_test.py`: dựng **fixture dương** từ bảng §1 (38 khoá, giá trị của receipt mẫu, viết thẳng trong test, không đọc artifact), rồi mỗi ca âm là **một** biến đổi của fixture ấy. Đột biến chạy trên **bản sao tạm** của module (không sửa tệp thật), nạp bằng `importlib` với `sys.dont_write_bytecode = True`. Suite in dòng tổng `doc_receipt_thu_hoi tests: N/N ca QUA · M/M dot bien GIET` | L3 |
| **M8** | Đăng ký `.claude/dev/doc_receipt_thu_hoi_test.py` vào `MOI` của `ci_dang_ky_test.py` với regex bắt được hai cặp N/N và M/M của dòng tổng ở M7 | `ci_dang_ky_test.py` |

## 5. `nghiem_thu` — mỗi tiêu chí nêu phép đo làm nó ĐỎ (L3)

"Đột biến X ⇒ ca Y ĐỎ" nghĩa là: chạy ca Y trên bản sao module đã đột biến X, ca Y phải **thất bại vì đúng
assertion của nó** (lớp ngoại lệ riêng, kèm tên ca), không vì lỗi vô can (bài học #355/#359).

| # | tiêu chí | phép đo làm nó **ĐỎ** |
|---|---|---|
| **A1** | Fixture dương ⇒ `ok: true`, cả năm luật `qua`, CLI rc 0 | Mọi đột biến ở dưới giữ fixture dương xanh; đột biến nào làm fixture dương đỏ là đột biến quá tay và phải đổi |
| **A2** | Có BOM ⇒ K1 `do` | Đột biến bỏ phép kiểm ba byte đầu ⇒ ca BOM ĐỎ (không có nó, `json.loads` nuốt BOM và K1 thành `qua`) |
| **A3** | Byte `0x80` giữa thân ⇒ K1 `do`, không ném ngoại lệ trần | Đột biến bỏ `try` quanh giải mã ⇒ ca ĐỎ vì kiểu ngoại lệ sai |
| **A4** | Thiếu **từng** khoá trong 38 (lặp đủ 38) ⇒ K1 `do`; thừa một khoá ⇒ K1 `do` | Đột biến đổi phép so tập khít thành `issubset` ⇒ ca "thừa khoá" ĐỎ. Đột biến đổi thành `issuperset` ⇒ ca "thiếu khoá" ĐỎ. Hai đột biến, hai ca đích khác nhau |
| **A5** | `schema_version = True` ⇒ K1 `do` (vì `True == 1` trong Python) | Đột biến dùng `== 1` không kiểm kiểu ⇒ ca ĐỎ |
| **A6** | Mỗi nhóm kiểu của M3 có ít nhất một ca âm: hex 39 ký tự, hex HOA, `int` là `bool`, `job_id = null`, `thoi_diem_utc` thiếu `Z`, `descriptor_q13_ghim` là hex 63 | Mỗi ca có **một** đột biến nới đúng phép kiểm của nhóm ấy ⇒ đúng ca ấy ĐỎ |
| **A7** | Ba trường C lệch nhau (`bo_kiem_da_chay_commit` khác hai trường kia) ⇒ K2 `do` | Đột biến bỏ phép so bằng nhau ⇒ ca ĐỎ |
| **A8** | K3: bốn ca âm, mỗi ca lệch đúng một trong `repository` · `kho_canonical` · `nhanh_mac_dinh` · `workflow_ref` | Đột biến lấy `nhanh` từ `receipt["nhanh_mac_dinh"]` thay vì tham số ⇒ ca "receipt khai nhánh khác, workflow_ref khớp nhánh receipt" ĐỎ. Đột biến bỏ phép so `workflow_ref` ⇒ ca sai `workflow_ref` ĐỎ |
| **A9** | K4: `base_hien_hanh ≠ S` ⇒ `do`; `head_hien_hanh ≠ H` ⇒ `do` | Đột biến bỏ từng vế ⇒ đúng ca của vế ấy ĐỎ |
| **A10** | K5: `checker_rc = 1` ⇒ `do`; `ket_luan` lạ ⇒ `do`; `che_do = "da_kich_hoat"` ⇒ `do` | Đột biến bỏ từng vế ⇒ đúng ca ĐỎ |
| **A11** | Mọi luật được ghi trạng thái: ca đỏ đồng thời K3 và K4 ⇒ `luat` có **cả hai** `do` | Đột biến "dừng ở luật đỏ đầu tiên" ⇒ ca ĐỎ |
| **A12** | CLI: rc 0 / 12 / 2 đúng như M1; tệp không tồn tại ⇒ 2; `--base` 39 ký tự ⇒ 2 | Đọc `rc` trực tiếp từ `subprocess.run`, không qua pipe |
| **A13** | Suite in **N/N và M/M, mỗi cặp hai số bằng nhau**; `ci_dang_ky_test.py --chay` nhận tệp mới, rc 0 | Xoá dòng đăng ký ⇒ `ci_dang_ky_test.py` ĐỎ |
| **A14** | `git diff --numstat origin/master..<head>` chạm **đúng ba** đường của write set, và **tổng dòng thêm ≤ 300** | Vượt 300 ⇒ executor **DỪNG** và hỏi chủ kho. Không viết vào PR rằng ADR-0044 "ĐẠT" khi chưa đo |
| **A15** | `python3 .claude/dev/packet_loop.py doctrine-scan --root .` rc 0; `adr-song` rc 0 | rc đọc trực tiếp |

**Không tiêu chí nào được đóng bằng `rc=0` trơn.** Mỗi tiêu chí đòi bằng chứng dương: hai số bằng nhau,
`ok: true`, hoặc một đột biến ĐỔI MÀU đúng ca đích.

## 6. `hinh_dang_ke_thua` (L4)

C1a1a không phải packet khắc phục, nhưng nó là consumer của chuỗi thu hồi lease. Chép **đủ** bảng spec A1a
§7 (đo 20-09-2026) và thêm hai dòng từ #620:

| hình dạng | số lần | nguồn |
|---|---|---|
| "thu hồi là dữ liệu ghi vào bản sao" | 2 | r9 §1 |
| "lời khai hội tụ rộng hơn phép đo" | 3 | r9 g2, lượt 1 |
| "hai cổng bất đồng" | 1 | r9, #473 |
| **"nguồn được tin mà chưa xác minh"** | **6** | r9 lượt 1, 2, 3, 4b, 5, 6 |
| "cổng CÓ MẶT khác cổng ĐO ĐƯỢC" | 1 | #499 C2a |
| "gate xanh lane PR, master đo lần đầu" | 1 | #499 C3 |
| "stub bỏ qua toán hạng nên đột biến sống" | 1 | #620 F1 (`ops/lease_publish_test.py` d.5958) |
| "lời khai về mốc cũ chưa sửa hết" | 1 (lặp 3 lượt review liền) | #620 F3, verdict tại PR #620 comment `5820326415` (không nằm trong kho) |

Hình dạng thứ tư đã chạm **6**. Review lượt 1 của bản nháp C1a1 tìm thêm một trường hợp thuộc đúng lớp này
(lớp `fact-do-caller-dua-thay-cho-fact-do`: CLI nhận `--master`/`--base`/`--head` không nguồn bắt buộc) —
tức **lần thứ 7**, phát hiện **ở tầng đặc tả**, trước khi có mã. Theo §12 protocol, lần này đòi đổi cách làm
chứ không vá thêm. Cách đã đổi: (1) C1a1a lấy danh tính kho và nhánh **chỉ** từ tham số, không từ receipt
(M4); (2) nguồn của `base/head` thành **hợp đồng** bắt buộc với caller ở §8, có ca nghiệm thu ở C1b; (3) mọi
fact cần đo độc lập bằng git dồn sang C1a1b, kèm các luật mà review lượt 1 đã chỉ ra.

## 7. `chua_do_duoc`

1. **Số dòng thêm.** Ước từ mật độ §1: module ~110–140, test ~150–190, đăng ký 1–3, tổng **~260–330**.
   Khoảng ấy **chạm** trần 300. Chốt A14: vượt thì dừng và hỏi, không tự tách tiếp.
2. **Receipt thật cho ca S ≠ C.** Chưa có (đo 04:0xZ). Không ảnh hưởng C1a1a, vì C1a1a không so đồ thị;
   nó là tiền đề của C1a1b.
3. **Producer đổi tập khoá hoặc `che_do`.** Tập khoá khít (M2) và `che_do` hằng (M6) làm consumer đỏ tới khi
   có revision. Đó là chủ ý (fail-close), nhưng chưa có cổng nào báo sớm khi producer đổi. Ghi nợ cho C1b.
4. **`job_id` có từng là `null` trên receipt thật không.** Mẫu có `int`. M3 bác `null`; nếu producer thật
   sự phát `null` ở ca nào đó, consumer sẽ đỏ và cần xem lại producer, không nới consumer.
5. **Assurance.** Xem §9. Không lượt review nào trong packet này cho được `cross_approved`.

## 8. Thứ tự và nghĩa vụ chuyển tiếp

`C1a1a` → `C1a1b` → `C1a2` → `C1b`. Mỗi lát được cấp lease sau khi lát trước land. `C1b` là lát duy nhất
chạm `land-packets`, và phải land **trước** A1b (bật cờ `SO_THU_HOI_KICH_HOAT`).

**Nghĩa vụ bắt buộc của C1a1b** (từ review lượt 1 của bản nháp C1a1, ngày 25-09-2026). Spec C1a1b phải
chép và đo lại từng dòng:

| # | nghĩa vụ | vì sao (số đo của review lượt 1) |
|---|---|---|
| N1 | C phải thuộc `git rev-list --first-parent MOC^..<master>` ∪ {MOC}, không chỉ "là tổ tiên master" | producer chỉ chạy tại HEAD nhánh mặc định; **1795** commit là tổ tiên master mà không nằm trên first-parent, **37** trong số đó chạm `ops/lease_publish.py` |
| N2 | Thêm luật `merge-base --is-ancestor S H` | spec cha d.447 đòi "S tổ tiên H"; không luật nào của bản nháp đo nó; `canh_ancestry` chỉ là lời khai |
| N3 | Test dựng đồ thị bằng `git clone --shared <ROOT>` và commit **trên** MOC thật, không `git init` rỗng; hằng MOC không nhận ghi đè | trong repo `git init` mới, MOC không tồn tại ⇒ `--is-ancestor` rc 128 cho **mọi** ca |
| N4 | Trước mọi `rev-parse X:path` hoặc `X^{tree}`, chạy `git cat-file -e X^{commit}`: rc khác 0 ⇒ `khong_do_duoc`; sau đó rc 128 của `rev-parse` ⇒ `do` | commit vắng và path vắng cùng trả rc 128 |
| N5 | Ca "C là tổ tiên thật sự của S" để giết đột biến đảo toán hạng; ca "nhánh rẽ" không giết được nó | đo: với nhánh rẽ, cả `S X` lẫn `X S` đều rc 1 ⇒ bộ tương đương |
| N6 | `--master` phải bằng `git rev-parse refs/remotes/origin/<nhanh>` trong repo, lệch ⇒ 2 | `--master <C>` làm luật "C ≤ master" luôn đúng |
| N7 | Gọi tên đúng thứ được chứng minh: K6/K7 chứng minh receipt **nhất quán với C tự khai**; chứng minh C = `workflow_sha` của run là việc của C1a2 | tránh lời khai rộng hơn phép đo |
| N8 | Đối chiếu `oid_bo_kiem_tai_S == git rev-parse S:ops/lease_publish.py` (đối chiếu, không dùng làm identity) | trường đo được offline nhưng bản nháp chỉ kiểm có mặt |

**Hợp đồng với caller (C1b phải tuân và có ca nghiệm thu riêng):** `base_hien_hanh` và `head_hien_hanh` lấy
từ **readback PR hiện hành** (`base.sha`, `head.sha` đọc qua API ngay trước land), **không** từ receipt. C1a1a
không kiểm được nguồn của hai tham số ấy — nó chỉ kiểm receipt khớp với chúng.

## 9. Review và assurance

- Reviewer: Claude **cùng provider**, effort hoặc model **cao hơn** executor. Lặp vá và review theo **lớp lỗi**
  tới khi hết P1/P2/P3. Mỗi lượt đăng verdict.
- Protocol §8 d.652: `same_provider_approved` **không** thay được `cross_approved` cho lớp `sensitive`. Vì vậy
  merge cần thêm **human audit của chủ kho** trên exact head, như PR #620. PR và receipt phải khai thẳng:
  *không có `cross_approved`*.
- Không CI, không full CI cho tới khi đủ điều kiện merge. Không CI Windows.
