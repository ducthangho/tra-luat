verdict: approve
reviewed_sha: 2fa630ae3986ea1b8f9388a704e8f972d544963f
P1: 0
P2: 0
finding_moi: 0

# Cross-review packet #364 — lượt 2

Provider/execution: `openai_codex` · Codex service · transport `machine`; reviewer độc lập,
read-only đối với cây Executor `claude`. Executor và reviewer khác provider, nên đây là
cross-provider review trên exact head được giao.

## Kết luận

Hai P1 lượt 1 đều **ĐÃ ĐÓNG THẬT**. Nhãn thứ tám nay chọn đúng phương án (B): chỉ gắn
`cơ chế đã xác minh — chiều MỞ` cho socket và URL; `git` bị loại tường minh và vẫn giữ
`KHÔNG_ĐO_ĐƯỢC`; cảnh báo loopback không xác minh ranh giới mạng vẫn nguyên nghĩa. Hàng
`workspace-write` vẫn `chưa xếp được` và nay mô tả đúng trạng thái bằng chứng kiểm được.

Tôi mua ranh giới S5 hiện tại. Đoạn mới không chép probe, bảng hay các số 0/1 của
`docs/MANG_SANDBOX_CODEX.md`; nó ghi tại chỗ điều kiện/phạm vi tối thiểu cần để nhãn có nghĩa,
rồi trỏ sang hiện vật cho số đo đầy đủ. Nếu chỉ để một đường dẫn mà không ghi đối tượng, cấu hình
và chiều kết quả thì mệnh đề sẽ không còn là “mệnh đề kèm điều kiện đo” theo hợp đồng dòng
609–610. Câu “ĐIỀU KIỆN ĐO nằm NGAY ĐÂY” vì vậy đứng được; bằng chứng chi tiết vẫn ở packet kia.

Không có P1/P2 mới và không có finding riêng về phân bố.

## Preflight và gate

```text
$ git rev-parse HEAD
2fa630ae3986ea1b8f9388a704e8f972d544963f
$ git rev-parse HEAD^{tree}
34b15fa683a5fa5a31a67592eb12134b27ba0533
$ git branch --show-current
[rỗng — detached HEAD]
$ git config --get core.abbrev
7
$ git status --short
[rỗng]
$ git merge-base --is-ancestor fe6152be2cb77e90b2624487e5b2403e4e4424b7 2fa630ae3986ea1b8f9388a704e8f972d544963f; echo $?
0
$ git diff --name-status fe6152be 2fa630ae
M       docs/GOI_AGENT_DA_NEN.md
$ git diff --numstat fe6152be 2fa630ae
21      17      docs/GOI_AGENT_DA_NEN.md
$ git diff --numstat 7a79d94 2fa630ae
20      19      docs/GOI_AGENT_DA_NEN.md
$ python3 .claude/dev/packet_loop.py doctrine-scan --root .; echo $?
doctrine-scan: sạch — đã quét 7 tệp, 0 chỗ chép doctrine
0
$ git diff --check fe6152be 2fa630ae; echo $?
0
```

Diff chạm đúng một đường trong write set; số dòng thêm thật là **21**, dưới trần **50**.

## P1 lượt 1 #1 — đã đóng

Lệnh đã chạy:

```text
$ nl -ba docs/GOI_AGENT_DA_NEN.md | sed -n '670,691p'
674  **socket và url của sandbox: `network_access=true` MỘT MÌNH đảo cả hai từ `POLICY_DENIED` sang
675  `LOT`** ⇒ **cơ chế đã xác minh — chiều MỞ**, phạm vi CHỈ hai kênh này; hạng MỞ không phải ranh
676  giới (định nghĩa ở trên) — nó giải thích VÌ SAO không chặn, không tuyên bố có chặn. `git` KHÔNG
677  vào phạm vi nhãn này.
682  Bằng chứng MỞ cho SOCKET/URL riêng, đo lại SAU KHI packet `MANG-SANDBOX-CODEX` (#334) land: bốn
683  tổ hợp (a)-(d) ở `docs/MANG_SANDBOX_CODEX.md` giữ `writable_roots` cố định và chỉ đảo
684  `network_access` — một mình cờ đó lật socket/url từ `POLICY_DENIED` sang `LOT`, không phải tổ hợp
685  hai cờ như phép đo `git ls-remote` ở trên; trỏ sang tệp đó, không chép bảng về đây. `git` ở trạng
686  thái đóng mang lớp `KHÔNG_ĐO_ĐƯỢC` trong CHÍNH tệp ấy — phiên đo chưa tách được sandbox chặn khỏi
687  việc không nối tới proxy loopback của chính phiên đo — nên với `git`, VÌ SAO không chặn vẫn chưa
688  biết; giữ `KHÔNG_ĐO_ĐƯỢC`, không gộp vào nhãn MỞ trên. Loopback không phải egress: cờ này gate
689  capability socket rộng hơn hai phép HTTPS ra ngoài, nên MỞ chỉ xác minh phạm vi cờ cấu hình đã đo,
690  không xác minh một ranh giới mạng nói chung.
```

Phạm vi được thu hẹp tường minh; `git` bị loại rõ; caveat loopback còn nguyên. Không câu nào
đọc thành “sandbox có ranh giới mạng”: dòng 675–676 nói hạng MỞ **không phải ranh giới**, và
dòng 689–690 phủ định suy rộng ấy lần nữa.

Đối chiếu hiện vật nguồn đã chạy:

```text
$ rg -n -C 1 'network_access=true một mình|Loopback không phải egress|KHÔNG_ĐO_ĐƯỢC' docs/MANG_SANDBOX_CODEX.md
48:network_access=true một mình đã đảo cả ba quan sát; `writable_roots` không đảo ô nào.
49:Loopback không phải egress: cờ này gate capability socket rộng hơn hai phép HTTPS ra ngoài,
50-nên kết quả chỉ xác minh phạm vi cờ cấu hình đã đo, không xác minh một ranh giới mạng.
52:## KHÔNG_ĐO_ĐƯỢC
```

## P1 lượt 1 #2 — đã đóng

Lệnh đã chạy:

```text
$ nl -ba docs/GOI_AGENT_DA_NEN.md | sed -n '698,704p'
698  | tầng | phép đo | kết quả |
699  |---|---|---|
700  | `--allowedTools`, luật hẹp `Bash(x:*)` | gặp lệnh ghép | không khớp gì ⇒ **cơ chế đã xác minh — chiều ĐÓNG**, nhưng CHỈ đóng HÌNH DẠNG lệnh ghép (cơ chế khớp tiền tố, năm lệnh `TỪ CHỐI` đo ở mục trên); nó KHÔNG bó quyền ghi |
701  | `--allowedTools`, `Bash` trần | cùng lệnh ghép | khớp mọi thứ ⇒ **cơ chế đã xác minh — chiều MỞ** |
702  | `codex -s workspace-write` | ghi tệp **ngoài** cây | **`rc=0`** — tệp ngoài cây bị ghi đè thật ⇒ **CHƯA XẾP ĐƯỢC**: đo được nó KHÔNG chặn, nhưng chưa ai đo CƠ CHẾ vì sao — `docs/MANG_SANDBOX_CODEX.md` (#334) chỉ đo mạng/socket/proxy, không đo đối tượng ghi-ngoài-cây này |
703  | xoá `GITHUB_PAT` `GH_TOKEN` `GITHUB_TOKEN` `GIT_CONFIG_*` khỏi env | `git push --dry-run` lên GitHub | **`rc=0`** — vẫn đẩy được ⇒ **cơ chế đã xác minh — chiều MỞ** |
704  | nhét **token RÁC** vào URL đẩy | cùng lệnh | **`rc=0`** ⇒ **cơ chế đã xác minh — chiều MỞ** |
```

Câu trạng thái chết “cơ chế đã theo mục sandbox sang packet kia” đã mất. Dòng 702 nói đúng bằng
chứng dương (`rc=0`, ghi đè thật), đúng phần chưa đo (cơ chế vì sao không chặn), và không nâng hạng.

## Đếm lại tám mệnh đề và quét theo ý

Đơn vị là lần gắn nhãn cho một mệnh đề, không phải số lần chuỗi xuất hiện:

1. luật hẹp `Bash(x:*)` — ĐÓNG;
2. `Bash` trần — MỞ;
3. `workspace-write` ghi ngoài cây — chưa xếp được;
4. xoá credential — MỞ;
5. token rác — MỞ;
6. proxy ambient — MỞ;
7. bộ ba clone rời/`--require-clean`/kiểm sạch đối với quyền ghi — chưa xếp được;
8. socket và URL của sandbox — MỞ.

Kết quả: **`1/5/2/0/0`**, khớp dòng 625–626.

Các neo đọc đã chạy:

```text
$ nl -ba docs/GOI_AGENT_DA_NEN.md | sed -n '622,648p;670,714p'
625  sandbox ở đoạn khai chỗ tách. Đếm ra: `chiều ĐÓNG` ×1 · `chiều MỞ` ×5 · `chưa xếp được` ×2 ·
626  `máy phát hiện` ×0 · `quan sát chưa rõ cơ chế` ×0.
641  hai ô `chưa xếp được` là hai mệnh đề chưa chốt.
643  `máy phát hiện` rỗng cũng là kết luận, không phải sót: bộ ba từng bị gọi là máy phát hiện hoá ra
644  KHÔNG tố cáo sự kiện đang bàn. `quan sát chưa rõ cơ chế` rỗng vì lý do riêng của TỪNG mệnh đề chưa
645  chốt, không phải một lý do chung: hàng `workspace-write` không mang phiên bản lẫn số lần lặp, mà
646  hạng ấy đòi lặp lại được; mệnh đề bộ-ba-với-quyền-ghi thì chưa ai đo CƠ CHẾ.
674  **socket và url của sandbox: `network_access=true` MỘT MÌNH đảo cả hai từ `POLICY_DENIED` sang
675  `LOT`** ⇒ **cơ chế đã xác minh — chiều MỞ** ...
700  | `--allowedTools`, luật hẹp `Bash(x:*)` | ... **cơ chế đã xác minh — chiều ĐÓNG** ... |
701  | `--allowedTools`, `Bash` trần | ... **cơ chế đã xác minh — chiều MỞ** |
702  | `codex -s workspace-write` | ... **CHƯA XẾP ĐƯỢC** ... |
703  | xoá ... credential ... | ... **cơ chế đã xác minh — chiều MỞ** |
704  | nhét **token RÁC** ... | ... **cơ chế đã xác minh — chiều MỞ** |
708  container**. Đây là **cơ chế đã xác minh — chiều MỞ**: ta biết vì sao nó không chặn.
713  bộ ba ấy là **CHƯA XẾP ĐƯỢC** ...
```

Lệnh quét số lượng/hạng trên toàn tệp đã chạy:

```text
$ rg -n -i '([0-9]+|một|hai|ba|bốn|năm|sáu|bảy|tám) (ô|hạng|mệnh đề)|×[0-9]|rỗng vì|mệnh đề chưa|phân bố|đếm ra|số hạng|hạng đã dùng' docs/GOI_AGENT_DA_NEN.md
592:#### NĂM HẠNG bằng chứng — đọc mục dưới bằng từ vựng này, kẻo lại viết ra những câu chỏi nhau
595:điều phối, thành NĂM mệnh đề TRONG BẢNG (`--allowedTools` và cặp credential mỗi cái được đo ở
596:hai cấu hình); văn xuôi dưới bảng mang thêm BA mệnh đề nữa; phép đếm đầy đủ nằm ngay sau bảng năm hạng.
600:hai pha. Cái Ở LẠI là ĐÚNG MỘT mệnh đề về mạng sandbox: nó nằm TRONG phạm vi từ vựng này, mang
622:**Mục này dùng BA trên năm hạng — nhưng KHÔNG phải ba hạng mà bản trước tưởng.** Đơn vị đếm là
623:**lần GẮN NHÃN cho một mệnh đề**, không phải số lần xuất hiện của cụm chữ. TÁM mệnh đề mang nhãn:
625:sandbox ở đoạn khai chỗ tách. Đếm ra: `chiều ĐÓNG` ×1 · `chiều MỞ` ×5 · `chưa xếp được` ×2 ·
626:`máy phát hiện` ×0 · `quan sát chưa rõ cơ chế` ×0.
633:Ghi lại vì bài học đắt hơn con số: **quan hệ tổng còn đúng không chứng minh các số hạng còn đúng**.
634:Số hạng-được-dùng vẫn là ba trước và sau khi sửa, nên mọi phép kiểm đếm-theo-quan-hệ đều xanh
641:hai ô `chưa xếp được` là hai mệnh đề chưa chốt.
644:KHÔNG tố cáo sự kiện đang bàn. `quan sát chưa rõ cơ chế` rỗng vì lý do riêng của TỪNG mệnh đề chưa
648:chung**; đừng đọc số hàng thành số hạng đã dùng.
659:#### Ba CONTROL thường bị coi là hàng rào, NĂM mệnh đề trong bảng — đo Ở VỎ PHIÊN ĐIỀU PHỐI: CHƯA đo được control nào bó được QUYỀN GHI VÀO KHO (24-08-2026)
```

Không còn “chỗ thứ sáu”: `TÁM`, `NĂM + BA`, phân bố `1/5/2/0/0`, “hai ô”, và hai lý do riêng
cho hai mệnh đề chưa chốt đều nhất quán.

## Không đo được

- `KHÔNG ĐO ĐƯỢC`: CI/check runs, PR head phía máy chủ, receipt và trạng thái GitHub hiện hành;
  phiên này chỉ đo clone detached được giao, không gọi mạng hoặc fetch.
- `KHÔNG ĐO ĐƯỢC`: tái chạy probe bốn tổ hợp trong phiên reviewer; acceptance yêu cầu đọc hiện vật
  đã land, và không cấp nested execution để tái đo runtime đó.

