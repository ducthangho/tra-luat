# Cross-review độc lập — packet #675 r2 g2 — lượt 3
verdict: changes_requested
reviewed_sha: 5138faae91d2e9fb0fa36be8137326afb8f526a8
reviewed_tree: c9171fd133ce1224aefe44fa3b681ca3ab9a84ca
baseline_sha: cd23c7dbc7833d64a8e87e8ffd94f194c18e0060

Kết luận: **changes_requested — 1 P1 / 2 P2 / 1 P3**. P1 là W4 head làm rỗng tệp ngoài fixture; hai khóa hồi quy còn đường xanh giả. Chi tiết, lệnh, output và phần KHÔNG ĐO ĐƯỢC ở dưới.

Provider: OpenAI. Bề mặt quan sát: Codex qua API với công cụ shell cục bộ; transport: machine/tool trực tiếp. Model: GPT-6 theo chỉ dẫn phiên (tự khai); biến thể/effort/attestation runtime độc lập: **KHÔNG ĐO ĐƯỢC**. Không suy danh tính từ actor GitHub. Executor theo vật liệu: Claude Sonnet 5.5; chưa có attestation độc lập của executor.

Chỉ đọc hai cây nguồn; mọi thử nghiệm/đột biến trong bản sao `tam/tmp.mtrFTlLP7L/`, được tạo bằng `mktemp -d -p "$PWD/tam"`. Không sửa sản phẩm, không push, không đăng GitHub. Ngưỡng theo prompt: approved chỉ khi 0 P1 / 0 P2 / 0 P3. Chỉ thị trực tiếp cho lượt 3 là authority của review này; không tự thực hiện thêm vòng sửa/review hay land.

HƯỚNG 1 — Neo nguồn, SPEC, write set

- Lệnh và output đầy đủ: `tam/tmp.mtrFTlLP7L/logs/anchors-start.json` (từng argv, rc, stdout/stderr).
- `git -C cay-kho rev-parse HEAD HEAD^{tree}` → SHA/tree như trên; `git -C cay-nen rev-parse HEAD` → đúng baseline; `sha256sum SPEC.md` → `81fb6d533a892ec33c9b6b3f161dc1eca971579f4acfdb277c26521539be71cc`.
- `git -C cay-kho diff 89fc4fa..HEAD --name-only` → chỉ W1–W5. `git diff cd23c7d..HEAD --numstat` trên năm tệp: W1 3/1, W2 2/1, W3 2/1, W4 281/0, W5 6/2; tổng **294 dòng thêm ≤300**. Từ `1ea9c1c` chỉ đổi W4. Cả hai `status --porcelain --untracked-files=all --ignored` rỗng, rc0.
- **KHÔNG PHẢI LỖI** về neo/phạm vi. Diff từ baseline còn các tệp merge master; không tính chúng là sửa packet. Đọc đầy đủ prompt.snapshot, SPEC và hai verdict trước; bảng đường đo bên dưới do reviewer dựng lại, không lấy bảng executor làm trần.



HƯỚNG 2 — W4 và từng điểm nền (đã hoàn tất phần dưới)

- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python tam/tmp.mtrFTlLP7L/measure.py mutations`; hàm `w4()` gọi `bash <bản-sao-head>/ops/do_sigpipe.sh --goc <bản-sao-đầy-đủ> --lan 10`. Log: `logs/mutations.jsonl`, từng `w4-*.stdout/.stderr/.json`.
- Harness dùng subprocess khôi phục SIGPIPE mặc định, TMPDIR riêng dưới scratch; cấu hình Git chỉ qua env (`commit.gpgsign=false`, `core.abbrev=7`). Không chạy W4 trực tiếp trong shell thừa kế tín hiệu bị bỏ qua rồi gọi rc=1 đó là SIGPIPE.
- Head: **53/53 DAT**, rc0, 27,648s. Nền: **49/53**, rc1, 25,901s; ba điểm `(d)` đều `rc0=0 rc141=10 khac=0`, B1 khớp đầu đỏ. Đổi riêng W1/W2/W3 về nền: từng bản **52/53**, rc1, đúng điểm tương ứng đỏ.
- **KHÔNG PHẢI LỖI** về các phép nền này. 53 = 3 × (14 đầu vào biểu thức + 1 phép chạy toàn tệp + 1 tự kiểm) + 4 phép B1 + 1 tự kiểm B1. Chỉ ghi số ca không thay chứng minh từng đường.

HƯỚNG 3 — Hồi quy đã hoàn tất, delta head/nền

- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python tam/tmp.mtrFTlLP7L/measure.py regressions`; từng argv, cwd, rc, thời gian và output trong `logs/{head,base}-*.json/.stdout/.stderr`. ShellCheck 0.11.0 lấy từ binary có sẵn của review trước, sao chép vào scratch; không tải/cài qua mạng.

| Lệnh | Head | Nền | Kết luận |
|---|---|---|---|
| `bash ops/don_ref_chot_test.sh` | 105/105, rc0, 2,534s | 105/105, rc0, 2,681s | Không mất ca |
| `python ops/bash_nen.py quet --root .` | DAT, rc0, 20,752s | DAT, rc0, 20,335s | Delta 0 |
| `python .claude/dev/ci_dang_ky_test.py` | TỔNG: ĐẠT, rc0, 7,155s | TỔNG: ĐẠT, rc0, 7,055s | Delta 0 |
| `actionlint .github/workflows/*.yml` có ShellCheck | rc1, SC1003 tại ops-don-ref.yml:117 | Cùng lỗi | Lỗi nền, KHÔNG PHẢI LỖI packet |
| `shellcheck --format=json W1 W2 W3 W5 [W4 trên head]` | rc1, SC1090 tại cai_cong_cu.sh:54 | Cùng lỗi | Lỗi nền, W4 không thêm lỗi |

`lease_publish_test.py` đã hoàn tất; kết quả187/187 ở HƯỚNG 10.

HƯỚNG 4 — Đường thứ ba của G2: lối gọi hàm và tuổi thọ DEBUG trap

- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python tam/tmp.mtrFTlLP7L/third.py w5_variants` (lượt sửa harness: `logs/third-w5-v2.jsonl`), `python tam/tmp.mtrFTlLP7L/audit.py witness`, `python tam/tmp.mtrFTlLP7L/follow_checks.py confirm`. Tất cả nguồn mutant, stdout/stderr/rc được giữ dưới scratch.
- Hai mutant giữ ca `lam "thử khô: ..."` đầu tiên của W5 nguyên vẹn, rồi định nghĩa lại bằng nguyên hàm baseline `lam () { ... }`:
  1. Chèn `builtin trap - DEBUG` trước lần định nghĩa lại, giữ các lời gọi sau nguyên dạng.
  2. Không đụng trap; đổi các lời gọi sau từ `lam ...` thành `"lam" ...` — Bash vẫn gọi chính hàm `lam`.
- Output ban đầu `--lan 1`: cả hai **53/53 DAT, rc0**. Đối chứng chỉ định nghĩa lại, không gỡ trap/đổi cách gọi → **52/53, rc1**, đúng `(e) B1/lam-bi-dinh-nghia-lai`; `trap - DEBUG` thông thường cũng bị bắt; thay space bằng tab vẫn bị bắt. Không quy chụp mọi DEBUG trap đều vô dụng.
- Chạy TOÀN BỘ W5 mutant với recorder tại biên `env`, thêm lời gọi stress 20.000 đối số **sau** các ca gốc: cả hai mutant ghi explicit rồi thêm `GIA_REF_STATE=.../refstate` và `NEO_TEP=.../neo_auto`; head chỉ có hai dòng explicit. Log: `witness-{trap-builtin-off,quoted-calls}.stdout`, `confirm-witness-head.stdout`.
- Xác nhận lại bằng `follow_checks.py confirm`, **--lan 10**: quoted-calls53/53 rc0 (45,217s), builtin-trap-off53/53 rc0 (44,194s); witness head và cả hai mutant đều105/105 rồi mới chạy stress. Head chỉ hai dòng explicit, mutant thêm hai fallback.
- Cơ chế ở W4:197–202: chỉ nhận dạng chuỗi `BASH_COMMAND` bắt đầu bằng `lam `; `"lam" ...` không khớp. Hàm mang tên `trap` không chặn được `builtin trap`; không có biên nhận hoàn tất/kiểm tra trap còn sống sau `source`. Kết quả stress lấy từ lần đầu vẫn đủ điều kiện cấp điểm.
- **H1 — P2, G2 còn mở ở cấp lớp.** Đã bỏ trích văn bản nhưng vẫn chứng minh một tập con do hình thức câu lệnh quyết định. Lời commit “W5 không gỡ được trap” sai qua phép đo. `"lam"` còn cho thấy đường lọt không cần can thiệp công cụ đo. Đây là cùng hình dạng **vá hẹp tính gắn với mã chạy** qua F1 → G1/G2 → H1; không coi việc chặn đúng mutant cũ là đóng cả lớp.
- Giới hạn harness: lượt `third-w5.jsonl` đầu nhận nhầm dòng Python `lam = ...` trong here-doc làm điểm chèn; các ca đó lỗi dựng mutant, **không dùng làm finding**. Lượt v2 neo đúng lời gọi Bash `^lam "` và có W5 chạy thật/recorder. Một lượt W5 chứng kiến lỗi tag ở bước chốt trước mọi `lam`, ghi riêng ở hướng giới hạn hồi quy; không dùng lỗi đó chứng minh H1.

HƯỚNG 5 — Đường thứ ba của F3/G4: nhánh cấp điểm cha vẫn không được tự kiểm chạy qua

- Lệnh: `python tam/tmp.mtrFTlLP7L/third.py scoring`, rồi `python tam/tmp.mtrFTlLP7L/score_target.py`; log `third-score*.jsonl` và các `third-score-*.stdout/.json`.
- Đổi đúng predicate W4:155 từ `if [ "$1" -eq 0 ]; then DAT=$((DAT + 1));` thành `if true; then DAT=$((DAT + 1));` → head **53/53**, nền cả bốn điểm **53/53**, rc0. Không đổi tổng kết cuối, không đổi số ca.
- Để loại phản biện “đã vô hiệu hóa cả báo cáo tự kiểm”, mutant hẹp hơn chỉ cấp điểm vô điều kiện cho nhãn **(d)**:
  `if [ "$1" -eq 0 ] || [[ "$2" == "(d) "* ]]; then DAT=$((DAT + 1));`
  Các nhãn `(c)`, `(e)`, `(a)` giữ nguyên cách chấm. W4 này trên bản sao chỉ W1 về nền, `--lan 10`, vẫn **53/53 DAT, rc0** (`third-score-d-parent-basew1.stdout`), trong khi W4 thật là **52/53**, W1 `rc141=10`.
- Cơ chế: `tu_kiem()` đặt `CON=1`; `ghi()` dùng nhánh :150–152 ghi CON_DO rồi **return trước :155**. Vì vậy tự kiểm không đi qua nhánh thực sự thêm điểm DAT của phép (d). Việc đổi predicate :174 hoặc đổi `ghi 1` tại :175 có bị bắt không giải quyết đường :155.
- **H2 — P2, F3/G4 VÁ HỜ ở cấp lớp**, cùng hình dạng lần thứ ba: nhánh cấp điểm đã chuyển chỗ, nhưng đường tự kiểm vẫn rẽ trước nhánh ấy. Hai mutant cũ được chặn; hợp đồng “đổi nhánh cấp điểm luôn đúng ⇒ (c) đỏ” chưa khép.

HƯỚNG 6 — Fixture ghi ngoài thư mục sở hữu và để lại tệp

- Lệnh: `python tam/tmp.mtrFTlLP7L/leak.py`; log `leak-evidence.json`, `leak-runner-temp.stdout/.json`. Reviewer tạo riêng `leak-outside-w4/don_ref_neo.txt` trong scratch, đặt RUNNER_TEMP tới thư mục đó, còn TMPDIR của W4 ở `temp/leak-runner-temp/`.
- Output: W4 **53/53, rc0**. Sentinel từ **27 byte** (SHA256 `c74fbb7e2e8c628cfc08645cd8bee656b9f72e517357fcbbb99b9a37d117c4a0`) thành **0 byte** (SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`); W4 đã dọn thư mục riêng nhưng tệp ngoài ấy còn lại.
- W4:208 gọi B1 driver với môi trường caller. `source` W5 thực thi cả bước CHỐT trước `lam`; workflow được W5 trích có `NEO_TEP="${NEO_TEP:-${RUNNER_TEMP:-/tmp}/don_ref_neo.txt}"; : > "$NEO_TEP"`. TMPDIR không bảo vệ đường này. Không có RUNNER_TEMP/NEO_TEP thì đích là **`/tmp/don_ref_neo.txt`**; tệp ấy có sẵn trong môi trường, mtime thay đổi trong loạt thử dù danh sách tên `/tmp` không thêm phần tử. Không ghi sentinel của reviewer vào tệp có sẵn đó, không xóa nó.
- Đối chứng chỉ trên bản sao W4: thay lời gọi tại :208 thành `RUNNER_TEMP="$TMP" NEO_TEP="$TMP/b1.neo" bash -c ...`; `python .../follow_checks.py leak_control` → vẫn **53/53, rc0**, sentinel ngoài giữ nguyên SHA256, TMP riêng sạch. Đây là phép kiểm định hướng sửa, không phải sửa sản phẩm hay chứng nhận mọi đường ghi.
- **H3 — P1, sai hành vi trên head nguyên vẹn: W4 mới chạy toàn W5 nhưng không cô lập đích ghi của nó.** Trái yêu cầu fixture chỉ ghi trong cây tạm của phép đo; có thể làm rỗng tệp caller và không dọn tệp mặc định. Lỗi W5 có sẵn là nguồn đường ghi, nhưng W4 trước không chạy toàn suite nên chưa kéo đường ghi đó vào phép đo này.

HƯỚNG 7 — Công cụ/producer và giới hạn chẩn đoán

- Lệnh: `python tam/tmp.mtrFTlLP7L/third.py deps`, log `third-deps.jsonl` và wrapper ở `deps/`; phép G3 nguyên dạng `seq -f` nằm trong `measure.py mutations`.
- `awk` trả127 → rc2, KHÔNG ĐO ĐƯỢC producer; `awk` trả0 nhưng không in gì → rc2 vì thiếu dòng; `sha256sum` trả127 → rc2, KHÔNG ĐO ĐƯỢC băm; `python3` trả127 → rc2, W5 không tới ca lam. **KHÔNG PHẢI LỖI** xanh giả của các đường này. PAD mới được dựng bằng Bash và kiểm số phần tử, không còn nuốt lỗi process substitution của seq.
- Riêng wrapper `cksum` trả127: W4 **50/53, rc1**, stdout chấm lỗi số lần B1, stderr ngoài rỗng; không có “KHÔNG ĐO ĐƯỢC”. Công cụ tạo dấu vân tay hàm tại :198 hỏng nhưng rc bị bỏ qua; h rỗng làm driver stress lại nhiều lần. **H4 — P3**, lỗi chẩn đoán/rc của fixture, vẫn fail-close, không phải xanh giả. Lời chú thích “công cụ hỏng ⇒ rc2” rộng hơn hành vi. Không đếm H4 như một B1 sai hành vi.
- Wrapper `actionlint` trả127 vẫn **53/53, rc0**. **KHÔNG PHẢI LỖI của phép B1 tự nó**: actionlint nằm ở kiểm YAML cuối W5, không tạo payload hay quyết định dò đối số. Điều này giới hạn lời “chạy toàn tệp”: W4 không chứng nhận toàn suite W5 đạt; suite W5 được đo riêng ở HƯỚNG 3. Không lấy 53/53 thay 105/105 hay coi lời khai “mọi công cụ” là chứng minh.

HƯỚNG 8 — Chạy lại đúng phản chứng cũ và đối chiếu từng finding

Lệnh: `python tam/tmp.mtrFTlLP7L/measure.py mutations`; tổng hợp không mất output tại `logs/old-counterexamples-summary.json`. Tất cả ca thường `--lan 10`; ca thiếu tệp `--lan 1` vì dừng ở preflight.

| Finding cũ | Phản chứng chạy lại trên head lượt 3 | Trạng thái kết luận |
|---|---|---|
| F1 (lượt1) | Bọc LENH vào hàm không gọi; bọc vào here-doc: từng mutant **51/53, rc1**. (d) thất bại vì script thật không có LENH; (c) cũng từ chối lý do không phải141. | **ĐÃ VÁ THẬT cho đường W1–W3**, cùng G1. Lớp rộng “đo đúng mã đang chạy” còn G2/H1; không coi đóng toàn lớp. |
| F2 (lượt1) | Xóa riêng W1/W2/W3/W5: từng ca **rc2 + KHÔNG ĐO ĐƯỢC**, nêu đúng tệp, không tổng kết xanh. | **ĐÃ VÁ THẬT, đóng**. H4 là lỗi công cụ khác, không mở lại lỗi thiếu tệp. |
| F3 (lượt1) | Đổi điều kiện chấm :174 thành `if true`: **50/53, rc1**, cả ba (c) đỏ; đổi nhánh cấp `ghi 1` :175 thành `ghi 0` cũng **50/53**. | **VÁ HỜ ở cấp lớp**, còn H2 tại nhánh cấp điểm :155. |
| B1 (lượt1) | W5 head giữ explicit mỗi biến đúng một lần với20.000 đối số; W5 nền thêm fallback; chỉ thay W5 về nền → **52/53**, khớp-đầu sai10/10. W5 suite cùng105/105. | **ĐÃ VÁ THẬT trong W5, đóng lỗi hành vi gốc**. Khóa hồi quy còn H1. |
| G1 (lượt2) | Sau mỗi dòng vá thêm đúng `:; <phép gán pipeline baseline>`; cả ba trong cùng mutant → **50/53**, từng (d) `rc141=10/10`. `exit 0` và `export LENH=false` sau dòng đều **52/53, rc1**. | **ĐÃ VÁ THẬT, đóng đường cắt đuôi W1–W3**. Không còn “head -n tới dòng vá” trong phép(d). |
| G2 (lượt2) | Here-doc chứa hàm head + hàm baseline `lam ()` sống: **52/53, rc1**, B1 khớp-đầu sai10/10. Định nghĩa lại sau ca đầu theo cách gọi thường cũng đỏ. | **VÁ HỜ ở cấp lớp**, còn H1 qua tên hàm có quote và gỡ trap bằng builtin. |
| G3 (lượt2) | Wrapper chỉ phá `seq -f`: head **53/53**; W5 nền **52/53**, B1 vẫn sai10/10. Producer awk hỏng/ngắn đều rc2. | **ĐÃ VÁ THẬT, đóng lỗi payload mất âm thầm**. PAD không còn phụ thuộc seq; H4 không phải payload rỗng lọt xanh. |
| G4 (lượt2) | Hai đường :174/:175 chấm sai bị (c) bắt; riêng chốt (e) :220 luôn đúng → **52/53**, (c) B1 đỏ. | **VÁ HỜ ở cấp lớp**, H2 cho thấy (c) vẫn bỏ qua nhánh cấp điểm cha. |
| Corpus glob | Đúng mutant `; LENH="${LENH//\*/}"` → **50/53, rc1**, đúng3 đầu vào glob đỏ. | **ĐÃ VÁ THẬT, đóng**. |

Bảng lớp giữ lịch sử, không đếm một biểu hiện thành hai finding mới:

| Slug lớp dùng để đối chiếu | Nguồn/lịch sử | Biểu hiện còn mở lượt 3 | Cách đóng chung |
|---|---|---|---|
| `phep-do-khong-neo-ma-chay` | F1@41d03d8 → G1/G2@1ea9c1c | H1 P2; G1 riêng đã đóng | Quan sát lời gọi/hàm thực sự chạy, không lọc theo cách viết tên; có biên nhận hoàn tất và tình trạng observer. |
| `tu-kiem-bo-qua-cap-diem` | F3@41d03d8 → G4@1ea9c1c | H2 P2 | Tự kiểm đi qua chính đường chấm bình thường trong tiến trình/phạm vi cô lập, không rẽ sang đường CON trước nhánh cấp điểm. |
| `fixture-khong-co-lap-ghi` | Mới ở5138faa khi chạy toàn W5 | H3 P1 | Mọi đích ghi và biến môi trường điều khiển đích đều thuộc fixture và được dọn. |
| `loi-cong-cu-mat-chan-doan` | Mới đo ở5138faa | H4 P3 | Lỗi observer/công cụ phải về trạng thái không đo được, không thành số liệu B1 sai. |

Hai lớp đầu là **cùng hình dạng vá hẹp qua ba lượt**; theo SPEC S3 và chỉ thị lượt3, cần checkpoint của chủ kho trước vòng sửa/review tiếp theo. Reviewer chỉ hoàn tất verdict này; không tự cấp thêm vòng hoặc sửa packet.

HƯỚNG 9 — Bảng đường kiểm tra do reviewer tự dựng; môi trường và an toàn

| Đường | Logic thật được đo / phần fixture thay thế | Chốt và phản chứng | Kết luận/phần bỏ sót |
|---|---|---|---|
| (a), ba biểu thức | Trích một dòng từ chính W1/W2/W3; không chứng minh ngữ cảnh chạy | So baseline +14 đầu vào; strip-star đỏ3 ca | Đúng vai trò kiểm giá trị, không lấy nó chứng minh đường chạy |
| (d) W1 | Toàn bộ W1; python giả chỉ cấp lệnh/env và ghi probe | rc0, lệnh cài đã chạy, PATH/FIX_X đúng tại probe; unused/heredoc/exit/overwrite/pipeline-after đều đỏ | Không thay logic gán LENH/eval/export/PATH. Không chứng nhận cong_cu.py/YAML/cài thật |
| (d) W2 | Toàn bộ W2; archive/binary giả có hash thật,20.001 dòng | Giải nén, kiểm bản, stdout và GITHUB_PATH; baseline/pipeline-after đỏ141 | Không chạy đường tải mạng hoặc nền Windows/macOS; thuộc fixture Linux offline |
| (d) W3 | Toàn bộ W3; kho Git cục bộ thật; chỉ installer W2 và shellcheck là stub | cong-cu.txt + kết luận1/1/1 ref; baseline/pipeline-after đỏ141 | Installer stub tránh phụ thuộc lỗi W2 ở điểm W3; không thay phép gán al_ban cần đo. Không chứng nhận installer hoặc ShellCheck từ phép này |
| (c) ba điểm | Cùng cham_diem nhưng ghi ở CON=1 | Predicate174 / cấp ghi175 hỏng đều làm(c) đỏ | Nhánh DAT155 không đi qua: **H2** |
| (e) W5 lần đầu | Source W5, env recorder, PAD20.000 bằng Bash | Khớp/không khớp/chuỗi con; old/dead-lam đều đỏ | Theo được body lúc hook thấy lời gọi; không bao phủ mọi cách gọi hoặc trap bị gỡ: **H1** |
| (e) W5 sau lần đầu | Checksum body ở lời gọi có prefix lam+space | Redef thường bị bắt, quoted/builtin-trap lọt | **H1**, không coi source là bằng chứng tự động của mọi đường |
| (c) B1 | Đổi hai chốt về printf/grep; dùng cham_b1 | Predicate220 luôn đúng làm(c) đỏ | Khóa B1 cơ bản có răng; không khắc phục H1/H2 |
| Dựng payload/công cụ | awk rc+số dòng, PAD đếm, archive/hash | awk lỗi/ngắn/sha lỗi bị chặn; seq-f không còn là dependency | **G3 đóng**; lỗi checksum observer không chẩn đoán đúng: **H4** |
| Cách ly và dọn fixture | TMP/EXIT trap; (d) env-i, (e) kế thừa môi trường | TMP riêng hết rác; sentinel RUNNER_TEMP ngoài TMP bị làm rỗng | **H3**; chỉ so danh sách tên /tmp là không đủ |

Lệnh bổ sung: `python tam/tmp.mtrFTlLP7L/audit.py safety` → `safety-w4` **53/53**, wrapper log không có curl/wget/ssh; Git ls-remote/clone chỉ dùng đường cục bộ dưới fixture. `safety/tmp-delta.json` có `after_new=[]`, `deleted=[]`, TMP riêng rỗng. Đây chỉ là quan sát wrapper và tên tệp; H3 chứng minh có thể ghi đè tệp có sẵn mà phép này không thấy. `strace -f -e trace=network,file ... true` rc1, `PTRACE_*: Operation not permitted`: **KHÔNG ĐO ĐƯỢC audit syscall toàn cục**, không tuyên bố tuyệt đối không kết nối/ghi nào khác.

`env -i` không mô phỏng toàn CI: nó bỏ CI/GITHUB_ACTIONS/RUNNER_TEMP/BASH_ENV, hàm export và các biến caller. Reviewer chạy bổ sung `python tam/tmp.mtrFTlLP7L/batch_context.py` trên **toàn W1**, producer lớn20.000 dòng, giữ `CI=true GITHUB_ACTIONS=true`, cả lời gọi `actionlint` lẫn `--bat-buoc` (đi qua source thật): head rc0 có PROBED; nền rc141 ở cả hai. **KHÔNG PHẢI LỖI đã đo** về nhánh batch/source W1 hoặc giá trị CI ở đây. Không mở rộng kết quả này thành mọi biến môi trường/mọi hệ điều hành. Sai khác source/execute giả định không có ca sản phẩm bị sai đã đo thì không thêm finding.

Sau khi thấy H3, harness các phép đo bổ sung tự đặt RUNNER_TEMP trong scratch để không tiếp tục chạm đích mặc định; `logs/harness-env-history.txt` ghi thay đổi này. Phép H3 chính cố ý đặt đích sentinel do reviewer sở hữu **bên ngoài TMP riêng của W4 nhưng vẫn trong scratch**. Hai cây nguồn vẫn chỉ đọc.

HƯỚNG 10 — Hoàn tất hồi quy, lời khai và giới hạn

- `python tam/tmp.mtrFTlLP7L/follow_checks.py syntax_versions`: Bash5.2.21, Python3.11.15, Git2.43.0, actionlint1.7.7, ShellCheck0.11.0; `bash -n` head8/8 và nền7/7. Lệnh/version/output trong `logs/versions-comparison.jsonl`.
- `python tam/tmp.mtrFTlLP7L/prior_old_review_checks.py equivalence`: **604 đầu vào ×3 điểm ×3 chế độ =5.436**, mọi rc0, không mismatch với baseline và oracle độc lập; gồm CR/LF, glob, %, Unicode. W1–W3 **KHÔNG PHẢI LỖI hành vi mới** trong tập đo; không tuyên bố vét cạn.
- So byte output: W5 (5.314 byte), bash_nen (41), đăng ký CI (54.062;938/938 phản chứng), actionlint (224), ShellCheck (216) **giống hệt head/nền**. `regression-comparison.stdout` ghi phép so.
- `python ops/lease_publish_test.py`: head **187/187, đã chạy187, bỏ qua0**, rc0, **509,794s**; nền **187/187**, rc0, **505,950s**. Danh sách187 ca ngoài giống nhau. A6 delta0.
- `TMPDIR=<scratch>/temp PYTHONDONTWRITEBYTECODE=1 python tam/tmp.mtrFTlLP7L/t5_repeat.py`: head **200/200**, rc141=0, JSON DAT/1.7.7,78,211s; nền **200/200**, rc141=0,122,123s. Gói offline1.7.7 + PATH có9.9.9; số đo nền không phủ định race. Không tải công cụ mới; chỉ dùng binary ShellCheck có sẵn trong vật liệu trước.
- `python ops/cong_cu_test.py` trên hai bản sao đầy đủ riêng (`cong-head`, `cong-base`), launcher `full_cong.py`: cả hai đã in **52/52 đạt; tổng53, bỏ qua1, tiền kiểm bỏ qua0**; bỏ qua `t2_canary_thieu_shellcheck_phai_SUY_GIAM` vì thiếu công cụ `jsonschema`. Tự kiểm song song in ĐẠT; phần **212 đột biến chưa hoàn tất**, reviewer ngắt launcher (rc130). **KHÔNG ĐO ĐƯỢC N/N, rc con cuối và delta toàn suite**, không ghi pass. `logs/cong-full-incomplete.json` giữ toàn output có được và lý do; A2 đầy đủ chưa chứng nhận. Đây là phần tùy chọn “nếu kịp” trong prompt, không che phần chưa chạy xong.
- Trong loạt W5 bổ sung, `witness-head` và `whole-v2-quoted-calls` có lần **104/105** ở ca tag của bước CHỐT, trước mọi gọi lam; thông báo “KHÔNG tag nào giữ” dù fixture có tag. Workflow/bước chốt/producer này giống baseline, nằm ngoài diff packet; phép chính ban đầu hai cây105/105 và lần xác nhận head/witness mutant sau đều105/105. **KHÔNG PHẢI LỖI mới do packet**; không giấu lần đỏ, cũng không dùng nó làm bằng chứng H1. Tần suất flake và sửa pipeline `gh ... | grep -qxF` có sẵn ở workflow: **KHÔNG ĐO ĐƯỢC đầy đủ trong lượt này**, không tự mở write set.
- Ruff bare lint: **not_run / KHÔNG ĐO ĐƯỢC**; packet không sửa `.py`. Không gộp bash_nen hay pin/probe thành “Ruff passed”.

Đối chiếu commit5138faa với phép đo:

| Lời khai | Đo độc lập |
|---|---|
| 53/53 head;49/53 nền; mỗi W1/W2/W3/W5 nền đỏ riêng | Đúng, đã tái lập |
| Chạy toàn tệp, đo tại điểm sử dụng W1–W3 | Đúng với ba fixture/CLI đã mô tả; G1 đóng |
| Dùng chung hàm; predicate/nhánh cấp điểm luôn đúng làm(c) đỏ | Đúng ở174/175/220; **sai khi hiểu toàn đường cấp điểm**, H2 |
| Bắt runtime lam kể cả đổi trước/sau ca đầu; W5 không gỡ được trap | Đúng cho gọi thường; **sai qua quoted call/builtin trap**, H1 |
| Công cụ hỏng/ngắn ⇒ rc2; không xanh im lặng | Đúng cho producer/hash archive; **sai chẩn đoán cksum**, H4; actionlint cuối W5 không thuộc chốt B1 |
| Fixture offline và temp | Không thấy mạng ở wrapper; **ghi ra ngoài TMP/để lại tệp đã đo**, H3 |

Số lịch sử2/3000,0/3000 và “một write() mỗi dòng” ở commit r1/chú thích không có log executor độc lập trong vật liệu; strace không dùng được. **KHÔNG ĐO ĐƯỢC** provenance tự đo lại/syscall, không tự kết luận số liệu giả. Chú thích W4 ghi “r2 g3” còn commit/prompt là r2 g2 lượt3: lệch tên chú thích, không ảnh hưởng neo exact SHA; ghi như nợ biên tập, không tạo thêm finding hành vi riêng.

BẢNG FINDING MỚI VÀ GỢI Ý KHẮC PHỤC

| ID | Hạng, vị trí trên head | Hậu quả đã đo | Vá ở đâu/cách nào; ca khóa; rủi ro và trần |
|---|---|---|---|
| H1 | **P2** — W4:197–208,223 | B1 quay lại ở hàm sống nhưng W4 vẫn53/53 vì observer mất lời gọi hoặc bị gỡ | **Chỉ W4:** thay bộ lọc prefix câu lệnh bằng quan sát vào hàm thực tế/định danh frame, theo dõi các lần body sống thay đổi; bắt buộc biên nhận driver kết thúc và observer còn hoạt động. Có thể từ chối cấu trúc không chứng minh được bằng rc2. Không chữa chỉ bằng thêm mẫu cho quote hay chặn thêm đúng một cách viết trap. **Khóa:** giữ dead-lam/redef trước và sau ca đầu; thêm quoted-call và builtin-trap-off, tất cả phải đỏ hoặc không đo được, head53/53. **Rủi ro:** recursion/dynamic scope/errexit và chi phí DEBUG trên20.000 đối số; không dùng readonly hay sửa hàm sản phẩm để “làm đúng” hành vi cần đo. **Trần:** thay khối B1 hiện có (~45 dòng driver), không nối thêm một bộ observer; phải bù mọi dòng mới bằng dòng cũ bỏ đi. Chưa có bản vá hoàn chỉnh được chứng nhận≤300. |
| H2 | **P2** — W4:149–163 | (c) chạy CON rồi return trước chốt DAT thật; cấp điểm riêng cho mọi(d) khiến W1 nền lọt53/53 | **Chỉ W4:** bỏ nhánh CON riêng; chạy chính đường chấm bình thường trong subshell/phạm vi cô lập, đối chiếu tăng TONG/DAT và lý do/rc của kết quả thực. Tự kiểm thất bại phải truyền lỗi được xác nhận, không dựa vào nhánh cấp điểm đang bị thử. **Khóa:** mutant predicate174, ghi175 và predicate155 chỉ cho(d) luôn đạt đều khiến(c)/driver báo lỗi; head xanh, từng nền đỏ141. **Rủi ro:** không rò bộ đếm sang cha, không đệ quy, không lấy lỗi setup làm tín dụng141. **Trần:** thay ~17 dòng ghi/tu_kiem hiện có, tái dùng phần phán quyết; không cộng một tầng chấm thứ ba. Chưa có bản vá đầy đủ được chứng nhận≤300. |
| H3 | **P1** — W4:208 | Head nguyên vẹn làm rỗng tệp ngoài TMP của fixture và để lại nó, vẫn53/53 | **Chỉ W4:** đặt RUNNER_TEMP và NEO_TEP riêng cho lời gọi B1 dưới TMP sở hữu; kiểm các biến tương đương có thể đổi đích và giữ cleanup. Đối chứng một dòng `RUNNER_TEMP="$TMP" NEO_TEP="$TMP/b1.neo" bash -c ...` đã giữ sentinel và53/53. **Khóa:** sentinel caller ngoài TMP còn nguyên byte/hash, không tạo /tmp/don_ref_neo.txt, TMP riêng sạch; kiểm cả lúc đã có và chưa có tệp. **Rủi ro:** không thay đổi các override NEO_TEP/GIA_REF_STATE tường minh của từng ca và không dọn tệp caller. **Trần:** thay một dòng sẵn có, không cần tăng294 dòng thêm. |
| H4 | **P3** — W4:198,208–209 và preflight:67 | cksum trả127 bị nuốt; W4 gọi lại B1 48 lần rồi báo50/53 rc1, không KHÔNG ĐO ĐƯỢC | **Chỉ W4:** kiểm cksum và bắt rc khi băm body, đưa lỗi observer tới trạng thái không đo được; không dùng output cũ nếu lỗi xuất hiện sau ca đầu. Có thể dùng cùng biên nhận lỗi/hoàn tất của H1. **Khóa:** thiếu/hỏng cksum ngay lần đầu và sau lần đầu ⇒ rc2, tên công cụ, không tổng kết xanh; head/nền vẫn giữ kết quả thật. **Rủi ro:** đừng gộp lỗi công cụ với thay đổi body hợp lệ hoặc kết quả sản phẩm đỏ. **Trần:** thêm tên vào dòng preflight và thay cách truyền lỗi trong driver; phải dùng lại khối H1, không thêm bộ chấm độc lập. |

Kiểm đếm `python` trên W4:281 dòng,20 dòng trắng và35 dòng bắt đầu bằng chú thích (kể cả shebang trong fixture); có thể tái bố trí ngân sách bằng cách cô đọng phần giải thích lặp, không bỏ chốt đo hay shebang. Không dùng số dòng trắng/chú thích này như bằng chứng một patch chưa viết đã đạt trần.

Tất cả hướng sửa thuộc **W4**, không đòi ghi ngoài W1–W5. Head đang294, chỉ còn6 dòng thêm nếu không cắt/thay thế phần cũ. H3 đã có đối chứng một dòng trong bản sao; H1/H2/H4 là đề xuất để executor tự dẫn xuất, **không phải bản vá đã chứng minh nằm trong trần**. Không có bằng chứng rằng chỉ có thể sửa bằng cách vượt300; vì vậy không tự xin/nới trần. Nếu bản triển khai thực tế vẫn>300 sau khi thay phần cũ, SPEC S5 buộc checkpoint trước khi ghi tiếp.

KẾT LUẬN NGHIỆM THU

- **1 P1 / 2 P2 / 1 P3**, bốn biểu hiện H1–H4 trong bốn lớp ở bảng trên; không đếm lại F1/F3/G2/G4 thành finding mới. Không phát hiện sai giá trị W1–W3 hoặc tái xuất hiện B1 trong W5 head hiện hành; H1/H2 là sức bắt hồi quy, H3 là side effect trên head thật, H4 là chẩn đoán fixture.
- A1 số head/nền và từng điểm đạt, nhưng khóa lớp runtime/self-check chưa đạt H1/H2; điều kiện fixture bị vi phạm H3. A3/A4 và A6 đã hoàn tất không delta lỗi. A2 phần t5 đạt; toàn bộ suite **KHÔNG ĐO ĐƯỢC đầy đủ**. A5 không đủ0/0/0.
- `verdict: changes_requested`. Không approve, không merge/push/đăng GitHub. Hai lớp tái diễn cần chủ kho xử lý checkpoint trước vòng tiếp theo, không tự chuyển vai sang executor.

HƯỚNG 11 — Chốt hiện vật, neo cuối và dọn thử nghiệm

- Lệnh: các argv trong `tam/tmp.mtrFTlLP7L/logs/anchors-final.json`: `git rev-parse HEAD HEAD^{tree}`, `sha256sum SPEC.md`, `git diff 89fc4fa..HEAD --check`, `git status --porcelain --untracked-files=all --ignored` trên cả hai cây, và numstat. Output: SHA/tree/baseline/SPEC giữ nguyên như đầu verdict; diff-check rc0; hai status rỗng; vẫn294 dòng thêm chỉ W1–W5.
- `bash tam/tmp.mtrFTlLP7L/cleanup.sh` dùng EXIT trap dọn **chỉ** `tam/tmp.mtrFTlLP7L/temp/`:117 thư mục con,979 mục, còn0; log `cleanup.json`. Giữ bản sao, mutant, script và log làm hiện vật; không xóa `/tmp/don_ref_neo.txt` có sẵn hoặc bất kỳ tệp caller nào. Các snapshot sạch chỉ chứng minh không có delta quan sát được ở hai mốc; không được diễn giải thành audit syscall.
- Lượt witness đầu dừng ở ca cuối vì mutant dead-lam chưa được vòng mutations tạo xong; không dùng lỗi dựng đó làm kết luận. Sau khi dependencies hoàn tất, `python tam/tmp.mtrFTlLP7L/audit.py witness` chạy lại đủ7 ca (`witness-repeat.jsonl`), tất cả rc0/105 ca gốc đạt; head giữ explicit, sáu biến thể body cũ thêm fallback như dự kiến. `unchanged-flake-path.json` xác nhận prefix W5 trước lam và workflow giống hệt nền.
- `evidence.sha256` băm script/harness, các W4 mutant, các tệp ops đột biến và log; `logs/verdict-final.json` ghi đường dẫn, kích thước và SHA256 của VERDICT.md. Không commit/push/đăng nhận xét bên ngoài.
