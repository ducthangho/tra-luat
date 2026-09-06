verdict: changes_requested
reviewed_sha: 2d5fb722a3d4f43d4e884cca6f80825cc84f6d4e

Review PR #460, base `5898e5ff101b0bf3b3fb485bb0cfdbdf53c1f183`, tree được review `2aba8a989ac0184bbde94cb77c0f7c462e92a933`.
Reviewer: Codex, provider OpenAI, bề mặt service/API có shell Linux, transport `machine`; không có chứng thực độc lập model/backend hay launcher run của phiên này. Authority là chỉ thị review trực tiếp trong đề bài; không tự cấp Packet/lease/approval. **Verdict này không cấp quyền land.** Không có finding P1.

## ĐỐI CHIẾU LƯỢT TRƯỚC

- R8-01: **ĐÃ VÁ THẬT** — `m56/m57` chết ở đúng mã thoát của lượt mất riêng neo tương ứng; `m58` chết ở parity với oracle độc lập. Gỡ hai lượt thì `m56/m57` sống; cho `c43` hỏi oracle từ sản phẩm thì `m58` sống. Đối chứng `c18` đều sạch. Đã chạy lại mutant trên suite base để kiểm lời khai sống trước vá.
- R8-02: **ĐÃ VÁ THẬT** — CHANGELOG hạ kết luận CLI xuống nghi vấn, nói rõ không có trace lịch sử. Ba lượt hook thực đo cùng rc=0 nhưng lần lượt stdout rỗng/`ask`/`deny`; ghi lại bytes trên bản sao thành công. Không suy phép ghi hiện tại thành phép đo phiên executor cũ.
- R8-03: **ĐÃ VÁ THẬT** với ba phản chứng cũ — sáu lượt nguồn, hai mẫu số transport và ba tập của `m49` đều khớp. Chuỗi bốn đợt đã được nêu tên và định nghĩa; không còn gộp đối chứng vào năm nguồn hỏng. Tuy nhiên phát biểu bao quát “mỗi con số … mang điều kiện đo” vẫn chưa đúng với mọi đoạn, và phần bổ sung sinh số đếm sai khác: xem F07.
- R8-04: **ĐÃ VÁ THẬT** về hành vi — sáu giá trị hỏng đang bị từ chối, trường vắng và giá trị hợp đồng vẫn qua. `m59` chết đúng vì nhận sai năm giá trị. **Độ phủ hồi quy chưa kín:** bỏ riêng chặn `None` vẫn xanh toàn suite; F02.
- R8-05: **ĐÃ VÁ THẬT** ở hàng Antigravity — sửa đúng transport, có thay đổi hành vi hai chiều. “Duy nhất lệch” chỉ được chứng minh ở cột transport của năm hàng, còn `c44` chưa chứng minh đầy đủ bộ ba/receipt được nhận như mô tả; F04/F05.
- R8-06: **VÁ SINH LỖI MỚI** — bác “master đỏ vì squash” là đúng trên mirror: master có hai cha, tám neo đều là tổ tiên, cổng biên nhận master sạch. Nhưng blockquote mới làm vỡ bảng README và `t27` đỏ; `c45` nhận lỗi Git 128 thành kết quả đo hợp lệ; caveat “khi và chỉ khi merge commit” quá rộng. F01/F03/F06.

## BẢNG ĐO

Các lệnh Python chạy với `PYTHONDONTWRITEBYTECODE=1`. `TMPDIR`, cache pip và mọi bản sao nằm trong `rv9-audit/` tại thư mục được giao; pip chạy với `PIP_NO_INDEX=1`, Git chỉ cho giao thức file. Không gọi mạng. Linux, Python **3.11.15**, PyYAML **6.0.1**, `core.abbrev=7` khớp EVIDENCE. Lệnh baseline chạy từ `cay-kho/`; các ngoại lệ là bản sao ghim SHA hoặc phép đột biến, ghi rõ bên dưới. Mã thoát lấy từ `CompletedProcess.returncode`, không từ pipeline.

Log nguyên stdout/stderr và kết quả JSON nằm ở [rv9-audit/logs](rv9-audit/logs). Các dòng tổng kết dưới đây giữ nội dung thật; bảng công bố đã lược vài từ so với stdout, không coi việc lược từ đó là sai số.

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| Exact head/base | `2d5fb72` / `5898e5f` | Git trả đúng hai OID đầy đủ ở đầu verdict | Có |
| Diff, `numstat.txt` | 7 tệp; từng hàng trong tệp | Cả 7 hàng byte-for-byte khớp `git diff --numstat`; cộng **522 thêm, 44 xoá**; `diff --check` rc=0 | Có |
| Môi trường | Linux / 3.11.15 / PyYAML 6.0.1 / abbrev 7 | Đúng cả bốn | Có |
| Mirror đầy đủ | Không nông; 298 ref | `--is-shallow-repository=false`; **339 ref tổng**, **299 remote-tracking**, trong đó **298 nhánh origin + symbolic origin/HEAD** | 298 đúng nếu đơn vị là nhánh origin, không phải tổng ref |
| Hai nguồn trước clone | `298/298`, `comm -23` rỗng | Chỉ đo được 298 nhánh origin trong mirror; không truy vấn máy chủ | KHÔNG ĐO ĐƯỢC phép so hai nguồn |
| `ls-remote` ngoài sandbox | rc=128, 0 dòng | Không gọi do lệnh cấm mạng | Chưa đo; không coi là xanh |
| `python3 ops/bien_nhan_v2_test.py` | rc=0; 48/48, 62/62, 2/2, 44/62 | **rc=0**; `bien_nhan_v2_test: 48/48 ca đạt · 62/62 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 44/62 đột biến thường khai đối chứng`; `TỔNG: ĐẠT` | Có |
| `python3 ops/bien_nhan_v2.py --root .` | rc=0; 17, 11/11, 42, 0, 0, tổng 70 | **rc=0**; `bien_nhan_v2: 17 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 70`; `TỔNG: ĐẠT` | Có |
| `python3 .claude/dev/launcher_test.py`, lượt đầu | rc=0; 181/181, tổng 182, bỏ qua 1, hỏng 0 | **rc=1**; `172/173 ca DA CHAY QUA (tong 182, bo qua 9, hong 1) - KHONG DU: 9 ca BO QUA, chua do gi`; hỏng `t81` | Không; F08 |
| Launcher, đối chứng lặp cùng môi trường | Cùng con số công bố trên head | Head **rc=0** và base **rc=0**, cùng `173/173 ca DA CHAY QUA (tong 182, bo qua 9, hong 0) - KHONG DU: 9 ca BO QUA, chua do gi` | Không tái lập 181 ca; không chứng minh hồi quy |
| `python3 ops/lease_publish_test.py` | rc=1; 120/121; chỉ `t33` | **rc=1**; `lease_publish: 119/121 đạt; đã chạy=121, bỏ qua=0`; **t27 + t33** đỏ | **Không; F01** |
| Lease trên `origin/master=cacaba3` | rc=1; 120/121; cùng chữ ký, delta=0 | **rc=1**; `lease_publish: 120/121 đạt; đã chạy=121, bỏ qua=0`; chỉ `t33` đỏ | Số master khớp; **delta không bằng 0**, head thêm 1 lỗi |
| `python3 .claude/dev/ci_dang_ky_test.py` | rc=0; 51/51 | **rc=0**; `PHẢN CHỨNG: 51/51 đỏ đúng`; `TỔNG: ĐẠT` | Có |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | rc=0; 7 tệp, 0 chỗ | **rc=0**; `doctrine-scan: sạch — đã quét 7 tệp, 0 chỗ chép doctrine` | Có |
| Suite base `5898e5f` | 45/45, 57/57, 2/2, 39/57 | Bản sao ghim base: **rc=0**, đúng **45/45 · 57/57 · 2/2 · 39/57**, `TỔNG: ĐẠT` | Có |
| CLI base `5898e5f` | 70 receipt trước vá | **rc=0**, **17 đạt + 11 legacy + 42 nợ = 70**, không vi phạm/chưa đo | Có |
| Receipt ghi kết quả đợt đầu | 46/46, 60/60, 2/2; 17 đạt, tổng 70 | Bản sao ghim `d87f444`: suite **rc=0, 46/46 · 60/60 · 2/2 · 42/60**; CLI **rc=0**, 17 đạt/tổng 70 | Có tại `d87f444`, không phải số head cuối |
| Delta của PR | +3 ca, +5 mutant | **48−45=3**, **62−57=5**; CA cũ còn đủ; hai tự kiểm giữ nguyên | Có |
| Hai mutant trước vá | Mỗi cái sống qua 45/45, 57/57, 2/2, rc=0 | Hai bản sao base, áp nguyên phép thay của m56/m57 lấy từ AST head: **cả hai rc=0, 45/45 · 57/57 · 2/2 · 39/57, TỔNG: ĐẠT**; log `before-fix-m56-suite` / `before-fix-m57-suite` | Có |
| Oracle neo/nguồn | 3 bộ, từ 2 tệp; 2 neo PROTOCOL | **3 bộ**, **2 tệp**, **2 neo PROTOCOL**; đủ câu đúng một lần | Có |
| Parity | 11 hằng | `len(HANG_PARITY)=11` | Có |
| c28 “34 hàng” | 34 ở đoạn kể phép đo cũ | Base `5898e5f`: **34 hàng tuple**; head: **33 hàng tuple + 2 lượt neo riêng + 1 lượt hỗn hợp = 36 lượt** | Đúng số lịch sử; không phải số head hiện tại |
| Sáu lượt nguồn | 1 rc=0; 5 rc=2; cả 6 không vi phạm/traceback | Replay script R7 có sẵn, chỉ chép thêm PROTOCOL bắt buộc: **0,2,2,2,2,2**; mỗi lượt 70 receipt; **0 vi phạm, 0 traceback** | Có |
| Transport trên tệp tự khai v2 | `1/16 → 2/17` | Byte YAML từ **4488ff1 → c0f18ac**: **1/16 → 2/17** | Có |
| Transport trên receipt đạt v2 | `1/15 → 2/16` | Cổng head trên byte receipt hai mốc: **rc=0, 15 đạt/tổng 68 → rc=0, 16 đạt/tổng 69**; transport **1 → 2** | Có |
| Tập receipt head cuối | 17 đạt/tổng 70 | **18 tự khai v2**, 17 đạt; transport **3/18 tự khai**, **3/17 đạt** | Có; không thay số lịch sử bằng số này |
| Đếm transport bằng substring | 3/4 | **3 rồi 4 trên toàn bộ 68/69 YAML**; nếu chỉ tập tự khai v2 thì **2 rồi 3** | Khớp trên toàn bộ receipt; cần nêu tập, F07 |
| Provider chính tắc / bí danh / tên chép tay | `5→6` / `1→1` / `1→0` | Đọc AST các bảng và mã hai mốc: đúng; hằng chép tay `human` ở mốc cũ đã bị gỡ | Có |
| `m49`, ba tập hiện vật | `11/68`, `12/69`, `13/70` | Cùng mutant head, byte receipt tương ứng **4488ff1 / c0f18ac / 2d5fb72**: **11,12,13** cáo buộc ở lượt thiếu launcher; đều `giet_that`, đối chứng sạch | Có |
| Số thứ tự R7-01 | Bốn đợt, không tìm được đợt thứ năm theo định nghĩa | Đối chiếu verdict lượt 8 và diff lịch sử `b7a53ba`: bốn neo đã nêu phù hợp; không chạy lại mọi executor lịch sử | Khớp hồ sơ trong phạm vi đã đối chiếu |
| Ba lượt hook | Cả 3 rc=0; rỗng/ask/deny | Chạy hook, dùng các lệnh có sẵn trong test làm **dữ liệu**: **0/rỗng, 0/ask, 0/deny** | Có |
| Ghi Python / lớp CLI | Ghi được / CLI chỉ nghi vấn | Bản sao launcher ghi lại byte-identical; không có trace quyết định CLI lịch sử | Khớp giới hạn; không tái hiện phiên gốc |
| Kiểu transport trước/sau | Sáu giá trị hỏng trước 0 lỗi; vắng 0; chuỗi sai 1 | Base: **0 lỗi** cho năm giá trị ma trận và `None`; head: **1 lỗi mỗi giá trị**; vắng và `machine` vẫn 0; `human` vẫn 1 | Có |
| `m59` | 5/40 | **5/40 = 5 giá trị transport lọt / (8 trường × 5 giá trị)**; từng dòng là “cổng NHẬN” | Có; không bao gồm None |
| “6 trường còn lại đã chặn chuỗi rỗng” | 6 | Base có **7** trường, cả **7/7** chặn chuỗi rỗng | **Không; F07** |
| `m59` hình dạng `if False` | c34 qua, vẫn bị chặn bởi hợp đồng | Chạy c34 trên bản sao: **qua**; chỉ đổi chẩn đoán, không bỏ thuộc tính từ chối | Có |
| Năm hàng §2 | Antigravity duy nhất lệch | Trước vá: **1/5 lệch transport**; sau vá: **0/5**. Kiểm execution surface có caveat Codex service | Khớp riêng transport; F05 |
| Object `403fe125…` | Không tồn tại | `git cat-file -t 403fe125`: **rc=128**, `Not a valid object name` | Có trên mirror |
| Master là merge commit | `cacaba3`, hai cha | `git log -1 --format='%H %p' origin/master`: **cacaba3…**, **1b3caa1 c0f18ac** | Có |
| Tám neo trên master | Tất cả là tổ tiên | `merge-base --is-ancestor` cho **78ac0ddf, 4488ff1d, c0f18ac1, ca960160, b912e5f, 4ef73e6, 670071b, b7a53ba**: **8 lần rc=0** | Có |
| Cổng biên nhận master | rc=0; 16 đạt, 0 vi phạm, 0 chưa đo, tổng 69 | Bản sao ghim đúng **cacaba3**: đúng toàn bộ dòng tổng kết, `TỔNG: ĐẠT` | Có; không gọi toàn bộ gate master là xanh |
| c45, cùng cây | Merge giữ neo, squash mất neo | Fixture gốc: ancestry **0 rồi 1**, hai tree OID bằng nhau | Có trong fixture; lỗi 128 bị nhận nhầm, F03 |
| Caveat “khi và chỉ khi merge commit” | Điều kiện cần và đủ | Fixture đổi sang **fast-forward** vẫn giữ neo và qua c45 | **Không; F06** |
| Review bắt đầu/merge cách 40 giây | 19:36:33Z → 19:37:13Z | Phép trừ là 40 giây; Git commit timestamp là **19:37:11Z**. Không có readback sự kiện GitHub để xác minh hai thời điểm công bố | KHÔNG ĐO ĐƯỢC sự kiện; không đồng nhất commit time với merge-event time |
| Clone nông ban đầu | 2/298 ref, 296 thiếu; CLI rc=2/8 chưa đo, suite 43/45 | Mirror được giao đã đầy đủ. Không có snapshot/cấu hình hai ref của lần đo gốc; không gọi fetch/ls-remote | KHÔNG ĐO ĐƯỢC các số lịch sử môi trường này |
| FULL GATE sau bổ sung | Chưa chạy | Không chạy golden/doc-claims/determinism/release-verify trong lượt này; không suy thiếu log thành xanh | Chưa đo, đúng giới hạn |
| Write set tự nhận | Không đổi verdict/launcher_test; chỉ trường trạng thái receipt | Diff: **0 verdict đổi**, **launcher_test không đổi**, YAML receipt chỉ **trang_thai_va** đổi | Có |

### Đo răng từng mutant và làm yếu chính bản vá

Lệnh tái lập: `PYTHONDONTWRITEBYTECODE=1 python3 rv9-audit/teeth.py`. Script lấy nguyên lambda mutant từ AST, chạy trên bản sao, ghi đầy đủ thông báo giết và đối chứng trong khi mutant còn hiệu lực.

| mutant | trạng thái thực | assertion thực sự giết | đối chứng c18 |
|---|---|---|---|
| m56 | `giet_that` | `mất RIÊNG neo ASSURANCE_CUA_NGUOI: đòi rc=2, được 0` | Sạch |
| m57 | `giet_that` | `mất RIÊNG neo ASSURANCE_CUA_MO_HINH: đòi rc=2, được 0` | Sạch |
| m58 | `giet_that` | Bảng neo sản phẩm mất đúng mục người, lệch oracle ba mục | Sạch |
| m59 | `giet_that` | Năm dòng **nhận sai giá trị transport**, tổng `5/40`; không phải năm lỗi thông báo | Sạch |
| m60 | `giet_that` | Hàng launcher lệch đáng lẽ từ chối `machine/local`, thực tế `_thieu` trả `[]` | Sạch |

**Năm mutant nguyên gốc không nhận tín dụng giả trong phép chạy này.** `TinHieuChotCa` chỉ xác minh nguồn **ca**, không xác minh nguồn **thuộc tính**. Đã đo giới hạn ấy: gỡ hai lượt neo để m56 sống, rồi chỉ làm hỏng đối chứng đủ nguồn bên trong c28; kết quả lại là **`giet_that`**, lỗi “đủ nguồn: đòi rc=0, được 1”, c18 vẫn sạch. Ngoại lệ `AssertionError` trần và `RuntimeError` bị phân đúng `tin_dung_gia`. Không dùng thí nghiệm cố ý phá giàn đo này để phủ nhận năm kill đúng ở bảng trên; nó chứng minh vì sao vẫn phải đọc thông báo như CHANGELOG yêu cầu.

| làm yếu trên bản sao | phép đo đích |
|---|---|
| Gỡ hai lượt neo riêng của c28 | m56 **qua**, m57 **qua**, c18 sạch |
| Cho c43 lấy oracle từ bảng sản phẩm | m58 **qua**, c18 sạch |
| Bỏ entry transport khỏi c34 | m59 **qua**, c18 sạch |
| Bỏ witness của c44 | m60 **qua**, c18 sạch |
| Cho oracle + hàng Claude dùng `machine`, giữ nguồn §2 `machine/local` | c44 so ô chính xác **đỏ**; đổi sang substring **qua**. Dùng hàng Claude để giữ witness Antigravity không đổi |
| Cô lập tầng (b) đúng hàng Antigravity: đổi oracle và dữ liệu trả về cho tầng (a), giữ sản phẩm/witness gốc | So ô **đỏ**; substring **qua**; log `c44-ag-exact.json`, `c44-ag-substring.json` |
| Lặp lại nguyên câu neo có sẵn trong bản sao nguồn | c43 **đỏ vì 2 chỗ**; làm yếu đòi một chỗ thành có ít nhất một chỗ thì **qua** |
| Bơm kết quả ancestry cuối c45 bằng 0 / 1 / 128 | Lần lượt **đỏ / qua / qua**; 128 là lỗ F03 |
| Bỏ riêng chặn transport `None` trong sản phẩm | Witness **1 lỗi → 0 lỗi**, nhưng toàn suite **48/48 · 62/62 · 2/2 · 44/62**, rc=0; F02 |
| Sửa riêng surface trong bảng kế hoạch | c44 vẫn **qua**; F05 |
| Làm receipt của c44 thiếu receipt_id | `_thieu` báo lỗi, c44 vẫn **qua**; F04 |

### F01-bang-canh-bao-bi-cat  [P2]  Blockquote mới cắt bảng README và làm lease gate đỏ thêm một ca

TỆP/DÒNG: `cay-kho/ops/reviews/README.md:30`; consumer `cay-kho/ops/lease_publish_test.py:843`, `:972`; lời khai delta ở `EVIDENCE.md`.

VẤN ĐỀ: Blockquote R8-06 được chèn giữa các hàng của bảng cảnh báo. Parser kết thúc bảng tại đây; phần hàng tiếp theo không có header/separator mới. Nó chỉ đọc được **13/246 hàng**, làm **233 hàng cảnh báo** biến mất khỏi kết quả kiểm. Đây là thay đổi của PR, không phải thiếu actionlint. Lời khai “120/121, cùng chữ ký, delta=0” sai trên exact head.

ĐÃ THỬ NGHIỆM: `python3 rv9-audit/run_baselines.py` cho head **119/121, rc=1**, đỏ t27 và t33; bản sao master cho **120/121, rc=1**, chỉ t33. `PYTHONDONTWRITEBYTECODE=1 python3 rv9-audit/regressions.py`: t27 head **FAIL/13 hàng**; thay riêng README bằng base **PASS/246**; giữ nội dung mới nhưng chuyển blockquote sau bảng **PASS/246**. Log `t27-*.json`, `lease.*`, `master-lease.*`.

GỢI Ý VÁ: Đặt caveat mới ở ngoài bảng, giữ bảng liên tục; chạy lại t27 và toàn lease suite, sửa số liệu EVIDENCE theo exact head mới. Không bỏ assertion t27 để hợp thức hóa Markdown hỏng.

ĐỘ TIN: cao.

### F02-null-khong-co-ca-canh  [P2]  Bỏ chặn transport null vẫn qua toàn suite và toàn bộ mutant

TỆP/DÒNG: `cay-kho/ops/bien_nhan_v2_test.py:1376`; nhánh sản phẩm mới `cay-kho/ops/bien_nhan_v2.py:403`; CHANGELOG `:559`.

VẤN ĐỀ: Bản vá khai `None` là phản chứng đã tìm thêm, nhưng `KIEU_KHONG_PHAI_CHUOI` chỉ có dict, list, số, True và chuỗi rỗng. Vì thế **5/40 đúng nhưng không khóa null**. Đột biến coi riêng null là vắng mặt bỏ được một hành vi công bố mà mọi ca và mutant vẫn xanh.

ĐÃ THỬ NGHIỆM: `PYTHONDONTWRITEBYTECODE=1 python3 rv9-audit/regressions.py`. Trên bản sao, trước nhánh mới chỉ loại trường transport khỏi ánh xạ khi giá trị là None; các giá trị khác giữ nguyên. Dùng `v2_du()` có sẵn, đổi đúng transport: sản phẩm gốc **1 lỗi**, bản yếu **0 lỗi**. Chạy `python3 ops/bien_nhan_v2_test.py` từ bản yếu: **rc=0**, `48/48 ca đạt · 62/62 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 44/62 đột biến thường khai đối chứng`, `TỔNG: ĐẠT`. Log `null-witness-*`, `null-mutant-full-suite.*`.

GỢI Ý VÁ: Đưa `None` vào ma trận giá trị và có đối chứng trường vắng; thêm phép làm yếu chỉ bỏ chặn null. Phân biệt kiểm hành vi với việc chỉ đổi thông báo. Không cần đổi nhánh sản phẩm đang đúng.

ĐỘ TIN: cao. Đây là lỗ hồi quy, **không phải sản phẩm gốc đang nhận null**.

### F03-c45-nhan-loi-git-thanh-ket-qua  [P2]  c45 vẫn xanh khi Git không đo được quan hệ tổ tiên

TỆP/DÒNG: `cay-kho/ops/bien_nhan_v2_test.py:2134`, `:2137`.

VẤN ĐỀ: Assertion cuối dùng `returncode != 0`; vì vậy lỗi Git 128 được tính như kết quả hợp lệ “không phải tổ tiên” (rc=1). Hai lượt đọc tree chỉ so stdout, không kiểm rc hay OID hợp lệ. Ca có nói chỉ khóa tiền đề, nhưng vẫn có đường **không đo được tiền đề mà báo qua**.

ĐÃ THỬ NGHIỆM: `PYTHONDONTWRITEBYTECODE=1 python3 rv9-audit/teeth.py`: fixture gốc có ancestry **0/1**, qua; chỉ bơm lỗi **128** ở lời gọi ancestry thứ hai, giữ mọi lời gọi khác chạy thật ⇒ **qua**. Bơm **0** ⇒ đỏ đúng assertion cuối. Log `c45-final-git-128.json` ghi từng lời gọi và rc, không có ngoại lệ vô can được tính làm kill.

GỢI Ý VÁ: Lấy kết quả Git một lần, phân biệt rc=0, rc=1 và lỗi khác; lỗi công cụ phải thành `LoiDungCa`. Kiểm rc và hình dạng OID của hai lượt đọc tree trước khi so. Thêm tự kiểm lỗi Git riêng cho nhánh squash.

ĐỘ TIN: cao.

### F04-c44-chap-nhan-bang-viec-thieu-tu-khoa  [P2]  Witness c44 không chứng minh receipt được nhận

TỆP/DÒNG: `cay-kho/ops/bien_nhan_v2_test.py:2095`; CHANGELOG `:575`.

VẤN ĐỀ: `duoc_nhan = not any("transport" in x for x in loi)` coi receipt có lỗi khác là **được nhận**. Vế dương của witness được mô tả là biên nhận trung thực được nhận, nhưng assertion chỉ chứng minh không có thông báo chứa một từ khóa. Đây chính là khoảng cách giữa hành vi và diagnostic mà PR đang cố khóa.

ĐÃ THỬ NGHIỆM: `PYTHONDONTWRITEBYTECODE=1 python3 rv9-audit/finish_measurements.py`: làm yếu fixture riêng bằng receipt_id rỗng, giữ nguyên provider/surface/transport có sẵn. `_thieu` trả **`thiếu/rỗng receipt_id`**, nhưng **c44 vẫn `qua`**. Log `c44-false-positive-witness.json`. Với fixture nguyên gốc, m60 vẫn chết đúng thuộc tính; không khai kill m60 hiện tại là giả.

GỢI Ý VÁ: Vế dương phải đòi danh sách lỗi rỗng. Vế âm phải đòi lỗi transport mong đợi, đồng thời xác minh các trường độc lập còn hợp lệ. Nếu chỉ muốn đo riêng điều kiện transport, thu hẹp tên ca và lời khai “được nhận”.

ĐỘ TIN: cao về giới hạn witness; chưa chứng minh receipt hợp lệ bị sản phẩm head từ chối.

### F05-duy-nhat-lech-chi-dung-cho-transport  [P3]  Đối chiếu năm hàng chưa đủ cho lời khai khớp toàn bộ §2

TỆP/DÒNG: `cay-kho/.claude/dev/launcher.py:171`; `cay-kho/CHANGELOG.md:570`; `cay-kho/ops/bien_nhan_v2_test.py:2069`; nguồn `cay-kho/ops/KE_HOACH_THI_CONG_DA_PROVIDER.md:33`.

VẤN ĐỀ: Đã kiểm cả năm hàng, không chỉ Antigravity. Transport bốn hàng còn lại khớp. Nhưng hàng Codex của §2 cho **codex_cli hoặc Codex service**, còn bảng/ oracle chỉ biểu diễn codex_cli. Tầng (b) bỏ qua biến `_be_mat`, chỉ so ô transport. Vì vậy “Antigravity là hàng duy nhất lệch §2” rộng hơn phép đối chiếu thực sự; chưa có phép kiểm đầy đủ các surface của nguồn kế hoạch.

ĐÃ THỬ NGHIỆM: `history.py` ghi cả năm hàng ở base/head trong `provider-five-rows.json`. `finish_measurements.py` đổi riêng ô surface Antigravity trong **bản sao kế hoạch** thành một surface đã có sẵn trong cây ⇒ **c44 vẫn qua** (`c44-source-surface-drift.json`). Phép substring layer (b) cũng đã tái hiện độc lập: so chính xác đỏ, so substring qua. Không coi cụm prose “Codex service” là một tên máy hợp lệ đã được đặc tả, không tự bịa receipt service để báo chặn nhầm.

GỢI Ý VÁ: Thu hẹp lời khai thành “duy nhất lệch cột transport trong năm hàng đã đối chiếu”. Nếu muốn khóa bộ ba, đối chiếu cả tập execution surface và xác định cách biểu diễn Codex service trong hợp đồng dữ liệu.

ĐỘ TIN: cao về phạm vi kiểm; vừa về phần chính sách surface còn cần quy định.

### F06-caveat-merge-la-dieu-kien-can-sai  [P3]  Canonical ancestry không đòi bắt buộc phải có merge commit

TỆP/DÒNG: `cay-kho/ops/reviews/README.md:32`; `cay-kho/ops/bien_nhan_v2_test.py:2107`; CHANGELOG `:585`.

VẤN ĐỀ: Caveat áp “**khi và chỉ khi kho land bằng MERGE COMMIT**” cho mọi canonical ancestry. Fast-forward cũng giữ nguyên neo. Squash chỉ làm mất tư cách tổ tiên của neo chưa nằm trong lịch sử nhánh đích và bị thay bởi commit mới; neo đã là tổ tiên trước squash vẫn còn. c45 chỉ dựng một neo mới trên nhánh riêng, không chứng minh mệnh đề tổng quát hay chính sách land. Câu “không khóa chính sách” là đúng, nhưng chưa tự làm phần “tiền đề” hẹp đủ.

ĐÃ THỬ NGHIỆM: `PYTHONDONTWRITEBYTECODE=1 python3 rv9-audit/teeth.py`: đổi đúng lựa chọn merge trong fixture c45 từ tạo merge commit sang **fast-forward**; Git chạy thật, neo phía land vẫn rc=0, hai tree bằng nhau, phía squash rc=1, **c45 qua**. Log `c45-fast-forward.json`. Phép đo master thật vẫn sạch và tám neo vẫn là tổ tiên.

GỢI Ý VÁ: Viết điều kiện theo quan hệ tổ tiên và vị trí neo trước land; ghi c45 chỉ chứng minh trường hợp neo mới của fixture. Không cần đổi kiến trúc neo hay chính sách merge trong PR này.

ĐỘ TIN: cao.

### F07-so-dem-moi-va-dieu-kien-do-con-sot  [P3]  Phần bổ sung đếm sai số trường cũ và còn số thiếu tập đo

TỆP/DÒNG: `cay-kho/CHANGELOG.md:565`, `:457`, `:490`, `:548`; `cay-kho/ops/bien_nhan_v2_test.py:1375`.

VẤN ĐỀ: “6 trường còn lại” sai: trước thêm transport, ma trận có **7** trường và cả bảy chặn chuỗi rỗng. `5/40` đúng theo **8 trường × 5 giá trị**, không phải theo toàn bộ sáu phản chứng kiểu được liệt kê ở đoạn trước. Số substring “3/4” chỉ đúng khi quét **toàn bộ receipt**, trong khi bảng ngay trên nói tập tự khai v2. Số “34 hàng c28” là số base trước khi tách hàng; trên head mới còn 33 hàng tuple và các lượt riêng. Không sửa số lịch sử thành số head, nhưng phải giữ mốc/tập/đơn vị cạnh số để đáp ứng chính lời khai “mỗi con số … mang điều kiện đo”.

ĐÃ THỬ NGHIỆM: `PYTHONDONTWRITEBYTECODE=1 python3 rv9-audit/numeric_extras.py`: ma trận base **7**, kiểm chuỗi rỗng **7/7 bị chặn**; head **8×5=40**. Đếm substring YAML trên toàn bộ 68/69 receipt: **3/4**; chỉ tập tự khai v2: **2/3**. AST base/head c28: **34/33 hàng tuple**. Các tỉ lệ cũ bị R8-03 bắt — **1/16→2/17, 1/15→2/16, 11/68→12/69→13/70** — đã tái đo và **khớp**, không nằm trong phần sai của finding này.

GỢI Ý VÁ: Sửa 6 thành 7 ở cả hai vị trí; chú thích rõ mẫu 8×5 của m59, tập toàn bộ receipt của phép substring và SHA của số 34 lịch sử. Gắn “head lượt 8” với OID cụ thể khi dùng số 13/70 để không nhầm với c0f18ac của verdict lượt 8.

ĐỘ TIN: cao về số đếm; vừa về khả năng người đọc hiểu thiếu phạm vi trong đoạn lịch sử.

### F08-launcher-khong-tai-lap-duoc-181-ca  [P3]  EVIDENCE launcher chưa tái lập đủ dưới ràng buộc offline

TỆP/DÒNG: `EVIDENCE.md` hàng `.claude/dev/launcher_test.py`; fixture `cay-kho/.claude/dev/launcher_test.py:6321`.

VẤN ĐỀ: Không đo lại được `181/181, bỏ qua 1`. Với cấm mạng, tám ca cần dựng venv và cài phiên bản pypdf cho fixture không dựng được; cộng một ca Windows thành **9 ca bỏ qua**. Lượt đầu còn t81 hỏng, nhưng lỗi này không tái hiện ở lượt A/B tiếp theo hay khi chạy riêng. Đây là sai khác bằng chứng phải khai, **không phải hồi quy launcher đã chứng minh**.

ĐÃ THỬ NGHIỆM: `run_baselines.py`: **rc=1, 172/173, tổng 182, bỏ qua 9, hỏng 1**. `finish_measurements.py` chạy head/base cùng môi trường: **rc=0 ở cả hai, 173/173, tổng 182, bỏ qua 9, hỏng 0**. `regressions.py` chạy riêng t81 trên cả hai: **PASS/PASS**. Không tải dependency từ mạng và không thay fixture để lấy số xanh. Log `launcher.*`, `launcher-repeat-head.*`, `launcher-base.*`, `t81-*.json`.

GỢI Ý VÁ: Ghi riêng số tái hiện offline và điều kiện cần cho tám ca venv; cung cấp artifact dependency cục bộ nếu cần reviewer kiểm đủ 181 ca. Giữ dấu vết t81 không ổn định; không quy nguyên nhân cho hàng transport chỉ từ một lần lỗi.

ĐỘ TIN: cao về số thực chạy; thấp về nguyên nhân t81 ban đầu.

## TÔI ĐÃ ĐO ĐƯỢC GÌ / KHÔNG ĐO ĐƯỢC GÌ

Đã chạy các suite công bố, gate biên nhận trên head/base/master/commit vá thứ nhất; truy vấn lịch sử Git; so byte receipt ba tập; chạy lại sáu fixture nguồn có sẵn; kiểm năm mutant mới đến thông báo assertion và đối chứng; làm yếu tất cả các chốt mới được giao, rồi tìm thêm mutant null sống qua toàn suite. Bộ ba Antigravity sửa đúng hai chiều. Với **14 tổ hợp hợp đồng/surface/transport-vắng-hoặc-đúng** lấy từ dữ liệu hiện tại, không thấy trường hợp hợp lệ nào trước qua mà sau bị từ chối; tổ hợp Antigravity machine/local chuyển từ bị chặn sang qua như mong đợi. Gate 70 receipt thật sạch. Nhánh hành vi mới nằm trong **`_mri`**; `_thieu` gọi nó qua bảng yêu cầu, không có nhánh hành vi mới trực tiếp trong thân `_thieu`.

Các lỗ chạy được ở đây thuộc **test/hồ sơ và bảng cảnh báo bị phá**. Chưa chứng minh đường chấp nhận sai mới trong sản phẩm gốc của PR. Thí nghiệm null là đột biến trên bản sao để đo độ phủ, không phải bằng chứng head gốc đang nhận null.

Không đo được GitHub trực tiếp, ref phía máy chủ, review-event/merge-event timestamps, quyền CLI phiên executor gốc, nền clone nông lịch sử, Windows thật, tám fixture launcher thiếu dependency và FULL GATE sau bổ sung. Không gọi mạng/commit/push hay sửa mirror. Các commit/merge trong test chỉ là fixture Git do **bộ test có sẵn** dựng trong thư mục tạm được chuyển vào `rv9-audit/tmp`; không có commit review hay commit trên kho được giao.

Không tự soạn payload đường dẫn thoát cây, chuỗi thoát hay đồng tự Unicode. Fixture loại đó được thực thi nguyên từ các suite. Hướng chưa thử giao lại bằng lời cho điều phối: cung cấp nguồn PROTOCOL vẫn giữ câu neo như trích dẫn/ví dụ nhưng không còn là điều khoản hiệu lực; parser hiện tìm substring, các phép thử hiện tại chưa chứng minh nó hiểu hiệu lực pháp quy. Không tự tạo nội dung phản chứng ấy, không nâng giả thuyết thành P1.

Ba lỗi của **script reviewer** đã gặp và loại khỏi bằng chứng: lần trích AST mutant đầu thiếu biến `_VONG_NEO`; lần ghép nguồn historical làm parity giàn đo hỏng; lần đọc hằng frozenset bằng literal_eval sai hình dạng. Đã sửa giàn đo, chạy lại với đúng biến/hình dạng và giữ **nguồn head cố định, chỉ thay byte receipt** cho phép m49. Không tính traceback hoặc parity hỏng ấy là tín dụng kill hay finding sản phẩm. Các log kết quả cuối được dẫn ở trên là các lượt đã sửa.

Worktree `cay-kho/` sạch khi bắt đầu và sau các phép chạy; exact HEAD giữ nguyên. Script và log tái lập giữ trong `rv9-audit/`; không dùng các kết quả có sẵn ở `review-artifacts/` làm bằng chứng thay cho lượt chạy này.
