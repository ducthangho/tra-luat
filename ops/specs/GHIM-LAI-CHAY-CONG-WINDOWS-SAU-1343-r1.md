tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# GHIM-LAI-CHAY-CONG-WINDOWS-SAU-1343 r1 — bảng ghim dấu vân và gương của cổng Windows phải theo ci.yml sau khi #1343 chia mảnh packet-loop

- packet_id: GHIM-LAI-CHAY-CONG-WINDOWS-SAU-1343; revision: 1;

| trường | giá trị |
|---|---|
| `packet_issue` | #1361 |
| `nguon_cap_viec` | Chủ kho yêu cầu 17-11-2026 ("Mở packet ghim lại chay-cong-windows_test.ps1"); nợ ghi ở `ops/land/pr1344-wp1343-land-evidence.yaml`. |
| `review_class` | `sensitive` (cổng gate Windows dùng thay CI Windows) |
| `base` | nhánh mặc định lúc cấp lease |

## 0. Vấn đề (đo 17-11-2026 trên master `a0702d0`)

`.claude/dev/chay-cong-windows_test.ps1` ghim `$DauVanCi` lần cuối ở wp1325 r4 (nền `9aa40ac`). #1343 (`26090fd`) tách job `gate-packet-loop` thành 16 job `gate-packet-loop-manh` (mỗi job: các bước cài như cũ + `packet-loop selftest` = `python .claude/dev/packet_loop_test_manh.py` + `upload-artifact`) và job gom `gate-packet-loop` (`if: ${{ !cancelled() }}`, `download-artifact`, bước `gom manh packet-loop (so TAP ca; wp1343)` = `python .claude/dev/packet_loop_test_manh.py --gom manh --n 16`). Hai job packet-loop không còn bước cài Ruff.

Mã Python của `Doc-DauVanCi` tách nguyên văn ra chạy trên `ci.yml`:

| job | bảng ghim | `9aa40ac` | `a0702d0` |
|---|---|---|---|
| `gate-packet-loop` | `5546b9244930` | `5546b9244930` | `67a508fb841f` |
| `gate-packet-loop-manh` | — | — | `c386d4cf83f3` |
| `<workflow>` `gate` `gate-cong-cu` `gate-cong-cu-gop` `gate-nhanh-gop` `gate-nhanh-manh` `gate-ops` `gate-registry` | khớp | khớp | khớp |

⇒ ca t32 của bộ test phải ĐỎ trên master; chưa ai thấy vì CI không chạy lane Windows. `chay-cong-windows.ps1` vẫn chạy `Chay-Py 'packet-loop selftest' @('.claude/dev/packet_loop_test.py')` (TRỌN) và chưa có dòng `THAY BẰNG` nào cho bước mảnh/gom mới.

## 1. `write_set`

```
.claude/dev/chay-cong-windows_test.ps1
.claude/dev/chay-cong-windows.ps1
```

## 2. `ngoai_pham_vi`

Không sửa `.github/workflows/ci.yml`, `.claude/dev/packet_loop_test*.py`, hay ca test nào ngoài phần bảng ghim/gương. Không nới chốt nào của `Tim-ThieuGuong`/`Doc-DauVanCi`. Nếu t32/t34/t35 không xanh được mà không đổi logic chốt ⇒ DỪNG, báo kèm log.

## 3. `muc_tieu`

| # | mục tiêu |
|---|---|
| M1 | Rà `git diff 9aa40ac <base> -- .github/workflows/ci.yml` (bỏ chú thích) cho hai job packet-loop; liệt kê trong chú thích ghim mọi đổi NGOÀI lệnh và mọi đổi LỆNH, theo nếp khối chú thích wp1325 r4 ngay trên `$DauVanCi`. |
| M2 | Gương: giữ `packet-loop selftest` chạy `.claude/dev/packet_loop_test.py` TRỌN; thêm MỘT dòng `Noi 'THAY BẰNG MỘT LƯỢT (master từ 26090fd): "packet-loop selftest" (mảnh) + "gom manh packet-loop (so TAP ca; wp1343)" — …'` theo đúng mẫu hai dòng `THAY BẰNG` hiện có, nêu rõ chạy TRỌN gồm cả `CA_DAI` mà CI đẩy sang workflow đêm. Nếu `Tim-ThieuGuong` đòi thêm (bước `download-artifact`/`upload-artifact`, `if:` mới), xử lý theo nếp đã có cho `gate-cong-cu`/`gate-nhanh-*`, không nới chốt. |
| M3 | Ghim lại `$DauVanCi`: `'gate-packet-loop' = '<giá trị đo trên base>'`, thêm `'gate-packet-loop-manh' = '<giá trị đo trên base>'`; dòng chú thích nêu nền đã đo. Giá trị lấy từ thông báo lỗi t32 hoặc từ chính `Doc-DauVanCi`, KHÔNG chép từ bảng §0 nếu base đã khác `a0702d0`. |
| M4 | Rà ca t9 (trần `timeout-minutes` của job packet-loop so `HanGiay`) và các ca nhắc `gate-packet-loop` khác; sửa ghi chú/ghim nếu lệch, không nới chốt. |

## 4. `nghiem_thu`

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| N1 | pwsh ≥ 7.4 trên Linux (executor tự cài vào container, ngoài kho): `pwsh -NoProfile -File .claude/dev/chay-cong-windows_test.ps1` — các ca t32, t34, t35, t9 ĐẠT trên head; ghi rõ ca nào BỎ QUA vì nền (Linux). Base: t32 ĐỎ với thông báo `<DAU-VAN>` nêu đúng hai job trên. | Bỏ một dòng ghim mới ⇒ t32 ĐỎ (`job MOI chua ghim`). Bỏ dòng `THAY BẰNG` ⇒ t32 ĐỎ (bước không có gương) — nếu không ĐỎ thì ghi rõ vì sao. |
| N2 | Windows thật (VM `tra-luat-win`, phiên điều phối chạy): toàn bộ `chay-cong-windows_test.ps1` trên head và base; head không còn ca ĐỎ nào mà base cũng ĐỎ vì ghim; mọi ca ĐỎ còn lại phải ĐỎ y hệt ở base (delta 0). | Head có ca ĐỎ mới so base. |
| N3 | Ruff F không áp (PowerShell); `adr-song`, `doctrine-scan` rc 0; `git diff --check` sạch; EOL theo `.githooks/eol_policy.py --all --json` ok. | — |

Chỉ chạy `chay-cong-windows_test.ps1` (không chạy `chay-cong-windows.ps1` thật — nó chạy toàn bộ cổng, rất dài).

## 5. Kích thước và trần

2 tệp, dự kiến ≤ 40 dòng thêm. Trần `ADR-0053`: ≤ 450.

## 6. `luat_dung`

Cần đổi logic chốt của bộ so/dấu vân, hoặc cần sửa `ci.yml` ⇒ DỪNG, báo kèm log, không tự làm.

## 7. `chua_do_duoc`

N2 do phiên điều phối đo trên VM Windows của chủ kho trước merge. Cổng thật `chay-cong-windows.ps1 -Muc day-du` không chạy trong packet này.
