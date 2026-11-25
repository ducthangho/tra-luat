import pathlib,json
w=pathlib.Path(__file__).resolve().parent;s=(w.parent/'repo/ops/gate_output_doi_chieu.py').read_text();rows=[]
def add(n,cu,moi):
 assert s.count(cu)==1,(n,s.count(cu));rows.append(dict(id=n,kind='order_or_missing_url',line=s[:s.index(cu)].count('\n')+1,src=s.replace(cu,moi)))
a='    if not isinstance(d, dict) or d.get("html_url") != url:\n        return ["html_url"]\n'
b='    if not (isinstance(d.get("user"), dict) and d["user"].get("login") == CHU_KHO and d.get("author_association") == "OWNER"):\n        return ["tac_gia"]\n'
c='    dong = [m for x in str(d.get("body")).splitlines() if (m := RE_MIEN.fullmatch(x.strip()))]\n    if len(dong) != 1:\n        return ["dong_mien"]\n'
add('waiver_order_author_url',a+b,'    if not isinstance(d, dict):\n        return ["html_url"]\n'+b+'    if d.get("html_url") != url:\n        return ["html_url"]\n')
add('waiver_order_line_author',b+c,c+b)
d='    try:\n        datetime.date.fromisoformat(m[4])\n    except ValueError:\n        return ["han"]\n'
e='    if "ubuntu-latest" not in m[2].split(","):\n        return ["os"]\n'
add('waiver_order_os_date',d+e,e+d)
add('url_zero_indexerror','if isinstance(gia_tri, str) else []) != 1:', 'if isinstance(gia_tri, str) else []) > 1:')
add('url_zero_optional','        return ["url"]\n','        return ["url"] if urls else []\n')
(w/'order_url_mutants.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in rows))
