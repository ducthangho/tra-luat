"""Dựng đặc tả wp1466 r8 từ r7: rút khối tiền kiểm, thu hẹp điều kiện bắt đầu. Mọi phép thay đòi đúng 1 lần xuất hiện."""
import hashlib, pathlib, sys

SPEC = pathlib.Path("/home/user/tra-luat/ops/specs/wp1466.md")
HERE = pathlib.Path(__file__).resolve().parent
R7_SHA = "baf01d45ba30512e768466fd077842346644db730d69471a44efb2a40b6b9139"

raw = SPEC.read_bytes()
assert hashlib.sha256(raw).hexdigest() == R7_SHA, "tệp không phải r7"
lines = raw.decode("utf-8").split("\n")

# --- Mục 1: thay bước 3 (dòng 67–75) và xoá khối tien-kiem + bảng đầu vào (dòng 77–239, gồm dòng trống trước khối)
assert lines[66].startswith("3. Tiền kiểm cấp lease, chạy NGAY TRƯỚC khi cấp")
assert lines[74].startswith("   wp1466 KHÔNG dựa vào phần chưa có của nợ")
assert lines[75].startswith("4. Trên base ấy, sáu neo chèn")
assert lines[76] == "" and lines[77].startswith("Khối `tien-kiem` (137 dòng không trống)")
assert lines[79] == "~~~ tien-kiem" and lines[217] == "~~~"
assert lines[219].startswith("**Đầu vào của khối**") and lines[238].startswith("| P5 |")
assert lines[239] == "" and lines[240] == "## 2. `nguon_cap_viec`"
buoc3 = (HERE / "muc1_buoc3.md").read_text(encoding="utf-8").rstrip("\n").split("\n")
lines = lines[:66] + buoc3 + [lines[75]] + lines[239:]
s = "\n".join(lines)


def thay(old, new):
    global s
    n = s.count(old)
    if n != 1:
        sys.exit(f"thay: {n} lần cho {old[:90]!r}")
    s = s.replace(old, new)


# --- H1, revision, dòng trạng thái
thay("# wp1466 r7 — ADR-0068", "# wp1466 r8 — ADR-0068")
thay("\nrevision: 7\n", "\nrevision: 8\n")
thay("theo mục sổ `xet_lai_cach_lam` nêu ở mục 0. Người soạn r1 đến r4",
     "theo mục sổ `xet_lai_cach_lam` nêu ở mục 0. Revision 8 soạn cùng ngày, cùng người soạn, trên `origin/master` "
     "`4e56f005785db1b04e043bb71fc694a674a8dc9f` (đo lại 05:41:07Z), sau review Codex lượt 7 của r7 (commit `3c89d87`; "
     "hồ sơ lưu ở `fd2f17e`; verdict `ops/specs/wp1466/review/r7-l7/VERDICT.md`, sha256 "
     "`082db6d7c1cb824336268bff5c274990bea83bb783eefa2986a38df7ac8c8d54`: `changes_requested`; bảng (i) 1 lớp P2, 0 P0, "
     "0 P1, 0 lớp mới, 0 lớp tái mở; hội tụ 0/1) và sau quyết định E2 của chủ kho tách khối tiền kiểm (mục 0); r8 chỉ "
     "rút khối ấy và thu hẹp điều kiện bắt đầu về công cụ sẵn có. Người soạn r1 đến r4")

# --- Mục 0: bảng việc không thuộc wp1466, thẩm quyền
thay("| verdict máy đọc theo lớp: lược đồ v2, danh tính provider, vị từ chuyển tiếp, K4 của `kiem-merge`, lệnh kiểm verdict đặc tả và kế hoạch | Issue #1470 | `INV-12-CONG-VERDICT-THEO-LOP` |\n",
     "| verdict máy đọc theo lớp: lược đồ v2, danh tính provider, vị từ chuyển tiếp, K4 của `kiem-merge`, lệnh kiểm verdict đặc tả và kế hoạch | Issue #1470 | `INV-12-CONG-VERDICT-THEO-LOP` |\n"
     "| công cụ tiền kiểm lease toàn kho: closure của §5 khi policy tồn tại, chuẩn hoá và so tiền tố cho một write set bất kỳ, nguồn dữ liệu chỉ từ ảnh chụp máy chủ, mọi đầu vào của quyết định cấp lease; gồm giới hạn G1 đến G10 ở mục 1 | Issue #1484 | `INV-02-TIEN-KIEM-CAP-LEASE-KHONG-CLOSURE` |\n")
thay("Thẩm quyền của việc tách: chủ kho chọn \"Duyệt tách 3 packet\" (mã E2), ghi hộ ở https://github.com/ducthangho/tra-luat/issues/1466#issuecomment-7053593553.",
     "Thẩm quyền của việc tách: chủ kho chọn \"Duyệt tách 3 packet\" (mã E2), ghi hộ ở https://github.com/ducthangho/tra-luat/issues/1466#issuecomment-7053593553. "
     "Thẩm quyền của việc tách khối tiền kiểm: chủ kho chọn \"Tách khối ra (Recommended)\" (mã E2), ghi hộ ở "
     "https://github.com/ducthangho/tra-luat/issues/1466#issuecomment-7058057029; Issue kế nhiệm #1484 (`open` lúc 05:41:58Z, REST GET) "
     "khai `depends_on: [1466]`.")

# --- Mục 0: checkpoint lần hai, ý 3 (r5) thành lịch sử
thay("3. `tien-kiem-lease-chua-du` (F11.b/c): vắng tệp policy change-impact trên base là ĐIỀU KIỆN BẮT ĐẦU đo được, fail-closed; phần chuẩn hoá và so tiền tố của §5 mà `ai-dang-giu` không làm được đo bằng một khối tiền kiểm có điều kiện dừng, chạy trước khi đăng lease và chạy lại ngay sau khi đăng (mục 1).",
     "3. `tien-kiem-lease-chua-du` (F11.b/c): r5 đặt việc vắng policy change-impact trên base làm điều kiện bắt đầu, và dựng một khối tiền kiểm cho phần chuẩn hoá và so tiền tố của §5 mà `ai-dang-giu` không làm được. Khối ấy đã rút ở r8 (đoạn cuối mục này).")

# --- Mục 0: đoạn r6 và r7 gọn lại thành lịch sử; thêm đoạn r8
i6 = s.index("**Revision 6, sau review lượt 5.**")
i1 = s.index("## 1. `packet_id` · `packet_issue`")
assert s.count("**Revision 6, sau review lượt 5.**") == 1 and i6 < i1
moi_0 = (
    "**Revision 6 và 7, sau review lượt 5 và 6.** Lượt 5 cho hội tụ 2/3: U là ba lớp bảng (i) cuối lượt 4; F là phần "
    "wp1466 của `kiem-chuoi-khong-doc-cau-truc` và lớp `tieu-chi-dong-xoa-khong-do-hanh-vi`. Lượt 6 cho 0/1. Cả hai lượt "
    "không có lớp mới, không có lớp tái mở; lớp duy nhất còn mở ở bảng (i) là `tien-kiem-lease-chua-du`. r6 và r7 chỉ "
    "sửa lớp ấy, bằng cách mở rộng khối tiền kiểm: r6 thêm một bất biến về nguồn dữ liệu (F11.d), r7 viết bất biến ấy "
    "thành danh sách đầu vào (F11.e, F11.f), theo mục sổ `xet_lai_cach_lam` ở "
    "https://github.com/ducthangho/tra-luat/issues/1466#issuecomment-7057370281. Bốn tệp của nguyên mẫu, khoá văn bản, "
    "N8, khối `khoa`, các khối protocol và bảng (ii) không đổi ở cả hai revision. Khối và bảng đầu vào của r6, r7 đã "
    "rút ở r8; hồ sơ của chúng ở mục 18 và mục 19.\n\n"
    "**Revision 8, sau review lượt 7: lần thứ bảy của cùng một lớp, và quyết định E2 tách khối tiền kiểm.** Lượt 7 cho "
    "hội tụ 0/1: U là lớp duy nhất của bảng (i) cuối lượt 6; F là 0. F11.e và các đường PyYAML cụ thể của F11.f được "
    "xếp đã đóng, nhưng lượt 7 đo được ba biểu hiện mới trong cùng lớp. F11.g: đối số `--sau-dang` loại một người giữ "
    "theo `lease_id` tự khai, không đối chiếu với lease vừa đăng. F11.h: dòng `import os, sys` ở đầu khối chạy trước chốt "
    "`-I`, nên với `-S -X frozen_modules=off` `os` nạp được từ PYTHONPATH. F11.i: mã quét lease nạp từ B đọc `ls-tree` "
    "không `-z`, nên tên tệp lease bị git quote bị bỏ mà không báo. Lớp này có mặt ở cả bảy lượt. Hai tín hiệu của §12 "
    "cùng bật: hai chuyển tiếp liên tiếp dưới 50% (r5→r6 và r6→r7, cả hai 0/1), và một lớp có mặt ba lượt trở lên. Phiên "
    "điều phối đưa ba phương án cho chủ kho (mã E2, vì một phương án là nâng trần lời gọi Codex, khi đó còn 2/10): tách "
    "khối, vá tiếp, hay nâng trần. Chủ kho chọn \"Tách khối ra (Recommended)\", ghi hộ ở "
    "https://github.com/ducthangho/tra-luat/issues/1466#issuecomment-7058057029. Revision 8 làm đúng lựa chọn ấy:\n\n"
    "1. Xoá khối `tien-kiem`, bảng *Đầu vào của khối* (V1 đến V11, P1 đến P5), các bước T0 đến T7, bất biến `I-NGUON`, "
    "các kịch bản và đột biến của khối, cùng mọi lời khai rằng khối đóng hay dừng khi không đo được.\n"
    "2. Điều kiện bắt đầu 3a đến 3e (mục 1) chỉ chạy công cụ đã có trên base và đòi kết quả của chúng: so tập cặp ref, "
    "vắng policy trên `origin/master`, `ai-dang-giu` cho từng đường dẫn, số ADR, và đo lại sau khi đăng. Giới hạn đã "
    "biết của các công cụ ấy được ghi thẳng ở bảng G1 đến G10 của mục 1. Bước số ADR đổi nhãn từ 3f thành 3d, vì bước 3d "
    "cũ (khối) đã rút.\n"
    "3. wp1466 không hứa rằng điều kiện bắt đầu phát hiện mọi lease giao write set. Phần còn thiếu là nợ "
    "`INV-02-TIEN-KIEM-CAP-LEASE-KHONG-CLOSURE`: tên đã có sẵn trong ADR-0068, mục *Nợ*, và trong ô `còn nợ` của dòng "
    "`INV-02` ở bảng §1.1. Nợ ấy giao cho Issue #1484 (bảng đầu mục này; mục 14).\n\n"
    "Theo protocol §8.3, chuyển biểu hiện ra ngoài phạm vi KHÔNG được tính là vá. Lớp `tien-kiem-lease-chua-du` vì vậy "
    "không được r8 gọi là đã vá; nó chuyển sang bảng (ii) với thẩm quyền là quyết định E2 trên, và slug giữ nguyên trong "
    "lịch sử (mục 19). Những gì r8 không đổi: bốn tệp của nguyên mẫu (`c35ee03`, +434 −4), khoá văn bản, khối `khoa`, "
    "các khối protocol và băm byte, N8 (`do-pham-vi`), `so-dang-ky`, khối `adr`, và các dòng bảng (ii) cũ. Kích thước "
    "của đặc tả: r7 là 1022 dòng, 184992 byte; r8 là {{DONG}} dòng, {{BYTE}} byte.\n\n"
)
s = s[:i6] + moi_0 + s[i1:]

# --- Mục 1: bảng trường
thay("| packet | `wp1466`, revision 7, generation 1.", "| packet | `wp1466`, revision 8, generation 1.")
thay("| `packet_issue` | #1466 (`open` lúc 03:05Z, REST GET) |", "| `packet_issue` | #1466 (`open` lúc 05:41:58Z, REST GET) |")
thay("r7 đo lại trên `4e56f005785db1b04e043bb71fc694a674a8dc9f` (S17) |",
     "r7 đo lại trên `4e56f005785db1b04e043bb71fc694a674a8dc9f` (S17); r8 đo lại trên cùng commit (S18) |")
thay("| `depends_on` | `[1462]`. 03:05Z, REST GET: #1462 còn `open`; 02:57Z, lease `wp1462-r8-g2-claude` đang giữ `.claude/dev/packet_loop.py` và `.claude/dev/packet_loop_test.py` (S4) |",
     "| `depends_on` | `[1462]`. 05:41:58Z, REST GET: #1462 còn `open`; 05:41:09Z, lease `wp1462-r8-g2-claude` đang giữ `.claude/dev/packet_loop.py` và `.claude/dev/packet_loop_test.py` (S18) |")
thay("| packet sau | #1469 rồi #1470 (mục 0) |", "| packet sau | #1469 rồi #1470 (mục 0); #1484 nhận nợ tiền kiểm lease (mục 0, mục 14) |")

# --- Mục 3
thay("r7, 04:56:46Z: `master` vẫn ở `4e56f00`, nên S2–S15 giữ nguyên; S17 là phép đo lại của r7.",
     "r7, 04:56:46Z: `master` vẫn ở `4e56f00`, nên S2–S15 giữ nguyên; S17 là phép đo lại của r7. r8, 05:41:07Z: `master` "
     "vẫn ở `4e56f00`; S18 là phép đo lại của r8. Các ô S1, S4, S16, S17 nhắc khối `tien-kiem` là số đo lịch sử của r5 đến "
     "r7; khối đã rút ở r8, và không số đo nào của nó là điều kiện của wp1466.")
s17_end = ("Kho chính `/home/user/tra-luat` chỉ làm nguồn object cho `--reference`; không ref nào của nó bị đổi |\n")
thay(s17_end, s17_end +
     "| S18 | đo lại của r8 (`4e56f00`, clone sạch `--reference /home/user/tra-luat` từ máy chủ, tạo 05:40:59Z–05:41:04Z; "
     "log `r8/do/do_that_r8.log`) | Theo đúng điều kiện bắt đầu của r8. 3a, 05:41:07Z, sau `fetch --prune`: tập tên 394 và "
     "394, thiếu 0, thừa 0; tập cặp (tên, SHA) thiếu 0, thừa 0; kho không shallow; `master` ở "
     "`4e56f005785db1b04e043bb71fc694a674a8dc9f`. 3b, 05:41:08Z: 0 đường dẫn chứa `change-impact` dưới `.github/coordination` "
     "trên `master`. 3d, 05:41:08Z: 66 tệp ADR trên `master`; 0 trong 394 ref có `docs/adr/0068-*` hay số lớn hơn. 3c "
     "(05:41:09Z–05:41:44Z, `/usr/bin/python3`, checkout tách rời tại `master`): `packet_loop.py` và `packet_loop_test.py` "
     "đều `NGƯỜI_GIỮ 1: wp1462-r8-g2-claude`, rc 11, lease ở `refs/remotes/origin/ops/wp1462-r1:ops/leases/wp1462-r8-g2-claude.yaml`; "
     "protocol và tệp ADR `NGƯỜI_GIỮ 0: không có`, rc 0. Đối chứng, không phải điều kiện (05:41:51Z, các hàm quét của "
     "`ops/lease_publish.py` trên clone ấy): 551 bản ghi lease; 17 còn hạn; 12 trong số đó có bia mộ hai chiều; 5 còn "
     "hiệu lực (`wp1236-a-r10-g1-claude-20261121`, `wp1448-r6-g6-claude`, `wp1462-r8-g2-claude`, `wp1475-r1-g1-claude`, "
     "`wp433-r9-g5-claude`). Lease B4 `wp1462-r8-g2-claude` vẫn chặn wp1466. Kho chính chỉ làm nguồn object cho "
     "`--reference`; không ref nào của nó bị đổi |\n")
thay("tiền kiểm trước khi cấp: `INV-02-TIEN-KIEM-CAP-LEASE-KHONG-CLOSURE`; và nợ đường state |",
     "tiền kiểm trước khi cấp: `INV-02-TIEN-KIEM-CAP-LEASE-KHONG-CLOSURE` (Issue #1484); và nợ đường state |")

# --- Mục 9
thay("Tiền kiểm 3a–3f của mục 1 là điều kiện CẤP LEASE, không phải tiêu chí nghiệm thu của H; răng của nó đo trên kho giả (mục 18), và lượt ĐẠT của nó chỉ đo được lúc cấp lease.",
     "Điều kiện bắt đầu 3a–3e của mục 1 là điều kiện CẤP LEASE, không phải tiêu chí nghiệm thu của H; chúng chỉ chạy được lúc cấp lease, và giới hạn G1 đến G10 của chúng là nợ của Issue #1484, không phải tiêu chí của wp1466.")

# --- Mục 13
thay("với N8, mọi dạng câu lệnh và biểu thức ràng buộc tên ở module, chỗ chèn được phép, tên dựng sẵn, và ghi đè sổ; với tiền kiểm, cả sáu bước của §5 (mục 19).",
     "với N8, mọi dạng câu lệnh và biểu thức ràng buộc tên ở module, chỗ chèn được phép, tên dựng sẵn, và ghi đè sổ. Với "
     "tiền kiểm, r5 đến r7 cũng tự liệt kê đường vào (sáu bước của §5, rồi nguồn dữ liệu, rồi danh sách đầu vào), nhưng "
     "mỗi lượt review vẫn tìm ra đường thứ ba ở một biên mới. Hình dạng ấy lặp bảy lượt; r8 không vá tiếp mà rút phạm vi "
     "theo quyết định E2 (mục 0, mục 19).")

# --- Mục 14
thay("Hai packet đã có thẩm quyền (quyết định E2 và E5 ở mục 0): **#1469** và **#1470**.",
     "Ba packet đã có thẩm quyền (các quyết định E2 và E5 ở mục 0): **#1469**, **#1470** và **#1484**.")
thay("| #1470 | `INV-12-CONG-VERDICT-THEO-LOP`; và, tuỳ đặc tả của nó, `INV-06-PHIEN-VA-VAI`, `INV-11-K4-KHONG-DOC-HO-MODEL` |\n",
     "| #1470 | `INV-12-CONG-VERDICT-THEO-LOP`; và, tuỳ đặc tả của nó, `INV-06-PHIEN-VA-VAI`, `INV-11-K4-KHONG-DOC-HO-MODEL` |\n"
     "| #1484 | `INV-02-TIEN-KIEM-CAP-LEASE-KHONG-CLOSURE`, gồm giới hạn G1 đến G10 ở mục 1 và các biểu hiện F11.b đến F11.i của lớp `tien-kiem-lease-chua-du` (mục 19). Issue ấy hiện ghi tên nợ khác (`INV-02-TIEN-KIEM-LEASE-TOAN-KHO`) và hẹn chốt tên ở r8; tên chốt là tên đã có trong ADR-0068 |\n")
thay("`COT-CONG-20-CHUA-CO-CONG`; một packet cho `INV-28-TRAN-KICH-THUOC` cùng `INV-16-BO-DEM-NGOAI-TRUC-LOI-GOI`; một packet cho `INV-02-TIEN-KIEM-CAP-LEASE-KHONG-CLOSURE`; một packet đo cho `INV-03`.",
     "`COT-CONG-20-CHUA-CO-CONG`; một packet cho `INV-28-TRAN-KICH-THUOC` cùng `INV-16-BO-DEM-NGOAI-TRUC-LOI-GOI`; một packet đo cho `INV-03`.")

# --- Mục 16: D12 viết lại, thêm D17
i = s.index("| D12 | tiền kiểm lease là chuỗi phép đo fail-closed")
j = s.index("\n", i)
s = s[:i] + (
    "| D12 | điều kiện cấp lease chỉ chạy công cụ đã có trên base (so tập cặp ref, `git ls-tree` cho policy, `ai-dang-giu` "
    "cho từng đường dẫn, đo lại sau khi đăng) và khai giới hạn G1 đến G10; wp1466 không dựng công cụ tiền kiểm riêng | "
    "quyết định E2 ở https://github.com/ducthangho/tra-luat/issues/1466#issuecomment-7058057029. Lịch sử: r5 đến r7 dựng "
    "một khối tiền kiểm và mở rộng nó qua ba revision, mỗi lượt review 5 đến 7 vẫn tìm ra biểu hiện mới ở một biên khác "
    "(F11.d nguồn ref; F11.e, F11.f policy và đường nạp; F11.g, F11.h, F11.i đối số, tiến trình cha, giao thức tên). Phần "
    "còn thiếu là nợ có tên, có Issue kế nhiệm #1484 |") + s[j:]
thay("| D16 | người soạn từ r5 là Claude Opus 5.5; reviewer và executor không đổi | quyết định E2 ghi hộ ở đầu tệp |\n",
     "| D16 | người soạn từ r5 là Claude Opus 5.5; reviewer và executor không đổi | quyết định E2 ghi hộ ở đầu tệp |\n"
     "| D17 | nợ của #1484 dùng tên đã có `INV-02-TIEN-KIEM-CAP-LEASE-KHONG-CLOSURE`, không đặt tên mới; mối nối tới #1484 nằm ở "
     "mục 0, mục 1 và mục 14 của đặc tả, không nằm trong văn bản ADR | tên ấy đã nằm trong khối `adr` (mục *Nợ*) và trong ô "
     "`còn nợ` của dòng `INV-02`, thuộc đơn vị khoá `K01`. Đổi tên hay thêm \"Giao cho Issue #1484\" vào ADR sẽ đổi khối `adr`, "
     "tệp ADR của nguyên mẫu, và với tên mới thì cả băm của `K01`, tức chạm phần review đã xếp ĐÃ VÁ THẬT. Văn bản nợ hiện "
     "có (\"trước khi cấp lease chỉ có `ai-dang-giu`, so chuỗi đường dẫn bằng nhau; I2(Đ) chỉ chạy trên lease ĐÃ đăng; kho "
     "chưa có phép tính closure nào của §5\") đã đúng với điều kiện bắt đầu của r8 |\n")

# --- Mục 17
thay("Đã quyết, không còn là câu hỏi: tách ba packet (E2) và nhánh nhận của chuỗi (E5), hai URL ở mục 0; đổi người soạn từ r5 (E2), URL ở đầu tệp. Revision 5, 6 và 7 không có câu hỏi mới. Ở r7, đòi hỏi PyYAML phải nằm trong site-packages của chính trình thông dịch là điều kiện vận hành cho người cấp lease, không phải câu hỏi E. Nó không đổi thẩm quyền, và có lối ra không cần chủ kho: dùng một trình thông dịch như thế (S17). Ba quyết định thiết kế của r5 (ngữ pháp đóng của N8, khối tiền kiểm, cách nhận dạng hiển thị của chốt ID) không gắn được mã E nào: chúng không thiếu tài nguyên, không đảo quyết định nào của chủ kho, không đổi thẩm quyền ngoài phạm vi E5 đã khai ở mục 12. Người soạn tự quyết và ghi lý do ở mục 16 (D9, D12, D5).",
     "Đã quyết, không còn là câu hỏi: tách ba packet (E2) và nhánh nhận của chuỗi (E5), hai URL ở mục 0; đổi người soạn từ r5 (E2), URL ở đầu tệp; tách khối tiền kiểm sang #1484 (E2), URL ở mục 0. Revision 5 đến 8 không có câu hỏi mới. Hai quyết định thiết kế của r5 còn lại trong đặc tả (ngữ pháp đóng của N8, cách nhận dạng hiển thị của chốt ID) không gắn được mã E nào: chúng không thiếu tài nguyên, không đảo quyết định nào của chủ kho, không đổi thẩm quyền ngoài phạm vi E5 đã khai ở mục 12. Người soạn tự quyết và ghi lý do ở mục 16 (D9, D5). Quyết định thứ ba của r5, khối tiền kiểm, đã rút theo E2 (D12).")

# --- Mục 18
thay("`sc/tien_kiem.py` (khối `tien-kiem` r6, trùng từng byte với khối trong tệp này, sha256",
     "`sc/tien_kiem.py` (khối `tien-kiem` r6, trùng từng byte với khối của đặc tả r6, sha256")
thay("`sc/tien_kiem.py` (khối `tien-kiem` r7, trùng từng byte với khối trong tệp này)",
     "`sc/tien_kiem.py` (khối `tien-kiem` r7, trùng từng byte với khối của đặc tả r7 `3c89d87`)")
a = s.index("- Răng của khối `tien-kiem` r7, chạy bằng `/usr/bin/python3`")
b = s.index("- Chốt ID không bắt chữ cùng hình thuộc hệ chữ khác")
assert s.count("- Răng của khối `tien-kiem` r7") == 1 and a < b
doan = s[a:b]
for dau in ("- Răng của khối `tien-kiem` r6", "- Răng của khối `tien-kiem` r5", "- Khối `tien-kiem` chưa chạy được tới ĐẠT",
            "- Bốn hàm quét lease mà khối `tien-kiem` gọi", "- Giới hạn của `I-NGUON`"):
    assert doan.count(dau) == 1, dau
s = s[:a] + (
    "- Khối `tien-kiem` của r5 đến r7 và mọi số đo răng của nó (r5: 19 kịch bản; r6: 33 kịch bản, 3 đột biến; r7: 54 kịch "
    "bản, 14 đột biến; các phản chứng của review lượt 5 và 6 chạy lại) đã rút ở r8. Hồ sơ nằm ở các thư mục hiện vật nêu "
    "trên và ở đặc tả r7 (`3c89d87`). Chúng là dữ liệu đầu vào cho Issue #1484, không phải bằng chứng hay lời khai của wp1466.\n"
    "- Hiện vật của r8 nằm ở `/tmp/claude-0/-home-user-tra-luat/1428173d-f5d8-5c81-a6c4-b24675398aaa/scratchpad/r8`, ngoài "
    "kho: `sc/muc1_buoc3.md` (bước 3 và bảng G1 đến G10 của mục 1), `sc/sua_r8.py` (bộ dựng r8 từ r7, mỗi phép thay đòi đúng "
    "một lần xuất hiện), `sc/do_that_r8.sh` và log `do/do_that_r8.log` (S18), `do/issue_*.json` (REST GET ba Issue), "
    "`do/grep_r8.log` (phép rà lời hứa, mục 19). Clone đo thật là `kho/`. Nguyên mẫu mã không đổi ở r8: nhánh `proto` của "
    "cây r5 vẫn ở `c35ee0399f529d1f45c7fdc3eedbec2872e9843a`.\n"
    "- Điều kiện bắt đầu 3a đến 3e chưa chạy tới kết quả cho phép cấp lease trên kho thật: 3c ra người giữ B4 (S18). Kết "
    "quả ấy chỉ có được lúc cấp lease, sau khi B4 land và lease của nó được thu hồi. Giới hạn G1 đến G10 của mục 1: wp1466 "
    "không đo, vì chúng là nợ của Issue #1484.\n") + s[b:]

# --- Mục 19
thay("lượt 6 trên r6 (`6c4ffe9`, verdict `ops/specs/wp1466/review/r6-l6/VERDICT.md`, sha256 `2a059046…`).",
     "lượt 6 trên r6 (`6c4ffe9`, verdict `ops/specs/wp1466/review/r6-l6/VERDICT.md`, sha256 `2a059046…`), lượt 7 trên r7 "
     "(`3c89d87`, verdict `ops/specs/wp1466/review/r7-l7/VERDICT.md`, sha256 `082db6d7…`).")
i = s.index("| `tien-kiem-lease-chua-du` · P2 | mới → VÁ HỜ → còn mở → VÁ HỜ")
j = s.index("\n", i)
s = s[:i] + (
    "| `tien-kiem-lease-chua-du` · P2 | mới → VÁ HỜ → còn mở → VÁ HỜ; lượt 5, 6, 7 đều VÁ HỜ (mục 0) | r8: không còn gì. "
    "wp1466 không hứa tiền kiểm; điều kiện bắt đầu 3a đến 3e chỉ chạy công cụ sẵn có và khai giới hạn G1 đến G10 (mục 1). "
    "r5 đến r7 từng đo lớp này bằng một khối tiền kiểm, đã rút ở r8 | toàn bộ lớp, gồm F11.b đến F11.i và G1 đến G10: "
    "#1484 · `INV-02-TIEN-KIEM-CAP-LEASE-KHONG-CLOSURE`. Thẩm quyền: quyết định E2 tách khối (mục 0). Theo §8.3, việc "
    "chuyển này KHÔNG được tính là vá | ĐẠT trên kho thật của 3a đến 3e: chỉ đo được lúc cấp lease |") + s[j:]
thay("Chưa đo: ĐẠT trên kho thật, chỉ đo được lúc cấp lease.\n\nKhông finding nào của sáu lượt bị người soạn bác.",
     "Chưa đo: ĐẠT trên kho thật, chỉ đo được lúc cấp lease.\n\n"
     "**Lượt 7 (r7 `3c89d87`) và r8.** Nhãn của lượt 7: `tien-kiem-lease-chua-du` VÁ HỜ (F11.e ĐÃ VÁ THẬT; các đường "
     "PyYAML cụ thể của F11.f đã đóng nhưng F11.f vẫn VÁ HỜ; F11.g, F11.h, F11.i mới trong cùng lớp); bốn nhóm bảng (ii) "
     "CHƯA VÁ, đúng như đã chuyển sang #1469 và #1470; các lớp đã đóng trước r7 được giữ. Hội tụ r6→r7 là 0/1: U là 1, F là "
     "0. Không lớp mới, không lớp tái mở. Lớp ấy có mặt ở cả bảy lượt; lượt 7 là lần thứ bảy. Lịch sử của nó: mới → VÁ HỜ → "
     "còn mở → VÁ HỜ → VÁ HỜ → VÁ HỜ → VÁ HỜ. Hai chuyển tiếp liên tiếp r5→r6 và r6→r7 đều 0/1, dưới 50%. Checkpoint trước "
     "r7 là mục sổ `xet_lai_cach_lam` ở https://github.com/ducthangho/tra-luat/issues/1466#issuecomment-7057370281; câu trả "
     "lời cho checkpoint sau lượt 7 là quyết định E2 của chủ kho ở "
     "https://github.com/ducthangho/tra-luat/issues/1466#issuecomment-7058057029: \"Tách khối ra (Recommended)\". r8 làm "
     "đúng quyết định ấy (mục 0): rút khối tiền kiểm, chỉ giữ công cụ sẵn có làm điều kiện cấp lease, khai giới hạn G1 "
     "đến G10, và chuyển lớp sang bảng (ii) với nợ `INV-02-TIEN-KIEM-CAP-LEASE-KHONG-CLOSURE` của Issue #1484. Theo "
     "protocol §8.3, chuyển biểu hiện ra ngoài phạm vi KHÔNG được tính là vá: r8 không xin xếp lớp này ĐÃ VÁ THẬT, và nếu "
     "lượt 8 tính hội tụ r7→r8 thì lớp ấy không vào F. Nhãn của lớp ở lượt 8 do reviewer đặt. Phép rà \"không còn lời hứa\" "
     "của r8 (lệnh và output ở `r8/do/grep_r8.log`, mục 18): mọi câu còn nhắc khối, `I-NGUON`, \"fail-closed\" hay \"đóng\" "
     "trong phạm vi tiền kiểm đều là lịch sử của r5 đến r7 hoặc là lời khai giới hạn.\n\n"
     "Không finding nào của bảy lượt bị người soạn bác.")
thay("Thước tiến triển mà mục sổ checkpoint thứ hai đã chọn là số lớp mở ở bảng (i): 13 → 9 → 3 → 1 → 1, và r7 nhắm 0.",
     "Thước tiến triển mà mục sổ checkpoint thứ hai đã chọn là số lớp mở ở bảng (i): 13 → 9 → 3 → 1 → 1 → 1. Ở r8 thước "
     "ấy có thể về 0, nhưng con số 0 ấy đến từ việc chuyển phạm vi theo E2, không đến từ vá; theo §8.3 nó không được đọc "
     "thành tiến triển của vá.")

# --- điền kích thước (số byte lặp tới điểm bất động; số dòng = số LF, như `wc -l`)
s = s.replace("{{DONG}}", str(s.count("\n")))
nb = 0
for _ in range(10):
    t = s.replace("{{BYTE}}", str(nb))
    if len(t.encode("utf-8")) == nb:
        break
    nb = len(t.encode("utf-8"))
s = t
nd = s.count("\n")
assert f"r8 là {nd} dòng, {len(s.encode('utf-8'))} byte" in s, (nd, len(s.encode('utf-8')))
SPEC.write_bytes(s.encode("utf-8"))
print("ghi", SPEC, nd, "dòng", len(s.encode("utf-8")), "byte", hashlib.sha256(s.encode("utf-8")).hexdigest())
