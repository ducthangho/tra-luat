verdict: approve
reviewed_sha: 5d889bab2ad227d31b1ff800c3158967c65d1ef0
spec_sha256: ed027f410aac7eeedd60335459ba8cfef521a34730fea68c1255533bb56f1a21
reviewer_provider: anthropic
reviewer_model: claude-sonnet-5-5 (subagent review-sonnet-max, tự khai)
execution_surface: claude_code_subagent
che_do: subagent_trong_phien_dieu_phoi

# Review thi hành wp698 `CI-G5-CONG-CU-VA-TIEP` r14 g2 — lượt thi hành 2 (HẸP: bản vá Windows `5d889ba`)

**KẾT LUẬN: `approve` — 0 P1 · 0 P2 · 3 P3 = 3 lớp mở.** Ba lớp P3: `windows-hai-canh-t52-khong-do-duoc-nhung-bao-van-xanh`, `chot-nen-nt-ba-cua-noi-chi-song-tren-linux`, `khoi-phuc-ket-thuc-manh-sau-mo-phong-nt-khong-co-chot`.
`goi/HINT.patch` mô tả hướng sửa cho cả ba (chỉ chú thích, không mã; `ast.dump` trước/sau bằng nhau).

Reviewer tự khai: **Claude Sonnet 5.5 (`claude-sonnet-5-5`), subagent trong phiên điều phối, KHÔNG phải codex**; effort "max" theo chỉ thị điều phối — effort và model thực đã phục vụ là **KHÔNG ĐO ĐƯỢC** từ bên trong phiên.
Làm đúng `PROMPT.md` với ba khác biệt do điều phối nêu: (1) khai đúng danh tính trên; (2) không sửa `cay-kho/` (chỉ đọc; mọi đo trên `git clone --shared` / `cp -al` trong `mktemp -d -p $R`, dọn bằng `shutil`, không `rm -rf`); (3) không mạng, không đăng GitHub, không commit/push.
Phiên đo 2026-10-10 16:02Z–≈18:30Z (lease hết hạn 20:20Z), container 4 lõi (`nproc` = 4), Python 3.12.3 (+ 3.11.15, 3.13.12), PyYAML 6.0.3, jsonschema 4.26.0, ruff 0.15.15, git 2.43.0. Ba trạng thái: **có · không · KHÔNG ĐO ĐƯỢC**. Số liệu thô và script ở `goi/so-lieu/`, `goi/script/` (§9).

`approve` ở đây chỉ nói: bản vá đạt chữ r14 và đóng P1 của bot **ở mức `t52` trên Linux và trong mô phỏng**, không đổi hành vi Linux, và không có lỗi 0-P1/0-P2 đo được. Nó **không** thay A6 (cổng thẩm quyền `human_audited`), không thay lượt CI 2 (S10), và **không chứng minh Windows**: Windows thật là KHÔNG ĐO ĐƯỢC (Q8).

## Trả lời bốn việc của PROMPT (tóm tắt; bằng chứng ở các mục sau)
1. **Bản vá có đóng P1 không — CÓ, ở mức `t52`.** Dưới shim luật tên tệp Windows: g2 ⇒ `t52` ĐỎ (9/456 ô lệch, `NEM:OSError` — đúng cơ chế PROMPT và thông điệp commit mô tả: "bộ ghi ném, ô lệch"); ứng viên + quyết định `nt` ⇒ `t52` QUA; gỡ chốt ⇒ ĐỎ lại (§1.3). Khối là chỗ DUY NHẤT trong cả 56 ca còn ghi tên cấm mà không tự bỏ qua (§1.3, §1.2).
   Cha/con không so khoá `ghi698` lệch về giá trị (§1.4). Còn lại: vòng bán kính lane Windows (hai canh `t52_` thành "không đo được", báo "vẫn XANH") — P3 thứ nhất (§1.5); quyết định nền đọc ở ba chỗ độc lập — P3 thứ hai (§3).
2. **Linux không đổi hành vi — CÓ.** Suite `manh` 56/56 ở 3.11/3.12/3.13 (kèm g2 ở 3.12); ruff F delta ∅; Phụ lục G `cham: []`; **`_in_tu_kiem_gom` không nằm trong sáu hàm cấm đổi của A4-d** nên tách khối không vi phạm A4-d/S1; S5 = 269 ≤ 300; KQ ba cửa con: `main` trùng từng byte,
   `gom` và `che-do` trùng sau khi chuẩn hoá đường dẫn/tên tạm (`che-do` khác duy nhất ở sha256 của chính tệp test) (§2).
3. **Kiểm mới có răng — CÓ cho chốt, CHƯA cho dây nối.** 19 đột biến toàn tệp: gỡ/sửa/đảo chốt đều CHẾT bằng `TinHieuChotCa` đúng ca `t52_…`, bán kính 1/56; đột biến đổi mặc định `ten_nen` → `"nt"` CHẾT, → `"posix"`/`None` **SỐNG**; thêm ba cửa nối khác cũng SỐNG (§3, P3).
4. **Mẫu 419 dò / bán kính:** 67 dò (100 % dò đích `t52_` + 22 đối chứng) × g2 và ứng viên = 134 lượt: hạng bằng nhau 67/67 và tập ca chết bằng nhau 67/67; 67/67 mục `DOT_BIEN` đích `t52_` giết đúng ca, bán kính 1/56; Phụ lục F rc=0 (§4).

## 0. Đầu vào đã kiểm (lệnh + output thật)

```
$ git -C cay-kho rev-parse HEAD HEAD:ops/cong_cu_test.py
5d889bab2ad227d31b1ff800c3158967c65d1ef0
f0fc96c1dcd3d21ee8e4737ec88226575c9209e8                       (= reviewed_sha và blob của PROMPT; không lệch ⇒ không `blocked`)
$ git -C cay-kho status --short --untracked-files=all | wc -l  ->  0     (trước, giữa và sau mọi phép đo)
$ sha256sum SPEC.md lease.yaml PROMPT.md diff-g2-g2b.patch
ed027f410aac7eeedd60335459ba8cfef521a34730fea68c1255533bb56f1a21   SPEC.md        (= spec_sha256 của PROMPT)
a8c9cd161db29d3f4cca0153978d6e2738b30c96f6fa7d62e2b251c684ce79af   lease.yaml     (lease_id wp698-r14-g2-claude, hết hạn 2026-10-10T20:20:00Z, chưa tới lúc đo)
7d702394a143728165f65f224e47f1ca26bbea2107dc85b46396560432599cf8   PROMPT.md
25a80d34c115be5d48603e00840143fabeb596013e631f0dbd0ce66352613e1c   diff-g2-g2b.patch
$ python3 goi/script/trich_pl.py SPEC.md goi/so-lieu/pl     ->  14 phụ lục, "khop 14 lech 0" (băm khớp tiêu đề từng phụ lục)
   bản ghép do_dot_bien_r3…r6 dựng bằng đúng lệnh của đặc tả: 37b6e8bd…, bec92f6e…, acb8d897…, 5d1a4ada… (khớp băm đặc tả khai)
$ patch -p1 --fuzz=0 < diff-g2-g2b.patch  (trên blob g2 `ba9099e3`)  ->  blob `f0fc96c1…` = blob ứng viên
$ git -c core.abbrev=9 diff 3b3d644 5d889ba | cmp - diff-g2-g2b.patch   ->  trùng từng byte (diff cung cấp là diff thật)
$ git diff --numstat 3b3d644 5d889ba  ->  50  30  ops/cong_cu_test.py    (đúng một tệp)      $ git diff --check 3b3d644 5d889ba -> rc=0
```
Ba cây đo dựng **trong MỘT vòng lặp** (`git clone --shared` rồi `checkout`, `core.abbrev 7`, `core.autocrlf false`): `nen` = `fc852ff…`, `g2` = `3b3d644…`, `ung` = `5d889ba…`
(blob `ops/cong_cu_test.py`: `9edea6b1…` · `ba9099e3…` · `f0fc96c1…`; `git status` mỗi cây: 0 dòng). Mọi lượt đo chạy với `env -i` (PATH có `/root/.local/bin` cho `actionlint`),
`HOME`/`TMPDIR` riêng từng tiến trình, `PYTHONDONTWRITEBYTECODE=1`, `python -B`; không biến `CONG_CU_TEST_*` ngoài ý muốn. Không dùng mạng.

## 1. Việc 1 — bản vá có đóng P1 không (Windows: mô phỏng được thì mô phỏng, không thì lập luận từ mã)

### 1.1 Khối được dời có TRUNG THỰC không (đo)
```
$ python3 (dedent khối cũ trong _in_tu_kiem_gom @3b3d644 ↔ thân _ghi698 @5d889ba, difflib.unified_diff -n0)
@@ -4,0 +5,4 @@   + 2 dòng chú thích `# PR #721 (Codex P1) …` + `if ten_nen == "nt":` + `    return [0, [], 0]`
@@ -8 +12 @@     - cac_p, t1 = _duong698()[:60] + [...], cac[:1]      + cac_p = _duong698()[:60] + [...]          (t1 thành tham số)
@@ -29 +33 @@    - kq["ghi698"] = [len(cac_p), lech[:10], len(lech)]  + return [len(cac_p), lech[:10], len(lech)]
```
Đúng ba khác biệt, mọi dòng khác trùng từng ký tự sau khi bỏ thụt lề. Không tên cục bộ nào rò từ khối ra phần sau của `_in_tu_kiem_gom` (ruff F delta ∅, không `F821` mới). Cửa con trên Linux
in `kq["ghi698"] == [456, [], 0]` ở cả g2 lẫn ứng viên (§2.5).

### 1.2 Tên tệp THẬT mà `t52` và cửa con của nó ghi ra đĩa, ngoài khối #698
`grep` mọi chỗ dùng `_duong698`/`_d698`/`_N698`/`_R698`: chỗ ghi đĩa duy nhất là `_ghi698`; các chỗ còn lại là bộ nhớ thuần (`_luoi_che_do`, `_luoi_git`, `_luoi_noi_main` đi qua `main()` với `_ket_thuc_manh` đã thay bằng bộ ghi sự kiện ở `_in_tu_kiem_main`).
Tên tệp còn lại của `t52`/cửa con: `manh-{k}.txt`, `manh-0b.txt`, `ngoai-{thu.name}.txt`, `gay.txt`, `thu_muc_con`, và **một** tên có khoảng trắng cuối `a/b c/manh-0.txt ` (F35) — **không tên nào chứa `<>:"|?*`, ký tự U+0001–U+001F**.
Tên có khoảng trắng cuối đã có ở nền `fc852ff` (1 lần, đo bằng `grep -c`), theo hiểu biết về Win32 (chuẩn hoá bỏ khoảng trắng cuối) thì `write`/`is_file()`/`read_text()` cùng đường — đó là hiểu biết, không phải phép đo: chạy trên Windows thật **KHÔNG ĐO ĐƯỢC**, nhưng không phải thứ bản vá thêm.

### 1.3 Mô phỏng luật tên tệp Windows trên Linux (đo; KHÔNG phải Windows thật)
`script/shim/sitecustomize.py` (nạp qua `PYTHONPATH`, nên cả cha lẫn mọi tiến trình Python con đều thấy): `os.stat/lstat/mkdir/open/unlink/rmdir/rename/replace/scandir/listdir/chdir/symlink/readlink/remove`
và `io.open`/`builtins.open` ném `OSError(EINVAL)` khi đường dẫn có `<>:"|?*` hoặc U+0001–U+001F (giống `ERROR_INVALID_NAME`). Cây `ntsim` = ứng viên với **đúng hai dòng** đổi để mô phỏng quyết định `nt`
(`ten_nen=os.name` → `ten_nen="nt"`; `if os.name == "nt" else` → `if True else`; `diff` chỉ hai dòng). `script/win_t52.py` chạy RIÊNG ca `t52` bằng `_chay_1_ca` của cây:

| lượt | cây | shim luật tên Windows | `t52` | thông điệp đầu |
|---|---|---|---|---|
| R1 | g2 `3b3d644` (trước bản vá) | có | giet_that | `bộ ghi #698 [số ô, ô lệch đầu, tổng lệch]: [456, [[30, "'\\ta/b'", "['NEM:OSError']"], [31, "'a…` |
| R2 | ứng viên, quyết định Linux | có | giet_that | `bộ ghi #698 [số ô, ô lệch đầu, tổng lệch]: [456, [[30, "'\\ta/b'", "['NEM:OSError']"], [31, "'a…` |
| R3 | ứng viên + quyết định `nt` (mô phỏng) | có | qua | — |
| R4 | như R3 nhưng gỡ chốt `ten_nen == "nt"` | có | giet_that | `bộ ghi #698 [số ô, ô lệch đầu, tổng lệch]: [456, [[30, "'\\ta/b'", "['NEM:OSError']"], [31, "'a…` |
| R0 | ứng viên, quyết định Linux | không | qua | — |
| R0b | ứng viên + quyết định `nt` | không | qua | — |

- **R1 tái hiện cơ chế P1 như PROMPT và thông điệp commit mô tả (nội dung bình luận thật của bot: KHÔNG ĐO ĐƯỢC)**: g2 + luật tên Windows ⇒ `t52` ĐỎ với `ghi698 = [456, […], 9]` — **9/456 ô lệch**, tất cả `['NEM:OSError']`: ô 30–32 và 42–44 (TAB và VT ở đầu/giữa/cuối `a/b`: `'\ta/b'`, `'a\t/b'`, `'a/b\t'`, `'\x0ba/b'`…) và ô 60–62 (ba khúc tên 50 ký tự chứa U+0001…, `"` `*` `:` `<` `>` `?` `\` `|`) — đúng "bộ ghi ném, ô lệch".
- **R2**: bản vá không đổi quyết định trên Linux (như mong): vẫn đỏ dưới luật Windows nếu khối chạy. **R3**: chỉ khi quyết định là `nt` thì `t52` **QUA** dưới cùng luật tên ⇒ khối là nguồn DUY NHẤT của tên cấm trong `t52` và cửa con (mọi lệnh đĩa còn lại qua shim sạch).
  **R4**: gỡ chốt khỏi R3 ⇒ ĐỎ lại. R0/R0b: không shim ⇒ cả hai xanh (ntsim là một biến thể nhất quán, không tự đỏ).

**Cả 56 ca dưới cùng luật tên** (`script/db_run.py … nen` với `PYTHONPATH=script/shim`; mỗi ca bằng `_chay_1_ca` của cây, 3.12):

| cây | ca không `qua` |
|---|---|
| `ntsim` (quyết định `nt`) | chỉ `t48_khung_INDEX_giu_BYTES_va_anh_chup_ghim_BLOB`: `bo_qua` — "nền này không đặt được tên tệp có ký tự điều khiển: [Errno 22] mo phong Windows: ten co ky tu cam" (tự bỏ qua, có sẵn từ #570 r13). **Không ca nào ĐỎ.** |
| `ung` (quyết định Linux) | `t48_…` `bo_qua` như trên, và `t52_…` **giet_that** (khối ghi #698). Không ca thứ ba. |

⇒ dưới luật tên Windows, khối #698 M2b T4/T5 là chỗ DUY NHẤT trong cả bộ ca còn ghi tên cấm mà không tự bỏ qua; chốt `nt` đưa bộ ca về 55/55 đạt + 1 tự bỏ qua (`t48`).


### 1.4 Cha và con có so khoá `ghi698` lệch giữa hai nền không?
**Không lệch ở giá trị; lệch ở CÁCH QUYẾT ĐỊNH nền (lớp P3 thứ hai).**
- Cửa con đặt `kq["ghi698"]` **vô điều kiện** (lời gọi `_ghi698(d, n, vt, cac[:1])` luôn chạy; chỉ nội dung khác): Linux `[456, [], 0]` (3.12; 452 ở 3.11, 457 ở 3.13 — đo ở §2.5), `nt` `[0, [], 0]`. Nên không có `KeyError` nào ở cha, kể cả trên Windows.
- Cha: Linux đòi `kq["ghi698"][0] > 60 and kq["ghi698"][1:] == [[], 0]`; `nt` đòi `kq["ghi698"] == [0, [], 0]`. Thứ tự ưu tiên toán tử đã đo (đột biến `cha_nhanh_dao` chết đúng ở câu `bang` này): `A if os.name == "nt" else (B and C)`.
- Hai vế đọc `os.name` **độc lập** (con: giá trị mặc định tính lúc `def`; cha: lúc gọi) và nơi gọi còn có thể ghim tham số — cùng một interpreter nên không thể lệch trong thực tế, nhưng **không có nguồn duy nhất** ⇒ ba cửa mà Linux không thấy (§3, lớp P3).
- Bất đối xứng độ chặt có chủ đích: Linux chỉ đòi `> 60` (số ô chính xác do A10 (v) ghim ngoài tệp, 456/452/457), `nt` đòi đúng `[0, [], 0]`. Không phải lỗi.

### 1.5 Điều bản vá chưa đóng: vòng BÁN KÍNH của lane Windows — lớp P3 thứ nhất
Bản vá làm `t52` **xanh** trên `nt` (R3). Nhưng khối #698 M2b T4/T5 không chỉ là một phép kiểm của `t52`; nó là **nguồn giết duy nhất** của hai canh thường trực mà đặc tả đòi (A2, A5) với ca đích `t52_…`:
`w698_x_wr_ra_nfkc` (chỉ số 454 trong `DOT_BIEN` ⇒ mảnh **6**/8) và `w698_x3_wr5_nfkc` (chỉ số 455 ⇒ mảnh **7**/8) — NFKC đặt ở `Path(ra)` / ở chỗ ghi của `_ket_thuc_manh`, chỉ lộ nhờ khúc tên tệp chứa ký tự NFKC-nhạy; mọi tên tệp khác mà `t52` ghi đều thuần ASCII.
Hai canh được đăng ký **vô điều kiện** (vòng `for _ten, _ca, _tim, _thay in (…)`, dòng 1869–2312; hai canh ở dòng 2309–2310). Trên `nt` khối không chạy ⇒ không ca nào giết được chúng. Đo bằng chính `_do_ban_kinh` + `_ket_luan_ban_kinh` của cây trên **67 mục `DOT_BIEN` có ca đích `t52_`** (65 cũ + 2 canh mới; 3.12; `script/db_run.py`):

```
ứng viên (Linux thật)       :  67/67  "ok … giết đúng 't52_…' · bán kính 1/56"
  ok  w698_x_wr_ra_nfkc → giết đúng 't52_gom_manh_phai_DO_khi_thieu_trung_lech_va_moi_chot_co_THE_RIENG' · bán kính 1/56
  ok  w698_x3_wr5_nfkc  → giết đúng 't52_gom_manh_phai_DO_khi_thieu_trung_lech_va_moi_chot_co_THE_RIENG' · bán kính 1/56
ntsim (quyết định `nt`)     :  65/67  — đúng hai mục không ok, dich_tt=`qua`, khong_qua={} (đo hai lần: lượt đầu và lượt chạy lại, cùng kết quả):
  ĐỎ  w698_x_wr_ra_nfkc: đích 't52_gom_manh_phai_DO_khi_thieu_trung_lech_va_moi_chot_co_THE_RIENG' vẫn XANH ⇒ đột biến không giết được gì
  ĐỎ  w698_x3_wr5_nfkc: đích 't52_gom_manh_phai_DO_khi_thieu_trung_lech_va_moi_chot_co_THE_RIENG' vẫn XANH ⇒ đột biến không giết được gì
```
65 mục cũ còn lại giết đúng `t52_…` bán kính 1/56 cả ở `ntsim` — tức **chỉ hai canh mới bị ảnh hưởng**, không phải cả họ `t52_`.

Hậu quả nếu lane Windows chạy (nhãn `windows` trên PR, hoặc `workflow_dispatch`; `ci.yml` `chuan-bi.outputs.os`): `_ket_luan_ban_kinh` ⇒ `loi=1` cho mỗi canh; `_ket_thuc_manh` không ghi tệp mảnh và in
`ĐỎ  mảnh 6/8 [M-loi]: 1 lỗi đột biến — không ghi tệp` (tương tự mảnh 7/8) ⇒ `rc=1`, bước `upload-artifact … if-no-files-found: error` đỏ, job `gate-cong-cu-gop` thiếu hai tệp (`[G-tap]`). Tức mảnh 6, mảnh 7 và gom đỏ trên Windows — **suy từ mã** `main()`/`_ket_thuc_manh`/`_gom_manh` (đã đọc), không chạy end-to-end.

**Vì sao P3, không P2 (đã cân, và đổi hạng sau khi đo thêm).** Tệp CÓ tiền lệ cho "nền không dựng được kịch bản ⇒ đột biến của nó không đo được ⇒ vòng bán kính đỏ, và đó là thiết kế fail-closed (`None ≠ False`)": `t48` ném `BoQuaMoiTruong("nền này không đặt được tên tệp có ký tự điều khiển")`,
và hai đột biến đích `t48_` (`bn_khung_dich_dong`, `bn_anh_chup_chi_dem_so`) đăng ký vô điều kiện. Đo dưới shim luật tên Windows (cây `ung`, 3.12, `script/db_run.py` với `PYTHONPATH=script/shim`):
```
KHÔNG_ĐO_ĐƯỢC bn_khung_dich_dong: đích 't48_khung_INDEX_giu_BYTES_va_anh_chup_ghim_BLOB' bị BỎ QUA — nền này không đặt được tên tệp có ký tự điều khiển: [Errno 22] …     (loi=1)
KHÔNG_ĐO_ĐƯỢC bn_anh_chup_chi_dem_so: đích 't48_…' bị BỎ QUA — nền này không đặt được tên tệp có ký tự điều khiển: [Errno 22] …                                              (loi=1)
```
Tức (dưới shim; Windows thật KHÔNG ĐO ĐƯỢC) vòng bán kính Windows đã có ít nhất hai mục "không đo được ⇒ đỏ" TRƯỚC bản vá, và Windows (Q8; `ngoai_pham_vi`: "Chạy Windows … chủ kho quyết không", nợ `windows-chua-do-o-moi-wp698`) không phải trạng thái xanh đã được thiết lập (0 job mảnh Windows trong 56 run nền đã đọc, §1.13.2 đặc tả).
Hai canh mới chỉ thêm hai mục vào cùng họ. Cái đáng ghi là **chẩn đoán**: `t48` nói đúng "BỎ QUA — không đặt được tên tệp…", còn hai canh nói "đích vẫn XANH ⇒ đột biến không giết được gì" — đọc thành "kiểm mất răng" trong khi thật ra là "kịch bản không chạy trên nền này".
Chính `_do_co_symlink` (docstring) dạy cách tránh: *"Kịch bản + đột biến symlink chỉ đăng ký khi CÓ: đăng ký mà không dựng được kịch bản thì đột biến ấy sống trên nền đó và làm ĐỎ oan cả vòng bán kính."* Không chặn: lane Windows tắt theo Q8; đóng bằng hồ sơ hoặc bằng idiom đăng ký-theo-năng-lực.

### 1.6 Trả lời việc 1 (tóm tắt)
- `t52` xanh dưới luật tên Windows khi quyết định là `nt` (R3), đỏ khi gỡ chốt (R4); khối là nguồn duy nhất của tên cấm trong toàn bộ 56 ca (§1.3, lượt toàn bộ CA); đóng P1 **cho ca `t52`**. Windows thật: KHÔNG ĐO ĐƯỢC.
- Đường khác liên quan khối #698: vòng bán kính Windows — 2 canh `t52_` thành "không đo được" nhưng báo "vẫn XANH" (lớp P3 thứ nhất). Không đường nào khác chạm tên cấm.
- Cha/con không lệch giá trị; quyết định nền có ba cửa đọc độc lập mà Linux không thấy (lớp P3 thứ hai).

## 2. Việc 2 — trên Linux không đổi hành vi

### 2.1 Suite `CONG_CU_TEST_BAN_KINH=manh`, ba phiên bản Python, bốn tiến trình song song (258–264 s mỗi lượt)
```
$ env -i PATH=… HOME=<riêng> TMPDIR=<riêng> PYTHONDONTWRITEBYTECODE=1 CONG_CU_TEST_BAN_KINH=manh <venv3.11|3.12|3.13>/bin/python -B ops/cong_cu_test.py     (script/suite.sh)
```
| cây · Python | dòng `56/56 đạt; … bỏ qua=0` | dòng `SỐ LIỆU … lỗi đột biến=0 … cổng cây thật=ĐẠT` | dòng `ĐỎ` | dòng `BỎ QUA` | `rc=0` |
|---|---|---|---|---|---|
| g2 `3b3d644` · 3.12 | 1 | 1 | 0 | 0 | 1 |
| ứng viên · 3.11 | 1 | 1 | 0 | 0 | 1 |
| ứng viên · 3.12 | 1 | 1 | 0 | 0 | 1 |
| ứng viên · 3.13 | 1 | 1 | 0 | 0 | 1 |

Mỗi lượt có đúng một dòng `cong_cu_test: 56/56 đạt; tổng=56, bỏ qua=0, tiền kiểm bỏ qua=0` và đúng một dòng
`SỐ LIỆU: ca=56 · đột biến=470 (giao mảnh) · lỗi đột biến=0 · tiền kiểm bỏ qua=0 · cổng cây thật=ĐẠT`, `rc=0`, 0 dòng `ĐỎ`, 0 dòng `BỎ QUA` — bằng chứng DƯƠNG (hai số bằng nhau, không chỉ `rc=0`). Cây g2 cùng lệnh, cùng lượt: giống hệt.
Trong tiến trình (một lượt 56 ca, không đột biến, 3.12): `ung` và `g2` đều `khong_qua = {}` (33,8 s / 34,2 s; `script/db_run.py … nen`).

### 2.2 Cây sạch, tĩnh
```
$ git diff --numstat fc852ff -- ops/cong_cu_test.py ; git diff --numstat 4beb9d0 -- .github/workflows/ci.yml ops/ci_duong_nhanh_test.py
267	14	ops/cong_cu_test.py
1	1	.github/workflows/ci.yml
1	1	ops/ci_duong_nhanh_test.py
$ git diff --name-only 4beb9d0 5d889ba
.github/workflows/ci.yml
ops/ci_duong_nhanh_test.py
ops/cong_cu_test.py
$ giao_a4d_r3.py ung fc852ff  (Phu luc G)
{"hunk": 23, "cham": []}
rc=0
$ ast_dot_bien_r2.py ung/ops/cong_cu_test.py  (Phu luc E)
{"_TRUOC_NANG_LUC": 7514, "_TEN_NANG_LUC": 7548, "tong": 9, "truoc_anh": [2312, 2318], "trong_cua_so": 7, "sau_moc": []}
$ ruff 0.15.15 check --select F --no-cache (nen / g2 / ung): da tap (ma, thong diep)
nen {('F841', 'Local variable `ci` is assigned to but never used'): 1} [2606]
g2 {('F841', 'Local variable `ci` is assigned to but never used'): 1} [2662]
ung {('F841', 'Local variable `ci` is assigned to but never used'): 1} [2662]
$ kiem_canh_r5.py nen ung bang_noi.txt do_dot_bien.py do_dot_bien_r6.py  (Phu luc F)
{"nen": 416, "ung_vien": 470, "them": 54, "bang_noi": 54, "dem_neo": {"muc": 470, "lech": 0}, "so_loi": 0, "loi": []}
rc=0
$ A1 (iv) cua A1: nen / g2 / ung
0 0 ['0x2026']
0 0 ['0x2026']
0 0 ['0x2026']
$ python -B -W error -c "compile(open(f).read(), f, 'exec')"  g2 và ung × 3.11/3.12/3.13      ->  6/6 "compile -W error: OK"
$ git diff --check 3b3d644 5d889ba  ->  rc=0        (0 CR/TAB/ký tự điều khiển trong 50 dòng thêm)
```
- **S5:** `267 + 1 + 1 = 269 ≤ 300` (trước: 249) · 3 tệp ≤ 3 ⇒ không dừng. · **S1:** chỉ `ops/cong_cu_test.py` đổi so với g2; hai tệp còn lại của write set không đổi (mỗi tệp đúng `1 1` so với `4beb9d0`).
- **ruff F:** cả ba cây cùng đúng một lỗi `F841 Local variable ci is assigned to but never used` (:2606 / :2662 / :2662) ⇒ delta đa tập ∅.
- **A4-e:** `sau_moc: []`, `tong: 9` (không đổi).

### 2.3 A4-d — `_in_tu_kiem_gom` có trong danh sách cấm đổi không? ĐỌC CHỮ r14
A4-d (§6) cấm đổi **thân đúng sáu hàm**: `_doc_che_do`, `_van_tay`, `main`, `_so_tien_trinh_ban_kinh`, `_ket_luan_ban_kinh`, `_chay_1_ca`; danh sách giống hệt ở §4 ("Đổi thân … ⇒ S1"), ở S1 và ở hằng `SAU` của Phụ lục G.
**`_in_tu_kiem_gom` KHÔNG nằm trong đó** (toàn đặc tả nhắc nó ba lần: §1.8 mô tả kịch bản, §1.11.2 liệt kê chỗ gọi bằng AST, A7 là danh sách hàm phải `grep`). Nên dời một khối ra hàm mới `_ghi698` **không** vi phạm A4-d/S1.
Đo: Phụ lục G trên ứng viên so với `fc852ff`: `{"hunk": 23, "cham": []}`, rc=0 (g2: 22 hunk, `cham: []`); và với g2 làm nền (khoảng hàm lấy trên g2): 3 hunk, `cham: []`.
Cũng không trái M2b ("thêm vào cửa `--tu-kiem-gom` một lưới ô bộ ghi THẬT": cửa vẫn gọi khối) hay M6 (khối bắt `BaseException` quanh lời gọi bộ ghi giữ nguyên, §1.1).

### 2.4 Mỏ neo (A5 pre-check, Phụ lục F) — khối bị dời không làm trượt mỏ neo nào
`kiem_canh_r5.py nen ung bang_noi.txt do_dot_bien.py do_dot_bien_r6.py` (bảng nối dựng từ chính 54 tên `w698_*` của `DOT_BIEN`; chốt `tap-do` so với 54 tên đóng băng): `{"nen": 416, "ung_vien": 470, "them": 54, "bang_noi": 54, "dem_neo": {"muc": 470, "lech": 0}, "so_loi": 0}` **rc=0**.
Cùng lệnh trên g2: kết quả y hệt. Thêm: 0/419 dò có mỏ neo trong `t52`/`_in_tu_kiem_gom`/`_ghi698` (§4.1).

### 2.5 KQ ba cửa con, g2 ↔ ứng viên, cùng một lệnh (xen kẽ g2 rồi ứng viên từng cửa; `PYTHONHASHSEED=0`)
```
$ python -B ops/cong_cu_test.py --tu-kiem-che-do | --tu-kiem-gom | --tu-kiem-main      (script/cua_kq.sh, script/cua_kq_pv.sh)
```
| Python | cửa | rc g2/ứng | số khoá | byte dòng `KQ` | trùng từng byte (thô) | trùng sau chuẩn hoá đường dẫn/tên tạm | khoá còn khác | `ghi698` g2 / ứng |
|---|---|---|---|---|---|---|---|---|
| 3.11 | `--tu-kiem-che-do` | rc=0/rc=0 | 32/32 | 11714/11717 | không | không | `byte` | — |
| 3.11 | `--tu-kiem-gom` | rc=0/rc=0 | 72/72 | 50886/50891 | không | có | — | [452, [], 0] / [452, [], 0] |
| 3.11 | `--tu-kiem-main` | rc=0/rc=0 | 508/508 | 2692698/2692698 | có | có | — | — |
| 3.12 | `--tu-kiem-che-do` | rc=0/rc=0 | 32/32 | 11764/11767 | không | không | `byte` | — |
| 3.12 | `--tu-kiem-gom` | rc=0/rc=0 | 72/72 | 50866/50871 | không | có | — | [456, [], 0] / [456, [], 0] |
| 3.12 | `--tu-kiem-main` | rc=0/rc=0 | 508/508 | 2697714/2697714 | có | có | — | — |
| 3.13 | `--tu-kiem-che-do` | rc=0/rc=0 | 32/32 | 11896/11899 | không | không | `byte` | — |
| 3.13 | `--tu-kiem-gom` | rc=0/rc=0 | 72/72 | 50886/50891 | không | có | — | [457, [], 0] / [457, [], 0] |
| 3.13 | `--tu-kiem-main` | rc=0/rc=0 | 508/508 | 2697774/2697774 | có | có | — | — |

Cột "chuẩn hoá" thay duy nhất: đường dẫn gốc cây (`…/g2` ↔ `…/ung`), thư mục `TMPDIR` riêng của lượt, và hậu tố ngẫu nhiên 8 ký tự của `gom668_xxxxxxxx`. Kết quả:
- **`main`: TRÙNG TỪNG BYTE** cả ba phiên bản (508 khoá; 2 692 698 / 2 697 714 / 2 697 774 B).
- **`gom`: trùng sau chuẩn hoá**; `ghi698` bằng nhau: `[452, [], 0]` (3.11), `[456, [], 0]` (3.12), `[457, [], 0]` (3.13) — đúng số lượt 1 ghi.
- **`che-do`: khác DUY NHẤT ở khoá `byte`** (`byte.thuc` = sha256 của chính tệp test: `6dc6f88c…` ↔ `a9c2a836…`) — không thể trùng giữa hai blob khác nhau. N1 (§6).
- Số khoá đỉnh 32 · 72 · 508 ở cả hai cây, cả ba phiên bản; rc=0 mọi lượt.

## 3. Việc 3 — kiểm mới có răng không (đột biến BẢN VÁ, mô hình TOÀN TỆP)

**Vì sao toàn tệp, không phải cơ chế `_do_ban_kinh`:** chốt `nt`, kiểm mô phỏng `nt` và câu `bang` của cha cùng nằm trong MỘT tệp; cha gọi `_ghi698` **của chính cha**.
Cơ chế đột biến thường trực (`bp = "TEP_TEST"`) chỉ sửa bản mà tiến trình CON chạy (đọc mã `_do_ban_kinh`: `g[bp] = dich`), nên không chạm được hàm của cha — đột biến chốt kiểu ấy sẽ
"SỐNG" vì sai mô hình, không vì kiểm yếu. Mô hình đúng cho bản vá là *ai đó sửa tệp này*: cha **và** con cùng bị sửa. `script/mut_ban_va.py`: mỗi đột biến =
`cp -al` cây ứng viên, `unlink` rồi ghi tệp test mới (không ghi lên inode dùng chung), anchor đúng 1 lần (`so_neo` = 1, kiểm bằng `assert`), rồi trong một
tiến trình sạch chạy `_chay_1_ca` cho **cả 56 ca** của `CA` (đúng hàm phân hạng của cây). `giet_that` ở đây = `TinHieuChotCa` mang **đúng tên ca `t52_…`**
(nhánh `return "giet_that"` của `_chay_1_ca`; ca khác lọt vào là `tin_dung_gia`); bán kính = số ca không `qua`.

| đột biến (TOÀN TỆP, cha và con cùng bị sửa) | sửa gì | kết quả | tín hiệu đỏ |
|---|---|---|---|
| `chot_bi_go` | gỡ chốt `if ten_nen == "nt": return [0, [], 0]` | **CHẾT** — `giet_that`, bán kính 1/56 | kiểm mô phỏng `nt` trong `t52` |
| `chot_tra_1` | chốt trả `[1, [], 0]` | **CHẾT** — `giet_that`, bán kính 1/56 | kiểm mô phỏng `nt` trong `t52` |
| `chot_tra_lech` | chốt trả `[0, ["x"], 0]` | **CHẾT** — `giet_that`, bán kính 1/56 | kiểm mô phỏng `nt` trong `t52` |
| `chot_tra_tong` | chốt trả `[0, [], 1]` | **CHẾT** — `giet_that`, bán kính 1/56 | kiểm mô phỏng `nt` trong `t52` |
| `chot_dao` | đảo chốt: `!= "nt"` | **CHẾT** — `giet_that`, bán kính 1/56 | câu `bang` đầu (kết quả cửa con trên Linux) |
| `chot_muon` | chốt ĐẶT MUỘN: khối chạy hết (bộ ghi giả bị gọi với tên cấm) rồi mới trả `[0, [], 0]` nếu `nt` | **CHẾT** — `giet_that`, bán kính 1/56 | kiểm mô phỏng `nt` trong `t52` |
| `chot_muon_va_cam_tat` | chốt muộn **cộng** `cam = []` (tắt chốt `cam`) | **SỐNG** — 56/56 ca `qua` | — |
| `cam_tat` | chỉ tắt chốt `cam` (`cam = []`), chốt còn nguyên | **SỐNG** — 56/56 ca `qua` | — |
| `mac_dinh_nt` | mặc định `ten_nen=os.name` → `"nt"` | **CHẾT** — `giet_that`, bán kính 1/56 | câu `bang` đầu (kết quả cửa con trên Linux) |
| `mac_dinh_posix` | mặc định → `"posix"` | **SỐNG** — 56/56 ca `qua` | — |
| `mac_dinh_none` | mặc định → `None` | **SỐNG** — 56/56 ca `qua` | — |
| `noi_goi_nt` | nơi gọi ở `_in_tu_kiem_gom` ghim `ten_nen="nt"` | **CHẾT** — `giet_that`, bán kính 1/56 | câu `bang` đầu (kết quả cửa con trên Linux) |
| `noi_goi_posix` | nơi gọi ghim `ten_nen="posix"` | **SỐNG** — 56/56 ca `qua` | — |
| `cha_nhanh_chet` | cha: `os.name == "nt"` → `== "khong-co"` (nhánh Windows chết) | **SỐNG** — 56/56 ca `qua` | — |
| `cha_nhanh_dao` | cha: `os.name == "nt"` → `!= "nt"` | **CHẾT** — `giet_that`, bán kính 1/56 | câu `bang` đầu (kết quả cửa con trên Linux) |
| `cha_nhanh_nt_sai_gia_tri` | cha: giá trị mong trên `nt` `[0, [], 0]` → `[0, [], 1]` | **SỐNG** — 56/56 ca `qua` | — |
| `mo_phong_goi_posix` | kiểm mô phỏng gọi `ten_nen="posix"` thay `"nt"` | **CHẾT** — `giet_that`, bán kính 1/56 | kiểm mô phỏng `nt` trong `t52` |
| `mo_phong_bang_tat` | kiểm mô phỏng: `bang(…)` → `bang(True, …)` | **SỐNG** — 56/56 ca `qua` | — |
| `khoi_phuc_bi_go` | bỏ khôi phục `_ket_thuc_manh` trong `finally` (→ `pass`) | **SỐNG** — 56/56 ca `qua` | — |

**Đọc bảng:**
- **Chốt (hàm con) có răng, đúng ca, đúng lý do.** Gỡ chốt (`chot_bi_go`), trả sai giá trị ở ba chiều (`chot_tra_*`), đảo chốt (`chot_dao`) đều `giet_that` bởi `t52_…`, bán kính **1/56**, không `tin_dung_gia`.
  `chot_bi_go` chỉ chết bởi kiểm mô phỏng `nt` (câu `bang` đầu vẫn xanh trên Linux vì cửa con chạy nhánh POSIX) với thông điệp
  `khối #698 M2b trên `nt` gọi bộ ghi với tên Windows cấm: [456, …` — đúng chuỗi executor khai.
- **`ra_nt == [0, [], 0]` và `not cam` là hai chốt KHÔNG tương đương.** `chot_muon` (khối chạy hết rồi mới trả `[0, [], 0]`) làm `ra_nt` đúng nhưng chết nhờ `cam`
  (bộ ghi giả bị gọi với `'a\\b'`, `'\ta/b'`…); thêm `cam = []` thì cùng đột biến **SỐNG** (`chot_muon_va_cam_tat`). Tức `cam` có việc riêng, không thừa.
- **`mac_dinh_nt`, `noi_goi_nt`, `cha_nhanh_dao`, `mo_phong_goi_posix` CHẾT** (đổi hành vi trên Linux, hoặc làm kiểm mô phỏng chạy khối thật).
- **SỐNG, và đó là câu hỏi của PROMPT (đột biến đổi mặc định `ten_nen`):** `mac_dinh_posix` và `mac_dinh_none` SỐNG (tương đương trên Linux: `os.name` là `"posix"`).
  Cùng họ, **ba cửa nữa** của quyết định "nền nào" cũng SỐNG: `noi_goi_posix` (nơi gọi ghim `"posix"`), `cha_nhanh_chet` và `cha_nhanh_nt_sai_gia_tri` (nhánh `nt` của cha chết/sai
  giá trị — trên Windows `t52` đỏ, trên Linux không ai thấy). **Năm đột biến SỐNG, mỗi cái tái mở đúng lỗi P1 (hoặc làm `t52` đỏ) trên Windows mà Linux không có tín hiệu nào** — lớp P3 bên dưới.
  Executor khai: mặc định `os.name` không có kiểm nào bắt trên Linux, và nhánh `nt` của `bang` "chưa từng chạy". Điều không được khai rõ: nơi gọi ghim nền (`noi_goi_posix`) cũng sống, và mỗi cái trong năm đột biến sống đều tái mở đúng lỗi trên Windows.
- `mo_phong_bang_tat` SỐNG là đương nhiên (xoá chính cái kiểm). **`khoi_phuc_bi_go` SỐNG**: 56/56 ca vẫn `qua`; xem lớp P3 thứ ba (đo trực tiếp rò rỉ ở §5).

## 4. Việc 4 — tập 419 dò và bán kính đột biến: MẪU có lý do, nền (g2) và ứng viên trong cùng một lệnh

### 4.1 Vì sao mẫu này, và vì sao mẫu này đủ cho miền bản vá chạm

Bản vá chỉ (i) dời một khối từ thân `_in_tu_kiem_gom` ra hàm mới `_ghi698` (3 khác biệt sau khi bỏ thụt lề, §1.1) và (ii) thêm vào `t52` một kiểm chạy TRONG TIẾN TRÌNH CHA bằng hàm
của cha. Hai hệ quả kiểm tra được: **(a)** dò/đột biến nào chết nhờ khối ghi #698 thì chết qua `_ghi698` trong cửa con — phải còn chết đúng; **(b)** đột biến của cơ chế thường trực chỉ sửa
`TEP_TEST` (tiến trình con) nên không chạm được kiểm mới của cha — bán kính của mọi dò/canh khác không được đổi. Vì thế mẫu gồm:
1. **Toàn bộ 45 dò có ca đích `t52_`** (`P[..][2] is T52`, đọc từ bản ghép r6): 36 dò T-C của bộ ghi T4/T5 (`x_wr_ra_*`, `x3_wr_ra_*`, `x3_wr5_*`, `x4_t4_*`, `x4_t5_*`, `y4_t4_*`, `x6_t4_ra`) + 9 dò ngoài lớp (`g_*`, `x3_gop_*`, `x3_cua_*`).
2. **22 dò đối chứng** chọn có lý do: 5 KHAI; 2 tương đương (`m_nfkc_no_bk`, `m_nfkc_khac_bmp_mh`); 3 KHÁC đã khai (`s_ra_realpath`, `x3_cat_ll_bk`; `x3_wr_ra_lower` đã nằm ở mục 1); 6 dò đường `ra` ở `main`
   (`x_main_ra_normpath`, `x_main_ra_nfkc`, `x3_m3a_ra_nfkc`, `x3_m3b_ra_cf`, `x4_t2_thoat_ra`, `x6_t2_ra`) và 3 dò `ra` ở `_doc_che_do` (`s_ra_nfkc`, `x4_t1_thoat_ra`, `x6_t1_ra`) — những chỗ cùng nuôi tham số `ra` mà khối #698 dùng;
   2 dò T-D (`s2_hong_va_khong_bq`, `x_f50_h_ge2`); 2 dò T-E (`z_exc_oserror_only`, `z_exc_subproc_only`).
3. **Tĩnh, cho cả 419:** vị trí mọi lần xuất hiện của mỏ neo trong ba cây (`goi/script/dump_probes.py`): **0** dò có mỏ neo nằm trong thân `t52`, `_in_tu_kiem_gom` hay `_ghi698` (ở cả ba cây — mọi mỏ neo ở mã bị đo), và số lần xuất hiện mỏ neo
   bằng nhau ở `nen`, `g2`, `ung` cho cả 419 dò (không dò nào lệch). Với 470 mục `DOT_BIEN`: số lần xuất hiện mỏ neo trong tệp đích của **ứng viên == g2 == nền** (mục cũ) cho mọi mục, và **= 1** cho cả 286 mục đích `ops/cong_cu_test.py`
   (`goi/script/dump_db.py`); Phụ lục F (A5 pre-check) rc=0 `dem_neo {"muc":470,"lech":0}` (§2.4).

### 4.2 Kết quả động: 67 dò × 2 cây = 134 lượt `_do_ban_kinh`

`script/probe_driver.sh` (bản ghép `do_dot_bien_r6.py` nguyên bản + `_do_ban_kinh`/`_ket_luan_ban_kinh` của chính cây; hạng bằng hàm `hang`/`tap` của Phụ lục D nạp bằng `exec`, không chép):
với MỖI dò chạy `g2` rồi `ung` liên tiếp trong cùng worker (hai hàng đợi `xargs -P 2`, tổng ≤ 4 tiến trình).

```
$ python3 goi/script/agg_probes.py .
so do co ca hai cay: 67 | chi g2: 0 | chi ung: 0
hang g2 : {'SONG': 17, 'GIET': 47, 'KHAC': 3}
hang ung: {'SONG': 17, 'GIET': 47, 'KHAC': 3}
LECH (hang khac hoac tap ca chet khac): []
so_neo g2: {1: 67} | ung: {1: 67}
theo tap (ung): {'KHAI': {'SONG': 5}, 'NGOAI': {'SONG': 9}, 'T-B': {'SONG': 2, 'KHAC': 1}, 'T-C': {'GIET': 43, 'KHAC': 2, 'SONG': 1}, 'T-D': {'GIET': 2}, 'T-E': {'GIET': 2}}
```
- **g2 = ứng viên từng dò: hạng bằng nhau 67/67 VÀ tập ca chết (`khong_qua`) bằng nhau 67/67.** Không dò nào đổi hạng, không dò nào mất bán kính 1, không `tin_dung_gia` mới.
- **Bộ ghi T4/T5 (36 dò T-C `t52`): 34 GIẾT**, đúng ca đích `t52_…`, bán kính 1, qua `_ghi698` trong cửa con (gồm `x_wr_ra_nfkc`, `x3_wr5_nfkc`, `x4_t4_*`, `x4_t5_*`, `y4_t4_*`, `x6_t4_ra`);
  1 SỐNG tương đương đã khai (`x3_wr5_normpath`) và 1 KHÁC đối chứng đã khai (`x3_wr_ra_lower`, `tin_dung_gia`).
- **9 dò ngoài lớp `t52`** (`g_cf_head`, `g_nfkc_head`, `g_strip_head`, `g_tab_head`, `x3_cua_nfkc`, `x3_cua_strip`, `x3_gop_dir_nfkc`, `x3_gop_dir_normpath`, `x3_gop_dir_strip`): cả 9 SỐNG, đúng khai của §2/§6.
- **22 đối chứng:** GIẾT 13 (`s2_hong_va_khong_bq`, `s_ra_nfkc`, `x3_m3a_ra_nfkc`, `x3_m3b_ra_cf`, `x4_t1_thoat_ra`, `x4_t2_thoat_ra`, `x6_t1_ra`, `x6_t2_ra`, `x_f50_h_ge2`, `x_main_ra_nfkc`, `x_main_ra_normpath`, `z_exc_oserror_only`, `z_exc_subproc_only`);
  SỐNG 7 (5 KHAI + `m_nfkc_khac_bmp_mh` + `m_nfkc_no_bk`, đúng khai); KHÁC 2 (`s_ra_realpath`, `x3_cat_ll_bk`, đúng khai "KHÁC bán kính 2"/đối chứng). Cả ba KHÁC của bảng 397/19/3 (`s_ra_realpath`, `x3_wr_ra_lower`, `x3_cat_ll_bk`) có mặt và khớp.
- Độ phủ: 67/419 dò (16,0 %), gồm **100 %** dò có ca đích `t52_`. 352 dò còn lại **KHÔNG ĐO ĐƯỢC** bởi tôi; lập luận cho chúng là (b) ở trên cộng bằng nhau về mỏ neo, không phải phép đo.


### 4.3 Bán kính của mục `DOT_BIEN` có ca đích `t52_` (A5, mẫu có lý do): 67 mục = toàn bộ họ `t52_` (65 cũ + 2 canh mới `w698_*`)
`script/db_queue.sh` + `script/db_run.py`: chính `_do_ban_kinh` + `_ket_luan_ban_kinh` của từng cây (3.12), hai worker mỗi cây, TMPDIR riêng. Đây là phép đo trực tiếp "mọi mục mà `t52` phải giết còn bị giết đúng, bán kính 1/56, trên cây ứng viên thật".

- **ỨNG VIÊN (cây Linux thật)**: 67/67 mục đã chạy; `ok … giết đúng ca đích · bán kính 1/56` = **67**; không ok = **0**; chạy lại (do sự cố `/dev/null`, §8) = 2 mục; thiếu = 0
- **CÂY MÔ PHỎNG QUYẾT ĐỊNH `nt`**: 67/67 mục đã chạy; `ok … giết đúng ca đích · bán kính 1/56` = **65**; không ok = **2**; chạy lại (do sự cố `/dev/null`, §8) = 4 mục; thiếu = 0
    - `w698_x_wr_ra_nfkc` → dich_tt=`qua` khong_qua={} · `  ĐỎ  w698_x_wr_ra_nfkc: đích 't52_gom_manh_phai_DO_khi_thieu_trung_lech_va_moi_chot_co_THE_RIENG' vẫn XANH ⇒ đột biến không giết được gì`
    - `w698_x3_wr5_nfkc` → dich_tt=`qua` khong_qua={} · `  ĐỎ  w698_x3_wr5_nfkc: đích 't52_gom_manh_phai_DO_khi_thieu_trung_lech_va_moi_chot_co_THE_RIENG' vẫn XANH ⇒ đột biến không giết được gì`

- **Ứng viên: 67/67 `ok … giết đúng 't52_…' · bán kính 1/56`** — 65 mục cũ (họ `g668_*`, `f*`, `bn_*`…) và hai canh `w698_x_wr_ra_nfkc`, `w698_x3_wr5_nfkc`. Không `tin_dung_gia`, không bán kính > 1, không `LOI_DUNG` ⇒ S4 không kích hoạt trong phần đã đo.
- `ntsim`: 65/67; hai mục không ok là hai canh của lớp P3 thứ nhất (§1.5) — 65 mục cũ vẫn giết đúng ca đích.
- **Sự cố làm bẩn 6 lượt đầu và cách xử lý:** sáu mục (ung 2: `g668_gom_bo_phien_ban`, `g668_gom_bo_sha`; ntsim 4: `g668_gom_bo_head`, `g668_gom_bo_tep_thuong` cùng hai canh `w698_*`) ra không-ok ở lượt đầu; bốn mục `g668_*` kèm `giết THÊM ['t37_…']`/`['t43_…']` hoặc `t43_… chết bằng lỗi VÔ CAN` — đúng các ca chạy `git`/`bash` trong cây tạm, và là mục ĐẦU hàng đợi của mỗi worker, tức chạy đúng lúc tôi lỡ xoá `/dev/null` (§8; jsonl không có dấu thời gian từng mục nên đây là suy luận từ vị trí và loại ca). Chạy lại cả sáu trên môi trường sạch: bốn mục `g668_*` thành `ok … 1/56` (xác nhận nhiễu); hai canh ở `ntsim` vẫn `vẫn XANH` (lặp được, không phải nhiễu). Mục `ok` ở lượt đầu không cần chạy lại: nhiễu chỉ có thể làm ca chết thêm hoặc đích chết sai lý do, mà cả hai đều hiện thành không-ok.

## 5. Phân lớp — lớp mở

P1 = không land hợp lệ / hồi quy / CI không xanh hợp lệ / mâu thuẫn đặc tả · P2 = tiêu chí không đạt / kiểm không răng / lời khai rộng hơn phép đo · P3 = chính xác hoá (như lượt 1). Ngưỡng chủ kho: 0 P1 và 0 P2 là đạt; P3 liệt kê, không chặn.
**0 P1 · 0 P2 · 3 P3 = 3 lớp mở.**

| # | slug | hạng | một dòng | nơi mô tả hướng sửa |
|---|---|---|---|---|
| 1 | `windows-hai-canh-t52-khong-do-duoc-nhung-bao-van-xanh` | P3 | Trên `nt` khối không chạy, hai canh `w698_x_wr_ra_nfkc`/`w698_x3_wr5_nfkc` (ca đích `t52_`) vẫn đăng ký vô điều kiện ⇒ "không đo được" nhưng báo "đích vẫn XANH" (sai chẩn đoán); vòng bán kính lane Windows đỏ ở mảnh 6, 7, gom | HINT hunk 2 (trước `_TRUOC_NANG_LUC`) |
| 2 | `chot-nen-nt-ba-cua-noi-chi-song-tren-linux` | P3 | Quyết định "nền nào" đọc ở ba chỗ độc lập (mặc định `ten_nen=os.name`, nơi gọi, nhánh `nt` của cha); kiểm mới chỉ đo chốt bên trong ⇒ 5 đột biến SỐNG, mỗi cái tái mở P1/đỏ trên Windows mà Linux không thấy | HINT hunk 1 (cạnh câu `bang`) |
| 3 | `khoi-phuc-ket-thuc-manh-sau-mo-phong-nt-khong-co-chot` | P3 | Bỏ `finally` khôi phục `_ket_thuc_manh` ⇒ 56/56 ca vẫn `qua` nhưng tên toàn cục còn là `<lambda>`; chỉ lộ ở CI (`main()` chế độ mảnh gọi tên ấy) | HINT hunk 1 (cạnh `try:`) |

### Lớp 1 — `windows-hai-canh-t52-khong-do-duoc-nhung-bao-van-xanh` (P3)
Bằng chứng: §1.5 (67 mục × 2 cây; hai dòng `ĐỎ … vẫn XANH` ở `ntsim`, hai dòng `ok … 1/56` ở `ung`; tiền lệ `t48`: hai dòng `KHÔNG_ĐO_ĐƯỢC … bị BỎ QUA`), tái lập: `script/db_run.py <cây> <ra.jsonl> w698_x_wr_ra_nfkc w698_x3_wr5_nfkc` trên `ung` và `ntsim`.
Vì sao không P2: §1.5 (tiền lệ `t48`; lane Windows tắt theo Q8, không phải trạng thái xanh đã thiết lập). Hướng sửa (**chỉ mô tả**; chủ kho chọn một):
- **(a)** đăng ký hai canh CHỈ ở nền chạy khối, theo đúng idiom `_CO_SYMLINK` của F24–F41, từ MỘT nguồn nền chung với `_ghi698`; kèm mở rộng oracle năng lực của `t52` và một đột biến riêng cho từng tên có điều kiện (F37/F41).
  Lưu ý đụng vùng F43–F48 (registry năng lực, nợ `registry-nang-luc-ngoai-cua-so`, Q1): cần chủ kho xác nhận phạm vi.
- **(b)** thay vì bỏ qua, chạy trên `nt` các ô chỉ gồm tên HỢP LỆ của Windows (loại ký tự cấm và dấu chấm/khoảng trắng cuối khỏi từng ô) để hai canh vẫn có kịch bản giết; **KHÔNG ĐO ĐƯỢC tại đây** vì cần một lần chạy Windows thật (Q8) — không nên chọn nếu Windows vẫn tắt.
- **(c)** giữ bỏ qua, khai vào nợ `windows-chua-do-o-moi-wp698` rằng trên `nt` hai canh này là "không đo được" (lane Windows đỏ ở mảnh 6/8, 7/8 và gom, cùng họ với hai mục `t48_`) và không bật lane Windows cho PR #721. Rẻ nhất; đóng lớp bằng hồ sơ.

### Lớp 2 — `chot-nen-nt-ba-cua-noi-chi-song-tren-linux` (P3)
Bằng chứng: bảng §3 — SỐNG: `mac_dinh_posix`, `mac_dinh_none`, `noi_goi_posix`, `cha_nhanh_chet`, `cha_nhanh_nt_sai_gia_tri`; CHẾT: `mac_dinh_nt`, `noi_goi_nt`, `cha_nhanh_dao`.
Executor khai cửa mặc định ("không kiểm nào bắt trên Linux") và "nhánh `nt` của `bang` chưa từng chạy"; không khai rõ nơi gọi ghim nền, cũng không đếm rằng cả năm đột biến sống đều tái mở lỗi trên Windows. Đây là giới hạn cố hữu khi không có Windows, nhưng nó **thu hẹp được**: đưa quyết định về một nguồn do tệp test nắm
(cha và con cùng đọc) và cho kiểm mô phỏng đi qua đúng nguồn ấy thì ba cửa có đột biến riêng chết được trên Linux. Nếu không làm, khai thẳng "chỉ đo chốt, không đo dây nối".

### Lớp 3 — `khoi-phuc-ket-thuc-manh-sau-mo-phong-nt-khong-co-chot` (P3)
Bằng chứng (đo): đột biến `khoi_phuc_bi_go` (`finally: pass`) ⇒ 56/56 ca `qua` (§3); sau khi chạy riêng `t52`, `script/ro_ham.py`:
```
{"cay": "ung",           "t52": "qua", "ten_truoc": "_ket_thuc_manh", "ten_sau": "_ket_thuc_manh", "cung_doi_tuong": true}
{"cay": "mut_khoi_phuc", "t52": "qua", "ten_truoc": "_ket_thuc_manh", "ten_sau": "<lambda>",       "cung_doi_tuong": false}
```
Hệ quả (đọc mã, không đo end-to-end): `main()` chế độ mảnh gọi `_ket_thuc_manh` theo tên toàn cục sau vòng ca ⇒ gọi bộ ghi giả, không ghi tệp mảnh ⇒ `upload-artifact` đỏ và gom thiếu mảnh — chỉ lộ ở CI. Hướng: một chốt riêng ngay sau khối (tên toàn cục vẫn là hàm thật),
hoặc không tráo tên toàn cục (truyền hàm ghi giả vào `_ghi698` qua tham số).

### Mốc ĐÃ đóng (không phải lớp)
P1 của bot ở mức `t52` (R1 → R3); chốt có răng đúng ca (`TinHieuChotCa` mang tên `t52_…`, bán kính 1/56, §3); không đổi hành vi Linux (§2, §4); A4-d/S1/S5 (§2.3).

## 6. Ghi nhận không thành lớp (đo được, nhưng không phải lỗi của bản vá theo chữ r14)

**N1 — "KQ ba cửa con TRÙNG g2 từng byte" (thông điệp commit, BAO_CAO §Số đo) chỉ đúng chữ cho cửa `main`.** Đo ở §2.5: `--tu-kiem-main` trùng từng byte (2 697 714 B, 508 khoá, băm dòng bằng nhau);
`--tu-kiem-gom` khác đúng ở tên thư mục tạm có hậu tố ngẫu nhiên `gom668_xxxxxxxx` và tên thư mục `TMPDIR` — **trùng sau khi chuẩn hoá chỉ ba thứ ấy**; `--tu-kiem-che-do` khác ở khoá `byte` (`byte.thuc` là sha256 của CHÍNH tệp test, nên không thể trùng giữa hai blob khác nhau) và
đường dẫn gốc cây. Đây là cùng kết luận lượt 1 đã ghi cho g1→g2. Cách chuẩn hoá của executor (số byte `11420/2697714/50236`) **KHÔNG ĐO ĐƯỢC** từ gói (không có `so_kq_cua.py`); số byte `che-do`/`gom` của tôi khác vì đường dẫn gốc cây dài khác (cùng độ dài sau chuẩn hoá). Không thành lớp: không
đo được khác biệt hành vi nào.

**N2 — A7 ("mọi chỗ thêm có chú thích neo #698"):** `grep -n -E "đã đóng|ĐÃ ĐÓNG|mọi |MỌI |trọn|TRỌN|không còn|KHÔNG còn"` trên **dòng thêm** (50) và **dòng xoá** (30) của diff g2→ứng viên: 0 dòng khớp ở cả hai phía; 0 ký tự CR/điều khiển/TAB trong dòng thêm.
`_ghi698` mang `# #698 M2b T4/T5 (…)`; hai chú thích mới trong `t52` mang `PR #721` và đứng ngay dưới dòng `# #698 M2b T4/T5` có sẵn — đọc theo khối như tiền lệ N3 của lượt 1, không thành lớp.

**N3 — `A4 (c)`, `A9`, `A10 (i)` KHÔNG đo lại; chi phí g2 → ứng viên ĐO bằng Phụ lục I.** Diff g2→ứng viên chỉ chạm `ops/cong_cu_test.py` (50/30), không chạm `ci.yml`, `ops/ci_duong_nhanh_test.py` hay `.claude/dev/ci_dang_ky_test.py` (chỉ nhắc tên tệp, không băm nội dung `cong_cu_test.py`) nên A4 (c) không được chạy lại.
Chi phí: `chi_phi_r4.py <g2> <ung>` (3.12, máy yên: loadavg đầu 0,17; `loi_khac_dung` 0,06 lõi), rc=0, `loi: []`: số lời lớn gọi `_van_tay` **67 = 67** (122 474 lời gọi cả hai); Δ_CPU (ứng viên − g2, tổng min ba ca) = **+0,35 s** = t52 +0,43 · t53 −0,05 · t54 −0,03; C56 = 25,89 s; **r = 1,0135** (trần 1,35). 
Dấu của Δ khác con số executor khai (`4,39 → 4,14 s`, ứng viên nhanh hơn 0,25 s) nhưng cùng cỡ nhiễu: ba mẫu CPU của `t52` trên g2 là 4,97 · 5,93 · 5,78 s, trên ứng viên 5,40 · 5,46 · 5,49 s (trung vị 5,78 ↔ 5,46). Kết luận: **không có bằng chứng hồi quy chi phí** (≤ 1,4 % C56, trong nhiễu); phần thêm chạy một lần mỗi `t52` (một `TemporaryDirectory` và một lời gọi về sớm).
`A9` (thời gian tường một mảnh trên 2 lõi) và `A10 (i)` (so với g1) **không đo lại**: phép đo thật vẫn là lượt CI 2 (S10, chủ kho duyệt riêng).

**N4 — `cam` chỉ lọc ký tự, không lọc quy tắc tên của Windows** (tên thiết bị `CON`/`NUL`…, dấu chấm/khoảng trắng cuối). Hợp lý: chốt thật là `ra_nt == [0, [], 0]` và việc bộ ghi KHÔNG bị gọi (đột biến `chot_muon`); danh sách ký tự chỉ là chứng cứ thứ hai.
Không thành lớp.

**N5 — lượt tự đo có rò thư mục tạm** (mỗi `_do_ban_kinh` để lại ~1,4 MB trong `TMPDIR`, đã thấy ở lượt 1, không do bản vá). Tôi đặt `TMPDIR` riêng từng tiến trình và dọn bằng `shutil.rmtree` cuối phiên.

## 7. KHÔNG ĐO ĐƯỢC / giới hạn

- **Windows thật** (Q8): mọi kết luận về Windows ở §1 là **mô phỏng quyết định nền** (`ntsim`) và **mô phỏng luật tên** (shim) trên Linux, cộng lập luận từ mã. Chưa có lượt nào của `t52` hay của vòng bán kính chạy trên `windows-latest` cho bản này.
  Trạng thái `t52` trên Windows ở nền `fc852ff` cũng KHÔNG ĐO ĐƯỢC từ gói (nên "trước g1 xanh" là điều tôi không khẳng định).
- **Bình luận P1 thật của bot** (`discussion_r4238165679`), trạng thái PR #721, S2/S3/S10 phía GitHub, danh tính người ký comment: không dùng mạng ⇒ không đọc.
- **Độ phủ**: 67/419 dò (100 % dò có ca đích `t52_`) và 67/470 mục `DOT_BIEN` (100 % mục đích `t52_`); 352 dò và 403 mục còn lại chỉ có lập luận (miền bản vá không chạm) + phép tĩnh bằng nhau về mỏ neo, không có phép đo động. Tám mảnh A5 trọn: không chạy.
- **Python**: suite `manh` ở 3.11/3.12/3.13; mọi phép đo động còn lại ở 3.12.3 (cửa con ở 3.11/3.13 — §2.5).
- **effort/model thực** của executor và của tôi: không đọc được từ bên trong phiên.


## 8. Ghi chú quy trình (độ lệch so với PROMPT, nói thẳng)
1. **Sự cố tự gây: tôi xoá nhầm `/dev/null`.** Một lệnh của tôi (lúc chạy thử `patch` cho HINT, khoảng 16:48:40Z) có dòng thừa `rm -f /dev/null`; trong container tôi là root nên nút thiết bị bị xoá, và các `> /dev/null` kế tiếp tạo ra một tệp thường 48 B thay cho nó. Lệnh kế tiếp của tôi phát hiện (`stat`: `regular file`),
   tôi tạo lại bằng `rm -f /dev/null && mknod -m 666 /dev/null c 1 3` (xác nhận `character special file 1:3`, ghi/đọc đúng) lúc ≈16:49:05Z — cửa sổ ≈20–30 giây. Ngoài `$R` (và `cay-kho`, không bị đụng), đây là thay đổi tệp-hệ-thống DUY NHẤT do tôi gây ra, và đã hoàn nguyên.
   Ảnh hưởng đo được: sáu lượt `DOT_BIEN` đang chạy trong cửa sổ ấy ra không-ok (ca `t37_`/`t43_` đọc `git`/`bash` chết hoặc bị giết thêm); **chạy lại sạch cả sáu** (§4.3) — bốn mục `g668_*` thành `ok`, hai canh `w698_*` ở `ntsim` vẫn đúng như lượt đầu. Mọi phép đo khác (suite, cửa con 3.12, 19 đột biến bản vá, sáu lượt shim R0–R4, 134 lượt dò) hoàn tất TRƯỚC 16:48Z;
   các phép đo SAU (một lượt R1 chạy lại để lấy tổng ô lệch, toàn bộ CA dưới shim, cửa con 3.11/3.13, `t48` dưới shim, HINT dry-run cuối) chạy sau khi đã sửa. `cay-kho` không bị đụng (`HEAD` và `status` kiểm lại sau sự cố: `5d889ba…`, 0 dòng).
2. **Tiến trình song song:** đỉnh 4 tiến trình Python đo + một vài lệnh ngắn trong tiền cảnh (`patch`, `git`, `ruff`, `python3 -c`) nên có lúc 5–6 tiến trình trong vài giây; mọi tiến trình con được `wait` (script `suite.sh`, `*_batch.sh`, `probe_queue.sh`, `db_queue.sh` đều `wait`). Lúc kết thúc không còn tiến trình đo nào chạy.
3. Dùng `git clone --shared` từ `cay-kho` (chỉ đọc đối tượng, ghi `alternates` vào CLONE, không ghi vào `cay-kho`) và `cp -al` (liên kết cứng; tệp test được `unlink` rồi ghi mới, không ghi lên inode dùng chung). `$R` ≈ 1,1 GB trước khi dọn (< 2 GB).
4. **Đã làm khác lượt 1:** không có script lượt 1 trong gói, nên script của tôi (`goi/script/`) viết lại từ chữ đặc tả; tôi không ghim lõi (không `taskset`) vì không đo A9.
5. **Tác dụng phụ của một dò, đã dọn:** dò `x3_wr_ra_lower` (đột biến hạ chữ thường đường ra của bộ ghi, hạng KHÁC đã khai) ghi tệp mảnh vào đường dẫn viết thường nên tạo một thư mục `w.zkq2jp` (7 MB, chỉ chứa `td_pr_*_x3_wr_ra_lower/gom668_*`) cạnh thư mục làm việc `w.zkq2jP` — vẫn trong `$R`; đã `shutil.rmtree`.


## 9. Tái lập, và tệp trong `goi/`
`W` = thư mục `w.zkq2jP` (ghi ở `goi/so-lieu/W.txt`) chứa `nen`/`g2`/`ung`/`ntsim` (dựng lại: `git clone --shared cay-kho <cây> && git checkout <sha>`; `ntsim` = `ung` + đúng hai dòng đổi ở §1.3). `PY` = venv 3.11/3.12/3.13 (chỉ đọc), `env -i`, `PYTHONDONTWRITEBYTECODE=1`, `python -B`.
```
script/trich_pl.py SPEC.md <ra>                 # 14 phụ lục, kiểm sha256 tiêu đề
script/suite.sh                                 # §2.1: suite `manh` 3.11/3.12/3.13 (ung) + 3.12 (g2), 4 tiến trình song song
script/cua_kq.sh ; script/cua_kq_pv.sh 3.11|3.13 # §2.5: KQ ba cửa con g2 ↔ ung (PYTHONHASHSEED=0)
script/dump_db.py <cây> <ra.json> ; script/dump_probes.py …   # §4.1: mỏ neo 470 mục + 419 dò trên ba cây
Phụ lục F: (cd goi/so-lieu/pl && PY -B kiem_canh_r5.py $W/nen $W/ung ../bang_noi.txt do_dot_bien.py do_dot_bien_r6.py)   # §2.4
Phụ lục G: PY -B pl/giao_a4d_r3.py $W/ung fc852fff7da37f1669569572b79571446e61c294     ; Phụ lục E: PY -B pl/ast_dot_bien_r2.py $W/ung/ops/cong_cu_test.py
script/mut_ban_va.py $W/ung $W <ra.jsonl> <tmp> <tên…> ; script/tong_hop_mb.py goi/so-lieu/mb   # §3: 19 đột biến bản vá (toàn tệp)
script/win_t52.py <cây> (PYTHONPATH=script/shim)  # §1.3: R0–R4 (shim luật tên Windows, `sitecustomize.py`)
script/db_run.py <cây> <ra.jsonl> nen|<tên mục…>   # §1.3 (cả 56 ca), §1.5, §4.3 (PYTHONPATH=script/shim cho `nen` dưới shim và cho `t48_`)
script/probe_queue.sh 2 goi/so-lieu/ten_t52.txt ; … ten_ctl.txt ; script/agg_probes.py .   # §4.2: 67 dò × (g2, ung)
script/db_queue.sh <cây> 2 goi/so-lieu/ten_db_t52.txt <nhãn>     # §4.3: 67 mục DOT_BIEN đích t52_
script/ro_ham.py <cây> ; script/sinh_hint.py <tệp test ung> goi/HINT.patch    # lớp 3; sinh HINT (assert ast.dump bằng nhau)
Phụ lục I (N3): PY -B pl/chi_phi_r4.py $W/g2 $W/ung   # Δ_CPU g2→ứng viên; ra so-lieu/cpu/
script/tbl_md.py . suite|mb|shim|doors|db      # sinh các bảng Markdown của tệp này từ số liệu thô
```
Số liệu thô: `so-lieu/{suite,cua,cua_3.11,cua_3.13,mb,win,probes,db,cpu,pl}/`, `so-lieu/probes_tonghop.json`, `so-lieu/static.txt`, `so-lieu/hint_dryrun.txt`.

**Lớp mở ⇒ `goi/HINT.patch`.** sha256 ghi ở dòng cuối báo cáo của phiên điều phối (và trong tệp `so-lieu/hint_dryrun.txt`). Dry-run (cây gốc = bản sao của `ops/cong_cu_test.py` ứng viên, băm `a9c2a836735ab757…` trước và sau, không đổi):
```
sha256 HINT.patch: aeae786e5f18e5a60dbf1bb49d35b56d4d700c1fc3ba6120a243d760fc671654   (4542 B, 2 hunk, 24 dong them, 0 dong xoa)
blob/sha256 tep goc (ung): git=f0fc96c1dcd3d21ee8e4737ec88226575c9209e8  sha256=a9c2a836735ab757…
=== (1) cd <goc cay> && patch -p0 --fuzz=0 --dry-run --verbose < HINT.patch
checking file ops/cong_cu_test.py
Using Plan A...
Hunk #1 succeeded at 6898.
Hunk #2 succeeded at 7524.
done
rc=0
=== (2) patch -p0 --fuzz=0 --dry-run --verbose cong_cu_test.py < HINT.patch   (chi dinh tep, nhu luot 1)
checking file cong_cu_test.py
Using Plan A...
Hunk #1 succeeded at 6898.
Hunk #2 succeeded at 7524.
done
rc=0
sha256 sau dry-run: a9c2a836735ab757… / a9c2a836735ab757…  (khong doi)
=== (3) git -C <clone ung> apply --check -p0 HINT.patch
rc=0
=== (4) ap THAT len ban sao (khong phai cay that) roi do: AST va bien dich
patch rc=0
ast.dump bang nhau: True | dong: 8646 -> 8670 | '# lop:' them: 3
compile OK
…/ap/ops/cong_cu_test.py:2662:5: F841 Local variable `ci` is assigned to but never used
Found 1 error.
No fixes available (1 hidden fix can be enabled with the `--unsafe-fixes` option).
```
