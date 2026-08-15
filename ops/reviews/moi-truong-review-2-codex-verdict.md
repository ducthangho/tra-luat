# Verdict: changes_requested

- Reviewer: `codex`
- Lease: `moi-truong-review-2-codex-20260815`
- Reviewed head: `026c4ea95ae5039ce32f794018a69f03a94bf41a`
- Delta base: `0194ea0eea9d4b9eed569059f1bda9775ad92971`
- Master base: `d5b7bccd679480f2eb9e7f7d84c518bade7f7df1`
- Prompt SHA-256: `df3b11c130a6d317b353c5e13af82895b4cd3afeaca17d233e373c56c517a4a0`
- `la_viec_cua_packet: false`

## Findings

### `launcher-tests-leak-global-module-monkeypatches`

- Severity: high
- Disposition: changes_requested

Các ca mới nạp `launcher.py` bằng `importlib`, nhưng module được nạp vẫn dùng chính các
singleton `os`, `shutil`, `subprocess` của test runner. `t84` gán lại
`m.os.environ`; `t85` gán lại `m.shutil.which` và `m.subprocess.run`; không chỗ nào
khôi phục. Vì vậy ca t85 làm đổi luôn `subprocess.run` của runner và mọi mutation chạy
sau nó. Đây không chỉ là vệ sinh test: cổng bắt buộc thất bại ổn định, mutation bảo vệ
đường xác thực fail-open mới thêm sống `0/1`, và hai mutation từng được báo chập chờn
cũng sống trong cả hai lượt độc lập. Standard suite cũng chỉ in dòng skip t62 rồi mất
dòng tổng kết, phù hợp với việc trạng thái toàn cục của harness bị làm nhiễm.

Bằng chứng mã neo SHA bất biến:

```bash
git show 026c4ea95ae5039ce32f794018a69f03a94bf41a:.claude/dev/launcher_test.py | nl -ba | sed -n '128,145p;1878,1936p;2357,2432p'
```

`_tai_launcher_thu` (134–140) chỉ tạo module launcher mới, không tạo bản sao của các
module chuẩn. Các phép gán gây rò nằm ở 1878, 1906, 1913, 1918, 1923 và 1934. Runner
mutation (2377–2432) chạy tuần tự trong cùng tiến trình và chỉ khôi phục đường dẫn
launcher, không khôi phục các singleton bị sửa.

Bằng chứng chạy được, neo snapshot bằng SHA bất biến và dùng HOME tạm:

```bash
tmp=$(mktemp -d)
git archive 026c4ea95ae5039ce32f794018a69f03a94bf41a | tar -x -C "$tmp"
probe_home=$(mktemp -d)
(cd "$tmp" && HOME="$probe_home" python3 .claude/dev/launcher_test.py --dot-bien)
```

Chạy độc lập hai lần đều cho cùng ba dòng thất bại:

```text
do_codex_tin_DONG_DAU_thay_vi_ma_thoat SAI  giet 0/1
so_URL_tho_khong_chuan_hoa              SAI  giet 0/2
bo_cung_hoa_dau_ra                      SAI  giet 0/1
```

Đặc biệt mutation `do_codex_tin_DONG_DAU_thay_vi_ma_thoat` đã gỡ cả hai lớp độc lập
(mã thoát và lọc dòng nhiễu), nên về ý nghĩa nó là phép thử phòng thủ nhiều lớp hợp
lệ, không phải “làm nhẹ” tuỳ tiện. Vấn đề là fixture/harness không cô lập được chính
phép thử ấy. Cần monkeypatch có hoàn nguyên (`unittest.mock.patch`/fixture tương đương),
hoặc giữ tham chiếu và khôi phục trong `finally`; sau đó cổng phải xanh trọn vẹn và
in được tổng kết đáng tin.

## Đánh giá delta an ninh và hook

- Finding HIGH lượt 1 về digest ổn định đã được xử lý đúng hướng: đầu ra không còn
  `van_tay`; HMAC có khoá ngẫu nhiên theo tiến trình chỉ dùng nội bộ; nhãn nhóm tuần
  tự không cho phép băm từ điển hay nối chéo tiến trình.
- Nhãn nhóm + cờ giữ chỗ vẫn cố ý tiết lộ quan hệ “cùng giá trị” cho nhóm ít nhất ba
  biến. Đây là tín hiệu chức năng cốt lõi. Độ dài chính xác của giá trị dài làm tăng
  metadata nhưng không tạo lại oracle kiểm chứng ứng viên; ngưỡng 8 là heuristic,
  chưa có căn cứ mạnh, song không đủ thành finding chặn trong delta này.
- Cắt HMAC còn 32 bit có xác suất va chạm xấp xỉ `n(n-1)/2^33` với `n` giá trị khác
  nhau trong một lượt. Với vài chục giá trị, rủi ro khoảng 10^-7; hậu quả là báo oan
  một nhóm giữ chỗ, không lộ giá trị. Không đáng nâng thành finding.
- `_KHOA_PHIEN` giữ ổn định trong một tiến trình nên hai lần gọi helper trong cùng
  tiến trình có thể nối nhóm nội bộ; CLI hiện thực thi một lệnh rồi thoát, và digest
  không được xuất, nên không thấy đường nối transcript thành oracle.
- Không thấy đường mới in plaintext credential hoặc đưa giá trị vào traceback/thông
  điệp lỗi. Không thực hiện probe nào đụng auth thật.
- Hợp đồng `hook-nang-luc` mạnh hơn băm toàn tệp ở khả năng bỏ qua thay đổi vô hại và
  nêu đúng năng lực thiếu; yếu hơn vì marker tự khai có thể nói dối khi code hỏng hoặc
  khi quên thêm tên. Dòng khai thứ hai chỉ hợp tập, không thể xoá marker dòng trước.
  Sai chính tả/đổi tên làm lệch tập và báo thiếu, tức fail-closed. Đây là đánh đổi có
  chủ đích chấp nhận được, nhưng không phải bằng chứng cơ học rằng implementation còn
  hoạt động. Đường `parents[2]` của t88 đúng với vị trí cố định
  `.claude/dev/launcher_test.py` trong kho.

## Gates và evidence khác

Bước 0 khớp: repo không shallow; `core.abbrev=7`; HEAD và ref đều là
`026c4ea95ae5039ce32f794018a69f03a94bf41a`; remote đúng
`github.com/ducthangho/tra-luat`; delta từ `0194ea0eea9d4b9eed569059f1bda9775ad92971`
có đúng ba tệp đã khai; prompt hash đúng; cây sạch.

Các gate độc lập:

```bash
tmp=$(mktemp -d)
git archive 026c4ea95ae5039ce32f794018a69f03a94bf41a | tar -x -C "$tmp"
(cd "$tmp" && python3 .githooks/eol_policy.py --all --json)
(cd "$tmp" && python3 scripts/tl.py doc-claims-check --strict --json)
(cd "$tmp" && bash -n .claude/hooks/session-start.sh)
```

Kết quả: EOL `scanned=330`, `checked=308`, `violations=[]`; doc claims `flags=[]`;
`bash -n` rc 0. Standard launcher command hoàn tất nhưng chỉ xuất dòng skip t62 và
không xuất tổng kết, nên không xác nhận tuyên bố `88/88`. Cổng đột biến không xanh như
bằng chứng finding trên. Hai mục chập chờn được hỏi trong prompt tái hiện ở cả hai lần,
và có cùng nguyên nhân ô nhiễm thứ tự sau t85; chưa thấy bằng chứng chúng là lỗi sản
phẩm độc lập.

## Boundaries

- Không chạy Windows; t62 là fixture Windows được skip, t63 POSIX nằm trong suite.
- Không fetch/config trong vai reviewer; điều phối viên đã làm trước do `.git` chỉ đọc,
  và reviewer xác minh lại toàn bộ SHA/ref bất biến bằng đọc.
- Không thử REST/GitHub/`gh` theo đường giao việc đã xác định là không dùng được.
- Không đọc, ghi, xoá hay thay `~/.codex/auth.json` thật; mọi lượt launcher dùng HOME tạm.
- Không in giá trị biến môi trường; báo cáo chỉ nêu tên biến, độ dài hoặc nhãn nhóm.
- Không sửa tệp kho, commit, push, merge, land hay deploy.

