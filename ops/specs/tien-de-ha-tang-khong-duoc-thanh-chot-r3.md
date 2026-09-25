# TIEN-DE-HA-TANG-KHONG-DUOC-THANH-CHOT — revision 3

Goi #593. Tep: `ops/nhanh_don_duoc_test.py`. Tiep noi revision 2 (`...-r2.md`, sha256
`ca05fac0...ad08454`), da LAND o master `0e2fe84` (PR #629).

| truong | gia tri |
|---|---|
| `packet_id` | `TIEN-DE-HA-TANG-KHONG-DUOC-THANH-CHOT` |
| `packet_issue` | 593 |
| `revision` | 3 |
| `review_class` | `sensitive` (cham nen ha tang cua MOI ca co fixture git) |
| `write_set` | `ops/nhanh_don_duoc_test.py` — MOT duong |
| `start_from_sha` | `4c53c76d1955595a5659ab577d9dc1b64f9600ad` (master luc mo r3) |
| tran dong them | **80**, DO bang `git diff --numstat 4c53c76 -- ops/nhanh_don_duoc_test.py` |

## 0. Nguon cap viec va chi thi

Phien wp461 bao (issues/593#issuecomment-5828404355): `gate-registry` DO tren master `4c53c76`
(job 107949420933) va hai lan tren PR #636 (job 107949106732, 107963706385), ca ba cung hinh:
`dot bien giet 192/193`, mot dot bien bi xep TIN DUNG GIA vi ca `r546` chet do
`OSError: [Errno 39] Directory not empty: '/tmp/.../remote.git'` (lan #636-1: `.../remote.git/objects`).
Executor da doc log master va xac nhan.

Chu kho chon trong phien Claude Code 2026-09-25 ~08:3xZ: *"Mo r3, tat bao tri git (Recommended)"* —
va tat bao tri git o moi lenh git con, KHONG dung thu-lai de che; kem ca khoa; tran 80.

## 1. Benh — do duoc, co che CHUA do duoc

- DO DUOC: `td.cleanup()` cua fixture `kho_bare` (rmtree tren thu muc chua `remote.git`) gap
  `ENOTEMPTY` — co thu dang ghi vao `remote.git` (hoac `remote.git/objects`) trong luc xoa.
- DO DUOC: loi CO SAN truoc goi — chu thich tai `ops/nhanh_don_duoc_test.py` (quanh dong 396) ghi
  cung chu ky `VO CAN r506 ... remote.git` tu thoi #568. r2 KHONG tao loi; r2 (a) them `r546` chay lai
  moi ca TU_KIEM ben trong dot bien => so lan dung/xoa `kho_bare` tang nhieu lan, va (b) so ha tang cua
  r2 bat loi dung nhu thiet ke (TIN DUNG GIA thay vi nuot).
- GIA THUYET, KHONG DO DUOC tai cho: tien trinh `git maintenance run --auto` / `gc --auto` do
  `receive-pack` (sau `git push`) hoac `fetch` sinh ra, chay TACH NEN, giu khoa/ghi vao `objects/`
  sau khi lenh git cha da tra ve. Container dev co git 2.43; CI co git 2.55. Tai cho: 0/60 lan tai
  hien (vong push+fetch+rmtree). Chi CI moi do duoc hieu qua ban va.

## 2. Closure

- **M1** — Luc nap module test, NOI THEM vao `GIT_CONFIG_COUNT`/`GIT_CONFIG_KEY_<n>`/
  `GIT_CONFIG_VALUE_<n>` cua `os.environ` (KHONG ghi de — moi truong co the da mang credential git
  qua chinh co che nay) cac khoa:
  `gc.auto=0`, `gc.autoDetach=false`, `maintenance.auto=false`, `maintenance.autoDetach=false`,
  `receive.autogc=false`. Idempotent: nap lai (ban sao dot bien, tien trinh con) khong them trung.
  Moi tien trinh git con — ke ca qua `ops/nhanh_don_duoc.py` va ban sao dot bien — thua ke.
- **M2** — Ca khoa moi: mot `git config --get <khoa>` chay qua `run()` trong mot kho tam phai tra
  dung gia tri da dat cho TUNG khoa; va cac bien `GIT_CONFIG_*` co san truoc khi nap phai con nguyen
  (so sanh truoc/sau). Kem dot bien: bo nap (M1 thanh no-op) => ca khoa DO; ghi de thay vi noi =>
  ca khoa DO.
- **M3** — KHONG them thu-lai, KHONG `ignore_errors=True`, KHONG noi long so ha tang cua r2.

## 3. Cam

- Che trieu chung (thu-lai rmtree, nuot `OSError` khi don, loai `r546` khoi dich).
- Doi `ops/nhanh_don_duoc.py`, `ci.yml`, hay bat ky tep ngoai write set.
- Khai "da chua" truoc khi CI tren head moi xanh; ghi ro so luot CI da do.

## 4. Nghiem thu

- Luot day du tai cho rc=0 · TU KIEM N/N · dot bien giet M/M · MUTANT 10/10 · stderr 0 B.
- CI tren head PR: `gate-registry` xanh. Mot luot xanh KHONG chung minh het chap chon — khai dung
  nhu vay; theo doi luot master sau land.
- Ruff F delta = 0.

## 5. Ngoai pham vi / KHONG DO DUOC

- Co che chinh xac trong git 2.55 (xem §1).
- Windows.
