verdict: approve
reviewed_sha: a789dc8db0785f4c3a9066288356b884aee54501
reviewed_tree: 38011d508005e9d0bef29d930edfb1cb2a3c80b8
base_sha: 9e9a74b2a396ef458d25c51a5563efafbb45ba0c
previous_reviewed_sha: d6b1e2d27cadc1d985ad2868aeae444598a6b97a
N4_windows_ci: KHÔNG ĐO ĐƯỢC

Không phát hiện P0/P1/P2 còn mở. Finding P3 `c09-thieu-chot-byte-sau-ghi` của lượt 1 **ĐÃ VÁ THẬT, đã đóng**: phép gỡ `newline=""` nay đỏ đúng chốt byte, và cả hai lần gọi helper đều được kiểm riêng. Bản vá giữ nguyên toàn bộ các chốt cũ và thứ tự ghi/kiểm. `approve` là verdict mã theo chỉ thị lượt 2; N4 là bằng chứng nghiệm thu riêng, chưa được xác minh và không được tính là pass.

Reviewer độc lập: Codex, provider `openai_codex`, model family `openai`, role `reviewer`. [run.json](runs/427d0ecb/run.json) ghi `execution_surface=codex_cli`, `transport=machine`, run ID `427d0ecb47384eee9f22aab84ff83f02`; packet không có attestation riêng cho exact serving-model/effort nên không suy từ cấu hình yêu cầu. Không tái sử dụng context executor; không gọi reviewer phụ. Không dùng mạng, không đăng GitHub (`github_submitter_identity: null`), không sửa `cay-kho/`, không tạo receipt/merge/land/deploy.

## ĐỐI CHIẾU LƯỢT TRƯỚC

### c09-thieu-chot-byte-sau-ghi  [P3] — ĐÃ VÁ THẬT, ĐÃ ĐÓNG

Vị trí hiện tại: `ops/land_evidence_nguon_test.py:248–255`, helper `ghi()` trong `c09_l5_mien_tru_theo_bam`. Lượt 1 có hai write riêng tại L248/L251; head mới gom chúng vào **một** write tại L249 và kiểm `read_bytes() == nd.encode()` tại L250 ngay sau ghi.

Lệnh đã chạy:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 review-evidence-r2/initial.py
PYTHONDONTWRITEBYTECODE=1 python3 review-evidence-r2/hunts.py
```

`initial.py` dựng bản sao bằng `mktemp -d` + `git archive` từ exact OID. Nó gỡ duy nhất keyword ở write trong helper mới, rồi chạy dưới `PYTHONPATH=<đường dẫn tuyệt đối tới sim>`. Output thật của ca:

```text
head nguyên vẹn, c09 sim: rc=0, stdout='\n', stderr=''
head gỡ newline trong ghi(), c09 sim: rc=3
DO:c09_l5_mien_tru_theo_bam:byte ghi phải đúng nguyên văn (LF): "x: 'measured — khong nguon'\n "
```

Đây là `TinHieuChotCa` tại chốt byte mới; không phải chốt “băm khớp”, chốt rc/hash sau ghi hoặc lỗi vô can. Đối chứng trên **revision lượt 1**: gỡ từng newline ở hai write c09 cũ, cả hai đều `rc=0`, `stdout='\n'` dưới cùng sim. Vì vậy đã tái lập chính lỗ hổng độ nhạy cũ và chứng minh nó được đóng ở head mới.

Để lần ghi đầu không che lần ghi sau, probe bổ sung vẫn gỡ keyword chung, nhưng phục hồi `newline=""` riêng cho lần gọi helper đầu tại biên I/O. Trace cho byte ba lần ghi là 30, 31, **26** (lần cuối đáng lẽ 25), và ca trả:

```text
rc=3
DO:c09_l5_mien_tru_theo_bam:byte ghi phải đúng nguyên văn (LF): "x: 'measured — a.json'\n"
```

Chốt rc/hash cũ của nhánh thứ nhất đã qua; lần ghi thứ hai đỏ tại chính chốt byte của nó. Probe process trả `rc=0` vì xác nhận được kết quả ca `rc=3` mong đợi; hai mã này được ghi riêng trong JSON.

Bằng chứng: [c09-remove-helper-newline.log](review-evidence-r2/c09-remove-helper-newline.log), [hai](review-evidence-r2/c09-prev-remove-write1.log) [đối chứng cũ](review-evidence-r2/c09-prev-remove-write2.log), [trace lần ghi thứ hai](review-evidence-r2/hunt-second-write-byte-check.log).

Không còn đề nghị sửa cho finding này. Giữ chốt byte tại c09, nơi đặc tả yêu cầu exact byte; không cần mở ràng buộc này sang toàn bộ YAML hay mã nguồn tạm.

### Bản vá P3 có nới hoặc đổi thứ tự chốt cũ không?

**Không.** `initial.py` parse AST hai revision, inline từng lời gọi `ghi(nd)` thành đúng write đầu trong helper, bỏ định nghĩa helper và chỉ chốt byte mới, rồi so **toàn module** không tính vị trí. Output thật:

```text
whole_module_equal_after_inline_and_remove_new_byte_check: true
old_c09_conditions_in_order:
  rc == 0 and '1/1 miễn trừ' in ra
  rc == 1 and 'MẤT MIỄN TRỪ' in ra and ('0/1 miễn trừ' in ra)
  rc == 0 and '0/1 miễn trừ' in ra
newline_sites: [74, 198, 249]
```

Do so cả module, phép đo cũng kiểm nội dung hai lần ghi, các `kiem(m, goc)`, băm kỳ vọng, đăng ký ca và danh sách đột biến không bị sửa. Trace thực thi của head xác nhận:

```text
kiểm băm khớp rc=0 → chốt 1/1
ghi hs + " " → đọc byte → chốt byte → kiểm rc=1 → chốt MẤT MIỄN TRỪ + 0/1
ghi YAML có a.json → đọc byte → chốt byte → kiểm rc=0 → chốt 0/1
```

Đột biến checker thật `L5_bo_so_bam` vẫn được xếp `GIET`, ca gốc `rc=0`, ca đột biến `rc=3`, output bắt đầu:

```text
DO:c09_l5_mien_tru_theo_bam:lệch một byte ⇒ kiểm đủ luật: rc=0 MIỄN TRỪ ...
```

Nó chết ở **chốt nghiệp vụ cũ**, không phải chốt byte mới. [AST audit](review-evidence-r2/ast-audit.json), [trace c09](review-evidence-r2/hunt-trace.log), [output L5 đầy đủ](review-evidence-r2/l5-real-mutant.log).

## BẢNG ĐO

Môi trường đã đo: Linux, Python **3.13.16**, PyYAML **6.0.3**, Ruff **0.17.1**. Tất cả tiến trình Python dùng `PYTHONDONTWRITEBYTECODE=1`; child chạy thêm `-B`. Baseline thường gỡ `PYTHONPATH`; sim dùng đường dẫn tuyệt đối tới `sim`. Gỡ `LAND_EVIDENCE_NGUON_MA` khỏi môi trường cha; mutation runner tự đặt nó cho checker scratch đúng như thiết kế. Mọi thử nghiệm đột biến chỉ sửa cây archive ngoài repository review.

Lệnh dựng **cả base và head trong cùng một invocation**, chạy ba baseline toàn suite và từng phép gỡ keyword:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 review-evidence-r2/matrix.py
```

Script gọi `git -C cay-kho archive <full OID>` cho base/head; không dùng cây đã đột biến cho baseline. Hai baseline head dùng cùng cây chỉ đọc; các fixture/checker đột biến bên trong suite dùng TemporaryDirectory riêng. Ba worker process đo đồng thời, thời gian là wall time từng lượt, không phải benchmark hiệu năng.

| cây / chế độ | CA | DOT BIEN | tự kiểm phân hạng | TONG | rc | giây |
|---|---|---|---|---|---|---|
| head thường | 16/16 | 64/64 | DAT (2) | DAT | 0 | 72.38 |
| head sim CRLF | 16/16 | 64/64 | DAT (2) | DAT | 0 | 73.43 |
| base sim CRLF | 15/16 | 63/64 | DAT (2) | DO | 1 | 74.65 |

Output thật cả hai lượt head:

```text
CA: 16/16 dat
DOT BIEN: 64/64 bi giet dung ly do
TU KIEM PHAN HANG: DAT (2 dot bien)
TONG: DAT
```

Base sim đỏ đúng c09 ở chốt băm khớp, không chỉ có rc khác 0:

```text
[DO:c09_l5_mien_tru_theo_bam:băm khớp ⇒ miễn trừ có ghi nhận: rc=1 ...]
CA: 15/16 dat
[DOT BIEN KHONG BI GIET DUNG] L5_bo_so_bam: HONG ca đích không xanh trên bản gốc (rc=3): ...
DOT BIEN: 63/64 bi giet dung ly do
TU KIEM PHAN HANG: DAT (2 dot bien)
TONG: DO
```

Dấu `...` ở trích đoạn chỉ rút gọn phần checker; log lưu toàn bộ output: [head thường](review-evidence-r2/head-normal.log), [head sim](review-evidence-r2/head-sim.log), [base sim](review-evidence-r2/base-sim.log). [matrix.json](review-evidence-r2/matrix.json) và từng JSON chứa command/cwd/env/rc/thời lượng/stderr thật; [matrix-paths.json](review-evidence-r2/matrix-paths.json) giữ đường dẫn scratch.

| tiêu chí | kết quả đo |
|---|---|
| N1: byte fixture cần LF | `cay()` giữ newline rỗng; hai lần ghi c09 dùng chung helper có newline rỗng và chốt byte, trace 30→31→25 byte, không CRLF |
| N2: Linux | head thường 16/16, 64/64, TONG DAT, rc=0 |
| N3: cùng lệnh, sim | head DAT, base DO đúng c09 như trên |
| N4: Windows check run trên exact head | **KHÔNG ĐO ĐƯỢC**, tách riêng ở cuối |
| N5: Ruff F delta | base/head cùng `All checks passed!`, rc=0; delta=0 |
| write set / diff | đúng một tệp `ops/land_evidence_nguon_test.py`, numstat `8 4`; diff và numstat khớp byte với packet |
| `git diff --check base head` | rc=0, stdout/stderr rỗng |
| SPEC/LEASE | SHA256 `48731f52ab75fd541b416c9aebc32231a05782d7754dec86b606aec580be48a8`, đúng giá trị đóng băng |

Lệnh Ruff/diff đã chạy trong bản sao exact base/head:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 review-evidence-r2/checks.py
# Bên trong, ở từng archive:
python3 -B -m ruff check --select F ops/land_evidence_nguon_test.py
# Read-only trên kho review:
git -C cay-kho diff --check 9e9a74b2a396ef458d25c51a5563efafbb45ba0c a789dc8db0785f4c3a9066288356b884aee54501
```

[ruff-base.log](review-evidence-r2/ruff-base.log), [ruff-head.log](review-evidence-r2/ruff-head.log), [checks.json](review-evidence-r2/checks.json). CI dùng Python 3.12 và Ruff 0.15.15; các số đo chính trên không được gọi là tái lập đầy đủ runtime CI.

### Răng của MỌI `newline=""` trên head mới

Inventory AST có **8 lời gọi write_text thật**, không có writer `open`/`write_bytes`; chính xác **3** keyword newline rỗng ở **L74/L198/L249**. Hai write c09 cũ đã được gộp, nên không tiếp tục liệt kê L248/L251 như hai site trên head mới. [io-inventory.log](review-evidence-r2/io-inventory.log).

Mỗi phép gỡ bắt đầu từ archive head sạch riêng, chỉ bỏ keyword ở một dòng rồi chạy **toàn suite dưới sim** bằng `matrix.py`:

| chỉ gỡ tại | sống/chết | CA | DOT BIEN | TONG / rc | giây |
|---|---|---|---|---|---|---|
| L74, `cay()` | CHẾT | 15/16 | 63/64 | DO / 1 | 74.36 |
| L198, `c14` | SỐNG | 16/16 | 64/64 | DAT / 0 | 73.66 |
| L249, `c09 → ghi()` | CHẾT | 15/16 | 63/64 | DO / 1 | 72.88 |

Tự kiểm phân hạng cả ba lượt đều `DAT (2 dot bien)`.

- **L74 chết** ở chốt băm khớp c09: fixture ban đầu bị CRLF, `rc=1`, `0/1 miễn trừ`. Đây là regression mà packet ban đầu chữa.
- **L249 chết** ở chốt byte mới: `DO:c09_l5_mien_tru_theo_bam:byte ghi phải đúng nguyên văn (LF): "x: 'measured — khong nguon'\n "`. Suite rc=1; chạy riêng ca rc=3. `L5_bo_so_bam` báo `HONG ca đích không xanh trên bản gốc` trong cây gỡ keyword vì chính test nền của cây đột biến đã đỏ; không coi đó là một kill checker đúng lý do. Trên head nguyên vẹn, L5 vẫn `GIET` đúng chốt cũ như đã đo riêng.
- **L198 vẫn sống, đúng và chấp nhận được** cho mục tiêu ca c14. Trace bổ sung đã đi qua site, không phải nhánh không chạy: YAML `plat-y` **43→44 byte, CRLF 0→1**; hai JSON giữ **69/69 byte, 0 CRLF**. Cả hai c14 `rc=0`; checker đều `rc=2` với output bằng nhau, báo `readback-pr-*.json cho 2 merged_at khác nhau`. YAML `plat-y` không được miễn trừ/băm tại đây; ca đo mâu thuẫn timestamp sau parse, không đo representation LF. Keyword giúp fixture nhất quán nhưng không có răng ở mục tiêu hiện tại; không tuyên bố nó được suite bảo vệ. Không cần sinh thêm chốt byte để phục vụ mục tiêu đó.

Lệnh trace c14 và kiểm mutation nghiệp vụ:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 review-evidence-r2/contracts.py
```

[L74](review-evidence-r2/remove-newline-L74.log), [L198](review-evidence-r2/remove-newline-L198.log), [L249](review-evidence-r2/remove-newline-L249.log), [c14 head](review-evidence-r2/c14-head.log), [c14 gỡ L198](review-evidence-r2/c14-remove-L198.log).

Các writer còn lại không thuộc hợp đồng exact byte LF ở đây: L127/L152 không có xuống dòng; L153 là log so token số; L462/L463 là source checker tạm được Python import. So AST với lượt 1 chứng minh chúng không đổi trong commit P3. Không suy từ việc chúng được đọc bằng byte rằng mọi newline đều được so nguyên văn.

## BẢNG SĂN

Bốn hướng dưới đây nhắm vào helper/chốt mới của commit sửa P3, ngoài ma trận toàn suite và phép gỡ keyword bắt buộc. Lệnh chung đã thực thi:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 review-evidence-r2/hunts.py
```

`hunts.py` dựng archive head, gọi `probe.py <scratch> <mode>` trong process con dưới sim, lưu stdout/stderr/rc đầy đủ. Mỗi hướng có giả thuyết, lệnh thực tế, output và kết luận riêng:

| hướng / giả thuyết | lệnh hoặc mode đã chạy | output thật | kết luận |
|---|---|---|---|
| 1. Closure `ghi()` dùng sai `goc`/`TEN`, đọc tệp khác hoặc gốc cũ | `probe.py <head> trace` và `alternate`; lần sau đổi `TEN` thành `pr9342-thử-có-dấu-land-evidence.yaml` cùng `PROV` tương ứng | cả hai c09 rc=0; mỗi lượt có 3 write trên đúng 1 path trong TemporaryDirectory của lượt đó; các read dùng cùng path; byte 30/31/25, không CRLF; checker rc=[0,1,0] | **KHÔNG PHẢI LỖI** trên các tên/gốc đã đo; trace xác nhận closure dùng đúng fixture, không chạm cây thật |
| 2. `nd.encode()` theo locale nên khác `encoding="utf-8"` khi Windows không bật UTF8 | `probe.py <head> locale` với `LC_ALL=C PYTHONUTF8=0 PYTHONCOERCECLOCALE=0 PYTHONIOENCODING=cp1252` | locale=`ANSI_X3.4-1968`, filesystem=`ascii`, default_encoding=`utf-8`; c09 rc=0; cả 3 chuỗi `.encode()==.encode('utf-8')`, disk_equals_utf8=True | **KHÔNG PHẢI LỖI** về default của str.encode: mặc định là UTF8, không lấy codec từ locale. Đã đo nội dung có dấu em dash; probe Linux không xác minh runtime Windows |
| 3. Chốt byte mới đỏ giả vì tầng text I/O dù có newline rỗng | `probe.py <head> textio`; thêm đối chứng thật bằng `io.TextIOWrapper(BytesIO(), encoding='utf-8', newline=...)` với chính hai chuỗi helper | newline rỗng: (31 byte,0 CRLF,True), (25,0,True); ép newline CRLF: (32,1,False), (26,1,False); c09 sim rc=0 | **KHÔNG PHẢI LỖI** trong semantics text I/O đã đo: newline rỗng giữ nguyên byte; codec UTF8 không tự thêm BOM/CR. **Windows native: KHÔNG ĐO ĐƯỢC**; không biến mô hình này thành bằng chứng N4 |
| 4. Helper chung chỉ bảo vệ lần ghi đầu, lần sau bị bỏ qua hoặc dùng nhầm `nd` | gỡ newline chung, chạy `probe.py <mutated-head> restore-first`, chỉ sửa tham số I/O của lần gọi helper đầu | write thứ nhất của helper 31 byte, chốt byte=True, checker rc=1; write sau 26 thay vì25 byte, chốt byte=False; ca rc=3, marker nhắc đúng `a.json` | **KHÔNG PHẢI LỖI**: lần gọi sau có chốt độc lập dùng đúng nội dung. Phép đo chỉ mở đường tới nhánh sau, không tắt chốt nào |

Log: [closure trace](review-evidence-r2/hunt-trace.log), [tên thay thế](review-evidence-r2/hunt-alternate.log), [locale ASCII](review-evidence-r2/hunt-locale-ascii.log), [TextIOWrapper](review-evidence-r2/hunt-textio.log), [nhánh ghi sau](review-evidence-r2/hunt-second-write-byte-check.log). JSON dùng escape Unicode để probe locale ASCII vẫn ghi được; số đo byte lấy từ `read_bytes()`, không từ biểu diễn JSON.

Kiểm riêng khả năng chốt mới che chốt cũ: `contracts.py` thực thi `L5_bo_so_bam` trên head sim; ca gốc rc=0, mutant rc=3, phân hạng GIET ở thông báo “lệch một byte ⇒ kiểm đủ luật”. Không có finding mới từ các hướng săn này.

## N4 — WINDOWS CI, TÁCH KHỎI VERDICT MÃ

**KHÔNG ĐO ĐƯỢC.** Không gọi mạng theo chỉ thị review; packet offline không cung cấp check run/log cho `workflow_dispatch` của `.github/workflows/ci.yml` trên exact SHA `a789dc8db0785f4c3a9066288356b884aee54501`. Host đo là Linux; không có `wine`, `wine64`, `python.exe`, `pwsh` trong PATH. [runtime.json](review-evidence-r2/runtime.json).

Sim chỉ mô phỏng `Path.write_text` với `newline=None`, kể cả subprocess. Nó không chạy Windows filesystem/runtime hay toàn job CI. Kết quả Linux, locale và TextIOWrapper không chứng minh job Windows đã xanh hoặc còn đỏ.

**N4 do executor đo riêng**: đọc check run/log của đúng workflow_dispatch, đúng head, xác minh job `gate-registry (windows-latest)` thực sự chạy và success; ghi run/check URL + head SHA + kết luận cạnh verdict mã này. Không `blocked` chỉ vì chưa đo được N4. Verdict này không cấp quyền merge/land/deploy.

## TRẠNG THÁI BẰNG CHỨNG

- **passed:** N1/N2/N3/N5 trong phạm vi đo local; AST không nới chốt; đóng P3 ở cả hai lần gọi; ba phép gỡ newline đã hoàn tất và được giải thích; bốn hướng săn; diff/write set/spec hash.
- **failed đúng dự kiến:** base sim, head gỡ L74, head gỡ L249; ca gỡ helper đơn lẻ và nhánh ghi sau rc=3 tại đúng chốt byte. Đây là phản chứng, không phải test bị bỏ qua để approve.
- **not_run / KHÔNG ĐO ĐƯỢC:** N4 và native Windows. Không có P0/P1/P2/P3 mới còn mở được phát hiện. L198 sống đã được đo và chấp nhận theo mục tiêu của c14.
- **Hạn chế harness đã sửa:** probe phụ L5 lần đầu tìm marker trong chuỗi summary bị suite cắt còn 200 ký tự nên assertion của reviewer thất bại; không phải lỗi mã review. Đã thu output đầy đủ từ `chay_con`, đo lại thành công; giữ [log lần đầu](review-evidence-r2/l5-real-mutant-harness-first-attempt.log) và [log sau sửa](review-evidence-r2/l5-real-mutant.log). Các lượt toàn suite không bị sửa hoặc chạy lại vì việc này.

`VERDICT.md` được tạo `pending` ngay sau khi đọc toàn bộ prompt và cập nhật tăng dần trong quá trình đo; [progress.md](review-evidence-r2/progress.md) giữ các cập nhật trước khi biên tập bản cuối. Script và log/JSON nguyên văn nằm trong [review-evidence-r2](review-evidence-r2/).

Kiểm cuối: `git -C cay-kho status --porcelain` output rỗng; HEAD/tree vẫn đúng các OID ở đầu. Mọi đột biến ở `/tmp/wp871-r2-*`, không sửa cây review, không phát sinh bytecode ở đó, không dùng mạng và không đăng GitHub.
