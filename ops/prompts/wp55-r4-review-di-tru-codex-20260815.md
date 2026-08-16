# Di trú AC 19 lên master · REVIEWER `codex`

Bạn là **reviewer** cross-provider. Tác giả commit là `claude` (§8 đòi khác nền). Vai này
**read-only**: KHÔNG sửa tệp, KHÔNG commit, KHÔNG push, KHÔNG merge/land.
Bạn được phép ghi tệp tạm và ghi ĐÚNG MỘT tệp verdict nêu ở cuối.

## BƯỚC 0 — xác minh. Lệch bất kỳ mục nào ⇒ DỪNG, báo lại, không review.

```bash
git rev-parse HEAD                       # ĐÒI 9a5b05cfd8804455dd785b8fe710736773dc78cf
git rev-parse --is-shallow-repository    # ĐÒI false
git diff --name-only 2531366e1abc6cbca0a6c2765e40e54be38d1fb7 HEAD   # ĐÒI đúng: CLAUDE.md
```

| | |
|---|---|
| head đang review | `9a5b05cfd8804455dd785b8fe710736773dc78cf` |
| dựng trên master | `2531366e1abc6cbca0a6c2765e40e54be38d1fb7` |
| phạm vi | **một tệp**: `CLAUDE.md` |
| bản thảo spec revision 4 | `ops/specs/wp55-r4-spec.md` trên `ops/wp55-r4-spec-draft` |
| nguyên mẫu AC 19 | `ops/specs/wp55-r4-ac19-nguyen-mau.py` cùng nhánh |

## Đây là lượt review KHÁC HẲN mọi lượt trước của wp55 — đọc kỹ

Đây **KHÔNG** phải một generation của packet. Đây là **một commit nhắm thẳng vào nhánh
MẶC ĐỊNH** (`master`), không thuộc `write_set` của packet nào, và nó là **điều kiện tiên
quyết** để revision 4 chốt được `base_sha`.

Vì sao có lượt này: chính phiên executor đề nghị. Commit do `claude` soạn, và nếu `claude`
tự duyệt commit của mình lên nhánh mặc định thì đó đúng là thứ protocol sinh ra để chặn.
**Bạn là chốt duy nhất trước khi nó vào master.**

## Việc commit này làm

Chủ kho đã chốt (trực tiếp, 2026-08-15): AC 19 của revision 4 thay miễn trừ ngữ nghĩa bằng
**khối chứng cứ khai báo**, `N=12` dòng/khối, `M=3` khối/tệp, khối được phép nằm trong mọi
tệp `write_set` kể cả `CLAUDE.md`, và di trú theo đường **sửa master trước rồi packet rebase**.

Commit này thực hiện bước di trú: bọc mục allowlist của `CLAUDE.md` bằng một khối chứng cứ.

Đo được, chính là lý do phải di trú: trên cây ĐÃ MERGE có **đúng một** chỗ cụm cấm bị ngắt
qua hai dòng — `CLAUDE.md` dòng 82–83 của master. Trên nhánh packet thì **không có chỗ nào**.
Dưới hợp đồng AC 19 mới, không bọc thì chỗ này sẽ ĐỎ.

## Hai quyết định thiết kế executor TỰ làm — soi kỹ hai chỗ này

**A. Bọc TRỌN mục danh sách (8 dòng thân), không chỉ hai dòng 82–83.**

Lý do executor đưa: chèn comment HTML vào giữa một đoạn văn sẽ **cắt đoạn ấy làm ba** theo
CommonMark, đổi cách render. Bọc trọn mục thì chỉ tách danh sách cấp trên thành hai danh
sách liên tiếp — thay đổi render nhẹ hơn.

**Phán định:** lý do ấy có đúng không, và cái giá có được khai đủ không? Cụ thể:

- kiểm bằng một trình render CommonMark thật, đừng tin lập luận: khối mới có làm vỡ danh
  sách, đổi tight/loose, hay đổi thứ tự mục nào không?
- bọc trọn mục nghĩa là **6 dòng KHÔNG cần miễn trừ cũng được miễn**. Đó có phải nới miễn
  trừ rộng hơn cần thiết không? AC 19 mới nói miễn trừ là ngoại lệ HẸP.
- có cách thứ ba tốt hơn cả hai không (ví dụ tách mục ra khỏi danh sách, hoặc viết lại câu
  để cụm không bị ngắt dòng — cách sau đóng lỗ mà KHÔNG cần miễn trừ nào)?

**Cách thứ ba đáng cân nhắc nghiêm túc:** nếu chỉ cần sửa chỗ xuống dòng để cụm `người có
thẩm quyền` nằm gọn một dòng, thì **không cần khối chứng cứ nào cả**, và toàn bộ cơ chế
miễn trừ trở thành không có người dùng. Executor KHÔNG xét khả năng này. Nếu bạn thấy nó
tốt hơn, nói thẳng — đó sẽ là finding có giá trị nhất của lượt này.

**B. `nguồn="CLAUDE.md@2531366:82-83"` trỏ về vị trí GỐC, không phải vị trí sau khi chèn.**

Sau khi chèn, chính hai dòng ấy nằm ở 83–84. Executor chọn trỏ về nơi phép đo được ghi lần
đầu, tức coi `nguồn` là **trích dẫn**, không phải **tự tham chiếu**.

**Phán định:** quy ước ấy có nhất quán và kiểm được không? Một `nguồn` trỏ tới SHA cha của
chính commit đang chứa nó có tự mâu thuẫn không? Spec revision 4 **chưa chốt** dạng chính
xác của `nguồn` — nếu bạn thấy quy ước này sai, nó phải được sửa TRONG SPEC trước khi land.

## Kiểm hình thức khối — nguyên mẫu có sẵn

```bash
git show origin/ops/wp55-r4-spec-draft:ops/specs/wp55-r4-ac19-nguyen-mau.py > /tmp/proto-9a5b05c.py
python3 - <<'PY'
import importlib.util, sys
spec = importlib.util.spec_from_file_location("p", "/tmp/proto-9a5b05c.py")
m = importlib.util.module_from_spec(spec); sys.argv = ["x"]
try: spec.loader.exec_module(m)
except SystemExit: pass
raw = open("CLAUDE.md", encoding="utf-8").read()
mien, loi = m.khoi_chung_cu(raw)
print("lỗi hình thức:", loi or "không")
print("dòng được miễn:", (min(mien), max(mien)) if mien else None, "·", len(mien), "dòng")
PY
```

Executor khai: 0 lỗi hình thức, miễn dòng 77–86 (10 dòng), cụm nằm TRỌN trong vùng miễn.
**Chạy lại, đừng nhận số.** Và tự hỏi: nguyên mẫu ấy có phải là thứ sẽ được cài thật không,
hay nó dễ dãi hơn bản cài đặt tương lai?

## Gate

```bash
python3 .githooks/eol_policy.py --all --json
python3 scripts/tl.py doc-claims-check --strict --json
python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --root . --strict --json
python3 scripts/tl.py golden-test
```

Executor khai `release-verify` checked=179 failed=0 extra=0, và `CLAUDE.md` **không** thuộc
manifest nên sửa nó không đụng băm phát hành. **Kiểm lại lời khai thứ hai** — nếu sai thì
commit này phá phát hành.

Cũng chạy scanner HIỆN HÀNH của packet để chắc chắn không hồi quy trên master:

```bash
python3 <(git show 1a4525a20aa360476a6f59cb157c21097919c457:.claude/dev/packet_loop.py) \
  doctrine-scan --root .
```

## Ba chuyện đã trả giá — đừng mất thời gian lại

1. **Sandbox từ chối `rm -rf`.** Dùng thư mục có hậu tố SHA.
2. **Đừng chạy `pip install`** — một lần cài giữa phiên đã làm hỏng `cryptography`.
3. **`release-verify` trong cây làm việc có thể trả `rc=2`** vì tệp nhiệm vụ này nằm ngoài
   manifest. Không phải finding — đo trên `git archive` của đúng head nếu cần số sạch.

## Câu hỏi cuối, trả lời thẳng

**Commit này có nên vào `master` không?** Nếu có, bạn khuyến nghị land bằng **fast-forward**
(giữ nguyên SHA `9a5b05c`, dùng được ngay làm `base_sha`) hay bằng merge/squash (đổi SHA,
phải chờ số mới)? Đây là câu chủ kho cần để quyết.

## Giao kết quả

Ghi verdict ra ĐÚNG một tệp: `VERDICT_DI_TRU.md` ở gốc thư mục làm việc.
KHÔNG commit, KHÔNG push.

Định dạng: `approve` | `changes_requested` | `blocked`, mỗi finding có `finding_id`
(slug kebab-case), `severity`, `disposition`, và **bằng chứng CHẠY ĐƯỢC neo SHA bất biến**.
Kèm khối `Evidence §7` dạng YAML với `reviewed_sha`, `base_sha`, danh sách `tests`, `findings`,
và một trường `land_recommendation` (`fast_forward` | `merge_commit` | `do_not_land`).

**Nói thẳng chỗ bạn KHÔNG chạy được.** Ranh giới của bản review quan trọng ngang kết luận.
