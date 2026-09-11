# ĐẶC TẢ PACKET — `THU-HOI-LEASE-VA-CAP-LAI`, **revision 4**

```yaml
packet_id: THU-HOI-LEASE-VA-CAP-LAI
packet_issue: CHƯA CÓ          # điền khi đăng Packet Issue; spec đóng băng TRƯỚC Issue
revision: 4
thay_the: ef9b3700514921d4cabe95947f86937fc36f4aecf2f4e2e39587cafe88a9bb20   # sha256 r3, review lượt 3
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
| 3 | r3 `ef9b3700…` | codex `gpt-6-astra` xhigh | xem biên nhận | `changes_requested` — N: 6 ĐÓNG/3 một phần/2 sai; lượt 1: 7 ĐÓNG/7 một phần; mới **9 P1 + 1 P2** (R1–R10); băm ở commit r4 |

**R10 — trần review §12 KHÔNG có ngoại lệ cho "review đặc tả".** r3 §0 suy một ngoại lệ từ nhãn "spec trước Issue" —
reviewer đối chiếu `docs/PROTOCOL_DA_PHIEN.md:806–816` và §8:579: trần **hai** lượt codex tính **theo PR**, đổi
prompt/phiên không reset, chạm trần ⇒ Review Rescue Checkpoint. r4 rút câu ấy. Trạng thái đúng: PR #475 đã dùng **3**
lượt; lượt 2–3 chạy theo chỉ thị trực tiếp của chủ kho trong phiên (*"hãy lặp … cho tới khi hết P1"*) — chỉ thị ấy có
hiệu lực cho các lượt đã chạy, **không** là neo bền cho lượt kế tiếp. **Checkpoint của r4:** (a) quyết định = **thiết kế
lại** (r4 là sản phẩm: adapter nguồn, bootstrap có biên riêng, C không đích); (b) trần mới **đã được chủ kho chốt và neo**:
comment `https://github.com/ducthangho/tra-luat/pull/475#issuecomment-5575587924` (tài khoản chủ kho, ghi hộ theo chỉ thị
trong phiên, đã readback): **trần 6 lượt** cho PR #475; dừng khi hết P1 hoặc chạm 6 ⇒ checkpoint kế; (c) mọi bộ đếm/ID
finding giữ nguyên, tách slice không reset. Comment ấy KHÔNG cấp lease, KHÔNG kích hoạt sổ.

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
- Tập so = closure bắc cầu tính từ `write_set` khai báo theo **policy canonical đã ghim** (`change_policy_sha` trong
  spec/lease theo §3.2); `effective_write_set` trong YAML lease **không được dùng** để thu hẹp — có mặt thì phải **bằng
  tập** closure tính lại, lệch ⇒ 8, vắng thì không sao. Raw set phải ⊆ closure. Thiếu policy/provenance để tính ⇒ 12,
  **không** fallback raw tự do. Đo: `.github/coordination/change-impact.v1.json` và
  `.github/coordination/schemas/change-impact.v1.schema.json` **vắng** (`schemas/` chỉ có `review_verdict.v1.schema.json`)
  ⇒ áp **ngoại lệ Q13 đã chốt** (comment `5575587924`): closure = tập khai báo + giải symlink theo cây OID; ngoại lệ
  ghi vào Packet Issue + `spec_hash` A1; không có neo ⇒ 12.
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

1. **Adapter nguồn (R1):** danh tính ghim trong mã `KHO_CANONICAL = "github.com/ducthangho/tra-luat"`; endpoint
   discovery = `https://` + `KHO_CANONICAL` (**URL tường minh**, không bao giờ là tên `origin`). Lời gọi discovery chạy
   trong **thư mục git rỗng cô lập** (`git init` tạm) với `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL=/dev/null`,
   `-c protocol.allow=never -c protocol.https.allow=always`, TLS mặc định (không `sslVerify=false`, không cờ bỏ kiểm);
   credential/proxy chỉ từ **môi trường triển khai tin cậy** (`GIT_CONFIG_COUNT`/`GIT_CONFIG_KEY_*`, `HTTPS_PROXY` +
   CA bundle) — readback mapping tới `KHO_CANONICAL` trước khi tin. `ls-remote --get-url origin` chỉ là **chẩn đoán**.
   `remote.<x>.vcs`, `url.*.insteadOf`, `include.path`, remote helper trong config ứng viên **không chạm** được adapter.
   Profile transport không đo được ⇒ 12. Fixture: test tiêm endpoint (đường dẫn bare) qua **API nội bộ**; không có biến
   môi trường/cờ production đổi authority.
2. **Chụp map cục bộ TRƯỚC:** `refs/heads/*` và `refs/remotes/origin/*` → map tên→OID một lần; tách map remote-tracking
   (đối chiếu máy chủ) khỏi local heads (chỉ THÊM người giữ). Giữ map cùng mọi occurrence ref của từng cặp.
3. **Một lời gọi discovery:** adapter `git ls-remote --symref <endpoint> HEAD 'refs/heads/*'` → nhánh mặc định máy chủ
   khai + `(tên, SHA40)`. Workflow truyền `--nhanh-mac-dinh`; phải bằng symref; lệch/vắng/mơ hồ ⇒ 12. Không fallback.
4. **So:** mọi tên máy chủ có trong map remote-tracking với **cùng SHA40** (thiếu/lệch ⇒ 12 nêu tên + hai SHA); local
   heads không bù. **OID canonical = OID nhánh mặc định trong advertisement đã so**; HEAD OID phải khớp. **Không chụp lại.**
5. **Đọc theo OID thô (R2):** mọi `ls-tree`/`cat-file`/ancestry/diff chạy với `GIT_NO_REPLACE_OBJECTS=1`
   (và `--no-replace-objects`); phát hiện `refs/replace/*` hoặc `replace.refBase`/graft trong kho đọc ⇒ chẩn đoán, và
   kết quả phải **bằng** cây thô; không cô lập được ⇒ 12. "Cùng SHA ký tự" chưa chứng minh cùng cây. Thiếu object / rc≠0
   / output hỏng ⇒ 12; chỉ kết luận "sổ vắng" khi đọc thành công cây chứa nó. Một timestamp snapshot cho mọi consumer.
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
thẩm quyền.

## `ngoai_pham_vi`

| thứ | vì sao |
|---|---|
| Tạo policy closure §5 / cổng phái sinh tổng quát | nợ #473; là **dependency của kích hoạt** (Q3/Q13), không miễn nghĩa vụ điền/xác minh phái sinh |
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
- `permissions`: `contents: read`, `pull-requests: read`, `issues: write` (chỉ bước chiếu receipt). Required check phải
  có provenance đúng H/T + OID workflow/mã; comment hoặc check trùng tên không đủ.
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
alias khác ⇒ giữ cả hai nguồn**; vòng/ngoài/thiếu ⇒ 12); **`effective_write_set: []` tự khai ⇒ 8** (cả phía Y lẫn W);
raw thiếu companion theo closure ⇒ 11; policy vắng ⇒ 12 (kích hoạt) / dự báo (chưa). Hàm thuần 0/0; CLI trước publish
12; sau publish đồng thời ⇒ 11/11. ĐỎ: bỏ bước chuẩn hoá; tin tự khai; CLI không so (blob, path).
**A6** — `b` cùng tên SHA cũ ⇒ 12; đổi ref sau so ⇒ kết quả không đổi; recapture ⇒ ĐỎ; **`refs/replace` cho OID
canonical ⇒ cây thô hoặc 12; mutant bỏ `GIT_NO_REPLACE_OBJECTS` ⇒ đọc bản ghi giả ⇒ ĐỎ**. Chi phí: xen kẽ 3 lượt, trung
vị, tỷ lệ ≤ 2, raw giây/byte/lệnh.
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
| **"nguồn được tin mà chưa xác minh"** (symref cục bộ · `origin` bất kỳ · config/helper/replace) | **3** | lượt 1, 2, 3 (R1/R2) |

Hình dạng thứ tư chạm **3** ⇒ §12 đòi xem lại cách làm: r4 **đổi thiết kế** — đọc nguồn qua adapter cô lập khỏi mọi
config runtime, object qua DAG thô; không vá thêm phép so nào nữa. Nếu lượt 4 còn tìm ra hình dạng này ⇒ dừng packet,
đưa "nguồn tin cậy cho cổng đọc" thành ADR riêng.

## `chua_do_duoc`

1. Ranh giới chủ kho / agent-cầm-PAT; chữ ký `web-flow` — như r3.
2. Kích thước — ước; `numstat` từng slice.
3. Required check / ruleset / bypass / direct push / strict up-to-date / merge queue — ngoài kho, chưa đo ⇒ cờ `False`.
4. `actions/checkout` exact S + fetch H trong `pull_request_target` nạp đủ heads cho Q4 — nghiệm thu A1.
5. Transport/proxy thật của executor với adapter — đo profile hợp lệ ở A1/B; REST 403 không suy Git hỏng.
6. Object Q8 — chưa tồn tại (nay là lệnh **không đích**).
7. Mốc A0 / `BIA_MO_LICH_SU` — readback sau A0.
8. Codex `Connection refused` — chưa gặp qua 3 lượt.
9. **Phần cuối verdict lượt 3** (A1–A12, bảng đo lại, `chua_do_duoc` của reviewer) — đọc sau khi lượt kết thúc; r4
   dựng từ R1–R10 + hint đầy đủ.

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
❓ **Q12 — ready từng slice.** ➡️ Issue + `spec_hash`/revision/generation; phái sinh + policy SHA do dispatcher dẫn xuất
(không kế thừa miễn trừ `b416830`); base đã nhận slice trước; hợp đồng adapter/nguồn symlink/danh sách lịch sử/bootstrap
trước ready A0. Thiếu hợp đồng ⇒ `proposed`; thiếu facts ⇒ chưa kích hoạt.
✅ **Q13 — closure khi policy chưa có — ĐÃ CHỐT (comment `5575587924` trên PR #475):** lối (ii) — ngoại lệ có phạm vi:
cho tới khi policy canonical `.github/coordination/change-impact.v1.json` tồn tại, closure = tập khai báo + giải symlink
theo cây OID, KHÔNG nhận `effective_write_set` tự khai; ngoại lệ phải được ghi vào Packet Issue và `spec_hash` của A1.
Hệ quả cho Q3: nhánh "policy vắng ⇒ 12" đổi thành "policy vắng ⇒ dùng ngoại lệ Q13 (có neo) ⇒ closure = khai báo + symlink";
không có neo ⇒ 12. Lối (i) (#473 land trước A1) không chọn.
✅ **Q14 — trần review (R10) — ĐÃ CHỐT:** comment `5575587924` trên PR #475: phạm vi = review đặc tả này; **trần 6
lượt**; dừng khi hết P1 hoặc chạm 6 ⇒ checkpoint kế, không tự nới. Lượt 4 phóng trên bản này.
