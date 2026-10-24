verdict: changes_requested
reviewed_sha: 70172ec590dc1eefd414d8aa951a8cb4fc82a86c
reviewed_tree: d53ad9e6b39d268eb33d8b4adb8a6af9f9b6326a
base_sha: 8324567788caab8dc332d45df458ef415fd305be

Có **2 P2**: răng của bộ y04 và thiếu phép đo cửa CLI của ca đường nhanh; thêm **1 P3** về đối chứng biên của gom. Chưa tìm được bypass đang hoạt động ở điều kiện Python của head. Không approve vì P2 chưa đóng. N4 GitHub thật chưa đo và được tách khỏi verdict mã.

Lớp review: **sensitive**. Môi trường đo: Linux, Python **3.13.16**, PyYAML **6.0.3**; workflow GitHub ghim Python 3.12. Không đồng nhất sandbox này với runner GitHub thật.

Reviewer độc lập: Codex / OpenAI, công cụ thực thi cục bộ qua machine transport trong sandbox quản lý; danh tính model dựa trên cấu hình phiên, không có attestation từng request. Không sửa `cay-kho/`, không push/comment/merge. Các phản chứng dùng archive riêng ở `/tmp/wp892-review.NUdvLP`; script/log/JSON giữ trong [evidence](evidence/). `VERDICT.md` được tạo với pending ngay đầu lượt và cập nhật theo các phép đo, sau đó tổng hợp lại ở đây.

## BẢNG ĐO

`TMP=$(cat evidence/tmp-root)`; mọi lệnh Python đặt `PYTHONDONTWRITEBYTECODE=1`. Hai bản base/head được tạo bằng `mktemp -d` + `git -C cay-kho archive <OID> | tar -xf -`; Git init/fetch từ mirror **cục bộ**, reset mixed tới đúng OID, `core.abbrev 7`. Không dùng mạng để tìm chứng cứ. Bản `y04-tooth` là archive head riêng cho meta-mutation.

| Phép đo | Lệnh / bằng chứng | Output thật và kết luận |
|---|---|---|
| Exact head/tree, spec | `git -C cay-kho rev-parse HEAD HEAD^{tree}`; `sha256sum SPEC.md` | Head/tree như header; SPEC `aeac5b18566f4b9d3bd5f88d39503d44facd4029913793c32e01a43c3ff5dc9b`, khớp lease r2. R1 chỉ dùng giải thích lý do nới. |
| Write set | `git -C cay-kho diff --name-only <base> <head>`; `diff --check` | Đúng bốn tệp trong lease/spec; diff-check rc 0. |
| Job ngoài phạm vi | `python3 evidence/probe-yaml.py "$TMP/y04-tooth" evidence/yaml.json` | `changed_jobs ['gate-cong-cu', 'gate-cong-cu-gop']`; `other_top_level_equal True`. So cấu trúc YAML đã parse cho mọi job khác. |
| Classifier suite base | `(cd "$TMP/base" && python3 ops/ci_duong_nhanh_test.py)` | **rc 1**, `CA: 103/104 dat · 0 do · 1 hong`; `DOT BIEN: 379/384 bi giet dung ly do`. [Log](evidence/ci-base.log). |
| Classifier suite head | Lệnh trên tại `$TMP/head` | **rc 1**, `CA: 103/104 dat · 0 do · 1 hong`; `DOT BIEN: 386/391 bi giet dung ly do`. [Log](evidence/ci-head.log). |
| Phân loại lỗi suite | So tên và traceback hai log | Cùng `t20zo_la_khong_phai_tep_thuong_do`, `socket.bind` AF_UNIX bị `PermissionError: [Errno 1] Operation not permitted`. Cùng 5 mutant không có baseline xanh; **không phải 5 survivor**. Không có lỗi mới; cả 7 mutant thêm của head bị giết. Không khai các tỷ lệ 104/104 hay 391/391. |
| Nền cong_cu | `python3 evidence/radius.py "$TMP/head" evidence/baseline-head-offline-signing.json baseline` với signing-off bên dưới | **61/61 qua, 0 bỏ qua**. Lượt đầu 60 qua/1 bỏ qua ở t47 vì commit signing của máy; không coi skip là pass. [JSON](evidence/baseline-head-offline-signing.json). |
| Registry base/head | `python3 .claude/dev/ci_dang_ky_test.py` tại hai bản | Lượt đầu rc 1 do Git signing gọi dịch vụ cục bộ bị sandbox chặn. Chạy lại bằng env `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false`: **1064/1064 → 1070/1070**, cả hai rc 0, `TỔNG: ĐẠT`. Không đổi config global. [Base](evidence/registry-base-offline-signing.log), [head](evidence/registry-head-offline-signing.log). |
| Lease t16 | `python3 ops/lease_publish_test.py --chi-ca=t16` hai vế | **9/9 đạt; đã chạy=9, bỏ qua=0**, cả hai rc 0. Các thông báo Windows tool không đo được là dữ liệu đối chứng, không phải case bị bỏ qua. [Head](evidence/lease-head.log). |
| Actions parser | `actionlint .github/workflows/ci.yml` hai vế | actionlint 1.7.7, **rc 0 / rc 0**, output rỗng. Đây là parser, không chứng minh job chạy. |
| Bare Ruff | `ruff check --no-cache --select F --output-format json .` hai vế | Ruff 0.16.9, rc 1 / rc 1, **8807 / 8807** finding nền; Counter theo đường tương đối + rule + message có added=0, removed=0. **Delta 0**, không khai bare lint xanh. [Base](evidence/ruff-base.json), [head](evidence/ruff-head.json). |
| Doctrine | `python3 .claude/dev/packet_loop.py doctrine-scan --root .` hai vế | **rc 0 / rc 0**, `sạch — đã quét 10 tệp, 0 chỗ chép doctrine`. |
| Read-only cuối lượt | Git status gồm ignored/untracked, diff/index; hash bốn tệp | Không delta; bốn tệp khớp byte với blob reviewed_sha. [Hashes](evidence/checkout-hashes.json). Snapshot đầu/cuối không chứng minh toàn bộ lịch sử giữa hai mốc. |

Năm mutant không đo được của classifier ở **cả hai** vế: `symlink_treo_khong_theo_bi_danh`, `la_bo_chot_tep_thuong`, `la_cho_phep_fifo`, `la_cho_phep_socket`, `la_khong_theo_symlink`. Tất cả dừng do tiền đề socket của t20zo chưa chạy được; bộ tự phân hạng vẫn `DAT (5 mau rc, 3 dot bien that)`.

### Ngữ nghĩa Actions — giới hạn đo offline

Tìm bằng `rg --files` và `rg -l` các chuỗi source download-artifact trong npm caches `/root/.npm`, `/home/claude/.npm`, pip/cache `/root/.cache`, `/home/claude/.cache`, công cụ `/opt`, cùng các dấu runner/Expressions2/act. **0 source phù hợp**. Danh sách kết quả rỗng được giữ ở `evidence/action-cache-all-hits.txt`, `evidence/action-cache-home-hits.txt`, `evidence/actions-runtime-files.txt`, `evidence/runner-cache-hits.txt`. Không lấy các workflow chỉ có `uses:` làm source action.

| Câu hỏi | Đo được | Hệ quả / cần quan sát ở lượt thật |
|---|---|---|
| (a) needs có job mảnh skipped; `!cancelled() && contains(...)` có chạy gom? | **KHÔNG ĐO ĐƯỢC**: không có scheduler/runner thật. Parser nhận đúng biểu thức, needs và matrix. | Cần jobs API/log của PR hồ sơ cho thấy 8 shard skipped nhưng context gom được tạo và chạy tới CLI; không suy xanh từ `!cancelled()`. |
| (b) download-artifact@v4 pattern không khớp | **KHÔNG ĐO ĐƯỢC**: không có source action/version tương ứng hoặc runtime offline. | Nếu action lỗi thì bước gom không bao giờ tới, required check đỏ ở mọi PR hồ sơ. Cần step conclusion + dòng số artifact được tải, xác nhận không có fail trước CLI. |
| (c) output thiếu thành env chuỗi rỗng | **KHÔNG ĐO ĐƯỢC** ở bộ máy biểu thức Actions. Python được thử riêng với env vắng và chuỗi rỗng, cả hai rc 1 khi thiếu mảnh. | Quan sát env được resolve trong một fixture job upstream không phát output; chỉ ghi repr/độ dài biến công khai này. Không dùng Python env rỗng làm chứng cứ cho Actions. |
| (d) path `manh` khi tải 0 artifact vắng hay rỗng | **KHÔNG ĐO ĐƯỢC** ở action; Python đã đo cả hai, đều rc 0 chỉ với mode chính xác. | Sau download cần `test -e manh`/liệt kê thư mục và thấy CLI tiếp tục. Nhánh Python bao phủ cả hai kết quả hợp lệ. |

### N1 — nhánh gom bằng CLI thật

Lệnh: `python3 evidence/probe-collector.py "$TMP/head" evidence/collector.json`. Script dựng từng fixture rồi gọi đúng `[python3, TEP_TEST, '--gop', path]`, không chỉ gọi parser hoặc một bản chép điều kiện. Toàn bộ stdout/stderr nằm ở [collector.json](evidence/collector.json); bảng sau trích output.

| Fixture / env | Output thật | Kết luận |
|---|---|---|
| `duong_nhanh` + vắng / rỗng | rc 0; `GOM: KHÔNG ĐO ... CONG_CU_TEST_GOP_CHE_DO=duong_nhanh ... 479 đột biến không chạy...`; không có chữ “giết” | KHÔNG PHẢI LỖI |
| Symlink tới thư mục rỗng | Cùng dòng KHÔNG ĐO, rc 0 | Thư mục đích rỗng, đúng hợp đồng; không phải bypass có mảnh. |
| Chỉ có thư mục con rỗng | rc 1, `[G-tep]: child không phải tệp thường` | Không coi đệ quy không có file là thư mục rỗng. KHÔNG PHẢI LỖI. |
| Chỉ có `.hidden` | rc 1, `[G-dau] ... thiếu dòng MANH đầu tệp` | Tệp ẩn vẫn đi vào gom. KHÔNG PHẢI LỖI. |
| Tên env `CONG_CU_TEST_GOP_CHE_DＯ` (O fullwidth) | rc 1, `[G-rong]` | Không sửa tên Unicode cho khớp. KHÔNG PHẢI LỖI. |
| Giá trị `duong_nhanh\r` | rc 1, `[G-rong]` | Không strip CR. KHÔNG PHẢI LỖI. |
| Giá trị có NUL | Lỗi phóng `ValueError: embedded null byte`; CLI không khởi chạy | Không phải pass/fail của sản phẩm; env chứa NUL không truyền được qua exec. |
| Quyền thư mục 000 | rc 1, stderr `PermissionError: [Errno 13] Permission denied` | Fail closed, không false success. Thử đổi UID riêng bị `preexec_fn` từ chối; không dùng nó làm bằng chứng. |
| Vắng / rỗng / `day_du` / `Duong_nhanh` / `duong_nhanh ` / `xduong_nhanh` / chuỗi fullwidth | Mỗi ca rc 1, `[G-rong]` | Chỉ exact Python string mở nhánh nhanh. KHÔNG PHẢI LỖI. |
| Đủ 8 mảnh hợp lệ, mode nhanh và thường | Cả hai rc 0; `GOM MẢNH 8/8`; toàn bộ stdout/stderr **giống hệt**, 479 kết luận thật | Gom thật. Mảnh fixture có bản ghi tổng hợp để đo consumer; không gọi đó là 479 mutation đã chạy ở lượt fixture. |
| Thiếu mảnh 7, mode nhanh và thường | Cả hai rc 1; `[G-tap]: tập mảnh [0, 1, 2, 3, 4, 5, 6] ≠ 0..7`; output giống hệt | Không bỏ gom khi có mảnh. |
| Bổ sung: symlink treo | rc 0 KHÔNG ĐO | `Path.exists()` thấy đích vắng; không thấy artifact bị giấu trong fixture này, không xếp là lỗi dữ liệu. |

### N2 — y04 nới hẹp trên YAML hợp lệ

Lệnh: `python3 evidence/probe-yaml.py "$TMP/y04-tooth" evidence/yaml.json`; mỗi biến thể chạy `ci_duong_nhanh_test.py --mot-ca y04_tap_buoc_mang_if_che_do_khop_dung` trong tiến trình con, phục hồi archive sau mỗi bộ đo. [Log](evidence/yaml.log), [JSON](evidence/yaml.json).

| Biến thể | Output |
|---|---|
| `che_do` ở if gate-ops | rc 3, `DO:y04...:gate-ops: che_do khong duoc xuat hien...` |
| `che_do` ở if gate-packet-loop | rc 3, cùng thẻ y04, đúng job |
| `strategy.max-parallel` mang che_do | rc 3, y04 cấm strategy |
| Env gom thêm STRANGE cùng giá trị che_do | rc 3, y04 env/with |
| Env gom thêm STRANGE hằng `x` | rc 3, y04 env/with |
| With bước download-artifact của job gom mang che_do (actionlint rc 0) | rc 3, y04 env/with |
| If shard dạng logic tương đương `!(... == 'duong_nhanh')` | rc 3, y04 vì không khớp nguyên văn được phép |
| Env che_do ở bước khác | rc 3, y04 env/with |
| Thêm: đổi nguồn env gom sang output os | y04 rc 0 vì không còn chuỗi che_do thuộc luật này; **y13 rc 3** ghim hình dạng bước. Không phải biến thể lọt qua toàn bộ bộ kiểm. |

Serializer fixture đã khôi phục khóa top-level `on` về string trước khi dump (PyYAML đọc nó thành boolean); lượt đầu actionlint báo thiếu on, lượt đã sửa của with fixture rc 0. [Ghi chú hiệu chỉnh](evidence/fixture-serialization-note.txt). Consumer meta-mutation dùng văn bản workflow gốc, không qua phép round-trip này.

Các ngoại lệ triển khai hiện tại không bị nới quá mức ở những fixture hợp lệ trên. Finding P2 dưới đây là bảng đột biến không khóa được hai mặt của chính luật này.

## BẢNG ĐỘT BIẾN

### Chín mutant wp892 đăng ký — đã chạy bán kính thật

Lệnh: `PYTHONDONTWRITEBYTECODE=1 REVIEW_WORKERS=8 python3 evidence/radius.py "$TMP/head" "$PWD/evidence/radius-new.json" new`; driver gọi **`_ban_kinh_moi_dot_bien`** của bộ, không giả kết quả. [JSON](evidence/radius-new.json), [log](evidence/radius-new.log).

| Mutant | Output thật |
|---|---|
| wp892_bo_nhanh | giết đúng t52; bán kính 1/61; lỗi 0 |
| wp892_strip | giết đúng t52; bán kính 1/61; lỗi 0 |
| wp892_lower | giết đúng t52; bán kính 1/61; lỗi 0 |
| wp892_tien_to | giết đúng t52; bán kính 1/61; lỗi 0 |
| wp892_vang_la_nhanh | giết đúng t52; bán kính 1/61; lỗi 0 |
| wp892_bo_dk_rong | giết đúng t52; bán kính 1/61; lỗi 0 |
| wp892_nhan_tep | giết đúng t52; bán kính 1/61; lỗi 0 |
| wp892_rc_do | giết đúng t52; bán kính 1/61; lỗi 0 |
| wp892_dong_gia_giet | giết đúng t52; bán kính 1/61; lỗi 0 |

`TOTAL 9 errors 0`, rc 0. Tên t52 đầy đủ là `t52_gom_manh_phai_DO_khi_thieu_trung_lech_va_moi_chot_co_THE_RIENG`. Các dòng bộ in dùng mẫu số 61 là tổng CA. Lượt nền đầu và radius custom cùng môi trường có t47 bị bỏ qua vì signing của máy; radius-new chỉ lưu kết luận tổng hợp, không dùng mẫu số để khẳng định cả 61 ca đều đo được. Lượt nền riêng signing-off sau đó đo đủ 61/61; không hồi tố biến skip trong lượt bán kính thành pass.

### Năm mutant độc lập của reviewer

Lệnh: `python3 evidence/custom-radius.py "$TMP/head" evidence/radius-custom.json`; mỗi mutant đi qua **`_do_ban_kinh` + `_ket_luan_ban_kinh`**, gọi đủ danh sách 61 ca. [Định nghĩa nguyên văn + mọi trạng thái](evidence/radius-custom.json). Chốt witness CLI riêng: `python3 evidence/witness-mutants.py "$TMP/head" evidence/mutant-witness.json`.

| Mutant | Phân hạng bộ thật | Witness / ý nghĩa |
|---|---|---|
| rv_contains: so `in` | t52 chết thật, 59 qua/1 bỏ qua/1 giết, bán kính 1/61 | Đã có fixture hậu tố x; không phải lỗ. |
| rv_endswith | 60 qua/1 bỏ qua/0 giết; t52 vẫn xanh | `xduong_nhanh` + rỗng: head rc 1, mutant rc 0 KHÔNG ĐO. Thiếu đối chứng tiền tố, P3. |
| rv_ignore_hidden | 60 qua/1 bỏ qua/0 giết; t52 vẫn xanh | Chỉ `.hidden`: head rc 1 G-dau, mutant rc 0 KHÔNG ĐO. Thiếu đối chứng hidden, P3. |
| rv_strip_CR | 60 qua/1 bỏ qua/0 giết; t52 vẫn xanh | `duong_nhanh\r`: head rc 1 G-rong, mutant rc 0 KHÔNG ĐO. Thiếu đối chứng CR, P3. |
| rv_dispatch_fast_rc1 (driver riêng) | 61 qua/0 bỏ qua/0 giết; t52 vẫn xanh | Literal --gop với fast env: head rc 0 KHÔNG ĐO, mutant rc 1 rỗng. Thiếu đo dispatcher mode mới, P2. |

Mutant thứ năm chạy bằng `probe-dispatch.py` với signing-off, cũng gọi `_do_ban_kinh` + `_ket_luan_ban_kinh`; [JSON đầy đủ](evidence/dispatch.json). Ba survivor miền đầu vào là lỗ của **ca khóa**, không chứng minh sản phẩm head xử lý sai. t47 bỏ qua là cùng hạn chế signing, không cấp tín dụng giết. Giữ phân biệt survivor với môi trường chưa đo.

### N3 — so Linux đầy đủ

`metadata` của driver import hai bộ thật: CA giữ nguyên **61 tên/thứ tự**; DOT_BIEN cũ **470/470 định nghĩa** giống hệt (đường, neo, thay, binding, phụ thuộc, ca đích); head thêm đúng 9, tổng 479; thứ tự tương đối 470 tên cũ cũng giữ nguyên. Số lần xuất hiện **từng** mỏ neo cũ giống nhau, **0** neo đổi số lần; không chỉ so tổng. [Base](evidence/meta-base.json), [head](evidence/meta-head.json).

Bán kính chạy hai vế trong **một lệnh**, cả hai có `PYTHONDONTWRITEBYTECODE=1`, local `core.abbrev=7`:

```sh
TMP=$(cat evidence/tmp-root)
for side in base head; do
  PYTHONDONTWRITEBYTECODE=1 REVIEW_WORKERS=8 python3 evidence/radius.py \
    "$TMP/$side" "$PWD/evidence/radius-old-$side.json" old \
    > "evidence/radius-old-$side.log" 2>&1
  rc=$?
  tail -3 "evidence/radius-old-$side.log"
  printf '%s rc=%s\n' "$side" "$rc"
done
```

Đã đo **67/67** đột biến t52 cũ trên cả hai vế; 0 lỗi phân hạng base / 0 head; kết luận khác nhau: `[]`. Toàn bộ dòng kết luận được so nguyên văn, không chỉ đếm tên. [So sánh](evidence/n3-comparison.json), [base radius](evidence/radius-old-base.json), [head radius](evidence/radius-old-head.json).

Đây là phần so cục bộ các mutant t52 cũ, không thay cho việc so kết luận job gom PR thật/master thật (N4). Không khai đã chạy đủ toàn bộ 470 mutant cũ.

## BẢNG SĂN

| Hướng độc lập / giả thuyết | Lệnh | Output thật | Kết luận |
|---|---|---|---|
| Merge-ref của PR hồ sơ kéo thay đổi mã từ nhánh đích mới hơn | `python3 evidence/probe-hunts.py "$TMP/head" evidence/hunts.json` gọi `--mot-ca t11d_merge_ref_that_dung_base_moi_hon_day_du` | rc 0. Ca dùng git thật: đối chứng merge trên base cũ cho duong_nhanh; merge-ref mới đổi scripts/f.py bị phân loại day_du. | **KHÔNG PHẢI LỖI** trong fixture; không suy ra đã đo GitHub merge-ref thật. |
| PR sửa chính ci.yml/bộ phân loại tự cho mình đường nhanh | Cùng script, `--mot-ca t08_doi_workflow_hoac_bo_phan_loai_day_du`; thêm hai quyết định classifier in trực tiếp | rc 0; `.github/workflows/ci.yml day_du`, `ops/ci_duong_nhanh.py day_du`, lý do diff ngoài allowlist | **KHÔNG PHẢI LỖI**; phần output trực tiếp dùng git giả, ca t08 cũng kiểm các tổ hợp với hồ sơ. |
| Push/dispatch vô tình nhận đường nhanh | `ci_duong_nhanh_test.py --mot-ca t03_push_va_dispatch_khong_goi_git` | rc 0; ca kiểm push/dispatch/schedule/case lạ, luôn day_du và không gọi git | **KHÔNG PHẢI LỖI** ở classifier; Actions output binding chưa đo. |
| chuan-bi thất bại toàn job, output che_do vắng, required gom có bị skipped? | Đọc YAML parse trong hunts; CLI env_absent/env_empty ở collector | Python rc 1 G-rong nếu CLI được chạy. Chưa có runner để tạo tình huống needs upstream failed và xem os output/fromJson. | **KHÔNG ĐO ĐƯỢC** ở scheduler; cần job-level failure fixture. Step phân loại failure/timeout với continue-on-error và fallback khác whole-job failure. Không tuyên bố required check đã chạy. |
| Tệp artifact có mặt nhưng thiếu một mảnh được mode nhanh bỏ qua | `probe-collector.py`, valid/partial × day_du/duong_nhanh | Đủ: hai output bằng nhau rc 0; thiếu: hai output bằng nhau rc 1 G-tap | **KHÔNG PHẢI LỖI**; không mất chốt cũ khi đã có artifact. |
| Ca fast mode có bỏ sót cửa CLI? | `probe-dispatch.py` | 61 ca qua dưới mutation làm literal --gop fast mode rc 1; head rc 0 | **LỖI P2**, chi tiết dưới. |
| “Giết đúng y04” có thể chỉ do YAML invalid và thiếu một mặt luật | `probe-y04-tooth.py` trên archive riêng | Hai meta-mutation độc lập vẫn 7/7 killed dù with/extra-step-env bị cấm được chấp nhận; một mutant có duplicate env | **LỖI P2**, chi tiết dưới. |

### y04-dot-bien-khong-khoa-du-hai-ngoai-le  [P2]  Bảng đột biến không khóa được env bước khác và with

**TỆP/DÒNG:** `ops/ci_duong_nhanh_test.py:3286` (mutation env ở bước khác), `:3281` (nhóm đăng ký y04), `:2163` (chốt with).

**VẤN ĐỀ:** Spec r2 yêu cầu mutation hợp lệ, đích y04, cho cả env che_do ở bước khác và with che_do. `y04_env_vao_buoc_khac` chèn thêm `env:` vào bước G5 mảnh vốn đã có env, nên YAML loader ném lỗi khóa trùng trước khi y04 đo luật env. Bảy mutant đích y04 không có cái nào đưa che_do vào with. Vì vậy tuy bảng báo killed, nó không khóa đủ hai ngoại lệ đã được phép nới. Đây là lỗi nghiệm thu/độ tin cậy của test; YAML head hiện vẫn từ chối đúng các fixture hợp lệ.

**ĐÃ THỬ NGHIỆM:** `python3 evidence/probe-y04-tooth.py "$TMP/y04-tooth" evidence/y04-tooth.json` dùng consumer thật `chay_tap_dot_bien` cho nhóm y04:

```text
y04_targeted_mutants 7
with_che_do_introduced_by_table []
invalid_yaml_in_declared_table ... khoa trung 'env' o dong 573
after_deleting_with_guard 7 / 7 bad []
forbidden_with_accepted_after_guard_deletion True
after_allowing_env_at_every_shard_step 7 / 7 bad []
forbidden_env_at_other_step_accepted True
head_rejects_forbidden_with True
head_rejects_forbidden_shard_env True
```

Đối chứng head không đổi: `probe-yaml.py` với YAML hợp lệ cho cả with ở action download (actionlint rc 0) và env ở bước khác đều **rc 3 DO:y04**. Phản chứng không dựa vào lỗi môi trường/socket. [Log](evidence/y04-tooth.log), [JSON](evidence/y04-tooth.json), [script nguyên văn](evidence/probe-y04-tooth.py).

**ĐỘ TIN:** cao. **Vá ở đâu/cách vá:** bảng DOT_BIEN; mutation env phải thêm khóa vào map hiện hữu hoặc chọn bước chưa có env, không tạo duplicate key; thêm mutation `with` hợp lệ ở bước gom, đích y04. **Ca khóa:** bảo đảm hai fixture parse được trước, rồi loại/chuyển sai hai chốt riêng phải làm phép tự kiểm đỏ; không cấp tín dụng cho parser rejection thay kiểm ngoại lệ. **Rủi ro bản vá:** neo trùng/không khớp có thể tạo tín dụng giả lần nữa; đo tính duy nhất và chạy lại consumer thật. Không cần nới luật y04. Owner: executor wp892; chưa đóng.

### gom-duong-nhanh-chua-khoa-dispatcher-cli  [P2]  Ca đường nhanh chưa đo qua cửa CLI mà N1 yêu cầu

**TỆP/DÒNG:** `ops/cong_cu_test.py:8402`, `:8413` (fixtures mới gọi `_main_gop()` trực tiếp); cửa sản phẩm được đối chứng ở `:9139`.

**VẤN ĐỀ:** N1 yêu cầu tiến trình con chạy `TEP_TEST --gop`. Ca t52 gọi `--tu-kiem-gom`, và các fixture mới chỉ thay `sys.argv` rồi gọi `_main_gop` trong tiến trình tự kiểm ấy. Đột biến trên đĩa có cắn vào thân hàm (chín wp892 đều chết), nhưng không đo được đường dispatcher với env fast-mode. Những ca CLI F13 có sẵn chỉ chạy đường env bình thường. Một hỏng riêng cửa CLI ở mode mới vì thế không bị ca nào phát hiện.

**ĐÃ THỬ NGHIỆM:** `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false PYTHONDONTWRITEBYTECODE=1 python3 evidence/probe-dispatch.py "$TMP/head" evidence/dispatch.json`. Dùng cơ chế thật `_do_ban_kinh` + `_ket_luan_ban_kinh`; mutation chỉ đổi dispatcher:

```python
if cua == "--gop":
    sys.exit(1 if os.environ.get(_BIEN_GOP_CHE_DO) == "duong_nhanh" else _main_gop())
```

Output: `rv_dispatch_fast_rc1: ... t52 ... vẫn XANH ⇒ đột biến không giết được gì`; **61 qua, 0 giết, 0 bỏ qua**. Witness literal `[python3, TEP_TEST, '--gop', empty_dir]`, env duong_nhanh: head **rc 0 + KHÔNG ĐO**, mutant **rc 1 + stdout rỗng**. `_main_gop` không bị sửa trong mutation. [JSON](evidence/dispatch.json), [log](evidence/dispatch.log), [script](evidence/probe-dispatch.py).

**ĐỘ TIN:** cao; không phụ thuộc socket/signing hoặc lỗi dựng fixture. **Vá ở đâu/cách vá:** mở rộng giàn CLI F13 trong `_in_tu_kiem_gom` để chạy bảng mode × thư mục bằng subprocess `TEP_TEST --gop`, truyền env cho chính tiến trình con; có thể giữ kiểm trực tiếp để quan sát số lần vân tay, nhưng nó không thay phép đo CLI. **Ca khóa:** đăng ký mutation dispatcher ở trên, đích t52; nó phải chết đúng t52, còn các đường có mảnh giữ output như thường. **Rủi ro:** fixture có mảnh cần HEAD/hash của đúng bản test bị mutate; tái dùng rig git/vân tay hiện hữu để không giết vì G-head. Owner: executor wp892; chưa đóng.

### gom-thieu-doi-chung-ngoai-gia-tri-va-thu-muc  [P3]  Ca gom bỏ sót ba dạng nới điều kiện

**TỆP/DÒNG:** `ops/cong_cu_test.py:7275` (tập âm), `:8402` (fixtures mode × thư mục).

**VẤN ĐỀ:** Các ca mới khóa dư khoảng trắng/hoa-thường/hậu tố nhưng chưa có tiền tố trước mode, CR và thư mục chỉ có tệp ẩn. Ba mutation sai hợp đồng ở bảng reviewer đều sống qua cả tập CA. Không nâng thành lỗi runtime vì head xử lý đúng cả ba; đây là nợ kiểm thử bổ sung ngoài chín mutant đăng ký, không phải tự tuyên bố N1 đã đo toàn miền đầu vào.

**ĐÃ THỬ NGHIỆM:** `custom-radius.py` + `witness-mutants.py`: rv_endswith, rv_ignore_hidden, rv_strip_CR có 0 giết, t52 qua; mỗi witness CLI có **head rc 1 → mutant rc 0 KHÔNG ĐO**. [Radius](evidence/radius-custom.json), [witness](evidence/mutant-witness.json).

**ĐỘ TIN:** cao. **Hướng vá/ca khóa:** thêm ba fixture đối chứng qua TEP_TEST bị mutate; giữ kiểm rc, thẻ lỗi, không lấy vân tay ở đúng nhánh, và không in “giết” cho nhánh không đo. **Rủi ro:** vẫn cho NUL là input process bình thường hoặc coi lỗi dựng fixture là giết; NUL phải tách như phép đo hiện tại. Owner: executor wp892; ghi nợ bổ sung, không phải lý do chính của changes_requested.

## N4 — chưa đo GitHub, tách khỏi verdict mã

**KHÔNG ĐO ĐƯỢC offline.** Không có số phút từ jobs API, không có bằng chứng 8 shard chạy trên PR mã/day_du, không có lượt PR hồ sơ cho shard skipped + required gom success + dòng KHÔNG ĐO. Cũng chưa so từng dòng conclusion của job gom PR/master thật ngoài 9 mục mới. Không lấy actionlint hoặc fixture tổng hợp thay N4. Khi có lượt thật cần giữ exact head/run/attempt, jobs API và log download/gom để đóng riêng các câu hỏi Actions (a)–(d). Không đăng gì lên GitHub trong lượt review này.
