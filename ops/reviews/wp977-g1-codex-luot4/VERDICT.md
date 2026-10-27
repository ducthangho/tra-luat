Verdict: approve
Reviewed commit: c3124e5ad50810a725048aee6913b032855a75d5
Spec sha256: adaf8d2469ac16c46314c3c9ac7667cce90825a053a7b98e12b803c6719040c3; Chung sha256: 4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0

Hoàn tất review độc lập, offline, packet **#977 / revision 1 / generation 1**, lượt 4 xác minh merge. **(a), (b), (c) đều đạt; P0=0, P1=0, P2=0, P3=0**, không có biểu hiện lỗi trong phạm vi được giao.

Lý do lượt 4: master tiến từ `c2d84ea` tới `b3decc5` sau approval lượt 3; H là merge head lượt 3 với base mới. Đây là biên nhận riêng cho tác động của đoạn merge ấy, không mở lại review packet từ đầu. Đã đọc toàn bộ `runs/4f2346e0/prompt.snapshot`, đặc tả con, phần chung, bản chép lease và đối chiếu ba verdict trước. Base lease `e139e55` là mốc cấp lịch sử; base review B do assignment chỉ định. Lease khớp packet/revision/generation/spec/phân vai; handoff được dành trên nhánh lease không xuất hiện trong diff packet.

Reviewer: Codex, họ model `openai`; executor theo assignment/lease: Claude, họ `claude`. Review class `sensitive`, assurance target `cross_approved`; hai trục Spec và Standards/Security. `runs/4f2346e0/run.json` ghi provider `openai_codex`, execution surface `codex_cli`, transport `machine`, run ID `4f2346e06e5649b69f4fd961384c76ce` (ảnh chụp chọn trường: `runtime-observation.json`). Run đang chạy khi đọc, chưa có trường telemetry model/effort/sandbox terminal: không tự khai exact serving model/effort đã đo, không lấy header hoặc cấu hình thay telemetry. Sandbox phiên cấu hình `workspace-write`; SRC được đối xử read-only theo ranh giới công việc. Verdict nội dung không tự hoàn tất receipt thực thi/assurance sau run.

Không kế thừa context executor; không truy cập mạng/GitHub, không push/merge/land. Git refs và readback trong bundle là snapshot cục bộ. Mọi tệp do reviewer tạo ở `out/`; mọi phép thử thực thi trên bản sao vật lý `out/review-copy/`, không dùng hardlink hoặc object alternates.

**Bảng lớp finding**

| slug | hạng P0–P3 | biểu hiện file:dòng | phép đo/tái hiện đã chạy | hướng vá |
|---|---|---|---|---|
| — (không có lớp finding mở) | — | — | Các phép (a), (b), (c) bên dưới | Không yêu cầu vá |

Đếm theo nguyên nhân: **0 lớp, 0 biểu hiện**. Áp luật phân hạng chủ kho: không phát hiện hành vi/mệnh đề sai, luật mới chưa được mã cưỡng chế, mâu thuẫn protocol hoặc thiếu mục bắt buộc để xếp P2+. Không tự dựng đột biến độ phủ mới trong lượt này, nên không phát sinh P3. Nếu chỉ có đột biến độ phủ MỚI mà A/B vẫn xử lý đúng thì phải ghi P3 có tên/owner/hướng xử lý, không nâng P2.

Ba verdict #977 lượt 1–3 đều approve, P0–P3 bằng 0; không có finding/phản chứng mở kế thừa cần phân ĐÃ VÁ THẬT/VÁ HỜ/VÁ SINH LỖI MỚI/CHƯA VÁ. Tỷ lệ đóng lớp N/A. Nợ P3 lịch sử của **#813** không phải finding kế thừa của **#977** và không được tuyên bố đã đóng trong lượt này.

**(a) Toàn vẹn merge và write set — ĐẠT**

Ký hiệu dùng trong lệnh:

```text
H=c3124e5ad50810a725048aee6913b032855a75d5
B=b3decc512dd6e0247ec2439870bd06725d79f028
M=c2d84ea7c20e835968b630a4fb1b8daa29ac12c7
A1=e05ea6a11eb689e1cebb11b417a56930cec8f11e
A2=7c789142ce2a2599fd034a57faa5a6661001ec5f
A3=bd5a66ab01823d6775e1673e64c7da42f7e80135
O=09db70350414d767b793a71cb630e643f216a1b1
P=docs/PROTOCOL_DA_PHIEN.md
```

`commands.jsonl` lưu argv đầy đủ, cwd, rc, stdout/stderr; với rg đọc stdin có thêm SHA-256 đầu vào. Git preflight/diff đọc tại SRC, nghiệm thu chạy tại copy.

| Lệnh / phép đo | rc | Bằng chứng dương |
|---|---|---|
| `git rev-parse HEAD HEAD^{tree} refs/remotes/origin/master` | 0 | HEAD=H, tree=`ce2b357c872065717cc73b474e012d87647e8eb8`, ref master=B; đầu/cuối khớp. |
| `git symbolic-ref -q HEAD`; `git rev-parse --is-shallow-repository` | 1 mong đợi / 0 | Detached; shallow=`false`; `.git` là thư mục thật. |
| `git -c core.fsmonitor=false status --porcelain=v1 --untracked-files=all --ignored` | 0 | stdout rỗng đầu/cuối; copy cũng sạch sau nghiệm thu. |
| `sha256sum tham-chieu/wp977.md src/ops/specs/may-adr-0054-chung.md` (đường dẫn tuyệt đối trong log) | 0 | Khớp đủ hai băm ở dòng 3, kiểm lại cuối lượt. |
| `git merge-base --is-ancestor B H`; tương tự M/A1/A2/A3→H | 0 từng lệnh | Base mới, base cũ và cả ba head đã duyệt đều là tổ tiên H. |
| `git show -s --format='%H %P' H` | 0 | Hai parents đúng thứ tự **A3, B**; `parents.txt`. |
| `git rev-parse H:P A1:P A2:P A3:P` | 0 | Cả bốn cùng blob **`a8f689d11b2eab370de68d6dc197a97f72420e94`**; `protocol-oids.txt`. |
| `git diff --exit-code Ai H -- P` với i=1,2,3 | 0/0/0 | Không diff; protocol giống từng byte với ba bản đã duyệt. |
| `git diff --name-status B H`; `git diff --numstat B H` | 0/0 | Đúng một tệp P, **19 dòng thêm/2 dòng xóa**, 19 ≤ 40. |
| `git diff B H`; `git diff --check B H` | 0/0 | `candidate.diff`: chỉ đoạn văn xuôi §4 ngay sau `approved_pending` và câu §12; không lỗi whitespace. |
| `git cat-file blob H:P` và so bytes tại SRC/copy | 0; assertion đạt | Bytes trên đĩa đúng blob đã review; cũng kiểm `packet_loop.py`, `bien_nhan_v2.py`, `lease_publish.py`; `working-bytes.json`. |

M1/M2 giữ nguyên và đầy đủ; không sửa code hoặc các mục protocol khác trong diff packet.

**(b) Tác động của `c2d84ea..b3decc5` — không làm sai §4/§12**

`git diff --stat M B`, `--name-status`, `--numstat` đều **rc=0**: **65 tệp mới, 23.996 dòng thêm, 0 dòng xóa**, toàn bộ dưới `ops/land/` (`master-stat.txt`, `master-paths.txt`, `master-numstat.txt`; toàn diff lưu `master.diff`). Đây là một hồ sơ land YAML, một manifest SHA256SUMS và 63 hiện vật provenance của #813/PR #969.

`git diff --exit-code M B -- docs/ .claude/ .agents/ .github/ ':(glob)ops/*.py' CLAUDE.md AGENTS.md` **rc=0**. OID của các cây/tệp này và hai validator `ops/bien_nhan_v2.py`, `ops/lease_publish.py` cũng được đối chiếu độc lập (`unchanged-objects.json`). `git diff --exit-code A3 H -- docs/ .claude/ .agents/ .github/ ':(glob)ops/*.py'` **rc=0**. Hai tệp Python mới là bản chép công cụ thu thập tại `ops/land/pr969-wp813-provenance/do-lai-nguon-20261027/{readback,kiemgate}.py`; không phải thay đổi Python trực tiếp dưới `ops/`, không sửa đường thực thi nghiệm thu và reviewer không chạy chúng.

Đã đọc hồ sơ land, nội dung PR, trao đổi connector/chủ kho liên quan, verdict #813 lượt 6 và các đoạn lịch sử liên quan. Script `PYTHONDONTWRITEBYTECODE=1 python out/land_audit.py` **rc=0**: parse 41 JSON, trích và đọc đủ 20 body/title duy nhất chứa các chủ đề cần đối chiếu (`land-relevant-bodies.{json,txt}`). `sha256sum -c SHA256SUMS` tại provenance trong copy **rc=0, 63/63 OK** (`land-sha256-check.txt`); đây là kiểm byte bundle, không xác thực lại GitHub live.

| Nội dung mới và neo trong H | Đánh giá đối với §4/§12 |
|---|---|
| `ops/land/pr969-wp813-provenance/readback-pr-969.json`, trường `body`, M2/M3 | Mô tả `ci-do → running`, `connector → cho_chu_kho`, connector từ running đòi quyền ci-do cùng generation/head và chưa mở lượt mới; checkpoint master cho phép vá, quyền đẩy riêng. Khớp protocol:248–263 và mã `packet_loop.py:2949`, `:2997`. |
| `readback-review-comments-969.json:9`, `:32`, `:175`; comment chủ kho `6436510218` | Finding về quyền ci-do cũ neo `25bd151`, có trả lời đã vá ở `be88caf`. Mã hiện hành:2955–2958 kiểm không có `begin_attempt` sau `mo_lai` cuối; protocol:253–254 ghi đúng điều kiện ấy. Không diễn giải finding lịch sử thành lỗi còn mở trên H. |
| `verdicts/wp813-g1-claude-review-6-codex-verdict.md:9`; `pr969-wp813-land-evidence.yaml:115` | Nợ P3 gồm mixed refs và chuỗi ci-do → begin → void → connector; hồ sơ nói mã xử lý đúng, thiếu ca/đột biến khóa chốt. Không tuyên bố một cạnh thoát khác khỏi `cho_chu_kho`, không đổi phạm vi `cho_phep_va`/`cho_phep_day`. Không mở lại hoặc nâng hạng nợ code ngoài packet #977. |
| `pr969-wp813-land-evidence.yaml:116` | M4 §4/§12 được ghi là việc tách khỏi #813 r2. Câu lịch sử “Chủ kho chưa mở packet” không phải trạng thái hiện hành của #977: assignment, spec và lease #977 xác định việc đã được giao. Đây là ghi chú bookkeeping chưa cập nhật, không làm sai mệnh đề state machine hay nghiệm thu đang review; ngoài phạm vi xếp hạng. |
| `pr969-wp813-land-evidence.yaml:90`, `:92`, `:94`, `:99`; dòng 2 | Giữ `merged: true`, **`landed: false`**, nêu thiếu gate đúng merge SHA và assurance; ghi rõ không kích hoạt ADR-0054. Không tuyên bố mission complete khi gate chưa xanh, phù hợp câu §12:1158–1159. “Mo lai” trong điều kiện bổ sung evidence land không cấp cạnh CLI `mo-lai` mới. |

Các hàm `cmd_mo_lai`, `cmd_chu_kho_duyet`, `_xet_dung` và validator không đổi; các điều kiện refs, tuple checkpoint, quyền riêng, bộ đếm và tiêu thụ quyền trong đoạn §4 vẫn đúng. §12 giữ nghĩa vụ không complete khi còn trạng thái/gate chưa xong, không khai một lệnh máy complete mission mới. `doctrine-scan` đọc adapters/CLAUDE/protocol (`packet_loop.py:1625`); `adr-song` đọc `docs/adr` và §20 (`:1916`), không lấy hồ sơ land làm nguồn luật. Đã chạy lại cả hai trên H, không suy pass từ cây không đổi.

Ghi chú phép đo: lần đầu script reviewer dùng pathspec Git `ops/*.py`, vốn khớp cả Python ở thư mục con, nên `git diff --exit-code` trả **rc=1** và script dừng. Output chỉ ra đúng hai bản chép provenance nói trên. Đã sửa bộ đo thành `:(glob)ops/*.py` để đo tệp trực tiếp dưới ops, chạy lại **rc=0**; log ban đầu được giữ nguyên. Đây là lỗi kỳ vọng của bộ đo reviewer, không phải gate sản phẩm thất bại hoặc finding.

**(c) Nghiệm thu trên head mới — ĐẠT**

Copy ghim H/tree/ref như (a). Môi trường Linux; Python **3.13.17**, Git **2.43.0**, ripgrep **15.2.0**. `PYTHONDONTWRITEBYTECODE=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null`, `GIT_OPTIONAL_LOCKS=0`, `GIT_ALLOW_PROTOCOL=file`; `TMPDIR`/`TMP`/`TEMP` nằm dưới `out/tmp/`. Chỉ cấu hình `core.abbrev=7` trong copy. Lệnh bao `PYTHONDONTWRITEBYTECODE=1 python out/audit.py acceptance` **rc=0**, marker `ACCEPTANCE_OK`.

Ba biểu thức được truyền nguyên văn cho `rg -n`:

```text
cho_chu_kho
approved_pending.*cho_chu_kho|cho_chu_kho.*approved_pending
chu-kho-duyet
```

| Lệnh / phép đo tại copy | rc | Bằng chứng dương / đối chứng |
|---|---|---|
| `rg -n <biểu thức 1> docs/PROTOCOL_DA_PHIEN.md` | 0 | Khớp **253, 256, 1158**, gồm §4; `rg-head-1.txt`. |
| `rg -n <biểu thức 2> docs/PROTOCOL_DA_PHIEN.md` | 0 | Khớp đúng câu §12, **1158**; `rg-head-2.txt`. |
| `rg -n <biểu thức 3> docs/PROTOCOL_DA_PHIEN.md` | 0 | Khớp **256, 259, 261**; `rg-head-3.txt`. |
| `git show O:P`, đưa bytes vào từng `rg -n` ở trên | show 0; rg **1/1/1** mong đợi | Cả ba stdout rỗng; `old-base-protocol.md`. |
| `git show B:P`, đưa bytes vào từng `rg -n` ở trên | show 0; rg **1/1/1** mong đợi | Cả ba stdout rỗng; `new-base-protocol.md`. rc show và rg ghi riêng, không bị pipeline che lỗi. |
| `python .claude/dev/packet_loop.py doctrine-scan --root .` | **0** | `sạch — đã quét 10 tệp, 0 chỗ chép doctrine`; `doctrine-scan.txt`. |
| `python .claude/dev/packet_loop.py adr-song --root .` | **0** | `55 ADR trên đĩa, 55 dòng trong §20, khớp 1–1`; ngoại lệ trạng thái có sẵn `0016`; `adr-song.txt`. |
| `PYTHONDONTWRITEBYTECODE=1 python out/audit.py finish` | **0** | **8.243 mục SRC, 0 delta** byte/mode/path, gồm `.git`; HEAD/tree/ref/spec giữ nguyên; `src-before.json`, `src-after.json`, `source-integrity.json`. |

**Giới hạn đo:** full `python .claude/dev/packet_loop_test.py`, tập chọn lọc và mutation matrix **not_run bởi reviewer**; prompt lượt 4 miễn full suite và giao executor chạy riêng trên H. Không có log kết thúc full suite của executor trong bằng chứng đã kiểm, nên không tuyên bố N/N/full suite/CI xanh hoặc đủ điều kiện merge. Ruff pin/probe, bare lint, Windows và kiểm live **not_run**, ngoài nghiệm thu merge được giao. Không bỏ phép bắt buộc nào của (a)(b)(c). Snapshot chỉ chứng minh không có delta quan sát được giữa hai mốc, không chứng minh toàn bộ lịch sử thao tác. Receipt terminal cần đối chiếu sau khi writer kết thúc.

Verdict chỉ neo **`c3124e5ad50810a725048aee6913b032855a75d5`**, **không cấp quyền push, merge hay land**. Packet này không kích hoạt ADR-0054. Mọi thay đổi code, các mục protocol khác và #814/#815/#816 nằm ngoài phạm vi xếp hạng.
