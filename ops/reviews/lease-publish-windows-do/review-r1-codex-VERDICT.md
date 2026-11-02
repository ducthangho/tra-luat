# Cross-review REPORT.md — ghi tăng dần

Đối tượng: `ducthangho/tra-luat`, reviewed_sha `4bc94325e647ee5e32373f3af30b8f83b98a90fa`, tree `639c9a3fbf1cd5af48fa28f5a67f5d5e08184252`. Reviewer: Codex/OpenAI, công cụ shell cục bộ qua API; không dùng mạng. Chỉ ghi sandbox, không sửa `cay-kho/`. Chỉ thị cross-review của người dùng là authority và write set của lượt này.

Doctrine đã đọc: `CLAUDE.md:39–84`: bằng chứng dương, parity trên nền thật, “ca có mặt” khác “ca có đo”, phản chứng phải chạy. Mọi phép giả lập Windows dưới đây được ghi rõ; không gọi đó là chạy Windows thật.

## Kiểm cây — đã đo

Lệnh: `git -C cay-kho rev-parse HEAD HEAD^{tree}`; `git -C cay-kho status --porcelain`; `git -C cay-kho diff 1741e0a 4bc9432 --stat`; `git -C cay-kho diff 1741e0a 4bc9432 -- .github/workflows/ci.yml`.

Output: worktree sạch; đúng một tệp ci.yml, 3 dòng timeout 60→150. Hai SHA như trên. `git -C cay-kho diff f2582ba 1741e0a -- ops/lease_publish.py ops/lease_publish_test.py` và `git -C cay-kho merge-base --is-ancestor ddc41ec f2582ba` đều lỗi: không có object `f2582ba`. Vì vậy quan hệ chứa #579 và parity mã của lượt cũ hiện **KHÔNG ĐO ĐƯỢC**, không được mặc nhận từ REPORT.

## C1–C3 — ĐÚNG về kết quả suite trong log

Phép đo tái lập: `python measure_logs.py` (script ở gốc sandbox); output đầy đủ `log-measurements.txt`. Script tách timestamp, phân luồng `outer`/`[A]`/`[B]`, neo đầu dòng, so thứ tự và tập tên, không đếm lại bản tee như ca của lượt ngoài.

| Log | Lượt | vào/ra, tên duy nhất | QUA | BO_QUA | Tổng kết (dòng) |
|---|---|---:|---:|---:|---|
| Windows 36532243761 | ngoài / A / B | mỗi lượt 187/187 | 180 | 7 | 180/180; chạy=180; bỏ=7 (2471/2279/2253) |
| Ubuntu 36532243761 | ngoài / A / B | mỗi lượt 187/187 | 187 | 0 | 187/187; chạy=187; bỏ=0 (2448/2262/2259) |
| Windows 36498020895 | ngoài / A / B | mỗi lượt 187/187 | 180 | 7 | 180/180; chạy=180; bỏ=7 (2438/2235/2246) |

Mỗi lượt: thứ tự vào=ra, không tên trùng; Windows 180+7=187, Ubuntu 187+0=187. Cả ba lượt Windows bỏ đúng `{t51,t59,t60,t62,t63,t66,t68}`, A/B cùng tập với ngoài. Không thấy ca ĐỎ. 187 marker vào KHÔNG đồng nghĩa 187 ca đã thực thi đầy đủ: có marker cho ca skip và t125 trong con trả sớm để tránh đệ quy. C1 “success” phù hợp bằng chứng dương và log tiếp tục bước kế; bundle không có JSON kết luận step của GitHub để kiểm riêng trường `conclusion`.

C3 đúng về dòng kết quả; không chứng minh cây `f2582ba` đồng nhất head mới (object thiếu cả ở mirror cục bộ, `git --git-dir=kho.git rev-parse --verify f2582ba^{commit}` lỗi).

## C5 — SAI ở phần khái quát hiệu năng; ĐÚNG ở kết quả qua

Lệnh `python measure_logs.py`; mốc `<<< ra t191/t192`:

| Nền/lượt 36532243761 | t191 (s) | t192 (s) |
|---|---:|---:|
| Windows ngoài | 219.719 | 0.781 |
| Windows A | 265.546 | 0.829 |
| Windows B | 258.734 | 1.047 |
| Ubuntu ngoài | 91.076 | 0.076 |
| Ubuntu A | 157.062 | 0.117 |
| Ubuntu B | 156.992 | 0.109 |

Windows log dòng 2444/2446, 2242/2254, 2223/2225; Ubuntu 2428/2430, 2225/2230, 2220/2222. Các ca đều QUA, `t191` báo phân loại 7019 dòng. Không có ngưỡng “chậm” hay phép cô lập OS khỏi runner/tải; không thể suy “không chậm theo nền”. Lượt ngoài Windows/Ubuntu chênh khoảng 2.41× và 10.28×; đó là chênh quan sát, không phải kết luận nguyên nhân.

## C4 — SAI (có dẫn xuất thật, nhưng lời kết luận vượt cơ chế)

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3.12 probe_review.py`; output `probe-results.txt`. Script chạy bản sao tạo bằng `mktemp -d -p .`, đường dẫn lưu ở `scratch-path.txt`; chỉ tiêm `nen='nt'`/`os.name` tại seam, KHÔNG giả là Windows thật.

`ops/lease_publish_test.py:565–577` đọc YAML thật, lấy `runs-on` và trục matrix đơn giản; lý do không ghi cứng. `:2711–2712` ném `BoQuaNen`; `:10483–10489` tính lại lý do trong main. Workflow hiện có `runs-on: ubuntu-latest`. t70–t73 đều PASS trong probe. Tuy nhiên việc đọc YAML không đồng nghĩa đã phân giải đủ YAML và không chứng minh ca được phép bỏ qua: xem L1.

## L1 — Quyền skip suy từ nhãn runner nhưng thiếu ràng buộc phạm vi · P2

**Biểu hiện cùng cơ chế:**

- `ops/lease_publish_test.py:568–573` chỉ đọc `matrix.os`, bỏ `matrix.include`. Input `runs-on: '${{ matrix.os }}'; strategy.matrix: {os: [ubuntu-latest], include: [{os: windows-latest}]}` có lượt Windows thật theo cấu trúc matrix, nhưng helper trả “chỉ chạy Ubuntu”. Truyền YAML ấy qua CHÍNH `main()` trên seam nt cho `0/0 đạt; đã chạy=0, bỏ qua=1`, rc=0.
- `:10483–10489` không ràng buộc fn với workflow/job hoặc tập ca đã khai. Probe `must_measure_windows()` chỉ ném `BoQuaNen(WORKFLOW_DANG,'dang')`, được xanh rc=0, 0/0, bỏ=1. Đó là đường ca đáng lẽ phải đo bị bỏ qua; báo cáo vẫn có skip hiện rõ, nhưng cổng không chặn skip trái phạm vi. Không khẳng định log hiện có ca skip thứ tám.
- `:572–573` nhận mọi tiền tố `ubuntu-`, kể cả `ubuntu-not-a-runner`; t72 còn tạo nhãn ngẫu nhiên để tự chấp thuận. “Tên bắt đầu Ubuntu” không phải bằng chứng runner thuộc Ubuntu (nhãn self-hosted cũng là dữ liệu).
- Skip toàn `_chay_buoc_dang` ở `:2711` đặt trước đọc thân và dựng fixtures. Bảy ca dùng Bash/GitHub giả, không phải API kernel Ubuntu; thứ tự `kiem-github/check`, quy tắc rc9, cô lập lease lỗi, đếm POST và phân loại guard đều có phần logic độc lập OS. t64/t67 đã đo phần dẫn xuất YAML trên Windows; t66 lấy `_ve_dan_xuat()` rồi skip ngay vòng đầu, chưa đo phần hành vi. Việc workflow sản xuất chỉ chạy Ubuntu có thể biện minh không mô phỏng toàn job trên Windows, nhưng KHÔNG biện minh “không có gì để đo”. Chạy Bash harness trên Windows cần kiểm thêm đường dẫn/MSYS và công cụ; sandbox này chưa đo điều đó.

**Phép đo:** `python3.12 probe_review.py` in `SKIP matrix_basic ''` (đối chứng đúng), `SKIP matrix_include '…chỉ chạy Ubuntu…'`, `ARBITRARY_SKIP rc=0`, `INCLUDE_MAIN rc=0`, `META t70…t73 PASS`. Đường đi xanh giả đã thực thi, không chỉ grep.

**Hint patch:** thay quyết định nhận skip ở main bằng hợp đồng `(case_id, workflow, job, capability)` đã đăng ký; không nhận tuple do bất kỳ ca nào tự khai. Với matrix: dẫn xuất các tổ hợp sau include/exclude hoặc trả “không chứng minh Ubuntu-only” cho mọi dạng chưa hỗ trợ; không suy nền từ prefix tùy ý. Tách kiểm logic portable khỏi integration Bash, skip chỉ integration có dependency đã khai. Mở rộng `t70` hoặc thêm `t193_skip_contract`: chạy qua main với matrix Windows trực tiếp, matrix include thêm Windows, biểu thức chưa giải được, ca ngoài sổ đòi skip; tất cả phải ĐỎ khi yêu cầu skip. Đối chứng Ubuntu-only/ca đúng hợp đồng được skip. Đột biến bỏ xử lý include, bỏ kiểm case_id, hoặc skip cả phần portable phải làm ca mới ĐỎ. Đây là sửa mã và sửa C4; không chỉ đổi lý do hiển thị.

## C6 — ĐÚNG trong ba log được cấp

Lệnh `python measure_logs.py` và `PYTHONDONTWRITEBYTECODE=1 python3.12 probe_review.py`. Windows mới/cũ: 16 dòng cảnh báo fallback mỗi lượt ngoài/A/B (48/log); Ubuntu: 17 mỗi lượt (51/log). Replay từng fixture trên POSIX cho t165…t171 lần lượt `1,5,1,0,4,3,3` dòng, mọi ca PASS. Fixture tạo ProgramFiles rỗng, PATH và git.exe giả; nguồn cảnh báo là `ops/lease_publish.py` trong `_git_windows`, không phải CI tự báo thiếu Git. t168 không phát cảnh báo; không nên hiểu “t165–t171” là ca nào trong khoảng cũng phát nó. Sự lệch nền sẽ được đối chiếu thêm bằng vị trí marker log; không dùng fixture để suy mọi máy thật có Git hợp lệ.

## C7 — SAI về số lượng/định danh được gộp; ĐÚNG rằng không riêng Windows

Lệnh `python measure_logs.py`, `python3.12 probe_review.py` (gắn spy vào ast.parse, giữ thực thi ba ca t186/t188/t189).

Mỗi log có **27 SyntaxWarning tổng cộng**, nhưng chỉ **18** dòng ở `<unknown>:2555/:4509` (9+9). Sáu dòng nữa mang đường dẫn `lease_publish_test.py` (3+3); ba dòng còn lại là `bash_nen.py:900` với `\(` — REPORT bỏ mất loại này. Cả ba log cùng phân bố.

Nguồn thật: `t186:10067`, `t188:10198`, `t189:10373` gọi `ast.parse(Path(__file__).read_text(...))` (t186 qua biến `nguon`); chuỗi là TOÀN `lease_publish_test.py`, không phải lease hỏng hay mã của sản phẩm sinh động. `ast.parse` dùng compile với filename mặc định `<unknown>`. Spy chứng minh `same_as_test_file=True`, mỗi ca phát hai cảnh báo. 3 ca × 2 warning × 3 lượt = 18. Sáu warning từ biên dịch/nạp chính suite; ba `\(` từ nạp bash_nen, mỗi tiến trình một lần.

AST xác định chuỗi gây cảnh báo là docstring t42 (regex ví dụ `^\s*#…`), `_theo_duoi_va_in` (regex ví dụ `\d+`), `_tach_dinh_dang` (`\(`). Python cục bộ 3.12.3 báo dòng bắt đầu docstring 2542/4500/898; CI 3.12.10 báo vị trí escape 2555/4509/900. Không phải lệch cây. Ba ca AST vẫn PASS; chưa thấy lỗi thực thi bị che bởi các warning này. Không đủ cơ sở coi warning là một lỗi Windows, cũng không nên bỏ kiểm nguồn chỉ vì Ubuntu cùng phát. Có thể đổi ba docstring sang raw string và truyền filename vào ast.parse để chẩn đoán rõ hơn; không cần gọi đó là bản vá chức năng Windows.

Bổ sung C6 sau đối chiếu: lượt ngoài Windows phát theo ca `1,5,1,0,4,3,2`, Ubuntu `1,5,1,0,4,3,3`. `t171:7479` chỉ chạy vế thứ ba khi `os.pathsep == ':'`, giải thích chính xác chênh 1 dòng mỗi lượt. Ở A/B, stderr được tee độc lập stdout, nên warning có thể xuất hiện sau marker t168/t172; không quy nguồn bằng “dòng ở gần nhất”. Nguồn `lease_publish.py:1341–1345`, fixture replay và tổng theo từng luồng khớp nhau. Không có warning fallback ở vùng ngoài nhóm fixture trong lượt ngoài.

## C8 — KHÔNG ĐO ĐƯỢC toàn lời khai; phần gate-ops đo được

Lệnh `python measure_logs.py` (`STEP_BOUND`, `span_s`). Dùng timestamp CI, không cộng thời lượng A/B vào lượt ngoài (chúng nằm lồng bên trong).

| Nền/run | Khoảng log job (đầu→cuối, gồm setup/cleanup) | Từ đầu lệnh wrapper đến đầu bước tiếp | Marker ca đầu→ca cuối |
|---|---:|---:|---:|
| Windows 36532243761 | 1997.579443 s = 33m17.579s | 1264.076889 s = 21m04.077s | 1262.546838 s |
| Ubuntu 36532243761 | 636.121947 s = 10m36.122s | 412.331815 s = 6m52.332s | 411.760745 s |
| Windows 36498020895 | 1959.223910 s = 32m39.224s | 1181.785980 s = 19m41.786s | 1179.912202 s |

Windows mới: wrapper dòng 996 `06:51:58.9712910Z`, tổng kết 2471 `07:13:02.9555320Z`, bước tiếp 2472 `07:13:03.0481805Z`. Đây là biên log bước, không phải trường duration của API. Việc lease-publish thuộc job gate-ops cũng đo được tại `ci.yml:435–528` và tên job log dòng 50.

Không có log `gate (windows-latest)` trong evidence; **KHÔNG ĐO ĐƯỢC** lời `>80 phút tại G5`. Không có log gốc sự cố #504 trong bundle; chỉ có hồ sơ lịch sử. Một lần thành công dưới trần 150 ở head tạm, dù thực tế hết trước 60 phút, không chứng minh mọi lượt master hết dưới 60 hay xác nhận nguyên nhân sự cố cũ đã chuyển. Phạm vi hợp lệ: lần đo này gate-ops có lease-publish hoàn tất, không tái hiện timeout tại bước ấy.

## C9 — SAI: chưa đủ căn cứ đóng bằng “không có lỗi cần vá”

L1 và L2 là lỗ của suite vẫn tồn tại khi log xanh. Việc cấp/miễn lease là quyết định điều phối, không suy được từ N/N; review này không cấp lease và không sửa mã kho.

**Lịch sử Windows:**

- `git -C cay-kho log --all --format='%h %ad %s' --date=short -- ops/reviews/lease-dang-windows-review-3-claude-verdict.md` tìm `a0ab3b8` ngày 2026-08-22.
- `git -C cay-kho show a0ab3b8:ops/reviews/lease-dang-windows-review-3-claude-verdict.md` tại đoạn W3′ ghi run `32567293842`, head `7f91ea1cffe17af391362a91b83907c32b16f3b2`, Windows 65/65 + 8 skip; Ubuntu 73/73. Đây là hồ sơ review lịch sử có run/head, không phải log CI thô được tải lại ở phiên này.
- `ops/handoff/lease-dang-windows-exec-4-codex-handoff.md:46–58` ghi thêm run `32568867269`, head `e969739cb3aed38a4aad575df4184f541275f31f`, Windows 65/65 + 8 skip.
- Log thô đã cấp 36498020895 còn chứng minh trực tiếp lượt Windows trước lượt mới: 187 marker và cả t191/t192 QUA. SHA đầy đủ nằm dòng 686/702 là `f2582ba9856a7cad41e6bf284914007e5e34d71d`; object ấy thiếu ở checkout và mirror nên chưa kiểm được quan hệ chứa #579/parity blob.

Vì vậy “suite chưa từng chạy trên Windows” là sai nếu nói cả lịch sử suite. Với **đúng phiên bản #579**, phải neo blob/head và mốc thời gian phát biểu; lịch sử 73 ca không chứng minh bản 187 ca đã đo, nhưng log cũ đã có t191/t192. Không được dùng một trong hai ý để tráo ý còn lại.

**t192 có đo đúng spawn Windows không?** `python3.12 probe_extra.py` (`extra-results.txt`): ca nguyên vẹn PASS; các cặp `(rc, Popen)` là `(12,0),(12,0),(0,1)`. Đột biến `_con_thoi_gian=lambda ...:1.0` làm ca ĐỎ ngay (đòi rc12, nhận rc0). `lease_publish.py:1641` thực sự gọi `subprocess.Popen`; t192:9916 bọc chính module subprocess của sản phẩm và gọi tiếp Popen thật. Kiểm AST mã CPython cục bộ `/usr/lib/python3.12/subprocess.py:1436` cho nhánh Windows `_execute_child` gọi `_winapi.CreateProcess`. Popen KHÔNG phải cơ chế chỉ có POSIX; không tìm thấy lỗi “đếm nhầm API spawn Windows” trong mã hiện hành. Đối chứng dương một spawn của t192 đã QUA trong cả ba lượt Windows log.

Giới hạn: bộ đếm đo lời gọi Popen trong đoạn `kho.commit`, không đếm mọi CreateProcess của hệ điều hành, không đếm subprocess trong constructor `KhoObject` (được dựng trước patch), không đo cháu của git. Đó phù hợp lời khai hẹp “không spawn cat-file trong doc khi hết hạn”; không đủ để nói “không sinh bất cứ tiến trình Windows nào”. Phản chứng tại chỗ ở POSIX; chưa có lượt đột biến trên Windows thật vì sandbox không có nền ấy.

## L2 — A/B so sự giống nhau nhưng không xác nhận đã đo đủ · P2

Vấn đề bổ sung REPORT không nhắc tới, thuộc suite đang chạy trên Windows và cả Ubuntu.

**Biểu hiện:** `ops/lease_publish_test.py:4611–4618` chỉ tìm dòng tổng kết đầu tiên bằng regex không neo đầu dòng và lấy rc/tập đỏ/tập skip; `:4378–4379` trả KHỚP khi hai tuple giống nhau; `:4658–4659` chỉ chốt KHỚP. Không đòi tập vào/ra trùng CA, không kiểm tổng chạy+skip=187, không đòi tập skip hợp đồng. Cả hai con cùng mất phép đo vẫn được tính t125 đạt. `t160:6762–6781` hiện chỉ dựng summary/tập lỗi để thử parity, không thử tính đầy đủ; sửa t125 phải cập nhật fixture này để giữ đối chứng hợp lệ.

**Phép đo đã chạy:** `PYTHONDONTWRITEBYTECODE=1 python3.12 probe_extra.py`, output `extra-results.txt`. Thay duy nhất argv tại seam `_mo_con_nhom_rieng`, mở HAI Python con thật; giữ nguyên wait, tee, parser, classifier và chốt của t125:

```text
AB empty_summary PASS real_children 2 case_markers 0
AB partial_summary PASS real_children 2 case_markers 0
AB missing_summary RED ... KHÔNG ĐO ĐƯỢC dòng tổng kết; rc=0
```

Con lần lượt chỉ in `lease_publish: 0/0 đạt; đã chạy=0, bỏ qua=0`, hoặc `1/1 …`, rồi thoát. Đối chứng không có summary bị bắt, chứng minh test thực sự chạm consumer. Không khẳng định ba log đã rơi vào lỗ này: phép đo C1–C3 độc lập đã xác nhận đủ tập ca. Cũng không đòi mọi tuple đỏ giống nhau phải mất thuộc tính parity; lỗi là thiếu bằng chứng hai phép so đó đã chạy đủ suite. Một lỗi chỉ xảy ra ở nhánh con `CO_AB` có thể làm cả hai con hụt ca mà lượt ngoài không hụt.

**Hint patch:** tách parser kết quả con thành một cửa xác minh transcript hoàn chỉnh trước khi so A/B: summary đúng một dòng neo đầu dòng; mọi CA dự kiến có đúng một vào/ra theo thứ tự; tên/status không lạ/không trùng; N/M và chạy/skip khớp transcript; tổng bằng tập đăng ký ở head; skip phải đúng hợp đồng L1. Sau đó mới so parity. Thêm `t194_AB_du_bang_chung_truoc_so_sanh` hoặc mở rộng t160: hai vế cùng 0/0, cùng 1/1, mất cùng một ca, trùng tên, thiếu `ra`, summary lệch markers đều phải ĐỎ; đủ tập ca và skip hợp lệ phải QUA. Đột biến bỏ validator hoặc chỉ so số tổng thay tập tên phải làm ca mới ĐỎ. Sửa mã test/harness, không phải sửa mã nghiệp vụ lease.

## L3 — Kết luận và provenance rộng hơn bằng chứng được cấp · P2

**Biểu hiện:** REPORT.md:3–5 “chưa từng chạy”/“không cần vá”; :12–14 xác nhận parity `f2582ba`; C5 suy hiệu năng từ kết quả QUA; C7 gộp 27 warning vào hai loại/địa chỉ; C8 khai `gate Windows >80 phút` khi bundle chỉ có gate-ops; C9 đóng phiếu. Đây cùng lỗi ranh giới chứng cứ: kết quả một lần chạy, một loại log hoặc một bản cây bị nâng thành kết luận rộng hơn đối tượng đã đo. C4 có lỗi mã riêng đã gom L1, không tách thêm lớp theo từng câu.

**Phép đo:** `python measure_logs.py`, `python3.12 probe_review.py`, `python3.12 probe_extra.py`; các lệnh Git nêu ở phần kiểm cây/C9. Toàn bộ số và giới hạn ở C1–C9 phía trên. Đo thêm tập tên giữa ba log bằng regex neo `^\S+ >>> vao (\w+)`: cả ba cùng 187 tên, tập bằng nhau. Điều đó chứng minh parity tên ca, không chứng minh parity bytes mã của head cũ.

**Hint patch — chỉ sửa BÁO CÁO cho lớp này:** thay phần kết luận bằng:

> Trên head tạm `4bc94325e647ee5e32373f3af30b8f83b98a90fa`, log 36532243761 ghi Windows 180 ca đạt, 7 ca skip; Ubuntu 187 ca đạt. Cả hai có đủ 187 cặp vào/ra; A/B có cùng tập ca và skip. Không có ca đỏ trong các lượt đó. Tuy vậy cross-review phát hiện hợp đồng skip chưa kín và t125 chưa xác minh hai lượt con đo đủ suite, nên chưa đủ căn cứ kết luận không cần vá hay đóng phiếu.

Các câu thay thế bắt buộc kèm theo:

- C4: “Lý do skip được đọc từ YAML thật; bộ giải hiện chỉ hỗ trợ dạng runs-on/matrix đơn giản, chưa xử lý include và chưa ràng buộc quyền skip theo ca. Bảy integration test Bash bị bỏ qua trên Windows; không đồng nghĩa mọi phần logic của chúng không đo được trên Windows.”
- C5: “Lượt ngoài Windows mới: t191 219.719s, t192 0.781s; các lượt A/B: 265.546/258.734s và 0.829/1.047s. Tất cả qua; chưa cô lập nguyên nhân chênh thời gian giữa nền.”
- C7: “Mỗi log có 27 SyntaxWarning: 18 từ ast.parse toàn tệp test với filename mặc định `<unknown>`, 6 khi nạp tệp test, 3 từ docstring bash_nen. Chưa thấy lỗi thực thi do ba docstring này; không riêng Windows.”
- C8: “Khoảng log gate-ops Windows mới là 33m17.579s; khoảng bước wrapper là 21m04.077s. Lần này không tái hiện huỷ ở lease-publish. Bundle không có log gate Windows/G5 để xác nhận >80 phút hoặc kết luận triệu chứng master đã chuyển chỗ.”
- Lịch sử: “Suite đã có hồ sơ chạy Windows từ 2026-08-22; log 36498020895 cũng đã chạy t191/t192. Chưa đối chiếu được blob với `f2582ba` vì object không có trong bundle; cần bổ sung object/bằng chứng blob nếu dùng lượt cũ làm đối chứng cùng mã.”

Không đề nghị test rXX_/tXXX_ cho lớp thuần báo cáo; các script review kèm theo là phép kiểm số liệu tái lập. Không lấy việc sửa chữ thay cho hai bản vá harness ở L1/L2.

## Giới hạn và kiểm bảo toàn cây

- Không có nền Windows thật tại sandbox, không có mạng: không chạy lại CI Windows, không truy vấn Issue/step conclusion, không tải object thiếu. Log thô được coi là bằng chứng CI do người dùng cung cấp; chưa xác thực lại máy chủ.
- Không chạy lại toàn suite tại chỗ: phạm vi là cross-review báo cáo; đã đo toàn transcript ba log và chạy các probe mục tiêu trên bản sao. Không tuyên bố suite hiện tại xanh trên máy này.
- Lệnh kết thúc `git -C cay-kho status --porcelain` cho output rỗng; `git -C cay-kho diff --exit-code` rc=0. Không sửa checkout review. Script và output đo nằm ở gốc sandbox; bản sao tạm được ghi trong `scratch-path.txt`.
- Warning docstring là ghi nhận, không có bằng chứng che lỗi thật. Không bịa finding về Popen Windows: t192 đếm đúng đường gọi hiện hành, trong phạm vi nêu ở C9.

| lớp | mức | sửa mã hay sửa báo cáo |
|---|---|---|
| L1 — Quyền skip thiếu ràng buộc phạm vi | P2 | Mã harness/test + báo cáo C4/C9 |
| L2 — A/B không xác minh phép đo đầy đủ | P2 | Mã harness/test + báo cáo C9 |
| L3 — Kết luận/provenance vượt bằng chứng | P2 | Báo cáo |

VERDICT: CHANGES_REQUIRED
