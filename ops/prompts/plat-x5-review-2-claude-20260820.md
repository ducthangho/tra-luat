# Prompt BẤT BIẾN — Reviewer chéo `PLAT-X5`, lượt **2/2**, provider `claude`

**ĐẢO VAI:** executor là `codex`, reviewer là `claude`. Vẫn cross-provider ⇒ §8 thoả.

**ĐÂY LÀ LƯỢT REVIEW CUỐI CÙNG CỦA PACKET.** `review_rounds_limit: 2`, lượt 1 đã tiêu.
Executor cũng đã dùng **3/3 attempt**. Nghĩa là: `changes_requested` ở lượt này KHÔNG mở ra
lượt vá nào nữa — nó đẩy packet lên checkpoint để người giữ kho xử cách khác. Hãy soi với ý
thức đó: **finding phải neo được vào một phép đo**, đừng nêu thứ chỉ là sở thích kiến trúc.

Read-only với KHO: **không commit, không push, không đổi HEAD.**

```
./nhiem_vu.txt          prompt này
./PACKET_ISSUE_206.md   đặc tả có thẩm quyền (revision 2)
./VERDICT_LUOT_1.md     verdict cross-review lượt 1 (chính bạn, trên e071e0aa) — 5 finding
./diff_delta.patch      e071e0aa..2284b465 — ĐÚNG phần vá của lượt này
./diff.patch            a09aae62..2284b465 — toàn bộ packet, để soi hồi quy
./bin/actionlint        actionlint 1.7.7 (NGOÀI cây kho)
./kho/                  bản sao kho — `git worktree` tách rời tại exact head, GHI ĐƯỢC
```

Lệnh git dạng `git -C kho ...`; test chạy sau khi `cd kho`. PATH: `export PATH="$PWD/../bin:$PATH"`.

**CHỐT SẠCH CÂY:** `git -C kho status --short` RỖNG trước và sau; HEAD không đổi. Đột biến chạy
trên **BẢN SAO TẠM** (`git -C kho archive <sha> | tar -x -C <thư mục tạm>` — thuần đọc).
Lượt 1 đã lỡ ghi vào INDEX của worktree vì dùng `git --work-tree=… checkout -- .`; **đừng lặp
lại lỗi ấy**, và nếu vẫn lỡ thì KHAI THẲNG trong verdict như lượt 1 đã khai.

## 1. Mỏ neo

| trường | giá trị |
|---|---|
| packet | `#206` · PR `#207` (xếp tầng trên PR `#205`) |
| exact head | `2284b4657304d0229e95d1f64ebd0c22035d201d` — ĐO LẠI bằng `git -C kho rev-parse HEAD` |
| head lượt trước | `e071e0aae6bdc4d270a42fbc534ad3f05dcba0fa` (đã review, verdict `changes_requested`) |
| base packet | `a09aae627533f59e6b2e817858a6db50b999d41c` |
| delta lượt này | **2 tệp**: `ops/cai_actionlint.sh` (+3−1) · `ops/lease_publish_test.py` |
| CI trên exact head | lượt `workflow_dispatch` **32402136904**: `gate (ubuntu-latest)` **success**, `gate (windows-latest)` **success**, **0 bước hỏng ở cả hai job** |

Bước `lease-publish selftest (cài công cụ + chạy cổng)` **success trên CẢ Windows lẫn Ubuntu** —
tức wrapper đã chạy thật trên Windows. Con số này do **phiên điều phối đo**, không phải bạn;
nếu bạn không tự xác minh được thì khai là **lời khai của người khác**, đúng như lượt 1 đã làm.

## 2. Bốn việc executor đã làm — và ĐÚNG BỐN VIỆC ĐÓ

Lượt 1 nêu 5 finding. Người giữ kho **phân xử phạm vi**: hai mục nặng nhất tách sang packet
`#209` (PLAT-X6), lượt này chỉ vá bốn:

| finding lượt 1 | xử ở đâu | executor làm gì |
|---|---|---|
| **P1** `t25` không còn thấy lời gọi bộ kiểm | **TẠI ĐÂY** | regex nhận thêm token lệnh dẫn đầu + wrapper; thêm chốt riêng `thay_wrapper >= 1`; ngưỡng 3 → 4 |
| **P2** nợ `required-status-check` không vào sổ nợ | **`#209`** | *không chạm* |
| **P2** `t34` khai hẹp hơn thực tế | **TẠI ĐÂY, đường RẺ** | chỉ sửa **lời khai** — liệt kê đủ 5 dạng lọt. **Regex KHÔNG đổi.** Việc đảo thành danh sách cho phép thuộc `#209` |
| **P3** `GOI_WRAPPER` gác nghĩa vụ ⇒ ra ngoài là được miễn | **TẠI ĐÂY** | nhận diện theo token thực thi rồi **TỪ CHỐI** dạng ngoài danh sách |
| **P3** `mkdir` hỏng trả rc=1 | **TẠI ĐÂY** | mã thoát riêng **12** + thông điệp phân biệt |

**PHẠM VI CỦA LƯỢT REVIEW NÀY:** finding 2 và phần "đảo `t34` thành danh sách cho phép" đã được
người giữ kho chuyển sang `#209`. **Nêu lại chúng như finding CHẶN của `#206` là sai phạm vi** —
quyết định đã có, và một reviewer nhắc lại quyết định đã phân xử thì đang review người giữ kho
chứ không review bản vá. Được phép ghi chúng vào mục "còn mở, đã có chỗ xử".

## 3. Trục phải soi — HAI CHIỀU, đo trên bản sao tạm

1. **Chốt mới có RĂNG không.** Với mỗi chốt trong delta, dựng một đột biến giết nó, và **chạy
   cùng đột biến ấy trên `e071e0aa`** để chứng minh cây cũ IM. Một chốt chỉ được coi là đóng lỗ
   khi có **cả hai chiều**. Bốn đột biến executor khai đã giết: bỏ `$NEO` khỏi wrapper · gỡ hẳn
   wrapper · `bash ./ops/…` thiếu `AL_VER` · gỡ chốt mã `mkdir`. **Xác nhận cả bốn, đừng tin.**
2. **Chốt mới có BÁO OAN không.** Đây là mặt executor dễ bỏ sót nhất. `t25` nay bắt cả
   `bash|sh|exec`; dòng `sha256sum ops/…` cố ý không có `$NEO`. Có dòng hợp lệ nào bị bắt nhầm?
   Thử thêm một bước vô hại nhắc tên tệp trong `echo`, trong chú thích, trong tên bước.
3. **Ngưỡng `thay >= 4` có tự trở thành cổng xanh rỗng lần nữa không?** Lượt 1 giết ngưỡng 3 vì
   ba lời gọi KHÁC tự thoả nó. Hỏi đúng câu ấy với 4: gỡ wrapper rồi thêm một lời gọi
   `lease_publish.py` thứ tư — cổng còn đỏ không? Chốt `thay_wrapper >= 1` có bù được không?
4. **`GOI_WRAPPER_THUC_THI` — nhận diện được bao nhiêu, và phần KHÔNG nhận diện được thì sao?**
   Đây là chỗ lỗ cũ có thể tái sinh dưới hình dạng mới: dạng nào **không khớp regex nhận diện**
   thì vẫn rơi vào `continue`, tức **vẫn được miễn** nghĩa vụ `AL_VER`. Thử ít nhất:
   `env AL_X=1 bash ops/chay_lease_publish_test.sh` · `bash -c 'bash ops/chay…'` ·
   `command bash ops/chay…` · đường dẫn tuyệt đối · `${{ github.workspace }}/ops/chay…`.
   **Nếu còn dạng lọt thì câu hỏi KHÔNG phải "vá tiếp thế nào"** (trần attempt đã cạn) mà là:
   *lời khai trong mã có nói đúng phạm vi ấy không?* Khai thiếu là finding; lọt-mà-đã-khai là nợ.
5. **rc=12 có thật sự phân biệt được không.** `12` có đụng mã nào khác của installer, của wrapper
   (`10`, `11`), hay của suite không? `mkdir -p` hỏng vì lý do khác (quyền, đường dẫn quá dài,
   đích là symlink gãy) có ra `12` không, hay lại rơi về `1`? `|| loi 12` có thật sự chặn `set -e`?
6. **Lời khai `t34` có ĐÚNG không — cả năm dạng.** Lượt 1 đo được 5 dạng lọt. Executor chép chúng
   vào docstring. **Chạy lại cả năm** trên cây mới: dạng nào thực ra KHÔNG lọt thì lời khai đang
   **sai theo chiều ngược lại** — và một lời khai sai làm người đọc tin nhầm hai lần. Đồng thời
   xác nhận `_CHAY_BO_TEST` **không đổi một ký tự** (đúng cam kết "không nối regex").
7. **Hồi quy.** Số ca vẫn **40**, không tụt. Hai phản chứng vòng 2 (`V2a`, `V2b`) vẫn ĐỎ `t34`.
   Ba trục lượt 1 đã đo sạch (wrapper không tách rời · `exec` giữ rc · ba nhánh python) có bị
   bản vá này làm hỏng không? `actionlint` rc=0 cả 5 workflow. `diff.patch` trung thực với
   `git diff`. Write set không có tệp thứ ba.

## 4. Điều kiện DỪNG

- Thấy một tiêu chí ở mục 3 là **sai** ⇒ DỪNG và nói ra, đừng tự đổi tiêu chí giữa đường.
- Cần sửa mã để chứng minh một luận điểm ⇒ **KHÔNG sửa cây kho**; dựng bản sao tạm.
- Phát hiện thứ đòi sửa tệp **ngoài** `ops/lease_publish_test.py` và `ops/cai_actionlint.sh`
  ⇒ ghi thành finding kèm đề xuất, KHÔNG tự mở rộng.

## 5. Định dạng trả về

Kết thúc bằng **đúng hai dòng cuối**, không có gì sau chúng:

```
VERDICT: <approve|changes_requested|do_not_land>
Reviewed commit: <sha 40 ký tự đã ĐO bằng git -C kho rev-parse HEAD>
```

Trước hai dòng đó: các finding (mức P1/P2/P3, **bằng chứng đo được**, invariant bị cắt, gợi ý
vá), rồi mục **"đã đo và sạch"** (để im lặng không bị đọc thành chưa thử), rồi mục
**"chưa đo được — ghi là GIẢ THUYẾT"**. Lượt 1 làm đúng khuôn này; giữ nguyên khuôn.

**`approve` ở lượt này nghĩa là gì:** bốn việc trong phạm vi đã đóng, không hồi quy, và mọi thứ
còn hở đều đã **được khai tên** (ở đây hoặc ở `#209`). KHÔNG có nghĩa là `t34` đã kín — nó chưa,
và cả hai bên đều biết. Đừng giữ `changes_requested` chỉ vì một lỗ đã được khai và đã có packet.
