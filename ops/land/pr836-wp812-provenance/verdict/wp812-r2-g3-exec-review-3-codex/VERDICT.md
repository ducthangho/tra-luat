Reviewed commit: 468667238e53e77580e4be62e0b8ed5753a75cd9
Verdict: changes_requested — P0=0 P1=1 P2=3 P3=0

Review độc lập, offline, **4 lớp còn mở**. Ngưỡng chủ kho là hết cả P0–P3. Kho `/home/user/rv812` được đối xử read-only; bản sao chạy suite, fixture và mutant đều ở `/tmp`. Không push, merge, đăng comment hay gọi connector.

## Định danh và phạm vi

- HEAD đã kiểm bằng `git -C /home/user/rv812 rev-parse HEAD`, đúng SHA dòng 1; clone đầy đủ, không shallow. Base: `4c7c29858220ae575bebc5e0a343842cd3db4546`. Đã đọc diff base→head, `783463b`→head và `97f3bc1`→head, cùng hai verdict trước và mã validator được gọi.
- Đã đọc đặc tả qua `git show origin/ops/wp812-spec:…` và tự băm: r2 `d64987461d89429ca97230ec5e796bf987bb9383d765279543e6a7fc14513eef`; phần chung `4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0`. Cả hai khớp. Lease: `ops/leases/wp812-r2-g3-claude.yaml`, revision 2 / generation 3, executor Claude, reviewer Codex, sensitive / cross_approved. Đã đọc cả đặc tả #834 để giữ ranh giới r2.
- Reviewer thực: Codex/OpenAI, nền phiên khai GPT-6; Linux/Python, thực thi shell qua `exec_command`, transport máy. Không có telemetry chứng minh model/effort từng request hoặc danh tính launcher CLI/Desktop; không suy identity từ actor GitHub và không tự tạo receipt assurance. Không dùng reviewer con hay context executor.
- Không gọi mạng của kho nguồn. Các lệnh fetch/push trong phản chứng chỉ đi tới bare origin **cục bộ của fixture**. Payload đo là tên tệp tương đối và dữ liệu schema thông thường.

## Bảng lớp còn mở

`pl` = `.claude/dev/packet_loop.py`; `test` = `.claude/dev/packet_loop_test.py`. Dòng trên exact head. Các biểu hiện cùng nguyên nhân được đếm chung, không cộng riêng mỗi probe.

| slug | hạng | biểu hiện (file:dòng) | phép đo đã chạy | hướng vá |
|---|---|---|---|---|
| `lease-holder-scope-incomplete` | P1 | pl:2437–2440, pl:2500, pl:2516–2526 | `REPRO_R3.jsonl`: baseline lease rc=0; chỉ thêm lease cạnh tranh giữ `X/`, `x\a.py`, hoặc prefix Unicode NFD tương đương NFC của ứng viên: **rc=0, leased**, state đổi. Dạng `./x/a.py` cũng bị bỏ qua. Chiều bắt oan: effective set hợp lệ mở rộng từ `x/a.py` sang thêm `y/b.py` lại **rc=7**. | Chuẩn hóa/kiểm đường dẫn theo protocol §5 trước mọi phép hỏi và so giao: separator, NFC, case-fold, miền đường dẫn, symlink/parent. Dùng một biểu diễn cho cả hai bên và cả tập khai báo/hiệu lực. `ai-dang-giu` hiện chỉ hỏi chuỗi trong `write_set`; không dùng câu trả lời hẹp ấy để kết luận rằng phần closure chỉ nằm trong `effective_write_set` không có người giữ. Giữ Đ canon, bổ sung phép đo scope đúng nghĩa; dạng không đo được phải từ chối. HINT có bốn ca. |
| `identity-compared-by-provider-family` | P2 | pl:2575, pl:2588 | `IDENTITY_R3.jsonl`: luồng **CLI đầy đủ** với lease AG/Gemini + reviewer Claude đạt `approved_pending`; đổi họ executor hợp lệ sang `openai`, receipt khai họ canon `gpt`, H schema và Git anchor đều đạt nhưng **rc=11, `ho-executor`**. | Chuẩn hóa họ **được lease khai** sang miền canon, kể cả `openai`↔`gpt`; khi có lời khai, không quay về họ mặc định của tên provider. Dùng cùng phép đổi cho cả hai vai. Giữ các chốt provider/surface/transport vừa bổ sung. HINT có baseline AG qua CLI. |
| `new-input-schema-incomplete` | P2 | pl:2427, pl:2443–2449, pl:2502–2505, pl:2543–2552, pl:2573–2587 | `REPRO_R3.jsonl`: lease chỉ đổi `branch: ""` vẫn **rc=0, leased**, ghi state mà lần `status` kế tiếp **rc=8** (`STATUS.json`). Receipt chỉ đổi provider reviewer hoặc executor thành list/dict gây **TypeError/traceback, rc=1**. Chỉ khai `model_reviewer_identity.model_family: []` hoặc `{}` lại **rc=0, approved_pending**, vì dữ liệu hỏng bị đọc như vắng rồi fallback. Quét context cũng thấy `lease_ref=[]`, `lease_path={}`, OID/repo sai dạng và required-check entry sai kiểu qua `_load`. | Kiểm kiểu/miền trước chuẩn hóa, tra dict hoặc fallback; nguồn có mặt nhưng sai kiểu không phải nguồn vắng. Dựng context rồi kiểm bằng **cùng schema** trước `_save`; `_load` kiểm toàn bộ khóa và giá trị lồng. Receipt hỏng phải trả rc=11 có kiểm soát, state nguyên byte; không tiếp tục đánh giá các biểu thức identity sau khi schema đã báo lỗi. HINT có ca lease tự sinh state hỏng, provider sai kiểu và family falsy. |
| `required-mutation-coverage-missing` | P2 | test:6003–6023, test:6081, test:6116–6124, test:6125–6177 | Nền **50/50** ca r812 và **51/51** mutant r812 khai báo đều đạt yêu cầu hiện có. Nhưng mutant riêng bỏ so receipt SHA, bỏ so lease ID, hoặc bỏ transport executor đều **sống 50/50** (`AUDIT_R3.jsonl`). Vẫn thiếu ca dependency thật sự vắng; ca AG chỉ gọi predicate với context tự đặt và `spec_hash='s'*64`. Ba ca chưa được bảng mutant chọn làm đích: prompt là thư mục, verdict path vắng, verdict âm hợp lệ. | Thêm baseline/âm đúng một yếu tố cho tuple I10 và đủ identity; thêm dependency vắng thật; đưa AG qua record-lease/CLI với băm thật. Gắn mutant r812 vào đúng ca và kiểm lý do đỏ. Bốn ca xanh mới trong HINT đỏ đúng khi lần lượt gỡ SHA, lease ID, transport executor và chốt dependency. Không coi một mutant tương đương sống sót là thiếu coverage. |

### Chi tiết phạm vi quét cùng lớp

**Holder.** Bản vá đã chặn giao prefix cùng cách viết và lease khác mở rộng effective set. Tuy nhiên `_giao` chỉ bỏ `planned:`, trim và bỏ `/` cuối; chưa làm các bước chuẩn hóa bắt buộc của §5. Các phép đo case-fold/NFC là quy tắc exclusion của protocol trên mọi hệ điều hành, không phải suy đoán rằng Linux sẽ đồng nhất hai tên tệp Git. Dạng `.` phải bị bác theo §5, cũng không được âm thầm coi là một lease không liên quan. Các probe đều có lease remote fixture, H check và comment workflow; không làm yếu canon để nhận lease. Với effective expansion, lease chỉ có một holder, không có đối thủ: caller hỏi `y/b.py` nhưng canon chỉ xét `write_set`, trả không ai giữ, rồi caller bác quyền mà effective set đã cấp. Hai chiều lỗi cùng nằm ở phép hợp thành scope của M1/I2.

Đã đo thêm symlink **hoàn toàn trong fixture**, không có đường thoát cây: `alias` trỏ `x`, kiểm bằng `resolve()` rằng `alias/a.py` và `x/a.py` là cùng tệp thật. Baseline có alias và một lease đạt rc=0; chỉ thêm lease cạnh tranh giữ `alias/a.py` vẫn rc=0/leased (`SYMLINK_R3.py`, `SYMLINK_R3.json`). Đây là giao cùng tệp trên chính Linux đã đo, ngoài ba chiều chuẩn hóa chuỗi ở trên.

**Identity.** Các phản chứng identity lượt 2 đã được chặn thật: provider executor khác dù cùng họ, surface khác, transport khác đều rc=11; bí danh `anthropic_claude` và `openai_codex` được nhận. Lớp còn mở ở chuyển miền họ model: `MODEL_FAMILIES` của lease dùng `openai`, còn `_ho_model_cua_ten('openai')` của validator trả rỗng. Fallback theo provider cứu trường hợp Codex nhưng không cứu Antigravity, vì AG không có họ mặc định. `IDENTITY_R3.py` đi qua init → lease remote/H/Đ/R → begin → reviewing → record-review; cả hai receipt được kiểm độc lập `_thieu=[]`, `_neo_git=([],[])`, dùng spec hash thật. Vì vậy đây là từ chối một cấu hình được cả lease validator và receipt validator cho phép, không phải lỗi setup hay đòi hỗ trợ họ ngoài miền.

**Schema/I4.** Falsy identity trong lease, role, generation, assurance, prompt là thư mục, context rỗng/lồng sai hình dạng của lượt 2 đều đã bị từ chối có kiểm soát. Lỗ mới ở `_ten_provider`: dù `_thieu` đã phát hiện provider sai kiểu, list biểu thức sau nó vẫn được đánh giá, tra dict bằng list/dict rồi traceback. Byte state giữ nguyên trong các ca traceback; không gọi đó là ghi-state-trước-từ-chối. Lease branch rỗng thực sự ghi state hỏng; receipt family sai kiểu thực sự được approve. Các context field chưa dùng ở r2 được ghi để chỉ rõ độ đầy đủ schema, không nâng thành finding riêng của #834.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn lượt 2: `origin/ops/wp812-g2-reviews:ops/reviews/wp812-r2-g3-exec-review-2-codex/`, SHA `97f3bc18a937c251f9ee639279e2ca818bce9a58`. Đã chạy lại `REPRO.py`, `EXTRA_PROBES.py`, `IDENTITY_AB.py`, `AUDIT_MUTANTS.py` trên bản sao exact head. Chỉ đổi đường dẫn bản sao; runner mutant được bổ sung hỗ trợ cặp thay thế tuple mới, không đổi ý nghĩa probe. Mã/kết quả ở `REPLAY/`.

| lớp lượt 2 | nhãn | bằng chứng |
|---|---|---|
| `lease-holder-scope-incomplete` | **vá hờ** | Prefix/effective của lease cạnh tranh và `planned:` đã đúng; chuẩn hóa §5 vẫn lọt, effective closure của chính ứng viên vẫn bị hỏi sai phạm vi. |
| `identity-compared-by-provider-family` | **vá hờ** | Ba phép A/B provider/surface/transport đều bị bác đúng, alias canon đã nhận; AG/openai hợp lệ vẫn bị suy về họ mặc định rỗng. |
| `lease-checks-worktree` | **đã vá thật** trong phạm vi đã đo | Lease thay thế/bia mộ hai chiều qua H trên Git snapshot và `record-lease` rc=0; spec/prompt vắng worktree vẫn rc=0. Mutant snapshot mất Git giết ca bia mộ; không quay lại kiểm checkout ứng viên. |
| `new-input-schema-incomplete` | **vá sinh lỗi mới** | Các ca cũ đã chặn; helper alias mới phát sinh TypeError khi provider là list/dict. Branch rỗng/family receipt falsy còn nhận; schema context chưa đầy đủ. |
| `required-mutation-coverage-missing` | **vá hờ** | Cả sáu mutant kiểm toán sống của lượt 2 nay bị giết đúng ca; vẫn còn ba mutant mới I10/identity sống 50/50 và các thiếu hụt nghiệm thu dưới đây. |
| `temporary-artifacts-not-cleaned` | **đã vá thật** trong phạm vi đã đo | `CLEANUP.json`: thành công, H lease bị bác, review bị bác và cả traceback provider đều còn **0** `pl812-canon-*`, registry chỉ còn **1** worktree chính. Mutant bỏ cleanup bị ca r812 dọn tạm giết. |

Các lớp lượt 1 còn trong r2 được kiểm lại bằng phần áp dụng của `REPRO.py` gốc (`REPLAY/REPRO_R1_APPLICABLE.py`), cùng probe r1 trong REPLAY/REPRO.py. Phần `accept` được bỏ theo scope; probe doctor ở trần dùng verdict âm H hợp lệ trước đó để có cửa begin hợp lệ.

| lớp lượt 1 | kết luận ở lượt này |
|---|---|
| `receipt-validation-incomplete` | **Đã vá thật** với các phản chứng gốc: ChatGPT giả Codex, transport sai, mỏ neo vắng đều rc=11, byte nguyên; baseline H đầy đủ. Bỏ `_thieu` nay bị ca `schema_h_bat_buoc` giết. Input kiểu mới/family falsy được đếm trong schema, không cộng lớp thứ hai. |
| `identity-compared-by-provider-family` | **Vá hờ**, như bảng lớp. AG/Gemini đạt; AG/openai còn lỗi. |
| `findings-not-receipt-bound` — record-review | **Đã vá thật**: verdict âm không H hoặc slug ngoài bảng bị rc=11; âm có slug trong bảng chạy được. Predicate vẫn gọi cho cả hai đường verdict. |
| `stop-validation-order` | **Đã vá thật** ở các đường đã đo: bad H ở trần vòng rc=11/byte nguyên; doctor hỏng ở trần attempt rc=10/byte nguyên; approve khép ở trần vòng ghi review và vào approved_pending; âm hợp lệ ghi đủ hai review, đóng attempt rồi rc=3/blocked/rescue. Hai mutant thứ tự/cửa khép của lượt 2 nay bị giết. |
| `lease-checks-worktree` | **Đã vá thật** như đối chiếu lượt 2; cả biểu hiện r1 vắng spec worktree và r2 thiếu Git snapshot đều đã đóng. |
| `new-input-schema-incomplete` | **Còn mở**, như bảng lớp. Required-check falsy và slug newline không tái phát. |
| `required-mutation-coverage-missing` | **Còn mở**, như bảng lớp. Sáu thiếu hụt kiểm toán lượt 2 đã có răng; còn chốt mới chưa được bảo vệ. |

## Đối chiếu `nghiem_thu` r2

Tên ca dưới đây đều có tiền tố `r812_`. “Đạt” là đã chạy, đọc assertion của mutant và thấy đỏ ở chốt tương ứng, không chỉ thấy tên ca. Baseline review chung được kiểm độc lập bằng `_thieu` và `_neo_git`; không có accept/CI/connector trong bảng này.

| mục bắt buộc | ca tương ứng | kết quả |
|---|---|---|
| Lease chỉ ref cục bộ | `lease_chi_o_ref_cuc_bo` | Đạt; mutant ls-remote bị giết. |
| Spec lệch băm, byte nguyên | `dac_ta_lech_bam` | Đạt; mutant bỏ băm/ghi sớm đều bị giết. |
| Init chưa lease | `duong_cu_luon_false` | Assert awaiting_lease đúng. Vẫn thiếu mutant **khóa r812** của candidate nhắm riêng init; mutant cũ toàn suite có bảo vệ init. Mutant init riêng của reviewer cũng làm ca này đỏ. |
| Ctx.cap_lease → leased/false | `duong_cu_luon_false` | Đạt. |
| True không quay đường cũ | `true_khong_quay_ve_duong_cu` | Đạt, byte nguyên. |
| Thiếu kích hoạt → false | `khong_kich_hoat_la_false` | Đạt; review đi accepted legacy. |
| Shallow → false | `nong_la_false` | Đạt. |
| Hai dòng khai → false | `hai_dong_khai_la_false` | Đạt. |
| Chưa comment workflow | `lease_chua_comment_workflow` | Đạt. |
| H lease check có răng | `lease_h_hong` | Đạt; bỏ returncode giết đúng ca. |
| Holder có răng | `nguoi_giu_khac`, `nguoi_giu_prefix_giao_nhau`, `nguoi_giu_effective_giao_nhau` | Đạt với cách viết đã test. Chưa bao phủ chuẩn hóa và own effective closure; sản phẩm còn lỗi P1. |
| Canon thiếu phụ thuộc | `canon_thieu_nguon` | **Đo khác mục**: AGENTS vẫn tồn tại, nội dung hỏng. Thiếu ca tệp dependency thực sự vắng. Ca gợi ý `r812_r3_dependency_absent` xanh ở head, đỏ khi bỏ chốt đọc nguồn. |
| Spec ở lease OID, vắng worktree | `dac_ta_chi_tai_lease_oid` | Đạt; mutant quay về worktree bị giết. Ca bia mộ bổ sung cũng xanh. |
| Required-check sai kiểu falsy | `required_checks_falsy` | Đạt. |
| Approve kèm P1 | `approve_kem_lop_p1` | Đạt. |
| Hạng PX | `hang_px` | Đạt. |
| Slug newline | `slug_xuong_dong` | Đạt. |
| Verdict path/blob không tồn tại | `verdict_path_khong_ton_tai` | **Đã có ca đúng mục** mới. Ca cũ `verdict_blob_khong_co` vẫn đo sai digest, có ích nhưng khác mục. Ca mới chưa được chọn làm target trong bảng mutant. |
| Receipt lệch surface | `bien_nhan_lech_surface` | Đạt. |
| Receipt lệch transport | `bien_nhan_lech_transport` | Đo xóa trường transport; có răng. Reviewer tái đo giá trị transport sai cũng bị bác. Executor transport còn thiếu ca/mutant riêng. |
| Chỉ generation khác | `bien_nhan_lech_generation` | Đạt. |
| Chỉ packet khác | `bien_nhan_lech_packet` | Đạt. |
| Chỉ spec_hash khác | `bien_nhan_lech_spec_hash` | Đạt. I10 còn thiếu SHA độc lập: mutant bỏ so SHA sống 50/50. |
| H changes_requested, CLI approve | `verdict_changes_requested` | Đạt. |
| H blocked, CLI approve | `verdict_blocked` | Đạt. |
| Executor AG/Gemini hợp lệ | `executor_antigravity_hop_le` | **Chưa đủ baseline luồng**: predicate nội bộ, context tự dựng, spec hash không thật. Reviewer đã đo CLI AG/Gemini xanh và AG/openai đỏ như trên. |
| Verdict âm, slug ngoài H | `slug_ngoai_bang_lop` | Đạt; baseline âm hợp lệ có ở `verdict_am_dung_bang_lop`, nhưng ca dương này chưa có mutant chọn làm đích. |
| Lớp rỗng → approved_pending | `duong_moi_du_dieu_kien` | Đạt; H thật, mutant siết lớp rỗng/đường approve cũ bị giết. |
| Packet không ADR-0054 đi đường cũ | `duong_cu_luon_false`, `khong_kich_hoat_la_false` | Đạt các đường cũ đã đo; nền legacy xanh. |
| Trần attempt: chặn mở, cho khép | `cua_khep_luot_van_chay`, `tran_vong_cua_khep_ghi_ket_qua` | Đạt; nay có thêm ADR-0054 ở trần vòng. |
| Input hỏng ở trần, byte nguyên | `cua_khep_luot_van_chay`, `tran_vong_dau_vao_hong_khong_ghi` | Đạt; mutant dừng trước H nay bị giết. |

Ba phép land-OID độc lập nay có đủ ca `oid_khong_chua_adr`, `oid_khong_dua_adr_vao`, `oid_ngoai_first_parent` và mutant tương ứng. Cả ba mutant kiểm toán cũ bị giết đúng ca. `_thieu`, I4 ở trần vòng và I5 khép vòng cũng đã được test mới bảo vệ thật.

`AUDIT_R3.jsonl` còn đo mutant bỏ uniqueness slug sống 50/50; đây là khoảng phủ của một chốt sản phẩm, không thêm lớp/hạng riêng. Mutant bỏ phép so khác họ tại caller là **tương đương khi `_thieu` canon còn sống**, nên không lấy sự sống của nó làm bằng chứng thiếu coverage.

## I1–I11 và M1/M2/M4/M5

| bất biến/mục tiêu | kết quả trong phạm vi r2 |
|---|---|
| I1 / M2 | Đường approved_pending có H thật, không còn approve→accepted cũ khi true. Schema receipt sai kiểu còn được nhận như lớp P2. |
| I2 / M1 | H trên snapshot Git, remote ref và comment workflow đã đo; holder scope còn P1. Không đòi quyền từ readback R đơn độc. |
| I3 | Miền P0–P3/fullmatch slug/lớp rỗng đúng; đầu vào mới vẫn có falsy bị đọc như vắng. |
| I4 | Reject ở trần giữ nguyên byte và có mã kiểm soát. Lease branch rỗng ghi state hỏng; provider sai kiểu traceback; xem schema. |
| I5 / M4 | Một helper gom trần attempt, pre-review legacy, same-failure và rescue sau review. Cửa khép ADR-0054 không bị chặn ở trần vòng; đã đo cả dương/âm và mutant. Lời gọi helper ở record-lease trước validate là no-op ở cửa này, không tạo finding chỉ từ vị trí. |
| I6 | Không mở quyền phái sinh mới ở packet này; không đòi #813–#815. |
| I7 | Ngoài phạm vi r2, #834. |
| I8 | Tuple provider/surface/transport của lượt 2 đã vá; chuyển miền model family và schema family còn lỗi. |
| I9 | Init/lease legacy false, review legacy accepted và nền cũ đã đo. Không phát hiện thêm hồi quy luồng hợp lệ cũ trong phạm vi đo. |
| I10 | Sản phẩm có chốt packet/generation/SHA/spec_hash/lease_id và role reviewer. Chốt SHA/lease_id chưa có răng trong suite r812; context schema chưa đủ. |
| I11 | Verdict âm dùng H và chỉ nhận slug trong bảng reviewer; phản chứng gốc và mutant membership đều đạt. Phần connector thuộc #834. |
| M5 | Protocol:241–244 có approved_pending **có điều kiện ADR-0054**, chỉ cửa accept #834 đi tiếp; đạt. Parser r2 không có cửa accept mới. |

## Kết quả lệnh và bằng chứng

`cp -a /home/user/rv812 /tmp/rv812-r3-suite`, rồi `python3 /tmp/rv812-r3-suite/.claude/dev/packet_loop_test.py > SUITE.log 2>&1`: **rc=0**, **`nền: 455/455 đạt · BỎ QUA: 1`**, **`TỔNG: ĐẠT`**. Tổng **456 ca**, **219 mutant**; **218 mutant đo được và bị giết**, **1 mutant Windows skipped**, không tính thành pass. Ca skipped: `luong_canonical_chay_that`; mutant: `luong_canonical_chay_that_dao_os_name`. Không có thất bại trong phần suite đo được. Toàn văn `SUITE.log`, số liệu `RUN_RESULTS.json`.

`AUDIT_R3.py`: rc=0, chạy cả 50 ca r812 trên mỗi mutant riêng. Ba mutant SHA/lease ID/transport executor sống 50/50; uniqueness sống 50/50; chốt khác họ tại caller tương đương với `_thieu` nên không tính thiếu hụt. Mutant đổi init sang leased bị giết bởi 49/50 ca, trong đó `duong_cu_luon_false` đỏ đúng assert awaiting_lease. Kết quả này không dùng các lỗi setup phụ thuộc init để tuyên bố ca khác đo riêng init.

Các phép chạy bổ sung:

- `REPLAY/REPRO.py`: rc=0; baseline H thật; tất cả phản chứng gốc còn áp dụng đều cho kết quả đã ghi. `REPLAY/REPRO_R1_APPLICABLE.py`: rc=0, chạy phần review/lease của script r1 gốc; không chạy accept đã tách.
- `REPLAY/EXTRA_PROBES.py` và `REPLAY/IDENTITY_AB.py`: rc=0; cả ba lỗi scope và ba lỗi tuple của lượt 2 đã đổi sang kết quả đúng. `REPLAY/AUDIT_MUTANTS.py`: 50/50 baseline, 51/51 mutant khai báo bị giết; cả **6/6** mutant kiểm toán lượt 2 nay bị giết, đọc lỗi assertion đúng chốt.
- `REPRO_R3.py`: rc=0; dữ liệu phản chứng mới trong `REPRO_R3.jsonl`. `IDENTITY_R3.py`: rc=0; H/schema/Git anchor đã kiểm độc lập trước CLI. Lệnh `status` xác minh state do lease branch rỗng sinh ra: rc=8, byte nguyên (`STATUS.json`).
- `doctrine-scan`: rc=0, quét 10 tệp/0 chỗ chép doctrine. `adr-song`: rc=0, 53 ADR/53 dòng, khớp 1–1, ngoại lệ 0016 được khai sẵn. `git diff --check 4c7c298 HEAD`: rc=0.
- `CLEANUP.json`: 4 đường hoàn tất, không sót canon directory/worktree phụ. Đây là bằng chứng đóng P3 cleanup, không che lỗi rc=1 của schema.

Kích thước đo bằng `git -C /home/user/rv812 diff --numstat 4c7c298 HEAD`:

| đường dẫn | thêm | xóa |
|---|---:|---:|
| `.claude/dev/packet_loop.py` | 288 | 35 |
| `.claude/dev/packet_loop_test.py` | 307 | 0 |
| `docs/PROTOCOL_DA_PHIEN.md` | 4 | 0 |
| **Tổng** | **599** | **35** |

Đúng **3 đường dẫn**. Chủ kho đã cho #812 r2 vượt 450 dòng: **không có finding kích thước**. Review này không khởi chạy thêm lời gọi Codex con hay vòng review tự động.

## HINT và giới hạn

Nhãn: **“chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit”**.

`HINT.patch` là diff **TEST thuần** áp exact head, tuân protocol §8 cho packet sensitive. Không sửa production authority/gate bằng hint. Đã chạy `git apply --check` trên bản sao exact head: rc=0; compile test sau chèn đạt. Không áp vào KHO.

`HINT_CHECK.jsonl`: 12 ca gợi ý chạy trên head, **8 đỏ** đúng lỗi sản phẩm và **4 xanh**. Bốn ca xanh (SHA receipt, lease ID, transport executor, dependency vắng) lần lượt **đỏ đúng rc/state** khi gỡ riêng chốt của chúng. Không có lỗi import/setup vô can. `HINT_TESTS.py` là nội dung test được chèn; `HINT_RUN.py` là runner phép đo. Patch chưa phải bản sửa sản phẩm đủ nghiệm thu; hướng sửa nằm trong bảng lớp. Executor cần tái dẫn xuất, thêm mutant mục tiêu và chạy lại gate.

Kiểm cuối (`READONLY_CHECK.json`): HEAD vẫn đúng SHA dòng 1; tree `42b4aeb19e649a837aef4e81f14b621cf87d177f`; base là tổ tiên; nguồn không shallow, worktree nguồn sạch. **4.254 tệp tracked** của nguồn so byte/symlink với bản sao ban đầu sau chạy suite: **0 khác biệt**. Đây là kiểm snapshot nội dung, không tuyên bố chứng minh mọi thao tác trong lịch sử. Tất cả đường ghi của phép review neo thư mục ra hoặc `/tmp`; không áp patch vào kho nguồn.

## Ngoài phạm vi r2 — không tính hạng

- `accept`, CI readback, connector, I7: **#834**, theo quyết định chủ kho #812 issuecomment-6248507114. Ba lớp r1 `connector-verdict-incomplete`, `ci-attempt-provenance-missing`, `conflicting-evidence-overwrite` và phần connector của `findings-not-receipt-bound` không được nhận là đã vá; cũng không đưa vào số finding r2.
- `mo-lai`, `cho_chu_kho`, checkpoint mới: #813; vòng P3: #814; generation kế tiếp: #815; ghi đẩy/kích hoạt: #816. Không đòi triển khai các packet này và không gọi dịch vụ ngoài để đo chúng.
- Ca/mutant Windows chỉ được ghi skipped trên môi trường Linux, không coi là đã giết hay đã pass.
