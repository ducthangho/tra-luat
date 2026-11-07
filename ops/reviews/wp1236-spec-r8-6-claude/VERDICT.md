Kết luận vòng 6: **changes_requested**. Còn hai P2 và hai P3. Cả hai P2 đều không chặn thi công: executor viết đúng văn bản thì qua mọi ca. Vấn đề là A14-S0 chưa khoá được thứ mà đặc tả nói là đã khoá, đúng lớp lỗi mà quyết định (a′) chọn đóng.

**Câu hỏi chính: còn đường để module qua A14-S0 và mọi ca hành vi mà vẫn nhận khác tham chiếu không? Còn, hai đường.**
- **Ở hàm (M01).** Vế (4) dùng `inspect.getsource(f)`. Hàm này lần theo `__wrapped__`, tin `co_firstlineno` và đọc qua `linecache`. Vì vậy câu "NGUỒN CỦA CHÍNH ĐỐI TƯỢNG gắn với tên" sai. Bốn biến thể qua cả năm vế:
  - W1: bọc bằng `functools.wraps`, tức `def` thứ hai;
  - W2: gán `__wrapped__` bằng tay;
  - W3: thay `__code__`, giữ dòng của `def` gốc;
  - W4: đặt sẵn một mục giả trong `linecache`.

  Cả bốn đổi `python ops/a.py || exit 0` (không LF) thành "đo được", trong khi Bash thật ra rc 0 dưới cả ba dòng lệnh GitHub. Lỗ này nằm trong chính đề xuất L01 vòng 5 của tôi; con số "7/7 đỏ" lúc ấy không thử dạng bọc này.
- **Ở chỗ gọi (M02).** Bản sửa 5 THAY phép kiểm hình dạng lời gọi bằng phép gián điệp, chứ không thêm vào. Một `removesuffix(" || true")`, `(" || :")` hay `(" || exit 0")` đặt ở chỗ gọi thì qua hết. Lý do: mọi đầu vào của gián điệp và A14-S3b đều không đổi dưới phép biến đổi ấy. 110/112 vế âm có LF cuối, trong khi 25/30 thân bước luật thật là một dòng không LF.

**Có chặn oan không:** không. Bản gốc, thêm docstring/`#`, `-> str | None`, `from __future__` đều đạt. Mẫu được loader thật dùng: `nap()` của gen 1 nạp từ tệp, và bộ chạy đột biến ghi tệp tạm rồi chạy `-B`, nên `getsource` dùng được. Đề xuất vá M01 cũng không chặn oan code đã chạy nóng hay đang bị `settrace`/`sys.monitoring` theo dõi.

**Về mức nghiêm trọng:** vòng 5 tôi xếp lớp "chỉ có khi cố ý viết" là P3. Chủ kho đã chọn đóng lớp này ở (a′), theo P2 của Codex. Tôi xếp theo chuẩn ấy.

Tôi không sửa gì trong `repo/`: HEAD vẫn `95565cb`, `git status` rỗng. Script và JSON của phép đo nằm ở `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-6-claude/work/v6/`, bảng tóm tắt ở `GHI_CHU_DO.md` trong cùng thư mục.

```
# VERDICT wp1236 r8 vòng 6
spec_sha256: 7c85e68e1ac5a5875925a4a48b7c5b691b146bbdcf4d740e274eb29ff09ab1c4
## Finding vòng 5 của tôi
- L01: ĐÓNG — bốn đường đã nêu (gán lại tên, def thứ hai, đổi __code__, __builtins__) cùng decorator và bản bọc tinh vi: 6/6 biến thể nhóm A của tôi ĐỎ ở kiem_s0_v5 (work/v6/thu_s0_v5cu_qua_v5.json); nhưng đề xuất L01 của tôi thiếu, các đường còn lại ghi thành M01.
- L02: ĐÓNG — mô hình chuẩn hoá NFC/rstrip trên bản sao dict bước ĐỎ ở gián điệp (main_v5); số A14-S3b tái lập đúng 112 + 7 + 206 = 325, mẫu 69/69/68 shell, 8 được nhận; việc THAY (không thêm) phép kiểm hình dạng mở đường mới, ghi thành M02.
- L03: ĐÓNG — văn bản vế (4) và dòng 415–416 khớp thuật toán dump_doi_tuong (bỏ docstring và returns, decorator_list rỗng); `-> str | None` ĐẠT, chú thích kiểu tham số ĐỎ.
- L04: ĐÓNG — hằng GIOI_HAN_K7S (dòng 330, 345, 347); hằng GIOI_HAN của gen 1 giữ nguyên.
- L05: ĐÓNG — A14-S5 theo os.name (dòng 978); cột đột biến A14-S6 (dòng 979); danh sách CHƯA đo có m-S26, m-S29 và vế (5) (dòng 982); cơ chế cờ chế độ (dòng 1046; P3 về chính cái cờ ghi ở M04).
## Findings mới
- id: M01
  severity: P2
  vi_tri: A14-S0 vế (3)–(4), dòng 972; dòng 415–418; bảng Phản biện dòng 1532 ("mọi biến thể đã nêu ĐỎ")
  van_de: Vế (4) chạy trên `inspect.getsource(f)`. Hàm này lần theo `__wrapped__` (inspect.unwrap), tin `f.__code__.co_firstlineno` và đọc dòng nguồn qua `linecache`, nên nó KHÔNG đọc "nguồn của chính đối tượng gắn với tên" như đặc tả viết. Bốn biến thể qua cả năm vế và mọi ca hành vi mà vẫn nuốt lỗi. Không chặn thi công: executor viết đúng văn bản thì qua; nhưng A14-S0 không chứng nhận được đúng điều quyết định (a′) đặt ra.
  bang_chung: `python3 -I work/v6/thu_s0_v6.py` (rc 0): W1 `@functools.wraps(_goc)` + def cu_phap_run thứ hai bọc `removesuffix(' || exit 0')`, W2 `_boc.__wrapped__ = _goc; cu_phap_run = _boc`, W3 `cu_phap_run.__code__ = _boc.__code__.replace(co_firstlineno=<dòng def gốc>)`, W4 mục `linecache.cache[__file__]` có mtime None ⇒ kiem_s0_v5 = [] ở cả bốn, trong khi `cu_phap_run("python ops/a.py || exit 0", None)` ra None (tham chiếu: lenh_ngoai_cu_phap). Phép biến đổi ấy cho 0/119 vế bảng, 0/206 mẫu, 0/61 530 kho A14-S6 lệch (thu_goi_v6.json, removesuffix_hoac_exit0). `thu_bash_v6.py`: thân không LF `python ops/hong.py || exit 0` ⇒ rc 0 và DA_CHAY dưới `bash -e`, `bash --noprofile --norc -eo pipefail`, `sh -e`.
  de_xuat: Thay vế (4) bằng một thuật toán không đi qua inspect hay linecache: (a) `vars(f) == {}`; (b) đọc thẳng `Path(module.__file__)`, `compile(..., dont_inherit=True)`, đòi ĐÚNG MỘT code object con có `co_name == "cu_phap_run"` và `co_firstlineno == f.__code__.co_firstlineno`, và nó `== f.__code__` (so cả bytecode, consts, names); (c) `ast` của `def` tại đúng dòng ấy (decorator_list rỗng, bỏ docstring và returns) BẰNG bản chép. Đo bằng `thu_de_xuat_v6.py`: 22/22 đúng kỳ vọng (hợp lệ ĐẠT; mọi biến thể v4, v5, W1–W4 và W5 đổi `co_consts` ĐỎ). `thu_chan_oan_v6.py`: không chặn oan sau 200 000 lời gọi nóng, dưới settrace, dưới sys.monitoring. Thêm m-S30 (bọc bằng `functools.wraps`), ca đích A14-S0. Sửa câu "NGUỒN CỦA CHÍNH ĐỐI TƯỢNG" cho khớp phép đo.
- id: M02
  severity: P2
  vi_tri: A14-S0 vế (5), dòng 972 ("thay vế 'hình dạng lời gọi' của bản sửa 4"); dòng 418–419; A14-S3b dòng 976; bảng vế âm dòng 947–968
  van_de: Bản sửa 5 BỎ phép kiểm cấu trúc của chỗ gọi (đối số phải là `<tên>.get("run")`) để thay bằng gián điệp. Gián điệp chỉ bắt được phép biến đổi làm đổi một trong 40 thân nó đưa vào, và A14-S3b không có vế một dòng KHÔNG LF nào. Vì vậy `kiem` gọi `cu_phap_run(buoc.get("run").removesuffix(" || true"), …)` qua mọi ca, rồi nhận `run: python ops/x.py || true` dạng plain scalar, đúng dạng của 25/30 bước luật thật. Không chặn thi công; đây là hồi quy so với văn bản bản sửa 4, cùng lớp với (a′).
  bang_chung: `python3 -I ../work/v6/thu_goi_v6.py` (từ repo): removesuffix(" || :"), (" || exit 0"), (" || true") ⇒ đổi 0/30 thân F-ok-goc, 0/30 F-ok, 0/10 lượt gián điệp đặc biệt; lệch 0/119 + 0/206 ở A14-S3b; 0/61 530 ở kho S6. Đếm: 25/30 thân bước luật ở ci.yml@fe84620 là một dòng không LF; 110/112 vế âm có LF cuối (2 còn lại không phải chuỗi). `thu_bash_v6.py`: ba thân ấy không LF ⇒ rc 0, DA_CHAY dưới cả ba dòng lệnh GitHub.
  de_xuat: Giữ CẢ phép kiểm `ast` hình dạng lời gọi của bản sửa 4 LẪN gián điệp. Thêm vào gián điệp 10 thân không LF × hai giá trị `shell` (`X || true`, `X || :`, `X || exit 0`, `X &`, `! X`, `X\r\n`, `X\t`, hai dấu cách, cách đầu, cách cuối). Đo bằng `thu_goi_de_xuat_v6.py`: 12/12 phép biến đổi bị bắt. Cho A14-S3b chạy thêm bản bỏ LF của 116 vế (7 được nhận). Ghi thẳng phần còn lại: ghi đè KẾT QUẢ ở chỗ gọi chỉ được canh bằng kho hữu hạn và review mã.
- id: M03
  severity: P3
  vi_tri: bảng disposition dòng 1032; đoạn dòng 1041–1043; nang_tran can_cu dòng 814 và bảng kich_thuoc dòng 801; dòng 418–419
  van_de: Bốn chỗ câu chữ. (a) m-S26 không nêu cụ thể phép biến đổi, nên có thể sống qua chính ca đích A14-S3b (vd NFC: 0 lệch). (b) Đoạn văn xếp m-S21 và m-S22 vào nhóm "CHỈ cấu trúc bắt được", trong khi g_bom_dau và g_python_hoa bắt chúng bằng hành vi; bảng thắng nên vô hại. (c) "164 đột biến (… 6 tiền xử lý/đường gọi …)" và ước số dòng chưa tính m-S27…S29 cùng phần gián điệp. (d) "ĐÚNG MỘT lời gọi cho một bước YAML" đọc được là cho phép một lời gọi cho bước YAML mà tám mảnh `gate-cong-cu` dùng chung, trong khi vế (5) đòi số lời gọi bằng số cặp (job J, bước luật).
  bang_chung: SPEC.md:1032 ("trên `run` đã biến đổi"); thu_goi_v6: strip lệch 3/119 vế ở A14-S3b, nfc 0; probes_r8.py có g_bom_dau và g_python_hoa; 53 + 91 + 8 + 9 + 6 = 167.
  de_xuat: Ghim m-S26 = `run.strip()` tại lời gọi; sửa câu ở dòng 1043; cập nhật 164 thành 167 và cộng thêm khoảng 40 dòng (vẫn dưới 2400); viết "mỗi cặp (job J, bước luật) đúng một lời gọi, không dùng chung kết quả giữa các mảnh".
- id: M04
  severity: P3
  vi_tri: dòng 1046 (cờ chế độ `TL_A14S6_CHI_A`)
  van_de: Một biến môi trường tắt vế (b) của A14-S6. Nếu biến ấy lọt vào lượt chạy gate thường thì (b) bị bỏ mà vẫn xanh, đúng kiểu "cổng xanh vì vắng mặt" của CLAUDE.md.
  bang_chung: SPEC.md:1046: cờ do bộ chạy đột biến đặt, nhưng không có chốt nào đòi bằng chứng dương rằng (b) đã chạy ở lượt thường.
  de_xuat: Chỉ nhận cờ khi chạy trong tiến trình con của `chay_con`, vd khi `GATE_OUTPUT_DOI_CHIEU_MA` trỏ vào thư mục tạm của đột biến. Khi chạy đủ, A14-S6 in dòng dương "(b) N/N truyen_loi"; khi có cờ, in rõ "BỎ QUA (b): chế độ đột biến".
## Đã đo lại, khớp
- sha256 SPEC.md = HEAD:ops/specs/wp1236-r8.md (cmp trùng); HEAD 95565cb, git status rỗng trước và sau; khối hằng SPEC.md:395–400 và hàm 403–413 trùng byte gram.py.
- khoa_ast_r8.py (bản sao): rc 0, JSON trùng byte; main_v5: gốc, chú thích/docstring, `-> str | None` ĐẠT; sáu biến thể ĐỎ; hai mô hình gián điệp ĐỎ.
- probes_r8 112/112 (42 rc 0, 37 nuốt thật), 7/7 dương; dot_bien_r8 53/53; g1_qua_grammar 52/52; sinh_r8 61 530 / 2 647 / 0 lệch / 0 nuốt / 0 không chạy, 2 phút 6 giây; bốn JSON trùng byte bản trong kho.
- Grammar K7-S đúng trong môi trường sạch: fuzz từ EBNF với hạt mới 20261108, 300 thân, 902 lượt Bash/dash thật (env chỉ PATH/HOME), 0 lượt xấu.
- Tính khả thi của getsource: `nap()` của gen 1 nạp bằng spec_from_file_location(MA); bộ chạy đột biến ghi tệp tạm rồi chạy con với `-B`; khoa_ast_r8 nạp từ tệp đo được. Vế (5): doc_wf = yaml.safe_load của `git cat-file blob`, nên chuỗi trùng với bản test tự đọc, không chặn oan vì khác bộ nạp.
- A14-S3b 325 = 112 + 7 + 206; vế (5) đọc từ F-ok/F-ok-goc: 30 tên bước luật, 6 thân VL-F đúng nguyên văn.
- Q-r8-1…5, kich_thuoc (≈ 2250, tran_moi 2400) và tran_loi_goi_codex_A1_gen2 (4 ≤ 8 theo ADR-0052, hết trần đi ADR-0037) không đổi ở bản sửa 5; không thấy số đo sai hay mâu thuẫn ADR mới.
KET_LUAN: changes_requested
```