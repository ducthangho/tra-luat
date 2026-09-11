verdict: changes_requested
reviewed_sha: bd4ecd4fffb389f6f9dfde9dee5b6a8250a80459
reviewed_base: c0a5cbe89a90588115262e1a2c3ac84cbd98be9e
reviewed_spec_sha256: 465538364b1a3f9477782fba79869bbd1c9351140e3fa9df50451baae22f9c79
reviewed_adr0047_sha256: b9975929c52e12767417b46b47829c265230117fe65df6a9fd22540d4868fdab
reviewed_files_sha256: lease_publish.py 6acb6a89abacbe214639a7ceed45b083e43ca06bb18a23c1fc5a702fa41a3816 · lease_publish_test.py 3f2acee321a8fd7edf58e4eff225a3bd4aa632455c05191c7fb8c9cadce247c2 · ops-thu-hoi-admission.yml 7c7c572a7fe9cc428e980ab26cb74c19dc7961f831a955cfeead528431715bee
model_tu_khai: claude-fable-5 (Claude Fable 5, Anthropic; effort max — theo cấu hình phiên, không có phép đo độc lập build)
provider: anthropic
review_class: sensitive
lease: wp488-thu-hoi-lease-a0-exec-1-claude-20260909
review_round: 2
started_at_utc: 2026-09-09T19:59:34Z

**KHÔNG P1. `changes_requested` chỉ vì MỘT P2 mới executor vá được trong packet (F10, hint kèm sẵn, đã đo hai chiều); cả 9 finding lượt 1 đều ĐÓNG hoặc ĐÓNG-MỘT-PHẦN với phần còn mở ĐÃ KHAI ĐÚNG CHỦ (chủ kho/A1), không phần nào fail-open.** Sau khi áp F10, trong tay executor không còn gì; hai mục còn mở (pin `upload-artifact` bằng commit — F07; manifest ADR-0047 lớp 2 đầy đủ trường — F08) là việc chủ kho/A1, đang fail-close (workflow chưa required, mỏ neo profile rỗng ⇒ mọi discovery production 12).

Kỷ luật lượt này: read-only mức git với `cay-kho/` (kiểm cuối: HEAD `bd4ecd4`, worktree sạch 0 dòng, sha256 ba tệp khớp đầu lượt); mọi bản sao/đột biến/fixture nằm trong `scratch/luot2/`; không mạng; không dựng ca thuộc lớp cấm — các ca âm S1/S2/A6 chỉ CHẠY qua t129/t130/t136/t149 có sẵn và qua t139; đột biến chỉ trên bản sao. Fixture non-UTF-8 của F10/t150 là tên tệp/bytes latin-1 thông thường trong kho Git thật — không đồng tự Unicode, không chuỗi thoát, không đường thoát cây.

**Khai báo sự cố môi trường (không phải lỗi executor):** harness của phiên TỰ ĐỘNG bơm nội dung `CLAUDE.md` của kho vào ngữ cảnh hai lần (khi cwd trôi vào `cay-kho/` và khi đọc tệp trong bản sao `scratch/luot2/head/`) — tệp thuộc danh sách CẤM ĐỌC của phân công; tôi không yêu cầu và KHÔNG dùng nội dung đó: mọi hợp đồng trích trong verdict này dẫn từ `SPEC.md`/`ADR-0047.md`/`EVIDENCE.md`/`VERDICT.luot1.md` và từ mã/số đo. Lệnh xoá tệp đó khỏi bản sao bị guard tệp nhạy cảm chặn nên dừng ở cam kết không-dùng. `docs/PROTOCOL_DA_PHIEN.md`, `.claude/**`, `ops/reviews/**` không được đọc.

## Bảng F01–F09 → trạng thái

| F | Trạng thái | Bằng chứng đã chạy (mã mới bd4ecd4) |
|---|---|---|
| **F01** Q13 binding | **ĐÓNG** | Phản chứng lượt 1 chạy lại: `m4_bad_policy_metadata` **12** (policy không JSON object), `m4_policy_no_marker` **12** (trước là 0). t133 ma trận binding trong suite 144/144. Probe thêm: marker CŨ + policy đổi sang JSON object khác ⇒ **0** (đúng spec dòng 232–235 "Marker ghi policy ĐẦU TIÊN… B(P1,R1)→B2(P2,R1) có thể qua" — chốt "policy có mà thiếu marker ⇒ 12" KHÔNG chặn oan chuỗi ấy vì marker còn nguyên qua append-only); marker cũ + policy đổi HỎNG ⇒ 12; policy ở cả S lẫn T không marker ⇒ **12** "không grandfather" (đúng spec dòng 230–231); marker mới khi `DESCRIPTOR_Q13_SHA256 = None` ⇒ 12 (t133/t140). Descriptor `"None"`/rỗng không lách được: `kiem_metadata_retired` đòi SHA256.match nên `descriptor_sha256` luôn là chuỗi 64-hex, không bao giờ bằng `None`. S là merge: so chuỗi `base_sha_before_add == S`, không phụ thuộc hình dạng S; ca merge giữ/mất marker (0/8) trong harness. Canonical hiện tại không bị chặn oan: `c0a5cbe` KHÔNG có policy lẫn `ops/thu-hoi` (cat-file -e rc=128 cả hai). |
| **F02** ls-tree −z | **ĐÓNG** (trong packet) | Tên Việt thường: `holder_unicode_ledger`(±forecast) **12**, t141 trong suite; scan trả đúng entry `thu hồi.yaml`. Namespace là blob/gitlink: **12** (t142 + harness, "không phải thư mục"). Tên KHÔNG phải UTF-8: probe mới ⇒ **12** sạch qua catch UnicodeDecodeError của `_ls_tree_z`, không traceback — đúng hợp đồng fail-close. Luật cũ `_quet_lease_toan_kho` còn lỗi quote: xác nhận NGOÀI packet (mã base không đổi; write set 3 đường) — ghi nợ P3, xem Findings; lưu ý forecast MỚI trên `ops/leases` đã dùng `_ls_tree_z` sửa rồi. |
| **F03** tree entry | **ĐÓNG** | `m4_slash_entry_name` chạy lại ⇒ **12** "tên entry không hợp lệ/trùng 'thu-hoi/x.yaml'" (t143 trong suite). `tree()` từ chối mode ngoài {100644,100755,120000,160000,40000}, tên rỗng/`.`/`..`/chứa `/`/`.git`/trùng, entry cụt, tên không UTF-8. Không từ chối oan: tên Việt hợp lệ ngoài sổ qua (`m4_unicode_outside` 0), 5 mode Git canonical đều nhận; mode legacy (vd `100664`, zero-padded) bị 12 fail-close — chấp nhận được cho kho này (không có object cổ), ghi chú không phải finding. |
| **F04** deadline | **ĐÓNG** | `reader_expired_memo` ⇒ **12 "hết deadline tại memo"** (trước là 0); `deadline_at_completion` ⇒ **12**; chốt "trước khi trả" tồn tại và có răng (mutant catalog `F04-bo-deadline-memo`/`F04-bo-deadline-truoc-tra` GIẾT qua t144). t131 giữ phân biệt "trước spawn" vs join-timeout. |
| **F05** thu hồi subprocess | **ĐÓNG** (+P3 F13) | Blob 1 MiB > trần: **12 đúng mã, KHÔNG TimeoutExpired, child ĐÃ chết** (`reader_large_child_alive [False]`; t145). Tổng budget kiểm TỪ HEADER trước khi đọc body (`total_budget_before_allocation` 12, t146 đo `reads == []`). `cat-file` rc≠0 ⇒ **12 "không dùng bytes của tiến trình lỗi"**. `start_new_session`+killpg trong `finally` mọi đường thoát. Còn lại: 3 fd ống không đóng khi thread kẹt đường deadline (daemon giữ tham chiếu Popen) — bounded 1 lần/lời gọi chết, tiến trình CLI thoát ngay sau Chan ⇒ P3 (F13), không phải rò tiến trình. |
| **F06** schema/date | **ĐÓNG** | `schema_float` ⇒ **8** đúng thông điệp; metadata float ⇒ 12; `invalid_date` 30-02 ⇒ **8 "không phải thời điểm có thật"**, CLI không traceback (t147 hai chiều 8/12). `type(sv) is not int` loại cả bool lẫn 1.0. Residual P3 (F14): M4 vẫn lấy `datetime.now` riêng từng record thay vì một snapshot — chỉ lệch micro-giây theo chiều CHẶT hơn→lỏng dần trong một lần chạy, vô hại ở inactive; lượt 1 đã gợi ý snapshot chung, executor chưa làm — không mở lỗ. |
| **F07** M9 definition/receipt | **ĐÓNG-MỘT-PHẦN** | Phần trong packet ĐÓNG: `workflow_sha` đo riêng, đòi hex + `== S` (S đã đòi 40-hex dòng 75–77); `workflow_ref` so đúng chuỗi `<kho>/.github/workflows/ops-thu-hoi-admission.yml@refs/heads/<nhánh>` sau khi kho đã so bằng canonical; blob định nghĩa lấy tại ĐÚNG commit `workflow_sha` rồi sha256 bytes blob (không phải tệp checkout); `check_run_id` từ jobs API của đúng run/attempt (`actions: read` cả workflow lẫn job, t137 đòi đúng 3 quyền read và "không quyền ghi nào"); receipt thêm definition commit/ref/blob/sha256, check_run_id, job_id, checker_rc. actionlint 1.7.7 **rc=0**, shellcheck bash **rc=0** trên run block. t148 CÓ RĂNG: đột biến bỏ `workflow_definition_commit` khỏi workflow ⇒ t148 đỏ TinHieuChotCa (đo được). **CÒN MỞ (P2, chủ kho — giữ nguyên từ lượt 1):** `actions/upload-artifact@v4` vẫn pin bằng tag, spec M9 dòng 454 đòi "action ghim commit đã duyệt"; sandbox không readback được SHA kho ngoài và reviewer cấm tự chọn ⇒ đúng là ngoài tay executor, PHẢI đóng trước khi bật required check/A1. P3 (F12): `CHECKER_RC=$?` là dòng chết dưới `set -euo pipefail` (demo: script thoát TRƯỚC phép gán khi checker fail) ⇒ trường `checker_rc` chỉ có thể là 0; không sai dữ liệu (receipt chỉ sinh khi rc=0) nhưng thoả hợp đồng "checker rc" một cách tầm thường — sửa gợi ý trong Findings. |
| **F08** profile miền | **ĐÓNG-MỘT-PHẦN** | `kiem_mien_ho_so` (đúng tập khoá + kiểu/miền từng giá trị) đứng TRƯỚC phép so digest; phản chứng lượt 1 (khoá lạ + digest tự neo) nay chết Ở ĐÚNG validator miền: profile_probe trả **12 "hồ sơ adapter phải có đúng khoá […]"**; t136 bổ sung ca này trong suite; mutant `F08-bo-validator-mien` GIẾT trong t139. **CÒN MỞ (P2, chủ kho/A1 — đã khai trong EVIDENCE):** hồ sơ đo chưa mang identity HTTPS-helper/runtime/thư viện/toàn trust store hiệu lực mà ADR-0047 lớp 2 (dòng 46–49) đòi cho manifest được duyệt — ở A0 fail-close tuyệt đối vì `PROFILE_ADAPTER_DA_DUYET` rỗng ⇒ mọi discovery production 12; phải mở rộng schema trước khi duyệt mỏ neo đầu tiên. |
| **F09** preflight env | **ĐÓNG** | t149: hai lời gọi `rev-parse` của preflight có env dict tường minh từ rỗng (sentinel caller không lọt) + argv git tuyệt đối. Positive không vỡ: bare + linked worktree đọc đúng cùng tree (probe `reader_bare_linked` khớp), harness working/bare/linked/pack/alternate witness=2 như lượt 1. Residual P3: stdout của `_git_nguon` decode theo locale tiến trình cha (đường dẫn objects non-UTF-8 → traceback, thuần lý thuyết); các đường consumer (`_ls_tree_z`, cat-file policy) vẫn đi `GOI_GIT` kế thừa env caller — ĐÚNG THIẾT KẾ đã khai ("cùng cửa với luật cũ" cho đồ giả trạng thái), chỉ reader M4 mới là thẩm quyền receipt và nó đã cô lập. |

## Findings mới

### F10 — P2 — Consumer Q13 nổ UnicodeDecodeError (traceback rc=1) thay vì Chan 12 khi policy không phải UTF-8 — executor VÁ ĐƯỢC TRONG PACKET (hint kèm)

- **Vị trí:** `ops/lease_publish.py:1602` (`_kiem_so_rong_khi_chua_kich_hoat`, nhánh metadata) — mã MỚI của bản vá F01 lượt này: đổi `cat-file -e` (chỉ đọc rc) thành `cat-file blob` qua `GOI_GIT` text-mode mà không đỡ lỗi decode, trong khi `_ls_tree_z` ngay cạnh có catch.
- **Hợp đồng:** SPEC Q13 dòng 221 "Mọi lỗi source metadata ⇒ 12", dòng 229 "policy hỏng ⇒ 12"; cùng lớp F06 lượt 1 (P2: lỗi nguồn thoát thành traceback).
- **Phản chứng đã chạy** (`scratch/luot2/probe.log`, ca `policy_nonutf8_consumer`): kho Git thường, nhánh mang marker retired hợp lệ + policy bytes `b'{"a": "\xc3\x28"}'` (không phải UTF-8); `ai-dang-giu ops/x.md --root <kho>` ⇒ **UnicodeDecodeError xuyên qua `main`** (subprocess `_translate_newlines` decode strict) ⇒ CLI traceback **rc=1**, không phải `CHAN [12]`. Fail-close VẪN GIỮ (rc≠0, không receipt, không verdict xanh) ⇒ P2, không P1.
- **Vá + test:** `HINT.patch` (2 hunk): bọc `try/except UnicodeDecodeError` quanh lời gọi, gộp vào đúng thông điệp 12 hiện có; test `t150_review2_F10_nguon_khong_utf8_la_12_khong_traceback` hai ca (policy non-UTF-8; tên tệp sổ non-UTF-8). Đã đo HAI CHIỀU trên bản sao: test-only trên mã chưa vá ⇒ ĐỎ bằng `TinHieuChotCa`; test+mã ⇒ QUA; suite đầy đủ trên bản sao TRỌN CÂY đã áp bằng chính `patch -p0`: **145/145 đạt; đã chạy=145, bỏ qua=0; rc=0** (`suite-hintfull.log`; số ca 144→145 — EVIDENCE cần cập nhật khi executor áp). Nhãn bắt buộc: **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.
- **Nguy cơ khi vá:** giữ nguyên thông điệp/mã 12 hiện có (t142 neo "không phải thư mục", chuỗi policy neo trong t133/t140 không đổi); không nuốt lỗi decode ở chỗ khác; không đổi neo mutant t139 (đã kiểm: không anchor nào chạm dòng sửa).

### F11 — P3 — Chốt UnicodeDecodeError của `_ls_tree_z` không có răng test

Mutant bỏ `except UnicodeDecodeError` trong `_ls_tree_z` **SỐNG** qua t141 (t141 chỉ dùng tên UTF-8 hợp lệ; không ca nào trong suite có tên non-UTF-8). Hành vi hiện tại ĐÚNG (probe: 12 sạch); mất chốt chỉ suy biến thành traceback rc=1 (vẫn fail-close) ⇒ P3. Ca (b) của t150 trong HINT.patch bịt luôn gap này — sau khi áp, mutant ấy chết ở t150.

### F12 — P3 — `CHECKER_RC=$?` là dòng chết dưới `set -euo pipefail`

`ops-thu-hoi-admission.yml:102`: checker fail ⇒ shell thoát TRƯỚC phép gán (demo chạy được: `set -e; false; X=$?` không bao giờ tới `X=$?`); trường `checker_rc` trong receipt vì thế hằng 0. Không mở lỗ (receipt chỉ sinh trên đường thành công; job đỏ mang rc qua exit code) nhưng là chốt-ghi-số không thể ghi số khác 0. Sửa gợi ý (khi thuận tay, không bắt buộc packet): `CHECKER_RC=0; python3 … || CHECKER_RC=$?; [ "$CHECKER_RC" -eq 0 ] || exit "$CHECKER_RC"` — giữ fail-close, số thật vào biến trước khi thoát.

### F13 — P3 — Rò 3 fd ống ở đường deadline của `KhoObject.doc`

`finally` chỉ đóng stdin/stdout/stderr khi thread ĐÃ dừng; đường deadline (thread kẹt `read`) để daemon thread giữ tham chiếu Popen ⇒ 3 fd sống tới hết tiến trình. Child đã bị killpg+reap (không rò tiến trình — t145 đo). Bounded một lần mỗi lời gọi chết, mà Chan 12 kết thúc CLI ngay ⇒ P3, ghi nhận cho consumer chạy dài tương lai.

### F14 — P3 — Clock snapshot per-record trong M4

`kiem_ban_ghi_thu_hoi`/`kiem_metadata_retired` mặc định `datetime.now` mỗi lần gọi; lượt 1 gợi ý một snapshot cho cả loạt. Lệch micro-giây, chiều nới dần trong MỘT lần chạy, mọi revocation vẫn 12 ở inactive ⇒ không mở lỗ.

### Ghi nhận ngoài packet (không đòi vá ở đây)

1. `_quet_lease_toan_kho` (luật cũ) vẫn đọc `ops/leases` bằng ls-tree có quote — tên lease phải khớp LEASE_ID (ASCII) mới qua cổng đăng nên tác động bị chặn từ nguồn; nợ dọn khi có packet luật cũ. 2. `_du_bao_check:1633` đọc bản ghi revocation qua GOI_GIT không catch decode — KHÔNG THỂ TỚI ở A0 (mọi bản ghi thu_hoi đã 12 tại `_kiem_so_rong` trước đó, metadata không bao giờ khớp `<LEASE_ID>.yaml`); phải đỡ khi A1 bật cờ. 3. `pip install PyYAML==6.0.3` pin version không pin hash — đồng bộ quy ước t31 toàn kho, đổi một mình workflow này sẽ lệch chuẩn; việc toàn kho.

## Mutant đã chạy

Cơ chế: bản sao `scratch/luot2/`, `sys.dont_write_bytecode`, mỗi mutant một tệp module riêng, thay `_nap_cong`; phân hạng GIẾT chỉ khi `TinHieuChotCa`, lỗi khác = VÔ CAN (không nhận công). Log: `scratch/luot2/probe.log`, `probe-results.json`.

| Mutant | Nguồn | Ca đích | Kết quả | Ghi chú |
|---|---|---|---|---|
| toàn catalog t139 (33 mutant) | t139 tại HEAD | từng ca khai trong catalog | **33 = 30 GIẾT / 3 SỐNG / 0 tín dụng giả / 0 sai kỳ vọng** | chạy nguyên ca t139; runner tự chốt neo-duy-nhất, lớp ngoại lệ, kỳ vọng từng mutant |
| `F01-bo-descriptor-ghim-SONG` (SỐNG thứ 3) | trong t139 | t133 | SỐNG đúng khai | **chốt che THẬT, không phải lỗ**: `descriptor_sha256` bị `kiem_metadata_retired` ép SHA256.match nên luôn là chuỗi 64-hex ⇒ phép so `!= DESCRIPTOR_Q13_SHA256(None)` vẫn 12; thông điệp thay thế vẫn chứa "descriptor" nên t133 không phân biệt — đúng bản chất "chỉ cho thông điệp rõ hơn" như seam khai |
| `bo-mode-policy` (mới, ngoài catalog) | bỏ chốt `loai_p != "blob" or mode_p != "100644"` | t133 | **GIẾT** ("policy executable: đợi 12 '100644', được 0") | chốt mới F01 có răng ngoài catalog |
| `bo-grandfather` (mới) | bỏ chốt `tim(tree_S, POLICY) is not None` | t133 | **GIẾT** ("S đã có policy: đợi 12 'grandfather', được 0") | — |
| `bo-thieu-marker` (mới, độc lập với t139) | `policy_T is not None and not metadata_T` → False | t133 | **GIẾT** ("policy không marker phải 12") | trùng hướng catalog `F01-bo-thieu-marker`, đo lại độc lập |
| `bo-catch-UnicodeDecodeError` của `_ls_tree_z` (mới) | xoá 2 dòng except | t141 | **SỐNG** | ⇒ F11 (P3); t150 trong HINT bịt |
| đột biến workflow: xoá `workflow_definition_commit` khỏi receipt | bản sao workflow | t148 | **ĐỎ TinHieuChotCa** | t148 tĩnh nhưng CÓ THỂ đỏ ở chốt chịu lực |
| đột biến t136-F08 lượt 1 (khoá lạ + digest tự neo) | profile_probe lượt 1 nguyên bản | t136 domain-copy | nay trả **12 tại validator miền** | phản chứng F08 đóng đúng chỗ |

Hai mutant executor khai "khai GIẾT hoá SỐNG khi vá rồi đã sửa catalog" (`F01-bo-descriptor-ghim` → SONG, `F01-bo-policy-JSON` → đổi ca đích sang t133 marker-cũ): kiểm chéo bằng đọc catalog tại HEAD + chạy t139 = khớp; riêng `F01-bo-policy-JSON` ghi chú trong catalog nói rõ t140 không cô lập được chốt (binding descriptor che) — nhất quán với hành vi đo được (t140 chết ở "descriptor chưa ghim" trước khi tới policy-JSON).

## Bảng đo lại

| Phép đo | Kết quả tại môi trường review | Bằng chứng |
|---|---|---|
| HEAD / base / origin/master / worktree | `bd4ecd4…0459` / `c0a5cbe…be9e` / `c0a5cbe` / sạch (0 dòng porcelain, đo đầu VÀ cuối lượt) | git rev-parse/status trên `cay-kho/` |
| sha256 SPEC / ADR-0047 / VERDICT.luot1 / HINT.luot1 / 3 tệp head | khớp cả 7 giá trị được giao (`4655…`, `b997…`, `abd1…`, `0434…`, `6acb…`, `3f2a…`, `7c7c…`) | sha256sum đầu lượt + 3 tệp đo lại cuối lượt |
| numstat `c0a5cbe..HEAD` | đúng 3 đường: wf +139/−0 · mã +880/−0 · test +1224/−1 = **+2243/−1**; name-only = đúng write set; không packet_loop/ops thu-hoi/ops-publish-lease/ci.yml | git diff --stat/--name-only |
| numstat `d5a980e..HEAD` (bản vá) | wf **+39/−7** · mã **+240/−72** · test **+370/−12** — khớp EVIDENCE từng số | git diff --numstat |
| `git diff --check` base..HEAD | rc=0 | — |
| Suite tại HEAD (bản sao, PATH có actionlint 1.7.7 + shellcheck 0.9.0) | **144/144 đạt; đã chạy=144, bỏ qua=0; rc=0** (t33/t137 CHẠY, không skip) | `scratch/luot2/suite-head.log` |
| Suite trên bản áp HINT.patch lượt này | **145/145 đạt; đã chạy=145, bỏ qua=0; rc=0** — bản sao TRỌN CÂY của HEAD + `patch -p0` sạch 2/2 hunk | `scratch/luot2/suite-hintfull.log`. Trung thực rig: lần chạy ĐẦU trên rig chỉ chép 3 tệp cho 121/145 — 24 ca đỏ đều là ca đọc cây kho thật (t31/t33/t98/t137…), t150 và mọi ca A0 qua; đã nhận diện là artifact của rig thiếu cây và đo lại trên bản trọn cây (`suite-hint.log` giữ làm vết, KHÔNG phải số đo của bản vá) |
| t139 tại HEAD | in đúng "mẫu số=33, giết thật=30, SỐNG có chủ đích=3, tín dụng giả=0" | `scratch/luot2/probe.log` |
| Phản chứng lượt 1 chạy lại trên HEAD (37 ca review_harness + 10 ca extra_checks + profile_probe) | mọi ca F01–F06/F08: nay 12/8 đúng mã như bảng trên; positive controls giữ 0 (m4_empty, unicode ngoài sổ, S==H, merge-giữ, reader working/bare/linked/alternate/pack, 129 siblings, holder sạch) | `scratch/luot2/rerun-review_harness.log`, `rerun-extra_checks.log`, `rerun-profile_probe.log` (ca `workflow_receipt_definition_drift` lượt 1 vỡ đường dẫn lưu trữ — thay bằng phép đo trực tiếp F07 ở trên) |
| actionlint 1.7.7 / shellcheck 0.9.0 trên workflow mới | rc=0 / rc=0 (run block, bash) | in trong phiên |
| Demo `set -e` cho F12 | `X=$?` không bao giờ chạy sau lệnh fail; script thoát rc=1 | in trong phiên |
| ruff `--select F` | lease_publish.py **0**; test **4** finding, cái đầu tại dòng 1593 (vùng cũ, trước khối A0 ~4100) — khớp EVIDENCE "delta 0" | in trong phiên |
| HINT.patch | 2 hunk (1 mã + 1 test), `patch --dry-run -p0` **rc=0** trên bản sao sạch và áp thật rc=0 trên bản trọn cây; test-only ĐỎ TinHieuChotCa trên mã chưa vá; sha256 `6a7d7e30e199d145a735c51d284ad5cec5ac1063f51164c5a238a0badb6e54c2` | `scratch/luot2/hint/`, `testonly/`, `hintfull/`, `pristine/` |
| Chặn oan canonical | `c0a5cbe:change-impact.v1.json` và `c0a5cbe:ops/thu-hoi` đều KHÔNG tồn tại (rc=128) ⇒ chốt Q13 mới không thể đỏ oan PR thường hiện nay | probe `master_khong_policy` |

Không dùng nội dung nào từ các tệp cấm đọc; không đọc `scratch/luot1/` ngoài các script harness được phép tái dùng.

## chua_do_duoc

1. **GitHub/Actions thật:** không mạng — không đo run `34377083111`/`34382549720`, CI `cong`, jobs API thật, quan hệ `workflow_sha`/base.sha trên pull_request_target thật, artifact upload/readback. Các trường F07 mới (check_run_id, run_attempt filter) chỉ được kiểm hình dạng + logic cục bộ; canary A0 theo spec M9 dòng 466 vẫn PHẢI chạy trước khi tin route/field thật.
2. **Suite trong `cay-kho/` và qua wrapper `chay_lease_publish_test.sh`:** tôi chạy trên BẢN SAO đầy đủ (144/144); không chạy trong `cay-kho/` (giữ read-only) và không qua wrapper — số 144/144 wrapper là lời khai executor, nhất quán với số đo bản sao của tôi.
3. **Lịch sử "123/144 trước khi vá" và diễn biến áp HINT lượt 1:** trạng thái trung gian không còn để đo; chỉ xác minh được kết quả cuối (t140–t149 có mặt, t148 đổi assertion pin như khai, suite xanh).
4. **doctrine-scan / doc-claims-check / release-verify / các gate ngoài suite:** không chạy lại (công cụ nằm trong `.claude/dev/**` thuộc vùng cấm đọc của phân công) — không chứng nhận các dòng ấy trong EVIDENCE.
5. **Pin `upload-artifact` bằng commit & manifest ADR-0047 lớp 2 đầy đủ:** cần chủ kho cấp SHA đã readback / duyệt manifest — ngoài khả năng đo của sandbox; trạng thái mở P2 có chủ như bảng F07/F08.
6. **Model identity:** tự khai từ cấu hình phiên; không có phép đo độc lập model build, cũng không suy từ lease.
