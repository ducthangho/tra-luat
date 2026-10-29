import difflib
import shutil
from review_common import HEAD, SCRATCH, WORK, case, emit, invoke, load_tests, run

rel = 'ops/bien_nhan_v2_test.py'
original = (HEAD / rel).read_text()
needle = '''            ("v-provider-dong-sau", "execution_surface: codex_service\\nprovider: openai_codex\\n", 1)):'''
replacement = '''            ("v-provider-dong-sau", "execution_surface: codex_service\\nprovider: openai_codex\\n", 1),
            ("vi-provider-truoc-hai-dong", "provider: openai_codex\\n\\nexecution_surface: codex_service\\n", 0),
            ("vii-provider-sau-hai-dong", "execution_surface: codex_service\\n\\nprovider: openai_codex\\n", 0),
            ("viii-trich-dan-truoc-hai-dong", "ops/x/v.md:6\\n\\nprovider: openai_codex execution_surface: codex_service\\n", 1),
            ("ix-trich-dan-sau-hai-dong", "provider: openai_codex execution_surface: codex_service\\n\\nops/x/v.md:6\\n", 1)):'''
assert original.count(needle) == 1
updated = original.replace(needle, replacement)
doc_old = '''    ⇒ rc=0; (v) `provider` ở dòng SAU cũng thuộc cửa sổ ⇒ rc=1."""'''
doc_new = '''    ⇒ rc=0; (v) `provider` ở dòng SAU cũng thuộc cửa sổ ⇒ rc=1. Hai dòng cách xa là NGOÀI cửa sổ:
    provider ngoài cửa sổ không tạo tự khai; trích dẫn ngoài cửa sổ không miễn tự khai."""'''
assert updated.count(doc_old) == 1
updated = updated.replace(doc_old, doc_new)
anchor = '''    do("m130_bo_chot_GRAFTS", lambda: _dot_bien_tep('''
extra = '''    # Cửa sổ M4 đúng ba dòng, không được nới thêm về phía trước hoặc phía sau.
    do("m140_B4_noi_cua_so_ve_truoc", lambda: _dot_bien_tep(
        "cua = dong_tep[max(0, j - 1):j + 2]", "cua = dong_tep[max(0, j - 2):j + 2]"),
       "c88_B4_LOI_TU_KHAI_surface_can_provider_va_khong_trich_dan", "provider/citation cách hai dòng là ngoài cửa sổ", doi_chung=DC)
    do("m141_B4_noi_cua_so_ve_sau", lambda: _dot_bien_tep(
        "cua = dong_tep[max(0, j - 1):j + 2]", "cua = dong_tep[max(0, j - 1):j + 3]"),
       "c88_B4_LOI_TU_KHAI_surface_can_provider_va_khong_trich_dan", "provider/citation cách hai dòng là ngoài cửa sổ", doi_chung=DC)
'''
assert updated.count(anchor) == 1
updated = updated.replace(anchor, extra + anchor)
patch = WORK / 'HINT.patch'
patch.write_text('# chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit\n' +
                 ''.join(difflib.unified_diff(original.splitlines(True), updated.splitlines(True), fromfile=rel, tofile=rel)))
root = SCRATCH / 'hint'
shutil.copytree(HEAD, root)
assert run(['patch', '--dry-run', '--fuzz=0', '-p0', '-i', patch], cwd=root).returncode == 0
assert run(['patch', '--fuzz=0', '-p0', '-i', patch], cwd=root).returncode == 0
t = load_tests(root)
assert invoke(t, 'c88')[0] == 'qua'
original_module, original_cong = t.bnv2, t.CONG
for direction, new in [('before', 'cua = dong_tep[max(0, j - 2):j + 2]'),
                       ('after', 'cua = dong_tep[max(0, j - 1):j + 3]')]:
    t._dot_bien_tep('cua = dong_tep[max(0, j - 1):j + 2]', new)
    emit(direction=direction)
    assert invoke(t, 'c88')[0] == 'giet_that'
    emit(control=t._sach_hoan_toan(case(t, 'c18')))
    t.bnv2, t.CONG = original_module, original_cong
