# Handoff — #1240 ASSURANCE-81-MODEL-EFFORT-TUY-CHON r1 g1 (lease `wp1240-r1-g1-claude`)

- Head đã push (một lần): `ecd30737e10cb7cdffe0e17178c28b3a12448874`, base `3163f4d02a583787a9340c63a1f5eebd3780d970`,
  nhánh `agent/wp1240-g1-claude`, PR draft #1249.
- Handoff gate trên Issue: https://github.com/ducthangho/tra-luat/issues/1240#issuecomment-6665153747
- Diff: 4 tệp, +128/−18. Gate tại chỗ: A1–A11 ĐẠT; A7 base = head (98 ĐẠT · 25/28 · 0 vi phạm);
  `land_evidence_nguon_test` CA 23/23 · DOT BIEN 116/116 · TONG: DAT; selftest 1777/1777; release-verify --strict ok 184/184.

## Review Codex offline lượt 1/2 — approve

- Lệnh: `.claude/dev/launcher.py run` → `codex exec -m gpt-6.1-sol -c model_reasoning_effort=xhigh -s workspace-write`,
  workspace = bản clone tại head (origin = URL GitHub thật), `--expected-head ecd3073…`, `--require-clean`,
  `--prompt-file` + `--expected-prompt-sha256 c2682b62265918dd48396797913b3e390d9b6c86883b36295151486e24d1092a`.
- Run `bc004964`: `trang_thai xong`, `ma_thoat 0`, 1032,5 s, `stdout_sha256 cd8fdeed…0b038`, dòng cuối `KET_LUAN: approve`.
  `model_phuc_vu` gpt-6.1-sol, `effort_phuc_vu` xhigh, sandbox `codex-linux-sandbox` — cả ba `DO_DUOC` (trong run.json dưới).
- Lần gọi launcher trước đó dừng ở preflight `CHAN [11]` (origin của clone là đường dẫn cục bộ). Codex chưa được gọi,
  nên lần ấy không tính vào ngân sách lời gọi.
- Windows M3: reviewer chốt `not_required` (A9 = 0).

## F1 (P3) — nợ chuyển sang #1236, KHÔNG rework #1240

Quyết định của phiên điều phối `session_015GtxraXfMD1t2FJLzzGDr4` (05-11-2026 ~18:11Z): land như hiện tại trên `ecd3073`,
ghi nợ. Lý do: P3 là thiếu độ phủ test; hành vi trên head đúng spec; không đáng đổi SHA đã review. Packet #1236 sắp siết
đúng `ops/land_evidence_nguon.py`, nên nợ đi theo packet ấy.

Ca `c23_l7_model_effort_tuy_chon` để sống 7 đột biến do reviewer tự dựng (chỉ trên bản sao tạm). Mỗi fixture khai `DAT`,
`sandbox_mode` measured có nguồn, và chỉ một trong `model`/`effort`. Cột rc là head → mutant.

| mutant sống | giá trị trường đang xét | rc | điều test bỏ sót |
|---|---|---|---|
| `accept_bare_not_measured` | chuỗi `not_measured` (không dấu phân cách) | 1 → 0 | nhận token thiếu dấu phân cách |
| `accept_numeric_string` | chuỗi `"5"` | 1 → 0 | nhận chuỗi số không phải lời khai |
| `accept_whitespace_only` | chuỗi ba dấu cách | 1 → 0 | nhận lời khai chỉ có khoảng trắng |
| `drop_leading_whitespace_not_measured` | `  not_measured — absent` | 0 → 1 | từ chối khoảng trắng đầu hợp lệ |
| `drop_hyphen_delimiter` | `not_measured-absent` | 0 → 1 | từ chối dấu `-` hợp lệ |
| `drop_emdash_delimiter` | `not_measured—absent` | 0 → 1 | từ chối dấu `—` hợp lệ |
| `single_not_measured_requires_peer` | `not_measured — absent`, khoá tuỳ chọn kia vắng | 0 → 1 | ép trường còn lại phải có |

Hướng xử lý (việc của #1236): mở rộng bảng dữ liệu của c23, kiểm riêng mỗi khoá khi khoá kia vắng / measured / not_measured;
thêm ca dương cho khoảng trắng đầu và các dấu phân cách, ca âm cho not_measured trần, chuỗi số có nháy, chuỗi toàn khoảng
trắng; khoá bảy đột biến trên vào `DOT_BIEN`. Giữ sandbox bắt buộc, không đổi ngữ pháp measured/L1 hay `MIEN_TRU_L7`.

Script phản chứng của reviewer (`review_evidence/mutate_patch.py`, `mutation_witnesses.py` cùng các JSON) **không được
lưu vào kho**: chúng nằm ngoài write set của lease. Chúng chỉ còn trong scratch của phiên executor và mất khi container bị thu hồi.

## Hiện vật của run `bc004964` — chép NGUYÊN BYTE

Write set của lease chỉ có tệp này ở phía handoff, nên bốn hiện vật được nhúng vào đây thay vì thành tệp riêng. Nguồn có
thẩm quyền là băm dưới đây. Mỗi khối nằm giữa dòng `~~~~ BEGIN <tên>` và `~~~~ END <tên>`. Byte của hiện vật là mọi
dòng ở giữa, tính cả ký tự xuống dòng cuối nếu tệp gốc có. Tệp gốc không kết thúc bằng xuống dòng thì khối được đánh
dấu `no-final-newline` và bộ tách phải bỏ đúng một `\n` cuối. Kiểm bằng:
`python3 -c 'import re,hashlib,sys;t=open(sys.argv[1],"rb").read();[print(m.group(1).decode(),hashlib.sha256(m.group(3)[:-1] if m.group(2) else m.group(3)).hexdigest()) for m in re.finditer(rb"~~~~ BEGIN (\S+)( no-final-newline)?\n(.*?)~~~~ END \1\n",t,re.S)]' ops/handoff/wp1240-g1-claude.md`

| hiện vật | sha256 | byte |
|---|---|---|
| `VERDICT.md` | `ed49ec20331b700946ec6ff31cab49034ca777722654b40dd8fc5ffb01c8186b` | 16545 |
| `run.json` | `ceca63e81c44c95fc29a320eaf50d6763bb2a6481378d5ff952aff92749fce8c` | 16259 |
| `stdout.log` | `cd8fdeed117d32ee8e21c2d2f027df347297e5963c4318e088e94f5f1df0b038` | 244 |
| `stderr.log` | `1aa26269eb1cc57f86b235a03cda53c004edb5b1e9fc99d4da4f00843293d721` | 39 |

~~~~ BEGIN VERDICT.md
# Cross-review offline — #1240 r1 g1

**Verdict: approve.** Không có finding P1/P2; có F1 mức P3 về độ phủ test. Áp quy tắc của [prompt.snapshot](run/bc004964/prompt.snapshot): P3 không chặn approve. Đây là kết luận review nội dung trên SHA dưới đây, không thay thế authorization/CI/land.

- Reviewed head: `ecd30737e10cb7cdffe0e17178c28b3a12448874`.
- Reviewed tree: `1b18da0468a9b04a2d0d567935157d17f3c5111f`.
- Base: `3163f4d02a583787a9340c63a1f5eebd3780d970`.
- SPEC SHA-256 tự đo: `e7c6707860ba6a7ca6d24b1cadc2510b4b93952048375bdc332e0328d601487e`; byte của SPEC ngoài kho bằng blob đặc tả tại HEAD.
- Provider reviewer: `openai_codex`; bề mặt quan sát được: agent qua API với công cụ thực thi cục bộ. Không tự xác minh attestation CLI/launcher, session/run ID, model hoặc effort phục vụ; các mục ấy là `KHONG_DO_DUOC`.
- Runtime: Linux x86_64, Python 3.13.18, Git 2.43.0, Ruff 0.17.3. Sandbox cấp quyền `workspace-write`, mạng restricted; không gọi mạng trong review. `core.abbrev=7` trước khi chạy cổng.

## Phạm vi và mục tiêu

Nguồn diff là `git -C kho diff 3163f4d02a583787a9340c63a1f5eebd3780d970 ecd30737e10cb7cdffe0e17178c28b3a12448874`. Có đúng bốn tệp:

| Tệp | Thêm | Bớt |
|---|---:|---:|
| `docs/PROTOCOL_DA_PHIEN.md` | 10 | 7 |
| `docs/adr/0065-model-effort-phuc-vu-tuy-chon.md` | 56 | 0 |
| `ops/land_evidence_nguon.py` | 13 | 1 |
| `ops/land_evidence_nguon_test.py` | 49 | 10 |

Tổng **4 tệp, 128 dòng thêm**, đạt trần ≤6/≤450. Cả bốn thuộc write set SPEC/LEASE; handoff mà lease cho phép thêm không xuất hiện trong diff. Đối chiếu mục tiêu 1–4: ADR có đủ sáu ý; protocol đổi §8 mục 1, §8.1 và §20; L7 chỉ giữ sandbox bắt buộc và kiểm riêng hai khoá tuỳ chọn; test có ca hai chiều cùng m1–m3.

`ops/kiem_ho_so_land.py`, `.claude/dev/packet_loop*.py`, `.claude/dev/launcher.py`, `ops/bien_nhan_v2.py`, SPEC và mọi `ops/land/**` đều không đổi trong diff. Không phát sinh trường hợp S1/S2/S3/S5 qua phép đo; đây là lượt đọc/review, không thực thi lease ghi của executor.

## A1–A11

Các lệnh cổng dưới đây chạy từ `kho/`, trừ các script reviewer có tiền tố `review_evidence/`, chạy từ thư mục chứa verdict. Mọi cache/bytecode chủ động được đưa ngoài checkout hoặc tắt. Đo văn bản bằng `measure_static.py`: nối khoảng trắng **trong từng đoạn**, giữ ranh giới dòng trống; §8.1 lấy từ `### 8.1` đến trước `### 8.2`; A2 bỏ dấu nháy ngược.

| Tiêu chí | Lệnh/phép đo đã chạy | Đầu ra rút gọn | Kết quả |
|---|---|---|---|
| A1 | `python3 -B .claude/dev/packet_loop.py adr-song --root .`; đếm dòng `ADR-0065` bằng `measure_static.py` | rc=0; 64 ADR/64 dòng §20; ADR-0065 đúng 1 dòng. Xoá dòng ấy trên bản sao: rc=9, báo thiếu ADR-0065. | ĐẠT |
| A2 | `python3 -B review_evidence/measure_static.py` | Ba cụm dương lần lượt **1,1,1**. BASE: 0,0,0. Đổi “ghi nếu đo được” thành “bắt buộc” trên bản sao: cụm đầu còn 0. | ĐẠT |
| A3 | Cùng phép nối đoạn/giới hạn §8.1 của `measure_static.py` | Hai câu cũ lần lượt **0,0**; BASE là 1,1. | ĐẠT |
| A4 | `python3 -B review_evidence/independent_l7.py`; `c23` trong suite | Hai trường `not_measured — …`, sandbox measured có nguồn: HEAD rc=0, 0 vi phạm; BASE rc=1, 2 vi phạm L7. | ĐẠT |
| A5 | Cùng script, ca `both_absent`, `sandbox_absent`, `sandbox_not_measured` | Chỉ sandbox measured: rc=0; thiếu sandbox hoặc sandbox not_measured: rc=1, đúng 1 vi phạm tại `thuc_thi.sandbox_mode`. | ĐẠT |
| A6 | Cùng script, kiểm riêng từng khoá model/effort | Chuỗi rỗng, `DAT`, số, null, list, mapping, bool, `not_measuredx`, `x not_measured — y` đều rc=1, đúng 1 vi phạm ở khoá tương ứng. Tổng script **51/51** đúng kỳ vọng. | ĐẠT |
| A7 | `python3 -B review_evidence/run_gates.py`: lấy mã BASE bằng `git show`, chạy BASE rồi HEAD với `--root .` trong cùng lệnh; `python3 -B ops/land_evidence_nguon_test.py` | BASE/HEAD rc=0; **98 ĐẠT · 25/28 miễn trừ · 0 vi phạm**; toàn bộ stdout bằng nhau. Suite **CA 23/23, DOT BIEN 116/116, TONG: DAT**. | ĐẠT |
| A8 | `git diff --exit-code 3163f4d02a583787a9340c63a1f5eebd3780d970 ecd30737e10cb7cdffe0e17178c28b3a12448874 -- ops/kiem_ho_so_land.py`; so blob bằng `git rev-parse` | rc=0; cả hai blob là `846f3697dc453f349852a613ed9a2ec7ab369569`. Kiểm lại trên head cuối không đổi. | ĐẠT |
| A9 | `measure_static.py`: `git diff -U0 BASE HEAD -- '*.py'`, lấy dòng thêm, đếm đúng bảy token nền của SPEC | **0** dòng khớp trên 62 dòng Python thêm. Phản chứng thêm dòng có `encoding=` trên bản sao: đếm **1**. | ĐẠT |
| A10 | `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .`; Ruff `check --no-cache --select F` hai tệp trên HEAD và mã BASE; `python3 -B scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json`; selftest, chi tiết bên dưới | Doctrine rc=0: 10 tệp/0 chỗ chép; Ruff hai bản rc=0, delta=0; manifest `ok=true`, **184/184**; selftest sau sửa môi trường **1777/1777**, rc=0 trên bản sao cùng HEAD/tree. | ĐẠT sau sửa môi trường |
| A11 | `measure_static.py` trên ADR đã nối đoạn | Sáu cụm lần lượt **2,1,2,1,4,2**. Xoá mục (iv) trên bản sao: `identity provider` còn 0. | ĐẠT |

Bằng chứng chi tiết: [gates.json](review_evidence/gates.json), [static.json](review_evidence/static.json), [static-mutations.json](review_evidence/static-mutations.json), [A7-suite.stdout](review_evidence/A7-suite.stdout).

### A7: giải thích 96 → 98 và tương thích ngược

Bản BASE được xuất ra `review_evidence/base/ops/land_evidence_nguon.py`, ngoài `kho/`. Cả hai lượt kiểm đều đọc chính cây `kho/` trong một tiến trình điều khiển; stdout có **134 dòng, 8645 byte**, cùng SHA-256 `e0dfd18ef107f091752547d62e5ea1f3c6d40d94fe5ed523e098d2803d2f7aac`. Đã so từng dòng và toàn bộ byte, không chỉ so tổng.

`git ls-tree` đo được 121 hồ sơ ở `b255b0b7131da7f6e026639f6b0da0a06cc68a44`, 123 ở BASE được lease neo. Diff hai mốc thêm `pr1197-wp1099-land-evidence.yaml` và `pr1231-wp1105-land-evidence.yaml`; cả hai ĐẠT ở cả hai lượt. Hồ sơ pr1127 được bổ sung bằng chứng giữa hai mốc, vẫn ĐẠT. Vì miễn trừ vẫn 25 nên 121−25=96, 123−25=98: chênh số trong SPEC được giải thích bằng thay đổi cây trước BASE, không do bản vá L7. Xem [baseline-counts.json](review_evidence/baseline-counts.json) và [A7-comparison.json](review_evidence/A7-comparison.json).

Ngoài 51 ca độc lập, tôi chạy **64 tổ hợp** model/effort/sandbox measured có nguồn, gồm hoa/thường, dấu phân cách và khoảng trắng đầu: tất cả BASE ĐẠT đều HEAD ĐẠT. Không tìm được phản chứng S5. Về mã, mọi chuỗi mà BASE nhận ở model/effort đều đi qua cùng `RE_KHAI_DO.match` trong nhánh đầu của hàm mới; luật L1 và sandbox giữ nguyên. Đây là lập luận bổ sung cho phép đo, không phải chứng minh bằng vét cạn mọi YAML.

### A10: lỗi bootstrap đã xác minh và xử lý

Lượt selftest đầu chạy trực tiếp trong `kho/` trả rc=1, **1775/1777**. Hai ca đỏ duy nhất: `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim`, `r268_l2_trichotomy_theo_trang_thai_object`. `git config --get commit.gpgsign` đo được `true`; hai ca này tạo commit fixture trong kho Git tạm. Chỉ đặt `commit.gpgsign=false` qua môi trường Git của tiến trình test thì cả hai hàm nguyên bản đều trả true; không sửa test hoặc mã sản phẩm. Xem [selftest-git-probe.json](review_evidence/selftest-git-probe.json).

Chạy lại bằng `python3 -B review_evidence/rerun_selftest.py`: clone **cục bộ**, không gọi remote, checkout đúng HEAD/tree nêu trên, đặt `core.abbrev=7`, tắt ký commit chỉ trong môi trường tiến trình test, rồi chạy nguyên lệnh `python3 -B scripts/tl.py --selftest`. Kết quả **1777/1777**, rc=0; tracked diff của bản sao vẫn rỗng. Toàn bộ output và hash ở [selftest-corrected.json](review_evidence/selftest-corrected.json), [A10-selftest-corrected.stdout](review_evidence/A10-selftest-corrected.stdout). Lượt đỏ đầu được giữ nguyên để đối chiếu, không ghi đè thành xanh.

Selftest đầu tự sinh 20 tệp ignored dưới `references/golden/fixtures/` và `scripts/.tl_state/`. Tôi đã ghi băm rồi chuyển đúng các tệp phát sinh ra `review_evidence/selftest-generated/`; không sửa tệp tracked. Lượt chạy lại dùng bản sao tạm để cô lập việc sinh fixture. Đây là giới hạn của kỷ luật checkout read-only trong runtime được giao, đã ghi nhận rõ thay vì khai không từng có ghi. [Manifest tệp sinh ra](review_evidence/selftest-generated-manifest.json).

## Đột biến bổ sung và finding

Đã sao chép riêng mã kiểm ra thư mục `/tmp` rồi mới đột biến. Không vá mã trong `kho/`. `mutate_patch.py` thử **12** đột biến ngoài ba đột biến m1–m3 bắt buộc: **5 bị giết đúng chốt c23**, **7 sống sót**, không có lỗi setup/import được tính là giết.

Năm đột biến bị giết: bắt riêng model buộc lại; bỏ kiểm model; bỏ kiểm effort; từ chối measured ở trường tuỳ chọn; bỏ dấu cách khỏi mẫu not_measured. Với từng mutant sống sót, đã chạy lần lượt cả **23 ca `--mot-ca`**, đều rc=0, kể cả c23. Phạm vi này đo các ca chức năng; audit 116 đột biến đăng ký được chạy một lần trên HEAD nguyên bản. Ba m1–m3 còn được chạy riêng, đều `GIET` với marker `DO:c23...` đúng lý do: [m1-m3.json](review_evidence/m1-m3.json).

### F1 — P3 — c23 chưa phủ hết ngữ pháp và tính độc lập của hai trường tuỳ chọn

- Class slug: `l7-optional-test-input-matrix`; 1 lớp, 7 biểu hiện.
- Vị trí sửa đề xuất: `ops/land_evidence_nguon_test.py:505`, ca `c23_l7_model_effort_tuy_chon`, và bảng `DOT_BIEN` của tệp ấy.
- Tác động hiện tại: khoảng trống hồi quy trong test; 51 ca reviewer trên HEAD hiện tại đều đúng SPEC. Các lỗi dưới đây được đưa vào **bản đột biến tạm** và bộ ca hiện có vẫn để lọt.

Mỗi fixture khai `assurance_81.reviewer_assurance_81: DAT`, `sandbox_mode: "measured — run.json"`, có tệp `run.json` thật trong thư mục provenance của hồ sơ; chỉ khai một trong model/effort theo giá trị ở bảng. Đã lặp cho cả hai khoá, tổng **14 chứng cứ đối nghịch**. Cột rc là HEAD → mutant.

| Mutant sống sót | Giá trị trường đang xét | rc | Điều test bỏ sót |
|---|---|---|---|
| `accept_bare_not_measured` | chuỗi `not_measured` | 1 → 0 | Nhận token thiếu dấu phân cách |
| `accept_numeric_string` | chuỗi `"5"` | 1 → 0 | Nhận chuỗi số không khớp lời khai |
| `accept_whitespace_only` | chuỗi ba dấu cách | 1 → 0 | Nhận lời khai chỉ có khoảng trắng |
| `drop_leading_whitespace_not_measured` | `  not_measured — absent` | 0 → 1 | Từ chối khoảng trắng đầu hợp lệ |
| `drop_hyphen_delimiter` | `not_measured-absent` | 0 → 1 | Từ chối dấu `-` hợp lệ |
| `drop_emdash_delimiter` | `not_measured—absent` | 0 → 1 | Từ chối dấu `—` hợp lệ |
| `single_not_measured_requires_peer` | `not_measured — absent`, khoá tuỳ chọn kia vắng | 0 → 1 | Ép trường còn lại phải có khi khai not_measured |

Phản chứng chạy được, từ thư mục chứa verdict:

```sh
python3 -B review_evidence/mutate_patch.py
python3 -B review_evidence/mutation_witnesses.py
```

Kết quả đã đo: `KILLED: 5, SURVIVED: 7, UNRELATED_FAILURE: 0`; `Witnesses verified: 14`. Cặp neo/thay nguyên văn và rc/stdout của từng ca được giữ trong [mutations.json](review_evidence/mutations.json); đầu vào và đầu ra đối nghịch trong [mutation-witnesses.json](review_evidence/mutation-witnesses.json). Các script chỉ tạo mutant trong thư mục tạm ngoài kho.

Đề xuất vá: mở rộng bảng dữ liệu của c23, kiểm riêng mỗi khoá khi khoá kia vắng/measured/not_measured. Thêm ca dương cho khoảng trắng đầu và các dấu phân cách; ca âm cho not_measured trần, chuỗi số được quote và chuỗi toàn khoảng trắng. Khoá hồi quy bằng bảy mutant trên, đòi rc và đúng đường dẫn/số vi phạm. Rủi ro khi vá test: phải giữ đúng kiểu YAML (chuỗi `"5"` khác số 5), giữ sandbox bắt buộc và không thay ngữ pháp measured/L1 hoặc danh sách miễn trừ. Đây là đề xuất sửa test trong write set; không cần mở rộng luật nhận dữ liệu.

## Đối chiếu văn bản

Không thấy mâu thuẫn cần chặn giữa §8.1 mới và §8 mục 1, §20, §10.2. Câu mới ở §8 mục 1 tạo đúng ngoại lệ Q1 khi không đo được model: ánh xạ họ theo identity của Claude Code/Codex; provider nhiều họ vẫn phải khai model_family. Yêu cầu hai họ độc lập tiếp tục có nghĩa khi áp ánh xạ ấy. §10.2 tiếp tục đòi provenance/exact identity/output của CI; việc model/effort reviewer tuỳ chọn không gỡ các mốc đó. §20 có đúng một dòng ADR-0065 và chỉ đúng cổng L7.

ADR-0065 có đủ (i)–(vi): dòng 23 ghi nếu đo được ở mọi packet; dòng 27 không chặn assurance/landed; dòng 29 giữ các mốc/sandbox; dòng 32 ánh xạ identity provider và ngoại lệ nhiều họ; dòng 37 hồi tố ở packet riêng theo nhóm và Q2; dòng 42 giữ launcher. Hai URL quyết định và đáp án Q1/Q2 có ở đầu ADR. Không thấy mở rộng quyết định ngoài SPEC đã đóng băng. Cụm “hoặc bỏ trống” ở (i) được đọc theo phần “Cổng” dòng 46–48 là được vắng khoá; phần ấy vẫn loại rõ chuỗi rỗng và null.

## Windows M3

**Chốt `not_required`.** Diff không chạm nhóm đường dẫn bắt buộc của bước 2 ADR-0060; A9 đo 0 dòng thêm chứa token nền, và phản chứng `encoding=` làm phép đo đổi thành 1 đúng kỳ vọng. Hai tệp Python thay điều kiện thuần trên chuỗi/kiểu/mapping và ca test, không thêm thao tác OS/path/process/encoding. Sau bước 4 `unknown`, reviewer chốt như trên. Không chạy Windows và không khai Windows đã xanh.

## Bất biến và snapshot cuối

`MIEN_TRU_L7` giữ nguyên ba tên/băm; fingerprint `6b5ef08603e37239742fe5d7fe8cbe933b24e33174cf3af04c453b0e7be83574` khớp BASE và HEAD. Blob L-6 không đổi. Không có thay đổi packet_loop, launcher, hồ sơ land hoặc spec. Snapshot cuối `2026-11-05T18:09:35.715555+00:00`: HEAD/tree khớp đầu; `git diff HEAD`, `git diff --cached`, `git status --short --ignored` đều rỗng. Chỉ cấu hình `core.abbrev=7` được đặt theo chỉ thị trước gate. Xem [final-snapshot.json](review_evidence/final-snapshot.json).

## Những gì KHÔNG ĐO ĐƯỢC / không chạy

- Không xác minh trực tuyến nội dung/actor của comment GitHub, lease, CI PR/CI master, connector hoặc quyền merge/land. Review dùng authority và Q1/Q2 đã cho trong packet offline.
- Không đo Windows thực tế; M3 đã chốt not_required bằng phạm vi diff/A9.
- Không tự đo model/effort/session thực phục vụ lượt reviewer hoặc attestation của launcher; verdict này không tự sinh receipt identity.
- Không chạy phân loại/mở lại hồ sơ hồi tố, kiểm từng biên nhận r24 hoặc xác lập danh sách lô hồi tố; các việc đó thuộc packet riêng theo SPEC.
- Không vét cạn mọi YAML/mutant. Snapshot đầu/cuối sạch không chứng minh không từng có ghi giữa hai mốc; side effect ignored của selftest đầu đã mô tả và lưu băm.

KET_LUAN: approve
~~~~ END VERDICT.md

~~~~ BEGIN run.json no-final-newline
{
  "version": "1.5.0",
  "run_id": "bc004964744a4c7e95f6724045faae29",
  "short_id": "bc004964",
  "ten": "wp1240-g1-codex-luot1",
  "lenh": {
    "chuong_trinh": "codex",
    "so_doi_so": 11,
    "van_tay": "15c6a1461c2fa4e2"
  },
  "trang_thai": "xong",
  "bat_dau_utc": "2026-11-05T17:52:28.911391+00:00",
  "ket_thuc_utc": "2026-11-05T18:09:41.454542+00:00",
  "ma_thoat": 0,
  "ly_do_dung": null,
  "pid": 4664,
  "khoa_danh_tinh": "linux:83742",
  "workspace": "/tmp/claude-0/-home-user-tra-luat/dfca9940-39f8-56e4-a9f4-62b23a5409b2/scratchpad/rv1/kho",
  "head": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
  "ref": "HEAD",
  "remotes": [
    "github.com/ducthangho/tra-luat"
  ],
  "commit_goc": [
    "00dd9d43554c6cd2ed70c5526bbf1f21e76e354d",
    "a5f1c5efc42fe2469c4b687ab16cc014ac923e69",
    "5217887906a354452bcd76b7da23778ec63ecf46",
    "7372ba540ab43f018a531a0dddc67709063b3e56",
    "77c6df0fa3b10a0ae1d0a34dd63fc7da3c72adce",
    "39f21b331a1f46d3c8d6ad3efba9371f1412fc08",
    "36057e8292bcb3b27ceb64b461d7cf29057a8ba3",
    "7009ab94f814fa19d3dc148f1ce074f40fd9031b",
    "227dcdebc62c9275f9df09056f66e2124ed5f14c",
    "b3592bd75d1a68de66b86ae71827937cfb3d5bda",
    "cdc4e80bc439fa974775f319dccac5bf2fc955fe",
    "08af2eb1ee055a77b25b2af16e44dc7386ea7c3f",
    "9f686e6ca93808b0c5b299496a1fc36e505db51c",
    "6c6e3d891274f50a36014cf8cd4440449af8987d",
    "11918650806345013f336dba5a1450ec1aa7478f",
    "786bf3baf5afa9a5735d79cc06e8f2ca23cda6bd",
    "7dcb9d43736b6241c4014c07ef2d6f93f1695da9",
    "186e6d504d4e0648554b2a3de2705e7541207691",
    "ff7f05ff3335d4e02f267d5912d48fa55c6473db",
    "f80924940c706626902090269a4f81b7e5b12da6",
    "cd25aba0fab9831dd7e87ba378b7429fa0602166",
    "36473cdeb9782356fd0a498d516f8e1347934785",
    "0db2b658ff69ea73a1c432cc05d5c372e11fca1a",
    "5e4b1df6d2a2df5b8d7d6d444e0158feacc78d72",
    "f783fbf363047adf9057b34cb06a60c0deed01df",
    "3ba222bc07b9df2bd0580d16853836e0c0d434ae",
    "2575f0f00fe64acdf27d030546ce702ebc05ce6b",
    "eb2160ab0f191fbb1027bb9da22b89426371d9ed",
    "9d7a523e80e91ef6aca2c7935f3ee1813fc369f9",
    "3569472cb9b11e71b3c791725a2ffb416802f975",
    "20ec8d5d0e86cb7dc01f202c7596407a957e5961",
    "e1a933f6d0c5d6953f03f3e84bc836b4e1e7b9fc",
    "7bd692b1b3b38b6890e2bfbb58485aaf5410c197",
    "acbd0008a125d712cbd8919b0382114cf38cdb8d",
    "c78a5d0651dd80023cde04b04c378511d8fb7af0",
    "342e62c7a23fe03780539e2395c1e24832648c91",
    "b2981a0c7a26c486ef5d1356186f9da609a8f6db",
    "d46163d96fe8037f64e44578f7ec6e4156930cb8",
    "60971e659d4ad9e837a4beee134fb90bc9bab730",
    "f8a7829cc44f296c25faf1a6439b603ba840f70b",
    "0a5de491f7a3f7f79f9d648be5d81f9bf06c5cb8",
    "4c53c76d1955595a5659ab577d9dc1b64f9600ad",
    "ff1c6ada836c95e0116d3bfe05550d0735802e07",
    "f81a9c911c22e9afd5fdb437f4661ca240352f84",
    "20bab0447edcc9e60665eb78948acf9f19706faf",
    "999cb6ee709128a06655c40f6273727f4f4c3eb1",
    "6ed7f02b03694298312f660611da6b68bae47a81",
    "177876fabda55cfa6ac18028613361d9b48816cc",
    "6635379ca1cfd9e03fbfac6df98723f248dcd014",
    "d28c4b1062e8505cbdaaf0237fcbe3f9b8ee4705"
  ],
  "worktree_sach": true,
  "so_muc_ban": 0,
  "prompt_sha256": "c2682b62265918dd48396797913b3e390d9b6c86883b36295151486e24d1092a",
  "deadline_utc": null,
  "probe": {
    "workspace": {
      "trang_thai": "DAT",
      "chi_tiet": ".git la thu muc"
    },
    "ghi": {
      "trang_thai": "DAT",
      "chi_tiet": "ghi-readback-xoa thanh cong"
    },
    "spawn": {
      "trang_thai": "DAT",
      "chi_tiet": "rc=0; output=18B"
    }
  },
  "bo_qua_probe_ly_do": null,
  "provider": "openai_codex",
  "execution_surface": "codex_cli",
  "transport": "machine",
  "transport_sha256": "5c77b6e983ee8d667b7b413bbc3827ac244976b4cac9b422afbb6d2e9ae469c6",
  "checkpoint_sha256": "fe576b1778e64f8d3e780f1d0ec750597a835fa13aff07530372f7cadd9fbcf1",
  "prompt_ban_chup": "/tmp/claude-0/-home-user-tra-luat/dfca9940-39f8-56e4-a9f4-62b23a5409b2/scratchpad/rv1/run/bc004964/prompt.snapshot",
  "prompt_kin_hoan_toan": true,
  "model_phuc_vu": [
    {
      "response_id": "resp_09f58c05a8a7fd72016aecc25faf1887d1a81cc084edc93504",
      "model": "gpt-6.1-sol",
      "su_kien": "response.created"
    },
    {
      "response_id": "resp_09f58c05a8a7fd72016aecc260e7d887d194cd27912a9ba1a2",
      "model": "gpt-6.1-sol",
      "su_kien": "response.created"
    },
    {
      "response_id": "resp_09f58c05a8a7fd72016aecc26457a087d1a224ca5aa9aae915",
      "model": "gpt-6.1-sol",
      "su_kien": "response.created"
    },
    {
      "response_id": "resp_09f58c05a8a7fd72016aecc268cda887d18a55e2fef3d8a4c2",
      "model": "gpt-6.1-sol",
      "su_kien": "response.created"
    },
    {
      "response_id": "resp_09f58c05a8a7fd72016aecc26de7a487d19653d45fbb241792",
      "model": "gpt-6.1-sol",
      "su_kien": "response.created"
    },
    {
      "response_id": "resp_09f58c05a8a7fd72016aecc27928e887d1af226be4ba76495d",
      "model": "gpt-6.1-sol",
      "su_kien": "response.created"
    },
    {
      "response_id": "resp_09f58c05a8a7fd72016aecc280a4b887d1a7fa3c302fba2c6d",
      "model": "gpt-6.1-sol",
      "su_kien": "response.created"
    },
    {
      "response_id": "resp_09f58c05a8a7fd72016aecc291e4b887d199813416deffbb5a",
      "model": "gpt-6.1-sol",
      "su_kien": "response.created"
    },
    {
      "response_id": "resp_09f58c05a8a7fd72016aecc2a6bb5887d1847ea1e91f11e8a6",
      "model": "gpt-6.1-sol",
      "su_kien": "response.created"
    },
    {
      "response_id": "resp_09f58c05a8a7fd72016aecc2c25c2087d19f350c5e266405e9",
      "model": "gpt-6.1-sol",
      "su_kien": "response.created"
    },
    {
      "response_id": "resp_09f58c05a8a7fd72016aecc2ce181887d19f457c062575c3e2",
      "model": "gpt-6.1-sol",
      "su_kien": "response.created"
    },
    {
      "response_id": "resp_09f58c05a8a7fd72016aecc2d7f2ac87d19ba6f9a0fd6b91d2",
      "model": "gpt-6.1-sol",
      "su_kien": "response.created"
    },
    {
      "response_id": "resp_09f58c05a8a7fd72016aecc3214a0487d186a0f3c355a6188e",
      "model": "gpt-6.1-sol",
      "su_kien": "response.created"
    },
    {
      "response_id": "resp_09f58c05a8a7fd72016aecc34eaea087d1bf427a3e6e604f01",
      "model": "gpt-6.1-sol",
      "su_kien": "response.created"
    },
    {
      "response_id": "resp_09f58c05a8a7fd72016aecc36a90f887d1aa28eecbd2128bbb",
      "model": "gpt-6.1-sol",
      "su_kien": "response.created"
    },
    {
      "response_id": "resp_09f58c05a8a7fd72016aecc37c1e2487d198ee52ae44ee7197",
      "model": "gpt-6.1-sol",
      "su_kien": "response.created"
    },
    {
      "response_id": "resp_09f58c05a8a7fd72016aecc3aafc9487d1a6b3edca6e49cb1a",
      "model": "gpt-6.1-sol",
      "su_kien": "response.created"
    },
    {
      "response_id": "resp_09f58c05a8a7fd72016aecc3b7fa3087d1ba8a0aef051bc3d7",
      "model": "gpt-6.1-sol",
      "su_kien": "response.created"
    },
    {
      "response_id": "resp_09f58c05a8a7fd72016aecc3cdf82087d1b8894c5932d9b87d",
      "model": "gpt-6.1-sol",
      "su_kien": "response.created"
    },
    {
      "response_id": "resp_09f58c05a8a7fd72016aecc3e17f2487d19e04ba4c6c7d4ce1",
      "model": "gpt-6.1-sol",
      "su_kien": "response.created"
    },
    {
      "response_id": "resp_09f58c05a8a7fd72016aecc3f5454087d18a24c027e61da5b4",
      "model": "gpt-6.1-sol",
      "su_kien": "response.created"
    },
    {
      "response_id": "resp_09f58c05a8a7fd72016aecc408ecb487d1b84d33b1d15055eb",
      "model": "gpt-6.1-sol",
      "su_kien": "response.created"
    },
    {
      "response_id": "resp_09f58c05a8a7fd72016aecc419f0a487d1a635a894fb07fcde",
      "model": "gpt-6.1-sol",
      "su_kien": "response.created"
    },
    {
      "response_id": "resp_09f58c05a8a7fd72016aecc44fe4d887d18c11dd9348f2d9dc",
      "model": "gpt-6.1-sol",
      "su_kien": "response.created"
    },
    {
      "response_id": "resp_09f58c05a8a7fd72016aecc458f76487d19eb98c982a1b2bfe",
      "model": "gpt-6.1-sol",
      "su_kien": "response.created"
    },
    {
      "response_id": "resp_09f58c05a8a7fd72016aecc45ff24887d1bad07090ef94b31c",
      "model": "gpt-6.1-sol",
      "su_kien": "response.created"
    },
    {
      "response_id": "resp_09f58c05a8a7fd72016aecc4714c3487d1953cf6abd40751b5",
      "model": "gpt-6.1-sol",
      "su_kien": "response.created"
    },
    {
      "response_id": "resp_09f58c05a8a7fd72016aecc4852f0087d1a0d7a84cd111e904",
      "model": "gpt-6.1-sol",
      "su_kien": "response.created"
    },
    {
      "response_id": "resp_09f58c05a8a7fd72016aecc4a78f7487d187edfd0e666f4567",
      "model": "gpt-6.1-sol",
      "su_kien": "response.created"
    },
    {
      "response_id": "resp_09f58c05a8a7fd72016aecc4be0db087d1a134e2f6269c29b5",
      "model": "gpt-6.1-sol",
      "su_kien": "response.created"
    },
    {
      "response_id": "resp_09f58c05a8a7fd72016aecc4d8f75c87d1a732a2c250da92aa",
      "model": "gpt-6.1-sol",
      "su_kien": "response.created"
    },
    {
      "response_id": "resp_09f58c05a8a7fd72016aecc5091c4087d1b76765dd41df6acd",
      "model": "gpt-6.1-sol",
      "su_kien": "response.created"
    },
    {
      "response_id": "resp_09f58c05a8a7fd72016aecc52dbec087d1b9c342a8d07f72aa",
      "model": "gpt-6.1-sol",
      "su_kien": "response.created"
    },
    {
      "response_id": "resp_09f58c05a8a7fd72016aecc5473a6887d188f54a5aef87796e",
      "model": "gpt-6.1-sol",
      "su_kien": "response.created"
    },
    {
      "response_id": "resp_09f58c05a8a7fd72016aecc5acbabc87d1a527c4f7e06cf5bd",
      "model": "gpt-6.1-sol",
      "su_kien": "response.created"
    },
    {
      "response_id": "resp_09f58c05a8a7fd72016aecc6250bb487d1bb2cccfed522a898",
      "model": "gpt-6.1-sol",
      "su_kien": "response.created"
    },
    {
      "response_id": "resp_09f58c05a8a7fd72016aecc62f0e9887d188a16d068859686f",
      "model": "gpt-6.1-sol",
      "su_kien": "response.created"
    },
    {
      "response_id": "resp_09f58c05a8a7fd72016aecc64ac5a487d1b11279a22cfc1824",
      "model": "gpt-6.1-sol",
      "su_kien": "response.created"
    },
    {
      "response_id": "resp_09f58c05a8a7fd72016aecc6602ed487d1ada94402c8c39460",
      "model": "gpt-6.1-sol",
      "su_kien": "response.created"
    }
  ],
  "model_phuc_vu_trang_thai": "DO_DUOC",
  "stderr_bo_dong": 397951,
  "stderr_bo_byte": 38779195,
  "effort_phuc_vu": [
    "xhigh"
  ],
  "effort_phuc_vu_trang_thai": "DO_DUOC",
  "sandbox_quan_sat": [
    {
      "chuong_trinh": "codex-linux-sandbox",
      "co": [
        "--command-cwd=to_tien_workspace",
        "--sandbox-policy-cwd=to_tien_workspace"
      ],
      "permission_profile": {
        "file_system": "restricted",
        "loai": "managed",
        "muc": [
          [
            "root",
            "read"
          ],
          [
            "to_tien_workspace",
            "write"
          ],
          [
            "slash_tmp",
            "write"
          ],
          [
            "tmpdir",
            "write"
          ],
          [
            "khac",
            "read"
          ],
          [
            "khac",
            "read"
          ],
          [
            "khac",
            "read"
          ],
          [
            "khac",
            "read"
          ]
        ],
        "network": "restricted"
      },
      "so_lan": 38
    },
    {
      "chuong_trinh": "bwrap",
      "co": [
        "--cap-drop=ALL",
        "--die-with-parent",
        "--new-session",
        "--unshare-ipc",
        "--unshare-net",
        "--unshare-pid",
        "--unshare-user"
      ],
      "gan": [
        [
          "--ro-bind",
          "/"
        ],
        [
          "--bind",
          "/tmp"
        ],
        [
          "--ro-bind",
          "khac"
        ],
        [
          "--bind",
          "to_tien_workspace"
        ]
      ],
      "so_lan": 29
    },
    {
      "chuong_trinh": "codex-linux-sandbox",
      "co": [
        "--apply-seccomp-then-exec",
        "--command-cwd=to_tien_workspace",
        "--sandbox-policy-cwd=to_tien_workspace"
      ],
      "permission_profile": {
        "file_system": "restricted",
        "loai": "managed",
        "muc": [
          [
            "root",
            "read"
          ],
          [
            "to_tien_workspace",
            "write"
          ],
          [
            "slash_tmp",
            "write"
          ],
          [
            "tmpdir",
            "write"
          ],
          [
            "khac",
            "read"
          ],
          [
            "khac",
            "read"
          ],
          [
            "khac",
            "read"
          ],
          [
            "khac",
            "read"
          ]
        ],
        "network": "restricted"
      },
      "so_lan": 24
    },
    {
      "chuong_trinh": "codex-linux-sandbox",
      "co": [
        "--command-cwd=/",
        "--sandbox-policy-cwd=to_tien_workspace"
      ],
      "permission_profile": {
        "file_system": "restricted",
        "loai": "managed",
        "muc": [
          [
            "root",
            "read"
          ],
          [
            "to_tien_workspace",
            "write"
          ],
          [
            "slash_tmp",
            "write"
          ],
          [
            "tmpdir",
            "write"
          ],
          [
            "khac",
            "read"
          ],
          [
            "khac",
            "read"
          ],
          [
            "khac",
            "read"
          ],
          [
            "khac",
            "read"
          ]
        ],
        "network": "restricted"
      },
      "so_lan": 3
    },
    {
      "chuong_trinh": "codex-linux-sandbox",
      "co": [
        "--apply-seccomp-then-exec",
        "--command-cwd=/",
        "--sandbox-policy-cwd=to_tien_workspace"
      ],
      "permission_profile": {
        "file_system": "restricted",
        "loai": "managed",
        "muc": [
          [
            "root",
            "read"
          ],
          [
            "to_tien_workspace",
            "write"
          ],
          [
            "slash_tmp",
            "write"
          ],
          [
            "tmpdir",
            "write"
          ],
          [
            "khac",
            "read"
          ],
          [
            "khac",
            "read"
          ],
          [
            "khac",
            "read"
          ],
          [
            "khac",
            "read"
          ]
        ],
        "network": "restricted"
      },
      "so_lan": 3
    },
    {
      "chuong_trinh": "bwrap",
      "co": [
        "--cap-drop=ALL",
        "--die-with-parent",
        "--new-session",
        "--unshare-ipc",
        "--unshare-net",
        "--unshare-pid",
        "--unshare-user"
      ],
      "gan": [
        [
          "--ro-bind",
          "khac"
        ],
        [
          "--ro-bind",
          "khac"
        ],
        [
          "--ro-bind",
          "khac"
        ],
        [
          "--ro-bind",
          "khac"
        ],
        [
          "--ro-bind",
          "khac"
        ],
        [
          "--ro-bind",
          "khac"
        ],
        [
          "--ro-bind",
          "khac"
        ]
      ],
      "so_lan": 2
    }
  ],
  "sandbox_lech": {
    "chuyen_cha_trong_cay": 0,
    "chuyen_cha_ngoai_cay": 0,
    "cha_con_song": 0,
    "tai_dung": 0,
    "to_tien_doi": 0
  },
  "sandbox_trang_thai": "DO_DUOC",
  "sandbox_gioi_han": "lay mau /proc tu ben ngoai moi 0.2s: lenh ngan hon chu ky co the lot; argv[0] do tien trinh tu khai. DO_DUOC = da THAY co che sandbox voi cac co ghi o day, KHONG chung minh moi lenh deu chay trong no. Lech danh tinh tien trinh (#1105): chuyen cha khi cha cu da mat/Z va cha moi la to tien da xac thuc thi duoc tha; moi lech khac (ke ca chuyen ra ngoai cay hay PID 1) => KHONG_DO_DUOC: co the ha nham mot luot binh thuong, khong bao gio khai manh hon phep do",
  "prompt_ban_chup_da_xoa": true,
  "thoi_luong_giay": 1032.543,
  "stdout_byte": 244,
  "stdout_sha256": "cd8fdeed117d32ee8e21c2d2f027df347297e5963c4318e088e94f5f1df0b038",
  "stderr_byte": 39,
  "stderr_sha256": "1aa26269eb1cc57f86b235a03cda53c004edb5b1e9fc99d4da4f00843293d721"
}
~~~~ END run.json

~~~~ BEGIN stdout.log
Đã ghi [VERDICT.md](/tmp/claude-0/-home-user-tra-luat/dfca9940-39f8-56e4-a9f4-62b23a5409b2/scratchpad/rv1/VERDICT.md). A1–A11 đạt; có một finding P3 về độ phủ test, không có P1/P2. Windows: `not_required`.

KET_LUAN: approve
~~~~ END stdout.log

~~~~ BEGIN stderr.log
Reading additional input from stdin...
~~~~ END stderr.log

## kiem-merge rc=0 trên PR #1249 — readback và đầu ra (đo 2026-11-06 ~01:33Z)

Kết quả: `ĐỦ ĐIỀU KIỆN MERGE trên ecd30737e10cb7cdffe0e17178c28b3a12448874`, rc 0.
Kho đầy đủ (`is-shallow-repository` = false). base = `git merge-base origin/master ecd3073` = `3163f4d`; origin/master lúc đo = `4f03566`.
`run.json`, `stdout.log` là hai hiện vật offline của run `bc004964`, đã nhúng ở mục trên.

Nguồn từng readback (REST GET, chưa qua chuẩn hoá):
- `chu-kho.json`: `issues/comments/6674302414`, comment chủ kho 01:31:53Z, hai dòng `windows: … not_required` · `approve_merge: …`.
- `cn-agg.json`: object gộp `{repo, pr, head_sha, reviews, review_comments, issue_comments}`, dựng từ `pulls/1249/reviews`, `pulls/1249/comments`, `issues/1249/comments` (mỗi endpoint một trang, per_page=100). Phần `items` là nguyên mảng API trả về.
- `cr.json`: `commits/<head>/check-runs?per_page=100`.
- `wr.json`: `actions/runs?head_sha=<head>&per_page=100`.
- `wj.json`: `actions/runs/42081680387/jobs?per_page=100`.
- `ddr.json`: `actions/workflows/ci-dot-bien-du.yml/runs?head_sha=<head>&per_page=100`.
- `ddj.json`: `actions/runs/42092343146/attempts/1/jobs?per_page=100`.
- `lease.yaml`: `git show origin/ops/wp1240-r1-g1-lease:ops/leases/wp1240-r1-g1-claude.yaml`.

Lệnh, chạy từ gốc kho, với các tệp đã tách ra cùng một thư mục:

```
python3 .claude/dev/packet_loop.py kiem-merge --root . --repo ducthangho/tra-luat --pr 1249 \
  --head ecd30737e10cb7cdffe0e17178c28b3a12448874 --base 3163f4d02a583787a9340c63a1f5eebd3780d970 \
  --spec ops/specs/assurance-81-model-effort-tuy-chon-r1.md --lease lease.yaml \
  --workflow-runs wr.json --workflow-jobs wj.json --check-runs cr.json --connector cn-agg.json \
  --offline-run-json run.json --offline-stdout stdout.log \
  --dot-bien-du-runs ddr.json --dot-bien-du-jobs ddj.json --chu-kho-comment chu-kho.json
```

Cùng quy ước khối và cùng lệnh kiểm băm như mục trên.

| hiện vật | sha256 | byte |
|---|---|---|
| `chu-kho.json` | `60c52e8a967a9aa9ee7aeb68e48b7012b0ea9f73f8de9632ca4fc7c2c64bae6b` | 1997 |
| `cn-agg.json` | `b83f13938df4b1afe299f1f70af712b18ee3b9f612d5e2d496fd7c68f5ac4e5d` | 17632 |
| `cr.json` | `e9190e132b4cc8c933691085601643b194497334249454bde20a5d4d9f9b14ff` | 171961 |
| `wr.json` | `49b360be3579e3b858b0f734623a7fe1676764a3b2c4ded8de3b06c9d652d7c4` | 48487 |
| `wj.json` | `1fd9830858575f55cf9d373f5bcaf726b9e8cea6f910db0cc57a12b8380114ec` | 104275 |
| `ddr.json` | `1668e42acb574ab03eb1f6d6c10a034c770805a998d059736775389ade9d5503` | 16160 |
| `ddj.json` | `b5537958262af2fce7122c3c1b333a7f1051176e80c80107fd0245355cc6eb43` | 33644 |
| `lease.yaml` | `7e87c7d34c69ac2bcc86f19ce95eceaebcf47f1d794901511944f3f69bc6b404` | 6382 |
| `output4.txt` | `0c8ced8f207613f759f0ac97971023dff651782e119e4806ac99ae412da89746` | 79 |

~~~~ BEGIN chu-kho.json
{
  "url": "https://api.github.com/repos/ducthangho/tra-luat/issues/comments/6674302414",
  "html_url": "https://github.com/ducthangho/tra-luat/pull/1249#issuecomment-6674302414",
  "issue_url": "https://api.github.com/repos/ducthangho/tra-luat/issues/1249",
  "id": 6674302414,
  "node_id": "IC_kwDOTNeRjc8AAAABjdHFzg",
  "user": {
    "login": "ducthangho",
    "id": 12748935,
    "node_id": "MDQ6VXNlcjEyNzQ4OTM1",
    "avatar_url": "https://avatars.githubusercontent.com/u/12748935?v=4",
    "gravatar_id": "",
    "url": "https://api.github.com/users/ducthangho",
    "html_url": "https://github.com/ducthangho",
    "followers_url": "https://api.github.com/users/ducthangho/followers",
    "following_url": "https://api.github.com/users/ducthangho/following{/other_user}",
    "gists_url": "https://api.github.com/users/ducthangho/gists{/gist_id}",
    "starred_url": "https://api.github.com/users/ducthangho/starred{/owner}{/repo}",
    "subscriptions_url": "https://api.github.com/users/ducthangho/subscriptions",
    "organizations_url": "https://api.github.com/users/ducthangho/orgs",
    "repos_url": "https://api.github.com/users/ducthangho/repos",
    "events_url": "https://api.github.com/users/ducthangho/events{/privacy}",
    "received_events_url": "https://api.github.com/users/ducthangho/received_events",
    "type": "User",
    "user_view_type": "public",
    "site_admin": false
  },
  "created_at": "2026-11-06T01:31:53Z",
  "updated_at": "2026-11-06T01:31:53Z",
  "author_association": "OWNER",
  "body": "windows: ecd30737e10cb7cdffe0e17178c28b3a12448874 not_required\r\napprove_merge: ecd30737e10cb7cdffe0e17178c28b3a12448874",
  "reactions": {
    "url": "https://api.github.com/repos/ducthangho/tra-luat/issues/comments/6674302414/reactions",
    "total_count": 0,
    "+1": 0,
    "-1": 0,
    "laugh": 0,
    "hooray": 0,
    "confused": 0,
    "heart": 0,
    "rocket": 0,
    "eyes": 0
  },
  "performed_via_github_app": null,
  "minimized": null,
  "pin": null
}
~~~~ END chu-kho.json

~~~~ BEGIN cn-agg.json no-final-newline
{
 "repo": "ducthangho/tra-luat",
 "pr": 1249,
 "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
 "reviews": {
  "total_count": 0,
  "items": []
 },
 "review_comments": {
  "total_count": 0,
  "items": []
 },
 "issue_comments": {
  "total_count": 4,
  "items": [
   {
    "url": "https://api.github.com/repos/ducthangho/tra-luat/issues/comments/6665551922",
    "html_url": "https://github.com/ducthangho/tra-luat/pull/1249#issuecomment-6665551922",
    "issue_url": "https://api.github.com/repos/ducthangho/tra-luat/issues/1249",
    "id": 6665551922,
    "node_id": "IC_kwDOTNeRjc8AAAABjUxAMg",
    "user": {
     "login": "ducthangho",
     "id": 12748935,
     "node_id": "MDQ6VXNlcjEyNzQ4OTM1",
     "avatar_url": "https://avatars.githubusercontent.com/u/12748935?v=4",
     "gravatar_id": "",
     "url": "https://api.github.com/users/ducthangho",
     "html_url": "https://github.com/ducthangho",
     "followers_url": "https://api.github.com/users/ducthangho/followers",
     "following_url": "https://api.github.com/users/ducthangho/following{/other_user}",
     "gists_url": "https://api.github.com/users/ducthangho/gists{/gist_id}",
     "starred_url": "https://api.github.com/users/ducthangho/starred{/owner}{/repo}",
     "subscriptions_url": "https://api.github.com/users/ducthangho/subscriptions",
     "organizations_url": "https://api.github.com/users/ducthangho/orgs",
     "repos_url": "https://api.github.com/users/ducthangho/repos",
     "events_url": "https://api.github.com/users/ducthangho/events{/privacy}",
     "received_events_url": "https://api.github.com/users/ducthangho/received_events",
     "type": "User",
     "user_view_type": "public",
     "site_admin": false
    },
    "created_at": "2026-11-05T18:10:28Z",
    "updated_at": "2026-11-05T18:10:28Z",
    "body": "@codex review\n\nHead `ecd30737e10cb7cdffe0e17178c28b3a12448874`. Spec `ops/specs/assurance-81-model-effort-tuy-chon-r1.md` (packet #1240, sensitive).\n\n---\n_Generated by [Claude Code](https://claude.ai/code)_",
    "author_association": "OWNER",
    "reactions": {
     "url": "https://api.github.com/repos/ducthangho/tra-luat/issues/comments/6665551922/reactions",
     "total_count": 0,
     "+1": 0,
     "-1": 0,
     "laugh": 0,
     "hooray": 0,
     "confused": 0,
     "heart": 0,
     "rocket": 0,
     "eyes": 0
    },
    "performed_via_github_app": {
     "id": 1236702,
     "client_id": "Iv23liqTIFEtdIu6Vn1r",
     "slug": "claude",
     "node_id": "A_kwHOBIuudM4AEt7e",
     "owner": {
      "login": "anthropics",
      "id": 76263028,
      "node_id": "MDEyOk9yZ2FuaXphdGlvbjc2MjYzMDI4",
      "avatar_url": "https://avatars.githubusercontent.com/u/76263028?v=4",
      "gravatar_id": "",
      "url": "https://api.github.com/users/anthropics",
      "html_url": "https://github.com/anthropics",
      "followers_url": "https://api.github.com/users/anthropics/followers",
      "following_url": "https://api.github.com/users/anthropics/following{/other_user}",
      "gists_url": "https://api.github.com/users/anthropics/gists{/gist_id}",
      "starred_url": "https://api.github.com/users/anthropics/starred{/owner}{/repo}",
      "subscriptions_url": "https://api.github.com/users/anthropics/subscriptions",
      "organizations_url": "https://api.github.com/users/anthropics/orgs",
      "repos_url": "https://api.github.com/users/anthropics/repos",
      "events_url": "https://api.github.com/users/anthropics/events{/privacy}",
      "received_events_url": "https://api.github.com/users/anthropics/received_events",
      "type": "Organization",
      "user_view_type": "public",
      "site_admin": false
     },
     "name": "Claude",
     "description": "Run Claude Code from your GitHub Pull Requests and Issues to respond to reviewer feedback, fix CI errors, or modify code, turning it into a virtual teammate that works alongside your development pipelines.\r\n\r\nThis is built on the publicly available Claude Code SDK.",
     "external_url": "https://anthropic.com/claude-code",
     "html_url": "https://github.com/apps/claude",
     "created_at": "2025-04-30T17:54:24Z",
     "updated_at": "2026-11-01T18:14:07Z",
     "permissions": {
      "actions": "write",
      "administration": "read",
      "checks": "write",
      "contents": "write",
      "discussions": "write",
      "issues": "write",
      "members": "read",
      "merge_queues": "read",
      "metadata": "read",
      "pull_requests": "write",
      "repository_hooks": "write",
      "statuses": "read",
      "workflows": "write"
     },
     "events": [
      "branch_protection_rule",
      "check_run",
      "check_suite",
      "commit_comment",
      "discussion",
      "discussion_comment",
      "issues",
      "issue_comment",
      "merge_group",
      "merge_queue_entry",
      "pull_request",
      "pull_request_review",
      "pull_request_review_comment",
      "pull_request_review_thread",
      "push",
      "release",
      "repository_ruleset",
      "status",
      "sub_issues"
     ]
    },
    "minimized": null
   },
   {
    "url": "https://api.github.com/repos/ducthangho/tra-luat/issues/comments/6665558517",
    "html_url": "https://github.com/ducthangho/tra-luat/pull/1249#issuecomment-6665558517",
    "issue_url": "https://api.github.com/repos/ducthangho/tra-luat/issues/1249",
    "id": 6665558517,
    "node_id": "IC_kwDOTNeRjc8AAAABjUxZ9Q",
    "user": {
     "login": "chatgpt-codex-connector[bot]",
     "id": 199175422,
     "node_id": "BOT_kgDOC98s_g",
     "avatar_url": "https://avatars.githubusercontent.com/in/1144995?v=4",
     "gravatar_id": "",
     "url": "https://api.github.com/users/chatgpt-codex-connector%5Bbot%5D",
     "html_url": "https://github.com/apps/chatgpt-codex-connector",
     "followers_url": "https://api.github.com/users/chatgpt-codex-connector%5Bbot%5D/followers",
     "following_url": "https://api.github.com/users/chatgpt-codex-connector%5Bbot%5D/following{/other_user}",
     "gists_url": "https://api.github.com/users/chatgpt-codex-connector%5Bbot%5D/gists{/gist_id}",
     "starred_url": "https://api.github.com/users/chatgpt-codex-connector%5Bbot%5D/starred{/owner}{/repo}",
     "subscriptions_url": "https://api.github.com/users/chatgpt-codex-connector%5Bbot%5D/subscriptions",
     "organizations_url": "https://api.github.com/users/chatgpt-codex-connector%5Bbot%5D/orgs",
     "repos_url": "https://api.github.com/users/chatgpt-codex-connector%5Bbot%5D/repos",
     "events_url": "https://api.github.com/users/chatgpt-codex-connector%5Bbot%5D/events{/privacy}",
     "received_events_url": "https://api.github.com/users/chatgpt-codex-connector%5Bbot%5D/received_events",
     "type": "Bot",
     "user_view_type": "public",
     "site_admin": false
    },
    "created_at": "2026-11-05T18:10:48Z",
    "updated_at": "2026-11-05T18:14:54Z",
    "body": "<!-- codex-pull-request-review-summary -->\n<!-- codex-review-state:v1 {\"code_review\":{\"commit_sha\":\"ecd30737e10cb7cdffe0e17178c28b3a12448874\",\"has_any_findings\":false,\"has_unresolved_findings\":false,\"status\":\"completed\"},\"security_review\":{\"commit_sha\":null,\"has_any_findings\":null,\"has_unresolved_findings\":null,\"status\":null}} -->\n\n## Codex Review Summary\n\nThis comment shows the latest Codex review activity on this pull request.\n\n| Review | Status | Commit | Review trigger |\n| --- | --- | --- | --- |\n| 📝 **Code Review** | ✅ **Completed** <relative-time datetime=\"2026-11-05T18:14:53.606251Z\">2026-11-05T18:14:53.606251Z</relative-time> | `ecd3073` | Manual request |\n\n\n\n<details> <summary>ℹ️ About Codex in GitHub</summary>\n<br/>\n\n[Your team has set up Codex to review pull requests in this repo](https://chatgpt.com/codex/cloud/settings/general). Reviews are triggered when you\n- Open a pull request for review\n- Mark a draft as ready\n- Comment \"@codex review\" or \"@codex security review\".\n\nCodex reacts with 👀 while any review is running, comments if it has suggestions, and reacts with 👍 once all reviews finish with no findings.\n\n</details>",
    "author_association": "NONE",
    "reactions": {
     "url": "https://api.github.com/repos/ducthangho/tra-luat/issues/comments/6665558517/reactions",
     "total_count": 0,
     "+1": 0,
     "-1": 0,
     "laugh": 0,
     "hooray": 0,
     "confused": 0,
     "heart": 0,
     "rocket": 0,
     "eyes": 0
    },
    "performed_via_github_app": {
     "id": 1144995,
     "client_id": "Iv23liVemv8A9if9v0F2",
     "slug": "chatgpt-codex-connector",
     "node_id": "A_kwHOAOQ6Gs4AEXij",
     "owner": {
      "login": "openai",
      "id": 14957082,
      "node_id": "MDEyOk9yZ2FuaXphdGlvbjE0OTU3MDgy",
      "avatar_url": "https://avatars.githubusercontent.com/u/14957082?v=4",
      "gravatar_id": "",
      "url": "https://api.github.com/users/openai",
      "html_url": "https://github.com/openai",
      "followers_url": "https://api.github.com/users/openai/followers",
      "following_url": "https://api.github.com/users/openai/following{/other_user}",
      "gists_url": "https://api.github.com/users/openai/gists{/gist_id}",
      "starred_url": "https://api.github.com/users/openai/starred{/owner}{/repo}",
      "subscriptions_url": "https://api.github.com/users/openai/subscriptions",
      "organizations_url": "https://api.github.com/users/openai/orgs",
      "repos_url": "https://api.github.com/users/openai/repos",
      "events_url": "https://api.github.com/users/openai/events{/privacy}",
      "received_events_url": "https://api.github.com/users/openai/received_events",
      "type": "Organization",
      "user_view_type": "public",
      "site_admin": false
     },
     "name": "ChatGPT Codex Connector",
     "description": "Bring ChatGPT and Codex to your GitHub repositories.",
     "external_url": "https://www.chatgpt.com",
     "html_url": "https://github.com/apps/chatgpt-codex-connector",
     "created_at": "2025-02-14T01:37:05Z",
     "updated_at": "2026-09-23T18:52:59Z",
     "permissions": {
      "actions": "write",
      "checks": "read",
      "contents": "write",
      "emails": "read",
      "issues": "write",
      "metadata": "read",
      "pull_requests": "write",
      "statuses": "read",
      "workflows": "write"
     },
     "events": [
      "check_run",
      "check_suite",
      "commit_comment",
      "issues",
      "issue_comment",
      "pull_request",
      "pull_request_review",
      "pull_request_review_comment",
      "pull_request_review_thread",
      "repository",
      "status",
      "sub_issues"
     ]
    },
    "minimized": null
   },
   {
    "url": "https://api.github.com/repos/ducthangho/tra-luat/issues/comments/6665640232",
    "html_url": "https://github.com/ducthangho/tra-luat/pull/1249#issuecomment-6665640232",
    "issue_url": "https://api.github.com/repos/ducthangho/tra-luat/issues/1249",
    "id": 6665640232,
    "node_id": "IC_kwDOTNeRjc8AAAABjU2ZKA",
    "user": {
     "login": "chatgpt-codex-connector[bot]",
     "id": 199175422,
     "node_id": "BOT_kgDOC98s_g",
     "avatar_url": "https://avatars.githubusercontent.com/in/1144995?v=4",
     "gravatar_id": "",
     "url": "https://api.github.com/users/chatgpt-codex-connector%5Bbot%5D",
     "html_url": "https://github.com/apps/chatgpt-codex-connector",
     "followers_url": "https://api.github.com/users/chatgpt-codex-connector%5Bbot%5D/followers",
     "following_url": "https://api.github.com/users/chatgpt-codex-connector%5Bbot%5D/following{/other_user}",
     "gists_url": "https://api.github.com/users/chatgpt-codex-connector%5Bbot%5D/gists{/gist_id}",
     "starred_url": "https://api.github.com/users/chatgpt-codex-connector%5Bbot%5D/starred{/owner}{/repo}",
     "subscriptions_url": "https://api.github.com/users/chatgpt-codex-connector%5Bbot%5D/subscriptions",
     "organizations_url": "https://api.github.com/users/chatgpt-codex-connector%5Bbot%5D/orgs",
     "repos_url": "https://api.github.com/users/chatgpt-codex-connector%5Bbot%5D/repos",
     "events_url": "https://api.github.com/users/chatgpt-codex-connector%5Bbot%5D/events{/privacy}",
     "received_events_url": "https://api.github.com/users/chatgpt-codex-connector%5Bbot%5D/received_events",
     "type": "Bot",
     "user_view_type": "public",
     "site_admin": false
    },
    "created_at": "2026-11-05T18:14:52Z",
    "updated_at": "2026-11-05T18:14:52Z",
    "body": "<!-- codex-review-receipt:v1 -->\n\nCodex Review: Didn't find any major issues. Can't wait for the next one!\n\n**Reviewed commit:** `ecd30737e1`\n\n<details> <summary>ℹ️ About Codex in GitHub</summary>\n<br/>\n\n[Your team has set up Codex to review pull requests in this repo](https://chatgpt.com/codex/cloud/settings/general). Reviews are triggered when you\n- Open a pull request for review\n- Mark a draft as ready\n- Comment \"@codex review\".\n\nIf Codex has suggestions, it will comment; otherwise it will react with 👍.\n\n\n\n\nCodex can also answer questions or update the PR. Try commenting \"@codex address that feedback\".\n            \n</details>",
    "author_association": "NONE",
    "reactions": {
     "url": "https://api.github.com/repos/ducthangho/tra-luat/issues/comments/6665640232/reactions",
     "total_count": 0,
     "+1": 0,
     "-1": 0,
     "laugh": 0,
     "hooray": 0,
     "confused": 0,
     "heart": 0,
     "rocket": 0,
     "eyes": 0
    },
    "performed_via_github_app": {
     "id": 1144995,
     "client_id": "Iv23liVemv8A9if9v0F2",
     "slug": "chatgpt-codex-connector",
     "node_id": "A_kwHOAOQ6Gs4AEXij",
     "owner": {
      "login": "openai",
      "id": 14957082,
      "node_id": "MDEyOk9yZ2FuaXphdGlvbjE0OTU3MDgy",
      "avatar_url": "https://avatars.githubusercontent.com/u/14957082?v=4",
      "gravatar_id": "",
      "url": "https://api.github.com/users/openai",
      "html_url": "https://github.com/openai",
      "followers_url": "https://api.github.com/users/openai/followers",
      "following_url": "https://api.github.com/users/openai/following{/other_user}",
      "gists_url": "https://api.github.com/users/openai/gists{/gist_id}",
      "starred_url": "https://api.github.com/users/openai/starred{/owner}{/repo}",
      "subscriptions_url": "https://api.github.com/users/openai/subscriptions",
      "organizations_url": "https://api.github.com/users/openai/orgs",
      "repos_url": "https://api.github.com/users/openai/repos",
      "events_url": "https://api.github.com/users/openai/events{/privacy}",
      "received_events_url": "https://api.github.com/users/openai/received_events",
      "type": "Organization",
      "user_view_type": "public",
      "site_admin": false
     },
     "name": "ChatGPT Codex Connector",
     "description": "Bring ChatGPT and Codex to your GitHub repositories.",
     "external_url": "https://www.chatgpt.com",
     "html_url": "https://github.com/apps/chatgpt-codex-connector",
     "created_at": "2025-02-14T01:37:05Z",
     "updated_at": "2026-09-23T18:52:59Z",
     "permissions": {
      "actions": "write",
      "checks": "read",
      "contents": "write",
      "emails": "read",
      "issues": "write",
      "metadata": "read",
      "pull_requests": "write",
      "statuses": "read",
      "workflows": "write"
     },
     "events": [
      "check_run",
      "check_suite",
      "commit_comment",
      "issues",
      "issue_comment",
      "pull_request",
      "pull_request_review",
      "pull_request_review_comment",
      "pull_request_review_thread",
      "repository",
      "status",
      "sub_issues"
     ]
    },
    "minimized": null
   },
   {
    "url": "https://api.github.com/repos/ducthangho/tra-luat/issues/comments/6674302414",
    "html_url": "https://github.com/ducthangho/tra-luat/pull/1249#issuecomment-6674302414",
    "issue_url": "https://api.github.com/repos/ducthangho/tra-luat/issues/1249",
    "id": 6674302414,
    "node_id": "IC_kwDOTNeRjc8AAAABjdHFzg",
    "user": {
     "login": "ducthangho",
     "id": 12748935,
     "node_id": "MDQ6VXNlcjEyNzQ4OTM1",
     "avatar_url": "https://avatars.githubusercontent.com/u/12748935?v=4",
     "gravatar_id": "",
     "url": "https://api.github.com/users/ducthangho",
     "html_url": "https://github.com/ducthangho",
     "followers_url": "https://api.github.com/users/ducthangho/followers",
     "following_url": "https://api.github.com/users/ducthangho/following{/other_user}",
     "gists_url": "https://api.github.com/users/ducthangho/gists{/gist_id}",
     "starred_url": "https://api.github.com/users/ducthangho/starred{/owner}{/repo}",
     "subscriptions_url": "https://api.github.com/users/ducthangho/subscriptions",
     "organizations_url": "https://api.github.com/users/ducthangho/orgs",
     "repos_url": "https://api.github.com/users/ducthangho/repos",
     "events_url": "https://api.github.com/users/ducthangho/events{/privacy}",
     "received_events_url": "https://api.github.com/users/ducthangho/received_events",
     "type": "User",
     "user_view_type": "public",
     "site_admin": false
    },
    "created_at": "2026-11-06T01:31:53Z",
    "updated_at": "2026-11-06T01:31:53Z",
    "body": "windows: ecd30737e10cb7cdffe0e17178c28b3a12448874 not_required\r\napprove_merge: ecd30737e10cb7cdffe0e17178c28b3a12448874",
    "author_association": "OWNER",
    "reactions": {
     "url": "https://api.github.com/repos/ducthangho/tra-luat/issues/comments/6674302414/reactions",
     "total_count": 0,
     "+1": 0,
     "-1": 0,
     "laugh": 0,
     "hooray": 0,
     "confused": 0,
     "heart": 0,
     "rocket": 0,
     "eyes": 0
    },
    "performed_via_github_app": null,
    "minimized": null
   }
  ]
 }
}
~~~~ END cn-agg.json

~~~~ BEGIN cr.json
{
  "total_count": 34,
  "check_runs": [
    {
      "id": 127489703361,
      "name": "dot-bien-gop",
      "node_id": "CR_kwDOTNeRjc8AAAAdrvp9wQ",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "external_id": "d4496ae2-ace5-53ba-a088-a487481b793f",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127489703361",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42092343146/job/127489703361",
      "details_url": "https://github.com/ducthangho/tra-luat/actions/runs/42092343146/job/127489703361",
      "status": "completed",
      "conclusion": "success",
      "started_at": "2026-11-05T19:46:18Z",
      "completed_at": "2026-11-05T19:46:28Z",
      "output": {
        "title": null,
        "summary": null,
        "text": null,
        "annotations_count": 2,
        "annotations_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127489703361/annotations"
      },
      "check_suite": {
        "id": 114059822218
      },
      "app": {
        "id": 15368,
        "client_id": "Iv1.05c79e9ad1f6bdfa",
        "slug": "github-actions",
        "node_id": "MDM6QXBwMTUzNjg=",
        "owner": {
          "login": "github",
          "id": 9919,
          "node_id": "MDEyOk9yZ2FuaXphdGlvbjk5MTk=",
          "avatar_url": "https://avatars.githubusercontent.com/u/9919?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/github",
          "html_url": "https://github.com/github",
          "followers_url": "https://api.github.com/users/github/followers",
          "following_url": "https://api.github.com/users/github/following{/other_user}",
          "gists_url": "https://api.github.com/users/github/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/github/subscriptions",
          "organizations_url": "https://api.github.com/users/github/orgs",
          "repos_url": "https://api.github.com/users/github/repos",
          "events_url": "https://api.github.com/users/github/events{/privacy}",
          "received_events_url": "https://api.github.com/users/github/received_events",
          "type": "Organization",
          "user_view_type": "public",
          "site_admin": false
        },
        "name": "GitHub Actions",
        "description": "Automate your workflow from idea to production",
        "external_url": "https://help.github.com/en/actions",
        "html_url": "https://github.com/apps/github-actions",
        "created_at": "2018-07-30T09:30:17Z",
        "updated_at": "2026-06-18T16:17:48Z",
        "permissions": {
          "actions": "write",
          "administration": "read",
          "artifact_metadata": "write",
          "attestations": "write",
          "checks": "write",
          "code_quality": "write",
          "contents": "write",
          "copilot_requests": "write",
          "deployments": "write",
          "discussions": "write",
          "drives": "write",
          "issues": "write",
          "merge_queues": "write",
          "metadata": "read",
          "models": "read",
          "packages": "write",
          "pages": "write",
          "pull_requests": "write",
          "repository_hooks": "write",
          "repository_projects": "write",
          "security_events": "write",
          "statuses": "write",
          "vulnerability_alerts": "read"
        },
        "events": [
          "branch_protection_rule",
          "check_run",
          "check_suite",
          "create",
          "delete",
          "deployment",
          "deployment_status",
          "discussion",
          "discussion_comment",
          "fork",
          "gollum",
          "issues",
          "issue_comment",
          "label",
          "merge_group",
          "milestone",
          "page_build",
          "public",
          "pull_request",
          "pull_request_review",
          "pull_request_review_comment",
          "push",
          "registry_package",
          "release",
          "repository",
          "repository_dispatch",
          "status",
          "watch",
          "workflow_dispatch",
          "workflow_run"
        ]
      },
      "pull_requests": [
        {
          "url": "https://api.github.com/repos/ducthangho/tra-luat/pulls/1249",
          "id": 5176379564,
          "number": 1249,
          "head": {
            "ref": "agent/wp1240-g1-claude",
            "sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          },
          "base": {
            "ref": "master",
            "sha": "3163f4d02a583787a9340c63a1f5eebd3780d970",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          }
        }
      ]
    },
    {
      "id": 127473377832,
      "name": "dot-bien-manh (5)",
      "node_id": "CR_kwDOTNeRjc8AAAAdrgFiKA",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "external_id": "d9865247-fdbe-529f-a1e3-9bb7b22d5f0f",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127473377832",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42092343146/job/127473377832",
      "details_url": "https://github.com/ducthangho/tra-luat/actions/runs/42092343146/job/127473377832",
      "status": "completed",
      "conclusion": "success",
      "started_at": "2026-11-05T19:16:48Z",
      "completed_at": "2026-11-05T19:46:16Z",
      "output": {
        "title": null,
        "summary": null,
        "text": null,
        "annotations_count": 2,
        "annotations_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127473377832/annotations"
      },
      "check_suite": {
        "id": 114059822218
      },
      "app": {
        "id": 15368,
        "client_id": "Iv1.05c79e9ad1f6bdfa",
        "slug": "github-actions",
        "node_id": "MDM6QXBwMTUzNjg=",
        "owner": {
          "login": "github",
          "id": 9919,
          "node_id": "MDEyOk9yZ2FuaXphdGlvbjk5MTk=",
          "avatar_url": "https://avatars.githubusercontent.com/u/9919?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/github",
          "html_url": "https://github.com/github",
          "followers_url": "https://api.github.com/users/github/followers",
          "following_url": "https://api.github.com/users/github/following{/other_user}",
          "gists_url": "https://api.github.com/users/github/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/github/subscriptions",
          "organizations_url": "https://api.github.com/users/github/orgs",
          "repos_url": "https://api.github.com/users/github/repos",
          "events_url": "https://api.github.com/users/github/events{/privacy}",
          "received_events_url": "https://api.github.com/users/github/received_events",
          "type": "Organization",
          "user_view_type": "public",
          "site_admin": false
        },
        "name": "GitHub Actions",
        "description": "Automate your workflow from idea to production",
        "external_url": "https://help.github.com/en/actions",
        "html_url": "https://github.com/apps/github-actions",
        "created_at": "2018-07-30T09:30:17Z",
        "updated_at": "2026-06-18T16:17:48Z",
        "permissions": {
          "actions": "write",
          "administration": "read",
          "artifact_metadata": "write",
          "attestations": "write",
          "checks": "write",
          "code_quality": "write",
          "contents": "write",
          "copilot_requests": "write",
          "deployments": "write",
          "discussions": "write",
          "drives": "write",
          "issues": "write",
          "merge_queues": "write",
          "metadata": "read",
          "models": "read",
          "packages": "write",
          "pages": "write",
          "pull_requests": "write",
          "repository_hooks": "write",
          "repository_projects": "write",
          "security_events": "write",
          "statuses": "write",
          "vulnerability_alerts": "read"
        },
        "events": [
          "branch_protection_rule",
          "check_run",
          "check_suite",
          "create",
          "delete",
          "deployment",
          "deployment_status",
          "discussion",
          "discussion_comment",
          "fork",
          "gollum",
          "issues",
          "issue_comment",
          "label",
          "merge_group",
          "milestone",
          "page_build",
          "public",
          "pull_request",
          "pull_request_review",
          "pull_request_review_comment",
          "push",
          "registry_package",
          "release",
          "repository",
          "repository_dispatch",
          "status",
          "watch",
          "workflow_dispatch",
          "workflow_run"
        ]
      },
      "pull_requests": [
        {
          "url": "https://api.github.com/repos/ducthangho/tra-luat/pulls/1249",
          "id": 5176379564,
          "number": 1249,
          "head": {
            "ref": "agent/wp1240-g1-claude",
            "sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          },
          "base": {
            "ref": "master",
            "sha": "3163f4d02a583787a9340c63a1f5eebd3780d970",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          }
        }
      ]
    },
    {
      "id": 127473377134,
      "name": "dot-bien-manh (2)",
      "node_id": "CR_kwDOTNeRjc8AAAAdrgFfbg",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "external_id": "c85c6a80-6ee3-5d5d-ad3f-8bdb6ffd1b21",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127473377134",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42092343146/job/127473377134",
      "details_url": "https://github.com/ducthangho/tra-luat/actions/runs/42092343146/job/127473377134",
      "status": "completed",
      "conclusion": "success",
      "started_at": "2026-11-05T19:16:48Z",
      "completed_at": "2026-11-05T19:44:04Z",
      "output": {
        "title": null,
        "summary": null,
        "text": null,
        "annotations_count": 2,
        "annotations_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127473377134/annotations"
      },
      "check_suite": {
        "id": 114059822218
      },
      "app": {
        "id": 15368,
        "client_id": "Iv1.05c79e9ad1f6bdfa",
        "slug": "github-actions",
        "node_id": "MDM6QXBwMTUzNjg=",
        "owner": {
          "login": "github",
          "id": 9919,
          "node_id": "MDEyOk9yZ2FuaXphdGlvbjk5MTk=",
          "avatar_url": "https://avatars.githubusercontent.com/u/9919?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/github",
          "html_url": "https://github.com/github",
          "followers_url": "https://api.github.com/users/github/followers",
          "following_url": "https://api.github.com/users/github/following{/other_user}",
          "gists_url": "https://api.github.com/users/github/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/github/subscriptions",
          "organizations_url": "https://api.github.com/users/github/orgs",
          "repos_url": "https://api.github.com/users/github/repos",
          "events_url": "https://api.github.com/users/github/events{/privacy}",
          "received_events_url": "https://api.github.com/users/github/received_events",
          "type": "Organization",
          "user_view_type": "public",
          "site_admin": false
        },
        "name": "GitHub Actions",
        "description": "Automate your workflow from idea to production",
        "external_url": "https://help.github.com/en/actions",
        "html_url": "https://github.com/apps/github-actions",
        "created_at": "2018-07-30T09:30:17Z",
        "updated_at": "2026-06-18T16:17:48Z",
        "permissions": {
          "actions": "write",
          "administration": "read",
          "artifact_metadata": "write",
          "attestations": "write",
          "checks": "write",
          "code_quality": "write",
          "contents": "write",
          "copilot_requests": "write",
          "deployments": "write",
          "discussions": "write",
          "drives": "write",
          "issues": "write",
          "merge_queues": "write",
          "metadata": "read",
          "models": "read",
          "packages": "write",
          "pages": "write",
          "pull_requests": "write",
          "repository_hooks": "write",
          "repository_projects": "write",
          "security_events": "write",
          "statuses": "write",
          "vulnerability_alerts": "read"
        },
        "events": [
          "branch_protection_rule",
          "check_run",
          "check_suite",
          "create",
          "delete",
          "deployment",
          "deployment_status",
          "discussion",
          "discussion_comment",
          "fork",
          "gollum",
          "issues",
          "issue_comment",
          "label",
          "merge_group",
          "milestone",
          "page_build",
          "public",
          "pull_request",
          "pull_request_review",
          "pull_request_review_comment",
          "push",
          "registry_package",
          "release",
          "repository",
          "repository_dispatch",
          "status",
          "watch",
          "workflow_dispatch",
          "workflow_run"
        ]
      },
      "pull_requests": [
        {
          "url": "https://api.github.com/repos/ducthangho/tra-luat/pulls/1249",
          "id": 5176379564,
          "number": 1249,
          "head": {
            "ref": "agent/wp1240-g1-claude",
            "sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          },
          "base": {
            "ref": "master",
            "sha": "3163f4d02a583787a9340c63a1f5eebd3780d970",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          }
        }
      ]
    },
    {
      "id": 127473376921,
      "name": "dot-bien-manh (7)",
      "node_id": "CR_kwDOTNeRjc8AAAAdrgFemQ",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "external_id": "d5771645-e452-56b5-927d-263b73cf2c3b",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127473376921",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42092343146/job/127473376921",
      "details_url": "https://github.com/ducthangho/tra-luat/actions/runs/42092343146/job/127473376921",
      "status": "completed",
      "conclusion": "success",
      "started_at": "2026-11-05T19:16:48Z",
      "completed_at": "2026-11-05T19:45:12Z",
      "output": {
        "title": null,
        "summary": null,
        "text": null,
        "annotations_count": 2,
        "annotations_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127473376921/annotations"
      },
      "check_suite": {
        "id": 114059822218
      },
      "app": {
        "id": 15368,
        "client_id": "Iv1.05c79e9ad1f6bdfa",
        "slug": "github-actions",
        "node_id": "MDM6QXBwMTUzNjg=",
        "owner": {
          "login": "github",
          "id": 9919,
          "node_id": "MDEyOk9yZ2FuaXphdGlvbjk5MTk=",
          "avatar_url": "https://avatars.githubusercontent.com/u/9919?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/github",
          "html_url": "https://github.com/github",
          "followers_url": "https://api.github.com/users/github/followers",
          "following_url": "https://api.github.com/users/github/following{/other_user}",
          "gists_url": "https://api.github.com/users/github/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/github/subscriptions",
          "organizations_url": "https://api.github.com/users/github/orgs",
          "repos_url": "https://api.github.com/users/github/repos",
          "events_url": "https://api.github.com/users/github/events{/privacy}",
          "received_events_url": "https://api.github.com/users/github/received_events",
          "type": "Organization",
          "user_view_type": "public",
          "site_admin": false
        },
        "name": "GitHub Actions",
        "description": "Automate your workflow from idea to production",
        "external_url": "https://help.github.com/en/actions",
        "html_url": "https://github.com/apps/github-actions",
        "created_at": "2018-07-30T09:30:17Z",
        "updated_at": "2026-06-18T16:17:48Z",
        "permissions": {
          "actions": "write",
          "administration": "read",
          "artifact_metadata": "write",
          "attestations": "write",
          "checks": "write",
          "code_quality": "write",
          "contents": "write",
          "copilot_requests": "write",
          "deployments": "write",
          "discussions": "write",
          "drives": "write",
          "issues": "write",
          "merge_queues": "write",
          "metadata": "read",
          "models": "read",
          "packages": "write",
          "pages": "write",
          "pull_requests": "write",
          "repository_hooks": "write",
          "repository_projects": "write",
          "security_events": "write",
          "statuses": "write",
          "vulnerability_alerts": "read"
        },
        "events": [
          "branch_protection_rule",
          "check_run",
          "check_suite",
          "create",
          "delete",
          "deployment",
          "deployment_status",
          "discussion",
          "discussion_comment",
          "fork",
          "gollum",
          "issues",
          "issue_comment",
          "label",
          "merge_group",
          "milestone",
          "page_build",
          "public",
          "pull_request",
          "pull_request_review",
          "pull_request_review_comment",
          "push",
          "registry_package",
          "release",
          "repository",
          "repository_dispatch",
          "status",
          "watch",
          "workflow_dispatch",
          "workflow_run"
        ]
      },
      "pull_requests": [
        {
          "url": "https://api.github.com/repos/ducthangho/tra-luat/pulls/1249",
          "id": 5176379564,
          "number": 1249,
          "head": {
            "ref": "agent/wp1240-g1-claude",
            "sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          },
          "base": {
            "ref": "master",
            "sha": "3163f4d02a583787a9340c63a1f5eebd3780d970",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          }
        }
      ]
    },
    {
      "id": 127473376875,
      "name": "dot-bien-manh (1)",
      "node_id": "CR_kwDOTNeRjc8AAAAdrgFeaw",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "external_id": "3c77fad5-7635-5df8-b41b-541d0a7c43d7",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127473376875",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42092343146/job/127473376875",
      "details_url": "https://github.com/ducthangho/tra-luat/actions/runs/42092343146/job/127473376875",
      "status": "completed",
      "conclusion": "success",
      "started_at": "2026-11-05T19:16:48Z",
      "completed_at": "2026-11-05T19:42:12Z",
      "output": {
        "title": null,
        "summary": null,
        "text": null,
        "annotations_count": 2,
        "annotations_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127473376875/annotations"
      },
      "check_suite": {
        "id": 114059822218
      },
      "app": {
        "id": 15368,
        "client_id": "Iv1.05c79e9ad1f6bdfa",
        "slug": "github-actions",
        "node_id": "MDM6QXBwMTUzNjg=",
        "owner": {
          "login": "github",
          "id": 9919,
          "node_id": "MDEyOk9yZ2FuaXphdGlvbjk5MTk=",
          "avatar_url": "https://avatars.githubusercontent.com/u/9919?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/github",
          "html_url": "https://github.com/github",
          "followers_url": "https://api.github.com/users/github/followers",
          "following_url": "https://api.github.com/users/github/following{/other_user}",
          "gists_url": "https://api.github.com/users/github/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/github/subscriptions",
          "organizations_url": "https://api.github.com/users/github/orgs",
          "repos_url": "https://api.github.com/users/github/repos",
          "events_url": "https://api.github.com/users/github/events{/privacy}",
          "received_events_url": "https://api.github.com/users/github/received_events",
          "type": "Organization",
          "user_view_type": "public",
          "site_admin": false
        },
        "name": "GitHub Actions",
        "description": "Automate your workflow from idea to production",
        "external_url": "https://help.github.com/en/actions",
        "html_url": "https://github.com/apps/github-actions",
        "created_at": "2018-07-30T09:30:17Z",
        "updated_at": "2026-06-18T16:17:48Z",
        "permissions": {
          "actions": "write",
          "administration": "read",
          "artifact_metadata": "write",
          "attestations": "write",
          "checks": "write",
          "code_quality": "write",
          "contents": "write",
          "copilot_requests": "write",
          "deployments": "write",
          "discussions": "write",
          "drives": "write",
          "issues": "write",
          "merge_queues": "write",
          "metadata": "read",
          "models": "read",
          "packages": "write",
          "pages": "write",
          "pull_requests": "write",
          "repository_hooks": "write",
          "repository_projects": "write",
          "security_events": "write",
          "statuses": "write",
          "vulnerability_alerts": "read"
        },
        "events": [
          "branch_protection_rule",
          "check_run",
          "check_suite",
          "create",
          "delete",
          "deployment",
          "deployment_status",
          "discussion",
          "discussion_comment",
          "fork",
          "gollum",
          "issues",
          "issue_comment",
          "label",
          "merge_group",
          "milestone",
          "page_build",
          "public",
          "pull_request",
          "pull_request_review",
          "pull_request_review_comment",
          "push",
          "registry_package",
          "release",
          "repository",
          "repository_dispatch",
          "status",
          "watch",
          "workflow_dispatch",
          "workflow_run"
        ]
      },
      "pull_requests": [
        {
          "url": "https://api.github.com/repos/ducthangho/tra-luat/pulls/1249",
          "id": 5176379564,
          "number": 1249,
          "head": {
            "ref": "agent/wp1240-g1-claude",
            "sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          },
          "base": {
            "ref": "master",
            "sha": "3163f4d02a583787a9340c63a1f5eebd3780d970",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          }
        }
      ]
    },
    {
      "id": 127473376653,
      "name": "dot-bien-manh (0)",
      "node_id": "CR_kwDOTNeRjc8AAAAdrgFdjQ",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "external_id": "be4393dc-cd33-561b-bca0-41a690fbbde6",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127473376653",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42092343146/job/127473376653",
      "details_url": "https://github.com/ducthangho/tra-luat/actions/runs/42092343146/job/127473376653",
      "status": "completed",
      "conclusion": "success",
      "started_at": "2026-11-05T19:16:48Z",
      "completed_at": "2026-11-05T19:43:50Z",
      "output": {
        "title": null,
        "summary": null,
        "text": null,
        "annotations_count": 2,
        "annotations_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127473376653/annotations"
      },
      "check_suite": {
        "id": 114059822218
      },
      "app": {
        "id": 15368,
        "client_id": "Iv1.05c79e9ad1f6bdfa",
        "slug": "github-actions",
        "node_id": "MDM6QXBwMTUzNjg=",
        "owner": {
          "login": "github",
          "id": 9919,
          "node_id": "MDEyOk9yZ2FuaXphdGlvbjk5MTk=",
          "avatar_url": "https://avatars.githubusercontent.com/u/9919?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/github",
          "html_url": "https://github.com/github",
          "followers_url": "https://api.github.com/users/github/followers",
          "following_url": "https://api.github.com/users/github/following{/other_user}",
          "gists_url": "https://api.github.com/users/github/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/github/subscriptions",
          "organizations_url": "https://api.github.com/users/github/orgs",
          "repos_url": "https://api.github.com/users/github/repos",
          "events_url": "https://api.github.com/users/github/events{/privacy}",
          "received_events_url": "https://api.github.com/users/github/received_events",
          "type": "Organization",
          "user_view_type": "public",
          "site_admin": false
        },
        "name": "GitHub Actions",
        "description": "Automate your workflow from idea to production",
        "external_url": "https://help.github.com/en/actions",
        "html_url": "https://github.com/apps/github-actions",
        "created_at": "2018-07-30T09:30:17Z",
        "updated_at": "2026-06-18T16:17:48Z",
        "permissions": {
          "actions": "write",
          "administration": "read",
          "artifact_metadata": "write",
          "attestations": "write",
          "checks": "write",
          "code_quality": "write",
          "contents": "write",
          "copilot_requests": "write",
          "deployments": "write",
          "discussions": "write",
          "drives": "write",
          "issues": "write",
          "merge_queues": "write",
          "metadata": "read",
          "models": "read",
          "packages": "write",
          "pages": "write",
          "pull_requests": "write",
          "repository_hooks": "write",
          "repository_projects": "write",
          "security_events": "write",
          "statuses": "write",
          "vulnerability_alerts": "read"
        },
        "events": [
          "branch_protection_rule",
          "check_run",
          "check_suite",
          "create",
          "delete",
          "deployment",
          "deployment_status",
          "discussion",
          "discussion_comment",
          "fork",
          "gollum",
          "issues",
          "issue_comment",
          "label",
          "merge_group",
          "milestone",
          "page_build",
          "public",
          "pull_request",
          "pull_request_review",
          "pull_request_review_comment",
          "push",
          "registry_package",
          "release",
          "repository",
          "repository_dispatch",
          "status",
          "watch",
          "workflow_dispatch",
          "workflow_run"
        ]
      },
      "pull_requests": [
        {
          "url": "https://api.github.com/repos/ducthangho/tra-luat/pulls/1249",
          "id": 5176379564,
          "number": 1249,
          "head": {
            "ref": "agent/wp1240-g1-claude",
            "sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          },
          "base": {
            "ref": "master",
            "sha": "3163f4d02a583787a9340c63a1f5eebd3780d970",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          }
        }
      ]
    },
    {
      "id": 127473376504,
      "name": "dot-bien-manh (3)",
      "node_id": "CR_kwDOTNeRjc8AAAAdrgFc-A",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "external_id": "579a9178-250b-5682-8682-9554d0518d86",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127473376504",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42092343146/job/127473376504",
      "details_url": "https://github.com/ducthangho/tra-luat/actions/runs/42092343146/job/127473376504",
      "status": "completed",
      "conclusion": "success",
      "started_at": "2026-11-05T19:16:48Z",
      "completed_at": "2026-11-05T19:45:29Z",
      "output": {
        "title": null,
        "summary": null,
        "text": null,
        "annotations_count": 2,
        "annotations_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127473376504/annotations"
      },
      "check_suite": {
        "id": 114059822218
      },
      "app": {
        "id": 15368,
        "client_id": "Iv1.05c79e9ad1f6bdfa",
        "slug": "github-actions",
        "node_id": "MDM6QXBwMTUzNjg=",
        "owner": {
          "login": "github",
          "id": 9919,
          "node_id": "MDEyOk9yZ2FuaXphdGlvbjk5MTk=",
          "avatar_url": "https://avatars.githubusercontent.com/u/9919?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/github",
          "html_url": "https://github.com/github",
          "followers_url": "https://api.github.com/users/github/followers",
          "following_url": "https://api.github.com/users/github/following{/other_user}",
          "gists_url": "https://api.github.com/users/github/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/github/subscriptions",
          "organizations_url": "https://api.github.com/users/github/orgs",
          "repos_url": "https://api.github.com/users/github/repos",
          "events_url": "https://api.github.com/users/github/events{/privacy}",
          "received_events_url": "https://api.github.com/users/github/received_events",
          "type": "Organization",
          "user_view_type": "public",
          "site_admin": false
        },
        "name": "GitHub Actions",
        "description": "Automate your workflow from idea to production",
        "external_url": "https://help.github.com/en/actions",
        "html_url": "https://github.com/apps/github-actions",
        "created_at": "2018-07-30T09:30:17Z",
        "updated_at": "2026-06-18T16:17:48Z",
        "permissions": {
          "actions": "write",
          "administration": "read",
          "artifact_metadata": "write",
          "attestations": "write",
          "checks": "write",
          "code_quality": "write",
          "contents": "write",
          "copilot_requests": "write",
          "deployments": "write",
          "discussions": "write",
          "drives": "write",
          "issues": "write",
          "merge_queues": "write",
          "metadata": "read",
          "models": "read",
          "packages": "write",
          "pages": "write",
          "pull_requests": "write",
          "repository_hooks": "write",
          "repository_projects": "write",
          "security_events": "write",
          "statuses": "write",
          "vulnerability_alerts": "read"
        },
        "events": [
          "branch_protection_rule",
          "check_run",
          "check_suite",
          "create",
          "delete",
          "deployment",
          "deployment_status",
          "discussion",
          "discussion_comment",
          "fork",
          "gollum",
          "issues",
          "issue_comment",
          "label",
          "merge_group",
          "milestone",
          "page_build",
          "public",
          "pull_request",
          "pull_request_review",
          "pull_request_review_comment",
          "push",
          "registry_package",
          "release",
          "repository",
          "repository_dispatch",
          "status",
          "watch",
          "workflow_dispatch",
          "workflow_run"
        ]
      },
      "pull_requests": [
        {
          "url": "https://api.github.com/repos/ducthangho/tra-luat/pulls/1249",
          "id": 5176379564,
          "number": 1249,
          "head": {
            "ref": "agent/wp1240-g1-claude",
            "sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          },
          "base": {
            "ref": "master",
            "sha": "3163f4d02a583787a9340c63a1f5eebd3780d970",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          }
        }
      ]
    },
    {
      "id": 127473376385,
      "name": "dot-bien-manh (4)",
      "node_id": "CR_kwDOTNeRjc8AAAAdrgFcgQ",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "external_id": "9ca94682-e794-5cfa-a956-e662e97a71d4",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127473376385",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42092343146/job/127473376385",
      "details_url": "https://github.com/ducthangho/tra-luat/actions/runs/42092343146/job/127473376385",
      "status": "completed",
      "conclusion": "success",
      "started_at": "2026-11-05T19:16:48Z",
      "completed_at": "2026-11-05T19:44:10Z",
      "output": {
        "title": null,
        "summary": null,
        "text": null,
        "annotations_count": 2,
        "annotations_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127473376385/annotations"
      },
      "check_suite": {
        "id": 114059822218
      },
      "app": {
        "id": 15368,
        "client_id": "Iv1.05c79e9ad1f6bdfa",
        "slug": "github-actions",
        "node_id": "MDM6QXBwMTUzNjg=",
        "owner": {
          "login": "github",
          "id": 9919,
          "node_id": "MDEyOk9yZ2FuaXphdGlvbjk5MTk=",
          "avatar_url": "https://avatars.githubusercontent.com/u/9919?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/github",
          "html_url": "https://github.com/github",
          "followers_url": "https://api.github.com/users/github/followers",
          "following_url": "https://api.github.com/users/github/following{/other_user}",
          "gists_url": "https://api.github.com/users/github/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/github/subscriptions",
          "organizations_url": "https://api.github.com/users/github/orgs",
          "repos_url": "https://api.github.com/users/github/repos",
          "events_url": "https://api.github.com/users/github/events{/privacy}",
          "received_events_url": "https://api.github.com/users/github/received_events",
          "type": "Organization",
          "user_view_type": "public",
          "site_admin": false
        },
        "name": "GitHub Actions",
        "description": "Automate your workflow from idea to production",
        "external_url": "https://help.github.com/en/actions",
        "html_url": "https://github.com/apps/github-actions",
        "created_at": "2018-07-30T09:30:17Z",
        "updated_at": "2026-06-18T16:17:48Z",
        "permissions": {
          "actions": "write",
          "administration": "read",
          "artifact_metadata": "write",
          "attestations": "write",
          "checks": "write",
          "code_quality": "write",
          "contents": "write",
          "copilot_requests": "write",
          "deployments": "write",
          "discussions": "write",
          "drives": "write",
          "issues": "write",
          "merge_queues": "write",
          "metadata": "read",
          "models": "read",
          "packages": "write",
          "pages": "write",
          "pull_requests": "write",
          "repository_hooks": "write",
          "repository_projects": "write",
          "security_events": "write",
          "statuses": "write",
          "vulnerability_alerts": "read"
        },
        "events": [
          "branch_protection_rule",
          "check_run",
          "check_suite",
          "create",
          "delete",
          "deployment",
          "deployment_status",
          "discussion",
          "discussion_comment",
          "fork",
          "gollum",
          "issues",
          "issue_comment",
          "label",
          "merge_group",
          "milestone",
          "page_build",
          "public",
          "pull_request",
          "pull_request_review",
          "pull_request_review_comment",
          "push",
          "registry_package",
          "release",
          "repository",
          "repository_dispatch",
          "status",
          "watch",
          "workflow_dispatch",
          "workflow_run"
        ]
      },
      "pull_requests": [
        {
          "url": "https://api.github.com/repos/ducthangho/tra-luat/pulls/1249",
          "id": 5176379564,
          "number": 1249,
          "head": {
            "ref": "agent/wp1240-g1-claude",
            "sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          },
          "base": {
            "ref": "master",
            "sha": "3163f4d02a583787a9340c63a1f5eebd3780d970",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          }
        }
      ]
    },
    {
      "id": 127473376345,
      "name": "dot-bien-manh (6)",
      "node_id": "CR_kwDOTNeRjc8AAAAdrgFcWQ",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "external_id": "71aae1e8-9622-5d43-b93c-35fa6fe41ea9",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127473376345",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42092343146/job/127473376345",
      "details_url": "https://github.com/ducthangho/tra-luat/actions/runs/42092343146/job/127473376345",
      "status": "completed",
      "conclusion": "success",
      "started_at": "2026-11-05T19:16:48Z",
      "completed_at": "2026-11-05T19:44:16Z",
      "output": {
        "title": null,
        "summary": null,
        "text": null,
        "annotations_count": 2,
        "annotations_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127473376345/annotations"
      },
      "check_suite": {
        "id": 114059822218
      },
      "app": {
        "id": 15368,
        "client_id": "Iv1.05c79e9ad1f6bdfa",
        "slug": "github-actions",
        "node_id": "MDM6QXBwMTUzNjg=",
        "owner": {
          "login": "github",
          "id": 9919,
          "node_id": "MDEyOk9yZ2FuaXphdGlvbjk5MTk=",
          "avatar_url": "https://avatars.githubusercontent.com/u/9919?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/github",
          "html_url": "https://github.com/github",
          "followers_url": "https://api.github.com/users/github/followers",
          "following_url": "https://api.github.com/users/github/following{/other_user}",
          "gists_url": "https://api.github.com/users/github/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/github/subscriptions",
          "organizations_url": "https://api.github.com/users/github/orgs",
          "repos_url": "https://api.github.com/users/github/repos",
          "events_url": "https://api.github.com/users/github/events{/privacy}",
          "received_events_url": "https://api.github.com/users/github/received_events",
          "type": "Organization",
          "user_view_type": "public",
          "site_admin": false
        },
        "name": "GitHub Actions",
        "description": "Automate your workflow from idea to production",
        "external_url": "https://help.github.com/en/actions",
        "html_url": "https://github.com/apps/github-actions",
        "created_at": "2018-07-30T09:30:17Z",
        "updated_at": "2026-06-18T16:17:48Z",
        "permissions": {
          "actions": "write",
          "administration": "read",
          "artifact_metadata": "write",
          "attestations": "write",
          "checks": "write",
          "code_quality": "write",
          "contents": "write",
          "copilot_requests": "write",
          "deployments": "write",
          "discussions": "write",
          "drives": "write",
          "issues": "write",
          "merge_queues": "write",
          "metadata": "read",
          "models": "read",
          "packages": "write",
          "pages": "write",
          "pull_requests": "write",
          "repository_hooks": "write",
          "repository_projects": "write",
          "security_events": "write",
          "statuses": "write",
          "vulnerability_alerts": "read"
        },
        "events": [
          "branch_protection_rule",
          "check_run",
          "check_suite",
          "create",
          "delete",
          "deployment",
          "deployment_status",
          "discussion",
          "discussion_comment",
          "fork",
          "gollum",
          "issues",
          "issue_comment",
          "label",
          "merge_group",
          "milestone",
          "page_build",
          "public",
          "pull_request",
          "pull_request_review",
          "pull_request_review_comment",
          "push",
          "registry_package",
          "release",
          "repository",
          "repository_dispatch",
          "status",
          "watch",
          "workflow_dispatch",
          "workflow_run"
        ]
      },
      "pull_requests": [
        {
          "url": "https://api.github.com/repos/ducthangho/tra-luat/pulls/1249",
          "id": 5176379564,
          "number": 1249,
          "head": {
            "ref": "agent/wp1240-g1-claude",
            "sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          },
          "base": {
            "ref": "master",
            "sha": "3163f4d02a583787a9340c63a1f5eebd3780d970",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          }
        }
      ]
    },
    {
      "id": 127473376216,
      "name": "dot-bien-du",
      "node_id": "CR_kwDOTNeRjc8AAAAdrgFb2A",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "external_id": "6e1b1fe3-6787-563d-9b0c-5e7702abd6b6",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127473376216",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42092343146/job/127473376216",
      "details_url": "https://github.com/ducthangho/tra-luat/actions/runs/42092343146/job/127473376216",
      "status": "completed",
      "conclusion": "success",
      "started_at": "2026-11-05T19:16:48Z",
      "completed_at": "2026-11-05T19:36:48Z",
      "output": {
        "title": null,
        "summary": null,
        "text": null,
        "annotations_count": 2,
        "annotations_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127473376216/annotations"
      },
      "check_suite": {
        "id": 114059822218
      },
      "app": {
        "id": 15368,
        "client_id": "Iv1.05c79e9ad1f6bdfa",
        "slug": "github-actions",
        "node_id": "MDM6QXBwMTUzNjg=",
        "owner": {
          "login": "github",
          "id": 9919,
          "node_id": "MDEyOk9yZ2FuaXphdGlvbjk5MTk=",
          "avatar_url": "https://avatars.githubusercontent.com/u/9919?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/github",
          "html_url": "https://github.com/github",
          "followers_url": "https://api.github.com/users/github/followers",
          "following_url": "https://api.github.com/users/github/following{/other_user}",
          "gists_url": "https://api.github.com/users/github/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/github/subscriptions",
          "organizations_url": "https://api.github.com/users/github/orgs",
          "repos_url": "https://api.github.com/users/github/repos",
          "events_url": "https://api.github.com/users/github/events{/privacy}",
          "received_events_url": "https://api.github.com/users/github/received_events",
          "type": "Organization",
          "user_view_type": "public",
          "site_admin": false
        },
        "name": "GitHub Actions",
        "description": "Automate your workflow from idea to production",
        "external_url": "https://help.github.com/en/actions",
        "html_url": "https://github.com/apps/github-actions",
        "created_at": "2018-07-30T09:30:17Z",
        "updated_at": "2026-06-18T16:17:48Z",
        "permissions": {
          "actions": "write",
          "administration": "read",
          "artifact_metadata": "write",
          "attestations": "write",
          "checks": "write",
          "code_quality": "write",
          "contents": "write",
          "copilot_requests": "write",
          "deployments": "write",
          "discussions": "write",
          "drives": "write",
          "issues": "write",
          "merge_queues": "write",
          "metadata": "read",
          "models": "read",
          "packages": "write",
          "pages": "write",
          "pull_requests": "write",
          "repository_hooks": "write",
          "repository_projects": "write",
          "security_events": "write",
          "statuses": "write",
          "vulnerability_alerts": "read"
        },
        "events": [
          "branch_protection_rule",
          "check_run",
          "check_suite",
          "create",
          "delete",
          "deployment",
          "deployment_status",
          "discussion",
          "discussion_comment",
          "fork",
          "gollum",
          "issues",
          "issue_comment",
          "label",
          "merge_group",
          "milestone",
          "page_build",
          "public",
          "pull_request",
          "pull_request_review",
          "pull_request_review_comment",
          "push",
          "registry_package",
          "release",
          "repository",
          "repository_dispatch",
          "status",
          "watch",
          "workflow_dispatch",
          "workflow_run"
        ]
      },
      "pull_requests": [
        {
          "url": "https://api.github.com/repos/ducthangho/tra-luat/pulls/1249",
          "id": 5176379564,
          "number": 1249,
          "head": {
            "ref": "agent/wp1240-g1-claude",
            "sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          },
          "base": {
            "ref": "master",
            "sha": "3163f4d02a583787a9340c63a1f5eebd3780d970",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          }
        }
      ]
    },
    {
      "id": 127448292389,
      "name": "gate-cong-cu-gop (ubuntu-latest)",
      "node_id": "CR_kwDOTNeRjc8AAAAdrIKcJQ",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "external_id": "15365ac0-ebc8-5edb-baaf-84e135f85229",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127448292389",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127448292389",
      "details_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127448292389",
      "status": "completed",
      "conclusion": "success",
      "started_at": "2026-11-05T18:32:25Z",
      "completed_at": "2026-11-05T18:32:40Z",
      "output": {
        "title": null,
        "summary": null,
        "text": null,
        "annotations_count": 2,
        "annotations_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127448292389/annotations"
      },
      "check_suite": {
        "id": 114030831118
      },
      "app": {
        "id": 15368,
        "client_id": "Iv1.05c79e9ad1f6bdfa",
        "slug": "github-actions",
        "node_id": "MDM6QXBwMTUzNjg=",
        "owner": {
          "login": "github",
          "id": 9919,
          "node_id": "MDEyOk9yZ2FuaXphdGlvbjk5MTk=",
          "avatar_url": "https://avatars.githubusercontent.com/u/9919?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/github",
          "html_url": "https://github.com/github",
          "followers_url": "https://api.github.com/users/github/followers",
          "following_url": "https://api.github.com/users/github/following{/other_user}",
          "gists_url": "https://api.github.com/users/github/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/github/subscriptions",
          "organizations_url": "https://api.github.com/users/github/orgs",
          "repos_url": "https://api.github.com/users/github/repos",
          "events_url": "https://api.github.com/users/github/events{/privacy}",
          "received_events_url": "https://api.github.com/users/github/received_events",
          "type": "Organization",
          "user_view_type": "public",
          "site_admin": false
        },
        "name": "GitHub Actions",
        "description": "Automate your workflow from idea to production",
        "external_url": "https://help.github.com/en/actions",
        "html_url": "https://github.com/apps/github-actions",
        "created_at": "2018-07-30T09:30:17Z",
        "updated_at": "2026-06-18T16:17:48Z",
        "permissions": {
          "actions": "write",
          "administration": "read",
          "artifact_metadata": "write",
          "attestations": "write",
          "checks": "write",
          "code_quality": "write",
          "contents": "write",
          "copilot_requests": "write",
          "deployments": "write",
          "discussions": "write",
          "drives": "write",
          "issues": "write",
          "merge_queues": "write",
          "metadata": "read",
          "models": "read",
          "packages": "write",
          "pages": "write",
          "pull_requests": "write",
          "repository_hooks": "write",
          "repository_projects": "write",
          "security_events": "write",
          "statuses": "write",
          "vulnerability_alerts": "read"
        },
        "events": [
          "branch_protection_rule",
          "check_run",
          "check_suite",
          "create",
          "delete",
          "deployment",
          "deployment_status",
          "discussion",
          "discussion_comment",
          "fork",
          "gollum",
          "issues",
          "issue_comment",
          "label",
          "merge_group",
          "milestone",
          "page_build",
          "public",
          "pull_request",
          "pull_request_review",
          "pull_request_review_comment",
          "push",
          "registry_package",
          "release",
          "repository",
          "repository_dispatch",
          "status",
          "watch",
          "workflow_dispatch",
          "workflow_run"
        ]
      },
      "pull_requests": [
        {
          "url": "https://api.github.com/repos/ducthangho/tra-luat/pulls/1249",
          "id": 5176379564,
          "number": 1249,
          "head": {
            "ref": "agent/wp1240-g1-claude",
            "sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          },
          "base": {
            "ref": "master",
            "sha": "3163f4d02a583787a9340c63a1f5eebd3780d970",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          }
        }
      ]
    },
    {
      "id": 127437301409,
      "name": "gate-registry (ubuntu-latest)",
      "node_id": "CR_kwDOTNeRjc8AAAAdq9rmoQ",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "external_id": "2766a543-c49d-5d39-a06f-5eb77d56df05",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127437301409",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127437301409",
      "details_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127437301409",
      "status": "completed",
      "conclusion": "success",
      "started_at": "2026-11-05T18:12:46Z",
      "completed_at": "2026-11-05T18:29:14Z",
      "output": {
        "title": null,
        "summary": null,
        "text": null,
        "annotations_count": 2,
        "annotations_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127437301409/annotations"
      },
      "check_suite": {
        "id": 114030831118
      },
      "app": {
        "id": 15368,
        "client_id": "Iv1.05c79e9ad1f6bdfa",
        "slug": "github-actions",
        "node_id": "MDM6QXBwMTUzNjg=",
        "owner": {
          "login": "github",
          "id": 9919,
          "node_id": "MDEyOk9yZ2FuaXphdGlvbjk5MTk=",
          "avatar_url": "https://avatars.githubusercontent.com/u/9919?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/github",
          "html_url": "https://github.com/github",
          "followers_url": "https://api.github.com/users/github/followers",
          "following_url": "https://api.github.com/users/github/following{/other_user}",
          "gists_url": "https://api.github.com/users/github/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/github/subscriptions",
          "organizations_url": "https://api.github.com/users/github/orgs",
          "repos_url": "https://api.github.com/users/github/repos",
          "events_url": "https://api.github.com/users/github/events{/privacy}",
          "received_events_url": "https://api.github.com/users/github/received_events",
          "type": "Organization",
          "user_view_type": "public",
          "site_admin": false
        },
        "name": "GitHub Actions",
        "description": "Automate your workflow from idea to production",
        "external_url": "https://help.github.com/en/actions",
        "html_url": "https://github.com/apps/github-actions",
        "created_at": "2018-07-30T09:30:17Z",
        "updated_at": "2026-06-18T16:17:48Z",
        "permissions": {
          "actions": "write",
          "administration": "read",
          "artifact_metadata": "write",
          "attestations": "write",
          "checks": "write",
          "code_quality": "write",
          "contents": "write",
          "copilot_requests": "write",
          "deployments": "write",
          "discussions": "write",
          "drives": "write",
          "issues": "write",
          "merge_queues": "write",
          "metadata": "read",
          "models": "read",
          "packages": "write",
          "pages": "write",
          "pull_requests": "write",
          "repository_hooks": "write",
          "repository_projects": "write",
          "security_events": "write",
          "statuses": "write",
          "vulnerability_alerts": "read"
        },
        "events": [
          "branch_protection_rule",
          "check_run",
          "check_suite",
          "create",
          "delete",
          "deployment",
          "deployment_status",
          "discussion",
          "discussion_comment",
          "fork",
          "gollum",
          "issues",
          "issue_comment",
          "label",
          "merge_group",
          "milestone",
          "page_build",
          "public",
          "pull_request",
          "pull_request_review",
          "pull_request_review_comment",
          "push",
          "registry_package",
          "release",
          "repository",
          "repository_dispatch",
          "status",
          "watch",
          "workflow_dispatch",
          "workflow_run"
        ]
      },
      "pull_requests": [
        {
          "url": "https://api.github.com/repos/ducthangho/tra-luat/pulls/1249",
          "id": 5176379564,
          "number": 1249,
          "head": {
            "ref": "agent/wp1240-g1-claude",
            "sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          },
          "base": {
            "ref": "master",
            "sha": "3163f4d02a583787a9340c63a1f5eebd3780d970",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          }
        }
      ]
    },
    {
      "id": 127437121173,
      "name": "gate-nhanh-gop (ubuntu-latest)",
      "node_id": "CR_kwDOTNeRjc8AAAAdq9gmlQ",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "external_id": "e3c2a632-4b5e-5a5e-b725-859e8cdf81ca",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127437121173",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127437121173",
      "details_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127437121173",
      "status": "completed",
      "conclusion": "success",
      "started_at": "2026-11-05T18:12:27Z",
      "completed_at": "2026-11-05T18:12:43Z",
      "output": {
        "title": null,
        "summary": null,
        "text": null,
        "annotations_count": 2,
        "annotations_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127437121173/annotations"
      },
      "check_suite": {
        "id": 114030831118
      },
      "app": {
        "id": 15368,
        "client_id": "Iv1.05c79e9ad1f6bdfa",
        "slug": "github-actions",
        "node_id": "MDM6QXBwMTUzNjg=",
        "owner": {
          "login": "github",
          "id": 9919,
          "node_id": "MDEyOk9yZ2FuaXphdGlvbjk5MTk=",
          "avatar_url": "https://avatars.githubusercontent.com/u/9919?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/github",
          "html_url": "https://github.com/github",
          "followers_url": "https://api.github.com/users/github/followers",
          "following_url": "https://api.github.com/users/github/following{/other_user}",
          "gists_url": "https://api.github.com/users/github/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/github/subscriptions",
          "organizations_url": "https://api.github.com/users/github/orgs",
          "repos_url": "https://api.github.com/users/github/repos",
          "events_url": "https://api.github.com/users/github/events{/privacy}",
          "received_events_url": "https://api.github.com/users/github/received_events",
          "type": "Organization",
          "user_view_type": "public",
          "site_admin": false
        },
        "name": "GitHub Actions",
        "description": "Automate your workflow from idea to production",
        "external_url": "https://help.github.com/en/actions",
        "html_url": "https://github.com/apps/github-actions",
        "created_at": "2018-07-30T09:30:17Z",
        "updated_at": "2026-06-18T16:17:48Z",
        "permissions": {
          "actions": "write",
          "administration": "read",
          "artifact_metadata": "write",
          "attestations": "write",
          "checks": "write",
          "code_quality": "write",
          "contents": "write",
          "copilot_requests": "write",
          "deployments": "write",
          "discussions": "write",
          "drives": "write",
          "issues": "write",
          "merge_queues": "write",
          "metadata": "read",
          "models": "read",
          "packages": "write",
          "pages": "write",
          "pull_requests": "write",
          "repository_hooks": "write",
          "repository_projects": "write",
          "security_events": "write",
          "statuses": "write",
          "vulnerability_alerts": "read"
        },
        "events": [
          "branch_protection_rule",
          "check_run",
          "check_suite",
          "create",
          "delete",
          "deployment",
          "deployment_status",
          "discussion",
          "discussion_comment",
          "fork",
          "gollum",
          "issues",
          "issue_comment",
          "label",
          "merge_group",
          "milestone",
          "page_build",
          "public",
          "pull_request",
          "pull_request_review",
          "pull_request_review_comment",
          "push",
          "registry_package",
          "release",
          "repository",
          "repository_dispatch",
          "status",
          "watch",
          "workflow_dispatch",
          "workflow_run"
        ]
      },
      "pull_requests": [
        {
          "url": "https://api.github.com/repos/ducthangho/tra-luat/pulls/1249",
          "id": 5176379564,
          "number": 1249,
          "head": {
            "ref": "agent/wp1240-g1-claude",
            "sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          },
          "base": {
            "ref": "master",
            "sha": "3163f4d02a583787a9340c63a1f5eebd3780d970",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          }
        }
      ]
    },
    {
      "id": 127436213872,
      "name": "gate-nhanh-manh (ubuntu-latest, 5)",
      "node_id": "CR_kwDOTNeRjc8AAAAdq8pOcA",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "external_id": "4781bb22-7ee1-58e8-8561-aeacbd4b5985",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213872",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213872",
      "details_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213872",
      "status": "completed",
      "conclusion": "success",
      "started_at": "2026-11-05T18:10:46Z",
      "completed_at": "2026-11-05T18:11:41Z",
      "output": {
        "title": null,
        "summary": null,
        "text": null,
        "annotations_count": 2,
        "annotations_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213872/annotations"
      },
      "check_suite": {
        "id": 114030831118
      },
      "app": {
        "id": 15368,
        "client_id": "Iv1.05c79e9ad1f6bdfa",
        "slug": "github-actions",
        "node_id": "MDM6QXBwMTUzNjg=",
        "owner": {
          "login": "github",
          "id": 9919,
          "node_id": "MDEyOk9yZ2FuaXphdGlvbjk5MTk=",
          "avatar_url": "https://avatars.githubusercontent.com/u/9919?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/github",
          "html_url": "https://github.com/github",
          "followers_url": "https://api.github.com/users/github/followers",
          "following_url": "https://api.github.com/users/github/following{/other_user}",
          "gists_url": "https://api.github.com/users/github/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/github/subscriptions",
          "organizations_url": "https://api.github.com/users/github/orgs",
          "repos_url": "https://api.github.com/users/github/repos",
          "events_url": "https://api.github.com/users/github/events{/privacy}",
          "received_events_url": "https://api.github.com/users/github/received_events",
          "type": "Organization",
          "user_view_type": "public",
          "site_admin": false
        },
        "name": "GitHub Actions",
        "description": "Automate your workflow from idea to production",
        "external_url": "https://help.github.com/en/actions",
        "html_url": "https://github.com/apps/github-actions",
        "created_at": "2018-07-30T09:30:17Z",
        "updated_at": "2026-06-18T16:17:48Z",
        "permissions": {
          "actions": "write",
          "administration": "read",
          "artifact_metadata": "write",
          "attestations": "write",
          "checks": "write",
          "code_quality": "write",
          "contents": "write",
          "copilot_requests": "write",
          "deployments": "write",
          "discussions": "write",
          "drives": "write",
          "issues": "write",
          "merge_queues": "write",
          "metadata": "read",
          "models": "read",
          "packages": "write",
          "pages": "write",
          "pull_requests": "write",
          "repository_hooks": "write",
          "repository_projects": "write",
          "security_events": "write",
          "statuses": "write",
          "vulnerability_alerts": "read"
        },
        "events": [
          "branch_protection_rule",
          "check_run",
          "check_suite",
          "create",
          "delete",
          "deployment",
          "deployment_status",
          "discussion",
          "discussion_comment",
          "fork",
          "gollum",
          "issues",
          "issue_comment",
          "label",
          "merge_group",
          "milestone",
          "page_build",
          "public",
          "pull_request",
          "pull_request_review",
          "pull_request_review_comment",
          "push",
          "registry_package",
          "release",
          "repository",
          "repository_dispatch",
          "status",
          "watch",
          "workflow_dispatch",
          "workflow_run"
        ]
      },
      "pull_requests": [
        {
          "url": "https://api.github.com/repos/ducthangho/tra-luat/pulls/1249",
          "id": 5176379564,
          "number": 1249,
          "head": {
            "ref": "agent/wp1240-g1-claude",
            "sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          },
          "base": {
            "ref": "master",
            "sha": "3163f4d02a583787a9340c63a1f5eebd3780d970",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          }
        }
      ]
    },
    {
      "id": 127436213870,
      "name": "gate-cong-cu (ubuntu-latest, 7)",
      "node_id": "CR_kwDOTNeRjc8AAAAdq8pObg",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "external_id": "ef5a619c-9ba8-5565-82af-87108eae5441",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213870",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213870",
      "details_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213870",
      "status": "completed",
      "conclusion": "success",
      "started_at": "2026-11-05T18:10:46Z",
      "completed_at": "2026-11-05T18:23:32Z",
      "output": {
        "title": null,
        "summary": null,
        "text": null,
        "annotations_count": 2,
        "annotations_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213870/annotations"
      },
      "check_suite": {
        "id": 114030831118
      },
      "app": {
        "id": 15368,
        "client_id": "Iv1.05c79e9ad1f6bdfa",
        "slug": "github-actions",
        "node_id": "MDM6QXBwMTUzNjg=",
        "owner": {
          "login": "github",
          "id": 9919,
          "node_id": "MDEyOk9yZ2FuaXphdGlvbjk5MTk=",
          "avatar_url": "https://avatars.githubusercontent.com/u/9919?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/github",
          "html_url": "https://github.com/github",
          "followers_url": "https://api.github.com/users/github/followers",
          "following_url": "https://api.github.com/users/github/following{/other_user}",
          "gists_url": "https://api.github.com/users/github/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/github/subscriptions",
          "organizations_url": "https://api.github.com/users/github/orgs",
          "repos_url": "https://api.github.com/users/github/repos",
          "events_url": "https://api.github.com/users/github/events{/privacy}",
          "received_events_url": "https://api.github.com/users/github/received_events",
          "type": "Organization",
          "user_view_type": "public",
          "site_admin": false
        },
        "name": "GitHub Actions",
        "description": "Automate your workflow from idea to production",
        "external_url": "https://help.github.com/en/actions",
        "html_url": "https://github.com/apps/github-actions",
        "created_at": "2018-07-30T09:30:17Z",
        "updated_at": "2026-06-18T16:17:48Z",
        "permissions": {
          "actions": "write",
          "administration": "read",
          "artifact_metadata": "write",
          "attestations": "write",
          "checks": "write",
          "code_quality": "write",
          "contents": "write",
          "copilot_requests": "write",
          "deployments": "write",
          "discussions": "write",
          "drives": "write",
          "issues": "write",
          "merge_queues": "write",
          "metadata": "read",
          "models": "read",
          "packages": "write",
          "pages": "write",
          "pull_requests": "write",
          "repository_hooks": "write",
          "repository_projects": "write",
          "security_events": "write",
          "statuses": "write",
          "vulnerability_alerts": "read"
        },
        "events": [
          "branch_protection_rule",
          "check_run",
          "check_suite",
          "create",
          "delete",
          "deployment",
          "deployment_status",
          "discussion",
          "discussion_comment",
          "fork",
          "gollum",
          "issues",
          "issue_comment",
          "label",
          "merge_group",
          "milestone",
          "page_build",
          "public",
          "pull_request",
          "pull_request_review",
          "pull_request_review_comment",
          "push",
          "registry_package",
          "release",
          "repository",
          "repository_dispatch",
          "status",
          "watch",
          "workflow_dispatch",
          "workflow_run"
        ]
      },
      "pull_requests": [
        {
          "url": "https://api.github.com/repos/ducthangho/tra-luat/pulls/1249",
          "id": 5176379564,
          "number": 1249,
          "head": {
            "ref": "agent/wp1240-g1-claude",
            "sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          },
          "base": {
            "ref": "master",
            "sha": "3163f4d02a583787a9340c63a1f5eebd3780d970",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          }
        }
      ]
    },
    {
      "id": 127436213864,
      "name": "gate-nhanh-manh (ubuntu-latest, 3)",
      "node_id": "CR_kwDOTNeRjc8AAAAdq8pOaA",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "external_id": "2dfe8e47-f496-5c78-b474-593c1e961b79",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213864",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213864",
      "details_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213864",
      "status": "completed",
      "conclusion": "success",
      "started_at": "2026-11-05T18:10:47Z",
      "completed_at": "2026-11-05T18:12:22Z",
      "output": {
        "title": null,
        "summary": null,
        "text": null,
        "annotations_count": 2,
        "annotations_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213864/annotations"
      },
      "check_suite": {
        "id": 114030831118
      },
      "app": {
        "id": 15368,
        "client_id": "Iv1.05c79e9ad1f6bdfa",
        "slug": "github-actions",
        "node_id": "MDM6QXBwMTUzNjg=",
        "owner": {
          "login": "github",
          "id": 9919,
          "node_id": "MDEyOk9yZ2FuaXphdGlvbjk5MTk=",
          "avatar_url": "https://avatars.githubusercontent.com/u/9919?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/github",
          "html_url": "https://github.com/github",
          "followers_url": "https://api.github.com/users/github/followers",
          "following_url": "https://api.github.com/users/github/following{/other_user}",
          "gists_url": "https://api.github.com/users/github/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/github/subscriptions",
          "organizations_url": "https://api.github.com/users/github/orgs",
          "repos_url": "https://api.github.com/users/github/repos",
          "events_url": "https://api.github.com/users/github/events{/privacy}",
          "received_events_url": "https://api.github.com/users/github/received_events",
          "type": "Organization",
          "user_view_type": "public",
          "site_admin": false
        },
        "name": "GitHub Actions",
        "description": "Automate your workflow from idea to production",
        "external_url": "https://help.github.com/en/actions",
        "html_url": "https://github.com/apps/github-actions",
        "created_at": "2018-07-30T09:30:17Z",
        "updated_at": "2026-06-18T16:17:48Z",
        "permissions": {
          "actions": "write",
          "administration": "read",
          "artifact_metadata": "write",
          "attestations": "write",
          "checks": "write",
          "code_quality": "write",
          "contents": "write",
          "copilot_requests": "write",
          "deployments": "write",
          "discussions": "write",
          "drives": "write",
          "issues": "write",
          "merge_queues": "write",
          "metadata": "read",
          "models": "read",
          "packages": "write",
          "pages": "write",
          "pull_requests": "write",
          "repository_hooks": "write",
          "repository_projects": "write",
          "security_events": "write",
          "statuses": "write",
          "vulnerability_alerts": "read"
        },
        "events": [
          "branch_protection_rule",
          "check_run",
          "check_suite",
          "create",
          "delete",
          "deployment",
          "deployment_status",
          "discussion",
          "discussion_comment",
          "fork",
          "gollum",
          "issues",
          "issue_comment",
          "label",
          "merge_group",
          "milestone",
          "page_build",
          "public",
          "pull_request",
          "pull_request_review",
          "pull_request_review_comment",
          "push",
          "registry_package",
          "release",
          "repository",
          "repository_dispatch",
          "status",
          "watch",
          "workflow_dispatch",
          "workflow_run"
        ]
      },
      "pull_requests": [
        {
          "url": "https://api.github.com/repos/ducthangho/tra-luat/pulls/1249",
          "id": 5176379564,
          "number": 1249,
          "head": {
            "ref": "agent/wp1240-g1-claude",
            "sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          },
          "base": {
            "ref": "master",
            "sha": "3163f4d02a583787a9340c63a1f5eebd3780d970",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          }
        }
      ]
    },
    {
      "id": 127436213669,
      "name": "gate-nhanh-manh (ubuntu-latest, 4)",
      "node_id": "CR_kwDOTNeRjc8AAAAdq8pNpQ",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "external_id": "548f43ee-0f56-5709-814d-78d47825c3eb",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213669",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213669",
      "details_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213669",
      "status": "completed",
      "conclusion": "success",
      "started_at": "2026-11-05T18:10:46Z",
      "completed_at": "2026-11-05T18:12:00Z",
      "output": {
        "title": null,
        "summary": null,
        "text": null,
        "annotations_count": 2,
        "annotations_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213669/annotations"
      },
      "check_suite": {
        "id": 114030831118
      },
      "app": {
        "id": 15368,
        "client_id": "Iv1.05c79e9ad1f6bdfa",
        "slug": "github-actions",
        "node_id": "MDM6QXBwMTUzNjg=",
        "owner": {
          "login": "github",
          "id": 9919,
          "node_id": "MDEyOk9yZ2FuaXphdGlvbjk5MTk=",
          "avatar_url": "https://avatars.githubusercontent.com/u/9919?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/github",
          "html_url": "https://github.com/github",
          "followers_url": "https://api.github.com/users/github/followers",
          "following_url": "https://api.github.com/users/github/following{/other_user}",
          "gists_url": "https://api.github.com/users/github/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/github/subscriptions",
          "organizations_url": "https://api.github.com/users/github/orgs",
          "repos_url": "https://api.github.com/users/github/repos",
          "events_url": "https://api.github.com/users/github/events{/privacy}",
          "received_events_url": "https://api.github.com/users/github/received_events",
          "type": "Organization",
          "user_view_type": "public",
          "site_admin": false
        },
        "name": "GitHub Actions",
        "description": "Automate your workflow from idea to production",
        "external_url": "https://help.github.com/en/actions",
        "html_url": "https://github.com/apps/github-actions",
        "created_at": "2018-07-30T09:30:17Z",
        "updated_at": "2026-06-18T16:17:48Z",
        "permissions": {
          "actions": "write",
          "administration": "read",
          "artifact_metadata": "write",
          "attestations": "write",
          "checks": "write",
          "code_quality": "write",
          "contents": "write",
          "copilot_requests": "write",
          "deployments": "write",
          "discussions": "write",
          "drives": "write",
          "issues": "write",
          "merge_queues": "write",
          "metadata": "read",
          "models": "read",
          "packages": "write",
          "pages": "write",
          "pull_requests": "write",
          "repository_hooks": "write",
          "repository_projects": "write",
          "security_events": "write",
          "statuses": "write",
          "vulnerability_alerts": "read"
        },
        "events": [
          "branch_protection_rule",
          "check_run",
          "check_suite",
          "create",
          "delete",
          "deployment",
          "deployment_status",
          "discussion",
          "discussion_comment",
          "fork",
          "gollum",
          "issues",
          "issue_comment",
          "label",
          "merge_group",
          "milestone",
          "page_build",
          "public",
          "pull_request",
          "pull_request_review",
          "pull_request_review_comment",
          "push",
          "registry_package",
          "release",
          "repository",
          "repository_dispatch",
          "status",
          "watch",
          "workflow_dispatch",
          "workflow_run"
        ]
      },
      "pull_requests": [
        {
          "url": "https://api.github.com/repos/ducthangho/tra-luat/pulls/1249",
          "id": 5176379564,
          "number": 1249,
          "head": {
            "ref": "agent/wp1240-g1-claude",
            "sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          },
          "base": {
            "ref": "master",
            "sha": "3163f4d02a583787a9340c63a1f5eebd3780d970",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          }
        }
      ]
    },
    {
      "id": 127436213654,
      "name": "gate-nhanh-manh (ubuntu-latest, 0)",
      "node_id": "CR_kwDOTNeRjc8AAAAdq8pNlg",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "external_id": "ec9ba0c8-8438-5795-8031-4800e8e5e273",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213654",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213654",
      "details_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213654",
      "status": "completed",
      "conclusion": "success",
      "started_at": "2026-11-05T18:10:47Z",
      "completed_at": "2026-11-05T18:11:46Z",
      "output": {
        "title": null,
        "summary": null,
        "text": null,
        "annotations_count": 2,
        "annotations_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213654/annotations"
      },
      "check_suite": {
        "id": 114030831118
      },
      "app": {
        "id": 15368,
        "client_id": "Iv1.05c79e9ad1f6bdfa",
        "slug": "github-actions",
        "node_id": "MDM6QXBwMTUzNjg=",
        "owner": {
          "login": "github",
          "id": 9919,
          "node_id": "MDEyOk9yZ2FuaXphdGlvbjk5MTk=",
          "avatar_url": "https://avatars.githubusercontent.com/u/9919?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/github",
          "html_url": "https://github.com/github",
          "followers_url": "https://api.github.com/users/github/followers",
          "following_url": "https://api.github.com/users/github/following{/other_user}",
          "gists_url": "https://api.github.com/users/github/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/github/subscriptions",
          "organizations_url": "https://api.github.com/users/github/orgs",
          "repos_url": "https://api.github.com/users/github/repos",
          "events_url": "https://api.github.com/users/github/events{/privacy}",
          "received_events_url": "https://api.github.com/users/github/received_events",
          "type": "Organization",
          "user_view_type": "public",
          "site_admin": false
        },
        "name": "GitHub Actions",
        "description": "Automate your workflow from idea to production",
        "external_url": "https://help.github.com/en/actions",
        "html_url": "https://github.com/apps/github-actions",
        "created_at": "2018-07-30T09:30:17Z",
        "updated_at": "2026-06-18T16:17:48Z",
        "permissions": {
          "actions": "write",
          "administration": "read",
          "artifact_metadata": "write",
          "attestations": "write",
          "checks": "write",
          "code_quality": "write",
          "contents": "write",
          "copilot_requests": "write",
          "deployments": "write",
          "discussions": "write",
          "drives": "write",
          "issues": "write",
          "merge_queues": "write",
          "metadata": "read",
          "models": "read",
          "packages": "write",
          "pages": "write",
          "pull_requests": "write",
          "repository_hooks": "write",
          "repository_projects": "write",
          "security_events": "write",
          "statuses": "write",
          "vulnerability_alerts": "read"
        },
        "events": [
          "branch_protection_rule",
          "check_run",
          "check_suite",
          "create",
          "delete",
          "deployment",
          "deployment_status",
          "discussion",
          "discussion_comment",
          "fork",
          "gollum",
          "issues",
          "issue_comment",
          "label",
          "merge_group",
          "milestone",
          "page_build",
          "public",
          "pull_request",
          "pull_request_review",
          "pull_request_review_comment",
          "push",
          "registry_package",
          "release",
          "repository",
          "repository_dispatch",
          "status",
          "watch",
          "workflow_dispatch",
          "workflow_run"
        ]
      },
      "pull_requests": [
        {
          "url": "https://api.github.com/repos/ducthangho/tra-luat/pulls/1249",
          "id": 5176379564,
          "number": 1249,
          "head": {
            "ref": "agent/wp1240-g1-claude",
            "sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          },
          "base": {
            "ref": "master",
            "sha": "3163f4d02a583787a9340c63a1f5eebd3780d970",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          }
        }
      ]
    },
    {
      "id": 127436213596,
      "name": "gate-nhanh-manh (ubuntu-latest, 1)",
      "node_id": "CR_kwDOTNeRjc8AAAAdq8pNXA",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "external_id": "b354d6e4-c372-5658-8b77-cfae025588c7",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213596",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213596",
      "details_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213596",
      "status": "completed",
      "conclusion": "success",
      "started_at": "2026-11-05T18:10:47Z",
      "completed_at": "2026-11-05T18:11:42Z",
      "output": {
        "title": null,
        "summary": null,
        "text": null,
        "annotations_count": 2,
        "annotations_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213596/annotations"
      },
      "check_suite": {
        "id": 114030831118
      },
      "app": {
        "id": 15368,
        "client_id": "Iv1.05c79e9ad1f6bdfa",
        "slug": "github-actions",
        "node_id": "MDM6QXBwMTUzNjg=",
        "owner": {
          "login": "github",
          "id": 9919,
          "node_id": "MDEyOk9yZ2FuaXphdGlvbjk5MTk=",
          "avatar_url": "https://avatars.githubusercontent.com/u/9919?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/github",
          "html_url": "https://github.com/github",
          "followers_url": "https://api.github.com/users/github/followers",
          "following_url": "https://api.github.com/users/github/following{/other_user}",
          "gists_url": "https://api.github.com/users/github/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/github/subscriptions",
          "organizations_url": "https://api.github.com/users/github/orgs",
          "repos_url": "https://api.github.com/users/github/repos",
          "events_url": "https://api.github.com/users/github/events{/privacy}",
          "received_events_url": "https://api.github.com/users/github/received_events",
          "type": "Organization",
          "user_view_type": "public",
          "site_admin": false
        },
        "name": "GitHub Actions",
        "description": "Automate your workflow from idea to production",
        "external_url": "https://help.github.com/en/actions",
        "html_url": "https://github.com/apps/github-actions",
        "created_at": "2018-07-30T09:30:17Z",
        "updated_at": "2026-06-18T16:17:48Z",
        "permissions": {
          "actions": "write",
          "administration": "read",
          "artifact_metadata": "write",
          "attestations": "write",
          "checks": "write",
          "code_quality": "write",
          "contents": "write",
          "copilot_requests": "write",
          "deployments": "write",
          "discussions": "write",
          "drives": "write",
          "issues": "write",
          "merge_queues": "write",
          "metadata": "read",
          "models": "read",
          "packages": "write",
          "pages": "write",
          "pull_requests": "write",
          "repository_hooks": "write",
          "repository_projects": "write",
          "security_events": "write",
          "statuses": "write",
          "vulnerability_alerts": "read"
        },
        "events": [
          "branch_protection_rule",
          "check_run",
          "check_suite",
          "create",
          "delete",
          "deployment",
          "deployment_status",
          "discussion",
          "discussion_comment",
          "fork",
          "gollum",
          "issues",
          "issue_comment",
          "label",
          "merge_group",
          "milestone",
          "page_build",
          "public",
          "pull_request",
          "pull_request_review",
          "pull_request_review_comment",
          "push",
          "registry_package",
          "release",
          "repository",
          "repository_dispatch",
          "status",
          "watch",
          "workflow_dispatch",
          "workflow_run"
        ]
      },
      "pull_requests": [
        {
          "url": "https://api.github.com/repos/ducthangho/tra-luat/pulls/1249",
          "id": 5176379564,
          "number": 1249,
          "head": {
            "ref": "agent/wp1240-g1-claude",
            "sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          },
          "base": {
            "ref": "master",
            "sha": "3163f4d02a583787a9340c63a1f5eebd3780d970",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          }
        }
      ]
    },
    {
      "id": 127436213593,
      "name": "gate-nhanh-manh (ubuntu-latest, 7)",
      "node_id": "CR_kwDOTNeRjc8AAAAdq8pNWQ",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "external_id": "8e535882-0d1d-59bd-a394-42e404bc702b",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213593",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213593",
      "details_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213593",
      "status": "completed",
      "conclusion": "success",
      "started_at": "2026-11-05T18:10:47Z",
      "completed_at": "2026-11-05T18:12:24Z",
      "output": {
        "title": null,
        "summary": null,
        "text": null,
        "annotations_count": 2,
        "annotations_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213593/annotations"
      },
      "check_suite": {
        "id": 114030831118
      },
      "app": {
        "id": 15368,
        "client_id": "Iv1.05c79e9ad1f6bdfa",
        "slug": "github-actions",
        "node_id": "MDM6QXBwMTUzNjg=",
        "owner": {
          "login": "github",
          "id": 9919,
          "node_id": "MDEyOk9yZ2FuaXphdGlvbjk5MTk=",
          "avatar_url": "https://avatars.githubusercontent.com/u/9919?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/github",
          "html_url": "https://github.com/github",
          "followers_url": "https://api.github.com/users/github/followers",
          "following_url": "https://api.github.com/users/github/following{/other_user}",
          "gists_url": "https://api.github.com/users/github/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/github/subscriptions",
          "organizations_url": "https://api.github.com/users/github/orgs",
          "repos_url": "https://api.github.com/users/github/repos",
          "events_url": "https://api.github.com/users/github/events{/privacy}",
          "received_events_url": "https://api.github.com/users/github/received_events",
          "type": "Organization",
          "user_view_type": "public",
          "site_admin": false
        },
        "name": "GitHub Actions",
        "description": "Automate your workflow from idea to production",
        "external_url": "https://help.github.com/en/actions",
        "html_url": "https://github.com/apps/github-actions",
        "created_at": "2018-07-30T09:30:17Z",
        "updated_at": "2026-06-18T16:17:48Z",
        "permissions": {
          "actions": "write",
          "administration": "read",
          "artifact_metadata": "write",
          "attestations": "write",
          "checks": "write",
          "code_quality": "write",
          "contents": "write",
          "copilot_requests": "write",
          "deployments": "write",
          "discussions": "write",
          "drives": "write",
          "issues": "write",
          "merge_queues": "write",
          "metadata": "read",
          "models": "read",
          "packages": "write",
          "pages": "write",
          "pull_requests": "write",
          "repository_hooks": "write",
          "repository_projects": "write",
          "security_events": "write",
          "statuses": "write",
          "vulnerability_alerts": "read"
        },
        "events": [
          "branch_protection_rule",
          "check_run",
          "check_suite",
          "create",
          "delete",
          "deployment",
          "deployment_status",
          "discussion",
          "discussion_comment",
          "fork",
          "gollum",
          "issues",
          "issue_comment",
          "label",
          "merge_group",
          "milestone",
          "page_build",
          "public",
          "pull_request",
          "pull_request_review",
          "pull_request_review_comment",
          "push",
          "registry_package",
          "release",
          "repository",
          "repository_dispatch",
          "status",
          "watch",
          "workflow_dispatch",
          "workflow_run"
        ]
      },
      "pull_requests": [
        {
          "url": "https://api.github.com/repos/ducthangho/tra-luat/pulls/1249",
          "id": 5176379564,
          "number": 1249,
          "head": {
            "ref": "agent/wp1240-g1-claude",
            "sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          },
          "base": {
            "ref": "master",
            "sha": "3163f4d02a583787a9340c63a1f5eebd3780d970",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          }
        }
      ]
    },
    {
      "id": 127436213573,
      "name": "gate-packet-loop (ubuntu-latest)",
      "node_id": "CR_kwDOTNeRjc8AAAAdq8pNRQ",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "external_id": "5fcee2d4-1aab-52be-aff1-a5c5f058f061",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213573",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213573",
      "details_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213573",
      "status": "completed",
      "conclusion": "success",
      "started_at": "2026-11-05T18:10:46Z",
      "completed_at": "2026-11-05T19:13:21Z",
      "output": {
        "title": null,
        "summary": null,
        "text": null,
        "annotations_count": 2,
        "annotations_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213573/annotations"
      },
      "check_suite": {
        "id": 114030831118
      },
      "app": {
        "id": 15368,
        "client_id": "Iv1.05c79e9ad1f6bdfa",
        "slug": "github-actions",
        "node_id": "MDM6QXBwMTUzNjg=",
        "owner": {
          "login": "github",
          "id": 9919,
          "node_id": "MDEyOk9yZ2FuaXphdGlvbjk5MTk=",
          "avatar_url": "https://avatars.githubusercontent.com/u/9919?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/github",
          "html_url": "https://github.com/github",
          "followers_url": "https://api.github.com/users/github/followers",
          "following_url": "https://api.github.com/users/github/following{/other_user}",
          "gists_url": "https://api.github.com/users/github/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/github/subscriptions",
          "organizations_url": "https://api.github.com/users/github/orgs",
          "repos_url": "https://api.github.com/users/github/repos",
          "events_url": "https://api.github.com/users/github/events{/privacy}",
          "received_events_url": "https://api.github.com/users/github/received_events",
          "type": "Organization",
          "user_view_type": "public",
          "site_admin": false
        },
        "name": "GitHub Actions",
        "description": "Automate your workflow from idea to production",
        "external_url": "https://help.github.com/en/actions",
        "html_url": "https://github.com/apps/github-actions",
        "created_at": "2018-07-30T09:30:17Z",
        "updated_at": "2026-06-18T16:17:48Z",
        "permissions": {
          "actions": "write",
          "administration": "read",
          "artifact_metadata": "write",
          "attestations": "write",
          "checks": "write",
          "code_quality": "write",
          "contents": "write",
          "copilot_requests": "write",
          "deployments": "write",
          "discussions": "write",
          "drives": "write",
          "issues": "write",
          "merge_queues": "write",
          "metadata": "read",
          "models": "read",
          "packages": "write",
          "pages": "write",
          "pull_requests": "write",
          "repository_hooks": "write",
          "repository_projects": "write",
          "security_events": "write",
          "statuses": "write",
          "vulnerability_alerts": "read"
        },
        "events": [
          "branch_protection_rule",
          "check_run",
          "check_suite",
          "create",
          "delete",
          "deployment",
          "deployment_status",
          "discussion",
          "discussion_comment",
          "fork",
          "gollum",
          "issues",
          "issue_comment",
          "label",
          "merge_group",
          "milestone",
          "page_build",
          "public",
          "pull_request",
          "pull_request_review",
          "pull_request_review_comment",
          "push",
          "registry_package",
          "release",
          "repository",
          "repository_dispatch",
          "status",
          "watch",
          "workflow_dispatch",
          "workflow_run"
        ]
      },
      "pull_requests": [
        {
          "url": "https://api.github.com/repos/ducthangho/tra-luat/pulls/1249",
          "id": 5176379564,
          "number": 1249,
          "head": {
            "ref": "agent/wp1240-g1-claude",
            "sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          },
          "base": {
            "ref": "master",
            "sha": "3163f4d02a583787a9340c63a1f5eebd3780d970",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          }
        }
      ]
    },
    {
      "id": 127436213571,
      "name": "gate-cong-cu (ubuntu-latest, 1)",
      "node_id": "CR_kwDOTNeRjc8AAAAdq8pNQw",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "external_id": "c6650ba7-d2ba-5092-bad9-6fc8d58b20d5",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213571",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213571",
      "details_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213571",
      "status": "completed",
      "conclusion": "success",
      "started_at": "2026-11-05T18:10:46Z",
      "completed_at": "2026-11-05T18:31:40Z",
      "output": {
        "title": null,
        "summary": null,
        "text": null,
        "annotations_count": 2,
        "annotations_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213571/annotations"
      },
      "check_suite": {
        "id": 114030831118
      },
      "app": {
        "id": 15368,
        "client_id": "Iv1.05c79e9ad1f6bdfa",
        "slug": "github-actions",
        "node_id": "MDM6QXBwMTUzNjg=",
        "owner": {
          "login": "github",
          "id": 9919,
          "node_id": "MDEyOk9yZ2FuaXphdGlvbjk5MTk=",
          "avatar_url": "https://avatars.githubusercontent.com/u/9919?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/github",
          "html_url": "https://github.com/github",
          "followers_url": "https://api.github.com/users/github/followers",
          "following_url": "https://api.github.com/users/github/following{/other_user}",
          "gists_url": "https://api.github.com/users/github/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/github/subscriptions",
          "organizations_url": "https://api.github.com/users/github/orgs",
          "repos_url": "https://api.github.com/users/github/repos",
          "events_url": "https://api.github.com/users/github/events{/privacy}",
          "received_events_url": "https://api.github.com/users/github/received_events",
          "type": "Organization",
          "user_view_type": "public",
          "site_admin": false
        },
        "name": "GitHub Actions",
        "description": "Automate your workflow from idea to production",
        "external_url": "https://help.github.com/en/actions",
        "html_url": "https://github.com/apps/github-actions",
        "created_at": "2018-07-30T09:30:17Z",
        "updated_at": "2026-06-18T16:17:48Z",
        "permissions": {
          "actions": "write",
          "administration": "read",
          "artifact_metadata": "write",
          "attestations": "write",
          "checks": "write",
          "code_quality": "write",
          "contents": "write",
          "copilot_requests": "write",
          "deployments": "write",
          "discussions": "write",
          "drives": "write",
          "issues": "write",
          "merge_queues": "write",
          "metadata": "read",
          "models": "read",
          "packages": "write",
          "pages": "write",
          "pull_requests": "write",
          "repository_hooks": "write",
          "repository_projects": "write",
          "security_events": "write",
          "statuses": "write",
          "vulnerability_alerts": "read"
        },
        "events": [
          "branch_protection_rule",
          "check_run",
          "check_suite",
          "create",
          "delete",
          "deployment",
          "deployment_status",
          "discussion",
          "discussion_comment",
          "fork",
          "gollum",
          "issues",
          "issue_comment",
          "label",
          "merge_group",
          "milestone",
          "page_build",
          "public",
          "pull_request",
          "pull_request_review",
          "pull_request_review_comment",
          "push",
          "registry_package",
          "release",
          "repository",
          "repository_dispatch",
          "status",
          "watch",
          "workflow_dispatch",
          "workflow_run"
        ]
      },
      "pull_requests": [
        {
          "url": "https://api.github.com/repos/ducthangho/tra-luat/pulls/1249",
          "id": 5176379564,
          "number": 1249,
          "head": {
            "ref": "agent/wp1240-g1-claude",
            "sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          },
          "base": {
            "ref": "master",
            "sha": "3163f4d02a583787a9340c63a1f5eebd3780d970",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          }
        }
      ]
    },
    {
      "id": 127436213564,
      "name": "gate-nhanh-manh (ubuntu-latest, 6)",
      "node_id": "CR_kwDOTNeRjc8AAAAdq8pNPA",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "external_id": "686a6a8d-bcf2-501c-938e-27cee3bb39fa",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213564",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213564",
      "details_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213564",
      "status": "completed",
      "conclusion": "success",
      "started_at": "2026-11-05T18:10:46Z",
      "completed_at": "2026-11-05T18:11:57Z",
      "output": {
        "title": null,
        "summary": null,
        "text": null,
        "annotations_count": 2,
        "annotations_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213564/annotations"
      },
      "check_suite": {
        "id": 114030831118
      },
      "app": {
        "id": 15368,
        "client_id": "Iv1.05c79e9ad1f6bdfa",
        "slug": "github-actions",
        "node_id": "MDM6QXBwMTUzNjg=",
        "owner": {
          "login": "github",
          "id": 9919,
          "node_id": "MDEyOk9yZ2FuaXphdGlvbjk5MTk=",
          "avatar_url": "https://avatars.githubusercontent.com/u/9919?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/github",
          "html_url": "https://github.com/github",
          "followers_url": "https://api.github.com/users/github/followers",
          "following_url": "https://api.github.com/users/github/following{/other_user}",
          "gists_url": "https://api.github.com/users/github/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/github/subscriptions",
          "organizations_url": "https://api.github.com/users/github/orgs",
          "repos_url": "https://api.github.com/users/github/repos",
          "events_url": "https://api.github.com/users/github/events{/privacy}",
          "received_events_url": "https://api.github.com/users/github/received_events",
          "type": "Organization",
          "user_view_type": "public",
          "site_admin": false
        },
        "name": "GitHub Actions",
        "description": "Automate your workflow from idea to production",
        "external_url": "https://help.github.com/en/actions",
        "html_url": "https://github.com/apps/github-actions",
        "created_at": "2018-07-30T09:30:17Z",
        "updated_at": "2026-06-18T16:17:48Z",
        "permissions": {
          "actions": "write",
          "administration": "read",
          "artifact_metadata": "write",
          "attestations": "write",
          "checks": "write",
          "code_quality": "write",
          "contents": "write",
          "copilot_requests": "write",
          "deployments": "write",
          "discussions": "write",
          "drives": "write",
          "issues": "write",
          "merge_queues": "write",
          "metadata": "read",
          "models": "read",
          "packages": "write",
          "pages": "write",
          "pull_requests": "write",
          "repository_hooks": "write",
          "repository_projects": "write",
          "security_events": "write",
          "statuses": "write",
          "vulnerability_alerts": "read"
        },
        "events": [
          "branch_protection_rule",
          "check_run",
          "check_suite",
          "create",
          "delete",
          "deployment",
          "deployment_status",
          "discussion",
          "discussion_comment",
          "fork",
          "gollum",
          "issues",
          "issue_comment",
          "label",
          "merge_group",
          "milestone",
          "page_build",
          "public",
          "pull_request",
          "pull_request_review",
          "pull_request_review_comment",
          "push",
          "registry_package",
          "release",
          "repository",
          "repository_dispatch",
          "status",
          "watch",
          "workflow_dispatch",
          "workflow_run"
        ]
      },
      "pull_requests": [
        {
          "url": "https://api.github.com/repos/ducthangho/tra-luat/pulls/1249",
          "id": 5176379564,
          "number": 1249,
          "head": {
            "ref": "agent/wp1240-g1-claude",
            "sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          },
          "base": {
            "ref": "master",
            "sha": "3163f4d02a583787a9340c63a1f5eebd3780d970",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          }
        }
      ]
    },
    {
      "id": 127436213563,
      "name": "gate-cong-cu (ubuntu-latest, 0)",
      "node_id": "CR_kwDOTNeRjc8AAAAdq8pNOw",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "external_id": "2afeea2f-2add-556e-9eb7-1b7322ca6c62",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213563",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213563",
      "details_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213563",
      "status": "completed",
      "conclusion": "success",
      "started_at": "2026-11-05T18:10:47Z",
      "completed_at": "2026-11-05T18:32:22Z",
      "output": {
        "title": null,
        "summary": null,
        "text": null,
        "annotations_count": 2,
        "annotations_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213563/annotations"
      },
      "check_suite": {
        "id": 114030831118
      },
      "app": {
        "id": 15368,
        "client_id": "Iv1.05c79e9ad1f6bdfa",
        "slug": "github-actions",
        "node_id": "MDM6QXBwMTUzNjg=",
        "owner": {
          "login": "github",
          "id": 9919,
          "node_id": "MDEyOk9yZ2FuaXphdGlvbjk5MTk=",
          "avatar_url": "https://avatars.githubusercontent.com/u/9919?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/github",
          "html_url": "https://github.com/github",
          "followers_url": "https://api.github.com/users/github/followers",
          "following_url": "https://api.github.com/users/github/following{/other_user}",
          "gists_url": "https://api.github.com/users/github/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/github/subscriptions",
          "organizations_url": "https://api.github.com/users/github/orgs",
          "repos_url": "https://api.github.com/users/github/repos",
          "events_url": "https://api.github.com/users/github/events{/privacy}",
          "received_events_url": "https://api.github.com/users/github/received_events",
          "type": "Organization",
          "user_view_type": "public",
          "site_admin": false
        },
        "name": "GitHub Actions",
        "description": "Automate your workflow from idea to production",
        "external_url": "https://help.github.com/en/actions",
        "html_url": "https://github.com/apps/github-actions",
        "created_at": "2018-07-30T09:30:17Z",
        "updated_at": "2026-06-18T16:17:48Z",
        "permissions": {
          "actions": "write",
          "administration": "read",
          "artifact_metadata": "write",
          "attestations": "write",
          "checks": "write",
          "code_quality": "write",
          "contents": "write",
          "copilot_requests": "write",
          "deployments": "write",
          "discussions": "write",
          "drives": "write",
          "issues": "write",
          "merge_queues": "write",
          "metadata": "read",
          "models": "read",
          "packages": "write",
          "pages": "write",
          "pull_requests": "write",
          "repository_hooks": "write",
          "repository_projects": "write",
          "security_events": "write",
          "statuses": "write",
          "vulnerability_alerts": "read"
        },
        "events": [
          "branch_protection_rule",
          "check_run",
          "check_suite",
          "create",
          "delete",
          "deployment",
          "deployment_status",
          "discussion",
          "discussion_comment",
          "fork",
          "gollum",
          "issues",
          "issue_comment",
          "label",
          "merge_group",
          "milestone",
          "page_build",
          "public",
          "pull_request",
          "pull_request_review",
          "pull_request_review_comment",
          "push",
          "registry_package",
          "release",
          "repository",
          "repository_dispatch",
          "status",
          "watch",
          "workflow_dispatch",
          "workflow_run"
        ]
      },
      "pull_requests": [
        {
          "url": "https://api.github.com/repos/ducthangho/tra-luat/pulls/1249",
          "id": 5176379564,
          "number": 1249,
          "head": {
            "ref": "agent/wp1240-g1-claude",
            "sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          },
          "base": {
            "ref": "master",
            "sha": "3163f4d02a583787a9340c63a1f5eebd3780d970",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          }
        }
      ]
    },
    {
      "id": 127436213536,
      "name": "gate-cong-cu (ubuntu-latest, 4)",
      "node_id": "CR_kwDOTNeRjc8AAAAdq8pNIA",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "external_id": "af5b2e75-30a2-5312-9616-cbae898f547b",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213536",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213536",
      "details_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213536",
      "status": "completed",
      "conclusion": "success",
      "started_at": "2026-11-05T18:10:46Z",
      "completed_at": "2026-11-05T18:32:10Z",
      "output": {
        "title": null,
        "summary": null,
        "text": null,
        "annotations_count": 2,
        "annotations_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213536/annotations"
      },
      "check_suite": {
        "id": 114030831118
      },
      "app": {
        "id": 15368,
        "client_id": "Iv1.05c79e9ad1f6bdfa",
        "slug": "github-actions",
        "node_id": "MDM6QXBwMTUzNjg=",
        "owner": {
          "login": "github",
          "id": 9919,
          "node_id": "MDEyOk9yZ2FuaXphdGlvbjk5MTk=",
          "avatar_url": "https://avatars.githubusercontent.com/u/9919?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/github",
          "html_url": "https://github.com/github",
          "followers_url": "https://api.github.com/users/github/followers",
          "following_url": "https://api.github.com/users/github/following{/other_user}",
          "gists_url": "https://api.github.com/users/github/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/github/subscriptions",
          "organizations_url": "https://api.github.com/users/github/orgs",
          "repos_url": "https://api.github.com/users/github/repos",
          "events_url": "https://api.github.com/users/github/events{/privacy}",
          "received_events_url": "https://api.github.com/users/github/received_events",
          "type": "Organization",
          "user_view_type": "public",
          "site_admin": false
        },
        "name": "GitHub Actions",
        "description": "Automate your workflow from idea to production",
        "external_url": "https://help.github.com/en/actions",
        "html_url": "https://github.com/apps/github-actions",
        "created_at": "2018-07-30T09:30:17Z",
        "updated_at": "2026-06-18T16:17:48Z",
        "permissions": {
          "actions": "write",
          "administration": "read",
          "artifact_metadata": "write",
          "attestations": "write",
          "checks": "write",
          "code_quality": "write",
          "contents": "write",
          "copilot_requests": "write",
          "deployments": "write",
          "discussions": "write",
          "drives": "write",
          "issues": "write",
          "merge_queues": "write",
          "metadata": "read",
          "models": "read",
          "packages": "write",
          "pages": "write",
          "pull_requests": "write",
          "repository_hooks": "write",
          "repository_projects": "write",
          "security_events": "write",
          "statuses": "write",
          "vulnerability_alerts": "read"
        },
        "events": [
          "branch_protection_rule",
          "check_run",
          "check_suite",
          "create",
          "delete",
          "deployment",
          "deployment_status",
          "discussion",
          "discussion_comment",
          "fork",
          "gollum",
          "issues",
          "issue_comment",
          "label",
          "merge_group",
          "milestone",
          "page_build",
          "public",
          "pull_request",
          "pull_request_review",
          "pull_request_review_comment",
          "push",
          "registry_package",
          "release",
          "repository",
          "repository_dispatch",
          "status",
          "watch",
          "workflow_dispatch",
          "workflow_run"
        ]
      },
      "pull_requests": [
        {
          "url": "https://api.github.com/repos/ducthangho/tra-luat/pulls/1249",
          "id": 5176379564,
          "number": 1249,
          "head": {
            "ref": "agent/wp1240-g1-claude",
            "sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          },
          "base": {
            "ref": "master",
            "sha": "3163f4d02a583787a9340c63a1f5eebd3780d970",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          }
        }
      ]
    },
    {
      "id": 127436213499,
      "name": "gate-cong-cu (ubuntu-latest, 3)",
      "node_id": "CR_kwDOTNeRjc8AAAAdq8pM-w",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "external_id": "6cf68e6a-3f52-5f85-a82b-e46a5b486bd5",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213499",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213499",
      "details_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213499",
      "status": "completed",
      "conclusion": "success",
      "started_at": "2026-11-05T18:10:46Z",
      "completed_at": "2026-11-05T18:24:43Z",
      "output": {
        "title": null,
        "summary": null,
        "text": null,
        "annotations_count": 2,
        "annotations_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213499/annotations"
      },
      "check_suite": {
        "id": 114030831118
      },
      "app": {
        "id": 15368,
        "client_id": "Iv1.05c79e9ad1f6bdfa",
        "slug": "github-actions",
        "node_id": "MDM6QXBwMTUzNjg=",
        "owner": {
          "login": "github",
          "id": 9919,
          "node_id": "MDEyOk9yZ2FuaXphdGlvbjk5MTk=",
          "avatar_url": "https://avatars.githubusercontent.com/u/9919?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/github",
          "html_url": "https://github.com/github",
          "followers_url": "https://api.github.com/users/github/followers",
          "following_url": "https://api.github.com/users/github/following{/other_user}",
          "gists_url": "https://api.github.com/users/github/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/github/subscriptions",
          "organizations_url": "https://api.github.com/users/github/orgs",
          "repos_url": "https://api.github.com/users/github/repos",
          "events_url": "https://api.github.com/users/github/events{/privacy}",
          "received_events_url": "https://api.github.com/users/github/received_events",
          "type": "Organization",
          "user_view_type": "public",
          "site_admin": false
        },
        "name": "GitHub Actions",
        "description": "Automate your workflow from idea to production",
        "external_url": "https://help.github.com/en/actions",
        "html_url": "https://github.com/apps/github-actions",
        "created_at": "2018-07-30T09:30:17Z",
        "updated_at": "2026-06-18T16:17:48Z",
        "permissions": {
          "actions": "write",
          "administration": "read",
          "artifact_metadata": "write",
          "attestations": "write",
          "checks": "write",
          "code_quality": "write",
          "contents": "write",
          "copilot_requests": "write",
          "deployments": "write",
          "discussions": "write",
          "drives": "write",
          "issues": "write",
          "merge_queues": "write",
          "metadata": "read",
          "models": "read",
          "packages": "write",
          "pages": "write",
          "pull_requests": "write",
          "repository_hooks": "write",
          "repository_projects": "write",
          "security_events": "write",
          "statuses": "write",
          "vulnerability_alerts": "read"
        },
        "events": [
          "branch_protection_rule",
          "check_run",
          "check_suite",
          "create",
          "delete",
          "deployment",
          "deployment_status",
          "discussion",
          "discussion_comment",
          "fork",
          "gollum",
          "issues",
          "issue_comment",
          "label",
          "merge_group",
          "milestone",
          "page_build",
          "public",
          "pull_request",
          "pull_request_review",
          "pull_request_review_comment",
          "push",
          "registry_package",
          "release",
          "repository",
          "repository_dispatch",
          "status",
          "watch",
          "workflow_dispatch",
          "workflow_run"
        ]
      },
      "pull_requests": [
        {
          "url": "https://api.github.com/repos/ducthangho/tra-luat/pulls/1249",
          "id": 5176379564,
          "number": 1249,
          "head": {
            "ref": "agent/wp1240-g1-claude",
            "sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          },
          "base": {
            "ref": "master",
            "sha": "3163f4d02a583787a9340c63a1f5eebd3780d970",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          }
        }
      ]
    },
    {
      "id": 127436213490,
      "name": "gate-cong-cu (ubuntu-latest, 5)",
      "node_id": "CR_kwDOTNeRjc8AAAAdq8pM8g",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "external_id": "5a3a0e13-18b9-5df0-9903-fa36b9514730",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213490",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213490",
      "details_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213490",
      "status": "completed",
      "conclusion": "success",
      "started_at": "2026-11-05T18:10:46Z",
      "completed_at": "2026-11-05T18:31:07Z",
      "output": {
        "title": null,
        "summary": null,
        "text": null,
        "annotations_count": 2,
        "annotations_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213490/annotations"
      },
      "check_suite": {
        "id": 114030831118
      },
      "app": {
        "id": 15368,
        "client_id": "Iv1.05c79e9ad1f6bdfa",
        "slug": "github-actions",
        "node_id": "MDM6QXBwMTUzNjg=",
        "owner": {
          "login": "github",
          "id": 9919,
          "node_id": "MDEyOk9yZ2FuaXphdGlvbjk5MTk=",
          "avatar_url": "https://avatars.githubusercontent.com/u/9919?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/github",
          "html_url": "https://github.com/github",
          "followers_url": "https://api.github.com/users/github/followers",
          "following_url": "https://api.github.com/users/github/following{/other_user}",
          "gists_url": "https://api.github.com/users/github/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/github/subscriptions",
          "organizations_url": "https://api.github.com/users/github/orgs",
          "repos_url": "https://api.github.com/users/github/repos",
          "events_url": "https://api.github.com/users/github/events{/privacy}",
          "received_events_url": "https://api.github.com/users/github/received_events",
          "type": "Organization",
          "user_view_type": "public",
          "site_admin": false
        },
        "name": "GitHub Actions",
        "description": "Automate your workflow from idea to production",
        "external_url": "https://help.github.com/en/actions",
        "html_url": "https://github.com/apps/github-actions",
        "created_at": "2018-07-30T09:30:17Z",
        "updated_at": "2026-06-18T16:17:48Z",
        "permissions": {
          "actions": "write",
          "administration": "read",
          "artifact_metadata": "write",
          "attestations": "write",
          "checks": "write",
          "code_quality": "write",
          "contents": "write",
          "copilot_requests": "write",
          "deployments": "write",
          "discussions": "write",
          "drives": "write",
          "issues": "write",
          "merge_queues": "write",
          "metadata": "read",
          "models": "read",
          "packages": "write",
          "pages": "write",
          "pull_requests": "write",
          "repository_hooks": "write",
          "repository_projects": "write",
          "security_events": "write",
          "statuses": "write",
          "vulnerability_alerts": "read"
        },
        "events": [
          "branch_protection_rule",
          "check_run",
          "check_suite",
          "create",
          "delete",
          "deployment",
          "deployment_status",
          "discussion",
          "discussion_comment",
          "fork",
          "gollum",
          "issues",
          "issue_comment",
          "label",
          "merge_group",
          "milestone",
          "page_build",
          "public",
          "pull_request",
          "pull_request_review",
          "pull_request_review_comment",
          "push",
          "registry_package",
          "release",
          "repository",
          "repository_dispatch",
          "status",
          "watch",
          "workflow_dispatch",
          "workflow_run"
        ]
      },
      "pull_requests": [
        {
          "url": "https://api.github.com/repos/ducthangho/tra-luat/pulls/1249",
          "id": 5176379564,
          "number": 1249,
          "head": {
            "ref": "agent/wp1240-g1-claude",
            "sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          },
          "base": {
            "ref": "master",
            "sha": "3163f4d02a583787a9340c63a1f5eebd3780d970",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          }
        }
      ]
    },
    {
      "id": 127436213488,
      "name": "gate-nhanh-manh (ubuntu-latest, 2)",
      "node_id": "CR_kwDOTNeRjc8AAAAdq8pM8A",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "external_id": "c2a4ea6c-a5f5-523d-b6e9-316e265aab44",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213488",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213488",
      "details_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213488",
      "status": "completed",
      "conclusion": "success",
      "started_at": "2026-11-05T18:10:46Z",
      "completed_at": "2026-11-05T18:11:32Z",
      "output": {
        "title": null,
        "summary": null,
        "text": null,
        "annotations_count": 2,
        "annotations_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213488/annotations"
      },
      "check_suite": {
        "id": 114030831118
      },
      "app": {
        "id": 15368,
        "client_id": "Iv1.05c79e9ad1f6bdfa",
        "slug": "github-actions",
        "node_id": "MDM6QXBwMTUzNjg=",
        "owner": {
          "login": "github",
          "id": 9919,
          "node_id": "MDEyOk9yZ2FuaXphdGlvbjk5MTk=",
          "avatar_url": "https://avatars.githubusercontent.com/u/9919?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/github",
          "html_url": "https://github.com/github",
          "followers_url": "https://api.github.com/users/github/followers",
          "following_url": "https://api.github.com/users/github/following{/other_user}",
          "gists_url": "https://api.github.com/users/github/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/github/subscriptions",
          "organizations_url": "https://api.github.com/users/github/orgs",
          "repos_url": "https://api.github.com/users/github/repos",
          "events_url": "https://api.github.com/users/github/events{/privacy}",
          "received_events_url": "https://api.github.com/users/github/received_events",
          "type": "Organization",
          "user_view_type": "public",
          "site_admin": false
        },
        "name": "GitHub Actions",
        "description": "Automate your workflow from idea to production",
        "external_url": "https://help.github.com/en/actions",
        "html_url": "https://github.com/apps/github-actions",
        "created_at": "2018-07-30T09:30:17Z",
        "updated_at": "2026-06-18T16:17:48Z",
        "permissions": {
          "actions": "write",
          "administration": "read",
          "artifact_metadata": "write",
          "attestations": "write",
          "checks": "write",
          "code_quality": "write",
          "contents": "write",
          "copilot_requests": "write",
          "deployments": "write",
          "discussions": "write",
          "drives": "write",
          "issues": "write",
          "merge_queues": "write",
          "metadata": "read",
          "models": "read",
          "packages": "write",
          "pages": "write",
          "pull_requests": "write",
          "repository_hooks": "write",
          "repository_projects": "write",
          "security_events": "write",
          "statuses": "write",
          "vulnerability_alerts": "read"
        },
        "events": [
          "branch_protection_rule",
          "check_run",
          "check_suite",
          "create",
          "delete",
          "deployment",
          "deployment_status",
          "discussion",
          "discussion_comment",
          "fork",
          "gollum",
          "issues",
          "issue_comment",
          "label",
          "merge_group",
          "milestone",
          "page_build",
          "public",
          "pull_request",
          "pull_request_review",
          "pull_request_review_comment",
          "push",
          "registry_package",
          "release",
          "repository",
          "repository_dispatch",
          "status",
          "watch",
          "workflow_dispatch",
          "workflow_run"
        ]
      },
      "pull_requests": [
        {
          "url": "https://api.github.com/repos/ducthangho/tra-luat/pulls/1249",
          "id": 5176379564,
          "number": 1249,
          "head": {
            "ref": "agent/wp1240-g1-claude",
            "sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          },
          "base": {
            "ref": "master",
            "sha": "3163f4d02a583787a9340c63a1f5eebd3780d970",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          }
        }
      ]
    },
    {
      "id": 127436213461,
      "name": "gate-cong-cu (ubuntu-latest, 6)",
      "node_id": "CR_kwDOTNeRjc8AAAAdq8pM1Q",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "external_id": "09891cfe-77d4-5122-b31b-f97a5163efe2",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213461",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213461",
      "details_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213461",
      "status": "completed",
      "conclusion": "success",
      "started_at": "2026-11-05T18:10:46Z",
      "completed_at": "2026-11-05T18:23:54Z",
      "output": {
        "title": null,
        "summary": null,
        "text": null,
        "annotations_count": 2,
        "annotations_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213461/annotations"
      },
      "check_suite": {
        "id": 114030831118
      },
      "app": {
        "id": 15368,
        "client_id": "Iv1.05c79e9ad1f6bdfa",
        "slug": "github-actions",
        "node_id": "MDM6QXBwMTUzNjg=",
        "owner": {
          "login": "github",
          "id": 9919,
          "node_id": "MDEyOk9yZ2FuaXphdGlvbjk5MTk=",
          "avatar_url": "https://avatars.githubusercontent.com/u/9919?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/github",
          "html_url": "https://github.com/github",
          "followers_url": "https://api.github.com/users/github/followers",
          "following_url": "https://api.github.com/users/github/following{/other_user}",
          "gists_url": "https://api.github.com/users/github/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/github/subscriptions",
          "organizations_url": "https://api.github.com/users/github/orgs",
          "repos_url": "https://api.github.com/users/github/repos",
          "events_url": "https://api.github.com/users/github/events{/privacy}",
          "received_events_url": "https://api.github.com/users/github/received_events",
          "type": "Organization",
          "user_view_type": "public",
          "site_admin": false
        },
        "name": "GitHub Actions",
        "description": "Automate your workflow from idea to production",
        "external_url": "https://help.github.com/en/actions",
        "html_url": "https://github.com/apps/github-actions",
        "created_at": "2018-07-30T09:30:17Z",
        "updated_at": "2026-06-18T16:17:48Z",
        "permissions": {
          "actions": "write",
          "administration": "read",
          "artifact_metadata": "write",
          "attestations": "write",
          "checks": "write",
          "code_quality": "write",
          "contents": "write",
          "copilot_requests": "write",
          "deployments": "write",
          "discussions": "write",
          "drives": "write",
          "issues": "write",
          "merge_queues": "write",
          "metadata": "read",
          "models": "read",
          "packages": "write",
          "pages": "write",
          "pull_requests": "write",
          "repository_hooks": "write",
          "repository_projects": "write",
          "security_events": "write",
          "statuses": "write",
          "vulnerability_alerts": "read"
        },
        "events": [
          "branch_protection_rule",
          "check_run",
          "check_suite",
          "create",
          "delete",
          "deployment",
          "deployment_status",
          "discussion",
          "discussion_comment",
          "fork",
          "gollum",
          "issues",
          "issue_comment",
          "label",
          "merge_group",
          "milestone",
          "page_build",
          "public",
          "pull_request",
          "pull_request_review",
          "pull_request_review_comment",
          "push",
          "registry_package",
          "release",
          "repository",
          "repository_dispatch",
          "status",
          "watch",
          "workflow_dispatch",
          "workflow_run"
        ]
      },
      "pull_requests": [
        {
          "url": "https://api.github.com/repos/ducthangho/tra-luat/pulls/1249",
          "id": 5176379564,
          "number": 1249,
          "head": {
            "ref": "agent/wp1240-g1-claude",
            "sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          },
          "base": {
            "ref": "master",
            "sha": "3163f4d02a583787a9340c63a1f5eebd3780d970",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          }
        }
      ]
    },
    {
      "id": 127436213436,
      "name": "gate-cong-cu (ubuntu-latest, 2)",
      "node_id": "CR_kwDOTNeRjc8AAAAdq8pMvA",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "external_id": "4e469b1b-a8f1-5e54-9775-f0a39c77473f",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213436",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213436",
      "details_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213436",
      "status": "completed",
      "conclusion": "success",
      "started_at": "2026-11-05T18:10:46Z",
      "completed_at": "2026-11-05T18:27:08Z",
      "output": {
        "title": null,
        "summary": null,
        "text": null,
        "annotations_count": 2,
        "annotations_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213436/annotations"
      },
      "check_suite": {
        "id": 114030831118
      },
      "app": {
        "id": 15368,
        "client_id": "Iv1.05c79e9ad1f6bdfa",
        "slug": "github-actions",
        "node_id": "MDM6QXBwMTUzNjg=",
        "owner": {
          "login": "github",
          "id": 9919,
          "node_id": "MDEyOk9yZ2FuaXphdGlvbjk5MTk=",
          "avatar_url": "https://avatars.githubusercontent.com/u/9919?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/github",
          "html_url": "https://github.com/github",
          "followers_url": "https://api.github.com/users/github/followers",
          "following_url": "https://api.github.com/users/github/following{/other_user}",
          "gists_url": "https://api.github.com/users/github/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/github/subscriptions",
          "organizations_url": "https://api.github.com/users/github/orgs",
          "repos_url": "https://api.github.com/users/github/repos",
          "events_url": "https://api.github.com/users/github/events{/privacy}",
          "received_events_url": "https://api.github.com/users/github/received_events",
          "type": "Organization",
          "user_view_type": "public",
          "site_admin": false
        },
        "name": "GitHub Actions",
        "description": "Automate your workflow from idea to production",
        "external_url": "https://help.github.com/en/actions",
        "html_url": "https://github.com/apps/github-actions",
        "created_at": "2018-07-30T09:30:17Z",
        "updated_at": "2026-06-18T16:17:48Z",
        "permissions": {
          "actions": "write",
          "administration": "read",
          "artifact_metadata": "write",
          "attestations": "write",
          "checks": "write",
          "code_quality": "write",
          "contents": "write",
          "copilot_requests": "write",
          "deployments": "write",
          "discussions": "write",
          "drives": "write",
          "issues": "write",
          "merge_queues": "write",
          "metadata": "read",
          "models": "read",
          "packages": "write",
          "pages": "write",
          "pull_requests": "write",
          "repository_hooks": "write",
          "repository_projects": "write",
          "security_events": "write",
          "statuses": "write",
          "vulnerability_alerts": "read"
        },
        "events": [
          "branch_protection_rule",
          "check_run",
          "check_suite",
          "create",
          "delete",
          "deployment",
          "deployment_status",
          "discussion",
          "discussion_comment",
          "fork",
          "gollum",
          "issues",
          "issue_comment",
          "label",
          "merge_group",
          "milestone",
          "page_build",
          "public",
          "pull_request",
          "pull_request_review",
          "pull_request_review_comment",
          "push",
          "registry_package",
          "release",
          "repository",
          "repository_dispatch",
          "status",
          "watch",
          "workflow_dispatch",
          "workflow_run"
        ]
      },
      "pull_requests": [
        {
          "url": "https://api.github.com/repos/ducthangho/tra-luat/pulls/1249",
          "id": 5176379564,
          "number": 1249,
          "head": {
            "ref": "agent/wp1240-g1-claude",
            "sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          },
          "base": {
            "ref": "master",
            "sha": "3163f4d02a583787a9340c63a1f5eebd3780d970",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          }
        }
      ]
    },
    {
      "id": 127436213365,
      "name": "gate (ubuntu-latest)",
      "node_id": "CR_kwDOTNeRjc8AAAAdq8pMdQ",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "external_id": "cbcbeda0-5479-51d5-90df-c64268ced6b6",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213365",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213365",
      "details_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213365",
      "status": "completed",
      "conclusion": "success",
      "started_at": "2026-11-05T18:10:46Z",
      "completed_at": "2026-11-05T18:25:43Z",
      "output": {
        "title": null,
        "summary": null,
        "text": null,
        "annotations_count": 3,
        "annotations_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213365/annotations"
      },
      "check_suite": {
        "id": 114030831118
      },
      "app": {
        "id": 15368,
        "client_id": "Iv1.05c79e9ad1f6bdfa",
        "slug": "github-actions",
        "node_id": "MDM6QXBwMTUzNjg=",
        "owner": {
          "login": "github",
          "id": 9919,
          "node_id": "MDEyOk9yZ2FuaXphdGlvbjk5MTk=",
          "avatar_url": "https://avatars.githubusercontent.com/u/9919?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/github",
          "html_url": "https://github.com/github",
          "followers_url": "https://api.github.com/users/github/followers",
          "following_url": "https://api.github.com/users/github/following{/other_user}",
          "gists_url": "https://api.github.com/users/github/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/github/subscriptions",
          "organizations_url": "https://api.github.com/users/github/orgs",
          "repos_url": "https://api.github.com/users/github/repos",
          "events_url": "https://api.github.com/users/github/events{/privacy}",
          "received_events_url": "https://api.github.com/users/github/received_events",
          "type": "Organization",
          "user_view_type": "public",
          "site_admin": false
        },
        "name": "GitHub Actions",
        "description": "Automate your workflow from idea to production",
        "external_url": "https://help.github.com/en/actions",
        "html_url": "https://github.com/apps/github-actions",
        "created_at": "2018-07-30T09:30:17Z",
        "updated_at": "2026-06-18T16:17:48Z",
        "permissions": {
          "actions": "write",
          "administration": "read",
          "artifact_metadata": "write",
          "attestations": "write",
          "checks": "write",
          "code_quality": "write",
          "contents": "write",
          "copilot_requests": "write",
          "deployments": "write",
          "discussions": "write",
          "drives": "write",
          "issues": "write",
          "merge_queues": "write",
          "metadata": "read",
          "models": "read",
          "packages": "write",
          "pages": "write",
          "pull_requests": "write",
          "repository_hooks": "write",
          "repository_projects": "write",
          "security_events": "write",
          "statuses": "write",
          "vulnerability_alerts": "read"
        },
        "events": [
          "branch_protection_rule",
          "check_run",
          "check_suite",
          "create",
          "delete",
          "deployment",
          "deployment_status",
          "discussion",
          "discussion_comment",
          "fork",
          "gollum",
          "issues",
          "issue_comment",
          "label",
          "merge_group",
          "milestone",
          "page_build",
          "public",
          "pull_request",
          "pull_request_review",
          "pull_request_review_comment",
          "push",
          "registry_package",
          "release",
          "repository",
          "repository_dispatch",
          "status",
          "watch",
          "workflow_dispatch",
          "workflow_run"
        ]
      },
      "pull_requests": [
        {
          "url": "https://api.github.com/repos/ducthangho/tra-luat/pulls/1249",
          "id": 5176379564,
          "number": 1249,
          "head": {
            "ref": "agent/wp1240-g1-claude",
            "sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          },
          "base": {
            "ref": "master",
            "sha": "3163f4d02a583787a9340c63a1f5eebd3780d970",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          }
        }
      ]
    },
    {
      "id": 127436213333,
      "name": "gate-ops (ubuntu-latest)",
      "node_id": "CR_kwDOTNeRjc8AAAAdq8pMVQ",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "external_id": "82e425e8-6778-5096-a95a-283fdf95aed6",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213333",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213333",
      "details_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213333",
      "status": "completed",
      "conclusion": "success",
      "started_at": "2026-11-05T18:10:46Z",
      "completed_at": "2026-11-05T18:30:31Z",
      "output": {
        "title": null,
        "summary": null,
        "text": null,
        "annotations_count": 2,
        "annotations_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213333/annotations"
      },
      "check_suite": {
        "id": 114030831118
      },
      "app": {
        "id": 15368,
        "client_id": "Iv1.05c79e9ad1f6bdfa",
        "slug": "github-actions",
        "node_id": "MDM6QXBwMTUzNjg=",
        "owner": {
          "login": "github",
          "id": 9919,
          "node_id": "MDEyOk9yZ2FuaXphdGlvbjk5MTk=",
          "avatar_url": "https://avatars.githubusercontent.com/u/9919?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/github",
          "html_url": "https://github.com/github",
          "followers_url": "https://api.github.com/users/github/followers",
          "following_url": "https://api.github.com/users/github/following{/other_user}",
          "gists_url": "https://api.github.com/users/github/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/github/subscriptions",
          "organizations_url": "https://api.github.com/users/github/orgs",
          "repos_url": "https://api.github.com/users/github/repos",
          "events_url": "https://api.github.com/users/github/events{/privacy}",
          "received_events_url": "https://api.github.com/users/github/received_events",
          "type": "Organization",
          "user_view_type": "public",
          "site_admin": false
        },
        "name": "GitHub Actions",
        "description": "Automate your workflow from idea to production",
        "external_url": "https://help.github.com/en/actions",
        "html_url": "https://github.com/apps/github-actions",
        "created_at": "2018-07-30T09:30:17Z",
        "updated_at": "2026-06-18T16:17:48Z",
        "permissions": {
          "actions": "write",
          "administration": "read",
          "artifact_metadata": "write",
          "attestations": "write",
          "checks": "write",
          "code_quality": "write",
          "contents": "write",
          "copilot_requests": "write",
          "deployments": "write",
          "discussions": "write",
          "drives": "write",
          "issues": "write",
          "merge_queues": "write",
          "metadata": "read",
          "models": "read",
          "packages": "write",
          "pages": "write",
          "pull_requests": "write",
          "repository_hooks": "write",
          "repository_projects": "write",
          "security_events": "write",
          "statuses": "write",
          "vulnerability_alerts": "read"
        },
        "events": [
          "branch_protection_rule",
          "check_run",
          "check_suite",
          "create",
          "delete",
          "deployment",
          "deployment_status",
          "discussion",
          "discussion_comment",
          "fork",
          "gollum",
          "issues",
          "issue_comment",
          "label",
          "merge_group",
          "milestone",
          "page_build",
          "public",
          "pull_request",
          "pull_request_review",
          "pull_request_review_comment",
          "push",
          "registry_package",
          "release",
          "repository",
          "repository_dispatch",
          "status",
          "watch",
          "workflow_dispatch",
          "workflow_run"
        ]
      },
      "pull_requests": [
        {
          "url": "https://api.github.com/repos/ducthangho/tra-luat/pulls/1249",
          "id": 5176379564,
          "number": 1249,
          "head": {
            "ref": "agent/wp1240-g1-claude",
            "sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          },
          "base": {
            "ref": "master",
            "sha": "3163f4d02a583787a9340c63a1f5eebd3780d970",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          }
        }
      ]
    },
    {
      "id": 127436069597,
      "name": "thu-hoi",
      "node_id": "CR_kwDOTNeRjc8AAAAdq8ga3Q",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "external_id": "9ed9c4cb-0c9b-5d4a-a486-a34e02dd01b1",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436069597",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680093/job/127436069597",
      "details_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680093/job/127436069597",
      "status": "completed",
      "conclusion": "success",
      "started_at": "2026-11-05T18:10:31Z",
      "completed_at": "2026-11-05T18:10:47Z",
      "output": {
        "title": null,
        "summary": null,
        "text": null,
        "annotations_count": 2,
        "annotations_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436069597/annotations"
      },
      "check_suite": {
        "id": 114030830337
      },
      "app": {
        "id": 15368,
        "client_id": "Iv1.05c79e9ad1f6bdfa",
        "slug": "github-actions",
        "node_id": "MDM6QXBwMTUzNjg=",
        "owner": {
          "login": "github",
          "id": 9919,
          "node_id": "MDEyOk9yZ2FuaXphdGlvbjk5MTk=",
          "avatar_url": "https://avatars.githubusercontent.com/u/9919?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/github",
          "html_url": "https://github.com/github",
          "followers_url": "https://api.github.com/users/github/followers",
          "following_url": "https://api.github.com/users/github/following{/other_user}",
          "gists_url": "https://api.github.com/users/github/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/github/subscriptions",
          "organizations_url": "https://api.github.com/users/github/orgs",
          "repos_url": "https://api.github.com/users/github/repos",
          "events_url": "https://api.github.com/users/github/events{/privacy}",
          "received_events_url": "https://api.github.com/users/github/received_events",
          "type": "Organization",
          "user_view_type": "public",
          "site_admin": false
        },
        "name": "GitHub Actions",
        "description": "Automate your workflow from idea to production",
        "external_url": "https://help.github.com/en/actions",
        "html_url": "https://github.com/apps/github-actions",
        "created_at": "2018-07-30T09:30:17Z",
        "updated_at": "2026-06-18T16:17:48Z",
        "permissions": {
          "actions": "write",
          "administration": "read",
          "artifact_metadata": "write",
          "attestations": "write",
          "checks": "write",
          "code_quality": "write",
          "contents": "write",
          "copilot_requests": "write",
          "deployments": "write",
          "discussions": "write",
          "drives": "write",
          "issues": "write",
          "merge_queues": "write",
          "metadata": "read",
          "models": "read",
          "packages": "write",
          "pages": "write",
          "pull_requests": "write",
          "repository_hooks": "write",
          "repository_projects": "write",
          "security_events": "write",
          "statuses": "write",
          "vulnerability_alerts": "read"
        },
        "events": [
          "branch_protection_rule",
          "check_run",
          "check_suite",
          "create",
          "delete",
          "deployment",
          "deployment_status",
          "discussion",
          "discussion_comment",
          "fork",
          "gollum",
          "issues",
          "issue_comment",
          "label",
          "merge_group",
          "milestone",
          "page_build",
          "public",
          "pull_request",
          "pull_request_review",
          "pull_request_review_comment",
          "push",
          "registry_package",
          "release",
          "repository",
          "repository_dispatch",
          "status",
          "watch",
          "workflow_dispatch",
          "workflow_run"
        ]
      },
      "pull_requests": [
        {
          "url": "https://api.github.com/repos/ducthangho/tra-luat/pulls/1249",
          "id": 5176379564,
          "number": 1249,
          "head": {
            "ref": "agent/wp1240-g1-claude",
            "sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          },
          "base": {
            "ref": "master",
            "sha": "3163f4d02a583787a9340c63a1f5eebd3780d970",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          }
        }
      ]
    },
    {
      "id": 127436066699,
      "name": "chuan-bi",
      "node_id": "CR_kwDOTNeRjc8AAAAdq8gPiw",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "external_id": "3c35a130-25a1-5193-a8c0-02e2c72b4e42",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436066699",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436066699",
      "details_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436066699",
      "status": "completed",
      "conclusion": "success",
      "started_at": "2026-11-05T18:10:31Z",
      "completed_at": "2026-11-05T18:10:44Z",
      "output": {
        "title": null,
        "summary": null,
        "text": null,
        "annotations_count": 2,
        "annotations_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436066699/annotations"
      },
      "check_suite": {
        "id": 114030831118
      },
      "app": {
        "id": 15368,
        "client_id": "Iv1.05c79e9ad1f6bdfa",
        "slug": "github-actions",
        "node_id": "MDM6QXBwMTUzNjg=",
        "owner": {
          "login": "github",
          "id": 9919,
          "node_id": "MDEyOk9yZ2FuaXphdGlvbjk5MTk=",
          "avatar_url": "https://avatars.githubusercontent.com/u/9919?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/github",
          "html_url": "https://github.com/github",
          "followers_url": "https://api.github.com/users/github/followers",
          "following_url": "https://api.github.com/users/github/following{/other_user}",
          "gists_url": "https://api.github.com/users/github/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/github/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/github/subscriptions",
          "organizations_url": "https://api.github.com/users/github/orgs",
          "repos_url": "https://api.github.com/users/github/repos",
          "events_url": "https://api.github.com/users/github/events{/privacy}",
          "received_events_url": "https://api.github.com/users/github/received_events",
          "type": "Organization",
          "user_view_type": "public",
          "site_admin": false
        },
        "name": "GitHub Actions",
        "description": "Automate your workflow from idea to production",
        "external_url": "https://help.github.com/en/actions",
        "html_url": "https://github.com/apps/github-actions",
        "created_at": "2018-07-30T09:30:17Z",
        "updated_at": "2026-06-18T16:17:48Z",
        "permissions": {
          "actions": "write",
          "administration": "read",
          "artifact_metadata": "write",
          "attestations": "write",
          "checks": "write",
          "code_quality": "write",
          "contents": "write",
          "copilot_requests": "write",
          "deployments": "write",
          "discussions": "write",
          "drives": "write",
          "issues": "write",
          "merge_queues": "write",
          "metadata": "read",
          "models": "read",
          "packages": "write",
          "pages": "write",
          "pull_requests": "write",
          "repository_hooks": "write",
          "repository_projects": "write",
          "security_events": "write",
          "statuses": "write",
          "vulnerability_alerts": "read"
        },
        "events": [
          "branch_protection_rule",
          "check_run",
          "check_suite",
          "create",
          "delete",
          "deployment",
          "deployment_status",
          "discussion",
          "discussion_comment",
          "fork",
          "gollum",
          "issues",
          "issue_comment",
          "label",
          "merge_group",
          "milestone",
          "page_build",
          "public",
          "pull_request",
          "pull_request_review",
          "pull_request_review_comment",
          "push",
          "registry_package",
          "release",
          "repository",
          "repository_dispatch",
          "status",
          "watch",
          "workflow_dispatch",
          "workflow_run"
        ]
      },
      "pull_requests": [
        {
          "url": "https://api.github.com/repos/ducthangho/tra-luat/pulls/1249",
          "id": 5176379564,
          "number": 1249,
          "head": {
            "ref": "agent/wp1240-g1-claude",
            "sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          },
          "base": {
            "ref": "master",
            "sha": "3163f4d02a583787a9340c63a1f5eebd3780d970",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          }
        }
      ]
    }
  ]
}
~~~~ END cr.json

~~~~ BEGIN wr.json
{
  "total_count": 3,
  "workflow_runs": [
    {
      "id": 42092343146,
      "name": "đột biến đủ (hằng tuần)",
      "node_id": "WFR_kwLOTNeRjc8AAAAJzOYvag",
      "head_branch": "agent/wp1240-g1-claude",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "path": ".github/workflows/ci-dot-bien-du.yml",
      "display_title": "đột biến đủ (hằng tuần)",
      "run_number": 38,
      "event": "workflow_dispatch",
      "status": "completed",
      "conclusion": "success",
      "workflow_id": 367998662,
      "check_suite_id": 114059822218,
      "check_suite_node_id": "CS_kwDOTNeRjc8AAAAajn7Eig",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42092343146",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42092343146",
      "pull_requests": [
        {
          "url": "https://api.github.com/repos/ducthangho/tra-luat/pulls/1249",
          "id": 5176379564,
          "number": 1249,
          "head": {
            "ref": "agent/wp1240-g1-claude",
            "sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          },
          "base": {
            "ref": "master",
            "sha": "3163f4d02a583787a9340c63a1f5eebd3780d970",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          }
        }
      ],
      "created_at": "2026-11-05T19:16:44Z",
      "updated_at": "2026-11-05T19:46:29Z",
      "actor": {
        "login": "ducthangho",
        "id": 12748935,
        "node_id": "MDQ6VXNlcjEyNzQ4OTM1",
        "avatar_url": "https://avatars.githubusercontent.com/u/12748935?v=4",
        "gravatar_id": "",
        "url": "https://api.github.com/users/ducthangho",
        "html_url": "https://github.com/ducthangho",
        "followers_url": "https://api.github.com/users/ducthangho/followers",
        "following_url": "https://api.github.com/users/ducthangho/following{/other_user}",
        "gists_url": "https://api.github.com/users/ducthangho/gists{/gist_id}",
        "starred_url": "https://api.github.com/users/ducthangho/starred{/owner}{/repo}",
        "subscriptions_url": "https://api.github.com/users/ducthangho/subscriptions",
        "organizations_url": "https://api.github.com/users/ducthangho/orgs",
        "repos_url": "https://api.github.com/users/ducthangho/repos",
        "events_url": "https://api.github.com/users/ducthangho/events{/privacy}",
        "received_events_url": "https://api.github.com/users/ducthangho/received_events",
        "type": "User",
        "user_view_type": "public",
        "site_admin": false
      },
      "run_attempt": 1,
      "referenced_workflows": [

      ],
      "run_started_at": "2026-11-05T19:16:44Z",
      "triggering_actor": {
        "login": "ducthangho",
        "id": 12748935,
        "node_id": "MDQ6VXNlcjEyNzQ4OTM1",
        "avatar_url": "https://avatars.githubusercontent.com/u/12748935?v=4",
        "gravatar_id": "",
        "url": "https://api.github.com/users/ducthangho",
        "html_url": "https://github.com/ducthangho",
        "followers_url": "https://api.github.com/users/ducthangho/followers",
        "following_url": "https://api.github.com/users/ducthangho/following{/other_user}",
        "gists_url": "https://api.github.com/users/ducthangho/gists{/gist_id}",
        "starred_url": "https://api.github.com/users/ducthangho/starred{/owner}{/repo}",
        "subscriptions_url": "https://api.github.com/users/ducthangho/subscriptions",
        "organizations_url": "https://api.github.com/users/ducthangho/orgs",
        "repos_url": "https://api.github.com/users/ducthangho/repos",
        "events_url": "https://api.github.com/users/ducthangho/events{/privacy}",
        "received_events_url": "https://api.github.com/users/ducthangho/received_events",
        "type": "User",
        "user_view_type": "public",
        "site_admin": false
      },
      "jobs_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42092343146/jobs",
      "logs_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42092343146/logs",
      "check_suite_url": "https://api.github.com/repos/ducthangho/tra-luat/check-suites/114059822218",
      "artifacts_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42092343146/artifacts",
      "cancel_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42092343146/cancel",
      "rerun_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42092343146/rerun",
      "previous_attempt_url": null,
      "workflow_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/workflows/367998662",
      "head_commit": {
        "id": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
        "tree_id": "1b18da0468a9b04a2d0d567935157d17f3c5111f",
        "message": "wp1240 ASSURANCE-81-MODEL-EFFORT-TUY-CHON r1: model/effort reviewer thành trường ghi nếu đo được\n\n- ADR-0065 (Accepted, quyết định chủ kho #1240 issuecomment-6662892793, Q1/Q2 issuecomment-6663218706).\n- PROTOCOL §8.1: model/effort phục vụ là trường ghi nếu đo được; KHONG_DO_DUOC không làm assurance\n  CHUA_DAT, không chặn landed; bỏ câu \"cùng model, effort cao hơn\"; thu hẹp câu nhận dạng về\n  provider/surface/transport/session/sandbox. §8 mục 1: họ model theo identity provider. §20: dòng ADR-0065.\n- ops/land_evidence_nguon.py L7: chỉ sandbox_mode bắt buộc measured; model/effort vắng được, có mặt thì\n  measured hoặc not_measured, rác vẫn ĐỎ. MIEN_TRU_L7 giữ nguyên.\n- ops/land_evidence_nguon_test.py: c17 cập nhật, c23 mới (A4–A6), đột biến m1–m3 + 7 biên. 23/23, 116/116.\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_015Gtxra1nVwvZnd2Xy32KWw",
        "timestamp": "2026-11-05T17:46:20Z",
        "author": {
          "name": "Claude",
          "email": "noreply@anthropic.com"
        },
        "committer": {
          "name": "Claude",
          "email": "noreply@anthropic.com"
        }
      },
      "repository": {
        "id": 1289195917,
        "node_id": "R_kgDOTNeRjQ",
        "name": "tra-luat",
        "full_name": "ducthangho/tra-luat",
        "private": false,
        "owner": {
          "login": "ducthangho",
          "id": 12748935,
          "node_id": "MDQ6VXNlcjEyNzQ4OTM1",
          "avatar_url": "https://avatars.githubusercontent.com/u/12748935?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/ducthangho",
          "html_url": "https://github.com/ducthangho",
          "followers_url": "https://api.github.com/users/ducthangho/followers",
          "following_url": "https://api.github.com/users/ducthangho/following{/other_user}",
          "gists_url": "https://api.github.com/users/ducthangho/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/ducthangho/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/ducthangho/subscriptions",
          "organizations_url": "https://api.github.com/users/ducthangho/orgs",
          "repos_url": "https://api.github.com/users/ducthangho/repos",
          "events_url": "https://api.github.com/users/ducthangho/events{/privacy}",
          "received_events_url": "https://api.github.com/users/ducthangho/received_events",
          "type": "User",
          "user_view_type": "public",
          "site_admin": false
        },
        "html_url": "https://github.com/ducthangho/tra-luat",
        "description": null,
        "fork": false,
        "url": "https://api.github.com/repos/ducthangho/tra-luat",
        "forks_url": "https://api.github.com/repos/ducthangho/tra-luat/forks",
        "keys_url": "https://api.github.com/repos/ducthangho/tra-luat/keys{/key_id}",
        "collaborators_url": "https://api.github.com/repos/ducthangho/tra-luat/collaborators{/collaborator}",
        "teams_url": "https://api.github.com/repos/ducthangho/tra-luat/teams",
        "hooks_url": "https://api.github.com/repos/ducthangho/tra-luat/hooks",
        "issue_events_url": "https://api.github.com/repos/ducthangho/tra-luat/issues/events{/number}",
        "events_url": "https://api.github.com/repos/ducthangho/tra-luat/events",
        "assignees_url": "https://api.github.com/repos/ducthangho/tra-luat/assignees{/user}",
        "branches_url": "https://api.github.com/repos/ducthangho/tra-luat/branches{/branch}",
        "tags_url": "https://api.github.com/repos/ducthangho/tra-luat/tags",
        "blobs_url": "https://api.github.com/repos/ducthangho/tra-luat/git/blobs{/sha}",
        "git_tags_url": "https://api.github.com/repos/ducthangho/tra-luat/git/tags{/sha}",
        "git_refs_url": "https://api.github.com/repos/ducthangho/tra-luat/git/refs{/sha}",
        "trees_url": "https://api.github.com/repos/ducthangho/tra-luat/git/trees{/sha}",
        "statuses_url": "https://api.github.com/repos/ducthangho/tra-luat/statuses/{sha}",
        "languages_url": "https://api.github.com/repos/ducthangho/tra-luat/languages",
        "stargazers_url": "https://api.github.com/repos/ducthangho/tra-luat/stargazers",
        "contributors_url": "https://api.github.com/repos/ducthangho/tra-luat/contributors",
        "subscribers_url": "https://api.github.com/repos/ducthangho/tra-luat/subscribers",
        "subscription_url": "https://api.github.com/repos/ducthangho/tra-luat/subscription",
        "commits_url": "https://api.github.com/repos/ducthangho/tra-luat/commits{/sha}",
        "git_commits_url": "https://api.github.com/repos/ducthangho/tra-luat/git/commits{/sha}",
        "comments_url": "https://api.github.com/repos/ducthangho/tra-luat/comments{/number}",
        "issue_comment_url": "https://api.github.com/repos/ducthangho/tra-luat/issues/comments{/number}",
        "contents_url": "https://api.github.com/repos/ducthangho/tra-luat/contents/{+path}",
        "compare_url": "https://api.github.com/repos/ducthangho/tra-luat/compare/{base}...{head}",
        "merges_url": "https://api.github.com/repos/ducthangho/tra-luat/merges",
        "archive_url": "https://api.github.com/repos/ducthangho/tra-luat/{archive_format}{/ref}",
        "downloads_url": "https://api.github.com/repos/ducthangho/tra-luat/downloads",
        "issues_url": "https://api.github.com/repos/ducthangho/tra-luat/issues{/number}",
        "pulls_url": "https://api.github.com/repos/ducthangho/tra-luat/pulls{/number}",
        "milestones_url": "https://api.github.com/repos/ducthangho/tra-luat/milestones{/number}",
        "notifications_url": "https://api.github.com/repos/ducthangho/tra-luat/notifications{?since,all,participating}",
        "labels_url": "https://api.github.com/repos/ducthangho/tra-luat/labels{/name}",
        "releases_url": "https://api.github.com/repos/ducthangho/tra-luat/releases{/id}",
        "deployments_url": "https://api.github.com/repos/ducthangho/tra-luat/deployments"
      },
      "head_repository": {
        "id": 1289195917,
        "node_id": "R_kgDOTNeRjQ",
        "name": "tra-luat",
        "full_name": "ducthangho/tra-luat",
        "private": false,
        "owner": {
          "login": "ducthangho",
          "id": 12748935,
          "node_id": "MDQ6VXNlcjEyNzQ4OTM1",
          "avatar_url": "https://avatars.githubusercontent.com/u/12748935?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/ducthangho",
          "html_url": "https://github.com/ducthangho",
          "followers_url": "https://api.github.com/users/ducthangho/followers",
          "following_url": "https://api.github.com/users/ducthangho/following{/other_user}",
          "gists_url": "https://api.github.com/users/ducthangho/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/ducthangho/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/ducthangho/subscriptions",
          "organizations_url": "https://api.github.com/users/ducthangho/orgs",
          "repos_url": "https://api.github.com/users/ducthangho/repos",
          "events_url": "https://api.github.com/users/ducthangho/events{/privacy}",
          "received_events_url": "https://api.github.com/users/ducthangho/received_events",
          "type": "User",
          "user_view_type": "public",
          "site_admin": false
        },
        "html_url": "https://github.com/ducthangho/tra-luat",
        "description": null,
        "fork": false,
        "url": "https://api.github.com/repos/ducthangho/tra-luat",
        "forks_url": "https://api.github.com/repos/ducthangho/tra-luat/forks",
        "keys_url": "https://api.github.com/repos/ducthangho/tra-luat/keys{/key_id}",
        "collaborators_url": "https://api.github.com/repos/ducthangho/tra-luat/collaborators{/collaborator}",
        "teams_url": "https://api.github.com/repos/ducthangho/tra-luat/teams",
        "hooks_url": "https://api.github.com/repos/ducthangho/tra-luat/hooks",
        "issue_events_url": "https://api.github.com/repos/ducthangho/tra-luat/issues/events{/number}",
        "events_url": "https://api.github.com/repos/ducthangho/tra-luat/events",
        "assignees_url": "https://api.github.com/repos/ducthangho/tra-luat/assignees{/user}",
        "branches_url": "https://api.github.com/repos/ducthangho/tra-luat/branches{/branch}",
        "tags_url": "https://api.github.com/repos/ducthangho/tra-luat/tags",
        "blobs_url": "https://api.github.com/repos/ducthangho/tra-luat/git/blobs{/sha}",
        "git_tags_url": "https://api.github.com/repos/ducthangho/tra-luat/git/tags{/sha}",
        "git_refs_url": "https://api.github.com/repos/ducthangho/tra-luat/git/refs{/sha}",
        "trees_url": "https://api.github.com/repos/ducthangho/tra-luat/git/trees{/sha}",
        "statuses_url": "https://api.github.com/repos/ducthangho/tra-luat/statuses/{sha}",
        "languages_url": "https://api.github.com/repos/ducthangho/tra-luat/languages",
        "stargazers_url": "https://api.github.com/repos/ducthangho/tra-luat/stargazers",
        "contributors_url": "https://api.github.com/repos/ducthangho/tra-luat/contributors",
        "subscribers_url": "https://api.github.com/repos/ducthangho/tra-luat/subscribers",
        "subscription_url": "https://api.github.com/repos/ducthangho/tra-luat/subscription",
        "commits_url": "https://api.github.com/repos/ducthangho/tra-luat/commits{/sha}",
        "git_commits_url": "https://api.github.com/repos/ducthangho/tra-luat/git/commits{/sha}",
        "comments_url": "https://api.github.com/repos/ducthangho/tra-luat/comments{/number}",
        "issue_comment_url": "https://api.github.com/repos/ducthangho/tra-luat/issues/comments{/number}",
        "contents_url": "https://api.github.com/repos/ducthangho/tra-luat/contents/{+path}",
        "compare_url": "https://api.github.com/repos/ducthangho/tra-luat/compare/{base}...{head}",
        "merges_url": "https://api.github.com/repos/ducthangho/tra-luat/merges",
        "archive_url": "https://api.github.com/repos/ducthangho/tra-luat/{archive_format}{/ref}",
        "downloads_url": "https://api.github.com/repos/ducthangho/tra-luat/downloads",
        "issues_url": "https://api.github.com/repos/ducthangho/tra-luat/issues{/number}",
        "pulls_url": "https://api.github.com/repos/ducthangho/tra-luat/pulls{/number}",
        "milestones_url": "https://api.github.com/repos/ducthangho/tra-luat/milestones{/number}",
        "notifications_url": "https://api.github.com/repos/ducthangho/tra-luat/notifications{?since,all,participating}",
        "labels_url": "https://api.github.com/repos/ducthangho/tra-luat/labels{/name}",
        "releases_url": "https://api.github.com/repos/ducthangho/tra-luat/releases{/id}",
        "deployments_url": "https://api.github.com/repos/ducthangho/tra-luat/deployments"
      }
    },
    {
      "id": 42081680093,
      "name": "thu-hoi",
      "node_id": "WFR_kwLOTNeRjc8AAAAJzEN63Q",
      "head_branch": "agent/wp1240-g1-claude",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "path": ".github/workflows/ops-thu-hoi-admission.yml",
      "display_title": "wp1240 ASSURANCE-81-MODEL-EFFORT-TUY-CHON r1: model/effort reviewer thành trường ghi nếu đo được (ADR-0065)",
      "run_number": 2639,
      "event": "pull_request_target",
      "status": "completed",
      "conclusion": "success",
      "workflow_id": 354604665,
      "check_suite_id": 114030830337,
      "check_suite_node_id": "CS_kwDOTNeRjc8AAAAajMRjAQ",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42081680093",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680093",
      "pull_requests": [
        {
          "url": "https://api.github.com/repos/ducthangho/tra-luat/pulls/1249",
          "id": 5176379564,
          "number": 1249,
          "head": {
            "ref": "agent/wp1240-g1-claude",
            "sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          },
          "base": {
            "ref": "master",
            "sha": "3163f4d02a583787a9340c63a1f5eebd3780d970",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          }
        }
      ],
      "created_at": "2026-11-05T18:10:28Z",
      "updated_at": "2026-11-05T18:10:47Z",
      "actor": {
        "login": "ducthangho",
        "id": 12748935,
        "node_id": "MDQ6VXNlcjEyNzQ4OTM1",
        "avatar_url": "https://avatars.githubusercontent.com/u/12748935?v=4",
        "gravatar_id": "",
        "url": "https://api.github.com/users/ducthangho",
        "html_url": "https://github.com/ducthangho",
        "followers_url": "https://api.github.com/users/ducthangho/followers",
        "following_url": "https://api.github.com/users/ducthangho/following{/other_user}",
        "gists_url": "https://api.github.com/users/ducthangho/gists{/gist_id}",
        "starred_url": "https://api.github.com/users/ducthangho/starred{/owner}{/repo}",
        "subscriptions_url": "https://api.github.com/users/ducthangho/subscriptions",
        "organizations_url": "https://api.github.com/users/ducthangho/orgs",
        "repos_url": "https://api.github.com/users/ducthangho/repos",
        "events_url": "https://api.github.com/users/ducthangho/events{/privacy}",
        "received_events_url": "https://api.github.com/users/ducthangho/received_events",
        "type": "User",
        "user_view_type": "public",
        "site_admin": false
      },
      "run_attempt": 1,
      "referenced_workflows": [

      ],
      "run_started_at": "2026-11-05T18:10:28Z",
      "triggering_actor": {
        "login": "ducthangho",
        "id": 12748935,
        "node_id": "MDQ6VXNlcjEyNzQ4OTM1",
        "avatar_url": "https://avatars.githubusercontent.com/u/12748935?v=4",
        "gravatar_id": "",
        "url": "https://api.github.com/users/ducthangho",
        "html_url": "https://github.com/ducthangho",
        "followers_url": "https://api.github.com/users/ducthangho/followers",
        "following_url": "https://api.github.com/users/ducthangho/following{/other_user}",
        "gists_url": "https://api.github.com/users/ducthangho/gists{/gist_id}",
        "starred_url": "https://api.github.com/users/ducthangho/starred{/owner}{/repo}",
        "subscriptions_url": "https://api.github.com/users/ducthangho/subscriptions",
        "organizations_url": "https://api.github.com/users/ducthangho/orgs",
        "repos_url": "https://api.github.com/users/ducthangho/repos",
        "events_url": "https://api.github.com/users/ducthangho/events{/privacy}",
        "received_events_url": "https://api.github.com/users/ducthangho/received_events",
        "type": "User",
        "user_view_type": "public",
        "site_admin": false
      },
      "jobs_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42081680093/jobs",
      "logs_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42081680093/logs",
      "check_suite_url": "https://api.github.com/repos/ducthangho/tra-luat/check-suites/114030830337",
      "artifacts_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42081680093/artifacts",
      "cancel_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42081680093/cancel",
      "rerun_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42081680093/rerun",
      "previous_attempt_url": null,
      "workflow_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/workflows/354604665",
      "head_commit": {
        "id": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
        "tree_id": "1b18da0468a9b04a2d0d567935157d17f3c5111f",
        "message": "wp1240 ASSURANCE-81-MODEL-EFFORT-TUY-CHON r1: model/effort reviewer thành trường ghi nếu đo được\n\n- ADR-0065 (Accepted, quyết định chủ kho #1240 issuecomment-6662892793, Q1/Q2 issuecomment-6663218706).\n- PROTOCOL §8.1: model/effort phục vụ là trường ghi nếu đo được; KHONG_DO_DUOC không làm assurance\n  CHUA_DAT, không chặn landed; bỏ câu \"cùng model, effort cao hơn\"; thu hẹp câu nhận dạng về\n  provider/surface/transport/session/sandbox. §8 mục 1: họ model theo identity provider. §20: dòng ADR-0065.\n- ops/land_evidence_nguon.py L7: chỉ sandbox_mode bắt buộc measured; model/effort vắng được, có mặt thì\n  measured hoặc not_measured, rác vẫn ĐỎ. MIEN_TRU_L7 giữ nguyên.\n- ops/land_evidence_nguon_test.py: c17 cập nhật, c23 mới (A4–A6), đột biến m1–m3 + 7 biên. 23/23, 116/116.\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_015Gtxra1nVwvZnd2Xy32KWw",
        "timestamp": "2026-11-05T17:46:20Z",
        "author": {
          "name": "Claude",
          "email": "noreply@anthropic.com"
        },
        "committer": {
          "name": "Claude",
          "email": "noreply@anthropic.com"
        }
      },
      "repository": {
        "id": 1289195917,
        "node_id": "R_kgDOTNeRjQ",
        "name": "tra-luat",
        "full_name": "ducthangho/tra-luat",
        "private": false,
        "owner": {
          "login": "ducthangho",
          "id": 12748935,
          "node_id": "MDQ6VXNlcjEyNzQ4OTM1",
          "avatar_url": "https://avatars.githubusercontent.com/u/12748935?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/ducthangho",
          "html_url": "https://github.com/ducthangho",
          "followers_url": "https://api.github.com/users/ducthangho/followers",
          "following_url": "https://api.github.com/users/ducthangho/following{/other_user}",
          "gists_url": "https://api.github.com/users/ducthangho/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/ducthangho/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/ducthangho/subscriptions",
          "organizations_url": "https://api.github.com/users/ducthangho/orgs",
          "repos_url": "https://api.github.com/users/ducthangho/repos",
          "events_url": "https://api.github.com/users/ducthangho/events{/privacy}",
          "received_events_url": "https://api.github.com/users/ducthangho/received_events",
          "type": "User",
          "user_view_type": "public",
          "site_admin": false
        },
        "html_url": "https://github.com/ducthangho/tra-luat",
        "description": null,
        "fork": false,
        "url": "https://api.github.com/repos/ducthangho/tra-luat",
        "forks_url": "https://api.github.com/repos/ducthangho/tra-luat/forks",
        "keys_url": "https://api.github.com/repos/ducthangho/tra-luat/keys{/key_id}",
        "collaborators_url": "https://api.github.com/repos/ducthangho/tra-luat/collaborators{/collaborator}",
        "teams_url": "https://api.github.com/repos/ducthangho/tra-luat/teams",
        "hooks_url": "https://api.github.com/repos/ducthangho/tra-luat/hooks",
        "issue_events_url": "https://api.github.com/repos/ducthangho/tra-luat/issues/events{/number}",
        "events_url": "https://api.github.com/repos/ducthangho/tra-luat/events",
        "assignees_url": "https://api.github.com/repos/ducthangho/tra-luat/assignees{/user}",
        "branches_url": "https://api.github.com/repos/ducthangho/tra-luat/branches{/branch}",
        "tags_url": "https://api.github.com/repos/ducthangho/tra-luat/tags",
        "blobs_url": "https://api.github.com/repos/ducthangho/tra-luat/git/blobs{/sha}",
        "git_tags_url": "https://api.github.com/repos/ducthangho/tra-luat/git/tags{/sha}",
        "git_refs_url": "https://api.github.com/repos/ducthangho/tra-luat/git/refs{/sha}",
        "trees_url": "https://api.github.com/repos/ducthangho/tra-luat/git/trees{/sha}",
        "statuses_url": "https://api.github.com/repos/ducthangho/tra-luat/statuses/{sha}",
        "languages_url": "https://api.github.com/repos/ducthangho/tra-luat/languages",
        "stargazers_url": "https://api.github.com/repos/ducthangho/tra-luat/stargazers",
        "contributors_url": "https://api.github.com/repos/ducthangho/tra-luat/contributors",
        "subscribers_url": "https://api.github.com/repos/ducthangho/tra-luat/subscribers",
        "subscription_url": "https://api.github.com/repos/ducthangho/tra-luat/subscription",
        "commits_url": "https://api.github.com/repos/ducthangho/tra-luat/commits{/sha}",
        "git_commits_url": "https://api.github.com/repos/ducthangho/tra-luat/git/commits{/sha}",
        "comments_url": "https://api.github.com/repos/ducthangho/tra-luat/comments{/number}",
        "issue_comment_url": "https://api.github.com/repos/ducthangho/tra-luat/issues/comments{/number}",
        "contents_url": "https://api.github.com/repos/ducthangho/tra-luat/contents/{+path}",
        "compare_url": "https://api.github.com/repos/ducthangho/tra-luat/compare/{base}...{head}",
        "merges_url": "https://api.github.com/repos/ducthangho/tra-luat/merges",
        "archive_url": "https://api.github.com/repos/ducthangho/tra-luat/{archive_format}{/ref}",
        "downloads_url": "https://api.github.com/repos/ducthangho/tra-luat/downloads",
        "issues_url": "https://api.github.com/repos/ducthangho/tra-luat/issues{/number}",
        "pulls_url": "https://api.github.com/repos/ducthangho/tra-luat/pulls{/number}",
        "milestones_url": "https://api.github.com/repos/ducthangho/tra-luat/milestones{/number}",
        "notifications_url": "https://api.github.com/repos/ducthangho/tra-luat/notifications{?since,all,participating}",
        "labels_url": "https://api.github.com/repos/ducthangho/tra-luat/labels{/name}",
        "releases_url": "https://api.github.com/repos/ducthangho/tra-luat/releases{/id}",
        "deployments_url": "https://api.github.com/repos/ducthangho/tra-luat/deployments"
      },
      "head_repository": {
        "id": 1289195917,
        "node_id": "R_kgDOTNeRjQ",
        "name": "tra-luat",
        "full_name": "ducthangho/tra-luat",
        "private": false,
        "owner": {
          "login": "ducthangho",
          "id": 12748935,
          "node_id": "MDQ6VXNlcjEyNzQ4OTM1",
          "avatar_url": "https://avatars.githubusercontent.com/u/12748935?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/ducthangho",
          "html_url": "https://github.com/ducthangho",
          "followers_url": "https://api.github.com/users/ducthangho/followers",
          "following_url": "https://api.github.com/users/ducthangho/following{/other_user}",
          "gists_url": "https://api.github.com/users/ducthangho/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/ducthangho/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/ducthangho/subscriptions",
          "organizations_url": "https://api.github.com/users/ducthangho/orgs",
          "repos_url": "https://api.github.com/users/ducthangho/repos",
          "events_url": "https://api.github.com/users/ducthangho/events{/privacy}",
          "received_events_url": "https://api.github.com/users/ducthangho/received_events",
          "type": "User",
          "user_view_type": "public",
          "site_admin": false
        },
        "html_url": "https://github.com/ducthangho/tra-luat",
        "description": null,
        "fork": false,
        "url": "https://api.github.com/repos/ducthangho/tra-luat",
        "forks_url": "https://api.github.com/repos/ducthangho/tra-luat/forks",
        "keys_url": "https://api.github.com/repos/ducthangho/tra-luat/keys{/key_id}",
        "collaborators_url": "https://api.github.com/repos/ducthangho/tra-luat/collaborators{/collaborator}",
        "teams_url": "https://api.github.com/repos/ducthangho/tra-luat/teams",
        "hooks_url": "https://api.github.com/repos/ducthangho/tra-luat/hooks",
        "issue_events_url": "https://api.github.com/repos/ducthangho/tra-luat/issues/events{/number}",
        "events_url": "https://api.github.com/repos/ducthangho/tra-luat/events",
        "assignees_url": "https://api.github.com/repos/ducthangho/tra-luat/assignees{/user}",
        "branches_url": "https://api.github.com/repos/ducthangho/tra-luat/branches{/branch}",
        "tags_url": "https://api.github.com/repos/ducthangho/tra-luat/tags",
        "blobs_url": "https://api.github.com/repos/ducthangho/tra-luat/git/blobs{/sha}",
        "git_tags_url": "https://api.github.com/repos/ducthangho/tra-luat/git/tags{/sha}",
        "git_refs_url": "https://api.github.com/repos/ducthangho/tra-luat/git/refs{/sha}",
        "trees_url": "https://api.github.com/repos/ducthangho/tra-luat/git/trees{/sha}",
        "statuses_url": "https://api.github.com/repos/ducthangho/tra-luat/statuses/{sha}",
        "languages_url": "https://api.github.com/repos/ducthangho/tra-luat/languages",
        "stargazers_url": "https://api.github.com/repos/ducthangho/tra-luat/stargazers",
        "contributors_url": "https://api.github.com/repos/ducthangho/tra-luat/contributors",
        "subscribers_url": "https://api.github.com/repos/ducthangho/tra-luat/subscribers",
        "subscription_url": "https://api.github.com/repos/ducthangho/tra-luat/subscription",
        "commits_url": "https://api.github.com/repos/ducthangho/tra-luat/commits{/sha}",
        "git_commits_url": "https://api.github.com/repos/ducthangho/tra-luat/git/commits{/sha}",
        "comments_url": "https://api.github.com/repos/ducthangho/tra-luat/comments{/number}",
        "issue_comment_url": "https://api.github.com/repos/ducthangho/tra-luat/issues/comments{/number}",
        "contents_url": "https://api.github.com/repos/ducthangho/tra-luat/contents/{+path}",
        "compare_url": "https://api.github.com/repos/ducthangho/tra-luat/compare/{base}...{head}",
        "merges_url": "https://api.github.com/repos/ducthangho/tra-luat/merges",
        "archive_url": "https://api.github.com/repos/ducthangho/tra-luat/{archive_format}{/ref}",
        "downloads_url": "https://api.github.com/repos/ducthangho/tra-luat/downloads",
        "issues_url": "https://api.github.com/repos/ducthangho/tra-luat/issues{/number}",
        "pulls_url": "https://api.github.com/repos/ducthangho/tra-luat/pulls{/number}",
        "milestones_url": "https://api.github.com/repos/ducthangho/tra-luat/milestones{/number}",
        "notifications_url": "https://api.github.com/repos/ducthangho/tra-luat/notifications{?since,all,participating}",
        "labels_url": "https://api.github.com/repos/ducthangho/tra-luat/labels{/name}",
        "releases_url": "https://api.github.com/repos/ducthangho/tra-luat/releases{/id}",
        "deployments_url": "https://api.github.com/repos/ducthangho/tra-luat/deployments"
      }
    },
    {
      "id": 42081680387,
      "name": "gate",
      "node_id": "WFR_kwLOTNeRjc8AAAAJzEN8Aw",
      "head_branch": "agent/wp1240-g1-claude",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "path": ".github/workflows/ci.yml",
      "display_title": "wp1240 ASSURANCE-81-MODEL-EFFORT-TUY-CHON r1: model/effort reviewer thành trường ghi nếu đo được (ADR-0065)",
      "run_number": 4191,
      "event": "pull_request",
      "status": "completed",
      "conclusion": "success",
      "workflow_id": 309682866,
      "check_suite_id": 114030831118,
      "check_suite_node_id": "CS_kwDOTNeRjc8AAAAajMRmDg",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42081680387",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387",
      "pull_requests": [
        {
          "url": "https://api.github.com/repos/ducthangho/tra-luat/pulls/1249",
          "id": 5176379564,
          "number": 1249,
          "head": {
            "ref": "agent/wp1240-g1-claude",
            "sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          },
          "base": {
            "ref": "master",
            "sha": "3163f4d02a583787a9340c63a1f5eebd3780d970",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          }
        }
      ],
      "created_at": "2026-11-05T18:10:28Z",
      "updated_at": "2026-11-05T19:13:21Z",
      "actor": {
        "login": "ducthangho",
        "id": 12748935,
        "node_id": "MDQ6VXNlcjEyNzQ4OTM1",
        "avatar_url": "https://avatars.githubusercontent.com/u/12748935?v=4",
        "gravatar_id": "",
        "url": "https://api.github.com/users/ducthangho",
        "html_url": "https://github.com/ducthangho",
        "followers_url": "https://api.github.com/users/ducthangho/followers",
        "following_url": "https://api.github.com/users/ducthangho/following{/other_user}",
        "gists_url": "https://api.github.com/users/ducthangho/gists{/gist_id}",
        "starred_url": "https://api.github.com/users/ducthangho/starred{/owner}{/repo}",
        "subscriptions_url": "https://api.github.com/users/ducthangho/subscriptions",
        "organizations_url": "https://api.github.com/users/ducthangho/orgs",
        "repos_url": "https://api.github.com/users/ducthangho/repos",
        "events_url": "https://api.github.com/users/ducthangho/events{/privacy}",
        "received_events_url": "https://api.github.com/users/ducthangho/received_events",
        "type": "User",
        "user_view_type": "public",
        "site_admin": false
      },
      "run_attempt": 1,
      "referenced_workflows": [

      ],
      "run_started_at": "2026-11-05T18:10:28Z",
      "triggering_actor": {
        "login": "ducthangho",
        "id": 12748935,
        "node_id": "MDQ6VXNlcjEyNzQ4OTM1",
        "avatar_url": "https://avatars.githubusercontent.com/u/12748935?v=4",
        "gravatar_id": "",
        "url": "https://api.github.com/users/ducthangho",
        "html_url": "https://github.com/ducthangho",
        "followers_url": "https://api.github.com/users/ducthangho/followers",
        "following_url": "https://api.github.com/users/ducthangho/following{/other_user}",
        "gists_url": "https://api.github.com/users/ducthangho/gists{/gist_id}",
        "starred_url": "https://api.github.com/users/ducthangho/starred{/owner}{/repo}",
        "subscriptions_url": "https://api.github.com/users/ducthangho/subscriptions",
        "organizations_url": "https://api.github.com/users/ducthangho/orgs",
        "repos_url": "https://api.github.com/users/ducthangho/repos",
        "events_url": "https://api.github.com/users/ducthangho/events{/privacy}",
        "received_events_url": "https://api.github.com/users/ducthangho/received_events",
        "type": "User",
        "user_view_type": "public",
        "site_admin": false
      },
      "jobs_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42081680387/jobs",
      "logs_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42081680387/logs",
      "check_suite_url": "https://api.github.com/repos/ducthangho/tra-luat/check-suites/114030831118",
      "artifacts_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42081680387/artifacts",
      "cancel_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42081680387/cancel",
      "rerun_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42081680387/rerun",
      "previous_attempt_url": null,
      "workflow_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/workflows/309682866",
      "head_commit": {
        "id": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
        "tree_id": "1b18da0468a9b04a2d0d567935157d17f3c5111f",
        "message": "wp1240 ASSURANCE-81-MODEL-EFFORT-TUY-CHON r1: model/effort reviewer thành trường ghi nếu đo được\n\n- ADR-0065 (Accepted, quyết định chủ kho #1240 issuecomment-6662892793, Q1/Q2 issuecomment-6663218706).\n- PROTOCOL §8.1: model/effort phục vụ là trường ghi nếu đo được; KHONG_DO_DUOC không làm assurance\n  CHUA_DAT, không chặn landed; bỏ câu \"cùng model, effort cao hơn\"; thu hẹp câu nhận dạng về\n  provider/surface/transport/session/sandbox. §8 mục 1: họ model theo identity provider. §20: dòng ADR-0065.\n- ops/land_evidence_nguon.py L7: chỉ sandbox_mode bắt buộc measured; model/effort vắng được, có mặt thì\n  measured hoặc not_measured, rác vẫn ĐỎ. MIEN_TRU_L7 giữ nguyên.\n- ops/land_evidence_nguon_test.py: c17 cập nhật, c23 mới (A4–A6), đột biến m1–m3 + 7 biên. 23/23, 116/116.\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_015Gtxra1nVwvZnd2Xy32KWw",
        "timestamp": "2026-11-05T17:46:20Z",
        "author": {
          "name": "Claude",
          "email": "noreply@anthropic.com"
        },
        "committer": {
          "name": "Claude",
          "email": "noreply@anthropic.com"
        }
      },
      "repository": {
        "id": 1289195917,
        "node_id": "R_kgDOTNeRjQ",
        "name": "tra-luat",
        "full_name": "ducthangho/tra-luat",
        "private": false,
        "owner": {
          "login": "ducthangho",
          "id": 12748935,
          "node_id": "MDQ6VXNlcjEyNzQ4OTM1",
          "avatar_url": "https://avatars.githubusercontent.com/u/12748935?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/ducthangho",
          "html_url": "https://github.com/ducthangho",
          "followers_url": "https://api.github.com/users/ducthangho/followers",
          "following_url": "https://api.github.com/users/ducthangho/following{/other_user}",
          "gists_url": "https://api.github.com/users/ducthangho/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/ducthangho/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/ducthangho/subscriptions",
          "organizations_url": "https://api.github.com/users/ducthangho/orgs",
          "repos_url": "https://api.github.com/users/ducthangho/repos",
          "events_url": "https://api.github.com/users/ducthangho/events{/privacy}",
          "received_events_url": "https://api.github.com/users/ducthangho/received_events",
          "type": "User",
          "user_view_type": "public",
          "site_admin": false
        },
        "html_url": "https://github.com/ducthangho/tra-luat",
        "description": null,
        "fork": false,
        "url": "https://api.github.com/repos/ducthangho/tra-luat",
        "forks_url": "https://api.github.com/repos/ducthangho/tra-luat/forks",
        "keys_url": "https://api.github.com/repos/ducthangho/tra-luat/keys{/key_id}",
        "collaborators_url": "https://api.github.com/repos/ducthangho/tra-luat/collaborators{/collaborator}",
        "teams_url": "https://api.github.com/repos/ducthangho/tra-luat/teams",
        "hooks_url": "https://api.github.com/repos/ducthangho/tra-luat/hooks",
        "issue_events_url": "https://api.github.com/repos/ducthangho/tra-luat/issues/events{/number}",
        "events_url": "https://api.github.com/repos/ducthangho/tra-luat/events",
        "assignees_url": "https://api.github.com/repos/ducthangho/tra-luat/assignees{/user}",
        "branches_url": "https://api.github.com/repos/ducthangho/tra-luat/branches{/branch}",
        "tags_url": "https://api.github.com/repos/ducthangho/tra-luat/tags",
        "blobs_url": "https://api.github.com/repos/ducthangho/tra-luat/git/blobs{/sha}",
        "git_tags_url": "https://api.github.com/repos/ducthangho/tra-luat/git/tags{/sha}",
        "git_refs_url": "https://api.github.com/repos/ducthangho/tra-luat/git/refs{/sha}",
        "trees_url": "https://api.github.com/repos/ducthangho/tra-luat/git/trees{/sha}",
        "statuses_url": "https://api.github.com/repos/ducthangho/tra-luat/statuses/{sha}",
        "languages_url": "https://api.github.com/repos/ducthangho/tra-luat/languages",
        "stargazers_url": "https://api.github.com/repos/ducthangho/tra-luat/stargazers",
        "contributors_url": "https://api.github.com/repos/ducthangho/tra-luat/contributors",
        "subscribers_url": "https://api.github.com/repos/ducthangho/tra-luat/subscribers",
        "subscription_url": "https://api.github.com/repos/ducthangho/tra-luat/subscription",
        "commits_url": "https://api.github.com/repos/ducthangho/tra-luat/commits{/sha}",
        "git_commits_url": "https://api.github.com/repos/ducthangho/tra-luat/git/commits{/sha}",
        "comments_url": "https://api.github.com/repos/ducthangho/tra-luat/comments{/number}",
        "issue_comment_url": "https://api.github.com/repos/ducthangho/tra-luat/issues/comments{/number}",
        "contents_url": "https://api.github.com/repos/ducthangho/tra-luat/contents/{+path}",
        "compare_url": "https://api.github.com/repos/ducthangho/tra-luat/compare/{base}...{head}",
        "merges_url": "https://api.github.com/repos/ducthangho/tra-luat/merges",
        "archive_url": "https://api.github.com/repos/ducthangho/tra-luat/{archive_format}{/ref}",
        "downloads_url": "https://api.github.com/repos/ducthangho/tra-luat/downloads",
        "issues_url": "https://api.github.com/repos/ducthangho/tra-luat/issues{/number}",
        "pulls_url": "https://api.github.com/repos/ducthangho/tra-luat/pulls{/number}",
        "milestones_url": "https://api.github.com/repos/ducthangho/tra-luat/milestones{/number}",
        "notifications_url": "https://api.github.com/repos/ducthangho/tra-luat/notifications{?since,all,participating}",
        "labels_url": "https://api.github.com/repos/ducthangho/tra-luat/labels{/name}",
        "releases_url": "https://api.github.com/repos/ducthangho/tra-luat/releases{/id}",
        "deployments_url": "https://api.github.com/repos/ducthangho/tra-luat/deployments"
      },
      "head_repository": {
        "id": 1289195917,
        "node_id": "R_kgDOTNeRjQ",
        "name": "tra-luat",
        "full_name": "ducthangho/tra-luat",
        "private": false,
        "owner": {
          "login": "ducthangho",
          "id": 12748935,
          "node_id": "MDQ6VXNlcjEyNzQ4OTM1",
          "avatar_url": "https://avatars.githubusercontent.com/u/12748935?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/ducthangho",
          "html_url": "https://github.com/ducthangho",
          "followers_url": "https://api.github.com/users/ducthangho/followers",
          "following_url": "https://api.github.com/users/ducthangho/following{/other_user}",
          "gists_url": "https://api.github.com/users/ducthangho/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/ducthangho/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/ducthangho/subscriptions",
          "organizations_url": "https://api.github.com/users/ducthangho/orgs",
          "repos_url": "https://api.github.com/users/ducthangho/repos",
          "events_url": "https://api.github.com/users/ducthangho/events{/privacy}",
          "received_events_url": "https://api.github.com/users/ducthangho/received_events",
          "type": "User",
          "user_view_type": "public",
          "site_admin": false
        },
        "html_url": "https://github.com/ducthangho/tra-luat",
        "description": null,
        "fork": false,
        "url": "https://api.github.com/repos/ducthangho/tra-luat",
        "forks_url": "https://api.github.com/repos/ducthangho/tra-luat/forks",
        "keys_url": "https://api.github.com/repos/ducthangho/tra-luat/keys{/key_id}",
        "collaborators_url": "https://api.github.com/repos/ducthangho/tra-luat/collaborators{/collaborator}",
        "teams_url": "https://api.github.com/repos/ducthangho/tra-luat/teams",
        "hooks_url": "https://api.github.com/repos/ducthangho/tra-luat/hooks",
        "issue_events_url": "https://api.github.com/repos/ducthangho/tra-luat/issues/events{/number}",
        "events_url": "https://api.github.com/repos/ducthangho/tra-luat/events",
        "assignees_url": "https://api.github.com/repos/ducthangho/tra-luat/assignees{/user}",
        "branches_url": "https://api.github.com/repos/ducthangho/tra-luat/branches{/branch}",
        "tags_url": "https://api.github.com/repos/ducthangho/tra-luat/tags",
        "blobs_url": "https://api.github.com/repos/ducthangho/tra-luat/git/blobs{/sha}",
        "git_tags_url": "https://api.github.com/repos/ducthangho/tra-luat/git/tags{/sha}",
        "git_refs_url": "https://api.github.com/repos/ducthangho/tra-luat/git/refs{/sha}",
        "trees_url": "https://api.github.com/repos/ducthangho/tra-luat/git/trees{/sha}",
        "statuses_url": "https://api.github.com/repos/ducthangho/tra-luat/statuses/{sha}",
        "languages_url": "https://api.github.com/repos/ducthangho/tra-luat/languages",
        "stargazers_url": "https://api.github.com/repos/ducthangho/tra-luat/stargazers",
        "contributors_url": "https://api.github.com/repos/ducthangho/tra-luat/contributors",
        "subscribers_url": "https://api.github.com/repos/ducthangho/tra-luat/subscribers",
        "subscription_url": "https://api.github.com/repos/ducthangho/tra-luat/subscription",
        "commits_url": "https://api.github.com/repos/ducthangho/tra-luat/commits{/sha}",
        "git_commits_url": "https://api.github.com/repos/ducthangho/tra-luat/git/commits{/sha}",
        "comments_url": "https://api.github.com/repos/ducthangho/tra-luat/comments{/number}",
        "issue_comment_url": "https://api.github.com/repos/ducthangho/tra-luat/issues/comments{/number}",
        "contents_url": "https://api.github.com/repos/ducthangho/tra-luat/contents/{+path}",
        "compare_url": "https://api.github.com/repos/ducthangho/tra-luat/compare/{base}...{head}",
        "merges_url": "https://api.github.com/repos/ducthangho/tra-luat/merges",
        "archive_url": "https://api.github.com/repos/ducthangho/tra-luat/{archive_format}{/ref}",
        "downloads_url": "https://api.github.com/repos/ducthangho/tra-luat/downloads",
        "issues_url": "https://api.github.com/repos/ducthangho/tra-luat/issues{/number}",
        "pulls_url": "https://api.github.com/repos/ducthangho/tra-luat/pulls{/number}",
        "milestones_url": "https://api.github.com/repos/ducthangho/tra-luat/milestones{/number}",
        "notifications_url": "https://api.github.com/repos/ducthangho/tra-luat/notifications{?since,all,participating}",
        "labels_url": "https://api.github.com/repos/ducthangho/tra-luat/labels{/name}",
        "releases_url": "https://api.github.com/repos/ducthangho/tra-luat/releases{/id}",
        "deployments_url": "https://api.github.com/repos/ducthangho/tra-luat/deployments"
      }
    }
  ]
}
~~~~ END wr.json

~~~~ BEGIN wj.json
{
  "total_count": 23,
  "jobs": [
    {
      "id": 127436066699,
      "run_id": 42081680387,
      "workflow_name": "gate",
      "head_branch": "agent/wp1240-g1-claude",
      "run_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42081680387",
      "run_attempt": 1,
      "node_id": "CR_kwDOTNeRjc8AAAAdq8gPiw",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/actions/jobs/127436066699",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436066699",
      "status": "completed",
      "conclusion": "success",
      "created_at": "2026-11-05T18:10:29Z",
      "started_at": "2026-11-05T18:10:31Z",
      "completed_at": "2026-11-05T18:10:44Z",
      "name": "chuan-bi",
      "steps": [
        {
          "name": "Set up job",
          "status": "completed",
          "conclusion": "success",
          "number": 1,
          "started_at": "2026-11-05T18:10:32Z",
          "completed_at": "2026-11-05T18:10:32Z"
        },
        {
          "name": "Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 2,
          "started_at": "2026-11-05T18:10:32Z",
          "completed_at": "2026-11-05T18:10:41Z"
        },
        {
          "name": "phan loai diff (duong nhanh ho so)",
          "status": "completed",
          "conclusion": "success",
          "number": 3,
          "started_at": "2026-11-05T18:10:41Z",
          "completed_at": "2026-11-05T18:10:41Z"
        },
        {
          "name": "Post Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 6,
          "started_at": "2026-11-05T18:10:41Z",
          "completed_at": "2026-11-05T18:10:41Z"
        },
        {
          "name": "Complete job",
          "status": "completed",
          "conclusion": "success",
          "number": 7,
          "started_at": "2026-11-05T18:10:41Z",
          "completed_at": "2026-11-05T18:10:41Z"
        }
      ],
      "check_run_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436066699",
      "labels": [
        "ubuntu-latest"
      ],
      "runner_id": 1000039476,
      "runner_name": "GitHub Actions 1000039476",
      "runner_group_id": 0,
      "runner_group_name": "GitHub Actions"
    },
    {
      "id": 127436213333,
      "run_id": 42081680387,
      "workflow_name": "gate",
      "head_branch": "agent/wp1240-g1-claude",
      "run_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42081680387",
      "run_attempt": 1,
      "node_id": "CR_kwDOTNeRjc8AAAAdq8pMVQ",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/actions/jobs/127436213333",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213333",
      "status": "completed",
      "conclusion": "success",
      "created_at": "2026-11-05T18:10:44Z",
      "started_at": "2026-11-05T18:10:46Z",
      "completed_at": "2026-11-05T18:30:31Z",
      "name": "gate-ops (ubuntu-latest)",
      "steps": [
        {
          "name": "Set up job",
          "status": "completed",
          "conclusion": "success",
          "number": 1,
          "started_at": "2026-11-05T18:10:47Z",
          "completed_at": "2026-11-05T18:10:48Z"
        },
        {
          "name": "Force LF checkout (hash parity với manifest)",
          "status": "completed",
          "conclusion": "success",
          "number": 2,
          "started_at": "2026-11-05T18:10:48Z",
          "completed_at": "2026-11-05T18:10:48Z"
        },
        {
          "name": "Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 3,
          "started_at": "2026-11-05T18:10:48Z",
          "completed_at": "2026-11-05T18:10:56Z"
        },
        {
          "name": "Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 4,
          "started_at": "2026-11-05T18:10:56Z",
          "completed_at": "2026-11-05T18:10:56Z"
        },
        {
          "name": "cài PyYAML + jsonschema (cổng đăng lease + validator verdict cần)",
          "status": "completed",
          "conclusion": "success",
          "number": 5,
          "started_at": "2026-11-05T18:10:56Z",
          "completed_at": "2026-11-05T18:10:58Z"
        },
        {
          "name": "cài shellcheck cho G5 (cài xong đo lại)",
          "status": "completed",
          "conclusion": "success",
          "number": 6,
          "started_at": "2026-11-05T18:10:58Z",
          "completed_at": "2026-11-05T18:11:00Z"
        },
        {
          "name": "cài rg cho G5 (cài xong đo lại)",
          "status": "completed",
          "conclusion": "success",
          "number": 7,
          "started_at": "2026-11-05T18:11:00Z",
          "completed_at": "2026-11-05T18:11:04Z"
        },
        {
          "name": "DUONG_NHANH - liet ke buoc bo qua (job gate-ops)",
          "status": "completed",
          "conclusion": "skipped",
          "number": 8,
          "started_at": "2026-11-05T18:11:04Z",
          "completed_at": "2026-11-05T18:11:04Z"
        },
        {
          "name": "DUONG_NHANH - kiem re thay cho buoc bi bo (doctrine-scan, YAML, diff --check, lease check)",
          "status": "completed",
          "conclusion": "skipped",
          "number": 9,
          "started_at": "2026-11-05T18:11:04Z",
          "completed_at": "2026-11-05T18:11:04Z"
        },
        {
          "name": "ci-duong-nhanh selftest (phan loai diff + khoa cau truc if)",
          "status": "completed",
          "conclusion": "success",
          "number": 10,
          "started_at": "2026-11-05T18:11:04Z",
          "completed_at": "2026-11-05T18:19:01Z"
        },
        {
          "name": "bien-nhan v2 selftest",
          "status": "completed",
          "conclusion": "success",
          "number": 11,
          "started_at": "2026-11-05T18:19:01Z",
          "completed_at": "2026-11-05T18:23:23Z"
        },
        {
          "name": "lease-publish selftest (đo lại setup sau G5)",
          "status": "completed",
          "conclusion": "success",
          "number": 12,
          "started_at": "2026-11-05T18:23:23Z",
          "completed_at": "2026-11-05T18:28:47Z"
        },
        {
          "name": "don-nhanh selftest (chốt xoá nhánh)",
          "status": "completed",
          "conclusion": "success",
          "number": 13,
          "started_at": "2026-11-05T18:28:47Z",
          "completed_at": "2026-11-05T18:29:08Z"
        },
        {
          "name": "bo ca gate chay TRONG cgroup duoc uy quyen (Linux)",
          "status": "completed",
          "conclusion": "success",
          "number": 14,
          "started_at": "2026-11-05T18:29:08Z",
          "completed_at": "2026-11-05T18:30:28Z"
        },
        {
          "name": "gate lifecycle selftest (nen khong co cgroup)",
          "status": "completed",
          "conclusion": "skipped",
          "number": 15,
          "started_at": "2026-11-05T18:30:28Z",
          "completed_at": "2026-11-05T18:30:28Z"
        },
        {
          "name": "Post Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 29,
          "started_at": "2026-11-05T18:30:28Z",
          "completed_at": "2026-11-05T18:30:28Z"
        },
        {
          "name": "Post Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 30,
          "started_at": "2026-11-05T18:30:28Z",
          "completed_at": "2026-11-05T18:30:28Z"
        },
        {
          "name": "Complete job",
          "status": "completed",
          "conclusion": "success",
          "number": 31,
          "started_at": "2026-11-05T18:30:29Z",
          "completed_at": "2026-11-05T18:30:29Z"
        }
      ],
      "check_run_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213333",
      "labels": [
        "ubuntu-latest"
      ],
      "runner_id": 1000039493,
      "runner_name": "GitHub Actions 1000039493",
      "runner_group_id": 0,
      "runner_group_name": "GitHub Actions"
    },
    {
      "id": 127436213365,
      "run_id": 42081680387,
      "workflow_name": "gate",
      "head_branch": "agent/wp1240-g1-claude",
      "run_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42081680387",
      "run_attempt": 1,
      "node_id": "CR_kwDOTNeRjc8AAAAdq8pMdQ",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/actions/jobs/127436213365",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213365",
      "status": "completed",
      "conclusion": "success",
      "created_at": "2026-11-05T18:10:44Z",
      "started_at": "2026-11-05T18:10:46Z",
      "completed_at": "2026-11-05T18:25:43Z",
      "name": "gate (ubuntu-latest)",
      "steps": [
        {
          "name": "Set up job",
          "status": "completed",
          "conclusion": "success",
          "number": 1,
          "started_at": "2026-11-05T18:10:47Z",
          "completed_at": "2026-11-05T18:10:48Z"
        },
        {
          "name": "Force LF checkout (hash parity với manifest)",
          "status": "completed",
          "conclusion": "success",
          "number": 2,
          "started_at": "2026-11-05T18:10:48Z",
          "completed_at": "2026-11-05T18:10:48Z"
        },
        {
          "name": "Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 3,
          "started_at": "2026-11-05T18:10:48Z",
          "completed_at": "2026-11-05T18:10:57Z"
        },
        {
          "name": "Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 4,
          "started_at": "2026-11-05T18:10:57Z",
          "completed_at": "2026-11-05T18:10:58Z"
        },
        {
          "name": "cài PyYAML + jsonschema (cổng đăng lease + validator verdict cần)",
          "status": "completed",
          "conclusion": "success",
          "number": 5,
          "started_at": "2026-11-05T18:10:58Z",
          "completed_at": "2026-11-05T18:11:02Z"
        },
        {
          "name": "cài actionlint cho G5",
          "status": "completed",
          "conclusion": "success",
          "number": 6,
          "started_at": "2026-11-05T18:11:02Z",
          "completed_at": "2026-11-05T18:11:02Z"
        },
        {
          "name": "cài shellcheck cho G5 (cài xong đo lại)",
          "status": "completed",
          "conclusion": "success",
          "number": 7,
          "started_at": "2026-11-05T18:11:02Z",
          "completed_at": "2026-11-05T18:11:08Z"
        },
        {
          "name": "cài rg cho G5 (cài xong đo lại)",
          "status": "completed",
          "conclusion": "success",
          "number": 8,
          "started_at": "2026-11-05T18:11:08Z",
          "completed_at": "2026-11-05T18:11:14Z"
        },
        {
          "name": "G5 kiem ban ke cong cu + T1..T8 (packet",
          "status": "completed",
          "conclusion": "success",
          "number": 9,
          "started_at": "2026-11-05T18:11:14Z",
          "completed_at": "2026-11-05T18:17:01Z"
        },
        {
          "name": "cài Ruff 0.15.15 và in probe dương",
          "status": "completed",
          "conclusion": "success",
          "number": 10,
          "started_at": "2026-11-05T18:17:01Z",
          "completed_at": "2026-11-05T18:17:02Z"
        },
        {
          "name": "DUONG_NHANH - liet ke buoc bo qua (job gate)",
          "status": "completed",
          "conclusion": "skipped",
          "number": 11,
          "started_at": "2026-11-05T18:17:02Z",
          "completed_at": "2026-11-05T18:17:02Z"
        },
        {
          "name": "PR head contains required EOL base",
          "status": "completed",
          "conclusion": "success",
          "number": 12,
          "started_at": "2026-11-05T18:17:02Z",
          "completed_at": "2026-11-05T18:17:03Z"
        },
        {
          "name": "py_compile",
          "status": "completed",
          "conclusion": "success",
          "number": 13,
          "started_at": "2026-11-05T18:17:03Z",
          "completed_at": "2026-11-05T18:17:03Z"
        },
        {
          "name": "codex credential selftest (packet #300)",
          "status": "completed",
          "conclusion": "success",
          "number": 14,
          "started_at": "2026-11-05T18:17:03Z",
          "completed_at": "2026-11-05T18:17:07Z"
        },
        {
          "name": "idiom-ba-ten selftest",
          "status": "completed",
          "conclusion": "success",
          "number": 15,
          "started_at": "2026-11-05T18:17:07Z",
          "completed_at": "2026-11-05T18:17:20Z"
        },
        {
          "name": "eol-policy selftest",
          "status": "completed",
          "conclusion": "success",
          "number": 16,
          "started_at": "2026-11-05T18:17:20Z",
          "completed_at": "2026-11-05T18:18:29Z"
        },
        {
          "name": "pre-push selftest",
          "status": "completed",
          "conclusion": "success",
          "number": 17,
          "started_at": "2026-11-05T18:18:29Z",
          "completed_at": "2026-11-05T18:18:37Z"
        },
        {
          "name": "eol-policy survey",
          "status": "completed",
          "conclusion": "success",
          "number": 18,
          "started_at": "2026-11-05T18:18:37Z",
          "completed_at": "2026-11-05T18:18:39Z"
        },
        {
          "name": "bundled-fragment check (topology gói)",
          "status": "completed",
          "conclusion": "success",
          "number": 19,
          "started_at": "2026-11-05T18:18:39Z",
          "completed_at": "2026-11-05T18:18:57Z"
        },
        {
          "name": "gen_instructions selftest",
          "status": "completed",
          "conclusion": "success",
          "number": 20,
          "started_at": "2026-11-05T18:18:57Z",
          "completed_at": "2026-11-05T18:18:57Z"
        },
        {
          "name": "command-registry unit test (AG-T0-03)",
          "status": "completed",
          "conclusion": "success",
          "number": 21,
          "started_at": "2026-11-05T18:18:57Z",
          "completed_at": "2026-11-05T18:18:58Z"
        },
        {
          "name": "tl selftest (luot PR — khong sinh bang chung)",
          "status": "completed",
          "conclusion": "success",
          "number": 22,
          "started_at": "2026-11-05T18:18:58Z",
          "completed_at": "2026-11-05T18:23:42Z"
        },
        {
          "name": "tl selftest (co bang chung exact-identity)",
          "status": "completed",
          "conclusion": "skipped",
          "number": 23,
          "started_at": "2026-11-05T18:23:42Z",
          "completed_at": "2026-11-05T18:23:42Z"
        },
        {
          "name": "tai len gate-evidence",
          "status": "completed",
          "conclusion": "success",
          "number": 24,
          "started_at": "2026-11-05T18:23:42Z",
          "completed_at": "2026-11-05T18:23:42Z"
        },
        {
          "name": "workflow-audit strict",
          "status": "completed",
          "conclusion": "success",
          "number": 25,
          "started_at": "2026-11-05T18:23:42Z",
          "completed_at": "2026-11-05T18:23:43Z"
        },
        {
          "name": "golden-test",
          "status": "completed",
          "conclusion": "success",
          "number": 26,
          "started_at": "2026-11-05T18:23:43Z",
          "completed_at": "2026-11-05T18:24:11Z"
        },
        {
          "name": "doc-claims-check strict",
          "status": "completed",
          "conclusion": "success",
          "number": 27,
          "started_at": "2026-11-05T18:24:11Z",
          "completed_at": "2026-11-05T18:24:15Z"
        },
        {
          "name": "determinism-audit strict",
          "status": "completed",
          "conclusion": "success",
          "number": 28,
          "started_at": "2026-11-05T18:24:15Z",
          "completed_at": "2026-11-05T18:24:59Z"
        },
        {
          "name": "ci-phamvi guard (bang phu thuoc khop ma)",
          "status": "completed",
          "conclusion": "success",
          "number": 29,
          "started_at": "2026-11-05T18:24:59Z",
          "completed_at": "2026-11-05T18:25:01Z"
        },
        {
          "name": "ci-phamvi selftest (phan chung — cong co rang)",
          "status": "completed",
          "conclusion": "success",
          "number": 30,
          "started_at": "2026-11-05T18:25:01Z",
          "completed_at": "2026-11-05T18:25:23Z"
        },
        {
          "name": "release-check full",
          "status": "completed",
          "conclusion": "success",
          "number": 31,
          "started_at": "2026-11-05T18:25:23Z",
          "completed_at": "2026-11-05T18:25:27Z"
        },
        {
          "name": "release-verify strict (lane LAND — manifest committed)",
          "status": "completed",
          "conclusion": "skipped",
          "number": 32,
          "started_at": "2026-11-05T18:25:27Z",
          "completed_at": "2026-11-05T18:25:27Z"
        },
        {
          "name": "release-verify strict (lane WORKER — manifest TẠM ngoài repo)",
          "status": "completed",
          "conclusion": "success",
          "number": 33,
          "started_at": "2026-11-05T18:25:27Z",
          "completed_at": "2026-11-05T18:25:31Z"
        },
        {
          "name": "release-bundle x2 cùng SHA-256",
          "status": "completed",
          "conclusion": "success",
          "number": 34,
          "started_at": "2026-11-05T18:25:31Z",
          "completed_at": "2026-11-05T18:25:38Z"
        },
        {
          "name": "tl_boot smoke",
          "status": "completed",
          "conclusion": "success",
          "number": 35,
          "started_at": "2026-11-05T18:25:38Z",
          "completed_at": "2026-11-05T18:25:39Z"
        },
        {
          "name": "Post Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 69,
          "started_at": "2026-11-05T18:25:39Z",
          "completed_at": "2026-11-05T18:25:39Z"
        },
        {
          "name": "Post Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 70,
          "started_at": "2026-11-05T18:25:39Z",
          "completed_at": "2026-11-05T18:25:40Z"
        },
        {
          "name": "Complete job",
          "status": "completed",
          "conclusion": "success",
          "number": 71,
          "started_at": "2026-11-05T18:25:40Z",
          "completed_at": "2026-11-05T18:25:40Z"
        }
      ],
      "check_run_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213365",
      "labels": [
        "ubuntu-latest"
      ],
      "runner_id": 1000039492,
      "runner_name": "GitHub Actions 1000039492",
      "runner_group_id": 0,
      "runner_group_name": "GitHub Actions"
    },
    {
      "id": 127436213436,
      "run_id": 42081680387,
      "workflow_name": "gate",
      "head_branch": "agent/wp1240-g1-claude",
      "run_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42081680387",
      "run_attempt": 1,
      "node_id": "CR_kwDOTNeRjc8AAAAdq8pMvA",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/actions/jobs/127436213436",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213436",
      "status": "completed",
      "conclusion": "success",
      "created_at": "2026-11-05T18:10:44Z",
      "started_at": "2026-11-05T18:10:46Z",
      "completed_at": "2026-11-05T18:27:08Z",
      "name": "gate-cong-cu (ubuntu-latest, 2)",
      "steps": [
        {
          "name": "Set up job",
          "status": "completed",
          "conclusion": "success",
          "number": 1,
          "started_at": "2026-11-05T18:10:47Z",
          "completed_at": "2026-11-05T18:10:48Z"
        },
        {
          "name": "Force LF checkout (hash parity với manifest)",
          "status": "completed",
          "conclusion": "success",
          "number": 2,
          "started_at": "2026-11-05T18:10:48Z",
          "completed_at": "2026-11-05T18:10:48Z"
        },
        {
          "name": "Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 3,
          "started_at": "2026-11-05T18:10:48Z",
          "completed_at": "2026-11-05T18:10:56Z"
        },
        {
          "name": "Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 4,
          "started_at": "2026-11-05T18:10:56Z",
          "completed_at": "2026-11-05T18:10:56Z"
        },
        {
          "name": "cài PyYAML + jsonschema (cổng đăng lease + validator verdict cần)",
          "status": "completed",
          "conclusion": "success",
          "number": 5,
          "started_at": "2026-11-05T18:10:56Z",
          "completed_at": "2026-11-05T18:10:58Z"
        },
        {
          "name": "cài actionlint cho G5",
          "status": "completed",
          "conclusion": "success",
          "number": 6,
          "started_at": "2026-11-05T18:10:58Z",
          "completed_at": "2026-11-05T18:10:59Z"
        },
        {
          "name": "cài shellcheck cho G5 (cài xong đo lại)",
          "status": "completed",
          "conclusion": "success",
          "number": 7,
          "started_at": "2026-11-05T18:10:59Z",
          "completed_at": "2026-11-05T18:11:01Z"
        },
        {
          "name": "cài rg cho G5 (cài xong đo lại)",
          "status": "completed",
          "conclusion": "success",
          "number": 8,
          "started_at": "2026-11-05T18:11:01Z",
          "completed_at": "2026-11-05T18:11:05Z"
        },
        {
          "name": "G5 manh ban kinh dot bien (#668)",
          "status": "completed",
          "conclusion": "success",
          "number": 9,
          "started_at": "2026-11-05T18:11:05Z",
          "completed_at": "2026-11-05T18:27:04Z"
        },
        {
          "name": "Run actions/upload-artifact@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 10,
          "started_at": "2026-11-05T18:27:04Z",
          "completed_at": "2026-11-05T18:27:06Z"
        },
        {
          "name": "Post Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 19,
          "started_at": "2026-11-05T18:27:06Z",
          "completed_at": "2026-11-05T18:27:06Z"
        },
        {
          "name": "Post Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 20,
          "started_at": "2026-11-05T18:27:06Z",
          "completed_at": "2026-11-05T18:27:06Z"
        },
        {
          "name": "Complete job",
          "status": "completed",
          "conclusion": "success",
          "number": 21,
          "started_at": "2026-11-05T18:27:06Z",
          "completed_at": "2026-11-05T18:27:06Z"
        }
      ],
      "check_run_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213436",
      "labels": [
        "ubuntu-latest"
      ],
      "runner_id": 1000039483,
      "runner_name": "GitHub Actions 1000039483",
      "runner_group_id": 0,
      "runner_group_name": "GitHub Actions"
    },
    {
      "id": 127436213461,
      "run_id": 42081680387,
      "workflow_name": "gate",
      "head_branch": "agent/wp1240-g1-claude",
      "run_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42081680387",
      "run_attempt": 1,
      "node_id": "CR_kwDOTNeRjc8AAAAdq8pM1Q",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/actions/jobs/127436213461",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213461",
      "status": "completed",
      "conclusion": "success",
      "created_at": "2026-11-05T18:10:44Z",
      "started_at": "2026-11-05T18:10:46Z",
      "completed_at": "2026-11-05T18:23:54Z",
      "name": "gate-cong-cu (ubuntu-latest, 6)",
      "steps": [
        {
          "name": "Set up job",
          "status": "completed",
          "conclusion": "success",
          "number": 1,
          "started_at": "2026-11-05T18:10:47Z",
          "completed_at": "2026-11-05T18:10:47Z"
        },
        {
          "name": "Force LF checkout (hash parity với manifest)",
          "status": "completed",
          "conclusion": "success",
          "number": 2,
          "started_at": "2026-11-05T18:10:47Z",
          "completed_at": "2026-11-05T18:10:48Z"
        },
        {
          "name": "Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 3,
          "started_at": "2026-11-05T18:10:48Z",
          "completed_at": "2026-11-05T18:10:54Z"
        },
        {
          "name": "Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 4,
          "started_at": "2026-11-05T18:10:54Z",
          "completed_at": "2026-11-05T18:10:54Z"
        },
        {
          "name": "cài PyYAML + jsonschema (cổng đăng lease + validator verdict cần)",
          "status": "completed",
          "conclusion": "success",
          "number": 5,
          "started_at": "2026-11-05T18:10:54Z",
          "completed_at": "2026-11-05T18:10:57Z"
        },
        {
          "name": "cài actionlint cho G5",
          "status": "completed",
          "conclusion": "success",
          "number": 6,
          "started_at": "2026-11-05T18:10:57Z",
          "completed_at": "2026-11-05T18:10:57Z"
        },
        {
          "name": "cài shellcheck cho G5 (cài xong đo lại)",
          "status": "completed",
          "conclusion": "success",
          "number": 7,
          "started_at": "2026-11-05T18:10:57Z",
          "completed_at": "2026-11-05T18:10:59Z"
        },
        {
          "name": "cài rg cho G5 (cài xong đo lại)",
          "status": "completed",
          "conclusion": "success",
          "number": 8,
          "started_at": "2026-11-05T18:10:59Z",
          "completed_at": "2026-11-05T18:11:03Z"
        },
        {
          "name": "G5 manh ban kinh dot bien (#668)",
          "status": "completed",
          "conclusion": "success",
          "number": 9,
          "started_at": "2026-11-05T18:11:03Z",
          "completed_at": "2026-11-05T18:23:51Z"
        },
        {
          "name": "Run actions/upload-artifact@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 10,
          "started_at": "2026-11-05T18:23:51Z",
          "completed_at": "2026-11-05T18:23:52Z"
        },
        {
          "name": "Post Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 19,
          "started_at": "2026-11-05T18:23:52Z",
          "completed_at": "2026-11-05T18:23:52Z"
        },
        {
          "name": "Post Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 20,
          "started_at": "2026-11-05T18:23:52Z",
          "completed_at": "2026-11-05T18:23:52Z"
        },
        {
          "name": "Complete job",
          "status": "completed",
          "conclusion": "success",
          "number": 21,
          "started_at": "2026-11-05T18:23:52Z",
          "completed_at": "2026-11-05T18:23:52Z"
        }
      ],
      "check_run_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213461",
      "labels": [
        "ubuntu-latest"
      ],
      "runner_id": 1000039490,
      "runner_name": "GitHub Actions 1000039490",
      "runner_group_id": 0,
      "runner_group_name": "GitHub Actions"
    },
    {
      "id": 127436213488,
      "run_id": 42081680387,
      "workflow_name": "gate",
      "head_branch": "agent/wp1240-g1-claude",
      "run_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42081680387",
      "run_attempt": 1,
      "node_id": "CR_kwDOTNeRjc8AAAAdq8pM8A",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/actions/jobs/127436213488",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213488",
      "status": "completed",
      "conclusion": "success",
      "created_at": "2026-11-05T18:10:44Z",
      "started_at": "2026-11-05T18:10:46Z",
      "completed_at": "2026-11-05T18:11:32Z",
      "name": "gate-nhanh-manh (ubuntu-latest, 2)",
      "steps": [
        {
          "name": "Set up job",
          "status": "completed",
          "conclusion": "success",
          "number": 1,
          "started_at": "2026-11-05T18:10:47Z",
          "completed_at": "2026-11-05T18:10:48Z"
        },
        {
          "name": "Force LF checkout (hash parity với manifest)",
          "status": "completed",
          "conclusion": "success",
          "number": 2,
          "started_at": "2026-11-05T18:10:48Z",
          "completed_at": "2026-11-05T18:10:48Z"
        },
        {
          "name": "Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 3,
          "started_at": "2026-11-05T18:10:48Z",
          "completed_at": "2026-11-05T18:10:55Z"
        },
        {
          "name": "Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 4,
          "started_at": "2026-11-05T18:10:55Z",
          "completed_at": "2026-11-05T18:10:55Z"
        },
        {
          "name": "DUONG_NHANH - liet ke buoc bo qua (job gate-nhanh-manh)",
          "status": "completed",
          "conclusion": "skipped",
          "number": 5,
          "started_at": "2026-11-05T18:10:55Z",
          "completed_at": "2026-11-05T18:10:55Z"
        },
        {
          "name": "chạy mảnh nhanh_don_duoc (targeted_mutant_gate)",
          "status": "completed",
          "conclusion": "success",
          "number": 6,
          "started_at": "2026-11-05T18:10:55Z",
          "completed_at": "2026-11-05T18:11:28Z"
        },
        {
          "name": "Run actions/upload-artifact@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 7,
          "started_at": "2026-11-05T18:11:28Z",
          "completed_at": "2026-11-05T18:11:29Z"
        },
        {
          "name": "Post Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 13,
          "started_at": "2026-11-05T18:11:29Z",
          "completed_at": "2026-11-05T18:11:29Z"
        },
        {
          "name": "Post Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 14,
          "started_at": "2026-11-05T18:11:29Z",
          "completed_at": "2026-11-05T18:11:29Z"
        },
        {
          "name": "Complete job",
          "status": "completed",
          "conclusion": "success",
          "number": 15,
          "started_at": "2026-11-05T18:11:29Z",
          "completed_at": "2026-11-05T18:11:29Z"
        }
      ],
      "check_run_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213488",
      "labels": [
        "ubuntu-latest"
      ],
      "runner_id": 1000039482,
      "runner_name": "GitHub Actions 1000039482",
      "runner_group_id": 0,
      "runner_group_name": "GitHub Actions"
    },
    {
      "id": 127436213490,
      "run_id": 42081680387,
      "workflow_name": "gate",
      "head_branch": "agent/wp1240-g1-claude",
      "run_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42081680387",
      "run_attempt": 1,
      "node_id": "CR_kwDOTNeRjc8AAAAdq8pM8g",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/actions/jobs/127436213490",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213490",
      "status": "completed",
      "conclusion": "success",
      "created_at": "2026-11-05T18:10:44Z",
      "started_at": "2026-11-05T18:10:46Z",
      "completed_at": "2026-11-05T18:31:07Z",
      "name": "gate-cong-cu (ubuntu-latest, 5)",
      "steps": [
        {
          "name": "Set up job",
          "status": "completed",
          "conclusion": "success",
          "number": 1,
          "started_at": "2026-11-05T18:10:47Z",
          "completed_at": "2026-11-05T18:10:48Z"
        },
        {
          "name": "Force LF checkout (hash parity với manifest)",
          "status": "completed",
          "conclusion": "success",
          "number": 2,
          "started_at": "2026-11-05T18:10:48Z",
          "completed_at": "2026-11-05T18:10:48Z"
        },
        {
          "name": "Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 3,
          "started_at": "2026-11-05T18:10:48Z",
          "completed_at": "2026-11-05T18:10:56Z"
        },
        {
          "name": "Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 4,
          "started_at": "2026-11-05T18:10:56Z",
          "completed_at": "2026-11-05T18:10:56Z"
        },
        {
          "name": "cài PyYAML + jsonschema (cổng đăng lease + validator verdict cần)",
          "status": "completed",
          "conclusion": "success",
          "number": 5,
          "started_at": "2026-11-05T18:10:56Z",
          "completed_at": "2026-11-05T18:10:58Z"
        },
        {
          "name": "cài actionlint cho G5",
          "status": "completed",
          "conclusion": "success",
          "number": 6,
          "started_at": "2026-11-05T18:10:58Z",
          "completed_at": "2026-11-05T18:10:59Z"
        },
        {
          "name": "cài shellcheck cho G5 (cài xong đo lại)",
          "status": "completed",
          "conclusion": "success",
          "number": 7,
          "started_at": "2026-11-05T18:10:59Z",
          "completed_at": "2026-11-05T18:11:00Z"
        },
        {
          "name": "cài rg cho G5 (cài xong đo lại)",
          "status": "completed",
          "conclusion": "success",
          "number": 8,
          "started_at": "2026-11-05T18:11:00Z",
          "completed_at": "2026-11-05T18:11:04Z"
        },
        {
          "name": "G5 manh ban kinh dot bien (#668)",
          "status": "completed",
          "conclusion": "success",
          "number": 9,
          "started_at": "2026-11-05T18:11:04Z",
          "completed_at": "2026-11-05T18:31:04Z"
        },
        {
          "name": "Run actions/upload-artifact@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 10,
          "started_at": "2026-11-05T18:31:04Z",
          "completed_at": "2026-11-05T18:31:05Z"
        },
        {
          "name": "Post Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 19,
          "started_at": "2026-11-05T18:31:05Z",
          "completed_at": "2026-11-05T18:31:05Z"
        },
        {
          "name": "Post Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 20,
          "started_at": "2026-11-05T18:31:05Z",
          "completed_at": "2026-11-05T18:31:05Z"
        },
        {
          "name": "Complete job",
          "status": "completed",
          "conclusion": "success",
          "number": 21,
          "started_at": "2026-11-05T18:31:05Z",
          "completed_at": "2026-11-05T18:31:05Z"
        }
      ],
      "check_run_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213490",
      "labels": [
        "ubuntu-latest"
      ],
      "runner_id": 1000039485,
      "runner_name": "GitHub Actions 1000039485",
      "runner_group_id": 0,
      "runner_group_name": "GitHub Actions"
    },
    {
      "id": 127436213499,
      "run_id": 42081680387,
      "workflow_name": "gate",
      "head_branch": "agent/wp1240-g1-claude",
      "run_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42081680387",
      "run_attempt": 1,
      "node_id": "CR_kwDOTNeRjc8AAAAdq8pM-w",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/actions/jobs/127436213499",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213499",
      "status": "completed",
      "conclusion": "success",
      "created_at": "2026-11-05T18:10:44Z",
      "started_at": "2026-11-05T18:10:46Z",
      "completed_at": "2026-11-05T18:24:43Z",
      "name": "gate-cong-cu (ubuntu-latest, 3)",
      "steps": [
        {
          "name": "Set up job",
          "status": "completed",
          "conclusion": "success",
          "number": 1,
          "started_at": "2026-11-05T18:10:47Z",
          "completed_at": "2026-11-05T18:10:48Z"
        },
        {
          "name": "Force LF checkout (hash parity với manifest)",
          "status": "completed",
          "conclusion": "success",
          "number": 2,
          "started_at": "2026-11-05T18:10:48Z",
          "completed_at": "2026-11-05T18:10:48Z"
        },
        {
          "name": "Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 3,
          "started_at": "2026-11-05T18:10:48Z",
          "completed_at": "2026-11-05T18:10:54Z"
        },
        {
          "name": "Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 4,
          "started_at": "2026-11-05T18:10:54Z",
          "completed_at": "2026-11-05T18:10:54Z"
        },
        {
          "name": "cài PyYAML + jsonschema (cổng đăng lease + validator verdict cần)",
          "status": "completed",
          "conclusion": "success",
          "number": 5,
          "started_at": "2026-11-05T18:10:54Z",
          "completed_at": "2026-11-05T18:10:58Z"
        },
        {
          "name": "cài actionlint cho G5",
          "status": "completed",
          "conclusion": "success",
          "number": 6,
          "started_at": "2026-11-05T18:10:58Z",
          "completed_at": "2026-11-05T18:10:58Z"
        },
        {
          "name": "cài shellcheck cho G5 (cài xong đo lại)",
          "status": "completed",
          "conclusion": "success",
          "number": 7,
          "started_at": "2026-11-05T18:10:58Z",
          "completed_at": "2026-11-05T18:11:00Z"
        },
        {
          "name": "cài rg cho G5 (cài xong đo lại)",
          "status": "completed",
          "conclusion": "success",
          "number": 8,
          "started_at": "2026-11-05T18:11:00Z",
          "completed_at": "2026-11-05T18:11:04Z"
        },
        {
          "name": "G5 manh ban kinh dot bien (#668)",
          "status": "completed",
          "conclusion": "success",
          "number": 9,
          "started_at": "2026-11-05T18:11:04Z",
          "completed_at": "2026-11-05T18:24:39Z"
        },
        {
          "name": "Run actions/upload-artifact@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 10,
          "started_at": "2026-11-05T18:24:39Z",
          "completed_at": "2026-11-05T18:24:40Z"
        },
        {
          "name": "Post Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 19,
          "started_at": "2026-11-05T18:24:40Z",
          "completed_at": "2026-11-05T18:24:40Z"
        },
        {
          "name": "Post Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 20,
          "started_at": "2026-11-05T18:24:40Z",
          "completed_at": "2026-11-05T18:24:41Z"
        },
        {
          "name": "Complete job",
          "status": "completed",
          "conclusion": "success",
          "number": 21,
          "started_at": "2026-11-05T18:24:41Z",
          "completed_at": "2026-11-05T18:24:41Z"
        }
      ],
      "check_run_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213499",
      "labels": [
        "ubuntu-latest"
      ],
      "runner_id": 1000039481,
      "runner_name": "GitHub Actions 1000039481",
      "runner_group_id": 0,
      "runner_group_name": "GitHub Actions"
    },
    {
      "id": 127436213536,
      "run_id": 42081680387,
      "workflow_name": "gate",
      "head_branch": "agent/wp1240-g1-claude",
      "run_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42081680387",
      "run_attempt": 1,
      "node_id": "CR_kwDOTNeRjc8AAAAdq8pNIA",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/actions/jobs/127436213536",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213536",
      "status": "completed",
      "conclusion": "success",
      "created_at": "2026-11-05T18:10:44Z",
      "started_at": "2026-11-05T18:10:46Z",
      "completed_at": "2026-11-05T18:32:10Z",
      "name": "gate-cong-cu (ubuntu-latest, 4)",
      "steps": [
        {
          "name": "Set up job",
          "status": "completed",
          "conclusion": "success",
          "number": 1,
          "started_at": "2026-11-05T18:10:47Z",
          "completed_at": "2026-11-05T18:10:48Z"
        },
        {
          "name": "Force LF checkout (hash parity với manifest)",
          "status": "completed",
          "conclusion": "success",
          "number": 2,
          "started_at": "2026-11-05T18:10:48Z",
          "completed_at": "2026-11-05T18:10:49Z"
        },
        {
          "name": "Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 3,
          "started_at": "2026-11-05T18:10:49Z",
          "completed_at": "2026-11-05T18:11:00Z"
        },
        {
          "name": "Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 4,
          "started_at": "2026-11-05T18:11:00Z",
          "completed_at": "2026-11-05T18:11:00Z"
        },
        {
          "name": "cài PyYAML + jsonschema (cổng đăng lease + validator verdict cần)",
          "status": "completed",
          "conclusion": "success",
          "number": 5,
          "started_at": "2026-11-05T18:11:00Z",
          "completed_at": "2026-11-05T18:11:04Z"
        },
        {
          "name": "cài actionlint cho G5",
          "status": "completed",
          "conclusion": "success",
          "number": 6,
          "started_at": "2026-11-05T18:11:04Z",
          "completed_at": "2026-11-05T18:11:05Z"
        },
        {
          "name": "cài shellcheck cho G5 (cài xong đo lại)",
          "status": "completed",
          "conclusion": "success",
          "number": 7,
          "started_at": "2026-11-05T18:11:05Z",
          "completed_at": "2026-11-05T18:11:10Z"
        },
        {
          "name": "cài rg cho G5 (cài xong đo lại)",
          "status": "completed",
          "conclusion": "success",
          "number": 8,
          "started_at": "2026-11-05T18:11:10Z",
          "completed_at": "2026-11-05T18:11:19Z"
        },
        {
          "name": "G5 manh ban kinh dot bien (#668)",
          "status": "completed",
          "conclusion": "success",
          "number": 9,
          "started_at": "2026-11-05T18:11:19Z",
          "completed_at": "2026-11-05T18:32:06Z"
        },
        {
          "name": "Run actions/upload-artifact@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 10,
          "started_at": "2026-11-05T18:32:06Z",
          "completed_at": "2026-11-05T18:32:08Z"
        },
        {
          "name": "Post Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 19,
          "started_at": "2026-11-05T18:32:08Z",
          "completed_at": "2026-11-05T18:32:08Z"
        },
        {
          "name": "Post Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 20,
          "started_at": "2026-11-05T18:32:08Z",
          "completed_at": "2026-11-05T18:32:08Z"
        },
        {
          "name": "Complete job",
          "status": "completed",
          "conclusion": "success",
          "number": 21,
          "started_at": "2026-11-05T18:32:08Z",
          "completed_at": "2026-11-05T18:32:08Z"
        }
      ],
      "check_run_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213536",
      "labels": [
        "ubuntu-latest"
      ],
      "runner_id": 1000039491,
      "runner_name": "GitHub Actions 1000039491",
      "runner_group_id": 0,
      "runner_group_name": "GitHub Actions"
    },
    {
      "id": 127436213563,
      "run_id": 42081680387,
      "workflow_name": "gate",
      "head_branch": "agent/wp1240-g1-claude",
      "run_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42081680387",
      "run_attempt": 1,
      "node_id": "CR_kwDOTNeRjc8AAAAdq8pNOw",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/actions/jobs/127436213563",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213563",
      "status": "completed",
      "conclusion": "success",
      "created_at": "2026-11-05T18:10:44Z",
      "started_at": "2026-11-05T18:10:47Z",
      "completed_at": "2026-11-05T18:32:22Z",
      "name": "gate-cong-cu (ubuntu-latest, 0)",
      "steps": [
        {
          "name": "Set up job",
          "status": "completed",
          "conclusion": "success",
          "number": 1,
          "started_at": "2026-11-05T18:10:48Z",
          "completed_at": "2026-11-05T18:10:48Z"
        },
        {
          "name": "Force LF checkout (hash parity với manifest)",
          "status": "completed",
          "conclusion": "success",
          "number": 2,
          "started_at": "2026-11-05T18:10:48Z",
          "completed_at": "2026-11-05T18:10:49Z"
        },
        {
          "name": "Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 3,
          "started_at": "2026-11-05T18:10:49Z",
          "completed_at": "2026-11-05T18:10:57Z"
        },
        {
          "name": "Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 4,
          "started_at": "2026-11-05T18:10:57Z",
          "completed_at": "2026-11-05T18:10:57Z"
        },
        {
          "name": "cài PyYAML + jsonschema (cổng đăng lease + validator verdict cần)",
          "status": "completed",
          "conclusion": "success",
          "number": 5,
          "started_at": "2026-11-05T18:10:57Z",
          "completed_at": "2026-11-05T18:10:59Z"
        },
        {
          "name": "cài actionlint cho G5",
          "status": "completed",
          "conclusion": "success",
          "number": 6,
          "started_at": "2026-11-05T18:10:59Z",
          "completed_at": "2026-11-05T18:10:59Z"
        },
        {
          "name": "cài shellcheck cho G5 (cài xong đo lại)",
          "status": "completed",
          "conclusion": "success",
          "number": 7,
          "started_at": "2026-11-05T18:10:59Z",
          "completed_at": "2026-11-05T18:11:01Z"
        },
        {
          "name": "cài rg cho G5 (cài xong đo lại)",
          "status": "completed",
          "conclusion": "success",
          "number": 8,
          "started_at": "2026-11-05T18:11:01Z",
          "completed_at": "2026-11-05T18:11:52Z"
        },
        {
          "name": "G5 manh ban kinh dot bien (#668)",
          "status": "completed",
          "conclusion": "success",
          "number": 9,
          "started_at": "2026-11-05T18:11:52Z",
          "completed_at": "2026-11-05T18:32:17Z"
        },
        {
          "name": "Run actions/upload-artifact@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 10,
          "started_at": "2026-11-05T18:32:17Z",
          "completed_at": "2026-11-05T18:32:19Z"
        },
        {
          "name": "Post Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 19,
          "started_at": "2026-11-05T18:32:19Z",
          "completed_at": "2026-11-05T18:32:19Z"
        },
        {
          "name": "Post Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 20,
          "started_at": "2026-11-05T18:32:19Z",
          "completed_at": "2026-11-05T18:32:19Z"
        },
        {
          "name": "Complete job",
          "status": "completed",
          "conclusion": "success",
          "number": 21,
          "started_at": "2026-11-05T18:32:19Z",
          "completed_at": "2026-11-05T18:32:19Z"
        }
      ],
      "check_run_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213563",
      "labels": [
        "ubuntu-latest"
      ],
      "runner_id": 1000039479,
      "runner_name": "GitHub Actions 1000039479",
      "runner_group_id": 0,
      "runner_group_name": "GitHub Actions"
    },
    {
      "id": 127436213564,
      "run_id": 42081680387,
      "workflow_name": "gate",
      "head_branch": "agent/wp1240-g1-claude",
      "run_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42081680387",
      "run_attempt": 1,
      "node_id": "CR_kwDOTNeRjc8AAAAdq8pNPA",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/actions/jobs/127436213564",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213564",
      "status": "completed",
      "conclusion": "success",
      "created_at": "2026-11-05T18:10:44Z",
      "started_at": "2026-11-05T18:10:46Z",
      "completed_at": "2026-11-05T18:11:57Z",
      "name": "gate-nhanh-manh (ubuntu-latest, 6)",
      "steps": [
        {
          "name": "Set up job",
          "status": "completed",
          "conclusion": "success",
          "number": 1,
          "started_at": "2026-11-05T18:10:47Z",
          "completed_at": "2026-11-05T18:10:48Z"
        },
        {
          "name": "Force LF checkout (hash parity với manifest)",
          "status": "completed",
          "conclusion": "success",
          "number": 2,
          "started_at": "2026-11-05T18:10:48Z",
          "completed_at": "2026-11-05T18:10:48Z"
        },
        {
          "name": "Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 3,
          "started_at": "2026-11-05T18:10:48Z",
          "completed_at": "2026-11-05T18:10:54Z"
        },
        {
          "name": "Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 4,
          "started_at": "2026-11-05T18:10:54Z",
          "completed_at": "2026-11-05T18:10:54Z"
        },
        {
          "name": "DUONG_NHANH - liet ke buoc bo qua (job gate-nhanh-manh)",
          "status": "completed",
          "conclusion": "skipped",
          "number": 5,
          "started_at": "2026-11-05T18:10:54Z",
          "completed_at": "2026-11-05T18:10:54Z"
        },
        {
          "name": "chạy mảnh nhanh_don_duoc (targeted_mutant_gate)",
          "status": "completed",
          "conclusion": "success",
          "number": 6,
          "started_at": "2026-11-05T18:10:54Z",
          "completed_at": "2026-11-05T18:11:54Z"
        },
        {
          "name": "Run actions/upload-artifact@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 7,
          "started_at": "2026-11-05T18:11:54Z",
          "completed_at": "2026-11-05T18:11:55Z"
        },
        {
          "name": "Post Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 13,
          "started_at": "2026-11-05T18:11:55Z",
          "completed_at": "2026-11-05T18:11:55Z"
        },
        {
          "name": "Post Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 14,
          "started_at": "2026-11-05T18:11:55Z",
          "completed_at": "2026-11-05T18:11:56Z"
        },
        {
          "name": "Complete job",
          "status": "completed",
          "conclusion": "success",
          "number": 15,
          "started_at": "2026-11-05T18:11:56Z",
          "completed_at": "2026-11-05T18:11:56Z"
        }
      ],
      "check_run_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213564",
      "labels": [
        "ubuntu-latest"
      ],
      "runner_id": 1000039478,
      "runner_name": "GitHub Actions 1000039478",
      "runner_group_id": 0,
      "runner_group_name": "GitHub Actions"
    },
    {
      "id": 127436213571,
      "run_id": 42081680387,
      "workflow_name": "gate",
      "head_branch": "agent/wp1240-g1-claude",
      "run_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42081680387",
      "run_attempt": 1,
      "node_id": "CR_kwDOTNeRjc8AAAAdq8pNQw",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/actions/jobs/127436213571",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213571",
      "status": "completed",
      "conclusion": "success",
      "created_at": "2026-11-05T18:10:44Z",
      "started_at": "2026-11-05T18:10:46Z",
      "completed_at": "2026-11-05T18:31:40Z",
      "name": "gate-cong-cu (ubuntu-latest, 1)",
      "steps": [
        {
          "name": "Set up job",
          "status": "completed",
          "conclusion": "success",
          "number": 1,
          "started_at": "2026-11-05T18:10:47Z",
          "completed_at": "2026-11-05T18:10:48Z"
        },
        {
          "name": "Force LF checkout (hash parity với manifest)",
          "status": "completed",
          "conclusion": "success",
          "number": 2,
          "started_at": "2026-11-05T18:10:48Z",
          "completed_at": "2026-11-05T18:10:48Z"
        },
        {
          "name": "Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 3,
          "started_at": "2026-11-05T18:10:48Z",
          "completed_at": "2026-11-05T18:10:56Z"
        },
        {
          "name": "Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 4,
          "started_at": "2026-11-05T18:10:56Z",
          "completed_at": "2026-11-05T18:10:56Z"
        },
        {
          "name": "cài PyYAML + jsonschema (cổng đăng lease + validator verdict cần)",
          "status": "completed",
          "conclusion": "success",
          "number": 5,
          "started_at": "2026-11-05T18:10:56Z",
          "completed_at": "2026-11-05T18:10:58Z"
        },
        {
          "name": "cài actionlint cho G5",
          "status": "completed",
          "conclusion": "success",
          "number": 6,
          "started_at": "2026-11-05T18:10:58Z",
          "completed_at": "2026-11-05T18:10:58Z"
        },
        {
          "name": "cài shellcheck cho G5 (cài xong đo lại)",
          "status": "completed",
          "conclusion": "success",
          "number": 7,
          "started_at": "2026-11-05T18:10:58Z",
          "completed_at": "2026-11-05T18:11:00Z"
        },
        {
          "name": "cài rg cho G5 (cài xong đo lại)",
          "status": "completed",
          "conclusion": "success",
          "number": 8,
          "started_at": "2026-11-05T18:11:00Z",
          "completed_at": "2026-11-05T18:11:05Z"
        },
        {
          "name": "G5 manh ban kinh dot bien (#668)",
          "status": "completed",
          "conclusion": "success",
          "number": 9,
          "started_at": "2026-11-05T18:11:05Z",
          "completed_at": "2026-11-05T18:31:36Z"
        },
        {
          "name": "Run actions/upload-artifact@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 10,
          "started_at": "2026-11-05T18:31:36Z",
          "completed_at": "2026-11-05T18:31:37Z"
        },
        {
          "name": "Post Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 19,
          "started_at": "2026-11-05T18:31:37Z",
          "completed_at": "2026-11-05T18:31:38Z"
        },
        {
          "name": "Post Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 20,
          "started_at": "2026-11-05T18:31:38Z",
          "completed_at": "2026-11-05T18:31:38Z"
        },
        {
          "name": "Complete job",
          "status": "completed",
          "conclusion": "success",
          "number": 21,
          "started_at": "2026-11-05T18:31:38Z",
          "completed_at": "2026-11-05T18:31:38Z"
        }
      ],
      "check_run_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213571",
      "labels": [
        "ubuntu-latest"
      ],
      "runner_id": 1000039480,
      "runner_name": "GitHub Actions 1000039480",
      "runner_group_id": 0,
      "runner_group_name": "GitHub Actions"
    },
    {
      "id": 127436213573,
      "run_id": 42081680387,
      "workflow_name": "gate",
      "head_branch": "agent/wp1240-g1-claude",
      "run_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42081680387",
      "run_attempt": 1,
      "node_id": "CR_kwDOTNeRjc8AAAAdq8pNRQ",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/actions/jobs/127436213573",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213573",
      "status": "completed",
      "conclusion": "success",
      "created_at": "2026-11-05T18:10:44Z",
      "started_at": "2026-11-05T18:10:46Z",
      "completed_at": "2026-11-05T19:13:21Z",
      "name": "gate-packet-loop (ubuntu-latest)",
      "steps": [
        {
          "name": "Set up job",
          "status": "completed",
          "conclusion": "success",
          "number": 1,
          "started_at": "2026-11-05T18:10:47Z",
          "completed_at": "2026-11-05T18:10:48Z"
        },
        {
          "name": "Force LF checkout (hash parity với manifest)",
          "status": "completed",
          "conclusion": "success",
          "number": 2,
          "started_at": "2026-11-05T18:10:48Z",
          "completed_at": "2026-11-05T18:10:48Z"
        },
        {
          "name": "Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 3,
          "started_at": "2026-11-05T18:10:48Z",
          "completed_at": "2026-11-05T18:10:56Z"
        },
        {
          "name": "Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 4,
          "started_at": "2026-11-05T18:10:56Z",
          "completed_at": "2026-11-05T18:10:56Z"
        },
        {
          "name": "cài PyYAML + jsonschema (cổng đăng lease + validator verdict cần)",
          "status": "completed",
          "conclusion": "success",
          "number": 5,
          "started_at": "2026-11-05T18:10:56Z",
          "completed_at": "2026-11-05T18:11:00Z"
        },
        {
          "name": "cài actionlint cho G5",
          "status": "completed",
          "conclusion": "success",
          "number": 6,
          "started_at": "2026-11-05T18:11:00Z",
          "completed_at": "2026-11-05T18:11:00Z"
        },
        {
          "name": "cài shellcheck cho G5 (cài xong đo lại)",
          "status": "completed",
          "conclusion": "success",
          "number": 7,
          "started_at": "2026-11-05T18:11:00Z",
          "completed_at": "2026-11-05T18:11:02Z"
        },
        {
          "name": "cài rg cho G5 (cài xong đo lại)",
          "status": "completed",
          "conclusion": "success",
          "number": 8,
          "started_at": "2026-11-05T18:11:02Z",
          "completed_at": "2026-11-05T18:11:07Z"
        },
        {
          "name": "G5 probe ban ke cong cu (#290; selftest T1..T8 chi o job gate, chot M6",
          "status": "completed",
          "conclusion": "success",
          "number": 9,
          "started_at": "2026-11-05T18:11:07Z",
          "completed_at": "2026-11-05T18:11:08Z"
        },
        {
          "name": "cài Ruff 0.15.15 và in probe dương",
          "status": "completed",
          "conclusion": "success",
          "number": 10,
          "started_at": "2026-11-05T18:11:08Z",
          "completed_at": "2026-11-05T18:11:09Z"
        },
        {
          "name": "DUONG_NHANH - liet ke buoc bo qua (job gate-packet-loop)",
          "status": "completed",
          "conclusion": "skipped",
          "number": 11,
          "started_at": "2026-11-05T18:11:09Z",
          "completed_at": "2026-11-05T18:11:09Z"
        },
        {
          "name": "packet-loop selftest",
          "status": "completed",
          "conclusion": "success",
          "number": 12,
          "started_at": "2026-11-05T18:11:09Z",
          "completed_at": "2026-11-05T19:13:19Z"
        },
        {
          "name": "Post Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 23,
          "started_at": "2026-11-05T19:13:19Z",
          "completed_at": "2026-11-05T19:13:19Z"
        },
        {
          "name": "Post Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 24,
          "started_at": "2026-11-05T19:13:19Z",
          "completed_at": "2026-11-05T19:13:19Z"
        },
        {
          "name": "Complete job",
          "status": "completed",
          "conclusion": "success",
          "number": 25,
          "started_at": "2026-11-05T19:13:19Z",
          "completed_at": "2026-11-05T19:13:19Z"
        }
      ],
      "check_run_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213573",
      "labels": [
        "ubuntu-latest"
      ],
      "runner_id": 1000039486,
      "runner_name": "GitHub Actions 1000039486",
      "runner_group_id": 0,
      "runner_group_name": "GitHub Actions"
    },
    {
      "id": 127436213593,
      "run_id": 42081680387,
      "workflow_name": "gate",
      "head_branch": "agent/wp1240-g1-claude",
      "run_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42081680387",
      "run_attempt": 1,
      "node_id": "CR_kwDOTNeRjc8AAAAdq8pNWQ",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/actions/jobs/127436213593",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213593",
      "status": "completed",
      "conclusion": "success",
      "created_at": "2026-11-05T18:10:44Z",
      "started_at": "2026-11-05T18:10:47Z",
      "completed_at": "2026-11-05T18:12:24Z",
      "name": "gate-nhanh-manh (ubuntu-latest, 7)",
      "steps": [
        {
          "name": "Set up job",
          "status": "completed",
          "conclusion": "success",
          "number": 1,
          "started_at": "2026-11-05T18:10:48Z",
          "completed_at": "2026-11-05T18:10:48Z"
        },
        {
          "name": "Force LF checkout (hash parity với manifest)",
          "status": "completed",
          "conclusion": "success",
          "number": 2,
          "started_at": "2026-11-05T18:10:48Z",
          "completed_at": "2026-11-05T18:10:48Z"
        },
        {
          "name": "Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 3,
          "started_at": "2026-11-05T18:10:48Z",
          "completed_at": "2026-11-05T18:10:57Z"
        },
        {
          "name": "Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 4,
          "started_at": "2026-11-05T18:10:57Z",
          "completed_at": "2026-11-05T18:10:57Z"
        },
        {
          "name": "DUONG_NHANH - liet ke buoc bo qua (job gate-nhanh-manh)",
          "status": "completed",
          "conclusion": "skipped",
          "number": 5,
          "started_at": "2026-11-05T18:10:57Z",
          "completed_at": "2026-11-05T18:10:57Z"
        },
        {
          "name": "chạy mảnh nhanh_don_duoc (targeted_mutant_gate)",
          "status": "completed",
          "conclusion": "success",
          "number": 6,
          "started_at": "2026-11-05T18:10:57Z",
          "completed_at": "2026-11-05T18:12:20Z"
        },
        {
          "name": "Run actions/upload-artifact@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 7,
          "started_at": "2026-11-05T18:12:20Z",
          "completed_at": "2026-11-05T18:12:21Z"
        },
        {
          "name": "Post Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 13,
          "started_at": "2026-11-05T18:12:21Z",
          "completed_at": "2026-11-05T18:12:21Z"
        },
        {
          "name": "Post Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 14,
          "started_at": "2026-11-05T18:12:21Z",
          "completed_at": "2026-11-05T18:12:22Z"
        },
        {
          "name": "Complete job",
          "status": "completed",
          "conclusion": "success",
          "number": 15,
          "started_at": "2026-11-05T18:12:22Z",
          "completed_at": "2026-11-05T18:12:22Z"
        }
      ],
      "check_run_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213593",
      "labels": [
        "ubuntu-latest"
      ],
      "runner_id": 1000039484,
      "runner_name": "GitHub Actions 1000039484",
      "runner_group_id": 0,
      "runner_group_name": "GitHub Actions"
    },
    {
      "id": 127436213596,
      "run_id": 42081680387,
      "workflow_name": "gate",
      "head_branch": "agent/wp1240-g1-claude",
      "run_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42081680387",
      "run_attempt": 1,
      "node_id": "CR_kwDOTNeRjc8AAAAdq8pNXA",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/actions/jobs/127436213596",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213596",
      "status": "completed",
      "conclusion": "success",
      "created_at": "2026-11-05T18:10:44Z",
      "started_at": "2026-11-05T18:10:47Z",
      "completed_at": "2026-11-05T18:11:42Z",
      "name": "gate-nhanh-manh (ubuntu-latest, 1)",
      "steps": [
        {
          "name": "Set up job",
          "status": "completed",
          "conclusion": "success",
          "number": 1,
          "started_at": "2026-11-05T18:10:47Z",
          "completed_at": "2026-11-05T18:10:48Z"
        },
        {
          "name": "Force LF checkout (hash parity với manifest)",
          "status": "completed",
          "conclusion": "success",
          "number": 2,
          "started_at": "2026-11-05T18:10:48Z",
          "completed_at": "2026-11-05T18:10:48Z"
        },
        {
          "name": "Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 3,
          "started_at": "2026-11-05T18:10:48Z",
          "completed_at": "2026-11-05T18:10:56Z"
        },
        {
          "name": "Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 4,
          "started_at": "2026-11-05T18:10:56Z",
          "completed_at": "2026-11-05T18:10:57Z"
        },
        {
          "name": "DUONG_NHANH - liet ke buoc bo qua (job gate-nhanh-manh)",
          "status": "completed",
          "conclusion": "skipped",
          "number": 5,
          "started_at": "2026-11-05T18:10:57Z",
          "completed_at": "2026-11-05T18:10:57Z"
        },
        {
          "name": "chạy mảnh nhanh_don_duoc (targeted_mutant_gate)",
          "status": "completed",
          "conclusion": "success",
          "number": 6,
          "started_at": "2026-11-05T18:10:57Z",
          "completed_at": "2026-11-05T18:11:38Z"
        },
        {
          "name": "Run actions/upload-artifact@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 7,
          "started_at": "2026-11-05T18:11:38Z",
          "completed_at": "2026-11-05T18:11:39Z"
        },
        {
          "name": "Post Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 13,
          "started_at": "2026-11-05T18:11:39Z",
          "completed_at": "2026-11-05T18:11:39Z"
        },
        {
          "name": "Post Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 14,
          "started_at": "2026-11-05T18:11:39Z",
          "completed_at": "2026-11-05T18:11:39Z"
        },
        {
          "name": "Complete job",
          "status": "completed",
          "conclusion": "success",
          "number": 15,
          "started_at": "2026-11-05T18:11:39Z",
          "completed_at": "2026-11-05T18:11:39Z"
        }
      ],
      "check_run_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213596",
      "labels": [
        "ubuntu-latest"
      ],
      "runner_id": 1000039487,
      "runner_name": "GitHub Actions 1000039487",
      "runner_group_id": 0,
      "runner_group_name": "GitHub Actions"
    },
    {
      "id": 127436213654,
      "run_id": 42081680387,
      "workflow_name": "gate",
      "head_branch": "agent/wp1240-g1-claude",
      "run_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42081680387",
      "run_attempt": 1,
      "node_id": "CR_kwDOTNeRjc8AAAAdq8pNlg",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/actions/jobs/127436213654",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213654",
      "status": "completed",
      "conclusion": "success",
      "created_at": "2026-11-05T18:10:44Z",
      "started_at": "2026-11-05T18:10:47Z",
      "completed_at": "2026-11-05T18:11:46Z",
      "name": "gate-nhanh-manh (ubuntu-latest, 0)",
      "steps": [
        {
          "name": "Set up job",
          "status": "completed",
          "conclusion": "success",
          "number": 1,
          "started_at": "2026-11-05T18:10:48Z",
          "completed_at": "2026-11-05T18:10:49Z"
        },
        {
          "name": "Force LF checkout (hash parity với manifest)",
          "status": "completed",
          "conclusion": "success",
          "number": 2,
          "started_at": "2026-11-05T18:10:49Z",
          "completed_at": "2026-11-05T18:10:49Z"
        },
        {
          "name": "Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 3,
          "started_at": "2026-11-05T18:10:49Z",
          "completed_at": "2026-11-05T18:10:58Z"
        },
        {
          "name": "Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 4,
          "started_at": "2026-11-05T18:10:58Z",
          "completed_at": "2026-11-05T18:10:58Z"
        },
        {
          "name": "DUONG_NHANH - liet ke buoc bo qua (job gate-nhanh-manh)",
          "status": "completed",
          "conclusion": "skipped",
          "number": 5,
          "started_at": "2026-11-05T18:10:58Z",
          "completed_at": "2026-11-05T18:10:58Z"
        },
        {
          "name": "chạy mảnh nhanh_don_duoc (targeted_mutant_gate)",
          "status": "completed",
          "conclusion": "success",
          "number": 6,
          "started_at": "2026-11-05T18:10:58Z",
          "completed_at": "2026-11-05T18:11:41Z"
        },
        {
          "name": "Run actions/upload-artifact@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 7,
          "started_at": "2026-11-05T18:11:41Z",
          "completed_at": "2026-11-05T18:11:43Z"
        },
        {
          "name": "Post Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 13,
          "started_at": "2026-11-05T18:11:43Z",
          "completed_at": "2026-11-05T18:11:43Z"
        },
        {
          "name": "Post Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 14,
          "started_at": "2026-11-05T18:11:43Z",
          "completed_at": "2026-11-05T18:11:43Z"
        },
        {
          "name": "Complete job",
          "status": "completed",
          "conclusion": "success",
          "number": 15,
          "started_at": "2026-11-05T18:11:43Z",
          "completed_at": "2026-11-05T18:11:43Z"
        }
      ],
      "check_run_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213654",
      "labels": [
        "ubuntu-latest"
      ],
      "runner_id": 1000039489,
      "runner_name": "GitHub Actions 1000039489",
      "runner_group_id": 0,
      "runner_group_name": "GitHub Actions"
    },
    {
      "id": 127436213669,
      "run_id": 42081680387,
      "workflow_name": "gate",
      "head_branch": "agent/wp1240-g1-claude",
      "run_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42081680387",
      "run_attempt": 1,
      "node_id": "CR_kwDOTNeRjc8AAAAdq8pNpQ",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/actions/jobs/127436213669",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213669",
      "status": "completed",
      "conclusion": "success",
      "created_at": "2026-11-05T18:10:44Z",
      "started_at": "2026-11-05T18:10:46Z",
      "completed_at": "2026-11-05T18:12:00Z",
      "name": "gate-nhanh-manh (ubuntu-latest, 4)",
      "steps": [
        {
          "name": "Set up job",
          "status": "completed",
          "conclusion": "success",
          "number": 1,
          "started_at": "2026-11-05T18:10:47Z",
          "completed_at": "2026-11-05T18:10:48Z"
        },
        {
          "name": "Force LF checkout (hash parity với manifest)",
          "status": "completed",
          "conclusion": "success",
          "number": 2,
          "started_at": "2026-11-05T18:10:48Z",
          "completed_at": "2026-11-05T18:10:48Z"
        },
        {
          "name": "Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 3,
          "started_at": "2026-11-05T18:10:48Z",
          "completed_at": "2026-11-05T18:10:55Z"
        },
        {
          "name": "Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 4,
          "started_at": "2026-11-05T18:10:55Z",
          "completed_at": "2026-11-05T18:10:55Z"
        },
        {
          "name": "DUONG_NHANH - liet ke buoc bo qua (job gate-nhanh-manh)",
          "status": "completed",
          "conclusion": "skipped",
          "number": 5,
          "started_at": "2026-11-05T18:10:55Z",
          "completed_at": "2026-11-05T18:10:55Z"
        },
        {
          "name": "chạy mảnh nhanh_don_duoc (targeted_mutant_gate)",
          "status": "completed",
          "conclusion": "success",
          "number": 6,
          "started_at": "2026-11-05T18:10:55Z",
          "completed_at": "2026-11-05T18:11:57Z"
        },
        {
          "name": "Run actions/upload-artifact@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 7,
          "started_at": "2026-11-05T18:11:57Z",
          "completed_at": "2026-11-05T18:11:59Z"
        },
        {
          "name": "Post Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 13,
          "started_at": "2026-11-05T18:11:59Z",
          "completed_at": "2026-11-05T18:11:59Z"
        },
        {
          "name": "Post Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 14,
          "started_at": "2026-11-05T18:11:59Z",
          "completed_at": "2026-11-05T18:11:59Z"
        },
        {
          "name": "Complete job",
          "status": "completed",
          "conclusion": "success",
          "number": 15,
          "started_at": "2026-11-05T18:11:59Z",
          "completed_at": "2026-11-05T18:11:59Z"
        }
      ],
      "check_run_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213669",
      "labels": [
        "ubuntu-latest"
      ],
      "runner_id": 1000039488,
      "runner_name": "GitHub Actions 1000039488",
      "runner_group_id": 0,
      "runner_group_name": "GitHub Actions"
    },
    {
      "id": 127436213864,
      "run_id": 42081680387,
      "workflow_name": "gate",
      "head_branch": "agent/wp1240-g1-claude",
      "run_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42081680387",
      "run_attempt": 1,
      "node_id": "CR_kwDOTNeRjc8AAAAdq8pOaA",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/actions/jobs/127436213864",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213864",
      "status": "completed",
      "conclusion": "success",
      "created_at": "2026-11-05T18:10:44Z",
      "started_at": "2026-11-05T18:10:47Z",
      "completed_at": "2026-11-05T18:12:22Z",
      "name": "gate-nhanh-manh (ubuntu-latest, 3)",
      "steps": [
        {
          "name": "Set up job",
          "status": "completed",
          "conclusion": "success",
          "number": 1,
          "started_at": "2026-11-05T18:10:48Z",
          "completed_at": "2026-11-05T18:10:49Z"
        },
        {
          "name": "Force LF checkout (hash parity với manifest)",
          "status": "completed",
          "conclusion": "success",
          "number": 2,
          "started_at": "2026-11-05T18:10:49Z",
          "completed_at": "2026-11-05T18:10:49Z"
        },
        {
          "name": "Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 3,
          "started_at": "2026-11-05T18:10:49Z",
          "completed_at": "2026-11-05T18:10:59Z"
        },
        {
          "name": "Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 4,
          "started_at": "2026-11-05T18:10:59Z",
          "completed_at": "2026-11-05T18:10:59Z"
        },
        {
          "name": "DUONG_NHANH - liet ke buoc bo qua (job gate-nhanh-manh)",
          "status": "completed",
          "conclusion": "skipped",
          "number": 5,
          "started_at": "2026-11-05T18:10:59Z",
          "completed_at": "2026-11-05T18:10:59Z"
        },
        {
          "name": "chạy mảnh nhanh_don_duoc (targeted_mutant_gate)",
          "status": "completed",
          "conclusion": "success",
          "number": 6,
          "started_at": "2026-11-05T18:10:59Z",
          "completed_at": "2026-11-05T18:12:18Z"
        },
        {
          "name": "Run actions/upload-artifact@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 7,
          "started_at": "2026-11-05T18:12:18Z",
          "completed_at": "2026-11-05T18:12:19Z"
        },
        {
          "name": "Post Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 13,
          "started_at": "2026-11-05T18:12:19Z",
          "completed_at": "2026-11-05T18:12:19Z"
        },
        {
          "name": "Post Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 14,
          "started_at": "2026-11-05T18:12:19Z",
          "completed_at": "2026-11-05T18:12:20Z"
        },
        {
          "name": "Complete job",
          "status": "completed",
          "conclusion": "success",
          "number": 15,
          "started_at": "2026-11-05T18:12:20Z",
          "completed_at": "2026-11-05T18:12:20Z"
        }
      ],
      "check_run_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213864",
      "labels": [
        "ubuntu-latest"
      ],
      "runner_id": 1000039494,
      "runner_name": "GitHub Actions 1000039494",
      "runner_group_id": 0,
      "runner_group_name": "GitHub Actions"
    },
    {
      "id": 127436213870,
      "run_id": 42081680387,
      "workflow_name": "gate",
      "head_branch": "agent/wp1240-g1-claude",
      "run_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42081680387",
      "run_attempt": 1,
      "node_id": "CR_kwDOTNeRjc8AAAAdq8pObg",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/actions/jobs/127436213870",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213870",
      "status": "completed",
      "conclusion": "success",
      "created_at": "2026-11-05T18:10:44Z",
      "started_at": "2026-11-05T18:10:46Z",
      "completed_at": "2026-11-05T18:23:32Z",
      "name": "gate-cong-cu (ubuntu-latest, 7)",
      "steps": [
        {
          "name": "Set up job",
          "status": "completed",
          "conclusion": "success",
          "number": 1,
          "started_at": "2026-11-05T18:10:47Z",
          "completed_at": "2026-11-05T18:10:48Z"
        },
        {
          "name": "Force LF checkout (hash parity với manifest)",
          "status": "completed",
          "conclusion": "success",
          "number": 2,
          "started_at": "2026-11-05T18:10:48Z",
          "completed_at": "2026-11-05T18:10:48Z"
        },
        {
          "name": "Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 3,
          "started_at": "2026-11-05T18:10:48Z",
          "completed_at": "2026-11-05T18:10:54Z"
        },
        {
          "name": "Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 4,
          "started_at": "2026-11-05T18:10:54Z",
          "completed_at": "2026-11-05T18:10:55Z"
        },
        {
          "name": "cài PyYAML + jsonschema (cổng đăng lease + validator verdict cần)",
          "status": "completed",
          "conclusion": "success",
          "number": 5,
          "started_at": "2026-11-05T18:10:55Z",
          "completed_at": "2026-11-05T18:10:56Z"
        },
        {
          "name": "cài actionlint cho G5",
          "status": "completed",
          "conclusion": "success",
          "number": 6,
          "started_at": "2026-11-05T18:10:56Z",
          "completed_at": "2026-11-05T18:10:56Z"
        },
        {
          "name": "cài shellcheck cho G5 (cài xong đo lại)",
          "status": "completed",
          "conclusion": "success",
          "number": 7,
          "started_at": "2026-11-05T18:10:56Z",
          "completed_at": "2026-11-05T18:10:58Z"
        },
        {
          "name": "cài rg cho G5 (cài xong đo lại)",
          "status": "completed",
          "conclusion": "success",
          "number": 8,
          "started_at": "2026-11-05T18:10:58Z",
          "completed_at": "2026-11-05T18:11:02Z"
        },
        {
          "name": "G5 manh ban kinh dot bien (#668)",
          "status": "completed",
          "conclusion": "success",
          "number": 9,
          "started_at": "2026-11-05T18:11:02Z",
          "completed_at": "2026-11-05T18:23:28Z"
        },
        {
          "name": "Run actions/upload-artifact@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 10,
          "started_at": "2026-11-05T18:23:28Z",
          "completed_at": "2026-11-05T18:23:30Z"
        },
        {
          "name": "Post Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 19,
          "started_at": "2026-11-05T18:23:30Z",
          "completed_at": "2026-11-05T18:23:30Z"
        },
        {
          "name": "Post Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 20,
          "started_at": "2026-11-05T18:23:30Z",
          "completed_at": "2026-11-05T18:23:30Z"
        },
        {
          "name": "Complete job",
          "status": "completed",
          "conclusion": "success",
          "number": 21,
          "started_at": "2026-11-05T18:23:30Z",
          "completed_at": "2026-11-05T18:23:30Z"
        }
      ],
      "check_run_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213870",
      "labels": [
        "ubuntu-latest"
      ],
      "runner_id": 1000039496,
      "runner_name": "GitHub Actions 1000039496",
      "runner_group_id": 0,
      "runner_group_name": "GitHub Actions"
    },
    {
      "id": 127436213872,
      "run_id": 42081680387,
      "workflow_name": "gate",
      "head_branch": "agent/wp1240-g1-claude",
      "run_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42081680387",
      "run_attempt": 1,
      "node_id": "CR_kwDOTNeRjc8AAAAdq8pOcA",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/actions/jobs/127436213872",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127436213872",
      "status": "completed",
      "conclusion": "success",
      "created_at": "2026-11-05T18:10:44Z",
      "started_at": "2026-11-05T18:10:46Z",
      "completed_at": "2026-11-05T18:11:41Z",
      "name": "gate-nhanh-manh (ubuntu-latest, 5)",
      "steps": [
        {
          "name": "Set up job",
          "status": "completed",
          "conclusion": "success",
          "number": 1,
          "started_at": "2026-11-05T18:10:47Z",
          "completed_at": "2026-11-05T18:10:48Z"
        },
        {
          "name": "Force LF checkout (hash parity với manifest)",
          "status": "completed",
          "conclusion": "success",
          "number": 2,
          "started_at": "2026-11-05T18:10:48Z",
          "completed_at": "2026-11-05T18:10:48Z"
        },
        {
          "name": "Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 3,
          "started_at": "2026-11-05T18:10:48Z",
          "completed_at": "2026-11-05T18:10:56Z"
        },
        {
          "name": "Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 4,
          "started_at": "2026-11-05T18:10:56Z",
          "completed_at": "2026-11-05T18:10:56Z"
        },
        {
          "name": "DUONG_NHANH - liet ke buoc bo qua (job gate-nhanh-manh)",
          "status": "completed",
          "conclusion": "skipped",
          "number": 5,
          "started_at": "2026-11-05T18:10:56Z",
          "completed_at": "2026-11-05T18:10:56Z"
        },
        {
          "name": "chạy mảnh nhanh_don_duoc (targeted_mutant_gate)",
          "status": "completed",
          "conclusion": "success",
          "number": 6,
          "started_at": "2026-11-05T18:10:56Z",
          "completed_at": "2026-11-05T18:11:38Z"
        },
        {
          "name": "Run actions/upload-artifact@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 7,
          "started_at": "2026-11-05T18:11:38Z",
          "completed_at": "2026-11-05T18:11:39Z"
        },
        {
          "name": "Post Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 13,
          "started_at": "2026-11-05T18:11:39Z",
          "completed_at": "2026-11-05T18:11:39Z"
        },
        {
          "name": "Post Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 14,
          "started_at": "2026-11-05T18:11:39Z",
          "completed_at": "2026-11-05T18:11:39Z"
        },
        {
          "name": "Complete job",
          "status": "completed",
          "conclusion": "success",
          "number": 15,
          "started_at": "2026-11-05T18:11:39Z",
          "completed_at": "2026-11-05T18:11:39Z"
        }
      ],
      "check_run_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127436213872",
      "labels": [
        "ubuntu-latest"
      ],
      "runner_id": 1000039495,
      "runner_name": "GitHub Actions 1000039495",
      "runner_group_id": 0,
      "runner_group_name": "GitHub Actions"
    },
    {
      "id": 127437121173,
      "run_id": 42081680387,
      "workflow_name": "gate",
      "head_branch": "agent/wp1240-g1-claude",
      "run_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42081680387",
      "run_attempt": 1,
      "node_id": "CR_kwDOTNeRjc8AAAAdq9gmlQ",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/actions/jobs/127437121173",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127437121173",
      "status": "completed",
      "conclusion": "success",
      "created_at": "2026-11-05T18:12:24Z",
      "started_at": "2026-11-05T18:12:27Z",
      "completed_at": "2026-11-05T18:12:43Z",
      "name": "gate-nhanh-gop (ubuntu-latest)",
      "steps": [
        {
          "name": "Set up job",
          "status": "completed",
          "conclusion": "success",
          "number": 1,
          "started_at": "2026-11-05T18:12:27Z",
          "completed_at": "2026-11-05T18:12:29Z"
        },
        {
          "name": "Force LF checkout (hash parity với manifest)",
          "status": "completed",
          "conclusion": "success",
          "number": 2,
          "started_at": "2026-11-05T18:12:29Z",
          "completed_at": "2026-11-05T18:12:29Z"
        },
        {
          "name": "Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 3,
          "started_at": "2026-11-05T18:12:29Z",
          "completed_at": "2026-11-05T18:12:37Z"
        },
        {
          "name": "Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 4,
          "started_at": "2026-11-05T18:12:37Z",
          "completed_at": "2026-11-05T18:12:37Z"
        },
        {
          "name": "DUONG_NHANH - gom KHONG DO (job gate-nhanh-gop)",
          "status": "completed",
          "conclusion": "skipped",
          "number": 5,
          "started_at": "2026-11-05T18:12:37Z",
          "completed_at": "2026-11-05T18:12:37Z"
        },
        {
          "name": "DUONG_NHANH - liet ke buoc bo qua (job gate-nhanh-gop)",
          "status": "completed",
          "conclusion": "skipped",
          "number": 6,
          "started_at": "2026-11-05T18:12:37Z",
          "completed_at": "2026-11-05T18:12:37Z"
        },
        {
          "name": "Run actions/download-artifact@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 7,
          "started_at": "2026-11-05T18:12:37Z",
          "completed_at": "2026-11-05T18:12:39Z"
        },
        {
          "name": "gộp mảnh nhanh_don_duoc (targeted_mutant_gate)",
          "status": "completed",
          "conclusion": "success",
          "number": 8,
          "started_at": "2026-11-05T18:12:39Z",
          "completed_at": "2026-11-05T18:12:39Z"
        },
        {
          "name": "Post Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 15,
          "started_at": "2026-11-05T18:12:39Z",
          "completed_at": "2026-11-05T18:12:39Z"
        },
        {
          "name": "Post Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 16,
          "started_at": "2026-11-05T18:12:39Z",
          "completed_at": "2026-11-05T18:12:40Z"
        },
        {
          "name": "Complete job",
          "status": "completed",
          "conclusion": "success",
          "number": 17,
          "started_at": "2026-11-05T18:12:40Z",
          "completed_at": "2026-11-05T18:12:40Z"
        }
      ],
      "check_run_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127437121173",
      "labels": [
        "ubuntu-latest"
      ],
      "runner_id": 1000039497,
      "runner_name": "GitHub Actions 1000039497",
      "runner_group_id": 0,
      "runner_group_name": "GitHub Actions"
    },
    {
      "id": 127437301409,
      "run_id": 42081680387,
      "workflow_name": "gate",
      "head_branch": "agent/wp1240-g1-claude",
      "run_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42081680387",
      "run_attempt": 1,
      "node_id": "CR_kwDOTNeRjc8AAAAdq9rmoQ",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/actions/jobs/127437301409",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127437301409",
      "status": "completed",
      "conclusion": "success",
      "created_at": "2026-11-05T18:12:44Z",
      "started_at": "2026-11-05T18:12:46Z",
      "completed_at": "2026-11-05T18:29:14Z",
      "name": "gate-registry (ubuntu-latest)",
      "steps": [
        {
          "name": "Set up job",
          "status": "completed",
          "conclusion": "success",
          "number": 1,
          "started_at": "2026-11-05T18:12:47Z",
          "completed_at": "2026-11-05T18:12:47Z"
        },
        {
          "name": "Force LF checkout (hash parity với manifest)",
          "status": "completed",
          "conclusion": "success",
          "number": 2,
          "started_at": "2026-11-05T18:12:47Z",
          "completed_at": "2026-11-05T18:12:47Z"
        },
        {
          "name": "Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 3,
          "started_at": "2026-11-05T18:12:47Z",
          "completed_at": "2026-11-05T18:12:54Z"
        },
        {
          "name": "Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 4,
          "started_at": "2026-11-05T18:12:54Z",
          "completed_at": "2026-11-05T18:12:54Z"
        },
        {
          "name": "DUONG_NHANH - liet ke buoc bo qua (job gate-registry)",
          "status": "completed",
          "conclusion": "skipped",
          "number": 5,
          "started_at": "2026-11-05T18:12:54Z",
          "completed_at": "2026-11-05T18:12:54Z"
        },
        {
          "name": "cài PyYAML + jsonschema (cổng đăng lease + validator verdict cần)",
          "status": "completed",
          "conclusion": "success",
          "number": 6,
          "started_at": "2026-11-05T18:12:54Z",
          "completed_at": "2026-11-05T18:12:56Z"
        },
        {
          "name": "cài actionlint cho G5",
          "status": "completed",
          "conclusion": "success",
          "number": 7,
          "started_at": "2026-11-05T18:12:56Z",
          "completed_at": "2026-11-05T18:12:57Z"
        },
        {
          "name": "cài shellcheck cho G5 (cài xong đo lại)",
          "status": "completed",
          "conclusion": "success",
          "number": 8,
          "started_at": "2026-11-05T18:12:57Z",
          "completed_at": "2026-11-05T18:12:58Z"
        },
        {
          "name": "cài rg cho G5 (cài xong đo lại)",
          "status": "completed",
          "conclusion": "success",
          "number": 9,
          "started_at": "2026-11-05T18:12:58Z",
          "completed_at": "2026-11-05T18:13:03Z"
        },
        {
          "name": "G5 probe ban ke cong cu (#290; selftest T1..T8 chi o job gate, chot M6",
          "status": "completed",
          "conclusion": "success",
          "number": 10,
          "started_at": "2026-11-05T18:13:03Z",
          "completed_at": "2026-11-05T18:13:03Z"
        },
        {
          "name": "cài Ruff 0.15.15 và in probe dương",
          "status": "completed",
          "conclusion": "success",
          "number": 11,
          "started_at": "2026-11-05T18:13:03Z",
          "completed_at": "2026-11-05T18:13:04Z"
        },
        {
          "name": "test registry (phạm vi + các bộ chưa được nối)",
          "status": "completed",
          "conclusion": "success",
          "number": 12,
          "started_at": "2026-11-05T18:13:04Z",
          "completed_at": "2026-11-05T18:29:11Z"
        },
        {
          "name": "Post Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 23,
          "started_at": "2026-11-05T18:29:11Z",
          "completed_at": "2026-11-05T18:29:11Z"
        },
        {
          "name": "Post Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 24,
          "started_at": "2026-11-05T18:29:11Z",
          "completed_at": "2026-11-05T18:29:11Z"
        },
        {
          "name": "Complete job",
          "status": "completed",
          "conclusion": "success",
          "number": 25,
          "started_at": "2026-11-05T18:29:11Z",
          "completed_at": "2026-11-05T18:29:11Z"
        }
      ],
      "check_run_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127437301409",
      "labels": [
        "ubuntu-latest"
      ],
      "runner_id": 1000039498,
      "runner_name": "GitHub Actions 1000039498",
      "runner_group_id": 0,
      "runner_group_name": "GitHub Actions"
    },
    {
      "id": 127448292389,
      "run_id": 42081680387,
      "workflow_name": "gate",
      "head_branch": "agent/wp1240-g1-claude",
      "run_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42081680387",
      "run_attempt": 1,
      "node_id": "CR_kwDOTNeRjc8AAAAdrIKcJQ",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/actions/jobs/127448292389",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42081680387/job/127448292389",
      "status": "completed",
      "conclusion": "success",
      "created_at": "2026-11-05T18:32:23Z",
      "started_at": "2026-11-05T18:32:25Z",
      "completed_at": "2026-11-05T18:32:40Z",
      "name": "gate-cong-cu-gop (ubuntu-latest)",
      "steps": [
        {
          "name": "Set up job",
          "status": "completed",
          "conclusion": "success",
          "number": 1,
          "started_at": "2026-11-05T18:32:26Z",
          "completed_at": "2026-11-05T18:32:27Z"
        },
        {
          "name": "Force LF checkout (hash parity với manifest)",
          "status": "completed",
          "conclusion": "success",
          "number": 2,
          "started_at": "2026-11-05T18:32:27Z",
          "completed_at": "2026-11-05T18:32:27Z"
        },
        {
          "name": "Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 3,
          "started_at": "2026-11-05T18:32:27Z",
          "completed_at": "2026-11-05T18:32:32Z"
        },
        {
          "name": "Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 4,
          "started_at": "2026-11-05T18:32:32Z",
          "completed_at": "2026-11-05T18:32:32Z"
        },
        {
          "name": "cài PyYAML + jsonschema (cổng đăng lease + validator verdict cần)",
          "status": "completed",
          "conclusion": "success",
          "number": 5,
          "started_at": "2026-11-05T18:32:32Z",
          "completed_at": "2026-11-05T18:32:36Z"
        },
        {
          "name": "Run actions/download-artifact@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 6,
          "started_at": "2026-11-05T18:32:36Z",
          "completed_at": "2026-11-05T18:32:37Z"
        },
        {
          "name": "G5 gom manh ban kinh dot bien (#668)",
          "status": "completed",
          "conclusion": "success",
          "number": 7,
          "started_at": "2026-11-05T18:32:37Z",
          "completed_at": "2026-11-05T18:32:38Z"
        },
        {
          "name": "Post Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 13,
          "started_at": "2026-11-05T18:32:38Z",
          "completed_at": "2026-11-05T18:32:38Z"
        },
        {
          "name": "Post Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 14,
          "started_at": "2026-11-05T18:32:38Z",
          "completed_at": "2026-11-05T18:32:38Z"
        },
        {
          "name": "Complete job",
          "status": "completed",
          "conclusion": "success",
          "number": 15,
          "started_at": "2026-11-05T18:32:38Z",
          "completed_at": "2026-11-05T18:32:38Z"
        }
      ],
      "check_run_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127448292389",
      "labels": [
        "ubuntu-latest"
      ],
      "runner_id": 1000039545,
      "runner_name": "GitHub Actions 1000039545",
      "runner_group_id": 0,
      "runner_group_name": "GitHub Actions"
    }
  ]
}
~~~~ END wj.json

~~~~ BEGIN ddr.json
{
  "total_count": 1,
  "workflow_runs": [
    {
      "id": 42092343146,
      "name": "đột biến đủ (hằng tuần)",
      "node_id": "WFR_kwLOTNeRjc8AAAAJzOYvag",
      "head_branch": "agent/wp1240-g1-claude",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "path": ".github/workflows/ci-dot-bien-du.yml",
      "display_title": "đột biến đủ (hằng tuần)",
      "run_number": 38,
      "event": "workflow_dispatch",
      "status": "completed",
      "conclusion": "success",
      "workflow_id": 367998662,
      "check_suite_id": 114059822218,
      "check_suite_node_id": "CS_kwDOTNeRjc8AAAAajn7Eig",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42092343146",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42092343146",
      "pull_requests": [
        {
          "url": "https://api.github.com/repos/ducthangho/tra-luat/pulls/1249",
          "id": 5176379564,
          "number": 1249,
          "head": {
            "ref": "agent/wp1240-g1-claude",
            "sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          },
          "base": {
            "ref": "master",
            "sha": "3163f4d02a583787a9340c63a1f5eebd3780d970",
            "repo": {
              "id": 1289195917,
              "url": "https://api.github.com/repos/ducthangho/tra-luat",
              "name": "tra-luat"
            }
          }
        }
      ],
      "created_at": "2026-11-05T19:16:44Z",
      "updated_at": "2026-11-05T19:46:29Z",
      "actor": {
        "login": "ducthangho",
        "id": 12748935,
        "node_id": "MDQ6VXNlcjEyNzQ4OTM1",
        "avatar_url": "https://avatars.githubusercontent.com/u/12748935?v=4",
        "gravatar_id": "",
        "url": "https://api.github.com/users/ducthangho",
        "html_url": "https://github.com/ducthangho",
        "followers_url": "https://api.github.com/users/ducthangho/followers",
        "following_url": "https://api.github.com/users/ducthangho/following{/other_user}",
        "gists_url": "https://api.github.com/users/ducthangho/gists{/gist_id}",
        "starred_url": "https://api.github.com/users/ducthangho/starred{/owner}{/repo}",
        "subscriptions_url": "https://api.github.com/users/ducthangho/subscriptions",
        "organizations_url": "https://api.github.com/users/ducthangho/orgs",
        "repos_url": "https://api.github.com/users/ducthangho/repos",
        "events_url": "https://api.github.com/users/ducthangho/events{/privacy}",
        "received_events_url": "https://api.github.com/users/ducthangho/received_events",
        "type": "User",
        "user_view_type": "public",
        "site_admin": false
      },
      "run_attempt": 1,
      "referenced_workflows": [

      ],
      "run_started_at": "2026-11-05T19:16:44Z",
      "triggering_actor": {
        "login": "ducthangho",
        "id": 12748935,
        "node_id": "MDQ6VXNlcjEyNzQ4OTM1",
        "avatar_url": "https://avatars.githubusercontent.com/u/12748935?v=4",
        "gravatar_id": "",
        "url": "https://api.github.com/users/ducthangho",
        "html_url": "https://github.com/ducthangho",
        "followers_url": "https://api.github.com/users/ducthangho/followers",
        "following_url": "https://api.github.com/users/ducthangho/following{/other_user}",
        "gists_url": "https://api.github.com/users/ducthangho/gists{/gist_id}",
        "starred_url": "https://api.github.com/users/ducthangho/starred{/owner}{/repo}",
        "subscriptions_url": "https://api.github.com/users/ducthangho/subscriptions",
        "organizations_url": "https://api.github.com/users/ducthangho/orgs",
        "repos_url": "https://api.github.com/users/ducthangho/repos",
        "events_url": "https://api.github.com/users/ducthangho/events{/privacy}",
        "received_events_url": "https://api.github.com/users/ducthangho/received_events",
        "type": "User",
        "user_view_type": "public",
        "site_admin": false
      },
      "jobs_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42092343146/jobs",
      "logs_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42092343146/logs",
      "check_suite_url": "https://api.github.com/repos/ducthangho/tra-luat/check-suites/114059822218",
      "artifacts_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42092343146/artifacts",
      "cancel_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42092343146/cancel",
      "rerun_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42092343146/rerun",
      "previous_attempt_url": null,
      "workflow_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/workflows/367998662",
      "head_commit": {
        "id": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
        "tree_id": "1b18da0468a9b04a2d0d567935157d17f3c5111f",
        "message": "wp1240 ASSURANCE-81-MODEL-EFFORT-TUY-CHON r1: model/effort reviewer thành trường ghi nếu đo được\n\n- ADR-0065 (Accepted, quyết định chủ kho #1240 issuecomment-6662892793, Q1/Q2 issuecomment-6663218706).\n- PROTOCOL §8.1: model/effort phục vụ là trường ghi nếu đo được; KHONG_DO_DUOC không làm assurance\n  CHUA_DAT, không chặn landed; bỏ câu \"cùng model, effort cao hơn\"; thu hẹp câu nhận dạng về\n  provider/surface/transport/session/sandbox. §8 mục 1: họ model theo identity provider. §20: dòng ADR-0065.\n- ops/land_evidence_nguon.py L7: chỉ sandbox_mode bắt buộc measured; model/effort vắng được, có mặt thì\n  measured hoặc not_measured, rác vẫn ĐỎ. MIEN_TRU_L7 giữ nguyên.\n- ops/land_evidence_nguon_test.py: c17 cập nhật, c23 mới (A4–A6), đột biến m1–m3 + 7 biên. 23/23, 116/116.\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_015Gtxra1nVwvZnd2Xy32KWw",
        "timestamp": "2026-11-05T17:46:20Z",
        "author": {
          "name": "Claude",
          "email": "noreply@anthropic.com"
        },
        "committer": {
          "name": "Claude",
          "email": "noreply@anthropic.com"
        }
      },
      "repository": {
        "id": 1289195917,
        "node_id": "R_kgDOTNeRjQ",
        "name": "tra-luat",
        "full_name": "ducthangho/tra-luat",
        "private": false,
        "owner": {
          "login": "ducthangho",
          "id": 12748935,
          "node_id": "MDQ6VXNlcjEyNzQ4OTM1",
          "avatar_url": "https://avatars.githubusercontent.com/u/12748935?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/ducthangho",
          "html_url": "https://github.com/ducthangho",
          "followers_url": "https://api.github.com/users/ducthangho/followers",
          "following_url": "https://api.github.com/users/ducthangho/following{/other_user}",
          "gists_url": "https://api.github.com/users/ducthangho/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/ducthangho/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/ducthangho/subscriptions",
          "organizations_url": "https://api.github.com/users/ducthangho/orgs",
          "repos_url": "https://api.github.com/users/ducthangho/repos",
          "events_url": "https://api.github.com/users/ducthangho/events{/privacy}",
          "received_events_url": "https://api.github.com/users/ducthangho/received_events",
          "type": "User",
          "user_view_type": "public",
          "site_admin": false
        },
        "html_url": "https://github.com/ducthangho/tra-luat",
        "description": null,
        "fork": false,
        "url": "https://api.github.com/repos/ducthangho/tra-luat",
        "forks_url": "https://api.github.com/repos/ducthangho/tra-luat/forks",
        "keys_url": "https://api.github.com/repos/ducthangho/tra-luat/keys{/key_id}",
        "collaborators_url": "https://api.github.com/repos/ducthangho/tra-luat/collaborators{/collaborator}",
        "teams_url": "https://api.github.com/repos/ducthangho/tra-luat/teams",
        "hooks_url": "https://api.github.com/repos/ducthangho/tra-luat/hooks",
        "issue_events_url": "https://api.github.com/repos/ducthangho/tra-luat/issues/events{/number}",
        "events_url": "https://api.github.com/repos/ducthangho/tra-luat/events",
        "assignees_url": "https://api.github.com/repos/ducthangho/tra-luat/assignees{/user}",
        "branches_url": "https://api.github.com/repos/ducthangho/tra-luat/branches{/branch}",
        "tags_url": "https://api.github.com/repos/ducthangho/tra-luat/tags",
        "blobs_url": "https://api.github.com/repos/ducthangho/tra-luat/git/blobs{/sha}",
        "git_tags_url": "https://api.github.com/repos/ducthangho/tra-luat/git/tags{/sha}",
        "git_refs_url": "https://api.github.com/repos/ducthangho/tra-luat/git/refs{/sha}",
        "trees_url": "https://api.github.com/repos/ducthangho/tra-luat/git/trees{/sha}",
        "statuses_url": "https://api.github.com/repos/ducthangho/tra-luat/statuses/{sha}",
        "languages_url": "https://api.github.com/repos/ducthangho/tra-luat/languages",
        "stargazers_url": "https://api.github.com/repos/ducthangho/tra-luat/stargazers",
        "contributors_url": "https://api.github.com/repos/ducthangho/tra-luat/contributors",
        "subscribers_url": "https://api.github.com/repos/ducthangho/tra-luat/subscribers",
        "subscription_url": "https://api.github.com/repos/ducthangho/tra-luat/subscription",
        "commits_url": "https://api.github.com/repos/ducthangho/tra-luat/commits{/sha}",
        "git_commits_url": "https://api.github.com/repos/ducthangho/tra-luat/git/commits{/sha}",
        "comments_url": "https://api.github.com/repos/ducthangho/tra-luat/comments{/number}",
        "issue_comment_url": "https://api.github.com/repos/ducthangho/tra-luat/issues/comments{/number}",
        "contents_url": "https://api.github.com/repos/ducthangho/tra-luat/contents/{+path}",
        "compare_url": "https://api.github.com/repos/ducthangho/tra-luat/compare/{base}...{head}",
        "merges_url": "https://api.github.com/repos/ducthangho/tra-luat/merges",
        "archive_url": "https://api.github.com/repos/ducthangho/tra-luat/{archive_format}{/ref}",
        "downloads_url": "https://api.github.com/repos/ducthangho/tra-luat/downloads",
        "issues_url": "https://api.github.com/repos/ducthangho/tra-luat/issues{/number}",
        "pulls_url": "https://api.github.com/repos/ducthangho/tra-luat/pulls{/number}",
        "milestones_url": "https://api.github.com/repos/ducthangho/tra-luat/milestones{/number}",
        "notifications_url": "https://api.github.com/repos/ducthangho/tra-luat/notifications{?since,all,participating}",
        "labels_url": "https://api.github.com/repos/ducthangho/tra-luat/labels{/name}",
        "releases_url": "https://api.github.com/repos/ducthangho/tra-luat/releases{/id}",
        "deployments_url": "https://api.github.com/repos/ducthangho/tra-luat/deployments"
      },
      "head_repository": {
        "id": 1289195917,
        "node_id": "R_kgDOTNeRjQ",
        "name": "tra-luat",
        "full_name": "ducthangho/tra-luat",
        "private": false,
        "owner": {
          "login": "ducthangho",
          "id": 12748935,
          "node_id": "MDQ6VXNlcjEyNzQ4OTM1",
          "avatar_url": "https://avatars.githubusercontent.com/u/12748935?v=4",
          "gravatar_id": "",
          "url": "https://api.github.com/users/ducthangho",
          "html_url": "https://github.com/ducthangho",
          "followers_url": "https://api.github.com/users/ducthangho/followers",
          "following_url": "https://api.github.com/users/ducthangho/following{/other_user}",
          "gists_url": "https://api.github.com/users/ducthangho/gists{/gist_id}",
          "starred_url": "https://api.github.com/users/ducthangho/starred{/owner}{/repo}",
          "subscriptions_url": "https://api.github.com/users/ducthangho/subscriptions",
          "organizations_url": "https://api.github.com/users/ducthangho/orgs",
          "repos_url": "https://api.github.com/users/ducthangho/repos",
          "events_url": "https://api.github.com/users/ducthangho/events{/privacy}",
          "received_events_url": "https://api.github.com/users/ducthangho/received_events",
          "type": "User",
          "user_view_type": "public",
          "site_admin": false
        },
        "html_url": "https://github.com/ducthangho/tra-luat",
        "description": null,
        "fork": false,
        "url": "https://api.github.com/repos/ducthangho/tra-luat",
        "forks_url": "https://api.github.com/repos/ducthangho/tra-luat/forks",
        "keys_url": "https://api.github.com/repos/ducthangho/tra-luat/keys{/key_id}",
        "collaborators_url": "https://api.github.com/repos/ducthangho/tra-luat/collaborators{/collaborator}",
        "teams_url": "https://api.github.com/repos/ducthangho/tra-luat/teams",
        "hooks_url": "https://api.github.com/repos/ducthangho/tra-luat/hooks",
        "issue_events_url": "https://api.github.com/repos/ducthangho/tra-luat/issues/events{/number}",
        "events_url": "https://api.github.com/repos/ducthangho/tra-luat/events",
        "assignees_url": "https://api.github.com/repos/ducthangho/tra-luat/assignees{/user}",
        "branches_url": "https://api.github.com/repos/ducthangho/tra-luat/branches{/branch}",
        "tags_url": "https://api.github.com/repos/ducthangho/tra-luat/tags",
        "blobs_url": "https://api.github.com/repos/ducthangho/tra-luat/git/blobs{/sha}",
        "git_tags_url": "https://api.github.com/repos/ducthangho/tra-luat/git/tags{/sha}",
        "git_refs_url": "https://api.github.com/repos/ducthangho/tra-luat/git/refs{/sha}",
        "trees_url": "https://api.github.com/repos/ducthangho/tra-luat/git/trees{/sha}",
        "statuses_url": "https://api.github.com/repos/ducthangho/tra-luat/statuses/{sha}",
        "languages_url": "https://api.github.com/repos/ducthangho/tra-luat/languages",
        "stargazers_url": "https://api.github.com/repos/ducthangho/tra-luat/stargazers",
        "contributors_url": "https://api.github.com/repos/ducthangho/tra-luat/contributors",
        "subscribers_url": "https://api.github.com/repos/ducthangho/tra-luat/subscribers",
        "subscription_url": "https://api.github.com/repos/ducthangho/tra-luat/subscription",
        "commits_url": "https://api.github.com/repos/ducthangho/tra-luat/commits{/sha}",
        "git_commits_url": "https://api.github.com/repos/ducthangho/tra-luat/git/commits{/sha}",
        "comments_url": "https://api.github.com/repos/ducthangho/tra-luat/comments{/number}",
        "issue_comment_url": "https://api.github.com/repos/ducthangho/tra-luat/issues/comments{/number}",
        "contents_url": "https://api.github.com/repos/ducthangho/tra-luat/contents/{+path}",
        "compare_url": "https://api.github.com/repos/ducthangho/tra-luat/compare/{base}...{head}",
        "merges_url": "https://api.github.com/repos/ducthangho/tra-luat/merges",
        "archive_url": "https://api.github.com/repos/ducthangho/tra-luat/{archive_format}{/ref}",
        "downloads_url": "https://api.github.com/repos/ducthangho/tra-luat/downloads",
        "issues_url": "https://api.github.com/repos/ducthangho/tra-luat/issues{/number}",
        "pulls_url": "https://api.github.com/repos/ducthangho/tra-luat/pulls{/number}",
        "milestones_url": "https://api.github.com/repos/ducthangho/tra-luat/milestones{/number}",
        "notifications_url": "https://api.github.com/repos/ducthangho/tra-luat/notifications{?since,all,participating}",
        "labels_url": "https://api.github.com/repos/ducthangho/tra-luat/labels{/name}",
        "releases_url": "https://api.github.com/repos/ducthangho/tra-luat/releases{/id}",
        "deployments_url": "https://api.github.com/repos/ducthangho/tra-luat/deployments"
      }
    }
  ]
}
~~~~ END ddr.json

~~~~ BEGIN ddj.json
{
  "total_count": 10,
  "jobs": [
    {
      "id": 127473376216,
      "run_id": 42092343146,
      "workflow_name": "đột biến đủ (hằng tuần)",
      "head_branch": "agent/wp1240-g1-claude",
      "run_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42092343146",
      "run_attempt": 1,
      "node_id": "CR_kwDOTNeRjc8AAAAdrgFb2A",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/actions/jobs/127473376216",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42092343146/job/127473376216",
      "status": "completed",
      "conclusion": "success",
      "created_at": "2026-11-05T19:16:46Z",
      "started_at": "2026-11-05T19:16:48Z",
      "completed_at": "2026-11-05T19:36:48Z",
      "name": "dot-bien-du",
      "steps": [
        {
          "name": "Set up job",
          "status": "completed",
          "conclusion": "success",
          "number": 1,
          "started_at": "2026-11-05T19:16:49Z",
          "completed_at": "2026-11-05T19:16:49Z"
        },
        {
          "name": "Force LF checkout (hash parity với manifest)",
          "status": "completed",
          "conclusion": "success",
          "number": 2,
          "started_at": "2026-11-05T19:16:49Z",
          "completed_at": "2026-11-05T19:16:49Z"
        },
        {
          "name": "Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 3,
          "started_at": "2026-11-05T19:16:49Z",
          "completed_at": "2026-11-05T19:17:05Z"
        },
        {
          "name": "Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 4,
          "started_at": "2026-11-05T19:17:05Z",
          "completed_at": "2026-11-05T19:17:05Z"
        },
        {
          "name": "cài PyYAML + jsonschema (cổng đăng lease + validator verdict cần)",
          "status": "completed",
          "conclusion": "success",
          "number": 5,
          "started_at": "2026-11-05T19:17:05Z",
          "completed_at": "2026-11-05T19:17:06Z"
        },
        {
          "name": "cài actionlint cho G5",
          "status": "completed",
          "conclusion": "success",
          "number": 6,
          "started_at": "2026-11-05T19:17:06Z",
          "completed_at": "2026-11-05T19:17:06Z"
        },
        {
          "name": "cài shellcheck cho G5 (cài xong đo lại)",
          "status": "completed",
          "conclusion": "success",
          "number": 7,
          "started_at": "2026-11-05T19:17:06Z",
          "completed_at": "2026-11-05T19:17:08Z"
        },
        {
          "name": "cài rg cho G5 (cài xong đo lại)",
          "status": "completed",
          "conclusion": "success",
          "number": 8,
          "started_at": "2026-11-05T19:17:08Z",
          "completed_at": "2026-11-05T19:17:51Z"
        },
        {
          "name": "G5 probe ban ke cong cu (#290; selftest T1..T8 chi o job gate, chot M6",
          "status": "completed",
          "conclusion": "success",
          "number": 9,
          "started_at": "2026-11-05T19:17:51Z",
          "completed_at": "2026-11-05T19:17:51Z"
        },
        {
          "name": "cài Ruff 0.15.15 và in probe dương",
          "status": "completed",
          "conclusion": "success",
          "number": 10,
          "started_at": "2026-11-05T19:17:51Z",
          "completed_at": "2026-11-05T19:17:52Z"
        },
        {
          "name": "test registry (phạm vi + các bộ chưa được nối)",
          "status": "completed",
          "conclusion": "success",
          "number": 11,
          "started_at": "2026-11-05T19:17:52Z",
          "completed_at": "2026-11-05T19:36:44Z"
        },
        {
          "name": "Post Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 21,
          "started_at": "2026-11-05T19:36:44Z",
          "completed_at": "2026-11-05T19:36:44Z"
        },
        {
          "name": "Post Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 22,
          "started_at": "2026-11-05T19:36:44Z",
          "completed_at": "2026-11-05T19:36:44Z"
        },
        {
          "name": "Complete job",
          "status": "completed",
          "conclusion": "success",
          "number": 23,
          "started_at": "2026-11-05T19:36:44Z",
          "completed_at": "2026-11-05T19:36:44Z"
        }
      ],
      "check_run_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127473376216",
      "labels": [
        "ubuntu-latest"
      ],
      "runner_id": 1000039620,
      "runner_name": "GitHub Actions 1000039620",
      "runner_group_id": 0,
      "runner_group_name": "GitHub Actions"
    },
    {
      "id": 127473376345,
      "run_id": 42092343146,
      "workflow_name": "đột biến đủ (hằng tuần)",
      "head_branch": "agent/wp1240-g1-claude",
      "run_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42092343146",
      "run_attempt": 1,
      "node_id": "CR_kwDOTNeRjc8AAAAdrgFcWQ",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/actions/jobs/127473376345",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42092343146/job/127473376345",
      "status": "completed",
      "conclusion": "success",
      "created_at": "2026-11-05T19:16:46Z",
      "started_at": "2026-11-05T19:16:48Z",
      "completed_at": "2026-11-05T19:44:16Z",
      "name": "dot-bien-manh (6)",
      "steps": [
        {
          "name": "Set up job",
          "status": "completed",
          "conclusion": "success",
          "number": 1,
          "started_at": "2026-11-05T19:16:48Z",
          "completed_at": "2026-11-05T19:16:49Z"
        },
        {
          "name": "Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 2,
          "started_at": "2026-11-05T19:16:49Z",
          "completed_at": "2026-11-05T19:16:53Z"
        },
        {
          "name": "Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 3,
          "started_at": "2026-11-05T19:16:53Z",
          "completed_at": "2026-11-05T19:16:54Z"
        },
        {
          "name": "đột biến một mảnh",
          "status": "completed",
          "conclusion": "success",
          "number": 4,
          "started_at": "2026-11-05T19:16:54Z",
          "completed_at": "2026-11-05T19:44:11Z"
        },
        {
          "name": "Run actions/upload-artifact@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 5,
          "started_at": "2026-11-05T19:44:11Z",
          "completed_at": "2026-11-05T19:44:13Z"
        },
        {
          "name": "Post Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 9,
          "started_at": "2026-11-05T19:44:13Z",
          "completed_at": "2026-11-05T19:44:13Z"
        },
        {
          "name": "Post Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 10,
          "started_at": "2026-11-05T19:44:13Z",
          "completed_at": "2026-11-05T19:44:13Z"
        },
        {
          "name": "Complete job",
          "status": "completed",
          "conclusion": "success",
          "number": 11,
          "started_at": "2026-11-05T19:44:13Z",
          "completed_at": "2026-11-05T19:44:13Z"
        }
      ],
      "check_run_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127473376345",
      "labels": [
        "ubuntu-latest"
      ],
      "runner_id": 1000039619,
      "runner_name": "GitHub Actions 1000039619",
      "runner_group_id": 0,
      "runner_group_name": "GitHub Actions"
    },
    {
      "id": 127473376385,
      "run_id": 42092343146,
      "workflow_name": "đột biến đủ (hằng tuần)",
      "head_branch": "agent/wp1240-g1-claude",
      "run_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42092343146",
      "run_attempt": 1,
      "node_id": "CR_kwDOTNeRjc8AAAAdrgFcgQ",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/actions/jobs/127473376385",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42092343146/job/127473376385",
      "status": "completed",
      "conclusion": "success",
      "created_at": "2026-11-05T19:16:46Z",
      "started_at": "2026-11-05T19:16:48Z",
      "completed_at": "2026-11-05T19:44:10Z",
      "name": "dot-bien-manh (4)",
      "steps": [
        {
          "name": "Set up job",
          "status": "completed",
          "conclusion": "success",
          "number": 1,
          "started_at": "2026-11-05T19:16:49Z",
          "completed_at": "2026-11-05T19:16:49Z"
        },
        {
          "name": "Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 2,
          "started_at": "2026-11-05T19:16:49Z",
          "completed_at": "2026-11-05T19:16:58Z"
        },
        {
          "name": "Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 3,
          "started_at": "2026-11-05T19:16:58Z",
          "completed_at": "2026-11-05T19:16:58Z"
        },
        {
          "name": "đột biến một mảnh",
          "status": "completed",
          "conclusion": "success",
          "number": 4,
          "started_at": "2026-11-05T19:16:58Z",
          "completed_at": "2026-11-05T19:44:05Z"
        },
        {
          "name": "Run actions/upload-artifact@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 5,
          "started_at": "2026-11-05T19:44:05Z",
          "completed_at": "2026-11-05T19:44:07Z"
        },
        {
          "name": "Post Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 9,
          "started_at": "2026-11-05T19:44:07Z",
          "completed_at": "2026-11-05T19:44:07Z"
        },
        {
          "name": "Post Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 10,
          "started_at": "2026-11-05T19:44:07Z",
          "completed_at": "2026-11-05T19:44:07Z"
        },
        {
          "name": "Complete job",
          "status": "completed",
          "conclusion": "success",
          "number": 11,
          "started_at": "2026-11-05T19:44:07Z",
          "completed_at": "2026-11-05T19:44:07Z"
        }
      ],
      "check_run_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127473376385",
      "labels": [
        "ubuntu-latest"
      ],
      "runner_id": 1000039621,
      "runner_name": "GitHub Actions 1000039621",
      "runner_group_id": 0,
      "runner_group_name": "GitHub Actions"
    },
    {
      "id": 127473376504,
      "run_id": 42092343146,
      "workflow_name": "đột biến đủ (hằng tuần)",
      "head_branch": "agent/wp1240-g1-claude",
      "run_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42092343146",
      "run_attempt": 1,
      "node_id": "CR_kwDOTNeRjc8AAAAdrgFc-A",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/actions/jobs/127473376504",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42092343146/job/127473376504",
      "status": "completed",
      "conclusion": "success",
      "created_at": "2026-11-05T19:16:46Z",
      "started_at": "2026-11-05T19:16:48Z",
      "completed_at": "2026-11-05T19:45:29Z",
      "name": "dot-bien-manh (3)",
      "steps": [
        {
          "name": "Set up job",
          "status": "completed",
          "conclusion": "success",
          "number": 1,
          "started_at": "2026-11-05T19:16:50Z",
          "completed_at": "2026-11-05T19:16:50Z"
        },
        {
          "name": "Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 2,
          "started_at": "2026-11-05T19:16:50Z",
          "completed_at": "2026-11-05T19:16:54Z"
        },
        {
          "name": "Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 3,
          "started_at": "2026-11-05T19:16:54Z",
          "completed_at": "2026-11-05T19:16:54Z"
        },
        {
          "name": "đột biến một mảnh",
          "status": "completed",
          "conclusion": "success",
          "number": 4,
          "started_at": "2026-11-05T19:16:54Z",
          "completed_at": "2026-11-05T19:45:26Z"
        },
        {
          "name": "Run actions/upload-artifact@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 5,
          "started_at": "2026-11-05T19:45:26Z",
          "completed_at": "2026-11-05T19:45:27Z"
        },
        {
          "name": "Post Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 9,
          "started_at": "2026-11-05T19:45:27Z",
          "completed_at": "2026-11-05T19:45:27Z"
        },
        {
          "name": "Post Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 10,
          "started_at": "2026-11-05T19:45:27Z",
          "completed_at": "2026-11-05T19:45:27Z"
        },
        {
          "name": "Complete job",
          "status": "completed",
          "conclusion": "success",
          "number": 11,
          "started_at": "2026-11-05T19:45:27Z",
          "completed_at": "2026-11-05T19:45:27Z"
        }
      ],
      "check_run_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127473376504",
      "labels": [
        "ubuntu-latest"
      ],
      "runner_id": 1000039623,
      "runner_name": "GitHub Actions 1000039623",
      "runner_group_id": 0,
      "runner_group_name": "GitHub Actions"
    },
    {
      "id": 127473376653,
      "run_id": 42092343146,
      "workflow_name": "đột biến đủ (hằng tuần)",
      "head_branch": "agent/wp1240-g1-claude",
      "run_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42092343146",
      "run_attempt": 1,
      "node_id": "CR_kwDOTNeRjc8AAAAdrgFdjQ",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/actions/jobs/127473376653",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42092343146/job/127473376653",
      "status": "completed",
      "conclusion": "success",
      "created_at": "2026-11-05T19:16:46Z",
      "started_at": "2026-11-05T19:16:48Z",
      "completed_at": "2026-11-05T19:43:50Z",
      "name": "dot-bien-manh (0)",
      "steps": [
        {
          "name": "Set up job",
          "status": "completed",
          "conclusion": "success",
          "number": 1,
          "started_at": "2026-11-05T19:16:49Z",
          "completed_at": "2026-11-05T19:16:50Z"
        },
        {
          "name": "Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 2,
          "started_at": "2026-11-05T19:16:50Z",
          "completed_at": "2026-11-05T19:16:54Z"
        },
        {
          "name": "Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 3,
          "started_at": "2026-11-05T19:16:54Z",
          "completed_at": "2026-11-05T19:16:54Z"
        },
        {
          "name": "đột biến một mảnh",
          "status": "completed",
          "conclusion": "success",
          "number": 4,
          "started_at": "2026-11-05T19:16:54Z",
          "completed_at": "2026-11-05T19:43:46Z"
        },
        {
          "name": "Run actions/upload-artifact@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 5,
          "started_at": "2026-11-05T19:43:46Z",
          "completed_at": "2026-11-05T19:43:48Z"
        },
        {
          "name": "Post Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 9,
          "started_at": "2026-11-05T19:43:48Z",
          "completed_at": "2026-11-05T19:43:48Z"
        },
        {
          "name": "Post Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 10,
          "started_at": "2026-11-05T19:43:48Z",
          "completed_at": "2026-11-05T19:43:48Z"
        },
        {
          "name": "Complete job",
          "status": "completed",
          "conclusion": "success",
          "number": 11,
          "started_at": "2026-11-05T19:43:48Z",
          "completed_at": "2026-11-05T19:43:48Z"
        }
      ],
      "check_run_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127473376653",
      "labels": [
        "ubuntu-latest"
      ],
      "runner_id": 1000039622,
      "runner_name": "GitHub Actions 1000039622",
      "runner_group_id": 0,
      "runner_group_name": "GitHub Actions"
    },
    {
      "id": 127473376875,
      "run_id": 42092343146,
      "workflow_name": "đột biến đủ (hằng tuần)",
      "head_branch": "agent/wp1240-g1-claude",
      "run_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42092343146",
      "run_attempt": 1,
      "node_id": "CR_kwDOTNeRjc8AAAAdrgFeaw",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/actions/jobs/127473376875",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42092343146/job/127473376875",
      "status": "completed",
      "conclusion": "success",
      "created_at": "2026-11-05T19:16:46Z",
      "started_at": "2026-11-05T19:16:48Z",
      "completed_at": "2026-11-05T19:42:12Z",
      "name": "dot-bien-manh (1)",
      "steps": [
        {
          "name": "Set up job",
          "status": "completed",
          "conclusion": "success",
          "number": 1,
          "started_at": "2026-11-05T19:16:48Z",
          "completed_at": "2026-11-05T19:16:49Z"
        },
        {
          "name": "Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 2,
          "started_at": "2026-11-05T19:16:49Z",
          "completed_at": "2026-11-05T19:16:53Z"
        },
        {
          "name": "Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 3,
          "started_at": "2026-11-05T19:16:53Z",
          "completed_at": "2026-11-05T19:16:53Z"
        },
        {
          "name": "đột biến một mảnh",
          "status": "completed",
          "conclusion": "success",
          "number": 4,
          "started_at": "2026-11-05T19:16:53Z",
          "completed_at": "2026-11-05T19:42:09Z"
        },
        {
          "name": "Run actions/upload-artifact@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 5,
          "started_at": "2026-11-05T19:42:09Z",
          "completed_at": "2026-11-05T19:42:10Z"
        },
        {
          "name": "Post Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 9,
          "started_at": "2026-11-05T19:42:10Z",
          "completed_at": "2026-11-05T19:42:10Z"
        },
        {
          "name": "Post Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 10,
          "started_at": "2026-11-05T19:42:10Z",
          "completed_at": "2026-11-05T19:42:10Z"
        },
        {
          "name": "Complete job",
          "status": "completed",
          "conclusion": "success",
          "number": 11,
          "started_at": "2026-11-05T19:42:10Z",
          "completed_at": "2026-11-05T19:42:10Z"
        }
      ],
      "check_run_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127473376875",
      "labels": [
        "ubuntu-latest"
      ],
      "runner_id": 1000039624,
      "runner_name": "GitHub Actions 1000039624",
      "runner_group_id": 0,
      "runner_group_name": "GitHub Actions"
    },
    {
      "id": 127473376921,
      "run_id": 42092343146,
      "workflow_name": "đột biến đủ (hằng tuần)",
      "head_branch": "agent/wp1240-g1-claude",
      "run_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42092343146",
      "run_attempt": 1,
      "node_id": "CR_kwDOTNeRjc8AAAAdrgFemQ",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/actions/jobs/127473376921",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42092343146/job/127473376921",
      "status": "completed",
      "conclusion": "success",
      "created_at": "2026-11-05T19:16:46Z",
      "started_at": "2026-11-05T19:16:48Z",
      "completed_at": "2026-11-05T19:45:12Z",
      "name": "dot-bien-manh (7)",
      "steps": [
        {
          "name": "Set up job",
          "status": "completed",
          "conclusion": "success",
          "number": 1,
          "started_at": "2026-11-05T19:16:48Z",
          "completed_at": "2026-11-05T19:16:49Z"
        },
        {
          "name": "Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 2,
          "started_at": "2026-11-05T19:16:49Z",
          "completed_at": "2026-11-05T19:16:53Z"
        },
        {
          "name": "Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 3,
          "started_at": "2026-11-05T19:16:53Z",
          "completed_at": "2026-11-05T19:16:54Z"
        },
        {
          "name": "đột biến một mảnh",
          "status": "completed",
          "conclusion": "success",
          "number": 4,
          "started_at": "2026-11-05T19:16:54Z",
          "completed_at": "2026-11-05T19:45:09Z"
        },
        {
          "name": "Run actions/upload-artifact@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 5,
          "started_at": "2026-11-05T19:45:09Z",
          "completed_at": "2026-11-05T19:45:10Z"
        },
        {
          "name": "Post Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 9,
          "started_at": "2026-11-05T19:45:10Z",
          "completed_at": "2026-11-05T19:45:10Z"
        },
        {
          "name": "Post Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 10,
          "started_at": "2026-11-05T19:45:10Z",
          "completed_at": "2026-11-05T19:45:11Z"
        },
        {
          "name": "Complete job",
          "status": "completed",
          "conclusion": "success",
          "number": 11,
          "started_at": "2026-11-05T19:45:11Z",
          "completed_at": "2026-11-05T19:45:11Z"
        }
      ],
      "check_run_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127473376921",
      "labels": [
        "ubuntu-latest"
      ],
      "runner_id": 1000039626,
      "runner_name": "GitHub Actions 1000039626",
      "runner_group_id": 0,
      "runner_group_name": "GitHub Actions"
    },
    {
      "id": 127473377134,
      "run_id": 42092343146,
      "workflow_name": "đột biến đủ (hằng tuần)",
      "head_branch": "agent/wp1240-g1-claude",
      "run_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42092343146",
      "run_attempt": 1,
      "node_id": "CR_kwDOTNeRjc8AAAAdrgFfbg",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/actions/jobs/127473377134",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42092343146/job/127473377134",
      "status": "completed",
      "conclusion": "success",
      "created_at": "2026-11-05T19:16:46Z",
      "started_at": "2026-11-05T19:16:48Z",
      "completed_at": "2026-11-05T19:44:04Z",
      "name": "dot-bien-manh (2)",
      "steps": [
        {
          "name": "Set up job",
          "status": "completed",
          "conclusion": "success",
          "number": 1,
          "started_at": "2026-11-05T19:16:49Z",
          "completed_at": "2026-11-05T19:16:49Z"
        },
        {
          "name": "Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 2,
          "started_at": "2026-11-05T19:16:49Z",
          "completed_at": "2026-11-05T19:16:54Z"
        },
        {
          "name": "Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 3,
          "started_at": "2026-11-05T19:16:54Z",
          "completed_at": "2026-11-05T19:16:54Z"
        },
        {
          "name": "đột biến một mảnh",
          "status": "completed",
          "conclusion": "success",
          "number": 4,
          "started_at": "2026-11-05T19:16:54Z",
          "completed_at": "2026-11-05T19:44:01Z"
        },
        {
          "name": "Run actions/upload-artifact@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 5,
          "started_at": "2026-11-05T19:44:01Z",
          "completed_at": "2026-11-05T19:44:02Z"
        },
        {
          "name": "Post Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 9,
          "started_at": "2026-11-05T19:44:02Z",
          "completed_at": "2026-11-05T19:44:02Z"
        },
        {
          "name": "Post Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 10,
          "started_at": "2026-11-05T19:44:02Z",
          "completed_at": "2026-11-05T19:44:02Z"
        },
        {
          "name": "Complete job",
          "status": "completed",
          "conclusion": "success",
          "number": 11,
          "started_at": "2026-11-05T19:44:02Z",
          "completed_at": "2026-11-05T19:44:02Z"
        }
      ],
      "check_run_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127473377134",
      "labels": [
        "ubuntu-latest"
      ],
      "runner_id": 1000039625,
      "runner_name": "GitHub Actions 1000039625",
      "runner_group_id": 0,
      "runner_group_name": "GitHub Actions"
    },
    {
      "id": 127473377832,
      "run_id": 42092343146,
      "workflow_name": "đột biến đủ (hằng tuần)",
      "head_branch": "agent/wp1240-g1-claude",
      "run_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42092343146",
      "run_attempt": 1,
      "node_id": "CR_kwDOTNeRjc8AAAAdrgFiKA",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/actions/jobs/127473377832",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42092343146/job/127473377832",
      "status": "completed",
      "conclusion": "success",
      "created_at": "2026-11-05T19:16:46Z",
      "started_at": "2026-11-05T19:16:48Z",
      "completed_at": "2026-11-05T19:46:16Z",
      "name": "dot-bien-manh (5)",
      "steps": [
        {
          "name": "Set up job",
          "status": "completed",
          "conclusion": "success",
          "number": 1,
          "started_at": "2026-11-05T19:16:48Z",
          "completed_at": "2026-11-05T19:16:49Z"
        },
        {
          "name": "Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 2,
          "started_at": "2026-11-05T19:16:49Z",
          "completed_at": "2026-11-05T19:16:53Z"
        },
        {
          "name": "Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 3,
          "started_at": "2026-11-05T19:16:53Z",
          "completed_at": "2026-11-05T19:16:54Z"
        },
        {
          "name": "đột biến một mảnh",
          "status": "completed",
          "conclusion": "success",
          "number": 4,
          "started_at": "2026-11-05T19:16:54Z",
          "completed_at": "2026-11-05T19:46:13Z"
        },
        {
          "name": "Run actions/upload-artifact@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 5,
          "started_at": "2026-11-05T19:46:13Z",
          "completed_at": "2026-11-05T19:46:14Z"
        },
        {
          "name": "Post Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 9,
          "started_at": "2026-11-05T19:46:14Z",
          "completed_at": "2026-11-05T19:46:14Z"
        },
        {
          "name": "Post Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 10,
          "started_at": "2026-11-05T19:46:14Z",
          "completed_at": "2026-11-05T19:46:14Z"
        },
        {
          "name": "Complete job",
          "status": "completed",
          "conclusion": "success",
          "number": 11,
          "started_at": "2026-11-05T19:46:14Z",
          "completed_at": "2026-11-05T19:46:14Z"
        }
      ],
      "check_run_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127473377832",
      "labels": [
        "ubuntu-latest"
      ],
      "runner_id": 1000039627,
      "runner_name": "GitHub Actions 1000039627",
      "runner_group_id": 0,
      "runner_group_name": "GitHub Actions"
    },
    {
      "id": 127489703361,
      "run_id": 42092343146,
      "workflow_name": "đột biến đủ (hằng tuần)",
      "head_branch": "agent/wp1240-g1-claude",
      "run_url": "https://api.github.com/repos/ducthangho/tra-luat/actions/runs/42092343146",
      "run_attempt": 1,
      "node_id": "CR_kwDOTNeRjc8AAAAdrvp9wQ",
      "head_sha": "ecd30737e10cb7cdffe0e17178c28b3a12448874",
      "url": "https://api.github.com/repos/ducthangho/tra-luat/actions/jobs/127489703361",
      "html_url": "https://github.com/ducthangho/tra-luat/actions/runs/42092343146/job/127489703361",
      "status": "completed",
      "conclusion": "success",
      "created_at": "2026-11-05T19:46:16Z",
      "started_at": "2026-11-05T19:46:18Z",
      "completed_at": "2026-11-05T19:46:28Z",
      "name": "dot-bien-gop",
      "steps": [
        {
          "name": "Set up job",
          "status": "completed",
          "conclusion": "success",
          "number": 1,
          "started_at": "2026-11-05T19:46:19Z",
          "completed_at": "2026-11-05T19:46:20Z"
        },
        {
          "name": "Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 2,
          "started_at": "2026-11-05T19:46:20Z",
          "completed_at": "2026-11-05T19:46:24Z"
        },
        {
          "name": "Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 3,
          "started_at": "2026-11-05T19:46:24Z",
          "completed_at": "2026-11-05T19:46:25Z"
        },
        {
          "name": "Run actions/download-artifact@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 4,
          "started_at": "2026-11-05T19:46:25Z",
          "completed_at": "2026-11-05T19:46:26Z"
        },
        {
          "name": "gom mảnh",
          "status": "completed",
          "conclusion": "success",
          "number": 5,
          "started_at": "2026-11-05T19:46:26Z",
          "completed_at": "2026-11-05T19:46:26Z"
        },
        {
          "name": "Post Run actions/setup-python@v5",
          "status": "completed",
          "conclusion": "success",
          "number": 9,
          "started_at": "2026-11-05T19:46:26Z",
          "completed_at": "2026-11-05T19:46:26Z"
        },
        {
          "name": "Post Run actions/checkout@v4",
          "status": "completed",
          "conclusion": "success",
          "number": 10,
          "started_at": "2026-11-05T19:46:26Z",
          "completed_at": "2026-11-05T19:46:26Z"
        },
        {
          "name": "Complete job",
          "status": "completed",
          "conclusion": "success",
          "number": 11,
          "started_at": "2026-11-05T19:46:26Z",
          "completed_at": "2026-11-05T19:46:26Z"
        }
      ],
      "check_run_url": "https://api.github.com/repos/ducthangho/tra-luat/check-runs/127489703361",
      "labels": [
        "ubuntu-latest"
      ],
      "runner_id": 1000039711,
      "runner_name": "GitHub Actions 1000039711",
      "runner_group_id": 0,
      "runner_group_name": "GitHub Actions"
    }
  ]
}
~~~~ END ddj.json

~~~~ BEGIN lease.yaml
# LEASE — ASSURANCE-81-MODEL-EFFORT-TUY-CHON revision 1 / generation 1 — model/effort phuc vu cua reviewer thanh truong "ghi neu do duoc"
# GHI HO theo chi thi CHU KHO (chep nguyen van o granted_on_instruction_nguyen_van).

schema_version: 2
event: executor_lease_granted

packet_issue: 1240
granted_by: ducthangho
granted_on_instruction: https://github.com/ducthangho/tra-luat/issues/1240#issuecomment-6663237223
authority_url: https://github.com/ducthangho/tra-luat/issues/1240
granted_on_instruction_nguyen_van: >-
  Chu kho trong phien dieu phoi session_015GtxraXfMD1t2FJLzzGDr4, 05-11-2026: 'điều chỉnh để từ sau model và effort chỉ là
  optional, không phải bắt buộc'; '(a) hồi tố, (b) không bắt buộc'; Q1 'Có, theo provider', Q2 'Không tính';
  ~16:27Z 'Duyệt spec_hash, cấp lease sau 16:40Z'.
authority_caveat: >-
  Chi thi qua tin nhan trong phien dieu phoi; comment ghi lai tren Issue do phien agent dang bang token chu kho (#566).
dieu_kien_cap_da_do: >-
  Cap SAU 16:40Z (lease wp1099-cloud-setup-p3b-r11-g1-claude tren docs/PROTOCOL_DA_PHIEN.md het han 16:40Z). ai-dang-giu do
  16:4xZ sau fetch du ref (comm -23 may chu/cuc bo = 0): NGUOI_GIU 0 cho ca 4 duong dan code. Spec r1 land qua PR #1241
  (merge 3163f4d). Bao truoc phien dieu phoi tong session_015GtxrYPjZCTZeRiazdssgq ('ok merge #1241').
recorded_by: claude-session
recorder_is_dispatcher: true
recorder_ghi_chu: 'Phien dieu phoi session_015GtxraXfMD1t2FJLzzGDr4 ghi lease; KHONG thi hanh packet nay.'

leased_at_utc: '2026-11-05T17:32:53Z'
heartbeat_at: '2026-11-05T17:32:53Z'
lease_until: '2026-11-06T17:32:53Z'
lease_expires_at_utc: '2026-11-06T17:32:53Z'

packet_id: ASSURANCE-81-MODEL-EFFORT-TUY-CHON
packet_slug: assurance-81-model-effort-tuy-chon
revision: 1
generation: 1
lease_id: wp1240-r1-g1-claude
thay_the_cho: []
role: executor
provider: anthropic_claude
executor: claude
surface: claude_code
model: claude-opus-5-5
environment: cloud
risk: sensitive
review_class: sensitive
effective_review_class: sensitive
assurance_target: cross_approved_or_human_audited
reviewer_provider: openai_codex
reviewer_surface: codex_cli
reviewer_ghi_chu: 'Codex offline qua launcher.py run tren SHA ung vien cuc bo (ADR-0060 M12), roi connector @codex review tren PR draft.'
access: read-write

spec_path: ops/specs/assurance-81-model-effort-tuy-chon-r1.md
spec_source_oid: 3163f4d02a583787a9340c63a1f5eebd3780d970
spec_blob: 02b9d4fe932d02fe36ab534962b0253fccefb911
spec_sha256: e7c6707860ba6a7ca6d24b1cadc2510b4b93952048375bdc332e0328d601487e
spec_hash: e7c6707860ba6a7ca6d24b1cadc2510b4b93952048375bdc332e0328d601487e
spec_hash_formula: SHA256 of UTF-8 LF Git blob bytes at spec_source_oid:spec_path
spec_ref_ghi_chu: 'Khong spec_ref: spec da tren master (PR #1241) => kiem-merge K1 doc spec tai H, so sha256 voi spec_hash.'

branch: agent/wp1240-g1-claude
branch_ownership: exclusive
target_branch_neu_land: master
base_sha: 3163f4d02a583787a9340c63a1f5eebd3780d970
start_from_sha: 3163f4d02a583787a9340c63a1f5eebd3780d970
immutable_acceptance_baseline: 3163f4d02a583787a9340c63a1f5eebd3780d970
reviewed_sha_required: 3163f4d02a583787a9340c63a1f5eebd3780d970
reviewed_sha_ghi_chu: 'chua co head code luc cap lease; moi luot review neo dung SHA cua luot.'

write_set:
  - docs/PROTOCOL_DA_PHIEN.md
  - docs/adr/0065-model-effort-phuc-vu-tuy-chon.md
  - ops/handoff/wp1240-g1-claude.md
  - ops/land_evidence_nguon.py
  - ops/land_evidence_nguon_test.py
write_set_hash: 1e197a9a6ae490ed534fd6706e1dd4ae7acdf3a6b10d23bff35826bc958b68e4
write_set_hash_cach_tinh: 'sha256 cua cac duong dan DA SAP XEP (LC_ALL=C), noi bang LF, co LF cuoi, utf-8.'
write_set_ghi_chu: >-
  Diff PR dung 4 tep code/doc; handoff chi tren nhanh lease/handoff. KHONG sua ops/kiem_ho_so_land.py (A8, rang buoc #1210),
  KHONG sua .claude/dev/packet_loop*.py, KHONG mo lai ho so ops/land/** (hoi to la packet RIENG sau khi #1240 land).
bat_bien_tuong_thich_nguoc: >-
  #1240 chi NOI luat L7. Moi ho so DAT tren base phai van DAT tren head: A7 cua spec (land_evidence_nguon --root . => 0 vi pham,
  so DAT/mien tru khop nen hoac lech co giai thich). Ho so dang ghi (#1099 pr1197, #1105 pr1231) land truoc hay sau deu khong doi mau.
tran_kich_thuoc: 'ADR-0053: <= 6 tep / <= 450 dong them.'
tran_loi_goi_codex: >-
  ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544: tran cung 10; ngan sach mem 2. Hai luot lien tiep chua approve
  => Review Rescue Checkpoint (ADR-0037), hoi chu kho truoc loi goi ke tiep.
quy_trinh_ap: >-
  ADR-0060 mac dinh theo ADR-0062: worker gate tai cho tren dung SHA ung vien -> handoff len Issue #1240 neo SHA ung vien ->
  review Codex OFFLINE tren SHA cuc bo (in dung 'KET_LUAN: approve') -> approve moi push DUNG SHA do mot lan + PR draft ->
  connector + CI PR. Truoc khi bao san sang merge: packet_loop.py kiem-merge rc=0. Windows: theo M3 (spec: du kien unknown,
  reviewer chot not_required neu A9 dat).
ci_budget:
  gate_tu_dong: 'CI PR tu dong (ubuntu) tren PR cua packet'
  windows: 'KHONG chay CI Windows; khong full mutant tren Windows (chi thi chu kho 05-11). Neu M3 = required: chi chay Windows tap trung, bao truoc phien dieu phoi tong.'
  het: 'Mot job bat buoc do 2 luot lien tiep cung mot loi => DUNG, bao phien dieu phoi'
dieu_kien_dung:
  - 'S1 — can sua tep ngoai write set (ke ca ops/kiem_ho_so_land.py, packet_loop*.py, ops/land/**). DUNG, handoff.'
  - 'S2 — vuot tran ADR-0053 (> 6 tep hoac > 450 dong them). DUNG, checkpoint chu kho.'
  - 'S3 — spec tu mau thuan / thieu du kien. DUNG, bao phien dieu phoi (khong tu suy).'
  - 'S4 — het han lease => ngung ghi, ban giao theo luat chu kho 02-11.'
  - 'S5 — A7 doi mau mot ho so DAT tren base thanh TRUOT. DUNG, bao phien dieu phoi.'

cam_tuyet_doi:
  - Khong sua spec; khong sua tep ngoai write set
  - Khong tu review / approve / merge / land
  - Khong LIVE (Drive/NLM/webapp/registry), khong deploy webapp hay Package, khong bump VERSION
  - Khong doc/ghi credential that
  - Khong workflow_dispatch
  - Khong force-push
  - Khong viet chuoi bo-qua-CI nguyen van trong commit message

coordination_paths:
  - ops/leases/wp1240-r1-g1-claude.yaml
run_minutes: 1440
heartbeat_required_minutes: 360

chua_do_duoc:
  - 'Danh tinh nguoi ky: #566.'
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab
dieu_kien_merge: ADR-0060@36d7c5dcdcbbb27176b75135125b9009f9fe0587
~~~~ END lease.yaml

~~~~ BEGIN output4.txt
ĐỦ ĐIỀU KIỆN MERGE trên ecd30737e10cb7cdffe0e17178c28b3a12448874
rc=0
~~~~ END output4.txt
