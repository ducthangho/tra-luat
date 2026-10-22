verdict: approve
reviewed_sha: 974859d67a8062f869cb49e8d3be75db44ef4d58

Kết luận lượt 5/5, packet #845, lớp `sensitive`: **kết luận approve lượt 4 giữ được cho HEAD merge này sau khi kiểm lại độc lập**. Hai tệp write set khớp byte với lượt 4; dữ liệu master mang vào không làm sai L6 hoặc làm đỏ bộ test. Không có P0/P1/P2 mở trong phạm vi xác nhận. Hai lớp P3 của lượt 4 tiếp tục được chấp nhận ghi nợ, không đo lại theo chỉ dẫn hiện hành. Đây là verdict mới neo HEAD mới; không dùng verdict cũ như bằng chứng còn hiệu lực tự động sau merge.

Reviewer độc lập OpenAI/Codex; executor Claude theo assignment. Chỉ xác nhận tác động của merge master, không mở vòng sửa mới. Authority tăng ngân sách 4→5 và thông tin PR #846 đã merge được nhận từ `prompt.snapshot`; không xác minh GitHub. Không gọi mạng/GitHub, không push/merge/land và không sửa `cay-kho/`.

**Neo phép đo.** Trong bảng, H = `974859d67a8062f869cb49e8d3be75db44ef4d58`, P = `7a39463e8b6c25d4811bcc9cd544b164e7ce53a7`, M = `3cfbf41306ad19b720f308f52840b77018394727`, B = `9f4a539b12d1d948817123d117f4bf2aedb1898f`. Các lệnh Git do `prepare.py`/`audit_merge.py` gọi trên `cay-kho`, với `--no-optional-locks`, `GIT_OPTIONAL_LOCKS=0` và `core.abbrev=7` theo từng lệnh; không đổi config nguồn. Hai bản sao đều được đối chiếu từng blob với Git tree, nằm dưới `review-data/`.

| Lệnh / phép đo thực chạy | Kết quả thật | Ý nghĩa |
|---|---|---|
| `git rev-parse HEAD HEAD^{tree} HEAD^1 HEAD^2`; `git show -s --format=%P H` | rc=0; HEAD=H; tree=`b5d5b7714096878a603530ee1da71e384389dc21`; danh sách cha đúng **P, M**, không có cha thứ ba | Đúng HEAD được giao và đúng merge commit |
| `python -B review-data/prepare.py`: SHA-256 byte `SPEC-r1.md` | Lần chạy hoàn tất rc=0; `a5a89622376495186ae265f18f4f6d1ce7e2b2e3b7613c61c2d96087a2c3af0b` | Khớp spec r1 đóng băng |
| `git diff --binary P H -- ops/land_evidence_nguon.py ops/land_evidence_nguon_test.py`; `git show P:<tệp>` đối chiếu `git show H:<tệp>` và byte checkout | rc=0; diff **0 byte**; cả hai tệp bằng nhau từng byte; blob/hash ở bảng dưới | Tự đo bằng Git, không nhận số 0 executor khai |
| `git diff --stat P H`; `git diff --name-only P H` | rc=0; **59 tệp, +5658/-6**: `ops/land/` 25, `ops/leases/` 4, `ops/reviews/` 28, `ops/specs/` 2; không có tệp `.py` thay đổi | Xác định toàn bộ phần master mang vào, gồm dữ liệu có thể ảnh hưởng cây thật |
| `git diff B H -- <hai tệp write set>`; `git diff --numstat B H -- <hai tệp write set>` | rc=0; patch khớp byte `diff-write-set.patch`; checker +19/-1, test +81/-0, tổng **+100/-1**, đúng 2 tệp | Phần triển khai packet và Q3 không đổi |
| Trong `review-data/head-974859d/`: `python ops/land_evidence_nguon_test.py` | **rc=0**; `CA: 16/16 dat`; `DOT BIEN: 64/64 bi giet dung ly do`; `TU KIEM PHAN HANG: DAT (2 dot bien)`; `TONG: DAT`; stderr rỗng | Suite trên H đạt, gồm `c11` cây thật và `c16` L6 |
| Cùng bản sao H: `python ops/land_evidence_nguon.py --root .` | **rc=0**; **13 ĐẠT · 28/28 miễn trừ · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 41**; `TỔNG: ĐẠT`; stderr rỗng | Tất cả hồ sơ hiện hành qua checker; phân biệt hồ sơ ĐẠT với miễn trừ |
| Trong `review-data/prior-7a39463/`: `python ops/land_evidence_nguon.py --root .` | rc=0; **12 ĐẠT · 28/28 miễn trừ · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 40**; `TỔNG: ĐẠT` | Đối chứng tại P: merge thêm một hồ sơ được kiểm, không sinh đỏ |
| `python -B review-data/audit_merge.py` | rc=0; ghi nhận các lần đọc nội dung và phân giải token nguồn; phụ thuộc checker/test, `requirements.txt`, registry CI, workflow và `.gitattributes` gốc đều khớp byte P/H | Kiểm tác động dữ liệu và đường chạy, không chỉ so hai tệp mã |
| `git diff --check B H -- <hai tệp write set>` | rc=0, stdout/stderr rỗng | Write set không có lỗi whitespace |
| Kiểm phụ: `git diff --check P H` | **rc=2**; 28 dòng ở 3 tệp `.patch` bằng chứng; đọc lại thấy mỗi dòng đúng một dấu cách, là dòng ngữ cảnh trống của patch | Không khai phép này pass. Các patch là dữ liệu lưu trữ, không được checker/suite đọc hoặc áp; không có tác động L6 được phát hiện |
| `python -B review-data/finalize.py` | rc=0; stdout suite khớp toàn bộ regex registry; xác nhận 16 ca có đăng ký `c11`/`c16`, 64 mutant, trong đó 27 mutant đích `c16`; snapshot nguồn **4897→4897 mục, 0 delta**, HEAD/tree/status/index không đổi | Đầu ra vẫn được CI nhận; giữ nguồn nguyên trạng theo phép đo cuối |

| Tệp write set | Git blob tại cả P và H | Byte / SHA-256 tại cả P và H |
|---|---|---|
| `ops/land_evidence_nguon.py` | `b0cb1588b2b5bdf82c455ca9c170c77f6c720b0a` | 21151; `7f621c4aa88fb9dd9c9549b5c7671f7fca3b53804366da48f1e2a0778a703b87` |
| `ops/land_evidence_nguon_test.py` | `99a955c5c49836143512086c9b04fdf9122fd748` | 34123; `f9cc180c9c0c84a3178974e3509bddc0e72a4747a5bd596ed7ddd640d74f3720` |

**Tác động master lên hành vi.** Mã và luật L6 không đổi. Đầu vào cây thật có đổi, nên số hồ sơ ĐẠT tăng 12→13. Trace chạy checker trên hai bản sao cho thấy chỉ hai tệp nội dung thay đổi được đọc: `ops/land/pr823-wp802-land-evidence.yaml` và tệp mới `ops/land/pr838-wp671-land-evidence.yaml`. Các token L1 mới phân giải tới 9 đường dẫn provenance đã mang vào; kết quả có thật được lưu trong `runtime-inputs.json`, không suy từ lời khai trong YAML.

Hồ sơ pr823 đổi `landed: false`→`true`, kích hoạt L6 thật: `post_merge_checks` là list 5 mapping, `bookkeeping` là list 4 mapping, không chuỗi khoá/giá trị nào chứa `CHO_DIEN`; hồ sơ ĐẠT. Hồ sơ pr838 có `landed: false` kiểu bool: L6 cho phép thiếu hai trường hoàn tất theo Q1.4; các luật còn lại cũng ĐẠT. Bộ kiểm vẫn có 28/28 miễn trừ bằng băm, không thêm hoặc nới danh sách.

Các tệp lease, review, spec và patch được master mang vào không thay module Python, dependencies hay đăng ký CI. Đường `c11_cay_that_dat_va_mien_tru_du` ở test:277 vẫn gọi checker trên `ROOT_THAT` của chính bản sao H; không chạy nhầm cây nguồn hoặc cây P. Toàn suite đã chạy ở H và xanh. Phép trace bổ sung cũng trả đúng tổng kết 13/41 như CLI không instrument. L1 chỉ xác minh token trỏ tới nguồn tồn tại; kết quả này không xác nhận tính đúng của nội dung nghiệp vụ/authority trong các hồ sơ land khác.

**ĐỐI CHIẾU LƯỢT TRƯỚC.** Giữ nguyên quyết định P3 của `verdict-luot4.md`, theo yêu cầu không đo lại. Không đóng finding chỉ vì merge master hoặc suite xanh.

| Mức / slug / vị trí giữ nguyên | Trạng thái và quyết định lượt 5 | Owner / hướng xử lý giữ nguyên |
|---|---|---|
| P3 `c16-thieu-rang-q1`; `ops/land_evidence_nguon_test.py:313`, `:320`; ba biểu hiện giới hạn mẫu độ sâu/độ dài chuỗi/số phần tử | **CHƯA VÁ, chấp nhận ghi nợ, không chặn approve.** Không chạy lại ba mutant SPACE; không nhận 64/64 hiện tại là chứng minh chúng đã chết. Các biểu hiện P2 A–Q đã đóng theo lượt 4; không mở lại khi mã/test khớp byte và suite H đạt | Executor/điều phối #845. Mô tả đúng giới hạn mẫu; nếu tăng độ bền thì làm packet riêng, sinh nhiều kích thước có đối chứng và giữ yêu cầu `TinHieuChotCa`; tránh nhận lỗi parser là tín dụng giết L6 |
| P3 `loi-khai-bang-chung-cu`, biểu hiện A; `SPEC-r1.md:21` | **CHƯA VÁ, chấp nhận ghi nợ, không chặn approve.** Giữ finding lịch sử mẫu số 5/9 cần đính chính 5/10 tại OID/phạm vi đã đo ở lượt 4; không đếm lại trong lượt này, không đổi mẫu số theo cây H để diễn giải lại finding cũ. Biểu hiện B về docstring CI đã đóng theo lượt 4 | Executor/điều phối #845. Đính chính tại handoff/hiện vật công bố với exact OID và phạm vi miễn trừ; giữ r1 bất biến, đổi spec phải ra revision mới. Không có xác nhận GitHub về việc đã đính chính |

**Finding mới:** không có P0/P1/P2/P3 mới trong phạm vi xác nhận merge này. Ngưỡng áp dụng đúng assignment: không P0/P1/P2 mở; P3 có quyết định ghi nợ như trên. Không có payload hoặc patch sửa sản phẩm được soạn.

**Bằng chứng, môi trường và giới hạn.** Log gốc, rc và cwd nằm tại `head-test.json`, `head-root.json`, `prior-root.json` cùng các tệp `.stdout.txt`/`.stderr.txt`; tổng hợp ở `check-results.json`. `preflight.json`, `merge-impact.json`, `runtime-inputs.json`, `registry-check.json`, `readonly-before.json`, `readonly-after.json`, `readonly-delta.json`, `validation-summary.json` và các script cùng thư mục cho phép kiểm lại các con số. Mọi tiến trình kiểm chạy với `TMPDIR` tuyệt đối dưới `review-data/tmp`, `PYTHONDONTWRITEBYTECODE=1`; bỏ biến override `LAND_EVIDENCE_NGUON_MA` cho suite gốc.

Python 3.13.16, PyYAML 6.0.1, Linux x86_64. Chuẩn bị bản sao lần đầu rc=1 vì Git archive áp `eol=crlf` cho `tl-setup.cmd`; đây là lỗi giả định của bộ đo reviewer. Đã khôi phục đúng byte Git blob của 3 tệp `.cmd` trong mỗi bản sao trước khi chạy test; bước chuẩn bị hoàn tất rc=0, mọi blob trong bản sao H (4607 tệp) và P (4550 tệp) đã đối chiếu Git tree. Chi tiết ở `preparation-note.json`/`preflight.json`. Không sửa nguồn để vượt kiểm tra.

Snapshot cuối có 0 delta nội dung/mode/symlink đã quan sát và 0 delta trạng thái Git/index; với 5 tệp tên liên quan secret chỉ kiểm metadata, không đọc nội dung. Đây là đối chiếu hai mốc, không tuyên bố filesystem bị cưỡng chế read-only tuyệt đối. Chỉ tạo bản sao và đầu ra trong `review-data/`.

`identity-evidence.json` lưu run `964888d964f24e3e9715b5f38b908457`, provider `openai_codex`, surface `codex_cli`, transport `machine`, prompt SHA-256 `fd81d4a435c3299806c1dbfa408efcf36e18e3a2ab65db5e65c1658e0486fc70` khớp launcher. Header CLI v0.163.0 khai model `gpt-6.1-sol`, effort `xhigh`, session `01a15387-07c2-7a70-bfc2-4fa15604c01a`. Đây là metadata/header của lượt chạy, không chứng minh từng request có cùng model/effort; danh tính executor chỉ theo assignment. Không gọi Codex lồng, không tự lập receipt hoặc state `cross_approved`; controller cần kiểm rc terminal và hash hiện vật khi phiên kết thúc.

Hai lệnh được giao, đối chứng checker P, audit tác động merge và xác minh cuối: **passed**. Kiểm phụ whitespace toàn merge: **failed (rc=2, dòng ngữ cảnh patch lưu trữ)**; chuẩn bị lần đầu: **failed ở bộ đo, đã sửa trong bản sao và chạy lại đạt**. Full repository selftest, release/deploy gate, Windows, GitHub Actions và ba probe P3 cũ: **not_run**, không nhận là pass. Tool `cloud_environment.environment_status` không có trong danh sách khả dụng; readiness môi trường quản lý không đo được, không thao tác mạng.
