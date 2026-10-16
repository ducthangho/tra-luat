# Cross-review độc lập — packet #675 r2 g2 — lượt 5
verdict: approved
reviewed_sha: 41d52ae461b267f7f5291a0794c5328cc00dc360
reviewed_tree: bd5b5ee65e511d0237f39ac68f79b9c44e14e298
baseline_sha: cd23c7dbc7833d64a8e87e8ffd94f194c18e0060

Provider OpenAI; execution surface Codex qua API, công cụ shell cục bộ; transport trực tiếp. Model GPT-6 theo chỉ dẫn phiên (tự khai); effort/biến thể và attestation runtime độc lập: **KHÔNG ĐO ĐƯỢC**. Executor được khai trong vật liệu là Claude Sonnet 5.5. Vai trò reviewer độc lập, hai trục Spec và Standards/Security.

**Kết luận: approved — 0 P1 / 0 P2 / 0 P3.** I1 đã vá thật theo đúng phản chứng lượt 4 và chốt khôi phục cache có răng. Còn **J1 — lần thứ 5, cùng hình dạng**, được chuyển thành **GIỚI HẠN KHAI BÁO / Chấp nhận giới hạn** theo quyết định chủ kho; không tính vào P. Các bộ hồi quy được yêu cầu, kể cả hai bộ dài, đã hoàn tất; lỗi lint nền và các lần đỏ ngoài dự kiến được ghi rõ bên dưới.

Hai cây nguồn được đối xử read-only. Mọi thử nghiệm/đột biến dùng bản sao tại `tam/tmp.m6iWkppEzG/`, tạo bằng `mktemp -d -p "$PWD/tam"`. W4/W5 có TMPDIR và RUNNER_TEMP trong `tam/`; không push hoặc đăng GitHub. Báo cáo đã được ghi tăng dần và chốt trên exact SHA ở trên.

Trong các lệnh rút gọn, `<scratch>` là `tam/tmp.m6iWkppEzG/`; argv tuyệt đối, cwd, môi trường đo, mã thoát và output của từng ca nằm trong thư mục `logs/`. Các harness lấy từ lượt 4 chỉ tái dùng cách dựng phản chứng; mọi kết quả được ghi ở đây là lần chạy mới trên head lượt 5.

Chỉ thị chủ kho áp dụng: “Vá I1 theo đối chứng + review lượt 5. Nếu lượt 5 lại ra cùng hình dạng ⇒ tự động chuyển sang 'Chấp nhận giới hạn' (không hỏi lại).” Biểu hiện mới cùng lớp `phep-do-khong-neo-ma-chay` được ghi thành GIỚI HẠN KHAI BÁO; các lớp khác vẫn phân hạng P1/P2/P3.

HƯỚNG 1 — Neo nguồn và phạm vi

Lệnh và output nguyên văn lưu trong `tam/tmp.m6iWkppEzG/logs/anchors.json`: `git -C cay-kho rev-parse HEAD HEAD^{tree}`, tương tự cây nền; `sha256sum SPEC.md`; `git -C cay-kho diff 89fc4fa..HEAD --numstat`; `git -C cay-kho diff cd23c7d..HEAD --numstat`; `git -C cay-kho diff 89fc4fa..HEAD --check`.

SPEC đúng SHA256 `81fb6d533a892ec33c9b6b3f161dc1eca971579f4acfdb277c26521539be71cc`. Commit cuối chỉ W4, +2/−3 dòng; bỏ `B_SEEN` và nhánh bỏ qua hash đã thấy. Các phép đo phía dưới chạy lại trên head này, không dùng kết quả lượt trước làm bằng chứng mới.

Output phạm vi packet: W1=3/1, W2=2/1, W3=2/1, W4=284/0, W5=6/2 (thêm/xóa), tổng **297 dòng thêm ≤300**. Diff `89fc4fa..HEAD` chỉ năm tệp write set; `--check` rc0. Diff nền có thêm bốn tệp từ lịch sử merge master, không quy thành sửa của packet. **KHÔNG PHẢI LỖI** neo/phạm vi/trần.

HƯỚNG 2 — Hồi quy chung (kết quả đối chiếu)

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python tam/tmp.m6iWkppEzG/measure.py regressions`. Harness ghi từng argv/cwd/env/rc/thời gian vào `logs/<case>.json`, stdout/stderr riêng. Tiến trình con khôi phục SIGPIPE mặc định; Git fixture ghim `commit.gpgsign=false`, `core.abbrev=7` qua môi trường. Công cụ có sẵn; không tải/cài mạng.

| Lệnh trên bản sao đầy đủ | Head | Nền | Delta/kết luận |
|---|---|---|---|
| `bash ops/don_ref_chot_test.sh` | 105/105, rc0, 2,024s | 105/105, rc0, 2,172s | Không mất ca |
| `python ops/bash_nen.py quet --root .` | DAT, rc0, 17,247s | DAT, rc0, 17,481s | Delta0 |
| `python .claude/dev/ci_dang_ky_test.py` | 938/938 phản chứng, TỔNG: ĐẠT, rc0, 6,855s | Cùng kết quả, rc0, 7,196s | Delta0 |
| `actionlint .github/workflows/*.yml` có ShellCheck | rc1, SC1003 ở ops-don-ref.yml:117 | Cùng lỗi | Lỗi nền, **KHÔNG PHẢI LỖI packet** |
| `shellcheck --format=json W1 W2 W3 W5 [W4 trên head]` | rc1, SC1090 ở cai_cong_cu.sh:54 | Cùng lỗi | Delta0; W4 không thêm lỗi |

Kết quả hoàn tất hai suite dài nằm ở HƯỚNG 7–8 và HƯỚNG 11; không dùng output giữa chừng như bằng chứng đạt toàn bộ.

HƯỚNG 3 — Phản chứng I1 và lớp neo mã chạy

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python tam/tmp.m6iWkppEzG/third.py helpers`. Dùng chính hàm dựng mutant của lượt 4: tách vòng dò vào `kiem_mac_dinh`, helper-control giữ vòng `case`, helper-after đổi helper thành hai pipeline `printf | grep -q` ngay sau lời gọi `lam` đầu, helper-before dùng helper xấu từ đầu. Mọi mutant chỉ đổi W5 trên bản sao; W4 head giữ nguyên.

| Ca `--lan 3` | Output | Kết luận |
|---|---|---|
| helper-control | 53/53, rc0, 100,486s | Control hợp lệ |
| helper-after | 52/53, rc1, 208,902s; 24 body, khớp đầu sai 69/72 | Bắt helper đổi sau ca đầu |
| helper-before | 52/53, rc1, 195,707s; 24 body, khớp đầu sai 72/72 | Bắt helper xấu từ đầu |
| Khôi phục cache + helper-after | 53/53, rc0, 26,718s | Chốt có răng: xanh giả cũ trở lại |

Ca cuối chạy `python tam/tmp.m6iWkppEzG/review5.py controls`: bản sao W4 lấy từ `git show HEAD^:ops/do_sigpipe.sh`, chính là bản trước commit +2/−3 đang review (diff đã xác nhận chỉ cache/chú thích). **I1 ĐÃ VÁ THẬT theo đúng phản chứng lượt 4**, không chỉ thay kết quả chấm. Lớp rộng còn J1 dưới đây.

Witness helper-control và helper-before chạy toàn W5 **105/105** rồi stress: control chỉ hai explicit; before thêm hai fallback. Witness helper-after lượt đầu **104/105, rc1**, dừng ở ca CHỐT `luu-tru/**: có tag giữ thì QUA`, trước khi tới recorder; không dùng run này chứng minh I1. Nhật ký thất bại được giữ, phép xác nhận lại ghi ở phần hoàn tất.

Xác nhận `witness-helper-after-retry`: **105/105, rc0, 4,148s**, rồi explicit kèm hai fallback (`logs/witness-helper-after-retry.*`). Lệnh: `bash -c 'exec 3>&1; exec bash "$1"' _ <scratch>/mutants/witness-helper-after/ops/don_ref_chot_test.sh` qua cùng harness/env. Đủ đối chứng hành vi cho cả ba helper.

HƯỚNG 4 — Finding mới và GIỚI HẠN KHAI BÁO

| ID | Phân loại / vị trí | Bằng chứng | Xử lý |
|---|---|---|---|
| J1 | **GIỚI HẠN**, không tính P; W4 `ops/do_sigpipe.sh:191–195`; slug `phep-do-khong-neo-ma-chay` | Probe luôn gọi `lam t 0 xoa-nhanh r1 sha thu ...`; không dùng đối số của lời gọi đang bị quan sát. Nhánh hỏng chỉ khi thao tác thực là `tao-tag` lọt **53/53, rc0**, trong khi lời gọi thật thêm fallback sau explicit. | **lần thứ 5, cùng hình dạng**, F1 → G2 → H1 → I1 → J1. Tự động chuyển **Chấp nhận giới hạn** theo quyết định chủ kho, không đề xuất thiết kế lại. |

Lệnh tái lập: `PYTHONDONTWRITEBYTECODE=1 python tam/tmp.m6iWkppEzG/review5.py limits`. Mã dựng giữ nguyên vòng `case` ở mọi thao tác ngoài `tao-tag`; riêng `tao-tag` dùng lại hai phép dò pipeline cũ:

```bash
if [ "$hd" = tao-tag ]; then
  if printf '%s\n' "$@" | grep -q '^GIA_REF_STATE='; then mac_ref=0; fi
  if printf '%s\n' "$@" | grep -q '^NEO_TEP='; then mac_neo=0; fi
else
  for a in "$@"; do case "$a" in GIA_REF_STATE=*) mac_ref=0 ;; NEO_TEP=*) mac_neo=0 ;; esac; done
fi
```

Mutant `mutants/tag-branch/` không biết hoặc sửa trap, seam, checksum, biến hay biên nhận của observer. W4 nguyên vẹn + mutant, `--lan 3`: **53/53 DAT, rc0, 169,018s** (`logs/j1-tag-branch.*`). Vì cả ba dạng probe đều dùng `xoa-nhanh`, tăng số lần vào hàm vẫn không đi qua nhánh `tao-tag` đang chạy thật.

Đối chứng hành vi: chạy **toàn W5**, giữ đủ ca gốc, rồi nối recorder tại `env` và lời gọi `tao-tag` với hai explicit ở đầu +20.000 đối số. Cả control/head và mutant đều **105/105, rc0** trước lời gọi thêm. Head chỉ in `WITNESS:GIA_REF_STATE=explicit`, `WITNESS:NEO_TEP=explicit`; mutant in thêm `GIA_REF_STATE=…/refstate`, `NEO_TEP=…/neo_auto` phía sau. Log `j1-witness-{control,tag-branch}.{stdout,json}`. Đây là B1 tái xuất hiện trong mutant thực, không phải chỉ phá phép tổng kết W4.

Phạm vi giới hạn cần khai: **W4 xác nhận ba bộ đối số tổng hợp trên hàm đang tồn tại tại các lần observer bắt được; không chứng nhận mọi nhánh phụ thuộc đối số/ngữ cảnh của lời gọi thực.** Không diễn giải “đo mỗi lần vào lam” thành “đo đúng mọi đường chạy của lam”. J1 là giới hạn sức bắt hồi quy W4; chưa thấy lỗi B1 trong W5 head hiện hành. Không đếm lại G2/H1/I1 như các finding P mới.

HƯỚNG 5 — Reentry, side effect và chi phí

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python tam/tmp.m6iWkppEzG/review5.py audits`. Bản sao W4 chỉ thêm ghi biên nhận/hash trước–sau probe và lưu output trước khi dọn; so với bản sao khôi phục cache. Đây là **phép chẩn đoán có instrument**, tách khỏi các run head nguyên vẹn. Log `logs/audit-copy/1..4/`, `audit-summary.json`, `audit-{each-call,cache}.json`.

- `--lan 1`: bỏ cache **53/53 rc0, 69,972s**; có cache **53/53 rc0, 22,027s**. Mỗi lượt B1 có **trap=24, seam=24**, không bùng đệ quy ở head. Bỏ cache có24 `body`/72 record probe; cache có1 `body`/3 record. Cả phép head và tự kiểm B1 cho cùng số lượng tương ứng.
- Probe **có side effect trong fixture**, không phải phép đọc thuần: QUA tăng 3 mỗi entry ở `--lan 1`; `gialog`, `refstate`, `neo_auto`, `out` được tạo/ghi lại; hash trước–sau khác. W5 dưới observer in **177/177** so với **108/108** khi cache và **105/105** khi chạy suite trực tiếp. Không dùng số177 làm bằng chứng không mất ca: A6 được kiểm độc lập bằng105/105 ở HƯỚNG2.
- Chi phí từ chính vòng lặp là `2 × 24 × 3 × LAN` lời gọi stress cho head và tự kiểm, mỗi lời gọi mang20.000 đối số đệm: `--lan 10` là **1.440** lời gọi stress, **28.800.000 lượt đối số đệm**; đây là phép tính từ số entry đo được, không phải số syscall. Tệp fixture bị thay đổi lặp lại là hạn chế của phép quan sát; trong các ca hiện hành đã đo, chưa thấy sai hành vi mới hoặc ghi ngoài fixture. Thời gian có cạnh tranh tài nguyên, không coi số này là benchmark cô lập.

Head nguyên vẹn, `python tam/tmp.m6iWkppEzG/measure.py initial` gọi `bash head/ops/do_sigpipe.sh --goc head --lan 10`: **53/53, rc0, 420,803s** (`logs/w4-head.*`). Executor khai khoảng 4 phút; lượt này khoảng 7 phút trong khi nhiều bộ đo khác cùng chạy. Xác nhận được chi phí tăng đáng kể, **không đủ cơ sở** coi chênh lệch wall time này là lời khai sai hay tăng trưởng không kiểm soát. Chi phí phụ thuộc tuyến tính số entry × LAN × số đối số trong cấu trúc vòng lặp hiện tại; không có yêu cầu thời gian tối đa của W4 trong SPEC.

HƯỚNG 6 — H3 và an toàn fixture

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python tam/tmp.m6iWkppEzG/review5.py safety`; log `logs/h3-{present,absent,explicit}.*`, `logs/safety.json`. RUNNER_TEMP của caller nằm ngoài TMPDIR của W4, nhưng cả hai vẫn trong scratch do reviewer sở hữu.

Cả ba ca `--lan 1` **53/53, rc0**: mặc định đã có, mặc định chưa có và NEO_TEP tường minh. Tệp có sẵn giữ 30 byte, SHA256 `d90a2014f519386df97c789de10f5e13eec7c5d6f548f18d7a20876186b28509` và mtime_ns; tệp vắng vẫn vắng. Sentinel HOME giữ hash/mtime. TMPDIR trống sau run; ngoài những sentinel đã dựng không có tệp mới trong HOME/RUNNER_TEMP. `/tmp/don_ref_neo.txt` thật được đọc snapshot, không sửa/xóa: cả ba cặp trước/sau giữ 0 byte, SHA256 rỗng, mtime_ns `1790696696306487047`.

Lệnh probe `strace -f -e trace=file,network -o <scratch>/logs/strace-probe.trace true` → rc1, `PTRACE_TRACEME: Operation not permitted` (`logs/strace-probe.json`). **KHÔNG ĐO ĐƯỢC syscall audit toàn cục** hoặc mọi hành vi ghi rồi hoàn nguyên. Snapshot trên các đích nêu trên chứng minh phạm vi quan sát, không phải bảo đảm tuyệt đối mọi ghi/mạng của một script tùy ý.

Phản chứng gỡ riêng `env -i` ở driver B1 trên bản sao W4: **52/53, rc1, 65,639s**, đúng `(e) B1/cach-ly-ghi` đỏ (`logs/h3-without-env-i.*`). Tất cả đích ghi của ca đột biến vẫn trong scratch. **H3 ĐÃ VÁ THẬT** ở các đường đã đo; bỏ cache không mở lại rò ghi đã biết.

HƯỚNG 7 — Hoàn tất hồi quy và ngoại lệ cần giữ trong báo cáo

- `python <scratch>/t5_repeat.py`, qua `measure.run('t5-repeat', ...)` với TMPDIR/RUNNER_TEMP/HOME trong scratch: **head 200/200 và nền 200/200**, mọi rc0, rc141=0, từng lần có JSON DAT/1.7.7; 71,114s và 87,110s. Gói1.7.7 offline và PATH có bản sai 9.9.9. Log `logs/t5-repeat.*`. Nền không gặp race trong200 lần này không phủ định phép stress20.000 của W4.
- `python ops/lease_publish_test.py`: head **187/187, đã chạy 187, bỏ qua 0, rc0, 523,627s**. Nền lượt đầu **186/187, rc1, 521,367s**: t125 báo hai suite con khác kết quả; nhánhA của t154 ném `ValueError: invalid literal for int() with base 10: ''` khi đọc PID, nhánhB và lần t154 ở suite ngoài đều đạt. Log `logs/base-lease.stdout:1035–1036,1210,1230`. **Không quy lỗi nền này cho packet**, cũng không tự kết luận nguyên nhân chỉ từ tên ca; lần xác nhận lại nền ở HƯỚNG 8, giữ nguyên lần đỏ đầu.
- `follow.py compare`: stdout của W5/bash_nen/ci/actionlint/shellcheck giống hệt head/nền, lần lượt 5314/41/54062/224/216 byte (`logs/regression-compare.json`). `follow.py versions`: Bash5.2.21, Python3.11.15, Git2.43.0, actionlint 1.7.7, ShellCheck 0.11.0. `bash -n` từng `ops/*.sh`: head8/8, nền7/7, rc0.
- `h1-seam-command`: ca phụ đổi `env` thành `command env` làm stress đi qua thực thi downstream thay vì recorder; reviewer dừng sau nhiều phút, harness rc130, **KHÔNG ĐO ĐƯỢC rc/kết luận cuối của W4**. Giữ `logs/h1-seam-command.{stdout,stderr}` và `h1-seam-command-interrupted.json`. Không coi đây là xanh/đỏ hoặc khẳng định một timeout nội tại của sản phẩm. Các khóa bắt buộc còn lại chạy riêng sau đó; không để việc dừng ca phụ biến các ca chưa chạy thành pass.

Bổ sung reentry: `python <scratch>/review5.py recursion` dựng wrapper đệ quy một tầng, dùng local guard rồi gọi `lam "$@"` trước khi vào thân gốc. W4 **53/53, rc0, 64,811s** (`reentry-recursive-control`); suite trực tiếp lần xác nhận **105/105, rc0, 5,237s** (`reentry-recursive-suite-retry`). Không gặp bùng đệ quy ở biến thể bảo toàn hành vi này. Lần dựng harness đầu neo chuỗi thiếu đầu dòng nên assertion từ chối trước khi chạy W4; đã sửa mỏ neo riêng harness. Lần suite đầu104/105 là ca CHỐT trước `lam`, được giữ log, không dùng làm chứng nhận. **KHÔNG PHẢI LỖI mới** về reentry trong đường đã đo; không suy thành chứng minh mọi hàm đệ quy.

HƯỚNG 8 — W4 head/nền và các khóa cũ (kết quả hoàn tất)

Lệnh: `python <scratch>/measure.py initial`; `python <scratch>/review5.py oldlocks` (phần đã hoàn tất trước ca phụ bị dừng); sau đó `python <scratch>/measure.py scoring`, `.../measure.py deps`, `.../measure.py old` chạy riêng. Từng lệnh thật và output đầy đủ nằm trong `logs/<case>.json/.stdout/.stderr`.

- W4 head `--lan 10`:53/53 rc0; W4 `--goc <bản sao nền đầy đủ>` `--lan 10`: **49/53, rc1, 469,056s**. Ba `(d)` riêng đều `rc0=0 rc141=10 khac=0`; B1 khớp đầu sai 240/240 qua24 entry. Số49 phản ánh đúng bốn điểm đỏ, không có ca mất âm thầm.
- Redef-trước/sau, `"lam"` có ngoặc, `$L`, subshell: mỗi ca `--lan 1` **52/53, rc1**; trước sai 24/24, sau/các biến thể lời gọi sai 23/24. Redef y hệt vẫn **53/53, rc0**. `builtin trap - DEBUG` + redef-sau **rc2**, `KHÔNG ĐO ĐƯỢC: ... trap=1 seam=24`. H1 cũ đã bị chặn trong những biến thể này.
- `cksum` trả127 từ lần0/1/2/5: **4/4 rc2 + KHÔNG ĐO ĐƯỢC**, nêu đúng `cksum`; lần0 dừng ở preflight, các lần sau báo lỗi observer. H4 đóng; không biến lỗi công cụ thành số liệu B1 sai.

Các cây chỉ đưa riêng W1/W2/W3/W5 về nền được đo với `--lan 1` để tách đúng điểm tác động; bộ toàn nền phía trên đã xác nhận từng điểm SIGPIPE10/10. Lượt mixed-W1 `--lan 10` đang chạy đã được dừng khi chuyển lịch đo, **không sử dụng kết quả dở dang**. Mã thoát130 là của harness bị ngắt, không gán cho W4. Kết quả hoàn chỉnh mang tên `w4-isolated-0..3`; lệnh/môi trường mỗi ca lưu trong JSON, quyết định đổi lịch lưu `initial-isolation-interrupted.json`.

Các khóa hoàn tất bổ sung (`--lan 1`, tên log cũng là ID ca trong harness):

| Khóa/đột biến | Output thật | Kết luận |
|---|---|---|
| F1: `old-unused-function`, `old-heredoc` | Mỗi ca51/53, rc1; `(d)` không chạy được LENH, `(c)` cũng từ chối lý do không phải141 | Hai phản chứng gốc đóng |
| F2: `old-missing-0..3` |4/4 rc2, KHÔNG ĐO ĐƯỢC và đúng tên W1/W2/W3/W5 bị thiếu | Đóng |
| Corpus: `old-strip-star` |50/53, rc1; đúng 3 đầu vào glob đỏ | Đóng |
| G1: `old-all-postcut` |50/53, rc1; nối pipeline nền sau mỗi dòng vá, ba `(d)` đều `rc141=1` | Không còn cắt bỏ mã sau dòng vá |
| G1: `old-exit-after`, `old-overwrite-after` | Mỗi ca52/53, rc1 ở `(d)` | Kiểm dấu vết tại điểm sử dụng có tác dụng |
| G2: `old-dead-lam` |52/53, rc1; hàm head ở here-doc, hàm sống là baseline, B1 khớp đầu sai 24/24 | Đóng phản chứng mã chết; lớp còn J1 |
| H2/F3/G4: `h2-155` + `h2-155-basew1` | Cả hai in53/53 nhưng **rc1, CO PHEP DO ĐỎ** khi `ghi` toàn cục luôn tăng DAT | Cờ SAI chặn xanh giả |
| H2: `h2-155-d` + bản chỉ W1 nền |50/53, rc1; cả ba `(c)` đỏ | Nhánh cấp DAT vô điều kiện riêng `(d)` bị bắt |
| H2: `h2-174`, `h2-175` | Mỗi ca50/53, rc1; cả ba `(c)` đỏ | Predicate(d)/nhánh ghi(d) luôn đúng đều bị bắt |
| H2 B1: `h2-b1` |52/53, rc1; `(c) B1/dot-bien-printf-grep` đỏ, ghi4/4 không đủ | Tự kiểm B1 đi qua đường cấp điểm |

Tên155/174/175 là ID harness giữ từ lượt trước, **không phải số dòng hiện tại**: tương ứng dòng149/167/168 của W4 head; predicate B1 ở226. Không nhầm số ca bị chính mutant phá thành xanh khi rc thực và cờ SAI vẫn đỏ.

Xác nhận lại nền của bộ lease: `base-lease-retry` **187/187, đã chạy 187, bỏ qua 0, rc0, 471,174s**. Lệnh vẫn `python ops/lease_publish_test.py` trên cùng bản sao/ENV. So với head 187/187, lần xác nhận có delta lỗi 0. Run186/187 trước đó là thất bại thật trên nền và vẫn được báo ở HƯỚNG 7; không thay thế/xóa nó hoặc khẳng định chắc chắn nguyên nhân là tải.

Từng điểm về nền (`w4-isolated-0..3`): W1 **52/53 rc1, 47,418s**; W2 **52/53 rc1, 46,665s**; W3 **52/53 rc1, 40,637s**; W5 **52/53 rc1, 45,843s**. Ba ca đầu đúng `(d)` tương ứng rc141=1; ca W5 đúng B1 khớp đầu sai 24/24. Không thấy ca đỏ phụ ngoài điểm đích trong bốn run này.

G3: `python <scratch>/follow.py dependencies` qua wrapper chờ cây W5 nền sẵn sàng; `seq -f` trả127 vẫn head **53/53 rc0** và W5 nền **52/53 rc1** (`--lan 3`, khớp đầu sai 72/72). `awk` trả127 → rc2, báo producer thất bại; `awk` trả0 nhưng không có payload → rc2, báo1 dòng thay vì 20001. Log `g3-{seq-format,seq-basew5,awk-fail,awk-short}.*`. PAD không mất âm thầm khi producer cũ bị hỏng; **G3 đóng**.

HƯỚNG 9 — ĐỐI CHIẾU F/B/G/H/I, đóng cụ thể và giới hạn còn lại

| Finding/lớp | Trạng thái lượt 5 | Bằng chứng đo lại |
|---|---|---|
| F1 | **ĐÃ VÁ THẬT** cho hai đường W1; lớp rộng còn J1 được chấp nhận | unused-function/here-doc51/53; G1 ba điểm rc141 |
| F2 | **ĐÓNG** | Thiếu riêng W1/W2/W3/W5:rc2 + đúng tên tệp |
| F3 | **ĐÓNG** trong các khóa cấp điểm được yêu cầu | Tất cả mutant H2 cùng đường chấm bị từ chối |
| B1 | **ĐÃ VÁ THẬT hành vi W5 head**; giới hạn khóa hồi quy là J1 | Explicit20.000 giữ đúng; W5 nền52/53; suite105/105 |
| G1 | **ĐÓNG** | Pipeline sau ba dòng vá50/53; exit/overwrite sau dòng52/53 |
| G2 | Phản chứng cũ **đóng**; lớp **còn giới hạn J1 đã chấp nhận** | dead-lam52/53; nhánh tao-tag lọt53/53 |
| G3 | **ĐÓNG** | Phá seq-f không xóa payload; awk hỏng/ngắn rc2 |
| G4 | **ĐÓNG**, cùng F3/H2 | Predicate, callsite và nhánh ghi đều bị tự kiểm bắt |
| H1 | Các phản chứng quote/builtin-trap/redef **đóng**; lớp **còn J1 đã chấp nhận** | quote/redef52/53; builtin-trap rc2; J1 HƯỚNG4 |
| H2 | **ĐÓNG** | ghi toàn cục luôn đúng vẫn rc1 với SAI; các mutant hẹp đều có(c) đỏ |
| H3 | **ĐÓNG đường rò ghi đã biết** | Sentinel có/vắng/explicit giữ nguyên; gỡ env-i52/53 |
| H4 | **ĐÓNG** | cksum hỏng tại0/1/2/5 đều rc2, đúng chẩn đoán |
| I1 | **ĐÃ VÁ THẬT theo đúng phản chứng lượt 4** | helper-control53/53; before/after52/53; khôi phục cache khiến after53/53 |
| Corpus glob | **ĐÓNG** | strip-star đỏ đúng 3 đầu vào |

Không đếm một biểu hiện thành nhiều finding. Bảng finding mới có **một J1/GIỚI HẠN**, không có P1/P2/P3 mới trong phạm vi đã đo. I1 đóng không đồng nghĩa đóng toàn lớp `phep-do-khong-neo-ma-chay`; quyết định S3 lần 2 của chủ kho xử lý J1 bằng **Chấp nhận giới hạn**, không phát thêm một vòng thiết kế/vá/review.

HƯỚNG 10 — Phạm vi chưa đo và ý nghĩa kết luận

- **KHÔNG ĐO ĐƯỢC** audit syscall toàn cục do ptrace bị chặn; không chứng nhận mọi hành vi ghi/mạng hoặc ghi rồi hoàn nguyên bằng snapshot sentinel.
- **KHÔNG ĐO ĐƯỢC / not_run** Windows/macOS, toàn bộ biến thể PATH/caller, mọi đường phá observer phối hợp; không chạy lại 5.436 so sánh giá trị của các lượt trước. Các kết quả lịch sử đó chỉ là vật liệu tham khảo, không nhập vào tổng phép đo lượt 5.
- **KHÔNG ĐO ĐƯỢC** kết luận cuối ca phụ seam-bypass đã dừng. Đây cũng giới hạn phép đánh giá thời gian khi mã được đo đi vòng qua recorder; không suy từ thời gian head sang mọi W5 tùy ý.
- **KHÔNG ĐO ĐƯỢC** effort/attestation runtime độc lập; provider/model được khai đúng nguồn quan sát như phần đầu. Không tự tạo assurance/approval receipt hoặc quyền land trên GitHub bằng tệp verdict cục bộ.
- Bare Ruff **not_run**; packet không đổi Python. Không gọi `bash_nen` hoặc bộ đăng ký CI là “Ruff passed”.

Các ca đỏ do đột biến có chủ đích là bằng chứng chốt hoạt động, không phải lỗi head. Các lần suite nền hoặc witness bị đỏ ngoài dự kiến được giữ riêng cùng lần xác nhận; không đổi chúng thành pass. Phép đếm ca và lỗi lint nền không thay cho kiểm hành vi.

HƯỚNG 11 — Hoàn tất A2 và tổng hợp nghiệm thu

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python <scratch>/review5.py cong`, gọi đúng `python ops/cong_cu_test.py` trên hai bản sao đầy đủ riêng `cong-head/`, `cong-base/`; TMPDIR/RUNNER_TEMP/HOME nằm trong scratch. Không sửa Python của bộ test. Mỗi suite dùng 4 tiến trình theo mặc định của nó.

| Kết quả toàn bộ | Head | Nền |
|---|---|---|
| Mã thoát/thời gian | rc0, 2481,290s | rc0, 2484,741s |
| Ca cơ bản |53/53; bỏ qua 0; tiền kiểm bỏ qua 0 |53/53; bỏ qua 0; tiền kiểm bỏ qua 0 |
| Bộ đột biến |212; lỗi đột biến 0 |212; lỗi đột biến 0 |
| Cổng cây thật |ĐẠT |ĐẠT |

Stdout **25.397 byte giống hệt**, SHA256 `007633398654914a064074a5c112e572363a0c2d3322e3d7df73bfc920587ff3`; stderr cả hai rỗng. Log `logs/{head,base}-cong.{json,stdout,stderr}`, `logs/cong-compare.json`. **A2 toàn suite đã đo xong trong lượt này**, cộng t5 head 200/200 ở HƯỚNG 7; không cần dùng bằng chứng các lượt trước thay cho nó. ShellCheck 0.11.0 được sao chép từ binary có sẵn vào scratch, actionlint 1.7.7 có sẵn trên PATH; không cài phụ thuộc qua mạng.

- **A1:** head 53/53; nền 49/53, ba điểm SIGPIPE10/10; từng điểm riêng 52/53; F1/F2/F3/B1/glob và hồi quy H/I có phản chứng. Phạm vi còn thiếu của lớp neo mã chạy là J1 đã được chấp nhận, không tuyên bố đóng toàn lớp.
- **A2:** hai suite 53/53, 212 đột biến không lỗi; t5 head 200/200, rc141=0.
- **A3/A4:** bash_nen và đăng ký CI đạt; actionlint/ShellCheck delta0 so nền, giữ nguyên hai chẩn đoán nền đã nêu. Không khai lint tuyệt đối sạch.
- **A6:** W5 head/nền 105/105; lease head 187/187 và nền xác nhận 187/187. Lần nền 186/187 vẫn được lưu/báo, không bị che bởi lần chạy lại.
- **A5/ngưỡng lượt 5:** **0 P1 / 0 P2 / 0 P3**, một giới hạn J1 được xử lý theo authority trực tiếp. **verdict: approved** là kết luận review cục bộ trên exact SHA; không phải thao tác approve/merge/land trên GitHub.

HƯỚNG 12 — Neo cuối, dọn và hiện vật

Lệnh: `python <scratch>/finalize.py anchors_end`; log `logs/final-anchors.jsonl` và từng JSON tương ứng. Head/tree vẫn `41d52ae461b267f7f5291a0794c5328cc00dc360` / `bd5b5ee65e511d0237f39ac68f79b9c44e14e298`; nền/tree vẫn `cd23c7dbc7833d64a8e87e8ffd94f194c18e0060` / `f905bbb1aeaa6e83c5ce09a603035eb71db9a5fc`. SPEC giữ nguyên SHA256. `git status --porcelain --untracked-files=all --ignored` trên **cả hai nguồn rỗng**, rc0; `git diff 89fc4fa..HEAD --check` rc0; phạm vi vẫn chỉ W1–W5, **297 dòng thêm**.

`bash <scratch>/cleanup.sh` dùng EXIT trap dọn **chỉ thư mục runtime `temp/` do reviewer sở hữu**, sau khi các phép chạy đã dừng/hoàn tất: **4632 mục →0** (`logs/cleanup.json`). Giữ bản sao, nguồn mutant, sentinel và log làm bằng chứng tái lập; không sửa/xóa `/tmp/don_ref_neo.txt` thật hoặc hai cây nguồn.

`python <scratch>/finalize.py summary` tạo `logs/all-results.json`; `python <scratch>/finalize.py hash_evidence` tạo `evidence.sha256` cho harness/nguồn đột biến/log và `logs/verdict-artifact.json` ghi path, size, SHA256 của bản verdict đã chốt. Không có commit, push hoặc đăng GitHub trong lượt này.
