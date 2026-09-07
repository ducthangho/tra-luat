# ĐẶC TẢ PACKET — `THU-HOI-LEASE-VA-CAP-LAI`, **revision 3**

```yaml
packet_id: THU-HOI-LEASE-VA-CAP-LAI
packet_issue: CHƯA CÓ          # điền khi đăng Packet Issue (Bước 3); spec đóng băng TRƯỚC Issue
revision: 3
thay_the: 9e775a154dd83741fd4e7af85aaeae1f5693ceabc5c5763cf6890ff4f2606c80   # sha256 r2, review lượt 2
thay_the_r1: 43844cb2ea2653f502320a6f35a6e3ae7fd182770f02b62d4d73b9aa8dbea6f9
review_class: sensitive        # ops/lease_publish.py + .claude/dev/packet_loop.py + .github/workflows/ — §8, fail-closed
executor: claude
reviewer: codex
assurance_target: cross_approved
base_sha: b416830ef2a509d60203d55552ce17950afcf67c   # origin/master lúc đóng băng
```

**Mọi con số đo lúc `13:2x–15:1xZ 07-09-2026` trên `303` ref** (302 tên nhánh máy chủ + 1 nhánh cục bộ
`master`); reviewer lượt 1 (13:52Z) và lượt 2 (14:33Z) đo lại trên mirror và **khớp**, trừ chỗ ghi "đính chính".
**Đo lại trước mỗi bước công bố** (L5). Đơn vị (L1): "cặp" = **(blob, đường dẫn) duy nhất** trên mọi ref — `ai-dang-giu`
in **một dòng cho mỗi cặp**, không phải mỗi ref; "lease_id" = giá trị trường `lease_id`; "ref" = một dòng của
`git for-each-ref refs/heads refs/remotes` trừ `*/HEAD`. Con số chỉ có ở phía điều phối (API GitHub, mạng) được
đánh dấu **[API]** — reviewer offline không đo lại được và spec không dùng chúng làm bằng chứng thẩm quyền.

## 0. Lịch sử review — và lệnh chủ kho cho vòng lặp

| lượt | model/effort | thời lượng | verdict | sha256 verdict |
|---|---|---|---|---|
| 1 (r1 `43844cb2…`) | codex `gpt-6-astra` high | 1842,8 s · stderr 777 646 B | `changes_requested` — 11 P1 + 3 P2 | `b60a755f611bf814e0c9116e1cb5c9c4f9cb5ac3f1a6e96a951cd3dc7f17123e` |
| 2 (r2 `9e775a15…`) | codex `gpt-6-astra` **xhigh** | xem biên nhận | `changes_requested` — cũ: 5 ĐÓNG · 8 ĐÓNG-MỘT-PHẦN · 1 ĐÓNG SAI; mới: **9 P1 + 2 P2** (N1–N11) | ghi ở commit r3 |

§12 đặt trần **hai** lượt review codex trên một PR làm stop condition; đây là lượt review **đặc tả** trước
Issue/lease trên PR #475 (không phải review packet code), và chủ kho ra lệnh trong phiên (`07-09-2026 ~14:2xZ`):
*"hãy lặp claude, fable 5.1 xhigh vá, gpt-6-astra codex xhigh review, có hint patch cho tới khi hết P1"*. Lệnh chat
KHÔNG phải neo; nó được chép ở đây và ở thân PR #475 để lượt ≥3 có căn cứ đọc được, và bộ đếm lượt được giữ trong bảng
trên chứ không reset.

### 0.1 Delta r2 → r3 theo finding lượt 2

| finding (P) | r2 sai/thiếu ở đâu | r3 làm gì |
|---|---|---|
| N1 `canonical-remote-identity-unbound` (P1) | Q4 tin "máy chủ mà `origin` trỏ tới" — đổi `origin` sang bare khác có cùng heads/symref ⇒ sổ giả có hiệu lực | Q4: danh tính kho **ghim trong mã** (`KHO_CANONICAL`), so với `git ls-remote --get-url origin` đã áp rewrite; lệch/không đo ⇒ 12; fixture tiêm qua API nội bộ của test, không có cờ production |
| N2 `snapshot-pinned-after-unverified-recapture` (P1) | "sau đối chiếu, chụp map" cho phép chụp lại map mới rồi ghim | Q4: chụp map cục bộ **TRƯỚC** phép so; OID canonical = OID của nhánh mặc định trong **advertisement đã so**; không chụp lại |
| N3 `admission-workflow-does-not-cover-canonical-updates` (P1) | M9 chỉ mở `paths` trong workflow đăng lease (nhánh `ops/**`, lọc `author.name`) — không phủ PR thường/integration/`merge -s ours` | M9: **workflow riêng** `ops-thu-hoi-admission.yml`, `pull_request_target` vào nhánh mặc định + `workflow_dispatch`, không phụ thuộc đường dẫn lease, `rc=9`, tên tác giả |
| N4 `canonical-checker-bootstrap-is-circular` (P1) | bước "neo bộ kiểm" chạy mã từ canonical, nên lượt đầu tiên không có lệnh mới (`invalid choice`, rc=2) | Q7: **A0** (mã + test, sổ CHƯA kích hoạt, cổng CI đòi `ops/thu-hoi/` rỗng) → **A1** (workflow + kích hoạt, dùng mã A0 đã canonical) → B → C |
| N5 `effective-write-set-and-symlink-resolution-missing` (P1) | giao trên chuỗi đường dẫn; symlink trong cây trỏ cùng tệp không giao; closure §5 chưa có nguồn policy | Q3: giải symlink/parent **trong cây OID đã ghim**; dùng `effective_write_set` nếu lease có, không thì `write_set` — **chọn tường minh**, khai giới hạn closure là dependency #473 |
| N6 `historical-cutoff-revives-feature-holders` (P1) | mốc canonical `b416830` không chứa cặp `gate-tach` (chúng ở #468) ⇒ r1–r3 gate sống lại, r4 `check` 8 | Q6: mốc = OID canonical lúc **A0 land**, danh sách đóng **ghim trong mã**; kích hoạt đòi **delta người giữ cũ/mới = 0** đo thật; đo được cả 4 gate hết hạn `2026-09-08T10:17:12Z` |
| N7 `candidate-map-omits-entry-mode` (P1) | map path→blob bỏ mode/type; đổi 100644→120000 giữ blob qua cổng rồi reader 12 | M1/M4/A8: map path→**(mode, type, blob)**; kiểm M1 **toàn namespace** `ops/thu-hoi/` của T |
| N8 `record-lease-guard-has-no-candidate-id` (P1) | guard lấy ID từ state; `record-lease` có `lease: null` ⇒ sống→8, thu hồi→không ghi stale | M7: guard nhận `target_lease_id`; `record-lease` truyền ID ứng viên đã validate |
| N9 `acceptance-prepublish-and-second-parent-contradictions` (P1) | A5 gọi CLI `check` trước publish = 0 trong khi Q3 đòi ứng viên đã có trên máy chủ; A8 gộp "S ở cha thứ hai" vào nhóm 8 | Q3/A5: tách **hàm thuần** (0/0) khỏi **CLI** (chưa publish ⇒ 12); A8: cha-thứ-hai giữ X ⇒ 0, mất X ⇒ 8 |
| N10 `authorization-json-and-url-contract-is-open` (P2) | JSON không đóng (float, khoá trùng), 3 loại object chưa có mapping endpoint | Q2: chỉ **Issue comment**; schema JSON đóng, kiểu chặt, khoá trùng ⇒ 8 |
| N11 `readback-after-admission-lifecycle-undefined` (P2) | `kiem-github` của lease mới đọc lại căn cứ đã tiêu thụ ⇒ 12 khi object bị xoá | Q2.3: sau khi vào canonical, tin event; không đọc lại căn cứ lịch sử |
| 8 finding lượt 1 ĐÓNG-MỘT-PHẦN | phần thiếu chính là N1/N2/N3/N5/N6/N7/N9 và Q12-bootstrap | đóng qua các hàng trên |
| `size-estimate…` (đã ĐÓNG) | câu "không có slice nào ≤300" sai với B/C | §write_set sửa; ước lại theo A0/A1/B/C |

Đính chính số của r2 do reviewer lượt 2 đo: `6635379` có **1** `gpgsig` SSH (r2 viết "2" là số dòng BEGIN/END);
"5 ref mang `26f07b4` sau PR #475" là **[API]**, mirror chỉ đo 4 — tách khỏi mẫu số 303; lease_id `CÒN_HẠN`
**7** và chưa bia mộ **3** tại 14:33Z (#456 hết hạn `14:30:07Z`, đo phía điều phối 14:30:12Z: `HET_HAN`).

## `nguon_cap_viec`

- Lệnh chủ kho lập phiên (`session_01Vt7NfNpABHfSWpxvx4aJGE`, 07-09-2026): *"bổ sung cơ chế CHỦ KHO THU HỒI
  LEASE và CẤP LẠI CHO MỘT PR KHÁC"*. Neo là Packet Issue ở Bước 3, không phải câu chat.
- Nợ `AG-T0-01B-thu-hoi-lease-chua-co-duong` (`ops/specs/ag-t0-01b-r4.md` §0.2; `CLAUDE.md`).
- Nợ #473: `bia-mo-check-bo-sot-chieu-nguoc`, `cong-check-thieu-do-phu-tham-quyen` — đóng phần "bia mộ theo blob"
  và "độc quyền write set trên tập khai báo"; phần "bốn trường phái sinh / policy closure" KHÔNG.
- Lease g2 `wp461-…-exec-1g2-claude-20260907` (PR #474), khoá `hoi_tu_nguoi_giu_doi_thao_tac.no_nen`.

## 1. Vấn đề — ĐÃ ĐO, hai reviewer đã đo lại

Thu hồi hôm nay chỉ có bia mộ hai chiều (`thay_the_cho` ↔ `da_bi_thay_the`), ép bởi
`ops/lease_publish.py::_kiem_bia_mo` (595–617). Bia mộ là **dữ liệu ghi vào TỆP CŨ**, mà tệp cũ có bản sao trên
nhiều ref:

| phép đo | giá trị |
|---|---|
| ref quét | **303** |
| cặp (blob, path) trong `ops/leases/` · đường dẫn · lease_id | **288 · 273 · 273** |
| lease_id có >1 blob | **7 / 273** (số blob 2,2,4,4,5,3,2) |
| lease_id `CÒN_HẠN` / chưa bia mộ trên ≥1 ref | **8 / 4** tại 13:41Z → **7 / 3** tại 14:33Z (#456 hết hạn) |
| r2 wp461: cặp | **2** — `26f07b4` (0 bia mộ; 4 ref: `heads/master` · `origin/master` · `origin/ops/cap-lease-461` · `origin/claude/soan-spec-3-viec-treo-20260906`) · `fdfde3a` (bia mộ; 1 ref: `origin/ops/lease-wp461-g2`) |
| #456 `mutant-…-exec-1`: `8b2103c` chưa bia mộ / `1f95042` bia mộ | **11 ref / 1 ref** (bia mộ trên #468) — tiền lệ thứ hai, cùng hình dạng |
| tệp mang `da_bi_thay_the` trên `origin/master` / trên #468 | **7 / 11**; 7 cặp trên master đều hai chiều hợp lệ; ba `gate-tach` + `mutant` chỉ ở #468 |
| commit riêng của #468 | **31** |
| `ai-dang-giu` 4 đường wp461 | `NGƯỜI_GIỮ 2`, rc=11 (mirror: 3,3–3,8 s mỗi đường) |
| `check` lease g2 | rc=0 `ĐĂNG ĐƯỢC` trong khi người giữ là 2 |

Ba hệ quả có dòng mã: (1) `_kiem_bia_mo` dùng `any(...)` (606–610) ⇒ hai cổng bất đồng; (2) `kiem()` (787–890)
gọi `_lease_cham_duong` **0** lần ⇒ `check` không đo độc quyền; (3) bia mộ nằm trên nhánh `ops/**`; số ref mang
bản sống chỉ tăng (**[API]** PR #475 của chính spec này là ref thứ 5 mang `26f07b4`).

**Bất biến:** *cấp ở bất kỳ ref nào chỉ THÊM người giữ (chiều an toàn); thu hồi phải ở đúng MỘT chỗ mọi phép đo đọc,
chỗ ấy phải có cổng tiếp nhận chạy MÃ ĐÃ CANONICAL trước khi có hiệu lực, và nguồn ấy phải có danh tính ghim.*

## 2. Sáu câu hỏi — trả lời kèm phép đo

### Q1 — Chủ kho phát lệnh thu hồi ở ĐÂU?

➡️ **Sổ thu hồi append-only `ops/thu-hoi/<lease_id>.yaml`** trên nhánh mặc định của kho canonical. **Hiệu lực =
(i) sổ đã KÍCH HOẠT (A1 land, Q7/Q10) ∧ (ii) bản ghi hợp lệ M1 ∧ (iii) đã qua cổng tiếp nhận M9 trên đúng cây sẽ nhận
∧ (iv) có mặt trong cây canonical tại OID đã chụp (Q4).** Bản ghi ở ref khác = CHƯA thu hồi. Nhánh mặc định là thứ
**máy chủ có danh tính ghim** khai (Q4).

| phương án đã cân nhắc | vì sao loại |
|---|---|
| Sửa tệp lease cũ trên MỌI ref | đẩy vào nhánh người khác (#468: 31 commit riêng); phiên web không xoá/force ref; là chính lỗi hiện nay |
| Bia mộ trong cùng nhánh `ops/**` với lease mới | `NGƯỜI_GIỮ 2` là phép đo của phương án này |
| Chỉ comment Issue làm sổ | online-only; `ai-dang-giu` cố ý offline fail-close; comment là hiện vật sửa được (`kiem()` khối 795–812) |
| `git notes` / `refs/thu-hoi/*` | không fetch mặc định, không qua PR, không diff trong review |
| `ops/leases/thu-hoi/` | `_quet_lease_toan_kho` `ls-tree -r ops/leases` đọc bản ghi như LEASE ⇒ 12; workflow đăng lease cố ĐĂNG nó |
| Mở `paths` trong `ops-publish-lease.yml` (r2) | chỉ bắn cho push `ops/**`, lọc `head_commit.author.name`, không phủ PR thường/integration/`merge -s ours` (N3); chạy mã từ canonical nên lượt đầu thiếu lệnh (N4) |

### Q2 — Danh tính chủ kho và LỆNH thu hồi

Bằng chứng Git tại `b416830` (hai reviewer đo lại):

| object | dữ liệu Git | giới hạn |
|---|---|---|
| `b416830` (merge PR #471) | author `ducthangho`, committer `GitHub <noreply@github.com>`, **1** `gpgsig` PGP; `%G?=E` với keyring rỗng | không chứng minh ai bấm nút; Git không lưu `author.login` |
| `6635379` (lease r2, phiên agent đẩy) | author/committer `Claude <noreply@anthropic.com>`, **1** `gpgsig` SSH | có chữ ký ≠ đã xác minh người ký |
| **[API]** actor 5 lượt `ops-publish-lease` 372–376 = `ducthangho`; `author.login` của `6635379` = `claude` | đo qua MCP phía điều phối | dữ liệu API; reviewer không readback |

Kết luận **không đổi, đã được chính `b416830` thừa nhận**: trong tài khoản chủ kho **không có ranh giới máy** tách
"chủ kho gõ" khỏi "agent cầm PAT của chủ kho". Spec không bịa; chữ ký `web-flow` ngoài hợp đồng (`curl` 403; push
thẳng của chủ kho không có chữ ký ấy).

➡️ Bản ghi thu hồi dùng **đúng chuẩn thẩm quyền của bản ghi CẤP** + **cổng tiếp nhận bắt buộc TRƯỚC hiệu lực**:

1. `thu_hoi_boi`: chốt provider (`rc=4`) rồi danh sách cho phép `NGUOI_CO_THAM_QUYEN` (`rc=4`) — cùng hai chốt,
   cùng thứ tự với `granted_by`.
2. `can_cu`: **MỘT** URL HTTPS GitHub của **Issue comment** (`https://github.com/<KHO_CANONICAL>/issues/<N>#issuecomment-<ID>`),
   cùng repository với danh tính ghim (Q4), `<N>` == `packet_issue`. Issue body / PR review comment **không** được hỗ
   trợ ở revision này ⇒ `rc=8`, không đoán endpoint. Readback endpoint Issue comment phải trả đúng `id` == `<ID>`,
   `issue_url` đúng repo và `<N>`, `user.login ∈ NGUOI_CO_THAM_QUYEN` (khác ⇒ `rc=4`, kể cả `github-actions[bot]`,
   kể cả collaborator). Phân biệt **Issue number** trong URL với **global object ID** của comment.
   Thân comment có **đúng một** khối lệnh — ví dụ hợp lệ về cú pháp (ID là fixture):

   ````text
   ```json lease_revocation_authorization
   {"event":"lease_revoked","lease_id":"X","packet_issue":461,"cap_lai_cho":"Y","thu_hoi_boi":"ducthangho","thu_hoi_luc_utc":"2026-09-07T13:00:00Z"}
   ```
   ````

   Parser JSON: từ chối **khoá trùng** trước khi tạo dict; root phải là object; **đúng sáu khoá**, không thiếu/thừa;
   `packet_issue` là integer dương (không bool/float); chuỗi theo M1; `cap_lai_cho` là ID hợp lệ hoặc `null` (YAML
   vắng/null/rỗng chuẩn hoá về null trước khi so; JSON phải ghi tường minh). So **giá trị VÀ kiểu** từng trường với
   bản ghi. Thiếu/trùng/lệch/JSON lệnh hỏng ⇒ `rc=8`; HTTP ≠ 200 / timeout / envelope API hỏng / thiếu định danh ⇒
   `rc=12` (dòng trạng thái HTTP thật). Văn xuôi nhắc ID, phủ định, ID chỉ là tiền tố ⇒ **không phải lệnh**.
3. Cổng M4 readback **mọi bản ghi mới so với S** ở mỗi lần kiểm ứng viên T; receipt của lần trước không bỏ được
   readback khi bản ghi chưa canonical. Receipt (M9 đăng bản chiếu lên `packet_issue`, tiền tố `**Thu hồi `X`**`)
   ghi: danh tính kho, nhánh mặc định, S/T, OID bộ kiểm đã chạy, từng path/(mode, type, blob), comment ID và sha256
   thân UTF-8 **đã đến**. Receipt chỉ có giá trị cho đúng S/T. **Sau khi bản ghi vào canonical**: sửa/xoá object API
   không gỡ event, và `kiem-github` của lease mới **không đọc lại căn cứ lịch sử** (N11) — chỉ dùng bản ghi canonical.
4. Hiệu lực theo Q1(i)–(iv). Merge là *hành vi*, tệp là *lời khai*, M9 là *cổng đứng giữa chạy mã canonical*.

Lớp này phân biệt **tài khoản chủ kho** với **tài khoản khác** — toàn bộ thứ GitHub xác thực được.

### Q3 — Lease mới neo vào thu hồi thế nào; `check` bỏ `any(...)` ra sao

Giữ `thay_the_cho: [X, …]`. Mọi cổng dùng **cùng snapshot Q4** và **cùng hàm trạng thái theo lease_id**. Với từng X:

1. **Có bản ghi sổ cho X** (canonical, M1): `cap_lai_cho` null hoặc == `lease_id` mới ⇒ qua; khác ⇒ `rc=8`, **không
   rơi sang bia mộ**. Sổ ưu tiên tuyệt đối.
2. **Không có bản ghi**: chỉ nhận cặp **lịch sử** trong danh sách đóng Q6. Không có ⇒ `rc=8`, chẩn đoán trỏ
   `ops/thu-hoi/` + OID canonical.
3. **Chiều ngược**: lease đang `check` đã chết (sổ HOẶC danh sách lịch sử) ⇒ `rc=8`, kể cả không khai `thay_the_cho`.

**Độc quyền — cho MỌI lease** (không riêng lease có `thay_the_cho`). Quyết định tường minh về tập so:
- Tập của mỗi lease = `effective_write_set` nếu lease có trường ấy (dispatcher điền, §3.2), **nếu không** = `write_set`
  khai báo. Closure theo policy `.github/coordination/change-impact.v1.json` (§5) **chưa tồn tại trên canonical**
  (đo 15:20Z: tệp ấy và `schemas/change-impact.v1.schema.json` đều vắng; `schemas/` chỉ có `review_verdict.v1.schema.json`) ⇒ là dependency #473; spec này **không** tự tạo policy, không mặc nhiên coi closure rỗng, và khai
  thẳng: cho tới khi policy canonical có, độc quyền đo trên tập khai báo + giải symlink.
- Chuẩn hoá §5: separator `/`; từ chối tuyệt đối/`.`/`..`/thoát repo (⇒ 12 nếu lease `CÒN_HẠN`); NFC; case-fold;
  `normpath`; mục kết thúc `/` = prefix, còn lại exact; `planned:` bỏ nhãn. **Giải symlink và parent trong cây OID đã
  ghim** (entry mode `120000` ⇒ đọc đích, chuẩn hoá, so đường đã giải; đích thoát cây ⇒ 12) — không dùng worktree.
- Giao (exact∩exact, exact∈prefix, prefix∩prefix, sau giải symlink) với lease `CÒN_HẠN` chưa chết khác ⇒ `rc=11` nêu
  `lease_id` + đường va chạm. Tập của lease `CÒN_HẠN` không đọc được ⇒ `rc=12`; lease `HẾT_HẠN` (đã xác minh hạn)
  không đọc được: chẩn đoán, không chặn (đo: 3 lease `plat-x4/x5` 20-08 dùng `planned:` đều hết hạn).
- Không dùng `_lease_cham_duong` (so chuỗi) làm phép giao.

**Hàm thuần vs CLI (N9):** hàm thuần `trang_thai(snapshot, ứng_viên)` tính vị từ trên bất kỳ ứng viên nào (test dùng;
hai ứng viên Y/Z trước publish có thể cùng 0/0 — đó là bằng chứng giới hạn của ảnh chụp). CLI `check <tệp>` vận hành:
ứng viên phải **đã nằm trên một ref máy chủ trong snapshot đúng (blob, path)** — chỉ cùng ID chưa đủ; chưa publish ⇒
`rc=12`, không in `ĐĂNG ĐƯỢC`. `check rc=0` là **ảnh chụp**, không phải acquire nguyên tử. Cấp → readback `ai-dang-giu`
→ cho bắt đầu do **một** bên điều phối tuần tự hoá (Q11). Fencing máy là dependency khác.

`thu_hoi_can_cu` trong lease (tuỳ chọn) chỉ để đối chiếu; cổng không dùng nó bỏ phép kiểm nào.

### Q4 — MỘT snapshot có danh tính, MỘT phép tính cho mọi bản sao

1. **Danh tính nguồn ghim trong mã**: hằng `KHO_CANONICAL = "github.com/ducthangho/tra-luat"` trong
   `ops/lease_publish.py` (mã đã canonical, sửa phải qua commit có review — cùng luật `NGUOI_CO_THAM_QUYEN`). So với
   `git ls-remote --get-url origin` (đã áp `url.*.insteadOf`), chuẩn hoá: bỏ scheme/`.git`/`/` cuối, so **bằng nhau
   tuyệt đối** host + đường (đo: `https://github.com/ducthangho/tra-luat`). Lệch / không đo ⇒ `rc=12`. Không lấy tên
   `origin`, cùng heads/SHA/symref làm chứng. Fixture: test tiêm danh tính qua **API nội bộ** (tham số hàm), **không**
   có cờ CLI/biến môi trường production bỏ chốt.
2. **Chụp map cục bộ TRƯỚC**: `for-each-ref refs/remotes/origin` → map tên→OID (một lần).
3. **Một lời gọi discovery**: `git ls-remote --symref origin HEAD 'refs/heads/*'` → nhánh mặc định máy chủ khai + tập
   `(tên, SHA40)`. Đo 14:0xZ: `ref: refs/heads/master\tHEAD`; `refs/remotes/origin/HEAD` cục bộ trong clone này
   **không** là symref — không dùng. Workflow truyền `--nhanh-mac-dinh "$MAC_DINH"`; phải bằng symref máy chủ, lệch ⇒
   12. HEAD máy chủ vắng/mơ hồ ⇒ 12. **Không fallback tên.**
4. **So**: mọi tên máy chủ phải có trong map cục bộ với **cùng SHA40** (thiếu/lệch ⇒ 12 nêu tên + hai SHA); local
   `refs/heads/*` không bù. **OID canonical = OID của nhánh mặc định trong advertisement ĐÃ SO** (HEAD OID cũng phải
   khớp). **Không chụp lại** map/ref sau phép so (N2).
5. **Đọc theo OID**: mọi `ls-tree`/`cat-file`/tra sổ/danh sách lịch sử/write set/symlink dùng OID đã ghim. Thiếu
   object / `git` rc≠0 / output hỏng ⇒ 12; chỉ kết luận "sổ vắng" khi đã đọc thành công cây chứa nó. Snapshot mang
   **một** timestamp cho mọi consumer.
6. Nạp sổ một lần; áp theo `lease_id` cho **MỌI** cặp: in `<hạn> · ĐÃ_THU_HỒI`, không vào tập người giữ, bất kể blob.
   `blob_da_biet_luc_ghi` không phải allowlist. Đầu ra: một dòng/cặp + `MAP_REF` (cặp → tập ref) + `MÙ 0` với số ref
   đã đo. `check`, `ai-dang-giu`, `body`, `kiem-github`, `kiem-thu-hoi-github` dùng chung hàm trạng thái.
7. Chi phí: `ls-remote --symref` thay `ls-remote --heads` (+0 lời gọi mạng) + `get-url` (cục bộ) + đọc sổ + kiểm; A6 đo
   cũ/mới xen kẽ, không lấy 4,1 s / 3,359 s / 3,676 s làm mẫu số cố định.

### Q5 — Việc còn dở của lease bị thu hồi

`ls-remote --heads origin 'refs/heads/agent/wp461*'` ⇒ RỖNG **[API]** — chỉ chứng minh không có ref khớp mẫu.
§4/ADR-0028: worker cũ không heartbeat/push/handoff; branch/PR → `stale`; generation mới không tự cherry-pick. Ba mức răng:

1. **Executor cũ, `packet_loop.py` (M7):** guard chung `_kiem_thu_hoi(root, target_lease_id, snapshot)` gọi ở **5** cửa
   TRƯỚC mọi thay đổi bền (đo: `record-post`/`transition`/`record-review` gọi `_kiem_luoc_do_lease` **0** lần).
   `record-lease` validate ứng viên từ đối số rồi truyền **ID ứng viên** (state còn `awaiting_lease`, `lease: null`);
   bốn cửa kia lấy ID từ `state.lease` (N8). Snapshot: **cùng routine Q4** (có mạng: `ls-remote`, `get-url`); quyết định
   tường minh: **không có chế độ đệm offline** ở revision này — `ls-remote` hỏng ⇒ `KHÔNG ĐO ĐƯỢC` ⇒ `RC_STATE`, state
   không đổi (fail-close; executor không mạng không mở lượt được, và đó là ý định). Ba trạng thái: **thu hồi** ⇒ state
   `stale` + history `lease_revoked_seen{lease_id, oid_canonical, blob_ban_ghi, snapshot_ts}` (idempotent; ở
   `record-lease` không ghi `record_lease`), lưu xong mới `RC_STATE`; **sống** ⇒ tiếp; **không đo được** ⇒ `RC_STATE`
   + `KHÔNG ĐO ĐƯỢC`, không sửa state; lỗi ghi state cũng chặn. `--root` tường minh (state-dir có thể ngoài kho).
2. **Lease mới (M3):** `check` từ chối khi còn người giữ — trên ảnh chụp.
3. **Land** — ngoài write set, nợ `LAND-DOC-SO-THU-HOI`: `land-packets` phải hỏi sổ. Chưa có ⇒ chưa răng máy ở tầng land.

Không có gỡ thu hồi; cấp lại = lease mới, `lease_id` + `generation` mới (ADR-0025).

### Q6 — Bia mộ lịch sử: danh sách đóng, mốc, di trú

➡️ **Sổ thay bia mộ cho mọi thu hồi MỚI; bia mộ = danh sách đóng ghim trong mã.**

- **Mốc** = OID canonical **lúc A0 land** (không phải `b416830` cố định — N6). Lúc A0 land, executor tính danh sách
  cặp `(cũ, mới, blob cũ, blob mới)` hai chiều hợp lệ (lease_id == tên tệp, cả hai tệp) trên cây canonical mốc ấy và
  **ghim vào mã** (`BIA_MO_LICH_SU`); test tiêm danh sách qua API nội bộ, không dựng lại từ cây ứng viên. Sau mốc, bia
  mộ mới ⇒ `check` `rc=8` trỏ `ops/thu-hoi/`. Bia mộ trên feature ref không phải nguồn thẩm quyền.
- Cặp lịch sử áp theo **lease_id toàn kho**; vòng/chuỗi kết thúc hữu hạn; mâu thuẫn ⇒ 12. Sổ > lịch sử; chiều ngược
  chặn cả hai.
- **Tác động đổi ngữ nghĩa phải ĐO trước kích hoạt (N6):** so bảng người giữ/eligibility **cũ vs mới** trên mọi đường
  có lease `CÒN_HẠN`; delta ≠ 0 ⇒ chưa kích hoạt, cần bản ghi di trú riêng (đủ Q2) hoặc chờ hết hạn **đo được**. Đo
  hôm nay (14:3xZ): lane `gate-tach` (#463) có r1→r2→r3 bia mộ chỉ trên #468, r4 sống — dưới luật mới tại `b416830`
  cả 4 ID giữ `ci.yml`; nhưng cả 4 hết hạn `2026-09-08` (**03:37:33Z · 07:50:35Z · 09:44:51Z · 10:17:12Z**), tức
  trước bất kỳ mốc A0 khả dĩ nào — vẫn phải **đo lại** lúc A0 land, không suy từ lịch.
- Di trú `CÒN_HẠN` chưa bia mộ (đo 14:33Z, đo lại lúc cấp lease):

| lease_id | tình trạng | việc |
|---|---|---|
| `wp461-…-exec-1r2-claude-20260907` | phải chết; lệnh chủ kho hiện chỉ ở lease g2 + PR #474 — **chưa có object đạt Q2** (comment `5569885143` là bản chiếu `github-actions[bot]`) | **M5 (slice C)** sau Q8/Q10/Q11 |
| `mutant-…-exec-1` (#456) | **HẾT_HẠN** (đo 14:30:12Z ≥ 14:30:07Z) | không di trú |
| `wp461-…-exec-1g2` | người giữ dự kiến sau C; còn phải đo độc quyền + Q11 | không tự cấp lại từ lời khai |
| `gate-tach-…-1r4` (#463) + r1–r3 trên #468 | xem tác động ở trên | không đụng; đo delta trước kích hoạt |

## `write_set` — theo slice (Q7)

| slice | đường dẫn | nội dung | ước dòng thêm |
|---|---|---|---|
| **A0** | `ops/lease_publish.py` · `ops/lease_publish_test.py` | M1–M4, M6; hằng `KHO_CANONICAL`, `SO_THU_HOI_KICH_HOAT = False`; **cổng bootstrap**: ca test đòi `ops/thu-hoi/` **rỗng** trên canonical và trên HEAD ứng viên (chạy ở `ci.yml` lane PR qua `chay_lease_publish_test.sh`) | 480–680 |
| **A1** | `.github/workflows/ops-thu-hoi-admission.yml` (MỚI) · `ops/lease_publish.py` · `ops/lease_publish_test.py` | M9; đổi `SO_THU_HOI_KICH_HOAT = True` + ghim `BIA_MO_LICH_SU`/mốc; thay cổng bootstrap bằng ca wiring (A11) | 80–140 |
| **B** | `.claude/dev/packet_loop.py` · `.claude/dev/packet_loop_test.py` | M7–M8 | 150–220 |
| **C** | `ops/thu-hoi/wp461-be-mat-thu-hai-cua-codex-exec-1r2-claude-20260907.yaml` | M5 | ~15 |

Sáu đường dẫn tổng, không ký tự đại diện; `ops-publish-lease.yml` **không đụng** (N3). ADR-0044 (`sensitive` ≤ 3
tệp, ≤ 300 dòng thêm): **A0 vượt dòng** ⇒ ngoại lệ có phạm vi, lý do: phần vượt là ca fail-close (A1–A9 ≈ 30 ca +
đối chứng + đột biến); cắt ca là đổi độ phủ lấy con số. A1/B/C **không** vượt. Mốc neo đo lại: PR #250 = 2 tệp
SPEC +409; mã #275 = 2 tệp +368; PLAT-X8 land #248 = 2 tệp +328. Mọi slice `git diff --numstat` trước review; vượt
ước thì dừng, không mở PR chồng lấn.

## `ngoai_pham_vi`

| thứ | vì sao KHÔNG làm ở đây |
|---|---|
| Policy closure §5 / bốn trường phái sinh §3.2 | nợ #473; Q3 chọn tường minh tập khai báo + symlink; nghĩa vụ **điền** trường phái sinh cho packet này trước `ready` không được miễn ngầm |
| Fencing máy heartbeat/push/handoff/land; `land-packets` đọc sổ | Q11; nợ `LAND-DOC-SO-THU-HOI` |
| Sửa `ops-publish-lease.yml` | cổng tiếp nhận là workflow riêng (N3); giữ vòng đăng lease nguyên |
| Xoá nhánh `ops/cap-lease-461`, `ops/lease-wp461-g2` | thao tác phá; với sổ thì không cần xoá để hội tụ — A1 đo |
| Nâng `timeout-minutes` trong `ci.yml` | cấm cứng; hình dạng đã hỏng 3 lần |
| Sửa `CHANGELOG.md` | trong `RELEASE_MANIFEST.json`; việc của đợt phát hành |
| Chữ ký `web-flow` | 403; chặn oan push thẳng |
| Di trú #456 | đã hết hạn (đo) |
| Ruleset/branch protection ngoài kho | Q10 đo; spec không tự tạo |

## `muc_tieu`

| # | mục tiêu | slice · đường dẫn |
|---|---|---|
| **M1** | Lược đồ + parser bản ghi; nạp sổ từ cây canonical theo OID; ba trạng thái; hằng `KHO_CANONICAL`, `SO_THU_HOI_KICH_HOAT` | A0 · `ops/lease_publish.py` |
| **M2** | `ai-dang-giu`: snapshot Q4 (danh tính, map trước, symref, (tên, SHA40), OID ghim), áp sổ theo `lease_id`, `MAP_REF`, `--nhanh-mac-dinh`; khi `SO_THU_HOI_KICH_HOAT = False` mà `ops/thu-hoi/` canonical không rỗng ⇒ 12 | A0 · `ops/lease_publish.py` |
| **M3** | `check`: precedence Q3/Q6, chiều ngược, độc quyền mọi lease trên tập khai báo + symlink, CLI đòi đã publish (12), hàm thuần tách riêng | A0 · `ops/lease_publish.py` |
| **M4** | `kiem-thu-hoi-github <T-sha40> --canonical-base <S-sha40> --nhanh-mac-dinh <tên>`: map path→(mode, type, blob) append-only; M1 toàn namespace T; readback Q2 mọi bản ghi mới; receipt S/T | A0 · `ops/lease_publish.py` |
| **M5** | Bản ghi thu hồi r2 | C · `ops/thu-hoi/…yaml` |
| **M6** | Ca + đột biến A1–A9, A11–A12; cổng bootstrap (A0) | A0/A1 · `ops/lease_publish_test.py` |
| **M7** | Guard 5 cửa với `target_lease_id`, cùng routine Q4, ba trạng thái, `stale` + history idempotent, `--root` | B · `.claude/dev/packet_loop.py` |
| **M8** | A10 | B · `.claude/dev/packet_loop_test.py` |
| **M9** | Workflow **mới** `ops-thu-hoi-admission.yml`: `pull_request_target` (types opened/reopened/synchronize/ready_for_review) vào nhánh mặc định + `workflow_dispatch`; `permissions: contents: read, issues: write`; checkout **base** (mã canonical, như `duyet-khac-danh-tinh.yml`), `git fetch origin refs/pull/<n>/head` để có T; chạy `kiem-thu-hoi-github <T> --canonical-base <base.sha>` từ mã base; delta sổ rỗng ⇒ 0 có receipt; đăng receipt; `actionlint` xanh. Kích hoạt: bật `SO_THU_HOI_KICH_HOAT`, ghim `BIA_MO_LICH_SU` | A1 |

### Lược đồ bản ghi (M1) — hợp đồng parser

```yaml
schema_version: 1                     # integer đúng 1, KHÔNG bool
event: lease_revoked                  # literal
lease_id: <X>                         # khớp LEASE_ID, == tên tệp không đuôi
packet_issue: 461                     # integer dương, không bool
thu_hoi_boi: ducthangho               # provider ⇒ rc=4; ngoài NGUOI_CO_THAM_QUYEN ⇒ rc=4
thu_hoi_luc_utc: '2026-09-07T13:41:32Z'   # CHUỖI (quote) ISO8601 Z; không ở tương lai so clock snapshot
ly_do: >-                              # chuỗi không rỗng
can_cu: https://github.com/ducthangho/tra-luat/issues/461#issuecomment-<ID>   # Issue comment, cùng KHO_CANONICAL
cap_lai_cho: <Y> | null               # vắng/null/rỗng = không đặt đích; có thì hợp lệ LEASE_ID và ≠ X
blob_da_biet_luc_ghi: [<sha40>, …]    # tuỳ chọn, CHỈ đối chiếu; cổng KHÔNG dùng
```

Root là mapping; **khoá trùng cấm**; chỉ regular blob (mode `100644`) tại đúng `ops/thu-hoi/<lease_id>.yaml` (không
symlink/submodule/thư mục con); đường thoát cây / đồng tự / chuỗi thoát bị từ chối TRƯỚC khi truy cập (ca do điều
phối dựng). Khoá thừa / sai kiểu / sai giá trị ⇒ `rc=8`; YAML hỏng / khoá trùng / tên tệp ≠ ID / nguồn không đọc được
⇒ `rc=12`; tài khoản không được phép ⇒ `rc=4`. Thứ tự: nguồn/object → cấu trúc/ID → thẩm quyền → trường còn lại.
Không truthiness cho bool. packet_loop ánh xạ mọi lỗi sang `RC_STATE` kèm chẩn đoán gốc. Validate một lần, dùng chung.

**Append-only cưỡng chế ở ỨNG VIÊN (M4/A8):** S = canonical base đã xác minh, T = **exact cây sẽ nhận**. Map
**path → (mode, type, blob OID)**: mọi entry tại S nguyên vẹn ở T (sửa/xoá/đổi tên/đổi mode/type ⇒ 8); kiểm M1 trên
**toàn namespace** `ops/thu-hoi/` của T (entry mới không đúng regular/schema không được bỏ qua); phần thêm qua Q2.
S không là tổ tiên T / shallow / object thiếu ⇒ 12. **S ở cha thứ hai tự nó không phải lỗi**: cây giữ nguyên entry cũ
⇒ 0, cây bỏ/sửa ⇒ 8. Không dùng `git log --diff-filter`. Chạy trước mọi cập nhật canonical (kể cả commit chỉ sửa đường
khác ⇒ 0 có receipt); S/T đổi ⇒ receipt stale.

## `nghiem_thu`

Mỗi tiêu chí nêu phép đo làm nó **ĐỎ** (L3). Kho giả = bare + working copy trong thư mục tạm, bare có `HEAD` symref
hợp lệ; danh tính kho và danh sách lịch sử tiêm qua API nội bộ của test; clock cố định.

**A1 — áp toàn ID, đơn vị = cặp.** X có **3 blob** cùng path trên ≥4 ref, một blob ngoài `blob_da_biet_luc_ghi`; X, Y
còn hạn (clock cố định), cùng `p`. Trước: holder {X, Y}; sau bản ghi X vào canonical (sổ đã kích hoạt): holder {Y},
đúng **3** dòng `CÒN_HẠN · ĐÃ_THU_HỒI`, `MAP_REF` phủ đủ ref. ĐỎ khi: bỏ nạp sổ; áp theo `blob_da_biet_luc_ghi` (blob
thứ 3 sống); bỏ dòng in. Ca hết hạn: `HẾT_HẠN · ĐÃ_THU_HỒI`. **Smoke kho thật** (sau C): in tập cặp/ref đo lúc chạy
(hôm nay r2 = **2** cặp) và `NGƯỜI_GIỮ 1: …1g2…`; land không giết lease; smoke không thay fixture.

**A2 — nguồn không thẩm quyền.** Cùng blob X trên 3 ref ⇒ **1** dòng/cặp, `MAP_REF` 3 ref. Sổ chỉ ở feature ref ⇒ holder
có X; vào canonical ⇒ không. Symref cục bộ trỏ feature ⇒ không đổi (máy chủ quyết); máy chủ mặc định `main` mà
`master` còn ⇒ đọc `main`; symref máy chủ vắng/hỏng ⇒ 12. **Kho khác có đủ heads/SHA/symref nhưng sai danh tính ⇒ 12**
(N1). ĐỎ khi: nạp sổ từ mọi ref; đọc symref cục bộ; fallback `master`; gỡ kiểm danh tính.

**A3 — precedence.** Y khai `thay_the_cho: [X]`: (a) không sổ/không lịch sử ⇒ 8; (b) sổ X đích trống ⇒ 0; (c) sổ X đích
Z≠Y ⇒ 8 **kể cả** có bia mộ X→Y; (d) cặp lịch sử (tiêm) ⇒ 0 **dù** còn blob X chưa bia mộ trên ref khác; (e) cặp chỉ
trên feature / bia mộ **sau mốc** ⇒ 8, thông điệp có `ops/thu-hoi/`. ĐỎ khi: `any` mọi ref; bỏ so `cap_lai_cho`; OR
fallback khi sổ từ chối; bỏ áp toàn ID; danh sách lịch sử tự mở rộng từ cây ứng viên.

**A4 — chiều ngược.** Y bị thu hồi bởi sổ ⇒ 8 + `ĐÃ_THU_HỒI`; Y chết theo lịch sử ⇒ 8; có/không `thay_the_cho`; đối
chứng Y sống ⇒ 0. ĐỎ khi: bỏ riêng từng nguồn trong hàm trạng thái chung.

**A5 — giao tập, không tự nhận nguyên tử.** X đã thu hồi, Y xin `p`, W (≠X, không thay thế) giữ `p` ⇒ **11** kèm W/p;
W thu hồi ⇒ 0. Chạy Y có/không `thay_the_cho` (cả hai ⇒ 11), exact/exact, exact∈prefix, prefix∩prefix, case-fold, NFC,
**alias symlink trong cây trỏ cùng tệp ⇒ 11** (N5), `effective_write_set` có thì dùng nó; tập `CÒN_HẠN` không đọc
được ⇒ 12. **Hàm thuần**: hai ứng viên trước publish có thể 0/0 (ghi làm giới hạn); **CLI** `check` trước publish ⇒
**12**; sau publish đồng thời Y/Z ⇒ mỗi bên 11. ĐỎ khi: bỏ từng bước chuẩn hoá/giải symlink; thu hẹp về "chỉ khi thay
thế"; CLI chỉ kiểm ID mà không kiểm đúng (blob, path) trên máy chủ.

**A6 — danh tính, (tên, SHA), OID ghim, chi phí.** Remote-tracking `b` cùng tên SHA cũ ⇒ 12 nêu `b` + hai SHA40; local
head không bù. Đổi `refs/remotes/origin/<mặc định>` SAU phép so ⇒ kết quả không đổi (OID đã ghim); **chụp lại map sau
so rồi ghim** ⇒ phải bị ca riêng bắt (N2); object thiếu sau so ⇒ 12. ĐỎ khi: so chỉ tên; đọc lại theo tên; recapture.
Chi phí: cũ/mới xen kẽ 3 lượt cùng kho/ref/clock, trung vị, tỷ lệ ≤ **2**, ghi raw giây/byte/lệnh.

**A7 — schema và ba trạng thái.** Mỗi ràng buộc M1 một fixture sai **đúng một** trường + đối chứng: YAML hỏng 12 · tên
≠ ID 12 · `thu_hoi_boi: codex` 4 · `ai-codex-bot` 4 · symref máy chủ vắng 12 · sai danh tính kho 12 · khoá thừa 8 ·
thời gian tương lai 8 · `schema_version: true` 8 · khoá trùng 12 · `cap_lai_cho: X` 8 · sổ rỗng ⇒ 0 bản ghi · `git`
rc≠0 12 · blob thiếu 12 · entry mode `120000` 12 · **sổ có bản ghi nhưng `SO_THU_HOI_KICH_HOAT = False` ⇒ 12**. Chạy qua
các consumer. ĐỎ khi: `raise`→`continue` (so verdict thật, có thể 0 hoặc 11); nới `NGUOI_CO_THAM_QUYEN` chứa
`ai-codex-bot` ⇒ ca allowlist ĐỎ.

**A8 — append-only đo cây ứng viên.** S có X; T thêm Y ⇒ 0. T sửa/xoá/đổi tên X, **đổi mode cùng blob**, đổi type,
`merge -s ours` bỏ X ⇒ 8. **Hai ca riêng** S ở cha thứ hai: giữ X ⇒ 0; mất X ⇒ 8 (N9). Sửa bản nháp trước tiếp nhận
đầu ⇒ 0 nếu cây cuối hợp lệ. Commit chỉ sửa đường khác ⇒ 0 có receipt. Mất S/object ⇒ 12. Đơn vị: map path→(mode,
type, blob) + rc. Kho giả/bare hỏi `git rev-parse`, không hỏi thư mục `.git`. ĐỎ khi: chỉ quét canonical; `git log`
path-limited; chỉ validate phần thêm (đổi mode entry cũ lọt).

**A9 — thẩm quyền trước hiệu lực.** Đồ giả API GIỮ TRẠNG THÁI, trace endpoint/ID/số lời gọi: đúng comment/account/khối ⇒
0 + receipt; account lạ (kể cả bot/collaborator) ⇒ 4; chỉ nhắc ID / phủ định / `X-extra` / sai Issue / sai repo / khối
trùng / lệch một trường / **float / khoá JSON trùng / thiếu-thừa khoá / object không phải Issue comment** ⇒ 8; 404 / 500 /
timeout / JSON hỏng ⇒ 12. Bản ghi **không** kèm lease mới ⇒ vẫn qua cổng (≥1 lời gọi; bỏ wiring ⇒ 0 ⇒ ĐỎ); lease mới
có comment (`rc=9`) ⇒ cổng vẫn chạy. Object đổi **SAU canonical** ⇒ X không sống lại và `kiem-github` của Y **không**
đọc lại (0, không 12); đổi **TRƯỚC** ⇒ lần M4 mới readback, receipt cũ stale. ĐỎ khi: bỏ so account/nội dung/repo/Issue.

**A10 — mọi cửa packet_loop.** State thật do `init` tạo. 5 cửa × {sống, thu hồi, không đo được, sổ ở ref khác}:
sống ⇒ qua (`record-lease` ⇒ `leased`); thu hồi ⇒ `RC_STATE`, `stale`, **một** event đúng ID (ở `record-lease`: ID ứng
viên, không ghi `record_lease`); gọi lại ⇒ không thêm event/tiêu lượt/comment; không đo được (`ls-remote` hỏng, blob
thiếu, YAML/schema, clock) ⇒ `RC_STATE` + `KHÔNG ĐO ĐƯỢC`, state byte-match; root ≠ cwd / state-dir ngoài root vẫn
đúng kho. ĐỎ khi: guard chỉ trong `_kiem_luoc_do_lease` (3 cửa ⇒ `accepted`); lấy ID từ state cũ ở `record-lease`
(sống ⇒ 8 hoặc thu hồi không stale); bỏ lưu state; boolean tồn tại.

**A11 — nền và wiring.** Hai vế (base · candidate) trong **MỘT** lệnh, cùng môi trường; tập ca passed/failed/skipped/
not_run + delta **theo tên**. Nền: `lease_publish` 121/121 (wrapper actionlint; 120/121 khi thiếu — không gọi N/N),
`packet_loop` 278/278 + 81 mutant. **A0**: cổng bootstrap chạy ở `ci.yml` (`chay_lease_publish_test.sh`): `ops/thu-hoi/`
rỗng trên canonical **và** HEAD ⇒ xanh; thêm một bản ghi ⇒ ĐỎ. **A1**: `actionlint` + `shellcheck` rc=0; ma trận wiring
trích thân bước từ YAML (kiểu `t32`): S chưa có lệnh/T có (không dùng mã T tự chứng thực) ⇒ 12; S = A0 đã canonical ⇒
chạy; PR thường / integration / chỉ sửa đường khác / `author.name` bot / `rc=9` / bản ghi độc lập ⇒ **đều** có lượt
tiếp nhận; check skipped/not-created/sai SHA ⇒ không pass. `doc-claims-check --strict` rc=0 + `ok:true`;
`doctrine-scan --path` kèm SPEC ⇒ 0.

**A12 — biên nhận bằng chứng dương.** Mỗi suite: lệnh, exact SHA/tree, rc thật, output byte, N/N, registered/executed/
passed/failed/skipped/not_run. Rỗng / thiếu ca đã đăng ký / chỉ banner ⇒ chưa đo. Đột biến runner không gọi suite /
summary rỗng / bỏ một ca ⇒ kiểm biên nhận ĐỎ. Ca lớp sandbox cấm khai `not_run`, điều phối dựng.

## `hinh_dang_ke_thua` (L4)

| hình dạng | số lần | nguồn |
|---|---|---|
| "thu hồi là dữ liệu ghi vào bản sao, không đuổi kịp bản sao" | **2** (wp461-r2 · #456) | §1 |
| "lời khai hội tụ rộng hơn phép đo" | **3** (`3c4c587`, `ddb3200`, r1 spec: "không tồn tại cửa sổ hai lease") | g2, verdict lượt 1 |
| "hai cổng bất đồng về cùng hồ sơ" | **1** | #473 |
| **"nguồn được tin mà chưa xác minh danh tính"** (r1: symref cục bộ · r2: `origin` bất kỳ) | **2** | verdict lượt 1 (default-ref), lượt 2 (N1) |

Hình dạng thứ hai chạm **3**; hình dạng thứ tư chạm **2** trong hai lượt liên tiếp ⇒ r3 ghim danh tính vào **mã**,
không vào bất kỳ thứ gì cấu hình được ở runtime. Lần thứ ba ⇒ hỏi lại thiết kế, không vá.

## `chua_do_duoc`

1. **Ranh giới chủ kho / agent-cầm-PAT** — không đo được trong tài khoản (Q2). Chỉ hứa "tài khoản chủ kho".
2. **Chữ ký `web-flow`** — 403; ngoài hợp đồng.
3. **Kích thước** — ước theo slice, chưa có diff; `numstat` từng slice trước review.
4. **Required check / branch protection / bypass / direct push** cho M9 — ngoài kho; **chưa đo**. Chưa đo ⇒
   `SO_THU_HOI_KICH_HOAT` giữ `False` (Q10). Đường đã biết: "push được vào `ops/**` thì đăng được".
5. **`actions/checkout` + `refs/pull/<n>/head` trong `pull_request_target`** nạp đủ heads cho snapshot Q4? — đo ở A1
   bằng chính workflow (so tên/OID/default, không đếm); thiếu ⇒ thêm `git fetch origin '+refs/heads/*:refs/remotes/origin/*'`
   trong write set A1. Đây là nghiệm thu A1, không phải điều kiện cần mã mới trước lease A0.
6. **Không có chế độ đệm offline cho packet_loop** — quyết định (Q5.1); hệ quả: executor không mạng không mở lượt.
7. **Object Q8** — chưa tồn tại.
8. **Nguyên nhân `Connection refused (os error 111)` của codex** — chưa gặp ở hai lượt (1842,8 s và lượt 2).
9. **Mốc A0 và danh sách `BIA_MO_LICH_SU`** — chỉ tính được lúc A0 land; delta người giữ đo lúc kích hoạt (A1).

## 4. Câu chủ kho phải chốt khi cấp lease (mỗi câu có khuyến nghị)

❓ **Q7 — packaging/ngoại lệ ADR-0044.** ➡️ **A0 → A1 → B → C**, mỗi slice spec/Issue/lease riêng, base đã nhận slice
trước (§5/ADR-0044); mã mà workflow neo phải **có thật trên canonical** trước A1 (N4). A0 cần ngoại lệ dòng có phạm vi;
không cắt test. A0 hữu ích như phép đo ngay khi land nhưng **không** tự đủ; kích hoạt ở A1 sau Q10.
❓ **Q8 — object cấp lệnh thu hồi r2.** ➡️ Chủ kho đăng lên **#461** một Issue comment chứa đúng khối
`lease_revocation_authorization` cho `wp461-…-exec-1r2-claude-20260907`, `cap_lai_cho: wp461-…-1g2…`. Bản chiếu bot và
PR #474 chỉ là tài liệu tham khảo; comment cùng tài khoản không nói human hay agent.
❓ **Q9 — nhận bản ghi cho lease đã hết hạn?** ➡️ Nhận; in `HẾT_HẠN · ĐÃ_THU_HỒI`; không gỡ event, không tái dùng ID.
Lựa chọn sản phẩm, không phải luật.
❓ **Q10 — kích hoạt sổ.** ➡️ Điều kiện bắt buộc, đo bằng facts ngoài kho: (a) `ops-thu-hoi-admission.yml` là **required
check** trên nhánh mặc định, neo đúng repo/S/T, không pass khi skipped/not-created/sai SHA; (b) ruleset chặn direct
push/bypass cho `ops/thu-hoi/**` (hoặc khai thẳng chưa có); (c) A0 đã canonical, A1 chạy wiring thật với mã A0; (d) delta
người giữ cũ/mới = 0 (Q6). Thiếu ⇒ `SO_THU_HOI_KICH_HOAT = False`, không phải "chưa ghi M5".
❓ **Q11 — gỡ quyền worker cũ, cho worker mới bắt đầu.** ➡️ Tuần tự có thẩm quyền: (1) bản ghi thu hồi land qua M9;
(2) chủ kho xác nhận worker cũ đã dừng + giữ last SHA/state/journal (ADR-0028); (3) lease mới `check` trên ảnh chụp
mới, land, readback `NGƯỜI_GIỮ 1`; (4) mới cho bắt đầu. KHÔNG chọn "`check rc=0` là khoá".
❓ **Q12 — ready của từng slice.** ➡️ Issue + `spec_hash` bản được duyệt + revision; closure/policy SHA/checks/land
obligations do bên điều phối điền (không kế thừa miễn trừ `b416830`); base đã nhận slice trước; hợp đồng danh tính
nguồn/target ID/bootstrap đóng trước ready A0. Bằng chứng wiring thật là nghiệm thu A1, không phải điều kiện cần trước
lease A0. Thiếu hợp đồng ⇒ `proposed`; thiếu facts runtime ⇒ sổ chưa kích hoạt.
