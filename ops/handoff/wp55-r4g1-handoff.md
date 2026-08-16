# Bàn giao §7 — wp55 revision 4, generation 1

**Từ:** phiên executor `claude`, lease `wp55-r4-exec-1-claude-20260816`
**Tới:** phiên kế tiếp, để cấp lease REVIEW cho `codex`
**Ngày:** 2026-08-16

---

## Neo — đọc bằng SHA, không bằng tên nhánh

```yaml
packet_id: wp55
packet_issue: 55
mission_issue: 54
mission_revision: 6
revision: 4
phase_key: F3-03

spec_path: ops/specs/wp55-r4-spec.md
spec_branch: ops/wp55-r4-spec-draft
spec_sha256: 86d9627caf55ea2cb8e4caa29ef036fd490c190d8481fb4f79dd5d1703eb1afd
spec_duyet_boi: ducthangho          # trực tiếp trong phiên 2026-08-16

base_sha: 18da1da6a07ab2c86d716cef1d74ff2cd0e3218a     # tip master sau PR #129
start_from_sha: b0e3e3b6a4c630ba0652b8fc939025d9c4031c67
head_de_review: 2432e3f64f05739741dfe6f49081e9aaa140799f
branch: claude/wp55-r4g1-f3-03

attempts_used: 1
attempts_limit: 3
```

### Commit của lượt này, kèm lease mỗi commit chạy dưới (AC 26)

| sha | lease_id | nội dung |
|---|---|---|
| `179d5f37` | `wp55-r4-exec-1-claude-20260816` | merge master `18da1da` vào nhánh packet |
| `2432e3f6` | `wp55-r4-exec-1-claude-20260816` | AC 19 bỏ hẳn miễn trừ — xoá cơ chế, nối lại ma trận |

Không có commit nào ngoài sổ. Đây là chỗ revision 3 hỏng (bốn commit không lease), và AC 26 sinh ra để chặn.

---

## Số liệu — chép nguyên văn từ khối suite tự in (AC 25)

```
ca               : 185
đột biến         : 34
lớp lách         : 78
ca bắt-oan       : 35
ngoại lệ AC 18   : 0
```

Nền trước lượt này: `173 / 44 / 66 / 35 / 0`.

## Gate — `rc` THẬT từng lệnh, không đọc qua ống

| phép đo | rc |
|---|---|
| `doctrine-scan` trên nhánh | `0` — 4 tệp |
| suite trên nhánh | `0` — ĐẠT |
| bộ tái lập 24 ca | lệch `0/24` · trước khi vá `10/24` |
| **AC 20** `doctrine-scan` trên cây ĐÃ MERGE | `0` |
| **AC 20** suite trên cây ĐÃ MERGE, có `GIT_DIR` | `0` |
| **AC 20** suite BỎ `GIT_DIR` — chứng đường | `1` |

Dòng cuối là phép đo cố ý: nếu bỏ `GIT_DIR` mà vẫn xanh thì điều kiện spec vừa thêm là thừa
và cả AC 20 chỉ là nghi lễ. Nó đỏ (`fatal: not a git repository`), nên finding
`ac20-archive-tree-suite-not-self-contained` hoãn từ verdict lượt 6 đã đóng THẬT.

Công thức đã dùng, nguyên văn:

```bash
MASTER=18da1da6a07ab2c86d716cef1d74ff2cd0e3218a
TREE=$(mktemp -d)
git archive "$MASTER" | tar -x -C "$TREE"
git diff --binary 18da1da..2432e3f6 | git -C "$TREE" apply
python3 -B "$TREE/.claude/dev/packet_loop.py" doctrine-scan --root "$TREE"
GIT_DIR="$PWD/.git" python3 -B "$TREE/.claude/dev/packet_loop_test.py"
```

Phạm vi diff: đúng 6 tệp `write_set`, không ra ngoài.

---

## Đã làm

**AC 19 mục 2 — xoá, không vô hiệu.** `packet_loop.py` từ `1503` xuống `1223` dòng.

Xoá: `_duoc_tha_vi_ngat_dong`, `_dong_khoi_ma`, `_dong_bang_html`, `_go_dau_dong_tho`,
`_CO_CHU`, `_RE_DAU_DONG_THO`, `_RE_HANG_RAO`, `_RE_MO_BANG`, `_RE_DONG_BANG`,
`_RE_MA_INLINE`, `_RE_COMMENT_MOT_DONG`, `_DAU_HIEU_PHEP_DO`, `CUM_NGON_NGU_THUONG`.

Giữ: `_go_dau_dong` (còn dùng bởi `_khuc_chuan`), `_RE_DAU_DONG`, `_dong_tai`. Không còn
tham chiếu nào tới cơ chế miễn trừ ngoài một khối chú thích lịch sử — khối ấy cố ý giữ, kèm
danh sách kiểm ba lớp lỗi sẽ quay lại nếu một revision sau mở lại miễn trừ.

**Bốn finding lượt 10 — tái lập độc lập trên head thật.** Cả bốn đóng cùng lúc, không vá gì
thêm, đúng như spec dự đoán. AC 22–24 vì thế rút được.

**AC 19 mục 3–4 — ma trận.** Xem mục "ngược spec" ngay dưới.

---

## BA CHỖ NGƯỢC VỚI SPEC — khai ở đây để reviewer không phải tự tìm

### 1 · Spec đoán HAI ca đổi ma trận. Đo thật: MƯỜI HAI.

Phân hoạch sạch: 12 ca đỏ đúng bằng 12 ca **có chứa** cụm cấm; 23 ca không chứa vẫn xanh.
Không ca nào đỏ vì lý do khác — hợp đồng cơ học chạy đúng thiết kế. Chênh lệch là do spec
mới mô phỏng chứ chưa chạy trọn suite; spec đã nói trước "có thể còn ca khác".

Cách nối lại:

- 12 bản GỐC sang `LOP_LACH`, tên `cum_don_*_tha_cu`, kèm lý do ghi tại chỗ (AC 19 mục 4).
- 12 tên CŨ ở lại `LOP_BAT_OAN`, **viết lại nội dung giữ Y HỆT hình dạng** — bảng chưa đóng
  thẻ, rào bốn backtick, dòng thụt lề, mã inline, comment, bullet, danh sách số, trích dẫn
  — chỉ đổi cụm sang `tên thuộc / danh sách cho phép`.
- 23 ánh xạ AC 18 giữ nguyên nhờ giữ nguyên tên; thêm 12 ánh xạ cho lớp mới.

**Chỗ đáng soi nhất của lượt này:** cặp cùng-hình-dạng ấy là thứ chứng minh cổng phân biệt
NỘI DUNG chứ không phân biệt cấu trúc Markdown. Nếu reviewer thấy một hình dạng nào đó chỉ
có mặt ở một vế của cặp, đó là finding thật.

### 2 · Số dòng mã chết

Spec ước lượng `~241 dòng, ≈16% tệp`. Đo thật: **280 dòng, 18,6%**. Và `_RE_BANG_HTML` mà
spec liệt kê trong danh sách phải xoá **KHÔNG TỒN TẠI** trong tệp.

### 3 · Mười hai đột biến mất mỏ neo

Chúng nhắm vào máy dò cấu trúc phục vụ miễn trừ, mà máy ấy đã bị xoá. Thay bằng HAI cái cùng
họ, đo hai bề rộng của cùng một sai lầm:

| đột biến | giết | phủ |
|---|---|---|
| `mo_lai_mien_tru_ngat_dong` | 37 ca | hình dạng generation 6–9 |
| `tha_vo_dieu_kien_nhu_generation_4` | 43 ca | thêm 6 lớp MỘT DÒNG mà cái trên không với tới |

Cần cả hai: suite báo thẳng *"6 lớp KHÔNG đột biến nào giết"* khi mới có cái thứ nhất. Cả hai
danh sách phải-chết **đo được** — chạy scanner đã đột biến trên từng ca của `LOP_LACH` rồi lấy
đúng những ca trả `rc=0` — không kê tay. Đây là finding `packet-suite-mutation-count-mismatch`
của lượt 9 được tôn trọng.

---

## Hai khuyết của spec đã sửa TRƯỚC khi chạy (lý do `spec_hash` khác lúc chủ kho duyệt)

Chủ kho duyệt bản băm `271b88f9…`. Sau khi duyệt, đo ra hai khuyết cưỡng chế, nên băm chốt là
`86d9627c…`. Cả hai khai trong lease ở trường `sua_sau_khi_duyet`.

1. **`start_from_sha: 1a4525a` bỏ mất bản vá P1 an ninh.**
   `git merge-base --is-ancestor 4085bbf2 1a4525a` → SAI; với `b0e3e3b6` → ĐÚNG.
   `4085bbf2` vá chỗ `SKILL.md` nối `${VAR:+…}` với `${VAR:-…}` — nhánh "đã đặt" bung ra
   CHÍNH GIÁ TRỊ biến bí mật. `SKILL.md` nằm trong `write_set`, nên xuất phát từ `1a4525a`
   là **mở lại lỗ ấy trong im lặng**.

2. **Nhánh packet đỏ vì `CLAUDE.md` của master CŨ.** Trên `b0e3e3b6`: r3g5 `rc=0` nhưng mô
   phỏng r4 `rc=6` tại dòng 82. Bản vá đã nằm trên master `18da1da`, nên phải merge master
   trước khi đo. Đã merge ở `179d5f37`.

---

## Việc CHƯA làm, nói ra thay vì để reviewer phát hiện

1. **Lỗ hook token xoay** — chốt "không ghi đè khi đã đăng nhập" tin `codex login status`, mà
   lệnh ấy chỉ đọc TỆP chứ không hỏi máy chủ; ngày 16-08 nó báo `Logged in` với một token ĐÃ
   THU HỒI. Lỗ thật, **ngoài `write_set`**, cố ý không đóng ở lượt này.
2. **Sổ attempts của revision 3 không khớp thực tế** — bốn commit chạy không lease. Revision 4
   không hồi tố sửa được; AC 26 chỉ chặn tái diễn.
3. **Chưa chạy `ruff`/gate phát hành đầy đủ** trên nhánh này — `packet_loop*.py` là công cụ
   dev-side, không vào gói, nhưng nếu reviewer muốn thì đó là phép đo thiếu.

---

## Việc của phiên nhận bàn giao

Cấp **lease REVIEWER** cho `codex` (§8 — executor là `claude` ⇒ reviewer phải khác provider),
neo `reviewed_sha_required: 2432e3f64f05739741dfe6f49081e9aaa140799f`.

Lease + prompt đặt trên một nhánh `ops/**`; workflow `ops-publish-lease.yml` sẽ chiếu lên #55.
Chạy `python3 ops/lease_publish.py check <tệp>` trước khi đẩy, và **kèm chứng đường** — đổi
một byte của prompt phải cho `rc=6`, khôi phục phải cho `rc=0`. Không có chứng đường thì dòng
"khớp băm" chỉ là lời khen.

### Bốn chỗ đáng đặt làm mục kiểm của prompt review

1. Cặp cùng-hình-dạng giữa `LOP_LACH` và `LOP_BAT_OAN` có thật sự phủ mọi hình dạng không.
2. Hai đột biến mới có nhắm đúng tầng không, hay giết cả đối chứng khác họ.
3. `280 dòng / 18,6%` và `37 / 43` — tái lập, đừng nhận theo lời kể.
4. Mã chết: còn hàm/hằng nào phục vụ miễn trừ sót lại mà chỉ bị vô hiệu chứ không bị xoá không.

### Công cụ — đo trước, đừng suy từ tài liệu

GitHub: dùng **`https://api.githubcopilot.com/mcp/`** với `Authorization: Bearer $GITHUB_PAT`.
`api.github.com` trả 403 và là ngõ cụt. Toolset `actions` (đọc trạng thái gate) KHÔNG có ở
endpoint mặc định — nó nằm ở **`https://api.githubcopilot.com/mcp/x/actions`**. Đây không phải
chuyện thiếu quyền PAT; đã đo bằng `tools/list` trên cả hai endpoint.
