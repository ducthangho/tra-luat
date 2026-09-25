# ĐẶC TẢ — `LAND-DOC-RECEIPT-THU-HOI-C1a1` — **revision 1**

| trường | giá trị |
|---|---|
| `packet_id` | `LAND-DOC-RECEIPT-THU-HOI-C1a1`. Đây là lát **đầu** của C1 (`#499` §C1): bộ kiểm receipt **offline** đối chiếu facts git độc lập |
| `packet_issue` | **CHƯA ĐĂNG**. Đặc tả không cấp việc (soan-spec §5); phải có Issue và lease còn hiệu lực mới được giao |
| `nguon_cap_viec` | `#499` §C1 · nghĩa vụ S≠C từ `#618`, chuyển sang tại `#499` comment `5819877014` · hợp đồng M9 trong spec cha `ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md` d.439–477 · quyết định chủ kho vòng 1–2 bên dưới |
| `review_class` | **`sensitive`**. Đây là bộ kiểm mà `land-packets` sẽ dựa vào để chấp nhận land (protocol §8 d.680: *review/land authority*) |
| `thay_the_cho` | không có. Đây là revision đầu |

**GIỚI HẠN LỜI KHAI:** mọi khẳng định trong tệp này chỉ chứng minh được tới đúng phép đo ghi kèm.
**Ba trạng thái:** có · không · **KHÔNG ĐO ĐƯỢC**. Trạng thái thứ ba làm cổng ĐỎ, không được làm tròn thành một trong hai trạng thái kia.

---

## 0. Quyết định của chủ kho

Mỏ neo: `#499` comment `5825988768` (quyết định Q1/Q3/biên giới A1a và "soạn spec C1"). Các câu vòng 1–2
dưới đây được chủ kho trả lời trong phiên 25-09-2026. Phiên agent ghi lại, theo đúng lựa chọn đã bấm.

| vòng | câu | chọn, nguyên văn | hệ quả |
|---|---|---|---|
| 1 | Chia C1 | **"Tách C1a / C1b"** | C1a = kiểm thuần offline · C1b = fetch API thật + nối vào `land-packets` |
| 1 | Luật S/C | **"S ≤ C ≤ master"** | M4, M5 |
| 1 | Receipt cũ thiếu trường | **"Thiếu trường ⇒ 12"** | M2, M6 |
| 1 | Assurance khi codex hết quota | **"Same-provider + human audit"** | §9 |
| 2 | C1a ~500 dòng > trần 300 | **"Tách tiếp C1a1 / C1a2"** | tệp này = **C1a1**. C1a2 = kiểm chuỗi join API từ response thô |

Chỉ thị reviewer, nguyên văn (25-09-2026): *"Do codex đã hết quota, thay cross review bằng same provider
reviewer với effort hoặc mô hình ở mức cao hơn"*.

## 1. Số đo — `origin/master` `601a0f18`, đo **03:0x–03:42Z 25-09-2026**

**Receipt thật dùng làm fixture dương.** PR #589 head `af6b54cd…`, check-run `thu-hoi` `107905495884` success,
suite `97710440275`, run `36081907282` attempt 1, artifact `10842182657`
`thu-hoi-receipt-af6b54cd…-1` (1102 B, digest `sha256:43ee2205…918a90d`, hết hạn 2026-12-24).
`receipt.json` có **38 khoá**:

```
H S T bo_kiem_da_chay_commit canh_ancestry che_do check_run_id checker_rc checkout_commit
descriptor_q13_ghim discovery event job_id ket_luan kho_canonical metadata_T ngan_sach
nhanh_mac_dinh oid_bo_kiem_da_chay oid_bo_kiem_tai_S policy_T profile_digest pull_request
repository run_attempt run_id schema_version so_object_da_doc so_thu_hoi_S so_thu_hoi_T
thoi_diem_utc thu_hoi_moi tong_bytes tree_S workflow_definition_blob
workflow_definition_commit workflow_definition_sha256 workflow_ref
```

Giá trị trong receipt ấy: `S = checkout_commit = bo_kiem_da_chay_commit = workflow_definition_commit = 601a0f18…`,
`oid_bo_kiem_da_chay = oid_bo_kiem_tai_S = 5e811ebb…`, `checker_rc = 0`, `ket_luan = TAP_THU_HOI_RONG`,
`che_do = chua_kich_hoat`. **Đây là ca S = C.** Chưa có receipt thật nào cho ca S ≠ C (xem `chua_do_duoc` #1).

**Producer phát `ket_luan` nào:** `ops/lease_publish.py:1890` chỉ có đúng một literal, `"TAP_THU_HOI_RONG"`,
đo bằng grep lúc 03:4xZ.

**Mốc định dạng receipt:** các khoá `bo_kiem_da_chay_commit`, `oid_bo_kiem_da_chay` và `checkout_commit` vào
master qua PR #620, merge commit `601a0f18c83057fa079d204122660f5697fc6389`. Receipt do producer trước mốc
này phát ra thiếu cả ba khoá.

| đường dẫn | `ai-dang-giu` 03:42Z (ref đủ: fetch `--prune` rồi đo) |
|---|---|
| `.claude/dev/doc_receipt_thu_hoi.py` (MỚI) | `rc=0` · NGƯỜI_GIỮ 0 |
| `.claude/dev/doc_receipt_thu_hoi_test.py` (MỚI) | `rc=0` · NGƯỜI_GIỮ 0 |
| `.claude/dev/ci_dang_ky_test.py` | `rc=0` · NGƯỜI_GIỮ 0 |

Lần đo đầu của `ci_dang_ky_test.py` trả `rc=12 KHÔNG_XÁC_ĐỊNH: cache thiếu nhánh máy chủ` vì remote vừa có
thêm hai nhánh. Fetch lại xong đo được `rc=0`. Ghi lại để không ai đọc nhầm lần đo hỏng thành "có người giữ".

**Vì sao cần `ci_dang_ky_test.py`:** tệp test mới dưới `.claude/dev/` phải có mặt trong sổ `MOI` của tệp ấy
(d.29) thì CI mới chạy nó và đối chiếu được N/N. Không đăng ký thì test tồn tại mà không ai chạy.

## 2. `write_set`

```
.claude/dev/doc_receipt_thu_hoi.py
.claude/dev/doc_receipt_thu_hoi_test.py
.claude/dev/ci_dang_ky_test.py
```

Đúng ba đường, không ký tự đại diện, đúng bằng trần tệp của ADR-0044 cho lớp `sensitive`. Hiện vật review
và bookkeeping (`ops/reviews/**`, `CHANGELOG.md`, `RELEASE_MANIFEST.json`) **KHÔNG** nằm trong write set.

## 3. `ngoai_pham_vi`

| thứ CỐ Ý không làm | lý do |
|---|---|
| Gọi API GitHub, tải artifact | C1b. C1a1 chỉ nhận **tệp** đã có trên đĩa |
| Kiểm chuỗi join check-run → suite → run → attempt jobs → artifact | C1a2. C1a1 **tin** không có trường nào trong nhóm `check_run_id`/`run_id`/`job_id`/`run_attempt`; nó chỉ kiểm kiểu của chúng |
| Nối vào `.claude/skills/land-packets/SKILL.md` hay `packet_loop.py` | C1b |
| Sửa producer (`ops-thu-hoi-admission.yml`, `ops/lease_publish.py`) | ngoài write set; `lease_publish.py` còn đang bị #589 giữ |
| Sửa §M9 của spec cha | spec cha là snapshot đã đóng băng; đặc tả này **thay** vế consumer của nó bằng các luật ở §4–§5 |
| Diễn giải `so_thu_hoi_*`, `thu_hoi_moi`, `policy_T`, `metadata_T`, `discovery` | ngữ nghĩa của sổ thu hồi thuộc A1a/A1b. C1a1 chỉ đòi các khoá ấy **có mặt** |
| CI, full CI, CI Windows, `workflow_dispatch`, rerun tay | chỉ thị chủ kho: không chạy tới khi đủ điều kiện merge · `manual_ci_budget: 0` · không Windows |

## 4. `muc_tieu` — mỗi dòng chiếu vào MỘT đường dẫn (L2)

Mọi mục tiêu dưới đây thuộc `.claude/dev/doc_receipt_thu_hoi.py`, trừ M10 và M11.

| # | mục tiêu | nguồn |
|---|---|---|
| **M1** | CLI `kiem --receipt <receipt.json> --repo <git dir> --master <oid> --base-hien-hanh <oid> --head-hien-hanh <oid> --kho <owner/repo> --nhanh-mac-dinh <ten>`. Thoát **0** khi mọi luật qua; thoát **12** khi bất kỳ luật nào đỏ **hoặc không đo được**; thoát **2** khi tham số sai. In một JSON một dòng: `{"ok": bool, "luat": {"K1": "qua"\|"do"\|"khong_do_duoc", …}, "ly_do": [...]}` | L3 |
| **M2** | **K1 — hình dạng.** JSON phải là object, và **tập khoá khít đúng 38 khoá** ở §1 (thiếu một khoá ⇒ 12, thừa một khoá ⇒ 12). `schema_version == 1`, `event == "thu_hoi_admission_receipt"`. Receipt đọc bằng **bytes thô** rồi `json.loads`; JSON hỏng hoặc UTF-8 hỏng ⇒ 12 | chọn "thiếu trường ⇒ 12" |
| **M3** | **K2 — kiểu.** `S`, `H`, `T`, `tree_S`, `checkout_commit`, `bo_kiem_da_chay_commit`, `workflow_definition_commit`, `oid_bo_kiem_da_chay`, `workflow_definition_blob` là hex thường, đúng 40 ký tự. `workflow_definition_sha256` là hex thường 64 ký tự. Ba trường C phải **bằng nhau**: `checkout_commit == bo_kiem_da_chay_commit == workflow_definition_commit` (gọi chung là **C**). `checker_rc` là `int` và **không phải** `bool` | producer #620 |
| **M4** | **K3 — S ≤ C.** `git merge-base --is-ancestor S C`: rc 0 ⇒ qua · rc 1 ⇒ đỏ · rc khác ⇒ **khong_do_duoc**. S = C là hợp lệ | chọn "S ≤ C ≤ master" |
| **M5** | **K4 — C ≤ master** (`--master`, oid do caller đưa). Cùng ba trạng thái như K3. **K5 — mốc ≤ C:** hằng `MOC_RECEIPT_C = "601a0f18c83057fa079d204122660f5697fc6389"`, đòi `merge-base --is-ancestor MOC C` rc 0 | "S ≤ C ≤ master" · "receipt cũ ⇒ 12" |
| **M6** | **K6 — mã đã chạy, đo độc lập.** `git rev-parse C:ops/lease_publish.py` phải bằng `oid_bo_kiem_da_chay`. Không đọc `oid_bo_kiem_tai_S` để quyết định (đó là dữ liệu nền về S, `#499` 5819877014) | nghĩa vụ #618 mục 2 |
| **M7** | **K7 — định nghĩa workflow.** `git rev-parse C:.github/workflows/ops-thu-hoi-admission.yml` phải bằng `workflow_definition_blob`, và sha256 của bytes blob ấy (`git cat-file blob`) phải bằng `workflow_definition_sha256`. `workflow_ref` phải bằng đúng `f"{kho}/.github/workflows/ops-thu-hoi-admission.yml@refs/heads/{ten}"` với `kho` và `ten` lấy từ **tham số** `--kho`/`--nhanh-mac-dinh`, không từ receipt. `repository`, `kho_canonical` và `nhanh_mac_dinh` trong receipt phải bằng hai tham số ấy | M9 spec cha: "actual workflow-definition commit+blob sha256" |
| **M8** | **K8 — cây.** `git rev-parse H^{tree}` phải bằng `T`, và `git rev-parse S^{tree}` phải bằng `tree_S`. Không có H hoặc S trong object store ⇒ **khong_do_duoc** ⇒ 12 | M9 spec cha "T=tree(H)" |
| **M9** | **K9 — stale.** `S == --base-hien-hanh` và `H == --head-hien-hanh`. Lệch một trong hai ⇒ đỏ ("receipt stale, chạy lại") | nghĩa vụ #618 mục 3: giữ stale-check đúng vai |
| **M10** | **K10 — kết luận bộ kiểm.** `checker_rc == 0` **và** `ket_luan` thuộc tập đóng `{"TAP_THU_HOI_RONG"}`. Giá trị lạ ⇒ đỏ. Tập mở rộng phải qua revision | producer §1 |
| **M11** | Mọi lời gọi git chạy **argv** (không `shell=True`), có `timeout`, `env` cố định `GIT_CONFIG_NOSYSTEM=1`, `GIT_TERMINAL_PROMPT=0`, `LC_ALL=C`. Hết giờ hoặc `OSError` ⇒ **khong_do_duoc**, không ném ngoại lệ trần | bài học B2 của #499 |
| **M12** | Mỗi luật K1–K10 có ca dương và ca âm trong `.claude/dev/doc_receipt_thu_hoi_test.py`, dựng trên **đồ thị git thật** trong thư mục tạm (không stub git, bài học F1 của #620). Suite in dòng tổng khớp regex đăng ký ở M13 | `…_test.py` |
| **M13** | Đăng ký `.claude/dev/doc_receipt_thu_hoi_test.py` vào sổ `MOI` của `.claude/dev/ci_dang_ky_test.py`, kèm regex đếm N/N | `ci_dang_ky_test.py` |

## 5. `nghiem_thu` — mỗi tiêu chí nêu phép đo làm nó ĐỎ (L3)

| # | tiêu chí | phép đo làm nó **ĐỎ** |
|---|---|---|
| **A1** | Fixture dương dựng lại **đúng 38 khoá** và giá trị của receipt thật ở §1 (ca S = C), trên đồ thị git có C chứa `ops/lease_publish.py` và workflow. Kết quả `ok: true`, rc 0 | Bất kỳ đột biến nào dưới đây làm ca dương đỏ là đột biến quá tay |
| **A2** | **Ca S ≠ C:** đồ thị `MOC → S → C → master`, với blob `ops/lease_publish.py` tại S **khác** tại C, được nhận | Đột biến so `oid_bo_kiem_da_chay` với `S:ops/lease_publish.py` ⇒ ca A2 ĐỎ. Đây là chốt của nghĩa vụ #618 mục 4 |
| **A3** | Tráo OID: `oid_bo_kiem_da_chay` = blob tại S (không phải tại C) ⇒ 12 | Đột biến bỏ K6 ⇒ ca ĐỎ |
| **A4** | Tráo commit: `bo_kiem_da_chay_commit` khác `checkout_commit` ⇒ 12 | Đột biến bỏ phép so bằng nhau của ba trường C ⇒ ca ĐỎ |
| **A5** | S **không** là tổ tiên C (C nằm trên nhánh rẽ trước S) ⇒ 12 | Đột biến đảo toán hạng `--is-ancestor C S` ⇒ ca ĐỎ; đột biến `S S` ⇒ ca ĐỎ |
| **A6** | C không là tổ tiên master ⇒ 12 | Đột biến bỏ K4 ⇒ ca ĐỎ |
| **A7** | C là tổ tiên **thật sự** của MOC (receipt dạng cũ, C trước mốc) ⇒ 12 | Đột biến bỏ K5 ⇒ ca ĐỎ |
| **A8** | Thiếu **một** khoá bất kỳ ⇒ 12; thừa một khoá ⇒ 12. Bảng tham số theo từng khoá trong 38 khoá | Đột biến đổi phép so tập khít thành `issubset` ⇒ ca "thừa khoá" ĐỎ |
| **A9** | `T` lệch tree(H) ⇒ 12; `tree_S` lệch tree(S) ⇒ 12 | Đột biến bỏ từng vế ⇒ đúng ca của vế ấy ĐỎ |
| **A10** | `workflow_definition_sha256` lệch **một** ký tự ⇒ 12; `workflow_ref` sai nhánh ⇒ 12 | Đột biến bỏ phép so băm ⇒ ca ĐỎ |
| **A11** | Stale: `--base-hien-hanh` ≠ S ⇒ 12; `--head-hien-hanh` ≠ H ⇒ 12 | Đột biến bỏ K9 ⇒ ca ĐỎ |
| **A12** | `checker_rc = True` (bool) ⇒ 12; `checker_rc = 1` ⇒ 12; `ket_luan` lạ ⇒ 12 | Đột biến dùng `== 0` thay kiểm kiểu (`False == 0`) ⇒ ca `bool` ĐỎ |
| **A13** | H vắng trong object store ⇒ `khong_do_duoc` ⇒ 12 (không phải `do`, không phải `qua`) | Đột biến gộp `khong_do_duoc` vào `qua` ⇒ ca ĐỎ. Phân hạng theo **giá trị trạng thái**, không theo chuỗi thông điệp |
| **A14** | Receipt có BOM, hoặc byte `0x80` ⇒ 12, không ném `UnicodeDecodeError` trần | Đột biến bỏ `try` ⇒ ca ĐỎ vì kiểu ngoại lệ sai |
| **A15** | Suite in **N/N hai số bằng nhau**; `ci_dang_ky_test.py --chay` nhận tệp mới và `rc=0` | Đọc `rc` **trực tiếp**, không qua pipe. Xoá dòng đăng ký ⇒ `ci_dang_ky_test.py` ĐỎ (tệp test không có trong sổ) |
| **A16** | `git diff --numstat origin/master..<head>` chạm **đúng ba** đường của write set, và **tổng dòng thêm ≤ 300** | Vượt 300 ⇒ executor **DỪNG** và hỏi chủ kho. Không viết vào PR rằng ADR-0044 "ĐẠT" |
| **A17** | `python3 .claude/dev/packet_loop.py doctrine-scan --root .` rc 0; `adr-song` rc 0 | rc đọc trực tiếp |

**Không tiêu chí nào được đóng bằng `rc=0` trơn.** Mỗi tiêu chí đòi bằng chứng dương: hai số bằng nhau,
`ok: true`, hoặc một đột biến ĐỔI MÀU đúng ca đích. Đột biến chạy trên **bản sao** module, không sửa tệp thật.

## 6. `hinh_dang_ke_thua` (L4)

C1a1 không phải packet khắc phục, nhưng nó là **consumer** của chuỗi thu hồi lease, nên chép bộ đếm từ spec
A1a §7 (đo 20-09-2026) và thêm #618:

| hình dạng | số lần | nguồn |
|---|---|---|
| **"nguồn được tin mà chưa xác minh"** | **6** | r9 lượt 1, 2, 3, 4b, 5, 6 |
| "lời khai hội tụ rộng hơn phép đo" | 3 | r9 g2, lượt 1 |
| "hai cổng bất đồng" | 1 | r9, #473 |
| "cổng CÓ MẶT khác cổng ĐO ĐƯỢC" | 1 | #499 C2a |
| "stub bỏ qua toán hạng nên đột biến sống" | 1 | #620 F1 |
| "lời khai mốc cũ chưa cập nhật khắp nơi" | 1 (3 lượt liền) | #620 F3 |

Hình dạng đầu đã chạm **6**, và một consumer receipt **chính là** chỗ dễ lặp lại nó nhất: tin một trường mà
receipt tự khai. Vì vậy mọi luật ở §4 đều so với **fact tính độc lập từ git**. Một finding lớp này ở lượt review
đầu là **lần thứ 7**. Theo §12 protocol, lần đó phải đặt lại câu hỏi về cách làm, không vá thêm.

## 7. `chua_do_duoc`

1. **Receipt thật cho ca S ≠ C.** Chưa có (đo 03:4xZ: receipt duy nhất sau #620 là của #589, với S = C). A2 dùng
   đồ thị tổng hợp. Receipt thật đầu tiên có base tụt sau master cũng chính là phép thử thật của #618. Khi có,
   C1b (hoặc bookkeeping) phải chạy bộ kiểm trên nó và ghi kết quả.
2. **Số dòng thêm.** Ước bộ kiểm ~150, test ~140, đăng ký ~2, tổng ~290. Chưa có mã nên **chưa đo**. Chốt ở A16.
3. **Producer đổi tập khoá.** Tập khoá khít (M2) làm mọi thay đổi producer đỏ ở consumer cho tới khi có revision.
   Đó là chủ ý (fail-close), nhưng chưa có cổng nào báo sớm khi producer đổi. Ghi nợ cho C1b.
4. **`MOC_RECEIPT_C` đúng về ngữ nghĩa.** Đã đo: ba khoá mới xuất hiện ở receipt sau `601a0f18`. Chưa đo: có
   receipt nào do producer **trước** mốc mà vẫn mang đủ 38 khoá (ví dụ run trên PR #620 trước merge). Nếu có, K5
   bác nó. Đó là đúng ý, vì producer ấy chưa phải producer canonical.
5. **Assurance.** Xem §9. Không lượt review nào trong packet này cho được `cross_approved`.

## 8. Thứ tự

`C1a1` → `C1a2` → `C1b`. Mỗi lát được cấp lease sau khi lát trước land. `C1b` là lát duy nhất chạm
`land-packets`, và phải land **trước** A1b (bật cờ `SO_THU_HOI_KICH_HOAT`), đúng như spec cha đòi consumer
có trước cửa sổ kích hoạt.

## 9. Review và assurance

- Reviewer: Claude **cùng provider**, effort hoặc model **cao hơn** executor. Lặp vá và review theo **lớp lỗi**
  tới khi hết P1/P2/P3. Mỗi lượt đăng verdict.
- Protocol §8 d.652: `same_provider_approved` **không** thay được `cross_approved` cho lớp `sensitive`. Vì vậy
  merge cần thêm **human audit của chủ kho** trên exact head, như PR #620. Receipt và PR phải khai thẳng:
  *không có `cross_approved`*.
- Không CI, không full CI cho tới khi đủ điều kiện merge. Không CI Windows.
