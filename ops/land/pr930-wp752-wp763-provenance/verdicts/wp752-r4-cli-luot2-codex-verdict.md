---
verdict: changes_requested
reviewed_sha: fc1bb3add70b7e7a2f17cdf4f940d7ce484b7053
spec_sha256: a98d09e86e32ee249668aaa114aed43e8a982e8bd7f9ef81fe61aa6a2a168791
so_p0: 0
so_p1: 0
so_p2: 1
so_p3: 0
---

**Kết luận: 1 P2 — F752-03, lỗ hổng của ca tự kiểm mới trong bản vá F752-02.** Hai công cụ nguyên bản đạt các phép đo đã chạy. Bản vá so byte đóng F752-01; bản vá lỗi dựng scalar 4369279124 vẫn đúng. Bản vá symlink sửa được hành vi cũ, nhưng ca tự kiểm mới không khóa đủ các nhánh mà nó tuyên bố khóa. Bốn đột biến liên quan sống qua suite; một đột biến khôi phục đúng kiểu `1/1` khi công cụ được gọi 0 lần. Theo thang chấm của chỉ thị, lỗi răng test này chặn merge.

Review offline theo `runs/f8f838f0/prompt.snapshot`, dùng [skill cross-review](../mirror/.agents/skills/cross-review/SKILL.md). Bản ghi được lưu tăng dần trong lượt và giữ nguyên ở [VERDICT-progress.md](VERDICT-progress.md). Chỉ ghi dưới thư mục gói `goi`; không sửa mirror, không mạng, không sửa ref, không push. Không thực hiện thao tác land hay chuyển state assurance.

- **Candidate:** `fc1bb3add70b7e7a2f17cdf4f940d7ce484b7053`; **tree:** `67860d1e7de654e3da71ad14ed01f61a2ff84119`. HEAD detached, cùng SHA/tree ở snapshot đầu và cuối.
- **Base diff:** `1797c32530fba381afd4009340a3fa558b7e37b0`, là tổ tiên candidate (`git merge-base --is-ancestor`, rc 0). Diff đúng bốn tệp mới: land +141, land test +284, HINT +78, HINT test +206; **+709/−0**, đạt trần 4 tệp/1.000 dòng thêm. Diff lượt trước → lượt này chỉ đổi `ops/kiem_nhan_hint_test.py`.
- **Spec r4:** đọc toàn bộ `ops/specs/no-p3-cong-cu-ho-so-r4.md`; SHA-256 file trước/sau và blob ở candidate đều khớp băm frontmatter. Nền cố định cho ca đỏ thật B3 là `1d7e642092fb3dda15967be44d095f37bb22ac5f`, khác base diff.
- **Reviewer:** provider `openai_codex`, họ model `openai`, execution surface `codex_cli`, transport `machine`; header CLI khai `gpt-6-astra`, effort `xhigh`, CLI `0.164.0`, session `01a17134-98cd-7561-8493-f7600cfb4044`, run `f8f838f0`. Nguồn: `runs/f8f838f0/stderr.log`, header dòng 2–13. Đây là cấu hình CLI công bố, không chứng minh model từng request. Executor Claude theo assignment; không có runtime receipt Executor để tự xác minh.
- **Class/authority:** spec khai routine, hiệu lực sensitive. Chỉ thị hiện tại cấp review offline exact SHA. Không tìm được lease #752 trong `ops/leases` bằng mẫu định danh packet (`rg`, rc 1); generation, hạn lease và state server **not_measured**. Không dùng lượt này để chứng nhận điều kiện cấp lease/land. Không suy model từ actor đăng GitHub.
- **Môi trường:** Linux x86_64, Python 3.11.17 `/usr/local/bin/python3`, PyYAML 6.0.1, Git 2.43.0, Ruff 0.16.9, `core.abbrev=7`; origin `https://github.com/ducthangho/tra-luat`. Sandbox khai workspace-write; reviewer giữ mirror read-only bằng phạm vi thao tác. Ignored `.codex/` có sẵn.

Mọi script đo đặt `TMPDIR=goi/tmp`, `PYTHONDONTWRITEBYTECODE=1`, dùng Python `-B`; Ruff dùng `--no-cache`; Git đọc dùng `GIT_OPTIONAL_LOCKS=0`. Mỗi mutant có bản sao mới bằng `mktemp -d -p goi`, chỉ đổi một chốt. Command, cwd, rc thật, stdout, stderr lưu trong JSON evidence. Các driver rc 0 là hoàn thành phép đo, không đồng nghĩa mọi tiến trình con rc 0.

Lệnh chạy lại từ bất kỳ cwd nào (đường dẫn các lệnh trong bảng baseline tương đối với mirror):

```bash
G=/tmp/claude-0/-home-user-tra-luat/8413b80e-5157-5812-ad93-3be1f70600c0/scratchpad/review752cli2/goi
python3 -B "$G/baseline.py"
python3 -B "$G/independent.py"
python3 -B "$G/mutations.py"
python3 -B "$G/content_probe.py"
python3 -B "$G/scalar_probe.py"
python3 -B "$G/focused.py"
python3 -B "$G/absent_probe.py"
python3 -B "$G/extra.py"
```

`mutations.py` có cơ chế nối tiếp theo tên đã ghi trong `mutations.json`; tái chạy một mutant độc lập dùng command/copy lưu ở chính dòng JSON đó. Không cần sửa repository để tái lập finding.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn: [VERDICT-luot1.md](VERDICT-luot1.md), SHA-256 đã đo trước khi dùng `97b0770b08ec40889c65737163ce7dcfc55cb3740dc1abc5f009d6e529ee53e6`, reviewed SHA lượt 1 `f9b3dc1ec11a5089b06d67a658e0f840742466eb`. Mỗi finding nhận đúng một nhãn dưới đây.

| Finding | Trạng thái | Phép đo độc lập trên candidate |
|---|---|---|
| **F752-01 [P2]** — chỉ so tập đường dẫn | **ĐÃ VÁ THẬT** | `content_probe.py`, rc 0: mutant thêm LF vào HINT có sẵn ở cả hai mode, chỉ JSON, hoặc chỉ chữ đều làm `ca_glob_va_khong_ghi` đỏ, suite **5/6**, rc **1**. Bản giao **6/6**, rc 0. [content.json](content.json), các mutant h06/h07. |
| **F752-02 [P2]** — symlink không đo vẫn tính đạt | **VÁ SINH LỖI MỚI** | Hành vi cũ đã sửa: POSIX thiếu quyền/thiếu API ⇒ đơn ca **0/1**, rc 1; Windows mô phỏng ⇒ **BO QUA**, **0/0**, rc 0, gọi công cụ 0 lần. Toàn suite lần lượt **5/6** rc 1 và **5/5** rc 0, skip được khai riêng. Nhưng ca tự kiểm MỚI tuyên bố khóa F752-02 lại thay chính policy và luôn tạo thuộc tính symlink; bốn mutant qua **6/6**. Nhánh vắng API bị khôi phục `return` vẫn qua tự kiểm, và probe đơn ca cho **1/1 / calls=0**. Lỗi evidence mới là **F752-03**, không cáo buộc bản giao hiện bỏ qua sai trên POSIX. [focused.json](focused.json), [absent.json](absent.json). |
| **4369279124 [P2]** — ngoại lệ dựng scalar YAML | **ĐÃ VÁ THẬT** | `scalar_probe.py`, rc 0: tái dùng cả bốn fixture có sẵn, bản giao rc 3, JSON có **LOI + DAT** và không traceback; thu hẹp catch về `yaml.YAMLError` cho rc 1/traceback ở cả bốn. Mutant l01 làm `ca_b1b_scalar_hong` đỏ, **8/9**. [scalar.json](scalar.json). |

Chi tiết scalar, không soạn tải trọng mới:

| Fixture có sẵn | Bản giao | Mutant catch hẹp |
|---|---|---|
| `thang-13` | rc 3, LOI + DAT | rc 1, ValueError: month must be in 1..12 |
| `the-timestamp` | rc 3, LOI + DAT | rc 1, AttributeError |
| `the-int` | rc 3, LOI + DAT | rc 1, ValueError |
| `long-sau` | rc 3, LOI + DAT | rc 1, RecursionError |

**Nghĩa N/N và nhánh thứ ba:** bản giao trên Linux in đúng một dòng `6/6`. Khi giả lập Windows thiếu symlink, in đúng một dòng `5/5` kèm một dòng `BO QUA ca_symlink_treo: …`; 5 gồm bốn ca đo công cụ và một ca tự kiểm harness, không phải năm lần gọi CLI. Ca bị skip không tăng số đạt. Cách đếm ca thực chạy này nằm trong hướng sửa đã cho ở F752-02 lượt 1; không chấm riêng việc trừ skip là một finding mới. Dòng `0/0` chỉ có khi chủ động chọn riêng ca bị skip, hoặc bên trong tiến trình con của tự kiểm; nó không được dùng làm bằng chứng xanh B6(c) của toàn suite (B6(c) vẫn đòi N ≥ 1). Không phát hiện sai đếm mới của bản giao trong ma trận đã đo. Điều chưa được khóa là policy nền và nhánh API vắng, nêu ở F752-03.

Theo tập hai lớp mở của lượt CLI 1, chỉ một lớp đạt nhãn ĐÃ VÁ THẬT trong lượt này: 1/2 = 50%; finding connector là kiểm lại lớp đã đóng, không cộng vào mẫu số. Một finding P2 hiện tại, hai biểu hiện cùng cơ chế; không tách bốn mutant thành bốn finding.

## Bảng đo lại

| Lệnh | rc thật · đầu ra/bằng chứng dương | Khớp/lệch |
|---|---|---|
| `python3 -B ops/kiem_ho_so_land_test.py` | **0 · 9/9**; đúng một dòng N/N | passed |
| `python3 -B ops/kiem_nhan_hint_test.py` | **0 · 6/6**; đúng một dòng N/N | passed với bản giao; F752-03 là răng tự kiểm |
| `python3 -B ops/kiem_ho_so_land.py --root . --json` | **1**; 65 tệp, `n_dat=15`, `n_landed=16`, `n_mien_tru=0`, glob đúng | khớp oracle; rc 1 vì nợ dữ liệu F |
| `python3 -B ops/kiem_nhan_hint.py --root . --json` | **0**; 65 tệp, `CO_NHAN=26`, thiếu nhãn=37, `RONG=2`, `KHONG_DOC_DUOC=0`, glob đúng | passed; từng tệp và đếm khớp oracle |
| `python3 -B ops/kiem_ho_so_land.py --root .` | **1**; token `ops/land/*-land-evidence.yaml`; `TỔNG: 15/16 … 0 miễn trừ … rc=1` | khớp B3(iii) |
| `python3 -B ops/kiem_nhan_hint.py --root .` | **0**; token `ops/reviews/**/*HINT.patch`; `ĐẾM: CO_NHAN 26 · KHONG_DU_DIEU_KIEN_PATCH_AS_HINT 37 · RONG 2 · KHONG_DOC_DUOC 0 · tổng 65 · rc=0` | passed B5 |
| `python3 -B .claude/dev/ci_dang_ky_test.py` | **1**; `ĐĂNG KÝ: 26/24`; đúng hai dòng `ĐỎ: test sống chưa đăng ký:` cho hai test packet; `TỔNG: ĐỎ` | failed có kiểm soát đúng đường A |
| `python3 -B ops/ci_duong_nhanh_test.py --mot-ca k01_so_dang_ky_nhan_muc_da_noi` | **3** theo chế độ đơn ca; `DO:k01_…` chỉ liệt kê đúng hai test chưa đăng ký | khớp nguyên nhân được cho phép; không phải kết quả full gate |
| `ruff --version` | **0 · ruff 0.16.9** | tool version đã đo |
| `ruff check --no-cache --select F ops/kiem_ho_so_land.py ops/kiem_ho_so_land_test.py ops/kiem_nhan_hint.py ops/kiem_nhan_hint_test.py` | **0 · All checks passed!** | passed bare lint, delta 0 so cơ sở rỗng |
| `git diff --check 1797c32530fba381afd4009340a3fa558b7e37b0 fc1bb3add70b7e7a2f17cdf4f940d7ce484b7053` | **0**, output rỗng | không lỗi whitespace được Git báo |

Đầu ra nguyên văn, không cắt ở trên, trong [baseline.json](baseline.json). Registry còn in `RUFF CI: 3/3 hợp đồng`, `LAUNCHER WINDOWS: 4/4 hợp đồng`; đây là phép kiểm cấu trúc, không phải đã chạy Windows hay phiên bản Ruff CI. Đối chứng lint bản sao thêm `import fractions` ⇒ rc 1/F401 ([extra.json](extra.json)).

`independent.py` dựng oracle đúng L-6/L-5, **không import công cụ packet**, so tập đường dẫn, trạng thái, lý do hai chiều và bộ đếm. Script/output đều có băm ở cuối. Đầu vào lịch sử xuất blob Git cục bộ, không checkout, không đổi ref. Kết quả:

| Cây/đầu vào land | Tệp | DAT / landed / MIEN_TRU | F / BO_QUA | rc công cụ |
|---|---:|---|---|---:|
| Mirror candidate | 65 | 15 / 16 / 0 | 1 / 49 | 1 |
| Base diff 1797c325… | 65 | 15 / 16 / 0 | 1 / 49 | 1 |
| Base, bỏ đúng F khỏi bản sao | 64 | 15 / 15 / 0 | 0 / 49 | 0 |
| Nền cố định 1d7e642… | 51 | 16 / 29 / 1 | 12 / 22 | 1 |
| Nền cố định, bỏ đúng F | 39 | 16 / 17 / 1 | 0 / 22 | 0 |

Tất cả khớp oracle. Trên hai cây loại F, `n_dat + n_mien_tru == n_landed`; len(tep) đúng glob. Trên cây cố định, miễn trừ đúng tập một tệp `pr672-wp574`; bộ đếm đúng ghim **16/29/1**. HINT mirror có 65 tệp, đếm **26/37/2/0**, từng đường dẫn/phân loại khớp oracle.

**Nợ dữ liệu được báo riêng:** F hiện tại là `ops/land/pr881-wp852-land-evidence.yaml`, trượt `authorization_url` vì thiếu mảnh yêu cầu L-6; đã có tại base diff. Đây là finding dữ liệu của B3, không phải finding mã #752. Owner: bên ghi sổ hồ sơ land/phiên điều phối; không sửa và không thêm miễn trừ. Danh sách F của nền cố định nằm ở [independent.json](independent.json).

| Tiêu chí | Phép đo | Kết quả |
|---|---|---|
| B1 | `ca_b1_rang_l6`, 19 fixture; mutant regex/kiểu SHA/khoá lồng/URL/mảnh/landed làm đỏ đúng nhánh | passed phạm vi đã đo |
| B1b | `ca_b1b_fail_close`, thẻ Python có sẵn, thiếu PyYAML, scalar; rc 3 và ưu tiên rc trên cây trộn; mutant l01/l15 | passed; không tạo thêm payload |
| B1c | Biên SHA 41/64, repo anh em, landed số 1 trong fixture; l02/l11/l13/l14 bị bắt | passed các biên đã đo; không tuyên bố đã tái lập toàn bộ 19 mutant lịch sử |
| B2 | Hằng thật không tiêm; ca A miễn trừ có lý do, ca B rc 3; l16–l19 đều đỏ ca B2 | passed |
| B2b | Quét đúng một tệp, l20 và l21 chết ở ca phạm vi | passed |
| B3 | Oracle trên mirror/base/fixed, cây loại F, token chữ/JSON, ghim 16/29/1; sáu mutant oracle bị bác | passed hành vi đầu vào; giới hạn bản sao nêu dưới |
| B4 | Đủ nhãn, hai mồi, rỗng/LF, UTF-8 hỏng, thư mục; symlink treo thật rc 3; h01–h05 bị bắt | passed phân loại công cụ |
| B5 | Oracle HINT khớp từng tệp/đếm; snapshot byte trước/sau mirror không delta; h06/h07 làm ca không ghi đỏ ở cả hai mode | passed F752-01 |
| B6(a) | Registry rc 1, 26/24, đúng hai lỗi được phép | failed có kiểm soát, không finding |
| B6(b) | Lint thật rc 0; import thừa rc 1/F401 | passed |
| B6(c) | Hai suite một dòng 9/9 và 6/6; nhánh skip khai riêng; đột biến policy/API vắng qua tự kiểm mới | bản giao đúng định dạng/đếm; răng tự kiểm **failed F752-03** |
| B6(d) | k01 rc 3 riêng ca, đúng nguyên nhân hai test; không full suite hoặc Actions | measured k01; phần còn lại not_run/not_measured |
| B7 | Mỗi công cụ ba root sai × chữ/JSON: rc 2, không dòng đếm; l26/h26 bỏ chốt ⇒ đỏ | passed |

Snapshot đầu/cuối giống nhau: SHA/tree, trạng thái Git tracked/untracked/ignored, diff/index và hash của **135 tệp** (bốn tệp packet + 65 land + 65 HINT + spec). Git status thông thường sạch; có ignored `.codex/` từ đầu, nội dung không đọc. [snapshot-before.json](snapshot-before.json), [snapshot-after.json](snapshot-after.json). Đây là không có delta quan sát được ở hai mốc, không phải chứng minh chưa từng ghi rồi hoàn nguyên.

## Đột biến

`mutations.py`: **47 mutant duy nhất**, **43 bị giết**, **4 sống**, tất cả bốn mutant sống thuộc F752-03. Mỗi mutant đổi một anchor độc nhất trong một bản sao; test giữ nguyên trừ các mutant `t*` cố ý kiểm răng của harness. Các lỗi khởi tạo do anchor trùng docstring được sửa trong script reviewer trước khi chạy mutant; không tính chúng là “giết”. JSON lưu old/new, bản sao, command, stdout/stderr và rc đầy đủ.

Bảng ghi ca đỏ đầu tiên; toàn bộ ca đỏ ở [mutations.json](mutations.json). `h04` làm công cụ ném lỗi đọc thư mục, không có JSON; JSONDecodeError trong test là hệ quả của regression đã tiêm, không phải setup lỗi.

| Tên | Chốt đổi | rc · N/N · ca đỏ đầu | Kết quả |
|---|---|---|---|
| l01-yaml-catch | `except Exception as e: → except yaml.YAMLError as e:` | 1 · 8/9 · DO ca_b1b_scalar_hong: AssertionError: thang-13: rc 1 (cần 3); hon3/dist-packages/yaml/constructor.py", line 330, in construct_yaml_timestamp | GIẾT |
| l02-fullmatch-to-match | `RE_SHA.fullmatch(sha) → RE_SHA.match(sha)` | 1 · 8/9 · DO ca_b1_rang_l6: AssertionError: sha-lf: DAT (cần TRUOT) — đủ authorized_head_sha và authorization_url | GIẾT |
| l03-relax-regex | `RE_SHA = re.compile(r"[0-9a-f]{40}") → RE_SHA = re.compile(r"[0-9a-fA-F]{39,40}")` | 1 · 8/9 · DO ca_b1_rang_l6: AssertionError: sha39: DAT (cần TRUOT) — đủ authorized_head_sha và authorization_url | GIẾT |
| l04-coerce-sha | `isinstance(sha, str) and RE_SHA.fullmatch(sha) → RE_SHA.fullmatch(str(sha))` | 1 · 8/9 · DO ca_b1_rang_l6: AssertionError: sha-so: DAT (cần TRUOT) — đủ authorized_head_sha và authorization_url | GIẾT |
| l05-nested-keys | `    truot = [] ⏎     sha = →     doc = doc.get("candidates", [doc])[0] ⏎     truot = [] ⏎     sha =` | 1 · 8/9 · DO ca_b1_rang_l6: AssertionError: long: DAT (cần TRUOT) — đủ authorized_head_sha và authorization_url | GIẾT |
| l06-no-startswith | `url.startswith(TIEN_TO_URL) → True` | 1 · 8/9 · DO ca_b1_rang_l6: AssertionError: url-ngoai: DAT (cần TRUOT) — đủ authorized_head_sha và authorization_url | GIẾT |
| l07-prefix-in | `url.startswith(TIEN_TO_URL) → TIEN_TO_URL in url` | 1 · 8/9 · DO ca_b1_rang_l6: AssertionError: url-nhung: DAT (cần TRUOT) — đủ authorized_head_sha và authorization_url | GIẾT |
| l08-no-fragment | `any(m in url for m in MANH_URL) → True` | 1 · 8/9 · DO ca_b1_rang_l6: AssertionError: url-thieu-manh: DAT (cần TRUOT) — đủ authorized_head_sha và authorization_url | GIẾT |
| l09-remove-fragment-0 | `any(m in url for m in MANH_URL) → any(m in url for m in MANH_URL if m != '#issuecomment-')` | 1 · 5/9 · DO ca_b1_rang_l6: AssertionError: dat-ic: TRUOT (cần DAT) — trượt L-6 ở authorization_url | GIẾT |
| l09-remove-fragment-1 | `any(m in url for m in MANH_URL) → any(m in url for m in MANH_URL if m != '#pullrequestreview-')` | 1 · 8/9 · DO ca_b1_rang_l6: AssertionError: dat-prr: TRUOT (cần DAT) — trượt L-6 ở authorization_url | GIẾT |
| l09-remove-fragment-2 | `any(m in url for m in MANH_URL) → any(m in url for m in MANH_URL if m != '#discussion_r')` | 1 · 8/9 · DO ca_b1_rang_l6: AssertionError: dat-disc: TRUOT (cần DAT) — trượt L-6 ở authorization_url | GIẾT |
| l10-landed-truthy | `landed is not True → not landed` | 1 · 8/9 · DO ca_b1_rang_l6: AssertionError: boqua-chuoi: TRUOT (cần BO_QUA) — trượt L-6 ở authorized_head_sha, authorization_url | GIẾT |
| l11-landed-equality | `landed is not True → landed != True` | 1 · 8/9 · DO ca_b1_rang_l6: AssertionError: boqua-mot: TRUOT (cần BO_QUA) — trượt L-6 ở authorized_head_sha, authorization_url | GIẾT |
| l12-no-root-landed | `landed, cho = doc.get("landed"), "landed (mức gốc)" → landed, cho = None, "landed (mức gốc)"` | 1 · 8/9 · DO ca_b1_rang_l6: AssertionError: goc-hoa: BO_QUA (cần TRUOT) — landed (mức gốc) = None, không phải True | GIẾT |
| l13-sha-unbounded | `RE_SHA = re.compile(r"[0-9a-f]{40}") → RE_SHA = re.compile(r"[0-9a-f]{40,}")` | 1 · 8/9 · DO ca_b1_rang_l6: AssertionError: sha41: DAT (cần TRUOT) — đủ authorized_head_sha và authorization_url | GIẾT |
| l14-no-trailing-slash | `TIEN_TO_URL = "https://github.com/ducthangho/tra-luat/" → TIEN_TO_URL = "https://github.com/ducthangho/tra-luat"` | 1 · 8/9 · DO ca_b1_rang_l6: AssertionError: url-anh-em: DAT (cần TRUOT) — đủ authorized_head_sha và authorization_url | GIẾT |
| l15-priority | `rc = 3 if co_loi else (1 if co_truot else 0) → rc = 1 if co_truot else (3 if co_loi else 0)` | 1 · 8/9 · DO ca_b1b_fail_close: AssertionError: tron: rc 1 (cần 3);  | GIẾT |
| l16-no-exemption-presence | `vang = sorted(k for k in mien_tru if not (root / k).is_file()) → vang = []` | 1 · 8/9 · DO ca_b2_mien_tru_hang: AssertionError: ca B (không có pr672) rc 0 (cần 3 — miễn trừ vắng) | GIẾT |
| l17-no-exemption | `"ops/land/pr672-wp574-land-evidence.yaml": "hồ sơ của packet khác, ghi trước luật L-6; sửa ở packet riêng", → ` | 1 · 8/9 · DO ca_b2_mien_tru_hang: AssertionError: ca A rc 1 (cần 0); pham vi: ops/land/*-land-evidence.yaml (không đệ quy) | GIẾT |
| l18-extra-exemption | `MIEN_TRU = { → MIEN_TRU = { ⏎     "ops/land/extra-land-evidence.yaml": "extra",` | 1 · 8/9 · DO ca_b2_mien_tru_hang: AssertionError: ca A rc 3 (cần 0); yaml (không đệ quy) | GIẾT |
| l19-empty-exemption-reason | `"hồ sơ của packet khác, ghi trước luật L-6; sửa ở packet riêng", → "",` | 1 · 8/9 · DO ca_b2_mien_tru_hang: AssertionError: ca A lý do rỗng: 'MIEN_TRU ops/land/pr672-wp574-land-evidence.yaml —  (trượt L-6 ở authorized_head_sha, authorization_url)' | GIẾT |
| l20-glob-yaml | `thu_muc.glob("*-land-evidence.yaml") → thu_muc.glob("*.yaml")` | 1 · 8/9 · DO ca_b2b_pham_vi: AssertionError: rc 1 (cần 0) | GIẾT |
| l21-glob-recursive | `thu_muc.glob("*-land-evidence.yaml") → thu_muc.rglob("*-land-evidence.yaml")` | 1 · 8/9 · DO ca_b2b_pham_vi: AssertionError: rc 1 (cần 0) | GIẾT |
| l22-empty-reason | `"trượt L-6 ở " + ", ".join(truot) → ""` | 1 · 8/9 · DO ca_b1_rang_l6: AssertionError: sha39: ly_do thiếu authorized_head_sha:  | GIẾT |
| l23-both-keys-reason | `"trượt L-6 ở " + ", ".join(truot) → "authorized_head_sha authorization_url"` | 1 · 8/9 · DO ca_b1_rang_l6: AssertionError: sha39: ly_do nêu thừa authorization_url: authorized_head_sha authorization_url | GIẾT |
| l24-json-glob-suffix | `"phamvi_glob": PHAMVI_GLOB} ⏎  ⏎  ⏎ def main → "phamvi_glob": PHAMVI_GLOB + ".bak"} ⏎  ⏎  ⏎ def main` | 1 · 8/9 · DO ca_glob_token: AssertionError: ops/land/*-land-evidence.yaml.bak | GIẾT |
| l25-text-glob-suffix | `print(f"pham vi: {PHAMVI_GLOB} → print(f"pham vi: {PHAMVI_GLOB}.bak` | 1 · 8/9 · DO ca_glob_token: AssertionError: không có đúng một dòng mang token glob | GIẾT |
| l26-no-root-check | `if not root.is_dir() or not (root / THU_MUC).is_dir(): → if False:` | 1 · 8/9 · DO ca_b7_root_sai: AssertionError: khong-ton-tai: rc 3 (cần 2) | GIẾT |
| h24-json-glob-suffix | `"phamvi_glob": PHAMVI_GLOB} ⏎  ⏎  ⏎ def main → "phamvi_glob": PHAMVI_GLOB + ".bak"} ⏎  ⏎  ⏎ def main` | 1 · 5/6 · DO ca_glob_va_khong_ghi: AssertionError: ops/reviews/**/*HINT.patch.bak | GIẾT |
| h25-text-glob-suffix | `print(f"pham vi: {PHAMVI_GLOB} → print(f"pham vi: {PHAMVI_GLOB}.bak` | 1 · 5/6 · DO ca_glob_va_khong_ghi: AssertionError: không có đúng một dòng mang token glob | GIẾT |
| h26-no-root-check | `if not root.is_dir() or not (root / THU_MUC).is_dir(): → if False:` | 1 · 5/6 · DO ca_b7_root_sai: AssertionError: khong-ton-tai: rc 0 (cần 2) | GIẾT |
| h01-short-label | `if NHAN in van_ban: → if "chưa chạy" in van_ban:` | 1 · 5/6 · DO ca_b4_rang_l5: AssertionError: ops/reviews/b/x-HINT.patch: CO_NHAN (cần KHONG_DU_DIEU_KIEN_PATCH_AS_HINT) | GIẾT |
| h02-no-commit | `if NHAN in van_ban: → if NHAN.removesuffix(" commit") in van_ban:` | 1 · 5/6 · DO ca_b4_rang_l5: AssertionError: ops/reviews/c/HINT.patch: CO_NHAN (cần KHONG_DU_DIEU_KIEN_PATCH_AS_HINT) | GIẾT |
| h03-utf8-replace | `.decode("utf-8") → .decode("utf-8", errors="replace")` | 1 · 5/6 · DO ca_b4_rang_l5: AssertionError: ops/reviews/f/HINT.patch: KHONG_DU_DIEU_KIEN_PATCH_AS_HINT (cần KHONG_DOC_DUOC) | GIẾT |
| h04-oserror-escape | `except OSError as e: → except PermissionError as e:` | 1 · 4/6 · DO ca_b4_rang_l5: JSONDecodeError: Expecting value: line 1 column 1 (char 0) | GIẾT |
| h05-no-strip | `if not van_ban.strip(): → if not van_ban:` | 1 · 5/6 · DO ca_b4_rang_l5: AssertionError: ops/reviews/e/HINT.patch: KHONG_DU_DIEU_KIEN_PATCH_AS_HINT (cần RONG) | GIẾT |
| h06-write-existing-content | `van_ban = tep.read_bytes().decode("utf-8") → van_ban = tep.read_bytes().decode("utf-8") ⏎         tep.write_bytes(tep.read_bytes() + b"\n")` | 1 · 5/6 · DO ca_glob_va_khong_ghi: AssertionError: công cụ đã ghi/sửa tệp (lượt đầu ra chữ) | GIẾT |
| h07-write-json-only | `van_ban = tep.read_bytes().decode("utf-8") → van_ban = tep.read_bytes().decode("utf-8") ⏎         if "--json" in sys.argv: ⏎             tep.write_bytes(tep.read_bytes() + b"\n")` | 1 · 5/6 · DO ca_glob_va_khong_ghi: AssertionError: công cụ đã ghi/sửa tệp (lượt --json): ['ops/reviews/a/HINT.patch', 'ops/reviews/b/x-HINT.patch'] | GIẾT |
| h07-write-text-only | `van_ban = tep.read_bytes().decode("utf-8") → van_ban = tep.read_bytes().decode("utf-8") ⏎         if "--json" not in sys.argv: ⏎             tep.write_bytes(tep.read_bytes() + b"\n")` | 1 · 5/6 · DO ca_glob_va_khong_ghi: AssertionError: công cụ đã ghi/sửa tệp (lượt đầu ra chữ) | GIẾT |
| t01-skip-counted-pass | `bo_qua += 1 → dat += 1` | 1 · 5/6 · DO ca_tu_kiem_bo_qua_symlink: AssertionError: tha=True: ['BO QUA ca_symlink_treo: PermissionError: gia lap', '1/1', 'GOI_CONG_CU 0'] | GIẾT |
| t02-skip-in-total | `tong = len(CA) - bo_qua → tong = len(CA)` | 1 · 0/1, 5/6 · DO ca_tu_kiem_bo_qua_symlink: AssertionError: tha=True: rc 1 (cần 0); BO QUA ca_symlink_treo: PermissionError: gia lap | GIẾT |
| t03-silent-skip | `print(f"BO QUA {ca.__name__}: {e}") → pass` | 1 · 5/6 · DO ca_tu_kiem_bo_qua_symlink: AssertionError: tha=True: thiếu dòng 'BO QUA ca_symlink_treo:': ['0/0', 'GOI_CONG_CU 0'] | GIẾT |
| t04-policy-always-allow | `return os.name == "nt" → return True` | 0 · 6/6 · không ca đỏ | **SỐNG → F752-03** |
| t05-policy-never-allow | `return os.name == "nt" → return False` | 0 · 6/6 · không ca đỏ | **SỐNG → F752-03** |
| t06-policy-inverted | `return os.name == "nt" → return os.name != "nt"` | 0 · 6/6 · không ca đỏ | **SỐNG → F752-03** |
| t07-early-return | `_khong_tao_duoc(f"{type(e).__name__}: {e}") → return` | 1 · 5/6 · DO ca_tu_kiem_bo_qua_symlink: AssertionError: tha=True: ['1/1', 'GOI_CONG_CU 0'] | GIẾT |
| t08-absent-symlink-pass | `_khong_tao_duoc("os.symlink vắng") → return` | 0 · 6/6 · không ca đỏ | **SỐNG → F752-03** |

B3 đo riêng bằng `extra.py`, driver rc 0. “Giết” ở bảng sau là oracle bác đúng vi phạm, không phải cứ công cụ rc khác 0:

| Mutant | rc công cụ | Oracle phát hiện | Kết quả |
|---|---:|---|---|
| b3-no-fragment | 0 | 12 tệp F bị nâng DAT; n_dat 16 → 28 | GIẾT |
| b3-only-pull | 1 | Hai hồ sơ hợp lệ dùng /issues/ thành TRUOT trên cây loại F; n_dat 16 → 14 | GIẾT |
| b3-glob-yaml | 0 | Thêm provenance ngoài glob, len(tep) 39 → 40 trên cây loại F | GIẾT |
| b3-remove-exemption | 1 | Tập MIEN_TRU rỗng, n_mien_tru 1 → 0 | GIẾT |
| b3-add-F-exemptions | 0 | 12 tệp F thành miễn trừ, n_mien_tru 1 → 13 | GIẾT |
| b3-undercount | 1 | n_dat 16 → 14 và n_landed 29 → 27 | GIẾT |

## Findings

### F752-03 [P2] Ca tự kiểm mới bỏ qua hai điều kiện cần khóa của nhánh symlink

**Lớp:** `hint-symlink-tu-kiem-thay-chot-can-do`; nguồn phát sinh: bản vá F752-02 trong `fc1bb3a`. **Vị trí:** `ops/kiem_nhan_hint_test.py:160`–`:174`; hai nhánh được đo ở dòng 84–103. Một lớp, hai biểu hiện: không kiểm policy nền thật và không kiểm API vắng.

Dòng 173 khai ca mới khóa việc “không tạo được symlink” phải bỏ qua tường minh trên Windows hoặc đỏ trên POSIX. Nhưng `_TU_KIEM` luôn gán `os.symlink = _hong` và thay `_cho_phep_bo_qua` bằng `lambda: {tha}`. Do đó tự kiểm đo được xử lý hai giá trị bool đã tiêm cùng nhánh PermissionError; nó không kiểm việc chọn bool đúng nền, và không chạm nhánh `not hasattr(os, "symlink")`.

**Phép đo chạy được:** `python3 -B "$G/focused.py"` và `python3 -B "$G/absent_probe.py"`, cả hai driver rc 0. Từng command subprocess, đường bản sao và output ở `focused.json`/`absent.json`. Các probe thay riêng `m.os` bằng proxy của module, **giữ nguyên `_cho_phep_bo_qua`**; không giả vờ chạy Windows thật.

| Bản được đo | Suite tự đứng bình thường | Tự kiểm mới riêng ca | Probe đối chứng |
|---|---|---|---|
| Bản giao | rc 0, 6/6 | rc 0, 1/1 | POSIX PermissionError/API vắng ⇒ rc 1, 0/1, calls=0; Windows mô phỏng ⇒ BO QUA, rc 0, 0/0, calls=0 |
| `return os.name == "nt"` → `return True` | **rc 0, 6/6** | **rc 0, 1/1** | POSIX PermissionError ⇒ **BO QUA + 5/5, rc 0** ở toàn suite, sai luật “POSIX ⇒ ĐỎ” |
| Cùng anchor → `return False` | **rc 0, 6/6** | **rc 0, 1/1** | Windows mô phỏng PermissionError ⇒ **DO + 5/6, rc 1**, sai nhánh bỏ qua đã khai |
| Cùng anchor → `return os.name != "nt"` | **rc 0, 6/6** | **rc 0, 1/1** | Cả hai chính sách đảo: POSIX xanh 5/5, Windows đỏ 5/6 |
| `_khong_tao_duoc("os.symlink vắng")` → `return` | **rc 0, 6/6** | **rc 0, 1/1** | Khi API vắng: riêng ca **1/1, rc 0, calls=0** trên cả hai tên nền; toàn suite **6/6**, không dòng BO QUA. Khôi phục đúng lớp pass giả của F752-02 mà “ca khóa” vẫn xanh. |

Đầu ra then chốt của mutant API vắng, lấy nguyên ý số liệu từ probe:

```text
mutant-suite rc 0 6/6
mutant-posix-single rc 0 1/1
PROBE {"os_name": "posix", "mode": "absent", "scope": "single", "calls": 0, "case_total": 1, "policy": false}
mutant-posix-self rc 0 1/1
mutant-posix-all rc 0 6/6
```

Đối chứng bản giao cùng probe POSIX API vắng: `DO ca_symlink_treo: AssertionError: nền POSIX không tạo được symlink: os.symlink vắng`, `0/1`, rc 1. Vì vậy lỗi đo được nằm trong **răng của ca tự kiểm được thêm để khóa F752-02**; không khẳng định mã nguyên bản hiện thực thi mutant. Các mutant bộ đếm/nhãn skip (`t01`, `t02`, `t03`, `t07`) bị ca mới giết: nó có răng ở phần accounting, nhưng thiếu đúng phần capability/policy mà lời khai gộp vào.

**Đề xuất sửa, owner Executor #752:**

1. Tại `_TU_KIEM`/`ca_tu_kiem_bo_qua_symlink`, giữ nguyên `_cho_phep_bo_qua`; cung cấp proxy OS của module với `name` lần lượt `nt`/`posix`, và hai trạng thái symlink: có hàm ném PermissionError / không có thuộc tính. Đo riêng giá trị policy nếu cần, nhưng không dùng kết quả policy để tự tính oracle.
2. Khóa bằng bảng kỳ vọng độc lập: POSIX lỗi/vắng phải đỏ 0/1; Windows lỗi/vắng phải BO QUA 0/0; calls=0 ở cả hai. Với suite đầy đủ: 5/6 đỏ hoặc 5/5 có skip riêng. Ca symlink thật vẫn cần gọi công cụ đúng một lần và kiểm rc 3/KHONG_DOC_DUOC.
3. Bốn mutant sống trên phải bị bắt đúng assertion, bản giao xanh. `probe_symlink.py` đã chạy theo cách này và phân biệt được bản giao với các mutant; Executor tự tái dẫn xuất trên cây của mình, không áp mù artifact reviewer.
4. Rủi ro khi sửa: đừng đổi `os.name` của module os toàn cục — pathlib/tempfile có thể khởi tạo kiểu đường dẫn nền khác rồi gây lỗi setup. Proxy cục bộ tránh việc đó. Phân biệt số ca test với số lần gọi CLI; giữ đúng một dòng N/N ở stdout suite, thông báo skip riêng và hoàn trả monkeypatch sau từng probe.

| Slug lớp | Nối lịch sử | Biểu hiện | P cao nhất mở | Điều kiện đóng |
|---|---|---|---|---|
| hint-khong-ghi-chi-so-duong-dan | F752-01 lượt 1 → đã đóng | Sửa byte tại chỗ | không | h06/h07 chết, bản giao xanh |
| hint-symlink-skip-tinh-pass | F752-02 lượt 1 → hành vi sửa; bản vá sinh F752-03 | Ca không chạy bị tính đạt ở bản cũ | liên kết P2 kế tiếp | Giữ đối chứng lỗi/vắng API và accounting; không bỏ lịch sử |
| hint-symlink-tu-kiem-thay-chot-can-do | **F752-03**, sinh từ bản vá F752-02 | Policy bị thay trong test; nhánh API vắng bị dựng thành có | **P2** | Giữ predicate thật, phủ ma trận nền × capability; giết t04/t05/t06/t08 đúng lý do |

Việc tách slug phản ánh cơ chế mới (tự kiểm thay phần cần đo) khác cơ chế cũ (`return` rồi tăng đạt), không xóa quan hệ với F752-02. Không có finding P1/P3 mới trong phạm vi đo.

## chua_do_duoc

- **not_measured:** Windows thật. Ma trận `nt`/`posix` là mô phỏng nhánh Python trên Linux; không xác nhận quyền symlink hay pathlib Windows thật. Symlink treo thực trên Linux đã chạy, công cụ rc 3.
- **not_measured:** CI GitHub, run/attempt/checkout/workflow provenance, remote head, generation/lease còn hạn, approval/land. Assignment cấm mạng; không khai `cross_approved` hay gate xanh toàn phần. Terminal status/rc của launcher lượt review đang chạy phải được bên vận chuyển đọc sau khi lượt kết thúc.
- **not_run:** full `ops/ci_duong_nhanh_test.py`, registry `--chay`, release/LIVE/deploy. Full suite có ca tạo/sửa Git ref; lượt này giữ ràng buộc không sửa ref nên đo riêng k01. Không suy từ k01 rằng toàn bộ gate chỉ đỏ một ca; kết quả các ca khác chưa đo. Đỏ registry và k01 đo được đúng lý do được cho phép, không báo finding cho phần #763.
- **Giới hạn B3:** cây lịch sử/cây loại F là phép chiếu các YAML mức đỉnh `ops/land` (kể cả provenance ngoài glob để phản chứng phạm vi), không full clone. Đã đối chiếu phân loại/đếm trên toàn bộ tập đầu vào land; không chứng nhận mọi tệp ngoài đầu vào bất biến trong một full clone. Mirror thật đã chạy cả công cụ chữ/JSON.
- **Phạm vi đột biến:** 47 chốt suite và sáu chốt B3 ghi rõ ở trên; không tuyên bố phủ mọi đột biến lịch sử của bản tham chiếu spec. Hai lần driver mutant dừng trước thực thi vì anchor cũng có trong docstring (`l03`, `l05`): lỗi setup reviewer, đã siết anchor duy nhất rồi nối tiếp; không tính là finding hay mutant bị giết.
- **Không soạn đầu vào nguy hiểm mới:** chỉ tái dùng fixture sẵn có trong test, gồm thẻ Python/scalar sâu. Các hướng cần đường dẫn thoát cây hoặc payload mới chỉ bàn giao bằng lời: điều phối tự dựng mục được glob chọn dẫn ra ngoài root để đo giới hạn đọc; tự dựng loại tệp đặc biệt hoặc trường hợp cạn tài nguyên để đo khả năng kết thúc/mã lỗi. Không tạo các chuỗi/payload đó trong lượt này.
- **Giới hạn snapshot:** băm bốn file packet, đầu vào hai glob và spec; Git kiểm tracked/untracked/ignored, nhưng không đọc nội dung ignored `.codex/` hoặc tệp bí mật. Không tuyên bố quan sát mọi lần ghi tạm thời trong lịch sử run. Repo nguồn Executor ngoài mirror không thuộc phạm vi.
- **Giới hạn identity:** header CLI chỉ công bố model/effort, không đo từng request; runtime Executor và GitHub submitter chưa xác minh. Verdict này là kết quả review offline exact SHA, không là merge/land authorization.

Artifact evidence — SHA-256:

| Artifact | SHA-256 |
|---|---|
| [reviewlib.py](reviewlib.py) | `13fdf02b29c6110a7fb4b8b8e89cd22a3355a5c41a822bd95e9b70ec8215ab63` |
| [baseline.py](baseline.py) | `555132335a0d69194500d90eb9b4d39783490b115cd67c821882cbbe82cc54d5` |
| [baseline.json](baseline.json) | `d5443f4631f7faa8571d98790500f3f706400392b2d2bcfaa339acb892566556` |
| [independent.py](independent.py) | `a06a8b61dd5cea748d12c5f1d6a70b4e7e69ff087768bc3f04c1eb2d807ff5a5` |
| [independent.json](independent.json) | `c928e43f110d65f13ec03357c554ddddd20dce1ba85aa56a08d5caf033e6560b` |
| [mutations.py](mutations.py) | `0705f94bf39a802dca58efddc763e9efb9f632a976f983ab6b47dd48f23d6178` |
| [mutations.json](mutations.json) | `ae1d60a70df329cb693bd3d1f4facec38a5e9a5f9571037c87859515ea571395` |
| [content_probe.py](content_probe.py) | `57519ae1514af1a12b4a287e3108ba6dfdf836ddb55f62f8a0ef96922fff223b` |
| [content.json](content.json) | `4daac76bac0f1d72e788bff63975d691af8cca882795c44b7b138714ba08db60` |
| [scalar_probe.py](scalar_probe.py) | `96c720b496373aeb39c810405796f4942f6b18125be12d80513ee532a7d8c95c` |
| [scalar.json](scalar.json) | `c28115eeb8e9a864c267313c868034c3031af5001df84ab32cbabd2f6c9f414a` |
| [probe_symlink.py](probe_symlink.py) | `3be6e6a3c840d35151ceb5ce25eb8da7060278bdee21e840ecbe07d9d731a720` |
| [focused.py](focused.py) | `a0e58124ede58b499866635cbed5d1b0a1b2e2aadb34f0d3a02a3900ada6342c` |
| [focused.json](focused.json) | `9674629a25c693121bb725c3dc644ce80091152545c8c7c5cde67176bd2ddb51` |
| [absent_probe.py](absent_probe.py) | `ea6a1faf5590d4f08466574e8a58fb5631c0a7525714a9f66c2fff528d4c1a36` |
| [absent.json](absent.json) | `4fde6398e05478f8e55fa2f2f14cda020708a0491dcc855f78351c6c66d20644` |
| [extra.py](extra.py) | `5e0478a5b2893420fd03eb9500ea1d1c2f5a2cd7a503cb43ae9039d9153a8d50` |
| [extra.json](extra.json) | `3a89149a8d9739db7bf5e45e77dca1974b234d745b7c99e0edf654761f70c7bc` |
| [preflight-extra.json](preflight-extra.json) | `4c1b320f25ceaddf9fce1369a8adeb15b5c32ea174d21d3d9b882731525c0c61` |
| [snapshot-before.json](snapshot-before.json) | `9868b9b0a5e2faac8decc34c4fcd6b6177b7c2bf86ba976eaa5864c978f13422` |
| [snapshot-after.json](snapshot-after.json) | `9868b9b0a5e2faac8decc34c4fcd6b6177b7c2bf86ba976eaa5864c978f13422` |
| [VERDICT-progress.md](VERDICT-progress.md) | `1a13b9c5c28669551fe9111505e74f0fe9268f20c6cbb25ffa1411032314a13e` |
