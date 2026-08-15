# Verdict: changes_requested

- Reviewer: `codex`
- Reviewed head: `0194ea0eea9d4b9eed569059f1bda9775ad92971`
- Base: `d5b7bccd679480f2eb9e7f7d84c518bade7f7df1`
- Prompt SHA-256: `144198286555951ce1d82a310cb0d4773e58b3fc1fc1dd4146619a5bcbf623ae`

## Findings

### `deterministic-secret-fingerprint-is-dictionary-oracle`

- Severity: high
- Disposition: changes_requested

`moi-truong` và `doctor --json` xuất 8 hex đầu của SHA-256 cho **mọi** biến khớp mẫu nhạy cảm, kể cả giá trị ngắn; đồng thời xuất chính xác độ dài. Đây không phải là phép che bí mật. Với password, token cấu hình, cờ hoặc credential có tập ứng viên nhỏ, người đọc transcript chỉ cần băm ngoại tuyến từng ứng viên rồi so 32 bit là xác định được giá trị. Ngưỡng 8 ký tự chỉ được áp dụng trong `_nhom_van_tay`, không áp dụng khi trường `van_tay` được xuất ở `quet_bien_moi_truong`.

Bằng chứng mã, neo SHA bất biến:

```bash
git show 0194ea0eea9d4b9eed569059f1bda9775ad92971:.claude/dev/launcher.py | nl -ba | sed -n '1538,1602p'
```

Các dòng 1544–1546 trả `sha256(...).hexdigest()[:8]`; dòng 1596 xuất vân tay cho từng biến không rỗng. Trong khi đó điều kiện độ dài chỉ nằm ở dòng 1583, trong hàm nhóm. Phép đo an toàn trên môi trường phiên (không in giá trị) cho thấy lệnh hiện xuất 66 mục và một nhóm 5 biến có cùng vân tay; tức dữ liệu này thực sự đi vào đầu ra CLI, không chỉ là helper nội bộ.

Đề nghị: không xuất digest ổn định của giá trị. Nếu nhu cầu chỉ là phát hiện trùng nhau trong cùng một lượt, gán nhãn nhóm ngẫu nhiên/tuần tự (`group-1`) sau phép so sánh nội bộ, hoặc dùng HMAC với khoá ngẫu nhiên chỉ sống trong tiến trình và không xuất khoá. Với giá trị ngắn/không gian nhỏ, chỉ nên báo loại (`short`, `duplicate`) mà không xuất digest.

## Evidence khác

### Bước 0

Tất cả mỏ neo khớp: repo không shallow; `core.abbrev=7`; HEAD và ref đều là `0194ea0eea9d4b9eed569059f1bda9775ad92971`; remote là `github.com/ducthangho/tra-luat`; diff từ base có đúng 5 tệp đã khai; prompt có đúng SHA-256 yêu cầu. `git fetch` và ghi config do điều phối viên thực hiện trước vì `.git` read-only trong sandbox; reviewer xác minh lại bằng đọc theo chỉ dẫn bổ sung.

### Hợp đồng `doctor` và `hook-phien`

- `doctor` mặc định: rc 0, `ok=true`, `ok_kha_dung=false`.
- `doctor --doi-kha-dung`: rc 13, vẫn giữ `ok=true`, `ok_kha_dung=false`.
- Không tìm thấy caller cũ nào thêm cờ mới ngoài hook được sửa; workflow Windows vẫn gọi mặc định.
- `hook-phien` không fail-open khi thiếu `origin/master`: trả `KHONG_DO_DUOC`; trạng thái này chỉ không đổi rc mặc định, còn dưới `--doi-kha-dung` nó góp vào rc 13. Quyết định không chặn mặc định là hợp lý để tránh chốt đỏ thường trực trên nhánh packet, nhưng so băm toàn tệp có thể báo lệch vì thay đổi vô hại. Một tiêu chí cơ học tốt hơn là marker/version năng lực trong hook; quan hệ tổ tiên commit đơn thuần không đủ vì chính nhánh packet cũ cần bị cảnh báo.

### Hook, credential và chống rò

- Không thấy đường in trực tiếp giá trị credential trong `quet_bien_moi_truong`, `lenh_moi_truong`, `lenh_doctor` hay `chuan_bi_xac_thuc`; finding trên là rò suy diễn qua digest, không phải in plaintext.
- `chuan_bi_xac_thuc` giữ bốn chốt: không đè khi `codex login status` xanh; đòi object có khoá `tokens`; `mkstemp` tạo tệp hẹp rồi `chmod 0600` và `os.replace`; thông báo lỗi không chứa nội dung. `mkstemp` vốn tạo mode 0600 nên không có cửa sổ quyền rộng. SIGKILL giữa lúc ghi vẫn có thể để lại tệp tạm 0600, nhưng không để lại destination nửa vời.
- Hook và Python là hai triển khai độc lập nên có rủi ro trôi; hiện khác có chủ đích ở việc Python nhận thêm JSON thô. Nên cân nhắc gom parser/writer dùng chung nếu muốn giữ bất biến lâu dài.
- Không thấy bệnh `set -e` tương tự còn sót ở đường doctor. Chuỗi cài `rg` cố ý nuốt lỗi từng installer rồi kiểm dương bằng `rg --version`; lỗi cuối vẫn được báo rõ. `rg` bắt buộc là hợp lý cho workflow agent hiện tại; Windows có đường cài chính thức được khai.

### Tests và phản chứng

Các lệnh tái lập từ snapshot SHA bất biến (trích snapshot bằng `git archive`, không dựa vào HEAD/ref động):

```bash
tmp=$(mktemp -d)
git archive 0194ea0eea9d4b9eed569059f1bda9775ad92971 | tar -x -C "$tmp"
(cd "$tmp" && python3 .claude/dev/launcher_test.py)
(cd "$tmp" && python3 .githooks/eol_policy.py --all --json)
(cd "$tmp" && python3 scripts/tl.py doc-claims-check --strict --json)
```

Kết quả: `86/86 ca (qua 85, bo qua 1, hong 0)`; ca bỏ qua là fixture Windows t62 và bản POSIX t63 đã chạy; EOL `violations=[]`; doc claims `flags=[]`.

Ba đột biến riêng trên bản sao `/tmp` đều bị ca mới giết:

- t84: bỏ lọc độ dài + tên bí mật → bắt oan nhóm ba cờ bật/tắt.
- t85: quay lại tin dòng đầu cảnh báo → báo `DUNG_DUOC` khi chưa đăng nhập.
- t86: bỏ đường JSON thô → từ chối fixture JSON thô.

Ba ca chưa được nối vào `DOT_BIEN`, nhưng standard suite vẫn khóa hành vi và phản chứng thủ công xác nhận chúng có răng.

### Tài liệu

Đo lại lịch sử đối tượng Git cho kết quả đúng như tài liệu:

- hook blob `298d96fe51f70e4e` tại commit `f08e45b2eac667235558d1670732fdc9dd638973`: 0 lần nhắc `CODEX_AUTH_JSON`;
- hook blob `3c3dd49a8a163479` tại commit `2573765355c61fe42342d78877d306edde649ab8`: 5 lần;
- hook ở base/master bất biến `d5b7bccd679480f2eb9e7f7d84c518bade7f7df1` cũng có SHA-256 đầy đủ bắt đầu `3c3dd49a8a163479` và 5 lần nhắc;
- môi trường reviewer hiện cũng có đúng nhóm 5 biến cùng vân tay `f07d7417`, không in hoặc kiểm tra giá trị.

## Boundaries

- Không đụng `~/.codex/auth.json` thật; mọi probe có khả năng đọc/ghi credential dùng HOME tạm.
- Không in giá trị của bất kỳ biến môi trường nào.
- Không chạy Windows; dựa vào fixture Windows được đánh dấu skip và ca POSIX tương ứng.
- Không thử lại REST/GitHub vì đường này đã được điều phối viên đo là proxy 403 và prompt bổ sung yêu cầu không mất thời gian thử lại. Vì vậy khẳng định lịch sử “REST 403, `/user` 200” không được reviewer tái đo độc lập trong lượt này.
- Không fetch trong vai reviewer vì `.git` read-only; xác minh các SHA ref bất biến sau fetch do điều phối viên thực hiện lúc `2026-08-15T17:57:46Z`.
- Không commit, push, merge, land hay sửa cây kho.
