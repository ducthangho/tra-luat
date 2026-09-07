# ĐẶC TẢ PACKET — `THU-HOI-LEASE-VA-CAP-LAI`, **revision 6** (sau lời gọi review cuối 6/6 — CHƯA ĐƯỢC REVIEW)

```yaml
packet_id: THU-HOI-LEASE-VA-CAP-LAI
packet_issue: CHƯA CÓ          # KHÔNG đăng: còn P1 chưa được reviewer xác nhận đóng (§3.2/§12)
revision: 6
thay_the: 23a7deaf60af17aea2fa3b027d08fb8c187b6f03499f34540822ab7b9c3b1672   # sha256 r5, review lượt 5 (lời gọi 6/6)
thay_the_r4: 415ce35db32aa370ce43315c1ff6d4db7b59005e6288538e72705ce4caed4d0e
thay_the_r3: ef9b3700514921d4cabe95947f86937fc36f4aecf2f4e2e39587cafe88a9bb20
thay_the_r2: 9e775a154dd83741fd4e7af85aaeae1f5693ceabc5c5763cf6890ff4f2606c80
thay_the_r1: 43844cb2ea2653f502320a6f35a6e3ae7fd182770f02b62d4d73b9aa8dbea6f9
review_class: sensitive        # ops/lease_publish.py + .claude/dev/packet_loop.py + .github/workflows/ — §8, fail-closed
executor: claude
reviewer: codex
assurance_target: cross_approved
base_sha: b416830ef2a509d60203d55552ce17950afcf67c   # origin/master lúc đóng băng
```

**Mọi con số đo lúc `13:2x–16:0xZ 07-09-2026` trên `303` ref** (302 tên nhánh máy chủ + 1 nhánh cục bộ
`master`); ba lượt reviewer đo lại trên mirror (13:52Z · 14:33Z · lượt 3) và **khớp**, trừ chỗ ghi "đính chính".
**Đo lại trước mỗi bước công bố** (L5). Đơn vị (L1): "cặp" = **(blob, đường dẫn) duy nhất** trên mọi ref — một dòng
`ai-dang-giu` cho mỗi cặp; "lease_id" = giá trị trường; "ref" = dòng `git for-each-ref refs/heads refs/remotes` trừ
`*/HEAD`. **[API]** = chỉ đo được phía điều phối (mạng), không dùng làm bằng chứng thẩm quyền.

## 0. Lịch sử review — và Review Rescue Checkpoint (§12)

| lượt | bản | model/effort | thời lượng · byte | verdict |
|---|---|---|---|---|
| 1 | r1 `43844cb2…` | codex `gpt-6-astra` high | 1842,8 s · stderr 777 646 B | `changes_requested` — 11 P1 + 3 P2; verdict `b60a755f…` |
| 2 | r2 `9e775a15…` | codex `gpt-6-astra` xhigh | 3322,4 s · stderr 4 964 212 B | `changes_requested` — cũ 5 ĐÓNG/8 một phần/1 sai; mới 9 P1 + 2 P2 (N1–N11); verdict `bb293295…`, hint `02b562b3…` |
| 3 | r3 `ef9b3700…` | codex `gpt-6-astra` xhigh | 2737,1 s · stderr 3 488 714 B | `changes_requested` — N: 6 ĐÓNG/3 một phần/2 sai; lượt 1: 7 ĐÓNG/7 một phần; mới **9 P1 + 1 P2** (R1–R10); verdict `6b8dde21…`, hint `0a81bd8b…` |
| 4a | r4 `415ce35d…` | codex `gpt-6-astra` xhigh | 1601,5 s · stdout **0 B** · stderr 1 891 237 B · 183 508 token | **CHẾT** — bộ lọc nội dung của nền bắn khi reviewer tự soạn probe helper/config; KHÔNG phải mạng. Theo §12 vẫn **đếm** (đã sinh output) |
| 4b | r4 `415ce35d…` | codex `gpt-6-astra` xhigh, **đổi phân công** (hướng đổi-nguồn chỉ mô tả bằng lời) | 2076,6 s · stderr 743 428 B | `changes_requested` — R2–R10 ĐÓNG, R1 một phần; mới **4 P1 + 2 P2** (S1–S6); verdict `7d3017ec…`, hint `4a0321fd…` |
| 5 | r5 `23a7deaf…` | codex `gpt-6-astra` xhigh, **lời gọi 6/6** | VERDICT `1596d562…` · HINT `8ca8474b…` · 2394,7 s · rc=0 | `changes_requested` — S4 + mọi R/N/L1 còn lại ĐÓNG; còn **3 P1** (S1, S2 một phần; S3 ĐÓNG SAI) + **2 P2** (S5, S6 một phần); reviewer khai `blocked` theo stop condition |

**R10 — trần review §12 KHÔNG có ngoại lệ cho "review đặc tả".** r3 §0 suy một ngoại lệ từ nhãn "spec trước Issue" —
reviewer đối chiếu `docs/PROTOCOL_DA_PHIEN.md:806–816` và §8:579: trần **hai** lượt codex tính **theo PR**, đổi
prompt/phiên không reset, chạm trần ⇒ Review Rescue Checkpoint. r4 rút câu ấy. Trạng thái đúng: PR #475 đã dùng **6/6** lời gọi
(3 lượt + 4a chết + 4b + 5); **trần đã hết**. r6 là bản vá theo hint lượt 5, **chưa được lượt review nào xác nhận** ⇒
không đăng Packet Issue; checkpoint kế thuộc chủ kho (ADR nguồn tin cậy + trần mới, hoặc dừng). Lượt 2–3 chạy theo chỉ thị trực tiếp trong phiên; từ lượt 4 có neo bền. **Checkpoint của r4:** (a) quyết định = **thiết kế
lại** (r4 là sản phẩm: adapter nguồn, bootstrap có biên riêng, C không đích); (b) trần mới **đã được chủ kho chốt và neo**:
comment `https://github.com/ducthangho/tra-luat/pull/475#issuecomment-5575587924` (tài khoản chủ kho, ghi hộ theo chỉ thị
trong phiên, đã readback): **trần 6 lượt** cho PR #475; dừng khi hết P1 hoặc chạm 6 ⇒ checkpoint kế; (c) mọi bộ đếm/ID
finding giữ nguyên, tách slice không reset. Comment ấy KHÔNG cấp lease, KHÔNG kích hoạt sổ. **Lời gọi 6/6:** reviewer 4b
khuyến nghị dừng packet để chốt ADR nguồn tin cậy trước; chủ kho chốt trong phiên (~22:1xZ 07-09) **dùng lời gọi 6 trên r5**
(S1/S2 đã đóng bằng hai lớp tận cùng); còn P1 sau lượt này ⇒ checkpoint kế + ADR, không tự nới.

### 0.1 Delta r3 → r4 theo finding lượt 3

| finding (P) | r3 sai/thiếu | r4 làm gì |
|---|---|---|
| R1 `canonical-url-check-does-not-bind-transport` (P1) | so `ls-remote --get-url` rồi vẫn discovery qua tên `origin` chịu config ứng viên: `remote.origin.vcs=<helper>` giữ URL canonical mà trả sổ của kho khác; đổi config giữa hai lời gọi | Q4.1: **adapter nguồn** — discovery bằng URL tường minh dựng từ `KHO_CANONICAL`, chạy trong thư mục git RỖNG cô lập (`GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`), allowlist transport `https` + TLS; không bao giờ gọi `origin` |
| R2 `replace-refs-bypass-oid-pinning` (P1) | `refs/replace` làm `ls-tree <OID>` trả cây khác dù OID không đổi | Q4.5: `GIT_NO_REPLACE_OBJECTS=1` cho mọi lời gọi đọc object/ancestry/diff; phát hiện graft/`replace.refBase` ⇒ 12 |
| R3 `bootstrap-gate-trusts-pr-and-arrives-too-late` (P1) | cổng bootstrap là ca test chạy trong CI của chính PR (PR xoá ca ⇒ 0/1-of-1 vẫn xanh); workflow M9 chỉ có ở A1 nên lượt A1 không có mã canonical để chạy | Q7: **workflow vào A0** ở chế độ chưa kích hoạt (S và T rỗng ⇒ receipt, khác ⇒ 12); lần land A0 = audit bootstrap của chủ kho (exact S/H/tree rỗng); A1 chỉ bật cờ + ghim mốc |
| R4 `inactive-a0-already-changes-lease-decisions` (P1) | A0 giao M3 precedence nhưng danh sách lịch sử chỉ có ở A1 ⇒ `check Y` cũ 0 thành 8 trước cổng delta | Q3/M3: khi cờ `False` và sổ rỗng, verdict sản phẩm = luật cũ; luật mới chỉ chạy ở **hàm dự báo có nhãn** `DU_BAO`; A1 bật toàn bộ cùng lúc |
| R5 `admission-head-is-not-the-landed-candidate` (P1) | M9 fetch `refs/pull/n/head` không so với `head.sha`; base trôi ⇒ receipt S0/H cũ vẫn 0 trong khi cây merge sửa event canonical | M9: S = canonical hiện tại đã Q4; H = `head.sha` event, fetch phải == H; T = tree(H); strict up-to-date + merge giữ tree; land đối chiếu tree(M) == T; queue chưa hỗ trợ ⇒ chặn; dispatch có input S/H/PR |
| R6 `self-declared-effective-set-shrinks-exclusion` (P1) | "có `effective_write_set` thì dùng" ⇒ lease tự khai `[]` làm 11 thành 0; raw fallback thiếu companion §5 | Q3: **không nhận** trường tự khai; closure tính từ policy canonical ghim + provenance; policy vắng ⇒ độc quyền mới chỉ là dự báo, kích hoạt đòi #473 hoặc ngoại lệ Q13 có neo |
| R7 `symlink-resolution-lacks-source-and-termination-contract` (P2) | không nói giải theo cây nào khi một cặp khử trùng qua nhiều ref; vòng A↔B; local head ghim lúc nào | Q3: hợp đồng symlink (nguồn theo từng occurrence OID, hợp bảo thủ, tương đối từ thư mục chứa, vòng/ngoài/thiếu ⇒ 12, visited-set) |
| R8 `cutover-delta-and-fixed-g2-smoke-conflict` (P1) | "delta = 0" làm C thành điều kiện của A1; g2 hết hạn `2026-09-08T09:52:00Z` **trước** gate cuối 10:17Z ⇒ smoke "1 g2" không thể xanh | Q6: cutover phân loại delta (a)/(b)/(c); **C = thu hồi KHÔNG đích** (`cap_lai_cho: null`); cấp lại = lease g3 riêng sau kích hoạt; smoke in tập thật |
| R9 `a8-mode-case-cannot-kill-stated-mutant` (P1) | mutant "chỉ validate phần thêm" vẫn bị map tuple chặn ⇒ ca mode không giết được nó | A8: khai mutant ấy **sống** dưới ca mode; mutant kết hợp (map chỉ blob + validate phần thêm) mới giết; unit riêng cho validator toàn T |
| R10 `spec-review-label-does-not-waive-review-cap` (P1) | §0 r3 suy ngoại lệ trần | §0 trên; Q14 |
| N1/N3/N6 một phần; N4/N5 ĐÓNG SAI | = R1/R3/R5/R8/R6 | như trên |

### 0.2 Delta r4 → r5 theo finding lượt 4b

| finding (P) | r4 thiếu | r5 làm gì |
|---|---|---|
| S1 `adapter-environment-boundary-is-not-specified` (P1, tiếp R1) | chỉ tắt system/global config + allowlist tên protocol; chưa nói env con dựng từ đâu, executable nào, `GIT_DIR`/template/include gián tiếp | Q4.1: **hồ sơ adapter** — env con dựng từ RỖNG + allowlist khoá deployment; `PATH` tối thiểu; executable ghim (đường tuyệt đối + sha256 vào receipt); `GIT_DIR` tường minh, `--template=` rỗng; hồ sơ ghi vào receipt; lệch ⇒ 12 |
| S2 `raw-object-read-does-not-verify-content-identity` (P1) | đọc cache object cục bộ (không tin cậy) theo OID mà không băm lại bytes | Q4.5: **băm lại** mọi object dùng trên đường commit→tree→blob và ancestry, so với OID ghim; parser ăn đúng bytes đã xác minh; lệch ⇒ 12. Lớp này CŨNG bắt `refs/replace` |
| S3 `a6-single-mutant-is-shielded-by-cli-flag` (P1) | A6 hứa bỏ riêng biến env làm ca đỏ trong khi cờ CLI còn che | A6: mutant đơn (env HOẶC cờ) khai **sống**; sau S2 cả mutant kết hợp cũng bị lớp băm che ⇒ khai sống; chỉ mutant bỏ **cả ba** (env + cờ + băm) mới đổi màu |
| S4 `q13-selected-mode-conflicts-with-a5-and-ready-fields` (P1) | A5 vẫn đòi "policy vắng ⇒ 12" trái Q13; Q12 đòi policy SHA chưa tồn tại | A5 ba nhánh (policy / ngoại lệ có neo / không neo); Q12: **descriptor nguồn closure** (policy SHA HOẶC descriptor ngoại lệ) đóng băng trong `spec_hash` |
| S5 `m9-check-publisher-consumer-is-unspecified` (P2) | chưa nói object nào phát/tiêu required check | M9: publisher = check-run của chính workflow (`pull_request_target` gắn với **H** — đo được trên PR #475: check-run `cong` id `101767296495` của `duyet-khac-danh-tinh.yml` nằm dưới head `1ebd86e`); consumer = required check + land readback theo (tên, H, OID workflow, kết luận, receipt trong `output.summary`) |
| S6 `q13-exception-scope-and-retirement-are-not-bound` (P2) | ngoại lệ chưa có descriptor/hết hiệu lực/nơi ghi retired | Q13: descriptor `{owner, object_id, body_sha256, pham_vi, het_hieu_luc}`; hết theo **lần đầu** policy hợp lệ xuất hiện trên canonical; policy có mà hỏng ⇒ 12; retired ghi ở receipt A1 + Packet Issue; không cache |

### 0.3 Delta r5 → r6 theo finding lượt 5 (chưa review)

| finding (P) | r5 thiếu | r6 làm gì |
|---|---|---|
| S1 (P1, nguồn tin cậy) | allowlist `credential.*`/`http.*` theo tên + dò chuỗi trong giá trị (không phải validator Git: `http.sslVerify=false` là boolean, `http.proxy` là endpoint); receipt chỉ ghi TẬP TÊN biến | Q4.1: allowlist **hữu hạn khoá + kiểu + miền giá trị**; **profile digest** (băm của cấu hình không bí mật + định danh helper/CA/executable) so với **mỏ neo đã duyệt ghim trong mã**; khác ⇒ 12 |
| S2 (P1, nguồn tin cậy) | băm blob nhưng chưa ràng buộc CẠNH (tree trung gian, parent) và repo tạm không có object (`cat-file` trả `missing`) | Q4.5: **API object-store**: `GIT_DIR` = repo tạm cô lập + `GIT_OBJECT_DIRECTORY` = objects của kho nguồn (chỉ đọc); mọi cạnh trích từ **bytes đã xác minh** (entry tree, header parent), tự đi đồ thị, memoize `(type, OID)`; không `merge-base`/walker |
| S3 (P1, ĐÓNG SAI) | A6 đòi `refs/replace` ⇒ 12 dù no-replace đọc object gốc (băm khớp); hứa mutant bỏ 3 lớp "đọc giả" dù profile còn chặn | A6: replacement ⇒ verdict **không đổi** (đọc gốc); ca riêng bytes lệch OID ⇒ 12; catalog ghi **seam** + chốt còn nguyên, không hứa kill vô điều kiện |
| S5 (P2) | `GITHUB_STEP_SUMMARY` ≠ `output.summary` của Checks API (chưa readback); dispatch H không tự gắn check-run; join provenance | M9: receipt = **workflow artifact** `thu-hoi-receipt-<H>` (readback qua API artifacts); join độc lập check-run → run → artifact → định nghĩa workflow tại S; dispatch **không** tạo pass; consumer = bước trong `land-packets` (dependency, ngoài write set) |
| S6 (P2) | ai produce/verify descriptor; sự kiện policy xuất hiện rồi biến mất (A→B→D) bị đọc current-only bỏ lỡ | Q13: descriptor = comment chủ kho + **hằng ghim trong mã A1** (ID + băm thân); retirement = tệp append-only `ops/thu-hoi/_ngoai-le-closure.retired.yaml` do **M9 ép** (T có policy mà thiếu tệp ⇒ 12); tệp ở lại vĩnh viễn ⇒ không hồi sinh |

Đính chính số: tổng ước dòng r3 (`885–1285` theo hint lượt 3; r3 viết 725–1055 ở một chỗ và bảng khác ở chỗ khác) —
r4 ước lại theo slice ở `write_set`.

## `nguon_cap_viec`

- Lệnh chủ kho lập phiên (`session_01Vt7NfNpABHfSWpxvx4aJGE`, 07-09-2026): *"bổ sung cơ chế CHỦ KHO THU HỒI LEASE
  và CẤP LẠI CHO MỘT PR KHÁC"*. Neo là Packet Issue, không phải câu chat.
- Nợ `AG-T0-01B-thu-hoi-lease-chua-co-duong`; nợ #473 (`bia-mo-check-bo-sot-chieu-nguoc`, `cong-check-thieu-do-phu-tham-quyen`);
  lease g2 `wp461-…-exec-1g2-claude-20260907` (PR #474), khoá `hoi_tu_nguoi_giu_doi_thao_tac.no_nen`.

## 1. Vấn đề — ĐÃ ĐO, ba lượt reviewer đo lại

Thu hồi hôm nay chỉ có bia mộ hai chiều, ép bởi `ops/lease_publish.py::_kiem_bia_mo` (595–617); bia mộ là dữ liệu ghi
vào TỆP CŨ có nhiều bản sao:

| phép đo | giá trị |
|---|---|
| ref quét · cặp · đường dẫn · lease_id | **303 · 288 · 273 · 273**; 7/273 lease_id có >1 blob |
| lease_id `CÒN_HẠN` / chưa bia mộ | **8/4** (13:41Z) → **7/3** (14:33Z; #456 hết hạn `14:30:07Z`) |
| r2 wp461 | **2 cặp**: `26f07b4` (0 bia mộ; 4 ref) · `fdfde3a` (bia mộ; 1 ref `origin/ops/lease-wp461-g2`); **[API]** PR #475 là ref thứ 5 |
| #456 | `8b2103c` chưa bia mộ **11 ref** / `1f95042` bia mộ **1 ref** (#468) |
| tệp `da_bi_thay_the` master / #468 | **7 / 11**; 7 cặp master hai chiều hợp lệ; 3 `gate-tach` + `mutant` chỉ ở #468; #468 có **31** commit riêng |
| `ai-dang-giu` 4 đường wp461 · `check` g2 | `NGƯỜI_GIỮ 2` rc=11 · rc=0 `ĐĂNG ĐƯỢC` |
| hạn g2 · gate r1/r2/r3/r4 (2026-09-08) | **09:52:00Z** · 03:37:33Z / 07:50:35Z / 09:44:51Z / 10:17:12Z |

Ba hệ quả có dòng mã: `_kiem_bia_mo` dùng `any(...)` (606–610); `kiem()` (787–890) gọi `_lease_cham_duong` **0** lần;
bia mộ trên nhánh `ops/**` không đuổi kịp bản sao.

**Bất biến:** *cấp ở bất kỳ ref nào chỉ THÊM người giữ; thu hồi ở đúng MỘT chỗ mọi phép đo đọc; chỗ ấy có cổng tiếp
nhận chạy MÃ ĐÃ CANONICAL trước hiệu lực; nguồn được đọc phải có danh tính VÀ transport ghim, đọc object không qua lớp
diễn giải lại.*

## 2. Sáu câu hỏi

### Q1 — Chủ kho phát lệnh thu hồi ở ĐÂU?

➡️ Sổ append-only `ops/thu-hoi/<lease_id>.yaml` trên nhánh mặc định của kho canonical. **Hiệu lực = (i) sổ đã KÍCH
HOẠT (A1, Q10) ∧ (ii) bản ghi hợp lệ M1 ∧ (iii) đã qua cổng M9 trên đúng S/H/T ∧ (iv) có mặt trong cây canonical tại
OID đã chụp qua adapter Q4.** Bản ghi ở ref khác = CHƯA thu hồi. Bảng phương án đã loại giữ như r3 (sửa tệp mọi ref ·
bia mộ cùng nhánh · chỉ comment · `git notes`/ref riêng · `ops/leases/thu-hoi/` · mở `paths` của `ops-publish-lease.yml`).

### Q2 — Danh tính chủ kho và LỆNH thu hồi

Bằng chứng Git tại `b416830` (đo lại ba lượt): `b416830` author `ducthangho`, committer `GitHub`, **1** `gpgsig` PGP,
`%G?=E` keyring rỗng; `6635379` author/committer `Claude`, **1** `gpgsig` SSH; **[API]** actor 5 lượt workflow =
`ducthangho`, `author.login` = `claude`. Trong tài khoản chủ kho **không có ranh giới máy** tách "chủ kho gõ" khỏi
"agent cầm PAT"; spec không bịa; chữ ký `web-flow` ngoài hợp đồng.

➡️ Bản ghi thu hồi = chuẩn thẩm quyền của bản ghi CẤP + cổng tiếp nhận:

1. `thu_hoi_boi`: chốt provider (`rc=4`) rồi `NGUOI_CO_THAM_QUYEN` (`rc=4`).
2. `can_cu`: **MỘT** URL Issue comment `https://github.com/<KHO_CANONICAL>/issues/<N>#issuecomment-<ID>`, `<N>` ==
   `packet_issue`; loại object khác ⇒ 8. Readback: `id` == `<ID>`, `issue_url` đúng repo và `<N>`, `user.login ∈
   NGUOI_CO_THAM_QUYEN` (khác ⇒ 4, kể cả bot/collaborator). Thân có **đúng một** khối:

   ````text
   ```json lease_revocation_authorization
   {"event":"lease_revoked","lease_id":"X","packet_issue":461,"cap_lai_cho":null,"thu_hoi_boi":"ducthangho","thu_hoi_luc_utc":"2026-09-07T13:00:00Z"}
   ```
   ````

   JSON: khoá trùng ⇒ 8 (từ chối trước khi tạo dict); root object; **đúng sáu khoá**; `packet_issue` integer dương
   (không bool/float); `cap_lai_cho` ID hợp lệ hoặc `null` (YAML vắng/null/rỗng chuẩn hoá về null); so **giá trị và
   kiểu**. Lệch/thiếu/JSON lệnh hỏng ⇒ 8; HTTP ≠ 200 / timeout / envelope hỏng ⇒ 12. Prose nhắc ID / phủ định / tiền tố
   ⇒ không phải lệnh.
3. M4 readback **mọi bản ghi mới so với S** ở mỗi lần kiểm T; receipt (M9 đăng bản chiếu `**Thu hồi `X`**` lên
   `packet_issue`) ghi: `KHO_CANONICAL`, nhánh mặc định, **S/H/tree T**, OID bộ kiểm, từng path/(mode, type, blob),
   comment ID, sha256 thân UTF-8 **đã đến**. Sau khi vào canonical: object đổi không gỡ event; `kiem-github` của lease
   mới **không đọc lại** căn cứ lịch sử (0 lời gọi thêm).
4. Hiệu lực theo Q1(i)–(iv).

### Q3 — Lease mới neo vào thu hồi; `check` bỏ `any(...)`; độc quyền

Giữ `thay_the_cho: [X, …]`. **Hai chế độ, một mã** (R4):
- **Chưa kích hoạt** (`SO_THU_HOI_KICH_HOAT = False`, A0): verdict sản phẩm của `check`/`ai-dang-giu` = **luật cũ** trên
  đầu vào hợp lệ; luật mới (precedence, chiều ngược, độc quyền theo closure, danh sách lịch sử) chỉ chạy trong **hàm dự
  báo có nhãn** (`--du-bao`, in `DU_BAO:` riêng, không đổi rc). Sổ canonical **không rỗng** khi cờ `False` ⇒ 12 ở mọi
  consumer vận hành. Validator ứng viên M4 độc lập với cờ.
- **Đã kích hoạt** (A1): với từng X: (1) sổ có X ⇒ `cap_lai_cho` null hoặc == ID mới ⇒ qua, khác ⇒ 8, không rơi sang bia
  mộ; (2) không sổ ⇒ chỉ cặp trong `BIA_MO_LICH_SU` ghim ⇒ 0, không ⇒ 8; (3) chiều ngược: lease đang kiểm chết (sổ hoặc
  danh sách) ⇒ 8.

**Độc quyền — MỌI lease, theo CLOSURE, không theo tự khai (R6):**
- **Nguồn closure — ba nhánh, một descriptor (S4/S6):** (1) policy canonical `.github/coordination/change-impact.v1.json`
  **có và hợp lệ theo schema** ⇒ closure bắc cầu tính từ `write_set` theo policy, `change_policy_sha` = sha256 policy;
  (2) policy **vắng** và **descriptor ngoại lệ Q13 hợp lệ** ⇒ closure = tập khai báo + giải symlink theo cây OID;
  (3) policy vắng, không descriptor hợp lệ, sổ đã kích hoạt ⇒ 12; policy **có mà hỏng/lệch schema/lệch băm ghim** ⇒ 12
  (không rơi về (2)). `effective_write_set` trong YAML lease **không dùng để thu hẹp**: có mặt thì phải **bằng tập** closure
  tính lại theo nhánh đang áp, lệch ⇒ 8; vắng thì không sao. Raw set ⊆ closure. Đo 21:2xZ: policy và schema đều **vắng**
  ⇒ nhánh (2) áp khi kích hoạt. **Descriptor ngoại lệ Q13 — producer/verifier/retirement (S6):** *producer* = chủ kho (comment `5575587924`; thân đã
  readback); *verifier* = hằng `NGOAI_LE_CLOSURE = {object_id: 5575587924, body_sha256: <băm thân UTF-8 đã đến>, owner:
  "ducthangho", pham_vi: "phép giao write set của lease trong kho này"}` **ghim trong mã A1** (commit có review) — không
  có dispatcher thì mỏ neo trong mã đã canonical là thứ duy nhất không tự khai; descriptor trong Issue/lease phải **bằng**
  hằng ấy, lệch ⇒ 12. *Retirement theo sự kiện, không bỏ lỡ:* PR đầu tiên đưa policy hợp lệ vào canonical **phải** kèm tệp
  append-only `ops/thu-hoi/_ngoai-le-closure.retired.yaml` (`{policy_sha256, oid_T, thoi_diem}`), **M9 ép** (T có policy hợp
  lệ mà thiếu tệp ⇒ 12; tệp có mà policy vắng/hỏng ⇒ 12); tệp ở lại vĩnh viễn (append-only A8) ⇒ ca A→B→D (policy xuất
  hiện rồi biến mất) **không** quay lại ngoại lệ vì tệp retired còn. Reader: tệp retired có ⇒ nhánh (2) chết; policy có
  mà không tệp ⇒ 12. Không cache. Policy canonical mới làm closure/check/băm đổi ⇒ pause + revision/generation (§5/ADR-0025),
  không chuyển lease đang sống sang policy dưới descriptor cũ. Ngoại lệ chỉ miễn **phép tính va chạm** của packet này.
- Chuẩn hoá §5: separator `/`; từ chối tuyệt đối/`.`/`..`/thoát repo (lease `CÒN_HẠN` ⇒ 12); NFC + case-fold **chỉ làm
  khoá so va chạm**, tra Git tree bằng tên thật; `normpath`; kết thúc `/` = prefix; `planned:` bỏ nhãn.
- **Symlink (R7):** giải theo **Git tree của từng occurrence OID** của cặp lease (không khử trùng trước khi giữ nguồn),
  và theo cây ứng viên; đích tương đối tính từ thư mục chứa link; link ở parent của tệp mới cũng giải; tập loại trừ =
  **hợp** của đường logic + mọi đích đã giải; đích tuyệt đối / trỏ ngoài cây / vòng (visited-set, trần độ sâu) / object
  thiếu / entry không hiểu ⇒ 12; đích chưa tồn tại chỉ hợp lệ cho tệp mới sau khi mọi parent có mặt đã giải; prefix bao
  cả alias lồng trong subtree.
- Giao exact/exact, exact∈prefix, prefix∩prefix của hai tập hiệu lực với lease `CÒN_HẠN` chưa chết khác ⇒ 11 nêu
  `lease_id`, đường logic, đích va chạm, OID nguồn. Tập sống không đo được ⇒ 12; lease đã xác minh `HẾT_HẠN` chỉ chẩn
  đoán (lỗi parse hạn **không** là bằng chứng hết hạn). Không dùng `_lease_cham_duong`.

**Hàm thuần vs CLI:** `trang_thai(snapshot, ứng_viên)` thuần (test; hai ứng viên trước publish có thể 0/0 — giới hạn ảnh
chụp). CLI `check <tệp>`: ứng viên phải nằm **đúng (blob, path)** trên ít nhất một `refs/heads/*` máy chủ quảng bá trong
snapshot (nhánh nào cũng được; tag/`refs/pull/*`/local-only ⇒ 12). `check rc=0` là **ảnh chụp**; cấp → readback → cho
bắt đầu do một bên điều phối tuần tự hoá (Q11).

### Q4 — MỘT snapshot qua ADAPTER NGUỒN, MỘT phép tính

1. **Adapter nguồn (R1 + S1) — HỒ SƠ TIẾN TRÌNH tường minh:** danh tính ghim trong mã `KHO_CANONICAL =
   "github.com/ducthangho/tra-luat"`; endpoint = `https://` + `KHO_CANONICAL` (URL tường minh, không bao giờ là tên
   `origin`). Adapter là một hàm trong `ops/lease_publish.py` dựng **env con từ RỖNG** (không kế thừa `os.environ`):
   `PATH=/usr/bin:/bin` (hoặc thư mục chứa executable đã ghim), `HOME=<thư mục tạm riêng>`, `GIT_CONFIG_NOSYSTEM=1`,
   `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_DIR=<repo tạm mới do adapter tạo>`, `GIT_TEMPLATE_DIR=` (rỗng; `git init
   --template=`), `GIT_NO_REPLACE_OBJECTS=1`, `GIT_TERMINAL_PROMPT=0`, `GIT_ALLOW_PROTOCOL=https`, `LC_ALL=C`; **cấm**
   `GIT_WORK_TREE`, `GIT_COMMON_DIR`, `GIT_CEILING_DIRECTORIES`, `GIT_EXEC_PATH`, `GIT_SSL_NO_VERIFY`, `GIT_PROXY_COMMAND`,
   `GIT_ASKPASS`, `SSH_*`. Từ deployment chỉ kế thừa **allowlist HỮU HẠN theo khoá + kiểu + miền giá trị** (S1) — không wildcard:
   `credential.helper` ∈ tập tên helper đã duyệt (ghim trong mã, vd `{"", "cache", "store"}` — không đường dẫn, không `!`);
   `credential.<url>.username` chuỗi; `http.sslCAInfo`/`http.sslCAPath` đường tuyệt đối tới tệp/thư mục tồn tại;
   `http.proxy`/`https_proxy`/`HTTPS_PROXY` URL `http(s)://host[:port]` với host ∈ allowlist proxy ghim; **cấm** mọi khoá khác
   (`http.sslVerify`, `http.<url>.*`, `http.curloptResolve`, `http.followRedirects`, `core.*`, `url.*`, `include.*`,
   `remote.*`, `credential.*.helper` khác tập) ⇒ 12. Giá trị được **parse theo kiểu Git** (bool/path/URL), không dò chuỗi.
   **Profile digest** = sha256 của bản chuẩn hoá `{khoá=giá trị không bí mật đã sắp xếp, đường tuyệt đối + sha256
   executable git, `git --version`, sha256 tệp CA, tên helper}`; digest phải **bằng** mỏ neo `PROFILE_ADAPTER_DA_DUYET`
   ghim trong mã (sửa qua commit có review); khác/không tính được ⇒ 12. Receipt ghi digest + các trường không bí mật.
   Executable = đường **tuyệt đối** giải một lần bằng `shutil.which("git")` trong `PATH` tối thiểu.
   Lệnh: `git init --template= <tmp>` rồi `git ls-remote --symref <endpoint> HEAD 'refs/heads/*'` với env trên; `-c
   protocol.allow=never -c protocol.https.allow=always`. Receipt ghi **hồ sơ** (tập khoá env đã dùng, đường + băm
   executable, endpoint); hồ sơ khác hồ sơ đã ghim trong mã ⇒ 12. `ls-remote --get-url origin` chỉ là chẩn đoán.
   Config kho (`remote.<x>.vcs`, `url.*.insteadOf`, `include.path`, helper) **không chạm** được adapter vì adapter không
   đọc config kho, không chạy trong kho, không kế thừa env. Fixture: test tiêm endpoint (bare cục bộ) qua **API nội bộ**;
   không có biến môi trường/cờ production đổi authority. Ca âm cho S1 (env bẩn, executable giả) do **điều phối dựng**.
2. **Chụp map cục bộ TRƯỚC:** `refs/heads/*` và `refs/remotes/origin/*` → map tên→OID một lần; tách map remote-tracking
   (đối chiếu máy chủ) khỏi local heads (chỉ THÊM người giữ). Giữ map cùng mọi occurrence ref của từng cặp.
3. **Một lời gọi discovery:** adapter `git ls-remote --symref <endpoint> HEAD 'refs/heads/*'` → nhánh mặc định máy chủ
   khai + `(tên, SHA40)`. Workflow truyền `--nhanh-mac-dinh`; phải bằng symref; lệch/vắng/mơ hồ ⇒ 12. Không fallback.
4. **So:** mọi tên máy chủ có trong map remote-tracking với **cùng SHA40** (thiếu/lệch ⇒ 12 nêu tên + hai SHA); local
   heads không bù. **OID canonical = OID nhánh mặc định trong advertisement đã so**; HEAD OID phải khớp. **Không chụp lại.**
5. **API object-store đã xác minh (R2 + S2):** cache object của kho đọc là **không tin cậy**. Adapter đọc object bằng
   `GIT_DIR=<repo tạm cô lập>` (không ref, không `refs/replace`, config trống) + `GIT_OBJECT_DIRECTORY=<kho nguồn>/.git/objects`
   (chỉ đọc; `GIT_ALTERNATE_OBJECT_DIRECTORIES` cho alternates của nó), `GIT_NO_REPLACE_OBJECTS=1`, `cat-file --batch`.
   Đo 22:4xZ (reviewer): repo tạm **không có object** ⇒ `cat-file` trả `<OID> missing` rc=0 — routing trên là bắt buộc, và
   `missing` ⇒ 12. **Tập gốc** = {OID canonical, OID từng occurrence ref của mọi cặp lease, S, H, OID mốc lịch sử, OID mã
   A0/workflow}. Với mọi object: đọc bytes một lần, băm `sha1("<type> <size>\0" + bytes)` = OID ⇒ mới dùng; **mọi cạnh**
   (entry của tree: mode/tên/OID; header `tree`/`parent` của commit) trích từ **bytes đã xác minh** của object cha —
   không `merge-base`, không revision walker, không `ls-tree` để suy cạnh; ancestry S→H = tự đi đồ thị parent từ H tới S
   với visited-set + trần độ sâu (chạm trần ⇒ 12). Memoize theo `(type, OID)` trong một snapshot. Lời khai "sổ vắng"
   chỉ hợp lệ khi tree cha **đã xác minh** không có entry `thu-hoi`. Lệch/thiếu/kiểu sai/rc≠0 ⇒ 12. Vì repo tạm không có
   ref, `refs/replace` của kho nguồn **không thể** áp — no-replace là dây đai thứ hai, băm là dây đai thứ ba; cả ba là
   chốt riêng, có seam riêng trong catalog A6. Chi phí theo số object reachable (reviewer đo scan lease: 1186 object,
   4 311 029 B; ancestry S→H 9 commit; closure toàn mirror 2622 commit) — đặt trần fail-close, đo ở A6.
6. Nạp sổ một lần; áp theo `lease_id` cho **MỌI** cặp; in `<hạn> · ĐÃ_THU_HỒI`; `MAP_REF`; `MÙ 0` + số ref. Mọi lệnh
   (`check`, `ai-dang-giu`, `body`, `kiem-github`, `kiem-thu-hoi-github`, guard packet_loop) dùng chung hàm trạng thái.
7. Chi phí: một lời gọi Git mạng (`ls-remote --symref` qua adapter); chi phí cấu hình adapter/đọc cây/closure đo riêng ở
   A6, không lấy "+0 lời gọi" làm bằng chứng thời gian.

### Q5 — Việc còn dở của lease bị thu hồi

`ls-remote --heads origin 'refs/heads/agent/wp461*'` ⇒ RỖNG **[API]** — chỉ chứng minh không có ref khớp mẫu. §4/ADR-0028:
worker cũ không heartbeat/push/handoff; `stale`; không tự cherry-pick. Ba mức răng:

1. **`packet_loop.py` (M7):** guard `_kiem_thu_hoi(root, target_lease_id, snapshot)` ở **5** cửa TRƯỚC thay đổi bền (đo:
   `record-post`/`transition`/`record-review` gọi helper **0** lần). `record-lease` truyền **ID ứng viên** đã validate
   (state `awaiting_lease`, `lease: null`); bốn cửa kia lấy từ `state.lease`. Snapshot = **cùng adapter Q4** (Git, không
   REST): adapter hỏng ⇒ `KHÔNG ĐO ĐƯỢC` ⇒ `RC_STATE`, state không đổi (fail-close; **không có đệm offline**). REST 403
   nhưng Git hợp lệ ⇒ đi tiếp (số lời gọi REST = 0). Thu hồi ⇒ `stale` + history `lease_revoked_seen{lease_id,
   oid_canonical, blob, snapshot_ts}` (idempotent; ở `record-lease` không ghi `record_lease`), lưu xong mới `RC_STATE`.
   Cờ `False` ⇒ guard cũng ở chế độ dự báo (không đổi verdict), trừ "sổ không rỗng ⇒ chặn".
2. **Lease mới (M3):** `check` từ chối khi còn người giữ — ảnh chụp.
3. **Land** — nợ `LAND-DOC-SO-THU-HOI`, ngoài write set.

### Q6 — Danh sách lịch sử, mốc, cutover, di trú

- **Mốc** = OID canonical **readback SAU khi A0 land** (không nhúng được vào chính A0). A1 ghi `MOC_BIA_MO_LICH_SU` và
  `BIA_MO_LICH_SU` = tuple `(cũ, mới, blob cũ, blob mới)` dẫn xuất từ **đúng cây mốc**, kiểm hai chiều/ID/tên, kèm băm
  biểu diễn sắp thứ tự. Không lấy HEAD lúc A1, merge-base trôi, hay cây ứng viên. Ca dẫn xuất chạy trên hai cây (mốc có
  X→Y; cây sau thêm Z→W): `check W thay Z` ⇒ 8; mutant đọc cây sau ⇒ 0 ⇒ ĐỎ. Feature tomb không bổ sung lịch sử.
- Cặp lịch sử áp theo `lease_id` toàn kho; chuỗi/vòng hữu hạn; mâu thuẫn ⇒ 12; sổ > lịch sử; chiều ngược chặn cả hai.
- **Cutover phân loại delta (R8), không đòi "= 0":** đo cũ/mới trên **cùng map/clock**, holder + eligibility, từng
  ID/path + nguyên nhân. (a) thêm holder / từ được sang bị chặn = delta **bảo thủ**, nhận khi lane bị ảnh hưởng đã dừng
  và có expiry/xử lý đo được; (b) mất holder / mở lại quyền chỉ khi có nguồn Q2 hoặc cặp lịch sử đúng mốc, audit riêng;
  (c) không giải thích được ⇒ **không kích hoạt**. Kế hoạch tách "eligibility tạm chặn trước C" khỏi "sau C"; C không
  phải điều kiện của A1. Đo `b416830` (14:33Z): gate lane luật cũ giữ {r4}, luật mới giữ {r1,r2,r3,r4}, `check r4` 8
  (delta bảo thủ, lane #463 phải dừng hoặc chờ hết hạn **đo được**: 10:17:12Z 08-09); g2 eligibility 0→8 (cần C).
- **g2 hết hạn 09:52:00Z 08-09, trước gate cuối** ⇒ đích cấp lại g2 **không bền**. **C = thu hồi r2 KHÔNG đích**
  (`cap_lai_cho: null`); cấp lại cho wp461 = **lease generation mới** (g3) trong ops PR riêng **sau** kích hoạt, theo
  Q11; không gia hạn/tái dùng ID. Smoke: in **tập thật** (sau C: wp461 holder = ∅ nếu g2 hết hạn, = {g2} nếu còn).
- Di trú (đo 14:33Z, đo lại lúc cấp lease): r2 → C; #456 **HẾT_HẠN**; g2/gate-r4 không đụng; lane gate xử theo cutover.

## `write_set` — theo slice (Q7)

| slice | đường dẫn | nội dung | ước dòng thêm |
|---|---|---|---|
| **A0** | `ops/lease_publish.py` · `ops/lease_publish_test.py` · `.github/workflows/ops-thu-hoi-admission.yml` (MỚI) | M1–M4, M6, **M9 ở chế độ chưa kích hoạt**; adapter Q4; hàm dự báo; `SO_THU_HOI_KICH_HOAT = False`; checker đòi sổ rỗng ở S và T | 560–780 |
| **A1** | `ops/lease_publish.py` · `ops/lease_publish_test.py` · `.github/workflows/ops-thu-hoi-admission.yml` | ghim `MOC_BIA_MO_LICH_SU` + `BIA_MO_LICH_SU` từ receipt A0; nghiệm thu wiring thật; đổi cờ `True` khi Q10 đạt; sổ vẫn rỗng | 90–160 |
| **B** | `.claude/dev/packet_loop.py` · `.claude/dev/packet_loop_test.py` | M7–M8 | 160–240 |
| **C** | `ops/thu-hoi/wp461-be-mat-thu-hai-cua-codex-exec-1r2-claude-20260907.yaml` | M5 (không đích) sau Q8/Q10/Q11 | ~15 |

Tổng ước **825–1195**; `ops-publish-lease.yml` không đụng. ADR-0044: A0 vượt dòng ⇒ ngoại lệ có phạm vi (adapter +
validator + workflow + ca fail-close/mutant, không phải "≈30 ca"); A1/B/C không vượt. Mốc neo: PR #250 +409 SPEC; #275
+368; #248 +328. `numstat` từng slice trước review.

**Bootstrap có biên thẩm quyền riêng (R3):** PR A0 không thể được kiểm bởi workflow của chính nó. Lần land A0: chủ kho
audit exact S/H/tree (sổ rỗng ở cả S lẫn cây sẽ nhận) + review/gate hiện có; điều phối **giữ đóng cập nhật canonical**
từ lúc land A0 → cấu hình required check → readback lượt chạy đầu từ mã A0. Từ đó workflow canonical chạy M4 chế độ chưa
kích hoạt: S hoặc T có bản ghi ⇒ 12, rỗng ⇒ receipt — **bất kể** PR xoá test/wrapper/workflow. Bản ghi lọt trước kích
hoạt ⇒ dừng, phục hồi có audit, không grandfather. CI lane PR (`chay_lease_publish_test.sh`) chỉ là hồi quy, không là
thẩm quyền. **Audit bootstrap ghi bền** trong Packet Issue A0 (comment chủ kho) + journal: object ID/băm, exact S/H/tree
sẽ nhận, catalog ca độc lập (A12), khoảng giữ đóng, OID A0 sau land, cấu hình required check đã readback, run đầu từ A0
được consumer xác minh — chỉ mở lại cập nhật canonical sau receipt ấy.

## `ngoai_pham_vi`

| thứ | vì sao |
|---|---|
| Tạo policy closure §5 / cổng phái sinh tổng quát | nợ #473; kích hoạt cần **policy hợp lệ HOẶC descriptor ngoại lệ Q13** (không đòi cả hai); không miễn nghĩa vụ điền/xác minh phái sinh |
| ADR "nguồn tin cậy cho cổng đọc" | hình dạng đã chạm **5** lần (lượt 5: S1 miền giá trị/profile, S2 cạnh đồ thị/object-store) ⇒ theo chính r4/r5: **`blocked`, ADR trước**. r6 đóng bằng profile digest ghim + object-store cô lập + cạnh từ bytes; hợp đồng Q4.1/Q4.5 là hạt ADR — chủ kho quyết ADR + trần mới |
| Bước đọc receipt M9 trong `land-packets` | dependency `LAND-DOC-RECEIPT-THU-HOI`, phải land trước kích hoạt (S5) |
| Fencing máy; `land-packets` đọc sổ | Q11; nợ `LAND-DOC-SO-THU-HOI` |
| Sửa `ops-publish-lease.yml` · xoá nhánh cũ · `timeout-minutes` · `CHANGELOG.md` · chữ ký `web-flow` · di trú #456 · ruleset ngoài kho | như r3 |
| Cấp lại cho wp461 (lease g3) | ops PR riêng sau kích hoạt, theo Q11; không thuộc C |

## `muc_tieu`

| # | mục tiêu | slice |
|---|---|---|
| **M1** | Lược đồ + parser bản ghi (hợp đồng r3 giữ nguyên); nạp sổ theo OID thô; ba trạng thái; hằng `KHO_CANONICAL`, `SO_THU_HOI_KICH_HOAT` | A0 |
| **M2** | `ai-dang-giu` qua adapter Q4; áp sổ theo `lease_id`; `MAP_REF`; `--nhanh-mac-dinh`; `--du-bao`; cờ `False` + sổ không rỗng ⇒ 12 | A0 |
| **M3** | `check`: chưa kích hoạt = luật cũ + dự báo; đã kích hoạt = precedence/chiều ngược/độc quyền theo closure + symlink; CLI đòi đã publish; hàm thuần | A0 (dự báo) / A1 (bật) |
| **M4** | `kiem-thu-hoi-github <H-sha40> --canonical-base <S-sha40> --nhanh-mac-dinh <tên>`: ancestry S→H (thô), T = tree(H), map path→(mode, type, blob), M1 toàn namespace T, readback Q2 mọi bản ghi mới, receipt S/H/T/OID bộ kiểm; chế độ chưa kích hoạt đòi S, T rỗng | A0 |
| **M5** | Bản ghi thu hồi r2, `cap_lai_cho: null` | C |
| **M6** | Ca + đột biến A1–A9, A11–A12 | A0/A1 |
| **M7/M8** | Guard 5 cửa + A10 | B |
| **M9** | Workflow `ops-thu-hoi-admission.yml` — hợp đồng dưới; cài ở A0 (chưa kích hoạt), nghiệm thu + kích hoạt ở A1 | A0/A1 |

**Hợp đồng M9 (R5):**
- `pull_request_target` cho PR có base = nhánh mặc định, types `opened/reopened/synchronize/ready_for_review/edited`;
  **không** lọc path/author/nguồn nhánh/`rc=9`. `workflow_dispatch` với input PR number, expected S, expected H; ref
  định nghĩa phải là canonical.
- Định nghĩa workflow và mã chạy từ nguồn canonical: checkout **exact S** = canonical head Q4 vừa xác minh (không
  `base.ref` trôi); `base.sha` của event lệch S ⇒ 12 + chạy lại. Không checkout/chạy mã/hook/action của cây ứng viên.
- H = `head.sha` trong event (PR number integer dương, readback PR); `git fetch <endpoint> refs/pull/<n>/head` vào ref
  tạm, OID nhận **== H** (khác ⇒ 12, receipt stale). T = tree(H). Giá trị đi qua đối số/env đã kiểm, không nội suy vào
  shell.
- Chọn **strict up-to-date tại merge** (S là tổ tiên H; merge giữ tree H): receipt ghi S/H/T, phân biệt merge commit M;
  land đối chiếu current base == S và tree(M) == T; base/head đổi ⇒ receipt stale, chạy lại (không áp ngoại lệ drift
  §5.1). Merge queue **chưa hỗ trợ** ⇒ chặn tới khi có lane `merge_group`.
- `permissions`: `contents: read`, `pull-requests: read`, `issues: write` (chỉ bước chiếu receipt).
- **Publisher/consumer (S5):** publisher = **check-run** do GitHub Actions tạo cho job `thu-hoi` của chính workflow này
  (với `pull_request_target`, check-run gắn với **H** — suy từ phép đo trên `duyet-khac-danh-tinh.yml`: check-run `cong`
  id `101767296495` dưới head `1ebd86e` của PR #475; **phải đo lại** trên chính workflow này ở A1, kể cả raw `head_sha`
  của run). **Kênh receipt = workflow artifact** `thu-hoi-receipt-<H>.json` (`actions/upload-artifact`, readback qua API
  `list_workflow_run_artifacts`/download) — KHÔNG dùng `$GITHUB_STEP_SUMMARY` làm kênh thẩm quyền (nó không phải
  `output.summary` của Checks API; chưa có readback). Receipt: `run_id`/`run_attempt`/`check_run_id`, repository, PR,
  S/H/T, **OID commit chứa định nghĩa workflow** (= S) + sha256 blob workflow, OID mã A0 đã chạy, profile digest adapter,
  kết luận. **Join độc lập** (consumer tự làm, không tin thân receipt): check-run(name=`thu-hoi`, head_sha=H, app=GitHub
  Actions) → `run_id` → run(`head_sha`==H, `path`==`.github/workflows/ops-thu-hoi-admission.yml`, event ∈ {pull_request_target})
  → artifact cùng run → receipt.S == canonical lúc chạy, receipt.T == tree(H). `workflow_dispatch` **không tạo pass** (H không
  gắn check-run) — chỉ dùng chẩn đoán. Consumer: (i) branch protection required check `thu-hoi` (Q10, ngoài kho);
  (ii) bước đọc receipt trong `land-packets` — **dependency có tên** `LAND-DOC-RECEIPT-THU-HOI`, ngoài write set, phải land
  trước kích hoạt. Ca âm: check thuộc S / sai app / sai path workflow / H cũ / artifact thiếu ⇒ không pass. Comment chiếu
  chỉ là projection.
- Kích hoạt (A1) chỉ sau Q10.

**Lược đồ bản ghi (M1)** giữ nguyên r3 (hợp đồng parser, thứ tự lỗi, append-only map path→(mode, type, blob), M1 toàn
namespace T, S ở cha thứ hai giữ entry ⇒ 0 / mất ⇒ 8, không `git log --diff-filter`).

## `nghiem_thu`

Kho giả = bare + working copy; adapter/danh tính/danh sách lịch sử tiêm qua API nội bộ; clock cố định. Mỗi tiêu chí nêu
phép đo làm nó ĐỎ.

**A1** — X 3 blob/≥4 ref, một blob ngoài `blob_da_biet_luc_ghi`; sau bản ghi (sổ đã kích hoạt): holder {Y}, **3** dòng
`CÒN_HẠN · ĐÃ_THU_HỒI`, `MAP_REF` đủ. ĐỎ: bỏ nạp sổ; áp theo known-list; bỏ dòng in. Smoke kho thật sau C: in **tập
thật** (∅ nếu g2 hết hạn; {g2} nếu còn); land không giết lease.
**A2** — 1 cặp/3 ref; sổ ở feature ⇒ holder có X; máy chủ `main`/`master`; symref cục bộ giả ⇒ không đổi; symref máy chủ
vắng ⇒ 12; **kho khác cùng heads/SHA/symref nhưng sai danh tính ⇒ 12; `remote.origin.vcs`/insteadOf/đổi config giữa hai
lời gọi ⇒ không đổi được nguồn (adapter không đọc config kho)**; profile transport chưa xác minh ⇒ 12, profile hợp lệ
⇒ control xanh. ĐỎ: nạp mọi ref; đọc symref cục bộ; fallback; dùng `get-url` làm bằng chứng; discovery qua `origin`.
**A3** — 5 mã như r3 + ca danh sách đóng hai cây (mốc X→Y, sau Z→W ⇒ `check W` 8; mutant đọc cây sau ⇒ 0 ⇒ ĐỎ). **Chế độ
chưa kích hoạt**: verdict = luật cũ, `DU_BAO:` in luật mới; mutant gắn luật mới vào verdict sớm ⇒ ĐỎ.
**A4** — chiều ngược hai nguồn; đối chứng sống 0.
**A5** — W giữ p ⇒ 11 (có/không thay thế; exact/prefix/case-fold; alias symlink; **cùng blob lease ở hai OID có đích
alias khác ⇒ giữ cả hai nguồn**; vòng/ngoài/thiếu ⇒ 12); **`effective_write_set: []` tự khai ⇒ 8** (cả phía Y lẫn W).
**Ba nhánh nguồn closure (S4), fixture riêng từng nhánh:** (1) policy fixture hợp lệ `SKILL.md → GOTCHAS.md`, hai raw set
rời nhau nhưng closure giao ⇒ **11**; (2) policy vắng + descriptor Q13 hợp lệ: hai raw set rời, không symlink giao ⇒
**0** (control của ngoại lệ); cùng `docs/a.md` ⇒ **11**; (3) policy vắng, không descriptor, đã kích hoạt ⇒ **12**; policy
có mà hỏng ⇒ **12**. Chưa kích hoạt: mọi nhánh chỉ là `DU_BAO`. Hàm thuần 0/0; CLI trước publish 12; sau publish đồng
thời ⇒ 11/11. ĐỎ: bỏ bước chuẩn hoá; tin tự khai; CLI không so (blob, path); nhánh (2) trả 12 hoặc nhánh (3) trả 0.
**A6** — `b` cùng tên SHA cũ ⇒ 12; đổi ref sau so ⇒ kết quả không đổi; recapture ⇒ ĐỎ. **Toàn vẹn object (S2/S3):**
(i) fixture cache có blob mà bytes băm ≠ OID (điều phối dựng) ⇒ **12**; (ii) `refs/replace` trong kho nguồn cho OID
canonical ⇒ **verdict KHÔNG đổi** (repo tạm không có ref ⇒ đọc object gốc; băm khớp) — không đòi 12, không có detector
presence riêng; (iii) tree cha thiếu entry ⇒ "sổ vắng" chỉ khi tree đã xác minh; (iv) repo tạm thiếu `GIT_OBJECT_DIRECTORY`
⇒ `missing` ⇒ 12. **Catalog mutant ghi SEAM + chốt còn nguyên, không hứa kill vô điều kiện:** bỏ `GIT_OBJECT_DIRECTORY`
routing ⇒ (iv) ĐỎ; bỏ băm ⇒ (i) ĐỎ (không còn lớp nào che ở seam đọc bytes); bỏ riêng env no-replace / cờ / cả hai ⇒
**sống** (repo tạm không ref); bỏ profile digest ⇒ ca S1 (giá trị ngoài profile, cùng tập tên biến) ĐỎ; control sạch ⇒ 0.
Hồ sơ adapter (S1): profile digest khớp mỏ neo ⇒ 0; cùng tập tên biến nhưng giá trị ngoài miền ⇒ 12; helper/CA/executable
ngoài mỏ neo ⇒ 12 (ca âm do điều phối dựng). Chi phí (kể cả băm + đi đồ thị): xen kẽ 3 lượt, trung vị, tỷ lệ ≤ 2, raw
giây/byte/lệnh/số object.
**A7** — ma trận M1 như r3 + `120000` 12 + sổ không rỗng khi cờ `False` ⇒ 12 (consumer vận hành) + JSON envelope 12 /
JSON lệnh 8. `raise`→`continue` so verdict thật. Nới allowlist ⇒ ca đích ĐỎ.
**A8** — như r3, cộng: **mutant "chỉ validate phần thêm" SỐNG dưới ca mode** (map tuple chặn trước) — ghi là mutant sống,
không nhận công; mutant **kết hợp** (map chỉ blob + chỉ validate phần thêm) ⇒ lọt mode ⇒ ĐỎ; unit riêng gọi thẳng
validator toàn T với entry lỗi. Thêm: base trôi / fetch H ≠ event / sai tree / sai OID bộ kiểm ⇒ mất pass; control strict
up-to-date cùng tree ⇒ xanh.
**A9** — như r3; sau canonical: 0 lời gọi thêm.
**A10** — 5 cửa × {sống, thu hồi, không đo được, sổ ở ref khác}; `record-lease` ID ứng viên; REST 403 + Git hợp lệ ⇒ đi
tiếp; Git không đo được ⇒ chặn, state byte-match.
**A11** — hai vế một lệnh, delta theo tên; nền `lease_publish` 121/121 (wrapper; 120/121 thiếu actionlint), `packet_loop`
278/278 + 81 mutant. **A0**: checker từ canonical A0 trên PR rỗng ⇒ receipt; PR thêm bản ghi ⇒ 12; thêm bản ghi + xoá
test/wrapper/workflow ⇒ vẫn 12 (workflow canonical, không phải mã PR). **A1**: `actionlint` + `shellcheck` rc=0; ma trận
wiring trích thân bước (S chưa có lệnh ⇒ 12; S = A0 ⇒ chạy); PR thường/integration/docs-only/bot/`rc=9`/bản ghi độc lập
⇒ đều có lượt; drift/dispatch thiếu input/retarget/skipped/not-created/sai SHA/queue ⇒ không pass; **phải có receipt
Actions thật**; `doc-claims-check --strict` rc=0 + `ok:true`; `doctrine-scan --path` ⇒ 0.
**A12** — biên nhận đủ trường; **catalog ca kỳ vọng neo độc lập với cây PR**; mutant xoá cả đăng ký lẫn lời gọi không
được làm mẫu số nhỏ đi; mutant sống ghi sống kèm lý do.

## `hinh_dang_ke_thua` (L4)

| hình dạng | số lần | nguồn |
|---|---|---|
| "thu hồi là dữ liệu ghi vào bản sao" | 2 | §1 |
| "lời khai hội tụ rộng hơn phép đo" | 3 | g2, lượt 1 |
| "hai cổng bất đồng" | 1 | #473 |
| **"nguồn được tin mà chưa xác minh"** (symref cục bộ · `origin` bất kỳ · config/helper/replace · env tiến trình/bytes cache · miền giá trị config/cạnh đồ thị) | **5** | lượt 1, 2, 3, 4b, 5 (R1/R2/S1/S2) |

Hình dạng thứ tư chạm **4** — r4 đã tuyên bố "lượt 4 còn tìm ra ⇒ dừng packet, ADR riêng". r5 thực hiện đúng một nửa,
nói thẳng: (a) S1/S2 là hai lớp **còn lại** của cùng biên (tiến trình và bytes), r5 đóng bằng hồ sơ tiến trình tường minh
và băm lại nội dung — hai lớp này là **tận cùng** của chuỗi (không còn lớp nào giữa bytes đã băm và OID); (b) toàn bộ hợp
đồng nguồn ở Q4.1/Q4.5 được giữ tự đủ để một ADR "nguồn tin cậy cho cổng đọc" kế thừa nguyên văn (ghi ở `ngoai_pham_vi`);
(c) **lượt 5 ĐÃ tìm ra lần thứ 5** (S1 miền giá trị/profile; S2 cạnh đồ thị) ⇒ theo đúng luật đã khai: packet
**`blocked`** cho tới khi có ADR "nguồn tin cậy cho cổng đọc"; r6 vá theo hint lượt 5 để ADR có hạt đầy đủ, **không** tự
khai đã đóng.

## `chua_do_duoc`

1. Ranh giới chủ kho / agent-cầm-PAT; chữ ký `web-flow` — như r3.
2. Kích thước — ước; `numstat` từng slice.
3. Required check / ruleset / bypass / direct push / strict up-to-date / merge queue — ngoài kho, chưa đo ⇒ cờ `False`.
4. `actions/checkout` exact S + fetch H trong `pull_request_target` nạp đủ heads cho Q4 — nghiệm thu A1.
5. Transport/proxy thật của executor với adapter — đo profile hợp lệ ở A1/B; REST 403 không suy Git hỏng.
6. Object Q8 — chưa tồn tại (nay là lệnh **không đích**).
7. Mốc A0 / `BIA_MO_LICH_SU` — readback sau A0.
8. Codex `Connection refused` — chưa gặp qua 3 lượt.
9. **Ca âm S1/S2** (env bẩn, executable giả, bytes cache lệch OID) — thuộc lớp reviewer bị cấm tự soạn; **điều phối dựng**
   ở A0, chưa có.
10. **Check-run của workflow mới gắn với H** — suy từ phép đo trên `duyet-khac-danh-tinh.yml` (cùng event); phải đo lại
    trên chính `ops-thu-hoi-admission.yml` ở A1.

## 4. Câu chủ kho phải chốt (mỗi câu có khuyến nghị)

❓ **Q7 — packaging/ngoại lệ ADR-0044.** ➡️ A0 → A1 → B → C, spec/Issue/lease/acceptance riêng; A0 gồm workflow; ngoại lệ
dòng cho A0; biên bootstrap A0 do chủ kho audit.
❓ **Q8 — lệnh thu hồi r2.** ➡️ Chủ kho đăng lên #461 khối `lease_revocation_authorization` với `cap_lai_cho: null`. Cấp
lại wp461 = lease g3 riêng sau kích hoạt (Q11), không qua C.
❓ **Q9 — nhận bản ghi cho lease hết hạn?** ➡️ Nhận; `HẾT_HẠN · ĐÃ_THU_HỒI`; không gỡ event, không tái dùng ID.
❓ **Q10 — kích hoạt sổ.** ➡️ Bắt buộc, đo bằng facts: (a) workflow/checker A0 canonical, neo mã/transport/mốc readback;
(b) required check có provenance S/H/T, skipped/not-created/sai SHA không pass; (c) strict up-to-date + merge giữ tree +
chặn direct push/bypass trên nhánh canonical và các đường mã thẩm quyền; (d) wiring thật gồm drift/dispatch/retarget;
(e) policy/closure hợp lệ (Q13); (f) kế hoạch delta Q6 chủ kho readback, lane bị chặn đã dừng; (g) sổ rỗng ở S và A1.
Thiếu ⇒ cờ `False`.
❓ **Q11 — gỡ quyền worker cũ, cấp lại.** ➡️ (1) C land qua M9; (2) chủ kho xác nhận worker cũ dừng + giữ last SHA/state;
(3) lease g3 mới `check` trên ảnh chụp mới, land, readback `NGƯỜI_GIỮ 1`; (4) mới bắt đầu. KHÔNG "rc=0 là khoá".
❓ **Q12 — ready từng slice.** ➡️ Issue + `spec_hash`/revision/generation; phái sinh do dispatcher dẫn xuất (không kế
thừa miễn trừ `b416830`); **descriptor nguồn closure** có tag = `change_policy_sha: <sha256 policy>` (khi policy hợp lệ) HOẶC
`change_policy_sha: null` + descriptor ngoại lệ Q13 (khi vắng) — một trong hai, đóng băng trong `spec_hash`; không giả SHA
của policy chưa tồn tại; base đã nhận slice trước; hợp đồng adapter (hồ sơ tiến trình)/toàn
vẹn object/nguồn symlink/danh sách lịch sử/bootstrap/publisher-consumer M9 trước ready A0. Thiếu hợp đồng ⇒ `proposed`;
thiếu facts ⇒ chưa kích hoạt.
✅ **Q13 — closure khi policy chưa có — ĐÃ CHỐT (comment `5575587924` trên PR #475):** lối (ii) — ngoại lệ có phạm vi:
cho tới khi policy canonical `.github/coordination/change-impact.v1.json` tồn tại, closure = tập khai báo + giải symlink
theo cây OID, KHÔNG nhận `effective_write_set` tự khai; ngoại lệ phải được ghi vào Packet Issue và `spec_hash` của A1.
Hệ quả cho Q3: nhánh "policy vắng ⇒ 12" đổi thành "policy vắng ⇒ dùng ngoại lệ Q13 (có neo) ⇒ closure = khai báo + symlink";
không có neo ⇒ 12. Lối (i) (#473 land trước A1) không chọn.
✅ **Q14 — trần review (R10) — ĐÃ CHỐT:** comment `5575587924` trên PR #475: phạm vi = review đặc tả này; **trần 6
lượt**; dừng khi hết P1 hoặc chạm 6 ⇒ checkpoint kế, không tự nới. Lượt 4 phóng trên bản này.
