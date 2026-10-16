# Cross-review độc lập — packet #675 r2 g2 — lượt 4
verdict: changes_requested
reviewed_sha: e311bbffaa820f3a12f2e2f8316582e312e344ea
reviewed_tree: 20bee52ebb573114d5870892e43c66e67b5cc4c1
baseline_sha: cd23c7dbc7833d64a8e87e8ffd94f194c18e0060

Provider OpenAI; execution surface Codex qua API với công cụ shell cục bộ; transport machine/tool trực tiếp. Model GPT-6 theo chỉ dẫn phiên (tự khai); effort/biến thể và attestation runtime độc lập: **KHÔNG ĐO ĐƯỢC**. Executor theo vật liệu: Claude Sonnet 5.5; không suy model từ actor GitHub.

Kết luận: **changes_requested — 0 P1 / 1 P2 / 0 P3**. H2/H3/H4 đã đóng trong các đường đo; H1 còn đường I1, **lần thứ 4, cùng hình dạng**. Đề nghị điều phối dừng vòng vá/review tự động và chuyển checkpoint chủ kho; reviewer không tự cấp vòng tiếp theo.

Hai cây nguồn chỉ đọc. Mọi thử nghiệm và đột biến dùng bản sao tại `tam/tmp.CEWbH0B0ZQ/`, tạo bằng `mktemp -d -p "$PWD/tam"`; mọi lần chạy W4/W5 có TMPDIR/RUNNER_TEMP trong `tam/`. Không sửa sản phẩm, không push, không đăng GitHub. Báo cáo được ghi tăng dần. Trong các lệnh rút gọn dưới đây, `.../` thay cho `tam/tmp.CEWbH0B0ZQ/`; argv đầy đủ có trong từng log JSON.

HƯỚNG 1 — Neo nguồn và phạm vi

- Lệnh: `git -C cay-kho rev-parse HEAD HEAD^{tree}`; `git -C cay-nen rev-parse HEAD HEAD^{tree}`; `sha256sum SPEC.md`.
- Output: head/tree như trên; nền đúng `cd23c7d…`, tree `f905bbb1aeaa6e83c5ce09a603035eb71db9a5fc`; SPEC SHA256 `81fb6d533a892ec33c9b6b3f161dc1eca971579f4acfdb277c26521539be71cc`; rc0.
- Lệnh: `git -C cay-kho diff 89fc4fa..HEAD --stat`; `git -C cay-kho diff cd23c7d..HEAD --numstat`; `git -C cay-kho diff HEAD^ HEAD --stat`; `git -C cay-kho log -1 --format=%B`.
- Output: chỉ W1–W5 trong diff packet; W1=3/1, W2=2/1, W3=2/1, W4=285/0, W5=6/2 (thêm/xóa), **298 dòng thêm ≤300**. Commit lượt 4 chỉ đổi W4, 73 thêm/69 xóa. Đã đọc bảng mọi đường và giới hạn executor khai trong commit. Các tệp merge master trong diff nền không tính vào write set packet.
- **KHÔNG PHẢI LỖI** về neo và trần. Chỉ thị trực tiếp cho lượt 4 ghi chủ kho đã quyết “Vá tiếp lượt 4” ở S3; review này không tự cấp vòng vá/review tiếp theo.

HƯỚNG 2 — Chạy lại H1/H2/H4

Lệnh tái lập: `PYTHONDONTWRITEBYTECODE=1 python tam/tmp.CEWbH0B0ZQ/measure.py w5_variants`, `.../measure.py scoring`, `.../measure.py deps`. Mỗi phép có argv/cwd/rc/thời gian/môi trường và stdout/stderr riêng trong `logs/`; các dòng tổng hợp là `h1.jsonl`, `h2.jsonl`, `h4.jsonl`. Tiến trình con dùng `subprocess.Popen`, khôi phục SIGPIPE mặc định; không nhầm SIGPIPE bị bỏ qua của shell công cụ thành hành vi sản phẩm.

- H1 đúng phản chứng cũ: redef-trước, redef-sau và `"lam"` sau lần gọi đầu đều **52/53, rc1**, đúng B1 khớp đầu đỏ. `builtin trap - DEBUG` + redef-sau → **rc2**, `KHÔNG ĐO ĐƯỢC: observer B1 khong bao phu moi lan goi lam: trap=1 seam=24`. Các phép trên dùng `--lan 3`.
- H2 predicate cũ :155 nay ở :149 (`ghi` luôn cấp DAT): head và bản chỉ W1 về nền đều **rc1**, dù dòng tổng có `53/53 — CO PHEP DO ĐỎ`. Cờ `SAI` độc lập giữ kết quả đỏ; không gọi đây là xanh giả vì số đếm bị chính mutant cố ý phá. Nhánh chỉ cấp vô điều kiện cho `(d)` cũng đỏ **50/53**.
- H4 wrapper `cksum` trả127 từ lần 0/1/2/5 (lần 0 là probe) đều **rc2 + KHÔNG ĐO ĐƯỢC**, nêu `cksum`; lần 0 dừng ngay, các lần sau có lỗi observer. Không còn biến lỗi công cụ thành số liệu B1 sai như H4 lượt 3.

HƯỚNG 3 — Đường chưa khai: cache thân `lam` bỏ qua thay đổi hàm phụ (I1)

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python tam/tmp.CEWbH0B0ZQ/third.py helpers`; `.../third.py witnesses`. Mã mutant và hàm dựng nằm trong `third.py`, cây đầy đủ tại `mutants/helper-{control,after,before}/`; log `third-helpers.jsonl`, `witnesses.jsonl`, `third-helper-*.stdout`, `witness-helper-*.stdout`.

Đột biến chỉ W5, không đổi W4 hay công cụ: tách đúng vòng `for a in "$@"; case ...` vào hàm `kiem_mac_dinh()`, gọi nó tại chỗ vòng lặp. Biến `mac_ref/mac_neo` vẫn là local của `lam`, được helper cập nhật theo dynamic scope Bash. Bản control giữ helper đúng. Bản `helper-after` định nghĩa lại helper ngay sau lời gọi `lam` đầu tiên bằng:

```bash
kiem_mac_dinh() {
  if printf '%s\n' "$@" | grep -q '^GIA_REF_STATE='; then mac_ref=0; fi
  if printf '%s\n' "$@" | grep -q '^NEO_TEP='; then mac_neo=0; fi
}
```

Output `--lan 3`: control **53/53, rc0**; helper xấu ngay từ trước lời gọi đầu **52/53, rc1**; helper chuyển xấu sau lời gọi đầu **53/53, rc0**. W4 không nhìn thấy helper đổi vì `declare -f lam` giữ nguyên; :190 gặp hash đã thấy và `return 0` trước khi stress. Biên nhận trap/seam vẫn khớp, W5 vẫn tới tổng kết. Đây là cùng vấn đề neo phép đo vào mã đang chạy, khác đường quote/trap đã được vá.

Đối chứng hành vi thật: chạy **toàn W5**, giữ mọi ca gốc, nối recorder `env` và lời gọi stress explicit +20.000 đối số ở cuối. Cả `helper-control` và `helper-after` đều chạy đủ **105/105, rc0** trước lời gọi thêm. Control chỉ in hai dòng `WITNESS:GIA_REF_STATE=explicit`, `WITNESS:NEO_TEP=explicit`; mutant in thêm `GIA_REF_STATE=…/refstate` và `NEO_TEP=…/neo_auto` phía sau. Vì giá trị phía sau thắng trong `env`, B1 đã thực sự tái xuất hiện, không phải lỗi giả chỉ do phá bộ đo.

**I1 — P2, `ops/do_sigpipe.sh:189–190`; slug `phep-do-khong-neo-ma-chay`. H1/G2 còn mở ở cấp lớp; lần thứ 4, cùng hình dạng** (F1 → G1/G2 → H1 → I1). Giới hạn executor khai về phá đồng thời trap và seam không bao gồm thay đổi dependency của thân hàm với observer nguyên vẹn. Không đếm lại H1/G2 thành finding mới riêng.

Bổ sung xác nhận: `python .../third.py confirm` → `confirm-helper-after` **53/53 DAT, rc0, 80,520s, --lan 10**. Kết quả không phụ thuộc chỉ một lần thử hoặc SIGPIPE ngẫu nhiên trên đối số ngắn; witness 20.000 đối số cho B1 thực vẫn như trên.

HƯỚNG 4 — H3 và an toàn ghi ngoài fixture

- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python tam/tmp.CEWbH0B0ZQ/safety.py`; log `logs/safety.json` và từng `safety-{present,absent,explicit}.{json,stdout,stderr}`. RUNNER_TEMP của caller nằm ngoài TMPDIR của W4, nhưng cả hai vẫn thuộc scratch do reviewer sở hữu.
- Cả ba ca **53/53, rc0**: tệp mặc định `RUNNER_TEMP/don_ref_neo.txt` đã có, chưa có và caller đặt `NEO_TEP` tường minh. Tệp có sẵn giữ đúng 30 byte, SHA256 `d90a2014f519386df97c789de10f5e13eec7c5d6f548f18d7a20876186b28509` và mtime; tệp chưa có vẫn không được tạo. Sentinel HOME giữ nguyên hash/mtime. TMPDIR sau mỗi run rỗng; HOME/RUNNER_TEMP không có tệp mới ngoài sentinel đã dựng.
- `/tmp/don_ref_neo.txt` thật vốn có sẵn: trước/sau cả ba ca đều 0 byte, mtime_ns `1790686536659291928`, SHA256 rỗng `e3b0c442…b855`. Không xóa hay sửa nó để mô phỏng ca chưa tồn tại; ca chưa tồn tại được đo trong RUNNER_TEMP riêng như H3 lượt 3.
- Phản chứng chốt cách ly: `python .../follow.py isolation_mut` gỡ riêng `env -i` ở driver B1 trên bản sao W4 → **52/53, rc1**, đúng `(e) B1/cach-ly-ghi` đỏ. Mọi đích của mutant này vẫn trong scratch; không chạy mutant bỏ RUNNER_TEMP/TMPDIR làm ghi vào `/tmp` thật.
- Quan sát inotify trên `/tmp` cấp đầu và **5.449 thư mục HOME thật** trong thời gian đo: các sự kiện chỉ thuộc log/state của hạ tầng phiên (`claude-code.log`, log session và SQLite của Codex). Không thấy sự kiện trên tệp mặc định của W5. Inotify không kèm PID nên không quy toàn bộ sự kiện hệ thống cho W4 hoặc coi chúng là bằng chứng W4 không thể ghi bất cứ đâu.
- `strace -f -e trace=file,network -o <scratch>/logs/strace-probe.trace true` → rc1, `PTRACE_TRACEME: Operation not permitted`. **KHÔNG ĐO ĐƯỢC audit syscall toàn cục** hoặc mọi hành vi ghi rồi hoàn nguyên. Snapshot sạch và observer trên các thư mục nêu trên chỉ chứng minh phạm vi đã quan sát; sandbox thực là workspace-write, không phải syscall sandbox riêng của W4.
- **H3 ĐÃ VÁ THẬT trong các đường đã đo; KHÔNG PHẢI LỖI mới.** Không dùng inotify hoặc số 53/53 thay cho chứng minh tuyệt đối mọi đường ghi/mạng.

HƯỚNG 5 — Hồi quy head/nền và delta

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python tam/tmp.CEWbH0B0ZQ/measure.py initial`; `.../measure.py regressions`; `.../follow.py compare`; `.../follow.py versions`. Các argv thật lưu trong `logs/<case>.json`; mỗi lệnh chạy tại bản sao đầy đủ `head/` hoặc `base/`. Git fixture ghim `commit.gpgsign=false` và `core.abbrev=7` qua môi trường, không sửa config nguồn.

| Phép đo | Head | Nền / từng điểm về nền | Kết luận |
|---|---|---|---|
| W4 `--lan 10` | 53/53, rc0, 26,144s | 49/53, rc1, 29,831s; ba `(d)` `rc0=0 rc141=10 khac=0`, B1 khớp đầu sai10/10 | A1 đo cơ bản đúng |
| Chỉ W1/W2/W3/W5 về nền | — | W1=52/53; W2=52/53; W3=51/53; W5=52/53; đều rc1 | Đúng điểm đích đỏ; W3 còn một ca ngắn đỏ141 như ghi chú dưới |
| `bash ops/don_ref_chot_test.sh` | 105/105, rc0, 2,832s | 105/105, rc0, 2,994s | Không mất ca; stdout 5.314 byte giống hệt |
| `python ops/bash_nen.py quet --root .` | DAT, rc0, 19,692s | DAT, rc0, 19,786s | Delta0; stdout 41 byte giống hệt |
| `python .claude/dev/ci_dang_ky_test.py` | TỔNG: ĐẠT, rc0, 7,622s | TỔNG: ĐẠT, rc0, 7,417s | Delta0; stdout 54.062 byte giống hệt |
| `actionlint .github/workflows/*.yml` có ShellCheck | rc1, SC1003 tại ops-don-ref.yml:117 | Cùng lỗi, stdout 224 byte giống hệt | Lỗi nền, **KHÔNG PHẢI LỖI packet** |
| `shellcheck --format=json W1 W2 W3 W5 [W4 trên head]` | rc1, SC1090 tại cai_cong_cu.sh:54 | Cùng lỗi, JSON 216 byte giống hệt | Delta0; W4 không thêm lỗi |
| `bash -n ops/*.sh` (từng tệp) | 8/8 rc0 | 7/7 rc0 | W4 là tệp mới |

Môi trường đã đo: Bash5.2.21, Python3.11.15, Git2.43.0, actionlint1.7.7, ShellCheck0.11.0. ShellCheck sao chép binary có sẵn của lượt 3 vào scratch; không tải/cài qua mạng. Số thời gian của các run có thể chịu ảnh hưởng các bộ test chạy đồng thời; không dùng làm benchmark.

Không giấu lần đỏ ngoài dự kiến: mutant chỉ W3 về nền có thêm `(a) dung_goi_review/crlf trich rc=141`, nên51/53 thay vì52/53. Chính phép gán nền dùng pipeline cũ, đầu vào ngắn vẫn có race; `(d)` W3 vẫn141/10 lần. Đây là thêm biểu hiện lỗi baseline, không phải hồi quy head hay xanh giả. Hai lượt witness head/builtin-trap và witness helper-before từng dừng ở104/105 vì ca tag của CHỐT (trước mọi `lam`); không dùng các run chưa tới recorder ấy để chứng minh I1. Các cặp control/helper-after dùng làm I1 đã105/105 và có output stress dương.

HƯỚNG 6 — Đối chiếu bảng executor bằng phép đo

Lệnh/nguồn: `git -C cay-kho log -1 --format=%B`; `measure.py w5_variants/scoring/deps`, `follow.py isolation_mut`, `safety.py`, `third.py helpers/confirm` như các hướng trên. Không coi bảng executor là danh sách bao phủ đầy đủ.

| Dòng executor khai | Đo độc lập lượt 4 | Đánh giá |
|---|---|---|
| Quote, `$L`, subshell vẫn bắt redef baseline | `h1-quoted-calls`, `h1-dollar-calls`, `h1-subshell-calls`:52/53 rc1; case subshell219,414s | Khớp các biến thể đã chạy; không tự ghi8/8 khi chưa chạy đủ8 |
| Redef trước/sau; redef y hệt vẫn xanh | Trước/sau52/53; same-redef53/53 | Khớp; cache chỉ xét `lam`, chưa đủ cho helper-after I1 |
| Gỡ DEBUG qua builtin ⇒ không đo được | `trap=1 seam=24`, rc2 | Khớp phản chứng H1 cũ |
| Lách seam qua `command env` ⇒ không đo được | `h1-seam-command`:rc2, trap24/seam0 | Đúng fail-close. Reviewer thay seam từ đầu nên0; bảng thay sau ca đầu nên1; không gọi khác bộ đếm này là lời khai sai |
| W5 thoát sớm ⇒ không đo được | `h1-early-exit`:rc2, thiếu dòng tổng kết | Khớp |
| Predicate(d), nhánh ghi0, ghi(d) luôn đạt, B1 luôn đạt | Lần lượt50/53,50/53,50/53,52/53; rc1; các `(c)` đích đỏ | Khớp; H2 :174/:175 cũ nay ở :167/:168; B1 ở :227 |
| `ghi` toàn cục luôn đạt vẫn bị SAI chặn | Head lẫn W1 nền đều rc1; tổng bị mutant làm53/53 nhưng ghi rõ CO PHEP DO ĐỎ | Khớp; không còn CON rẽ trước đường cấp điểm |
| Bỏ env-i bị chốt cách ly bắt |52/53 rc1, đúng B1/cach-ly-ghi | Khớp; không chạy biến thể có thể ghi `/tmp` thật |
| Sentinel head đã có/chưa có giữ nguyên | Ba ca ở HƯỚNG4 đều53/53, hash/mtime giữ nguyên hoặc tệp vẫn vắng | Khớp trong phạm vi quan sát |
| cksum hỏng từ 0/1/2/5 ⇒rc2 |4/4 rc2, tên cksum và KHÔNG ĐO ĐƯỢC | Khớp |
| Không chặn phá đồng thời trap+seam | `h1-declared-double`: builtin-trap-off + body baseline dùng command-env sau ca đầu ⇒ **53/53 rc0** | Giới hạn khai là thật; phân loại dưới đây |
| “Mọi đường” quan sát mã sống | Helper-after giữ nguyên hash của `lam` nhưng helper đổi ⇒ **53/53 rc0**, B1 tái hiện thật | Bảng còn thiếu đường I1; không dùng tên bảng như bảo đảm vét cạn |

Giới hạn **đã khai** không tự thành P2. Với `declared-double`, chính mutant đồng thời tắt hai cơ chế đo nằm cùng tiến trình Bash; head/nền nguyên vẹn vẫn có kết quả đúng và các phá đơn lẻ fail-close. Theo yêu cầu phân biệt của prompt/spec§4–§5, ghi **KHÔNG PHẢI LỖI mới độc lập** cho kịch bản cố ý phá công cụ đo này. Không có luận cứ rằng Bash source có thể chống mọi script chủ động phá driver. Ngược lại I1 chỉ sửa logic W5 và một hàm phụ, không biết/tắt/ghi vào biến, trap, seam hoặc file biên nhận của driver; đó là hồi quy sản phẩm lọt qua khóa, đủ P2.

Các mục “gọi lam bằng đường tuyệt đối”, toàn bộ biến thể PATH caller, và mọi cặp gỡ chốt phối hợp trong bảng: **KHÔNG ĐO ĐƯỢC đầy đủ trong lượt này**; không xác nhận bằng suy luận hay gán P2 chỉ vì executor khai giới hạn. Việc self-check có các chốt chồng nhau không phải lỗi khi các mutant hợp đồng F3 đã bị từ chối. “PATH chỉ đọc” không được hiểu thành sandbox ngăn binary độc hại; phép đo sử dụng toolchain cục bộ có sẵn, wrapper công cụ hỏng chỉ trên bản sao có chủ đích.

HƯỚNG 7 — ĐỐI CHIẾU F/B/G/H, từng finding và lớp

Lệnh: `python .../measure.py old`, `.../follow.py dependencies`, các lệnh H1–H4 và witness ở trên. Log `old.jsonl`, `g3.jsonl`, mỗi mutant/argv/rc/output được giữ. `seq -f` hỏng ⇒ head 53/53, chỉ W5 nền 52/53; awk hỏng hoặc trả ít dòng đều rc2, tên producer/số dòng.

| Finding cũ | Kết quả lần này | Trạng thái |
|---|---|---|
| F1 | unused-function và here-doc: 51/53 rc1; không chạy được LENH, `(d)` và `(c)` đều từ chối | ĐÃ VÁ THẬT cho hai đường W1; lớp neo mã chạy còn I1 |
| F2 | Thiếu riêng W1/W2/W3/W5: rc2, KHÔNG ĐO ĐƯỢC và đúng tên tệp | ĐÃ VÁ THẬT, đóng |
| F3 | :155/:174/:175 cũ cùng nhánh B1 luôn đúng đều bị self-check từ chối | ĐÃ VÁ THẬT trong phạm vi khóa đã đo; H2 đóng |
| B1 | W5 head/control giữ explicit với 20.000 đối số; chỉ W5 nền: 52/53; suite 105/105 hai cây | ĐÃ VÁ THẬT hành vi W5 head; khóa hồi quy còn I1 |
| G1 | Thêm pipeline nền sau cả ba dòng vá: 50/53, rc1, ba `(d)` rc141; exit-after/overwrite-after cũng đỏ | ĐÃ VÁ THẬT, đóng đường cắt đuôi W1–W3 |
| G2 | Dead-lam/head here-doc + living baseline: 52/53; redef trực tiếp bị bắt | VÁ HỜ ở cấp lớp: I1 còn đường helper đổi sau ca đầu |
| G3 | Phá seq-f không còn xóa payload; awk lỗi/ngắn đều rc2 | ĐÃ VÁ THẬT, đóng |
| G4 | Predicate trong helper, callsite ghi điểm, predicate B1 và nhánh ghi cha đều bị bắt | ĐÃ VÁ THẬT, cùng F3/H2 |
| H1 | Quote, builtin-trap, redef trước/sau đã chặn; helper-after vẫn xanh giả | VÁ HỜ ở cấp lớp; còn I1, **lần thứ 4, cùng hình dạng** |
| H2 | Self-check chạy lại đường ghi thật trong subshell, các predicate/ghi luôn đúng đều đỏ; cờ SAI giữ rc1 khi DAT bị phá | ĐÃ VÁ THẬT, đóng theo phạm vi đo |
| H3 | Đã có/chưa có/NEO_TEP explicit giữ sentinel; gỡ env-i đỏ | ĐÃ VÁ THẬT, đóng đường rò ghi đã biết; giới hạn audit ở HƯỚNG 4 |
| H4 | cksum127 từ probe/ca đầu/ca sau ⇒ rc2 có tên công cụ | ĐÃ VÁ THẬT, đóng |
| Corpus glob | Đúng mutant `LENH="${LENH//\*/}"`: 50/53 rc1, ba đầu vào glob đỏ | ĐÃ VÁ THẬT, đóng |

Không gộp thành nhiều finding mới: lớp `phep-do-khong-neo-ma-chay` có đúng một biểu hiện còn mở I1/P2; các lớp `tu-kiem-bo-qua-cap-diem` (F3/G4/H2), `fixture-khong-co-lap-ghi` (H3), `loi-cong-cu-mat-chan-doan` (H4) không tìm thấy biểu hiện còn mở trong phép đo lần này. Bảng không chứng nhận các đường KHÔNG ĐO ĐƯỢC là đã kiểm.

HƯỚNG 8 — Finding mới, hướng vá và tác động trần

| ID | Hạng / vị trí | Hậu quả đã đo | Gợi ý trong write set / khóa / rủi ro / trần |
|---|---|---|---|
| I1 | **P2**, W4 `ops/do_sigpipe.sh:189–190`; `phep-do-khong-neo-ma-chay` | Chỉ băm thân `lam`, cache đã thấy bỏ qua dependency thay đổi. W4 vẫn 53/53 `--lan 10`; W5 mutant thực thêm fallback sau explicit +20.000 đối số. Không sửa observer. | **Ở đâu/cách:** thay cache tại W4, đo lại ở mỗi lần vào `lam`, hoặc từ chối ngữ cảnh có dependency/trạng thái không được chứng minh. Không chỉ thêm hash cho đúng tên helper của reviewer. **Khóa:** helper-control xanh, helper xấu trước/sau ca đầu đều đỏ hoặc rc2; giữ quote/builtin-trap/redef, cksum, H2/H3 và từng điểm baseline. **Rủi ro:** chi phí stress tăng theo số lần gọi; thực thi lặp có thể đổi fixture, nên giữ bảo vệ chống reentry và cô lập side effect. **Trần:** đối chứng loại cache dưới đây giảm 1 dòng, từ 298 còn 297; không cần mở write set/trần. Bản triển khai cuối cần tự đo lại toàn gate và hiệu năng. |

Đối chứng hướng vá, **“chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit”**: `python .../third.py confirm` dựng `w4-probe-each-call.sh` bằng cách bỏ dòng :190 và bỏ khởi tạo `B_SEEN`, giữ checksum/biên nhận/lỗi công cụ. Chạy `--lan 1`: head **53/53 rc0**, 89,623s; helper-after **52/53 rc1**, 80,504s, B1 explicit sai **23/24** lần gọi sống. Tệp đối chứng 284 dòng so 285 của W4 head; `logs/hint-line-budget.json` ghi tổng W1–W5 giả định 297. Đây là bằng chứng hướng sửa có răng và không vượt trần, không phải bản vá sản phẩm hoặc chứng nhận đầy đủ hiệu năng ở mặc định 10 lần. Chú thích “body” và chính sách đo cần chỉnh lại nếu executor chọn bỏ cache.

HƯỚNG 9 — Hoàn tất bộ dài, giới hạn và nghiệm thu

- `python ops/lease_publish_test.py` qua `measure.py regressions`: head **187/187, đã chạy 187, bỏ qua 0, rc0, 548,348s**; nền **187/187, đã chạy 187, bỏ qua 0, rc0, 555,739s**. A6 delta lỗi 0; log đầy đủ `head-lease.*`, `base-lease.*`.
- `TMPDIR=<scratch>/temp RUNNER_TEMP=<scratch>/temp HOME=<scratch>/home PYTHONDONTWRITEBYTECODE=1 python <scratch>/t5_repeat.py`: cả head/nền **200/200**, mọi rc0, **rc141=0**, từng run có JSON DAT/1.7.7; thời gian 83,795s/47,157s. Gói offline 1.7.7, PATH có bản sai 9.9.9; không tải công cụ. Log `t5-repeat.jsonl`. Nền không gặp race trong 200 lần này không phủ định phản chứng 20.000 dòng của W4.
- Lần xác nhận witness sau flake: `follow.py witness_retry` cho head 105/105 rồi chỉ hai explicit; `witness-builtin-retry-1.json` cho builtin-trap 105/105 rồi explicit kèm hai fallback. Không dùng các lần flake 104/105 trước đó làm bằng chứng hợp lệ.
- `python ops/cong_cu_test.py` đầy đủ: **not_run / KHÔNG ĐO ĐƯỢC** trong lượt 4; đây là mục “nếu kịp” của prompt. Không dùng kết quả phần đầu hoặc 212 đột biến chưa hoàn tất ở lượt 3 để chứng nhận A2 lần này. Phần t5 đã đo riêng không thay thế toàn suite.
- Bare Ruff lint: **not_run / KHÔNG ĐO ĐƯỢC**; packet không sửa Python. Không gọi bash_nen/đăng ký CI là “Ruff passed”. W1–W3/W5 không đổi từ lượt 3 (`git diff 5138faa..HEAD -- <bốn tệp>` rỗng); lượt này chạy các ca W4, W5 và t5 đã nêu, không tự khai đã chạy lại 5.436 so sánh giá trị của lượt trước.
- **0 P1 / 1 P2 / 0 P3; một lớp/một biểu hiện còn mở.** Không thấy sai hành vi mới trong W1–W3/W5 head; I1 là sức bắt hồi quy của W4. A1 phép đo head/nền đạt nhưng khóa neo mã chạy chưa đạt I1; A3/A4/A6 delta 0 trên các bộ đã chạy; A2 toàn suite chưa chứng nhận; A5 chưa đạt 0/0/0.
- **verdict: changes_requested**. Vì **lần thứ 4, cùng hình dạng**, chuyển điều phối về checkpoint chủ kho theo S3 và chỉ thị lượt 4; không tự tiếp tục một vòng sửa/review nữa. Không approve/merge/push/đăng GitHub.

HƯỚNG 10 — Neo cuối, hiện vật và dọn thử nghiệm

- Lệnh `measure.py anchors` và các argv tại `logs/{anchor-*,final-*}.json`: SHA/tree hai cây và hash SPEC giữ nguyên; `git status --porcelain --untracked-files=all --ignored` rỗng trên cả hai nguồn; `git diff 89fc4fa..HEAD --check` rc0; numstat vẫn **298 dòng thêm W1–W5**. Hai nguồn không có thay đổi được quan sát ở mốc cuối.
- `shellcheck --format=json <scratch>/w4-probe-each-call.sh` → rc0, `[]`; `bash -n` đối chứng này → rc0. Đây chỉ là kiểm cú pháp/lint của hiện vật hướng sửa, không thay nghiệm thu bản vá sản phẩm.
- `bash tam/tmp.CEWbH0B0ZQ/cleanup.sh` dùng EXIT trap dọn **chỉ** `<scratch>/temp/`: trước 103 mục cấp đầu/390 mục tổng, sau 0. Giữ bản sao đầy đủ, mã mutant, sentinel an toàn và log để tái lập; không xóa tệp caller hay `/tmp/don_ref_neo.txt` thật. Nhật ký `logs/cleanup.json`.
- `evidence.sha256` băm các harness, nguồn mutant W1–W5 và log; `logs/verdict-artifact.json` ghi đường dẫn/kích thước/hash của bản verdict hoàn tất. Không có commit hoặc thao tác ghi lên GitHub trong lượt này.
