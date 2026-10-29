Verdict: approve
Reviewed commit: 65e623b4357906b4a2406d5923ae7e45f3eed965
Spec sha256: 6c21bd26b64aa5a57925875789a8d9f9f3132a00ae53416b1ac4d0ad703e3eef

Không phát hiện P0/P1/P2/P3 mới. Hai finding của lượt 1 đã được vá thật. Head đạt `t27` 2/2, toàn suite 268/268 và validator biên nhận `TỔNG: ĐẠT`. Các đột biến bắt buộc chết đúng chốt; dữ liệu hai biên nhận khớp hiện vật Git. Approve chỉ áp dụng exact SHA ở dòng 2, không cấp quyền merge/land và không chứng nhận CI/Windows chưa đo.

Reviewer: OpenAI Codex (`openai_codex`), phiên độc lập với executor Claude. Bề mặt quan sát là agent qua API với công cụ shell trong sandbox Linux (`codex_service` theo danh mục của kho), transport `machine`; không có bằng chứng để tự khai phiên này chạy qua `codex exec`, hoặc chứng nhận model/effort thực phục vụ. Review class `sensitive`, r1, lượt 2 theo SPEC/prompt. Cây `cay-kho/` không có delta nội dung quan sát được đầu/cuối; thay đổi cấu hình duy nhất là `git config core.abbrev 7` theo chỉ thị. Sandbox cho phép ghi cây này, nên read-only ở đây là kỷ luật thực hiện, không phải cưỡng chế quyền hệ thống. Đột biến chạy ngoài cây nguồn; Python dùng `PYTHONDONTWRITEBYTECODE=1`, các fixture Git dùng `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null`.

**Findings**

Không có finding mới cần liệt kê theo mẫu `[P0..P3]`. Tổng P0/P1/P2/P3 của review này: **0/0/0/0**. Không tính tiền đề sai “không có run.json” trong SPEC M4 thành lỗi của diff, theo chỉ thị lượt 2.

**ĐỐI CHIẾU LƯỢT TRƯỚC**

Nguồn: `VERDICT-LUOT1.md`, reviewed SHA `183e28f4b59467895c411db7f565dd21769ee511`.

| Finding cũ | Kết luận | Bằng chứng tự đo trên head hiện tại |
|---|---|---|
| P2 `wp1006-runtime-artifacts-falsely-absent` | **ĐÃ VÁ THẬT** | `python3 audit_receipts.py` rc=0, `ALL_AUDIT_ASSERTIONS=PASS`: run_id/head/rc/thời lượng/prompt hash, byte verdict, mỏ neo và ancestry khớp. Đọc cả hai receipt và bốn hàng README mới; không còn câu phủ nhận run.json/prompt tồn tại. Hạn chế còn lại được ghi đúng là không đo được model/effort thực phục vụ. |
| P3 `wp1006-listing-boundaries-unmeasured` | **ĐÃ VÁ THẬT** | `python3 measure_mutations.py` rc=0: `c2_no_is_file` và `c3_receipt_glob_in_checker` đều rc=1, 0/1 ở đúng ca `t27_phan_chung_*`, đúng thông báo dưới đây. `c4_receipt_glob_in_helper` cũng chết đúng chốt. |

**Các cổng đã đo**

- `PYTHONDONTWRITEBYTECODE=1 python3 cay-kho/ops/lease_publish_test.py --chi-ca=t27_`: rc=0, `lease_publish: 2/2 đạt; đã chạy=2, bỏ qua=0` (`evidence/head-t27.log`).
- Base xuất bằng `git archive 79dbaf443f90daece751d9ab2537796bbd6084bf ops/lease_publish_test.py ops/reviews`; cùng lệnh chọn `t27_` trên `base-copy/`: rc=0, `1/1 đạt; đã chạy=1, bỏ qua=0` (`evidence/base-t27.log`).
- Trong `cay-kho`, `PYTHONDONTWRITEBYTECODE=1 python3 ops/bien_nhan_v2.py --root .`: rc=0, `246 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 299`, `TỔNG: ĐẠT` (`evidence/receipt-validator.log`).
- `PYTHONDONTWRITEBYTECODE=1 python3 measure_mutations.py`: rc=0; control `1/1`, cả 9 đột biến `0/1`. Hai đột biến bắt buộc (a)/(b) chết đúng chốt; bỏ `is_file()` và glob riêng receipt trong checker đều chết đúng thông báo. Đột biến đổi gốc chết bằng `ValueError`, KHÔNG tính là tín dụng bắt lỗi glob. Log và mã tái hiện nằm ở `evidence/mutations-summary.log`, `evidence/mutations.json`, `mutations/`.
- Bare Ruff `ruff check --no-cache --select F --output-format json <base/head>/ops/lease_publish_test.py`, Ruff 0.16.9: mỗi bên rc=1 với 7 F401 + 2 F541; so cặp `(code,message)` cho `ruff_F_delta_zero True`. Không gọi bare lint là xanh tuyệt đối.
- Trong `cay-kho`, `git diff --check 79dbaf4 HEAD`: rc=0, không output; `PYTHONDONTWRITEBYTECODE=1 python3 .claude/dev/packet_loop.py doctrine-scan --root .`: rc=0, `sạch — đã quét 10 tệp, 0 chỗ chép doctrine`.
- Trong `cay-kho`, `PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null python3 ops/lease_publish_test.py`: **rc=0, `lease_publish: 268/268 đạt; đã chạy=268, bỏ qua=0`** (`evidence/full-suite.log`, `evidence/full-suite.rc`). `python3 final_integrity.py` kiểm nhật ký: 268 lượt vào, 268 lượt ra, 268 tên khác nhau, cùng thứ tự, 0 thất bại, 0 bỏ qua. Không có ca thiếu mạng/actionlint/shellcheck cần loại khỏi kết quả lần chạy này.

**Head, base và phạm vi**

Các lệnh Git trong `audit_receipts.py` chạy ở `cay-kho/`. Script này rc=0; toàn bộ output tại `evidence/receipt-audit.log`.

| Phép đo | Kết quả |
|---|---|
| `git rev-parse HEAD HEAD^{tree}` | `65e623b4357906b4a2406d5923ae7e45f3eed965`; tree `1d62bc326b67e3e22a714a96140871583211f2fe` |
| `git rev-parse 79dbaf4^{tree}` | `b95fb2108ab139c9a31f6f107797b00aa704ab34` |
| `git branch --show-current`; `git rev-parse --is-shallow-repository` | nhánh rỗng (detached); `false`; `.git` là thư mục |
| `git remote get-url origin`; `git config core.abbrev` | `https://github.com/ducthangho/tra-luat.git`; `7` |
| `sha256sum SPEC.md` từ sandbox | khớp dòng 3, không đổi |
| `git diff --stat 79dbaf4 HEAD` | 7 tệp, 417 dòng thêm, 6 dòng bỏ: gồm 4 tệp packet và 3 tệp merge master |
| `git diff --name-only 183e28f b1be853` | chỉ ba tệp `ops/land/pr870-claude-md-bai-hoc-c-land-evidence.yaml`, `ops/land/pr889-claude-md-bai-hoc-c-land-evidence.yaml`, `ops/land/pr896-claude-md-bai-hoc-c-tro-nguon-land-evidence.yaml` |
| So byte `git diff 79dbaf4 0a8f4d7` với `git diff 183e28f b1be853` | bằng nhau; merge master không chạm write set |
| `git diff --name-only 0a8f4d7 HEAD` | đúng `ops/lease_publish_test.py`, `ops/reviews/README.md`, hai `wp929-g1-codex-luot{1,2}-VERDICT.receipt.yaml` |
| So byte diff theo phạm vi snapshot | `DIFF.patch_byte_equal PASS`; `DIFF-LUOT2.patch_byte_equal PASS` |
| `git status --porcelain=v1 --ignored` đầu/cuối; `git diff --exit-code`; `git diff --cached --exit-code` cuối | rc=0, output rỗng; HEAD/tree giữ nguyên |

Kiểm cuối: `PYTHONDONTWRITEBYTECODE=1 python3 final_integrity.py` rc=0, `evidence/final-integrity.log`. Snapshot sạch không chứng minh lịch sử “chưa từng ghi rồi hoàn nguyên”; chỉ khẳng định không có delta quan sát được. Môi trường đo: Linux x86_64, Python 3.13.17; `ruff --version` 0.16.9, `actionlint -version` 1.7.7, `shellcheck --version` 0.9.0, `pandoc --version` 3.1.3.

**Đột biến và tính thực chất của ca phản chứng**

`measure_mutations.py` tạo bản riêng tại `mutations/<tên>/ops/lease_publish_test.py`, rồi chạy `python3 <bản-sao>/ops/lease_publish_test.py --chi-ca=t27_phan_chung_`. Tất cả đều chạy đúng **một** ca `t27_phan_chung_verdict_duoi_HOA_thieu_muc_luc_phai_DO_tren_moi_nen`, không dùng `.pyc` cũ. Chi tiết phép thay nguồn và lệnh nằm trong script; log riêng tại `evidence/mutation-<tên>.log`.

| Bản / đột biến | rc; kết quả | Thông báo hoặc chốt gây đỏ |
|---|---|---|
| control | 0; 1/1 | QUA |
| (a) `return sorted(thu_muc.glob("*" + duoi))` | 1; 0/1 | `bộ liệt kê không thấy đủ cả hai cách viết đuôi — nó đang phụ thuộc nền` |
| (b) như (a), bỏ đúng chốt tự kiểm bộ liệt kê đầu tiên | 1; 0/1 | `verdict đuôi ... vắng khỏi mục lục mà _kiem_muc_luc vẫn XANH — chốt mù với đuôi HOA trên nền này (lỗi #1006)` |
| c1: bỏ `lower()` của tên | 1; 0/1 | cùng thông báo bộ liệt kê như (a) |
| c2: bỏ `is_file()` | 1; 0/1 | `bộ liệt kê nhận cả THƯ MỤC mang đuôi verdict — is_file() đã mất` |
| c3: glob riêng `.receipt.yaml` ngay trong `_kiem_muc_luc` | 1; 0/1 | `biên nhận đuôi .RECEIPT.YAML vắng khỏi mục lục mà _kiem_muc_luc vẫn XANH — nhánh duyệt biên nhận còn phụ thuộc nền (lỗi #1006)` |
| c4: helper dùng glob riêng cho receipt | 1; 0/1 | `bộ liệt kê không thấy biên nhận đuôi HOA .RECEIPT.YAML` |
| c5: checker chỉ `return` | 1; 0/1 | cùng thông báo “vẫn XANH” như (b), chống bỏ toàn bộ phép kiểm |
| c6: checker luôn ném lỗi đúng tên verdict/cột | 1; 0/1 | lỗi thoát ra ở lượt đối chứng dương, bắt chặn quá rộng |
| c7: đổi `relative_to(goc)` về `relative_to(HERE.parent)` | 1; 0/1 | `ValueError: ... is not in the subpath of ...`; **không cấp tín dụng bắt lỗi glob** cho lỗi gốc đường dẫn này |

Không có đột biến **SỐNG** trong tập đã chạy. Phạm vi kết luận là ca `t27_phan_chung_*`, không phải toàn suite dưới từng đột biến.

Trace độc lập gắn quanh checker thật (`evidence/fixture-trace.json`, do `measure_mutations.py` sinh) ghi đủ ba lượt:

1. Có `moi-VERDICT.md` nhưng không có hàng mục lục/sidecar, bên cạnh cặp `thuong-verdict.md` hợp lệ: checker đỏ bằng `README.md: verdict 'moi-VERDICT.md' KHÔNG có trong CỘT 'tệp verdict'...`.
2. Thêm sidecar và hàng mục lục của verdict HOA: checker **PASS**.
3. Thêm `le.RECEIPT.YAML` chưa vào mục lục: checker đỏ bằng `README.md: biên nhận le.RECEIPT.YAML KHÔNG có trong CỘT 'biên nhận'...`.

Việc lượt âm đầu chưa có sidecar là chủ ý đúng: nếu có sidecar, nhánh duyệt receipt có thể phát hiện thiếu hàng dù nhánh verdict vẫn mù. Chốt âm/dương không xanh rỗng trong các đột biến đã đo. `python3 probe_contract.py` còn dựng riêng tình huống M3 **có sidecar**: thiếu hàng verdict HOA vẫn đỏ đúng tên/cột, thêm hàng thì xanh (`M3_uppercase_with_receipt_negative=PASS`, `M3_uppercase_with_receipt_positive=PASS`). Đây là kiểm hợp đồng t27; không tuyên bố fixture tổng hợp là hồ sơ review lịch sử đã được validator v2 chứng nhận.

Giới hạn đo bổ sung, **không phải finding mới của packet**: thêm hàng `le.RECEIPT.YAML` vẫn bị checker từ chối, vì `_ten_tep('le.RECEIPT.YAML')` trả `set()`; regex đọc phần mở rộng trong ô bảng vẫn phân biệt hoa thường. `probe_contract.py` so AST `_ten_tep` giữa base/head cho `base_head_ten_tep_AST_identical=True`. Đây là giới hạn sẵn có đã được lượt 1 phân biệt với hợp đồng liệt kê M1. Không suy ca âm receipt mới thành chứng minh toàn checker chấp nhận mọi cách viết HOA. Log phép kỳ vọng dương ban đầu thất bại được giữ ở `evidence/contract-probes-initial.log`; log kiểm giới hạn và M3 cuối ở `evidence/contract-probes.log`, script rc=0, `ALL_CONTRACT_PROBES=PASS`.

**Đối chiếu hai biên nhận với hiện vật**

Lệnh tái hiện: `PYTHONDONTWRITEBYTECODE=1 python3 audit_receipts.py` → rc=0, `ALL_AUDIT_ASSERTIONS=PASS`. Script đọc YAML/JSON, băm byte và chạy Git trực tiếp; không nhận số liệu từ lời khai executor. Nguồn runtime là bộ `ops/land/pr933-wp929-provenance/verdicts/wp929-r1-g1-claude-review-{1,2}-codex-{run.json,prompt.md,stderr-header.txt,verdict.md}`.

| Giá trị tự đo | Lượt 1 | Lượt 2 |
|---|---|---|
| `run_id` | `0d78fe118c6340fda716921de68a5d06` | `3536a415068645adab6cfed3e3de5f03` |
| `head` = `reviewed_sha` = dòng 2 verdict | `8a6d795c982fc7e9da2fbfd28a75ca25d5f3eb95` | `227dcdebc62c9275f9df09056f66e2124ed5f14c` |
| `trang_thai`; `ma_thoat`; giây | `xong`; `0`; `1337.003` | `xong`; `0`; `594.161` |
| SHA-256 prompt, khớp JSON và byte `prompt.md` | `5104ab547b0136c34c67cad01cf082add93a62283bfd4bc624c29fe738c5a4af` | `35f2eb79ff5990b071239fe46c9464e5963ded6037768b396c5a98aea55733f5` |
| Verdict bytes | `11158` | `12184` |
| SHA-256 verdict | `8a392561044c0ae6b9d504260149ff441fb8ec81cfe828fd8e06bd8f27c80bbf` | `40d42d53d7b30f7e703eced0376803907aa3b3a57d1d62dd697adcac25c30e49` |
| Verdict nguồn → nhãn receipt | `request_changes` → `changes_requested` | `approve` → `approve` |
| Số finding P0/P1/P2/P3 từ dòng finding | `0/0/1/3` | `0/0/0/1` |
| Trường `model_phuc_vu` trong JSON | không có | không có |

`findings_ids` khớp từng id và hạng: lượt 1 có `wp929-tree-is-not-activation-file` (P2), `wp929-filename-boundaries-unmeasured`, `wp929-git-error-guards-unmeasured`, `wp929-nfc-unmeasured` (ba P3); lượt 2 chỉ có `wp929-git-error-guards-unmeasured` (P3). Script đếm dòng `- [P*]` và `- **[P*]`, không đếm các chỗ nhắc lại trong prose.

Các quan hệ và lời khai (a) còn lại, đo trong cùng script và `final_integrity.py`:

- `git show <base>:<verdict>` và `git show 8d3f655:<verdict>` đều trùng byte head; bản verdict trong hồ sơ land cũng trùng. Không đổi verdict lịch sử.
- `git log --format=%H [--diff-filter=A] HEAD -- <verdict>` và `git log --all --format=%H -- <hai-verdict>` chỉ có `8d3f6553b5b63dac9d8e79c8e017a0d5a4335cb5`. URL evidence ghim đúng commit/path đó.
- `git merge-base --is-ancestor` cho từng reviewed SHA → `ab94c4f`, `8d3f655` → base, `8d3f655` → `fe46e7e` → base, `f46ddf5` → base và `ab94c4f` → base đều rc=0. `git show -s --format='%H %cI %P %s'` xác nhận `fe46e7e` là merge nhánh lease, anchor có thông điệp `handoff(#929)`.
- Lease `wp929-r1-g1-claude.yaml` ghi cửa sổ `[2026-10-25T15:30:00Z, 2026-10-26T00:33:00Z)`. Committer time của `8a6d795` là `2026-10-25T16:12:52Z`, `227dcde` là `16:42:31Z`, anchor `8d3f655` là `17:29:37Z`: cả ba nằm trong cửa sổ. Đây là thời điểm commit đo được, không suy thành bằng chứng mọi hoạt động runtime nằm trong lease.
- Packet/lease/revision/generation/review_class khớp YAML gốc. Lease tự khai executor `claude`, surface `claude_code`, model `claude-opus-5-5`; receipt giữ nhãn tự khai. Băm `ops/specs/wp929.md` khớp `79251bee45fc39003d13438d741c4e6319dc80ea6b480dc1b931c93d0c6a7ae6` như lease và tiền tố ở README.
- Cả tám hiện vật runtime/trace/verdict đã có ở base và không đổi byte. `git log --format='%H %cI' -- <artifact>` chỉ ra `f46ddf5e64d5e938a334d46084b1b865d609c4b0`, `2026-10-26T01:25:13Z`.
- `run.json` ghi `provider=local_process`, `execution_surface=subprocess`; không coi đó là nhận dạng model. Header có 13 dòng gốc cộng một dòng chú giải, khai `model: gpt-6-astra`, `reasoning effort: xhigh`. Không có toàn stderr trong bộ hiện vật trên; băm toàn stderr trong run.json không thể kiểm bằng excerpt. Hạn chế model/effort và assurance `cross_reviewed` trong receipt là phù hợp với bằng chứng này.
- `git show` cho `ab94c4f` ghi merge PR #933 lúc `2026-10-26T07:29:09+07:00` = `00:29:09Z`; parent thứ hai là `f3b54d260bcdecf5b6d2348730a958e168bf7330`, commit merge có parent đầu `227dcde` và parent thứ hai `36057e8`. Vì vậy approve lượt 2 không neo exact head land. Không nâng thành quyền merge/land hoặc tự chứng nhận `cross_approved`.

Đã đọc toàn bộ hai receipt, các dòng phủ định được trích trong `evidence/receipt-audit.log`, và bốn hàng README mới bằng `git diff 79dbaf4 HEAD -- ops/reviews`. Không còn phủ nhận run.json/prompt; các phủ định hiện tại nói về `model_phuc_vu`, stderr đầy đủ, chứng nhận model và merge authority. Những trường đánh dấu (b) là lời thuật lại vẫn được giữ là lời thuật lại, không được review này nâng thành dữ liệu tự đo.

**README và ba hàng bị cắt bảng**

Diff README chỉ thêm hai hàng Mục lục, hai hàng cảnh báo và bỏ một dòng trống. Hai hàng Mục lục có đúng receipt, head, bytes, số P; hai hàng cảnh báo dùng id `WP929-MODEL-PHUC-VU-KHONG-DO-DUOC`, dẫn đúng runtime artifact, không nói runtime vắng mặt. `t27` 2/2 và audit kiểm từng verdict có đúng hai hàng liên quan.

`audit_receipts.py` lấy đoạn cảnh báo từ base bằng `git show`, render cả base/head qua `pandoc --from=gfm --to=html`, rồi kiểm vị trí HTML của **hàng cùng id** `ANCESTRY-CHI-TREN-NHANH-LA-TRANG-THAI-LICH-SU` (không chỉ tìm tên tệp vì các tên còn xuất hiện ở hàng khác). Kết quả cho cả `doctor-github-mcp-review-6`, `don-nhanh-base-review-4` và `don-nhanh-base-review-5`:

| Bản | Trong hàng bảng | Ngoài bảng | Dòng trống trước doctor |
|---|---|---|---|
| base | `false` | `true` | `true` |
| head | `true` | `false` | `false` |

HTML giữ tại `evidence/readme-warning-base.html` và `evidence/readme-warning-head.html`. Lời khai về tác dụng của việc bỏ dòng trống đã được xác nhận bằng render độc lập.

**Giới hạn nghiệm thu**

- Windows thật, `workflow_dispatch` và check runs CI trên head cuối: **KHÔNG ĐO ĐƯỢC trong lượt review cục bộ này**; không thực hiện thao tác GitHub. Không dùng kết quả Linux hoặc lời khai lịch sử để đánh dấu các gate đó đạt.
- Model/effort thực phục vụ của các run lịch sử và của reviewer hiện tại: **KHÔNG ĐO ĐƯỢC** từ chứng cứ hiện có; không tự gán assurance runtime.
- Không sửa kho, không push/comment, không merge/land. Các script và log tái hiện ở sandbox là bằng chứng review, không phải bản vá sản phẩm.
