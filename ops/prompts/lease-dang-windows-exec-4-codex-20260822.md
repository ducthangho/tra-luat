# Prompt EXECUTOR — `LEASE-DANG-WINDOWS` (#238), lượt **4** — neo đặc tả **r4**

Lease `lease-dang-windows-exec-4-codex-20260822`. **TIẾP TỤC** lượt 3 (không thay thế).

## Lượt này KHÁC MỌI LƯỢT TRƯỚC: bạn CHÉP một bản vá ĐÃ CHẠY, không nghĩ lại

Cross-review lượt 2 kết `can_sua`. **`P1-1` và `P1-2` của lượt 1 ĐÃ ĐÓNG** — reviewer kiểm lại
năm phép đo của phiên điều phối, 5/5 khớp, và bác hai nghi vấn của phiên điều phối bằng phép chạy
(`W8` có răng thật; tập gỡ rỗng của `W9`-cho-`W8` là kết quả ĐÚNG).

Còn đúng **một** việc: `P1-3`.

```
b0c8fb3 + X1 (bỏ mệnh đề `(nen or os.name) == "nt"`)
  -> lease_publish: 64/64 đạt; đã chạy=64, bỏ qua=8 ; rc=0     XANH
```

Tám ca `_chay_buoc_dang` biến mất **im lặng trên chân Ubuntu — chân LUÔN chạy**. Ba ca mới của
bạn (`t70` `t71` `t72`) đều ép `nen="nt"`, nên **không ca nào đo nhánh `posix`**.

## Nguồn sự thật — KIỂM BĂM, lệch ⇒ DỪNG

| gì | ở đâu | sha256 |
|---|---|---|
| đặc tả **r4** | `ops/specs/LEASE-DANG-WINDOWS-r4.md` | `11972e8ce5d543304b35b7239128af5130d11feaef378465461c3b2b649cc613` |
| verdict lượt 2 | `ops/reviews/lease-dang-windows-review-2-claude-verdict.md` | `e5dd9584d2e01172f71a0308c1d90eb0918d5b971af56cbb664d91438cf3c4a7` |
| r3 · r2 · r1 | `ops/specs/LEASE-DANG-WINDOWS-r3.md` · `-r2.md` · `.md` | `130b6d29…` · `d9da7705…` · `f555cbe1…` |

Hồ sơ ở nhánh `ops/pkg-windows` (chưa vào master): `git fetch origin ops/pkg-windows`.
Cây bắt đầu: `b0c8fb368d70f17bce5eb7e3d1fe02d810db8e19` trên `codex/lease-dang-windows-1`.

## Việc — MỘT việc

Chèn ngay **trước** `def main() -> int:` trong `ops/lease_publish_test.py`, **nguyên văn**:

```python
@ca
def t73_nen_posix_khong_duoc_bo_qua_ca_nao():
    def bo(): raise BoQuaNen(WORKFLOW_DANG, "dang")
    rc, out = _chay_main_meta(bo, "posix")
    bang(rc == 1 and "ĐỎ" in out and "bỏ qua=0" in out,
         f"nền posix mà vẫn bỏ qua được: rc={rc}, {out!r}")
```

**KHÔNG cải tiến, KHÔNG đổi tên, KHÔNG gộp vào ca khác.** `r4/Q13` nói thẳng lý do: điều kiện dừng
`E lần 4` đã kêu; người giữ kho cho đi tiếp **chỉ vì** lượt này không đặc tả phép dẫn xuất nào
mới. Cho bạn tự nghĩ lại chính là mở đường cho lần thứ năm.

Nếu bạn thấy ca này SAI hoặc thiếu — **DỪNG và nói**, đừng tự sửa. Đó là một phát hiện, không
phải một việc.

## Ngân sách

**≤ 3 tệp, ≤ 125 dòng THÊM so với `ba82b06f`.** Đã dùng **116**. Bản vá đo được **8** dòng thêm
theo `git diff --numstat` ⇒ **124**, dư **1**.

**Con số của verdict là "5 dòng" — đó là dòng MÃ LOGIC, không phải đơn vị ngân sách.** Đơn vị là
`git diff --numstat` (kể 2 dòng trống ngăn cách và dòng `f"..."` bị ngắt). Đừng lấy số 5 làm chuẩn.

## Cổng — ba số phải khớp CHÍNH XÁC

| đo gì | phải ra |
|---|---|
| bản vá nguyên vẹn | `73/73 đạt; đã chạy=73, bỏ qua=0`, `rc=0` |
| bản vá **+** `X1` | `64/65 đạt; đã chạy=65, bỏ qua=8`, `rc=1`, ĐỎ `t73_nen_posix_khong_duoc_bo_qua_ca_nao` |
| `X1` **không** kèm bản vá (đối chứng) | `64/64`, `rc=0` — **XANH**, đây là lỗ; tái hiện được thì mới biết ca vá đo đúng thứ ấy |

Lệch bất kỳ số nào ⇒ **DỪNG**, báo số đo được. **Không sửa ca cho vừa số.**

Cộng thêm, giữ nguyên từ lượt 3:
`actionlint` trên `ops-publish-lease.yml` rc=0 với `shellcheck` **có mặt** (kiểm nó có mặt TRƯỚC
khi tin actionlint) · cùng suite với ba biến GitHub đặt và `gh` VẮNG ⇒ `N/N` y hệt ·
`M1`–`M4` `A5` `D3`/`D4` và tám đột biến gỡ guard của `#227` **vẫn phải giết** ·
ba phản chứng `P1-1`/`P1-2`/`P1-2(b)` của lượt 3 **vẫn phải đỏ**.

## CẤM

`P2-5` (`except Exception: ly_do = ""` gộp ba nguyên nhân) — **lỗi thật, đã đo, CỐ Ý để ngoài**;
nó vào packet kế tiếp cùng `P2-3` mà nó làm nặng thêm. Bảy mục P2/P3 của verdict lượt 1: y vậy.
Cũng cấm sửa `ops/specs/**` và `ops/reviews/**`.

## Bạn KHÔNG chạy được `workflow_dispatch`

`W3′` đã đạt trên `b0c8fb3` (run `32563904221`: ubuntu `72/72 bỏ qua=0` · windows `64/64 bỏ qua=8`)
nhưng head sẽ đổi và **bằng chứng cũ không chuyển sang head mới**. Phiên điều phối chạy lại.

## Handoff — bắt buộc

`ops/handoff/lease-dang-windows-exec-4-codex-handoff.md`. Ngắn thôi: ba số của cổng trên, số
`git diff --numstat`, và `chua_do_duoc`. Nêu **TÊN CA đã đỏ THẬT**, không phải ca bạn nghĩ sẽ đỏ.

Nguồn sự thật là **tệp có băm trong kho**; prompt này chỉ là bản chiếu.
