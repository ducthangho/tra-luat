from pathlib import Path
import difflib, yaml
work=Path(__file__).resolve().parent.parent
chunks=[]
for n in (1,2):
    path=f'ops/reviews/pr1050-review-{n}-codex-verdict.receipt.yaml'
    old=(work/'cay-kho'/path).read_text()
    d=yaml.safe_load(old)
    prefix='review_class: standard\nreview_class_ghi_chu: '+next(l.split(': ',1)[1] for l in old.splitlines() if l.startswith('review_class_ghi_chu: '))+'\n'
    count=32 if n==1 else 33
    replacement=(
        'review_class: sensitive\n'
        'effective_review_class: sensitive\n'
        "review_class_ghi_chu: '(a) Protocol section 8: class khong ro xu ly nhu sensitive; "
        f"_tinh_lop_tu_write_set tren {count} tep cua diff b29da0b..{d['reviewed_sha'][:7]} tra sensitive "
        "(fail-closed cho path chua phan loai), khong dung class standard. "
        "(b) Khong co lease rieng; PR chi ghi so du lieu ops/reviews/** va ops/land/**; khong co override class co audit.'\n"
    )
    assert old.count(prefix)==1
    new=old.replace(prefix,replacement)
    parsed=yaml.safe_load(new)
    assert parsed['review_class']==parsed['effective_review_class']=='sensitive'
    chunks.extend(difflib.unified_diff(old.splitlines(keepends=True),new.splitlines(keepends=True),fromfile=path,tofile=path))
hint='chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit\nPatch-as-hint: chỉ sửa metadata phân lớp; không sửa verdict nguyên byte.\n'+''.join(chunks)
(work/'HINT.patch').write_text(hint)
print('HINT.patch generated; files=2, metadata_only=True')
