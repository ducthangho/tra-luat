# Đặc tả packet `K3-CONNECTOR-STATE` r1: K3 của `kiem-merge` nhận khối `codex-review-state` neo đúng head

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab
dieu_kien_merge: ADR-0060@36d7c5dcdcbbb27176b75135125b9009f9fe0587

| trường | giá trị |
|---|---|
| packet_id | `K3-CONNECTOR-STATE`, revision 1, generation 1 |
| packet_issue | #1211 |
| nguon_cap_viec | chủ kho `ducthangho` duyệt mở packet ngày 05-11-2026, qua phiên điều phối `session_015GtxrYPjZCTZeRiazdssgq`. Căn cứ: K3 đỏ trên PR #1200 (packet #1196) dù connector đã báo sạch trên đúng head |
| trạng thái | `proposed`. Bản r1 áp các khuyến nghị ở §7. Chủ kho trả lời khác ở câu nào thì soạn r2, không sửa đè r1 |
| review_class | `sensitive`: sửa cổng `.claude/dev/packet_loop.py` (`docs/PROTOCOL_DA_PHIEN.md` §20) |
| base | `origin/master` lúc cấp lease, và **phải sau** merge của PR #1194 (§3.1). Lúc soạn (05-11 04:5xZ) master là `bbfb460` |
| executor / reviewer | theo §7 Q7 |
| windows | `required` (ADR-0060 M3 bước 2: diff chạm `.claude/dev/**`) |
| full_mutant_audit | bắt buộc (ADR-0060 M9: diff chạm `.claude/dev/**`) |

## 1. Vì sao: số đo

Mọi số đo ở mục này lấy bằng REST GET (`urllib`, `GITHUB_PAT`, trạng thái 200 kèm `X-GitHub-*`) trong khung
05-11-2026 04:40Z–04:55Z. Phạm vi là 1000 issue comment mới nhất của kho, comment cũ nhất tạo lúc `2026-10-30T09:45:18Z`.

### 1.1 Hai hình dạng kết luận sạch

| # | hình dạng | ví dụ readback | đặc điểm |
|---|---|---|---|
| H1 | issue comment chứa `<!-- codex-review-receipt:v1 -->` và dòng `**Reviewed commit:** \`<sha10>\`` | #1204 comment 6649724305 (`d2064d95c0`), #1199 comment 6648151590 | mỗi lượt review là một comment MỚI, không sửa lại (`updated_at` = `created_at`) |
| H2 | issue comment `<!-- codex-pull-request-review-summary -->` chứa `<!-- codex-review-state:v1 {json} -->` | #1200 comment 6649440969; #1201 comment 6648733704; #1149 comment 6649466132; #1148 comment 6649465839 | **một** comment mỗi PR, connector **sửa đè tại chỗ** (`updated_at` > `created_at`), chỉ phản ánh lượt review mới nhất |

JSON của H2 trên #1200, nguyên văn:
`{"code_review":{"commit_sha":"ec805d8c1ab322cd049d74822a3972425809cf93","has_any_findings":false,"has_unresolved_findings":false,"status":"completed"},"security_review":{"commit_sha":null,"has_any_findings":null,"has_unresolved_findings":null,"status":null}}`

Trên 4 PR được giao đo (#1200, #1201, #1149, #1148), mỗi PR có đúng một comment của connector: một H2, `completed`/`false`/`false`,
neo đúng head, trigger `Draft marked ready`. **0** comment H1, **0** review, **0** review comment của connector.

### 1.2 Miền giá trị của H2 (126 comment H2 của connector, 125 PR)

| đại lượng | số đo |
|---|---|
| bộ `(status, has_any_findings, has_unresolved_findings)` | `completed,false,false` 113 · `completed,true,true` 7 · `failed,true,true` 4 · `running,null,null` 2. Chưa thấy `has_any_findings` khác `has_unresolved_findings` |
| khoá JSON | luôn đúng `{code_review, security_review}`; `code_review` luôn đúng 4 khoá trên; `security_review` luôn toàn `null` |
| `commit_sha` | luôn 40 hex |
| danh tính | cả 126 comment: `login` `chatgpt-codex-connector[bot]`, `user.id` 199175422, `user.type` `Bot`, `performed_via_github_app.slug` `chatgpt-codex-connector` |
| comment H2 mỗi PR | 124 PR có 1; **#1071 có 2** trên cùng head `0104461`: 6541910865 `running`/`null` (không sửa lại từ 09:52:37Z) và 6541910927 `completed`/`false` |
| H2 đứng `running` cũ | #1100: H2 6553110441 đứng `running`, trong khi có H1 6553184640 tạo sau |
| `failed` | #1167, #1168, #1169, #1171: `failed,true,true` kèm comment "You have reached your Codex usage limits", **không** có finding thật |
| người khác chép khối H2 | 2 comment của `ducthangho` (#1196, #1175) chứa chuỗi `codex-review-state`. Đây là phản chứng tự nhiên cho allow-list danh tính |

### 1.3 Khi nào thiếu H1 (113 trạng thái H2 sạch-hoàn-tất)

| trigger trong bảng của H2 | có H1 cùng SHA | không có H1 |
|---|---|---|
| `Manual request` (`@codex review`) | 30 | 0 |
| `Draft marked ready` | 29 | 53 |
| `PR opened` | 0 | 1 |

Riêng 05-11-2026 có 9 PR `Draft marked ready` sạch mà không có H1: #1148 #1149 #1188 #1191 #1197 #1200 #1201 #1203 #1209.

### 1.4 Hình dạng khi có finding

Cả 11 trạng thái `has_any_findings: true` đều có review (`COMMENTED`) của connector. Riêng 7 ca `completed` còn có review comment
mang badge. Ví dụ:
- #1194: review 5779358121 `commit_id` `29ee9ca7` = head, review comment 4476177126 `original_commit_id` = head, `![P2 Badge]`.
- #1175: review 5779897524, ba review comment `original_commit_id` = head `8e15b928`, `![P2 Badge]`.
- #1204: P1 4476535747 có `original_commit_id` `2dd75dfe` nhưng `commit_id` `abd0d413`, tức GitHub đã dời `commit_id`.
  H2 trên head mới `d2064d95` lại báo `has_any_findings: false`. Hệ quả: `has_any_findings` chỉ nói về **lượt mới nhất**, không nói về PR.

### 1.5 Mã K3 hiện hành (`bbfb460`)

- `.claude/dev/packet_loop.py` `_neo_connector`: issue comment chỉ được neo qua `Reviewed commit:`. Không có dòng đó thì trả `None`.
- `_doc_connector`: "xong" khi có một issue comment `hien`, hoặc một review `hien` ở trạng thái `APPROVED`/`COMMENTED`/`CHANGES_REQUESTED`.
  Ngoài hai đường đó thì `_die("connector chưa xong …")`. Danh tính chỉ so `user.login == BOT_CONNECTOR`.
- Ba nơi gọi `_doc_connector`: `accept` (dòng ~2921), `mo-lai` (~2977), `kiem-merge` K3 (~3267).

### 1.6 Phân loại các điều kiện đỏ trên PR #1200

| điều kiện | đo | phân loại |
|---|---|---|
| K3 | H2 sạch đúng head; không H1; không `@codex review` nào trên PR (issue comment chỉ có human audit và H2) | **Đúng theo chữ ADR-0060 M6** (*"dòng `Reviewed commit:` cho đúng SHA"*, lượt C1 gọi bằng `@codex review` khi còn draft). **Đỏ oan theo ý định**: connector đã review sạch đúng head. Packet này xử lý |
| K6, K7 | head `ec805d8` là commit merge (cha `5ca9cdbf` + master `f2e33bc`). Diff hai chấm `4d258cc..ec805d8` dài **168 tệp**, chạm `.github/workflows/**` ⇒ `_phan_loai_windows` = `required`, `_cham_m9` = `True`. Cùng hàm với base `f2e33bc` (= merge-base với master trước lúc merge) ⇒ **1 tệp**, `not_required`, `False` | **Đỏ oan do chọn base**: `kiem-merge` lấy `--base` của người gọi. Sau khi master được merge vào nhánh, base của lease không còn là điểm rẽ, nên diff kéo theo thay đổi của master. Lớp lỗi khác K3 ⇒ đề xuất packet riêng (§5, P-A) |
| K4 | human audit (6649074827) neo `5ca9cdbf`; head đã thành `ec805d8` sau update-branch. `k4()` chỉ nhận `run.json` của review offline bằng model | **Đỏ thật** theo M5/M6 (*"PR head bằng SHA đã approve"*). Việc nhận human audit là phạm vi của #1187/PR #1194 (ADR-0063 đang chờ). Merge master vào nhánh sau khi approve có được miễn re-review hay không là quyết định luật ⇒ đề xuất packet riêng (§5, P-B) |

## 2. Thay đổi

### 2.1 Đường H2 trong `_doc_connector`

Tham số mới (tên do executor đặt, ví dụ `nhan_state=False`). Chỉ `kiem-merge` K3 truyền `True` (§7 Q3). `accept` và `mo-lai`
giữ nguyên hành vi từng byte.

Khi bật, một issue comment `x` là **bằng chứng H2 cho head H** khi và chỉ khi **đủ cả 8 chốt**:

| # | chốt | thiếu chốt ⇒ |
|---|---|---|
| S1 | danh tính allow-list: `user.login` = `chatgpt-codex-connector[bot]` **và** `user.id` = 199175422 (int, không bool) **và** `user.type` = `Bot`. Hằng nằm trong mã, không cờ đổi. Trường nào vắng ⇒ không phải của connector | không phải H2 |
| S2 | thân có **đúng một** khớp `<!-- codex-review-state:v1 (\{…\}) -->`. Có ≥ 2 khớp trong cùng comment ⇒ `_die` mơ hồ | `_die` |
| S3 | JSON parse được, là object có đúng khoá `{code_review, security_review}`; `code_review` có đúng 4 khoá `commit_sha`, `has_any_findings`, `has_unresolved_findings`, `status` | `_die` (bằng chứng hỏng) |
| S4 | `code_review.commit_sha` là chuỗi 40 hex và **bằng nguyên chuỗi** H. Không so tiền tố | SHA 40 hex khác H ⇒ `cu` (bỏ qua như mục head cũ); không phải 40 hex ⇒ `_die` |
| S5 | `status` = `"completed"` | `running`/`failed`/khác trên H ⇒ K3 không đạt (§7 Q4) |
| S6 | `has_any_findings is False` **và** `has_unresolved_findings is False` (đúng kiểu bool) | `true`/`null`/kiểu khác trên H ⇒ K3 không đạt |
| S7 | `security_review`: nếu `commit_sha` = H thì `status` = `completed` và cả hai cờ `is False`; nếu `commit_sha` là `null` thì 4 trường đều `null` | không khớp ⇒ K3 không đạt (§7 Q5) |
| S8 | toàn readback **không có** review comment nào của connector (S1) với `original_commit_id` = H (khi vắng `original_commit_id` thì xét `commit_id`), và không có review nào của connector với `commit_id` = H | có ⇒ H2 không được dùng làm tín hiệu "xong". Đường cũ (review/H1) quyết định, finding xếp hạng như hiện hành |

Luật gộp khi bật:
- **G1.** Mọi H2 của connector neo H đều phải qua S5–S7. Chỉ cần một H2 neo H không qua (ví dụ `running` như #1071) là K3 không đạt.
  Không chọn bản "đẹp nhất" (§7 Q4).
- **G2.** "Xong" = điều kiện hiện hành, **hoặc** (có ≥ 1 H2 neo H qua đủ S1–S8 **và** G1 đạt).
- **G3.** Mâu thuẫn ⇒ `_die` "bằng chứng mâu thuẫn". Ví dụ: H2 neo H sạch, nhưng một H1 neo H mang badge, hoặc một review của
  connector trên H ở `CHANGES_REQUESTED`.
- **G4.** Comment không qua S1 (kể cả của chủ kho, chép khối H2) **không** được xét. Nếu nó mang badge thì xử như hiện hành
  (bỏ qua vì không phải connector).
- **G5.** Bỏ dòng `Reviewed commit:` khỏi H1, hay đổi bất kỳ trường H1/review nào, không được đổi kết quả của đường cũ khi `nhan_state=False`.

### 2.2 Allow-list danh tính cho đường cũ

Không đổi trong packet này. S1 chỉ áp cho đường H2 (§7 Q6).

### 2.3 Tài liệu

`docs/adr/0060-dieu-kien-merge-va-moc-ready.md` M6, gạch *"connector đã review đúng commit (dòng `Reviewed commit:` cho đúng SHA)"*:
thêm vế *"hoặc khối `codex-review-state:v1` của connector neo đúng SHA, `completed`, không finding, theo các chốt của `kiem-merge` K3"*,
kèm một dòng nguồn sửa đổi (packet #1211, ngày duyệt). Mục *Cưỡng chế — M11*: cập nhật số dòng `rg -c` của `packet_loop.py`.
Đây là cách sửa của §7 Q1 khuyến nghị.

## 3. Write set

`.claude/dev/packet_loop.py` · `.claude/dev/packet_loop_test.py` · `docs/adr/0060-dieu-kien-merge-va-moc-ready.md` ·
`ops/specs/K3-CONNECTOR-STATE-r1.md` (chép **nguyên byte** từ nhánh đặc tả vào commit đầu của nhánh thực thi, để K1 đọc được blob tại H).
Bốn tệp. Ước lượng ≤ 80 dòng thêm ở `packet_loop.py`, ≤ 250 ở test, ≤ 10 ở ADR, chưa tính tệp đặc tả.

### 3.1 Người giữ (đo 05-11-2026 04:44Z)

- Phép đo: fetch `+refs/heads/*:refs/remotes/origin/*`, so tập tên `ls-remote --heads` với `for-each-ref`, ra 862/862, thiếu 0, thừa 0.
  Sau `git branch -f master refs/remotes/origin/master`, chạy `ops/lease_publish.py ai-dang-giu`.
- `.claude/dev/packet_loop.py`, `.claude/dev/packet_loop_test.py` ⇒ **rc 11, `NGƯỜI_GIỮ 1`**:
  `pr1184-merge-contract-r2-g4-codex-service` (#1187, PR #1194 đang mở). Lease hết hạn `2026-11-05T05:23:42Z`; packet ấy có thể gia hạn.
  PR #1194 không chạm `_neo_connector`/`_doc_connector`, đo bằng grep diff `1f0941e..29ee9ca`, 0 dòng.
- `docs/adr/0060-…md` ⇒ rc 0, `NGƯỜI_GIỮ 0`.
- Hệ quả: **không cấp lease cho packet này trước khi lease #1187 đã nhả** (land hoặc thu hồi), và base phải chứa merge của #1194.
  Đo lại `ai-dang-giu` cho cả bốn tệp ngay trước lúc cấp lease (L5).

## 4. Nghiệm thu

Ca mới trong `.claude/dev/packet_loop_test.py` mang tiền tố `k3st_`, dùng lại fixture connector `_r834_ca`/`_CN834`/`_API834` (đã
có). Fixture H2 phải mang danh tính đủ S1 (`id` 199175422, `type` `Bot`), và JSON chép **nguyên khuôn** readback #1200 (§1.1), chỉ thay SHA.
Đột biến đích phải bị giết **đúng lý do**: tức ở tín hiệu assertion của ca đích, kèm thông báo mong đợi. Traceback không tính.

| # | tiêu chí | phép đo làm ĐỎ |
|---|---|---|
| A1 | `packet_loop_test.py` ra N/N, hai số bằng nhau; mọi ca `r834_*`, `cong_c_*`, `cong_m9_*` cũ vẫn xanh | bất kỳ ca đỏ |
| A2 | ca dương: readback chỉ có một H2 khuôn #1200 neo H ⇒ K3 đạt (`kiem-merge` không còn `K3` trong danh sách thiếu) | trên nền `bbfb460` ĐỎ: đo 05-11 04:5xZ, `_doc_connector` với readback REST thật của #1200 (3 endpoint, `head_sha` `ec805d8…`) ⇒ `connector chưa xong …`, rc 12 |
| A3 | ca âm, mỗi ca một chốt, K3 không đạt hoặc `_die` đúng thông báo: S1 `login` khác (comment của `ducthangho` chép nguyên khối) · S1 `id` khác · S1 `type` `User` · S1 vắng `id` · S2 hai khối · S3 JSON hỏng · S3 thừa khoá · S4 SHA tiền tố 10 ký tự của H · S4 SHA = H viết hoa · S5 `running` · S5 `failed` · S6 `has_any_findings: true` · S6 `has_unresolved_findings: true` · S6 `null` · S6 chuỗi `"false"` · S6 số `0` · S7 `security_review` neo H có finding · S8 review comment connector `original_commit_id` = H (P3) · S8 review comment chỉ có `commit_id` = H · G1 hai H2 neo H, một `completed`, một `running` (khuôn #1071) · G3 H1 neo H mang `![P1 Badge]` cùng H2 sạch | ca nào cho K3 đạt ⇒ đỏ |
| A4 | ca không tác động: H2 neo SHA khác H (head cũ) và không có bằng chứng nào khác ⇒ K3 không đạt `chưa xong` (H2 cũ không tính là xong của H) · H2 neo SHA cũ `has_any_findings: true` cùng H2/H1 sạch neo H ⇒ K3 đạt | sai màu ⇒ đỏ |
| A5 | G5 / Q3: cùng readback chỉ-H2 đưa vào `accept` và `mo-lai` ⇒ hành vi **y hệt** nền `bbfb460` (`connector chưa xong` với `accept`; với `mo-lai` thì như nền) | khác nền ⇒ đỏ |
| A6 | đột biến đích, mỗi cái giết ít nhất một ca A3/A4/A5 tương ứng: bỏ so `user.id` · bỏ so `user.type` · so `commit_sha` theo tiền tố · bỏ S5 · chỉ xét `has_any_findings` (bỏ `has_unresolved_findings`) · dùng `==` thay `is` cho bool (để `0`/`False` lọt) · bỏ S7 · bỏ S8 · G1 chọn bản đẹp nhất (`any` thay `all`) · bật H2 cho cả `accept` · nhận H2 neo head cũ là "xong" | đột biến sống ⇒ đỏ |
| A7 | M6: K3 thiếu cùng một điều kiện K0–K7 khác ⇒ thông báo nêu cả hai | — |
| A8 | `git diff --numstat <base> <ứng viên>`: đúng bốn tệp §3 | tệp thứ năm ⇒ đỏ |
| A9 | ADR-0060 M6 có vế mới (vế dương: `rg -F 'codex-review-state'` trong ADR ≥ 1 dòng, đo trên văn bản đã nối dòng theo L6(b)) và vẫn giữ vế `Reviewed commit:` (vế âm: xoá vế cũ ⇒ đỏ); `doctrine-scan`, `adr-song`, `doc-claims-check` xanh | — |
| A10 | Windows (M3 `required`): **một** lượt chạy ca `k3st_*` và `r834_*` trên `tra-luat-win` tại ứng viên, > 0 ca, không ca `skipped`. Lượt nền Windows thì chủ kho miễn (theo tiền lệ `KIEM-MERGE-M9` A8) hoặc chạy hai lượt theo M3(a) (§7 Q8) | 0 ca ⇒ đỏ |
| A11 | M9: một lượt `ci-dot-bien-du.yml` `success` tại head cuối, và K7 đạt với readback của lượt ấy | run đỏ ⇒ sửa hoặc hỏi chủ kho |
| A12 | **canary dữ liệu thật**: chạy `kiem-merge` (đúng mã ứng viên) với readback connector REST **thật** của PR của chính packet này, sau khi connector review sạch đúng head. Nếu chỉ có H2 thì K3 đạt; nếu có cả H1 thì cũng đạt. Thêm một lượt K3 trên readback thật của #1200 (head `ec805d8`, readback lấy lại), chỉ đo K3 | K3 thiếu ⇒ đỏ. Trạng thái `chưa đo được` cho tới lúc chạy thật |

## 5. Ngoài phạm vi

- **P-A (đề xuất packet riêng): base của K6/K7 khi nhánh đã merge master.** Hướng sửa: `kiem-merge` tính diff từ
  `merge-base(H, origin/master)`, hoặc đòi `--base` bằng merge-base ấy và `_die` khi khác. Số đo ở §1.6. Không gộp, vì đổi
  hợp đồng đối số của cổng và cần phản chứng riêng (base lùi để giấu thay đổi?).
- **P-B (đề xuất packet riêng, cần quyết định luật): update-branch sau approve.** Merge master vào nhánh sau review offline hay
  human audit sinh SHA mới, nên K4 đỏ. Câu hỏi luật: có miễn re-review khi phần thêm chỉ là cha thứ hai từ master và tree của
  packet không đổi hay không. Liên quan ADR-0060 M5 (đếm push) và ADR-0063 (#1187).
- Allow-list `user.id` cho đường H1/review hiện hành (§7 Q6).
- Nhận H2 trong `accept`/`mo-lai`.
- Gọi API từ trong lệnh: `kiem-merge` vẫn chỉ đọc readback.

## 6. `hinh_dang_ke_thua`

`khong_ap_dung`: packet này không khắc phục một packet trước. Họ lỗi liên quan để reviewer quét theo lớp (ADR-0060 M2):
- CLAUDE.md, *"HỎI CHỖ TIỆN TAY"* ý (b): kết luận sạch không nằm ở chỗ API hỏi.
- Bộ test `r834_*`: neo `Reviewed commit:` mơ hồ, hai khai mâu thuẫn, span thừa.
- #1106 P2 4435201341: `commit_id` bị dời, nên phải neo `original_commit_id`.

## 7. Câu hỏi cho chủ kho. r1 áp khuyến nghị; trả lời khác ⇒ r2

- **Q1. Sửa ADR thế nào?** ADR-0060 M6 ghi đích danh *"dòng `Reviewed commit:`"*, nên K3 hiện hành đúng chữ ADR.
  - (a) Sửa tại chỗ gạch M6 trong ADR-0060, kèm dòng nguồn.
  - (b) ADR mới. Số `0063` đang bị **hai** nhánh chưa land dùng cùng lúc (`agent/pr1184-merge-contract-r2-g3-codex-service`, `claude/wp1099-cloud-setup-p3b-g1`). ADR mới còn kéo `docs/PROTOCOL_DA_PHIEN.md` §20 vào write set, mà tệp ấy đang bị `wp1099-cloud-setup-p3b-r9-g1-claude` giữ.
  - (c) Không đổi mã, chỉ kỷ luật: luôn `@codex review` khi còn draft (§1.3: 30/30 lượt `Manual request` có H1).

  ➡️ Khuyến nghị (a). (c) rẻ nhất nhưng 9 PR ngày 05-11 cho thấy kỷ luật ấy không giữ được.
- **Q2. H2 sinh ra từ lượt `Draft marked ready` có hợp lệ không?** Lượt đó chạy *sau* khi bỏ draft, trái tinh thần M6/C1 (*"connector đã review rồi mới bỏ draft"*).
  ➡️ Khuyến nghị: hợp lệ cho **điều kiện merge** (K3 hỏi "connector đã review sạch đúng head chưa", không hỏi trigger). Kỷ luật bỏ draft là việc khác, giữ nguyên chữ M6. Không đọc cột trigger của bảng H2.
- **Q3. Phạm vi gọi.** ➡️ Chỉ `kiem-merge` K3. `accept`/`mo-lai` thuộc nhánh ADR-0054 đã đóng băng (ADR-0062).
- **Q4. Nhiều H2 neo cùng head, có bản không `completed`** (khuôn #1071, 1/125 PR). ➡️ Fail-closed: một bản chưa `completed` là K3 không đạt; muốn qua thì gọi `@codex review` để có H1.
- **Q5. `security_review`.** ➡️ Như S7: neo H thì phải sạch; `null` thì phải toàn `null`. Chưa từng thấy giá trị khác `null`.
- **Q6. Siết allow-list `user.id`/`type` cho cả đường H1/review cũ?** ➡️ Không trong packet này (giữ nhỏ, đường cũ đã có ca `r834_*`). Ghi thành nợ.
- **Q7. Executor/reviewer.** ➡️ Như tiền lệ `KIEM-MERGE-M9`: executor `anthropic_claude` (một phiên Claude Code mới), reviewer `openai_codex` qua `launcher.py run` cộng connector `@codex review` trên PR draft. Trần lời gọi theo dòng `tran_loi_goi_codex` ở đầu tệp.
- **Q8. Windows nền.** ➡️ Chủ kho miễn lượt nền như `KIEM-MERGE-M9` A8; chỉ chạy lượt ứng viên.
- **Q9. Mở P-A, P-B (§5)?** ➡️ Mở P-A ngay (cổng đang đỏ oan cho mọi PR đã merge master vào nhánh). P-B chờ #1187 land.

## 8. `chua_do_duoc`

- Readback REST do executor lấy: lệnh kiểm nội dung, không chứng minh nguồn (cùng giới hạn với K2/K3 hiện hành).
- Định dạng H2 là hợp đồng **không công bố** của connector; chỉ đo được 126 mẫu trong 6 ngày. Đổi phiên bản (`v2`) ⇒ S2 không khớp ⇒ K3 về hành vi cũ (fail-closed), nhưng không có cảnh báo sớm.
- H2 bị sửa đè: ảnh chụp readback là tức thời. Nếu connector sửa H2 giữa lúc đọc ba endpoint, có thể ghép trạng thái của hai thời điểm. Neo head (S4) và S8 thu hẹp khe ấy, **không đóng** nó.
- Executor #1196 (`session_015Gtxra9St4SrF625qHwL6o`) có số liệu chạy `kiem-merge` thật trên #1200. Đặc tả này **không** dùng số liệu ấy: phân loại K6/K7 ở §1.6 do phiên soạn đo lại bằng cách gọi thẳng `_phan_loai_windows`/`_cham_m9`, không chạy trọn `kiem-merge`.
- A2 trên nền mới đo bằng readback thật của #1200 gọi thẳng `_doc_connector`, chưa đo bằng fixture `k3st_`. Executor chạy ca A2 trên nền trước khi vá.
