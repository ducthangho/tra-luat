# VERDICT — cross-review MÃ packet wp488 slice A0, lượt 4

- verdict: **`approve`**
- reviewed_sha: `826bc36fd1801bf828f21bf9580897899f16a299`
- reviewed_base: `c0a5cbe89a90588115262e1a2c3ac84cbd98be9e`
- reviewed_spec_sha256: `465538364b1a3f9477782fba79869bbd1c9351140e3fa9df50451baae22f9c79` (SPEC.md r9)
- reviewed_adr0047_sha256: `b9975929c52e12767417b46b47829c265230117fe65df6a9fd22540d4868fdab`
- reviewed_files_sha256:
  - `ops/lease_publish.py` = `f5ae7bbcc6509f96036de3ce0877322162c1e5172cd5d8c4a28578a7fbd06f6d`
  - `ops/lease_publish_test.py` = `d2b8a50b58ae3d956cff233278ff955ee39cac5d9803dcd92ffe1f8241e0f90a`
  - `.github/workflows/ops-thu-hoi-admission.yml` = `f7e5fd2d0fb38caa064632355fd98d51acd2fddbe03886754ead848db443ea62`
- model_tu_khai: `claude-fable-5` (system prompt của lượt này khai "You are powered by the model named
  Fable 5. The exact model ID is claude-fable-5" — một model duy nhất suốt lượt, không lẫn nhãn)
- review_round: 4
- Kết luận một câu: bản vá `457affd..826bc36` đóng ĐÚNG và CHỈ ba finding của Codex connector, đóng đúng
  chỗ ở CẢ reader lẫn consumer, không mở lỗ mới, không chặn oan chỗ nào spec cho phép; **0 P1, 0 P2
  executor vá được trong packet** ⇒ `approve`. HINT.patch 0 hunk.

## Khai báo nhiễm ngữ cảnh
Harness đã TỰ BƠM nội dung `cay-kho/CLAUDE.md` và danh sách skill `cay-kho/.claude/skills/**` vào ngữ cảnh
ngay sau lệnh Read đầu tiên trỏ vào `cay-kho/ops/lease_publish.py` (đúng hiện tượng lượt 2/3 đã khai).
Reviewer KHÔNG dùng nội dung ấy và KHÔNG gọi skill nào từ đó: mọi hợp đồng lấy từ `SPEC.md`, `ADR-0047.md`,
`EVIDENCE.md`, `VERDICT.luot1..3.md` và ba tệp của diff; git chạy `git -C cay-kho …` từ cwd; suite chạy trong
subshell `(cd cay-kho && …)`. Không đọc `cay-kho/CLAUDE.md`, `cay-kho/docs/PROTOCOL_DA_PHIEN.md`,
`cay-kho/.claude/**`, `cay-kho/ops/reviews/**` bằng bất kỳ lệnh nào (với `ops/reviews` chỉ liệt kê TÊN tệp
qua `git diff --name-only` cho phép đo drift, không đọc nội dung).

## Bản vá so ba finding Codex
Diff `457affd..826bc36`: mã +46/−10, test +72/−3, workflow **0** (numstat tự đo, khớp lời khai). Từng hunk:

| hunk | thuộc finding | nhận xét |
|---|---|---|
| `kiem_ban_ghi_thu_hoi`: `sorted(thua, key=repr)` | C3 | `repr` tổng trên mọi khoá YAML tạo được (dict key luôn hashable; list-key đã chết ở loader ⇒ 12) |
| `KhoObject.tim`: tổ tiên non-tree ⇒ `Chan 12` thay `return None` | C1 reader | đúng một điểm nghẽn: `namespace` (S/T), policy `PATH_POLICY_CLOSURE`, `PATH_BO_KIEM` đều đi qua `tim` |
| `_ls_tree_z(..., de_quy=False)` | C1 consumer (hạ tầng) | nhánh `de_quy=True` GIỮ NGUYÊN từng byte lời gọi (`ls-tree -r -z`, một occurrence duy nhất — grep); anchor mutant `F02-bo-z` là substring 8-space nằm trong dòng 12-space nên vẫn khớp, t139 tự cưỡng chế `count==1` và mutant vẫn GIẾT (suite đo) |
| `_kiem_to_tien_la_tree` + lời gọi đầu vòng `_quet_so_thu_hoi_moi_ref` | C1 consumer | hỏi đúng tiền tố thật (`ops`), chỉ raise khi entry ĐÚNG TÊN mà không phải tree; `ops` vắng hẳn ⇒ đi tiếp (positive control rc 0); chi phí +1 lời gọi `ls-tree` mỗi ref (một tiền tố) |
| `_doc_blob_text_12` | C2 (hạ tầng) | thay khối try/except F10 của đường policy, CÙNG ngữ nghĩa rc: vắng/rc≠0 ⇒ None ⇒ 12 ở caller; không UTF-8 ⇒ 12 (thông điệp chính xác hơn bản cũ, cùng mã 12); tái dùng cho đọc marker — nằm trong phạm vi tối thiểu của C2 |
| `_kiem_so_rong_khi_chua_kich_hoat`: `kiem_metadata_retired(...)` TRƯỚC policy | C2 | đúng thứ tự Q13 "mọi lỗi metadata ⇒ 12"; `or b""` đỡ blob vắng (đo: 12, không AttributeError) |
| test: t129 đổi control, t139 +4 mutant (33→37), t151 mới | C1/C2/C3 | xem mục t139/t151 dưới |

**Không có dòng nào ngoài ba finding.** Hai helper (`de_quy`, `_doc_blob_text_12`) là hạ tầng tối thiểu mà
C1-consumer/C2 cần, không đổi hành vi đường cũ (đo: suite 146/146, mutant F02-bo-z vẫn chết, ruff delta 0).

## C1–C3 → trạng thái
**C1 — ĐÓNG, đúng cả hai chỗ.**
- Reader (`tim`): ops=blob ⇒ 12, ops=symlink ⇒ 12 (t151 + repro executor 5/5), ops=gitlink ⇒ 12
  (probe C-P1, "mode 160000 commit"); `TAP_THU_HOI_RONG` không in ở mọi ca trên. "Vắng thật" vẫn là vắng:
  `tim("ops/khong-co")` = None (t129 giữ), H xoá hẳn `ops` ⇒ rc 0 + `TAP_THU_HOI_RONG` (positive control t151).
- `namespace` khi `ops` là symlink trỏ `docs` (tree) ⇒ 12 — **KHÔNG chặn oan**: SPEC dòng 323 đòi
  *"'Sổ vắng' cần chuỗi tree cha đã băm chứng minh entry vắng"* và dòng 312 *"không suy 'sổ vắng'"*; hợp đồng
  alias/symlink (Q3, `max_tree_or_alias_edges` Q4.5: đếm bước tree-entry + dereference symlink trên MỘT lần
  resolve) là hợp đồng của **closure write-set khi ĐÃ kích hoạt**, không phải của reader sổ A0 — và ngay Q3
  mọi ca mơ hồ cũng ⇒ 12. Reader A0 không dereference nên budget không đổi ngữ nghĩa (S8 mutant vẫn bị t131 ghim).
- Consumer (`_kiem_to_tien_la_tree`): ops=blob ⇒ 12 (t151), symlink ⇒ 12 (C-P2), gitlink ⇒ 12 (C-P3);
  ops VẮNG ⇒ đi tiếp đúng. Đồ giả `_GitKhoGia` bỏ qua cả pathspec lẫn `-r` (trả mọi entry của ref) ⇒ guard
  thành no-op dưới đồ giả — test cũ t89/t94-lớp không bị đỏ oan (suite xanh), và răng của guard được đo bằng
  git THẬT ở t151/t139, đúng chỗ cần đo.
- `.github` là blob (tổ tiên của policy) ở T ⇒ 12 "tổ tiên" (C-P8) — không suy "policy vắng". `PATH_BO_KIEM`
  đọc qua `tim` tại S — S có ops blob thì đã 12 từ `namespace(tree_S)` trước đó; cùng điểm nghẽn.
- Tree TRÙNG TÊN khác kiểu (crafted, OID băm đúng bytes): reader `KhoObject.tree` ⇒ 12 "trùng" (C-P10a — chốt
  `ten in da_thay` có sẵn từ F03); consumer ⇒ 12 vì `ls-tree` liệt kê cả hai entry và guard bắt entry non-tree
  (C-P10b). Fail-closed cả hai đường.

**C2 — ĐÓNG.** Marker rác + policy `{}` ⇒ 12 (t151 + repro); marker đúng schema + `{}` ⇒ **0** — không chặn oan
(t151). Biến thể đều 12 tại consumer: mode 100755 (C-P4), marker là symlink — mode 120000 (C-P5),
`retired_at_utc` tương lai (C-P6); blob vắng ⇒ `b""` ⇒ 12 "phải là mapping", không AttributeError (C-P9a).
Thứ tự đúng Q13: marker validate TRƯỚC policy. **Text-mode/CRLF:** `GOI_GIT(text=True)` chuẩn hoá `\r\n`/`\r`
→ `\n` trong `_doc_blob_text_12`; đo marker CRLF hợp lệ ⇒ rc 0 (C-P7) và KHÔNG có lệch chấp nhận giữa hai
đường đọc: YAML vốn nhận CRLF/CR làm ngắt dòng nên reader M4 (bytes thô đã băm qua `kho.doc`) cũng nhận;
consumer không băm byte marker/policy nên laundering không chạm phép so băm nào (first_policy_sha256 chỉ được
so ở reader, trên bytes thô). Cùng kiểu đọc với đường policy F10 đã duyệt lượt 2/3 — ghi nhận, không finding.

**C3 — ĐÓNG.** Khoá thừa lẫn kiểu ⇒ 8 kèm thông điệp (t151, repro; C-P9c với None/bool/int ⇒
`khoá thừa [2, None, True]`). Quét TOÀN BỘ sorted/so-sánh trên khoá không tin cậy trong khối A0:
`sorted(map_T.items())` (1743) — khoá là f-string path (str thuần); `sorted(nguoi_giu)` (1860) — khoá đã
`str(...)`; `set(d) != set(_KHOA_RETIRED)` — không sort; `kiem_mien_ho_so` `sorted(hoso)` (1180) — `hoso` do
`hoso_adapter_do()`/caller nội bộ dựng, khoá str cố định, không phải dữ liệu đối phương (discovery production
bị chặn 12 từ `PROFILE_ADAPTER_DA_DUYET` rỗng — A2); `_nap_yaml_khong_trung_khoa` với khoá unhashable —
TypeError nổ TRONG `yaml.load` và bị `except Exception` bắt ⇒ Chan 12, đo C-P9b. Không còn site C3-lớp.

## Cùng lớp — đã tìm ở đâu, thấy gì
Câu hỏi đặt ra: ba lượt trước sót một P1 cấu trúc — còn chỗ nào cùng lớp "tin cấu trúc chưa xác minh / suy
vắng từ đường hỏng"? Đã rà từng đường đi qua cây:
- `tim` — vá lượt này, đo blob/symlink/gitlink (trên), budget giữ nguyên.
- `namespace` — chỉ gọi `tim` + `tree`; đích non-tree ⇒ 12 (F02 cũ, t142); tổ tiên non-tree ⇒ 12 (mới).
- `KhoObject.tree` — parse bytes đã băm, whitelist mode, cấm `/`／`.git`／trùng tên (F03) — đo C-P10a.
- `_ls_tree_z` — rc≠0/OSError/decode ⇒ 12; entry hỏng ⇒ 12; `de_quy=False` chỉ thêm nhánh hỏi kiểu.
- `_quet_so_thu_hoi_moi_ref` — chính `ops/thu-hoi` non-tree ⇒ 12 (F02 cũ); tổ tiên ⇒ guard mới; lọc path
  trong mã, entry gitlink/thư mục con trong sổ đi tuyến `thu_hoi` ⇒ 12 ở M1/consumer (docstring
  `phan_tuyen_so` + t127).
- `PATH_POLICY_CLOSURE` tổ tiên (`.github`, `.github/coordination`): reader ⇒ 12 qua `tim` (C-P8);
  consumer đọc `cat-file blob ref:path` — tổ tiên hỏng làm cat-file rc≠0 ⇒ None ⇒ **12** (fail-closed,
  dòng 1642), không suy "policy vắng ⇒ 0" vì nhánh này chỉ chạy khi ĐÃ có marker, mà marker + policy vắng ⇒ 12.
- `PATH_BO_KIEM` — qua `tim` tại S, cùng điểm nghẽn.
- Hai hàm DU_BAO — chạy SAU `_kiem_so_rong_khi_chua_kich_hoat` trên cùng tập refs (gồm cả
  `refs/remotes/*` — `_cac_ref_cuc_bo` dòng 308), nên mọi ref chúng chạm đã qua guard tổ tiên; không có
  đường rò rc mới (mutant `M3-du-bao-doi-rc` vẫn bị t135 giết — catalog).
- Đồ giả `_GitKhoGia` — không mô hình non-tree ancestor được (bỏ qua pathspec/`-r`), nên không sinh xanh giả
  cho guard: mọi ca chịu lực của C1 dùng git thật.
Kết quả: **không tìm thấy chỗ cùng lớp còn hở trong write set**. Hai chỗ cùng lớp NGOÀI write set (mã có sẵn
trước packet, diff +919/−0 không chạm): `_quet_lease_toan_kho` (luật cũ) không có chốt tổ tiên — nhưng trong
`ai-dang-giu` guard A0 chạy cùng lệnh nên bề mặt consumer vẫn 12 (đo C-P2/P3); còn `con-tro-treo` (advisory,
rc 0 theo thiết kế) dùng luật cũ trần — ghi ở "Còn mở có chủ", đúng như EVIDENCE đã khai.

## Findings mới
Không có P1. Không có P2 executor vá được trong packet. Ba ghi nhận P3 (không đổi verdict, không cần vá lượt này):
1. (P3) `_doc_blob_text_12` không bắt OSError (git không gọi được ⇒ traceback rc 1) — Y HỆT hành vi khối
   F10 cũ nó thay (cũng chỉ bắt UnicodeDecodeError), và trong cùng lệnh `_ls_tree_z` đã chạy trước đó bắt
   OSError ⇒ 12; cửa sổ thực tế ~0. Nếu muốn, A1 thêm `except OSError ⇒ 12` cho đối xứng.
2. (P3) Laundering text-mode (`\r`→`\n`) ở consumer — mô tả ở mục C2; không lệch chấp nhận đo được, reader
   thẩm quyền dùng bytes thô. Giữ nguyên là chấp nhận được; nếu A1 thêm phép so băm marker thì PHẢI chuyển
   consumer sang đọc bytes thô trước.
3. (P3, ghi để A1 khỏi quên) `_du_bao_check` dòng 1672 `.stdout.encode` không đỡ decode (EVIDENCE tự khai).
   Tại HEAD này nó KHÔNG với tới được với blob không-UTF-8: guard C2 đã validate mọi blob metadata (UTF-8)
   trong cùng lệnh TRƯỚC khi DU_BAO chạy, và bản ghi `thu_hoi` ⇒ 12 trước DU_BAO; chỉ thành đường sống khi
   `SO_THU_HOI_KICH_HOAT=True` (A1 — packet khác, review riêng). Bản vá C2 vô tình ĐÓNG luôn reachability ở A0.

## Còn mở có chủ
(giữ nguyên từ lượt 2/3 + EVIDENCE — KHÔNG phải lý do changes_requested cho executor)
- F07: pin `upload-artifact` bằng commit SHA (chủ kho cấp SHA đã readback).
- F08: manifest ADR-0047 lớp 2 đủ trường; `PROFILE_ADAPTER_DA_DUYET` rỗng chờ chủ kho duyệt.
- `DESCRIPTOR_Q13_SHA256 = None` — ghim ở A1 từ readback comment.
- Q7 / ADR-0044 packaging.
- Ngoài packet: `_quet_lease_toan_kho` (luật cũ) cùng lỗi quote F02 + không có chốt tổ tiên non-tree
  (bề mặt `ai-dang-giu` đã được guard A0 che — đo; `con-tro-treo` còn trần); `_du_bao_check` decode (mục P3.3).

## Mutant đã chạy
Catalog t139 (trong suite, git thật + module bản sao, mỗi mutant một tệp, `dont_write_bytecode`):
**mẫu số=37, giết thật=34, SỐNG có chủ đích=3, tín dụng giả=0** — khớp lời khai; t139 tự cưỡng chế neo duy nhất
(`nguon.count(cu)==1`) và phân hạng bằng lớp `TinHieuChotCa` (mã sản phẩm không giả được).
Mutant ĐỘC LẬP của reviewer (bản sao HEAD trong `scratch/luot4/`, chạy `t151` qua override `_nap_cong` —
`scratch/luot4/probe_luot4.py`, 20/20):
| mutant | kết quả | chết ở chốt |
|---|---|---|
| B1 `tim` raise → `return None` | ĐỎ TinHieuChotCa | "M4: ops=blob phải 12, không được kết luận sổ rỗng: 0 'THU_HOI_ADMISSION TAP_THU_HOI_RONG…'" — đúng chốt reader |
| B2 bỏ `_kiem_to_tien_la_tree` | ĐỎ TinHieuChotCa | "consumer: ops là blob phải 12, không suy sổ vắng: 0" — đúng chốt consumer |
| B3 bỏ `kiem_metadata_retired` ở consumer | ĐỎ TinHieuChotCa | "consumer marker rác + policy {} phải 12: 0" — đúng chốt C2 |
| B4 bỏ `key=repr` | ĐỎ TinHieuChotCa | "sorted ném TypeError thay vì Chan 8: '<' not supported…" — đúng chốt C3 |
| B5 (thêm của reviewer) guard yếu `loai == "commit"` | ĐỎ TinHieuChotCa | t151 ghim CẢ LỚP non-tree, không chỉ sự có mặt của lời gọi |
Hai chiều trên module `457affd` (A1/A2): `t151` ĐỎ TinHieuChotCa — tái hiện ĐÚNG P1 gốc (rc=0 +
`TAP_THU_HOI_RONG` in ra); `t129` ĐỎ TinHieuChotCa ("tim qua blob phải 12… 0 None"). Trên HEAD cả hai XANH
(suite). Sửa positive control t129 là HỢP LÝ: "đường XUYÊN blob" nay 12 theo hợp đồng SPEC dòng 323, còn
control "vắng thật = None" (`ops/khong-co`) vẫn giữ — hai khái niệm tách bạch đúng.

## Bảng đo lại
| phép đo | executor khai | lượt 4 đo | khớp |
|---|---|---|---|
| head / base / origin/master | `826bc36` / `c0a5cbe` / `28ba133` | y hệt (`git rev-parse`) | ✓ |
| numstat `c0a5cbe..826bc36` | +141 · +919 · +1327−1 = +2387/−1, 3 tệp | y hệt; write set ĐÚNG 3 đường của spec §write_set A0 | ✓ |
| numstat `457affd..826bc36` | wf 0 · mã +46/−10 · test +72/−3 | y hệt | ✓ |
| sha256 3 tệp tại head | `f5ae7b…`/`d2b8a5…`/`f7e5fd…` | y hệt (`sha256sum`) | ✓ |
| t139 catalog | 37 = 34 giết / 3 SỐNG / 0 tín dụng giả | y hệt (dòng in trong suite) | ✓ |
| suite tại head | 146/146 (wrapper có actionlint) | 144/146 khi PATH mặc định (2 đỏ = t33/t137 "KHÔNG ĐO ĐƯỢC: thiếu actionlint"); chạy lẻ 2 ca với `PATH=/tmp/actionlint` ⇒ cả hai ĐẠT ⇒ hợp thành 146/146, 0 bỏ qua | ✓ (điều kiện đo ghi rõ) |
| repro Codex | 457affd 0/5 · 826bc36 5/5 | 826bc36: **5/5 XANH** (chạy nguyên bản); phía 457affd đo bằng bằng chứng tương đương: t151+t129 ĐỎ trên module 457affd + B1–B4 hoàn nguyên từng chốt đều ĐỎ | ✓ (bản chất) |
| ruff F | mã 0; test 4 có sẵn, delta 0 | mã 0; test 4 tại HEAD **và** 4 tại 457affd (đo cả hai phía) ⇒ delta 0 | ✓ |
| workflow từ 457affd | không đổi | numstat 0 dòng; sha256 khớp giá trị lượt 3 | ✓ |
| master drift ∩ write set | ∅ (2 merge: reviews/ CHANGELOG/ manifest/ land) | `git diff --name-only c0a5cbe..origin/master` (chỉ TÊN): không tệp nào thuộc write set | ✓ |
| `SO_THU_HOI_KICH_HOAT` | False | dòng 929 = `False`; verdict sản phẩm luật cũ: t53/t135 ĐẠT trong suite + mutant `M3-du-bao-doi-rc` bị giết | ✓ |
| không chạm packet_loop / ops/thu-hoi / ops-publish-lease / ci.yml | đúng | diff toàn packet chỉ 3 tệp khai | ✓ |
| actionlint 1.7.7 + shellcheck | rc=0 (đo lượt 3, wf không đổi) | gián tiếp qua t33 + t137 ĐẠT (`PATH=/tmp/actionlint`, shellcheck `/usr/bin`) | ✓ |

## chua_do_duoc
- CI GitHub run trên `826bc36` (không mạng trong sandbox) — nhận theo lời khai, không tự đo.
- `doctrine-scan` / `doc-claims-check`: công cụ nằm trong `cay-kho/.claude/dev/**` (thư mục cấm đọc của
  phân công) — không chạy để giữ sạch lệnh cấm; các số 7 tệp/0 · ok:true nhận theo lời khai, không ảnh
  hưởng verdict mã.
- Con số nguyên văn "0/5 trên 457affd" của repro: không chạy lại script trên module cũ nguyên trạng (script
  nạp module HEAD); thay bằng bằng chứng tương đương đã ghi ở Bảng đo lại (mỗi finding có hoàn nguyên riêng
  ĐỎ đúng chốt) — bản chất lời khai ĐÃ kiểm.
- Lời khai suite "AL_VER=1.7.7 bash ops/chay_lease_publish_test.sh 146/146" qua wrapper: không chạy wrapper
  (script shell của kho, không cần cho verdict); đo bằng suite python trực tiếp + 2 ca actionlint chạy lẻ như trên.
