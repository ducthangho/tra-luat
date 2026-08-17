# Cross-review lượt 5 — PR #150. PHẠM VI ĐÓNG BĂNG. MỘT TỆP.

Bạn là REVIEWER, provider **`claude`** (`claude-fable-5`, effort `max`), chạy trong một
**tiến trình HOÀN TOÀN MỚI** — không có ngữ cảnh nào của phiên người vá. **CHỈ ĐỌC**: không
sửa tệp trong kho, không commit, không push. Đột biến chạy trên bản sao tạm.

## LƯỢT NÀY KHÔNG ĐỦ MỨC ASSURANCE ĐỂ LAND

§8: workflow / security path / credential boundary / dispatcher / migration / LIVE adapter
**phải** có cross-review khác nền tảng hoặc human review có audit; `same_provider_approved`
*"một mình không thay mức assurance bắt buộc"*. #150 sửa `.github/workflows/ci.yml`.

`codex` **đã hết quota** — không còn đường cross-provider cho lượt này. Chủ kho chấp nhận
sai lệch, có ghi. **Đừng viết gì hàm ý "đã đủ điều kiện land".**

Bạn cùng nhà cung cấp với người vá ⇒ **cùng thiên kiến**. Số đo của chuỗi này: **năm lượt,
năm lần tìm ra thứ thật**, và **hai lượt gần nhất tìm ra lỗi nằm trong chính phần TEST** chứ
không phải trong mã. Delta lần này **thuần test**. Nếu bạn không tìm được gì, khả năng cao
nhất không phải là "sạch" mà là "đang nhìn theo đúng cách người vá đã nhìn".

## Neo

```
git rev-parse HEAD    # phải = 12dd16ea6d92a177898a78fb9a547bda1d601dbb
```

Lease của lượt này **không** có trong cây bạn checkout (commit sau). Đọc bằng:

```
git show origin/ops/don-nhanh-giu-base-pr:ops/leases/don-nhanh-base-review-5-claude-20260817.yaml
```

## Phạm vi đóng băng — ĐÚNG MỘT TỆP

```
git diff 05568de6ad054a5f0c9991ecac7e38805d1227c3..HEAD -- scripts/
```

`scripts/don-nhanh_test.ps1` (+56). **`don-nhanh.ps1` KHÔNG đổi.** Delta toàn bộ còn có
`ops/uy-quyen-150-same-provider-20260817.yaml` và hồ sơ lease/prompt — không phải mã ⇒
`## Nợ khai báo`.

## Bối cảnh: lượt 4 tìm ra HAI đột biến sống sót, đây là bản vá cho chúng

**F1 (P2)** — cặp `t17`/`t18` chỉ ghim biên **từ phía dưới**, nên hai đột biến làm chốt
**fail-open** sống sót 18/18:
- `M12` `-ge` → `-eq`: chỉ chặn khi đếm **bằng đúng** trần. Fail-open thật, đo được:
  `-Xoa -TranPR 0` với 1 PR mở ⇒ rc=0 và **xoá thật**.
- `M16` so sánh **chuỗi**: `"10" -ge "9"` là `$false` ⇒ vượt trần mà vẫn cho qua.

**F2 (P3)** — mặc định `TranPR = 1000` không được ghim: `M13` (→200) và `M13b` (→3) đều sống
sót 18/18, vì **mọi ca đa-PR đều truyền `-TranPR` tường minh**.

**Bản vá** (18 → 21 ca):
- `t19` — 10 PR, `-TranPR 9` ⇒ rc=13. Nhắm giết **cả M12 lẫn M16 trong một ca**.
- `t20` — 999 PR, **không** truyền `-TranPR` ⇒ rc=0, vẫn xoá.
- `t21` — 1000 PR, **không** truyền `-TranPR` ⇒ rc=13.
- helper `Nhieu-PR` sinh N PR giả, base đều `master`.

## NĂM câu, tất cả ĐO ĐƯỢC

**1. Ba ca mới có THẬT SỰ giết bốn đột biến kia không.** Tự dựng lại `M12` `M16` `M13`
`M13b` trên bản sao tạm và chạy. Người vá báo: M12 ⇒ 20/21 (đỏ t19) · M16 ⇒ 19/21 (đỏ
t19+t20) · M13 ⇒ 20/21 (đỏ t20) · M13b ⇒ 20/21 (đỏ t20). **Đừng tin, chạy.**

**2. `t19` có đo ĐÚNG HAI thứ nó khai không.** Nó khai giết cả `-eq` lẫn so-sánh-chuỗi bằng
cặp 10/9. Kiểm: 10/9 có thật là cặp **nhỏ nhất** phân biệt số học với chuỗi không? Có cặp
nào `t19` **không** phân biệt được không (ví dụ đột biến so `[string]` nhưng pad số)?

**3. `t20`/`t21` ghim mặc định — ghim CHẶT tới đâu.** Chúng ghim 1000 từ hai phía. Nhưng:
một đột biến đổi mặc định thành **1001** thì sao? **999**? Có đột biến nào đổi mặc định mà
cặp này **không** bắt được không? Nếu có, cặp ấy ghim lỏng hơn lời khai.

**4. HELPER `Nhieu-PR` LÀ MÃ MỚI TRONG BỘ TEST — nó có tự đúng không?** Nó sinh N PR với
`baseRefName = 'master'`. Hỏi: `t20` xoá được `ops/rac` nghĩa là danh sách PR đọc **được
thật**, hay nghĩa là nó đọc **rỗng** rồi rơi vào đường khác? Phân biệt hai thứ đó bằng phép
đo. **Một helper sinh sai dữ liệu làm cả ba ca xanh vì lý do sai** — đó đúng là hình dạng
lỗi mà lượt 3 đã bắt (`[string]$X = $null` làm `gh` giả in rỗng ở khắp nơi, ba ca xanh vì lý
do sai).

**5. Đột biến sống sót thứ ba.** Lượt 4 tìm ra hai. Có cái nữa trong tệp này không? Gợi ý,
không giới hạn: sửa `Nhieu-PR` trả `N-1` phần tử; đổi `1..$So` thành `0..$So`; bỏ
`-TranPR` khỏi `t19`; đổi 999→998 trong `t20`.

## Số người vá báo — kiểm lại

```
don-nhanh_test  21/21   pwsh 7.4.6, TMPDIR=/dev/shm, ~14s
M12  -> 20/21 do t19        M16  -> 19/21 do t19+t20
M13  -> 20/21 do t20        M13b -> 20/21 do t20
M10 18/21 · M11 19/21 · M14 18/21   (dot bien CU, van chet)
NANG mac dinh -> 2000  -> 20/21 do t21   (do loi khai trong chu thich t21)
eol ok=true checked=396 · lease_publish 31/31 · release-verify ok=true · golden rc=0
file_count 179
```

**Môi trường, đã trả giá — đọc trước khi đọc bất kỳ con số nào:**
- `pwsh` KHÔNG cài sẵn. Tải PowerShell 7.4.6 linux-x64 từ GitHub release. **Tarball giải nén
  ra `pwsh` THIẾU BIT EXEC** (rc=126) — phải `chmod +x`. Không phải `/dev/shm` noexec.
- Đặt `TMPDIR=/dev/shm` (sandbox khoá `/tmp`).
- `/dev/shm` **bị xoá khi phiên khởi động lại** — một lượt đo của người vá trả `rc=127` với
  đầu ra **rỗng**, trông y hệt "chạy xong sạch". **Kiểm công cụ có mặt TRƯỚC khi đọc số.**
- `release-verify --strict` trong worktree review sẽ ĐỎ vì `nhiem_vu.txt` (tệp harness đặt
  vào, untracked) nằm trong `extra_files`. Đo trên `git archive HEAD` ra cây sạch thì xanh.
- `claude` báo "Ignoring N permissions.allow entries… not trusted" — bình thường.

Thiếu `pwsh` ⇒ khai **KHÔNG ĐO ĐƯỢC**, đừng suy từ đọc code.

## Nợ đã khai — KHÔNG nêu lại trừ khi lời khai SAI

`-BoQuaLopPR` không kiểm gì · phụ thuộc `gh` · `.cmd` chỉ chạy Windows · `tl selftest` KHÔNG
ĐO ĐƯỢC (chết ở `import cryptography`, `pyo3_runtime.PanicException`; bốn lượt trước không ai
xác nhận được) · lease không nằm trong cây được review · hành vi phân trang THẬT của `gh` ở
kho >1000 PR chưa ai đo · `gh` bị proxy container chặn cả REST lẫn GraphQL.

## MỖI FINDING PHẢI KÈM GỢI Ý CÁCH VÁ — yêu cầu MỚI từ lượt này

Chủ kho yêu cầu reviewer nêu luôn **nên vá thế nào**. Không phải để người vá làm theo mù,
mà để cái giá của bản vá được cân **ngay lúc phát hiện** thay vì một lượt sau.

Với **mỗi** mục trong `## Findings`, thêm khối `**Gợi ý vá:**` gồm bốn phần:

1. **Vá ở đâu** — tệp + hàm/ca cụ thể, và **tại sao ở đó** chứ không phải chỗ khác.
2. **Vá thế nào** — mô tả thay đổi. Đoạn mã ngắn thì được, nhưng **đừng viết cả bản vá**:
   viết hộ cả bản vá là bạn tự biến mình thành người vá, và lượt sau bạn sẽ đang review
   chính đề xuất của mình.
3. **Ca test khoá nó** — phép thử nào làm bản vá ấy có răng, và **đột biến nào phải chết**
   sau khi vá. Không nêu được ca test thì nói thẳng là chưa nghĩ ra.
4. **Bản vá này có thể đẻ ra gì** — hình dạng lỗi nào nó có nguy cơ mở. Kho này đã có
   **hai lần liên tiếp** bản vá đẻ ra lỗi mới trong cùng một hàm; câu hỏi ấy không phải
   nghi lễ.

**Xếp hạng gợi ý:** nếu có nhiều đường vá, nêu đường **RẺ NHẤT mà vẫn đóng lớp**, rồi nói
đường đắt hơn mua thêm được gì. Nếu bạn cho rằng **không nên vá** (finding thật nhưng cái
giá lớn hơn cái lợi) thì nói thẳng — "khai thành nợ" là một gợi ý hợp lệ.

**Gợi ý là GỢI Ý, không phải chỉ thị.** Người vá được phép làm khác, và nếu làm khác thì
lượt sau bạn **không** được coi "đã làm đúng theo gợi ý của tôi" là bằng chứng đúng — vẫn
phải đo.

## Định dạng trả lời

```
verdict: approve | changes_requested | do_not_land
reviewed_sha: <sha40 bạn đã thật sự đọc>
assurance: same_provider_approved      # BẮT BUỘC dòng này

## Danh sách đóng được của lượt 4

F1 và F2: ĐÓNG hay CHƯA, kèm phép thử đã chạy cho từng đột biến.

## Findings

CHỈ nhận: hồi quy · lỗ an ninh MỚI · đột biến SỐNG SÓT — trong ĐÚNG tệp `don-nhanh_test.ps1`.
MỖI mục kèm khối `**Gợi ý vá:**` bốn phần như trên.

## Nợ khai báo

Mục nào ở đây mà bạn thấy đáng vá thì cũng kèm gợi ý — ngắn hơn cũng được.

## Phép đo đã chạy
```

Nguồn có thẩm quyền là tệp lease trên **đầu nhánh**.
