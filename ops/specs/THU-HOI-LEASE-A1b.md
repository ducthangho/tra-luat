# ĐẶC TẢ — `THU-HOI-LEASE-A1b` — **revision 1, bản nháp 4 (CHƯA đóng băng)**

| trường | giá trị |
|---|---|
| `packet_id` | `THU-HOI-LEASE-A1b` — **bật cờ** của slice A1 (mã: `THU-HOI-LEASE-A1a`; đo profile: `THU-HOI-LEASE-A1-DO-PROFILE`; nối verdict: `THU-HOI-LEASE-A1-WIRING`) |
| `packet_issue` | **#656** (con của #564). Issue **không** cấp việc; chỉ Issue + lease còn hiệu lực mới giao được (protocol §3.2, §4). |
| `nguon_cap_viec` | Spec cha **r9** `ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md` (sha256 `465538364b1a3f9477782fba79869bbd1c9351140e3fa9df50451baae22f9c79`) §`write_set` dòng **A1**: *"… nghiệm thu wiring thật; đổi cờ `True` khi Q10 đạt; sổ vẫn rỗng"*. Q5 (A1 → A1a/A1b) ở `ops/specs/THU-HOI-LEASE-A1.md`. A1a r2 đã đóng băng: `ops/specs/THU-HOI-LEASE-A1a-r2.md` sha256 `9bc0fe282fbebc02791f47a30e4ff187b1182a2e5e357ee2e66c04d4f7dac7cd` (commit `7fc2868`, land merge `67802bf`). Chỉ thị chủ kho phiên Claude Code 27-09-2026: "Soạn spec đi"; ba vòng quyết định, cả ba "Theo khuyến nghị" (§0). |
| `review_class` | **`sensitive`**: `ops/lease_publish.py` là cổng đọc lease (protocol §8). |
| `reviewer` | codex `gpt-6-astra`, effort `high`; trần `codex_review_calls` **10** cho đặc tả này (tiền lệ A1a r2); connector (`advisory_review`); cổng land **`human_audited`** (Q7). |
| `dong_bang` | **CHƯA.** Chỉ đóng băng khi đủ T1–T6 (§1) **và** đo lại mọi số ở §2 (L5). Tới lúc đó tệp này là DỮ LIỆU, không cấp việc. |
| `lich_su_ban_nhap` | Bản nháp 1: commit `65a612a`, sha256 `cb9ec4736551e9713d26e8f6b2384f203a37dea3f1d5eb6d8ab923de9337a39a`, codex lượt 1 `changes_requested` **2 P1 + 3 P2** (F1–F5, `ops/reviews/thu-hoi-lease-a1b/luot1-VERDICT.md`). Bản nháp 2: commit `673256e`, sha256 `0a1f7213c8f78456c4fdac24c0a0bcc4713e17da15a0204e286f9c2147dbb510`, codex lượt 2 `changes_requested` **1 P1 + 1 P2** (F6–F7, `luot2-VERDICT.md`). Lượt 2 xác nhận **F3 đã vá thật**; F1, F4, F5 **chuyển** sang packet tiền đề (§8.3: chuyển sang successor KHÔNG tính là đã vá — chỉ đóng khi successor land và đo được); F2 vá một phần ⇒ F6. Bản nháp 3: commit `1503ca8`, sha256 `b7baed1cc9076bb760963013b4accf7215c4e0a7955f3ce90ef483c85ad958b9`, codex lượt 3 `changes_requested` **0 P1 + 1 P2** (F8, `luot3-VERDICT.md`); lượt 3 xác nhận **F6, F7 đã vá thật trong đặc tả** (phản chứng lượt 2 nay bị từ chối). Bản nháp 4 vá F8 (ma trận oracle riêng từng đường production) và cập nhật T4 (strict nay ĐO ĐƯỢC): commit `52831cc`, sha256 `d135c6215680355de932ca5ec8db15bc856f6994a0ec4bea57d14838bf3519ec`, codex lượt 4 **`approve` — 0 P1 / 0 P2 / 0 P3** (`luot4-VERDICT.md`); F8 đã vá thật trong đặc tả. Approve là cho **bản nháp đặc tả**, không xác nhận tiền đề T1–T6. Dùng **4/10** lượt. Commit ghi dòng này chỉ thêm lịch sử — nội dung kỹ thuật = bản nháp 4. |

## 0. Quyết định của chủ kho (27-09-2026)

**Vòng 1–2** (`soan-spec`, "Theo khuyến nghị"):

| # | câu | quyết định |
|---|---|---|
| Q1 | phạm vi | A1b = **(i)** bật cờ · **(ii)** nghiệm thu wiring thật · **(iv)** ghim lại `BIA_MO_LICH_SU` trước khi bật · **(v)** mỏ neo `PROFILE_ADAPTER_DA_DUYET` do chủ kho duyệt. **(iii)** xoá holder theo bia mộ nhánh mặc định ⇒ **A1c** |
| Q2 | facts Q10 | chủ kho đăng **một** comment facts trên #656, mỗi mục (a)–(i) một dòng bằng chứng; spec neo comment ID; executor **tự đo lại** (a)(c)(d)(h) trước khi bật; thiếu ⇒ DỪNG |
| Q3 | Q10(d) ngoài kho | chủ kho sửa ruleset `20856202` trước cấp lease: required check `thu-hoi`, strict up-to-date, `allowed_merge_methods = [merge]`, `bypass_actors = []` |
| Q4 | thời điểm | bản nháp bây giờ; đóng băng khi đủ tiền đề §1 |
| Q5 | Issue | #656, con của #564 |
| Q6 | rollback | A1b land với **sổ rỗng**; rollback = PR revert cờ về `False`, **chỉ hợp lệ khi sổ còn rỗng** |
| Q7 | review/trần | codex + connector + `human_audited`; ADR-0044 **≤ 300** dòng thêm; vượt ⇒ hỏi |
| Q8 | wiring thật | fixture có đột biến **và** canary PR thật; hiện vật ở `ops/reviews/thu-hoi-lease-a1b/` |
| Q9 | `BIA_MO_LICH_SU` | mốc giữ **A0** (`0721811`); chạy lại script dẫn xuất của A1a trên ứng viên, clock = lúc bật; phải **trùng** hằng; lệch ⇒ DỪNG |
| Q10 | profile | digest đo trên **runner thật bởi mã CANONICAL**; executor ĐỀ XUẤT, chủ kho DUYỆT bằng cách trích digest trong audit; trôi ⇒ runbook (đo lại → PR dữ liệu → duyệt); đo ≥ 2 run cách ≥ 24 h, khác nhau ⇒ DỪNG |
| Q11 | consumer | `LAND-DOC-RECEIPT-THU-HOI` (#499 C1) là packet tiền đề riêng |
| Q12 | ruleset | đọc ruleset là **phép đo của executor** ghi vào biên nhận, không là unit test |

**Vòng 3** (sau codex lượt 1, "Theo khuyến nghị"):

| # | finding | quyết định |
|---|---|---|
| Q13 | F1 (P1): bước đo profile phải có trên canonical **trước** khi đo được digest | **packet tiền đề riêng `THU-HOI-LEASE-A1-DO-PROFILE`**: thêm bước đo vào workflow `thu-hoi` (chạy MÃ CANONICAL tại `workflow_sha`), ghim runner, cờ vẫn `False`. Đo ≥ 2 run canonical sau khi land. M6 cũ **rời** A1b |
| Q14 | F2 (P1): bật cờ chưa nối luật mới vào verdict production — `lenh_check`/`lenh_ai_dang_giu`/`lenh_kiem_thu_hoi_github` không gọi discovery (codex đo AST) | **packet tiền đề riêng `THU-HOI-LEASE-A1-WIRING`**: nối sổ + discovery vào verdict production **sau cờ** (cờ `False` ⇒ hành vi y hệt), land với cờ `False`. A1b chỉ **bật** + nghiệm thu |
| Q15 | F2 (P1): M5 "mọi rc bằng nhau" trái r9 Q6 | **phân loại delta theo Q6** trên cùng map ref + cùng clock — đủ HAI trục của Q6 (r9 `:381–388`): **eligibility** (rc) chỉ cho `0→8` bảo thủ ở cặp thay thế sinh sau mốc; **holder** so TẬP theo ID/path kèm nguyên nhân, không suy từ rc (codex lượt 2 F7). Delta khác ⇒ ĐỎ |
| Q16 | F4 (P2): nợ "C == S" trong hợp đồng consumer | **packet consumer đóng**: chốt hợp đồng C/S/H/T và có ca C≠S. A1b neo exact SHA + entry point consumer, test import consumer thật |

## 1. Tiền đề — thiếu một ⇒ KHÔNG đóng băng, KHÔNG cấp lease

| # | tiền đề | trạng thái lúc soạn (đo 01:30–02:40Z 27-09) | cách đo lại |
|---|---|---|---|
| T1 | **mã A1a đã land** | spec A1a r2 đóng băng (merge `67802bf`); mã **chưa**. #579 g20 giữ `ops/lease_publish.py`, `ops/lease_publish_test.py` tới **2026-09-29T00:00:00Z** (đo bởi agent khảo sát ~23:30Z 26-09) | merge A1a trên `--first-parent origin/master`; `ai-dang-giu` 2 đường ⇒ `NGƯỜI_GIỮ 0` (quét đủ ref) |
| T2 | **consumer `LAND-DOC-RECEIPT-THU-HOI` đã land**, có: exact commit SHA · entry point production gọi được · hợp đồng C/S/H/T đã chốt · ca C≠S (Q16) | **CHƯA** — `git grep -E 'check_suite\|check_run_url\|thu-hoi-receipt' 67802bf -- .claude` ⇒ rc=1 (codex lượt 1) | SHA + entry point ghim vào bản đóng băng |
| T3 | **facts Q10 (a)–(i)** trên #656 | **CHƯA** | comment ID ghim vào bản đóng băng |
| T4 | **ruleset** đủ Q3 | **CHƯA** — `GET rulesets/20856202` (đo 02:45Z 27-09, codex lượt 3 và đo lại trong phiên): required checks `gate (ubuntu-latest)`, `gate-packet-loop (ubuntu-latest)`, **không** `thu-hoi`; **`strict_required_status_checks_policy = false`**; `allowed_merge_methods = [merge, squash, rebase]`; `bypass_actors = []` | `GET rulesets/20856202` (đọc được; `branches/master/protection` vẫn 403 nhưng không cần) |
| T5 | **`THU-HOI-LEASE-A1-DO-PROFILE` đã land** và có **≥ 2** receipt của run canonical cách **≥ 24 h** cho **cùng** digest schema v2 (Q13) | **CHƯA** — workflow tại `67802bf` có 2 bước `run`, không gọi `hoso_adapter_do` (codex lượt 1) | receipt: run ID, attempt, `workflow_sha`, digest, `image_os`/`image_version` |
| T6 | **`THU-HOI-LEASE-A1-WIRING` đã land** với cờ `False` (Q14), có: exact commit SHA · danh sách **đường production** cần nghiệm thu (`check`, `ai-dang-giu`, admission `kiem-thu-hoi-github`) **kèm HỢP ĐỒNG verdict riêng từng đường** (ma trận A6) · **seam tiêm** map ref, clock, nguồn discovery nội bộ · kết quả discovery **quyết định** verdict (không chỉ được gọi). Validator ứng viên M4 của admission **độc lập với cờ** (r9 Q3) — WIRING không được đổi semantics ấy | **CHƯA** — chưa có spec | SHA + entry point + chữ ký seam ghim vào bản đóng băng; ca "gọi discovery rồi bỏ kết quả" của chính packet WIRING phải ĐỎ |

## 2. Số đo (L5 — đo lại trước MỖI bước công bố)

- `origin/master` lúc soạn: **`67802bf`** (01:49Z 27-09).
- Hằng A0 (`ops/lease_publish.py` @ `67802bf`): `SO_THU_HOI_KICH_HOAT = False` (:934) · `PROFILE_ADAPTER_DA_DUYET = frozenset()` (:942) · `BIA_MO_LICH_SU = ()` (:944) · `DESCRIPTOR_Q13_SHA256 = None` (:948). Số dòng **đổi** sau A1a/A1-WIRING — đo lại.
- `ops/thu-hoi/` **không tồn tại** @ `67802bf` (sổ rỗng).
- **Schema profile là v2 sau A1a** (A1a r2 M1/M2, `ops/specs/THU-HOI-LEASE-A1a-r2.md:145–146`, A2 `:222`): digest băm **tầng BẮT BUỘC** (`git_path`, `git_version`, `credential_helper`, `tls_thu_vien`, `http_sslCAInfo`/`http_sslCAPath`/`proxy`/`endpoint`, `image_os`/`image_version`); `git_sha256` ở tầng **AUDIT-ONLY**, ngoài digest. Trôi digest vì thế theo **`image_version`/`git_version`** của runner, không theo băm nhị phân. Tại `67802bf` mã vẫn là schema A0 (v1).
- Workflow `thu-hoi`: `runs-on: ubuntu-latest` (`ops-thu-hoi-admission.yml:47`); checkout `ref: ${{ github.workflow_sha }}`; `bo_kiem_da_chay_commit = wf_sha` (:160). Annotation GitHub 27-09: `ubuntu-latest` → Ubuntu 26 từ **2026-10-19**. **100** run gần nhất, **89** `success` (01:50Z 27-09; chưa đo độc lập lần hai).
- Q6 (chạy lại bởi codex lượt 1 @ `67802bf`): **89** lease hợp lệ, **11** cặp hai chiều, digest `8f372ccd…`, **0** cặp giữ lại.
- Cỡ tham chiếu: A0 = **2 387** dòng thêm / 3 tệp (`141 + 919 + 1327`, numstat `0721811^1..0721811`).

## 3. `write_set`

```
ops/lease_publish.py
ops/lease_publish_test.py
```

Hai đường (bản nháp 1 có ba — workflow rời sang `THU-HOI-LEASE-A1-DO-PROFILE`, Q13). Trùng write set A1a
và A1-WIRING ⇒ tuần tự sau cả hai. Test **được đọc/import** consumer ngoài write set (Q16) — không vi phạm L2.
Hiện vật review/biên nhận đo ở `ops/reviews/thu-hoi-lease-a1b/**`, nhánh riêng (tiền lệ A1a/#551).

## 4. `ngoai_pham_vi`

| thứ | lý do |
|---|---|
| **(iii)** xoá holder theo bia mộ nhánh mặc định (nợ `AG-T0-01B` dạng 2) | Q1 ⇒ **A1c** |
| Bước đo profile, ghim runner, sửa `ops-thu-hoi-admission.yml` và ca "đúng hai bước run" (`ops/lease_publish_test.py:5154`) | Q13 ⇒ `THU-HOI-LEASE-A1-DO-PROFILE`; phải giữ chốt nhận diện từng bước, không chỉ nới `len(than)` (codex lượt 1 F5) |
| Nối sổ + discovery vào verdict production | Q14 ⇒ `THU-HOI-LEASE-A1-WIRING` |
| Hợp đồng C/S/H/T và ca C≠S của consumer | Q16 ⇒ packet consumer |
| Bản ghi thu hồi đầu tiên | slice **C** (r9); A1b land với sổ rỗng |
| Sửa ruleset | Q3: việc chủ kho; A1b chỉ đo |
| Tự cập nhật digest | Q10: executor không tự duyệt (ADR-0047 lớp 2) |

## 5. `muc_tieu` — mỗi dòng chiếu vào MỘT đường dẫn (L2)

| # | mục tiêu | đường |
|---|---|---|
| **M1** | `SO_THU_HOI_KICH_HOAT = True` — chỉ sau T1–T6 và executor đo lại Q10 (a)(c)(d)(h) | `ops/lease_publish.py` |
| **M2** | Ca **wiring thật** qua **consumer thật** (import, không chép validator): join check-run → suite → run → attempt → artifact; từng mắt xích sai ⇒ consumer từ chối; có ca C≠S | `ops/lease_publish_test.py` |
| **M3** | Ca khoá `BIA_MO_LICH_SU` = giá trị dẫn xuất Q9 | `ops/lease_publish_test.py` |
| **M4** | `PROFILE_ADAPTER_DA_DUYET = frozenset({<digest v2 chủ kho duyệt>})` — lấy từ receipt T5, không từ máy executor | `ops/lease_publish.py` |
| **M5** | Ca **phân loại delta** (Q15), cùng map ref + clock, cờ `False` → `True`, qua **verdict thật** của WIRING (không chép validator): (a) **fixture dương bắt buộc** — cặp thay thế sau mốc, sổ rỗng — phải cho **đúng** `0→8`; tập delta rỗng ⇒ ĐỎ; (b) eligibility: ngoài (a), mọi delta mở quyền (`8→0`, `11→0`, `12→0`) ⇒ ĐỎ; (c) holder: so **tập holder theo ID/path** kèm nguyên nhân trước/sau — mất một holder khi còn holder khác (rc vẫn `11`) ⇒ ĐỎ trừ khi nguyên nhân được Q6 cho phép | `ops/lease_publish_test.py` |
| **M6** | Ca **production qua discovery**: cờ `True` + mỏ neo đúng ⇒ discovery chạy; mỏ neo sai/rỗng ⇒ `12` | `ops/lease_publish_test.py` |

## 6. `nghiem_thu` — mỗi tiêu chí nêu phép đo làm nó ĐỎ (L3)

| # | tiêu chí | ĐỎ khi |
|---|---|---|
| A1 | M1: cờ `True`; biên nhận đo lại (a)(c)(d)(h) trong thân PR | thiếu một mục, hoặc lệch facts #656 |
| A2 | M2: consumer thật chấp nhận fixture đủ; từ chối từng mắt xích sai; canary PR thật S≠H **và** C≠S cho join đủ qua API | đột biến gỡ một mắt xích mà ca xanh; canary thiếu mắt xích |
| A3 | M3: script dẫn xuất A1a chạy lại trên ứng viên, clock = lúc bật, ra **đúng** hằng | lệch digest/số cặp ⇒ DỪNG |
| A4 | M4: digest mỏ neo = digest trong ≥ 2 receipt T5; chủ kho trích nguyên digest trong audit | receipt khác nhau ⇒ DỪNG; mỏ neo ≠ receipt |
| A5 | M5 (a)(b)(c); biên nhận đếm delta **theo loại và theo trục** (eligibility / holder) trên kho thật | đột biến "gọi discovery rồi bỏ kết quả" (fixture dương ra delta rỗng) mà ca xanh; đột biến mở quyền một nhánh mà ca xanh; đột biến bỏ một holder trong tập ≥ 2 holder mà ca xanh |
| A6 | M6 — **ma trận oracle riêng từng đường** (codex lượt 3 F8), mỗi đường mỏ neo sai/rỗng ⇒ `12`: **`check`** (eligibility) — fixture dương M5(a) ra `0→8`; **`ai-dang-giu`** (holder) — **tập holder theo ID/path** trước/sau theo M5(c), rc đi kèm tập, không suy tập từ rc; **admission `kiem-thu-hoi-github`** (namespace sổ) — sổ rỗng/hợp lệ ⇒ **giữ** kết quả nền (validator M4 độc lập cờ), và dữ liệu discovery **không khớp** (OID/nhánh mặc định lệch) ⇒ từ chối. Không đường nào được đổi semantics để "đạt" oracle của đường khác | trên **mỗi** đường: đột biến bỏ phép so mỏ neo mà ca xanh; đột biến gọi discovery rồi bỏ kết quả mà ca xanh; đột biến làm admission trả `8` cho fixture eligibility (mở rộng semantics) mà ca xanh |
| A7 | T4 đo bởi executor (API ruleset) trước cấp lease **và** trước merge | thiếu `thu-hoi`/strict/merge-only/không bypass ⇒ DỪNG |
| A8 | ADR-0044 ≤ 300 dòng thêm | vượt mà chưa có ngoại lệ chủ kho |

## 7. `hinh_dang_ke_thua` (L4)

Chép từ A1a r2 §7 (`9bc0fe28…`), cộng #651 và lượt 1 của đặc tả này:

| hình dạng | số lần | nguồn |
|---|---|---|
| **"nguồn được tin mà chưa xác minh"** | **7** | r9 lượt 1–6 · A1a r2 lượt 1 F1. **Lần 8** phải nhắm chỗ A1b **trao thẩm quyền**: M4 (digest) và M1 (facts Q10). |
| "thu hồi là dữ liệu ghi vào bản sao" | 3 | r9 §1 (2) · #564 dạng 2. Chứng cứ thêm 27-09: rút hạn lease #651 g1 (PR #654/#655) không tới được hai nhánh phiên khác. |
| "lời khai hội tụ rộng hơn phép đo" | 3 | r9 g2, lượt 1 |
| "hai cổng bất đồng" | 1 | r9, #473 |
| "cổng CÓ MẶT khác cổng ĐO ĐƯỢC" | **2** | #499 C2a · **A1b lượt 1 F2**: cờ có mặt nhưng không đường production nào đọc nó để gọi discovery |
| "gate xanh lane PR, master đo lần đầu" | 1 | #499 C3 |
| "khử trùng giữ một đại diện…" | 1 | A1a M14 §5.1 |
| "quyết định đổi bộ lọc bị đọc thành quyền đổi nguồn" | 1 | A1a r2 lượt 1 F2 |
| "ô tự do trong workflow" | 4 | #651 lượt 2–5 — áp cho `THU-HOI-LEASE-A1-DO-PROFILE` |
| **"đặc tả hứa thứ tiền đề chưa có producer/đường nối"** (mới) | **2** | A1b lượt 1 F1 (bước đo profile), F2 (wiring production) |
| **"một oracle cho nhiều hợp đồng"** (mới) | **1** | A1b lượt 3 F8: A6 áp oracle eligibility cho cả holder và admission |
| **"tiêu chí thoả được bởi tập rỗng"** (mới) | **2** | A1b lượt 2 F6 (delta rỗng qua A5), F7 (delta rc rỗng che mất holder) — cùng gốc: tiêu chí chỉ cấm cái XẤU mà không đòi cái TỐT phải xảy ra |

## 8. `chua_do_duoc`

1. **Tần suất trôi digest v2** — theo `image_version`/`git_version`; chưa đo (A0 `KHONG_CHAY`). T5 đòi 2 lần cách 24 h. Trôi ⇒ admission `12` tới khi chủ kho duyệt digest mới — fail-closed, chặn land.
2. ~~Strict up-to-date của ruleset~~ — **đã đo được** (bản nháp 4): `GET rulesets/20856202` trả `strict_required_status_checks_policy = false`. A7 đọc nguồn này.
3. **Số dòng thêm** — chưa ước lại sau khi rút M6 cũ và thêm M5/M6 mới; phụ thuộc giao diện A1-WIRING.
4. **Vị trí dòng hằng** sau A1a/A1-WIRING — §2 là số @ `67802bf`.
5. **Delta trên toàn kho thật** — M5 đo trên fixture; kho thật chỉ đo lúc thi công (A5 biên nhận).
6. **Các số chưa đo độc lập lần hai** (codex lượt 1): 100/89 run `thu-hoi`, annotation Ubuntu 26, hạn #579 g20, ruleset.
