# Review Codex rút gọn — packet #1223 CLOUD-SETUP-P3C-CONTRACT r1, lượt 4/5 (trần cứng 10)

Bạn là reviewer độc lập (họ OpenAI), chỉ đọc. KHÔNG sửa tệp nào trong kho, không push, không gọi mạng ngoài git cục bộ.

## Neo
- Kho: thư mục làm việc hiện tại. HEAD phải là `1d5ee67` (đọc `git rev-parse HEAD`; khác thì dừng và kết luận request_changes).
- Head đã approve ở lượt 3: `f27dba426acf683010a05872be5411007f773e84` (0 P0–P3).
- Đặc tả: `ops/specs/cloud-setup-p3c-contract-r1.md` (sha256 `db83020d7cd57c8c9981c8f94ffcc50bf59d536a7224c1f3fb6ae6195511de3a`).
- master: `b255b0b7131da7f6e026639f6b0da0a06cc68a44` (sau khi #1197 land).

## Delta cần xét (chỉ phần này)
Từ `f27dba4` tới HEAD có:
1. `da87d40` — merge master trước (đem đặc tả P3c-docs r2 vào, không chạm 6 tệp packet).
2. `3095ad9` — merge `origin/master` b255b0b (land #1197/#1099) vào nhánh.
3. `1d5ee67` — phiên land tái sinh `RELEASE_MANIFEST.json` (spec A10).

## Việc phải kiểm, mỗi việc bằng lệnh chạy được
- K-a: 6 tệp packet (`INSTALL.md`, `SKILL.md`, `references/API_CONTRACT.md`, `scripts/tl.py`, `scripts/tl_selftest.py`, `changelog.d/wp-1223.md`) giống hệt từng byte giữa `f27dba4` và HEAD (`git diff --quiet f27dba4 HEAD -- <6 tệp>`).
- K-b: `git diff --stat origin/master HEAD` (hoặc `b255b0b HEAD`) chỉ gồm 6 tệp packet + `RELEASE_MANIFEST.json`; merge không có conflict marker (`git grep -n '^<<<<<<<\|^>>>>>>>' HEAD` rỗng).
- K-c: `RELEASE_MANIFEST.json` khớp cây: `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` ⇒ `ok: true`, `expected_file_count == checked_file_count`, `failed == 0`; `webapp_target == "2.21.2q"`; so với manifest ở `b255b0b` chỉ đổi sha của đúng 5 tệp gói của packet cộng `webapp_target`/`total_bytes`/`package_hash`/`content_hash`, `file_count` không đổi.
- K-d: `python scripts/tl.py --selftest` ra `N/N` với hai số bằng nhau.
- K-e: tương tác ngữ nghĩa giữa #1099 (`scripts/nlm_cli.py`, fragment test mới) và thay đổi của packet (EXPECT_VERSION 2.21.2q, ca selftest `expect_version`/`r210`): có ca nào của #1099 phụ thuộc phiên bản webapp hay nội dung SKILL.md/API_CONTRACT.md mà nay đổi không.

Ngoài delta trên thì không review lại (đã approve ở lượt 3).

## Đầu ra
Ghi phát hiện theo bậc P0/P1/P2/P3, mỗi phát hiện kèm lệnh tái hiện. Cuối cùng in ĐÚNG MỘT dòng, là dòng cuối cùng của stdout, chữ thường:
`KET_LUAN: approve` nếu không còn P0/P1/P2; ngược lại `KET_LUAN: request_changes`.
