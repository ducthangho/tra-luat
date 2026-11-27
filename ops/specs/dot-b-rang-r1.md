tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab
dieu_kien_merge: ADR-0060@36d7c5dcdcbbb27176b75135125b9009f9fe0587

# dot-b-rang r1 — chốt danh tính 128 giá trị ASCII (R4-02) và phân hạng 186 đột biến không bị giết của ops/land_evidence_nguon.py (đặc tả đóng băng)

## Định danh

- packet_id: dot-b-rang
- revision: 1
- Packet Issue: #1570. Generation 1. Role `executor` (Claude), reviewer Codex. Review Class `sensitive`: tệp là bộ test của cổng
  land `ops/land_evidence_nguon.py`.
- Căn cứ: chỉ thị chủ kho ngày 27-11-2026 (ghi hộ #1570 issuecomment-7207958642). Nợ gốc: `BO-SINH-BAT-BIEN-R4-chot-dich-doc-lap`
  phần R4-02 (#1539 issuecomment-7198178108; verdict `ops/reviews/bo-sinh-bat-bien-r1-ma-4-codex/VERDICT.md` trên nhánh
  `ops/bo-sinh-bat-bien-lease`, mục `R4-02`) và mục nợ 3 trong thân #1539 (173 `SONG` cộng 13 `VO_CAN` của cặp B ở luật 9).
- Base soạn và base thi công: `origin/master` `26a6e2a0f7addcaa26cb6e01c3ad690dd9ec860f`. `ops/land_evidence_nguon.py` (sha256
  `a104a7d9949aa235b4b9e60eb589aae16a3e0fbcf52f90c7d40d3c94e321f36c`), `ops/land_evidence_nguon_test.py` (sha256
  `63a74f315c6ecaaf591f347255a3226abadec3a602fcfce5b58fa8393fee5e27`) và bộ quét ghim không đổi từ `97ec968` tới base này. Số đo
  dưới đây đo trên `97ec968`, Linux, Python 3.13.18.

## 1. Vấn đề

### 1.1 R4-02

Chốt miền của `c37` (khoảng dòng 914–928 tại base) dựng `vu_tru = [*map(chr, range(128)), ...]` rồi chỉ kiểm category ở
`vu_tru[128:]` và tổng 158 giá trị, 648 ô. Danh tính của 128 phần tử đầu không được kiểm. Reviewer đo: thay thành
`[chr(0x81), *map(chr, range(1, 128)), ...]` (mất U+0000, thêm U+0081) vẫn đủ 158 giá trị khác nhau và 648 ô; `c37`, `c39`, `c40`
đều rc 0. Biến thể mất U+007F (`range(127)` rồi U+0081) cũng lọt `c37`/`c39`. Hậu quả nếu để nguyên: các ô NUL hoặc DEL ở vị trí văn
bản tự do biến mất mà chốt vẫn báo đủ miền.

### 1.2 Đột biến không bị giết của cặp B

Luật 9 trên `97ec968` (bộ quét `ops/reviews/wp1236-r10-soan/quet_dot_bien.py`, sha256
`1b3e4a9e0a4608b9fd6c62e1de99bf509cfd8cb96bedb4d956bac681fc1b9c0c`; cặp `ops/land_evidence_nguon.py` /
`ops/land_evidence_nguon_test.py`; kho hồi quy RỖNG, tệp 0 byte): 624 đột biến, 438 `GIET`, **173 `SONG`**, **13 `VO_CAN`**.
Danh sách 186 ID ở `ops/specs/dot-b-rang-r1.ton-kho.tsv` (sha256 `ff5dab822ffe7bcb33d8ad6db22f17d785553b4430eb3e8d9267eab133a1cde4`;
cột id, hạng, toán tử, dòng, sha256 nguồn đột biến).

Phân bố theo toán tử: `g` 75 (đổi hằng chuỗi), `b` 20, `i5` 12, `j1` 10, `i4` 10, `e` 10, `i1` 8, `a2` 8, `i3` 6, `i6` 4, `i2` 4,
`f` 4, `c2` 4, `i7` 3, `h2` 2, `d` 2, `k2` 1, `k1` 1, `c` 1, `a` 1. Theo hàm hoặc tên mức module (trường thứ hai của ID): `kiem_ho_so` 76, `RE_MOC` 26, `main` 17, `merged_at` 15, `RE_SO_POS` 11, `_thoi_diem` 7, `duyet` 5, `token_nguon` 4, `nap_yaml` 4, `map_khong_trung` 3, `RE_KHAI_DO` 3, `phan_giai` 2, `_trong_goc` 2, `_la_nguon` 2, `_chuan_hoa_81` 2, `RE_KHAI_KHONG_DO` 2, `RE_DUOI_NGUON` 2, `_khai_tuy_chon` 1, `L7_MUC_DAT` 1, `L7_KHOA_TUY_CHON` 1. Executor đếm lại từ tệp tồn kho; con số trong đặc tả chỉ để định hướng.

## 2. Hành vi bắt buộc

1. **R4-02.** Chốt miền của `c37` đòi DANH TÍNH của phần ASCII: tập 128 phần tử đầu của `vu_tru` bằng đúng
   `{chr(i) for i in range(128)}`, so với một hằng hoặc biểu thức dựng độc lập với chính `vu_tru`. Danh tính phần ngoài ASCII
   giữ chốt category hiện có.
2. **Đột biến không bị giết.** Mỗi ID trong `ops/specs/dot-b-rang-r1.ton-kho.tsv` phải kết thúc ở đúng MỘT trong ba trạng thái:
   - `GIET` khi chạy lại luật 9 trên head: một ca của `ops/land_evidence_nguon_test.py` đỏ ĐÚNG LÝ DO (bộ quét phân hạng `GIET`).
     Với ID ở hạng `VO_CAN` tại base, đây là đích mặc định: ca phải chết bằng tín hiệu chốt của ca, không bằng ngoại lệ vô can.
   - `TUONG_DUONG`: không đầu vào nào phân biệt được hành vi quan sát được của module (giá trị trả về, ngoại lệ, stdout, stderr,
     rc) giữa bản gốc và bản đột biến. Handoff ghi lập luận theo từng ID, kèm phép thử chạy được nếu có. Ví dụ: `x is None` →
     `x == None` chỉ tương đương khi mọi kiểu thực của `x` tại vị trí ấy không ghi đè `__eq__`; phải nêu tập kiểu ấy.
   - `NGOAI_HOP_DONG`: CHỈ cho đột biến làm đổi văn bản tự do của một dòng chẩn đoán (thường là `g`, đôi khi `i*` trên chuỗi
     định dạng), khi phần bị đổi không thuộc hợp đồng đầu ra mà bất kỳ consumer nào dựa vào. Handoff phải ghi cho ID ấy: (a) dòng
     ra bị đổi trước và sau; (b) danh sách consumer của đầu ra module trong kho, liệt kê bằng phép tìm toàn kho có ghi lệnh
     (tối thiểu xét `ops/gate_output_doi_chieu.py`, `ops/ci_duong_nhanh.py`, `.claude/dev/ci_dang_ky_test.py`, `.github/workflows/`,
     `docs/PROTOCOL_DA_PHIEN.md`); (c) với từng consumer, vì sao nó không đọc phần bị đổi. Phần đầu dòng mang nhãn luật (`L1`…`L8`,
     `ĐẠT`, `ĐỎ`, `KHÔNG ĐO ĐƯỢC`, `MIỄN TRỪ`, `TỔNG:`), mã thoát và các trường có cấu trúc (đường dẫn, khoá YAML, số đếm) LUÔN thuộc
     hợp đồng: đột biến chạm chúng không được xếp `NGOAI_HOP_DONG`.
   Không có trạng thái thứ tư. "Khó giết" không phải lý do. Nếu một đột biến cho thấy module SAI (hành vi đột biến mới đúng đặc
   tả gốc), executor ghi nó thành phát hiện trong handoff, KHÔNG sửa module (ngoài write set), và xếp ID ấy vào mục chờ quyết định.
3. Không đột biến nào đang `GIET` ở base chuyển sang hạng khác ở head (luật 9, cặp B).
4. Ca mới bám nhãn và trường có cấu trúc của đầu ra, không bám nguyên văn câu chẩn đoán, trừ khi đặc tả gốc của luật quy định
   nguyên văn. Mục đích: không biến văn bản tự do thành hợp đồng chỉ để giết đột biến `g`.

## 3. Phản chứng bắt buộc (là ca trong bộ test)

`DOT_BIEN` của bộ test đột biến MODULE, nên răng của chốt R4-02 đo bằng CA. Mỗi phản chứng phải đỏ bằng tín hiệu chốt của đúng
ca đích (rc 3 kèm `DO:<tên ca>:`), không phải lỗi vô can (rc 4); bản nguyên vẹn phải xanh; phép sửa chỉ trong bộ nhớ, neo văn bản
xuất hiện đúng một lần.

| # | Phản chứng | Ca phải đỏ |
|---|---|---|
| P1 | Thay U+0000 bằng U+0081 trong phần ASCII của `vu_tru` (giữ 158 giá trị, 648 ô) | `c37` |
| P2 | Thay U+007F bằng U+0081 (`range(127)` rồi U+0081) | `c37` |
| P3 | Thay một ký tự ASCII giữa khoảng (ví dụ U+0041) bằng một ký tự ngoài ASCII chưa có trong `vu_tru` | `c37` |
| P4 | Bản sao nguyên vẹn đi cùng đường | xanh |

Phản chứng có sẵn của `c36`, `c37`, `c39`, `c40` giữ nguyên hành vi.

## 4. Không đổi

- Không sửa `ops/land_evidence_nguon.py` hay tệp nào ngoài write set.
- Tên các ca hiện có giữ nguyên. Hợp đồng đầu ra bốn dòng (`CA: N/N dat` · `DOT BIEN: M/M bi giet dung ly do` ·
  `TU KIEM PHAN HANG: DAT` · `TONG: DAT`) giữ nguyên; consumer `MOI` trong `.claude/dev/ci_dang_ky_test.py`.
- Thời gian: đo bộ test trên base và head trong cùng một lệnh, cùng máy, Linux, ba cặp xen kẽ thứ tự, công bố mọi mẫu. Chấp
  nhận khi trung vị delta ≤ 60 giây và không mẫu nào vượt 120 giây so mẫu base cùng cặp.

## 5. Nghiệm thu

Đo trên đúng SHA ứng viên, clone đầy đủ (không nông), `core.abbrev 7`. Phép so với base dựng hai vế trong cùng một lệnh.

1. `python3 -B ops/land_evidence_nguon_test.py`: rc 0, đủ bốn dòng hợp đồng với hai số bằng nhau.
2. `python3 -B ops/gate_output_doi_chieu_test.py`: rc 0, đủ bốn dòng (bộ này import module cặp B).
3. `python3 -B ops/land_evidence_nguon.py --root .`: `TỔNG: ĐẠT`.
4. `python scripts/tl.py --selftest`: N/N hai số bằng nhau.
5. `python3 -m ruff check --select F ops/land_evidence_nguon_test.py`: delta so base bằng 0.
6. `git diff --check` rc 0; `git diff --numstat <base>...<head>` chỉ tệp write set, trong trần §7.
7. Luật 9 cặp B trên base và head, cùng bộ quét ghim, cùng kho rỗng: 0 `GIET` → hạng khác; mỗi ID của tồn kho §1.2 là `GIET` trên
   head hoặc có mục `TUONG_DUONG` / `NGOAI_HOP_DONG` trong bảng handoff. Luật 9 cặp A KHÔNG chạy ở packet này.
8. Handoff kèm bảng nghĩa vụ → mệnh đề/ca → phản chứng, và bảng 186 ID: hạng ở base, hạng ở head, ca giết hoặc lập luận. Kèm
   một dòng tổng: số `GIET`, `TUONG_DUONG`, `NGOAI_HOP_DONG`, chờ quyết định, cộng lại đúng 186.

## 6. Review theo lớp, CI, Windows, thẩm quyền

- Review mã: Codex offline qua `launcher.py run` do phiên điều phối gọi, theo §8.3 và ADR-0060 M2: mỗi finding một slug lớp,
  quét mọi biểu hiện cùng lớp trước khi báo, bảng lớp có slug, biểu hiện, mức cao nhất, cách vá chung, phép đóng. Executor vá
  theo LỚP: liệt kê hết đường vào của lớp trước khi vá, mỗi đường một ca và một phản chứng riêng.
- Lớp đã biết và slug dự kiến: `nghiem-thu-khong-co-lap-chot-dich` (lịch sử #1539); `dot-bien-song-chua-phan-hang`;
  `phan-hang-ngoai-hop-dong-khong-du-bang-chung` (xếp `NGOAI_HOP_DONG` thiếu danh sách consumer hoặc chạm phần thuộc hợp đồng).
- Reviewer được kiểm mẫu: chọn ngẫu nhiên các ID `TUONG_DUONG` và `NGOAI_HOP_DONG`, tự tìm đầu vào phân biệt hoặc consumer bị bỏ sót.
- Trần packet: tối đa 4 lời gọi Codex review (dưới trần ADR-0055). Chạm trần mà chưa approve ⇒ dừng, hỏi chủ kho E2.
- Push và PR theo ADR-0060 M5/M12: executor commit tại chỗ, bàn giao bundle, chỉ push khi điều phối báo review offline approve
  đúng SHA; PR mở draft; connector gọi khi còn draft (M6).
- M3 Windows: reviewer phân loại theo diff thật (ADR-0060 M3 bước 2). Nếu `required`, phiên điều phối chạy Windows local
  TẬP TRUNG (chỉ bước 1–3 của §5) trên base và head.
- M9: diff chạm `ops/**/*.py` ⇒ cần `ci-dot-bien-du.yml` trên đúng head; phiên điều phối gọi.
- Phạm vi E: chỉ sửa tệp test; E1–E5 đều `khong`. Audit trước merge: audit uỷ quyền ADR-0067 (`delegated_audited`). Merge cần
  lần duyệt M7 của chủ kho neo đúng SHA. ID ở mục chờ quyết định (§2.2) cần chủ kho quyết trước merge.

## 7. Write set (không glob) và trần

- `ops/land_evidence_nguon_test.py`

Trần: 1 tệp, không quá 420 dòng thêm theo `git diff --numstat <base>...<head>` (dưới trần sensitive ADR-0053). Vượt thì dừng
trước review, báo E2. Đụng tệp ngoài write set thì dừng, ghi vào handoff.

## 8. Chưa đo được và ngoài phạm vi

- Hành vi trên Windows của ca mới: chưa đo khi soạn.
- Đột biến ngoài tập toán tử của bộ quét ghim: không thuộc nghĩa vụ §2.2.
- Cặp A (`ops/gate_output_doi_chieu.py`): packet #1569.
- Cổng land không kiểm `SHA256SUMS`: #1473.
