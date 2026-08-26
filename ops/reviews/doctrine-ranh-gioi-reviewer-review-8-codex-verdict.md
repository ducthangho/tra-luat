# Cross-review vòng 8 — packet #318 `DOCTRINE-RANH-GIOI-REVIEWER`

```yaml
verdict: changes_requested
reviewed_sha: d14ba2f3afd317b903224d1b06b4ddffb238dc5b
reviewed_tree: 70bea4939b8ccb0c013f900841e29e0651f497b0
base_sha: c35ae1c0a1104dbd6e65a321cda3b9f9441a408b
reviewer: codex
provider: openai_codex
execution_surface: codex_service
transport: machine
executor: claude
review_axes:
  - spec
  - standards_security
```

## Kết luận

`changes_requested`. Năm finding vòng 7 đã được vá thật; finding
`may-phat-hien-khong-phat-hien-push` được sửa đúng ở lõi nhưng bản vá sinh lỗi mới.
Còn **1 P1 và 4 P2**.

P1 là lỗi phạm vi: mục tự khai đối tượng đo là **quyền ghi vào kho**, nhưng đưa việc
`--require-clean` chặn một lượt chạy trên cây bẩn — một đối tượng khác — vào chính thân
mục và phép đếm. Nhãn `cơ chế đã xác minh — chiều ĐÓNG` tự nó **đúng nghĩa** cho đối
tượng cây bẩn; lỗi là đối tượng đó không thuộc phạm vi mục hiện hành.

## Preflight và giới hạn vai trò

- `git rev-parse HEAD` → `d14ba2f3afd317b903224d1b06b4ddffb238dc5b`.
- `git rev-parse HEAD^{tree}` → `70bea4939b8ccb0c013f900841e29e0651f497b0`.
- Branch: `claude/doctrine-ranh-gioi-reviewer-exec-1`; `core.abbrev=7`.
- Worktree sạch trước review và sạch lại sau hai phép đo bẩn; reviewer không sửa tệp
  packet, không chạm `.git`, không commit, không push, không gọi mạng.
- Hồ sơ lease local đọc được ghi `revision: 4`, `generation: 1`, nhưng trường
  `reviewed_sha_required` vẫn là head vòng 7 `ed50b734...` và không có `spec_hash`.
  Chỉ thị trực tiếp vòng 8 đã cho exact head/base/write set/acceptance và được dùng làm
  chỉ thị điều phối hiện hành; trạng thái durable trên GitHub vẫn là
  `KHÔNG_ĐO_ĐƯỢC` vì mạng bị đóng.

## ĐỐI CHIẾU SÁU FINDING VÒNG 7

| finding vòng 7 | phán quyết vòng 8 | bằng chứng tự đo |
|---|---|---|
| `nam-hang-khong-tao-phan-hoach` [P1] | **ĐÃ VÁ THẬT** | Dòng 633 hạ kết luận thành “chưa đo được control nào”; tiêu đề dòng 651 cũng dùng `CHƯA đo được`. Hai lượng từ tuyệt đối cũ đã biến mất. |
| `allowedtools-hep-bi-xep-sai-hang` [P1] | **ĐÃ VÁ THẬT** | Dòng 676 gắn `cơ chế đã xác minh — chiều ĐÓNG` và đặt ngay trong hàng điều kiện “CHỈ đóng HÌNH DẠNG lệnh ghép, KHÔNG bó quyền ghi”. Năm lệnh bị từ chối nằm ở dòng 545–550; định nghĩa hạng ở dòng 613. |
| `may-phat-hien-khong-phat-hien-push` [P1] | **VÁ SINH LỖI MỚI** | Dòng 690–695 đã tách đúng hai đối tượng: quyền ghi/push là `CHƯA XẾP ĐƯỢC`, chạy trên cây bẩn là `chiều ĐÓNG`. Nhưng đối tượng thứ hai vượt phạm vi dòng 651–654, và lệnh đo in ở dòng 693 thiếu `--run-root`, nên chạy nguyên dạng cho `rc=2`, không phải `0/6`. |
| `bon-control-thuc-ra-ba` [P2] | **ĐÃ VÁ THẬT** | Riêng bảng dòng 674–680 có ba họ control: `--allowedTools` (2 cấu hình), `workspace-write` (1), credential/proxy (2). Dòng 651 và 670 đã đổi `Bốn` thành `Ba`, dòng 671–672 nêu đúng luật nhóm. Lời khai rộng hơn “ba control của cả mục” là finding mới riêng bên dưới. |
| `ba-cau-nhung-liet-ke-bon` [P2] | **ĐÃ VÁ THẬT** | Tiêu đề dòng 592 bỏ số, nay nói “những câu”; dòng 603–605 vẫn liệt kê và gọi đúng bốn câu. |
| `packet-rieng-khong-co-neo` [P2] | **ĐÃ VÁ THẬT** | Dòng 597–599 đặt một neo duy nhất `MANG-SANDBOX-CODEX`, Issue #334; các con trỏ `packet kia` phía dưới đều hướng ngược về neo này. Số/slug khớp hồ sơ lease local; nội dung/trạng thái Issue không đo được khi offline. |

## Phép đo mới của `--require-clean`

### Chạy nguyên văn như tài liệu

Trên cả cây sạch lẫn cây bẩn:

```text
python3 .claude/dev/launcher.py run --require-clean -- true
rc=2
launcher.py run: error: the following arguments are required: --run-root
```

Vì parser dừng trước chốt sạch/bẩn, lệnh được in trong doctrine không tái lập được hai
kết quả mà nó gán cho lệnh ấy.

### Bổ sung tham số bắt buộc để đo đúng hành vi

Cây sạch:

```text
python3 .claude/dev/launcher.py run --workspace . --require-clean \
  --run-root /tmp/tra-luat-review8-clean.<tam> -- true
rc=0
run.json: worktree_sach=true, so_muc_ban=0, trang_thai=xong, ma_thoat=0
```

Cây bẩn bằng đúng một tệp untracked không bị ignore:

```text
?? review8-require-clean-dirty.txt
python3 .claude/dev/launcher.py run --workspace . --require-clean \
  --run-root /tmp/tra-luat-review8-dirty.<tam> -- true
rc=6
CHAN [6]: worktree KHONG sach (1 muc) - tu choi chay mo ho
```

Tệp rác được xóa ngay sau phép đo; HEAD/tree không đổi và `git status --short` trở lại
rỗng. Hai ca có sẵn cũng qua:

```text
launcher_test.py --lap-ca t10_worktree --lan 1  -> 1/1 qua, rc=0
launcher_test.py --lap-ca t12_tep --lan 1       -> 1/1 qua, rc=0
```

Mã tại `.claude/dev/launcher.py:1217–1224` chạy
`git status --porcelain=v1 --untracked-files=all` và ném mã 6 trước khi sinh tiến trình
khi `--require-clean` bật. Vì vậy kết luận ngữ nghĩa là:

- với **việc khởi chạy trên cây bẩn**, nhãn `chiều ĐÓNG` đúng định nghĩa;
- đây không phải `máy phát hiện`, vì nó chặn trước khi lệnh con chạy;
- nó không chứng minh bó **quyền ghi vào kho**, và đối tượng khởi chạy không nằm trong
  phạm vi hiện được dòng 651–654 khai.

## Kiểm phép đếm và luật đếm

Năm hàng bảng tự chúng cho:

| dòng | mệnh đề | nhãn |
|---:|---|---|
| 676 | luật hẹp gặp lệnh ghép | `chiều ĐÓNG` |
| 677 | `Bash` trần gặp cùng lệnh | `chiều MỞ` |
| 678 | `workspace-write` ghi ngoài cây | `chưa xếp được` |
| 679 | bỏ credential client | `chiều MỞ` |
| 680 | token client rác | `chiều MỞ` |

Hai bullet dòng 690–695 thêm `chưa xếp được` ×1 và `chiều ĐÓNG` ×1. Nếu chỉ đếm
đúng bảy vị trí mà đoạn đếm tự chỉ định, kết quả executor khai là `ĐÓNG ×2 · MỞ ×3 ·
chưa xếp ×2`.

Nhưng luật viết là **lần gắn nhãn cho một mệnh đề**, không phải “năm hàng cộng đúng hai
bullet”. Dòng 682–684 còn một mệnh đề hiện hành khác: proxy bỏ qua credential client,
tự chèn credential ambient, rồi gắn chính mệnh đề cơ chế ấy nhãn đầy đủ
`cơ chế đã xác minh — chiều MỞ`. Nó không đồng nhất với từng quan sát có điều kiện ở
dòng 679 hoặc 680; nó là kết luận cơ chế tổng hợp từ hai quan sát. Áp luật như viết ra
cho kết quả tối thiểu **8** mệnh đề: `ĐÓNG ×2 · MỞ ×4 · chưa xếp ×2`; hai hạng còn lại
vẫn ×0. Do đó phép đếm “đầy đủ” hiện không tự nhất quán.

Phép đột biến an toàn trên clone rời đổi riêng nhãn cây-bẩn từ `chiều ĐÓNG` sang
`máy phát hiện`; `doctrine-scan` vẫn `rc=0`, 8 tệp. Cổng chỉ canh hình thức, không phải
oracle cho nghĩa hoặc phép đếm này.

## Rà con số bằng chữ, con trỏ vị trí và neo

| lời khai/con trỏ | kết quả |
|---|---|
| `BA control` trong bảng, `NĂM mệnh đề TRONG BẢNG` | đúng cho bảng: 3 họ control, 5 hàng; không đúng nếu `BA` được đọc là tổng control của cả mục, vì prose còn `--require-clean` và bộ ba clone/cleanliness. |
| `văn xuôi dưới bảng ... hai mệnh đề` | đúng nếu nói riêng hai bullet dòng 690–695; không đủ cho luật “mọi lần gắn nhãn”, vì dòng 684 còn một mệnh đề cơ chế có nhãn. |
| `tổng BẢY`, `ĐÓNG ×2`, `MỞ ×3`, `chưa xếp ×2` | sai theo luật đã viết; tối thiểu 8 và `MỞ ×4`. |
| `hai ô chưa xếp ... hai mệnh đề chưa chốt` | đúng: dòng 678 và 690. |
| `mệnh đề chưa chốt duy nhất` | sai: chỏi với chính “hai mệnh đề chưa chốt” bốn dòng phía trên. |
| `mục dưới` ở dòng 592/603 | đúng hướng, đích là mục bắt đầu dòng 651. |
| `ngay sau bảng năm hạng` ở dòng 596 | đúng hướng, đoạn đếm bắt đầu dòng 619. |
| `phía dưới` ở dòng 598 | đúng hướng; các con trỏ `packet kia` nằm tại 659, 667, 678. |
| `mục trên` ở dòng 676 | đúng hướng, đích là phép đo năm lệnh tại 545–550. |
| `nằm ngay trên` ở dòng 687 | đúng hướng, đích là quan sát push/clean tại 669–670. |
| bảng gốc `ba hàng` | đúng: blob `48cf331` có ba data-row định nghĩa. |
| `bốn vòng`, `tám finding` mạng/sandbox | khớp hồ sơ verdict local vòng 1–4: 3 + 2 + 1 + 2 = 8. |
| `sáu chục dòng` | mô tả xấp xỉ lịch sử; không có cặp anchor đầu/cuối nên không thể dùng làm số chính xác. |

Không thấy mệnh đề mồ côi mới sau lát cắt ngoài các lỗi phạm vi/đếm đã nêu. Các nhãn
hiện hành đều có neo quan sát hoặc neo thiếu-cơ-chế trong tệp; riêng trạng thái remote
của các neo GitHub không được suy từ bản local.

## BẢNG CHẤM N1–N6, N7a, N7b

| tiêu chí | kết quả | lệnh/phép đo và bằng chứng dương |
|---|---|---|
| N1 | **KHÔNG ĐẠT** | `nl -ba docs/GOI_AGENT_DA_NEN.md \| sed -n '651,695p'`: dòng 653–654 khai đối tượng là quyền ghi vào kho; dòng 692–695 thêm đối tượng chạy trên cây bẩn. Câu đầu không còn phủ đúng thân mục. |
| N2 | **KHÔNG ĐẠT** | Đối chiếu dòng 613–617 với 676–695 cho thấy từng nhãn chính đúng nghĩa, nhưng phép đếm tự xưng đầy đủ bỏ mệnh đề có nhãn ở 682–684: luật cho tối thiểu 8, không phải 7. Semantic mutant đổi nhãn cây-bẩn vẫn qua `doctrine-scan rc=0`, nên gate hình thức không chữa được lỗi này. |
| N3 | **ĐẠT** | Dòng 633 dùng lượng từ “chưa đo được”; dòng 690–691 giữ quyền ghi/push ở `chưa xếp được`; không nâng phần chưa biết cơ chế thành khẳng định không-control tuyệt đối. |
| N4 | **KHÔNG ĐẠT** | Điều kiện/ngày/kết quả nằm cạnh quan sát, nhưng lệnh được ghi thiếu tham số parser bắt buộc. Chạy nguyên văn trên cả cây sạch/bẩn đều `rc=2`; thêm `--run-root <tmp ngoài kho>` mới cho `0/6`. |
| N5 | **ĐẠT** | Sáu `rg -n -F` tìm đúng các neo tại dòng 553, 566–568, 570 và 575. Dải 553–577 ở `ed50b734...` và HEAD có cùng SHA-256 `cd7599e6c4bb84d72e06996e7b02e6b982def4f0124b05d7e634f147cbc2363c`; ba số `78/5/10,8 M · 85/10/12,8 M · 45/1/3,7 M` nguyên vẹn. |
| N6 | **ĐẠT** | `git diff --name-status c35ae1c0...HEAD` → đúng `M docs/GOI_AGENT_DA_NEN.md`; `git diff --check ...` → `rc=0`. |
| N7a | **ĐẠT** | `python3 .claude/dev/packet_loop.py doctrine-scan --root . --path docs/GOI_AGENT_DA_NEN.md` → `rc=0`, `đã quét 8 tệp, 0 chỗ chép doctrine`. |
| N7b | **ĐẠT** | `git diff --numstat c35ae1c0...HEAD -- docs/GOI_AGENT_DA_NEN.md` → `179  0`; `179 <= 200`. |

## Gate và test đã chạy

### `passed`

- `python3 .claude/dev/packet_loop_test.py` → `rc=0`; nền `257/257`, 66 đột biến,
  78 lớp lách, 35 ca bắt-oan, 0 ngoại lệ AC18, `TỔNG: ĐẠT`.
- `python3 scripts/tl.py doc-claims-check --strict --json` → `rc=0`, `ok=true`,
  105 tệp, 359 advisories, 0 flags, `layers_skipped={}`.
- Hai ca launcher đích danh `t10_worktree...` và `t12_tep...` → mỗi ca `1/1 qua`,
  `rc=0`.
- Phép chạy đầy đủ có `--run-root`: sạch `rc=0`; bẩn một tệp untracked `rc=6`.

### `failed` — finding, không phải gate nền

- Lệnh phép đo được in nguyên văn trong doctrine → `rc=2` ở cả hai trạng thái do thiếu
  `--run-root`.
- Hai lần gọi thử selector test bằng tiền tố quá ngắn (`t10`, `t12`) → `rc=2` vì mỗi
  tiền tố khớp 11 ca; đã sửa lệnh thành tiền tố duy nhất và hai ca đích đều pass.

### `skipped`

- Không có required local check nào bị `skipped`.

### `not_run`

- Không chạy toàn bộ `launcher_test.py`; phạm vi thay đổi là docs, và hai ca hiện hữu
  trực tiếp khóa hành vi mới đã được chạy riêng.
- Không chạy gate phát hành/LIVE hay Windows; packet docs-only không yêu cầu và môi
  trường review này là Linux offline.

## FINDING MỚI

### `require-clean-vuot-pham-vi-quyen-ghi` [P1] — mệnh đề cây bẩn nằm ngoài phạm vi mục

- **Tệp/dòng:** `docs/GOI_AGENT_DA_NEN.md:651–654`, `:692–695`.
- **Vấn đề và phép đo:** câu đầu khóa đối tượng thành quyền ghi vào kho; bullet sau đo
  một event khác là có cho chạy lệnh con khi worktree bẩn hay không. Phép A/B `0/6`
  chứng minh guard ấy thật, nhưng không đưa event đó vào phạm vi quyền ghi.
- **Vá ở đâu/tại sao:** ưu tiên giữ phạm vi mục và chuyển mệnh đề cây-bẩn cùng phần của
  nó trong phép đếm sang một mục có scope riêng; vị trí này là nơi phải sửa vì N1 yêu
  cầu câu đầu phủ toàn thân. Đường khác là mở rộng câu phạm vi thành đúng hai đối tượng,
  nhưng phải chứng minh việc mở scope không chồng packet #334.
- **Ca khóa:** một kiểm tra tài liệu phải đối chiếu mọi bullet được tính với danh sách
  đối tượng ở câu scope; mutant thêm lại một bullet về event khác phải đỏ.
- **Rủi ro bản vá:** xóa thẳng bằng chứng `0/6` sẽ làm mất phân biệt đúng giữa detector
  và blocker; nếu chuyển, phải giữ nguyên bằng chứng và nhãn đúng nghĩa ở chỗ mới.
- **Độ tin:** cao.

### `require-clean-command-thieu-run-root` [P2] — lệnh ghi trong doctrine không chạy được

- **Tệp/dòng:** `docs/GOI_AGENT_DA_NEN.md:692–695`.
- **Vấn đề và phép đo:** chạy đúng chuỗi in ra trả `rc=2` ở cả cây sạch/bẩn vì
  `--run-root` là bắt buộc; kết quả `0/6` chỉ xuất hiện sau khi reviewer tự bổ sung tham
  số không có trong tệp.
- **Vá ở đâu/tại sao:** thêm `--run-root <thư-mục-tạm-ngoài-kho>` ngay trong lệnh đo ở
  dòng 693; không đặt trong repo vì chính run artifact sẽ làm cây bẩn.
- **Ca khóa:** trích đúng command từ tài liệu, thay placeholder bằng thư mục tạm, chạy
  trên clone sạch và clone có một tệp untracked; đòi lần lượt `0/6`. Mutant bỏ
  `--run-root` phải chết ở parser.
- **Rủi ro bản vá:** hard-code một đường dẫn dùng lại có thể va chạm run ID hoặc làm bẩn
  workspace; dùng placeholder/mktemp ngoài kho.
- **Độ tin:** cao.

### `phep-dem-bo-sot-menh-de-proxy` [P2] — phép đếm “đầy đủ” bỏ một nhãn hiện hành

- **Tệp/dòng:** `docs/GOI_AGENT_DA_NEN.md:619–622`, `:679–684`.
- **Vấn đề và phép đo:** dòng 684 gắn nhãn đầy đủ `chiều MỞ` cho mệnh đề cơ chế proxy
  ambient, ngoài hai mệnh đề điều kiện ở 679/680. Theo đơn vị “lần gắn nhãn cho một
  mệnh đề”, tổng tối thiểu là 8 và `MỞ ×4`, không phải 7/`MỞ ×3`.
- **Vá ở đâu/tại sao:** đường rẻ nhất là biến dòng 684 thành con trỏ giải thích hai nhãn
  đã có trong bảng, không gắn thêm một nhãn mới; hoặc giữ mệnh đề độc lập và cập nhật
  phép đếm thành 8. Sửa ở cả định nghĩa đơn vị và projection số, không chỉ một con số.
- **Ca khóa:** bộ đếm phải định danh từng proposition+condition; mutant thêm một kết
  luận cơ chế có nhãn ngoài danh sách chỉ định phải làm count đỏ.
- **Rủi ro bản vá:** đếm theo literal sẽ tính cả lời kể lịch sử; cần loại lịch sử bằng
  identity/phạm vi, không chỉ grep cụm nhãn.
- **Độ tin:** cao.

### `ba-control-chi-dung-cho-bang` [P2] — lượng từ BA rộng hơn phần đã đếm

- **Tệp/dòng:** `docs/GOI_AGENT_DA_NEN.md:594–599`, `:651`, `:688–695`.
- **Vấn đề và phép đo:** ba họ control là đúng cho năm hàng bảng. Nhưng dòng 594 nói
  “các control của mục này — BA control”, trong khi prose cùng mục còn gọi
  `--require-clean` và bộ ba clone/cleanliness. Mệnh đề đã được giới hạn `TRONG BẢNG`,
  lượng từ control chưa được giới hạn tương ứng.
- **Vá ở đâu/tại sao:** đổi thành “BA control TRONG BẢNG” hoặc bỏ lượng từ tổng ở dòng
  594; tiêu đề dòng 651 cũng nên làm rõ nó đặt tên riêng cho bảng.
- **Ca khóa:** tách control-ID ở bảng và prose; thêm một control prose không được làm
  câu “BA control trong bảng” đỏ, nhưng phải làm câu “BA control của cả mục” đỏ.
- **Rủi ro bản vá:** gom `--require-clean` vào một trong ba họ chỉ để cứu con số sẽ trộn
  các cơ chế khác nhau và tái tạo lỗi đếm row thành control.
- **Độ tin:** cao.

### `hai-menh-de-chua-chot-nhung-goi-duy-nhat` [P2] — số ít chỏi số hai

- **Tệp/dòng:** `docs/GOI_AGENT_DA_NEN.md:633–638`.
- **Vấn đề và phép đo:** dòng 633–634 nói hai ô `chưa xếp được` là hai mệnh đề chưa
  chốt; dòng 637 ngay sau đó gọi “mệnh đề chưa chốt duy nhất”. Hai mệnh đề là hàng
  `workspace-write` và bullet quyền ghi/push.
- **Vá ở đâu/tại sao:** đổi dòng 637 thành “một trong hai mệnh đề chưa chốt — hàng
  `workspace-write` — không mang phiên bản...” để không vô tình áp cùng lý do cho bullet
  quyền ghi/push.
- **Ca khóa:** kiểm cặp số lượng ở đoạn giải thích với số proposition mang nhãn
  `chưa xếp được`; mutant `một trong hai` → `duy nhất` phải đỏ.
- **Rủi ro bản vá:** sửa thành “cả hai” sẽ gán sai cùng nguyên nhân thiếu phiên bản/lặp
  cho mệnh đề quyền ghi, vốn chưa xếp vì chưa biết cơ chế không tố cáo.
- **Độ tin:** cao.

## CHỖ KHÔNG ĐO ĐƯỢC

1. **PR head/check/CI, Packet projection, lease và review budget trên GitHub:**
   `KHÔNG_ĐO_ĐƯỢC` vì mạng sandbox đóng và chỉ thị cấm gọi GitHub/fetch. Local exact
   HEAD/tree/base/diff đã đo; không suy trạng thái remote từ chúng.
2. **Spec hash của Issue #318:** `KHÔNG_ĐO_ĐƯỢC`; lease local không có trường này và
   body Issue không đọc được offline.
3. **Nội dung/trạng thái trực tiếp của Issue #334:** `KHÔNG_ĐO_ĐƯỢC`; chỉ xác nhận được
   số/slug khớp hồ sơ lease local.
4. **Ba `stdout.log` gốc của bảng 78/85/45:** `KHÔNG_ĐO_ĐƯỢC` vì không tracked. Lượt
   này chỉ chứng minh toàn dải N5 giữ nguyên byte so với vòng 7.
5. **GitHub ref/credential-proxy hiện tại:** `KHÔNG_ĐO_ĐƯỢC`; không tái chạy push hoặc
   kiểm remote trong review offline.
6. **Model build/string chính xác phía dịch vụ:** `KHÔNG_ĐO_ĐƯỢC`; execution surface
   chỉ phơi danh tính Codex service, không phơi chuỗi model bền để ghi receipt.
7. **`sáu chục dòng` như một số chính xác:** `KHÔNG_ĐO_ĐƯỢC` vì câu lịch sử không định
   danh exact blob và hai endpoint; chỉ đọc được như mô tả xấp xỉ.

## Đếm finding

- P1: **1**
- P2: **4**

Đường dẫn verdict: `ops/reviews/doctrine-ranh-gioi-reviewer-review-8-codex-verdict.md`

Finding P1/P2: **1/4**
