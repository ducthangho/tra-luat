Reviewed commit: 97f3bc18a937c251f9ee639279e2ca818bce9a58
Verdict: changes_requested — P0=0 P1=1 P2=4 P3=1

Review độc lập, offline, đếm theo **6 lớp**. Ngưỡng của chủ kho: hết cả P0/P1/P2/P3. Kho nguồn `/home/user/rv812` được đối xử read-only; mọi phép sửa fixture, mutation và chạy suite ở `/tmp`. Không push, merge hay gửi verdict ra dịch vụ ngoài.

**Định danh và phạm vi**

- Base: `4c7c29858220ae575bebc5e0a343842cd3db4546`; tree của head: `127beecdd27d7730255c70bb6ddbdcdddc49b699`; clone không shallow. Head đầu/cuối khớp assignment; worktree nguồn sạch.
- Đặc tả r2: `d64987461d89429ca97230ec5e796bf987bb9383d765279543e6a7fc14513eef`; phần chung: `4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0`. Đã tự đọc bằng `git show` và băm lại, đều khớp. Lease đã đọc: `origin/ops/wp812-spec:ops/leases/wp812-r2-g3-claude.yaml`.
- Reviewer: Codex/OpenAI, họ GPT, độc lập với executor Claude. Môi trường thực đo: Linux, Python 3.13.16, shell qua công cụ `exec_command`, transport thực thi máy cục bộ. Tên model do nền phiên khai là GPT-6; không có telemetry chứng minh model/effort của từng request, không suy identity từ GitHub actor. Không gọi reviewer con.
- Đã đọc diff base→head và `783463b`→head, verdict/REPRO lượt 1, protocol cùng các validator được gọi. Bằng chứng và lệnh: `PREFLIGHT.json`, `SPEC_HASHES.json`, `GATES.json`, `REPRO.py`, `REPRO.jsonl`, `EXTRA_PROBES.py`, `EXTRA.jsonl`, `AUDIT_MUTANTS.py`, `MUTANTS.jsonl`.

**Bảng lớp còn mở**

Trong bảng, `pl` = `.claude/dev/packet_loop.py`, `test` = `.claude/dev/packet_loop_test.py`; số dòng trên exact head.

| slug | hạng | biểu hiện (file:dòng) | phép đo đã chạy | hướng vá |
|---|---|---|---|---|
| `lease-holder-scope-incomplete` | P1 | pl:2453, pl:2466–2469 | `EXTRA.jsonl`: thêm lease khác giữ `x/`, lease ứng viên giữ `x/a.py` vẫn **rc=0, leased**. Lease khác có effective write set chứa `x/a.py` cũng bị bỏ qua, **rc=0**. Chiều bắt oan: write set hợp lệ `planned:x/a.py` lại **rc=7**. | Giữ chốt canon `ai-dang-giu`, nhưng phải đo giao toàn **effective** write set theo protocol §5: chuẩn hóa, prefix hai chiều, và các lease cạnh tranh. Kết quả khớp chuỗi chính xác của validator hiện tại không chứng minh độc quyền đường dẫn. Dạng chưa đo được phải từ chối; không tuyên bố duy nhất từ phép hỏi hẹp. HINT có ba phản chứng. |
| `identity-compared-by-provider-family` | P2 | pl:2413–2414, pl:2512–2525 | `REPRO.jsonl`: receipt đổi executor từ Claude sang Antigravity nhưng khai cùng họ Claude vẫn **rc=0, approved_pending**; executor surface/transport trái lease cũng **rc=0**. Lease dùng bí danh canon `anthropic_claude` hoặc `openai_codex` lại bị `_identity` bác **rc=2**. | Chuẩn hóa identity lease/receipt bằng các hàm của canon, so provider và những trường identity được khai, gồm surface/transport của đúng vai; so họ bằng `model_family` lease, không dùng họ làm đại diện cho toàn identity. Từ chối lời khai mâu thuẫn, nhận bí danh canon hợp lệ. Giữ baseline receipt cũ không khai executor tuple riêng theo hợp đồng validator; khi tuple có mặt phải kiểm nhất quán. HINT có ca executor lệch và bí danh. |
| `lease-checks-worktree` | P2 | pl:2460–2463 | `REPRO.jsonl`: lease thay thế có bia mộ **hai chiều**, cùng tree tại lease OID, qua `lease_publish.kiem` trên checkout Git của OID ấy; `record-lease` lại **rc=7**, validator con **rc=12**, `fatal: not a git repository`. | Dựng snapshot Git cô lập đủ nội dung/ngữ cảnh mà canon đọc, neo lease OID; chỉ chép prompt không đủ. `_kiem_bia_mo` còn quét lease qua refs. Không quay lại kiểm worktree ứng viên. HINT có baseline thay lease hợp lệ. |
| `new-input-schema-incomplete` | P2 | pl:667–670, pl:2413–2414, pl:2451–2461, pl:2512 | `REPRO.jsonl`: `model_family: false`, `[]`, `reviewer_model_family: false`, role không hợp lệ, generation âm, assurance không hợp lệ đều **rc=0, leased**, state đã đổi. `prompt_path: '.'` ném **FileExistsError, rc=1**. Context giữ đủ khóa nhưng `reviewer={}`/`executor=null` vượt `_load`, rồi review ném **KeyError/TypeError, rc=1**. | Kiểm đầy đủ kiểu/miền của đầu vào đường mới trước khi dùng/ghi; phân biệt vắng với falsy sai kiểu; role lease phải đúng executor, generation dương, assurance thuộc miền protocol. Kiểm lược đồ lồng của context ở `_load`, thay vì chỉ tập khóa. Kiểm đường dẫn là tệp và chuyển lỗi I/O thành rc có kiểm soát. Giữ default của đường legacy theo I9. HINT có ca falsy. |
| `required-mutation-coverage-missing` | P2 | test:5985–6015, test:6033–6048, test:6050–6091 | 29/29 ca `r812_*` xanh và 31 mutant khai báo bị giết; nhưng **6 mutant kiểm toán** vẫn qua **29/29**: bỏ `_thieu`, bỏ từng phép đo land-OID, chặn cửa khép ADR-0054 ở trần vòng, và dừng review trước khi kiểm H ở trần. Xem `MUTANTS.jsonl`. | Bổ sung baseline/âm đúng yếu tố cho từng chốt còn thiếu, nhất là H schema và I4/I5 ở trần vòng trên state ADR-0054. Sửa ca “blob không có” đang chỉ đổi digest; thêm ca dependency thật sự vắng. HINT và `HINT_CHECK.jsonl` chứng minh ca bổ sung bắt được hai mutant sống. |
| `temporary-artifacts-not-cleaned` | P3 | pl:2396–2403; các caller pl:2460, pl:2505 | `LEAK.json`: một chuỗi lease→review thành công, **rc=0**, để lại **2** thư mục `pl812-canon-*`, **1,234,346 byte** trong TMPDIR riêng sau khi các tiến trình đã kết thúc. Các đường từ chối cũng không có cleanup. | Bao vòng đời canon/snapshot trong context manager `TemporaryDirectory` hoặc `try/finally`; dọn cả khi `_die` ném `SystemExit`. Việc trả Path từ `_canon` phải đi cùng chủ sở hữu vòng đời rõ ràng. |

Không có P0. P1 ở lớp holder vì máy chấp nhận quyền độc quyền trong khi write set đang giao lease khác; P2 identity vẫn giữ phép so khác họ nhưng chưa giữ đúng identity được lease ủy quyền. Không nâng hạng chỉ vì mô hình tấn công giả định.

**Chi tiết quan trọng của phản chứng**

`lease-holder-scope-incomplete`: ba phép đo đều dùng bare origin cục bộ, lease được commit/push vào origin fixture, workflow comment và H check đầy đủ. Không sửa validator canon để làm xanh. Canon `ops/lease_publish.py::_lease_cham_duong` khớp chuỗi từ `write_set`, không xét prefix hay `effective_write_set`. Caller mới hỏi đúng mỗi chuỗi của lease ứng viên rồi diễn giải `NGƯỜI_GIỮ 1` thành độc quyền toàn write set. Vì vậy đây là lỗi của phép hợp thành mới, dù câu trả lời hẹp của validator là đúng. Đã quét chiều prefix, effective closure và cách viết `planned:`; không chỉ một đường dẫn cụ thể.

`identity-compared-by-provider-family`: ca Antigravity/Gemini hợp lệ của candidate đã xanh, nên lỗi ban đầu “Google không có họ mặc định” đã được vá tại vị từ. Tuy nhiên, phép so giờ chỉ so họ executor; không so provider executor với lease, cũng không xử lý các lời khai executor surface/transport mâu thuẫn. `IDENTITY_AB.py`/`IDENTITY_AB.jsonl` dựng thêm baseline có đủ tuple executor và bằng chứng họ model; baseline qua `_thieu`, `_neo_git`, CLI rồi đổi riêng từng **một trường** provider, surface, transport. Cả ba vẫn rc=0→approved_pending. Chiều bí danh đã được canon lease validator chấp nhận rồi mới bị caller mới bác. Không đòi đổi cách suy assurance theo họ model của ADR-0050.

`lease-checks-worktree`: ca “đặc tả chỉ có ở lease OID, vắng worktree” hiện xanh, đóng đúng biểu hiện cũ. Bản vá chép một tệp prompt vào thư mục `snap` không có `.git`, nên làm hỏng phụ thuộc Git khác của chính validator. Probe mới thêm cặp thay thế/bia mộ hợp lệ; canonical H check trên snapshot Git thật đạt trước khi chạy lệnh sản phẩm. Lease r2 thực của #812 cũng có `thay_the_cho`, nên đây là dạng dữ liệu vận hành có thật. Không coi “từ chối mọi lease thay thế” là fail-closed đúng đặc tả.

`new-input-schema-incomplete`: `required_checks` falsy và slug newline đã bị chặn đúng; lớp vẫn mở ở các trường mới khác. `_identity` là helper legacy có fallback theo truthiness; caller mới dùng nó trên YAML chưa kiểm kiểu đầy đủ. `_load` mới kiểm đúng **tập khóa** context nhưng không kiểm các giá trị lồng, nên vẫn nổ khi context có hình dạng sai. Với các traceback đã đo, byte state giữ nguyên; không gọi chúng là ghi-state-trước-từ-chối. Các ca lease falsy/role/generation sai thực sự ghi state, vi phạm M1/I4.

**ĐỐI CHIẾU LƯỢT TRƯỚC**

Nguồn: verdict và `REPRO.py` tại `origin/ops/wp812-g2-reviews:ops/reviews/wp812-r1-g2-exec-review-1-codex/`, SHA lượt 1 `783463b5d62efbc43c6a6116e32c43accbc485f7`. Giữ bản gốc ở `REPRO_R1.py`; chạy lại phần còn áp dụng trong `REPRO.py` bằng fixture H thật của r2. Đường `accept` không chạy lại trong packet này. Probe doctor ở trần được đặt sau một verdict âm hợp lệ để có cửa mở attempt hợp lệ, tránh đo nhầm lỗi “lượt vẫn mở”.

| lớp lượt 1 còn trong r2 | kết luận | bằng chứng độc lập trên head mới |
|---|---|---|
| `receipt-validation-incomplete` | **ĐÃ VÁ THẬT** trong phạm vi đã đo | Canon có đủ nguồn; baseline `_thieu=[]`, `_neo_git=([],[])`. ChatGPT giả Codex, transport sai, mỏ neo vắng đều rc=11, state nguyên byte. Mutant bỏ `_neo_git` bị giết bởi sai digest. Thiếu test bảo vệ `_thieu` được tính ở lớp coverage, không báo lại thành lỗi sản phẩm đã đóng. |
| `identity-compared-by-provider-family` | **VÁ HỜ** | AG/Gemini đã đạt; identity khác cùng họ vẫn lọt và bí danh canon vẫn bị bác như bảng lớp. |
| `findings-not-receipt-bound` — phần `record-review` | **ĐÃ VÁ THẬT** | Verdict âm không có H bị rc=11; slug ngoài bảng H bị rc=11; verdict âm có slug trong bảng xanh. Predicate nay chạy cho cả verdict dương/âm; mutant chỉ kiểm approve và mutant bỏ membership đều bị giết. Phần connector ở #834, không nhận là đã vá. |
| `stop-validation-order` | **ĐÃ VÁ THẬT** ở các đường đã đo | Bad H tại trần vòng rc=11, state nguyên byte; doctor hỏng tại trần attempt rc=10, byte nguyên. Approve khép lượt tại trần vòng rc=0→approved_pending; verdict âm hợp lệ ghi đủ 2 review, đóng attempt rồi rc=3→blocked/rescue. Same-failure và rescue sau review nay chung helper. Test candidate chưa bảo vệ hết phần này: xem coverage. |
| `lease-checks-worktree` | **VÁ SINH LỖI MỚI** | Vắng đặc tả/prompt ở worktree vẫn nhận; lease thay thế hợp lệ bị snapshot thiếu Git bác. Giữ slug lớp nguồn vì cùng lỗi thiếu ngữ cảnh đầu vào cho H check. |
| `new-input-schema-incomplete` | **VÁ HỜ** | Required-check falsy/slug newline đã đóng; falsy identity, miền role/generation/assurance, path và context lồng còn lỗi. |
| `required-mutation-coverage-missing` | **VÁ HỜ** | Đã có mutant H lease, holder, shallow, anchor và I11; 6 mutant kiểm toán mới còn sống 29/29 và các mục nghiệm thu đo sai như dưới. |

**Đối chiếu `nghiem_thu` r2**

Tên dưới bỏ tiền tố chung `r812_`. “Đạt” là ca đã chạy và mutant khai báo giết ca đích với assertion đúng chốt; không suy từ tên ca. Baseline review chung đã được reviewer kiểm độc lập qua `_thieu` và `_neo_git` canon thật.

| mục bắt buộc | ca tương ứng | đánh giá |
|---|---|---|
| Lease chỉ ref cục bộ | `lease_chi_o_ref_cuc_bo` | Đạt; mutant bỏ ls-remote bị giết. |
| Spec lệch băm, byte nguyên | `dac_ta_lech_bam` | Đạt; mutant bỏ băm và ghi sớm đều bị giết. |
| Init chưa lease | `duong_cu_luon_false` | Có assert awaiting_lease; **chưa có mutant r812 nhắm riêng chốt init**. Mutant của ca đổi cờ ở record-lease cũ. |
| Ctx.cap_lease → leased/false | `duong_cu_luon_false` | Đạt. |
| True không quay về đường cũ | `true_khong_quay_ve_duong_cu` | Đạt, kiểm byte nguyên. |
| Thiếu kích hoạt → false/legacy | `khong_kich_hoat_la_false` | Đạt; review legacy accepted. |
| Shallow → false | `nong_la_false` | Đạt. |
| Hai dòng khai → false | `hai_dong_khai_la_false` | Đạt. |
| Chưa comment workflow | `lease_chua_comment_workflow` | Đạt. |
| H lease check có răng | `lease_h_hong` | Đạt cho H check; bỏ returncode làm ca đỏ. |
| Holder check có răng | `nguoi_giu_khac` | Đạt cho hai lease cùng **chuỗi**; chưa đo giao prefix/effective như lớp P1. |
| Canon thiếu phụ thuộc → từ chối | `canon_thieu_nguon` | **Đo khác mục**: AGENTS vẫn có nhưng nội dung hỏng. Có giá trị kiểm guard nguồn suy giảm; thiếu ca xóa hẳn dependency để đo `_canon`. |
| Spec có ở lease OID, không worktree | `dac_ta_chi_tai_lease_oid` | Đạt; mutant H check trên worktree bị giết. Chưa chứng minh snapshot đủ cho bia mộ. |
| Required-check sai kiểu falsy | `required_checks_falsy` | Đạt. |
| Approve còn P1 | `approve_kem_lop_p1` | Đạt. |
| Hạng PX | `hang_px` | Đạt. |
| Slug newline | `slug_xuong_dong` | Đạt. |
| Verdict path/blob không tồn tại | `verdict_blob_khong_co` | **THIẾU ca đúng mục**: path và blob vẫn tồn tại, chỉ đổi `verdict_sha256` thành `b…b`. Ca này đo sai băm, có ích nhưng không thay ca mỏ neo vắng. Reviewer đã tái đo vắng mỏ neo: sản phẩm từ chối đúng. |
| Receipt lệch surface | `bien_nhan_lech_surface` | Đạt cho reviewer. |
| Receipt lệch transport | `bien_nhan_lech_transport` | Bỏ trường transport; đo chốt bắt buộc, mutant bị giết. Reviewer cũng đã đo giá trị transport sai với H thật. |
| Chỉ generation khác | `bien_nhan_lech_generation` | Đạt. |
| Chỉ packet khác | `bien_nhan_lech_packet` | Đạt. |
| Chỉ spec_hash khác | `bien_nhan_lech_spec_hash` | Đạt. |
| Changes_requested trong H, CLI approve | `verdict_changes_requested` | Đạt. |
| Blocked trong H, CLI approve | `verdict_blocked` | Đạt. |
| Executor AG/Gemini hợp lệ | `executor_antigravity_hop_le` | **Một phần**: gọi trực tiếp predicate bằng context tự dựng, không đi record-lease/CLI; `spec_hash='s'*64` không phải băm thật. Có đo họ model và mutant bị giết, chưa phải baseline luồng đầy đủ như yêu cầu. |
| Verdict âm, slug ngoài H | `slug_ngoai_bang_lop` | Đạt; có baseline âm hợp lệ `verdict_am_dung_bang_lop`. |
| Lớp rỗng → approved_pending | `duong_moi_du_dieu_kien` | Đạt; receipt H thật, mutant ép lớp không rỗng/đường approve cũ bị giết. |
| Packet không ADR-0054 đi đường cũ | `khong_kich_hoat_la_false`, `duong_cu_luon_false` | Đạt các ca cũ cùng nền suite. |
| Trần attempt chặn mở, cho khép | `cua_khep_luot_van_chay` | **Một phần**: chỉ state legacy, trần attempt; chưa đo cửa khép ADR-0054 tại trần vòng. Mutant bật lại chốt trần vòng vẫn qua 29/29. |
| Input hỏng ở trần attempt/vòng, byte nguyên | `cua_khep_luot_van_chay` | Đã đo doctor hỏng ở trần attempt; **THIẾU trần vòng với ADR-0054**. Mutant dừng trước H tại trần vẫn qua 29/29. |

Ngoài các mục thiếu/đo lệch trên, chưa có ca r812 bảo vệ ba phép đo land-OID độc lập hay H receipt schema `_thieu`. Cả bốn chốt bị gỡ riêng mà 29/29 vẫn xanh. `COUNTS.json` còn xác nhận `verdict_am_dung_bang_lop` chưa được mutant khai báo nào chọn làm ca đích, nên chưa đủ yêu cầu “mỗi ca có một đột biến”. Đây không phải yêu cầu `accept` hay CI của #834.

**I1–I11 và M1/M2/M4/M5**

| bất biến/mục tiêu | kết quả trong phạm vi r2 |
|---|---|
| I1 / M2 | Approve dùng H canon và vào approved_pending; mỏ neo đã được đo. Identity context còn lệch như lớp P2. |
| I2 / M1 | Local-only, H invalid, holder cùng chuỗi và thiếu comment bị chặn. Độc quyền prefix/effective chưa đúng; snapshot H thiếu phụ thuộc Git cho thay lease. |
| I3 | Miền hạng và lớp rỗng được đo đúng; schema lease/context còn các miền/kiểu hỏng được nhận. |
| I4 | Các reject bình thường của r812 kiểm byte nguyên; input lease hỏng nêu trên lại được ghi. Path/context lỗi còn traceback. Không tìm được đường ghi state rồi từ chối ở review/doctor tại trần sau bản vá. |
| I5 / M4 | Đã đo ghi kết quả rồi mới blocked/rescue; không chặn cửa khép ADR-0054 tại trần vòng. Thiếu mutant bảo vệ trong candidate được tính riêng ở coverage. `_xet_dung(record-lease)` hiện gọi trước kiểm input nhưng nhánh ấy không có tác dụng ghi state; không tính thêm một finding chỉ từ vị trí gọi. |
| I6 | Packet này chưa mở quyền phái sinh mới; không đòi làm #813–#815. |
| I7 | Ngoài r2; chuyển #834, không tính hạng. |
| I8 | So họ AG đã sửa; provider/tuple executor và bí danh lease chưa khớp trọn vẹn. |
| I9 | Init/lease cũ false và review legacy accepted được đo; nền suite cũ xanh. |
| I10 | Packet/generation/SHA/spec hash receipt được kiểm; role receipt reviewer được kiểm. Role/generation lease và shape context còn thiếu validation. |
| I11 | Record-review âm chỉ nhận slug trong bảng H, đã đo cả dương/âm và mutation. Connector không nằm trong packet. |
| M5 | Protocol:241–244 có điều kiện “packet áp ADR-0054”, trỏ accept sang #834; đạt. Không còn parser/lệnh accept mới của candidate r1 trong r2. |

**Kết quả chạy và giới hạn**

- `cp -a /home/user/rv812 /tmp/rv812-r2-suite`, rồi `python3 /tmp/rv812-r2-suite/.claude/dev/packet_loop_test.py > SUITE.log 2>&1`: **rc=0**, **`nền: 434/434 đạt · BỎ QUA: 1`**, **`TỔNG: ĐẠT`**. Tổng 435 ca, 199 mutant; **198 mutant đo được và bị giết**, **1 mutant Windows không đo được**, không tính là đã giết. Ca bỏ qua: `luong_canonical_chay_that`; mutant: `luong_canonical_chay_that_dao_os_name`. Không có ca/mutant thất bại trong phần đo được; không dùng kết quả này để xóa 6 mutant kiểm toán sống. Toàn văn `SUITE.log`, số liệu `RUN_RESULTS.json`.

- `python3 /tmp/rv812-r2-suite/.claude/dev/packet_loop.py doctrine-scan --root /tmp/rv812-r2-suite`: **rc=0**, 10 tệp, 0 chỗ chép doctrine.
- `adr-song` trên cùng bản sao: **rc=0**, 53 ADR / 53 dòng, khớp 1–1; ngoại lệ trạng thái 0016 được khai sẵn.
- `git -C /home/user/rv812 diff --check 4c7c298 HEAD`: **rc=0**.
- 29/29 ca r812 chạy lại độc lập; 31/31 mutant r812 khai báo đều giết ca đích. Đã đọc lý do đỏ trong `MUTANTS.jsonl`: lỗi assertion rc/state/byte đúng chốt, không phải traceback setup/import. Sáu mutant kiểm toán ngoài bảng **sống 29/29 mỗi mutant**.
- `HINT.patch`: `git apply --check` trong bản sao cùng head **rc=0**, compile Python đạt. Chạy 9 ca gợi ý trên exact head: 7 đỏ đúng các lỗi sản phẩm đã báo, 2 xanh. Hai ca xanh này đỏ đúng lý do khi bỏ `_thieu` hoặc bật chặn cửa khép ở trần vòng; xem `HINT_CHECK.jsonl`.

Kích thước, đo bằng `git diff --numstat 4c7c298 HEAD`:

| đường dẫn | thêm | xóa |
|---|---:|---:|
| `.claude/dev/packet_loop.py` | 222 | 35 |
| `.claude/dev/packet_loop_test.py` | 209 | 0 |
| `docs/PROTOCOL_DA_PHIEN.md` | 4 | 0 |
| **Tổng** | **435** | **35** |

Đúng **3 đường dẫn**, **435 ≤ 450**, đạt ADR-0053. HINT là dữ liệu gợi ý, chưa phải diff sản phẩm đủ nghiệm thu hay phương án bảo đảm nằm trong trần nếu chép nguyên vào candidate.

Đối chiếu byte nguồn với bản `cp -a` ban đầu: mọi tệp chung giống nhau trừ `.git/index` của bản sao được Git refresh; index entries qua `git ls-files --stage` vẫn trùng. Bản sao có thêm hai tệp bytecode do lệnh Python chạy trên bản sao; không có chúng ở kho nguồn. Xem `READONLY_CHECK.json`. Đây là phép so snapshot nội dung đầu/cuối, không tuyên bố chứng minh mọi thao tác trong lịch sử; mọi lệnh ghi của review đều neo `/tmp` hoặc thư mục ra.

**HINT và hướng xử lý**

Nhãn: **“chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit”**.

`HINT.patch` chỉ thêm phản chứng TEST thuần cho các lớp phức tạp, phù hợp giới hạn patch-as-hint của packet sensitive ở protocol §8. Hướng sửa production nằm ở bảng lớp; patch không tự sửa authority/gate của executor. Các ca mới không được coi là đã vá chỉ vì reviewer soạn chúng: chính kết quả chạy trên head hiện tại còn đỏ được lưu kèm. Executor cần tái dẫn xuất, bổ sung mutant mục tiêu và giữ tổng diff trong trần, hoặc dùng quy trình thay scope được chủ kho quyết định. Không áp HINT vào KHO trong lượt này.

**Ngoài phạm vi r2 — không tính hạng, không nhận là đã vá**

- `accept`, readback CI, connector, I7: #834. Ba lớp r1 `connector-verdict-incomplete`, `ci-attempt-provenance-missing`, `conflicting-evidence-overwrite`, cùng phần connector của `findings-not-receipt-bound`, được chuyển theo scope do chủ kho quyết. Không dùng việc gỡ mã ấy để tuyên bố các lớp đã đóng.
- `mo-lai`, `cho_chu_kho`, checkpoint mới: #813; vòng P3: #814; generation kế tiếp: #815; đếm lần đẩy và kích hoạt: #816.
- Windows-only gate/mutant không đo được trên Linux; ghi riêng là skipped, không chuyển thành pass. Không thực hiện CI/readback/connector qua mạng vì assignment offline.
