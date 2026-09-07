from pathlib import Path
import json
root=Path(__file__).resolve().parent.parent
s=json.loads((root/'do-review9/state.json').read_text())
lines=['# VERDICT — cross-review PR #468, lượt 9','',f'verdict: {s["verdict"]}','reviewed_sha: 0bc6e56e1a1fd21cedfc18557320941d51db866c','', 'Reviewer: Codex / OpenAI, phiên độc lập qua API, có shell cục bộ. Transport: tệp trong sandbox. Dùng khung `tai-lieu/cross-review-SKILL.md`; chỉ đọc/ghi trong phạm vi PROMPT, không mạng, không commit/push, không đăng GitHub, không cấp merge authorization. Đường `ops/...` tính từ `cay-kho/`; hiện vật tự đo nằm ở `do-review9/`.','', '## ĐỐI CHIẾU LƯỢT TRƯỚC','']
if s['verdict'] != 'dang-do':
    lines[5:5] = ['Kết luận: **changes_requested — 1 P1, 4 P2**. Đối chiếu bốn finding lượt 8: **3 VÁ HỜ, 1 CHƯA VÁ**; phép so nghiệm thu A2 đã sửa đúng, phần còn lại của finding đó hạ từ P1 xuống P2.', '']
lines += ['- '+x for x in s['reconciliations']] or ['Đang đo; chưa phân loại.']
lines += ['', '## BẢNG ĐO','', '| khẳng định | PR khai | đo được | khớp? |','|---|---|---|---|']
for row in s['rows']: lines.append('| '+' | '.join(str(x).replace('|',' / ').replace('\n','<br>') for x in row)+' |')
lines += ['', *s['findings'], '', '## Giới hạn và bàn giao','', *s['notes'], '',f'verdict: {s["verdict"]}','']
(root/'VERDICT.md').write_text('\n'.join(lines))
