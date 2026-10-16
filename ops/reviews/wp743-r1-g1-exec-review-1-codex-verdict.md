Reviewed commit: 80e0fac0a4ab8c74486cf3bab1a73e1dec600994

verdict: approve
P1=0, P2=0, P3=0

Không có finding cần sửa trong diff. Review read-only trên đúng head; mọi bản sao, driver và log nằm ngoài KHO. Không merge/land. Approval này không thay thế CI Windows thật và uỷ quyền land của chủ kho.

## Kết luận kỹ thuật

- `launcher.py:666–674`: `Path.stat()` chạy một lần; ENOENT/ENOTDIR không đọc, rơi về kill/ps; ESRCH trả False ngay; OSError khác đọc đúng một lần rồi dùng kill nếu đọc/phân tích lỗi. Không mở thêm đường coi tiến trình sống là chết. Nhận diện zombie sau EBADF/ELOOP là thay đổi được Q2 cho phép; nhánh đọc thành công chỉ trả chết khi trạng thái là Z. Các nhánh đọc lỗi vốn có, Windows, Darwin và kill giữ nguyên.
- Trên 3.12/3.13, EBADF/ELOOP trước đây bị `exists()` nuốt: đo nền read=0, kill=1; head read=1, kill=0 với tiến trình thật còn sống, kết quả đều True. ValueError do phép stat ném trước đây bị exists nuốt, nay thoát nguyên: Q2 cho phép rõ phạm vi chỉ bắt họ OSError. Đường dẫn /proc được tạo từ PID, phép đo ValueError là seam, không phải lỗi thật của tiến trình Linux thông thường.
- `_CsSeam` vá chính `Path.stat` nên bắt thao tác mới trên cả ba interpreter. Ca r743 chặn exists bằng sentinel, đo stat/read/kill, và dùng zombie thật qua B3-zombie. Ca đỏ khi đổi về exists trên chính 3.12. t156 còn chốt ValueError/ngoại lệ ngoài OSError và các nhánh ENOENT/Darwin giả lập.
- Ba mẫu `wp685_a`, `wp685_f`, `wp685_m4` vẫn có răng: trên 3.14 lần lượt chết tại `B1 result True`, `B2-dem-lan result False`, `B1 stat count 2`. Mẫu f vẫn đo việc thăm dò lần hai sau lần đầu chưa kết luận, không chỉ đếm lần gọi trong nhánh thành công.
- Runner `chay_dot_bien` có sẵn cơ chế tính cả ngoại lệ thường là chết. Không dựa vào cơ chế đó để approve: driver riêng phân loại ngoại lệ; cả 59 mutant (60 cặp đích gốc, cộng 1 cặp bổ sung exists→t156) đều chết bằng chính `TinHieuChotCa` trên cả ba phiên bản. Không survivor, không lỗi vô can được ghi công.
- Write set đúng hai tệp, 90 dòng thêm / 10 dòng xoá, dưới trần 300 dòng thêm. Số ca tổng tăng đúng 1 (195→196). Không đổi workflow; nợ `ci-chua-co-lan-python-314` giữ nguyên theo Q3.

## Đã đo

Các lệnh đọc/kiểm tra chạy từ thư mục ra; `KHO=../rv`. Driver và log giữ ngay cạnh biên nhận để chạy lại. Không lấy lời khai executor làm kết quả đo độc lập.

| Lệnh / phép đo | rc và kết quả |
|---|---|
| `pwd; sha256sum spec-r1.md; cat spec-r1.md` | rc=0; băm đúng `e2121dc07571edb24bf410badccf88d0d35a3d1ddba1f1a490ab378b607d8519`. |
| `git -C ../rv rev-parse HEAD`; `git -C ../rv status --short` | rc=0; đúng SHA dòng đầu; cây sạch trước/sau review. |
| `git -C ../rv diff 9fddb1d 80e0fac -- .claude/dev/launcher.py .claude/dev/launcher_test.py`; `git -C ../rv diff --stat 9fddb1d 80e0fac` | rc=0; đọc toàn diff; 2 tệp, +90/-10. |
| `git -C ../rv diff --check 9fddb1d 80e0fac` | rc=0, không có lỗi khoảng trắng. |
| Các lệnh `rg -n`, `sed -n` trên launcher/test; `cat`/`tail`/`ls` đọc log, `ps -eo pid,etime,args` lọc tiến trình | Đọc seam, `_con_song`, `_CsNhan`, t81, runner mutation và runner suite; không sửa KHO. Một số `ls`/`ps` thăm dò rc=1/2 khi chưa có rc-file hoặc không khớp tiến trình; không coi là kết quả test. |
| `cp -a ../rv /tmp/review743-head`; `mkdir -p /tmp/review743-base`; `git -C ../rv archive 9fddb1d19e8e5b753bb687673846d484fb710182 \| tar -x -C /tmp/review743-base` | rc=0; head đầy đủ, base là archive đúng commit. |
| `PYTHONDONTWRITEBYTECODE=1 python<V> -B measure.py` với V=3.12,3.13,3.14 | Mỗi lệnh rc=0. Bốn ca đích r743/t156/t157/t117 PASS; 59 mutant, 61 cặp mỗi phiên bản đều KILL_CHOT; FAILURES=0. Log `measure-<V>.log`. Driver import test, đặt `LAUNCHER_DANG_DUNG` vào bản sao mutant riêng, chạy dưới `_co_lap_toan_cuc`, chỉ ghi công TinHieuChotCa. |
| `PYTHONDONTWRITEBYTECODE=1 python<V> -B semantics.py` với V=3.12,3.13,3.14 | rc=0 cả ba; so nền/head với seam EBADF/ELOOP/ValueError như phân tích trên. Trên nền 3.14 stat seam không chạm (stat=0), đúng vấn đề gốc; không dùng số đó để suy errno thực tế của exists. |
| `python3.13 -m ruff --version`; tương tự 3.12 và 3.14 | rc=1, không có module ruff trong các interpreter này. |
| `ruff check --select F /tmp/review743-<tree>/.claude/dev/launcher.py /tmp/review743-<tree>/.claude/dev/launcher_test.py`, tree=head,base | rc=1 mỗi bản, cùng 5 F841: goc_open, rc, PENDING, goc_run, p; delta=0. Dùng CLI ruff có sẵn thay cho module không cài. Log `ruff-head.log`, `ruff-base.log`. |
| `(cd /tmp/review743-<tree> && PYTHONDONTWRITEBYTECODE=1 python<V> -B .claude/dev/launcher_test.py)` cho 6 tổ hợp | Chạy đầy đủ, kết quả bảng dưới. Log/rc `review743-<tree>-<V>.log/.rc`. Các lượt độc lập chạy đồng thời trên bản sao riêng. |
| `PYTHONDONTWRITEBYTECODE=1 python3.13 -B pid_collision.py <pid>` với pid=10,11,12 | rc=0; cưỡng bức getpid đúng PID giả fixture, cả nền lẫn head đều ném cùng TinHieuChotCa tại t81. Log `pid-collision.log`. |
| `PYTHONDONTWRITEBYTECODE=1 python<V> -B /tmp/review743-<tree>/.claude/dev/launcher_test.py --lap-ca t81_chup_cay_windows_thieu_creationdate_phai_fail_closed --lan 20` | Chạy riêng trên head/base, ba interpreter: năm tổ hợp 20/20, rc=0; head 3.14 lần đầu PID=10 nên 0/20, rc=1 (cùng va chạm fixture). Chạy lại head 3.14 PID=4: 20/20, rc=0, ghi riêng `t81-head-3.14-retry.log`. Logs `t81-*`. |
| Tạo `measure.py`, `semantics.py`, `pid_collision.py`, biên nhận và sao chép log vào thư mục ra | Chỉ ghi thư mục ra hoặc /tmp; không sửa mã trong KHO. |

### Full suite: kết quả thô, không giấu ca đỏ

| Python | Base: qua/đã chạy; tổng; bỏ qua; rc | Head: qua/đã chạy; tổng; bỏ qua; rc | Ca đỏ |
|---|---|---|---|
| 3.12 | 182/186; 195; 9; 1 | 184/187; 196; 9; 1 | Nền: t81, r09, r15, r351. Head: r09, r15, r351. |
| 3.13 | 194/194; 195; 1; 0 | 194/195; 196; 1; 1 | Nền: không. Head: t81. |
| 3.14 | 181/186; 195; 9; 1 | 183/187; 196; 9; 1 | Nền: r09, r15, r351, t156, t157. Head: t81, r09, r15, r351. |

`t81` không phải hồi quy của packet: full-suite có PID nền 3.12=11, head 3.13=10, head 3.14=12, trùng ba PID giả hardcode trong fixture. `_chup_cay` loại PID hiện tại (`launcher.py:544`); ở PID 11, nhánh “con mù” không còn được xem như hậu duệ cần xác minh; ở PID 10/12 ảnh mất phần tử fixture. Phép đo cưỡng bức PID tái hiện trên CẢ nền lẫn head; các lượt chạy riêng không trùng PID đều 20/20. Sau khi tách nhiễu này, tập đỏ 3.12/3.13 không đổi; 3.14 bỏ đúng t156/t157. Đây không phải tuyên bố rằng mọi lượt full-suite đều xanh.

## KHÔNG ĐO ĐƯỢC

- Không chứng nhận full-suite sạch mọi điều kiện: 3.12/3.14 có 8 ca phụ thuộc venv/pip tự bỏ qua (r345/r347/r348), cùng tình trạng trên nền và head. Ngoài ra t62 dành Windows bỏ qua trên mọi lượt Linux. Không đánh đồng skip với pass.
- Không có một lượt full-suite 3.13 head sạch hoàn toàn trong phép đo này do va chạm PID nói trên; đã xác định nguyên nhân bằng phép đo đối chứng và chạy riêng, không chạy lại toàn suite sau khi hoàn tất sáu lượt.
- Không chạy Windows thật, Darwin thật, CI GitHub hay Python >=3.15. Darwin chỉ được chốt nhánh giả lập trong suite; Windows là điều kiện land cần kiểm riêng.
- Không chạy toàn bảng đột biến ngoài phạm vi wp685/r743; đã chạy toàn suite thường và toàn nhóm 59 mutant liên quan trên ba Python.
- Không dùng web để đọc issue/PR hay xác minh lease/CI: nội dung issue được đóng băng trong spec đã kiểm băm; việc review ở đây giới hạn mã và phép đo cục bộ.
- Không có tool environment_status trong công cụ phiên này; không cần truy cập mạng/credential/container build cho các phép đo trên.
