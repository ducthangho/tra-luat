Kết luận vòng 5: **approve**. Không còn P0, P1 hay P2. Có năm P3; không cái nào chặn thi công.

**Bản sửa 4 có đóng được lớp "cài đặt khác mà tưởng tương đương" không?**
- **Trong thân hàm: đóng.** Tôi chạy lại 10 biến thể vòng 4 sửa trong thân `cu_phap_run`, gồm `removesuffix(" || :")`, `removesuffix(" &")`, `removeprefix("! ")`, `strip`, `rstrip`, `splitlines`, `.match` và hàm phụ. Cả 10 đều đỏ ở A14-S0 (`ast_ham`).
- **Ngoài thân `def`: còn lọt.** A14-S0 so đoạn `def` trong mã nguồn, chứ không so hàm mà tên `cu_phap_run` thực sự trỏ tới lúc chạy.
  - Có bốn cách qua cả năm vế: gán lại tên sau `def`, viết `def` thứ hai, đổi `__code__`, hoặc tự đặt `__builtins__`. Đọc vế (4) theo văn bản hay theo `khoa_ast_r8.py` thì kết quả như nhau.
  - Một bản bọc bỏ đuôi `" || exit 0"` qua được mọi ca hành vi: 0/112 vế âm, 0/61 530 đầu vào A14-S6 (a), 0/209 mẫu A14-S3b.
  - Thân ấy chạy chương trình hỏng mà vẫn ra rc 0 dưới cả ba shell (`bash -e`, `bash --noprofile --norc -eo pipefail`, `sh -e`), tức là nuốt lỗi.
  - Tôi xếp P3, cùng mức với K01 vòng 4. Lý do: đường này chỉ có khi cố ý viết; đặc tả đã cấm bằng lời; review mã nhìn là thấy. Cách sửa rẻ và tôi đã đo: chạy vế (4) trên nguồn của chính đối tượng mà tên trỏ tới (`inspect.getsource(module.cu_phap_run)`), cộng vài phép kiểm binding. Khi đó 7/7 biến thể lọt đều đỏ, các bản hợp lệ vẫn đạt (L01).
- **Lời gọi:** vế (5) chỉ kiểm hình dạng lời gọi. Nếu `run` bị sửa trên dict bước trước khi gọi thì lời gọi vẫn đúng hình dạng. Mẫu A14-S3b chỉ bắt được vài kiểu sửa như vậy (L02).
- **Có chặn oan cài đặt hợp lệ không?** Theo thuật toán của `khoa_ast_r8.py` thì không. Theo văn bản vế (4) thì có một chỗ: chú thích kiểu trả về `-> str | None`, viết y như chữ ký ở dòng 362, sẽ làm A14-S0 đỏ (L03). Vế (5) bắt đúng mẫu `str(y.get("run", ""))` mà gen 1 để lại; đó là chặn đúng luật, không phải chặn oan.

**Những phần khác:**
- **Các P3 vòng 4:** đã sửa. Còn sót vài câu (L05) và một chỗ trùng tên: gen 1 đã có hằng `GIOI_HAN`, khác giá trị, đang được in trong dòng `TỔNG` của `kiem-ho-so` (L04).
- **Grammar trong môi trường sạch:** vẫn đúng. Tôi chạy lại kho sinh (2 phút 8 giây, mọi số khớp) và một phép fuzz độc lập từ EBNF: 400 thân, 1 201 lượt Bash/dash thật, 0 lượt xấu.
- **Merge `origin/master`:** sạch, không đưa vào tệp nào ngoài `ops/specs/` và `ops/reviews/`.

Tôi không sửa gì trong `repo/` (HEAD vẫn `a419a01`, `git status` rỗng). Script đo và ghi chú nằm ở `/tmp/claude-0/-home-user-tra-luat/caf22779-10f3-5574-a917-7d9657c1fb93/scratchpad/review/r8-5-claude/work/v5/` (`GHI_CHU_DO.md`, `thu_s0.py`, `thu_s3b.py`, `thu_de_xuat.py`, `thu_k01.py`, `fuzz_ebnf.py`, kèm JSON).

# VERDICT wp1236 r8 vòng 5
spec_sha256: 36bbcee68fcbbd5079a399f5cc8a8d00e179d6615272c7ed9754199da4b70b6c
## Finding vòng 4 của tôi
- K01: ĐÓNG — `cu_phap_run` nay chép nguyên văn (SPEC.md:402–412 trùng byte gram.py:12–22); 10/10 biến thể sửa TRONG thân hàm của vòng 4 (L1, L3–L8, L14, L15, L17) đỏ `ast_ham` ở `kiem_s0` (`work/v5/thu_k01.py`). Đường còn hở nằm NGOÀI thân `def`, ghi thành L01.
- K02: ĐÓNG — 24 hạt; lấy mẫu 222/665 có khai (đo lại 665 và 222); m-S0f ghi là chốt cấu trúc; tách hằng/hàm/tiền xử lý; "SÁU cái v3a–d, v3f, v3h" ở đoạn đo; 1620 + 10 + 555 + 63 = 2248 ≈ 2250; *Phạm vi của passed* có `kiem-ho-so`. Còn sót "v3a…v3h" ở hàng A14-S6 (L05b).
- K03: ĐÓNG — `GIOI_HAN: str` có trong API mục 6; B/C/D in từ module, test so với hằng và với bản chép chữ. Tên trùng với hằng có sẵn của gen 1: L04.
- K04: ĐÓNG — mỗi đột biến một ca đích; vế (a) đo 0,07 s, vế (b) 2 phút 8 giây; A14-S5/S6 (b) chỉ chạy khi `os.name == "posix"`; tổng thời gian dưới 5 400 s. Còn sót câu "Chạy khi bash/sh có trên PATH" ở hàng A14-S5 (L05a).
## Findings mới
- id: L01
  severity: P3
  vi_tri: K7-S dòng 414–416; A14-S0 dòng 969 vế (3) và (4); đoạn "Chốt cho LỚP là A14-S0" dòng 1030–1037; bảng Phản biện dòng 1509
  van_de: A14-S0 so đoạn `def cu_phap_run` trong NGUỒN, không so đối tượng đang gắn với tên `cu_phap_run`, nên gán lại tên sau `def`, viết `def` thứ hai, đổi `__code__` hay tự đặt `__builtins__` qua cả năm vế, và một bản bọc như thế sống qua mọi ca hành vi mà vẫn nuốt lỗi dưới Bash thật. Không chặn thi công: đường này chỉ có khi cố ý viết, văn bản dòng 414–416 đã cấm, review mã thấy ngay; nhưng câu "đóng theo KIẾN TRÚC" rộng hơn phép đo.
  bang_chung: `python3 -I work/v5/thu_s0.py`: biến thể A_boc_gan_lai_tinh_vi (`_goc = cu_phap_run`, rồi `def _boc(run, shell)` trả `_goc(run.removesuffix(' || exit 0'), shell)`, rồi `cu_phap_run = _boc`) ⇒ `kiem_s0` = [] (ĐẠT), vế (4) đọc theo văn bản cũng ĐẠT; 0/112 vế âm lệch. A_gan_lai_ten, A_hai_def, A_doi_code, A_builtins đều ĐẠT `kiem_s0` (A_builtins chỉ đổi được sang "từ chối hết", nên A14-S2 vẫn bắt). `thu_s3b.py` (suffix_exit0): 0/61 530 ở A14-S6 (a), 0/209 ở mẫu A14-S3b. `thu_k01.py`: Bash thật trên `python ops/hong_test.py || exit 0` ⇒ rc 0 và DA_CHAY dưới `bash -e`, `bash --noprofile --norc -eo pipefail` và `sh -e`.
  de_xuat: Cho vế (4) chạy trên `inspect.getsource(module.cu_phap_run)` (nguồn của chính đối tượng gắn với tên) và đòi `decorator_list` rỗng; thêm vào vế (3) `__closure__`, `__defaults__`, `__kwdefaults__` là None và `cu_phap_run.__builtins__ is vars(builtins)`. Đo bằng `work/v5/thu_de_xuat.py`: 7/7 biến thể A đỏ; bản gốc, bản thêm chú thích/docstring, `-> str | None`, `from __future__ import annotations` và đổi kiểu nháy đều ĐẠT; chỉ chú thích kiểu tham số đỏ, đúng luật. Thêm đột biến m-S27 (gán lại tên) với ca đích A14-S0. Nếu không sửa thì ghi thẳng ở dòng 1030: chốt khoá NGUỒN `def`, đường gán lại tên do review mã canh.
- id: L02
  severity: P3
  vi_tri: A14-S0 vế (5) dòng 969; A14-S3b dòng 973; K7-S dòng 415–416 ("trên chính dict bước … kết quả dùng nguyên")
  van_de: Vế (5) chỉ kiểm HÌNH DẠNG lời gọi, nên một biến đổi đặt trên dict bước TRƯỚC lời gọi (vd `y = {**y, "run": y["run"].rstrip("\n")}`) vẫn qua; vế "trên chính dict bước" khi đó chỉ còn A14-S3b canh, mà mẫu 1/300 của nó bắt rất ít. Số "200 thân" cũng không tái lập được.
  bang_chung: `python3 -I work/v5/thu_s3b.py`, số đầu vào lệch trong mẫu A14-S3b (209): strip 2, rstrip 2, rstrip("\n") 0, bỏ BOM 1, hạ chữ 1, removesuffix(" || :") 0 (vế `g_hoac_hai_cham` có LF cuối nên biến đổi trên `run` thô không chạm tới), removesuffix(" &") 1, removeprefix("! ") 0, CRLF 0, tab→cách 0, gộp cách 4, dòng đầu 0 (A14-S3 bắt). Cùng các biến đổi ấy qua 112 vế âm: 3, 3, 1, 1, 1, 0, 1, 1, 1, 3, 14, 6. Đếm mẫu theo thứ tự `sinh_r8.main` với `i % 300 == 0`: 206 đầu vào (3 được nhận), cộng 3 vế đặt tên = 209.
  de_xuat: Thêm phép gián điệp vào A14-S3: thay `module.cu_phap_run` bằng hàm ghi lại đối số, gọi `kiem` trên `F-ok` và `F-ok-goc`, đòi multiset (run, shell) ghi được BẰNG multiset `(bước.get("run"), bước.get("shell"))` mà test tự đọc từ `git show <SHA>:.github/workflows/ci.yml` cho mỗi cặp (job J, bước luật). Phép so này dùng giá trị thật, không phụ thuộc kho. Thêm cả 112 + 7 vế vào A14-S3b qua `kiem`, và ghi quy tắc chọn mẫu đúng với con số (209, hoặc một quy tắc ra đúng 200).
- id: L03
  severity: P3
  vi_tri: A14-S0 vế (4) dòng 969; dòng 362 (`cu_phap_run(run, shell) -> str | None`); dòng 414 ("Được thêm docstring, chú thích…")
  van_de: Văn bản vế (4) và thuật toán đã đo (`khoa_ast_r8.dump_ham` dựng lại FunctionDef với `decorator_list=[]`, `returns=None`) cho hai chốt khác nhau. Theo thuật toán, decorator tiền xử lý lọt. Theo văn bản, chú thích `-> str | None` y như chữ ký ở dòng 362 làm A14-S0 đỏ. "Chú thích" cũng đọc được là chú thích kiểu (type annotation).
  bang_chung: `work/v5/thu_s0.py`: A_decorator_removesuffix — theo thuật toán [] (ĐẠT), theo văn bản ĐỎ; B_return_annotation — theo thuật toán ĐẠT, theo văn bản ĐỎ; B_param_annotation — đỏ theo cả hai.
  de_xuat: Ghi vế (4) đúng một thuật toán: "bỏ docstring và `returns`; `decorator_list` phải rỗng; không được thêm chú thích kiểu cho tham số"; ở dòng 414 đổi "chú thích" thành "chú thích `#`".
- id: L04
  severity: P3
  vi_tri: API mục 6 dòng 330; *Phạm vi của passed* dòng 343–347
  van_de: Gen 1, nền của gen 2, đã có hằng `GIOI_HAN` mang giá trị khác (giới hạn §10.2.3/Q10 của waiver), và CLI `kiem-ho-so` in hằng ấy trong dòng `TỔNG`; đặc tả đặt cho hằng xuất mới đúng tên ấy mà không nói hằng cũ đi đâu.
  bang_chung: `git show 508d678:ops/gate_output_doi_chieu.py`: dòng 360 `GIOI_HAN = ("điều kiện cần cho §10.2.3; giới hạn Q10: actor không tách được chủ kho với agent (cùng login), "…`; dòng 529 `print(f"TỔNG: … ({len(kq)} lời khai; {GIOI_HAN})")`.
  de_xuat: Đặt tên khác cho hằng mới (vd `GIOI_HAN_K7S`), hoặc ghi rõ hằng cũ đổi tên (vd `GIOI_HAN_WAIVER`) và dòng `TỔNG` của `kiem-ho-so` vẫn giữ văn bản §10.2.3/Q10.
- id: L05
  severity: P3
  vi_tri: hàng A14-S5 dòng 975; hàng A14-S6 dòng 976; dòng 979; dòng 1039–1040
  van_de: Bốn chỗ câu chữ còn sót sau bản sửa 4: (a) hàng A14-S5 vẫn ghi "Chạy khi bash/sh có trên PATH … nền khác vắng ⇒ BỎ QUA", trái với đoạn 1040 ("chỉ khi os.name == posix, bất kể PATH"); (b) cột đột biến của hàng A14-S6 vẫn ghi "v3a…v3h, m-S15/…" trong khi bảng disposition đã gán chúng cho A14-S0; (c) m-S26 và vế (5) chưa được đo (`khoa_ast_r8.py` không cài vế (5)) mà không có trong danh sách "CHƯA đo" ở dòng 979; (d) bộ chạy kế thừa từ gen 1 chạy ca đích trên bản gốc trước MỖI đột biến, nên câu "(b) chỉ chạy MỘT lần" cần nói cơ chế.
  bang_chung: SPEC.md:975 và :1040 đọc liền nhau; SPEC.md:976 so với :1021–1025; `khoa_ast_r8.py` không có phép kiểm `Call`; `git show 508d678:ops/gate_output_doi_chieu_test.py` (`chay_dot_bien`): gọi `chay_con(khop[0], ma, …)` trên bản gốc, rồi mới ghi `goc_.replace(cu, moi)`. Không có cơ chế thì 7 × ~128 s ≈ 15 phút, vẫn dưới 5 400 s, nên không chặn.
  de_xuat: Sửa hàng A14-S5 theo đúng luật POSIX; ghi "v3a–d, v3f, v3h" và ghi chú "ca đích là A14-S0" ở hàng A14-S6; thêm m-S26 và vế (5) vào danh sách CHƯA đo; ghi cơ chế, vd A14-S6 có chế độ đột biến chỉ chạy (a).
## Đã đo lại, khớp
- sha256 SPEC.md = HEAD:ops/specs/wp1236-r8.md = 36bbcee6…; HEAD a419a01, `git status` rỗng trước và sau; khối hằng SPEC.md:394–399 trùng byte gram.py:4–9, hàm SPEC.md:402–412 trùng byte gram.py:12–22.
- khoa_ast_r8: gốc và bản thêm chú thích/docstring ĐẠT, bảy biến thể đỏ, rc 0, JSON khớp byte.
- probes_r8: 112/112 vế âm bị từ chối (g 50, kt 29, l8 16, l9 11, connector 6), 42 rc 0, 37 nuốt thật, 7/7 vế dương; `g_bom_dau`, `g_python_hoa` rc 127, `g_hoac_hai_cham` rc 0 kèm DA_CHAY; JSON khớp. dot_bien_r8: 53/53. g1_qua_grammar: 52/52. JSON khớp.
- sinh_r8: 61 530 đầu vào, 2 647 được nhận, 0 lệch, 0 nuốt lỗi, 0 không chạy, 2 phút 8 giây, JSON khớp. 24 hạt; 222/665; vế (a) 0,07 s. gram.py, sinh_r8.py, dot_bien_r8.py, census_r8.py không đổi từ 2e7fab1, nên số 91/91 và census của vòng 4 vẫn đứng.
- Grammar K7-S đúng trong môi trường sạch: `work/v5/fuzz_ebnf.py` sinh 400 thân ngẫu nhiên từ EBNF (P, W đủ bảng ký tự), chạy 1 201 lượt Bash/dash thật với env chỉ PATH/HOME: 0 thân không được nhận, 0 lượt xấu.
- Merge: merge-base = 9607e3e = origin/master; `git diff --name-only 9607e3e 3eb4be1` chỉ có ops/specs/wp1236-r8.md và ops/reviews/** (0 tệp ngoài); `git merge-tree --write-tree 975fe2b 9607e3e` = tree của 843126b (a9a29e8f…), tức merge tự động, không sửa tay.
- Vế (5) bắt đúng mẫu `str(y.get("run", ""))` mà gen 1 để lại (508d678:337); vế (3) không chặn oan, vì gen 1 không định nghĩa `type` hay `str` ở mức module.
- Ước 2150–2300 (≈ 2248), `tran_moi` 2400; Q-r8-1…5 và `tran_loi_goi_codex_A1_gen2` không đổi so với vòng 4 (4 ≤ 8 theo ADR-0052, hết trần thì đi ADR-0037), không có mâu thuẫn mới.
KET_LUAN: approve