verdict: changes_requested
reviewed_sha: e68e9fac23690399121b76d6ea3c35a6c5e9a067
reviewed_tree: 0cfa60aed6ac8d4b4291ea494c07272da9d4695a
base_sha: c35ae1c0a1104dbd6e65a321cda3b9f9441a408b
packet: wp318 (`DOCTRINE-RANH-GIOI-REVIEWER`)
review_round: 13
provider: openai_codex
execution_surface: codex_service
transport: machine
role: reviewer
independent_from_executor_session: true

# Cross-review vòng 13 — packet #318

## Kết luận

`changes_requested`. Còn **1 finding [P1]**, **0 finding [P2]**. Không có slug mới: finding còn lại vẫn là `menh-de-sandbox-mo-coi-khong-nhan`, đúng quy ước không đếm đôi cùng một gốc lỗi.

Bản vá đã sửa thật câu phạm vi và vị trí neo đo, nhưng sinh một lời khai đo sai ngay trong neo mới: dòng 678 nói chỉ thêm cờ `network_access` thì `lsremote_rc=0`, trong khi phép đo gốc ở dòng 328–339 và chính dòng 681–683 đều nói hai cờ `network_access` và `writable_roots` được bật cùng lúc. Vì chưa có phép thử tách từng cờ, dữ liệu hiện có không xác minh cơ chế riêng của mạng. Nhãn của mệnh đề thứ tám vì thế phải là `chưa xếp được`, không phải `cơ chế đã xác minh — chiều MỞ`; phân bố đúng theo dữ liệu hiện có là `chiều ĐÓNG` ×1 · `chiều MỞ` ×4 · `chưa xếp được` ×3 · `máy phát hiện` ×0 · `quan sát chưa rõ cơ chế` ×0.

Luật dừng `luat_dung_LAND` được áp đúng nghĩa: đây là [P1] vì tệp đang khai một phép đo không xảy ra, gắn nhãn mạnh hơn bằng chứng và giữ một phân bố chỏi với tám đơn vị tự liệt kê. Không hạ xuống [P2] vì packet đã qua nhiều vòng.

## ĐỐI CHIẾU LƯỢT TRƯỚC

- `menh-de-sandbox-mo-coi-khong-nhan`: **VÁ SINH LỖI MỚI**. N1 đã được vá: câu phạm vi nay bao đúng tám mệnh đề. N4 đã được vá về vị trí: điều kiện và kết quả A/B được viết ngay cạnh mệnh đề, không còn chỉ trỏ sang #334. Nhưng neo mới mô tả sai biến đã đổi và dùng phép A/B hai-biến để xác minh một cơ chế một-biến; từ đó làm N2, N3 và phân bố bằng chứng sai.

## Bốn đối chiếu bắt buộc

1. **Phạm vi:** khớp `5 + 3 = 8`. Năm mệnh đề bảng là: (1) luật hẹp `Bash(x:*)`; (2) `Bash` trần; (3) `codex -s workspace-write` ghi ngoài cây; (4) xoá credential khỏi env; (5) token rác trong URL. Ba mệnh đề văn xuôi là: (6) proxy ambient; (7) bộ ba clone rời/`--require-clean`/kiểm cây sạch đối với quyền ghi; (8) mạng sandbox. Không có mệnh đề thứ tám nào bị loại khỏi phạm vi.
2. **Vị trí điều kiện đo:** đạt yêu cầu vị trí của N4. Dòng 676–686 ghi ngay tại chỗ phép A/B, mode sandbox, execution surface và caveat hai cờ; đây không còn là con trỏ trần. Tính đúng của điều kiện lại không đạt: dòng 678 khai một cờ, dòng 682 khai hai cờ. Sai nội dung này được chấm riêng ở N2/N3, không nhập nhằng với tiêu chí vị trí.
3. **Neo:** không sinh neo thứ hai. Trong vùng dòng 592–699 chỉ có đúng một `Issue #334` và một `MANG-SANDBOX-CODEX`; câu “NEO DUY NHẤT” còn ở dòng 597–599. Các lần nói “packet kia” quy chiếu về neo đó.
4. **Phép A/B hai cờ:** lời khai “mệnh đề chỉ nói cấu hình đổi được kết quả” không đứng được. Mệnh đề thực tế ở dòng 674–675 nói riêng rằng *mạng đóng* là mặc định cấu hình, “biết cơ chế”, rồi nhận nhãn `cơ chế đã xác minh — chiều MỞ`. A/B hai-biến chỉ chứng minh tổ hợp cấu hình đổi kết quả; nó không đo cờ nào là nguyên nhân. `git ls-remote` không ghi `.git` làm suy luận về `network_access` hợp lý, nhưng bảng hạng đòi cơ chế **đã xác minh**, không phải cơ chế suy luận. Hạng `quan sát chưa rõ cơ chế` cũng chưa đạt vì mục không ghi số lần lặp và phiên bản ngay tại quan sát; theo chính định nghĩa dòng 618 và giải thích dòng 643–647, hạng còn lại là `chưa xếp được`.

## Quét toàn mục

Đã đọc tuyến tính từ tiêu đề `NĂM HẠNG bằng chứng` ở dòng 592 qua hết bảng đo ở dòng 699, rồi đọc tiếp phần giải nghĩa tới dòng 719.

- Không còn câu nào nói hoặc hàm ý bằng chứng của **mệnh đề thứ tám** nằm ở packet khác. Dòng 627–629 và 676–686 nói rõ điều ngược lại. Câu ở dòng 697 về cơ chế “theo mục sandbox sang packet kia” thuộc mệnh đề thứ ba — hành vi ghi ngoài cây — không phải mệnh đề mạng thứ tám.
- Không còn câu nào loại mệnh đề thứ tám khỏi phạm vi. Dòng 594–601 đưa đúng một mệnh đề mạng vào phạm vi và phép đếm.
- `5 + 3 = 8` khớp tám đơn vị thực tế. Tuy nhiên phân bố `1/5/2/0/0` ở dòng 625–626 không đứng sau khi chấm đúng nghĩa mệnh đề thứ tám; phân bố phải là `1/4/3/0/0`.
- Không thấy câu chỏi hoặc con số chỏi nào khác trong vùng được yêu cầu ngoài cùng gốc lỗi trên.

## Bảng chấm nghiệm thu

| Tiêu chí | Kết quả | Bằng chứng và lệnh |
|---|---|---|
| N1 | PASS | `nl -ba docs/GOI_AGENT_DA_NEN.md | sed -n '592,699p'`; tự liệt kê ở trên cho đúng 5 mệnh đề bảng + 3 văn xuôi. |
| N2 | **FAIL [P1]** | Dòng 674–686 gắn `cơ chế đã xác minh — chiều MỞ` cho cơ chế mạng chưa được phép A/B tách riêng. Đối chiếu với định nghĩa dòng 616–620 cho ra `chưa xếp được`; phân bố phải đổi từ `1/5/2` thành `1/4/3`. |
| N3 | **FAIL [P1]** | Dòng 678 khẳng định thêm riêng cờ mạng thì `lsremote_rc=0`; dòng 328–339 và 681–683 chỉ ghi phép đo bật đồng thời hai cờ, đồng thời nói chưa ai chạy riêng từng cờ. Đây là điều chưa đo nhưng lại được dùng làm căn cứ. |
| N4 | PASS | Điều kiện đo nằm ngay dòng 676–686 cạnh mệnh đề. PASS này chỉ chấm vị trí; nó không hợp thức hoá lời khai sai về số biến, đã bị N2/N3 bắt. |
| N5 | PASS | `rg -n -F 'tương quan có neo'`, `rg -n -F 'stdout.log'`, `rg -n -F 'bash /tmp/refscan.sh'`, và `rg -n '78|85|45|10,8 M|12,8 M|3,7 M' docs/GOI_AGENT_DA_NEN.md` lần lượt xác nhận ba P2 cũ và các dòng `78/5/10,8 M`, `85/10/12,8 M`, `45/1/3,7 M`; patch `fa9a505d0926a56603cabfb998bd4832084ed68f..HEAD` không chạm chúng. |
| N6 | PASS | `git diff --name-status c35ae1c0a1104dbd6e65a321cda3b9f9441a408b..HEAD` in đúng `M docs/GOI_AGENT_DA_NEN.md`; `git status --short --branch` trước khi ghi verdict chỉ in `## HEAD (no branch)`. |
| N7a | PASS | `python3 .claude/dev/packet_loop.py doctrine-scan --root . --path docs/GOI_AGENT_DA_NEN.md` → `rc=0`, `doctrine-scan: sạch — đã quét 8 tệp, 0 chỗ chép doctrine`. |
| N7b | PASS | `git diff --numstat c35ae1c0a1104dbd6e65a321cda3b9f9441a408b -- docs/GOI_AGENT_DA_NEN.md` → `197  0`; `197 <= 200`, còn biên 3 dòng. |

Lệnh bổ trợ: `git diff --check c35ae1c0a1104dbd6e65a321cda3b9f9441a408b -- docs/GOI_AGENT_DA_NEN.md` → `rc=0`, không có output; `git rev-parse HEAD` → `e68e9fac23690399121b76d6ea3c35a6c5e9a067`; `git rev-parse HEAD^{tree}` → `0cfa60aed6ac8d4b4291ea494c07272da9d4695a`.

## Finding

### `menh-de-sandbox-mo-coi-khong-nhan` [P1] — neo mới khai phép một-cờ nhưng bằng chứng chỉ có phép hai-cờ

**Tệp/dòng:** `docs/GOI_AGENT_DA_NEN.md:674`, đặc biệt dòng 677–686; phân bố tại dòng 625–626; phép đo gốc tại dòng 328–339.

**Trích dòng:**

> “thêm `-c 'sandbox_workspace_write.network_access=true'` thì `lsremote_rc=0`”

và bốn dòng sau:

> “nó bật HAI cờ cùng lúc (`network_access` và `writable_roots`)”

Hai câu không thể cùng mô tả một phép đo. Phép đo gốc nói “Mở đúng hai chốt” rồi liệt kê cả hai cờ trước khi ghi `fetch_rc=0`, `lsremote_rc=0`.

**Phép đo tái lập được:** chạy

```bash
nl -ba docs/GOI_AGENT_DA_NEN.md | sed -n '328,342p;622,629p;670,699p'
```

Kết quả trên exact SHA được review cho thấy: cặp cờ ở 333–335; kết quả sau khi thêm cặp ở 338–339; lời khai một cờ ở 677–679; tự thú phép hai cờ ở 681–683; phân bố cũ ở 625–626. Đây là phản chứng nội tại, không cần và không được thay bằng lời khai Executor.

**Gợi ý vá — ở đâu:** sửa chính đoạn 674–686 vì đây là nơi mệnh đề, nhãn và điều kiện đo phải đi cùng nhau; sửa đồng bộ phân bố dòng 625–626. Không chuyển căn cứ sang #334 và không tạo neo mới.

**Gợi ý vá — thế nào:** đường rẻ nhất là viết đúng phép đã đo: mặc định lỗi kết nối; thêm **đồng thời cặp cờ** thì `lsremote_rc=0`; chưa tách được cờ gây đảo kết quả. Hạ mệnh đề mạng xuống `chưa xếp được`, rồi đổi phân bố thành `chiều MỞ` ×4 và `chưa xếp được` ×3. Có thể thay/rút gọn các dòng hiện có, không cần tăng số dòng; như vậy vẫn ở dưới trần 200. Đường đắt hơn là chạy A/B chỉ đổi `network_access`, ghi exact version/điều kiện/kết quả ngay cạnh rồi mới giữ nhãn hiện tại, nhưng phép ấy hiện chưa có trong evidence của packet này.

**Ca test khoá:** chạy lại lệnh `nl -ba` trên, tự liệt kê tám mệnh đề và kiểm ba điều cùng lúc: (a) lời mô tả số cờ khớp phép gốc; (b) nhãn mạng khớp định nghĩa; (c) tổng vẫn là 8 với phân bố mới. Đột biến cần chết: đổi “đồng thời hai cờ” thành “chỉ cờ mạng” mà không có phép A/B tách riêng, hoặc đổi nhãn mà giữ phân bố `1/5/2`.

**Bản vá có thể đẻ ra gì:** hạ nhãn mà quên phân bố sẽ tạo một con số chỏi mới; rút đoạn quá mạnh có thể làm mất điều kiện đo cạnh mệnh đề hoặc tạo neo #334 thứ hai. Vì ngân sách chỉ còn 3 dòng, hướng đúng là cắt/viết ngắn lại hay thay dòng hiện có, không xin nâng trần.

## CHỖ KHÔNG ĐO ĐƯỢC

- `KHÔNG_ĐO_ĐƯỢC`: cờ nào trong cặp `network_access`/`writable_roots` thực sự làm `lsremote_rc` đổi. Clone không có một lượt tách từng cờ; mạng sandbox mặc định đóng và chỉ thị review cấm gọi GitHub. Suy luận rằng `ls-remote` không ghi `.git` không thay được phép đo cơ chế.
- `KHÔNG_ĐO_ĐƯỢC`: nội dung và số đo đầy đủ của Issue #334, vì chúng không có trong clone và review bị cấm gọi GitHub. Verdict không dùng chúng làm evidence.
- `KHÔNG_ĐO_ĐƯỢC`: dữ liệu gốc của ba dòng usage `78/5/10,8 M`, `85/10/12,8 M`, `45/1/3,7 M`, vì `stdout.log` nằm trong scratchpad lịch sử và không được git theo dõi. Chỉ đo được rằng ba lời khai cùng ba P2 cũ được giữ nguyên trong tệp.
- `KHÔNG_ĐO_ĐƯỢC`: trạng thái CI/PR/GitHub hiện hành. Theo điều kiện vận hành, không gọi mạng, không `git fetch`; chỉ exact local commit/tree và gate offline nêu trên được đo.

---

Verdict: `ops/reviews/doctrine-ranh-gioi-reviewer-review-13-codex-verdict.md`
Finding: **[P1] 1 / [P2] 0**
