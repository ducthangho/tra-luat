# ĐẶC TẢ PACKET — `THU-HOI-LEASE-VA-CAP-LAI`, **revision 8** (vá S1/S3/S5/S6/S7/S8/S9 theo lượt 6 = lời gọi 7; CHƯA được review — lời gọi 8 sẽ đọc bản này)

```yaml
packet_id: THU-HOI-LEASE-VA-CAP-LAI
packet_issue: CHƯA CÓ          # KHÔNG đăng: còn P1 chưa được reviewer xác nhận đóng (§3.2/§12)
revision: 8
thay_the: 6a0ea66b8e9a53b5be8f3df0ed6e79a9ef5f217ac86e161004fb306ee6845aae   # sha256 r7 (kế toán; kỹ thuật = r6)
thay_the_r6: f78135cff428f0744476d7f27426f459d926578c4bac4a4339928330c4a0d6a5   # bản lượt 6 (lời gọi 7) đã đọc
thay_the_r5: 23a7deaf60af17aea2fa3b027d08fb8c187b6f03499f34540822ab7b9c3b1672
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
| 6 | r6 `f78135cf…` | codex `gpt-6-astra` xhigh, **lời gọi 7** (trần mới `5578460203`), harness dựng lại từ đầu (scratch lượt 1–5 mất theo container) | VERDICT `9090aadd…` · HINT `47fbf8cb…` (7 hunk) · 2889,1 s · stdout 85 B · stderr 4 049 518 B · rc=0 | `changes_requested` — **S2, S4 ĐÓNG**; còn **3 P1** (S1 một phần — nền thực thi/trust chưa duyệt độc lập; S3 một phần — A6 hứa kill ở ca bị lớp khác che; **S7 mới** — tệp retired xung đột schema M1) + **3 P2** (S5, S6 một phần; **S8 mới** — layout/ngân sách object-store) + P3 S9 (kế toán) |

**R10 — trần review §12 KHÔNG có ngoại lệ cho "review đặc tả".** r3 §0 suy một ngoại lệ từ nhãn "spec trước Issue" —
reviewer đối chiếu `docs/PROTOCOL_DA_PHIEN.md:806–816` và §8:579: trần **hai** lượt codex tính **theo PR**, đổi
prompt/phiên không reset, chạm trần ⇒ Review Rescue Checkpoint. r4 rút câu ấy. Trần 6 (comment `5575587924`) đã dùng hết
ở lượt 5 (3 lượt + 4a chết + 4b + 5) ⇒ checkpoint `5576397733` (packet `blocked`, chờ ADR). **Checkpoint thứ hai — quyết định
chủ kho 08-09-2026, comment `5578460203`:** reroute của human theo §12 — tiếp tục vòng vá/review **tới hết P1**, không đặt
trần số, **bộ đếm KHÔNG reset** (lời gọi kế = 7), ID finding giữ nguyên; hết P1 ⇒ Packet Issue rồi DỪNG xin lease; không sửa
mã khi chưa có lease. Chủ kho cũng duyệt **soạn ADR-0047** (`docs/adr/0047-nguon-tin-cay-cho-cong-doc-lease.md`, Proposed,
cùng PR) — xem `ngoai_pham_vi`. Lượt 2–3 chạy theo chỉ thị trực tiếp trong phiên; từ lượt 4 có neo bền. **Checkpoint của r4:** (a) quyết định = **thiết kế
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

### 0.3 Delta r5 → r6 theo finding lượt 5

| finding (P) | r5 thiếu | r6 làm gì |
|---|---|---|
| S1 (P1, nguồn tin cậy) | allowlist `credential.*`/`http.*` theo tên + dò chuỗi trong giá trị (không phải validator Git: `http.sslVerify=false` là boolean, `http.proxy` là endpoint); receipt chỉ ghi TẬP TÊN biến | Q4.1: allowlist **hữu hạn khoá + kiểu + miền giá trị**; **profile digest** (băm của cấu hình không bí mật + định danh helper/CA/executable) so với **mỏ neo đã duyệt ghim trong mã**; khác ⇒ 12 |
| S2 (P1, nguồn tin cậy) | băm blob nhưng chưa ràng buộc CẠNH (tree trung gian, parent) và repo tạm không có object (`cat-file` trả `missing`) | Q4.5: **API object-store**: `GIT_DIR` = repo tạm cô lập + `GIT_OBJECT_DIRECTORY` = objects của kho nguồn (chỉ đọc); mọi cạnh trích từ **bytes đã xác minh** (entry tree, header parent), tự đi đồ thị, memoize `(type, OID)`; không `merge-base`/walker |
| S3 (P1, ĐÓNG SAI) | A6 đòi `refs/replace` ⇒ 12 dù no-replace đọc object gốc (băm khớp); hứa mutant bỏ 3 lớp "đọc giả" dù profile còn chặn | A6: replacement ⇒ verdict **không đổi** (đọc gốc); ca riêng bytes lệch OID ⇒ 12; catalog ghi **seam** + chốt còn nguyên, không hứa kill vô điều kiện |
| S5 (P2) | `GITHUB_STEP_SUMMARY` ≠ `output.summary` của Checks API (chưa readback); dispatch H không tự gắn check-run; join provenance | M9: receipt = **workflow artifact** `thu-hoi-receipt-<H>` (readback qua API artifacts); join độc lập check-run → run → artifact → định nghĩa workflow tại S; dispatch **không** tạo pass; consumer = bước trong `land-packets` (dependency, ngoài write set) |
| S6 (P2) | ai produce/verify descriptor; sự kiện policy xuất hiện rồi biến mất (A→B→D) bị đọc current-only bỏ lỡ | Q13: descriptor = comment chủ kho + **hằng ghim trong mã A1** (ID + băm thân); retirement = tệp append-only `ops/thu-hoi/_ngoai-le-closure.retired.yaml` do **M9 ép** (T có policy mà thiếu tệp ⇒ 12); tệp ở lại vĩnh viễn ⇒ không hồi sinh |

### 0.4 Delta r6 → r8 theo finding lượt 6 (chưa review; r7 chỉ là kế toán)

| finding (P) | r6 thiếu | r8 làm gì |
|---|---|---|
| S1 (P1, nguồn tin cậy — lần **6**) | digest băm executable Git + tên helper + tệp CA: tên helper không định danh bytes chương trình, `sslCAPath` là thư mục, runtime/transport HTTPS ngoài digest; chưa nói ai sản xuất/duyệt mỏ neo | Q4.1: **deployment profile = nền thực thi được duyệt** (manifest image/runtime bất biến: Git, helper HTTPS/credential thật, runtime, trust store đầy đủ, endpoint/proxy); producer độc lập caller; approver = chủ kho qua commit review; **một** phép so profile duy nhất; đường tạm không vào digest; ADR-0047 lớp 2 cập nhật cùng |
| S3 (P1, tiêu chí) | A6 hứa kill ở ca (iv) và ca "ngoài miền" — hai ca này mutant SỐNG vì validator miền/đầu vào thiếu đã 12 sẵn; dòng 221 tạo phép so profile thứ hai che mutant bỏ digest | A6: catalog theo seam — ca **positive** routing 0 giết mutant bỏ routing; ca **trong miền nhưng khác neo** giết mutant bỏ phép so profile; ca băm ghi seam **sau cat-file, trước kiểm OID**; mutant sống ghi sống kèm chốt che; A12 không nhận công lỗi hạ tầng trước seam |
| S5 (P2) | mũi tên check-run → `run_id` chưa có khoá API; `workflow_dispatch` vẫn trong workflow required; retention/attempt/quyền đọc chưa chốt; thứ tự bootstrap vs dependency consumer | M9: bỏ `workflow_dispatch` khỏi workflow required; join qua `check_suite.id` → runs → attempt jobs (`check_run_url`) → artifacts theo ID; artifact `thu-hoi-receipt-<H>-<attempt>` đúng một `receipt.json`, `if-no-files-found: error`; canary thật S≠H ở A0; consumer `LAND-DOC-RECEIPT-THU-HOI` land **trước cửa sổ bootstrap A0** |
| S6 (P2) | descriptor chưa bind activation context; marker retired ghi `oid_T` tự tham chiếu; rollback/policy đổi sau retirement chưa nói | Q3: hằng ghim thêm `repository` + `het_hieu_luc`; receipt A1 + Issue ghim `{packet_id, revision, generation, spec_hash, descriptor_sha256}`; marker ghi policy **đầu tiên** + `base_sha_before_add = S`, không `oid_T`; B(P1)→B2(P2) qua binding mới; B→D (policy vắng) M9 từ chối 12 |
| **S7** (P1 mới, không phải nguồn tin cậy) | M1 bắt **mọi** tệp `ops/thu-hoi/` là bản ghi `lease_revoked` ⇒ tệp retired của r6 bị M1 từ chối, thiếu tệp thì Q13 từ chối: PR policy đầu tiên không có biểu diễn hợp lệ | Q3/M1/M4: **đúng một path reserved** `_ngoai-le-closure.retired.yaml` phân tuyến sang schema metadata riêng (`event: closure_exception_retired`, 6 khoá, regular `100644`); mọi path khác vẫn M1; metadata không đếm là thu hồi, không đi Q2; "sổ rỗng" = tập revocation rỗng; A7/A8 thêm ca |
| **S8** (P2 mới) | `GIT_OBJECT_DIRECTORY=<kho>/.git/objects` literal sai với bare/linked worktree; alternates/pack/partial/shallow chưa nói; trần chi phí không đơn vị | Q4.5: giải gitdir/common dir bằng API Git một lần; hỗ trợ loose+pack+alternates do adapter dựng; partial thiếu object ⇒ 12 (không "sổ vắng"); shallow ⇒ 12; chuẩn bị/fetch trước snapshot rồi chụp lại map; **ngân sách có đơn vị** (8 trần, giá trị mặc định là ĐỀ XUẤT phải đo ở A0) |
| S9 (P3) | kế toán trần cũ | r7 đã sửa §0/Q14/`ngoai_pham_vi`; r8 sửa nốt `hinh_dang_ke_thua` |

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
| **Đo lại L5 — reviewer lượt 6, map 310 ref, 03:12Z 08-09** | ref **310** = 309 máy chủ + 1 cục bộ (306 tip khác nhau); cặp/đường/lease_id/đa-blob **288/273/273/7** (không đổi); CÒN_HẠN/chưa bia mộ **6/3** (r1 wp461 hết 03:05Z); r2 `26f07b4` nay trên **9 ref** (cũ 4 — nhánh spec + các nhánh land), `fdfde3a` 1 ref; #456 `8b2103c` **14 ref** / `1f95042` **5 ref**; `da_bi_thay_the` tại base `b416830` / H `02b0b86` / master `585c7d5` = **7 / 11 / 11** (#468 đã vào master ở `802fc01`); scan lease + absence **1204 object · 4 350 922 B**; closure parent **2658 commit**; witness S→H **9 commit / 8 cạnh**. Số ref/blob trôi vì nhánh mới xuất hiện — **không** đổi bất biến, chỉ chứng minh L5 |

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
  ⇒ nhánh (2) áp khi kích hoạt. **Descriptor Q13 (S6) và metadata retirement (S7):** producer = chủ kho hoặc người
  được uỷ quyền bền, có phạm vi; nguồn = comment PR #475 `5575587924`, thân UTF-8 đã readback. Hằng
  `NGOAI_LE_CLOSURE` trong mã canonical A1 ghim `{repository, object_id, body_sha256, owner, pham_vi,
  het_hieu_luc: "lần đầu policy hợp lệ được canonical nhận"}`. Receipt kích hoạt và Packet Issue A1 ghim thêm
  `{packet_id, revision, generation, spec_hash, descriptor_sha256}`; verifier đối chiếu cả descriptor với hằng lẫn
  activation context với Issue/receipt đã duyệt. Không tự đăng ký từ descriptor caller gửi. Lease lịch sử không phải
  tự thêm descriptor; ngoại lệ này chỉ cấp nguồn cho phép tính va chạm của checker, không cấp quyền ready packet khác.
  Thiếu binding bắt buộc trước ready/kích hoạt ⇒ chưa qua bước đó; lệch hoặc không xác minh được lúc dùng ⇒ 12.

  **Đúng một path reserved** `ops/thu-hoi/_ngoai-le-closure.retired.yaml` được phân tuyến sang schema metadata riêng,
  không phải bản ghi `lease_revoked`. Chỉ regular blob `100644`; root mapping, cấm khoá trùng, đúng các khoá:
  `{schema_version: 1, event: "closure_exception_retired", descriptor_sha256: <sha256>,
  first_policy_sha256: <sha256>, base_sha_before_add: <SHA40 S>, retired_at_utc: <chuỗi ISO8601 Z>}`.
  Integer không nhận bool; các băm phải đúng định dạng; thời gian không ở tương lai so clock snapshot. Mọi lỗi
  source metadata ⇒ 12; metadata MỚI sai schema/mode ⇒ 12. M4 kiểm map append-only trước validator T: thay
  mode/type/bytes của marker đã có ở S ⇒ 8. Mọi path khác vẫn M1, không bỏ qua prefix `_` hoặc tên gần reserved.
  Metadata không tính vào tập event thu hồi, không đi Q2 như một lease giả; vẫn nằm trong map append-only M4/A8.
  Không lưu `oid_T` của chính cây chứa tệp: H/T của lần tiếp nhận nằm trong workflow receipt/journal ngoài cây.

  **Transition:** khi S chưa có marker và policy vắng, PR đầu tiên đưa policy hợp lệ vào T phải kèm marker; M9
  so `descriptor_sha256` với nguồn đã ghim, `first_policy_sha256` với policy T và `base_sha_before_add == S`.
  Thiếu marker / marker khi chưa có policy hợp lệ / policy hỏng ⇒ 12. PR policy phải có lease/write set bao gồm
  path marker; không âm thầm thêm path vào A1/C. Nếu policy đã canonical trước khi guard A0 được cài mà chưa có
  marker, quay lại revision/bootstrap có audit, không tự grandfather. A0/A1 khi policy vẫn vắng không tạo marker.
  Khi marker đã được canonical nhận: giữ nguyên `(mode,type,blob)` ở mọi T; sửa/xoá ⇒ 8. Marker ghi policy ĐẦU TIÊN,
  không cập nhật hoặc đòi hash ấy bằng mọi policy về sau. Policy hiện tại được kiểm bằng descriptor policy của
  revision hiện tại; đổi closure/check/hash vẫn pause + revision/generation (§5/ADR-0025).
  B(P1,R1)→B2(P2 hợp lệ,R1) có thể qua sau khi binding mới được duyệt. B→D(policy vắng,R1) bị M9 từ chối 12;
  đây là candidate bị chặn, không gọi là chuỗi canonical đã được chấp nhận. Reader nếu thấy D vẫn 12, không hồi sinh
  ngoại lệ. Rollback về một policy hợp lệ trước đó khác với xoá policy về vắng; xoá về vắng không được hỗ trợ dưới
  hợp đồng này. Commit feature có policy rồi bỏ trước khi vào canonical không tự là sự kiện retirement. Không cache.
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
   `GIT_ASKPASS`, `SSH_*`. **Deployment profile là nền thực thi được duyệt (S1), không chỉ băm Git chính.**
   `PROFILE_ADAPTER_DA_DUYET` là tập manifest/digest ghim trong mã canonical, do chủ kho/người có uỷ quyền bền duyệt
   qua commit review. Producer manifest thuộc deployment/bootstrap tin cậy, độc lập caller và cây ứng viên.
   Manifest ghim image/runtime bất biến và tập thực thi/trust hiệu lực: Git chính (đường, sha256, version), transport
   HTTPS helper, credential helper thực sự dùng (identity/đường/sha256 hoặc không dùng), runtime/library manifest,
   CA/trust-store manifest đầy đủ (file, thư mục CA, default system store nếu dùng), endpoint và proxy profile.
   Chỉ tên helper hoặc `git --version` không là identity của chương trình. Không yêu cầu tự băm cả OS: dùng image/
   deployment manifest được xác minh và giữ read-only suốt invocation; không đo từ caller rồi tự thêm vào allowlist.
   Executable giải bằng đường tuyệt đối trong profile trước khi chạy; hash/manifest phải khớp. Helper/trust/runtime
   không định danh được hoặc có thể đổi sau kiểm ⇒ 12. Đổi ubuntu image/runner/package phải qua profile mới nếu
   manifest identity đổi; không tự chấp nhận chỉ vì executable Git chính chưa đổi.

   Chỉ các giá trị không bí mật sau được producer profile cung cấp, parse/chuẩn hoá trước khi dựng argv/env:
   `credential.helper` = không dùng hoặc đúng helper ghim; username chỉ scope URL canonical ghim;
   `http.sslCAInfo`/`http.sslCAPath` chỉ đúng trust store trong manifest; proxy chỉ đúng scheme/host/port/profile
   đã duyệt. Không wildcard `http.*`/`credential.*`, không substring validator. Adapter chuyển cấu hình đã validate
   thành đối số Git hữu hạn, không kế thừa các cặp `GIT_CONFIG_*` caller gửi. Unknown key ⇒ 12; TLS verification
   phải bật; URL rewrite/redirect/resolution ngoài profile và mọi config repo nguồn không được đọc.
   Chọn đúng một cấu hình proxy hiệu lực; nếu có `http.proxy`, `HTTPS_PROXY`, `https_proxy` thì chúng phải quy về
   cùng giá trị ghim, không để precedence tạo một tuyến khác. Profile trước ready phải ghi host/port/scheme cụ thể,
   trust manifest cụ thể và nguồn credential nếu cần; thiếu ⇒ chưa ready cho deployment đó. Không log secret.

   **Digest** = sha256(JSON UTF-8, sort_keys, separators `,`/`:`, schema_version ghim) của manifest + toàn bộ cấu hình
   không bí mật hiệu lực và identity/version nguồn secret. HOME/GIT_DIR tạm và object-store dữ liệu là vai trò do
   adapter tạo/xác định, kiểm isolation/ownership riêng; không đưa đường tạm ngẫu nhiên vào digest deployment.
   Receipt ghi digest, profile ID, image/runtime identity, endpoint và bindings invocation không bí mật.
   Digest phải bằng một neo approved; không tính được/lệch ⇒ 12. Đây là **một** phép so profile duy nhất; câu ghi
   receipt không tạo thêm chốt so profile độc lập để che mutant A6. Validator miền chỉ kiểm key/type/miền an toàn;
   các yêu cầu bằng identity/store/proxy đã ghim được thực hiện trong phép so profile này, không so lần thứ hai.
   Adapter không kế thừa env ambient.
   Lệnh: init repo tạm với `--template=` rồi `git ls-remote --symref <endpoint> HEAD 'refs/heads/*'`,
   `-c protocol.allow=never -c protocol.https.allow=always`; `ls-remote --get-url origin` chỉ là chẩn đoán.
   Fixture tiêm endpoint bare nội bộ/profile trơ qua API test, không có cờ/env production đổi authority. Negative
   source/profile/helper/trust fixtures do điều phối cung cấp theo phân công; control thật của từng runner ở A0/A1.
2. **Chụp map cục bộ TRƯỚC:** `refs/heads/*` và `refs/remotes/origin/*` → map tên→OID một lần; tách map remote-tracking
   (đối chiếu máy chủ) khỏi local heads (chỉ THÊM người giữ). Giữ map cùng mọi occurrence ref của từng cặp.
3. **Một lời gọi discovery:** adapter `git ls-remote --symref <endpoint> HEAD 'refs/heads/*'` → nhánh mặc định máy chủ
   khai + `(tên, SHA40)`. Workflow truyền `--nhanh-mac-dinh`; phải bằng symref; lệch/vắng/mơ hồ ⇒ 12. Không fallback.
4. **So:** mọi tên máy chủ có trong map remote-tracking với **cùng SHA40** (thiếu/lệch ⇒ 12 nêu tên + hai SHA); local
   heads không bù. **OID canonical = OID nhánh mặc định trong advertisement đã so**; HEAD OID phải khớp. **Không chụp lại.**
5. **API object-store đã xác minh (S2 đã sửa identity; S8 chốt vận hành):** Git cache nguồn không tin cậy. Giải
   gitdir/common object directory của đúng source một lần bằng API Git phù hợp bare/working copy/linked worktree;
   không ghép literal `<source>/.git/objects`. Reader dùng `GIT_DIR=<repo tạm cô lập>` không ref/config nguồn và
   `GIT_OBJECT_DIRECTORY=<object directory đã giải>` read-only. Không kế thừa `GIT_COMMON_DIR` hoặc env store caller.
   Loose và pack đều được hỗ trợ. Alternate stores chỉ là nguồn bytes cache, không là authority; adapter kiểm danh
   sách/root/độ sâu/quyền đọc trước khi cho reader dùng, kể cả `objects/info/alternates` và alternate bắc cầu Git có
   thể tự đọc. Chỉ `GIT_ALTERNATE_OBJECT_DIRECTORIES` do adapter dựng từ store profile ấy mới được dùng.
   Reader không tự network/lazy-fetch trong snapshot. Shallow ⇒ 12 theo M1. Partial/promisor cache được dùng chỉ
   khi mọi object cần cho quyết định đã có: commit/tree có entry nhưng blob thiếu ⇒ 12, không suy "sổ vắng".
   Chuẩn bị/fetch/unshallow phải thực hiện trước snapshot bằng nguồn hợp lệ; sau đó chụp lại map/clock và so Q4.
   Chi phí chuẩn bị/fetch ghi riêng, không gộp thành claim "một ls-remote". Không dùng config/ref nguồn để lazy-fetch.

   `cat-file --batch` giữ `GIT_NO_REPLACE_OBJECTS=1` và `--no-replace-objects`. Repo tạm thiếu routing trả `missing`
   dù Git rc=0 ⇒ reader12. Roots = {canonical, mọi occurrence ref, S,H, mốc lịch sử, mã A0/workflow}; bao gồm đường
   tới lease/symlink, sổ, metadata reserved, policy/schema và code/workflow thực sự dùng. Với mỗi object, kiểm framing,
   actual type/size, băm `sha1("<actual-type> <size>\0" + bytes)` bằng OID rồi so expected type mới dùng.
   Mọi cạnh tree (mode/tên/OID) và commit (`tree`/`parent`) lấy từ bytes cha đã xác minh; không revision walker,
   merge-base hoặc ls-tree để suy cạnh. Ancestry tự đi parent từ H tới S, visited-set; mọi prerequisite lỗi/thiếu ⇒12.
   Parser dùng chính bytes đã băm, không mở lại. Memoize `(expected_type,OID)` trong snapshot; cache-hit cũng kiểm
   actual type. Cùng OID bị yêu cầu kiểu khác ⇒12. "Sổ vắng" cần chuỗi tree cha đã băm chứng minh entry vắng;
   missing object không phải missing entry. Repo tạm không ref khiến source replacement không áp; no-replace và
   hash là chốt khác với seam riêng, không coi replacement presence tự là lỗi.

   **Budget profile ghim trước ready**, tính cả graph/tree/alias và trước cấp phát. Giá trị dưới đây là **ĐỀ XUẤT của
   reviewer lượt 6, CHƯA đo trên roots thật** — A0 phải đo bound−1/bound/bound+1 trên deployment rồi mới ghim vào profile
   + `spec_hash` (chua_do_duoc 12); không phải số đo. Đề xuất mặc định
   `max_unique_objects=50000`, `max_object_bytes=8388608`, `max_total_object_bytes=134217728`,
   `max_parent_path_edges=10000`, `max_tree_or_alias_edges=128`, `max_alternate_stores=8`,
   `max_alternate_depth=4`, `max_reader_wall_seconds=60`. Số byte là bytes thô sau giải nén; depth là số cạnh;
   objects là `(actual_type,OID)` phân biệt, wall time dùng monotonic deadline cho cả reader/subprocess.
   Vượt bất kỳ trần/timeout/không đo được ⇒12, không cắt graph rồi kết luận vắng. Các giá trị phải được đo trên
   roots thực của deployment và ghi trong profile/spec_hash trước ready; đổi giá trị qua revision/review, không
   caller tự nới. A6 có bound−1/bound/bound+1 và graph rộng/object lớn ở seam, không chỉ depth.
   Số scan cũ1186object/4.311.029B và closure2622commit thuộc map lượt5 chưa được tái lập exact; lượt6 đo map310ref:
   scan+absence1204object/4.350.922B, parent closure2658commit; witness S→H02b0b86 vẫn9commit/8cạnh. Không lấy số
   witness làm số commit phải đọc; thứ tự traversal có thể làm visited khác. Đây không phải benchmark end-to-end.
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
| **A0** | `ops/lease_publish.py` · `ops/lease_publish_test.py` · `.github/workflows/ops-thu-hoi-admission.yml` (MỚI) | M1–M4 gồm schema/guard metadata Q13, M6, **M9 chưa kích hoạt**; adapter/profile Q4; hàm dự báo; `SO_THU_HOI_KICH_HOAT = False`; checker đòi sổ rỗng ở S và T | 560–780 |
| **A1** | `ops/lease_publish.py` · `ops/lease_publish_test.py` · `.github/workflows/ops-thu-hoi-admission.yml` | ghim `MOC_BIA_MO_LICH_SU` + `BIA_MO_LICH_SU` từ receipt A0; nghiệm thu wiring thật; đổi cờ `True` khi Q10 đạt; sổ vẫn rỗng | 90–160 |
| **B** | `.claude/dev/packet_loop.py` · `.claude/dev/packet_loop_test.py` | M7–M8 | 160–240 |
| **C** | `ops/thu-hoi/wp461-be-mat-thu-hai-cua-codex-exec-1r2-claude-20260907.yaml` | M5 (không đích) sau Q8/Q10/Q11 | ~15 |

Tổng ước trước vá lượt 6 **825–1195**; phải ước/đo lại phần profile, metadata và join trước ready, không coi số này là numstat implementation; `ops-publish-lease.yml` không đụng. ADR-0044: A0 vượt dòng ⇒ ngoại lệ có phạm vi (adapter +
validator + workflow + ca fail-close/mutant, không phải "≈30 ca"); A1/B/C không vượt. Mốc neo: PR #250 +409 SPEC; #275
+368; #248 +328. `numstat` từng slice trước review.

**Bootstrap có biên thẩm quyền riêng (R3):** dependency consumer receipt phải land trước cửa sổ này. PR A0 không thể được kiểm bởi workflow của chính nó. Lần land A0: chủ kho
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
| ADR "nguồn tin cậy cho cổng đọc" — **ĐÃ SOẠN**: `ADR-0047` (Proposed, cùng PR #475, dòng §20 PROTOCOL, `adr-song` 47/47) | hình dạng đã chạm **6** lần (lượt 6: S1 nền thực thi/trust chưa duyệt độc lập) ⇒ chủ kho duyệt soạn (08-09-2026, AskUserQuestion trong phiên 2). ADR giữ BẤT BIẾN ba lớp + ba luật; lớp 2 cập nhật theo S1 lượt 6 (nền thực thi được duyệt, producer độc lập, approver). Chi tiết allowlist/manifest/tập gốc object vẫn ở Q4.1/Q4.5 của spec này. **Quyết định còn của chủ kho** (không phải câu chữ spec): nền thực thi cụ thể nào được tin (runner/image) và quy trình duyệt mỏ neo — ghi vào ADR-0047 khi có. Promote `Accepted` = A0 land với A2/A6 đỏ đúng ca — không thuộc write set slice nào |
| Bước đọc receipt M9 trong `land-packets` | dependency `LAND-DOC-RECEIPT-THU-HOI`, phải land **trước cửa sổ bootstrap A0** (S5); kiểm bằng fixture độc lập trước A0, canary thật sau A0 trước mở lại canonical |
| Fencing máy; `land-packets` đọc sổ | Q11; nợ `LAND-DOC-SO-THU-HOI` |
| Sửa `ops-publish-lease.yml` · xoá nhánh cũ · `timeout-minutes` · `CHANGELOG.md` · chữ ký `web-flow` · di trú #456 · ruleset ngoài kho | như r3 |
| Cấp lại cho wp461 (lease g3) | ops PR riêng sau kích hoạt, theo Q11; không thuộc C |

## `muc_tieu`

| # | mục tiêu | slice |
|---|---|---|
| **M1** | Lược đồ + parser revocation r3 và đúng một schema metadata reserved Q13; nạp sổ theo OID thô; ba trạng thái; hằng `KHO_CANONICAL`, `SO_THU_HOI_KICH_HOAT` | A0 |
| **M2** | `ai-dang-giu` qua adapter Q4; áp sổ theo `lease_id`; `MAP_REF`; `--nhanh-mac-dinh`; `--du-bao`; cờ `False` + sổ không rỗng ⇒ 12 | A0 |
| **M3** | `check`: chưa kích hoạt = luật cũ + dự báo; đã kích hoạt = precedence/chiều ngược/độc quyền theo closure + symlink; CLI đòi đã publish; hàm thuần | A0 (dự báo) / A1 (bật) |
| **M4** | `kiem-thu-hoi-github <H-sha40> --canonical-base <S-sha40> --nhanh-mac-dinh <tên>`: ancestry S→H (thô), T = tree(H), map path→(mode, type, blob), phân tuyến schema toàn namespace T; Q2 cho revocation mới, Q13 cho metadata mới; receipt S/H/T/OID bộ kiểm; chế độ chưa kích hoạt đòi S, T rỗng | A0 |
| **M5** | Bản ghi thu hồi r2, `cap_lai_cho: null` | C |
| **M6** | Ca + đột biến A1–A9, A11–A12 | A0/A1 |
| **M7/M8** | Guard 5 cửa + A10 | B |
| **M9** | Workflow `ops-thu-hoi-admission.yml` — hợp đồng dưới; cài ở A0 (chưa kích hoạt), nghiệm thu + kích hoạt ở A1 | A0/A1 |

**Hợp đồng M9 (R5/S5):**
- Workflow admission chỉ có `pull_request_target` cho PR base=default, types
  `opened/reopened/synchronize/ready_for_review/edited`, không lọc path/author/nguồn nhánh/rc9. Không khai
  `workflow_dispatch` trong workflow required này. Chẩn đoán ngoài lane không tạo check `thu-hoi`; consumer từ chối
  event khác kể cả check success/skipped cùng tên. Rerun dùng attempt của event PR đã xác minh.
- Định nghĩa workflow và mã phải từ canonical: đo riêng `workflow_sha`/workflow_ref và OID checkout; cả hai phải
  neo exact S=canonical Q4. `base.sha` event lệch S hoặc chưa chứng minh definition==S ⇒12, receipt stale.
  Không chạy code/hook/action của cây ứng viên. H=`pull_request.head.sha` sau readback PR; fetch endpoint ghim
  `refs/pull/<n>/head` vào store/ref tạm, OID nhận==H; T=tree(H) từ Q4.5. Inputs validate rồi truyền qua argv/env.
- Strict up-to-date: S tổ tiên H, merge giữ tree H. Ngay trước land consumer so current base==S, current PR head==H
  và tree(M)==T; drift ⇒ mất pass/chạy lại. Không áp §5.1; merge queue chưa hỗ trợ⇒chặn.
- Job kiểm `thu-hoi` có quyền đọc cần cho contents/PR/Checks/Actions và không quyền ghi Issue; job projection riêng
  mới có `issues: write`. Consumer land dùng identity/token đọc Checks/Actions đã chốt trong packet dependency.
  Upload artifact dùng cơ chế runtime của Actions; không suy cần `actions: write` chỉ để upload. Mọi quyền/capability
  phải được canary bằng đúng token thực trước kích hoạt; không tự nâng quyền khi API lỗi.
- Receipt là file JSON trong artifact `thu-hoi-receipt-<H>-<run_attempt>`, upload qua action ghim commit đã duyệt,
  `if-no-files-found: error`; chứa đúng một file `receipt.json`. Receipt ghi repository/PR, run_id/run_attempt,
  check_run_id, S/H/T, actual workflow-definition commit+blob sha256, OID mã đã chạy, profile digest và checker rc.
  Kết luận job cuối lấy từ Checks/Actions sau khi job hoàn tất, không tự ghi success thay platform. Upload thất bại
  làm job thất bại. Artifact name không là identity: consumer dùng artifact ID/digest và metadata run sau readback.
- **Join độc lập, không nhận run_id/identity từ thân receipt làm nguồn:** đọc raw check-run theo ID, kiểm tên/app ID/
  conclusion success và quan hệ với H; lấy `check_suite.id`; liệt kê workflow runs theo suite (phân trang), chọn
  đúng workflow ID/path/event/repository; đọc jobs của đúng run attempt, so `check_run_url` với check-run đang xét.
  Không đồng nhất job ID với check-run ID, không parse URL giao diện để tin run_id. Sau đó list/download artifacts
  của run theo ID; yêu cầu đúng attempt/không expired, nội dung và mọi S/H/T/ID/băm khớp facts độc lập.
  Đường API dự kiến: check-runs/{id} → actions/runs?check_suite_id=... →
  actions/runs/{run_id}/attempts/{attempt}/jobs → actions/runs/{run_id}/artifacts → download artifact ID.
  A0 canary phải lưu raw responses để xác nhận các trường/route ấy trên API thật; thiếu/mơ hồ/pagination thiếu⇒12.
  `run.head_sha`, check head_sha, PR H và `workflow_sha` được đo riêng: quan hệ cho event PR phải được chốt bằng
  canary khi S≠H, không suy `run.head_sha==H` từ một check xuất hiện dưới H. Nếu API thực không thể cung cấp association
  mà branch protection/consumer yêu cầu, chưa mở lại canonical/chưa kích hoạt; phải revision publisher, không nới so.
- Artifact retention ghi tường minh theo khả năng repo trước kích hoạt; expired/xoá/thiếu/stale attempt trước land
  ⇒ mất pass và rerun. Không overwrite artifact attempt trước để đổi bằng chứng trong lúc consumer đọc. Khi land,
  journal/Packet Issue có audit lưu receipt hash, artifact ID/digest, joins đã xác minh và S/H/T/M/canonical readback;
  final state hash neo theo ADR-0025/0028. Artifact có hạn không thay journal. Sau canonical, mất artifact không gỡ
  event thu hồi đã được nhận, không bắt lease mới đọc lại căn cứ lịch sử. STEP_SUMMARY/comment thường chỉ projection.
- Required check tên `thu-hoi` là một consumer, không đủ thay land readback. Bước trong `land-packets` thuộc dependency
  `LAND-DOC-RECEIPT-THU-HOI`, ngoài write set, có spec/lease/review/acceptance riêng và **land trước cửa sổ bootstrap A0**.
  Consumer được kiểm bằng fixture độc lập trước A0; canary thật sau A0 trước mở lại canonical. A1 chỉ bật khi Q10 đủ.

**M1/M4:** schema revocation r3 giữ nguyên cho mọi path ngoài **đúng** reserved metadata Q13; reserved có schema và
transition riêng Q13. Validate toàn namespace T bằng dispatcher schema hữu hạn, không bỏ qua entry không hiểu.
Map path→(mode,type,blob) append-only áp cho cả hai loại. Chỉ revocation mới đi Q2; metadata mới đi verifier Q13.
“Sổ rỗng” ở inactive/A0/A1 nghĩa là tập revocation rỗng; metadata vẫn phải được validate và admission theo Q13.
S ở cha2: giữ entry0/mất8; shallow/object thiếu12; không git log --diff-filter. H/T của metadata nằm trong receipt
ngoài cây; không trường nào trong record tự yêu cầu bằng OID của chính commit/tree chứa nó.

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
rời nhau nhưng closure giao ⇒ **11**; fixture tích hợp có metadata retired hợp lệ Q13; (2) policy vắng + descriptor Q13 hợp lệ: hai raw set rời, không symlink giao ⇒
**0** (control của ngoại lệ); cùng `docs/a.md` ⇒ **11**; (3) policy vắng, không descriptor, đã kích hoạt ⇒ **12**; policy
có mà hỏng ⇒ **12**. Chưa kích hoạt: mọi nhánh chỉ là `DU_BAO`. Hàm thuần 0/0; CLI trước publish 12; sau publish đồng
thời ⇒ 11/11. ĐỎ: bỏ bước chuẩn hoá; tin tự khai; CLI không so (blob, path); nhánh (2) trả 12 hoặc nhánh (3) trả 0.
**A6** — `b` cùng tên SHA cũ⇒12; đổi ref sau so không đổi OID/bytes quyết định; recapture bị ca pinning bắt.
Catalog ghi mỗi ca: input, expected, seam, mutant đúng một chốt, mọi chốt còn lại và result/credit:
- Object-store hợp lệ từ repo tạm routed đọc commit/tree/blob⇒0; **ca positive này** giết mutant bỏ routing (12).
  Ca khác cố ý thiếu routing⇒missing/12 dù Git rc0; nó không giết mutant bỏ routing, ghi SỐNG dưới ca ấy.
- Bytes mismatch chỉ do điều phối cung cấp ở seam **sau cat-file response/framing, trước hash** ⇒12 và parser
  nhận 0 byte chưa xác minh. Unit tại seam kiểm cả rc lẫn việc chưa giao bytes cho parser; bỏ hash phải phá
  assertion này. Nếu chỉ so verdict tích hợp thì payload cần hợp lệ ở mọi chốt downstream còn lại; chốt khác
  vẫn trả12 ⇒ mutant SỐNG ở ca tích hợp. Corrupt storage bị Git bắt trước cũng không nhận công hash.
- Source refs/replace ⇒verdict không đổi; bỏ env/cờ/cả hai no-replace vẫn SỐNG khi repo tạm không ref. Không có
  detector presence riêng. Mọi tree/parent/absence assertion lấy từ bytes đã băm; missing object không là absent entry.
- Profile approved⇒0. Ngoài miền key/value⇒12, bỏ digest vẫn SỐNG vì domain validator che. Ca **trong miền** nhưng
  khác approved profile⇒12; bỏ phép so profile duy nhất⇒0 mới ĐỎ. Nếu còn chốt tương đương thì ghi SỐNG, không nhận công.
  Helper/runtime/trust manifest lệch approved⇒12; negative source fixtures theo phân công điều phối, không tự soạn.
- Bare/linked worktree/pack/alternate hợp lệ⇒0; partial thiếu object⇒12, chuẩn bị đầy đủ trước snapshot⇒0;
  shallow⇒12. Bound−1/bound/bound+1 theo từng đơn vị Q4.5, thiếu/timeout⇒12, không cắt graph rồi0.
Chi phí E2E baseline/candidate xen kẽ3cặp cùng ref/map/clock, trung vị tỷ lệ≤2; raw wall seconds, object-body bytes,
output bytes, số lệnh/phân biệt network, unique objects, visited commits và witness length. Benchmark chỉcat-file
hoặc chỉhash không chứng nhận E2E. Ghi cả chuẩn bị cache và profile setup khi chúng có chi phí.
**A7** — ma trận M1 như r3 + `120000` 12 + sổ không rỗng khi cờ `False` ⇒ 12 (consumer vận hành) + JSON envelope 12 /
JSON lệnh 8. Thêm metadata Q13 valid0, thiếu/hỏng/mode sai12; một path khác gần tên reserved vẫn M1; revocation thật khi inactive12. `raise`→`continue` so verdict thật. Nới allowlist ⇒ ca đích ĐỎ.
**A8** — như r3, cộng: **mutant "chỉ validate phần thêm" SỐNG dưới ca mode** (map tuple chặn trước) — ghi là mutant sống,
không nhận công; mutant **kết hợp** (map chỉ blob + chỉ validate phần thêm) ⇒ lọt mode ⇒ ĐỎ; unit riêng gọi thẳng
validator toàn T với entry lỗi. Thêm: base trôi / fetch H ≠ event / sai tree / sai OID bộ kiểm ⇒ mất pass; control strict
up-to-date cùng tree ⇒ xanh. First-policy+metadata hợp lệ0; sửa/xoá marker8; B(P1,R1)→B2(P2 hợp lệ,R1)0 sau binding mới; D(policy vắng,R1)12; không self-pin containing T.
**A9** — như r3; sau canonical: 0 lời gọi thêm.
**A10** — 5 cửa × {sống, thu hồi, không đo được, sổ ở ref khác}; `record-lease` ID ứng viên; REST 403 + Git hợp lệ ⇒ đi
tiếp; Git không đo được ⇒ chặn, state byte-match.
**A11** — hai vế một lệnh, delta theo tên; nền lịch sử lease_publish121/121(wrapper),packet_loop278/278+81mutant
chỉ là mốc, phải đo lại đúng ca/môi trường cho candidate. A0: checker canonical rỗng⇒receipt; thêm revocation dù xoá
test/wrapper/workflow ở PR vẫn12. Consumer dependency fixture đủ trước bootstrap; raw canary của workflow A0 chứng
minh check→suite→run→attempt job→artifact, S≠H, actual workflow_sha/S và token read scopes trước mở canonical.
A1: actionlint+shellcheck0; mọi PR thường/integration/docs/bot/rc9/standalone/retarget đều được admission; drift,
skipped/not-created/sai SHA/queue/missing-or-expired artifact/wrong attempt/wrong app hoặc workflow không pass.
Workflow required không khai dispatch; consumer cũng từ chối dispatch dù có cùng tên/success. Artifact rerun khác
attempt không thay thế identity attempt cũ. **Phải có raw receipt/joins Actions thật**; thiếu⇒False, không lấy model
thay evidence. doc-claims-check --strict rc0+ok:true; doctrine-scan --path có spec⇒0.
**A12** — biên nhận đủ trường; **catalog ca kỳ vọng neo độc lập với cây PR**; mutant xoá cả đăng ký lẫn lời gọi không
được làm mẫu số nhỏ đi; mutant sống ghi sống kèm seam/chốt che theo A6. Lỗi hạ tầng/parser xảy ra trước seam không nhận công mutant; skipped/not_run không là pass.

## `hinh_dang_ke_thua` (L4)

| hình dạng | số lần | nguồn |
|---|---|---|
| "thu hồi là dữ liệu ghi vào bản sao" | 2 | §1 |
| "lời khai hội tụ rộng hơn phép đo" | 3 | g2, lượt 1 |
| "hai cổng bất đồng" | 1 | #473 |
| **"nguồn được tin mà chưa xác minh"** (symref cục bộ · `origin` bất kỳ · config/helper/replace · env tiến trình/bytes cache · miền giá trị config/cạnh đồ thị · **nền thực thi/trust store phía sau executable**) | **6** | lượt 1, 2, 3, 4b, 5, 6 (R1/R2/S1/S2; lượt 6 chỉ còn S1) |

Hình dạng thứ tư chạm **4** — r4 đã tuyên bố "lượt 4 còn tìm ra ⇒ dừng packet, ADR riêng". r5 thực hiện đúng một nửa,
nói thẳng: (a) S1/S2 là hai lớp **còn lại** của cùng biên (tiến trình và bytes), r5 đóng bằng hồ sơ tiến trình tường minh
và băm lại nội dung — hai lớp này là **tận cùng** của chuỗi (không còn lớp nào giữa bytes đã băm và OID); (b) toàn bộ hợp
đồng nguồn ở Q4.1/Q4.5 được giữ tự đủ để một ADR "nguồn tin cậy cho cổng đọc" kế thừa nguyên văn (ghi ở `ngoai_pham_vi`);
(c) **lượt 5 ĐÃ tìm ra lần thứ 5** (S1 miền giá trị/profile; S2 cạnh đồ thị) ⇒ packet `blocked` (checkpoint `5576397733`);
(d) chủ kho reroute (`5578460203`) và duyệt **ADR-0047**; **lượt 6 tìm ra lần thứ 6** — chỉ còn S1 (S2 ĐÓNG): lớp bị bỏ sót là
*nền thực thi phía sau executable* (helper HTTPS/runtime/trust store) và *ai sản xuất/duyệt mỏ neo*. r8 đóng bằng deployment
profile được duyệt (Q4.1) và ghi vào ADR-0047 lớp 2; câu "tận cùng" của r5 là lời khai lịch sử đã bị review bác, không dùng
làm chứng minh. Phần còn mở của S1 sau r8 là **quyết định quản trị** (nền nào, ai duyệt) — ghi ở `ngoai_pham_vi`, chờ chủ kho.

## `chua_do_duoc`

1. Ranh giới chủ kho / agent-cầm-PAT; chữ ký `web-flow` — như r3.
2. Kích thước — ước; `numstat` từng slice.
3. Required check / ruleset / bypass / direct push / strict up-to-date / merge queue — ngoài kho, chưa đo ⇒ cờ `False`.
4. `actions/checkout` exact S + fetch H trong `pull_request_target` nạp đủ heads cho Q4 — nghiệm thu A1.
5. Transport/proxy thật của executor với adapter — đo profile hợp lệ ở A1/B; REST 403 không suy Git hỏng.
6. Object Q8 — chưa tồn tại (nay là lệnh **không đích**).
7. Mốc A0 / `BIA_MO_LICH_SU` — readback sau A0.
8. Codex `Connection refused` — chưa gặp qua 6 lượt (lời gọi 1–7); nguyên nhân nếu gặp: chưa biết, không đổ cho proxy.
   Lượt 6: `CODEX_AUTH_JSON` là ảnh chụp 36 h vẫn chạy trọn; ảnh chụp cũ hơn có thể bị `refresh_token_invalidated`.
9. **Ca âm S1/S2** (env bẩn, executable giả, bytes cache lệch OID) — thuộc lớp reviewer bị cấm tự soạn; **điều phối dựng**
   ở A0, chưa có.
10. **Check-run của workflow mới gắn với H** — suy từ phép đo trên `duyet-khac-danh-tinh.yml` (cùng event); phải đo lại
    trên chính `ops-thu-hoi-admission.yml` ở A0 canary (raw check-run/run/attempt/artifact, S≠H); `run.head_sha == H` và
    `workflow_sha == S` là **giả thuyết** cho tới khi có raw response.
11. **Nền thực thi được duyệt (S1)** — giá trị thật của deployment profile (image/runtime, helper, trust store, proxy
    host/port/scheme, CA) và người duyệt mỏ neo `PROFILE_ADAPTER_DA_DUYET`: chưa có; là quyết định chủ kho + đo ở A0.
12. **Ngân sách object-store (S8)** — 8 trần ở Q4.5 là giá trị ĐỀ XUẤT, chưa đo trên roots thật; đo ở A0 rồi ghim vào
    profile/`spec_hash` trước ready.
13. **Scratch reviewer lượt 1–5** đã mất theo container; số cũ (1186 object · 4 311 029 B · 2622 commit) không tái lập
    exact — lượt 6 đo map mới (1204 · 4 350 922 B · 2658), không kết luận số cũ sai.

## 4. Câu chủ kho phải chốt (mỗi câu có khuyến nghị)

❓ **Q7 — packaging/ngoại lệ ADR-0044.** ➡️ A0 → A1 → B → C, spec/Issue/lease/acceptance riêng; A0 gồm workflow; ngoại lệ
dòng cho A0; biên bootstrap A0 do chủ kho audit; consumer `LAND-DOC-RECEIPT-THU-HOI` land **trước cửa sổ bootstrap**,
không chờ A1 mới bắt đầu dependency.
❓ **Q8 — lệnh thu hồi r2.** ➡️ Chủ kho đăng lên #461 khối `lease_revocation_authorization` với `cap_lai_cho: null`. Cấp
lại wp461 = lease g3 riêng sau kích hoạt (Q11), không qua C.
❓ **Q9 — nhận bản ghi cho lease hết hạn?** ➡️ Nhận; `HẾT_HẠN · ĐÃ_THU_HỒI`; không gỡ event, không tái dùng ID.
❓ **Q10 — kích hoạt sổ.** ➡️ Bắt buộc, đo bằng facts: (a) workflow/checker A0 canonical và actual definition/code == S;
(b) deployment profile (image/runtime/helper/trust/proxy) đã được duyệt và chạy thật trên runner; (c) consumer dependency đã
canonical; join check-run → suite → run → attempt job → artifact canary bằng đúng token, ca S≠H; (d) required check `thu-hoi`
có provenance S/H/T + strict up-to-date + tree(M)==T + chặn direct push/bypass; merge queue chưa hỗ trợ ⇒ chặn; (e) wiring
thật gồm drift/retarget, skipped/not-created/sai SHA/sai attempt/artifact thiếu không pass; (f) nguồn closure Q13 có binding
hợp lệ, marker retired nếu policy đã xuất hiện; (g) kế hoạch delta Q6 chủ kho readback, lane bị chặn đã dừng; (h) tập
revocation rỗng ở S và A1; (i) artifact retention + journal/readback sau land đã chốt. Thiếu ⇒ cờ `False`.
❓ **Q11 — gỡ quyền worker cũ, cấp lại.** ➡️ (1) C land qua M9; (2) chủ kho xác nhận worker cũ dừng + giữ last SHA/state;
(3) lease g3 mới `check` trên ảnh chụp mới, land, readback `NGƯỜI_GIỮ 1`; (4) mới bắt đầu. KHÔNG "rc=0 là khoá".
❓ **Q12 — ready từng slice.** ➡️ Issue + `spec_hash`/revision/generation; phái sinh do producer/dispatcher được uỷ quyền dẫn
xuất (không kế thừa miễn trừ `b416830`); **descriptor nguồn closure** = `change_policy_sha: <sha256 policy>` (khi policy hợp
lệ) HOẶC `change_policy_sha: null` + descriptor ngoại lệ Q13 — một trong hai, đóng băng trong `spec_hash`; không giả SHA của
policy chưa tồn tại; base đã nhận slice trước và mã canonical nơi M9 đòi. **Trước ready A0 đóng băng:** hợp đồng deployment
profile (producer/approver/manifest bất biến/serialization), object-store layout + availability + ngân sách có đơn vị,
M1/reserved metadata/Q13 transitions, danh sách lịch sử/bootstrap, publisher/consumer API + retention + dependency. Giá trị
profile, ngân sách và activation binding phải được **điền ở đúng slice** trước ready/kích hoạt — executor không tự mặc định
nguồn, không tự nới trần. Thiếu hợp đồng ⇒ `proposed`; thiếu facts rollout ⇒ chưa kích hoạt.
✅ **Q13 — closure khi policy chưa có — ĐÃ CHỐT (comment `5575587924` trên PR #475):** lối (ii) — ngoại lệ có phạm vi:
cho tới khi policy canonical `.github/coordination/change-impact.v1.json` tồn tại, closure = tập khai báo + giải symlink
theo cây OID, KHÔNG nhận `effective_write_set` tự khai; ngoại lệ phải được ghi vào Packet Issue và `spec_hash` của A1.
Hệ quả cho Q3: nhánh "policy vắng ⇒ 12" đổi thành "policy vắng ⇒ dùng ngoại lệ Q13 (có neo) ⇒ closure = khai báo + symlink";
không có neo ⇒ 12. Descriptor/binding A1 và sự kiện retirement theo Q3 (S6/S7): chỉ miễn **phép va chạm** của checker, không
miễn phái sinh/ready packet khác; hết ở lần đầu policy hợp lệ được canonical nhận, không hồi sinh khi policy mất; marker
bất biến ghi policy **đầu tiên**, policy hiện tại đi binding mới; rollback về vắng ⇒ 12, rollback về policy hợp lệ đi quy
trình policy/revision/generation. Lối (i) (#473 land trước A1) không chọn, không hỏi lại.
✅ **Q14 — trần review (R10) — ĐÃ CHỐT hai lần:** (1) comment `5575587924`: trần 6 lời gọi — đã dùng hết ở lượt 5 (kế toán:
lời gọi 1–6 = lượt 1, 2, 3, 4a chết, 4b, 5); (2) comment `5578460203` (08-09-2026, checkpoint thứ hai): **tới hết P1**, bộ đếm
không reset, lời gọi 7 = lượt 6 trên r6. Còn P1 sau một lượt ⇒ vá rồi gọi tiếp; **không** tự đặt trần số, không tự dừng.
