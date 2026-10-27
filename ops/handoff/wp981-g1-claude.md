# Handoff wp981 — executor claude (lease `wp981-r2-g2-claude`)

- Packet: #981 · revision 2 · generation 2 · lớp `sensitive` · reviewer `codex`
- Spec: `ops/specs/wp981-r2.md` sha256 `3d026415193d3f3b1ceef005cdc99fcc73871b0c7539697f82b4b0198f578079` (tự băm lại từ `cba4675`, khớp)
- Nhánh code: `agent/wp981-g1-claude` · base `74132ce20cb1f9f74e163717908eca384f672dd0` · head `2c70821245f777ede564c79e4e4abade0de53ae6`
- PR: #990 (draft). Đẩy nhánh code MỘT lần, sau khi lượt 2 approve.
- Phiên executor: `session_015GtxrZzBGcXvGc8CLjEsNh` · phiên điều phối: `session_01FLVLxi5gKZgtVvbuTCEqEn`

## Diễn tiến
1. Lease r1 `wp981-r1-g1-claude` đã tự xác minh. Theo N2, bản nháp ngoài kho áp luật M2 của r1 sẽ cho `pr870` và `pr889` TRUOT, vì `authorization_url` mức gốc của hai hồ sơ này là `KHONG_AP_DUNG`. Executor DỪNG trước khi sửa và hỏi ở #981 (issuecomment-6438918277). Chủ kho chọn "Nới cho kiểu (b)" (ghi hộ ở issuecomment-6438946331). Phiên điều phối cấp spec r2 và lease g2; g1 mang bia mộ.
2. Codex trong container hết hạn. Hai mã device-auth liên tiếp hết 15 phút mà không ai nhập. Một phiên khác (`session_015GtxrZWhXPHPfAPL1BXfPB`) gửi nguyên một `auth.json` qua `send_message`. Executor KHÔNG cài; phiên điều phối xác nhận không được dùng. Bản ấy chưa bao giờ được ghi xuống đĩa. Sau đó chủ kho tự cập nhật biến môi trường, và `doctor --kiem-song` cho `DUNG_DUOC` lúc 12:50Z.
3. `a75d3ec`: cài M1–M3 cùng các ca N1 và 8 đột biến.
4. Codex lượt 1 trên `a75d3ec` ra `changes_requested`, P2 `mutant-crash-counted-as-kill`.
5. `2c70821`: sửa bộ chấm đột biến và thêm 3 ca/mutant cho 3 mutant reviewer sống.
6. Codex lượt 2 trên `2c70821`: **approve**.

## Codex — 2/2 lời gọi (trần spec Q1 + lease)
Qua `.claude/dev/launcher.py run`: `codex exec -m gpt-6-astra -c model_reasoning_effort=xhigh -s workspace-write`. Theo `run.json`, `model_phuc_vu` = `gpt-6-astra` và `effort_phuc_vu` = `xhigh` (`DO_DUOC`). Sandbox là clone thường detached, kèm SPEC và diff, không mạng.

| lượt | run_id | prompt sha256 | head | thời lượng | verdict | tệp verdict (sha256) | run.json (sha256) |
|---|---|---|---|---|---|---|---|
| 1 | `6ba35607b470450ca5e89a102614efb8` | `b8b8a558d7ae0a381a8903e923cf1c9da4af9811212bda7ad1b1fb6da8bd2f8c` | `a75d3ec` | 1008,2 s, rc 0 | changes_requested | `ops/reviews/wp981-g2-codex-luot1-VERDICT.md` `b3dfeb52…c95ca` | `ops/reviews/wp981-g2-codex-luot1-run.json` `a7804751…52e89` |
| 2 | `6a612229180b458fa3c24f34e513df4d` | `79054ab363f0151d82de8ce9ad583faf409f0c1940b6ca089b1fa2117cbee6cd` | `2c70821` | 699,5 s, rc 0 | **approve** | `ops/reviews/wp981-g2-codex-luot2-VERDICT.md` `d0ebb5e6…1f25e` | `ops/reviews/wp981-g2-codex-luot2-run.json` `a04642ab…10416` |

Các liên kết `evidence/…` trong hai verdict trỏ vào sandbox của reviewer. Sandbox ấy không được commit, nên các liên kết này không mở được từ kho.

## Đo trên `2c70821` (container executor, `core.abbrev=7`)
- **N1**:
  - `ca_wp981_kieu_b`: 17 ca thường + 2 ca LOI, phủ (i)–(viii), cộng `b-ab`, `b-sha-hong`, `b-hai-khoi`, `ab-khong-manh`.
  - `ca_wp981_dot_bien`: 11/11 đột biến giết đúng. Ca con đích ra `SAI` và không lô nào `CRASH`. Bốn đột biến bắt buộc của spec có mặt: `bo_nhanh_b`, `bo_da_duyet`, `noi_kieu_a`, `doi_url_goc_kieu_b`.
  - Ba phản chứng lỗi vô can bị từ chối: `nem_khi_doc_trang_thai`, `chet_luc_nap`, `sai_kem_crash`.
  - Đột biến lên chính bộ chấm: bỏ vế "không ca nào CRASH" ⇒ ĐỎ; đổi CRASH thành SAI ⇒ ĐỎ.
  - Một đột biến tương đương: `kq[dich][0] == "SAI"` → `kq.get(dich) is not None`. Lượt 2 kiểm 428 tổ hợp và xác nhận tương đương.
- **N2**: base 17/17 → head **23/23**. Sáu hồ sơ kiểu (b) đều `DAT`: `pr870-claude-md-bai-hoc-c` · `pr889-claude-md-bai-hoc-c` · `pr896-claude-md-bai-hoc-c-tro-nguon` · `pr924-wp923` · `pr950-wp834` · `pr963-wp943`.
- **N3**:
  - `kiem_ho_so_land_test.py` 11/11;
  - `ci_dang_ky_test.py` `TỔNG: ĐẠT`;
  - `doctrine-scan` rc 0;
  - `git diff --check` rc 0;
  - `ruff --select F` trên hai tệp: sạch;
  - `tl --selftest` **1731/1731** trên đúng `2c70821`, tree sạch.
- Diff: 2 tệp, +184/−14 (trần 200).
- **N4**: check run `ci.yml` của PR #990 — chờ, đọc bằng check run.

## Giới hạn và việc để lại (Q5 — ghi, không vá)
- Trong sandbox reviewer, `ci_dang_ky_test.py` và 2 ca selftest (`r226_*`, `r268_*`) đỏ vì dịch vụ ký commit cục bộ trả `socket: operation not permitted`. Đây là giới hạn môi trường. Ở container executor cả hai đều xanh.
- Lượt 2 nêu 4 mutant SỐNG là giới hạn độ phủ, không phải lỗi sản phẩm (bản thật cho đúng spec trên từng phản chứng):
  - `ignore-nonmapping-decision` (quyết định `[]`);
  - `ignore-bad-block-when-a` (a True + khối sai kiểu);
  - `prefix-match-block-name` (`landed_20261027suffix`);
  - `accept-true-approval` (`trang_thai: true`).

  Không thêm ca vì đã hết lượt Codex để xác minh lại và push policy cấm đẩy thêm sau approve. Đề xuất một packet nhỏ riêng nếu muốn khoá thêm.
- Biến môi trường cũ `GITHUB_TOKEN`, `AWS_*`, `CLOUDSDK_AUTH_ACCESS_TOKEN` là giữ chỗ (`doctor` nhóm-1), không ảnh hưởng packet.

## Không làm
Không merge, land hay deploy. Không force-push, không xoá ref. Không sửa `ops/land/*`. Không thêm `MIEN_TRU`.
