# Đặc tả packet `no-p3-cong-cu-ho-so` r1 — nợ P3 (b2): bộ kiểm hồ sơ land + bộ kiểm nhãn HINT

| mục | nội dung |
|---|---|
| `packet_id` | `no-p3-cong-cu-ho-so` |
| `packet_issue` | #752 |
| `revision` | 1 |
| `nguon_cap_viec` | Sổ nợ P3 mục 5 và 6, cả hai do connector Codex nêu trên PR #722 (mục 5: comment `4231959151` "audit mọi `*-HINT.patch`"; mục 6: schema check `authorized_head_sha` khi `landed: true`). Ngưỡng chủ kho #698 `6094652521`. Cách tách và phạm vi do chủ kho chốt 15-10-2026 (Q4, Q7, Q9). |
| `review_class` | standard — hai công cụ CHỈ ĐỌC, không tham gia authority/gate/runtime, không gắn vào CI ở packet này. |
| `executor` · `reviewer` | Claude (executor); reviewer subagent Claude Sonnet (`review_deferred`). Chỉ P1/P2 chặn merge. |
| `base` | `origin/master` `6f121a3810045af27bf65eb723edf36b29e387f2` (đo 15-10 ~06:10Z). |
| `write_set` | `ops/kiem_ho_so_land.py` (MỚI) · `ops/kiem_ho_so_land_test.py` (MỚI) · `ops/kiem_nhan_hint.py` (MỚI) · `ops/kiem_nhan_hint_test.py` (MỚI) |
| `kich_thuoc` | 4 tệp; ước ≤ 700 dòng thêm (đơn vị: dòng thêm theo `git diff --numstat`); dưới trần thường ADR-0044 (6 tệp, 1.000 dòng). |

## Số đo nền (đo 15-10-2026 ~06:00Z trên `origin/master` `6f121a3`)

- **Hồ sơ land:** 26 tệp `ops/land/*-land-evidence.yaml` (đơn vị: tệp). 14 tệp có `landed: true` (đọc ở
  `trang_thai_packet.landed`, hoặc khoá `landed` mức gốc nếu không có `trang_thai_packet`). Với luật L-6 dưới đây: 13 đạt,
  **1 trượt** — `ops/land/pr672-wp574-land-evidence.yaml` (thiếu cả `authorized_head_sha` lẫn `authorization_url`).
- **HINT:** 52 tệp khớp `ops/reviews/**/*HINT.patch` (đơn vị: tệp). Theo chuỗi khoá `chưa chạy trên cây thật` (nhãn bắt buộc
  PROTOCOL §8 "patch-as-hint", ràng buộc 1, `docs/PROTOCOL_DA_PHIEN.md` dòng 644–645 tại `6f121a3`): 15 có nhãn, 2 tệp
  rỗng (0 byte sau strip), **35 thiếu nhãn**. Cả 35 là bản sao nguyên byte có băm trong biên nhận ⇒ KHÔNG được sửa.

## Luật

- **L-6 (`kiem_ho_so_land.py`):** hồ sơ có `landed: true` thì `authorized_head_sha` phải là chuỗi khớp `^[0-9a-f]{40}$` VÀ
  `authorization_url` phải bắt đầu bằng `https://github.com/ducthangho/tra-luat/` và chứa `#issuecomment-` hoặc
  `#pullrequestreview-` hoặc `#discussion_r`. `landed` khác `true` ⇒ không kiểm. YAML không parse được ⇒ lỗi (fail-close).
- **L-5 (`kiem_nhan_hint.py`):** tệp `*HINT.patch` không rỗng mà không chứa nguyên văn chuỗi
  `chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm` ⇒ xếp **`KHONG_DU_DIEU_KIEN_PATCH_AS_HINT`**; rỗng
  ⇒ `RONG`; có ⇒ `CO_NHAN`. Đọc UTF-8 nghiêm; giải mã lỗi ⇒ `KHONG_DOC_DUOC` (không âm thầm `errors="replace"`).

## Mục tiêu

1. **[`ops/kiem_ho_so_land.py`]** CLI `python ops/kiem_ho_so_land.py --root . [--json]`: quét theo L-6, in từng tệp
   `DAT`/`TRUOT`/`BO_QUA` kèm lý do, tổng `n_dat/n_landed`. Rc 0 khi không tệp nào trượt NGOÀI danh sách miễn trừ; rc 1 khi
   có; rc 2 lỗi tham số; rc 3 không đọc được tệp/YAML. Danh sách miễn trừ là hằng trong mã, mỗi mục có lý do; r1 chứa đúng
   một mục: `ops/land/pr672-wp574-land-evidence.yaml` — lý do "hồ sơ của packet khác, ghi trước luật L-6; sửa ở packet riêng".
   Miễn trừ một tệp không tồn tại ⇒ rc 3 (danh sách không được thối).
2. **[`ops/kiem_ho_so_land_test.py`]** Bộ test tự đứng, dựng cây tạm.
3. **[`ops/kiem_nhan_hint.py`]** CLI `python ops/kiem_nhan_hint.py --root . [--json]`: liệt kê mọi tệp theo L-5, in đếm từng
   loại. Rc 0 luôn khi đọc được hết (đây là công cụ BÁO CÁO, không phải cổng); rc 3 khi có `KHONG_DOC_DUOC`. Không ghi tệp nào.
4. **[`ops/kiem_nhan_hint_test.py`]** Bộ test tự đứng, dựng cây tạm.

## Nghiệm thu

- **B1 (L-6 răng):** cây tạm có 4 hồ sơ `landed: true`: đủ cả hai trường ⇒ `DAT`; SHA 39 ký tự ⇒ `TRUOT`; SHA viết hoa ⇒
  `TRUOT`; URL ngoài kho ⇒ `TRUOT`; và một hồ sơ `landed: false` thiếu cả hai ⇒ `BO_QUA`. Rc 1. ĐỎ khi: đột biến nới regex
  thành `[0-9a-fA-F]{39,40}` ⇒ hai ca ĐỎ; đột biến bỏ kiểm URL ⇒ ca URL ĐỎ.
- **B2 (miễn trừ):** hồ sơ trượt có trong danh sách miễn trừ ⇒ rc 0 và dòng `MIEN_TRU` kèm lý do; mục miễn trừ trỏ tệp vắng ⇒
  rc 3. ĐỎ khi: đột biến bỏ kiểm tồn tại ⇒ ca tệp vắng ĐỎ.
- **B3 (trên kho thật):** `python ops/kiem_ho_so_land.py --root .` tại ứng viên ⇒ rc 0, đếm `13/14 DAT` + `1 MIEN_TRU`
  (đo lại lúc thi hành theo L5; số hạng lệch thì ghi số mới và lý do, đừng ép khớp). ĐỎ khi: gỡ miễn trừ ⇒ rc 1.
- **B4 (L-5 răng):** cây tạm có 4 tệp HINT: có nhãn, thiếu nhãn, rỗng, byte không phải UTF-8 ⇒ đúng bốn loại; rc 3 vì có
  `KHONG_DOC_DUOC`. ĐỎ khi: đột biến khớp nhãn bằng chuỗi rút gọn `chưa chạy` ⇒ tệp mồi chứa `chưa chạy` mà không đủ nhãn
  ĐỎ; đột biến đọc `errors="replace"` ⇒ ca byte lỗi ĐỎ.
- **B5 (trên kho thật, chỉ đọc):** `python ops/kiem_nhan_hint.py --root . --json` ⇒ rc 0, đếm theo loại khớp số đo nền (đo
  lại lúc thi hành); `git status --porcelain` rỗng sau khi chạy. ĐỎ khi: công cụ ghi bất kỳ tệp nào ⇒ `git status` không
  rỗng.
- **B6 (cổng kho):** ruff F delta 0 (multiset) bốn tệp; CI PR xanh. Hai test chạy được bằng `python -B <tệp>` và in `N/N`.

## Ngoài phạm vi (cố ý)

- Gắn hai công cụ vào CI (`ci.yml` thuộc write set #748) — ghi nợ cho packet sau #748.
- Sửa `pr672-wp574` hay bất kỳ tệp HINT nào (bản sao nguyên byte có băm).
- Ghi cờ "không đủ điều kiện" vào biên nhận từng lượt — để packet khác quyết định có cần hay không.

## Hình dạng kế thừa

`khong_ap_dung` (công cụ mới). Chép một hình dạng có thể tái phát: **bộ lọc theo danh sách đoán trước mù đúng chỗ** (CLAUDE.md,
"Quét secrets: lọc theo PHẦN MỞ RỘNG") — glob `*HINT.patch` bỏ sót `*HINT-sanpham.diff` và tệp `hint*.json`; r1 CỐ Ý chỉ
phủ `*HINT.patch` (đúng phạm vi #722 nêu) và công cụ phải in phạm vi glob trong đầu ra.

## Chưa đo được

- Hồ sơ land trên nhánh `ops/**` chưa vào master: công cụ chỉ quét cây được chỉ định, không quét mọi ref.
- Đường Windows: không đo ở packet này.
