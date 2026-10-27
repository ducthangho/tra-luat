Verdict: approve
Reviewed commit: acce679c350adab2afa2c4c151039bf16edb4cc0
Spec sha256: 39b4288959f3889c6c3aad2d24b355c1c02b1462a8854c6a5b00677e81a7ce73; Chung sha256: 4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0

**Kết luận lượt 5: approve về nội dung trên exact head dòng 2; 0 P0/P1/P2, giữ nguyên 2 lớp P3 của lượt 4.** Không phát hiện hồi quy do merge. Hai blob write set giống từng byte head đã approve; master mới không đổi các tệp canon mà cửa H nạp. Verdict này không cấp quyền push, merge, land hoặc kích hoạt ADR-0054.

| slug | hạng P0–P3 | biểu hiện file:dòng | phép đo/tái hiện đã chạy | hướng vá |
|---|---|---|---|---|
| `legacy-p3-failure-counts-retained` | **P3**, giữ quyết định và owner lượt 4 | `.claude/dev/packet_loop.py:672`, `:1207`, `:1229` | State do blob thật `20a2e2b` tạo bằng CLI: approve a-x:P3 có finding-id lưu count1. Đổi sang candidate, vua-p3 rồi cùng slug lên P2: count2/rc3/blocked. State mới bằng candidate: count1/rc0/running. Cả hai có vòng k1/1→0, status rc0. [Probe legacy/fresh](probes/results.json). | Owner **#816**. Giữ nợ, không migration ở #814. Trước kích hoạt kiểm dữ liệu thực; nếu được phép di trú, sửa đồng bộ finding_ids/counts và giữ audit, phân biệt P3 có chứng cứ với P0–P2 thật. Ca khóa: upgrade/fresh cùng slug rồi P2 và reload. Rủi ro: xóa count đơn độc làm hỏng invariant findings; suy hạng thiếu chứng cứ xóa nhầm lỗi thật. |
| `r814-mutation-evidence-incomplete` | **P3**, giữ biểu hiện `duplicate-destination` | `.claude/dev/packet_loop_test.py:9060`, `:9116`; chốt `.claude/dev/packet_loop.py:3064` | Mutant tự dựng bỏ riêng `and len(set(den)) == len(den)` sống **312/312 ca đã chọn**. A/B accept: candidate rc11/bang-noi/nguyên byte, mutant rc0/accepted; oracle riêng AssertionError. Một hàng hợp lệ được cả hai nhận. [Mutant](extra-mutants/duplicate-destination/mutation.json), [A/B](probes/results.json). | Owner executor **Claude #814**, chủ kho định tuyến nợ như lượt 4. Thêm ca đích lặp và mutant bỏ đúng chốt duy nhất đích; giữ predicate sản phẩm đúng. Dùng baseline accept đầy đủ, nguồn rỗng, đích P3 có thật, đủ refs/quyết định. Rủi ro: lỗi nguồn/refs hoặc vòng không giảm có thể che chốt cần đo. Không yêu cầu mở thêm vòng vá chỉ vì nợ này. |

**Lý do phân hạng.** Đây là lượt xác minh merge theo `push_policy`, không có bản vá mới cho hai nợ. Điều khoản riêng của prompt yêu cầu “giữ nguyên hạng và slug … nếu không có thay đổi”, nên không nâng P3 chỉ vì mutant đã biết còn sống. `duplicate-destination` vẫn là thiếu độ phủ trên predicate sản phẩm xử lý đúng ở A/B; legacy vẫn là nợ đã được chuyển #816, không có migration mới trong merge. Không có lỗi hành vi mới do merge, thiếu ca nghiệm thu bắt buộc mới, hoặc lớp mới được mở từ phần không đổi. Luật P3 cho mutant độ phủ mới không được dùng để hạ một lỗi sản phẩm thật.

**Xác minh merge và hợp đồng các cửa.** Đã đọc toàn bộ hunk trong [packet.diff](packet.diff) (`c2d84ea→acce679`) và [master.diff](master.diff) (`4488444→c2d84ea`), gồm cả mã sản phẩm, test và tám tệp master mới. Phạm vi review không lọc theo bảng gợi ý của executor.

| phép đo | bằng chứng |
|---|---|
| Head / tree | `acce679c350adab2afa2c4c151039bf16edb4cc0` / `6f43192a0834c660e2758a9954e0769a0aa98978` |
| Hai cha merge | `5a5c5c1f687f74b73301fe161e332ae6b4c0f779` và `c2d84ea7c20e835968b630a4fb1b8daa29ac12c7` |
| Base mới | `refs/remotes/origin/master` = `c2d84ea7c20e835968b630a4fb1b8daa29ac12c7`; `merge-base --is-ancestor` rc0 |
| Blob product tại head và lượt4 | Cùng `54de38e84b111d5301896abf365523bd4d59a78a` |
| Blob test tại head và lượt4 | Cùng `03b26eff6788eb32bc1d6c9cfc72b2dc0a72a782` |
| Worktree so blob | `git hash-object` của cả hai tệp khớp OID head; clone thường, `.git` là thư mục, detached, không nông, sạch |
| Diff PR | Đúng hai đường dẫn: product +85/−6, test +125/−6; **210 dòng thêm ≤450**; diff-check rc0 |

`44884446f71c89e25f9a72ac58e4f597db63c1ba` là master dùng ở lượt4. So blob tại mốc đó, base mới và head mới: **ops/bien_nhan_v2.py, ops/lease_publish.py, .claude/dev/launcher.py, AGENTS.md, docs/PROTOCOL_DA_PHIEN.md đều không đổi**. Đây là toàn bộ tuple `CANON` ở product:2400; `_canon` lấy các blob ấy từ origin/master và `_du_dieu_kien_approve` dùng validator cùng bảng chuẩn hóa identity. Không có thay đổi schema, nguồn identity hay parser do master mới. [OID và từng command/rc](IDENTITY.json).

Hai adapter `.claude/skills/cross-review/SKILL.md` và `.agents/skills/cross-review/SKILL.md` đổi hướng dẫn đọc model/effort/sandbox từ các trường `run.json`, chỉ công nhận khi trạng thái `DO_DUOC`; header stderr là thông tin phụ. Đây là thay đổi đầu vào **doctrine-scan**, nên đã chạy lại gate trên chính cây merge: 10 tệp/0 chỗ chép, rc0. `adr-song` cũng rc0: 55 ADR/55 dòng, ngoại lệ0016 đã khai. Bốn tệp evidence/provenance #899, release manifest và sửa cô lập biến môi trường trong `scripts/tl_selftest.py` không thay predicate M1–M4 hoặc năm nguồn canon; chúng không nằm trên đường đọc H đã lần trong product. Không nhận tài liệu land #899 làm authority của #814.

**ĐỐI CHIẾU LƯỢT TRƯỚC — giữ lịch sử lớp.**

| lớp / biểu hiện | trạng thái lượt 5 | bằng chứng độc lập trên candidate |
|---|---|---|
| `legacy-p3-failure-counts-retained` | **CHƯA VÁ**, giữ P3/#816 | Upgrade/fresh bằng CLI thật cho count2/count1; cả hai vẫn giữ mốc vòng1 và reload được. |
| `r814-mutation-evidence-incomplete` · duplicate-destination | **CHƯA VÁ**, giữ P3 | Mutant tự dựng sống312/312; A/B xác nhận product từ chối đúng. Không gán đây là hồi quy merge. |
| Cùng lớp · first-map-only | Giữ **ĐÃ VÁ THẬT** | `r814_noi_chi_hang_dau` bị cả rr/ci/accept nhiều hàng bắt; lỗi đều AssertionError đúng oracle. |
| `receipt-map-validation-skipped` | Giữ **ĐÃ VÁ THẬT** | Bốn ca đích không có ở record-review/ci-do/connector/accept đạt; mutant bỏ kiểm chung bị10 ca bắt, mutant bỏ kiểm đích bị4 ca bắt. |
| `finding-lineage-counter-reset` | Giữ **ĐÃ VÁ THẬT** | Các ca nối P2, nguồn P2, đích P2 và nối lại tại ci-do/connector/accept đều từ chối đúng; mutant đúng chốt bị bắt. |
| `p3-mapping-namespace-collision` | Giữ **ĐÃ VÁ THẬT** | Ca nối chuỗi và mutant nguồn còn hiện diện; gộp thuần áp nối hai vòng cho1→1/blocked. |
| `p3-reopen-enters-failure-counter` | Giữ **ĐÃ VÁ THẬT với sự kiện mới** | P3 ở mo-lai cho counts{}; mutant bỏ lọc cho ci-gate:1 và bị oracle bắt. |
| `legacy-p3-milestone-lost` | Giữ **ĐÃ VÁ THẬT phần mốc** | Ca state cũ/mutant đạt; probe nâng cấp blob thật cũng cho k1. Nợ count giữ riêng. |
| `new-command-codepage-matrix-incomplete` | Giữ **ĐÃ VÁ THẬT** | stdout_cp1252 và stdout_cp1258 PASS, gồm vua-p3 thành công có stdout. Chỉ đo Linux với env codepage. |
| M4 · `r813-mutation-evidence-incomplete` | Giữ **ĐÃ VÁ THẬT hai biểu hiện được giao** | Mixed check_refs rc11/đúng dạng/nguyên byte; ci-do→begin→void→connector rc8/chưa mở lượt mới/nguyên byte; các mutant chính xác đều bị bắt. |

**Đối chiếu từng ca bắt buộc.** Nền r814 **37/37 PASS**. **30 mutant / 47 lượt ca đích GIET / 90 lượt đối chứng khác họ PASS**. Tất cả lỗi đích là `AssertionError` nghiệp vụ, không có BO_QUA/TIN_DUNG_GIA hay traceback CLI. Đã đọc tên ca, lớp lỗi và thông điệp; với oracle quyền đã đối chiếu tuple `(nguyên nhân,generation,sha)` và pending_sha, không chỉ rc. [Audit từng target](MUTATION_AUDIT.md), [toàn văn lỗi/cặp neo-thay](mutants/results.json).

| yêu cầu nghiệm thu | ca r814 (nền PASS) | mutant bị chính ca đó bắt | lý do đỏ đã đo |
|---|---|---|---|
| {A,B}→{B} hợp lệ | r814_ab_b_hop_le | r814_giam_hai_lop | AssertionError đòi0/được3; mutant siết sai mức giảm2→1 |
| biểu hiện trùng, lớp2→2 | r814_bieu_hien_trung | r814_khong_giam_van_qua | Đòi3/được0; bỏ chặn không giảm |
| đổi tên không bảng nối | r814_doi_ten_khong_noi | r814_doi_ten_tu_do | Đòi11/được0; baseline không qua bảng nối/nguyên byte |
| gộp thuần sau nối1→1 | r814_gop_qua_noi | r814_noi_chi_vong_nay | Đòi3/được0; mutant bỏ áp nối ở vòng trước |
| mốc→vòng1 không giảm | r814_moc_vong1_khong_giam | r814_vong1_mien_so | Đòi3/được0 |
| vòng3 | r814_vong_3 | r814_vong_3_lot | Bước6 đòi3/được0; baseline vòng3 dù1→0 vẫn blocked |
| P3 không vào same-failure | r814_p3_khong_dem | r814_p3_vao_dem | Counts đòi{}, được a-b:1 |
| đối chứng P2 vẫn đếm | r814_p2_van_dem | r814_bo_ca_p2 | Counts đòi a-b:1, được{} |
| tự chọn vá P3 đi được | r814_vua_p3_di_duoc | r814_vua_khong_ghi_quyen | Quyền None thay vì (p3,1,pending_sha) |
| tập chọn rỗng | r814_vua_p3_rong | r814_vua_tap_rong | Đòi2/được0; baseline ít nhất một/nguyên byte |
| slug ngoài H | r814_vua_p3_ngoai_bien_nhan | r814_vua_ngoai_bien_nhan | Đòi11/được0; baseline không phải lớp P3/nguyên byte |
| xóa hết P3 | r814_xoa_het_p3 | r814_rong_la_khong_giam | Đòi0/được3; mutant coi tập sạch là không giảm |
| H changes_requested khác generation | r814_am_generation_khac | r812_bo_generation | Đòi11/được0; mutant dùng chung còn bị hai ca r812/r834 bắt |
| M4(a) refs hợp lệ trộn null | r814_check_refs_tron_null | r814_refs_bo_do_dai | Đòi11/được0; baseline đúng dạng/nguyên byte |
| M4(b) CI→begin→void→connector | r814_ci_void_connector | r814_void_khoi_phuc_quyen_ci; r813_quyen_ci_qua_luot_moi | Cả hai đòi8/được0 ở bước3 |
| hồi quy r812/r834/r813 | 148 r812 +63 r834 +43 r813 | Không chạy mọi mutant lịch sử | **254/254 PASS**; thêm37 r814 +2 stdout +2 moc = **295/295 PASS** |

Chốt M4(b) là điều kiện **không có begin_attempt sau mo_lai cuối** tại product:2966, không phải số attempts_used còn lại. Void không xóa lịch sử begin. Đã đối chiếu hai biểu hiện với handoff#813 và verdict#813 lượt6 được giao; không lấy lời khai executor làm kết quả riêng. Không sửa mã sản phẩm M4.

Những ca bổ sung schema/lý do/nguồn lặp/hạng nguồn/hạng đích, nhiều hàng, giữ mốc cũ, thay quyền cũ, P3 ở ci-do và vua-p3 xét dừng đều có mutant bị chính ca đó bắt: **37/37 ca r814 có bằng chứng mutant**, gồm mutant dùng chung. Trường hợp rr_nhieu_hang trên mutant đi tới rc3 của chốt vòng thay vì rc11 đầu vào vẫn là phát hiện đúng lỗi nghiệp vụ, không phải CLI sập.

**I1–I11 và các nhánh biên M1–M4.** Đọc các đường load/save, begin/void, record-review, H/canon, accept, mo-lai, checkpoint, xét dừng và parser liên quan; kết hợp hồi quy với [16 kịch bản riêng, 60 bước có oracle](probes/results.json), [trace CLI](probes/trace.jsonl).

| bất biến | kết luận và giới hạn |
|---|---|
| I1/I2 | Quyền mới vẫn dựa H đã validate hoặc checkpoint từ Git đo được. vua-p3 dùng ảnh H pending, không biến readback R thành authority. Lease/remote trong phép thử là fixture cục bộ; không xác minh authority online. |
| I3/M1 | `_kiem_noi` dùng chung kiểm kiểu, khóa, slug, lý do, nguồn/đích duy nhất, đích P3 trong chính H; nguồn chỉ P3 vòng trước và đã rời vòng hiện tại. Ngoài record-review không có nguồn nối hợp lệ. Tập chọn P3 rỗng không đạt, tập finding sạch được phép rỗng. |
| I4 | Ca âm kiểm byte state trước/sau. vua-p3 rỗng/ngoài H tại trần vẫn rc2/11 và nguyên byte; lựa chọn đúng tại cùng trần ghi blocked/rc3. Vòng không giảm/vòng3 là kết quả hợp lệ: ghi review, tăng rounds, đóng attempt, tiêu thụ call rồi blocked_vong_p3. State reload được. |
| I5 | vua-p3 có trong CUA_DI_TIEP và gọi cùng `_xet_dung`; mutant bỏ đăng ký bị bắt. Record-review vẫn khép lượt đang mở. Không dựng máy xét dừng thứ hai. |
| I6 | Quyền p3 neo generation/pending_sha và thay quyền ci-do cũ; mutant giữ quyềnA khi pendingB bị oracle tuple bắt. Quyền p3 không mở connector từ running (rc8/nguyên byte). Checkpoint cho_phep_va tiêu thụ quyền connector như cũ. Tiêu thụ quyền tại cửa đẩy thuộc#816. |
| I7 | Hồi quy r813/r834 và M4 kiểm kho/PR/head, app/workflow/job, run/attempt mới nhất, refs đủ và đúng dạng. Không suy fixture thành CI thật. |
| I8/I10 | Dùng canon/chuẩn hóa identity không đổi; H khác packet/generation/head/spec/role bị các ca hồi quy bắt. Biên nhận changes_requested khác generation rc11/nguyên byte. |
| I9 | Non-ADR giữ nhánh đếm cũ, đường record-lease cũ vẫn false; hồi quy được phép chạy đều đạt. State ADR cũ giữ mốc qua H pending; counts lịch sử là nợ P3 đã chuyển#816. Không tuyên bố full-suite N/N. |
| I11/M2 | Sự kiện mới loại P3 khỏi review.finding_ids, history.record_review.finding_ids và mo_lai.finding_ids, đồng bộ finding_counts với `_load`. Slug mới qua bảng nối, gộp so trên cả hai vòng. |

Probe `changes_requested` toàn-P3: lặp2→2 bị rc3/blocked, giảm2→1 rc0/running/counts{}. `vua-p3→begin→void→review` không giảm vẫn blocked. `chu-kho-duyet cho_phep_day` không reset vòng. CI hoặc connector→chu-kho-duyet xen giữa tạo mốc mới đúng cơ chế đã công bố vì có sự kiện mo_lai; số vòng vá đã ghi vẫn được cộng trong k toàn lịch sử. Cả16 state cuối đều `status` rc0.

Khai `tu:[]` cho đích C có thật, đồng thời reviewer khai A/B hết, được nhận2→1. Cùng slug từ P3 lên P2 được ghi1→0 nhưng state **running/changes_requested**, counts1; không tạo approve. Đây là quyền phân lớp/hạng của reviewer H theo I11 và mô hình tin cậy. Máy không chứng minh được sửa mã thật chỉ từ bảng lớp; điều kiểm được là tính nhất quán của chính H. Không mở lớp mới cho hai hành vi đã có và không đổi này.

**Bằng chứng lệnh và giới hạn phép đo.** Đã đọc `tham-chieu/chon.py` và logic mục3 main trước khi chạy. [audit.py](audit.py) tái dùng chay_suite, phân loại kill và đối chứng; kiểm tập chọn không rỗng, tên ca duy nhất, target tồn tại, neo thay đúng một chỗ; ghi đầy đủ output CLI và hash state. Tập chọn baseline chính xác:

```text
python -B -W ignore out/audit.py baseline '^r81[234]_|^r834_|^stdout_cp|^moc_'
python -B -W ignore out/audit.py extra_duplicate '^r81[234]_|^r834_|^stdout_cp|^doctrine_|^ac18_nfkc_hai_cham_toan_rong$|^ac19_oan_claude_md_master$' out/extra-mutants/duplicate-destination/packet_loop.py
```

| command đã chạy | rc | kết quả / bằng chứng dương |
|---|---:|---|
| `python -B out/bootstrap.py` | 0 | Sáu hash khớp; head/tree/base/parents/blobs/ancestry/scope; [IDENTITY.json](IDENTITY.json) |
| `python -B -W ignore out/audit.py gates` | 0 | Hai gate product đều rc0; [gates/results.json](gates/results.json) |
| `python -B -W ignore out/audit.py baseline …` | 1 do logger reviewer | 294 PASS,1 lỗi logger UnicodeEncodeError; không phải lỗi sản phẩm. [summary gốc](baseline/summary.json), [log](baseline.log) |
| `python -B -W ignore out/audit.py logging_recheck '^r812_r6_receipt_native$'` | 0 | 1/1 PASS sau sửa logger; hợp nhất **295/295 PASS**, loại1 ca đường dẫn trước chạy. [BASELINE_VERIFIED.json](BASELINE_VERIFIED.json) |
| `python -B -W ignore out/audit.py mutants` | 0 | **30 mutant,47 target GIET,90 đối chứng PASS**, 0 tín dụng giả; [summary](mutants/summary.json), [log](mutants.log) |
| `python -B -W ignore out/probes.py` | 0 | **16/16 kịch bản,60 bước đúng oracle**, gồm A/B mutant và nợ legacy; [summary](probes/summary.json), [log](probes.log) |
| `python -B -W ignore out/audit.py extra_duplicate …` | 1 do cùng logger | 311 PASS,1 lỗi logger; [summary gốc](extra_duplicate/summary.json), [log](extra_duplicate.log) |
| `python -B -W ignore out/audit.py logging_recheck_mutant '^r812_r6_receipt_native$' …` | 0 | 1/1 PASS; hợp nhất mutant sống **312/312** ca, gồm3 đối chứng doctrine. [EXTRA_VERIFIED.json](EXTRA_VERIFIED.json); A/B riêng vẫn giết mutant |
| `python -B out/finalize.py` | 0 | Kiểm số lượng/kết quả, hash/toàn vẹn source và bản sao, xuất verdict/evidence manifest; [SOURCE_INTEGRITY.json](SOURCE_INTEGRITY.json) |

Hai lỗi logger có cùng nguyên nhân: JSON ghi argv chứa surrogate bằng ensure_ascii=False. Chỉ sửa logger thành ensure_ascii=True rồi đo lại đúng ca trên hai vế, không đổi product/test. Giữ log và kết quả ban đầu, không tính lỗi logger làm finding/kill hay PASS. Kết quả hợp nhất có chỉ rõ nguồn recheck. Không coi rc0 của probe A/B là product mutant đúng: oracle cố ý đòi vế mutant nhận sai để xác nhận chốt bị gỡ, đồng thời oracle đặc tả riêng ném AssertionError. Mutant chỉ được khẳng định sống trên312 ca đã chọn, không suy thành toàn repository.

**Định danh hồ sơ.** Đã đọc toàn bộ `runs/1bd2a15c/prompt.snapshot`; theo chỉ thị trực tiếp, SRC=`src/`, OUT=`out/` tính từ cwd. Reviewer độc lập Codex/OpenAI, họ openai; executor theo lease là Claude, họ claude; packet#814 revision3 generation2, sensitive, assurance_target cross_approved. Thực tế có shell Linux qua công cụ/API, transport machine. Không kế thừa context executor. Không dùng actor GitHub để suy model reviewer hoặc tự sinh receipt assurance.

Đã đọc các trường quan sát model/effort/sandbox trong `runs/1bd2a15c/run.json` theo hướng dẫn master mới: tại lúc đọc, các trường này chưa có giá trị (`null`), xem [RUN_EVIDENCE.json](RUN_EVIDENCE.json). Vì vậy serving model/effort/session, launcher surface và trạng thái terminal của lượt hiện tại **chưa được đo độc lập trong verdict này**; không dùng việc thiếu header stderr làm kết luận. Consumer phải kiểm run đã kết thúc và receipt đúng contract; `approve` nội dung không tự chứng minh assurance vận hành hay quyền đẩy.

Hai hash đặc tả khớp dòng3. Bốn verdict trước đã băm lại và khớp toàn bộ:

| lượt | SHA-256 |
|---|---|
| 1 | `8ca0f12346366fd9efde9a445923d2c7e7bfc98358fb2a1a05989de6bc62aea2` |
| 2 | `d2459a3672a0b3de757323fc1a86bb0346637655e64f775ab3156df45a29bc0a` |
| 3 | `9dc9d5a696f9fee205e964b582cf6f4b0c0a23a304250fde4c1e26fee1fd1c7f` |
| 4 | `d75eda0f09de0f997cf5acabdfc2f0ea172705a4dc3477ccf7fa34331e5718b2` |

Base lease `09db70350414d767b793a71cb630e643f216a1b1` là mốc cấp lịch sử, không nhầm với base review mới. Handoff trong lease chỉ ở nhánh lease, không thuộc diff PR hai tệp. Lý do lượt5 là master tiến sau approve làm check thu-hoi đỏ theo hồ sơ được giao; đã đo graph/git, không xác minh check GitHub online.

Mọi script, fixture, mutant, bản sao và report do reviewer tạo đều trong OUT. Môi trường: `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=OUT/tmp`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null`, `GIT_OPTIONAL_LOCKS=0`, `GIT_ALLOW_PROTOCOL=file`, core.abbrev của copy=7. Các thao tác fetch/push/ls-remote của fixture chỉ dùng kho bare riêng dưới OUT; không mạng/GitHub, không push SRC/remote thật.

Snapshot SRC đầu/cuối: **7540→7540 tệp,0 delta byte/mode**, gồm .git, tracked/untracked/ignored. HEAD/tree/ref/worktree/index giữ nguyên; bản sao không có delta nội dung ngoài cấu hình core.abbrev được ghi trước test. Đây là phép so hai mốc, không phải giám sát mọi lần ghi. Sandbox thực tế workspace-write; SRC được đối xử read-only. [SOURCE_INTEGRITY.json](SOURCE_INTEGRITY.json), [bản ghi tăng dần](VERDICT-progress.md), [băm artifact](ARTIFACTS.json).

`not_run`: full suite `python .claude/dev/packet_loop_test.py` (~60 phút, prompt ưu tiên chọn lọc); mutant ngoài tập đã nêu; CI/thu-hoi/lease/GitHub online; Windows thật; bare Ruff lint và Ruff pin/probe contract. Không lấy full-suite của executor làm kết quả độc lập. `r812_r4_own_parent` bị loại **trước chạy** theo chỉ thị không soạn nội dung đường dẫn thoát cây, không tính PASS. Hướng thử ấy chỉ mô tả bằng lời: receipt/lease/checkpoint hoặc liên kết dẫn ngoài phạm vi phải bị từ chối trước truy cập ngoài cây, giữ state nguyên byte.

Protocol#977, generation kế tiếp#815, ghi đẩy/tiêu thụ quyền ở cửa đẩy#816 và kích hoạt ADR-0054 ngoài phạm vi. Không phát hiện thay đổi hợp đồng accept, mo-lai hoặc chu-kho-duyet do merge.
