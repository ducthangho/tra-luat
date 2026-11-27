tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab
dieu_kien_merge: ADR-0060@36d7c5dcdcbbb27176b75135125b9009f9fe0587

# dot-a-rang r1 — chốt danh tính năm bộ đối số độc lập (R4-01) và diệt 23 đột biến SONG của ops/gate_output_doi_chieu.py (đặc tả đóng băng)

## Định danh

- packet_id: dot-a-rang
- revision: 1
- Packet Issue: #1569. Generation 1. Role `executor` (Claude), reviewer Codex. Review Class `sensitive`: tệp là bộ test
  của module cổng land đợt A.
- Căn cứ: chỉ thị chủ kho ngày 27-11-2026 (ghi hộ #1569 issuecomment-7207957215). Nợ gốc: `BO-SINH-BAT-BIEN-R4-chot-dich-doc-lap`
  phần R4-01 (#1539 issuecomment-7198178108; verdict `ops/reviews/bo-sinh-bat-bien-r1-ma-4-codex/VERDICT.md` trên nhánh
  `ops/bo-sinh-bat-bien-lease`) và 23 đột biến `SONG` có sẵn của cặp A ghi ở #1539.
- Base soạn và base thi công: `origin/master` `26a6e2a0f7addcaa26cb6e01c3ad690dd9ec860f`. `ops/gate_output_doi_chieu.py`,
  `ops/gate_output_doi_chieu_test.py` và bộ quét ghim không đổi từ `e209579` tới base này. Số đo dưới đây đo trên `97ec968`
  (cùng nội dung hai tệp), Linux, Python 3.13.18.

## 1. Vấn đề

### 1.1 R4-01

`kiem_bo_sinh` của `ops/gate_output_doi_chieu_test.py` so ba nguồn danh tính của năm bộ đối số `(cam, bo_loai)`: tập đọc bằng
AST từ các lời gọi `_mau_loai_unicode(...)` trong các ca `aNNN_`, hằng `BO_SINH_MONG`, và tập lời gọi thực. Cả ba đều lấy
danh tính từ mã của chính tệp test, nên một đột biến đổi ĐỒNG THỜI lời gọi trong ca và hằng `BO_SINH_MONG` (reviewer đo:
`"\r\n"` → `"\r"` ở bộ 5) làm mất một bộ bắt buộc mà `a135`/`a136` vẫn xanh. Reviewer quét cùng lệch ở cả năm bộ: bộ 1, 2 bị
bắt; bộ 3, 4, 5 lọt.

Năm bộ đối số bắt buộc (nguyên văn từ §1 của đặc tả `bo-sinh-bat-bien` r1, blob `a47f5bfb` tại `d22fe11`):

| # | `cam` | `bo_loai` | số phần tử | category vắng |
|---|---|---|---:|---|
| 1 | `"—"` | rỗng | 31 | không |
| 2 | `""` | `Cs` | 30 | `Cs` |
| 3 | `"\n\r\v\f\x1c\x1d\x1e\x85" + chr(0x2028) + chr(0x2029) + " \t"` | rỗng | 29 | `Zl`, `Zp` |
| 4 | `""` | rỗng | 31 | không |
| 5 | `"\r\n"` | `Cs` | 30 | `Cs` |

Chuỗi `cam` của bộ 3 viết theo cú pháp biểu thức Python, đúng như `BO_SINH_MONG[2][0]` tại base: tám ký tự điều khiển, U+2028 (ký tự duy nhất của `Zl`), U+2029 (ký tự duy nhất của `Zp`), một dấu cách U+0020 và một tab. Lời gọi trong ca `a126_mien_ascii_qua_ho_so` (dòng 1039 tại base) viết hai ký tự ấy bằng `\u2028\u2029`. Bộ 5 được gọi với `bo_loai` là tập `{"Cs"}` (`a129_ten_job_lazy_qua_ho_so`, dòng 1266), `BO_SINH_MONG` ghi tuple `("Cs",)`; so danh tính theo TẬP. Executor xác nhận lại từng ký tự (`repr`) bằng cách đọc chính tệp test tại base trước khi chép thành hằng, và viết hằng bằng `chr(...)` hoặc chuỗi thoát ASCII, không chép ký tự U+2028/U+2029 nguyên văn vào mã.

### 1.2 Đột biến SONG của cặp A

Luật 9 trên `97ec968` (bộ quét `ops/reviews/wp1236-r10-soan/quet_dot_bien.py`, sha256
`1b3e4a9e0a4608b9fd6c62e1de99bf509cfd8cb96bedb4d956bac681fc1b9c0c`; cặp `ops/gate_output_doi_chieu.py` /
`ops/gate_output_doi_chieu_test.py`; kho hồi quy `ops/specs/dot-a-rang-r1.kho-A.jsonl`, sha256
`191225cac93a5bec155cc9116911022b334df5d7b6f0bf6094632973b82af740`): 946 đột biến, 923 `GIET`, **23 `SONG`**, 0 `VO_CAN`.
Danh sách 23 ID ở `ops/specs/dot-a-rang-r1.ton-kho.tsv` (sha256 `25d523208b7abc21f710833b4cd0551b49e45e2965cf0301a25964c61580e6a2`):
8 `j1` (`is` → `==`), 3 `h2` (thêm phần tử vào tập), 1 mỗi `e`, `i4`, `i7`, `k3`, và 8 ID lấy từ kho hồi quy.

## 2. Hành vi bắt buộc

1. **R4-01.** Thêm vào test một hằng ghi năm bộ đối số của bảng §1.1, chép từ đặc tả này, không dựng từ AST, từ
   `BO_SINH_MONG` hay từ lời gọi thực. `kiem_bo_sinh` (hoặc ca mới) đòi CẢ BA nguồn hiện có bằng ĐÚNG hằng ấy: bằng tập, đúng
   năm phần tử, không thừa không thiếu. Lệch ở bất kỳ nguồn nào ⇒ ca đích đỏ.
2. **Đột biến SONG.** Mỗi ID trong `ops/specs/dot-a-rang-r1.ton-kho.tsv` phải kết thúc ở đúng MỘT trong hai trạng thái:
   - `GIET` khi chạy lại luật 9 trên head: một ca của `ops/gate_output_doi_chieu_test.py` đỏ đúng lý do (bộ quét phân hạng
     `GIET`); hoặc
   - `TUONG_DUONG`: handoff ghi cho ID ấy một lập luận vì sao không đầu vào nào phân biệt được hành vi quan sát được của
     module (giá trị trả về, ngoại lệ, stdout, stderr, rc) giữa bản gốc và bản đột biến, kèm phép thử chạy được nếu có.
     Ví dụ hợp lệ tiềm năng: `x is None` → `x == None` khi `x` chỉ có thể là kiểu không ghi đè `__eq__`; executor phải nêu
     tập kiểu thực của `x` tại vị trí ấy.
   Không có trạng thái thứ ba. "Khó giết" không phải lý do.
3. Không đột biến nào đang `GIET` ở base chuyển sang hạng khác ở head (luật 9, cặp A).

## 3. Phản chứng bắt buộc (là ca trong bộ test)

`DOT_BIEN` của bộ test đột biến MODULE, không đột biến tệp test, nên răng của chốt R4-01 đo bằng CA. Mỗi phản chứng phải đỏ
bằng tín hiệu chốt của đúng ca đích (rc 3 kèm `DO:<tên ca>:`), không phải lỗi vô can (rc 4); bản nguyên vẹn phải xanh; phép
sửa chỉ trong bộ nhớ, neo văn bản xuất hiện đúng một lần.

| # | Phản chứng | Ca phải đỏ |
|---|---|---|
| Q1 | Đổi đồng thời lời gọi trong ca và `BO_SINH_MONG` ở từng bộ 1..5 (mỗi bộ một biến thể; giữ năm phần tử, chỉ đổi danh tính) | ca đích của §2.1 |
| Q2 | Bỏ một bộ ở cả hai nơi; thêm một bộ thứ sáu ở cả hai nơi | ca đích của §2.1 |
| Q3 | Bản sao nguyên vẹn đi cùng đường | xanh |

Các phản chứng có sẵn của `a136` (năm bộ sinh giả sai tại từng bộ, bỏ/lặp/thay một bộ của `BO_SINH_MONG`, AST không đọc
được ⇒ đỏ) giữ nguyên hành vi.

## 4. Không đổi

- Không sửa `ops/gate_output_doi_chieu.py` hay tệp nào ngoài write set.
- Tên các ca hiện có giữ nguyên. Hợp đồng đầu ra bốn dòng (`CA: N/N dat` · `DOT BIEN: M/M bi giet dung ly do` ·
  `TU KIEM PHAN HANG: DAT` · `TONG: DAT`) giữ nguyên; consumer `MOI` trong `.claude/dev/ci_dang_ky_test.py`.
- Thời gian: bộ test không chậm hơn base quá 20 giây. Đo hai vế trong cùng một lệnh, cùng máy, Linux, ba cặp xen kẽ thứ tự,
  công bố mọi mẫu; đặc tả chấp nhận khi trung vị delta ≤ 20 giây và không mẫu nào vượt 40 giây.

## 5. Nghiệm thu

Đo trên đúng SHA ứng viên, clone đầy đủ (không nông), `core.abbrev 7`. Phép so với base dựng hai vế trong cùng một lệnh.

1. `python3 -B ops/gate_output_doi_chieu_test.py`: rc 0, đủ bốn dòng hợp đồng với hai số bằng nhau.
2. `python3 -B ops/land_evidence_nguon_test.py`: rc 0, đủ bốn dòng (bộ này tái dùng bộ sinh của tệp đợt A).
3. `python3 -B ops/land_evidence_nguon.py --root .`: `TỔNG: ĐẠT`.
4. `python scripts/tl.py --selftest`: N/N hai số bằng nhau.
5. `python3 -m ruff check --select F ops/gate_output_doi_chieu_test.py`: delta so base bằng 0.
6. `git diff --check` rc 0; `git diff --numstat <base>...<head>` chỉ tệp write set, trong trần §7.
7. Luật 9 cặp A trên base và head, cùng bộ quét ghim và cùng kho `ops/specs/dot-a-rang-r1.kho-A.jsonl`: 0 `GIET` → hạng khác;
   mỗi ID của tồn kho §1.2 là `GIET` trên head hoặc có mục `TUONG_DUONG` trong bảng handoff. Luật 9 cặp B (module
   `ops/land_evidence_nguon.py`, tệp test của nó) KHÔNG chạy ở packet này: write set không chạm cặp B.
8. Handoff kèm bảng nghĩa vụ → mệnh đề/ca → phản chứng, và bảng 23 ID: hạng ở base, hạng ở head, ca giết hoặc lập luận.

## 6. Review theo lớp, CI, Windows, thẩm quyền

- Review mã: Codex offline qua `launcher.py run` do phiên điều phối gọi, theo §8.3 và ADR-0060 M2: mỗi finding một slug lớp,
  quét mọi biểu hiện cùng lớp trước khi báo, bảng lớp có slug, biểu hiện, mức cao nhất, cách vá chung, phép đóng. Executor vá
  theo LỚP: liệt kê hết đường vào của lớp trước khi vá, mỗi đường một ca và một phản chứng riêng.
- Lớp đã biết và slug dự kiến: `nghiem-thu-khong-co-lap-chot-dich` (chốt thiếu phản chứng cô lập, lịch sử #1539);
  `dot-bien-song-chua-phan-hang` (đột biến SONG chưa có ca giết hay lập luận tương đương).
- Trần packet: tối đa 4 lời gọi Codex review (dưới trần ADR-0055). Chạm trần mà chưa approve ⇒ dừng, hỏi chủ kho E2.
- Push và PR theo ADR-0060 M5/M12: executor commit tại chỗ, bàn giao bundle, chỉ push khi điều phối báo review offline approve
  đúng SHA; PR mở draft; connector gọi khi còn draft (M6).
- M3 Windows: reviewer phân loại theo diff thật (ADR-0060 M3 bước 2). Nếu `required`, phiên điều phối chạy Windows local
  TẬP TRUNG (chỉ bước 1–3 của §5) trên base và head.
- M9: diff chạm `ops/**/*.py` ⇒ cần `ci-dot-bien-du.yml` trên đúng head; phiên điều phối gọi.
- Phạm vi E: chỉ sửa tệp test; E1–E5 đều `khong`. Audit trước merge: audit uỷ quyền ADR-0067 (`delegated_audited`). Merge cần
  lần duyệt M7 của chủ kho neo đúng SHA.

## 7. Write set (không glob) và trần

- `ops/gate_output_doi_chieu_test.py`

Trần: 1 tệp, không quá 200 dòng thêm theo `git diff --numstat <base>...<head>`. Vượt thì dừng trước review, báo E2. Đụng tệp
ngoài write set thì dừng, ghi vào handoff.

## 8. Chưa đo được và ngoài phạm vi

- Hành vi trên Windows của ca mới: chưa đo khi soạn.
- Đột biến ngoài tập toán tử của bộ quét ghim: không thuộc nghĩa vụ §2.2.
- Ngoài phạm vi, có Issue riêng: #1552 (module đợt A trên Windows), #1257.
