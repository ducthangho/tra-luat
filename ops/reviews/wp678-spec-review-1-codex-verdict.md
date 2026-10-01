verdict: changes_requested
reviewed_sha: 342e62c7a23fe03780539e2395c1e24832648c91
spec_sha256: 578916a9b04965b178e5dcaf949c725771129d0cb4d4e13f216adb5056d5fa7c
model/effort tự khai: GPT-6 theo cấu hình phiên / exact model phục vụ và effort không có runtime evidence để tự xác minh
provider: openai_codex
execution_surface: API agent có công cụ shell cục bộ; không tự nhận đã đo Codex CLI/Desktop
transport: machine (ghi hiện vật cục bộ); không có GitHub submitter
reviewed_tree: e6ab8444f000df78bd81bd81cefb564dd5d88456
base_sha: 1741e0a1ab7ebce4b26912aefadca56ddfcdc691
assurance: review nội dung độc lập theo chỉ thị; không tự cấp cross_approved/land authority

Q1/Q2 có thể đóng va chạm ép kiểu YAML, nhưng hợp đồng nghiệm thu còn cho mutant sống ở A2/A5 và phép quét A9 bỏ sót miền. Đề nghị revision mới trước thi hành. Không có lớp P1 đã được chứng minh; các lỗi tiêu chí không đỏ được xếp P2 theo thang của prompt, không thổi thành khẳng định không tồn tại cách triển khai nào đạt spec.

Mọi lệnh dưới đây lấy `$R` là thư mục tuyệt đối người dùng đã cấp, mặc định cwd=$R. Các script bằng chứng nằm trong `goi/`; mọi repo fixture, mã đột biến, tempfile và bản sao áp patch nằm dưới thư mục `mktemp -d -p "$R"`. Thời điểm chính xác của các phép đo nằm trong log UTC. Không gọi mạng, không đăng GitHub. Các số lịch sử từ phiên soạn được phân biệt với kết quả tái đo; không tự coi lịch sử thiếu log là sai.

Đã đọc toàn bộ prompt.snapshot. Hai phép kiểm định danh ban đầu khớp:
```
$ sha256sum SPEC.md
578916a9b04965b178e5dcaf949c725771129d0cb4d4e13f216adb5056d5fa7c  SPEC.md
$ git -C cay-kho rev-parse HEAD
342e62c7a23fe03780539e2395c1e24832648c91
```

## BẢNG LỚP

| slug lớp | hạng | biểu hiện (vị trí trong SPEC) | phương án chung | phép kiểm / giới hạn |
|---|---|---|---|---|
| tieu-chi-dot-bien-khong-phan-biet-chot | P2 | A2 dòng 132–134; A5 dòng 147–151; liên hệ §6.7/#677/A10 | Đo trực tiếp đúng chốt và từng toán hạng, sửa lời khai L/t178 cùng hợp đồng tương tác | `probes.py`, `acceptance_probe.py`: mutant D2, D5_peer, D6_self sống; chỉ mô hình tạm, chưa có implementation PR |
| bo-quet-nghiem-thu-thieu-mien | P2 | A9 dòng 166–168, phép quét §8 dòng 180–182 | Định nghĩa miền runtime, kiểm lỗi và mẫu số, self-test bộ quét | `draft_controls.py`: lease `.yml` sai kiểu và hồ sơ lỗi bị bỏ qua; snapshot thật sạch |
| so-do-nen-khong-khop | P2 | A6 dòng 154; §8 dòng 176–182; cập nhật nền A8 | Đo lại số hạng/rc kèm UTC, lệnh, điều kiện; giữ lịch sử đúng nhãn | A6 rc=11, snapshot 505 ref; suite 187/187, không phủ nhận log lịch sử 185/187 chưa được cấp |
| hop-dong-dong-bang-thieu-neo | P2 | bảng đầu dòng 3–13, thiếu trường và công thức băm | Chốt đủ hợp đồng §3.2, dẫn nguồn authoritative, đặt hash ngoài bytes được băm | grep và đọc protocol; nội dung Issue #678/mission/environment thật KHÔNG ĐO ĐƯỢC |
| bang-duong-phan-loai-sai | P3 | D7/D8/D9 dòng 62–64; làm rõ A7 | Chia theo hàm thật và vai trò so danh tính/hiển thị; phân hai CLI DU_BAO | `identity-paths.log`, `probes.py`; không phát hiện đường quyết định ngoài D1–D8 |
| trang-thai-q3-chua-dong-bo | P3 | Q3 dòng 77–78 và §10 dòng 204–205 | Đồng bộ trạng thái xác nhận theo authority đã giao, không hỏi lại | Prompt xác nhận Q1–Q4; không có GitHub receipt để tự kiểm object ID |

Đếm lớp từ các hàng trên bằng `python goi/verify_artifacts.py` (kết quả ở cuối báo cáo). Hạng là hạng cao nhất trong lớp; A2 và A5 chung hình dạng “mutant riêng của chốt không đổi quan sát của ca được chỉ định”, không đếm mỗi toán hạng thành finding mới.

## BẢNG SĂN

### HƯỚNG 1: Kiểm kê đường danh tính và thứ tự gọi
- Giả thuyết: bảng D1–D9 gán nhầm đường hiển thị thành đường danh tính, hoặc bỏ một consumer chạy trước chốt.
- Lệnh đã chạy: `rg -n 'lease_id|thay_the_cho|da_bi_thay_the|cap_lai_cho|\.stem|name\[:-5\]' cay-kho/ops/lease_publish.py` (toàn output: `goi/identity-paths.log`); đọc các hàm từ dòng 561–620, 667–694, 861–870, 949–1003, 1050–1076, 1920–1972, 2060–2147.
- Output thật, trích:
  ```text
  1967: lid = str(muc["lease"].get("lease_id") or "?")
  2102: for dong in _du_bao_ai_dang_giu(...):
  2110: lease_id = str(lease.get("lease_id") or "<thiếu lease_id>")
  2123: nguoi_giu[lease_id] = None
  2139: lease_id = str(lease.get("lease_id") or "<thiếu lease_id>")
  2143: lease_id = str(lease.get("lease_id") or "<thiếu lease_id>")
  ```
- Kết luận: LỖI về phân loại/khẳng định trong §2: D8 gồm cả ép `str()` ở 1967, không chỉ so giá trị thô; 2139/2143 thuộc `lenh_con_tro_treo`, chỉ in báo cáo, không thuộc `lenh_ai_dang_giu`. D9 bỏ hai vị trí hiển thị này. `--du-bao` của `ai-dang-giu` chạy trước vòng kiểm D7 và không gọi D1; cần đo riêng với đường `check --du-bao`. Chưa tìm thấy một đường quyết định danh tính nào ngoài tập D1–D8; đây không phải bằng chứng bảo đảm mọi biến thể đều đã được phủ.

### HƯỚNG 2: Tiêu chí đột biến có bị chốt khác che?
- Giả thuyết: A2 đòi gỡ D2 làm lời gọi GitHub tăng, nhưng Q2/D3 chặn trước `_doc_gh` nên không thể tăng.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 TMPDIR="$R/tmp.PhJBxuiZ59" python "$R/goi/probes.py"` (script và `probes.log` lưu trong gói).
- Output thật:
  ```text
  A2 baseline 5 probe= RETURN GH_calls= 1 D2_direct= 0
  A2 D1_D4 5 probe= RETURN GH_calls= 0 D2_direct= 8
  A2 restore_D2 5 probe= RETURN GH_calls= 0 D2_direct= 0
  A2 L_remove_D2 5 probe= RETURN GH_calls= 0 D2_direct= 0
  t178 D1_D4 PASS
  t178 restore_D2 PASS
  t178 L_remove_D2 PASS
  A7 ai-dang-giu D1 strict: D8_types= ['str', 'int'] rc= 11
  DU_BAO: 1000 MAP_REF 1 ref
  ```
- Kết luận: LỖI. A2 không đỏ theo đột biến chỉ định; A10 sẽ bắt sống sót dù sản phẩm làm đúng Q1/Q2. Cần đo D2 trực tiếp hoặc seam xác nhận chuyển giao sang D3, giữ phép đo 0 GitHub cho toàn phép dò. A7 phải phân riêng `check --du-bao` và `ai-dang-giu --du-bao`; đường sau tới D8 trước D7, không có D1.
- Giới hạn: `D1_D4` là mô hình tối thiểu trên tệp sao tạm, chỉ thêm chốt chung đúng Q1 cho D1–D4; chưa phải mã thi hành hoàn chỉnh. Không dùng kết quả này làm chứng cứ ứng viên đã đạt suite. Các phép thử đo lời gọi và kiểu thật; không phân loại chúng thành mutant đã giết bằng tín hiệu của ca chưa tồn tại.

### HƯỚNG 3: Fixture A5/A6 và mã thoát thực tế
- Giả thuyết: suite không dựng được repo/ref thật, hoặc A6 khai sai mã thoát nền.
- Lệnh: `rg -n '^def _.*(kho|gh|buoc)|^class GhGia' cay-kho/ops/lease_publish_test.py`; chạy `goi/probes.py` như hướng 2.
- Output thật:
  ```text
  193:class GhGia:
  555:def _buoc_workflow(ten: str) -> dict:
  1506:def _kho_thu(tmp: Path):
  2703:def _chay_buoc_dang(...):
  A5 baseline old_id= 1000 _kiem_bia_mo= 0 _bia_mo_doi_xung= True
  A5 baseline old_id= '1000' _kiem_bia_mo= 0 _bia_mo_doi_xung= True
  A6 baseline rc= 11
  CÒN_HẠN True refs/heads/on:ops/leases/on.yaml
  CÒN_HẠN True refs/heads/yes:ops/leases/yes.yaml
  NGƯỜI_GIỮ 1: True
  ```
- Kết luận: LỖI ở con số A6 (người giữ còn sống ⇒ rc=11). KHÔNG PHẢI LỖI về khả năng dựng fixture: `_kho_thu` + `viet` dựng được git thật và các ref. A5 baseline chứng minh lỗi đang có; đây chưa là phép giết đột biến bản sửa. Hai vị trí đọc lease cũ/mới trong mỗi D5/D6 cần các vế riêng nếu muốn khai mỗi chốt đều được đo.

### HƯỚNG 4: Miền chuỗi Q1 và biểu diễn YAML
- Giả thuyết: Unicode/khoảng trắng vẫn lọt regex rồi gộp hai chuỗi khác nhau; tag/khóa lặp chứng minh Q1 không đóng đúng phạm vi đã hứa.
- Lệnh: `goi/probes.py` (các vế `Q1` đọc bằng `_doc_yaml`).
- Output thật:
  ```text
  'yes' -> 'yes' str regex=True
  !!str 1.5 -> '1.5' str regex=True
  '1.5' -> '1.5' str regex=True
  "a b" -> 'a b' str regex=False
  "a\n" -> 'a\n' str regex=False
  "é" -> 'é' str regex=False
  "é" -> 'é' str regex=False
  "A" -> 'A' str regex=True
  "a" -> 'a' str regex=True
  Q1 duplicate -> {'lease_id': 'fresh'}
  ```
- Kết luận: KHÔNG PHẢI LỖI trong phạm vi Q1: các cách viết ra cùng chuỗi sau load cố ý là cùng ID; hai chuỗi ASCII khác nhau giữ nguyên, Unicode/khoảng trắng bị regex loại. Khóa YAML lặp được PyYAML lấy giá trị cuối, nhưng không có mâu thuẫn giữa các consumer cùng đọc dict sau load. Chưa có yêu cầu chặn khóa lặp hoặc bảo toàn cách viết YAML; không tự mở packet sang những việc ấy.

### HƯỚNG 5: Biên workflow A3, giữ trạng thái thật
- Giả thuyết: lời khai rc=0/0 POST của §1/A3 chỉ là suy từ unit, hoặc giàn thử khiến đối chứng dương cũng không đăng được.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 TMPDIR="$R/tmp.PhJBxuiZ59" python "$R/goi/workflow_probe.py"`.
- Output thật (`goi/workflow.log`):
  ```text
  base yes rc=0 POST=0 calls=2
  base 'fresh-id' rc=0 POST=1 calls=4
  D1_D4 yes rc=1 POST=0 calls=0
  D1_D4 'fresh-id' rc=0 POST=1 calls=4
  ```
- Kết luận: KHÔNG PHẢI LỖI. A3 khả thi và có răng chống nền: script lấy nguyên thân `đăng` bằng `_buoc_workflow`, chạy Python sản phẩm và `gh` giả trên PATH, lưu comment/state sau mỗi lời gọi. Có sẵn bộ trích và fixture Git, nhưng `_chay_buoc_dang` hiện thay Python sản phẩm bằng stub và thay cả lệnh gh: executor cần harness mới/tái cấu trúc trong đúng `ops/lease_publish_test.py`, không được lấy rc của stub làm bằng chứng cho A3. Không cần sửa workflow. Ca unit D3 là cần thiết vì D1 sẽ che khi chỉ đo workflow.

### HƯỚNG 6: Thử thước đo nháp và miền quét A9
- Giả thuyết: `quet.py` im lặng bỏ lease sai kiểu hoặc sai cấu trúc nên A9 xanh giả.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 TMPDIR="$R/tmp.PhJBxuiZ59" python "$R/goi/draft_controls.py"`; đọc script `quet.py`; đối chiếu `_quet_lease_toan_kho` và `_cac_ref_cuc_bo`.
- Output thật, trích:
  ```text
  DRAFT quet.py: rc=0
  refs=1 blob_yaml=5 parse_loi=0 kieu_lease_id={'str': 3}
  []
  INDEPENDENT bad-type.yml ['lease_id']
  INDEPENDENT missing.yaml ['lease_id']
  INDEPENDENT wrong-shape.yaml ['not_mapping']
  INDEPENDENT bad-pointer.yaml ['da_bi_thay_the']
  ```
- Kết luận: LỖI. Thước nháp chỉ đọc `.yaml` trên origin, bỏ `.yml`, bỏ ánh xạ thiếu ID và tài liệu không phải ánh xạ; nhận `da_bi_thay_the` là list dù sản phẩm chỉ nhận str. Git lỗi cũng không được kiểm rc. §8/A9 chưa định nghĩa thuật toán/lệnh có self-test cho kết luận “mọi lease trên mọi ref”; một lease sai kiểu trên nhánh local hoặc `.yml` không bị chặn bởi phép đo đó. Đây là thiếu miền nghiệm thu, không phải bằng chứng snapshot hiện có lease hỏng.
- Hai công cụ còn lại đã thử đối chứng biết trước: `do_bang.py` cho `'yes'` là `str` và qua cả hai hàm, `null`/`~` cho `kiem` rc=8; `do_va_cham.py` cho khác tên rc=0 và chuỗi cùng tên rc=9. Các dòng §1 và sáu cặp va chạm đều tái hiện (`goi/draft-controls.log`). Không trao độ tin của hai script này cho bộ quét.

### HƯỚNG 7: Số hạng nền và suite thật
- Giả thuyết: quan hệ sạch vẫn đúng nhưng số ref/số ca đã trôi.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 TMPDIR="$R/tmp.PhJBxuiZ59" python "$R/goi/measure.py"`; `PYTHONDONTWRITEBYTECODE=1 TMPDIR="$R/tmp.PhJBxuiZ59" python "$R/cay-kho/ops/lease_publish_test.py" > "$R/goi/suite.log" 2>&1`.
- Output thật:
  ```text
  refs=505 mirror_heads=505 name+oid_equal=True
  scan unique_blobs=559 blob_path_pairs=559 types={'str': 559}
  parse_errors=0 non_mapping_or_missing_id=0 bad=[]
  ops/lease_publish.py lines=2206 same_as_base=True
  ops/lease_publish_test.py lines=10508 same_as_base=True
  CA=187 max=192
  NGƯỜI_GIỮ 0: không có
  OFFLINE ops/lease_publish.py rc=0
  NGƯỜI_GIỮ 1: t131-deadline-dem-spawn-exec-1-claude-20260929
  OFFLINE ops/lease_publish_test.py rc=11
  workflow lease_id lines=0
  suite_rc=0
  lease_publish: 187/187 đạt; đã chạy=187, bỏ qua=0
  ```
- Kết luận: LỖI về số ref còn khai 503 (§8); 559/559, kích thước và số ca vẫn khớp. 185/187 là số lịch sử với công cụ thiếu, không phải kết quả hiện tại: sandbox có shellcheck 0.9.0, actionlint 1.7.7 và chạy đủ 187/187. Không suy số đo mới phủ nhận một lượt lịch sử chưa có log. Cần ghi lại số đối chiếu hiện tại cùng thời điểm, điều kiện và lệnh.
- Giới hạn: đối chiếu tên+OID với mirror được cấp, không đo máy chủ HTTPS live. `ai-dang-giu` dùng tên nhánh từ chính mirror thay riêng `_ten_nhanh_may_chu`; đọc blob, ref, bia mộ và đồng hồ thật. Không giả rằng `ls-remote` đã chạy. Runtime scan chỉ quét lease hoạt động, phép đếm độc lập còn quét `ops/leases_retired/` và cả hai suffix.

### HƯỚNG 8: Q3 có kéo sửa ngoài write set?
- Giả thuyết: workflow/consumer coi mọi nonzero là lỗi hoặc đòi định dạng cũ khiến Q3 cần sửa thêm tệp.
- Lệnh: `rg -n 'ai-dang-giu' cay-kho/.github cay-kho/.claude/skills cay-kho/.agents/skills cay-kho/.claude/dev -g '*.py' -g '*.md' -g '*.yml' > goi/callers.log`; `rg -l 'ai-dang-giu' cay-kho/.github cay-kho/.claude cay-kho/.agents cay-kho/ops -g '*.py' -g '*.sh' -g '*.yml' -g '!**/reviews/**' -g '!lease_publish*'`; đọc `lenh_ai_dang_giu`.
- Output thật: `wc -l goi/callers.log` ⇒ `0`; tìm rộng hơn chỉ có `ops/dung_goi_review.sh`, hai chỗ nhắc nằm trong chú thích giải thích phạm vi quét.
- Kết luận: KHÔNG PHẢI LỖI đã chứng minh về L2. Không thấy caller vận hành tự động bên ngoài cần sửa; hiện caller là CLI/doctrine cho người vận hành. Q3 cố ý đổi lease hỏng sang không xác định. Không tuyên bố mọi tài liệu vận hành đều đúng hoặc mọi consumer ngoài kho đã được đo. Điều cần lưu ý trong A6 là rc=11 đã khác 0 trên nền, nên phải chốt nhãn KHÔNG_XÁC_ĐỊNH và từng lease, không chỉ `rc != 0`.

### HƯỚNG 9: Tương tác #677 / L và hồ sơ đóng băng
- Giả thuyết: sau D3, mutant L không còn chạm GitHub nhưng spec vẫn giữ lời khai t178 là chốt phân biệt; metadata chưa đủ để thực thi theo protocol.
- Lệnh: `goi/probes.py` như hướng 2; `rg -n 'spec_hash|environment|risk|mission_issue' SPEC.md`; đọc protocol §3.2, §4, §8, §13 và skill soan-spec §2/§4; `git -C cay-kho rev-list --objects --all | rg ' .*(dot.bien.l|bien.cong.khai)'`.
- Output thật: các bản `D1_D4`, `restore_D2`, `L_remove_D2` đều `t178 PASS`; grep metadata rc=1, không có dòng; tìm tên hiện vật #677 không có kết quả (`goi/packet677-search.log`).
- Kết luận: LỖI cùng lớp chốt-che-chốt của hướng 2: không chỉ D1 thay đổi lời khai; D3 làm L mất sức phân biệt. §6.7 mới yêu cầu sửa lời khai hiện trạng nhưng chưa nói rõ đột biến/đường đo của #677 phải tái định nghĩa; không sửa đặc tả #677 ngoài write set, cần điều phối neo revision/acceptance tương thích.
- Schema: đủ các mục bắt buộc của bảng skill §4; thiếu `environment`, `risk`, `mission_issue` và công thức/nguồn `spec_hash` theo protocol §3.2. Không thể suy environment từ tên executor; `review_class` không thay trường risk. Không có nội dung Issue #678 trong gói nên không khẳng định Issue cũng thiếu; vấn đề là tệp tự nhận hợp đồng đóng băng chưa chỉ chỗ tự xác minh các trường ấy. Q3/§10 còn khai “chưa được xác nhận” trong khi authority của lượt review đã xác nhận Q1–Q4; cần đồng bộ văn bản ở revision sau, không hỏi chủ kho lại.

### Bổ sung hướng 2/3: đo từng toán hạng của A5
Lệnh: `PYTHONDONTWRITEBYTECODE=1 TMPDIR="$R/tmp.PhJBxuiZ59" python "$R/goi/acceptance_probe.py"`.
Output thật (`goi/acceptance.log`):
```text
A5 strict_D5_D6 results=[(8, False), (0, True)] PASS
A5 D5_self results=[(8, True), (0, True)] TinHieuChotCa A5 literal
A5 D5_peer results=[(8, False), (0, True)] PASS / mutant survives
A5 D6_self results=[(8, False), (0, True)] PASS / mutant survives
A5 D6_peer results=[(0, False), (0, True)] TinHieuChotCa A5 literal
```
Kết luận: fixture A5 viết nguyên văn chỉ đổi kiểu lease cũ. Nó giết ép kiểu lease cũ trong D5 và lease quét trong D6; ép kiểu lease được quét trong D5 và lease chủ thể trong D6 vẫn sống. Cần thêm vế đổi kiểu ở đầu còn lại; không gộp việc hoàn nguyên cả hàm thành bằng chứng mỗi chốt đều có răng. Mô hình chốt D5/D6 chỉ chạy trong bản sao tạm, không phải bản vá sản phẩm.

Cùng lệnh đo A1 qua `_doc_yaml`: từng dạng `true yes on 1.5 1.50 0x1F 017 1_000 5 2026-09-29` cho strict rc=8 / trả riêng D1 về cũ rc=0; `'yes'` đối chứng rc=0 ở cả hai. A3 unit strict rc=8 / trả riêng D3 về cũ rc=9. A4 strict rc=8 / gỡ riêng D4 trả thân `**Lease True**` (dấu backtick đầy đủ trong log). Các tiêu chí này phân biệt được.

Ruff: `python -m ruff --version` và `python -m ruff check --no-cache --select F cay-kho/ops/lease_publish.py cay-kho/ops/lease_publish_test.py` đều rc=1: `No module named ruff`. Trạng thái **KHÔNG ĐO ĐƯỢC**, không gọi đó là delta F=0. PR chỉ thêm đặc tả, hai tệp Python có cùng blob với base; chưa có ứng viên thi hành để chạy delta A8.


## BẢNG ĐO

Lệnh tái lập cho §1: `python goi/draft_controls.py` với `PYTHONDONTWRITEBYTECODE=1` và TMPDIR như hướng 6; probe độc lập `_doc_yaml`/chốt ở `goi/acceptance_probe.py`. Lệnh cho §8: `python goi/measure.py` như hướng 7. Lệnh cho số dòng: `rg -n 'lease_id|thay_the_cho|da_bi_thay_the|cap_lai_cho' cay-kho/ops/lease_publish.py` và `sed -n '760,780p' cay-kho/.claude/dev/packet_loop.py`.

| khẳng định trong spec | spec khai | đo được | khớp? |
|---|---|---|---|
| §1 true/yes/on/True | bool → `True`, D2=8, kiem qua | Đúng từng giá trị (`draft-controls.log`) | Có |
| §1 1.5/1.50 | float → `1.5`, D2=8, kiem qua | Đúng từng giá trị | Có |
| §1 0x1F | int → `31`, D2/kiem qua | Đúng | Có |
| §1 017 | int → `15`, D2/kiem qua | Đúng | Có |
| §1 1_000 | int → `1000`, D2/kiem qua | Đúng | Có |
| §1 2026-09-29 | date, D2=8, kiem qua | Đúng | Có |
| §1 'yes' | str, D2/kiem qua | Đúng | Có |
| §1 va chạm | sáu cặp rc=9, khác tên rc=0 | cả sáu rc=9; khác tên rc=0; cùng chuỗi thật rc=9 | Có |
| §1/A3 workflow nền | chưa tái đo; dự kiến rc=0/0 POST | rc=0/0 POST; đối chứng rc=0/1 POST | Đã xác nhận phạm vi thân bước |
| D1 | :861 | :861 | Có |
| D2 | :949 | :949 | Có |
| D3 | :668 | :668 | Có |
| D4 | :1070 | :1070 | Có |
| D5 | :587/:592 | :587/:592 | Có |
| D6 | :609/:612 | :609/:612 | Có |
| D7 | :2110/:2139/:2143 cùng thuộc ai-dang-giu | :2110 lấy ID, :2123 lập khóa; :2139/:2143 thuộc con-tro-treo | Không, phân loại sai |
| D8 | :1938/:1942/:1946/:1967 so thô | số dòng đúng; :1946 f-string, :1967 str rồi tra tập | Không, mô tả cơ chế sai |
| D9 | :2074/:2089 chỉ hiển thị | đúng, còn :2139/:2143 cũng chỉ hiển thị | Thiếu phân loại |
| Sổ thu hồi | :1192 đã đòi chuỗi | lấy ID :1192, kiểm str+regex+tên tệp :1193 | Có, mốc vùng mã đúng |
| packet_loop | :769–771 đã đòi chuỗi | vòng trường :769, đọc :770, kiểm str :771 | Có |
| Workflow | 0 dòng đọc lease_id | 0 dòng khớp trong `*.yml`; thân đăng không đọc ID trực tiếp | Có |
| §8 ref | 503/503, thiếu/thừa=0 ở thời điểm cũ | 505 origin ref / 505 mirror head, map tên+OID bằng nhau | Số hạng trôi; live KHÔNG ĐO ĐƯỢC |
| §8 người giữ .py | 0 | 0, rc=0 ở snapshot/offline seam | Có trong giới hạn đã khai |
| §8 người giữ test | 1, lease t131 được nêu tên | 1 đúng lease ấy, rc=11 | Có trong giới hạn đã khai |
| §8 blob YAML | 559 | 559 blob, 559 cặp (blob,path) | Có |
| §8 kiểu ID | str 559/559 | str 559/559; không ánh xạ/thiếu ID=0 | Có |
| §8 pointer sai kiểu/parse | 0 / 0 | 0 / 0 theo phép đo độc lập phân schema | Có |
| §8 kích thước sản phẩm/test | 2206 / 10508 dòng | 2206 / 10508 dòng | Có |
| §8 số ca/max | 187 / t192 | `len(CA)=187`, max số tiền tố=192 | Có |
| A6 rc nền | 0 | 11, NGƯỜI_GIỮ 1: True | Không |
| A8 nền | 185/187 khi thiếu shellcheck | 187/187; đã chạy=187, bỏ qua=0, rc=0 | Khác điều kiện môi trường; không phải hồi quy |
| A8 Ruff | delta F=0 khi thi hành | module Ruff vắng, rc=1 trước khi lint | KHÔNG ĐO ĐƯỢC |

## ĐỐI CHIẾU TỪNG TIÊU CHÍ A1–A10

| tiêu chí | khả năng đỏ và chốt che | bằng chứng / việc executor phải làm |
|---|---|---|
| A1 | Có răng khi gọi kiem trực tiếp không tep/không neo prompt như §1 | Mọi scalar âm: strict=8, trả D1 cũ=0; chuỗi đối chứng cùng 0 (`acceptance.log`) |
| A2 | Chưa đủ răng: D3 giữ 0 GH dù trả D2 nhận int | D2 trực tiếp 8→0; phép dò vẫn RETURN/0; không buộc chuyển kiểm D3 xuống sau mạng |
| A3 | Workflow đỏ trên nền; unit D3 tách được D1 | workflow nền 0/0 POST, mô hình 1/0 POST, đối chứng 0/1; unit D3 8→9 |
| A4 | Có răng nhờ gọi trực tiếp dung_than | gỡ D4: rc=8→trả thân True |
| A5 | Chỉ hai toán hạng được phân biệt bởi fixture đã viết | D5_self/D6_peer đỏ bằng TinHieuChotCa của phép A5 mô phỏng; D5_peer/D6_self sống. Cần cả hai chiều |
| A6 | Nhãn thay đổi là quan sát có răng; rc!=0 riêng lẻ thì mù | Nền 11 và NGƯỜI_GIỮ; Q3 đòi KHÔNG_XÁC_ĐỊNH cho từng ref/path; cần chốt không dừng báo chỉ lease đầu |
| A7 | Khả thi nếu phân từng entry point | check qua D1; ai-dang-giu tới D8 với int trước D7. Không viện kết quả một đường cho đường còn lại; đơn vị D8 tránh che bởi caller |
| A8 | Có răng với ca mới đỏ/lỗi F mới | Baseline suite đã đo; delta với ứng viên chưa tồn tại là not_run; Ruff unavailable. Không tự miễn lỗi mới dưới nhãn thiếu shellcheck |
| A9 | Chưa đủ răng nếu dùng phép quét nháp | Fixture known-answer cho thấy âm giả; cần self-test tập ref/suffix/lỗi/shape như HINT |
| A10 | Nguyên tắc phân loại đúng, nhưng không cứu A2/A5 | Phải công bố target name + exception identity + cause; không đổi mutant chỉ để bảng xanh. Full mutant catalog của executor chưa có nên KHÔNG ĐO ĐƯỢC |

## CHI TIẾT TỪNG LỚP

### tieu-chi-dot-bien-khong-phan-biet-chot [P2] Ca chỉ định không phân biệt được chốt bị gỡ
VỊ TRÍ: §7 A2 (132–134), A5 (147–151), A10; §6.7 và liên hệ #677 trong §3/§9.

VẤN ĐỀ: D2 và D3 dùng cùng validator. Cài chốt D3 trước `_doc_gh` là triển khai hợp lý của Q2 nhưng làm mutant D2 ở A2 sống: phép dò vẫn trả về, không chạm GitHub. Spec không nên ép executor thực hiện I/O trước kiểm kiểu để cứu một chỉ số không còn phân biệt được. D3 cũng làm mutant L gỡ D2 mất răng ở t178. Riêng A5, đổi kiểu mỗi lease cũ không thử đầu mới: trả ép kiểu ở D5 :592 hoặc D6 :609 vẫn xanh. Chung cách chữa là ghim ca ở đúng chốt/toán hạng với dữ liệu làm thay đổi quan sát.

HINT: có — nhóm cùng slug; đo D2 trực tiếp, giữ chốt tích hợp 0 GH; thêm chiều A5 còn lại; điều phối đối chiếu #677, executor chỉ sửa hai tệp được cấp.

ĐÃ THỬ: `goi/probes.py` và `goi/acceptance_probe.py` như hướng 2/3. Đột biến D2 vẫn 0 lời gọi; direct 8→0; t178 vẫn PASS. A5 D5_peer/D6_self vẫn `[(8, False),(0, True)]`, trong khi D5_self/D6_peer đỏ bằng `TinHieuChotCa`. Script ghi rõ các phiên bản chỉ là mô hình chốt tạm. Nội dung đầy đủ đặc tả #677 không có hiện vật tên tương ứng tìm được, không kết luận về từng A của packet ấy.

ĐỘ TIN: cao cho hành vi đã chạy; vừa cho ảnh hưởng quy trình của #677 do thiếu nội dung Issue. Ca khóa phải giữ cả kết quả trả về lẫn số lời gọi; chỉ thêm chốt đếm có thể tái tạo tín dụng giả.

### bo-quet-nghiem-thu-thieu-mien [P2] Phép quét chứng nhận một tập hẹp hơn miền runtime
VỊ TRÍ: A9 (166–168), §8 (180–182), liên hệ `quet.py` được giao làm công cụ nền.

VẤN ĐỀ: “mọi ref” chưa có lệnh/miền xác định trong spec. Công cụ đã dùng lọc origin và `.yaml`; runtime `_cac_ref_cuc_bo` đọc heads/remotes, `_quet_lease_toan_kho` nhận `.yaml`/`.yml`. Công cụ còn bỏ non-dict/thiếu ID, nhận list cho `da_bi_thay_the`, và không kiểm rc Git. Vì thế A9 có thể qua ngay khi một lease hoạt động sắp bị Q1 chặn. Đó là thiếu tiêu chí kiểm bộ quét, không phải finding yêu cầu sửa scanner sản phẩm.

HINT: có — nhóm cùng slug; định nghĩa tập, schema, lỗi, mẫu số và ca tự kiểm ngay trong test file. Ghi cách chạy trong handoff. Không thêm mã ngoài write set.

ĐÃ THỬ: `goi/draft_controls.py`: quet in `[]`, rc=0 trước fixture bad-type.yml/thiếu ID/non-mapping/pointer list; phép độc lập phân đúng từng lỗi. `goi/measure.py` vẫn xác nhận snapshot hiện tại 559/559 hợp lệ. Nên không khai hiện đã có lease xấu trong kho thật.

ĐỘ TIN: cao. Rủi ro bản vá: không gộp lease retired vào người giữ hoạt động; ghi nhãn lịch sử riêng và không sửa/xóa lease cũ để làm sạch phép đo.

### so-do-nen-khong-khop [P2] Con số rc và số ref không dùng được làm đối chiếu hiện tại
VỊ TRÍ: A6 dòng 154; §8 dòng 176–182; ghi chú cập nhật A8 dòng 161–163.

VẤN ĐỀ: A6 khai rc=0 sai với code nền: có người giữ ⇒ `RC_DANG_GIU=11`. Chỉ kiểm nonzero sẽ xanh ở cả trước lẫn sau Q3. Snapshot đã có 505 ref trong khi số đối chiếu còn là 503; quan hệ mọi ID là chuỗi và số blob 559 vẫn đúng, nên chỉ kiểm quan hệ không bắt được số hạng trôi. 185/187 được khai là lịch sử thiếu công cụ, không có log để bác; với công cụ đầy đủ, số tái đo phải ghi 187/187.

HINT: có — nhóm cùng slug; sửa A6 và ghi số hiện tại cùng lệnh/UTC, giữ lời khai cũ dưới nhãn lịch sử; L5 áp cả bước công bố băm, không chỉ cấp lease/land.

ĐÃ THỬ: `goi/probes.py`, `goi/measure.py`, lệnh suite và tool versions ở hướng 3/7. A6 rc=11; map snapshot 505=505 tên+OID; suite rc=0 187/187. Mạng live không đo và không dùng thất bại mạng làm finding.

ĐỘ TIN: cao cho hiện tại và A6; KHÔNG ĐO ĐƯỢC số máy chủ tại thời điểm lịch sử. Rủi ro bản vá: thay bằng một con số mới rồi lại đóng cứng; phải neo gate vào bất biến cùng phép đo lặp, không vào 505.

### hop-dong-dong-bang-thieu-neo [P2] Hợp đồng chưa cho executor tự kiểm đủ trường bắt buộc
VỊ TRÍ: bảng metadata đầu SPEC (3–13), không có đoạn công thức hash; protocol §3.2/§3.2.1/§4; bài học preflight trong CLAUDE.md.

VẤN ĐỀ: các mục theo skill soan-spec có đủ, nhưng minimum contract còn environment/risk/mission_issue/spec_hash. Spec không khai environment hoặc trỏ nguồn authoritative để đọc nó; không thể suy từ “claude”. Review class không thay risk. Không có công thức băm và nơi externalize hash nên dễ nhầm hash tệp lease với hash hợp đồng, hoặc tự tham chiếu. Snapshot cung cấp băm để reviewer xác minh PR này; đó không tự là hợp đồng cấp lease thi hành. ID `LEASE-ID-EP-KIEU-YAML` cũng chưa giải thích ánh xạ với quy ước `wp678` của protocol; cần đối chiếu, không đổi ID âm thầm.

HINT: có — nhóm cùng slug; ghi schema/risk, nêu rõ metadata chưa được cấp phải được điều phối neo nguồn trước freeze; công thức SHA-256 toàn bytes, hash công bố ngoài chính tệp. Hint không bịa mission/environment/receipt. Các ô cần authority phải điền lúc soạn r2; đây là giới hạn có chủ đích của hint, không phải yêu cầu executor đi quyết ngoài spec.

ĐÃ THỬ: grep tên trường rc=1; đọc schema tối thiểu và luật biến environment ⇒ revision mới. Issue #678 không có body/receipt trong gói, nên **không kết luận Issue thật thiếu trường**, chỉ kết luận tệp tự nhận hợp đồng đóng băng chưa tự đủ và không dẫn chỗ tự xác minh. Không đòi spec_hash nhúng giá trị tự băm trong cùng tệp.

ĐỘ TIN: cao về phần vắng mặt; vừa về cách authority của kho sẽ bổ sung. Rủi ro bản vá: băm prose mà bỏ closure; hint yêu cầu trường dispatcher dẫn xuất nằm trong hợp đồng trước khi băm.

### bang-duong-phan-loai-sai [P3] Bảng gán nhầm hàm và đồng nhất hai loại DU_BAO
VỊ TRÍ: D7/D8/D9 (62–64), làm rõ A7 (155–159).

VẤN ĐỀ: :2139/:2143 là báo cáo con-tro-treo; khóa người giữ nằm ở :2123. :1967 ép str rồi tra ID thu hồi, không phải so raw; :1946 cũng f-string. Bảng không thiếu hoàn toàn consumer đó, vì đã ghi đúng dòng, nên không thổi thành P1 bỏ sót đường sửa. A7 có thể làm đúng nếu executor phân cả hai entry point; cần ghi rõ để không lấy chốt D1 của check che kết luận về ai-dang-giu.

HINT: có — nhóm cùng slug; sửa bảng và ghi phạm vi ca A7.

ĐÃ THỬ: grep/đọc flow; `goi/probes.py` đưa int tới D8 từ ai-dang-giu với D1 strict. D9 vẫn chỉ hiển thị, không lập khóa/so đối tượng.

ĐỘ TIN: cao. Không tự mở mục sửa hành vi của con-tro-treo từ nhầm lẫn vị trí trong bảng.

### trang-thai-q3-chua-dong-bo [P3] Trạng thái quyết định đã có vẫn bị ghi thành câu hỏi mở
VỊ TRÍ: Q3 (77–78), §10 (204–205).

VẤN ĐỀ: authority giao review nói chủ kho đã xác nhận Q1–Q4, nhưng đặc tả đóng băng vẫn nói Q3 suy ra/chưa xác nhận. Lượt sau có thể dừng để hỏi lại việc đã được quyết, hoặc hiểu Q3 chưa có hiệu lực.

HINT: có — nhóm cùng slug; ghi đã xác nhận và yêu cầu điều phối neo nguồn bền khi soạn revision mới. Không sửa hành vi Q3.

ĐÃ THỬ: đọc toàn bộ `prompt.snapshot` và đối chiếu nguyên văn hai vị trí; không có receipt GitHub trong gói để xác minh object ID. Không hỏi người dùng lại.

ĐỘ TIN: cao trong phạm vi authority của lượt review; nguồn bền GitHub KHÔNG ĐO ĐƯỢC.

## DRY-RUN HINT.patch

HINT là gợi ý sửa đặc tả cho điều phối soạn revision mới, không sửa đè r1 đóng băng. Nhãn: **“chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit”**. Các thí nghiệm trên bản sao không trở thành patch sản phẩm; không thay write set.

Lệnh đã chạy từ `$R`:
```sh
hint_tmp=$(mktemp -d -p "$R")
cp -a "$R/cay-kho" "$hint_tmp/cay"
patch -d "$hint_tmp/cay" -p0 --fuzz=0 --dry-run --verbose < "$R/goi/HINT.patch"
```
Output cuối cùng (toàn bộ, `goi/hint-dry-run.log`):
```text
Hmm...  Looks like a unified diff to me...
The text leading up to this was:
--------------------------
|# lop: tieu-chi-dot-bien-khong-phan-biet-chot
|--- ops/specs/lease-id-ep-kieu-yaml-r1.md
|+++ ops/specs/lease-id-ep-kieu-yaml-r1.md
--------------------------
checking file ops/specs/lease-id-ep-kieu-yaml-r1.md
Using Plan A...
Hunk #1 succeeded at 131.
Hunk #2 succeeded at 157.
Hmm...  The next patch looks like a unified diff to me...
The text leading up to this was:
--------------------------
|# lop: bo-quet-nghiem-thu-thieu-mien
|--- ops/specs/lease-id-ep-kieu-yaml-r1.md
|+++ ops/specs/lease-id-ep-kieu-yaml-r1.md
--------------------------
checking file ops/specs/lease-id-ep-kieu-yaml-r1.md
Using Plan A...
Hunk #1 succeeded at 165.
Hmm...  The next patch looks like a unified diff to me...
The text leading up to this was:
--------------------------
|# lop: so-do-nen-khong-khop
|--- ops/specs/lease-id-ep-kieu-yaml-r1.md
|+++ ops/specs/lease-id-ep-kieu-yaml-r1.md
--------------------------
checking file ops/specs/lease-id-ep-kieu-yaml-r1.md
Using Plan A...
Hunk #1 succeeded at 153.
Hunk #2 succeeded at 163.
Hunk #3 succeeded at 180.
Hunk #4 succeeded at 199.
Hmm...  The next patch looks like a unified diff to me...
The text leading up to this was:
--------------------------
|# lop: hop-dong-dong-bang-thieu-neo
|--- ops/specs/lease-id-ep-kieu-yaml-r1.md
|+++ ops/specs/lease-id-ep-kieu-yaml-r1.md
--------------------------
checking file ops/specs/lease-id-ep-kieu-yaml-r1.md
Using Plan A...
Hunk #1 succeeded at 13.
Hmm...  The next patch looks like a unified diff to me...
The text leading up to this was:
--------------------------
|# lop: bang-duong-phan-loai-sai
|--- ops/specs/lease-id-ep-kieu-yaml-r1.md
|+++ ops/specs/lease-id-ep-kieu-yaml-r1.md
--------------------------
checking file ops/specs/lease-id-ep-kieu-yaml-r1.md
Using Plan A...
Hunk #1 succeeded at 62.
Hunk #2 succeeded at 155.
Hmm...  The next patch looks like a unified diff to me...
The text leading up to this was:
--------------------------
|# lop: trang-thai-q3-chua-dong-bo
|--- ops/specs/lease-id-ep-kieu-yaml-r1.md
|+++ ops/specs/lease-id-ep-kieu-yaml-r1.md
--------------------------
checking file ops/specs/lease-id-ep-kieu-yaml-r1.md
Using Plan A...
Hunk #1 succeeded at 76.
Hunk #2 succeeded at 203.
done
```

Đã áp thật tiếp trên **cùng bản sao tạm**, không phải `cay-kho` nguồn, rồi `cmp` với nội dung dự kiến do script sinh. Phép áp thật này bắt được tương tác context giữa nhóm hunk mà riêng dry-run nhiều nhóm cùng tệp không mô phỏng; bản hint cuối đã sửa và kiểm lại:
```text
dry_run_rc=0
apply_rc=0
expected_spec_cmp_rc=0
```

Tệp đích mọi nhóm là `ops/specs/lease-id-ep-kieu-yaml-r1.md`, không có tiền tố a/b. Mỗi nhóm mở bằng `# lop: <slug>` ngay trước header. `goi/build_hint.py` là lệnh tái sinh và kiểm các đoạn tìm/thay khớp duy nhất.

## TOÀN VẸN VÀ GIỚI HẠN CUỐI

Snapshot trước/sau băm toàn bộ tệp (tracked, untracked, ignored, Git metadata) trong `cay-kho` và `kho.git`. Lệnh `python goi/snapshot.py goi/snapshot-after.json`; so JSON với `goi/snapshot-before.json`: cùng tập 3003 tệp, delta 0. Bằng chứng này chỉ chứng minh không có delta quan sát được ở hai mốc, không phải audit mọi syscall trong cả phiên. Sandbox cho phép ghi workspace, còn kỷ luật đo và TMPDIR giới hạn mọi thao tác của review vào `goi` và các thư mục mktemp.

HEAD/tree và băm SPEC giữ nguyên. Suite chạy thật; Ruff không đo được; nền Windows, GitHub live, nội dung đầy đủ #677/#678 và identity runtime exact model/effort không đo được. Không có mã thi hành PR để phán delta candidate hoặc tuyên bố packet đã đóng. Verdict là yêu cầu sửa hợp đồng, không phải approval/land authorization.

Kiểm cấu trúc hiện vật bằng `PYTHONDONTWRITEBYTECODE=1 python goi/verify_artifacts.py`:
```text
verdict: verdict: changes_requested
class_count= 6 severities= {'P2': 4, 'P3': 2}
hunt_count= 9 hint_groups= 6 unique_target_paths= 1
SPEC sha256= 578916a9b04965b178e5dcaf949c725771129d0cb4d4e13f216adb5056d5fa7c
HEAD/tree= ['342e62c7a23fe03780539e2395c1e24832648c91', 'e6ab8444f000df78bd81bd81cefb564dd5d88456']
source_snapshot_delta= 0
dry_run_rc=0
apply_rc=0
expected_spec_cmp_rc=0
```
