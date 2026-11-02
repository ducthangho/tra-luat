Reviewed commit: 4504b80e67e4c3c8e967be92212842eb835c6e85
Verdict: changes_requested — P0=0 P1=1 P2=2 P3=0

Review độc lập, offline, **3 lớp còn mở** trong revision 2. Ngưỡng chủ kho là hết P0–P3. Kho `/home/user/rv812` chỉ được đọc; chạy chương trình, tạo fixture, mutation và thử hint trên bản sao dưới `/tmp`. Không gọi GitHub, push kho nguồn, merge hay dùng reviewer con. Fetch/push của fixture chỉ tới bare origin cục bộ.

## Định danh và phạm vi

- Đã kiểm `git -C /home/user/rv812 rev-parse HEAD`, đúng SHA dòng 1; tree `c122a2c0accf61111b61c43d0d5f73d4d8b11b2b`; clone đầy đủ, không shallow; base `4c7c29858220ae575bebc5e0a343842cd3db4546` là tổ tiên. Bằng chứng máy: [PREFLIGHT.json](PREFLIGHT.json).
- Đã đọc diff base→head, `783463b`→head, `97f3bc1`→head, `4686672`→head; cả ba verdict trước, mã tái hiện và hai validator được gọi.
- Đọc đặc tả qua `git show origin/ops/wp812-spec:…`, tự tính sha256: r2 `d64987461d89429ca97230ec5e796bf987bb9383d765279543e6a7fc14513eef`; phần chung `4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0`. Cả hai khớp. Lease `ops/leases/wp812-r2-g3-claude.yaml`: revision 2, generation 3, executor Claude, reviewer Codex, sensitive/cross_approved. Đã đọc #834 để giữ ranh giới r2.
- Reviewer thực: Codex/OpenAI trong phiên API này, thực thi shell Linux qua `exec_command`, transport máy. Không có telemetry để chứng minh launcher CLI/Desktop, model hoặc effort của từng request; không suy identity từ tài khoản GitHub, không tự phát biên nhận assurance. Không dùng context executor.
- Chỉ thị trực tiếp của chủ kho cho vượt 450 dòng và đòi hết cả P1/P2/P3 được áp dụng; không lấy giới hạn kích thước cũ làm finding. Trần lời gọi Codex 8 giữ nguyên; không gọi thêm model/reviewer con trong lượt này.

## Bảng lớp còn mở

`pl` = `.claude/dev/packet_loop.py`; `test` = `.claude/dev/packet_loop_test.py`. Số dòng trên exact head. Đếm theo lớp nguyên nhân, không cộng mỗi biểu hiện thành một finding.

| slug | hạng | biểu hiện (file:dòng) | phép đo đã chạy | hướng vá |
|---|---|---|---|---|
| `lease-holder-scope-incomplete` | P1 | pl:2440, pl:2515, pl:2521, pl:2533, pl:2543 | `SYMLINK_R3`: baseline và chỉ thêm đối thủ qua alias đều **rc=0/leased**, dù `resolve()` chứng minh cùng tệp trong fixture. `PROBE_R4`: effective che tập khai, tập khai rỗng, own path có `.`/`..`/glob đều **rc=0/leased**. | Đo scope đối xứng `write_set ∪ effective_write_set` của cả hai bên; tập khai phải không rỗng để không bỏ toàn bộ phép Đ. Chuẩn hóa và kiểm miền **mọi đường trước khi so**, kể cả không có đối thủ; resolve symlink/parent và kiểm vẫn trong worktree. Giữ H snapshot và phép Đ canon. HINT có ca symlink, own union, tập rỗng và miền đường dẫn. |
| `new-input-schema-incomplete` | P2 | pl:2455, pl:2509, pl:2592, pl:2594, pl:2615 | `PROBE_R4`: thêm riêng top-level `model_family: []`/`executor_model_family: false`, hoặc `model_executor_identity: false` vẫn **rc=0/approved_pending**. Context chỉ đổi executor surface hoặc transport thành list cũng được approve. `PARSER_R4`: metadata YAML lồng sâu gây **RecursionError/traceback, rc=1**, byte state nguyên. | Kiểm kiểu/miền trên toàn bộ nguồn mà canon thực sự tra, gồm khối identity, top-level fallback và các bí danh; có mặt sai kiểu không phải vắng. Kiểm surface/transport lồng trong `_nc_hop_le`, trước lưu và khi đọc. Chuyển lỗi parser đầu vào thành rc có kiểm soát. HINT dùng bảng nguồn của canon và bổ sung chốt tương ứng. |
| `required-mutation-coverage-missing` | P2 | test:6003, test:6102, test:6153, test:6166, test:6169, test:6174 | Nền có **63 ca r812**; **61 mutant r812** khai báo đều giết đúng ca đích. Nhưng mutant bỏ uniqueness slug **sống 63/63**. Bảng candidate vẫn không có mutant r812 nhắm init; ca dependency thực sự vắng, verdict path vắng và verdict âm hợp lệ chưa có mutant chọn làm đích. Reviewer đã chạy ba mutant bổ sung: các ca ấy đỏ đúng chốt. | Khóa từng mục nghiệm thu bằng mutant r812 đúng yếu tố; thêm ca slug trùng và các biểu hiện scope/schema ở trên. Dùng baseline H/CLI thật cho nghiệm thu. HINT bổ sung ca/mutant và điều chỉnh mutant khi có hai chốt cùng bảo vệ một yếu tố. |

### Scope: các chiều cùng lớp đã quét

Các probe dùng lease đã commit vào remote fixture, H check, holder canon và comment workflow; không thay validator để làm xanh. Đã chạy lại chuẩn hóa case-fold, dấu phân cách, Unicode NFC/NFD và `./`: các xung đột cũ nay bị rc=7, byte state nguyên. Effective expansion hợp lệ của chính ứng viên nay rc=0: lỗi bắt oan lượt 3 đã hết.

Nhưng symlink từ lượt 3 vẫn chưa được xử lý: `alias → x` hoàn toàn trong fixture, `alias/a.py` và `x/a.py` là cùng tệp thật, chỉ thêm lease giữ alias vẫn leased. Không cần dựng đường thoát cây hay đọc dữ liệu nhạy cảm để chứng minh lỗi này.

Đổi vòng hỏi Đ từ `ws` sang `l["write_set"]` để nhận effective expansion còn mở chiều mới: ứng viên khai `write_set=["x/a.py"]`, `effective_write_set=["y/b.py"]`, đối thủ giữ prefix `x/`. Phép Đ khớp chính xác chỉ thấy ứng viên ở `x/a.py`; phép so bổ sung chỉ xét `y/b.py`, nên bỏ mất xung đột ở tập khai. Baseline không đối thủ rc=0; chỉ thêm đối thủ vẫn rc=0. Cùng nguyên nhân, `write_set=[]` và effective không rỗng làm vòng Đ chạy **0 lần**, nhưng lease vẫn được nhận.

Chuẩn hóa chỉ được gọi bên trong `any(_giao(...))` với lease cạnh tranh. Khi không có đối thủ, `effective_write_set=["x/../y/b.py"]` không được kiểm miền dù `_chuan_duong` có chốt `..`. Own path `./x/a.py` và glob `x/*.py` cũng được nhận, trái miền write set của protocol §5. Đây là cùng lớp phạm vi/thẩm quyền, không thêm hạng riêng cho từng cách viết.

**Vá ở đâu/cách vá:** helper biểu diễn đường dẫn và hai vòng ở M1. **Ca khóa:** baseline alias không đối thủ phải nhận; thêm đối thủ cùng đích phải bác; effective mở rộng hợp lệ vẫn nhận; effective không được che tập khai; tập khai rỗng và miền sai phải bác, byte nguyên. **Nguy cơ của bản vá:** resolve sau case-fold có thể tra sai đường trên Linux; phải resolve cách viết thật trước rồi mới chuẩn hóa để so. Tránh bỏ H/Đ canon hoặc chặn oan mọi effective expansion. HINT giữ tên khai và đích resolved để đo cả hai chiều.

### Schema: phần đã vá và phần còn lọt

Các phản chứng lượt 3 về branch rỗng, provider list/dict và family sai kiểu **bên trong** identity nay bị bác đúng rc=2/11, byte nguyên, không traceback. `_ten_provider` không còn TypeError với list/dict.

Tuy nhiên, canon `_nguon_tra_model`/`_giai_ho_va_bc` còn đọc model family, model, bằng chứng và bí danh ở top-level. Chốt kiểu mới chỉ duyệt khối reviewer/executor và top-level `executor_provider`. Đã quét `model_family`, `ho_model`, `canonical_model`, `model` cùng các khóa `executor_*`: list/dict/bool đều bị đọc như không khai, fallback theo provider và vào approved_pending. Khối executor sai kiểu cũng bị thay thành `{}`. Bằng chứng tham chiếu/bí danh có mặt sai kiểu cũng chưa được kiểm đầy đủ; toàn bộ kết quả ở [PROBE_R4.jsonl](PROBE_R4.jsonl).

`_nc_hop_le` kiểm tập khóa của identity nhưng không kiểm giá trị surface/transport. Chỉ thay **một** giá trị executor thành `[]` vẫn qua `_load`; receipt baseline không khai tuple executor riêng nên `mei.get(k, nc[...])` lấy chính giá trị hỏng ấy làm mặc định, phép so tự bằng nhau và approve. Không phải lỗi chỉ ở phần context để dành cho #834: nó ảnh hưởng ngay cửa review của #812.

Parser lease chỉ bắt `yaml.YAMLError`. Probe thêm một trường metadata thông thường với 700 mức list, giữ nguyên các trường lease khác, gây RecursionError trước chốt lược đồ; rc=1 với traceback thay vì từ chối có kiểm soát. Byte state giữ nguyên, **không** gọi đây là ghi state trước từ chối.

**Vá ở đâu/cách vá:** `_du_dieu_kien_approve`, `_nc_hop_le` và chỗ parse lease. **Ca khóa:** H thật chỉ thêm top-level family sai kiểu; chỉ thay hình dạng khối executor; chỉ đổi context surface; parser sâu phải trả rc có kiểm soát. **Nguy cơ của bản vá:** không biến optional field vắng thành field bắt buộc, không siết đường legacy; dùng đúng bảng nguồn của canon để tránh hai schema trôi lệch. HINT giữ baseline receipt không khai tuple executor và các cấu hình AG hợp lệ.

### Mutation: có răng ở đâu, thiếu ở đâu

[AUDIT_R4.jsonl](AUDIT_R4.jsonl) ghi assertion của **từng mutant r812**, không chỉ con số từ harness. Tất cả 61 mutant khai báo giết ca đích bằng rc/trạng thái/byte ở đúng chốt; không có lỗi import/setup hoặc traceback vô can được tính thành bằng chứng. Ba mutant riêng bổ sung cũng giết ca đích: bỏ chốt dependency vắng làm lease rc=0; bỏ Git anchor làm verdict path vắng rc=0; chặn verdict âm hợp lệ làm baseline âm bị rc=11.

[REPLAY/AUDIT_R3.jsonl](REPLAY/AUDIT_R3.jsonl): bỏ so receipt SHA, lease ID hoặc transport executor nay đều bị đúng ca mới giết (**62/63** còn xanh). Bỏ uniqueness slug vẫn **63/63 xanh**. Bỏ phép so khác họ ở caller cũng sống, nhưng canon `_thieu` còn kiểm khác họ: đó là mutant tương đương, **không** lấy làm finding coverage. Mutant đổi init sang leased giết assertion `awaiting_lease` đúng nghĩa, nhưng candidate vẫn thiếu khóa mutant r812 nhắm chốt ấy.

**Vá ở đâu/cách vá:** bảng ca/MUTANTS và kiểm kê target của r812. **Ca khóa:** thiếu dependency thật, verdict path thật sự vắng, baseline âm hợp lệ, init và slug trùng. **Nguy cơ của bản vá:** một yếu tố có hai chốt cần mutation phối hợp, tránh mutant sống tương đương hoặc đỏ vì setup thay vì yếu tố cần đo. Không đòi mọi ca phụ phải có mutant nếu nó không đại diện thêm một mục nghiệm thu; các thiếu hụt bắt buộc nêu dưới đây mới là căn cứ của lớp.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn lượt 3: `origin/ops/wp812-g2-reviews:ops/reviews/wp812-r2-g3-exec-review-3-codex/`, SHA `468667238e53e77580e4be62e0b8ed5753a75cd9`. Đã chạy lại **REPRO_R3.py, IDENTITY_R3.py, AUDIT_R3.py, SYMLINK_R3.py** trên bản sao exact head, chỉ thay đường dẫn bản sao. Script và kết quả ở [REPLAY](REPLAY/); bản nguyên gốc ở [PRIOR/R3](PRIOR/R3/).

| lớp lượt 3 | nhãn bắt buộc | bằng chứng trên head này |
|---|---|---|
| `lease-holder-scope-incomplete` | **vá sinh lỗi mới** | Bốn dạng chuẩn hóa chuỗi bị bác đúng; effective expansion hợp lệ đã nhận. Symlink cũ vẫn lọt; đổi vòng Đ sang tập khai mở thêm chiều effective che tập khai và vòng Đ rỗng. |
| `identity-compared-by-provider-family` | **đã vá thật** | CLI đầy đủ AG/Gemini và AG/openai + receipt họ canon gpt đều rc=0/approved_pending; `_thieu=[]`, `_neo_git=([],[])`. Ba phép đổi riêng provider/surface/transport của lượt 2 vẫn rc=11. Mutant suy họ theo provider bị ca CLI giết. |
| `new-input-schema-incomplete` | **vá hờ** | Branch/provider/family lồng cũ đã đóng. Top-level fallback, hình dạng khối executor, surface/transport context và ngoại lệ parser vẫn chưa được xử lý đầy đủ. |
| `required-mutation-coverage-missing` | **vá hờ** | Ba mutant SHA/lease ID/transport cũ đã bị giết; dependency vắng thật và AG CLI đã có ca. Uniqueness vẫn chưa có ca, một số mục bắt buộc vẫn chưa có mutant r812 chọn đúng ca. |

Đã chạy lại phần r2 áp dụng của `REPRO.py` lượt 1, giữ nguyên probe và H thật, bỏ đoạn accept thuộc #834. Probe doctor được chạy lại qua runner lượt 2 sau một verdict âm hợp lệ để có cửa begin hợp lệ. Đã chạy thêm `REPRO.py`, `EXTRA_PROBES.py`, `IDENTITY_AB.py` của lượt 2; không chỉ đọc verdict cũ.

| lớp lượt 1–2 còn trong r2 | kết luận ở lượt này |
|---|---|
| `receipt-validation-incomplete` | **Đã vá thật** với các phản chứng gốc: ChatGPT giả Codex, transport sai, mỏ neo vắng đều rc=11/byte nguyên; H baseline qua cả schema và Git. Sai kiểu mới đếm chung lớp schema ở trên. |
| `identity-compared-by-provider-family` | **Đã vá thật**, như bảng lượt 3. AG với cả hai họ được khai hợp lệ đạt qua CLI. |
| `findings-not-receipt-bound` — record-review | **Đã vá thật**: verdict âm không H hoặc slug ngoài bảng đều bị bác; âm đúng bảng chạy được. Predicate dùng chung cho hai đường vẫn có mutation bảo vệ. |
| `stop-validation-order` | **Đã vá thật** trên đường đã đo: bad H ở trần vòng rc=11/byte nguyên; doctor hỏng ở trần attempt rc=10/byte nguyên; approve cửa khép rc=0/approved_pending. Âm hợp lệ ở trần ghi đủ 2 review, đóng attempt rồi rc=3/blocked-rescue. |
| `lease-checks-worktree` | **Đã vá thật**: spec/prompt vắng worktree vẫn nhận; bia mộ hai chiều qua H trên snapshot Git đúng lease OID vẫn nhận. Mutant trở lại worktree hoặc snapshot mất Git bị giết. |
| `new-input-schema-incomplete` | **Còn mở** như bảng lớp; required-check falsy và slug newline không tái phát. |
| `required-mutation-coverage-missing` | **Còn mở** như bảng lớp. Các mutant H/schema, ba phép land-OID và thứ tự/cửa khép của lượt 1–2 hiện có ca giết đúng chốt. |
| `temporary-artifacts-not-cleaned` | **Đã vá thật**: kiểm riêng thành công, H lease bị bác và review bị bác đều còn 0 thư mục canon trong TMPDIR riêng, 1 worktree chính. Ca cleanup và mutant của candidate cũng đạt. Xem `CLEANUP_R4.jsonl`. |

## Đối chiếu `nghiem_thu` revision 2

Tên dưới đây bỏ tiền tố chung `r812_`. “Đạt” nghĩa là đã chạy ca, đọc assertion dưới mutation và thấy đỏ đúng yếu tố. Baseline review chung được kiểm độc lập bằng `_thieu` và `_neo_git`; không dùng accept/CI/connector để lấp mục r2.

| mục bắt buộc | ca tương ứng | kết quả |
|---|---|---|
| Lease chỉ ref cục bộ | `lease_chi_o_ref_cuc_bo` | Đạt; mutant ls-remote bị giết. |
| Spec lệch băm, byte nguyên | `dac_ta_lech_bam` | Đạt; mutant băm và ghi sớm bị giết. |
| Init chưa lease → awaiting_lease | `duong_cu_luon_false` | Assert đúng; **THIẾU mutant khóa r812 nhắm init**. Mutant reviewer giết đúng assertion ấy; mutant legacy toàn suite có bảo vệ. |
| Ctx.cap_lease → leased/false | `duong_cu_luon_false` | Đạt. |
| True không quay đường cũ | `true_khong_quay_ve_duong_cu` | Đạt, byte nguyên. |
| Thiếu kích hoạt → false | `khong_kich_hoat_la_false` | Đạt; review đi accepted legacy. |
| Shallow → false | `nong_la_false` | Đạt. |
| Hai dòng khai → false | `hai_dong_khai_la_false` | Đạt. |
| Chưa comment workflow | `lease_chua_comment_workflow` | Đạt. |
| Gỡ H check làm ca đỏ | `lease_h_hong` | Đạt. |
| Gỡ holder check làm ca đỏ | `nguoi_giu_khac`, `nguoi_giu_prefix_giao_nhau`, `nguoi_giu_effective_giao_nhau` | Đạt các cách viết đã khóa; chưa bảo vệ symlink, union own/empty và miền đường dẫn; sản phẩm còn P1. |
| Canon thiếu dependency thật | `canon_vang_phu_thuoc` | **Đã có ca đúng mục**, xóa AGENTS khỏi origin/master; **THIẾU mutant candidate chọn ca này**. Mutant reviewer bỏ chốt đọc nguồn làm ca đỏ rc=0 thay vì 8. `canon_thieu_nguon` cũ đo nội dung hỏng, khác mục. |
| Spec ở lease OID, vắng worktree | `dac_ta_chi_tai_lease_oid` | Đạt; có thêm ca snapshot Git/bia mộ. |
| Required-check sai kiểu falsy | `required_checks_falsy` | Đạt. |
| Approve còn P1 | `approve_kem_lop_p1` | Đạt. |
| Hạng PX | `hang_px` | Đạt. |
| Slug newline | `slug_xuong_dong` | Đạt. |
| Verdict path/blob không tồn tại | `verdict_path_khong_ton_tai` | Ca đúng mục xanh; **THIẾU mutant candidate chọn ca này**. Mutant reviewer bỏ neo làm ca đỏ rc=0 thay vì 11. `verdict_blob_khong_co` cũ chỉ đo digest sai. |
| Receipt lệch surface | `bien_nhan_lech_surface` | Đạt. |
| Receipt lệch transport | `bien_nhan_lech_transport` | Đo thiếu trường; có răng. Giá trị transport khác cũng đã đo bằng probe cũ; executor có thêm ca riêng. |
| Chỉ generation khác | `bien_nhan_lech_generation` | Đạt. |
| Chỉ packet khác | `bien_nhan_lech_packet` | Đạt. |
| Chỉ spec_hash khác | `bien_nhan_lech_spec_hash` | Đạt. |
| H changes_requested, CLI approve | `verdict_changes_requested` | Đạt. |
| H blocked, CLI approve | `verdict_blocked` | Đạt. |
| AG/Gemini hợp lệ | `executor_ag_qua_cli` | **Đạt mới**: CLI đầy đủ, spec hash thật, cả Gemini và OpenAI/gpt. Ca `executor_antigravity_hop_le` cũ vẫn là predicate với hash giả `s*64`, không dùng ca đó làm bằng chứng nghiệm thu luồng. |
| Verdict âm, slug ngoài H | `slug_ngoai_bang_lop` | Đạt; baseline âm đúng bảng ở `verdict_am_dung_bang_lop`, nhưng **ca dương ấy chưa có mutant candidate chọn làm đích**. Mutant reviewer chặn âm hợp lệ làm đỏ đúng membership. |
| Lớp rỗng → approved_pending | `duong_moi_du_dieu_kien` | Đạt, H thật. |
| Packet legacy đi đường cũ | `duong_cu_luon_false`, `khong_kich_hoat_la_false` | Đạt các luồng hợp lệ đã đo; nền legacy không có ca đỏ. |
| Trần attempt chặn mở, cho khép | `cua_khep_luot_van_chay`, `tran_vong_cua_khep_ghi_ket_qua` | Đạt; có cả ADR-0054 ở trần vòng. |
| Input hỏng ở trần, byte nguyên | `cua_khep_luot_van_chay`, `tran_vong_dau_vao_hong_khong_ghi` | Đạt; mutant thứ tự kiểm bị giết. |

Ba phép land-OID độc lập có các ca `oid_khong_chua_adr`, `oid_khong_dua_adr_vao`, `oid_ngoai_first_parent` và mutant tương ứng, đều có răng. Ba chốt mới SHA, lease ID, executor transport cũng đã được khóa. Không gộp sự tiến bộ này với các thiếu hụt còn mở.

## I1–I11 và M1/M2/M4/M5

| bất biến/mục tiêu | kết quả trong phạm vi r2 |
|---|---|
| I1 / M2 | approved_pending phải qua H/schema/Git; state true không đi approve→accepted cũ. Sai kiểu còn được chấp nhận như lớp schema. |
| I2 / M1 | H trên snapshot Git, ref remote và R workflow có chốt thật; phép hợp thành holder/scope còn P1. |
| I3 | Miền P0–P3, fullmatch slug và lớp rỗng đúng. Giá trị identity sai kiểu vẫn có đường fallback. |
| I4 | Các reject cũ ở trần giữ byte; input schema hỏng còn được nhận, YAML sâu còn traceback. Không thấy đường mới ghi state rồi trả lỗi đầu vào có kiểm soát trong các probe đã chạy. |
| I5 / M4 | Một `_xet_dung` gom attempt/review/same-failure/rescue. Cửa khép ADR-0054 ghi kết quả trước trần. Lời gọi ở record-lease trước validate hiện là no-op, không báo finding chỉ từ vị trí dòng. |
| I6 | Không thêm cửa quyền phái sinh trong r2; không đòi #813–#815. |
| I7 | Ngoài phạm vi r2, #834. |
| I8 | So họ lease khai đã sửa thật; provider/surface/transport lệch được bác. Lỗi kiểu dữ liệu đếm ở lớp schema, không báo lặp lớp identity. |
| I9 | Init/lease legacy/review legacy và nền cũ đạt trên Linux; phần Windows ghi skipped riêng. |
| I10 | Chốt role/packet/generation/SHA/spec_hash/lease ID hiện có; các ca tuple và mutant chạy đúng. |
| I11 | Verdict âm qua cùng H, slug phải trong bảng reviewer; không còn đường tự đặt slug trong record-review đã đo. |
| M5 | Protocol:241 có approved_pending có điều kiện ADR-0054, trỏ accept sang #834. Đạt; parser r2 không thêm accept. |

## Kết quả chạy và kích thước

- Đã chạy `cp -a /home/user/rv812 /tmp/rv812-r4-suite`, rồi `python3 /tmp/rv812-r4-suite/.claude/dev/packet_loop_test.py`: **rc=0**; **`nền: 468/468 đạt · BỎ QUA: 1`**; **`TỔNG: ĐẠT`**. Tổng khai báo **469 ca / 229 mutant**. **228 mutant đo được đều bị giết**, gồm đủ **61/61 mutant r812**. Một ca `luong_canonical_chay_that` và mutant `luong_canonical_chay_that_dao_os_name` chỉ dành cho Windows bị **skipped**, không tính là đã giết; không có ca/mutant r812 bị bỏ qua. Toàn văn [SUITE.log](SUITE.log), kết quả cấu trúc [SUITE_RESULT.json](SUITE_RESULT.json).

- `python3 /tmp/rv812-r4-suite/.claude/dev/packet_loop.py doctrine-scan --root /tmp/rv812-r4-suite`: **rc=0**, 10 tệp, 0 chỗ chép doctrine.
- `python3 /tmp/rv812-r4-suite/.claude/dev/packet_loop.py adr-song --root /tmp/rv812-r4-suite`: **rc=0**, 53 ADR/53 dòng, khớp 1–1, ngoại lệ trạng thái 0016 đã có. [GATES.json](GATES.json).
- Các runner replay, probe riêng, audit được chạy trên bản sao; đầu ra stdout/stderr được lưu riêng. `PARSER_R4.jsonl` cố ý ghi rc=1 của **sản phẩm** làm bằng chứng finding; runner của reviewer vẫn hoàn tất. Không đổi một phép không chạy thành pass.

`git -C /home/user/rv812 diff --numstat 4c7c298 HEAD`:

| đường dẫn | thêm | xóa |
|---|---:|---:|
| `.claude/dev/packet_loop.py` | 312 | 35 |
| `.claude/dev/packet_loop_test.py` | 366 | 0 |
| `docs/PROTOCOL_DA_PHIEN.md` | 4 | 0 |
| **Tổng: 3 đường dẫn** | **682** | **35** |

Vượt 450 được chủ kho cho phép ở #812 issuecomment-6250555271 theo chỉ thị review này; **không tính finding**.

## HINT và giới hạn xác minh

[HINT.patch](HINT.patch) là diff gợi ý trên exact head, chỉ chạm hai tệp Python trong write set. Sinh và chạy trong cây riêng của reviewer; **chưa áp/chạy trên cây thật**. Executor cần tự tái dẫn xuất, tự đo và chịu trách nhiệm tích hợp. Không có nội dung pháp lý hoặc payload nhạy cảm được soạn để thử.

`git apply --check` trên bản sao đúng SHA dòng 1: **rc=0**, không áp vào KHO ([HINT_APPLY_CHECK.json](HINT_APPLY_CHECK.json)). Trên cây hint, **74/74 ca r812 xanh**; **73 mutant r812 đầu tiên** đều giết đúng target, sau đó thêm và chạy riêng mutant parser sâu thứ **74**, cũng bị giết vì quay lại đúng RecursionError của chỗ parse lease. Bằng chứng: [HINT_FINAL.jsonl](HINT_FINAL.jsonl), [HINT_PARSER.json](HINT_PARSER.json). Việc thêm mutant cuối chỉ thêm mục trong bảng test, không đổi mã sản phẩm hay 74 ca nền đã đo. Chưa chạy lại toàn bộ suite legacy trên hint; kết quả toàn suite ở trên thuộc exact head được review.

Hint giữ H canon/snapshot, phép hỏi holder canon, effective expansion hợp lệ, identity AG và đường legacy. Các phần cần chú ý khi tích hợp là ngữ cảnh worktree dùng resolve path, hỗ trợ symlink theo nền và mutation phối hợp khi hai chốt cùng bảo vệ một yếu tố. Kết quả hint không thay kết quả review exact head.

Kiểm cuối: HEAD vẫn đúng SHA dòng 1, `git status --porcelain=v1 --untracked-files=all` rỗng, diff tracked và staged đều rc=0; byte của cả ba tệp review khớp blob HEAD. [READONLY_CHECK.json](READONLY_CHECK.json). Không có thay đổi nào được thực hiện trong KHO.

## Ngoài phạm vi r2

- #834: `accept`, I7, readback CI/run-attempt/connector; các lớp lượt 1 `connector-verdict-incomplete`, `ci-attempt-provenance-missing`, `conflicting-evidence-overwrite` và phần connector của `findings-not-receipt-bound`. Không yêu cầu triển khai hoặc tính hạng ở review này.
- #813: mở lại/chờ chủ kho/checkpoint; #814: vòng P3; #815: generation tiếp; #816: ghi đẩy và kích hoạt ADR-0054. Không mở rộng packet để vá các cửa này.
