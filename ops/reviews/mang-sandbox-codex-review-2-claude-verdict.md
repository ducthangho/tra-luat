verdict: changes_requested
reviewed_sha: b5bb3952b99f991e84f458f70dcd38c0bf9b90e2
provider: claude
executor: codex
reviewer: claude
round: 2

# Cross-review vòng 2 — `MANG-SANDBOX-CODEX` (#334)

## 0. Khả năng chạy mã và vị trí đứng của lượt này

```text
python3 --version        -> Python 3.11.15, rc=0
python3 -c 'print("PROBE_OK")'  -> PROBE_OK, rc=0
codex --version           -> codex-cli 0.150.0, rc=0
```

Workspace: KHÔNG phải clone rời mới dựng — thư mục làm việc hiện tại đã ở đúng
`HEAD=b5bb3952b99f991e84f458f70dcd38c0bf9b90e2` (detached), `git status --porcelain` RỖNG,
`origin` là `https://github.com/ducthangho/tra-luat` (URL thật, không phải đường dẫn cục bộ).
Không cần dựng mirror riêng vì cây đã đúng exact SHA và sạch.

**Khác biệt lớn nhất so với vòng 1: `codex sandbox` LỒNG CHẠY ĐƯỢC trong môi trường của tôi.**
Vòng 1 (reviewer `codex`) và bản thân executor lượt 3 (theo `docs/MANG_SANDBOX_CODEX.md:50`)
đều báo `rc=101` ("failed to open synthetic bubblewrap mount registry lock") trước khi probe
kịp chạy. Tôi KHÔNG gặp lỗi đó — cả ba hàng bảng ba cột và cả bốn tổ hợp đều chạy thật, có
đầu ra thật. Nguyên nhân của khác biệt môi trường này CHƯA XÁC ĐỊNH (có thể khác quyền
container/mount giữa hai lượt) — không suy diễn thêm, chỉ ghi nhận: đây là **lượt review đầu
tiên tái lập được toàn bộ bảng số bằng lệnh nguyên văn của tài liệu**, đúng như đề bài yêu cầu.

### Bảng ba cột — kết quả tôi tự đo (không phải chép lại)

| lệnh | socket | url | git | class socket | class url | class git |
|---|---:|---:|---:|---|---|---|
| `python3 .claude/dev/probe_mang.py` (ngoài codex) | 0 | 0 | 0 | LOT | LOT | LOT |
| `codex sandbox -c sandbox_mode=workspace-write --` | 1 | 1 | 1 | POLICY_DENIED (stage=create) | POLICY_DENIED (stage=urlopen) | **UNKNOWN** (rc=128) |
| `... -c sandbox_workspace_write.network_access=true --` | 0 | 0 | 0 | LOT | LOT | LOT |

Ba hàng khớp byte-với-byte với "Bảng ba cột đã chốt" ở `docs/MANG_SANDBOX_CODEX.md:18-22` **về
cột `MA_CU` (0/1)**. Nhưng cột `class` — thứ mà tài liệu tự nói "chỉ class mới phân biệt" —
không nằm trong bảng đó, và khi tôi đo ra, ô git ở hàng "sandbox mặc định" là `UNKNOWN`, không
phải `POLICY_DENIED`. Chi tiết ở Việc 3 / finding mới bên dưới.

### Bảng bốn tổ hợp — bốn lệnh nguyên văn của tài liệu, tôi copy-paste và chạy thật

```text
(a) không override                              -> socket=1 url=1 git=1  (git: class=UNKNOWN, rc=128)
(b) network_access=true                         -> socket=0 url=0 git=0  (LOT)
(c) writable_roots=[.../.git,/tmp]              -> socket=1 url=1 git=1  (git: class=UNKNOWN, rc=128)
(d) network_access=true + writable_roots        -> socket=0 url=0 git=0  (LOT)
```

Khớp byte-với-byte với bảng ở `docs/MANG_SANDBOX_CODEX.md:37-42`. `raw` của git ở (a)/(c):
`"fatal: unable to access '[URL] Failed to connect to 127.0.0.1 port 37215 after 0 ms:
Couldn't connect to server"`. Đã kiểm nguồn gốc: môi trường của tôi (và theo mô tả hệ thống,
mọi phiên Claude Code cùng loại) đặt `https_proxy=http://127.0.0.1:37215` — HTTPS ra ngoài đi
qua proxy loopback do hạ tầng phiên bơm vào, không liên quan chính sách sandbox của Codex.
Trong sandbox lồng không mở `network_access`, kết nối tới CHÍNH proxy loopback đó bị từ chối
kiểu "couldn't connect" (không phải "operation not permitted"), nên `phan_loai_git()` — vốn chỉ
khớp các mẫu chuỗi liệt kê ở `probe_mang.py:70-77` — không nhận diện được và rơi vào `UNKNOWN`
theo đúng thiết kế fail-close. Đây KHÔNG phải bug của `probe_mang.py` (nó làm đúng việc phải
làm: không đoán, trả `UNKNOWN`); vấn đề nằm ở TÀI LIỆU coi ô này ngang hàng "1 = bị chặn chính
sách" như hai cột kia. Xem finding mới `bang-chinh-gom-unknown-vao-1-nhu-chan`.

## 1. Phán quyết năm finding vòng 1

### `ma-chan-gom-moi-loi-khong-phan-loai` (P1) — **ĐÃ VÁ THẬT**

`probe_mang.py` nay có 9 mã lớp (`LOT POLICY_DENIED ENDPOINT_ERROR TIMEOUT TOOL_ERROR UNKNOWN
DNS_ERROR REPOSITORY_ERROR AUTH_ERROR`), `phan_loai_loi()`/`phan_loai_git()` phân biệt theo
kiểu ngoại lệ/errno/mẫu chuỗi, và `UNKNOWN` khiến `main()` trả rc=1 (`t10_main_schema_va_fail_close`
khóa hành vi này). Bảy ca khóa đúng bảy tình huống round-1 liệt kê:

| ca | tình huống | lớp mong đợi | tôi tự vô hiệu hoá nhánh tương ứng — kill |
|---|---|---|---|
| `t1_url_sai_cu_phap` | URL sai cú pháp | `ENDPOINT_ERROR` | có (xem Việc 4) |
| `t2_dns_loi` | DNS lỗi | `DNS_ERROR` | có (baseline `nền: 11/11`) |
| `t3_timeout` | timeout | `TIMEOUT` | có (baseline) |
| `t4_path_rong` | `PATH=""` | `TOOL_ERROR` | có (baseline) |
| `t5_kho_khong_ton_tai` | repo không tồn tại | `REPOSITORY_ERROR` | có (baseline) |
| `t6_auth_loi` | auth lỗi | `AUTH_ERROR` | có (baseline, redact `secret`) |
| `t7_policy_denied` | policy-denied | `POLICY_DENIED` | có (xem Việc 4) |

Tự đo (không chỉ chạy `gate()` có sẵn): vô hiệu hoá nhánh `endpoint and isinstance(reason,
ValueError)` → `phan_loai_loi()` không còn phân biệt URL sai cú pháp → CHỈ `t1` đỏ. Vô hiệu hoá
nhánh `PermissionError`/errno EPERM/EACCES → CHỈ `t7` đỏ. Hai ca này có răng thật, không vô nghĩa.

### `cong-dot-bien-tu-giam-van-xanh` (P1) — **VÁ HỜ**

Năm phép xoá y hệt vòng 1 (đo lại trên cấu trúc mới, ánh xạ sang 5 chốt hiện có: xoá 1 entry
`DOT_BIEN` · xoá `# canh-nen-do` · xoá `# canh-duy-nhat` · xoá `# canh-ghi-song` · xoá
`# canh-ket-luan`) — **cả năm đều CHẾT** (`rc=1`, đứt ngay ở `t12_cong_dot_bien_tu_canh`). Đây
là cải thiện thật: năm phép xoá cụ thể mà vòng 1 dùng để lừa cổng không còn lừa được.

Nhưng: **cả bốn trong năm phép chết đó (mọi thứ trừ xoá entry) CHẾT DUY NHẤT vì `t12` — một
hàm meta-test tự mutate chính văn bản test để kiểm tra các `canh-*` bằng fixture tổng hợp — và
`t12` bản thân nó KHÔNG có ai canh.** Xem Việc 2 và finding mới
`meta-test-tu-canh-khong-ai-canh` — đây là đúng HỌ lỗi cũ, dịch lên một tầng, chưa đóng.

### `bon-to-hop-chua-co-lenh-nguyen-van` (P1) — **ĐÃ VÁ THẬT**

`docs/MANG_SANDBOX_CODEX.md:29-34` có đủ bốn lệnh Bash nguyên văn, dùng đúng `-c key=value` với
dotted key `sandbox_workspace_write.network_access`/`sandbox_workspace_write.writable_roots`,
kèm `DUONG_DAN_GOC=$(git rev-parse --show-toplevel)`. Tôi copy-paste nguyên bốn lệnh (không sửa
một ký tự) và chạy — probe thật sự khởi động ở cả bốn, kết quả khớp bảng byte-với-byte (xem mục
0). Đây là bằng chứng mạnh hơn vòng 1 và vòng "lượt 3" tự khai có được: cả hai lượt trước chỉ
parse được lệnh, không chạy được probe (rc=101); tôi chạy được cả bốn tới cùng.

### `network-access-gate-rong-hon-egress` (P2) — **ĐÃ VÁ THẬT**

`probe_mang.py:43-60` (`kenh_socket_loopback`) nay theo dõi `stage` (`create`/`bind`/`listen`)
tường minh; `probe_mang_test.py:55-60` (`t8_giai_doan_socket`) khoá cả hai giai đoạn còn lại
ngoài `create`. Tài liệu (`docs/MANG_SANDBOX_CODEX.md:44-46`) đã tự nhận đúng phạm vi: "Loopback
không phải egress... kết quả chỉ xác minh phạm vi cờ cấu hình đã đo, không xác minh một ranh
giới mạng" — không còn overclaim "cờ mở mạng". Đo thật của tôi xác nhận `stage=create` nhất
quán ở cả hai hàng bị chặn (mặc định và tổ hợp (a)/(c)) — đúng như tài liệu mô tả, không lệch.

### `ban-kinh-phai-chet-che-tac-dong-cheo` (P2) — **ĐÃ VÁ THẬT**

`gate()` (`probe_mang_test.py:116`) nay chạy `chay_suite(goc.replace(cu, moi, 1), CA_SAN_PHAM)`
— TOÀN BỘ 11 ca cho mỗi mutant, không chỉ ca đích — và in `kill-set=sorted(chet)` đầy đủ
(`ok m1_sai_stage_bind: kill-set=['t8_giai_doan_socket']`, đo thật từ lần chạy nền của tôi).
Cơ chế phát hiện coupling đã tồn tại và đang hoạt động (dù ở 5 mutant hiện tại không có ca nào
lộ coupling — kill-set mỗi mutant đúng bằng tập tối thiểu). Đủ để đóng finding.

## 2. Hỏi tiếp một tầng — `t12` là lớp canh duy nhất, và không ai canh nó

Đo trực tiếp (bản sao ngoài repo, không đụng cây thật):

```text
xoa-entry-m1          -> rc=1 (chet ngay trong t12, KHONG lien quan canh rieng — vi entry-count
                          duoc gate() chinh no bat doc lap qua canh-so-luong, khong can t12)
xoa-canh-nen-do        -> rc=1 (chet trong t12)
xoa-canh-duy-nhat      -> rc=1 (chet trong t12)
xoa-canh-ghi-song      -> rc=1 (chet trong t12)
xoa-canh-ket-luan      -> rc=1 (chet trong t12)
```

Tiếp một tầng: **vô hiệu hoá `t12` theo BA đường độc lập** (không gọi `t12_cong_dot_bien_tu_canh`
trong `main()`; hoặc để thân hàm rỗng `pass`), rồi GIỮ NGUYÊN mỗi phép xoá guard ở trên:

```text
canh-nen-do   xoá + main() không gọi t12   -> TỔNG: ĐẠT, rc=0   (SỐNG)
canh-nen-do   xoá + thân t12 rỗng          -> TỔNG: ĐẠT, rc=0   (SỐNG)
canh-duy-nhat xoá + main() không gọi t12   -> TỔNG: ĐẠT, rc=0   (SỐNG)
canh-ghi-song xoá + main() không gọi t12   -> TỔNG: ĐẠT, rc=0   (SỐNG)
canh-ket-luan xoá + main() không gọi t12   -> TỔNG: ĐẠT, rc=0   (SỐNG)
```

Bốn trong năm chốt của round-1 quay lại y nguyên trạng thái "SỐNG" chỉ bằng MỘT dòng sửa thêm
(bỏ lời gọi `t12` hoặc làm rỗng thân nó) — **không cần đụng gì tới bốn `canh-*` line comment**.
Chỉ `canh-so-luong` (bảo vệ số lượng entry `DOT_BIEN`) sống sót độc lập, vì nó được `gate()`
chạy vô điều kiện trên dữ liệu THẬT (`GOC.read_text()`), không phụ thuộc `t12`.

**Đây là finding, không phải giới hạn không thể xoá.** Lý do: một giới hạn không-thể-xoá đúng
nghĩa là "mọi lớp canh thêm đều dịch vấn đề lên một tầng y hệt, không giảm được rủi ro" — điều
này ĐÚNG về mặt tuyệt đối (không file nào tự bảo vệ được 100% khỏi chính ai sửa nó), nhưng nó
KHÔNG đúng ở đây theo nghĩa thực hành: hiện tại việc vô hiệu hoá tầng bảo vệ tốn ĐÚNG MỘT dòng
và KHÔNG bị bất kỳ ca nào — kể cả `t12` chính nó — phát hiện. Thêm một tầng canh (vd một `t13`
kiểm `t12` có được gọi không, kiểm `t12.__code__.co_names` chứa các lời gọi mong đợi, hoặc so
sánh checksum thân hàm) sẽ ĐÓNG được đúng ba trong bốn đường tôi vừa liệt kê ở trên (giống vòng
lặp round-1 → round-3 đã đóng năm đường cụ thể) — không phải vô ích, chỉ không phải lời giải
cuối cùng. Đường thực sự khác họ, không dịch tầng: xác minh `probe_mang_test.py` (rc, VÀ chuỗi
`"tự đột biến cổng: 9/9 chết"` trong stdout) từ một cổng NẰM NGOÀI write set của packet này —
ví dụ một bước CI/`packet_loop.py` không do packet `MANG-SANDBOX-CODEX` kiểm soát — vì kẻ sửa
đổi ba tệp trong write set của packet này không đồng thời sửa được cấu hình CI đó. `docs/
MANG_SANDBOX_CODEX.md` KHÔNG khai giới hạn này ở đâu cả (mục `KHÔNG_ĐO_ĐƯỢC` chỉ nói về mạng,
không nói về độ bền của chính cổng đột biến) — theo đúng tiêu chí đề bài đặt ra ("nếu không khai
thì đó có phải P1 không?"), câu trả lời là CÓ.

## 3. Bảng số có còn đọc được sau khi đổi schema — CÓ, với một lỗ

`1` bây giờ, theo `docs/MANG_SANDBOX_CODEX.md:7-11`, đúng như tài liệu tự khai: chỉ nghĩa
"không lọt" (`MA_CU=1`), KHÔNG tự thân là "bị chặn bởi chính sách". Đo ba cảnh thật (mục 0):

| kênh | ngoài sandbox | sandbox mặc định | sandbox + network_access |
|---|---|---|---|
| socket | `LOT` | `POLICY_DENIED` (create) | `LOT` |
| url | `LOT` | `POLICY_DENIED` (urlopen) | `LOT` |
| git | `LOT` | **`UNKNOWN`** (rc=128) | `LOT` |

Hai ô đầu (socket, url) đúng như tài liệu ngụ ý: `1` = chính sách sandbox từ chối, đo được rõ
ràng qua `class`. Ô thứ ba (git, hàng giữa) là **đúng cái ô tài liệu gọi là "bị chặn" mà bộ
phân loại KHÔNG quy cho chính sách** — nó là `UNKNOWN`, tức theo lời chính tài liệu
(`docs/MANG_SANDBOX_CODEX.md:10`), đây là `KHÔNG_ĐO_ĐƯỢC`. Tài liệu đang khai mạnh hơn dữ liệu:
cả "Bảng ba cột đã chốt" lẫn "Bốn lệnh tách hai cờ" trình bày ô này ngang hàng thị giác với hai
ô `POLICY_DENIED` thật, không có ghi chú nào tách nó ra. Xem finding mới bên dưới — đúng lớp lỗi
`ma-chan-gom-moi-loi-khong-phan-loai` bị dịch từ mã nguồn (đã vá) lên bảng tài liệu (chưa vá).

## 4. Bảy ca khoá phân loại — có răng, đã tự đo thêm ngoài bộ có sẵn

`t11_ma_phan_loai_doc_nhat` khoá CHẶT mọi phép gộp hai mã bất kỳ (kiểm `len(set(9 hằng))==9`).
Tự đo năm cặp KHÔNG nằm trong `DOT_BIEN` sẵn có (không dùng `gate()`, gọi thẳng `chay_suite`):

```text
TIMEOUT+TOOL_ERROR            -> chết (t11)
POLICY_DENIED+ENDPOINT_ERROR  -> chết (t11)
TIMEOUT+POLICY_DENIED         -> chết (t11)
TOOL_ERROR+UNKNOWN            -> chết (t11)
REPOSITORY_ERROR+DNS_ERROR    -> chết (t11)
```

Mọi cặp gộp hằng số đều chết qua đúng một cửa (`t11`) — cửa đó đủ mạnh vì nó kiểm TẬP HỢP, không
kiểm từng cặp. Không tìm thấy ca nào PASS mà vô nghĩa trong phạm vi đã spot-check (`t1`, `t7`
xác nhận có răng thật ở mục 1). Tôi KHÔNG chạy hết 11×11 tổ hợp có thể — ghi ở CHỖ KHÔNG ĐO ĐƯỢC.

## 5. Ngân sách và phạm vi

```text
git diff --numstat ac82ddc583f688d54bdc60e06922ec09bdab9f16 -- .claude/dev/probe_mang.py .claude/dev/probe_mang_test.py docs/MANG_SANDBOX_CODEX.md
101  0  .claude/dev/probe_mang.py
156  0  .claude/dev/probe_mang_test.py
52   0  docs/MANG_SANDBOX_CODEX.md
```

Tổng = **309**, khớp lời khai executor, dưới trần 320.
`git diff --name-only ...` chỉ in đúng ba đường dẫn write set; `docs/GOI_AGENT_DA_NEN.md`
không xuất hiện trong `git diff --name-only ac82ddc583f688d54bdc60e06922ec09bdab9f16 --
docs/GOI_AGENT_DA_NEN.md` (rỗng) — ngoài write set, không bị chạm.

Vết ngân sách qua ba lượt (đo lại từ `base..2ef85c9d`, `base..511a58d2`, `base..b5bb3952`):

| lượt | probe.py | test.py | doc | tổng | số ca |
|---|---:|---:|---:|---:|---:|
| 1 | 69 | 186 | 52 | 307 | 5 mutant (không có t-case đặt tên) |
| 2 | 69 | 186 | 61 | 316 | như lượt 1 (chỉ doc đổi) |
| 3 | 101 | 156 | 52 | 309 | 11 case + 5 mutant + `t12` meta-test |

Lượt 3 KHÔNG chỉ "viết ngắn lại" — nó thay hẳn cơ chế phân loại 0/1 cũ bằng hệ 9-lớp, nên số
dòng test giảm (186→156) trong khi số ca tăng (5→11) là hợp lý về mặt kiến trúc (thay thế, không
cắt gọt). Đối chiếu `511a58d2..b5bb3952` xác nhận: mọi cải thiện của lượt 2 ở tài liệu (bốn lệnh
nguyên văn) được GIỮ NGUYÊN trong lượt 3 (không bị ghi đè); phần bị bỏ trong doc là các câu diễn
giải cũ ("đối chứng NGOÀI codex — container này có mạng", "Cơ chế mạng ĐÃ XÁC MINH") — bị THAY
bằng câu thận trọng hơn, không phải bị xoá không thay. Không phát hiện phản chứng nào bị mất
theo nghĩa "test case biến mất mà không có case thay thế tương đương" — xem mục 1, cả năm
finding vòng 1 vẫn có ca khoá tương ứng trong bộ 11+5+`t12` hiện tại.

## 6. Finding mới

### `meta-test-tu-canh-khong-ai-canh` — P1

**Tệp/dòng:** `.claude/dev/probe_mang_test.py:131-148` (thân `t12_cong_dot_bien_tu_canh`),
`:149-154` (lời gọi trong `main()`).

**Vấn đề:** bốn trong năm chốt bảo vệ `gate()` (`canh-nen-do`, `canh-duy-nhat`, `canh-ghi-song`,
`canh-ket-luan`) chỉ được xác minh bởi fixture tổng hợp bên trong `t12` — không case nào trong
`CA_SAN_PHAM`/`DOT_BIEN` chạm tới chúng qua đường dữ liệu thật. `t12` được gọi từ đúng MỘT chỗ
(`main()`), không try/except nào khác bảo vệ lời gọi đó ngoài khối bắt lỗi đã có, và bản thân
`t12` không có phép đo nào xác nhận nó ĐÃ chạy hay thân nó còn nguyên vẹn. Bỏ lời gọi
`t12_cong_dot_bien_tu_canh(None)` trong `main()`, hoặc làm rỗng thân hàm, tái tạo NGUYÊN VẸN cả
bốn phép xoá mà vòng 1 dùng để chứng minh cổng có thể bị lừa — bằng đúng MỘT dòng sửa, không
chạm tới bất kỳ `canh-*` nào. Đây là chính bug `cong-dot-bien-tu-giam-van-xanh` tái phát ở tầng
cao hơn, và tài liệu không khai giới hạn này ở đâu.

**Đo tái lập:**
```text
D=$(mktemp -d); cp probe_mang.py probe_mang_test.py "$D/"
python3 - "$D/probe_mang_test.py" <<'PY'
import re
p = "ARGV1"  # duong dan that
src = open(p, encoding="utf-8").read()
src = src.replace(
    'def main() -> int:\n    try:\n        t12_cong_dot_bien_tu_canh(None)\n'
    '    except Exception as e:\n        return bao(f"TỔNG: ĐỎ (t12_cong_dot_bien_tu_canh: '
    '{type(e).__name__}: {e})")\n    return gate(GOC.read_text(encoding="utf-8"))\n',
    'def main() -> int:\n    return gate(GOC.read_text(encoding="utf-8"))\n', 1)
open(p, "w", encoding="utf-8").write(src)
PY
# roi xoa BAT KY dong nao trong bon dong "# canh-nen-do|canh-duy-nhat|canh-ghi-song|canh-ket-luan"
# tren ban sao do -> python3 probe_mang_test.py -> "TỔNG: ĐẠT" rc=0
```
(Đã chạy thật ở mục 2 của verdict này với năm tổ hợp; tất cả cho `rc=0`.)

**Gợi ý vá:** (1) vá tại chỗ gọi `t12` trong `main()` và tại cổng CI/`packet_loop.py` bên NGOÀI
write set của packet này (một cổng nằm trong chính ba tệp bị sửa không thể tự bảo vệ mình khỏi
người sửa ba tệp đó — cần một bên thứ ba không đổi cùng lúc). (2) Ca khoá tối thiểu: mutant xoá
lời gọi `t12` trong `main()`, mutant làm thân `t12` rỗng, phải đỏ ở MỘT nơi không nằm trong ba
tệp của packet. (3) Rủi ro/giới hạn: không có cách đóng triệt để bên trong CHÍNH file bị sửa —
đây là quy luật, không phải lỗi thiết kế của lượt 3; nhưng KHÔNG khai giới hạn này trong tài
liệu là lỗ hổng khai báo thật, tách biệt với lỗ hổng kỹ thuật.

### `bang-chinh-gom-unknown-vao-1-nhu-chan` — P1

**Tệp/dòng:** `docs/MANG_SANDBOX_CODEX.md:18-22` (bảng ba cột), `:37-42` (bảng bốn tổ hợp);
minh chứng lớp thật ở `.claude/dev/probe_mang.py:68-78` (`phan_loai_git`).

**Vấn đề:** ô "git" ở hàng "sandbox mặc định" (bảng ba cột) và ở tổ hợp (a)/(c) (bảng bốn tổ
hợp) hiển thị `1`, cùng hình dạng với ô "socket"/"url" ở đúng hàng đó — nhưng khi chạy probe
THẬT (mục 0 verdict này), lớp thực tế của ô git là `UNKNOWN` (`rc=128`, lỗi "Couldn't connect to
server" tới proxy loopback `127.0.0.1:37215` mà môi trường phiên bơm vào qua `https_proxy`),
không phải `POLICY_DENIED` như hai ô kia. Theo đúng câu tài liệu tự đặt ra ở dòng 10
("`UNKNOWN` là `KHÔNG_ĐO_ĐƯỢC`"), ô này đang được trình bày như một phép đo chính sách sandbox
trong khi nó là một kết quả CHƯA PHÂN LOẠI ĐƯỢC — đúng loại lỗi mà finding `ma-chan-gom-moi-loi-
khong-phan-loai` (vòng 1) đã đóng ở tầng mã nguồn nhưng chưa đóng ở tầng bảng tóm tắt. Không ai
phát hiện được điều này trước lượt review này vì cả reviewer vòng 1 lẫn executor lượt 3 đều gặp
`rc=101` (bubblewrap) trước khi probe kịp chạy trong sandbox lồng — số trong bảng được kế thừa từ
lượt đo cũ hơn hệ phân loại hiện tại, và `class=` thật của các ô đó chưa từng được đối chiếu.

**Đo tái lập:** ba lệnh ở mục 0 của verdict này (bảng ba cột) và bốn lệnh nguyên văn ở
`docs/MANG_SANDBOX_CODEX.md:29-34` (bảng bốn tổ hợp) — đọc trực tiếp dòng `class=` trong stdout,
không đọc số `MA_CU`.

**Gợi ý vá:** (1) vá ngay hai bảng — thêm cột `class` (hoặc chú thích riêng ô) cho từng ô hiện
là `1`, ít nhất tách rõ ô nào là `POLICY_DENIED` xác nhận và ô nào là `UNKNOWN`/khác. (2) Nếu
nguyên nhân UNKNOWN của git đến từ hạ tầng proxy của phiên chạy (không phải chính sách sandbox
của Codex), nói thẳng điều đó trong `KHÔNG_ĐO_ĐƯỢC` thay vì để mặc định người đọc suy ra "cả ba
kênh cùng bị chặn bởi cùng một cơ chế". (3) Ca khoá: một bước đối chiếu tự động (script hoặc
người review kế tiếp) chạy lại đúng 3+4 lệnh và so `class=` với bảng — mutant làm bảng ghi
`POLICY_DENIED` cho ô git phải bị bắt. (4) Rủi ro: `class` của git có thể đổi theo môi trường
proxy của từng phiên chạy (không phải hằng số theo Codex) — nên câu đúng có thể là "chưa xác
định được git bị chặn bởi CHÍNH SÁCH SANDBOX hay bởi HẠ TẦNG PROXY của phiên", và tài liệu nên
khai đúng mức độ chưa chắc đó thay vì đưa ra hàng "1,1,1" đồng nhất.

## 7. CHỖ KHÔNG ĐO ĐƯỢC

| ô / khẳng định | lệnh đã thử | lý do |
|---|---|---|
| Nguyên nhân `rc=101` (bubblewrap) không tái lập ở môi trường này | so sánh môi trường của tôi với mô tả của vòng 1/lượt 3 | không có quyền truy cập môi trường của lượt kia để so trực tiếp; chỉ ghi nhận khác biệt hành vi |
| `class` thật của git trong MỌI môi trường Codex (không chỉ môi trường có proxy loopback kiểu Claude Code) | không có môi trường Codex nào khác để thử | phiên này chỉ có một loại container |
| Toàn bộ 11×11 (hoặc C(9,2) đầy đủ) tổ hợp gộp mã phân loại | đã đo 5 cặp mẫu ngoài `DOT_BIEN`, không đo hết | ngân sách thời gian của lượt review; `t11` đủ mạnh về mặt cấu trúc (kiểm tập hợp, không kiểm từng cặp) nên rủi ro bỏ sót thấp nhưng chưa = 0 |
| Trạng thái GitHub (PR/Issue #334) trực tiếp | không dùng `gh`/MCP GitHub trong lượt này | không cần cho phạm vi review — mọi thứ đo trên exact SHA cục bộ |
| Toàn bộ 11 ca trong `CA_SAN_PHAM` có "răng" thật hay không (chỉ spot-check t1, t7, t11) | đã đo t1/t7/t11/t2..t6,t8,t9,t10 gián tiếp qua baseline 11/11 | không tự vô hiệu hoá riêng từng nhánh còn lại (t3,t4,t5,t6,t9,t10) — nền `11/11` xác nhận chúng ĐANG pass đúng nhưng không xác nhận chúng sẽ ĐỎ nếu logic tương ứng hỏng |

## 8. Kết luận

`changes_requested`. Còn hai P1 mới: `meta-test-tu-canh-khong-ai-canh` (lớp bảo vệ cổng đột
biến bị dịch lên `t12` mà `t12` không có ai canh — tái phát trực tiếp của
`cong-dot-bien-tu-giam-van-xanh`) và `bang-chinh-gom-unknown-vao-1-nhu-chan` (hai bảng flagship
của tài liệu trình bày một ô `UNKNOWN` ngang hàng hai ô `POLICY_DENIED` thật — tái phát của
`ma-chan-gom-moi-loi-khong-phan-loai` ở tầng bảng tóm tắt). Năm finding vòng 1: bốn ĐÃ VÁ THẬT
(`ma-chan-gom-moi-loi-khong-phan-loai`, `bon-to-hop-chua-co-lenh-nguyen-van`,
`network-access-gate-rong-hon-egress`, `ban-kinh-phai-chet-che-tac-dong-cheo`), một VÁ HỜ
(`cong-dot-bien-tu-giam-van-xanh` — năm phép xoá cụ thể của vòng 1 đã chết thật, nhưng lớp bảo
vệ mới (`t12`) mở lại đúng bốn trong năm đường đó bằng một dòng sửa duy nhất). Không nâng P2 nào
lên P1 để giữ packet mở; không có P2 nào tồn đọng lại từ vòng 1 cần ghi thành nợ — cả hai đã
đóng thật.
