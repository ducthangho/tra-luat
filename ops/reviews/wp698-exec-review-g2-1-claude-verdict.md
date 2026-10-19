verdict: approve
reviewed_sha: 3b3d64422adb9a6200071244bfe2a14e42d0dd4a
spec_sha256: ed027f410aac7eeedd60335459ba8cfef521a34730fea68c1255533bb56f1a21
reviewer_provider: anthropic
reviewer_model: claude-sonnet-5-5 (subagent review-sonnet-max, tự khai)
execution_surface: claude_code_subagent
che_do: subagent_trong_phien_dieu_phoi

# Review thi hành wp698 `CI-G5-CONG-CU-VA-TIEP` r14 — lượt thi hành 1 của g2

**KẾT LUẬN: `approve` — 0 P1 · 0 P2 · 0 P3 = 0 lớp mở. `goi/HINT.patch` rỗng** (sha256 `e3b0c442…b855`).

Reviewer tự khai: Claude Sonnet 5.5 (`claude-sonnet-5-5`), chạy bằng subagent trong phiên điều phối, **KHÔNG phải codex**; effort "max"
theo chỉ thị điều phối — effort và model thực đã phục vụ là **KHÔNG ĐO ĐƯỢC** từ bên trong phiên. Làm đúng `PROMPT.md` với ba khác biệt
do điều phối nêu: không sửa `cay-kho/` tại chỗ (chỉ đọc; mọi đo trên bản sao `git clone --shared` / `git archive` / `cp -al` trong
`mktemp -d -p $R`), không dùng mạng và không đăng GitHub, không commit/push. Phiên đo 2026-10-10 06:25Z–08:55Z, container 4 lõi
(`nproc` = 4), Python 3.12.3 (+ 3.11.15, 3.13.12), PyYAML 6.0.3, jsonschema 4.26.0, ruff 0.15.15, git 2.43.0.
Ba trạng thái: **có · không · KHÔNG ĐO ĐƯỢC**. Số liệu thô và script của tôi nằm ở `goi/so-lieu/` (liệt kê ở §8).

`approve` ở đây chỉ nói: bản thi hành g2 đạt chữ r14 tới đúng phạm vi tôi đo được (§1–§3), và không có lỗi đo được nào phải vá. Nó **không**
thay A6 (cổng thẩm quyền: chủ kho `human_audited`), không thay duyệt lượt CI 2 (S10), không thay phép đo trên runner thật (§7).

---

## 0. Đầu vào đã kiểm (lệnh + output thật)

```
$ sha256sum SPEC.md lease.yaml
ed027f410aac7eeedd60335459ba8cfef521a34730fea68c1255533bb56f1a21  SPEC.md
a8c9cd161db29d3f4cca0153978d6e2738b30c96f6fa7d62e2b251c684ce79af  lease.yaml
$ git -C cay-kho rev-parse HEAD HEAD:ops/cong_cu_test.py
3b3d64422adb9a6200071244bfe2a14e42d0dd4a
ba9099e3046607464d548278bfb8be74587fec44
$ git -C cay-kho status --short --untracked-files=all | wc -l   ->  0   (trước, giữa và sau mọi phép đo; HEAD vẫn 3b3d644)
$ git -C cay-kho show d17ec09:ops/specs/ci-g5-cong-cu-va-tiep-r14.md | sha256sum  ->  ed027f41…1a21   (blob b427f19d…, = spec_blob của lease)
$ git -C cay-kho show 5caad65:ops/leases/wp698-r14-g2-claude.yaml | sha256sum     ->  a8c9cd16…79af
$ printf '%s\n' ops/cong_cu_test.py .github/workflows/ci.yml ops/ci_duong_nhanh_test.py | LC_ALL=C sort | sha256sum
669f5137356f30c78cf329f6946a0d129061b23953d4d29302aceaf27cb511cb   (= write_set_hash của lease)
```
Khớp mọi mốc của PROMPT ⇒ không `blocked`. 14 phụ lục của đặc tả được trích bằng script riêng (`script/trich_pl.py`), **14/14** băm khớp tiêu đề; bản
ghép `do_dot_bien_r3…r6` khớp `37b6e8bd…`, `bec92f6e…`, `acb8d897…`, `5d1a4ada…` (đúng băm đặc tả khai).

## 1. Đối tượng review: diff g1 (`19a2d96`) → g2 (`3b3d644`)

`git diff --numstat 19a2d96 3b3d644` = `1 1 .github/workflows/ci.yml` · `1 1 ops/ci_duong_nhanh_test.py` · `15 3 ops/cong_cu_test.py`;
`git diff --summary` rỗng (không đổi mode/tạo/xoá), `git diff --check` rc=0, 0 ký tự CR hay điều khiển trong dòng thêm. Năm hunk (`-U3`) của `ops/cong_cu_test.py`, ở bốn chỗ:

| đầu hunk (dòng g1) | chỗ | thay đổi |
|---|---|---|
| 8027 | `_in_tu_kiem_main` | khai `phat_nho = {}` (nhớ đệm trong tiến trình con) |
| 8040 + 8050 | `phong` (đồ giả của `_phong_con`) | khoá `(tuple(ten), kb.get("con"))`; trúng ⇒ gán lại `phat["gt"]`, `phat["ly"]` và trả **bản sao** `list(n)`; thân cũ dời vào `phong_dung(ten)` (`phat` cục bộ), trả `(gt, kq_con, ly)` |
| 8349 | `_in_tu_kiem_che_do`, quét `head` | thay `Path.read_bytes` bằng lambda trả bytes của `TEP_TEST` đọc một lần |
| 8380 | `finally` của quét `head` | khôi phục `g["TEP_TEST"], Path.read_bytes = cu[1], cu_rb` |

Không chạm thân `_doc_che_do`, `_van_tay`, `main`, `_so_tien_trinh_ban_kinh`, `_ket_luan_ban_kinh`, `_chay_1_ca`, không chạm `_d698`, `_luoi_*`, `_RA698`, `_R698`, `_N698`, `DOT_BIEN`.

## 2. Bảng đối chiếu tiêu chí (chữ r14)

### M1–M8

| mục | trạng thái | bằng chứng đo |
|---|---|---|
| M1, M1b, M2, M2b, M3, M5, M5b, M6 (đã đóng ở g1) | **giữ nguyên ở g2** | diff g1→g2 không chạm miền/ô nào (§1; Phụ lục G: `cham: []`, 22 hunk, rc=0); `kq["m1"]` = `[673234, 122268, [], 0]` ở 3.12 (g1 = g2); `luoi` 212 · `luoi_git` 60 · `m3698-` 162 · `noi698-` 122 · `ghi698` 456 · `E698` 121 (g1 = g2); mẫu 199 dò (§3.1) đúng hạng |
| M4 (chú thích neo) | có, theo khối | A7 dưới |
| **M7a** | **có** | `.github/workflows/ci.yml:505` `    timeout-minutes: 30` → `45`; diff vs `4beb9d0` đúng `1 1`; dòng nằm giữa `497:  gate-cong-cu:` và `555:  gate-cong-cu-gop:`; so YAML bằng `yaml.safe_load`: chỉ `jobs.gate-cong-cu.timeout-minutes` đổi (30 → 45, kiểu int), phần còn lại của job, mọi job khác và phần ngoài `jobs` giống hệt |
| **M7b** | **có** | `ops/ci_duong_nhanh_test.py:2196` (`KHUNG_JOB['gate-cong-cu']`): `x.replace("'timeout-minutes': 30","'timeout-minutes': 45") == y`, và dòng duy nhất khác trong 3609 dòng; bắt đầu bằng `    'gate-cong-cu': {` |
| **M8 "Được"** | **có** | §3.2 (không thu hẹp miền, không bỏ ô, không làm yếu canh; đột biến bản vá §4; đạt đích A10 (i) 0,7125) |

### A1–A10 (A6 = cổng thẩm quyền, bỏ)

| tiêu chí | kết quả | bằng chứng (lệnh/số) |
|---|---|---|
| A1 (i)–(iii), A2, A3, A8 | **có** trên mẫu | 199 dò (47,5 % của 419; mọi họ, đủ KHAI/NGOÀI/T-D/T-E) hạng = kỳ vọng của §6, 0 lệch; §3.1 |
| A1 (iv) | **có** | lệnh nguyên văn trên `ops/cong_cu_test.py` của nền, g1, g2 → cả ba in `0 0 ['0x2026']` |
| A1 (v) | **có, đủ 27/27** | 27 dò xoá-cả-nhóm (`x-nhom` 18 + `x3-nhom` 9) chạy đủ trên g2: **26 GIẾT + 1 KHÁC** (`x3_cat_ll_bk`, đối chứng KHÁC đã khai, bán kính 2) |
| A1-b2 (bậc hai) | **một phần đo trực tiếp** | gỡ nhóm `cf` khỏi `D698` ở con **và** công thức `trong` của cha trên g2 (base 56/56): ba canh r1 của Cf `w698_e49_cf_{bk,mh,head}` → SỐNG, hai canh r1 của phép khác `w698_e49_nfkc_bk`, `w698_x46_tab_bk` → GIẾT `t53_` — đúng điều A1-b2 (1) khai. Các nhóm còn lại và A2/A3/A8 bậc hai: **không chạy lại** (§5 N6, §7) |
| A4 (a) | **có** | `CONG_CU_TEST_BAN_KINH=manh`: g2 3.12 `56/56`, rc=0, 266 s; nền 3.12 `56/56`, 221 s; g2 3.11 `56/56`, 270 s; g2 3.13 `56/56`, 257 s; cả bốn `SỐ LIỆU: … lỗi đột biến=0 … cổng cây thật=ĐẠT`, 0 dòng `ĐỎ`, 0 `BỎ QUA` |
| A4 (b) | **có** | `ruff check --select F --no-cache` 0.15.15: nền, g1, g2 cùng đúng một lỗi `F841 Local variable ci is assigned to but never used` (:2606 / :2662 / :2662) ⇒ delta đa tập ∅; `ops/ci_duong_nhanh_test.py`: `All checks passed!` cả `4beb9d0` lẫn g2 |
| A4 (c) | **có** | bảng §3.3 |
| A4 (d) Phụ lục G | **có** | `{"hunk": 22, "cham": []}` rc=0 |
| A4 (e) Phụ lục E | **có** | `sau_moc: []`, `tong: 9` (nền = g1 = g2) |
| A4 (f) | **có** | `git diff --name-only 4beb9d0 3b3d644` = đúng ba tệp; numstat `1 1` và `1 1`; `git status --short --untracked-files=all` của cả cay-kho lẫn ba clone (nền, g1, g2) sau mọi lượt chạy: 0 dòng |
| A4 (g) = A10 (iii) | **có** | `ty_le` g2 = 1,2623 và 1,2734 ≤ 1,35; đếm lời gọi lớn nền/g2 = 64/67 ≤ 128 |
| A5 | **có một phần đo trực tiếp** | Phụ lục F với bảng nối do tôi **dựng lại từ chính `DOT_BIEN`** (54 dòng, trùng bảng executor sau `sort`): `{"nen":416,"ung_vien":470,"them":54,"bang_noi":54,"dem_neo":{"muc":470,"lech":0},"so_loi":0}` rc=0. Hai mảnh A9 (1, 3) trên g2: `MẢNH k/8: 59/59 đột biến bán kính 1`, đọc lại từng bản ghi: 59/59 mỗi mảnh `giet_that` đúng ca đích, không `tin_dung_gia`, bán kính 1. Thêm 191 mục `DOT_BIEN` đích `t53_`/`t54_`: **191/191 GIẾT**. Hợp 259/470 mục, gồm 52/54 canh `w698_` (hai canh còn lại đích `t52_`, cửa `gom` không đổi). 6 mảnh còn lại: **KHÔNG ĐO ĐƯỢC** bởi tôi (chỉ có lời khai executor 8/8) |
| A7 | **có** | grep nguyên văn trên dòng thêm của g2: 0 dòng khớp; chú thích `#698 M8` ở đầu hai khối thêm (§5 N3) |
| **A9** | **có** | bảng §3.4 — R9 1,4671, dự báo 29,59 ≤ 33,75 |
| **A10 (i)** | **có** | Δ_g1 = min(8,94; 9,14) = 8,94 s; Δ_g2 = min(6,43; 6,37) = 6,37 s; **0,7125 ≤ 0,85** (§3.2) |
| A10 (ii) | **có trên mẫu** | 199 dò g2, trong đó 48 dò chạy cả g1: 0 đổi hạng |
| A10 (iii) | **có** | như A4 (g) |
| A10 (iv), (v), (r13), (r14) | **có ở 3.11/3.12/3.13** | bảng §3.4 |

### S1–S11

| điều kiện dừng | trạng thái |
|---|---|
| S1 | không kích hoạt: ba tệp, hai tệp phụ đúng `1 1`, không đổi thân sáu hàm |
| S2, S3 | **KHÔNG ĐO ĐƯỢC** (cần GitHub/ máy chủ). Đo được cục bộ: băm đặc tả + lease khớp đối tượng git; hạn lease 2026-10-10T20:20Z chưa tới (phiên đo kết thúc 08:55Z). Bộ đệm `origin/master` của `cay-kho` = `ab457c6` (cũ, đúng như đặc tả cảnh báo) nên không dùng được cho S3 |
| S4 | không kích hoạt: 0 canh/dò chết bằng `tin_dung_gia` hay bán kính > 1 trong phần đã đo |
| S5 | không: 247 (`numstat fc852ff -- ops/cong_cu_test.py`) + 1 + 1 = **249 ≤ 300**; 3 tệp ≤ 3 |
| S6, S7a, S7b | không áp dụng ở lượt review này (không CI, không vòng vá) |
| S8 | không: lease còn hạn |
| S9 | không có phát hiện ngoài đặc tả |
| S10 | **KHÔNG ĐO ĐƯỢC** phía GitHub; trong `cay-kho` remote `origin` là bản sao cục bộ `…/wt-698-exec`, không có thao tác đẩy; thông điệp commit ghi "KHONG day" |
| S11 | không kích hoạt: A9 và A10 đạt mà không phạm điều cấm nào của §5 M8 (§3.2) |

## 3. Các việc của PROMPT

### 3.1 Spec acceptance — những gì tôi chạy lại, một mục một lệnh

**Mẫu 419 dò (A1–A3, A8, A10 (ii))** — chạy **g2 và g1 trong cùng một script worker** (`script/probes_w.sh`: g2 rồi g1 trên mỗi lát; `do_dot_bien_r6.py` nguyên bản ghép, `_do_ban_kinh` + `_ket_luan_ban_kinh` của chính cây, hạng theo hàm `hang`/`tap` của Phụ lục D nạp bằng `exec`, không chép).
Chọn mẫu có lý do (`probes/mau_lydo.json`): 5 KHAI; 11 ngoài lớp; 3 KHÁC (`s_ra_realpath`, `x3_wr_ra_lower`, `x3_cat_ll_bk`); 3 tương đương (`m_nfkc_no_bk`,
`m_nfkc_khac_bmp_mh`, `x3_wr5_normpath`); 8 đối chứng GIẾT-trên-nền (`x3_main_ra_lower`, `x3_main_ra_nfd`, `m_cc_mh`, `x3_cat_cc_bk`, `x3_cat_zs_bk`, `x_head_cfk_lead_only`,
`x_head_cfk_trail_only`, `x_head_nfkc_fwletters`) và `x_f50_h_ge2`, `x_f50_tk_ge2`, `z_exc_oserror_only`, `z_exc_subproc_only`; **toàn bộ T-E (30)** vì M5b nằm trong cửa sổ vá VB;
**toàn bộ T-D (16) và mọi họ đích `t54`** (`x-main-ra`, `x3-main-ra`, `x3-m3a`, `x3-m3b`, `luc-luong`) vì đó là chỗ nhớ đệm VD; họ `x3-head`, `x-head`, `x-head-pos` và 10 dò `head` nữa
vì đó là chỗ cửa sổ vá VB; **toàn bộ 27 dò xoá-cả-nhóm** (A1 (v)); cộng mẫu phân tầng (seed 698) cho mọi họ còn lại.
```
$ python agg_probes.py        (đọc g2_{A,B,C}.jsonl, g1_{A,B}.jsonl, nen_{g1,g2}.jsonl)
so_do_g2 199 | so_do_g1 48 | hang_g2 {"SONG":19,"KHAC":3,"GIET":177} | hang_g1 {"SONG":19,"KHAC":3,"GIET":26}
theo_tap_g2 {"KHAI":{"SONG":5},"NGOAI":{"SONG":11},"T-B":{"GIET":95,"SONG":2,"KHAC":1},"T-C":{"KHAC":2,"GIET":36,"SONG":1},"T-D":{"GIET":16},"T-E":{"GIET":30}}
lech_so_voi_mong_g2 {} | lech_g1_g2 {} | lech_so_voi_mong_g1 {} | so_neo {"1":199} | chua_do_g2 [] | loi_dung []
nen_g1/nen_g2: khong_qua {}, so_ca 56, so_dot_bien 470 (56 ca đều qua ở nền của chính hai cây)
```
Ý nghĩa: 19/19 dò SỐNG khai (11 + 5 + 3 tương đương), 3/3 KHÁC, 177 GIẾT — **đúng từng tên** với bảng 397/19/3 của §6; trên 48 dò chạy cả hai cây: g1 = g2 từng dò.
Độ phủ: g2 199/419 (47,5 %); tôi không khẳng định phần 220 dò còn lại — đó là lời khai executor (419/419, 0 đổi hạng), **KHÔNG ĐO ĐƯỢC** bởi tôi.

**A10 (iv)(v) + so khoá nghiêm, 3 phiên bản** — script **tôi viết độc lập** từ chữ "Cách tính, chốt" (`script/a10v.py`), hai cây `git archive` không `.git`/`__pycache__`
(`a10_g2` = `3b3d644`; `a10_g1` = cùng cây, `ops/cong_cu_test.py` thay bằng blob `9c628700…`), `-B`, `PYTHONDONTWRITEBYTECODE=1`, bỏ mọi biến `CONG_CU_TEST_*`, 6 lệnh rc=0 mỗi phiên bản:

| | 3.11.15 (Unicode 14.0.0) | 3.12.3 (15.0.0) | 3.13.12 (15.1.0) |
|---|---|---|---|
| `kq["m1"]` g1 = g2 | `[666094, 121008, [], 0]` | `[673234, 122268, [], 0]` | `[673404, 122298, [], 0]` |
| `len(luoi)` · `len(luoi_git)` · `m3698-` · `noi698-` · `ghi698[0]` (g1 = g2) | 212 · 60 · 162 · 122 · 452 | 212 · 60 · 162 · 122 · 456 | 212 · 60 · 162 · 122 · 457 |
| `ghi698[1:]` | `[[], 0]` | `[[], 0]` | `[[], 0]` |
| khoá `E698` g1 / g2 (g2 ⊇ g1) | 119 / 119 | 121 / 121 | 124 / 124 |
| khoá đỉnh `KQ` che-do · main · gom (g2 ⊇ g1) | 32 · 508 · 72 | 32 · 508 · 72 | 32 · 508 · 72 |
| (r14) đường list/dict thiếu, đổi loại, ngắn hơn | 0 · 0 · 0 | 0 · 0 · 0 | 0 · 0 · 0 |
| `XANH` | true | true | true |

Số đường chứa list/dict của `KQ` g1 (trừ `m5b[0]`): **409 · 1512 · 210** — đúng số đặc tả khai, nên phép đếm của tôi trùng định nghĩa.
**Răng của script tôi** (một phép kiểm không thể đỏ thì không là bằng chứng): cây `P1a` (g2 với `for n in range(2, 17) for k in range(n)` → `for n in (2, 16) for k in (0, n - 1)` ở `_luoi_noi_main`) cho `kq["m1"]`
và mọi số ghim BẰNG vẫn xanh nhưng khoá đỉnh main 508 → 377, (r14) 132 lỗi ⇒ `XANH false`, rc=1; thử đơn vị `so_hinh_dang` trên `KQ` giả: list → chuỗi ⇒ `DOI_LOAI` đúng một đường; đổi loại theo chỉ số ⇒ đỏ; thêm ô giả ở cuối ⇒ không bắt (đúng giới hạn "Wpad" đặc tả đã khai).
**Đối chiếu giá trị `KQ` g1 ↔ g2** (3.12): `--tu-kiem-main` **0 chênh lệch** trên 508 khoá (503 kịch bản + 5 khoá giàn; mỗi kịch bản là rc, nhật ký, stdout); `--tu-kiem-che-do` 4 chênh lệch, đều là đường dẫn hay băm của chính tệp test
(`byte.tep`, `byte.thuc`, `goi_git[0][0][2]`, `goi_git[1]`); `--tu-kiem-gom` 5 chênh lệch, đều là tên thư mục tạm ngẫu nhiên. Hai bản chạy hai tiến trình khác nhau với `PYTHONHASHSEED` ngẫu nhiên ⇒ không phụ thuộc thứ tự băm.

### 3.2 M8 có thật là "Được"?

**Có.** Bốn lớp bằng chứng:

1. *Không thu hẹp miền, không bỏ ô* — §1 (không chạm miền), §3.1 (khoá, độ dài, loại của `KQ` ba cửa con không thiếu, không hẹp; `KQ` main trùng từng byte), Phụ lục F (470 mục, 0 mỏ neo lệch).
2. *Không làm yếu canh/dò* — 191/191 mục `DOT_BIEN` đích `t53_`/`t54_` GIẾT đúng ca đích (`giet_that`, bán kính 1/56, không `tin_dung_gia`; `t53_`: 90, `t54_`: 101, `dbk_g2_t53_t54.jsonl`); hai mảnh A9 trên g2 59/59 mỗi mảnh;
   199 dò mẫu đúng hạng (gồm cả 27 dò xoá-cả-nhóm); A1-b2 (1) cho nhóm `cf`.
3. *Nhớ đệm là bất biến quan sát được, đo thẳng trên lượt thật*: tôi dựng bản "bóng" của g2 mà **mỗi lần trúng nhớ đệm đều tính lại tươi** rồi so với giá trị trong nhớ đệm (cây `a10_shadow`, chạy `--tu-kiem-main`):
   ```
   139 MISS · 148 HIT_BANG · 0 HIT_LECH         (tệp: so-lieu/khac/bong_phong_hit_miss.txt)
   KQ cua ban 'bong' == KQ g2 binh thuong: True | so kich ban: 508
   ```
   (508 là số khoá của `KQ`: 503 kịch bản + 5 khoá giàn.) Tức trong 287 lời gọi `phong`, 148 lần trúng nhớ đệm đều trả đúng cái mà g1 sẽ dựng lại (gt, đầu ra con, ly); bản "bóng" không đổi `KQ`.
4. *Về "mutant chỉ lộ khi mỗi lần gọi phải tạo mới"*: nhớ đệm sống trong MỘT tiến trình con, khoá bằng mọi đầu vào thay đổi giữa các kịch bản (`ten`, `kb["con"]`); hai đầu vào còn lại của `phong_dung` — tên ca (`CA`, qua `_cac_ca_da_chay`) và `DOT_BIEN` — bất biến trong cửa này
   (`ten_ca` chốt từ đầu, `CA[:]` dựng lại cùng tên mỗi kịch bản); không mục nào trong 419 dò hay 470 mục `DOT_BIEN` sửa tại chỗ rồi đọc lại một đối tượng mà `main` đã nhận (đã kiểm bằng regex trên anchor/phép thay của 419 dò và của `DOT_BIEN` đích `ops/cong_cu_test.py`, rồi đọc từng mục: 10 dò + 26 mục nhắc `ket`/`nhom`/`_phong_con`; không mục nào sửa tại chỗ `nhom` hay danh sách `_phong_con` trả về).
   Phản chứng thực nghiệm ở §4.

Phụ lục I **trên máy này** (một script `script/pli.sh`, bốn lượt xen kẽ `(nền,g1)`, `(nền,g2)`, `(nền,g1)`, `(nền,g2)`, venv hai gói ghim; `loi_khac_dung` 0,05–0,12 lõi; `loadavg` đầu lượt trong JSON 0,14–1,05):

| lượt | `delta_cpu` | C56 | `ty_le` | rc | lời gọi lớn nền/ứng viên |
|---|---|---|---|---|---|
| g1 #1 | 8,94 s | 23,64 | 1,3782 | 1 (`cpu` > 1,35, như đặc tả dự báo) | 64 / 67 |
| g2 #1 | 6,43 s | 24,51 | 1,2623 | 0 | 64 / 67 |
| g1 #2 | 9,14 s | 22,71 | 1,4025 | 1 | 64 / 67 |
| g2 #2 | 6,37 s | 23,30 | 1,2734 | 0 | 64 / 67 |

**Δ_g1 = 8,94 s; Δ_g2 = 6,37 s; tỷ số min/min = 0,7125 ≤ 0,85** (cặp-theo-cặp 0,7192 và 0,6969; trung bình 0,708). Executor khai 0,733 (8,80/9,04 so 6,45/6,73) — cùng kết luận, khác máy. Phân rã CPU ba cửa con (script `cpu_cua_rv.py`, min ba vòng xen kẽ, 3.12):
`che-do` nền 0,49 → g1 5,38 → g2 3,73 · `main` 1,95 → 3,54 → 2,80 · `gom` 5,04 → 6,36 → 6,53 · tổng chênh g1 7,80, g2 5,58, tỷ số 0,715. Đúng chỗ M8 sửa (che-do −1,65, main −0,74), `gom` không đổi.

### 3.3 M7 và A4 (c)

Liệt kê mọi chỗ ghim/suy: `git grep -n -E 'timeout-minutes' HEAD -- '*.py' '*.yml' '*.yaml' '*.sh' ':!ops/specs'` = **76 dòng** ở cả `4beb9d0` lẫn g2 (số đặc tả khai); lọc dòng mang số 30:
`4beb9d0` có 6 (`ci.yml:505`, `ci_duong_nhanh_test.py:2196`, và bốn dòng khác), g2 còn **4** — `.claude/dev/ci_dang_ky_test.py:888` và `:2096` (job `dot-bien-manh`), `.github/workflows/ci-dot-bien-du.yml:68`, `ops/ci_duong_nhanh_test.py:2430` (cận trên của job `chuan-bi`) —
bốn dòng thuộc job khác. `rg --hidden` (ripgrep 14.1.0, bỏ `.git`/`ops/specs`) cho đúng cùng bốn dòng. Suy: `1800`/`30*60`/`60*30` trong mã (không tính hồ sơ) không có ca nào liên quan `gate-cong-cu`; `docs/`, `CHANGELOG.md`, `CLAUDE.md`, `AGENTS.md` không nhắc `gate-cong-cu`.
Không tệp nào khác ghim băm blob của `ci.yml` (`1d3c63ff`/`2e3095bb`). `actionlint 1.7.7` (có `shellcheck`) trên `ci.yml`: `4beb9d0` rc=0, g2 rc=0, đầu ra trùng (delta 0). `release-verify --strict --json`: `ok true`, `expected_file_count 180 = checked_file_count 180`, `failed 0`, `package_hash_match true`.

| lệnh (3.12, cùng tập lệnh, hai cây chạy song song) | `4beb9d0` | g2 | chỉ M7a (`ci.yml` 45, khung 30) | chỉ M7b (`ci.yml` 30, khung 45) |
|---|---|---|---|---|
| `.claude/dev/ci_dang_ky_test.py` | `PHẢN CHỨNG: 1025/1025`, `TỔNG: ĐẠT`, rc=0 | y hệt, đầu ra **trùng từng byte** (`cmp` rc=0) | y hệt (trùng từng byte) | y hệt (trùng từng byte) |
| `ops/ci_duong_nhanh_test.py` | `CA: 104/104`, `DOT BIEN: 383/383`, `TONG: DAT`, rc=0 | `CA: 104/104`, `DOT BIEN: 383/383`, `TONG: DAT`, rc=0 | `[DO] y13_khoa_topology_cua_ci_yml_ngoai_than_run: gate-cong-cu: … khac ['timeout-minutes']`, `CA: 103/104`, `DOT BIEN: 361/383`, **`TONG: DO`, rc=1** | y hệt cột trái: **`TONG: DO`, rc=1** |

⇒ `ci_duong_nhanh_test` đỏ đúng khi chỉ sửa MỘT trong hai chỗ, theo cả hai chiều.

### 3.4 A9 và A10 (i) — bảng số

**A9** — `taskset -c 0,1 python -B manh_a9_r12.py <nền clone> <g2 clone> <ra tuyệt đối ngoài cây> 45 1 3` (Phụ lục M nguyên bản `2fe67a92…`), rc=0, `loi: []`:

| lượt | giây tường | CPU con | dòng cuối |
|---|---|---|---|
| nền, mảnh 1 | 815,9 | 1250,1 | `MẢNH 1/8: 52/52 đột biến bán kính 1` |
| g2, mảnh 1 | 1197,0 | 1890,4 | `MẢNH 1/8: 59/59 đột biến bán kính 1` |
| nền, mảnh 3 | 825,3 | 1274,6 | `MẢNH 3/8: 52/52 …` |
| g2, mảnh 3 | 1174,3 | 1883,4 | `MẢNH 3/8: 59/59 …` |

Mọi lượt kèm `cong_cu_test: 56/56 đạt; tổng=56, bỏ qua=0, tiền kiểm bỏ qua=0`. `ty_le_theo_manh` {1: 1,4671; 3: 1,4229}; **R9 = 1,4671; dự báo = 1,4671 × 20,17 = 29,59 phút ≤ 0,75 × 45 = 33,75 ⇒ ĐẠT**.
`blob_nen` = `9edea6b1629b46f27758b2073e74210dc73495b7`; `blob_ung_vien` = `ba9099e3046607464d548278bfb8be74587fec44` = `git rev-parse 3b3d644:ops/cong_cu_test.py` (vế mà script không tự kiểm; tôi đã kiểm: bằng nhau).
Chỉ báo: `loi_khac_dung` **1,7** lõi, `loadavg` 0,65 → 3,41, cửa sổ 4012,5 s — **máy KHÔNG yên**: trong cửa sổ ấy tôi chạy song song suite `manh`, đột biến bản vá, A4 (c), `release-verify` và 191 mục `DOT_BIEN` trên lõi 2–3 (A9 ghim lõi 0–1). R9 trùng giá trị executor đo trên máy yên (1,467), ghi nhận thế; không dựa vào đó để nói gì thêm.
Đây vẫn là ƯỚC, không phải phép đo trên runner (§7).

**A10 (i)/(iii)** — bảng trong §3.2. **A10 (ii)** — §3.1. **A10 (iv)(v)** — §3.1.

### 3.5 Lỗi mới, ngoài write set, phụ thuộc nền, chậm bất thường

- *Lỗi mới*: không đo được lỗi nào của g2 (§2, §3, §4).
- *Ngoài write set*: không (§1; `git status` sạch; `ci.yml` chỉ đổi một giá trị).
- *Phụ thuộc nền*: `compile(..., "exec")` với `-W error` trên 3.11/3.12/3.13 không cảnh báo; suite 56/56 và A10 xanh ở ba phiên bản; `Path.read_bytes` được thay/khôi phục đúng ở cả ba (cũng cách F35 của `--tu-kiem-gom`). **Windows không đo** (Q8, nợ `windows-chua-do-o-moi-wp698`).
- *Chậm bất thường*: suite `manh` 3.12 g2 / nền = 266 s / 221 s (×1,20, cùng cỡ executor 260/212 và g1 267); `delta_giay` Phụ lục I 6,49 s (g2) so 9,08–9,29 s (g1). Không phép đo nào của tôi cho g2 chậm hơn g1, trừ cửa `gom` (mã không đổi) min ba vòng 6,53 so 6,36 s — chênh 0,17 s (2,7 %); ba vòng g2 6,53–6,91, g1 6,36–6,56, executor đo 6,73 so 6,76: mức nhiễu của cửa này, ghi nhận không kết luận.

## 4. Đột biến BẢN VÁ (M8) — `script/pm.py`, trên `3b3d644`, cơ chế `_do_ban_kinh`/`_ket_luan_ban_kinh` của chính cây (anchor đúng 1 lần, `so_neo` = 1)

| # | đột biến của bản vá | hạng | tín hiệu |
|---|---|---|---|
| pm1 | **gỡ khôi phục** `Path.read_bytes` trong `finally` | **GIẾT** `t53_`, bán kính 1/56 | `giet_that`: "`_van_tay` phải băm TRỌN bytes (bảng biên/lớn/non-ASCII/hoa/khoảng trắng + TEP_TEST thật): ['e4c6a9f3…', 'e4c6a9f3…', …]" — `thuc`/`luoi` thành băm của `b"698"` |
| pm1b | "khôi phục" về chính hàm đang vá | **GIẾT** `t53_` 1/56 | cùng thông điệp |
| pm2 | khoá **bỏ `kb["con"]`** | **GIẾT** `t54_` 1/56 | "`main` nối SAI (kịch bản …)": `con_rc` thấy `ghi … dung none` thay vì `None dung-rc3` |
| pm4 | khoá **hằng** | **GIẾT** `t54_` 1/56 | cùng, `con_rc` |
| pm5 | trúng nhớ đệm **không gán lại** `gt` và `ly` | **GIẾT** `t54_` 1/56 | `m3698-0-0-` …: `gt` cũ ⇒ log lệch |
| pm5c | trúng nhớ đệm không gán lại `gt` (còn `ly`) | **GIẾT** `t54_` 1/56 | cùng loại |
| pm3 | khoá **bỏ `tuple(ten)`** (chỉ `kb["con"]`) | **SỐNG** | `t54_` vẫn XANH — xem N1 |
| pm5b | trúng nhớ đệm không gán lại `ly` (còn `gt`) | **SỐNG** | không kịch bản nào lặp khoá có `ly ≠ None` — N1 |
| pm6 | **dùng chung** đối tượng (không `list(n)`) | **SỐNG** | không mục nào sửa tại chỗ phản hồi — N1 |
| pm6b | bản sao **nông** chỉ tầng ngoài | **SỐNG** | idem |
| pm11 | vá trả `b""` thay `b"698"` | **SỐNG** | quét `head` không phụ thuộc bytes (đúng điều chú thích khai), băm đo ở bảng byte dưới |
| g1a | **g1** (không nhớ đệm): `phong` bỏ qua `ten` thật, luôn dựng cho `3/8` | **SỐNG** | tính chất có sẵn của `t54`: phản hồi giả không bị đối chiếu với `ten` |

Cả sáu đột biến làm lệch thứ **t53/t54 thực sự đo** (khôi phục `read_bytes`, khoá thiếu `con`, khoá hằng, hai kiểu không gán lại `gt`) đều bị GIẾT bằng `TinHieuChotCa` đúng tên ca (không phải `tin_dung_gia`), bán kính 1/56.

## 5. Ghi nhận không thành lớp (đo được, nhưng không phải lỗi của g2 theo chữ r14)

**N1 — bốn đột biến bản vá SỐNG (pm3, pm5b, pm6/6b).** Chúng sửa chính các dòng mới của bản tối ưu; không canh/dò nào mất răng vì chúng (mục §3.2 điểm 2–4, 148/148 trúng khớp, KQ main trùng g1 từng byte). Vì sao KHÔNG thành lớp: (a) r14 chỉ đòi "giữ răng", không đòi chốt cho nội tạng của bản tối ưu
(M8 "Giữ răng"); (b) pm3 có tương đương SỐNG ngay trên g1 (`g1a`), tức tính chất "phản hồi giả của `phong` không đối chiếu với `ten`" có từ trước M8 và không do nhớ đệm sinh ra; (c) `pm5b` chia nhánh trúng/trượt mà mã thật của g2 không chia (gán tuple một lần cho cả hai) nên đó là khoảng hở của tập kịch bản, không phải của mã;
(d) pm6 chỉ đáng kể nếu `main` sửa tại chỗ danh sách nhận về, mà không đột biến nào làm thế. Nếu chủ kho muốn canh: một tự kiểm trong `phong` rằng tên nhóm trả về khớp `ten` đã nhận, và một kịch bản lặp khoá có `kb["con"]` lỗi — hướng mô tả, không mã (Q14).

**N2 — chú thích ở `phong` ("kỳ vọng `gt`/`ly` chỉ phụ thuộc (tên, `kb["con"]`)")** nói hẹp hơn mã đọc: `phong_dung` còn đọc `CA` (qua `_cac_ca_da_chay`) và `DOT_BIEN` (qua `_dich_mong`, `_ban_ghi_du_gia`). Đúng cho tập kịch bản hiện có vì hai thứ ấy bất biến trong cửa này; một kịch bản mới đổi tên ca giữa chừng sẽ khiến nhớ đệm trả dữ liệu cũ mà không ca nào đỏ (pm3 cho thấy loại sai lệch ấy lọt). Đo thẳng cho tập hiện có: §3.2 điểm 3 (148/148 trúng khớp).

**N3 — A7, "mọi chỗ thêm có chú thích neo `#698 M8`" (BAO_CAO §2)** chỉ đúng theo khối: hai dòng chú thích `#698 M8` đứng ở đầu khối nhớ đệm và đầu khối cửa sổ vá; 3/5 hunk (khai báo `phat_nho`, `return phat["gt"], …`, dòng `finally`) không mang chữ `#698` trong dòng thêm. Tiền lệ cùng cách đọc: g1 có 19 hunk thêm, 1 hunk không mang `#698`, và đã `approve` 0/0/0.

**N4 — A9 và độ yên của máy** (§3.4): `loi_khac_dung` 1,7. Không kết luận thêm.

**N5 — rò thư mục tạm**: mỗi lượt `_do_ban_kinh` để lại trong `TMPDIR` một thư mục ~1,4 MB (có `a/bash`, bản sao tệp `bash`) không được dọn; thấy cả ở g1 (`g1a`: 1 thư mục cho 1 đột biến) lẫn g2 (862 thư mục sau ~600 lượt), nên không do M8. Tôi dọn bằng `shutil.rmtree` trong các thư mục `mktemp` của tôi.

**N6 — bậc hai A1-b2 (trừ nhóm `cf`)/A2/A3/A8 và 220 dò còn lại** không chạy lại đầy đủ cho g2: mã M1–M5 không đổi, `KQ` ba cửa con trùng/ không hẹp, A10 (iv)(v) xanh, và một mẫu bậc hai (nhóm `cf`) khớp A1-b2 (1). Bảng bậc hai và bảng hạng 419 của g1 **không có trong gói review này** nên tôi không đối chiếu được trực tiếp: **KHÔNG ĐO ĐƯỢC** từ gói, không phải lỗi của g2.

## 6. Cách phân lớp — vì sao 0 lớp

Không lỗi nào của §2–§5 thoả định nghĩa P1 (không land hợp lệ/hồi quy/CI không xanh hợp lệ/mâu thuẫn đặc tả), P2 (tiêu chí không đạt/test không răng/lời khai rộng hơn phép đo) hay P3 (chính xác hoá) ở mức **đo được** trên g2:
mọi tiêu chí tôi chạy lại đều đạt (A4, A5 phần đo, A7, A9, A10, M7); các điểm N1–N6 hoặc có sẵn từ g1, hoặc nằm ngoài chữ r14, hoặc chỉ là KHÔNG ĐO ĐƯỢC từ gói. Tôi không dựng lớp mới từ những thứ đó (`approve` đòi 0/0/0, và một lớp suy diễn là một vòng thi hành thừa).

## 7. KHÔNG ĐO ĐƯỢC / giới hạn

- **Windows** (Q8) và **runner CI thật**: A9 là ước từ máy đo (container 4 lõi, ghim 2 CPU), không phải thời lượng mảnh trên runner; phép đo thật duy nhất là lượt CI 2 (đòi chủ kho duyệt riêng, S10).
- **Máy chủ GitHub**: comment cấp quyền `6091633467` và việc nó neo đúng `lease_id` + `spec_sha256`; S2, S3 (master có đổi write set không); S10 phía GitHub; bản chiếu verdict các lượt trước trên #698 — không dùng mạng, nên không đọc.
- **Tám mảnh A5 trọn vẹn**: tôi đo hai mảnh nguyên (1, 3) + 191 mục `t53_`/`t54_` = 259/470 mục; sáu mảnh còn lại và 211 mục còn lại chỉ có lời khai executor (8/8, 470 `ok`, 0 `ĐỎ`; Phụ lục F của tôi khớp phần đếm neo).
- **Tập 419 dò**: mẫu 199 (47,5 %), trong đó 48 chạy cả g1; 220 dò còn lại là lời khai executor.
- **Hai cây răng của reviewer lượt 13** (`W1c`, `Gb`) và bảng bậc hai/ bảng hạng 419 của g1, VERDICT r14 (dòng 84, 113 mà BAO_CAO trích cho `hint_provenance`) không có trong gói: không đối chiếu được. Răng của script A10 tôi chứng minh bằng cây `P1a` + thử đơn vị (§3.1), không bằng `W1c`/`Gb`.
- **Danh tính người ký comment cấp quyền** (#566), **effort/model thực** của executor và của tôi.
- **Tính chất ứng-với-`ten` của `phong`** (N1): chưa có chốt nào đo, ở cả g1 lẫn g2.

## 8. Tái lập, và tệp trong `goi/`

Mọi script của tôi ở `goi/so-lieu/script/`; số liệu thô ở `goi/so-lieu/{pli,a10,a4,a9,dbk,probes,pm,khac}/`. Lệnh chính (đường dẫn rút gọn; `PY` = interpreter venv, `-B`, `PYTHONDONTWRITEBYTECODE=1`, `HOME` rỗng riêng):
```
pli.sh                                  # Phụ lục I: bốn lượt xen kẽ (nền,g1),(nền,g2),(nền,g1),(nền,g2) trong MỘT script
PY a10v.py PY <a10_g1> <a10_g2> <ra>    # A10 (iv)(v)+(r13)+(r14), chạy ở 3.11/3.12/3.13 (hai cây git archive)
taskset -c 0,1 PY -B manh_a9_r12.py <nen> <g2> <ra tuyet doi> 45 1 3
CONG_CU_TEST_BAN_KINH=manh PY -B ops/cong_cu_test.py                      # A4 (a), ba phiên bản
PY -B kiem_canh_r5.py <nen> <g2> bang_noi_reviewer.txt do_dot_bien.py do_dot_bien_r6.py   # A5 pre-check, bảng nối dựng từ DOT_BIEN
PY -B giao_a4d_r3.py <g2> fc852ff… ; PY -B ast_dot_bien_r2.py <g2>/ops/cong_cu_test.py   # A4 (d)(e)
PY -m ruff check --select F --no-cache --output-format json ops/cong_cu_test.py
PY -B dbk.py <g2> <ra> <w> 2 t53_,t54_  # 191 mục DOT_BIEN đích t53/t54;   PY -B pm.py <g2> <ra> <pm…>   # đột biến bản vá
probes_w.sh <w> 2 <cpu> mau_A.txt A ;  agg_probes.py                      # mẫu 419 dò, g2 rồi g1 trong cùng worker
```
Mọi phép đo chạy trên các cây sau, đều nằm trong `mktemp -d -p $R`: bốn clone `git clone --shared` (`nen` = `fc852ff`, `g1` = `19a2d96`, `g2` = `3b3d644`, `c4beb` = `4beb9d0`), hai cây `git archive` (`a10_g1`, `a10_g2`) và các cây `cp -al` có thay đúng một tệp (`chi_m7a`, `chi_m7b`, `a10_p1a`, `a10_shadow`, `a10_gocf`); `cay-kho` chỉ được đọc.

**Ghi chú quy trình (độ lệch so với PROMPT, nói thẳng):** (1) đỉnh song song của tôi vượt trần 4 tiến trình đo trong ~15 phút (A4 (c) chạy 4 tiến trình trên lõi 2–3 cạnh 2 tiến trình A9 trên lõi 0–1; kết quả A4 (c) là đúng/sai nên không ảnh hưởng, riêng A9 đã ghi ở N4) và vài phút khi `release-verify`, `ruff`, `actionlint` chen vào lúc đã đủ 4; (2) hai tệp tạm 0 byte (đầu ra `actionlint`) tạo ở `/tmp/claude-0/` rồi xoá ngay — ngoài thư mục cho phép, nội dung rỗng;
(3) tôi dùng `git clone --shared` từ `cay-kho` (chỉ đọc đối tượng, không ghi vào `cay-kho`) cho các phép đo cần `HEAD`, và `git archive` cho A10 (v) như đặc tả đòi; (4) `rm -f` trên hai tệp tạm nói ở (2) và `shutil.rmtree` cho thư mục tạm; không dùng `rm -rf`. `cay-kho` kết thúc ở `HEAD 3b3d644`, `status` sạch; không còn tiến trình con nào của tôi.

**Lớp mở:** không. `goi/HINT.patch` rỗng. Dry-run trên bản sao `cong_cu_test.py` của g2 (băm `6dc6f88c…` trước và sau):
`patch -p0 --fuzz=0 --dry-run --verbose cong_cu_test.py < HINT.patch` → "Hmm...  I can't seem to find a patch in there anywhere." rc=0; `git apply --check HINT.patch` → `error: No valid patches in input (allow with "--allow-empty")` rc=128; `git apply --check --allow-empty HINT.patch` → rc=0.
