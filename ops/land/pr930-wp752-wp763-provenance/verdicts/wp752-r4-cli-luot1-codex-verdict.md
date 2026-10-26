---
verdict: changes_requested
reviewed_sha: f9b3dc1ec11a5089b06d67a658e0f840742466eb
spec_sha256: a98d09e86e32ee249668aaa114aed43e8a982e8bd7f9ef81fe61aa6a2a168791
so_p0: 0
so_p1: 0
so_p2: 2
so_p3: 0
---

Kết luận: **2 P2, 2 lớp mới**, đều là lỗ hổng bằng chứng của bộ test HINT. Theo thang chấm trong prompt, hai finding chặn merge. Không tìm được lỗi công cụ nguyên bản qua các phép đo đã chạy. Đỏ đăng ký test theo đường A và nợ dữ liệu land được tách khỏi finding mã.

Review local theo `runs/43502cca/prompt.snapshot`, dùng [skill cross-review](../mirror/.agents/skills/cross-review/SKILL.md). Chỉ ghi vào `/tmp/claude-0/-home-user-tra-luat/8413b80e-5157-5812-ad93-3be1f70600c0/scratchpad/review752cli/goi`. Bản ghi từng bước giữ tại `VERDICT-progress.md`; bản này tổng hợp các phép đo đã hoàn tất.

- Candidate `f9b3dc1ec11a5089b06d67a658e0f840742466eb`, tree `d3c289645d355a07d23c337c3fc235b3bfaed84a`; base diff `1797c32530fba381afd4009340a3fa558b7e37b0`. HEAD detached, khớp đầu/cuối.
- Spec r4 tại `ops/specs/no-p3-cong-cu-ho-so-r4.md`; băm trước khi đọc và cuối lượt đều `a98d09e86e32ee249668aaa114aed43e8a982e8bd7f9ef81fe61aa6a2a168791`. Đã đọc toàn bộ 675 dòng. Nền lịch sử cố định B3 là `1d7e642092fb3dda15967be44d095f37bb22ac5f`, không đồng nhất với base diff được giao.
- Diff đúng 4 tệp mới được giao: `kiem_ho_so_land.py` +141, test +284, `kiem_nhan_hint.py` +78, test +150, đều dưới `ops/`; tổng +653/−0, đạt trần 4 tệp/1.000 dòng. `git diff --check 1797c32530fba381afd4009340a3fa558b7e37b0 f9b3dc1ec11a5089b06d67a658e0f840742466eb` rc 0, output rỗng.
- Reviewer: provider **openai_codex**, surface **codex_cli**, transport **machine**, model **gpt-6-astra**, effort **xhigh**, CLI 0.164.0. Nguồn: header thật `runs/43502cca/stderr.log` dòng 2–13; session `01a170f2-910e-7e83-8b10-0899bb43ce44`. Header xác nhận cấu hình CLI công bố, không đo model từng request. Executor Claude theo assignment; không có runtime receipt Executor trong phạm vi này. Không suy danh tính từ actor GitHub, không tự chuyển state `cross_approved`.
- Review class: khai routine / hiệu lực sensitive theo spec. Không có lease #752 trong `ops/leases` của mirror (`rg` rc 1); generation, lease còn hạn và state server **not_measured**. Authority của lượt này là chỉ thị review offline exact SHA; không chứng nhận điều kiện cấp lease hoặc quyền land.
- Môi trường: Linux x86_64, Python 3.11.17 tại `/usr/local/bin/python3`, PyYAML 6.0.1, git 2.43.0, Ruff 0.16.9; `core.abbrev=7`, origin `https://github.com/ducthangho/tra-luat`. Sandbox công bố workspace-write; mirror được đối xử read-only. Không gọi mạng, push, sửa ref hoặc đọc tệp bí mật.

Mọi test có `-B`, `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=/tmp/claude-0/-home-user-tra-luat/8413b80e-5157-5812-ad93-3be1f70600c0/scratchpad/review752cli/goi/tmp`; Ruff có `--no-cache`. Lệnh tương đối ở bảng đầu chạy từ mirror. Lệnh dùng `goi/*.py` chạy từ thư mục cha mirror hoặc thay bằng đường dẫn tuyệt đối. Script và JSON giữ nguyên trong gói để chạy lại. Các probe có fixture thẻ Python/lồng sâu chỉ tái dùng fixture có sẵn của bộ test; không soạn tải trọng hay đường dẫn thoát cây mới.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Finding P2 comment **4369279124**, nguồn head `5208254`: **ĐÃ VÁ THẬT** trên `f9b3dc1ec11a5089b06d67a658e0f840742466eb`.

Lệnh `python3 -B /tmp/claude-0/-home-user-tra-luat/8413b80e-5157-5812-ad93-3be1f70600c0/scratchpad/review752cli/goi/focused.py` (rc 0) tái dùng nguyên bốn fixture của `ca_b1b_scalar_hong`, so công cụ nguyên bản với đột biến chỉ đổi `except Exception` → `except yaml.YAMLError` quanh `safe_load`:

| Fixture có sẵn | Bản giao | Đột biến hồi quy | Ngoại lệ |
|---|---|---|---|
| thang-13 | rc 3, JSON LOI + DAT | rc 1, traceback, không JSON | ValueError |
| the-timestamp | rc 3, JSON LOI + DAT | rc 1, traceback, không JSON | AttributeError |
| the-int | rc 3, JSON LOI + DAT | rc 1, traceback, không JSON | ValueError |
| long-sau | rc 3, JSON LOI + DAT | rc 1, traceback, không JSON | RecursionError |

Cả bốn bản giao tiếp tục báo tệp tốt, không traceback. Suite gốc `9/9`, rc 0; mutant `l01` bị `ca_b1b_scalar_hong` bắt, `8/9`, rc 1. Không phát hiện lỗi mới cùng cơ chế trong các đầu vào đã đo. Hai lượt connector sau trên f9b3dc1 được prompt ghi không finding; không có finding cũ khác để phân loại. Lịch sử trên GitHub chưa đọc lại do phạm vi offline. Evidence: `focused-results.json` và `mutations.json`.

## Bảng đo lại

| Lệnh | rc thật · bằng chứng dương/đầu ra | Đối chiếu |
|---|---|---|
| `git status --porcelain=v1 --untracked-files=all --ignored=matching` | 0 · !! .codex/ | Chỉ ignored .codex/ có sẵn; tracked/untracked sạch |
| `python3 -B ops/kiem_ho_so_land_test.py` | 0 · 9/9; dòng N/N=[('9', '9')] | passed trong scope đã đo |
| `python3 -B ops/kiem_nhan_hint_test.py` | 0 · 5/5; dòng N/N=[('5', '5')] | passed trong scope đã đo |
| `python3 -B ops/kiem_ho_so_land.py --root . --json` | 1 · {"n_dat": 15, "n_landed": 16, "n_mien_tru": 0, "phamvi_glob": "ops/land/*-land-evidence.yaml", "rc": 1}; len(tep)=65 | Khớp oracle; rc 1 là nợ dữ liệu F |
| `python3 -B ops/kiem_nhan_hint.py --root . --json` | 0 · {"dem": {"CO_NHAN": 26, "KHONG_DU_DIEU_KIEN_PATCH_AS_HINT": 37, "RONG": 2, "KHONG_DOC_DUOC": 0}, "phamvi_glob": "ops/reviews/**/*HINT.patch", "rc": 0}; len(tep)=65 | passed trong scope đã đo |
| `python3 -B ops/kiem_ho_so_land.py --root .` | 1 · pham vi: ops/land/*-land-evidence.yaml (không đệ quy)<br>TỔNG: 15/16 hồ sơ landed True đạt · 0 miễn trừ · rc=1 | Khớp oracle; rc 1 là nợ dữ liệu F |
| `python3 -B ops/kiem_nhan_hint.py --root .` | 0 · pham vi: ops/reviews/**/*HINT.patch<br>ĐẾM: CO_NHAN 26 · KHONG_DU_DIEU_KIEN_PATCH_AS_HINT 37 · RONG 2 · KHONG_DOC_DUOC 0 · tổng 65 · rc=0 | passed trong scope đã đo |
| `python3 -B .claude/dev/ci_dang_ky_test.py` | 1 · ĐỎ: test sống chưa đăng ký: ops/kiem_ho_so_land_test.py<br>ĐỎ: test sống chưa đăng ký: ops/kiem_nhan_hint_test.py<br>ĐĂNG KÝ: 26/24<br>TRẠNG THÁI: chan=24 cach_ly=0<br>LAUNCHER WINDOWS: 4/4 hợp đồng<br>RUFF CI: 3/3 hợp đồng<br>TỔNG: ĐỎ | failed có kiểm soát; đúng hai test chưa đăng ký |
| `ruff --version` | 0 · ruff 0.16.9 | passed trong scope đã đo |
| `ruff check --no-cache --select F ops/kiem_ho_so_land.py ops/kiem_ho_so_land_test.py ops/kiem_nhan_hint.py ops/kiem_nhan_hint_test.py` | 0 · All checks passed! | passed trong scope đã đo |

Log nguyên văn của mỗi dòng ở `logs/<name>.stdout`/`.stderr`, command/rc/hash ở `baseline-receipts.json`. Hai suite mỗi suite có đúng **một** dòng chỉ gồm N/N; 9/9 và 5/5. Ruff lint trên đúng bốn tệp: delta 0 so cơ sở rỗng. `RUFF CI: 3/3 hợp đồng` của registry là phép kiểm cấu trúc riêng, không thay lint thật. Đối chứng Ruff trong `extra_checks.py`: chèn `import fractions` vào bản sao ⇒ rc 1, F401.

`python3 -B ops/ci_duong_nhanh_test.py --mot-ca k01_so_dang_ky_nhan_muc_da_noi` ⇒ rc **3** theo chế độ một ca, đầu ra:

```text
DO:k01_so_dang_ky_nhan_muc_da_noi:so dang ky phai sach, duoc ['test sống chưa đăng ký: ops/kiem_ho_so_land_test.py', 'test sống chưa đăng ký: ops/kiem_nhan_hint_test.py']
```

Đây là đo local ca k01, không phải rc của cả suite hoặc CI thật. Registry và k01 đỏ đúng nguyên nhân được phép trong prompt; không ghi finding cho phần đăng ký thuộc #763.

Phép đo độc lập `python3 -B goi/independent.py` ⇒ rc 0, không import mã packet, đối chiếu từng đường dẫn, trạng thái, lý do hai chiều và bộ đếm. Các cây lịch sử xuất blob Git cục bộ; chỉ tái dựng đầu vào land liên quan, không checkout/sửa ref. `extra_checks.py` giữ thêm YAML provenance ngoài glob để kiểm glob bị nới.

| Cây/đầu vào | Số tệp thuộc glob | DAT / landed / MIEN_TRU | F / BO_QUA | rc công cụ | Đối chiếu |
|---|---:|---|---|---:|---|
| Mirror candidate | 65 | 15 / 16 / 0 | 1 / 49 | 1 | Khớp oracle |
| Base diff 1797c325… | 65 | 15 / 16 / 0 | 1 / 49 | 1 | Khớp oracle |
| Nền cố định 1d7e642… | 51 | 16 / 29 / 1 | 12 / 22 | 1 | Khớp ghim đặc tả |
| Mirror/base, loại đúng F khỏi đầu vào land | 64 | 15 / 15 / 0 | 0 / 49 | 0 | DAT + MIEN_TRU = landed |
| Nền cố định, loại đúng F | 39 | 16 / 17 / 1 | 0 / 22 | 0 | DAT + MIEN_TRU = landed |
| HINT trên mirror | 65 | CO_NHAN 26; thiếu nhãn 37 | RONG 2; KHONG_DOC_DUOC 0 | 0 | Khớp từng tệp và dem của oracle |

Nợ dữ liệu F trên mirror: **`ops/land/pr881-wp852-land-evidence.yaml`**, trượt `authorization_url` (thiếu mảnh URL theo L-6); đã có ở base diff. Owner xử lý: bên ghi sổ hồ sơ land/phiên điều phối, ngoài write set #752. Không sửa hồ sơ, không thêm miễn trừ, không tính đây là finding công cụ. Chi tiết F của nền cố định cũng giữ trong `independent-results.json`.

| Tiêu chí | Phép đo · đầu ra | Kết luận |
|---|---|---|
| B1 | `ca_b1_rang_l6`, 19 fixture; các mutant regex, kiểu SHA, khoá lồng, tiền tố/mảnh URL, truthy và fallback gốc bị bắt. Probe regex nới đo đủ `sha39`, `sha-hoa`, `goc-hoa` lệch. | passed các nhánh đã đo |
| B1b | Ca fail-close, thẻ Python sẵn có, thiếu PyYAML và scalar mới trong suite 9/9; mutant nuốt YAML/đảo rc/thu hẹp catch đỏ đúng nhánh. Bốn scalar có đối chứng riêng ở trên. | passed; không soạn thêm tải trọng |
| B1c | Ca SHA 41, SHA 64, repo anh em và landed số 1 đều có phản chứng làm đỏ; l16/l17/l18/l14 trong bảng đột biến. | passed |
| B2 | CLI không tiêm: ca A MIEN_TRU có lý do; ca B rc 3. Bỏ kiểm tồn tại, gỡ mục, thêm mục và làm rỗng lý do đều đỏ ca B2. | passed |
| B2b | `ca_b2b_pham_vi`: chỉ một hồ sơ đúng phạm vi; đổi *.yaml hoặc rglob đều bị bắt. | passed |
| B3 | Oracle trên mirror, base và nền cố định; đếm/trạng thái/lý do khớp; cây đầu vào loại F rc 0; glob chữ là token và JSON bằng đúng. Sáu probe đột biến B3 đều bị oracle bắt. | passed phạm vi đầu vào công cụ; giới hạn bản sao ghi dưới |
| B4 | `ca_b4_rang_l5`: đủ nhãn, hai mồi, rỗng, LF, UTF-8 hỏng, thư mục; mutant nhãn ngắn/thiếu commit/replace/không strip đỏ. Symlink thật chạy được ở Linux; nhánh thiếu quyền có F752-02. | phân loại passed; reporting skip failed |
| B5 | HINT CLI trên mirror rc 0, đếm 26/37/2/0 khớp oracle, glob chữ/JSON đúng, snapshot Git không delta. Mutant sửa byte giữ tên lọt ca “không ghi”. | công cụ đo được đạt; răng test failed F752-01 |
| B6(a) | Registry rc 1, 26/24, đúng hai dòng ĐỎ đều chỉ hai test của packet. | failed có kiểm soát đúng đường A |
| B6(b) | Ruff 0.16.9 lint thật rc 0; mutant import thừa rc 1/F401. | passed |
| B6(c) | Suite bình thường một dòng 9/9 và một dòng 5/5, rc 0; giả lập thiếu quyền symlink vẫn 5/5 dù bỏ một ca, đơn ca 1/1 dù công cụ gọi 0 lần. | failed nghĩa số ca đạt: F752-02 |
| B6(d) | k01 riêng rc 3, đúng hai lỗi đăng ký; CI GitHub và các ca khác của suite không chạy. | nguyên nhân k01 khớp; tổng gate not_run/not_measured |
| B7 | Mỗi công cụ 3 root sai × chữ/JSON ⇒ rc 2, không dòng đếm; mutant bỏ chốt root bị bắt. | passed |

Snapshot cuối: `git rev-parse HEAD HEAD^{tree}` khớp đầu lượt; `git diff --binary`, `git diff --cached --binary` rỗng, rc 0. `git status --porcelain=v1 --untracked-files=all --ignored=matching` trước/sau cùng chỉ `!! .codex/` (ignored có sẵn), các tệp tracked/untracked không delta. Băm spec không đổi. Evidence `final-snapshot.json`.

## Đột biến

Lệnh `python3 -B goi/mutations.py`: **42 lượt suite**, **41 đỏ**, **1 sống**. Mỗi lượt tạo thư mục bằng `mktemp -d -p goi`, chép cả bốn tệp, đổi đúng một anchor trong công cụ; các test giữ nguyên byte. Sống `h06` là F752-01. Bảng ghi ca đỏ đầu tiên và N/N; stdout đầy đủ cùng mọi ca đỏ khác, stderr, old/new nguyên văn, command và đường dẫn bản sao nằm ở `mutations.json`.

| Tên | Chốt đổi | rc suite · ca đỏ / bằng chứng | Giết/sống |
|---|---|---|---|
| l01-except-yaml-only | `except Exception as e:` → `except yaml.YAMLError as e:` | 1 · DO ca_b1b_scalar_hong: AssertionError: thang-13: rc 1 (cần 3); hon3/dist-packages/yaml/constructor.py", line 330, in construct_yaml_timestamp; 8/9 | GIẾT |
| l02-fullmatch-to-match | `RE_SHA.fullmatch(sha)` → `RE_SHA.match(sha)` | 1 · DO ca_b1_rang_l6: AssertionError: sha-lf: DAT (cần TRUOT) — đủ authorized_head_sha và authorization_url; 8/9 | GIẾT |
| l03-match-dollar | `RE_SHA.fullmatch(sha)` → `re.match(r"[0-9a-f]{40}$", sha)` | 1 · DO ca_b1_rang_l6: AssertionError: sha-lf: DAT (cần TRUOT) — đủ authorized_head_sha và authorization_url; 8/9 | GIẾT |
| l04-regex-relaxed | `re.compile(r"[0-9a-f]{40}")` → `re.compile(r"[0-9a-fA-F]{39,40}")` | 1 · DO ca_b1_rang_l6: AssertionError: sha39: DAT (cần TRUOT) — đủ authorized_head_sha và authorization_url; 8/9 | GIẾT |
| l05-string-coercion | `isinstance(sha, str) and RE_SHA.fullmatch(sha)` → `RE_SHA.fullmatch(str(sha))` | 1 · DO ca_b1_rang_l6: AssertionError: sha-so: DAT (cần TRUOT) — đủ authorized_head_sha và authorization_url; 8/9 | GIẾT |
| l06-nested-keys | `truot = []` → `doc = doc.get("candidates", [doc])[0]     truot = []` | 1 · DO ca_b1_rang_l6: AssertionError: long: DAT (cần TRUOT) — đủ authorized_head_sha và authorization_url; 8/9 | GIẾT |
| l07-no-url-prefix | `url.startswith(TIEN_TO_URL) and` → `(bỏ)` | 1 · DO ca_b1_rang_l6: AssertionError: url-ngoai: DAT (cần TRUOT) — đủ authorized_head_sha và authorization_url; 8/9 | GIẾT |
| l08-in-prefix | `url.startswith(TIEN_TO_URL)` → `(TIEN_TO_URL in url)` | 1 · DO ca_b1_rang_l6: AssertionError: url-nhung: DAT (cần TRUOT) — đủ authorized_head_sha và authorization_url; 8/9 | GIẾT |
| l09-in-without-scheme | `url.startswith(TIEN_TO_URL)` → `(TIEN_TO_URL.removeprefix("https://") in url)` | 1 · DO ca_b1_rang_l6: AssertionError: url-gia: DAT (cần TRUOT) — đủ authorized_head_sha và authorization_url; 8/9 | GIẾT |
| l10-in-without-host | `url.startswith(TIEN_TO_URL)` → `("ducthangho/tra-luat" in url)` | 1 · DO ca_b1_rang_l6: AssertionError: url-ngoai: DAT (cần TRUOT) — đủ authorized_head_sha và authorization_url; 8/9 | GIẾT |
| l11-no-url-fragment | `and any(m in url for m in MANH_URL)` → `(bỏ)` | 1 · DO ca_b1_rang_l6: AssertionError: url-thieu-manh: DAT (cần TRUOT) — đủ authorized_head_sha và authorization_url; 8/9 | GIẾT |
| l12-0-remove-fragment | `any(m in url for m in MANH_URL)` → `any(m in url for m in MANH_URL if m != '#issuecomment-')` | 1 · DO ca_b1_rang_l6: AssertionError: dat-ic: TRUOT (cần DAT) — trượt L-6 ở authorization_url; 5/9 | GIẾT |
| l12-1-remove-fragment | `any(m in url for m in MANH_URL)` → `any(m in url for m in MANH_URL if m != '#pullrequestreview-')` | 1 · DO ca_b1_rang_l6: AssertionError: dat-prr: TRUOT (cần DAT) — trượt L-6 ở authorization_url; 8/9 | GIẾT |
| l12-2-remove-fragment | `any(m in url for m in MANH_URL)` → `any(m in url for m in MANH_URL if m != '#discussion_r')` | 1 · DO ca_b1_rang_l6: AssertionError: dat-disc: TRUOT (cần DAT) — trượt L-6 ở authorization_url; 8/9 | GIẾT |
| l13-truthy-landed | `landed is not True` → `not landed` | 1 · DO ca_b1_rang_l6: AssertionError: boqua-chuoi: TRUOT (cần BO_QUA) — trượt L-6 ở authorized_head_sha, authorization_url; 8/9 | GIẾT |
| l14-equal-landed | `landed is not True` → `landed != True` | 1 · DO ca_b1_rang_l6: AssertionError: boqua-mot: TRUOT (cần BO_QUA) — trượt L-6 ở authorized_head_sha, authorization_url; 8/9 | GIẾT |
| l15-no-root-landed | `doc.get("landed"), "landed (mức gốc)"` → `None, "landed (mức gốc)"` | 1 · DO ca_b1_rang_l6: AssertionError: goc-hoa: BO_QUA (cần TRUOT) — landed (mức gốc) = None, không phải True; 8/9 | GIẾT |
| l16-long-sha | `re.compile(r"[0-9a-f]{40}")` → `re.compile(r"[0-9a-f]{40,}")` | 1 · DO ca_b1_rang_l6: AssertionError: sha41: DAT (cần TRUOT) — đủ authorized_head_sha và authorization_url; 8/9 | GIẾT |
| l17-sha64 | `re.compile(r"[0-9a-f]{40}")` → `re.compile(r"(?:[0-9a-f]{40}\|[0-9a-f]{64})")` | 1 · DO ca_b1_rang_l6: AssertionError: sha64: DAT (cần TRUOT) — đủ authorized_head_sha và authorization_url; 8/9 | GIẾT |
| l18-prefix-no-slash | `url.startswith(TIEN_TO_URL)` → `url.startswith(TIEN_TO_URL.rstrip("/"))` | 1 · DO ca_b1_rang_l6: AssertionError: url-anh-em: DAT (cần TRUOT) — đủ authorized_head_sha và authorization_url; 8/9 | GIẾT |
| l19-swallow-yaml | `return "LOI", f"YAML không đọc được ({type(e).__name__})", False` → `return "BO_QUA", "YAML bỏ qua", False` | 1 · DO ca_b1b_fail_close: AssertionError: yaml-ngoac: rc 0 (cần 3); ; 6/9 | GIẾT |
| l20-rc-priority | `3 if co_loi else (1 if co_truot else 0)` → `1 if co_truot else (3 if co_loi else 0)` | 1 · DO ca_b1b_fail_close: AssertionError: tron: rc 1 (cần 3); ; 8/9 | GIẾT |
| l21-no-exemption-existence | `sorted(k for k in mien_tru if not (root / k).is_file())` → `[]` | 1 · DO ca_b2_mien_tru_hang: AssertionError: ca B (không có pr672) rc 0 (cần 3 — miễn trừ vắng); 8/9 | GIẾT |
| l22-no-pr672 | `"ops/land/pr672-wp574-land-evidence.yaml": "hồ sơ của packet khác, ghi trước luật L-6; sửa ở packet riêng",` → `(bỏ)` | 1 · DO ca_b2_mien_tru_hang: AssertionError: ca A rc 1 (cần 0); pham vi: ops/land/*-land-evidence.yaml (không đệ quy); 8/9 | GIẾT |
| l23-extra-exemption | `MIEN_TRU = {` → `MIEN_TRU = {     "ops/land/extra-land-evidence.yaml": "extra",` | 1 · DO ca_b2_mien_tru_hang: AssertionError: ca A rc 3 (cần 0); yaml (không đệ quy); 8/9 | GIẾT |
| l24-empty-exemption-reason | `"hồ sơ của packet khác, ghi trước luật L-6; sửa ở packet riêng",` → `"",` | 1 · DO ca_b2_mien_tru_hang: AssertionError: ca A lý do rỗng: 'MIEN_TRU ops/land/pr672-wp574-land-evidence.yaml —  (trượt L-6 ở authorized_head_sha, authorization_url)'; 8/9 | GIẾT |
| l25-glob-all-yaml | `thu_muc.glob("*-land-evidence.yaml")` → `thu_muc.glob("*.yaml")` | 1 · DO ca_b2b_pham_vi: AssertionError: rc 1 (cần 0); 8/9 | GIẾT |
| l26-recursive-glob | `thu_muc.glob("*-land-evidence.yaml")` → `thu_muc.rglob("*-land-evidence.yaml")` | 1 · DO ca_b2b_pham_vi: AssertionError: rc 1 (cần 0); 8/9 | GIẾT |
| l28-text-glob-suffix | `print(f"pham vi: {PHAMVI_GLOB}` → `print(f"pham vi: {PHAMVI_GLOB}.bak` | 1 · DO ca_glob_token: AssertionError: không có đúng một dòng mang token glob; 8/9 | GIẾT |
| l29-no-root-check | `if not root.is_dir() or not (root / THU_MUC).is_dir():` → `if False:` | 1 · DO ca_b7_root_sai: AssertionError: khong-ton-tai: rc 3 (cần 2); 8/9 | GIẾT |
| h27-json-glob-suffix | `"phamvi_glob": PHAMVI_GLOB}` → `"phamvi_glob": PHAMVI_GLOB + ".bak"}` | 1 · DO ca_glob_va_khong_ghi: AssertionError: ops/reviews/**/*HINT.patch.bak; 4/5 | GIẾT |
| h28-text-glob-suffix | `print(f"pham vi: {PHAMVI_GLOB}` → `print(f"pham vi: {PHAMVI_GLOB}.bak` | 1 · DO ca_glob_va_khong_ghi: AssertionError: không có đúng một dòng mang token glob; 4/5 | GIẾT |
| h29-no-root-check | `if not root.is_dir() or not (root / THU_MUC).is_dir():` → `if False:` | 1 · DO ca_b7_root_sai: AssertionError: khong-ton-tai: rc 0 (cần 2); 4/5 | GIẾT |
| l27-json-glob-suffix | `"phamvi_glob": PHAMVI_GLOB}   def main` → `"phamvi_glob": PHAMVI_GLOB + ".bak"}   def main` | 1 · DO ca_glob_token: AssertionError: ops/land/*-land-evidence.yaml.bak; 8/9 | GIẾT |
| l30-reason-empty | `"trượt L-6 ở " + ", ".join(truot)` → `""` | 1 · DO ca_b1_rang_l6: AssertionError: sha39: ly_do thiếu authorized_head_sha: ; 8/9 | GIẾT |
| l31-reason-both-keys | `"trượt L-6 ở " + ", ".join(truot)` → `"authorized_head_sha authorization_url"` | 1 · DO ca_b1_rang_l6: AssertionError: sha39: ly_do nêu thừa authorization_url: authorized_head_sha authorization_url; 8/9 | GIẾT |
| h01-short-label | `if NHAN in van_ban:` → `if "chưa chạy" in van_ban:` | 1 · DO ca_b4_rang_l5: AssertionError: ops/reviews/b/x-HINT.patch: CO_NHAN (cần KHONG_DU_DIEU_KIEN_PATCH_AS_HINT); 4/5 | GIẾT |
| h02-label-without-commit | `if NHAN in van_ban:` → `if NHAN.removesuffix(" commit") in van_ban:` | 1 · DO ca_b4_rang_l5: AssertionError: ops/reviews/c/HINT.patch: CO_NHAN (cần KHONG_DU_DIEU_KIEN_PATCH_AS_HINT); 4/5 | GIẾT |
| h03-utf8-replace | `.decode("utf-8")` → `.decode("utf-8", errors="replace")` | 1 · DO ca_b4_rang_l5: AssertionError: ops/reviews/f/HINT.patch: KHONG_DU_DIEU_KIEN_PATCH_AS_HINT (cần KHONG_DOC_DUOC); 4/5 | GIẾT |
| h04-oserror-escape | `except OSError as e:` → `except PermissionError as e:` | 1 · DO ca_b4_rang_l5: JSONDecodeError: Expecting value: line 1 column 1 (char 0); 3/5 (tool ném ngoại lệ đọc tệp nên JSON không có; không phải lỗi setup) | GIẾT |
| h05-no-strip | `if not van_ban.strip():` → `if not van_ban:` | 1 · DO ca_b4_rang_l5: AssertionError: ops/reviews/e/HINT.patch: KHONG_DU_DIEU_KIEN_PATCH_AS_HINT (cần RONG); 4/5 | GIẾT |
| h06-write-existing-content | `van_ban = tep.read_bytes().decode("utf-8")` → `van_ban = tep.read_bytes().decode("utf-8")         tep.write_bytes(tep.read_bytes() + b"\n")` | 0 · không ca đỏ; 5/5 | SỐNG → F752-01 |

Sáu phép B3 bổ sung qua `python3 -B goi/extra_checks.py` (script rc 0); **GIẾT** dưới đây nghĩa oracle phát hiện vi phạm, không đồng nhất với rc của công cụ:

| Tên | rc công cụ | Bằng chứng oracle | Kết quả |
|---|---:|---|---|
| b3-no-fragment | 0 | 12 trạng thái lệch; phần tử thừa []; bộ đếm expected→actual {'n_dat': [16, 28]} | GIẾT |
| b3-remove-exemption | 1 | 1 trạng thái lệch; phần tử thừa []; bộ đếm expected→actual {'n_mien_tru': [1, 0]} | GIẾT |
| b3-all-yaml | 0 | 0 trạng thái lệch; phần tử thừa ['ops/land/pr666-wp650-provenance.yaml']; bộ đếm expected→actual {} | GIẾT |
| b3-add-F-exemptions | 0 | 12 trạng thái lệch; phần tử thừa []; bộ đếm expected→actual {'n_mien_tru': [1, 13]} | GIẾT |
| b3-undercount | 1 | 0 trạng thái lệch; phần tử thừa []; bộ đếm expected→actual {'n_dat': [16, 14], 'n_landed': [29, 27]} | GIẾT |
| b3-only-pull | 1 | 2 trạng thái lệch; phần tử thừa []; bộ đếm expected→actual {'n_dat': [16, 14]} | GIẾT |

## Findings

### F752-01 [P2] Ca “không ghi” bỏ lọt sửa nội dung tệp đã tồn tại

Lớp `hint-khong-ghi-chi-so-duong-dan`; vị trí `ops/kiem_nhan_hint_test.py:105` và `:111–112`.
Ca `ca_glob_va_khong_ghi` tuyên bố đo không ghi tệp nhưng chỉ so danh sách đường dẫn. Đột biến `h06-write-existing-content` thêm một LF vào mỗi HINT đọc được: bộ test vẫn `5/5`, rc 0. `python3 -B goi/focused.py` đo A/B cùng fixture: bản gốc 98 → 98 byte, hash không đổi; mutant 98 → 99 byte, hash đổi, cùng danh sách đường dẫn, CLI vẫn rc 0. Command cụ thể và toàn bộ đầu ra trong `mutations.json`, `focused-results.json`; script tái lập `goi/mutations.py` và `goi/focused.py`.

Đây là lỗi răng của test theo Mục tiêu 3/B5 và thang P2 của prompt, không phải lời cáo buộc công cụ nguyên bản hiện ghi tệp. Sửa tại ca này: so byte/hash các tệp có sẵn cùng tập đường dẫn trước/sau từng lượt chữ và JSON. Khoá bằng mutant sửa nội dung tại chỗ phải đỏ, bản gốc xanh. Tránh hồi quy khi so metadata biến động hoặc theo symlink ra ngoài fixture; dùng byte của các tệp fixture được kiểm soát.

### F752-02 [P2] Ca symlink chưa đo vẫn được tính là đạt

Lớp `hint-symlink-skip-tinh-pass`; vị trí `ops/kiem_nhan_hint_test.py:78`, `:84–85`, `:141–142`.
Khi nền không hỗ trợ symlink hoặc việc tạo symlink ném OSError, ca trả về trước `_chay`, rồi main tăng `dat`. `python3 -B goi/focused.py` giả lập đúng nhánh PermissionError: suite vẫn in `5/5`, rc 0, số lần gọi công cụ từ 5 xuống 4. Khi chỉ chọn ca này, in `1/1`, rc 0, `_chay` gọi **0 lần**. Đây là nhánh skip thực thi có trong mã, không phải kiểm thử Windows thật.

Vi phạm nghĩa “số ca đạt/tổng ca” ở Mục tiêu 4/B6(c) và yêu cầu tách skipped khỏi passed. Sửa ca và bộ đếm: trả trạng thái skip tường minh, không tăng ca đạt; xuất skip riêng và giữ đúng một dòng N/N theo hợp đồng. Nếu symlink là evidence bắt buộc, thiếu capability phải giữ chưa đo/đỏ; nếu không bắt buộc, chỉ đếm ca thực chạy trong N/N và khai riêng phần skip. Test khoá: giả lập lỗi tạo symlink phải cho skipped=1, số lần gọi công cụ ở ca này =0 và không nhận ca ấy là passed; nền hỗ trợ vẫn đo rc 3 thật. Tránh phát sinh hai dòng N/N hoặc biến thiếu capability thành lỗi công cụ.

Phép đo byte của F752-01: SHA-256 trước `a50fea727b2481dae9c107edadcaabb8e2d6a8d8062f7f123098557869025c06`, sau mutant `ed684624d170bb593539d1d66c9a84c959f9a4cfeb4eca8fa8fa3e874d5254f0`; 98 → 99 byte, tập đường dẫn không đổi. Bản gốc cùng fixture giữ nguyên hash và 98 byte. Mutant chỉ ghi vào fixture trong gói.

| Lớp | Finding/biểu hiện | Nguồn | Mức mở | Điều kiện đóng |
|---|---|---|---|---|
| hint-khong-ghi-chi-so-duong-dan | F752-01; sửa byte tại chỗ lọt test | Lượt CLI này trên f9b3dc1ec11a5089b06d67a658e0f840742466eb | P2 | Test so nội dung; mutant h06 đỏ đúng ca, bản gốc xanh |
| hint-symlink-skip-tinh-pass | F752-02; OSError trước đo bị đếm đạt | Lượt CLI này trên f9b3dc1ec11a5089b06d67a658e0f840742466eb | P2 | Skip tách khỏi pass; phản chứng không còn 1/1 khi gọi công cụ 0 lần |

Owner remediation của cả hai: Executor packet #752. Hai cơ chế khác nhau (snapshot nội dung và giao thức trả trạng thái ca test), cần sửa hai chỗ; không gộp để giảm số lớp. Lớp lỗi YAML cũ đã đóng theo mục đối chiếu; không nhập vào hai lớp mới.

## chua_do_duoc

- **not_measured:** CI thật PR #918, run/attempt/checkout/workflow provenance, remote head, điều kiện cấp lease/generation và quyền land; prompt cấm gọi mạng. Không coi gate-registry/gate-ops hoặc job khác của GitHub đã xanh. Verdict này không phải approval/merge authorization.
- **not_run:** toàn bộ `ops/ci_duong_nhanh_test.py`, registry `--chay`, release/LIVE/deploy. Full ci_duong_nhanh dựng Git repo/ref tạm; lượt này giữ ràng buộc không sửa ref và đo riêng k01. Không biết có ca đỏ khác trong toàn bộ gate; không suy từ k01 rằng chỉ có một ca đỏ.
- **not_measured:** Windows thật. Linux chạy ca symlink bình thường; PermissionError là probe mô phỏng nhánh có sẵn, không phải claim đã chạy Windows. Kết quả bị skip trong probe đã tách riêng, không gọi là pass của tính chất symlink.
- Các bản sao B3 là **phép chiếu đầu vào ops/land**, xuất hồ sơ thuộc glob và thêm YAML provenance cho phản chứng glob; không phải clone toàn bộ repository. B3 trên mirror thật đã chạy; trên cây loại F, đã đo tính chất phân loại/đếm của tập đầu vào còn lại. Không chứng nhận mọi tệp ngoài đầu vào không bị thay đổi trong một full clone.
- Không đo bảo vệ trước đường dẫn/symlink thoát khỏi cây, tải trọng thực thi mới, tệp đặc biệt gây chặn đọc hoặc giới hạn tài nguyên mới. Theo mục 5 của prompt, chỉ bàn giao hướng bằng lời: điều phối có thể tự dựng trường hợp một mục được glob chọn dẫn ra ngoài root, rồi đo phạm vi đọc và hành vi từ chối; các loại tệp không phải tệp thường cần đo khả năng kết thúc và mã lỗi. Không đưa chuỗi đường dẫn thoát cây hoặc nội dung tải trọng vào artifact này.
- Snapshot sạch chỉ chứng minh không có delta tracked/untracked quan sát được ở hai mốc. Nội dung ignored `.codex/` không đọc/băm do ràng buộc tệp bí mật; không tuyên bố đã kiểm toàn bộ lịch sử ghi của hệ điều hành.
- Header CLI không chứng minh model từng request; runtime Executor và receipt độc lập của các lượt connector chỉ có lời khai trong prompt. Giữ giới hạn assurance này cho bên điều phối, không tự tạo nhãn state machine.

Artifact evidence (SHA-256; byte đầy đủ ở gói):

| Artifact | SHA-256 |
|---|---|
| [baseline-receipts.json](baseline-receipts.json) | `26fc7ca8860232b57a1fc27dde1c9c3c1856823324199bbbb36cbf2b5f94aad4` |
| [mutations.py](mutations.py) | `ae4bbcc307422e3280f6be767f11eca954f23e2c8f41ac56c4353890c44ade46` |
| [mutations.json](mutations.json) | `56b5126530601629c5b6ecb0f2af2b338ff369679b32c7430632c4c5548867e7` |
| [independent.py](independent.py) | `73ed5d538a5637b8eac915e781b3e02ee3e136c3a2af64bc7b9cd9f0791d7e75` |
| [independent-results.json](independent-results.json) | `c872ef16da8e5af8885b71ba3ce6619107a9fb2311adead5f09a99ebd0e14ffa` |
| [focused.py](focused.py) | `4bfb42f31f0d8fd0643d1dfd92ea9c58eac737aed632976529332b5de1e0f7d8` |
| [focused-results.json](focused-results.json) | `cd50d68b7056a6c2df90fb3d22521f79a706ba8e23d28da739db591a0bf340d7` |
| [extra_checks.py](extra_checks.py) | `32b6244b6e46e7d4982794de9720284949a7d75f21f24ae5be8e992a8b0818e6` |
| [extra-results.json](extra-results.json) | `4e9149791380de0dd786cc73fe5d4c825a17553eb3a564c9aaf2e2f4fa68ee8c` |
| [k01-receipt.json](k01-receipt.json) | `ea53b32124551b03984a46574eca494154fde7afdf7548b83abf8d8305d420bd` |
| [final-snapshot.json](final-snapshot.json) | `8b184bcab5029cf9a1a500bdbac004462f21eaa3b3dc294feb427bed19c72d93` |
