verdict: changes_requested
reviewed_sha: 22f0e6f2d5d091f63a71a45ff0906d8b50947546
P1: 0
P2: 2

Kết luận: **changes_requested — 0 P1 / 2 P2 / 1 P3**. Có **9 hướng săn**; đo nền và đối chiếu lượt 7 không tính vào N. Hai finding P2 thuộc phần Ruff trong write set. F/G là nợ đã xác nhận ngoài write set, không cộng lại vào số finding cần vá của #463.

Reviewer: Codex / OpenAI; execution surface: Codex service qua API, transport: machine. Danh tính model/effort cụ thể mà lease dự kiến (`gpt-6-astra`, `xhigh`) không được xác minh bằng receipt runtime trong gói này; không suy định danh từ lời khai của executor.

Neo: tree `d15c46fe3e954e061dd8be43b1ccce3c9e9a628b`; merge-base `bb7013c7669da19304a8769e5b25f8c1f8951e9c`. Cây review chỉ đọc. Đột biến, probe và log ở `review/`; chỉ sửa ROOT/TAM của công cụ nháp `do_rang_luot7.py` theo yêu cầu.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Bằng chứng chạy: `python3 -B review/check_previous.py` → [log](review/logs/doi-chieu.log); `python3 -B review/ops_previous.py` → [log](review/logs/ops-previous.log). Log và kết quả cụ thể được giữ phía dưới.

| lớp | chấm | bằng chứng tự đo và phạm vi |
|---|---|---|
| A | **VÁ SINH LỖI MỚI** | Ba cửa cũ đã có răng riêng: gỡ cách gọi → đúng 4 ca LỌT, gỡ thứ tự → đúng 1, gỡ env → đúng 3; các tập không giao nhau. Mỗi mutant vẫn chạy đủ 102 ca, `phan_chung=False`, `main rc=1`. Tuy nhiên H2/H3/H4/H5/H9 cho thấy hợp đồng còn chặn oan hoặc nhận đầu vào mà Python không khởi động được. Giữ slug của lớp A ở finding bên dưới. |
| B | **CHƯA VÁ** trên head | Hai tệp `ops/kiem_hop_dong_packet*.py` không tồn tại ở HEAD (`cat-file rc=128`); `e7a271b` không là tổ tiên (`rc=1`), chỉ nằm ở nhánh `ops/cap-lease-463`. Bản trích nhánh đó chạy lại **13/13, rc=0**, đọc SPEC-r21/lease hiện tại **rc=0, 0 chốt bỏ qua**. Đó là kiểm bản nhánh phụ, không phải chứng nhận công cụ trên head. Không yêu cầu mở đường dẫn thứ ba. |
| C | **ĐÃ VÁ THẬT** | Fixture hiện là `[_khac, _reg]`. Đổi riêng sentinel `-1` thành `0` → đúng `ruff-ci-da-tach-thieu-ruff` LỌT, **101/102**, `main rc=1`; ba nhóm ca A vẫn đạt. |
| D | **ĐÃ VÁ THẬT** | Đọc SPEC-r21 đã khớp SHA256: phân bổ N=2 ở A1; một suất sau tách và một suất gộp lại; A2=2 lane×2=4 ô, A5=1 lane×2=2 ô, tổng 6. Không có phép chạy CI ở lượt này. |
| E | **ĐÃ VÁ THẬT** về số công bố | Tự chạy **102/102**, đếm **102 tên phân biệt**, Ruff **4/4**; diff thật **346+154=500**, đúng hai đường dẫn, khớp EVIDENCE và thông điệp commit HEAD. Gói không đủ chứng minh cơ chế sinh commit message tự động; chỉ chứng nhận các số tại SHA này khớp. |
| F | **CHƯA VÁ — đúng ràng buộc phạm vi** | Hai mutant ký commit có sẵn: cấu hình Git trung hòa → **2/2** được công nhận; ép ký → **0/2**, r521 chết vì lỗi ngoài chốt. Lease dòng 51–53 chỉ cấp hai tệp; dòng 168–172 nói rõ nghĩa vụ ĐỌC và S1 cấm tệp ops thứ ba. Không vá F trong #463 là đúng, không phải lý do mở lease. |
| G | **CHƯA VÁ — đúng ràng buộc phạm vi** | Mutant có sẵn `dao-chieu-to-tien`, tái gọi cùng bản sao: **GIET lần 1 → GIET lần 2 → KHONG_DO_DUOC sau 2 lần**; thư mục mới lập tức **GIET lần 1**. Tệp ops bằng byte với base và bản `tai-lieu/`; A8/S1 và lease áp dụng như F. Giữ nợ cho packet riêng. |

**Giới hạn của chữ “độc lập”:** đã chứng minh trên các ca đích được giao bằng cả giá trị trả về, số ca và tập tên; không khái quát thành phủ toàn miền đầu vào. H9 là đầu vào cả ba cửa không bắt: pin/probe nguyên vẹn, tên env nằm trong allowlist nhưng giá trị khiến Python dừng trước khi chạy module. Cổng Ruff vẫn trả `[]`. Đây không phải bằng chứng toàn CI vượt qua khi Python chết.

## BẢNG SĂN

Mỗi khối dưới đây được ghi ngay sau phép đo. H7 có biến thể mới là hai lần gọi registry **trong cùng job**, lần mới nằm trước cài, cùng đối chứng đổi tên job; các ca mất/hai job chỉ là đối chứng. H8 đo vòng duyệt **cả ba job** và việc ghép hai bước cài khác nhau qua consumer thật; các phép phân loại dòng có sẵn không được tính là một hướng riêng.

HƯỚNG 1: Kiểm công cụ nháp bằng bộ phản chứng không chạy
  giả thuyết : Nếu phan_chung trả False trước khi chạy ca mà chay vẫn trả tập rỗng, phép đo nháp không chứng minh nền hợp lệ.
  lệnh       : `python3 -B review/run_review.py 1`
  output     :
```text
known-answer mutant: phan_chung returns False before running cases
independent suite: {'return': False, 'count': 0, 'summary': [], 'failed': []}
draft chay(mutant): lot= []
draft baseline predicate not nen: True
Meaning: empty execution is indistinguishable from successful execution in chay(); full four-mutant loop may still fail its target-set checks.
```
  kết luận   : LỖI

HƯỚNG 2: Tên env vô hại và phạm vi bước không cài Ruff
  giả thuyết : Biến thể mới so lượt 7 H5: env tùy ý chỉ dùng làm nhãn, kể cả ở bước checkout, bị chặn oan dù pin/probe không đổi.
  lệnh       : `python3 -B review/run_review.py 2`
  output     :
```text
workflow extra harmless env => ["CI có env ngoài danh sách chứng minh được, nên đích cài Ruff không còn chứng minh được (job: ['gate', 'gate-packet-loop', 'gate-registry'])"]
job extra harmless env => ["CI có env ngoài danh sách chứng minh được, nên đích cài Ruff không còn chứng minh được (job: ['gate-registry'])"]
install-step extra harmless env => ["CI có env ngoài danh sách chứng minh được, nên đích cài Ruff không còn chứng minh được (job: ['gate-registry'])"]
unrelated-step extra harmless env => ["CI có env ngoài danh sách chứng minh được, nên đích cài Ruff không còn chứng minh được (job: ['gate-registry'])"]
helper empty/null benign value: '' ['REVIEW_DISPLAY_LABEL']
helper empty/null benign value: None ['REVIEW_DISPLAY_LABEL']
allowed env identity: []
```
  kết luận   : LỖI

HƯỚNG 3: Cờ hợp lệ của trình Python trước -m
  giả thuyết : Biến thể mới so lớp A: các lời gọi -u/-B/-I đã chạy thật vẫn bị danh sách bốn tiền tố gán thành cài không phân tích được.
  lệnh       : `python3 -B review/run_review.py 3`
  output     :
```text
EXEC ['/usr/local/bin/python3', '-u', '-m', 'ruff', '--version'] rc= 0 output= ruff 0.15.15
classifier: python3 -u -m ruff --version ('KHONG_PHAN_TICH_DUOC', 'python3 -u -m ruff --version')
workflow retains original install and probe: ["CI không ghim Ruff 0.15.15 (job: ['gate-registry'])"]
EXEC ['/usr/local/bin/python3', '-B', '-m', 'ruff', '--version'] rc= 0 output= ruff 0.15.15
classifier: python3 -B -m ruff --version ('KHONG_PHAN_TICH_DUOC', 'python3 -B -m ruff --version')
workflow retains original install and probe: ["CI không ghim Ruff 0.15.15 (job: ['gate-registry'])"]
EXEC ['/usr/local/bin/python3', '-I', '-m', 'ruff', '--version'] rc= 0 output= ruff 0.15.15
classifier: python3 -I -m ruff --version ('KHONG_PHAN_TICH_DUOC', 'python3 -I -m ruff --version')
workflow retains original install and probe: ["CI không ghim Ruff 0.15.15 (job: ['gate-registry'])"]
```
  kết luận   : LỖI

HƯỚNG 4: Probe tương đương về argv nhưng khác cách viết
  giả thuyết : Nếu probe chỉ nhận bằng chuỗi, khoảng trắng/tab và module hợp lệ bị chặn dù thứ tự cài-trước-probe giữ nguyên.
  lệnh       : `python3 -B review/run_review.py 4`
  output     :
```text
EXEC ['ruff', '--version'] rc= 0 output= ruff 0.15.8
probe variant: 'ruff  --version' logical= ['python -m pip install --quiet ruff==0.15.15', 'ruff  --version'] classified= ('GHIM', 'python -m pip install --quiet ruff==0.15.15') order= False
consumer: ["CI không in probe Ruff --version (job: ['gate-registry'])"]
EXEC ['ruff', '--version'] rc= 0 output= ruff 0.15.8
probe variant: 'ruff\t--version' logical= ['python -m pip install --quiet ruff==0.15.15', 'ruff\t--version'] classified= ('GHIM', 'python -m pip install --quiet ruff==0.15.15') order= False
consumer: ["CI không in probe Ruff --version (job: ['gate-registry'])"]
EXEC ['python', '-m', 'ruff', '--version'] rc= 0 output= ruff 0.15.15
probe variant: 'python -m ruff --version' logical= ['python -m pip install --quiet ruff==0.15.15', 'python -m ruff --version'] classified= ('GHIM', 'python -m pip install --quiet ruff==0.15.15') order= False
consumer: ["CI không in probe Ruff --version (job: ['gate-registry'])"]
EXEC ['python3', '-m', 'ruff', '--version'] rc= 0 output= ruff 0.15.15
probe variant: 'python3 -m ruff --version' logical= ['python -m pip install --quiet ruff==0.15.15', 'python3 -m ruff --version'] classified= ('GHIM', 'python -m pip install --quiet ruff==0.15.15') order= False
consumer: ["CI không in probe Ruff --version (job: ['gate-registry'])"]
```
  kết luận   : LỖI

HƯỚNG 5: Ranh giới dòng logic với hai lệnh cùng dòng
  giả thuyết : Biến thể mới so lượt 7 H4: giữ thứ tự cài-trước-probe nhưng ghép bằng && hoặc ; làm chỉ số dòng và phân loại mất ngữ nghĩa.
  lệnh       : `python3 -B review/run_review.py 5`
  output     :
```text
original lines: ['python -m pip install --quiet ruff==0.15.15', 'ruff --version']
join: ' && ' logical: ['python -m pip install --quiet ruff==0.15.15 && ruff --version'] classification: ('KHONG_PHAN_TICH_DUOC', 'python -m pip install --quiet ruff==0.15.15 && ruff --version') probe: False
consumer: ["CI không ghim Ruff 0.15.15 (job: ['gate-registry'])", "CI không in probe Ruff --version (job: ['gate-registry'])", "CI không provision Ruff trước test registry trong cùng job (job chạy test registry: ['gate-registry'])"]
join: '; ' logical: ['python -m pip install --quiet ruff==0.15.15; ruff --version'] classification: ('KHONG_PHAN_TICH_DUOC', 'python -m pip install --quiet ruff==0.15.15; ruff --version') probe: False
consumer: ["CI không ghim Ruff 0.15.15 (job: ['gate-registry'])", "CI không in probe Ruff --version (job: ['gate-registry'])", "CI không provision Ruff trước test registry trong cùng job (job chạy test registry: ['gate-registry'])"]
join: ' \\\n' logical: ['python -m pip install --quiet ruff==0.15.15  ruff --version'] classification: ('KHONG_PHAN_TICH_DUOC', 'python -m pip install --quiet ruff==0.15.15  ruff --version') probe: False
consumer: ["CI không ghim Ruff 0.15.15 (job: ['gate-registry'])", "CI không in probe Ruff --version (job: ['gate-registry'])", "CI không provision Ruff trước test registry trong cùng job (job chạy test registry: ['gate-registry'])"]
Only && and ; preserve two commands; a bare backslash newline merges argv and SHOULD be rejected.
```
  kết luận   : LỖI

HƯỚNG 6: Tín dụng sai khi bỏ riêng chốt ghim ở tầng consumer
  giả thuyết : Nếu fixture pin chỉ đòi có lỗi, chốt probe có thể nhận thay tín dụng cho chốt pin đã bị xóa. Đây là chốt khác sentinel lớp C.
  lệnh       : `python3 -B review/run_review.py 6`
  output     :
```text
removed consumer check pin {'return': True, 'count': 102, 'summary': ['PHẢN CHỨNG: 102/102 đỏ đúng'], 'failed': []}
existing ruff-pin-required input original: ["CI không ghim Ruff 0.15.15 (job: ['gate'])", "CI không in probe Ruff --version (job: ['gate'])"]
existing ruff-pin-required input mutant: ["CI không in probe Ruff --version (job: ['gate'])"]
removed consumer check probe {'return': False, 'count': 102, 'summary': ['PHẢN CHỨNG: 100/102 đỏ đúng'], 'failed': ['ĐỘT BIẾN ruff-version-probe-required: LỌT', 'ĐỘT BIẾN ruff-ci-probe-truoc-cai: LỌT']}
removed consumer check provision {'return': False, 'count': 102, 'summary': ['PHẢN CHỨNG: 98/102 đỏ đúng'], 'failed': ['ĐỘT BIẾN ruff-ci-da-tach-thieu-ruff: LỌT', 'ĐỘT BIẾN ruff-ci-da-tach-ruff-sau-registry: LỌT', 'ĐỘT BIẾN ruff-ci-khong-job-nao-chay-registry: LỌT', 'ĐỘT BIẾN ruff-ci-hai-job-chay-registry: LỌT']}
removed consumer check env {'return': False, 'count': 102, 'summary': ['PHẢN CHỨNG: 99/102 đỏ đúng'], 'failed': ['ĐỘT BIẾN ruff-ci-env-la-cap-workflow: LỌT', 'ĐỘT BIẾN ruff-ci-env-la-cap-job: LỌT', 'ĐỘT BIẾN ruff-ci-env-la-cap-buoc: LỌT']}
```
  kết luận   : LỖI

HƯỚNG 7: Nhiều lời gọi registry trong/cross-job và đổi định danh job
  giả thuyết : Nếu consumer chỉ nhận tên job cố định hoặc bỏ qua lần chạy registry sớm hơn trong cùng job thì provisioning sai vẫn xanh.
  lệnh       : `python3 -B review/run_review.py 7`
  output     :
```text
duplicate registry to gate ["CI không provision Ruff trước test registry trong cùng job (job chạy test registry: ['gate', 'gate-registry'])"]
duplicate registry to gate-registry ["CI không provision Ruff trước test registry trong cùng job (job chạy test registry: ['gate-registry'])"]
duplicate registry to gate-packet-loop ["CI không provision Ruff trước test registry trong cùng job (job chạy test registry: ['gate-registry', 'gate-packet-loop'])"]
remove only registry: ['CI không provision Ruff trước test registry trong cùng job (job chạy test registry: KHÔNG CÓ)']
rename job preserves behavior: []
```
  kết luận   : KHÔNG PHẢI LỖI

HƯỚNG 8: Cài lần hai và kiểm mọi job sau khi đã thấy pin hợp lệ
  giả thuyết : Nếu tồn tại pin tốt che cài không ghim ở job khác hoặc cuối job thì phép tổng hợp trả sạch sai.
  lệnh       : `python3 -B review/run_review.py 8`
  output     :
```text
unpin existing install in gate ["CI không ghim Ruff 0.15.15 (job: ['gate'])", "CI không in probe Ruff --version (job: ['gate'])"]
unpin existing install in gate-registry ["CI không ghim Ruff 0.15.15 (job: ['gate-registry'])", "CI không in probe Ruff --version (job: ['gate-registry'])", "CI không provision Ruff trước test registry trong cùng job (job chạy test registry: ['gate-registry'])"]
unpin existing install in gate-packet-loop ["CI không ghim Ruff 0.15.15 (job: ['gate-packet-loop'])", "CI không in probe Ruff --version (job: ['gate-packet-loop'])"]
extra unpinned install after registry: ["CI không ghim Ruff 0.15.15 (job: ['gate-registry'])"]
extra pinned install after registry: []
```
  kết luận   : KHÔNG PHẢI LỖI

HƯỚNG 9: Giá trị không hợp lệ dưới tên env đã được cho phép
  giả thuyết : Biến thể mới so lượt 7 H5: giữ tên có sẵn PYTHONUTF8/PYTHONIOENCODING, chỉ đổi giá trị, có thể làm Python chết trước khi cài nhưng cả ba chốt mới vẫn cho qua.
  lệnh       : `python3 -B review/env_values.py`
  output     :
```text
allowed key abnormal value: PYTHONUTF8 '2'
env guard: []
consumer: []
real Python startup: rc= 1 output= Fatal Python error: preconfig_init_utf8_mode: invalid PYTHONUTF8 environment variable value
Python runtime state: preinitializing
allowed key abnormal value: PYTHONIOENCODING 'not-a-codec'
env guard: []
consumer: []
real Python startup: rc= 1 output= Fatal Python error: init_stdio_encoding: failed to get the Python codec name of the stdio encoding
Python runtime state: core initialized
LookupError: unknown encoding: not-a-codec

Current thread 0x00007f2362dfa080 (most recent call first):
  <no Python frame>
```
  kết luận   : LỖI

## Đối chiếu A/C — số đo ban đầu (không tính N)

Lệnh: `TMPDIR="$PWD/review/tmp" PYTHONDONTWRITEBYTECODE=1 python3 -B do_rang_luot7.py`.
Script đã được sửa ROOT về `cay-kho/`, TAM về `review/tmp/rang-luot7/` trước khi chạy.
NEN (chua dot bien): lot=[]
DAT  go-chot-cach-goi: lot=['nhan-chay-module', 'nhan-chay-module-py3', 'nhan-chay-uv-run', 'nhan-chay-uvx']
DAT  go-chot-thu-tu: lot=['ruff-ci-probe-truoc-cai']
DAT  go-chot-env: lot=['ruff-ci-env-la-cap-buoc', 'ruff-ci-env-la-cap-job', 'ruff-ci-env-la-cap-workflow']
DAT  lopC-sentinel-ruff-i-0: lot=['ruff-ci-da-tach-thieu-ruff']
TONG: DAT — bon chot co rang RIENG, phan biet duoc bang dau vao

## ĐỐI CHIẾU LƯỢT TRƯỚC — bằng chứng tự đo
```text
A/C: independent capture with bool, case count, exact failed set, then actual main
BASE {'return': True, 'count': 102, 'summary': ['PHẢN CHỨNG: 102/102 đỏ đúng'], 'failed': []}
go-chot-cach-goi {'return': False, 'count': 102, 'summary': ['PHẢN CHỨNG: 98/102 đỏ đúng'], 'failed': ['ĐỘT BIẾN nhan-chay-module: LỌT', 'ĐỘT BIẾN nhan-chay-module-py3: LỌT', 'ĐỘT BIẾN nhan-chay-uv-run: LỌT', 'ĐỘT BIẾN nhan-chay-uvx: LỌT']}
actual main rc= 1 summary= ['RUFF CI: 4/4 hợp đồng', 'PHẢN CHỨNG: 98/102 đỏ đúng', 'TỔNG: ĐỎ']
go-chot-thu-tu {'return': False, 'count': 102, 'summary': ['PHẢN CHỨNG: 101/102 đỏ đúng'], 'failed': ['ĐỘT BIẾN ruff-ci-probe-truoc-cai: LỌT']}
actual main rc= 1 summary= ['RUFF CI: 4/4 hợp đồng', 'PHẢN CHỨNG: 101/102 đỏ đúng', 'TỔNG: ĐỎ']
go-chot-env {'return': False, 'count': 102, 'summary': ['PHẢN CHỨNG: 99/102 đỏ đúng'], 'failed': ['ĐỘT BIẾN ruff-ci-env-la-cap-workflow: LỌT', 'ĐỘT BIẾN ruff-ci-env-la-cap-job: LỌT', 'ĐỘT BIẾN ruff-ci-env-la-cap-buoc: LỌT']}
actual main rc= 1 summary= ['RUFF CI: 4/4 hợp đồng', 'PHẢN CHỨNG: 99/102 đỏ đúng', 'TỔNG: ĐỎ']
lopC-sentinel-ruff-i-0 {'return': False, 'count': 102, 'summary': ['PHẢN CHỨNG: 101/102 đỏ đúng'], 'failed': ['ĐỘT BIẾN ruff-ci-da-tach-thieu-ruff: LỌT']}
actual main rc= 1 summary= ['RUFF CI: 4/4 hợp đồng', 'PHẢN CHỨNG: 101/102 đỏ đúng', 'TỔNG: ĐỎ']

B: branch tool attribution
git cat-file -e HEAD:ops/kiem_hop_dong_packet.py rc= 128 fatal: path 'ops/kiem_hop_dong_packet.py' does not exist in 'HEAD'
git cat-file -e HEAD:ops/kiem_hop_dong_packet_test.py rc= 128 fatal: path 'ops/kiem_hop_dong_packet_test.py' does not exist in 'HEAD'
git merge-base --is-ancestor e7a271b HEAD rc= 1 
git branch -a --contains e7a271b rc= 0 remotes/origin/ops/cap-lease-463

D: current frozen spec constraints
209 **Ràng buộc chi phí CI (chỉ thị chủ kho 11-09-2026).** Packet này được chi **đúng `N = 2`** lượt
210 `workflow_dispatch`. **PHÂN BỔ hai suất ấy nêu ĐÚNG MỘT CHỖ — tại `A1`** — và chỗ này chỉ nêu
258 `N = 2` vừa được giải phóng đúng một suất (nền không còn phải chi), nên **suất ấy dành cho đột biến
507 **Số ô SUY TỪ CHIỀU, không khai rời:** `A2` = 2 lane × {trước, sau} = **4** ô (cặp dispatch có thể
508 `KHÔNG ĐO ĐƯỢC` theo `A1`); `A5` = 1 lane × {trước, sau} = **2** ô; tổng **6**. Một manifest dùng
601 `additions` ≤ **500** (ngoại lệ CÓ PHẠM VI, xem dưới; đây là trần hiệu lực DUY NHẤT của packet). Đường thứ ba ⇒ **DỪNG và hỏi chủ kho**,
615 `ghim-noi-dong` ⇒ survivor `l3-bo-noi-dong-logic` của reviewer sống lại. `so_tep = 2` **không** nới — bán kính ảnh hưởng vẫn là chốt, và `S1` nguyên vẹn.

E: counts from actual baseline log and actual diff
named= 102 unique= 102
ĐĂNG KÝ: 21/21
LAUNCHER WINDOWS: 4/4 hợp đồng
RUFF CI: 4/4 hợp đồng
PHẢN CHỨNG: 102/102 đỏ đúng
TỔNG: ĐẠT
git diff --numstat bb7013c7669da19304a8769e5b25f8c1f8951e9c HEAD rc= 0 346	88	.claude/dev/ci_dang_ky_test.py
154	6	.github/workflows/ci.yml

F/G: scope and unchanged bytes
git diff --exit-code bb7013c7669da19304a8769e5b25f8c1f8951e9c HEAD -- ops/nhanh_don_duoc_test.py rc= 0 
tai-lieu/nhanh_don_duoc_test.py b56636d9c26d9b0f7b537d71e9a7edc7ef446e8c51ef0466fbc849a064497134
cay-kho/ops/nhanh_don_duoc_test.py b56636d9c26d9b0f7b537d71e9a7edc7ef446e8c51ef0466fbc849a064497134
51 write_set:
52   - .github/workflows/ci.yml
53   - .claude/dev/ci_dang_ky_test.py
168      review nào chạy trên nó (Codex chỉ chạy trên `94c416d`). Đây là nghĩa vụ ĐỌC, KHÔNG mở write
169      set; phát hiện nào cần vá thì đi bằng packet riêng.'
172   - 'S1 — đường dẫn thứ BA trong write set, kể cả `ops/nhanh_don_duoc_test.py`. Chủ kho đã chọn

H6 consequence: additional installation copied from existing workflow, unpin only
original consumer: ["CI không ghim Ruff 0.15.15 (job: ['gate-registry'])"]
mutant consumer: []
mutant actual main on original workflow: rc= 0 ['RUFF CI: 4/4 hợp đồng', 'PHẢN CHỨNG: 102/102 đỏ đúng', 'TỔNG: ĐẠT']
```

<!-- Khối này do `review/ops_previous.py` sinh; ở lần PHÁT LẠI nó hỏng vì mkdir không
idempotent, nên được ĐO LẠI sau đó và chèn về đúng vị trí trong trình tự gốc. -->
## Đối chiếu F/G — tái lập bằng mã/đột biến có sẵn; không tính N
```text
G: repeat the SAME existing product mutant in one copy; no fabricated channel
existing mutant= dao-chieu-to-tien target= ('T1',)
call= 1 result= ('GIET', '', 1)
call= 2 result= ('GIET', '', 2)
call= 3 result= ('KHONG_DO_DUOC', "ban ghi khong neo dung luot: T1 | rc_con=1 | stderr[-200:]=''", 2)
fresh copy= ('GIET', '', 1)
F: existing two signing mutants under controlled forced-sign config
DOT BIEN TU KIEM go-tat-ky-o-kho-mutant | r506 | TIN DUNG GIA: ca chet vi loi VO CAN ['r521']
DOT BIEN TU KIEM src-tat-ky-khong-chay | r506 | TIN DUNG GIA: ca chet vi loi VO CAN ['r521']
mode= forced result= (0, 2)
DOT BIEN TU KIEM go-tat-ky-o-kho-mutant | r506 | 1/1
DOT BIEN TU KIEM src-tat-ky-khong-chay | r506 | 1/1
mode= neutral result= (2, 0)
```

## A2/A3/A4 cục bộ — không tính N
```text
structure base -> HEAD {'jobs': True, 'steps': True, 'prefix9': True, 'on': True, 'concurrency': True, 'A4': True}
existing workflow mutation job-if {'jobs': False, 'steps': True, 'prefix9': True, 'on': True, 'concurrency': True, 'A4': True}
existing workflow mutation prefix-delete {'jobs': True, 'steps': True, 'prefix9': False, 'on': True, 'concurrency': True, 'A4': True}
existing workflow mutation on-delete {'jobs': True, 'steps': True, 'prefix9': True, 'on': False, 'concurrency': True, 'A4': True}
existing workflow mutation timeout-delete {'jobs': False, 'steps': True, 'prefix9': True, 'on': True, 'concurrency': True, 'A4': False}
moved steps exact dict matches: [('packet-loop selftest', 1), ('test registry (phạm vi + các bộ chưa được nối)', 1)]
gate remaining order: True
step counts base/head: 40 {'gate': 38, 'gate-registry': 10, 'gate-packet-loop': 10}
actionlint -version rc= 0 1.7.12
installed by downloading from release page
built with go1.26.1 compiler for linux/amd64
shellcheck --version rc= 0 ShellCheck - shell script analysis tool
version: 0.9.0
license: GNU General Public License, version 3
website: https://www.shellcheck.net
actionlint ci.yml base rc= 0 diagnostics= []
actionlint ci.yml head rc= 0 diagnostics= []
actionlint existing workflow mutation existing-error rc= 1 diagnostic count= 1
messages= [('shellcheck', "shellcheck reported issue in this script: SC1003:info:44:50: Want to escape a single quote? echo 'This is how it'\\''s done'")]
actionlint existing workflow mutation added-error rc= 1 diagnostic count= 2
messages= [('shellcheck', 'shellcheck reported issue in this script: SC2086:info:12:27: Double quote to prevent globbing and word splitting'), ('shellcheck', "shellcheck reported issue in this script: SC1003:info:44:50: Want to escape a single quote? echo 'This is how it'\\''s done'")]
```

### A3 — đa tập chuẩn hóa (bỏ tọa độ, neo đúng thân run)
```text
ci.yml: normalized before=0, after=0, added=0, removed=0, equal=True
ops-don-ref.yml: normalized before=1, after=2, added=1, removed=0, equal=False
added x1: ('ops-don-ref.yml', 'shellcheck', 'shellcheck reported issue in this script: SC2086:info: Double quote to prevent globbing and word splitting')
```

## Bổ sung phép đo nền và lớp B (không tính N)

`review/logs/doc-claims.log`:
```text
ok=true; files_scanned=107; flags=0; advisory_count=376; layers_skipped=0; strict=true; EXIT_CODE=0
Toàn bộ 2.788 dòng: review/logs/doc-claims.log
```
`review/logs/doctrine-scan.log`:
```text
doctrine-scan: sạch — đã quét 7 tệp, 0 chỗ chép doctrine

EXIT_CODE=0
```
`TMPDIR="$PWD/review/tmp" PYTHONDONTWRITEBYTECODE=1 python3 -B review/kiem_hop_dong_packet_test.py` (trích từ e7a271b, ngoài head):
```text
ĐẠT   t1-cap-khop-phai-DAT                         rc=0 (mong 0)
ĐẠT   t2-revision-truong-lech-tieu-de              rc=2 (mong 2)
ĐẠT   t3-dac-ta-neu-tran-HAI-lan                   rc=3 (mong 3)
ĐẠT   t4-lease-CHEP-nguong-vao-muc-A8              rc=4 (mong 4)
ĐẠT   t5-spec_hash-khong-khop                      rc=5 (mong 5)
ĐẠT   t6-thieu-truong-revision-o-lease             rc=6 (mong 6)
ĐẠT   t8-dinh-danh-ADR-KHONG-bi-bat                rc=0 (mong 0)
ĐẠT   t9-ADR-tha-nhung-nguong-cung-muc-VAN-bi-bat  rc=4 (mong 4)
ĐẠT   t10-tham-chieu-cung-so-voi-nguong            rc=4 (mong 4)
ĐẠT   t11-vi-pham-CHI-o-dieu_kien_dung             rc=4 (mong 4)
ĐẠT   t7-tham-chieu-trong-muc-A8-KHONG-bi-bat      rc=0 (mong 0)
ĐẠT   dot-bien-noi-danh-sach-CHO-PHEP              rc=0 (nới danh sách ⇒ t4 phải THÔI đỏ; nếu vẫn 4 thì t4 đang đo thứ khác)
ĐẠT   dot-bien-bo-khoi-nghia-vu                    rc=4 (bo mot khoi ⇒ chot 5 phai CHAN [4])

PHẢN CHỨNG CỔNG: 13/13 đạt
```
Bộ hợp đồng từ nhánh phụ chạy với SPEC-r21/LEASE-exec-2r10: rc=0, 0 chốt bỏ qua; vẫn tự khai chỉ đếm một mẫu Markdown. Không dùng kết quả nhánh phụ để chứng nhận công cụ tồn tại trên HEAD.

Bộ ops đầy đủ (từng bộ cục bộ, không chạy CI):
`TMPDIR="$PWD/review/tmp" PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL="$PWD/review/gitconfig-empty" GIT_CONFIG_NOSYSTEM=1 python3 -B cay-kho/ops/nhanh_don_duoc_test.py`
```text
DOT BIEN TU KIEM tu-dot-bien-chuan-hoa-rc-khac | r516 | 1/1
DOT BIEN TU KIEM tu-kiem-gop-hai-lop-ngoai-le | r516 | 1/1
DOT BIEN TU KIEM tu-kiem-bo-ghi-nhan-loi-vo-can | r516 | 1/1
TU KIEM co dot bien rieng: 23/23 nhom bat buoc · dot bien giet 76/76
8/8
MUTANT: giet = 10 · khong giet = 0 · khong do duoc = 0 / tong 10

EXIT_CODE=0
```

## Kiểm tra bất biến cuối lượt
```text
git rev-parse HEAD HEAD^{tree} rc= 0 output= '22f0e6f2d5d091f63a71a45ff0906d8b50947546\nd15c46fe3e954e061dd8be43b1ccce3c9e9a628b'
git status --porcelain rc= 0 output= ''
git log --oneline 22f0e6f2d5d091f63a71a45ff0906d8b50947546..HEAD rc= 0 output= ''
git merge-base HEAD origin/master rc= 0 output= 'bb7013c7669da19304a8769e5b25f8c1f8951e9c'
git rev-parse --is-shallow-repository rc= 0 output= 'false'
git config --get core.abbrev rc= 0 output= '7'
git diff --numstat bb7013c7669da19304a8769e5b25f8c1f8951e9c HEAD rc= 0 output= '346\t88\t.claude/dev/ci_dang_ky_test.py\n154\t6\t.github/workflows/ci.yml'
bare local heads= 365 snapshot remote-tracking= 365 equal name+OID= True missing= 0 extra= 0
sha256 tai-lieu/SPEC-r21.md decdb1a1ae794508f0be6d680342bbf7c46b7353e0708f16b522567e8cc56d96
sha256 tai-lieu/LEASE-exec-2r10.yaml 46182004162a051847bd2c80db489c43021c2f543e86b18d13a4651c85404db3
```


## BẢNG ĐO

| khẳng định | PR khai / hợp đồng | đo được | khớp? |
|---|---|---|---|
| HEAD | `22f0e6f2d5d091f63a71a45ff0906d8b50947546` | đúng ở đầu và cuối | Có |
| merge-base | `bb7013c7669da19304a8769e5b25f8c1f8951e9c` | đúng | Có |
| spec SHA256 | `decdb1a1ae794508f0be6d680342bbf7c46b7353e0708f16b522567e8cc56d96` | đúng | Có |
| lease SHA256 | `46182004162a051847bd2c80db489c43021c2f543e86b18d13a4651c85404db3` | đúng | Có |
| đăng ký | 21/21 | 21/21 | Có |
| launcher Windows, hợp đồng tĩnh | 4/4 | 4/4 | Có; không phải chạy Windows |
| Ruff CI, hợp đồng tĩnh | 4/4 | 4/4 | Có trên workflow gốc |
| phản chứng | 102/102 | 102/102, 102 tên phân biệt, rc=0 | Có |
| Ruff F | All checks passed | `python3 -B -m ruff check --no-cache --select F ...` đạt | Có |
| A8 / ci_dang_ky_test.py | +346 / −88 | +346 / −88 | Có |
| A8 / ci.yml | +154 / −6 | +154 / −6 | Có |
| A8 tổng | 500 additions, 2 tệp, trần 500 | 500 / 500, 2 tệp | Có; hết biên dòng |
| Răng cách gọi / thứ tự / env / sentinel | 4 / 1 / 3 / 1 ca đích, không chồng | đúng tập tên; main mỗi mutant rc=1 | Có trong miền ca đã giao |
| Chốt ghim được phản chứng bảo vệ | `ruff-pin-required` được tính ĐỎ đúng | tắt riêng chốt ghim: main vẫn rc=0, 102/102 | **Không** |
| A2 phần cấu trúc | chỉ dời hai bước, bảo toàn lệnh | hai dict bước khớp nguyên vẹn, mỗi bước 1 bản; 40 → 38+10+10, tăng đúng 18 bước setup | Có ở mức cấu trúc |
| A2 kết quả CI hai lane | cần tập `(tên bước,nền,conclusion)` | không chạy CI | **KHÔNG ĐO ĐƯỢC** |
| A3 / A4 | cùng điều kiện, tiền tố 9, timeout 60 | các so sánh True; đột biến if trần / mất setup / mất on / mất timeout đều bị phép riêng bắt | Có tại chỗ |
| actionlint ci.yml A/B | delta chẩn đoán bằng 0 | 0 → 0, đa tập bằng nhau; actionlint 1.7.12, shellcheck 0.9.0 | Có với toolchain này |
| Ca âm actionlint | thêm lỗi vào workflow đã lỗi phải thấy delta | `ops-don-ref.yml`: rc 1 → 1; SC1003 → SC1003+SC2086; đa tập +1 / −0 | Có; ca âm đổi màu đúng |
| doc-claims-check sandbox | rc=0 | rc=0, 107 tệp, 0 flags, 376 advisory | Có; không đo lại cây nguồn bên ngoài |
| doctrine-scan | adapter đòi sạch | rc=0, 7 tệp, 0 chỗ | Có |
| mirror không shallow | false | false; core.abbrev=7 | Có |
| mirror nhận đủ ref đã cấp | 365; hai danh sách khớp | 365 tên+OID ở bare = 365 remote-tracking ở snapshot | Có trong sandbox |
| GitHub trực tiếp / source ref completeness | không đo được offline | không đọc bên ngoài sandbox | **KHÔNG ĐO ĐƯỢC** |
| ops đã land | nghĩa vụ đọc, ngoài write set | cùng hash với base/bản cấp; full suite rc=0: 8/8, 10/10, 23/23 nhóm, 76/76 tự đột biến dưới Git trung hòa | Đã tự kiểm; F/G vẫn tái lập riêng |
| A1 / A5 | KHÔNG ĐO ĐƯỢC, chủ kho cấm CI | không phóng CI, không lấy thời gian head khác | **KHÔNG ĐO ĐƯỢC** |
| A6 ruleset | cần readback required contexts | không có readback GitHub trong phạm vi đóng | **KHÔNG ĐO ĐƯỢC** |
| cây review nguyên trạng | không dirty/commit mới | status rỗng; log SHA..HEAD rỗng; HEAD/tree giữ nguyên | Có |

## Finding

### ruff-khuon-chua-chung-minh-provisioning  [P2]  Ba cửa chỉ phủ các cách viết đã liệt kê, còn chặn oan và có đầu vào không cửa nào bắt

TỆP/DÒNG: `cay-kho/.claude/dev/ci_dang_ky_test.py:161` (`_TIEN_TO_CHAY`), `:168` (`_env_la`), `:174` (`_dong_logic`), `:200` (nhận lời gọi), `:246` (so probe nguyên chuỗi), `:304` (gom env mọi bước).

VẤN ĐỀ: Giữ slug của lớp A lượt 7; không tách từng triệu chứng thành nhiều P2. Bản vá đóng các ca cũ nhưng chưa có một hợp đồng thống nhất giữa nhận lời gọi, nhận probe và môi trường thực thi:

- **Cách gọi:** thêm chẩn đoán `python3 -u/-B/-I -m ruff --version` vào bước registry, giữ nguyên install và probe trước đó. Cả ba chạy thật rc=0, in `ruff 0.15.15`; consumer lại báo không ghim Ruff. Cờ của trình Python làm lời gọi chạy thành “cài không phân tích được”.
- **Probe:** đổi riêng khoảng trắng/tab giữa hai argv, hoặc dùng lời gọi module mà `_TIEN_TO_CHAY` vừa công nhận. Phân loại cả thân run vẫn `GHIM`, nhưng `_probe_sau_ghim=False` vì so chuỗi nguyên văn. Với module, chạy thật rc=0, Ruff 0.15.15. Trong môi trường reviewer, executable `ruff` trên PATH là 0.15.8 còn module là 0.15.15; phép khoảng trắng chỉ chứng minh argv tương đương, không dùng nó để khai đã provision 0.15.15 trên CI.
- **Dòng logic:** giữ thứ tự hai lệnh nhưng ghép bằng `&&` hoặc `;` → một dòng bị gán KPT, probe False và ba thông điệp lỗi. Đây là cùng thứ tự shell ở cách viết khác. Đối chứng nối bằng backslash thuần là ghép argv, không còn hai lệnh và bị từ chối đúng; không dùng đối chứng đó làm lỗi. Không chạy pip hay suy thành bằng chứng CI của dạng ghép này.
- **Env:** một tên chỉ dùng làm nhãn `REVIEW_DISPLAY_LABEL`, kể cả ở bước checkout không cài/chạy Ruff, làm cổng đỏ. Ngược lại, đổi **giá trị** các tên sẵn có thành `PYTHONUTF8=2` hoặc codec không tồn tại làm Python thật dừng rc=1 trước module, trong khi `_env_la=[]` và `loi_ruff_ci=[]`. Danh sách tên vừa coi env không liên quan là mất bằng chứng, vừa coi tên quen là đủ bằng chứng. Đầu vào thứ hai không bị bất kỳ cửa A nào bắt.

Ảnh hưởng đo được là false positive/false negative của hợp đồng tĩnh Ruff. Không có bằng chứng bypass toàn CI; hai giá trị env xấu làm tiến trình Python đỏ. Workflow hiện tại vẫn qua cổng nền.

ĐÃ THỬ VÁ: **không — chỉ nêu hướng bằng lời**, không đính patch gate. Dùng chung cách nhận dạng argv cho phân loại lời gọi và probe; xác định rõ miền shell được hỗ trợ và phạm vi env thực sự áp dụng cho bước cài/chạy, thay vì mở thêm danh sách tùy tiện. Hướng dòng: hợp nhất hai đoạn tách token hiện đang lặp trong `_phan_loai_cai_ruff` và `_probe_sau_ghim`, thay các predicate hiện có; không thêm đường dẫn. Chưa có gói vá nên **chưa đo chi phí dòng**, không coi hướng này là patch đã đạt A8; executor phải đưa một gói thay thế có additions **≤500**, hoặc quay lại thiết kế theo §12. Không đề nghị nới lần thứ tư.

ĐÃ THỬ NGHIỆM: `python3 -B review/run_review.py 2`, `3`, `4`, `5`; `python3 -B review/env_values.py`. Kết quả nguyên văn trong H2–H5/H9 và `review/logs/h*.log`. Phần thứ tự cũ, cách gọi bốn tiền tố cũ, env nguy hiểm ba cấp cũ đo riêng trong `review/check_previous.py`, không tính lại vào N.

ĐỘ TIN: **cao** với các đầu vào đã đo; chưa tuyên bố phủ mọi shell/env.

### ruff-phan-chung-ghim-nhan-tin-dung-tu-probe  [P2]  Xóa chốt ghim ở consumer vẫn qua cả main và 102 phản chứng

TỆP/DÒNG: `cay-kho/.claude/dev/ci_dang_ky_test.py:314` (chốt ghim), `:301` (probe phụ thuộc nhãn GHIM), `:665` (`ruff-pin-required`).

VẤN ĐỀ: Fixture pin chỉ kiểm có ít nhất một thông điệp lỗi. Bỏ pin ở bản cài đầu làm **cả ghim lẫn probe** lỗi do nhãn không còn GHIM. Đột biến chính điều kiện kiểm ghim ở dòng 314 thành đúng giữ chốt probe: `ruff-pin-required` vẫn được ghi “ĐỎ đúng”; **toàn main rc=0, Ruff 4/4, PHẢN CHỨNG 102/102**. Đây không phải đột biến tương đương: sao chép một bước cài đã có xuống cuối job registry, chỉ bỏ ghim ở bản sao, consumer gốc báo lỗi ghim còn consumer mutant trả `[]`. Như vậy mất kiểm tra ghim có hậu quả sản phẩm thật mà suite không bắt. Các ca BẢNG NHÃN kiểm helper chưa bảo vệ đường consumer này.

ĐÃ THỬ VÁ: **không — hướng bằng lời, trung hòa dòng**. Thay predicate `bool(danh_sách_lỗi)` của `ruff-pin-required` bằng yêu cầu có đúng loại thông điệp ghim của job bị đột biến, ngay trên dòng predicate hiện có; **0 dòng thêm** nếu giữ bố cục hai dòng của ca. Ca hiện có khi ấy phải LỌT khi bỏ chốt ghim, dù còn lỗi probe. Có thể dùng dữ liệu H8 làm đối chứng lỗi ghim độc lập nếu gộp vào bảng ca hiện có và bù đủ dòng. Không đề nghị sửa workflow hay tệp thứ ba.

ĐÃ THỬ NGHIỆM: `python3 -B review/run_review.py 6` → chốt ghim bị xóa vẫn **102/102**; xóa riêng các chốt probe/provision/env cho **100/102**, **98/102**, **99/102**, đúng các ca tương ứng. `python3 -B review/check_previous.py` → mutant main **rc=0**; workflow có thêm bản cài không ghim: gốc **1 lỗi**, mutant **0 lỗi**. Chưa chạy gói vá vì chỉ giao hướng bằng lời.

ĐỘ TIN: **cao**.

### rang-luot7-nhan-bo-khong-chay-la-nen-sach  [P3]  Công cụ nháp bỏ giá trị trả về và không đòi bằng chứng ca đã chạy

TỆP/DÒNG: `do_rang_luot7.py:42`, `:45`, `:50` — hiện vật ngoài write set, không phải mã đã commit trong PR.

VẤN ĐỀ: `chay()` bỏ kết quả `phan_chung()` và chỉ trích các dòng kết thúc LỌT. Chèn `return False` trước KQ trong bản sao mã có sẵn → bộ độc lập đo **False, 0 ca, 0 dòng tổng**, nhưng công cụ nháp trả `lot=[]` và điều kiện nền `not nen` là True. Tập LỌT rỗng không đủ để chứng nhận một lần thực thi sạch.

Phạm vi được giới hạn: **không** khẳng định toàn script bốn mutant báo ĐẠT với đột biến không chạy ca; so tập đích ở vòng sau vẫn có thể làm nó đỏ. Bốn số đo được PR khai ở head hiện tại đã được reviewer chứng nhận lại bằng công cụ riêng (giá trị trả về + số ca + tập lỗi + main rc), nên finding này không phủ nhận các số đó. Đây là lỗi chất lượng hiện vật đo, không là blocker P2 sản phẩm.

ĐÃ THỬ VÁ: **không — hướng bằng lời**. Trả riêng trạng thái đã thực thi hợp lệ và tập ca sai; đòi có kết quả tổng, số ca dương, tên phân biệt, và giá trị trả về nhất quán. Kiểm tra nền đòi True; đo mutant phải cho phép False nhưng đòi đủ bằng chứng và so đúng tập đích. Sửa công cụ nháp **0 dòng vào hai tệp A8**; không đưa hiện vật này vào write set của packet.

ĐÃ THỬ NGHIỆM: `python3 -B review/run_review.py 1` → `return=False, count=0`, draft `lot=[]`, `not nen=True`. Sau đó chạy script gốc đã ghim ROOT/TAM **rc=0**, và đối chiếu độc lập bằng `review/check_previous.py` đủ 102 ca cho từng mutant.

ĐỘ TIN: **cao**, chỉ trong phạm vi `chay()` và chốt nền đã đo.

## Hướng chuyển điều phối bằng lời — chưa đo, không tính N hoặc P

1. **Here-document / dòng dữ liệu bị hiểu là lệnh.** Đọc `:174–184`, `:234–251` thấy không có trạng thái thân here-document; dòng không nhắc Ruff bị bỏ qua. Công thức tái hiện: lấy bước cài và probe đang có, đặt hai dòng nguyên vẹn vào phần dữ liệu của một here-document được một lệnh chỉ in dữ liệu tiêu thụ; giữ bước registry phía sau. So consumer với nhật ký chạy shell trong môi trường chưa có Ruff. Mong đợi cổng từ chối nếu không có lần cài/probe thực thi. Reviewer không tự soạn payload; **KHÔNG ĐO ĐƯỢC** hành vi động này.
2. **Env ngoài ba map trực tiếp.** `:304` chỉ truyền workflow, job và các step; không đi vào cấu hình env của container hoặc thay đổi môi trường do bước trước phát ra. Công thức: trên bản sao workflow, chuyển thiết lập đổi đích cài vào env của container, giữ ba map trực tiếp và argv Ruff nguyên trạng; đo đích cài bằng tiến trình thật trong container rồi so với cổng. Reviewer không tạo cấu hình giả mạo hoặc chạy container; **KHÔNG ĐO ĐƯỢC**. Đây là việc điều phối viết probe và đo, không phải kết luận đã có bypass.

## Giới hạn và ràng buộc bàn giao

- A1/A5 và conclusions CI của A2, ruleset A6: **KHÔNG ĐO ĐƯỢC** trong lượt này. Không `workflow_dispatch`, không full CI, không Windows CI, không suy từ lượt/head khác. Bộ ops cục bộ đã chạy riêng không được gọi là full CI.
- Đọc/ghi phục vụ review nằm trong sandbox; không dùng nguồn GitHub trực tiếp. Hai mirror local khớp không chứng minh kho nguồn đã nhận mọi ref GitHub tại thời điểm review.
- F/G vẫn là nợ thật của tệp đã land; lập luận “không sửa trong write set #463” đúng lease và A8/S1. B chưa hiện diện trên head cũng không tạo quyền thêm đường dẫn ops.
- `actionlint` cục bộ là 1.7.12, workflow ghim 1.7.7. Phép A/B dùng cùng 1.7.12 và shellcheck 0.9.0; chưa chứng nhận lại dưới 1.7.7. Khác phiên bản được khai, không suy kết quả CI.
- H5 không chạy installer; H4 phân biệt phiên bản executable và module như đã ghi. Bộ Git đầy đủ được chạy với global/system trung hòa; ảnh hưởng cấu hình ép ký được đo riêng ở F.
- Rig so cấu trúc ban đầu tự ném KeyError khi xóa timeout. Đã sửa **rig review** dùng `.get` rồi chạy lại; không ghi lỗi rig đó thành lỗi sản phẩm. Baseline doc-claims dài được giữ toàn bộ ở log và rút gọn trong verdict; các khối hướng vẫn được bảo toàn.
- Không có gói vá được chứng nhận A8. Mọi hướng sửa ở trên là lời mô tả cho executor tự dẫn xuất, không là quyền sửa branch. Không nới trần, không xin đường dẫn thứ ba.
- Verdict là tệp bàn giao tại sandbox theo PROMPT; chưa đăng PR hay ghi state/receipt từ phiên này. Quy tắc đăng PR của adapter không mở quyền ghi ra ngoài phạm vi đóng người dùng đã giao.
