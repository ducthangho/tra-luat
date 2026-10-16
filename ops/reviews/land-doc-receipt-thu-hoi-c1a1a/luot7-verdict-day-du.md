**0 P1 / 0 P2 / 1 P3**

verdict: changes_requested

```yaml
packet: LAND-DOC-RECEIPT-THU-HOI-C1a1a
issue: 650
review_round: 7
reviewed_sha: 55619d8e9ddc9dd4e7ad3ab9ba6c43d64679a45a
reviewed_tree: 0d1be2fe07962b1c2516bafeed73399261923b35
base: ceb1a3f36912dd4f03fe1741c443cd09e82a44ee
previous_reviewed_sha: a212059c5a2ea7379e08c3081f777583dcaa5f62
spec_revision: 5
spec_sha256: 978058983e8eddefebfba267dbff2ef5cee95daf9b2d4847121d43b8cff89d77
receipt_sha256: ca67dc6a817b7cf8643616e4762d5f3e95c0ec7a46cf9693f9436b47c00f5960
review_class: sensitive
assurance: advisory_review
provider: openai_codex
execution_surface: codex_cli
transport: machine
executor: Claude (assignment)
review_axes: [spec, standards_security]
```

**F38 và F39 đã vá thật trong miền được giao; F40 giết được phản chứng cũ nhưng chưa đóng lớp.** F41 dưới đây là biểu hiện còn hở của chính bộ lọc K4 vừa vá: thêm một dấu cách hoặc tab trước nhãn khiến thông báo ngược nghĩa biến mất khỏi oracle. Cả hai bản sao mutant vẫn xanh toàn suite. Đếm **một biểu hiện / một lớp mở**, không cộng F40 lần nữa. Theo yêu cầu hết P1/P2/P3, chưa đạt điều kiện approve. Không thấy lỗi runtime HEAD trong ba phép đo đã giao.

## Mỏ neo, authority và phạm vi

`git rev-parse HEAD 'HEAD^{tree}' origin/master` đo được đúng khối trên ở đầu và cuối. Parent duy nhất của HEAD là `a212059c5a2ea7379e08c3081f777583dcaa5f62`: đúng một commit vá. Spec blob tại `HEAD:ops/specs/LAND-DOC-RECEIPT-THU-HOI-C1a1a.md` và bản trên đĩa cùng băm đã giao; receipt thật cũng khớp. Xem [facts.json](facts.json), [patch.txt](patch.txt), [snapshot-before.json](snapshot-before.json), [snapshot-after.json](snapshot-after.json).

Authority lượt 7 nhận trực tiếp từ chủ kho trong assignment ngày 28-09-2026, dẫn [#650 comment 5862498825](https://github.com/ducthangho/tra-luat/issues/650#issuecomment-5862498825), lựa chọn “(a) lượt 7 hẹp xác nhận F38–F40”. Không gọi mạng để đọc lại comment/lease/generation. Không tự suy quyền thi công từ lease lịch sử. Trần sản phẩm **≤650** và phạm vi hiện vật review nhận theo assignment hiện hành; không dùng trần 400 lịch sử trong spec để bác chỉ thị này.

Chỉ kiểm F38–F40, cơ chế của diff `a212059..55619d8 -- .claude/dev`, ba driver runtime và các gate được yêu cầu. Diff sản phẩm chỉ đổi `.claude/dev/doc_receipt_thu_hoi_test.py`; module runtime và registry không đổi trong commit vá. Không audit lại toàn bảng A0 hoặc săn lớp khác.

Quy ước lệnh: `ROOT` là checkout được giao, `OUT=/tmp/review650-r7-output`; cwd là ROOT. [run_logged.py](run_logged.py) giữ nguyên từ lượt 6, ghi argv/rc/stdout/stderr/thời gian vào `*.json`, `*.stdout`, `*.stderr`. Driver này trả 0 sau khi ghi log; **rc con trong JSON và rc suite lồng bên trong output mới là kết quả cần đọc**. Mọi lệnh qua driver có `PYTHONDONTWRITEBYTECODE=1` và `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false`.

## Đối chiếu lượt 6

Nguồn: `luot6-VERDICT.md`, `luot6-verdict-day-du.md` trên `a212059`. Cả **15/15 tệp đầu vào** được chép nguyên byte ra OUT; cả **8/8 tệp có bản `luot6-*` tương ứng** khớp checkout. Không đổi neo các phép đo F38–F40. Bảng băm/đối chiếu tại [input-identity.json](input-identity.json). `executor_restore_chk.py` chép nguyên `luot6-executor-restore_chk.py` rồi chạy lại độc lập.

| Finding | Trạng thái | Bằng chứng tự chạy trên HEAD |
|---|---|---|
| **F38 — `phu-thuoc-cau-hinh-python`** | **da_va_that** | Nguyên `import_effect.py` dưới env 0: trước/sau import cùng `(limit=0, env="0", parse=parsed_4500, child_limit=0)`; dưới `-X 640`: cùng `(640, null, ValueError, child_limit=4300)`. Chưa gọi main. 17 child thực của `ca_cli`/`ca_tinh` mỗi cấu hình đều ghim 4300. Đối chứng executor giữ nguyên cấu hình sau ca xanh và ca ném; kiểm bổ sung cả lồng nhau/có-vắng env/đường gọi ở mục kế tiếp. Suite sáu cấu hình đều xanh, M2j vẫn chết đúng `ValueError@58#0`. |
| **F39 — `oracle-k4-ghim-cau-chu`** | **da_va_that** | Nguyên `k4_patch_check.py`: `K4: S: receipt stale, chạy lại` và bản H qua đủ 7 control, gồm ca hai trường, K3+K4, K2+K4. Ma trận thêm 16 cách phân cách/có-không `receipt`/có-không dấu đều qua. Đối chứng thiếu lý do, `fresh`, sai trường, lặp, phần đuôi ngược nghĩa vẫn bị bắt; đảo thứ tự S/H vẫn qua. |
| **F40 — `oracle-k4-bo-sot-ly-do`** | **va_ho** | Nguyên `k4_survives.py` nay suite mutant **rc 1**, `152/156 ca`, `162/171 mutant`, `unresolved 9`: dòng `K4:S fresh, khong can chay lai` bị bắt đúng ở oracle K4. Nhưng cùng dòng đó thêm một dấu cách/tab **trước** K4 lại lọt, mỗi suite mutant **rc 0, 156/156; 162/162; equivalent 9; unresolved 0**. Đây là F41, cùng lớp bộ lọc bỏ lý do. |

Log gốc: [import_effect-zero.stdout](import_effect-zero.stdout), [import_effect-x640.stdout](import_effect-x640.stdout), [executor_restore_chk-zero.stdout](executor_restore_chk-zero.stdout), [executor_restore_chk-x640.stdout](executor_restore_chk-x640.stdout), [k4_patch_check.stdout](k4_patch_check.stdout), [k4_survives.stdout](k4_survives.stdout), [limit-zero.stdout](limit-zero.stdout), [limit-x640.stdout](limit-x640.stdout).

**Giới hạn F39 được giữ rõ:** control lịch sử `r5_english` (`receipt stale, rerun`) vẫn bị bác, như output nguyên bản ghi. Lượt 6 dùng phản chứng tiếng Việt giữ nguyên cụm M5 và nêu không cần dựa vào tranh luận dịch nghĩa `rerun`; lượt này đóng miền dấu phân cách/cụm tiếng Việt ấy, không tuyên bố oracle hiểu mọi diễn đạt đồng nghĩa. Không tạo finding mới chỉ từ việc không nhận tiếng Anh. Khoảng trắng đầu nhãn được đo ở F41 theo nghĩa vụ thu nhận lý do của F40.

## Kiểm cơ chế bản vá

### `_ghim` và đường gọi

Đã chạy:

```text
python3.12 -B "$OUT/patch_mechanisms.py" "$ROOT" ghim
```

Rc **0**, [ghim.stdout](ghim.stdout), không sửa checkout. Năm cặp cấu hình `(parent limit, env)` là `(0, absent)`, `(0,"0")`, `(640, absent)`, `(640,"640")`, `(4300,"0")`. Mỗi cặp đo trực tiếp `ca`, `ca` ném `TinHieuChotCa`, `chay_ca`, `ca_thu_tu`, `ca_dang_ky`, `ca_cli`, `ca_tinh`, `chay_dot_bien` với M2j và M5g. Tất cả trở về đúng trạng thái đầu; các điểm gọi API được theo dõi đều đang ở `(4300,"4300")`. **85/85 lần sinh child** trong ma trận có parent/env 4300.

Kiểm lồng `_ghim` thêm `ValueError`, `KeyboardInterrupt`, `SystemExit`: wrapper trong hoàn nguyên về 4300 của wrapper ngoài; wrapper ngoài hoàn nguyên về cấu hình caller, gồm trạng thái env vắng. Không chỉ kiểm đường thành công.

Đọc đường gọi và kiểm danh tính function sau import:

- Gán lại tên tại dòng 278 hoàn tất trước driver nhận module. Không có global alias giữ bản chưa bọc của `ca`/`ca_cli`/`ca_tinh`; các bản gốc chỉ nằm trong closure của chính wrapper. Bảng CA giữ payload/lambda dựng fixture, không giữ ba helper ấy.
- `chay_ca` tra `ca`/`ca_cli` tại lúc chạy; tuple có `ca_tinh` được dựng trong thân hàm sau khi import xong. Bộ chạy mutant đi qua `chay_ca`. Driver cũ import module hoàn chỉnh rồi gọi các tên này.
- `ca_thu_tu` gọi global `ca` đã bọc; không sinh child. `ca_dang_ky` nạp registry và đo các cặp số nhỏ, không chạy registry main hay parse số dài. Không thấy đường bỏ ghim trong các entrypoint đã giao.
- `_cli` riêng là primitive dùng env caller; đường ca CLI gọi nó bên trong `ca_cli` đã bọc. Driver runtime gọi `_cli` trực tiếp để đo runtime thật với cấu hình môi trường; không coi đường ấy là một ca test đã ghim.

Harness này không tạo thread. Phép batch của reviewer chạy các **process độc lập**; không tuyên bố `_ghim` an toàn cho nhiều thread trong cùng process. Không mở finding giả định về một đường đa luồng không có trong phạm vi.

### K4 và M5g

Đã chạy `patch_mechanisms.py ROOT k4` rc **0**, [k4-mechanisms.stdout](k4-mechanisms.stdout), và nguyên `executor_va5_check.py` rc **0**, [executor_va5_check.stdout](executor_va5_check.stdout). 16 biến thể cùng nghĩa của F39 qua; `fresh`, hậu tố `..., fresh`, lý do trùng, sai trường và thiếu lý do bị bác ở ca liên quan. `K40:...` hoặc `K3: K4 ...` không bị nhận nhầm thành nhãn K4; ca K3+K4 và K2+K4 trên HEAD qua. Không thấy fullmatch nhận một lý do phủ định trong những đối chứng đã đo; lỗ còn lại nằm ở bộ lọc phía trước fullmatch (F41).

M5g có phân biệt thật, không chỉ có mặt trong DB:

```text
baseline k4_base: pass
M5g duong_fixture: pass
M5g k4_base: TinHieuChotCa: k4_base: ly do K4 sai nghia:
  ['K4:S fresh', 'K4: S stale, chay lai']
disposition: ['witness_killed', 'giet']
```

Trên **bản sao test ngoài checkout**, chỉ phục hồi bộ lọc `startswith("K4: ")` của lượt 6: M5g thành `['unresolved','song']`. Thay payload M5g bằng comment vô hại → `unresolved/song`; thêm lý do cả ở fixture dương → `unresolved/tin dung gia/qua tay`; gây `ValueError` vô can ở ca đích → `unresolved/nem sai dang: None`. Như vậy M5g hiện chết đúng assertion ngữ nghĩa của `k4_base`. Nó chưa khóa biến thể đầu nhãn của F41.

## F41 — P3 — `oracle-k4-bo-sot-ly-do`: khoảng trắng đầu nhãn làm lý do mâu thuẫn biến mất

**Tệp:dòng:** `.claude/dev/doc_receipt_thu_hoi_test.py:93` (`if re.match(r"K4\b", x)`). Liên hệ lịch sử: **F40** tại `a212059`; không đổi slug để coi đây là lớp mới.

`re.match` bắt đầu ở ký tự đầu chuỗi. Một dấu cách/tab trước `K4` làm dòng bị loại trước khi tới fullmatch/so đa tập. Khi đã có một lý do stale chuẩn cho S, oracle vẫn thấy đúng một S và cho qua, dù kết quả đồng thời nói S fresh/không cần chạy lại. Đây là chính trục “thu nhận mọi lý do nhãn K4” của bản vá; không mở một luật runtime hoặc nhóm finding khác.

**Lệnh đã chạy**, ghi argv/rc đầy đủ tại [k4-mechanisms.json](k4-mechanisms.json):

```text
python3.12 -B "$OUT/patch_mechanisms.py" "$ROOT" k4
```

Driver rc **0**. Hai suite lồng thực sự chạy bằng:

```text
/usr/bin/python3.12 -B /tmp/review650-r7-output/k4_space_prefix/.claude/dev/doc_receipt_thu_hoi_test.py
/usr/bin/python3.12 -B /tmp/review650-r7-output/k4_tab_prefix/.claude/dev/doc_receipt_thu_hoi_test.py
```

**Cả hai rc 0**, stdout mỗi bản:

```text
nghia vu: witness_killed 162 · equivalent_verified 9 · unresolved 0
doc_receipt_thu_hoi tests: 156/156 ca QUA · 162/162 dot bien GIET
```

Kết quả API của bản sao với dấu cách đầu dòng:

```json
{"ok":false,"luat":{"K1":"qua","K2":"qua","K3":"qua","K4":"do","K5":"qua"},"ly_do":["K4: S stale, chay lai"," K4:S fresh, khong can chay lai"]}
```

`duong_fixture`, `k4_base`, `k4_head`, `k4_ca_hai`, `a11_k3_k4`, `kieu_S`, `kieu_H` đều `pass`. Với tab, phần tử thứ hai là `"\tK4:S fresh, khong can chay lai"` và kết quả giống nhau. Bỏ đúng ký tự đầu ấy thì ca có S lệch ném `TinHieuChotCa` đúng oracle K4. Log suite: [k4_space_prefix.log](k4_space_prefix.log), [k4_tab_prefix.log](k4_tab_prefix.log); bản sao module và test giữ trong hai thư mục cùng tên, ngoài checkout.

**Mức P3:** lỗ oracle/test còn cho output mâu thuẫn qua và làm tuyên bố đóng F40 rộng hơn phép kiểm. Không có bằng chứng module runtime HEAD tự phát thông báo ấy; không nâng thành lỗi runtime P1/P2.

**Đề xuất đủ bốn phần:**

1. **Vá ở đâu:** khối thu nhận/parse lý do K4 trong `ca`, dòng 93–95, cùng ca/đột biến M5g. Sai nằm trước fullmatch; chỉ sửa biểu thức stale hoặc thêm mutant không đóng được bộ lọc.
2. **Vá thế nào:** dùng cùng một cách chuẩn hóa khoảng trắng đầu nhãn cho cả nhận diện nhãn và parse toàn lý do; mọi dòng đã được nhận là K4 mà không parse được phải làm ca đỏ. Giữ ranh giới tên luật và so đa tập trường. Đối với khoảng trắng đã đo, đây là thay đổi nhỏ; không cần oracle ngôn ngữ tự nhiên hoặc mở write set.
3. **Ca khóa:** cặp lời stale hợp lệ + lời fresh có tiền tố `""`, dấu cách, tab đều phải đỏ; lời stale hợp lệ đơn thuần với cùng tiền tố phải qua. Giữ ca hai trường, sai/thiếu/trùng trường, phần đuôi ngược nghĩa, K3+K4 và K2+K4. Đột biến thu hẹp nhận diện về ký tự đầu chưa chuẩn hóa phải sống trước và chết sau vá. [f41_controls.py](f41_controls.py) đã chạy rc **0**, [f41-controls.stdout](f41-controls.stdout): trên bản sao test, chuẩn hóa đồng nhất bằng `lstrip(" \t")` làm cả ba ca K4 mục tiêu chuyển sang **đỏ đúng** với lời fresh, và **xanh** với lời stale có cùng tiền tố. Đây là script đối chứng ngoài cây, không phải code đã sửa trên HEAD.
4. **Rủi ro vá:** đổi thành tìm substring ở bất kỳ đâu có thể vơ `K3: ... K4 ...`; chỉ nới bộ lọc mà không chuẩn hóa đầu vào fullmatch lại bác lời đúng có thụt đầu dòng. Không bỏ fullmatch hoặc đổi đa tập thành set vì sẽ mở lại phần đuôi ngược nghĩa/lý do trùng. Đối chứng nhãn K40 và lý do K3 nhắc K4 phải giữ nguyên kết quả.

## Runtime

Chỉ chạy lại ba driver được giao, giữ nguyên bytes, trên HEAD thật bằng Python **3.10.20 / 3.11.15 / 3.12.3 / 3.13.12**:

```text
python3.<v> -B "$OUT/runtime_isolated.py" "$ROOT"
python3.<v> -B "$OUT/runtime_depth.py" "$ROOT"
python3.<v> -B "$OUT/focused_controls.py" "$ROOT" receipt
```

**12/12 lệnh rc 0.** Mỗi Python: **592 ca API**, `errors=[]`; **16 mẫu API+CLI**; **6 độ sâu nhóm C: 900/990/1000/1200/2000/5000**. Không ngoại lệ API, không timeout/crash, mọi JSON CLI bằng API, rc trong `{0,12,2}`. Receipt thật bằng fixture, API `ok:true`, năm luật `qua`, CLI **rc 0** cả bốn Python. CLI lỗi tham số/tệp vắng được suite đo riêng với rc 2.

Khác lượt 6, import test nay giữ cấu hình caller. Bốn runtime này khởi động với giới hạn **4300**, đo trong [facts.json](facts.json); không suy kết quả runtime ở mọi giới hạn khác. Suite dưới env 0 và `-X 640` xanh là bằng chứng `_ghim` hoạt động trong test, không phải phép đo runtime production dưới 0/640.

[Runtime summary](runtime-summary.json) được tạo bằng [summarize.py](summarize.py), so trực tiếp JSON từng output API/CLI, không chỉ so rc. Logs mang tên `runtime_isolated-*.stdout`, `runtime_depth-*.stdout`, `focused_controls-*.stdout`. Mỗi phiên bản có thư mục fixture riêng. Không chạy thêm fuzz/runtime driver khác.

## Nợ ngoài phạm vi

**Không phát sinh nợ ngoài phạm vi mới (`no-ngoai-danh-muc`).** F41 thuộc chính bộ lọc K4 được giao, giữ P3 trong verdict, không đẩy ra ngoài danh mục. Các thiếu hụt môi trường/evidence dưới đây là giới hạn phép đo, không phải finding sản phẩm mới. Không soạn hoặc chạy nội dung dựng đường dẫn thoát cây.

## Đã chạy

Lệnh kiểm tra dưới đây chạy từ ROOT; các nhãn log có argv/rc con trong [commands.json](commands.json). `passed` của driver đối chứng nghĩa là phép đo hoàn tất, không biến kết quả mutant sống thành pass nghiệm thu.

| Lệnh/phạm vi | Rc thật, bằng chứng dương | Trạng thái |
|---|---|---|
| `git rev-parse HEAD 'HEAD^{tree}' origin/master`; `git show -s --format='%H %P %T' HEAD`; băm spec blob/bản đĩa/receipt | 0; khớp exact identity, parent duy nhất; [facts.json](facts.json) | passed |
| `git diff a212059..55619d8 -- .claude/dev`; `git diff --name-only a212059..55619d8` | 0; sản phẩm chỉ đổi test, còn lại hiện vật lượt 6 | measured |
| `python3.10 -B .claude/dev/doc_receipt_thu_hoi_test.py` | 0; **156/156 ca, 162/162 mutant, equivalent 9, unresolved 0** | passed |
| Cùng suite bằng `python3.11`, `python3.12`, `python3.13` | Mỗi lệnh 0; cùng bằng chứng trên | passed |
| `env PYTHONINTMAXSTRDIGITS=0 python3.12 -B .claude/dev/doc_receipt_thu_hoi_test.py` | 0; **156/156; 162/162; equivalent 9; unresolved 0** | passed |
| `python3.12 -X int_max_str_digits=640 -B .claude/dev/doc_receipt_thu_hoi_test.py` | 0; cùng bằng chứng | passed |
| Nguyên `import_effect.py ROOT`, dưới env 0 và `-X 640` | Mỗi lệnh 0; import giữ state/parse/child; 17 child trong helper mỗi lần đều 4300 | passed — F38 |
| Nguyên `executor_restore_chk.py ROOT`, dưới env 0 và `-X 640` | Mỗi lệnh 0; `khoi_phuc:true` sau ca xanh và ca ném | passed |
| Nguyên `focused_controls.py ROOT limit`, dưới env 0 và `-X 640` | Mỗi lệnh 0; baseline pass, M2j đúng `ValueError@58#0`, `witness_killed` | passed |
| `patch_mechanisms.py ROOT ghim` | 0; 5 cặp cấu hình hoàn nguyên, 85 child ghim, lồng/ngoại lệ đúng, không global alias chưa bọc | passed |
| Nguyên `k4_patch_check.py ROOT` | 0; câu tiếng Việt có `:` qua, phản chứng cũ F40 bị bắt; English vẫn bị bác như đã khai | measured; F39 đóng trong miền đã nêu |
| Nguyên `k4_survives.py ROOT` | Driver 0; suite mutant **1**, `152/156`, `unresolved 9` | passed đối chứng cũ F40 |
| Nguyên `executor_va5_check.py ROOT` | 0; thêm receipt/dấu/đảo thứ tự qua, fresh/sai trường/trùng/đuôi ngược nghĩa bị bắt | passed trong scope K4 của script |
| `patch_mechanisms.py ROOT k4` | Driver 0; 16 biến thể F39 qua; M5g giết đúng; **2 suite mutant đầu nhãn rc 0** | **failed nghiệm thu F40/F41** |
| `f41_controls.py ROOT` | 0; bản sao oracle chuẩn hóa đổi màu đúng cho cặp stale/fresh | passed đối chứng hướng vá, không phải HEAD đã vá |
| `python3 -B .claude/dev/ci_dang_ky_test.py` với signer tắt bằng env trên | 0; **22/22 đăng ký, 4/4 launcher contract, 3/3 Ruff contract, 938/938 phản chứng; TỔNG ĐẠT** | passed |
| `python3 -m ruff --version` | 0; **0.16.9** | measured |
| `python3 -m ruff check --no-cache --select F` ba tệp sản phẩm | 0; **All checks passed!** | bare lint passed |
| `python3 -B "$OUT/ruff_delta.py"` | Driver 0; registry base/HEAD đều 0 lỗi; hai tệp mới HEAD 0. `scripts/tl.py` base/HEAD cùng **rc 1, 12 F821**, diagnostics bằng nhau | bare lint tl.py failed sẵn; **delta F=0 passed** |
| `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` | 0; **10 tệp, 0 chỗ chép doctrine** | passed |
| `python3 -B .claude/dev/packet_loop.py adr-song --root .` | 0; **50 ADR/50 dòng**, ngoại lệ thiếu trạng thái 0016 có sẵn | passed |
| `git diff --numstat origin/master..HEAD` | 0; toàn diff **52 đường, +4836/−0**. Sản phẩm đúng 3 đường: **+1 +114 +535 = +650/−0**, đúng trần | measured/passed theo trần sản phẩm được giao; không phải finding |
| `git diff --check origin/master..HEAD` | 0; không diagnostic | passed |
| Ba driver runtime × bốn Python | Mỗi lệnh 0; số dương ở mục Runtime | passed trong tập thử |
| `python3 -B "$OUT/summarize.py"` | 0; kiểm 35 log lệnh/driver, 6 suite và parity runtime; rc suite mutant nằm trong output được giữ riêng | passed |
| `python3 -B "$OUT/snapshot.py" before`, `... after`, so snapshot | Mỗi lệnh 0; **2336/2336 tệp bằng size/hash**, HEAD/tree/diff/index/status không đổi | passed |

`ruff_delta.py` dùng `git show origin/master:<path>` và `ruff check --no-cache --select F --output-format json --stdin-filename <path> -`. Hai `git show` cho tệp sản phẩm mới trả **128 vì chưa tồn tại ở base**, ghi `absent_at_base`, không gọi là lint pass. Ruff pin/probe contract trong registry là phép riêng; không tuyên bố Ruff cài tại đây là đúng pin CI. Lệnh tìm tên tệp lease/handoff local bằng `rg --files ops | rg ...` trả **1** vì không có tên khớp; không dùng kết quả ấy làm bằng chứng lease hợp lệ.

**not_run:** mạng/GitHub, đọc lại live PR/comment/lease/generation, CI remote/full CI/Windows, đúng Python 3.12.14 của CI, toàn registry `--chay`, legacy full selftest/release gate, audit lại toàn bộ A0 hoặc các lớp trước F38–F40, các entrypoint `audit.py census/attacks/classifier`, `schema_head.py`, `artifact_check.py`, `mechanisms_scoped.py` trọn vẹn (có khối telemetry ngoài scope; các phép K4 tương ứng đã chạy qua script cũ và ma trận hẹp), runtime bổ sung khác ba driver được giao, thread-safety của `_ghim`, merge/land/deploy/LIVE. **skipped:** không dùng check skipped nào làm pass.

## Lịch sử lớp và giới hạn evidence

| Slug | Đối chiếu lượt 6 → 7 | Phép kiểm còn lại |
|---|---|---|
| `phu-thuoc-cau-hinh-python` | F38: **da_va_that** trong đường import/helper/mutant đơn luồng đã đo | Không còn biểu hiện mở trong scope |
| `oracle-k4-ghim-cau-chu` | F39: **da_va_that** cho dấu phân cách và cụm M5 tiếng Việt | Không tuyên bố hỗ trợ mọi diễn đạt tự do |
| `oracle-k4-bo-sot-ly-do` | F40: **va_ho**; F41: **P3 mở**, cùng cơ chế loại dòng trước oracle | Thu nhận nhãn nhất quán; cặp stale/fresh đầu dòng có/không khoảng trắng đổi màu đúng |

Checkout detached, `core.abbrev=7`, origin là mirror local `/home/user/tra-luat` được cấp. Snapshot phủ checkout này, không phủ repo nguồn Executor; `.codex/` ignored có sẵn, bytes không đổi. Sandbox thực tế `workspace-write`; checkout giữ read-only bằng thao tác, cache/output/mutant ngoài cây. Snapshot bằng nhau chỉ chứng minh hai mốc không có delta, không chứng minh cả lịch sử chưa từng ghi rồi hoàn nguyên. Registry test tự dựng lịch sử trong repo tạm là hành vi của lệnh test được giao; không commit/push checkout.

Provider/surface/transport theo assignment và skill [cross-review](/tmp/claude-0/-home-user-tra-luat/0682048d-075d-5414-b3ff-642b89411167/scratchpad/rv7/.agents/skills/cross-review/SKILL.md) trong checkout; không có header launcher của chính run để độc lập đo exact model/effort/session ID, không suy chúng từ model của lượt 6 hoặc actor GitHub. System nhận dạng họ GPT-6; giữ **advisory_review**, không tự tạo `cross_approved`. Không dùng reviewer Claude hoặc subagent. Báo cáo này không tự cấp lượt review tiếp theo hay quyền thi công/land.

Manifest SHA-256 của báo cáo, script, log và bản sao mutant: [ARTIFACTS.sha256](ARTIFACTS.sha256).
