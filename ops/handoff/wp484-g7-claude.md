# Handoff wp484 r7/g7 — hồi sinh #509 (Codex credential refresh)

Lease `wp484-r7-g7-claude` (spec `ops/specs/wp484-r7.md` sha256 `35a81f47…`, thẩm quyền
<https://github.com/ducthangho/tra-luat/issues/484#issuecomment-6222200389>, ghi hộ chủ kho qua GitHub App).
Executor: Claude (`claude-opus-5-5`, Claude Code, cloud). Reviewer định tuyến: Codex. Không có ủy quyền merge.

## Đã làm

1. Nhánh `agent/wp484-g7-claude` từ `faaedff` (head #509), merge `origin/master` `653fef3` (cách 1580 commit).
   Hai xung đột, mỗi tệp 1 hunk:
   - `.claude/hooks/session-start.sh`: giữ khối chụp `TL_CODEX_SNAPSHOT` của #509 TRƯỚC khối `GOC`/
     `ghi_dau_vet_hook` của master (`dirname` là lệnh ngoài; snapshot phải gỡ khỏi môi trường trước nó).
   - `.claude/dev/launcher_test.py`: ca `r484_g*` + ca wp685/k124 của master; mục `DOT_BIEN` hai phía gộp
     vào MỘT danh sách.
2. Bốn P2 của connector Codex (13-10) trên `faaedff`:

| thread | vấn đề | xử lý | ca · đột biến |
|---|---|---|---|
| `PRRT_…XLy` launcher ~2655 | thay `auth.json` không phải CAS | phép đọc lại ngay trước `os.replace` ĐÃ CÓ; thêm phép đo. **THU HẸP, không ĐÓNG** — Codex CLI không tôn trọng khoá của kho, khe syscall cuối vẫn còn. Nợ có tên `codex-auth-json-khong-cas` | `r484_g7_auth_doi_truoc_khi_thay_thi_giu_ban_moi` · `g7_bo_doc_lai_truoc_replace` |
| `PRRT_…XL-` codex_cred ~489 | home hợp lệ chưa tạo ⇒ ĐỎ rc 2 | `lexists` ⇒ `KHÔNG_ĐO_ĐƯỢC` rc 3; symlink treo vẫn đi tiếp cho `_KhoCodex` từ chối | `t15_home_chua_tao_la_KHONG_DO_DUOC` · `t15_bo_nhanh_home_vang` |
| `PRRT_…XMG` launcher ~3136 | kết quả `_danh_dau_auth_hong` bị nuốt | trả lý do riêng "KHÔNG ghi được trạng thái chờ snapshot … CHẶN" — ở CẢ HAI đường: `launcher._do_codex_song` và `codex_cred.cmd_kiem` (đường thứ hai reviewer không chỉ) | `r484_g7_khong_ghi_duoc_trang_thai_tu_choi_phai_noi_ra` · `g7_nuot_loi_ghi_trang_thai`; `t16_…` · `t16_nuot_loi_ghi` |
| `PRRT_…XML` launcher ~4538 | `CODEX_HOME` sai ⇒ traceback rc 1 | `_cho_snapshot_hoac_chan` ⇒ `Chan(13)`; dùng ở `credential-status` và `run … codex` (hai lối thô duy nhất; các lối khác đã có `try` hoặc `_co_chan_codex`) | `r484_g7_credential_status_home_sai_la_chan_khong_traceback` · `g7_home_sai_lai_traceback` |

   Giới hạn của XMG, nói thẳng: không ghi được trạng thái thì kho KHÔNG có chỗ nào để nhớ hộ, nên lần gọi sau
   vẫn thử lại credential cũ. Thứ đổi là lỗi nay ỒN ÀO và có lý do riêng, không còn trông như đã ghi.

3. Phát hiện ngoài 4 P2 (đo được, có sẵn trên #509, master không có): `launcher.py run` và bridge phiên của #509
   khôi phục `CODEX_AUTH_JSON` trước mọi child ⇒ mọi ca chép `os.environ` mang biến của PHIÊN xuống tiến trình
   con. Đo: `t124`–`t126` ĐỎ chỉ khi phiên có credential thật (master XANH cả hai môi trường); với biến giả,
   68 ca đỏ trên g7, `t158` master XANH / g7 ĐỎ rc 13. Tức bộ test từng đem credential THẬT đi materialize.
   Chữa: `launcher_test.py` gỡ biến một lần ở đầu module; ca `r484_g7_bo_test_kin_voi_credential_cua_phien`
   canh (gỡ dòng `pop` ⇒ ĐỎ, đã đo trên bản sao tạm).

## Bằng chứng (đo 17-10, Linux, container cloud)

- `launcher_test.py`: **214/214** cả khi CÓ `CODEX_AUTH_JSON` giả lẫn khi KHÔNG có; bỏ qua 2 ca Windows-only
  (`t62`, `r484_g4_windows_sid_alias_identity`).
- `codex_cred_test.py`: nền **16/16**, đột biến **16/16** bị giết, mỗi ca đích chết vì `AssertionError` của chính nó.
- Ba đột biến launcher g7: chạy trên bản sao tạm `.claude/dev`, mỗi đột biến một tiến trình, `-B`; cả ba giết
  ca đích bằng `bang` của chính ca (không traceback vô can).
- Ruff F: delta so `origin/master` = 0 (`launcher.py` 0/0, `codex_cred.py` 0/0, `launcher_test.py` 5/5,
  `codex_cred_test.py` 0/0). `bash -n session-start.sh` ok. `doctrine-scan` rc 0.
- CHƯA chạy trong phiên: bảng đột biến đầy đủ của `launcher_test.py --dot-bien` (để CI), Windows (M-3).

## Ngân sách

attempt 1/3 · lời gọi Codex 0/2 (trước review).

## Điều kiện merge còn mở

M-1 verdict Codex · M-2 trả lời + resolve 4 thread · M-3 CI xanh + một lượt Windows ·
M-4 wp775 land/nhả `packet_loop_test.py` rồi merge lại master. Không tự merge.
