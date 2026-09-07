# ĐẶC TẢ PACKET — `THU-HOI-LEASE-VA-CAP-LAI`, **revision 2**

```yaml
packet_id: THU-HOI-LEASE-VA-CAP-LAI
packet_issue: CHƯA CÓ          # điền khi đăng Packet Issue (Bước 3); spec đóng băng TRƯỚC Issue
revision: 2
thay_the: 43844cb2ea2653f502320a6f35a6e3ae7fd182770f02b62d4d73b9aa8dbea6f9   # sha256 bản r1 đã được review
review_class: sensitive        # chạm ops/lease_publish.py + .claude/dev/packet_loop.py + .github/workflows/ — §8, fail-closed
executor: claude
reviewer: codex
assurance_target: cross_approved
base_sha: b416830ef2a509d60203d55552ce17950afcf67c   # origin/master lúc đóng băng
```

**Mọi con số đo lúc `13:2x–14:2xZ 07-09-2026` trên `303` ref** (302 tên nhánh máy chủ + 1 nhánh cục bộ
`master`; `git ls-remote --heads origin` so `git for-each-ref refs/remotes/origin` bằng TẬP TÊN: `comm -23` =
**0**, `comm -13` = **0**), reviewer lượt 1 đo lại trên mirror lúc `13:52:30Z` và **khớp** trừ các chỗ ghi
"đính chính" bên dưới. **Đo lại trước mỗi bước công bố** (L5). Đơn vị (L1): "cặp" = **(blob, đường dẫn) duy
nhất** trên mọi ref — `ai-dang-giu` in **một dòng cho mỗi cặp**, KHÔNG phải mỗi ref; "lease_id" = giá trị trường
`lease_id`; "ref" = một dòng của `git for-each-ref refs/heads refs/remotes` trừ `*/HEAD`.

## 0. Delta so revision 1 — cross-review lượt 1 (codex `gpt-6-astra`, effort high, 1842,8 s)

Verdict `changes_requested`, **11 P1 + 3 P2**, sha256 `b60a755f611bf814e0c9116e1cb5c9c4f9cb5ac3f1a6e96a951cd3dc7f17123e`;
19 phản chứng chạy được trên Git thật + mô phỏng luật mới (`scratch/adversarial.py`). Từng finding và cách r2 xử:

| finding (P) | r1 sai ở đâu | r2 làm gì |
|---|---|---|
| `authority-signature-evidence-false` (P1) | khai `6635379` "không chữ ký" — **SAI**, `cat-file -p` có `gpgsig -----BEGIN SSH SIGNATURE-----` | bảng Q2 sửa; tách "raw git" khỏi "login API"; không suy human/agent từ bất kỳ object nào |
| `default-ref-is-untrusted-cache` (P1) | tin `refs/remotes/origin/HEAD` cục bộ, vắng thì thử `master` — reviewer đổi symref cục bộ trỏ nhánh giả ⇒ sổ giả có hiệu lực | Q4: nhánh mặc định lấy từ **máy chủ** (`ls-remote --symref`), cache phải khớp, KHÔNG fallback tên |
| `standalone-revocation-has-no-admission-gate` (P1) | bản ghi thu hồi không kèm lease mới thì **0** lời gọi online trước hiệu lực; workflow không bắn cho `ops/thu-hoi/` | M9: workflow là **cổng tiếp nhận**, vào write set (tệp thứ 6); Q10 |
| `evidence-mention-is-not-an-authorization` (P1) | `can_cu` chỉ đòi "thân chứa lease_id" — `Do not revoke X` cũng qua | Q2: khối lệnh JSON có schema, so **bằng nhau**, cùng repo/Issue, readback băm thân |
| `write-set-exclusion-is-incomplete` (P1) | chỉ đo độc quyền khi có `thay_the_cho`; `_lease_cham_duong` so chuỗi bằng nhau, lọt prefix/case-fold | M3: đo giao cho **MỌI** lease theo §5 (NFC, case-fold, exact/prefix); A5 đổi ca không-thay-thế từ 0 thành 11 |
| `snapshot-check-does-not-fence-writers` (P1) | khai "không tồn tại cửa sổ hai lease ĐĂNG ĐƯỢC" — hai clone `check` trước publish cùng 0 | Q3/Q5: `rc=0` là **ảnh chụp**; cấp → readback → cho bắt đầu do MỘT bên điều phối tuần tự hoá; Q11 |
| `reads-are-not-pinned-to-one-snapshot` (P1) | so SHA một lần rồi đọc theo TÊN ref — đổi ref giữa chừng thì trộn hai cây | Q4: ghim OID từng ref, mọi `ls-tree`/`cat-file` theo OID |
| `legacy-fallback-conflicts-with-ledger` (P1) | vế OR bia mộ vượt được `cap_lai_cho`; A3(d) hứa 0 mà luật theo-blob cho 11; "5 cặp bia mộ trên master" sai (thật: **7** tệp, gate/mutant nằm ở #468) | Q6: sổ ưu tiên tuyệt đối; bia mộ lịch sử = danh sách đóng neo canonical, áp theo lease_id |
| `append-only-check-misses-candidate-and-merges` (P1) | `git log --diff-filter=MD` ra 7 dòng cho một sửa, và **0** dòng khi `merge -s ours` xoá sổ | A8: so **map đường→blob** ứng viên với canonical, chạy TRƯỚC merge |
| `packet-loop-guard-is-partial-and-boolean` (P1) | chỉ `record-lease`/`begin-attempt` gọi helper; `record-post`/`transition`/`record-review` = **0/0/0** lời gọi; boolean tồn tại coi "không đọc được" là "không có" | M7: guard chung ở **5** cửa, ba trạng thái |
| `acceptance-confuses-refs-blobs-and-mutations` (P1) | A1 đòi ≥4 dòng trong khi r2 chỉ có **2 cặp**; mutant theo blob-đã-biết sống vì cả 2 blob đều trong `blob_da_biet_luc_ghi` | A1/A2 đếm cặp + map cặp→ref; fixture 3 blob, 1 blob ngoài danh sách; clock cố định |
| `revocation-schema-and-error-contract-incomplete` (P2) | thiếu kiểu/khoá trùng/thứ tự lỗi | M1: hợp đồng parser đầy đủ |
| `size-estimate-and-slice-anchor-are-stale` (P2) | mốc #250 sai (là +409 SPEC, mã land #275 +368); PLAT-X8 cuối +328; #468 = **31** commit | §write_set ước lại từng module; Q7 |
| `ready-and-rollout-decisions-are-not-closed` (P2) | thiếu Q10–Q12 | §4 thêm ba câu |

Con số reviewer đo mà r1 không có: launcher `ai-dang-giu` 3 lượt **3,596 / 3,285 / 3,359 s** (trung vị 3,359 s)
trên mirror — r1 ghi 4,1 s trên kho nguồn; hai môi trường, không phải hồi quy. `packet_loop_test` **278/278 +
81 mutant**, output 8752 B. `lease_publish_test` 120/121 (t33 thiếu actionlint) output 9027 B; với wrapper cài
actionlint: **121/121**, 8726 B (đo phía điều phối).

## `nguon_cap_viec`

- Lệnh chủ kho lập phiên này (`session_01Vt7NfNpABHfSWpxvx4aJGE`, 07-09-2026): *"bổ sung cơ chế CHỦ KHO THU
  HỒI LEASE và CẤP LẠI CHO MỘT PR KHÁC"*. Câu chat KHÔNG phải neo; neo là Packet Issue ở Bước 3.
- Nợ `AG-T0-01B-thu-hoi-lease-chua-co-duong` (`ops/specs/ag-t0-01b-r4.md` §0.2; `CLAUDE.md` mục *"LEASE KHÔNG TỰ
  CHẾT KHI PACKET ĐÃ LAND"*).
- Nợ #473: `bia-mo-check-bo-sot-chieu-nguoc`, `cong-check-thieu-do-phu-tham-quyen` — packet này đóng phần
  "bia mộ theo từng blob" và phần "độc quyền write set"; phần "bốn trường phái sinh" KHÔNG.
- Lease g2 `wp461-…-exec-1g2-claude-20260907` (PR #474), khoá `hoi_tu_nguoi_giu_doi_thao_tac.no_nen`.

## 1. Vấn đề — ĐÃ ĐO, reviewer đã đo lại

Thu hồi hôm nay chỉ có bia mộ hai chiều (`thay_the_cho` ↔ `da_bi_thay_the`), ép bởi
`ops/lease_publish.py::_kiem_bia_mo` (595–617). Bia mộ là **dữ liệu ghi vào TỆP CŨ**, mà tệp cũ có bản sao trên
nhiều ref:

| phép đo | giá trị | reviewer |
|---|---|---|
| ref quét | **303** | khớp |
| cặp (blob, path) trong `ops/leases/` · đường dẫn · lease_id | **288 · 273 · 273** | khớp |
| lease_id có >1 blob | **7 / 273** (số blob: 2,2,4,4,5,3,2) | khớp |
| lease_id `CÒN_HẠN` | **8** | khớp (13:41Z và 13:52Z) |
| trong đó CHƯA bia mộ trên ≥1 ref | **4**: `gate-tach-…-1r4` (1 ref, #468) · `mutant-…-exec-1` #456 (**11** ref; bia mộ trên 1 ref = #468) · `wp461-…-1g2` (1 ref) · `wp461-…-1r2` (**4** ref; bia mộ trên 1 ref) | khớp |
| r2: cặp (blob, path) | **2** cặp — `26f07b4` (0 bia mộ, 4 ref: `heads/master` · `origin/master` · `origin/ops/cap-lease-461` · `origin/claude/soan-spec-3-viec-treo-20260906`) và `fdfde3a` (bia mộ, 1 ref: `origin/ops/lease-wp461-g2`) | khớp — **r1 viết "≥4 dòng" là SAI đơn vị** |
| tệp mang `da_bi_thay_the` trên `origin/master` | **7** (`ci-cai-jsonschema` ×2 · `khong-do-duoc-phai-do` · `lease-hoi-toan-kho` ×3 · `wp461-…-exec-1`); chỉ `wp461-…-exec-1` `CÒN_HẠN` (hết `2026-09-08T03:05:00Z`) | đính chính r1 |
| tệp mang `da_bi_thay_the` trên #468 | **11** (7 trên + 3 `gate-tach` + `mutant`) | đính chính r1 |
| commit riêng của #468 so master | **31** (`rev-list --left-right --count` ⇒ `0 31`) | đính chính r1 (28) |
| `ai-dang-giu` cả 4 đường wp461 | `NGƯỜI_GIỮ 2`, rc=11 | khớp |
| `check` lease g2 | rc=0 `ĐĂNG ĐƯỢC` — trong khi người giữ là 2 | khớp |

Ba hệ quả, mỗi hệ quả có dòng mã: (1) `_kiem_bia_mo` dùng `any(...)` (606–610): một bản sao có bia mộ trên
bất kỳ ref nào là đủ ⇒ hai cổng bất đồng; (2) `kiem()` (787–890) gọi `_lease_cham_duong` **0** lần ⇒ `check` không
đo độc quyền; (3) bia mộ nằm trên nhánh `ops/**` — merge xong thì nhánh đã rẽ trước đó (#468) vẫn mang bản
chưa bia mộ; số ref mang bản sống **tăng** theo thời gian (PR #475 của chính spec này là ref thứ 5 mang `26f07b4`).

**Bất biến đúc kết:** *cấp ở bất kỳ ref nào chỉ THÊM người giữ (chiều an toàn); thu hồi phải ở đúng MỘT chỗ mọi
phép đo đọc, và chỗ ấy phải có cổng tiếp nhận TRƯỚC khi có hiệu lực.* Hôm nay chỗ ấy không tồn tại.

## 2. Sáu câu hỏi — trả lời kèm phép đo

### Q1 — Chủ kho phát lệnh thu hồi ở ĐÂU để có hiệu lực trên mọi ref?

➡️ **Sổ thu hồi append-only `ops/thu-hoi/<lease_id>.yaml`** trên nhánh mặc định (charset `LEASE_ID` =
`^[A-Za-z0-9._-]+$`, an toàn làm tên tệp). **Hiệu lực = bản ghi hợp lệ (M1) + đã qua cổng tiếp nhận (M9, Q2) + có
mặt trong cây canonical tại OID đã chụp (Q4).** Bản ghi ở ref khác = CHƯA thu hồi. Tên nhánh mặc định là thứ
**máy chủ khai** (Q4), không phải symref cục bộ, không phải tên `master` thử vào.

| phương án đã cân nhắc | vì sao loại |
|---|---|
| Sửa tệp lease cũ trên MỌI ref | phải đẩy vào nhánh người khác (#468: 31 commit riêng); phiên web không xoá/force ref; là chính lỗi hiện nay |
| Bia mộ trong cùng nhánh `ops/**` với lease mới | `NGƯỜI_GIỮ 2` là phép đo của phương án này |
| Chỉ comment Issue làm sổ | online-only; `ai-dang-giu` cố ý offline fail-close; comment là hiện vật sửa được (`kiem()` khối 795–812) |
| `git notes` / `refs/thu-hoi/*` | không fetch mặc định, không qua PR, không diff trong review |
| `ops/leases/thu-hoi/` | `_quet_lease_toan_kho` `ls-tree -r ops/leases` sẽ đọc bản ghi như LEASE ⇒ rc=12; workflow lọc `ops/leases/**.yaml` sẽ cố ĐĂNG nó |

### Q2 — Danh tính chủ kho và LỆNH thu hồi

Bằng chứng Git tại `b416830`, đã đo lại (đính chính r1):

| object | dữ liệu Git đọc được | giới hạn |
|---|---|---|
| `b416830` (merge PR #471) | author `ducthangho`, committer `GitHub <noreply@github.com>`, **một chữ ký PGP**; `%G?=E` với keyring rỗng | không chứng minh ai bấm nút; Git không lưu `author.login` |
| `6635379` (lease r2, phiên agent đẩy) | author/committer `Claude <noreply@anthropic.com>`, **một chữ ký SSH** (r1 khai "không chữ ký" — SAI) | có chữ ký ≠ đã xác minh người ký |
| API: actor 5 lượt `ops-publish-lease` 372–376 = `ducthangho`; `author.login` của `6635379` = `claude` | đo qua MCP phía điều phối, reviewer **không readback được** (offline) | dữ liệu API, không phải Git |

Kết luận **không đổi và đã được chính `b416830` thừa nhận**: trong tài khoản chủ kho, **không có ranh giới máy**
tách "chủ kho gõ" khỏi "agent cầm PAT của chủ kho". Spec không bịa ranh giới ấy; chữ ký `web-flow` **không** nằm
trong hợp đồng (Q2 lớp 4 của r1 bỏ: `curl web-flow.gpg` 403; push thẳng của chủ kho không có chữ ký ấy).

➡️ Bản ghi thu hồi dùng **đúng chuẩn thẩm quyền của bản ghi CẤP**, cộng **cổng tiếp nhận bắt buộc TRƯỚC hiệu lực**:

1. `thu_hoi_boi`: chốt provider (`rc=4`) rồi danh sách cho phép `NGUOI_CO_THAM_QUYEN` (`rc=4`) — cùng hai chốt,
   cùng thứ tự với `granted_by`.
2. `can_cu`: **MỘT** URL HTTPS GitHub **cùng repository**, trỏ Issue comment / Issue body / PR review comment.
   Parse thành (loại object, ID số). Readback (`kiem-thu-hoi-github`, online) phải khớp: repository, ID, Issue
   đích == `packet_issue`, `user.login ∈ NGUOI_CO_THAM_QUYEN` (`rc=4` nếu khác — kể cả `github-actions[bot]`,
   kể cả collaborator). Thân object phải chứa **đúng một** khối:

   ```
   ```json lease_revocation_authorization
   {"event":"lease_revoked","lease_id":"<X>","packet_issue":<N>,"cap_lai_cho":"<Y>"|null,
    "thu_hoi_boi":"ducthangho","thu_hoi_luc_utc":"<ISO Z>"}
   ```
   ```

   so **BẰNG NHAU từng trường** với bản ghi (không substring, không prose nhắc tên, `X-extra` không khớp `X`,
   `Do not revoke X` không khớp). Khối thiếu/trùng/lệch ⇒ `rc=8`; object không đọc được / HTTP ≠ 200 / JSON hỏng
   ⇒ `rc=12` (dòng trạng thái HTTP thật, không dò văn bản tự do).
3. Readback lưu **object ID + sha256 thân đã đến** (UTF-8) vào comment tiếp nhận (M9) — "đo thứ đã ĐẾN". Object bị
   sửa/xoá SAU tiếp nhận không hồi sinh lease (event trong Git bất biến); thay đổi TRƯỚC tiếp nhận ⇒ phải kiểm lại.
4. **Hiệu lực chỉ khi trong cây canonical** ⇒ phải merge vào nhánh mặc định — cùng hành vi chủ kho làm với mọi
   lease. Merge là *hành vi*, tệp là *lời khai*, workflow M9 là *cổng đứng giữa*.

Lớp này phân biệt **tài khoản chủ kho** với **tài khoản khác** — toàn bộ thứ GitHub xác thực được. Nói đúng thế.

### Q3 — Lease mới neo vào thu hồi thế nào; `check` bỏ `any(...)` ra sao

Giữ `thay_the_cho: [X, …]` (schema không đổi). Mọi cổng dùng **cùng snapshot Q4** và **cùng bộ tính trạng thái
theo lease_id**. Với từng X, thứ tự bắt buộc:

1. **Có bản ghi sổ cho X** (canonical, hợp lệ M1): `cap_lai_cho` null/rỗng hoặc == `lease_id` mới ⇒ qua; khác ⇒
   `rc=8`, **KHÔNG rơi sang bia mộ**. Sổ ưu tiên tuyệt đối.
2. **Không có bản ghi**: chỉ nhận cặp bia mộ **lịch sử** theo danh sách đóng ở Q6 (trên canonical, hai chiều,
   lease_id == tên tệp). Không có ⇒ `rc=8`, chẩn đoán trỏ `ops/thu-hoi/` và OID canonical.
3. **Chiều ngược**: chính lease đang `check` đã chết (sổ HOẶC cặp lịch sử canonical) ⇒ `rc=8`, kể cả không khai
   `thay_the_cho`.

**Độc quyền write set — cho MỌI lease** (không riêng lease có `thay_the_cho`), theo §5 protocol: chuẩn hoá
separator `/`, từ chối tuyệt đối/`..`/thoát repo, NFC, case-fold, `normpath`; mục kết thúc `/` = prefix, còn lại
exact; `planned:` bỏ nhãn rồi xử như thường. Giao (exact∩exact, exact∈prefix, prefix∩prefix) với bất kỳ lease
`CÒN_HẠN` chưa chết nào khác ⇒ `rc=11` nêu `lease_id` + đường va chạm. Write set của một lease `CÒN_HẠN` **không
đọc được** ⇒ `rc=12`, không coi là rỗng (lease `HẾT_HẠN` không đọc được: in chẩn đoán, không chặn — đo: 3 lease
`plat-x4/x5` 20-08 dùng `planned:` đều đã hết hạn). Không dùng `_lease_cham_duong` (so chuỗi bằng nhau) làm phép giao.

**`check rc=0` là ẢNH CHỤP** — chứng minh các vị từ trên đúng tại OID đã chụp; **không** phải acquire nguyên tử.
Reviewer dựng được: X đã thu hồi, hai clone soạn Y/Z cùng `p`, hai `check` trước publish cùng **0**, push cả hai
⇒ holder **[Y, Z]**. Nên: ứng viên phải **đã có trên ref máy chủ và được quét trong snapshot**; cấp → readback
`ai-dang-giu` → cho phép bắt đầu do **MỘT** bên điều phối (chủ kho) tuần tự hoá; hai ứng viên đã `check` trên
ảnh chụp cũ **không** cùng được bắt đầu. Fencing bằng máy (heartbeat/push/handoff/land) là dependency KHÁC
(Q11) — chưa có thì packet này **chỉ cung cấp phép tính**, không tuyên bố "đã gỡ cửa sổ hai writer".

`thu_hoi_can_cu` trong lease (tuỳ chọn) chỉ để người đọc đối chiếu; cổng không dùng nó bỏ bất kỳ phép kiểm nào.

### Q4 — MỘT snapshot, MỘT phép tính cho mọi bản sao

- **Một lời gọi mạng**: `git ls-remote --symref origin HEAD 'refs/heads/*'` cho **nhánh mặc định máy chủ khai**
  + tập `(tên, SHA40)`. Đo 14:0xZ: trả `ref: refs/heads/master\tHEAD` — còn `refs/remotes/origin/HEAD` cục bộ
  trong clone này **không** phải symref (`fatal: … not a symbolic ref`), tức cache không đủ tin. Workflow truyền
  `--nhanh-mac-dinh "$MAC_DINH"` (từ `github.event.repository.default_branch`) và giá trị ấy **phải bằng** symref
  máy chủ; lệch ⇒ `rc=12`. HEAD máy chủ vắng/mơ hồ ⇒ `rc=12`. **Không fallback tên `master`.**
- So `(tên, SHA40)` máy chủ với `refs/remotes/origin/*`: thiếu/lệch SHA ở bất kỳ nhánh nào ⇒ `rc=12` nêu tên và
  hai SHA. Local `refs/heads/*` không được dùng bù cache thiếu (chốt tụt-sau hiện có giữ nguyên).
- **Ghim OID**: sau đối chiếu, chụp map ref→SHA40 + OID canonical **một lần**; mọi `ls-tree`/`cat-file`/tra sổ/bia
  mộ/write set đọc theo OID, không phân giải lại tên. Đổi ref giữa chừng không trộn hai cây (reviewer đổi
  `refs/remotes/origin/master` sau phép so ⇒ r1 đọc sổ rỗng trong khi scan thấy X). Thiếu object / `git` rc≠0 /
  output hỏng ⇒ `rc=12`; chỉ được kết luận "sổ vắng" khi đã đọc thành công cây chứa nó.
- Nạp sổ một lần từ cây canonical; áp theo `lease_id` cho **MỌI** cặp (blob, path): in `<hạn> · ĐÃ_THU_HỒI`
  (cả `HẾT_HẠN · ĐÃ_THU_HỒI`), không vào tập người giữ, **bất kể blob**. `blob_da_biet_luc_ghi` KHÔNG phải allowlist.
- Đầu ra: một dòng/cặp + `MAP_REF` (cặp → tập ref) khi cần chứng minh đủ ref + `MÙ 0` với số ref đã đo. `check`,
  `ai-dang-giu`, `body`, `kiem-github`, `kiem-thu-hoi-github` dùng **chung** một hàm trạng thái.
- Chi phí: một `ls-remote --symref` thay cho `ls-remote --heads` (0 lời gọi mạng thêm) + đọc sổ + kiểm. A6 đo
  cũ/mới xen kẽ trên cùng kho; không lấy 4,1 s / 3,359 s làm mẫu số cố định.

### Q5 — Việc còn dở của lease bị thu hồi; có mất mát ghi không

`git ls-remote --heads origin 'refs/heads/agent/wp461*'` ⇒ RỖNG (09:49Z, 13:4xZ) — chỉ chứng minh không có ref
khớp mẫu; **không** chứng minh không có worktree bẩn/commit chưa push/tiến trình cũ. Không dùng "Git không mất
commit" thay kiểm kê.

➡️ §4 protocol: worker cũ không heartbeat/push/handoff được; branch/PR → `stale`; generation mới đọc diff cũ,
không tự cherry-pick; retention theo ADR-0028. Ba chỗ, ba mức răng khác nhau — nói đúng từng mức:

1. **Executor cũ, `packet_loop.py` (M7):** guard chung `_kiem_thu_hoi(root, state, snapshot)` nhận **root kho tường
   minh** (state-dir có thể ngoài kho — `--state-dir` mặc định `.claude/.packet_state`), gọi ở **5** cửa:
   `record-lease`, `begin-attempt`, `record-post`, `record-review`, `transition` — TRƯỚC mọi thay đổi (đo: 3 cửa
   sau hiện gọi `_kiem_luoc_do_lease` **0** lần). Ba trạng thái: **thu hồi** ⇒ ghi state `stale` + history
   `lease_revoked_seen{lease_id, oid_canonical, blob_ban_ghi}` (idempotent: không trùng event, không tiêu
   attempt/comment), lưu xong mới `RC_STATE`; **sống** ⇒ tiếp; **không đo được** (không có `refs/remotes/origin/*`,
   sổ hỏng, object thiếu, YAML/schema lỗi, clock) ⇒ `RC_STATE` + `KHÔNG ĐO ĐƯỢC`, **không** sửa state. Lỗi ghi state
   cũng chặn. Giới hạn khai thẳng: packet_loop **không fetch**, chỉ áp được thu hồi có trong đệm đã xác minh; đây
   là giới hạn, **không phải cổng fencing**.
2. **Lease mới (M3):** `check` từ chối khi còn người giữ — trên ảnh chụp (Q3).
3. **Land** — NGOÀI write set, nợ `LAND-DOC-SO-THU-HOI`: `land-packets` phải hỏi sổ trước khi land PR mang
   `lease_id` bị thu hồi. Chưa có ⇒ chưa có răng máy ở tầng land; không gọi nợ là chốt.

Không có thao tác gỡ thu hồi; cấp lại = lease mới, `lease_id` + `generation` mới (ADR-0025).

### Q6 — Bia mộ lịch sử: precedence, danh sách đóng, di trú

➡️ **Sổ thay thế bia mộ cho mọi thu hồi MỚI; bia mộ chỉ còn là LỊCH SỬ có danh sách đóng.**

- **Danh sách đóng** = các cặp `(lease cũ, lease mới)` có bia mộ **hai chiều** hợp lệ (lease_id == tên tệp, cả hai
  tệp) trên canonical `b416830ef2a509d60203d55552ce17950afcf67c`. Đo: **7** tệp mang `da_bi_thay_the` trên
  master (bảng §1); từng cặp phải được kiểm khi executor dựng danh sách — "tệp mang trường" ≠ "cặp hợp lệ".
  Bia mộ trên feature ref (#468: 3 `gate-tach`, `mutant`) **không** phải nguồn thẩm quyền. Sau mốc này, bia mộ
  mới ⇒ `check` `rc=8` trỏ `ops/thu-hoi/`.
- Cặp lịch sử áp theo **lease_id toàn kho** — bản blob chưa bia mộ trên ref cũ cũng chết (nhất quán với sổ;
  r1 giữ theo-blob nên tự mâu thuẫn A3(d)). Vòng/chuỗi kết thúc hữu hạn; lịch sử mâu thuẫn ⇒ `rc=12`.
- **Sổ > lịch sử**: có bản ghi hạn chế `cap_lai_cho` thì không dùng bia mộ vượt hạn chế; chiều ngược chặn cả hai.
- `_bia_mo_doi_xung` và nhãn `ĐÃ_BỊ_THAY_THẾ` giữ để in; **quyết định người giữ** đi qua hàm trạng thái chung.
- **Di trú 4 lease `CÒN_HẠN` chưa bia mộ** (đo 13:41Z; đo lại lúc cấp lease):

| lease_id | tình trạng | việc |
|---|---|---|
| `wp461-…-exec-1r2-claude-20260907` | phải chết; lệnh của chủ kho hiện chỉ ở lease g2 + PR #474 — **chưa có object đạt Q2** (comment `5569885143` do `github-actions[bot]` đăng ⇒ không thuộc allowlist) | **M5** sau khi chủ kho đăng khối lệnh (Q8) |
| `mutant-…-exec-1` (#456) | hạn `2026-09-07T14:30:07Z`; lúc viết r2 (14:2xZ) **CÒN_HẠN** | không di trú; **đo lại `now ≥ 14:30:07Z`** lúc cấp lease, đừng suy từ lịch |
| `wp461-…-exec-1g2` · `gate-tach-…-1r4` (#463) | người giữ hợp lệ | không đụng |

## `write_set`

```
ops/lease_publish.py
ops/lease_publish_test.py
.github/workflows/ops-publish-lease.yml
.claude/dev/packet_loop.py
.claude/dev/packet_loop_test.py
ops/thu-hoi/wp461-be-mat-thu-hai-cua-codex-exec-1r2-claude-20260907.yaml
```

Sáu đường dẫn, không ký tự đại diện. Workflow là **cổng tiếp nhận** (M9), không phải tiện ích comment. Tệp M5 là
dữ liệu, chỉ viết sau khi Q8 có object đạt và Q10 đã đo.

**Kích thước — vượt trần ADR-0044 (`sensitive` ≤ 3 tệp, ≤ 300 dòng thêm) cả hai chiều, khai thẳng.** Mốc neo
đo lại: PR #250 = 2 tệp **SPEC** +409 (r1 ghi nhầm là mã); mã `LEASE-HOI-TOAN-KHO` land ở #275 = 2 tệp **+368**;
`PLAT-X8` land #248 = 2 tệp **+328** (r1 dùng mốc trung gian +313). Ước lại **theo nhóm ca**, chưa có diff:

| module | ước dòng thêm | vì sao |
|---|---|---|
| `ops/lease_publish.py` | 180–260 | snapshot OID + symref (Q4) · hàm trạng thái chung · parser M1 · giao §5 · `kiem-thu-hoi-github` · append-only |
| `ops/lease_publish_test.py` | 300–420 | A1–A9 ≈ 30 ca + đối chứng + đột biến, fixture bare có symref |
| `.github/workflows/ops-publish-lease.yml` | 30–50 | mở `paths`, bước gọi cổng từ canonical, comment tiếp nhận |
| `.claude/dev/packet_loop.py` | 50–80 | guard 5 cửa, ba trạng thái, root tường minh |
| `.claude/dev/packet_loop_test.py` | 80–120 | A10 |
| `ops/thu-hoi/…yaml` | ~15 | dữ liệu |

Tổng ước **655–945**; không có cách chia nào cho MỘT slice ≤300 mà vẫn có răng. Q7 chốt packaging; mọi slice
đều phải `git diff --numstat` trước review, vượt ước thì dừng (ADR-0044), không tự mở PR chồng lấn.

## `ngoai_pham_vi`

| thứ | vì sao KHÔNG làm ở đây |
|---|---|
| Cưỡng chế `generation` / bốn trường phái sinh §3.2 | nợ #473, khác gốc; nhưng nghĩa vụ **điền** chúng cho chính packet này trước `ready` không được miễn ngầm (miễn trừ ở `b416830` chỉ cho wp461 r2 g1) |
| Fencing bằng máy cho heartbeat/push/handoff/land; `land-packets` đọc sổ | Q11; nợ `LAND-DOC-SO-THU-HOI`. Không gọi là đã đóng |
| Xoá nhánh `ops/cap-lease-461`, `ops/lease-wp461-g2` | thao tác phá; với sổ thì **không cần** xoá để hội tụ — đó là điều A1 đo |
| Nâng `timeout-minutes` trong `ci.yml` | cấm cứng; hình dạng đã hỏng 3 lần |
| Sửa `CHANGELOG.md` | trong `RELEASE_MANIFEST.json`; việc của đợt phát hành |
| Chữ ký `web-flow` | không lấy được khoá (403); chặn oan push thẳng của chủ kho |
| Di trú lease #456 | đo hết hạn thật trước; sổ ghi một lease đã chết là nhiễu |
| Ruleset/branch protection ngoài kho | Q10 đo; spec không tự tạo được |

## `muc_tieu`

| # | mục tiêu | đường dẫn |
|---|---|---|
| **M1** | Lược đồ + parser bản ghi thu hồi (hợp đồng đầy đủ bên dưới); nạp sổ từ cây canonical theo OID; ba trạng thái | `ops/lease_publish.py` |
| **M2** | `ai-dang-giu`: snapshot Q4 (symref máy chủ, `(tên, SHA40)`, ghim OID); áp sổ theo `lease_id` lên mọi cặp; `MAP_REF`; `--nhanh-mac-dinh` | `ops/lease_publish.py` |
| **M3** | `check`: precedence Q3/Q6; chiều ngược (sổ + lịch sử); giao write set §5 cho MỌI lease; rc=0 = ảnh chụp | `ops/lease_publish.py` |
| **M4** | `kiem-thu-hoi-github <candidate-sha40> --canonical-base <sha40>`: append-only (A8) + readback `can_cu` (Q2) cho mọi bản ghi mới trong delta; `kiem-github` của lease mới kiểm LẠI (không phải cửa duy nhất) | `ops/lease_publish.py` |
| **M5** | Bản ghi thu hồi r2 — dữ liệu, sau Q8/Q10 | `ops/thu-hoi/wp461-…-exec-1r2-claude-20260907.yaml` |
| **M6** | Ca + đột biến A1–A9, A11–A12 | `ops/lease_publish_test.py` |
| **M7** | Guard chung 5 cửa, ba trạng thái, root tường minh, `stale` + history idempotent | `.claude/dev/packet_loop.py` |
| **M8** | A10 | `.claude/dev/packet_loop_test.py` |
| **M9** | Workflow: `paths` thêm `ops/thu-hoi/**.yaml`; bước gọi `kiem-thu-hoi-github` từ worktree **canonical** (như bước "neo bộ kiểm" hiện có), truyền `--nhanh-mac-dinh`; đăng comment tiếp nhận `**Thu hồi `X`**` + object ID + sha256 thân lên `packet_issue`; `actionlint` xanh | `.github/workflows/ops-publish-lease.yml` |

### Lược đồ bản ghi (M1) — hợp đồng parser

```yaml
schema_version: 1                     # integer đúng 1, KHÔNG bool
event: lease_revoked                  # literal
lease_id: <X>                         # khớp LEASE_ID, == tên tệp không đuôi
packet_issue: 461                     # integer dương, không bool
thu_hoi_boi: ducthangho               # provider ⇒ rc=4; ngoài NGUOI_CO_THAM_QUYEN ⇒ rc=4
thu_hoi_luc_utc: '2026-09-07T13:41:32Z'   # CHUỖI (quote) ISO8601 Z; không ở tương lai so clock snapshot
ly_do: >-                              # chuỗi không rỗng
can_cu: https://github.com/ducthangho/tra-luat/issues/461#issuecomment-<ID>   # MỘT URL cùng repo, xem Q2
cap_lai_cho: <Y> | null               # vắng/null/rỗng = không đặt đích; có thì hợp lệ LEASE_ID và ≠ X
blob_da_biet_luc_ghi: [<sha40>, …]    # tuỳ chọn, CHỈ đối chiếu; cổng KHÔNG dùng
```

Parser: root phải là mapping; **khoá trùng bị cấm** trước khi thành dict; chỉ nhận regular blob tại đúng
`ops/thu-hoi/<lease_id>.yaml` (không symlink/submodule/thư mục con); đường thoát cây / đồng tự / chuỗi thoát bị từ
chối TRƯỚC khi truy cập (ca do phiên điều phối dựng). Khoá thừa / sai kiểu / sai giá trị ⇒ `rc=8`; YAML hỏng /
khoá trùng / tên tệp ≠ `lease_id` / nguồn không đọc được ⇒ `rc=12`; tài khoản không được phép ⇒ `rc=4`. Thứ tự
kiểm: nguồn/object → cấu trúc/ID → thẩm quyền → trường còn lại. Không dùng truthiness cho bool. packet_loop ánh
xạ mọi lỗi đọc/kiểm sổ sang `RC_STATE` kèm chẩn đoán gốc. Validate **một lần**, mọi consumer dùng chung.

**Append-only cưỡng chế ở ỨNG VIÊN (M4/A8):** với canonical base S (OID đã xác minh) và cây ứng viên T: mọi
đường→blob bản ghi tại S phải còn **NGUYÊN** tại T (sửa/xoá/đổi tên/thay blob ⇒ `rc=8`); phần thêm phải qua M1 +
readback Q2; S không phải tổ tiên T / object thiếu / shallow không chứng minh được mốc ⇒ `rc=12`. Chạy trước MỌI
cập nhật canonical (kể cả fast-forward mà S nằm ở cha thứ hai). **Không** dùng `git log --diff-filter=MD` (reviewer
đo: sửa một bản ghi ⇒ 7 dòng metadata; `merge -s ours` xoá sổ ⇒ 0 dòng).

## `nghiem_thu`

Mỗi tiêu chí nêu phép đo làm nó **ĐỎ** (L3). "Kho giả" = bare + working copy trong thư mục tạm, bare có
`HEAD` symref hợp lệ để `ls-remote --symref` trả nhánh mặc định; clock **cố định** qua tham số/biến để lease
fixture không hết hạn giữa chừng (tiền lệ `t109`–`t113`, `_git_fixture`).

**A1 — áp toàn ID, đơn vị = cặp.** Kho giả: X có **3 blob** khác nhau cùng path trên ≥4 ref, **một** blob KHÔNG
trong `blob_da_biet_luc_ghi`; X, Y còn hạn theo clock cố định; Y giữ cùng `p`. Trước event: holder **{X, Y}**;
sau khi bản ghi X vào canonical: holder **{Y}**, đúng **3** dòng `CÒN_HẠN · ĐÃ_THU_HỒI` cho X, `MAP_REF` phủ đủ ref.
ĐỎ khi: bỏ nạp sổ (holder sai); đột biến áp theo `blob_da_biet_luc_ghi` (blob thứ 3 sống); đột biến bỏ dòng in
(đếm dòng ≠ 3). Ca hết hạn: `HẾT_HẠN · ĐÃ_THU_HỒI`. **Smoke kho thật** (sau M5 land): in đúng tập cặp/ref đo lúc
chạy (hôm nay r2 = **2** cặp) và `NGƯỜI_GIỮ 1: …1g2…`; **land không giết lease** — chỉ nhận 0 khi đã đo g2 hết
hạn/bị thu hồi. Smoke không thay fixture.

**A2 — ref không thẩm quyền.** Cùng blob X trên 3 ref ⇒ **1** dòng/cặp, `MAP_REF` 3 ref. Sổ chỉ ở feature ref ⇒
holder vẫn có X; vào canonical ⇒ không. Thêm: symref cục bộ `origin/HEAD` trỏ feature ⇒ không đổi kết quả (máy
chủ quyết); máy chủ mặc định `main` mà `master` còn tồn tại ⇒ đọc `main`; symref máy chủ vắng/hỏng ⇒ `rc=12`.
ĐỎ khi: đột biến nạp sổ từ mọi ref; đột biến đọc symref cục bộ; đột biến fallback `master`.

**A3 — precedence.** Y khai `thay_the_cho: [X]`: (a) không sổ, không lịch sử ⇒ 8; (b) sổ X, đích trống ⇒ 0;
(c) sổ X đích Z≠Y ⇒ 8 **kể cả** có bia mộ X→Y; (d) cặp lịch sử hợp lệ trên canonical ⇒ 0 **dù** còn blob X chưa
bia mộ trên ref khác (áp toàn ID); (e) cặp chỉ trên feature ⇒ 8, thông điệp có `ops/thu-hoi/`. ĐỎ khi: `any`
mọi ref; bỏ so `cap_lai_cho`; OR fallback khi sổ đã từ chối; bỏ áp toàn ID.

**A4 — chiều ngược.** Chính Y bị thu hồi bởi sổ ⇒ 8 + `ĐÃ_THU_HỒI`; Y chết theo cặp lịch sử ⇒ 8; đo cả có/không
`thay_the_cho`; đối chứng Y sống ⇒ 0. ĐỎ khi: bỏ riêng từng guard.

**A5 — giao write set, không tự nhận nguyên tử.** X đã thu hồi, Y xin `p`, W (≠X, không thay thế) còn giữ `p` ⇒ **11**
kèm W/p; W thu hồi hợp lệ ⇒ 0. Chạy Y có/không `thay_the_cho` (cả hai ⇒ 11 khi W giữ), exact/exact, exact∈prefix,
prefix∩prefix, case-fold (`README.md` vs `readme.md`), NFC; write set `CÒN_HẠN` không đọc được ⇒ 12. ĐỎ khi: bỏ
từng bước chuẩn hoá; thu hẹp về "chỉ khi thay thế". Ca giới hạn: hai clone `check` trước publish cùng 0 — lưu làm
**bằng chứng giới hạn ảnh chụp**, không gọi là hết hai writer.

**A6 — (tên, SHA), OID ghim, chi phí.** Remote-tracking `b` cùng tên nhưng SHA cũ ⇒ 12 nêu `b` + hai SHA40; local
head cùng tên không bù. Đổi `refs/remotes/origin/<mặc định>` SAU phép so ⇒ mọi lần đọc vẫn dùng OID đã ghim
(kết quả không đổi); object thiếu sau so ⇒ 12. ĐỎ khi: so chỉ tên; đọc lại theo tên ref. Chi phí: cũ/mới xen kẽ
3 lượt trên cùng kho/ref/clock, trung vị, tỷ lệ ≤ **2**, ghi raw giây/byte/lệnh.

**A7 — schema và ba trạng thái.** Mỗi ràng buộc M1 một fixture sai **đúng một** trường + đối chứng hợp lệ: YAML hỏng
12 · tên tệp ≠ ID 12 · `thu_hoi_boi: codex` 4 · `ai-codex-bot` 4 · symref máy chủ vắng 12 · khoá thừa 8 · thời gian
tương lai 8 · `schema_version: true` 8 · khoá trùng 12 · `cap_lai_cho: X` 8 · thư mục sổ rỗng ⇒ 0 bản ghi (không lỗi)
· `git` rc≠0 12 · blob thiếu 12. Chạy qua **các consumer** (`ai-dang-giu`, `check`, packet_loop), không chỉ parser.
ĐỎ khi: `raise`→`continue` — **so verdict thật** (có thể 0 hoặc 11 tuỳ holder), không mặc định 0; nới
`NGUOI_CO_THAM_QUYEN` chứa `ai-codex-bot` phải làm đúng ca allowlist ĐỎ.

**A8 — append-only đo cây ứng viên.** S có X; T thêm Y đúng ⇒ 0. T sửa/xoá/đổi tên X, `merge -s ours` bỏ X,
fast-forward có S ở cha thứ hai ⇒ **8** trước khi cập nhật canonical. Sửa bản nháp trong nhánh TRƯỚC lần tiếp nhận
đầu tiên không phải sửa canonical ⇒ 0. Mất lịch sử/object/mốc S ⇒ 12. Đơn vị: **tập đường→blob** trước/sau + rc.
Kho giả cũng là kho thật của phép thử; không tha vì thiếu thư mục `.git` (worktree là tệp, bare không có) — hỏi
`git rev-parse`. ĐỎ khi: chỉ quét `origin/master`; chỉ `git log` path-limited; bỏ kiểm ứng viên.

**A9 — thẩm quyền trước hiệu lực (`kiem-thu-hoi-github`).** Đồ giả `gh api` GIỮ TRẠNG THÁI, ghi trace endpoint/ID/số
lần gọi (tiền lệ `t126`): đúng object/account/khối ⇒ 0; account lạ (kể cả `github-actions[bot]`, `notebyme88`)
⇒ 4; chỉ nhắc ID / phủ định / `X-extra` / sai Issue / sai repo / khối trùng / khối lệch một trường ⇒ 8; 404 / 500 /
timeout / JSON hỏng / thiếu định danh ⇒ 12 (dòng trạng thái HTTP thật). Ca riêng: bản ghi **không** kèm lease mới
⇒ vẫn phải qua cổng (số lời gọi API **≥1**, đột biến bỏ wiring ⇒ 0 lời gọi ⇒ ĐỎ); lease mới đã có comment
(`rc=9`) ⇒ cổng thu hồi vẫn chạy. Object đổi SAU tiếp nhận ⇒ X không sống lại; đổi TRƯỚC ⇒ receipt cũ stale.
ĐỎ khi: bỏ so account / nội dung / repository / Issue.

**A10 — mọi cửa packet_loop.** State hợp lệ riêng cho **5** cửa. Mỗi cửa: sống ⇒ qua; thu hồi ⇒ `RC_STATE`, state
`stale`, history **một** event đúng neo; gọi lại ⇒ không thêm event/tiêu lượt/comment; sổ chỉ ở ref khác ⇒ không
thu hồi; ref/object/YAML/schema/clock không đọc được ⇒ `RC_STATE` + `KHÔNG ĐO ĐƯỢC`, state **không** đổi; root ≠
cwd và state-dir ngoài root vẫn đọc đúng kho. ĐỎ khi: guard chỉ trong `_kiem_luoc_do_lease` (3 cửa bypass ⇒ state
đi tới `accepted`); bỏ lưu state; boolean tồn tại (blob thiếu ⇒ qua).

**A11 — nền và wiring.** Hai vế (base SHA · candidate SHA) dựng và chạy trong **MỘT** lệnh, cùng môi trường; ghi
tập ca passed/failed/skipped/not_run và **delta theo tên ca**, không chỉ tổng. Nền: `lease_publish` 121/121 (wrapper
có actionlint; 120/121 khi thiếu — thiếu công cụ **không** gọi là N/N), `packet_loop` 278/278 + 81 mutant. Mọi
ca mới chạy thật và xanh; mutant đích đỏ, đối chứng khác họ xanh. Workflow: `actionlint` rc=0 (kèm `shellcheck`
có mặt, `t33`) và đo wiring trên ứng viên đúng event/path/SHA gồm ca thu hồi độc lập (`t32`-style: trích thân bước
từ chính YAML). `doc-claims-check --strict` rc=0 + `ok:true`; `doctrine-scan --path` kèm SPEC ⇒ 0.

**A12 — biên nhận có bằng chứng dương.** Mỗi suite ghi lệnh, exact SHA/tree, rc thật, output byte, N/N,
registered/executed/passed/failed/skipped/not_run. Output rỗng / thiếu ca đã đăng ký / chỉ banner ⇒ chưa đo. Đột
biến runner không gọi suite, summary rỗng, bỏ một ca ⇒ kiểm biên nhận ĐỎ. Ca thuộc lớp sandbox cấm (đường thoát
cây/đồng tự/chuỗi thoát) khai `not_run` cho reviewer, phiên điều phối dựng.

## `hinh_dang_ke_thua` (L4)

| hình dạng | số lần | nguồn |
|---|---|---|
| "thu hồi là dữ liệu ghi vào bản sao, không đuổi kịp bản sao" | **2** (wp461-r2 · #456) | §1 |
| "lời khai hội tụ rộng hơn phép đo" | **3** (`3c4c587`, `ddb3200`, **r1 spec này**: "không tồn tại cửa sổ hai lease") | g2, verdict lượt 1 |
| "hai cổng bất đồng về cùng hồ sơ" (`check` 0 · `ai-dang-giu` 11) | **1** (đo được ở #473; con số lịch sử `0/12` chưa có biên nhận API) | #473 |

Hình dạng thứ hai chạm **3** ⇒ theo §12 phải hỏi "có nên tiếp tục cách này". Câu trả lời của r2: **đổi cách
phát biểu** — mọi bảo đảm trong spec này là bảo đảm trên ẢNH CHỤP hoặc trên CÂY CANONICAL, không có câu "đã gỡ".

## `chua_do_duoc`

1. **Ranh giới chủ kho / agent-cầm-PAT** — không đo được từ trong tài khoản (Q2). Chỉ hứa "tài khoản chủ kho".
2. **Chữ ký `web-flow`** — 403; `%G?=E`; ngoài hợp đồng.
3. **Kích thước** — ước 655–945 theo nhóm ca, chưa có diff; đo `numstat` từng slice trước review.
4. **Required check / branch protection / bypass** cho M9 — ngoài kho; **chưa đo**. Chưa đo thì M5 chưa kích hoạt
   (Q10). Đường đã biết: "push được vào `ops/**` thì đăng được" (header workflow) — sổ kế thừa đúng lỗ ấy.
5. **`actions/checkout fetch-depth: 0` nạp đủ `refs/remotes/origin/*`?** — bước "neo bộ kiểm" fetch riêng nhánh
   mặc định; snapshot Q4 cần đủ heads. Đo ở **lượt thi công đầu tiên** bằng chính workflow (in
   `for-each-ref | wc -l` so `ls-remote`); thiếu ⇒ thêm `git fetch origin '+refs/heads/*:refs/remotes/origin/*'`
   vào bước ấy — **trong** write set (M9), không còn là revision.
6. **Độ tươi phía executor** — packet_loop đọc đệm; không có phép đo "đệm cũ bao nhiêu" từ trong lệnh (Q5.1).
7. **Object Q8** — chưa tồn tại; comment `5569885143` là bản chiếu của bot, không đạt.
8. **#456** — `now ≥ 14:30:07Z` chưa đo lúc viết r2 (14:2xZ).
9. **Nguyên nhân `Connection refused (os error 111)` của codex** — chưa biết; lượt 1 chạy trọn 1842,8 s, không gặp.

## 4. Câu chủ kho phải chốt khi cấp lease (mỗi câu có khuyến nghị)

❓ **Q7 — packaging và ngoại lệ ADR-0044.** ➡️ Ba slice nối tiếp, mỗi slice spec/Issue/lease riêng, mọc trên base đã
nhận slice trước (§5/ADR-0044): **A** = `ops/lease_publish.py` + `ops/lease_publish_test.py` + `ops-publish-lease.yml`
(M1–M4, M6, M9; ước 510–730 ⇒ **ngoại lệ có phạm vi**, lý do: phần vượt là ca fail-close, cắt ca là đổi độ phủ lấy
con số); **B** = `packet_loop.py` + test (M7–M8; ước 130–200); **C** = M5 (dữ liệu, sau Q8/Q10). A hữu ích như phép
đo ngay khi land, nhưng **không** tự đủ để wp461 chạy lại — cần C và điều kiện Q11.
❓ **Q8 — object cấp lệnh thu hồi r2.** ➡️ Chủ kho đăng lên **#461** một comment chứa đúng khối
`lease_revocation_authorization` (Q2) cho `wp461-…-exec-1r2-claude-20260907`, `cap_lai_cho: wp461-…-1g2…`. Bản
chiếu bot và PR #474 chỉ là tài liệu tham khảo. Comment cùng tài khoản không nói human hay agent — không hứa hơn.
❓ **Q9 — nhận bản ghi cho lease ĐÃ hết hạn?** ➡️ Nhận; in `HẾT_HẠN · ĐÃ_THU_HỒI`; hết hạn không gỡ event, không
cho tái dùng ID. Protocol không cấm; đây là lựa chọn sản phẩm, không phải đáp án bắt buộc.
❓ **Q10 — kích hoạt sổ bằng đường có thẩm quyền nào?** ➡️ Đo required-check/branch protection cho `master` với
check của M9 trước khi ghi M5; chưa đo được bypass/direct-push ⇒ sổ chưa kích hoạt. Đây là điều kiện bắt buộc,
không phải nợ "đăng comment".
❓ **Q11 — gỡ quyền worker cũ, cho worker mới bắt đầu.** ➡️ Quy trình tuần tự có thẩm quyền: (1) bản ghi thu hồi
land; (2) chủ kho xác nhận worker cũ đã dừng + giữ last SHA/state (ADR-0028); (3) lease mới `check` trên ảnh chụp
mới, land, `ai-dang-giu` readback `NGƯỜI_GIỮ 1`; (4) mới cho bắt đầu. Fencing máy toàn phần là dependency khác;
KHÔNG chọn "`check rc=0` là khoá".
❓ **Q12 — ready của chính packet.** ➡️ Trước cấp lease: Issue + `spec_hash` r2 + revision; closure/checks/land
obligations do bên điều phối điền (không kế thừa miễn trừ `b416830`); base đã nhận slice trước; wiring fetch/admission
đã đo (mục 5 `chua_do_duoc`). Thiếu ⇒ giữ `proposed`.
