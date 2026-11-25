from measure import *
sys.path.insert(0,str(PROTO/'.claude/dev'))
pl=mod('probe_pl',PROTO/'.claude/dev/packet_loop.py')
raw=(PROTO/'docs/PROTOCOL_DA_PHIEN.md').read_text()
scratch=OUT/'probe-root';(scratch/'docs').mkdir(parents=True,exist_ok=True)
f=scratch/'docs/PROTOCOL_DA_PHIEN.md'
def cli(text):
    f.write_text(text)
    return run([sys.executable,'-B',str(PROTO/'.claude/dev/packet_loop.py'),'doctrine-scan','--root',str(scratch)])
neo=[d.split(' | ',3) for d in blocks['neo'].splitlines()]
print('INTACT',cli(raw))
for n,k,h,text in neo:
    matches=list(re.finditer(r'\s+'.join(map(re.escape,text.split())),raw));assert len(matches)==1
    match=matches[0];r=cli(raw[:match.start()]+raw[match.end():])
    print('REMOVE',n,'RC',r[0],'LABELS',re.findall(r'neo (N\d+)',r[2]))
print('REMOVE_8_3',cli(raw[:raw.index('### 8.3 ')]+raw[raw.index('## 9. EOL'):]))
row=next(d for d in raw.splitlines() if d.startswith('| `INV-07`'))
print('TABLE_BLANK_LINE',cli(raw.replace(row,'\n'+row,1)))
table_lines=[d for d in raw.splitlines() if d.startswith('| `INV-')]
print('TABLE_BLANK_EVERY_ROW',cli(raw.replace('\n'.join(table_lines),'\n\n'.join(table_lines),1)))
print('TABLE_DELETE',cli(raw.replace(row+'\n','',1)))
# Counterexample to N8: a harmless unreachable pass extends the preceding old function,
# but remains inside the same permitted insertion hunk before cmd_doctrine_scan.
path=PROTO/'.claude/dev/packet_loop.py';orig=path.read_text()
anchor='# --- ADR-0068:';assert orig.count(anchor)==1
before=run(['git','-C',str(PROTO),'diff','-U0','--','.claude/dev/packet_loop.py'])[1]
try:
    modified=orig.replace(anchor,'    pass\n\n'+anchor,1);path.write_text(modified)
    after=run(['git','-C',str(PROTO),'diff','-U0','--','.claude/dev/packet_loop.py'])[1]
    def node(s):return next(n for n in ast.parse(s).body if isinstance(n,ast.FunctionDef) and n.name=='_doc_nguon_protocol')
    a,b=node(orig),node(modified)
    print('N8_OLD_FUNCTION_CHANGED',ast.dump(a)!=ast.dump(b),'HUNKS',before.count('\n@@'),after.count('\n@@'),'NUMSTAT',run(['git','-C',str(PROTO),'diff','--numstat','--','.claude/dev/packet_loop.py'])[1])
    (OUT/'n8-counterexample.diff').write_text(after)
finally:path.write_text(orig)
print('R1_CUTOVER_CONTRACT','ngày của H không tham gia; bốn ô đều theo start >= T')
print('R1_SCHEMA_CONTRACT','v2 độc lập; google_antigravity + họ model + surface + transport; chưa có schema hợp đồng r2')
print('LEASE_NORMALIZATION_SPEC_CASEFOLD','case-fold' in spec.split('**3b')[1].split('**3c')[0] or 'casefold' in spec.split('**3b')[1].split('**3c')[0])
