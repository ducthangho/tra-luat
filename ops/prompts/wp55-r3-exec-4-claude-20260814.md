# wp55 revision 3 · generation 4 · EXECUTOR `claude`

Bạn là **executor** cho work packet **wp55** (issue #55), mission #54 revision 6.
Vai này được **ghi** trong đúng 6 đường dẫn write_set và **không gì khác**.

Reviewer kế tiếp bắt buộc là `codex` (§8 — khác provider với executor). Đừng tự review.

---

## BƯỚC 0 — xác minh trước khi đọc bất cứ gì. Lệch bất kỳ mục nào ⇒ DỪNG, báo lại.

```bash
git rev-parse --is-shallow-repository        # ĐÒI false
git remote -v                                # ĐÒI github.com/ducthangho/tra-luat

# spec revision 3 — NGUỒN SỰ THẬT là TỆP, không phải thân Issue
git fetch origin ops/wp55-r3-spec
git show origin/ops/wp55-r3-spec:ops/specs/wp55-r3-spec.md | sha256sum
#   ĐÒI e321f811724fae97b19d523a3e5159bc13b425cd15fc6c753c7439fe28cae22d

# head xuất phát
git fetch origin claude/wp55-r2g2-f3-03
git rev-parse origin/claude/wp55-r2g2-f3-03
#   ĐÒI 546ecf9fd4dfe889d0cd3ee77b9589d8bed0465f
```

**Đọc `ops/specs/wp55-r3-spec.md` TRỌN VẸN trước khi gõ dòng mã đầu tiên.** Prompt này
không thay spec; spec mới là hợp đồng. Chỗ nào prompt và spec lệch nhau thì **spec thắng**,
và báo lại chỗ lệch.

Đọc thêm — bản gốc, không đọc tóm tắt:
- verdict lượt 5: PR #92 review `4939956924`; bản chép trong kho tại
  `ops/reviews/wp55-r2-review-5-codex-verdict.POSTED-COPY.md` (nhánh
  `ops/wp55-r2-review-5-verdict`) — **đọc mục đầu tệp**, nó KHÔNG phải bản gốc.
- verdict lượt 4: `ops/reviews/wp55-r2-review-4-codex-verdict.md`
  (sha256 `d58088bec10ad36a912b64749cbe8a41af5de0b3f70033d9109f12bb6647e82f`).
- `docs/PROTOCOL_DA_PHIEN.md` §5, §8, §12.

**Kiểm đường ghi kết quả TRƯỚC khi làm việc.** Ba lượt liên tiếp đã review/vá xong rồi
không ghi được lên GitHub. Thử ngay đường bạn định dùng (MCP GitHub, `gh`, hay git push).
Không ghi được thì **vẫn làm**, nhưng ghi kết quả vào kho và nói rõ ai cần đăng hộ — đừng
bỏ dở, và đừng im lặng.

---

## Nhánh và PR

Tạo nhánh **`claude/wp55-r3g4-f3-03`** xuất phát từ `546ecf9`, mở PR mới nhắm `master`.

Vì sao xuất phát từ `546ecf9` chứ không từ base: ba bản vá của generation 3
(`lease-authority-spoof`, `legacy-lease-bypass`, `doctrine-rendering-bypass`) đã được
cross-review lượt 5 soi và **không** bị bác — chúng vẫn đúng, chỉ là chưa đủ. Vứt đi rồi
gõ lại là tự tạo rủi ro không có lợi ích.

Vì sao **tên nhánh mới** chứ không đẩy tiếp lên `claude/wp55-r2g2-f3-03`: tên phải nói
đúng revision và generation. PR #92 giữ nguyên làm hồ sơ của revision 2; chủ kho quyết
định lúc nào đóng nó, **bạn không đóng**.

---

## Việc phải làm — ba P1, nhưng thứ tự quan trọng hơn danh sách

Spec mô tả đầy đủ ở mục *Ba finding P1*. Ràng buộc nặng nhất là **AC 18**, và nó nói về
**thứ tự**:

### Trước khi sửa một dòng mã nào: xuất DANH SÁCH ĐÓNG

`doctrine-scan` đã thua **năm** vòng liên tiếp, mỗi vòng một lớp ký tự mới (dấu `.` →
`==`/`!=`/`!` → nháy ngược Markdown → ZWSP + HTML entity → ký tự tương thích toàn rộng).
Chốt lease thua **hai** vòng cùng một lỗ. Cả bảy lần đều vá đúng hình dạng vừa bị chỉ ra.

Nên lượt này **cấm** bắt đầu bằng bản vá. Bắt đầu bằng một bảng:

| lớp | phép thử chạy được | rc đo được | bị bắt nhờ đâu | đề xuất tầng chữa |
|---|---|---|---|---|

Phủ tối thiểu (spec AC 18 liệt kê đủ): NFKC vs NFC (toàn rộng, ký tự tương thích, chữ số
tròn, ligature); ký tự định dạng `Cf` (ZWSP/ZWNJ/ZWJ/WORD JOINER/soft hyphen/BOM); HTML
entity (thập phân, thập lục, có tên, thiếu `;`, lồng nhau `&amp;#58;`); đồng tự Cyrillic/
Hy Lạp; nháy cong; biến thể dash; nhấn mạnh Markdown giữa từ, tag HTML xen giữa, comment
HTML, link/anchor, bảng, code fence; tổ hợp dấu và thứ tự chuẩn hoá.

Làm y như vậy cho **hình dạng `lease`** (AC 21): thiếu từng khoá; `lease` là chuỗi/số/
mảng/`null`/dict rỗng; `expires_utc` rỗng/sai dạng/thiếu múi giờ/là số/năm 9999/trước 1970.

Rồi **vá một lượt** cho cả danh sách, ở **tầng**:
- `_chuan_hoa`: **NFKC** (không phải NFC) + lọc `Cf` + giải entity đúng **một** lần, áp
  cho **cả hai vế** so khớp — cụm cấm cũng phải đi qua đúng hàm ấy.
- lease: **một hàm kiểm chung** trọn lược đồ + kiểu, dùng bởi cả `record-lease` lẫn
  `begin-attempt`. Mọi hình dạng sai trả **mã thoát có kiểm soát**, KHÔNG traceback.

Mỗi lớp trong danh sách phải có **một ca phản chứng** và **một đột biến giết đúng ca đó**.

### Chiều BẮT OAN, ngang hàng chiều lọt (AC 19)

Ca bắt buộc: cụm doctrine **ngắt qua xuống dòng** trong văn xuôi kể lại kết quả đo KHÔNG
được tính là chép doctrine. Ca thật đang làm gate đỏ: `CLAUDE.md` của master dòng 82 kết
thúc bằng `người có`, dòng 83 bắt đầu bằng `thẩm quyền`.

Chuẩn hoá mạnh hơn mà bắt oan văn bản bình thường là **KHÔNG ĐẠT**, y như để lọt. Mỗi lớp
chuẩn hoá thêm ở AC 18 phải có ít nhất một ca bắt-oan.

Cẩn thận hai chiều cùng lúc: lọc `Cf` không được nuốt ký tự cần cho tiếng Việt hay Markdown;
giải entity một lần không được biến `&amp;#58;` (hiển thị nguyên văn `&#58;`, KHÔNG phải
dấu hai chấm) thành báo nhầm.

### Gate đo trên CÂY ĐÃ MERGE (AC 20)

`git merge-tree` trả `rc=0` **không** phải bằng chứng tương thích — nó chỉ trả lời có xung
đột văn bản hay không, không trả lời *cây sau merge còn qua gate không*. Bằng chứng giao
nộp phải gồm `doctrine-scan` **và** bộ suite chạy trên cây dựng như sau, kèm SHA của master
lúc đo:

```bash
merged=$(mktemp -d)
git archive origin/master | tar -x -C "$merged"
git diff --binary fbe5ab9e..<head-cua-ban> | git -C "$merged" apply
python3 "$merged/.claude/dev/packet_loop.py" doctrine-scan --root "$merged"
python3 "$merged/.claude/dev/packet_loop_test.py"
```

Chỉ đo trên nhánh là **KHÔNG ĐẠT**.

---

## Gate phải chạy, và phải đọc rc THẬT từng lệnh

`rc` của một pipe là `rc` của lệnh **cuối**. Đòi **bằng chứng dương** — hai số bằng nhau,
`ok: true` — đừng tin `rc=0`.

```bash
python .claude/dev/packet_loop_test.py            # ĐÒI N/N + đủ đột biến giết đúng ca đích
python .claude/dev/packet_loop.py doctrine-scan --root .
python scripts/tl.py --selftest                   # ĐÒI hai số BẰNG NHAU
python scripts/tl.py doc-claims-check --strict --json      # ĐÒI flags=0
python scripts/tl.py release-verify RELEASE_MANIFEST.json --root . --strict --json
python scripts/tl.py golden-test                  # KHÔNG --write
python .githooks/eol_policy.py --all --json       # ĐÒI violations=0
release-bundle hai lần + bundle từ fbe5ab9e — ĐÒI cả ba CÙNG sha256
git diff --name-status fbe5ab9e <head>            # ĐÒI ĐÚNG 6 tệp write_set
```

`core.abbrev` phải = 7 khi chạy gate, nếu không golden/determinism/doc-claims đỏ giả.

---

## Ranh giới — vượt là dừng, không phải xin lỗi sau

- Ghi **đúng 6 tệp** write_set. Không mở rộng, không đụng `RELEASE_MANIFEST.json`,
  `references/golden/**`, `scripts/tl_test_fragments_bundled.py`.
- KHÔNG merge, KHÔNG land, KHÔNG deploy, KHÔNG gọi LIVE, KHÔNG đọc/ghi secrets,
  KHÔNG force-push, KHÔNG xoá nhánh, KHÔNG sửa spec packet khác.
- KHÔNG bump VERSION, KHÔNG cấp rNNN, KHÔNG sửa CHANGELOG.
- KHÔNG tự review bản vá của mình. KHÔNG tự cấp lease. KHÔNG đóng #54/#55/#92.
- KHÔNG đụng `claude/wp55-f3-03` hay PR #56.
- Phát hiện ngoài spec ⇒ xuất successor §7 rồi dừng; **không tự mở write set**.

## Trần và stop conditions

`attempts_limit: 3`, đếm lại từ **0** cho revision 3. Lượt này là **attempt 1**.

Dừng và báo khi: head đổi giữa chừng · lease hết hạn · chạm quota (ghi lý do allowlist,
**không** tiêu attempt nội dung) · phát hiện chính spec revision 3 thiếu ⇒ báo, **không**
tự nới, đi Mission Change Request.

## Giao nộp

Handoff §7 máy đọc được lên #55, neo `spec_hash e321f811…`, `base_sha fbe5ab9e`,
`head_sha` thật, kèm bảng danh sách đóng ở AC 18 và bằng chứng cây-đã-merge ở AC 20.

Heartbeat **mỗi 30 phút** lên #55: `lease_id`, giờ VN, đang làm bước nào, đã chạy lệnh nào.
Lease sống được là nhờ dấu vết, không nhờ con số hạn dài.
