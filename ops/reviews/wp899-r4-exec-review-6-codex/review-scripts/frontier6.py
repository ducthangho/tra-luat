from pathlib import Path
import ast,sys,os,json,subprocess,concurrent.futures,collections
R=Path(__file__).resolve().parent;root=R.parent
src=(root/'ops/ci_provenance.py').read_text();out=R/'frontier6';out.mkdir(exist_ok=True)
M=[]
def add(n,o,v): M.append((n,o,v))
add('job_nested_parentheses', 'r"(?: \\(.*\\))?"', 'r"(?: \\([^()]*\\))?"')
add('job_ascii_suffix', 're.escape(x) + r"(?: \\(.*\\))?", ten)', 're.escape(x) + r"(?: \\([ -~]*\\))?", ten)')
add('job_one_suffix_item', 'r"(?: \\(.*\\))?"', 'r"(?: \\([^,]*\\))?"')
add('job_alias_truncate', 'for x in (k, j.get("name"))', 'for x in (k, str(j.get("name"))[:20])')
add('job_only_named_keys', 'for x in (k, j.get("name"))', 'for x in ((None if "name" in j else k), j.get("name"))')
add('job_drop_unmatched_bad_jobs', 'type(j) is dict and any(', '(type(j) is dict and bool(j.get("steps"))) and any(')
add('job_requires_nonempty_steps', 'type(sy) is not list or', '(type(sy) is not list or not sy) or')
add('job_nonempty_rest_required','type(st) is list and all(', 'type(st) is list and bool(st) and all(')
add('rest_number_under_100','_so(s.get("number"), 1)', '(_so(s.get("number"), 1) and s["number"] < 100)')
add('rest_number_order_contiguous','len({s["number"] for s in st}) == len(st)', 'len({s["number"] for s in st}) == len(st) and min(s["number"] for s in st) == 1')
add('rest_skipped_time_required','if not all((a := _gio(', 'if any(not _gio(s.get("started_at")) for s in ung) or not all((a := _gio(')
add('name_explicit_nonblank_strip','return s["name"] if _chuoi(s["name"])', 'return s["name"].rstrip() if _chuoi(s["name"])')
add('name_uses_fallback_falsy_run','v = s.get("run", s.get("uses"))','v = s.get("run") or s.get("uses")')
add('name_has_run_uses_prefer','v = s.get("run", s.get("uses"))','v = s.get("uses", s.get("run"))')
add('name_crlf_split','v.split("\\n")[0]', 'v.splitlines()[0]')
add('time_second_start_plus_one','a <= h <= z','a + datetime.timedelta(seconds=1) <= h <= z')
add('time_nonzero_duration','a <= h <= z','a <= h <= z and a < z')
add('time_require_same_day','a <= h <= z','a <= h <= z and a.date() == h.date() == z.date()')
add('time_reject_leap_day','return datetime.datetime.strptime(v[:19], "%Y-%m-%dT%H:%M:%S") if', 'return datetime.datetime.strptime(v[:19], "%Y-%m-%dT%H:%M:%S") if v[5:10] != "02-29" and')
add('time_reject_year_before_2000','type(v) is str and RE_GIO.fullmatch(v)', 'type(v) is str and RE_GIO.fullmatch(v) and v[:4] >= "2000"')
add('time_accept_invalid_leap_day','except ValueError:\n        return None','except ValueError:\n        return datetime.datetime(2026, 2, 28) if type(v) is str and v[:10] == "2026-02-29" else None')
add('time_header_first_position','(h := _gio(b["gio"]))','(h := _gio(buoc[0]["gio"]))')
add('time_skip_middle','for b, i in zip(buoc, chay)):', 'for b, i in list(zip(buoc, chay))[::2]):')
add('names_skip_middle','for s, y in zip(ung, sy)):', 'for s, y in list(zip(ung, sy))[::2]):')
add('names_compare_as_strings','s.get("name") != ten_du_kien(y)', 'str(s.get("name")) != str(ten_du_kien(y))')
add('env_only_keys_str','str(k).startswith("CI_DANG_KY_")','(type(k) is str and k.startswith("CI_DANG_KY_"))')
add('env_ignore_false_values','any(str(k).startswith("CI_DANG_KY_") for k in d["env"])','any(str(k).startswith("CI_DANG_KY_") and d["env"][k] for k in d["env"])')
add('env_ignore_empty_collections','type(d["env"]) is not dict','type(d["env"]) is not dict and bool(d["env"])')
add('env_prefix_full_key','str(k).startswith("CI_DANG_KY_")','str(k) == "CI_DANG_KY_"')
add('env_suffix_casefold','str(k).startswith("CI_DANG_KY_")','str(k).strip().startswith("CI_DANG_KY_")')
add('prior_entire_step_instead_run','str(t.get("run", ""))', 'str(t)')
add('prior_uses_preferred','str(t.get("run", ""))','str(t.get("uses", t.get("run", "")))')
add('prior_ignore_if_empty_env','for t in j["steps"][:i]))','for t in j["steps"][:i] if "env" not in t))')
add('prior_only_last_two','for t in j["steps"][:i]))','for t in j["steps"][max(0,i-2):i]))')
add('prior_only_first','for t in j["steps"][:i]))','for t in j["steps"][:min(1,i)]))')
add('prior_case_insensitive','re.search("GITHUB_(ENV|PATH)",','re.search("(?i)GITHUB_(ENV|PATH)",')
add('step_allow_env_empty','set(s) - KHOA_BUOC','set(s) - KHOA_BUOC - ({"env"} if not s.get("env") else set())')
add('step_defaults_null_allowed','"defaults" in j','("defaults" in j and j["defaults"] is not None)')
add('workflow_defaults_null_allowed','"defaults" in wf','("defaults" in wf and wf["defaults"] is not None)')
add('mode_no_sh','("bash", "pwsh", "sh")','("bash", "pwsh")')
add('mode_allow_empty_shell','s.get("shell", "bash") not in','(s.get("shell") or "bash") not in')
add('log_first_output_line','"\\n".join(b["phan"]) + "\\n"','"\\n".join(b["phan"][:1]) + "\\n"')
add('log_last_output_line','"\\n".join(b["phan"]) + "\\n"','"\\n".join(b["phan"][-1:]) + "\\n"')
add('log_output_strip','"\\n".join(b["phan"]) + "\\n"','"\\n".join(b["phan"]).strip() + "\\n"')
add('log_reverse_output','"\\n".join(b["phan"]) + "\\n"','"\\n".join(reversed(b["phan"])) + "\\n"')
add('log_reject_metadata_after_shell','not b["tien_to"] or t.startswith("shell: ")','b["tien_to"] and t.startswith("shell: ")')
add('log_endgroup_need_shell_first','if t == "##[endgroup]":','if t == "##[endgroup]" and not b["tien_to"]:')
add('log_uncolored_metadata_add_to_echo','elif mau and b["tien_to"]:', 'elif mau and b["tien_to"] or t.startswith("  NOTE:"):')
add('log_shell_nonempty','t.startswith("shell: ")','t.startswith("shell: ") and len(t)>7')
add('log_color_prefix_only','mau = "\\x1b[36;1m" in d','mau = d.split(" ", 1)[-1].startswith("\\x1b[36;1m")')
add('log_color_without_timestamp','mau = "\\x1b[36;1m" in d','mau = "\\x1b[36;1m" in d and bool(RE_DONG.match(d))')
add('run_reverse_calls','for duong in dict.fromkeys([g[2] for g in goi] if goi and all(goi) else []):','for duong in reversed(dict.fromkeys([g[2] for g in goi] if goi and all(goi) else [])):')
add('run_sort_calls','for duong in dict.fromkeys([g[2] for g in goi] if goi and all(goi) else []):','for duong in sorted(dict.fromkeys([g[2] for g in goi] if goi and all(goi) else [])):')
add('run_drop_last_call','[g[2] for g in goi] if goi and all(goi) else []','[g[2] for g in goi][:-1] if goi and all(goi) else []')
add('run_no_dedup','dict.fromkeys([g[2] for g in goi] if goi and all(goi) else [])','([g[2] for g in goi] if goi and all(goi) else [])')
add('run_unknown_omitted','if duong not in moi or chan:', 'if duong not in moi:\n                continue\n            if chan:')
add('run_unknown_priority','"khong_co_trong_MOI" if duong not in moi else','"khong_co_trong_MOI" if duong not in moi and not chan else')
add('run_blank_lines_disallowed','for d in dong_logic(run.rstrip("\\n").split("\\n")) if d]', 'for d in dong_logic(run.rstrip("\\n").split("\\n"))]')
add('run_blank_counted','so += 1','so += len(b["in_lai"])')
add('run_strip_carriage','run.rstrip("\\n") == "\\n".join(b["in_lai"])','run.rstrip("\\r\\n") == "\\n".join(b["in_lai"])')
add('run_strip_match_only','run.rstrip("\\n") == "\\n".join(b["in_lai"])','run.rstrip("\\n").strip() == "\\n".join(b["in_lai"]).strip()')
add('rest_post_casefold','str(s.get("name")).startswith("Post ")','str(s.get("name")).lower().startswith("post ")')
add('rest_skipped_casefold','s.get("conclusion") != "skipped"]','str(s.get("conclusion")).lower() != "skipped"]')
add('rest_also_skip_null','s.get("conclusion") != "skipped"]','s.get("conclusion") not in (None, "skipped")]')
add('yaml_empty_workflow_reject','type(wf.get("jobs")) is dict','type(wf.get("jobs")) is dict and bool(wf["jobs"])')
known=set()
for p in [root/'ops/ci_provenance_test.py',root/'.review-input/tu-dot-bien/tu_dot_bien.py',root/'.review-input/tu-dot-bien/tu_dot_bien2.py']:
 for n in ast.walk(ast.parse(p.read_text())):
  if isinstance(n,ast.Tuple):
   try:v=ast.literal_eval(n)
   except Exception:continue
   if len(v)>=3 and all(type(x) is str for x in v[:3]):known.add((v[1],v[2]))
def cases(path):
 code="import importlib.util as u,json;s=u.spec_from_file_location('t',%r);t=u.module_from_spec(s);s.loader.exec_module(t);print(json.dumps([(c,)+t.chay_ca(c) for c in t.CA]))"%str(root/'ops/ci_provenance_test.py')
 cmd=[sys.executable,'-B','-c',code]
 p=subprocess.run(cmd,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',CI_PROVENANCE_MA=str(path)),timeout=900)
 try:res=json.loads(p.stdout)
 except Exception:res=[('import',p.returncode or 4,(p.stdout+p.stderr).decode('utf8','replace'))]
 return cmd,p,res
cmd,p,base=cases(root/'ops/ci_provenance.py');assert p.returncode==0 and len(base)==49 and all(rc==0 for c,rc,o in base),base
(out/'baseline.json').write_text(json.dumps(base,ensure_ascii=False,indent=2))
def one(v):
 name,old,new=v;rec={'name':name,'old':old,'new':new,'count':src.count(old),'new_vs_executor':(old,new) not in known}
 if src.count(old)!=1:return rec|{'rank':'HONG_NEO'}
 path=out/(name+'.py');path.write_text(src.replace(old,new));cmd,p,res=cases(path)
 (out/(name+'.stdout')).write_bytes(p.stdout);(out/(name+'.stderr')).write_bytes(p.stderr)
 killed=[c for c,rc,o in res if rc==3 and o.startswith('DO:'+c+':')];bad=[{'case':c,'rc':rc,'output':o} for c,rc,o in res if rc and not(rc==3 and o.startswith('DO:'+c+':'))]
 return rec|{'command':cmd,'source':str(path),'rc':p.returncode,'rank':'GIET+NEM' if killed and bad else 'GIET' if killed else 'TIN_DUNG_GIA' if bad else 'SONG_SOT','killed':killed,'other_errors':bad,'cases':res}
if __name__=='__main__':
 rows=[]
 with concurrent.futures.ThreadPoolExecutor(3) as ex:
  for v in ex.map(one,M):
   rows.append(v);(out/'results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2));print(v['name'],v['rank'],v.get('killed'),flush=True)
 print(collections.Counter(r['rank'] for r in rows))
