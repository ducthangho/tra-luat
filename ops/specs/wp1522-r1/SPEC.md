# wp1522 r3 — nợ B1a: bỏ lời hứa toàn phần của lệnh thu (chỉ giữ tính chất an toàn) + oracle «Lệnh kiểm» v2 (năm 0001, `jobs[].run_id`) (NO-B1A-N1)
packet_id: wp1522
revision: 3
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab
tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
dieu_kien_merge: ADR-0060@36d7c5dcdcbbb27176b75135125b9009f9fe0587
mission_issue: 1172
packet_issue: 1522
risk: sensitive
review_class: sensitive
executor: claude
environment: cloud (Linux)

Trạng thái: r3, lượt soạn cuối (3/3). Thay r2 (`ops/wp1522-r1@5826c84`, sha256 `07f7cf25…`). Review lượt 2 trên r2 trả `blocked`: N1-02 ĐÃ VÁ THẬT; N1-01 VÁ SINH LỖI MỚI; finding mới N1-03 P2 thuộc lớp `v1-not-fully-specified`, lần tái diễn thứ 6. Checkpoint §12: không vá tiếp; chủ kho chọn bỏ lời hứa toàn phần. r3 viết lại §1 thành MỘT tính chất an toàn, bỏ biên ngoài cùng và bản dự phòng. K2, K4 và hiện vật v2 không đổi byte. Chưa duyệt băm, chưa có lease.

## Mục tiêu
Đóng ba khoản nợ của B1a #1460: khoản 1, 2 và 4 trong mục `no_ngoai_pham_vi` của `ops/land/pr1516-wp1460-land-evidence.yaml`. Lớp `v1-not-fully-specified` đã tái diễn sáu lần: B1-04 ở review đặc tả wp1460; F02, F02-R2, F02-R3 ở review mã PR #1516; N1-01, N1-03 ở review đặc tả của chính packet này. Theo L4 của skill soạn spec, số đếm hình dạng lỗi chép sang là **6**. Packet này làm ba việc:
- **K1** — bỏ lời hứa toàn phần; chỉ giữ tính chất AN TOÀN «tệp đã ghi thì hợp lệ, mã 0 ⇔ đã ghi biên nhận xanh» (quyết định chủ kho, phương án (b) của checkpoint §12).
- **K2** — tài liệu mà chính parser từ chối (kể cả vì độ sâu) được khai thẳng là «không đọc được». Đây là hành vi của chốt hẹp `_doc_json_du`, kiểm bằng ca.
- **K4** — oracle «Lệnh kiểm» v2: không ném ở năm 0001, định dạng mốc không phụ thuộc nền, thêm luật đối chiếu chéo `jobs[].run_id`. Bên thu thêm điều kiện tương ứng ở X1.

Hình biên nhận `bien_nhan_audit.v1` (schema) KHÔNG đổi một byte.

## Hợp đồng

### 1. Lời hứa của lệnh thu: bỏ tính toàn phần, chỉ giữ tính chất AN TOÀN

Mục này thay câu «Với đối số hợp lệ lệnh thu LUÔN ghi một biên nhận hợp lệ theo schema rồi mới thoát» ở wp1460 r9 §3. Quyết định chủ kho «(b) Bỏ lời hứa toàn phần» được đưa ra sau checkpoint §12, khi lớp `v1-not-fully-specified` tái diễn lần thứ 6; bảng các lần tái diễn ở #1522.

- **1a. Lời hứa duy nhất.** Mọi tệp mà lệnh thu ghi ở đường dẫn `ra` đều là biên nhận hợp lệ theo schema đóng băng. Chi tiết:
  - Biên nhận được kiểm bằng bộ kiểm của schema ngay TRƯỚC lần ghi, trên đúng đối tượng sắp mã hoá.
  - Ghi đi qua MỘT hàm ghi nguyên tử: tệp tạm cùng thư mục, `fsync`, rồi `os.replace`.
  - Kiểm không đạt, hoặc bộ kiểm không nạp được ⇒ KHÔNG ghi tệp ấy.
  - Không có trạng thái nào mà `ra` chứa bytes dở hay một tệp không hợp schema do lượt này để lại.
- **1b. Mã thoát.**
  - 0 ⇔ lượt này đã ghi xong một biên nhận `ok: true` ở `ra`.
  - 1 khi đã ghi xong một biên nhận `ok: false`.
  - Mọi kết cục khác — lỗi đối số (2, như cũ), ngoại lệ bất kỳ lan ra, không ghi được — cho mã khác 0, và `ra` có thể vắng.
  - Mã 0 không bao giờ xuất hiện khi chưa ghi biên nhận xanh.
- **1c. Không còn lời hứa «luôn có biên nhận».** Lệnh thu KHÔNG bắt chung mọi ngoại lệ. Không có biên ngoài cùng, không có bản dự phòng. Một ngoại lệ bất ngờ lan ra, để traceback trong log job, và làm bước thu — tức job thu — đỏ.
  - Bước tải biên nhận lên có `if-no-files-found: error`, nên vắng tệp cũng làm job đỏ.
  - Bên tiêu dùng thấy job thu đỏ ⇒ từ chối lượt ấy theo C2. B2 phán `khong_do_duoc` cho lượt không có biên nhận, như hợp đồng B2 đã có.
- **1d. Không để biên nhận cũ sống sót.** Ngay sau khi `doi_so_thu` trả về hợp lệ, lệnh thu xoá `ra` nếu có. Xoá lỗi ⇒ ngoại lệ lan ra, mã khác 0. Lỗi đối số ⇒ KHÔNG xoá.
- **1e. Các chốt hẹp hiện có GIỮ nguyên:** F02-R2; F02-R3 (sáu lớp lỗi YAML); `_hop_le_du`; `_doc_json_du`; `_gt_du`; kiểm UTF-8 tên. Các ca hiện có của chúng (đầu vào hỏng ⇒ biên nhận không xanh) vẫn phải đạt. Từ đây chúng là HÀNH VI được kiểm bằng ca, KHÔNG phải một phần của lời hứa. Một đường hỏng mới mà không có chốt hẹp nào bắt thì cho kết cục ở 1c, và đó không phải vi phạm hợp đồng.

### 2. Tài liệu parser từ chối (K2)
- `_doc_json_du` coi mọi tài liệu mà `json.loads` không trả về được (gồm `RecursionError` vì độ sâu) là «không đọc được». Ở REST và ở mảnh ⇒ không xanh; ở definition ⇒ `not_measured`. Đây là hành vi hiện tại của chốt hẹp (1e), kiểm bằng ca ở Nghiệm thu 3. Nó không phải một lời hứa toàn phần.
- **Không mục tiêu**: đọc được tài liệu sâu hơn giới hạn parser. Không thêm parser phi đệ quy, không thêm trần độ sâu nào. Trần 64 của H3 đã bị F02-R3 bác.

### 3. Oracle «Lệnh kiểm» v2 và fixture v2 (K4) — hiện vật đóng băng
- Thư mục mới `ops/specs/wp1522-r1/hop_dong/`:
  - `bien_nhan_audit.v1.schema.json`: chép NGUYÊN BYTE từ `ops/specs/wp1460-r1/hop_dong/`;
  - `fixture.json`: bản `bien_nhan_audit.v1.fixture/4`.
- Hai tệp của wp1460 KHÔNG đổi, KHÔNG xoá. Chúng là GHIM-B1A của B2 #1494 (B2 pin băm hai tệp ấy và chép `tieu_dung`/`khung_cron` của khối v1).

| tệp | sha256 |
|---|---|
| `ops/specs/wp1522-r1/hop_dong/bien_nhan_audit.v1.schema.json` | `844b5218b6f6844945f5c4c9440f09015d238fe09a60d64b3787c440787e4f46` |
| `ops/specs/wp1522-r1/hop_dong/fixture.json` | `19dc7fd172be2d32c1aff8d0d2bdeb300df3fcb6ccb8d846bef3e15cd667e832` |
| khối «Lệnh kiểm» bên dưới (bytes utf-8 giữa hai dòng rào, không gồm dòng rào) | `da8e032fdef3429711a75796886b6e97d3ae60e8428e16efac0968db4cda9519` |

- **Đổi so với v1** (ba chỗ trong mã, ba nhóm trong fixture):
  - `khung_cron` trả `None` khi phép trừ ngày tràn miền `datetime` hoặc năm của khung < 1000. Hàm mới `chuoi_moc` định dạng mốc tường minh bằng `{:04d}`, thay `strftime("%Y…")`, vốn cho kết quả khác nhau giữa glibc và Python 3.14. `C9.khung` vi phạm khi khung là `None`.
  - Vị từ mới `C4.rest_run_id`: mọi bản ghi `rest.jobs` có `run_id` kiểu `int` và bằng `run.id`.
  - Fixture: thêm `run_id` vào mọi bản ghi `nen.rest.jobs`. Ca `luat-C3-run-id-khac` đổi luôn `jobs[].run_id` cho nhất quán với `run.id` mới, để vẫn chỉ cô lập C3. Thêm năm ca:
    - `luat-C9-khung-nam-0001-tran`;
    - `luat-C9-khung-nam-0999-khong-bieu-dien`: khung ghi ĐÚNG lịch `0999-11-16T19:17:00Z`, nên chỉ luật năm < 1000 làm C9;
    - `luat-C4-rest-job-cua-luot-khac`;
    - `luat-C4-rest-job-run-id-float-bang-gia-tri`;
    - `luat-C4-rest-job-thieu-run-id`.
  - **Hai đột biến đích bắt buộc** (người soạn đã chạy, mục "Số đo"). Mỗi đột biến sửa khối «Lệnh kiểm» trên bản sao, và phải cho `TONG: DO` với đúng một dòng `LECH` nêu tên ca đích:
    - `return t if t.year >= 1000 else None` → `return t`, ca đích `luat-C9-khung-nam-0999-khong-bieu-dien`;
    - `type(j.get("run_id")) is int and j["run_id"] == run["id"]` → `j.get("run_id") == run["id"]`, ca đích `luat-C4-rest-job-run-id-float-bang-gia-tri`.

    Bộ chạy `--dot-bien` của khối chỉ gỡ cả vị từ, nên hai đột biến này nằm ở bảng đột biến của `ci_dang_ky_test.py` (Nghiệm thu 1).
- **Dòng kỳ vọng** (người soạn đã chạy, mục "Số đo"):
  - `FIXTURE: 490/490 phep kiem dung ky vong · hinh 125 · ngu nghia 123 · tu vung 79 · doi tuong 163 · luat duoc phu 12/12`
  - `DOT BIEN: giet 250/250 · vi tu 58 · noi long schema 192`
  - `TONG: DAT`

### 4. Bên thu (K4, phía sản xuất)
- **X1 thêm:** mọi bản ghi của `jobs` có `run_id` đúng kiểu `int` (không nhận `bool`, không nhận `float`) và bằng `run_id` của context. Lệch, thiếu hoặc sai kiểu ⇒ không xanh, `ly_do` nêu tên job. Miền này trùng với `C4.rest_run_id`.
- **X8:** `_khung_du` dùng cùng luật với `khung_cron`/`chuoi_moc` của oracle v2: tràn hoặc năm < 1000 ⇒ khung `null`, không xanh. Hành vi tại base đã tương đương trên glibc (đã đo ở review lượt 4 PR #1516). Packet chỉ bỏ phụ thuộc `%Y`.

### 5. `.claude/dev/ci_dang_ky_test.py`
- `LENH_KIEM_HOP_DONG` thay bằng khối v2, chép nguyên byte.
- `BAM_HOP_DONG` đổi sang ba băm ở mục 3.
- `DAU_RA_LENH_KIEM` đổi sang ba dòng ở mục 3.
- `THU_MUC_HOP_DONG` trỏ `ops/specs/wp1522-r1/hop_dong/`.
- Nếu #1521 (N2) đã land, khoá `DA_DO_DOT_BIEN_1460` phải nhận khoá mới bằng một lượt đầy đủ đo trên H.
- Ca, đột biến và chốt hiện có của wp1460 giữ nguyên ý nghĩa. Ca nào phụ thuộc số đếm cũ thì cập nhật kèm A/B trong MỘT lệnh.

## Nghiệm thu
1. **Hợp đồng máy.** Lưu khối «Lệnh kiểm» ra tệp ngoài kho, chạy `python3 -B <tệp> ops/specs/wp1522-r1/hop_dong --dot-bien` với `jsonschema==4.26.0` ⇒ đúng ba dòng ở mục 3, mã thoát 0. sha256 của ba hiện vật bằng bảng mục 3, trên nhánh đặc tả và trong PR.
2. **Tính chất an toàn (K1).** Ca tiến trình con kiểu `CON_1460`, tiêm lỗi bằng cách thay MỘT hàm nội bộ trong bản nạp. Không thêm móc vào mã sản xuất. Mỗi ca chạy hai lần: với `ra` vắng, và với `ra` đã chứa sẵn một biên nhận `ok: true` của lượt khác.
   - **(a)** Ngoại lệ (`RecursionError` / `KeyError` / `MemoryError`) từ giữa X2 / X4 / X5 ⇒ mã khác 0 và `ra` VẮNG, kể cả khi trước đó có biên nhận xanh cũ.
   - **(b)** Biên nhận dựng ra không hợp schema ở lần kiểm cuối ⇒ không ghi, mã khác 0, `ra` vắng. Tiêm lỗi bằng cách làm hỏng một trường của đối tượng ngay trước lần kiểm cuối.
   - **(c)** Tiêm lỗi giữa chừng trong hàm ghi nguyên tử, sau khi đã ghi một phần tệp tạm ⇒ `ra` vắng. Không còn tệp tạm nào trong thư mục, hoặc nếu còn thì tên của nó không trùng `ra`.
   - **(d)** Bộ kiểm schema không nạp được ⇒ không ghi, mã khác 0.
   - **(e)** Mã 0 ⇔ `ra` là biên nhận `ok: true` hợp schema. Kiểm trên MỌI ca dương và âm hiện có.
   - **(f)** Lỗi đối số ⇒ mã 2, và biên nhận cũ ở `ra` KHÔNG bị xoá.
   - **(g)** Mọi ca hiện có của wp1460 vẫn đạt, gồm các ca «đầu vào hỏng ⇒ biên nhận không xanh».
3. **K2.** Hai ca hiện có ở biên parser (dấu job sâu, `started_at`/`completed_at` sâu) vẫn đạt. Thêm một ca: trường KHÔNG dùng của `rest/run.json` sâu hơn giới hạn parser đo trên chính nền (tìm nhị phân như `quet_bien`) ⇒ rc 1, biên nhận không xanh hợp schema, `ly_do` nêu `rest/run.json`.
4. **K4 bên thu.** Ca âm: một bản ghi `jobs` có `run_id` = lượt + 1 ⇒ rc 1, không xanh. Ca âm: `run_id` vắng ⇒ không xanh. Ba ca dương hiện có (lượt khoẻ, chạy lại job thu, chạy lại một mảnh) vẫn xanh, và `tieu_dung` v2 trên đầu vào của ca cho tập vi phạm rỗng.
5. **Hồi quy.** Mọi ca hiện có của wp1460 đạt. Dựng A/B base/head trong MỘT lệnh; mọi chênh lệch số ca phải giải thích được bằng ca thêm hoặc bỏ có tên.
6. **Đột biến riêng cho MỖI chốt mới.** Chạy trên BẢN SAO tạm, tên tệp riêng, tắt bytecode; phân hạng bằng lớp ngoại lệ riêng của ca đích, neo tên ca; chết vì lỗi vô can ⇒ tín dụng giả. Tối thiểu:
   - (i) bỏ lần kiểm schema cuối trước khi ghi;
   - (ii) ghi trực tiếp, không qua tệp tạm + `os.replace`;
   - (iii) bỏ bước xoá `ra` ở 1d;
   - (iv) xoá `ra` cả khi lỗi đối số;
   - (v) trả 0 khi biên nhận đã ghi là `ok: false`;
   - (vi) bắt chung `Exception` quanh bước chính và trả 0 hoặc 1 mà không ghi biên nhận;
   - (vii) bộ kiểm không nạp được mà vẫn ghi;
   - (viii) bỏ X1 `run_id`;
   - (ix) X1 chấp nhận `run_id` kiểu `float` bằng giá trị;
   - (x) `_khung_du` dùng lại `strftime`.

   Mỗi đột biến neo đúng ca đích ở mục 2 hoặc mục 4.
   Đòi `n/n` giết thật.
7. **Cổng kho.** `python .claude/dev/ci_dang_ky_test.py --chay` N/N; Ruff F delta = 0 trên mọi `.py` đổi; numstat trong trần; CI PR Ubuntu xanh.

## Lệnh kiểm (dùng cho Nghiệm thu 1)
```python
"""Lenh kiem hop dong bien_nhan_audit.v1 (wp1460 B1a). python3 -B <tep> <thu muc hop_dong> [--dot-bien]"""
import copy, datetime, json, re, sys
import jsonschema
JOB_THU, JOB_GOP, TIEN_TO_MANH, CRON_GHIM = "bien-nhan-audit", "dot-bien-gop", "dot-bien-manh", "17 19 * * 6"

def nap(d):
    d = d.rstrip("/") + "/"
    return (json.load(open(d + "bien_nhan_audit.v1.schema.json", encoding="utf-8")), json.load(open(d + "fixture.json", encoding="utf-8")))

def bo_kiem(S):
    jsonschema.Draft202012Validator.check_schema(S)
    return {"bien_nhan": jsonschema.Draft202012Validator(S),
            "dau_job": jsonschema.Draft202012Validator({"$schema": S["$schema"], "$ref": "#/$defs/dau_job_v1", "$defs": S["$defs"]})}

def tro(doc, duong):
    o = doc
    for k in [x.replace("~1", "/").replace("~0", "~") for x in duong.split("/")[1:]]:
        o = o[int(k)] if isinstance(o, list) else o[k]
    return o

def ap(doc, sua):
    for s in sua or []:
        cha, _, cuoi = s["duong"].rpartition("/")
        o, cuoi = tro(doc, cha), cuoi.replace("~1", "/").replace("~0", "~")
        if isinstance(o, list) and cuoi == "-":
            o.append(s["gia_tri"])
        elif s.get("xoa"):
            del o[int(cuoi) if isinstance(o, list) else cuoi]
        else:
            o[int(cuoi) if isinstance(o, list) else cuoi] = s["gia_tri"]
    return doc

def khoa_tu_ten(ten):
    m = re.fullmatch(r"(.+) \((.+)\)", ten)
    return f"{m[1]}-{m[2]}" if m else ten

def doc_moc(v):
    try:
        return datetime.datetime.strptime(v, "%Y-%m-%dT%H:%M:%SZ")
    except (TypeError, ValueError):
        return None

def khung_cron(tao):
    """Moc `17 19 * * 6` (thu Bay 19:17 UTC) gan nhat <= tao; None khi KHONG tinh duoc (phep tru ngay tran mien datetime, vd nam 0001)
    hoac nam < 1000 (ben thu cung coi la khong bieu dien duoc). wp1522: ban cu nem OverflowError o nam 0001."""
    try:
        t = tao.replace(hour=19, minute=17, second=0) - datetime.timedelta(days=(tao.weekday() - 5) % 7)
        t = t if t <= tao else t - datetime.timedelta(days=7)
    except OverflowError:
        return None
    return t if t.year >= 1000 else None

def chuoi_moc(t):
    """Dinh dang moc tuong minh, khong phu thuoc `%Y` cua nen (glibc khong dem nam < 1000; Python 3.14 thi dem)."""
    return f"{t.year:04d}-{t.month:02d}-{t.day:02d}T{t.hour:02d}:{t.minute:02d}:{t.second:02d}Z"

def tieu_dung(V, b, rest, ngoai, bo=None, hop_le=None):
    """Luat C cua ben tieu dung, tung VI TU co ten. Tra (tap luat vi pham, canh bao, moc tinh tuoi). `bo` = ten vi tu bi go (dot bien);
    `hop_le` = ket qua kiem hinh da co cua b (None thi tu kiem)."""
    if not (V["bien_nhan"].is_valid(b) if hop_le is None else hop_le) or b["ok"] is not True:
        return {"C1"}, [], None
    vp, run, lu, sk = set(), rest["run"], b["luot"], b["su_kien"]
    def vt(ten, dk):                           # ten = "<luat>.<vi tu>"
        if ten != bo and not dk: vp.add(ten.split(".")[0])
    E = ngoai["job_ky_vong"]                   # ten job ben tieu dung TU lap tu tep workflow tai H
    moi = {}                                   # ten job -> ban ghi REST co run_attempt lon nhat
    for j in rest["jobs"]:
        if j["name"] not in moi or j["run_attempt"] > moi[j["name"]]["run_attempt"]:
            moi[j["name"]] = j
    cap = [(j["name"], j["run_attempt"]) for j in rest["jobs"]]
    vt("C1.attempt_moi_nhat", lu["run_attempt"] == run["run_attempt"])
    vt("C2.run_completed", run["status"] == "completed")
    vt("C2.run_success", run["conclusion"] == "success")
    vt("C2.moi_job_success", all(j["conclusion"] == "success" for j in moi.values()))
    vt("C3.kho", b["kho"] == run["repository"]["full_name"])
    vt("C3.kho_id", b["kho_id"] == run["repository"]["id"])
    vt("C3.duong_dan", b["workflow"]["duong_dan"] == run["path"])
    vt("C3.run_id", lu["run_id"] == run["id"])
    vt("C3.su_kien_ten", sk["ten"] == run["event"])
    vt("C3.sha_rest", sk["sha"] == run["head_sha"])
    vt("C3.sha_h", sk["sha"] == ngoai["h"])
    hang = {r["ten"]: r for r in b["job"]}
    vt("C4.rest_khong_trung", len(cap) == len(set(cap)))
    vt("C4.rest_run_id", all(type(j.get("run_id")) is int and j["run_id"] == run["id"] for j in rest["jobs"]))
    vt("C4.rest_du", set(moi) == set(E))
    vt("C4.dong_khong_trung", len(b["job"]) == len(hang))
    vt("C4.tap_ten", set(hang) == set(E))
    vt("C4.ky_vong", b["kiem_ke_job"]["ky_vong"] == sorted(E))
    vt("C4.thuc_co", b["kiem_ke_job"]["thuc_co"] == sorted(E))
    cung = [(r, moi[t]) for t, r in hang.items() if t in moi]
    vt("C4.job_id", all(r["job_id"] == j["id"] for r, j in cung))
    vt("C4.run_attempt", all(r["run_attempt"] == j["run_attempt"] for r, j in cung))
    vt("C4.khoa", all(r["khoa"] == khoa_tu_ten(r["ten"]) for r in b["job"]))
    vt("C4.tu_than", all(r["tu_than"] == (r["ten"] == JOB_THU) for r in b["job"]))
    vt("C4.ten_dau", all(r["dau_job"]["ten"] == f"dau-job-{lu['run_id']}-{j['run_attempt']}-{khoa_tu_ten(r['ten'])}" for r, j in cung))
    vt("C5.job_sha", all(r["checkout_sha"] == sk["sha"] for r in b["job"]))
    vt("C5.manh_head", all(m["head"] == sk["sha"] for m in b["manh"]))
    vt("C5.tree_h", all(r["checkout_tree"] == ngoai["tree_h"] for r in b["job"]))
    ky = {}                                    # khoa job manh -> k, lap tu E (doc lap voi bien nhan va REST)
    for t in E:
        m = re.fullmatch(re.escape(TIEN_TO_MANH) + r" \((0|[1-9][0-9]*)\)", t)
        if m: ky[khoa_tu_ten(t)] = int(m[1])
    ten_theo_khoa = {khoa_tu_ten(t): t for t in E}
    att = lambda khoa: moi.get(ten_theo_khoa.get(khoa), {}).get("run_attempt")   # attempt REST moi nhat cua job mang khoa ay
    co = [m for m in b["manh"] if m["khoa_job"] in ky and att(m["khoa_job"]) is not None]
    vt("C6.manh_khong_trung", len(b["manh"]) == len({m["khoa_job"] for m in b["manh"]}))
    vt("C6.tap_manh", {m["khoa_job"] for m in b["manh"]} == set(ky))
    vt("C6.job_le_luot", all(j["run_attempt"] <= lu["run_attempt"] for j in moi.values()))
    vt("C6.chi_so", all(m["manh"] == ky[m["khoa_job"]] for m in co))
    vt("C6.attempt", all(m["attempt_ben_san_xuat"] == att(m["khoa_job"]) for m in co))
    vt("C6.le_gop", att(JOB_GOP) is not None and all(att(m["khoa_job"]) <= att(JOB_GOP) for m in co))
    vt("C6.ten_artifact", all(m["artifact"]["ten"] == f"{TIEN_TO_MANH}-{lu['run_id']}-{att(m['khoa_job'])}-{ky[m['khoa_job']]}" for m in co))
    vt("C7.job_truoc", b["dau_hieu_duong"]["job_truoc_success"] == f"{len(E) - 1}/{len(E) - 1}")
    vt("C7.manh", b["dau_hieu_duong"]["manh"] == f"{len(ky)}/{len(ky)}")
    kho = {a["id"]: a for a in rest["artifacts"]}
    dau = [(r["dau_job"], "dau-job.json", r) for r in b["job"]]
    mnh = [(m["artifact"], f"manh-{m['manh']}.json", m) for m in b["manh"]]
    cr = [(a, kho[a["id"]]) for a, _, _ in dau + mnh if a["id"] in kho]
    ct = [(a, ten, d, ngoai["tai_ve"][str(a["id"])]) for a, ten, d in dau + mnh if str(a["id"]) in ngoai["tai_ve"]]
    c1 = [x for x in ct if len(x[3]["tep"]) == 1 and x[3]["tep"][0]["ten"] == x[1]]      # dung MOT tep, dung ten
    vt("C8.co_trong_rest", len(cr) == len(dau + mnh))
    vt("C8.ten", all(a["ten"] == r["name"] for a, r in cr))
    vt("C8.digest_rest", all(a["digest"] == r["digest"] for a, r in cr))
    vt("C8.chua_het_han", all(r["expired"] is False for a, r in cr))
    vt("C8.da_tai", len(ct) == len(dau + mnh))
    vt("C8.goi", all(a["digest"] == "sha256:" + t["sha256_goi"] for a, _, _, t in ct))
    vt("C8.mot_tep", len(c1) == len(ct))
    vt("C8.tep_bam", all(a["sha256_noi_dung"] == t["tep"][0]["sha256"] for a, _, _, t in c1))
    nd = [(t["tep"][0]["noi_dung"], d) for a, ten, d, t in c1 if ten == "dau-job.json"]
    nho = V.setdefault("nho", {})                # nho ket qua kiem hinh dau theo noi dung
    def dau_hop_le(n):
        k = json.dumps(n, sort_keys=True)
        if k not in nho: nho[k] = V["dau_job"].is_valid(n)
        return nho[k]
    ok = [(n, d) for n, d in nd if dau_hop_le(n)]
    vt("C11.hinh", len(ok) == len(nd))
    vt("C11.khoa_job", all(n["khoa_job"] == d["khoa"] for n, d in ok))
    vt("C11.run_id", all(n["run_id"] == lu["run_id"] for n, d in ok))
    vt("C11.run_attempt", all(n["run_attempt"] == d["run_attempt"] for n, d in ok))
    vt("C11.su_kien_sha", all(n["su_kien_sha"] == sk["sha"] for n, d in ok))
    vt("C11.checkout_sha", all(n["checkout_sha"] == d["checkout_sha"] for n, d in ok))
    vt("C11.checkout_tree", all(n["checkout_tree"] == d["checkout_tree"] for n, d in ok))
    nm = [(t["tep"][0]["noi_dung"], d) for a, ten, d, t in c1 if ten != "dau-job.json"]
    om = [(n, d) for n, d in nm if isinstance(n, dict)]
    vt("C12.la_object", len(om) == len(nm))
    vt("C12.head", all(n.get("head") == d["head"] for n, d in om))
    vt("C12.manh", all(type(n.get("manh")) is int and n.get("manh") == d["manh"] for n, d in om))
    tao = doc_moc(sk["run_created_at"])
    vt("C9.tao_khop_rest", sk["run_created_at"] == run["created_at"])
    vt("C9.lich_hop_le", tao is not None)
    if sk["ten"] == "schedule":
        vt("C9.cron_ghim", sk["cron"] == CRON_GHIM)
        k = khung_cron(tao) if tao is not None else None
        vt("C9.khung", tao is None or (k is not None and sk["khung_danh_nghia_utc"] == chuoi_moc(k)))
    canh = ["C10"] if bo != "C10.canh_bao" and b["dinh_danh_definition"]["trang_thai"] == "not_measured" else []
    return vp, canh, sk.get("khung_danh_nghia_utc") or sk["run_created_at"]

class LechDauTien(Exception):
    """Tin hieu RIENG cua bo kiem: phep kiem dau tien lech (dung cho dot bien; ngoai le khac KHONG duoc tinh la giet)."""

def chay(S, F, bo=None, som=False):
    """Chay moi phep kiem. Tra (danh sach lech, bo dem, tap luat duoc phu). `bo` (go mot vi tu) chi anh huong phan ngu nghia nen chi chay phan ay."""
    V, sai, dem, phu = bo_kiem(S), [], {"hinh": 0, "ngu_nghia": 0, "tu_vung": 0, "doi_tuong": 0}, set()
    def hop(nen, doc): return V["dau_job" if nen == "dau_job" else "bien_nhan"].is_valid(doc)
    def lech(x):
        sai.append(x)
        if som: raise LechDauTien(x)
    ten = [c["ten"] for c in F["ca"]]
    assert len(ten) == len(set(ten)), "ten ca trung"
    for t in [] if bo else F["tu_vung"]:         # moi dia diem co pattern: mau hop le; bien the thi khong
        bien = [t["mau"] + "\n", t["mau"] + "\r\n", " " + t["mau"], t["mau"] + " ", 5, None, [t["mau"]]] + t["sai"]
        for gt, mong in [(t["mau"], True)] + [(x, False) for x in bien]:
            dem["tu_vung"] += 1
            if hop(t["nen"], ap(copy.deepcopy(F["nen"][t["nen"]]), [{"duong": t["duong"], "gia_tri": gt}])) != mong:
                lech(f"TU VUNG {t['dia_diem']}: {gt!r}")
    for t in [] if bo else F["doi_tuong"]:       # moi object: go tung khoa / them khoa la / thay bang chuoi, danh sach deu KHONG hop le
        goc = ap(copy.deepcopy(F["nen"][t["nen"]]), t.get("sua_truoc"))
        o = tro(goc, t["duong"]) if t["duong"] else goc
        bien = [{k: v for k, v in o.items() if k != x} for x in o] + [dict(o, khoa_la=1), "x", [o]]
        for moi, mong in [(o, True)] + [(x, False) for x in bien]:
            dem["doi_tuong"] += 1
            doc = moi if not t["duong"] else ap(copy.deepcopy(goc), [{"duong": t["duong"], "gia_tri": moi}])
            if hop(t["nen"], doc) != mong:
                lech(f"DOI TUONG {t['nen']}{t['duong']}: {sorted(moi) if isinstance(moi, dict) else moi!r}")
    for c in F["ca"]:
        doc = ap(copy.deepcopy(F["nen"][c["nen"]]), c.get("sua"))
        hop_le = c["hinh_hop_le"] if bo else hop(c["nen"], doc)
        dem["hinh"] += 1
        if hop_le != c["hinh_hop_le"]:
            lech("HINH " + c["ten"])
            continue                             # lech hinh: bao rieng, khong roi xuong nhanh ngu nghia
        if c["nen"] == "dau_job":
            continue
        vp, canh, moc = tieu_dung(V, doc, ap(copy.deepcopy(F["nen"]["rest"]), c.get("sua_rest")), ap(copy.deepcopy(F["nen"]["ngoai"]), c.get("sua_ngoai")), bo, hop_le)
        dem["ngu_nghia"] += 1
        if sorted(vp) != sorted(["C1"] if not hop_le else c["vi_pham"]) or canh != c.get("canh_bao", []) or ("moc_tuoi" in c and moc != c["moc_tuoi"]):
            lech(f"NGU NGHIA {c['ten']}: vi pham {sorted(vp)} canh bao {canh} moc {moc}")
        phu |= set(vp) | set(canh) | ({"C9"} if "moc_tuoi" in c else set())
    can = {f"C{i}" for i in range(1, 13)}
    if bo is None and phu != can:
        lech(f"PHU LUAT thieu {sorted(can - phu)}")
    return sai, dem, phu

def vi_tri_schema(S):
    """Moi cho noi long schema: (mo ta, ham sua tren ban sao)."""
    ra = []
    def di(n, duong):
        if isinstance(n, dict):
            for k in ("pattern", "minLength", "minimum", "minItems", "uniqueItems", "const", "maxContains", "type"):
                if k in n: ra.append((f"{duong}: go {k}", duong, ("go", k)))
            if "contains" in n: ra.append((f"{duong}: go contains", duong, ("go", "contains")))
            if n.get("additionalProperties") is False: ra.append((f"{duong}: mo additionalProperties", duong, ("mo", None)))
            for x in n.get("required", []): ra.append((f"{duong}: bo required {x}", duong, ("req", x)))
            for i in range(len(n.get("oneOf", []))): ra.append((f"{duong}: bo nhanh oneOf[{i}]", duong, ("oneOf", i)))
            for k, v in n.items(): di(v, f"{duong}/{k}")
        elif isinstance(n, list):
            for i, v in enumerate(n): di(v, f"{duong}/{i}")
    di(S, "")
    return ra

def sua_schema(S, duong, lenh):
    S = copy.deepcopy(S)
    n = tro(S, duong) if duong else S
    if lenh[0] == "go":
        del n[lenh[1]]
        if lenh[1] == "contains": n.pop("maxContains", None)
    elif lenh[0] == "mo": n["additionalProperties"] = True
    elif lenh[0] == "req": n["required"].remove(lenh[1])
    else: del n["oneOf"][lenh[1]]
    return S

def dot_bien(S, F):
    """Moi dot bien phai lam `chay` bao LECH ma KHONG nem ngoai le. Tra (giet, tong, danh sach song/loi)."""
    ten_vt = sorted(set(re.findall(r'vt\("(C[0-9]+\.[a-z_0-9]+)"', open(__file__, encoding="utf-8").read())) | {"C10.canh_bao"})
    ds = [("vi tu " + t, lambda t=t: chay(S, F, bo=t, som=True)) for t in ten_vt]
    ds += [("schema " + mt, lambda d=d, l=l: chay(sua_schema(S, d, l), F, som=True)) for mt, d, l in vi_tri_schema(S)]
    def loi_gia(): raise KeyError("tu kiem")       # tu kiem bo phan hang: ngoai le KHONG duoc tinh la giet
    giet, xau = 0, []
    for ten, f in ds + [("TU KIEM ngoai le vo can", loi_gia)]:
        try:
            f()
            ket = "SONG"
        except LechDauTien:                        # CHI tin hieu rieng cua bo kiem moi la giet
            ket = "GIET"
        except Exception as e:                     # noqa: BLE001
            ket = f"LOI {type(e).__name__}"
        if ten.startswith("TU KIEM"):
            if ket != "LOI KeyError": xau.append(f"TU KIEM bo phan hang hong: {ket}")
        elif ket == "GIET": giet += 1
        else: xau.append(f"{ket} (khong tinh la giet): {ten}")
    return giet, len(ds), xau, len(ten_vt)

if __name__ == "__main__":
    S, F = nap(sys.argv[1])
    sai, dem, phu = chay(S, F)
    n = sum(dem.values())
    print(f"FIXTURE: {n - len(sai)}/{n} phep kiem dung ky vong · hinh {dem['hinh']} · ngu nghia {dem['ngu_nghia']} · tu vung {dem['tu_vung']} · doi tuong {dem['doi_tuong']} · luat duoc phu {len(phu)}/12")
    for x in sai: print("LECH:", x)
    if "--dot-bien" in sys.argv[2:] and not sai:
        giet, tong, xau, so_vt = dot_bien(S, F)
        print(f"DOT BIEN: giet {giet}/{tong} · vi tu {so_vt} · noi long schema {tong - so_vt}")
        for x in xau: print("LECH:", x)
        sai += xau
    print("TONG:", "DAT" if not sai else "DO")
    sys.exit(1 if sai else 0)
```

## Write set
- Nhánh đặc tả `ops/wp1522-r1` (không thuộc PR giao nộp): `ops/specs/wp1522-r1/SPEC.md`, `ops/leases/wp1522-*.yaml`.
- PR giao nộp, đúng BA tệp: `.claude/dev/ci_dang_ky_test.py` · `ops/specs/wp1522-r1/hop_dong/bien_nhan_audit.v1.schema.json` · `ops/specs/wp1522-r1/hop_dong/fixture.json`. Hai tệp `hop_dong/` chép nguyên byte từ nhánh đặc tả; executor không soạn, không sửa.

## Ngoài phạm vi
- **Bản chép `tieu_dung`/`khung_cron` của B2** (`ops/canh_tuoi_audit.py`, nếu B2 đã land) vẫn ở v1. Đưa B2 và B3 lên v2 là việc của packet bên tiêu dùng, và cần quyết định của Mission. Đã nêu cho phiên điều phối Mission.
- Khoản 3 và 5 của nợ B1a thuộc #1521.
- Mọi phần B1b: chẩn đoán, A+3, phụ thuộc, giây/RSS.
- `ci.yml`, `ci-dot-bien-du.yml`, hai tệp `ops/specs/wp1460-r1/hop_dong/*`.

## Baseline nghiệm thu
Immutable acceptance baseline là `origin/master` lúc cấp lease, ghi vào lease. Lúc soạn, baseline là `437257a3` (2026-11-25).

## Kích thước
Trần mặc định của lớp `sensitive` theo `ADR-0053`: ≤ 6 tệp và ≤ 450 dòng thêm theo `git diff --numstat` so baseline. Hai tệp `hop_dong/` chiếm 34 + 166 = 200 dòng thêm (đếm trên hai tệp đã ghim). Đo trước MỖI lần xin review; vượt trần ⇒ DỪNG trước review, xin `nang_tran` theo `ADR-0053`.

## Quy trình và quyền
- **Điều kiện cấp lease:**
  1. Chủ kho duyệt băm đặc tả này.
  2. Mission revision xếp packet vào hàng `.claude/dev/ci_dang_ky_test.py`.
  3. Mọi lease khác giữ `.claude/dev/ci_dang_ky_test.py` (B2 `wp1494-*`, N2 `wp1521-*`, …) đã hết hạn hoặc đã thu hồi hai chiều. `ai-dang-giu` chạy trên MỌI ref, sau khi so TẬP TÊN ref với `ls-remote`, thiếu 0.
- **Vai (đề xuất, chủ kho chốt khi duyệt băm):** executor Claude Code Fable 5.2. Reviewer Codex gpt-6-astra, mức suy luận cao nhất, phiên độc lập, chỉ đọc. Reviewer CHẠY ca và đột biến có sẵn trong cây, và có bản sao kho đủ để đo lại.
- **Trần:** theo Mission r96 `per_new_packet`, trừ khi Mission revision cho packet này ghi khác. Lời gọi Codex trên PR theo dòng khai `ADR-0055`, đếm trước MỖI lời gọi. Lớp lỗi này đã tái diễn 4 lần: nếu review mã lượt 2 vẫn còn một biểu hiện của `v1-not-fully-specified`, DỪNG và quay lại chủ kho, không vá tiếp.
- **Windows (`ADR-0060` M3):** diff chạm `.claude/dev/**` ⇒ `required`. Chỉ đạt khi có dòng chủ kho `windows: <H> mien` neo H cuối, hoặc một lượt Windows local được cấp.
- Audit exact-H và merge theo `ADR-0060`. Merge do chủ kho bấm.
- **Hoàn tác:** revert PR giao nộp. Hai tệp v1 không bị đụng.

## Sổ quyết định (chủ kho, công cụ hỏi đáp trong phiên điều phối nợ, 2026-11-25 ~07:4xZ)
- Gom: «2 packet»: N1 #1522 gồm khoản 1, 2, 4; N2 #1521 gồm khoản 3, 5.
- Lời hứa (vòng 1): «Biên ngoài cùng + khoanh chữ». Quyết định này bị THAY ở checkpoint §12 sau review lượt 2: chủ kho chọn «(b) Bỏ lời hứa toàn phần (Recommended)» qua công cụ hỏi đáp ngày 2026-11-25 ~08:3xZ. Bảng tái diễn và các hướng đã nêu ở https://github.com/ducthangho/tra-luat/issues/1522#issuecomment-7156987442.
- Thẩm quyền gốc của nợ: https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-7137001118 (phương án b). Ứng viên biên ngoài cùng lấy từ https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-7137108788.
- Người soạn tự chọn, đưa vào lời xin duyệt băm để chủ kho bác nếu muốn:
  - hiện vật v2 đặt ở thư mục MỚI, giữ nguyên hai tệp v1 để không làm lệch GHIM-B1A của B2;
  - năm < 1000 ⇒ khung không biểu diễn được, ở CẢ HAI phía.

## Số đo lúc soạn (2026-11-25, `master` `437257a3`, Python 3.13.18, `jsonschema` 4.26.0)
- Khối v1 trên hai tệp v1, không `--dot-bien`: dòng FIXTURE `480/480` + `TONG: DAT`, rc 0, 2,50 s. Có `--dot-bien`: `DOT BIEN: giet 249/249 · vi tu 57 · noi long schema 192`, `TONG: DAT`, rc 0, 212 s (chạy song song với lượt v2 trên cùng máy, nên số giây cao hơn chạy riêng).
- Khối v2 trên hai tệp v2 bản r1 (fixture `5a8b7050…`): không `--dot-bien` ⇒ `486/486`; có `--dot-bien` ⇒ `giet 250/250`, 217 s (chạy song song với lượt v1).
- Khối v2 (băm không đổi giữa r1 và r2) trên fixture r2:
  - không `--dot-bien` ⇒ dòng `FIXTURE: 490/490 …` của mục 3 và `TONG: DAT`, rc 0;
  - có `--dot-bien` ⇒ `DOT BIEN: giet 250/250 · vi tu 58 · noi long schema 192`, `TONG: DAT`, rc 0, 214,7 s.
- Hai đột biến đích của mục 3, chạy trên bản sao: mỗi đột biến ⇒ `FIXTURE: 489/490`, `TONG: DO`, đúng một dòng `LECH` nêu đúng ca đích (`luat-C9-khung-nam-0999-khong-bieu-dien`; `luat-C4-rest-job-run-id-float-bang-gia-tri`).
- Lần chạy đầu của v2 (r1) lệch đúng 1 ca: `luat-C3-run-id-khac` ra `['C3','C4']`. Nguyên nhân là ca chỉ đổi `run.id`, nên `jobs[].run_id` lệch theo. Đã sửa FIXTURE (cho jobs cùng `run_id` mới để cô lập C3), không sửa oracle.
- `rest.jobs` của fixture v1 không có trường `run_id` nào. Đo bằng `json` trên tệp; 24 lần xuất hiện `"run_id"` đều nằm ở nơi khác.
- Bên thu tại base không đọc `jobs[].run_id`. Grep `"run_id"]` trong `ci_dang_ky_test.py` chỉ ra X4 dấu (dòng 1776) và oracle (C3, C11).
- Quét toàn ref ~07:3xZ (so tập tên, thiếu 0): `.claude/dev/ci_dang_ky_test.py` có NGƯỜI_GIỮ 1, là `wp1494-r5-g2-claude` (B2).

## Thay đổi
| revision | thay đổi |
|---|---|
| r1 | bản đầu |
| r3 | Checkpoint §12 sau N1-03 (`v1-not-fully-specified`, lần thứ 6). Quyết định chủ kho (b): §1 chỉ còn tính chất an toàn (1a–1e); bỏ biên ngoài cùng, bản dự phòng và lời hứa «luôn có biên nhận». Nghiệm thu 2 và bảng đột biến viết lại. Hiện vật `hop_dong/` và khối «Lệnh kiểm» không đổi. |
| r2 | Review lượt 1, 2 finding P2.<br>• `v1-not-fully-specified` (N1-01; lần tái diễn thứ 5): §1 viết lại — khoảng phủ 1a; lời hứa 1b không đặt điều kiện «hàm trả về»; danh sách loại trừ đóng 1c; bản dự phòng đủ trường bắt buộc, chỉ hai mốc `null` (1d); thứ tự gồm xoá `ra`, ghi nguyên tử, dự phòng, chẩn đoán làm hết sức (1e); lỗi đối số không xoá `ra` (1f). Nghiệm thu 2 viết lại thành 13 ca, mỗi ca chạy với `ra` vắng và với `ra` chứa sẵn biên nhận xanh; đột biến 15 mục.<br>• `mutant-oracles-non-discriminating` (N1-02): sửa ca 0999 cho khung đúng lịch; thêm ca `run_id` float và ca thiếu `run_id`; thêm hai đột biến đích, đã đo là bị giết; X1 dùng cùng miền kiểu. |
