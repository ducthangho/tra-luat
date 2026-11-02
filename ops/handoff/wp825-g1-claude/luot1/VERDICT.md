verdict: changes_requested
reviewed_sha: 46421d7e4365b3490124bef541e243289f4d2006
spec_sha256: dee36a1148bc1fe8a934a9dceb74dbe0eab7d3a2830908d7f15afb3293f0812e
Ket qua: 0 P0, 1 P1, 1 P2, 0 P3.

Ngưỡng áp dụng: không còn P1/P2/P3 theo chỉ thị lượt review; review_class `sensitive`.
Hai finding là lỗi lời khai thực chứng, không phản đối quyết định chấp nhận giới hạn vĩnh viễn của chủ kho.

## Phạm vi và định danh

- Base bất biến: `c7174bfe03b3acd22cfa055b5fce176129d29542`.
- Candidate: SHA dòng 2; tree `3f2274e5b27c49028323828d9813b2166c8307f1`.
- Spec authoritative có sẵn offline tại commit `18a5f89442545943ac7a4965063dc7db01ed8a5a`, đường dẫn `ops/specs/wp825.md`, qua ref `refs/remotes/origin/ops/wp825-r1-g1-lease`. Byte của blob khớp hoàn toàn `../SPEC.md` và băm dòng 3. Lease cùng ref xác nhận r1/g1, `wp825-r1-g1-claude`, hai tệp docs và handoff trên nhánh lease.
- Diff khớp `../diff.patch` về nội dung; chỉ khác độ dài OID rút gọn khi ghim `core.abbrev=7`. Diff đúng 2 tệp, thêm 64 dòng ADR và đúng 1 dòng §20; không sửa runtime/test.
- Reviewer thực tế theo `../run/cd2bdaca/run.json`: `provider: openai_codex`, `execution_surface: codex_cli`, `transport: machine`; run `cd2bdaca`. Executor theo lease: Claude, `claude_code`. Không tự coi khai báo model/effort trong lease là số đo model đã phục vụ từng response; phần đó KHÔNG ĐO ĐƯỢC ở review này. Không cấp merge/land authority hay đăng verdict lên GitHub.
- Linux, Python 3.13.18; không gọi mạng, không dùng credential thật. Shell sandbox thực tế cho ghi workspace và `/tmp`; checkout được giữ chỉ đọc theo chỉ thị, không được mount read-only riêng.
- Snapshot cuối và đối chiếu hash được ghi trong `evidence/final-integrity.json`; giới hạn snapshot: chỉ chứng minh hai mốc quan sát, không chứng minh toàn bộ lịch sử chưa từng có ghi rồi hoàn nguyên.

## Lệnh và hiện vật tái lập

Từ `cay-kho/`, chạy được các script sau; mọi output, bản sao, bytecode/temp đều nằm ngoài cây được review:

```bash
python3 -B ../evidence/review_checks.py
python3 -B ../evidence/check_facts.py
python3 -B ../evidence/repro_probe.py
```

Runner `review_checks.py` chạy các lệnh A1/A2/A4 dưới đây với cwd của từng cây, môi trường sạch không kế thừa credential, `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=../evidence/tmp` (đường tuyệt đối), Git config global/system rỗng và `core.abbrev=7`. Bản base được xuất bằng `git archive` từ exact base, không checkout vào cây được review. Từng command/cwd/rc/stdout/stderr ở `evidence/<base|head>-*.json`.

Không có đường temp ghi được ngoài `/tmp` trong quyền được cấp. `/tmp/.git` tồn tại và `_KhoCodex` từ chối mọi descendant. Không sửa gate hoặc bỏ kiểm tra này để làm A4 xanh; phép thử `unshare -m true` cũng bị từ chối (`Operation not permitted`).

## BANG NGHIEM THU

| Tiêu chí | Lệnh chạy trong gốc cây tương ứng | Bằng chứng dương/âm | Kết luận |
|---|---|---|---|
| A1 | `python3 -B .claude/dev/packet_loop.py adr-song --root .` | HEAD rc=0, `60 ADR trên đĩa, 60 dòng trong §20`; base rc=0, 59/59. Bỏ duy nhất dòng ADR-0061 trên bản sao rồi chạy cùng consumer: rc=9, nêu rõ ADR có tệp mà thiếu dòng §20. | ĐẠT; cả vế dương và âm. |
| A2 | `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` | Base và HEAD rc=0, quét 10 tệp, 0 chỗ chép doctrine. | ĐẠT. |
| A3 dương | `python3 -B ../evidence/review_checks.py` — nối khoảng trắng ADR, kiểm từng chuỗi yêu cầu | `evidence/a3.json`: đủ `CODEX_HOME`, `_danh_dau_auth_hong`, tên ca launcher, tên mutation, `#825`. | ĐẠT phép kiểm năm chuỗi. |
| A3 âm | Cùng script, đối chiếu ADR:35–37, 50–64 và các phép grep sáu cổng | ADR phủ định cổng đọc quyết định; không tự khai test đọc ADR. Tuy vậy nhãn “0 cổng” có lỗi suy rộng theo §20, nêu ở F2. | ĐẠT điều kiện văn bản âm; chưa đủ đóng L6e/§20 do F2. |
| A4 launcher | `python3 -B .claude/dev/launcher_test.py --lap-ca r484_g7_khong_ghi_duoc_trang_thai_tu_choi_phai_noi_ra --lan 1` | Base và HEAD rc=0, `1/1 qua, 0 bo qua, 0 hong`. | ĐẠT riêng ca này. |
| A4 materializer | `python3 -B .claude/dev/launcher_test.py --lap-ca r484_g7_materializer_khong_ghi_duoc_trang_thai_noi_dung_ly_do --lan 1` | Cả hai cây rc=1, `0/1 qua`; lỗi setup `OSError: Codex home is inside a repository`. | FAILED khi chạy; tiêu chí hành vi KHÔNG ĐO ĐƯỢC vì môi trường. |
| A4 credential | `python3 -B .claude/dev/codex_cred_test.py` | Cả hai cây rc=1, nền `13/18 đạt`, `TỔNG: ĐỎ`; 5 ca đỏ, gồm t16/t18 lỗi OSError. Runner dừng trước đột biến do nền đỏ. | FAILED khi chạy; KHÔNG ĐO ĐƯỢC kết quả `TỔNG: ĐẠT`, không quy lỗi setup cho PR. |
| A5 | Không gọi check-run API vì chỉ thị offline | Không có readback check run trên exact head trong dữ liệu đã đo. Các gate local không thay CI. | KHÔNG ĐO ĐƯỢC / not_run. |

Không kết luận toàn bộ acceptance đạt. Lời khai test lịch sử trên máy executor không bị bác chỉ vì sandbox này có bẫy `/tmp/.git`; cũng không dùng lời khai ấy thay bằng chứng reviewer.

## BANG DO

Các đường dẫn/dòng dưới đây trùng base và HEAD đối với mã và test: `evidence/code-identity.json` xác nhận byte của cả bốn tệp giống hệt nhau. `check_facts.py` lưu provenance và số lần khớp mỏ neo trong `evidence/facts.json`.

| Khẳng định trong ADR | Đo được (lệnh hoặc consumer) | Khớp? |
|---|---|---|
| Accepted, r1/g1, băm spec `dee36a11…812e`, quyết định chủ kho | `git show refs/remotes/origin/ops/wp825-r1-g1-lease:ops/specs/wp825.md` và lease cùng ref; SHA-256 bằng bản giao. Chủ kho lựa chọn ADR được nhận làm authority đầu vào theo prompt. | Khớp metadata. Không xác minh độc lập byte câu AskUserQuestion hoặc sự kiện mạng. |
| Nợ sinh từ #484/PR #792 | Hồ sơ local `ops/land/pr792-wp484-land-evidence.yaml`, `ops/handoff/wp484-g7-claude.md` ghi đúng packet, PR và tên nợ. | Khớp hồ sơ lưu; không tuyên bố đã đọc GitHub trực tiếp. |
| `_danh_dau_auth_hong` dùng `_KhoCodex`, trả False với OSError/ValueError/UnicodeError | `sed -n '3589,3620p' .claude/dev/launcher.py`; function ở :3589, return/catch :3602–3604. | Khớp. False không đồng nghĩa chắc chắn state chưa thay đổi (F1). |
| Đã lưu danh tính thì chặn credential ấy | `_doc_rejected` :3565, `_ghi_rejected` :3578, `_dang_cho_snapshot` :3607; guard ở :3875 và `codex_cred.py:518`. Fixture ghi thành công cho ba lối: probe [1,0], đúng danh tính. | Khớp trong các đường đã đo. |
| Không có chỗ lưu dự phòng | `python3 -B ../evidence/check_facts.py`, kết quả `production-state-sites`; đọc `_ghi_rejected` và cả ba nhánh ghi. Một backend/file state, không có nhánh ghi dự phòng trong ba luồng. | Khớp phạm vi runtime đã đọc. Không suy thành kiểm hết mọi dịch vụ ngoài kho. |
| Launcher báo đúng lý do CHẶN riêng | :3895–3897: `KHÔNG ghi được trạng thái chờ snapshot sau khi … — CHẶN: sửa CODEX_HOME (quyền/dung lượng) trước khi thử lại`; ca launcher A4 xanh và đột biến g7 bị giết 1/1. | Khớp. |
| Materializer báo đúng lỗi ghi riêng, giữ credential cũ | :3704–3709: `CHỜ snapshot mới: auth bị từ chối nhưng KHÔNG ghi được trạng thái chờ (OSError) — CHẶN; giữ credential cũ`; fixture I/O cho kết quả này, auth cũ không đổi. | Khớp mã/fixture; ca gốc và mutation target bị chặn setup, không nhận tín dụng giết. |
| `codex_cred.cmd_kiem` báo đúng lỗi ghi riêng | :524–526: `KHÔNG ghi được trạng thái chờ snapshot sau khi … — CHẶN: sửa CODEX_HOME trước khi thử lại`; fixture rc=2 và in đúng câu. | Khớp mã/fixture; suite gốc/t16 mutation chưa đo xanh. |
| Cả ba có ca và mutation khóa | Launcher ca :9154, mutation `g7_nuot_loi_ghi_trang_thai` :13393; materializer ca :9069, mutation `g7_f01_materializer_gop_loi` :13401; credential ca t16 :449, mutation `t16_nuot_loi_ghi` :570. AST đo mỗi mỏ neo đúng 1 lần ở cả hai cây. | Khớp tên/đăng ký. Thực thi mutant launcher: OK giết 1/1; materializer: neutral đỏ môi trường; credential: không chạy mutant do nền đỏ. |
| “Mỗi lần gọi … thêm 1 probe”, luôn từ chối và cùng CHẶN | `python3 -B ../evidence/repro_probe.py`; 4 trạng huống × 3 lối × 2 cây, mỗi trạng huống 2 lượt gọi. | SAI: có [1,0] sau lỗi; lý do lần hai thay đổi (F1). |
| “Không có trạng thái nào bị ghi sai. Kho chỉ không nhớ” | Trong fixture: không ghi nhầm danh tính, auth cũ nguyên vẹn ở mọi trạng huống. Nhưng sau lỗi fsync, đúng danh tính đã được ghi; câu “chỉ không nhớ” sai. Các ca viện dẫn không chứng minh một bảo đảm cho mọi lỗi I/O/xen kẽ. | Chưa đủ cho lời khai tổng quát; gộp F1. Không báo đã tìm thấy ghi sai danh tính hoặc kéo #824 vào scope. |
| Có đường nào >1 probe mỗi lần gọi không? | Đọc `_probe_snapshot`, `_do_codex_song`, `cmd_kiem`, `chuan_bi_xac_thuc`, các wrapper abort khi chuẩn bị thất bại; fixture đếm lời gọi helper. | Chưa thấy >1 lời gọi helper trong một lượt trực tiếp của ba nhánh. KHÔNG đo số HTTP request/retry nội bộ của Codex CLI; không coi đó là số mạng đã đo. |
| Sửa quyền/dung lượng rồi thử lại; login hoặc chuan-bi để khôi phục | Mã cùng các nhánh; fixture lỗi trước replace không lưu state, đối chứng ghi thành công lưu đúng id. `chuan-bi` nhận snapshot từ biến, có guard từ chối id đã hỏng. | Hướng gỡ khớp có điều kiện: biến phải có snapshot phù hợp, còn login cần thực hiện thật. Không chạy login/chuan-bi với credential thật. |
| Vì sao dự phòng không đáng làm | ADR :45–48 ghi nguyên văn đây là suy luận, CHƯA ĐO trên từng loại hỏng. | Khai giới hạn đúng. Không dùng fault injection ở đây để chứng minh đầy đĩa/quyền/read-only đều làm dự phòng hỏng. |
| Sáu tệp không khớp định danh ADR | Hai cây: chạy riêng regex định danh bằng `rg -c` trên từng tệp, lệnh đầy đủ và log ở bảng dưới. | Khớp số kết quả 0; thực tế stdout rỗng, rc=1. |
| Suy ra “0 cổng” theo nghĩa §20 từ regex trên | Regex khái niệm ở bảng dưới cho `launcher.py` 4 dòng. §20 :1491–1496 phân biệt “0 cổng” với “có nhắc”. | Khai rộng hơn phép đo (F2). Không coi 4 dòng nhắc là 4 cổng đọc luật. |
| §20 thêm đúng một dòng, đúng bảng/khuôn và nội dung khớp ADR | `git diff --numstat BASE HEAD`; A1 dương/âm thực sự gọi parser. Dòng :1548 có ADR/id, mô tả, Accepted, cột cổng. | Đúng khuôn, đúng 1 dòng; nội dung lặp lỗi F1/F2 nên phải sửa đồng bộ. |
| `adr-song` canh đăng ký, không kiểm quyết định chấp nhận | Đọc `packet_loop.py:1917–2009`: duyệt mọi ADR, đọc bytes để kiểm trạng thái; không kiểm hậu quả runtime hay lý do chấp nhận. | Đúng khi nói về nội dung quyết định; vẫn có đọc metadata, nên không nên viết thành tuyệt đối “không cổng nào đọc tệp ADR”. |

### Đếm đủ sáu vị trí cổng

Hai regex đã chạy riêng trên **từng tệp**, ở cả base và HEAD:

```bash
rg -c 'ADR-0061|0061-codex' <tep>
rg -c 'codex-rejected-state-khong-ghi-duoc|_danh_dau_auth_hong|KHÔNG ghi được trạng thái' <tep>
```

| Tệp | Định danh base/HEAD | Khái niệm base/HEAD |
|---|---|---|
| `ops/lease_publish.py` | 0/0, rc=1/1 | 0/0, rc=1/1 |
| `.claude/dev/packet_loop.py` | 0/0, rc=1/1 | 0/0, rc=1/1 |
| `.claude/dev/launcher.py` | 0/0, rc=1/1 | 4/4, rc=0/0 |
| `.claude/dev/gate_lifecycle.py` | 0/0, rc=1/1 | 0/0, rc=1/1 |
| `.github/workflows/ci.yml` | 0/0, rc=1/1 | 0/0, rc=1/1 |
| `.github/workflows/ops-publish-lease.yml` | 0/0, rc=1/1 | 0/0, rc=1/1 |

Các dòng khái niệm là `launcher.py:3589,3702,3895,3896`. Log: `evidence/{base,head}-gate-{0..5}.json`, `evidence/{base,head}-concept-{0..5}.json`. Regex khái niệm cũng chỉ là proxy có phạm vi đã khai; không chứng minh cưỡng chế. Không tìm thấy consumer của **quyết định chấp nhận** khi đọc các nhánh nêu trên; phần đó là đối chiếu mã, không suy riêng từ grep tên.

## Bảng lớp

| Slug lớp | Biểu hiện | Hạng cao nhất | Nguồn | Cách vá chung / phép đóng |
|---|---|---|---|---|
| `loi-ghi-khong-suy-ra-probe-lap` | ADR :15–23; mô tả §20 lặp lời khai; False bị đọc thành state chắc chắn vắng | P1 | Lượt 1, exact reviewed_sha dòng 2 | Thêm điều kiện và các nhánh 0 probe; phân biệt lời gọi helper với số HTTP request; đối chiếu matrix ba lối. |
| `grep-ten-khong-do-khai-niem` | ADR :50–64; cột cổng §20 :1548 | P2 | Lượt 1, exact reviewed_sha dòng 2 | Tách định danh, khái niệm và cơ chế consumer; dùng đúng mức proxy theo §20. |

2 lớp, 2 finding; không có lượt review trước cần đối chiếu. Mỗi lớp bao gồm mọi biểu hiện vừa tìm thấy trong hai tệp diff.

### loi-ghi-khong-suy-ra-probe-lap [P1] Lỗi ghi không bảo đảm lần sau probe lại đúng một lần

**Tệp/dòng:** `docs/adr/0061-codex-trang-thai-tu-choi-khong-ghi-duoc.md:15–23`; câu rút gọn ở `docs/PROTOCOL_DA_PHIEN.md:1548`.

**Vấn đề:** ADR biến `_danh_dau_auth_hong == False` thành lời khẳng định state chưa lưu, lần sau luôn tốn đúng 1 probe và luôn cùng lý do CHẶN. Mã có hai nhánh phản chứng: `_KhoCodex.write` `os.replace` trước `os.fsync(self.fd)` (:3388–3391), nên lỗi fsync có thể xảy ra khi state đã chứa đúng id; hoặc state không đọc được, `_dang_cho_snapshot` bắt lỗi rồi trả True (:3615–3616). Cả hai làm lần sau chặn trước probe; materializer cũng có nhánh lỗi đọc state. Lỗi ở đây là mô tả mới sai, không yêu cầu sửa runtime đã có.

**Đã thử nghiệm:** `evidence/repro_probe.py`, rc=0, cùng kết quả trên base/HEAD:

| Lỗi chèn / đối chứng | Probe hai lượt, cả ba lối | State chứa đúng id sau hai lượt |
|---|---|---|
| Lỗi trước `replace` state | [1,1] | Không |
| Lỗi `fsync` thư mục sau `replace` | [1,0] | Có |
| State không đọc được sau probe đầu | [1,0] | Không |
| Ghi thành công | [1,0] | Có |

Ở hai phản chứng, lượt đầu báo “KHÔNG ghi được … CHẶN”; lượt sau launcher trả `CHỜ snapshot Codex mới`, credential CLI rc=2 với `CHỜ snapshot mới; không lặp credential đã thất bại`; materializer trả chờ id đã thất bại hoặc `HỎNG: không đọc/ghi an toàn được credential hoặc state; không chạy child`. Xem `evidence/base-probe-repro.json` và `evidence/head-probe-repro.json`.

Fixture dùng auth INERT, probe giả, read/write sản phẩm trên dirfd riêng và chèn lỗi I/O. Factory fixture cấp dirfd trực tiếp, **không đo constructor kiểm ancestor/ACL của `_KhoCodex`**. Đây là phép đo nhánh lỗi, không thay A4 và không phải đo mạng, mất điện, đầy đĩa thật hoặc Windows.

**Vá ở đâu/cách vá:** sửa ADR và đúng dòng §20, giới hạn “probe lặp” vào state còn đọc được nhưng chưa lưu id, credential không đổi, probe vẫn bị từ chối và lỗi ghi còn tái diễn trước promote. Ghi rõ lỗi sau replace hoặc lỗi đọc có thể cho 0 probe/lý do khác. Bỏ bảo đảm tuyệt đối về mọi trạng thái I/O. Giữ quyết định chấp nhận vĩnh viễn. Cùng tiền đề “đúng 1” cũng có trong mục “Sự thật đã đo” của SPEC; nếu nghiệm thu buộc giữ tiền đề tuyệt đối ấy, cần revision spec do authority xử lý, reviewer không sửa spec đóng băng.

**Ca khóa:** hai lượt cho cả ba lối, bốn trạng huống trong bảng, đối chứng giữ auth cũ và đúng id. Script đính kèm đã chạy. **Rủi ro vá:** chỉ đổi “1” thành “tối đa 1” mà giữ “lần nào cũng … cùng lý do” vẫn còn lỗi; không sửa runtime hoặc mở #824/#826. **Độ tin:** cao.

### grep-ten-khong-do-khai-niem [P2] Đếm tên ADR không đủ cho nhãn 0 cổng theo §20

**Tệp/dòng:** `docs/adr/0061-codex-trang-thai-tu-choi-khong-ghi-duoc.md:50–64`, `docs/PROTOCOL_DA_PHIEN.md:1548`; định nghĩa cột tại §20 :1491–1496.

**Vấn đề:** `rg -c 'ADR-0061|0061-codex'` chỉ đo định danh; tại base ADR mới chưa tồn tại nên không thấy tên không chứng minh không có consumer theo khái niệm. §20 định nghĩa “0 cổng” là không tệp cổng nào nhắc **khái niệm** dù một lần. Regex khái niệm trên cho 4 dòng launcher, gồm chính tên nợ ở :3702. Nhãn đúng theo thước §20 là “có nhắc”, kèm giới hạn chưa chứng minh đọc luật. `adr-song` còn đọc mọi ADR theo cơ chế generic để kiểm metadata, không cần nhắc tên ADR-0061. Câu cuối ADR phân biệt test hành vi với cổng là đúng, nhưng chưa đủ sửa phép suy trong nhãn.

**Đã thử nghiệm:** cả hai regex, đủ sáu tệp và hai cây, kết quả bảng trên; các rc/log lưu đầy đủ. Không nói 4 dòng là 4 cổng cưỡng chế. Không yêu cầu tạo cổng mới để đọc ADR.

**Vá ở đâu/cách vá:** giữ bảng đủ sáu vị trí, tách kết quả tìm định danh (0) và tìm khái niệm (launcher 4); dùng mức “có nhắc” ở §20. Nếu kết luận chưa có cổng đọc quyết định chấp nhận, ghi đó là đối chiếu luồng mã và nêu rõ `adr-song` chỉ kiểm đăng ký/trạng thái. Nối kết luận với phạm vi đo, không gọi grep định danh là bằng chứng phủ mọi cách đọc nội dung.

**Ca khóa:** lặp hai regex trên đủ sáu vị trí; đối chiếu dòng §20 với định nghĩa cột; chạy `adr-song`/`doctrine-scan` sau sửa trên cây riêng. **Rủi ro vá:** không nâng proxy “có nhắc” thành khẳng định có cưỡng chế. **Độ tin:** cao về độ hẹp phép đo và định nghĩa §20; không khẳng định tuyệt đối không tồn tại mọi reader ngoài sáu vị trí.

## Gợi ý vá và phần chưa đo

`HINT.patch` là artifact theo yêu cầu, patch -p0 từ `cay-kho/`, chỉ sửa văn bản ADR và đúng dòng §20. Nhãn: **“chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit”**. Đã dry-run và áp thật `patch -p0 --fuzz=0` **chỉ trên bản sao reviewer** `evidence/hint-final/`, rc=0; A1 ở bản ấy vẫn 60/60 rc=0, A2 rc=0. Log `evidence/hint-validation.log` và `hint-*.json`. Không áp HINT vào `cay-kho/`; không coi gợi ý đã qua review trên SHA mới.

Chưa đo: A4 đầy đủ trong temp không có ancestor `.git`; mutation materializer/t16 ở nền neutral xanh; CI/check-run exact head A5; số request mạng thực; disk-full/ACL/read-only thật, Windows và mất điện; byte lời duyệt trong phiên người dùng. Các phần này không được ghi là pass. Quyết định không dựng dự phòng vẫn được coi là authority đầu vào; lập luận dự phòng tiếp tục mang nhãn suy luận chưa đo.
