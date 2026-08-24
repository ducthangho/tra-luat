# ĐẶC TẢ ĐÓNG BĂNG — `T33-DOI-SHELLCHECK`, **bản sửa đổi 4** (delta)

> **CHỈ ghi phần thay đổi** so với r3 (`78c3ecb40eb8dd7dcf628ef7ea9a372aae5cfbf7a4fcfd25bb4ec7f32fe6ea0d`).
> r1 (`1405d390ca9376725517d01ef5b8d1abffd6a09d78d2b7206c2f068e7711f4da`), r2
> (`b9620d17b86f503b12d93359fb6d3423d29c034c29ab372f40cc5d7089b40e71`) và r3 **KHÔNG bị sửa,
> KHÔNG bị xoá**; mọi thứ r4 không nêu thì r3 (rồi r2, rồi r1) nguyên hiệu lực.

```yaml
packet_id: T33-DOI-SHELLCHECK
packet_issue: 249
revision: 4
sua_dung_mot_dieu: docstring của ca `t98` — một lời khai rộng hơn phép đo
khong_doi: mọi mục tiêu, write set, nghiệm thu, điều kiện dừng của r1/r2/r3
```

## Bản này sửa ĐÚNG MỘT lời khai, không đặc tả gì mới

`r3:192` viết:

```
rc=0 trên toàn chân Ubuntu (đo 23-08-2026)
```

Câu ấy nói về đột biến `X2` (thay mệnh đề nền bằng phân biệt theo TÊN TỆP). **Đột biến ấy chưa
bao giờ được đẩy lên CI**, nên nó chưa từng chạy trên một runner Ubuntu nào — nó chạy trong một
worktree cục bộ. `"toàn chân Ubuntu"` chỉ cả job/leg CI.

**Lời khai rộng hơn phép đo — hình dạng `A`.**

## Vì sao đáng một bản sửa đổi chứ không phải một dòng CHANGELOG

Ba tầng, và tầng thứ ba là phần đắt:

1. Câu sai nằm trong **đặc tả ĐÓNG BĂNG**, băm được lease `#249` ghim làm `spec_sha256_required`.
2. Nó **đi qua vòng cross-review của PR #288 với `0` finding** — phân bố đã đo trong
   `nang_tran.can_cu` của lease: `r2 = 0 · r3 = 0 · handoff = 4`.
3. Rồi luật **`r4/Q13`** — *"chép bản vá đã chạy, KHÔNG tự nghĩ lại"* — **chuyển nguyên vẹn** nó vào
   `ops/lease_publish_test.py`. Người thi công làm **ĐÚNG** luật và vẫn đưa một lời khai sai vào mã.

Luật dựng ra để chặn hình dạng `E` (executor tự nghĩ lại) đã **vận chuyển trung thành một hình
dạng `A`**. Đây không phải lỗi khâu thi công; nó là chỗ hai luật gặp nhau mà chưa ai đo.

Vòng nó khép lại đáng ghi: câu sai nằm trong ca `t98` — ca sinh ra cho mục `N3` của #269 — **cùng
packet** với mục `M4`, vốn tồn tại **để hạ một lời khai rộng hơn phép đo trong docstring `t33`**.
Packet chống hình dạng `A` mang sẵn một hình dạng `A` trong đặc tả của chính nó, và **ba vòng đọc**
(một của #288, một của #293 lượt 1) đi qua mà không dừng lại. Chỉ lượt 2 của #293 bắt được.

## Lời khai ĐÚNG — thay cho `r3:192`

```
rc=0 khi chạy cục bộ trên Linux (đo 23-08-2026)
```

Phép đo đằng sau nó, nói cho chật: đột biến `X2` áp lên cây **NỀN** cho `97/97 đạt; đã chạy=97,
bỏ qua=0`, `rc=0`, chạy trong một worktree rời trong container Linux, 23-08-2026. Câu mới **không**
nói "mọi Linux" và **không** nói chân CI nào.

## Khối `t98` — bản ĐÚNG để chép từ nay

`r4/Q13` vẫn nguyên hiệu lực: chép NGUYÊN VĂN khối dưới, KHÔNG tự nghĩ lại. Ai còn chép từ `r3`
sẽ chép lại đúng câu sai.

```python
@ca
def t98_truc_phan_biet_la_NEN_chu_khong_phai_TEN_TEP():
    """Cặp với `t73`: CÙNG tuple, ĐỔI mỗi nền, phải ra kết quả NGƯỢC nhau.

    `t73` một mình chỉ chứng minh "posix thì không bỏ qua". Nó KHÔNG chứng minh quyết
    định ấy tra theo NỀN: thay mệnh đề nền bằng phân biệt theo TÊN TỆP vẫn cho 97/97,
    rc=0 khi chạy cục bộ trên Linux (đo 23-08-2026). Ca này khoá đúng cái trục ấy.

    Đi qua `main()`, KHÔNG gọi thẳng `_ly_do_bo_qua_workflow` — tuân `r4/Q8`.
    """
    def bo(): raise BoQuaNen(WORKFLOW_DANG, "dang")
    rc, out = _chay_main_meta(bo, "nt")
    bang(rc == 0 and "bỏ qua=1" in out,
         f"cùng tuple mà nền nt KHÔNG bỏ qua: rc={rc}, {out!r}")
```

Băm khối 14 dòng (từ `@ca`): `1ed3eb53770076d6` — thay cho `4c9b223d3e5edd4a` của r3.
Lệch **đúng 1/14 dòng**; decorator, tên, thân ca và 13 dòng còn lại đồng nhất.

## Trạng thái thi hành khi ký bản này

Mã **đã mang** lời khai đúng từ `3239279b` (PR #293), **trước** bản đặc tả này — vì bản vá đi theo
đường ghi đè có vết (lease `r4`, khối `ghi_de_byte_identity_voi_dac_ta`) chứ không đợi đặc tả. Bản
r4 này **đóng nguồn**, để lần sau ai chép `r3` không chép lại câu sai. Sau khi r4 land, khối
`ghi_de_byte_identity_voi_dac_ta` của lease `r4` trở thành **vết lịch sử**, không còn là điều khoản
đang có hiệu lực: mã và đặc tả lại khớp.

## `nghiem_thu` — KHÔNG đổi

Toàn bộ `W11`–`W14` của r3 giữ nguyên. Bản này không đụng logic ca nào, nên bảy ô không đổi. Đã đo
lại trên `3239279b` sau khi sửa docstring, môi trường sạch:

```
NEN                  97/97 dat; bo qua=0
NEN + X2             97/97 dat; bo qua=0
VA                   98/98 dat; bo qua=0
VA + X1              89/90 dat; bo qua=8   DO t73
VA + X2              97/98 dat; bo qua=0   DO t98
VA + X1 · go t70     88/89 dat; bo qua=8   DO t73
VA + X2 · go t70     96/97 dat; bo qua=0   DO t98
```

## Chưa đo được — giữ nguyên từ r3, và thêm một mục

1. **Hành vi trên `windows-latest` THẬT** — cả bảy ô chạy Linux.
2. **Còn lời khai nào KHÁC cùng hình dạng trong r1/r2/r3 không** — **CHƯA AI QUÉT**. Một câu đã lọt
   qua ba vòng đọc thì "chỉ có một câu" là giả định, không phải phép đo. Nợ có tên
   `SPEC-QUET-LOI-KHAI` — xem #297.
3. **Kho không có cơ chế canh văn xuôi.** `t42` khớp marker nợ ↔ sổ; `doc-claims-check` đọc trích dẫn
   số hiệu văn bản, không đọc lời khai về phép đo. Nên hình dạng `A` trong văn xuôi hiện **chỉ bắt
   được bằng mắt reviewer**, và ba vòng đã chứng minh mắt thì trượt.
