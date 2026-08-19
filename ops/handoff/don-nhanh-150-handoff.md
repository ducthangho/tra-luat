> # ⛔ BÀN GIAO NÀY ĐÃ ĐÓNG — 19-08-2026. ĐỪNG LÀM THEO.
>
> **PR #150 đã merge** (`6d8fce5`, `2026-08-19T09:08:57Z`). Lượt 6 **đã chạy**, và sau nó
> còn một lượt 7 nữa — cả hai đã có verdict + biên nhận trong `ops/reviews/`. Mọi việc mà
> trang này giao cho "phiên mới" **đã xong**.
>
> **Lệnh ĐẦU TIÊN của trang này nay GÃY**, và đó là điều đáng học chứ không phải một chỗ
> lỗi thời tầm thường: nó `git fetch origin ops/don-nhanh-giu-base-pr`, mà nhánh ấy **đã bị
> xoá khi PR merge**. Ai chạy theo sẽ dừng ngay ở dòng đầu và không có cách nào biết phần
> còn lại đúng hay sai. Đúng bài học `CLAUDE.md` đã trả giá: *"thứ định danh tệp là BĂM,
> không phải tên nhánh — tên nhánh là thứ trôi và bị xoá."* Trang này neo theo **tên nhánh**
> ở khắp nơi, nên nó hết hạn đúng vào lúc merge. Muốn đọc các tệp nó nhắc tới thì tra bằng
> **SHA** (`git show 99e9383:…`), đừng tra bằng tên nhánh.
>
> **Ba việc "còn nợ chủ kho" ở cuối trang — trạng thái đo được ngày 19-08:**
>
> 1. *Xoá 9 nhánh remote* — **XONG**. Đo lại: `git branch -r --merged origin/master` trả về
>    rỗng (đối chứng dương: lệnh vẫn liệt kê `origin/master`, nên nó không im vì hỏng), và
>    cả 9 tên trong danh sách đều không còn. `mission/76/integration` — nhánh trang này và
>    PR #179 nói **tuyệt đối không được xoá** vì là base của 5 PR đang mở — **vẫn còn**.
> 2. *Cấp uỷ quyền mới để land bằng `same_provider_approved`* — **KHÔNG CÒN Ý NGHĨA**: chủ
>    kho đã tự merge #150, nên không còn quyết định nào chờ uỷ quyền. Nói cho ĐÚNG hai tệp,
>    vì suýt nữa dòng này gộp chúng làm một: `ops/uy-quyen-150-same-provider-20260817.yaml`
>    **VẪN CÒN** trong kho, neo `05568de`, tự ghi `trang_thai: HET_HIEU_LUC` và
>    `authorization_url: pending-owner-post` — tức nó chưa từng được chủ kho đăng công khai.
>    Tệp bị **gỡ** ở `ec17a83` là một tệp **KHÁC**, `ops/uy-quyen-150-land-20260819.yaml`,
>    do agent tự soạn; chính thông điệp commit gọi đó là *"LỖI THAO TÁC của tôi"*. Đừng đọc
>    tệp còn lại thành một uỷ quyền đang có hiệu lực: nó tự khai là không.
> 3. *Chạy một lượt `codex` trên SHA đã land* — **CÒN MỞ**. Đây là lỗ hổng **bằng chứng**,
>    không phải lỗ hổng mã: bảy lượt review của #150 đều `same_provider_approved`, chưa lượt
>    nào là cross-provider, trong khi §8 đòi cross-provider cho phạm vi workflow. Verdict
>    lượt 7 đo được đường ấy mở lại **2026-08-20 06:23** (quota, không phải auth chết).
>
> **Bảng "SÁU LƯỢT" bên dưới nay thiếu**: đã có **bảy** lượt. Verdict lượt 4 và 5 — trang
> này viết khi chúng còn nằm ngoài kho — nay **đã ở trong** `ops/reviews/`, kèm cảnh báo
> rằng dụng cụ đo của chúng đã mất. Xem `ops/reviews/README.md`.
>
> Giữ trang này thay vì xoá: nó là bản ghi của một đợt làm việc thật, và chính chỗ nó gãy
> là bằng chứng cho bài học neo-theo-băm ở trên.

# BÀN GIAO — PR #150 `don-nhanh`, sang phiên mới

Chủ kho: *"Cấp lượt 6. Sang phiên mới thực hiện tiếp"* (17-08-2026).

## Việc đầu tiên của phiên mới

```bash
git fetch origin ops/don-nhanh-giu-base-pr
git show origin/ops/don-nhanh-giu-base-pr:ops/leases/don-nhanh-base-review-6-claude-20260817.yaml
```

Lease lượt 6 **đã cấp và đã đẩy**, `lease_publish check` rc=0. Việc còn lại là **chạy nó**.

Lệnh chạy (đường đã dùng cho lượt 3-5, có bằng chứng chạy được):

```bash
S=<scratchpad>; R=$S/wt-rv6
git worktree add --detach "$R" 99e9383e9ff60bb8850f41242beb607808a821e9
git -C "$R" show origin/ops/don-nhanh-giu-base-pr:ops/prompts/don-nhanh-base-review-6-claude-20260817.md > "$R/nhiem_vu.txt"
sha256sum "$R/nhiem_vu.txt"   # phải = 84f32f22e150b2464daade9d2df1ec1ec39f1f6cad24a3cc0c9413314943e42f

export TMPDIR=/dev/shm
python3 .claude/dev/launcher.py run \
  --run-root "$S/runs" --name claude-fable5-review-150-l6 \
  --workspace "$R" \
  --expected-repo ducthangho/tra-luat \
  --expected-root-commit 394e93468fc8d84ec20938e6df8fb7ab72b2cc37 \
  --expected-head 99e9383e9ff60bb8850f41242beb607808a821e9 \
  --prompt-file "$R/nhiem_vu.txt" \
  --expected-prompt-sha256 84f32f22e150b2464daade9d2df1ec1ec39f1f6cad24a3cc0c9413314943e42f \
  --deadline-utc 2026-08-18T17:45:00Z \
  -- claude -p "Doc tep {PROMPT_FILE} va thuc hien dung theo do. Tra loi theo DUNG dinh dang o cuoi tep do." \
     --model claude-fable-5 --effort max --permission-mode auto
```

**Sau khi chạy, ĐO chốt read-only** (đừng tin cờ quyền):
`git -C "$R" rev-parse HEAD` phải vẫn `99e9383…`, và `git -C "$R" status --porcelain` chỉ
được còn `?? nhiem_vu.txt`.

## Trạng thái

| | |
|---|---|
| PR | #150, nhánh `ops/don-nhanh-giu-base-pr`, base `master` |
| head lúc bàn giao | `99e9383e9ff60bb8850f41242beb607808a821e9` |
| master lúc bàn giao | `1a6aedf6b92ff271bf07a8b9deee2f83d430ed49` |
| bộ test | `21/21` (pwsh 7.4.6, `TMPDIR=/dev/shm`, ~15s) |
| cổng | eol ok=true checked=398 · lease_publish 31/31 · release-verify ok=true · golden rc=0 · `file_count` 179 |

> **Đính chính một con số — và bài học đắt hơn con số.**
>
> Thông điệp commit `9a133a4` ghi `eol … checked=400`. Người vá **gõ số trước khi đo**; phép
> đo lúc ấy in **398**. Đó là lỗi thứ nhất, tầm thường.
>
> Lỗi thứ hai mới đáng ghi: `398` cũng **không** mô tả cây của commit ấy.
> **`eol_policy.py --all` đọc INDEX của git**, nên đo *trước* `git add` là đo một cây
> **khác** với cây sắp commit — ba tệp `ops/` mới (lease 6, prompt 6, bàn giao) chưa vào
> index nên không được đếm. Đo lại sau khi đã stage: **`checked=401`**.
>
> Tức một con số có thể sai theo **hai kiểu độc lập**: sai vì đoán, và sai vì đo đúng lệnh
> nhưng **sai thời điểm**. Kiểu thứ hai nguy hiểm hơn vì nó *có* phép đo đằng sau và trông
> hoàn toàn đáng tin.
>
> **Nếp rút ra:** mọi số cổng phải ghi kèm **neo** — đo ở SHA/trạng thái index nào. Số đúng
> cho commit `4a22cec` là `checked=401`; số `398` đúng cho cây **trước khi stage** ba tệp ops.
> Commit `9a133a4` đã đẩy nên không sửa tại chỗ; sửa lịch sử đã công bố đắt hơn nhiều so với
> một dòng đính chính.

## SÁU LƯỢT, SÁU LẦN TÌM RA THỨ THẬT — đọc bảng này trước khi nghĩ "chắc sạch rồi"

| lượt | reviewer | tìm ra |
|---|---|---|
| 1 | codex | `gh` thoát khác 0 mà in JSON hợp lệ ⇒ fail-close mở toang, **xoá thật** |
| 2 | codex | `2>&1` trộn stderr vào JSON ⇒ thao tác hợp lệ **bị từ chối oan** (hồi quy do bản vá lượt 1) |
| 3 | claude | đếm **số dòng thô** thay vì nội dung đã tách ⇒ đột biến sống sót |
| kiến trúc | claude | `giu_nguyen` (giữ `gh`); phát hiện bằng chứng MCP của người vá **chết trong 12 phút** |
| 4 | fable-5 max | `-ge`→`-eq` và so-sánh-**chuỗi** đều sống 18/18; mặc định `TranPR` không được ghim |
| 5 | fable-5 max | `gh` giả **mù với argv** ⇒ 4 đột biến sống 21/21, một con **tái tạo đúng lỗ gốc của PR** |

**Ba lượt gần nhất tìm ra lỗi nằm trong chính phần TEST.** Delta lượt 6 cũng thuần test.
"Thuần test" ở kho này **không** đồng nghĩa "ít rủi ro".

## Hai thứ tuyệt đối đừng làm

1. **Đừng ghi `cross_approved`** cho bất kỳ lượt `claude` nào. `codex` hết quota; §8 đòi
   cross-provider cho phạm vi workflow và #150 sửa `.github/workflows/ci.yml`. Mọi lượt từ
   số 3 trở đi là `same_provider_approved` và **không cấp điều kiện land**.
2. **Đừng trỏ lại uỷ quyền cũ sang SHA mới.** `ops/uy-quyen-150-same-provider-20260817.yaml`
   neo `05568de`; head đã đổi hai lần từ đó nên nó **hết hiệu lực** (§9). Trỏ lại là agent
   tự nới uỷ quyền sang một cây chủ kho chưa từng thấy — §2 cấm. Chủ kho phải cấp lại.

## Quy ước phải giữ

- **Verdict là NGUYÊN VĂN, neo băm, không sửa.** Chép từ `runs/<short_id>/stdout.log`, đối
  chiếu `diff -q`. Đính chính sống ở `*.receipt.yaml`, và caveat phải **nâng lên bảng cảnh
  báo** của `ops/reviews/README.md` (`t27` đỏ nếu thiếu).
- **Hai commit:** verdict đứng riêng trước, rồi biên nhận + mục lục — để `evidence_url` neo
  được vào một commit đã chứa tệp.
- **Lease của lượt N không nằm trong cây neo ở SHA của lượt N** (nó commit sau). Prompt phải
  nêu đích danh `git show origin/<nhánh>:ops/leases/…`. Nợ đã khai, chữa gốc chưa làm.
- **Merge, không squash** — `evidence_url` của các biên nhận neo vào `e872e98`.
- Ghi ngược `posted_comment_id` sinh commit trên nhánh ⇒ **merge, đừng rebase**.

## Bẫy môi trường đã trả giá

- `pwsh` không cài sẵn. Tải 7.4.6 linux-x64; **tarball giải nén ra `pwsh` thiếu bit exec**
  (rc=126) ⇒ `chmod +x`. **Không** phải `/dev/shm` noexec — reviewer lượt 4 chẩn đoán nhầm
  hướng này rồi phải sửa lại.
- `/dev/shm` **bị xoá khi phiên khởi động lại**: mất cả `pwsh` lẫn `actionlint`. Một lượt đo
  từng trả `rc=127` với đầu ra **rỗng** — trông y hệt "chạy xong sạch". **Kiểm công cụ có mặt
  trước khi đọc bất kỳ con số nào.**
- `TMPDIR=/dev/shm` (sandbox khoá `/tmp`).
- `release-verify --strict` đỏ trong worktree review vì `nhiem_vu.txt` của harness nằm trong
  `extra_files`; đo trên `git archive HEAD` thì xanh.
- `tl selftest` chết ở `import cryptography` (`pyo3_runtime.PanicException`) — **nợ đã khai,
  sáu lượt đều thế, nền master hỏng y hệt ⇒ delta 0**. Nối `tail` sau pipeline sẽ nuốt rc.
- Phiên web **không xoá được ref** và **không đẩy được tag** (proxy 403). Đường duy nhất là
  `ops-don-ref.yml`.

## Việc còn nợ chủ kho

1. **Xoá 9 nhánh remote** bằng `.\scripts\don-nhanh.cmd -Xoa` trên máy Windows — đây là việc
   GỐC khởi đầu cả chuỗi này và **vẫn chưa xong**. Làm được ngay, không cần chờ #150.
2. **Cấp uỷ quyền mới** neo SHA cuối cùng, nếu muốn land bằng `same_provider_approved`.
3. Khi `codex` có quota: chạy một lượt **trên SHA đã land** — đóng lỗ hổng *bằng chứng*,
   không phải lỗ hổng mã.

## Nợ kỹ thuật còn mở

`-BoQuaLopPR` không kiểm gì · phụ thuộc `gh` · `.cmd` chỉ chạy Windows · `tl selftest` chưa
ai đo · lease không nằm trong cây được review · hành vi phân trang **thật** của `gh` ở kho
>1000 PR chưa ai đo · hằng `999` của `t20` không tự canh (lượt 5 khuyên **không** vá).
