# ĐẶC TẢ — `LAND-DOC-RECEIPT-THU-HOI-C1a1a` — **revision 5**

| trường | giá trị |
|---|---|
| `packet_id` | `LAND-DOC-RECEIPT-THU-HOI-C1a1a`. Lát **đầu** của C1 (`#499` §C1): bộ kiểm receipt `thu-hoi` gồm các luật **thuần trên JSON**, không gọi git, không gọi mạng |
| `packet_issue` | **CHƯA ĐĂNG**. Đặc tả không cấp việc (soan-spec §5); phải có Issue và lease còn hiệu lực mới được giao |
| `nguon_cap_viec` | `#499` §C1 · nghĩa vụ S≠C từ `#618`, chuyển sang tại `#499` comment `5819877014` · hợp đồng M9 của spec cha `ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md` d.439–477 · quyết định chủ kho ở §0 |
| `review_class` | **`sensitive`**. Đây là bộ kiểm mà `land-packets` sẽ dựa vào để chấp nhận land (protocol §8 d.680: *review/land authority*) |
| `revision` | **5**. Revision 1–4 (`11a97f47` · `90675fa3` · `ee02122b` · `0c8c3532`; sha256 `970fb4c3…` · `1f998e02…` · `c614d350…` · `231489ee…`) chưa đóng băng. Revision 5 chép hợp đồng phủ do codex lượt 4 đề xuất (§5.0), nâng ngoại lệ dòng lên ≤ 400, và **đóng băng bằng human audit của chủ kho** thay vì thêm lượt codex (§0 vòng 6, §9) |
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
| 1 | Assurance khi codex hết quota | **"Same-provider + human audit"** | **thay bởi** chỉ thị sau, xem §9 |
| 2 | C1a ~500 dòng > trần 300 | **"Tách tiếp C1a1 / C1a2"** | C1a2 = kiểm chuỗi join API từ response thô |
| 3 | C1a1 ước 450–570 dòng > trần 300 | **"Tách: không-git / đồ thị git"** | tệp này = **C1a1a** (không git). **C1a1b** = luật trên đồ thị git |
| 4 | Checkpoint §12: hết trần 2 lượt codex, và lớp `dot-bien-tuong-duong-hoac-thieu` đã xuất hiện ở 3 lượt review | **"Đổi phương pháp + nâng trần 2→4"** | §5.0 (checklist nguồn chuẩn → nhóm trường phụ thuộc) · khối `nang_tran` ở §9 |
| 4 | Prototype sau vá chạm đúng 300 dòng | **"Ngoại lệ có phạm vi ≤330"** | A14; **thay bởi** vòng 6 (≤ 400) |
| 5 | Checkpoint lần 2: lớp `dot-bien-tuong-duong-hoac-thieu` xuất hiện **lần thứ 4** (codex lượt 3, chín biểu hiện) | **"Chuyển độ phủ sang triển khai"** | A0 (bảng phủ mệnh đề là sản phẩm bắt buộc của executor, codex kiểm trên mã thật) · §5.0 thành hợp đồng phủ · thêm 9 guard đã đo vào A6/A7/A8 · lượt codex 4/4 chỉ hỏi hợp đồng ấy có đóng được lớp ở tầng đặc tả không |
| 6 | Checkpoint lần 3: hết trần 4/4 lượt codex, lớp đột biến **lần thứ 5**, hai chuyển tiếp liền 0/1 (§12) | **"Đồng ý, làm revision 5 rồi soạn human audit"**, theo đề xuất: (1) chép hợp đồng phủ codex lượt 4 đề xuất; (2) ngoại lệ dòng ≤ 400; (3) không gọi codex thêm cho đặc tả, đóng băng bằng human audit, dồn ngân sách codex cho PR thi công | §5.0 · A0 · A2 · A6 · A7 · A14 · §9 |

Hai chỉ thị reviewer, như chủ kho gõ trong phiên 25-09-2026 (không có bản trên GitHub), theo thứ tự thời gian:
*"Do codex đã hết quota, thay cross review bằng same provider reviewer với effort hoặc mô hình ở mức cao hơn"*,
rồi *"Codex đã sống lại, hãy quay lại sử dụng codex để cross review"*. Chỉ thị sau đang hiệu lực.

## 1. Số đo — `origin/master` `0e2fe847`, đo **04:08Z–04:36Z 25-09-2026**

**Receipt thật làm mẫu hình dạng.** PR #589 head `af6b54cd…`, check-run `thu-hoi` `107905495884` success,
run `36081907282` attempt 1, artifact `10842182657` `thu-hoi-receipt-af6b54cd…-1`: zip **1102 byte**
(digest `sha256:43ee2205…918a90d`, hết hạn 2026-12-24), chứa đúng một tệp `receipt.json` **1863 byte**,
không BOM, sha256 của `receipt.json` `ca67dc6a…`. Artifact tải về lúc **03:05:00Z** (mtime tệp `art.zip`); kích thước
và băm đo lại lúc **04:36:31Z**, khớp.

Kiểu của **38** khoá trong receipt ấy (đo bằng `json.loads` + `type()` lúc ~04:0xZ, không có log phút; cross-review
lượt 1 đo lại độc lập lúc 04:23–04:35Z bằng AST producer: 24 khoá từ `lease_publish.py` + 14 từ workflow = 38, khớp), và nơi producer ghi nó:

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
(`ci_dang_ky_test.py` d.29 tại `0e2fe847`; d.**36** tại `b7396160`, xem §11) thì CI mới chạy và đối chiếu N/N; xoá dòng đăng ký thì `kiem()` báo test sống
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
| **M1** | Hàm thuần `kiem_json(raw: bytes, *, kho: str, nhanh: str, base_hien_hanh: str, head_hien_hanh: str) -> dict` trả `{"ok": bool, "luat": {"K1": "qua"\|"do", …}, "ly_do": [str, …]}`, và CLI `kiem-json --receipt <tệp> --kho <owner/repo> --nhanh-mac-dinh <tên> --base-hien-hanh <oid> --head-hien-hanh <oid>` in đúng dict ấy thành **một dòng JSON**. Thoát **0** khi `ok`; **12** khi có luật `do`; **2** khi tham số sai hoặc không đọc được tệp (`OSError`). Bốn tham số chuỗi phải khác rỗng; `--base/--head` phải hex thường 40 ký tự, sai ⇒ 2. Mọi luật đều được chạy và ghi trạng thái (không dừng ở luật đỏ đầu tiên), trừ khi K1 đỏ thì K2–K5 ghi `do` với lý do "K1 đỏ". **`ok: true` của C1a1a KHÔNG phải quyền land** và không chứng minh provenance: nó chỉ nói receipt có hình dạng, kiểu, danh tính kho, độ tươi và kết luận đúng so với tham số. Provenance cần C1a1b + C1a2 + C1b | L3 |
| **M2** | **K1 — hình dạng.** (a) Ba byte đầu là `EF BB BF` ⇒ đỏ. Kiểm **trước** giải mã. Chốt này **trùng** với parser `str` (`json.loads('\ufeff…')` ném `JSONDecodeError: Unexpected UTF-8 BOM`, đo 04:36Z); giữ cả hai có chủ ý, và A2 đo bằng đột biến ghép. (b) Giải mã `raw` **một lần** bằng UTF-8 **strict**; `UnicodeDecodeError` ⇒ đỏ. (c) `json.loads` nhận **chính chuỗi `str` đã giải mã**, không bao giờ nhận `bytes` (overload `bytes` tự nhận UTF-16/UTF-32: đo 04:36Z, cả bốn mã hoá UTF-16LE/BE, UTF-32LE/BE của receipt thật đều được `json.loads(bytes)` nhận, còn đường `str` bác cả bốn bằng `JSONDecodeError`); `JSONDecodeError` ⇒ đỏ. (d) Kết quả phải là `dict`. (e) Tập khoá **khít đúng 38 khoá** ở §1: thiếu một khoá ⇒ đỏ, thừa một khoá ⇒ đỏ. (f) `schema_version == 1` và là `int` không phải `bool`. (g) `event == "thu_hoi_admission_receipt"` | chọn "thiếu trường ⇒ 12" |
| **M3** | **K2 — kiểu.** Theo đúng bảng §1: nhóm hex 40 là `str` khớp `^[0-9a-f]{40}$`, riêng `oid_bo_kiem_tai_S` được thêm `null`. `workflow_definition_sha256` khớp `^[0-9a-f]{64}$`. Nhóm số nguyên là `int` và **không phải** `bool`; `job_id` **không** được `null`. `thoi_diem_utc` khớp `^\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$`. `descriptor_q13_ghim` là `null` hoặc hex 64. `policy_T` là `null` hoặc `dict`. `profile_digest` là `null` hoặc `str`. `discovery` là `str`. `so_thu_hoi_S` `so_thu_hoi_T` `ngan_sach` là `dict`; `metadata_T` `thu_hoi_moi` là `list`. Ba trường C phải **bằng nhau**: `checkout_commit == bo_kiem_da_chay_commit == workflow_definition_commit` | producer §1 |
| **M4** | **K3 — danh tính kho.** Lấy từ **tham số**, không từ receipt: `repository == kho`; `kho_canonical == "github.com/" + kho`; `nhanh_mac_dinh == nhanh`; `workflow_ref == kho + "/.github/workflows/ops-thu-hoi-admission.yml@refs/heads/" + nhanh` | review lượt 1, lớp `tieu-chi-mau-thuan-luat-hoac-producer` |
| **M5** | **K4 — stale.** `S == base_hien_hanh` và `H == head_hien_hanh`. Lệch một trong hai ⇒ đỏ ("receipt stale, chạy lại"). Hợp đồng với caller ghi ở §8 | nghĩa vụ #618 mục 3 |
| **M6** | **K5 — kết luận bộ kiểm.** `checker_rc == 0` (đã là `int` không `bool` nhờ K2); `ket_luan` thuộc tập đóng `{"TAP_THU_HOI_RONG"}`; `che_do == "chua_kich_hoat"`. Giá trị lạ ⇒ đỏ; mở rộng tập phải qua revision. Khi A1b đổi `che_do`, bộ kiểm này **phải** đỏ tới khi có revision, và đó là chủ ý | producer §1 |
| **M7** | `.claude/dev/doc_receipt_thu_hoi_test.py`: dựng **fixture dương** từ bảng §1 (38 khoá, giá trị của receipt mẫu, viết thẳng trong test, không đọc artifact), rồi mỗi ca âm là **một biến đổi logic** của fixture ấy. Ca cả nhóm theo hợp đồng §5.0 (A8: nhóm kho ba trường, nhóm nhánh hai trường) và ca phối hợp A11 (K3 + K4) phải liệt kê các trường chúng đổi. Đột biến chạy trên **bản sao tạm** của module (không sửa tệp thật), nạp bằng `importlib` với `sys.dont_write_bytecode = True`. Suite in dòng tổng `doc_receipt_thu_hoi tests: N/N ca QUA · M/M dot bien GIET` | L3 |
| **M8** | Đăng ký `.claude/dev/doc_receipt_thu_hoi_test.py` vào `MOI` của `ci_dang_ky_test.py`. Regex **tự buộc** từng cặp bằng nhau và lớn hơn 0 bằng backreference: `r'^doc_receipt_thu_hoi tests: ([1-9]\d*)/(\1) ca QUA · ([1-9]\d*)/(\3) dot bien GIET$'`. **Không** dựa vào `bang_chung_xanh` để so: hàm ấy (`ci_dang_ky_test.py` d.605–609 tại `0e2fe847`; d.**612–616** tại `b7396160`, thân hàm không đổi) chỉ so khi regex có **đúng hai** nhóm, nên với bốn nhóm nó trả `True` mà không so gì (cross-review lượt 1 đo). Không sửa `bang_chung_xanh` dùng chung | `ci_dang_ky_test.py` |

## 5. `nghiem_thu` — mỗi tiêu chí nêu phép đo làm nó ĐỎ (L3)

### 5.0 Hợp đồng phủ mệnh đề (revision 5; chép đề xuất của codex lượt 4, thay bản revision 4)

**Vì sao đổi.** Lớp `dot-bien-tuong-duong-hoac-thieu` xuất hiện ở **năm** lượt review (same-provider 1, codex 1–4).
Revision 3 dùng checklist nguồn chuẩn; revision 4 chuyển độ phủ sang bảng A0 kèm ngoại lệ "ca âm từng trường tự nó
là bằng chứng". Codex lượt 4 bác ngoại lệ ấy bằng phép đo: bỏ chốt kiểu của **cả ba** trường C thì suite vẫn
136/136 · 45/45, và receipt có ba C cùng là 39 ký tự được nhận `ok=true`. Bỏ từng chốt riêng là tương đương (quan hệ
C che nó), bỏ cả nhóm thì không. Lượt 4 còn chỉ ra yêu cầu cô lập tuyệt đối mâu thuẫn với M1, và `P/P menh de` chưa
có cách đếm. Hợp đồng dưới đây là đề xuất của lượt 4, chép gần nguyên văn.

**Bảng nghĩa vụ.** Lập từ văn bản M1–M6, **không** sinh từ danh sách ca đã có. Mỗi ID ghi: mệnh đề hành vi, miền đầu
vào, vị trí mã thực hiện hoặc các chốt suy ra nó, oracle quan sát, ca, và kết quả đo. Predicate ghép được tách thành
các điều kiện của nó, kèm tập trường áp dụng. Ghi riêng: quan hệ giữa các trường; quan hệ giữa tham số và nhóm trường
phụ thuộc nó (`kho`: `repository`, `kho_canonical`, phần kho của `workflow_ref`; `nhanh`: `nhanh_mac_dinh`, phần nhánh
của `workflow_ref`); và mọi thành phần **hằng** của chuỗi ghép (tiền tố `github.com/`; đường
`.github/workflows/ops-thu-hoi-admission.yml`; loại ref `@refs/heads/`). Nhóm quan hệ C được kiểm bằng cách **loại
từng trường khỏi ràng buộc đồng nhất với hai trường còn lại**; không quy định số cạnh của biểu thức so sánh.

**Ca phân biệt** phải làm đúng oracle của nó đổi màu. Luật hoặc chốt phụ tất yếu cùng đỏ thì **khai ra**, không đòi
chúng xanh: K1 đỏ thì K2–K5 cùng `do` theo M1; S/H sai miền thì cả K2 lẫn K4 đỏ; không truyền tham số caller sai
miền để giữ K4 xanh. Ca sai kiểu đơn trường **không** tự chứng minh predicate đã được áp cho trường ấy. Khi một chốt
khác che nó, phải ghi quan hệ che và đo **nhóm chốt / nhóm trường** liên quan, hoặc chứng minh thuộc tính vẫn được
suy ra từ các chốt còn lại. Mọi suy luận tương đương xét trên **mã cuối cùng**; không cộng các kết luận tương đương
của từng phép bỏ riêng rồi suy ra bỏ cả nhóm cũng tương đương.

**Disposition.** Mỗi ID có đúng một: `witness_killed` (có đột biến làm sai mệnh đề, và ca đích thất bại đúng
assertion của nó), `equivalent_verified` (đột biến tương đương, kèm lập luận phụ thuộc và phép đo để reviewer kiểm),
hoặc `unresolved`. **Chặn merge** nếu: thiếu ID cho một mệnh đề của M1–M6; oracle không phân biệt; tương đương chưa
được kiểm; hoặc còn `unresolved`. Mutant tương đương không được đếm là đã giết. Một mutant bị nhiều ca giết vẫn hợp
lệ; chỉ bắt buộc đúng assertion đích thất bại, không bắt buộc chỉ ca đó thất bại.

**Đếm P.** `P_tong` = số ID nghĩa vụ khác nhau trong bảng, sau khi đã đối chiếu với M1–M6. `P_phu` chỉ đếm ID có
`witness_killed` chạy thật thành công hoặc `equivalent_verified`. Suite in ba số riêng: số `witness_killed`, số
`equivalent_verified`, số `unresolved`, **tính từ kết quả chạy**, không từ độ dài danh sách ca. Việc đối chiếu bảng
với văn bản M1–M6 là **audit bắt buộc của reviewer PR thi công**; dòng P do suite in và hai cặp N/M của M8 **không**
thay được audit ấy.

**Ngoài phạm vi C1a1a.** Receipt đổi **cả ba** trường C sang **cùng** một commit khác, đúng kiểu hex40, vẫn qua C1a1a:
đó là ca **dương** của giới hạn lát này (C chỉ đo được bằng git, C1a1b N1/N7). Ba C **bất đồng**, hoặc cả ba cùng
**sai kiểu**, phải bị bác (A7).

"Đột biến X ⇒ ca Y ĐỎ" nghĩa là: chạy ca Y trên bản sao module đã đột biến X, ca Y phải **thất bại vì đúng
assertion của nó** (lớp ngoại lệ riêng, kèm tên ca), không vì lỗi vô can (bài học #355/#359).

| # | tiêu chí | phép đo làm nó **ĐỎ** |
|---|---|---|
| **A1** | Fixture dương ⇒ `ok: true`, cả năm luật `qua`, CLI rc 0 | Mọi đột biến ở dưới giữ fixture dương xanh; đột biến nào làm fixture dương đỏ là đột biến quá tay và phải đổi |
| **A2** | Có BOM ⇒ K1 `do`. Bốn ca UTF-16LE/BE, UTF-32LE/BE không BOM (38 khoá, giá trị như fixture) ⇒ K1 `do` | Đột biến **ghép**: bỏ chốt ba byte đầu **và** cho parser bỏ `U+FEFF` đầu chuỗi ⇒ ca BOM ĐỎ. Đột biến bỏ riêng chốt ba byte đầu có disposition `equivalent_verified` (parser `str` vẫn chặn), không được đếm là đã giết. Đột biến đổi `json.loads(chuoi)` thành `json.loads(raw)` ⇒ cả bốn ca UTF-16/32 ĐỎ |
| **A3** | Byte `0x80` giữa thân ⇒ K1 `do`, không ném ngoại lệ trần | Đột biến bỏ `try` quanh giải mã ⇒ ca ĐỎ vì kiểu ngoại lệ sai |
| **A4** | Thiếu **từng** khoá trong 38 (lặp đủ 38) ⇒ K1 `do`; thừa một khoá ⇒ K1 `do` | Đột biến đổi phép so tập khít thành `issubset` ⇒ ca "thừa khoá" ĐỎ. Đột biến đổi thành `issuperset` ⇒ ca "thiếu khoá" ĐỎ. Hai đột biến, hai ca đích khác nhau |
| **A5** | `schema_version = True` ⇒ K1 `do` (vì `True == 1` trong Python); `schema_version = 2` ⇒ K1 `do` | Đột biến dùng `== 1` không kiểm kiểu ⇒ ca `True` ĐỎ. Đột biến bỏ phép so giá trị ⇒ ca `2` ĐỎ |
| **A5b** | `event = "thu_hoi_admission_receipt_v2"` ⇒ K1 `do` | Đột biến bỏ phép so `event` ⇒ ca ĐỎ. (Revision 2 có luật M2(g) mà **không** có ca nào; checklist của revision 3 bắt được) |
| **A6** | **Mỗi trường** trong 38 khoá có ít nhất một ca âm **riêng** với giá trị sai miền của nhóm nó (bảng trường → nhóm viết **trong test**, độc lập với hằng của module). Trường mà K1 chặn trước (`schema_version`, `event`) khai là K1 chặn, không tính làm bằng chứng K2. Trường có chốt kiểu bị chốt khác che (ba trường C bị quan hệ đồng nhất che) thì theo §5.0: ghi quan hệ che và có ca **cả nhóm** | Mỗi **predicate** có một đột biến nới nó ⇒ các ca của predicate ấy ĐỎ. Bỏ áp predicate cho một trường không bị che ⇒ ca riêng của trường ấy ĐỎ. Với trường bị che, đột biến bỏ **cả nhóm** chốt ⇒ ca cả nhóm ĐỎ (xem A7) |
| **A7** | Ba ca, mỗi ca **loại một** trường C khỏi ràng buộc đồng nhất: đổi đúng trường ấy sang một hex40 hợp lệ khác, hai trường còn lại giữ nguyên ⇒ K2 `do`. Ca **cả nhóm sai kiểu**: cả ba C cùng là chuỗi 39 ký tự ⇒ K2 `do`. Ca dương: cả ba cùng đổi sang một hex40 khác ⇒ K2 `qua` (giới hạn §5.0) | Ba đột biến, mỗi đột biến bỏ **một trường** khỏi ràng buộc đồng nhất ⇒ đúng ca của trường ấy ĐỎ. Đột biến bỏ chốt hex của **cả ba** trường C ⇒ ca cả nhóm sai kiểu ĐỎ (codex lượt 4 đo: đột biến này sống trên suite 136/136 · 45/45, và thêm ca cả nhóm thì 137/137 · 46/46 giết được nó). Bỏ chốt hex của **một** trường C: `equivalent_verified` (hai chốt kiểu còn lại cộng quan hệ đồng nhất suy ra kiểu của trường thứ ba) |
| **A8** | K3 theo §5.0: **năm ca đơn trường** (`repository`, `kho_canonical`, phần kho của `workflow_ref`, `nhanh_mac_dinh`, phần nhánh của `workflow_ref`), **ca cả nhóm kho** (đổi `repository`, `kho_canonical`, phần kho của `workflow_ref` sang `other/repo`), **ca cả nhóm nhánh** (đổi `nhanh_mac_dinh` và phần nhánh của `workflow_ref` sang nhánh khác), và **ba ca thành phần hằng**: `kho_canonical` đổi tiền tố host (`evil.example/ducthangho/tra-luat`); `workflow_ref` đổi đường workflow (`…/untrusted.yml@…`); `workflow_ref` đổi loại ref (`@refs/tags/`). Mọi ca giữ nguyên tham số caller, S, H và các trường khác | Đột biến `kho = receipt["repository"]` ⇒ **ca cả nhóm kho** ĐỎ (năm ca đơn trường không giết được nó: cross-review lượt 2 đo được 85/85 · 30/30 vẫn xanh với đột biến này trên revision 2). Đột biến `nhanh = receipt["nhanh_mac_dinh"]` ⇒ **ca cả nhóm nhánh** ĐỎ. Đột biến bỏ phép so `workflow_ref` ⇒ ca đơn trường `workflow_ref` ĐỎ. Ba đột biến nới từng thành phần hằng (chỉ giữ hậu tố `/<kho>` cho host; bỏ ràng buộc đường; cho phép `@refs/tags/`) ⇒ đúng ca thành phần ấy ĐỎ (codex lượt 3 đo: cả ba sống trên suite revision 3, và receipt tương ứng cho `ok=true`) |
| **A9** | K4 theo §5.0: `base_hien_hanh ≠ S` ⇒ `do`; `head_hien_hanh ≠ H` ⇒ `do` | Đột biến bỏ từng vế ⇒ đúng ca của vế ấy ĐỎ. Đột biến `base = receipt["S"]` ⇒ ca `base` ĐỎ; `head = receipt["H"]` ⇒ ca `head` ĐỎ |
| **A10** | K5: `checker_rc = 1` ⇒ `do`; `ket_luan` lạ ⇒ `do`; `che_do = "da_kich_hoat"` ⇒ `do` | Đột biến bỏ từng vế ⇒ đúng ca ĐỎ |
| **A11** | Mọi luật được ghi trạng thái: ca đỏ đồng thời K3 và K4 ⇒ `luat` có **cả hai** `do` | Đột biến "dừng ở luật đỏ đầu tiên" ⇒ ca ĐỎ |
| **A12** | CLI: rc 0 / 12 / 2 đúng như M1; tệp không tồn tại ⇒ 2; `--base` 39 ký tự ⇒ 2 | Đọc `rc` trực tiếp từ `subprocess.run`, không qua pipe |
| **A13** | Suite in **N/N và M/M, mỗi cặp hai số bằng nhau**; `ci_dang_ky_test.py --chay` nhận tệp mới, rc 0. Trong suite, gọi `chay_moi` (hoặc `bang_chung_xanh`) với **đúng regex đăng ký** và runner giả rc 0: dòng dương được nhận; lệch riêng cặp ca, lệch riêng cặp đột biến, cả hai lệch, và `0/0` đều bị bác | Xoá dòng đăng ký ⇒ `ci_dang_ky_test.py` ĐỎ. Đột biến thay `(\1)` hoặc `(\3)` bằng `(\d+)` ⇒ đúng ca lệch của cặp ấy ĐỎ |
| **A14** | `git diff --numstat origin/master..<head>` chạm **đúng ba** đường của write set, và **tổng dòng thêm ≤ 400** theo **ngoại lệ có phạm vi** của ADR-0044 (chủ kho, §0 vòng 6 thay vòng 4: ≤ 3 tệp, ≤ 400 dòng thêm, chỉ cho C1a1a; trần gốc lớp `sensitive` là 300) | Vượt 400 ⇒ executor **DỪNG** và hỏi chủ kho, **không** cắt ca hay gộp ID để vừa trần. PR phải ghi số numstat thật và gọi đúng tên là *ngoại lệ*, không viết "ADR-0044 ĐẠT" |
| **A0** | Executor nộp **bảng nghĩa vụ** theo hợp đồng §5.0, dạng bảng dữ liệu hoặc docstring trong `.claude/dev/doc_receipt_thu_hoi_test.py` (không thêm đường thứ tư vào write set). Mỗi ID có disposition. Suite in `witness_killed`, `equivalent_verified`, `unresolved` từ kết quả chạy, và `unresolved` phải bằng 0 | Cross-review PR thi công đối chiếu ngược từ văn bản M1–M6 sang bảng. Mệnh đề thiếu ID, oracle không phân biệt, tương đương chưa kiểm được, hoặc `unresolved` > 0 là **finding chặn merge**. Dòng P và hai cặp N/M không thay audit này |
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
chứ không vá thêm. Cách đã đổi: (1) ranh giới mới — C1a1a là hàm thuần, không chạy git hay mạng, nên đo được độc lập; (2) nguồn
của `base/head` thành **hợp đồng** bắt buộc với caller ở §8, có ca nghiệm thu ở C1b; (3) mọi fact cần đo độc lập
bằng git dồn sang C1a1b, kèm các luật mà review lượt 1 đã chỉ ra.

**Lớp này CHƯA đóng** (cross-review codex lượt 1 đánh giá, và đặc tả nhận đúng như vậy): tách lát là hợp lệ,
nhưng chuyển fact sang C1a1b và hứa ca ở C1b chưa phải đã chữa. Lớp giữ trạng thái mở tới khi C1a1b, C1a2 và
C1b đo và nối đủ. Không nơi nào được quảng bá `ok` của C1a1a là receipt đã xác minh provenance (M1).

## 7. `chua_do_duoc`

1. **Số dòng thêm.** Codex lượt 4 (08:13–08:16Z 25-09) đo prototype theo revision 4, **chưa** có bảng nghĩa vụ đầy đủ:
   **+344** (module 90, test 253, đăng ký 1); thêm ca và đột biến cả nhóm C: **+346**. Bảng nghĩa vụ (A0) còn thêm
   dòng. Đó là căn cứ ngoại lệ ≤ 400. Ước tổng ~360–395 là **ước**, chưa đo; chốt A14 đo trên mã thật.
   Trước đó, cross-review codex lượt 3 (04:55Z–05:02Z) đo prototype theo revision 3: **+307**; thêm chín guard
   của finding lượt 3: **+325** (module 89, test 235, đăng ký 1). Revision 4 còn đòi ca riêng cho **từng** trường (A6)
   và bảng phủ (A0). Viết bằng bảng dữ liệu thì ước thêm ~10–25 dòng, tức **có thể vượt 330**. Chốt A14 giữ nguyên:
   vượt thì dừng và hỏi chủ kho, **không** được cắt ca để vừa trần.
   Trước đó, cross-review codex lượt 2 (04:40–04:48Z) đo prototype theo revision 2: **+297**; thêm ca cả nhóm
   kho và đột biến của nó: **+300** (module 89, test 210, đăng ký 1). Revision 3 còn thêm ca `schema_version = 2`,
   A5b và hai đột biến `base/head` lấy từ receipt, nên dự kiến vượt 300 vài dòng: đó là lý do chủ kho cấp
   ngoại lệ ≤ 330 (A14). Trước đó, cross-review codex lượt 1 viết prototype và đo bằng `git diff --no-index --numstat`
   (04:23–04:35Z): module **+91**, test **+195** (85 ca, 28 đột biến), đăng ký **+1**, tổng **+287** trên 3 đường.
   Đó là prototype của reviewer, **không** phải numstat của mã thi công; còn 13 dòng tới trần 300. Chốt A14 giữ
   nguyên: vượt thì dừng và hỏi.
2. **Receipt thật cho ca S ≠ C.** Phiên soạn đặc tả chỉ đọc **một** receipt (PR #589, tải lúc 03:05:00Z), và đó là ca
   S = C. Chưa tìm receipt S ≠ C nào. Không ảnh hưởng C1a1a, vì C1a1a không so đồ thị;
   nó là tiền đề của C1a1b.
3. **Producer đổi tập khoá hoặc `che_do`.** Tập khoá khít (M2) và `che_do` hằng (M6) làm consumer đỏ tới khi
   có revision. Đó là chủ ý (fail-close), nhưng chưa có cổng nào báo sớm khi producer đổi. Ghi nợ cho C1b.
4. **`job_id` có từng là `null` trên receipt thật không.** Mẫu có `int`. M3 bác `null`; nếu producer thật
   sự phát `null` ở ca nào đó, consumer sẽ đỏ và cần xem lại producer, không nới consumer.
5. **Assurance.** Xem §9.

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

- Reviewer: **codex** (`gpt-6-astra`, effort từ `medium` trở lên; đặc tả lớp `sensitive` dùng `high`), theo chỉ thị
  đang hiệu lực ở §0. Lặp vá và cross-review theo **lớp lỗi** tới khi hết P1/P2/P3. Mỗi lượt đăng verdict.
- Nâng trần trục LỜI GỌI, khai **trước** khi phóng lượt codex thứ 3 (ADR-0043):

  ```yaml
  nang_tran:
    truc: codex_review_calls_used
    ai_nang: ducthangho (chủ kho), lựa chọn "Đổi phương pháp + nâng trần 2→4" trong phiên 25-09-2026
    can_cu: >-
      Review Rescue Checkpoint (protocol §12 d.1054, d.1076): hết trần 2 lượt codex và lớp
      dot-bien-tuong-duong-hoac-thieu xuất hiện ở 3 lượt review. Chủ kho chọn đổi phương pháp
      (§5.0), không vá thêm theo chỗ bị chỉ.
    tran_cu: 2
    tran_moi: 4
    da_dung_truoc_khi_nang: 2   # run 0ef2c936 (lượt 1), a0fb6806 (lượt 2)
  ```

  Đã dùng **4/4** (lượt 3: run `2452e13b`; lượt 4: run `aa19c808`). Lượt 4 còn P2 (lớp đột biến lần thứ 5).
- **Đặc tả đóng băng bằng human audit của chủ kho**, không gọi thêm codex cho đặc tả (§0 vòng 6). Hệ quả phải khai:
  đặc tả này **không có** `cross_approved`. Đó là lựa chọn có chủ ý: bốn lượt codex liền đều tìm ra lỗi thật nhưng cùng
  một lớp, tỷ lệ đóng 0%; bằng chứng độ phủ đáng tin nằm trên **mã thật** của PR thi công, không trên văn bản đặc tả.
  Lớp `dot-bien-tuong-duong-hoac-thieu` vì thế **vẫn mở**, và được chuyển thành nghĩa vụ chặn merge của PR thi công
  (A0), không được ghi là đã đóng.
- Cross-review của **PR thi công** là một trục khác (trần lời gọi riêng của PR ấy), dùng codex `gpt-6-astra` effort `high`,
  và có nhiệm vụ bắt buộc: audit bảng nghĩa vụ A0 trên mã thật, đối chiếu ngược từ M1–M6.
- Lượt review same-provider trên bản nháp C1a1 (trước khi codex hoạt động lại) được giữ làm **lịch sử**, không
  tính là approval. Protocol §8 d.652: `same_provider_approved` không thay được `cross_approved` cho lớp
  `sensitive`.
- Nếu codex không cho được approval trên exact head, merge cần **human audit của chủ kho**, và PR phải khai thẳng
  là không có `cross_approved`.
- Không CI, không full CI cho tới khi đủ điều kiện merge. Không CI Windows.

## 10. Lịch sử review

| lượt | reviewer | đối tượng | verdict | P1 | P2 | P3 | ghi chú |
|---|---|---|---|---:|---:|---:|---|
| 1 (same-provider) | Claude cùng provider, model cao hơn | bản nháp C1a1 `21e92702` | request_changes | 0 | 6 | 2 | dẫn tới tách C1a1a/C1a1b (§0 vòng 3) |
| 1 (codex) | `gpt-6-astra` effort `high`, run `0ef2c936`, 04:21:43–04:36:05Z | revision 1 `11a97f47` | request_changes | 0 | 2 | 1 | `dot-bien-tuong-duong-hoac-thieu` (đường parse, đột biến BOM) · `loi-khai-rong-hon-phep-do` (regex bốn nhóm không được so) · `mau-thuan-noi-tai-va-so-thieu-don-vi-thoi-diem` (giờ giữ chỗ, ca phối hợp A8). Revision 2 vá cả ba ở M1, M2, M7, M8, A2, A8, A13, §1, §6, §7, §9 |
| 2 (codex) | `gpt-6-astra` effort `high`, run `a0fb6806`, 04:38:04–04:49:04Z | revision 2 `90675fa3` | request_changes | 0 | 1 | 0 | Hai lớp của lượt 1 đã vá thật. Còn `dot-bien-tuong-duong-hoac-thieu`: thiếu ca cả nhóm **kho** (đột biến `kho = receipt["repository"]` sống, nhận receipt kho khác với `ok=true`). Lớp này đã ở 3 lượt ⇒ Review Rescue Checkpoint. Revision 3 đổi phương pháp (§5.0) và rà toàn đặc tả theo checklist; bắt thêm A5b (`event` không có ca) và hai đột biến `base/head` lấy từ receipt |
| 3 (codex) | `gpt-6-astra` effort `high`, run `2452e13b`, 04:52:51–05:02:33Z | revision 3 `ee02122b` | request_changes | 0 | 1 | 0 | Biểu hiện r1/r2 đã vá thật; các ca cả nhóm kho/nhánh và base/head có răng. Còn `dot-bien-tuong-duong-hoac-thieu`, **lần thứ 4**, chín biểu hiện: ba thành phần hằng của K3, hai vế C, bốn trường chưa được áp predicate kiểu. Chủ kho qua checkpoint lần 2 và chọn chuyển độ phủ sang triển khai: revision 4 thêm A0 và chín guard, §5.0 thành hợp đồng phủ mệnh đề |
| 4 (codex) | `gpt-6-astra` effort `high`, run `aa19c808`, 08:10:15–08:20:43Z | revision 4 `0c8c3532` | request_changes | 0 | 1 | 0 | Chín guard lượt 3 vào đúng chỗ. Lớp đột biến **lần thứ 5**, trong chính hợp đồng phủ: ngoại lệ loại (c) sai khi chốt che nhau (bỏ chốt kiểu cả ba C sống, nhận C 39 ký tự); cô lập tuyệt đối mâu thuẫn M1; `P/P` chưa có cách đếm. Hết trần 4/4. Chủ kho qua checkpoint lần 3: revision 5 chép hợp đồng lượt 4 đề xuất, ngoại lệ ≤ 400, đóng băng bằng human audit |

## 11. Đo lại khi hợp nhất master — `origin/master` `b7396160`, **07:43Z 26-09-2026**

Nhánh đặc tả hợp nhất 84 commit mới của master (merge `dcb5267a`, không xung đột). §1 giữ nguyên làm lịch sử;
bảng dưới là số hiện hành. Các lời khai trong §1–§9 không bị viết lại, chỉ hai trích dẫn dòng được ghi kèm vị trí mới.

| đại lượng | tại `0e2fe847` (§1) | tại `b7396160` | hệ quả |
|---|---|---|---|
| producer `ops/lease_publish.py` + workflow `thu-hoi` | — | `git diff --stat 0e2fe847 b7396160 --` hai tệp: **rỗng** | bảng 38 khoá và kiểu ở §1 còn đúng |
| `ci_dang_ky_test.py` | — | **+293/−11** (packet #637, song song hoá registry) | vị trí `MOI` và `bang_chung_xanh` trôi (dưới) |
| dòng `MOI = {` | d.29 | d.**36** | chỉ trích dẫn |
| `bang_chung_xanh` | d.605–609 | d.**612–616**, thân **không đổi** (vẫn `len(m.groups()) != 2`) | M8 và regex backreference còn nguyên giá trị |
| `chay_moi` gọi `bang_chung_xanh` | trực tiếp | qua `mau_theo_nen(path, mau, la_windows)` với `any(...)` | cross-review PR thi công phải đo lại regex M8 trên `chay_moi` mới |
| `ai-dang-giu .claude/dev/doc_receipt_thu_hoi.py` | rc 0 · 0 | rc 0 · **0** | — |
| `ai-dang-giu .claude/dev/doc_receipt_thu_hoi_test.py` | rc 0 · 0 | rc 0 · **0** | — |
| `ai-dang-giu .claude/dev/ci_dang_ky_test.py` | rc 0 · 0 | rc **11** · **1**: `ci-registry-dot-bien-theo-diff-r1-g1-claude` (packet **#643**, hết `2026-09-27T01:20:00Z`) | **chặn cấp lease C1a1a** tới khi đường ấy về 0 |

**Lease C1a1a chỉ được cấp sau khi đo lại `ai-dang-giu` cả ba đường ra `NGƯỜI_GIỮ 0`**, không suy từ giờ hết hạn
(nợ `AG-T0-01B`: lease không tự chết khi packet đã land).
