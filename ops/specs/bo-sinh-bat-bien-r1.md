tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# bo-sinh-bat-bien r1 — chốt miền của bộ sinh ký tự và ô cấu trúc mà test đợt B tái dùng từ test đợt A (đặc tả đóng băng)

## Định danh

- packet_id: bo-sinh-bat-bien
- revision: 1
- Packet Issue: #1539. Generation 1. Role `executor` (Claude), reviewer Codex. Review Class `sensitive`: hai tệp là bộ test của cổng land.
- Căn cứ: chủ kho giao ngày 25-11-2026 (Issue #1539, mục *Nguồn cấp việc*). Nợ gốc: `WP1236-B02-bat-bien-bo-sinh-test-dot-A`,
  finding B02 mức P3 lớp `nghiem-thu-khong-co-lap-chot-dich` của review mã wp1236 đợt B lượt 4
  (`ops/reviews/wp1236-b-r12-ma-4-codex/VERDICT.md` và `VERDICT.json` trên nhánh `ops/wp1236-bc-lease`), chủ kho miễn ở
  #1236 issuecomment-7156364013.
- Base soạn và base thi công: `origin/master` `a89c83acf998008caecba9084a7d295845bf1976`. Mọi số đo dưới đây đo trên base này,
  Linux, Python 3.13.18, Unicode data 15.1.0, ngày 25-11-2026.

## 1. Vấn đề

`c36` và `c37` của `ops/land_evidence_nguon_test.py` tái dùng bộ sinh của `ops/gate_output_doi_chieu_test.py`: hàm
`_mau_loai_unicode` và tám ca `a124`, `a125`, `a126`, `a129`, `a131`, `a132`, `a133`, `a134`. Chốt hiện có là sàn đếm
(`A_CA`) và `len(vu_tru) >= 150`; biểu thức `4 * len(vu_tru) + 16` của `c37` co theo chính bộ sinh. Reviewer đo trên bản sao:

- `_mau_loai_unicode` không xuất đại diện category `Mn`: `c36` 8396 → 8343 phần tử, `c37` 648 → 644 ô, cả bộ test đợt B vẫn rc 0.
- Bỏ một lời gọi `kiem(...)` của `a129`: 36 → 35 phần tử (sàn 30), `c36` và `c38` vẫn rc 0.

Số đo nền của bộ sinh (đo lại khi soạn): tập general category là 30 tên
`Lu Ll Lt Lm Lo Mn Mc Me Nd Nl No Pc Pd Ps Pe Pi Pf Po Sm Sc Sk So Zs Zl Zp Cc Cf Cs Co Cn`. Năm bộ đối số mà test đợt A gọi:

| đối số `cam` | `bo_loai` | số phần tử trả về | category vắng |
|---|---|---:|---|
| `"—"` | rỗng | 31 | không |
| `""` | `Cs` | 30 | `Cs` |
| `"\n\r\v\f\x1c\x1d\x1e\x85   \t"` | rỗng | 29 | `Zl`, `Zp` |
| `""` | rỗng | 31 | không |
| `"\r\n"` | `Cs` | 30 | `Cs` |

Mỗi lần trả về: không category nào lặp, phần tử cuối là `U+10400` (ngoài BMP), không phần tử nào khác ngoài BMP.
Số phần tử qua `main` → L8 của tám ca: 1733, 3840, 52, 36, 1, 1280, 1136, 318; tổng 8396. `c37` chạy 648 ô.

## 2. Hành vi bắt buộc

Kỳ vọng ở mọi mục dưới đây viết thành HẰNG trong tệp test, lấy từ đặc tả này. Không được tính kỳ vọng bằng cách gọi chính
bộ sinh đang bị kiểm.

### 2.1 Test đợt B: `c37`

1. Vũ trụ ký tự của `c37` phải đúng 158 ký tự đôi một khác nhau: 128 ký tự ASCII, mỗi category trong 30 tên trừ `Cs` đúng
   một đại diện (29), và đúng một ký tự ngoài BMP. Không ký tự nào thuộc `"\r\n"` ở phần ngoài ASCII.
2. Số ô của `c37` là hằng 648, không tính từ `len(vu_tru)`.
3. Hai chốt trên chạy TRƯỚC vòng 648 ô. Vũ trụ sai thì `c37` đỏ ngay, không chạy ô nào.

### 2.2 Test đợt B: `c36`

1. Với từng ca trong tám ca, số phần tử qua `main` → L8 phải BẰNG ĐÚNG kỳ vọng. Kỳ vọng là một biểu thức gồm số ô cấu trúc
   của ca (hằng nguyên, có chú thích nguồn trong test đợt A) và kích thước miền ký tự của từng lời gọi bộ sinh trong ca
   (lấy từ hằng miền của test đợt B). Tám biểu thức phải ra đúng tám số ở mục 1. Sàn `A_CA` bị thay, không giữ song song.
2. Với từng ca có dùng bộ sinh, tập general category của các ký tự ngoài ASCII trong những phần tử ĐÃ đi qua L8 phải chứa
   tập bắt buộc của ca, và phải có ít nhất một ký tự ngoài BMP. Một phần tử gồm hồ sơ và mọi tệp của thư mục provenance
   được đưa qua cùng nó. Tập bắt buộc của ca là hằng: 30 tên trừ những category mà lời gọi của ca loại, mỗi loại trừ có
   chú thích lý do.
3. `c38` (bỏ, đổi tên, nhân đôi một ca bắt buộc) giữ nguyên hành vi: 24/24 biến thể làm `c36` đỏ đúng chốt.

### 2.3 Test đợt A

1. Thêm một ca mới (tên không bắt đầu bằng tiền tố nào của tám ca trên) kiểm `_mau_loai_unicode` với đúng năm bộ đối số ở
   bảng mục 1: số phần tử, tập category vắng, không lặp category, không phần tử nào thuộc `cam`, mọi đại diện từ `U+0080`
   trở lên, phần tử cuối ngoài BMP và là phần tử ngoài BMP duy nhất.
2. Phép kiểm ấy là một hàm nhận bộ sinh làm tham số, để phản chứng ở mục 3 gọi nó với bộ sinh giả.

## 3. Phản chứng bắt buộc

`DOT_BIEN` của hai bộ test đột biến MODULE sản phẩm, không đột biến tệp test. Vì vậy răng của các chốt mới được đo bằng CA,
theo cách `c38` đang làm. Mỗi phản chứng phải đỏ bằng tín hiệu chốt của đúng ca đích (rc 3 kèm dấu `DO:<tên ca>:`), không
phải lỗi vô can (rc 4), và bản nguyên vẹn phải xanh. Bộ sinh hay ca bị sửa chỉ tồn tại trong bộ nhớ; không ghi vào tệp
nào của kho. Phép sửa theo neo văn bản phải đòi neo xuất hiện đúng một lần, sai thì ca đỏ.

| # | Phản chứng | Ca phải đỏ |
|---|---|---|
| P1 | Bộ sinh bỏ một category, lần lượt cho CẢ 29 category của vũ trụ `c37` | `c37`, thông báo nêu tên category |
| P2 | Bộ sinh bỏ ký tự ngoài BMP | `c37` |
| P3 | Bộ sinh trả thừa một phần tử, hoặc lặp một category | `c37` |
| P4 | Bộ sinh bỏ `Mn`, chạy thật qua `main` → L8 trên ít nhất ca `a129` | `c36` |
| P5 | `a129` mất một lời gọi `kiem(...)` cấu trúc, chạy thật qua `main` → L8 | `c36` |
| P6 | Bộ sinh đổi đại diện của một category thành bản sao đại diện của category khác (số phần tử không đổi) | `c36` hoặc `c37` |
| P7 | Ở test đợt A: bộ sinh giả bỏ một category, bỏ ký tự ngoài BMP, bỏ lọc `cam`, bỏ lọc `bo_loai` (bốn biến thể) | ca mới của mục 2.3 |

P4 và P5 được phép chạy trên tập con ca (ví dụ chỉ `a129`) để rẻ. Bảng đầy đủ tám ca chỉ chạy một lần, ở `c36`.

## 4. Không đổi

- Không sửa `ops/land_evidence_nguon.py` và `ops/gate_output_doi_chieu.py`. Luật 9 của wp1236 vì thế không có đột biến mới
  của module; yêu cầu còn lại là không hồi quy (mục 5).
- Tên các ca hiện có giữ nguyên. Hợp đồng đầu ra bốn dòng của hai bộ test (`CA: N/N dat` · `DOT BIEN: M/M bi giet dung ly do` ·
  `TU KIEM PHAN HANG: DAT` · `TONG: DAT`) giữ nguyên; consumer là `MOI` trong `.claude/dev/ci_dang_ky_test.py`.
- Thời gian: bộ test đợt B không chậm hơn base quá 30 giây, bộ test đợt A không chậm hơn base quá 5 giây. Đo hai vế trong
  cùng một lệnh, cùng máy, Linux.

## 5. Nghiệm thu

Đo trên đúng SHA ứng viên, clone sạch, `core.abbrev 7`. Phép so với base dựng hai vế trong cùng một lệnh.

1. `python3 -B ops/land_evidence_nguon_test.py`: rc 0, đủ bốn dòng hợp đồng với hai số bằng nhau.
2. `python3 -B ops/gate_output_doi_chieu_test.py`: như trên.
3. `python3 -B ops/land_evidence_nguon.py --root .`: rc 0, `TỔNG: ĐẠT`.
4. `python3 -B .claude/dev/ci_dang_ky_test.py`: rc 0.
5. `python scripts/tl.py --selftest`: N/N.
6. `python3 -m ruff check --select F` trên hai tệp: delta so base bằng 0.
7. `git diff --check` rc 0. `git diff --numstat <base>...<head>`: chỉ hai tệp của write set, trong trần ở mục 7.
8. Luật 9, bộ quét ghim `ops/reviews/wp1236-r10-soan/quet_dot_bien.py do`, chạy cho cả hai cặp module/test trên base và trên
   head: không đột biến nào đổi từ `GIET` ở base sang hạng khác ở head. Số `SONG` và `VO_CAN` có sẵn ở base là nợ ngoài
   phạm vi, khai nguyên con số.
9. Bảy phản chứng ở mục 3 là ca trong bộ test, nên đã nằm trong số ca của bước 1 và 2. Handoff kèm bảng: phản chứng → tên ca
   → dòng `DO:` quan sát được.

## 6. Review, CI, Windows, thẩm quyền

- Review mã: Codex offline qua `launcher.py run`, do phiên điều phối gọi, theo §8.3 (bảng lớp). Packet này tự đặt trần 4 lời
  gọi; chạm trần mà chưa approve thì dừng, hỏi chủ kho mã E2.
- Push và PR theo ADR-0060 M5/M12: executor commit tại chỗ, bàn giao bundle, chỉ push khi điều phối báo review offline
  approve đúng SHA.
- M3 Windows: reviewer phân loại theo diff thật. Nếu `required`, phiên điều phối chạy Windows local trên base và head.
- M9: diff chạm `ops/**/*.py`, nên cần lượt `ci-dot-bien-du.yml` trên head; phiên điều phối gọi.
- Phạm vi E: packet chỉ sửa tệp test, không đổi điều kiện để một hồ sơ được tính là land, không chạm mã cổng lease hay cổng
  merge. Khai E1–E5 đều `khong`. Audit trước merge là audit uỷ quyền theo ADR-0067 (mức `delegated_audited`). Reviewer hay
  phiên audit thấy diff chạm E4 hoặc E5 thì dừng và hỏi chủ kho.

## 7. Write set (không glob) và trần

- `ops/land_evidence_nguon_test.py`
- `ops/gate_output_doi_chieu_test.py`

Trần: 2 tệp, không quá 320 dòng thêm theo `git diff --numstat <base>...<head>`. Vượt thì dừng trước review, báo mã E2.
Đụng tệp ngoài hai tệp trên thì dừng, ghi vào handoff.

## 8. Chưa đo được và ngoài phạm vi

- Thời gian và hành vi trên Windows của các ca mới: chưa đo khi soạn.
- Một ô cấu trúc bị THAY bằng ô khác cùng số lượng và cùng tập category: các chốt đếm và chốt category không thấy được.
- Ngoài phạm vi, đã ghi ở Issue #1539: 173 đột biến `SONG` và 13 `VO_CAN` của mã L1–L7 có sẵn; cổng land không đối chiếu
  `SHA256SUMS`; ba ca `ops/ci_duong_nhanh_test.py` đỏ sẵn trên Windows; fixture `wp433_gws_cred_no` trên Windows.
