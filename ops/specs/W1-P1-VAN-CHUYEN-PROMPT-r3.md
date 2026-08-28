# ĐẶC TẢ ĐÓNG BĂNG — `W1-P1-VAN-CHUYEN-PROMPT` — **BẢN SỬA ĐỔI 3**

> Đặc tả này **không cấp việc**. Phải có Issue + lease còn hiệu lực (`docs/PROTOCOL_DA_PHIEN.md`
> §3.2, §4) mới được bắt tay.
>
> Sửa đặc tả đã có băm ⇒ đi qua **bản sửa đổi mới**.

`packet_id`: `W1-P1-VAN-CHUYEN-PROMPT`
`revision`: **3**
`packet_issue`: **368**
`thay_the_cho_ban`: r2 (`4a058ce4d48c62651c8ba734a4cb064335710b5d4f6c50cf939892a06d0da4b3`) — r1 và r2 GIỮ NGUYÊN làm hồ sơ.
`nen_do`: nhánh `codex/w1-p1-van-chuyen-prompt-exec-1` tại `3151371d42557448750ca8b82e5597823c898881`
`thoi_diem_soan`: 2026-08-28T11:34:29Z

## VÌ SAO CÓ BẢN SỬA ĐỔI 3

Cross-review `claude` (cross-provider; executor là `codex`) trả **`blocked` — 2×P1** trên
`3151371d`. Verdict đầy đủ ở comment của PR #381.

**Cả hai P1 đều thuộc ĐẶC TẢ r2, không thuộc executor.** r2 đòi *"Schema từ chối verdict đúng
shape nhưng sai `reviewed_sha`"* trong khi cấp write set ba đường dẫn **không chứa nổi điểm cưỡng
chế**. Executor ĐÚNG khi dừng: thêm validator xuất xưởng là đường dẫn thứ tư ⇒ chạm `S1`.

### P1-1 — `r17`/`r18` KHÔNG đo schema

Reviewer đo được, và đây là phép đo tôi (phiên điều phối) đã **bỏ sót**:

> Thay schema bằng `{'x-tra-luat-runtime-bindings':{…}}` — bỏ hết `type`/`required`/
> `properties`/`additionalProperties` — **`r17` vẫn 1/1 qua, `r18` vẫn 1/1 qua.**
> Đối chứng: `r19`/`r20`/`r21` **ĐỀU hỏng** khi làm yếu schema.

Chúng đo một comparator viết tay (`_schema_hop_le`, d.5936) trong chính tệp test, không đo schema.
Ràng buộc duy nhất lên schema là *"khoá binding có MẶT hay không"*.

Đúng hai bệnh kho đã đặt tên: **"ca có MẶT khác ca có ĐO"** và **"bộ test tự chấm chính mình"**
(#361). Phép đối chứng `r19`–`r21` là thứ làm finding này chắc chắn, không phải phỏng đoán.

### P1-2 — M4/M5 không được thi hành ở đâu cả

`jsonschema` 4.26.0 trên schema @head: `reviewed_sha='b'*40` ⇒ **NHẬN**; `generation=2` ⇒ **NHẬN**.
`x-tra-luat-runtime-bindings` chỉ là chú thích — không tầng schema nào đọc, **không mã xuất xưởng
nào đọc tệp schema**.

Ghép hai P1: **sửa `r17`/`r18` cho trung thực sẽ làm chúng ĐỎ**, vì schema thật sự không từ chối.
Nên M4/M5 không thể vừa được đo trung thực vừa xanh trong write set r2.

## QUYẾT ĐỊNH CỦA NGƯỜI GIỮ KHO (trong phiên, 28-08-2026)

**Hướng (i): mở write set cho validator XUẤT XƯỞNG** đọc `x-tra-luat-runtime-bindings`.
Bác hướng (ii) (viết lại M4/M5 cho khớp thứ schema làm được) vì nó **giữ cổng xanh bằng cách hạ
điều được tuyên bố**, mà semantic identity chính là thứ packet sinh ra để làm.

**Đóng gói: TÁCH ĐÔI.** r3 chỉ chữa 2×P1. Bốn P2 + bốn P3 thành packet nối tiếp có tên.
Căn cứ ADR-0044, neo từ số đo của chính kho: `PLAT-M4` 2 tệp ⇒ **một vòng, một finding**;
`PLAT-X4` 4 tệp ⇒ **ba vòng, tám finding**. Gói to đi tệ hơn, đo được.

## Write set — BỐN đường dẫn (đổi so r2 ⇒ lease r2 MẤT HIỆU LỰC, §3.2)

```
.claude/dev/review_verdict_binding.py        (CHƯA TỒN TẠI — tạo mới, validator xuất xưởng)
.claude/dev/launcher_test.py                 (sửa r17/r18)
.claude/dev/packet_loop.py                   (nối record-review vào validator)
.claude/dev/packet_loop_test.py              (phản chứng cho đường nối)
```

**RA khỏi write set so với r2:** `.claude/dev/launcher.py` và
`.github/coordination/schemas/review_verdict.v1.schema.json`. Thay đổi đã commit ở
`3151371d` **GIỮ NGUYÊN**; r3 không sửa chúng nữa. Bốn P2 chạm `launcher.py` và ba P3 chạm
schema đều thuộc packet nối tiếp.

Trần ADR-0044: 4 tệp < 6, dự kiến < 1000 dòng ⇒ **không vượt ngưỡng nào**, không cần khai ngoại lệ.

## VÌ SAO PHẢI CÓ NGƯỜI GỌI — đừng dời tầng rỗng sang tệp mới

Thêm module validator mà **không ai gọi** là lặp lại đúng khuyết tật P1-1, chỉ đổi chỗ. Người tiêu
thụ thật đã có sẵn: `packet_loop.py` `cmd_record_review` (d.998), và chú thích của chính nó ghi
*"chỉ được ghi bởi `record-review --verdict approve`, tức ĐÚNG MỘT ĐƯỜNG"*. Đó là điểm cưỡng chế.

## Mục nghiệm thu — mỗi mục kèm phép đo làm nó ĐỎ

| # | mục | phép đo bắt buộc |
|---|---|---|
| **N1** | `review_verdict_binding.py` validate verdict bằng **`jsonschema`** trên schema ĐỌC TỪ ĐĨA, không bằng comparator viết tay | ca `rXX_` nạp schema thật. **Đột biến: xoá `properties` khỏi schema ⇒ ca phải ĐỎ.** Đây là đột biến P1-1 đòi. |
| **N2** | validator đọc `x-tra-luat-runtime-bindings` và **từ chối `reviewed_sha` sai commit** dù đúng 40 hex | fixture hợp lệ; đổi mỗi `reviewed_sha` sang 40 hex KHÁC ⇒ bị từ chối. Đột biến: bỏ binding `reviewed_sha` ⇒ ĐỎ |
| **N3** | validator **từ chối `generation` sai số** dù đúng kiểu | như trên với `generation`. Đột biến: bỏ binding `generation` ⇒ ĐỎ |
| **N4** | `r17`/`r18` viết lại để **thật sự đo schema** | đột biến làm yếu schema (xoá `type`/`required`/`properties`/`additionalProperties`) phải làm `r17` **VÀ** `r18` ĐỎ — hiện chúng vẫn xanh |
| **N5** | `packet_loop record-review` **GỌI** validator; verdict không qua validator thì **không** được ghi vào state | ca `rXX_` trong `packet_loop_test.py`: verdict sai `reviewed_sha` ⇒ `record-review` từ chối, state KHÔNG đổi. Đột biến: bỏ lời gọi validator ⇒ ĐỎ |
| **N6** | Đường đọc/validate hỏng ⇒ **KHÔNG ĐO ĐƯỢC** ⇒ **ĐỎ**, không được đọc thành ĐẠT | ca: schema thiếu/không parse được ⇒ `record-review` ĐỎ, không im lặng cho qua |

**N4 là mục quan trọng nhất.** Không có nó thì ta chỉ thêm mã mới bên cạnh hai ca rỗng, và lượt sau
vẫn báo M4/M5 ĐẠT bằng đúng hai ca không đo gì.

## Nợ CHUYỂN sang packet nối tiếp — chép nguyên, đừng để rơi

Bốn P2 (`launcher.py`) và bốn P3 (schema + test) từ verdict `blocked`:

| id | mức | tóm tắt |
|---|---|---|
| `oracle-lech-voi-jsonschema` | P2 | `_schema_hop_le` dùng `re.fullmatch`, `jsonschema` dùng `re.search`; `$` khớp TRƯỚC newline cuối ⇒ `'a'*40+'\n'` được NHẬN. 3/9 ca lệch, **cả ba theo hướng jsonschema dễ dãi hơn** |
| `m1-bam-sau-khi-con-thoat` | P2 | cháu giữ fd ghi muộn ⇒ `run.json` ghi `stdout_byte=6` + băm của 6 byte, trên đĩa **39 byte** băm khác. Sổ **ký HMAC** đóng dấu lên băm KHÔNG khớp hiện vật |
| `m2-danh-tinh-tu-basename` | P2 | `/home/kesau/malware/codex` ⇒ `openai_codex`; `codex-cli`, `cödex` ⇒ `local_process` IM LẶNG. **`r15` hardlink Python thành tệp tên `codex` rồi khẳng định contract là codex — ca test hợp thức hoá phép giả mạo** |
| `transport-sha-vong-tron` | P2 | `transport_sha256` băm chính ba hằng số vừa trả ra ⇒ chỉ phát hiện NHÃN đổi, không phát hiện transport thật đổi |
| `raise-mot-provider-hai-transport-chet` | P3 | bảng 3 provider duy nhất ⇒ `cu != contract` luôn False ⇒ chốt chết |
| `r13-la-bi-danh-cua-t70` | P3 | `r13` chỉ `return t70(...)`; bảng đột biến đếm "giết 2/2" cho cùng MỘT đường mã |
| `khong-rang-buoc-cheo-provider` | P3 | `{provider:'codex', identity.provider:'anthropic'}` HỢP LỆ; `cross_approved` không bị ràng với việc hai bên KHÁC nhau |
| `format-uri-khong-duoc-khang-dinh` | P3 | Draft 2020-12 mặc định `format` chỉ là chú thích ⇒ `evidence_url='not a uri at all'` HỢP LỆ |

## Giới hạn lời khai — không đổi

Chứng minh **BYTE tới consumer adapter**. **KHÔNG** tuyên bố model "đã hiểu"/"đã đọc"/"đã tuân thủ".

## Nền đã ĐO tại `3151371d` — reviewer đã xác minh ĐỘC LẬP, mọi số TRÙNG

| phép đo | giá trị |
|---|---|
| `launcher_test.py` @ base `27fb9de` | `154/154 (tổng 155, bỏ qua 1, hỏng 0)` |
| `launcher_test.py` @ head `3151371d` | `164/164 (tổng 165, bỏ qua 1, hỏng 0)` — delta **+10**, hỏng **0** |
| `--dot-bien` | `157/157 đạt (1 không đo được)` — `124_khi_chau_con_song` KHÔNG tính killed |
| `actionlint` | `rc=1`, ĐÚNG 1 finding `ops-don-ref.yml:106` — **đỏ sẵn, delta 0** |
| Windows parity | `windows-latest` **success** + `ubuntu-latest` **success**, 4 probe Windows-only chạy thật |

**Reviewer khai `KHÔNG ĐO ĐƯỢC` cho parity Windows** vì phạm vi cấm ra ngoài sandbox — nó **từ chối
rửa lời khai của điều phối thành phép đo của mình**. Ghi lại vì đó là hành vi đúng.

## Điều kiện DỪNG

- **S1** cần đường dẫn thứ NĂM ngoài write set ⇒ DỪNG, khai
- **S2** vượt 600 dòng thêm+xoá trên bốn tệp ⇒ DỪNG
- **S3** `origin/master` đi tiếp mà **CÓ chạm** một trong bốn đường write set ⇒ DỪNG. Master nhích
  mà không chạm write set thì KHÔNG phải lý do dừng — nền đã đo, xem bảng trên
- **S4** muốn sửa `launcher.py` hoặc schema ⇒ DỪNG: chúng đã RA khỏi write set, thuộc packet nối tiếp
- **S5** muốn khai một mục ĐẠT mà không có ca `rXX_` làm nó ĐỎ được ⇒ DỪNG
