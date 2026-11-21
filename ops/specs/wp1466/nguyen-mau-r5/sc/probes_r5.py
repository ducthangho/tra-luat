"""Chạy lại 48 phép của `probes_r4.py` (reviewer lượt 4) cộng các phép byte mới, trên cây nguyên mẫu r5.

Dùng: python -B probes_r5.py <cây> <khoa.json> <thư mục tạm>. Chỉ đọc cây; ghi vào thư mục tạm.
"""
from pathlib import Path
import json, subprocess, sys, hashlib, os
P, locks, D = Path(sys.argv[1]), json.load(open(sys.argv[2])), Path(sys.argv[3]); D.mkdir(parents=True, exist_ok=True)
raw = (P / 'docs/PROTOCOL_DA_PHIEN.md').read_bytes(); rows = []
env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', TMPDIR=str(D))
L = raw.split(b"\n")
def unit(k):
    a, b = locks[k]["dong"]; return b"\n".join(L[a - 1:b])
def run(name, b, want):
    d = D / name; (d / 'docs').mkdir(parents=True, exist_ok=True); (d / 'docs/PROTOCOL_DA_PHIEN.md').write_bytes(b)
    r = subprocess.run([sys.executable, '-B', str(P / '.claude/dev/packet_loop.py'), 'doctrine-scan', '--root', str(d)], capture_output=True, text=True, env=env)
    row = {'case': name, 'rc': r.returncode, 'expected': want, 'bytes_changed': b != raw, 'stderr': r.stderr.strip()[:300]}
    rows.append(row); print(json.dumps(row, ensure_ascii=False), flush=True)
# --- 48 phép của reviewer, giữ nguyên định nghĩa ---
run('baseline', raw, 0)
for k in locks:
    u = unit(k); assert raw.count(u) == 1, k
    run('delete_' + k, raw.replace(u, b'', 1), 9)
    run('crlf_inside_' + k, raw.replace(u, u.replace(b'\n', b'\r\n', 1), 1), 9)
    run('tab_indent_' + k, raw.replace(u, b'\n'.join(b'\t' + line for line in u.split(b'\n')), 1), 9)
    run('trailing_space_' + k, raw.replace(u, u + b' ', 1), 9)
    if locks[k]['thu_tu']:
        run('duplicate_' + k, raw + b'\n\n' + u + b'\n', 9)
        run('relocate_' + k, raw.replace(u, b'Mot doan ghi chu thu nghiem.', 1) + b'\n\n' + u + b'\n', 9)
for k in ['K04', 'K05']:
    u = unit(k); run('insert_block_before_' + k, raw.replace(u, b'Doan bien tap thu nghiem.\n\n' + u, 1), 9)
for name, line in [('plain', b'INV-01 | ghi chu'), ('compact', b'|`INV-01`|ghi chu|'), ('canonical', b'| `INV-01` | ghi chu |'), ('debt', b'| INV-01-NO | ghi chu |')]:
    run('id_' + name, raw + b'\n\n' + line + b'\n', 0 if name == 'debt' else 9)
u = unit('K01'); run('duplicate_K01_same_ancestor', raw.replace(u, u + b'\n\n' + u, 1), 9)
run('relocate_K01', raw.replace(u, b'', 1) + b'\n\n## Phu luc thu nghiem\n\n' + u + b'\n', 9)
run('append_unlocked_note', raw + b'\nGhi chu bien tap thu nghiem.\n', 0)
# --- phép MỚI của người soạn r5: byte lạ, dòng biên, che tại địa chỉ ---
for k in locks:
    u = unit(k)
    run('cr_le_giua_' + k, raw.replace(u, u.replace(b' ', b' \r', 1), 1), 9)
    run('nbsp_cuoi_' + k, raw.replace(u, u + ' '.encode(), 1), 9)
    run('tab_cuoi_' + k, raw.replace(u, u + b'\t', 1), 9)
    run('cr_cuoi_' + k, raw.replace(u, u + b'\r', 1), 9)
    run('u2028_thay_xuong_dong_' + k, raw.replace(u, u.replace(b'\n', ' '.encode(), 1), 1), 9)
    run('ff_giua_' + k, raw.replace(u, u.replace(b' ', b' \x0c', 1), 1), 9)
    run('nul_giua_' + k, raw.replace(u, u.replace(b' ', b' \x00', 1), 1), 9)
    run('zwsp_giua_' + k, raw.replace(u, u.replace(b' ', ' ​'.encode(), 1), 1), 9)
    run('dong_khoang_trang_sau_' + k, raw.replace(u + b'\n', u + b'\n   \n', 1), 9)
    run('dong_tab_sau_' + k, raw.replace(u + b'\n', u + b'\n\t\n', 1), 9)
    run('dong_cr_sau_' + k, raw.replace(u + b'\n', u + b'\n\r\n', 1), 9)
    run('rao_ngay_sau_' + k, raw.replace(u + b'\n', u + b'\n```\nx\n```\n', 1), 9)
    run('comment_ngay_sau_' + k, raw.replace(u + b'\n', u + b'\n<!-- x -->\n', 1), 9)
    run('comment_trong_dong_' + k, raw.replace(u, u.replace(b' ', b' <!-- x --> ', 1), 1), 9)
    run('them_dong_rong_sau_' + k, raw.replace(u + b'\n', u + b'\n\n', 1), 0)
# che một khối khoá bằng comment mở ở khối trước, đóng ở khối sau, rồi đặt bản hiển thị ở cuối tệp
for k in ['K04', 'K05', 'K06', 'K02']:
    u = unit(k); assert raw.count(b'\n\n' + u + b'\n\n') == 1, k
    run('che_tai_cho_ban_hien_noi_khac_' + k, raw.replace(b'\n\n' + u + b'\n\n', b' <!--\n\n' + u + b'\n\n-->', 1) + b'\n' + u + b'\n', 9)
u = unit('K04'); run('ban_sao_trong_rao_co_dong_rong', raw + b'\n```\n\n' + u + b'\n\n```\n', 0)
run('ban_sao_trong_rao_dinh_lien', raw + b'\n```\n' + u + b'\n```\n', 0)
run('ban_sao_trong_comment', raw + b'\n<!--\n\n' + u + b'\n\n-->\n', 0)  # bị che trọn ⇒ không tính là bản thứ hai
run('bom_dau_tep', b'\xef\xbb\xbf' + raw, 9)
for ten, dong in [('id_zwsp', '| `INV-' + chr(0x200b) + '99` | x |'), ('id_shy', '| INV' + chr(0xad) + '-99 | x |'), ('id_fullwidth_digit', '| `INV-' + chr(0xff19) * 2 + '` | x |'),
                  ('id_fullwidth_bar', chr(0xff5c) + 'INV-99' + chr(0xff5c) + 'x' + chr(0xff5c)), ('id_debt_zwsp', '| INV-12-NO' + chr(0x200b) + ' | x |')]:
    run(ten, raw + b'\n\n' + dong.encode() + b'\n', 0 if ten == 'id_debt_zwsp' else 9)
run('crlf_toan_tep', raw.replace(b'\n', b'\r\n'), 9)
(D / 'ket_qua.json').write_text(json.dumps(rows, ensure_ascii=False, indent=1))
sai = [(r['case'], r['rc'], r['expected']) for r in rows if r['rc'] != r['expected']]
print('TONG', len(rows), 'LECH', len(sai), sai)
