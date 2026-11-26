# Đặc tả packet — `CLOUD-SETUP-P2B-WIRE` (revision 2)

- `packet_id`: **CLOUD-SETUP-P2B-WIRE** · `packet_issue`: **#1039** · `revision`: **2** · trạng thái: **ĐÓNG BĂNG** 24-11-2026.
  Thay revision 1 (`ops/specs/cloud-setup-p2b-wire-r1.md`) **CHỈ** ở ba điểm dưới đây. Mọi mục khác của r1 giữ nguyên hiệu lực.
- `nguon_cap_viec`: chỉ thị trực tiếp của chủ kho trong chat 24-11-2026: *"nâng cấp lên phiên bản agy mới nhất, ghim sang
  bản mới nhất … cho phép cập nhật phiên bản và ghim lại khi cần"*. Chủ kho chọn: bật tự cập nhật (bản ghim là SÀN), làm
  thẳng trên nhánh, không mở Issue/lease mới.
- `review_class`: **sensitive** (như r1: chạm việc cài nhị phân vào phiên cloud).

## Thay đổi 1 — Hằng ghim `agy` (đo 24-11-2026)

Nguồn: GitHub release `google-antigravity/antigravity-cli` bản **1.5.16** (`releases/latest`, phát hành 24-11-2026). Đã tải
cả sáu tarball, so sha256 với trường `digest` của GitHub ⇒ khớp cả sáu; mỗi tarball chứa đúng một tệp thường `antigravity`.
sha512 dưới đây tính trên chính các byte đã tải.

| khoá nền | URL tarball | sha512 |
|---|---|---|
| `linux_amd64` | `https://github.com/google-antigravity/antigravity-cli/releases/download/1.5.16/agy_cli_linux_x64.tar.gz` | `3dee9f26e298156db673f6ce2a0f5dfed5b30006e04ceb9809c68070e7b717587b33a3da0f8bc2eda45af81a50bc8b14c82b28ae5832bcfe3e7fd49397117b31` |
| `linux_arm64` | `https://github.com/google-antigravity/antigravity-cli/releases/download/1.5.16/agy_cli_linux_arm64.tar.gz` | `23c193151499a4986fd5fa0d8132665cc8ffbad6cc0b3ff4fd53a2cb68abb76b149a992b836d53063443cd89add335f14d8134fb02abdcecbf6e1eaef6c53d33` |
| `linux_amd64_musl` | `https://github.com/google-antigravity/antigravity-cli/releases/download/1.5.16/agy_cli_linux_x64_musl.tar.gz` | `9f868c13f308557192b8c3fa30f1251283167b7e551e9f0f05ed0fa2640e91e02accaeacd41692a0422e8de90c1cc0b6e327f2b6befbd11080a4881d45bf61b1` |
| `linux_arm64_musl` | `https://github.com/google-antigravity/antigravity-cli/releases/download/1.5.16/agy_cli_linux_arm64_musl.tar.gz` | `4bc5c802c97ca19404c666136f1e74dc880a3b0346e7c6950ad4e217056c6cc86ae5afa633aa5989a260600f49cb6e71db438558c4f2d44e5f5bdab8bb38980c` |
| `darwin_amd64` | `https://github.com/google-antigravity/antigravity-cli/releases/download/1.5.16/agy_cli_mac_x64.tar.gz` | `b3eae073ee633032e9d473cdc7725c30bdfe2e09436bc36cfb3422e7e5fa3733de9591a7f78d02362294e7bf87e345d70e5d839689e526129a6f3fc041857a05` |
| `darwin_arm64` | `https://github.com/google-antigravity/antigravity-cli/releases/download/1.5.16/agy_cli_mac_arm64.tar.gz` | `33f5617dc74fea606d47b2483c6d271c850c9f3c9c55b724c664c3c0d4b82100d819fbcf55714f851765f6628d4296883ac8939b4fdeb55d5e6b9ce923135d18` |

`AGY_VER = "1.5.16"`. Luật chọn nền giữ nguyên r1.

## Thay đổi 2 — Bản ghim là SÀN, cho phép tự cập nhật

- Thay gạch *"`agy --version` in chuỗi chứa `1.4.12` ⇒ không tải gì"* của r1 mục tiêu 2: `agy --version` rc 0 và có **một
  token** dạng đúng `X.Y.Z` (chỉ chữ số, không hậu tố như `rc1`/`beta`) với `(X, Y, Z) >= AGY_VER` ⇒ không tải gì. Bản
  cài sẵn MỚI HƠN sàn (do `agy` tự cập nhật) được GIỮ, không hạ cấp. Thấp hơn sàn, hậu tố lạ, hỏng ⇒ tải bản ghim như r1.
- Bỏ mục tiêu 4 của r1: `cai-agy` **không** còn ghi `export AGY_CLI_DISABLE_AUTO_UPDATE=1` vào `CLAUDE_ENV_FILE` và không
  đụng tệp đó. Ca D1 của r1 bị thay bằng D1': có `CLAUDE_ENV_FILE` ⇒ tệp không đổi một byte. Ca D2 giữ nguyên.
- Rủi ro chấp nhận (chủ kho duyệt): tự cập nhật của `agy` tải nhị phân mà kho không kiểm băm. Sàn chỉ bảo đảm lần cài ĐẦU
  của mỗi phiên là bản đã kiểm.

## Thay đổi 3 — Lệnh con `ghim-agy` (ghim lại khi cần)

`python ops/cloud_agent_creds.py ghim-agy [--ban X.Y.Z]`: đọc release `latest` (hoặc tag `X.Y.Z`) của
`google-antigravity/antigravity-cli` trên GitHub, tải đủ sáu tarball của bảng trên, đòi sha256 khớp `digest` của GitHub và
tarball đúng một tệp thường `antigravity`. Đạt cả sáu ⇒ in ra stdout khối Python (`AGY_VER`, `NEN`) và sáu dòng bảng Markdown
để dán vào revision đặc tả kế tiếp, rc 0. Thiếu tài sản, lệch digest, tarball sai, lỗi mạng ⇒ in `ghim-agy: ✗ …`, rc 1, không
in khối nào. Lệnh **không ghi tệp nào**: ghim lại vẫn là sửa tay + revision đặc tả mới, như r1.

## Ca nghiệm thu thay đổi

| ca | mô tả | đột biến bắt buộc ĐỎ |
|---|---|---|
| B3' | `agy` giả in `antigravity 1.5.16` và `antigravity 1.6.0` ⇒ tải đếm **0** | luôn tải ⇒ ĐỎ |
| B4' | `1.5.15`, `1.4.120`, `1.5.16rc1`, rc 1, đầu ra rác ⇒ tải đếm **1** và tệp được thay | so chuỗi con / bỏ chặn hậu tố ⇒ ĐỎ |
| B8' | bảng `NEN` của mã THẬT bằng nguyên văn bảng Thay đổi 1 của tệp này (băm cố định), `AGY_VER == "1.5.16"` | đổi một ký tự sha512 ⇒ ĐỎ |
| D1' | `CLAUDE_ENV_FILE` có sẵn nội dung; chạy `cai-agy` hai lần ⇒ tệp không đổi | ghi lại dòng tắt cập nhật ⇒ ĐỎ |
| G1 | `ghim-agy` với release giả đủ sáu tài sản đúng ⇒ rc 0, in đúng sáu cặp URL/sha512 tính từ byte giả | in sha256 thay sha512 ⇒ ĐỎ |
| G2 | một tài sản lệch digest, hoặc thiếu, hoặc tarball hai tệp ⇒ rc 1, không in khối | bỏ kiểm digest ⇒ ĐỎ |
