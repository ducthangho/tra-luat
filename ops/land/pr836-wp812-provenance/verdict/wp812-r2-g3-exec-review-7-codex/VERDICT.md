Reviewed commit: 91c6d8c31190f5f9ea08e4da42ecafd898ee8935
Verdict: changes_requested — P0=0 P1=0 P2=4 P3=0

Review độc lập, OFFLINE, Packet #812 / MAY-ADR-0054-a revision 2, lượt 7. Còn **4 lớp P2**. Không sửa KHO, không dùng reviewer con, GitHub hay connector. Mọi fixture, state, đột biến và cây HINT nằm ngoài KHO; fetch/push của phép thử chỉ tới bare origin cục bộ.

## Định danh và phạm vi

- HEAD đúng dòng 1; tree `93e27f856872101a9410f82fa870becc4e60a606`; base `4c7c29858220ae575bebc5e0a343842cd3db4546`; clone đầy đủ, không shallow. Ba tệp được review khớp byte blob HEAD. [READONLY_CHECK.json](READONLY_CHECK.json).
- Tự đọc bằng `git show origin/ops/wp812-spec:…` và tính SHA-256: [SPEC.txt](SPEC.txt) = `d64987461d89429ca97230ec5e796bf987bb9383d765279543e6a7fc14513eef`; [COMMON.txt](COMMON.txt) = `4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0`. Cả hai khớp chỉ thị. [LEASE.txt](LEASE.txt): revision 2, generation 3, executor Claude, reviewer Codex, sensitive/cross_approved.
- Đọc mã thật và diff trong write set, các verdict lượt 1–5 và hiện vật dở dang lượt 6. Không suy một verdict cho lượt 6.
- Reviewer thực: Codex/OpenAI, phiên riêng với executor Claude, thực thi shell Linux qua `exec_command`, transport máy. Không có telemetry xác nhận launcher CLI/Desktop hoặc model/effort từng request; không suy danh tính từ người vận chuyển artifact.
- Áp chỉ thị chủ kho #812 issuecomment-6250555271: phải hết P0–P3; được vượt 450 dòng. Không tính kích thước thành finding. Không gọi thêm model/reviewer, giữ ngân sách lời gọi 7/8.

## Bảng lớp còn mở

`pl` = `.claude/dev/packet_loop.py`; `test` = `.claude/dev/packet_loop_test.py`. Dòng trên exact head. Đếm theo lớp, không đếm từng biểu hiện.

| slug | hạng | biểu hiện (file:dòng) | phép đo đã chạy | hướng vá |
|---|---|---|---|---|
| `identity-compared-by-provider-family` | P2 | pl:2451, pl:2513, pl:2514 | Lease dương H/Đ/R rc=0. Provider có khoảng trắng, gồm tên ngắn và bí danh canon, ở executor hoặc reviewer đều rc=2 dù H và holder đã qua. Các ca mới chỉ đổi **một trường** xác nhận cùng kết quả. | Chuẩn hoá chuỗi provider trước tra bí danh và dựng context ở **cả hai vai**; giữ nguyên byte lease. HINT thêm bốn ca và mutant bỏ chuẩn hoá. |
| `new-input-schema-incomplete` | P2 | pl:946, pl:947, pl:955 | Đường mới hợp lệ thêm riêng một trong bốn cờ đường cũ với chuỗi rỗng vẫn rc=0/leased. Đường cũ hợp lệ thêm riêng một trong ba cờ đường mới với chuỗi rỗng cũng rc=0/leased. State đổi. | Phân biệt cờ **có mặt** (`is not None`) với giá trị truthy, rồi kiểm đầy đủ và loại trừ hai đường. HINT quét đủ bảy cờ, kèm mutant khôi phục truthiness. |
| `lease-publication-readback-incomplete` | P2 | pl:2603, pl:2604 | Chỉ đổi `issue_url` của comment baseline sang URL sai host, chuỗi không phải URL, hoặc URL có thêm prefix repo: cả ba vẫn rc=0/leased. Login bot và lease ID giữ nguyên. | So URL đầy đủ thuộc GitHub của **đúng kho + đúng issue**; không dùng phép so hậu tố. HINT giữ cả dạng API và web hợp lệ, có ba ca âm và một ca dương. |
| `required-mutation-coverage-missing` | P2 | test:6219, test:6231, test:6375, test:6505; các chốt ở pl:947, pl:2531, pl:2556, pl:2614 | Các mutant kiểm toán bỏ riêng so packet lease, loại trừ hai đường lease, so identity lease với init, và tên ADR trong kích hoạt đều sống **115/115** ca r812. Đây là chốt đúng của sản phẩm nhưng thiếu ca bảo vệ. | Thêm ca H/Đ/R thật chỉ sai từng yếu tố; khoá mutant r812 cho từng chốt. HINT có cả hai vai AG khi so family với init, cùng ca reviewer surface. |

### Identity: còn sót phía lease

Lượt 5 đã sửa chuẩn hoá receipt; replay hiện tại xác nhận provider/surface/transport receipt có khoảng trắng và bí danh hợp lệ đều được nhận. Tuy nhiên `_ngu_canh_lease` vẫn đưa provider **thô** qua `_ten_provider`. `_ten_provider` tra bảng trước khi strip, còn `_identity` chỉ strip family/surface/transport. Vì thế cùng một identity được canon lease validator chuẩn hoá và nhận, sau đó lại bị caller bác tại bước dựng context.

[IDENTITY_LEASE_R7.jsonl](IDENTITY_LEASE_R7.jsonl) ghi baseline và bốn chiều executor/reviewer × tên ngắn/bí danh. Các ca một trường trong [HINT_FINAL_VERIFY.jsonl](HINT_FINAL_VERIFY.jsonl) loại bỏ khả năng phép đo chỉ thất bại vì đồng thời sửa provider và executor. Không có traceback hay đổi state khi bị bác; lỗi là từ chối một lease hợp lệ. Giữ slug cũ vì lớp so identity chưa khép, không gọi đây là lỗi mới ở phép so họ model.

### Schema: cờ rỗng vẫn là cờ đã truyền

`any(moi)`/`any(cu)` đọc chuỗi rỗng thành “chưa chọn đường ấy”. Cờ có mặt nhưng rỗng vì vậy bị bỏ qua hoàn toàn khi đường kia đầy đủ. Đây trái M1 về hai đường loại trừ và input hỏng phải bị bác, giữ state nguyên byte. Bản vá không chỉ thiếu thông báo lỗi: lệnh thực sự ghi `leased`.

[SAFE_PROBES_R7.jsonl](SAFE_PROBES_R7.jsonl) có baseline, ca trộn hai đường đầy đủ bị bác đúng rc=2, và ca trộn một cờ rỗng lại được nhận. Ma trận mới quét **đủ bốn cờ cũ** (`--lease-id`, `--granted-by`, `--evidence`, `--expires-utc`) và **ba cờ mới** (`--lease-ref`, `--lease-path`, `--lease-comments`) trên exact head rồi trên HINT. Các input hợp lệ của legacy vẫn chạy; chỉ trường hợp đã truyền thêm cờ của đường kia bị từ chối.

### Readback workflow: đúng hậu tố chưa định danh đúng issue

Phép so `.endswith()` không kiểm scheme/host hoặc phần đầu đường dẫn repo. Một comment có URL `https://example.org/repos/o/r/issues/55` được đọc thành comment của issue GitHub `o/r#55`; chuỗi `ordinary/o/r/issues/55` cũng được nhận. Chỉ trường `issue_url` đổi, H/Đ, login bot và body đều giữ baseline. [SAFE_PROBES_R7.jsonl](SAFE_PROBES_R7.jsonl).

I2 đòi đủ H/Đ/R. H và holder hợp lệ không biến readback chỉ sang địa điểm khác thành R hợp lệ của Packet Issue. Finding này là kiểm nhất quán dữ liệu R bị thiếu; không yêu cầu gọi mạng, connector hoặc chứng thực mật mã cho tệp JSON.

HINT so đầy đủ hai dạng URL GitHub hợp lệ, chặn cả sai host, không phải URL và thêm prefix repo. Ca web dương cùng mutant siết bỏ web bảo vệ việc không bắt oan dạng đang được hỗ trợ. Mutant workflow-issue lượt 6 được cập nhật mỏ neo sau thay đổi sản phẩm, vẫn giết đúng ca chỉ lệch số issue.

### Mutation: phân biệt chốt chưa có ca với lỗi sản phẩm

[OWN_MUTANTS](OWN_MUTANTS/) ghi chạy **toàn bộ 115 ca r812** dưới từng mutant kiểm toán. Bốn mutant sống nêu trong bảng là bốn biểu hiện của **một lớp coverage**. Không cộng các lỗi schema, identity hay URL vừa tìm được lần nữa vào số mutant sống.

Mutant thứ năm, bỏ so issue của `granted_on_instruction`, **đã bị giết** bởi `r812_r5_instruction_long` (114/115 còn xanh). HINT thêm ca số issue bình thường để có bằng chứng dễ đọc, nhưng không báo chốt ấy đang thiếu bảo vệ.

[REPLAY/AUDIT_R4.jsonl](REPLAY/AUDIT_R4.jsonl) kiểm assertion và lý do đỏ của **96 mutant r812 khai báo** trên head này. Các mutant khôi phục ngoại lệ chết bởi đúng ngoại lệ bị gỡ chốt, không phải lỗi import/setup vô can. Mutant replay cũ chỉ bỏ chốt tệp dependency vắng vẫn sống do **chốt source-health thứ hai** còn chặn: mutant tương đương, không tính finding. Mutant phối hợp `r812_r4_bo_dep_vang` hiện tại gỡ đúng cả hai lớp phòng vệ cho cùng yếu tố nguồn vắng và bị giết.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn: verdict lượt 5 trên `77393f6b5d9b04070567ec999e0137b9024b04f1` và hiện vật dở dang lượt 6 trên nhánh reviews đã chỉ định. Chạy lại trên bản sao exact head; chỉ thay đường dẫn repo. Phần tự soạn input thuộc các dạng người dùng cấm không được replay; thay bằng chạy **ca r812 đã có** và đột biến chốt của chúng.

| lớp lượt 5 | nhãn bắt buộc | kết quả lượt 7 |
|---|---|---|
| `receipt-validation-incomplete` | **đã vá thật** | Replay nguồn AGENTS/launcher/protocol hỏng, module thiếu API/sai cú pháp đều từ chối có kiểm soát. Ma trận lượt 6: chín API không dùng được × hai cửa lease/review = 18/18 từ chối rc=8, byte nguyên, không traceback. Các chốt `_thieu`, `_neo_git`, source-health và loader có mutant giết đúng ca. Chưa thấy tái phát ở M1/M2 đã đo. |
| `identity-compared-by-provider-family` | **vá hờ** | Receipt alias/chuỗi được vá thật; AG/Gemini và AG/OpenAI qua CLI vẫn đạt; họ lệch lease ở hai vai bị chặn. **Còn provider lease chưa chuẩn hoá chuỗi**, như bảng lớp. |
| `new-input-schema-incomplete` | **vá hờ** | Các nguồn attestation lồng/top-level, kiểu falsy, parser, argv, serialization lượt 5–6 đã có chốt thật. **Còn cờ đường lease đã truyền nhưng rỗng bị coi là vắng**. Không gọi các biểu hiện cũ đã đóng là còn lỗi. |
| `required-mutation-coverage-missing` | **vá hờ** | Role/assurance lượt 5 và sáu mutant sống lượt 6 đã có ca giết. 96/96 mutant r812 khai báo bị giết. **Còn bốn mutant kiểm toán M1 sống 115/115**, như bảng lớp. |

Lượt 6 không có verdict. Các biểu hiện trong `API_R6`, `MORE_R6`, HINT và sáu `OWN_MUTANTS` được đối chiếu như sau:

| nhóm hiện vật lượt 6 | kết quả hiện tại |
|---|---|
| API canon có mặt nhưng không dùng được | 18 phép replay ở hai cửa đều rc=8, byte nguyên, không traceback. [REPLAY/API_R6.jsonl](REPLAY/API_R6.jsonl). |
| Lỗi gọi tiến trình vì write-set, lỗi đọc neo receipt, lỗi encoding khi lưu state | Chạy các ca `r812_r6_write_set_nul`, `write_set_long`, `receipt_nul`, `receipt_native` có sẵn; baseline đạt, mutant gỡ đúng chốt đều đỏ. Không soạn lại các input ấy. |
| Sáu mutant sống: family hai vai; kích hoạt protocol; author/issue/lease ID comment | Nay đều bị đúng các ca `r812_r6_family_*`, `activation_*`, `workflow_*` giết. [REPLAY/AUDIT_R4.jsonl](REPLAY/AUDIT_R4.jsonl). |

Các lớp lượt 1–4 thuộc r2 cũng được rà lại:

| lớp cũ | kết luận/bằng chứng |
|---|---|
| `receipt-validation-incomplete` | ChatGPT giả Codex, transport sai, neo Git vắng bị rc=11/byte nguyên; H dương nhận. Replay R1 áp dụng và R2. |
| `identity-compared-by-provider-family` | AG hai họ hợp lệ, executor provider/surface/transport lệch bị chặn; còn lớp chuẩn hoá lease nêu trên. Replay IDENTITY_R3, IDENTITY_AB_R2, IDENTITY_R5. |
| `findings-not-receipt-bound` — record-review | Âm thiếu H hoặc slug ngoài bảng bị bác; âm đúng bảng chạy được. Vị từ chung và membership có mutant riêng. |
| `stop-validation-order` | H hỏng ở trần vòng rc=11/byte nguyên; doctor hỏng ở trần attempt rc=10/byte nguyên; approve khép lượt được; âm hợp lệ ở trần ghi đủ sổ rồi rc=3/rescue. Replay REPRO_R2. |
| `lease-checks-worktree` | Spec/prompt chỉ tại lease OID vẫn nhận; lease có bia mộ hai chiều được H đo trên snapshot Git đúng OID. Replay R1/R2 và ca r812. |
| `lease-holder-scope-incomplete` | Quét union declared/effective, prefix hai chiều, case/separator/Unicode, miền đường dẫn và đích liên kết bằng các ca có sẵn cùng mutant. Không soạn input mới cho các dạng bị cấm. |
| `new-input-schema-incomplete` | Các phản chứng receipt/context/falsy đã bị bác; còn biểu hiện cờ rỗng ở M1 nêu trên. Replay REPRO_R2/R3/AUDIT_R5. |
| `temporary-artifacts-not-cleaned` | Thành công, lease bị bác và review bị bác đều còn 0 thư mục canon và 1 worktree chính. [REPLAY/CLEANUP_R4.jsonl](REPLAY/CLEANUP_R4.jsonl). |

## Đối chiếu `nghiem_thu` r2

Tên dưới bỏ tiền tố `r812_`. “Đạt” ở các bullet cụ thể nghĩa là đã chạy ca và đột biến r812 của đúng yếu tố. Không lấy việc có tên ca làm bằng chứng đủ cho toàn M1/M2.

| mục | ca | đo trên head |
|---|---|---|
| Lease chỉ ref cục bộ | `lease_chi_o_ref_cuc_bo` | Đạt; ls-remote có răng. |
| Spec lệch hash, byte nguyên | `dac_ta_lech_bam` | Đạt. |
| Init → awaiting_lease; Ctx.cap_lease → leased/false | `duong_cu_luon_false` | Đạt cả hai chiều, có mutant init. |
| True không quay về đường cũ | `true_khong_quay_ve_duong_cu` | Đạt, byte nguyên. |
| Thiếu kích hoạt; shallow; hai dòng khai | `khong_kich_hoat_la_false`, `nong_la_false`, `hai_dong_khai_la_false` | Đạt. Điều kiện tên ADR trong tệp kích hoạt còn thiếu ca riêng. |
| Workflow chưa đăng | `lease_chua_comment_workflow`, `r6_workflow_*` | Các yếu tố hiện có đạt; **URL sai host/prefix chưa bị bác**. |
| Gỡ lease H; gỡ người giữ | `lease_h_hong`, `prompt_path_thu_muc`, `nguoi_giu_*` | Đạt. |
| Canon thiếu dependency | `canon_vang_phu_thuoc`, `r5_lease_canon_hong`, `r6_api_*` | Đạt; có cả tệp vắng, nội dung hỏng, API không dùng được. |
| Spec chỉ tại lease OID | `dac_ta_chi_tai_lease_oid`, `bia_mo_hai_chieu_tai_lease_oid` | Đạt. |
| required_checks falsy sai kiểu | `required_checks_falsy` | Đạt. |
| Approve còn P1; hạng PX; slug newline | `approve_kem_lop_p1`, `hang_px`, `slug_xuong_dong` | Đạt; fullmatch và miền đóng có răng. |
| Verdict path/blob vắng | `verdict_path_khong_ton_tai` | Đạt. `verdict_blob_khong_co` thực tế đo **hash sai**, không thay ca path vắng. |
| Receipt lệch surface/transport | `bien_nhan_lech_surface`, `bien_nhan_lech_transport`, `executor_*_lech_lease` | Đạt chốt. Ca transport reviewer đo **thiếu trường**; replay R1/R2 đo thêm giá trị thực sự sai. |
| Chỉ generation/packet/spec_hash khác | `bien_nhan_lech_generation`, `bien_nhan_lech_packet`, `bien_nhan_lech_spec_hash` | Đạt I10 ở receipt. **Packet của lease** chưa được cùng các ca này bảo vệ. |
| Receipt changes_requested/blocked, CLI approve | `verdict_changes_requested`, `verdict_blocked` | Đạt cả hai. |
| AG/Gemini hợp lệ | `executor_ag_qua_cli`, `r6_family_*` | Đạt qua CLI/H thật; không dùng riêng predicate hash giả để kết luận. |
| Âm dùng slug ngoài bảng | `slug_ngoai_bang_lop`, `verdict_am_dung_bang_lop` | Đạt cả âm bị bác và âm hợp lệ. |
| Lop rỗng → approved_pending | `duong_moi_du_dieu_kien` | Đạt H thật. |
| Legacy đường cũ | `duong_cu_luon_false`, `khong_kich_hoat_la_false` và nền legacy | Đạt trên Linux. |
| Trần attempt chặn mở, cho khép | `cua_khep_luot_van_chay`, `tran_vong_cua_khep_ghi_ket_qua` | Đạt. |
| Input hỏng ở trần, byte nguyên | `cua_khep_luot_van_chay`, `tran_vong_dau_vao_hong_khong_ghi` | Đạt. |
| M2 role/assurance đúng lease | `r5_review_role`, `r5_review_assurance` | Đạt; hai mutant lượt 5 đã bị giết. |
| M1 loại trừ hai đường; packet lease; identity lease↔init; tên ADR kích hoạt | **THIẾU bảo vệ độc lập trong candidate** | Bốn mutant kiểm toán sống 115/115. HINT bổ sung ca/mutant. |

## I1–I11 và M1/M2/M4/M5

| bất biến/mục tiêu | kết quả |
|---|---|
| I1 / M2 | approved_pending qua schema và Git của receipt H; true không vào accepted theo đường approve cũ. Đạt trong các luồng đã đo. |
| I2 / M1 | H snapshot và holder Đ có chốt thật. **R chưa định danh đầy đủ URL issue**, lớp mở. |
| I3 | Hạng, slug, bảng lớp rỗng và required checks có chốt. **Đầu vào cờ có mặt/rỗng bị gộp**, lớp schema còn mở. |
| I4 | Các đường bị bác đã đo giữ byte, kể cả ở trần. Chưa thấy đường mới ghi state rồi báo từ chối có kiểm soát. **Cờ trộn rỗng và URL sai lại được nhận, ghi state**. Không gọi chúng là traceback hoặc ghi rồi từ chối. |
| I5 / M4 | `_xet_dung` gom các điều kiện dừng; cửa khép ADR-0054 ghi sổ trước trần. Lời gọi record-lease trước validation hiện không xét điều kiện nào, không tạo finding chỉ vì vị trí dòng. |
| I6 | R2 không thêm cửa quyền phái sinh của #813–#815. Không đòi triển khai các cửa đó. |
| I7 | Ngoài phạm vi, #834. |
| I8 | Họ model lease và receipt, tuple identity, alias receipt đã đúng. **Chuẩn hoá provider phía lease còn thiếu**. |
| I9 | Init, lease/review cũ và nền legacy Linux đạt. Không có kết quả Windows thực; skipped ghi riêng. |
| I10 | Tuple receipt/role/lease ID có chốt; kiểm packet lease đúng nhưng **chưa có ca bảo vệ**. |
| I11 | Mọi verdict ADR-0054 qua predicate H chung; ID đi vào counter phải có trong bảng reviewer. Không thấy tái phát ở record-review. |
| M5 | Protocol thêm approved_pending có điều kiện ADR-0054 và trỏ accept sang #834; không thêm accept vào parser. Đạt. |

## Suite, gate và kích thước

Đã chạy `cp -a /home/user/rv812 /tmp/rv812-r7-suite`, rồi `python3 /tmp/rv812-r7-suite/.claude/dev/packet_loop_test.py`:

- **rc=0; `nền: 520/520 đạt · BỎ QUA: 1`; `TỔNG: ĐẠT`.**
- 521 ca khai báo; **263/263 mutant đo được bị giết** trong tổng 264 mutant. Một ca `luong_canonical_chay_that` và mutant tương ứng chỉ chạy Windows bị skipped, không tính là đã đo/đã giết.
- **115/115 ca r812 xanh; 96/96 mutant r812 khai báo bị giết**; không có r812 skipped. Bốn mutant kiểm toán riêng sống được báo ở lớp coverage, không bị con số mutant candidate che khuất.

[SUITE.log](SUITE.log), [SUITE_RESULT.json](SUITE_RESULT.json), [SUITE.exit](SUITE.exit).

`doctrine-scan --root /tmp/rv812-r7-suite`: **rc=0**, 10 tệp, 0 chỗ chép doctrine. `adr-song --root /tmp/rv812-r7-suite`: **rc=0**, 53 ADR/53 dòng, khớp 1–1, ngoại lệ 0016 có sẵn. [DOCTRINE.log](DOCTRINE.log), [ADR.log](ADR.log); mã thoát lưu riêng trong tệp `.exit`.

`git -C KHO diff --numstat 4c7c298 HEAD`:

| đường dẫn | thêm | xoá |
|---|---:|---:|
| `.claude/dev/packet_loop.py` | 391 | 40 |
| `.claude/dev/packet_loop_test.py` | 649 | 0 |
| `docs/PROTOCOL_DA_PHIEN.md` | 4 | 0 |
| **3 đường dẫn** | **1044** | **40** |

Chủ kho đã cho vượt 450; không tính finding kích thước.

## HINT và giới hạn xác minh

[HINT.patch](HINT.patch) là diff gợi ý từ cây riêng trên exact head dòng 1, chỉ chạm hai tệp Python trong write set. **Chưa áp/chạy trên KHO.** Executor tự tái dẫn xuất, tự đo và chịu trách nhiệm tích hợp. `git apply --check` trên bản sao exact head: **rc=0**. [HINT_APPLY_CHECK.log](HINT_APPLY_CHECK.log).

Trên sản phẩm HINT cuối, **137/137 ca r812 xanh; 105/105 mutant r812 theo định nghĩa cuối bị giết tại ca đích**. Trên exact head, 22 ca mới cho **14 ca đỏ đúng lỗi sản phẩm** (7 cờ rỗng, 3 URL, 4 identity lease); 8 ca còn lại xanh, gồm các chốt sản phẩm đúng đang thiếu bảo vệ. [HINT_FINAL_VERIFY.jsonl](HINT_FINAL_VERIFY.jsonl), [HINT_RESULT.json](HINT_RESULT.json).

Việc thêm strip ở `_ten_provider` khiến mutant cũ `r812_r5_raw_provider` chỉ bỏ strip ở caller trở thành tương đương: hàm dùng chung còn strip. Bản HINT cuối sửa mutant thành phối hợp bỏ hai lớp chuẩn hoá của **cùng một yếu tố**; ca receipt vẫn đỏ đúng rc=11/provider-reviewer. Đã đo lại cả nhóm lease provider bốn chiều: baseline xanh, bỏ strip chung thì đều đỏ đúng rc=2. [HINT_MUTANT_DELTA_R7.jsonl](HINT_MUTANT_DELTA_R7.jsonl). Log lần đầu giữ nguyên để thấy vì sao phải cập nhật định nghĩa mutant; kết quả cuối dùng phép đo delta thay cho kết quả mutant tương đương ấy. Không thay mã sản phẩm giữa hai phép đo.

**not_run:** chưa chạy toàn bộ suite legacy trên HINT. Kết quả suite đầy đủ thuộc exact head candidate; kết quả HINT không thay verdict của candidate.

Không tự soạn phản chứng kiểu đường dẫn thoát cây, tên tệp byte thô, liên kết hay argv quá lớn. Các dạng này chỉ chạy lại qua ca r812 đã có. Nếu mở rộng thêm hướng đó, executor cần tự viết ca: giữ baseline H thật, chỉ đổi một giá trị đường dẫn/encoding/kích thước, yêu cầu rc có kiểm soát, state nguyên byte; gỡ đúng chốt phải làm ca đỏ. Không tính hướng chưa đo thành finding.

## Ngoài phạm vi r2

- **#834**: `accept`, I7, readback CI/run-attempt/connector; các lớp lượt 1 `connector-verdict-incomplete`, `ci-attempt-provenance-missing`, `conflicting-evidence-overwrite` và phần connector của `findings-not-receipt-bound`. Không tính hạng ở đây.
- **#813–#816**: mở lại/chờ chủ kho/checkpoint, vòng P3, generation tiếp, ghi đẩy và kích hoạt. Không yêu cầu triển khai trong #812 r2.
