verdict: changes_requested
reviewed_sha: 88bd4f2fe6e02803a97f2da9df86c8b43d53076f
reviewed_tree: 57e734c69468100687ca643d45a763f22736f613
provider: openai_codex
execution_surface: codex_cli
transport: machine

## ĐỐI CHIẾU NĂM FINDING VÒNG 2

| finding vòng 2 | phán quyết | phép đo độc lập trên head được review |
|---|---|---|
| `phan-hang-mang-tu-mau-thuan` [P1] | **ĐÃ VÁ THẬT** | `nl -ba docs/GOI_AGENT_DA_NEN.md \| sed -n '647,704p'`: tiêu đề dòng 647 không còn gọi sandbox là quan sát; dòng 659 xếp mạng mặc định vào hạng đóng; bảng mới dòng 670 ghi `128/0/0`; bảng hai pha dòng 696–697 không còn gọi mạng là quan sát. Bốn chỗ mà finding vòng 2 nêu đã đọc xuôi được với nhau. Giá trị probe chưa được tôi xác nhận độc lập vì `codex sandbox` lồng nhau hỏng; giới hạn này không làm sống lại mâu thuẫn văn bản cũ. |
| `nam-hang-khong-tao-phan-hoach` [P1] | **VÁ HỜ** | Bản vá đã sửa thành **NĂM**, định nghĩa đơn vị là “mệnh đề kèm điều kiện đo”, và áp ô dư ở dòng 636. Nhưng chính dòng 636 gộp hai điều kiện `Bash(x:*)` và `Bash` trần trong một hàng; dòng 683 và 696–697 lại dùng nhãn rút gọn `cơ chế đã xác minh`/`… CHỈ ở cấu hình mặc định`, không phải một trong hai nhãn đầy đủ có chiều. Audit Python in-memory cho `N2_allowedTools_same_row_narrow_and_bare=1` và liệt kê các nhãn rút gọn tại 683, 696, 697. |
| `n7-doc-claims-khong-phai-phep-n7` [P1] | **ĐÃ VÁ THẬT** | Lease revision 2 đã thay tiêu chí hỏng. N7a chạy thật cho `rc=0`, `doctrine-scan: sạch — đã quét 8 tệp, 0 chỗ chép doctrine`. N7b chạy thật cho `194  0  docs/GOI_AGENT_DA_NEN.md`, nên `194 <= 200`. Hai phép mới đều có lệnh, kết quả dương và chặt hơn hai vế cũ. |
| `probe-mang-moi-khong-tai-lap-duoc` [P2] | **VÁ HỜ** | Dòng 660–664 đã thêm cách gọi `codex sandbox` và mô tả ba phép trong `P`, nhưng không chứa thân `P` hay raw output. `git grep -F 'socket.socket().bind' 88bd4f2 -- docs .claude scripts ops` trả `rc=1`; không có `P`/`probe_r3.py` tracked; chạy nguyên văn phần cuối `python3 P` trả `rc=2`, `No such file or directory`. Probe đầy đủ do prompt cấp chạy trực tiếp được, nhưng hai lượt `codex sandbox` đều chết trước probe với `rc=101`, nên sáu số A/B vẫn chưa được tôi tái lập. |
| `ba-neo-cua-48cf331-dem-sai` [P2] | **ĐÃ VÁ THẬT** *(ngoài tệp được chấm)* | `git show 6802aa8:ops/leases/doctrine-ranh-gioi-reviewer-exec-1r2-claude-20260826.yaml` nay khai đúng “HAI mỏ neo chính xác + MỘT quan hệ tổ tiên”; `git merge-base --is-ancestor 48cf331e36cc2bde9fbdd485d51b85c81a5b25af 88bd4f2fe6e02803a97f2da9df86c8b43d53076f` trả `rc=0`. Theo chỉ thị, kết quả này không tham gia chấm tệp write set. |

## CHẤM N1–N7

| tiêu chí | kết quả | lệnh và bằng chứng |
|---|---|---|
| N1 | **ĐẠT** | `nl -ba ... \| sed -n '623,629p'` cho tiêu đề và câu mở đầu cùng ghi rõ **vỏ phiên điều phối** và đối tượng **quyền ghi vào kho**. Detector in-memory: baseline `1`; đột biến bỏ đối tượng khỏi tiêu đề `0`. Tiêu đề sandbox dòng 647 cũng tự ghi phạm vi “Trong sandbox codex”. |
| N2 | **KHÔNG ĐẠT** | Bảng định nghĩa đủ 5 hạng (`sed -n '606,612p' ... \| rg -c '^\| \*\*'` = `5`), nhưng audit vùng 623–715 tìm nhãn không thuộc từ vựng đóng tại dòng 683, 696 và 697. Dòng 636 còn đặt hai cấu hình vào một claim dù dòng 602–604 vừa định nghĩa đơn vị là claim đã kèm điều kiện. |
| N3 | **ĐẠT** | Bảng dòng 694–697 dùng cột `DỰA VÀO (kèm hạng)`, không còn `mạng đóng = **quan sát**`, và cả hai hàng đều ghi giới hạn “CHỈ ở cấu hình mặc định”. Detector baseline `1`; đột biến đổi lại header thành cột cưỡng chế `0`. Đoạn 699–712 nói thẳng đây là mặc định tự lật được, nên bảng và văn xuôi đọc xuôi được. |
| N4 | **ĐẠT** | Ngay trước bảng mạng, dòng 660–664 ghi ngày `26-08-2026`, `codex-cli 0.149.1`, mode `sandbox_mode=workspace-write` và biến thể `network_access=true`. Detector baseline `1`; đột biến bỏ version cụ thể `0`. |
| N5 | **ĐẠT** | Đối chiếu `git show 48cf331:docs/GOI_AGENT_DA_NEN.md \| rg ...` với `rg ... docs/GOI_AGENT_DA_NEN.md`: ví dụ thứ sáu vẫn tách ở 553–556; giới hạn `stdout.log` vẫn ở 570–572; “tương quan có neo” vẫn ở 574–576. Ba hàng số vẫn nguyên `78/5/10,8 M`, `85/10/12,8 M`, `45/1/3,7 M`. |
| N6 | **ĐẠT** | `git diff --name-status c35ae1c0a1104dbd6e65a321cda3b9f9441a408b..88bd4f2fe6e02803a97f2da9df86c8b43d53076f` chỉ in `M docs/GOI_AGENT_DA_NEN.md`; `git diff --check ...` trả `rc=0`. |
| N7a | **ĐẠT** | `python3 .claude/dev/packet_loop.py doctrine-scan --root . --path docs/GOI_AGENT_DA_NEN.md` trả `rc=0` và in đúng `đã quét 8 tệp`. |
| N7b | **ĐẠT** | `git diff --numstat c35ae1c0a1104dbd6e65a321cda3b9f9441a408b -- docs/GOI_AGENT_DA_NEN.md` trả `194  0`, nên cột thêm không vượt 200. |

## FINDING HIỆN HÀNH

### `nam-hang-khong-tao-phan-hoach` [P1] — đơn vị “claim + điều kiện” được định nghĩa rồi bị gộp lại ngay khi áp dụng

**Tệp/dòng:** `docs/GOI_AGENT_DA_NEN.md:602`, `:636`, `:683`, `:696`, `:697`.

**Trích dòng:** dòng 602–604 nói đơn vị là “MỆNH ĐỀ KÈM ĐIỀU KIỆN ĐO”; dòng 636 lại viết cùng một hàng “luật `Bash(x:*)` … hoặc … `Bash` trần”; dòng 696–697 dùng `cơ chế đã xác minh — CHỈ ở cấu hình mặc định` thay vì hạng đã định nghĩa `cơ chế đã xác minh — chiều ĐÓNG`.

**Phép đo tái lập:** audit in-memory đã chạy trên blob `f8c4449e05a14d77fd38b1af092e23f863ae1f7f` cho:

```text
N2_allowedTools_same_row_narrow_and_bare=1
N2_generic_rank:683: ... cơ chế đã xác minh ...
N2_generic_rank:696: ... cơ chế đã xác minh ... CHỈ ở cấu hình mặc định ...
N2_generic_rank:697: ... cơ chế đã xác minh — CHỈ ở cấu hình mặc định ...
```

Đây không chỉ là khác cách viết: hàng `--allowedTools` không còn là một đơn vị phân loại theo định nghĩa của chính mục, còn cấu hình mở mạng ở dòng 670/676–678 không được gắn nhãn đầy đủ `chiều MỞ`. Vì thế bảng chưa phân hoạch mọi claim thành đúng một trong năm hạng và N2 đỏ.

**Gợi ý vá:**

- Vá ở vùng taxonomy và hai bảng trong đúng tệp này, vì lỗi là quan hệ giữa định nghĩa với các lần áp dụng, không phải ở gate hay launcher.
- Tách mỗi cấu hình/chiều thành một claim riêng; dùng nguyên văn đúng một trong năm nhãn, gồm cả `chiều ĐÓNG`/`chiều MỞ`, thay vì nhãn rút gọn. Nếu chưa có phép đo cho một claim cụ thể thì gắn riêng `chưa xếp được`, không gộp nó với cấu hình đã biết.
- Ca khóa: detector phải đếm mỗi claim-condition có đúng một nhãn canonical; đột biến bỏ `chiều`, gộp hai cấu hình vào một hàng, hoặc gắn hai nhãn cho một claim đều phải đỏ. Detector phải bỏ qua các câu lịch sử được trích dẫn.
- Rủi ro của bản vá là biến kiểm tra thành grep từ khóa rồi báo giả trên phần kể lịch sử; vì vậy phạm vi detector phải neo vào các bảng/claim vận hành, không quét mù toàn tệp.

### `probe-mang-moi-khong-tai-lap-duoc` [P2] — lệnh mới vẫn phụ thuộc một tệp `P` không có trong artefact

**Tệp/dòng:** `docs/GOI_AGENT_DA_NEN.md:660-670`.

**Trích dòng:** tài liệu gọi `... -- python3 P` rồi chỉ mô tả bằng văn xuôi rằng `P` in ba mã thoát. Không có thân script hay raw output đi kèm.

**Phép đo tái lập:** `git grep -F 'socket.socket().bind' 88bd4f2 -- docs .claude scripts ops` trả `rc=1`; tìm path tracked `P`/`probe_r3.py` trả `rc=1`; `python3 P` trả `rc=2`. Probe đầy đủ từ prompt cho `1/1/128` khi chạy trực tiếp trong sandbox mặc định của phiên này. Hai lượt lồng nhau, cả mặc định và bật mạng, đều trả `rc=101` trước khi Python chạy vì không mở được khóa mount bubblewrap chỉ-đọc.

**Gợi ý vá:**

- Vá ngay cạnh bảng mạng trong tệp write set: đây là nơi đang đưa sáu số vào doctrine và là nơi người đọc cần phép tái lập.
- Đưa thân probe copy/paste-runnable hoặc raw command/output đã neo version vào cùng mục; không để `P` là metavariable không có hiện vật. Tiếp tục giữ nhãn theo ngày/version/configuration, không nâng số đo một phiên thành bất biến.
- Ca khóa: trên môi trường cho phép chạy `codex sandbox`, chạy probe mặc định và bật mạng, assert đủ ba dòng cùng mã; đột biến một kỳ vọng, hoặc bỏ thân `P`, phải đỏ. Nếu lồng sandbox không được thì kết quả bắt buộc là `KHÔNG_ĐO_ĐƯỢC`, không pass.
- Rủi ro là raw output sẽ trôi theo CLI/proxy; giảm bằng cách ghi điều kiện đo ngay cạnh và giữ phép đo như snapshot có hạn dùng.

## CHỖ KHÔNG ĐO ĐƯỢC

- Hai lệnh `codex sandbox` lồng nhau không chạy được: cả mặc định lẫn `network_access=true` đều `rc=101`, hỏng tại khóa `/tmp/codex-bwrap-synthetic-mount-targets-0/lock` vì mount chỉ-đọc. Vì vậy tôi không xác nhận độc lập hai cột A/B `1/1/128` và `0/0/0`.
- Lệnh Python trực tiếp cho `1/1/128`, không phải `0/0/0`; nhưng shell hiện tại đã nằm trong sandbox mặc định của Codex, không phải vỏ điều phối Claude mà dòng 625 định nghĩa. Do khác execution surface, kết quả này không đủ để bác cột đối chứng Claude; nó chỉ chứng minh điều kiện môi trường là material.
- Không có mạng/GitHub theo điều kiện vận hành, nên không đo trạng thái động của Issue #318, PR #322 hay CI. Exact SHA, tree, branch và refs cục bộ đã đo được.
- Ba `stdout.log` của bảng 78/85/45 không có trong kho; tôi chỉ xác nhận chúng được giữ nguyên và lời giới hạn vẫn còn, không xác nhận được số gốc.
- Lease revision 2 cục bộ xác nhận `revision: 2`, `generation: 1` và exact head, nhưng tự khai không có spec riêng và không có `spec_hash`; trường `spec_hash` vì vậy **KHÔNG_ĐO_ĐƯỢC** từ artefact cục bộ.

Đường dẫn verdict: `ops/reviews/doctrine-ranh-gioi-reviewer-review-3-codex-verdict.md`

Số finding: **P1 = 1 · P2 = 1**
