"""Chỉ kiểm normalization/nhãn K4 của cb9ecc8; mọi biến đổi output là đối chứng oracle."""
import audit as A
import re, sys, types, unicodedata
T=A.T
rx=re.compile(r'\s'); label=re.compile(r'\s*K4\b'); plain=re.compile(r'K4\b')
regex_ws=[];strip_ws=[];diff=[];label_diff=[]
for cp in range(sys.maxunicode+1):
 c=chr(cp);a=rx.fullmatch(c) is not None;b=c.lstrip()==''
 if a:regex_ws.append(cp)
 if b:strip_ws.append(cp)
 if a!=b:diff.append(cp)
 s=c+'K4:S fresh'
 if bool(label.match(s))!=bool(plain.match(s.lstrip())):label_diff.append(cp)
A.emit(kind='unicode_exhaustive',python=sys.version,unicode=unicodedata.unidata_version,codepoints=sys.maxunicode+1,re_whitespace_count=len(regex_ws),lstrip_whitespace_count=len(strip_ws),difference=diff,label_difference=label_diff,whitespace=['U+%04X'%x for x in regex_ws])
assert not diff and not label_diff
cases=('duong_fixture','k4_base','k4_head','k4_ca_hai','a11_k3_k4','kieu_S','kieu_H')
white=['']+[chr(x) for x in regex_ws]
prefixes=white+[''.join(chr(x) for x in regex_ws), ''.join(chr(x) for x in reversed(regex_ws))]+[chr(a)+chr(b) for a in regex_ws for b in regex_ws]
counts={};failures=[]
for prefix in prefixes:
 for mode in ('valid','contradiction','K40','K3_mentions_K4'):
  def changed(raw,**params):
   result=A.M.kiem_json(raw,**params)
   if result['luat']['K4']=='do' and result['luat']['K1']=='qua':
    if mode=='valid':result['ly_do']=[prefix+x if x.startswith('K4:') else x for x in result['ly_do']]
    else:result['ly_do'].append(prefix+{'contradiction':'K4:S fresh, khong can chay lai','K40':'K40:S fresh','K3_mentions_K4':'K3: workflow co K4 trong ten'}[mode])
   return result
  proxy=types.SimpleNamespace(kiem_json=changed,__file__=A.M.__file__)
  for case in cases:
   actual=A.target(proxy,T.MODUN,case)
   rejected=mode=='contradiction' and case!='duong_fixture'
   ok=actual.startswith('TinHieuChotCa: '+case+': ly do K4 sai nghia:') if rejected else actual=='pass'
   counts[mode]=counts.get(mode,0)+1
   if not ok:failures.append(dict(prefix=ascii(prefix),mode=mode,case=case,result=actual))
A.emit(kind='oracle_matrix',prefixes=len(prefixes),cases=cases,calls=counts,failures=failures)
assert not failures
