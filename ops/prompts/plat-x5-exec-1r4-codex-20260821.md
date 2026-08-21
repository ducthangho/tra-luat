# Prompt BẤT BIẾN — Executor `PLAT-X5` (#206), lease **r4**, provider `codex`

Bạn là executor. Reviewer là `claude` (cross-provider, §8 thoả).

## 0. ĐỌC TRƯỚC MỌI THỨ — lượt này KHÁC ba lượt trước

Đây là **một lượt vá NHỎ, phạm vi ĐÓNG**, do người giữ kho nới thêm ĐÚNG MỘT attempt sau khi
cross-review lượt 2/2 trả `changes_requested`. Trần review **đã cạn** (2/2) — **sẽ KHÔNG có
lượt review chéo nào nữa cho packet này**. Nghĩa là:

- Không ai soi lại giúp bạn. Bằng chứng bạn tự dựng là bằng chứng cuối cùng.
- **Đừng mở rộng phạm vi.** Một dòng ngoài phạm vi là một dòng không ai review.
- Thấy thứ đáng sửa mà ngoài phạm vi ⇒ **KHAI, đừng sửa**.

## 1. Mỏ neo

| trường | giá trị |
|---|---|
| packet | `#206` · PR `#207` |
| head xuất phát | `2284b4657304d0229e95d1f64ebd0c22035d201d` |
| write set | **`ops/lease_publish_test.py` — ĐÚNG MỘT TỆP** |
| verdict phải đọc | `./VERDICT_LUOT_2.md` (sha256 `b317226602a48c1647efbd0b4f203cbd4e041817a489f9821654b1422f8b20d2`) |
| CI trên head xuất phát | run `32402136904`: cả hai job `success`, 0 bước hỏng |

## 2. ĐÚNG HAI VIỆC — không việc thứ ba

### Việc 1 — sửa LỜI KHAI của `GOI_WRAPPER_THUC_THI` cho khớp phép đo (finding P2)

Chú thích hiện tại (ngay trên định nghĩa regex) khẳng định:

> `Ngoài hai dạng canonical vẫn là một LỜI GỌI, và vì allowlist đang gác nghĩa vụ AL_VER, dạng
> ngoài danh sách phải ĐỎ chứ không được miễn.`

**Câu đó SAI theo phép đo.** Reviewer đo được: bước NHẬN DIỆN neo `^` và `\S*` không vượt được
khoảng trắng, nên bốn dạng dưới đây **không hề được coi là lời gọi** — chúng rơi vào `continue`,
tức **ĐƯỢC MIỄN** nghĩa vụ `AL_VER`, không phải bị từ chối:

```
env AL_X=1 bash ops/chay_lease_publish_test.sh          40/40 rc=0  (thiếu AL_VER mà cổng im)
bash -c 'bash ops/chay_lease_publish_test.sh'           40/40 rc=0
command bash ops/chay_lease_publish_test.sh             40/40 rc=0
bash ${{ github.workspace }}/ops/chay_…_test.sh         40/40 rc=0   ← có KHOẢNG TRẮNG trong ${{ }}
```

Đối chứng — hai dạng regex THỰC SỰ nhận diện được thì bị từ chối đúng thiết kế:

```
bash /đường/dẫn/tuyệt/đối/ops/chay_…_test.sh            39/40 ĐỎ t35
bash ${{github.workspace}}/ops/chay_…_test.sh           39/40 ĐỎ t35   ← KHÔNG khoảng trắng
```

**Việc phải làm:** viết lại chú thích cho **ĐÚNG bằng phạm vi đo được** — nói rõ nó neo `^`,
nhận đúng một token lệnh dẫn đầu, và **không vượt được khoảng trắng**; liệt kê bốn dạng đã ĐO
là lọt cùng hai dạng đối chứng bị bắt. Đây đúng khuôn đã dùng cho `t34` ở lượt trước.

**KHÔNG ĐƯỢC mở regex nhận diện.** Quyết định đảo nó thành danh sách CHO PHÉP thuộc packet
`#209`, đã được người giữ kho phân xử. Mở regex ở đây là lấn phạm vi.

**Kèm: khai NỢ CÓ TÊN** ngay tại chỗ, dạng `NỢ CÓ TÊN \`PLAT-X5-nhan-dien-loi-goi-wrapper\``,
nêu rõ: bốn dạng trên vẫn được miễn `AL_VER` ở tầng `t35`; hậu quả bị chặn ở tầng sau vì
`ops/cai_actionlint.sh` vẫn `loi 2` khi thiếu `AL_VER` bất kể cú pháp gọi; nợ này cùng họ với
việc đảo `t34` và thuộc `#209`. Viết theo đúng lối nợ `PLAT-X5-required-status-check` đã có.

### Việc 2 — `t25` không được báo oan CHÚ THÍCH ĐI SAU LỆNH (finding P3)

`goi.findall` quét **toàn bộ** dòng và không cắt phần sau `#`, nên hai dòng này bị đếm là lời
gọi thiếu `$NEO` ⇒ **ĐỎ GIẢ**:

```
run: echo ok # sh chay_lease_publish_test.sh
run: echo ok # xem bash ops/chay_lease_publish_test.sh
```

Ba dạng sau ĐÃ an toàn sẵn, **phải giữ nguyên an toàn**: chú thích nguyên dòng · `echo` nhắc
tên · `name:` của bước nhắc tên.

**Cạm bẫy bắt buộc xử lý:** `#` trong shell chỉ mở chú thích khi nó **đứng đầu dòng hoặc đứng
sau khoảng trắng**. `echo "a#b"` và `${{ github.event.issue.number }}#x` KHÔNG phải chú thích.
Cắt ngây thơ ở dấu `#` đầu tiên là **mở một lỗ mới**: một lời gọi thật đặt sau một `#` không
phải chú thích sẽ biến mất khỏi phép đếm — tức đổi một ĐỎ GIẢ lấy một XANH GIẢ, **đắt hơn hẳn**.
Nếu bạn không chắc cắt đúng thì **thà giữ nguyên báo oan** và khai nó thành nợ: fail-closed là
trạng thái chấp nhận được, fail-open thì không.

**Khai giới hạn** của cách cắt bạn chọn: `#` bên trong nháy đơn/kép, `#` sau dấu chéo ngược,
heredoc… — nói thẳng cái nào bạn xử được, cái nào không.

## 3. Bằng chứng BẮT BUỘC (không có review chéo để bù)

1. `python3 ops/lease_publish_test.py` ⇒ `rc=0`, `N/N` **hai số bằng nhau**, **không tụt dưới 40 ca**.
2. `actionlint .github/workflows/*.yml` ⇒ `rc=0` cả 5.
3. **Hai ca báo oan ở việc 2 phải trở thành `rc=0`** — đo trực tiếp, đọc `rc` từ tiến trình.
4. **Ba dạng vốn an toàn vẫn `rc=0`** (chống hồi quy theo chiều ngược).
5. **Một lời gọi THẬT thiếu `$NEO` vẫn phải ĐỎ `t25`** — đây là phản chứng chống "cắt quá tay":
   nếu cách cắt của bạn làm mất lời gọi thật thì ca này sẽ xanh, và đó là XANH GIẢ.
6. **Đột biến khoá việc 2:** gỡ phép cắt ⇒ ca mới phải ĐỎ 1/1. Không có đột biến thì không biết
   ca đang đo cái gì.
7. Mọi đột biến chạy trên **BẢN SAO TẠM** (`git archive … | tar -x` ra ngoài cây), KHÔNG sửa
   cây kho rồi khôi phục — `finally` không chạy khi bị giết.
8. Cây sạch cuối lượt: `git status --short` RỖNG. Commit, **KHÔNG push** (phiên điều phối đẩy).

## 4. Điều kiện DỪNG — dừng đúng lúc có giá hơn một bản vá nữa

- Cần sửa tệp **ngoài** `ops/lease_publish_test.py` ⇒ **DỪNG**, báo cáo, không tự nới.
- Thấy cách cắt `#` nào cũng có nguy cơ **fail-open** ⇒ **DỪNG việc 2**, giữ nguyên hành vi,
  khai thành nợ, **vẫn làm việc 1**. Báo rõ đã dừng vì lý do gì.
- Thấy một tiêu chí ở mục 3 là sai ⇒ DỪNG và nói ra, đừng tự đổi tiêu chí giữa đường.

## 5. Báo cáo cuối

In ra: hai việc đã làm gì · **số đo thật với `rc` đọc trực tiếp** · bảng phản chứng
(mỗi dòng: tên · rc · N/N · ca nào đỏ) · **phần còn hở đã khai tên** · SHA commit · trạng thái
cây. Nói thẳng thứ nào bạn **không** đo được — im lặng sẽ bị đọc thành đã kiểm.
