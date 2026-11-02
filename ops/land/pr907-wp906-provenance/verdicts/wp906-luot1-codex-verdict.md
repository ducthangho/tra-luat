verdict: approve
reviewed_head: 35d87eb073ae8c6f79049c0097b4208cc2139c47
reviewed_sha: 35d87eb073ae8c6f79049c0097b4208cc2139c47
reviewed_tree: d9aaf7d988367fa8f051d806c9af92ca11a157f8
review_class: sensitive
provider: openai_codex
model: gpt-6.1-sol
model_family: openai
reasoning_effort: xhigh
execution_surface: codex_cli
transport: machine
review_round: 1/2

## Kết luận

**Approve** bản vá trên exact head `35d87eb073ae8c6f79049c0097b4208cc2139c47`, tree `d9aaf7d988367fa8f051d806c9af92ca11a157f8`: N1–N3 đạt, không có finding P0/P1/P2/P3 mở trong phạm vi hai dòng chú thích.

Cổng công cụ đỏ sẵn vì thiếu `shellcheck`, delta base/head bằng 0. Suite chế độ gate kết thúc rc=0 trên cả hai, 60/60 ca đo được đạt và một ca môi trường bỏ qua; **toàn bộ 490 đột biến, Windows native và CI/check run trên exact head: KHÔNG ĐO ĐƯỢC**. Chưa xác nhận hoàn thành toàn bộ điều kiện merge của spec. Đã giữ review offline, không sửa sản phẩm, không merge/land/deploy; mọi hiện vật phát sinh nằm trong `out/`.

## Neo và môi trường

- Đầu lượt: `git -C cay-kho rev-parse HEAD 'HEAD^{tree}'` → head `35d87eb073ae8c6f79049c0097b4208cc2139c47`, tree `d9aaf7d988367fa8f051d806c9af92ca11a157f8`.
- Base: cùng lệnh trên `nen` → head `1c20f3bd6a7ed08114feaf1d91c0790360b8f581`, tree `ecc03182c2359a1fa9c50a9bf87a8bb0cc34f5e0`.
- `sha256sum evidence/spec.md` → `683d648a678e93ec874d32e9d611aca88d756cd2088391ddbfb406d807452337`, đúng giá trị yêu cầu.
- `GIT_OPTIONAL_LOCKS=0 git -C {cay-kho,nen} status --porcelain=v1 --untracked-files=all`: cả hai output rỗng đầu lượt và lần kiểm tra cuối. `out/final-audit.json`: head/tree giữ nguyên, SHA-256 của 5.363 tệp được theo dõi ở mỗi cây đều giữ nguyên, không có `.pyc`; spec SHA-256 vẫn đúng. Cả hai clone đang detached HEAD ở đúng OID yêu cầu; remote khai báo đúng `https://github.com/ducthangho/tra-luat.git` (chỉ đọc config local).
- Lease offline chỉ là bằng chứng cung cấp, không xác nhận authority/live CI. Header `runs/ca68315e/stderr.log:2–11` công bố Codex CLI `0.163.0`, model `gpt-6.1-sol`, effort `xhigh`; bản trích tại `out/cli-header.txt`.
- Môi trường đo: Python `3.13.16`, PyYAML `6.0.3`, Linux x86_64. Đã đọc `AGENTS.md` cùng các mục review/gate trong protocol và `CLAUDE.md`. Hai bản sao riêng tại `out/head`, `out/base`; chỉ cấu hình Git của bản sao được đổi.

## Bảng finding

| ID | Mức | Tệp:dòng | Bằng chứng | Hướng sửa bằng lời |
|---|---|---|---|---|
| — | — | — | Không có finding P0–P3 trong phạm vi bản vá sau 5 hướng săn và đối chiếu base/head. | — |

## Bảng N1–N3

| Tiêu chí | Kết quả | Bằng chứng |
|---|---|---|
| N1 | ĐẠT | `TEN_PYTHON` tại `ops/cong_cu.py:113`, `_python_theo_path:131–137`, `_chay:139–148`; installer `ops/cai_cong_cu.sh:20–29`: cùng thứ tự tên, thêm `-3` chỉ khi chọn tên `py`, thiếu hết trả lỗi, không fallback `sys.executable`. Câu không nói `py -3` luôn được dùng trên mọi nền. Phần L1 giữ nguyên từng byte. Git xác nhận merge #888 `42143ad00154e1038bbecf820bc34d10761215b9` thuộc tổ tiên base, commit message ghi #886; code checker/installer không đổi từ merge đó. `out/hunt-results.json`: 8/8 phản chứng N1 đạt. |
| N2 | ĐẠT | `PYTHONDONTWRITEBYTECODE=1 python3 -B out/measure_static.py`: `yaml_safe_load_equal=true`, `all_changed_lines_whitespace_comment=true`; 4 dòng diff = 2 xóa + 2 thêm, đều có 6 khoảng trắng rồi `#`. |
| N3 | ĐẠT | `changed_files="M\\tops/cong_cu.yaml"`, numstat `2 2 ops/cong_cu.yaml`; chỉ một opcode replace dòng 25–26; `outside_lines_25_26_equal=true`; 106 LF mỗi bản, CRLF=0, bare CR=0, có LF cuối, không trailing whitespace. Diff tự đo khớp byte `evidence/diff.patch`; tệp làm việc khớp Git blob. Chi tiết tại `out/static-results.json`. |

## Cổng

Đo trên bản sao `out/head` và `out/base`; mỗi lệnh có `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR` tuyệt đối dưới `out/tmp`, Python có `-B`. Lệnh/rc/thời gian/stdout/stderr lưu riêng trong `out/logs/{head,base}-*.{json,stdout,stderr}`. Rc dưới đây là của cổng con, không phải rc=0 của script thu thập.

| Cổng | Base | Head | Delta / bằng chứng dương |
|---|---|---|---|
| `python3 -B ops/cong_cu.py kiem-tra --json` | rc=2 | rc=2 | Parse JSON được; 7/8 công cụ DAT, shellcheck KHONG_DO_DUOC; canary blocking DO vì thiếu shellcheck. So JSON đối tượng và stdout byte đều bằng nhau; delta=0, đây là nền máy. |
| `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` | rc=0 | rc=0 | Cùng output: `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine`. |
| `git config --local core.abbrev 7` rồi `python3 -B scripts/tl.py doc-claims-check --strict` | rc=0 | rc=0 | `ok=true`, `files_scanned=113`, `flags=[]`, mọi by_layer=0, 396 advisory lịch sử; toàn bộ stdout byte và JSON bằng nhau, delta=0. |
| `PYTHONUTF8=1 CONG_CU_TEST_BAN_KINH=manh python3 -B ops/cong_cu_test.py` | rc=0; 390,644 s | rc=0; 387,480 s | `60/60 đạt; tổng=61, bỏ qua=1, tiền kiểm bỏ qua=0`, cổng cây thật ĐẠT; tự kiểm bộ phân hạng/giàn giáo/song song ĐẠT. t47 KHÔNG ĐO ĐƯỢC vì không dựng được INDEX chưa hòa giải (`stage={0}`). Chế độ gate giao 490 đột biến sang mảnh, không tính là đo đủ 490. Stdout hai bên bằng byte; stderr chỉ khác đường dẫn bản sao, cùng SyntaxWarning về escape có sẵn. `out/suite-delta.json`. |
| Full `ops/cong_cu_test.py` gồm toàn bộ đột biến | KHÔNG ĐO ĐƯỢC | KHÔNG ĐO ĐƯỢC | Chưa chạy trọn vòng đột biến rất lâu; không ghi xanh. |
| `ci.yml` check run exact head / review connector | KHÔNG ĐO ĐƯỢC | KHÔNG ĐO ĐƯỢC | Packet chỉ cung cấp dữ liệu offline; không mạng/GitHub. Không suy xanh hoặc merge-ready. |

## Các hướng săn

Đã chạy các phép đo sau; script/phản chứng chỉ tồn tại dưới `out/`, không có patch sản phẩm.

| Hướng | Giả thuyết | Lệnh / điểm đọc | Output thực | Kết luận |
|---|---|---|---|---|
| H1 — hành vi Python | Thứ tự tên sai, Python hỏng bị bỏ qua, hoặc checker fallback trình đang chạy. | `PYTHONDONTWRITEBYTECODE=1 python3 -B out/hunt.py`; import mã từ `out/head`, dựng executable giả trong `out/tmp`. | 8/8: `python` thắng `python3` dù ở thư mục sau; cùng tên lấy thư mục đầu; Python hỏng giữ rc=17; chỉ python3 → rc=0, `Python 3.12.7`; chỉ py → argv có `-3`, output `-3 --version`; thiếu hết → rc=None và `khong_khoi_chay:khong co python, python3, py tren PATH`; mô phỏng PATHEXT `.EXE` giải `py.EXE -3`. | KHÔNG PHẢI LỖI. Mô phỏng Windows không được tính là chạy Windows thật. |
| H2 — consumer chú thích / cổng tài liệu | Có công cụ so raw comment hoặc chuỗi nợ khiến bản vá đổi kết quả gate. | `rg -l` chuỗi `cong_cu\.yaml` trong Python/shell/YAML/workflow; xem `ops/cong_cu.py:19–20`, `ops/cai_cong_cu.sh:94`, `.claude/dev/packet_loop.py:1620–1645`, `scripts/tl_core/workflow.py:990–1020`; chạy cả ba cổng trên base/head rồi `out/hunt.py` so output. | Checker/installer dùng `yaml.safe_load` và UTF-8; doctrine mặc định quét adapter Markdown + CLAUDE.md; doc-claims mặc định quét Markdown, không quét khối YAML này. Tools/doctrine/claims: `stdout_bytes_equal=true`; JSON tools/claims: `json_objects_equal=true`. Danh sách điểm tham chiếu: `out/yaml-consumers.txt`. | KHÔNG PHẢI LỖI trong các consumer/cổng đã đo; không suy rằng scanner tài liệu xác minh ngữ nghĩa chú thích YAML. |
| H3 — nợ vẫn mở / neo #886–#888 sai | Kho hiện vẫn coi nợ Python là mở, hoặc #888 chưa chứa sửa code. | `rg -n --max-columns 350 --max-columns-preview 'python-probe-khong-theo-PATH' --hidden -g '!.git/**' cay-kho` (lưu `out/debt-references.txt`); `git show -s --format='%H%n%P%n%B' 42143ad`; `git merge-base --is-ancestor 42143ad 1c20f3bd6a7ed08114feaf1d91c0790360b8f581`; `git diff 42143ad HEAD -- ops/cong_cu.py ops/cai_cong_cu.sh`. | 30 dòng tham chiếu: 4 ở code/test/changelog/chú thích hiện tại, 26 ở hồ sơ lịch sử `ops/land/`. Changelog wp886 ghi closing debt; `pr888-wp886-land-evidence.yaml:109` là `trang_thai: dong`; dòng 110 mở riêng nợ chú thích lỗi thời. Commit merge ghi đúng PR #888, #886; ancestor rc=0; diff hai tệp code rỗng. Readback offline #888: merged=true, merge SHA `42143ad…`, merged_at `2026-10-24T03:01:16Z`. | KHÔNG PHẢI LỖI. Các chữ “mở” ở snapshot #858/#868 là lịch sử, không phải một nợ mới do patch. `landed: false` trong hồ sơ #888 nói về assurance/provenance, không phủ định code đã sửa hay nợ kỹ thuật đã đóng; không suy trạng thái live. |
| H4 — Unicode / cp1258 | Hai dấu `→` mới làm bộ đọc YAML hỏng trên Windows. | `out/hunt.py`: parse bytes, UTF-8 explicit, gọi `doc_ban_ke`, rồi thử raw decode `cp1258` trên cả hai; đối chiếu các điểm đọc UTF-8. | Cả hai: UTF-8 parse=true, bytes parse=true, `doc_ban_ke`=true. Raw cp1258 đều lỗi `UnicodeDecodeError`, cùng offset=31, byte=0x8a (trước khối đổi). `·`: 9→9; `→`: 0→2. | KHÔNG PHẢI LỖI ở bộ đọc thực đã đối chiếu; đọc sai cp1258 đã hỏng trên base. Windows native: KHÔNG ĐO ĐƯỢC trên Linux, không ghi xanh. |
| H5 — whitespace / độ dài | Chú thích dài hoặc Unicode gây hỏng layout/line ending, hoặc làm biến nghĩa câu L1. | `python3 -B out/measure_static.py`, so bytes `splitlines(keepends=True)`. | Dòng 25/26 head: 115/124 ký tự; lân cận dòng 24=123, 27=154, 28=139, 29=281. Ngoài hai dòng bằng byte, L1 bằng byte, không trailing whitespace, 106 LF và newline cuối giữ nguyên. | KHÔNG PHẢI LỖI. Cụm “in ứng viên” thuộc L1 có từ base; patch giữ nguyên đúng phạm vi N1, không thay hành vi kênh kết quả wp868. |

Bằng chứng đầy đủ của H1/H4 và delta H2/H3: `out/hunt-results.json` (lệnh rc=0).

## Tiến độ

1. Đã đọc spec/diff/numstat và đo neo đầu lượt; tiếp theo kiểm mã, N1–N3 và các cổng.
2. Đã đo N2/N3, đối chiếu mã N1, tạo bản sao và lưu snapshot SHA-256 của toàn bộ tệp được Git theo dõi ở hai cây gốc trong `out/initial-snapshot.json`.

3. Cổng nhanh hoàn tất trên head/base: tools rc=2 vì shellcheck vắng, doctrine rc=0, doc-claims strict rc=0; log được lưu ngay khi từng cổng kết thúc.

4. Hoàn tất 5 hướng săn độc lập: phản chứng N1 8/8; cả ba cổng nhanh có stdout bằng byte trên base/head; neo #886/#888 và trạng thái nợ được đối chiếu bằng Git + hồ sơ offline; kiểm Unicode và độ dài không thấy hồi quy trong patch.

5. Suite trên cả hai qua 60 ca đo được, bỏ qua cùng một ca môi trường t47; đã lưu trạng thái tạm trước khi tự kiểm kết thúc. `git diff --check 1c20f3b HEAD` rc=0, output rỗng; raw diff giữ mode `100644` ở cả hai.

6. `PYTHONDONTWRITEBYTECODE=1 python3 -B out/final_audit.py` rc=0: hai cây gốc sạch, neo không đổi; toàn bộ 5.363 tệp được theo dõi/cây giữ nguyên byte; không phát sinh `.pyc`, spec hash giữ nguyên. Sau bước này chỉ chạy suite trên bản sao; neo và độ sạch tiếp tục được đo lại sau khi suite kết thúc.

7. Suite chế độ gate kết thúc rc=0 trên base/head, không timeout; stdout bằng byte, stderr chỉ khác gốc bản sao. Kết luận cuối `approve` cho phạm vi bản vá, không có finding mở; full 490 đột biến/live CI/Windows native được giữ trạng thái KHÔNG ĐO ĐƯỢC. Đã chạy lại audit cuối sau suite.
