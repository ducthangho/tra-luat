---
verdict: changes_requested
reviewed_sha: 1e36bb42e42a34751feae4d312d9cc48a466bc3f
reviewed_base: 27c413c3e531800431cad9db4452d7236505a5a9
reviewed_files_sha256:
  .github/workflows/duyet-khac-danh-tinh.yml: DELETED
  .github/workflows/duyet-phan-chung.yml: DELETED
  .claude/dev/duyet_danh_tinh.py: DELETED
  .claude/dev/duyet_danh_tinh_test.py: DELETED
  .claude/dev/ci_dang_ky_test.py: 0012d3ebb4dc1dc2ba6a8822a21f705efe20f6cdf98c428fc7ffc1a64776a4d3
  ops/RUNBOOK_TACH_DANH_TINH_GITHUB.md: c12fc3d2a79e91228ca367afa981c759c0ed00280d5667e184eabb285a69061e
model_tu_khai: GPT-6 / Codex (tự khai; khác nền tác giả Claude)
review_round: 1
review_class: sensitive
packet: BO-CONG-DUYET-KHAC-DANH-TINH
pr: 506
issue: 502
---

Có **2 P2 vá được trong write set**, nên yêu cầu sửa. Không tìm thấy P1 do packet xoá này: đúng 4 tệp bị xoá, registry và hai suite đạt, actionlint không thêm lỗi. Còn **1 finding P3** gồm hai tham chiếu tài liệu sống đã cũ, không phải lời gọi CI/mã thực thi.

`HINT.patch` sửa cả hai P2, chỉ chạm runbook. Đã thử `patch --dry-run --batch -p0` rồi áp thật trên `scratch/hint-check/`: đều rc=0. Sau HINT, packet vẫn đúng 6 tệp, **+13/−1710**, thân runbook lịch sử giữ nguyên. Đây là gợi ý đã kiểm trên bản sao; SHA được review và các băm trên vẫn là HEAD gốc, chưa áp HINT vào `cay-kho/`.

## BẢNG ĐO

Đo offline độc lập trong cwd; không dùng mạng. Các lệnh git trên `cay-kho/` chỉ đọc, dùng `GIT_OPTIONAL_LOCKS=0`; cây sạch trước/sau. Hai mutant, bản base dùng lint và bản thử HINT đều ở `scratch/`. Test dùng `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR` trong `scratch/`; PATH chứa `nguon/actionlint/` ở các phép cần actionlint.

| Phép đo | Kết quả độc lập | Bằng chứng |
|---|---|---|
| HEAD/base | Khớp đủ 40 ký tự như metadata trên | `scratch/logs/identity.json` |
| SHA-256 spec nguồn | `d8d1e0837f093b5c65b0583a02cee9d82ca1736c30df199f770c2671095edffd`, khớp đầu bài | `nguon/BO-CONG-DUYET-KHAC-DANH-TINH.md` |
| Lease exact write set | Đúng 6 đường; hash danh sách sort + LF là `366dab362ae70c865456c102d98ce0350ce83f38ab1231aabf618bd6019e8e29`, khớp lease | `scratch/logs/lease.yaml`, `scope-check.json` |
| Nguồn lease/spec trong mirror | `origin/ops/cap-lease-502` tại `b3e4ae6190801c257b430ce94093745e89287abe`; blob spec khớp nguồn được cấp; lease có ngoại lệ 6 tệp/≤30 dòng, dẫn comment 5629584614 | `scratch/logs/frozen-spec-from-lease.md`, `lease.yaml` |
| Xoá đủ 4 tệp | Cả bốn không còn trong HEAD; 6 workflows còn lại không có job key `cong` hoặc `phan-chung` | `name-status.txt`, `workflow-coverage.json` |
| M5 | Diff đúng một dòng bị gỡ khỏi `DA_NOI`; không thay phần khác của registry | Diff base..HEAD và băm đã ghi |
| `python3 .claude/dev/ci_dang_ky_test.py`, không `--chay` | **rc=0; ĐĂNG KÝ 21/21; PHẢN CHỨNG 51/51 đỏ đúng; TỔNG: ĐẠT** | `scratch/logs/registry-head.log` |
| Mutant khôi phục dòng DA_NOI | **rc=1; 21/22; mục đăng ký không có tệp** và **CI không gọi mục đăng ký**, đúng tên tệp bị xoá | `scratch/logs/restore-registry.log` |
| Mutant khôi phục 4 tệp, giữ registry HEAD | **rc=1; 22/21; test sống chưa đăng ký: .claude/dev/duyet_danh_tinh_test.py** | `scratch/logs/restore-four.log` |
| actionlint toàn workflows HEAD | **rc=1**, đúng **1** diagnostic `SC1003:info` tại `.github/workflows/ops-don-ref.yml:117:9`; 6/6 tệp được truyền cho công cụ | `scratch/logs/actionlint-head.log`, `actionlint.json` |
| actionlint toàn workflows base chính xác `27c413c3` | **rc=1**, cùng diagnostic trên; 8/8 tệp. Đầu ra giống HEAD từng byte ⇒ **delta=0** | `scratch/logs/actionlint-base.log`; base `.github/` lấy bằng `git archive 27c413c3 .github` |
| Phiên bản lint | actionlint **1.7.7**, ShellCheck **0.9.0** có trên PATH; không tắt shellcheck | Binary cấp sẵn và lệnh `-version`/`--version` |
| `python3 ops/lease_publish_test.py` | **rc=0; 146/146 đạt; đã chạy=146, bỏ qua=0** | `scratch/logs/lease-head.log` |
| t24/t34 thật sự đọc workflows | Gọi lại nguyên hàm, ghi nhận `Path.read_text`: **mỗi ca đọc đủ 6/6** workflows còn lại | `scratch/logs/workflow-coverage.json` |
| `bash ops/don_ref_chot_test.sh` | **rc=0; 105/105 đạt** khi PATH có actionlint cấp sẵn | `scratch/logs/don-ref-head.log` |
| Lần don-ref đầu thiếu PATH | **rc=1; 104/105**, đúng ca thiếu actionlint; thêm công cụ vào PATH rồi đo lại thành 105/105. Không coi đây là hồi quy HEAD | `scratch/logs/don-ref-no-actionlint.log` |
| Quét tham chiếu toàn cây | `grep -rnE` ra **75 dòng**: 73 dòng trong working tree, 2 dòng metadata git; tệp cấm chỉ đếm, đều 0. **0 lời gọi sống trong CI/mã thực thi**; 2 dòng doc/comment sống ghi P3 | Phân loại từng dòng bên dưới và `scratch/logs/references.tsv` |
| Khối ĐÃ RÚT | HEAD dòng 3–14: đúng 12 dòng thêm, trước tiêu đề dòng 23, đủ 3 mục (rút gì/packet/ngày, lý do trỏ spec, việc chủ kho ở nửa A). **Hai vấn đề P2 bên dưới** | `ops/RUNBOOK_TACH_DANH_TINH_GITHUB.md` |
| Thân lịch sử runbook | Bỏ chính 12 dòng chèn ở HEAD thì byte bằng bản base | `scratch/logs/scope-check.json` |
| Numstat base..HEAD | **+12/−1710; đúng 6 tệp; 12 ≤ 30** | Bảng numstat bên dưới |
| Các đường cấm thay đổi | Blob base=HEAD cho toàn bộ `docs/PROTOCOL_DA_PHIEN.md`, `ops/cai_actionlint.sh`, `ops/cai_cong_cu.sh`, CHANGELOG và manifest | `scratch/logs/scope-check.json`; không đọc nội dung protocol |
| Diff whitespace/cây gốc | `git diff --check 27c413c3..HEAD` rc=0; `git status --porcelain=v1` rỗng trước/sau | `diff-check.log`, `status-before.txt`, `status-after.txt` |
| Master đi tiếp | Mirror có **27 commit** tới `4b5184e21373eb8f8a36493d0282ebd020bb4458`; hợp tất cả đường chạm trong 27 commit **không giao write set** | `scratch/logs/master-drift-all-commits.json` |

**Đính chính dữ kiện đầu vào:** 27 commit ấy không chỉ chạm hồ sơ/CHANGELOG/manifest: còn `ops/cong_cu.py` (+23 dòng ở diff tổng). Không có đường nào trong sáu đường packet bị chạm, nên dùng base đã ghim vẫn hợp lệ cho lượt review này. Đây là sai khác trong mô tả bundle, không phải finding về diff PR #506.

**Giới hạn A3:** điều kiện `actionlint rc=0` trong spec đóng băng chưa đạt trên cả base lẫn HEAD. Không đổi tên kết quả này thành xanh; số đo đúng là **rc=1, delta=0**, phù hợp lời khai tác giả về lỗi có sẵn. Hai suite xanh không chứng minh toàn workflow lint xanh, cũng không chứng minh GitHub đã nhận/chạy workflow.

| Thêm | Xoá | Tệp (`git diff --numstat 27c413c3..HEAD`) |
|---:|---:|---|
| 0 | 1 | `.claude/dev/ci_dang_ky_test.py` |
| 0 | 338 | `.claude/dev/duyet_danh_tinh.py` |
| 0 | 1235 | `.claude/dev/duyet_danh_tinh_test.py` |
| 0 | 74 | `.github/workflows/duyet-khac-danh-tinh.yml` |
| 0 | 62 | `.github/workflows/duyet-phan-chung.yml` |
| 12 | 0 | `ops/RUNBOOK_TACH_DANH_TINH_GITHUB.md` |
| **12** | **1710** | **6 tệp** |

## Findings

### loi-khai-vuot-hai-su-kien [P2] Khối mới suy rộng từ hai merge thành mọi PR

- **TỆP/DÒNG:** `ops/RUNBOOK_TACH_DANH_TINH_GITHUB.md:9`, cùng lời tuyệt đối ở dòng 12.
- **VẤN ĐỀ:** dòng 9 dẫn hai PR nhưng kết luận “cổng không chặn gì”, “một check đỏ trên mọi PR” và “mọi push xoá bản duyệt”. Dòng 12 lại kết luận `master` kẹt “với mọi PR”. Hai sự kiện được dẫn không đủ cho các mệnh đề phổ quát ấy. Chính spec §`chua_do_duoc` và Q3 thừa nhận không phân biệt được cấu hình chưa bật với cấu hình có bypass. Reviewer không xác minh các sự kiện GitHub, không kết luận cổng đang/chưa cưỡng chế với ai.
- **ĐÃ THỬ VÁ:** HINT giữ nguyên quyết định rút và việc nửa A, ghi rõ “Spec ghi hai PR…”, bỏ các suy rộng, khai GitHub/nửa A **KHÔNG ĐO ĐƯỢC**, đổi nguy cơ kẹt thành “có thể chặn các PR chịu luật ấy”.
- **ĐÃ THỬ NGHIỆM:** áp thử và áp thật HINT trên bản sao đều rc=0; vẫn ba mục; thân lịch sử byte-identical với base; tổng packet +13/−1710, 6 tệp. Kiểm nội dung trực tiếp, không dùng regex làm bằng chứng sự thật GitHub.
- **ĐỘ TIN:** cao về lời khai vượt phạm vi nguồn; **KHÔNG ĐO ĐƯỢC** trạng thái GitHub thực tế.

### duong-dan-spec-khong-co-tren-head [P2] Mục lý do không định vị được spec trong cây được review

- **TỆP/DÒNG:** `ops/RUNBOOK_TACH_DANH_TINH_GITHUB.md:8`.
- **VẤN ĐỀ:** đường trần `ops/specs/BO-CONG-DUYET-KHAC-DANH-TINH.md` không tồn tại trên HEAD. Lease ghi rõ spec chưa ở master và có bản sao trên nhánh cấp lease. Runbook chỉ đưa đường trong kho mà không nêu ref, nên người đọc cây này không tìm được căn cứ rút tại vị trí đã chỉ. Mục lý do có chữ nhưng thiếu cách tìm đúng bản nguồn.
- **ĐÃ THỬ VÁ:** HINT thay đường trần bằng permalink tới commit `b3e4ae6190801c257b430ce94093745e89287abe` của nhánh lease, vẫn giữ tên đường spec và §VÌ SAO; không tạo tệp thứ bảy.
- **ĐÃ THỬ NGHIỆM:** `git ls-tree HEAD <spec_path>` trả rỗng; `git show b3e4ae6…:<spec_path>` có blob và SHA-256 khớp đúng `d8d1e083…95edffd` của spec nguồn/lease. HINT áp được với `patch -p0`. Đã kiểm đích commit/blob trong mirror, **chưa kiểm HTTP của permalink**.
- **ĐỘ TIN:** cao về thiếu đường tại HEAD và định danh byte của bản nguồn; truy cập GitHub **KHÔNG ĐO ĐƯỢC**.

### tham-chieu-tai-lieu-song-con-sot [P3] Hai chú dẫn đang dùng nhắc tệp đã xoá

- **TỆP/DÒNG:** `requirements.txt:29`; `ops/PHAN_BIEN_QUY_TRINH_BUILD_REVIEW_20260905.md:118`.
- **VẤN ĐỀ:** chú thích requirements vẫn liệt kê `duyet-phan-chung.yml:39` trong “Ba workflow”; bảng bằng chứng §2 của tài liệu phản biện vẫn đưa lệnh tái hiện đọc `.claude/dev/duyet_danh_tinh.py`. Dòng 118 nằm trước mốc PHỤ LỤC/lịch sử, nên không gộp nhầm với hai trích dẫn lịch sử ở dòng 661 và 728. Đây là chú dẫn/tài liệu cũ; không có consumer thực thi đọc hai tên đó trong mã/CI còn lại. Không nâng thành P1 vì không đo thấy CI/công cụ sản phẩm hỏng.
- **ĐÃ THỬ VÁ:** không sửa hai tệp vì nằm ngoài exact write set. HINT không có hunk ngoài sáu đường; P3 này không yêu cầu mở rộng packet để thông qua.
- **ĐÃ THỬ NGHIỆM:** quét toàn cây và đọc ngữ cảnh cho thấy một comment phụ thuộc và một lệnh minh hoạ trong Markdown; registry HEAD, lease và don-ref đều đạt. Không chạy lại lệnh minh hoạ trỏ tệp đã biết bị xoá.
- **ĐỘ TIN:** cao về hai tham chiếu còn sống ở lớp tài liệu; không có bằng chứng lỗi runtime do chúng.

## Mutant đã chạy

Hai bản sao chứa nguyên các đường mà registry quét (`.claude/dev`, `.claude/hooks`, `.githooks`, `.github`, `scripts/tl_core`, `ops`), lấy từ HEAD bằng `git archive`. Không sao chép các tệp bị cấm đọc. Chỉ làm hai thay đổi phục hồi được yêu cầu, không tự soạn nội dung khai thác/đường dẫn thoát.

1. **`restore-registry` — xoá bốn tệp, trả riêng M5 về base.** Đã xác minh registry base chỉ hơn HEAD đúng dòng `".claude/dev/duyet_danh_tinh_test.py",`. Chạy không `--chay`, **rc=1**:

   ```text
   ĐỎ: mục đăng ký không có tệp: .claude/dev/duyet_danh_tinh_test.py
   ĐỎ: CI không gọi mục đăng ký: .claude/dev/duyet_danh_tinh_test.py
   ĐĂNG KÝ: 21/22
   TỔNG: ĐỎ
   ```

   HEAD cùng phép đo rc=0, 21/21. Vế đỏ bắt đúng điều kiện tệp vắng và lời gọi workflow vắng ⇒ M5 không thừa.

2. **`restore-four` — trả bốn tệp bị xoá về đúng byte base, giữ M5 HEAD.** Chạy không `--chay`, **rc=1**:

   ```text
   ĐỎ: test sống chưa đăng ký: .claude/dev/duyet_danh_tinh_test.py
   ĐĂNG KÝ: 22/21
   TỔNG: ĐỎ
   ```

   Có phản chứng theo chiều ngược: khôi phục bộ test mà giữ registry đã gỡ mục là không nhất quán.

Registry HEAD còn chạy sẵn 51/51 phản chứng của chính suite. Hai mutant ngoài nêu trên dừng ở kiểm đăng ký và không được khai là đã chạy lại 51 ca ấy. Lease suite chạy nguyên bộ test hiện có; không tự thêm payload.

## Phân loại từng dòng tham chiếu

Mẫu: `duyet-khac-danh-tinh|duyet-phan-chung|duyet_danh_tinh|NGUOI_DUOC_DUYET`.

Đã dùng `grep -rnE` trên toàn `cay-kho/`, loại riêng các basename/nhánh bị cấm khỏi đầu ra nội dung rồi dùng `grep -cE` cho từng tệp cấm. Đã đối chiếu danh mục: không có tệp khác bị loại nhầm; không symlink, không lỗi đọc. Một lượt đối chiếu từng tệp quét tổng 1.937 tệp cho cùng 75 dòng. Nhật ký nguyên dòng được phép đọc ở `scratch/logs/grep-rn.log`; **mỗi dòng** có nhãn trong `scratch/logs/references.tsv` và `.json`.

`ops/specs/**`, `ops/leases/**`, `ops/reviews/**` có 59 dòng, đều hồ sơ chấp nhận. Ngoài ba vùng ấy, phân loại theo nội dung/ngữ cảnh: thông báo xoá mới, thân runbook giữ lịch sử, changelog gắn sự kiện, phụ lục lịch sử và attestation land gắn PR cũ đều chấp nhận; hai dòng tài liệu sống ghi P3. Hai dòng `.git` là tên ref, không phải consumer.

| Tệp | Từng dòng khớp | Phân loại |
|---|---|---|
| `.git/FETCH_HEAD` | 29 | Metadata git/tên ref — chấp nhận |
| `.git/packed-refs` | 30 | Metadata git/tên ref — chấp nhận |
| `CHANGELOG.md` | 185 | Changelog sự kiện cũ — chấp nhận |
| `ops/PHAN_BIEN_QUY_TRINH_BUILD_REVIEW_20260905.md` | 661, 728 | Phụ lục đã đánh lịch sử — chấp nhận |
| `ops/PHAN_BIEN_QUY_TRINH_BUILD_REVIEW_20260905.md` | 118 | Lệnh minh hoạ trong doc sống — P3 |
| `ops/RUNBOOK_TACH_DANH_TINH_GITHUB.md` | 17, 105, 106, 190, 198, 220 | Thân runbook lịch sử — chấp nhận |
| `ops/RUNBOOK_TACH_DANH_TINH_GITHUB.md` | 5, 6 | Thông báo thứ đã xoá — chấp nhận |
| `ops/land/pr489-land-evidence.yaml` | 456 | Attestation land PR #489/#490 cũ — chấp nhận |
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

Các tệp cấm: chỉ số đếm, không có nội dung hoặc số dòng nội dung được trích:

| Tệp | Số dòng khớp |
|---|---:|
| `AGENTS.md` | 0 |
| `CLAUDE.md` | 0 |
| `.claude/skills/cross-review/SKILL.md` | 0 |
| `.claude/skills/grill-me/LICENSE` | 0 |
| `.claude/skills/grill-me/SKILL.md` | 0 |
| `.claude/skills/grilling/LICENSE` | 0 |
| `.claude/skills/grilling/SKILL.md` | 0 |
| `.claude/skills/land-packets/SKILL.md` | 0 |
| `.claude/skills/soan-spec/SKILL.md` | 0 |
| `.claude/skills/work-packet/SKILL.md` | 0 |
| `docs/PROTOCOL_DA_PHIEN.md` | 0 |

`docs/PROTOCOL_DA_PHIEN.md` còn được kiểm **OID blob** base/HEAD giống nhau (`9d33347c12667aae289a07f61c4480c5527804fe`), đủ chứng minh cả §8 `human_audited` không bị đổi mà không cần đọc nội dung.

## chua_do_duoc

- **KHÔNG ĐO ĐƯỢC** GitHub: trạng thái/giờ merge/check/review của #500/#501, cài đặt required checks/approvals/bypass, nội dung comment quyền hạn #502 trên máy chủ. Chỉ đối chiếu attestation/spec/lease được cung cấp và các object Git có trong mirror; không suy từ hai merge ra cấu hình hiện tại.
- **KHÔNG ĐO ĐƯỢC** A5: check `cong`/`phan-chung` biến mất trên PR đầu tiên sau land; A6: gate master sau land, parity Windows và tình trạng master có kẹt hay không. Lượt này không dùng mạng và không land.
- **KHÔNG ĐO ĐƯỢC** HTTP của permalink trong HINT. Đích commit/path và SHA-256 đã xác minh offline; khả năng truy cập GitHub chưa đo.
- Chưa chạy `python scripts/tl.py doc-claims-check --strict`: không phải phép đo bắt buộc được yêu cầu trong danh sách gate lượt này; giữ giới hạn cấm đọc các tài liệu được chỉ định. Không khai A4 gate strict xanh và không dùng nó làm bằng chứng cho runbook.
- Không chạy registry với `--chay` theo yêu cầu. Chỉ Linux hiện tại; không khai Windows xanh. Không biến 146/146 hay 105/105 thành bằng chứng bao phủ mọi cú pháp workflow/GitHub.
- Không kiểm nội dung `CLAUDE.md`, `AGENTS.md`, `docs/PROTOCOL_DA_PHIEN.md`, `.claude/skills/**`; số đếm mẫu được yêu cầu trong cả 11 tệp đều bằng 0.

Hoàn tất ghi verdict: 2026-09-11T05:13:53Z.
