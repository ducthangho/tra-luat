Đo xong. Cây review sạch, `HEAD` không đổi (`edc1906c`).

```
KET_LUAN: can_sua
reviewed_sha: edc1906cf01fcceb15c646e1fdc4fcd8957644ed
```

Đặc tả kiểm băm TRƯỚC: r2 `d9da7705…` ✓ · r1 `f555cbe1…` ✓. `W3′`/`W4`/`W5` **đạt, có bằng chứng sơ cấp**. Nhưng `W6`/`W7`/`W8` — ba tiêu chí sinh ra riêng cho lượt này — **không có răng**: cả ba đều đo HÀM TRỢ GIÚP chứ không đo DÂY NỐI, nên phép dẫn xuất chạy thật mà **không cổng nào giữ nó khỏi biến thành hằng số**.

---

## P1-1 · `BoQuaNen` là cửa sau chưa khoá — `W7` KHÔNG ĐẠT

Bất kỳ ca nào cũng bỏ qua được vì **bất kỳ lý do gì**, không dính `runs-on` chút nào, suite vẫn rc=0.

```
$ # them mot ca: raise BoQuaNen("hom nay troi mua; TL_SKIP=1 — khong lien quan runs-on")
$ python3 ops/lease_publish_test.py
  BỎ QUA tX_cua_sau_bo_qua_theo_bien_moi_truong: hom nay troi mua; TL_SKIP=1 — khong lien quan runs-on
lease_publish: 72/72 đạt; đã chạy=72, bỏ qua=1
rc=0
```

`t71` chỉ gọi `_ly_do_bo_qua_workflow(..., job={"runs-on":"windows-latest"})` và đòi nó trả `""` — nó đo hàm, không đo rằng **mọi lần bỏ qua trong suite đều đi qua hàm ấy**. Đúng nguyên văn `W7`: *"bỏ qua một ca mà workflow của nó KHÔNG ubuntu-only ⇒ ĐỎ"* — tôi bỏ qua một ca **không có workflow nào cả** và cổng xanh.

**Vá đề xuất (~19 dòng thêm):** `BoQuaNen` mang theo `(tep, ten_job)`; `main()` **ĐO LẠI** bằng `_ly_do_bo_qua_workflow(ex.tep, ex.ten_job)` thay vì nhận lý do do ca tự khai — rỗng ⇒ xếp vào `hong`. Cộng một ca meta bơm `BoQuaNen` với mỏ neo không ubuntu-only và đòi phân loại ra ĐỎ (tách hàm `_phan_loai_bo_qua` để ca gọi được).

## P1-2 · Phép dẫn xuất KHÔNG được khoá — hằng số trá hình sống sót; `W6` KHÔNG ĐẠT

Thay lời đọc YAML bằng hằng số, suite không nhúc nhích:

```
$ # job = job or {"runs-on": "ubuntu-latest"}   # thay cho yaml.safe_load(tep.read_text())["jobs"][ten_job]
--- H1 hang so tra hinh (YAML nguyen):                        rc=0  lease_publish: 72/72 đạt; đã chạy=72, bỏ qua=0
--- H1+ hang so + YAML doi sang matrix [ubuntu, windows]:     rc=0  lease_publish: 72/72 đạt; đã chạy=72, bỏ qua=0
```

Dòng thứ hai chính là phép thử `W6` khai làm chuẩn (*"ghi cứng danh sách ⇒ đột biến này không đổi gì ⇒ ĐỎ"*) — nó **không đỏ**. Lý do: `t70` truyền `job=` dựng sẵn nên **chưa từng chạm tệp**; `t72` có đọc tệp nhưng chỉ đòi chuỗi literal `'ubuntu-latest'`, mà hằng số trá hình thoả luôn.

Kèm theo: handoff §3 khai **"W6 | 1/1 | t70"**. Sai quy kết — `t70` **không đỏ ở bất kỳ đột biến `runs-on` nào**; ca duy nhất đỏ trong cả sáu đột biến YAML là `t72`:

```
W6a runs-on=windows-latest (Linux) rc=1  ĐỎ t72   71/72
W6a' windows-latest (winsim)       rc=1  ĐỎ t72   71/72
W6b matrix[ubuntu,windows]         rc=1  ĐỎ t72   71/72  (8 ca chay lai: bo qua=0 ✓)
W6c matrix.os KHONG TON TAI        rc=1  ĐỎ t72   70/72
W6d runs-on RONG                   rc=1  ĐỎ t72   70/72
W6e runs-on=${{ env.RUNNER }}      rc=1  ĐỎ t72   70/72
```

**Vá đề xuất (~10 dòng):** một ca ghi YAML tạm với `runs-on` đặc trưng (vd `ubuntu-22.04-dackiet`) rồi đòi **chính chuỗi ấy** xuất hiện trong lý do, cộng đối chứng `windows-2022` phải trả rỗng. Hằng số không thể giả được chuỗi mà ca vừa tự sinh.

## P2-1 · `W8` không có răng — bỏ dòng in / hạ tổng kết đều không làm ca nào đỏ

`t72` tự dựng lấy chuỗi `f"BỎ QUA ca-gia: {ly_do}"` rồi khẳng định về chuỗi nó vừa dựng; nó **không chạm `main()`**.

```
--- NEN winsim (Linux dong vai Windows):  rc=0  64/64 đạt; đã chạy=64, bỏ qua=8   (in du 8 dong ly do)
--- winsim + BO vong `for ten, ly in bo_qua: print(...)`:  rc=0  64/64 đạt; đã chạy=64, bỏ qua=8   <- 8 ca BIEN MAT im lang
--- winsim + tong ket CU `{qua}/{len(CA)} đạt`:            rc=0  lease_publish: 64/72 đạt          <- trong nhu 8 ca DO
```

Đúng *"ca có MẶT khác ca có ĐO"*, chỉ dịch lên một tầng: **dòng in có mặt, nhưng không ca nào đo là nó có in**. **Vá (~10 dòng):** một ca chạy `main()` trong tiến trình con với một ca bỏ qua cưỡng bức rồi grep stdout.

## P2-2 · Dẫn xuất MỘT CHIỀU — vẫn ghi cứng tên nền (`"nt"`, tiền tố `ubuntu-`)

Prompt hỏi thẳng: *"đổi `runs-on` thành `windows-latest` thuần ⇒ tám ca phải chạy trên Windows và **bỏ qua trên Linux**. Có đảo đúng chiều không?"* — **KHÔNG**:

```
$ # runs-on: windows-latest, chay tren LINUX THAT
lease_publish: 71/72 đạt; đã chạy=72, bỏ qua=0     <- tam ca VAN CHAY va VAN DAT
```

`(nen or os.name) == "nt" and all(x.startswith("ubuntu-"))` chỉ chặn một chiều. Với một workflow windows-only, tám ca đó lại đo trên Linux **một thứ không bao giờ chạy ở đó** — nguyên văn hình dạng đã làm `#227` phải revert, chỉ đảo nền. **Vá (~5 dòng):** so nền hiện tại với tập nhãn dẫn xuất theo cả hai chiều.

## P2-3 · Không có trạng thái thứ ba "KHÔNG ĐO ĐƯỢC"

`${{ matrix.os }}` mà không có `strategy.matrix.os` ⇒ `nhan = None` ⇒ `nhan and …` rỗng ⇒ `return ""` — **không phân biệt được với "dẫn xuất được, không phải ubuntu-only"**. `runs-on:` rỗng và `${{ env.X }}` cũng vậy (W6c/W6d/W6e ở trên). Cổng có đỏ, nhưng đỏ ở `t72` với thông điệp *"bỏ qua im lặng hoặc tổng kết thiếu số"* — chỉ sai chỗ. Mỉa mai: **chính bước `tìm lease vừa đổi` trong tệp YAML này** khai đủ ba trạng thái và `t32` đòi chuỗi `KHONG DO DUOC`; hàm mới của lượt này thì không. **Vá (~4 dòng):** `nhan` rỗng/không phân giải ⇒ `raise AssertionError("KHÔNG ĐO ĐƯỢC runs-on …")`.

## P2-4 · `_doc_do_gia` được đo ở mức HÀM, không ở DÂY NỐI

Ba đột biến gỡ riêng từng mảnh đều chết đúng như executor khai — nhưng tháo hẳn dây nối thì không:

```
W1-bo-rc      rc=1  ĐỎ t69   71/72
W1-bo-stdout  rc=1  ĐỎ t69   71/72
W1-bo-stderr  rc=1  ĐỎ t69   71/72
W2 thao day noi (tra 2 loi goi trong _chay_buoc_dang ve `read_text() if is_file() else ""`)
              rc=0  72/72 đạt; đã chạy=72, bỏ qua=0     <- SONG SOT
```

Cùng một hình dạng với P1-1/P1-2/P2-1 — **bốn lần trong một diff 90 dòng**. Đây là thứ đáng ghi vào `hinh_dang_ke_thua` hơn từng finding lẻ: *khoá phần LIỆT KÊ ĐƯỢC (hàm thuần, gọi trực tiếp được) thay vì phần THẬT SỰ CHẶN (dây nối trong `main()`/call site)* — hình dạng **E**, và đây là lần **3**.

## P3-1 · Vẫn còn chỗ đọc tệp đồ giả chưa bọc — lời khai "mọi chỗ" rộng hơn phép đo

`ops/lease_publish_test.py:1243` — `_chay_than`: `ds.read_text(...).split() if ds.is_file() else []`. Rỗng đọc y hệt *"không có lease nào"*, và khẳng định tiêu thụ nó (`:1283`, `:1296`) **không kèm `rc`/`stdout`/`stderr`**:

```python
assert ds == ["ops/leases/moi.yaml"], f"chờ ĐÚNG lease nhánh này thêm, được {ds} — …"
```

`t32` **CHẠY trên Windows** (không thuộc diện `Q3′`), nên đây là đúng đường đã sinh ra `FileNotFoundError: …\argv.log` của `#227`, chỉ chưa nổ. **Vá (~2 dòng):** dùng `_doc_do_gia`.

## P3-2 · Hunk YAML (−4/+2) có lý do thật nhưng handoff KHÔNG giải trình nó

Handoff §1–§6 không nhắc lần nào tới thay đổi `.github/workflows/ops-publish-lease.yml`. Tôi đo được lý do:

```
$ # hoan nguyen ve dang ba82b06f: set +e / echo … / rc=$? / set -e
$ /tmp/actionlint/actionlint …/ops-publish-lease.yml
…:192:9: shellcheck reported issue: SC2320:warning: This $? refers to echo/printf … [shellcheck]
rc=1      (suite: 71/72, t33 ĐỎ)
$ /tmp/actionlint/actionlint  <cung tep, PATH KHONG co shellcheck>
rc=0
```

Nên hunk là **bắt buộc** và **được `t33` khoá — chỉ khi shellcheck có mặt**. `t33` đòi `actionlint` nhưng **không đòi `shellcheck`**, tức chốt giữ chính hunk này tự tắt khi thiếu công cụ: đúng bệnh `A=7` mà r1 ghi cho phiên điều phối, nay áp vào mã của packet. **Vá (~3 dòng):** `t33` khẳng định `shutil.which("shellcheck")`.

## P3-3 · `t49`: nhật ký argv LỆCH MỘT TOKEN giữa hai nền

Trên Windows `gh.exe` là bản sao `python.exe`, nên `api` bị python nuốt làm **tên script**:

```
$ cp $(command -v python3) gh_demo && ./gh_demo api "repos/o/r" --jq .id
argv= ['api', 'repos/o/r', '--jq', '.id']          # sys.argv[1:] KHONG co 'api'
$ ./ghp api "repos/o/r" --jq .id                    # ban POSIX (shebang)
argv= ['/tmp/rvw238/ghp', 'api', 'repos/o/r', '--jq', '.id']
```

Không làm ca rỗng ruột (`bool(goi1)` đòi bằng chứng dương, `ep` bắt theo `startswith('repos/')` nên bền), nhưng hai nền ghi **nội dung khác nhau** vào cùng một nhật ký; khẳng định nào sau này đọc nội dung `calls` sẽ trôi lệch âm thầm. Đáng một dòng chú thích.

---

## Cái tôi ĐÃ XÁC NHẬN (đừng làm lại)

- **`W3′` có bằng chứng sơ cấp**, lấy từ zip log đầy đủ của run `32558427472`, `head_sha=edc1906c…`:
  `gate (windows-latest)` **success** — `10_lease-publish selftest`: **8 dòng `BỎ QUA`** đủ tên ca + `runs-on đã đọc được: 'ubuntu-latest', phân giải thành ['ubuntu-latest']`, rồi `lease_publish: 64/64 đạt; đã chạy=64, bỏ qua=8`. `gate (ubuntu-latest)` **success** — `72/72 đạt; đã chạy=72, bỏ qua=0` (≥69 ✓). `t49` **không** nằm trong 8 ca bỏ qua ⇒ nó **chạy thật** trên Windows (`Q6` đạt), và không đường nào đưa nó vào diện `Q3′` (nó không gọi `_chay_buoc_dang` lẫn `_ly_do_bo_qua_workflow`).
- **`W5` đạt, đo cả hai nền.** 7 đột biến quyết định của `#227`, mỗi cái chạy hai lượt (Linux + Windows mô phỏng), **14/14 chết**: `M1` `M2` `D3` `D4` `A5` `gỡ guard kiem-github` `gỡ guard check`. Trên nền Windows mô phỏng, `t64`/`t67` (và `t66` khi nó đỏ TRƯỚC lúc bỏ qua) gánh hết — **phép bỏ qua KHÔNG tạo vùng mù đột biến**. Đây là thứ handoff §3 chưa đo (bảng của họ là một lượt Linux).
- Đổi **tên job** `dang`→`dang2` ⇒ 12 ca ĐỎ `KeyError: 'dang'`; đổi **tên bước** `đăng` ⇒ 10 ca ĐỎ. Không im lặng.
- 20 dòng bị xoá đã truy hết: **4** ở YAML (hunk SC2320 ở P3-2) + **16** ở test (2 chữ ký `chay`/`WORKFLOW_DANG`, 9 của `t49`, 2 dây nối `_doc_do_gia`, 2 của `main()`, 1 hằng). Không dòng nào mất mà không có bản thay.

## Ngân sách cho bản vá — con số người giữ kho cần

Ngân sách đã cạn (`+90/90`). Đề xuất tối thiểu để **đóng đúng hai P1**: **~29 dòng thêm** (P1-1 ≈ 19, P1-2 ≈ 10) ⇒ nới trần **90 → 120**.
Đóng trọn P1+P2 (thêm P2-1 ≈ 10, P2-2 ≈ 5, P2-3 ≈ 4, P2-4 ≈ 6): **~54 dòng** ⇒ nới trần **90 → 145**.
P3 cộng thêm ~6 dòng.

Nếu người giữ kho chọn **không nới trần**: hai P1 phải thành packet kế tiếp có tên, vì bỏ chúng lại nghĩa là `Q3′` — quyết định trung tâm của r2 — **không có cổng nào giữ**, và đúng khoảnh khắc ai đó "dọn gọn" hàm dẫn xuất thành hằng số thì không phép đo nào kêu.

---

**`da_do_gi`**: kiểm băm r1/r2 · `git diff --numstat ba82b06f..HEAD` (2 tệp, +90/−20) và truy từng dòng xoá · suite nền `72/72` trên bản sao tạm · 6 đột biến `runs-on` trên YAML thật (windows thuần ×2 nền, matrix có windows, matrix thiếu key, rỗng, biểu thức `env.`) · 2 đột biến hằng-số-trá-hình · 1 đột biến cửa sau `BoQuaNen` · 3 đột biến `W8` (winsim, bỏ in, hạ tổng kết) · 4 đột biến `W1`/`W2` (gỡ rc/stdout/stderr + tháo dây nối) · 2 đột biến đổi tên job/bước · 14 lượt đột biến `#227` (7 mutant × 2 nền) · hoàn nguyên hunk YAML + `actionlint` có/không `shellcheck` · tải zip log đầy đủ run `32558427472` và đọc thẳng bước selftest của **cả hai** job · phản chứng argv `gh.exe`. Tất cả trên bản sao trong `/tmp`; cây review `git status` **rỗng**, `HEAD` vẫn `edc1906c`, băm hai tệp write-set không đổi.

**`khong_do_duoc`**:
1. **`shellcheck` có mặt trên runner `windows-latest` hay không** — chưa đo được; log bước selftest chỉ ghi `AL_VER: 1.7.7`. Nếu vắng, `t33` trên nhánh Windows xanh mà không kiểm gì (P3-2), và tôi chỉ đo được điều đó trên PATH tự dựng ở container.
2. **Nguyên nhân gốc thật của tám ca** vẫn **chưa ai đo** — `_doc_do_gia` (`W1`) dựng ra để báo nguyên nhân, nhưng phép bỏ qua chạy **TRƯỚC** nó, nên trên Windows nó không bao giờ bắn. Kế thừa `Q1` của r1 (*"ĐO TRƯỚC, VÁ SAU"*) — theo chữ thì `Q1` **chưa được thoả**, `r2` không thu hồi nó tường minh; tôi ghi ra chứ không tự quyết, vì `Q3′` đã nói tám ca ấy "không cần nguyên nhân".
3. Hành vi thật của `t49` trên Windows ở mức nội dung nhật ký (P3-3) — suy từ ngữ nghĩa `sys.argv` của CPython + phản chứng trên Linux, **không** từ một lượt Windows.
4. `gh` thật vẫn chưa đo lần nào (kế thừa `#227`).
5. Tôi **không rà nội dung** `ops/lease_publish.py` (khớp byte-for-byte `ba82b06f`, đã tin phép đo ấy) và không rà phần YAML ngoài hunk mới — review này là review **delta**, đừng đọc thành "đã rà toàn bộ diff".
