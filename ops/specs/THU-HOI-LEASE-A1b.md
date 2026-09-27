# ĐẶC TẢ — `THU-HOI-LEASE-A1b` — **revision 1, bản nháp 8 (CHƯA đóng băng)**

| trường | giá trị |
|---|---|
| `packet_id` | `THU-HOI-LEASE-A1b` — **bật cờ** của slice A1 (mã: `THU-HOI-LEASE-A1a`; đo profile: `THU-HOI-LEASE-A1-DO-PROFILE`; nối verdict: `THU-HOI-LEASE-A1-WIRING`) |
| `packet_issue` | **#656** (con của #564). Issue **không** cấp việc; chỉ Issue + lease còn hiệu lực mới giao được (protocol §3.2, §4). |
| `nguon_cap_viec` | Spec cha **r9** `ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md` (sha256 `465538364b1a3f9477782fba79869bbd1c9351140e3fa9df50451baae22f9c79`) §`write_set` dòng **A1**: *"… nghiệm thu wiring thật; đổi cờ `True` khi Q10 đạt; sổ vẫn rỗng"*. Q5 (A1 → A1a/A1b) ở `ops/specs/THU-HOI-LEASE-A1.md`. A1a **r3** đã đóng băng và **thay** r2: `ops/specs/THU-HOI-LEASE-A1a-r3.md` sha256 `ac7e0129b281b517c69e9a2512a05b47d55ad99f0ac964462c061ea511f70bc1` (land merge `f5bef3a`; `thay_the_cho` r2 `9bc0fe28…`, merge `67802bf`). Nhắc tới "A1a r2" ở dưới là hồ sơ đo r2 mà r3 giữ nguyên, trừ khi ghi khác. Chỉ thị chủ kho phiên Claude Code 27-09-2026: "Soạn spec đi"; ba vòng quyết định, cả ba "Theo khuyến nghị" (§0). |
| `review_class` | **`sensitive`**: `ops/lease_publish.py` là cổng đọc lease (protocol §8). |
| `reviewer` | codex `gpt-6-astra`, effort `high`; trần `codex_review_calls` **2** theo protocol §8 (`docs/PROTOCOL_DA_PHIEN.md:669`) — một đặc tả KHÔNG nới được trần ấy. Bản nháp 1–4 tự ghi trần 10 (chép tiền lệ A1a r2) và đã dùng **4** lượt ⇒ **vượt trần từ lượt 3**; connector bắt (P1 `r4113875422`). **Review Rescue Checkpoint** (§12 `:1079–1089`) ghi ở #657 `issuecomment-5852188204`: chủ kho quyết **không gọi thêm lượt Codex nào** cho #657; bản nháp 5 vá lời khai theo connector; assurance cho lần land bản nháp làm DỮ LIỆU là **`human_audited`** trên đúng head sau vá. Connector (`advisory_review`); cổng land thi công **`human_audited`** (Q7). |
| `dong_bang` | **CHƯA.** Chỉ đóng băng khi đủ T1–T6 (§1) **và** đo lại mọi số ở §2 (L5). Tới lúc đó tệp này là DỮ LIỆU, không cấp việc. |
| `lich_su_ban_nhap` | Bản nháp 1: commit `65a612a`, sha256 `cb9ec4736551e9713d26e8f6b2384f203a37dea3f1d5eb6d8ab923de9337a39a`, codex lượt 1 `changes_requested` **2 P1 + 3 P2** (F1–F5, `ops/reviews/thu-hoi-lease-a1b/luot1-VERDICT.md`). Bản nháp 2: commit `673256e`, sha256 `0a1f7213c8f78456c4fdac24c0a0bcc4713e17da15a0204e286f9c2147dbb510`, codex lượt 2 `changes_requested` **1 P1 + 1 P2** (F6–F7, `luot2-VERDICT.md`). Lượt 2 xác nhận **F3 đã vá thật**; F1, F4, F5 **chuyển** sang packet tiền đề (§8.3: chuyển sang successor KHÔNG tính là đã vá — chỉ đóng khi successor land và đo được); F2 vá một phần ⇒ F6. Bản nháp 3: commit `1503ca8`, sha256 `b7baed1cc9076bb760963013b4accf7215c4e0a7955f3ce90ef483c85ad958b9`, codex lượt 3 `changes_requested` **0 P1 + 1 P2** (F8, `luot3-VERDICT.md`); lượt 3 xác nhận **F6, F7 đã vá thật trong đặc tả** (phản chứng lượt 2 nay bị từ chối). Bản nháp 4 vá F8 (ma trận oracle riêng từng đường production) và cập nhật T4 (strict nay ĐO ĐƯỢC): commit `52831cc`, sha256 `d135c6215680355de932ca5ec8db15bc856f6994a0ec4bea57d14838bf3519ec`, codex lượt 4 **`approve` — 0 P1 / 0 P2 / 0 P3** (`luot4-VERDICT.md`); F8 đã vá thật trong đặc tả. Approve là cho **bản nháp đặc tả**, không xác nhận tiền đề T1–T6. Đã dùng **4** lượt, vượt trần 2 (xem `reviewer`). Commit `59916b0` chỉ thêm dòng lịch sử (sha256 `34f9837f…`) — nên approve lượt 4 **neo `52831cc`, KHÔNG neo head nào sau đó**, và KHÔNG là verdict exact-SHA cho bất kỳ head nào của #657 (connector P2 `r4113875424`). Bản nháp 5: commit `699057c`, sha256 `468dd6761ba5edf1bbe2f54224b15e02ce9e0006bb23a9041cc4acd90e8119f2`, vá **6** finding connector review `5328618160` chỉ bằng sửa lời khai/điều kiện: trần 2 + checkpoint (`r4113875422`) · approve cũ (`r4113875424`) · facts Q10 neo byte (`r4113875431`, T3/Q2) · vai đo ruleset (`r4113875427`, T4/A7) · bootstrap consumer bị bỏ lỡ (`r4113875442`, T2) · hiện vật nằm trong write set (`r4113875429`, §3/Q8/A2). Không có verdict Codex nào cho bản nháp 5; thay bằng `human_audited`. Bản nháp 6 (commit `4324f2a`, sha256 `1cffaa97…`) vá review **Claude độc lập** lượt 1 trên `699057c` (`ops/reviews/thu-hoi-lease-a1b/claude-luot1-VERDICT.md`) (`same_provider_approved`, bổ sung — KHÔNG thay `human_audited` cho phạm vi nhạy cảm; KHÔNG tính vào trần Codex): `changes_requested` **0 P1 / 6 P2 / 2 P3** — neo A1a r3 + bộ đo thi công `do_q6_hk.py` và clock = giờ commit mốc (Q9/A3); facts đo lại vào biên nhận, không vào thân PR (A1); lần đo ruleset trước lease ghi ở chỗ của vai cấp lease (Q12/A7); A7/Q3 thêm `merge_queue` + push thẳng (r9 Q10(d)); M5(d) delta ngoài bảng + holder mới; Q17 quyết định chủ kho cho phục hồi bootstrap; P3: đường đọc băm thân comment, A8 tính cả biên nhận. Nhánh đã merge `origin/master` `f5bef3a`. Bản nháp 7 (commit `19890bf`, sha256 `40e09b25…`) vá review Claude độc lập lượt 2 trên `4324f2a` (`claude-luot2-VERDICT.md`): `changes_requested` **0 P1 / 2 P2 / 2 P3** — A3/Q9 đòi bảng tiêu chí dương r3 thay vì `rc`; tách M5(d) fixture (ĐỎ vô điều kiện) khỏi A5 kho thật (R8), Q15 khớp theo; lịch sử neo băm + hiện vật verdict; mốc đo §1/§2 đồng nhất. Bản nháp 8 (commit ghi dòng này) vá review Claude độc lập lượt 3 trên `19890bf` (`claude-luot3-VERDICT.md`): `changes_requested` **0 P1 / 2 P2 / 3 P3** — bỏ miễn trừ của M5(c) trên fixture, (a) khai tập holder kỳ vọng, (d) "ngoài tập kỳ vọng của (a)"; A5/Q15 thêm R8(b) cho delta mở quyền/mất holder; mốc giờ không muộn hơn commit chứa nó; §8.6 cập nhật; verdict hạ lời khai đọc GitHub. |

## 0. Quyết định của chủ kho (27-09-2026)

**Vòng 1–2** (`soan-spec`, "Theo khuyến nghị"):

| # | câu | quyết định |
|---|---|---|
| Q1 | phạm vi | A1b = **(i)** bật cờ · **(ii)** nghiệm thu wiring thật · **(iv)** ghim lại `BIA_MO_LICH_SU` trước khi bật · **(v)** mỏ neo `PROFILE_ADAPTER_DA_DUYET` do chủ kho duyệt. **(iii)** xoá holder theo bia mộ nhánh mặc định ⇒ **A1c** |
| Q2 | facts Q10 | chủ kho đăng **một** comment facts trên #656, mỗi mục (a)–(i) một dòng bằng chứng; bản đóng băng neo **comment ID + sha256 UTF-8 của thân + biên nhận đọc ngược** (ai đọc, lúc nào, qua đường nào); comment là BẢN CHIẾU, thân sửa sau đóng băng ⇒ băm lệch ⇒ **DỪNG**, cần revision mới (connector `r4113875431`). Lần đọc lại để so băm phải đi **cùng đường** (client + endpoint) đã ghi trong biên nhận — đường đọc MCP chuẩn hoá thân thành thực thể HTML (CLAUDE.md, đo 22-08-2026); đường khác ⇒ **KHÔNG ĐO ĐƯỢC** ⇒ DỪNG, không tính là thân đã sửa; executor **tự đo lại** (a)(c)(d)(h) trước khi bật; thiếu ⇒ DỪNG |
| Q3 | Q10(d) ngoài kho | chủ kho sửa ruleset `20856202` trước cấp lease: required check `thu-hoi`, strict up-to-date, `allowed_merge_methods = [merge]`, `bypass_actors = []`, **không** `merge_queue`, **không** đường push thẳng lên nhánh mặc định bỏ qua required check (r9 Q10(d)) |
| Q4 | thời điểm | bản nháp bây giờ; đóng băng khi đủ tiền đề §1 |
| Q5 | Issue | #656, con của #564 |
| Q6 | rollback | A1b land với **sổ rỗng**; rollback = PR revert cờ về `False`, **chỉ hợp lệ khi sổ còn rỗng** |
| Q7 | review/trần | codex + connector + `human_audited`; ADR-0044 **≤ 300** dòng thêm; vượt ⇒ hỏi |
| Q8 | wiring thật | fixture có đột biến **và** canary PR thật; hiện vật ghi vào **một tệp trong write set**: `ops/reviews/thu-hoi-lease-a1b/bien-nhan-thi-cong.md` (connector `r4113875429`) |
| Q9 | `BIA_MO_LICH_SU` | mốc giữ **A0** (`0721811`); chạy **bộ đo thi công của A1a r3** (§8 mục 2, khối "Bộ đo THI CÔNG"): đo sha256 `ops/reviews/thu-hoi-lease-a1a-r2/do_q6_hk.py` = `0ec537e4…` và `mut_q6_hk.py` = `c4f04f03…` (lệch ⇒ DỪNG), rồi chạy đúng ba lệnh của r3 trên **cây mốc** `MOC_BIA_MO_LICH_SU`, clock = **giờ commit của mốc** (ghim, không phải giờ chạy); ra khác hằng ⇒ DỪNG. **Đạt** chỉ theo bảng tiêu chí dương của r3 §8 mục 2 (`ops/specs/THU-HOI-LEASE-A1a-r3.md:398–404`: đọc bản in, không suy từ `rc` một mình). Chạy `do_q6.py`/`mut_q6.py` (lỗi C5/C6 của r2) ⇒ biên nhận **vô hiệu** |
| Q10 | profile | digest đo trên **runner thật bởi mã CANONICAL**; executor ĐỀ XUẤT, chủ kho DUYỆT bằng cách trích digest trong audit; trôi ⇒ runbook (đo lại → PR dữ liệu → duyệt); đo ≥ 2 run cách ≥ 24 h, khác nhau ⇒ DỪNG |
| Q11 | consumer | `LAND-DOC-RECEIPT-THU-HOI` (#499 C1) là packet tiền đề riêng |
| Q12 | ruleset | đọc ruleset là **phép đo** ghi vào biên nhận, không là unit test. Trước cấp lease: **chủ kho/điều phối** (vai đóng băng + cấp lease) đo và ghi bền ở chỗ **của vai ấy** — comment trên #656 kèm sha256 thân + biên nhận đọc ngược, hoặc trong tệp lease; sau khi nhận lease và trước merge: **executor** chép nguyên văn lần đo trước kèm ID/băm nguồn vào `bien-nhan-thi-cong.md` rồi ghi lần đo của mình bên dưới (connector `r4113875427`) |

**Vòng 3** (sau codex lượt 1, "Theo khuyến nghị"):

| # | finding | quyết định |
|---|---|---|
| Q13 | F1 (P1): bước đo profile phải có trên canonical **trước** khi đo được digest | **packet tiền đề riêng `THU-HOI-LEASE-A1-DO-PROFILE`**: thêm bước đo vào workflow `thu-hoi` (chạy MÃ CANONICAL tại `workflow_sha`), ghim runner, cờ vẫn `False`. Đo ≥ 2 run canonical sau khi land. M6 cũ **rời** A1b |
| Q14 | F2 (P1): bật cờ chưa nối luật mới vào verdict production — `lenh_check`/`lenh_ai_dang_giu`/`lenh_kiem_thu_hoi_github` không gọi discovery (codex đo AST) | **packet tiền đề riêng `THU-HOI-LEASE-A1-WIRING`**: nối sổ + discovery vào verdict production **sau cờ** (cờ `False` ⇒ hành vi y hệt), land với cờ `False`. A1b chỉ **bật** + nghiệm thu |
| Q15 | F2 (P1): M5 "mọi rc bằng nhau" trái r9 Q6 | **phân loại delta theo Q6** trên cùng map ref + cùng clock — đủ HAI trục của Q6 (r9 `:381–388`): **eligibility** (rc) chỉ cho `0→8` bảo thủ ở cặp thay thế sinh sau mốc; **holder** so TẬP theo ID/path kèm nguyên nhân, không suy từ rc (codex lượt 2 F7). Delta khác: **fixture** (M5) ⇒ ĐỎ vô điều kiện; **kho thật** (A5, biên nhận) ⇒ theo r9 R8 (a)(b)(c) |
| Q16 | F4 (P2): nợ "C == S" trong hợp đồng consumer | **packet consumer đóng**: chốt hợp đồng C/S/H/T và có ca C≠S. A1b neo exact SHA + entry point consumer, test import consumer thật |
| Q17 | bootstrap A0 bị bỏ lỡ (connector `r4113875442`; review độc lập nháp 5) | chủ kho, phiên Claude Code 27-09-2026 ("Tôi đồng ý, làm đi" cho đề xuất đưa quét lịch sử có audit + receipt canonical đã xác minh vào T2; checkpoint #657 `issuecomment-5852188204`): bootstrap r9 R3 **đã bị bỏ lỡ** — consumer chưa land trước A0 và cập nhật canonical không được giữ đóng. Phục hồi = T2 (a)+(b); **không grandfather** (r9 R3). Đây là quyết định của chủ kho trong phạm vi A1b; nếu chủ kho muốn nó thành luật của spec cha thì đi revision r10 (protocol §12 `:1075–1076`) |

## 1. Tiền đề — thiếu một ⇒ KHÔNG đóng băng, KHÔNG cấp lease

| # | tiền đề | trạng thái lúc soạn (đo 01:30Z 27-09 tới trước commit `4324f2a` 04:31Z; từng ô ghi mốc riêng) | cách đo lại |
|---|---|---|---|
| T1 | **mã A1a đã land** | spec A1a r3 đóng băng (merge `f5bef3a`, thay r2 `67802bf`); mã **chưa** (đo ngay trước merge `7b99230` 04:30Z 27-09: `origin/master` = `f5bef3a`, 77 commit first-parent sau A0). #579 g20 giữ `ops/lease_publish.py`, `ops/lease_publish_test.py` tới **2026-09-29T00:00:00Z** (đo bởi agent khảo sát ~23:30Z 26-09) | merge A1a trên `--first-parent origin/master`; `ai-dang-giu` 2 đường ⇒ `NGƯỜI_GIỮ 0` (quét đủ ref) |
| T2 | **consumer `LAND-DOC-RECEIPT-THU-HOI` đã land**, có: exact commit SHA · entry point production gọi được · hợp đồng C/S/H/T đã chốt · ca C≠S (Q16) | **CHƯA** — `git grep -E 'check_suite\|check_run_url\|thu-hoi-receipt' 67802bf -- .claude` ⇒ rc=1 (codex lượt 1). **Bootstrap đã bị BỎ LỠ**, không chỉ "còn chờ" (connector `r4113875442`): r9 đòi consumer land TRƯỚC A0 và đóng cập nhật canonical tới receipt đầu tiên đã xác minh; A0 `0721811` đã land mà consumer thì chưa. Đo 03:08Z 27-09: `ls-remote` **441** ref máy chủ = **441** cục bộ (thiếu **0**, so tập tên); `git log --all -- ops/thu-hoi/` ⇒ **0** commit trên mọi ref; `origin/master` `67802bf`, **76** commit first-parent sau A0. Sổ RỖNG hôm nay KHÔNG chứng minh chưa từng có thu hồi thêm-rồi-xoá — phép quét trên mới là bằng chứng, và nó phải được audit | SHA + entry point ghim vào bản đóng băng, **CỘNG** (a) biên nhận quét lịch sử `ops/thu-hoi/` từ A0 `0721811` trên **mọi** ref (so tập tên `ls-remote` ↔ cục bộ trước khi quét; không fetch được ⇒ ĐỎ), do một vai KHÁC người đo audit lại; (b) **một** receipt canonical của consumer đã xác minh (run ID, attempt, `head_sha`, C/S/H/T). Thiếu (a) hoặc (b) ⇒ KHÔNG đóng băng — consumer land muộn tự nó KHÔNG đủ T2 (Q17) |
| T3 | **facts Q10 (a)–(i)** trên #656 | **CHƯA** | comment ID **+ sha256 UTF-8 thân + biên nhận đọc ngược** ghim vào bản đóng băng (Q2); thân đổi ⇒ revision mới |
| T4 | **ruleset** đủ Q3 | **CHƯA** — `GET rulesets/20856202` (đo 02:45Z 27-09, codex lượt 3 và đo lại trong phiên): required checks `gate (ubuntu-latest)`, `gate-packet-loop (ubuntu-latest)`, **không** `thu-hoi`; **`strict_required_status_checks_policy = false`**; `allowed_merge_methods = [merge, squash, rebase]`; `bypass_actors = []` | `GET rulesets/20856202` (đọc được; `branches/master/protection` vẫn 403 nhưng không cần). Trước cấp lease: **chủ kho/điều phối** đo; executor đo lại sau khi nhận lease và trước merge (Q12, A7) |
| T5 | **`THU-HOI-LEASE-A1-DO-PROFILE` đã land** và có **≥ 2** receipt của run canonical cách **≥ 24 h** cho **cùng** digest schema v2 (Q13) | **CHƯA** — workflow tại `67802bf` có 2 bước `run`, không gọi `hoso_adapter_do` (codex lượt 1) | receipt: run ID, attempt, `workflow_sha`, digest, `image_os`/`image_version` |
| T6 | **`THU-HOI-LEASE-A1-WIRING` đã land** với cờ `False` (Q14), có: exact commit SHA · danh sách **đường production** cần nghiệm thu (`check`, `ai-dang-giu`, admission `kiem-thu-hoi-github`) **kèm HỢP ĐỒNG verdict riêng từng đường** (ma trận A6) · **seam tiêm** map ref, clock, nguồn discovery nội bộ · kết quả discovery **quyết định** verdict (không chỉ được gọi). Validator ứng viên M4 của admission **độc lập với cờ** (r9 Q3) — WIRING không được đổi semantics ấy | **CHƯA** — chưa có spec | SHA + entry point + chữ ký seam ghim vào bản đóng băng; ca "gọi discovery rồi bỏ kết quả" của chính packet WIRING phải ĐỎ |

## 2. Số đo (L5 — đo lại trước MỖI bước công bố)

- `origin/master` lúc soạn: **`67802bf`** (01:49Z 27-09); **đo lại** trên **`f5bef3a`** (review Claude độc lập lượt 2, 04:31–04:35Z 27-09, giữa commit `4324f2a` và `19890bf`): bốn hằng A0 dưới đây và `ops/lease_publish_test.py:5154` **không đổi**; 100/89 run `thu-hoi` và annotation Ubuntu 26 **chưa đo lại** (§8 mục 6).
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
ops/reviews/thu-hoi-lease-a1b/bien-nhan-thi-cong.md
```

Ba đường (bản nháp 1–4 có hai — workflow rời sang `THU-HOI-LEASE-A1-DO-PROFILE`, Q13). Trùng write set A1a
và A1-WIRING ⇒ tuần tự sau cả hai. Test **được đọc/import** consumer ngoài write set (Q16) — không vi phạm L2.
Đường thứ ba là **một tệp cố định** (không phải `**`): biên nhận thi công — facts đo lại (A1), canary (A2),
dẫn xuất (A3), digest (A4), delta (A5), ruleset (A7). Bản nháp 4 viết "hiện vật ở nhánh riêng" mà không vai nào
được cấp quyền ghi đường ấy (connector `r4113875429`). Verdict review vẫn thuộc vai reviewer, ngoài write set executor.

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
| **M5** | Ca **phân loại delta** (Q15), cùng map ref + clock, cờ `False` → `True`, qua **verdict thật** của WIRING (không chép validator): (a) **fixture dương bắt buộc** — cặp thay thế sau mốc, sổ rỗng — phải cho **đúng** `0→8` trên trục eligibility **và đúng tập holder kỳ vọng** mà ca test **khai tường minh** (ID/path + nguyên nhân Q6; tập ấy có thể thêm holder, như r9 `:385–386` đo {r4} → {r1,r2,r3,r4}); tập delta rỗng ⇒ ĐỎ; tập holder lệch tập khai ⇒ ĐỎ; (b) eligibility: ngoài (a), mọi delta mở quyền (`8→0`, `11→0`, `12→0`) ⇒ ĐỎ; (c) holder: so **tập holder theo ID/path** kèm nguyên nhân trước/sau — mất một holder khi còn holder khác (rc vẫn `11`) ⇒ ĐỎ (trên fixture **không** có miễn trừ; miễn trừ theo nguyên nhân chỉ ở kho thật, A5); (d) **trên fixture, mọi delta ngoài tập kỳ vọng của (a)** — kể cả đóng quyền khác `0→8` (`0→11`, `0→12`, `8→12`…) và **holder mới** — ⇒ ĐỎ **vô điều kiện** (fixture không có lane/expiry thật để miễn) | `ops/lease_publish_test.py` |
| **M6** | Ca **production qua discovery**: cờ `True` + mỏ neo đúng ⇒ discovery chạy; mỏ neo sai/rỗng ⇒ `12` | `ops/lease_publish_test.py` |

## 6. `nghiem_thu` — mỗi tiêu chí nêu phép đo làm nó ĐỎ (L3)

| # | tiêu chí | ĐỎ khi |
|---|---|---|
| A1 | M1: cờ `True`; biên nhận đo lại (a)(c)(d)(h) ghi vào `bien-nhan-thi-cong.md`; thân PR chỉ trích và dẫn sha256 tệp ấy (thân PR là bản chiếu sửa được, không là thẩm quyền) | thiếu một mục, hoặc lệch facts #656 |
| A2 | M2: consumer thật chấp nhận fixture đủ; từ chối từng mắt xích sai; canary PR thật S≠H **và** C≠S cho join đủ qua API — ghi vào `bien-nhan-thi-cong.md` | đột biến gỡ một mắt xích mà ca xanh; canary thiếu mắt xích |
| A3 | M3: bộ đo thi công A1a r3 (Q9) chạy trên cây mốc, clock = giờ commit mốc, ra **đúng** hằng; ghi **nguyên bản in** của ba lệnh + rc + sha256 hai script vào `bien-nhan-thi-cong.md` | thiếu một tiêu chí dương r3 `:400–404` ⇒ DỪNG: tự kiểm `rc=0` + dòng cuối `TU_KIEM: 35/35 dat` + **0** dòng `HONG` · ma trận `rc=0` + dòng cuối `TAT_CA_KHOP` + đúng **27** dòng `DUNG ` + **0** dòng `SAI ` + dòng `DUNG LECH` duy nhất là `chet-im-lang-rc2` · Q6 thật `rc=0` + bản in `cmp`-bằng `ops/reviews/thu-hoi-lease-a1a-r2/q6-do-2026-09-26.json` (sha256 `1fc99cd9…`); biên nhận chỉ có `rc` ⇒ DỪNG; lệch digest/số cặp ⇒ DỪNG; băm script lệch ⇒ DỪNG; biên nhận nêu `do_q6.py`/`mut_q6.py` ⇒ vô hiệu. (Clock "lúc bật" của bản nháp 1–5 không thể ĐỎ: mọi C ≥ `2026-09-08T10:17:12Z` cho cùng `()` — r3 §8 mục 2) |
| A4 | M4: digest mỏ neo = digest trong ≥ 2 receipt T5; chủ kho trích nguyên digest trong audit | receipt khác nhau ⇒ DỪNG; mỏ neo ≠ receipt |
| A5 | M5 (a)(b)(c)(d) trên fixture; biên nhận đếm delta **theo loại và theo trục** (eligibility / holder) trên **kho thật** — delta ngoài (a) trên kho thật tách hai loại theo r9 `:383–385`: **bảo thủ** (thêm holder / được → bị chặn) chỉ nhận khi biên nhận ghi nguyên nhân Q6, lane bị ảnh hưởng **đã dừng** và expiry **đo được** (R8 (a)); **mất holder / mở lại quyền** (`8→0`…) chỉ nhận khi có **nguồn Q2** hoặc **cặp `BIA_MO_LICH_SU` đúng mốc**, cộng **audit riêng** (R8 (b)); không giải thích được ⇒ **không kích hoạt** (R8 (c)) | đột biến "gọi discovery rồi bỏ kết quả" (fixture dương ra delta rỗng) mà ca xanh; đột biến mở quyền một nhánh mà ca xanh; đột biến bỏ một holder trong tập ≥ 2 holder mà ca xanh; đột biến phân loại `0→12` (hoặc holder mới) là bảo thủ-được-nhận **trong fixture** mà ca xanh; biên nhận kho thật nhận một delta bảo thủ thiếu nguyên nhân/lane dừng/expiry, hoặc một delta mở quyền/mất holder thiếu nguồn Q2/cặp đúng mốc/audit riêng ⇒ DỪNG |
| A6 | M6 — **ma trận oracle riêng từng đường** (codex lượt 3 F8), mỗi đường mỏ neo sai/rỗng ⇒ `12`: **`check`** (eligibility) — fixture dương M5(a) ra `0→8`; **`ai-dang-giu`** (holder) — **tập holder theo ID/path** trước/sau theo M5(c), rc đi kèm tập, không suy tập từ rc; **admission `kiem-thu-hoi-github`** (namespace sổ) — sổ rỗng/hợp lệ ⇒ **giữ** kết quả nền (validator M4 độc lập cờ), và dữ liệu discovery **không khớp** (OID/nhánh mặc định lệch) ⇒ từ chối. Không đường nào được đổi semantics để "đạt" oracle của đường khác | trên **mỗi** đường: đột biến bỏ phép so mỏ neo mà ca xanh; đột biến gọi discovery rồi bỏ kết quả mà ca xanh; đột biến làm admission trả `8` cho fixture eligibility (mở rộng semantics) mà ca xanh |
| A7 | T4 (API ruleset) đo bởi **chủ kho/điều phối** trước cấp lease (ghi ở chỗ của vai ấy, Q12), rồi **executor** đo lại sau khi nhận lease **và** trước merge; executor chép lần đầu (kèm ID/băm nguồn) và ghi lần của mình vào `bien-nhan-thi-cong.md` | lần nào thiếu `thu-hoi`/strict/merge-only/không bypass, **hoặc** ruleset bật `merge_queue`, **hoặc** còn đường push thẳng lên nhánh mặc định không qua required check (r9 Q10(d)) ⇒ DỪNG |
| A8 | ADR-0044 cho `sensitive`: `git diff --numstat` **gồm cả** `bien-nhan-thi-cong.md` — **≤ 3 tệp và ≤ 300 dòng thêm** | vượt một trong hai mà chưa có ngoại lệ chủ kho ⇒ hỏi, không review |

## 7. `hinh_dang_ke_thua` (L4)

Chép từ A1a r2 §7 (`9bc0fe28…`), cộng #651 và lượt 1 của đặc tả này:

| hình dạng | số lần | nguồn |
|---|---|---|
| **"nguồn được tin mà chưa xác minh"** | **7** | r9 lượt 1–6 · A1a r2 lượt 1 F1. **Lần 8** phải nhắm chỗ A1b **trao thẩm quyền**: M4 (digest) và M1 (facts Q10). |
| "thu hồi là dữ liệu ghi vào bản sao" | 3 | r9 §1 (2) · #564 dạng 2. Chứng cứ thêm 27-09: rút hạn lease #651 g1 (PR #654/#655) không tới được hai nhánh phiên khác. |
| "lời khai hội tụ rộng hơn phép đo" | 3 | r9 g2, lượt 1 |
| "hai cổng bất đồng" | 1 | r9, #473 |
| **"đặc tả tự nới luật của protocol"** (mới) | **1** | bản nháp 1–4: trần Codex 10 chép tiền lệ thay vì trần 2 của §8 (connector `r4113875422`) |
| **"bản chiếu có thể sửa được dùng làm thẩm quyền"** (mới) | **1** | bản nháp 4 T3: neo comment ID trần (connector `r4113875431`) |
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
6. **Các số chưa đo độc lập lần hai** (codex lượt 1): 100/89 run `thu-hoi`, annotation Ubuntu 26. Đã đo lần hai: hạn #579 g20 (review Claude lượt 1, đọc tệp lease `dang-lease-dau-truoc-kiem-sau-r21-g20-claude` qua git, trước 04:30Z 27-09) · ruleset (T4: codex lượt 3 + đo lại trong phiên, 02:45Z 27-09).
