# Prompt BẤT BIẾN — EXECUTOR `PLAT-X5` (#206), lượt 1 **revision 2**, provider `codex`

> **LƯỢT TRƯỚC BẠN ĐÃ DỪNG, VÀ DỪNG ĐÚNG.** Bạn phát hiện `#206` tự mâu thuẫn: §5 đòi xử "ba
> phản chứng vòng 3" nhưng chỉ liệt kê nhóm `t34`, trong khi finding ZIP cần sửa
> `ops/cai_actionlint.sh` — ngoài write set. Bạn tái hiện được ZIP (`rc=5` cả hai ca) rồi dừng
> thay vì lách phạm vi. Đó là hành vi đúng, và nó bắt lỗi của NGƯỜI VIẾT ĐẶC TẢ.
>
> **Người giữ kho đã phân xử:** `ops/cai_actionlint.sh` **nay NẰM TRONG write set**; `#206` xử
> **cả ba** finding. §5 của Issue đã viết lại cho hết mập mờ. Đọc §0 của Issue.
>
> Điều kiện dừng vẫn nguyên hiệu lực — đừng vì đã bị chặn một lần mà ngại dùng lại nó.

Bạn là NGƯỜI THI CÔNG packet này. Reviewer sẽ là `claude` (khác nền — §8 thoả, chỉ đảo vai
so với các packet trước).

## 0. Bố cục

```
./nhiem_vu.txt          prompt này
./PACKET_ISSUE_206.md   thân Packet Issue — ĐÂY LÀ ĐẶC TẢ CÓ THẨM QUYỀN
./VERDICT_LUOT_3.md     verdict vòng 3 của codex trên #203 — ba finding phải xử
./bin/actionlint        actionlint 1.7.7 (NGOÀI cây kho). PATH: export PATH="$PWD/../bin:$PATH"
./kho/                  cây làm việc — nhánh `codex/plat-x5-exec-1`, GHI ĐƯỢC
```

Làm việc trong `./kho`. **Commit vào nhánh ấy. ĐỪNG `git push`** — phiên điều phối đẩy sau khi
kiểm. Đừng đụng ra ngoài sandbox.

## 1. Mỏ neo

| trường | giá trị |
|---|---|
| packet | `#206` — `[WP PLAT-X5]` |
| nhánh | `codex/plat-x5-exec-1` |
| base | `a09aae627533f59e6b2e817858a6db50b999d41c` (head PR `#205`, packet `#203`) |
| write set | `ops/lease_publish_test.py` · **`ops/cai_actionlint.sh`** · `.github/workflows/ci.yml` · `.github/workflows/ops-publish-lease.yml` · `planned:ops/chay_lease_publish_test.sh` |

**VÌ SAO BASE LÀ MỘT PR CHƯA MERGE:** `ops/cai_actionlint.sh` chỉ tồn tại trên nhánh `#203`,
chưa có trên `master`. Wrapper phải gọi lại nó (ĐỪNG chép). Nên packet này **xếp tầng**; thứ tự
land là `#205` rồi mới tới đây.

## 2. Việc

Đọc `PACKET_ISSUE_206.md` — đó là đặc tả. Tóm tắt để bạn không đọc lệch:

`t34` cố khẳng định *"job này có cài `actionlint` trước khi chạy bộ test không"* bằng **phân tích
tĩnh trên thân `run` của YAML**. **Ba vòng review, ba lần bị đánh bại** bằng một dạng shell khác
(`echo` → tách job → `python -m` / `bash -c` / `if: false`). Đây là lần thứ tư, nên **đừng siết
mẫu khớp thêm**.

Hướng: **wrapper** `ops/chay_lease_publish_test.sh` gộp cài + chạy vào MỘT lời gọi, hai workflow
chỉ gọi wrapper.

**ĐỌC KỸ CHỖ NÀY — packet tự khai giới hạn của chính nó:** wrapper **KHÔNG tự nó đóng hết**.
`run: echo ops/chay_lease_publish_test.sh` vẫn qua được một phép kiểm ngây thơ — cùng hình dạng,
lần thứ tư. Thứ wrapper mua được là **đổi hình dạng thất bại**: cài và chạy hết tách rời được,
nên "chạy mà thiếu công cụ" hết đường tồn tại; còn lại đúng câu *"CI có thật sự chạy bộ test
không"*, mà câu ấy **không thuộc thẩm quyền của một bộ test** (nó không tự khẳng định được là
mình đã được gọi, cũng không nhìn được job khác). Nhà của nó là required status checks.

**Vậy `t34` phải được QUYẾT LẠI, không siết tiếp.** §4 của Issue nêu ba lựa chọn. **Chọn một và
BIỆN HỘ**; nếu chọn (1) thì phải **khai thẳng nó vẫn thua `python -m`**, đừng giấu.

## 3. Tiêu chí hoàn tất — §5 của Issue, chép ra cho khỏi lệch

- Bộ test rc=0, `N/N` hai số BẰNG NHAU, không tụt dưới **38** ca.
- **CẢ BA FINDING vòng 3 phải được xử** — mỗi phản chứng ĐỎ *hoặc VÔ NGHĨA-có-giải-thích*:
  - **F1** `python -m ops.lease_publish_test` · `bash -c "python ops/lease_publish_test.py"`
  - **F2** installer `if: false`
  - **F3** zip **không đuôi** ⇒ rc=5 · `.ZIP` **hoa** ⇒ rc=5 (bạn đã tái hiện cả hai).
    Sửa ở `ops/cai_actionlint.sh` — NAY TRONG write set. Nhắc: đừng vá bằng cách liệt kê thêm
    đuôi; hợp đồng `AL_GOI` chỉ khai là "đường dẫn tới một gói", không hứa quy ước tên.
- Hai phản chứng vòng 2 vẫn ĐỎ: installer ở **job khác**; installer **sau** selftest.
- `actionlint .github/workflows/*.yml` rc=0 cả 5.
- Mỗi chốt mới có **đột biến giết 1/1**.

## 4. Nếp của kho này — KHÔNG phải tuỳ chọn

1. **`rc` đọc TRỰC TIẾP từ tiến trình.** Nối `| tail`/`| head` là **nuốt mã thoát**; lỗi này đã
   xảy ra ba lần trong đợt vừa rồi, một lần làm cả bảng đo `AL_VER` báo `rc=0` sai.
2. **Đột biến chạy trên BẢN SAO TẠM**, không bao giờ chạm cây thật. Một bản vá NGƯỢC từng đi
   thẳng vào commit vì đột biến ghi vào tệp thật rồi khôi phục trong `finally` — mà `finally`
   không chạy khi bị cắt giữa chừng.
3. **Đồ giả phải mô phỏng TRẠNG THÁI, không diễn kịch bản.** Một bộ test từng cho `40/40` trong
   khi đột biến xoá hẳn lệnh phá vẫn qua, vì đồ giả trả lời theo kịch bản.
4. **Ca có MẶT khác ca có ĐO.** Harness `lease_publish_test.py` **KHÔNG có cơ chế bỏ qua** —
   `main()` chỉ `qua += 1` khi hàm không ném, nên một ca `return` sớm vẫn được đếm là ĐẠT. Đừng
   viết nhánh "không thấy thì bỏ qua"; nếu buộc phải rẽ theo nền thì **mỗi nhánh phải đo thật**.
5. **Chú thích tiếng Việt không dấu trong `.sh`, có dấu trong `.py`** — theo tệp xung quanh. Ghi
   **LÝ DO** và **bằng chứng đo được**, không chỉ ghi "cái gì".
6. **ĐỪNG viết chuỗi bỏ-qua-CI** (`skip` + `ci` trong ngoặc vuông) vào thông điệp commit, kể cả
   khi trích dẫn — GitHub khớp chuỗi trên toàn thông điệp và sẽ tắt gate.
7. Thông điệp commit: nêu **đo được gì**, kèm số. Kết bằng:
   `Co-Authored-By: Codex <noreply@openai.com>`

## 5. Điều kiện dừng — tôn trọng, đừng cố cho xong

- **Gặp lại đúng hình dạng ấy lần thứ tư** (một dạng cú pháp shell mới làm phép kiểm thua) ⇒
  **DỪNG**, không vá. Ghi lại và nói thẳng rằng hướng (2)/(3) mới đúng. Dừng đúng lúc ở đây
  **có giá trị hơn** một bản vá nữa.
- Chốt phải nằm ngoài write set ⇒ DỪNG, xuất handoff.
- Thấy một tiêu chí ở §3 là sai ⇒ DỪNG và nói, đừng tự đổi giữa đường.

## 6. Trả lời

Kết thúc bằng một báo cáo ngắn: đã chọn phương án nào cho `t34` và **vì sao**; số đo (`N/N`,
rc, bảng đột biến); và **cái gì còn hở** — mục cuối này bắt buộc, đừng để trống.
