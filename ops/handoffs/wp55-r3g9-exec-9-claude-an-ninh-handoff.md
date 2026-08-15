# Handoff §7 — wp55 r3 · lease `wp55-r3-exec-9-claude-20260815` · phiên claude thứ HAI

```yaml
schema_version: 1
event: executor_handoff
packet_id: wp55
packet_issue: 55
revision: 3
generation: 9
lease_id: wp55-r3-exec-9-claude-20260815
role: executor
provider: claude
ket_qua: mot_phan            # đóng ĐÚNG finding ưu tiên 1; sáu finding kia KHÔNG đụng
da_push_len_nhanh_packet: false
ly_do_khong_push: push_precondition_kich_hoat
```

## 0. TÓM TẮT CHO CHỦ KHO — ba câu

1. **Lease này đã bị một phiên khác tiêu thụ.** Generation 9 đã chạy xong và đẩy
   `1a4525a`; sổ ghi `attempts_used: 3/3, attempts_exhausted: true`. Tôi là phiên
   executor THỨ HAI mở trên cùng một lease — lần đụng độ thứ **năm** trong ngày.
2. **Finding ưu tiên 1 (P1 an ninh) CHƯA ĐƯỢC ĐÓNG** ở `1a4525a` — chính cái head
   mà lease review lượt 10 đang neo để soi. Phiên g9 kia chỉ đóng SÁU finding
   doctrine; mục an ninh chỉ có trong lease (thêm lúc 10:10Z) nên nó không thấy.
3. **Tôi KHÔNG đẩy lên nhánh packet** — `push_precondition` kích hoạt. Bản vá đã
   verify nằm ở `ops/patches/wp55-r3g9-an-ninh.patch`, áp sạch lên `1a4525a`.

## 1. Vì sao handoff này khác thường

Lease chỉ định head xuất phát `4270210…c949b93` và tôi xác minh đúng nó lúc mở
phiên. Nhưng khi chạy `push_precondition` (fetch `ops/*` trước khi push), đo được:

| lúc (UTC) | quan sát |
|---|---|
| 2026-08-15T10:30:20Z | fetch `ops/*` — nhánh MỚI `ops/wp55-r3-review-10` xuất hiện |
| 2026-08-15T10:30:56Z | fetch nhánh packet — tip đã dời `4270210` → `1a4525a` |

`ops/leases/wp55-r3-review-10-codex-20260815.yaml` (cấp `10:27:00Z`, đăng
`10:29:15Z`, comment `5301820608`) neo:

```yaml
reviewed_sha_required: 1a4525a20aa360476a6f59cb157c21097919c457
branch: claude/wp55-r3g5-f3-03
lease_expires_at_utc: '2026-08-16T11:00:00Z'   # CÒN HIỆU LỰC
```

Đây đúng hình dạng mà `push_precondition` sinh ra để chặn: **có một lease đang neo
một SHA trên nhánh này** ⇒ DỪNG, hỏi chủ kho. Đẩy vào đây là lặp lại nguyên xi sự
cố đã huỷ lease lượt 8 — lần này là cố ý, nên còn nặng hơn.

**Chốt cho phiên điều phối:** tin nhắn điều phối nói *"ĐÓNG BĂNG ĐÃ GỠ … đẩy lên
`claude/wp55-r3g5-f3-03` là hợp lệ"*. Điều đó **SAI tại thời điểm đo**. Đóng băng
được gỡ trong khoảnh khắc rồi **lên lại** lúc 10:27Z trên một SHA mới. Chính vì
tin nhắn dặn "vẫn fetch ops/* và tự kiểm, đừng bỏ bước" mà bước đó bắt được.

## 2. Finding ưu tiên 1 — ĐÃ ĐÓNG (nhưng chưa vào nhánh packet)

`finding_id: work-packet-secret-check-prints-secret` · P1 · an ninh ·
`must_finish_even_if_out_of_time: true`

### 2.1 Tái lập trên head ĐANG BỊ SOI

`.claude/skills/work-packet/SKILL.md:67` tại `1a4525a` vẫn nguyên văn:

```
echo "${TEN_BIEN:+có, ${#TEN_BIEN} ký tự}${TEN_BIEN:-chưa đặt}"
```

`${VAR:-…}` chỉ thay thế khi biến **rỗng/chưa đặt**; ở nhánh "đã đặt" nó trả
**chính giá trị**, nối liền sau phần đếm ký tự. Bơm giá trị GIẢ 27 ký tự:

```
TRƯỚC (1a4525a): có, 27 ký tựghp_FAKE_TOKEN_abcdef123456     ⇒ RÒ RỈ
SAU   (df5c09c): có, 27 ký tự                                 ⇒ SẠCH
```

Lệnh tái lập: `bash ops/evidence/wp55-r3g9-an-ninh-probe.sh` (neo SHA bất biến,
không ref di động). Đầu ra đã đo: `ops/evidence/wp55-r3g9-an-ninh-probe.txt`.

Adapter tự khai kiểm bằng **sự tồn tại**, *"không bao giờ in nội dung"* — nên đây
là tài liệu nói ngược với thứ nó làm. Đây là lệnh hướng dẫn agent chạy với refresh
token THẬT, và stdout agent đi vào transcript: một lần làm theo là phải thu hồi và
cấp lại token.

### 2.2 Bản vá — và vì sao KHÔNG dùng `:-`

```bash
if [ -n "${TEN_BIEN:+x}" ]; then echo "có, ${#TEN_BIEN} ký tự"; else echo "chưa đặt"; fi
```

Đường vá "hiển nhiên" là `[ -n "${TEN_BIEN:-}" ]`. Nó sạch stdout nhưng **vẫn rò
ra vết `set -x`**, mà stderr agent cũng vào transcript. Đo được:

```
sạch cả vết  : [ -n "${TEN_BIEN:+x}" ]   → vết in `[ -n x ]`
RÒ RỈ ra vết : [ -n "${TEN_BIEN:-}" ]    → vết in `[ -n ghp_FAKE_TOKEN_abcdef123456 ]`
```

`:+` trả **từ thay thế**, không bao giờ trả giá trị — nên không đường nào in giá
trị, kể cả đường vết. Giữ nguyên ngữ nghĩa cũ (rỗng ⇒ "chưa đặt"), an toàn dưới
`set -u`, và `${#TEN_BIEN}` chỉ chạm tới ở nhánh đã-đặt.

### 2.3 Chốt bằng máy — và nó CHẾT ĐƯỢC

Ca `work_packet_kiem_bi_mat_khong_in_gia_tri`: **bóc lệnh nguyên văn ra khỏi
adapter** rồi chạy thật với giá trị giả, đòi giá trị không xuất hiện ở stdout LẪN
stderr. Không chép chuỗi vào suite — chép là dựng bản sao, và bản sao trôi lệch
(đúng cái bẫy adapter này đã dính ba lượt).

Ba lớp: (1) hình dạng — cấm `${TEN_BIEN:-` , chạy được cả ở nền không có shell
POSIX; (2) hành vi — giá trị không lọt; (3) nhánh chưa-đặt vẫn phân biệt được.

**Đột biến bắt buộc — `MUTANTS_ADAPTER`.** `MUTANTS` cũ chỉ vá `packet_loop.py`,
nên MỌI ca đọc tệp adapter nằm NGOÀI phép tự chứng minh không rỗng: chúng có thể
đã mục từ lâu mà suite vẫn xanh. Đã bổ sung tầng đột biến cho adapter; đo được:

```
đột biến ADAPTER (ca đọc tệp skill cũng phải chứng minh KHÔNG RỖNG):
  ok  work_packet_kiem_bi_mat_nhu_bug_goc        → giết 1 ca đích
  ok  cross_review_go_cu_phap_ghi_pr             → giết 1 ca đích
  ok  land_packets_go_disable_model_invocation   → giết 1 ca đích
```

Tức: trả lệnh về **đúng dạng cũ** ⇒ ca an ninh **ĐỎ**. Đúng yêu cầu
`mutation_required` của lease.

Một chi tiết đã trả giá để biết: đột biến adapter phải thay **TẤT CẢ** chỗ khớp,
không phải chỗ đầu. Lần chạy đầu hai đột biến cũ báo "VẪN XANH" vì `gh pr ` có 6
chỗ và `disable-model-invocation: true` có 2 — gỡ một chỗ thì ca đúng ra vẫn phải
xanh. Đó là đột biến không đo được gì, và suite đã bắt đúng nó.

## 3. SÁU finding doctrine — KHÔNG ĐỤNG, và đây là lý do

Phiên g9 kia đã đóng cả sáu ở `1a4525a`, và lease review lượt 10 đang soi đúng
head đó. Vá lại sẽ là (a) làm trùng, (b) trên nền đã cũ, (c) đẩy tip rời khỏi SHA
reviewer đang thuê soi. **Không khai là đã xử lý.**

Riêng finding 6 `packet-suite-mutation-count-mismatch`: g9 đã chọn cách **IN** số
đếm bằng máy. Tôi đã soạn một chốt **ASSERT** số khai và đã **BỎ** khi rebase — một
finding đang trong tầm soi thì không phải chỗ của tôi. Chỉ thêm đúng một dòng
`đột biến adapter : 3` vào khối SỐ LIỆU của g9 để con số máy đếm không bị khuyết.

Hai mục đã HOÃN sang revision 4 (`ac20-archive-tree-suite-not-self-contained`,
`same-provider-fallback-contradicts-protocol`): không đụng, không khai.

## 4. Đo — bản vá trên `df5c09c` (= `1a4525a` + vá an ninh)

Đọc rc trực tiếp từng tiến trình, không qua pipe.

| lệnh | rc | số |
|---|---|---|
| `packet_loop_test.py` | 0 | nền **174/174** · 44 đột biến · **3 đột biến adapter** · 66 lớp lách · 35 ca bắt-oan · **0 ngoại lệ** · TỔNG ĐẠT |
| `packet_loop.py doctrine-scan --root .` | 0 | sạch, 4 tệp, 0 chỗ chép |
| `tl.py --selftest` | 0 | **1696/1696** (≈90 giây, KHÔNG timeout) |
| `tl.py doc-claims-check --strict --json` | 0 | — |
| `tl.py release-verify … --strict --json` | 0 | `package_hash_match: true` |
| `tl.py golden-test` | 0 | — |
| `.githooks/eol_policy.py --all --json` | 0 | `violations: []` |
| **AC 20** doctrine-scan (cây merge) | 0 | sạch, 4 tệp |
| **AC 20** suite (cây merge, `GIT_DIR` kho thật) | 0 | **174/174**, TỔNG ĐẠT |

AC 20 neo master bất biến `2531366e1abc6cbca0a6c2765e40e54be38d1fb7`; apply diff
`fbe5ab9e…` → `df5c09c` rc=0.

Phạm vi: **đúng 2 tệp**, cả hai trong `write_set` —
`.claude/dev/packet_loop_test.py`, `.claude/skills/work-packet/SKILL.md`.

## 5. Ba chỗ tin nhắn điều phối LỆCH với tạo phẩm trong kho

Nêu ra vì phiên sau sẽ đọc lại tin nhắn ấy, không phải để bắt lỗi.

1. **"ĐÓNG BĂNG ĐÃ GỠ"** — sai tại thời điểm đo. Xem §1: lease review 10 lên lúc
   10:27Z, còn hiệu lực tới 2026-08-16T11:00Z.
2. **"`ac20-merged-tree-recipe`: not_run"** — verdict lượt 9 CÓ chạy và ghi kết
   quả (`apply rc=0; doctrine-scan rc=0; suite GIT_DIR rc=0, 157/157`). Tôi cũng
   chạy lại: rc=0, 174/174.
3. **"`tl.py --selftest`: timeout, KHÔNG có tổng N/N"** — verdict lượt 9 ghi rõ
   `rc=1, 1694/1696` kèm tên hai ca đỏ. Tôi đo trên head mới: **rc=0, 1696/1696**,
   ~90 giây. Hai ca đỏ ấy nay xanh.

Và một id không khớp: tin nhắn gọi *"Finding 4 `packet-loop-suite-mutant-gate-red`
— Windows rc=1, Linux rc=0 với 157/157"*. **Không có** `finding_id` nào như vậy
trong lease hay verdict; finding 4 của verdict là
`doctrine-structural-opener-poisons-ac19-tail`. Không đo được chênh lệch nền vì
không có ca nào để neo, và tôi không dựng lại từ mô tả (doctrine: fixture lấy
NGUYÊN VĂN). Nếu chênh lệch Windows/Linux là thật thì cần một fixture thật để đo.

## 6. Câu hỏi MỞ — chủ kho quyết, tôi KHÔNG tự chọn

**6.1 (chặn) Bản vá an ninh đi đường nào?** Nó đã verify và áp sạch lên `1a4525a`,
nhưng nhánh packet đang đóng băng cho review lượt 10. Ba đường:

- **(a)** chủ kho cho phép đẩy `df5c09c` lên nhánh packet ⇒ lease review 10 phải
  được cấp lại neo SHA mới (đúng bài học lượt 8);
- **(b)** giữ nguyên head, để reviewer lượt 10 soi `1a4525a`, vá an ninh vào đầu
  revision 4 — nhưng khi ấy một P1 an ninh đã biết nằm trên nhánh thêm một lượt;
- **(c)** cấp một lease executor hẹp CHỈ cho tệp adapter, chạy song song ngoài
  trục doctrine.

Tôi nghiêng về **(a)**: đây là P1 an ninh, `must_finish_even_if_out_of_time`, và
chi phí cấp lại lease review rẻ hơn để một lệnh in-token nằm lại trong adapter.
Nhưng quyết định là của chủ kho — §2.

**6.2 Câu hỏi spec chưa ai trả lời** (tin nhắn điều phối nêu, tôi không tự chốt):
nội dung trong code fence có được MIỄN trừ AC 19 không? Nó render ra chữ nhìn
thấy được; AC 2 và AC 18 không nói rõ. Đây là **spec thiếu**, không phải lỗi mã ⇒
theo lease `open_question.ac19-can-sua-spec-khong`, phải xuất successor §7 chứ
không tự chọn rồi vá theo lựa chọn của mình. Ghi lại nguyên vẹn cho revision 4.

**6.3 Sổ lượt.** `attempts_used: 3/3, attempts_exhausted: true` sau g9, mà bốn
commit không lease không vào sổ ⇒ số thật CAO HƠN. Phiên này không mở lượt mới,
không gọi `begin-attempt`, không tự cấp lease.

## 7. Việc phiên sau tiếp nhận

```yaml
patch_san_sang: ops/patches/wp55-r3g9-an-ninh.patch
  ap_len: 1a4525a20aa360476a6f59cb157c21097919c457
  cach_ap: git apply ops/patches/wp55-r3g9-an-ninh.patch
  da_verify_tai: df5c09cb1f3553cadd3c8d53420420d1d4334438
  pham_vi: 2 tệp, cả hai trong write_set
canh_bao_cho_reviewer_luot_10: >-
  Head 1a4525a VẪN mang P1 an ninh work-packet-secret-check-prints-secret.
  Nó KHÔNG nằm trong prior_review_findings của lease review 10 nên sẽ không
  được soi trừ khi có người nêu. Đây là lời nêu đó.
khong_lam:
  - không đẩy lên claude/** (push_precondition kích hoạt)
  - không đụng sáu finding doctrine (đã đóng ở 1a4525a, đang bị soi)
  - không sửa spec, không tự cấp lease, không mở lượt, không đóng issue nào
  - không chạm ops/specs/**, RELEASE_MANIFEST.json, references/golden/**,
    scripts/tl_test_fragments_bundled.py, VERSION, CHANGELOG
```

## 8. Nhịp (heartbeat) — 403, ghi vào tệp

Lease đòi heartbeat 30 phút một lần lên #55, và dặn: 403 thì ghi nhịp vào tệp
trong kho và **nói rõ**. API trả:

```
GET /repos/ducthangho/tra-luat → HTTP 403
{"message":"GitHub access is not enabled for this session.
  An org admin must connect the Claude GitHub App for this organization."}
```

`gh` cũng không có trong phiên (`command -v gh` → không thấy) — theo doctrine
"vắng mặt là QUAN SÁT", tôi đã đo cả hai đường chứ không kết luận từ một đường.
Nhịp ghi ở `ops/handoffs/wp55-r3g9-heartbeat.md`. **Không có comment nào của phiên
này trên #55** — ai đọc sổ trên Issue sẽ thấy khoảng trống đúng chỗ này.
