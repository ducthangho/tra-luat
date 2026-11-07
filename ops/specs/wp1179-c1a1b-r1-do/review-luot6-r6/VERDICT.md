# Cross-review wp1179 C1a1b r6 — lượt 6

reviewed_sha: `b439048e4ffe15eed0202b0a91b82be2750041af`
spec_sha256: `a76b3e98761da2f1e589b73aa8b8b11fe8934c84887190582c9d04b1ab7cc7e2`
model/effort tự khai: Codex (GPT-6); tên model chi tiết và effort thực tế không được kênh thực thi cung cấp để xác minh độc lập; không suy từ cấu hình yêu cầu của spec.
provider: `openai_codex`; execution_surface: công cụ shell của phiên Codex; transport: tool calls trực tiếp trong phiên.
verdict: **`changes_requested`**

## Tiến độ và giới hạn

- Đã đọc prompt.snapshot, AGENTS.md; checkout đúng SHA, `git status --short` rỗng, spec 806 dòng và SHA-256 khớp.
- Cây được review chỉ đọc. Mọi probe và evidence mới được ghi trong sandbox; Python dùng `-B`/`PYTHONDONTWRITEBYTECODE=1`.
- Review đặc tả, không khẳng định implementation tương lai đã qua acceptance. Các số lịch sử remote/Windows không có môi trường tương ứng được phân biệt với phép đo lại tại đây.
- Tree của reviewed SHA: `1b327fd650627786d500aaafc335889d573f050b`. Base đo: `889334fb87c25136a13c6776a40a25b401820e04`. Mirror không shallow; `origin/master` tại snapshot: `d26b36f5d2f952c2d952d58517571ffe27c4f826`.
- Đã ghi tệp này từ bước preflight, cập nhật khi có phản chứng, rồi hoàn tất. Mọi số dòng dưới đây thuộc `ops/specs/wp1179-c1a1b-r6.md`, trừ khi ghi khác.
- `gpt-6-astra` / `xhigh` là cấu hình yêu cầu của spec; không dùng nó thay bằng chứng model/effort phục vụ thực tế. Đây là review độc lập có công cụ đo, không tự cấp assurance/land authority.

## ĐỐI CHIẾU LƯỢT TRƯỚC — F13–F15

Nguồn: r5 `268137452ce1d9e21a4cc635eb9ad4ca7358b57d`, verdict tại `ops/specs/wp1179-c1a1b-r1-do/review-luot5-r5/VERDICT.md`.

| Finding cũ | Trạng thái | Bằng chứng |
|---|---|---|
| F13 P2 — `phan-loai-vang-va-khong-do-duoc` | **VÁ SINH LỖI MỚI** | Lỗi trực tiếp gán tree ops C cho G8 đã bỏ. Ba vị trí parser cho đúng G6/G7/G8 trên fixture cô lập subtree; H hỏng/vắng cho G3/G4. Nhưng oracle mới “chỉ luật đích, mọi luật khác giữ màu” bỏ sót OID dùng chung và vòng đời reader: F16. |
| F14 P2 — `dot-bien-tuong-duong-hoac-thieu` | **ĐÃ VÁ THẬT ở tầng đặc tả** | Dòng 530–539/A20b cho disposition tương đương có chứng minh toàn miền và đo trên mã cuối; thêm mutant nhóm t2+t3+t5. Probe producer: bỏ t2 riêng vẫn E_hong với 5 mode đúng và 3 token sai; bỏ cả nhóm thì nhận. Không còn ép 12 witness_killed. |
| F15 P3 — `huong-dan-cli-khong-khop-parser` | **ĐÃ VÁ THẬT ở tầng đặc tả** | §8 dòng 687–689 chỉ nhắc cặp cờ và dẫn §11.2. Invocation đầy đủ rc 0, đọc lại limit 3; thiếu mission/limit 0 rc 2; rescue ID/URL trong đúng state rc 2/0. |

Bằng chứng mới: [graph-review](evidence/graph-review.txt), [conformance](evidence/conformance.txt), [cli-review](evidence/cli-review.txt). F14 được đóng ở tầng đặc tả, không thay audit disposition trên implementation cuối.

## Bảng lớp

| Slug ổn định | Nguồn / finding | Trạng thái, mức mở | Cách vá chung và phép kiểm |
|---|---|---|---|
| `phan-loai-vang-va-khong-do-duoc` | Draft0–2; F4/r1, F6/r2, F11/r4, F13/r5; **F16/r6** | **Mở, P2; 2 biểu hiện mới** | Dùng tập đọc theo OID và trạng thái tài nguyên chung, đối chứng subtree riêng/chung và reader sống/chết. |
| `dot-bien-tuong-duong-hoac-thieu` | F3/r1, F7/r2, F14/r5; kế thừa C1a1a | Đóng ở tầng spec cho biểu hiện đã nêu | Bảng nghĩa vụ, disposition đo thật, assertion đúng tên; nhóm chốt che nhau có ID riêng. A9/A18 giữ guard hạ tầng/child dương. |
| `huong-dan-cli-khong-khop-parser` | F12/r4, F15/r5 | Đóng | Invocation đầy đủ, state-dir nhất quán, cặp âm/dương và readback limit. |
| `mo-rong-module-pha-hop-dong-json-thuan` | Draft0–2; ABI r1 | Không tái mở | JSON module nguyên byte, module mới bọc nguyên dict; đối chiếu blob và chạy suite nền. |
| `predicate-consumer-khong-khop-producer` | F2/r1 | Không tái mở | G6 không đọc leaf; G7/G8 nhận symlink, so OID entry; khai giới hạn provenance. Đã đo các mode. |
| `oracle-trang-thai-g0-mau-thuan` | F8/r2 | Không tái mở | A6 giữ G0 qua khi JSON nhỏ đỏ; quá trần thì G0 đỏ/json null. Đối chiếu JSON thật và ma trận ABI. |
| `dat-lai-ngan-sach-khi-doi-truc` | F1/r1, F9/r3, F10/r4 | Không tái mở | Allowance 3, U_max unknown; counter thật nhận 3/chặn thứ 4, không gọi model. |
| `so-do-ke-thua-chua-do-lai` | F5/r1 | Không tái mở | Đo lại S2–S6 và §11.5 trên exact base; số lượng/bytes khớp. |
| `nguon-duoc-tin-ma-chua-xac-minh` | C1a1a §6; N6/N7 | Không thấy biểu hiện mới | Băm lại object, hai lần đọc ref, khai nguồn API/provenance ngoài scope. Missing/hash/ref drift đo trong scratch. |

Lượt trước có 3 lớp mở, lượt này đóng 2/3 (**66,7%**) ở tầng spec. Không có slug mới; F16 là biểu hiện tiếp của lớp phân loại. Hiện có **1 finding mới / 1 lớp mở / 2 biểu hiện**, mức P2. Tỷ lệ đóng lớp không thay điều kiện dừng: đây là lượt 4/4 của pha spec và vẫn còn finding.

## Findings mới

### F16 — P2 — `phan-loai-vang-va-khong-do-duoc`

**Vị trí:** §0.7 dòng 197–214; §4 dòng 510–516, 541–565; A20 dòng 588 và A20b dòng 589. Đối chiếu §2.3 dòng 318, 335–360 và §2.6 dòng 457–458.

**Nguyên nhân chung:** oracle suy tập luật bị ảnh hưởng từ tên vị trí trong fixture dương, nhưng chưa khóa OID thực tế và phạm vi sự kiện dùng chung. Những câu “chỉ G7”, “mọi luật ngoài tập đích giữ màu” mạnh hơn tiền đề fixture có thể chứng minh. Đây là lỗi acceptance: implementation đọc đúng object có thể bị bộ nghiệm thu bác.

**Biểu hiện 1 — root tree khác nhau không bảo đảm subtree khác OID.** Dòng 516 chỉ buộc A/B/H1 sửa ba tệp khác nhau và ba root tree đôi một khác. Không có guard tree ops A khác tree ops B, nhưng dòng 562 vẫn khẳng định “tree ops của tree(B) hỏng ⇒ chỉ G7”; A20/A20b tiếp tục dùng vị trí để cô lập G6/G7.

Đồ thị phản chứng tuân thủ fixture: A sửa `ops/lease_publish.py` so với MOC thật; B thêm `probe-b.txt` ở root; H1 thêm `probe-h.txt` so với A. S=A, C=B, H=H1, D merge(B,E). Ba root tree khác nhau nhưng cùng tree ops được G6/G7 đọc. Đối chứng dương mọi G qua. Xóa đúng loose object này trong clone scratch, không đổi receipt/commit/ref:

```text
SHARED_ASSERTIONS three_roots_distinct=true
ops_s=23643283e2c95b438173a4b302830b5dd3bef358
ops_c=23643283e2c95b438173a4b302830b5dd3bef358
A20-shared-ops-missing: G6=khong_do_duoc, G7=khong_do_duoc
G0–G5, G8, G9=qua
```

Đây là E_vang thật trên OID dùng chung, không phải mutant “lan lỗi sang luật không đọc object”. Quan hệ phụ thuộc tương tự áp dụng với lỗi hash/parser của object dùng chung. Dòng 564 yêu cầu lập lại bảng khi đổi graph không cứu ca này: phép xóa giữ nguyên graph/ref/receipt. Các dòng tập đọc G6/G7 đúng nếu hiểu theo OID; **ví dụ cô lập chỉ G7 thiếu tiền đề** để suy kết luận đó.

**Biểu hiện 2 — E_git_chet không phải lỗi cục bộ của D.** A20 chọn “framing hỏng ở lần đọc đầu của G1 ⇒ G1”, rồi đòi mọi luật ngoài tập đích giữ màu. §0.7 bỏ sót đường này. E_git_chet ở §2.3 còn gồm tiến trình thoát/đóng ống, và chỉ có **một** tiến trình cat-file. Khi nó chết ở lần đọc đầu, cache trống; G2–G8 còn cần object và sẽ phát sự kiện riêng khi thử đọc, không thể giữ qua chỉ vì không đọc D.

Probe kết thúc đúng tiến trình cat-file của probe trước request đầu G1, rồi tiếp tục G1→G9 theo bảng:

```text
DEAD_READER_RC -9
A20-real-E_git_chet-first-G1:
G1,G2,G3,G4,G5,G6,G7,G8=khong_do_duoc
G0=qua, G9=qua
```

G9 vẫn đọc ref qua tiến trình git riêng. Đối chứng cùng graph, reader sống: mọi G qua. Đây là lỗi reader thật tiêm bằng seam; **không** khẳng định đã đo phục hồi framing của module tương lai. Seam giả header hỏng nhưng giữ reader đã đồng bộ có thể chỉ làm G1 unknown; nếu đó là chủ đích A20, phải khai rõ tính phục hồi, không dùng ca ấy làm oracle chung cho toàn E_git_chet.

**Lệnh / rc / output:**

```text
PYTHONDONTWRITEBYTECODE=1 python -B probes/graph_review.py > evidence/graph-review.txt 2>&1
rc=0
```

[Script](probes/graph_review.py), [log](evidence/graph-review.txt), [graph cùng OID](evidence/graph-shared.json), [trace reader chết](evidence/graph-dead-reader.json). Parser commit/tree lấy nguyên từ producer tại base; reader mẫu băm lại bytes. Không dùng rev-list/merge-base/ls-tree để quyết luật. Mọi ghi/xóa object ở clone tạm trong sandbox.

**Đề xuất cụ thể:**

1. Sửa §4/§0.7/A20/A20b theo một nguồn phụ thuộc: tập `(kiểu mong đợi, OID)` của fixture thật, cộng tài nguyên chung còn cần đọc. Ca dự kiến chỉ G6/chỉ G7 phải có guard object tiêm không trùng OID trong tập đọc luật ngoài đích; ba root khác nhau không thay guard này. Dựng lại tập đọc sau mỗi thay graph.
2. Thêm ca alias có chủ ý: OID subtree chung bị thiếu ⇒ G6/G7 cùng unknown, G8/G4 qua; mutant gán lỗi theo vị trí thay vì OID phải bị assertion bắt. Giữ ca subtree riêng để bắt mutant lan lỗi vô điều kiện.
3. Tách sự kiện object cục bộ với reader/ngân sách dùng chung. Reader chết ở đầu ⇒ G1–G8 unknown, G9 độc lập; chết muộn phải tính cache/luật đã xong. Tách framing phục hồi được khỏi chết/EOF. Chỉ khẳng định luật khác giữ màu khi chứng minh còn đủ dữ liệu.
4. Rà A12/A13/A20 theo quy tắc ấy và bổ sung hai đường bị sót vào §0.7. Giữ nhánh “so OID trước”, scope C1a1b, trần hai tệp/750 dòng.

**Rủi ro khi vá:** đánh dấu mọi G unknown sau lỗi reader sẽ làm sai luật có đủ cache và G9; ép fixture có OID khác nhau rồi bỏ ca alias sẽ che phụ thuộc thật. Guard fixture mới phải có ca âm và disposition riêng, không chỉ assert luôn đúng.

## Bảng tập đọc và độ đầy đủ của §0.7

Đồ thị dương riêng subtree được dựng bằng plumbing trên MOC thật. [graph-isolated.json](evidence/graph-isolated.json) ghi OID và trace đầy đủ. Đây là tập **yêu cầu đọc** theo luật; memo khiến không phải mỗi yêu cầu đều đọc lại từ tiến trình.

| Luật | Tập đọc đo được | Đối chiếu r6 |
|---|---|---|
| G1 | D, B, A; dừng tại OID MOC | Khớp, không đọc MOC. |
| G2 | B; gặp parent S thì dừng | Khớp. |
| G3 / G4 | H1 / H1 | Khớp. |
| G5 | A | Khớp. |
| G6 | A, root tree A, ops tree A | Khớp; không đọc leaf. |
| G7 | B, root tree B, ops tree B, checker blob sau khi mode/OID qua | Khớp. Ops tree có thể chung OID với G6: F16. |
| G8 | B, root tree B, github tree B, workflows tree B, workflow blob sau khi mode/OID qua | Khớp; không đọc ops tree. |
| G9 | Ref origin/master lần cuối | Khớp; độc lập với cat-file. |

Kiểm các ví dụ luật đích trong A12/A13/A20/A20b:

| Ví dụ | Kết quả / giới hạn |
|---|---|
| A12(a) H vắng; A12(b) H băm lệch | Xóa loose H1 thật / thay bytes tại OID H1: G3/G4 unknown, mọi luật khác qua. |
| A13 max_object_bytes | H1 thêm message 300.000 ký tự, cap 250.000, mọi object khác dưới cap: G3/G4 unknown; cap tổng không che. |
| A13 max_tong_bytes | Cap 1 byte: G1 gặp giới hạn đầu tiên, không G nào đỏ vì ngân sách. Không suy các luật sau phải giữ qua. |
| A13 per-walk/deadline | Văn bản phân biệt counter mỗi phép đi với ngân sách chung. Chưa có implementation để nghiệm thu counter/timeout thực; ca phải chỉnh graph/limit để thực sự vượt. |
| A20 commit B/A/H lỗi | Seam object và trace: B ⇒ G1/G2/G7/G8; A ⇒ G1/G5/G6; H1 ⇒ G3/G4. Khớp. |
| A20 ops C có mode tree nhưng object blob | Object thật: chỉ G7 unknown trên fixture cô lập. |
| A20 ops S có mode sai | Object băm đúng ở riêng S: chỉ G6 unknown. Nếu OID dùng chung phải mở rộng tập đích: F16. |
| A20 E_git_chet ở G1 | Oracle chỉ G1 thiếu tiền đề phục hồi; reader chết thật tác động G1–G8: F16. |
| A20b t1–t5, t9, t10 | Chạy riêng cả ba vị trí; t1 có cả thiếu NUL và thiếu byte OID. Khi subtree riêng: chỉ G6/G7/G8 tương ứng unknown, các luật khác qua. |
| A20b c1/c2 | Commit H1 băm đúng thiếu tree / parent sai dạng ⇒ G3/G4 unknown, luật khác qua. |
| A20b t6/t7/t8 | Chỉ đối chiếu nguồn và đường resolve; không tạo payload thoát thư mục. Hướng thử: đặt entry vi phạm đúng từng chốt tên vào tree con đúng vị trí, không checkout. Ví dụ t8 mới chọn ops C phù hợp G7, với tiền đề cô lập OID của F16. |

Danh sách **F13 chưa đủ**: thiếu đồng nhất OID giữa các đường và nhánh E_git_chet dùng chung reader. Quét từ khóa unknown không phát hiện hai điều này. Danh sách **F14** xử lý t2 bằng disposition chung và mutant nhóm; không thấy thêm yêu cầu ép killed trái quan hệ che. **F15** đã phân biệt invocation thật với cặp cờ/lời thuật, không có biểu hiện mới được xác nhận.

Tập parser c1/c2/t1–t10 khớp `KhoObject.commit/tree`: tree cuối sau strip trong header; parent chỉ trong header; hai nhánh t1; năm mode; tên UTF-8, không rỗng, loại tên đặc biệt/trùng. Không thêm chốt hoa thường/thứ tự/author/committer. Lập luận t2 toàn miền: có separator thì điều kiện bỏ đi vốn false; thiếu separator thì tên rỗng, nên mode sai bị t3 bác, mode đúng bị t5 bác. Bỏ cả nhóm t2+t3+t5 đổi hành vi như log đo.

## Rà toàn bộ r6 và A1–A22

| Phạm vi | Kết quả và giới hạn |
|---|---|
| §2.1, A1 | JSON module nguyên byte base→HEAD, blob `3490ea0ee40081c0eba2d121f5b19a67a021a54b`. Module Git mới nạp theo đường dẫn và bọc nguyên dict giữ ranh giới ABI. |
| A2 | Suite JSON thật: 156/156 ca, 162/162 killed, equivalent 9, unresolved 0. Registry rc 0: 29/29, phản chứng 1070/1070. Write set không cần sửa sổ/thêm test file mới. |
| A3 | Gọi JSON module thật với dương/K1/K2/K4. Giữ nguyên dict/không viết lại K1–K5 có ca và mutant; wrapper sản phẩm chưa có để nghiệm thu. |
| §2.2, A4 | Bốn khóa top-level, bool nghiêm, 10 luật G, do_dac không thời gian; ok iff và công thức byte stdout rõ. Ma trận mô hình nhất quán; serializer/CLI sản phẩm chưa chạy. |
| A5 | Rc 2 preflight → 12 → 13 → 0 nhất quán; mixed do+unknown ra 12. Mô hình đã đo. Tham số sai phải stderr một dòng/stdout rỗng; A5 đòi từng vế §2.5, gồm check-ref-format sau regex. |
| A6 | K1/K2 đỏ nhỏ: G0 qua, G1–G9 không chạy. K3/K4/K5 đỏ không chặn G. Quá trần: G0 đỏ/json null. Không tái mở F8. |
| A7 | C=B/MOC qua, C=P/E/X đỏ đã đo. G1 vẫn phải xác minh tới biên MOC, không trả qua sớm khi gặp C. Cặp hết chuỗi không MOC/object thiếu vẫn có riêng trong spec; chưa chạy lại chuỗi phụ đó lượt này. |
| A8 | Đo S=B,C=A ⇒ G2 đỏ; S=A,H=X ⇒ G3 đỏ. Có strict-ancestor witness, không chỉ nhánh rẽ để giết đảo toán hạng. |
| A9 | Ba root khác đo được; T=tree(S) làm G4 đỏ; tree_S=tree(H) làm G5 đỏ. Guard hạ tầng có fixture âm; không bảo đảm subtree khác: F16. |
| A10 | G6 nhận OID cả năm mode với leaf vắng vì không đọc leaf. Có entry/null đỏ; vắng/null qua; vắng/hex đỏ. Ancestor không-tree là do, khác object theo cạnh tree mà sai type. |
| A11 | Đo G7/G8: 100644/100755/120000 qua, 160000/40000 đỏ. OID lệch × missing/sai type ⇒ do; khớp ⇒ unknown. Giữ F6 so OID trước. G8 hash nội dung entry, symlink là chuỗi đích; không chứng minh GitHub nạp symlink. |
| A12 | Missing/hash mismatch H đo mới. Reader mẫu lọc GIT_* và tắt replace; không khai đã chạy lại cặp mutant env/replace của implementation. Không suy entry vắng từ object chưa xác minh. |
| §2.5, A14 | N6 đầu sai caller/ref ⇒ rc 2, cuối drift ⇒ G9 unknown/rc 13. Ref đổi/xóa thật đã đo. Nguồn tham số qua API vẫn là hợp đồng caller, không do module chứng minh. |
| §2.6, A13 | Cap per-walk/object/total/deadline/receipt có đơn vị riêng. Object cap/total/memo đo được: 12 OID phân biệt, 134.354 byte, một lần/object. Deadline thực/pipe treo/RSS/cold-cache/Windows/biên G0 trên implementation: not_run. Clock seam không chứng minh timeout I/O thực. |
| §3, A15 | Write set hai tệp; JSON/sổ/producer ngoài scope, trần 750 dòng giữ nguyên. ~710 là ước lịch sử có khai, không là numstat ứng viên. Vượt trần dừng, không bỏ ca. |
| A16 | Windows required theo M3; base/candidate cùng máy/cùng lệnh, skip không tính đạt. Vẫn cần danh sách test ID+kết quả theo M3 ngoài số tổng. Lượt tập trung không miễn Windows CI. Windows: not_run. |
| A17 | Chạm .claude/dev kích M9: full_mutant_audit Ubuntu hoặc waiver đúng scope còn bắt buộc; JSON suite không thay CI. Gate sản phẩm: not_run. |
| A18 | Setup đủ suite/hai module/registry nguyên byte, gốc kho/MOC tường minh; child dương trước tiêm, tránh đệ quy, lỗi đúng import Git; N_git/M_git=0 riêng. Không thấy tái mở F7 trong spec; e2e ứng viên chưa có để chạy. |
| A19 | doctrine-scan rc 0: 10 tệp/0 vi phạm; adr-song rc 0: 64/64; diff --check thay đổi r6 rc 0. Ruff hai tệp ứng viên: not_run, không khai Ruff passed. |
| A20 | ID luật×E/không-E giữ nguyên; target/non-target còn F16. Vắng entry đã xác minh là kết quả đo, không là object missing. |
| A20b | F14 disposition đã sửa; nhánh G8 của F13 sửa nhưng còn thiếu tiền đề OID/phạm vi sự kiện: F16. |
| A21 | Allowance=3 không suy từ U_lower 8/14/15; U_max unknown. Counter thật readback 3; call 1–3 rc 0, call 4 rc 3, không gọi model. |
| A22 | Init/status/record-codex-call/record-rescue chạy parser thật trong state-dir scratch. Holder --help xác nhận positional path/flags, không đo holder live. Gate tương lai không bị khai đã chạy. |

N1–N8 đều có nơi chiếu. N4 được đáp ứng ở hợp đồng bằng đọc/băm/parse commit/tree trước khi suy entry vắng, không quay lại suy nghĩa từ rc 128. N7/§5/§6 giữ giới hạn ok chỉ nhất quán với C tự khai; C1a2/C1b/T2/Q17, #656/#564/#499, producer/registry và #1160 vẫn ngoài phạm vi.

## §8/§11 với ADR-0043/0052/0055 và protocol §12

Lời gọi, vòng hợp lệ và attempt vẫn là ba trục độc lập. Nâng call 10→16 không nâng hai trục kia. Q-NT/allowance 4/3 được giữ theo chỉ thị user và spec, không giả đã kiểm live comment GitHub. U_max unknown không có nhánh vận hành nào gán số; status/journal chỉ nâng cận dưới. Allowance 3 là ngoại lệ có khai, không chứng minh U+3 ≤16, phù hợp phân biệt allowance với lịch sử chưa đo đủ ở protocol §12.

Ba opt-in ADR-0055/0053/0060 mỗi loại một dòng, đo có file ở L rc 0/vắng L^1 rc 128/L thuộc first-parent snapshot. Không thay freshness trước lease. Trần kích thước Q-KT giữ nguyên. Lượt spec cuối này chưa sạch thì phải dừng/trình chủ kho, không gọi thêm review hoặc chuyển thi công.

Init đầy đủ không reset U; state chỉ đếm pha. Probe tạo trạng thái reviewing nhân tạo **trong sandbox** để thử parser/counter; call thứ 4 tự đưa vào blocked/rescue_required. Rescue revision rc 0 vẫn blocked, không phải đã mở lại pha. Không giả replay lease/journal production; đường phục hồi lịch sử vẫn unknown như §11.2 khai.

Human audit exact head trước merge vẫn bắt buộc; Q-NT chỉ thay cách đóng băng spec. M1/M3/M9/M12/connector draft giữ nguyên. Các đoạn Q-R/hai call cũ là lịch sử, không tự cấp call mới. Không có điều khoản cho phép ok/verdict tự tạo quyền land.

## Đo lại số liệu

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python -B probes/setup_metrics.py > evidence-setup.txt 2>&1`, rc **0**. [Log](evidence-setup.txt) có command/rc/output lệnh con. Môi trường: Linux 6.18.44-fc-v242, Python **3.13.18**, git **2.43.0**.

| Đại lượng | Kết quả đo | Đối chiếu |
|---|---|---|
| S2 first-parent MOC^..base | 411 | Khớp. |
| S2 reader tới MOC | 410 commit / 531.751 byte / 0,027 s | Khớp số object/bytes; không đọc MOC. |
| S3 mọi tổ tiên base | 5.444 / 8.480.418 byte / 0,397 s | Khớp số lượng/bytes; thời gian chỉ máy/cache lượt này. |
| S4 | First-parent 1.084; ngoài first-parent 4.360; log checker 64, giao 64 | Khớp. |
| S5 MOC→base | 2 tệp +650/−93: workflow +1/−1, producer +649/−92 | Khớp. |
| S6 | 156/156 ca; 162/162 killed; equivalent 9; unresolved 0; rc 0; 12,539 s | [Output](evidence/json-baseline.txt), khớp. |
| Suite nền | 535 dòng | Khớp. |
| Tỷ lệ §2.6 | 50.000/5.444 ≈9,184; ngoại suy ≈77,89 MB | Là ngoại suy master, không đo H ngoài master/RSS. |
| §11.5 base→08bcb51f | 1 tệp .githooks/eol_policy_test.py, +698/−92 | Khớp. |
| Base→reviewed SHA, tập code/phụ thuộc trong log | 0 delta | JSON/suite/registry/producer/packet_loop và nguồn hợp đồng đã kiểm không đổi. |
| Hash spec/verdict | Tính lại r1–r6 và verdict lượt 1–5 | Các băm trích r6 khớp; [hash đầy đủ](evidence/final-checks.txt). |
| Opt-in ADR | 0/128, nằm trên first-parent snapshot | Khớp. |

Không đo mới: S7 receipt thật S≠C, S8 Windows/WSL, 776 refs từ lần fetch cũ, holder/lease live, quota/reservation, journal dispatcher cũ, nguồn comment GitHub, cold-cache, GitHub workflow symlink. Không lấy số lịch sử làm readback hiện tại. Gate cần implementation chưa có ghi not_run, không coi việc chưa thi công là finding mới của spec.

## Hồ sơ chạy và bảo toàn cây

Các lệnh dưới chạy từ sandbox với `PYTHONDONTWRITEBYTECODE=1`:

| Command | Rc cuối | Output |
|---|---:|---|
| `python -B probes/setup_metrics.py` | 0 | [metrics/registry](evidence-setup.txt) |
| `python -B probes/graph_review.py` | 0 | [graph/parser/F14/F16](evidence/graph-review.txt) |
| `python -B probes/conformance.py` | 0 | [G/ABI mô hình/N6/budget](evidence/conformance.txt) |
| `python -B probes/cli_review.py` | 0 | [CLI/counter/gate](evidence/cli-review.txt) |
| `python -B probes/final_checks.py` | 0 | [hash/snapshot](evidence/final-checks.txt) |

Rc âm 2/3/128 của lệnh con là phản chứng có chủ ý, không đổi thành product pass. Có hai lần dựng probe rc 1 được giữ log: `graph-review-initial-setup-error.txt` (loose object Git mode chỉ đọc; sửa bằng unlink/tạo lại **trong scratch**) và `graph-review-empty-object-not-fatal.txt` (giả thuyết empty loose object làm cat-file chết bị bác: thực tế trả missing). Phản chứng reader chết cuối dùng kill seam rõ ràng, không dùng hai lần hỏng đó. Bản trước cleanup có cảnh báo BrokenPipe khi destructor; bản cuối đóng pipe có xử lý, log sạch và rc 0.

[Manifest SHA-256 probe](evidence/probe-manifest.sha256). Không tạo payload thoát thư mục/checkout tree hỏng; không gọi thêm model/connector, cấp lease, push, merge hay land. Đã đọc skill cloud-environment-runtime; không có tool environment_status, không suy readiness mạng và không sử dụng mạng.

[Snapshot đầu](evidence/snapshot-start.json) và [cuối](evidence/snapshot-end.json) bằng nhau: HEAD/tree, index hash, diff staged/unstaged, status tracked/untracked/ignored, SHA-256 nội dung **12.854 tệp**. Symlink băm chuỗi đích. Snapshot không gồm toàn bộ .git/objects và không chứng minh mọi thời điểm trung gian; nó chứng minh không có delta ở hai mốc. Clone/source copy/state/probe/output mới đều ở sandbox; không sửa repository review.

**Kết luận:** chưa đủ điều kiện approve/đóng băng r6. Còn F16 P2; F14/F15 đã sửa ở tầng spec. Q-NT: lượt cuối còn finding ⇒ dừng vòng review và trình chủ kho quyết định tiếp theo.

TONG: P1=0 P2=1 P3=0
