# VERDICT lượt 8 — PR #689 / packet #677

- reviewer: Sonnet 5.5, effort high (tự khai)
- reviewed_sha: adad5f5f8f22263120edb1d80b64164159f041ab (cha 3c308b304d9bed46afba2ca698d94d7c31a77a01)
- sha256 SPEC-r8.md đo lại: 4dfbfd69e161d55aa28f2685741cdcf11fcd5171438081e9eb63815c69bb4094 (khớp lời khai)
- nhãn: advisory_review

## Mục 1 — diff-luot8.patch so luot7/HINT.patch
`cmp diff-luot8.patch luot7/HINT.patch` ⇒ BYTE-GIỐNG (sha256 HINT = 3928946c…9c1ae1 đo lại); `git diff 3c308b3 adad5f5 | cmp - diff-luot8.patch` ⇒ khớp. 3 hunk, +4/−2 (tệp duy nhất `ops/lease_publish_test.py`). Không lệch hunk nào.

## Mục 2 — L1 lượt 7 (t202, đột biến W1/W2) — ĐÓNG
Phương pháp: bản sao `mktemp -d -p $R` (copy nguyên `cay-kho`), ghi đè `ops/lease_publish_test.py` từ bản gốc mỗi đột biến (assert đúng 1 lần khớp chuỗi), chạy `python -B ops/lease_publish_test.py --chi-ca=t202`. Bản sao gốc khôi phục byte-exact (`cmp`).
Đột biến ở `_lech_m4` (dòng 10729): `kq["goi"]` → `kq["goi"][:4]` (W1) và `kq["goi"][-4:]` (W2).

| đột biến | hàng bị gỡ | t202 | đỏ bằng |
|---|---|---|---|
| (nền, không đột biến) | — | 1/1 QUA | — |
| W1 `[:4]` | không | 0/1 ĐỎ | `chot()` của t202: "…sai chiều: M4 thừa lời gọi phía sau" (đúng hàng "sau", không hàng khác) |
| W2 `[-4:]` | không | 0/1 ĐỎ | `chot()` của t202: "…M4 thừa lời gọi phía trước" (đúng hàng "trước") |
| W1 | gỡ "phía sau" | 1/1 QUA (W1 SỐNG) | — |
| W1 | gỡ "phía trước" | 0/1 ĐỎ | hàng "sau" còn lại giết W1 |
| W2 | gỡ "phía trước" | 1/1 QUA (W2 SỐNG) | — |
| W2 | gỡ "phía sau" | 0/1 ĐỎ | hàng "trước" còn lại giết W2 |
| W1 / W2 | gỡ cả hai hàng | 1/1 QUA (cả hai sống) | — |

Kết luận: mỗi hàng mới là chốt ĐỘC LẬP đúng W tương ứng, đột biến chỉ chết bằng assertion của chính t202 (thông điệp nêu tên hàng). L1 lượt 7: ĐÓNG. Không có finding.

## Mục 3 — L2 lượt 7 (`doc_pid`, tập `nguy`) — ĐÓNG (1 ghi chú P4 về phụ thuộc hình dạng runner)
Mã: `ops/lease_publish_test.py:6482` `nguy = {1, getpid, getppid, *getpgid(0), *getsid(0)}` — tính MỘT LẦN ở đầu thân t154 (mỗi lần t154 chạy, trong tiến trình đang chạy nó), đóng qua closure cho `doc_pid`; vòng tự kiểm dòng 6507 dựng lại dãy giá trị từ CHÍNH các lời gọi ấy (độc lập với `nguy`, không đọc `nguy`).

Phép đo (bản sao, `--chi-ca=t154`, cây tiến trình dựng bằng `shape.py` để pid/ppid/pgid/sid KHÁC NHAU: pid 21098 ppid 21097 pgid 21096 sid 21095):

| đột biến (chỉ phần tử bỏ khỏi `nguy` / khỏi vòng tự kiểm) | t154 | đỏ bằng |
|---|---|---|
| nền | 1/1 QUA | — |
| bỏ `1` khỏi nguy | 0/1 ĐỎ | `bang()` trong vòng tự kiểm: "doc_pid trả đích giết nguy hiểm 1" |
| bỏ pgid khỏi nguy | 0/1 ĐỎ | `bang()`: "…nguy hiểm <pgid>" |
| bỏ sid khỏi nguy | 0/1 ĐỎ | `bang()`: "…nguy hiểm <sid>" |
| bỏ `1` khỏi nguy VÀ khỏi vòng | 1/1 QUA (sống) | — (đúng: hàng vòng là chốt của phần tử) |
| bỏ pgid / sid khỏi nguy VÀ khỏi vòng | 1/1 QUA (sống) | — |
| chỉ bỏ khỏi vòng (nguy nguyên) | 1/1 QUA | — (tương đương hành vi: `doc_pid` vẫn chặn) |
| bỏ `1`+vòng-pgid / pgid+vòng-sid (lệch chéo) | 0/1 ĐỎ | hàng vòng của phần tử còn lại giết |

⇒ mỗi phần tử mới (1, pgid, sid) có chốt RIÊNG bằng `bang()` của t154; đột biến chỉ chết ở assertion của chính ca.

**Ghi chú P4 (hình dạng runner):** trong shell thường của sandbox này (`pid 21099 ppid 21090 pgid 21099 sid 21090` ⇒ pgid==pid, sid==ppid) đột biến bỏ pgid hoặc bỏ sid SỐNG (đo: `nguy-bo=g` và `=s` ⇒ 1/1 QUA; `=1` vẫn ĐỎ 0/1). Lý do: các số ấy trùng `getpid`/`getppid` nên tập không đổi. Vậy răng của hai phần tử này chỉ hiện khi runner có pgid, sid khác pid/ppid (kiểu cây ở trên). Đây là tính chất của chính bất biến (phần tử dư thừa khi trùng), không phải lỗi mã; chốt không-oan vẫn đúng. Không cần vá; chỉ ghi để lượt sau không đọc "sống" ở runner trùng số thành finding. Bản vá tuỳ chọn KHÔNG đề xuất (thêm ca dựng cây tiến trình = tăng dòng, trần 600 đã chạm).

**Đỏ oan?** (a) Trong lượt con `t125` (`_mo_con_nhom_rieng` ⇒ `start_new_session`, runner con là trưởng phiên: pgid==sid==pid): `nguy` = {1, pid, ppid} (tập dedup), vòng tự kiểm chạy các giá trị lặp — không đỏ (phần bao phủ: toàn suite ở mục 4, gồm [A]/[B] của t125, xanh). (b) PID con/cháu tình cờ trùng pgid/sid: cháu được sinh qua `_mo_con_nhom_rieng` (nhóm+phiên RIÊNG mới) và `Popen` từ con; PID của cháu là PID SỐNG khác, còn pgid/sid của runner là PID đang được nhóm/phiên của runner giữ — nhân Linux không cấp lại PID đang làm pgid/sid cho tiến trình khác, nên trùng là bất khả; KHÔNG ĐO ĐƯỢC bằng stress (chỉ lập luận nhân; không có cách ép tái dụng PID có kiểm soát ở đây). Đo được: t154 QUA ở nền trong shell thường, trong cây 4-số-khác-nhau (shape.py), và trong toàn suite ở cả lượt chính lẫn `[A]`/`[B]` của t125 (runner con là trưởng phiên: pgid==sid==pid) — xem mục 4.
**Nền không có getpgid/getsid (Windows):** `getattr(os,"getpgid",None)` ⇒ None, bị lọc bởi `if g` ⇒ `nguy={1,pid,ppid}`, vòng = 4 giá trị. Mô phỏng: xoá `getpgid/getsid/killpg/setsid` khỏi `os` rồi trích và `exec` đúng hai dòng (win.py): `nguy=[1, 22170, 22186]`, `vong=('0','1','22186','22170')`, không ném. Phần CHẠY THẬT trên Windows (t154 đủ: `taskkill`, `CREATE_NEW_PROCESS_GROUP`) KHÔNG ĐO ĐƯỢC: không có máy Windows ở sandbox này; mô phỏng chỉ phủ 2 dòng mới, không phủ cả ca.

## Mục 4 — Hồi quy (bản sao `mktemp -d -p $R`, `PYTHONDONTWRITEBYTECODE=1`, Linux 4 CPU, python 3.11, ruff 0.15.8)
- **Toàn suite** `python -B ops/lease_publish_test.py` trên bản sao đúng `adad5f5` (git status sạch): dòng tổng kết `lease_publish: 195/195 đạt; đã chạy=195, bỏ qua=0`; `195` = số `^@ca$` đếm tĩnh (đo `grep -c`), hai số bằng nhau. t125 QUA (152,130 s); lượt con `[A]` = `195/195 đạt; đã chạy=195, bỏ qua=0`, `[B]` = `195/195 đạt; đã chạy=195, bỏ qua=0`; 0 dòng `ĐỎ`, 0 dòng `!!! do`. t154 QUA ở cả ba lượt ([A] 6,264 s · [B] 6,200 s · chính 6,225 s); t202 QUA ở cả ba.
- **A7(1)**: `git diff --name-only <merge-base>...HEAD`. Lưu ý rig: ref `origin/master` của mirror sandbox = `c16bec6` (CŨ hơn master đã merge vào nhánh), nên không lọc đường dẫn thì liệt kê 26 tệp của 44 commit master đã merge (tạo tác của mirror, cùng hiện tượng lượt 7 đã ghi phải lọc). Đo trên master ĐÃ MERGE thật (`8e630c0^2` = `423b4ba`, merge-base = chính nó): `git diff --name-only 423b4ba HEAD` ⇒ đúng `ops/lease_publish_test.py` (không lọc đường dẫn).
- **A7(2)**: `git diff --numstat $(git merge-base HEAD origin/master) HEAD -- ops/lease_publish_test.py ops/lease_publish.py` ⇒ `600 15 ops/lease_publish_test.py`; cùng số với `423b4ba` (`600 15`). **600 ≤ 600 ĐẠT, dư 0** — chạm trần: mọi dòng thêm sau đây phải kèm dòng gọn tương ứng (lượt này không đề xuất hint nào).
- **A8**: bản `git show 89fc4fac8cea65979cc2483043dc8cd07a6e8518:ops/lease_publish_test.py` so HEAD, cắt theo `ast` (gồm decorator), so byte `_chay_buoc_dang` + `t51`…`t68` (kể cả `t55a`/`t55b`; bản regex đầu thiếu hậu tố chữ và cho 16 khối — đã sửa, không dùng số ấy) ⇒ `so khoi 18 18 cung ten True lech []`. Phản chứng: chèn hai dấu cách cuối dòng đầu thân `t60` ⇒ `lech ['t60_kiem_github_hong_khong_POST_va_lam_buoc_DO']` (giàn A8 có răng). `--chi-ca=t5` ⇒ `10/10 đạt`, `--chi-ca=t6` ⇒ `9/9 đạt` (đã chạy = đạt, bỏ qua=0).
- **ruff F** (`ruff check --select F --no-cache` trên `ops/lease_publish_test.py`): `3c308b3` ⇒ 9 lỗi; `adad5f5` ⇒ 9 lỗi, cùng các vị trí (F401 `shutil` ×5 ở dòng 1915/2106/2179/2264/2319, F401 `contextlib`+`io` dòng 3437, F541 dòng 1975 và 3579) ⇒ **delta = 0**.
- **`git diff --check 3c308b3 adad5f5`** rc=0 (và `423b4ba..HEAD` rc=0).
- **Mutant `L` gốc** (spec §1/§2: gỡ hai dòng chốt `lease_id` khỏi `_tien_kiem_mien_dang` trong `ops/lease_publish.py`, bản sao riêng, chạy TOÀN suite): `lease_publish: 191/195 đạt` ⇒ chết **4** ca, mỗi ca đỏ bằng thông điệp `chot()` của chính nó: `t178` ("`lease_id` là `None`: tiền kiểm phải chặn PHÉP DÒ trước khi nó chạm mạng…"), `t195` (M2: "nền phải rc=1, 0 lời gọi gh… lệch: null/Issue/trống: rc=1 goi=[('GET', …/comments)]"), `t196` (M3a "…đột biến L cho rc=0; lệch: true/PR/có dấu/còn hạn: rc=0 POST=0 bỏ_qua=True…"), `t197` (M3b, tương tự). Không ca nào chết bằng ngoại lệ vô can (4 dòng `ĐỎ` đều là thông điệp chốt tường minh). ≥1 ca ⇒ ĐẠT.

## Mục 5 — Đường vào MỚI do 6 dòng này mở ra
Đọc mã + đo; KHÔNG tìm thấy đường vào mới mức P1–P3.
1. `nguy` (dòng 6482): không va tên (grep `\bnguy\b` trong tệp: chỉ dòng 6482/6491/6509 + chữ "nguy hiểm" trong chú thích); `ast.parse` ok; tính một lần, `doc_pid` chỉ đọc, không ghi ⇒ không đổi trạng thái giữa hai lần gọi `doc_pid`.
2. Nền thiếu `getpgid`/`getsid`: `getattr(..., None)` + `if g` ⇒ không ném (mô phỏng, mục 3). Nền có: `getpgid(0)`, `getsid(0)` không ném với đối số 0.
3. Thời gian: vòng tự kiểm tối đa 6 lần × 0,2 s hạn = ≤ 1,2 s; t154 đo 6,2–6,3 s cả trước (`--chi-ca=t154` bản sao: 6,261 s) lẫn sau ⇒ không đổi đáng kể.
4. t202: hai hàng mới dùng `GOI_M4 + [...]` và `[...] + GOI_M4` (tạo list mới), không đột biến `GOI_M4` dùng chung (hàng `M4 đối chứng`/`t198`/vòng nối helper vẫn QUA trong suite 195/195).
5. Ghi chú P4 duy nhất: răng của phần tử pgid/sid phụ thuộc hình dạng runner (mục 3) — không phải lỗi, không cần vá.
Hint patch: KHÔNG CÓ (không có lớp sửa mã); `HINT.patch` không tạo.

## Bảng trạng thái finding lượt 7
| finding lượt 7 | mức | trạng thái lượt 8 | bằng chứng |
|---|---|---|---|
| L1 — `_lech_m4`/`t202` thiếu hàng "thừa lời gọi" (W1/W2 sống) | P3 | **ĐÃ ĐÓNG** | mục 2: W1 ⇒ ĐỎ đúng hàng "sau", W2 ⇒ ĐỎ đúng hàng "trước"; gỡ từng hàng ⇒ đúng W sống lại |
| L2/B — `doc_pid` chỉ loại pid/ppid (init/nhóm/phiên lọt) | P4 | **ĐÃ ĐÓNG** | mục 3: đột biến bỏ từng phần tử 1/pgid/sid khỏi `nguy` ⇒ `t154` ĐỎ bằng `bang()` (ở runner có 4 số khác nhau) |
| L3 lượt 7 (chốt chiều sâu "trường khác" chỉ có răng khi gỡ kép) · B1/B3 (độ giòn: chỉ `t198` đỏ, 2 literal) | P4 | **MANG NGUYÊN** (hồ sơ, không yêu cầu sửa mã ở lượt 7) | diff lượt 8 chỉ 3 hunk (`nguy`/`doc_pid`/vòng tự kiểm trong t154 + 1 dòng hàng t202) không chạm `t198`, literal B1/B3 hay chốt chiều sâu; không đo lại riêng từng mục (ngoài phạm vi lượt ngắn) — KHÔNG ĐO ĐƯỢC trạng thái hồ sơ (docstring `t198` dẫn Q13) |

## Bảng lớp / mức
| lớp | mức | mới/mang | sửa mã hay hồ sơ |
|---|---|---|---|
| L1 (lượt 7) — hàng thừa lời gọi ở t202 | đóng | mang, ĐÃ ĐÓNG | — |
| L2 (lượt 7) — `nguy` ở `doc_pid` | đóng | mang, ĐÃ ĐÓNG | — |
| L3' — phụ thuộc hình dạng runner của pgid/sid | P4 | mới (ghi chú) | hồ sơ (không vá; trần 600 đã chạm) |
| L3/B1/B3 (lượt 7) — chốt chiều sâu, độ giòn `t198` | P4 | mang | hồ sơ (như lượt 7) |
| Phần KHÔNG ĐO ĐƯỢC: Windows chạy thật t154 | — | mang | hồ sơ |

VERDICT: PASS
