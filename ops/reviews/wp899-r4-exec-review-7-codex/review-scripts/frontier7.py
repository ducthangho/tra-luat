from pathlib import Path
import ast,sys,os,json,subprocess,concurrent.futures,collections
R=Path(__file__).resolve().parent;root=R.parent
src=(root/'ops/ci_provenance.py').read_text();out=R/'frontier7';out.mkdir(exist_ok=True)
known=set()
for folder in [root/'ops',root/'.review-input/tu-dot-bien']+[root/f'.review-input/r4-luot{i}' for i in range(1,7)]:
 for p in folder.glob('*.py'):
  try:a=ast.parse(p.read_text())
  except Exception:continue
  for n in ast.walk(a):
   if isinstance(n,(ast.Tuple,ast.List)):
    try:v=ast.literal_eval(n)
    except Exception:continue
    if len(v)>=3 and all(type(x) is str for x in v[:3]):known.add((v[1],v[2]))
M=[]
def add(n,a,b):M.append((n,a,b))
add('job_key_equals_alias_reject','type(ten) is str and type(j) is dict and any(', 'type(ten) is str and type(j) is dict and k != j.get("name") and any(')
add('job_alias_suffix_only_key','for x in (k, j.get("name"))','for x in (k, j.get("name")) if x == k or ten == x')
add('job_suffix_no_dot','r"(?: \\(.*\\))?"','r"(?: \\([^.] *\\))?"'.replace('[^.] *','[^.]*'))
add('job_alias_unicode_reject','type(x) is str and x and "${{"','type(x) is str and x.isascii() and x and "${{"')
add('job_alias_trim','for x in (k, j.get("name"))','for x in (k.strip() if type(k) is str else k, j.get("name").strip() if type(j.get("name")) is str else j.get("name"))')
add('job_alias_matches_duplicate_count','return khop[0] if len(khop) == 1 else None','return khop[0] if len(khop) == 1 and not (wf["jobs"][khop[0]].get("name") == khop[0]) else None')
add('name_explicit_strip','return s["name"] if _chuoi(s["name"])','return s["name"].strip() if _chuoi(s["name"])')
add('name_explicit_unicode_reject','_chuoi(s["name"]) and "${{"','_chuoi(s["name"]) and s["name"].isascii() and "${{"')
add('name_uses_whole_value','"Run " + v.split("\\n")[0]','"Run " + (v.split("\\n")[0] if "run" in s else v)')
add('name_run_empty_first_reject','v = s.get("run", s.get("uses"))','v = s.get("run", s.get("uses"))\n    if type(v) is str and v.startswith("\\n"): return None')
add('name_run_strip_cr','v.split("\\n")[0]','v.split("\\n")[0].rstrip("\\r")')
add('time_same_year','a <= h <= z','a <= h <= z and a.year == h.year == z.year')
add('time_same_month','a <= h <= z','a <= h <= z and a.month == h.month == z.month')
add('time_24h_window','a <= h <= z','a <= h <= z and z - a < datetime.timedelta(days=1)')
add('time_century_leap_reject','type(v) is str and RE_GIO.fullmatch(v)','type(v) is str and RE_GIO.fullmatch(v) and not (v[5:10] == "02-29" and int(v[:4]) % 100 == 0)')
add('time_year_9999_reject','type(v) is str and RE_GIO.fullmatch(v)','type(v) is str and RE_GIO.fullmatch(v) and v[:4] != "9999"')
add('time_year_0001_reject','type(v) is str and RE_GIO.fullmatch(v)','type(v) is str and RE_GIO.fullmatch(v) and v[:4] != "0001"')
add('time_date_only_compare','a <= h <= z','a.date() <= h.date() <= z.date()')
add('time_clock_only_compare','a <= h <= z','a.time() <= h.time() <= z.time()')
add('time_whitespace_strip','RE_GIO.fullmatch(v)','RE_GIO.fullmatch(v.strip())')
add('time_invalid_century_accept','except ValueError:\n        return None','except ValueError:\n        return datetime.datetime(1900, 2, 28) if type(v) is str and v[:10] == "1900-02-29" else None')
add('rest_number_no_gaps','len({s["number"] for s in st}) == len(st)','len({s["number"] for s in st}) == len(st) and (not st or max(s["number"] for s in st)-min(s["number"] for s in st)+1 == len(st))')
add('rest_number_metadata_ignored_validation','for s in st)\n            and len({s["number"] for s in st})','for s in st if type(s) is not dict or s.get("name") not in ("Set up job", "Complete job"))\n            and len({s["number"] for s in st})')
add('rest_metadata_time_required','if not all((a := _gio(','if any(not _gio(s.get("started_at")) or not _gio(s.get("completed_at")) for s in st if s.get("name") in ("Set up job", "Complete job") or str(s.get("name")).startswith("Post ")) or not all((a := _gio(')
add('rest_filter_post_number_order','and not str(s.get("name")).startswith("Post ")]','and not (str(s.get("name")).startswith("Post ") and s["number"] > 1)]')
add('rest_filter_skipped_uses_only','s.get("conclusion") != "skipped"]','s.get("conclusion") != "skipped" or "uses" not in sy[i]]')
add('rest_names_only_ran','for s, y in zip(ung, sy)):','for s, y in zip(ung, sy) if s.get("conclusion") != "skipped"):')
add('rest_number_max_as_count','if len(ung) != len(sy):','if (max((s["number"] for s in ung), default=0) != len(sy)+1) or len(ung) != len(sy):')
add('mode_env_present_values_only','any(str(k).startswith("CI_DANG_KY_") for k in d["env"])','any(str(k).startswith("CI_DANG_KY_") and d["env"][k] is not None for k in d["env"])')
add('mode_env_empty_key_reject','_env_chan(j) or','(_env_chan(j) or (type(j.get("env")) is dict and "" in j["env"])) or')
add('mode_env_unicode_key_reject','_env_chan(j) or','(_env_chan(j) or (type(j.get("env")) is dict and any(not str(k).isascii() for k in j["env"]))) or')
add('mode_prior_skip_uses','for t in j["steps"][:i]))','for t in j["steps"][:i] if "uses" not in t))')
add('mode_prior_skip_skipped','for t in j["steps"][:i]))','for t in j["steps"][:i] if t.get("if") != "false"))')
add('mode_prior_only_unblocked','for t in j["steps"][:i]))','for t in j["steps"][:i] if not set(t) - KHOA_BUOC))')
add('mode_prior_strip_empty_run','str(t.get("run", ""))','str(t.get("run") or "")')
add('mode_step_shell_nonempty','s.get("shell", "bash") not in','(s.get("shell") or "bash") not in')
add('dd_first_match_lines_only','k.group(0).splitlines() if k else []','k.group(0).splitlines()[:1] if k else []')
add('dd_last_match_lines_only','k.group(0).splitlines() if k else []','k.group(0).splitlines()[-1:] if k else []')
add('dd_blank_output_lines_remove','"\\n".join(b["phan"]) + "\\n"','"\\n".join(x for x in b["phan"] if x) + "\\n"')
add('dd_no_output_final_newline','"\\n".join(b["phan"]) + "\\n"','"\\n".join(b["phan"])')
add('dd_dedup_output_lines','"\\n".join(b["phan"]) + "\\n"','"\\n".join(dict.fromkeys(b["phan"])) + "\\n"')
add('dd_sort_output_lines','"\\n".join(b["phan"]) + "\\n"','"\\n".join(sorted(b["phan"])) + "\\n"')
add('dd_sort_match_lines','k.group(0).splitlines() if k else []','sorted(k.group(0).splitlines()) if k else []')
add('dd_wrong_lenh_first_call','"lenh": b["lenh"], "duong_dan": duong','"lenh": next(iter(moi)), "duong_dan": duong')
add('dd_truncate_path','"duong_dan": duong','"duong_dan": duong.split("/")[-1]')
add('dd_step_dedup_paths','for b, (k, i) in zip(buoc, ghep or []):','for b, (k, i) in zip(buoc, ghep or []):\n        if any(x["lenh"] == b["lenh"] for x in kq): continue')
add('dd_validated_step_count_calls','so += 1','so += bool(RE_LOI_GOI.fullmatch(run.rstrip("\\n")))')
add('log_output_ignore_indented_blank','buoc[-1]["phan"].append(t)','buoc[-1]["phan"].append(t.rstrip())')
add('log_header_strip','t[len("##[group]Run "):]','t[len("##[group]Run "):].strip()')
add('log_empty_metadata_reject','not b["tien_to"] or t.startswith("shell: ")','(not b["tien_to"] and bool(t)) or t.startswith("shell: ")')
add('log_second_shell_reject','not b["tien_to"] or t.startswith("shell: ")','(not b["tien_to"] and not t.startswith("shell: ")) or (b["tien_to"] and t.startswith("shell: "))')
add('log_output_drop_group_lines','buoc[-1]["phan"].append(t)','buoc[-1]["phan"].extend([t] if not t.startswith("##[group]") else [])')
add('log_require_output_nonempty','not b["mo"] and b["ok"]','not b["mo"] and bool(b["phan"]) and b["ok"]')
add('log_require_metadata_no_ansi','b["ok"] and not mau','b["ok"] and not mau and "\\x1b[" not in d')
add('log_color_run_not_contains_shell','elif mau and b["tien_to"]:','elif mau and b["tien_to"] and not t.startswith("shell: "):')
add('log_header_full_timestamp_required','"gio": d[:19] + "Z"','"gio": d[:19] + "Z" if RE_DONG.match(d) else ""')
add('log_same_header_body_len_reject','b["in_lai"][:1] == [b["lenh"]]','b["in_lai"][:1] == [b["lenh"]] and len(b["in_lai"]) == len(set(b["in_lai"]))')
def cases(path):
 code="import importlib.util as u,json;s=u.spec_from_file_location('t',%r);t=u.module_from_spec(s);s.loader.exec_module(t);rows=[]\nfor c in sorted(t.CA,key=lambda c:c.startswith('c49')):\n rc,o=t.chay_ca(c);rows.append((c,rc,o))\n if rc==3 and o.startswith('DO:'+c+':'):break\nprint(json.dumps(rows))"%str(root/'ops/ci_provenance_test.py')
 cmd=[sys.executable,'-B','-c',code]
 p=subprocess.run(cmd,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',CI_PROVENANCE_MA=str(path)),timeout=900)
 try:res=json.loads(p.stdout)
 except Exception:res=[('import',4,(p.stdout+p.stderr).decode('utf8','replace'))]
 return cmd,p,res
if __name__=='__main__':
 cmd,p,base=cases(root/'ops/ci_provenance.py');assert p.returncode==0 and len(base)==50 and all(rc==0 for c,rc,o in base)
 (out/'baseline.json').write_text(json.dumps(base,ensure_ascii=False,indent=2))
 def one(v):
  n,a,b=v;d={'name':n,'old':a,'new':b,'count':src.count(a),'new_vs_given_inventory':(a,b) not in known}
  if src.count(a)!=1:return d|{'rank':'HONG_NEO'}
  path=out/(n+'.py');path.write_text(src.replace(a,b));cmd,p,cs=cases(path)
  (out/(n+'.stdout')).write_bytes(p.stdout);(out/(n+'.stderr')).write_bytes(p.stderr)
  ks=[c for c,rc,o in cs if rc==3 and o.startswith('DO:'+c+':')];err=[{'case':c,'rc':rc,'output':o} for c,rc,o in cs if rc and not(rc==3 and o.startswith('DO:'+c+':'))]
  return d|{'source':str(path),'command':cmd,'rc':p.returncode,'rank':'GIET+NEM' if ks and err else 'GIET' if ks else 'TIN_DUNG_GIA' if err else 'SONG_SOT','killed':ks,'other_errors':err,'cases':cs}
 rows=[]
 with concurrent.futures.ThreadPoolExecutor(3) as ex:
  for r in ex.map(one,M):
   rows.append(r);(out/'results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print(r['name'],r['rank'],r.get('killed'),flush=True)
 print(collections.Counter(x['rank'] for x in rows))
