# wp1463 r1 — PR2 của kế hoạch nguồn r3/r4: chế độ nhẹ theo diff cho `ops/ci_provenance_test.py` trong registry, kèm chốt A+3 (CI-PROVENANCE-NHE-THEO-DIFF)
packet_id: wp1463
revision: 1
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab
tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544

Trạng thái: `proposed`, ứng viên đóng băng revision 1, CHƯA review, CHƯA có băm được duyệt, CHƯA có lease. Đặc tả chỉ có hiệu lực khi review đặc tả Codex không còn finding P0–P3, chủ kho duyệt băm của nó và một Mission revision cài nó (Mission r85 `r85_constraints`: "Each new packet needs its own frozen spec with the owner's hash approval before any lease").

## Định danh và nguồn
- `packet_id`: `wp1463` · `packet_issue`: #1463 (`[Packet proposed][Mission1172] PR2 — Chế độ nhẹ theo diff cho ci_provenance_test trong registry`).
- `nguon_cap_viec`: kế hoạch nguồn r3 §5 mục "PR2 — Chế độ nhẹ theo diff cho `ci_provenance_test` trong registry" (`ops/specs/wp1172-source-plan-r3/KE_HOACH_NGUON_R3.md` trên nhánh `ops/wp1172-plan-r3`, sha256 `2e9fb13f1ab3f299c2d2dc1e5a6e407ff0aadb8aee1f6ffd00d88fc02b146f89`, dòng 184–203 lúc đo) cộng chốt A+3 của kế hoạch nguồn r4 §4 (`ops/specs/wp1172-source-plan-r4/KE_HOACH_NGUON_R4.md` trên nhánh `ops/wp1172-plan-r4`, sha256 `0f287ce4369fbeb7b1939daa8de5db7c27c2a4efdc1a21f2fccdd37dc9d83fbe`, gạch đầu dòng "A+3 (PR2, PR5, B1)", dòng 208–215 lúc đo). "§…" không ghi nguồn là mục của r4; "r3 §…" là của r3. Nơi đặc tả này và kế hoạch khác chữ thì đặc tả này thắng cho packet này, và mọi chỗ khác chữ được liệt kê ở mục "Chỗ khác chữ kế hoạch".
- Thẩm quyền: Mission #1172 r85 (vai PR2 `admitted_spec_drafting`, `envelope.provider_budgets.per_new_packet`), Mission r95 (`source_plan_sha256` = `0f287ce4…`, `packet_graph` vai PR2: write set dự kiến `ops/ci_provenance_test.py`, `.claude/dev/ci_dang_ky_test.py`, `ops/specs/<pr2>/`; "after B1 (shared ci_dang_ky_test.py); Q3 decided in r84"). Quyết định chủ kho Q3 (Mission r84 `owner_decisions.Q3`): "Follow the existing NHE rule (push also light by diff) for the PR2 suite."
- Base lúc soạn: `origin/master` = `e2f28fb39c519511a61d1fdba5b1fc8f77bb76b8` (đo 2026-11-21 16:5xZ, PR1 #1448 đã land tại đây). Blob tại base: `.claude/dev/ci_dang_ky_test.py` `7b120b5fcce03c46b5dc22448251b4e65dcc198c` · `ops/ci_provenance_test.py` `21b23dbcdbab903bc840df70f95f7882a741118a` · `ops/ci_provenance.py` `086f416921c3df1b2e81d95f509e04c6a9d573ae` · `.github/workflows/ci.yml` `a1db88d9433fd548e36dcd598a63135f5fac7b73` · `ops/ci_duong_nhanh.py` `99aa3d9ff0180a54eea711b1724e549f98c70b0a`. Base thi công đo lại khi cấp lease; mọi con số ở đây là số TẠI base lúc soạn, hợp đồng neo vào bất biến chứ không vào con số.
- `review_class`: `sensitive`. Lý do: packet NỚI một cổng CI (bỏ vòng đột biến của một bộ trong `gate-registry` khi diff không chạm vùng) và sửa `.claude/dev/ci_dang_ky_test.py` (bộ chọn của registry); Mission rủi ro `sensitive`. Không rõ thì lấy mức chặt nhất, nên không hạ.

## Mục tiêu
Lượt `ci.yml` mà diff KHÔNG chạm vùng của `ops/ci_provenance_test.py` thì registry chạy bộ ấy ở chế độ NHẸ: mọi ca nền và tự kiểm phân hạng `TU_KIEM` vẫn chạy, chỉ vòng đột biến bị bỏ. Diff chạm vùng, diff không đo được, sự kiện không phải `push`/`pull_request` (gồm lượt `ci-dot-bien-du.yml`) ⇒ chạy ĐỦ như hôm nay. Kèm A+3: bộ in kết cục theo tầng, không gộp.

1. Cờ nhẹ mới của bộ và hành vi nhẹ — `ops/ci_provenance_test.py`.
2. Khối dòng kết luận của chế độ nhẹ, tách khỏi khối đủ — `ops/ci_provenance_test.py`.
3. Đưa bộ vào cơ chế `NHE` sẵn có với vùng ĐÓNG BĂNG ở mục 3 Hợp đồng — `.claude/dev/ci_dang_ky_test.py` (chỉ dữ liệu).
4. Kết cục A+3 theo tầng — `ops/ci_provenance_test.py`.
5. Ca hai chiều và đột biến riêng cho mọi chốt mới, kể cả chốt nằm ở dữ liệu registry — `ops/ci_provenance_test.py`.
6. Bằng chứng đo trước merge (A/B, vùng, thời gian) — `ops/specs/wp1463-r1/do/do_pr2.py` và `ops/specs/wp1463-r1/do/KET_QUA.md`.

## Hợp đồng

### 1. Cờ nhẹ (bên sản xuất: `ops/ci_provenance_test.py`)
- Tên biến môi trường: `CI_PROVENANCE_KHONG_DOT_BIEN` (hằng trong mã).
- Miền, so khớp TOÀN chuỗi theo byte, không cắt khoảng trắng, không đổi hoa thường: giá trị ĐÚNG bằng `1` ⇒ chế độ `nhe`. Biến vắng ⇒ `day_du`. MỌI giá trị khác (rỗng, `0`, ` 1`, `1 `, `1\n`, `01`, `true`, `TRUE`, chữ số Unicode như `１`) ⇒ `day_du` (fail-closed về phía chạy đủ, r3 I3). Không có trạng thái thứ ba: giá trị lạ không làm bộ đỏ, nó chỉ làm bộ chạy đủ.
- Cờ chỉ được đọc MỘT lần, ở nhánh chạy không đối số của `main` (nhánh registry gọi). Các nhánh `--mot-ca`, `--tat-ca-ca`, `--dot-bien-dong` không đổi hành vi theo cờ.
- Dòng thứ hai của đầu ra, ngay sau `TIEN TRINH: n`, là đúng `CHE DO: nhe` hoặc `CHE DO: day_du`, theo chế độ đã chọn.

### 2. Hành vi và khối dòng kết luận
- **`day_du`:** hành vi và bốn dòng cuối GIỮ NGUYÊN như base (đầu ra chỉ thêm hai dòng mới `CHE DO:` của mục 1 và `KET_CUC_A3:` của mục 4, cả hai đứng TRƯỚC bốn dòng cuối): `CA: N/N dat` · `DOT BIEN: g/M bi giet dung ly do` · `TU KIEM PHAN HANG: <DAT|DO> (k dot bien)` · `TONG: <DAT|DO>`, mã thoát 0 khi `TONG: DAT`, 1 khi `TONG: DO`. `M` là số việc trong kế hoạch đột biến (mọi mục đột biến các loại mà lượt đủ chạy, gồm các mục mới của mục 5), `g` là số việc có hạng `GIET`.
- **`nhe`:** chạy MỌI ca của `CA` đúng như `day_du`; chạy `TU_KIEM` đúng như `day_du` (kể cả lượt bản gốc của chính ca đích của `TU_KIEM`); KHÔNG chạy việc nào của kế hoạch đột biến và không gọi lượt làm nóng của vòng đột biến (`lam_nong_nen` tại base), tức không tiến trình con nào được sinh cho kế hoạch ấy. Bốn dòng cuối, theo đúng thứ tự, liền nhau, là bốn dòng cuối cùng của đầu ra:
  `CA: N/N dat` · `DOT BIEN: M muc CHE DO NHE — do khi diff cham vung` · `TU KIEM PHAN HANG: <DAT|DO> (k dot bien)` · `TONG: <DAT|DO>`, với `M` là số việc của CHÍNH kế hoạch mà lượt `day_du` sẽ chạy (cùng nguồn, không đếm lại bằng tay). `TONG: DAT` (mã thoát 0) khi và chỉ khi `ket_luan_tong` của mục 4 là `xanh`.
- Ở CẢ HAI chế độ, chế độ `nhe` không bao giờ in một dòng khớp `^DOT BIEN: \d+/\d+ bi giet` và chế độ `day_du` không bao giờ in dòng `CHE DO NHE`.
- Các dòng kết luận được dựng bởi MỘT hàm thuần (đầu vào: chế độ, số ca đạt/tổng, `g`, `M`, kết quả `TU_KIEM`, `ket_luan_tong`), và nhánh chạy không đối số của `main` dùng đúng hàm ấy. Quyết định "chạy những gì" theo chế độ nằm ở MỘT hàm nhận bộ chạy ca, bộ chạy vòng đột biến và bộ chạy `TU_KIEM` làm tham số, để ca test gọi nó với bộ chạy giả đếm lời gọi (không ca nào được gọi `main` không đối số trong tiến trình, vì `main` chạy lại mọi ca).

### 3. Đưa bộ vào `NHE` (bên chọn: `.claude/dev/ci_dang_ky_test.py`, CHỈ dữ liệu)
Đúng bốn thay đổi dữ liệu, không thay đổi logic nào của tệp này (không sửa `ke_hoach`, `env_theo_che_do`, `chay_moi`, `doc_diff`, `_cham_vung`, `MOI`, `VUNG_CHUNG`, `TIEN_TO_CHUNG`, `TIEN_TO_THEM`, `GOC_TAI_LIEU`, `ENV_REGISTRY`, `BAM_GATE_REGISTRY`; không sửa `.github/workflows/ci.yml`):
- `NHE["ops/ci_provenance_test.py"] = {"CI_PROVENANCE_KHONG_DOT_BIEN": "1"}`.
- `MAU_DAY_DU["ops/ci_provenance_test.py"]` = CHÍNH chuỗi `MOI["ops/ci_provenance_test.py"]` hiện có (tham chiếu, không chép lại một chuỗi thứ hai).
- `MAU_NHE["ops/ci_provenance_test.py"]` = đúng chuỗi sau (raw string Python):
  `r"(?ms)\A(?!.*^(?:TONG|TU KIEM PHAN HANG): DO\b).*^CA: ([1-9]\d*)/(\1) dat\nDOT BIEN: [1-9]\d* muc CHE DO NHE — do khi diff cham vung\nTU KIEM PHAN HANG: DAT \(\d+ dot bien\)\nTONG: DAT\n?\Z"`
- `VUNG_THEM["ops/ci_provenance_test.py"] = (".claude/dev/ci_dang_ky_test.py", ".github/workflows/ops-do-workflow-definition.yml", "ops/bash_nen.py")`.

**Vùng của bộ (đóng băng; oracle độc lập với mã registry).** Với tập đường dẫn đổi `doi` (kết quả của `doc_diff` sẵn có):
```python
Z = frozenset({"ops/ci_provenance_test.py", "ops/ci_provenance.py", ".github/workflows/ci.yml", "requirements.txt",
               ".claude/dev/ci_dang_ky_test.py", ".github/workflows/ops-do-workflow-definition.yml", "ops/bash_nen.py"})
GOC = frozenset({"AGENTS.md", "CHANGELOG.md", "CLAUDE.md", "CONTEXT.md", "INSTALL.md", "README.md", "SKILL.md"})

def oracle(doi):
    if doi is None:
        return "day_du"
    for x in doi:
        if x in Z or x.startswith("ops/cai_") or x.startswith("ops/cong_cu") or ("/" not in x and x not in GOC):
            return "day_du"
    return "nhe"
```
Vì sao từng phần tử ngoài cặp bộ/đích và `VUNG_CHUNG`: `ops/ci_provenance.py` nạp `.claude/dev/ci_dang_ky_test.py` (sổ `MOI`) bằng `importlib`, và ca của bộ dựng sổ tạm từ chính tệp ấy (`moi_tam`); ca của bộ đọc `.github/workflows/ops-do-workflow-definition.yml` thật (`WF_WD_TEP`); ca của bộ nạp `ops/bash_nen.py` (`__import__("bash_nen")`). Đo bằng audit hook `open` (mục "Số đo"). Hai tiền tố và luật tệp gốc là luật SẴN CÓ của `_cham_vung`, giữ nguyên. Hệ quả có chủ ý: mọi PR sửa `.claude/dev/ci_dang_ky_test.py` (B1, B2, B1b, chính PR2) chạy bộ này ĐỦ.

**Bảng fixture vùng (đóng băng, 23 hàng).** Mỗi hàng `tên · doi · kỳ vọng`; `null` = không đo được. Executor chép NGUYÊN bảng vào ca test; ca so `ke_hoach(doi)["ops/ci_provenance_test.py"][0]` của registry THẬT với cột kỳ vọng ở MỌI hàng, và so `oracle` (chép nguyên khối mã trên vào tệp test, không đọc hằng của registry) với cùng cột.

| tên | doi | kỳ vọng |
|---|---|---|
| khong_do_duoc | null | day_du |
| rong | [] | nhe |
| bo | ["ops/ci_provenance_test.py"] | day_du |
| dich | ["ops/ci_provenance.py"] | day_du |
| ci_yml | [".github/workflows/ci.yml"] | day_du |
| requirements | ["requirements.txt"] | day_du |
| bo_chon | [".claude/dev/ci_dang_ky_test.py"] | day_du |
| wf_wd | [".github/workflows/ops-do-workflow-definition.yml"] | day_du |
| bash_nen | ["ops/bash_nen.py"] | day_du |
| cai_cong_cu | ["ops/cai_cong_cu.sh"] | day_du |
| cong_cu_yaml | ["ops/cong_cu.yaml"] | day_du |
| goc_la | ["pyproject.toml"] | day_du |
| goc_ten_bo | ["ci_provenance.py"] | day_du |
| goc_tai_lieu | ["README.md", "CLAUDE.md", "CHANGELOG.md"] | nhe |
| tai_lieu | ["docs/x.md"] | nhe |
| spec_ho_so | ["ops/specs/wp1463-r1/SPEC.md", "ops/land/x.yaml"] | nhe |
| ops_khac | ["ops/ci_duong_nhanh.py", "ops/cong_cu_test.py"] | day_du |
| ops_khac_nhe | ["ops/ci_duong_nhanh.py", "ops/nhanh_don_duoc_test.py"] | nhe |
| gan_dung_hau_to | ["ops/ci_provenance.pyi", "ops/ci_provenance_test.py.bak", "ops/bash_nen.py~"] | nhe |
| gan_dung_thu_muc | ["x/ops/ci_provenance.py", "ops/ci_provenance/x.py", ".claude/dev/ci_dang_ky_test.pyc"] | nhe |
| workflow_khac | [".github/workflows/ci-dot-bien-du.yml", ".github/workflows/khac.yml"] | nhe |
| dev_khac | [".claude/dev/packet_loop.py", ".claude/settings.json"] | nhe |
| hon_hop | ["docs/x.md", "ops/bash_nen.py"] | day_du |

Hàng `ops_khac` ra `day_du` vì tiền tố sẵn có `ops/cong_cu` khớp cả `ops/cong_cu_test.py`; đó là hành vi bảo thủ hiện hành, PR2 không đổi. Dạng băm kiểm chép đúng: nối mỗi hàng thành `tên\t<json.dumps(doi)>\tkỳ vọng\n` (`doi` là danh sách theo thứ tự cột, `None` cho `null`, `json.dumps` mặc định) theo thứ tự bảng; sha256 của chuỗi UTF-8 ấy là `b0dd2b59cbf623c3abea7ee971b591d9ac39fc0d84bac52958bbe37a98b1f96a`.

Push (Q3): bộ đi đúng luật `NHE` hiện có, tức lượt `push` cũng chọn nhẹ theo diff qua `doc_diff` sẵn có (gốc phải là tổ tiên của đầu, không thì `day_du`). Lượt `ci-dot-bien-du.yml` không đặt biến diff nên `doc_diff` trả `None` ⇒ `day_du` (chốt `loi_workflow_dot_bien_du` sẵn có). Đây là ngoại lệ (b) của r3 I5, không rộng hơn.

### 4. Kết cục A+3 (bên sản xuất: `ops/ci_provenance_test.py`)
Ở CẢ HAI chế độ, nhánh chạy không đối số in ĐÚNG MỘT dòng `KET_CUC_A3: <json>` đứng NGAY TRƯỚC dòng `CA:` (bốn dòng cuối vẫn liền nhau và là bốn dòng cuối). `<json>` là `json.dumps(..., ensure_ascii=False, sort_keys=True, separators=(",", ":"))` của một object có ĐÚNG các khoá:
- `schema`: `"ket_cuc_a3.v1"` · `bo`: `"ops/ci_provenance_test.py"` · `che_do`: `"day_du"` | `"nhe"` · `ke_hoach_dot_bien`: số nguyên `M` của mục 2.
- `ca`: danh sách theo thứ tự `CA`, mỗi phần tử `{"ten", "trang_thai_thuc_thi", "quan_sat_ca"}`.
- `dot_bien`: `day_du` ⇒ danh sách theo thứ tự KẾ HOẠCH, mỗi phần tử `{"ten", "trang_thai_thuc_thi", "phan_hang_dot_bien"}`; `nhe` ⇒ `[]`.
- `tu_kiem`: danh sách theo thứ tự `TU_KIEM`, mỗi phần tử `{"ten", "trang_thai_thuc_thi", "dung_ky_vong"}` (`true`/`false`, `null` khi không hoàn tất).
- `ket_luan_tong`: `"xanh"` | `"do"` | `"khong_ket_luan"`.

Miền: `trang_thai_thuc_thi` ∈ {`hoan_tat`, `timed_out`, `infrastructure_error`, `cancelled`, `not_run`}; bộ này KHÔNG bao giờ phát `cancelled` (giá trị ấy dành cho bên đọc ngoài, khi job bị huỷ). `quan_sat_ca` ∈ {`passed`, `failed`, `null`}. `phan_hang_dot_bien` ∈ {`giet`, `song`, `tin_dung_gia`, `equivalent_reviewed`, `null`}.

**Bảng ánh xạ (đóng băng).**

| Nguồn | Điều kiện | `trang_thai_thuc_thi` | trường tầng hai |
|---|---|---|---|
| ca (`chay_ca`) | rc 0 | `hoan_tat` | `quan_sat_ca: passed` |
| ca | rc 3 (`TinHieuChotCa`) hoặc rc 4 (ngoại lệ vô can) | `hoan_tat` | `quan_sat_ca: failed` |
| việc đột biến | hạng `GIET` | `hoan_tat` | `giet` |
| việc đột biến | hạng `SONG_SOT`, tên KHÔNG có mục hợp lệ trong bảng tương đương | `hoan_tat` | `song` |
| việc đột biến | hạng `SONG_SOT`, tên có mục hợp lệ trong bảng tương đương | `hoan_tat` | `equivalent_reviewed` |
| việc đột biến | hạng `TIN_DUNG_GIA` | `hoan_tat` | `tin_dung_gia` |
| việc đột biến hoặc `TU_KIEM` | tiến trình con quá hạn (nhánh `QUA_HAN`, rc 124 của bộ chạy con) | `timed_out` | `null` |
| việc đột biến hoặc `TU_KIEM` | mọi kết quả khác (hạng `HONG`: bản gốc không xanh, neo sai số lần, tiền tố ca đích không khớp đúng một ca, lỗi khởi chạy) | `infrastructure_error` | `null` |
| việc của kế hoạch | không có kết quả đúng vị trí và đúng tên trong danh sách kết quả | `not_run` | `null` |
| `TU_KIEM` | hạng thật ∈ {`GIET`, `SONG_SOT`, `TIN_DUNG_GIA`} | `hoan_tat` | `dung_ky_vong` = (hạng thật == hạng mong đợi) |

Phân biệt quá hạn với lỗi hạ tầng khác phải đi bằng một trường CÓ CẤU TRÚC mà bộ chạy trả về, không bằng dò chuỗi trong phần chi tiết. Hạng `GIET` vẫn chỉ đến từ `phan_hang` sẵn có (rc 3 kèm `DO:<ca đích>:`); bảng này không đổi cách phân hạng (r3 I2).

**Bảng tương đương có xét duyệt.** Hàm tính kết cục nhận bảng `{tên: {"ly_do": str, "nguoi_xac_nhan": str}}` làm tham số; mục hợp lệ khi và chỉ khi cả hai giá trị là chuỗi khác rỗng sau khi bỏ khoảng trắng hai đầu. `equivalent_reviewed` không bao giờ được đếm là giết (không vào `g`). Tên có mục hợp lệ mà hạng là `GIET` ⇒ phân hạng `giet` VÀ lời khai tương đương sai ⇒ `ket_luan_tong` = `do`. Bảng sản xuất của bộ ở PR2 là RỖNG và có ca khẳng định nó rỗng: thêm mục vào nó cần một packet riêng (dòng `DOT BIEN: g/M` sẽ lệch khối mà `MOI` đọc).

**Luật `ket_luan_tong` (đóng băng, xét theo thứ tự, bước đầu tiên khớp quyết định).**
1. `do` nếu có ÍT NHẤT MỘT trong: ca `failed`; đột biến `song` hoặc `tin_dung_gia`; `TU_KIEM` hoàn tất mà `dung_ky_vong` sai; lời khai tương đương bị giết.
2. `khong_ket_luan` nếu có ÍT NHẤT MỘT trong: mục nào có `trang_thai_thuc_thi` khác `hoan_tat` (ca, `TU_KIEM`, và đột biến khi `day_du`); danh sách kết quả đột biến không khớp kế hoạch về tên, thứ tự hoặc số lần (`day_du`); `CA` rỗng; `DOT_BIEN` rỗng hoặc kế hoạch đột biến rỗng (`M` = 0, cả hai chế độ); `TU_KIEM` rỗng.
3. `xanh` cho mọi trường hợp còn lại.

`TONG: DAT` khi và chỉ khi `ket_luan_tong` = `xanh`; mã thoát 0 khi `xanh`, 1 khi `do` hoặc `khong_ket_luan`. Ở chế độ `day_du`, khi `CA`, `DOT_BIEN` và `TU_KIEM` khác rỗng (như ở base) và bảng tương đương rỗng, luật này cho `TONG` TRÙNG với công thức `ok` hiện có ở mọi tổ hợp kết quả ca, việc đột biến và `TU_KIEM`, nên bên đọc cũ (`MOI`) và số giết không đổi. (Luật mới chặt hơn công thức cũ ở đúng một cấu hình suy biến không có ở base: `TU_KIEM` rỗng ⇒ `khong_ket_luan`, trong khi công thức cũ cho `DAT`. Ghi ra để không ai đọc câu "trùng" rộng hơn nó.)

### 5. Chốt mới, ca hai chiều và đột biến
Theo bài học đã trả giá của B4 (lớp `b4-predicate-mutation-proof` tái diễn năm lượt khi đặc tả liệt kê ma trận), đặc tả này KHÔNG đóng băng danh sách ca hay danh sách đột biến. Nó đóng băng TẬP CHỐT dưới đây; với MỖI chốt:
- có ca HAI CHIỀU (một vế chốt phải chặn, một đối chứng khoẻ nó phải cho qua); chốt có ba kết cục thì có ca cho cả ba;
- có ít nhất MỘT đột biến riêng trong kế hoạch đột biến của lượt `day_du`, làm đúng ca của chốt ấy đỏ, phân hạng `GIET` bằng `phan_hang` sẵn có (tức bằng lớp `TinHieuChotCa` của chính ca, neo tên ca); chết vì lỗi vô can là `TIN_DUNG_GIA` và làm `TONG: DO`.

Tập chốt:
- **K1 miền cờ** (mục 1): `1` ⇒ `nhe`; vắng và mọi giá trị khác liệt kê ở mục 1 ⇒ `day_du`.
- **K2 nhẹ không chạy vòng đột biến, đủ chạy trọn** (mục 2): bộ chạy giả đếm lời gọi; `nhe` ⇒ 0 việc đột biến và 0 lượt làm nóng; `day_du` ⇒ đúng kế hoạch. Đột biến bắt buộc mang tên kế hoạch r3: **"cờ nhẹ rò sang lượt đủ"** (biến vắng mà vẫn bỏ vòng).
- **K3 nhẹ vẫn chạy mọi ca và `TU_KIEM`** (mục 2). Đột biến bắt buộc: **"cờ nhẹ bỏ luôn tự kiểm phân hạng"**; và một đột biến bỏ ca ở chế độ nhẹ.
- **K4 khối dòng kết luận** (mục 2): đầu ra của hàm dựng dòng cho `nhe` được `MAU_NHE` của registry THẬT chấp nhận và bị `MOI` của registry THẬT từ chối; đầu ra cho `day_du` ngược lại. Ca gọi `chay_moi` THẬT của registry với bộ chạy giả trả đầu ra ấy và kế hoạch tương ứng: (nhẹ, khối nhẹ) ⇒ `ĐẠT`; (nhẹ, khối đủ) ⇒ `ĐỎ` "chế độ nhẹ mà VẪN in dòng đột biến ĐỦ"; (đủ, khối nhẹ) ⇒ `ĐỎ`; (đủ, khối đủ) ⇒ `ĐẠT`; khối nhẹ với `M` = 0, với `CA` thiếu một, với `TU KIEM PHAN HANG: DO` ⇒ `ĐỎ`.
- **K5 kết cục A+3** (mục 4): mỗi hàng của bảng ánh xạ và mỗi bước của luật `ket_luan_tong` có vế chặn và đối chứng; `TONG` ⇔ `xanh`. Fixture bắt buộc theo §4 A+3: nền khoẻ · giết đúng đích · tín dụng giả · tương đương có xét duyệt (mục hợp lệ ⇒ `equivalent_reviewed`, không đếm giết; mục thiếu `nguoi_xac_nhan` ⇒ `song`; mục hợp lệ mà bị giết ⇒ `do`) · quá hạn ⇒ `timed_out` và `khong_ket_luan` · hạ tầng ⇒ `infrastructure_error` và `khong_ket_luan` · thiếu kết quả ⇒ `not_run`. Fixture "ca không đích sống sót" của §4 KHÔNG áp cho bộ này: mỗi việc đột biến của bộ chỉ chạy ĐÚNG ca đích của nó, nên không có quan sát nào về ca không đích (ghi ở mục "Chỗ khác chữ kế hoạch"). Kèm ca khẳng định bảng tương đương sản xuất rỗng.
- **K6 dữ liệu registry** (mục 3): bảng fixture vùng 23 hàng so với `ke_hoach` THẬT; `env_theo_che_do` THẬT cho bộ: `nhe` ⇒ đặt `CI_PROVENANCE_KHONG_DOT_BIEN=1`, `day_du` ⇒ GỠ khoá (giá trị `None`) dù môi trường cha có. Đột biến bắt buộc, mỗi cái một đột biến riêng: **"vùng thiếu tệp đích"** (bỏ phần dẫn xuất `ops/ci_provenance.py` khỏi vùng); bỏ từng phần tử của `VUNG_THEM` của bộ (ba đột biến); bỏ bộ khỏi vùng của chính nó; xoá mục `NHE` của bộ; xoá mục `MAU_NHE` của bộ. Ca của K4/K6 phải biến MỌI lệch của registry, kể cả khoá vắng (`ke_hoach` không có bộ, `MAU_NHE` không có bộ), thành tín hiệu chốt của ca (`bang`), không để nó thành ngoại lệ vô can; nếu không, đột biến xoá khoá chỉ được `TIN_DUNG_GIA` và `TONG: DO`.

**Đột biến trên dữ liệu và mã registry.** Đột biến của K4/K6 sửa `.claude/dev/ci_dang_ky_test.py`, nên chạy trên BẢN SAO TẠM của tệp ấy: ca đích nạp bản sao qua một biến môi trường riêng (cùng kiểu `CI_PROVENANCE_MA` hiện có), tên tệp tạm riêng từng đột biến, tắt bytecode; cùng `phan_hang`, cùng đòi ca đích XANH trên bản gốc trước. Không đột biến nào ghi vào tệp thật. Các việc ấy nằm trong kế hoạch đột biến của lượt `day_du` (được đếm vào `M`) và ánh xạ A+3 như mọi việc khác.

**Không có đột biến tương đương nào được khai** ở PR2: mọi việc của kế hoạch phải ra `GIET`. Một đột biến của một chốt mà không ca nào giết được là dấu hiệu chốt ấy không có thật; executor đổi DẠNG đột biến (vẫn nhắm đúng chốt) chứ không khai tương đương và không xoá chốt. Không yêu cầu nào ở đây đòi một đột biến phải SỐNG.

Việc bộ ca và bộ đột biến có ĐỦ cho K1–K6 hay không được thẩm định ở REVIEW MÃ trên đúng H, bằng CHẠY; chốt thiếu ca hai chiều, thiếu đột biến riêng, hoặc chỉ có tín dụng giả là finding của review mã. Đặc tả không cam kết trước một con số ca hay đột biến.

### 6. Bất biến (cưỡng chế bằng Nghiệm thu)
- **I-a (r3 I1, I2).** Không sửa, xoá hay đổi tên mục nào của `DOT_BIEN`, `DOT_BIEN_TEST`, `TU_KIEM` đang có; không đổi `phan_hang`; không đổi cách lượt `ci-dot-bien-du.yml` chạy bộ (vẫn đủ). Kế hoạch đột biến chỉ được THÊM mục.
- **I-b (r3 I4).** Lượt nhẹ vẫn khởi động, chạy mọi ca và `TU_KIEM`, và in dấu hiệu dương nói nó KHÔNG đo vòng đột biến (`CHE DO: nhe` và dòng `CHE DO NHE`).
- **I-c (bên đọc cũ).** Đầu ra `day_du` của H được mẫu `MOI["ops/ci_provenance_test.py"]` của BASE chấp nhận; đầu ra `nhe` bị mẫu ấy từ chối.
- **I-d (r3 I6).** Tập tên đột biến của lượt `day_du` trên H ⊇ tập tên trên base.
- **I-e.** Không đổi `.github/workflows/ci.yml`, `.github/workflows/ci-dot-bien-du.yml`, `ops/ci_provenance.py`, `ops/ci_duong_nhanh.py`, bộ nào khác trong `NHE`.

## Nghiệm thu
Mỗi tiêu chí nêu phép đo làm nó ĐỎ. "Chạy được trên base" chỉ cần cho tiêu chí đo bất biến; tiêu chí đo hành vi mới phải ĐỎ trên base (chưa làm).

1. **Bộ xanh ở cả hai chế độ, trên H, trong môi trường đủ công cụ.** `python -B ops/ci_provenance_test.py` (biến vắng) ⇒ `TONG: DAT`, rc 0, dòng `DOT BIEN: M/M bi giet dung ly do` với `M` ≥ (số việc base) + (số đột biến mới); cùng lệnh với `CI_PROVENANCE_KHONG_DOT_BIEN=1` ⇒ khối nhẹ của mục 2, `TONG: DAT`, rc 0. Môi trường phải có `actionlint` VÀ `shellcheck` (cài bằng `bash ops/cai_cong_cu.sh shellcheck` như CI); thiếu thì ca `c61` đỏ sẵn (đo lúc soạn) và phép đo không tính. ĐỎ khi: ca nào đỏ, đột biến nào không `GIET`, hoặc khối nhẹ không đúng hình.
2. **A/B trên base và H, dựng trong MỘT lệnh** (CLAUDE.md, bài học "phép đo delta"): script `ops/specs/wp1463-r1/do/do_pr2.py`, lệnh con `ab`, dựng hai cây tạm (clone của base của lease và của H) trong cùng một lệnh, `core.abbrev 7`, chạy lượt `day_du` ở cả hai. Đạt khi: cả hai `TONG: DAT`; tập tên kế hoạch đột biến của base (đọc bằng cách nạp module base, không dò log) ⊆ tập tên `dot_bien` trong `KET_CUC_A3` của H, và mọi tên ấy có `phan_hang_dot_bien` = `giet` trên H (I-a, I-d); đầu ra `day_du` của H khớp `MOI` của base, đầu ra `nhe` của H KHÔNG khớp (I-c). Tự kiểm của bộ so: một đầu vào cố ý thiếu một tên base phải làm lệnh con ĐỎ.
3. **Registry thật đọc đầu ra thật.** Lệnh con `registry` của cùng script: lấy đầu ra THẬT của lượt nhẹ và lượt đủ trên H (không phải chuỗi tự dựng) rồi đưa vào `chay_moi` THẬT của registry trên H với bộ chạy giả trả lại đầu ra ấy: (nhẹ, kế hoạch nhẹ) ⇒ `ĐẠT`; (đủ, kế hoạch đủ) ⇒ `ĐẠT`; (đủ, kế hoạch nhẹ) ⇒ `ĐỎ`; (nhẹ, kế hoạch đủ) ⇒ `ĐỎ`. Đây là phép đo duy nhất trước merge chạy khối nhẹ THẬT qua đường registry, vì CI của chính PR2 chạy bộ ở chế độ đủ (diff chạm vùng).
4. **Vùng đủ.** Lệnh con `vung`: chạy lượt `day_du` của H với một `sitecustomize` audit hook `open` trong MỌI tiến trình Python (qua `PYTHONPATH` trỏ ra ngoài kho), ghi mọi đường dẫn mà bộ, ca và tiến trình con mở, rồi giữ phần GIAO với `git ls-files` của H (vùng chỉ nói về tệp được theo dõi; phép giao cũng loại tạo tác đã đo lúc soạn: `shutil.rmtree` trên kho git tạm mở tên tương đối bằng `dir_fd`, nên hook giải nhầm `00`…`ff`, `objects`, `refs`, `.git` về gốc kho). Đạt khi mọi tệp `x` còn lại thoả `oracle({x}) == "day_du"`, và tập ấy khác rỗng (chứa ít nhất `ops/ci_provenance.py`; rỗng ⇒ hook không chạy ⇒ ĐỎ). Một tệp ngoài vùng ⇒ ĐỎ và DỪNG (đặc tả phải sửa vùng; không tự thêm). Giới hạn khai thẳng: tiến trình KHÔNG phải Python (`bash`, `git`, `actionlint`, `shellcheck`) không bị hook đo; chúng đến từ ảnh runner và `ops/cai_*`/`ops/cong_cu*`, vốn đã trong vùng.
5. **Thời gian, cùng máy, cùng SHA H.** Lệnh con `ab` ghi thêm giây tường của lượt đủ và lượt nhẹ trên H, số luồng `TIEN TRINH`, số CPU. Báo cáo, không có ngưỡng chặn (thời gian CI thật đo sau merge, tiêu chí 10). ĐỎ khi thiếu số đo.
6. **Ca và đột biến của K1–K6** theo mục 5: chạy tiêu chí 1 là chạy chúng. Reviewer mã kiểm ĐỦ bằng cách chạy; ngoài ra mọi đột biến mới phải `GIET` (tiêu chí 1 đỏ nếu không).
7. **Bảng fixture vùng chép đúng.** Ca K6 tính lại sha256 của bảng theo dạng ở mục 3 và so với `b0dd2b59cbf623c3abea7ee971b591d9ac39fc0d84bac52958bbe37a98b1f96a`; đổi một ô ⇒ ĐỎ.
8. **Cổng kho.** `python .claude/dev/ci_dang_ky_test.py` ⇒ `TỔNG: ĐẠT` (gồm `phan_chung`; các ca sẵn có `p643-A1-chi-bo-trong-NHE`, `p647-M2-mau-nhe-chi-cho-bo-trong-NHE` đạt với bộ mới); `python -m ruff check --select F` trên hai tệp `.py` đổi và script đo: delta so base = 0; numstat trong trần (mục "Kích thước"); CI PR Ubuntu xanh trên H, trong đó log job `gate-registry` có dòng `CI_DANG_KY_KE_HOACH ops/ci_provenance_test.py: day_du — diff chạm …` và dòng `CI_DANG_KY ops/ci_provenance_test.py: ĐẠT`; K7: một lượt `ci-dot-bien-du.yml` `success` trên đúng H (diff chạm `.claude/dev/**` và `ops/**/*.py`), job registry của lượt ấy in kế hoạch `day_du` cho bộ (tức `doc_diff` không đo được, đúng mục 3).
9. **Kết quả đo ghi lại.** `ops/specs/wp1463-r1/do/KET_QUA.md` chứa đầu ra của bốn lệnh con, neo bằng sha256 của `ops/ci_provenance_test.py` và `.claude/dev/ci_dang_ky_test.py` đã chạy (tệp này nằm trong H nên KHÔNG ghi SHA hay cây của H). Mọi bản ghi cần SHA của H (biên nhận kích thước, kết quả gate trên H) nằm ở handoff §7 và Packet Issue.
10. **Sau merge (M8, không chặn merge; điều phối đo; báo `dat` / `do_khong_dat` / `khong_du_mau`, không tự hạ mục tiêu — Mission r84 Q5).** Quần thể: job `gate-registry` trên `ubuntu-latest` của `ci.yml`, kết luận `success`, attempt cuối của mỗi run, tạo trong 14 ngày kể từ lúc merge PR2, head là hậu duệ của merge commit. (a) Lượt đầu tiên trong quần thể mà kế hoạch xếp bộ `nhe`: log có `CI_DANG_KY_KE_HOACH ops/ci_provenance_test.py: nhe`, khối nhẹ và `CI_DANG_KY ops/ci_provenance_test.py: ĐẠT`; không có lượt nào như thế trong 14 ngày ⇒ `khong_du_mau`. (b) Tỷ lệ bản ghi `che_do` = `day_du` của bộ trong `CI_DANG_KY_THOI_GIAN` ≤ 30 % (mục tiêu r3). (c) Trung vị thời gian BƯỚC `test registry` (đọc `steps[]` REST của job, không đọc tổng `giay` của bộ) ≤ 600 s (mục tiêu r3). Dưới 30 job trong quần thể ⇒ `khong_du_mau` cho (b) và (c). Lượt `push` sau merge của chính PR2: đọc theo nhãn job, kế hoạch `day_du` cho bộ, dòng đủ.

## Write set
- Nhánh đặc tả `ops/wp1463-r1` (không thuộc PR giao nộp): `ops/specs/wp1463-r1/SPEC.md`, `ops/leases/wp1463-*.yaml`.
- **PR giao nộp, đúng BỐN tệp:**
  1. `ops/ci_provenance_test.py`
  2. `.claude/dev/ci_dang_ky_test.py` (chỉ bốn thay đổi dữ liệu của mục 3)
  3. `ops/specs/wp1463-r1/do/do_pr2.py` — MỘT script, bốn lệnh con `ab`, `registry`, `vung` và lệnh in kết quả; không phải `*_test.py`, không được đăng ký vào registry.
  4. `ops/specs/wp1463-r1/do/KET_QUA.md`

Không tệp thứ năm. Cần tệp thứ năm (ví dụ `ci.yml` vì `BAM_GATE_REGISTRY` buộc đổi, hay sổ `ops/ci_provenance.py`) ⇒ DỪNG theo protocol §12 và báo điều phối; đó là mâu thuẫn của đặc tả, điều phối soạn revision. Đã rà lúc soạn: thêm khoá vào `NHE` không đổi định nghĩa job `gate-registry` nên `BAM_GATE_REGISTRY` không đổi; `loi_env_registry` đòi `env` bước registry BẰNG `ENV_REGISTRY` nên cờ mới không thể đặt từ `ci.yml`; `loi_workflow_dot_bien_du` giữ lượt tuần ở `day_du`.

## Ngoài phạm vi
- `ops/cloud_agent_creds_test.py` và `ops/land_evidence_nguon_test.py` (r3 PR2 "xét cùng lúc… chỉ đưa vào nếu vùng gọn"): KHÔNG đưa vào. Lý do: write set của Issue #1463 và Mission r95 chỉ có `ops/ci_provenance_test.py`; mỗi bộ thêm vào `NHE` cần phép đo vùng riêng. Ứng viên cho packet sau.
- Mọi thay đổi `ci.yml`, `ci-dot-bien-du.yml`, `ops/ci_provenance.py`, `ops/ci_duong_nhanh.py`; logic của registry; bộ khác trong `NHE`; ép đủ ở `push` (Q3 đã chọn không ép); đọc `vars`/công tắc A+1 (PR3/B4); bên đọc A+3 ngoài bộ (PR5, B1b); `--dot-bien-dong` và tập đóng `TUONG_DUONG` của nó; mọi giá trị `CHO_PHEP`; Windows CI; LIVE.

## Chỗ khác chữ kế hoạch (để review soi)
- r3 PR2 ghi "398 đột biến" (`[B: M3.bang."ops/ci_provenance_test.py"]`); base lúc soạn có `DOT_BIEN` 398 + `DOT_BIEN_TEST` 11 (thêm ở #1322) = 409 việc trong kế hoạch của lượt đủ, cộng 2 mục `TU_KIEM`. "Vòng đột biến" mà chế độ nhẹ bỏ là CẢ kế hoạch ấy (409 việc tại base, cộng các việc mới của mục 5), không chỉ `DOT_BIEN`. Hợp đồng không neo vào con số nào.
- r3 PR2 "vùng = cặp bộ/đích + `VUNG_CHUNG` + phần đo thêm": "phần đo thêm" được đóng băng thành ba đường dẫn `VUNG_THEM` ở mục 3, có phép đo hoàn chỉnh ở Nghiệm thu 4.
- r3 PR2 "`ci.yml` chỉ khi băm `BAM_GATE_REGISTRY` buộc đổi": đã rà, không buộc đổi ⇒ `ci.yml` ra khỏi write set.
- r3 PR2 nghiệm thu "tỷ lệ `day_du` ≤ 30 %, trung vị bước registry ≤ 600 s": phụ thuộc hỗn hợp PR sau merge, executor không điều khiển được, nên thành tiêu chí SAU MERGE báo cáo (Nghiệm thu 10), không chặn merge.
- r3 PR2 "Windows: một lượt dispatch": Mission r85 `windows_ci_runs` = 0 và quy tắc thường trực không Windows CI ⇒ không có lượt Windows (mục "Quy trình và quyền").
- §4 A+3 fixture "ca không đích sống": không áp cho bộ này (K5). §4 A+3 "kiểm hai chiều: bên đọc cũ vẫn đọc được; số giết không đổi trên cùng SHA": Nghiệm thu 2 (I-c, I-d), so base với H.

## Kích thước
- Trần: trần MẶC ĐỊNH của lớp `sensitive` theo `ADR-0053` (dòng khai ở đầu tệp; ba phép đo ở mục "Số đo"): ≤ 6 tệp và ≤ 450 dòng thêm theo `git diff --numstat <base> <H>`. Đặc tả không ước lượng, không xin, không cấp ngoại lệ (Mission r86: "No spec carries an estimated size exception").
- Đối tượng bị trần là ứng viên giao nộp (H sắp đẩy hoặc sắp đưa đi review/audit). Trước MỖI lần đẩy và MỖI lần xin review, executor đo numstat trên đúng bốn tệp sau khi H đã commit và ghi biên nhận kích thước (SHA H, cây H, SHA base, numstat từng tệp) ở handoff §7 và comment trên Packet Issue #1463, không trong tệp giao nộp.
- Vượt ⇒ DỪNG TRƯỚC review theo `ADR-0044` (không đẩy, không xin review, không cắt ca, đột biến hay bằng chứng để vừa trần, không tách PR); báo điều phối kèm numstat đã đo. Điều phối xin chủ kho [E2] một khối `nang_tran` đủ bốn trường của `ADR-0053` (`ai_nang`, `can_cu` có numstat ĐÃ ĐO, `tran_cu`, `tran_moi`); khối vào một revision đặc tả chỉ thêm nó, vào Mission revision và lease.
- Không cổng máy nào canh trần này (`ADR-0044`, `ADR-0053`: 0 cổng ở §20); executor, người cấp lease và reviewer đo bằng tay.

## Quy trình và quyền
- **Thứ tự và tệp chung (chặn lease).** Plan §7: B1 → B2 → PR2 dùng chung `.claude/dev/ci_dang_ky_test.py`, xếp NỐI TIẾP. Lúc soạn: (a) lease `wp1236-a-r12-g1-claude-20261121` (packet #1236, ngoài Mission) giữ `.claude/dev/ci_dang_ky_test.py` tới `2026-11-23T13:45:00Z` (tệp lease trên nhánh `ops/wp1236-r10-a-lease`); (b) lease `wp1475-r1-g1-claude` (packet #1475 `CI-PROVENANCE-WIN-THU-LAI`, ngoài Mission) giữ `ops/ci_provenance.py` VÀ `ops/ci_provenance_test.py` tới `2026-11-23T01:57:05Z` (nhánh `ops/wp1475-r1-g1-lease`); (c) B1a (#1460) đứng trước theo thứ tự plan. Thi công PR2 chờ cả ba: (a) và (b) đã hết hạn hoặc đã thu hồi hai chiều, (c) đã land hoặc không còn lease trên tệp chung, và B2 nếu khi ấy đã có lease trên tệp chung. Trước khi cấp lease: `ai-dang-giu` trên MỌI ref (so tập tên `ls-remote --heads` với ref cục bộ trước, theo CLAUDE.md) cho bốn đường dẫn giao nộp; đo lại base; chạy lại bảng fixture vùng và các số ở mục "Số đo" trên base mới. #1475 sẽ đổi `ops/ci_provenance_test.py`: hợp đồng neo vào hành vi (cờ, khối dòng, A+3, vùng), không neo vào số dòng hay số đột biến; nếu base mới đổi bốn dòng cuối, mẫu `MOI` của bộ hoặc tập tệp mà bộ mở (Nghiệm thu 4) thì DỪNG theo protocol §12 (đặc tả mâu thuẫn), điều phối soạn revision.
- **Trước lease — ba bước tách rời.** (1) Review đặc tả Codex không còn P0–P3, chủ kho duyệt BĂM. (2) Mission revision riêng nhận #1463 vào thi công, ràng buộc revision, băm, base, write set, trần. (3) Cấp lease. Duyệt băm không tự trao quyền thi công.
- **Hai bộ đếm tách nhau.** Soạn/review ĐẶC TẢ theo Mission `per_new_packet`: tác giả 5, review đặc tả Codex 6 (revision 1 này dùng 1/5 tác giả, 0/6 review); bộ đếm này không tính vào trần lời gọi trên PR và không đặt lại khi đặc tả đổi revision. THI CÔNG: attempts 3; review mã Codex 3; connector 2; CI PR Ubuntu 3; `ci-dot-bien-du.yml` (K7) 1; CI rerun 1; Windows CI 0. Trục LỜI GỌI Codex trên PR giao nộp (`ADR-0055`, kích hoạt bằng dòng khai ở đầu tệp) đếm CHUNG review mã và connector: trần packet 10, trần Mission 3 + 2 = 5 ≤ 10 là trần dùng được. Trước MỖI lời gọi, điều phối đọc lại bộ đếm đã dùng của đúng trục; chạm trần ⇒ dừng, hỏi chủ kho [E2] kèm mức đã dùng.
- **`ADR-0060` M10.** Đặc tả này CỐ Ý KHÔNG có dòng `dieu_kien_merge: ADR-0060@…`, giống B1a r7, B4 r9, PR1 r7 cùng Mission. Có dòng ấy thì M3 của `ADR-0060` xếp Windows `required` cho diff chạm `.claude/dev/**` và đòi một lượt Windows tại chỗ, mà Mission chỉ cho chạy Windows tại chỗ ở B3. Không có dòng: K1 của `kiem-merge` chấp nhận (0 dòng); K6 vẫn xếp Windows `required` ⇒ miễn bằng dòng `windows: <H> mien` của chủ kho theo quy tắc thường trực không Windows CI; K7 vẫn áp (diff chạm vùng M9) ⇒ một lượt `ci-dot-bien-du.yml` `success` trên đúng H. Ngưỡng severity theo bảng protocol §8 (0 P0–P2; P3 đóng có bằng chứng hoặc chủ kho miễn).
- Executor: Claude Code (Fable 5.2 khi có quota; trước 2026-11-25T08:00Z là Claude Opus 5.5 theo Mission r92), phiên riêng. Reviewer: Codex service gpt-6-astra, xhigh, phiên độc lập, chỉ đọc, được cấp mirror kho đủ để đo lại (protocol §8) và môi trường có `actionlint` + `shellcheck`; reviewer CHẠY bộ ở hai chế độ và kế hoạch đột biến, thẩm định ĐỦ của ca/đột biến so với K1–K6.
- Chủ kho tự audit exact-H trước LẦN ĐẨY ĐẦU của H; điều phối không ký thay. Trước khi đẩy H: cập nhật nhánh lên `master` mới nhất, đo lại làn (Mission r82). Merge do chủ kho bấm, sau `kiem-merge` K0–K7.
- Hoàn tác: xoá bộ khỏi `NHE` (một dòng) hoặc revert PR. Không có công tắc ngoài mã.

## `luat_dung`
- Điểm dừng của protocol §12 (trần attempt, cùng lỗi hai lần, đặc tả mâu thuẫn, write set lệch), `ADR-0044`/`ADR-0053` (vượt trần kích thước ⇒ dừng trước review), `ADR-0055` (trần lời gọi Codex), §5 và §4 protocol (lease, write set). Dẫn bằng tên, không chép, không hạ ngưỡng.
- [E2] chạm một trần cứng ở mục "Quy trình và quyền" hoặc "Kích thước": báo mức đã dùng, còn thiếu bao nhiêu, để làm gì.
- [E1] một lớp finding lặp lại sau khi đã đổi thiết kế (ví dụ đột biến của một chốt không giết được dù đã đổi dạng): báo gốc rễ, các phương án đã thử, một đề xuất.
- [E3] phép đo cho thấy quyết định Q3 (push cũng nhẹ) gây hại đo được: báo quyết định, bằng chứng, hậu quả.
- Không có ngân sách mềm hay điểm hỏi nào khác.

## `pham_vi_e`
- E4: KHÔNG chạm (không Drive, GAS, `--apply`, secrets, xoá ref/tag, ruleset).
- E5: KHÔNG chạm. Packet sửa dữ liệu bộ chọn của registry CI (`.claude/dev/ci_dang_ky_test.py`) và một bộ test; không sửa mã cổng cấp lease hay cổng merge (`.claude/dev/packet_loop.py`), không sửa danh sách thẩm quyền, không sửa `ADR-0067`. Dù vậy Mission r85 vẫn đòi chủ kho duyệt băm trước lease, nên khai này không bớt bước nào.

## `hinh_dang_ke_thua`
`khong_ap_dung` theo nghĩa L4 (không phải packet khắc phục). Đã áp TRƯỚC các lớp finding đã tốn nhiều lượt ở ba đặc tả cùng Mission: `b4-predicate-mutation-proof` (không liệt kê ma trận; mục 5 đóng băng chốt, review mã thẩm định đủ); lớp "không đòi đột biến sống" (mục 5); `frozen-fixture-semantic-oracle-missing` của B1a (oracle vùng là mã độc lập, bảng fixture ghim băm, Nghiệm thu 7); `legacy-selector-equivalence-is-impossible` của B1a (không khai tương đương; A/B và bên đọc cũ ở Nghiệm thu 2); `b4-sensitive-size-authority` và `source-review-budget-not-activated` (mục Kích thước, hai dòng khai); bài học CLAUDE.md "cấm chuỗi con để nhận diện đường kia" (K4 phân biệt hai khối bằng mẫu ĐẦY ĐỦ của registry thật, không bằng một từ chung).

## Quyết định của người soạn (uỷ quyền, điều phối ghi vào sổ `uy_quyen_quyet_dinh.v1` trên Issue #1463)
1. Không đưa `cloud_agent_creds_test`/`land_evidence_nguon_test` vào PR2 (Ngoài phạm vi). Đo chống đỡ: write set Issue/Mission.
2. Giá trị cờ lạ ⇒ `day_du`, không ĐỎ (mục 1), theo r3 I3; registry chỉ đặt đúng `1` hoặc gỡ khoá (`env_theo_che_do`).
3. Chốt của dữ liệu registry được ca và đột biến của CHÍNH `ops/ci_provenance_test.py` canh (mục 5), không bằng `phan_chung`: `phan_chung` không có bộ chạy đột biến phân hạng bằng lớp ngoại lệ; bộ này có sẵn. Hệ quả chấp nhận: mọi thay đổi registry chạy bộ này đủ, nên các đột biến ấy luôn chạy khi tệp registry đổi.
4. Không khai dòng `dieu_kien_merge` (mục Quy trình).
5. Bảng tương đương sản xuất rỗng (mục 4).

## `chua_do_duoc`
- Thời gian của lượt nhẹ và lượt đủ trên runner CI: chưa đo (chỉ có số đo cục bộ ở mục "Số đo"; CI đo sau merge, Nghiệm thu 10).
- Lượt nhẹ THẬT qua `ci.yml`: không có trước merge (PR2 chạm vùng nên CI của nó chạy đủ); thay bằng Nghiệm thu 3 cục bộ và Nghiệm thu 10(a) sau merge.
- Tệp mà tiến trình con KHÔNG phải Python mở (Nghiệm thu 4, giới hạn).
- Tiết kiệm thật: r3 ước 0,4–0,7 triệu s/30 ngày, giả định tỷ lệ `day_du` ≈ 16 % như hai bộ tiền lệ; chưa đo.
- Nội dung thay đổi của #1475 trên `ops/ci_provenance_test.py` và của B1a/B2 trên `.claude/dev/ci_dang_ky_test.py`: chưa land lúc soạn.
- Hành vi trên Windows của lượt nhẹ (registry có ma trận Windows khi dispatch): không đo, không có lượt Windows trong packet.

## Số đo lúc soạn (2026-11-21, base `e2f28fb`, phiên cloud Linux, 4 CPU, Python 3.13)
- Ba phép đo `ADR-0053` cho OID `8ab100793df9831505f495543a74044b91c2c9ab` và `ADR-0055` cho OID `d2e3052d479d140b7e7b91df41ec4914fab7d544` (kho không shallow): tệp ADR có ở OID (rc 0), vắng ở cha thứ nhất (rc 128), OID trên first-parent `origin/master` (rc 0) — cả hai đạt.
- Kế hoạch đột biến tại base (nạp module blob `21b23dbc` rồi đếm `len`; một lần đếm phần tử literal bằng `ast` ra 367 vì 6 phần tử của tuple là `*…` sinh nhiều mục khi chạy — số ấy SAI, không dùng): `DOT_BIEN` 398, `DOT_BIEN_TEST` 11, `TU_KIEM` 2; `CA` 68 ca. Khớp dòng `DOT BIEN: 409/409` của lượt đủ dưới đây.
- Oracle vùng và bảng 23 hàng: `ORACLE 23/23` đúng kỳ vọng; bơm bốn thay đổi dữ liệu của mục 3 vào một bản nạp của `ci_dang_ky_test.py` tại base (không sửa tệp) rồi gọi `ke_hoach` THẬT ⇒ 23/23 khớp; sha256 bảng `b0dd2b59cbf623c3abea7ee971b591d9ac39fc0d84bac52958bbe37a98b1f96a`. Tức hợp đồng mục 3 đạt được chỉ bằng dữ liệu.
- Tệp trong kho mà bộ mở: (a) audit hook `open` trong một tiến trình, chạy mọi ca: `.claude/dev/ci_dang_ky_test.py`, `.github/workflows/ops-do-workflow-definition.yml`, `ops/bash_nen.py`, `ops/ci_provenance.py` (cộng tệp test); tiến trình ngoài được sinh: `bash`, `git`, `python3`. (b) Đúng phép đo của Nghiệm thu 4 tại base: lượt đủ trọn (17:09Z → 17:24Z, chậm hơn vì hook) với `sitecustomize` audit hook trong MỌI tiến trình Python, 63 406 dòng nhật ký; giao với `git ls-files` còn đúng năm tệp: `.claude/dev/ci_dang_ky_test.py`, `.github/workflows/ops-do-workflow-definition.yml`, `ops/bash_nen.py`, `ops/ci_provenance.py`, `ops/ci_provenance_test.py` — cả năm thoả `oracle({x}) == "day_du"`. Các tên giả `00`…`ff`, `objects`, `refs`, `.git` trong nhật ký là tạo tác `dir_fd` đã nêu ở Nghiệm thu 4. Kết quả của lượt ấy: `CA: 67/68` (`c61`), `DOT BIEN: 409/409`, `TU KIEM PHAN HANG: DAT (2 dot bien)`.
- Lượt đủ của bộ tại base, cục bộ, biến vắng, `python3 -B ops/ci_provenance_test.py` (16:58:05Z → 17:06:28Z, ≈ 503 s tường, `TIEN TRINH: 4`): `CA: 67/68 dat` · `DOT BIEN: 409/409 bi giet dung ly do` · `TU KIEM PHAN HANG: DAT (2 dot bien)` · `TONG: DO`, rc 1 — ca đỏ duy nhất là `c61` (xem dòng dưới). Phần ca nền chạy trong một tiến trình (không vòng đột biến, không `TU_KIEM`) mất ≈ 73 s; đây là cận dưới thô của lượt nhẹ, không phải số đo lượt nhẹ (Nghiệm thu 5 đo).
- `actionlint` có, `shellcheck` VẮNG trong phiên soạn ⇒ ca `c61_actionlint_bat_yaml_sai` đỏ sẵn (`thiếu actionlint/shellcheck trong kho thật`). Vì thế Nghiệm thu 1 đòi cài `shellcheck`.
- Nền CI (từ kế hoạch r3, `[B: …]` của BASELINE #1434): bộ 660 bản ghi, tất cả `day_du`, trung vị 1371,7 s; bước registry trung vị 1252 s; hai bộ `NHE` tiền lệ chỉ `day_du` 134/829 và 124/829 lần.
