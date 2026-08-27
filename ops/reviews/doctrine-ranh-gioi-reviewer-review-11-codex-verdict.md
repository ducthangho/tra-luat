# Cross-review vòng 11 — packet #318 `DOCTRINE-RANH-GIOI-REVIEWER`

```yaml
verdict: changes_requested
reviewed_sha: 12e0315a439b1e73bde57b09152bc077e04d7ee5
reviewed_tree: f13e9dc33ef4873b639000f0c4573a928b8c4cd7
base_sha: c35ae1c0a1104dbd6e65a321cda3b9f9441a408b
reviewer_provider: openai_codex
execution_surface: codex_service
transport: machine
executor_provider: anthropic_claude
independent_from_executor_session: true
finding_counts:
  P1: 1
  P2: 0
```

Đã review trên clone độc lập, detached và sạch. `git rev-parse HEAD` trả đúng SHA nêu
trên; `git rev-parse HEAD^{tree}` trả đúng tree nêu trên. Cả
`c35ae1c0a1104dbd6e65a321cda3b9f9441a408b` và
`7d7354e14c540c3c2afd3f3a594ff2e432f6fd44` đều là tổ tiên của HEAD (`merge-base
--is-ancestor`, `rc=0`). Không gọi GitHub, không fetch, không sửa nhánh Executor.

## ĐỐI CHIẾU HAI FINDING VÒNG 9

### `require-clean-vuot-pham-vi-quyen-ghi` [P1] — ĐÃ VÁ THẬT

Đo tại `docs/GOI_AGENT_DA_NEN.md:694-698`: đoạn mới chỉ nói đối tượng cây bẩn nằm
ngoài phạm vi quyền ghi và yêu cầu một phép đo riêng nếu sau này muốn xếp hạng. Nó còn
nói tường minh rằng câu này **không khẳng định** `--require-clean` bó hay không bó.
Không còn kết luận thực chứng ngầm kiểu “có bó, và bó thật”. Vì vậy con trỏ này không
tạo thêm một mệnh đề `chiều ĐÓNG`.

Bảy mệnh đề được tệp chủ ý gắn nhãn vẫn đếm ra `chiều ĐÓNG` ×1 · `chiều MỞ` ×4 ·
`chưa xếp được` ×2. Finding mới bên dưới là một mệnh đề khác, đã tồn tại sau lát cắt
sandbox; nó không biến bản vá riêng của finding vòng 9 thành vá hờ.

Phép đo:

```bash
nl -ba docs/GOI_AGENT_DA_NEN.md | sed -n '687,698p'
```

Kết quả dương: dòng 694-698 có câu phủ định kết luận thực chứng; không có nhãn hạng mới
trong đoạn vá.

### `prompt-shell-bien-chua-khoi-tao` [P2] — ĐÃ VÁ THẬT

Khối lệnh ở dòng 583-586 nay kết thúc bằng `--output-format json < PROMPT.md`, đúng
thành ngữ đã có ở dòng 518 và 530. Không còn `$PROMPT`, nên không còn biến shell chưa
được gán.

```bash
sed -n '583,586p' docs/GOI_AGENT_DA_NEN.md | bash -n
# rc=0

rg -n '\$PROMPT|< PROMPT\.md' docs/GOI_AGENT_DA_NEN.md
# chỉ ra ba redirect ở dòng 518, 530, 586; không có $PROMPT
```

Đã chứng minh cú pháp và việc loại biến lỗi. Không gọi thật `claude -p`; giới hạn đó
được khai ở mục `CHỖ KHÔNG ĐO ĐƯỢC`.

## Phép đếm tự liệt kê

Áp đúng luật do tệp đặt ra — đơn vị là một mệnh đề kèm điều kiện, không phải số lần
grep cụm chữ — bảy mệnh đề **đã có nhãn** là:

| # | dòng | mệnh đề | nhãn trong tệp |
|---:|---:|---|---|
| 1 | 678 | luật hẹp `Bash(x:*)` gặp lệnh ghép | `chiều ĐÓNG` |
| 2 | 679 | `Bash` trần gặp cùng lệnh ghép | `chiều MỞ` |
| 3 | 680 | `workspace-write` ghi ngoài cây | `chưa xếp được` |
| 4 | 681 | bỏ credential khỏi môi trường mà dry-run vẫn qua | `chiều MỞ` |
| 5 | 682 | token rác mà dry-run vẫn qua | `chiều MỞ` |
| 6 | 684-686 | proxy ambient tự chèn credential | `chiều MỞ` |
| 7 | 687-692 | clone rời + `--require-clean` + kiểm cây đối với quyền ghi/push | `chưa xếp được` |

Tổng của bảy nhãn trên đúng là `1 + 4 + 2 = 7`, dùng ba hạng. Nhưng đó chưa phải
toàn bộ mệnh đề mà chính vùng văn bản tuyên bố phải gắn nhãn: dòng 667-668 tự gọi một
khẳng định sandbox khác là “Mệnh đề còn đứng”. Mệnh đề thứ tám này là finding [P1]
bên dưới.

## Bảng chấm N1-N7

| Tiêu chí | Kết quả | Lệnh/phép đo và bằng chứng dương |
|---|---|---|
| N1 | ĐẠT | `nl -ba ... | sed -n '653,662p'`: câu đầu dòng 655-656 chốt đúng hai trục — vỏ phiên điều phối và quyền ghi vào kho. |
| N2 | **KHÔNG ĐẠT** | Liệt kê thủ công dòng 678-692 cho bảy nhãn, rồi đọc dòng 664-669: còn một mệnh đề sandbox không mang nhãn. Cam kết dòng 609 và phép đếm dòng 619-623 vì vậy không phủ hết mệnh đề. |
| N3 | ĐẠT | Dòng 570-577 vẫn tách “không tái lập được từ kho” khỏi “tương quan có neo” và chỉ nói nhân quả chưa chứng minh; không dùng bảng đó để khẳng định nhân quả. |
| N4 | **KHÔNG ĐẠT** | Bảy mệnh đề được đếm có điều kiện/neo cạnh chúng, nhưng mệnh đề dòng 667-668 không có điều kiện đo cạnh quan sát; dòng 669 nói số đo/probe/bảng đã thuộc packet khác. Cùng finding [P1]. |
| N5 | ĐẠT | So `git show 7d7354e1:docs/GOI_AGENT_DA_NEN.md` với `HEAD`: cùng các dòng `tương quan có neo`, `stdout.log` không tái lập, ví dụ thứ sáu `bash /tmp/refscan.sh`, và đúng ba bộ `78/5/10,8 M` · `85/10/12,8 M` · `45/1/3,7 M`. |
| N6 | ĐẠT | `git diff --name-only 7d7354e1..HEAD` in đúng `docs/GOI_AGENT_DA_NEN.md`, `rc=0`. |
| N7a | ĐẠT | Lệnh bắt buộc trả `rc=0` và in `doctrine-scan: sạch — đã quét 8 tệp, 0 chỗ chép doctrine`. |
| N7b | ĐẠT | `git diff --numstat c35ae1c0a1104dbd6e65a321cda3b9f9441a408b -- docs/GOI_AGENT_DA_NEN.md` in `180  0  docs/GOI_AGENT_DA_NEN.md`; cột thêm 180 ≤ 200. |

Lệnh N7a đã chạy nguyên văn:

```bash
python3 .claude/dev/packet_loop.py doctrine-scan --root . --path docs/GOI_AGENT_DA_NEN.md
```

Kiểm bổ sung:

```bash
git diff --check 7d7354e14c540c3c2afd3f3a594ff2e432f6fd44..HEAD -- docs/GOI_AGENT_DA_NEN.md
# rc=0, không output
```

## Finding mới

### `menh-de-sandbox-mo-coi-khong-nhan` [P1]

**Tệp/dòng:** `docs/GOI_AGENT_DA_NEN.md:609`, `:619-623`, `:664-669`.

**Trích dòng:**

> “Mọi mệnh đề sau đây mang đúng một nhãn”
>
> “Mệnh đề còn đứng mà không cần bảng số nào: mạng đóng của sandbox là một MẶC
> ĐỊNH CẤU HÌNH, không phải bất biến — biết cơ chế KHÔNG làm nó thành ranh giới.”

**Vấn đề:** câu sau tự nhận là một mệnh đề hiện hành về một control, nhưng không mang
bất kỳ nhãn nào trong năm hạng. Ngay sau đó, tệp nói số đo/probe/bảng đã chuyển sang
packet khác. Do đó nó vừa nằm ngoài danh sách bảy mệnh đề, vừa thiếu điều kiện đo cạnh
quan sát. Đây không phải lỗi grep: liệt kê theo từng đơn vị cho ra bảy mệnh đề có nhãn
cộng một mệnh đề không nhãn. Cam kết “mọi mệnh đề” và phép đếm đầy đủ vì vậy sai. Theo
luật severity của packet, một nhãn/phép đếm sai nghĩa là [P1].

**Phép đo tái lập:** 

```bash
nl -ba docs/GOI_AGENT_DA_NEN.md | sed -n '594,623p;653,692p'
git show --format=fuller --stat 770b3af3399b6794874008dd907f1dfaad6c5dba
```

Lệnh đầu cho thấy tuyên bố “mọi mệnh đề”, phép đếm bảy, bảy đơn vị có nhãn và mệnh đề
sandbox không nhãn. Lệnh thứ hai xác nhận mệnh đề này được giữ lại có chủ ý khi bảng số
và probe sandbox bị cắt khỏi packet; nó không phải phần giải thích vô tình của một hàng
bảng còn sống.

**Gợi ý cách vá bắt buộc:**

- **Vá ở đâu:** dòng 664-669, vì đây là phần dư của lát cắt và là nơi mệnh đề ngoài phạm
  vi được giữ lại; không sửa các con số dòng 619-623 trước khi quyết định số phận mệnh đề.
- **Vá thế nào:** đường rẻ nhất là để lại một con trỏ trung tính tới `MANG-SANDBOX-CODEX`
  / Issue #334 và bỏ kết luận thực chứng về mạng đóng, cấu hình mặc định, bất biến và
  ranh giới khỏi packet này. Đường đắt hơn là đưa mệnh đề, điều kiện đo, bằng chứng và
  đúng một nhãn sang packet #334; nếu vẫn giữ nó ở đây thì phải mở lại phạm vi và tính
  lại phép đếm theo chính luật của tệp.
- **Ca test khóa:** tự liệt kê lại từng mệnh đề sau dòng 609; mỗi mệnh đề trong phạm vi
  phải có đúng một nhãn canonical và một điều kiện/neo bằng chứng cạnh nó. Đột biến phải
  chết: biến con trỏ trung tính thành câu khẳng định sandbox “là/không là” một cơ chế
  chặn mà không cập nhật phạm vi, nhãn và phép đếm. Sau đó chạy lại `doctrine-scan` và
  N7b.
- **Bản vá có thể đẻ ra gì:** con trỏ có thể lại hàm ý một kết luận thực chứng như lỗi
  `--require-clean`, hoặc trỏ tới vị trí không kiểm được; còn giữ mệnh đề tại đây dễ làm
  N1/N2 trôi và đẩy số thêm vượt 200.

## CHỖ KHÔNG ĐO ĐƯỢC

- `KHÔNG_ĐO_ĐƯỢC` trạng thái GitHub trực tiếp: PR head, Packet Issue, lease
  `luat_dung_LAND`, spec hash, revision/generation và nội dung Issue #334. Lý do: mạng
  sandbox đóng theo chỉ thị; không gọi GitHub và không `git fetch`. Exact local HEAD,
  tree, ancestry và diff đã đo được như trên.
- `KHÔNG_ĐO_ĐƯỢC` ba bộ usage `78/5/10,8 M` · `85/10/12,8 M` · `45/1/3,7 M` từ
  dữ liệu gốc. Lý do: chính tệp khai `stdout.log` nằm ngoài Git và clone không chứa các
  log đó. Review này chỉ chứng minh chúng được giữ nguyên so với `7d7354e1` và rằng câu
  giới hạn/tương quan còn nguyên.
- `KHÔNG_ĐO_ĐƯỢC` việc gọi thật khối `claude -p`. Lý do: nó cần CLI/auth/provider và các
  MCP GitHub; chạy sẽ vượt phạm vi offline. Đã đo phần lỗi vòng 9 cần đo: cú pháp `bash`
  hợp lệ và không còn biến `$PROMPT` chưa gán.
- `KHÔNG_ĐO_ĐƯỢC` tái hiện các push/proxy/sandbox đã kể trong doctrine. Lý do: review
  bị cấm gọi mạng và bị cấm tự soạn payload phản chứng. Tôi chỉ kiểm tính tự nhất quán
  và neo bằng chứng sẵn có trong tệp/lịch sử Git.

## Kết luận

Hai finding vòng 9 đều **ĐÃ VÁ THẬT**, N6/N7 đều xanh, và N5 được giữ nguyên. Tuy
nhiên còn một [P1] độc lập: mệnh đề sandbox mồ côi làm sai hợp đồng nhãn/phép đếm và
thiếu điều kiện đo cạnh quan sát. Vì luật land chỉ bỏ chặn khi không còn [P1], SHA này
chưa đạt điều kiện đó. Không có finding [P2] trong lượt này.

`ops/reviews/doctrine-ranh-gioi-reviewer-review-11-codex-verdict.md` — [P1]: 1 · [P2]: 0
