from pathlib import Path
import difflib
p=Path('/tmp/wp960-r2-Dt2G8H/repo/ops/bien_nhan_v2.py');old=p.read_text();new=old
pairs=[
('''    try:
        cay = yaml.compose(van, Loader=yaml.SafeLoader)
    except yaml.YAMLError:
        return False
    return any(cau in _cac_cau(n.value) for _, n, _ in _duyet_scalar(cay))
''','''    try:
        cay = yaml.compose(van, Loader=yaml.SafeLoader)
        return any(cau in _cac_cau(n.value) for _, n, _ in _duyet_scalar(cay))
    except (yaml.YAMLError, _AliasVong) as ex:
        raise KhongDoDuoc(f"không duyệt được phiên bản YAML lịch sử ({type(ex).__name__})") from ex
'''),
('''        if p.returncode != 0:
            continue                       # commit xoá tệp: phiên bản ấy không có câu
''','''        if p.returncode != 0:
            # Chỉ bỏ qua khi tree xác nhận tệp vắng. Blob thiếu/lỗi show không chứng minh câu vắng.
            rc_tree, entry = _git(root, "ls-tree", c, "--", rel)
            if rc_tree != 0 or entry:
                return None
            continue
'''),
('''        ten, b = p.name, _bam(p)
        try:
            van = p.read_text(encoding="utf-8")
''','''        ten = p.name
        try:
            b = _bam(p)
            van = p.read_text(encoding="utf-8")
''')]
for a,b in pairs:
 assert new.count(a)==1,(new.count(a),a)
 new=new.replace(a,b)
Path('HINT.patch').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='ops/bien_nhan_v2.py',tofile='ops/bien_nhan_v2.py')))
