# Review đặc tả lượt 4 — CI-TAI-DUNG-THEO-CAY

**Kết luận: `changes_requested`. Có 5 P2 và 2 P3 mở, không có P0/P1 được chứng minh trong lượt này.** A r4 giữ kết luận approve riêng về đặc tả văn bản. B1 r3 và B2 r3 cần revision.

Reviewer: Codex, họ model OpenAI, độc lập với người soạn. Thực hiện theo `PROMPT.md`: chỉ đọc trong RV, không mạng, không đọc `.codex` hay memory; mọi bản sao, phép thử và đầu ra mới ở `RV/out/`. Chuẩn L1–L7 là bản `cay-kho/.claude/skills/soan-spec/SKILL.md` được đề bài chỉ định. Không triển khai tính năng, sửa đặc tả, cấp lease hay công bố ra ngoài.

## Neo đã kiểm

| Đối tượng | Giá trị |
|---|---|
| SHA-256 `SPEC-A-r4.md` | `0400723011a4a2f0362736de6872a177537e36aeb403e5a4ce59cf8bbd96dacc` |
| SHA-256 `SPEC-B1-r3.md` | `814dfccaafcfed524fdaa733c94dfac3e6b1abd88a97b729005c18e4a2b6cb46` |
| SHA-256 `SPEC-B2-r3.md` | `a729dd7c3d931e87e54e293c83415eeda265fa46f063ab8c5bec7798f677a7a7` |
| `cay-kho` HEAD | `45bae8d07a8cdf06a1ca9a7a2e015a6258169379` |
| HEAD tree | `30d5c7dec30dc658ae04ef29a6ffafe94eb8f197` |
| `origin/master` cục bộ | `a31c680c8880786848f832a35554d9e84078b270` — khác HEAD đóng gói; review neo HEAD |
| Lịch sử / working tree | Không shallow; `git status --porcelain` rỗng ở đầu và cuối phép kiểm |
| Môi trường | Windows; Python 3.13 với `-S`, PyYAML 6.0.3 từ `RV/py-lib`; PowerShell với `-NoProfile` |
| Thời điểm | 20-11-2026; thời điểm UTC từng lệnh trong `review-evidence/commands.jsonl` |

A r4 có băm không đổi so với lượt 3. Hai OID land ADR-0053/0055 đều qua ba phép trên lịch sử HEAD: tệp tồn tại tại L (rc 0), chưa có tại L^1 (rc 128), L thuộc first-parent. Không fetch; đây không chứng nhận ref máy chủ hay quyền nâng trần hiện tại. [Neo, numstat và số đo](review-evidence/20261120T161531931226.txt), [băm kiểm lại](review-evidence/20261120T162309447100.txt).

Script tái lập: [review_r4.py](review_r4.py), [windows_probe.ps1](windows_probe.ps1); dùng lại [review_r3.py](review_r3.py), [review_r2.py](review_r2.py), [review_probes.py](review_probes.py). [review_tools.py](review_tools.py) ghi lệnh/cwd/rc/output, đặt TEMP/TMP trong `out/thu`, tắt bytecode và cấu hình Git người dùng. Nhãn `REAL` chỉ phép chạy Git hoặc hàm thật của kho; `MODEL` chỉ mô hình hợp đồng đặc tả, không phải triển khai B1/B2 hoặc phản hồi REST LIVE. Rc 0 của harness chỉ nghĩa là phép thử chạy xong.

## Trạng thái R1–R9 của lượt 3

| Phát hiện | Trạng thái lượt 4 | Phép đo và kết quả |
|---|---|---|
| R1 P2 — thiếu y04/y11 | **Đóng đúng hai chốt cũ; lớp thiếu consumer còn S1.** | `review_r4.py pins` dùng lại hàm `pins` lượt 3, thay YAML theo r3: B1 và B2 đều 15/15 guard đạt sau cập nhật đủ họ đã nêu; ngoại lệ rộng hơn đỏ. Nhưng bộ so Windows thật trên job mới của B1 đỏ, ngoài write set. |
| R2 P2 — thiếu lượt/attempt bóng | **Đóng phản chứng cũ ở cuối mẫu và latest; chưa đóng Q8, S3.** | `history`: 20 tốt + lượt thứ 21 thiếu artefact nay D0=false; `contract`: attempt 1 đỏ, attempt 2 xanh ⇒ rc 1. Nhưng một lượt đỏ mất artefact trước 20 lượt tốt ⇒ D0=true. |
| R3 P2 — bat đỏ oan làn nhanh/fallback | **Đóng phản chứng làn nhanh cũ; hợp đồng trạng thái cần S4/S5.** | `contract`: `khong_xet` làn nhanh/merge một cha/before khác P1 ở cả hai mode ⇒ rc 0 khi lý do được xác minh; không còn ép `gate-cong-cu` chạy. Nhánh `khong_tai_dung` không nguồn/khác image có đối chứng được yêu cầu ở D2. Mô hình giả định đã có bằng chứng độc lập cho lý do; không coi đó là đã đo REST. |
| R4 P2 — matrix skipped | **Đóng ở mức đặc tả.** | B2:101–102 và D4(ii) tách hình dạng job nghỉ cấp job và bắt đo REST thật trước land. Mô hình r3 nhận hai job-definition skipped của nhóm công cụ, không tạo chín shard/runner giả. LIVE D4 vẫn chưa đo. |
| R5 P2 — provenance | **Chưa đóng, S2.** | `provenance`: dòng checkout thật vẫn nhận SHA không tồn tại cùng tiền tố; phần “Merge … into …” là subject commit, không phải parents. Workflow-definition nguồn vẫn chưa là đầu vào chốt tái dùng. |
| R6 P2 — output sau lỗi | **Đóng đường fail-open cũ; sinh tương tác S5.** | `runtime`: tiến trình thật ghi output rồi rc 1; biểu thức mới trả rỗng. Ma trận 4×4 outcome chỉ nhận cặp success/success. Tuy nhiên bằng chứng đã ghi trước lỗi có thể còn `tai_dung`, làm replay bat đỏ oan. |
| R7 P3 — latency | **Đóng lời hứa không kéo dài toàn run vô điều kiện; còn S6.** | Đã có phép đo cả hai thời gian, nhưng “toàn lượt dài thêm tối đa 3 phút” chưa tính hàng đợi; không có needs cũng chưa bảo đảm không tranh runner với check bắt buộc. |
| R8 P3 — mã E tại câu | **Đóng.** | B1:112 và :219–222 nay có E2/E5; E1/E2/E3/E5 của ba spec đủ payload theo ADR-0067. |
| R9 P3 — năm/bốn bước | **Đóng.** | YAML r3 có đúng bốn bước push mới; bảng ước, mục tiêu 3, C3, C5 nay thống nhất bốn. |

15 guard ở đây không tính y15, vì y15 tự kiểm loader và không được thay loader như các phép kiểm YAML khác. Không nâng số này thành “mọi consumer đã đạt”. [Guard Python và các ngoại lệ](review-evidence/20261120T161723250163.txt), [hợp đồng r3](review-evidence/20261120T162742308775.txt), [lịch sử r3](review-evidence/20261120T161835039041.txt).

## Trạng thái F và N kế thừa

| Finding | Trạng thái và bằng chứng lượt 4 |
|---|---|
| F1 P1 | Giữ đóng ở bộ xét B1: chạy lại fixture rename bằng Git/hàm registry thật; before=P1 nhưng hai kế hoạch khác ⇒ loại `nhanh`. S4 là thiếu kiểm lại bất biến này ở B2, không phải B1 quay về phép so cũ. |
| F2 P2 | **Còn mở, S1.** Những họ Python đã đủ; B1 vẫn thiếu hai tệp gương Windows. |
| F3 P2 | Giữ đóng ở mức đặc tả: C1/D1 đòi chạy trực tiếp Windows, không nhận job Linux-only làm bằng chứng Windows. Chưa chạy M3 triển khai chưa có. |
| F4 P2 | **Còn mở phần identity, S2.** Attempt/schema/tập shard/giới hạn image đã được xử lý; prefix SHA và subject chưa thay được checkout/workflow identity. |
| F5 P2 | Giữ đóng: A có T4/P1/P2/R nhất quán; classifier thật vẫn cho push hồ sơ `duong_nhanh`, `packet_loop=chay`. |
| F6 P2 | Giữ đóng: A2/A3/A4/A6 ứng viên xanh, 19 đột biến nội dung đỏ, reflow Q1 xanh; A5 Git thật bắt tệp thứ ba; A1/A7 có phản chứng thật. |
| F7 P3 | Giữ đóng tiền đề C5: chạy lại fixture cũ cho diff khác nhưng kế hoạch thật bằng nhau; C5 đã khai tiền đề nhóm/attempt/image/kế hoạch. LIVE vẫn chưa đo. |
| F8 P2 | **Còn mở, S2–S5.** Replay đã chặt hơn về trường và inventory nhưng chưa là chứng minh độc lập đầy đủ cho quyết định và lịch sử. |
| F9 P3 | Đóng lỗi ước cũ và vòng phụ thuộc; khối xin nâng trần có hình thức đúng. S1 buộc ước lại trên write set đủ; S7 là con số B2 sót ở mục dừng. |
| F10 P3 | Giữ đóng các phản chứng L6/L7 cũ. Các thiếu sót thước đo mới được ghi riêng S3–S5. |
| N1 P2 | Đóng mâu thuẫn mode cũ: bong đúng ⇒ rc 0, bat đúng ⇒ rc 0, kết quả sai ⇒ rc 1. S5 là tương tác mới với outcome. |
| N2 P2 | **Chưa đóng toàn bộ, S1.** Không còn các y* cũ bị bỏ sót; còn consumer Windows của job biên nhận. |
| N3 P2 | **Chưa đóng toàn bộ, S2–S5.** Đổi source/kế hoạch/job list/zip hash/checkout line bị bắt; quyết định sai nhưng các trường mô tả trung thực vẫn có đường lọt. |
| N4 P2 | Đóng lỗi cô lập failure cũ: bốn bước mới COE; receipt job COE, không job nào needs receipt hoặc đọc `*_bong`. Latency còn S6 P3. |
| N5 P2 | Giữ đóng: bảng ngoại lệ làm A2 đỏ, Bối cảnh rỗng làm A6 đỏ. |
| N6 P2 | Giữ đóng: một/hai `doc_diff=None` loại `nhanh`; hai diff rỗng thật vẫn hợp lệ; truyền đúng `manh`. |
| N7 P2 | Giữ đóng: giao diện `kiem-tai-dung` nhận cây; Git thật cho baseline rc 0, sửa cây/đảo cha rc 1. |
| N8 P3 | Đóng các câu L7 cũ và R8. Không đặt thêm điểm hỏi chủ kho trong review này. |
| N9 P3 | Đóng vòng chờ cấp lease/D0 và thiếu khối nâng trần cũ. D0 được đo trước merge bằng mã B2; 550 vẫn chỉ là trần xin. |
| N10 P3 | Giữ đóng lời hứa sai về `contains`: chỉ bảo đảm producer chuẩn. Không dùng contains làm bộ xác thực toàn chuỗi; S4 yêu cầu kiểm lại quyết định/nhóm rõ hơn. |

## Các phát hiện còn mở và mới

### S1 — P2 — B1 vẫn thiếu consumer Windows; 15/15 y* không chứng minh đủ write set

**Vị trí:** `SPEC-B1-r3.md:70–74`, `:84–88`, `:116–117`, `:131–134`; mã `cay-kho/.claude/dev/chay-cong-windows_test.ps1:1248–1252`, `:1310–1315`, `:1399–1412`.

Câu “bản gương Windows … chỉ soát job gate*” sai với mã thật. Cả `Doc-DichCi` lẫn `Doc-DauVanCi` chỉ bỏ `chuan-bi`, rồi duyệt **mọi job còn lại**. Tên ca t32 có chữ `gate*` không phải điều kiện lọc. Thêm job bắt buộc `bien-nhan-cay` làm thiếu dấu vân và thiếu gương lệnh/khai báo KHÔNG CHẠY. Hai nơi sửa đều ngoài write set ba tệp của B1; không thể chờ B2 sửa vì B1 phải land độc lập trước B2.

**Lệnh:** `python -S out/review_tools.py python out/review_r4.py windows` ⇒ harness rc 0. Probe trích nguyên AST năm hàm so và hai bảng từ PowerShell thật; chỉ thay cách chọn Python để dùng `-S` và `py-lib`, không sửa predicate.

```text
BASE:                                     t32_equivalent_rc=0, errors=[]
B1_R3_UNCHANGED_WINDOWS:                   t32_equivalent_rc=1
  bien-nhan-cay :: ops/ci_duong_nhanh.py bien-nhan-cay
  job bien-nhan-cay :: <DAU-VAN> job MOI chua ghim
B1_R3_ADD_FINGERPRINT_ONLY:                t32_equivalent_rc=1 (thiếu gương)
B1_R3_ADD_FINGERPRINT_AND_MIRROR_NOTE:      t32_equivalent_rc=0
B2_R3_AFTER_LISTED_WINDOWS_UPDATES:        t32_equivalent_rc=0
```

[Output PowerShell](review-evidence/20261120T162212708316.txt), [YAML B1](thu/b1-r3-witness.yml), [YAML B2](thu/b2-r3-witness.yml). Không khai chạy trọn suite PowerShell. Kết quả y04/y11 của R1 vẫn đúng; phép đo Windows của harness cũ chỉ áp tám điều kiện lên nền, chưa áp job biên nhận mới. Nhận định Windows ở verdict lượt 3 vì thế chưa đủ và được sửa trong lượt này.

**Hướng sửa:** đưa `.claude/dev/chay-cong-windows_test.ps1` và `.claude/dev/chay-cong-windows.ps1` vào B1; ghim job mới sau rà soát và khai bước biên nhận không chạy trong gương Windows, hoặc thiết kế ngoại lệ hẹp có ca/đột biến tương ứng. Bổ sung nghiệm thu consumer này, ước dòng và rà lại `nang_tran`. Không tắt guard chung. B2 giữ cập nhật Windows cho các thay đổi riêng của B2.

### S2 — P2 — R5 chưa đóng: dòng HEAD không chứng minh full SHA/parents, workflow-definition nguồn vẫn thiếu

**Vị trí:** `SPEC-B1-r3.md:57–61`, `:150–154`, `:174–176`; `SPEC-B2-r3.md:92–98`, `:29–32`; đối chiếu `SPEC-A-r4.md:232–243`, `:253–254` và `cay-kho/docs/PROTOCOL_DA_PHIEN.md:968–983`.

`<h>` chỉ là SHA viết tắt. Một receipt thay phần đuôi SHA, giữ tiền tố đúng, vẫn qua 4d dù object không tồn tại. Phần `Merge <P2> into <P1>` của thông báo checkout là **subject commit**, không phải phép đọc `%P`; Git có thể in cùng khuôn cho commit một cha. Giới hạn “suy cây bằng merge-tree” đã được khai nhưng không biến subject thành chứng minh parents hay ràng SHA đầy đủ của receipt với checkout nguồn.

**Lệnh:** `python -S out/review_tools.py python out/review_r4.py provenance` ⇒ rc 0; Git thật trong `out/thu/`:

```text
log thật: HEAD is now at 3470fbe Merge <P2> into <P1>
checkout thật: 3470fbed58213a951ba82e17d14ed3247033030a
receipt.sha:   3470fbe000000000000000000000000000000000
4d r3: accepts=true; git cat-file -e receipt.sha^{commit}: rc=128

commit khác có MỘT parent thật, subject "Merge <P2> into <P1>":
git checkout in đúng khuôn; 4d r3 vẫn accepts=true
```

[Output](review-evidence/20261120T161834251879.txt), [fixture và OID](thu/provenance-r4.json). Phản chứng chứng minh giới hạn của phép đọc log được chọn; **không** tuyên bố đã tạo một Actions PR run ác ý hay GitHub đã sinh merge sai. Đuôi SHA giả là đột biến một trường receipt trong khi log thật không đổi.

Ngoài ra, B1 chỉ ghi blob workflow tại M; 4a–4g không xác minh definition của run/attempt PR nguồn. B2:31–32 đã sửa lời hứa về bốn mốc khi ghi `landed`, nhưng việc thu sau đó không cưỡng chế G1 (“định nghĩa workflow phải bằng nhau”) **trước khi bỏ job**. Không được đóng phần này của R5 bằng lời nhắc rằng hồ sơ land sẽ đo riêng.

**Hướng sửa:** neo full checkout SHA từ nguồn độc lập của đúng job/attempt và kiểm parents/tree gắn với SHA ấy. Nếu object không còn lấy được, lưu đủ bằng chứng commit lúc còn có thể kiểm, hoặc không tái dùng; không chỉ so tiền tố/subject. Đo exact workflow-definition nguồn và so với lượt push trước khi xuất quyết định. Bổ sung đột biến đổi đuôi SHA, subject giống nhưng parents khác, definition nguồn khác; thiếu chứng minh ⇒ fallback. Bốn mốc Q6 vẫn là nghĩa vụ riêng.

### S3 — P2 — Cửa sổ mới cho D0 quên một vi phạm khi artefact biến mất

**Vị trí:** `SPEC-B2-r3.md:103–110`, `:136`, `:157–162`, `:183`; đối chiếu Q8 tại `SPEC-A-r4.md:246–248`.

r3 giữ mọi lượt trong bảng, nhưng D0 chỉ đòi 20 lượt `tai_dung` trong đoạn cuối không rc2 và `rc1_toan_bo=0`. Một lượt từng có nhóm được đánh dấu và push đỏ sẽ thành rc2 khi artefact mất/hết hạn. Nếu sau đó có 20 lượt tốt, nó nằm ngoài cửa sổ và không còn tăng `rc1_toan_bo`. D0 đổi đỏ thành xanh dù không có sửa thuật toán hoặc thay đổi kết quả job. Đó vẫn là bỏ ảnh hưởng của lượt chưa đo khỏi quyết định, dù hàng trong bảng không bị xoá. Q8 của A không cho reset lịch sử theo việc mất artefact.

**Lệnh:** `python -S out/review_tools.py python out/review_r4.py history` ⇒ rc 0:

| Cùng lịch sử 21 lượt | `tai_dung` trong cửa sổ | `rc1_toan_bo` | `rc2_toan_bo` | D0 |
|---|---:|---:|---:|---|
| Lượt 0 đánh dấu ops và đỏ; lượt 1–20 tốt | 20 | 1 | 0 | false |
| Chỉ làm mất artefact lượt 0; kết quả job giữ nguyên | 20 | 0 | 1 | **true** |

[Output](review-evidence/20261120T161835039041.txt), [các lịch sử thử](thu/q8-r3-scenarios.json). Đây là mô hình đúng công thức mới, không phải dữ liệu API LIVE. Không cần giả định ai có quyền sửa log: mất bằng chứng hoặc retention cũng tạo đường này. Đột biến D2 hiện chỉ đòi “cửa sổ bị cắt”; phản chứng trên vẫn thỏa điều đó.

**Hướng sửa:** neo tập run/attempt, phiên bản bộ xét và thời điểm cắt; giữ vi phạm đã phát hiện bằng bằng chứng bền. Mọi khoảng chưa xác minh được trong phạm vi Q8 phải chặn bật hoặc được khôi phục từ nguồn độc lập. Nếu muốn chỉ một cửa sổ đánh giá mới có quyền loại lịch sử, phải định nghĩa điều kiện mở cửa sổ và sửa luật A tương ứng; không để việc mất artefact tự cấp quyền reset. Đột biến “lượt đỏ mất artefact + 20 tốt” phải giữ D0 không đạt.

### S4 — P2 — Replay so từng trường với bản ghi nhưng chưa buộc quyết định thỏa lại các phép B1

**Vị trí:** `SPEC-B2-r3.md:87–110`, `:136–138`; đối chiếu `SPEC-B1-r3.md:144–176`, nhất là :160–164.

1c yêu cầu hai kế hoạch tính lại **bằng bản đã ghi**, nhưng không nói phải bằng **nhau** khi đánh dấu `nhanh`. Nó gọi rõ lại 4f mà không gọi lại toàn bộ 4a–4g rồi so quyết định/tập nhóm. Vì vậy một bộ xét lỗi đánh dấu `nhanh` trong khi đã ghi trung thực hai kế hoạch khác nhau có thể qua các phép được liệt kê ở 1c/1d, nếu job hai lượt đều success. Chỉ đổi một trường của receipt như D2 hiện có không kiểm được trường hợp này.

**Lệnh:** `python -S out/review_tools.py python out/review_r4.py contract` ⇒ rc 0. Tái dùng **fixture Git và các hàm registry thật** đã dựng F1; chỉ bộ replay là mô hình câu chữ:

```text
accurate_fields_but_Q7_false:
  actual_plans_equal=false; B1_4g_eligible=false; replay_rc=0
changed_plan_pr (chỉ sửa lời khai, không đổi dữ kiện): replay_rc=1
```

[Output](review-evidence/20261120T162742308775.txt), [record chứa hai kế hoạch thật](thu/r4-q7-replay-record.json), [phép rename gốc](review-evidence/20261120T161612049312.txt). Đây là thiếu bất biến trong đặc tả của bộ kiểm độc lập; không phải bằng chứng implementation tương lai chắc chắn bỏ bất biến đó.

Ba trạng thái cũng cần schema và bất biến riêng. Hiện chưa ghi rõ `tai_dung` ⇔ có ít nhất một nhóm hợp lệ, hai trạng thái kia ⇒ tập nhóm/output rỗng; D0 đếm **nhãn** `quyet_dinh=tai_dung`. Mô hình các kiểm tra đã liệt kê nhận nhãn ấy với groups rỗng dù danh sách job của run không rỗng; 20 nhãn như vậy đủ D0. Nếu “không bao giờ rc 0 trên tập rỗng” ở 1e định nói cả tập nhóm, cần ghi rõ, vì nhánh 1b lại cố ý cho trường hợp không tái dùng rc 0. Tương tự, fallback không có nguồn không thể mang đủ các trường source/ZIP mà B1 liệt kê chung; cần phân biệt trường không áp dụng với trường bị mất. Kiểm lý do “không nguồn hợp lệ/ảnh không khớp” cần bằng chứng REST/ảnh, không chỉ các dữ kiện Git trong ngoặc của 1b.

**Hướng sửa:** quy định replay dựng lại điều kiện chung và từng nhóm từ dữ kiện độc lập, rồi so `(quyet_dinh, nhóm, lý do)` với bản ghi, ngoài việc so từng trường. Nêu schema có điều kiện cho ba trạng thái, phạm vi job cần đọc, quy tắc rc1/rc2 và bất biến nhóm không rỗng của trạng thái tái dùng. D0 đếm run có nhóm hợp lệ đã xác minh, không đếm nhãn đơn thuần. Bổ sung ca “hai kế hoạch khác nhau nhưng ghi đúng cả hai và vẫn đánh dấu nhanh”, `tai_dung` với nhóm rỗng, trạng thái không tái dùng nhưng còn nhóm/output, và reason không chứng minh được.

### S5 — P2 — Outcome đã fallback đúng nhưng replay bat vẫn buộc job nghỉ theo ý định trước lỗi

**Vị trí:** `SPEC-B1-r3.md:137–143`, `:166–176`, `:190–191`; `SPEC-B2-r3.md:99–104`, `:111–114`, `:141`.

R6 sửa đúng: output thật rỗng nếu bước xét thất bại. Nhưng bằng chứng phải được ghi **trước** output. Một tiến trình ghi xong JSON `quyet_dinh=tai_dung, groups=[ops]`, ghi output rồi lỗi có thể để lại tệp hợp lệ; upload thành công, còn outcome xét là failure. YAML r3 chạy ops theo fallback. Replay bat chỉ đọc quyết định trong artefact, không đọc outcome của hai bước để phân biệt quyết định đã được áp dụng, nên thấy ops success và trả `LECH_BAT`. Đây là một lượt thực hiện đúng C2/R6 mà D5 bắt buộc chấm đỏ.

**Lệnh:** `python -S out/review_tools.py python out/review_r4.py contract` ⇒ rc 0. Tiến trình con thực sự ghi hai tệp rồi ném lỗi; upload và REST job là dữ kiện mô hình:

```text
evaluator_rc=1; artifact_survives=true
evaluator_outcome=failure; upload_outcome=success
effective_job_output=''; actual_ops_conclusion=success
correct_yaml_fallback=true; replay_rc=1
```

[Output](review-evidence/20261120T162742308775.txt), [JSON sống sau lỗi](thu/r4-failed-evaluator-artifact.json), [output bước sống sau lỗi](thu/r4-failed-evaluator-outputs.txt). Ma trận outcome ở [runtime](review-evidence/20261120T161717949100.txt) xác nhận biểu thức mới không bỏ job trong đường này.

**Hướng sửa:** tách kết quả tính toán với quyết định thực tế được áp dụng. Replay đọc outcome đúng attempt của bước xét/upload, dựng tập tái dùng có hiệu lực như biểu thức output của workflow, rồi so hành vi job với tập ấy và chính sách nền. Khi chưa xác định được áp dụng hay chưa thì rc2; không gắn `LECH_BAT` cho fallback đúng. Thêm đối chứng dương lỗi sau khi đã ghi JSON/output, upload thành công, tất cả nhóm chạy lại.

### S6 — P3 — R7 còn lời hứa thời gian vượt điều DAG/timeout bảo đảm

**Vị trí:** `SPEC-B1-r3.md:53–55`, `:131–134`, `:196`, `:208–210`.

Job riêng không có dependent loại chờ trực tiếp trong DAG. Nó không loại thời gian queue hoặc tranh chỗ runner. Trần execution 3 phút không cho trần “toàn lượt PR dài thêm tối đa 3 phút”. Với số slot hữu hạn, job biên nhận còn có thể chạy trước check bắt buộc; không có điều kiện/đối chứng nào ở C5 chứng minh lời hứa tuyệt đối không tăng thời gian check đó. Số liệu được cấp cũng phân biệt queue với thời gian chạy, không coi queue bằng 0.

**Lệnh:** `python -S out/review_tools.py python out/review_r4.py runtime` ⇒ rc 0:

```text
MODEL queue: check cũ xong giây 90; receipt ready 30, queue 600,
             chạy 179 (<180), xong 809 => toàn run tăng 719 (>180).
MODEL một slot: receipt chạy 179 giây trước check ready cùng lúc;
                check bắt buộc xong 90 -> 269 dù không needs receipt.
```

[Output](review-evidence/20261120T161717949100.txt). Đây là phản chứng scheduling, **không** là đo latency thật hoặc khẳng định kho hiện có một slot. Đặt P3 vì chưa chứng minh hồi quy thời gian trên CI LIVE.

**Hướng sửa:** thu hẹp bảo đảm thành không thêm dependency của check bắt buộc; khai rõ queue/execution/toàn run, bỏ trần toàn run suy từ timeout. C5/C6 đo check completion và queue ở cả PR đầy đủ/làn nhanh, nêu tiêu chí chấp nhận hoặc cách xử lý hồi quy đo được.

### S7 — P3 — B2 còn hai ước kích thước hiện hành khác nhau

**Vị trí:** `SPEC-B2-r3.md:69–73`, `:151–152`.

Bảng khối mới cộng 368 ≈ 370 dòng, nhưng mục `luat_dung` vẫn ghi 335. Đây không phải số lịch sử nằm trong phần “thay đổi so với r1”; nó đang ở quy tắc thi hành hiện hành, làm hai mức dự phòng dưới trần 450 khác nhau.

**Lệnh:** `python -S out/review_tools.py python out/review_r4.py runtime` ⇒ rc 0: `B2_ESTIMATE_R3 total=368, approximation=370, stop_section_still_says=335, cap=450`. [Output](review-evidence/20261120T161717949100.txt).

**Hướng sửa:** cập nhật :151 thành khoảng 370 hoặc dẫn thẳng bảng ở mục 1; giữ phân biệt ước thiết kế với numstat ứng viên phải đo trước công bố.

## Đối chiếu trích dẫn và lời khai về mã

[citation-audit.json](citation-audit.json) đối chiếu **60 lần dẫn tệp:dòng** trong ba bản hiện hành, gồm 10 của A, 24 của B1, 26 của B2; lưu dòng dẫn và đoạn mã thật. Neo dòng đều thuộc đúng vùng được dẫn. Riêng B2:48 dẫn :1525 là dòng tiếp của nhánh `gate-registry` bắt đầu ở :1524; không coi lệch một dòng trong cùng biểu thức là finding. **Neo dòng đúng không chứng minh diễn giải đúng:** câu Windows ở B1:72–74 là phản chứng S1.

| Lời khai | Kết quả và giới hạn |
|---|---|
| Bốn nhóm/tám job | Đúng 8 định nghĩa job, tổng 37 instance Ubuntu khi nở đủ ma trận: 9+1+10+17. Job biên nhận mới ngoài nhóm. |
| Q4 theo event/ref | Quét nền: các bước có if trực tiếp theo event/ref đều ở gate; không ở job nhóm. Quy tắc mới có ca canh; chưa chạy triển khai tương lai. |
| B1 không job nào đọc `*_bong` / needs receipt | Đúng trên YAML chứng kiến r3; 4 bước mới COE, tổng timeout 23 < trần job 30; receipt job COE, timeout 3. Không suy từ đó ra bảo đảm latency, S6. |
| Gương Windows | **Lời khai B1 sai**, S1. Chạy bộ so thật: baseline xanh; B1 thêm job mới đỏ; sửa fingerprint và khai báo gương trên bản sao mới xanh. B2 sau sửa B1 và cập nhật đúng các họ Windows đã nêu đạt. B2 đầy đủ làm đổi 9 fingerprint (8 job nhóm và gate); con số 8 dẫn từ phép thử chỉ sửa if là đúng cho phép thử lịch sử đó. |
| t161 và t6 | Hai helper t161 thật trả `[]` trên nền/B1/B2. Bước mới sau G5 ⇒ t6 thật đạt. Không thêm `strategy.matrix.os` riêng. |
| Consumer registry | Hàm thật đọc diff độc lập; None không được biến thành diff rỗng; tham số `manh` đúng consumer. B1 không làm đổi các guard registry đã thử; B2 cập nhật các họ đã nêu thì đạt. |
| `goi_that` | Dùng opener giả, không mạng: redirect trả 200, request sang host khác không mang token. Timeout từng request 120 giây không tự chứng minh deadline tổng 120 giây của bộ xét; phải thực hiện và kiểm deadline tổng như C2 yêu cầu. |
| PyYAML | `python -S` thiếu `py-lib` không import được registry; thêm thì được. Chưa đo gói sẵn có trên image hosted runner; câu “hệ thống không có PyYAML” là lời khai phía tác giả, không kết luận mới của review. |
| Vùng mã 94cbb36 → HEAD | `git diff --stat` trên đúng tập đường dẫn B1 dẫn rỗng. |
| #674 / #1343 | Đo lại numstat: #674 ci.yml +90, classifier +618, test +3608; #1343 bốn tệp +56/+29/+133/+8 = 226. Khớp số tham chiếu. |
| A: 147/79/25/44/10, 8/8 | Khớp đề xuất cấp sẵn. Đề xuất ghi kiểm log **gate** 8 PR; không có log thô để đo lại hoặc suy ra đã kiểm cùng job chuan-bi. B1 mới dùng chuan-bi phải đo riêng ở C5. |
| Đo lần 2 | JSON có 60 lượt, 28 đầy đủ xanh; tính từ số làm tròn cho median wall 30,35, runner 266,5; bản tổng từ số gốc ghi 30,4/266,1, spec dùng 30,4/266. Không coi khác độ chính xác là finding. |
| Tổng nhóm / queue | 146,2+0,2=146,4; 25,3; 9,2+0,3+23,6=33,1; 41,5+0,2=41,7. Queue 2/878/123 khớp bảng cấp sẵn; thiếu jobs thô để tái tính percentile. |
| A “0 cổng” | 0 marker tính năng ở đủ sáu vị trí cổng và classifier. Đây là phép đo tên tính năng tại nền, không chứng minh mọi hành vi tương đương vắng mặt. |
| Hồ sơ land pr997 | Thực sự tách run/attempt, checkout, workflow definition và gate output; hỗ trợ việc không thay definition bằng blob tại M. |
| Lease, ADR còn trống, refs máy chủ | Là số đo phía tác giả có thời điểm. Không đọc D:/tlscan.git hoặc kết nối máy chủ; phải đo lại lúc công bố/cấp lease theo spec. |
| Hạn lưu artefact 90 ngày | Không có cấu hình dịch vụ hiện tại để xác minh trong hộp offline. S3 không phụ thuộc hạn cụ thể. |

## `nang_tran` và L1–L7

Khối B1 parse được, đúng bốn trường `ai_nang`, `can_cu`, `tran_cu`, `tran_moi`; có chủ kho, lý do không tách, numstat tham chiếu và cặp trần **6 tệp/450 dòng thêm → 6 tệp/550 dòng thêm**. Cộng bảng đúng **480**, còn **70** so với trần xin. 550 chưa được coi là đã duyệt. ADR-0053 còn yêu cầu chép khối vào lease và đo numstat ứng viên. S1 làm phạm vi ba tệp hiện khai chưa đủ; phải tính lại sau sửa, không coi 480 là ước đã bao cả hai consumer Windows.

| Luật | A r4 | B1 r3 | B2 r3 |
|---|---|---|---|
| L1 — con số đếm gì | Tám Q, ba K, bốn phép chèn, hai tệp rõ. | Bốn bước đã thống nhất; 480 là dòng thêm ước. 15/15 chỉ đếm y*, không đếm Windows, S1. | 20 phải là run có nhóm hợp lệ, không chỉ nhãn, S4; 368≈370 nhưng còn 335, S7. |
| L2 — mục tiêu/write set | Hai tệp đủ cho đổi văn bản. | **Chưa đạt: thiếu hai tệp Windows, S1.** | Sáu tệp chứa các consumer đã đo; các sửa hợp đồng còn lại ở trong vùng được phép, nhưng phụ thuộc B1 phải sửa trước. |
| L3 — phép làm đỏ | Nền/ứng viên/đột biến đổi đúng màu; gate thật có răng. | Identity cần thêm đột biến S2; output failure cũ được chặn. | Q8, quyết định độc lập và fallback còn S3–S5. |
| L4 — kế thừa | `khong_ap_dung` có lý do. | Có ghi lần thứ ba lớp chốt bỏ sót; S1 chứng minh cách đo cần mở rộng consumer. | Có ghi lớp lỗi cũ. Draft revision chưa tự thành packet khắc phục đã land; không tự áp thêm điểm hỏi. |
| L5 — thời điểm/đo lại | Neo băm/ngày rõ; trạng thái server chưa đo trong review offline. | Số tham chiếu đo lại khớp; 480 vẫn là ước, chưa bao S1; trần xin không thành quyền đã cấp. | D0 cần lịch sử/bằng chứng bền S3; sửa số 335 ở S7. |
| L6 — thước đo | Đã chạy lại script A và 0-cổng, reflow xanh/đột biến đỏ. | C5/C6 LIVE chưa đo; tách marker với nội dung hậu kiểm là đúng. | Mô hình r3 chứng minh còn trường hợp xanh giả/đỏ oan S3–S5; D4(ii) đúng cách yêu cầu fixture LIVE. |
| L7 — hỏi chủ kho | E2/E5 và payload đủ tại các câu hành động. | R8 đã sửa; E1/E2/E5 đủ, `nang_tran` có E2 gộp E5. | E2/E3/E5 đủ, E3 nêu quyết định bị đảo/bằng chứng/hậu quả. |

[l7-audit.json](l7-audit.json) giữ ngữ cảnh những câu nói tới hỏi/chờ/duyệt. Đã đọc từng câu và đối chiếu ADR-0067, không suy đạt chỉ vì cùng đoạn có một chữ E. Các câu lịch sử A:203 và B1:302 nói “mọi câu hỏi mang mã E” là mô tả việc sửa, không tạo một yêu cầu hỏi mới. Hai câu thực thi R8 được kiểm tại B1:112 và :219–222; payload E5 ở A:155–159, B1:236–239, B2:168–171. Không thấy ngân sách mềm hoặc quy tắc tự đặt “N lượt chưa approve”.

## Bảng lệnh đã chạy

`RV=C:\r\d2`, `REPO=RV/cay-kho`. Wrapper gọi từ RV; bảng ghi cwd lệnh con. Tất cả output đầy đủ nằm trong liên kết từng dòng; rc của ca âm nằm trong output. Hai lỗi của harness cũng được giữ lại: glob `q7-*` bắt nhầm tệp JSON mới, và bộ giải dẫn rút gọn nhận nhầm context sau ví dụ pr997. Đã sửa chỉ trong `out/` rồi chạy lại thành công; không quy thành lỗi sản phẩm.

Đọc thăm dò trước wrapper (rc 0, cwd RV): `Get-Content -LiteralPath 'C:\r\d2\PROMPT.md' -Raw`; `Get-ChildItem -Force`; đọc có số dòng ba spec; đọc `VERDICT-luot3.md`, skill L1–L7, `luot3/out/review_tools.py`, `review_r3.py` và các phần liên quan của `review_r2.py`/`review_probes.py`; `rg -n` tìm hàm và thao tác ghi trong các harness. Không có AGENTS.md ở root RV. Chuẩn bị: `New-Item -ItemType Directory -Force -Path 'out/thu','out/review-evidence'`; sao bốn harness từ `luot3/out` vào `out`; mọi patch sau đó chỉ sửa/tạo tệp trong `out`. Output các bước này nằm trong transcript công cụ.

<!-- COMMAND_TABLE_BEGIN -->
| # | Lệnh (gọi từ RV) | cwd | rc | Kết luận / output |
|---|---|---|---|---|
| 1 | <code>python -S out/review_tools.py &#x27;hash&#x27; &#x27;SPEC-A-r4.md&#x27; &#x27;SPEC-B1-r3.md&#x27; &#x27;SPEC-B2-r3.md&#x27;</code> | RV | 0 | Đo SHA-256 các đặc tả. [Output](review-evidence/20261120T161517025260.txt) |
| 2 | <code>python -S out/review_tools.py &#x27;python&#x27; &#x27;out/review_r2.py&#x27; &#x27;anchor&#x27;</code> | RV | 0 | Neo HEAD/tree/ref, ADR land, numstat tham chiếu, số đo JSON. [Output](review-evidence/20261120T161531931226.txt) |
| 3 | <code>python -S out/review_tools.py &#x27;read&#x27; &#x27;DIFF-B1-r2-r3.patch&#x27; &#x27;DIFF-B2-r2-r3.patch&#x27;</code> | RV | 0 | Đọc/tìm/đối chiếu vật liệu, không sửa nguồn. [Output](review-evidence/20261120T161532804329.txt) |
| 4 | <code>python -S out/review_tools.py &#x27;read&#x27; &#x27;cay-kho/.github/workflows/ci.yml@1:180&#x27; &#x27;cay-kho/.github/workflows/ci.yml@1120:1240&#x27; &#x27;cay-kho/docs/adr/0053-tran-kich-thuoc-sensitive-len-sau-tep.md@20:58&#x27; &#x27;cay-kho/docs/adr/0067-danh-sach-dong-va-uy-quyen-thuong-truc.md@20:55&#x27; &#x27;cay-kho/docs/PROTOCOL_DA_PHIEN.md@965:1000&#x27;</code> | RV | 0 | Đọc/tìm/đối chiếu vật liệu, không sửa nguồn. [Output](review-evidence/20261120T161533644397.txt) |
| 5 | <code>python -S out/review_tools.py &#x27;read&#x27; &#x27;luot3/out/review_r2.py@218:289&#x27; &#x27;cay-kho/ops/ci_duong_nhanh_test.py@2462:2517&#x27; &#x27;cay-kho/ops/ci_duong_nhanh_test.py@2840:3010&#x27;</code> | RV | 0 | Đọc/tìm/đối chiếu vật liệu, không sửa nguồn. [Output](review-evidence/20261120T161554983523.txt) |
| 6 | <code>python -S out/review_tools.py &#x27;python&#x27; &#x27;out/review_r3.py&#x27; &#x27;a_check&#x27;</code> | RV | 0 | Script A trùng phụ lục; nền đỏ/ứng viên xanh, mutant đúng màu; A1/A7 thật. [Output](review-evidence/20261120T161608462054.txt) |
| 7 | <code>python -S out/review_tools.py &#x27;python&#x27; &#x27;out/review_r2.py&#x27; &#x27;rename&#x27;</code> | RV | 0 | Git/consumer thật: before=P1, kế hoạch registry khác; loại nhanh. [Output](review-evidence/20261120T161612049312.txt) |
| 8 | <code>python -S out/review_tools.py &#x27;python&#x27; &#x27;out/review_r4.py&#x27; &#x27;runtime&#x27;</code> | RV | 0 | Outcome 4×4, process lỗi thật; DAG latency; 480/550 và 368≈370/335. [Output](review-evidence/20261120T161717949100.txt) |
| 9 | <code>python -S out/review_tools.py &#x27;python&#x27; &#x27;out/review_r4.py&#x27; &#x27;pins&#x27;</code> | RV | 0 | YAML r3: B1/B2 15/15 y*, ngoại lệ rộng đỏ; registry/t161/t6 thật. [Output](review-evidence/20261120T161723250163.txt) |
| 10 | <code>python -S out/review_tools.py &#x27;python&#x27; &#x27;out/review_r4.py&#x27; &#x27;provenance&#x27;</code> | RV | 0 | Git thật: đuôi SHA giả và subject không chứng minh parents, S2. [Output](review-evidence/20261120T161834251879.txt) |
| 11 | <code>python -S out/review_tools.py &#x27;python&#x27; &#x27;out/review_r4.py&#x27; &#x27;history&#x27;</code> | RV | 0 | Phản chứng cũ bị chặn; mất artefact lượt đỏ trước 20 tốt vẫn đạt D0, S3. [Output](review-evidence/20261120T161835039041.txt) |
| 12 | <code>python -S out/review_tools.py &#x27;python&#x27; &#x27;out/review_r4.py&#x27; &#x27;contract&#x27;</code> | RV | 0 | Ba trạng thái/hai mode/attempt 1; Q7 và fallback còn S4/S5. [Output](review-evidence/20261120T161836433158.txt) |
| 13 | <code>python -S out/review_tools.py &#x27;rg&#x27; &#x27;:[0-9]+&#x27; &#x27;../SPEC-A-r4.md&#x27; &#x27;../SPEC-B1-r3.md&#x27; &#x27;../SPEC-B2-r3.md&#x27;</code> | REPO | 0 | Đọc/tìm/đối chiếu vật liệu, không sửa nguồn. [Output](review-evidence/20261120T161838479863.txt) |
| 14 | <code>python -S out/review_tools.py &#x27;python&#x27; &#x27;out/review_r3.py&#x27; &#x27;b2_tree_input&#x27;</code> | RV | 1 | Lỗi harness: glob q7-* bắt tệp JSON; đổi tên tệp thử, lượt sau đạt. [Output](review-evidence/20261120T161859550270.txt) |
| 15 | <code>python -S out/review_tools.py &#x27;python&#x27; &#x27;out/review_r3.py&#x27; &#x27;q7_consumer&#x27;</code> | RV | 0 | None thật; predicate B1 loại lỗi, giữ diff rỗng, truyền manh. [Output](review-evidence/20261120T161859882571.txt) |
| 16 | <code>python -S out/review_tools.py &#x27;python&#x27; &#x27;out/review_r2.py&#x27; &#x27;a_write_set&#x27;</code> | RV | 0 | Git thật: đúng hai đường dẫn; thêm tệp thứ ba bị nhận ra. [Output](review-evidence/20261120T161901068094.txt) |
| 17 | <code>python -S out/review_tools.py &#x27;python&#x27; &#x27;out/review_r2.py&#x27; &#x27;f7_closure&#x27;</code> | RV | 0 | Fixture F7 cũ: diff khác, kế hoạch thực bằng nhau. [Output](review-evidence/20261120T161901700073.txt) |
| 18 | <code>python -S out/review_tools.py &#x27;python&#x27; &#x27;out/review_r3.py&#x27; &#x27;b2_tree_input&#x27;</code> | RV | 0 | Git thật: giao diện mới nhận cây, baseline 0; cây/cha sửa 1. [Output](review-evidence/20261120T161916945190.txt) |
| 19 | <code>python -S out/review_tools.py &#x27;read&#x27; &#x27;DE-XUAT-20261116.md@30:95&#x27; &#x27;bang-chung/do-master-20261120.txt&#x27; &#x27;cay-kho/ops/land/pr997-wp978-land-evidence.yaml@40:80&#x27; &#x27;cay-kho/docs/PROTOCOL_DA_PHIEN.md@965:1000&#x27;</code> | RV | 0 | Đọc/tìm/đối chiếu vật liệu, không sửa nguồn. [Output](review-evidence/20261120T162007009764.txt) |
| 20 | <code>python -S out/review_tools.py &#x27;python&#x27; &#x27;out/review_r3.py&#x27; &#x27;provenance&#x27;</code> | RV | 0 | Đối chứng hợp đồng r2 cũ; goi_that thật với opener giả, không mạng/token redirect. [Output](review-evidence/20261120T162008722282.txt) |
| 21 | <code>python -S out/review_tools.py &#x27;python&#x27; &#x27;out/review_r4.py&#x27; &#x27;audit&#x27;</code> | RV | 1 | Lỗi harness giải context citation; sửa bộ đọc trong out, lượt sau đạt. [Output](review-evidence/20261120T162009661433.txt) |
| 22 | <code>python -S out/review_tools.py &#x27;read&#x27; &#x27;cay-kho/.claude/dev/chay-cong-windows_test.ps1@1249:1253&#x27; &#x27;cay-kho/.claude/dev/chay-cong-windows_test.ps1@1311:1315&#x27; &#x27;cay-kho/.claude/dev/chay-cong-windows_test.ps1@1409:1415&#x27;</code> | RV | 0 | Đọc/tìm/đối chiếu vật liệu, không sửa nguồn. [Output](review-evidence/20261120T162026144437.txt) |
| 23 | <code>python -S out/review_tools.py &#x27;python&#x27; &#x27;out/review_r4.py&#x27; &#x27;audit&#x27;</code> | RV | 0 | 60 neo dòng và ngữ cảnh L7; inventory, Q4, 0-cổng, phụ thuộc PyYAML. [Output](review-evidence/20261120T162042052936.txt) |
| 24 | <code>python -S out/review_tools.py &#x27;read&#x27; &#x27;cay-kho/.claude/dev/ci_dang_ky_test.py@1513:1535&#x27; &#x27;cay-kho/.claude/dev/chay-cong-windows_test.ps1@1300:1318&#x27; &#x27;cay-kho/ops/ci_provenance.py@79:96&#x27;</code> | RV | 0 | Đọc/tìm/đối chiếu vật liệu, không sửa nguồn. [Output](review-evidence/20261120T162051339813.txt) |
| 25 | <code>python -S out/review_tools.py &#x27;read&#x27; &#x27;cay-kho/.claude/dev/chay-cong-windows_test.ps1@1190:1285&#x27; &#x27;cay-kho/.claude/dev/chay-cong-windows_test.ps1@1320:1413&#x27;</code> | RV | 0 | Đọc/tìm/đối chiếu vật liệu, không sửa nguồn. [Output](review-evidence/20261120T162101268860.txt) |
| 26 | <code>python -S out/review_tools.py &#x27;rg&#x27; &#x27;^function (Tim-PyYaml&#124;Doc-Utf8&#124;Doc-DichCi&#124;Doc-DauVanCi&#124;Khop-Duoi&#124;Tim-ThieuGuong)&#x27; &#x27;.claude/dev/chay-cong-windows_test.ps1&#x27;</code> | REPO | 0 | Đọc/tìm/đối chiếu vật liệu, không sửa nguồn. [Output](review-evidence/20261120T162112500242.txt) |
| 27 | <code>python -S out/review_tools.py &#x27;read&#x27; &#x27;cay-kho/.claude/dev/chay-cong-windows_test.ps1@1:100&#x27;</code> | RV | 0 | Đọc/tìm/đối chiếu vật liệu, không sửa nguồn. [Output](review-evidence/20261120T162112691873.txt) |
| 28 | <code>python -S out/review_tools.py &#x27;read&#x27; &#x27;cay-kho/.claude/dev/chay-cong-windows_test.ps1@190:225&#x27; &#x27;cay-kho/.claude/dev/chay-cong-windows_test.ps1@250:280&#x27;</code> | RV | 0 | Đọc/tìm/đối chiếu vật liệu, không sửa nguồn. [Output](review-evidence/20261120T162121886584.txt) |
| 29 | <code>python -S out/review_tools.py &#x27;python&#x27; &#x27;out/review_r4.py&#x27; &#x27;windows&#x27;</code> | RV | 0 | Tim-ThieuGuong thật: B1 thiếu fingerprint/gương; sửa cả hai mới đạt, S1. [Output](review-evidence/20261120T162212708316.txt) |
| 30 | <code>python -S out/review_tools.py &#x27;read&#x27; &#x27;VERDICT-luot1.md@1:80&#x27; &#x27;VERDICT-luot2.md@1:100&#x27;</code> | RV | 0 | Đọc/tìm/đối chiếu vật liệu, không sửa nguồn. [Output](review-evidence/20261120T162240820445.txt) |
| 31 | <code>python -S out/review_tools.py &#x27;python&#x27; &#x27;out/review_r4.py&#x27; &#x27;audit&#x27;</code> | RV | 0 | 60 neo dòng và ngữ cảnh L7; inventory, Q4, 0-cổng, phụ thuộc PyYAML. [Output](review-evidence/20261120T162242941036.txt) |
| 32 | <code>python -S out/review_tools.py &#x27;rg&#x27; &#x27;chay-cong-windows_test&#124;chay-cong-windows.ps1&#124;Tim-ThieuGuong&#x27; &#x27;.github/workflows/ci.yml&#x27; &#x27;.claude/dev/ci_dang_ky_test.py&#x27; &#x27;.claude/dev/chay-cong-windows_test.ps1&#x27;</code> | REPO | 0 | Đọc/tìm/đối chiếu vật liệu, không sửa nguồn. [Output](review-evidence/20261120T162244853668.txt) |
| 33 | <code>python -S out/review_tools.py &#x27;git&#x27; &#x27;status&#x27; &#x27;--porcelain&#x27;</code> | REPO | 0 | Trạng thái/neo Git giữ nguyên. [Output](review-evidence/20261120T162308880362.txt) |
| 34 | <code>python -S out/review_tools.py &#x27;git&#x27; &#x27;rev-parse&#x27; &#x27;HEAD&#x27; &#x27;HEAD^{tree}&#x27;</code> | REPO | 0 | Trạng thái/neo Git giữ nguyên. [Output](review-evidence/20261120T162309252313.txt) |
| 35 | <code>python -S out/review_tools.py &#x27;hash&#x27; &#x27;SPEC-A-r4.md&#x27; &#x27;SPEC-B1-r3.md&#x27; &#x27;SPEC-B2-r3.md&#x27;</code> | RV | 0 | Đo SHA-256 các đặc tả. [Output](review-evidence/20261120T162309447100.txt) |
| 36 | <code>python -S out/review_tools.py &#x27;python&#x27; &#x27;out/review_r3.py&#x27; &#x27;contract&#x27;</code> | RV | 0 | Chạy lại mô hình r1/r2 để đối chứng R2/R3/R4; không dùng làm verdict r3. [Output](review-evidence/20261120T162311389560.txt) |
| 37 | <code>python -S out/review_tools.py &#x27;python&#x27; &#x27;out/review_r4.py&#x27; &#x27;contract&#x27;</code> | RV | 0 | Ba trạng thái/hai mode/attempt 1; Q7 và fallback còn S4/S5. [Output](review-evidence/20261120T162352914852.txt) |
| 38 | <code>python -S out/review_tools.py &#x27;python&#x27; &#x27;out/review_r4.py&#x27; &#x27;contract&#x27;</code> | RV | 0 | Ba trạng thái/hai mode/attempt 1; Q7 và fallback còn S4/S5. [Output](review-evidence/20261120T162742308775.txt) |
| Cuối | `python -S out/finalize_review.py` | RV | 0 | Sinh bảng từ nhật ký; kiểm băm, finding, R/F/N, liên kết và kết luận. [Validation](review-evidence/report-validation.json) |
<!-- COMMAND_TABLE_END -->

## Kết luận

**A r4: approve riêng về đặc tả. B1 r3 và B2 r3: changes_requested.** Cần đóng **S1–S5 (5 P2)** trước khi approve bộ ba; **S6–S7 (2 P3)** cũng đã ghi hướng sửa. Không có mã B1/B2 hoặc Actions LIVE trong lượt review này; các phép C5/C6, D0/D4/D5 và M3 tương lai chưa được coi là đạt. Review không cấp quyền trần 550 hay thay bước duyệt của chủ kho.

KET_LUAN: changes_requested
