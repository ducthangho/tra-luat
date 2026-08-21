# Prompt BẤT BIẾN — Reviewer chéo `PLAT-M4`, lượt **1** (bản sửa r2), provider `codex`

Read-only với KHO: **không commit, không push, không đổi HEAD.**

**Bố cục sandbox** — bạn đang đứng ở thư mục gốc sandbox, KHÔNG phải trong kho:

```
./nhiem_vu.txt        prompt này
./EVIDENCE.md         số đo cổng của executor (đã đo lại độc lập)
./diff.patch          diff base..head
./numstat.txt         numstat base..head
./PROTOCOL_TRICH.md   bản sao docs/PROTOCOL_DA_PHIEN.md
./kho/                BẢN SAO KHO — `git worktree` tách rời tại exact head, GHI ĐƯỢC
```

Bản sao kho **ghi được** là cố ý: bạn tự chạy phản chứng và đột biến trong đó mà không
chạm kho thật. Mọi lệnh git chạy dạng `git -C kho ...`, mọi lệnh test chạy sau khi `cd kho`.

**CHỐT SẠCH CÂY:** `git -C kho status --short` phải **RỖNG** cả trước lẫn sau lượt, và
`git -C kho rev-parse HEAD` không đổi. Năm tệp artefact trên nằm NGOÀI `kho/` đúng để chốt
này đo được — lượt trước chúng nằm TRONG cây và làm preflight đỏ ngay từ đầu; đó là lỗi
của người dựng sandbox, đã sửa.

**Không đọc ra ngoài thư mục sandbox này.** Một lượt chạy phạm vi mở đã quét ra ngoài kho,
đọc nhầm transcript phiên, 40 phút không ra kết luận.

## 1. Mỏ neo

| trường | giá trị |
|---|---|
| packet | `#194` — `[WP PLAT-M4]` |
| PR | `#204` |
| exact head phải review | `5813fc450efe3cb349b082044708d27a589b69fb` |
| base | `2663477dfc63b68dbe34ff684f11213d95bcb8b9` |
| write set khai báo | `.claude/dev/launcher.py` · `.claude/dev/launcher_test.py` — **ĐÚNG 2 tệp** |
| review class | `sensitive` · vòng **1/2** (trần canon 2 vòng) |

`git -C kho rev-parse HEAD` phải bằng đúng chuỗi trên. Lệch ⇒ dừng, khai `stale head`.

## 2. Packet này làm gì

`doctor` trước đây chỉ đo **dây nối** MCP (`_doc_mcp_json` + `claude mcp get`) — cả hai
hỏi phía CLI. Không bước nào chạm **đầu kia**. Hệ quả đã xảy ra thật: CLI báo
`Pending approval` trong khi POST `initialize` tới URL khai trong `.mcp.json` trả HTTP 200
kèm header GitHub, và phiên đọc trường gộp cũ kết luận "GitHub bị chặn" rồi dừng — mất
trọn một lượt. Nay tách `mcp` thành `mcp-cli` + `mcp-endpoint`.

## 3. Trục phải soi

Đây là mã **chẩn đoán mà phiên khác tin để quyết định bỏ hay không bỏ một đường đi**. Sai
ở đây không làm đỏ cổng nào — nó làm phiên sau đi sai hướng, im lặng.

1. **`LAM_DUOC_VIEC` có bị nới không?** Phải giữ nguyên `{git, gh-kho, rest-kho}`.
   `initialize` chứng minh endpoint **trả lời**, KHÔNG chứng minh đọc được kho — cùng hạng
   `rest-chung`. Kho đã trả giá **ba lần** cho đúng cám dỗ "đếm sự CÓ MẶT thay vì KHẢ NĂNG"
   (`which(gh)`, `rest-chung`, `gh auth status`). Nếu `mcp-endpoint` lọt vào tập
   `DUNG_DUOC`/`LAM_DUOC_VIEC` bằng bất cứ đường nào ⇒ **P1**. Đo, đừng đọc: đột biến cho
   nó lọt vào rồi xem ca nào đỏ.
2. **Phân loại theo HEADER hay theo MÃ TRẠNG THÁI?** Doctrine của kho: dấu hiệu phân biệt
   proxy-tự-sinh với GitHub-thật là **`X-GitHub-*`**, không phải mã. Một 401 **có** header
   (endpoint sống, token sai) phải đọc KHÁC một 403 **không** header (proxy chặn). Chúng in
   ra giống nhau ⇒ P2 trở lên.
3. **Ba trạng thái, không phải hai.** `chua-do-duoc` phải đọc khác `khong` (`None ≠ False`).
   Đường nào biến "không đo được" thành "không" ⇒ **fail-open**, P1.
4. **Scheme có danh sách CHO PHÉP không?** `urlopen` nhận cả `file://`. Một `.mcp.json` trỏ
   `file:///etc/passwd` biến probe mạng thành lượt đọc đĩa. Danh sách **CẤM** không bao giờ
   đủ — kho đã ghi sổ. Thử thật: trỏ `.mcp.json` sang `file://`, `ftp://`, `gopher://`,
   và một URL có credential nhúng.
5. **Rò rỉ bí mật.** `doctor --json` **không được** in token ra byte nào. Probe gửi
   `Authorization` — nó có lọt vào log, vào thông điệp lỗi, vào JSON không? Thử với một
   token giả có vân tay dễ tìm rồi `grep` toàn bộ đầu ra.
6. **Treo và chi phí.** Có timeout thật không (`PROBE_TIMEOUT_GIAY`)? Có auto-retry không
   (không được có)? `doctor` phải chạy được **offline** — thử cắt mạng/trỏ URL đen; nó phải
   trả `chua-do-duoc` nhanh, không treo.
7. **API riêng nền.** Kho đã trả giá hai lần (`os.O_NOFOLLOW`, `os.getpgid` làm suite
   **0/103** trên Windows mà năm lượt review Linux không thấy). Mã mới có đụng API chỉ có
   trên một nền không? Có `hasattr`/`getattr(..., mặc_định)` trước không?
8. **`t115` còn gác không?** Bản cũ chốt bằng chuỗi `"mcp"` có dấu nháy hai đầu; sau khi
   tách tên thì `"mcp-cli"`/`"mcp-endpoint"` không khớp — **ca canh còn đó, không còn canh
   gì**. Executor khai đã mở sang cả ba tên. Đo: đột biến bỏ một tên ra khỏi kết xuất rồi
   xem `t115` có đỏ không.

## 4. Đừng tin bảng đột biến của executor — chạy lại

Kho có một bài học đắt: runner đột biến từng ghi mọi bản sao vào **cùng một** tệp tạm, và
CPython coi `.pyc` còn hợp lệ theo **(mtime tính bằng GIÂY, kích thước)** — hai đột biến
cùng kích thước ghi trong cùng một giây ⇒ bản sau chạy **mã của bản trước**. Một mutant báo
`giet 0/1` suốt ba lượt review vì lý do đó, và nó **tước răng mọi mutant**, không riêng một
cái.

Nên: **đột biến sống sót không luôn nghĩa là test yếu, và chết cũng không luôn nghĩa là
test có răng.** Tự dựng đột biến của bạn trên bản sao, đặt tên tệp riêng từng lượt, và
kiểm rằng lượt nạp KHÔNG để lại `.pyc`.

```
python3 .claude/dev/launcher_test.py              # chờ rc=0, hai số BẰNG NHAU
python3 .claude/dev/launcher_test.py --dot-bien   # mọi đột biến của lượt này giết 1/1
python3 .claude/dev/launcher.py doctor --json
```

**`N/N` với hai số bằng nhau** mới là bằng chứng — `rc=0` một mình có thể bị lừa. Ca bỏ qua
duy nhất trên Linux phải là `t62` (bản POSIX là `t63`).

## 5. Ba lời khai của executor — hãy ĐO, đừng đọc

1. **Trùng số ca đã hết?** `b178734` (merge) khai đã đổi `t138` → `t143` nhưng **chưa**:
   việc đổi tên chạy sau khi `git merge --no-commit` đóng băng index. Cả suite lẫn đột biến
   XANH với **hai** hàm `t138` cùng tồn tại — không cổng nào bắt được. `5813fc4` mang phần
   còn thiếu. Đo: `rg -o '^def (t[0-9]+)_' -r '$1' | sort | uniq -d` phải **RỖNG**.
2. **Diff đúng 2 tệp?** `git diff --name-only <base>..HEAD`. Tệp thứ ba là finding.
3. **`MO_DUN_PY` → `MODULE_PY`:** executor khai 4 chỗ `m.MO_DUN_PY` **có sẵn trên master**,
   delta = 0, nên không sửa. Kiểm lời khai nền ấy.

## 6. Cách trả lời

Mỗi finding bắt buộc bốn phần: (a) **bằng chứng đo được** (lệnh + kết quả nguyên văn);
(b) mức P1/P2/P3; (c) **invariant nào bị cắt**; (d) **gợi ý vá** cụ thể. Không chạy được
thì ghi thẳng là **giả thuyết**, đừng trình bày như phép đo.

Kết ở dòng cuối, đúng một trong ba, viết nguyên văn:

```
VERDICT: approved
VERDICT: changes_requested
VERDICT: blocked
```

Kèm ngay dưới:

```
Reviewed commit: 5813fc450efe3cb349b082044708d27a589b69fb
```
