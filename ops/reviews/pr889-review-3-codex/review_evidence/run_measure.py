from pathlib import Path
import os
import subprocess
import sys

root = Path(__file__).resolve().parents[1]
mode = sys.argv[1]
info = {
    'workflow-modes': (9, 'Đo cấu hình gọi thật và chốt CÙNG head', 'Job gate Windows còn chạy toàn bộ bán kính hoặc job gom nhận bằng chứng khác HEAD.'),
    'history-anchored': (10, 'Đối chiếu lịch sử chỉ từ reviewed_sha trở về trước', 'Dẫn #878/#879 và ngày 23-10 dựa trên thay đổi sau SHA đang review.'),
    'topology': (4, 'Mở ma trận và điều kiện job độc lập', 'Windows còn mảnh khác 0, job gom vẫn có thể chạy, hoặc gate khác bị loại Windows.'),
    'os-steps': (5, 'Đếm điều kiện hệ điều hành trên mọi bước YAML', 'Con số 6 sai hoặc bỏ sót if dùng matrix.os.'),
    'windows-main': (6, 'Phản chứng nhánh Windows bằng AST main thật', 'Nhánh Windows không duyệt hết CA, vẫn chạy đột biến, hoặc bỏ qua chưa bị trừ mẫu số.'),
    'history': (7, 'Kiểm SHA lịch sử và câu executor sửa ngoài hint', 'Dẫn e63961f/#878/#879 lệch phiên bản hoặc câu sửa thêm làm rộng kết luận.'),
}
n, name, hypothesis = info[mode]
script = 'measure_extra.py' if mode in ('workflow-modes', 'history-anchored') else 'measure.py'
cmd = ['python3', '../review-evidence/' + script, mode]
p = subprocess.run(cmd, cwd=root/'cay-kho', env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'), capture_output=True, text=True)
log = p.stdout + p.stderr
(root/'review-evidence'/f'{mode}.log').write_text(log)
(root/'review-evidence'/f'{mode}.rc').write_text(str(p.returncode)+'\n')
with (root/'VERDICT.md').open('a') as out:
    out.write(f'\nHƯỚNG {n}: {name}\n  giả thuyết : {hypothesis}\n  lệnh       : (cd cay-kho && PYTHONDONTWRITEBYTECODE=1 {" ".join(cmd)})\n  output     : rc={p.returncode}\n\n```text\n{log.rstrip()}\n```\n')
    if p.returncode:
        out.write('  kết luận   : KHÔNG ĐO ĐƯỢC — cần kiểm lỗi giàn đo, chưa kết luận về PR.\n')
    elif mode == 'topology':
        out.write('  kết luận   : KHÔNG PHẢI LỖI về cấu hình. KHÔNG ĐO ĐƯỢC trạng thái skipped thực trên máy chủ GitHub vì không mạng; predicate false và ma trận không có Windows là bằng chứng cục bộ, không giả khai đã đọc job run.\n')
    else:
        out.write('  kết luận   : KHÔNG PHẢI LỖI trong hướng đã đo; đánh giá tổng hợp khi hoàn tất các hướng.\n')
print(log)
print('rc:', p.returncode)
