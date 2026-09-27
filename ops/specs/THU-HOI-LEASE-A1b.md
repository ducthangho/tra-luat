# ĐẶC TẢ — `THU-HOI-LEASE-A1b` — **revision 1, bản nháp 1 (CHƯA đóng băng)**

| trường | giá trị |
|---|---|
| `packet_id` | `THU-HOI-LEASE-A1b` — nửa **cấu hình** của slice A1 (nửa **mã** là `THU-HOI-LEASE-A1a`) |
| `packet_issue` | **#656** (con của #564). Issue **không** cấp việc; chỉ Issue + lease còn hiệu lực mới giao được (protocol §3.2, §4). |
| `nguon_cap_viec` | Spec cha **r9** `ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md` (sha256 `465538364b1a3f9477782fba79869bbd1c9351140e3fa9df50451baae22f9c79`) §`write_set` dòng **A1**: *"… nghiệm thu wiring thật; đổi cờ `True` khi Q10 đạt; sổ vẫn rỗng"*. Quyết định **Q5** (A1 → A1a/A1b) ở `ops/specs/THU-HOI-LEASE-A1.md`. Phần A1a dồn sang A1b: `ops/specs/THU-HOI-LEASE-A1a-r2.md` (sha256 `9bc0fe282fbebc02791f47a30e4ff187b1182a2e5e357ee2e66c04d4f7dac7cd`, commit `7fc2868`, land merge `67802bf`) §4, §8. Soạn theo chỉ thị chủ kho phiên Claude Code 27-09-2026 ("Soạn spec đi"; hai vòng `soan-spec`, cả hai "Theo khuyến nghị"). |
| `review_class` | **`sensitive`**: `ops/lease_publish.py` là cổng đọc lease; `.github/workflows/**` (protocol §8). |
| `reviewer` | codex `gpt-6-astra`, effort `high`; trần `codex_review_calls` **4**; connector (`advisory_review`); cổng land **`human_audited`** (Q7). |
| `dong_bang` | **CHƯA.** Chỉ đóng băng khi đủ ba tiền đề ở §1 **và** đo lại mọi số ở §2 (L5). Tới lúc đó tệp này là DỮ LIỆU, không cấp việc. |

## 0. Quyết định của chủ kho (27-09-2026, hai vòng `soan-spec`, cả hai "Theo khuyến nghị")

| # | câu | quyết định | chiếu vào |
|---|---|---|---|
| Q1 | phạm vi | A1b = **(i)** bật cờ M-F · **(ii)** nghiệm thu wiring thật · **(iv)** ghim lại `BIA_MO_LICH_SU` trước khi bật · **(v)** mỏ neo `PROFILE_ADAPTER_DA_DUYET` do chủ kho duyệt. **(iii)** xoá holder theo bia mộ nhánh mặc định ⇒ **A1c** | §4, §5 |
| Q2 | facts Q10 | chủ kho đăng **một** comment facts trên #656, mỗi mục (a)–(i) một dòng bằng chứng; spec neo comment ID; executor **tự đo lại** (a)(c)(d)(h) trước khi bật; thiếu ⇒ DỪNG, cờ `False` | §1, M1 |
| Q3 | Q10(d) ngoài kho | chủ kho sửa ruleset `20856202` **trước khi cấp lease**: thêm required check `thu-hoi`, strict up-to-date, `allowed_merge_methods = [merge]`, giữ `bypass_actors = []` | §1, A6 |
| Q4 | thời điểm | bản nháp bây giờ; **đóng băng sau khi A1a land** | `dong_bang` |
| Q5 | Issue | Issue mới **#656**, con của #564 | `packet_issue` |
| Q6 | rollback | A1b land với **sổ rỗng**; rollback = PR revert cờ về `False`, **chỉ hợp lệ khi sổ còn rỗng** (sau slice C thì không) | M5, A5 |
| Q7 | review/trần | như A1a; ADR-0044 **≤ 300** dòng thêm; vượt ⇒ hỏi, không tự nới | §3 |
| Q8 | wiring thật | fixture có đột biến **và** một canary PR thật S≠H; hiện vật ở `ops/reviews/thu-hoi-lease-a1b/` (ngoài write set mã, tiền lệ A1a) | M2, A2 |
| Q9 | `BIA_MO_LICH_SU` | mốc giữ **A0** (`0721811`); chạy lại đúng script dẫn xuất của A1a trên ứng viên, clock = lúc bật; phải **trùng** hằng đã ghim; lệch ⇒ DỪNG | M3, A3 |
| Q10 | profile | ghim `runs-on: ubuntu-24.04`; digest đo bởi **bước workflow trên runner thật**, in vào receipt; executor ĐỀ XUẤT, chủ kho DUYỆT bằng cách trích digest trong audit; trôi ⇒ runbook (đo lại → PR dữ liệu → duyệt), không tự cập nhật; đo ≥ 2 run cách ≥ 24 h trước đóng băng, khác nhau ⇒ DỪNG | M4, A4 |
| Q11 | consumer | `LAND-DOC-RECEIPT-THU-HOI` (#499 C1) là **packet tiền đề riêng**, không vào A1b; A1b đóng băng khi nó đã land | §1 |
| Q12 | write set | 3 tệp (§3); đọc ruleset là **phép đo của executor** ghi vào biên nhận, **không** là unit test (test không gọi mạng) | §3, A6 |

## 1. Tiền đề — thiếu một ⇒ KHÔNG đóng băng, KHÔNG cấp lease

| # | tiền đề | trạng thái lúc soạn (đo 01:30–02:00Z 27-09) | cách đo lại |
|---|---|---|---|
| T1 | **A1a đã land** (write set trùng hoàn toàn với A1b, §3) | spec A1a r2 **đóng băng** (merge `67802bf`); mã A1a **chưa** có lease — #579 g20 giữ `ops/lease_publish.py`, `ops/lease_publish_test.py` tới **2026-09-29T00:00:00Z** | `git log --first-parent origin/master` có merge A1a; `ai-dang-giu` 3 đường ⇒ `NGƯỜI_GIỮ 0` (quét đủ ref) |
| T2 | **consumer `LAND-DOC-RECEIPT-THU-HOI` đã land** (Q10 c) | **CHƯA** — không có trong `.claude/`; chỉ `ops/specs/M9-FETCH-AUTH.md:61` nhắc là "packet riêng" | tệp consumer có trên `origin/master` và gọi được |
| T3 | **facts Q10 (a)–(i)** đã được chủ kho đăng trên #656 | **CHƯA** | comment ID ghim vào `nguon_cap_viec` bản đóng băng |
| T4 | **ruleset** đủ Q3 (trước cấp lease) | **CHƯA** — required checks chỉ `gate (ubuntu-latest)`, `gate-packet-loop (ubuntu-latest)`; **không** `thu-hoi`; `allowed_merge_methods = [merge, squash, rebase]`; `bypass_actors = []`; strict up-to-date **chưa đọc được** (`branches/master/protection` ⇒ 403) | `GET rules/branches/master`, `GET rulesets/20856202` |

## 2. Số đo (L5 — đo lại trước MỖI bước công bố)

- `origin/master` lúc soạn: **`67802bf`** (01:49Z 27-09).
- Hằng A0 trên master (`ops/lease_publish.py`, đo trên `fa8a062`): `SO_THU_HOI_KICH_HOAT = False` (:934) · `PROFILE_ADAPTER_DA_DUYET = frozenset()` (:942) · `BIA_MO_LICH_SU = ()` (:944) · `DESCRIPTOR_Q13_SHA256 = None` (:948). A1a r2 sẽ thêm `MOC_BIA_MO_LICH_SU` và ghim `DESCRIPTOR_Q13_SHA256` — số dòng CHÍNH XÁC phải đo lại sau khi A1a land.
- `ops/thu-hoi/` **không tồn tại** trên master (sổ rỗng).
- Digest profile = `sha256(JSON sort_keys)` của `hoso_adapter_do()` (`ops/lease_publish.py:1258`), trong đó có **`git_sha256` của binary git trên runner**. Workflow `thu-hoi` đang `runs-on: ubuntu-latest` (`ops-thu-hoi-admission.yml:47`). Annotation GitHub trên run CI 27-09: *"ubuntu-latest label will migrate to Ubuntu 26 beginning October 19, 2026"*.
- Workflow `thu-hoi`: **100** run gần nhất, **89** `success` (01:50Z 27-09) — ở A0 discovery `KHONG_CHAY`, nên **chưa từng có** phép đo digest trên runner thật.
- Cỡ tham chiếu: A0 = **2 387** dòng thêm / 3 tệp (numstat merge `0721811`). A1b ước **150–250** dòng thêm — ƯỚC, chưa đo.

## 3. `write_set`

```
ops/lease_publish.py
ops/lease_publish_test.py
.github/workflows/ops-thu-hoi-admission.yml
```

Đúng ba đường, không ký tự đại diện, **trùng hoàn toàn** write set A1a ⇒ tuần tự sau A1a. Hiện vật review
và biên nhận đo (canary, profile, ruleset) ở `ops/reviews/thu-hoi-lease-a1b/**` — nhánh riêng, tiền lệ A1a/#551.

## 4. `ngoai_pham_vi`

| thứ | lý do |
|---|---|
| **(iii)** xoá holder theo bia mộ nhánh mặc định bằng OID máy chủ (nợ `AG-T0-01B` dạng 2, #564) | Q1 ⇒ **A1c**. Mã nhạy cảm, cỡ lớn; làm sau khi sổ chạy. |
| Bản ghi thu hồi đầu tiên (`ops/thu-hoi/wp461-…yaml`) | slice **C** (r9), sau Q8/Q10/Q11 của r9. A1b land với sổ **rỗng**. |
| Consumer `LAND-DOC-RECEIPT-THU-HOI` | Q11: packet tiền đề riêng (#499 C1), đường `.claude/…` ngoài write set. |
| Sửa ruleset / branch protection | Q3: cấu hình ngoài kho, việc của chủ kho. A1b chỉ **đo**. |
| Cơ chế tự cập nhật digest profile | Q10: executor không tự duyệt (ADR-0047 lớp 2). |
| Bỏ `git_sha256` khỏi profile | Q10: chỉ xét nếu hai lần đo cách 24 h khác nhau — quyết định chủ kho, ngoài A1b. |

## 5. `muc_tieu` — mỗi dòng chiếu vào MỘT đường dẫn (L2)

| # | mục tiêu | đường |
|---|---|---|
| **M1** | `SO_THU_HOI_KICH_HOAT = True` — **chỉ** sau khi T1–T4 đạt và executor đo lại (a)(c)(d)(h) của Q10 | `ops/lease_publish.py` |
| **M2** | Ca **wiring thật** dạng fixture: join check-run → suite → run → attempt → artifact `thu-hoi-receipt-<H>-<attempt>`; mỗi mắt xích thiếu/sai SHA/sai attempt/artifact vắng ⇒ consumer từ chối; có đột biến gỡ từng mắt xích | `ops/lease_publish_test.py` |
| **M3** | Ca khoá `BIA_MO_LICH_SU`: hằng bằng đúng giá trị dẫn xuất (Q9) — đổi hằng mà không đổi bằng chứng ⇒ đỏ | `ops/lease_publish_test.py` |
| **M4** | `PROFILE_ADAPTER_DA_DUYET = frozenset({<digest chủ kho duyệt>})` — giá trị lấy từ receipt runner thật, KHÔNG từ máy executor | `ops/lease_publish.py` |
| **M5** | Ca **tương đương hành vi** (Q6): cờ `True` + sổ rỗng ⇒ `check` và `ai-dang-giu` cho **cùng rc và cùng tập `NGƯỜI_GIỮ`** như cờ `False`, trên một bộ lease fixture phủ mọi nhãn hiện có | `ops/lease_publish_test.py` |
| **M6** | Ghim `runs-on: ubuntu-24.04` + bước **đo profile** in `hoso_adapter_do()` (JSON) và digest vào receipt, không bí mật | `.github/workflows/ops-thu-hoi-admission.yml` |

## 6. `nghiem_thu` — mỗi tiêu chí nêu phép đo làm nó ĐỎ (L3)

| # | tiêu chí | ĐỎ khi |
|---|---|---|
| A1 | M1: cờ `True` trên ứng viên; biên nhận đo lại (a)(c)(d)(h) có trong thân PR | biên nhận thiếu một mục, hoặc một mục đo ra khác facts #656 |
| A2 | M2: fixture join qua; **canary PR thật** S≠H cho join đủ 5 mắt xích qua API, hiện vật ở `ops/reviews/thu-hoi-lease-a1b/` | đột biến gỡ bất kỳ mắt xích nào mà ca vẫn xanh; canary thiếu mắt xích |
| A3 | M3: script dẫn xuất A1a chạy lại trên ứng viên, clock = lúc bật, cho **đúng** hằng đã ghim | lệch digest/số cặp ⇒ DỪNG (không ghim đè) |
| A4 | M4: digest trong mỏ neo = digest in bởi bước M6 trên **≥ 2** run runner thật cách **≥ 24 h**; chủ kho trích nguyên digest trong audit | hai lần đo khác nhau ⇒ DỪNG; digest không khớp receipt; mỏ neo rỗng mà đường production đi tiếp (đột biến) |
| A5 | M5: cờ `True`/sổ rỗng ≡ cờ `False` trên rc + `NGƯỜI_GIỮ` | đột biến đổi một nhánh phân loại khi cờ `True` mà ca vẫn xanh |
| A6 | T4 đo bởi executor (API ruleset) ngay trước cấp lease **và** trước merge: `thu-hoi` required, strict, merge-only, không bypass | thiếu một điều kiện ⇒ DỪNG (không phải unit test — Q12) |
| A7 | `actionlint` (có `shellcheck`) rc=0 trên `ops-thu-hoi-admission.yml`; ADR-0044 ≤ 300 dòng thêm | rc≠0; vượt trần mà chưa có ngoại lệ chủ kho |

## 7. `hinh_dang_ke_thua` (L4)

Chép từ A1a r2 §7 (đóng băng `9bc0fe28…`), cộng một hình dạng từ #651:

| hình dạng | số lần | nguồn |
|---|---|---|
| **"nguồn được tin mà chưa xác minh"** | **7** | r9 lượt 1–6 · A1a r2 lượt 1 F1. Checkpoint §12 đã chạy (A1a vòng 3). **Lần 8** phải nhắm vào chỗ A1b **trao thẩm quyền** — ở đây là M4 (digest profile) và M1 (facts Q10): cả hai phải lấy từ nguồn đo, không từ lời khai. |
| "thu hồi là dữ liệu ghi vào bản sao" | 3 | r9 §1 (2) · #564 dạng 2. **Thêm chứng cứ 27-09:** thu hồi lease #651 g1 bằng rút hạn (PR #654/#655) không tới được hai nhánh của phiên khác — đúng hình dạng này. |
| "lời khai hội tụ rộng hơn phép đo" | 3 | r9 g2, lượt 1 |
| "hai cổng bất đồng" | 1 | r9, #473 |
| "cổng CÓ MẶT khác cổng ĐO ĐƯỢC" | 1 | #499 C2a |
| "gate xanh lane PR, master đo lần đầu" | 1 | #499 C3 |
| "khử trùng giữ một đại diện, rồi hỏi đại diện câu hỏi về cả nhóm" | 1 | A1a M14 §5.1 |
| "quyết định đổi bộ lọc bị đọc thành quyền đổi nguồn" | 1 | A1a r2 lượt 1 F2 |
| **"ô tự do trong workflow"** (mới với chuỗi này) | **4** | #651 (Codex CLI lượt 2–5): cron không ghim · `concurrency` · `name`/job id · YAML thô qua `safe_load`. **Áp trực tiếp M6**: mọi giá trị mới của workflow phải ghim hoặc dẫn xuất, và qua `actionlint` thật. |

## 8. `chua_do_duoc`

1. **Tần suất trôi `git_sha256` trong Ubuntu 24.04** — chưa có phép đo nào (A0 `KHONG_CHAY`). A4 đòi hai lần đo cách 24 h; nếu trôi hằng tuần thì runbook Q10 sẽ chạy thường xuyên và mọi admission 12 giữa hai lần duyệt — **fail-closed**, không mở quyền, nhưng chặn land. Quyết định bỏ `git_sha256` thuộc chủ kho.
2. **Strict up-to-date của ruleset** — `branches/master/protection` trả **403** cho token phiên; `rules/branches/master` chưa cho thấy trường ấy. A6 phải tìm được nguồn đọc được, không thì A6 là `KHÔNG ĐO ĐƯỢC` ⇒ DỪNG.
3. **Số dòng thêm** — ƯỚC 150–250, chưa đo; phụ thuộc cỡ fixture M2/M5 sau khi A1a land.
4. **Vị trí dòng của các hằng sau A1a** — mọi số dòng ở §2 là của A0 (`fa8a062`); phải đo lại trên master sau A1a.
5. **Hành vi của `ai-dang-giu` khi cờ `True` và sổ rỗng trên TOÀN KHO** — M5 đo trên fixture; trên kho thật chỉ đo được lúc thi công (biên nhận so trước/sau).
