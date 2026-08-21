# VERDICT cross-review — bản thẩm định "vòng lặp tri thức" (PR "#214"), lượt 1

**Chép nguyên văn** kết luận của lượt cross-review. Lease `tri-thuc-review-1-codex-20260821`, reviewer **codex**
(khác nhà cung cấp), neo exact head `825558a59fd93623dd2f2c9123577361e9e3abca`.

- Nguồn: stdout/stderr của `codex exec` do `launcher.py` giữ, run `5e0ec9f4`, `ma_thoat=0`.
- Chốt read-only sau lượt: `worktree_sach=True`, `so_muc_ban=0`, HEAD không đổi.
- Đường dẫn tuyệt đối của thư mục phiên đã rút gọn về `kho/…`; **không sửa gì khác**.
- **Kết luận: `changes_requested`.**

---

codex
# Báo cáo thẩm định PR #214

Kết luận: cần sửa trước khi chấp thuận. Phạm vi PR đúng như khai báo: 12 tệp dưới `ops/`, `+1137/−0`, không có mã nguồn bị sửa. Tuy nhiên, bản hợp nhất có một chỗ xuyên tạc bất đồng còn lại của vòng 3, một băm nguồn sai và vài lời khai được nâng từ suy luận/tự thuật thành sự kiện “đo được”.

## Findings

### 1. P1 — “Hội tụ hoàn toàn” che mất một bất đồng thiết kế thực chất

Bản hợp nhất đặt tiêu đề “hai bên hội tụ hoàn toàn về thiết kế” tại [THAM_DINH_VONG_LAP_TRI_THUC_20260821.md](kho/ops/THAM_DINH_VONG_LAP_TRI_THUC_20260821.md:83), nhưng ngay sau đó lại ghi khác biệt còn lại: codex chọn lát 1 `c+d+e`, Fable chọn `a+c+e`.

Bằng chứng chạy được:

```bash
rg -n 'check 3–4|a \+ c \+ e|c \+ d \+ e|Khác biệt còn lại duy nhất|hội tụ hoàn toàn' \
  ops/tham-dinh/tri-thuc-20260821/{codex-vong3,fable-vong3}.md \
  ops/THAM_DINH_VONG_LAP_TRI_THUC_20260821.md
```

Kết quả nguồn:

- codex: check 3–4 cùng receipt gate, tức `c+d+e`;
- Fable: `a+c+e`;
- phiên chính chọn phương án codex.

Đây không phải khác biệt câu chữ: nó quyết định sự cố nào được chặn ngay ở lát 1—thiếu bundle X4 hay đích báo cáo không ghi được. Câu “hội tụ hoàn toàn” vì thế sai; đúng phải là “hội tụ về kiến trúc và receipt gate, còn bất đồng về check của lát 1”.

Cùng hình dạng, câu “bị bác bởi cả hai bên, cả ba vòng” ở mục 2 cũng quá rộng: đề bài vòng 3 ra lệnh không tranh lại các điểm đã chốt, nên sự im lặng vòng 3 không phải một lần tái xác nhận độc lập.

- Bất biến bị cắt: bản hợp nhất phải bảo toàn dissent và không biến quyết định trọng tài của phiên chính thành đồng thuận của nguồn.
- Gợi ý vá: đổi tiêu đề mục 5; tách rõ phần hai bên đồng ý, phần bất đồng, và phần “phiên chính quyết chọn codex”. Hạ “cả ba vòng” thành “vòng 1–2; vòng 3 coi là tiền đề theo đề bài”.

### 2. P2 — Băm đề bài vòng 2 trong bảng nguồn bị sai

`BAM.txt` đúng, nhưng bảng đầu bản hợp nhất ghi `3602eafe…`; tệp thật bắt đầu bằng `3602eaf1…`.

Bằng chứng chạy được:

```bash
sha256sum ops/tham-dinh/tri-thuc-20260821/de-bai-vong2.md
rg -n '3602eafe' ops/THAM_DINH_VONG_LAP_TRI_THUC_20260821.md
```

Kết quả thật:

```text
3602eaf14ec068fb2f2c597c451280311eb95cb0d4ae9faf30422a796971ac77
```

- Bất biến bị cắt: con băm nhận dạng đúng chính xác nguồn mà báo cáo tuyên bố đã dùng.
- Gợi ý vá: thay `3602eafe…` bằng `3602eaf1…`, tốt hơn là ghi đủ 64 ký tự để tránh tiền tố mơ hồ.

### 3. P2 — Tính “ĐỘC LẬP” của hai báo cáo không được hồ sơ trong kho chứng minh

Nội dung hai báo cáo vòng 1 đúng là cùng bác khung ban đầu:

```bash
rg -n 'khung sai|Vấn đề không phải LƯU|Tất định hóa lưu trữ|Tất định hoá việc LƯU' \
  ops/tham-dinh/tri-thuc-20260821/{codex-vong1,fable-vong1}.md
```

Nhưng hồ sơ commit chỉ gồm prompt, báo cáo và bảng băm. Không có receipt/session manifest chứng minh hai lượt chạy cách ly, không đọc kết quả của nhau, hoặc neo run ID. Ba run ID codex và các nhãn “task vòng” chỉ xuất hiện trong chính bản hợp nhất:

```bash
find ops/tham-dinh/tri-thuc-20260821 -maxdepth 1 -type f -printf '%f\n' | sort
rg -n '5f124269|75644324|838809f8|task vòng' \
  ops/tham-dinh/tri-thuc-20260821 \
  ops/THAM_DINH_VONG_LAP_TRI_THUC_20260821.md
```

Vì vậy, “hai báo cáo riêng cùng kết luận” là đo được; “độc lập” là `KHÔNG ĐO ĐƯỢC` từ hồ sơ đã commit.

- Bất biến bị cắt: trạng thái thứ ba phải được khai; băm nội dung không chứng minh provenance hay cách ly phiên.
- Gợi ý vá: hoặc bổ sung receipt/run manifest bất biến cho cả hai provider, hoặc đổi câu thành “hai báo cáo vòng 1 riêng cùng bác khung; tính cách ly phiên theo lời khai của phiên điều phối, không đo được từ hồ sơ này”.

### 4. P2 — Mục 4 nâng tự thuật về “4 lượt review hỏng, không lần nào do reviewer” thành sự kiện chắc chắn

Có bằng chứng dương cho một số thành phần:

- receipt PLAT-M4 ghi prompt trỏ spec không tồn tại và quy trách nhiệm cho phiên điều phối;
- báo cáo codex vòng 1 ghi sandbox không cho tạo tệp, nên báo cáo được trả qua stdout.

```bash
nl -ba ops/reviews/plat-m4-review-2-codex-verdict.receipt.yaml | sed -n '70,92p'
nl -ba ops/tham-dinh/tri-thuc-20260821/codex-vong1.md | sed -n '1,5p'
```

Nhưng tổng “lần thứ tư trong ba ngày”, việc gom cả bốn ca thành cùng một hình dạng, và kết luận “không lần nào do reviewer” được ghi dưới dạng tự thuật của phiên chính tại `do-doc-lap-v1.md`; chúng không có bốn run receipt độc lập tương ứng. Đặc biệt, việc codex vẫn xuất được toàn văn qua stdout cho thấy gọi ca số 4 là “lượt review bị hỏng” là một phân loại quy trình, không phải kết quả máy tự chứng minh.

```bash
nl -ba ops/tham-dinh/tri-thuc-20260821/do-doc-lap-v1.md | sed -n '45,51p'
```

Mục 10 chỉ khai chi phí giờ-người không đo được, chưa khai giới hạn về số ca, phép gom hình dạng và quy kết nguyên nhân. Đây là thiếu caveat quan trọng vì ngưỡng `4 ≥ 3` là lý do chính để đưa Packet 1 lên trước.

- Bất biến bị cắt: bằng chứng dương và phạm vi tuyên bố phải bằng phạm vi đo được.
- Gợi ý vá: ghi “theo tự thuật có băm của phiên chính”; phân biệt các ca có artefact độc lập với ca chỉ có lời kể; thêm vào mục 10 rằng tổng số, phép phân loại cùng hình dạng và quy kết nguyên nhân chưa được đo độc lập.

### 5. P2 — Mục 6 gọi thứ tự thi công là “ĐO ĐƯỢC” dù nguồn gọi đó là suy luận

Codex vòng 3 gắn nhãn rõ ràng cho thứ tự mở packet là `SUY LUẬN`:

```bash
nl -ba ops/tham-dinh/tri-thuc-20260821/codex-vong3.md | sed -n '40,51p'
```

Fable đo được vị trí `t34` và giao điểm với `lease_publish_test.py`, nhưng đồng thời khai:

```bash
rg -n 'Write set CHÍNH XÁC của mục C' \
  ops/tham-dinh/tri-thuc-20260821/fable-vong3.md
```

Tức write set chính xác của mục C chưa được đóng băng. Vì vậy:

- giao điểm `C ∩ spec-gate` tại `lease_publish_test.py` có căn cứ;
- khuyến nghị “Packet 1 ∥ C, rồi spec-gate sau C” là suy luận thiết kế;
- lời khai “write set rời nhau hoàn toàn” giữa Packet 1 và C chưa đo được cho tới khi Packet Spec của C tồn tại.

- Bất biến bị cắt: không nâng khuyến nghị suy ra từ dữ kiện thành phép đo.
- Gợi ý vá: đổi tiêu đề thành “cả hai bên cùng khuyến nghị; các giao điểm đã biết đo được”; gắn nhãn `SUY LUẬN` cho thứ tự mở packet và yêu cầu đo lại exact write set khi Packet C được đóng băng. Thêm exact write set của C vào mục 10 nếu chưa có Packet Spec.

## Các tuyên bố đối chiếu đúng với nguồn

- Cả codex và Fable vòng 1 đều bác khung “tất định hóa việc lưu”; phần nội dung này trung thực.
- Fable thực sự rút chữ ký vòng 1 đối với `chi_la_chu: true` ở vòng 2.
- Cả hai bên thực sự đổi ý/đổi thứ tự ở vòng 2 để chọn script sandbox reviewer fail-đóng làm packet đầu.
- Hai bên vòng 3 cùng chốt `record-review` phải đòi receipt, class `sensitive`, hard stop `+300`, và không để helper chỉ là tùy chọn.
- Khác biệt vòng 3 không phải về kiến trúc chung mà về check nào phải nằm trong lát 1; vì thế chỉ cụm “hội tụ hoàn toàn” cần sửa.

## Kiểm băm

Chạy tại `ops/tham-dinh/tri-thuc-20260821`:

```bash
sha256sum -c BAM.txt
```

Kết quả: cả 10/10 tệp đều `OK`.

Ba băm đề bài thực tế:

| Vòng | Băm thật | Bảng hợp nhất |
|---|---|---|
| 1 | `8b4690a0ff1d…` | khớp |
| 2 | `3602eaf14ec0…` | sai: ghi `3602eafe…` |
| 3 | `23cb6d57592a…` | khớp |

## Đo lại các con số tại neo `0333948`

| Phép đo | Kết quả |
|---|---:|
| receipt có trường `seam` | `0/24` |
| lease có trường `seam` | `0/41` |
| khối “Bài học đắt giá”, kể tiêu đề | `160` dòng, từ dòng 39 đến trước dòng 199 |
| receipt có `verdict_usage_caveats` | `14/24` |
| `chi_la_chu` tại `0333948` | `0` occurrence |

Các lệnh chính:

```bash
git ls-tree -r --name-only 0333948 -- ops/reviews |
  awk '/\.receipt\.yaml$/{n++} END{print n}'
git grep -l -w seam 0333948 -- 'ops/reviews/*.receipt.yaml' | wc -l

git ls-tree -r --name-only 0333948 -- ops/leases |
  awk '/\.yaml$/{n++} END{print n}'
git grep -l -w seam 0333948 -- 'ops/leases/*.yaml' | wc -l

git show 0333948:CLAUDE.md |
  awk '/^## Bài học đắt giá/{on=1;s=NR}
       on && NR>s && /^## /{print NR-s; exit}'

git grep -l '^verdict_usage_caveats:' 0333948 \
  -- 'ops/reviews/*.receipt.yaml' | wc -l

(git grep -o -w chi_la_chu 0333948 -- || true) | wc -l
```

Ở commit đang review, `chi_la_chu` có 22 occurrence, và cả 22 đều do chính PR này thêm. Đây là trôi cây so với neo `0333948`, không phải lỗi của phép đo gốc; tuy vậy, bản hợp nhất nên ghi rõ “tại neo `0333948`” cạnh con số để tránh câu “0 occurrence toàn kho” tự mất hiệu lực sau khi tài liệu được merge.

## Chốt vệ sinh

- HEAD vẫn đúng `825558a59fd93623dd2f2c9123577361e9e3abca`.
- `git status --short` rỗng.
- Không tệp nào trong `./kho` bị sửa trong lượt thẩm định.
- Phạm vi commit: 12 tệp, toàn bộ dưới `ops/`, `+1137/−0`.

VERDICT: changes_requested
Reviewed commit: 825558a59fd93623dd2f2c9123577361e9e3abca
