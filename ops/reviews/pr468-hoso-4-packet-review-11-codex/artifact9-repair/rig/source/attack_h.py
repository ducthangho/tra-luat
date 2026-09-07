import copy, itertools, json, re
from harness import BASE_MOI, C, H, OUT, replay
P={k.split('/')[-1].replace('_test.py',''):k for k in C.MOI}
GREEN={
 'chon_reviewer':'nền: 25/25 đạt\nTỔNG: ĐẠT\n',
 'gh_readback':'gh_readback tests: 8/8 ca QUA (hong 0)\n',
 'mcp_gh':'CA         : 42/42 đạt · 0 đỏ · ĐẠT\nĐỘT BIẾN   : đã đo 54/54 tập giết · ĐẠT\nTỔNG: ĐẠT\n',
 'mcp_github_doc':'mcp_github_doc tests: 17/17 ca QUA (hong 0, bo qua 0)\n',
 'probe_mang':'tự đột biến cổng: 9/9 chết (m1..m5 + 4 dòng cơ chế)\nnamed mutant probe_missing_tool_executes_git: 1/1 chết\nnền: 11/11 đạt\nTỔNG: ĐẠT\n',
 'pretooluse_guard':'TONG: CA 39/39 dat · DOT BIEN 34/34 bi giet\nTONG: DAT\n',
 'subagent_ghi_detect':'TONG: CA 33/33 dat · DOT BIEN 22/22 bi giet\nTONG: DAT\n',
 'nhanh_don_duoc':'8/8\n',
}
rows=[]
def check(name,path,text,expected,mau=None,windows=False,kind='canonical'):
    try: result=replay(path,text,mau=mau,windows=windows)
    except Exception as e: result=type(e).__name__+': '+str(e)
    rows.append(dict(name=name,path=path,kind=kind,expected_red=expected,actual_red=result,text=text,mau=mau,windows=windows))

for name,path in P.items():
    text=GREEN[name]
    check('green-'+name,path,text,0)
    # Keep intact selected records; misleading SPAN text and fractions stay in prose.
    notes=['Ghi chú: DOT BIEN đã xem 3/5 hướng cải tiến.',
           'Thông tin: nền: 0/0 đạt; TỔNG: ĐẠT',
           'Một ví dụ CA : 0/999 đạt · 0 đỏ · ĐẠT',
           'trace => TONG: CA 0/0 dat · DOT BIEN 0/0 bi giet',
           'prefix gh_readback tests: 0/0 ca QUA (hong 0)',
           'ví dụ 99999999999999999999999/0 nằm ngoài bằng chứng',
           'Ghi chú: 31/12/2026 và tỷ lệ 0/1 chưa nghiệm thu',
           'Giải thích: ví dụ DOT BIEN 0/0 là bảng rỗng.',
           'unicode prose: ०/०; ０/９; Ⅲ/Ⅴ',
           'nguồn {"ca": [0,0], "version": "3/5"}',
           'ghi chú: signed -1/-1, decimal 0.5/1.5, exp 1e9/1e9',
           'ghi chú: literal regex (?:1/1|0/0) không phải số đo']
    lines=text.splitlines(keepends=True)
    for i in range(len(lines)+1):
        for n,note in enumerate(notes):
            check(f'prose-{name}-{i}-{n}',path,''.join(lines[:i])+note+'\n'+''.join(lines[i:]),0,kind='prose')
    records=H['TONG'][path]
    for ri,(selector,grammar) in enumerate(records):
        line=next(x for x in text.splitlines() if re.match(selector,x))
        for at in ('before','after'):
            for suffix in ('', '\t0/0', ': 0/0', '\u00a00/0', ' 0/0', ' '):
                label=line.split(':')[0]+':' if ':' in line else '0/0'
                bad=label+suffix
                if not re.match(selector,bad): continue  # declared selector boundary excluded
                full=bad+'\n'+text if at=='before' else text+bad+'\n'
                check(f'extra-record-{name}-{ri}-{at}-{suffix!r}',path,full,1,kind='duplicate')
        for pi,match in enumerate(re.finditer(r'\d+/\d+',line)):
            for pair in ('0/0','0/1','1/0','2/3','3/2','00/00','٠/٠'):
                changed=line[:match.start()]+pair+line[match.end():]
                check(f'bad-pair-{name}-{ri}-{pi}-{pair}',path,text.replace(line,changed),1,kind='pair')
        # Semantically equivalent ways to spell digit captures preserve source-position proof.
        for variant in (r'([0-9]+)', r'(\d{1,})', r'((?:\d)+)', r'((?=\d)\d+)', r'((?:\d{2}|\d+))'):
            changed=grammar.replace(r'(\d+)',variant)
            if changed==grammar: continue
            tong=copy.deepcopy(records); tong[ri]=(selector,changed)
            check(f'equiv-grammar-{name}-{ri}-{variant}',path,text,0,mau=(BASE_MOI[path],tong),kind='grammar-equivalent')
        # Literal fractions, duplicate groups, optional absent groups must fail law 7.
        gm=re.fullmatch(grammar,line)
        literal=re.escape(line)
        for changed in (literal, '('+grammar+')', grammar+r'(?: (\d+)/(\d+))?'):
            tong=copy.deepcopy(records); tong[ri]=(selector,changed)
            check(f'bad-grammar-{name}-{ri}-{changed}',path,text,1,mau=(BASE_MOI[path],tong),kind='grammar-hole')
# Exhaustive independent expected arithmetic, 625 cases. Neither integer nor fraction positions read from regex source.
path=P['mcp_gh']
for a,b,c,d in itertools.product(range(5),repeat=4):
    text=f'CA         : {a}/{b} đạt · 0 đỏ · ĐẠT\nĐỘT BIẾN   : đã đo {c}/{d} tập giết · ĐẠT\nTỔNG: ĐẠT\n'
    check(f'exhaustive-{a}-{b}-{c}-{d}',path,text,int(not(a==b and a>0 and c==d and c>0)),kind='exhaustive')
# The Windows consumer must choose replacement formats only, independent from environment prose.
path=P['pretooluse_guard']
win='TONG: CA 39/39 dat · DOT BIEN 34 muc KHONG DO TREN WINDOWS — do tren ubuntu-latest\nTONG: DAT\n'
for windows in (False,True):
    check(f'windows-form-{windows}',path,win,0 if windows else 1,windows=windows,kind='windows')
    check(f'linux-on-{windows}',path,GREEN['pretooluse_guard'],0,windows=windows,kind='windows')
    check(f'windows-duplicate-{windows}',path,win+'TONG: CA\t0/0\n',1,windows=windows,kind='windows')
    check(f'windows-empty-{windows}',path,win.replace('34 muc','0 muc'),1,windows=windows,kind='windows')
    check(f'linux-empty-{windows}',path,GREEN['pretooluse_guard'].replace('34/34','0/0'),1,windows=windows,kind='windows')
# Law 1 / law 5 bare-pattern cardinalities: groups 0..4, captured values positive or zero.
for n in range(5):
    for value in ('0','1'):
        span='X'+''.join(f'({value})' for _ in range(n))
        text='X'+value*n
        check(f'bare-{n}-{value}',P['nhanh_don_duoc'],text,int(not(n>0 and n%2==0 and value=='1')),mau=span,kind='bare-span')
# Retest exact old law7 failure modes with a zero-group SPAN so law7 alone decides.
path=P['mcp_gh']
for grammar,text,expect in [
 (r'T: (9)[/](9)','T: 9/9',0),
 (r'T: (9)\/(9)','T: 9/9',0),
 (r'T: (9)/(9)(?: \(schema 1/1\))?', 'T: 9/9',0),
 (r'T: (9)/(9)(?:1/1|\d+/\d+)', 'T: 9/90/0',1),
 (r'T: (9)/(9) (?:1/1|\d+/\d+)', 'T: 9/9 0/0',1),
 (r'T: (?=(\d+)/(\d+))(\d+)/(\d+)', 'T: 9/9',1),
 (r'T: (9)/(9) 0/0', 'T: 9/9 0/0',1),
 (r'T: (9)/(9) 33/34', 'T: 9/9 33/34',1),
]:
    check('law7-'+grammar,path,text,expect,mau=('T:', [('T:',grammar)]),kind='old-law7')
summary={'cases':len(rows),'false_red':sum(x['expected_red']==0 and x['actual_red']!=0 for x in rows),
 'missed':sum(x['expected_red']==1 and x['actual_red']==0 for x in rows),
 'exceptions':sum(isinstance(x['actual_red'],str) for x in rows),
 'by_kind':{k:sum(r['kind']==k for r in rows) for k in sorted({r['kind'] for r in rows})},
 'failures':[x for x in rows if x['expected_red']!=x['actual_red']]}
(OUT/'attack-h-cases.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
(OUT/'attack-h-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(summary,ensure_ascii=False,indent=2))
