verdict: request_changes
reviewed_sha: 8014baf0656a6154fbb646359010cb116c98a2a1
reviewed_tree: 604cdd8b19556bf63437bdd3f34b0635e9a0a784

## (i) DANH TÍNH

Lần đầu, trước review: `git -C cay-kho rev-parse HEAD HEAD^{tree}` (exit 0):

```text
8014baf0656a6154fbb646359010cb116c98a2a1
604cdd8b19556bf63437bdd3f34b0635e9a0a784
```

`git -C cay-kho status --porcelain=v1 --ignored` (exit 0): stdout rỗng.

`sha256sum cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r{1,2,3,4,5,6,7,8}.md` (exit 0):

```text
15fe242a65c8df1ff393cdc15784642013e904bacb9b754b0d72a64237dac11e  cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r1.md
c6e53a00c7370ce0d75d9bcd954f8b7e69aa7383a0f5e6427a29e5e0d0e3ed8d  cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r2.md
e2246e90aaf35b6b006b40a258e694a99c796a1ff1a8ac21aebb408121efa121  cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r3.md
d28d00b5dbf6aac631f2aaac4282eb50ad1e59490d03acff095a64e45535430f  cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r4.md
25473237f53684706112b5a2f8dfafce143000110a57c8d680f3b44f924e5ed5  cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r5.md
b078da106387512cac956d8bc18d702bb50cfcf4bfd37101bb6c7aeb0686d201  cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r6.md
887dc78a1f20d640f1b779b58fea7c963b2931e76e31abbe00ca13960d699061  cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r7.md
079868c4f757ea2248ed92045c918eb3e51d0d3976656d4b0d788d3226badc71  cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r8.md
```

HEAD/tree khớp yêu cầu; SHA-256 ghi từ byte thực tế (prompt không cung cấp bộ hash tham chiếu riêng). Reviewer: Codex, provider OpenAI; shell/tool API trong sandbox cục bộ; không suy danh tính từ actor GitHub. Không gọi mạng/dịch vụ, không đọc/ghi tệp credential thật; phép thử dùng dữ liệu giả. Model/effort/run-ID do launcher không có trong bundle này nên không tự suy hoặc khai bịa; đây là Codex qua shell/tool API, không phải advisory review qua người vận chuyển.


Bản hiệu lực: r8. Các r1–r7 chỉ được dùng để kiểm chuỗi errata/lịch sử; không chấm lại các quyết định đã được chủ kho chấp nhận. Đã đọc AGENTS.md, CONTEXT.md, protocol (nhất là §7–§8.3, §11–§12, §20), CLAUDE.md, SKILL.md, kế hoạch đa provider và luật L1–L6 của soan-spec.

Đo cuối lượt (`identity-final.txt`, mọi lệnh exit 0):

```text
$ git -C cay-kho rev-parse HEAD HEAD^{tree}
8014baf0656a6154fbb646359010cb116c98a2a1
604cdd8b19556bf63437bdd3f34b0635e9a0a784
$ git -C cay-kho status --porcelain=v1 --ignored
(stdout rỗng)
$ git -C cay-kho diff --exit-code
(stdout rỗng)
$ git -C cay-kho diff --cached --exit-code
(stdout rỗng)
```

Tám SHA-256 cuối lượt bằng các giá trị đầu lượt. Mốc đo cuối: 2026-11-04T17:07:09+00:00. Snapshot chứng minh không có delta quan sát được ở hai mốc; không suy từ snapshot rằng chưa từng có writer khác trong toàn lịch sử. Phiên này chỉ ghi artifact ngoài `cay-kho/`, không checkout/commit/config hoặc sửa cây ấy.

## (ii) ĐO LẠI KHẲNG ĐỊNH

Lệnh tái hiện từ SANDBOX: `python -B review_checks.py > review-checks.log 2>&1` — **exit 0**. Exit 0 ở đây nghĩa là các khẳng định của script review đều đúng, kể cả đối chứng tái hiện finding; không có nghĩa F3 của đặc tả đạt. Script biên dịch các hàm nguồn được chọn bằng AST, không import/chạy CLI `tl` thật. Tệp tạm đều nằm trong `review-fixtures/`; child chỉ chạy driver thật trên `tl.py` rỗng và loader nguồn đã sao chép. Không sửa cây được review; không sinh bytecode trong cây.

Bằng chứng: [script](review_checks.py), [log](review-checks.log), [JSON](review-results.json). JSON cuối có 69 bản ghi bằng chứng (gồm neo dòng và số đo; **không phải** 69 ca selftest).

| Artifact ngoài checkout | Byte | SHA-256 |
|---|---:|---|
| `review_checks.py` | 24404 | `947352f4757579e64577617a0afef1c1e8c8686624fcf9dd7c064b6f8fa8220c` |
| `review-checks.log` | 10203 | `0f10c55c92584b5625f806847336c56b25f4a8c0ec831f2054ff9ea9afdd05f4` |
| `review-results.json` | 12653 | `e488b0de17fcc2e0e059f3818d8109941b084e6e11746b425addf2b2068e29b9` |
| `identity-final.txt` | 1394 | `5b5cb0bdc9254e3f91d19079e20aecf18e0d8921ef5d1c0c67348d166fc7d16e` |


| Khẳng định | Lệnh đo | Kết quả | Khớp/lệch |
|---|---|---|---|
| Diff đúng base/head, không đổi runtime | `git -C cay-kho diff --stat 1f0941e9 HEAD`; tạo `measured-diff.patch` bằng `git diff ... --binary` | 5 tệp r4–r8, 1548 dòng thêm; `diff --check` exit 0 | Khớp |
| Diff giao đúng byte | `sha256sum diff.patch measured-diff.patch` | cả hai `b466cb7061d75204d41fd5903b98ba7923485b492fcc21d9db3a02196c08aa78` | Khớp |
| Base là merge-base | `git -C cay-kho merge-base 1f0941e9 HEAD` | `1f0941e9bba1d1d517eda4174167b81963c06bd5` | Khớp |
| OID trần ADR-0052/0053 là commit land PR #791 | `git -C cay-kho log -1 --format='%H %s' 8ab100793df9831505f495543a74044b91c2c9ab` | đúng OID, subject `Merge pull request #791 ...` | Khớp với mốc Git; không xác minh lại quyền phê duyệt ngoài kho |
| 9 mục tiêu, mỗi mục đúng một đường dẫn trong write_set; đủ ánh xạ nghiệm thu | Python trích các dòng `N. →`, write_set và 28 hàng nghiệm thu của r8 | 9/9 đường dẫn trùng theo thứ tự; mục tiêu 1: A/M; 2: F1; 3: F1/F3; 4–5: D1/R1; 6: D2/D3/R1; 7: D2; 8: H1/R1; 9: J1 | Khớp L2; F3 có finding riêng |
| Manifest 184 tệp, chứa đủ bốn tệp ở mục tiêu 9 | `json.loads(Path(...).read_text())`, đếm `files` và tìm từng `path` | `file_count=184`, `len(files)=184`; adapter, bundle và hai doctrine đều có | Khớp |
| Fragment tham chiếu 260 và 259 dòng | `wc -l cay-kho/scripts/test_fragments/wp726_script_nlm_canary.py cay-kho/scripts/test_fragments/wp727_tl_gws_refresh.py` | 260; 259 | Khớp |
| Khuôn fragment và sinh bundle có thật | đọc `tl_core/test_fragments.py:287`, `:323`, `:464`; gọi generator thật trong fixture F3 | `TEST_ID` + `run(tl_module)`; generator tạo byte bundle; một fragment là một registration tự kiểm thử | Khớp |
| Errata r2–r7 giữ nguyên | `check_anchors_and_errata()` cắt từng mục từ revision gốc và so với r8 | 6/6 mục bằng từng ký tự; E23 đính chính lời khai r7, không sửa lịch sử | Khớp |
| Năm tệp được E10/E14 dẫn không đổi so base | `git diff --numstat 1f0941e9 HEAD -- <từng tệp>` | stdout rỗng, exit 0 cho `nlm_cli.py`, hai doctrine, `tl_gws.py`, `tl_core/nlm_ops.py` | Khớp |
| Từng neo dòng hiện hành | `check_anchors_and_errata()`, 24 phép khẳng định trực tiếp trên từng dòng | `nlm_cli.py:110/143/162/229`; `tl_gws.py:308/363/1894/1909`; `nlm_ops.py:297/1398/1424/1425/1429`; `tl_selftest.py:24829`; `packet_loop.py:1887`; `RASOAT:118/119`; `QUY_TRINH:49`; shell `93/101/104`; protocol `1517`; ADR-0060/0062 dòng 3 | Khớp; toàn bộ text dòng nằm trong log/JSON |
| `_run` nền trả tuple, timeout 124, thiếu binary 127 | `check_source_contracts()` gọi `_run` nguồn với subprocess giả, môi trường giả rỗng | lỗi auth `(1,"","Authentication expired")`; thành công `(0,"[]","")`; exception → 127/124; không gọi dịch vụ | Khớp |
| A12 giữ nguyên bốn hằng | đọc AST hằng và `git show 1f0941e9:scripts/nlm_cli.py`, so với HEAD | cả nguồn adapter bằng byte; đủ `AUTH_FIX_HINT`, `AUTH_FIX_HINT_SHORT`, `_AUTH_FIX_ORDER`, `_AUTH_FIX_RASOAT_CARVE` | Khớp bất biến nền; không khẳng định tính năng mới đã chạy |
| A13: canary nguồn phân ba trạng thái và chuỗi trộn | `check_canary()`; `_nlm_auth_alive` + `_nlm_canary_raw_get` nguồn; lấy đúng thân `_canary_song` nguồn, chạy trong RAM với module giả | sáu ca ⇒ `None,None,False,False,False,None`; thân canary ⇒ `2,2,3,3,3,2`; ca quyền chỉ probe một lần, các ca còn lại ba lần | Khớp; chấp nhận “lần cuối quyết định”, không mở lại quyết định ấy |
| `nlm-auth-status` gộp lỗi probe thành False | cùng script, gọi `_nlm_preflight_report` nguồn với ba lỗi giả | refused/permission/auth đều `alive=False` | Khớp lý do r3 bỏ lệnh này khỏi canary |
| D1 chỉ đếm câu và bảo toàn chữ cũ | `check_documents()`, từng tệp riêng, 6 fixture/tệp | chưa chèn/nhân đôi/bỏ chữ cũ ⇒ đỏ; chèn sau cách/sau xuống dòng/ngắt dòng lại ⇒ xanh | Khớp phạm vi r8; không suy vị trí/render từ D1 |
| D2/D3 chạy cùng fixture | `check_documents()` gọi `cmd_adr_song` nguồn và regex nguồn | ADR đúng, ngắt dòng prose ⇒ D2 rc 0/D3 xanh; status trần ⇒ D2 rc 9/D3 đỏ; Proposed, status đôi, status thêm trong comment/fence ⇒ D3 đỏ; xoá dòng §20 ⇒ D2 rc 9 | Khớp; D2 chỉ đọc được trạng thái/đăng ký, D3 đo đúng một dòng thô |
| H1 chỉ đòi tiền tố dòng đầu không rỗng | `check_documents()`, 5 fixture | vắng/rỗng/bỏ tiền tố ⇒ đỏ; đúng tiền tố, kể cả sau dòng trống ⇒ xanh | Khớp phạm vi r8; nội dung thuộc R1 |
| F2/r213 vẫn xanh khi thêm ngoại lệ; xoá cấm thì đỏ | `check_source_contracts()` chạy nguyên hàm lồng `_c213_auth_carve_out_khong_pha_thu_tu` với hằng nguồn và tài liệu thật/bản sao | base=True; thêm câu=True; xoá `CẤM` ở QUY_TRINH=False | Khớp; không sửa `tl_selftest.py` |
| F3 bắt nguồn fragment khác nội dung nhưng cùng ID | `check_f3()`, main/checker, builder ZIP, loader, driver nguồn | đồng bộ ⇒ rc 0; đổi thân giữ ID, không sinh lại ⇒ **vẫn rc 0/ok=true**; freshness source ⇒ `GENERATED_BUNDLE_STALE`; sinh lại ⇒ hành vi mới bị bắt; đổi ID ⇒ `TEST_ID_SET_MISMATCH` | **LỆCH — F01** |
| J1 xác minh băm và bắt thay một byte | `_verify_release_manifest` nguồn, strict=True; một fixture sửa thêm byte newline ở adapter sau lập manifest | checkout thật `ok=true`, expected/checked=184/184; fixture trước xanh/sau đỏ, failed đúng `scripts/nlm_cli.py` | Khớp; không chạy public CLI |
| G2 nền xanh; cột đột biến có chỉ dẫn đủ | `cmd_doctrine_scan` nguồn; fixture bổ sung bằng `a.path` | base rc 0 (10 tệp); cụm cấm ⇒ rc 6 đúng nhóm; bỏ cụm ⇒ rc 0 (11 tệp). Spec không khai đối chứng này | **Thiếu trong hợp đồng — F02** |
| Tên bước CI và lane manifest hiện hữu | đọc `.github/workflows/ci.yml:293`, `:500`, `:520` | có `bundled-fragment check (topology gói)`; LAND dùng committed manifest, WORKER dùng manifest tạm | Khớp; không suy CI thực tế đã success |
| Đường nạp dùng cơ chế đã có, không tạo writer registry mới | đọc `tl_gws.py:1909–1949`, `:2024–2035`; đối chiếu CLAUDE “Nguồn sự thật” và mục tiêu 1 | `nlm-auth-load`: tải `nlm_cred.enc` qua public read/fallback GAS `download`, giải mã bằng token, chốt downgrade trước ghi jar local; r8 không sửa hàm này, không `--force`, không thêm write API | Khớp ranh giới đã nêu; không gọi endpoint hoặc đọc credential |

**Phạm vi R1 và Standards/Security.** R1 đủ cụ thể để reviewer PR code thực hiện: đọc render của đúng bốn tệp, ghi riêng vị trí câu ở hai doctrine, sáu gạch đầu dòng ADR nguyên văn + không thêm quyết định + `r208c` + fragment, và đoạn changelog tiếng Anh khớp hành vi mục tiêu 1; từng dòng có đạt/không đạt, trích dẫn, thiếu dòng là chưa review. Đây là kiểm độ rõ của hợp đồng R1, không phải nhận R1 đã đạt trên PR code chưa tồn tại. D1/D3/H1 không còn khai chứng minh nội dung hay render ngoài phạm vi phép đo. Các giới hạn canary không kết luận thì không nạp, chống đệ quy qua biến tắt ở child, danh sách cho phép retry đọc và không chuyển tiếp stdout/stderr child đều được viết rõ. Không nêu race liên tiến trình hay “lần cuối quyết định” thành finding; chúng là giới hạn chủ kho đã chấp nhận.

**ĐỐI CHIẾU LƯỢT TRƯỚC.** Bundle không có VERDICT gốc r7; nguồn đối chiếu là r7 + `errata_r8` (head r7 `bc1d5e04`, review `6488aa67`, một P2 thuộc lớp `thuoc-do-chuoi-khong-khop-markdown-nguon`; ID finding gốc không được cung cấp). Không tự gán ID hoặc khai đã đọc verdict gốc. Bộ phân tích Markdown cũ không được sửa; không đánh dấu lớp cũ “ĐÃ VÁ THẬT”. Theo authority đã cung cấp trong PROMPT, E23 thay phạm vi máy và đưa đọc nghĩa/render sang R1. Phép đo độc lập ở trên xác nhận hợp đồng r8 mới có đúng phạm vi đó và các fixture D1/D2/D3/H1 đúng màu. Giữ lịch sử lớp, không coi việc hạ tiêu chí là bản vá parser, không mở lại quyết định đã chốt.

**Phần chưa chạy/chưa đo được:** A1–A11/A13 trên cơ chế tự nạp mới và `<CANARY>` mới trong `nlm_cli.py` (chưa có mã); fragment `wp1099_nlm_nap_lai` thật; F1/G1 full selftest và số N; bare Ruff K1; CI L1; M1 LIVE sau land. Các phép nguồn/fixture nêu trên là `passed`; các phần này là `not_run`, không gọi là pass hoặc “skipped” thành công. Đã đọc cấu hình CI tĩnh, không gọi GitHub. Không xác nhận lại lease, toàn bộ ref remote, lịch WP710 thực tế 30 phút, log bootstrap, độ tươi bundle LIVE hay quyền chủ kho ngoài bộ dữ liệu; chúng không bị đoán là 0/đã đạt. R8 đã buộc đo lại điều kiện lease khi cấp và dành M1 cho kiểm LIVE có duyệt riêng. Không cài thêm dependency, không fetch, không chạy Drive/NLM/GAS hoặc `tl` thật lên dịch vụ.

## (iii) FINDINGS

### F01 — P2 — `phep-do-bundle-khong-kiem-do-tuoi-nguon`

- **Tệp:dòng:** `ops/specs/cloud-setup-p3b-nlm-401-r8.md:181` (F3; liên quan mục tiêu 3, dòng 131).
- **Mô tả:** F3 khai sửa fragment mà không sinh lại bundle sẽ làm `bundle_fragment_check.py` ĐỎ do lệch TEST_ID/băm. Với sửa thân fragment nhưng giữ TEST_ID, cổng chỉ chạy bản cũ trong bundle và so tập ID, không so byte nguồn. Vì vậy đột biến được khai có thể XANH, và bản bundle chưa chứa hành vi test mới vẫn đạt F3. Đây là lỗi phạm vi lời khai/thước đo của F3, độc lập với quyết định hạ D1/D3/H1.
- **Phép đo đã chạy:** `python -B review_checks.py > review-checks.log 2>&1` (exit 0). Script biên dịch hàm `main` thật của `.github/checks/bundle_fragment_check.py`; dùng hàm `cmd_release_bundle`/manifest thật từ `scripts/tl_core/release.py` để tạo ZIP fixture; driver thật chạy loader thật trong tiến trình vô hại với `tl.py` rỗng. Không chạy CLI `tl` thật, không mạng, không credential. Fixture có `TEST_ID = "wp1099_nlm_nap_lai"`, ban đầu `run` trả True: F3 rc 0/ok true; đổi thân sang trả False, giữ nguyên TEST_ID và bundle: F3 vẫn rc 0/ok true, trong khi `_test_fragments_check` nguồn trả `ok=false, error=GENERATED_BUNDLE_STALE`; sinh lại bundle thì F3 rc 1/`BUNDLED_FRAGMENT_FAILED` và freshness check xanh. Log/JSON giữ ngoài checkout.
- **Vá ở đâu/thế nào:** sửa F3 trong revision tiếp theo: giữ `bundle_fragment_check.py` để đo topology/hành vi và bổ sung phép riêng `python scripts/tl.py test-fragments-check --root . --json` (đòi rc 0, `ok=true`, `status=current`), hoặc so byte bundle với `generate_bundled_module_bytes`. Không cần sửa cổng ngoài write set; hàm kiểm freshness đã có ở `release.py:206`.
- **Ca khoá:** ba fixture trong script: nguồn/bundle đồng bộ ⇒ cả hai xanh; đổi thân giữ ID không sinh lại ⇒ freshness đỏ đúng `GENERATED_BUNDLE_STALE`; sinh lại ⇒ freshness xanh và phép đo hành vi phản ánh thân mới. Đã thêm đối chứng đổi tên/TEST_ID (rc 1, `TEST_ID_SET_MISMATCH`) để tách kiểm tập ID khỏi kiểm nội dung.
- **Nguy cơ khi vá:** chỉ chạy freshness check sẽ bỏ mất kiểm topology/hành vi; cần giữ cả hai phép. Không nhầm hash manifest của bundle với việc bundle khớp fragment (manifest có thể băm nhất quán chính bundle cũ).

### F02 — P3 — `tieu-chi-khong-khai-dot-bien`

- **Tệp:dòng:** `ops/specs/cloud-setup-p3b-nlm-401-r8.md:184` (G2; đối chiếu dòng 156 và `.claude/skills/soan-spec/SKILL.md:48`, `:120`).
- **Mô tả:** G2 để `—` ở cột đột biến và chỉ giải thích “canh bất biến; xanh sẵn trên nền”. Điều đó giải thích màu XANH của base nhưng chưa khai đột biến làm ĐỎ, trái lời mở đầu mục nghiệm thu và L3/L6 của skill. Cổng thật có thể ĐỎ; thiếu ở hợp đồng nghiệm thu, không phải kết luận cổng vô hiệu.
- **Phép đo đã chạy:** `review_checks.py`, mục `G2_baseline`: hàm `cmd_doctrine_scan` nguồn trên checkout trả rc 0, quét 10 tệp, 0 chỗ chép doctrine. Đối chứng âm ngoài checkout: tạo `review-fixtures/doctrine-probe.md` chứa cụm cấm `3 attempt/packet`, truyền nó bằng `a.path` vào cùng hàm nguồn ⇒ rc 6, finding `nguong-so-stop-conditions`. Phép này là đo bổ sung của reviewer, chưa được r8 quy định. Bỏ cụm cấm thì cùng phép đo về rc 0.
- **Vá ở đâu/thế nào:** điền đối chứng âm cụ thể tại G2 trong revision mới, cùng fixture, mã thoát và lý do dự kiến. Dùng hàm nguồn với `--path` trỏ fixture ngoài cây; giữ riêng mệnh đề base xanh. Không phải sửa scanner hay mở rộng write set code.
- **Ca khoá:** base rc 0; fixture có cụm cấm ⇒ rc 6 và đúng nhóm lỗi; bỏ cụm ⇒ rc 0. Không dùng lỗi cú pháp/setup để nhận là giết đúng lý do.
- **Nguy cơ khi vá:** tuyệt đối không chèn câu thử vào doctrine thật; không suy “scanner sạch” thành đã review đúng toàn bộ nội dung ADR (phần đó vẫn ở R1).



## (iv) TỔNG

| Mức | Số finding còn mở |
|---|---:|
| P0 | 0 |
| P1 | 0 |
| P2 | 1 — F01 |
| P3 | 1 — F02 |

**2 finding / 2 lớp nguyên nhân.** F01: `phep-do-bundle-khong-kiem-do-tuoi-nguon` (P2); F02: `tieu-chi-khong-khai-dot-bien` (P3). Cách đóng từng lớp và đối chứng dương/âm nằm ở từng finding. Hai lớp này không được ghép với lớp Markdown lịch sử chỉ vì cùng liên quan nghiệm thu.

**Kết luận: request_changes.** Cần sửa hợp đồng F3 và bổ sung đối chứng G2 trong revision mới; không sửa đè r8 đã băm. Đây là verdict review đặc tả trên exact SHA/tree nêu đầu tệp, không là approval PR code, merge, deploy hay LIVE.
