# HANDOFF — GIAM-HOI-P2-ADR-E1-E5 r11 g1, executor Claude

Trạng thái: **đã áp đủ ba tệp của write set lên working tree, chưa commit** (theo chỉ thị: phiên điều phối commit).
Không dừng ở điều kiện dừng nào. Viết lúc `2026-11-14T17:2xZ` (15-11-2026 giờ Việt Nam).

```yaml
schema_version: 1
packet_id: GIAM-HOI-P2-ADR-E1-E5
packet_issue: 1292
revision: 11
generation: 1
lease_id: giam-hoi-p2-r11-g1-claude
spec_hash: 4d94f1fedd198547901cd310f04c83fa8984f310d9c3be72609e8c36d692a6e9
provider: claude
model_family: claude
execution_surface: claude_code
transport: machine/local
role: executor
session_id: 91b58a44-bc44-4fe7-a9a8-9552e9ce4229   # suy từ đường dẫn scratchpad của phiên, không phải biên nhận
base_sha: 072d45a0595f3d2ff9f0880143a237c9e0ea70c3
head_sha: null          # chưa có commit ứng viên; HEAD nền 5b5e6171f81ac8199041d8d569331b0a218860d6 KHÔNG phải candidate
status: needs_followup
summary: áp 10 khối thay và dựng ADR-0067 đúng byte từ đặc tả r11; ba cổng working tree rc 0; chờ commit, A1–A6, A8, review
changed_paths:
  - .claude/skills/soan-spec/SKILL.md
  - docs/PROTOCOL_DA_PHIEN.md
  - docs/adr/0067-danh-sach-dong-va-uy-quyen-thuong-truc.md
tests:
  - {name: doctrine-scan, status: passed, evidence: "rc 0; 'sạch — đã quét 12 tệp, 0 chỗ chép doctrine'"}
  - {name: adr-song, status: passed, evidence: "rc 0; '65 ADR trên đĩa, 65 dòng trong §20, khớp 1–1'"}
  - {name: doc-claims-check --strict --json (A9), status: passed, evidence: "rc 0; ok=true, flags=[], files_scanned=130"}
  - {name: git diff --check (working tree), status: passed, evidence: "rc 0, không output; KHÔNG phủ tệp ADR untracked, xem dưới"}
  - {name: kiem_p2.py (A1–A6), status: not_run, evidence: "vị từ đọc HEAD; chạy sau khi phiên điều phối commit"}
  - {name: "tl.py --selftest (A8)", status: not_run, evidence: "phiên điều phối chạy trên đúng SHA sẽ đẩy"}
  - {name: "git diff --check <base> HEAD (A7, vế thứ ba)", status: not_run, evidence: "cần commit"}
test_selection:
  gate_tier: null       # không chọn tier; chỉ chạy các lệnh chỉ thị giao
  tested_sha: null      # mọi phép đo là trên WORKING TREE trên nền HEAD 5b5e617, không phải trên một commit
remaining_work:
  - commit đúng working tree này thành H (phiên điều phối)
  - chạy kiem_p2.py trên H với base 072d45a; A7 vế git diff --check <base> HEAD; A8 selftest
  - handoff/evidence lên Packet Issue #1292, phản biện Codex, audit chủ kho trước push (ADR-0060 M12)
next_role: human        # phiên điều phối commit; sau đó reviewer Codex rồi chủ kho audit
failure: {fingerprint: null, category: null}
successors: []
```

## Ba mốc Git (§3.2.1)

| mốc | giá trị |
|---|---|
| Immutable acceptance baseline | `072d45a0595f3d2ff9f0880143a237c9e0ea70c3`, tree `d33f1356014cdb3e7bc14a5f0d5227dd7e88f17d` |
| Continuation base | HEAD `5b5e6171f81ac8199041d8d569331b0a218860d6` trên `agent/giam-hoi-p2-g1-codex`; cha 1 `728aaac027b0e42daf09963ded246160986f62a1`, cha 2 = base; tree `d33f1356…` (đo: bằng tree base) |
| Reviewed candidate | **chưa có**: working tree chưa commit. Hiện vật working tree ở bảng dưới |

`git rev-parse --is-shallow-repository` = `false`. Commit land packet 1 `bab2279eddd267df77f43a4bf32e168678857f6a` là tổ
tiên của base: `git rev-list --count bab2279..072d45a` = 10, chiều ngược = 0.

## Đặc tả

- Nguồn authoritative: `git show d26151370b9a86eb495457193e1a440e0bbeb764:ops/specs/GIAM-HOI-P2-ADR-E1-E5-r11.md`
  (`git cat-file -t d261513…` = `commit`; ref cục bộ `origin/ops/spec-giam-hoi-p2-r11` trỏ đúng OID ấy).
- sha256 byte thô, đo hai đường (`git cat-file blob … | sha256sum` và `sha256sum` trên bản chép):
  `4d94f1fedd198547901cd310f04c83fa8984f310d9c3be72609e8c36d692a6e9` — **khớp** băm chỉ thị và `spec_hash` của lease.
  1003 dòng, 87925 byte, không có CR.
- Bản chép: `D:\tlx\p2r11-scratch\spec-r11.md` (cùng băm). Không chép vào checkout.
- Lease đọc từ ref CỤC BỘ `origin/ops/giam-hoi-p2-lease` (`9f9bdeebd72a655593d77754b4caa35fc3360fe5`), tệp
  `ops/leases/giam-hoi-p2-r11-g1-claude.yaml`: `packet_id`, `revision: 11`, `generation: 1`, `executor: claude`,
  `spec_hash`, `base_sha`, `start_from_sha`, `write_set` đều khớp chỉ thị; `lease_until: 2026-11-15T17:18:46Z`, còn hạn
  lúc làm (`date -u` = `2026-11-14T17:24:11Z`). Không fetch, nên đây là bản sao cục bộ của ref, không phải trạng thái máy chủ.

## Tệp đã đổi

| tệp | thay đổi | dòng sau | sha256 trên working tree |
|---|---|---|---|
| `.claude/skills/soan-spec/SKILL.md` | +13 −13 (khối K4, K7) | 218 | `15229522381a690e456028e74296b4171d271c07cfa7a7bf09976eb098ac6bb1` |
| `docs/PROTOCOL_DA_PHIEN.md` | +22 −2 (khối Q02, Q12A, Q12B, Q12C, Q12D, Q13A, Q13B, Q20) | 1736 | `b7f621286b47462a510261e19a37511f831d4201adddadc73b4b3c5153878d2f` |
| `docs/adr/0067-danh-sach-dong-va-uy-quyen-thuong-truc.md` | tệp mới | 332 (`wc -l`) | `eb3c65d5d390f1468bd79428c57e8fcd345615c8fcb7973ea044057199f97519` |

Số dòng khớp mục 3 của đặc tả (332; +22 −2; +13 −13; tổng thêm 367). `git diff | sha256sum` (hai tệp tracked) =
`a3318d28e0f6feaa1d67b15323b7965fd95dd8bc1ca5aca78aff0deac3ee7bee`.

Cách áp: không gõ tay. `ap_dung.py` (thư mục nháp) nạp chính các hàm `cac_khoi`, `ky_vong`, `mau_adr`, `so_dong_co` của
`kiem_p2.py` đã trích, đọc tệp gốc bằng `git show <base>:<tệp>`, dựng bản kỳ vọng rồi ghi byte (`write_bytes`, LF). Mỗi
khối `cu` được đếm trên base: cả 10 khối **đúng 1 lần**, không chồng nhau (`ky_vong` không ném lỗi).
`docs/adr/0067-*` vắng trên base (`git ls-tree <base> docs/adr/ | grep 0067` rỗng; `co_tep` = false).

Dòng Trạng thái đã điền:

```
- **Trạng thái:** Accepted (2026-11-15, chủ kho `ducthangho` duyệt `spec_hash` `4d94f1fedd198547901cd310f04c83fa8984f310d9c3be72609e8c36d692a6e9` của đặc tả `GIAM-HOI-P2-ADR-E1-E5` r11 trên Issue #1292: https://github.com/ducthangho/tra-luat/issues/1292#issuecomment-6880923050)
```

## Số đo `{{SO}}` / `{{DONG}}` trên base `072d45a`

Lệnh cho từng tệp: `git show 072d45a0595f3d2ff9f0880143a237c9e0ea70c3:<tệp> | grep -c 'ADR-0067'` và
`git show 072d45a0595f3d2ff9f0880143a237c9e0ea70c3:<tệp> | wc -l` (Git Bash trên Windows).

| tệp cổng | `{{SO}}` | `{{DONG}}` |
|---|---|---|
| `ops/lease_publish.py` | 0 | 2604 |
| `.claude/dev/packet_loop.py` | 0 | 6247 |
| `.claude/dev/launcher.py` | 0 | 5988 |
| `.claude/dev/gate_lifecycle.py` | 0 | 1688 |
| `.github/workflows/ci.yml` | 0 | 1184 |
| `.github/workflows/ops-publish-lease.yml` | 0 | 277 |

`ap_dung.py` đối chiếu 12 số này với phép đếm của vị từ (`so_dong_co(goc, "ADR-0067")` và `goc.count("\n")`): khớp cả 12.
Sáu tệp cổng trên working tree cũng không chứa chuỗi `ADR-0067`.

## `kiem_p2.py`

Trích khối ```` ```python ```` duy nhất của mục 4 bằng `trich.py`: `D:\tlx\p2r11-scratch\kiem_p2.py`, 152 dòng, 6642 byte,
sha256 `4869d7e554be82d0b9eec56a95e4d94de1eda44867293b721b8523f85721e67d`. **Không chạy** (đọc `HEAD`).

Thay vào đó `ap_dung.py` làm một phép đối chiếu tương đương **trên working tree, không phải vị từ**: hai tệp `thay` bằng
đúng byte bản `ky_vong` dựng từ base; tệp ADR `fullmatch` `mau_adr(khuon)`; băm ở dòng Trạng thái bằng sha256 đặc tả; số
Issue trong câu bằng số trong URL; 12 số Cưỡng chế khớp. Kết quả: rc 0, dòng cuối `WORKING TREE KHOP`. Phép này không
thay A1–A6: nó không đo `git diff --name-only <base> HEAD` và dùng chung mã với vị từ nên không độc lập với nó.

## Lệnh đã chạy (cwd `D:\tlx\p1`, Python 3.13.1, Git Bash)

rc đọc từ trạng thái thoát mà công cụ Bash báo cho từng lệnh chạy riêng (phiên không tương tác chặn `echo $?`).

| lệnh | rc | dòng kết luận |
|---|---|---|
| `python -B .claude/dev/packet_loop.py doctrine-scan --root .` | 0 | `doctrine-scan: sạch — đã quét 12 tệp, 0 chỗ chép doctrine` |
| `python -B .claude/dev/packet_loop.py adr-song --root .` | 0 | `adr-song: sạch — 65 ADR trên đĩa, 65 dòng trong §20, khớp 1–1 (tha thiếu trạng thái: ['0016'])` |
| `python -B scripts/tl.py doc-claims-check --strict --json` | 0 | `"ok": true`, `flags: []`, `files_scanned: 130`, `by_layer` mọi lớp 0, `layers_skipped: {}`, 379 advisory (không chặn; không cái nào thuộc tệp 0067), stderr rỗng |
| `python -B scripts/tl.py doc-claims-check --strict --json --path docs/adr/0067-danh-sach-dong-va-uy-quyen-thuong-truc.md` | 0 | `"ok": true`, `files_scanned: 1`, `flags: []`, `advisories: []` (phép phụ, xem dưới) |
| `git diff --check` | 0 | không output |
| `git status --short` | 0 | ` M .claude/skills/soan-spec/SKILL.md` · ` M docs/PROTOCOL_DA_PHIEN.md` · `?? docs/adr/0067-danh-sach-dong-va-uy-quyen-thuong-truc.md` |
| `git diff --numstat` | 0 | `13 13 .claude/skills/soan-spec/SKILL.md` · `22 2 docs/PROTOCOL_DA_PHIEN.md` |
| `wc -l docs/adr/0067-…md` | 0 | `332` |
| `python -B ap_dung.py spec-r11.md 072d45a… so_do.json` | 0 | `WORKING TREE KHOP` |

Log đầy đủ trong thư mục nháp: `log-doctrine-scan.txt`, `log-adr-song.txt`, `log-doc-claims-check.json` (75884 byte),
`log-doc-claims-check.stderr.txt` (0 byte), `log-doc-claims-check-adr-only.json`.

Hai phép phụ, vì hai lệnh được giao không phủ tệp ADR untracked theo cách hiển nhiên:

- `git diff --check` chỉ so index với working tree, nên **không đọc tệp untracked**. Đo bù trên tệp ADR: 0 dòng có khoảng
  trắng cuối dòng (regex `[ \t]+$`), 0 ký tự CR, tệp kết thúc bằng đúng một `\n` (`od -c` ở đuôi). Vế
  `git diff --check <base> HEAD` của A7 vẫn phải chạy sau commit.
- `doc-claims-check` liệt kê tệp bằng `Path.rglob("*.md")` trên đĩa (`scripts/tl_core/workflow.py:1013`), không qua
  `git ls-files`, nên tệp untracked nằm trong 130 tệp đã quét; lượt `--path` riêng xác nhận tệp ấy được đọc và sạch.

## Không làm / không đo được

- Không commit, không đổi nhánh, không push, không gọi GitHub, không dùng mạng, không `git fetch`. Không chạy
  `packet_loop.py init`/`begin-attempt`/lệnh ghi state. Không đăng heartbeat hay handoff lên Issue (không có quyền mạng).
- Không chạy `kiem_p2.py`, A8 (`tl.py --selftest`), ruff (diff không chạm `.py`).
- **Không chạy đột biến nào** của bảng mục 4 (kể cả đột biến A9 đưa lại dấu nháy ngược): mỗi đột biến đòi sửa tệp trong
  write set hoặc một bản sao cây, ngoài việc được giao.
- **Không đo được** comment `issuecomment-6880923050`: có tồn tại không, của ai, có neo đúng băm r11 không. URL lấy
  nguyên từ chỉ thị và khớp `granted_on_instruction` của lease.
- Không đo `core.eol`/`core.abbrev` bằng `git config` (lệnh bị chặn chờ duyệt). Đọc thẳng `.git/config`:
  `autocrlf = false`, `abbrev = 7`, không có dòng `eol`; `.gitattributes` khai `* text=auto eol=lf`, và
  `git ls-files --eol` trước khi sửa cho `i/lf w/lf` ở cả hai tệp tracked.
- Hook của kho chặn hai lệnh chỉ đọc (`git stash list`, `git merge-base --is-ancestor`) với lý do
  `Codex supervision guard: Git or GitHub mutation`; quan hệ tổ tiên đo bằng `git rev-list --count` thay thế.

## Chỗ đặc tả có vấn đề (không sửa, chỉ ghi)

1. **Hàng `executor` của đặc tả ghi `codex`** (adapter `.agents/skills/work-packet/SKILL.md`, model `gpt-6-astra`), còn
   lượt này chạy bằng Claude theo `executor_note` của lease. Đặc tả đóng băng và lease lệch nhau ở hàng ấy; tên nhánh vẫn
   là `agent/giam-hoi-p2-g1-codex`. Hàng `reviewer` của đặc tả gọi lượt Codex là `same_provider_approved` (đúng khi
   executor là Codex); lease ghi lại thành `cross_approved`. Không ảnh hưởng byte nào của diff.
2. **Ngày ở dòng Trạng thái là "ngày land"** theo mục 2, nhưng phải điền trước khi land. Đã điền `2026-11-15` theo chỉ
   thị. Vị từ (A3) chỉ kiểm ngày hợp lệ, nên land trượt sang ngày khác thì ADR mang ngày sai mà không phép đo nào đỏ.
3. **Dòng Trạng thái khai "chủ kho `ducthangho` duyệt `spec_hash`" và trỏ một comment mà lease mô tả là "ghi hộ"**
   (`granted_on_instruction_note`). Chính ADR này, mục *Comment ghi hộ*, nói tên tác giả comment không chứng minh ai đã
   quyết. Tôi không đọc được comment nên không biết nó mang nhãn ghi hộ hay là comment của chính chủ kho.
4. **Mục Cưỡng chế của ADR viết "Đo lúc land"**, còn số được đo lúc thi công trên base của lease. Hai thứ trùng nhau
   chừng nào base không đổi; vị từ đo lại trên đúng base nên A4 vẫn bắt được lệch.
5. A7 liệt kê `git diff --check <base> HEAD` (chỉ chạy được sau commit); lệnh `git diff --check` giao cho executor không
   phủ tệp mới. Đã đo bù như trên.

Không thấy câu nào trong các khối `adr`/`thay` cần đề xuất revision: `doctrine-scan`, `adr-song` và `doc-claims-check`
đều rc 0 ngay lượt đầu, không phải sửa gì.

## Việc kế tiếp cho phiên điều phối

```
git add .claude/skills/soan-spec/SKILL.md docs/PROTOCOL_DA_PHIEN.md docs/adr/0067-danh-sach-dong-va-uy-quyen-thuong-truc.md
git commit …            # đúng working tree này; sau commit `git status --short` phải rỗng
python D:\tlx\p2r11-scratch\kiem_p2.py D:\tlx\p2r11-scratch\spec-r11.md 072d45a0595f3d2ff9f0880143a237c9e0ea70c3   # đòi rc 0, dòng cuối ĐẠT
git diff --check 072d45a0595f3d2ff9f0880143a237c9e0ea70c3 HEAD
python scripts/tl.py --selftest          # A8, N/N
```

Blob kỳ vọng sau commit phải có sha256 bằng ba băm ở bảng *Tệp đã đổi* (`git show HEAD:<tệp> | sha256sum`).
