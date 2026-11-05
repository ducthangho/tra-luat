# Review Codex offline lượt 5/5 — packet #1224 CLOUD-SETUP-P3C-DOCS r2 g2: lượt THAY lượt 4 (run a8d7350a), TUÂN THỦ READ-ONLY

Bạn là reviewer độc lập (họ OpenAI). QUY TẮC TUYỆT ĐỐI: KHÔNG ghi bất kỳ tệp nào trong thư mục làm việc này, kể cả tệp bị .gitignore bỏ qua. Lượt trước bị loại vì selftest đã ghi 11 tệp ignored vào checkout. Phiên điều phối sẽ so sha256 của MỌI tệp trong cây trước và sau lượt này; chỉ cần lệch một byte là lượt này vô hiệu.

Muốn chạy bất cứ thứ gì có thể ghi (selftest, release-verify, script đo) thì:
1. `cp -a <thư mục làm việc> /tmp/rv5-copy` (hoặc `git worktree`/`git clone` RA NGOÀI vào /tmp);
2. chỉ chạy trong bản sao ấy.
Lệnh chỉ đọc (`git diff`, `git show`, `git rev-parse`, đọc tệp) thì chạy trực tiếp được.

## Neo
- HEAD phải là `4dc4fe9a30517cf4bb1cb78105a91687814cc0fa` (head đã merge của PR #1230, merge commit `825eb35`). Khác thì kết luận request_changes.
- Base merge-base: `50baf894216504d4bb975690ceb9dee4835a2ad7`. Head đã approve ở lượt 3: `0b1e6ad51b7989e5dc9d99991a204d4afb1d183b`.
- Đặc tả: `ops/specs/cloud-setup-p3c-docs-r2.md`, sha256 `a5afb3e749870535340d65cbbd4ebdc7eec5f82b1be053e4278a78ff95349bda`.

## Việc phải kiểm (giống lượt 4), mỗi việc bằng lệnh chạy được
- K-a: diff của 5 tệp packet (`CLAUDE.md`, `changelog.d/wp-1224.md`, `docs/GOI_AGENT_DA_NEN.md`, `references/DELTA_v1.19.md`, `references/DEV_TOOLING_GUIDE.md`) so với `50baf89` phải TRÙNG diff của `0b1e6ad` so với `c5a1c3d`. Câu M4 trong CLAUDE.md có đúng 1 lần; đoạn sự cố 15-08 nguyên byte so với master.
- K-b: `git diff --stat 50baf89 HEAD` chỉ gồm 5 tệp packet + `RELEASE_MANIFEST.json`; không có conflict marker.
- K-c (TRONG BẢN SAO): `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` ⇒ `ok: true`, 184/184, `failed` rỗng. So với manifest tại `50baf89`, chỉ đổi sha của `references/DELTA_v1.19.md` và `references/DEV_TOOLING_GUIDE.md` cùng các trường tổng hợp.
- K-d (TRONG BẢN SAO): `python scripts/tl.py --selftest` ⇒ `N/N` với hai số bằng nhau.
- K-e: DELTA_v1.19 nêu "ba bản mới nhất (2.21.2o, 2.21.2p, 2.21.2q)", khớp tập `references/Code.*.gs` trong manifest; DEV_TOOLING_GUIDE trỏ `Code.2.21.2q.gs`, và tệp này có trong cây.
- K-f: tự khai rõ: mọi lệnh có khả năng ghi đều chạy trong bản sao nào (in đường dẫn), và xác nhận KHÔNG ghi vào thư mục làm việc.

## Đầu ra
Ghi phát hiện theo bậc P0/P1/P2/P3, mỗi phát hiện kèm lệnh tái hiện. Dòng cuối cùng của stdout, đúng nguyên văn, chữ thường:
`KET_LUAN: approve` nếu không còn P0/P1/P2; ngược lại `KET_LUAN: request_changes`.
