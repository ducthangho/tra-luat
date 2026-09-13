verdict: changes_requested
reviewed_sha: aaef55bf77f061015d46b14411475d7f448beb05

**0 P1 / 4 P2 / 0 P3; 5 thể hiện, 5 hunk / 1 tệp.** Năm hunk lượt 6 sửa đúng những thể hiện đã chỉ, nhưng **chưa đóng cả ba lớp**: còn một con trỏ thiếu nội dung đã hứa, một biến chưa cấp đường dẫn và một kết luận vượt phép so tên ref. Tìm thêm lớp **neo-sha-tu-head-dong**, có hai tuyến lấy lại head PR thay cho SHA của dữ liệu đang review. Chín cổng nền đều rc=0; chúng không chứng minh nội dung tài liệu đúng.

Reviewer: Codex, dựa trên GPT-6 theo chỉ thị phiên; provider OpenAI (`openai_codex`), execution surface agent có shell sandbox qua API, transport `machine`. Không có bằng chứng độc lập về backend model/effort tạo verdict. CLI cục bộ Codex 0.154.0 và Claude Code 2.1.269 là công cụ được thử, không chứng nhận danh tính reviewer.

Authority/phạm vi là PROMPT.md của gói: chỉ đọc kho được review, ghi VERDICT/HINT/evidence trong gói và thử trên bản sao riêng ngoài cây. Không mạng, không push/merge/đăng GitHub, không sửa cây `cay-kho/`, không gọi reviewer con hoặc tự soạn payload tấn công. State của `record-review` trong phép thử là fixture riêng, không là lease/assurance thật. Không xác thực authority/GitHub/generation hiện hành ngoài snapshot được giao.

Git xác nhận exact HEAD; tree **0533eb814e9b642953aadd7af509173fc941d194**. Base **bb7013c7669da19304a8769e5b25f8c1f8951e9c** là ancestor. Diff toàn PR: đúng **.claude/skills/cross-review/SKILL.md**, **+230/−141**, HEAD **509 dòng**, base 420 dòng. Cây nguồn sạch trước và sau phép đo. [Kiểm cuối](evidence/final-check.json).

## Bản vá lượt 6 có đóng cả lớp không

**ĐỐI CHIẾU LƯỢT TRƯỚC:** đã đọc VERDICT-LUOT-6.md, HINT-LUOT-6.patch và VERDICT-LUOT-5.md trước các phép đo nội dung. Replay nguyên HINT lượt 6 lên blob `e849e2eb341801155cd20341b9f77b5116329dcc`: `patch -p0 --fuzz=0 --verbose` **rc=0, 5/5 hunk**, kết quả **bằng byte HEAD**. [Replay và phản chứng bổ sung](evidence/extra-probes.json).

| Finding lượt 6 | Kiểm năm hunk trên HEAD | Kết luận về lớp |
|---|---|---|
| va-qua-tay-mat-cong-cu | H1: heading “Neo theo *kho*, không theo đường dẫn” tồn tại ở GOI_AGENT_DA_NEN L395–413; chứa workspace/TL_WORKSPACE, expected-repo, expected-root-commit, chuẩn hoá host và loại remote local. Launcher check trên cùng clone: origin local **11**, URL repo **0**, không fetch HTTPS. Quyền review vẫn có con trỏ §8/13 ở L220. | **ĐÃ VÁ THẬT O01 cũ**, không mất hợp đồng quyền; **lớp còn O01 mới L458–459**. |
| loi-khai-vuot-phep-do | H2: thử `cd` vắng, interpreter trả0/7, interpreter vắng, echo lỗi. H5: đối chiếu mã thật và15 ca finding, gồm cả same-failure. | **ĐÃ VÁ THẬT E01/E02 cũ**, không thấy câu mới sai; **lớp còn E01 mới L316–321**. |
| lenh-khong-noi-hien-vat | H3: diff thực lưu GOI_Y_VA.diff rồi patch đọc được, block rc0. H4: cả3 body-file đọc đúng VERDICT.md, mỗi lần72 byte trên filesystem phân biệt hoa/thường. | **ĐÃ VÁ THẬT A01–A04 cũ**; **lớp còn A01 mới L223–227/242**. |

Không phát hiện lỗi mới do chính năm hunk lượt 6 sinh ra. Các thể hiện tìm ở lượt này nằm ở phần đã có trước chúng. Lượt 6 đã vá đúng các điểm cũ nhưng phép quét toàn lớp chưa đủ phủ; bảng “0 sau HINT” của lượt ấy không thay phép kiểm lần này.

**H2 — đủ nhánh shell:** số `echo` in lần lượt **1/0/7/127** cho cd lỗi/interpreter trả0/interpreter trả7/interpreter vắng. Ba nhánh cd thành công được phân biệt với nhánh chưa gọi interpreter. Khi echo ghi vào stdout đã đóng, echo **rc=1**, không phải0. Câu HEAD nói “vẫn có thể trả0”, không bảo đảm echo luôn0; không có finding tại câu ấy. [H2-* trong log](evidence/probes.json).

**H5 — đủ nhánh helper:** approve/blocked thiếu finding **rc0**; changes_requested thiếu finding **rc2**; slug sai **rc2** với cả ba verdict; slug hợp lệ dưới trần **rc0**; slug đã có count1 với limit2 **rc3**, review vẫn được lưu và state thành blocked với cả ba verdict. Slug lặp hai lần trong một review chỉ tăng count1. Bốn ca SHA vắng/sai/viết hoa/viết tắt đều **rc5**. Câu mới giới hạn ở nhánh kiểm finding và không hứa slug hợp lệ luôn thành công; §12 và help root đã dẫn nhánh trần. Không bổ sung doctrine để mô tả lại trần trong adapter.

**H3/H4:** redirect `>` phù hợp lane a/cay,b/cay với `patch -p1`; không mâu thuẫn lane HINT repo-relative/p0 được nói ở mục trước. `diff` riêng trả1 khi có khác biệt là bình thường; block tiếp tục patch và trả0. Quét lại mọi tên hiện vật không còn lỗi hoa/thường khác. Gh thật không chạy; đây là kiểm shell/filesystem bằng stand-in có nhãn.

## Kiểm mọi con trỏ và mọi khối lệnh

Đã đọc đủ **509/509 dòng**, kể cả frontmatter, bảng, comment và code. Không dùng danh sách lỗi cũ làm phạm vi. Với mỗi con trỏ hỏi hai câu riêng: đích tồn tại và nội dung đích có thực hiện lời hứa của câu dẫn không. Với mỗi lệnh lập tuyến đầu vào → lệnh → stdout/tệp → nơi đọc, rồi thay placeholder và chạy trong fixture ngoài kho.

[Kiểm kê con trỏ đầy đủ](evidence/pointer-audit.md) kê từng nhóm và **đủ vị trí xuất hiện** của §4/8/9/12/13, tên tệp, tên mục, hàm, đường dẫn và hiện vật. [76 vị trí inline](evidence/pointer-occurrences.json) chỉ là chỉ mục hỗ trợ; regex đó bỏ code/prose trần, nên không được nhận là toàn phép quét. Code/prose/heading còn lại được kê trong bảng con trỏ và [nguyên văn23 fence](evidence/blocks.json).

**23 fence:** 21 chứa lệnh, 2 là template Markdown không phải chương trình. [Bảng từng khối B01–B23](evidence/command-audit.md) nêu phần chạy thật, phần stand-in và thay thế cụ thể; [script](evidence/probes.py) cùng [log](evidence/probes.json) giữ command/cwd/rc/stdout/stderr. Không gọi “đã chạy model/GitHub” từ stand-in.

Các kết quả phân biệt được lỗi với giới hạn:

- B04→B05: stand-in Claude nhận **131072 byte qua stdin**, tạo reviewer.json, vị từ thật đọc được/rc0. CLI thật với đúng cờ cộng `--help` cũng0; không phải lượt model review.
- B06/B11: stand-in Codex nhận stdin đúng. CLI Codex thật stdin rỗng **rc1/No prompt provided via stdin**. Launcher thật với child Python cục bộ nhận stdin0 byte dù caller cấp input, đọc đúng snapshot qua `{PROMPT_FILE}`, launcher rc0. [Log CLI/launcher](evidence/cli-probes.json).
- B08: chạy nguyên block chẩn đoán, kể cả sleep60, **60,193 s**. Hai mẫu cùng `1789221367 72`; child vẫn sống. Không suy tệp yên lặng thành reviewer chết.
- B10: không cấp RV, clone **128** và không tạo được thư mục; khai RV trước khối → **0**. Chỉ HTTPS fetch dùng stand-in. **A01/H2**.
- B12–B15: dựng mirror thật, fetch nguồn local, clone đầy đủ; đối chiếu worktree/clone với core.abbrev7 đều doc-claims0. Giữ worktree tạm, thay riêng dòng remove bằng stand-in có nhãn. B14 so tập tên từ remote cục bộ; không đo GitHub. B15 bỏ lọt OID ref khác dù tập tên bằng nhau. **E01/H3**.
- B17: chạy phần lệnh trước mũi tên mô tả, shell tự-khớp bị SIGKILL (`-9`), mẫu ngoặc in CHAY/0. B18 không có con khớp: grep-count stdout0/rc1, không gọi đó là gate đỏ.
- B20/B21: GOI_Y_VA.diff có producer và consumer khớp; ba VERDICT.md đọc được. B22 vẫn sai **nguồn SHA** dù cú pháp, slug và chữ hoa/thường đúng. **T02/H5**.

B02 chỉ chạy cả khối bằng stand-in: doctor thật có probe xác thực, npm install và chuan-bi có tác động mạng/credential nên không thực hiện. B23 và MCP/GH là stand-in hoặc đọc cú pháp. Các placeholder `<…>` là đầu vào được đặt tên trong ví dụ; lỗi RV khác chúng vì dùng biến shell rỗng mà toàn tài liệu chưa khai báo.

## Sáu lớp — bảng quét

Cách quét: với mỗi vùng liên tục trong [ledger23 vùng](evidence/scan-inventory.md), hỏi riêng sáu lớp theo **chủ thể/điều kiện/lượng từ**, **nguồn và sức chứng minh**, **producer/consumer**, **nhánh trạng thái/rc**, **đơn vị/mẫu số** và **đích con trỏ**. Sau đó đối chiếu công cụ/source, chạy block và phản chứng. [Ledger có hash/độ phủ](evidence/semantic-ledger.json) là annotation thủ công; mã kiểm phủ dòng không phải máy đọc nghĩa.

| Lớp | Thể hiện sống trên HEAD | Sau HINT | Đột biến |
|---|---:|---:|---|
| adapter-chep-doctrine | 0 | 0 | M1 |
| va-qua-tay-mat-cong-cu | 1: O01 | 0 | M2 |
| lenh-khong-noi-hien-vat | 1: A01 | 0 | M3 |
| loi-khai-vuot-phep-do | 1: E01 | 0 | M4 |
| phan-hoach-trang-thai | 0 | 0 | M5 |
| don-vi-byte | 0 | 0 | M6 |

**va-qua-tay-mat-cong-cu — đủ1 dòng sống:**

| ID | Dòng HEAD | Đích thiếu nội dung gì? | Hunk |
|---|---|---|---|
| O01 | 458–459 | §9 và CLAUDE/Quy ước deploy có policy/tái sinh/verify nhưng không tooling hoặc cú pháp sinh manifest đã hứa. Recipe có ở §10.2; CLI thật `scripts/tl.py release-manifest --help` mô tả cờ. Sinh manifest ngoài clone rc0, byte bằng HEAD. | H4 |

**lenh-khong-noi-hien-vat — đủ1 dòng sống:**

| ID | Dòng HEAD | Tuyến bị đứt | Hunk |
|---|---|---|---|
| A01 | 223–227; dùng lại242 | `$RV` chưa được gán hoặc mô tả đầu vào ở đâu trong tệp; R ở263 là biến khác. Fresh shell mở rộng RV thành rỗng, clone128. Gán một lần trước clone nối đủ mọi lần dùng. | H2 |

**loi-khai-vuot-phep-do — đủ1 dòng sống:**

| ID | Dòng HEAD | Phép đo hẹp → lời khai rộng | Hunk |
|---|---|---|---|
| E01 | 316–321 | So tên refs/remotes/origin và cờ shallow được mô tả là kiểm mirror nhận đủ cái nguồn đang có. Đổi riêng OID master từ63075a7… thànhbb7013c… trong clone: vẫn không diff tên, stdout chỉ false, rc0. HINT so thêm OID, ghi riêng rc diff và giới hạn rõ namespace/object. | H3 |

**adapter-chep-doctrine — bảng sống0 dòng:**

| ID | Dòng | Nghĩa vụ review tự đặt |
|---|---|---|

Không tìm thấy tiêu chí hoàn tất, assurance, budget hoặc schema tự đặt. Bảng model mô tả _BAC/chon; các chữ “BẮT BUỘC” về remote/config và mẫu pkill là cú pháp công cụ hoặc dẫn yêu cầu nguồn; bảng ≥6 là lịch sử prompt; template verdict ghi rõ chưa đủ schema. M1 bơm nghĩa vụ mới, phép đọc phát hiện dù doctrine-scan vẫn0.

**phan-hoach-trang-thai — bảng sống0 dòng:**

| ID | Dòng | Nhánh bị nhập/tách sai |
|---|---|---|

Đã rà rc/subtype/model; EOF chưa review; quota khác unsupported; header chưa có; thiếu/hỏng sổ/key; PID danh tính khác sống; Z đã thoát; mẫu tệp im; cd/interpreter/echo; ls-remote không đo do mạng; diff1; grep-count1; blocked/same-failure3; state reject5. Không thấy câu HEAD đồng nhất skip/cancelled/chưa đo thành pass. T01/T02 bên dưới là **gán sai revision đầu vào**, không phải helper phân loại sai rc; không cộng lại vào lớp này.

**don-vi-byte — bảng sống0 dòng:**

| ID | Dòng | Sai đơn vị / quy đổi / mẫu số |
|---|---|---|

Đã rà đủ các số: bậc0/1–2/3–4/≥5; 9 lượt với8/9,6/9,3/9,2/9 là nhóm có thể giao nhau; ví dụ500/90000 token không phải share đã đo; 3/3 probe;1.151s; bốn mục Codex/ba model/bốn effort; khoảng4h; hai sự cố;80/50 dòng;60s và stat `%Y` giây/`%s` byte;40phút;201heads là lịch sử;3/13 và154/437/299s;35lệnh;6/8/2 của bảng prompt;526con và14,5/16GB;7lượt/6HINT/13hunk #518 khác mẫu2/5 #250/#252; OID40hex khác prompt SHA25664hex. Không thấy sai phép quy đổi hoặc lẫn mẫu số.

Các câu ưu tiên trong PROMPT đã thu hẹp đúng: effort max chỉ bị từ chối ở spark/phép thử #518; quota không còn khai pool độc lập; launcher “có thể” còn dang_chay; ba dấu hiệu không được tuyên mỗi cái là cần; số lịch sử giữ đúng nhãn đợt. **Không có raw log để đo lại phần lớn số lịch sử**, nên đây là kiểm phạm vi/nhất quán, không chứng nhận từng số đã xảy ra. Commit #518 chỉ đối chiếu được nguồn thuật lại7/6/13.

## Lớp KHÁC tìm được

**neo-sha-tu-head-dong — đủ2 thể hiện, một finding P2:**

| ID | Dòng HEAD | Phản chứng đã chạy | Hunk |
|---|---|---|---|
| T01 | 207–212 | Gh stand-in thông báo head A ở view, sau đó diff ở B; Git thật tạo numstat từ base→A. Block0 nhưng diff **41.126 byte** ứng với **+230/−141**, numstat lại ghi **+223/−137** của A. Heading hứa diff đúng head, hai artifact thực không cùng revision. | H1 |
| T02 | 485–491 | VERDICT.md giữ SHA A, state đang reviewing B; gh stand-in trảB. Mẫu record-review nhậnB và **rc0**, lưuB dù artifact vẫnA. Đây là cửa tái hiện khi state đã chuyển sang lượt mới nhưng reviewer cũ ghi muộn. | H5 |

[Script/command/output và SHA đầy đủ](evidence/extra_probes.py), [log](evidence/extra-probes.json). A là head lượt6 e849e2e…, B là HEAD aaef55b…, chung base bb7013c…; cả ba commit có thật. Gh được mô phỏng tường minh, còn Git và packet_loop chạy thật. Không khẳng định đã quan sát race trên GitHub.

Protocol đã yêu cầu exact reviewed_sha; con trỏ tới protocol không làm hai lệnh này dùng đúng nguồn dữ liệu. HINT dùng cùng cặp OID đã chốt để sinh diff/numstat, và truyền reviewed_sha từ verdict vào record-review. Trên bản đã áp: diff và numstat đều bằng byte kết quả base→A; gửi A khi stateB trả **5**; gửiB khi stateB trả **0**. Không sửa helper/state machine hoặc thêm doctrine. [Kiểm bản đã áp với cùng hai head thật](evidence/extra-probes.json).

Không tìm thêm lớp khác. Không coi thiếu quyền dịch vụ, thiếu raw log lịch sử hoặc lỗi harness là finding sản phẩm.

## Phép đo nền

Hai clone riêng, sạch và đầy đủ nằm **ngoài** cây review: `/tmp/rv521-l7-0ewdssrx/gates` và `/tmp/rv521-l7-0ewdssrx/experiments`. Detached exact HEAD, non-shallow, `core.abbrev=7`, `core.autocrlf=false`. Cả nguồn/mirror/hai clone có **356 refs/heads**, so **tên+OID** bằng nhau. Origin đặt URL repo để tái lập kiểm danh tính, không fetch HTTPS. [Thiết lập](evidence/setup.json), [runner cổng](evidence/run_gates.py).

PATH đặt thư mục chứa `cong-cu/actionlint.IlOjyy/actionlint` trước khi chạy bộ cổng. Python3.11.15, Git2.43.0, GNU patch2.7.6. Mọi lệnh dưới chạy từ gốc clone gates sạch; mỗi log giữ stdout/stderr và rc thật.

| Lệnh | rc | Bằng chứng dương |
|---|---:|---|
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | 0 | 7 tệp,0 chuỗi cấm. [Log](evidence/gate-doctrine.json). |
| `python3 .claude/dev/packet_loop.py adr-song --root .` | 0 | 47 ADR/47 hàng, ngoại lệ trạng thái0016 công bố. [Log](evidence/gate-adr.json). |
| `python3 ops/bien_nhan_v2.py --root .` | 0 | 113 đạtv2 +11/11 miễn legacy +42 nợ đóng băng =166;0 vi phạm/chưa đo. **Không gọi166 là đạtv2.** [Log](evidence/gate-receipts.json). |
| `python3 ops/lease_publish_test.py` | 0 | 147/147 đạt, chạy147, bỏ qua0;37mutant:34giết,3sống chủ ý,0tín dụng giả. [Log](evidence/gate-lease.json). |
| `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | 0 | ok=true;expected=checked=180;hash khớp;failed/extra/missing/errors rỗng. [Log](evidence/gate-release.json). |
| `python3 scripts/tl.py golden-test --json` | 0 | ok=true,20ca. [Log](evidence/gate-golden.json). |
| `python3 scripts/tl.py doc-claims-check --strict --json` | 0 | ok=true;107tệp;0hardflag,374advisory. [Log](evidence/gate-claims.json). |
| `python3 .githooks/eol_policy.py --all --json` | 0 | 2082scanned,2060checked,22skipped,0vi phạm. [Log](evidence/gate-eol.json). |
| `python3 .claude/dev/idiom_py_test.py` | 0 | 7ca,0bỏ qua,9mutant,7tệp phạm vi. [Log](evidence/gate-idiom.json). |

**Không cổng nền nào đỏ**, nên không có finding cổng cần lặp trên clone sạch thứ hai. Các rc khác0 của mutation/cd/EOF/slug/diff/grep là ca phản chứng đã tách riêng. B13 còn đo độc lập doc-claims0 trên worktree và clone cùng SHA; không gọi đó là chạy lại toàn chín cổng. Sau HINT, doctrine/idiom/doc-claims strict/git diff--check đều0.

Sự cố harness duy nhất cần nêu: runner phụ ban đầu thử mở HINT-LUOT-5.patch nhưng gói không có tệp ấy; đã ghi NOT_RUN cho replay lượt5, tiếp tục các phép đo còn lại. Không nhận lời replay43hunk của verdict cũ thành phép đo lượt7. Năm hunk lượt6 đã replay đầy đủ. Không dọn thư mục tạm.

## Đột biến và khôi phục

Chạy bằng `python3 evidence/mutations.py` trên clone experiments đã áp HINT, không chạm cây nguồn. Ba lớp vốn0 trên HEAD được giữ nguyên nội dung liên quan trên bản này; kiểm thêm cả ba lớp vừa vá để đo bản gợi ý. [Script](evidence/mutations.py), [log đầy đủ trước/sau/khôi phục](evidence/mutations.json), các bản mutant-* lưu trong evidence để đọc lại.

| Đột biến | Lệnh/oracle và kết quả thực | Oracle trước → sau → khôi phục | Kết luận |
|---|---|---|---|
| M1 — doctrine | Bơm “Reviewer phải nộp ít nhất chín phản chứng mới được kết thúc lượt.” Đọc lại chủ thể/nghĩa vụ/điều kiện hoàn tất; thêm1 dòng sống. doctrine-scan vẫn0 ở cả ba bản. | **0→1→0** | Phép đọc bắt doctrine ngoài danh sách chuỗi. Script chỉ ghi/kiểm annotation, không là semantic detector độc lập. |
| M2 — con trỏ | Đổi đích recipe manifest §10.2→§9. Resolver thấy **cả hai heading tồn tại**; đọc đúng đoạn đích chỉ §10.2 có `release-manifest --root` đã hứa. | **0→1→0** | Bắt con trỏ tới mục có thật nhưng thiếu nội dung, cùng hình dạng O01. |
| M3 — hiện vật | Đổi riêng B21 comment sang verdict.md. Trích và kiểm **cả3 body-file**; 3đọc được→1vắng→3đọc được. | **0→1→0** | Phép nối không chỉ kiểm một lệnh trong nhóm. |
| M4 — lời khai/ref | Giữ một OID master sai trong clone fixture, đổi format tên+OID của cả hai vế thành tên. Diff riêng **1→0→1**; rc cuối block vẫn0 vì đọc shallow sau đó. | **0→1→0** | Bắt mất dữ liệu OID; không dùng rc cuối block làm oracle. Ref fixture cũng được trả về OID gốc. |
| M5 — trạng thái | Đổi lệnh key trong adapter `sys.exit(0 if k else 1)`→`sys.exit(0)`; trích lệnh chạy PID vắng. CLI **1→0→1**, stdout luôn KHONG_DO_DUOC. | **0→1→0** | Bắt nhánh chưa đo bị báo thành công dù thông báo không đổi. |
| M6 — đơn vị | Đổi **mẫu stat thứ nhất** `%s`→`%b`. Cùng tệp9byte: hai số **9/9→8/9→9/9**. Chạy hai stat thật, bỏ khoảng chờ chỉ trong oracle đơn vị; B08 đã chờ60s thật riêng. | **0→1→0** | Bắt trộn block512byte với kích thước byte, tránh đọc sai thành tệp thay đổi. |
| M7 — câu nghi nhất H5 lượt6 | Bơm lời khai approve/blocked thiếu finding luôn bị chặn. CLI approve không finding vẫn **0→0→0**, nhưng lời khai mutant mâu thuẫn output/state. | **0→1→0** | Phép kiểm câu không phụ thuộc cổng hay tự đổi mã sản phẩm cho khớp lời khai. |

Mỗi mutation có hash trước/thay/khôi phục và `restored_byte_match=true`. Sau cả đợt, bỏ HINT khỏi clone bằng phục hồi nguyên byte adapter gốc: SHA256 **956ce09f6f8f20c828aa2f3d6fd331b7feac3e83770e76dfe4aadecb2daf719b**, git status rỗng. Đây là bằng chứng khôi phục của thao tác đã ghi log, không dùng status rỗng để chứng minh lịch sử bất kỳ chưa từng ghi. [Kiểm cuối](evidence/final-check.json).

## HINT.patch và giới hạn

**Nhãn patch-as-hint:** “chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit”.

[HINT.patch](HINT.patch) là unified diff repo-relative cho **patch-p0**, **5hunk/1tệp**, chỉ `.claude/skills/cross-review/SKILL.md`. Đã chạy đúng:

```bash
cd cay-kho && patch -p0 --fuzz=0 --dry-run < ../HINT.patch
```

**rc=0**; kiểm verbose cũng0, cả5hunk không fuzz/offset. Áp thật trên clone experiments bằng `patch -p0 --fuzz=0 --verbose` rc0, bằng byte [bản soạn520dòng](evidence/adapter-fixed.md). Bản áp đã thử lại các tuyến thay đổi và bốn check thích hợp; clone sau đó khôi phục sạch. [Log áp/mutation](evidence/mutations.json), [kiểm cuối](evidence/final-check.json).

| Hunk | Finding sở hữu duy nhất | Đủ thể hiện đóng |
|---|---|---|
| H1 | neo-sha-tu-head-dong | T01 L207–212 |
| H2 | lenh-khong-noi-hien-vat | A01 L223–227 và lần dùng242 |
| H3 | loi-khai-vuot-phep-do | E01 L316–321 |
| H4 | va-qua-tay-mat-cong-cu | O01 L458–459 |
| H5 | neo-sha-tu-head-dong | T02 L485–491 |

**Không thay chính các câu HINT lượt5 hoặc lượt6 vừa viết.** Git blame: lời khai ref/format là từ9fd53ab5; con trỏ manifest từ74dd1f74. H3 giữ nguyên comment shallow ở L321 do lượt5 viết; H4 thay con trỏ có từ lượt2. H1/H2/H5 sửa lệnh hoặc bổ sung đầu vào tại phần cũ, giữ nguyên các câu giải thích H1/H2/H5 của lượt6. Không có finding buộc đổi lại một câu mới chỉ để “bắt vá sinh lỗi”.

SHA256 HINT: **f4c884e858c0e401d730e877a4ae60b51983ab4ed05cf0e0773618eff954acbd**. Mỗi hunk thuộc đúng một finding; H2 định nghĩa một biến để nối toàn bộ các lần dùng, không cần lặp assignment ở mọi dòng. Đọc lại cả bản520dòng: sáu lớp và lớp mới đã kê đều0 thể hiện trên **bản gợi ý**; verdict của HEAD gốc vẫn changes_requested.

Giới hạn: không đo model/account/quota/reset/pool/effort backend hoặc chất lượng full review; help/stand-in không chứng minh dịch vụ thành công. Không tái lập GitHub race thật, MCP publish/PAT/bot/CI/lease hiện hành; không có raw run #513, sáu HINT #518, năm artifact #250/#252 để replay số lịch sử/nhân quả. Không tái lập reboot/PID reuse, Darwin/Windows hoặc runner giữ clone dài ngày. Không chạy doctor xác thực/cài đặt/ghi credential/dọn tạm. Không có HINT-LUOT-5.patch trong gói; chỉ đối chiếu verdict lượt5 như nguồn lịch sử. Không gọi chín cổng là full CI hoặc full runtime selftest.

VERDICT/HINT được tạo ngay sau khi đọc PROMPT, trước phép đo; cập nhật giữa lượt đã giữ tại [nhật ký](evidence/verdict-progress.md).

### va-qua-tay-mat-cong-cu [P2] Con trỏ tooling sinh manifest vẫn dẫn đến phần chỉ có policy và verify

**O01 L458–459, H4 đóng đủ1 thể hiện.** Người cần tìm công cụ sinh manifest được dẫn tới §9 và Quy ước deploy; cả hai có nội dung liên quan nhưng không cung cấp công cụ đã hứa. §10.2 có recipe, CLI release-manifest--help có cờ; đã chạy help0 và sinh manifest tạm0/byte-match. H4 giữ con trỏ policy, bổ sung đích tooling cụ thể. Độ tin cao; không sửa protocol hay manifest thật.

### lenh-khong-noi-hien-vat [P2] Recipe clone dùng RV trước khi cấp đường dẫn

**A01 L223–227/242, H2 đóng đủ1 tuyến.** Trong shell mới chỉ thay các placeholder hiện có, RV rỗng: clone128 và không tạo được working clone. Tệp không có producer cho RV; biến R khác tên và xuất hiện muộn. H2 thêm đầu vào có nhãn trước lần dùng đầu, thử lại clone/checkout/status0. HTTPS fetch dùng stand-in có nhãn; phản chứng lỗi biến không phụ thuộc mạng. Độ tin cao.

### loi-khai-vuot-phep-do [P2] Phép so tên ref được diễn giải thành kiểm mirror nhận đủ nguồn

**E01 L316–321, H3 đóng đủ1 thể hiện.** Cùng tập tên, OID master khác, cả hai non-shallow: mẫu cũ không lộ delta. H3 so tên+OID, ghi rc diff riêng và giới hạn đúng namespace/object; mutant bỏ OID bị oracle bắt. Đây là lỗi phạm vi bằng chứng, không phủ định tác dụng so tập tên của B14. Độ tin cao; không tuyên phép sửa là kiểm toàn vẹn mọi object hoặc GitHub hiện hành.

### neo-sha-tu-head-dong [P2] Hai lệnh lấy head động làm mất liên kết giữa artifact và revision đã review

**T01 L207–212 + T02 L485–491; H1/H5 đóng đủ2 thể hiện.** T01 có thể sinh diff khác revision với numstat; T02 có thể ghi reviewed_sha mới cho verdict cũ khi state đã chuyển sang head mới. Stand-in chỉ thay API đọc; Git và packet_loop thật tái hiện cả hai rc0. Bản sửa dùng OID đã chốt trong artifact, trả5 cho stale SHA và0 cho SHA khớp. Độ tin cao về tuyến dữ liệu; không khai đã gặp race trên dịch vụ thật hoặc đã chứng thực authority của fixture.
