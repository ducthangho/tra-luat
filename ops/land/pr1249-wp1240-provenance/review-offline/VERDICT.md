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
