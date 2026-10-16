<!-- Verdict codex lượt 1/2 (gpt-6-astra, reasoning effort xhigh — xác nhận ở header log runtime: "reasoning effort: xhigh", session 01a0e37c-0b37-77f0-9ff0-94b211365338), codex_cli tại chỗ, sandbox clone riêng, trên claude/spec-c1a1-doc-receipt-20260925 @ 96a9322 (tree 60373d7), base 5618f61c, spec sha256 978058983e8e…. Chép NGUYÊN VĂN tệp -o; không sửa chữ nào. Liên kết /tmp/review650-r1/* là đường trong sandbox reviewer; bản sao probe650.py và ARTIFACTS.sha256 nằm cạnh tệp này. -->
**13 P1 / 1 P2 / 0 P3**

verdict: **changes_requested**

```text
reviewed_sha:  96a93226109038331fb09d2a35bd71b73e6e43be
reviewed_tree: 60373d791a4c07be20c5842584efb7f82fd6b201
base:          5618f61c6ac2fa14aab52b0f5ce3d065aee8e022
spec_sha256:   978058983e8eddefebfba267dbff2ef5cee95daf9b2d4847121d43b8cff89d77
```

Đã ghi [báo cáo đầy đủ](/tmp/review650-r1/verdict.md), [script phản chứng](/tmp/review650-r1/probe650.py) và [băm hiện vật](/tmp/review650-r1/ARTIFACTS.sha256).

Reviewer: `openai_codex / codex_cli / machine`; assurance: `advisory_review`; lượt 1/2. Linux, Python 3.11.15, Ruff 0.16.9. Không có log launcher để chứng thực độc lập model/effort.

Theo định nghĩa mức trong yêu cầu, lỗi nghĩa vụ/oracle A0 **chặn merge theo spec** được xếp P1. Các đột biến sống dưới đây chứng minh lỗi độ phủ; không khẳng định mã sản phẩm hiện chứa chúng.

## Findings

**F1 — P1 — `lech-dac-ta` — K5 ném ngoại lệ với JSON sai kiểu**

Vị trí: `.claude/dev/doc_receipt_thu_hoi.py:82`.

Đã chạy:

```bash
python3 -B /tmp/review650-r1/probe650.py "$PWD" actual
```

Script đo rc 0; tiến trình CLI con với fixture chỉ đổi `ket_luan=[]` trả **rc 1, stdout rỗng**:

```text
TypeError: unhashable type: 'list'
```

`ket_luan={}` cũng ném ngoại lệ. M1/M6 đòi JSON kết quả, K5 `do`, rc 12.

Vá phép kiểm tập đóng để an toàn với mọi kiểu JSON. Thêm ca list/dict/null/số/chuỗi lạ cho API và CLI; tránh trả sớm làm mất trạng thái các luật khác.

**F2 — P1 — `tin-dung-gia` — ngoại lệ vô can cùng loại vẫn được tính giết**

Vị trí: `.claude/dev/doc_receipt_thu_hoi_test.py:63`, `:253`.

Đã chạy:

```bash
python3 -B /tmp/review650-r1/probe650.py "$PWD" credit
```

Rc 0; kết quả:

| Phản chứng, giữ nguyên chốt cần đo | Phân hạng |
|---|---|
| Thêm `len(0)` sau khi K1 đã ghi đỏ; dùng ca/loại ngoại lệ M2d | `witness_killed` |
| Lỗi tra dict vô can cùng `KeyError`, dùng M2e′ | `witness_killed` |
| Lỗi decode tại bước chẩn đoán cùng `UnicodeDecodeError`, dùng M2b′ | `witness_killed` |
| Ngoại lệ khác loại đã khai | `unresolved` |
| Đột biến làm fixture dương đỏ | `unresolved` |
| Đột biến TD làm fixture dương đỏ | `unresolved` |

**Chốt A1 hoạt động**, nhưng tên loại ngoại lệ không chứng minh nguyên nhân thất bại.

Vá `ca()`/`chay_dot_bien`: phân biệt assertion sai kết quả với lỗi implementation; với phép đo exception boundary, cần chứng cứ đúng giai đoạn gây lỗi. Khoá bằng các lỗi cùng loại ở giai đoạn khác ở trên. Tránh bắt rộng rồi biến lỗi implementation thành pass.

**F3–F10, F12–F14 đều P1, slug `dot-bien-tuong-duong-hoac-thieu`.** Mỗi hàng là một đột biến sống riêng.

Cả **11** lệnh suite dưới đây đã chạy, đều **rc 0**, cùng output:

```text
nghia vu: witness_killed 82 · equivalent_verified 7 · unresolved 0
doc_receipt_thu_hoi tests: 109/109 ca QUA · 82/82 dot bien GIET
```

Các thay thế chính xác và phép đo A/B nằm trong script phản chứng. Trong bảng, `test` là `.claude/dev/doc_receipt_thu_hoi_test.py`.

| ID, vị trí | Đột biến sống và kết quả A/B | Lệnh tái hiện đã chạy | Đề xuất vá |
|---|---|---|---|
| **F3**, `test:172` | Nới `[0-9a-f]` thành `[0-9a-z]`. `T="g"*40`: gốc đỏ, mutant **ok=true**. | `python3 -B /tmp/review650-r1/hex_charset/.claude/dev/doc_receipt_thu_hoi_test.py` | Tách bảng chữ cái hex khỏi chữ thường; thêm chữ ngoài `a–f` cho hex40/64. Tránh blacklist chỉ riêng `g`. |
| **F4**, `test:174` | Predicate int nhận float. `run_id=1.5`: gốc đỏ, mutant **ok=true**. | `python3 -B /tmp/review650-r1/int_float/.claude/dev/doc_receipt_thu_hoi_test.py` | Tách vế “phải int” khỏi “không bool”; thêm float/string/null. Giữ số nguyên hợp lệ và khai chốt K1 che schema. |
| **F5**, `test:176` | Nới `{64}` thành `{64,65}`. SHA-256 65 ký tự: gốc đỏ, mutant **ok=true**. | `python3 -B /tmp/review650-r1/hex64_length/.claude/dev/doc_receipt_thu_hoi_test.py` | Thêm ID độ dài hex64, ca 63/64/65 cho hai trường; giữ null của descriptor. |
| **F6**, `test:177` | Timestamp nhận `[ZX]` thay `Z`. Hậu tố `X`: gốc đỏ, mutant **ok=true**. | `python3 -B /tmp/review650-r1/timestamp_z/.claude/dev/doc_receipt_thu_hoi_test.py` | Tách đủ thành phần mẫu timestamp, không chỉ chữ T. Tránh thêm kiểm lịch ngoài spec. |
| **F7**, `test:67`, `:141` | Trả `ok=int(all(...))`: mutant trả **1** thay bool nhưng oracle vẫn xanh. | `python3 -B /tmp/review650-r1/ok_not_bool/.claude/dev/doc_receipt_thu_hoi_test.py` | Thêm ID kiểu kết quả; kiểm `type(ok) is bool` tại API/CLI. Không dùng phép bằng để thay kiểm kiểu. |
| **F8**, `test:114`, `:156` | CLI chỉ in `{"ok": true}`, mất `luat`/`ly_do`; vẫn rc 0 và suite xanh. | `python3 -B /tmp/review650-r1/cli_dict_lost/.claude/dev/doc_receipt_thu_hoi_test.py` | So toàn dict CLI với hàm trên cùng đầu vào, cả rc 0/12; không ghim thứ tự khoá ngoài hợp đồng. |
| **F9**, `test:157` | Decode trước BOM, rồi decode lần hai. Trace mutant thường: **decode,slice,decode,parse:str**; BOM: **decode,slice**. | `python3 -B /tmp/review650-r1/bom_order_v2/.claude/dev/doc_receipt_thu_hoi_test.py` | Thêm ID/spy đo thứ tự, số decode và chính str truyền parser; tránh chỉ kiểm source hoặc để spy tự gây đỏ. |
| **F10**, `test:67`, `:144` | Đổi phần tử lý do thành số: ca đỏ trả **`ly_do=[0]`** vẫn qua. | `python3 -B /tmp/review650-r1/reasons_not_strings/.claude/dev/doc_receipt_thu_hoi_test.py` | Kiểm list, từng phần tử str và lý do K1 đỏ cho K2–K5. Không ghim văn phong ngoài spec. |
| **F12**, `test:186` | Ghim kho mặc định. Caller và cả nhóm đổi sang `other/repo`: gốc **ok=true**, mutant **K3 do**. | `python3 -B /tmp/review650-r1/kho_fixed/.claude/dev/doc_receipt_thu_hoi_test.py` | Thêm chiều dương caller kho khác cùng nhóm khớp; giữ âm chỉ đổi receipt. Không nới host/workflow. |
| **F13**, `test:187` | Ghim nhánh `master`. Caller `main` và nhóm đồng bộ: gốc **ok=true**, mutant **K3 do**. | `python3 -B /tmp/review650-r1/nhanh_fixed/.claude/dev/doc_receipt_thu_hoi_test.py` | Thêm chiều dương caller nhánh khác; giữ loại ref `refs/heads`. |
| **F14**, `test:172`, `:208` | `_khop` ép int thành str. `T=int("1"*40)`: gốc đỏ, mutant **ok=true**. | `python3 -B /tmp/review650-r1/hex_numeric_coerce/.claude/dev/doc_receipt_thu_hoi_test.py` | Tách ID bắt buộc str khỏi mẫu hex; thử số dài 40/64 chữ số để độ dài không che lỗi. Giữ các vế nullable. |

**F11 — P2 — `lech-dac-ta` — regex timestamp hẹp hơn đặc tả**

Vị trí: `.claude/dev/doc_receipt_thu_hoi.py:34`.

Đã chạy:

```bash
python3 -B /tmp/review650-r1/probe650.py "$PWD" extra
```

Rc 0. `٢026-09-25T01:25:14Z` khớp regex `\d...` của spec nhưng module dùng `[0-9]`, trả **K2 do**. Chưa có bằng chứng producer thật phát chữ số Unicode; đây là lệch miền chấp nhận.

Vá theo regex đóng băng, thêm ca phân biệt ASCII/Unicode. Nếu muốn ASCII-only, cần authority/revision riêng; không tự sửa spec mang theo hoặc thêm ràng buộc lịch ngoài M3.

## Audit A0

`DB` có 58 ID, `_theo_truong()` thêm 31. **89 là số ID hiện có, chưa phải số nghĩa vụ đã audit đủ.**

| Mệnh đề M1–M6 → M8 | ID | Nhận xét |
|---|---|---|
| M1 hàm thuần, không git/mạng | Không có ID riêng | Code hiện phù hợp qua đọc source; thiếu disposition A0 cho purity. |
| M1 dict kết quả; bool; năm trạng thái; list[str] | M1a–d | Vectơ luật được đo. Thiếu ID kiểu kết quả; oracle không phân biệt F7/F10. |
| M1 ok khi mọi luật qua | M1a | all→any bị giết; không thay kiểm kiểu. |
| M1 chạy mọi luật; K1 đỏ lan kèm lý do | M1b/c | Trạng thái/không dừng sớm có đo; thiếu oracle nội dung lý do lan, F10. |
| M1 CLI một dòng, đúng dict | M1n | Chỉ bảo vệ một dòng và ok; thiếu parity dict, F8. |
| M1 rc 0/12/2, OSError | M1e–g, h–m | Đọc rc trực tiếp; nhánh JSON unhashable sai, F1. |
| M1 bốn chuỗi không rỗng | M1h–k | Kho/nhánh có ca; base/head TD đúng nhưng suite chưa thử rỗng. Reviewer thử thêm đều rc 2. |
| M1 base/head hex thường 40; tham số sai | M1l/m | Ca 39 ký tự có răng; chưa tách đầy đủ miền hex và lời gọi thiếu option. Reviewer thử thêm 41/chữ hoa/nonhex đều rc 2. |
| M1 không cấp land/provenance; caller readback | Không có ID runtime | Docstring khai đúng; đây là giới hạn lời khai được audit tĩnh. |
| M2 BOM đỏ | M2a/a′ | BOM riêng TD đúng; BOM ghép bị giết. |
| M2 BOM trước decode; decode một lần | **Không có ID** | F9 sống. |
| M2 UTF-8 strict, UnicodeDecodeError đỏ | M2b/b′ | Ca 0x80 có đo; classifier còn lỗ F2. |
| M2 parser nhận chính str, không bytes; lỗi JSON đỏ | M2c/c′ | Cả bốn UTF16/32 tới parser và giết loads(bytes). Chưa đo identity str, liên quan F9. |
| M2 root dict | M2d | Có null/list; tín dụng TypeError cần sửa F2. |
| M2 đúng 38 khoá, thiếu từng khoá/thừa | M2e/e′ | Đủ 38 ca thiếu, ca thừa; tín dụng KeyError có F2. |
| M2 schema int-không-bool, giá trị 1 | M2f/f′, M3.schema_version | Có True/2; TD K1 che K2 đúng. |
| M2 event hằng | M2g | event_v2 giết bỏ chốt. |
| M3 hex40 str, chữ cái, độ dài, toàn chuỗi; oid nullable | M3a/b/g/n, M3.<trường> | Thiếu ID str/bảng chữ cái đầy đủ, F3/F14. Có biên 39 nhóm C/41 tree_S nhưng chưa tách ID độ dài. |
| M3 hex64; descriptor null hoặc hex64 | M3e/h, ID theo trường | Thiếu ID độ dài, F5; str/chữ cái F3/F14. Vế descriptor null chỉ ở fixture, thiếu ID riêng. |
| M3 int, không bool; job_id không null | M3c/d, ID theo trường | Bool/null job_id có đo; thiếu vế int, F4. |
| M3 timestamp toàn mẫu | M3f, M3.thoi_diem_utc | Chỉ tách chữ T; thiếu các nhóm số/dấu/Z/biên của mẫu, F6. Code lệch `\d`, F11. |
| M3 policy/profile nullable; discovery str | M3i/j, ID theo trường | Có ca sai miền, ca dương dict/str. Hai vế null chỉ ở fixture, thiếu ID/disposition riêng. |
| M3 ba dict và hai list | ID theo từng trường | Bỏ áp predicate giết đúng ca. |
| M3 ba C đồng nhất; nhóm đúng kiểu; C khác S | M3k–n, ba TD theo C | Có ca riêng quan hệ, nhóm sai kiểu, nhóm dương khác S; TD đúng. |
| M4 kho/nhánh từ caller | M4a/b | Chống lấy từ receipt có răng; chưa chống ghim mặc định, F12/F13. |
| M4 bốn phép bằng và ba hằng | M4c–i | Ba mutant nới hằng bị giết đúng ca. |
| M5 S/base, H/head, nguồn caller | M5a–d | Bốn mutant bị giết đúng ca. |
| M6 rc=0, kết luận tập đóng, chế độ hằng | M6a–c | Bỏ từng vế bị giết; kiểu unhashable bị bỏ sót, F1. |
| M8 đăng ký, hai cặp bằng nhau và >0 | M8a/b, ca_dang_ky | Mẫu đúng spec; hai backreference có răng; 0/0 bị bác. Đăng ký/>0 chưa có ID riêng, nhưng có assertion chạy thật. |

Các hàng thiếu ID vẫn là thiếu nghĩa vụ A0 dù code hiện tại làm đúng hoặc fixture tình cờ đi qua. Không dùng tổng 109/109, 82/82 để đóng chúng.

**Bảy dòng TD đều kiểm được và đúng:** M1j, M1k, M2a, M3.schema_version và ba ID C. Đã chạy lại từng mutant, thêm probe CLI rỗng, schema True/1.0/2, C null/số/39 ký tự. Không tìm thấy TD sai. Không suy ba TD bỏ riêng thành bỏ cả nhóm tương đương.

## Đối chiếu nghiệm thu và lời khai

- **M7/fixture:** FIX bằng receipt thật toàn bộ giá trị và kiểu; đủ 38 khoá, `KHOA` khớp. Băm receipt đúng `ca67dc6a817b7cf8643616e4762d5f3e95c0ec7a46cf9693f9436b47c00f5960`.
- **A0:** failed theo audit trên.
- **A1:** fixture dương xanh; các control làm fixture đỏ được `unresolved`.
- **A2:** bốn encoding thực sự qua decode UTF-8 strict rồi mới bị parser str bác; mutant parser bytes bị giết cả bốn.
- **A3–A5b:** có ca và mutant; giữ caveat tín dụng ngoại lệ F2.
- **A6:** thiếu phân rã predicate. C có ca đơn trường sai đồng nhất và nhóm sai kiểu, chưa có ba ca riêng sai kiểu.
- **A7:** quan hệ C, nhóm sai kiểu, nhóm dương khác S đều có đo.
- **A8:** các hằng/nhóm âm có răng; thiếu chiều caller đổi cùng nhóm.
- **A9:** bốn mutant bị giết.
- **A10:** ba mutant bỏ vế bị giết; hành vi sai kiểu kết luận có F1.
- **A11:** ca K3+K4 và mutant dừng sớm đổi màu đúng.
- **A12:** đọc `returncode` trực tiếp; những ca đã có đúng, F1 mở nhánh rc 1 ngoài hợp đồng.
- **A13:** đăng ký/regex đúng; consumer thật với riêng suite mới rc 0. Chưa chạy `--chay` toàn registry; không khai toàn A13 pass.
- **A14:** **+391/−0**, đúng ba tệp sản phẩm. Đây là **ngoại lệ có phạm vi ≤400**, không phải đạt trần 300. Spec mang theo +331 dòng, băm không đổi.
- **A15:** hai lệnh đều rc 0, có bằng chứng dương.

Docstring nói rõ `ok: true` không cấp quyền land/provenance. Số suite và +391 trong commit message tái lập được. Không có finding lời khai độc lập ngoài các thiếu sót A0 đã nêu.

## Đã chạy

| Lệnh | Rc và bằng chứng |
|---|---|
| `git rev-parse HEAD 'HEAD^{tree}' origin/master` | 0; đúng ba OID đầu báo cáo, cả đầu/cuối. |
| `sha256sum` spec và receipt | 0; cả hai khớp assignment, cả đầu/cuối. |
| `python3 -B .claude/dev/doc_receipt_thu_hoi_test.py` | 0; **109/109**, **82/82**; witness 82, equivalent 7, unresolved 0. |
| `python3 -B .claude/dev/ci_dang_ky_test.py` | **1**; đăng ký 22/22, launcher 4/4, Ruff contract 3/3; subprocess Git fixture rc 128 do signer môi trường. |
| `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false python3 -B .claude/dev/ci_dang_ky_test.py` | **0; 916/916 phản chứng đỏ đúng, TỔNG: ĐẠT**. Chỉ đổi môi trường child cho commit fixture. |
| `python3 -m ruff check --no-cache --select F .claude/dev/doc_receipt_thu_hoi.py .claude/dev/doc_receipt_thu_hoi_test.py .claude/dev/ci_dang_ky_test.py` | 0; All checks passed. |
| Ruff F trên bytes registry tại `origin/master`, qua `--stdin-filename` | 0; All checks passed. Hai module mới không có lỗi F; **delta F=0**. |
| `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` | 0; 10 tệp, 0 chỗ chép doctrine. |
| `python3 -B .claude/dev/packet_loop.py adr-song --root .` | 0; 50 ADR/50 dòng khớp 1–1. |
| `git diff --numstat origin/master..HEAD --` ba tệp sản phẩm | 0; **1+109+281=391** dòng thêm. |
| `git diff --check origin/master..HEAD` | 0; không lỗi whitespace. |
| Script phản chứng, mode `actual`, `credit`, `mutants`, `extra`, `caller`, `targeted`, `registry` | Mỗi script rc 0; rc con ghi riêng trong log. **11 mutant suite sống**, 21 ca đích cho 18 mutant kiểm bổ sung thất bại đúng assertion. |
| Probe từng dòng TD | 0; **7/7 equivalent_verified**, có probe bổ sung. |

Hai thử nghiệm không được tính sống: bỏ guard str làm meta-test M3g `unresolved 1`; bản thử thứ tự BOM đầu tiên trùng mỏ neo làm `unresolved 2`. Bản BOM sửa phép đo, giữ mỏ neo duy nhất, sống và có trace thật ở F9.

CI remote/full CI/Windows và `--chay` toàn registry: **not_run**. Lease/generation/GitHub state và model/effort runtime: **not_measured** trong phạm vi offline. Không có check skipped nào được tính pass.

Lệnh registry nguyên bản khiến signer Git thử kết nối localhost và bị sandbox chặn; không có kết nối thành công. Không gọi API/remote, không push hay commit thay đổi sản phẩm.

`git checkout -- .` đã thử, **rc 128** vì `.git/index.lock` read-only. Không lách quyền. Toàn bộ mutant nằm ngoài checkout; ba tệp sản phẩm so byte với snapshot đầu **3/3 không đổi**, diff/index rỗng, HEAD/tree/base/spec giữ nguyên. Status đầu/cuối giống nhau, chỉ có `.codex/` ignored đã có sẵn.