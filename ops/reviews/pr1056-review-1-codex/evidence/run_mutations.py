from pathlib import Path
import json, subprocess, sys

work=Path(__file__).resolve().parent.parent
copy=work/'review-copy'
target='ops/reviews/pr1050-review-1-codex-verdict.md'
readme='ops/reviews/README.md'
receipt='ops/reviews/pr1050-review-1-codex-verdict.receipt.yaml'
summary={}
for label, path in [('byte',target),('toc',readme),('caveat',readme),('count',receipt)]:
    p=copy/path
    before=p.read_bytes()
    if label=='byte':
        after=before[:-1]+b' '
        assert sum(a!=b for a,b in zip(before,after))==1 and len(before)==len(after)
        detail=f'{path}: final LF -> space, bytes {len(before)} -> {len(after)}, changed_bytes=1'
    elif label=='count':
        assert before.count(b'so_p1: 1\n')==1
        after=before.replace(b'so_p1: 1\n',b'so_p1: 9\n')
        detail=f'{path}: so_p1 1 -> 9 (1 byte)'
    else:
        rows=before.splitlines(keepends=True)
        token=b'| [`pr1050-review-1-codex-verdict.md`]' if label=='toc' else b'| `pr1050-review-1-codex-verdict.md` | `TEP-LON-KHONG-VAO-KHO`'
        hit=[r for r in rows if r.startswith(token)]
        assert len(hit)==1
        after=b''.join(r for r in rows if r!=hit[0])
        detail=f'{path}: removed {label} row, removed_bytes={len(hit[0])}'
    p.write_bytes(after)
    with (work/'VERDICT.md').open('a') as f:
        f.write(f'\nĐỘT BIẾN `{label}` (chỉ trên clone từ mirror.git tại exact SHA): {detail}. LỆNH: `python3 evidence/run_mutations.py`; thao tác dữ liệu được ghi nguyên trong script.\n')
    try:
        run=subprocess.run([sys.executable,str(work/'evidence/run_gates.py'),str(copy),'mutant-'+label],cwd=work,capture_output=True,text=True)
        assert run.returncode==0,run.stderr
        data=json.loads((work/f'evidence/mutant-{label}-gates.json').read_text())
        summary[label]={'mutation':detail,'rc':{k:v['rc'] for k,v in data.items()},'summary':{k:v['summary'] for k,v in data.items()}}
        print(label, summary[label]['rc'],flush=True)
    finally:
        p.write_bytes(before)
    assert p.read_bytes()==before
    with (work/'VERDICT.md').open('a') as f:
        reds=[k for k,v in data.items() if v['rc']!=0]
        greens=[k for k,v in data.items() if v['rc']==0]
        f.write('Kết luận phản chứng: cổng ĐỎ='+repr(reds)+'; cổng KHÔNG CÓ RĂNG với đúng đột biến này='+repr(greens)+'. Đã phục hồi byte nguyên bản trước hướng tiếp theo.\n')
(work/'evidence/mutations-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(subprocess.check_output(['git','-C',str(copy),'status','--porcelain'],text=True) or 'clone status: clean',flush=True)
