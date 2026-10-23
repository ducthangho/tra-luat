# Handoff wp868 — executor claude, lease `wp868-r1-g1-claude`

Bản CUỐI — PR #873 đã được chủ kho merge 2026-10-23T01:10:05Z (head `f07f88c`). Nguồn sự thật: spec `ops/specs/wp868.md`
(sha256 `0d950c2b98b9e024bf1cc43a77c5d3351b5f4c21e6307b2e36ba9cdeca7b3f69`), lease `ops/leases/wp868-r1-g1-claude.yaml`.

```yaml
schema_version: 1
packet_id: wp868
generation: 1
spec_hash: 0d950c2b98b9e024bf1cc43a77c5d3351b5f4c21e6307b2e36ba9cdeca7b3f69
provider: claude
model_family: claude
execution_surface: claude_code
transport: machine/local
role: executor
session_id: session_01WgcSwsdNhpznNmmkxeLBuA
base_sha: 9e9a74b2a396ef458d25c51a5563efafbb45ba0c
head_sha: f07f88c75cabbef691c86ac8746317a6c0705162     # PR #873, merged bởi ducthangho 2026-10-23T01:10:05Z
status: done
summary: >-
  Kenh ket qua rieng giua chon_thu_muc_chay_duoc va reader (tep mktemp, bien khong export ke ca duoi allexport, trap +
  rm tuong minh): GIU_PATH | DICH+LF+thu muc; cong thuc chay `( set +e; eval ) > tep` (khong cho EOF stdout); kenh rong =>
  dong cuoi stdout (N3); doc hong / payload la => exit 7. rg dung bo chon chung (N4). Ca r868_* cho N1(a)(b)(c)(d), N2,
  N3 (LF+CRLF), N5, F868-01..06; (a)(b) va N2 DO tren 9e9a74b. Ratchet goi 190->191, manifest 191.
changed_paths: [ops/cai_cong_cu.sh, ops/cong_cu.yaml, .claude/dev/launcher_test.py, scripts/tl_selftest.py,
                RELEASE_MANIFEST.json, changelog.d/wp-868.md]
tests:   # tren f07f88c tru khi ghi khac
  - {name: launcher_test, status: passed, evidence: "head 250/250 (bo qua 2, /tmp/.git vang); nen 242/242 vs head 247/247 o 1965b71, co va khong CODEX_AUTH_JSON gia, hai ve dung trong MOT lenh"}
  - {name: launcher_test --dot-bien, status: passed, evidence: "Linux 310/310 (4 khong do duoc); launcher-windows.yml 39768109565 success"}
  - {name: tl.py --selftest, status: passed, evidence: "1731/1731"}
  - {name: release-verify --strict, status: passed, evidence: "ok=true, expected=checked=191 (manifest 1965b71; cac commit sau chi doi tep ngoai goi, tai sinh cho ra cung tep)"}
  - {name: cong_cu_test (CONG_CU_TEST_BAN_KINH=manh), status: passed, evidence: "61/61, tien kiem bo qua 0, cong cay that DAT; ban kinh 470 o gate-cong-cu CI (8 manh success)"}
  - {name: ruff F delta, status: passed, evidence: "tl.py 12=12 · tl_selftest 4392=4392 · launcher_test 5=5"}
  - {name: doctrine-scan / doc-claims-check --strict / actionlint / bash -n, status: passed, evidence: "rc0 / ok:true / rc0 nen va head / ok"}
  - {name: ci.yml, status: passed, evidence: "run 39765044279 attempt 2 success tren f07f88c"}
  - {name: launcher-windows.yml (workflow_dispatch), status: passed, evidence: "run 39768109565 success tren f07f88c"}
  - {name: Codex cross-review, status: passed, evidence: "luot 5/5 (684d95a7) approve tren f07f88c; F868-01..06 dong"}
remaining_work: []
next_role: null
manual_next_action: null
copyable_prompt: null
failure: {fingerprint: null, category: null}
successors: []
```

## Q4 — ca/đột biến cũ đã đổi, vì sao (hợp đồng đổi CÓ CHỦ ĐÍCH)

| Thứ đổi | Trước | Sau | Lý do |
|---|---|---|---|
| `r831` F01 (`_wp831_cai_rg_chon_ban_chay_duoc`) | eval công thức `rg` TRỰC TIẾP, đòi dòng in cuối = thư mục bản tốt đầu PATH | chạy qua `cai_cong_cu.sh`, đòi DAT và `$GITHUB_PATH` KHÔNG nhận thư mục ứng viên | `rg` nay dùng bộ chọn chung: tên trần đã DAT ⇒ `GIU_PATH`, không in thư mục nào. Ý đồ giữ nguyên: ứng viên không thực thi không bị chọn. Nhánh `truc_tiep` của helper wp831 bị bỏ (không còn ai gọi). |
| harness `truc_tiep` của `_wp858_chay_cai` | `eval "$LENH"` rồi đọc dòng in cuối stdout | cấp `KENH_KQ` tạm, chạy `( set +e; eval ) > out`, in như reader (kênh có nội dung ⇒ kênh, rỗng ⇒ stdout) | Bộ chọn không còn in ra stdout; không cấp kênh thì nó `return 1` và các ca `rc != 0` xanh VÔ NGHĨA. Đọc như reader giữ mutant `wp858_yaml_python_linux_ve_dirname` chết bằng hành vi. |
| `r858_hinh_dang_cong_thuc_cai` | 12 công thức; chốt `printf '\n%s\n' /dev/null` / `"$dich"` | 15 công thức (thêm `rg`); chốt `GIU_PATH`/`DICH` trên kênh + vòng duyệt có `break` | N4 + Q3. |
| đột biến `wp858_sh_bo_dong_canh_giu_path` · `dong_canh_la_ten_thu_muc` · `dong_canh_khong_tach_dong` | neo dòng canh `/dev/null` | neo dòng ghi `GIU_PATH` · payload `DICH` sai · nhánh `GIU_PATH` đọc stdout | dòng canh bị thay bằng kênh (Q3); giữ ý đồ "tên trần đã DAT thì không đổi PATH". |
| đột biến `wp802_yaml_bo_ung_vien_winget_links` · `wp831_yaml_{linux_bo_ung_vien_usrbin,macos_bo_ung_vien_brew}` | neo vòng `RG_D` riêng | neo đối số ứng viên của `chon_thu_muc_chay_duoc rg`; thêm `r858_hinh_dang_cong_thuc_cai` để đo được trên Windows | N4. |
| BỎ 5 đột biến YAML: `wp802_yaml_chon_ung_vien_chi_theo_ma_thoat`, `wp802_yaml_khong_ghi_github_path`, `wp831_yaml_linux_chi_theo_ma_thoat`, `wp831_yaml_macos_bo_kiem_thuc_thi`, `wp831_yaml_linux_ghi_github_path_vo_dieu_kien` | logic chọn/ghi PATH nằm trong YAML `rg` | logic ấy nay ở hàm chung, đã có `wp858_sh_chon_theo_ma_thoat` · `wp858_sh_nuot_loi_ghi_github_path` · `wp858_sh_bo_kiem_ten_tran` canh | neo không còn tồn tại; không xoá ca test nào. |

## Đo môi trường (Q9, packet khác — không vá)
- Sau khi một lượt Codex KẾT THÚC, `/tmp/.git` RỖNG (không còn mount) còn sót ⇒ 11 ca `r484_*` đỏ
  ("Codex home is inside a repository"). `rmdir /tmp/.git` (chỉ thư mục rỗng do chính lượt Codex của phiên này tạo) ⇒ cả
  11 ca xanh. Mở rộng nợ `r484_*`/`/tmp/.git` của #858: không chỉ KHI Codex đang chạy mà cả SAU khi nó thoát.
- `ci.yml` run 39746531917 (`ac4a6cb`): `chuan-bi` đỏ hai lần, ~5 s, `runner_id: 0`, log 404 — chưa cấp runner.
  Comment PR #873 issuecomment-6336148808.

## Review — 5 lượt Codex (`gpt-6.1-sol`, `xhigh`, qua `.claude/dev/launcher.py run`)
| Lượt | Head | Run | Verdict | sha256 (12) |
|---|---|---|---|---|
| 1 | `1965b71` | `fe6f5deb` | changes_requested — F868-01 P2 (đọc kênh lỗi nuốt) · 02 P2 · 03 P3 | `0a2e05421e5f` |
| 2 | `ac4a6cb` | `d675fb83` | changes_requested — 01–03 đóng; F868-04 P2 (lỗi ghi payload) · 05 P3 | `667af2a30eaf` |
| 3 | `93d33b4` | `1f61bfda` | changes_requested — 01–05 đóng; F868-06 P3 (allexport) | `d327dacae9d3` |
| 4 | `0bfc73d` | `6427f213` | changes_requested — 06 đóng; F868-02 mở lại (cleanup trên exit 7 reader) | `bf0dd45fa0d2` |
| 5 | `f07f88c` | `684d95a7` | **approve** — F868-01…06 đóng | `fc42378a86cc` |

Tệp: `ops/reviews/wp868-g1-luot{1..5}-codex-verdict.md` trên nhánh này. Duy nhất F868-01 là lỗi runtime (vá ở reader,
`cat && printf x`); 02–06 là khoảng trống test. Connector Codex GitHub review `0bfc73d`: không finding.

## Nợ có tên — trạng thái
- `cai-stdout-writer-muon` — ĐÓNG (N1(a), N2; đỏ trên `9e9a74b`).
- `rg-installer-stdout-khong-LF` — ĐÓNG (N1(b) + N4; đỏ trên `9e9a74b`).
- `vong-duyet-ung-vien-chua-khoa` — ĐÓNG (`r868_vong_duyet_ung_vien`, đột biến chỉ-hai-ứng-viên / bỏ-break).
- `python-probe-khong-theo-PATH` — giữ nguyên, ngoài phạm vi.
- Giới hạn ghi nhận, KHÔNG mở finding (reviewer lượt 3–5 đồng ý): mutant bỏ `pipefail` chỉ đổi kết quả với recipe có
  pipeline — YAML hiện không có recipe nào như vậy; caller bắt STDERR của `cai_cong_cu.sh` vẫn chờ EOF stderr của writer nền
  (N2 chỉ hứa stdout).
- Thứ tự commit (N7): manifest sinh ở `1965b71`; năm commit sau chỉ đổi `ops/cai_cong_cu.sh` / `.claude/dev/launcher_test.py`
  (ngoài gói) — tái sinh cho ra tệp y hệt nên không có commit manifest mới; `release-verify --strict` 191/191 trên `f07f88c`.

## Bài học đo được (đề nghị ghi CLAUDE.md qua packet có quyền)
- `( eval )` khác `$( eval )` ở errexit: subshell `( )` KẾ THỪA `set -e`, command substitution thì không. Đổi `$( )` →
  `( ) > tệp` mà quên `set +e` làm các `return 1` tường minh thành tương đương (mutant sống) — đo được ở lượt dot-bien 1.
- Hàm bash export qua môi trường (`BASH_FUNC_printf%%`) là cách tiêm lỗi vào builtin mà không sửa script — dùng cho F868-04.
- `/tmp/.git` rỗng do sandbox Codex để lại SAU khi lượt chạy kết thúc (không chỉ trong lúc chạy) làm 11 `r484_*` đỏ.
