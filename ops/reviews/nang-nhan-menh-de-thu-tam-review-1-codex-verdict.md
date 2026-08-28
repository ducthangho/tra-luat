verdict: changes_requested
reviewed_sha: 7a79d9494fd9a656de85d53e77eefdfe26140cbd
P1: 2
P2: 0
finding_moi: 2

# Cross-review packet #364 — lượt 1

Provider/execution: `openai_codex` · Codex service · transport `machine`; reviewer độc lập, read-only đối với cây Executor `claude`.

## Kết luận

Tôi đo ra **(B)**, không phải (C): bằng chứng bốn tổ hợp đã xác minh một biến `network_access` đảo kết quả cho socket và URL; vì vậy có thể gắn `cơ chế đã xác minh — chiều MỞ` nếu mệnh đề thu hẹp tường minh về hai kênh ấy. `git` ở trạng thái đóng là `UNKNOWN`/`KHÔNG_ĐO_ĐƯỢC`, nên không được nhập vào lời khẳng định cơ chế; giới hạn loopback cũng cấm suy rộng thành egress hay “ranh giới mạng” nói chung. Phân bố đúng sau khi sửa đồng bộ sẽ là `1/5/2/0/0`.

Việc sửa dòng 647 nằm trong write set và là **nhất quán bắt buộc**, không phải lan phạm vi S1: nếu đoạn giải thích chính đổi căn cứ mà câu tóm tắt vẫn giữ lý do “hai cờ chưa tách”, tệp sẽ tự mâu thuẫn đúng hình dạng vòng 14 đã bắt. Nội dung sửa cụ thể vẫn sai về hạng, được chấm trong finding thứ nhất.

## Preflight và gate

```text
$ git rev-parse HEAD
7a79d9494fd9a656de85d53e77eefdfe26140cbd
$ git rev-parse HEAD^{tree}
ea9618e469a2ad4321912cdc9d80f68a38ed5266
$ git config --get core.autocrlf; git config --get core.eol; git config --get core.abbrev
false
lf
7
$ git merge-base --is-ancestor fe6152be2cb77e90b2624487e5b2403e4e4424b7 7a79d9494fd9a656de85d53e77eefdfe26140cbd; echo $?
0
$ git diff --numstat fe6152be 7a79d94
10      7       docs/GOI_AGENT_DA_NEN.md
$ git diff --name-status fe6152be 7a79d94
M       docs/GOI_AGENT_DA_NEN.md
$ python3 .claude/dev/packet_loop.py doctrine-scan --root .; echo $?
doctrine-scan: sạch — đã quét 7 tệp, 0 chỗ chép doctrine
0
$ git diff --check fe6152be 7a79d94; echo $?
0
```

Diff chạm đúng một đường trong write set; 10 dòng thêm ≤ trần 50. `doctrine-scan` xanh chỉ là gate hình thức, không phủ định hai lỗi ngữ nghĩa dưới đây.

## Đếm lại phân bố — đúng đơn vị mệnh đề

Lệnh đọc đã chạy cho head và base:

```text
$ nl -ba docs/GOI_AGENT_DA_NEN.md | sed -n '592,722p'
$ git show fe6152be:docs/GOI_AGENT_DA_NEN.md | nl -ba | sed -n '592,722p'
```

Đọc từng lần gắn nhãn, không dùng `grep -c`, cho cùng tám đơn vị ở cả hai cây:

1. luật hẹp `Bash(x:*)` — ĐÓNG;
2. `Bash` trần — MỞ;
3. `workspace-write` ghi ngoài cây — chưa xếp được;
4. xoá credential — MỞ;
5. token rác — MỞ;
6. proxy ambient — MỞ;
7. bộ ba clone rời/`--require-clean`/kiểm sạch — chưa xếp được;
8. mạng sandbox — chưa xếp được theo nhãn hiện tại.

Kết quả ghi nhận hiện trạng là `1/4/3/0/0` ở cả base và head, khớp dòng 625–626. Bất biến đếm còn đúng nhưng không chứng minh nhãn thứ tám đúng; chấm hợp đồng dòng 616–620 với bằng chứng mới dẫn tới finding 1.

## Finding 1

- `slug`: `giu-c-sai-do-dung-unknown-git-chan-pham-vi-da-xac-minh`
- `severity`: P1
- Mô tả: đoạn 682–690 dùng việc kênh `git` ở trạng thái đóng chưa phân loại được để kết luận toàn mệnh đề mạng không đạt `chiều MỞ`. Đây là lượng từ quá rộng. Tệp bằng chứng xác minh `network_access=true` **một mình** đảo socket và URL từ `POLICY_DENIED` sang `LOT`; đó là “biết vì sao nó KHÔNG chặn, và đã đo” cho phạm vi hai kênh ấy. `git=UNKNOWN` và cảnh báo loopback chỉ buộc thu hẹp phạm vi, không xoá bằng chứng dương đã có. Vì mệnh đề hiện không thu hẹp mà vẫn giữ nhãn/phân bố cũ, trạng thái bằng chứng của exact tree bị khai sai.
- Bằng chứng chạy được:

```text
$ rg -n -C 5 'KHÔNG_ĐO_ĐƯỢC|Loopback không phải egress|network_access=true' docs/MANG_SANDBOX_CODEX.md
44-| (b) | CÓ | không | 0 | 0 | 0 | `LOT` · `LOT` · `LOT` |
45-| (c) | không | CÓ | 1 | 1 | 1 | `POLICY_DENIED` · `POLICY_DENIED` · **`UNKNOWN`** |
48-`network_access=true` một mình đã đảo cả ba quan sát; `writable_roots` không đảo ô nào.
49:Loopback không phải egress: cờ này gate capability socket rộng hơn hai phép HTTPS ra ngoài,
50-nên kết quả chỉ xác minh phạm vi cờ cấu hình đã đo, không xác minh một ranh giới mạng.
54-- Executor lượt này không chạy lại ba cột/bốn tổ hợp: `codex sandbox` lồng dừng `rc=101` trước probe.
55-- **`git` ở (a)/(c) bị chặn bởi CHÍNH SÁCH SANDBOX hay bởi HẠ TẦNG PROXY của phiên chạy — CHƯA
56-  TÁCH ĐƯỢC.**
58-  `phan_loai_git()` fail-close đúng và trả `UNKNOWN`
```

Đối chiếu hợp đồng đã chạy bằng `nl -ba ... | sed -n '614,620p'`: dòng 617 định nghĩa MỞ là “biết vì sao nó KHÔNG chặn, và đã đo”. Socket/URL thỏa; chỉ `git` không thỏa.
- Vá ở đâu: mệnh đề dòng 675–676, đoạn `VÌ SAO` dòng 682–690, phân bố dòng 625–626 và câu tóm tắt dòng 647–648.
- Vá thế nào: chọn (B), nói ngay phạm vi xác minh chỉ gồm socket và URL trong đúng cấu hình/phiên đã đo; nói `git` vẫn `KHÔNG_ĐO_ĐƯỢC`, loopback không chứng minh egress; đổi nhãn thứ tám sang MỞ và phân bố sang `1/5/2/0/0`.
- Ca khóa: đọc lại tám đơn vị trên exact head và kiểm đồng thời nhãn, lời giải thích, câu tóm tắt, phân bố. Đột biến phải chết: dùng `git=UNKNOWN` để hạ luôn socket/url, hoặc nâng MỞ mà bỏ caveat `git`/loopback.
- Rủi ro bản vá: (A) sẽ suy rộng quá bằng chứng; chỉ đổi nhãn/phân bố mà không đổi hai đoạn văn sẽ tái tạo lỗi vòng 14.

## Finding 2

- `slug`: `workspace-write-con-khai-co-che-theo-packet-da-land`
- `severity`: P1
- Mô tả: quét theo ý phát hiện hàng `workspace-write` dòng 701 vẫn nói “cơ chế đã theo mục sandbox sang packet kia”. Sau khi #334 land, đây là lời khai trạng thái đã chết; hơn nữa `docs/MANG_SANDBOX_CODEX.md` đo mạng/socket/proxy, không đưa cơ chế cho việc `workspace-write` ghi tệp ngoài cây. Nhãn `chưa xếp được` có thể vẫn đúng, nhưng lý do đi kèm không còn là trạng thái bằng chứng người đọc exact tree kiểm được — đúng hình dạng vòng 14 cảnh báo.
- Bằng chứng chạy được:

```text
$ rg -n -i -C 3 'packet kia|xong nó|đo lại được|MANG-SANDBOX-CODEX' docs/GOI_AGENT_DA_NEN.md
697-| tầng | phép đo | kết quả |
701:| `codex -s workspace-write` | ghi tệp **ngoài** cây | **`rc=0`** — tệp ngoài cây bị ghi đè thật ⇒ **CHƯA XẾP ĐƯỢC**: đo được nó KHÔNG chặn, nhưng cơ chế đã theo mục sandbox sang packet kia |
```

Lệnh cùng lượt chỉ tìm thấy nội dung `MANG_SANDBOX-CODEX` về `network_access`, `writable_roots`, socket/url/git; không có phép đo cơ chế ghi tệp ngoài cây. Do đó câu “cơ chế đã theo” không được hiện vật đích chống lưng.
- Vá ở đâu: đúng ô `workspace-write` dòng 701.
- Vá thế nào: thay lời trỏ trạng thái bằng giới hạn bền của exact tree, chẳng hạn đã đo được ghi ngoài cây thành công nhưng chưa đo cơ chế vì sao control không chặn; không nói cơ chế “đã theo” packet #334.
- Ca khóa: chạy lại phép quét theo ý ở trên; hàng phải tự đủ và không phụ thuộc trạng thái packet. Đột biến phải chết: khôi phục “thuộc/đã theo packet kia” mà không có hiện vật cơ chế tương ứng.
- Rủi ro bản vá: không được tiện tay nâng hàng này sang MỞ; chưa có bằng chứng cơ chế cho đối tượng “ghi ngoài cây”.

## Chỗ không đo được

- `KHÔNG ĐO ĐƯỢC`: CI/check runs, PR head phía máy chủ, receipt và trạng thái GitHub hiện hành; phiên review chỉ đo clone độc lập được giao và không gọi mạng/fetch.
- `KHÔNG ĐO ĐƯỢC`: tái chạy probe Codex bốn tổ hợp trong chính phiên này; nested sandbox không được cấp làm acceptance và verdict chỉ dùng hiện vật đã land cùng lời tự khai giới hạn của nó.

