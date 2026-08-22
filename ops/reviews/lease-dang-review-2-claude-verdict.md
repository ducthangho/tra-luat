Đo xong. Cây review sạch, HEAD không đổi.

```
KET_LUAN: can_sua
reviewed_sha: 90015a53c7407400f87c9f5a018067849fa1e842
```

**Neo đã kiểm:** `git rev-parse HEAD` = `90015a53…`; `sha256sum /tmp/spec_r2.md` = `3f310582de59dce7c109717dbab13ef9467b80c67ffeafc0ac8e1484309e0093` (khớp); verdict lượt 1 = `42b438ad15fc1a8978dcd3bef023aa1f41d0926b8b87dc9c4d521229c9d6ae41` (khớp). `git diff --numstat cfaccff9..90015a53` = 3 tệp, +498/−19 (trần 500). Suite tại chỗ **58/58 rc=0**; dưới `GITHUB_ACTIONS`+`GITHUB_REPOSITORY`+`GITHUB_ACTOR`, `gh` vắng → **58/58 rc=0** y hệt. `actionlint .github/workflows/*.yml` → rc=0, 5 tệp.

---

## P1 — Không phép đo nào bắt được việc workflow BỎ gọi `kiem-github`; `check` thì có. Bất đối xứng này là lỗ do chính packet mở

Q9 dời hai lớp GitHub ra khỏi `kiem()`. Sau đó `kiem-github` là **thứ duy nhất** chạy `_kiem_loai_so_hieu` và `_kiem_comment_da_co`, và **chỉ có đúng một điểm gọi trong toàn kho** — dòng 210 của workflow. Không ca nào đo điểm gọi ấy.

```
$ grep -rn "kiem-github" --include=*.py --include=*.yml --include=*.sh --include=*.md . | grep -v ops/specs/ | grep -v ops/reviews/
./ops/lease_publish.py:16,428,466              <- chú thích + dòng khai + bảng lệnh con
./ops/lease_publish_test.py:2244,2249,2263,2408 <- gọi TRỰC TIẾP lệnh con, không đo workflow
./ops/lease_publish_test.py:2278               <- `if cmd=='kiem-github': raise SystemExit(0)` (đồ giả, luôn 0)
./.github/workflows/ops-publish-lease.yml:210  <- ĐIỂM GỌI DUY NHẤT
```

Ba đột biến trên **bản sao tạm** (`/tmp/rv2b_90015a53_a/mut`, tar-copy, dựng lại từ `pristine` mỗi lượt):

```
$ python3 /tmp/rv2b_90015a53_a/m_wiring.py
  workflow BO loi goi `check`                rc=1 lease_publish: 57/58   giet=['t51']
  workflow BO loi goi `kiem-github`          rc=0 lease_publish: 58/58   giet=SONG SOT
  workflow BO ca hai (check + kiem-github)   rc=1 lease_publish: 57/58   giet=['t51']
```

Và biến thể mềm hơn — vẫn gọi nhưng **nuốt mã thoát**:

```
  D11 goi kiem-github nhung NUOT rc (bo ca hai nhanh if)   rc=0  58/58  SONG SOT
```

Đối chiếu: đột biến làm rỗng ruột `kiem_github()` **thì** bị bắt (`giet=['t43','t44','t46','t49']`), tức lệnh con được đo kỹ. Thứ không được đo là **sợi dây nối nó vào cổng**. Xoá 9 dòng khỏi YAML là hai lớp GitHub biến mất sạch — mất phép chặn PR, mất lớp idempotent xuyên nhánh, mất luôn đường tự chữa khi `mark` hỏng sau lúc đã POST — mà `58/58` vẫn xanh và `actionlint` vẫn rc=0. Đúng họ "cổng không nói dối, nó VẮNG MẶT".

Đây là lỗ **MỚI**, không phải lớp lỗ sẵn có: `t51` đã chứng minh đo được đúng loại này (bỏ `check` ⇒ đỏ). Packet thêm một lời gọi bắt buộc thứ hai, dồn toàn bộ giá trị an ninh của Q9 vào nó, rồi không nối nó vào phép đo đã có sẵn. Nó cũng là `muc_tieu` 7 ("phản chứng cho cả sáu mục") **chưa đạt** cho nửa `kiem-github` của `muc_tieu` 5 — tiêu chí nghiệm thu của chính đặc tả.

**Vá (rẻ, hạ tầng đã có):** trong `_chay_buoc_dang`, cho `lease_publish.py` giả **ghi nhật ký argv** thay vì `raise SystemExit(0)` câm, rồi thêm hai phép đòi: (a) mỗi lease phải có một dòng `kiem-github <tệp>` và nó phải đứng **trước** `check <tệp>`; (b) thêm tham số `kiem_github_hong=` để đột biến "kiem-github trả rc≠0" làm lease **không** được POST và bước rc≠0. Cả hai đột biến D10/D11 khi đó phải ĐỎ.

---

## P3 — `T53` khai "toàn suite", đo một lệnh; suite vẫn kế thừa môi trường qua `GITHUB_ACTOR`

`T53` nêu tiêu chí *"Toàn suite phải `N/N` khi `GITHUB_ACTIONS`/`GITHUB_REPOSITORY`/**`GITHUB_ACTOR`** ĐƯỢC ĐẶT"*. `t53` thật sự chạy **một** lệnh `check` với `GITHUB_ACTOR="ducthangho"` — đúng giá trị duy nhất không kích hoạt được lớp actor. `chay()` vẫn truyền `env=None` cho mọi ca khác, tức nguyên nhân GỐC của P1-1 lượt 1 (kế thừa môi trường) chưa bị đụng, chỉ có tên biến gây hại đổi từ `GITHUB_ACTIONS` sang `GITHUB_ACTOR`:

```
$ PATH=/tmp/actionlint:$PATH GITHUB_ACTOR=nguoi-la python3 ops/lease_publish_test.py
  ĐỎ t17 t18 t19 t20 t21 t22 t43 t44 t45 t46 t50 t56 … (22 ca)
lease_publish: 36/58 đạt      rc=1
```

Đo nền để khỏi đổ oan cho bản vá: cơ chế này **có sẵn từ trước packet**, delta = 0.

```
$ cd /tmp/rv2b_90015a53_a/base && python3 ops/lease_publish_test.py          # cfaccff9
lease_publish: 42/42 đạt   rc=0
$ GITHUB_ACTOR=nguoi-la python3 ops/lease_publish_test.py
lease_publish: 26/42 đạt   rc=1
```

Nên đây **không** phải hồi quy — nó là một **lời khai mới** (`T53`) rộng hơn phép đo mới. Hậu quả nếu trúng: `ci.yml:142` và bước `tự kiểm cổng` (`ops-publish-lease.yml:137`, có `set -euo pipefail`) chạy suite với `GITHUB_ACTOR` = người kích hoạt lượt chạy; actor ngoài `NGUOI_CO_THAM_QUYEN` ⇒ 22 ca đỏ ⇒ job chết **trước** bước `tìm lease`, đúng hình dạng khoá cổng của P1-1, chỉ khác cò. Với kho một chủ thì hẹp, nhưng cái giá phải trả là chẩn đoán: 22 ca đỏ khó đọc thay vì một dòng "actor không có thẩm quyền".

**Vá:** hoặc làm đúng chữ `T53` (thêm một ca chạy **toàn suite** trong tiến trình con với ba biến đặt và `GITHUB_ACTOR` là một tên **ngoài** allowlist), hoặc siết `chay()` dựng env sạch cho mọi ca — đúng bản vá lượt 1 đã đề ("phải làm chung cho mọi ca"). Nếu người giữ kho chọn không làm, thì phải hạ lời khai của `T53` xuống đúng thứ nó đo.

---

## P3 — `chua_do_duoc` r2 khai HẸP hơn thực tế: thiếu chính mục P1 ở trên

Sáu mục của `chua_do_duoc` đều đúng và tôi không bác được mục nào (mục 3 đã sửa đúng: khe `check`→`body` **đóng** vì `body` hết gọi mạng — đo được ở `t58`/D2, `check` và `body` không sinh lời gọi `GOI_GH` nào). Thứ thiếu là mục đáng kể nhất mà packet **tự tạo ra**: Q9 khai *"**CHỈ** bước `đăng` của workflow gọi nó"* và `muc_tieu` 5 khai *"bước `đăng` gọi `kiem-github` **trước** `check`"* — nửa "check/body KHÔNG gọi" có `t58` đo, nửa "workflow CÓ gọi" không ai đo (P1). Một tính chất bắt buộc mà không phép đo nào giữ thì nó thuộc `chua_do_duoc`, dù bản vá hiện tại làm đúng.

Cũng thiếu: `T53` chỉ đúng cho một giá trị `GITHUB_ACTOR` (P3 trên).

---

## P3 — `t55` gộp hai khiếm khuyết độc lập; và một đột biến giết nhiều ca chưa được NÓI RA

Đặc tả bắt "đột biến giết nhiều ca ⇒ NÓI RA", và bắt tách cặp `t46`/`t48` của lượt 1. **Cặp ấy đã tách thật** — kiểm được:

```
  bo lop comment (chi do posted_comment_id)    rc=1  57/58  giet=['t46']      <- lượt 1 giết t46+t48
```

Nhưng hình dạng gộp chuyển chỗ chứ chưa chết: hai đột biến **độc lập** cùng chỉ giết `t55`, nên ca ấy không nói được cái nào hỏng.

```
  D6 dau khong can o DAU than (`dau in body`)            rc=1  57/58  giet=['t55']
  D7 thieu user.login => bo qua (fail-open)              rc=1  57/58  giet=['t55']
```

Và một đột biến giết hai ca mà tôi không thấy khai ở đâu:

```
  bo lop do loai so hieu                                 rc=1  56/58  giet=['t43','t44']
```

**Vá:** tách `t55` thành `t55a` (thiếu `user.login` ⇒ CHẶN) và `t55b` (dấu không ở đầu thân ⇒ không tính); khai `bo lop do loai so hieu` giết `t43`+`t44` vào phần nghiệm thu.

---

## Bảy finding lượt 1 — trạng thái ĐO ĐƯỢC

| # | finding lượt 1 | trạng thái | phép đo của tôi |
|---|---|---|---|
| 1 | **P1** suite ĐỎ trong Actions ⇒ cổng tự khoá | **ĐÓNG** | `GITHUB_ACTIONS=true GITHUB_REPOSITORY=… GITHUB_ACTOR=ducthangho`, `gh` vắng → **58/58 rc=0**. `GITHUB_ACTIONS` không còn dòng nào trong `lease_publish.py`. Đột biến bắt buộc "cho `kiem()` gọi mạng trở lại" → `rc=1 49/58`, giết `t01 t02 t09 t14 t21 t50 t53 t58` (giết 8 ca — NÓI RA theo đòi hỏi nghiệm thu) |
| 2 | **P1** `đăng` chết giữa vòng; Q4/Q5 hẹp hơn lời khai | **ĐÓNG** | Trích thân bước `đăng` từ YAML, `gh` giả GIỮ TRẠNG THÁI trên PATH (cổng THẬT chạy, không phải đồ giả): POST lease `giua` 403 → **3 lần POST** (lease `cuoi` **vẫn được thử**), đăng `dau`+`cuoi`, `posted_comment_id` ghi cho cả hai, `GITHUB_ENV='DA_DOI=1\nDA_DOI=1\n'`, ảnh chụp lúc POST `giua` đã có `DA_DOI=1`, bước **rc=1** ⇒ `always() && env.DA_DOI=='1'` **ĐÚNG**. Đột biến (a) `DA_DOI` một lần cuối vòng → giết `t52`; (b) bỏ `set +e` quanh POST → giết `t52` |
| 3 | **P2** mỏ neo comment không kiểm tác giả (2 chiều) | **ĐÓNG cả hai chiều** | (a) `nguoi-la` đăng dấu của `lease-that` → **CHO QUA** (lease chính đáng không bị bịt); cùng dấu do `github-actions[bot]` → `CHAN rc=9`. (b) `lease_id = "x\`** **Lease \`nan-nhan"` → `kiem()` **CHAN rc=8**; và kể cả nếu thân ấy tồn tại, `startswith` làm lease `nan-nhan` vẫn **CHO QUA**. Đột biến: bỏ lọc `user.login` → `t54`; bỏ kiểm dạng `lease_id` → `t56`; vô hiệu neo tác giả → `t47 t54 t55` |
| 4 | **P3** `T49` là danh sách cấm một tên (đột biến SỐNG SÓT lượt 1) | **ĐÓNG** | Đột biến bắt buộc `[os.environ.get("GH_PATH") or "gh", "api", …]` → `rc=1 57/58 giet=['t49']`. Lượt 1: sống sót `52/52` |
| 5 | **P3** `T52` khớp CHUỖI `if:`, không đo hành vi | **ĐÓNG** | `t52` nay chạy thân bước thật; hai đột biến hành vi riêng biệt (D8, D9) đều giết đúng `t52` |
| 6 | **P3** `[]` là trạng thái thứ ba sập thành "không" | **ĐÓNG** | `[]` → `CHAN rc=8`; `[[]]` → **CHO QUA** (issue thật sự chưa có comment); `[[{bot,dấu}]]` → `CHAN rc=9`. Đột biến coi `[]` là "chưa có comment" → `giet=['t57']` |
| 7 | **P3** `T43` chẩn đoán `pull-requests` có thể sai | **ĐÓNG theo đúng Q16** | Thông điệp nay: `KHÔNG ĐO ĐƯỢC loại số hiệu: …; số hiệu trỏ vào PR là một nguyên nhân có thể — đây là phỏng đoán, không phải phép đo`; `t44` đòi cả hai chuỗi. Nhánh thật vẫn chưa ai đo — đặc tả khai đúng ở `chua_do_duoc` #2 |

---

## Bề mặt MỚI — kết quả từng mục

- **B.1 `kiem-github`** → **P1 ở trên.** Không có phép đo nào.
- **B.2 `set +e` quanh mọi lệnh có nuốt lỗi không?** → **Không**, trong mã hiện tại. Mọi nhánh `rc≠0` đều vào `bao_chan` (đặt `BI_CHAN=1`) rồi `continue`, và cuối vòng `exit 1`. Riêng `rc=9` từ `kiem-github` **không** đặt `BI_CHAN` — đo được là **đúng**, không phải lỗ: sau Q12, `rc=9` chỉ đến từ `posted_comment_id` trong tệp hoặc một comment do `github-actions[bot]` đăng **mở đầu** bằng đúng dấu; comment người ngoài không còn sinh ra nó (bảng #3). Chạy lại cùng nhánh khi đã có comment bot cho `giua`: `rc=0`, **2 POST** (chỉ `dau`+`cuoi`), `giua` **không** bị đăng trùng. Nuốt lỗi chỉ xuất hiện dưới **đột biến** D11 — tức nó là rủi ro hồi quy, và đó chính là P1.
- **B.3 `bao_chan()` in đúng tệp trong mọi nhánh?** → **Có.** Nhánh `kiem-github`: `::error file=ops/leases/dau.yaml::hai lớp GitHub chặn (rc=8)`; nhánh POST hỏng: `::error file=ops/leases/giua.yaml::đăng comment hỏng (rc=1)`. `$tep` luôn nằm trong thân vòng lặp, không nhánh nào gọi ngoài phạm vi.
- **B.4 thứ tự `kiem-github` TRƯỚC `check` ⇒ lease rác gửi được lời gọi mạng?** → **Tiền đề SAI, đo được.** `kiem_github()` chạy `kiem()` **thuần trước tiên** (`lease_publish.py:392`), nên không lease rác nào chạm mạng:

  ```
  granted_by=codex          loi goi mang = 0   CHAN rc=4
  granted_by=nguoi-la       loi goi mang = 0   CHAN rc=4
  het han 2020              loi goi mang = 0   CHAN rc=8
  thieu reviewed_sha        loi goi mang = 0   CHAN rc=8
  lease_id doc `x**`        loi goi mang = 0   CHAN rc=8
  packet_issue = -1         loi goi mang = 0   CHAN rc=8
  GITHUB_ACTOR=ke-la        loi goi mang = 0   CHAN rc=4
  packet_issue=99999999     loi goi mang = 1   CHAN rc=8   <- số hợp lệ nhưng không tồn tại
  lease hợp lệ hoàn toàn    loi goi mang = 2   QUA
  ```
  Bề mặt còn lại: một lease **đã qua toàn bộ cổng thuần** điều khiển được `{n}` trong `GET repos/<chính kho>/issues/{n}`. Không đáng kể.
- **B.5 neo `github-actions[bot]`** → phép đo **không** phân biệt được "không đặt được" với "không ai thử": `t54` chỉ dùng `nguoi-la`, và đồ giả tự đặt `user.login`. Lý do thật sự không giả mạo được nằm ở **luật không gian tên của GitHub** (tên người dùng không chứa `[`/`]`; slug `github-actions` được giữ chỗ) — đó là tài liệu, không phải phép đo, và không đo được từ đây. Đã kiểm: trong kho **không workflow nào khác** đăng comment (`grep` `comments|add_issue_comment` trên 4 workflow còn lại → rỗng), nên nguồn duy nhất sinh ra `user.login == "github-actions[bot]"` kèm dấu là chính workflow này.

---

## Đặc tả r2 — soi riêng

- **Q9 có mua thêm bề mặt không?** → **Có, đúng một**: điểm gọi `kiem-github` không được đo (P1). Đổi lại, nó **giết thật** hai lớp rủi ro (P1-1 theo kiến trúc, khe `check`→`body`). Kiến trúc đúng; thiếu là phản chứng.
- **`nghiem_thu` r2 có tiêu chí nào KHÔNG THỂ ĐỎ không?** → **Không.** Tôi đã tìm đột biến làm ĐỎ từng ca mới: `T49′`→D1, `T52′`→D8/D9, `T53`→D2, `T54`→D3, `T55`→D6/D7, `T56`→D5, `T57`→D4, `T58`→D2. Không ca nào thuộc loại `t52` cũ (khớp chuỗi, không thể đỏ). Nhưng `T53` **hẹp hơn chữ của nó** (P3 #2), và `muc_tieu` 7 **chưa đạt** cho nửa `kiem-github` của `muc_tieu` 5 (P1).
- **`chua_do_duoc` có mục nào khai hẹp hơn thực tế?** → **Có** (P3 #3): thiếu hẳn mục P1, và thiếu giới hạn của `T53`.
- **Bộ đếm hình dạng.** Tôi **không** tính P1 là hình dạng A lần thứ 7, và nói rõ vì sao: lần thứ 6 (Q5/`T52`) là **lời khai SAI** mà phép đo không thể phát hiện. Ở đây lời khai của `muc_tieu` 5 là **ĐÚNG** — tôi đo được wiring hiện tại chạy đúng thứ tự và tôn trọng mã thoát (xem dưới) — chỉ thiếu ca khoá. Đó là "phản chứng bắt buộc còn thiếu", không phải "khai rộng hơn đo". Nên **chốt DỪNG của `hinh_dang_ke_thua` KHÔNG kích hoạt**, và verdict là `can_sua` chứ không phải `dung_lai`. `T53` (P3 #2) thì đúng là hình dạng A nhưng ở mức P3, không phải mức làm sập packet — tôi để người giữ kho quyết có tính vào bộ đếm hay không, kèm số liệu ở trên.

Bằng chứng wiring hiện tại đúng (bọc lệnh thật, ghi nhật ký argv):

```
duong XANH : ['kiem-github dau','check dau','body dau','mark dau',
              'kiem-github cuoi','check cuoi','body cuoi','mark cuoi']   rc=0, đăng 2, DA_DOI=1 ×2
kiem-github HONG (đọc comment 403): ['kiem-github dau','kiem-github cuoi']
              rc=1, đăng 0, GITHUB_ENV rỗng, `check` KHÔNG BAO GIỜ chạy
```

---

## `da_do_gi`

1. `git rev-parse HEAD` = `90015a53…`; `git fetch origin ops/lease-dang-227` + `git show … | sha256sum` → spec r2 `3f310582…`, verdict r1 `42b438ad…`, cả hai khớp. `git diff --numstat cfaccff9..90015a53` → 3 tệp, +498/−19.
2. `PATH=/tmp/actionlint:$PATH python3 ops/lease_publish_test.py` → **58/58 rc=0**; cùng lệnh với `GITHUB_ACTIONS`+`GITHUB_REPOSITORY`+`GITHUB_ACTOR=ducthangho` và `gh` vắng → **58/58 rc=0**; với `GITHUB_ACTOR=nguoi-la` → **36/58 rc=1**.
3. Nền `cfaccff9` (`git archive` ra `/tmp/rv2b_90015a53_a/base`): **42/42** thường, **26/42** với `GITHUB_ACTOR=nguoi-la` ⇒ delta = 0 cho P3 #2.
4. `PATH=/tmp/actionlint:$PATH actionlint .github/workflows/*.yml` → rc=0, 5 tệp.
5. **16 đột biến**, mỗi lượt dựng lại `mut/` từ `pristine/` (tar-copy, không `.git` của kho thật): 13 theo lời khai executor + 3 của tôi (D10 bỏ hẳn `kiem-github`, D11 nuốt rc, D12 rỗng ruột `kiem_github()`), cộng 3 đột biến wiring so sánh `check` vs `kiem-github`. Bảng đầy đủ ở các mục trên.
6. `/tmp/rv2b_90015a53_a/p2_moneo.py` — dựng lại P2 hai chiều + ba trạng thái `--slurp`, gọi thẳng `_kiem_comment_da_co`/`kiem()` của bản head.
7. `/tmp/rv2b_90015a53_a/dang_that.py` — trích thân bước `đăng` bằng `yaml.safe_load` từ chính YAML, `gh` giả GIỮ TRẠNG THÁI đặt trên **PATH** (nên cả `GOI_GH` trong Python lẫn `gh api` trong shell đi cùng một đồ giả), chạy **cổng THẬT** từ head. Ba kịch bản: POST giữa 403 · đường xanh · chạy lại khi đã có comment bot.
8. `/tmp/rv2b_90015a53_a/wiring.py` — bọc `lease_publish.py` ghi nhật ký argv rồi uỷ quyền cho bản thật; đo thứ tự lệnh con và hành vi khi `kiem-github` hỏng.
9. `/tmp/rv2b_90015a53_a/b4_thutu.py` — đếm lời gọi `GOI_GH` cho 9 loại lease rác.
10. `grep -rn "kiem-github"` toàn kho; `grep -n "comments|add_issue_comment"` trên 4 workflow còn lại.
11. Kiểm sau cùng: `git status --porcelain` ở cây review **rỗng**, `git rev-parse HEAD` vẫn `90015a53…`.

## `khong_do_duoc`

- **Không có lượt chạy GitHub Actions THẬT nào.** Mọi phép đo bước `đăng` là thân bước trích từ YAML chạy dưới `bash` tại chỗ (tiền lệ `t32`/`t51`). Bằng chứng thật chỉ có ở lần đăng lease kế tiếp sau khi land. **Thu hẹp**, không đóng.
- **Không đo được GitHub có cho `issues: write` đọc một PR qua `GET /issues/{n}` hay không** — container này không có `gh`, và REST tới `api.github.com/repos/…` bị proxy chặn 403 theo ĐƯỜNG DẪN. Q16 vẫn chỉ là phỏng đoán có khai. Đặc tả khai đúng.
- **Không đo được rằng `user.login == "github-actions[bot]"` là không giả mạo được.** Đó là luật không gian tên của GitHub, không phải hành vi của mã; phép đo của kho chỉ chứng minh mã **lọc theo** trường ấy. Đây là chỗ "không đặt được" và "không ai thử" nhìn giống nhau, và tôi không tách được từ đây.
- **`[]` từ `gh --slurp` THẬT**: chỉ dựng được đầu vào bằng tay (`CompletedProcess`). Chưa chứng minh nó xảy ra ngoài đời — chỉ chứng minh cổng chặn nó.
- **Khe race hai nhánh `ops/**` vẫn MỞ** — `concurrency` gom theo `github.ref`. Q9 **đóng** khe `check`→`body` (đo được: `t58`, D2). Khe "hỏi comment → đăng comment" chỉ **thu hẹp**.
- **Chưa đo trên Windows.** `ci.yml` chỉ chạy `ubuntu` cho PR thường; gắn nhãn `windows` KHÔNG sinh lượt chạy (workflow khai `pull_request:` không kèm `types:`), phải gọi tay `workflow_dispatch` trên ref đó.
- **Không đo `posted_comment_id` của 4 tệp lease trên master** (Q7, ngoài phạm vi).
- **Không đo được có ai đã gắn ruleset/branch protection cho `.github/workflows/**` và `ops/lease_publish*.py`** — thiếu nó thì cả cổng này vẫn quy về "ai push được vào `ops/**` thì đăng được", đúng như đầu tệp YAML tự khai. Ngoài kho, ngoài phạm vi packet.

---

**Vì là vòng cuối, nói thẳng cái vẫn còn hở nếu người giữ kho chọn land:** bản vá này **tốt hơn nền `cfaccff9` trên mọi trục tôi đo được** — 7/7 finding lượt 1 đóng thật, có phản chứng chạy được cho từng cái, và wiring hiện tại chạy đúng. Thứ nó KHÔNG mang theo là một sợi dây an toàn: hai lớp GitHub nay treo vào một lời gọi duy nhất trong YAML mà không phép đo nào canh. Hôm nay nó đúng; lần refactor sau, lần giải xung đột merge sau, nó có thể biến mất và bảng điểm vẫn `58/58` xanh. Vá là ~10 dòng trong `_chay_buoc_dang` — hạ tầng đã có sẵn, `t51` đã chứng minh mẫu ấy chạy được.
