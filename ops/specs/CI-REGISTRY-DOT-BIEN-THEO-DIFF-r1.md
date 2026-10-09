---
kieu: dac_ta_packet
packet: CI-REGISTRY-DOT-BIEN-THEO-DIFF
packet_id: CI-REGISTRY-DOT-BIEN-THEO-DIFF
ban: r1
trang_thai: dong_bang_khi_dang_bam   # băm sha256 của blob này đăng lên Issue packet; đổi một byte = đổi băm.
nguon_cap_viec: >-
  Chỉ thị chủ kho trong phiên Claude Code 26-09-2026 (phiên executor của #637): hỏi "chạy gate registry toàn hơn 1
  tiếng. Quá đắt"; phiên đề xuất ba việc (cắt vòng đột biến nhanh_don_duoc theo diff, chọn theo diff, N=2); chủ kho
  trả lời "Làm cả 3. Tạo issue, Cấp lease và xử lý luôn cho tôi", rồi chọn "Duyệt lệch, bật ngay" cho xung đột với
  docs/PROTOCOL_DA_PHIEN.md:839-840 (mục 2).
ghi_chu_hinh_dang: >-
  Chưa cổng nào đọc tệp này. Nó là DỮ LIỆU cho lease và cho reviewer, không phải giao diện.
---

# `CI-REGISTRY-DOT-BIEN-THEO-DIFF` — vòng đột biến `nhanh_don_duoc` chạy theo diff, registry N=2 (bản **r1**)

- `packet_id`: **`CI-REGISTRY-DOT-BIEN-THEO-DIFF`** · `revision`: **1** · `generation`: **1** (dự kiến)
- `review_class`: **`sensitive`** — chạm `.github/workflows/ci.yml` và chính sách gate (§8).
- `risk`: `sensitive` · `environment`: `cloud` · `depends_on`: `[]`
- executor: `anthropic_claude` · `claude_code` · `claude-opus-5-5`
- assurance: review Codex (CLI tại chỗ trước push; connector trên PR non-draft) ⇒ `advisory_review`;
  **`assurance_target: human_audited`** — chủ kho audit exact head cuối, là cổng land.
- base: `origin/master` **`b739616058a8b5f1344710b8b215535f964577a1`** (đo 2026-09-26T01:16:09Z)

## 1. Phép đo nền

Nguồn: workflow `gate`, run **36167472209**, event `push` trên `master`, head
`6044aaf1898464344a0817eb4d92615dd94c36fa` (merge PR #640), job API đọc 2026-09-26. Đơn vị: phút runner Linux.

| job | thời lượng |
|---|---|
| `gate` | 15m43s |
| `gate-packet-loop` | 4m37s |
| `gate-registry` | **68m12s** (bước `test registry` 67m43s) |
| **tổng** | **≈ 88,6 phút runner mỗi push master** |

Dòng `CI_DANG_KY_THOI_GIAN` của chính lượt ấy (N=1, 2 lõi logic):

| bộ | giây |
|---|---|
| `ops/nhanh_don_duoc_test.py` | **3042,67** (75 %) |
| `.claude/hooks/pretooluse_guard_test.py` | 774,06 |
| `.claude/hooks/subagent_ghi_detect_test.py` | 199,76 |
| 5 bộ còn lại | 39,53 |

Đo tại chỗ (container phiên, 4 lõi, head `b739616…`, 2026-09-26T01:0xZ):
- `NHANH_DON_DUOC_KHONG_DOT_BIEN=1 python ops/nhanh_don_duoc_test.py` ⇒ **2 giây**, `rc=0`, dòng cuối `8/8`.
- `NHANH_DON_DUOC_CHI_TU_KIEM=1 python ops/nhanh_don_duoc_test.py` ⇒ **13 giây**, `TU KIEM: 48/48`, `rc=0`.
- ⇒ gần như toàn bộ 3042 giây là hai vòng đột biến (`chay_dot_bien` 10 mutant × T1..T8 và `chay_dot_bien_tu_kiem`
  48 nhóm / 200 mutant, mỗi mutant chạy lại bộ tự kiểm). Cờ `NHANH_DON_DUOC_KHONG_DOT_BIEN` **đã có sẵn** trong bộ
  (`ops/nhanh_don_duoc_test.py:5184`) và bộ ấy tự dùng nó cho tiến trình con của mutant (`:747`).

## 2. Lệch protocol có duyệt

`docs/PROTOCOL_DA_PHIEN.md:839-840`: selector chỉ được activate sau shadow 2–4 tuần; trước đó T1/T2 chạy full.
Packet này **bật ngay** một selector hẹp. Chủ kho duyệt lệch trong phiên (câu hỏi có ba phương án, chọn "Duyệt lệch,
bật ngay"). Phạm vi lệch, và **chỉ** phạm vi này:

- chỉ **vòng đột biến** của **một** bộ (`ops/nhanh_don_duoc_test.py`) bị bỏ; T1..T8 của bộ ấy và **mọi** bộ khác vẫn
  chạy mọi lượt;
- các điều kiện fallback full của `:833-836` được giữ (M1): diff không đo được, sự kiện không phải `push`/`pull_request`,
  workflow/runner đổi (vùng chung), tệp của bộ đổi;
- chế độ đã chạy được in ra dương (M2), không suy từ sự vắng mặt.

## 3. Ngoài phạm vi — cố ý không làm

| thứ | lý do |
|---|---|
| lịch chạy đủ hằng đêm (`schedule`) | chốt M6 của #637 (`loi_g5_workflow`) cấm `if` cấp job ở `gate`/`gate-packet-loop`; lịch sẽ kéo cả hai job (~20 phút/ngày). Chạy đủ theo yêu cầu = `workflow_dispatch` |
| chế độ nhẹ cho `pretooluse_guard_test` / `subagent_ghi_detect_test` | chưa có cờ; thêm cờ = sửa bộ (write set 4–5 tệp, vượt ADR-0044). Packet kế |
| bỏ nguyên bộ theo diff | cần bảng phụ thuộc do máy dựng (#245); bảng gõ tay đã sai ba lần ở đó |
| sửa nội dung bất kỳ bộ test nào | chỉ dùng cờ đã có |
| lane Windows | giữ N=1 như #637 |

## 4. Write set — 2 đường

| # | đường dẫn | vì sao |
|---|---|---|
| W1 | `.claude/dev/ci_dang_ky_test.py` | đọc diff, lập kế hoạch chế độ, truyền env cho bộ, bằng chứng chế độ, chốt workflow, phản chứng |
| W2 | `.github/workflows/ci.yml` | env của bước registry: `CI_DANG_KY_WORKERS: "2"` + ba biến sự kiện/diff |

Ngưỡng ADR-0044: ≤ 3 tệp, ≤ 300 dòng thêm.

## 5. Mục tiêu

| # | mục tiêu | đường |
|---|---|---|
| M1 | **kế hoạch theo diff, fail-closed.** Đọc `CI_DANG_KY_SU_KIEN`, `CI_DANG_KY_GOC`, `CI_DANG_KY_DAU` từ env. Chỉ khi sự kiện ∈ {`push`, `pull_request`} **và** cả hai SHA là 40 hex khác toàn-0 **và** `git diff --name-only --no-renames -z GOC...DAU` thoát 0 thì có tập đường dẫn đổi; mọi trường hợp khác ⇒ **không đo được ⇒ đủ**. Bộ có chế độ nhẹ chạy **nhẹ** chỉ khi tập đổi **không** giao vùng `{bộ, đích của bộ (bỏ hậu tố _test), ci.yml, ci_dang_ky_test.py, requirements.txt}`; ngược lại **đủ**. In mỗi quyết định kèm lý do | W1 |
| M2 | **bằng chứng chế độ.** Chế độ nhẹ: env con **có** cờ nhẹ. Chế độ đủ: env con **không có** cờ ấy dù cha có. Chế độ đủ đòi thêm dòng dương `MUTANT: giet = N · khong giet = 0 · khong do duoc = 0 / tong N` (N>0); thiếu ⇒ ĐỎ. JSON thời gian ghi `che_do` từng bộ | W1 |
| M3 | step registry trong `ci.yml`: `CI_DANG_KY_WORKERS: "2"`, `CI_DANG_KY_SU_KIEN: ${{ github.event_name }}`, `CI_DANG_KY_GOC: ${{ github.event.pull_request.base.sha \|\| github.event.before }}`, `CI_DANG_KY_DAU: ${{ github.event.pull_request.head.sha \|\| github.sha }}` — qua `env:` YAML, **không** nội suy vào `run` | W2 |
| M4 | chốt workflow trong `main` (như M6 của #637): step registry có đúng bốn khoá env trên với đúng giá trị; lệch ⇒ ĐỎ | W1 |

## 6. Nghiệm thu — mỗi tiêu chí nêu phép đo làm nó ĐỎ

| # | tiêu chí | phép đo làm ĐỎ |
|---|---|---|
| A1 | M1 fail-closed: `schedule`, `workflow_dispatch`, sự kiện rỗng, SHA thiếu/sai dạng/toàn-0, git rc≠0 ⇒ **đủ**; diff chạm bộ/đích/vùng chung ⇒ **đủ**; diff không chạm (kể cả rỗng) ⇒ **nhẹ**; argv git có `--no-renames` và `GOC...DAU` | mỗi đầu vào là một ca `p-cp-*` trong `phan_chung()` |
| A2 | M2 env: tiến trình con thật in env — đủ ⇒ không có cờ dù cha có; nhẹ ⇒ có | ca chạy subprocess thật |
| A3 | M2 bằng chứng: chế độ đủ mà đầu ra chỉ `8/8` ⇒ ĐỎ; đủ + dòng MUTANT ⇒ ĐẠT; nhẹ + `8/8` ⇒ ĐẠT | ba ca qua CHÍNH `chay_moi` |
| A4 | M4: workflow thật ĐẠT; bỏ/đổi từng khoá ⇒ ĐỎ | ca đột biến workflow trong bộ nhớ |
| A5 | lượt CI của PR (chạm W1/W2 ⇒ **đủ**, N=2) xanh, JSON in `N: 2` và `che_do: day_du`; ghi thời lượng | đỏ ⇒ dừng S2 |
| A6 | cổng hiện hành: `python .claude/dev/ci_dang_ky_test.py` (không `--chay`) in `TỔNG: ĐẠT` và `PHẢN CHỨNG: n/n`; `actionlint .github/workflows/ci.yml` rc=0; ruff F delta 0 | thiếu dấu hiệu dương ⇒ KHÔNG ĐẠT |
| A7 | quan sát sau land (không phải cổng land): lượt push master đầu tiên không chạm vùng in `che_do: nhe` và bước registry < 25 phút | ghi vào biên nhận land |

## 7. Ngân sách CI

| loại | `used / reserved / limit` |
|---|---|
| gate tự động (`pull_request` trên head cuối, sau review tại chỗ sạch) | 0 / 1 / 2 lượt |
| phép đo được cấp | 0 / 0 / 0 |
| thăm dò chưa cấp | cấm |

Hết allowance ⇒ DỪNG, chờ chủ kho.

## 8. Rủi ro đã biết

- **Bỏ sót do phụ thuộc ngầm:** vòng đột biến đọc hai tệp của bộ + môi trường (git, python của runner). Đổi runner
  image không nằm trong diff ⇒ vòng đột biến không chạy lại cho tới khi có diff chạm vùng hoặc bấm tay. T1..T8 vẫn chạy
  mọi lượt, nên hành vi công cụ vẫn được đo; thứ bị hoãn là **độ bén của bộ test**, không phải hành vi.
- **N=2 trên runner 2 lõi:** bộ nặng chạy chồng ⇒ có thể chậm hơn tuyến tính; A5 đo thật.
- **`github.event.before` trên push tạo nhánh** là toàn-0 ⇒ đủ (M1). Chỉ `master` có `push` trong `ci.yml`.

## 9. Điều kiện dừng

- S1 — chạm đường ngoài W1/W2. DỪNG.
- S2 — lượt CI (A5) đỏ vì packet. DỪNG, báo chủ kho.
- S3 — phải sửa một bộ test mới làm được. DỪNG.
- S4 — push chỉ sau review tại chỗ sạch; hết allowance ⇒ DỪNG.
- S5 — > 300 dòng thêm. DỪNG.
- S6 — hết hạn lease ⇒ ngừng ghi, handoff §7.
