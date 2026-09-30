Reviewed commit: 57b6578398a63c2afe4e583061440b3156aec155

# Cross-review lượt 8 — packet #674 CI-DUONG-NHANH-HO-SO

advisory_review: Claude (Opus, vai review-opus-max) review mã do Claude viết — mức bảo đảm ADVISORY, không phải review độc lập khác provider.
Trạng thái: HOÀN TẤT — **changes_requested** · TONG: P0=0 P1=0 P2=0 P3=2

## H0 — Số đo nền (chạy lại trong $R/cay, PYTHONDONTWRITEBYTECODE=1)
- `python ops/ci_duong_nhanh_test.py` ⇒ `CA: 71/71 dat · 0 do · 0 hong` · `DOT BIEN: 168/168 bi giet dung ly do` ·
  `KIEM KE: ca hanh_vi=43 + cau_truc_yaml=16 + so_dang_ky=3 + tu_kiem=9 = 71 · dot bien ...=2 + ci.yml=65 + ci_duong_nhanh.py=59 + ci_duong_nhanh_test.py=42 = 168` ·
  `TU KIEM PHAN HANG: DAT (5 mau rc, 3 dot bien that)` · `TONG: DAT` (47,8 s).
- `python .claude/dev/ci_dang_ky_test.py` ⇒ `ĐĂNG KÝ: 23/23` · `PHẢN CHỨNG: 938/938 đỏ đúng` · `TỔNG: ĐẠT`.
- `actionlint .github/workflows/ci.yml` ⇒ rc=0 (shellcheck CÓ mặt: /usr/bin/shellcheck — nền đo mạnh).
- Khớp lời khai executor từng số.

## H1 — Bản vá symlink `kiem_loai_tep`: fixture git THẬT qua `ci_duong_nhanh.py kiem-re` thật (log: out/h1-fixture.log, script tmp/fx.sh)
| Kịch bản (base→head) | diff | kiem-re | Đúng? |
|---|---|---|---|
| A symlink TREO thêm mới `ops/specs/zz-treo.md` | A 120000 | rc=1 `tep ho so la symlink` | đúng |
| B symlink HỢP LỆ trỏ ra ngoài (`../../CLAUDE.md`) | A 120000 | rc=1 | đúng (chặn cả loại hợp lệ, theo thiết kế) |
| C ĐỔI KIỂU tệp thường→symlink (`:100644 120000 … T`) | T | rc=1 | đúng — bắt cả phần ĐỔI, không chỉ phần thêm |
| D đổi ĐÍCH symlink có sẵn (base' đã có symlink) | M 120000 | rc=1 | đúng |
| F symlink→tệp thường | T | rc=0 | đúng (không chặn oan) |
| G xoá symlink | D | rc=0 | đúng |
| H symlink tới THƯ MỤC (`../land`) | A 120000 | rc=1 | đúng |
| I đối chứng tệp thường `ops/land/zz-ok.yaml` | A | rc=0 | đúng |
| J symlink treo tên `.yaml` dưới `ops/leases/` | A | rc=1 (2 lỗi: symlink + t23 FileNotFoundError) | đúng |
| E **gitlink** 160000 `ops/land/zz-sub` | A 160000 | **rc=0 DAT** | xem H2 |
Kết luận H1: chốt symlink đúng ở mọi dạng 120000 (thêm/đổi kiểu/đổi đích/thư mục), không chặn oan tệp thường, xoá, hay symlink→thường.

## H3 — Đột biến bản vá mới (`kiem_loai_tep`), mỗi mutant một bản clone riêng, PYTHONDONTWRITEBYTECODE=1 (tmp/mut.py; out/h3-mut.log, out/h3-mut-b.log)
Lượt a (thay thẳng vị từ — ĐỤNG neo của mutant `loai_tep_cho_symlink_qua`): M1/M3/M4/M5/M7 cho `CA: 71/71` nhưng `TONG: DO` CHỈ vì
`[DOT BIEN KHONG BI GIET DUNG] loai_tep_cho_symlink_qua: HONG … neo … thay 0` ⇒ **TÍN DỤNG GIẢ**, không tính là giết. M2 (`sorted(doi)[:1]`)
bị giết thật (CA 70/71). M6 (`exists()` — chặn mọi tệp) bị giết thật (CA 67/71).
Lượt b (giữ nguyên neo, chèn một dòng lọc `doi` trước `return`) — **SÁU mutant SỐNG, `CA: 71/71 · DOT BIEN: 168/168 · TONG: DAT`, rc=0**:
| Mutant | Hành vi mutant | Kết quả |
|---|---|---|
| N1_chi_symlink_treo | chỉ chặn symlink TREO; symlink hợp lệ lọt | SỐNG |
| N3_chi_duoi_md | chỉ chặn symlink đuôi `.md` | SỐNG |
| N4_chan_ca_tep_da_xoa | chặn OAN mọi tệp hồ sơ bị XOÁ | SỐNG |
| N5_chi_ops_specs | chỉ canh `ops/specs/` | SỐNG |
| N7_bo_qua_symlink_thu_muc | symlink tới THƯ MỤC lọt | SỐNG |
| N8_bo_qua_ops_leases | bỏ `ops/leases/` | SỐNG |
Gốc: `t20n` có đúng MỘT hình dạng (symlink TREO, `.md`, `ops/specs/`, thêm mới) cộng một đối chứng thêm tệp thường; không ca `kiem-re` nào đi qua
một tệp hồ sơ bị XOÁ. HEAD đúng ở cả sáu hình dạng (H1 đo bằng fixture thật) — đây là lỗ RĂNG, không phải lỗi hành vi.

## H2 — Lỗi HÀNH VI của kiem-re ở đầu vào biên (fixture git thật, hai vế dựng trong MỘT lệnh)
- **gitlink 160000** `ops/land/zz-sub` (không đuôi yaml): kiem-re DAT; các bước bị bỏ đo được — `t82` rc=0, golden/determinism/release-check full
  rc=0 cả hai vế (out/h2-gitlink.log). gitlink tên `.yaml` dưới `ops/leases/` bị bắt GIÁN TIẾP bởi `t23` (IsADirectoryError), không bởi
  `kiem_loai_tep`. Chưa đo được delta ⇒ KHÔNG mở finding; chỉ ghi: docstring "chỉ nhận tệp THƯỜNG" rộng hơn phép đo (chỉ đo symlink).
  lease_publish_test/packet_loop_test đầy đủ hai vế: xem cập nhật cuối.
- **tên tệp không phải UTF-8** `ops/reviews/zz-\xff\xfe.md`: phân loại `duong_nhanh`, kiem-re DAT; t82/golden/determinism/release-check/
  workflow-audit/doc-claims/eol-survey: rc hai vế BẰNG NHAU (golden/determinism/doc-claims rc=2 ở CẢ HAI vế do clone chưa ghim core.abbrev —
  delta = 0). Không finding (out/h2-non-utf8.log).
- **FINDING — PR hồ sơ XOÁ ĐÍCH của một symlink CÓ SẴN dưới allowlist** (out/h2-xoa-dich.log, tmp/xd.sh):
  nen = 57b6578 + symlink HỢP LỆ `ops/reviews/zz-l.md -> ../specs/zz-a.md` (giả định đã land qua đường ĐẦY ĐỦ — đường đầy đủ không cấm
  symlink hợp lệ, t82 chỉ đỏ với symlink treo); dot = nen + PR chỉ `D ops/specs/zz-a.md`.
  ```
  dot phan-loai: che_do=duong_nhanh
  dot kiem-re rc=0 DUONG_NHANH: kiem-re DAT (1 tep doi, 0 loi)|
  dot t82 rc=1 shutil.Error: [('…/xd_dot/ops/reviews/zz-l.md', '/tmp/lp_knm6k2po/repo/ops/reviews/zz-l.md', "[Errno 2] No such file or directo…
  nen t82 rc=0 DAT t82
  ```
  Tức PR hồ sơ xanh cả ba check, `gate-ops` ĐỎ trên master — đúng lớp F1 lượt 7, đường vào THỨ HAI: `kiem_loai_tep` chỉ nhìn `doi`, còn
  t82 phán CẢ cây. Điều kiện tiên quyết HIỆN KHÔNG có trên master (`git ls-files -s` toàn kho: 0 mục 120000) ⇒ P3.
- Quan sát (không finding): `kiem_yaml`/`kiem_lease` chạy TRƯỚC khi `kiem_loai_tep` phán và đi theo symlink (`is_file()`/`open`) — kết luận vẫn
  DO nên fail-close; tác giả PR vốn điều khiển ci.yml (giới hạn đã khai). Không soạn payload thoát cây để đo.
- gitlink cập nhật: `lease_publish_test` đầy đủ hai vế nen/dot(gitlink `ops/land/zz-sub`) ⇒ `187/187` · `187/187` (shellcheck có mặt) ⇒ delta 0.

## H4 — ĐỐI CHIẾU LƯỢT TRƯỚC
| Lớp (lượt) | Trạng thái trên 57b6578 | Bằng chứng |
|---|---|---|
| `buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca` F1 P2 (lượt 7 Opus) — symlink treo | **ĐÃ VÁ cho đường vào trong `doi`** (thêm, đổi kiểu, đổi đích, thư mục, hợp lệ/treo — H1). **VÁ HẸP**: đường vào thứ hai (symlink có sẵn bị PR hồ sơ xoá đích) còn mở ⇒ F-A dưới | out/h1-fixture.log · out/h2-xoa-dich.log |
| `kiem-re-cua-fail-close-chua-co-ca` P2 (lượt 7 cả hai) | **ĐÃ VÁ THẬT** cho 9+1 cửa đã chỉ (t20h–t20m, t20o; mutant nằm trong 168, bị giết). **Tái xuất ở cửa MỚI**: chính `kiem_loai_tep` mới thêm có fixture MỘT hình dạng ⇒ F-B dưới | out/h3-mut-b.log |
| `diff-check-tu-ha-nguong` P3 (g3) | **ĐÃ VÁ THẬT**: t20d có fixture + chốt "fixture vô hiệu" cho TỪNG loại; ba mutant bỏ từng loại bị giết | suite 168/168 |
| `bang-do-thieu-neo-va-thieu-kiem-ke` P3 (g3) — dòng `TU KIEM PHAN HANG:` | **ĐÃ VÁ THẬT**: t93 đòi dòng đúng + TẬP 5 dòng tổng kết; `test_main_tu_kiem_in_so_sai`/`_luon_in_dat` bị giết | suite |
| `kiem-re-bo-sot-duong-vao` P3 (g3) | **ĐÃ VÁ** ở mức helper (t20h/t20i); ở mức `kiem-re` vẫn KHÔNG ca nào đi qua tệp hồ sơ bị XOÁ (mutant N4 sống) ⇒ gộp vào F-B | out/h3-mut-b.log |
| `kiem-re-phu-thuoc-actor-su-kien` P3 | ĐÓNG theo quyết định chủ kho: docstring D2 đã khai hệ quả (không báo lại) | diff docstring |

## FINDINGS
### F-A · `buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca` (đường vào thứ hai) [P3] — PR hồ sơ xoá ĐÍCH của symlink có sẵn: kiem-re DAT, t82 ĐỎ trên master
- Vị trí: `ops/ci_duong_nhanh.py` `kiem_loai_tep` chỉ lặp trên `doi`.
- Phản chứng: H2 ở trên (`tmp/xd.sh`, hai vế một lệnh): `dot kiem-re rc=0 … DAT (1 tep doi, 0 loi)` / `dot t82 rc=1 shutil.Error … zz-l.md … No such file`; `nen t82 rc=0`.
- Gốc lớp: bước bù phán theo DIFF, bước bị bỏ phán theo CÂY — đúng nợ `buoc-bi-bo-doc-ca-cay` lượt 7 khai; bản vá đóng đường được chỉ, bỏ sót
  đường thứ hai (hình dạng "VÁ ĐÚNG CHỖ ĐƯỢC CHỈ RỒI BỎ SÓT ĐƯỜNG THỨ BA" của CLAUDE.md). Đường đầy đủ vẫn cho symlink HỢP LỆ vào hồ sơ, nên tiền đề
  đạt được bằng một PR hợp lệ. P3 vì HIỆN master có 0 symlink (tiền đề chưa có) và hậu quả là master đỏ nhìn thấy, không có mã lọt.
- Hint: `_symlink_treo_trong_ho_so(kho)` — `os.walk(followlinks=False, onerror=nem)` dưới 4 tiền tố, trả symlink TREO; `kiem_loai_tep` cộng lỗi cho
  symlink treo NGOÀI `doi`; `OSError` ⇒ `KHONG DO DUOC`. Ca `t20r` (có đối chứng symlink hợp lệ có sẵn + PR không đụng đích ⇒ DAT), `t20s` (quét ném ⇒ DO).
  Đã kiểm hint không chặn oan: F (symlink→thường), G (xoá symlink), I (tệp thường) đều DAT; phản chứng xd ⇒ `DO … co san bi TREO … 'ops/reviews/zz-l.md'`.

### F-B · `kiem-re-cua-fail-close-chua-co-ca` (tái xuất ở cửa mới `kiem_loai_tep`) [P3] — sáu đột biến thu hẹp chốt symlink SỐNG, TONG DAT
- Vị trí: `ops/ci_duong_nhanh_test.py` `t20n` (một hình dạng: treo, `.md`, `ops/specs/`, thêm mới); không ca kiem-re nào có tệp hồ sơ bị xoá.
- Phản chứng: H3 lượt b — N1 chỉ-chặn-treo, N3 chỉ-`.md`, N4 chặn-oan-tệp-xoá, N5 chỉ-`ops/specs`, N7 bỏ-symlink-thư-mục, N8 bỏ-`ops/leases`:
  mỗi cái `CA: 71/71 · DOT BIEN: 168/168 · TONG: DAT`, rc=0. (Lượt a cho `TONG: DO` chỉ nhờ HONG neo — tín dụng giả, đã loại.)
- Gốc lớp: fixture của cửa mới liệt kê theo ca reviewer chỉ, không liệt kê hết hình dạng đầu vào. HEAD đúng ở cả sáu hình dạng (H1) ⇒ lỗ RĂNG, P3.
- Hint: `t20p` (5 hình dạng trong một PR: hợp lệ · thư mục · `.yaml` · `ops/leases` · đổi kiểu; đòi dòng lỗi riêng cho TỪNG đường dẫn) + `t20q`
  (xoá hai tệp hồ sơ ⇒ DAT); 5 mutant chính thức giữ nguyên neo `LOAI_TEP_NEO` (không phá neo mutant cũ).

## ĐO HINT (out/HINT.patch, sha256 37f4cc94…5092)
- `git apply --check` trên clone sạch 57b6578 ⇒ OK; áp rồi chạy ⇒ `CA: 75/75 · DOT BIEN: 176/176 bi giet dung ly do · TONG: DAT`
  (`KIEM KE … ops/ci_duong_nhanh.py=67 … = 176`). `ruff --select F` hai tệp: sạch. `actionlint ci.yml` rc=0. `ci_dang_ky_test` 938/938 ĐẠT.
- Chỉ đổi `ops/ci_duong_nhanh.py` + `ops/ci_duong_nhanh_test.py` (trong write set). Nhánh chmod của `t20s` tự bỏ khi chạy root (ở đây là root);
  nhánh mock của nó vẫn đo và mutant `loai_tep_quet_nem_cho_qua` bị giết.

## KHÔNG ĐO ĐƯỢC
- Hành vi trên Actions thật (checkout merge ref, runner) — chỉ đo cục bộ.
- `tl selftest` / `release-bundle` hai vế cho gitlink; `packet_loop_test`/`tl selftest`/`release-bundle` cho tên non-UTF-8 (chỉ đo t82, lease_publish_test, golden, determinism,
  release-check, workflow-audit, doc-claims, eol-survey).
- Nhánh `os.walk` lỗi quyền thật (container chạy root).
- Symlink vòng về tổ tiên / thoát cây: không soạn payload (theo chỉ thị) — mô tả: chốt trong `doi` đã chặn mọi 120000, quét cây chỉ bắt TREO.

## Quan sát khác (không finding)
- `.gitattributes` dưới hồ sơ đã có thật (3 tệp dưới `ops/reviews/**`); đường đầy đủ KHÔNG có bước `git diff --check` nào, nên `kiem_diff_check`
  của đường nhanh là kiểm THÊM — thuộc tính `whitespace`/`conflict-marker-size` do PR mang theo không tạo delta so với đường đầy đủ.
- `packet_loop_test` hai vế gitlink (đo xong sau khi chốt): nen rc=0 TỔNG ĐẠT · dot rc=0 TỔNG ĐẠT ⇒ delta 0 (out/h2-gitlink-b.log).

## KẾT LUẬN
`changes_requested` — P0=0 P1=0 P2=0 **P3=2** (F-A `buoc-bi-bo-doc-ca-cay-khong-chi-ba-ca` đường vào thứ hai; F-B `kiem-re-cua-fail-close-chua-co-ca`
tái xuất ở cửa `kiem_loai_tep`). Số đo executor khai (71/71, 168/168, 23/23, 938/938, actionlint rc=0) tái hiện đúng. Bản vá symlink ĐÚNG và
không chặn oan ở mọi hình dạng đo được; ba lớp lượt 7 khác đã vá thật. advisory_review: Claude review mã Claude viết.
TONG: P0=0 P1=0 P2=0 P3=2
