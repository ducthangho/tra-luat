# Prompt BẤT BIẾN — Reviewer chéo `PLAT-X5`, lượt **3**, provider `claude`

**ĐẢO VAI:** executor là `codex`, reviewer là `claude`. Cross-provider ⇒ §8 thoả.

Đây là **review DELTA**, không phải review lại cả packet. Delta là `2284b465..117e0c42`:
**một tệp** `ops/lease_publish_test.py`, `+129 −18`, hai việc. Hai lượt review trước đã soi
phần còn lại; đừng lặp lại chúng.

Read-only với KHO: **không commit, không push, không đổi HEAD.** Đột biến chạy trên **BẢN SAO
TẠM** dựng bằng `git -C kho archive <sha> | tar -x` (thuần đọc). Lượt 1 đã lỡ ghi vào INDEX vì
dùng `git --work-tree=… checkout -- .`; **đừng lặp lại**, và nếu vẫn lỡ thì KHAI THẲNG.

```
./nhiem_vu.txt          prompt này
./VERDICT_LUOT_2.md     verdict lượt 2 — nguồn sinh ra delta này
./diff_delta.patch      2284b465..117e0c42 — ĐÚNG phần phải soi
./PACKET_ISSUE_206.md   đặc tả có thẩm quyền
./bin/actionlint        actionlint 1.7.7 (NGOÀI cây kho)
./kho/                  bản sao kho tại exact head, GHI ĐƯỢC
```

## 1. Mỏ neo

| trường | giá trị |
|---|---|
| exact head | `117e0c4258c5029c7a330611786733c5a583e1c5` — ĐO LẠI bằng `git -C kho rev-parse HEAD` |
| head trước delta | `2284b4657304d0229e95d1f64ebd0c22035d201d` (đã review ở lượt 2) |
| write set | **`ops/lease_publish_test.py` — ĐÚNG MỘT TỆP** |
| số ca | 40 → **41** (`t41` mới) |
| CI trên exact head | run `32439164265`: `gate(ubuntu)` success · `gate(windows)` success · **0 bước hỏng** cả hai |

## 2. Hai việc của delta

**Việc 1 — sửa LỜI KHAI của `GOI_WRAPPER_THUC_THI`** (finding P2 lượt 2). Chú thích cũ khẳng
định *"Ngoài hai dạng canonical vẫn là một LỜI GỌI"* — lượt 2 đo được câu ấy **SAI**. Delta viết
lại lời khai cho khớp phép đo và khai `NỢ CÓ TÊN PLAT-X5-nhan-dien-loi-goi-wrapper`.
**Regex KHÔNG được đổi** — việc mở nó thuộc packet `#209`.

**Việc 2 — `t25` không báo oan chú thích ĐI SAU LỆNH** (finding P3 lượt 2). Thêm hàm
`_cat_chu_thich_run_inline`, chỉ cắt `#` khi nó đứng đầu lệnh hoặc **sau khoảng trắng** và ngoài
nháy/escape. Ca `t41` khoá lại.

## 3. Trục phải soi — theo thứ tự rủi ro GIẢM DẦN

### 3.1 FAIL-OPEN của phép cắt `#` — rủi ro số 1, soi kỹ nhất

Đây là chỗ một bản vá đúng ý định vẫn có thể **đổi một ĐỎ GIẢ lấy một XANH GIẢ**, và xanh giả thì
đắt hơn hẳn. Câu hỏi trung tâm: **có đường nào giấu một lời gọi THẬT sau một `#` để `t25` không
còn thấy nó không?**

Phiên điều phối đã đo bốn ca dưới đây và nói rằng cả bốn **ĐỎ `t25`** (tức không lọt).
**XÁC NHẬN, đừng tin** — rồi đi xa hơn bốn ca ấy:

```
echo a#b && bash ops/chay_lease_publish_test.sh          (# không có khoảng trắng trước)
echo "a # b" && bash ops/chay_lease_publish_test.sh      (# trong nháy kép)
echo 'a # b' && bash ops/chay_lease_publish_test.sh      (# trong nháy đơn)
bash ops/chay_lease_publish_test.sh # ghi chu            (chú thích thật, lời gọi vẫn phải thấy)
```

Hướng tự nghĩ thêm, ít nhất: nháy LỒNG nhau · dấu chéo ngược trước nháy (`\"`) · `$'…'` của bash ·
chuỗi có `#` chưa đóng nháy tới cuối dòng · `${{ }}` chứa `#` · nhiều `#` trên một dòng · dòng
`run:` viết dạng `- run:` · khoảng trắng lạ (tab) trước `#`.

**Hàm tự khai fail-closed** khi `run:` mở bằng `|`, `>` hoặc một nháy (block/quoted scalar):
nó trả nguyên dòng, không cắt. **Kiểm lời khai ấy có đúng không** — và quan trọng hơn: có đường
nào **lách vào nhánh fail-closed rồi lại lọt** không?

### 3.2 `t41` có RĂNG hay chỉ CÓ MẶT

Harness này `qua += 1` khi hàm không ném, nên một ca `return` sớm vẫn tính ĐẠT — bệnh `t24` kho đã
trả giá. **`t41` có nhánh "không thấy thì bỏ qua" không?** Nếu có thì nó phải có chốt
(`bang(not (HERE.parent/".git").exists(), …)` như `t34`), nếu không thì ĐỎ.
Đột biến gỡ dòng gọi `_cat_chu_thich_run_inline` phải giết `t41` **1/1** — xác nhận.
Và hỏi ngược: `t41` đo **hành vi** hay chỉ đo **sự tồn tại của hàm**?

### 3.3 Lời khai mới có LẠI overclaim không

Lượt 2 rơi đúng vào đây: chú thích khẳng định rộng hơn phép đo. **Đọc từng câu của lời khai MỚI
và đo lại từng câu.** Bốn dạng nó liệt kê là lọt — có thật lọt? Hai dạng đối chứng — có thật bị
bắt? Câu mô tả giới hạn của phép cắt — có đúng không, hay lại rộng hơn thực tế? Một lời khai sai
lần thứ hai ở cùng một chỗ là tín hiệu về CÁCH LÀM, không phải một lỗi lẻ.

### 3.4 Hồi quy

Số ca **41**, không tụt. `_CHAY_BO_TEST` và `GOI_WRAPPER_THUC_THI` **không đổi một ký tự** (phiên
điều phối kiểm bằng băm — xác nhận độc lập). Hai ca báo oan cũ nay `rc=0`; ba dạng vốn an toàn vẫn
`rc=0`; bốn dạng lọt `AL_VER` vẫn `rc=0` (**không đổi hành vi** là ĐÚNG ở lượt này, không phải lỗi);
đối chứng đường dẫn tuyệt đối vẫn ĐỎ `t35`. `actionlint` rc=0 cả 5.

## 4. NGOÀI phạm vi — nêu lại là sai phạm vi

- **Bốn dạng lọt `AL_VER`** (`env X=1 bash`, `bash -c`, `command bash`, `${{ github.workspace }}`
  có khoảng trắng): đã thành **nợ có tên** ở `#209 §7` kèm điều kiện XONG. Người giữ kho đã phân
  xử. Được ghi vào mục "còn mở, đã có chỗ xử"; **không** được nêu như finding CHẶN.
- Đảo `t34` thành danh sách cho phép — `#209`.
- Nợ `PLAT-X5-required-status-check` — `#209`.
- Nhánh Windows của `t40`, branch protection — ngoài tầm sandbox, đã khai ở hai lượt trước.

## 5. Một điều phải biết về lượt này

Bản vá `117e0c42` **chưa từng được ai review**. Nó được đẩy sau khi phiên điều phối tự đo — và
phiên điều phối **cũng là bên viết lease và prompt cho executor**. Bạn là lớp soi độc lập ĐẦU TIÊN
và duy nhất của delta này. Đừng để bảng số đẹp ở mục 3.1 làm bạn đi nhanh: **những con số ấy do
chính bên có động cơ muốn land tạo ra.**

## 6. Điều kiện DỪNG

- Cần sửa mã để chứng minh một luận điểm ⇒ dựng bản sao tạm, **không sửa cây kho**.
- Thấy một tiêu chí ở mục 3 là sai ⇒ DỪNG và nói ra, đừng tự đổi giữa đường.
- Phát hiện thứ đòi sửa tệp ngoài `ops/lease_publish_test.py` ⇒ finding + đề xuất, không tự mở rộng.

## 7. Định dạng trả về

**IN RA STDOUT** — lượt 2 chỉ in tóm tắt rồi ghi verdict vào một tệp trong sandbox, mà sandbox
lượt trước đó đã từng bị xoá sạch giữa đợt. Verdict phải nằm trong **đầu ra của tiến trình**.

Kết thúc bằng **đúng hai dòng cuối**, không có gì sau chúng:

```
VERDICT: <approve|changes_requested|do_not_land>
Reviewed commit: <sha 40 ký tự đã ĐO bằng git -C kho rev-parse HEAD>
```

Trước đó: finding (mức, **bằng chứng đo được**, invariant bị cắt, gợi ý vá) · mục **"đã đo và
sạch"** · mục **"chưa đo được — GIẢ THUYẾT"**.

**`approve` ở đây nghĩa là:** hai việc của delta đã đóng, phép cắt `#` **không fail-open**, `t41`
có răng, lời khai mới **khớp phép đo**, không hồi quy. KHÔNG có nghĩa `t35` đã kín — nó chưa, và
phần chưa kín đã là nợ có tên ở `#209`. Đừng giữ `changes_requested` chỉ vì một lỗ đã được khai
và đã có packet xử.
