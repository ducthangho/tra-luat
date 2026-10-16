# Cross-review r2 — packet #687 LEASE-PUBLISH-WINDOWS-DO

Ghi tăng dần. Reviewer: Codex/OpenAI, shell cục bộ qua API; không mạng, không CI/Windows thật, không sửa `cay-kho/`. Authority: chỉ thị review của người dùng. Không tự xác thực model/effort bằng telemetry.

- `reviewed_sha`: `807c6c2898b2338cbc8f97cbcd8540519fbe4f8a`; tree `9ca413b041a8aa6e8453691931e38b5fa2b8d1a6`.
- Baseline: `89fc4fac8cea65979cc2483043dc8cd07a6e8518`.
- Lệnh `git -C cay-kho rev-parse HEAD 'HEAD^{tree}'`, `git -C cay-kho status --porcelain`: đúng hai OID trên, status rỗng.
- `git -C cay-kho show HEAD:ops/specs/lease-publish-windows-do-r1.md | sha256sum`: `87375af33e23157a89a9fee88696d5ad2466b388182aff4d896386ee6b16e230`, khớp hợp đồng r1/g1.
- Đã đọc spec, lease, verdict r1, REPORT-r2 và doctrine `CLAUDE.md` “Bài học đắt giá”. Thử/đột biến chỉ trong `r2-measure.fmUQ650G/`, tạo bằng `mktemp -d -p . r2-measure.XXXXXXXX`.

Đang đo: suite hai vế cùng rig, ca riêng lẻ, đột biến độc lập và đối chiếu log.

## L1 — Hợp đồng skip còn thiếu khóa ở đường workflow thật và tính kín của bộ giải · P2

**Trạng thái r1: ĐÓNG MỘT PHẦN.** A1 đã chặn ca ngoài sổ/cặp sai; A2 đã chặn include Windows, prefix giả, exclude trong nhánh matrix; A3 đã khai đúng phần chưa đo tại REPORT-r2:9–12. Chưa đủ khóa hồi quy cho đường dùng sổ thật, và bộ giải chưa fail-closed toàn bộ dạng mà hợp đồng yêu cầu.

**Biểu hiện (`ops/lease_publish_test.py`):**

- :587–590 trả sớm cho runs-on literal/list, trước kiểm strategy/matrix/exclude ở :597–605. Probe `runs-on: ubuntu-latest` (hoặc `[ubuntu-latest]`) + matrix có `exclude` vẫn được miễn; matrix có trục phụ dạng dict không hỗ trợ cũng được miễn. Spec A2 yêu cầu exclude/dạng chưa hỗ trợ ⇒ không chứng minh ⇒ không miễn. Không khẳng định các ví dụ này tạo Windows runner; đây là vi phạm luật fail-closed đã đóng băng.
- :10609–10612 chỉ dùng sổ tiêm cho các vế âm về runs-on; :10571 và :10614–10618 chỉ đọc workflow thật dưới dạng Ubuntu dương. Đột biến R15 ở :10705 cho nhánh **sổ thật + nt** lý do Ubuntu cố định, giữ bộ giải cho sổ tiêm: `t193` QUA, nhưng đổi chính YAML thật trong bản sao sang Windows rồi cho ca đã đăng ký ném đúng cặp ⇒ skip trái phép. Tức chưa khóa việc main phải đọc lại cấu hình thật khi cấu hình đổi.
- :10703 so Path.resolve hiện đúng với symlink/`..` trên POSIX. R20 bỏ resolve, dùng absolute: `t193` vẫn QUA trong khi alias symlink hợp lệ bị ĐỎ; thiếu đối chứng định danh đường dẫn. Case folding trên filesystem Windows thật: **KHÔNG ĐO ĐƯỢC** (sandbox POSIX); `PureWindowsPath` chỉ chứng minh mô hình so sánh của Python, không phải lượt chạy Windows.

**Phép đo tái lập:**

```sh
python r2-measure.fmUQ650G/run-mutations.py
PYTHONDONTWRITEBYTECODE=1 python r2-measure.fmUQ650G/probes.py
```

Output đã lưu `mutations.log`, `mutant-15.log`, `mutant-20.log`, `probes.log` trong thư mục đo:

```text
15 R15 main tin sổ thật thay YAML thật | t193_ | rc=0 | lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
REAL_WINDOWS intact 1 lease_publish: 0/1 đạt; đã chạy=1, bỏ qua=0
REAL_WINDOWS mutant 0 lease_publish: 0/0 đạt; đã chạy=0, bỏ qua=1
UNSUPPORTED fixed_exclude "... chỉ chạy Ubuntu ... ['ubuntu-latest']"
UNSUPPORTED list_exclude "... chỉ chạy Ubuntu ... ['ubuntu-latest']"
UNSUPPORTED bad_other_axis "... chỉ chạy Ubuntu ... ['ubuntu-latest']"
20 R20 so đường dẫn không resolve | t193_ | rc=0 | lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
PATH intact symlink 0 lease_publish: 0/0 đạt; đã chạy=0, bỏ qua=1
PATH intact dotdot 0 lease_publish: 0/0 đạt; đã chạy=0, bỏ qua=1
PATH mutant symlink 1 lease_publish: 0/1 đạt; đã chạy=1, bỏ qua=0
```

Probe `REAL_WINDOWS` là seam `nen='nt'`, không chạy Windows thật. Mã nguyên vẹn đã chặn đúng; finding về R15 là **ca khóa mất răng**, không cáo buộc bản hiện tại đang bỏ qua workflow Windows.

**Hint patch:** kiểm cấu trúc strategy/matrix và exclude trước các nhánh trả sớm, từ chối cấu trúc chưa hỗ trợ theo A2. Thêm vế âm đi qua main với **sổ mặc định** và YAML ở đường workflow đã đăng ký thực sự đổi sang Windows, rồi khôi phục bytes trong `finally` (trên cây fixture biệt lập); không chỉ truyền sổ tùy ý. Thêm đối chứng symlink/`..` trỏ cùng tệp được miễn, đường cùng basename nhưng khác tệp bị chặn; chạy đối chứng case folding trên Windows thật khi có phép. R15 và R20 phải làm t193 ĐỎ đúng assertion tương ứng; ba dạng unsupported nêu trên phải không được miễn.

## L2 — Transcript được đếm từng phần, ca khóa chưa bảo vệ đầy đủ biên xác minh · P2

**Trạng thái r1: ĐÓNG MỘT PHẦN.** Các ca 0/0, 1/1 thiếu tên, thiếu ra, trùng tên đầu vào và tổng kết lệch được chặn trong các fixture đã có. Nhưng B1 vẫn có đường xanh giả trên mã nguyên vẹn; B2 đang mock verifier nên chưa là đối chứng đầy đủ dưới luật mới.

**Biểu hiện cùng cơ chế:**

- :4593–4613 lấy marker chung và kết quả `<<< ra` bằng hai regex riêng. Không đòi mỗi marker ra có một kết quả hợp lệ. Khi 189 cặp vào/ra còn nguyên tên, nhưng mọi ra thành `bad-status`, `kq=[]`, `do_=[]`; tổng kết `0/189 đạt; đã chạy=189, bỏ qua=0`, rc=0 được verifier nhận và t125 :4694–4707 đưa sang so A/B rồi QUA. Một ra bị chia bởi dòng stderr giả ở giữa cũng lọt nếu tổng kết giảm QUA cho khớp lượng regex đọc được. Đây là phản chứng **mã nguyên vẹn**, không cần sửa verifier.
- :4593–4600 so đúng danh sách truyền vào nhưng không kiểm danh sách CA có tên duy nhất. CA chứa một tên hai lần ⇒ expected cũng trùng ⇒ transcript 190 marker với 189 tên duy nhất vẫn được nhận và t125 QUA. CA hiện tại thật có 189 tên duy nhất; không khẳng định đã có trùng trong bản vá.
- :4604–4608 có chốt dòng BỎ QUA đúng, nhưng t194 :10645–10659 chỉ khóa dòng ĐỎ. R16 bỏ riêng đối chiếu BỎ QUA vẫn `t194 1/1`; transcript khai BỎ QUA mà ra ghi QUA/tổng kết tất cả QUA đi qua cả verifier và t125.
- :4615 kiểm rc nhưng không có vế âm rc trong t194. R17 bỏ kiểm rc và R18 bỏ truyền rc ở t125 đều sống với t194; R18 cũng sống với t160 (R19). Hai con cùng rc=7 nhưng toàn marker QUA ⇒ t125 QUA dưới cả hai đột biến. Bản nguyên vẹn chặn đúng.
- :6860–6876 thay verifier bằng mock luôn trả [] trước classifier; fixture t160 không có marker. Nó bắt được bỏ hoàn toàn lời gọi verifier, nhưng không bắt bỏ tham số rc (R19). Vì thế chữ “fixture hợp lệ dưới luật mới” (B2) chưa được chứng minh bởi fixture này.

**Lệnh:** hai lệnh `run-mutations.py` và `probes.py` ở L1. Log nguyên văn có đầy đủ trường lỗi; output rút gọn:

```text
TRANSCRIPT valid verifier= [] t125= PASS
TRANSCRIPT CRLF verifier= [] t125= PASS
TRANSCRIPT noise_between_markers verifier= [] t125= PASS
TRANSCRIPT unknown_status verifier= [] t125= PASS
TRANSCRIPT ra_split_by_stderr verifier= [] t125= PASS
TRANSCRIPT all_ra_invalid verifier= [] t125= PASS
SEPARATE_STDERR PASS
CA_DUPLICATE 190 189 verifier= [] t125= PASS
WRONG_SKIP intact ['dòng ĐỎ/BỎ QUA lệch kết quả `<<< ra` (ĐỎ=[], BỎ QUA=[])']
WRONG_SKIP mutant [] t125= PASS
RC7 intact RED ... ['mã thoát 7 lệch số ca ĐỎ (0)']
RC7 drop_rc_guard PASS
RC7 drop_rc_argument PASS
```

Dòng stderr riêng giữa hai marker và CRLF hợp lệ **được nhận đúng**, không là finding. Lỗ là marker kết quả bị hỏng mà vẫn được tính là đủ bằng chứng. Probe dùng hai con giả ở seam tiến trình, giữ verifier/classifier/chốt thật; lượt t125 với hai con thật được ghi riêng ở phần nghiệm thu.

**Hint patch:** parse tuần tự các marker thành bản ghi ca, mỗi `ra` phải có chính xác một trạng thái thuộc `{QUA, DO, BO_QUA}`, đủ duration hợp lệ; kiểm CA duy nhất trước so chuỗi. Bắt buộc `len(kq)==len(ten_ca)` và `QUA+DO+BO_QUA==len(ten_ca)`; tổng kết chạy=QUA+DO, rc nhất quán. Không được chỉ dựa vào số lượng kết quả regex tìm được để hợp thức hóa số QUA thiếu. Giữ khả năng bỏ qua dòng diagnostic giữa các marker và nhận CRLF.

Mở t194: marker trạng thái lạ/khuyết, đủ tên nhưng tất cả status hỏng, CA trùng, dòng BỎ QUA lệch ra, rc sai ở cả helper và wiring t125 phải ĐỎ. Sửa t160 dựng transcript đủ CA với `_dung_transcript_ab`, dùng tên đỏ/skip thật và verifier thật (spy `wraps` nếu cần); xác nhận mỗi transcript hợp lệ trước kiểm lệch parity. R16, R17, R18/R19 phải làm ca đích ĐỎ; vẫn giữ đối chứng đủ ca + skip hợp lệ QUA.

## L3 — Ranh giới lời khai và bằng chứng trong REPORT-r2 · P4

**Trạng thái r1: ĐÃ ĐÓNG đối với các kết luận vượt bằng chứng đã nêu ở r1.** Báo cáo không còn nói không cần vá/đóng phiếu, không suy nguyên nhân hiệu năng theo OS, khai A3 chưa đo, không nhận đã đối chiếu blob f2582ba, và phân biệt Windows trước/sau packet. Không dùng việc đóng lớp báo cáo để đóng L1/L2.

**Phép đo:** `python r2-measure.fmUQ650G/audit-evidence.py` → `audit-evidence.log`:

- `full-base.log`: ngoài/A/B đều 187 vào, 187 ra, 187 tên duy nhất, 187 QUA, skip 0, đúng thứ tự.
- `full-nhanh.log` và `verify-r1.log`: ngoài/A/B đều 189 vào, 189 ra, 189 tên duy nhất, 189 QUA, skip 0. Như vậy lời 189/189 đúng về nội dung log được cấp; log tự nó không xác thực danh tính phiên điều phối.
- Ba log gate-ops cũ/mới: mỗi luồng có đủ 187 cặp; Windows QUA=180, BO_QUA=7 đúng t51/t59/t60/t62/t63/t66/t68; Ubuntu QUA=187, BO_QUA=0. Mỗi **log gate-ops** có 27 SyntaxWarning = 18 `<unknown>` + 6 `lease_publish_test.py` + 3 `bash_nen.py`. Không áp số 27 cho mọi log trong thư mục evidence (gate Windows=49, gate-registry=1).
- Windows mới t191/t192 ngoài `219.719/0.781s`, A `265.546/0.829s`, B `258.734/1.047s`; Ubuntu ngoài `91.076/0.076s`, khớp REPORT-r2:13–14.
- Khoảng log gate-ops Windows `1997.579443s`; gate Windows `6229.647412s` (~104 phút); gate-registry `5412.241431s` (~90 phút).
- `rg -n '49/51|Process completed|t23_batch' evidence/gate-windows-36532243761.log`: :1021 t23 có warning từ `bash_nen.py:900` trong tên công cụ; :1028 `cong_cu_test: 49/51 đạt`; :1284 `Process completed with exit code 1`.
- `sed -n '2160,2185p' evidence/gate-registry-windows-36532243761.log`: dòng cuối trước khoảng im lặng `07:04:49.2485913Z`; `08:10:11.9799443Z The operation was canceled`. Workflow hiện tại `ci.yml:660` ghi `timeout-minutes: 90`. Đây là phù hợp mốc timeout, không tự xác thực trường nguyên nhân hủy của GitHub.
- `git -C cay-kho cat-file -t f2582ba9856a7cad41e6bf284914007e5e34d71d`: rc128, object thiếu, đúng khai báo giới hạn. `rg -n '32567293842|65/65' cay-kho/ops/reviews/lease-dang-windows-review-3-claude-verdict.md`: :25–26 có hồ sơ run cũ và 65/65 + 8 skip.
- 14/14 đột biến và ruff delta 0 được reviewer chạy lại, bảng bên dưới. Số lượng 14/14 là đúng cho danh sách đã chạy, không chứng minh phủ toàn hợp đồng; REPORT-r2 đã ghi “executor khai”, không nói phủ hết.

**Hint báo cáo (làm rõ provenance, không chặn):** ở :15 thay “Mỗi log” bằng “Mỗi log gate-ops được đối chiếu”. Ở :20–22 có thể viết chính xác hơn: “Log gate Windows ghi bước G5 exit 1 sau khoảng 104 phút; gate-registry ghi hủy ở khoảng 90 phút, phù hợp trần cấu hình 90 phút. Chưa đối chiếu JSON conclusion/cancellation reason từ GitHub.” Ở :29 “log verify-r1 do phiên điều phối cung cấp cũng ghi 189/189”. Sau lượt review này, bổ sung: “Cross-review r2 tái hiện 14/14 đột biến đã khai nhưng tìm thêm lỗ ở verifier và độ phủ ca khóa; chưa đạt nghiệm thu packet.” Không cần ca khóa mã cho lớp thuần báo cáo.

## L4 — Seam của main thiếu khóa bảo toàn trạng thái qua lượt gọi · P2

**Trạng thái: MỚI.** Đây là khoảng trống của ca meta mới/đổi, không phải khẳng định main nguyên vẹn đang rò trạng thái.

**Biểu hiện:** `ops/lease_publish_test.py:10670–10681` cung cấp seam `chon/nen/so`, còn t193 chỉ kiểm kết quả từng lần gọi, không so trạng thái trước/sau. R22 thêm `CA[:] = cac_ca` sau `cac_ca = list(chon)`: t193 vẫn QUA nhưng CA từ 189 còn 1; một lần meta chọn lambda rồi gọi `main()` với mặc định chạy thật chỉ đo lambda và in 1/1, rc0. Biến toàn cục xác định “đủ suite” bị đổi theo seam, nên cổng có thể tự thu nhỏ tập kỳ vọng.

**Phép đo:** `run-mutations.py` dòng R22 và `probes.py`:

```text
22 R22 seam chon ghi đè CA | t193_ | rc=0 | lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
SEAM intact before= 189 after= 189 CA_equal= True SO_equal= True OS_equal= True
SEAM chon_leak before= 189 after= 1 CA_equal= False SO_equal= True OS_equal= True
```

Đột biến rò `nen` sang `os.name` (R21) bị đỏ `NotImplementedError: cannot instantiate 'WindowsPath' on your system`; **không nhận tín dụng ca khóa đúng lý do**, vì đó là lỗi nền Linux chứ chưa chứng minh có chốt bảo toàn `os.name` trên Windows. Đột biến sổ tiêm cập nhật sổ thật (R23) bị t193 giết ở đối chứng (e), đúng hành vi cặp đăng ký bị đổi. Không bỏ qua hai kết quả khác nhau này.

**Hint patch:** mở t193 hoặc thêm ca meta chuyên bảo toàn: chụp `CA` (danh sách và identity hàm), `SO_BO_QUA` (nội dung), `os.name`, `sys.argv`; gọi seam nhiều lượt với chon/nen/so khác nhau, kể cả fixture ném lỗi, rồi assert tất cả nguyên trạng. Chạy lượt mặc định tiếp theo trên fixture kiểm soát để chứng minh argv/platform/sổ thật được dùng. R22 và R21 phải ĐỎ bởi assertion “rò trạng thái” trên cả Linux lẫn Windows, không dựa vào lỗi `WindowsPath`; vẫn giữ R23. Không sửa main chỉ để khôi phục trạng thái do chính ca probe đã cố ý sửa; khóa đặc tính của implementation nguyên vẹn.

## L5 — Tổng diff vượt ngưỡng packet đóng băng khi tính cả hồ sơ đi cùng nhánh · P2

**Trạng thái: MỚI, thuộc điều kiện nghiệm thu/phạm vi, không phải lỗi runtime.** Spec §6 (`ops/specs/lease-publish-windows-do-r1.md:77`) và lease :89 ghi dừng khi >300 dòng thêm; ADR-0044 :5–7 quy định packet sensitive ≤3 tệp, ≤300 dòng thêm theo numstat. Chưa thấy ngoại lệ loại spec/lease khỏi phép đếm trong các tài liệu đóng băng được cấp.

**Phép đo:** `git -C cay-kho diff 89fc4fac8cea65979cc2483043dc8cd07a6e8518 807c6c2898b2338cbc8f97cbcd8540519fbe4f8a --numstat`:

```text
264  34  ops/lease_publish_test.py
102   0  ops/leases/lease-publish-windows-do-r1-g1-claude.yaml
79    0  ops/specs/lease-publish-windows-do-r1.md
```

Tổng **445 thêm / 34 xóa**, 3 tệp; chỉ riêng mã test mới là 264 thêm. Mã nghiệp vụ và `.github/**` có diff rỗng. Hai commit dựng spec/lease có provenance riêng trước commit mã; điều này giải thích sự hiện diện của chúng, nhưng tự nó không tạo ngoại lệ ngưỡng 300 của toàn packet. Không kết luận lease là sửa trái phép chỉ từ việc nó ngoài write set mã executor.

**Hint xử lý:** người có thẩm quyền cần ghi rõ ngoại lệ/phạm vi tính kích thước bằng revision hợp lệ hoặc đưa hồ sơ điều phối ra khỏi đơn vị diff nghiệm thu theo protocol; không đổi baseline đóng băng hay bỏ 181 dòng khỏi phép đếm một cách ngầm định. Câu báo cáo cần thêm: “baseline..head gồm 3 tệp, +445/−34; riêng mã test +264/−34. Tổng vượt S5=300, chưa có ngoại lệ ghi trong spec r1.” Không có ca khóa runtime cho lớp hồ sơ; phép khóa là numstat trên exact hai SHA phải phản ánh toàn diff và quyền ngoại lệ được ghi nhận. Lượt review này vẫn hoàn thành theo chỉ thị trực tiếp của người dùng; không tiếp tục sửa/thi công packet.

### Bổ sung phép đo có hai tiến trình con thật cho L2

`PYTHONDONTWRITEBYTECODE=1 python r2-measure.fmUQ650G/real-children.py` chỉ đổi argv tại `_mo_con_nhom_rieng`, giữ Popen/wait/tee/verifier/classifier thật. Con đọc transcript fixture, phát stderr riêng rồi thoát 0. Output `real-children.log`:

```text
REAL_CHILDREN valid_CRLF spawned= 2 t125= PASS
REAL_CHILDREN all_status_invalid spawned= 2 t125= PASS
REAL_CHILDREN one_status_invalid spawned= 2 t125= PASS
```

Đối chứng CRLF + stderr riêng hợp lệ được nhận; hai transcript sai vẫn lọt với tiến trình thật, không chỉ do mock. Bổ sung L4: `probes.log` đã ghi `SEAM mutant followup main() defaults 0 lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0` sau lượt seam chọn lambda.

Định vị chính xác cho các chỗ mã chính (các khoảng trên dùng để dẫn đoạn): `_nhan_runs_on` trả sớm :584–590, kiểm matrix :593–600; main so resolve :10702, tính lý do :10704; verifier kết quả ra :4599, đối chiếu BỎ QUA :4603, tổng kết :4607–4610, rc :4611–4612.

### Bảng đột biến độc lập

Lệnh `python r2-measure.fmUQ650G/run-mutations.py`; runner lấy **dữ liệu** 14 phép thế của executor bằng `ast.literal_eval`, không thực thi runner có đường dẫn máy executor; chép ops/.github vào bản sao dưới thư mục mktemp và chạy CLI `--chi-ca=`. Mỗi phép thế đòi neo xuất hiện đúng một lần. Chi tiết output/diagnostic trong `mutant-01.log` … `mutant-23.log`, tổng hợp `mutations.log`.

| # | Đột biến | Ca đích | Output/kết quả và lý do |
|---|---|---|---|
| 01 | M1 bỏ kiểm sổ | t193 | rc1, 0/1; (a) ca ngoài sổ được miễn |
| 02 | M2 bỏ include | t193 | rc1, 0/1; (c/d) include Windows được miễn |
| 03 | M3 cho phép → prefix | t193 | rc1, 0/1; ubuntu-not-a-runner được miễn |
| 04 | M4a thêm tên tấn công | t193 | rc1, 0/1; sổ lệch tập bảy ca |
| 05 | M4b thêm t01 | t193 | rc1, 0/1; sổ lệch tập bảy ca |
| 06 | M4c thêm tên lạ | t193 | rc1, 0/1; sổ lệch tập bảy ca |
| 07 | M5 bỏ gọi verifier | t194 | rc1, 0/1; 0/0 đã tới classifier |
| 08 | M5 cùng mutant | t160 | rc1, 0/1; thiếu hai lời gọi verifier |
| 09 | M6 chỉ so số marker | t194 | rc1, 0/1; trùng tên đủ số lọt |
| 10 | M7 bỏ tổng kết–marker | t194 | rc1, 0/1; tổng kết sai được nhận |
| 11 | M8 bỏ chặn exclude | t193 | rc1, 0/1; exclude được miễn |
| 12 | M9 bỏ skip ⊆ sổ | t194 | rc1, 0/1; skip ngoài sổ lọt |
| 13 | M10 bỏ đúng một summary | t194 | rc1, 0/1; hai summary lọt |
| 14 | M11 include thiếu khóa | t193 | rc1, 0/1; tổ hợp thiếu os được miễn |
| 15 | R15 sổ thật thay đọc YAML thật | t193 | **SỐNG**, rc0, 1/1; finding L1 |
| 16 | R16 bỏ đối chiếu dòng BỎ QUA | t194 | **SỐNG**, rc0, 1/1; finding L2 |
| 17 | R17 bỏ kiểm rc | t194 | **SỐNG**, rc0, 1/1; finding L2 |
| 18 | R18 t125 bỏ truyền rc | t194 | **SỐNG**, rc0, 1/1; finding L2 |
| 19 | R19 cùng R18 | t160 | **SỐNG**, rc0, 1/1; finding L2 |
| 20 | R20 resolve → absolute | t193 | **SỐNG**, rc0, 1/1; finding L1 |
| 21 | R21 nen ghi os.name | t193 | rc1, 0/1 do WindowsPath trên POSIX; **không tín dụng giết đúng lý do**, L4 |
| 22 | R22 chon ghi CA | t193 | **SỐNG**, rc0, 1/1; finding L4 |
| 23 | R23 sổ tiêm ghi sổ thật | t193 | rc1, 0/1; đối chứng (e) sai cặp sổ |

Tổng: **23 lượt đo đột biến**, 15 bị giết đúng assertion, 1 đỏ phụ thuộc nền, **7 sống**. Hai cặp 07/08 và 18/19 là cùng phép sửa với hai ca đích; không khai 23 mutant khác nhau. 14/14 lượt executor khai được tái hiện, nhưng thêm đường vào cho thấy chưa thể suy “ca khóa đủ răng”. Mọi dòng 0/1 hoặc 1/1 trong bảng đều có `đã chạy=1, bỏ qua=0`.

### Đối chiếu từng tiêu chí §3/§4/§5

| Tiêu chí | Phép đo và kết luận |
|---|---|
| A1 | Sổ đúng 7 tên/cặp; 01,04–06 giết đúng t193, sai job/tệp bị chặn. **Đạt hành vi kiểm sổ hiện tại**, còn thiếu khóa đường workflow thật (L1). |
| A2 | Include Windows/prefix/exclude matrix bị chặn; 02,03,11,14 đỏ đúng lý do. **ĐÓNG MỘT PHẦN**: nhánh literal/list và trục phụ chưa hỗ trợ còn fail-open theo hợp đồng (L1). |
| A3 (khai) | REPORT-r2:9–12 khai chưa tách/chưa đo phần portable trên Windows. **ĐẠT phần khai**, không gọi đó là đo Windows. |
| t193 (a)–(e) | Chạy riêng `--chi-ca=t193_`: rc0, 1/1, chạy1, skip0. Các bẫy spec liệt kê bị giết; các đường bổ sung R15/R20/R22 sống. **Ca qua nhưng độ phủ chưa đủ** (L1/L4). |
| B1 | Hai transcript thiếu 0/0, 1/1 bị chặn; marker trạng thái hỏng và CA trùng vẫn lọt verifier/t125. **CHƯA ĐẠT toàn bộ hợp đồng** (L2). |
| B2 | `--chi-ca=t160_` rc0, 1/1; bỏ toàn lời gọi verifier bị bắt, bỏ truyền rc không bị bắt; verifier được mock. **ĐÓNG MỘT PHẦN** (L2). |
| t194 | `--chi-ca=t194_` rc0, 1/1; 07,09,10,12,13 bị giết đúng lý do. R16–R18 sống; thiếu trạng thái ra/CA trùng trong ca khóa. **Ca qua nhưng độ phủ chưa đủ** (L2). |
| Bảng đột biến §3/§4 | Đã chạy đủ các phép bắt buộc; **14/14 lượt executor khai bị giết đúng lý do**. Mở rộng có 7 lượt sống; không lấy 14/14 làm bằng chứng hoàn tất tất cả cổng. |
| Ruff §5.3 | Ruff 0.15.15, `python -m ruff check --select F --output-format=json ops/lease_publish_test.py` trên hai cây: rc1 mỗi vế, 9 finding mỗi vế. So `(code,message,dòng nguồn,column)` bằng nhau, **delta 0 ĐẠT**; không gọi là ruff sạch. |
| Windows §5.4 | **KHÔNG ĐO ĐƯỢC** native Windows, filesystem không phân biệt hoa/thường, Windows resolve/symlink/OS; không mạng và không có nền Windows/ủy quyền CI. CRLF/seam nt chỉ là phép thử cục bộ. Kỳ vọng 182/182 + 7 skip chưa được xác thực sau patch. |
| S5 / toàn diff | 3 tệp +445/−34 vượt ngưỡng 300 không có ngoại lệ trong spec (L5). |

Chạy riêng các ca mới/đổi bằng `python r2-measure.fmUQ650G/run-selected.py` (bên trong gọi `python ops/lease_publish_test.py --chi-ca=t<n>_`): **t71, t72, t73, t98, t125, t158, t160, t193, t194** mỗi ca rc0 và `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0`. Log `selected-t<n>.log`; `selected-t125.log` gồm hai con thật chạy toàn suite. Không dùng cờ nội bộ `--ab-con-noi-bo` cho lời gọi reviewer để bỏ qua t125.

Rig: Linux POSIX, Python 3.11.15, shellcheck 0.9.0, actionlint 1.7.7, ruff 0.15.15; các công cụ phụ thuộc có mặt. Không có ca bị ghi hồi quy vì thiếu shellcheck/actionlint.

### Hoàn tất đo suite §5.1 và kiểm bảo toàn cây

Lệnh duy nhất dựng/chạy hai vế trên cùng rig: `python r2-measure.fmUQ650G/run-suites.py` (base lấy bằng `git archive` của baseline; head là bản sao đầy đủ checkout, cùng Python/env, bỏ ambient GITHUB_ACTOR; cả hai gọi đúng `python ops/lease_publish_test.py`). Output `suites-summary.log`:

```text
3.11.15 (main, Mar  3 2026, 09:26:23) [GCC 13.3.0]
base rc= 0 seconds= 360.12
lease_publish: 187/187 đạt; đã chạy=187, bỏ qua=0
head rc= 0 seconds= 349.319
lease_publish: 189/189 đạt; đã chạy=189, bỏ qua=0
```

**§5.1 ĐẠT** về lượt chạy Linux: +2 ca, không có lỗi/skip mới. Thời gian chỉ mô tả lượt này, không suy cải thiện hiệu năng (có công việc reviewer khác chạy đồng thời).

Đếm lại bằng parser reviewer độc lập với verifier bị review: `python r2-measure.fmUQ650G/audit-local.py` → `audit-local.log`. Lấy danh sách ca từ AST của từng bản, so toàn bộ chuỗi vào/ra và kết quả, kiểm tên duy nhất và summary chính xác:

```text
base outer/A/B: mỗi lượt expected=187 events=374 ra=187 unique=187 EXACT=True
head outer/A/B: mỗi lượt expected=189 events=378 ra=189 unique=189 EXACT=True
RUFF base count=9
RUFF head count=9
RUFF exact diagnostic + source line + column delta zero=True
```

Bổ sung L1, sau khi dùng YAML thật ở đường WORKFLOW_DANG trong bản sao thay vì chỉ truyền `job=`: `probes.py` in cả ba dòng `UNSUPPORTED_MAIN fixed_exclude/list_exclude/bad_other_axis 0 lease_publish: 0/0 đạt; đã chạy=0, bỏ qua=1`. Sổ mặc định và main nguyên vẹn cũng nhận miễn ba cấu trúc không hỗ trợ; lỗi fail-closed không chỉ tồn tại trong helper tiêm.

Kiểm cuối: `git -C cay-kho status --porcelain` rỗng; `git -C cay-kho diff --exit-code` rc0. SHA256 mã test của cây gốc và bản head đã chạy đều `68904a2eec86358e44e0fac9b324381eff1bac73f93d943e0678449d2ece9cbb`. Không sửa `cay-kho/`; mọi script/log/bản đột biến trong `r2-measure.fmUQ650G/` được giữ để tái lập. Không tải mạng, không chạy Windows/CI, không đăng verdict hay nhận quyền approve/merge/land.

| lớp | mức | trạng thái (mới / mang từ r1) | sửa mã hay báo cáo |
|---|---|---|---|
| L1 — hợp đồng skip/bộ giải và ca khóa | P2 | mang từ r1; ĐÓNG MỘT PHẦN | Mã test/helper và ca khóa |
| L2 — tính đầy đủ transcript và biên verifier | P2 | mang từ r1; ĐÓNG MỘT PHẦN | Mã verifier/t194/t160 |
| L3 — lời khai/provenance | P4 | mang từ r1; ĐÃ ĐÓNG các yêu cầu cũ | Báo cáo: làm rõ phạm vi, cập nhật kết quả r2 |
| L4 — khóa bảo toàn seam | P2 | mới | Ca khóa mã test |
| L5 — ngưỡng toàn diff S5 | P2 | mới | Báo cáo/hồ sơ phạm vi hoặc revision có thẩm quyền |

VERDICT: CHANGES_REQUIRED
