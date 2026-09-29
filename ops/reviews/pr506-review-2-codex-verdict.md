---
verdict: approve
reviewed_sha: 88e89b3afcb547326ad4233c2b806538ddaeb37b
reviewed_base: 27c413c3e531800431cad9db4452d7236505a5a9
reviewed_files_sha256:
  .github/workflows/duyet-khac-danh-tinh.yml: DELETED
  .github/workflows/duyet-phan-chung.yml: DELETED
  .claude/dev/duyet_danh_tinh.py: DELETED
  .claude/dev/duyet_danh_tinh_test.py: DELETED
  .claude/dev/ci_dang_ky_test.py: 0012d3ebb4dc1dc2ba6a8822a21f705efe20f6cdf98c428fc7ffc1a64776a4d3
  ops/RUNBOOK_TACH_DANH_TINH_GITHUB.md: 95dc50919d939230f45e256023db6bcdd84936ffc1aab4d214f119059c9043de
model_tu_khai: GPT-6 / Codex (tự khai; khác nền tác giả Claude)
review_round: 2
review_class: sensitive
packet: BO-CONG-DUYET-KHAC-DANH-TINH
pr: 506
issue: 502
---

## ĐỐI CHIẾU LƯỢT TRƯỚC

Đã làm trước các phép đo (1)–(7). Tự băm verdict lượt 1 được `99ff36d0bc36b03926e36083fc5ca7c536d9367f5ee6b8da88a88d50c285d34a`; spec đóng băng được `d8d1e0837f093b5c65b0583a02cee9d82ca1736c30df199f770c2671095edffd`, đều khớp đề bài. Không dùng số đo gate lượt 1 làm số đo lượt 2.

Diff toàn bộ `1e36bb4..HEAD` chỉ có runbook, +4/−3. HINT có đúng 1 hunk `@@ -5,11 +5,12 @@`; phần hunk của diff Git và HINT giống nhau từng byte (khác riêng header đường dẫn/metadata Git). Đã áp HINT bằng `patch --batch -p0` lên runbook lấy từ commit lượt 1 ở `scratch/hint-check/`, rc=0; kết quả bằng HEAD từng byte. Bằng chứng: `scratch/logs/round2.patch`, `round2-comparison.json`, `hint-apply.log`.

| Slug | Trạng thái | Bằng chứng tự đo và nhận định |
|---|---|---|
| `loi-khai-vuot-hai-su-kien` | **ĐÃ VÁ THẬT** | Trong hunk duy nhất: thay hai dòng lý do bằng ba dòng dẫn lời spec, giới hạn suy luận và khai GitHub KHÔNG ĐO ĐƯỢC; thay kết luận “master kẹt với mọi PR” bằng nguy cơ có điều kiện. Tất cả dòng tương ứng bằng HINT; không giữ lại lời khai phổ quát. |
| `duong-dan-spec-khong-co-tren-head` | **ĐÃ VÁ THẬT** | Cũng hunk này: dòng lý do đổi sang permalink commit `b3e4ae6190801c257b430ce94093745e89287abe`. Tự lấy blob tại commit/path đó trong mirror, SHA-256 khớp spec đóng băng. HTTP/GitHub KHÔNG ĐO ĐƯỢC. |
| `tham-chieu-tai-lieu-song-con-sot` | **CHƯA VÁ** | Tự so OID hai tệp giữa lượt 1 và HEAD: không đổi; đọc lại thấy `requirements.txt:29` và `ops/PHAN_BIEN_QUY_TRINH_BUILD_REVIEW_20260905.md:118` vẫn có tham chiếu. HINT không có hunk cho chúng. Giữ nguyên là xử lý đúng trong packet này vì cả hai nằm ngoài exact write set; P3 còn được ghi nhận, không coi là đã sửa. |

**Kết luận lượt 2: approve.** Hai P2 lượt 1 đã vá thật; không phát hiện P1/P2 còn mở. Packet xoá đúng bốn tệp, M5 cần thiết và không sửa quá phạm vi. Còn một P3 gồm hai tham chiếu tài liệu sống ngoài write set. `HINT.patch` có **0 hunk**, kèm ghi chú về P3.

## BẢNG ĐO

Tất cả số dưới đây được đo lại trong lượt 2, offline trên SHA đã ghim. Git ở `cay-kho/` chỉ đọc (`GIT_OPTIONAL_LOCKS=0`); mutant và base lint dùng bản sao trong `scratch/`. Khi chạy test: `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR` nằm trong `scratch/`, PATH có actionlint cấp sẵn, `AL_VER=1.7.7`. Không chạy registry với `--chay`.

| Mục / phép đo | Kết quả lượt 2 | Bằng chứng trong `scratch/logs/` |
|---|---|---|
| HEAD / base | Khớp đủ `88e89b3afcb547326ad4233c2b806538ddaeb37b` / `27c413c3e531800431cad9db4452d7236505a5a9` | `scope-check.json` |
| Spec đóng băng | Tự băm đúng `d8d1e0837f093b5c65b0583a02cee9d82ca1736c30df199f770c2671095edffd`; blob đích permalink bằng nguồn từng byte | `round2-comparison.json` |
| Lease / ngoại lệ ADR-0044 | Exact write set bằng đúng 6 đường lease; băm danh sách sort + LF `366dab362ae70c865456c102d98ce0350ce83f38ab1231aabf618bd6019e8e29` khớp. Lease có ngoại lệ 6 tệp/≤30 dòng, dẫn #502 comment 5629584614 | `lease.yaml`, `lease-check.json` |
| (1) Quét tham chiếu toàn cây | 75 dòng = 73 working tree + 2 metadata git; 59 dòng trong specs/leases/reviews. **0 tham chiếu thực thi sống** theo mẫu; **2 dòng doc/comment sống**, ghi P3. Phân loại từng dòng bên dưới | `grep-rn.log`, `references.tsv`, `references.json`, `references-scan.json` |
| (1) Bốn tệp bị xoá / jobs còn lại | Cả 4 vắng trong Git HEAD và working tree; YAML của cả 6 workflow còn lại không có job key `cong` hoặc `phan-chung` | `final-integrity.json`, `scope-check.json` |
| (2) Registry HEAD, không `--chay` | **rc=0; ĐĂNG KÝ 21/21; PHẢN CHỨNG 51/51 đỏ đúng; TỔNG ĐẠT** | `registry-head.log`, `.json` |
| (2) Mutant phục hồi riêng dòng DA_NOI | **rc=1; 21/22**; in đúng `mục đăng ký không có tệp: .claude/dev/duyet_danh_tinh_test.py`, thêm `CI không gọi mục đăng ký` | `restore-registry.log`, `.json`, `mutants-setup.json` |
| (2) Mutant phục hồi 4 tệp, giữ M5 | **rc=1; 22/21**; in đúng `test sống chưa đăng ký: .claude/dev/duyet_danh_tinh_test.py` | `restore-four.log`, `.json`, `mutants-setup.json` |
| (3) Phiên bản lint | **actionlint 1.7.7**, **ShellCheck 0.9.0** có trên PATH; không tắt shellcheck | `actionlint.json` |
| (3) Lint HEAD, toàn `.github/workflows/` | **rc=1; 6/6 tệp**, đúng **1 diagnostic SC1003:info** tại `.github/workflows/ops-don-ref.yml:117:9` | `actionlint-head.log`, `actionlint.json` |
| (3) Lint base chính xác `27c413c3`, bản sao | **rc=1; 8/8 tệp**, cùng một diagnostic. Đầu ra HEAD/base giống nhau từng byte ⇒ **delta=0** | `actionlint-base.log`; base `.github/` lấy bằng `git archive 27c413c3 .github` |
| (4) `python3 ops/lease_publish_test.py` | **rc=0; 146/146 đạt; đã chạy=146, bỏ qua=0** | `lease-head.log`, `.json` |
| (4) t24/t34 thực sự quét workflows | Gọi lại nguyên từng hàm, ghi nhận `Path.read_text`: **mỗi ca đọc đủ 6/6** workflows còn lại, đều PASS | `workflow-coverage.json` |
| (4) `bash ops/don_ref_chot_test.sh` | **rc=0; 105/105 đạt (chốt + bước làm)** | `don-ref-head.log`, `.json` |
| (5) Khối ĐÃ RÚT | Dòng 3–14: **12 dòng blockquote**, cộng dòng trống 15 thành **+13**. Đúng 3 mục; packet/ngày dòng 3, lý do/permalink dòng 8–10, việc nửa A dòng 11–14; trước tiêu đề dòng 24 | `survivors.patch`, `scope-check.json` |
| (5) Phạm vi lời khai / lịch sử | Lý do được gắn “Spec ghi hai PR”; khai GitHub/nửa A KHÔNG ĐO ĐƯỢC; nguy cơ chặn có điều kiện. Bỏ đúng 13 dòng thêm thì runbook bằng base từng byte | `round2.patch`, `scope-check.json` |
| (6) Numstat | **+13/−1710; đúng 6 tệp; 13 ≤ 30** | `numstat.txt`, `name-status.txt` |
| (7) Những tệp không được đụng | OID base=HEAD cho **toàn bộ** protocol, `ops/cai_actionlint.sh`, `ops/cai_cong_cu.sh`, CHANGELOG, manifest. Protocol không được đọc nội dung; OID đủ chứng minh cả §8 `human_audited` không đổi | `scope-check.json` |
| Chỉ M5 trong registry | Base bỏ đúng một dòng `".claude/dev/duyet_danh_tinh_test.py",` thì byte bằng HEAD; không đổi MOI, MOI_WINDOWS, CACH_LY hay phần kiểm khác | `survivors.patch`, `mutants-setup.json` |
| Cây gốc / whitespace / băm tệp | Status rỗng trước và sau; `git diff --check 27c413c3..HEAD` rc=0; hai tệp còn lại bằng Git HEAD từng byte, băm như metadata | `status-before.txt`, `status-after.txt`, `diff-check.log`, `final-integrity.json` |
| Master đi tiếp | `4b5184e21373eb8f8a36493d0282ebd020bb4458`; 27 commit, hợp đường chạm không giao sáu đường packet | `master-drift-all-commits.json` |

**Giới hạn A3:** điều kiện tuyệt đối `actionlint rc=0` trong spec vẫn **chưa đạt** ở cả base và HEAD. Kết quả đúng là **rc=1, delta=0**, phù hợp lời khai lỗi nền; không đổi tên nó thành xanh. Hai suite xanh và t24/t34 đọc đủ tệp không chứng minh mọi cú pháp workflow hoặc mọi hành vi GitHub đã được kiểm.

**Đính chính dữ kiện đầu vào:** đo lại 27 commit master cho thấy ngoài `ops/reviews/**`, CHANGELOG và manifest còn `ops/cong_cu.py` (+23/−0 trong diff tổng). Không giao write set; không phải finding về diff PR này. Bảng +12 của EVIDENCE ghi rõ lượt 1; số của lượt 2 là +13, phù hợp phần bổ sung của tác giả.

Lease/spec được đọc từ object tại `origin/ops/cap-lease-502` = `b3e4ae6190801c257b430ce94093745e89287abe`. Điều đó xác minh nội dung hồ sơ cục bộ; không xác minh comment hay quyền hạn hiện tại trên GitHub.

| Thêm | Xoá | Tệp (`git diff --numstat 27c413c3..HEAD`) |
|---:|---:|---|
| 0 | 1 | `.claude/dev/ci_dang_ky_test.py` |
| 0 | 338 | `.claude/dev/duyet_danh_tinh.py` |
| 0 | 1235 | `.claude/dev/duyet_danh_tinh_test.py` |
| 0 | 74 | `.github/workflows/duyet-khac-danh-tinh.yml` |
| 0 | 62 | `.github/workflows/duyet-phan-chung.yml` |
| 13 | 0 | `ops/RUNBOOK_TACH_DANH_TINH_GITHUB.md` |
| **13** | **1710** | **6 tệp** |

## Findings

Không còn P1/P2. Hai P2 đã đóng được đối chiếu từng hunk ở đầu verdict; P3 dưới đây còn mở và không yêu cầu mở rộng packet.

### tham-chieu-tai-lieu-song-con-sot [P3] Hai chú dẫn sống còn trỏ tệp đã xoá

- **TỆP/DÒNG:** `requirements.txt:29`; `ops/PHAN_BIEN_QUY_TRINH_BUILD_REVIEW_20260905.md:118`.
- **VẤN ĐỀ:** comment requirements vẫn kể `duyet-phan-chung.yml:39` trong “Ba workflow”; bảng §2 của tài liệu phản biện vẫn đưa lệnh tái hiện đọc `.claude/dev/duyet_danh_tinh.py`. Dòng 118 đứng trước mốc PHỤ LỤC dòng 122 (dòng 124 tuyên bố từ đó là bằng chứng/lịch sử), khác các trích dẫn lịch sử dòng 661/728. Đây là tham chiếu tài liệu sống; quét không tìm thấy consumer thực thi/CI còn gọi hai tên đó, và các gate được yêu cầu không hỏng do chúng.
- **ĐÃ THỬ VÁ:** không áp sửa vì cả hai đường ngoài exact write set. HINT lượt 1 không yêu cầu sửa P3; giữ nguyên là xử lý đúng trong packet này. `HINT.patch` lượt 2 có 0 hunk, không thêm tệp thứ bảy.
- **ĐÃ THỬ NGHIỆM:** đo lại grep toàn cây và ngữ cảnh; so OID hai tệp giữa lượt 1/HEAD bằng nhau; registry 21/21, lease 146/146, don-ref 105/105. Không chạy lệnh minh hoạ trỏ tới tệp đã xác minh bị xoá.
- **ĐỘ TIN:** cao về hai tham chiếu cũ và phân loại tài liệu; không có bằng chứng lỗi runtime do hai dòng này.

## Mutant đã chạy

Hai bản sao lấy các thư mục registry quét từ HEAD bằng `git archive`: `.claude/dev`, `.claude/hooks`, `.githooks`, `.github`, `scripts/tl_core`, `ops`. Không sao chép các tệp bị cấm đọc. Chỉ phục hồi byte có sẵn của base, không tự soạn nội dung khai thác/đường dẫn thoát.

1. **`scratch/restore-registry/` — xoá 4 tệp, phục hồi riêng dòng DA_NOI.** Tự so byte xác nhận registry base chỉ hơn HEAD đúng một dòng cần gỡ; bốn tệp vẫn vắng. `python3 .claude/dev/ci_dang_ky_test.py` **rc=1**:

   ```text
   ĐỎ: mục đăng ký không có tệp: .claude/dev/duyet_danh_tinh_test.py
   ĐỎ: CI không gọi mục đăng ký: .claude/dev/duyet_danh_tinh_test.py
   ĐĂNG KÝ: 21/22
   TỔNG: ĐỎ
   ```

   Đối chứng HEAD cùng lệnh rc=0, 21/21 ⇒ **M5 không thừa**.

2. **`scratch/restore-four/` — phục hồi 4 tệp, giữ registry HEAD.** Cả bốn được kiểm bằng byte và SHA-256 với base; registry vẫn bằng HEAD. Cùng lệnh **rc=1**:

   ```text
   ĐỎ: test sống chưa đăng ký: .claude/dev/duyet_danh_tinh_test.py
   ĐĂNG KÝ: 22/21
   TỔNG: ĐỎ
   ```

   Có phản chứng chiều ngược: phục hồi bộ test mà giữ mục đăng ký đã gỡ tạo cây không nhất quán.

Hai mutant không dùng `--chay`; điều kiện đăng ký đỏ khiến chúng dừng trước nhóm 51 phản chứng của registry. Riêng HEAD đã chạy 51/51 đỏ đúng. Bộ lease và don-ref chạy nguyên suite có sẵn; không tự thêm payload.

## Phân loại từng dòng tham chiếu

Mẫu: `duyet-khac-danh-tinh|duyet-phan-chung|duyet_danh_tinh|NGUOI_DUOC_DUYET`.

Dùng `grep -rnE` trên toàn `cay-kho/`, loại đầu ra nội dung các basename/nhánh bị cấm rồi dùng `grep -cE` riêng cho từng tệp cấm. Đối chiếu danh mục **1.937 tệp**: không có tệp ngoài phạm vi cấm bị loại nhầm; không có symlink hoặc lỗi đọc. Tổng **75 dòng**; mỗi dòng được gắn nhãn trong `scratch/logs/references.tsv` và `.json`. Không đọc nội dung tệp cấm để phân loại.

`ops/specs/**`, `ops/leases/**`, `ops/reviews/**` được giữ theo yêu cầu hồ sơ đóng băng. Ngoài các vùng ấy, đã đọc ngữ cảnh để phân biệt thông báo rút, thân runbook lịch sử, phụ lục lịch sử, changelog/land gắn sự kiện cũ với hai chú dẫn đang dùng. Metadata Git chỉ chứa tên ref.

| Tệp | Từng dòng khớp | Phân loại |
|---|---|---|
| `.git/FETCH_HEAD` | 29 | Metadata git/tên ref — chấp nhận |
| `.git/packed-refs` | 30 | Metadata git/tên ref — chấp nhận |
| `CHANGELOG.md` | 185 | Changelog sự kiện cũ — chấp nhận |
| `ops/PHAN_BIEN_QUY_TRINH_BUILD_REVIEW_20260905.md` | 118 | Lệnh tái hiện trong tài liệu sống — P3 |
| `ops/PHAN_BIEN_QUY_TRINH_BUILD_REVIEW_20260905.md` | 661, 728 | Phụ lục lịch sử — chấp nhận |
| `ops/RUNBOOK_TACH_DANH_TINH_GITHUB.md` | 18, 106, 107, 191, 199, 221 | Thân runbook lịch sử — chấp nhận |
| `ops/RUNBOOK_TACH_DANH_TINH_GITHUB.md` | 5, 6 | Thông báo rút hiện tại — chấp nhận |
| `ops/land/pr489-land-evidence.yaml` | 456 | Hồ sơ land PR #489/#490 đã đóng — chấp nhận |
| `ops/leases/cong-duyet-theo-tham-quyen-exec-1-claude-20260829.yaml` | 20, 43, 44, 82, 87, 90 | Hồ sơ đóng băng — chấp nhận |
| `ops/reviews/DO-T33-VA-GOI-REVIEW-20260907.md` | 40 | Hồ sơ đóng băng — chấp nhận |
| `ops/reviews/README.md` | 26, 87, 92 | Hồ sơ đóng băng — chấp nhận |
| `ops/reviews/n5-lenh-hook-windows-review-1-codex-verdict.receipt.yaml` | 123 | Hồ sơ đóng băng — chấp nhận |
| `ops/reviews/n5-lenh-hook-windows-review-2-codex-verdict.receipt.yaml` | 68 | Hồ sơ đóng băng — chấp nhận |
| `ops/reviews/phan-bien-quy-trinh-review-2-claude-verdict.md` | 47 | Hồ sơ đóng băng — chấp nhận |
| `ops/reviews/pr468-hoso-4-packet-review-12-codex/snapshot.json` | 727, 741, 742, 761, 762 | Hồ sơ đóng băng — chấp nhận |
| `ops/reviews/pr490-review-1-codex-verdict.md` | 77 | Hồ sơ đóng băng — chấp nhận |
| `ops/reviews/pr490-review-2-codex-verdict.md` | 33 | Hồ sơ đóng băng — chấp nhận |
| `ops/reviews/pr490-review-2-phep-do/gate-summary.json` | 394, 396, 397 | Hồ sơ đóng băng — chấp nhận |
| `ops/reviews/pr490-review-2-phep-do/status-audit.json` | 120, 122, 123 | Hồ sơ đóng băng — chấp nhận |
| `ops/reviews/pr490-review-4-codex-verdict.md` | 83, 127 | Hồ sơ đóng băng — chấp nhận |
| `ops/reviews/pr490-review-4-phep-do/claim-audit.json` | 279, 587 | Hồ sơ đóng băng — chấp nhận |
| `ops/reviews/pr490-review-4-phep-do/claim-ledger.tsv` | 41, 85 | Hồ sơ đóng băng — chấp nhận |
| `ops/reviews/pr492-review-4-claude-verdict.receipt.yaml` | 93 | Hồ sơ đóng băng — chấp nhận |
| `ops/reviews/pr500-review-1-codex-verdict.md` | 223, 451, 473, 546 | Hồ sơ đóng băng — chấp nhận |
| `ops/reviews/pr500-review-2-codex-verdict.md` | 255, 283, 507, 564, 664 | Hồ sơ đóng băng — chấp nhận |
| `ops/specs/CONG-DUYET-THEO-THAM-QUYEN.md` | 8, 22, 23, 48, 49, 69, 82, 85, 90, 92, 94, 99, 102, 121, 132, 170, 173 | Hồ sơ đóng băng — chấp nhận |
| `requirements.txt` | 29 | Comment sống — P3 |

Các tệp cấm: chỉ số đếm, không trích nội dung.

| Tệp | Số dòng khớp |
|---|---:|
| `.claude/skills/cross-review/SKILL.md` | 0 |
| `.claude/skills/grill-me/LICENSE` | 0 |
| `.claude/skills/grill-me/SKILL.md` | 0 |
| `.claude/skills/grilling/LICENSE` | 0 |
| `.claude/skills/grilling/SKILL.md` | 0 |
| `.claude/skills/land-packets/SKILL.md` | 0 |
| `.claude/skills/soan-spec/SKILL.md` | 0 |
| `.claude/skills/work-packet/SKILL.md` | 0 |
| `AGENTS.md` | 0 |
| `CLAUDE.md` | 0 |
| `docs/PROTOCOL_DA_PHIEN.md` | 0 |

OID của `docs/PROTOCOL_DA_PHIEN.md` ở base và HEAD đều là `9d33347c12667aae289a07f61c4480c5527804fe`; phép này không đọc nội dung protocol.

## chua_do_duoc

- **KHÔNG ĐO ĐƯỢC GitHub:** giờ/trạng thái merge, check và review của #500/#501; required checks, approvals, bypass; nội dung/thẩm quyền comment #502 trên máy chủ. Runbook nay thuật lại spec và giới hạn suy luận đúng; reviewer không lấy hai merge làm bằng chứng cho cấu hình hiện tại.
- **KHÔNG ĐO ĐƯỢC HTTP của permalink.** Đích commit/path tồn tại trong mirror, blob khớp spec đóng băng; khả năng truy cập URL trên GitHub chưa đo.
- **KHÔNG ĐO ĐƯỢC A5/A6 sau land:** check `cong`/`phan-chung` biến mất trên PR đầu tiên sau land, gate master sau land, parity Windows và tình trạng master có bị chặn. Phiên này offline, không land; việc nửa A vẫn thuộc chủ kho như runbook đã ghi.
- Chưa chạy `python scripts/tl.py doc-claims-check --strict`: ngoài các gate (1)–(7) được yêu cầu và có giới hạn cấm đọc tài liệu. Không khai toàn bộ A4 gate strict xanh hoặc cho rằng nó canh runbook.
- Không chạy registry `--chay` theo yêu cầu; chỉ kiểm trên Linux hiện tại, không khai Windows xanh.
- Không đọc nội dung `CLAUDE.md`, `AGENTS.md`, `docs/PROTOCOL_DA_PHIEN.md`, `.claude/skills/**`; chỉ đếm mẫu được cho phép (11 tệp, đều 0). Không dùng số đo lượt 1 thay cho lượt 2.

Hoàn tất ghi verdict: 2026-09-11T05:27:25Z.
