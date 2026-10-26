---
verdict: changes_requested
reviewed_sha: b0fadc96366115d3545b9c723b30f04281898d94
spec_sha256: 30776483ab40e57708c6b03ba0877bc3f40dd27edf334e7dceb0fe5629a113e2
so_p0: 0
so_p1: 0
so_p2: 0
so_p3: 0
---

Kết luận: chưa đủ bằng chứng để approve vì C8 bị giới hạn quyền Unix socket trong sandbox. Không phát hiện lỗi mã P0/P1/P2/P3; các phép đo đã hoàn tất và phần chưa đo được được tách rõ bên dưới.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Theo assignment: connector Codex trên PR #930 đã review `b0fadc96366115d3545b9c723b30f04281898d94`, `has_any_findings: false`; không có finding cũ để đối chiếu. Không đọc lại GitHub trong lượt offline.

## Bảng đo lại

- Candidate: `b0fadc96366115d3545b9c723b30f04281898d94`; tree `0f37ccea8563d543e239e77dd371ee293313736f`; detached HEAD.
- Base packet: `9d34a8e7e97fdc8ac178fc209219cea067e4c279`; revision 2, generation 1; Review Class `sensitive`.
- Lease đọc từ `a4e963db3a1c8f8811d17373e6de551a403e6042:ops/leases/wp763-r2-g1-claude.yaml`, khớp spec hash/base/write set; hạn khai `2026-10-27T15:40:00Z`. Review này theo chỉ thị `prompt.snapshot`, chỉ ghi thư mục gói, không chuyển state/đăng GitHub.
- Effective write set executor: `.claude/dev/ci_dang_ky_test.py`, +2/−0. Bốn tệp #752 chỉ đối chiếu tính toàn vẹn khi merge, không chấm lại nội dung.
- Provider `openai_codex`, model family `openai`, execution surface `codex_cli`, transport `machine`; run `c4103982ae4c4a8b9a98e308d7b7beb1`. Nguồn surface/transport: `runs/c4103982/run.json`. Model cụ thể/effort chưa có header để đo; không suy từ actor GitHub. Executor khai Claude Opus 5.5 trong lease, không có thống kê runtime độc lập trong gói này.
- Linux x86_64; Python 3.11.17; PyYAML 6.0.1; Git 2.43.0; actionlint 1.7.7; Ruff 0.16.9. Kho không nông, không khai promisor; `core.abbrev=7`.
- Snapshot ban đầu `before.json`: 5745 tệp, 5 đường dẫn khớp bộ lọc bí mật không đọc nội dung. Tracked/index sạch; ignored `.codex/` có từ đầu. Sandbox thực tế `workspace-write`; giữ mirror chỉ đọc bằng phạm vi lệnh, cache/temporary files đặt trong gói.

Các lệnh/rc/stdout/stderr/băm được ghi riêng cạnh verdict; `measure.py` là bộ ghi phép đo, không sửa mirror. `TMPDIR`, `TEMP`, `TMP` trỏ `goi/tmp`; `PYTHONDONTWRITEBYTECODE=1`; Git tắt optional locks.

| Tiêu chí | Lệnh | Đầu ra / rc | Khớp/lệch |
|---|---|---|---|
| Hash đặc tả | `sha256sum ops/specs/no-p3-dang-ky-ci-r2.md` | `30776483ab40e57708c6b03ba0877bc3f40dd27edf334e7dceb0fe5629a113e2`, rc 0 | Khớp |
| Diff packet | `git diff --numstat 9d34a8e 7a7d52d` | `2 0 .claude/dev/ci_dang_ky_test.py`, rc 0 | Khớp |
| Diff merge | `git diff --name-status cdc4e80 b0fadc9` | 1 tệp sổ sửa + 4 tệp #752 thêm, rc 0 | Khớp tập 5 tệp |
| C1 head gộp | `python3 -B .claude/dev/ci_dang_ky_test.py` tại mirror, môi trường fixture mô tả dưới | rc 0; `ĐĂNG KÝ: 26/26`; `PHẢN CHỨNG: 1070/1070 đỏ đúng`; `TỔNG: ĐẠT`; 0 dòng bắt đầu `ĐỎ:` | Khớp; `C1-head-env.*` |
| C1 head packet | Cùng lệnh trên bản xuất `7a7d52d5640f309d9242ae06d3711e6573ce34e5` | rc 0; cùng các dòng dương trên; stdout cùng SHA-256 với head gộp | Khớp; `C1-packet.*` |
| C1 nền S1 | Cùng lệnh trên bản xuất base `9d34a8e7e97fdc8ac178fc209219cea067e4c279` | rc 1; `26/24`; đúng 2 dòng chưa đăng ký, từng tệp #752; `TỔNG: ĐỎ` | Khớp; `C1-base-S1.*` |
| Parity bản sao | Cùng lệnh trên bản sao candidate ngoài mirror | rc 0; stdout SHA-256 `46b13bc5efa42afe74e84e5d88c7f842450d3735bc22c0d1bcd3e312a33f0fb0`, bằng mirror và head packet | Khớp; `C1-copy-parity.*` |
| C1b | Lệnh `runpy` nguyên tiêu chí C1b, lưu đầy đủ argv trong `C1b-*.json` | Base `False 10`; packet và head gộp `True 12`; cả ba rc 0 (giá trị Boolean của base là âm) | Khớp |
| Byte/vị trí | `python3 -B goi/verify_git.py` từ thư mục cha mirror; lệnh tuyệt đối trong `git-integrity.json` | Hai dòng mới bằng nguyên byte dòng nhanh sau khi chỉ đổi khoá; liền sau nhanh ở cả packet/head gộp. Băm dòng nhanh `1e58cbca24106f30ef47ddd0b3efc22d0b3ac99954d54deb92586f0dbec24876` | Khớp |
| C2 | `python3 -B .claude/dev/ci_dang_ky_test.py` trên từng bản đột biến M1/M1b | Mỗi lượt rc 1, `26/25`, đúng một dòng `ĐỎ:` nêu tệp vừa gỡ, `TỔNG: ĐỎ` | Khớp; `C2-M1.*`, `C2-M1b.*` |
| C3 | Cùng lệnh trên M2 | rc 1, `26/26`, đúng 2 dòng `ĐỎ:` đúng nội dung/mỗi dòng một lần; `TỔNG: ĐỎ` | Khớp; `C3-M2.*` |
| C4 hai test thật | `python3 -B <gói>/probe_c4.py <root>`; script gọi `chay_moi(moi={k: MOI[k] for k in hai_khoa})` của chính root | Cả packet và head gộp: `9/9`, `6/6`; từng dòng `CI_DANG_KY …: ĐẠT rc=0` đúng một lần; `do = 0`, rc 0; JSON thời gian cục bộ của hai khoá không lỗi | Khớp; `C4-real-head.*`, `C4-real-packet.*` |
| C4 màu nền | Cùng lệnh trên base | rc 1; `KeyError: 'ops/kiem_ho_so_land_test.py'` trước chạy test | Khớp màu chưa làm; `C4-base-not-done.*` |
| C4 M3/M4 | Cùng lệnh trên bản sao; mẫu luôn đọc từ `MOI` của bản đang đo | M3 `0/0`, `3/4`, M4 đổi mẫu: `do = 1`, wrapper rc 1, test con rc 0; đúng khoá bị chấm `ĐỎ`, khoá còn lại `ĐẠT`. Đã đo cả hai khoá | Khớp; `C4-M3-*`, `C4-M4-*` |
| C5 dương | `git cat-file -e <base>^{commit}`, rồi `git cat-file -t <base>:<tệp>` | Base đo được, rc 0; từng test là `blob`, rc 0; đo thêm hai công cụ cũng là blob | Khớp; `git-integrity.*` |
| C5 âm S3 | Chuyển riêng hai test sang tên lưu trong bản sao, chạy C1 | rc 1, `24/26`, đúng 2 dòng mục đăng ký không có tệp, `TỔNG: ĐỎ`; khôi phục bản sao sau phép đo | Khớp; `C5-S3.*` |
| C7 bare lint | `ruff check --select F --no-cache .claude/dev/ci_dang_ky_test.py` | Ruff 0.16.9: base, packet, head gộp đều rc 0, `All checks passed!`; multiset lỗi rỗng, delta 0 | Khớp; `C7-base.*`, `C7-packet.*`, `C7-head.*` |
| C7 răng | Cùng lệnh sau thêm `import fractions` ở bản sao | rc 1, đúng `F401`, `Found 1 error.` | Đạt phản chứng; `C7-unused-import.*` |
| Ruff pin/probe contract | C1 gọi `loi_ruff_ci()` trên YAML hiện hành | `RUFF CI: 3/3 hợp đồng` | Tách biệt với bare lint; không suy phiên bản Ruff đã chạy trên GitHub |
| C8 đầy đủ | `python3 -B ops/ci_duong_nhanh_test.py` tại mirror | rc 1, `CA: 103/104 dat · 0 do · 1 hong`; `DOT BIEN: 387/392 bi giet dung ly do`; `TONG: DO` | **Không tái lập được lời khai xanh trong sandbox này**; lỗi quyền, phân tích dưới; `C8-head.*` |
| C8 ca tiêu thụ sổ | `python3 -B ops/ci_duong_nhanh_test.py --mot-ca k01_so_dang_ky_nhan_muc_da_noi` | Head: rc 0. Base S1 và S3: rc 3, `DO:k01_so_dang_ky_nhan_muc_da_noi:…` với lỗi đăng ký đúng loại | Phần liên quan trực tiếp +2 dòng có bằng chứng dương/âm; không thay full C8 |
| Tính toàn vẹn merge | `python3 -B <gói>/verify_git.py` | rc 0; đúng parents `7a7d52d…` + `cdc4e80…`; 4/4 blob #752 bằng base và packet; 5740/5740 mục cây master ngoài sổ giữ nguyên mode/type/OID; bỏ đúng hai dòng mới khỏi sổ head gộp được nguyên byte sổ master | Không có tệp master bị lùi bản; `git-integrity.*` |

Môi trường fixture: lần C1 đầu (`C1-head.*`) rc 1 do `git commit` trong fixture thoát 128, chưa có dòng `PHẢN CHỨNG`/`TỔNG`. `git config --show-origin --get-regexp '^(commit\.gpgsign|gpg\.format|core\.abbrev)$'` cho global `commit.gpgsign=true`, `gpg.format=ssh`, local `core.abbrev=7`. Đặt `commit.gpgsign=false` và `core.abbrev=7` bằng các biến cấu hình Git **chỉ trong tiến trình test** rồi chạy lại C1 đạt; không sửa config/ref của mirror. Không coi lượt lỗi đầu là pass. Các lệnh sau dùng môi trường này, cùng ba biến temporary và bytecode đã nêu.

Bản sao được tạo bằng `mktemp -d -p <gói> <nhãn>.XXXXXX`, xuất blob của exact OID vào đó (`measure.py export`). Không chép `.git`/ignored `.codex`; 5 đường dẫn khớp tên cấm dưới `ops/reviews/` không đọc nội dung và không xuất. Parity C1 chứng minh các khác biệt đó không làm đổi đầu ra C1; không dùng bản sao này để chứng nhận mọi thuộc tính khác của kho.

Bốn merge #748 nêu trong spec đều là tổ tiên của cả base packet và `cdc4e80`, 8 lệnh `merge-base --is-ancestor` đều rc 0. Receipt #752 lượt 3 tại `01486f1cb4e32ed35da872c688bd2a38db80773b` ghi đúng base, `approve`, `cross_approved`; băm bytes verdict đọc từ cùng OID khớp `d132a22964fd50e37b30a346f378beb2411311a19e51ee0923355d7fe18c1b3d`. Đây là đối chiếu hồ sơ cục bộ, không phải đọc lại authority GitHub.

Hai biến động số đã kiểm độc lập bằng `python3 -B <gói>/history.py` (`history-counts.json`, rc 0):

- **1064 → 1070:** chạy C1 trên bản xuất `1d7e642` thật cho `1064/1064`, rc 0; trên `518fa0c5e37d9b10ab17df1e0eff7ab565a78d6e` cho `1070/1070`, rc 0. `git diff --numstat 518fa0c^ 518fa0c -- .claude/dev/ci_dang_ky_test.py` đúng `15 3`; blob trước bằng `1d7e642`, blob sau bằng base `9d34a8e`. Diff thêm đúng sáu phản chứng `wp892-*`. Lý do executor nêu đúng.
- **384 → 392:** nạp `CA`/`DOT_BIEN` từ chính blob từng commit: `1d7e642` = `104/384`; `518fa0c` vẫn `104/384`; `d73ed730b67e065dd80198168820e24722045405` = `104/391`; `70172ec` giữ nguyên; `f744f744da11e61952279289a00d1cda4f4a179f` = `104/392`. Base, packet, master `cdc4e80`, head gộp đều `104/392`. Bảy tên tăng ở `d73ed73`: `y04_env_ten_khac`, `y04_env_them_khoa`, `y04_env_vao_buoc_khac`, `y04_if_che_do_vao_job_gate`, `y04_if_che_do_vao_job_gom`, `y04_if_manh_doi_dang`, `yml_manh_bo_if_duong_nhanh`; một tên tăng ở `f744f74`: `y04_with_che_do_buoc_tai_ve`. Thay đổi thuộc lịch sử #892, đã có trước #763. Số lượng 392 là đúng; không đồng nghĩa 392 đột biến đều được giết trong lượt sandbox này.

## Đột biến

Script tái lập: `probes.py` và `negative_baselines.py` trong gói; từng lệnh con có JSON ghi cwd/argv/rc/hash và stdout/stderr riêng. Mọi thay đổi ở bản sao, khôi phục trong `finally`; không có patch sản phẩm.

| Phép | Thay đổi bản sao | Quan sát độc lập |
|---|---|---|
| M1 | Gỡ riêng mục `ops/kiem_nhan_hint_test.py` | rc 1; đúng `ĐỎ: test sống chưa đăng ký: ops/kiem_nhan_hint_test.py`; `26/25`; `TỔNG: ĐỎ` |
| M1b | Gỡ riêng mục `ops/kiem_ho_so_land_test.py` | rc 1; đúng `ĐỎ: test sống chưa đăng ký: ops/kiem_ho_so_land_test.py`; `26/25`; `TỔNG: ĐỎ` |
| M2 | Đổi khoá hint thành `ops/kiem_nhan_hint_tests.py` | rc 1; đúng một dòng chưa đăng ký tên thật và một dòng mục đăng ký không có tệp tên sai; `26/26`; `TỔNG: ĐỎ` |
| M3 × hai khoá | Test con in lần lượt `0/0`, `3/4` | Mỗi lượt test con rc 0 nhưng khoá đó `ĐỎ`, `do = 1`, wrapper rc 1; khoá còn lại `ĐẠT` |
| M4 × hai khoá | Thay mẫu của khoá đang thử bằng mẫu `gh_readback_test.py` trong cùng `MOI`; stub vẫn in `1/1` | Khoá đó `ĐỎ rc=0`, `do = 1`; đổi lại mẫu thật thì cả hai `ĐẠT`, `do = 0` |
| L6 chữ/văn xuôi × hai khoá | Test in `hai/hai` hoặc `xong 5/5 ca (ok)` | Đúng khoá `ĐỎ rc=0`, `do = 1`; đối chứng `1/1`, `2/2` đều `ĐẠT`, `do = 0` |
| S3 | Tạm vắng hai test, sổ giữ hai khoá | C1 rc 1, `24/26`, hai dòng thiếu tệp; C8 ca `k01` rc 3 vì đúng lỗi đó |
| Ruff | Thêm import không dùng `fractions` | rc 1, `F401`; bỏ mutant thì tệp nguyên byte candidate |

Không soạn tải trọng tấn công hoặc đường dẫn thoát cây. Các phản chứng sẵn có của suite chạy trong vùng temporary của gói; không bổ sung hướng thử ngoài chỉ thị.

## Findings

Không có finding mã đủ bằng chứng P0/P1/P2/P3 trong phạm vi packet: **0 lớp, 0 biểu hiện**. Không chấm lại bốn tệp #752. Không gán lỗi quyền của sandbox thành lỗi sản phẩm hoặc kết luận executor khai sai về môi trường của họ.

**Kết luận lượt: `changes_requested` vì thiếu bằng chứng dương C8.** Ngưỡng nội dung 0 P0/P1/P2 đã đạt, nhưng C8 bắt buộc chưa xác nhận được; assignment chỉ miễn chấm C6. Định dạng được giao không có `blocked`, nên dùng `changes_requested` để yêu cầu bổ sung phép đo, không phát sinh một P2 giả. Phần cần hoàn tất là chạy nguyên C8 trên exact SHA này trong môi trường được cấp quyền cho fixture Unix socket, lưu rc và ba dòng tổng; không đề nghị sửa hai dòng đăng ký hoặc bỏ ca/giả lập socket để làm xanh. Không gán `cross_approved` hay xác nhận đủ điều kiện merge từ lượt thiếu bằng chứng này.

Đối chiếu bắt buộc về C8:

```text
python3 -B ops/ci_duong_nhanh_test.py
rc=1
[HONG] t20zo_la_khong_phai_tep_thuong_do: PermissionError: [Errno 1] Operation not permitted
CA: 103/104 dat · 0 do · 1 hong
DOT BIEN: 387/392 bi giet dung ly do
TONG: DO
```

`C8-head.stdout` ghi năm đột biến không được tính giết vì **ca đích không xanh trên bản gốc**, đều ở cùng thao tác `s.bind(ten)` của fixture: `symlink_treo_khong_theo_bi_danh`, `la_bo_chot_tep_thuong`, `la_cho_phep_fifo`, `la_cho_phep_socket`, `la_khong_theo_symlink`. Đây là 5 mục **không đo được**, không phải 5 mutant sống chứng minh chốt hở.

Đối chứng trên bản xuất base, lệnh `python3 -B ops/ci_duong_nhanh_test.py --mot-ca t20zo_la_khong_phai_tep_thuong_do` cũng rc 4, cùng `PermissionError` tại `s.bind(ten)` (`C8-failed-case-base.*`). `final_checks.py` đối chiếu nguyên văn hàm ca và `_tao_socket`: base/head bằng nhau; công cụ `ops/ci_duong_nhanh.py` cùng blob ở base/master/head; test C8 cùng blob ở master/head. Test C8 khác giữa base/master chỉ ở hai giá trị timeout của `KHUNG_JOB`, 30/105 → 150, đúng phần master đưa vào khi merge. Phép đối chứng này phân biệt lỗi môi trường ở ca đang hỏng; không tuyên bố đã chạy full C8 trên base hay full C8 đạt.

## chua_do_duoc

- **C6 — `not_run`, không chấm theo assignment:** không gọi mạng/GitHub; chưa xác nhận run/attempt, checkout, workflow definition, log hai test và JSON thời gian đủ 12 khoá trong CI. JSON hai khoá từ C4 cục bộ không thay C6.
- **C8 — lệnh full đã chạy `failed` (rc 1); một ca và năm mutant `not_measured` do quyền Unix socket.** 103 ca và 387 mutant có kết quả dương từ bộ chạy; tổng bắt buộc `104/104`, `392/392`, `TONG: DAT` chưa tái lập được. Không sửa/bỏ ca, không vượt sandbox, không đổi sang pass.
- **Runtime/assurance:** `run.json` đang chạy xác nhận provider/surface/transport và exact head, nhưng `stderr.log` chưa có header model/effort khi đọc; không đo được model slug/effort hoặc kết quả terminal của launcher bao ngoài lúc chính reviewer còn chạy. Tự nhận diện là Codex, họ OpenAI; chỉ thị runtime mô tả dựa trên GPT-6, không có số đo riêng để neo model cụ thể. Identity Executor là lời khai lease, không phải runtime receipt được kiểm độc lập trong lượt này. Không có GitHub submitter (chưa đăng).
- **Authority động:** lease/receipt được đọc từ exact Git OID cục bộ. Không kiểm lại cập nhật/thu hồi trên máy chủ, ngân sách hiện hành hoặc PR head qua mạng. Đây là giới hạn của lượt offline được giao.
- **Nền:** chỉ Linux được đo; không chạy Windows. Bare lint dùng Ruff 0.16.9 cài sẵn; hợp đồng pin/probe CI được kiểm riêng, không tuyên bố đã chạy bản Ruff pin trong GitHub.
- **Snapshot:** chỉ quan sát mirror được cấp; repo nguồn ngoài mirror không thuộc phạm vi. `before.json` và `after.json` bằng nhau: HEAD/tree, refs, index/diff, tracked/untracked/ignored và băm nội dung tệp được phép đọc không đổi. Năm đường dẫn có tên cấm chỉ giữ metadata, không đọc byte; snapshot không chứng minh mọi thời điểm giữa hai mốc.

Trạng thái tổng hợp: C1/C1b/C2/C3/C4/C5/C7 và phép kiểm merge **passed**, các ca âm đạt vì thất bại đúng mục tiêu; C8 full **failed / còn phần not_measured**; C6 **not_run**; không có check được tự đổi từ **skipped** sang pass. `git diff --check` cho cả phạm vi packet và merge rc 0. Candidate cuối vẫn `b0fadc96366115d3545b9c723b30f04281898d94`, tree `0f37ccea8563d543e239e77dd371ee293313736f`.

Nhật ký rig của reviewer được giữ nguyên: `negative-baselines.*` là lần đầu lỗi import `IndexError` trong script scratch; sửa điều kiện entrypoint của scratch, `negative-baselines-fixed.*` rc 0 và các lệnh con có bằng chứng riêng. Một assertion chẩn đoán ban đầu giả định cả blob test C8 bằng base đã bị bác bởi hai thay đổi timeout; không dùng assertion đó làm bằng chứng. Đối chiếu chính xác theo hàm và master/head ở `final-checks.*` rc 0. Hai lỗi rig này không tính thành finding sản phẩm.

`measurements.json` tổng hợp 44 bản ghi lệnh có rc/stdout/stderr/hash tại mốc chốt; `final-checks.json` ghi lượt kiểm cuối riêng. Tất cả 44 cặp hash log đã được đọc lại và khớp. Bản sao phục vụ đột biến đã khôi phục nguyên byte ba tệp bị thay trong các phép thử; mirror không có delta quan sát được. Chỉ ghi hiện vật dưới thư mục gói; không push, không sửa ref mirror, không đăng verdict lên GitHub.
