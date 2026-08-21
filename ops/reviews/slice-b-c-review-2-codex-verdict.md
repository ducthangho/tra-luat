# VERDICT cross-review — `SLICE-B-C` (#215 / PR "#216"), lượt 2/2

**Chép nguyên văn** kết luận của lượt cross-review. Lease `slice-b-c-review-2-codex-20260821`, reviewer **codex**
(khác nhà cung cấp), neo exact head `175e95bd68556d38a7dde517ce858cb27e821097`.

- Nguồn: stdout/stderr của `codex exec` do `launcher.py` giữ, run `8ddb0c6f`, `ma_thoat=0`.
- Chốt read-only sau lượt: `worktree_sach=True`, `so_muc_ban=0`, HEAD không đổi.
- Đường dẫn tuyệt đối của thư mục phiên đã rút gọn về `kho/…`; **không sửa gì khác**.
- **Kết luận: `changes_requested`.**

---

codex
# Báo cáo cross-review lượt 2/2

## Danh tính và preflight

- Reviewer: `openai_codex`, phiên độc lập với Executor `claude`.
- Execution surface: Codex service; transport: machine.
- Review class: `sensitive`; assurance mục tiêu: `cross_approved`.
- SHA: `175e95bd68556d38a7dde517ce858cb27e821097`.
- Tree: `b5527925ee3040657d2a2fb9875530c0c52cf8f3`.
- Delta bản vá cuối đúng hai tệp: `ops/lease_publish_test.py`, `ops/NO_KY_THUAT.md`.
- Kho cuối lượt sạch; HEAD và tree không đổi.
- Tất cả đột biến chạy trên bản sao toàn cây ngoài `./kho`; các bản sao được chuyển tới `/tmp/rv216r2-review-sandboxes`.

## Findings

### F1 — P2: `t42` giết M4 nhưng vẫn không khóa hết hành vi mà `t34` tuyên bố

Bằng chứng chạy được:

- Baseline: `PYTHONDONTWRITEBYTECODE=1 python ops/lease_publish_test.py` → rc=0, `43/43`.
- M4, đổi:

  ```text
  (?:python3?|py)\s+
  →
  (?:python3?|py)\s+(?:-\S+\s+)?
  ```

  Hành vi đổi từ `3 bắt / 5 lọt` thành `3 bắt / 4 lọt`; `t42` đỏ đúng đích, suite `42/43`, rc=1. F1 lượt trước đã được đóng đối với chính M4.

- M5, siết phần đường dẫn:

  ```text
  \S*lease_publish_test\.py
  →
  (?:ops/)?lease_publish_test\.py
  ```

  Probe `python /tmp/ops/lease_publish_test.py` đổi từ `match=True` thành `match=False`, trong khi tám mẫu hiện có vẫn cho `3 bắt / 5 lọt`; suite vẫn `43/43`, rc=0.

M5 cắt đúng tuyên bố của `t34` rằng ba runner canonical nhận một `<đường-dẫn>/lease_publish_test.py`, nhưng bảng `_DANG_CANONICAL_BI_BAT` chỉ đo ba đường dẫn tương đối giống nhau. Ngoài ra, docstring `t42` tại dòng 2041–2044 vẫn nói đây “không phải ca đo HÀNH VI”, trái với phần triển khai mới tại dòng 2056–2067 đang trực tiếp đo regex.

Bất biến bị cắt: lời khai về miền canonical phải bằng miền hành vi được đo; thay đổi chiều đường dẫn không được sống sót chỉ vì tỷ lệ tám mẫu giữ nguyên.

Gợi ý vá:

- Vá tại `_DANG_CANONICAL_BI_BAT`/`t42`, vì đây là nguồn dữ liệu và phép đo hành vi của regex.
- Dựng ma trận có chủ đích theo các trục runner, đường dẫn tương đối/tuyệt đối, quoting và cờ; không dùng ba mẫu chỉ khác tên runner. Sửa docstring `t42` để khai đúng rằng nó đo cả lời khai lẫn hành vi.
- Ca khóa: M4 phải tiếp tục đỏ; M5 siết `\S*` như trên cũng phải đỏ; các mẫu âm hiện hữu vẫn phải lọt.
- Rủi ro bản vá: ma trận mới vẫn có thể bị đọc thành đặc tả toàn bộ shell. Phải khai rõ các trục được đo và không quảng bá nó thành parser shell.

### F2 — P2: hạ `t43` xuống một chiều làm mất dấu khi marker hiện hữu bị gỡ

Bằng chứng chạy được:

- Trên baseline: marker trong `ci.yml` là hai ID; sổ nợ có bốn ID, trong đó `PLAT-X2` và `launcher_test.py` không có marker. `marker - ledger = ∅`.
- Gỡ marker `PLAT-X5-required-status-check` khỏi `ci.yml`, không đổi mục §9:
  - marker giảm từ 2 xuống 1;
  - mục sổ nợ vẫn là 4;
  - `marker - ledger` vẫn rỗng;
  - suite vẫn `43/43`, rc=0.

Quyết định không ép mọi mục sổ nợ phải có marker là hợp lý cho §7–§8, nhưng triển khai hiện tại không phân biệt “nợ vốn không cần marker” với “nợ §9–§10 đang có liên kết marker và vừa bị gỡ”. Vì vậy liên kết đang tồn tại có thể biến mất im lặng. Docstring dòng 2088 còn tuyên bố “và ngược lại”, trực tiếp mâu thuẫn với phép kiểm một chiều ở dòng 2130.

Bất biến bị cắt: một khoản nợ đã khai là nhà của marker trong mã phải giữ liên kết hai chiều; việc gỡ một đầu không được biến thành trạng thái xanh.

Gợi ý vá:

- Vá tại `t43` và metadata của các mục §9–§10; không ép đối xứng lên toàn bộ sổ nợ.
- Cho mục có liên kết mã khai một backlink máy đọc được, rồi so hai chiều giữa marker trong `ci.yml` và riêng tập mục có backlink. §7–§8 không có backlink nên không báo động giả.
- Ca khóa: gỡ một trong hai marker hiện tại phải làm `t43` đỏ; §7–§8 vẫn xanh khi không có marker; thêm marker mới không có nhà vẫn đỏ.
- Rủi ro bản vá: metadata tự do sẽ tạo thêm một parser lỏng. Cần đúng một cú pháp canonical và ca âm cho mục không liên kết mã.

### F3 — P2: bộ nhận marker báo động giả và không thực thi “đúng một mục”

Bằng chứng chạy được:

1. Thêm một câu văn xuôi vào `ci.yml`:

   ```yaml
   # Câu văn xuôi có chữ NỢ CÓ TÊN nhưng không đặt marker; xem `van-xuoi` để giải thích.
   ```

   `_MARKER_NO` nhận `van-xuoi` làm marker; `t43` đỏ và suite thành `42/43`. Đây là báo động giả do mẫu `^\s*#.*NỢ CÓ TÊN...` cho phép văn bản bất kỳ trước cụm marker.

2. Thêm mục thứ hai có cùng tiêu đề `PLAT-X5-required-status-check` vào sổ nợ. `rg` thấy hai tiêu đề, nhưng suite vẫn `43/43`, vì comprehension chuyển chúng thành `set` và xóa dấu vết trùng. Tên ca hứa “ĐÚNG MỘT mục” nhưng chỉ kiểm “có ít nhất một”.

Bất biến bị cắt: chỉ đúng cú pháp marker mới được nhận; mỗi marker phải ánh xạ tới đúng một mục sổ nợ.

Gợi ý vá:

- Vá `_MARKER_NO`, `_MUC_SO_NO` và phần gom dữ liệu của `t43`.
- Neo marker ngay sau dấu chú thích, chẳng hạn `^\s*#\s*NỢ CÓ TÊN\s*:?\s*`…; dùng `Counter` hoặc danh sách vị trí thay cho `set` để phát hiện tiêu đề trùng.
- Ca khóa: câu văn xuôi trên phải xanh; hai tiêu đề cùng ID phải đỏ; hai cú pháp marker canonical hiện có phải tiếp tục được nhận.
- Rủi ro bản vá: regex quá cứng có thể báo đỏ khi chỉ đổi dấu câu. Chuẩn hóa một cú pháp marker duy nhất sẽ giảm bề mặt này.

### F4 — P2: bản đính chính F2 đã trôi ngay trên chính head hiện tại và vẫn chứa suy luận chưa đo

Bằng chứng chạy được:

```text
PATH=/usr/bin:/bin PYTHONDONTWRITEBYTECODE=1 \
  /usr/local/bin/python ops/lease_publish_test.py
```

Kết quả: rc=1; đúng một ca đỏ là `t33_workflow_dang_lease_phai_qua_actionlint`, thông điệp có `KHÔNG ĐO ĐƯỢC`; tổng hiện tại là `42/43`, không phải `41/42` như `ops/NO_KY_THUAT.md:501`.

Câu “tám lỗi cùng chết vì thiếu một dependency” tại dòng 511 cũng không được phép đo trên chứng minh: lượt chạy chỉ quan sát một ca đỏ và không định danh tám lỗi hay quan hệ nhân quả của chúng. Đây tiếp tục là suy luận được viết dưới dạng kết luận đo được.

Bất biến bị cắt: số đo trong sổ nợ sống phải đúng trên head nó mô tả; điều không đo được phải được khai là không đo được.

Gợi ý vá:

- Vá §9 của `ops/NO_KY_THUAT.md`.
- Bỏ mẫu số động, ghi hẹp rằng thiếu `actionlint` làm đúng `t33` fail-close với `KHÔNG ĐO ĐƯỢC`, rc khác 0. Xóa câu về “tám lỗi”, hoặc ghi rõ đó là suy luận chưa đo và không dùng làm bằng chứng.
- Ca khóa: chạy PATH thiếu công cụ, trích danh sách ca đỏ và đòi đúng `t33`; thêm một ca mới vào suite không được làm tài liệu sai chỉ vì mẫu số đổi.
- Rủi ro bản vá: nếu tiếp tục pin `N/N`, lần thêm test kế tiếp sẽ tái tạo lỗi. Nên neo tên ca và hậu điều, không neo tổng suite.

## Gate và giới hạn đo

- `lease_publish_test.py`: đạt `43/43`, rc=0 trên exact head với `actionlint 1.7.7`.
- `doc-claims-check --strict`: rc=0, `"ok": true`, `flags: []`.
- `git diff --check` trên hai tệp của bản vá: rc=0.
- Nhánh thiếu tệp của `t43` fail-close đúng:
  - thiếu `NO_KY_THUAT.md` → `42/43`, `t43` đỏ;
  - thiếu `ci.yml` → `41/43`, `t43` và `t31` đỏ.
- Full `tl --selftest`: rc=1, `1696/1698`; hai lỗi là `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` và `r268_l2_trichotomy_theo_trang_thai_object`, đúng hai hiện vật sandbox đã được khai tại `docs/AUDIT_LAUNCHER_VONG_7.md`, không phát sinh từ delta hai tệp.
- Không đo được Windows trên exact head trong lượt này.
- Không độc lập đọc GitHub CI/branch-protection; chỉ kiểm được checkout local và bằng chứng trong lease.
- Vì đây là vòng 2/2, các P2 còn mở dẫn tới human Review Rescue Checkpoint; không có lượt review thứ ba.

VERDICT: changes_requested
Reviewed commit: 175e95bd68556d38a7dde517ce858cb27e821097
diff --git a/review_sandboxes/m4/ops/lease_publish_test.py b/review_sandboxes/m4/ops/lease_publish_test.py
index 10671d967d35711be47230b870e1e99792e5092d..5ef777ac021010bf4296728c97785b6393e8aee1
--- a/review_sandboxes/m4/ops/lease_publish_test.py
+++ b/review_sandboxes/m4/ops/lease_publish_test.py
@@ -1340,7 +1340,7 @@
 # và không được nối regex ở packet này. Nợ "CI có chạy gate không" thuộc required
 # status check được nêu ngay trong t34.
 _CHAY_BO_TEST = __import__("re").compile(
-    r"""(?<![\w.])(?:python3?|py)\s+["']?\S*lease_publish_test\.py["']?""")
+    r"""(?<![\w.])(?:python3?|py)\s+(?:-\S+\s+)?["']?\S*lease_publish_test\.py["']?""")
 
 
 def _goi_actionlint_gia(dich, ver, than):
diff --git a/review_sandboxes/m5a/ops/lease_publish_test.py b/review_sandboxes/m5a/ops/lease_publish_test.py
index 10671d967d35711be47230b870e1e99792e5092d..097f811acbac57f5252b609b92202503efa8299c
--- a/review_sandboxes/m5a/ops/lease_publish_test.py
+++ b/review_sandboxes/m5a/ops/lease_publish_test.py
@@ -1340,7 +1340,7 @@
 # và không được nối regex ở packet này. Nợ "CI có chạy gate không" thuộc required
 # status check được nêu ngay trong t34.
 _CHAY_BO_TEST = __import__("re").compile(
-    r"""(?<![\w.])(?:python3?|py)\s+["']?\S*lease_publish_test\.py["']?""")
+    r"""(?<![\w.])(?:python3?|py)\s+["']?(?:ops/)?lease_publish_test\.py["']?""")
 
 
 def _goi_actionlint_gia(dich, ver, than):
diff --git a/review_sandboxes/m5b/ops/lease_publish_test.py b/review_sandboxes/m5b/ops/lease_publish_test.py
index 10671d967d35711be47230b870e1e99792e5092d..e6e061123e60b59ccb7ab3ec7a0c94b6e9f6ee68
--- a/review_sandboxes/m5b/ops/lease_publish_test.py
+++ b/review_sandboxes/m5b/ops/lease_publish_test.py
@@ -1340,7 +1340,7 @@
 # và không được nối regex ở packet này. Nợ "CI có chạy gate không" thuộc required
 # status check được nêu ngay trong t34.
 _CHAY_BO_TEST = __import__("re").compile(
-    r"""(?<![\w.])(?:python3?|py)\s+["']?\S*lease_publish_test\.py["']?""")
+    r"""(?<![\w.])(?:python3?(?:\.exe)?|py)\s+["']?\S*lease_publish_test\.py["']?""")
 
 
 def _goi_actionlint_gia(dich, ver, than):
diff --git a/review_sandboxes/t43_duplicate/ops/NO_KY_THUAT.md b/review_sandboxes/t43_duplicate/ops/NO_KY_THUAT.md
index f1fdacca0a696c8ba3e5277894d478bf3c2d4358..735a577bb03fee170451fb11cee180d5c7e4e4cf
--- a/review_sandboxes/t43_duplicate/ops/NO_KY_THUAT.md
+++ b/review_sandboxes/t43_duplicate/ops/NO_KY_THUAT.md
@@ -541,3 +541,7 @@
 
 **Điều kiện coi là XONG:** bước ấy chạy được trên `windows-latest` với bằng chứng DƯƠNG
 (`N/N` hai số bằng nhau) trên một lượt CI thật, và `if:` được gỡ hoặc thu hẹp kèm lý do.
+
+## 11. `PLAT-X5-required-status-check` — bản ghi trùng do lỗi hợp nhất
+
+Đây là một mục trùng tên dùng để đo bất biến “đúng một mục”.
diff --git a/review_sandboxes/t43_prose/.github/workflows/ci.yml b/review_sandboxes/t43_prose/.github/workflows/ci.yml
index c93bf40290219c17b5a2f914687f6754d022436e..fa0475bb3259ae20a83b86168e2d1b6accc09a3f
--- a/review_sandboxes/t43_prose/.github/workflows/ci.yml
+++ b/review_sandboxes/t43_prose/.github/workflows/ci.yml
@@ -127,6 +127,7 @@
       # Nâng bản là việc CÓ CHỦ ĐÍCH — đổi số ở đây, đừng để PyPI đổi hộ.
       - name: cài PyYAML (bộ cổng đăng lease cần)
         run: python -m pip install --quiet PyYAML==6.0.3
+      # Câu văn xuôi có chữ NỢ CÓ TÊN nhưng không đặt marker; xem `van-xuoi` để giải thích.
       # Cài + đối chiếu `actionlint` và chạy selftest trong MỘT lời gọi. Hai bước YAML
       # riêng từng cho phép installer nằm ở job khác, sau selftest, hoặc bị `if: false`:
       # có mặt trong YAML nhưng không cấp công cụ cho lần chạy. Wrapper gọi lại
diff --git a/review_sandboxes/t43_remove/.github/workflows/ci.yml b/review_sandboxes/t43_remove/.github/workflows/ci.yml
index c93bf40290219c17b5a2f914687f6754d022436e..6ed1b4a8db3f938130525abc0e57b6087c63bf1c
--- a/review_sandboxes/t43_remove/.github/workflows/ci.yml
+++ b/review_sandboxes/t43_remove/.github/workflows/ci.yml
@@ -132,7 +132,7 @@
       # có mặt trong YAML nhưng không cấp công cụ cho lần chạy. Wrapper gọi lại
       # `cai_actionlint.sh`, không chép logic cài.
       #
-      # NỢ CÓ TÊN `PLAT-X5-required-status-check`: selftest không thể tự chứng minh job
+      # Selftest không thể tự chứng minh job
       # này thật sự được GitHub gọi. Branch protection phải require status của job `gate`;
       # t34 chỉ còn canh lời gọi thẳng tệp `.py`, không giả làm bộ phân tích shell.
       - name: lease-publish selftest (cài công cụ + chạy cổng)

