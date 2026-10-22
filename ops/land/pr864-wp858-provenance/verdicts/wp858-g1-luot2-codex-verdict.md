verdict: changes_requested
reviewed_head: 97544b576392540ce316b2d61e5cc0de3a4a88eb
reviewed_sha: 97544b576392540ce316b2d61e5cc0de3a4a88eb
reviewed_tree: 75a0bdced48105b4cf82d860140bd8c372acbdc5
review_class: sensitive
provider: openai_codex
model: gpt-6.1-sol
model_family: openai
reasoning_effort: xhigh
execution_surface: codex_cli
transport: machine
review_run: 0ecfade95c0d4d08a2dee0029a00d62f

## Kết luận

F858-01 đã đóng. Độ phủ chuyển đổi Windows của F858-02 đã sửa thật; các nhánh lọc `-f/-x/.exe` cũ đã bị xoá nên không còn mutant tương ứng để đòi giết. Tuy nhiên, **lập luận rằng xoá bộ lọc là tương đương bị phản chứng**, trình bày riêng bên dưới. F858-03 đã qua đúng phép tái hiện cũ nhưng lớp lỗi hợp đồng stdout **chưa đóng**: thư mục thật trùng dòng canh khiến `--bat-buoc` lại làm `rg=DO`.

Còn hai finding P2 mới: chốt lỗi `cygpath -u` chưa có test hành vi giết được đột biến của nó, và diff vượt trần được cấp **461 > 450 dòng thêm**. Không phát hiện P0/P1 trong các phép đã đo. Chưa có quyết định chủ kho cho các finding mở trong nguồn được cấp; không đủ điều kiện approve lớp sensitive.

HEAD, merge-base `637f78029f5a5fe56d35199dd0f75c50274f2c0f` và băm spec đều khớp. Spec lấy nguyên byte từ `origin/ops/wp858-spec:ops/specs/wp858.md`, SHA-256 `5a61e959281f852592b2a5420b4618718d2364db8fa6320934d2651bbb7d4c54`. Lease được đọc offline từ `origin/ops/wp858-r1-g1-lease`; không gọi GitHub. Danh tính trên lấy từ [header CLI của run](evidence/model-header.txt) và [metadata run](evidence/run-identity.json), với giới hạn header chỉ chứng minh cấu hình CLI công bố.

## Đối chiếu lượt trước

Nguồn: `VERDICT-luot1.md`, reviewed SHA `bfbd2732a0e5359cbeb2a4d5336fc3dc7d2a7121`. Các script lượt 1 không có ở bundle này; đã dựng lại bằng [edges.py](edges.py). Đối chứng `luot1-*` dùng shell nguyên văn từ `git show bfbd273:ops/cai_cong_cu.sh`, cùng YAML/checker/fixture với head; đây là phép cô lập thay đổi shell, không phải lời khai đã chạy toàn bộ suite ở `bfbd273`.

| Finding lượt 1 | ĐÓNG / CHƯA ĐÓNG | Phép đo trên head mới và đối chứng |
|---|---|---|
| F858-01 — lỗi ghi PATH bị nuốt trong command substitution | **ĐÓNG — ĐÃ VÁ THẬT** | `PYTHONDONTWRITEBYTECODE=1 python out/edges.py`: `$GITHUB_PATH` là thư mục trên Linux/Windows: shell lượt 1 rc=0/DAT, head **rc=1**; `cygpath -w` thoát 37: lượt 1 **rc=0/DAT**, head **rc=1**, không ghi PATH. `python out/followup.py`: đối chứng eval trực tiếp lượt 1 rc=37, head rc=1. Các ca `r858_cai_*` cũng qua lỗi ghi ở cả ba nền mô phỏng. [Linux](evidence/head-linux-bad-gp.json), [Windows](evidence/head-windows-bad-gp.json), [-w](evidence/head-fail-w.json), [đối chứng cũ](evidence/luot1-fail-w.json). |
| F858-02 — fixture Windows không phân biệt chuyển đổi và các bộ lọc cũ | **ĐÓNG trong phạm vi finding độ phủ cũ — ĐÃ VÁ THẬT** | `python out/edges.py`: ánh xạ `V:` nguyên vẹn **rc=0/DAT**, bỏ `cygpath -u` **rc=1**, không ghi PATH. `python out/mutations.py`: `no-u` bị ca Windows và shape giết bằng **TinHieuChotCa**; làm hỏng ánh xạ `V:` bị ca Windows giết bằng **TinHieuChotCa**. Các điều kiện `-f/-x/.exe` đã bị xoá khỏi hàm, không gọi mutant của code đã xoá là “sống”. Không nhận giải thích tương đương là đúng và không suy fixture POSIX đã đo `.exe`/PATHEXT native; xem mục phân tích riêng. [Mutant](evidence/independent-mutations.json), [đối chứng](evidence/no-u-mapped-control.json). |
| F858-03 — stdout installer bị nhận làm thư mục chọn | **CHƯA ĐÓNG lớp lỗi — VÁ SINH LỖI MỚI** | `python out/edges.py`: đúng ba biến thể cũ stdout im lặng/chữ/thư mục: lượt 1 **0/0/2**, head **0/0/0**, head đều `rg=DAT,bash=DAT`. Nhưng head nguyên vẹn với thư mục thật trùng sentinel: **rc=2, rg=DO,bash=DAT**. Đối chứng chỉ bỏ thư mục sentinel, giữ tệp `rg` fixture ở cwd: **rc=0, cả hai DAT**. [Tái hiện cũ trên head](evidence/head-n4-directory.json), [collision](evidence/head-sentinel-collision.json), [control](evidence/head-sentinel-control.json). |

Hai trong ba lớp lượt trước đóng trong phạm vi finding gốc; lớp stdout còn mở. Những giới hạn Windows và phản chứng về lập luận không bị biến thành số đo đã qua.

## Finding mới và biểu hiện tái mở

| ID | Mức | Tệp:dòng ở head / nguồn ràng buộc | Lệnh → kết quả thật | Đề xuất |
|---|---|---|---|---|
| **F858-03 (tái mở)** | **P2** | `ops/cai_cong_cu.sh:47`, tương tác reader `:124`, `:126` | `python out/edges.py` → `head-sentinel-collision`: **rc=2**, `{'rg':'DO','bash':'DAT'}` trên **shell head nguyên vẹn**. `python out/followup.py` → `head-sentinel-control`: **rc=0**, cả hai DAT. | Dòng canh phải trở thành kết quả không thể được reader nhận làm thư mục. Khoá bằng ca N4 có thư mục trùng sentinel, tệp `rg` fixture ở cwd và cả hai thứ tự công cụ; xem hướng vá, phạm vi và rủi ro bên dưới. |
| **F858-04** | **P2** | `.claude/dev/launcher_test.py:8582` và bảng mutant `:10963`; chốt sản phẩm `ops/cai_cong_cu.sh:52` | `python out/mutations.py`: thay riêng `return 1` trong handler lỗi `-u` bằng lệnh rỗng, giữ nguyên tiền tố shape → **7/7 ca r858 liên quan PASS**, không TinHieuChotCa. Toàn suite bản mutant giữ đúng headline và tập lỗi/bỏ qua của control: **221/234, 13 đỏ môi trường, 10 bỏ qua**, không lỗi mới. `python out/edges.py`: stub `-u` in đúng đường rồi thoát 37 → head **rc=1/PATH rỗng**, mutant **rc=0/DAT, ghi PATH**. Đây là mutant sống **không tương đương**, không phải lỗi runtime ở head nguyên vẹn. | Bổ sung ca âm `-u` qua installer thật, gồm lỗi có stdout hợp lệ; đăng ký mutant chỉ bỏ hành động trả lỗi để ca hành vi giết nó. Không dựa riêng vào kiểm chuỗi shape. |
| **F858-05** | **P2** | Diff PR; `.claude/dev/launcher_test.py:2343` thuộc phần thêm mới. Ràng buộc: spec `ops/specs/wp858.md:38` tại ref đóng băng, lease M-4 | `git -C kho diff --numstat 637f78029f5a5fe56d35199dd0f75c50274f2c0f HEAD` → **6 tệp, 461 dòng thêm, 30 dòng xoá**. Spec/lease giới hạn **450 dòng thêm**; lease được cấp có `nang_tran: []`, prompt không bổ sung ngoại lệ kích thước. [Số đo](evidence/scope.json), [lease](evidence/wp858-lease.yaml), [spec](evidence/wp858-spec.md). | Thu gọn diff ít nhất 11 dòng thêm mà giữ các chốt cần thiết, hoặc lấy quyết định nâng trần đúng thẩm quyền và đưa bằng chứng vào bundle. Không tự coi sửa finding là ngoại lệ tự động của trần. |

**F858-03: cơ chế và hướng vá.** Trên POSIX, tên `:giu-nguyen-PATH:` hợp lệ cho thư mục. Reader chỉ kiểm `[ -d "$DICH" ]`, nên vẫn chấp nhận nó khi thư mục tồn tại trong cwd của installer. Dấu `:` trong giá trị được đưa vào PATH lại tạo các phần tử PATH rỗng/khác nghĩa, làm probe có thể thấy tệp fixture ở cwd. Đây là lỗi chức năng N4 đã đo bằng stub vô hại; không khẳng định trình cài thật thường tạo thư mục ấy, hay có khai thác credential.

Vị trí vá cần xử lý hợp đồng giữa dòng `47` và reader. Một hướng **giữ phạm vi trong hàm** đã thử bằng `PYTHONDONTWRITEBYTECODE=1 python out/cr_control.py` trên bản sao là kết thúc bằng dòng được phép bỏ CR sẵn có ở reader chuẩn hoá thành chuỗi rỗng; [đối chứng thay dòng cuối](evidence/cr-sentinel-collision-control.json) **rc=0, rg/bash DAT** trên fixture collision. Đây chỉ là thí nghiệm, chưa phải bản vá đã nghiệm thu; executor cần tự dẫn xuất và đo trên các nền, cập nhật shape phù hợp. Hướng so sánh marker tường minh tại reader cần giải quyết giới hạn Q1 “chỉ thêm hàm” trước khi sửa reader. Rủi ro cần khoá: stdout trình cài, command substitution bỏ newline cuối, CRLF và việc source trong `--bat-buoc`. Không chỉ thay bằng một tên thư mục POSIX khác.

**F858-04: vị trí, ca khoá và rủi ro.** Mở rộng fixture/test `r858_cai_windows_chon_ban_chay_duoc` tại nhóm lỗi ghi/chuyển đổi, dùng stub `cygpath -u` thất bại nhưng đã in ra đường hợp lệ. Khẳng định installer rc khác 0 và không ghi GITHUB_PATH; giữ một control `-u` thành công. Mutant giữ `d="$(cygpath -u "$d")" || { ... }`, chỉ bỏ `return 1`, phải chết bằng TinHieuChotCa của ca hành vi. Thêm biến thể stdout rỗng và vắng `cygpath` nếu muốn khoá đầy đủ nhánh lỗi. Tránh làm hỏng bootstrap Python/bash trong fixture rồi nhận lỗi giàn giáo là kill. [Delta toàn suite](evidence/mutant-u-delta.json) xác nhận survivor không tạo thêm ca đỏ so với control trong cùng sandbox.

**F858-05: phép khoá và rủi ro.** Đo lại tổng cột thêm của `git diff --numstat <merge-base> HEAD` sau mọi lần sửa; không trừ manifest, changelog hay comment khi hợp đồng không cấp phép trừ. Phân rã hiện tại: launcher test 358; manifest 11; changelog 25; shell 36; YAML 19; selftest 12. Thu gọn không được đổi thành bỏ ca âm, bỏ mutant, hoặc nới kiểm assertion. Nếu có quyết định nâng trần ngoài bundle, cần readback/bổ sung bằng chứng; review offline này không kết luận rằng quyết định ấy không tồn tại ở nơi chưa được cấp.

| Slug lớp nguyên nhân | Finding / lịch sử | Trạng thái cuối lượt | Cách kiểm đóng lớp |
|---|---|---|---|
| `loi-ghi-path-bi-nuot-trong-command-substitution` | F858-01, lượt 1 `bfbd273` | Đóng | Lỗi ghi và `-w` qua installer thật khác 0; chiều dương ghi đúng PATH. |
| `fixture-windows-khong-phan-biet-chuyen-doi-va-duoi-exe` | F858-02, lượt 1 `bfbd273` | Đóng phạm vi độ phủ code cũ | Mutant bỏ đổi `-u` bị ca Windows giết; không còn nhánh lọc `.exe` riêng trong hàm. Chưa có native Windows. |
| `stdout-installer-bi-nhan-lam-ket-qua-chon` | F858-03, lượt 1 và lượt 2 | **Mở, P2** | N4 qua cả stdout là thư mục và thư mục thật trùng marker; PATH không bị prefix lại trong nhánh tên trần DAT. |
| `cygpath-u-error-guard-khong-co-ca-am` | F858-04, mới lượt 2 | **Mở, P2** | Mutant chỉ bỏ trả lỗi `-u` bị ca âm installer giết bằng TinHieuChotCa. |
| `vuot-tran-diff-sensitive-chua-co-ngoai-le` | F858-05, mới lượt 2 | **Mở, P2** | Tổng thêm ≤450 hoặc có quyết định nâng trần hợp lệ, được readback. |

## Đột biến bản vá mới

Các bản shell/fixture đột biến nằm dưới `out/mutants/` hoặc `out/mutant-u-full/`; không sửa `kho/`. [mutations.py](mutations.py) ghi loại tín hiệu từng ca trong [independent-mutations.json](evidence/independent-mutations.json). Control 7 ca đều PASS trước khi tính kill; không dùng lỗi môi trường của `r858_goc_*` làm kill cho các mutant shell.

| Đột biến độc lập | Kết quả thật |
|---|---|
| Bỏ dòng canh | N4 và shape chết bằng **TinHieuChotCa**; tái hiện installer stdout là thư mục **rc=2/rg DO**. |
| Bỏ `return 1` của lỗi `cygpath -u`, giữ shape | **SỐNG** qua 7 ca liên quan; toàn suite delta lỗi = 0. Ca âm riêng phân biệt head rc=1 với mutant rc=0/DAT. |
| Bỏ `return 1` của lỗi `cygpath -w`, giữ shape | Ca Windows chết bằng **TinHieuChotCa**; phép lỗi riêng mutant rc=0/DAT, head rc=1. |
| Bỏ `return 1` của lỗi `printf >> GITHUB_PATH`, giữ shape | Cả ba ca nền mô phỏng chết bằng **TinHieuChotCa**; phép Linux đích là thư mục mutant rc=0/DAT, head rc=1. |
| Bỏ toàn bộ chuyển đổi `cygpath -u` | Ca Windows và shape chết bằng **TinHieuChotCa**; control ánh xạ tốt rc=0, mutant rc=1. |
| Làm hỏng ánh xạ fixture `V:` để nó trả lại đường Windows | Ca Windows chết bằng **TinHieuChotCa**; shape vẫn PASS. |
| Bỏ kiểm tên trần | Các ca Linux/macOS/Windows và shape chết bằng **TinHieuChotCa**; **N4 PASS**. Phép riêng khi tên trần đã DAT vẫn rc=0 nhưng ghi GITHUB_PATH, xác nhận đúng tác hại được nêu ở mục 5 prompt. |
| Bộ chọn gốc tạm bỏ kiểm tổ tiên | Native chưa có control xanh vì `/var/tmp` chỉ đọc. Unit test riêng của **bộ chọn**: control PASS, mutant chết bằng **TinHieuChotCa**. Xem giới hạn chính xác ở mục L2. |

Runner sẵn có `launcher_test.py --dot-bien` in **291/291 đạt, 4 không đo được**, rc=0. Số này không chứng minh lỗi `-u` đã được khoá: mutant tương ứng chưa có trong bảng. Cũng không dùng headline đó làm bằng chứng native cho mutant gốc tạm: trong sandbox này ca gốc đã đỏ vì EROFS; runner harness vẫn in “OK” cho mutant ấy. Những cơ chế tín dụng generic exception cũ của runner nằm ngoài packet theo Q8; báo giới hạn, không vá.

## Kiểm lập luận tương đương và quyết định đổi đích N4

**Bác lập luận tương đương tổng quát.** [followup.py](followup.py) giữ nguyên checker và YAML, dựng `git` fixture ở đầu PATH gọi một chương trình phụ. Ứng viên chỉ chứa chương trình phụ, **không có `git`**. Trước và sau thêm ứng viên, `command -v git` in **cùng một tệp**; checker đổi **rc=2/DO → rc=0/DAT** vì tiến trình probe thừa hưởng PATH. Head chọn và ghi ứng viên; bản đối chứng khôi phục bộ lọc không chọn được và rc=1. [Kết quả phân giải và checker](evidence/equivalence.json), [head](evidence/head-dependent-git.json), [bộ lọc đối chứng](evidence/filter-dependent-git.json).

Do đó “phép tra tên không đổi” không suy ra “checker không đổi”. Không cần sửa manifest thành nhiều probe để có phản chứng. Bình luận ở `ops/cai_cong_cu.sh:34` nên được diễn đạt trong phạm vi thực sự đúng; không dùng nó để khẳng định thư mục được in luôn chứa binary `<ten>`. Riêng phản chứng này **chưa chứng minh hậu điều checker của head sai**: thêm đường chứa dependency làm công cụ chạy được, và lần kiểm cuối cũng DAT. Vì vậy không nâng nó thành finding runtime độc lập hay tái mở nhánh `-f/.exe` đã xoá. Việc đóng F858-02 ở trên là đóng lỗ coverage code cũ, không là chấp nhận định lý tương đương hoặc nghiệm thu native Windows.

**Chấp nhận quyết định bỏ N4 khỏi đích của mutant bỏ kiểm tên trần.** Số đo độc lập: mutant đó **N4 PASS**, các ca chọn Linux/macOS/Windows và shape chết. Phép `no-bare-already-dat` **rc=0/DAT nhưng GITHUB_PATH có thư mục ứng viên**, trong khi control tên trần DAT không ghi. Mutant bỏ marker vẫn làm N4 chết đúng lỗi stdout. Đây là hai chốt có tác hại và ca đích khác nhau; không bắt N4 phải giết một thay đổi mà nó không còn phân biệt.

## L2, gốc tạm và các đường mới

**Điều kiện sandbox đã đo trước khi kết luận.** [mountinfo](evidence/mountinfo.txt) có `/tmp/.git ro … tmpfs` và `.git` tại workspace cũng là mount chỉ đọc. Bộ chọn head bỏ root trong `out/tmp` và chọn **`/var/tmp`**; tạo fixture ở đó thất bại **EROFS**. T86 nền đỏ khi kho credential từ chối tổ tiên `.git`; head đỏ tại tạo thư mục tạm. Một cặp suite nền/head với và không auth giả trong cùng điều kiện cho:

| Cây / môi trường | passed | skipped | failed | Tổng | rc |
|---|---:|---:|---:|---:|---:|
| Nền, không auth giả | 214 | 10 | 12 | 236 | 1 |
| Nền, auth giả | 214 | 10 | 12 | 236 | 1 |
| Head, không auth giả | 221 | 10 | 13 | 244 | 1 |
| Head, auth giả | 221 | 10 | 13 | 244 | 1 |

Ca đỏ mới về tên là `r858_goc_tam_tranh_to_tien_co_git`, **cùng EROFS**, không phải bằng chứng hồi quy runtime. Không khai delta ca đỏ bằng 0: delta thô là +1 ca môi trường mới. Không vá 11 ca `r484_*` cùng bị chặn. Hai tiến trình `--lap-ca t86... --lan 10` đồng thời ở từng cây đều **0/10 mỗi tiến trình**, với cùng nguyên nhân tương ứng; không chứng minh race và không xác nhận lời khai N5 10/10 trong môi trường sạch.

**Không thấy t86 bị đổi thành mock/skip.** Diff chỉ đổi nơi `mkdtemp`; ca vẫn gọi triển khai `chuan_bi_xac_thuc(that_su=True)`, kiểm byte JSON fixture trên đĩa, mode 600 trên POSIX, idempotence và từ chối dữ liệu rác. Dữ liệu luôn là credential fixture giả. Tuy nhiên, **không đo được thành công ghi credential end-to-end khi mọi gốc sạch** trong sandbox được cấp này. Không nới `_KhoCodex`, không đọc credential người dùng, không dùng unit test dưới đây thay cho phép ấy.

**Bộ chọn không bảo đảm mọi điều kiện mà kho credential đòi.** [l2_storage.py](l2_storage.py) chỉ mở thư mục, không đọc/ghi auth: nó chọn `/var/run` nhưng `_KhoCodex(create=False)` từ chối **ENOTDIR** vì đây là symlink; chọn `/var/tmp` mode 1777 nhưng nếu truyền trực tiếp làm Codex home thì kho từ chối quyền rộng. Trường hợp sticky bit này **không phải phản chứng rằng t86 sẽ hỏng vì sticky bit**: t86 tạo home con bằng `mkdtemp`, rồi `.codex` riêng; kho kiểm quyền thư mục cuối, không đòi root tạm 1777 thành riêng tư. `/dev/shm` được bộ chọn và phép mở kho đọc chấp nhận nhưng điều đó không chứng minh có quyền ghi. [Số đo](evidence/l2-readonly-storage.json).

Điểm giới hạn thực tế là predicate chỉ kiểm `is_dir` và `.git`, không kiểm quyền ghi, đường symlink hay thử root kế tiếp khi tạo fixture thất bại. Từ chối của storage vẫn làm test đỏ; chưa có bằng chứng fail-open hay che lỗi credential. Với môi trường này, không đủ bằng chứng đóng N5.

**Unit test có khai ranh giới.** `python out/followup.py` chạy riêng `r858_goc_*` dưới `out/tmp`, với proxy `lexists` chỉ che đúng **hai marker `.git` do sandbox gắn** đã đo ở trên. Các `.git` fixture thật vẫn được kiểm; không chạy `_KhoCodex` trong phép này. Control **PASS**, mutant bỏ kiểm tổ tiên **TinHieuChotCa: to tien co .git van duoc chon lam goc tam**. Đây là bằng chứng thuật toán bộ chọn có chốt, không là chứng nhận credential storage hoặc môi trường không `.git`. [selector-unit.json](evidence/selector-unit.json).

**GITHUB_PATH có khoảng trắng.** `python out/edges.py` chạy git/shellcheck/bash × Linux/macOS/Windows mô phỏng với **tên tệp GITHUB_PATH chứa khoảng trắng**: 9/9 **rc=0/DAT**, ghi đúng một dòng ứng viên, Windows có tiền tố `W:` từ stub `-w`. `python out/followup.py`: Python ×3 nền **rc=0/DAT, không ghi thư mục hỏng**, đúng phụ lục. Không nhầm khoảng trắng trong biến với chia từ của shell. [Log tổng](evidence/edges-run.log), [Python](evidence/followup.log).

**Windows vắng cygpath.** Ca git chưa DAT: **rc=1**, không ghi GITHUB_PATH; tên trần đã DAT: **rc=0/DAT**, không ghi GITHUB_PATH vì không cần chọn ứng viên. Ca Python vẫn rc=0/DAT theo giới hạn checker; có thông báo `cygpath: command not found` từ glob trong công thức nhưng không suy ra Python đã được probe theo PATH. [Chưa DAT](evidence/no-cyg-bad.json), [đã DAT](evidence/no-cyg-good.json), [Python](evidence/python-no-cyg.json). Đây đều là mô phỏng trên Linux.

## Bảng lệnh → kết quả thật

Từ workspace, các driver đặt `PYTHONDONTWRITEBYTECODE=1`, `PIP_NO_INDEX=1`, `TMPDIR=<workspace>/out/tmp`. Git signing và hooks được tắt **trong env tiến trình test**, không sửa cấu hình máy. Bản sao nền/head được dựng cùng một lệnh, cùng cách clone/config (`core.abbrev=7`, cùng URL origin), không truy cập URL đó. [audit.py](audit.py) lưu argv, cwd, rc, thời lượng và stdout/stderr cho từng lệnh con. Runtime đã đo: Python **3.13.16**, PyYAML **6.0.3**, Linux x86_64; Ruff **0.17.1** ([runtime](evidence/runtime.log), [Ruff version](evidence/ruff-version.log)).

| Lệnh / cwd | Kết quả thật |
|---|---|
| `git -C kho rev-parse HEAD HEAD^{tree}`; `git -C kho merge-base HEAD origin/master`; băm `git show origin/ops/wp858-spec:ops/specs/wp858.md` | HEAD/tree như header; nền `637f780…`; SHA-256 spec khớp. [Preflight](evidence/preflight.log). |
| `git -C kho diff --check origin/master HEAD` | **rc=0**, không output. [Log](evidence/diff-check.log). |
| `git -C kho diff --numstat 637f78029f5a5fe56d35199dd0f75c50274f2c0f HEAD` | **rc=0**, **461 thêm/30 xoá/6 tệp**, vượt trần 450. [Log](evidence/numstat.log). |
| `PYTHONDONTWRITEBYTECODE=1 python out/audit.py targeted` | 11 ca chọn công cụ/N4/shape/L3/rg **1/1 qua, 0 bỏ qua**, rc=0 từng ca; `r858_goc_*` và t86 native rc=1 vì môi trường như đã khai. [Ca Windows](evidence/r858_cai_windows_chon_ban_chay_duoc.log), [N4](evidence/r858_bat_buoc_bash_khong_dua_rg_hong_len_dau.log), [gốc tạm](evidence/r858_goc_tam_tranh_to_tien_co_git.log). |
| `PYTHONDONTWRITEBYTECODE=1 python out/edges.py` | Driver cuối **rc=0**; đủ các phép so lượt 1/head, ba chốt lỗi, marker collision, PATH có khoảng trắng và cygpath vắng. Các rc con có cả 0/1/2 theo bảng, không dùng rc driver làm pass. [JSON từng phép](evidence/edges-summary.json), [log](evidence/edges-run.log). |
| `PYTHONDONTWRITEBYTECODE=1 python out/followup.py` | Driver cuối **rc=0**; control collision xanh, eval trực tiếp, Python theo phụ lục, phản chứng tương đương và unit bộ chọn. T86 đôi ×10 vẫn đỏ môi trường. [Log](evidence/followup.log). |
| `PYTHONDONTWRITEBYTECODE=1 python out/mutations.py` | Driver **rc=0**; control 7 PASS; **1 survivor không tương đương** (`swallow-u`); các kill khác là TinHieuChotCa, như bảng. [Log](evidence/independent-mutations.log). |
| `python .claude/dev/launcher_test.py --nhat-ky <out/evidence/...>` trong cả `out/base`/`out/head`, có/không auth giả; một driver `python out/audit.py suites` | Cả bốn **rc=1**. Nền **214/226 đã chạy**; head **221/234 đã chạy**; mỗi lượt bỏ qua 10. [Nền sạch](evidence/base-suite-clean.log), [nền giả](evidence/base-suite-fake.log), [head sạch](evidence/head-suite-clean.log), [head giả](evidence/head-suite-fake.log). |
| Cùng lệnh launcher suite trong `out/mutant-u-full` | **rc=1**, **221/234**, đúng tập 13 lỗi và 10 bỏ qua của head control; mutant không bị suite phân biệt. [Log](evidence/mutant-u-full-suite.log), [delta](evidence/mutant-u-delta.json). |
| `python .claude/dev/launcher_test.py --dot-bien` tại `out/head` (`python out/audit.py mutations`) | **rc=0**, **291/291 đạt, 4 không đo được**; không tính headline là bằng chứng hợp lệ cho mọi kill, nhất là gốc tạm. [Log](evidence/all-mutations.log). |
| `python scripts/tl.py --selftest` tại `out/head` | **rc=0, 1731/1731**. [Log](evidence/selftest.log). |
| Hai `python scripts/tl.py --selftest` đồng thời tại `out/head` | Cả hai **rc=0, 1731/1731**, đều `[OK] edit_skill_assert_count_gate_dry`. [Lượt 1](evidence/parallel-selftest-1.log), [lượt 2](evidence/parallel-selftest-2.log). |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` tại `out/head` | **rc=0, ok=true, expected=checked=190, failed=[]**. [Log](evidence/release-verify.log). |
| `CONG_CU_TEST_BAN_KINH=manh python ops/cong_cu_test.py` tại `out/head` | **rc=0, 61/61, bỏ qua 0**, cổng cây thật ĐẠT, lỗi đột biến 0. **470 mutant giao mảnh, không chạy hết bán kính trong lệnh này**. [Log](evidence/cong-cu-manh.log). |
| `python scripts/tl.py golden-test --json`; `python scripts/tl.py doc-claims-check --strict --json` tại `out/head` | Đều **rc=0, ok=true**. [Golden](evidence/golden.log), [doc-claims](evidence/doc-claims.log). |
| `python .claude/dev/packet_loop.py doctrine-scan --root .` tại `out/head` | **rc=0**, sạch, quét 10 tệp/0 chỗ chép doctrine. [Log](evidence/doctrine.log). |
| `bash -n ops/cai_cong_cu.sh`; `actionlint` tại `out/head` | Đều **rc=0**, stdout/stderr rỗng. [Bash](evidence/bash-syntax.log), [actionlint](evidence/actionlint.log). |
| `python -m ruff check --no-cache --select F scripts/tl.py` tại `out/base`/`out/head` | Cả hai **rc=1, 12 F821**, delta=0. Đây là bare lint, không phải kiểm contract pin/probe riêng. [Nền](evidence/ruff-base.log), [head](evidence/ruff-head.log). |
| `PYTHONDONTWRITEBYTECODE=1 python out/l2_storage.py` | **rc=0**, kết quả mở thư mục đọc như mục L2; không đọc/ghi auth. [Log](evidence/l2-storage.log). |
| Snapshot hash/trạng thái `kho/` đầu/cuối | **4.839 hash tệp tracked, HEAD/tree/status/diff trùng nhau**; trạng thái tracked/untracked/ignored đều sạch. [Kết quả](evidence/integrity.json), [đầu](evidence/before.json), [cuối](evidence/after.json). |

Hai lần đầu dựng driver edges và một lần followup có lỗi **fixture của reviewer** (lookup thân stub rg/python và hook chặn nhầm phép dò bash); đã sửa driver và chạy lại hoàn tất. Không dùng các lần driver hỏng làm finding hay kill. Log lỗi ban đầu được giữ dưới `evidence/*error.log` để phân biệt với các lượt hoàn tất được dẫn ở trên.

## Không đo được

- **N5 end-to-end môi trường sạch**: không có gốc sạch và ghi được ngoài các ancestor `.git` trong sandbox được cấp; `/var/tmp` được chọn nhưng chỉ đọc. Không tháo mount, không nới storage, không né sandbox để ép xanh. Chưa nghiệm thu lời khai 242/242 hay t86 10/10 trong môi trường executor.
- **Native Windows/macOS**: chưa đo `.exe`, PATHEXT, MSYS thật, choco/brew/apt-get thật, hoặc sàn 70% toàn bảng trên Windows. Ca `windows` ở đây là công thức chạy qua Bash/Python trên Linux và stub `cygpath` có ánh xạ `V:`.
- **10 ca launcher bỏ qua** trong mỗi suite: 8 ca venv/pip không dựng được dependency offline, 1 fixture chỉ cho Windows và 1 ca Windows SID. Không tính bỏ qua vào số đã qua.
- **11 ca `r484_*` đỏ môi trường** cùng t86/gốc tạm không được sửa theo Q8; không suy headline đột biến thành mọi kill hợp lệ. Unit proxy gốc tạm không thay phép credential thật.
- **GitHub/CI/lease ngoài bundle**: không gọi GitHub, push hay đọc check run theo chỉ dẫn. Không xác nhận ci.yml, workflow_dispatch Windows, thread resolution, heartbeat hiện hành hay quyết định nâng trần có thể ở ngoài dữ liệu được cấp. Handoff wp858 không có tại đường yêu cầu trên ref lease đã cấp; không bịa nội dung handoff.
- **Bán kính 470 mutant của cong_cu_test** chưa chạy đủ; lệnh `manh` giao phần đó cho job mảnh. Bare Ruff đã đo; contract pin/probe Ruff riêng chưa chạy.
- **Python** giữ đúng phương án (a): chỉ rc=0 và không in/ghi thư mục bản hỏng; nợ `python-probe-khong-theo-PATH` vẫn mở, không sửa `ops/cong_cu.py` và không khai checker đã probe Python ứng viên theo PATH.
- Các hướng cần soạn nội dung nhạy cảm/đường thoát cây chỉ được mô tả bằng lời; không có số đo cho chúng trong lượt này.

Toàn bộ mã review, bản sao và bằng chứng nằm dưới `out/`. Cây `kho/` không có delta quan sát được giữa hai snapshot; kiểm hai mốc không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên, và không thay cơ chế sandbox. Không tạo patch sản phẩm, commit, push hoặc quyền merge/land/deploy. Các bằng chứng có băm trong [SHA256SUMS](SHA256SUMS).
