verdict: changes_requested
reviewed_sha: fa9a505d0926a56603cabfb998bd4832084ed68f
reviewed_tree: 38eb08ad09d43bca0e57ac098dba19e486c8c61f
packet: "#318 DOCTRINE-RANH-GIOI-REVIEWER"
review_round: 12
provider: openai_codex
execution_surface: codex_service
transport: machine
independent_from_executor_session: true

# Cross-review vòng 12

## Kết luận

`changes_requested`, với **[P1] 1 · [P2] 0**. Theo `luat_dung_LAND`, [P1] còn lại chặn land.

HEAD local detached khớp exact SHA được giao. Diff từ base
`c35ae1c0a1104dbd6e65a321cda3b9f9441a408b` chỉ chạm
`docs/GOI_AGENT_DA_NEN.md`. Cổng N7a xanh và N7b còn biên 16 dòng. Tuy nhiên bản vá vòng 11 làm
câu khai phạm vi tự mâu thuẫn với chính mệnh đề thứ tám, đồng thời chưa đặt điều kiện đo ngay cạnh
mệnh đề đó. Hai biểu hiện này thuộc cùng stable finding, không được đếm thành hai finding.

## ĐỐI CHIẾU LƯỢT TRƯỚC

### `menh-de-sandbox-mo-coi-khong-nhan` [P1] — **VÁ SINH LỖI MỚI**

Phần thiếu nhãn đã được vá thật về mặt hiện diện: dòng 669–673 gắn nhãn
`cơ chế đã xác minh — chiều MỞ`, và dòng 619–625 đưa mệnh đề vào phép đếm. Nhãn này không chỉ là
suy luận từ tài liệu cấu hình: cùng tệp đã ghi phép A/B ở dòng 328–339 — mặc định `ls-remote` lỗi
kết nối; khi bật cấu hình mạng của sandbox thì `lsremote_rc=0`. Vì vậy, xét riêng nghĩa của nhãn,
`chiều MỞ` đứng được cho câu hỏi “mạng đóng có phải một ranh giới bất biến không”.

Nhưng bản vá sinh lỗi phạm vi mới và không đóng phần N4 của finding cũ:

- Dòng 594–596 vẫn giới hạn mục vào năm mệnh đề trong bảng cộng **hai** mệnh đề văn xuôi; dòng
  597–601 còn nói từ vựng mạng/sandbox áp dụng ở #334, “không phải ở đây”. Ngược lại, dòng
  619–625 và 669–673 lại gắn nhãn và đếm mệnh đề mạng/sandbox **ở đây**. Câu đầu mục vì thế sai
  phạm vi thân nó (N1).
- Ngay cạnh mệnh đề ở dòng 669–673 chỉ có “cờ lật được” và con trỏ chung sang packet khác; không có
  điều kiện đo cụ thể, phiên bản, lệnh/kết quả A/B, cũng không trỏ tới phép đo local ở dòng 328–339.
  Con trỏ “bằng chứng nằm ở packet kia” không thay điều kiện đo ngay cạnh mà N4 yêu cầu. Nội dung
  #334 không có trong clone này để reviewer kiểm độc lập.

Phép đo tái lập được:

```text
nl -ba docs/GOI_AGENT_DA_NEN.md | sed -n '328,345p;592,625p;655,696p'
```

Kết quả cần đối chiếu là các cặp dòng `594–601 ↔ 619–625` và `669–673 ↔ 328–339` nêu trên.

Gợi ý vá bắt buộc:

1. **Vá ở đâu:** sửa cùng một cụm tại dòng 594–625 và 669–673, vì đây là nơi định nghĩa phạm vi,
   đơn vị đếm, nhãn và neo đo của đúng mệnh đề; sửa chỗ khác sẽ để hai nguồn sự thật tiếp tục lệch.
2. **Vá thế nào:** làm câu phạm vi thừa nhận rõ một mệnh đề mạng/sandbox còn lại trong tệp; đặt ngay
   cạnh mệnh đề một điều kiện đo tối thiểu và kết quả A/B đã có ở dòng 328–339. Nếu không muốn neo
   phép đo đó tại đây thì phải hạ mệnh đề về `chưa xếp được` và tính lại phân bố; không được vừa gọi
   là `cơ chế đã xác minh` vừa chỉ sang bằng chứng reviewer không có.
3. **Ca test khóa lỗi:** lập sổ bằng tay theo đơn vị “mệnh đề + điều kiện đo”; kiểm tập được câu phạm
   vi khai đúng bằng tập tám đơn vị thực tế, mỗi đơn vị có đúng một nhãn và điều kiện đo cạnh nó;
   sau đó chạy lại N7a và N7b. Một đột biến đổi “ba mệnh đề văn xuôi” về “hai”, hoặc bỏ điều kiện
   A/B cạnh mệnh đề thứ tám, phải làm ca kiểm ngữ nghĩa đỏ.
4. **Bản vá có thể đẻ ra gì:** chép cả bảng động của #334 về sẽ làm hỏng lát cắt và tạo số liệu dễ
   trôi; đổi nhãn mà quên phân bố sẽ làm tổng 8 vẫn đúng nhưng các số hạng sai; thêm một con trỏ mới
   mà không sửa câu “neo duy nhất” sẽ tạo hai neo cạnh tranh.

## Phép đếm theo từng đơn vị

Không dùng grep cụm nhãn. Tám mệnh đề được liệt kê như sau:

| # | mệnh đề kèm điều kiện đo | nhãn |
|---:|---|---|
| 1 | `--allowedTools` luật hẹp, gặp lệnh ghép | `chiều ĐÓNG` |
| 2 | `--allowedTools` với `Bash` trần, cùng lệnh ghép | `chiều MỞ` |
| 3 | `codex -s workspace-write`, phép ghi được mô tả trong hàng bảng | `chưa xếp được` |
| 4 | bỏ credential client khỏi môi trường, chạy phép đẩy khô | `chiều MỞ` |
| 5 | đưa credential client không hợp lệ vào URL, cùng phép đẩy khô | `chiều MỞ` |
| 6 | cơ chế proxy ambient suy ra từ hai phép đối chứng credential, dòng cuối là phép quyết định | `chiều MỞ` |
| 7 | bộ ba clone rời + `--require-clean` + kiểm cây sạch, xét quyền ghi/push | `chưa xếp được` |
| 8 | mạng sandbox đóng mặc định nhưng cấu hình có thể mở | `chiều MỞ` |

Tổng là **8**. Phân bố `chiều ĐÓNG` ×1 + `chiều MỞ` ×5 + `chưa xếp được` ×2 +
`máy phát hiện` ×0 + `quan sát chưa rõ cơ chế` ×0 = **8**. Không có đơn vị nào bị tính hai lần:
hai hàng credential là hai mệnh đề dưới hai điều kiện đo; mệnh đề proxy ambient là kết luận về cơ
chế, không phải một trong hai quan sát đầu vào.

## Bảng chấm nghiệm thu

| Tiêu chí | Kết quả | Lệnh/phép đo đã chạy và bằng chứng |
|---|---|---|
| N1 | **KHÔNG ĐẠT** — cùng finding [P1] | `nl -ba docs/GOI_AGENT_DA_NEN.md \| sed -n '592,625p;655,673p'`: dòng 594–601 loại mạng/sandbox khỏi phạm vi tại đây, còn dòng 619–625 và 669–673 lại đưa nó vào phạm vi, nhãn và phép đếm. |
| N2 | **ĐẠT** | Liệt kê tám đơn vị ở bảng trên: mỗi đơn vị có đúng một nhãn; phân bố 1/5/2/0/0. Nghĩa nhãn của đơn vị 8 được kiểm đối chiếu với phép A/B local ở dòng 328–339, không chỉ dựa vào câu tự khai. |
| N3 | **ĐẠT** | Đọc dòng 633–647 và 669–673: mệnh đề thứ tám kết luận một mặc định không phải ranh giới; nó không dựa vào một control chưa đo để khẳng định có bảo vệ. |
| N4 | **KHÔNG ĐẠT** — cùng finding [P1] | `nl -ba docs/GOI_AGENT_DA_NEN.md \| sed -n '328,345p;655,673p'`: điều kiện A/B nằm cách mệnh đề hơn 300 dòng; ngay cạnh chỉ có lời “cờ lật được” và con trỏ #334. |
| N5 | **ĐẠT** | `git show 12e0315a439b1e73bde57b09152bc077e04d7ee5:docs/GOI_AGENT_DA_NEN.md \| rg -n -C 2 'tương quan có neo\|stdout\\.log\|bash /tmp/refscan\\.sh\|10,8 M\|12,8 M\|3,7 M'`; bản hiện tại giữ nguyên ba P2 cũ và ba bộ số `78/5/10,8 M`, `85/10/12,8 M`, `45/1/3,7 M`. Diff vòng 11 không chạm các dòng này. |
| N6 | **ĐẠT** | `git diff --name-only c35ae1c0a1104dbd6e65a321cda3b9f9441a408b..HEAD` in đúng `docs/GOI_AGENT_DA_NEN.md`. |
| N7a | **ĐẠT** | `python3 .claude/dev/packet_loop.py doctrine-scan --root . --path docs/GOI_AGENT_DA_NEN.md` → rc=0; `doctrine-scan: sạch — đã quét 8 tệp, 0 chỗ chép doctrine`. |
| N7b | **ĐẠT** | `git diff --numstat c35ae1c0a1104dbd6e65a321cda3b9f9441a408b -- docs/GOI_AGENT_DA_NEN.md` → `184  0`; trần 200, còn biên **16 dòng thêm**. Ngân sách probe không được cộng vào số này. |

## Finding mới

Không có finding độc lập mới. Hồi quy phạm vi N1 do bản vá vòng 11 sinh ra được giữ dưới stable ID
`menh-de-sandbox-mo-coi-khong-nhan`; tách slug mới sẽ đếm đôi cùng một gốc lỗi. Không có [P2] mới.

## CHỖ KHÔNG ĐO ĐƯỢC

- `KHÔNG_ĐO_ĐƯỢC` nội dung phép đo/lease của Issue #334: clone không chứa artifact mang tên
  `MANG-SANDBOX-CODEX` hoặc `334`, và điều kiện vận hành cấm mạng/GitHub. Vì vậy verdict chỉ dùng
  phép A/B đã có trong chính tệp; không nhận lời “bằng chứng ở packet kia” làm evidence độc lập.
- `KHÔNG_ĐO_ĐƯỢC` ba `stdout.log` lịch sử: chính tệp khai chúng ở scratchpad không được Git theo
  dõi. Chỉ đo được rằng lời khai không-tái-lập, “tương quan có neo”, ví dụ thứ sáu và ba bộ số được
  giữ nguyên qua diff vòng 11; không tái lập được số liệu thô.
- `KHÔNG_ĐO_ĐƯỢC` Packet revision, generation, spec hash, lease hiện hành và GitHub PR head trực
  tiếp: các durable fact ấy không có trong clone và mạng bị cấm. Local đo được HEAD detached đúng
  `fa9a505d0926a56603cabfb998bd4832084ed68f`; review dùng exact SHA, base, write set và acceptance
  được người giữ kho cấp trong chỉ thị vòng 12.

---

Đường dẫn verdict: `ops/reviews/doctrine-ranh-gioi-reviewer-review-12-codex-verdict.md`

Số finding: **[P1] 1 · [P2] 0**
