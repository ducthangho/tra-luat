# wp899 r3 g2 — lưu trữ khi DỪNG HẲN theo V5 (packet #899, lease `wp899-r3-g2-claude`)

Đặc tả `ops/specs/wp899-r3.md` (sha256 `dd1a997d1f3682e23bb4b5577264076b7d9a12aeff5d9823f491cdda05e4f36f`), luật V5: một lớp —
kể cả F01–F07 kế thừa — lặp ở **lượt review thứ 2 của r3** ⇒ DỪNG HẲN. Lượt 2 trả F02 `nhac-ten-script-thanh-thuc-thi` **LẶP LỚP**
(P0). Nhánh code `agent/wp899-g2-claude` **chưa từng được đẩy** (V1); ứng viên chỉ nằm trong bundle dưới đây. Thứ định danh là
BĂM, không phải tên nhánh.

| hiện vật | sha256 |
|---|---|
| `ung-vien-7f5a02c.bundle` (`dc65714..7f5a02c9c2ff346484e10c2f5b4e94fcb0468b8b`, ref `refs/heads/agent/wp899-g2-claude`; gồm `9e5019e` điểm xuất phát, `29d641c` lượt 1, `7f5a02c` lượt 2) | `e066aefd897d52fa73586330fccf82a454358b351f3b43432ddcd38539a77fd2` |

Khôi phục: `git fetch <đường dẫn bundle> refs/heads/agent/wp899-g2-claude:refs/heads/agent/wp899-g2-claude` trong một kho đã có
`dc657149941f9db3ab2afc6fb6462ba4827bf18f`.

## Hai lượt review Codex CLI offline của r3 (lời gọi 5/8 và 6/8, đếm tiếp từ r2)

Mỗi thư mục `../wp899-r3-g2-exec-review-<n>-codex/` có `VERDICT.md`, `prompt.md`, `run.json` (launcher), tệp rollout của CLI và
`dinh-danh-reviewer.json` (năm mục của `dinh_danh_reviewer`). Model là **model do CLI công bố** (`turn_context`); model phục vụ
từng request: KHÔNG ĐO ĐƯỢC. `stdout_sha256` trong biên nhận khớp `run.json` của launcher.

| lượt | Reviewed commit | verdict | thread_id | rollout sha256 |
|---|---|---|---|---|
| 1 | `29d641cbd4a38504eb30d87f0fc7eaa82a185f24` | changes_requested P0=1 (F02 LẶP) P1=1 (F08 mới) | `01a16da4-4e87-7ec2-90e5-c3c0827f7192` | `ecd599d1dc455de3abe3e8079d3e3fd33252f45bc44a8db4810ae834b01e1f59` |
| 2 | `7f5a02c9c2ff346484e10c2f5b4e94fcb0468b8b` | changes_requested P0=1 (F02 LẶP ⇒ V5); F08 đã vá thật | `01a16dbe-aca3-7472-bcfb-157cff53f305` | `7a58373c6ada30476cb009051d46de84bba449eb004c1a7859214ffa32fee618` |

Gate tại chỗ trên `7f5a02c`: `ops/ci_provenance_test.py` ⇒ `CA: 35/35 dat` · `DOT BIEN: 74/74 bi giet dung ly do` ·
`TU KIEM PHAN HANG: DAT (2 dot bien)` · `TONG: DAT`; ruff 0.15.15 `--select F` sạch; `git diff --numstat dc65714` = 3 tệp / 1050 dòng
(trần chủ kho issuecomment-6383572422). A10 LIVE (run 39342960764, 40074551995): provenance sha256 `87b8be84…06b4`,
`d2e5247f…6c6a`, trùng byte giữa `29d641c` và `7f5a02c`. A9 (`ci_dang_ky_test.py --chay`): **not_run** (dừng trước khi xong vì V5).

Quét trước khi đẩy: giá trị của 20 biến môi trường bí mật đang sống ⇒ 0 lần xuất hiện; `scripts/pkg_secret_scan.py` rc 0;
`access_token`/`refresh_token`/`id_token` của `~/.codex/auth.json` ⇒ 0. Trường `account_id` (UUID định danh tài khoản, không phải
credential) có trong hai rollout, như trong cả bốn rollout r2 đã đẩy ở `ops/wp899-g1-luu-tru`. Không verdict nào ở đây là approve;
không gì ở đây cấp quyền merge, land hay `cross_approved`.
