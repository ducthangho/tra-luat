Verdict: approve
Reviewed commit: 4c73081474b1e2ab0800cc13992c8f86688532ed
Spec sha256: adaf8d2469ac16c46314c3c9ac7667cce90825a053a7b98e12b803c6719040c3; Chung sha256: 4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0

Hoàn tất review: **(a), (b), (c) đạt; P0=0, P1=0, P2=0, P3=0**. 100/100 ca packet loop chọn lọc và hai bộ test ops 11/11 mỗi bộ đạt. SRC giữ nguyên sau review.

Review độc lập, offline, packet #977 / revision 1 / generation 1, lượt 5. Phạm vi: toàn vẹn merge và tác động của b3decc5..ef34d88 đối với đoạn §4/câu §12 đã được duyệt; chạy lại nghiệm thu (a)(b)(c). Mọi phép thử trên bản sao riêng dưới out/. Không sửa SRC, không mạng/GitHub/push/merge/land.

Lý do lượt 5: master tiến từ `b3decc512dd6e0247ec2439870bd06725d79f028` tới `ef34d88838bc125727670f494b15213b6c6f0c8d` sau approval lượt 4. Head đang xét merge head lượt 4 với base mới, không rebase. Đây là biên nhận xác minh đoạn merge đó, không review packet từ đầu. Đã đọc toàn bộ `runs/8b502ef7/prompt.snapshot`, đặc tả con, phần chung, bản chép lease; đối chiếu kết luận/bảng lớp của bốn verdict trước. Lease khớp #977/r1/g1/spec/phân vai; base lease `e139e55` là mốc cấp lịch sử, base của lượt xác minh này do prompt chỉ định. Handoff dành trên nhánh lease không có trong diff packet.

Reviewer: Codex, họ model `openai`; executor theo assignment/lease: Claude, họ `claude`. Review class `sensitive`; assurance target `cross_approved`; các trục review: Spec và Standards/Security. `runs/8b502ef7/run.json` ghi provider `openai_codex`, execution surface `codex_cli`, transport `machine`, run ID `8b502ef70dca48dfbefb676184c73410` (`runtime-observation.json`). Không có telemetry terminal chứng minh exact serving model/effort tại thời điểm đọc; không lấy cấu hình hoặc header làm bằng chứng đã đo. Receipt thực thi/assurance cần được bên vận chuyển đối chiếu sau khi writer kết thúc. Sandbox cấu hình `workspace-write`; SRC được đối xử read-only theo ranh giới công việc.

**Bảng lớp finding**

| slug | hạng P0–P3 | biểu hiện file:dòng | phép đo/tái hiện đã chạy | hướng vá |
|---|---|---|---|---|
| — (không có lớp finding mở) | — | — | (a)(b)(c), 100/100 ca chọn lọc, 11/11 + 11/11 ca ops | Không yêu cầu vá |

Đếm theo nguyên nhân: **0 lớp, 0 biểu hiện**. Áp luật phân hạng bắt buộc: không thấy hành vi/mệnh đề sai, luật mới chưa được mã cưỡng chế, mâu thuẫn protocol hoặc thiếu phần bắt buộc trong phạm vi review hiện hành để xếp P2+. Bốn verdict trước của #977 đều approve, P0–P3=0, nên không có phản chứng/finding cũ còn sống cần phân ĐÃ VÁ THẬT/VÁ HỜ/VÁ SINH LỖI MỚI/CHƯA VÁ; tỷ lệ đóng lớp N/A. Không dựng đột biến độ phủ mới trong lượt này. Các đột biến chạy là ca có sẵn của bộ test ops; không phát hiện nợ mới P3. Theo luật chủ kho, nếu đột biến độ phủ MỚI có A/B vẫn xử lý đúng thì chỉ xếp P3 kèm tên/owner/hướng xử lý, không nâng P2. Nợ lịch sử của packet khác không được nhập hoặc tuyên bố đã đóng ở #977.

**(a) Toàn vẹn merge và write set — ĐẠT**

Ký hiệu lệnh: `H=4c73081474b1e2ab0800cc13992c8f86688532ed`, `B=ef34d88838bc125727670f494b15213b6c6f0c8d`, `M=b3decc512dd6e0247ec2439870bd06725d79f028`, `P=docs/PROTOCOL_DA_PHIEN.md`; `A1..A4` là bốn head đã duyệt trong prompt. `commands.jsonl` lưu argv đầy đủ, cwd, rc, stdout/stderr; rg qua stdin có SHA-256 đầu vào. Git đọc SRC với `GIT_OPTIONAL_LOCKS=0`; nghiệm thu chạy trong `out/review-copy/`.

| Lệnh / phép đo | rc | Bằng chứng dương |
|---|---|---|
| `git rev-parse HEAD HEAD^{tree} refs/remotes/origin/master` (đo từng đối tượng) | 0 mỗi lệnh | HEAD=H; tree=`63d7774375cfdcbc6be2e32481d95fc5285641fd`; origin/master=B. `identity.json`. |
| `git symbolic-ref -q HEAD`; `git rev-parse --is-shallow-repository` | 1 mong đợi / 0 | Detached; shallow=`false`; `.git` là thư mục thật. |
| `git -c core.fsmonitor=false status --porcelain=v1 --untracked-files=all --ignored` | 0 | SRC sạch ở đầu/cuối; copy cũng sạch cuối lượt. |
| `sha256sum tham-chieu/wp977.md src/ops/specs/may-adr-0054-chung.md` | 0 | Đúng hai băm đầy đủ ở dòng 3; `spec-hashes.txt`. |
| `git merge-base --is-ancestor <B/M/A1/A2/A3/A4> H` | 0 cả 6 lệnh | Base mới, base cũ và bốn head đã duyệt đều là tổ tiên H. |
| `git show -s --format='%H %P' H` | 0 | Parents đúng `c3124e5ad50810a725048aee6913b032855a75d5` và B. `parents.txt`. |
| `git rev-parse H:P A1:P A2:P A3:P A4:P`; `git diff --exit-code Ai H -- P` | 0 từng lệnh | Cả năm cùng blob **`a8f689d11b2eab370de68d6dc197a97f72420e94`**; bốn diff rỗng. `protocol-oids.txt`. |
| `git diff --name-status B H`; `git diff --numstat B H` | 0 / 0 | Đúng một tệp P: **19 dòng thêm, 2 dòng xóa**; 19 ≤ 40. |
| `git diff B H`; `git diff --check B H` | 0 / 0 | Chỉ §4 ngay sau đoạn approved_pending và câu §12; không lỗi whitespace. `candidate.diff`. |
| `git cat-file blob H:P`, so bytes với SRC và copy | 0; assertion đạt | Bytes trên đĩa đúng blob đã duyệt. Copy vật lý đầy đủ, không hardlink, không object alternates. |

M1/M2 đầy đủ và giữ nguyên như bốn head đã duyệt; không có thay đổi code hay mục protocol khác trong diff packet.

**(b) Tác động của `b3decc5..ef34d88` — không làm sai §4/§12**

`git diff --stat M B`, `--name-status`, `--numstat` đều rc=0: **4 tệp, 277 dòng thêm, 19 dòng xóa**. Đã đọc toàn bộ `master.diff` và toàn bộ `ops/kiem_ho_so_land.py`. Các tệp là `ops/codex_cloud_setup.sh`, `ops/codex_cloud_setup_test.py`, `ops/kiem_ho_so_land.py`, `ops/kiem_ho_so_land_test.py`; không có “một số tệp ngoài” khác trong đoạn đo này.

`git diff --exit-code M B -- docs/ .claude/ .github/ .agents/ AGENTS.md CLAUDE.md ops/bien_nhan_v2.py ops/lease_publish.py ops/bash_nen.py` **rc=0**; phép tương tự `A4 H` **rc=0**. OID cây/tệp M và B cũng khớp độc lập (`unchanged-objects.json`). Máy trạng thái, harness packet loop, validator biên nhận/lease và các nguồn doctrine/ADR không đổi.

| Nội dung tại H | Đánh giá tác động |
|---|---|
| `ops/kiem_ho_so_land.py:10`, `:62`, `:100` | Bổ sung đọc khối mức gốc `landed_<8 chữ số>` trong hồ sơ land. Khối `landed is True` phải có quyết định `da_duyet` và comment URL phù hợp; `authorized_head_sha` vẫn bắt buộc. Đây là kiểm cấu trúc/thẩm quyền khai trong hồ sơ, không phải lệnh chuyển state packet. |
| `ops/kiem_ho_so_land.py:119`, `:153` | Chỉ quét `ops/land/*-land-evidence.yaml`, xuất báo cáo và rc; không đọc protocol/state journal, không gọi packet loop, không ghi state. `DAT` ở đây là đạt L-6, không tuyên bố mission complete, không cấp đường rời `cho_chu_kho` hoặc quyền đẩy. Vì vậy không mâu thuẫn §4:248–263 hoặc §12:1158–1159. |
| `ops/kiem_ho_so_land_test.py:267`, `:391` | Thêm kiểm kiểu b và các đột biến có sẵn để bảo vệ validator; không sửa nghiệm thu của protocol. Full bộ riêng đạt 11/11 trên H. |
| `ops/codex_cloud_setup.sh:43`, `:89` và test đi kèm | Setup đặt PATH/LOCALAPPDATA ở đầu bashrc, giữ nội dung/quyền và hủy khi grep lỗi. Chỉ thay môi trường setup, không thêm luật packet hay sửa scanner. Test dùng HOME/công cụ giả dưới OUT, đạt 11/11, 8/8 đột biến có sẵn bị bắt đúng lý do. Không chạy setup cài đặt thật. |

`rg -n 'cho_chu_kho|mo.lai|chu.kho.duyet|§12|mission|complete|PROTOCOL|packet_loop' ops/kiem_ho_so_land.py` **rc=1** đúng kỳ vọng, không khớp. `rg -n 'kiem_ho_so_land|codex_cloud_setup' .claude/dev/packet_loop.py .claude/dev/packet_loop_test.py` cũng **rc=1**, không phụ thuộc trực tiếp. Kết luận không chỉ dựa trên tìm từ: đã đọc đường đọc YAML/kiểm/CLI và đối chiếu với `cmd_mo_lai:2949`, `cmd_chu_kho_duyet:2997`, `_xet_dung:3042` không đổi. §12 vẫn là nghĩa vụ chặn hoàn tất mission, không tuyên bố công cụ L-6 cưỡng chế toàn bộ nghĩa vụ đó.

**(c) Nghiệm thu trên H — các phép bắt buộc đã ĐẠT**

Môi trường Linux; Python **3.13.17**, Git **2.43.0**, ripgrep **15.2.0** (`versions.json`). Dùng `PYTHONDONTWRITEBYTECODE=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null`, `GIT_OPTIONAL_LOCKS=0`, `GIT_ALLOW_PROTOCOL=file`; `TMPDIR`/`TMP`/`TEMP` dưới `out/tmp/`. Chỉ đặt `core.abbrev=7` trong copy; harness tự cô lập Git khi tạo fixture. Remote của ca checkpoint là kho file cục bộ, không truy cập mạng.

Ba biểu thức nguyên văn truyền cho `rg -n`:

```text
cho_chu_kho
approved_pending.*cho_chu_kho|cho_chu_kho.*approved_pending
chu-kho-duyet
```

| Lệnh / phép đo trên copy | rc | Bằng chứng dương / đối chứng |
|---|---|---|
| `rg -n <biểu thức 1> docs/PROTOCOL_DA_PHIEN.md` | 0 | Khớp dòng **253, 256, 1158**; có hai dòng trong §4. `rg-head-1.txt`. |
| `rg -n <biểu thức 2> docs/PROTOCOL_DA_PHIEN.md` | 0 | Khớp đúng câu §12 dòng **1158**. `rg-head-2.txt`. |
| `rg -n <biểu thức 3> docs/PROTOCOL_DA_PHIEN.md` | 0 | Khớp dòng **256, 259, 261**. `rg-head-3.txt`. |
| `git show 09db703:P`, bytes đưa vào từng `rg -n` | show 0; rg **1/1/1** mong đợi | Ba stdout rỗng; `original-protocol.md`, `rg-original-*.txt`. |
| `git show B:P`, bytes đưa vào từng `rg -n` | show 0; rg **1/1/1** mong đợi | Ba stdout rỗng; `base-protocol.md`, `rg-base-*.txt`. rc show/rg ghi riêng. |
| `python .claude/dev/packet_loop.py doctrine-scan --root .` | **0** | `sạch — đã quét 10 tệp, 0 chỗ chép doctrine`. `doctrine-scan.txt`. |
| `python .claude/dev/packet_loop.py adr-song --root .` | **0** | `55 ADR trên đĩa, 55 dòng trong §20, khớp 1–1`; ngoại lệ trạng thái có sẵn 0016. `adr-song.txt`. |
| `python -B ops/kiem_ho_so_land_test.py` | **0** | **11/11**; gồm ca/đột biến có sẵn của thay đổi mới. `kiem_ho_so_land-test.txt`. |
| `python -B ops/codex_cloud_setup_test.py` | **0** | **11/11**, **8/8 đột biến bị bắt đúng lý do**, không bỏ qua. `codex_cloud_setup-test.txt`. |
| `python -B ops/kiem_ho_so_land.py --root . --json` | **0** | **23/23** hồ sơ landed True đạt, 0 miễn trừ. Đây là kiểm local L-6, không xác minh authority GitHub live. `land-scan.json`. |
| `PYTHONDONTWRITEBYTECODE=1 python3 -u out/run_selected.py` | **0** | **100/100 đạt, failed=0, skipped=0**, 164,85 giây; `selected-tests.log`, `selected-results.json`, `selected-receipt.json`. |
| `PYTHONDONTWRITEBYTECODE=1 python3 out/audit.py finish` | **0** | **8.249 mục SRC, 0 delta** nội dung/mode/path, gồm `.git`; HEAD/tree/ref/spec hashes giữ nguyên. `src-before.json`, `src-after.json`, `source-integrity.json`. |

Lệnh bao `PYTHONDONTWRITEBYTECODE=1 python3 out/audit.py acceptance` **rc=0**, marker `ACCEPTANCE_OK`. `run_ops.py` **rc=0**, chạy hai bộ test và kiểm local L-6 như bảng trên.

Tập chọn lọc được tìm từ `rg -n 'PROTOCOL_DA_PHIEN|kiem_ho_so_land' .claude/dev/packet_loop_test.py` (**rc=0**, `test-discovery.txt`). Không có match `kiem_ho_so_land` trong harness này; bộ ops được chạy riêng. Dùng chính `chay_suite` trên H với **17 doctrine_scan + 40 adr_song + 43 r813 = 100**; danh sách ở `selected-cases.json`, số theo nhóm ở `selected-scope.json`, argv/rc/stdout/stderr CLI ở `selected-calls.jsonl`. Các ca đọc protocol thật, kiểm scanner dương/âm, dựng lease/receipt/checkpoint qua Git file và kiểm hai cửa mở lại, phạm vi quyền, tuple generation/head/spec, bộ đếm, từ chối đầu vào sai và giữ nguyên state. Không sửa mã sản phẩm hoặc test trong copy để làm đạt. Log có SyntaxWarning sẵn tại `packet_loop_test.py:3720` về chuỗi đột biến `\d`; 100 ca vẫn hoàn tất, không phải failure hay skipped.

**Giới hạn đo và hiệu lực verdict:** full `python .claude/dev/packet_loop_test.py` và mutation matrix của packet loop **not_run bởi reviewer**. Chỉ thị prompt lượt 5 cho lấy N/N trên exact head đẩy từ job CI `ci.yml`, thay việc lặp suite 45–60 phút cục bộ; do đó không coi miễn chạy full suite cục bộ là thiếu mục nghiệm thu bắt buộc của lượt xác minh này. Các số executor 981/981 trên head cũ là thông tin giao việc, không phải kết quả reviewer đo. CI trên H **chưa được xác minh**, không tuyên bố full suite/CI xanh hoặc đủ điều kiện merge. Ruff pin/probe, bare lint, Windows và kiểm live **not_run**, ngoài phạm vi được giao. Snapshot chỉ chứng minh không có delta quan sát được giữa hai mốc, không chứng minh toàn bộ lịch sử thao tác. Receipt terminal/rc launcher phải được đối chiếu sau run.

Verdict chỉ neo commit **`4c73081474b1e2ab0800cc13992c8f86688532ed`**, **không cấp quyền push, merge hay land**. Packet này không kích hoạt ADR-0054. Mọi thay đổi code, các mục protocol khác và #814/#815/#816 nằm ngoài phạm vi xếp hạng.
