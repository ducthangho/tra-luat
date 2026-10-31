import contextlib
import hashlib
import importlib.util
import io
from pathlib import Path
import shutil
from record import REPO, record

spec = importlib.util.spec_from_file_location('suite', REPO/'ops/bien_nhan_v2_test.py')
t = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)

targets = {
    'm142_chon_bien_nhan_so_duoi_CHINH_XAC': 'c101_',
    'm147_bo_chon_bo_bat_OSError': 'c99_',
    'm153_hoi_trang_thai_bat_Exception': 'c100_',
    'm156_B4_bo_chan_bien_dau_tep': 'c88_',
    'm157_B4_trich_dan_bo_dong_sau': 'c88_',
}
seen = []
real_mutate = t._dot_bien_tep
def checked_mutate(*args, **kwargs):
    real_mutate(*args, **kwargs)
    copy_path = Path(t.bnv2.__file__).resolve()
    assert not copy_path.is_relative_to(REPO.resolve())
    assert copy_path.read_bytes() != Path(t._BNV2_THAT.__file__).read_bytes()
    seen.append(copy_path)
t._dot_bien_tep = checked_mutate

buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    rows = t._dot_bien(chi=set(targets))
assert len(rows) == len(targets) == len(seen)
for name, ca, passed, state, detail, selfcheck, control in rows:
    assert state == 'giet_that' and passed and ca.startswith(targets[name]), rows
    assert control and not selfcheck
assert not t._TAM_DOT_BIEN
record('h05','Năm đột biến chỉ định chạy riêng qua _dot_bien_tep và đối chứng',
       'PYTHONDONTWRITEBYTECODE=1 python3 evidence/mutations.py',
       buf.getvalue() + f'\n5/5 đúng ca đích; 5/5 giet_that; 5/5 đối chứng sạch; 5/5 tệp đột biến ngoài cay-kho; còn bản sao tạm={len(t._TAM_DOT_BIEN)}\n')

# C2 + các điểm lỗi hệ thống/lập trình, chạy ca dương trước phản chứng riêng.
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    for prefix in ('c89_', 'c99_', 'c100_', 'c101_'):
        fn = next(f for f in t.CA if f.__name__.startswith(prefix))
        state, detail = t._chay_1(fn)
        print(fn.__name__ + ' = ' + state + '; ' + str(detail))
        assert state == 'qua', (state,detail)
    extra = {'m143_chon_bien_nhan_loc_is_file',
             'm144_sinh_no_loc_duoi_CHINH_XAC', 'm145_bo_chon_khong_sap_xep',
             'm146_bo_chon_bo_nhanh_thu_muc_vang',
             'm148_bo_chon_hoi_is_dir_TRAN', 'm149_kiem_guard_hoi_is_dir_TRAN',
             'm150_hoi_trang_thai_bo_bat_OSError', 'm151_kiem_hoi_git_TRAN',
             'm152_bo_chon_bat_Exception', 'm154_hoi_trang_thai_chi_bat_PermissionError',
             'm155_bo_chon_chi_bat_PermissionError'}
    rows = t._dot_bien(chi=extra)
    assert len(rows) == len(extra) and all(x[2] and x[3] == 'giet_that' for x in rows)
record('h10','C2 và các nhánh sinh nợ, thứ tự, vắng thư mục, OSError và lỗi lập trình',
       'PYTHONDONTWRITEBYTECODE=1 python3 evidence/mutations.py',buf.getvalue())

# C3: đột biến glob chỉ dành cho phép đo tại chỗ, không thêm vào bảng thường.
buf = io.StringIO()
source = 'ds = [p for p in tm.iterdir() if p.name.lower().endswith(".receipt.yaml")]'
try:
    with contextlib.redirect_stdout(buf):
        t._dot_bien_tep(source, 'ds = list(tm.glob("*.receipt.yaml"))')
        fn = next(f for f in t.CA if f.__name__.startswith('c101_'))
        state, detail = t._chay_1(fn)
        print('glob-revert -> ' + fn.__name__ + ' = ' + state)
        print('detail=' + str(detail))
        assert state == 'giet_that', (state, detail)
        dc = next(f for f in t.CA if f.__name__.startswith('c18_'))
        ok, why = t._sach_hoan_toan(dc)
        print('control=' + dc.__name__ + '; clean=' + str(ok) + '; reason=' + why)
        assert ok
finally:
    t.bnv2 = t._BNV2_THAT
    t.CONG = Path(t._BNV2_THAT.__file__)
    while t._TAM_DOT_BIEN:
        shutil.rmtree(t._TAM_DOT_BIEN.pop())
record('h06','C3 hoàn nguyên glob trên bản sao tạm',
       'PYTHONDONTWRITEBYTECODE=1 python3 evidence/mutations.py',buf.getvalue())
