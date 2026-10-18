verdict: changes_requested
reviewed_sha: db1ed4dda529eb30806ecb053d2eef9933e188b1

Có **2 finding P2 cần sửa và 2 P3 cần quyết định**; không phát hiện P0/P1 trong phạm vi đo được. Chưa đủ nghiệm thu Windows/CI exact-head. Không approve khi các P2 và bằng chứng bắt buộc còn mở.

Reviewer: OpenAI Codex, họ model openai; provider `openai_codex`, execution surface `codex_service` (API agent với shell cục bộ), transport `machine`. Không có bằng chứng runtime độc lập để khai model ID/effort/session ID cụ thể; không nhận danh tính CLI từ tên reviewer trong lease. Đây là lượt 1, không có verdict trước để đối chiếu. Ngưỡng áp: prompt packet, hết P0/P1 và mỗi P2 phải có quyết định rõ; các P2 dưới đây được đề nghị SỬA, chưa có quyết định miễn của chủ kho.

Đã đọc SPEC, CLAUDE.md, AGENTS.md, protocol §8/§13 và diff. Checkout `cay-kho` được giữ nguyên. Mọi clone và script phản chứng riêng của reviewer ở `review-data/`; fixture của suite gốc dùng thư mục tạm do tempfile tạo.  không push, không gọi GitHub. Không soạn payload đường dẫn thoát cây. Không cung cấp patch launcher/hook cho packet sensitive; các hướng sửa runtime được mô tả bằng lời theo protocol §8.

## BẢNG SĂN

Các lệnh dưới đây chạy từ rv1, trừ khi ghi cwd. Mọi lượt Python chạy sản phẩm/test đều đặt `PYTHONDONTWRITEBYTECODE=1`; Ruff dùng `--no-cache`. Log executor chỉ dùng làm đối tượng đối chiếu, không làm bằng chứng của reviewer.

| Hướng | Giả thuyết / lệnh đã chạy | Output thật cắt gọn | Kết luận |
|---|---|---|---|
| 1 | `git -C cay-kho rev-parse HEAD`; `sha256sum SPEC.md`; status | HEAD=db1ed4d…188b1; spec=e4fd84e1…00e0; sạch | KHÔNG PHẢI LỖI |
| 2 | `git diff --numstat de82ef7 db1ed4d`; cộng và so write set | 6 tệp, 408 thêm / 35 xoá; đúng 6 đường dẫn spec, dưới 450 | KHÔNG PHẢI LỖI |
| 3 | Dựng head/base cùng lệnh `git clone --no-hardlinks kho.git …`, checkout SHA tường minh, `core.abbrev=7`, `core.autocrlf=false`; chạy `python .claude/dev/launcher_test.py` trên cả hai | Head rc1 **216/228**, tổng230/skip2/đỏ12; base rc1 **209/221**, tổng223/skip2/đỏ12 | KHÔNG ĐO ĐƯỢC tiêu chí suite xanh; delta tập ca đỏ=0 |
| 4 | Cùng lệnh suite, thêm `CODEX_AUTH_JSON='{"tokens":{"x":"gia"}}'` | Head rc1 **213/225**, tổng230/skip5/đỏ12; base rc1 **206/218**, tổng223/skip5/đỏ12 | KHÔNG ĐO ĐƯỢC suite xanh; delta tập ca đỏ=0 |
| 5 | `python .claude/dev/launcher_test.py --dot-bien` trên hai cây | Head rc0 **259/259**, base rc0 **250/250**; mỗi bên 4 không đo được | Khớp số runner; không suy tổng này là toàn bộ giết thật |
| 6 | `python review-data/probe_mutations.py`: audit 9 mutant mới và đột biến riêng YAML Windows/Linux | 12/12 lượt ca đích của 9 mutant mới = `TARGET_ASSERT`; 0 `UNRELATED_EXCEPTION`; đổi prefix YAML mỗi nền làm N6 đỏ | KHÔNG PHẢI LỖI ở 9 mutant mới |
| 7 | Gỡ `if i_uv == 0` thành `if True`; gỡ riêng WinGet fallback YAML, trên hai clone tạm; chạy toàn suite | Mỗi mutant rc1 **215/227**, tổng230/skip3/đỏ12; đúng tập 12 ca đỏ nền, không thêm assertion đỏ; 7 ca r802 vẫn chạy | LỖI độ phủ: hai chốt mới chưa được suite canh |
| 8 | `python review-data/probe_semantics.py`: cwd có rg hỏng; PATH rỗng đầu so với `.` đầu | PATH=`:<good>`: bare rc1, doctor rc0/ok=true/ok_kha_dung=true, không BI_CHE. PATH=`.:<good>`: doctor rc12/BI_CHE | LỖI F1 |
| 9 | Cũng script trên: probe timeout, budget; mock có kiểu timeout và đồng hồ tất định | Broken→timeout→good: rc12/BI_CHE; timeout→good: rc0, không BI_CHE; broken→hết budget: mặc định rc0/ok=true/ok_kha_dung=false, strict rc13 | Không gán timeout thành BI_CHE là đúng Q2; giới hạn trạng thái cũ còn nguyên, nêu bên dưới |
| 10 | `python review-data/probe_installer.py`: gọi CHÍNH `bash ops/cai_cong_cu.sh rg`, `CONG_CU_NEN=windows`, installer/cygpath giả | Winget thành công: DAT/rc0/chỉ winget; winget thất bại: winget,choco/DAT/rc0; cả hai thất bại: rc1 | KHÔNG PHẢI LỖI về ưu tiên `||`/`&&` hoặc `eval` ở các nhánh này |
| 11 | Cùng script: bản rg cũ hỏng trên PATH, winget tạo bản tốt vào WinGet Links | Bản tốt có thật nhưng installer DO/rc2; cho thư mục mới đứng trước bản hỏng thì DAT/rc0 | LỖI F2 |
| 12 | Cùng script: thiếu cygpath hoặc LOCALAPPDATA | rc3/KHONG_DO_DUOC; stderr lần lượt `cygpath: command not found`, `LOCALAPPDATA: unbound variable` | Không xanh giả; chưa xác nhận native Windows |
| 13 | `python review-data/probe_runner.py`: hook giả MINGW, Linux, thiếu uname, lỗi vô can, Windows skip | N7/N8 bắt đúng apt-get/cargo và chặn installer Windows; thiếu uname không crash (rc0), rơi POSIX; AttributeError vô can ⇒ SAI 0/1; Windows giả ⇒ 2 không đo được, 1 còn đo | KHÔNG PHẢI LỖI về phân loại lỗi hook; F3/F4 về khôi phục và lời khai |
| 14 | `python review-data/probe_resolution.py`: sửa mục PATH rỗng trong bộ nhớ; mô phỏng nhánh Windows của shutil.which đang cài | Sửa mục rỗng ⇒ rc12/BI_CHE; mô phỏng Windows có cwd/rg.EXE ⇒ chỉ trả cwd, bỏ mất bản tốt trên PATH | F1 được xác nhận; Windows là mô phỏng thuật toán, KHÔNG thay phép đo OS thật |
| 15 | `python -m ruff check --no-cache --select F .claude/dev/launcher.py .claude/dev/launcher_test.py` cả hai cây; `python ops/bash_nen.py quet --root .`; doctrine-scan; bash -n | Ruff 0.17.1: mỗi cây 5 F841/rc1, delta0; các cổng còn lại rc0; bash_nen `DAT` | KHÔNG PHẢI LỖI DELTA; không nhận đã kiểm pin Ruff CI |
| 16 | Hai lệnh release-manifest/release-verify của WORKER, manifest ở ngoài clone; đối chiếu git ls-files | `ok=true`, expected_file_count=checked_file_count=188; 188 tệp đều tracked | KHÔNG PHẢI LỖI local; N12 CI chưa đo |
| 17 | Kiểm mirror/ref/lease, không mạng | Mirror 597 heads; master=7c1b9a5…; base thực dùng=de82ef7…; lease f6159dc… và spec hash đều có trong mirror | Sai khác đóng gói đã được loại khỏi DELTA bằng checkout SHA tường minh; số lịch sử/máy chủ KHÔNG ĐO ĐƯỢC |
| 18 | Snapshot nội dung đầu/cuối + status gồm ignored/untracked, diff/index | 3745 tệp ngoài .git, 0 byte-delta quan sát; HEAD/tree giữ nguyên; status rỗng; diff/index rc0 | KHÔNG PHẢI LỖI toàn vẹn checkout |

## BẢNG ĐO

Đối chiếu toàn bộ khẳng định định lượng/hành vi có trong handoff và changelog; không lấy danh sách executor làm trần review.

| Khẳng định | PR/handoff khai | Đo được | Khớp? |
|---|---|---|---|
| Exact head | db1ed4dda529eb30806ecb053d2eef9933e188b1 | Khớp đầu/cuối; tree 1e3c40bd1c00c4a7ad8f07d7a76120f6fbe8b5d8 | Có |
| Base của nhánh | de82ef748e75659ab3dceed225b0f56dcc69e78b | merge-base bằng đúng SHA đó; cây nền checkout đúng SHA | Có |
| Spec SHA-256 | e4fd84e1…00e0 | e4fd84e1f079d0ac4841a145d078473576af3a3e4e2f593e4f3e40c5de7200e0, cả SPEC.md lẫn blob spec trong mirror | Có |
| Lease/ref/giới hạn ngân sách | wp802-r1-g1-claude @ f6159dc4; 3 attempt, ≤4 Codex | Blob lease/ref khớp f6159dc475c261cfbc80725b676b4f9391d6e592; giới hạn 3/4 đúng spec; usage thực tế không có receipt | Chỉ kiểm metadata; usage KHÔNG ĐO ĐƯỢC |
| Hai lượt đăng lease/bia mộ | 39092181024 và 39092090057 success | Không có log/run receipt được cấp, không gọi GitHub | KHÔNG ĐO ĐƯỢC |
| Tập ref máy chủ/cục bộ lúc executor preflight | 596↔596, thiếu0 | Snapshot mirror hiện tại có597 heads; không có snapshot máy chủ ở thời điểm cũ | KHÔNG ĐO ĐƯỢC, không kết luận 596 là sai |
| ai-dang-giu trên 6 đường dẫn | Mỗi đường chỉ wp802-r1-g1-claude giữ | Lease có đúng6 path và mốc hiệu lực; không tái lập được GitHub/ref state ở preflight cũ | KHÔNG ĐO ĐƯỢC lời khai lịch sử |
| Trần và write set | Đúng6 tệp, ≤450 thêm | 6 tệp, 408 thêm,35 xoá; từng tệp +48,+260,+35,+14,+4,+47 | Có |
| Phạm vi BI_CHE | rg/git; bash/python không áp | frozenset đúng2 tên; mutant bỏ git và mở rộng mọi công cụ bị assertion giết | Có |
| Phần tử0 là bản tên trần | Luôn tương đương bản shell gọi | PATH rỗng đầu bị bỏ qua; phản chứng bare rc1, doctor xanh | Không — F1 |
| JSON/text/exit khi BI_CHE thông thường | co=true, đủ2 path+cách chữa; thieu bắt buộc, rc12 | Tình huống bad→good đúng: rc12, ok=false, ok_kha_dung=false; JSON/text đều hiện2 path | Có ở trường hợp đã đo |
| Hành vi cũ nêu trong changelog | rg đầu hỏng, bản sau tốt nhưng doctor rc0/co=true | Phản chứng trên base: rc0/ok=true/co=true, duong_dan=/good/rg, không BI_CHE (`base-reproducer.json`) | Có trên base hiện cấp; mốc lịch sử17-10 không tái lập |
| Ba bảng cài | Windows/Linux CONG_CU và Windows hook khớp YAML | So chuỗi đúng; thiếu PyYAML thật được giả lập ⇒ TinHieuChotCa/KHONG DO DUOC, không skip | Có |
| Cờ winget phi tương tác | 3 cờ accept-source, accept-package, disable-interactivity | Có đúng3 cờ ở cả3 nguồn; khả năng chạy winget thật chưa đo | Có về nội dung |
| Công thức mới in thư mục vừa cài | dirname command-v hoặc WinGet Links | Với bản PATH hỏng, in/chọn lại thư mục cũ, không dùng thư mục mới | Không — F2 |
| Hook Windows | Không gọi installer rg, in đúng1 lệnh | N8 MINGW giả: nhật ký installer rỗng, dòng lệnh khớp YAML; mutant case và chuỗi đều bị assertion giết | Có trên mô phỏng POSIX |
| Hook Linux | rg hỏng vẫn tới cargo dù apt-get trả thành công | Nhật ký APT-GET install, CARGO install ripgrep; trả `co rg` ⇒ N7 đỏ | Có |
| Số ca mới | 7 r802_* | 230−223=7; đúng7 định nghĩa/đăng ký | Có |
| Số mutant mới | 9=6 launcher+3 hook | 263−254=9; audit độc lập12 lượt target, cả12 assertion đúng | Có |
| Suite thường Linux | 228/228, tổng230/skip2; master221/221 | Head216/228, base209/221, cùng12đỏ/skip2 | Không tái lập suite xanh; delta đỏ0 |
| Suite auth giả | Cũng228/228, tổng230/skip2 | Head213/225, base206/218, cùng12đỏ/skip5 | Không tái lập; 3 skip venv/pip có điều kiện |
| Mutation headline | 259/259,4 không đo được | Head259/259,4 không đo được; base250/250,4 không đo được | Có về headline |
| Mọi mutant mới giết đúng ca | Tên ca trần/TinHieuChotCa | Audit riêng xác nhận cả9, 0 lỗi vô can; lỗi vô can bơm vào runner hook bị từ chối | Có |
| Mọi chốt mới đã có răng | M6/changelog mô tả test phủ M1–M5 | Điều kiện i_uv==0 và tail WinGet fallback không làm suite thêm đỏ khi gỡ | Không đủ — xem F1/F2 và bảng mutant |
| Ba mutant hook không đo được trên Windows | Handoff dòng45 | Giả cờ Windows: chỉ2 không đo; mutant chuỗi còn N6 giết1/1 | Không — F4 |
| t106 vẫn giữ chốt cũ | Lùi bản tốt, đúng thứ tự probe | Vẫn đòi duong_dan=/tot/rg và da_thu=[hong,tot]; mutant chỉ thử phần tử đầu vẫn bị giết | Có, không làm yếu chốt cũ |
| 4 neo mutant cũ đổi | doctor_luon_xanh, auth_hong, chi_thu_binary_dau, text_CHUA_DO | Đúng4 hunk; các mutant tương ứng vẫn OK trong lượt chạy thật | Có |
| Ruff F DELTA | 5 F841 nền và head, delta0 | 5/5, delta0, Ruff0.17.1; CI ghim0.15.15 chưa thực thi | Có về delta local |
| bash_nen/doctrine/bash-n | DAT / rc0 / ok | Cả head/base rc0; doctrine quét10 tệp/0 vi phạm | Có |
| Worker release gate | Chờ CI | Local strict ok,188/188; CI PR không có log | Local đạt; CI KHÔNG ĐO ĐƯỢC |
| Windows N5/N9, dispatch CI và installer thực chạy nhánh nào | Handoff còn mở | Không có Windows runner/job logs trong bundle | KHÔNG ĐO ĐƯỢC |
| Tương thích cú pháp PowerShell5.1 | Handoff: chuỗi `||` không chạy trong PS5.1, cmd/PS7/Git Bash chạy được | Không có pwsh/powershell để chạy đối chứng; Bash đã chạy chuỗi thật, các shell Windows chưa đo | KHÔNG ĐO ĐƯỢC native Windows; giữ Q6 nguyên văn |
| WindowsApps thật; macOS; CLI dùng rg nội bộ | Chưa đo | Không có các môi trường/transport đó | Giữ KHÔNG ĐO ĐƯỢC |

### Đối chiếu M1–M8 và N1–N12

| Mục | Đánh giá sau review |
|---|---|
| M1 | Đường bad→good thông thường đạt; còn F1 và thiếu ca canh chỉ số0. Không nhận tuyên bố bao phủ tên trần đầy đủ. |
| M2 | Đạt đối chiếu chuỗi Windows/Linux, không thêm YAML dependency runtime. |
| M3 | Đạt N7 và mutant trả co rg bị giết. |
| M4 | Đạt ca MINGW giả/khối hook; Windows thực chưa đo; thiếu uname rơi POSIX như đã ghi. |
| M5 | Hai nhánh thành công/thất bại đúng hợp đồng Bash thông thường; F2 còn mở. |
| M6 | Đúng7 ca/9 mutant, giết đúng đích; chưa canh2 chốt nêu trong hướng7. |
| M7 | Có fragment đúng write set; phát biểu bản đầuPATH và thư mục cài cần thu hẹp/sửa theo F1/F2. |
| M8 | Có handoff; phần chưa đo được nêu rõ phần lớn, nhưng lời khai số mutant Windows sai (F4). |
| N1 | Qua trên POSIX, tệp script thật; JSON/text/rc12 được đo, hai mutant đích assertion đỏ. |
| N2 | Qua ca ứng viên tốt đơn, mutant luôn BI_CHE assertion đỏ; fixture là mock. |
| N3 | Qua ca git, mutant bỏ git assertion đỏ; fixture là mock. |
| N4 | Qua ca bash, mutant mở rộng phạm vi assertion đỏ; fixture là mock. |
| N5 | KHÔNG ĐO ĐƯỢC native Windows rg.exe0 byte và dòng qua của job exact-head. Có code ca, chưa có bằng chứng thực thi Windows. |
| N6 | Qua; đột biến launcher/hook/YAML mỗi bên làm đỏ; thiếu PyYAML ⇒ lỗi assertion KHONG DO DUOC, không bỏ qua. Tail dirname bị loại khỏi phép so, nên không chứng minh M5. |
| N7 | Qua trên POSIX, nhật ký cargo thật từ stub; mutant co rg assertion đỏ. |
| N8 | Qua MINGW giả trên POSIX; case mutation và chuỗi in bị assertion giết. |
| N9 | KHÔNG ĐO ĐƯỢC Windows installer thật; mô phỏng hợp đồng phát hiện F2. |
| N10 | Chưa đạt N/N trong rig này do12 lỗi nền; không có delta lỗi sản phẩm; 9 mutant mới giết đúng assertion. Dispatch Windows chưa đo; hai mutant bổ sung sống sót trên phần suite đo được. |
| N11 | Đạt các phép đo local và Ruff F delta0; pin/probe Ruff CI không được nhận thay bare lint. |
| N12 | Local tương đương WORKER đạt188/188/ok=true; job PR CI KHÔNG ĐO ĐƯỢC, không kết luận job đỏ hoặc chưa chạy. |

### Ma trận đột biến mới

| Chốt bị gỡ/đổi | Ca đích và bằng chứng |
|---|---|
| Tắt nhánh BI_CHE | r802 rg + git: 2 TinHieuChotCa |
| Gỡ bi_che khỏi thieu_bat_buoc | r802 rg + git: 2 TinHieuChotCa |
| Luôn BI_CHE khi có ứng viên | r802 bản tốt: 1 TinHieuChotCa |
| Bỏ git khỏi tập áp dụng | r802 git: 1 TinHieuChotCa |
| Áp cho mọi công cụ | r802 bash: 1 TinHieuChotCa |
| Đổi winget ở CONG_CU | N6: 1 TinHieuChotCa |
| Hook co_chay rg→co rg | N7: 1 TinHieuChotCa |
| Hook bỏ nhánh Windows | N8: 1 TinHieuChotCa |
| Hook đổi chuỗi RG_CAI_WINDOWS | N6+N8: 2 TinHieuChotCa |
| Đổi prefix YAML Windows hoặc Linux, mỗi bên riêng | N6: mỗi mutant1 TinHieuChotCa |
| Không bao giờ ghi hong_dau | r802 rg/git và t106 đỏ qua assertion |
| Bỏ ràng buộc i_uv==0 nhưng vẫn ghi hong_dau | **Sống**: toàn suite không thêm ca đỏ. Phản chứng reviewer bad1→bad2→good cho thấy mutant nêu nhầm bad2 làm bản tên trần. |
| Bỏ tail WinGet fallback, giữ delimiter dirname | **Sống**: toàn suite không thêm ca đỏ. Mô phỏng installer winget thành công/no-old-rg phân biệt được nhánh đó. |
| Đổi riêng nhãn dòng text BI_CHE thành co, giữ footer | Ca mới vẫn qua vì footer còn chữ BI_CHE. Không coi là mất toàn bộ thông tin text; đây là giới hạn độ chính xác assertion, không thêm finding. |

Các mutant toàn suite được chạy trên `review-data/mut-hong` và `review-data/mut-yaml`; không sửa checkout được review. Ba ca skip ở hai lượt đó gồm2 ca nền phụ thuộc OS và r345 venv/pip; không phải ca r802.

## Findings

### bare-path-empty-entry [P2] F1 — Phần tử0 không luôn là bản shell gọi, doctor vẫn xanh với rg hỏng

**TỆP/DÒNG:** `.claude/dev/launcher.py:4414` (khẳng định mới và quyết định BI_CHE); nguồn ở `:2284` bỏ phần tử PATH rỗng. `ops/handoff/wp802-g1-claude.md:13` và `changelog.d/wp-802.md:1` cũng khẳng định tương đương bản tên trần.

**VẤN ĐỀ:** Với cwd chứa rg hỏng và PATH bắt đầu bằng phần tử rỗng, Bash giải tên trần ra `./rg`. `_cac_duong_dan` bỏ mục đó nên doctor chỉ thấy bản tốt phía sau, không tạo hong_dau/BI_CHE; kết quả rc0, ok=true và ok_kha_dung=true, trong khi bare rg rc1. Đây là lỗ còn lại trong mục tiêu M1; helper bỏ mục rỗng đã tồn tại ở base, không báo là hồi quy mới của helper. Bản vá mới dựa vào bất biến chưa đúng nên chưa chữa trọn hành vi được cam kết.

**ĐÃ THỬ VÁ:** Chỉ chuẩn hoá phần tử rỗng thành cwd trong bộ nhớ, không ghi launcher ⇒ cùng phản chứng ra rc12/BI_CHE, ban_hong=./rg. Executor cần xác định bản tên trần độc lập với danh sách bản dự phòng; kiểm cả empty PATH entry, cwd/PATHEXT trên Windows và WinGet Links ngoài PATH. Không coi mọi ứng viên dự phòng là bản shell chắc chắn gọi được.

**ĐÃ THỬ NGHIỆM:** `probe_semantics.py`, `probe_resolution.py`, `semantics.jsonl`, `resolution.jsonl`. A/B `:<good>` so với `.:<good>` khác đúng biểu diễn cwd. Mô phỏng nhánh Windows của CPython shutil.which còn cho thấy tìm từng thư mục có thể lặp kết quả cwd và bỏ bản tốt; đó chỉ là bằng chứng thuật toán, cần Windows thật để kết luận hành vi OS. Bổ sung ca ba ứng viên bad1→bad2→good: head giữ bad1; mutant gỡ i_uv==0 giữ bad2 mà stock suite không đỏ.

**ĐỘ TIN:** Cao cho Linux và lỗi bất biến; giới hạn Windows ghi rõ. **Quyết định đề nghị:** sửa và thêm ca assertion/đột biến trước approval.

### installer-selects-broken-path [P2] F2 — Công thức winget trả thư mục rg cũ hỏng thay vì bản vừa cài

**TỆP/DÒNG:** `ops/cong_cu.yaml:90`; hợp đồng được tiêu thụ tại `ops/cai_cong_cu.sh:72`. Lời khai ở `ops/handoff/wp802-g1-claude.md:17` và `changelog.d/wp-802.md:7`.

**VẤN ĐỀ:** Fallback WinGet Links chỉ chạy khi `command -v rg` thất bại. Trong chính môi trường packet đi chữa, rg cũ có mặt nhưng không chạy được: command-v vẫn thành công, dirname trả thư mục cũ. Installer nối lại thư mục hỏng lên đầu PATH và probe sau cài vẫn DO/rc2 dù winget đã tạo bản tốt. Vi phạm M5/hợp đồng “dòng cuối là thư mục vừa cài”; test N6 chỉ so prefix nên không canh phần mới này. Mô phỏng hoàn toàn bằng Bash thật và installer stub, không tuyên bố đã đo winget thực trên Windows.

**ĐÃ THỬ VÁ:** A/B fixture đặt thư mục WinGet mới trước bản hỏng ⇒ cùng công thức/installer, kết quả đổi DO/rc2 thành DAT/rc0. Chưa phát patch YAML/hook. Hướng sửa: chọn và probe bản được installer thực sự tạo, in thư mục bản chạy được; phân biệt nguồn winget/choco, không dùng sự có mặt của command-v làm bằng chứng đã chữa. Thêm ca chạy nguyên công thức qua cai_cong_cu.sh và mutant gỡ fallback; không chỉ đối chiếu chuỗi prefix.

**ĐÃ THỬ NGHIỆM:** `probe_installer.py`/`installer.jsonl`: `broken_rg_before_new_winget` rc2, good_exists=true, chỉ gọi winget; đối chứng `new_winget_folder_before_broken` rc0/DAT. Các nhánh winget-success/choco-fallback/both-fail vẫn được chạy; thiếu cygpath/LOCALAPPDATA không xanh giả. `mut-yaml-full.log` cho thấy bỏ fallback không thêm assertion đỏ.

**ĐỘ TIN:** Cao về hợp đồng Bash và lỗi chọn đường dẫn; Windows installer thật KHÔNG ĐO ĐƯỢC. **Quyết định đề nghị:** sửa, thêm ca hành vi và đo lại N9 trên Windows.

### hook-pointer-restore [P3] F3 — Runner không khôi phục HOOK_DANG_DUNG của người gọi

**TỆP/DÒNG:** `.claude/dev/launcher_test.py:10502`.

**VẤN ĐỀ:** finally đặt con trỏ về đường dẫn canonical thay vì giá trị ban đầu. Nếu người gọi đã trỏ vào một hook tạm để kiểm A/B/runner lồng, sau chay_dot_bien() con trỏ mất; các lượt tiếp theo có thể đọc nhầm hook. CLI bình thường khởi đầu canonical nên chưa thấy ảnh hưởng sản phẩm.

**ĐÃ THỬ VÁ:** Sửa trong bộ nhớ: lưu con trỏ trước vòng hook, finally trả lại chính con trỏ ấy. Không commit hoặc sửa file test trong checkout. `probe_runner_fix.py`: result=[0,0], restored_original_pointer=true; bản chưa sửa false.

**ĐÃ THỬ NGHIỆM:** `probe_runner.py`/`runner.jsonl` với hook copy riêng và3 mutant hook; cả3 vẫn đo đúng. Tiêm AttributeError vô can ⇒ hong1, không tính là giết. `runner-fix.json` xác nhận hướng sửa.

**ĐỘ TIN:** Cao. **Nợ đề nghị:** owner executor wp802; sửa con trỏ và thêm ca harness nhỏ. Có thể giữ P3 chỉ khi chủ kho quyết định rõ; chưa có quyết định miễn trong bundle.

### windows-hook-mutation-count [P3] F4 — Handoff đếm nhầm số mutant hook không đo được trên Windows

**TỆP/DÒNG:** `ops/handoff/wp802-g1-claude.md:45`; đối chiếu `.claude/dev/launcher_test.py:10342`.

**VẤN ĐỀ:** Handoff nói cả3 mutant hook không đo được do N7/N8 chỉ POSIX. Mutant đổi RG_CAI_WINDOWS còn có ca N6 không skip Windows; vì vậy chỉ2 mutant hook hoàn toàn không đo được, mutant chuỗi vẫn đo1/1. Tổng tong_dot_bien cộng3 là đúng; nhầm nằm ở lời khai số không đo được.

**ĐÃ THỬ VÁ:** Chưa sửa tài liệu executor; hướng sửa là khai2 không đo được và mutant chuỗi còn N6. Giữ câu native Windows chưa đo, không suy headline Windows đầy đủ từ mô phỏng này.

**ĐÃ THỬ NGHIỆM:** `probe_runner.py` đặt LA_WINDOWS=True chỉ để đo nhánh skip: result=[0,2]; mutant1/2 KHONG DO DUOC, mutant3 OK giet1/1 qua N6. Đây là đo logic skip trên Linux, không phải một lượt Windows thật.

**ĐỘ TIN:** Cao về logic và sai khác văn bản. **Nợ đề nghị:** owner executor wp802; sửa handoff cùng lượt rework, không cần thêm dependency hoặc mở rộng write set.

### Bảng lớp và giới hạn kết luận

| Slug | Biểu hiện | Severity mở | Cách đóng lớp |
|---|---|---|---|
| bare-path-empty-entry | F1; bất biến index0 sai và thiếu ca first-index | P2 | Bản tên trần giải đúng, phản chứng PATH rỗng/cwd và ba ứng viên được canh bằng assertion; Windows đo riêng |
| installer-selects-broken-path | F2; tail cài không được test canh | P2 | Chọn thư mục bản mới chạy được; test nguyên công thức và Windows exact-head N9 |
| hook-pointer-restore | F3 | P3 | Lưu/khôi phục đúng con trỏ, ca harness A/B qua |
| windows-hook-mutation-count | F4 | P3 | Handoff khớp2 skip toàn phần/1 mutant còn đo N6, kèm log Windows thực khi có |

Nguồn của cả4 lớp: lượt1, exact SHA trên đầu verdict. Không có nhánh patch-as-hint runtime; các script phản chứng là bằng chứng reviewer, không phải quyền ghi cho executor.

Những điểm được săn nhưng **không nâng thành hồi quy packet**:

- Ưu tiên `winget || choco && dirname` trong Bash là `(winget || choco) && dirname`; đã đo cả hai nhánh, không có lỗi “winget thành công thì bỏ dirname”.
- t106 đổi rc0 thành rc12 là đúng Q2, vẫn canh lùi sang bản tốt và thứ tự probe; không làm yếu chốt cũ.
- Timeout ở ứng viên0 không tạo BI_CHE là đúng quyết định đã chốt. Tuy nhiên timeout0→good vẫn cho ok_kha_dung=true, còn broken0→hết budget cho mặc định rc0/strict13. Cả hai là giới hạn kế thừa, được ghi rõ để không đọc kết quả như đã chứng minh bản tên trần khả dụng; đề nghị điều phối quyết định phạm vi xử lý tiếp, không tự đổi hợp đồng timeout trong review này.
- Runner cũ vẫn gắn OK cho14 dòng không dùng TinHieuChotCa:4 AssertionError trần và10 ngoại lệ kiểu; cùng tập ở base/head. Vì vậy tổng259/259 là headline đã tái lập, không phải chứng nhận259 giết thật. Chín mutant wp802 đã được audit riêng, không chịu tín dụng giả này. Nợ nền thuộc harness hiện hữu; không cộng thành14 hồi quy của PR.
- `/tmp/.git` là điều kiện hạ tầng làm12 ca credential đỏ trên cảhead/base. Không thay guard, bỏ marker hoặc xin bypass để ép suite xanh. Ba/vài ca venv/pip skip thay đổi giữa lượt; đã kê số thật từng lượt, không quy nguyên nhân cho auth giả.
- Git mirror master khác lời mô tả bootstrap, nhưng objects/base/head đầy đủ và DELTA dùng SHA tường minh. Không dùng master trôi làm nền.

N5/N9, dispatch Windows của N10 và job PR N12 vẫn **KHÔNG ĐO ĐƯỢC**: bundle không có log exact-head tương ứng và prompt cấm mạng GitHub. Không kết luận chúng thất bại hoặc chưa chạy; cần điều phối cấp bằng chứng để đóng nghiệm thu. Ca WindowsApps thật/macOS cũng giữ trạng thái chưa đo như spec.

Checkout cuối: HEAD giữ db1ed4d…188b1, tree giữ1e3c40bd…b5d8;3745 tệp ngoài .git byte-match snapshot đầu; tracked/index/untracked/ignored không delta quan sát. Snapshot không chứng minh toàn lịch sử chưa từng ghi rồi hoàn nguyên; review này chỉ chạy sản phẩm trên các clone/scratch riêng. Sandbox thực tế workspace-write, không coi lời nhắc read-only là cơ chế sandbox cưỡng chế.

## Nhật ký cập nhật dần

Các mốc sau được ghi ngay trong lượt làm việc; bảng/phán quyết phía trên là trạng thái chốt, với 7 tình huống installer sau khi thêm đối chứng sửa PATH.

### Cập nhật phép đo 1

- Diff đo trực tiếp: đúng 6 tệp, 408 dòng thêm / 35 dòng xoá; trong trần 450 dòng.
- Ruff 0.17.1, `check --no-cache --select F`: head=5 F841, base=5 F841, delta=0 (cả hai rc=1). Đây là bare lint; không phải xác nhận pin 0.15.15 của CI.
- `doctrine-scan`: rc=0, quét 10 tệp, 0 chỗ; `bash -n` hook rc=0.
- Mirror hiện có 597 refs/heads; không suy ra lời khai lịch sử 596↔596 là sai. Chưa thể hỏi GitHub theo ràng buộc review offline.

### Cập nhật phép đo 2

- Suite thật head **216/228**, base **209/221**, cùng 12 ca đỏ, cùng 2 ca bỏ qua. Hạ tầng có `/tmp/.git`; guard credential từ chối mọi fixture home dưới `/tmp` (`Codex home is inside a repository`). Không sửa/bỏ guard hoặc di chuyển marker hạ tầng. Không nhận lại các số 228/228 và 221/221 của executor là đã tái lập; delta ca đỏ=0.
- Phản chứng M1 (`review-data/probe_semantics.py`): cwd chứa `rg` hỏng, PATH=`:<good>` ⇒ Bash gọi `./rg`, rc=1, doctor rc=0/ok=true/ok_kha_dung=true/không BI_CHE. Đối chứng PATH=`.:<good>` ⇒ doctor rc=12/BI_CHE. Lỗi nguồn `_cac_duong_dan` bỏ mục rỗng, nên lời khẳng định mới “phần tử 0 = tên trần” không đúng.
- 9 mutant mới của executor đã kiểm riêng: 12 lượt ca đích đều chết qua chính `TinHieuChotCa`, 0 lỗi vô can (`review-data/mutation-audit.jsonl`). Nhưng gỡ điều kiện `i_uv == 0` thành `True` sống qua cả 7 ca mới và t106; gỡ riêng đuôi WinGet fallback khỏi YAML cũng qua ca đối chiếu.
- `bash_nen.py quet --root .`: rc=0, `DAT: không có lời gọi trần mới`.

### Cập nhật phép đo 3

- `--dot-bien`: head 259/259, base 250/250, mỗi bên 4 không đo được. Đây là số runner báo; một số mutant CŨ nhận tín dụng từ OSError/FileNotFoundError/JSONDecodeError, nên không đồng nhất toàn bộ tổng này với “assertion đúng ca”. Chín mutant wp802 được audit riêng đều giết thật (12 lượt ca đích).
- Công thức Windows được chạy qua CHÍNH `bash ops/cai_cong_cu.sh rg`, `CONG_CU_NEN=windows`, installer/cygpath giả, probe thật trên Linux: winget thành công→DAT/rc0/chỉ winget; winget thất bại→choco→DAT/rc0; cả hai thất bại→rc1. `||`/`&&` đúng thứ tự vì cùng ưu tiên và kết hợp trái trong Bash.
- Có `rg` hỏng trên PATH rồi winget giả cài bản tốt vào WinGet Links: installer vẫn rc2/DO dù bản tốt tồn tại; `command -v rg` chọn thư mục bản hỏng và không thử WinGet fallback. Thiếu cygpath hoặc LOCALAPPDATA: rc3/KHONG_DO_DUOC, không xanh giả. Đây là phép đo hợp đồng Bash, KHÔNG thay Windows N9.
- Bản đầu fixture installer thiếu basename nên rc127; đã sửa fixture, chạy lại cả 6 tình huống. Chỉ kết quả sau sửa trong `review-data/installer.jsonl` được dùng kết luận.

### Cập nhật phép đo 4

- Có auth giả: head **213/225**, base **206/218**, cùng 12 đỏ / 5 bỏ qua (thêm 3 ca báo venv/pip không dùng được). Không quy 3 skip này cho credential: hai suite đã pop biến ở đầu; điều kiện venv/pip không ổn định giữa các lượt. Không có hồi quy đỏ ở 7 ca wp802.
- Runner hook: thử AttributeError vô can ⇒ `SAI giet 0/1`, hong=1, không tín dụng giả. Giả cờ Windows ⇒ 2 mutant hook không đo được; mutant lệch chuỗi còn đo được qua N6 (`giet 1/1`). Handoff nói cả ba không đo được là không chính xác.
- Gọi runner với HOOK_DANG_DUNG trỏ bản hook riêng: sau chạy không khôi phục con trỏ đầu vào (`restored_original_pointer=false`); nó đặt về đường dẫn canonical. Luồng CLI bình thường vẫn đúng vì con trỏ khởi đầu là canonical; ghi nợ runner, không nâng thành P1.
- Đã chạy lane WORKER tương đương ở local: release-verify strict `ok=true`, expected_file_count=checked_file_count=188; manifest tạm có 188 tệp đều được Git theo dõi. N12 job PR vẫn KHÔNG ĐO ĐƯỢC vì không có log CI và cấm mạng GitHub.
- Mirror có master ở 7c1b9a5e13c95fb9215d9956b4ebfe613bab7ca3, khác lời khai “master @ base” trong prompt. Phép DELTA đã dùng SHA base tường minh de82ef748e75659ab3dceed225b0f56dcc69e78b trên CẢ HAI clone, không dùng ref master trôi.

### Cập nhật phép đo 5

- Hai mutant được chạy CẢ suite trên clone độc lập từ cùng mirror: `if i_uv == 0`→`if True` và gỡ riêng `|| cygpath ...` trong YAML đều **215/227**, tổng230/bỏqua3/đỏ12. Tập 12 ca đỏ trùng hoàn toàn head/base; không thêm assertion đỏ. Bỏ qua thêm `r345_*` do venv/pip không khả dụng, không phải ca rg.
- Mutant chỉ số có tác dụng thật: `[bad1,bad2,good]` ở head nêu ban_hong=bad1, mutant nêu ban_hong=bad2. Test reviewer phân biệt được, stock suite không.
- Thử hướng sửa runner trong bộ nhớ: lưu con trỏ hook đầu vào và khôi phục chính nó ⇒ `(hong,khong_do)=(0,0)`, `restored_original_pointer=true`; bản chưa sửa false. Chỉ thử trong scratch, không phát patch runtime/hook.
- `uname` vắng dưới `set -euo pipefail` không làm khối rg crash (rc0); nó rơi vào nhánh POSIX, nhật ký apt-get/cargo. Không coi đây là xác nhận an toàn Windows khi uname vắng.
- Có 14 dòng mutant CŨ được runner gắn OK bằng tín hiệu khác TinHieuChotCa (4 AssertionError trần, 10 lỗi kiểu OSError/FileNotFoundError/JSONDecodeError/TypeError/AttributeError), cùng tập ở head/base. Đây là giới hạn/nợ nền của tổng mutant, không phải 14 hồi quy wp802.
