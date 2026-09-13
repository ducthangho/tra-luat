verdict: changes_requested
reviewed_sha: 3bbc6b46c2fb6066fa64088308ce30fe40f87aa5
P1: 0
P2: 1

Nhật ký dưới đây được ghi tăng dần sau các phép đo. A1/A5: KHÔNG ĐO ĐƯỢC (không chạy CI).

## ĐỐI CHIẾU LƯỢT TRƯỚC — ghi ngay sau phép đo đầu

- `ruff-khuon-chua-chung-minh-provisioning`: phần bỏ chốt env **ĐÃ VÁ THẬT theo quyết định thu hẹp của chủ kho**, không coi là đã chứng minh runtime env. Đã đọc M7/SPEC:205, A7/SPEC:586–598 và `viec_trong_lease`: bốn ca bố cục vẫn giữ đúng màu, pin/probe vẫn có răng. Không có nghĩa vụ phân tích env tại các mục ấy.
- Chạy `TMPDIR="$PWD/review/tmp" PYTHONDONTWRITEBYTECODE=1 python3 -B review/doi_chieu.py` → rc=0. Tái chạy nguyên fixture lượt 9: ba ca PIP_TARGET theo workflow/job/step và một ca PYTHONUTF8=2 đổi từ đỏ sang `([],3)`; đây là bốn năng lực kiểm env đã chủ ý bỏ, không ghi thành finding. Hai ca env vô hại trước/sau đều xanh. Tổng 111 → 108 = bỏ 8 ca (6 fixture env + 2 tập env), thêm 5 ca lexer/module.
- Đột biến đưa consumer base trở lại: `tra=False, so_ca=108`, ca A7 `ruff-ci-da-tach-dung` LỌT; bốn fixture bắt buộc trên head lần lượt 0/0/1/1 lỗi. A7 còn răng độc lập với chốt env.
- Bộ nháp: đột biến `return False` trước KQ → `(False,0,set())`, bị bác làm nền. Sau đó mới chạy `review/do_rang.py` (đã ghim ROOT/TAM trong sandbox): nền `True/108/[]`, 7 mutant có tập LỌT khớp toàn bộ lời khai. Chi tiết: `review/logs/rang.log`.
- **Tìm được răng cho nhánh trích dẫn:** bỏ hai nhánh ghi nhớ quote → bộ gốc vẫn `True/108/[]`, đúng lời khai giới hạn hiện tại. Chỉ đổi literal fixture echo có sẵn `a ; b && c | d` thành `a ; b ruff && c | d`: head vẫn `True/108/[]`, mutant mất quote → `False/108/{ruff-ci-toan-tu-trong-dau-nhay}`. Đây là thay dữ liệu vô hại trong fixture sẵn có, không tự soạn payload. Thay một dòng đang được thêm bằng một dòng khác: **0 dòng tăng, A8 vẫn 500**. Không giao patch gate để áp mù.
- Ba sửa lexer và đánh giá chung stable finding sẽ được chốt cuối sau các hướng mới; kết quả trên không tính vào N.

## BẢNG SĂN

HƯỚNG 1: Ranh giới tên gói gần Ruff
  giả thuyết : nếu tên gói khác hoặc tên tệp vẫn bị nhận là Ruff thì chặn oan job vô can
  lệnh       : TMPDIR="$PWD/review/tmp" PYTHONDONTWRITEBYTECODE=1 python3 -B review/hunt.py 1
  output     :
    ruff-lsp tokens= [['pdm', 'remove', 'ruff-lsp']] classification= ('KHONG', None) consumer= ([], 3)
    ruff_lsp tokens= [['pdm', 'remove', 'ruff_lsp']] classification= ('KHONG', None) consumer= ([], 3)
    ruff.lsp tokens= [['pdm', 'remove', 'ruff.lsp']] classification= ('KHONG', None) consumer= ([], 3)
    Ruff-LSP tokens= [['pdm', 'remove', 'Ruff-LSP']] classification= ('KHONG', None) consumer= ([], 3)
    ruff.toml tokens= [['pdm', 'remove', 'ruff.toml']] classification= ('KHONG', None) consumer= ([], 3)
    ruffian tokens= [['pdm', 'remove', 'ruffian']] classification= ('KHONG', None) consumer= ([], 3)
    ruff0 tokens= [['pdm', 'remove', 'ruff0']] classification= ('KHONG', None) consumer= ([], 3)
    x-ruff tokens= [['pdm', 'remove', 'x-ruff']] classification= ('KHONG', None) consumer= ([], 3)
  kết luận   : KHÔNG PHẢI LỖI

HƯỚNG 2: Tên module thực thi khác tên distribution
  giả thuyết : nếu chuẩn hóa PEP 503 áp vào module thì có thể nhận probe không chạy được
  lệnh       : TMPDIR="$PWD/review/tmp" PYTHONDONTWRITEBYTECODE=1 python3 -B review/hunt.py 2
  output     :
    ruff recognizer= True consumer= ([], 3) runtime= {'argv': ['/usr/local/bin/python3', '-m', 'ruff', '--version'], 'rc': 0, 'out': 'ruff 0.15.15'}
    Ruff recognizer= True consumer= ([], 3) runtime= {'argv': ['/usr/local/bin/python3', '-m', 'Ruff', '--version'], 'rc': 1, 'out': '/usr/local/bin/python3: No module named Ruff'}
    ruff[all] recognizer= True consumer= ([], 3) runtime= {'argv': ['/usr/local/bin/python3', '-m', 'ruff[all]', '--version'], 'rc': 1, 'out': '/usr/local/bin/python3: No module named ruff[all]'}
  kết luận   : LỖI

HƯỚNG 3: Ngữ pháp extras trong requirement
  giả thuyết : nếu mọi nội dung trong [] được bỏ thì requirement không hợp lệ vẫn nhận GHIM
  lệnh       : TMPDIR="$PWD/review/tmp" PYTHONDONTWRITEBYTECODE=1 python3 -B review/hunt.py 3
  output     :
    ruff[all]==0.15.15 requirement_parser= VALID classification= ('GHIM', 'python -m pip install --quiet ruff[all]==0.15.15') consumer= ([], 3)
    ruff[]==0.15.15 requirement_parser= VALID classification= ('GHIM', 'python -m pip install --quiet ruff[]==0.15.15') consumer= ([], 3)
    ruff[!]==0.15.15 requirement_parser= INVALID: Parse error at "'[!]==0.1'": Expected string_end classification= ('GHIM', 'python -m pip install --quiet ruff[!]==0.15.15') consumer= ([], 3)
    ruff[all,]==0.15.15 requirement_parser= INVALID: Parse error at "'[all,]=='": Expected string_end classification= ('GHIM', 'python -m pip install --quiet ruff[all,]==0.15.15') consumer= ([], 3)
    ruff[all..x]==0.15.15 requirement_parser= VALID classification= ('GHIM', 'python -m pip install --quiet ruff[all..x]==0.15.15') consumer= ([], 3)
  kết luận   : LỖI

HƯỚNG 4: Nối dòng ở GIỮA token
  giả thuyết : nếu backslash-newline bị thay bằng space thì argv hợp lệ bị tách sai
  lệnh       : TMPDIR="$PWD/review/tmp" PYTHONDONTWRITEBYTECODE=1 python3 -B review/hunt.py 4
  output     :
    probe= 'ruff --ver\\\nsion' tokens= [['ruff', '--ver', 'sion']] consumer= (["CI không in probe Ruff --version (job: ['gate-registry'])"], 3) runtime= {'argv': ['bash', '--noprofile', '--norc', '-c', 'ruff --ver\\\nsion'], 'rc': 0, 'out': 'ruff 0.15.8'}
    probe= 'ru\\\nff --version' tokens= [['ru', 'ff', '--version']] consumer= (["CI không in probe Ruff --version (job: ['gate-registry'])"], 3) runtime= {'argv': ['bash', '--noprofile', '--norc', '-c', 'ru\\\nff --version'], 'rc': 0, 'out': 'ruff 0.15.8'}
    probe= 'ruff --version' tokens= [['ruff', '--version']] consumer= ([], 3) runtime= {'argv': ['bash', '--noprofile', '--norc', '-c', 'ruff --version'], 'rc': 0, 'out': 'ruff 0.15.8'}
  kết luận   : LỖI

HƯỚNG 5: Trích dẫn ANSI-C của Bash
  giả thuyết : nếu ký hiệu dollar-quote đi vào argv literal thì probe Bash hợp lệ bị bác
  lệnh       : TMPDIR="$PWD/review/tmp" PYTHONDONTWRITEBYTECODE=1 python3 -B review/hunt.py 5
  output     :
    probe= "ruff '--version'" tokens= [['ruff', '--version']] consumer= ([], 3) runtime= {'argv': ['bash', '--noprofile', '--norc', '-c', "ruff '--version'"], 'rc': 0, 'out': 'ruff 0.15.8'}
    probe= "ruff $'--version'" tokens= [['ruff', '$--version']] consumer= (["CI không in probe Ruff --version (job: ['gate-registry'])"], 3) runtime= {'argv': ['bash', '--noprofile', '--norc', '-c', "ruff $'--version'"], 'rc': 0, 'out': 'ruff 0.15.8'}
    probe= 'ruff "--version"' tokens= [['ruff', '--version']] consumer= ([], 3) runtime= {'argv': ['bash', '--noprofile', '--norc', '-c', 'ruff "--version"'], 'rc': 0, 'out': 'ruff 0.15.8'}
  kết luận   : LỖI

HƯỚNG 6: Registry qua tên module và đường tuyệt đối
  giả thuyết : nếu chỉ đuôi .py định danh lời gọi thì module thật mất dấu registry
  lệnh       : TMPDIR="$PWD/review/tmp" PYTHONDONTWRITEBYTECODE=1 python3 -B review/hunt.py 6
  output     :
    absolute= ([], 3)
    module= (['CI không provision Ruff trước test registry trong cùng job (job chạy test registry: KHÔNG CÓ)'], 3)
    module-help= {'argv': ['/usr/local/bin/python3', '-m', 'ci_dang_ky_test', '--help'], 'rc': 0, 'out': 'usage: ci_dang_ky_test.py [-h] [--chay]\n                          [--mutant {windows_311_launcher_workflow}]\n\noptions:\n  -h, --help            show this help message and exit\n  --chay\n  --mutant {windows_311_launcher_workflow}'}
  kết luận   : LỖI

HƯỚNG 7: Cờ --chay phải cùng lệnh với đường registry
  giả thuyết : nếu cờ được lấy qua ranh giới lệnh thì registry chưa --chay vẫn được nhận
  lệnh       : TMPDIR="$PWD/review/tmp" PYTHONDONTWRITEBYTECODE=1 python3 -B review/hunt.py 7
  output     :
    separator= ' ' commands= [['python', '.claude/dev/ci_dang_ky_test.py', '--chay']] consumer= ([], 3)
    separator= '\n' commands= [['python', '.claude/dev/ci_dang_ky_test.py'], ['--chay']] consumer= (['CI không provision Ruff trước test registry trong cùng job (job chạy test registry: KHÔNG CÓ)'], 3)
    separator= ';' commands= [['python', '.claude/dev/ci_dang_ky_test.py'], ['--chay']] consumer= (['CI không provision Ruff trước test registry trong cùng job (job chạy test registry: KHÔNG CÓ)'], 3)
    separator= '&&' commands= [['python', '.claude/dev/ci_dang_ky_test.py'], ['--chay']] consumer= (['CI không provision Ruff trước test registry trong cùng job (job chạy test registry: KHÔNG CÓ)'], 3)
  kết luận   : KHÔNG PHẢI LỖI

HƯỚNG 8: Có nhiều probe, một probe đúng sau install
  giả thuyết : nếu ghi nhớ riêng probe đầu tiên thì một probe sớm che mất bằng chứng hợp lệ phía sau
  lệnh       : TMPDIR="$PWD/review/tmp" PYTHONDONTWRITEBYTECODE=1 python3 -B review/hunt.py 8
  output     :
    commands= [['ruff', '--version'], ['python', '-m', 'pip', 'install', '--quiet', 'ruff==0.15.15'], ['ruff', '--version']] probe_after= False consumer= (["CI không in probe Ruff --version (job: ['gate-registry'])"], 3)
    control_remove_only_early_probe= ([], 3)
  kết luận   : LỖI

HƯỚNG 9: Phân loại tên gói ở bước có điều kiện
  giả thuyết : nếu nhánh conditional vẫn dùng regex chuỗi con thì sửa tên gói chỉ hiệu lực một phần
  lệnh       : TMPDIR="$PWD/review/tmp" PYTHONDONTWRITEBYTECODE=1 python3 -B review/hunt.py 9
  output     :
    unconditional_classifier= ('KHONG', None)
    condition= None consumer= ([], 3)
    condition= runner.os != 'Windows' consumer= (["CI không ghim Ruff 0.15.15 (job: ['gate-registry'])"], 3)
  kết luận   : LỖI

HƯỚNG 10: Lỗi quote và fallback tokenizer
  giả thuyết : nếu shlex lỗi mà fallback split vẫn được dùng để cấp bằng chứng thì shell sai cú pháp vẫn xanh
  lệnh       : TMPDIR="$PWD/review/tmp" PYTHONDONTWRITEBYTECODE=1 python3 -B review/hunt.py 10
  output     :
    raw_commands= ['python -m pip install --quiet ruff==0.15.15', 'ruff --version "'] tokens= [['python', '-m', 'pip', 'install', '--quiet', 'ruff==0.15.15'], ['ruff', '--version', '"']] consumer= ([], 3)
    shell_parse= {'argv': ['bash', '--noprofile', '--norc', '-n', '/tmp/claude-0/-home-user-tra-luat/d706aae3-d737-5ec6-8390-ae296d24c1a2/scratchpad/rv463e/review/mutants/h10-probe.sh'], 'rc': 2, 'out': '/tmp/claude-0/-home-user-tra-luat/d706aae3-d737-5ec6-8390-ae296d24c1a2/scratchpad/rv463e/review/mutants/h10-probe.sh: line 1: unexpected EOF while looking for matching `"\''}
  kết luận   : LỖI

### Bổ sung bằng chứng sau H1–H10 (không tăng N)

- **Răng riêng của ca whitespace đã đo được:** `review/doi_chieu.py` thêm điều kiện vòng về văn bản `and " ".join(tok) in run` tại nhánh nhận probe, tái tạo lỗi chỉ nhận cách viết chuẩn. Kết quả **False / 108 / {ruff-ci-probe-thua-khoang-trang}**: chỉ đúng ca đích LỌT. Đây là đột biến kiểm việc phụ thuộc spelling quay lại; không chứng minh mọi nhánh lexer đã có răng. Lời khai “không đột biến nào giết được” trong EVIDENCE quá rộng.
- **H4/H5, kiểm lại đúng phiên bản:** lần đầu CLI `ruff` trên PATH thực tế in **0.15.8**, khác module Python **0.15.15**. Không dùng lần ấy chứng minh provisioning đúng pin. Đã chạy lại qua cùng Python/module 0.15.15 bằng `review/corroborate.py`: nối giữa `--ver`/`sion`, giữa `ru`/`ff`, và dollar-quote đều **rc=0, ruff 0.15.15**, nhưng consumer vẫn báo thiếu probe; đối chứng bình thường `([],3)`. Log `review/logs/corroborate.log` giữ cả argv/token/kết quả.
- **Đường main cũng lọt H2/H3/H10:** bản sao chương trình chỉ trỏ `CI_WORKFLOW` sang YAML đã đột biến của từng hướng, chạy main KHÔNG có `--chay` → cả ba **rc=0, RUFF CI 3/3, PHẢN CHỨNG 108/108, TỔNG ĐẠT**. Không gọi test registry đầy đủ hay CI. Log riêng: `main-h2.log`, `main-h3.log`, `main-h10.log`.
- **Thử vá một phần, không sửa cây review:** sửa nối dòng thành xóa cặp backslash-newline; chọn probe cuối có mặt; phân biệt tên module/executable với tên distribution. Bộ gốc vẫn 108/108; H2 được bác, H4/H8 chuyển đúng sang `[]`; H5 còn lỗi. Diff đo so base: Python **+373/−88**, workflow **+126/−6** ⇒ **499 additions, 2 tệp**, giảm một dòng vật lý. Đây là phép thử chẩn đoán trên `review/mutants/partial-fix.py`, **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**; không là gói vá hoàn chỉnh hoặc patch gate được cấp quyền áp.

HƯỚNG 11: Có cờ --version nhưng Ruff thực hiện chế độ khác
  giả thuyết : nếu chỉ tìm cờ trong argv thì --help hoặc cờ ở subcommand được nhận làm probe phiên bản
  lệnh       : TMPDIR="$PWD/review/tmp" PYTHONDONTWRITEBYTECODE=1 python3 -B review/hunt.py 11
  output     :
    probe= python -m ruff --version consumer= ([], 3) runtime= {'argv': ['/usr/local/bin/python3', '-m', 'ruff', '--version'], 'rc': 0, 'out': 'ruff 0.15.15'}
    probe= python -m ruff --version --help consumer= ([], 3) runtime= {'argv': ['/usr/local/bin/python3', '-m', 'ruff', '--version', '--help'], 'rc': 0, 'out': 'ruff 0.15.15'}
    probe= python -m ruff --help --version consumer= ([], 3) runtime= {'argv': ['/usr/local/bin/python3', '-m', 'ruff', '--help', '--version'], 'rc': 0, 'out': "Ruff: An extremely fast Python linter and code formatter.\n\nUsage: ruff [OPTIONS] <COMMAND>\n\nCommands:\n  check    Run Ruff on the given files or directories\n  rule     Explain a rule (or all rules)\n  config   List or describe the available configuration options\n  linter   List all supported upstream linters\n  clean    Clear any caches in the current directory and any subdirectories\n  format   Run the Ruff formatter on the given files or directories\n  server   Run the language server\n  analyze  Run analysis over Python source code\n  version  Display Ruff's version\n  help     Print this message or the help of the given subcommand(s)\n\nOptions:\n  -h, --help\n          Print help (see a summary with '-h')\n\n  -V, --version\n          Print version\n\nLog levels:\n  -v, --verbose\n          Enable verbose logging\n\n  -q, --quiet\n          Print diagnostics, but nothing else\n\n  -s, --silent\n          Di"}
    probe= python -m ruff check --version consumer= ([], 3) runtime= {'argv': ['/usr/local/bin/python3', '-m', 'ruff', 'check', '--version'], 'rc': 2, 'out': "error: unexpected argument '--version' found\n\n  tip: a similar argument exists: '--verbose'\n\nUsage: ruff check --verbose [FILES]...\n\nFor more information, try '--help'."}
  kết luận   : LỖI

### Tái kiểm điều kiện của fixture (không tăng N)

Bảo toàn khóa `on` khi round-trip PyYAML; đặt `shell: bash` tường minh cho H4/H5, đúng shell đã đo. Các fixture đầu dùng PyYAML mặc định nên `on` từng được dump thành khóa `true`; đây là lỗi dựng YAML của reviewer, không là finding sản phẩm. Hàm đang xét chỉ đọc `jobs`; vẫn đo lại cả 11 hướng để xác minh kết quả không phụ thuộc lỗi ấy.
- Đo lại H1: `python3 -B review/hunt.py 1 --no-append` → rc=0, log bằng lần trước=True.
- Đo lại H2: `python3 -B review/hunt.py 2 --no-append` → rc=0, log bằng lần trước=True.
- Đo lại H3: `python3 -B review/hunt.py 3 --no-append` → rc=0, log bằng lần trước=True.
- Đo lại H4: `python3 -B review/hunt.py 4 --no-append` → rc=0, log bằng lần trước=True.
- Đo lại H5: `python3 -B review/hunt.py 5 --no-append` → rc=0, log bằng lần trước=True.
- Đo lại H6: `python3 -B review/hunt.py 6 --no-append` → rc=0, log bằng lần trước=True.
- Đo lại H7: `python3 -B review/hunt.py 7 --no-append` → rc=0, log bằng lần trước=True.
- Đo lại H8: `python3 -B review/hunt.py 8 --no-append` → rc=0, log bằng lần trước=True.
- Đo lại H9: `python3 -B review/hunt.py 9 --no-append` → rc=0, log bằng lần trước=True.
- Đo lại H10: `python3 -B review/hunt.py 10 --no-append` → rc=0, log bằng lần trước=True.
- Đo lại H11: `python3 -B review/hunt.py 11 --no-append` → rc=0, log bằng lần trước=True.

## ĐỐI CHIẾU LƯỢT TRƯỚC — kết luận cuối

- **`ruff-khuon-chua-chung-minh-provisioning`: VÁ HỜ ở cấp lớp lỗi.** Các triệu chứng lexer được nêu ở lượt 9 **đã vá thật**; các phép đo mới cho thấy lớp diễn giải argv/cấp bằng chứng của chính chốt 1–3 vẫn chưa đóng. Giữ stable slug; không tính từng cửa thành một finding, không biến phần env đã được chủ kho bỏ thành lỗi.
- **Env: ĐÃ VÁ THẬT trong phạm vi quyết định rút về M7/A7.** Cụ thể đây là bỏ khả năng kiểm tĩnh env, không là chứng minh env đúng. Đã liệt kê bốn ca đỏ cũ nay xanh và tám ca bị bỏ ở nhật ký đầu. Bốn fixture A7, pin, probe, cùng-job/trước-registry đều còn đúng màu và còn răng. Không mất nghĩa vụ env nào mà M7/A7 thực sự ghi.
- **Lexer: ĐÃ VÁ THẬT đối với ca cũ.** `review/lexer_ab.py` chạy đối chiếu mã lượt 9 và head: hai inline-config TOML (nhiều dòng, hoặc `#` trong chuỗi) trước báo thiếu probe, head `[]`, Python/Ruff 0.15.15 thực chạy rc=0. Toán tử được quote thành toàn token: trước `[['echo']]`, head `[['echo',';','&&','|']]`. Registry tab và probe `-mruff` đều chuyển từ lỗi sang `[]`. `_cham_ruff` có răng ở mutant riêng, và H1 xác nhận tám tên khác không bị nhận là gói Ruff.
- **Không gán nhầm lỗi còn sót thành lỗi mới do delta lượt này:** `corroborate.log` có phép so old/head cho H2/H3/H4/H5/H6/H8/H10, các sai lệch ở những đầu vào ấy đã tồn tại trên head lượt 9. H9 cho thấy đường conditional vẫn dùng regex cũ thay vì vị từ tên mới. Kết luận “VÁ HỜ” áp cho tuyên bố đóng cả lớp, không phủ nhận các sửa cụ thể.
- **Hai lời khai không đo được răng:** giữ nguyên hai fixture lexer gốc thì mutant bỏ quote đúng là sống; tuy nhiên đột biến literal echo đã làm đúng ca quote giết nó, với **0 dòng tăng**. Ca whitespace cũng giết riêng mutant thêm ràng buộc quay về văn bản (`False/108/{ruff-ci-probe-thua-khoang-trang}`). Vì vậy lời khai giới hạn về fixture quote gốc là đúng; cách khẳng định không thể dựng đột biến có răng là không đúng. Không phát sinh finding P3 cho công cụ nháp từ việc reviewer tìm thêm phép đo.

## BẢNG ĐO

| Khẳng định | PR khai / yêu cầu | Đo được | Khớp? |
|---|---|---|---|
| Exact head | `3bbc6b46c2fb6066fa64088308ce30fe40f87aa5` | Khớp đầu/cuối; tree `39929536bc74845d07164a1c053b58b9bbe0fb7a` | Có |
| Merge-base | `bb7013c7669da19304a8769e5b25f8c1f8951e9c` | Khớp | Có |
| Spec r21 SHA256 | `decdb1a1ae794508f0be6d680342bbf7c46b7353e0708f16b522567e8cc56d96` | Khớp đủ 64 ký tự | Có |
| Lease SHA256 | `46182004162a051847bd2c80db489c43021c2f543e86b18d13a4651c85404db3` | Khớp đủ 64 ký tự | Có |
| ĐĂNG KÝ nền | 21/21 | 21/21, main rc=0 | Có |
| LAUNCHER WINDOWS nền | 4/4 | 4/4 hợp đồng tĩnh | Có, chưa chạy Windows |
| RUFF CI nền | Đầu EVIDENCE: 4/4; phần sửa mới: n/3 | **3/3** | Khớp phần mới; số đầu tệp cũ |
| PHẢN CHỨNG nền | Đầu EVIDENCE: 111/111; phần răng: 108 | **108/108**, tên phân biệt, `phan_chung=True`, main rc=0 | Khớp phần răng; số đầu tệp cũ |
| Ruff F | All checks passed | Module Ruff 0.15.15, `--no-cache --select F`, rc=0 | Có |
| A8 Python | +374/−88 | +374/−88 | Có |
| A8 workflow | +126/−6 | +126/−6 | Có |
| A8 tổng | 500 additions / 2 path | **500 / 2**, hết biên | Có |
| A7 bốn fixture | 0/0/≥1/≥1 lỗi | **0/0/1/1** | Có |
| A7 quay consumer về base | Tách đúng phải đổi màu | Ca `ruff-ci-da-tach-dung` LỌT; `False/108` | Có |
| Bộ nháp không nhận lần không chạy | Đòi return, số ca, tập LỌT | Early-return False → `False/0/[]`, bị bác làm nền | Có |
| Bảy mutant được giao | Các tập LỌT nêu trong EVIDENCE | Tất cả khớp, mỗi mutant chạy 108 ca và trả False | Có trong miền fixture được giao |
| Quote trong bộ gốc | Bỏ nhánh quote vẫn xanh | `True/108/[]` | Có |
| Có thể đo răng quote | Chưa dựng được | Chỉ đổi literal fixture: head xanh, mutant mất quote chỉ làm ca đích LỌT | Đã đo thêm được |
| Răng whitespace | “không đột biến nào giết được” | Mutant quay về so văn bản chỉ giết ca whitespace | **Không** với khẳng định tuyệt đối |
| A2 bảo toàn cấu trúc bước/lệnh | Chỉ dời hai bước + nhân setup | 40 → **38+10+10**; hai bước dời nguyên giá trị, phần gate còn lại nguyên giá trị | Có về cấu trúc |
| A2 conclusions hai lane | Phải đọc lượt thật, có miền tiền nhiệm xanh | Chưa chạy CI; không suy conclusion từ cấu trúc | **KHÔNG ĐO ĐƯỢC** |
| A3 job/step/prefix9/on/concurrency | Giữ nguyên | Đủ năm phép so xanh; mutant job-if, bỏ setup-copy, đổi trigger làm đỏ đúng phép | Có cục bộ |
| A4 | Mỗi job 60, không timeout mức bước | Đúng; bỏ khóa hoặc thêm timeout mức bước đều bị bác | Có cục bộ |
| Actionlint trên master snapshot và head | Delta đa tập chẩn đoán = 0 | **rc 0→0, 0→0 chẩn đoán**, delta 0; actionlint 1.7.12 + shellcheck 0.9.0 | Có với công cụ được cấp; chưa đo 1.7.7 |
| Ca âm actionlint bắt lỗi mới khi rc không đổi | Bắt buộc chạy | Bỏ quote ở hai bước Bash sẵn có: **rc 1→1, 1→2 chẩn đoán**, delta thêm 1, bỏ 0 | Có; đã chuẩn hóa tệp, loại/thông điệp, thân run và bỏ vị trí |
| A6 context cấu trúc | Ba context Ubuntu | `gate`, `gate-registry`, `gate-packet-loop`, mỗi tên kèm `(ubuntu-latest)`; không job nào có `name` khác | Có cục bộ |
| A6 ruleset/check trước merge | Readback live đúng head | Không có readback live trong phạm vi đóng | **KHÔNG ĐO ĐƯỢC** |
| Ops nghĩa vụ đọc | Bộ đã land, không thuộc write set | Đã đọc mã; cùng byte với bản cấp và base, SHA256 `b56636d9c26d9b0f7b537d71e9a7edc7ef446e8c51ef0466fbc849a064497134` | Có |
| Ops chạy cục bộ | Không lấy số lượt trước làm kết quả hiện tại | **rc=0, 8/8, 10/10 mutant, 23/23 nhóm, 76/76 tự đột biến** trên bản sao | Đã tự đo |
| Doctrine scan | Adapter yêu cầu | rc=0, 7 tệp, 0 chỗ chép doctrine | Có |
| Ref snapshot trong bundle | EVIDENCE ghi 368 và không shallow | Bare và origin snapshot **370/370 tên+OID bằng nhau**, shallow=false, abbrev=7 | Số đếm khác; hai bản trong sandbox khớp |
| Ref GitHub / đối chiếu cổng nguồn bên ngoài | Lời khai trước giao sandbox | Không truy cập nguồn ngoài sandbox; không xác nhận lại số/cổng tại head cũ | **KHÔNG ĐO ĐƯỢC** |
| A1/A5 | Chủ kho cấm CI | Không chi dispatch, không chạy full/Windows CI, không mượn log head khác | **KHÔNG ĐO ĐƯỢC** |
| Bản thử sửa một phần | Phải không tăng additions | **499 additions / 2 path**, main 108/108; H2/H4/H8 sửa được, H5 còn lỗi | Đúng trần, chưa là gói đầy đủ |
| Cây review không đổi | Không sửa/commit | HEAD/tree giữ nguyên; status và log reviewed_sha..HEAD rỗng | Có |

Lệnh cho các phép cấu trúc và ca âm: `python3 -B review/structure.py`; `TMPDIR="$PWD/review/tmp" PYTHONDONTWRITEBYTECODE=1 python3 -B review/acceptance.py`. Mã và stdout nằm trong `review/`; mọi log actionlint JSON nguyên vẹn ở `review/logs/*-raw.log`. Lần thử cấu trúc đầu dùng tên rút gọn `test registry` nên assertion của reviewer đỏ; sửa bộ đo dùng **tên bước thật đầy đủ**, rồi xác minh không có bước/lệnh nào bị đổi. Không ghi lỗi bộ đo này thành finding sản phẩm.

## Finding

### ruff-khuon-chua-chung-minh-provisioning  [P2]  Hợp đồng Ruff còn nhận bằng chứng sai và bác lời gọi hợp lệ

TỆP/DÒNG: `.claude/dev/ci_dang_ky_test.py:173` (nối dòng), `:194` (fallback sau lỗi lexer), `:209`/`:216`/`:218` (đồng nhất module với tên distribution), `:151`/`:245` (extras), `:271`/`:272` (nhận và chọn probe), `:310` (regex riêng cho bước conditional), `:319` (registry theo đuôi `.py`). Tất cả vị trí là trên `reviewed_sha` đã ghim.

VẤN ĐỀ: Ba chốt đang giữ vẫn dựa vào cách diễn giải argv không nhất quán với tiến trình thực thi. Đây là sai âm/sai dương của **hợp đồng tĩnh Ruff**, trong phạm vi consumer được M7/A7 sửa. Workflow gốc qua cổng nền; bằng chứng này không chứng minh bypass toàn CI.

- **Nhận bằng chứng sai:** H2, `python -m Ruff --version` và module `ruff[all]` đều được nhận `([],3)`, trong khi Python thật rc=1, không có module. H11, `python -m ruff --help --version` rc=0 nhưng in trợ giúp, vẫn được cấp probe; `python -m ruff check --version` rc=2 cũng được cấp probe. H3, requirement có extras `!` hoặc dấu phẩy treo bị parser requirement của pip bác nhưng được gắn `GHIM`. H10, thêm quote chưa đóng vào probe khiến Bash báo syntax error rc=2; fallback `split()` vẫn biến nó thành argv đủ điều kiện. Main trên ba YAML của H2/H3/H10 vẫn **3/3 + 108/108, rc=0**.
- **Bác bằng chứng hợp lệ:** H4, backslash-newline ở giữa `--version` hoặc tên module phải bị loại bỏ, mã lại chèn space làm tách token. H5, dollar-quote của Bash còn bị giữ `$` trong token. Đã đo lại cả hai qua cùng Python/Ruff **0.15.15**, rc=0; đặt shell Bash tường minh trong fixture. H8, một probe có sẵn trước install làm probe đúng **sau** install mất hiệu lực chỉ vì hàm giữ vị trí đầu tiên. H6, lời gọi module `ci_dang_ky_test` có thật từ `.claude/dev` bị báo không có registry; đường tuyệt đối được nhận. Chỉ chạy `--help` để xác minh module, không gọi toàn bộ registry.
- **Sửa tên gói chưa đồng bộ tới mọi đường đọc:** H9, bước echo vô can mang dữ liệu `ruff.toml` được `_phan_loai_cai_ruff` trả `KHONG`, nhưng cùng bước với điều kiện đang có trong workflow lại khiến consumer báo không ghim Ruff. Vị trí `:310` còn đọc chuỗi con thô. Đây là chốt phân loại Ruff, không là chốt env đã bỏ.

ĐÃ THỬ VÁ: **có, một phần trên bản sao**. Sửa H2/H4/H8 theo ba thay đổi đã ghi trong nhật ký; cột additions Python giảm **374→373**, tổng **500→499**, không đụng path thứ ba trong cây packet. Bộ phản chứng vẫn 108/108, H2 bị bác, H4/H8 được nhận đúng. Không tuyên bố phần này đóng các cửa còn lại. **Không đề nghị nâng trần lần thứ tư.**

Hướng sửa phần còn lại **bằng lời**: tách quy tắc tên distribution khỏi tên module/executable; nhận probe theo chế độ thực sự được chọn chứ không chỉ thấy một cờ ở bất kỳ vị trí; bảo toàn ranh giới token khi nối dòng/trích dẫn; lỗi phân tích phải được báo là không phân tích được thay vì cấp bằng chứng từ một argv khác; dùng chung việc xác định lời gọi liên quan ở cả nhánh có/không điều kiện; nhận đúng cách gọi registry được hỗ trợ. Phải chốt rõ miền cú pháp mà consumer nhận, giữ nghĩa vụ M7/A7 và quyết định bỏ env, thay các nhánh trùng trong hai path hiện có để bù số dòng. Chi phí **gói đầy đủ chưa đo**, không giao patch gate để áp mù. Cùng stable finding qua nhiều lượt vẫn cần xử lý theo §12; không biến các sửa nhỏ đã thử thành lời hứa hội tụ.

ĐÃ THỬ NGHIỆM: `review/hunt.py 1` … `11` (mỗi hướng có lệnh, output và kết luận ghi ngay); `review/recheck_hunt.py` xác minh lại 11/11 kết quả sau sửa cách dựng YAML; `review/corroborate.py` đo consumer, main và bản sửa một phần; `review/doi_chieu.py`, `review/do_rang.py`, `review/lexer_ab.py` đo riêng đối chiếu lượt trước và răng. Các lệnh dùng `TMPDIR="$PWD/review/tmp" PYTHONDONTWRITEBYTECODE=1 python3 -B ...`. Log được giữ trong sandbox.

ĐỘ TIN: **cao** cho những đầu vào đã đo. Không khái quát thành hỗ trợ mọi cú pháp shell, mọi package manager hoặc mọi runner.

## Những hướng chuyển điều phối bằng lời — không tính N/P

1. **Đối số dữ liệu bị coi là registry:** lấy fixture echo có sẵn và lời gọi registry có sẵn, đặt lời gọi vào vị trí dữ liệu thay vì vị trí chương trình. So `loi_ruff_ci` với số lần module registry thật được gọi. Vị từ hiện quét mọi token mang đuôi tên tệp; chưa tự soạn payload hay thực thi giả mạo trong lượt này.
2. **Command substitution/backtick/heredoc:** trên bản sao, đặt nguyên lệnh được cấp trong miền shell coi là dữ liệu hoặc lệnh lồng, giữ lệnh cài/probe thực ở ngoài. Đòi bộ đo ghi được ranh giới lệnh và thứ tự thực thi rồi so với `_lenh_tho`. Chưa có probe được cấp cho các miền ấy; **KHÔNG ĐO ĐƯỢC**, không lấy giả thuyết thành finding.
3. **Registry qua biến tên tệp:** lấy đúng đường registry đang có, gán vào biến theo shell được chọn, rồi dùng biến tại vị trí script. Đo argv sau khai triển và consumer tĩnh. Chưa dựng/đo đầu vào này; không suy kết quả từ ca module H6.

## Phạm vi bàn giao và bất biến cuối

- **11 hướng săn mới** có khối và log riêng; nền, A3/A4/actionlint, các mutant cũ, đối chiếu lexer/env và hai phép đo răng không tính vào N. Các hướng kiểm những điều kiện độc lập: ranh giới tên gói; định danh module; ngữ pháp requirement; nối token; kiểu quote Bash; định danh lời gọi registry; ranh giới lệnh của cờ registry; lựa chọn probe khi có nhiều probe; đường conditional; lỗi lexer; ưu tiên chế độ CLI. Không đếm mỗi triệu chứng thành một P2 riêng.
- Tổng: **0 P1 / 1 P2 / 0 P3**, verdict **changes_requested**. Các số nền cũ và lời khai giới hạn trong EVIDENCE được sửa bằng phép đo trong bảng, không tạo finding meta cho đủ số.
- Đã đọc mã `tai-lieu/nhanh_don_duoc_test.py` và bản đã land; chạy nguyên bộ trên bản sao `review/ops/`, giữ nguyên mô hình tin cậy của kênh kết quả, phân biệt lỗi hạ tầng với chết đúng chốt, giới hạn hai lần thử và kiểm các cổng của main. Kết quả xanh của bộ có sẵn không chứng minh mọi nợ lịch sử ngoài phạm vi đã biến mất. Không mở write set sang ops.
- Reviewer: **OpenAI Codex / GPT-6**, `provider=openai_codex`, execution surface **Codex service qua API**, transport **machine**. Không có biên nhận độc lập về snapshot model/effort trong bundle; không suy danh tính runtime từ trường khai của lease hoặc actor GitHub.
- **A1/A5: KHÔNG ĐO ĐƯỢC** vì chủ kho cấm CI. A2 conclusions và A6 live readback cũng chưa đo. Verdict không là quyền merge, không là biên nhận hoàn tất packet. Không gọi mạng, đăng PR/comment, commit, push hoặc sửa trạng thái bên ngoài.
- `review/logs/final-state.json`: HEAD/tree nguyên vẹn, `git status --porcelain --untracked-files=all` rỗng, `git log reviewed_sha..HEAD` rỗng; diff vẫn **+500/−94, đúng hai path**. Mọi bản sao/đột biến nằm trong `review/`; `cay-kho/` và bare mirror không bị sửa.
