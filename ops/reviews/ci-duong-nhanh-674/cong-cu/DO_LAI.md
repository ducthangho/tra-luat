# BANG DO — khai cua executor #674 va cach do lai

Moi muc kem lenh de tu chay. Bang nay TU KHAI GIOI HAN cua no: cac lenh loc theo tieu chi ghi ben duoi, nen bo sot
nhung khang dinh dinh luong khac. **Moi khang dinh dinh luong ban tim ra ma bang nay bo sot deu tinh la finding.**

| khang dinh | lenh do lai | gioi han cua phep do |
|---|---|---|
| bo test: `CA: N/N` va `DOT BIEN: M/M` bang nhau, `TU KIEM PHAN HANG: DAT`, `TONG: DAT` (KHONG ghim so trong bang nay; so that = dong in cua lenh, ~1-1,5 phut) | `python3 -B ops/ci_duong_nhanh_test.py` (trong `cay/`) | Linux, khong Windows; dot bien la thu executor tu nghi ra (ca cac dot bien len chinh tep test qua `--nguon-test`) |
| phan ra: cac ca `t*` (hanh vi), `y*` (cau truc ci.yml), `k*` (so dang ky), `t98`/`t99` (tu kiem); ba ca du lieu t23/t26/t27 cua lease_publish_test ~6-7 giay | lay tu `CA` va `DOT_BIEN` trong tep test (AST); do `kiem_ca_du_lieu` | thoi gian phu thuoc may; khong ngoai suy sang runner Actions |
| lease 6/113 (clone MOT ref) vs 0/113 (552 ref): so cua PHAM VI refs, khong phai cua kho | `python3 -B ../goi/do_lai_so.py` chay tren clone day du; muon so 6 phai clone `--single-branch` master roi chay `kiem(bo_qua_han=True)` tren `ops/leases/*.yaml` | refs cua runner Actions CHUA DO |
| ci_dang_ky_test: 22/22 (nen) -> 23/23 (sau), 938/938 phan chung | `python3 .claude/dev/ci_dang_ky_test.py`; nen = `git stash`/checkout `1741e0a` | so 938 khong doi vi khong sua logic |
| ci_dang_ky_test.py: dung 1 dong them | `git diff --numstat 1741e0a HEAD -- .claude/dev/ci_dang_ky_test.py` (mong `1 0`) | |
| actionlint rc=0 (co shellcheck 0.9.0), nen cung rc=0; dot bien `${{ }}` rong trong comment `run:` => rc=1 | `actionlint .github/workflows/ci.yml` | phien nay cai shellcheck 0.9.0; ban CI co the khac |
| ruff F tren scripts/tl.py: 12 loi (delta 0 so voi nen) | `python3 -m ruff check --no-cache --select F scripts/tl.py` | chi doc tl.py, khong do file moi (file moi sach: `ruff check --select F ops/ci_duong_nhanh*.py`) |
| AL_VER: 4 dong | `grep -cE '^\s*AL_VER:\s*[0-9]+\.[0-9]+\.[0-9]+' .github/workflows/ci.yml` (regex cua t152) | |
| 345 lan merge; 63 chi doi ho so; 8/63 truot `git diff --check` nguyen ban; 6/113 lease truot `kiem(bo_qua_han=True)` | `python3 -B ../goi/do_lai_so.py` (chay trong `cay/`) | chi 400 merge first-parent gan nhat tu `1741e0a`; `diff` la `a...b` cua cha 1/cha 2; khong do PR that (fork, rebase); `--check` do tren TOAN diff |
| G5 (`ops/cong_cu*`) chiem 46,5 phut / 52 phut cua job `gate` tren run 36518707072 | doc job steps cua run do tren GitHub (khong tai lap duoc offline) | **KHONG DO DUOC** trong sandbox (khong mang); la so lay tu API, executor khong tu do lai; #668 dang chia G5 thanh manh |
| `skipped` cua job phu thuoc duoc GitHub tinh la dat cho required check | tai lieu GitHub | **CHUA TU DO** — la co so cua `continue-on-error` o job `chuan-bi` |

| MOI TAT CA so luong (so ca, so dot bien, phan ra, mau rc, dot bien tu kiem, so buoc if...) | `python3 -B ../goi/kiem_ke.py` (chay trong `cay/`) — DEM TU CAU TRUC, khong ghim so; dong `TU KIEM PHAN HANG:` cua bo test cung in so mau rc/dot bien that dem tu hai hang so | bang nay khong ghi so cu the de khoi troi; so nao khong co trong dau ra `kiem_ke.py` la khang dinh chua duoc kiem ke |
