# wp728 r2 — chuỗi lệnh chạy lại (nền + đột biến) từ CHÍNH các tệp đã lưu

Spec: `ops/specs/wp728-do-linux-doc-lap-wp710-r2.md` (sha256 `daecd8b216663d8a275700adb7f572afeb020a3e34d976460fb5c4f55dc06a40`).
Lease: `ops/leases/wp728-r2-g1-codex-reviewer-20261016.yaml`. `reviewed_sha` = `9fddb1d19e8e5b753bb687673846d484fb710182`.

Bốn biến. Phiên điều phối đặt chúng khi bàn giao; mọi đường dẫn khác đều suy ra từ chúng:

| biến | nghĩa |
|---|---|
| `R` | checkout ĐƯỢC BÀN GIAO, read-only, đủ lịch sử, detached ở `reviewed_sha` |
| `E` | thư mục môi trường: `E/dl/` chứa tarball, `E/pwsh/` là bản giải nén, `E/shim/python` |
| `S` | thư mục scratch RỖNG, nơi xuất hai blob |
| `O` | thư mục đầu ra của lượt đo (mọi log, JSON, mẫu) |

Bên đo **read-only, offline**: không `fetch`, không `push`, không sửa `R`, không mạng. Chỗ nào ra
**KHÔNG ĐO ĐƯỢC** thì DỪNG và trả checkpoint, đừng tự phục hồi.

## 0. Môi trường

```bash
export PATH="$E/pwsh:$E/shim:$PATH" TMPDIR="$O/tmp" HOME="$O/home" PYTHONDONTWRITEBYTECODE=1
mkdir -p "$TMPDIR" "$HOME"
stat -c %s "$E/dl/powershell-7.4.6-linux-x64.tar.gz"        # đòi 71645796
sha256sum  "$E/dl/powershell-7.4.6-linux-x64.tar.gz"        # đòi 6f6015203c47806c5cc444c19d8ed019695e610fbd948154264bf9ca8e157561
command -v pwsh                                             # đòi "$E/pwsh/pwsh"
type -a pwsh                                                # đòi dòng ĐẦU là "$E/pwsh/pwsh"
pwsh -NoProfile -c '$PSVersionTable.PSVersion.ToString()'   # đòi 7.4.6
command -v python; python --version; python3 --version; uname -r
```

## 1. N0 — đích đo

```bash
git -C "$R" rev-parse --is-shallow-repository               # đòi false; true/lỗi ⇒ KHÔNG ĐO ĐƯỢC
RS=9fddb1d19e8e5b753bb687673846d484fb710182
git -C "$R" merge-base --is-ancestor 8b59185975a938504de5963d2310e574dd4858b2 "$RS"; echo "a rc=$?"   # 0 đạt · 1 không · khác ⇒ KHÔNG ĐO ĐƯỢC
git -C "$R" rev-parse "$RS:scripts/nlm-credential-refresh.ps1"        # đòi 24240a31be4d51332f748d3fdadf3307cb6f1a88
git -C "$R" rev-parse "$RS:scripts/nlm-credential-refresh.Tests.ps1"  # đòi 4dc5994c363245219419fc0e2a20350761d6f7f1
git -C "$R" cat-file blob "$RS:scripts/nlm-credential-refresh.ps1"       > "$S/nlm-credential-refresh.ps1"
git -C "$R" cat-file blob "$RS:scripts/nlm-credential-refresh.Tests.ps1" > "$S/nlm-credential-refresh.Tests.ps1"
sha256sum "$S/nlm-credential-refresh.ps1" "$S/nlm-credential-refresh.Tests.ps1"
# đòi 33d32769897f97644985def693a6c54c70d2dc4048aed242b557cf4df1e8da5d  .ps1
#      7f6e56362e2bea7a2033a8995aa779f12e0141ca4e2c950401a962863a46f1a8  .Tests.ps1
```

M1, M2, M2' đều lấy NGUỒN từ `$S`, không bao giờ từ `$R/scripts/`.

## 2. Rig tự kiểm

```bash
RIG="$R/ops/reviews/wp728-do-linux/rig"      # bản ĐÃ LƯU trong kho, không phải bản nháp
python3 "$RIG/zombie_rig.py" selftest | tee "$O/rig-selftest.txt"   # đòi dòng cuối "selftest 8/8", rc 0
```

## 3. M1 — suite

```bash
pwsh -NoProfile -File "$S/nlm-credential-refresh.Tests.ps1" > "$O/m1.out" 2> "$O/m1.err"; echo "m1 rc=$?" | tee "$O/m1.rc"
```

Ghi rc, dòng tổng kết NGUYÊN VĂN. Số ca thực thi phải được ĐẾM từ đầu ra, đừng nhận con số 34.

## 4. M2 — nền, và M2' — đột biến (chạy HAI lượt mỗi loại cho N4)

```bash
for L in 1 2; do
  python3 "$RIG/zombie_rig.py" run --wrapper "$S/nlm-credential-refresh.ps1" \
      --tests "$S/nlm-credential-refresh.Tests.ps1" --max-cycles 5 --interval 10 \
      > "$O/m2-nen-$L.jsonl"; echo "m2 nen $L rc=$?"
  python3 "$RIG/mutate.py" "$S/nlm-credential-refresh.ps1" "$O/dot-bien-$L.ps1" | tee "$O/mutate-$L.txt"
  python3 "$RIG/zombie_rig.py" run --wrapper "$O/dot-bien-$L.ps1" \
      --tests "$S/nlm-credential-refresh.Tests.ps1" --max-cycles 5 --interval 10 \
      > "$O/m2-dotbien-$L.jsonl"; echo "m2 dotbien $L rc=$?"
done
cmp "$O/dot-bien-1.ps1" "$O/dot-bien-2.ps1" && echo MUTATE_TAT_DINH
```

Mỗi lượt `run` mất khoảng 45 s (4 khoảng nghỉ × 10 s). Đọc dòng `tong_ket` cuối mỗi `.jsonl`:

- `trang_thai` khác `DO_DUOC` ⇒ lượt ấy KHÔNG ĐO ĐƯỢC (lý do nằm ở `ly_do`).
- Nền: `zombie_fixture_theo_khoang` phải `[0, 0, 0, 0]`.
- Đột biến: dãy ấy phải TĂNG qua các khoảng; không tăng ⇒ rig không có răng ⇒ M2 KHÔNG ĐO ĐƯỢC.
- `mutate.py` khớp ≠ 1 ⇒ rc 3, không ghi tệp; hai lượt phải in cùng `sha256_dot_bien`.

## 5. M3 — đồng hồ (ghi nhận, không đóng lớp)

Hai `pwsh` đọc mốc khởi động của CÙNG MỘT PID. `A` sống ≥ 250 s rồi mới đọc; `B` khởi động mới rồi đọc ngay.

```bash
sleep 1200 & T=$!
T=$T pwsh -NoProfile -c '$sw=[Diagnostics.Stopwatch]::StartNew(); Start-Sleep -Seconds 260;
  $s=(Get-Process -Id ([int]$env:T)).StartTime.ToUniversalTime();
  "{0} {1}" -f $s.Ticks, $sw.Elapsed.TotalSeconds' > "$O/m3-a.txt"
T=$T pwsh -NoProfile -c '(Get-Process -Id ([int]$env:T)).StartTime.ToUniversalTime().Ticks' > "$O/m3-b.txt"
awk '{print $22}' "/proc/$T/stat" > "$O/m3-proc-starttime.txt"
kill "$T"
python3 - "$O" <<'PY'
import sys; o = sys.argv[1]
a_ticks, a_age = open(f"{o}/m3-a.txt").read().split()
b_ticks = open(f"{o}/m3-b.txt").read().split()[0]
print(f"lech_s = (A - B)/1e7 = {(int(a_ticks) - int(b_ticks)) / 1e7:.3f} ; tuoi_pwsh_A_s = {float(a_age):.1f}")
PY
```

- **Công thức:** `lệch (giây) = (StartTime_A − StartTime_B).Ticks / 10^7`, cả hai là `DateTime` UTC.
- **Nguồn đồng hồ:** `System.Diagnostics.Process.StartTime` của .NET trên Linux, tức trường 22 của
  `/proc/<pid>/stat` (jiffies kể từ boot) cộng một mốc boot do runtime tự tính. Không lấy chênh starttime
  của hai tiến trình khác nhau làm độ lệch.
- **Tuổi `A`:** đo bằng `Stopwatch` (đồng hồ đơn điệu), không bằng `Get-Date`.

## Ghi chú của phiên điều phối (không phải phép đo)

Trước khi lưu rig, phiên điều phối đã chạy thử `selftest` (8/8) và chạy `run` một lần trên nền, một lần trên
bản đột biến, để kiểm rig chạy được: nền ra `[0, 0, 0, 0]`, đột biến ra `[1, 2, 3, 4]`. Khối M3 chỉ được
kiểm CÚ PHÁP với `Start-Sleep -Seconds 1` thay cho 260; M1 KHÔNG được chạy thử. Đó là lượt dựng thử
rig của bên ĐIỀU PHỐI (Claude), KHÔNG phải lượt đo được ghi nhận; kết quả của wp728 chỉ đến từ lượt bên đo
chạy lại theo tệp này.
