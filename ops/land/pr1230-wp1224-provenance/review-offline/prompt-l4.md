# Review Codex rút gọn — packet #1224 CLOUD-SETUP-P3C-DOCS r2 g2, lượt 4/5 (trần cứng 10)

Bạn là reviewer độc lập (họ OpenAI), chỉ đọc. KHÔNG sửa tệp nào trong kho, không push, không gọi mạng ngoài git cục bộ.

## Neo
- Kho: thư mục làm việc hiện tại. HEAD phải là `4dc4fe9`. Đọc `git rev-parse HEAD`; khác thì dừng và kết luận request_changes.
- Head đã approve ở lượt 3: `0b1e6ad51b7989e5dc9d99991a204d4afb1d183b` (0 P0–P3).
- Đặc tả: `ops/specs/cloud-setup-p3c-docs-r2.md`, sha256 `a5afb3e749870535340d65cbbd4ebdc7eec5f82b1be053e4278a78ff95349bda`.
- master: `50baf894216504d4bb975690ceb9dee4835a2ad7` (sau khi #1223/#1229 land).

## Delta cần xét (chỉ phần này)
1. `d09303d`: merge `origin/master` 50baf89 vào nhánh.
2. `4dc4fe9`: phiên land tái sinh `RELEASE_MANIFEST.json` (A9 của đặc tả).

## Việc phải kiểm, mỗi việc bằng lệnh chạy được
- K-a: 5 tệp packet (`CLAUDE.md`, `changelog.d/wp-1224.md`, `docs/GOI_AGENT_DA_NEN.md`, `references/DELTA_v1.19.md`, `references/DEV_TOOLING_GUIDE.md`) phải đúng như ý định của lượt 3. Phần diff của chúng so với master phải TRÙNG phần diff của `0b1e6ad` so với base cũ `c5a1c3d`. Riêng `CLAUDE.md` được merge tự động: kiểm rằng câu M4 vẫn còn đúng 1 lần, và đoạn sự cố 15-08 giữ nguyên byte so với master.
- K-b: `git diff --stat 50baf89 HEAD` chỉ gồm 5 tệp packet + `RELEASE_MANIFEST.json`. Không có conflict marker.
- K-c: `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` ⇒ `ok: true`, `expected_file_count == checked_file_count`, `failed` rỗng. So với manifest ở `50baf89`, chỉ được đổi sha của đúng 2 tệp `references/DELTA_v1.19.md` và `references/DEV_TOOLING_GUIDE.md`, cùng `total_bytes`/`package_hash`/`content_hash`. `file_count` không đổi.
- K-d: `python scripts/tl.py --selftest` ra `N/N` với hai số bằng nhau.
- K-e: câu `references/DELTA_v1.19.md` "ba bản mới nhất (2.21.2o, 2.21.2p, 2.21.2q)" vẫn khớp tập `references/Code.*.gs` trong manifest tái sinh. `DEV_TOOLING_GUIDE.md` trỏ đúng `Code.2.21.2q.gs`, và tệp ấy có trong cây. Lưu ý: #1223 đã đổi EXPECT_VERSION sang 2.21.2q.

Ngoài delta trên thì không review lại (đã approve ở lượt 3).

## Đầu ra
Ghi phát hiện theo bậc P0/P1/P2/P3, mỗi phát hiện kèm lệnh tái hiện. Cuối cùng in ĐÚNG MỘT dòng, là dòng cuối cùng của stdout, chữ thường:
`KET_LUAN: approve` nếu không còn P0/P1/P2; ngược lại `KET_LUAN: request_changes`.
