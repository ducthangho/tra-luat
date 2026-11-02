# Đặc tả packet `CI-DUONG-NHANH-BO-DOT-BIEN` r1: đường nhanh chỉ chạy ca của harness, không chạy 419 đột biến (vá A12 của #1113)

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab
dieu_kien_merge: ADR-0060@36d7c5dcdcbbb27176b75135125b9009f9fe0587

| trường | giá trị |
|---|---|
| packet_id | `CI-DUONG-NHANH-BO-DOT-BIEN`, revision 1, generation 1 |
| packet_issue | ghi ở comment đầu của Issue mở cùng đặc tả này |
| nguon_cap_viec | packet khắc phục của #1113 (`CI-LAN-LUU-TRU` r1, merge `c165a5d0` qua PR #1128). Hồ sơ `ops/land/pr1128-wp1113-land-evidence.yaml` mục `canary_a12`: `ket_qua: TRUOT`, `quyet_dinh_chu_kho: 'ha landed, mo packet va (bo dot bien cua harness tren duong nhanh …)'`. Chủ kho chốt Q1–Q6 qua hai vòng hỏi ngày 02-11-2026 trong phiên `session_015GtxrayCW1gNgN8F8GiVev` |
| review_class | `sensitive`: chạm `.github/workflows/ci.yml` (§8, *workflow/CI authority*) |
| base | `origin/master` lúc cấp lease, và **phải chứa merge của #1132** (§3). Đo khi soạn, 02-11 ~02:00Z: `9091cf5`, #1132 chưa land |
| executor / reviewer | `anthropic_claude`, chính phiên soạn spec / `openai_codex` qua `launcher.py run` trên clone độc lập, và connector `@codex review` trên PR draft |
| windows | `not_required`, **do chủ kho quyết** (Q4). Lý do: bước bị sửa có `if: runner.os == 'Linux'`, không chạy trên Windows |
| full_mutant_audit | bắt buộc (M9: diff chạm `.github/workflows/**` và `ops/**/*.py`) |

## 1. Vì sao: số đo

| # | sự kiện | số đo |
|---|---|---|
| S1 | canary A12 của #1113: PR #1140, run `41371625809` (`pull_request`, `che_do=duong_nhanh`) | tổng `completed_at − started_at` của 16 job = **1159 s** (≈ 19,3 phút) > trần 12 phút. Nguồn: `ops/land/pr1128-wp1113-provenance/readback-jobs-41371625809-canary-a12.json` (nhánh `claude/ghi-so-land-1113`) |
| S2 | phân rã S1 (cùng tệp) | `gate-ops` **966 s**: bước `ci-duong-nhanh selftest (phan loai diff + khoa cau truc if)` **636 s**, bước `bien-nhan v2 selftest` **303 s**, phần còn lại của job 27 s. 15 job kia cộng lại **193 s** (mỗi job 10–19 s; `gate-cong-cu` 0 s) |
| S3 | `ops/ci_duong_nhanh_test.py` trên `9091cf5` | **113** ca (`CA`) · **419** đột biến (`DOT_BIEN`) · tự kiểm phân hạng 5 mẫu rc + 3 đột biến thật. `main` không có cờ chỉ-chạy-ca (chỉ có `--mot-ca`, `--nguon-test`) |
| S4 | đo tại chỗ, container Linux 4 nhân, kho đã mở sâu, 02-11 ~01:55Z | 113 ca chạy tuần tự qua `chay_ca_trong_tien_trinh`: **104 s**, 113/113 đạt; riêng `t56_dau_do_bi_bat_tren_duong_nhanh` **72 s**; `t22` 9 s; còn lại ≤ 6 s mỗi ca. `tu_kiem_phan_hang()`: **1,8 s**. `ops/bien_nhan_v2_test.py`: **373 s**, `98/98 ca · 153/153 đột biến`, `TỔNG: ĐẠT` |
| S5 | ước tính sau vá (suy, chưa đo) | hệ số CI/tại chỗ ≈ 303/373 ≈ 0,8 (đo trên `bien_nhan_v2_test`) ⇒ 113 ca ≈ 85 s trên CI. Tổng ≈ 193 + 27 + 85 + 2 + 303 ≈ **610 s ≈ 10,2 phút**, dư ≈ 1,8 phút dưới trần. Biên mỏng ⇒ A6 đo tiền-canary trước merge |
| S6 | trạng thái cục bộ dễ đọc nhầm | trên clone **nông**, `t56` đỏ (`doc-claims-check strict: 2`) và `bien_nhan_v2_test` ra 94/98 (`kho nông … không đo được quan hệ tổ tiên`). Mở sâu kho thì cả hai xanh. Đo các bộ này phải trên kho đầy đủ |

**Vì sao bỏ đột biến ở đường nhanh là an toàn:** `che_do=duong_nhanh` chỉ được cấp khi mọi tệp đổi nằm dưới bốn tiền tố hồ sơ (`ops/{land,leases,reviews,specs}/**`), nên diff ấy **không đổi được** `ops/ci_duong_nhanh.py`, `ops/ci_duong_nhanh_test.py` hay `ci.yml`. 419 đột biến đo răng của MÃ bộ phân loại và của các `if:`; mã ấy đã được đo đủ ở lượt PR đã đổi nó (đường đầy đủ). Các **ca** thì vẫn phải chạy: `t56` chính là phép đo A7c (đầu dò DO1–DO6 trên dữ liệu thật của cây).

## 2. Thay đổi

### 2.1 `.github/workflows/ci.yml`

Bước `ci-duong-nhanh selftest (phan loai diff + khoa cau truc if)` của job `gate-ops`: **giữ** tên, `if: runner.os == 'Linux'` và `run: python ops/ci_duong_nhanh_test.py`. Chỉ thêm:

```
        env:
          CI_DUONG_NHANH_CHE_DO: ${{ needs.chuan-bi.outputs.che_do }}
```

Chú thích phía trên bước viết lại cho đúng hành vi mới: đường nhanh chạy đủ ca, bỏ đột biến; mọi giá trị khác chạy đủ. Chú thích **không** chứa cú pháp biểu thức Actions (bài học `ops-don-ref.yml`, run `31971137920`). Bước vẫn **không** có `if:` theo `che_do`.

### 2.2 `ops/ci_duong_nhanh_test.py`

1. Hàm thuần `che_do_harness(env) -> str`: trả `"chi_ca"` **chỉ khi** `env.get("CI_DUONG_NHANH_CHE_DO")` là `str` và **bằng đúng** `"duong_nhanh"` (không strip, không lower); mọi trường hợp khác — vắng, rỗng, `"day_du"`, `"Duong_nhanh"`, `"duong_nhanh "`, giá trị lạ — trả `"day_du"` (fail-close về đường đầy đủ).
2. `main([])`: gọi `che_do_harness(os.environ)`. Nhánh `"day_du"` giữ nguyên hành vi hiện tại từng dòng. Nhánh `"chi_ca"`: chạy đủ mọi ca của `CA` và `tu_kiem_phan_hang()`; KHÔNG gọi `chay_tap_dot_bien`; in đúng dòng `DOT BIEN: BO QUA {len(DOT_BIEN)} (che_do=duong_nhanh)` thay cho dòng `DOT BIEN: m/n …`; `TONG: DAT` (rc 0) khi và chỉ khi mọi ca đạt, `len(CA) > 0`, tự kiểm đạt, và không tên đột biến trùng. Dòng `CA:` và `KIEM KE:` in như cũ.
3. Tiến trình con do harness sinh (`chay_ca_trong_tien_trinh`, `chay_mot_dot_bien` và mọi chỗ khác harness gọi lại chính tệp test) **không** thừa kế `CI_DUONG_NHANH_CHE_DO`: gỡ biến khỏi môi trường truyền cho con. Lý do: ca đo `main` (vd. `t91`) chạy trong con; con thừa kế `duong_nhanh` thì ca ấy đo nhánh sai.
4. Ca mới (tên đặt khi thi công, tiền tố `t`; khai đích trong `DOT_BIEN` như mọi ca):
   - **C1** bảng giá trị của `che_do_harness`: đúng `"duong_nhanh"` ⇒ `chi_ca`; vắng, `""`, `"day_du"`, `"Duong_nhanh"`, `"duong_nhanh "`, `" duong_nhanh"`, `"duong_nhanh\n"` ⇒ `day_du`.
   - **C2** `main` với runner giả (theo khuôn `t91`/`t92`): env vắng và env `day_du` ⇒ `chay_tap_dot_bien` được gọi **đúng một lần** với đối số có `len == len(DOT_BIEN)`, và đầu ra có dòng `DOT BIEN: {len}/{len}`; env `duong_nhanh` ⇒ **không** gọi, có dòng `DOT BIEN: BO QUA {len(DOT_BIEN)} (che_do=duong_nhanh)`, `rc == 0` khi ca giả đều đạt; một ca giả `DO` ⇒ `rc == 1` và `TONG: DO`; tự kiểm giả trả lỗi ⇒ `rc == 1`.
   - **C3** gỡ biến khỏi con: với env cha mang `CI_DUONG_NHANH_CHE_DO=duong_nhanh`, môi trường mà `chay_ca_trong_tien_trinh` và `chay_mot_dot_bien` truyền cho `subprocess` **không** chứa khoá ấy (đo bằng gián điệp trên lời gọi `subprocess`, không đo bằng đọc mã).
   - **C4** (cấu trúc `ci.yml`, tiền tố `y`): bước harness của `gate-ops` có `env` **bằng đúng** `{"CI_DUONG_NHANH_CHE_DO": "${{ needs.chuan-bi.outputs.che_do }}"}`, `run` bằng đúng `python ops/ci_duong_nhanh_test.py`, `if` bằng đúng `runner.os == 'Linux'`. Cập nhật `KHUNG_BUOC` cho khớp; `RUN_BUOC_PACKET`, `TAP_CHO_PHEP`, `BUOC_HARNESS` **không** đổi.
5. Đột biến mới trong `DOT_BIEN` (mỗi cái một đích, phải bị giết đúng lý do theo bộ phân hạng hiện có):
   - `M1` nới so sánh thành `.strip()` (hoặc `.lower()`) ⇒ C1 đỏ;
   - `M2` mặc định khi vắng biến là `"duong_nhanh"` ⇒ C1 và C2 đỏ;
   - `M3` nhánh `chi_ca` vẫn gọi `chay_tap_dot_bien` hoặc nhánh `day_du` không gọi ⇒ C2 đỏ;
   - `M4` nhánh `chi_ca` bỏ điều kiện "mọi ca đạt" khỏi `TONG` ⇒ C2 đỏ;
   - `M5` bỏ việc gỡ biến khỏi môi trường con ⇒ C3 đỏ;
   - `M6` (đột biến `ci.yml`) giá trị `env` thành chuỗi hằng `duong_nhanh` ⇒ C4 đỏ;
   - `M7` (đột biến `ci.yml`) xoá khối `env` ⇒ C4 đỏ.

## 3. Write set

`.github/workflows/ci.yml` · `ops/ci_duong_nhanh_test.py` · `ops/specs/CI-DUONG-NHANH-BO-DOT-BIEN-r1.md` (chép **nguyên byte** từ nhánh lease vào commit đầu của nhánh thực thi). **Ba tệp**, đếm theo `git diff --numstat <base> <H>`. Trần (chủ kho, Q4): **≤ 150 dòng thêm trên hai tệp mã** (`ci.yml` + `ops/ci_duong_nhanh_test.py`); tệp đặc tả không tính vào 150 vì nó chép nguyên byte. Trong trần `ADR-0053` (6 tệp / 450 dòng thêm) kể cả khi cộng tệp đặc tả.

**Đụng lease (đo 02-11 ~01:58Z bằng `python ops/lease_publish.py ai-dang-giu`, sau khi so `ls-remote` = `for-each-ref`, thiếu 0):** lease `ci-concurrency-master-r1-g1-claude-remote-20261102` (#1132, `CÒN_HẠN` tới `2026-11-03T01:29:00Z`) giữ **cả** `.github/workflows/ci.yml` lẫn `ops/ci_duong_nhanh_test.py`; nhánh `agent/wp1132-g1-claude` đã có commit `024212c` sửa hai tệp ấy. Quyết định (Q1): đặc tả đóng băng ngay; **lease của packet này chỉ được cấp khi #1132 đã land hoặc đã nhả lease** (rút hạn/bia mộ), và base phải chứa merge của #1132. Trước khi cấp, chạy lại `ai-dang-giu` cho ba đường dẫn ⇒ phải ra `NGƯỜI_GIỮ 0`. Packet DO6 (`scripts/tl_core/workflow.py`) không giao write set này.

## 4. Nghiệm thu

| # | tiêu chí | phép đo làm ĐỎ |
|---|---|---|
| A1 | `python ops/ci_duong_nhanh_test.py` (env **vắng**, kho đầy đủ) ra `CA: N/N dat` với N = 113 + số ca mới (≥ 4), `DOT BIEN: M/M bi giet dung ly do` với **M = 419 + số đột biến mới (≥ 7)**, `TONG: DAT`. Ghi N, M thật vào biên bản | ca đỏ; hai số không bằng nhau; **M < 419 + 7** (bản vá đã làm rơi đột biến ở đường đầy đủ) |
| A2 | cùng lệnh với `CI_DUONG_NHANH_CHE_DO=day_du`: kết quả như A1 (cùng N, cùng M) | M khác A1 |
| A3 | cùng lệnh với `CI_DUONG_NHANH_CHE_DO=duong_nhanh`: `CA: N/N dat`, dòng `DOT BIEN: BO QUA M (che_do=duong_nhanh)` với **cùng M** của A1, `TONG: DAT`, rc 0; thời lượng tại chỗ ghi vào biên bản (S4 là mốc 104 s) | thiếu dòng `BO QUA`; có dòng `bi giet`; M lệch A1 |
| A4 | đo nền: ca C1–C4 viết trước, chạy trên mã **base** (chưa sửa) ⇒ C1/C2/C3 **ĐỎ hoặc HỎNG vì thiếu hàm**, C4 **ĐỎ** vì `ci.yml` base chưa có `env`. Ghi output | ca xanh trên base ⇒ ca không đo gì |
| A5 | bảy đột biến §2.2 mục 5 bị giết **đúng ca đích** (bộ phân hạng: `GIET`, không `TIN_DUNG_GIA`); 419 đột biến cũ vẫn `GIET` | một đột biến sống hoặc tín dụng giả |
| A6 | **tiền-canary trước bỏ draft** (Q3): PR nháp, base = nhánh thực thi tại head ứng viên, head = nhánh đo chỉ thêm **một** tệp `ops/land/**`. `ci.yml` không lọc nhánh ở `pull_request` nên lượt chạy dùng `ci.yml` mới. Đòi: log `chuan-bi` có `che_do=duong_nhanh`, log `gate-ops` có dòng `DOT BIEN: BO QUA`, tổng `completed_at − started_at` mọi job **≤ 11 phút** (chừa biên 1 phút cho A10), 0 job Windows chạy thật. Lưu readback jobs JSON vào biên bản; PR đo đóng sau khi đo, nhánh đo dọn bằng `ops-don-ref.yml` khi chủ kho duyệt | > 11 phút ⇒ **dừng, hỏi chủ kho** (phương án đã nêu ở Q3: bỏ thêm đột biến của `bien_nhan_v2_test`, tức mở rộng write set — không tự làm); thiếu `BO QUA` ⇒ đỏ |
| A7 | `actionlint` trên `ci.yml`: delta so `origin/master` = 0; ghi `shellcheck` có mặt hay vắng. Thiếu `actionlint` ⇒ `KHÔNG ĐO ĐƯỢC`, đỏ | finding mới |
| A8 | `git diff --numstat <base> <H>`: đúng ba tệp §3; tổng dòng thêm của `ci.yml` + `ops/ci_duong_nhanh_test.py` ≤ 150 | tệp thứ tư; > 150 |
| A9 | `ruff check --select F ops/ci_duong_nhanh_test.py` (Ruff 0.15.15): delta so base = 0. `doctrine-scan`, `adr-song`, `doc-claims-check`: delta = 0. `python .claude/dev/ci_dang_ky_test.py` (bộ chứa `BAM_GATE_*`) xanh trên head — packet không chạm hai job mà `BAM_GATE_*` băm; đổi băm ⇒ dừng, hỏi | delta > 0; `ci_dang_ky_test` đỏ |
| A10 | M9: một lượt `ci-dot-bien-du.yml` (`workflow_dispatch` trên nhánh thực thi) `success` tại head cuối; CI PR của ứng viên xanh (đường đầy đủ ⇒ log `gate-ops` có `DOT BIEN: M/M` với M của A1); `kiem-merge` trên PR ra rc 0 trước khi bỏ draft | run đỏ; log PR thiếu dòng `DOT BIEN: M/M` |
| A11 | **chưa đo được tới sau land — canary A12 MỚI** (Q5): PR hồ sơ land của chính packet này (chỉ `ops/{reviews,land}/**`). Ba run, mỗi run đo riêng: (a) run `pull_request` của PR ấy, (b) run push master của merge ấy, (c) một `workflow_dispatch` trên head của PR ấy (đúng vế dispatch của A12 gốc). Mỗi run: tổng `completed_at − started_at` mọi job **≤ 12 runner-phút**, **0** job `windows-latest` có `runner_id ≠ 0`, ba check bắt buộc `success`, log `chuan-bi` có `che_do=duong_nhanh`, log `kiem-re` của `gate-ops` báo đạt, log `gate-ops` có `CA: N/N` và `DOT BIEN: BO QUA`. Run (b) bị huỷ do concurrency ⇒ ghi `not_measured` cho (b) và dùng dispatch trên nhánh đo cùng merge SHA, không rerun trên master. Người đo: phiên này. Readback jobs JSON ghi vào hồ sơ land. Đạt cả ba ⇒ báo chủ kho để ghi `landed_<ngày>` cho **#1113** và cho packet này | một run > 12 phút; job Windows chạy thật; check bắt buộc vắng/`skipped`; log thiếu một trong các dòng trên |

## 5. Ngoài phạm vi

- **Đột biến của `ops/bien_nhan_v2_test.py`** (153 đột biến, 303 s trên CI): giữ nguyên (Q3). Chỉ mở lại khi A6 trượt, và khi đó là quyết định mới của chủ kho, write set mới.
- **`t56`** (≈ 72 s tại chỗ): giữ trên đường nhanh vì nó là phép đo A7c; không tối ưu ở packet này.
- **Các job khác** (193 s cộng lại): không đụng.
- **Ghi `landed` cho #1113**: việc bookkeeping của phiên land sau A11, không nằm trong diff của packet.
- **#1132** (concurrency master): packet riêng; packet này chỉ phụ thuộc thứ tự (§3).

## 6. `hinh_dang_ke_thua`

Packet khắc phục của #1113. Chép từ `ops/land/pr1128-wp1113-land-evidence.yaml` (nhánh `claude/ghi-so-land-1113`, mục `review` và `canary_a12`) và từ §8 của `ops/specs/CI-LAN-LUU-TRU-r1.md`:

- *tiêu chí chỉ đo được sau land mà không có phép đo trước merge* ⇒ trượt sau khi đã merge: **1** lần (A12 của #1113). Packet này đặt A6 (tiền-canary) để lần thứ hai không xảy ra theo cùng đường.
- finding review offline của #1113 theo lượt (P0/P1/P2/P3): r1 0/1/3/0 · r2 0/0/1/0 · r3 0/0/1/1 · r4 0/0/1/0 · r5 0/0/0/0 · r6 0/0/0/0; xử lý: F1 `bash` trần → `tim_bash` · F2 DO6 né sang `day_du` → `kiem-re` đo · F3 bảng `UY_NHIEM` · F4 trần dòng → lease g2. Mỗi hình dạng **1** lần, chưa hình dạng nào chạm ngưỡng ba.
- lớp đã lặp từ packet B (#1094), chép tiếp để quét sớm: *kiểm sau khi bộ phân tích đã chuẩn hoá* (**3** lượt) · *tin TÊN ref thay vì OID* (**2** lượt) · *`1 == True == 1.0`* (**2** lượt) ⇒ C1 so bằng `type(x) is str` rồi so chuỗi chính xác; C4 so cây YAML của `env` bằng đúng, không so chuỗi con.
- *đột biến chết vì ngoại lệ là tín dụng giả*: bộ phân hạng hiện có canh; ca mới không được bọc `except Exception` (ca `t99` quét AST).

## 7. `chua_do_duoc`

- Thời lượng 113 ca **trên runner CI**: chưa đo; S5 là suy từ hệ số 0,8. A6 đo thật trước merge.
- Dao động thời lượng `bien_nhan_v2_test` giữa các runner: một mẫu duy nhất (303 s). Nếu A6 đạt sát 11 phút thì A11 vẫn có thể trượt; khi ấy quay lại câu hỏi Q3.
- Phút tính tiền thật (billing) khác thời lượng job: A6/A11 đo thời lượng job, như A12 gốc.
- Ngày #1132 land: không đo được từ phiên này; nó quyết định lúc cấp lease (§3).
