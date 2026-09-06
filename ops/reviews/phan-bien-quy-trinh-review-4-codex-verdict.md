# Review độc lập lượt 4 — PR #452

**Kết luận: `changes_requested`.** Bản 4 sửa đúng số mới ở §0 nhưng chưa sửa hết khuyến nghị dựa vào số cũ. Tài liệu hiện hữu ích như hồ sơ phản biện, **chưa dùng được như bản quyết định build/review trong 5 phút**. Có **1 finding P1 và 4 finding P2** dưới đây; hai finding về test là lỗi có sẵn ngoài diff, được đo theo H2, không phải hồi quy do PR này.

## Mỏ neo, authority và môi trường

- `reviewed_sha`: `2fb43fc8e3fd6dacd6bb9e42731e751d3de2e262`.
- `reviewed_tree`: `eb3c5a256e3597e750ddd253db88e63419e8a531`.
- Base bảng §0 / diff PR: `c03a409afc17ee3b8287cd1a88b0ed3f9ba02fab`.
- Revision trước: `76318fa106019611fbd5ea9ec6e2553bb7773faf`.
- SHA-256 tài liệu được review: `0540c5b58d76936136d263f816949d3740f829d34e83d964a20757eeb08d3e36`.
- Authority: yêu cầu trực tiếp của người dùng và **toàn bộ** `prompt.snapshot` lượt 4; SHA-256 prompt `1c226c017450f101331d79939639c99b61751f428ba7fed84fc5ae009d93f89f`. Đây là review ad-hoc theo chỉ thị đó; không tự tạo Packet, spec hash hay lease/generation. Phạm vi docs-only `routine`, người dùng chỉ định reviewer Codex và các probes cổng.
- Vai trò reviewer; provider `openai_codex`; model GPT-6/Codex theo danh tính phiên; execution surface **Codex service qua API, công cụ shell**; transport `machine`. Không phải ChatGPT Web. Không có receipt độc lập xác minh model/session của lượt này; không tự cấp land authority.
- Clone rời, detached đúng SHA, sạch khi bắt đầu, `shallow=false`, 1684 commit. Remote `https://github.com/ducthangho/tra-luat`. Đọc nguồn; chỉ ghi báo cáo `VERDICT.md`. Mọi đột biến ở `/tmp/rv4-*`; clone chạy test `/tmp/rv4-review-clone`, ghim `core.abbrev=7`.
- Bản vá **đã nằm trong commit được giao**, chưa nằm trong `origin/master` **cục bộ**: ref này vẫn là base `c03a409…`; `git merge-base --is-ancestor HEAD origin/master` trả **1**. Không readback GitHub nên trạng thái LAND thật **KHÔNG ĐO ĐƯỢC**, không suy từ ref cục bộ.
- Linux x86_64; Python 3.11.15; PyYAML 6.0.1; actionlint 1.7.7; không có shellcheck trên PATH; thiếu jsonschema. Không đọc credential, gọi LIVE, commit, push, merge hay deploy.

## ĐỐI CHIẾU LƯỢT TRƯỚC / H1

| Finding lượt 3 | Kết quả tự kiểm trên bản 4 |
|---|---|
| **N1** — 50/82 không phải đặc tả đóng băng | **VÁ HỜ**: §0 đổi đúng thành 44 trường băm không rỗng; §2:162, §5:444 và MVP-2:466–469 vẫn 61% / 40 lease “đang làm đúng”. R4-01. |
| **N2** — không có `nang_tran` không chứng minh giữ trần | **VÁ HỜ**: §1 rút 81/82 và 61–99%, thêm ô chưa đủ bằng chứng. Nhưng dòng 128 vẫn “Chỉ ô thứ ba là việc”, phủ định phần bổ sung ngay trước nó. R4-02. Không thấy câu 81/82 còn được dùng như kết luận hiện hành ở §1; các lần còn lại ở §9 là lịch sử, cần gắn rõ trạng thái đã bác. |

Đọc YAML từ **hai Git snapshot**, không đếm lời nhắc trong văn xuôi:

| Đại lượng | Base `c03a409` | HEAD bản 4 |
|---|---:|---:|
| Lease | 82 | 82 |
| Có ≥1 trường băm không rỗng trong ba tên | 44 | 44 |
| Có ≥1 khóa trong bốn tên, kể cả locator/null | 50 | 50 |
| Limit thiếu / =2 / >2 | 41 / 23 / 18 | 41 / 23 / 18 |
| Trong nhóm >2, thiếu `nang_tran` | 17/18 | 17/18 |
| Tự khai `review_rounds_used_truoc_luot_nay >2` | 6 | 6 |
| Receipt | 57 | 60 |
| Receipt có khóa `review_rounds_used`, kể cả lồng | 4 | 4 |
| Receipt có khóa `codex_review_calls_used` | 0 | 0 |

**Số mới đúng trong phạm vi khai báo.** Đột biến bản dữ liệu trong bộ nhớ: cho cả 82 lease khai `nang_tran` ⇒ số “>2 thiếu nâng trần” đổi **17→0**, còn limit/used giữ nguyên. Xóa ba trường băm ⇒ **44→0**, trong khi union khóa vẫn **48** vì locator. Hai phép đếm sửa có độ nhạy với dữ liệu; chúng không tự chứng minh authority. Câu “chưa đủ bằng chứng” có thể đúng ở cả hai thế giới: đó là giới hạn nhận thức hợp lệ, không phải một phép đo tỷ lệ cần phải đổi màu.

**Quét cả lớp:** đã đọc đủ 640 dòng, tìm các lời khai về có/thiếu trường, tuân/vi phạm, có/không cổng và kiểm các phép đếm chúng viện dẫn. Ngoài N1/N2, các lỗi cũ **vẫn còn**: §0/§3 F6 ghi 10/57 và 2/57 thay vì 4/57 và 0/57; M6 ghi `assurance` 31/57 nhưng khóa top-level thật có **19/57**. `cross_provider` có 40 khóa, gồm **29 true + 11 false**, không phải 40 review khác nền. Đây là A1 lượt 2 đã nêu, không nhận làm finding mới. Ngược lại, **52/57 thuộc enum verdict canon** là phép đếm membership hợp lệ; nó chỉ không chứng minh receipt hợp schema/authority. `_kiem_lop_review` thực sự nhận **13/13** lease v2: chỉ chứng minh phép kiểm lớp ấy nhận các khai báo, không chứng minh toàn bộ lease tuân protocol.

Lệnh đã chạy: `python -B /tmp/rv4-measure.py` → **rc=0**; log `/tmp/rv4-measure.log`. Script lấy dữ liệu bằng `git ls-tree` + `git show` tại từng ref. Số lịch sử 57 không bị coi là lỗi chỉ vì HEAD có thêm receipt.

## R4-01 — P2: N1 chưa được truyền tới quyết định MVP-2

**Vị trí:** `ops/PHAN_BIEN_QUY_TRINH_BUILD_REVIEW_20260905.md:162`, `:444`, `:466–469`; đối chiếu `:31–33` và `:49–50`.

§0 nói 44 có trường băm và chưa chứng minh tuân; phần người dùng sẽ làm theo vẫn khẳng định bốn tên cùng một khái niệm, 61% đã neo và 40/82 đang làm đúng bằng tên khác. Sáu lease locator-only/null mà N1 bác vẫn nằm trong luận cứ “bắt oan”. Không thể chữa chỉ bằng đổi 40 thành 34: **có giá trị băm** vẫn chưa là **đã xác minh băm và authority**.

**Hậu quả:** chủ kho ưu tiên chuẩn hóa tên trước việc thiếu đặc tả đóng băng, dựa vào số lease “làm đúng” chưa đo được.

**Đề nghị:** sửa phần quyết định §2/§5, tách locator, định danh byte và định danh đã xác minh; bỏ tỷ lệ “đang làm đúng” chưa có bằng chứng. §9 giữ lịch sử nhưng gắn kết quả đã bị N1 bác ngay hàng liên quan. Không sửa lease lịch sử hoặc verdict cũ. Ca khóa: ba bản thảo + ba locator null không được phân loại đã đóng băng; alias băm hợp lệ không bị loại chỉ vì khác tên. Nguy cơ bản vá: kết tội alias, kiểm băm sai revision hoặc tiếp tục thay một tỷ lệ giả bằng tỷ lệ giả khác.

**Tái hiện:**

```bash
rg -n '61%|40/82|44/82|50/82' ops/PHAN_BIEN_QUY_TRINH_BUILD_REVIEW_20260905.md
python -B /tmp/rv4-measure.py
```

Cả hai lệnh **rc=0**; output phân biệt 44 trường băm với union 50, trong khi MVP vẫn dùng union như tuân thủ.

## R4-02 — P1 / H3: Bản quyết định không có một kết luận hiện hành nhất quán

**Vị trí:** tài liệu `:115–129`, `:183–226`, `:436–491`, `:497–510`.

Đây không phải finding vì “dài”. Các chỉ dẫn hành động **mâu thuẫn trực tiếp**:

- Dòng 125–126 thêm việc kiểm độ phủ/răng và không loại luật chỉ vì có cổng; dòng 128 vẫn **chỉ ô vi phạm đo được là việc**. Thiếu dữ liệu tiếp tục bị biến thành lý do không làm gì.
- MVP-4 tự gọi việc số một; MVP-1 được §6 gọi đứng trước mọi việc; cuối MVP lại hoãn mọi mục còn lại tới khi MVP-1 cho số. Không có một thứ tự duy nhất để triển khai.
- MVP-2 vẫn dựa trên N1 chưa vá; F1 giữ luận cứ CI “dồi dào” rồi rút ở đoạn sau. 9(a)/(b) vẫn dùng “mạnh nhất đã biết”/“đã chữa”, trong khi §6 rút bằng chứng PR #250 và quan hệ nhân quả đó.

Tôi đã đọc cả 640 dòng; kết luận ngắn bắt đầu dòng 59, MVP ở dòng 448. **Chưa đo thời gian đọc của chủ kho hoặc thử nghiệm người dùng 5 phút**. Nhận định biên tập của tôi: người chỉ đọc phần kết luận/MVP sẽ gặp quyết định sai hoặc không biết câu nào còn hiệu lực. Tệp còn giá trị làm hồ sơ bằng chứng, nhưng chưa đạt mục tiêu giúp quyết định quy trình.

**Hậu quả:** hoãn việc đo/chữa cổng chưa kiểm được, hoặc thi công theo một “số một” tùy đoạn đọc; thêm vòng sửa tài liệu mà không có quyết định mới.

**Đề nghị cắt/sắp lại:** một trang đầu chỉ chứa quyết định hiện hành, bằng chứng, giới hạn và thứ tự bước tiếp; đưa §9 cùng các đoạn “bản đầu viết/rút lại” sang phụ lục hoặc dẫn tới verdict đã lưu. Git đã giữ các bản cũ; không cần lặp nguyên câu sai trong phần khuyến nghị. Không xóa verdict/receipt gốc.

**Kết luận/MVP còn đứng được đến đâu:** giữ thử nghiệm tìm theo lớp lỗi, phản chứng regression và cấp năng lực đo như các bước có thể kiểm; giữ nguyên required gate trong lúc chưa có evidence cho thay đổi. Mô tả việc đo thời gian/vòng và Windows là **thử nghiệm để ra quyết định**, không là lợi ích đã chứng minh. MVP-2 cần định nghĩa lại đối tượng như R4-01; thứ tự MVP-1/MVP-4 chưa được phép đo hiện có chứng minh. Tài liệu chưa đủ căn cứ để bác trọn đề xuất gốc, mà nguyên bản 13 mục/10 câu hỏi cũng chưa có trong diff được giao.

**Ca khóa và rủi ro sửa:** đọc riêng trang quyết định phải lấy được cùng một thứ tự và cùng trạng thái của N1/N2 như phần evidence; tìm lại các câu đã rút trong phần hiện hành phải ra 0. Đây là kiểm tính nhất quán, không dùng grep để chứng minh quyết định đúng. Rủi ro: cắt mất điều kiện áp dụng hoặc biến “chưa đo” thành một lý do hoãn vô thời hạn; giữ đúng một bước đo hữu hạn cho mỗi quyết định còn thiếu evidence.

**Tái hiện, rc=0:**

```bash
sed -n '115,129p' ops/PHAN_BIEN_QUY_TRINH_BUILD_REVIEW_20260905.md
sed -n '436,510p' ops/PHAN_BIEN_QUY_TRINH_BUILD_REVIEW_20260905.md
```

## R4-03 — P2: Kết luận mới về điểm mù provider dùng sai quần thể đã tiếp xúc

**Vị trí:** tài liệu `:621–640`; cùng lời khai ở phần đầu receipt lượt 3.

“Bốn reviewer cùng nền đọc qua câu 61–99%” không khớp lịch sử. Câu ấy **không có** tại `07eb236` và `ba76a78`, hai SHA được verdict lượt 1/2 review; nó được thêm ở `d3bc218fe57eb467834fcaa36a02f68a5beec546` sau đó. Verdict lượt 2 B3 thực sự **đề xuất phép suy sai 50/82 và 81/82**: đó là bằng chứng một phân tích đã sinh lỗi, không phải bốn reviewer cùng bỏ sót câu chưa tồn tại. Verdict Codex lượt 3 ngay đầu cũng đã loại trừ suy luận nhân quả, khác revision và thiếu transcript đầy đủ.

**Hậu quả:** chủ kho phân bổ quota/chọn provider dựa trên một “4 so 1” không có cùng đầu vào. Caveat n=1 ở cuối không cứu được lời khẳng định “điểm mù có hệ thống” và “không còn suy đoán” phía trên.

**Đề nghị:** ở §9 và phần diễn giải receipt, chỉ ghi chuỗi sự kiện có thể kiểm: lượt 2 B3 đưa ra phép suy; tác giả đưa vào bản 3; lượt 3 Codex bác bằng phản chứng. Không suy tỷ lệ bỏ sót hay quan hệ nhân quả provider. Giữ nguyên luật cross-review hiện hành; finding này không bác luật đó. Ca khóa: đối chiếu **đúng reviewed SHA** của từng reviewer với câu được nói là họ đã đọc; so sánh provider nếu cần phải cùng bundle, cùng nhiệm vụ, giữ cả thất bại/không kết luận. Rủi ro: sửa quá tay thành “khác nền không có giá trị”, cũng vượt dữ liệu.

**Tái hiện, rc=0:** `python -B /tmp/rv4-measure.py` in `phrase_61_99`: **False, False, True** cho `07eb236`, `ba76a78`, `d3bc218`. Đọc kèm `ops/reviews/phan-bien-quy-trinh-review-2-claude-verdict.md` B3 và sáu dòng đầu verdict lượt 3.

## R4-04 — P2 / H2: `cong_cu` cấp tín dụng giết mutant cho lỗi ngoài assertion đích

**Vị trí:** `ops/cong_cu_test.py:300–310`, `:423–426`, `:453–464`, `:843–857`; đường chết ở `ops/cong_cu.py:222`.

Mutant có sẵn `t13_mat_requiredness_khi_tool_bien_mat` bỏ metadata `chinh_sach`. Tiến trình con chết **rc=1, stdout rỗng, `KeyError: 'chinh_sach'`** tại aggregator. `t13` chết tiếp bằng **JSONDecodeError** khi đọc stdout, **chưa đến assertion** về tổng `KHONG_DO_DUOC`. `_chay_1_ca` gom mọi Exception thành `chet`; runner vẫn in:

```text
ok t13_mat_requiredness_khi_tool_bien_mat → giết đúng 't13_actionlint_bien_mat_giua_probe_va_canary' · bán kính 1/23
```

Đây là tín dụng giả đo được, không suy đoán từ `rc!=0`. Control `t13` đạt trong suite. Đổi riêng kết quả nhánh mất executable sang DAT **nhưng giữ metadata** trên bản sao ⇒ JSON hợp lệ, rc=0, tổng DAT và **AssertionError đúng đích** “canary mất executable bị nuốt”. Tức ca có thể có răng; **mutant và bộ chấm hiện tại không chứng minh đúng răng ấy**.

**Hậu quả:** báo cáo độ phủ đột biến đánh đồng crash với kiểm trạng thái; chủ kho tin cổng công cụ đã được thử đúng lớp fail-open. Đây là mã có sẵn, không do diff PR #452.

**Đề nghị:** sửa mutant để giữ đầu vào không liên quan và phá đúng trạng thái; phân biệt assertion nghiệp vụ có tên ca với lỗi dựng fixture/parse/crash. Giữ stderr của child. Đặt ca tự kiểm bộ phân hạng với JSONDecodeError/KeyError và wrapper đổi exception; chúng phải thành tín dụng giả, không được `chet` hợp lệ. Nguy cơ: chỉ tìm chuỗi “AssertionError” hoặc đổi mọi lỗi thành AssertionError sẽ tái tạo đúng lớp đã ghi trong CLAUDE.md; không phải mọi crash đều vô nghĩa, nhưng phải được phân loại riêng.

**Tái hiện tối thiểu bằng mutant/fixture có sẵn** (chạy trên clone tạm):

```bash
python -B - <<'PY'
import sys
sys.path.insert(0, 'ops')
import cong_cu_test as t
name = 't13_mat_requiredness_khi_tool_bien_mat'
results, target = t._do_ban_kinh(name)
print(target, results[target])
PY
```

Lệnh **rc=0**, kết quả `('chet', 'JSONDecodeError: ...')`. Bằng chứng stderr và phép đối chứng ngữ nghĩa: `python -B /tmp/rv4-findings-probe.py`, `python -B /tmp/rv4-confirm.py` đều **rc=0** (script ghi kết quả, không có nghĩa mutant đạt); logs cùng tên `.log`.

## R4-05 — P2 / H2: Ba ca comment-id đang đo chốt head-sha thay vì sổ comment

**Vị trí:** `.claude/dev/packet_loop_test.py:995–1004`, `:1033–1052`; thứ tự chốt ở `packet_loop.py:1128–1133`.

Ba ca `comment_id_chua_dang_ky_bi_tu_choi`, `comment_id_sai_transition_bi_tu_choi`, `thieu_comment_id_chan_transition` đều chuyển sang reviewing **không cấp `--head-sha`**. Lệnh đã trả RC_TRACE=5 vì thiếu head, trước khi `_tieu_thu_comment_id` chạy. Assertion chỉ so mã 5 nên cả ba xanh.

Trên bản sao, thay đúng lời gọi `so = _tieu_thu_comment_id(...)` bằng `so = {}` ⇒ **cả ba vẫn xanh**. Ca tái sử dụng ID **đỏ**, chứng minh không được gọi toàn cổng mất răng. Cấp head hợp lệ cho đúng ba fixture đó, không đổi comment đầu vào ⇒ control **3/3 đạt**, mutant làm **3/3 đỏ đúng assertion**. Replay ca thiếu comment có head: control **rc=5**, stderr “thiếu --comment-id”, state `running`; mutant **rc=0**, state `reviewing`.

**Hậu quả:** bộ test báo đã bảo vệ ba thuộc tính sổ comment trong khi chúng cùng được “bảo vệ” bởi một đầu vào thiếu khác. Hồi quy từng nhánh có thể không được các ca mang tên ấy phát hiện. Không tuyên bố đã chứng minh bypass trên mã nguyên trạng hoặc mọi ca liên quan đều yếu.

**Đề nghị:** sửa fixture ba ca tại nơi dựng lời gọi, hoàn tất các tiền điều kiện không phải đích; đòi lý do từ chối đúng lớp và state không đổi. Mỗi thuộc tính thiếu/chưa đăng ký/sai transition cần mutant riêng, đối chứng hợp lệ đi qua; ca dùng lại hiện có giữ riêng. Rủi ro: thêm head rồi vẫn để một tiền điều kiện khác sai, hoặc assert nguyên văn cả stderr gây giòn; neo lý do/nhánh có nghĩa và state.

**Tái hiện:** `python -B /tmp/rv4-findings-probe.py` và `python -B /tmp/rv4-confirm.py`, **rc=0**. Script chỉ tái sử dụng ca đã có, đột biến nguồn trong thư mục tạm và bổ sung head hợp lệ cho phép đối chứng; không sửa test trong clone review. Log ghi đủ control, mutant, stderr/state.

## H2 — Phần sạch và giới hạn của phép mở rộng

| Nhóm | Đã nhìn/đã chạy | Kết luận giới hạn |
|---|---|---|
| `RC_TRAN=3` | Hai mutant có sẵn nới attempt và same-failure; control đều đạt; đích kỳ vọng 3 nhận 0 | Sạch ở hai phép này |
| `RC_PROVIDER=4`, `RC_TRACE=5`, `RC_GUARD=7`, `RC_STATE=8` | Đổi riêng mã sang 0 trên bản sao, chạy ca tương ứng; đọc stderr và đường gọi | Xác nhận răng **mã thoát** ở review sai provider, SHA sai, guard, cấm accepted qua transition; không phải chứng minh mọi bất biến state/authority. Ca init cùng provider bị fixture chuyển thành rc=8, không nhận làm bằng chứng đúng đích; ca thiếu comment dẫn tới R4-05 |
| `adr-song`, RC9 | **19 mutant có sẵn / 48 cặp control–mutant**; mọi control đạt; đọc traceback/assertion từng ca | Sạch: đích đỏ vì thiếu/trùng dòng, metadata không render, sai tên, bắt oan và các thuộc tính đã nêu; không dùng số bằng nhau như chứng minh hiệu lực ADR |
| `doi-chieu-uy-quyen` | 3 mutant: bỏ first-parent; nhận merge OID thay head; coi sổ vắng là sổ rỗng | Cả ba đỏ đúng assertion; control đạt. Đây là đo khai báo, không phải cổng duyệt authority |
| `nhanh_don_duoc` | Suite **8/8**, 10 mutant; đọc lại traceback của **14 cặp mutant–ca** | Sạch trong mẫu; assertion đúng nhóm A/B/C, lệnh in hoặc giới hạn. Cô lập config Git trước chạy |
| `cong_cu` | 23 ca, 18 mutant; xem từng lỗi đích | **16 mutant đúng assertion, 1 tín dụng giả (R4-04), 1 KHÔNG ĐO ĐƯỢC (`t2`, thiếu jsonschema)**. Không gọi 17 nhãn `ok` của runner là 17 giết thật |
| Lease publish ngoài sáu probes cũ | Toàn suite **121/121, bỏ qua=0**, gồm các ca còn lại và các bẫy mutation nội bộ | Baseline đạt. Không kiểm nội dung mọi assertion của mọi mutant lồng nên không suy 121 ca đều có răng độc lập |

Log `/tmp/rv4-probes.jsonl`: 28 cấu hình mutation, **59 cặp**, mọi control đạt. **59 AssertionError không có nghĩa 59 tín dụng đúng**: hai ca sai đích/fixture đã loại như bảng trên. Log `/tmp/rv4-extra-probes.jsonl` lưu 18 đích cong_cu và 14 đích nhanh, cả traceback. Script đều ở `/tmp/rv4-*.py`, dùng mã từ clone cùng SHA và thư mục riêng mỗi lần chạy.

## H4 — Tấn công verdict lượt 3

**Sáu phép thử của bảng H3 lượt 3: sạch trong phạm vi đã tái hiện.** Chạy lại ở HEAD bản 4; mã/test cổng không đổi so `76318fa` (`git diff --quiet` các tệp, rc=0):

- t26: thay byte verdict ⇒ **LỆCH BĂM**; t27: bỏ hàng mục lục ⇒ thiếu verdict trong đúng cột; t33: thêm khóa YAML top-level vô hại nhưng không thuộc schema ⇒ actionlint báo **unexpected key** đúng dòng.
- t76: bỏ so lớp ⇒ **reviewer routine lọt chốt**.
- Doctrine/bien-nhan: tắt chốt ⇒ assertion đích kỳ vọng **6/11**, nhận **0**; đối chứng sạch/đủ receipt vẫn đạt.

`python -B /tmp/rv4-h4.py` → **rc=0**; log `/tmp/rv4-h4.jsonl`: **8 control đạt**, **6 mutant đỏ đúng assertion**, **2 đối chứng dưới mutant vẫn đạt**. Không thấy tín dụng giả ở sáu phép này. Không có script/log gốc lượt 3 trong clone để chứng minh byte-exact lần chạy cũ; đây là phép tái hiện độc lập các thao tác đã mô tả.

Lượt 3 **bỏ sót phạm vi test mới** R4-04/R4-05, nhưng đã khai không suy từ sáu cổng ra mọi cổng, nên không quy việc chưa đo thành lời khai sai. Nó cũng đã ghi A1/A2/A5/B5/B6 còn tồn tại; lần này không nhận lại các lỗi đó là phát hiện mới của Codex. Giới hạn đáng giữ của verdict cũ là phân biệt số khai báo với vòng thật và không suy nhân quả provider; bản 4 đã đọc mạnh hơn nguồn ấy (R4-03).

## TÔI ĐÃ ĐO ĐƯỢC GÌ / KHÔNG ĐO ĐƯỢC GÌ

| Lệnh / kiểm tra | Trạng thái và mã thoát thật | Bằng chứng dương / giới hạn |
|---|---|---|
| `git diff --check c03a409 HEAD` | **passed, rc=0** | Không lỗi whitespace trong diff tám tệp |
| `python -B /tmp/rv4-measure.py` | **passed, rc=0** | Hai snapshot, 82 lease; số và đột biến dữ liệu như H1 |
| `python -B .claude/dev/packet_loop_test.py` | **passed, rc=0** | Clone tạm: nền **278/278**, skip=0; **81 mutant**, `TỔNG: ĐẠT`; log `/tmp/rv4-packet-suite.log`. Phân hạng nội bộ không thay kiểm đúng lý do |
| `python -B ops/lease_publish_test.py` | **passed, rc=0** | **121/121**, đã chạy=121, skip=0; `/tmp/rv4-lease-suite.log` |
| `python -B ops/nhanh_don_duoc_test.py`, môi trường ban đầu | **failed, rc=1** | **0/8**; Git signing qua helper ngoài sandbox làm fixture không commit được. Không gọi là hồi quy nguồn |
| Cùng lệnh, `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null GIT_CONFIG_COUNT=0` | **passed, rc=0** | **8/8**, 10 mutant đạt theo runner; 14 assertion đã kiểm riêng; `/tmp/rv4-nhanh-clean.log` |
| `python -B ops/cong_cu_test.py` | **failed, rc=1** | **22/22 chạy đạt**, tổng=23, **skipped=1**; t2/canary chưa đo do thiếu jsonschema. Một mutant khác có tín dụng giả dù được in `ok`. `/tmp/rv4-congcu-suite.log` |
| `python -m pip install --target /tmp/rv4-python-deps jsonschema` | **failed, rc=1** | DNS/network không truy cập được index; không giả công cụ để làm t2 xanh |
| `python -B /tmp/rv4-probes.py`, `rv4-extra-probes.py`, `rv4-h4.py`, `rv4-findings-probe.py`, `rv4-confirm.py` | **completed, rc=0** từng script | Kết quả control/mutant được ghi riêng; rc của script thu thập không phải rc/pass của mutant |
| `python -B scripts/tl.py doc-claims-check --strict` | **passed, rc=0** | `ok=true`, **106 files**, flags=[]; roots mặc định **không có ops**, không kiểm đúng/sai của tài liệu này |

**KHÔNG ĐO ĐƯỢC:** trạng thái PR/LAND/required checks trên GitHub hiện tại, authority của từng ngoại lệ lease, tỷ lệ tuân thủ thật, số vòng không có receipt, billing/CI thực tế, nguyên bản đề xuất 13 mục, transcript bốn reviewer, hiệu ứng nhân quả provider, thời gian đọc 5 phút của người thật, canary t2 trên môi trường đủ jsonschema, Windows/parity Windows–Linux. Không dùng “chưa đo” thay cho sạch hoặc vi phạm.

**not_run:** full runtime selftest, full release gates, Windows, LIVE, merge/deploy; đây là review tài liệu với probes, không phải chứng nhận release. **skipped:** t2 cong_cu như bảng, không tính pass. Các artifact `/tmp` là evidence của phiên, không phải receipt bền trên GitHub; cần giữ cùng verdict nếu muốn tái kiểm sau khi môi trường này hết hạn.

Kiểm cuối: exact HEAD/tree giữ nguyên; tracked diff không đổi; chỉ thêm `VERDICT.md` theo yêu cầu người dùng.

verdict: changes_requested
