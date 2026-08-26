# Cross-review vòng 9 — packet #318

```yaml
verdict: changes_requested
reviewed_sha: 7d7354e14c540c3c2afd3f3a594ff2e432f6fd44
reviewed_tree: eee35b0782fde46fc5492f26b89b7e7aa2c3477c
base_sha: c35ae1c0a1104dbd6e65a321cda3b9f9441a408b
packet_revision: 4
generation: 1
reviewer: codex
provider: openai_codex
execution_surface: codex_service
transport: machine
```

## Kết luận

`changes_requested`, còn **1 finding P1** và **1 finding P2**. P1 là mệnh đề `--require-clean` ngoài phạm vi vẫn còn trong thân mục, đồng thời làm sai phép đếm BẢY mệnh đề. Vì vẫn còn P1, packet **chặn land** theo `luat_dung_LAND`. P2 không được nâng hạng để giữ packet mở.

Tôi review đối tượng đóng băng tại exact SHA nêu trên. Checkout dùng chung ban đầu đúng SHA này nhưng đã bị một tiến trình khác chuyển sang nhánh `ops/cap-lease-tach-314` trong lúc review; từ thời điểm đó mọi phép đo đối tượng đều chạy trong clone cục bộ detached tại exact SHA, không dựa vào `HEAD` đang trôi.

## Preflight và phạm vi

- Repository: `ducthangho/tra-luat`; base và head khớp chỉ thị.
- Lease: revision 4, generation 1; lease ghi `spec_status: khong_co_dac_ta_rieng`, nên không có spec hash riêng để đối chiếu.
- Review Class: `sensitive`; cặp executor `claude` và reviewer `codex` là khác nền.
- Không gọi mạng, GitHub hay `git fetch`; không commit, push, merge, land hoặc LIVE.
- `git diff --name-only c35ae1c0a1104dbd6e65a321cda3b9f9441a408b 7d7354e14c540c3c2afd3f3a594ff2e432f6fd44` chỉ in `docs/GOI_AGENT_DA_NEN.md`.

## Đối chiếu năm finding vòng 8

| Finding vòng 8 | Phán quyết | Phép đo |
|---|---|---|
| `require-clean-vuot-pham-vi-quyen-ghi` [P1] | **VÁ HỜ** | Khối lệnh cũ đã bị gỡ, nhưng dòng 694–697 vẫn khẳng định control “có bó” việc chạy trên cây bẩn, “bó thật, đo được”. Đây vẫn là mệnh đề thực chứng ngoài phạm vi quyền ghi repository; sau khi gỡ phép đo, tệp không còn neo điều kiện hay output cho nó. |
| `require-clean-command-thieu-run-root` [P2] | **ĐÃ VÁ THẬT** | Tìm nguyên lệnh cũ bằng `rg -F` cho rc=1; khối lệnh hỏng không còn trong SHA được review. |
| `phep-dem-bo-sot-menh-de-proxy` [P2] | **VÁ SINH LỖI MỚI** | Proxy môi trường nay được gọi đích danh và được tính `chiều MỞ`; nhưng danh sách mới lại bỏ sót mệnh đề ở dòng 694–697, nên tổng BẢY và `chiều ĐÓNG ×1` vẫn sai. |
| `ba-control-chi-dung-cho-bang` [P2] | **ĐÃ VÁ THẬT** | Dòng 594 giới hạn rõ “BA control TRONG BẢNG”; bảng có đúng ba họ control. |
| `hai-menh-de-chua-chot-nhung-goi-duy-nhat` [P2] | **ĐÃ VÁ THẬT** | Dòng 638–641 tách riêng lý do chưa chốt của `codex -s workspace-write` và bộ ba clone/cây sạch/quyền ghi; không còn gọi hai lý do là “duy nhất”. |

## Kiểm kê độc lập các mệnh đề mang hạng

Tôi đếm theo nội dung mệnh đề, không grep tên nhãn:

| Vị trí | Mệnh đề | Hạng theo định nghĩa của chính mục |
|---|---|---|
| 678 | Narrow Bash chặn gọi GitHub CLI | `chiều ĐÓNG` |
| 679 | Bare Bash vẫn cho đường GitHub CLI | `chiều MỞ` |
| 680 | `codex -s workspace-write` và quyền ghi ngoài cây | `chưa xếp được` |
| 681 | Gỡ credential môi trường nhưng dry-run push vẫn rc=0 | `chiều MỞ` |
| 682 | Bỏ token nhưng dry-run push vẫn rc=0 | `chiều MỞ` |
| 684–686 | Proxy ambient credential không bó được đường thực thi | `chiều MỞ` |
| 687–692 | Clone sạch cộng `--require-clean` và quyền ghi repository | `chưa xếp được` |
| 694–697 | `--require-clean` bó thật, đo được việc chạy trên cây bẩn | về nghĩa là `chiều ĐÓNG`, nhưng văn bản không gắn nhãn |

Kết quả thực tế là **8 mệnh đề**: `chiều ĐÓNG ×2`, `chiều MỞ ×4`, `chưa xếp được ×2`, `máy phát hiện ×0`, `quan sát chưa rõ cơ chế ×0`. Con trỏ dòng 694–697 phải tính vì nó khẳng định hành vi thật và đã đo; câu “ngoài phạm vi” không biến một khẳng định thực chứng thành chỉ dẫn trung tính. Vì vậy cả “hai mệnh đề dưới bảng”, tổng BẢY và `chiều ĐÓNG ×1` đều sai.

## Chấm tiêu chí nghiệm thu

| Tiêu chí | Kết quả | Bằng chứng và lệnh |
|---|---|---|
| N1 | **KHÔNG ĐẠT** | Mục giới hạn đối tượng ở quyền ghi repository tại dòng 653–655, nhưng dòng 694–697 vẫn đưa vào thân mục một kết luận thực chứng về đối tượng khác: chạy trên cây bẩn. |
| N2 | **KHÔNG ĐẠT** | Kiểm kê ngữ nghĩa cho 8 mệnh đề, không phải 7; mệnh đề dòng 694–697 chưa có đúng một nhãn và về nghĩa làm số `chiều ĐÓNG` thành 2. |
| N3 | **ĐẠT** | Hai câu hỏi chưa có phép đo quyết định vẫn được ghi `chưa xếp được`; tệp không dùng chúng để khẳng định quyền ghi đã bị bó. |
| N4 | **KHÔNG ĐẠT** | Dòng 694 nói “bó thật, đo được” nhưng không có command, phiên bản, ngày hay output ngay cạnh; phép đo cây bẩn đã bị gỡ khỏi tệp. |
| N5 | **ĐẠT** | `bash /tmp/refscan.sh`, `stdout.log` không tái lập được, “tương quan có neo”, và ba bộ `78/5/10,8 M`, `85/10/12,8 M`, `45/1/3,7 M` đều còn nguyên. Hash SHA-256 đoạn dòng 553–577 ở parent và head cùng là `cd7599e6c4bb84d72e06996e7b02e6b982def4f0124b05d7e634f147cbc2363c`. |
| N6 | **ĐẠT** | `git diff --name-only c35ae1c0a1104dbd6e65a321cda3b9f9441a408b 7d7354e14c540c3c2afd3f3a594ff2e432f6fd44` in đúng một đường dẫn; `git diff --check` rc=0. |
| N7a | **ĐẠT** | `python3 .claude/dev/packet_loop.py doctrine-scan --root . --path docs/GOI_AGENT_DA_NEN.md` tại exact SHA cho rc=0 và `doctrine-scan: sạch — đã quét 8 tệp, 0 chỗ chép doctrine`. |
| N7b | **ĐẠT** | `git diff --numstat c35ae1c0a1104dbd6e65a321cda3b9f9441a408b 7d7354e14c540c3c2afd3f3a594ff2e432f6fd44 -- docs/GOI_AGENT_DA_NEN.md` cho `179  0`; 179 ≤ 200. |

Phép đối chiếu vòng hiện tại theo chỉ thị, `git diff d14ba2f3afd317b903224d1b06b4ddffb238dc5b 7d7354e14c540c3c2afd3f3a594ff2e432f6fd44 -- docs/GOI_AGENT_DA_NEN.md`, cho `22  22` và chỉ chạm tệp đích.

## Gate và phép đo bổ sung

| Trạng thái | Command | Kết quả dương |
|---|---|---|
| `passed` | `python3 .claude/dev/packet_loop_test.py` | rc=0; nền `257/257 đạt`, 66 đột biến, 78 lớp, 35 kiểm tra false-positive, 0 ngoại lệ AC18; `TỔNG: ĐẠT`. |
| `passed` | `python3 scripts/tl.py doc-claims-check --strict --json` | rc=0; `ok=true`, `files_scanned=105`, `flags=[]`, `layers_skipped={}`. |
| `passed` nhưng không bắt được lỗi nghĩa | `doctrine-scan` trên bản đột biến chỉ đổi mệnh đề dòng 694 thành nhãn tường minh `cơ chế đã xác minh — chiều ĐÓNG` | rc=0 và vẫn in đã quét 8 tệp. Điều này xác nhận gate hiện tại không kiểm phép đếm hay sự khớp nghĩa của nhãn. |
| `skipped` | Không có required local check nào bị skipped. | — |
| `not_run` | CI/GitHub, Windows, full release gate, LIVE. | Ngoài authority hoặc không có mạng; không được coi là pass. |

Đối với lời khai về chỗ-giữ-chỗ, regex thô ở base tìm 8 dòng vì tính cả một autolink URL; loại autolink đó thì có 7 chỗ-giữ-chỗ vận hành. Diff được review thêm 0 chỗ-giữ-chỗ ngoặc nhọn, phù hợp lời khai của executor. Tuy nhiên thay chỗ-giữ-chỗ bằng biến chưa khởi tạo tạo ra finding P2 bên dưới.

## Finding còn mở và finding mới

### `require-clean-vuot-pham-vi-quyen-ghi` — P1

**Trích dòng:** dòng 694–697: “`--require-clean` CÓ bó một thứ khác … và bó thật, đo được”, rồi mới nói đối tượng ấy ngoài phạm vi.

**Phép đo tái lập:** xuất các dòng 609–697 bằng `git show 7d7354e14c540c3c2afd3f3a594ff2e432f6fd44:docs/GOI_AGENT_DA_NEN.md`, liệt kê từng chủ thể–control–kết luận như bảng trên. Có 8 mệnh đề; mệnh đề cuối đáp ứng đúng định nghĩa `chiều ĐÓNG` ở dòng 613 nhưng không có trong danh sách dòng 619–623. Bản đột biến chỉ làm nhãn ngầm ấy thành tường minh vẫn qua `doctrine-scan` rc=0.

Đây là P1 vì tệp khai sai số mệnh đề và sai ý nghĩa nhãn, đồng thời giữ một kết luận thực chứng ngoài phạm vi đã tuyên bố; không phải lỗi trình bày P2.

**Remediation bốn phần:**

1. **Ở đâu:** sửa cùng nhau dòng 619–623 và 694–697.
2. **Sửa thế nào:** nếu giữ con trỏ, biến nó thành chỉ dẫn trung tính, chẳng hạn chỉ nói hạng của việc chạy trên cây bẩn không được xếp ở đây và phải được xử lý trong mục vòng đời với phép đo riêng; không khẳng định tại đây rằng control “bó thật” hay “đã đo”. Lựa chọn khác là chuyển toàn bộ mệnh đề, điều kiện và bằng chứng sang mục đúng phạm vi rồi đếm nó ở đó.
3. **Test nào:** thêm kiểm tra ngữ nghĩa dựa trên danh sách ID mệnh đề; bản đột biến tái đưa một kết luận thực chứng ngoài danh sách hoặc làm xuất hiện `chiều ĐÓNG` thứ hai phải fail. Gate hiện tại chưa làm việc này.
4. **Rủi ro:** xóa quá tay sẽ làm mất phân biệt hữu ích giữa quyền ghi repository và vòng đời lượt chạy; chuyển mà không gỡ bản cũ sẽ tạo hai mệnh đề trùng nhau.

### `prompt-shell-bien-chua-khoi-tao` — P2

**Trích dòng:** dòng 583–586 kết thúc lệnh bằng `--output-format json "$PROMPT"`, nhưng toàn tệp không có phép gán hay bước khởi tạo biến `PROMPT`; các lần xuất hiện trước là tên tệp `PROMPT.md`, không phải biến shell.

**Phép đo tái lập:** `rg -n '\bPROMPT\b|PROMPT=' docs/GOI_AGENT_DA_NEN.md` chỉ tìm tên tệp ở dòng 518, 530 và lần dùng biến ở dòng 586. Với môi trường đã bỏ biến, shell mặc định truyền một đối số rỗng; với `set -u`, shell dừng vì biến chưa được gán, rc=127 trong phép đo. Vì vậy khối chép được không còn mất đối số do transport, nhưng vẫn không bảo đảm có prompt.

Đây là P2: nó làm giảm tính chép-chạy của hướng dẫn, nhưng không làm sai doctrine hay phép đếm hạng.

**Remediation bốn phần:**

1. **Ở đâu:** ngay trước hoặc tại dòng 583–586.
2. **Sửa thế nào:** định nghĩa `PROMPT` ngay cạnh, hoặc ưu tiên cho CLI đọc stdin trực tiếp từ `PROMPT.md` để tránh biến môi trường ngầm.
3. **Test nào:** chạy nguyên khối khi `PROMPT` chưa có trong môi trường và xác nhận CLI nhận prompt khác rỗng; một bản đột biến bỏ bước khởi tạo hoặc nguồn stdin phải fail.
4. **Rủi ro:** nạp nội dung bằng command substitution có thể bỏ newline cuối và đụng giới hạn argv; stdin tránh hai rủi ro này.

## CHỖ KHÔNG ĐO ĐƯỢC

- `KHÔNG_ĐO_ĐƯỢC`: trạng thái GitHub, check từ xa, receipt ngoài cây và lease budget hiện thời, vì mạng đóng và chỉ thị cấm gọi GitHub.
- `KHÔNG_ĐO_ĐƯỢC`: spec hash riêng, vì lease tuyên bố không có đặc tả riêng và không cung cấp hash đó.
- `KHÔNG_ĐO_ĐƯỢC`: tái lập trực tiếp các số `78/5/10,8 M`, `85/10/12,8 M`, `45/1/3,7 M`, vì chính tệp nói `stdout.log` không được track; review này chỉ xác minh chúng được giữ nguyên.
- `KHÔNG_ĐO_ĐƯỢC`: quan sát gốc của mệnh đề cây bẩn ở dòng 694, vì command, ngày, phiên bản và output tương ứng đã bị gỡ khỏi tệp.
- `KHÔNG_ĐO_ĐƯỢC`: nội dung trực tiếp của Issue #334 và các measurement nằm ở packet đó, vì không dùng mạng và artifact đầy đủ không nằm trong exact tree được review.
- `KHÔNG_ĐO_ĐƯỢC`: con số bằng chữ “sáu chục dòng” như một giá trị chính xác, vì văn bản không xác định hai đầu đoạn để đếm; chỉ có thể hiểu là ước lượng.
- `KHÔNG_ĐO_ĐƯỢC`: các số lịch sử lấy từ scratch/log không track như chi phí xấp xỉ 39 USD và bộ `188 / 105911 / 31`; không có raw artifact trong exact tree để tái lập.

---

Verdict: `ops/reviews/doctrine-ranh-gioi-reviewer-review-9-codex-verdict.md`  
Finding: **P1 = 1 · P2 = 1**
