verdict: changes_requested
reviewed_sha: c98c33eb3e3260a10cd98dc0a6118981a45b7639
reviewed_base: 8802924d1744b4c3bcde8a198265b86b89c957bc
reviewed_files_sha256:
  CHANGELOG.md: cb75db7011556661542f448d5e5a93f8a90d75367648a96aefdd9b7825239c4c
  RELEASE_MANIFEST.json: 0ff739609a6600a6540e5357c50c2c75d91583342a61c5db5a4a94f48a06aab4
  ops/reviews/README.md: d6af20aa3141c5d2d95205900537ac3ca2c5a6015d81d90dc4073c6897a886c8
  ops/reviews/pr511-review-1-codex-verdict.md: 4e86bc17a72af476d2337bdba170dd569ff503c3bcc3ededf938b2fde5f4e6bf
  ops/reviews/pr511-review-1-codex-verdict.receipt.yaml: 896e5e75f8b42d4242341e3ae66da03a843440d7149a2429d736c7c5c63868b2
  ops/reviews/pr511-review-2-codex-verdict.md: cfe618258d782354b84b9dbeb733bf2861adfc04d94edd4cc3fb85a6effe842e
  ops/reviews/pr511-review-2-codex-verdict.receipt.yaml: d9552731686c100a150c383b853540d441ad9e60f5e3df55539626e9bc05b95f
model_tu_khai: GPT-6 / Codex (tự khai theo ngữ cảnh phiên; không xác thực độc lập backend)
review_round: 4
so_p1: 0
so_p2: 1
so_p3: 0
hint_sha256: a17f443e68231401403060b63899e723b1810d54b55e452ed6c1e88f9643f195

## ĐỐI CHIẾU LƯỢT TRƯỚC

Lượt 3 `approve` 0/0/0 trên `5f45e6e99bcd4cf8a410b99031d4a600bf5e83bb` — **không có finding để đối chiếu**.
Băm lại `nguon/VERDICT.rvhs516-3.md`: `532e022c16f75ba5780de45e4e4056788f58ac275d6638a1fbb5c55088cda968`.

**4/4 tệp pr511 không đổi byte**: hai verdict và hai receipt ở HEAD bằng từng blob tại cha 1 `5f45e6e`.
`git -C cay-kho diff 5f45e6e c98c33e -- 'ops/reviews/pr511-*'` có **0 byte stdout**, rc=0.
Hai verdict cũng bằng byte `nguon/VERDICT.rvhs511-{1,2}.md`.
Bốn SHA-256 ở đầu verdict khớp bốn băm đã ghi trong verdict lượt 3.
Không chạy lại bảng đo lượt 1–3; chỉ đọc phần kết luận và giới hạn land liên quan để phân biệt điều đã biết với delta mới.

**Kết luận về cây Git:** giải xung đột giữ đủ hai phía, không đổi nội dung r369.
**Kết luận về HỒ SƠ được giao:** `changes_requested`, 0 P1 / 1 P2 / 0 P3, vì lời khai tại `EVIDENCE.md:9`
khẳng định có đoạn nguồn riêng của #493 trong README mà cả base lẫn HEAD đều không có.
Không gán sự vắng mặt có sẵn ở base thành lỗi mất nội dung do merge.

## Bảng đo lại

Ghi `VERDICT.md` sơ bộ lúc **2026-09-11T20:34:03.834049+00:00**, bổ sung trong lúc đo;
chốt hồ sơ lúc **2026-09-11T20:43:33.710764+00:00**. Trong giới hạn 25 phút theo đồng hồ môi trường.
Đọc/cổng trên cây gốc; dựng merge, sinh manifest, mutant và commit mô phỏng chỉ trong `scratch/luot1/`.
Không dùng mạng. Băm trong frontmatter là băm 7 tệp worktree, đồng thời đã so bằng blob HEAD.

| Phép đo tự chạy | Kết quả |
|---|---|
| HEAD / base / cha | HEAD `c98c33eb3e3260a10cd98dc0a6118981a45b7639`; `origin/master` và `8802924` cùng bằng `8802924d1744b4c3bcde8a198265b86b89c957bc`. HEAD có đúng hai cha: `5f45e6e99bcd4cf8a410b99031d4a600bf5e83bb`, `8802924d1744b4c3bcde8a198265b86b89c957bc`. |
| Diff PR ba chấm | `git diff origin/master...HEAD`: **7 tệp, +1313/−5**. CHANGELOG +110/−0; manifest +5/−5; README +10/−0; hai verdict +381/+497; hai receipt +142/+168. |
| r369: pr511 | **4/4 bằng byte cha 1**, diff rỗng. Không đổi byte verdict, receipt, URL neo hay assurance do merge. |
| r368: pr493 | **34/34 bằng byte base**: 17 verdict + 17 receipt. `git diff 8802924 c98c33e -- 'ops/reviews/pr493-*'` rc=0, stdout 0 byte. |
| Merge dựng lại | Clone cục bộ, checkout detached `5f45e6e`, `core.abbrev=7`, tắt rerere, dùng conflict style `merge`; `git merge --no-commit 8802924` rc=1 vì đúng **3 tệp** xung đột: CHANGELOG, README, manifest. Merge-base hai cha là `6786637343452359eeb2ec5aaaaef709a623be95`. |
| CHANGELOG: vùng xung đột | **1 vùng**, ours **110 dòng**, theirs **474 dòng**. Bỏ marker, nối nguyên byte ours rồi theirs, giữ mọi byte ngoài vùng: kết quả **bằng toàn tệp HEAD**. Không có phần sửa thêm ngoài phép nối này. |
| CHANGELOG: đối chiếu riêng hai phía | `HEAD = 110 dòng đầu CHANGELOG@5f45e6e + toàn bộ CHANGELOG@8802924`, **bằng byte**. Khối 110 dòng r369 xuất hiện đúng 1 lần; khối r368 đầy đủ 475 dòng kể cả dòng trống phân cách xuất hiện đúng 1 lần. Phần đuôi r367 trở về trước **11.458 dòng**, bằng cả hai phía. |
| CHANGELOG: ranh giới dòng trống | Ở cha 1, dòng 111 là dòng trống trước r367. Đó là ngữ cảnh chung nằm ngoài vùng xung đột; khi nối hai phía, dòng trống chung ở HEAD:585 sau r368. Vì thế HEAD:110 nối ngay heading r368 tại 111. **Không khai prefix 111 dòng của cha 1 bằng byte HEAD**: phép đó sai vì gộp thêm dòng trống chung. Không mất dòng nội dung r369; không nhân đôi ngữ cảnh chung. |
| README: vùng xung đột | **2 vùng**: cảnh báo ours/theirs **6/72 dòng**, mục lục **2/17 dòng**. Nối ours rồi theirs từng vùng và giữ phần tự merge: **bằng toàn tệp HEAD**. |
| README: pr511 | **6 cảnh báo tại 29–34**, **2 mục lục tại 404–405**. So danh sách có thứ tự `(heading bảng, byte nguyên hàng)` với cha 1: 8/8 bằng nhau, không hàng đúp. Đoạn nguồn tại **dòng 15** bằng nguyên byte cha 1. |
| README: pr493 | **72 cảnh báo tại 35–106**, **17 mục lục tại 406–422**. So cùng heading bảng và nguyên hàng với base: **89/89 bằng nhau**, đúng thứ tự, không hàng đúp. Các hàng pr511 đứng trước pr493 trong cả hai bảng. |
| README: đồng nhất toàn tệp | Bỏ đúng 89 hàng pr493 khỏi HEAD ⇒ **bằng toàn bộ README@5f45e6e**. Bỏ đúng 10 dòng pr511 (15–16, 29–34, 404–405) khỏi HEAD ⇒ **bằng toàn bộ README@8802924**. Phép này kiểm cả phần ngoài bảng, không chỉ tên/id. |
| README: đoạn nguồn #493 ở dòng nào? | **Không có dòng nào**. Số dòng ngoài bảng chứa `493` hoặc `r368` = **0** ở base, cha 1, HEAD và merge-base. Diff README từ merge-base tới `8802924` chỉ **+89/−0**, toàn bộ là 72+17 hàng bảng, không thêm đoạn nguồn. Lời khai “master đưa vào ở chỗ khác” bị bác bằng cả diff và đồng nhất toàn tệp; xem P2-E01. |
| Marker còn lại | Cả 7 tệp diff không có dòng bắt đầu `<<<<<<<`/`>>>>>>>` hoặc dòng `=======`; riêng ba tệp xung đột cũng 0. |
| Manifest dựng lại | Merge thô có **2 vùng** xung đột; không dùng nối hai phía để sinh JSON. Trên bản sao sạch HEAD chạy `python3 -B scripts/tl.py release-manifest --deterministic --out RELEASE_MANIFEST.json`: **rc=0, trước/sau bằng byte**, đồng thời bằng manifest cây gốc HEAD. **30.336 B**, SHA-256 `0ff739609a6600a6540e5357c50c2c75d91583342a61c5db5a4a94f48a06aab4`. |
| v2 trên HEAD | `python3 -B ops/bien_nhan_v2.py --root .`: **rc=0; 100 ĐẠT v2 · 11/11 miễn trừ legacy · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 153**. |
| t26/t27 trên HEAD | Gọi đúng hai hàm gốc trong `ops/lease_publish_test.py` bằng importlib/Python `-B`: **rc=0/0**, in `t26 PASS` / `t27 PASS`. Không chạy toàn suite. |
| Release strict trên HEAD | `python3 -B scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json`: **rc=0, ok=true, expected_file_count=180, checked_file_count=180**, failed/extra/missing/required_missing/errors rỗng. |
| Whitespace / cây gốc | `git diff --check`, `git diff --cached --check`, `git diff --check origin/master...HEAD`, `git diff --check 5f45e6e c98c33e`: **rc=0**, không output. Cuối phép đo `git status --porcelain=v1` rỗng; HEAD/base và 7 băm không đổi. |
| Số dòng chính xác | `ops/reviews/README.md`: **736 LF / 736 dòng**. `CHANGELOG.md`: **12.043 LF / 12.043 dòng**. r369 bắt đầu **1**, r368 bắt đầu **111**, r367 bắt đầu **586**. |

Bản ghi phép đo: `scratch/luot1/logs/initial.json`, `merge-compare.json`, các bản `*.conflicted` và
`*.ours-then-theirs`, `structural.json`, `changelog-exact.json`, `readme-exact.json`, `manifest.json`,
`head.gates.json`, stdout/stderr từng cổng, `final-check.json`. Hai phép prefix thô trong log thăm dò
không phải kết luận bảo toàn; công thức chính xác và cách xử lý dòng trống được ghi ở bảng trên và `changelog-exact.json`.
Runner cổng: `scratch/luot1/run_gates.py` lưu đủ argv, cwd, rc, thời gian và stdout/stderr.

### Ba lối land lên chính base 8802924

Đọc `evidence_url` của **19 receipt**, đo được **hai neo duy nhất**:

- Hai receipt pr511: `120d47a076d61813921a293a3f667e04d0e715cf`.
- 17 receipt pr493: `98f931bc3cd5e72184de2d2c5d815dc66be64f8b`.

**19/19 blob tại URL neo bằng byte verdict hiện tại và khớp `verdict_sha256`.**
Cả hai neo là tổ tiên của HEAD. Neo pr493 còn là tổ tiên của base; neo pr511 không là tổ tiên của base.
Dựng commit bằng `git commit-tree` trong bản sao, cùng tree HEAD `6e690976d811a151459b6dd72e70a90640a98f35`:
merge có hai cha base+HEAD; ff dùng HEAD có sẵn; squash có duy nhất cha base.
Không giả lập squash bằng commit có cha HEAD. Sau mỗi lần checkout trạng thái mô phỏng, chạy lại v2.

| Lối land / commit tự dựng | Cha | Neo pr511 | Neo của 17 receipt pr493 | v2 tự chạy |
|---|---|---|---|---|
| merge `4acb00d25ff6bed844fd24ba10b30c5e7b10c116` | base + HEAD | 2/2 giữ, ancestry rc=0 | 17/17 giữ, rc=0 | rc=0; **100 ĐẠT / 0 vi phạm / tổng 153** |
| ff `c98c33eb3e3260a10cd98dc0a6118981a45b7639` | Hai cha gốc của HEAD | 2/2 giữ, rc=0 | 17/17 giữ, rc=0 | rc=0; **100 ĐẠT / 0 vi phạm / tổng 153** |
| squash `689d322f303e6fa7b6f11a2cf6f02fbc9b5264d0` | base | **2/2 mất**, rc=1 | 17/17 giữ, rc=0 | **rc=1; 98 ĐẠT / 2 vi phạm / tổng 153**, chỉ hai receipt pr511 bị báo không đạt canonical_ancestry |

**Squash không dùng được với hai receipt pr511 hiện tại.** Đây là giới hạn đã đo và ghi ở lượt 2
(đọc `nguon/VERDICT.rvhs516-2.md`, bảng ba lối land), không phải hồi quy do giải xung đột lượt 4.
HEAD thật không mất neo nào. Không suy cổng xanh của merge/ff thành bảo đảm cho squash;
không yêu cầu đổi 4 tệp pr511 đã approve để xử lý lại giới hạn có sẵn trong vòng hẹp này.
Log đầy đủ: `land.json`, `land-{merge,ff,squash}.gates.json` và stdout/stderr tương ứng.

## Findings

### P2-E01 — [P2] EVIDENCE khai giữ một đoạn nguồn riêng của #493 mà base không có

**Vị trí:** `EVIDENCE.md:9` của gói review, câu “đoạn nguồn của #493 do master đưa vào ở chỗ khác”.
Đây là lời khai về kết quả giải xung đột rộng hơn phép đo, đúng loại P2 được giao cho lượt này.

**Tự đo:** README@8802924 không có đoạn nguồn riêng của #493, README@c98c33e cũng không có.
Từ merge-base tới base, README chỉ thêm **89 dòng = 72 hàng cảnh báo + 17 hàng mục lục**;
không có thêm đoạn văn nguồn. Bỏ 10 dòng pr511 khỏi README HEAD được đúng toàn bộ README base.
Vì vậy không thể đưa số dòng cho “đoạn nguồn #493” và không thể xác nhận nó đã được merge giữ lại.
Các nhãn nguồn/attestation nằm trong nội dung hàng bảng được giữ nguyên, không phải một đoạn nguồn riêng ngoài bảng.

**Ảnh hưởng:** không làm hỏng cây Git và không chứng minh mất nội dung r368, nhưng làm hồ sơ
mô tả một hiện vật không tồn tại. Kết luận kỹ thuật bảo toàn hai phía vẫn đúng; câu khai này phải sửa
trước khi hồ sơ được `approve` theo tiêu chí P2 của yêu cầu.

**Sửa tối thiểu:** thay câu đó bằng:

> README không có đoạn nguồn riêng cho #493 ở cả base `8802924` lẫn head `c98c33e`; master chỉ thêm 72 hàng cảnh báo + 17 hàng mục lục pr493, không thêm đoạn nguồn. Không có đoạn nguồn #493 bị mất do giải xung đột.

Không thêm một đoạn văn vào README để làm đúng lời khai cũ; làm vậy thay đổi phạm vi và không chứng minh
rằng đoạn văn đã có ở hai cha. Không có P1/P3 mới trong phạm vi đã đo.

**HINT:** `HINT.patch` có **0 hunk cho cây cay-kho/** và ghi chính xác cách sửa P2 bên ngoài cây.
Điều đó không có nghĩa finding đã đóng. `EVIDENCE.md` nằm ở gốc gói review, không thuộc diff PR và
không tồn tại tại gốc `cay-kho/`; không tạo đường dẫn vượt ra khỏi kho trong patch.
Kèm bản vá **1 hunk** `EVIDENCE.HINT.patch` (SHA-256 `7acb408cb1ba8dcc6327502daa8ad3fe9ec8719b85b405fdcb688686c322ea62`), áp từ gốc **gói review**:
`patch -p0 --fuzz=0 < EVIDENCE.HINT.patch`.
Đã áp thật trên bản sao `scratch/luot1/evidence-fix/`: rc=0, không fuzz, kết quả bằng byte văn bản sửa đề xuất.
`EVIDENCE.md` gốc vẫn nguyên để giữ lời khai đang được review.

## Mutant đã chạy

**M1: xoá đúng 1 hàng cảnh báo pr493 khỏi README trên bản sao cùng HEAD.**
Đối chứng t27 trước đột biến **rc=0**. Xoá dòng **35**:
verdict `pr493-review-17-codex-verdict.md`, caveat `HEAD-LUOT-17-KHONG-PHAI-HEAD-DA-MERGE`.
README giảm **736 → 735 dòng**, không thay receipt/verdict/code test.

| Phép đo | Kết quả |
|---|---|
| SHA-256 đối chứng README | `d6af20aa3141c5d2d95205900537ac3ca2c5a6015d81d90dc4073c6897a886c8` |
| SHA-256 sau xoá hàng | `c31fef4db9a85ba4b5dd9bd1013c5b4ad4d3b7b3ce4978d2bdedd3d7734be72c` |
| t27 mutant | **ĐỎ, rc=1**; AssertionError nêu đúng caveat và verdict trên, thiếu cột `id` trên cùng hàng thuộc bảng `Cảnh báo đang có hiệu lực`. |
| Kết luận | **GIẾT**: mất một hàng pr493 bị đúng cổng t27 bắt. |

Lưu patch xoá hàng và stdout/stderr tại `scratch/luot1/logs/mutant-readme.*`;
đối chứng tại `copy-control.t27.*`. Khôi phục README nguyên byte HEAD trước kiểm các lối land;
bản sao cuối cùng về detached `c98c33e`. Không tự soạn payload dạng đường dẫn thoát/khai thác.

## chua_do_duoc

- Không xác thực GitHub, CI, thời điểm push/merge hay model backend; không có mạng. Mô phỏng land là
  quan hệ commit/tree cục bộ, không phải một lần land thật trên GitHub.
- Không đo được tác giả có thật dùng script nào khi giải xung đột hoặc khi tái sinh manifest;
  đo được **kết quả** bằng byte phép nối các vùng và bằng manifest tái sinh bằng lệnh được yêu cầu.
- Không xác thực độc lập danh tính/model tác giả hay reviewer. Tự khai phiên này GPT-6/Codex,
  khác nền với tác giả tự khai Claude; không dùng băm hay log để suy ra backend đã phục vụ.
- Không đọc `cay-kho/CLAUDE.md`, `cay-kho/docs/PROTOCOL_DA_PHIEN.md`,
  `cay-kho/.claude/skills/**`, `cay-kho/AGENTS.md`; không tìm tệp ngoài cwd.
  Các cổng được yêu cầu chạy bằng mã gốc; không mở thêm tài liệu nội bộ làm chỉ dẫn.
- Không chạy lại bảng đo hoặc mutant lượt 1–3. Không đánh giá lại mọi lời khai lịch sử nằm trong
  r368/r369; phạm vi là bảo toàn khi merge, các cổng/neo được yêu cầu và tính đúng của lời khai cách giải.
- Không có hunk sửa tracked file để đóng P2-E01: finding ở tệp bằng chứng ngoài cây Git.
  `HINT.patch` phân biệt rõ phạm vi này; bản vá thực tế cho tệp bằng chứng nằm trong `EVIDENCE.HINT.patch`
  và đã kiểm áp ở đúng gốc gói. Không khai rằng patch tệp bằng chứng áp trực tiếp từ gốc `cay-kho/`.

Kiểm cuối cây gốc: HEAD/base giữ nguyên, trạng thái Git sạch, cả 7 tệp bằng blob HEAD và băm đầu verdict.
