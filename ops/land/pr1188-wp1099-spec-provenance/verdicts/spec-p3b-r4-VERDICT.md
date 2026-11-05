verdict: request_changes
reviewed_sha: bbb0ec8306caf6d4a6d0e42477736ee6baa5f5b9
reviewed_tree: f16c7c75dd1b467676069cad0073995ce11be299

## DANH TÍNH

Đã đo danh tính theo PROMPT.md; kết quả đầu và cuối lượt dưới đây.

Phép đo đầu lượt (2026-11-04 UTC):

```text
$ git -C cay-kho rev-parse HEAD 'HEAD^{tree}'
bbb0ec8306caf6d4a6d0e42477736ee6baa5f5b9
f16c7c75dd1b467676069cad0073995ce11be299
$ git -C cay-kho status --porcelain=v1 --ignored
[output rỗng; rc=0]
$ sha256sum cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r{1,2,3,4}.md
15fe242a65c8df1ff393cdc15784642013e904bacb9b754b0d72a64237dac11e  r1
c6e53a00c7370ce0d75d9bcd954f8b7e69aa7383a0f5e6427a29e5e0d0e3ed8d  r2
e2246e90aaf35b6b006b40a258e694a99c796a1ff1a8ac21aebb408121efa121  r3
d28d00b5dbf6aac631f2aaac4282eb50ad1e59490d03acff095a64e45535430f  r4
```

HEAD/tree khớp PROMPT; cây sạch. PROMPT không cung cấp checksum kỳ vọng cho bốn đặc tả; các checksum trên là số đo, không phải đối chiếu với giá trị được cung cấp.

Provider: OpenAI; model: GPT-6/Codex (không suy phiên bản cụ thể từ GitHub submitter); execution_surface: Codex qua API, shell cục bộ; transport: công cụ cục bộ. Executor theo PROMPT: Claude; review session độc lập. Không gọi mạng/dịch vụ hay đọc credential thật; clone được giữ chỉ đọc.

### Đo cuối lượt

```text
2026-11-04T15:59:13.347008+00:00
$ git -C cay-kho rev-parse HEAD HEAD^{tree}
rc=0
bbb0ec8306caf6d4a6d0e42477736ee6baa5f5b9
f16c7c75dd1b467676069cad0073995ce11be299

$ git -C cay-kho status --porcelain=v1 --ignored
rc=0
[stdout rỗng]
$ git -C cay-kho diff --exit-code
rc=0
[stdout rỗng]
$ git -C cay-kho diff --cached --exit-code
rc=0
[stdout rỗng]
$ sha256sum cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r1.md cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r2.md cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r3.md cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r4.md
rc=0
15fe242a65c8df1ff393cdc15784642013e904bacb9b754b0d72a64237dac11e  cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r1.md
c6e53a00c7370ce0d75d9bcd954f8b7e69aa7383a0f5e6427a29e5e0d0e3ed8d  cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r2.md
e2246e90aaf35b6b006b40a258e694a99c796a1ff1a8ac21aebb408121efa121  cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r3.md
d28d00b5dbf6aac631f2aaac4282eb50ad1e59490d03acff095a64e45535430f  cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r4.md

```

HEAD/tree/status, diff/index và bốn băm đặc tả không đổi. Snapshot sạch chứng minh không có delta quan sát được ở hai mốc; không tự chứng minh lịch sử chưa từng ghi rồi hoàn nguyên. Sandbox thực tế cho phép ghi workspace, còn clone đã được xử lý chỉ đọc trong lượt này.

## ĐO LẠI KHẲNG ĐỊNH

Mốc đo: **2026-11-04, khoảng 15:30–16:00 UTC**, trên exact HEAD/tree nêu trên; nguồn giờ cuối lượt được ghi ở phần danh tính. Các lệnh đọc mã chạy từ SANDBOX, thêm tiền tố `cay-kho/` cho đường dẫn. `review_probe.py` và `review_additional.py` nằm ngoài clone; chạy bằng `python -B` để không tạo bytecode trong checkout. Bảng này gồm cả khẳng định ngoài E7–E10, không coi danh sách errata là trần review.

| Khẳng định | Lệnh đo | Kết quả | Khớp/lệch |
|---|---|---|---|
| Diff PR chỉ thêm r4; base được giao là `1f0941e9` | `git -C cay-kho diff --stat 1f0941e9 HEAD`; sinh lại diff vào `measured-diff.patch`, `cmp diff.patch measured-diff.patch` | 1 tệp, 259 dòng thêm; `cmp` rc=0 | KHỚP |
| R1–R3 là các blob lịch sử đã land ở `47ee1b20` | `git -C cay-kho show 47ee1b20:ops/specs/cloud-setup-p3b-nlm-401-rN.md`, so byte với tệp hiện tại, N=1,2,3 | Cả ba rc=0, byte-identical; sha256 đầy đủ ở DANH TÍNH | KHỚP nội dung Git; không xác minh GitHub/lease |
| Giữ nguyên errata r2/r3 | `python -B review_additional.py` (`docs_checks`) và `git diff --no-index` từng cặp revision | Errata r2 trong r2/r3/r4 trùng nhau; errata r3 trong r3/r4 trùng nhau; r4 supersede rõ lời khai “bền qua 3 lần” của E6 | KHỚP chuỗi errata |
| Mỗi mục tiêu chiếu đúng 1 path của write set; 9 path | `python -B review_additional.py` | `write_set_vs_goals: 9 9 True` | KHỚP L2 |
| Mỗi mục tiêu có nghiệm thu | Tách cột mục tiêu của các hàng A/D/F/J/G/K/L/M trong r4 bằng Python | Các mục được trỏ: `[1,2,3,4,5,6,7,9]`; thiếu `[8]` | LỆCH — F04 |
| Base cố định `1f0941e9` là merge PR #1186 | `git -C cay-kho log -1 --format='%H %s' 1f0941e9` | `1f0941e9bba1d1d517eda4174167b81963c06bd5 Merge pull request #1186 ...` | KHỚP; không thay bằng ref cục bộ khác |
| Không drift 5 tệp mã/doctrine ở E3/E10 | `git -C cay-kho diff --stat 90c101b8 c7174bfe -- scripts/nlm_cli.py references/RASOAT_HOSO_LOOP.md references/QUY_TRINH_RA_SOAT_3_TANG.md scripts/tl_gws.py scripts/tl_core/nlm_ops.py`; lặp cặp `90c101b8 1f0941e9` và `1f0941e9 HEAD` | Cả ba rc=0, output rỗng | KHỚP về blob; không chứng minh neo dòng gốc đúng |
| Neo `_c213_auth_carve_out_khong_pha_thu_tu` tại 24827 → 24829 | `git -C cay-kho show <OID>:scripts/tl_selftest.py`, đếm dòng chứa tên; AST ở `review_probe.py` | `c7174bfe`: def=24827, đăng ký=24850; `1f0941e9` và HEAD: def=24829, đăng ký=24852. `90c101b8`: def=24825 (mốc 24836 của r1 cũ đã bị r2 thay) | KHỚP neo r4/E10; không dùng lại neo r1 |
| `_AUTH_FIX_FALLBACK` ở `nlm_ops.py:296` | `python -B review_probe.py` (AST); `nl -ba cay-kho/scripts/tl_core/nlm_ops.py` | Gán hằng ở **297**; 296 là comment | LỆCH — F02 |
| Manifest r1/r2/r4 = 197/198/184 tệp | `git -C cay-kho show <OID>:RELEASE_MANIFEST.json`, `json.loads`, đọc `file_count` và `len(files)` | `90c101b8`: 197/197; `c7174bfe`: 198/198; `1f0941e9` và HEAD: 184/184 | KHỚP E5/E10 |
| Cả 4 tệp bị sửa thuộc gói | `python -B review_probe.py` (`manifest_contains`) | `nlm_cli.py`, `tl_test_fragments_bundled.py`, cả 2 tài liệu doctrine đều `True` | KHỚP write_set mục 9 |
| Auth detector tại `nlm_cli.py:143,162,229` | `nl -ba cay-kho/scripts/nlm_cli.py`, đọc 3 nhánh | Cả ba dùng `(err + out).lower()` và `auth, 401, login, unauthor, credential` | KHỚP |
| `_run` là seam mọi lời gọi trong adapter, tuple; timeout=124, thiếu binary=127 | AST và `rg -n 'subprocess\.' cay-kho/scripts/nlm_cli.py`; đọc dòng 110–124, các wrapper | Một `subprocess.run` ở 117; wrapper đều gọi `_run` trực tiếp/qua `_run_json`; 120 trả tuple, 122/124 trả 127/124 | KHỚP trong `nlm_cli.py`; không suy mọi lời gọi NLM của toàn kho |
| Các hằng auth không cần sửa để thêm ngoại lệ | `python -B review_probe.py`; đọc khai báo `nlm_cli.py:36,46,48,54` | `_AUTH_FIX_ORDER`, `_AUTH_FIX_RASOAT_CARVE`, `AUTH_FIX_HINT`, `AUTH_FIX_HINT_SHORT` hiện hữu; detector giữ nguyên; file không đổi so base | KHỚP hiện trạng; nghiệm thu head thi công chưa có |
| Hai điều cấm ở RASOAT:119 và QUY_TRINH:49; mẫu D1 riêng từng tệp | `python -B review_probe.py`; `nl -ba` hai tài liệu | RASOAT ngắt sau `CẤM tự` (118), command ở119; QUY_TRINH `**CẤM** tự` ở49. Sau gộp khoảng trắng: RASOAT mẫu=1, command=3 trong §4b; QUY_TRINH mẫu=1, command=1 trong gạch chỉ định | KHỚP sửa mẫu E8; lỗ hổng nghĩa ở F01 |
| `_nlm_auth_alive` ở 308–363; retry tối đa3, timeout30s, backoff4.5s | AST/source `tl_gws.py:308–363`; `python -B review_probe.py` | `range(3)`; mặc định30; sleep=1.5 rồi3; quyền 403 dừng sau1 lần, auth/mạng có thể3 | KHỚP; 120s là ngân sách canary **tương lai**, chưa đo LIVE |
| E7: phân loại dựa vào lần thử cuối | `python -B review_probe.py` với 6 đồ giả, chạy thân hàm nguồn trong RAM | refused→None; permission→None; auth→False; refused/refused/auth→False; auth/refused/auth→False; auth/auth/refused→None | KHỚP; giữ nguyên quyết định chủ kho |
| A13: cùng 6 ca qua thân canary, rc=2,2,3,3,3,2 | `python -B review_probe.py`; mỗi child `python -B review_probe.py --child <ca>` | Đúng `[2,2,3,3,3,2]`; stdout/stderr child rỗng. Thân canary lấy từ shell thật dòng95–104; `tl`, NLM đều giả | KHỚP phép phân loại; `<CANARY>` mới trong `nlm_cli` chưa tồn tại nên chưa chạy tích hợp đó |
| A13 có đột biến làm ĐỎ | AST bản sao trong RAM: giảm vòng probe thành chỉ lần đầu, chạy chuỗi auth/auth/refused | Đột biến trả False thay None; ca bị giết đúng khác biệt phân loại | KHỚP răng của ba ca trộn |
| E6: `nlm-auth-status` gộp lỗi mạng/quyền/auth thành False | `python -B review_additional.py` (`old_preflight`), hàm nguồn `_nlm_preflight_report` với NLM giả | Cả refused, 403 permission, auth expired đều `alive=False`; mã tại1424–1429 | KHỚP lý do bỏ canary cũ |
| Chốt chống hạ cấp của `nlm-auth-load` còn | Đọc `tl_gws.py:1894–1967,2024–2035`; chạy hàm nguồn `_nlm_auth_load_downgrade` với tuổi giả trong RAM | Bundle10 ngày/local5 ngày→chặn; bundle5/local10→không; thiếu mốc→không (hành vi cũ). `cmd_nlm_auth_load` truyền `force=False` khi không có cờ | KHỚP tái dùng đường có sẵn; không tuyên bố chốt chứng minh freshness khi thiếu mốc |
| Không thêm đường ghi registry/credential lên dịch vụ | Đọc CLAUDE.md:12–13, mục tiêu1 r4, `tl_gws.py:1919–1949`; `rg -n LockService cay-kho/references/Code.2.21.2q.gs` | Đường mới chỉ gọi `nlm-auth-load` sẵn có: download + ghi jar local; không đề xuất upload/registry write mới. GAS có `getScriptLock`/`tryLock` (vd2400–2401) | KHỚP kiến trúc đề xuất; không gọi endpoint LIVE |
| Không chuyển tiếp secret trong báo cáo mới | Đọc r4:97–119, A11; canary child đồ giả ở `review_probe.py` | Spec cấm forward đầu ra con, cookie/path trong chi tiết; canary chỉ dùng boolean và exit code. Runtime mới chưa có | KHỚP ràng buộc; chưa tuyên bố test sentinel tích hợp đạt |
| R4 khai trần thiệt hại 1 lần/10 phút | `python -B review_additional.py` (`race_model`) + đối chiếu r4:211–212 | Lịch xen kẽ được cho phép cho **2** lần nạp/1 cửa sổ; mỗi tiến trình đúng1 | LỆCH — F03; ngoại lệ race đã được chấp nhận vẫn giữ |
| D1 giữ “NGUYÊN chữ” và D3 đo đủ điều kiện | `python -B review_probe.py`; `python -B review_additional.py` | Xóa chữ cũ vẫn qua D1; `600`→`1600` vẫn qua phép khớp D3 | LỆCH — F01 (2 biểu hiện) |
| F2/r213 không cần sửa selftest để thêm câu ngoại lệ | `python -B review_additional.py` (`f2`) | Thân ca thật với import/hằng và tài liệu giả: base=True, thêm ngoại lệ=True; cũng True khi mất một mệnh đề cũ | KHỚP E8 về khả năng giữ nguyên selftest; không bù lỗ D1 |
| ADR-0062 đã bị chiếm; 0063 chưa có ở checkout | `git -C cay-kho ls-tree -r --name-only HEAD docs/adr/`; `python -B cay-kho/.claude/dev/packet_loop.py adr-song --root cay-kho` | Có `0062-adr-0060-mac-dinh-va-dong-bang-adr-0054.md`; không `0063-*`; 61 ADR/61 dòng §20, rc=0 (ngoại lệ0016 như mã nền) | KHỚP E9 trong checkout |
| E9: không 0063–0069/007* trên mọi remote ref hiện có | `git -C cay-kho for-each-ref --format='%(refname)' refs/remotes/origin/`, `ls-tree -r --name-only <ref> docs/adr/` cho từng ref | 6 ref cục bộ, mỗi ref0 path thuộc mẫu; không được gọi `ls-remote` nên không chứng minh đã đủ ref trên server | KHÔNG ĐO ĐƯỢC phần “đủ ref”/remote; không coi 0 cục bộ là chứng nhận toàn server |
| ADR-0052/0053 neo OID land `8ab10079…`; trần8 và nâng riêng9/550 | `git cat-file -e <L>:docs/adr/<0052,0053>` và `<L>^1:...`; đọc hai ADR và dòng khai r4 | L chứa cả2 (rc0), parent chưa có (rc128). Dòng khai0052 đúng regex, OID40 ký tự; trần8 trong0052. Nâng9 tệp/550 dòng là quyết định được tóm tắt, không phải số đo runtime | KHỚP 2 phép object; phép first-parent/ref tươi KHÔNG ĐO ĐƯỢC (clone shallow) |
| Số dòng hai fragment mẫu | `wc -l cay-kho/scripts/test_fragments/wp726_script_nlm_canary.py cay-kho/scripts/test_fragments/wp727_tl_gws_refresh.py` | 260 và259 dòng | KHỚP |
| Fragment có `TEST_ID`, `run(tl_module)`; bundle có generator; CI có check | Đọc `scripts/tl_core/test_fragments.py:287–324,464`, `tl_selftest.py:31677–31678`; `ci.yml:293–295` | Contract hiện hữu; generator đúng tên; CI chạy đúng lệnh. Harness đăng ký **1 ca outer / fragment**; ca con A/D phải báo riêng, không nhầm vào N tổng | KHỚP cơ chế; F1/F3 cho tính năng mới chưa chạy |
| G2 xanh sẵn | `python -B cay-kho/.claude/dev/packet_loop.py doctrine-scan --root cay-kho` | rc=0; `sạch — đã quét 10 tệp, 0 chỗ chép doctrine` | KHỚP |
| Ước tính kích thước ~495 dòng/9 tệp, LIVE fresh hơn, lịch laptop30 phút, log bootstrap, lease/call counts | Đối chiếu nguồn cục bộ và nhãn “ước tính/chưa đo”; không gọi dịch vụ | Tổng các hạng ước tính=495; chưa có diff thi công. Không có bằng chứng độc lập đầy đủ về vận hành laptop/log/lease hay số lời gọi1/8 trong sandbox | KHÔNG ĐO ĐƯỢC các sự kiện bên ngoài; không coi là pass |

### ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn duy nhất được cấp là tóm tắt `errata_r4` E7/E8. VERDICT dở của r3 không có trong cây như PROMPT đã thông báo; không suy ra slug/lịch sử finding ngoài tóm tắt. Các ID F01–F04 bên dưới thuộc **lượt này**.

| Finding r3 theo errata | Phân loại trên r4 | Bằng chứng tự đo và giới hạn |
|---|---|---|
| E7 / r3-F01: lời khai “auth_hint bền qua3 lần” | **ĐÃ VÁ THẬT** đối với lời khai và ba ca trộn | Sáu ca nguồn thật và exit-code canary đều khớp; đột biến chỉ xét lần đầu làm ca thứ6 đỏ. Chủ kho chấp nhận trộn kết thúc auth: giữ quyết định ấy. Lời khai mới về **trần toàn cục** là biểu hiện riêng F03, không phải bác quyết định canary. |
| E8 / r3-F02: một mẫu `CẤM tự` không khớp QUY_TRINH | **ĐÃ VÁ THẬT** đối với biểu hiện mẫu chung | Hai mẫu riêng đều có1 lần trong vùng tương ứng; F2 chạy thân ca với đồ giả xanh trước/sau thêm câu. **Chưa đóng lớp thước đo doctrine:** F01 chỉ ra bộ đếm hiện tại không chứng minh chữ cũ giữ nguyên và D3 cũng chỉ đo token. |

### Phạm vi chưa đo và trạng thái gate

- `passed`: 6 ca canary nguồn + 6 child rc; đối chứng F2 dùng thân ca/đồ giả; probe marker RAM; kiểm manifest/neo dòng/errata; `adr-song`; `doctrine-scan`.
- `failed` ở thước đo yêu cầu: D1/D3 không bắt các thay đổi đã mô tả (F01), neo dòng sai (F02), lời khai trần sai (F03), thiếu nghiệm thu mục8 (F04).
- `not_run`: full `tl.py --selftest`, bundle runtime gate, Ruff bare lint, release-verify, CI và M1. Đây là review đặc tả chưa thi hành; không chạy `tl` thật hay các suite có thể kéo dịch vụ. Không lấy hai cổng tài liệu xanh làm bằng chứng các gate thi công đạt.
- `not_measured`: quyền/lease đang hiệu lực, tập refs server, model/effort runtime của executor hay launcher r3, lịch/cookie LIVE và canary cloud. `origin/master` trong clone là **`8983e1bbf00c91d8def101a97a4d32509ae630cc`**, không phải snapshot ref tươi `1f0941e9`; clone `--is-shallow-repository=true`. Không fetch/unshallow/ls-remote theo lệnh cấm mạng. Dùng object cố định `1f0941e9` để đối chiếu E10; không dùng ref cục bộ cũ chứng minh authority/lease hiện hành.
- Không tạo payload tấn công; các phản chứng đã chạy chỉ dùng chuỗi tài liệu vô hại bị xóa chữ trong RAM, hàm nguồn với đồ giả, tiến trình Python vô hại hoặc mô hình marker trong RAM. Không đọc/ghi credential thật, không gọi Drive/NLM/GAS/GitHub, không viết trong `cay-kho/`.


## FINDINGS

### F01 — P2 — `doctrine-do-bang-tu-khoa-thay-vi-toan-bo-loi-khang-dinh`

- **Tệp:dòng:** `ops/specs/cloud-setup-p3b-nlm-401-r4.md:161` (D1; liên quan mục tiêu 4–5 tại dòng 129–131).
- **Mô tả:** D1 khẳng định chứng minh điều cấm cũ còn “NGUYÊN chữ”, nhưng chỉ so hai bộ đếm từ khóa riêng rẽ. Bộ đếm không chứng minh toàn bộ câu cũ được giữ; ngắt dòng đúng cũng không giải quyết được việc chỉ đo một phần lời khẳng định. Đây là lỗ hổng thước đo L3/L6b, khác lỗi mẫu Markdown chung của r3 đã được sửa. Một executor có thể thay/xóa phần còn lại của quy tắc mà D1 vẫn xanh, trái mục tiêu “Mọi chữ cũ giữ”.
- **Phép đo tái hiện đã chạy:** `python -B review_probe.py` (rc=0), phần `D1`: trên §4b và gạch “Sửa xác thực” thật, nối khoảng trắng, thêm đúng câu ngoại lệ; rồi chỉ xóa ngoặc giải thích cũ trong RAM. Cả hai bản bị mất chữ cũ vẫn qua mọi phép đếm D1. RASOAT: `CẤM tự=1`, `nlm-auth-load=3` trước/sau; QUY_TRINH: `**CẤM** tự=1`, `nlm-auth-load=1` trước/sau; `old_text_preserved=false` nhưng `deleted_old_text_pass=true` ở cả hai tệp. Không ghi bản đột biến vào clone.
- **Đề xuất sửa:** sau khi bỏ đúng một câu ngoại lệ mới, so toàn bộ vùng cũ đã chuẩn hóa với vùng base tương ứng (hoặc khớp toàn bộ từng câu cũ, không chỉ tiền tố/từ khóa). Bổ sung đột biến xóa/sửa hậu tố của điều cấm và đột biến ngắt dòng không đổi nghĩa. Giữ mẫu riêng từng tệp của E8.

Bổ sung ngay cho **F01**, sau quét cùng lớp bằng `python -B review_additional.py` (rc=0):

- **Biểu hiện D3, đặc tả dòng 163:** chỉ đòi các token, không đo đủ năm điều kiện của mục tiêu 6 (dòng 132–135). Fixture RAM chứa đủ bảy cụm vẫn ĐẠT sau khi đổi `600` thành `1600` vì khớp chuỗi con. Do đó thước đo không khóa được con số và toàn bộ mệnh đề; việc token `--force` có mặt cũng không chứng minh quan hệ cấm dùng nó. Cần đo từng mệnh đề đầy đủ, số nguyên có biên và đơn vị, kiểm sửa hậu tố/số/ngắt dòng; ghi rõ vế âm trên base cho ADR mới vắng mặt. Đây là biểu hiện thứ hai của cùng lớp F01, không đếm thành finding riêng.
- **Đối chứng F2:** thân ca r213 thật (chỉ thay import bằng các hằng nguồn trong RAM và đặt `_ROOT209` vào bản sao tài liệu ngoài clone) trả `True` trên base, trên bản thêm ngoại lệ đúng và cả bản xóa câu “không tin ... --check ... probe LIVE”. F2 không bù được lỗ hổng so chữ cũ của D1. Đây là phép chạy thân ca có đồ giả, không khai đã chạy toàn bộ selftest.

### F02 — P3 — `neo-dong-khong-tro-khai-bao`

- **Tệp:dòng:** `ops/specs/cloud-setup-p3b-nlm-401-r4.md:60`; lời xác nhận bao quát ở E10 dòng 256.
- **Mô tả:** neo `_AUTH_FIX_FALLBACK` ở `nlm_ops.py:296` không trỏ khai báo hằng. Dòng 296 là chú thích; khai báo bắt đầu ở dòng **297**. E10 suy “các neo dòng … còn đúng” từ diff rỗng chỉ chứng minh tệp không đổi, không chứng minh mốc gốc đúng.
- **Phép đo tái hiện đã chạy:** `python -B review_probe.py` (AST `Assign.lineno` ⇒ 297); `nl -ba cay-kho/scripts/tl_core/nlm_ops.py | sed -n '294,299p'` cho dòng 296 là comment, 297 là `_AUTH_FIX_FALLBACK = ...`. Cùng số dòng trên cây được review và base `1f0941e9` vì blob không đổi.
- **Đề xuất sửa:** ở revision tiếp theo, đổi neo hiện hành thành `nlm_ops.py:297` (hoặc ghi rõ khoảng 294–299 là khối hằng kèm chú thích). Không sửa errata lịch sử của r2; E10 phải xác minh từng neo thay vì chỉ dựa vào diff rỗng.

### F03 — P2 — `tran-thiet-hai-khai-tuyet-doi-trong-khi-da-chap-nhan-race`

- **Tệp:dòng:** `ops/specs/cloud-setup-p3b-nlm-401-r4.md:103` (đối chiếu dòng 88–105 và 211–212).
- **Mô tả:** lời khai mới của r4 “trần thiệt hại là một lần nạp ... trong cửa sổ 10 phút” là một giới hạn tuyệt đối không được đặc tả bảo đảm. Chính r4 giữ ngoại lệ đã chấp nhận từ r1: dấu không có khóa, hai tiến trình có thể cùng qua bước Giới hạn rồi nạp hai lần. Mỗi tiến trình vẫn tuân thủ giới hạn riêng và vẫn ghi dấu trước nạp. Đây là mâu thuẫn trong lời khai về trần, không phải finding chống quyết định giữ canary hay chống ngoại lệ race đã được duyệt.
- **Phép đo tái hiện đã chạy:** `python -B review_additional.py` (rc=0), mục `specified_steps_RAM_model`: lịch xen kẽ hợp lệ của các bước được đặc tả, hai tiến trình đều đọc dấu vắng trước khi tiến trình nào ghi; mỗi tiến trình canary chết rồi ghi dấu và nạp một lần. Kết quả `eligible=[true,true]`, `loads_same_window=2`, `per_process_loads=[1,1]`. Đây là mô hình các bước của đặc tả trong RAM, không phải phép chạy tính năng mới (chưa tồn tại) hay gọi dịch vụ.
- **Đề xuất sửa:** giữ quyết định chủ kho và ngoại lệ r1; sửa lời khai dòng 103 để giới hạn “một lần” theo từng tiến trình, và nói rõ cửa sổ 600 s giữa các tiến trình chỉ là best effort, không bảo đảm khi cạnh tranh. Đồng bộ phần Vấn đề/ADR tương lai để không đọc thành trần toàn cục. Nếu muốn bảo đảm trần toàn cục thì cần quyết định phạm vi mới; review này không yêu cầu đổi thiết kế đã duyệt.

### F04 — P3 — `muc-tieu-changelog-thieu-nghiem-thu`

- **Tệp:dòng:** `ops/specs/cloud-setup-p3b-nlm-401-r4.md:138` (mục tiêu 8; bảng nghiệm thu dòng 146–173).
- **Mô tả:** mục tiêu 8 đòi `changelog.d/wp-1099.md` có nội dung tóm tắt theo khuôn, nhưng không tiêu chí nghiệm thu nào chiếu vào mục tiêu 8 hay kiểm nội dung tệp. K2 chỉ canh tập đường dẫn và kích thước; một tệp rỗng cũng không bị phép đo nội dung nào làm ĐỎ. Thiếu điều kiện “mỗi mục tiêu ≥1 tiêu chí” của `soan-spec` §4 và L3.
- **Phép đo tái hiện đã chạy:** tách cột mục tiêu trong bảng nghiệm thu bằng Python chỉ đọc đặc tả: `acceptance_targets=[1,2,3,4,5,6,7,9]`, `unmapped_goals=[8]`. Đọc K2 dòng 171 xác nhận chỉ đo `git diff --numstat`, write set và trần.
- **Đề xuất sửa:** thêm tiêu chí cho mục tiêu 8: tệp changelog tồn tại, có mục tóm tắt đúng khuôn và nêu hành vi của packet; đột biến xóa/rỗng nội dung hoặc bỏ mục bắt buộc phải làm ĐỎ. Có thể dùng thước kiểm changelog sẵn có nếu đủ nghĩa; khai rõ lệnh và kết quả mong đợi.


## BẢNG LỚP FINDING

| Slug lớp | Finding / biểu hiện | Mức cao nhất | Nguồn và cách đóng lớp |
|---|---|---|---|
| `doctrine-do-bang-tu-khoa-thay-vi-toan-bo-loi-khang-dinh` | F01: D1, D3 (2 biểu hiện) | P2 | R4 ở SHA được review; có liên hệ lớp thước đo của E8, nhưng không biết slug r3. Sửa chung thước đo toàn mệnh đề/vùng cũ; cả đột biến mất chữ cũ, đổi hậu tố/số phải đỏ, ngắt dòng giữ nghĩa phải xanh. |
| `neo-dong-khong-tro-khai-bao` | F02 (1 biểu hiện) | P3 | Neo hiện hành dòng60 + xác nhận bao quát E10. Đo AST/từng neo, sửa neo hiện hành; không viết lại errata lịch sử. |
| `tran-thiet-hai-khai-tuyet-doi-trong-khi-da-chap-nhan-race` | F03 (1 biểu hiện) | P2 | Lời khai mới r4 dòng103. Phân biệt giới hạn từng tiến trình với best effort giữa tiến trình; đối chiếu lại ngoại lệ r1 và ADR dự kiến. |
| `muc-tieu-changelog-thieu-nghiem-thu` | F04 (1 biểu hiện) | P3 | Mục tiêu8 r4. Thêm thước nghiệm thu nội dung tệp, đo xóa/rỗng/sai khuôn làm đỏ. |

Đếm: **4 lớp, 4 finding, 5 biểu hiện**. Hai biểu hiện F01 được gom cùng cơ chế; không tách chúng để tăng số finding. Không tuyên bố đóng lớp L6 từ việc sửa xong một mẫu Markdown.

## TỔNG

| Mức | Số finding còn mở |
|---|---:|
| P0 | 0 |
| P1 | 0 |
| P2 | 2 |
| P3 | 2 |
| Tổng | 4 |

Kết luận: **request_changes**. Hai finding P2: thước đo doctrine không đủ chứng minh lời khẳng định (F01) và trần thiệt hại được khai tuyệt đối dù có ngoại lệ cạnh tranh đã chấp nhận (F03). Hai P3: neo dòng sai (F02), thiếu nghiệm thu mục tiêu8 (F04). Quyết định chủ kho giữ canary “chỉ lần thử cuối quyết định” được tôn trọng; ba ca trộn A13 đo đúng.
