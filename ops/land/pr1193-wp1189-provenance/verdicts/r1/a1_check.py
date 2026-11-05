import yaml,sys
st=yaml.safe_load(open(sys.argv[1]))['jobs']['dang']['steps']
idx=[i for i,s in enumerate(st) if str(s.get('uses','')).startswith('actions/setup-python@')]
co=[i for i,s in enumerate(st) if str(s.get('uses','')).startswith('actions/checkout@')]
py=[i for i,s in enumerate(st) if 'python3' in str(s.get('run',''))]
ok=len(idx)==1 and str(st[idx[0]].get('with',{}).get('python-version'))=="3.12" and co[0]<idx[0]<min(py)
print('DAT' if ok else 'DO'); sys.exit(0 if ok else 1)
