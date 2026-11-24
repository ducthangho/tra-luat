# Review wp1236 đợt C — lượt 1

**changes_requested** — 1 P1 và 1 P2, hai lớp nguyên nhân. Đây là review offline của mã; chưa đủ điều kiện merge.

- Reviewed SHA: `ac523aebd876640b369e94511fd44e81bace0908`
- Tree: `e62a4e166e9f181f2a291337d8c527dd84fbaf7e`
- Base: `f602325574c62184caf16309631f5f680ca5cee2`
- Spec r12/g1: SHA-256 `4589daf1fd666b03a68b7d7dcd5c60903c10e946963fd324c9ee6185ed8e2dc7`; blob `e5583bc042448517b94eadda57231dfc60e0a284`, bytes nguồn Git khớp `SPEC.md`.
- Reviewer: `openai_codex / codex_cli / machine/local`, họ `openai`, run `818363af`; độc lập với executor. Model/effort thực phục vụ: `KHONG_DO_DUOC`; không suy từ cấu hình yêu cầu. Sandbox thực tế `workspace-write`; các lệnh giữ checkout chỉ đọc, mọi nháp/bản sao/cache trong `work/`. Không gọi mạng/GitHub, không đăng verdict hoặc cấp authority.

## Bảng lớp

| Slug | Finding / biểu hiện | Mức mở | Vá chung và phép đóng |
|---|---|---|---|
| `archive-loc-mat-du-lieu-kiem` | C01: lọc mất symlink YAML trước validator; ca hiện tại chỉ thiếu provenance | P1 | Bảo toàn thông tin mode khi kiểm cây/archive, không cần dựng symlink. Đối chứng provenance thường đạt; thêm symlink fixture phải bị chặn với lý do đúng. |
| `hop-dong-dau-ra-duong-dan-tu-do` | C02: `passed`, `owner_waived`, lý do chứa path đều có thể vỡ dòng | P2 | Chốt miền ký tự hoặc quy tắc hiển thị trong spec; áp thống nhất ba cửa và đo số dòng/rc/lý do. |

Lượt đầu, không có bảng đối chiếu verdict trước. Hai finding đều là **hành vi của mã gốc**, không phải đột biến ngoài manifest; không áp nhãn P3 `ngoai_bang_dong`.

## C01 — P1: lọc archive biến hồ sơ bị từ chối thành hồ sơ được đóng WP

Vị trí: `.claude/dev/packet_loop.py:3965–3968`, `_d2b_kiem`. `filter=... if m.isreg() else None` xoá mọi symlink trước khi module được đọc dữ liệu. K2 của spec và `chon_provenance` yêu cầu ghi lý do `symlink` khi gặp symlink YAML/thư mục. Chốt mode của D2b chỉ kiểm đường tới tệp đánh giá, không kiểm các thành viên còn lại trong thư mục provenance.

Đo trên **cùng cây O** với symlink `p.yaml → prov.txt` từ fixture `_d2b_cay` đã có sẵn, chỉ thêm tệp thường `regular.yaml` chứa provenance hợp lệ:

| Phép đo | Kết quả |
|---|---|
| Validator module trực tiếp | `not_measured`, `['symlink']` |
| `git ls-tree O .../p.yaml` | `120000` |
| D2b qua CLI đầy đủ | rc **0**, `D2b ĐẠT …`, `ĐÓNG ĐƯỢC WP P` |
| Đối chứng mặc định | rc 0, đạt |

Ca `provenance_la_symlink` hiện tại chỉ có symlink, không có provenance thường hợp lệ cạnh nó, nên bị chặn bởi `provenance_0` sau khi symlink mất. Đo lại fixture **nguyên trạng**: module trả `[not_measured, [symlink, provenance_0]]`, còn CLI chỉ báo `kiem_tep:not_measured:provenance_0` ([existing_symlink.json](existing_symlink.json)); vì vậy cả lý do đầu cũng đã bị đổi. Nó không đo trường hợp lọc mất dấu vi phạm trong một thư mục đã có đủ provenance.

Tái lập từ checkout được giao:

```bash
PYTHONDONTWRITEBYTECODE=1 TMPDIR="$PWD/../work/tmp" python3 -B ../work/probe_behavior.py
```

Kết quả: [behavior.json](behavior.json), [behavior.log](behavior.log), rc 0 của script đo. Script sử dụng symlink an toàn sẵn có trong fixture, không soạn đường thoát cây hay symlink mới. Mọi fixture nằm ngoài checkout.

**Hướng sửa:** sửa tại ranh giới cây Git/archive → validator, nơi thông tin đang bị bỏ. Kiểm entry/mode trước giải nén và chuyển tiếp kết quả tương ứng; không nới K2 và không cần giải nén/theo symlink. Quét cả YAML symlink và thư mục symlink thuộc provenance. Khoá bằng đối chứng hợp lệ và biến thể có cả tệp thường + symlink; đột biến bỏ kiểm mode/thông tin phải chết đúng ca. Rủi ro của bản vá: chặn mọi symlink không phân biệt phạm vi có thể siết oan nhánh miễn hoặc tệp không liên quan; giữ phạm vi của từng API. Thư mục symlink trong cây con là biểu hiện cùng cơ chế suy từ mã; không tạo payload mới để đo do giới hạn assignment.

## C02 — P2: đường dẫn tự do phá hợp đồng một dòng

Vị trí: `.claude/dev/packet_loop.py:3914–3915,3956,3977`. `[^/]+` nhận LF. Tên thư mục POSIX hợp lệ `dong` + LF + `moi-provenance` đi qua Git/YAML/archive và cho rc 0 ở cả hai nhánh:

```text
D2b ĐẠT ops/land/dong
moi-provenance/danh-gia-gate-output-44669622916.txt@<O>
```

Nhánh miễn cũng tách `D2b ĐẠT mien ...` thành hai dòng. Khi đường dẫn ấy vắng, dòng stderr `THIẾU  D2b symlink_hoac_mode:…` cũng tách đôi. Bằng chứng: [behavior.json](behavior.json) và [more.json](more.json), script bổ sung [probe_more.py](probe_more.py), rc 0.

Đây là xung đột giữa hai yêu cầu đã đóng: đường dẫn nguyên văn với miền `[^/]+` và đúng một dòng output. Không thể vừa in LF nguyên văn vừa bảo đảm một dòng vật lý.

**Hướng xử lý:** điều phối chốt miền ký tự xuống dòng hoặc quy tắc mã hoá path trong output, cập nhật revision/hash nếu đổi hợp đồng; sau đó sửa chung ba cửa output. Không tự `strip` hoặc chuẩn hoá đường dẫn Git. Ca đóng phải đo cả đạt/miễn/trượt với LF, CR và ký tự phân dòng Unicode theo quyết định đó, bên cạnh đường dẫn thường. Rủi ro: cấm mọi ký tự điều khiển/Unicode sẽ siết quá miền văn bản tự do r12; escape path sẽ đổi hợp đồng raw-path và consumer. Không cung cấp patch sản phẩm dưới vai reviewer.

## Phán quyết các chỗ lệch

1. **Luật 9 trên khối:** chấp nhận cách nối delta theo chỉ thị điều phối; không thay nghĩa vụ không hồi quy. Khối có mọi byte code khớp, chỉ bỏ 2 LF phân cách cuối (`4595 → 4593` byte); băm khối `ceb9f97d…`, hai full-file hash khớp handoff. Bộ nối ghép vào file đầy đủ và gọi `chay_suite` thật; bảng tự kiểm phân hạng chạy riêng. Kết quả cuối ở mục phép đo.
2. **Fixture rút gọn/đổi head:** chấp nhận cho C1/C4/C5c. `kiem_tep` không đọc log; tệp đánh giá + YAML đủ dữ liệu nó dùng. Đo original/adapted lần lượt `passed/[]`, `failed/[]`; header khớp merge M tạm. C4 CLI chỉ báo `kiem_tep:failed:-`, không `neo_*` hoặc D3. C5c ở `ops/khac/…` ra đúng `duong_dan_sai`. Không suy từ việc rút gọn rằng Windows MAX_PATH đã đạt.
3. **Đầu ra riêng của packet_loop_test:** chấp nhận giữ hợp đồng producer/consumer đã đăng ký; không áp nhầm bốn dòng của harness A lên suite tích hợp. Đã đo đủ 16 shard và gom: tập 1.799 ca khớp, carrier đúng một mảnh; gom vẫn rc 1 vì ca socket bị sandbox chặn. Không gọi gate này là đạt.
4. **mC11:** thực tế bỏ mode cho ca symlink dẫn đến rc **8 FileNotFoundError**, không ra ĐẠT như chữ bảng C5. Phép kiểm lý do riêng vẫn phát hiện chốt mode bị bỏ; chấp nhận giá trị phép đo hẹp ấy, không xác nhận kỳ vọng “b ra ĐẠT”. Bộ phân hạng thực tế đã xác nhận mC11 `GIET` đúng `cong_d2b_c5_mode`. Bản thân việc lọc symlink toàn cục bị bác bởi C01.

## Phạm vi quét độc lập

Đã đối chiếu cả hai nhánh nguồn/miễn, kiểu OID/attempt, commit và remote origin, chuỗi path thô, mode tiền tố/lá, nạp mã từ master và dữ liệu từ O, `kiem_tep`, ba neo, `kiem_mien(head=M)`, output và rc. Đã quét các cửa cùng lớp C01/C02; không gộp chúng thành một lớp chỉ vì cùng chạm archive/path. OID lỗi trong `cat-file`/`branch` ra lý do OID đúng điều kiện đặc tả; lỗi `show`/`ls-tree`/`archive` ra rc 8. Không coi remote-tracking ref offline là xác nhận trạng thái GitHub hiện tại.

## Phép đo

Bản máy đọc được và kết quả cập nhật: [VERDICT.json](VERDICT.json). Các log, rc, command và giới hạn được lưu trong cùng `work/`.

- Preflight đạt; 2 tệp, +313/−12, trần +450; `git diff --check` rc 0.
- `chay_suite` đúng harness: D2b + D cũ + CRLF **29/29**, rc 0.
- Ruff 0.15.15 `--no-cache --select F`: base/head đều rc 1, **16 chẩn đoán**, delta 0 sau đối chiếu dịch số dòng F811; chạy trực tiếp ở checkout head và base, [ruff_checkout_comparison.json](ruff_checkout_comparison.json); không gọi bare lint là xanh. Pin/probe contract riêng: rc 0, 3 điểm, 0 lỗi.
- Bộ phân hạng: 1.787 tên cũ × 7 kiểu ngoại lệ = **12.509 phép so**, 0 lệch; đây là phép đo dispatch tổng hợp, không thay suite thực.
- Đột biến khai báo qua harness thật: **head 56/56**, **base 25/25**, rc 0; 31 delta D2b gồm đủ mC1–mC14 đều `GIET` đúng ca đích; 25 đột biến cũ không đổi kết quả, không đối chứng chết oan. [declared_comparison.json](declared_comparison.json).
- D cũ + CRLF trên base: **14/14**, rc 0; cùng nhóm trên head nằm trong 29/29 phía trên.
- Bốn đột biến tương đương: đã kiểm diff AST và miền `None/bytes`, hậu tố ref, regex `^[0-9a-f]{40}\Z`, type của YAML; [equivalence.json](equivalence.json).
- Ngoài khối: lời gọi `_d2b` có mC1; bỏ `import tarfile` trên bản sao bị `cong_d2b_c1_passed_dat` giết với rc 8 có kiểm soát; chuỗi help là văn bản giao diện, không có ca hành vi tự động. Phép bỏ import nằm ngoài manifest đã được đóng bằng ca hiện hữu, không có đột biến sống ngoài bảng.

**16/16 mảnh tích hợp head đã hoàn tất:** 1.799 ca = **1.746 passed + 15 failed + 38 skipped**. Cả 15 ca D2b đã chạy và đạt. Tất cả 15 lỗi đều `socket.PermissionError: [Errno 1] Operation not permitted` ở nhóm B4; đúng ca `cong_b4_vc_loi_ket_noi` trên base cũng rc 1 cùng lỗi ([base_socket_probe.log](base_socket_probe.log)). [head_shards_summary.json](head_shards_summary.json) ghi command/rc từng mảnh và tên từng ca lỗi/bỏ qua. **GOM rc 1**, 14 mảnh đỏ và aggregate failure; không thiếu/lệch phân hoạch hoặc carrier. [gom.log](gom.log). Gate đỏ được giữ nguyên; đây là giới hạn sandbox, không quy thành regression D2b.

Sau 16 receipt hoàn chỉnh, dừng hàng đợi dài bằng SIGINT (rc 130); phần batch 199 đột biến chỉ bắt đầu dở không được tính. Hai lượt riêng head56/base25 đã hoàn tất rc 0. Full baseline base, full mutation 2040/2009 và CA_DAI chưa được chứng nhận. Không dùng bằng chứng executor để khai reviewer đã chạy.

**Luật 9 trên khối:** `do` rc 0, `HOAN_TAT`, **178 = 174 GIET + 4 TUONG_DUONG**, 0 lỗi chạy/vô can; manifest khớp byte executor và không lệch ca giết/phân hạng. [luat9_comparison.json](luat9_comparison.json), [ledger_A.tsv](ledger_A.tsv), [luat9.log](luat9.log). Phần delta này không chứng nhận full non-regression.

## Đối chiếu C1–C9

| Yêu cầu | Ca và bằng chứng reviewer |
|---|---|
| C1 | `cong_d2b_c1_passed_dat`; source_separation đo mã từ master, dữ liệu từ O; mC1, mutant đọc worktree bị GIET. |
| C2 | `cong_d2b_c2_thieu_nguon`; mC2 GIET đúng ca. |
| C3 | `cong_d2b_c3_attempt_kieu`, `cong_d2b_c3_neo`; mC3/mC4/mC9/mC10 GIET đúng các chốt riêng. |
| C4 | `cong_d2b_c4_kiem_tep`; original/adapted đều failed, CLI đúng lý do; mC5 GIET. |
| C5 | `cong_d2b_c5_duong_dan`, `cong_d2b_c5_mode`; C5c đỏ đúng duong_dan_sai; mC6/mC11/mC12 GIET. Giới hạn symlink thành C01. |
| C6 | `cong_d2b_c6_mien`; mC7 GIET, bổ sung source separation nhánh miễn. |
| C7 | Các ca `module_vang`, `module_khong_nap`, `module_nem`, `git_loi`; mC8 GIET. |
| C8 | 14 ca D cũ/CRLF base và head đạt; 25 đột biến cũ delta 0; bộ phân hạng 12.509 so sánh delta 0. |
| C9 | `cong_d2b_c9_oid`, `cong_d2b_c9_oid_khong_phai_commit`; mC13 GIET; mC14 kiểm không in ĐẠT khi vi phạm. |

Toàn bộ 15 ca `cong_d2b_*` (14 hành vi + 1 tự kiểm phân hạng) đã chạy qua `chay_suite` thật. Bảng không thay giới hạn gate tích hợp hoặc các finding.

## Windows và phần chưa đo

**M3 required, bước 2:** diff chạm `.claude/dev/**`; đặc tả cũng khai required. Review này chưa chạy Windows. Lease dẫn quyết định miễn Windows CI; không miễn Windows local, và không có mạng để readback quyết định hiện hành.

Điều phối cần chạy base/head cùng máy/cùng lệnh, đủ ID và kết quả theo M3. Rủi ro cụ thể: MAX_PATH khi fixture/đột biến lồng nhiều tầng; CRLF; Unicode/ngoài BMP và ký tự điều khiển trong argv `git.exe`; backslash/NTFS reserved names/case collision; symlink index mode 120000 và lọc tar; console UTF-8/cp1258; Python 3.12+ `tarfile.data_filter`. Phải giữ skipped/not_run riêng. CI GitHub, Windows và toàn bộ đột biến kế thừa/CA_DAI chưa được review này chứng nhận.

Kiểm checkout cuối: HEAD/tree/base giữ nguyên, `core.abbrev=7`, diff/index sạch; snapshot 19.345 entry trong cây làm việc (kể cả ignored) không đổi từ trước lượt shard dài. `.git` không nằm trong snapshot byte; identity/index được kiểm bằng Git riêng. [final_check.json](final_check.json). Không sửa checkout.

KET_LUAN: changes_requested
