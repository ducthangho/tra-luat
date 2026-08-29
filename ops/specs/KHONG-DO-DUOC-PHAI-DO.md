# ĐẶC TẢ PACKET — `KHONG-DO-DUOC-PHAI-DO`

| | |
|---|---|
| `packet_id` | `KHONG-DO-DUOC-PHAI-DO` |
| `packet_issue` | **#401** |
| `revision` | 1 |
| `executor` | `claude` |
| `environment` | `cloud` |
| `review_class` | **`sensitive`** |
| `base` | `master` `3922add4` (đo `17:32:22Z 29-08-2026`) |
| `risk` | `sensitive` |

## `nguon_cap_viec`

Sổ nợ **#395**, mục **N6**, đã đính chính chiều bằng comment
[`5463823573`](https://github.com/ducthangho/tra-luat/issues/395#issuecomment-5463823573).
Packet Issue **#401**. Đây là packet **khắc phục** khuyết tật còn lại sau `#361` r4/r5.

## `review_class` — vì sao `sensitive`

`.claude/dev/ci_dang_ky_test.py` **không** khớp tiền tố nào trong `_BANG_LOP` của
`ops/lease_publish.py`, và `_tinh_lop_tu_write_set` mặc định `"sensitive"` (fail-closed).
Gọi chính hàm ấy, đo `17:29Z 29-08-2026`:

```
_tinh_lop_tu_write_set(['.claude/dev/ci_dang_ky_test.py']) -> 'sensitive'
```

Trần `ADR-0044` cho `sensitive`: **≤ 3 tệp và ≤ 300 dòng thêm**.

## `write_set`

| type | path |
|---|---|
| `exact` | `.claude/dev/ci_dang_ky_test.py` |

**Một tệp.** Đặc tả này và lease của nó land bằng **PR RIÊNG**, không nằm trong write set của packet.

Đo `17:32:22Z 29-08-2026`: lease đang giữ đường này = **0** (`rc=0, NGƯỜI_GIỮ 0`);
PR mở #394 và #389 **không** chạm đường này; blob hiện tại `436fc32a`.

## `ngoai_pham_vi`

| thứ CỐ Ý không làm | lý do |
|---|---|
| **N5** — `subagent_ghi_detect_test.py` rc=1 trên Windows | nguyên nhân khác họ; packet riêng. Đây là thứ đang làm bước 13 đỏ, nhưng chữa nó không chữa việc cổng làm tròn lên |
| **N7** — bước 13 chậm 2,91× | bài toán hiệu năng, chưa đo được nguyên nhân |
| thêm neo `github-actions/windows` vào `CACH_LY` | làm vậy là **KHAI** rằng nợ neo cho linux tái hiện **cùng nguyên nhân** trên windows. Chưa đo được. `soan-spec` §L5: một lời khai không phải một phép đo |
| sửa `.github/workflows/ci.yml` | cổng gọi `--chay` ở đúng d.130 và lời gọi ấy không cần đổi |
| sửa `ops/leases/**` | dọn dữ liệu và vá cổng là hai rủi ro khác nhau |

## `muc_tieu`

Mỗi mục chiếu vào đường dẫn duy nhất trong `write_set`:
`.claude/dev/ci_dang_ky_test.py` (viết tắt **[CDK]** dưới đây).

1. **[CDK]** Tách quyết định "trạng thái thứ ba có tính là ĐỎ không" thành **một hàm thuần**
   (đề xuất `dem_la_do(chap_nhan, trong_ci) -> bool`), để bất biến được cưỡng chế **ở tầng tiêu thụ**
   chứ không chỉ ở vị từ `cach_ly_chap_nhan`.
2. **[CDK]** Nhận diện "đang ở trong CI" bằng `GITHUB_ACTIONS == "true"` — **độc lập** với
   `moi_truong_hien_tai()`, vốn đòi thêm `RUNNER_OS == "Linux"`.
3. **[CDK]** `chay_moi()` d.140: khi `chap_nhan is None` **và đang ở trong CI** ⇒ **tính là ĐỎ**
   (`do += 1`) và in dòng nêu rõ đây là ĐỎ vì không đo được. Ngoài CI ⇒ in cảnh báo, **không** tính.
4. **[CDK]** Bổ sung phản chứng canh ở **tầng tiêu thụ**, vì đột biến sẵn có
   `r4-khong-do-duoc-thanh-dat` (d.211) chỉ canh vị từ và **đã xanh thật** trong khi cổng vẫn làm tròn lên.

## `nghiem_thu`

Mỗi tiêu chí nêu **phép đo làm nó ĐỎ** (`soan-spec` §L3).

| # | mục tiêu | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|---|
| A1 | 1, 3 | `dem_la_do(chap_nhan=None, trong_ci=True)` ⇒ `True` | đột biến `r6-khong-do-duoc-trong-ci-thanh-khong-dem`: đổi nhánh về `False` ⇒ ca phải ĐỎ |
| A2 | 3 | `dem_la_do(chap_nhan=None, trong_ci=False)` ⇒ `False` | đột biến `r6-ngoai-ci-cung-dem`: đổi về `True` ⇒ ca phải ĐỎ |
| A3 | 1, 4 | **Gỡ `do += 1` khỏi nhánh thứ ba trong `chay_moi()` phải làm ít nhất một ca ĐỎ** | đây chính là khuyết tật đã cho lỗi sống sót qua r4 và r5. Nếu gỡ mà mọi ca vẫn xanh thì bất biến vẫn ở sai tầng ⇒ tiêu chí **KHÔNG ĐẠT**, không làm tròn lên |
| A4 | 2 | `GITHUB_ACTIONS` khác `"true"` ⇒ `trong_ci=False`, kể cả khi có `RUNNER_OS` | đột biến `r6-coi-moi-noi-la-ci` ⇒ ca ngoài-CI phải ĐỎ |
| A5 | — | **Không hồi quy**: `ĐĂNG KÝ: 21/21`, `TRẠNG THÁI: chan=19 cach_ly=2`, và **mọi** đột biến cũ vẫn "ĐỎ đúng" (nền hiện tại 17/17) | chạy `python .claude/dev/ci_dang_ky_test.py` (không `--chay`) ⇒ `TỔNG: ĐẠT`, rc=0 |
| A6 | — | Trên Linux CI, `--chay` **vẫn ĐẠT**: môi trường giải ra `github-actions/linux`, hai bộ cách ly vẫn ra `CÁCH LY`, không phải ĐỎ | lượt `gate (ubuntu-latest)` trên nhánh packet phải `success` |
| A7 | — | Trên Windows CI, bước 13 in **ba** dòng đỏ (`mcp_gh_test.py`, `pretooluse_guard_test.py` vì không đo được + `subagent_ghi_detect_test.py` vì N5) thay vì một | lượt `gate (windows-latest)`: đếm dòng `CI_DANG_KY .*: ĐỎ`. **Đòi nhãn `windows` trên PR** (`ci.yml` d.43–48) và tốn ~50 phút ở hệ số 2× |

**A7 là tiêu chí đắt.** Nếu ngân sách không cho, khai thẳng **KHÔNG ĐO ĐƯỢC** cho A7 — không được
khai ĐẠT bằng suy luận từ Linux. Đó đúng là hình dạng lỗi mà packet này tồn tại để chặn.

## `hinh_dang_ke_thua`

**Họ hình dạng: "trạng thái KHÔNG BIẾT bị làm tròn lên thành trạng thái TỐT."**
Các lần đã có tên trong kho, đo `17:34Z 29-08-2026` bằng `grep` trên `docs/`, `ops/specs/`, `CLAUDE.md`:

| # | nơi | câu |
|---|---|---|
| 1 | `docs/PROTOCOL_DA_PHIEN.md:744` | *"cổng vắng mặt trông giống cổng xanh"* |
| 2 | `ops/specs/t33-doi-shellcheck.md:106` | cùng họ, `t33` chỉ trả 0 |
| 3 | `ops/specs/LEASE-DANG-WINDOWS-r3.md:33` (**Q8**) | *"Chưa thoả ⇒ khai KHÔNG ĐẠT, không làm tròn lên"* |
| 4 | `ops/specs/CONG-DUYET-THEO-THAM-QUYEN.md:11` | *"Ba trạng thái: có · không · KHÔNG ĐO ĐƯỢC — thứ ba làm cổng ĐỎ, không làm tròn lên"* |
| 5 | **packet này** | `chay_moi()` d.140 làm tròn lên |

Thêm hai biểu hiện cùng họ đã ghi trong #395 nhưng chưa thành luật viết:
*"bị giết trông giống chưa kịp đỏ"* (N5–N9) và **N11** (`merged=True` không chứng minh nội dung đã land).

**Kết luận bắt buộc theo `PROTOCOL §12`** (*"Cùng hình dạng lỗi xuất hiện lần thứ ba bắt buộc xem lại
có nên tiếp tục cách làm đó, không chỉ vá lần thứ tư"*): luật này đã được **viết thành luật ít nhất hai
lần** trong spec đóng băng (#3, #4) mà vẫn bị vi phạm ở một cổng khác. Vá lẻ từng cổng là cách làm
đang thua. Packet này vá **một** cổng và **không** giả vờ giải quyết cả họ; việc cưỡng chế họ này bằng
máy — một chỗ duy nhất — phải là packet riêng, và nên được mở ngay sau packet này.

## `chua_do_duoc`

- **Hồ sơ tiền nhiệm `#361` KHÔNG CÓ trong `ops/reviews/`** (`grep -rl '#361' ops/reviews/` ⇒ rỗng).
  Nên bộ đếm hình dạng lỗi của `#361` **không chép sang được**; bảng trên là phép đo mới của packet này,
  không phải bộ đếm kế thừa. `soan-spec` §L4 mất hiệu lực đúng ở chỗ nó cần nhất.
- **Nguyên nhân `rc=1` của N5** trên Windows — chưa đào, ngoài phạm vi.
- **Nguyên nhân bước 13 chậm 2,91×** (N7) — chưa đào.
- **Nợ neo cho linux có tái hiện cùng nguyên nhân trên windows không** — chưa đo. Đây là lý do packet
  này KHÔNG thêm neo windows.
- **Ruleset / branch protection / required checks** — REST `repos/*` trả 403 và MCP không có tool đọc;
  gồm cả việc chủ kho báo đã bật "Dismiss stale approvals" (**N10**), vẫn chỉ là lời khai.
- **Giá A7 trên Windows** — chưa đo được trước khi chạy thật.
