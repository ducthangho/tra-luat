verdict: changes_requested
reviewed_sha: d9c24ddaecb8b94dd234d77819745e96ea4226d1
reviewed_tree: 077334b6aedd54ed13036a5779e4ecdd9520df6f
base_sha: c35ae1c0a1104dbd6e65a321cda3b9f9441a408b
round_13_head: e68e9fac23690399121b76d6ea3c35a6c5e9a067
provider: openai_codex
execution_surface: Codex service
transport: machine
review_pair: claude executor / codex reviewer

# Cross-review vòng 14 — packet #318 `DOCTRINE-RANH-GIOI-REVIEWER`

## Kết luận ngắn

`changes_requested`. Còn đúng một finding [P1], giữ nguyên stable ID
`menh-de-sandbox-mo-coi-khong-nhan`; không mở slug mới cho cùng một lỗi gốc.

Bản vá vòng 13 đã sửa thật bốn phần được khai: gỡ suy luận một-cờ, hạ nhãn về
`chưa xếp được`, sửa phân bố thành `1/4/3/0/0`, đổi “hai ô” thành “ba ô”, và
thêm lý do thứ ba. Nhưng việc hạ nhãn làm lộ một câu văn xuôi cũ chưa được hạ
theo: dòng 675 vẫn nói “biết cơ chế”, trong khi dòng 682–684 nói chính phép A/B
hai-biến chưa xác minh được cơ chế. Đây là câu chỏi về nội dung bằng chứng, nên
là [P1] theo luật dừng đã chốt.

Phán quyết finding vòng 13:
**`menh-de-sandbox-mo-coi-khong-nhan` — VÁ SINH LỖI MỚI.**

## Preflight và phạm vi đo

- `git rev-parse HEAD` →
  `d9c24ddaecb8b94dd234d77819745e96ea4226d1`.
- `git rev-parse HEAD^{tree}` →
  `077334b6aedd54ed13036a5779e4ecdd9520df6f`.
- `git rev-parse HEAD^` →
  `e68e9fac23690399121b76d6ea3c35a6c5e9a067`.
- `git merge-base --is-ancestor c35ae1c0a1104dbd6e65a321cda3b9f9441a408b HEAD`
  → `rc=0`.
- Trước khi ghi verdict, `git status --porcelain=v1` rỗng; checkout detached,
  `.git` chỉ đọc. Không gọi mạng, không fetch, không commit, không push.
- Diff round 13 → round 14 chỉ chạm `docs/GOI_AGENT_DA_NEN.md`.

## ĐỐI CHIẾU LƯỢT TRƯỚC

### Bốn điều được kiểm riêng

1. **Câu khai một-cờ: đã gỡ thật.**

   `nl -ba docs/GOI_AGENT_DA_NEN.md | sed -n '671,687p'` cho thấy dòng
   677–680 hiện nói rõ phép A/B bật **hai** cờ cùng lúc. Không còn câu nói chỉ
   thêm `network_access` thì `lsremote_rc=0`; dòng 682–684 còn nói thẳng việc
   quy nguyên nhân cho cờ mạng chỉ là suy luận.

2. **Nhãn chính thức và lý do hạ nhãn: phần vá này đúng, nhưng toàn mệnh đề vẫn
   chỏi.**

   - Dòng 676 gắn đúng một nhãn chính thức: `chưa xếp được`.
   - Dòng 682–684 nói đúng lý do không phải `chiều MỞ`: phép A/B đổi hai biến,
     nên chưa biết cờ nào là nguyên nhân và chưa đạt điều kiện “cơ chế đã xác
     minh”.
   - Dòng 684–686 nói đúng lý do không phải `quan sát chưa rõ cơ chế`: quan sát
     không ghi phiên bản và số lần lặp ngay tại chỗ, trong khi định nghĩa dòng
     618 đòi các điều kiện đó.
   - Tuy nhiên dòng 675, nằm ngay trong phần chữ đậm của chính mệnh đề được gắn
     nhãn, vẫn viết “biết cơ chế KHÔNG làm nó thành ranh giới”. Trong cấu trúc
     “mệnh đề: nội dung ⇒ nhãn”, cụm này không được đánh dấu là giả định
     “nếu/dù”; nó khai rằng cơ chế đã biết. Dòng 682–684 lại phủ định đúng điều
     ấy. Vì vậy nhãn đã hạ đúng nhưng mệnh đề chưa nhất quán về nghĩa.

3. **Ba số phụ thuộc: đã cùng đổi, không bỏ sót.** Tôi đọc từng đơn vị, không
   suy từ số lần xuất hiện của cụm nhãn:

   - Phân bố ở dòng 625–626: `chiều ĐÓNG` ×1 · `chiều MỞ` ×4 ·
     `chưa xếp được` ×3 · `máy phát hiện` ×0 ·
     `quan sát chưa rõ cơ chế` ×0.
   - Câu giải thích ở dòng 640–641: “ba ô `chưa xếp được`”.
   - Danh sách lý do ở dòng 643–648 có đủ ba đơn vị: hàng `workspace-write`;
     bộ-ba-với-quyền-ghi; mạng sandbox với phép A/B bật hai cờ cùng lúc.

4. **Phạm vi `5 + 3 = 8`: vẫn khớp tám đơn vị thực tế.** Tự liệt kê:

   1. `--allowedTools` luật hẹp — `chiều ĐÓNG`;
   2. `--allowedTools` với `Bash` trần — `chiều MỞ`;
   3. `codex -s workspace-write` ghi ngoài cây — `chưa xếp được`;
   4. xoá credential khỏi env — `chiều MỞ`;
   5. token rác trong URL — `chiều MỞ`;
   6. cơ chế proxy ambient — `chiều MỞ`;
   7. bộ ba clone rời + `--require-clean` + kiểm cây sạch, xét quyền ghi/push —
      `chưa xếp được`;
   8. mệnh đề mạng sandbox — `chưa xếp được`.

   Tổng đúng `1/4/3/0/0`, đúng tám mệnh đề. Không còn câu đếm
   `chiều MỞ` ×5 trong mục được quét.

Vì ba phần vá chính đã đúng nhưng câu cũ ở dòng 675 trở thành lời khai chỏi với
nhãn và lý do mới, kết quả không phải `VÁ HỜ` hay `CHƯA VÁ`; nó là
`VÁ SINH LỖI MỚI`.

## Bảng chấm N1–N7

| Tiêu chí | Kết quả | Bằng chứng và lệnh đã chạy |
|---|---|---|
| N1 | ĐẠT | Câu phạm vi dòng 594–601 giới hạn đúng vào 3 control trong bảng → 5 mệnh đề, cộng 3 mệnh đề văn xuôi; tám đơn vị đọc lại khớp. Lệnh: `nl -ba docs/GOI_AGENT_DA_NEN.md | sed -n '592,722p'`. |
| N2 | KHÔNG ĐẠT | Nhãn chính thức ở dòng 676 là `chưa xếp được`, nhưng nội dung cùng mệnh đề ở dòng 675 vẫn khai “biết cơ chế”, chỏi với dòng 682–684 và với nghĩa của hạng. Một stable finding [P1], không tách slug. |
| N3 | KHÔNG ĐẠT | Exact tree chỉ có A/B hai-biến; câu “biết cơ chế” ở dòng 675 mạnh hơn thứ người đọc exact tree kiểm được. Bằng chứng packet #334 chưa land không được dùng để cứu câu này. |
| N4 | ĐẠT | Điều kiện đo nằm cạnh quan sát ở dòng 677–681: cùng lệnh, hai cờ bật đồng thời, codex CLI trong container này, sandbox `workspace-write`, vỏ phiên điều phối; dòng 682–686 khai phần chưa tách và thiếu phiên bản/lần lặp. |
| N5 | ĐẠT | Dòng 553–556 giữ riêng ví dụ thứ sáu `bash /tmp/refscan.sh`; dòng 570–572 giữ `stdout.log` không tái lập; dòng 574–577 giữ “tương quan có neo”. Bảng dòng 566–568 giữ nguyên `78/5/10,8 M` · `85/10/12,8 M` · `45/1/3,7 M`. |
| N6 | ĐẠT | `git diff --name-only e68e9fac23690399121b76d6ea3c35a6c5e9a067..HEAD` → đúng một dòng `docs/GOI_AGENT_DA_NEN.md`, `rc=0`. `git diff --check` trên cùng phạm vi → `rc=0`. |
| N7a | ĐẠT | `python3 .claude/dev/packet_loop.py doctrine-scan --root . --path docs/GOI_AGENT_DA_NEN.md` → `doctrine-scan: sạch — đã quét 8 tệp, 0 chỗ chép doctrine`, `rc=0`. |
| N7b | ĐẠT | `git diff --numstat c35ae1c0a1104dbd6e65a321cda3b9f9441a408b -- docs/GOI_AGENT_DA_NEN.md` → `198  0  docs/GOI_AGENT_DA_NEN.md`, `rc=0`; cột thêm 198 ≤ 200, còn biên 2 dòng. |

## Finding

### `menh-de-sandbox-mo-coi-khong-nhan` [P1] — nhãn đã hạ nhưng nội dung vẫn khai cơ chế đã biết

**Tệp/dòng:** `docs/GOI_AGENT_DA_NEN.md:675-676`, đối chiếu
`docs/GOI_AGENT_DA_NEN.md:682-684`.

**Vấn đề:** Dòng 675 là một phần của nội dung mệnh đề thứ tám và nói “biết cơ
chế KHÔNG làm nó thành ranh giới”; dòng 676 gắn `chưa xếp được`; dòng 682–684
lại nói phép A/B hai-biến không xác minh được cơ chế. Một mệnh đề không thể vừa
khai biết cơ chế vừa lấy việc chưa xác minh cơ chế làm lý do cho hạng dư. Việc
packet #334 đã đo ra nguyên nhân trên một nhánh chưa land chỉ làm câu ấy tình cờ
đúng ngoài clone; nó không biến thành evidence của exact SHA này.

**Phép đo tái lập:**

```text
nl -ba docs/GOI_AGENT_DA_NEN.md | sed -n '671,687p'
```

Kết quả dương cần đọc cùng nhau:

- dòng 675: “biết cơ chế ...”;
- dòng 676: `chưa xếp được`;
- dòng 682–684: “KHÔNG đo cờ nào là nguyên nhân” và bảng đòi cơ chế “ĐÃ XÁC
  MINH”.

**Gợi ý cách vá:**

1. **Vá ở đâu:** ngay dòng 675 trong nội dung mệnh đề thứ tám. Đây là nơi phát
   sinh mâu thuẫn; không sửa bảng định nghĩa, phân bố hoặc nhãn vì ba chỗ ấy hiện
   đúng.
2. **Vá thế nào:** viết lại riêng vế “biết cơ chế ...” để chỉ khai thứ A/B
   hai-biến chứng minh được: tổ hợp cấu hình đổi kết quả nhưng cơ chế riêng chưa
   được xác minh. Nếu ý định chỉ là một mệnh đề giả định tổng quát, phải ghi rõ
   “ngay cả nếu” hoặc “dù”, không để nó đọc như lời khai hiện tại.
3. **Ca khóa:** đọc lại riêng tám đơn vị như danh sách phía trên, rồi chạy N7a và
   N7b. Đột biến phải bị bắt bằng review ngữ nghĩa là khôi phục cụm “biết cơ chế”
   trong khi vẫn giữ nhãn `chưa xếp được` và lý do “không đo cờ nào”; N2/N3 phải
   đỏ. `doctrine-scan` hiện chỉ chứng minh hình thức, không tự bắt được mâu thuẫn
   ngữ nghĩa này.
4. **Rủi ro bản vá:** viết quá tay có thể xoá mất điều A/B thật sự chứng minh
   (tổ hợp cấu hình đổi kết quả), tái nâng nhãn, làm phân bố lệch, hoặc làm mất
   đường quay lại packet #334. Vì vậy chỉ thay vế chỏi, rồi đọc lại cả tám đơn vị.

**Ngân sách vá:** hướng trên là viết lại một dòng hiện có, dự kiến không tăng cột
THÊM; kể cả phải tách thêm một dòng vẫn nằm trong biên 2. Không cần và không được
nâng trần 200.

**Finding mới:** không có slug mới. Câu chỏi vẫn thuộc đúng mệnh đề và lỗi gốc
`menh-de-sandbox-mo-coi-khong-nhan`, nên tách slug sẽ làm hỏng lịch sử finding.

## Câu hỏi về packet #334 và đường quay lại

Với riêng tệp này ở exact SHA được review, `chưa xếp được` là hạng **đúng**, không
phải “hạng thấp hơn sự thật”. Hạng ở đây đo trạng thái bằng chứng mà người đọc
exact tree có thể kiểm: mệnh đề có cơ chế được xác minh và có điều kiện đo đủ hay
không. Nó không phải nhãn chân trị của thế giới bên ngoài. Một kết quả đúng nằm
trên nhánh packet khác, chưa land và không có trong clone, không phải evidence độc
lập của tệp này. Việc lời khai tình cờ đúng không đổi tiêu chuẩn đã áp ở vòng 12
và 13.

Tệp có sẵn đường quay lại ở dòng 685–686: nêu phép tách bốn tổ hợp và nói sau khi
phép tách của packet kia hoàn tất thì hạng này đo lại được. Trong review exact-tree
này, “hoàn tất” chỉ có thể dùng khi evidence đã land và đọc được; câu đó yêu cầu
**đo lại**, không tự động nâng hạng theo trạng thái ngoài repo. Vì vậy không mở
finding riêng về thiếu đường quay lại.

## CHỖ KHÔNG ĐO ĐƯỢC

- `KHÔNG_ĐO_ĐƯỢC` trạng thái GitHub hiện hành, PR head, lease, receipt và trạng
  thái land của packet #334: mạng bị đóng theo chỉ thị; không gọi GitHub và không
  fetch.
- `KHÔNG_ĐO_ĐƯỢC` phép tách bốn tổ hợp của packet #334: bằng chứng không có trong
  clone ở `d9c24ddaecb8b94dd234d77819745e96ea4226d1`; tôi cố ý không dùng lời mô tả
  trong prompt làm evidence độc lập để nâng hạng.
- `KHÔNG_ĐO_ĐƯỢC` raw `stdout.log` của ba lượt tạo các số
  `78/5/10,8 M` · `85/10/12,8 M` · `45/1/3,7 M`: chính tệp nói các log nằm ngoài
  Git. Tôi chỉ đo được các số và ba P2 cũ còn được giữ nguyên trong exact tree,
  không tái lập được nguồn thô của chúng.
- `KHÔNG_ĐO_ĐƯỢC` Packet revision, generation, spec hash và Review Class từ repo:
  chúng không có trong clone dưới hồ sơ #318. Phạm vi review này dựa trên chỉ thị
  trực tiếp của người giữ kho trong prompt, exact SHA/base/write set và acceptance
  r2 đã đóng băng tại đó.

## Kết luận

N1, N4, N5, N6, N7a và N7b đạt. N2 và N3 chưa đạt do cùng một [P1] còn lại.
Theo `luat_dung_LAND`, chỉ [P1] chặn land; lượt này còn [P1]=1 nên verdict là
`changes_requested`. Không có [P2] mới hoặc [P2] chưa đặt tên trong verdict này.

Đường dẫn verdict: `ops/reviews/doctrine-ranh-gioi-reviewer-review-14-codex-verdict.md`

Số finding: [P1]=1 · [P2]=0
