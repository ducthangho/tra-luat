verdict: blocked
reviewed_sha: d6b1e2d27cadc1d985ad2868aeae444598a6b97a
reviewed_tree: 2011f62e0615ef098cdeabd203990ac876891dc7
base_sha: 9e9a74b2a396ef458d25c51a5563efafbb45ba0c

Không tìm thấy P0/P1/P2 bằng các phép đo dưới đây. Bản vá tái lập và chữa đúng lỗi c09 trong mô phỏng được giao. Có một ghi chú P3 về độ nhạy của test. **Chặn nghiệm thu ở N4**: chưa có check run/log chứng minh `workflow_dispatch` của `ci.yml` trên đúng head này có job `gate-registry (windows-latest)` xanh. Gói offline không chứa bằng chứng đó; chỉ thị cấm mạng nên không thể đọc bổ sung. Đây là thiếu bằng chứng nghiệm thu bắt buộc, không phải kết luận rằng Windows vẫn đỏ. Chưa đủ cơ sở ghi `approve` cho toàn bộ đặc tả.

Reviewer: Codex, provider `openai_codex`, model family `openai`, role `reviewer`, phiên độc lập với executor. `runs/d7f23a04/run.json` ghi `execution_surface=codex_cli`, `transport=machine`, run ID `d7f23a040cae4fa6b514b49dd6b2e2d0`; exact serving-model/effort không có attestation riêng trong packet. Không đăng GitHub (`github_submitter_identity: null`), không sửa `cay-kho/`, không merge/land/deploy. Không tự tạo receipt `cross_approved`.

## BẢNG ĐO

Các lượt chính: Linux, Python 3.13.16, PyYAML 6.0.3. Tất cả có `PYTHONDONTWRITEBYTECODE=1`; thường gỡ `PYTHONPATH`, CRLF đặt đường dẫn tuyệt đối tới `sim`. Gỡ `LAND_EVIDENCE_NGUON_MA` khỏi môi trường cha để không đọc nhầm checker ngoài cây.

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| base thường | 16/16 · 64/64 · DAT | CA: 16/16 dat · DOT BIEN: 64/64 bi giet dung ly do · TONG: DAT; rc=0; 120.29 s | có |
| base CRLF | 15/16 · 63/64 · DO | CA: 15/16 dat · DOT BIEN: 63/64 bi giet dung ly do · TONG: DO; rc=1; 120.53 s | có |
| head thường | 16/16 · 64/64 · DAT | CA: 16/16 dat · DOT BIEN: 64/64 bi giet dung ly do · TONG: DAT; rc=0; 117.0 s | có |
| head CRLF | 16/16 · 64/64 · DAT | CA: 16/16 dat · DOT BIEN: 64/64 bi giet dung ly do · TONG: DAT; rc=0; 120.14 s | có |
| N1: nơi cần byte LF cố định | cay + hai c09 + nơi so/băm byte khác | đáp ứng; kiểm đủ 9 chỗ ghi và 3 chỗ đọc checker, bảng chi tiết dưới | có trong phạm vi so byte/LF |
| N2 | head Linux DAT | 16/16 · 64/64; rc=0 | có |
| N3: dựng hai vế cùng một lệnh | head DAT; base DO ở c09 | `run_matrix.py` dựng cả hai từ exact OID bằng `git archive` trong cùng invocation, chạy đủ bốn tổ hợp | có |
| N4 | Windows workflow_dispatch trên exact head, job xanh từ check run/log | KHÔNG ĐO ĐƯỢC; không có CI artifact/check object offline, không gọi mạng | chưa xác minh |
| N5 | Ruff F delta=0 | Ruff 0.17.1: base/head cùng rc=0, `All checks passed!`; delta 0 | có |
| write set | chỉ ops/land_evidence_nguon_test.py | git diff numstat = `5 4 ops/land_evidence_nguon_test.py`, khớp byte numstat.txt; diff --check rc=0 | có |
| Python cùng minor với CI (bổ sung) | không khai | Python 3.12.3, CRLF: 16/16 · 64/64 · DAT; rc=0; 73.21 s | — |

Lệnh chính, **cả hai vế được dựng trong cùng một lệnh**, không chạy suite trên worktree review:

```bash
PYTHONDONTWRITEBYTECODE=1 python3 review-evidence/run_matrix.py
```

Script tạo hai cây bằng `git -C cay-kho archive <full OID>` và chạy `python3 ops/land_evidence_nguon_test.py` trong từng cây, hai môi trường. Mã lệnh/môi trường/cwd/rc/thời lượng và output nguyên văn ở các file `.json`/`.log` tương ứng trong [review-evidence](review-evidence/). Hai lượt chạy cùng một revision chỉ đọc cây đó; mọi fixture và checker đột biến dùng TemporaryDirectory riêng.

Base CRLF đo được đúng hai dấu hiệu, không chỉ rc:

```text
[DO:c09_l5_mien_tru_theo_bam:băm khớp ⇒ miễn trừ có ghi nhận: rc=1 ...]
CA: 15/16 dat
[DOT BIEN KHONG BI GIET DUNG] L5_bo_so_bam: HONG ca đích không xanh trên bản gốc (rc=3): ...
DOT BIEN: 63/64 bi giet dung ly do
TU KIEM PHAN HANG: DAT (2 dot bien)
TONG: DO
```

Ba lượt còn lại đều in:

```text
CA: 16/16 dat
DOT BIEN: 64/64 bi giet dung ly do
TU KIEM PHAN HANG: DAT (2 dot bien)
TONG: DAT
```

Xem [base-CRLF.log](review-evidence/base-CRLF.log), [base-normal.log](review-evidence/base-normal.log), [head-CRLF.log](review-evidence/head-CRLF.log), [head-normal.log](review-evidence/head-normal.log). Output có dấu `...` ở trích đoạn trên được giữ đầy đủ trong log.

## N1 — KIỂM ĐỦ MỌI CHỖ GHI VÀ ĐỌC

Dùng AST để tránh đếm chuỗi mã đột biến là lời gọi thật; đối chiếu thêm `rg`. Test có **9 write_text, 0 write_bytes, 0 open**; checker có **0 lời gọi ghi**. Wrapper quan sát byte sau mỗi write, gọi đúng hàm write gốc hoặc mô phỏng; không sửa checker. Chạy c03/c05/c14/c09 và đột biến tự kiểm vô hại có sẵn để đi qua cả 9 chỗ ghi.

```bash
PYTHONDONTWRITEBYTECODE=1 python3 review-evidence/audit_static.py
PYTHONDONTWRITEBYTECODE=1 python3 review-evidence/run_io.py
```

Mọi dòng sau thuộc `ops/land_evidence_nguon_test.py` ở head:

| dòng / chỗ ghi | nội dung có LF? | byte được so/băm thế nào? | đo thường → CRLF, kết luận |
|---|---|---|---|
| 74, `cay`, `nd`, newline="" | tùy fixture; YAML/LOG có, JSON ở các ca đo thường không | hồ sơ đọc bằng read_bytes, L5 SHA256; c09 so với `hs.encode()`; provenance L2 đọc byte rồi so token số, L3 parse JSON | mọi nội dung giữ nguyên byte. c09 ban đầu 30 → 30 byte, 0 CRLF; đây là chốt cần thiết cho băm LF |
| 127, c03, `"{}"`, không newline | không | checker chỉ phân giải vị trí nguồn ngoài gốc, không đọc/băm nội dung này | 2 → 2 byte, 0 CRLF; không phụ thuộc EOL |
| 152, c05, `"1/1"`, không newline | không | L2 read_bytes/decode rồi regex so token số | 3 → 3 byte, 0 CRLF; không phụ thuộc EOL |
| 153, c05, `LOG`, không newline | có, 2 LF | có đọc bằng read_bytes và dùng nội dung gián tiếp qua checker, nhưng chỉ so các token `195/195`, `hong 0`; không băm/so toàn bộ byte hoặc dấu xuống dòng; ở nền thấp, ca gốc còn ưu tiên tệp `1/1` ở nền cao | **64 → 66 byte, 0 → 2 CRLF**, c05 vẫn rc=0. Byte còn phụ thuộc nền, kết quả kiểm token không phụ thuộc EOL |
| 198, c14, `nd`, newline="" | YAML có 1 LF; hai JSON không LF | YAML parse bằng byte; tên plat-y không trong MIEN_TRU; readback read_text rồi JSON; so merged_at | YAML 43 → 43 byte, JSON 69 → 69; không băm/so LF ở ca này |
| 248, c09, `hs + " "`, newline="" | có 1 LF | có băm bằng checker, nhưng chốt chỉ đòi **khác** hash gốc và rc=1, không xác nhận đúng một byte thêm | 31 → 31 byte, 0 CRLF. Khi gỡ newline, 32 byte và vẫn DAT; thiếu chốt kiểm chính xác nội dung ghi, xem P3 |
| 251, c09, YAML có nguồn, newline="" | có 1 LF | có băm bằng checker, nhưng chỉ đòi **khác** hash gốc và rc=0 | 25 → 25 byte, 0 CRLF. Khi gỡ newline, 26 byte và vẫn DAT; thiếu chốt kiểm LF chính xác, xem P3 |
| 459, `ban_goc.write_text(goc)`, không newline | có 339 LF | Python import/compile mã nguồn, không hash/so raw byte của tệp mới ghi. Nguồn trước khi thay đột biến được read_text rồi `count(cu)` | 21.151 → 21.490 byte, 339 CRLF. Python chuẩn hóa EOL khi đọc source; compile LF/CRLF cho code object bằng nhau |
| 460, `ban_db.write_text(goc.replace(...))`, không newline | có; đột biến comment tự kiểm giữ 339 LF | import mã đã thay, không hash/so byte tệp mới ghi | 21.161 → 21.500 byte cho đột biến comment đã đo; phân hạng SONG_SOT cả hai. Số LF có thể khác với đột biến khác |

**Kết luận N1:** bốn chỗ đã sửa giữ byte LF như yêu cầu; không còn nơi so toàn bộ byte/LF hay băm fixture mà thiếu newline="". Ba chỗ 153/459/460 vẫn đổi byte theo nền, nên không tuyên bố mọi tệp tạm đều giống byte trên mọi nền. L153 so token nội dung sau decode chứ không so byte LF; 459/460 đo hành vi mã nguồn. Đọc byte không tự đồng nghĩa với so toàn bộ byte: đã phân biệt hai việc này và đo đầu ra thay vì suy rằng mọi `read_bytes` đều nhạy EOL.

Phía đọc `ops/land_evidence_nguon.py`:

| dòng | API | hệ quả và phép đo |
|---|---|---|
| 307 | `tep.read_bytes()` | băm SHA256 chính byte đĩa ở 314; đưa **cùng byte đó** cho luật/YAML, không bị universal-newline che lệch |
| 256 | `p.read_bytes().decode("utf-8", "replace")` | giữ CRLF trong chuỗi L2, regex số của c05 vẫn cho cùng kết quả |
| 172 | `t.read_text(encoding="utf-8")` | universal-newline chuẩn hóa CRLF→LF **trên Linux lẫn Windows**; JSON sau đó được parse, không băm raw byte |

Test đọc source ở 454 cũng dùng `read_text(encoding="utf-8")`, do đó tìm anchor trên LF; tệp checker mới ghi CRLF được Python import với cùng ngữ nghĩa. [static-audit.log](review-evidence/static-audit.log), [io-summary.log](review-evidence/io-summary.log) và các `*-io.json` giữ trace từng write/read.

## RĂNG CỦA BẢN VÁ — BỐN ĐỘT BIẾN RIÊNG

```bash
PYTHONDONTWRITEBYTECODE=1 python3 review-evidence/run_mutations.py
```

Mỗi cây riêng bắt đầu từ head; chỉ bỏ keyword newline ở đúng **một** dòng, chạy toàn suite với PYTHONPATH tuyệt đối tới sim và PYTHONDONTWRITEBYTECODE=1.

| chỉ gỡ ở dòng | CA | DOT BIEN | tự kiểm | TONG / rc / giây | giải thích |
|---|---|---|---|---|---|
| 74 | 15/16 | 63/64 | DAT (2) | DO / 1 / 107.56 | cần cho lỗi đã khai; c09 đỏ và L5_bo_so_bam báo ca gốc không xanh |
| 198 | 16/16 | 64/64 | DAT (2) | DAT / 0 / 106.61 | không cần để ca c14 hiện tại giữ kết quả; YAML/JSON cho cùng dữ liệu, không có phép so LF |
| 248 | 16/16 | 64/64 | DAT (2) | DAT / 0 / 107.07 | cần theo N1 c09 để giữ đúng byte; ca chỉ kiểm khác hash, chưa đo đúng một byte thêm |
| 251 | 16/16 | 64/64 | DAT (2) | DAT / 0 / 106.99 | cần theo N1 c09 để giữ LF; ca chỉ kiểm khác hash + luật, chưa đo byte ghi |

Trace xác nhận các đột biến sống sót **có thực sự đổi byte**: L198 YAML 43→44 byte; L248 31→32; L251 25→26, mỗi tệp thêm 1 CR. Không gọi chúng “được suite bảo vệ”. L198 là việc giữ fixture nhất quán, không cần cho phép so hiện tại; hai dòng c09 là yêu cầu byte rõ trong spec nhưng thiếu test chống tái phạm. Log đầy đủ: `review-evidence/remove-newline-L{74,198,248,251}.log`.

## MÔ PHỎNG — PHẦN ĐO ĐƯỢC VÀ GIỚI HẠN

```bash
PYTHONDONTWRITEBYTECODE=1 python3 review-evidence/probe_portability.py
PYTHONDONTWRITEBYTECODE=1 python3 review-evidence/probe_registry_crlf.py
```

- `open(..., "w")`/file text I/O khác: sim không vá. AST xác nhận hai tệp mục tiêu không có `open` hoặc writer khác ngoài 9 Path.write_text đã kiểm. Không có đường ghi còn sót trong hai tệp để quy một lỗi Windows cho open.
- `read_text`: sim không vá, nhưng universal-newline có sẵn cả trên Linux. Byte `b'a\r\nb\rc\n'` đọc thô giữ nguyên, read_text cho `'a\nb\nc\n'`. Không được suy băm checker đã chuẩn hóa: chỗ L5 dùng read_bytes.
- `subprocess text=True`: sim không đổi stdout của tiến trình con sang EOL Windows. Đã cho child ghi trực tiếp UTF8 `ĐẠT\r\n`: capture binary giữ CRLF, capture text cho `'ĐẠT\n'`, cả hai rc=0. Còn đường con `chay_con` của mutation runner nhận binary rồi decode UTF8; phân hạng tìm marker, không so newline nguyên văn.
- Đo thêm **consumer registry thật**, không chỉ regex: `_chay_co_lap` ở `.claude/dev/ci_dang_ky_test.py:990` dùng `Popen(text=True, encoding="utf-8")`. Child phát 4 CRLF theo đúng output head; consumer nhận 0 CRLF/4 LF, bằng output head thực, rc=0, infrastructure_error=null, được nhận ở cả selector Linux và Windows. Bỏ sót mô phỏng stdout CRLF chưa tạo lỗi trên đường này đã đo.
- Encoding/locale: gate-registry đặt `PYTHONUTF8="1"`, `PYTHONIOENCODING=utf-8`; test và checker reconfigure stdout/stderr sang UTF8. Đã kiểm cấu hình và probe UTF8; không đánh đồng probe Linux với xác minh locale Windows thật.
- Git checkout/autocrlf không được sim vá. Dùng repository/index scratch và object store đọc chung, `checkout-index` 1.203 tệp gồm hai Python, policy và toàn `ops/land`: cả `core.autocrlf=false` lẫn `true`, `core.eol=lf`, đều **0 byte khác** so git-archive head. `.gitattributes`: text=auto/eol=lf cho các tệp mục tiêu; workflow còn ghim autocrlf=false/eol=lf trước checkout. Không đo bằng cách đổi config/worktree nguồn.
- Source đột biến: compile LF 21.151 byte và CRLF 21.490 byte tạo code object bằng nhau; trace cũng thấy self-check comment SONG_SOT ở cả hai chế độ.
- **Windows thật, Python/Win32 Path, filesystem, runtime/job đầy đủ: KHÔNG ĐO ĐƯỢC.** Host `os.name=posix`; `wine`, `wine64`, `pwsh`, `python.exe` đều không có. Gói không có check run/log N4 và chỉ thị cấm mạng. Không có phép đo nào ở đây chứng minh toàn job Windows xanh hoặc còn đỏ.

Python 3.12 bổ sung dùng PyYAML 6.0.1 do bản cài local; CI ghim 6.0.3. Bốn lượt chính đã dùng PyYAML 6.0.3 nhưng Python 3.13.16. Không gọi hai tập này là kiểm chứng đầy đủ đúng runtime Windows CI. Xem [portability.log](review-evidence/portability.log), [registry-crlf.log](review-evidence/registry-crlf.log).

## BẢNG SĂN

Sáu hướng sau bổ sung cho ma trận, inventory I/O, bốn phép gỡ newline và khảo sát mô phỏng bắt buộc. Không soạn tải trọng nhạy cảm.

HƯỚNG 1: Hợp đồng output có thực sự vào CI, có nhận xanh giả không?

- giả thuyết: suite chỉ xanh khi chạy tay, hoặc registry nhận thiếu mutation/thiếu tự kiểm.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review-evidence/hunt_extra.py` (phần registry-output). Import chính consumer ở head; đưa output thật head/base và các biến thể đổi bộ đếm/dòng kết luận qua `mau_theo_nen` + `bang_chung_xanh`.
- output thật: `registered=True; quarantined=False`; cả hai selector Windows=False/True: head actual accepted=True, base CRLF actual=False; missing final=False, false final=False, cases 15/16=False, mutants 63/64=False, zero mutants=False, selfcheck DO=False.
- kết luận: **KHÔNG PHẢI LỖI** trong các trường hợp đã đo. Selector Windows được gọi trực tiếp, không giả làm native Windows.

HƯỚNG 2: Đường dẫn có dấu/khoảng trắng làm gãy CLI hoặc fixture?

- giả thuyết: thêm newline làm lộ lỗi quoting/path khi module và tempfile ở đường dẫn Unicode có dấu cách.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review-evidence/hunt_extra.py` (unicode-paths); copy hai Python vào cây scratch có tên `đường dẫn có dấu và khoảng trắng`, đặt TMPDIR=`tạm có khoảng trắng`, Python3.12 + UTF8 + sim; chạy `--mot-ca` c03/c09/c14/c08.
- output thật: cả bốn ca `rc=0; stdout='\n'; stderr=''` (chế độ một ca của suite chỉ in dòng rỗng khi thành công). c14 bao gồm cả bốn tổ hợp root/tep tương đối/tuyệt đối; c08 chạy nhánh lỗi input/CLI.
- kết luận: **KHÔNG PHẢI LỖI** trên filesystem Linux và đường dẫn đã đo; không suy về Win32 API.

HƯỚNG 3: Lỗi vô can được đếm là giết mutation?

- giả thuyết: phan_hang cho GIET chỉ vì tiến trình đỏ hoặc marker của ca khác.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review-evidence/hunt_extra.py` (failure-classifier); gọi chính hàm với rc/marker điều khiển.
- output thật: rc=0→SONG_SOT; rc=1/2 kèm marker c09→HONG; rc=3 + marker c09→GIET; rc=3 + marker c01_other→TIN_DUNG_GIA; rc=4 + marker c09→TIN_DUNG_GIA. Hai tự kiểm đầy đủ của suite cũng DAT trong mọi lượt.
- kết luận: **KHÔNG PHẢI LỖI** cho ma trận rc/marker đã đo.

HƯỚNG 4: Khác minor Python với CI làm newline keyword hoặc mutation runner hỏng?

- giả thuyết: chỉ Python 3.13 đang dùng mới chạy được, CI Python3.12 bị regression.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review-evidence/run_py312.py`; bên trong chạy toàn suite head với Python3.12, sim và env UTF8.
- output thật: Python 3.12.3 / PyYAML 6.0.1; CA 16/16; DOT BIEN 64/64; TU KIEM PHAN HANG DAT (2); TONG DAT; rc=0; 73.21 s.
- kết luận: **KHÔNG PHẢI LỖI** tương thích Python3.12 trên Linux; native Windows và tổ hợp chính xác dependency CI vẫn KHÔNG ĐO ĐƯỢC.

HƯỚNG 5: Fixture tạm che mất regression trên hồ sơ thật hoặc thay danh sách miễn trừ?

- giả thuyết: sửa test làm checker/allowlist trôi hoặc chỉ dữ liệu giả mới qua.
- lệnh: trong từng cây base/head đã dựng, `PYTHONDONTWRITEBYTECODE=1 python3 ops/land_evidence_nguon.py`; so stdout và SHA256 checker.
- output thật: cả hai rc=0; `land_evidence_nguon: 18 ĐẠT · 28/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 46`, `TỔNG: ĐẠT`; stdout bằng nhau. Checker SHA256 cả hai `7f621c4aa88fb9dd9c9549b5c7671f7fca3b53804366da48f1e2a0778a703b87`.
- kết luận: **KHÔNG PHẢI LỖI** trên toàn bộ 46 hồ sơ local; không khẳng định nội dung của hồ sơ được miễn trừ đã qua luật.

HƯỚNG 6: Diff đồng thời nới assertion hoặc mutation để “chữa” màu đỏ?

- giả thuyết: ngoài EOL, bản vá có thay kỳ vọng/giảm số ca/đột biến.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 review-evidence/audit_static.py`; parse AST base/head, chỉ bỏ 4 keyword newline rỗng khỏi AST head rồi so toàn AST không vị trí.
- output thật: `AST delta only newline empty keywords: True; lines=[74, 198, 248, 251]`; checker cùng SHA256; base/head Ruff cùng `All checks passed!`, rc=0; numstat exact match=True.
- kết luận: **KHÔNG PHẢI LỖI**. Không có assertion/mutation bị nới hoặc sửa checker trong diff.

Output nguyên văn của các hướng: [extra-hunts.log](review-evidence/extra-hunts.log), [head-py312-CRLF.log](review-evidence/head-py312-CRLF.log), [checker-summary.log](review-evidence/checker-summary.log), [static-audit.log](review-evidence/static-audit.log).

## FINDING

### c09-thieu-chot-byte-sau-ghi  [P3]  Hai lần ghi sau của c09 chưa khóa được hợp đồng byte LF

TỆP/DÒNG: `ops/land_evidence_nguon_test.py:248` và `:251`, hàm `c09_l5_mien_tru_theo_bam`.

VẤN ĐỀ: Hai keyword đang có là đúng N1. Tuy nhiên, suite không phát hiện khi từng keyword bị bỏ lại. Chốt ở lần ghi thứ hai chỉ đòi lệch hash/rc=1, lần thứ ba đòi lệch hash/rc=0. CRLF cũng lệch hash nên cả hai phép gỡ đều CA 16/16 · DOT BIEN 64/64 · DAT. Riêng lời mô tả “lệch một byte” cũng không tự chứng minh chỉ thêm đúng một byte. Không có lỗi runtime còn mở do hai dòng hiện tại: đây là thiếu độ nhạy chống tái phạm, mức P3.

ĐÃ THỬ NGHIỆM:

- `run_mutations.py`: từng phép gỡ riêng ở 248/251 có rc=0, TONG DAT; trace ghi 32 thay vì 31 byte và 26 thay vì 25 byte.
- `PYTHONDONTWRITEBYTECODE=1 python3 review-evidence/probe_byte_assertions.py`: **chỉ trên cây scratch**, thêm kiểm `read_bytes()` bằng `.encode("utf-8")` của nội dung kỳ vọng ngay sau hai lần ghi. Ca c09 strengthened-head rc=0. Từng bản gỡ keyword lần lượt rc=3, stdout `DO:c09_l5_mien_tru_theo_bam:review-byte-contract-first` và `...:review-byte-contract-second`. [byte-assertions.log](review-evidence/byte-assertions.log).

GỢI Ý:

- Vá ở c09 ngay sau mỗi write vì đây là nơi yêu cầu exact byte và câu “một byte”; không buộc checker đổi logic nghiệp vụ.
- So read_bytes với nội dung kỳ vọng encode UTF8, rồi giữ nguyên các chốt hash/luật sẵn có. Không dùng read_text để kiểm LF vì nó chuẩn hóa CRLF.
- Ca khóa: chạy c09 dưới sim, từng đột biến bỏ newline ở 248/251 phải chết đúng chốt byte; đã đo gợi ý như trên. L198 không cần phép so byte cho mục tiêu mâu thuẫn merged_at hiện tại.
- Rủi ro của gợi ý: test ràng buộc representation chặt hơn ngữ nghĩa YAML; chỉ nên áp nơi spec yêu cầu byte cố định, tránh mở sang mọi source-code write hoặc checker read_text.

ĐỘ TIN: cao.

## TRẠNG THÁI CUỐI VÀ BẰNG CHỨNG

- passed: N1/N2/N3/N5, write set, cả bốn phép gỡ newline đã thực hiện (một đỏ đúng dự kiến, ba sống được giải thích), các hướng săn local.
- failed đúng dự kiến: base CRLF và head gỡ newline ở cay; không phải lỗi test bị bỏ qua.
- not_run / KHÔNG ĐO ĐƯỢC: N4 check run/log Windows; toàn job native Windows, do gói offline không có artifact và không được dùng mạng. Không coi rc của suite Linux là kết luận job CI.
- blocked: nghiệm thu đầy đủ N4. Bước để gỡ chặn là có check run/log của workflow_dispatch `ci.yml` trên đúng SHA, chứng minh job `gate-registry (windows-latest)` success và đã thực sự chạy; không cần sửa mã chỉ để lấp phần chưa đo.
- Không có P0/P1/P2 đã đo còn mở. Chỉ có ghi chú P3 trên; không coi ba mutation sống là ba lỗi runtime.
- Worktree review sạch lúc đầu/cuối, exact head/tree không đổi. Mọi bản sao/đột biến ở ngoài cay-kho; không phát sinh bytecode trong cây review.

```text
git status --porcelain: rc=0, stdout=''
HEAD=d6b1e2d27cadc1d985ad2868aeae444598a6b97a
TREE=2011f62e0615ef098cdeabd203990ac876891dc7
SPEC sha256=48731f52ab75fd541b416c9aebc32231a05782d7754dec86b606aec580be48a8
```

Report được tạo với `verdict: pending` ngay khi đọc xong chỉ thị và append sau mỗi phép đo. Nhật ký tăng dần trước khi biên tập bản này được giữ tại [progress.md](review-evidence/progress.md). Script tái lập và log/JSON đầy đủ nằm trong `review-evidence/`; đường dẫn các cây scratch được giữ trong [paths.json](review-evidence/paths.json). Không truy cập mạng, không đăng GitHub.
