Đã đo xong. Verdict:

```
KET_LUAN: can_sua
reviewed_sha: fefa15b67a2691cf90ee8bfd0ab3880adc5f35d9
```

**Neo đã kiểm:** `git rev-parse HEAD` = `fefa15b6…`; `sha256sum /tmp/spec227.md` = `e1026adb569f5b4732197afac9c0f35cdd5a8945d46301b1d4cb062624e7c72c` (khớp). Nền `cfaccff9`, diff 3 tệp +298/−11. Suite tại chỗ **52/52** (sau khi cài `actionlint` 1.7.7).

---

## P1 — Bộ tự kiểm của chính cổng ĐỎ khi chạy TRONG Actions ⇒ sau khi land, không lease nào đăng được nữa

`kiem()` áp hai lớp mới khi `"GITHUB_ACTIONS" in os.environ`. Bộ test gọi `check`/`body` bằng `chay()`, mà `chay()` truyền `env=None` ⇒ **kế thừa môi trường**. Cả `ops-publish-lease.yml` (bước `tự kiểm cổng`, dòng 137) lẫn `ci.yml` (dòng 142) chạy suite **bên trong Actions** và **không bước nào cấp `GH_TOKEN`** ⇒ `gh api` hỏng ⇒ 6 ca đòi `rc=0` chuyển thành `rc=8`.

```
$ printf '#!/bin/sh\necho "gh: ... set the GH_TOKEN environment variable." >&2\nexit 4\n' > /tmp/fakebin/gh; chmod +x /tmp/fakebin/gh
$ PATH=/tmp/fakebin:/tmp/actionlint:$PATH GITHUB_ACTIONS=true \
  GITHUB_REPOSITORY=ducthangho/tra-luat GITHUB_ACTOR=ducthangho python3 ops/lease_publish_test.py; echo RC=$?
  ĐỎ  t01_lease_hop_le_thi_QUA: chặn oan lease hợp lệ: rc=8 CHAN [8]: KHÔNG ĐO ĐƯỢC loại số hiệu:
       `gh api` rc=4: gh: ... set the GH_TOKEN environment variable.
  ĐỎ  t02c_nguoi_CO_tham_quyen_thi_QUA_moi_cach_viet
  ĐỎ  t02d_GITHUB_ACTOR_khong_co_tham_quyen_bi_CHAN
  ĐỎ  t09_body_in_ra_nguyen_van_YAML_de_doi_chieu
  ĐỎ  t14_neo_prompt_DUNG_thi_QUA
  ĐỎ  t21_bam_theo_BYTE_chu_khong_theo_van_ban
lease_publish: 46/52 đạt
RC=1
```

Kết quả **y hệt** khi `gh` vắng hẳn (container này): `46/52`. Nên kết luận không phụ thuộc runner có `gh` hay không.

Hậu quả: `chay_lease_publish_test.sh` kết bằng `exec` (giữ rc), bước `tự kiểm cổng` có `set -euo pipefail` ⇒ job `dang` chết **trước** bước `tìm lease`. **Cổng đăng lease tự khoá vĩnh viễn ngay lượt push `ops/**` đầu tiên sau khi land**, và `ci.yml` cũng đỏ. Đây đúng hình dạng "gate xanh ở máy ≠ gate xanh ở nơi nó chạy" — suite chỉ được đo ở nơi `GITHUB_ACTIONS` vắng.

**Vá:** trong `chay()`, mặc định dựng env = `os.environ` **trừ** `GITHUB_ACTIONS`/`GITHUB_REPOSITORY` (t50 tự pop rồi, phải làm chung cho mọi ca). Và thêm ca khoá: chạy lại toàn suite với `ENV_ACTIONS` đặt sẵn phải vẫn `N/N` — không có ca đó thì lớp này lại lọt lần nữa.

---

## P1 — `đăng` vẫn chết giữa vòng trên mọi đường KHÔNG đi qua mã thoát của `check`; Q4 và Q5 đều hẹp hơn lời khai

`DA_DOI=$DA_DOI >> $GITHUB_ENV` nằm **sau** vòng lặp. `set -euo pipefail` giết bước ở bất kỳ lệnh không được bọc `set +e` nào (`body`, `gh api` POST, `mark`) ⇒ biến chưa từng được xuất ⇒ `if: always() && env.DA_DOI == '1'` **SAI** ⇒ ghi ngược bị bỏ qua. Trích thân bước `đăng` từ chính YAML (tiền lệ `t32`/`t51`), `gh` giả **giữ trạng thái**:

```
$ python3 /tmp/rv227/m2_dang_chet_giua_chung.py . post_403
rc bước `đăng`        : 1
GITHUB_ENV            : ''
=> `always() && env.DA_DOI == '1'` : SAI  -> ghi ngược BỊ BỎ QUA
comment đã đăng       : ['**Lease `dau`**']
  dau.yaml posted_comment_id trong CÂY LÀM VIỆC: True      <-- mất theo runner
  cuoi.yaml posted_comment_id ...: False                    <-- chưa hề được thử
stdout cuối           : gh: Resource not accessible by integration (HTTP 403)
```

Đúng chuỗi Đ4, chỉ khác chỗ 403 phát ra. Và **bản vá tự thêm hai đường chết mới cho mỗi lease**: `lenh_body` nay đi qua `kiem()`, tức gọi mạng:

```
$ python3 /tmp/rv227/m3_body_goi_gh.py .
lệnh `check`: rc=0  số lời gọi `gh api` = 2
lệnh `body` : rc=0  số lời gọi `gh api` = 2
    api repos/o/r/issues/55
    api --paginate --slurp repos/o/r/issues/55/comments
```

Khe race giữa `check` và `body` (nhánh khác vừa đăng xong) nay làm `body` trả **rc=9** — và rc đó không được bọc:

```
$ python3 /tmp/rv227/m2_dang_chet_giua_chung.py . body_rc9
rc bước `đăng`        : 9
GITHUB_ENV            : ''
=> `always() && env.DA_DOI == '1'` : SAI  -> ghi ngược BỊ BỎ QUA
```

Nên: **Q4 "xử hết danh sách" chỉ đúng cho lease bị chặn qua mã thoát của `check`** (`cuoi` không được thử trong cả hai ca trên); **Q5 "ghi ngược chạy kể cả khi bước đăng đỏ" chỉ đúng cho đúng một đường đỏ** — đường `BI_CHAN` ở dòng cuối. Mọi đường đỏ khác vẫn mất `posted_comment_id` y như trước packet.

**Vá:** (a) ghi `DA_DOI=1` vào `$GITHUB_ENV` **ngay sau mỗi `mark`**, trong vòng lặp, thay vì một lần ở cuối; (b) bọc `body` + `gh api` + `mark` bằng `set +e` và cho vào cùng nhánh `BI_CHAN=1; continue` như `check`. Khoá bằng T51b: POST của lease **giữa** hỏng ⇒ lease **cuối** vẫn đăng, `GITHUB_ENV` có `DA_DOI=1`, rc≠0.

---

## P2 — Mỏ neo `**Lease \`id\`**` không kiểm TÁC GIẢ comment: một lease chính đáng bị bịt vĩnh viễn, cổng báo XANH

`_kiem_comment_da_co` dò chuỗi trong `body` của **mọi** comment, không lọc `user.login`. Q2 chuyển bản ghi idempotent từ chỗ **có cổng ghi** (tệp lease, chỉ `ducthangho` push được) sang chỗ **ai cũng ghi được** (thân comment trên issue), mà không thêm chốt danh tính.

```
$ python3 /tmp/rv227/m4_moneo.py .
=== (a) comment của NGƯỜI NGOÀI mang dấu ===
  trước : rc=0 lease lease-that ĐĂNG ĐƯỢC — issue #55, ...
  (thêm comment của `nguoi-la`: "Nhắc lại cho rõ: **Lease `lease-that`** đã hết hạn, xin cấp lại.")
  sau   : rc=9 CHAN [9]: lease 'lease-that' đã có comment 100 trên issue #55 — bỏ qua
```

`rc=9` ⇒ workflow in `đã đăng trước đó — bỏ qua`, `continue`, **không** đặt `BI_CHAN` ⇒ lượt chạy XANH. Người giữ kho thấy cổng xanh và không thấy lease. Đây lại là "cổng không nói dối — nó vắng mặt".

Chiều thứ hai: `lease_id` **không có phép kiểm dạng nào** trong `kiem()`, nên comment của lease A mang được dấu của lease B:

```
=== (b) lease_id do head kiểm soát bịt lease khác ===
  lease_id của A = x`** **Lease `nan-nhan
  thân comment A : **Lease `x`** **Lease `nan-nhan`** — đăng tự động từ `…/l.yaml`.
  lease B `nan-nhan` : rc=9 CHAN [9]: lease 'nan-nhan' đã có comment 100 trên issue #55 — bỏ qua
```

**Vá:** chỉ tính comment do `github-actions[bot]` đăng (lọc `user.login`, và trạng thái thứ ba khi thiếu trường ⇒ CHẶN), đòi dấu nằm ở **đầu** thân comment; cộng phép kiểm dạng `lease_id` (`^[A-Za-z0-9._-]+$`) trong `kiem()`. Đây **không** phải sửa `dung_than()` (ngoài phạm vi) — chỉ siết đầu vào và siết phía đọc.

---

## P3 — T49 là danh sách CẤM một tên; đột biến đổi tên biến sống sót nguyên vẹn

Tiêu chí T49 trong đặc tả là *"Biến môi trường / trường trong lease **không** đổi được mối nối"*, nhưng phép đo chỉ đặt đúng một tên do chính test bịa (`LEASE_PUBLISH_GH`).

```
# đột biến trên BẢN SAO tạm (/tmp/rv227/mut/repo), mã thật KHÔNG bị chạm:
#   ["gh", "api", ...]  ->  [os.environ.get("GH_PATH") or "gh", "api", ...]
MỐI NỐI chọn được bằng biến môi trường TÊN KHÁC  -> giết: KHÔNG CA NÀO (SỐNG SÓT)  [52/52]
```

Sáu đột biến còn lại đều giết **đúng ca của mình**:

```
coi PR như issue (bỏ đo loại)                        -> ['t43']  [51/52]
coi lỗi đo loại là 'chắc là issue'                   -> ['t44']  [51/52]
coi lỗi đọc comment là 'chưa có comment nào'         -> ['t48']  [51/52]
khớp substring LỎNG (bỏ ** đóng)                     -> ['t47']  [51/52]
im lặng bỏ qua khi ngoài Actions (bỏ dòng khai VẮNG) -> ['t50']  [51/52]
chỉ dò posted_comment_id như cũ (bỏ lớp comment)     -> ['t46','t48']  [50/52]
bỏ always() trong `if:` của bước ghi ngược           -> ['t52']  [51/52]
```

Nói ra theo đúng đòi hỏi của `nghiem_thu`: đột biến T46 giết **hai** ca (t46 + t48) — hai ca chưa tách đủ khỏi nhau, không làm tròn thành đạt.

**Vá:** đo mối nối bằng lời khai chứ đừng đoán tên — chạy `kiem()` với `os.environ` bị bơm đầy biến theo MẪU (`*GH*`, `*GITHUB*`, `*API*`…) và đòi số lời gọi tới `GOI_GH` giả không đổi; đây đúng bài "danh sách cấm không bao giờ đủ" của chính kho.

---

## P3 — T52 khớp CHUỖI `if:`, không đo HÀNH VI — đó là lý do P1 thứ hai lọt

`t52` chỉ đọc `buoc.get("if")` rồi kiểm `"always()" in dieu_kien`. Nó không thể đỏ vì `DA_DOI` không được xuất. Đúng hình dạng mà `ops/cai_actionlint.sh` ghi ở đầu tệp là *"lần thứ ba cùng một hình dạng lỗi — kiểm sự CÓ MẶT của chuỗi rồi tuyên là đã đo HÀNH VI"*. `t51` đã chứng minh đo được thân bước thật; `t52` nên làm y hệt trên đường đỏ (xem vá của P1-2).

---

## P3 — `[]` là trạng thái thứ ba sập thành "không"

Dò toàn bộ đường vào của lớp comment (bảng đầy đủ dưới đây): **7/9 fail-close đúng**, chỉ `[]` cho qua.

```
$ python3 /tmp/rv227/m5_batrangthai.py .
gh vắng (OSError)                | CHẶN rc=8: KHÔNG ĐO ĐƯỢC …
gh rc=4 (thiếu GH_TOKEN)         | CHẶN rc=8
JSON méo                         | CHẶN rc=8
stdout RỖNG, rc=0                | CHẶN rc=8
`--slurp` không hỗ trợ           | CHẶN rc=8
slurp trả [] (KHÔNG trang nào)   | >>> CHO QUA (sẽ ĐĂNG)
slurp trả [[]] (1 trang rỗng)    | >>> CHO QUA (sẽ ĐĂNG)     <-- ĐÚNG: issue không có comment
trang lỗi [{'message':…}]        | CHẶN rc=8
comment body = null              | CHẶN rc=8
```

`all(isinstance(x, dict) for x in [])` là `True` ⇒ `comments = []` ⇒ "chưa đăng". Tôi **không** dựng được đầu vào ấy từ một `gh` thật (container không có `gh`), nên xếp P3: cách vá rẻ là chặn `if not cac_trang: raise Chan(...)`.

---

## P3 — `T43` đo một nhánh có thể không tồn tại trong production

`_kiem_loai_so_hieu` gọi `GET repos/{o}/{r}/issues/{n}`. Workflow khai `permissions: issues: write` và **cố ý** không có `pull-requests`. Nếu GitHub đòi `pull-requests: read` để **đọc** một PR qua điểm cuối issues, thì với #214 lời gọi trả 403 ⇒ thông báo thực tế là `KHÔNG ĐO ĐƯỢC loại số hiệu` chứ **không** phải câu nêu `pull-requests` mà `muc_tieu` 1 và T43 đòi. Hành vi (CHẶN) vẫn đúng; **chẩn đoán** — thứ Q1 mua bằng việc không thêm quyền — thì không. `t43` xanh vì đồ giả trả 200 kèm `html_url`. Không đo được ở đây (xem `khong_do_duoc`).

---

## Điều ĐO ĐƯỢC là ĐÚNG, ghi lại để khỏi bị vá nhầm

- **Mối nối `GOI_GH` thật sự là MỘT.** `grep -n "GOI_GH\|subprocess\|_doc_gh" ops/lease_publish.py` → `subprocess` xuất hiện đúng một lần trong thân `GOI_GH`; `_doc_gh` là caller duy nhất; hai điểm gọi. Không biến môi trường nào, không trường lease nào chọn được nó trong **mã hiện tại** (chỉ phép ĐO của nó yếu — P3 ở trên).
- **Đồ giả `GhGia` GIỮ TRẠNG THÁI thật.** `t46` xanh vì lượt hỏi thứ hai thấy comment lượt một vừa `dang()` thêm vào danh sách — mutation "bỏ lớp comment" giết nó, tức nó có răng.
- **Nhánh `BI_CHAN` hoạt động đúng như Q4+Q5 khi lỗi đi qua `check`:** `t51` đo thân bước thật, lease giữa bị chặn, lease cuối vẫn đăng, `DA_DOI=1` có trong `GITHUB_ENV`, rc≠0.

---

## `da_do_gi`

1. `git rev-parse HEAD`; `git show origin/ops/lease-dang-227:ops/specs/…` + `sha256sum` → khớp `e1026adb…`.
2. `AL_VER=1.7.7 bash ops/cai_actionlint.sh` (dùng lại `/tmp/actionlint` sẵn có) → `actionlint 1.7.7`.
3. `PATH=/tmp/actionlint:$PATH python3 ops/lease_publish_test.py` → **52/52** (nền).
4. Suite dưới môi trường Actions, hai biến thể (`gh` vắng · `gh` có nhưng không token) → **46/52, rc=1** cả hai. → P1-1.
5. `/tmp/rv227/m2_dang_chet_giua_chung.py` — trích thân bước `đăng` từ YAML bằng `yaml.safe_load`, thay `python3`→interpreter thật và `gh api`→`gh` giả **giữ trạng thái trong `state.json`**; hai chế độ `post_403` và `body_rc9`. → P1-2.
6. `/tmp/rv227/m3_body_goi_gh.py` — `gh` giả ghi nhật ký lời gọi, đếm cho `check` và `body`. → 2+2.
7. `/tmp/rv227/m4_moneo.py` — `gh` giả đọc `state.json`, đi qua `GOI_GH` thật (subprocess), hai chiều (a)/(b). → P2.
8. `/tmp/rv227/m5_batrangthai.py` — thay `GOI_GH` bằng 9 `CompletedProcess` dựng tay. → bảng ba trạng thái.
9. Bảy đột biến trên **bản sao tạm** `/tmp/rv227/mut/repo` (tar-copy, không `.git`), khôi phục từ `/tmp/rv227/lp.orig` sau mỗi lượt. Kiểm sau cùng: `git status --porcelain` ở cây review **rỗng**, HEAD vẫn `fefa15b6`.

## `khong_do_duoc`

- **Không có lượt chạy Actions THẬT nào.** Phiên này không được cấp công cụ Actions/MCP đọc lượt chạy (`mcp__github__list_pull_requests` bị từ chối quyền), nên P1-1 là **dự đoán có phản chứng chạy được tại chỗ**, không phải một lượt chạy đã đỏ. Cách xác nhận rẻ nhất: mở check của PR này — bước `lease-publish selftest` trong `ci.yml` phải đang ĐỎ với đúng sáu ca trên.
- **Không đo được GitHub có cho `issues: write` ĐỌC một PR qua `GET /issues/{n}` hay không** (đòi token + quyền thật của runner). Vì thế chỉ nói được: T43 xanh trên đồ giả; nhánh thật cho #214 **chưa ai đo**.
- **`[]` từ `gh --slurp` thật:** container không có `gh`, chỉ dựng được đầu vào bằng tay. Chưa chứng minh nó xảy ra ngoài đời.
- **Khe race hai nhánh `ops/**` chỉ được THU HẸP**, và bản vá làm nó **rộng hơn một chút so với lời khai của `chua_do_duoc` mục 2**: đặc tả nói khe nằm giữa "hỏi comment" và "đăng comment"; đo được ở P1-2 là `body` nay cũng hỏi, nên còn một khe thứ hai (`check`→`body`) mà khi thua thì **giết cả bước** chứ không chỉ đăng trùng. Đó là chỗ `chua_do_duoc` khai hẹp hơn thực tế.
- **Không đo được** liệu `posted_comment_id` của 4 tệp lease trên `master` có bị bản vá này chạm tới (Q7, ngoài phạm vi — không kiểm).
- Ba con số `52/52` · `actionlint 5/5` · `+298/−11` **đã kiểm lại** (52/52 và +298/−11 tự chạy; actionlint không chạy riêng vì `t33` bao nó và đã xanh).

Nguồn sự thật là tệp có băm trong kho; các script `/tmp/rv227/*.py` ở trên là bản dựng lại được của từng phép đo.
