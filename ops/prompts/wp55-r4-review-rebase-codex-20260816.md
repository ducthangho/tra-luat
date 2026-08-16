# Rebase bản viết lại lên master hiện tại · REVIEWER `codex`

Bạn là **reviewer** cross-provider. Tác giả commit là `claude` (§8 đòi khác nền). Vai này
**read-only**: KHÔNG sửa tệp, KHÔNG commit, KHÔNG push, KHÔNG merge/land.
Bạn được phép ghi tệp tạm và ghi ĐÚNG MỘT tệp verdict nêu ở cuối.

## BƯỚC 0 — xác minh. Lệch bất kỳ mục nào ⇒ DỪNG, báo lại, không review.

```bash
git rev-parse HEAD                                                   # ĐÒI c44b2d4c351cbe7f519e1b46aadf68d45e98af86
git rev-parse HEAD^                                                  # ĐÒI d5b7bccd679480f2eb9e7f7d84c518bade7f7df1
git rev-parse --is-shallow-repository                                # ĐÒI false
git diff --name-only d5b7bccd679480f2eb9e7f7d84c518bade7f7df1 HEAD   # ĐÒI đúng: CLAUDE.md
git diff --shortstat d5b7bccd679480f2eb9e7f7d84c518bade7f7df1 HEAD   # ĐÒI 2 insertions, 2 deletions
```

| | |
|---|---|
| head đang review | `c44b2d4c351cbe7f519e1b46aadf68d45e98af86` |
| cha = master tip | `d5b7bccd679480f2eb9e7f7d84c518bade7f7df1` |
| bản ĐÃ DUYỆT trước rebase | `c47a439997e0191427d775636ebadbf3be7e1481` (cha `2531366`) |
| verdict của bản ấy | `approve`, không finding — `ops/reviews/wp55-r4-review-viet-lai-codex-verdict.md` trên `ops/wp55-r4-verdict-viet-lai` |

## LƯỢT NÀY HẸP — đọc kỹ phạm vi trước khi soi rộng

Nội dung đã được **bạn duyệt rồi** ở `c47a439`: `approve`, không finding, sau khi bạn quay
về PR #104 kiểm cả nghĩa của bản ghi phép đo. **Đừng soi lại nội dung ấy từ đầu.**

Việc của lượt này là trả lời đúng một câu: **phép rebase có làm thay đổi gì so với bản đã
duyệt không?**

Vì sao phải rebase: `c47a439` dựng trên `2531366`, nhưng master tip là `d5b7bcc` — đi trước
`2531366` hai commit (PR #116). Fast-forward vì thế BẤT KHẢ THI, dù verdict trước khuyến
nghị `fast_forward`. Cả executor lẫn reviewer khi ấy đều không đo topology — đó là sai sót
chung, ghi ra để không lặp.

## Ba việc cần kiểm, không hơn

**1. Diff có Y HỆT bản đã duyệt không?**

```bash
diff <(git diff d5b7bccd679480f2eb9e7f7d84c518bade7f7df1 c44b2d4c351cbe7f519e1b46aadf68d45e98af86 -- CLAUDE.md) \
     <(git diff 2531366e1abc6cbca0a6c2765e40e54be38d1fb7 c47a439997e0191427d775636ebadbf3be7e1481 -- CLAUDE.md)
```

Executor khai hai diff giống hệt nhau ở phần `+`/`-`. Kiểm cả phần ngữ cảnh và số dòng —
rebase qua một base khác có thể dời vị trí hunk mà nội dung vẫn giống.

**2. Hai commit PR #116 có đụng `CLAUDE.md` không, và nếu có thì rebase có nuốt mất gì?**

```bash
git log --oneline 2531366e1abc6cbca0a6c2765e40e54be38d1fb7..d5b7bccd679480f2eb9e7f7d84c518bade7f7df1
git diff --stat 2531366e1abc6cbca0a6c2765e40e54be38d1fb7 d5b7bccd679480f2eb9e7f7d84c518bade7f7df1 -- CLAUDE.md
```

Nếu PR #116 có sửa `CLAUDE.md` thì phải kiểm bản rebase giữ đủ thay đổi của họ. Đây là rủi
ro thật nhất của lượt này.

**3. Cây sau rebase còn cụm cấm nào không — cả dưới hợp đồng CŨ lẫn MỚI.**

Chủ kho đã chốt (2026-08-15) AC 19 của revision 4 **BỎ HẲN MIỄN TRỪ**: cụm cấm không được
xuất hiện ở bất kỳ hình dạng nào, không ngoại lệ. Nên kiểm bằng CẢ HAI:

```bash
# scanner hiện hành (còn miễn trừ)
python3 <(git show 1a4525a20aa360476a6f59cb157c21097919c457:.claude/dev/packet_loop.py) \
  doctrine-scan --root .
```

Và mô phỏng hợp đồng mới bằng cách bỏ nhánh miễn trừ — xoá dòng
`if cum in CUM_NGON_NGU_THUONG and _duoc_tha_vi_ngat_dong(raw, kim): continue`
khỏi bản sao của scanner rồi chạy lại. Executor khai cả hai `rc=0`.

## Gate

```bash
python3 .githooks/eol_policy.py --all --json
python3 scripts/tl.py doc-claims-check --strict --json
python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --root . --strict --json
python3 scripts/tl.py golden-test
```

Executor khai tất cả `rc=0`, `release-verify` checked=179 failed=0 extra=0.

## Ba chuyện đã trả giá — đừng mất thời gian lại

1. **Sandbox từ chối `rm -rf`.** Dùng thư mục có hậu tố SHA.
2. **Đừng chạy `pip install`** — một lần cài giữa phiên đã làm hỏng `cryptography`.
3. **`release-verify` trong cây làm việc có thể trả `rc=2`** vì tệp nhiệm vụ này ngoài
   manifest. Không phải finding — đo trên `git archive` của đúng head nếu cần số sạch.

## Câu hỏi cuối, trả lời thẳng

`c44b2d4` có nên vào `master` không, và **giờ ff được chưa** (cha nó đúng bằng master tip)?
Nếu master lại dời trong lúc bạn review thì nói rõ — chuyện ấy vừa xảy ra một lần rồi.

## Giao kết quả

Ghi verdict ra ĐÚNG một tệp: `VERDICT_REBASE.md` ở gốc thư mục làm việc.
KHÔNG commit, KHÔNG push.

Định dạng: `approve` | `changes_requested` | `blocked`, mỗi finding có `finding_id`,
`severity`, `disposition`, và **bằng chứng CHẠY ĐƯỢC neo SHA bất biến**. Kèm khối
`Evidence §7` dạng YAML với `reviewed_sha`, `base_sha`, `tests`, `findings`, và
`land_recommendation` (`fast_forward` | `merge_commit` | `do_not_land`).

**Nói thẳng chỗ bạn KHÔNG chạy được.**
