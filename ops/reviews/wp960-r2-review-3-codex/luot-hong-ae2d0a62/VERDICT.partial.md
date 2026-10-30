verdict: dang_lam
reviewed_sha: 934a5b063670acfbed410487d8244cd17d586d6e
Kết quả: đang đo.

## BẢNG ĐO

Đã đọc `run/ae2d0a62/prompt.snapshot`; review chỉ đọc cây `cay-kho/`, mọi đột biến trên bản sao `/tmp`. Chưa có kết luận.

## BẢNG ĐÓNG FINDING LƯỢT 2

Đang đọc các phản chứng cũ.

## BẢNG SĂN

Sẽ nối kết quả sau mỗi hướng thử; chưa có kết quả.

## NHẬT KÝ TĂNG DẦN

- Bắt đầu: tạo tệp trước khi đo; không gọi mạng, không sửa cây được review.

### Hướng 1 — định danh, phạm vi, kiểm tra nền

Lệnh: `git -C cay-kho rev-parse HEAD HEAD^{tree}`; `git -C cay-kho status --short`; `sha256sum cay-kho/ops/specs/NO-CAU-LICH-SU-BIEN-NHAN-r2.md`.
Output: HEAD `934a5b063670acfbed410487d8244cd17d586d6e`; tree `d46fa5b04fd1ae9d1580b59ae90e58ed73852451`; status rỗng; spec `9a155cb9995b225129dc11de03e2d6d9811a9c53321151e0389214a85d33b1ca` (khớp). `git diff --numstat 4488444 HEAD -- ops/bien_nhan_v2.py ops/bien_nhan_v2_test.py`: `260/193`, `532/104`, tổng 1089 dòng. `git diff --name-only 2618eb4 HEAD` chỉ hai tệp packet; merge `f7659a2..0a37008` không đổi hai tệp. Bản sao `/tmp/wp960-r3-copy` clone `--no-hardlinks`, checkout đúng SHA.

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 .claude/dev/packet_loop.py doctrine-scan --root .`; `git diff --check 4488444 HEAD` (trong cay-kho).
Output: `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine`, rc=0; diff-check output rỗng, rc=0. Git `2.43.0`, Python `3.13.17`, ruff `0.17.3` được đo bằng lệnh version. Suite đầy đủ và gate đang chạy, chưa coi là pass.

### Hướng 2 — chạy lại nguyên phản chứng cũ qua CLI

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 -u probe_r3.py matrix > evidence/matrix.log` và `... probe_r3.py yaml_cli > evidence/yaml-cli.log`. Harness nạp test từ bản sao exact SHA, giữ nguyên fixture/case; bọc `_chay_cli` chỉ ghi lại rc/stderr. c91 chạy 28 lời gọi (14 nguồn × có/không nợ), đều rc=2, không Traceback/NỢ CHẾT và stderr nêu nguồn; c92 10 lượt hỏng rc=2, 2 lượt lành rc=0; c93/c94 đều `qua`. Phép subprocess riêng cho timestamp sai, lồng sâu 1200 tầng, UTF8, thư mục receipt: gate thường và hai cờ sinh nợ đều rc=2. Các ca cũ đã đóng trên các phản chứng này; không suy ra đóng mọi lỗi đo.

### Hướng 3 — object hỏng nhưng Git không báo stderr

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 -u probe_r3.py objects > evidence/objects.log`. Dùng `_kho_cau`, `_ghi_bn_cau` hiện hữu; câu `Ban a19f1fc chua vao master.` nói về B0. Nguyên trạng CLI rc=1 (không nợ). Chỉ sửa loose object của M (`e72d857…`): bỏ dòng `parent <B0>`, nén zlib hợp lệ và giữ đường dẫn object cũ. `git fsck --full` rc=3, stderr `hash-path mismatch`. Tuy nhiên `--is-shallow-repository` rc0/stdout=false, `--disambiguate` rc0/OID đúng dạng, `cat-file --batch-check` rc0/`<OID> commit`, `for-each-ref` rc0/ref commit đúng dạng, `merge-base --is-ancestor` rc1 — **tất cả stderr rỗng**. CLI sau hỏng: không nợ **rc=0**; có nợ **rc=1/NỢ CHẾT**; không KHÔNG ĐO ĐƯỢC. Object rỗng/zlib lỗi ở phản chứng lượt trước nay rc=2 cả hai trạng thái nợ.

### object-lech-bam-van-duoc-tin [P1] Object hỏng có nội dung zlib hợp lệ biến lỗi đo thành sạch hoặc nợ chết
HÌNH DẠNG: loi-do
TỆP/DÒNG: `ops/bien_nhan_v2.py:1126` (`_git_do`), `1141` (`_kho_lanh`), `1336` (merge-base).
VẤN ĐỀ: stderr rỗng không chứng minh object toàn vẹn. Git có thể đọc object có nội dung không khớp tên băm mà vẫn trả giao thức hợp lệ, không cảnh báo trong các lệnh hiện dùng. Quan hệ tổ tiên bị thay đổi âm thầm, vi phạm M2: cổng kết luận sạch hoặc NỢ CHẾT trên kho hỏng.
ĐÃ THỬ NGHIỆM: `python3 -u probe_r3.py objects`, trường `valid-zlib-wrong-hash` trong `evidence/objects.log`: fsck rc3/hash-path mismatch, merge-base rc1/err="", CLI 1→0 không nợ, 0→1/NỢ CHẾT có nợ. Các object ngoài M giữ nguyên.
GỢI Ý VÁ: cần kiểm tra tính toàn vẹn object/lịch sử ở biên sức khỏe kho hoặc dùng nguồn Git đã xác minh; stderr chỉ là tín hiệu bổ sung. Thêm phản chứng này × hai trạng thái nợ và mutant bỏ kiểm toàn vẹn. Cân nhắc chi phí khi chọn phạm vi xác minh, không gán mọi stdout đúng dạng là dữ liệu đã xác minh.
ĐỘ TIN: cao

### Hướng 4 — stderr vô hại và ref hợp lệ có tên con

Cùng lệnh `probe_r3.py objects`, hai trường độc lập trong `evidence/objects.log`:
- `config-warning`: thêm đúng `core.fsyncObjectFiles=true` vào kho lành. Các lệnh Git rc0, stdout vẫn đúng, stderr `warning: core.fsyncObjectFiles is deprecated; use core.fsync instead`. CLI **rc1→rc2** không nợ, **rc0→rc2** có nợ. `GIT_TRACE=1` cũng làm rc2 ngay tại `--is-shallow-repository` với trace vô hại.
- `branch-prefix`: remote `origin/master` trỏ M hợp lệ; đổi tên local master thành main, thêm nhánh `master/topic`. `for-each-ref <ba tên>` rc0/stderr rỗng và trả cả `refs/heads/master/topic`. Quan hệ tổ tiên đo trực tiếp rc0; CLI rc2: `for-each-ref trả dòng lạ: 'refs/heads/master/topic ... commit'`.

### canh-bao-vo-hai-thanh-loi-do [P1] Cảnh báo cấu hình Git hợp lệ bị coi là không đo được
HÌNH DẠNG: loi-do
TỆP/DÒNG: `ops/bien_nhan_v2.py:1135` và `_ENV_GIT:1123`.
VẤN ĐỀ: `_git_do` chặn mọi stderr, kể cả cảnh báo deprecation không ảnh hưởng kết quả. Kho đầy đủ lành có `core.fsyncObjectFiles=true` bị đẩy sang rc2; không phải object/ref hỏng. GIT_TRACE kế thừa cũng gây cùng kết quả.
ĐÃ THỬ NGHIỆM: `python3 -u probe_r3.py objects`, `config-warning`: trước rc1/0, sau rc2/2, thông báo duy nhất là cảnh báo deprecation; raw Git vẫn rc0/stdout đúng. Không lấy trace làm bằng chứng duy nhất.
GỢI Ý VÁ: xác minh điều kiện lành và giao thức riêng cho từng lệnh; xử lý các kênh cảnh báo/trace được biết là vô hại mà vẫn giữ fail-closed với lỗi ref/object thực. Thêm đối chứng cấu hình deprecated và mutant làm đối chứng thành unknown. Không đơn giản bỏ kiểm stderr vì sẽ tái mở phản chứng object rỗng/ref hỏng.
ĐỘ TIN: cao

### ref-con-hop-le-bi-coi-la-dong-la [P1] Nhánh master/topic làm kiểm nhánh mặc định thất bại
HÌNH DẠNG: bo-chon-ung-vien
TỆP/DÒNG: `ops/bien_nhan_v2.py:1187`–`1192`.
VẤN ĐỀ: Mẫu của `for-each-ref` còn khớp các ref con ở ranh giới `/`; chúng là dữ liệu Git hợp lệ. Cổng đòi mọi dòng đều thuộc đúng ba tên nên từ chối kho lành dù `origin/master` đã có commit mặc định đo được. CI checkout detached có thể không có local master, do đó tên nhánh master/topic không xung đột với master local.
ĐÃ THỬ NGHIỆM: `python3 -u probe_r3.py objects`, `branch-prefix`: raw for-each-ref rc0, err rỗng, hai ref master/topic và origin/master; CLI rc2, direct merge-base rc0.
GỢI Ý VÁ: giới hạn phép liệt kê ở ref chính xác hoặc lọc ref con hợp lệ trước khi kiểm định dòng cần đo; giữ kiểm định nghiêm cho dòng ứng với ref chính xác và giữ dò dangling symref. Thêm fixture remote master lành + local master/topic, có và không nợ.
ĐỘ TIN: cao

### Hướng 5 — partial clone thật qua file://

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 -u probe_r3.py partial > evidence/partial.log`. `git clone --no-checkout --no-local --filter=blob:none file:///tmp/.../source <dst>` rc0/stderr rỗng. Config thực: `core.repositoryformatversion=1`, `remote.origin.promisor=true`, `remote.origin.partialclonefilter=blob:none`; **không có extensions.partialclone**. Có tệp pack `.promisor`, `rev-list --missing=print` báo 4 OID thiếu. `_kho_lanh` vẫn trả None (chấp nhận); chạy gate trên fixture receipt có sẵn được chép vào bản clone trả rc1/L-ANCESTRY, unknown=0. Đây là phép local file transport, không gọi mạng. Chưa khẳng định quan hệ tổ tiên của blob:none này sai; đang đo thêm đường partial thiếu commit.
