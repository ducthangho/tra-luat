# Prompt BẤT BIẾN — Reviewer chéo `PLAT-X4`, lượt **2/2**, provider `codex`

Read-only với KHO: **không commit, không push, không đổi HEAD.**

**Bố cục sandbox** — bạn đang đứng ở thư mục gốc sandbox, KHÔNG phải trong kho:

```
./nhiem_vu.txt          prompt này
./VERDICT_LUOT_1.md     verdict lượt 1 của chính bạn — NGUYÊN VĂN
./EVIDENCE.md           số đo của executor, đã đo lại độc lập
./diff.patch            diff base..head (TOÀN BỘ packet)
./diff_rev2.patch       diff CHỈ phần vá lượt này (d0acd79f..head)
./numstat.txt           numstat base..head
./PROTOCOL_TRICH.md     bản sao docs/PROTOCOL_DA_PHIEN.md
./bin/actionlint        actionlint 1.7.7 (NGOÀI cây kho)
./kho/                  BẢN SAO KHO — `git worktree` tách rời tại exact head, GHI ĐƯỢC
```

Mọi lệnh git chạy dạng `git -C kho ...`; lệnh test chạy sau khi `cd kho`. Đưa actionlint lên
PATH: `export PATH="$PWD/../bin:$PATH"` (từ trong `kho/`).

**CHỐT SẠCH CÂY:** `git -C kho status --short` phải **RỖNG** cả trước lẫn sau lượt, và
`git -C kho rev-parse HEAD` không đổi. Đột biến chạy trên **bản sao tạm**, đừng chạm cây.

**Không đọc ra ngoài thư mục sandbox này.**

## 1. Mỏ neo

| trường | giá trị |
|---|---|
| packet | `#203` — `[WP PLAT-X4]` |
| PR | `#205` |
| exact head phải review | `1d37861ec419d1c3a25cfbdb1b07689bbf42504c` |
| base (merge-base với master) | `909d3e171d7b37a734c1100b3fdc3c48e1b66d19` |
| head lượt 1 (đã cũ) | `d0acd79f8bf22acf12d226283f176f2e7cc81508` |
| write set | `ops/lease_publish_test.py` · `ops/cai_actionlint.sh` · `.github/workflows/ci.yml` · `.github/workflows/ops-publish-lease.yml` |
| vòng | **2/2 — VÒNG CUỐI trong trần canon** |

`git -C kho rev-parse HEAD` phải bằng đúng chuỗi trên. Lệch ⇒ dừng, khai `stale head`.

**Vòng cuối nghĩa là gì:** `changes_requested` ở lượt này **không** mở vòng 3 — nó đưa packet
sang Review Rescue Checkpoint để người giữ chọn Stable Slice / Remediation Slice / revision.
Đừng vì thế mà hạ chuẩn: một finding thật ở vòng cuối vẫn đáng hơn một `approved` sai.

## 2. Việc thứ nhất — ĐÓNG CHƯA? Đo, đừng đọc

Lượt 1 bạn ra **3 finding P2**. Executor khai đã đóng cả ba. Dựng lại **đúng phản chứng của
bạn** trên bản sao tạm và xem chúng có ĐỎ không:

1. **`t34` khớp chuỗi installer.** Phản chứng cũ: thay `run: bash ops/cai_actionlint.sh`
   bằng `run: echo ops/cai_actionlint.sh` ở cả hai workflow ⇒ trước đây `35/35` rc=0.
   Nay phải ĐỎ. Executor nói đã đảo thành **danh sách CHO PHÉP** `GOI_CANON`.
2. **`AL_VER` nhận `1x.2y.3z`.** Phải `rc=2`. Thử thêm các dạng bạn nghĩ ra.
3. **Không kiểm checksum.** Nay có `bam_ghim` + `bam_cua`. Kiểm 4 trạng thái và mã thoát:
   không có băm ghim `8` (và phải DỪNG TRƯỚC KHI TẢI), thiếu công cụ băm `8`, không khớp `9`,
   khớp `0`.

Ba mục trên **đóng chưa đủ để approve**. Mục 3 dưới đây mới là chỗ đáng soi.

## 3. Việc thứ hai — BẢN VÁ CÓ MỞ LỖ MỚI KHÔNG?

`diff_rev2.patch` là phần thêm của lượt này: **+~160 dòng script, +~470 dòng test**. Bản vá
lớn hơn lỗi nó chữa, và kho này đã trả giá đúng kiểu đó ("vá một lỗ mà mở lỗ khác trong cùng
hàm"). Executor **tự nêu** các hướng dưới đây vì nghi chúng — hãy đo, và đừng dừng ở đây:

1. **`t34` soi theo TỆP hay theo JOB?** Nếu nó chỉ đòi "trong tệp workflow này có một bước
   thực thi installer", thì đặt installer ở **job A** và bộ test ở **job B** sẽ qua — trong khi
   job B chạy trên runner KHÁC và không có `actionlint`. Đó đúng là regression `32351892214`
   quay lại qua một cửa khác. **Thử đi.**
2. **`GOI_CANON` — quá chặt hay quá lỏng?** Nó so NGUYÊN KHỐI phần lệnh. Một bước hợp lệ có
   thêm `set -e`, thêm `env`, đổi `shell:`, hay gọi qua `bash -lc` thì sao — bị từ chối oan?
   Ngược lại, có cách viết nào **không thực thi** mà vẫn khớp nguyên khối không?
3. **`AL_SHA256` là cửa hậu?** Nó **ghi đè** băm ghim. Ai đặt được biến môi trường thì đặt
   được băm của gói mình mang tới ⇒ cổng băm vô hiệu. Hỏi: trong mô hình đe doạ của workflow
   này (`contents: write` + `issues: write`), ai đặt được env? Nếu câu trả lời là "chỉ người đã
   sửa được workflow" thì mức rủi ro khác; **nói rõ kết luận và căn cứ**, đừng bỏ lửng.
4. **`( cd "$AL_DICH" && tar ... )` — mã thoát có truyền ra không?** Subshell + `||` + `set -e`
   là chỗ kinh điển nuốt rc. Đo bằng một gói hỏng thật.
5. **`DUOI_GOI="${TEN_GOI##*.}"`** khi tên tệp **không có dấu chấm** thì bằng cả tên. Ra
   `goi_giai_nen.<cả-tên>`. Có ca nào hỏng vì đó không?
6. **Bước `cp` mới**: `AL_DICH` không ghi được, đĩa đầy, `TEN_GOI` là symlink trỏ ra ngoài,
   hoặc `AL_GOI` trỏ đúng vào `$AL_DICH/goi_giai_nen.*` — mỗi ca ra mã thoát nào?
7. **`t36`/`t38` rẽ nhánh theo nền.** Executor đã tự sửa một nhánh "bỏ qua âm thầm" trong `t38`
   (harness này **không có** cơ chế bỏ qua — `return` sớm vẫn được đếm ĐẠT). Hỏi tiếp: hai ca
   ấy **thật sự đo** trên nhánh POSIX chứ? Và còn ca nào khác trong tệp có `return` sớm mà vẫn
   được đếm ĐẠT không? Đây là bệnh `t24` của kho.
8. **`t35`/`t36` nay TỰ CẤP `AL_SHA256`** cho gói giả — tức chúng **cố ý đi vòng qua** cổng băm.
   `t37` sinh ra để bù. Hỏi: `t37` có phủ hết phần hai ca kia bỏ qua không, hay còn khe?
9. **Băm ghim tính từ chính bản tải về lúc ghim.** Executor khai thẳng giới hạn này. Xác nhận
   lời khai ấy đúng và nêu mức rủi ro — đừng nhắc lại như một finding mới nếu nó đã được khai.

## 4. Bằng chứng nền phải kiểm

- `ops/lease_publish_test.py` ⇒ rc=0, `N/N` hai số BẰNG NHAU, không tụt dưới 38.
- `actionlint .github/workflows/*.yml` ⇒ rc=0 cả 5.
- `git -C kho diff --name-only 909d3e17..HEAD` ⇒ **đúng 4 tệp** write set.
- `doc-claims-check --strict` rc=2 — executor khai **ĐỎ SẴN** trên base. Đo nền trước khi nghi.

`rc` đọc **trực tiếp** từ tiến trình. Nối `| tail`/`| head` sau lệnh là **nuốt mã thoát**, và
lỗi ấy đã xảy ra thật hai lần trong đợt này — một lần làm cả bảng đo `AL_VER` báo `rc=0` sai.

## 5. Windows — đọc kỹ, đây là chỗ dễ kết luận nhầm

Packet này đã đi qua **ba** lượt Windows, và bảng bước nói nhiều hơn màu của job:

| head | bước 10 `cài actionlint` | bước 11 `lease-publish selftest` | job |
|---|---|---|---|
| `d0acd79f` | success | **failure** (lỗi `tar`) | failure |
| `22236f5b` | **failure** (lỗi băm) | **skipped** | failure |
| `2348710b` | success | **success** | success |

Chú ý dòng giữa: bước 11 **`skipped`**, không phải chạy-rồi-qua. Nên bản vá `tar` chỉ có bằng
chứng Windows từ `2348710b` trở đi. `get_job_logs` chỉ trả phần ĐUÔI log nên **không đọc được
`N/N` của Windows** — nếu bạn tìm được đường đọc, nói ra; nếu không, đừng khai là đã đọc.

## 6. Cách trả lời

Mỗi finding bắt buộc bốn phần: (a) **bằng chứng đo được** (lệnh + kết quả nguyên văn);
(b) mức P1/P2/P3; (c) **invariant nào bị cắt**; (d) **gợi ý vá** cụ thể. Không chạy được thì
ghi thẳng là **giả thuyết**, đừng trình bày như phép đo.

Nếu một hướng ở §3 bạn đo và thấy **không có vấn đề**, hãy nói rõ đã đo và kết quả — một hướng
im lặng đọc giống hệt một hướng chưa ai thử.

Kết ở dòng cuối, đúng một trong ba, viết nguyên văn:

```
VERDICT: approved
VERDICT: changes_requested
VERDICT: blocked
```

Kèm ngay dưới dòng `Reviewed commit: <băm bạn ĐO ĐƯỢC bằng git -C kho rev-parse HEAD>`.
