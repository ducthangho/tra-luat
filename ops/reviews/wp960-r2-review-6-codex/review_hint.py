import difflib
from pathlib import Path
import shutil
import subprocess
from review_checks import ROOT, TMP, E, record
from review_mutations import load, VARIANTS

source=ROOT/'ops/bien_nhan_v2_test.py'
old=source.read_text()
new=old
changes=[
    ('    thuần số / thuần chữ không ngữ cảnh ⇒ bỏ qua (rc=0). Trộn số-chữ đã có ở `c71`, OID thật ở `c78`.\n',
     '    thuần số / thuần chữ không ngữ cảnh ⇒ bỏ qua (rc=0). Trộn số-chữ đo RIÊNG không từ commit/backtick;\n    OID thật ở `c78`.\n'),
    ('                             ("sau-commit", "Commit 1234567 chua vao master.", 2),\n',
     '                             ("sau-commit", "Commit 1234567 chua vao master.", 2),\n                             ("tron-so-chu-rieng", "Ban 12ab34c chua vao master.", 2),\n'),
    ('            ("ung-vien-missing", lambda r: bnv2._commit_cua(r, "abcdef1"),\n',
     '            ("batch-check-sai-oid", lambda r: bnv2._commit_cua(r, "abcdef1"),\n             {"rev-parse --disambiguate": h + "\\n", "cat-file": "b" * 40 + " commit\\n"}),\n            ("batch-check-sai-loai", lambda r: bnv2._commit_cua(r, "abcdef1"),\n             {"rev-parse --disambiguate": h + "\\n", "cat-file": h + " nonsense\\n"}),\n            ("ung-vien-missing", lambda r: bnv2._commit_cua(r, "abcdef1"),\n'),
    ('    do("m130_bo_chot_GRAFTS", lambda: _dot_bien_tep(\n',
     '''    # Review r2 lượt 6: từng vế giao thức và từng ngữ cảnh phải có răng riêng.
    do("m137_bo_so_OID_batch_check", lambda: _dot_bien_tep(
        ' or ra[0] != oid40', ''),
       C94, "batch-check trả OID khác mà được tin", doi_chung=DC)
    do("m138_bo_kiem_loai_batch_check", lambda: _dot_bien_tep(
        ' or ra[1] not in ("commit", "tag", "tree", "blob")', ''),
       C94, "batch-check trả loại ngoài giao thức mà được tin", doi_chung=DC)
    do("m139_bo_ngu_canh_tron_so_chu", lambda: _dot_bien_tep(
        'if len(x) == 40 or _oid_tron(x):', 'if len(x) == 40:'),
       "c87_B3_OID_khong_tra_duoc_theo_NGU_CANH", "OID trộn số-chữ thiếu mà thành token thường", doi_chung=DC)
    do("m130_bo_chot_GRAFTS", lambda: _dot_bien_tep(
''')
]
for a,b in changes:
    assert new.count(a)==1, a
    new=new.replace(a,b)
hint=ROOT.parent/'HINT.patch'
hint.write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile='ops/bien_nhan_v2_test.py',tofile='ops/bien_nhan_v2_test.py')))
dr=TMP/'hint'
assert not dr.exists(), dr
shutil.copytree(ROOT,dr,symlinks=True)
for args in [['patch','--dry-run','--fuzz=0','-p0','-i',str(hint)], ['patch','--fuzz=0','-p0','-i',str(hint)]]:
    p=subprocess.run(args,cwd=dr,capture_output=True,text=True)
    print(' '.join(args), 'rc=',p.returncode,p.stdout,p.stderr,flush=True)
    assert p.returncode==0
assert (dr/'ops/bien_nhan_v2_test.py').read_text()==new
t=load(dr/'ops/bien_nhan_v2_test.py','hint_test')
for name in ['c94_giao_thuc_git_DANG_LA_la_KHONG_DO_DUOC','c87_B3_OID_khong_tra_duoc_theo_NGU_CANH']:
    result=t._chay_1(getattr(t,name))
    print('head',name,result,flush=True)
    assert result[0]=='qua'
for name,target in [('v1-batch-oid','c94_giao_thuc_git_DANG_LA_la_KHONG_DO_DUOC'),('v2-batch-type','c94_giao_thuc_git_DANG_LA_la_KHONG_DO_DUOC'),('v3-mixed-context','c87_B3_OID_khong_tra_duoc_theo_NGU_CANH')]:
    orig,cong=t.bnv2,t.CONG
    try:
        a,b,_=VARIANTS[name]
        t._dot_bien_tep(a,b)
        result=t._chay_1(getattr(t,target))
        control=t._chay_1(t.c18_neo_git_DUNG_thi_qua)
        print(name,result,'control=',control,flush=True)
        assert result[0]=='giet_that' and control[0]=='qua'
    finally:
        t.bnv2,t.CONG=orig,cong
        while t._TAM_DOT_BIEN:
            shutil.rmtree(t._TAM_DOT_BIEN.pop(),ignore_errors=True)
record('HINT.patch kiểm trên bản sao exact HEAD', 'Lệnh `python3 -B -u review_hint.py`: tạo HINT.patch dạng `patch -p0`; `patch --dry-run --fuzz=0 -p0 -i HINT.patch` trên bản sao tại78c138f rc=0, `checking file ops/bien_nhan_v2_test.py`, không fuzz/offset. Sau áp trên scratch: c94/c87 nguyên trạng qua; v1/v2/v3 đều `giet_that` vì đúng batch-check-sai-oid / batch-check-sai-loai / tron-so-chu-rieng; đối chứng c18 qua. Gợi ý chỉ sửa test, chưa áp vào cay-kho; chưa khai full suite của hint. Log `evidence/hint-validation.log`.')
