Reviewed commit: 77393f6b5d9b04070567ec999e0137b9024b04f1
Verdict: changes_requested — P0=0 P1=0 P2=4 P3=0

Review độc lập, offline, Packet #812 revision 2, lượt 5. Còn **4 lớp P2**. Không dùng reviewer con, GitHub, connector hoặc mạng ngoài để review. Kho `/home/user/rv812` được giữ chỉ đọc; mọi lần chạy, state, fixture, mutation và cây hint nằm ngoài kho ấy. Fetch/push trong phép thử chỉ tới bare origin cục bộ của fixture.

## Định danh và phạm vi

- HEAD đúng dòng 1; tree `0a3fd21d995c8b931f2035202b2f4c144503580e`; base `4c7c29858220ae575bebc5e0a343842cd3db4546` là tổ tiên; clone đầy đủ, không shallow. Worktree nguồn sạch; byte của cả ba tệp review khớp blob HEAD. [READONLY_CHECK.json](READONLY_CHECK.json).
- Đọc đặc tả bằng `git show origin/ops/wp812-spec:…` và tự tính SHA-256: r2 `d64987461d89429ca97230ec5e796bf987bb9383d765279543e6a7fc14513eef`; phần chung `4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0`. Cả hai khớp. Bản đọc: [SPEC.txt](SPEC.txt), [COMMON.txt](COMMON.txt), [LEASE.txt](LEASE.txt). Lease: revision 2, generation 3, executor Claude, reviewer Codex, sensitive/cross_approved.
- Đã đọc diff base→head và delta từ `783463b`, `97f3bc1`, `4686672`, `4504b80`; verdict và mã phản chứng của các lượt trước. Không dùng đặc tả r1 để đòi triển khai `accept`.
- Reviewer thực: Codex/OpenAI, phiên độc lập với executor Claude, shell Linux qua `exec_command`, transport máy. Không có telemetry xác nhận tên model/effort từng request hoặc loại launcher; không suy identity từ GitHub submitter.
- Áp chỉ thị chủ kho: phải hết cả P0–P3; được vượt 450 dòng (#812 issuecomment-6250555271). Không tính kích thước vượt trần thành finding. Trần lời gọi Codex 8 giữ nguyên; không gọi thêm model/reviewer con.

## Bảng lớp còn mở

`pl` = `.claude/dev/packet_loop.py`; `test` = `.claude/dev/packet_loop_test.py`. Dòng trên exact head. Giữ slug lớp cũ khi nguyên nhân vẫn là lớp ấy; không cộng từng biểu hiện thành finding riêng.

| slug | hạng | biểu hiện (file:dòng) | phép đo đã chạy | hướng vá |
|---|---|---|---|---|
| `receipt-validation-incomplete` | P2 | pl:2419, pl:2549; đối chiếu chốt chỉ có ở pl:2614 | Lease baseline rc=0. Chỉ làm hỏng nguồn AGENTS, bảng launcher hoặc neo luật trong protocol: vẫn rc=0/leased, trong hai probe sau còn `luat_adr0054=true`, dù chính validator báo `PROVIDER_NGUON_HONG`. Module receipt thiếu API/sai cú pháp lại gây rc=1/traceback. | Kiểm trạng thái nguồn canon ở **cả cửa lease**; việc đọc một hằng assurance không chứng minh validator khỏe. Kiểm giao diện/import và chuyển lỗi nguồn thành mã có kiểm soát, byte state nguyên. HINT có chốt và ca lease nguồn hỏng. |
| `identity-compared-by-provider-family` | P2 | pl:2425, pl:2642, pl:2643, pl:2645, pl:2646, pl:2647 | AG/Gemini và AG/OpenAI có Claude reviewer đều qua H thật. Chỉ đổi surface reviewer thành bí danh canon `claude_code_cli`: `_thieu=[]`, `_neo_git=([],[])`, nhưng CLI rc=11 vì `surface`. Chỉ thêm khoảng trắng quanh provider/surface/transport hợp lệ cũng bị raw comparison bác. | So bản chiếu identity đã chuẩn hóa bằng nguồn canon: provider, surface alias và chuỗi transport; giữ receipt nguyên byte cho hash/Git. Dùng họ lease khai như hiện tại. HINT có các chiều dương và giữ các ca identity lệch. |
| `new-input-schema-incomplete` | P2 | pl:2395, pl:2536, pl:2583, pl:2621 | Receipt chỉ thêm một khóa tham chiếu có tiền tố trong khối executor với kiểu list vẫn approved_pending. `che_do`, `KHONG_do_duoc`, `phien_doc_lap` sai kiểu cũng lọt khi có bằng chứng thay thế hợp lệ. `session_run_id=[]` bị bỏ qua nếu có hai bằng chứng dự phòng đúng. Số issue 4.400 chữ số và NUL trong `spec_path` gây ValueError/traceback, rc=1, byte state nguyên. | Kiểm **mọi nguồn thực sự được canon đọc**, gồm nguồn riêng của `_thieu`, không chỉ bảng tìm model. Phân biệt vắng với có-mà-sai. Tránh chuyển số issue không giới hạn sang int; bắt lỗi argv ở helper Git hoặc kiểm miền đường dẫn trước dùng. HINT có ma trận và chốt tương ứng. |
| `required-mutation-coverage-missing` | P2 | test:6153, test:6181, test:6204, test:6222; chốt chưa được khóa ở pl:2637 và pl:2641 | 74 mutant r812 khai báo đều giết target. Nhưng hai mutant reviewer mới, lần lượt bỏ chốt **role receipt** và **assurance = lease target**, đều sống **74/74**. Hai ca mới đổi đúng một yếu tố xanh trên sản phẩm hiện tại, rồi đỏ rc=0 dưới đúng mutant. | Thêm ca H thật chỉ lệch role và chỉ lệch assurance, cùng hai mutant r812. Đây là thiếu bảo vệ M2/I10, không phải hai lỗi sản phẩm đang cho phép role/assurance sai. HINT bổ sung cả hai. |

### Nguồn canon: còn đường suy giảm ở M1

Lượt trước đã đóng đường review chạy validator suy giảm. Tuy nhiên, `record-lease` chỉ lấy `ASSURANCE_CAN_DOC_LAP` từ module được nạp; nó không đọc `PROVIDER_NGUON_HONG`. Hằng này vẫn tồn tại khi bộ đọc nguồn của canon báo hỏng. Vì vậy việc chép đủ tệp trong `_canon` chưa đủ: **tệp hiện diện nhưng nội dung không còn dùng được** vẫn mở lease.

Đã quét ba phụ thuộc thực: AGENTS, launcher và protocol. [AUDIT_R5.jsonl](AUDIT_R5.jsonl) có baseline và AGENTS hỏng; [HEALTH_R5.jsonl](HEALTH_R5.jsonl) ghi nguyên lý do nguồn của canon, kết quả lease và byte state. Hai probe module thiếu API/sai cú pháp đo thêm chiều lỗi nạp nguồn. Không sửa validator để ép một lease lỗi thành hợp lệ; chỉ thay một nguồn trên remote fixture rồi để sản phẩm tự fetch.

Giữ slug `receipt-validation-incomplete` vì đây vẫn là nguyên nhân caller dùng validator receipt mà không kiểm tình trạng nguồn, nay ở M1. Hạ mức so với P1 lượt 1: chưa chứng minh cửa M2 hiện tại approve được receipt trái quyền; chốt nguồn của M2 vẫn hoạt động. Đây là lệch yêu cầu M1 về nguồn hỏng và lỗi có kiểm soát.

### Identity: họ model đã đúng, phép so chuẩn hóa chưa khép

[IDENTITY_R5.jsonl](IDENTITY_R5.jsonl) chạy CLI đầy đủ trên hai baseline AG/Gemini và AG/OpenAI, lease/receipt/spec hash thật. Cả hai baseline vào approved_pending. Bí danh provider `anthropic` được nhận; chỉ đổi surface thành `claude_code_cli` lại bị bác dù canon thừa nhận bí danh ấy. Thêm khoảng trắng quanh provider `anthropic` cũng bị bác. [AUDIT_R5.jsonl](AUDIT_R5.jsonl) đo riêng ba trường provider/surface/transport trên baseline Codex.

Không yêu cầu nới miền identity. Giữ phép bác provider/surface/transport thực sự khác lease, các chốt khác họ và họ do lease khai. Sửa bằng chuẩn hóa cùng một nghĩa trước phép so; không thay assurance bằng tên provider và không sửa byte receipt đã được băm. HINT đọc bảng alias surface từ bản launcher **canon đã kiểm**, đồng thời dùng các hàm chuỗi/provider của validator.

### Schema: bảng tìm model không phải toàn bộ nguồn attestation

Bản vá lượt 4 dùng `_nguon_tra_model` đúng cho model/family, nhưng `_thieu` còn tra các khóa tham chiếu và người audit với tiền tố executor **ngay bên trong** khối executor. Đã đo cả `executor_model_evidence_ref`, `executor_telemetry_path`, `executor_nguoi_audit`, `executor_audit_actor`: từng giá trị list được nhận khi tham chiếu không tiền tố hợp lệ vẫn có. Baseline chỉ dùng tham chiếu có tiền tố đúng cũng đạt, xác nhận đây là nguồn mà canon thực sự đọc, không phải khóa metadata tự đặt.

Đã quét thêm các trường attestation reviewer `che_do`, `KHONG_do_duoc`, `phien_doc_lap`, `session_run_id`. Với ca session, dựng baseline dương có session chuỗi và các bằng chứng dự phòng hợp lệ trước, rồi chỉ thay session thành list. Lỗi cùng lớp là dùng fallback hợp lệ để che lời khai có mặt nhưng sai kiểu. Các kết quả và kiểm H nằm trong [AUDIT_R5.jsonl](AUDIT_R5.jsonl).

Hai traceback lease không cần dữ liệu nhạy cảm: một ID issue quá dài và một đường dẫn fixture chứa NUL. Byte state vẫn nguyên; **không** gọi chúng là ghi state rồi từ chối. Chúng vi phạm yêu cầu mã thoát có kiểm soát. HINT xử lý số issue bằng so chuỗi đã bỏ số 0 đầu, và chuyển ValueError ở helper Git thành kết quả không đo được.

### Mutation: các chốt mới kiểm toán chưa có ca đích

[REPLAY/AUDIT_R4.jsonl](REPLAY/AUDIT_R4.jsonl) ghi lý do đỏ của đủ 74 mutant r812 khai báo, thêm ba mutant replay cũ; không dùng con số harness thay cho đọc assertion. Các target đều chết tại rc/trạng thái/byte mong đợi. Mutant parser sâu cố ý khôi phục đúng RecursionError của chốt parser, không phải lỗi setup vô can.

[OWN_MUTANTS_R5.py](OWN_MUTANTS_R5.py), [MUTANT_ROLE_R5.jsonl](MUTANT_ROLE_R5.jsonl), [MUTANT_ASSURANCE_R5.jsonl](MUTANT_ASSURANCE_R5.jsonl): bỏ riêng từng phép so M2; toàn bộ 74 ca r812 vẫn xanh. M2 yêu cầu vai reviewer và assurance bằng target lease; I10 yêu cầu vai trò đúng. Các ca tuple generation/packet/SHA/spec_hash không bảo vệ vai trò, và ca AG hợp lệ không bảo vệ assurance. Vì vậy lớp coverage còn mở, dù mọi bullet cụ thể trong danh sách nghiệm thu đã có ca.

[HINT_FINAL_DELTA.jsonl](HINT_FINAL_DELTA.jsonl) kiểm thêm hai ca trên **exact head**, đều bác đúng rc=11; chỉ bỏ đúng chốt tương ứng thì rc=0 và ca đỏ. Không báo đây là lỗi cho qua receipt sai của sản phẩm hiện tại; finding là thiếu mutation protection của điều kiện nghiệm thu.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn lượt 4: `origin/ops/wp812-g2-reviews:ops/reviews/wp812-r2-g3-exec-review-4-codex/`, SHA `4504b80e67e4c3c8e967be92212842eb835c6e85`. Hiện vật gốc ở [PRIOR](PRIOR/); replay trên bản sao head mới ở [REPLAY](REPLAY/).

| lớp lượt 4 | nhãn bắt buộc | bằng chứng lượt 5 |
|---|---|---|
| `lease-holder-scope-incomplete` | **đã vá thật** | `PROBE_R4`: effective không che tập khai; tập khai rỗng, own `.`/`..`/glob đều bị bác, byte nguyên. `SYMLINK_R3`: baseline nhận, thêm đối thủ cùng đích bị rc=7. Các chiều case-fold, separator, NFC/NFD, prefix/effective cũng bị bác; effective expansion hợp lệ vẫn nhận. Mutant union/resolve/miền đường dẫn có răng. Chưa thấy lỗ mới trong các chiều đã quét. |
| `new-input-schema-incomplete` | **vá hờ** | Những biểu hiện cụ thể lượt 4 đã đóng: top-level family, hình dạng identity, surface/transport context và parser YAML sâu bị bác đúng rc=2/8/11, byte nguyên. Còn các nguồn `_thieu` chưa kiểm và ngoại lệ chuyển đổi/argv như bảng lớp. Đây là biểu hiện còn sót của lớp, không gán tất cả thành hồi quy do delta lượt 5. |
| `required-mutation-coverage-missing` | **vá hờ** | Init, dependency thật sự vắng, verdict path vắng, verdict âm hợp lệ và slug trùng đã có mutant đúng ca; 74/74 mutant khai báo bị giết. Nhưng hai mutant M2 role/assurance mới sống 74/74. |

Đã chạy lại `PROBE_R4.py`, `PARSER_R4.py`, `AUDIT_R4.py`; các script lượt 3 `REPRO_R3.py`, `IDENTITY_R3.py`, `AUDIT_R3.py`, `SYMLINK_R3.py`; cùng phần r2 áp dụng của lượt 1 và các probe lượt 2. Chỉ thay đường dẫn sang bản sao cho replay r3/r4. Bản R1 áp dụng bỏ đoạn `accept` thuộc #834; probe doctor ở trần chạy qua runner R2 sau một verdict âm hợp lệ để không đo nhầm cửa đang mở. [REPLAY/RESULTS.json](REPLAY/RESULTS.json).

| lớp cũ còn trong r2 | kết luận trên head này |
|---|---|
| `receipt-validation-incomplete` | Các phản chứng M2 gốc đã đóng: ChatGPT giả Codex, transport sai, anchor vắng đều rc=11/byte nguyên. **Lớp còn mở ở nguồn canon của M1**, như trên. |
| `identity-compared-by-provider-family` | AG/Gemini và AG/OpenAI với họ lease khai đều đạt; provider/surface/transport thực sự lệch bị bác. **Còn mở ở chuẩn hóa alias/chuỗi**, như trên. |
| `findings-not-receipt-bound` — record-review | **Đã vá thật**: âm không H hoặc slug ngoài bảng bị bác; âm đúng bảng chạy được; predicate dùng chung được mutation bảo vệ. |
| `stop-validation-order` | **Đã vá thật ở các đường đã đo**: H hỏng tại trần vòng rc=11/byte nguyên; doctor hỏng ở trần attempt rc=10/byte nguyên; approve khép lượt thành công; âm hợp lệ ở trần ghi đủ review và đóng attempt rồi rc=3/blocked-rescue. |
| `lease-checks-worktree` | **Đã vá thật**: spec/prompt vắng worktree vẫn nhận; thay lease có bia mộ hai chiều qua H trên snapshot Git đúng OID vẫn nhận. |
| `new-input-schema-incomplete` | Required-check falsy, newline slug, branch/provider/family lồng hỏng đều bị bác. **Còn mở** ở các nguồn/ngoại lệ nêu trên. |
| `required-mutation-coverage-missing` | Các thiếu hụt cụ thể lượt 1–4 đã bổ sung; **còn mở** với hai phép so M2 mới kiểm toán. |
| `temporary-artifacts-not-cleaned` | **Đã vá thật**: thành công, lease bị bác và review bị bác đều còn 0 thư mục canon, 1 worktree chính. [REPLAY/CLEANUP_R4.jsonl](REPLAY/CLEANUP_R4.jsonl). |

`AUDIT_R3` nay giết các mutant SHA, lease ID, transport executor và uniqueness bằng đúng ca (73/74 xanh còn lại). Mutant đổi init bị assertion awaiting_lease giết; nhiều ca khác đỏ theo vì phụ thuộc fixture init. Mutant bỏ riêng so khác họ ở caller vẫn sống 74/74 vì `_thieu` canon còn giữ cùng chốt: mutant tương đương, không tính finding.

## Đối chiếu `nghiem_thu` r2

Tên dưới bỏ tiền tố `r812_`. “Đạt” nghĩa là đã chạy ca và kiểm assertion đỏ dưới mutant r812 của đúng yếu tố. Không thiếu tên ca cho các bullet cụ thể. Hai điều kiện M2/I10 role/assurance còn thiếu bảo vệ được ghi riêng, không bị con số 74 che khuất.

| mục | ca | kết quả |
|---|---|---|
| Lease chỉ ref cục bộ | `lease_chi_o_ref_cuc_bo` | Đạt; ls-remote có răng. |
| Spec lệch băm, byte nguyên | `dac_ta_lech_bam` | Đạt; cả bỏ băm và ghi sớm bị giết. |
| Init chưa lease → awaiting_lease | `duong_cu_luon_false` | Đạt; đã thêm mutant r4 nhắm init. |
| Ctx.cap_lease → leased/false | `duong_cu_luon_false` | Đạt. |
| True không quay đường cũ | `true_khong_quay_ve_duong_cu` | Đạt; byte nguyên. |
| Thiếu kích hoạt | `khong_kich_hoat_la_false` | Đạt, false và review accepted theo legacy. |
| Shallow | `nong_la_false` | Đạt, false. |
| Hai dòng khai | `hai_dong_khai_la_false` | Đạt, false. |
| Chưa comment workflow | `lease_chua_comment_workflow` | Đạt. |
| Gỡ H lease check | `lease_h_hong`, `prompt_path_thu_muc` | Đạt. |
| Gỡ holder check | `nguoi_giu_khac` và các ca prefix/effective/union/symlink | Đạt, gồm các chiều mới lượt 4. |
| Canon thiếu dependency | `canon_vang_phu_thuoc` | Đạt cho **tệp thật sự vắng**, có mutant mới chọn đúng ca. Nội dung nguồn hỏng ở M1 còn lỗi sản phẩm riêng. |
| Spec chỉ tại lease OID | `dac_ta_chi_tai_lease_oid` | Đạt; thêm ca bia mộ kiểm snapshot Git. |
| Required-check falsy sai kiểu | `required_checks_falsy` | Đạt. |
| Approve còn P1 | `approve_kem_lop_p1` | Đạt. |
| Hạng PX | `hang_px` | Đạt. |
| Slug newline | `slug_xuong_dong` | Đạt fullmatch. |
| Verdict path/blob không tồn tại | `verdict_path_khong_ton_tai` | Đạt, đã có mutant riêng. Ca tên `verdict_blob_khong_co` chỉ đo **digest sai**, không dùng nó thay ca path vắng. |
| Receipt lệch surface | `bien_nhan_lech_surface` | Đạt. |
| Receipt lệch transport | `bien_nhan_lech_transport` | Ca đo **thiếu trường**; mutant chốt transport bị giết. Giá trị transport sai được replay R1/R2 đo thêm; không khai ca này đã đổi giá trị transport. |
| Chỉ generation khác | `bien_nhan_lech_generation` | Đạt. |
| Chỉ packet khác | `bien_nhan_lech_packet` | Đạt. |
| Chỉ spec_hash khác | `bien_nhan_lech_spec_hash` | Đạt. |
| H changes_requested, CLI approve | `verdict_changes_requested` | Đạt. |
| H blocked, CLI approve | `verdict_blocked` | Đạt. |
| AG/Gemini hợp lệ | `executor_ag_qua_cli` | Đạt CLI/H thật, cả Gemini và OpenAI. Ca predicate `executor_antigravity_hop_le` dùng hash `s*64` không thay bằng chứng luồng này. |
| Âm có slug ngoài H | `slug_ngoai_bang_lop` | Đạt; baseline âm đúng bảng `verdict_am_dung_bang_lop` cũng đã có mutant khóa. |
| Lớp rỗng → approved_pending | `duong_moi_du_dieu_kien` | Đạt, H thật. |
| Packet legacy đi đường cũ | `duong_cu_luon_false`, `khong_kich_hoat_la_false` | Đạt trên Linux, nền legacy không đỏ. |
| Trần attempt chặn mở, cho khép | `cua_khep_luot_van_chay`, `tran_vong_cua_khep_ghi_ket_qua` | Đạt. |
| Input hỏng ở trần, byte nguyên | `cua_khep_luot_van_chay`, `tran_vong_dau_vao_hong_khong_ghi` | Đạt. |
| M2/I10 role reviewer | **THIẾU ca candidate** | Mutant riêng sống 74/74; HINT có ca chỉ đổi role. |
| M2 assurance đúng lease target | **THIẾU ca candidate** | Mutant riêng sống 74/74; HINT có ca chỉ đổi assurance. |

Các chốt land-OID có ba ca độc lập `oid_khong_chua_adr`, `oid_khong_dua_adr_vao`, `oid_ngoai_first_parent`, cùng mutant đúng yếu tố. SHA, lease ID, executor transport, cleanup và schema context cũng có mutation protection. Hai ca phụ chưa được chọn trực tiếp làm target (`bien_nhan_provider_sai_kieu`, `nguoi_giu_cham_gach`) không tự tạo finding: cùng chốt đã được target khác bảo vệ; đây khác hai mutant role/assurance còn sống.

## I1–I11 và M1/M2/M4/M5

| bất biến/mục tiêu | kết quả |
|---|---|
| I1 / M2 | approved_pending phải qua receipt schema/Git; không có đường true→accepted cũ. Source-health M1 còn thiếu như lớp thứ nhất. |
| I2 / M1 | Ref remote, H snapshot, holder canon + scope đối xứng, R workflow có chốt thật. M1 còn nhận nguồn phụ thuộc canon hỏng. |
| I3 | Hạng P0–P3/fullmatch slug/lớp rỗng đúng. Một số lời khai identity sai kiểu còn được nhận. |
| I4 | Reject ở trần đã đo giữ byte; không tìm thấy đường mới ghi state rồi **từ chối có kiểm soát**. Input sai kiểu còn được nhận và ghi state; input lease hoặc source hỏng còn traceback. |
| I5 / M4 | `_xet_dung` gom attempt, round, same-failure và rescue sau review. Cửa khép ADR-0054 ghi kết quả trước trần. Lời gọi record-lease trước validate hiện không xét điều kiện nào, nên không báo lỗi chỉ vì vị trí dòng. |
| I6 | Không thêm cửa quyền phái sinh trong r2; không đòi #813–#815. |
| I7 | Ngoài phạm vi, #834. |
| I8 | Họ model theo lease đã đúng; chuẩn hóa identity chưa khép ở alias và chuỗi. |
| I9 | Init, lease cũ, review cũ và nền legacy Linux đạt. Windows chưa đo, báo skipped riêng. |
| I10 | Các phép so role/packet/generation/SHA/spec_hash/lease ID có trong sản phẩm. Chốt role chưa có ca mutation bảo vệ. |
| I11 | Verdict âm qua H dùng chung; slug phải trong bảng lớp; không tái phát đường tự đặt slug ở record-review đã đo. |
| M5 | Protocol thêm approved_pending có điều kiện ADR-0054 và trỏ accept sang #834; parser không thêm accept. Đạt. |

## Suite, gate và kích thước

Đã chạy `cp -a /home/user/rv812 /tmp/rv812-r5-suite`, rồi `python3 /tmp/rv812-r5-suite/.claude/dev/packet_loop_test.py`:

- **rc=0; `nền: 479/479 đạt · BỎ QUA: 1`; `TỔNG: ĐẠT`.**
- Khai báo 480 ca, 242 mutant; **241 mutant đo được đều bị giết**, gồm **74/74 mutant r812**. Một ca `luong_canonical_chay_that` và mutant `luong_canonical_chay_that_dao_os_name` chỉ chạy Windows bị skipped, không tính là đã giết. Không ca/mutant r812 nào skipped.
- `python3 /tmp/rv812-r5-suite/.claude/dev/packet_loop.py doctrine-scan --root /tmp/rv812-r5-suite`: **rc=0**, 10 tệp, 0 chỗ chép doctrine.
- `python3 /tmp/rv812-r5-suite/.claude/dev/packet_loop.py adr-song --root /tmp/rv812-r5-suite`: **rc=0**, 53 ADR/53 dòng, khớp 1–1, ngoại lệ trạng thái 0016 có sẵn.

Toàn văn: [SUITE.log](SUITE.log), [SUITE_RESULT.json](SUITE_RESULT.json), [DOCTRINE.log](DOCTRINE.log), [ADR.log](ADR.log). Hai mutant kiểm toán mới sống được báo ở lớp coverage; không che bằng kết quả xanh của tập mutant candidate.

`git -C /home/user/rv812 diff --numstat 4c7c298 HEAD`:

| đường dẫn | thêm | xóa |
|---|---:|---:|
| `.claude/dev/packet_loop.py` | 344 | 35 |
| `.claude/dev/packet_loop_test.py` | 438 | 0 |
| `docs/PROTOCOL_DA_PHIEN.md` | 4 | 0 |
| **Tổng: 3 đường dẫn** | **786** | **35** |

Chủ kho đã cho vượt 450; không tính finding kích thước.

## HINT và giới hạn xác minh

[HINT.patch](HINT.patch) là diff gợi ý từ cây riêng trên exact head dòng 1, chỉ chạm hai tệp Python trong write set; **chưa áp/chạy trên KHO**. Executor tự tái dẫn xuất, tự đo và chịu trách nhiệm tích hợp. Không có payload nhạy cảm được soạn để thử.

HINT thêm kiểm nguồn ở lease và lỗi nạp module, chuẩn hóa bản chiếu identity, kiểm các nguồn attestation còn sót, xử lý hai lỗi chuyển đổi/argv, và thêm ca/mutant role/assurance. Nó giữ H canon/snapshot, holder check, effective expansion hợp lệ, AG với họ lease khai, predicate chung cho verdict âm và đường legacy.

`git apply --check` trên bản sao exact head: **rc=0**. Source cây hint giữ nguyên trong các lần đo cuối. Các probe schema/ngoại lệ đều bị bác đúng rc=2/11, byte nguyên; nguồn canon hỏng hoặc thiếu API/sai cú pháp bị rc=8 có kiểm soát; identity alias/chuỗi hợp lệ được nhận. Bằng chứng: [HINT_AUDIT_R5.jsonl](HINT_AUDIT_R5.jsonl), [HINT_HEALTH_R5.jsonl](HINT_HEALTH_R5.jsonl), [HINT_IDENTITY_R5.jsonl](HINT_IDENTITY_R5.jsonl).

Trên bản hint cuối, **94/94 ca r812 xanh; 85/85 mutant r812 bị giết tại ca đích**, không có lỗi import/setup được tính làm bằng chứng. [HINT_VERIFIED_FINAL.jsonl](HINT_VERIFIED_FINAL.jsonl) ghi từng assertion; [HINT_RESULT.json](HINT_RESULT.json) ghi số đếm và băm patch. Hai ca role/assurance cũng được kiểm riêng trên exact head rồi dưới mutant trong [HINT_FINAL_DELTA.jsonl](HINT_FINAL_DELTA.jsonl).

**not_run:** chưa chạy toàn bộ suite legacy trên cây hint; kết quả toàn suite 479/479 ở trên thuộc exact head được review. Kết quả hint không thay verdict của candidate.

Trong cây hint có hai chốt cùng ngăn nguồn dependency vắng: `_canon` và kiểm tình trạng nguồn ở lease. Mutant cũ bỏ một chốt trở thành tương đương; bản hint cuối đổi thành mutant phối hợp gỡ cả hai cho đúng một yếu tố “không đo được nguồn”. Đây là điều chỉnh test cho defense trùng, không lấy một mutant tương đương sống làm lỗi sản phẩm.

## Ngoài phạm vi r2

- **#834**: `accept`, I7, readback CI/run-attempt/connector. Các lớp lượt 1 `connector-verdict-incomplete`, `ci-attempt-provenance-missing`, `conflicting-evidence-overwrite` và phần connector của `findings-not-receipt-bound` được chuyển sang packet đó, không tính hạng tại đây.
- **#813–#816**: mở lại/chờ chủ kho/checkpoint; vòng P3; generation tiếp; ghi đẩy và kích hoạt. Không yêu cầu triển khai các cửa này trong #812 r2.
