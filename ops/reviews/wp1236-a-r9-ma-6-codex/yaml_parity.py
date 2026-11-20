import yaml,pathlib,json,copy,sys,collections
w=pathlib.Path(__file__).resolve().parent;r=w.parent/'repo';report=[]
# Derive malformed files by altering copied scalar values or whitespace from an actual provenance document.
src=(r/'ops/land/pr1440-wp1319-provenance/ci-provenance-44669622916/provenance.yaml').read_text()
bs=chr(92)
vectors={'original':src,'tab_after_colon':src.replace(': ',':\t',1),'tab_trailing':src.replace('\n','\t\n',1),'invalid_unicode_escape':src.replace('ci_provenance/1','"'+bs+'U00110000"',1),'surrogate_escape':src.replace('ci_provenance/1','"'+bs+'uD800"',1),'unicode_nextline':src.replace('\n','\u0085',1),'crlf':src.replace('\n','\r\n'),'duplicate_schema':src+'\nschema: ci_provenance/1\n','truncated':src[:len(src)//2]}
def read(x,loader):
 try:return ('ok',yaml.load(x,Loader=loader))
 except Exception as e:return (type(e).__name__,None)
for label,data in vectors.items():
 a=read(data,yaml.SafeLoader);b=read(data,yaml.CSafeLoader);row={'name':label,'safe':a[0],'c_safe':b[0],'same':a==b};report.append(row);print(row)
 if a!=b:(w/('yaml_'+label+'.yaml')).write_text(data)
(w/'yaml_parity.json').write_text(json.dumps(report,indent=2))
