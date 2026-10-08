verdict: approve
reviewed_sha: cd25aba0fab9831dd7e87ba378b7429fa0602166
spec_sha256: f39091a1d2be7629a11eb53b7daf3f076ce91f701012f7093108a98e91d140cc
reviewer_provider: openai_codex
reviewer_model: gpt-6.1-sol
execution_surface: codex_cli
transport: machine

Kết luận: **0 P1 / 0 P2 / 0 P3 trong phạm vi hẹp của Q16.** Phần cắt phù hợp Stable Slice; các vùng bất biến khớp byte; không còn nghĩa vụ chạy phép kiểm kê động trong packet r17. Bốn lựa chọn (a)–(d) đều chấp nhận được với cách đọc cụ thể dưới đây. Không có lớp mở nên không sinh `HINT.patch`.

Lớp `tuong-tac-677-kiem-ke-t70-chua-neu` và F16-1/F16-2 là **CHUYỂN GIAO sang §11**, không phải ĐÃ VÁ THẬT. Verdict này review đặc tả trên exact SHA, không xác nhận các điều kiện cấp lease đang thoả hoặc thay thế gate của lượt thi hành/land.

Model đọc từ header phiên trong `codex-run.log`: OpenAI Codex v0.160.1, `model: gpt-6.1-sol`, effort `xhigh`. Đây là thông tin header, không phải phép đo độc lập backend. Phiên này khác provider với phiên soạn Claude; không dùng subagent. Không mạng, không đăng GitHub, không commit/push, không sửa `cay-kho/` hoặc `kho.git`; mọi artifact reviewer nằm dưới `goi/`.

## Bước 0 và phép đo độc lập

`sha256sum PROMPT.md SPEC.md SPEC-r16.md`, rc=0:

```text
bee7b436212c1d9d01fe41f9b810beb7767362aa2834d63e518d83e22debbaed  PROMPT.md
f39091a1d2be7629a11eb53b7daf3f076ce91f701012f7093108a98e91d140cc  SPEC.md
38637ba34099ece359d55baa160edeccbe8d2066c2451ae0d9f77c2dae83bbe1  SPEC-r16.md
```

`git -C cay-kho rev-parse HEAD`, rc=0: `cd25aba0fab9831dd7e87ba378b7429fa0602166`; `HEAD^{tree}`: `f4aaea576ab832fb8345fb08e36b7246eb630a50`. `GIT_OPTIONAL_LOCKS=0 git -C cay-kho status --porcelain`, rc=0, output rỗng. Không có `goi/VERDICT.md` từ lượt bị cắt khi bắt đầu.

Đã đọc AGENTS, CONTEXT, PROTOCOL, CLAUDE, kế hoạch đa provider và ADR-0037. Khi kiểm các trích dẫn có tọa độ trên `ab457c6`, đọc **blob của ref `master-ab457c6`**, không lấy tọa độ từ cây nhánh soạn.

Lệnh tái lập chính: `python3 -B goi/evidence/measure.py`, **rc=0**, output cuối `ALL_MEASUREMENTS_PASSED`. Script do reviewer viết, cắt trực tiếp byte từ hai SPEC và gọi `cmp` thật; không lấy các tệp `r17do/vung` làm kết quả đo. Có 23 lệnh `cmp` trong script, tất cả rc=0, stdout/stderr rỗng. Lệnh `diff -u` rc=1 là kết quả mong đợi khi hai revision khác nhau. Lệnh và rc/output đầy đủ: [measure-commands.txt](evidence/measure-commands.txt); dữ liệu máy đọc: [measure.json](evidence/measure.json); script: [measure.py](evidence/measure.py).

| vùng | r16 | r17 | byte sau phép chuẩn hoá được nêu | phép đo |
|---|---|---|---:|---|
| A1–A7 | 1050–1198 | 1100–1248 | 19152 | `cmp evidence/A1-A7.r16 evidence/A1-A7.r17`, rc=0 |
| A9 | 1560–1687 | 1337–1464 | 14961 | `cmp evidence/A9.r16 evidence/A9.r17`, rc=0 |
| A10 | 1688–1692 | 1465–1469 | 388 | `cmp evidence/A10.r16 evidence/A10.r17`, rc=0 |
| closure, kể cả các ghi chú tới GIỚI HẠN LỜI KHAI | 524–675 | 541–692 | 18502 | `cmp evidence/closure.r16 evidence/closure.r17`, rc=0 |
| danh sách write set | 955–959 | 1005–1009 | 75 | `cmp evidence/write-set.r16 evidence/write-set.r17`, rc=0 |
| §6 mục tiêu | 1022–1044 | 1072–1094 | 2283 | `cmp evidence/objectives.r16 evidence/objectives.r17`, rc=0 |
| hàng objective | 36 | 53 | 399 | `cmp evidence/objective-row.r16 evidence/objective-row.r17`, rc=0 |
| khối lệnh cấp, không tính fence | 64–100 | 81–117 | 4270 | `cmp evidence/grant-commands.r16 evidence/grant-commands.r17`, rc=0 |
| mã `s5.py` | 120–326 | 137–343 | 9886 | `cmp evidence/s5.r16 evidence/s5.r17`, rc=0 |
| toàn mục Chuỗi lệnh tới closure | 54–523 | 71–540 | 44091 | `cmp`, rc=0 sau duy nhất đổi câu lịch sử `r14, r15 và r16` → `r14, r15, r16 và r17` |
| năm điều kiện cấp trong depends_on | 42 | 59 | 3145 | `cmp`, rc=0 sau duy nhất đổi `từ r16, đó là revision 16` → `từ r17, đó là revision 17` ở (3) |
| hàng review_class; hàng reviewer | 37; 41 | 54; 58 | 96; 3605 | hai `cmp`, rc=0 |
| A8 trước câu nối về (iii) | 1199–1227 | 1249–1277 | 3584 | `cmp`, rc=0 |
| phép quét lồng và G − D, trừ dòng cuối ghép động | 1229–1236 | 1279–1286 | 1250 | `cmp`, rc=0 |
| dòng cuối G − D trước đoạn động | nửa đầu 1237 | 1287 | 27 | `cmp G-D-last-line.r16 G-D-last-line.r17`, rc=0, chỉ kết thúc dòng sau dấu chấm |
| định nghĩa (S), tới trước hai câu nối | 1282–1294 | 1288–1300 | 1977 | `cmp`, rc=0 |

Các tên `evidence/…` trong bảng được chạy từ `goi/` tương đương lệnh có tiền tố `goi/` trong log. `git hash-object --stdin < goi/evidence/s5.r17`, rc=0: **`c730245ceea8cc5368d5ef84f8e296cd35102694`**.

## Phần cắt: kiểm hết các vùng đổi

Diff tự sinh khớp `r16-r17.diff` từng byte sau hai dòng header timestamp (`cmp`, rc=0). Reviewer đối chiếu hết **28 vùng đổi theo dòng**, không chỉ các vùng được phiên soạn liệt kê. Chi tiết: [diff-audit.txt](evidence/diff-audit.txt).

| dòng r16 bị đổi / điểm chèn | nội dung và phân loại phạm vi |
|---|---|
| 1, 3–25 | revision, bảng mô tả cắt A8, giới hạn, dòng bỏ và số đo nền mới; hồ sơ của chính lần cắt |
| 31–32, 35, 42–43, 47, 55 | revision/nguồn r16, verdict/checkpoint/Q16, số đo drift; đổi số revision ở (3), tên tệp băm và câu lịch sử chuỗi lệnh; các vùng nội dung được ghim đã `cmp` riêng |
| chèn trước 924, trước 955 | Q13/Q15 không còn đối tượng và nguyên văn Q16; đánh dấu lời lịch sử, không cấp việc mới |
| 960 | tên hồ sơ đặc tả r17 và dải revision r1–r16 |
| 1002–1003, 1008 | R12/t199 chuyển neo về §10; bỏ các vế N/K/H động khỏi câu phát hiện; giữ nghĩa vụ (i)–(iii) |
| 1228, 1237–1281, 1295–1559 | bỏ quét động, sửa ba câu nối, giữ các định nghĩa/chốt tĩnh; đưa số (S) tĩnh từ đoạn đo cũ lên phần còn hiệu lực; thêm giới hạn Q16 và chuyển hướng A3 |
| chèn trước 1717, 1724 | số nền mới, ghi rõ số suite/ruff/chuỗi vẫn là lịch sử có nhãn |
| chèn trước 2020, 2265–2284 | hướng đọc lịch sử §9; bỏ bảng xếp nhóm; bộ đếm sau lượt 16 và chuyển giao theo checkpoint |
| chèn trước 2608, 2672, 2700, 2706–2707 | ghi chú số đo r17 và đánh dấu các tham chiếu động ở §10 là của r11–r16 / §11 |
| chèn trước 2773 | §11 hồ sơ Remediation Slice, chưa mở |

Không có đổi ngoài cơ chế cắt, tham chiếu của nó hoặc định danh/số liệu của revision mới. Chuyển vị trí số đo (S) không xoá tiêu chí tĩnh: luật AST r13 giữ byte và các số chuyển vị trí khớp đoạn A8 r16 :1509–1533. Không có thay đổi nghĩa vụ ID/YAML, A1–A7, A9/A10, closure, write set hoặc chuỗi cấp.

## Không câu treo và phán bốn lựa chọn

Đã rà cả từ khoá lẫn đọc các đoạn còn hiệu lực. [references.txt](evidence/references.txt) ghi 61 dòng khớp `quet13/14/14b`, `setprofile`, `(δ)`, `H2`, `(q1)`–`(q5)`, vế K/H/N/L, luật xếp nhóm và phép quét động. Đây là bộ lọc từ khoá, không phải danh sách đầy đủ nghĩa vụ; reviewer còn đọc §3–§7, closure và các đoạn giới hạn/chuyển hướng.

| lựa chọn | phán và cơ sở |
|---|---|
| (a) A3 giữ byte, chuyển hướng trong A8 | **Chấp nhận.** A3 :1214 còn hai câu động. Đọc riêng đoạn ấy có thể tưởng phép đo vẫn tồn tại, nhưng hợp đồng r17 ghi ngay đầu rằng A8 động đã bỏ; A8 :1331–1336 trích đúng hai câu và chỉ rõ cách đọc từ r17: cổng tĩnh chỉ có thể bắt khi có dấu đọc được; kết cục ngoài ứng viên `t193` không còn phép đo trong packet. Câu còn lại ở A3 :1212, “vi phạm ấy chỉ lộ ở phép quét của A8”, được :1335–1336 neo đúng phép quét lồng tĩnh. Đọc cả đặc tả không sinh yêu cầu chạy vế K hay quét động. Không sửa A3 vì Q16 ghim A1–A7. |
| (b) còn kiểm lồng và G − D | **Chấp nhận.** Chúng là kiểm code-object tĩnh của chính vị từ `t70` và ứng viên `t193`, có từ r10, không phải phép quét mọi ca dưới seam. Đã đọc `_ca_doc_than_buoc` :3393–3394 và `_ca_ung_vien_gian_tiep` :3415–3431 trên blob nền: đọc `co_names` / đi theo hàm cấp module; không gọi thân ca. Cách diễn giải “cổng tĩnh t70/t193/(S)” có thể giữ các phép kiểm cùng vị từ này; r17 :997–999 khai rõ lựa chọn. Giữ chúng không mở lại A8 động. |
| (c) ba câu ở :1278, :1301–1304 | **Chấp nhận.** :1278 thay lời hứa đo “toàn bộ (iii)” bằng giới hạn ứng viên/`BoQuaNen` của `t193`. :1301–1302 bỏ q2/q4/q5 khỏi câu vị trí/hiệu ứng, ghi rõ t193 chỉ chạy ứng viên; :1303–1304 thay điều kiện q1–q5 bằng các cổng thật còn đứng. Đây là thay tổ hợp nghiệm thu được Q16 giao, không đổi định nghĩa hay ngưỡng phần tĩnh: suite delta 0; t70 1/1 ở hai bản; chỉ lồng `{t70}`; G − D bằng nền; (S) không thêm lần bị ĐỎ. Câu “nghĩa vụ được đo là đạt” phải đọc cùng :1319–1330: đây là mức phủ hữu hạn, không chứng minh mọi ca cố ý né làm đúng (iii). Nghĩa vụ executor ở §4 vẫn nguyên. |
| (d) master 19ca703, giữ nền ab457c6 | **Chấp nhận cho nền nghiệm thu.** Điều kiện cấp (4) nhìn hai tệp write set, không đòi dời nền chỉ vì master có commit mới. Đo dương cả diff rc=0 và ls-tree đúng hai blob ở hai ref; closure/policy không đổi. PROTOCOL §5.1 là luật cho reuse gate khi merge, không phải lệnh luôn dời nền đặc tả. Drift thực sự chạm workflow, tức kích hoạt (6) phải được đối chiếu lúc land; giữ nền không miễn hậu-merge gate. r17 không tuyên bố được reuse gate hay đã đủ điều kiện cấp; bước (v) và mọi điều kiện phải đo lại lúc cấp. |

Những hit còn lại ở đầu tệp, §3 Q15, §9 và §10 là lời lịch sử/trích dẫn hoặc lời khai đã bỏ; §9 :1800–1806 neo đoạn động lịch sử về r16, §10 :2394–2407 cùng các nhãn tại :2472, :2500, :2506–2507 làm tương tự. §11 là hồ sơ bàn giao, được :2576–2579 loại khỏi objective/write set/nghiệm thu. Không có yêu cầu còn hiệu lực chạy `quet14b`, cài profile, lập H2/K/H/N/L, q1–q5 hay áp luật xếp nhóm.

## Bảng số mới và các neo

Các lệnh Git dưới đây chạy trên mirror đã cấp, không liên lạc máy chủ. Băm, byte/dòng comment đo trực tiếp `body` UTF-8 từ JSON đã cấp, không nhận số trong transcript phiên soạn làm kết quả. Tọa độ trong bảng là của SPEC r17 trừ khi nêu r16.

| lời khai mới / được chuyển vị trí | phép đo, rc và output |
|---|---|
| r16 2889 dòng; r17; diff 738 dòng | `wc -l SPEC-r16.md SPEC.md r16-r17.diff`, rc=0: **2889 / 2746 / 738** |
| bỏ trọn 327 dòng, :38–40 | đếm dải r16 1238–1281 = **44**, 1297–1559 = **263**, 2265–2284 = **20**; tổng **327**. Mỗi dòng thuộc vùng delete/replace của diff. `cut-counts.json`, rc=0. Đây không phải toàn bộ dòng diff bỏ/thay: tổng ấy là 367, mới/thay 224; net −143, đúng 2889→2746. Nửa sau :1237 và hai câu :1295–1296 được khai riêng. |
| các dải r16 ở :978–979, :1803–1804, :2590–2594 | cắt đúng mốc trên blob đã băm: **1237–1281, 1297–1346, 1347–1463, 1464–1508, 1487–1508, 1509–1559, 2265–2284**; đầu/cuối đúng tiêu đề và nội dung được mô tả, trong `r16-range-anchors` của measure.json |
| r16 commit tạo, cha, số commit chạm, băm, dòng, :49 | `git log --diff-filter=A`, `rev-list --count … -- <r16>`, `rev-parse e39b73e^`, `git show`; rc=0: **e39b73ed6f054178211c228e7d886eb9ed981f43**, **b53362159766f51c1a03c5eac65efd94544d8ce9**, **1**, **2026-10-08T00:04:19+00:00**; blob 395491 byte, cmp với SPEC-r16 rc=0; băm **38637ba3…bbe1**, 2889 dòng |
| r17 blob tại exact reviewed SHA | `git show cd25aba…:ops/specs/lease-id-ep-kieu-yaml-r17.md`, rc=0; 375425 byte; cmp với SPEC.md rc=0 |
| master mới và ngày merge, :14–15 | `git rev-parse origin-master`, `git show --format=%cI`, rc=0: **19ca703328b6c2f0c578480692ea48e76af59e65**, **2026-10-08T10:21:33+07:00** = **03:21:33Z** |
| ahead 5 / behind 0 / 4 tệp, :15–18, :60, :1504 | `rev-list --count base..master` / ngược; `diff --name-only`, rc=0: **5 / 0 / 4**. Tệp: `.claude/dev/ci_dang_ky_test.py`, `.github/workflows/ci-dot-bien-du.yml`, `.github/workflows/ci.yml`, `ops/ci_duong_nhanh_test.py`. Không giao write set, docs hoặc `.github/coordination/`. |
| blob hai tệp giống hệt | `git diff --quiet master-ab457c6 origin-master -- ops/lease_publish.py ops/lease_publish_test.py`, rc=0; `git ls-tree` hai ref, rc=0, mỗi ref đúng **2** dòng, mode **100644**: **93cff2f97e01ebf41c18a4c5a1bd90343b343bbe**, **7dd06ab6e71a1fae73a29fca31df4a9b271aa081** |
| ci.yml 90→105, hai chú thích :836–837; :628/670/711 giữ nguyên | `git diff … -- .github/workflows/ci.yml`, rc=0: chỉ **2** dòng chú thích mới và **timeout 90→105**. Ba dòng trích `cmp` rc=0. Tên cả bốn job required_checks vẫn có; diff không đổi tên/job commands. |
| VERDICT/HINT lượt 16, :49, :2600–2602 | `sha256sum`, `wc -l`, `rg -c '^@@'`, `rg '^# lop:'`, rc=0: VERDICT **87e333f9ce96b7570f839c5767c6a58c9b38fa883a5155c42869a49c5aec0108**, **334** dòng; HINT **21bff7d5f26c318efa5d9147658a49b04d94af9dd71ac1eb7a19a89f7b12d057**, **111** dòng, **1** nhóm, **5** hunk |
| bản chiếu 6051498946, :49 | body JSON: **2915** byte, **27** dòng, **0** thực thể HTML, SHA-256 **2a67e30dc76da8138513ac48638d293a699386182c0efd661c6a821594f62f15**, tạo **03:21:49Z**; tự nhận bản chiếu và chứa đúng hai băm artifact lượt 16 |
| checkpoint 6051500946, :49 | body JSON: **2638** byte, **19** dòng, **0** thực thể, SHA-256 **6170d8b1a6b658000d3d3a1c9083918c84065175eea8caf57e1ad8a2b9099df5**, tạo **03:22:01Z**; nội dung có ba lựa chọn A/B/C, r17 chọn A đúng Q16 |
| Q16, :982–987 | body JSON: **1362** byte, **12** dòng, **0** thực thể; SHA-256 **eafa06b4c95b2b1363967229b5b36f31141fd00d90a33b6021566652940be45f**; id **6051538693**, tạo **03:25:41Z**, user **ducthangho**, app **claude**, association **OWNER** |
| nguyên văn Q16 dòng 3–9, :988–994 | bỏ duy nhất prefix Markdown `  >` của SPEC, giữ byte nội dung và dòng trống; `cmp q16-quote-lines-3-9.r16 q16-quote-lines-3-9.r17`, **rc=0**, **1235 byte** mỗi bên |
| (S) r13 chuyển vị trí, :1305–1318 | so trực tiếp đoạn r16 :1509–1533: **38 = 26 + 10 + 2**, **ĐỎ 25 / xanh 13 = 5 + 7 + 1**, đột biến **18 + 7 = 25** và hai tập rời; loại nút HINT **2**, mặc định **1**; ngày/giờ/bản Python đúng số r16. Đây là số lịch sử có nhãn, không khai đã chạy lại bộ biến thể ở r17. Các quan hệ bắt của t193 khớp phần A2 và số lịch sử trong r16. |
| số nền chuyển sang §11 :2596–2597 | so r16 :1433–1437 và VERDICT16: **201 = 187 + 12 + 2**, K **{t199,t203}**, H−D **{t193}**, H2−D **{t71,t72,t73,t98,t193,t203}**; khớp. Đếm AST blob nền có **201** ca @ca, rc=0; không chạy quét động. |
| sáu finding / chín lượt / hai chuyển tiếp 0%, :2052–2070 và §11 | bảng §11 giữ đúng **6 ID**; lượt **8–16 = 9**. VERDICT16 và bản chiếu15/16 khớp **14→15 0/1**, **15→16 0/1**, **1/2 theo finding ở 15→16**. Chuỗi cũ r17 chép khớp đoạn bộ đếm r16 :2244–2247; không đếm chuyển giao thành F trong tỷ lệ theo §12. |
| trích PROTOCOL mới :1087–1100 | `git show master-ab457c6:docs/PROTOCOL_DA_PHIEN.md`, rc=0: :1087–1093 định nghĩa U/F và hai chuyển tiếp <50%; :1098–1100 một lớp ở ba lượt và scope cut không reset. Đúng tọa độ trên nền. |
| băm/1175 byte cấu hình reviewer lặp ở §10 :2401–2403 | băm **e225b81c…792c**, **1175** byte và frontmatter đã có trong closure r16; vùng ấy cmp rc=0. Không có bản byte định nghĩa người dùng trong bundle để đo lại nguồn ngoài kho; chỉ xác nhận lời khai r17 khớp pin cũ. Không coi lời khai này là phép đo model/runtime hoặc thay thế việc kiểm lúc giao reviewer. |

Các lần đọc REST và mtime FETCH_HEAD của phiên soạn là lời khai lịch sử, đối chiếu với `r17do/t_rest_*.txt` / `t_adg2.txt`; không thể tự tái tạo thời điểm đọc của phiên khác. Reviewer không truy vấn lại máy chủ. Bằng chứng về commit/tree/blob/drift dùng Git đã cấp; về nội dung/comment metadata dùng JSON đã cấp. Số của các phép thử động cũ chỉ được kiểm việc chép/neo nguồn, không đo lại hoặc mở lại lớp động.

## Đối chiếu lượt trước và §11

| lớp/finding lượt 16 | trạng thái trong r17 | phép kiểm độc lập |
|---|---|---|
| `tuong-tac-677-kiem-ke-t70-chua-neu` (P2) | **CHUYỂN GIAO**, vẫn giữ lịch sử 8–16; không tính ĐÃ VÁ THẬT | vùng A8 r16 :1237–1281/:1297–1559 và bảng :2265–2284 không còn là acceptance r17; §11 loại khỏi packet rõ ràng |
| F16-1, luật xếp không tất định | **CHUYỂN GIAO, chưa vá trên phần động** | r17 không chứa luật xếp nhóm còn hiệu lực; §11 :2610 giữ nguyên ID, bốn biểu hiện và neo **6051498946** khớp VERDICT16/bản chiếu |
| F16-2, (δ) không bao hết | **CHUYỂN GIAO, chưa vá trên phần động** | r17 không còn hứa nhóm vét; §11 :2611 giữ G1/G1b, cơ chế q3/q5 so tập tên và neo **6051498946** khớp nguồn |

Nhãn “chuyển giao” phản ánh Q16 và §12; không ép nó vào nhãn “ĐÃ VÁ THẬT” để làm tỷ lệ hội tụ đẹp hơn. Chuỗi hai chuyển tiếp 0% vẫn kích hoạt checkpoint; số lượt không reset. Approve phần lõi độc lập không đóng slice kế nhiệm.

Kiểm sáu hàng §11 :2606–2611 với `r17do/comments.json` và `luot16/VERDICT.md`:

| ID | neo nguồn | trạng thái/chuyển tiếp được chép | kết quả |
|---|---:|---|---|
| F14-1 | 6042680156 | VÁ HỜ ở 15, nối F15-1 | khớp mô tả E8n/E8n2 của bản chiếu14 và phần đối chiếu của bản chiếu15 |
| F14-2 | 6042680156 | ĐÃ VÁ THẬT ở 15 | khớp V1/V6 và 9 ca; bản chiếu15 ghi rõ đã vá |
| F15-1 | 6049075233 | VÁ SINH LỖI MỚI ở 16 | khớp sáu D1–D5/D7, VERDICT16 giữ ID và sinh F16-1/F16-2 |
| F15-2 | 6049075233 | ĐÃ VÁ THẬT ở 16 | khớp V10, 3.12 chết 1/20 và 1/5; VERDICT16 phân loại đã vá |
| F16-1 | 6051498946 | MỞ, chuyển giao | khớp bốn chỗ và hai chỗ đổi phân hạng |
| F16-2 | 6051498946 | MỞ, chuyển giao | khớp G1/G1b, quét đủ hai bản, lỗ tên có sẵn trong K |

Bảng lịch sử §11 :2618–2626 có đúng chín lượt và các neo đều có trong JSON, đúng revision/lượt/lớp. Bản chiếu là tóm tắt; artifact đầy đủ lượt14/15 không nằm trong bundle nên không khai đã băm lại chúng. Những số và kết luận chi tiết của hai lượt đó được đối chiếu nguồn bản chiếu và đối chiếu trong VERDICT16 theo đúng cách §11 tự mô tả.

§11 giữ finding IDs, trạng thái đã vá của một số finding cũ và toàn bộ lịch sử, không biến chúng thành finding mở của Stable Slice. Câu hỏi “có nên làm hay không” cùng trạng thái packet riêng/chưa mở khớp Q16; không tạo Issue/lease/authority mới. Giới hạn A8 :1319–1330 khai đúng mức phủ: ứng viên tĩnh, t193 chỉ ghi BoQuaNen, khả năng ca cố ý né qua cổng và Windows thật chưa đo. Gate `human_audited` cùng nghĩa vụ (i)–(iii) vẫn đứng, closure đã cmp giữ byte.

## BẢNG SĂN — trong giới hạn đã khai, không phải finding

Không dựng hay chạy biến thể động mới. Bảng ghi mọi cơ chế né được xem xét trong review này; nguồn các biến thể là r16/VERDICT16 và phần giới hạn r17, không phải kết quả chạy mới của Codex.

| cách viết test cố ý né được xem xét | ví dụ / nguồn | cách đọc ở r17 |
|---|---|---|
| tên helper chỉ trong hàm lồng/lambda/generator/comprehension; gọi qua hàm bọc | §4, A2; họ N/R lịch sử | kiểm lồng/G−D bắt một số dạng; mọi dạng không để lại dấu mà các kiểm tĩnh đọc được thuộc giới hạn Q16 |
| lấy helper qua globals/getattr/partial/bí danh/decorator/mặc định/phương thức lớp, tự bắt BoQuaNen để giấu kết cục | N4, N8; §4 :1058, lịch sử r16 | qua các kiểm tên theo số cũ; ghi bảng săn, nghĩa vụ (i)/(ii) vẫn cấm |
| gọi helper ở luồng khác hoặc biến đổi BoQuaNen thành ngoại lệ khác | M5, M6 | t193 bỏ qua ngoại lệ khác / không thấy luồng; giới hạn của (iii) đã khai |
| nạp lại module/dựng bản sao helper, dùng tên trong thân hàm thay vì lần AST bị cấm | E8a–E8l, E8n/E8n2, E8r–E8v; E8m được t70 bắt | khả năng qua t70/t193/(S) là lịch sử đã khai; bỏ cổng động không làm nó thành finding r17 |
| bản sao helper ở luồng thô, lúc nạp/lúc thoát, đổi hay tắt hàm profile, đổi nhận dạng guard/os | E8e/E8g/E8l/E8p/E8q/E8u/E8v | không còn luật nhóm/profile động trong packet; chuyển §11 |
| tiến trình con; dựng tên helper để không tăng lần AST có chuỗi con | E5f; E5g/E5i là đối chứng bị (S) r13 bắt | ca thật sự lọt (S) đã thuộc giới hạn; không đòi dựng phép quét động bắt nó |
| đọc tên module, os.name ngoài guard, sys.getprofile, sys.platform hoặc phối hợp biến môi trường | D1–D5, D7; G2 | khác biệt seam/Windows được khai; không mở lại tranh luận (δ) hay phép thử một biến |
| sửa ca đã nằm trong K nền để kết cục tên tập vẫn bằng nền | G1 (`t199`), G1b (`t203`) | F16-2 giữ ở §11, không đếm là vá thật; không có cam kết r17 bắt cách né này |
| dùng sys.argv/sys.modules/đầu ra/lịch luồng/đồng hồ/ngẫu nhiên, hoặc giữ đa tập AST mà thay hiệu ứng | suy luận từ mức phủ cổng; r16 :1475–1476, không có phép đo biến thể mới | chỉ là hướng săn, **not_run**; Q16 không hứa chống test đối kháng và không yêu cầu xây nhóm vét mới |

## Nhật ký và giới hạn phép đo

- Bước 0 khớp hash/HEAD; tạo VERDICT tạm `blocked` để lượt bị cắt không để lại approve chưa hoàn tất.
- Tự sinh diff theo dòng/ký tự; rà hết 28 vùng; lưu bản byte cắt và gọi `cmp`.
- Lần đầu script reviewer thiếu LF trong mốc fence `python`, gây `StopIteration` sau các cmp đầu. Sửa chính script và chạy lại toàn bộ; lần hoàn chỉnh rc=0. Log lần lỗi giữ ở `measure-attempt1.err/out`; không tính đó là lỗi của đặc tả.
- Đo Git drift/CI/nguồn spec; đo Q16 và artifact lượt16; đối chiếu finding IDs/neo nguồn; đọc và phân loại các tham chiếu động còn lại. Bổ sung kiểm dòng cuối G−D, phủ đủ 327 dòng và AST đếm 201 ca.
- Hoàn tất bốn lựa chọn, bảng số và bảng săn; kiểm toàn vẹn cuối ở [final-integrity.txt](evidence/final-integrity.txt); thay verdict tạm bằng kết luận này.

**Passed:** so byte, source OID/hash, diff, dải dòng, comment body/quote, drift và neo chuyển giao. **Not_run:** suite nền/ứng viên, s13 trên 38 biến thể, mọi quét động, chuỗi cấp trên kho thật và gate land; đây là review đặc tả/phạm vi cắt, không phải lượt thi hành. **Không đo được:** máy chủ hiện thời, giờ đọc/mtime lịch sử của phiên soạn, model thực phục vụ phiên khác, định nghĩa reviewer ngoài bundle, Windows thật. Các giới hạn này không được ghi thành pass; phần động lịch sử không được review lại theo Q16.

Không có lớp P1/P2/P3 cần vá trong phạm vi được giao. Output không cấp authority ghi/land hoặc tự xoá lịch sử/nợ của Remediation Slice.
