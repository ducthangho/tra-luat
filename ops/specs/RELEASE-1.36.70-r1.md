# Đặc tả packet RELEASE-1.36.70 r1 — phát hành và deploy v1.36.70

Phiên: điều phối #1206 (land operator, PROTOCOL_DA_PHIEN §9: "phiên land … gán release, bump ba chỗ, hợp nhất changelog
fragment và tái sinh manifest"). Chủ kho duyệt deploy ngày 17-11-2026: "Đồng ý, land xong thì deploy luôn".

## 0. Bối cảnh đo được

- Package trên Drive (`1H5kAt3SRVP7…`): `tra-luat-skill-v1.36.69-working-method-r2.zip`, modifiedTime 2026-11-11T11:37:48Z.
- `VERSION` trên master: `1.36.69` (commit `dd9378d`, 27-10). Từ đó có 8 mảnh `changelog.d/` mới:
  wp-1009, wp-1030, wp-1038, wp-1052, wp-1099, wp-1223, wp-1224, wp-1334 (mảnh wp-1334 là P-D vừa land, merge `11eb100`).
- `test-fragments-check`: `status current` (bundled module không cần sinh lại tại thời điểm đo).
- `ai-dang-giu` các tệp write set: NGƯỜI_GIỮ 0 (đo trước khi cấp lease).

## 1. Write set (đúng 5 tệp)

`VERSION` · `scripts/tl.py` (chỉ hằng `VERSION`) · `SKILL.md` (chỉ dòng tiêu đề `v1.36.69`) · `CHANGELOG.md` (thêm một mục đầu tệp) ·
`RELEASE_MANIFEST.json` (tái sinh). Không sửa, không xoá mảnh `changelog.d/` (giữ nguyên tiền lệ: các bản trước không xoá mảnh).
Nếu `test-fragments-check` không còn `current` trên base thì DỪNG và hỏi (không tự mở rộng write set).

## 2. Việc

- M1: bump `1.36.69` → `1.36.70` đúng ba chỗ; guard `skill_md_version_matches_VERSION` phải đạt.
- M2: mục `# ★ v1.36.70 — r377: …` đầu `CHANGELOG.md`, tóm tắt 8 mảnh trên (mỗi mảnh một dòng, nêu số packet), không chép nguyên văn.
- M3: tái sinh `RELEASE_MANIFEST.json`; kiểm `git diff -- references/golden/` rỗng (không ghi golden).
- M4: PR → CI xanh → connector sạch → chủ kho duyệt merge đúng SHA (packet ghi sổ của land operator: không cần human audit JSON).
- M5 (deploy, sau merge): từ checkout ĐÚNG merge commit trên master, `core.abbrev 7`, chạy `./scripts/deploy-package.sh --push`
  (chốt bước 4: Drive phải < 1.36.70, không dùng `--force-older`). Sau đẩy: tải lại, đối chiếu md5/sha256 + VERSION (bước 5).

## 3. Nghiệm thu

| # | phép đo | đạt khi |
|---|---|---|
| N1 | `python scripts/tl.py --selftest` trên head | `N/N`, hai số bằng nhau |
| N2 | `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | `ok=true`, `expected == checked` |
| N3 | `git diff --numstat base..head` | đúng 5 tệp write set; `tl.py` +1/−1; `SKILL.md` +1/−1 |
| N4 | ruff `--select F` delta 0 trên `tl.py`; `doctrine-scan`, `adr-song` rc 0 | rc 0, delta 0 |
| N5 | CI trên head và ci.yml hậu merge | xanh; hồ sơ land đủ bốn mốc §10.2.2 |
| N6 | deploy | Drive trả tên chứa `v1.36.70`, tải lại byte-match (md5/sha256) với zip đã build, VERSION trong zip = `1.36.70` |

## 4. Ngân sách

Codex ≤ 2 (connector); CI Ubuntu ≤ 2; Windows native 0; deploy push ≤ 1 (thất bại thì dừng và báo, không đẩy lại tự động).
