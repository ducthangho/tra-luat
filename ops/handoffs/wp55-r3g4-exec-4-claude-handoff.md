# wp55 · revision 3 · generation 4 · EXECUTOR handoff (§7)

**Lease** `wp55-r3-exec-4-claude-20260814` · attempt **1/3** của revision 3.

> **ĐƯỜNG ĐĂNG LÊN GITHUB BỊ CHẶN — cần người đăng hộ.** Đã đo TRƯỚC khi làm việc:
> `api.github.com` trả **HTTP 403** (`"GitHub access is not enabled for this session"`)
> cho cả yêu cầu có token lẫn không token; `gh` không cài; MCP GitHub chưa xác thực
> và phiên này không chạy được OAuth. `git push` thì CHẠY ĐƯỢC (đã đẩy branch).
> Nên: heartbeat 30 phút lên #55 **không thực hiện được**, PR **chưa mở được**.
> Tệp này là bản ghi vào KHO thay cho comment — chủ kho hoặc một phiên có quyền
> GitHub cần đăng nó lên #55 và mở PR `claude/wp55-r3g4-f3-03` → `master`.

```yaml
schema_version: 1
packet_id: wp55
generation: 4
revision: 3
spec_hash: e321f811724fae97b19d523a3e5159bc13b425cd15fc6c753c7439fe28cae22d
spec_path: ops/specs/wp55-r3-spec.md
spec_branch: ops/wp55-r3-spec
prompt_sha256: dd9f01cc9b0a676a5052644868f49839a04cfa56dfa5c51d0182a9a3fc1152d9
provider: claude
role: executor
session_id: wp55-r3-exec-4-claude-20260814
lease_id: wp55-r3-exec-4-claude-20260814
base_sha: fbe5ab9e1ece3b45c065879bfd59dee2554db3e2
start_head_sha: 546ecf9fd4dfe889d0cd3ee77b9589d8bed0465f
head_sha: e6e4b73dc940fcd04e9030e353e0e5fe7f3f0af8
branch: claude/wp55-r3g4-f3-03
master_sha_at_measurement: 3d2c52d62696b0c7c190fd891115f543b0f9cb55
attempts_used: 1
attempts_limit: 3
status: needs_followup
summary: >-
  Đóng cả ba P1 bằng MỘT lượt vá ở tầng, sau khi xuất DANH SÁCH ĐÓNG và đo trên
  bản chưa vá (AC 18). Danh sách đóng lộ 18 lớp LỌT ở doctrine-scan (spec chỉ nêu
  2) và 16 hình dạng lease hỏng (spec nêu 5). Sau vá: 40/40 lớp lách bị bắt,
  15/15 ca bắt-oan được tha, 28/28 hình dạng lease có mã thoát kiểm soát và KHÔNG
  traceback. Suite 109/109 trên nhánh VÀ trên cây ĐÃ MERGE với master. Không đăng
  được lên GitHub — cần người đăng hộ.

changed_paths:
  - .claude/dev/packet_loop.py
  - .claude/dev/packet_loop_test.py
  - .claude/skills/cross-review/SKILL.md
  - .claude/skills/land-packets/SKILL.md
  - .claude/skills/work-packet/SKILL.md
  - CLAUDE.md

findings_closed:
  - finding_id: doctrine-rendering-bypass-nfkc
    how: >-
      `_chuan_hoa` viết lại cả tầng: NFKC (không phải NFC) + lọc Cf + giải entity
      MỘT lần + gấp đồng tự Cyrillic/Hy Lạp + gấp mũi tên + bỏ nháy cong + gộp
      phân cách + bỏ tag/comment HTML + rút text link + gỡ backslash escape. Áp
      cho CẢ HAI vế so khớp.
    mutation: 'ha_NFKC_ve_NFC → giết 7/7 ca đích'
  - finding_id: partial-lease-authority-bypass
    how: >-
      `_kiem_luoc_do_lease` — MỘT hàm kiểm chung, dùng bởi cả `record-lease` lẫn
      `begin-attempt`; kiểm trọn lược đồ + kiểu + thẩm quyền + cửa sổ hạn.
    mutation: 'tach_begin_attempt_khoi_ham_chung → giết 7/7 ca đích'
  - finding_id: merged-tree-doctrine-false-positive
    how: >-
      Hạng NGÔN NGỮ THƯỜNG + `_co_ngu_canh_doctrine`: một mục ngôn ngữ thường chỉ
      tính là chép doctrine khi có ngữ cảnh tái tạo doctrine (ô bảng, hoặc cùng
      đơn vị với một mục khác cùng nhóm).
    mutation: 'bo_ngu_canh_hang_ngon_ngu_thuong → giết 3/3 ca bắt-oan'

tests:
  - name: packet_loop_test.py (trên nhánh)
    status: passed
    evidence: 'rc=0 · nền 109/109 đạt · 23/23 đột biến giết đúng ca đích · TỔNG: ĐẠT'
  - name: packet_loop_test.py (trên CÂY ĐÃ MERGE với origin/master 3d2c52d)
    status: passed
    evidence: 'rc=0 · nền 109/109 đạt · TỔNG: ĐẠT (GIT_DIR trỏ về kho thật, xem ghi chú AC 20)'
  - name: doctrine-scan --root . (trên nhánh)
    status: passed
    evidence: 'rc=0 · sạch — đã quét 4 tệp, 0 chỗ chép doctrine'
  - name: doctrine-scan trên CÂY ĐÃ MERGE
    status: passed
    evidence: 'rc=0 · sạch — 4 tệp. TRƯỚC VÁ: rc=6 tại CLAUDE.md:82 (chính là P1-C)'
  - name: tl.py --selftest
    status: passed
    evidence: 'rc=0 · == tl selftest 1696/1696 == (hai số BẰNG NHAU)'
  - name: tl.py doc-claims-check --strict --json
    status: passed
    evidence: 'rc=0 · flags = [] (0 flag)'
  - name: tl.py release-verify RELEASE_MANIFEST.json --root . --strict --json
    status: passed
    evidence: >-
      rc=0 · ok=true · failed=[] · extra_files=[] · errors=[] ·
      package_hash_expected == current == full_tree ==
      e004956449c30f7176769a6ede69eecd31029aa7dcac54d3daf3bfa28375c400
  - name: tl.py golden-test (KHÔNG --write)
    status: passed
    evidence: 'rc=0'
  - name: .githooks/eol_policy.py --all --json
    status: passed
    evidence: 'rc=0 · ok=true · scanned=304 · violations=[] (0)'
  - name: release-bundle ×2 trên head + ×1 từ fbe5ab9e
    status: passed
    evidence: >-
      rc=0/0/0 · cả BA cùng sha256
      20c89545566b7682b3ecd2ac2ac0283add5af8a4d6ca377d9acbcde4487f8590 ·
      số sha256 khác nhau = 1
  - name: git diff --name-status fbe5ab9e e6e4b73
    status: passed
    evidence: 'ĐÚNG 6 tệp write_set, không hơn (SO_TEP=6); VERSION/CHANGELOG/RELEASE_MANIFEST/golden/bundled KHÔNG đổi'
  - name: đăng lên Issue #55 và mở PR
    status: not_run
    evidence: 'api.github.com HTTP 403 cho cả có token lẫn không token; gh không cài; MCP GitHub chưa xác thực'

gate_environment:
  core_abbrev: 7
  shallow_repository: false

danh_sach_dong_AC18:
  doctrine_truoc_va: '40 ca · 22 đạt · 18 LỌT · 0 bắt oan'
  doctrine_sau_va: '40 ca · 40 đạt · 0 LỌT · 0 bắt oan'
  bat_oan_truoc_va: '15 ca · 12 đạt · 3 BẮT OAN (O1/O2/O3)'
  bat_oan_sau_va: '15 ca · 15 đạt · 0 BẮT OAN'
  lease_truoc_va: '25 ca · 9 đạt · 11 LỌT · 5 TRACEBACK THÔ'
  lease_sau_va: '28 ca · 28 đạt · 0 LỌT · 0 TRACEBACK · 0 bắt oan'

remaining_work:
  - 'Đăng handoff này lên #55 và mở PR claude/wp55-r3g4-f3-03 → master (executor KHÔNG có đường ghi GitHub).'
  - 'Heartbeat 30 phút theo lease KHÔNG thực hiện được vì cùng lý do — cần nới điều kiện lease hoặc cấp đường ghi.'
  - 'Thân #55 vẫn hiển thị revision 2 (spec đã nêu ở mục "Việc chưa làm" #1).'
  - 'Verdict lượt 5 vẫn chưa có trong kho (spec "Việc chưa làm" #2) — không chặn lượt này.'

next_role: reviewer
next_reviewer_provider: codex   # §8 — executor là claude ⇒ reviewer BẮT BUỘC khác provider
manual_next_action: >-
  Chủ kho (hoặc phiên có quyền GitHub) đăng handoff lên #55, mở PR nhắm master,
  rồi cấp lease review cho codex neo head e6e4b73dc940fcd04e9030e353e0e5fe7f3f0af8.

failure:
  fingerprint: null
  category: null      # KHÔNG tiêu attempt vì lý do hạ tầng; nội dung đã hoàn tất
```

## Quan sát mức SPEC — báo, không tự nới

1. **Công thức AC 20 sinh ra một cây KHÔNG PHẢI kho git.** `git archive origin/master`
   + `git apply` cho một thư mục không có `.git`, nên ca
   `legacy_state_khong_co_lease_bi_chan` — vốn phải đọc blob lịch sử tại `22d2cc9`
   — không chạy được ở đó (`fatal: not a git repository`), suite ra 108/109.
   Đã đo lại với `GIT_DIR` trỏ về kho thật: **109/109**. Đây là khuyết của CÔNG THỨC
   ĐO trong spec/prompt, không phải của bản vá. Đề nghị revision sau ghi rõ bước
   cho kho đối tượng git tiếp cận được khi dựng cây đã merge.

2. **Lease đòi heartbeat 30 phút lên #55, nhưng môi trường executor không có đường
   ghi GitHub.** Ba lease trước "chết vì không có dấu vết sống"; nguyên nhân gốc có
   thể không phải phiên im lặng mà là đường ghi bị chặn ở tầng proxy. Điều kiện
   lease hiện KHÔNG thoả được bằng bất kỳ nỗ lực nào của phiên executor.

3. **`_TRANG_TRI` của bản trước khai SAI trong chú thích.** Nó nói xoá gạch dưới làm
   `same_failure_limit` và `same failure limit` "quy về một mối"; thực tế xoá `_` cho
   `samefailurelimit` còn dạng có khoảng trắng giữ nguyên — **hai chuỗi không khớp
   nhau**. Đã sửa bằng cách GỘP phân cách về khoảng trắng thay vì xoá, và có ca
   `ac18_phan_cach_hyphen` / `ac18_phan_cach_en_dash` chứng minh.

## Lệnh tái lập (mọi rc đọc TRỰC TIẾP, không qua pipe)

```bash
git rev-parse --is-shallow-repository            # false
git config core.abbrev 7
git show origin/ops/wp55-r3-spec:ops/specs/wp55-r3-spec.md | sha256sum   # e321f811…

python3 .claude/dev/packet_loop_test.py          # 109/109 + 23 đột biến
python3 .claude/dev/packet_loop.py doctrine-scan --root .
python3 scripts/tl.py --selftest                 # 1696/1696
python3 scripts/tl.py doc-claims-check --strict --json     # flags=[]
python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --root . --strict --json
python3 scripts/tl.py golden-test
python3 .githooks/eol_policy.py --all --json     # violations=[]
git diff --name-status fbe5ab9e e6e4b73          # ĐÚNG 6 tệp

# AC 20 — cây ĐÃ MERGE
merged=$(mktemp -d)
git archive origin/master | tar -x -C "$merged"
git diff --binary fbe5ab9e..e6e4b73 | git -C "$merged" apply
python3 "$merged/.claude/dev/packet_loop.py" doctrine-scan --root "$merged"
GIT_DIR="$PWD/.git" python3 "$merged/.claude/dev/packet_loop_test.py"
```
