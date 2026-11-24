import ast,copy,json,pathlib
w=pathlib.Path(__file__).resolve().parent
src=(w.parent/'repo/ops/gate_output_doi_chieu.py').read_text();tree=ast.parse(src)
parents={c:n for n in ast.walk(tree) for c in ast.iter_child_nodes(n)}
old=[]
for name in ['independent_mutants.jsonl','independent_corrected.jsonl','extra_mutants.jsonl','order_url_mutants.jsonl']:
 old += [json.loads(l) for l in (w/name).read_text().splitlines()]
seen={ast.dump(ast.parse(x['src'])) for x in old}
reasons={'khong_phai_utf8','xuong_dong_tron','cr_le','dau_tep_sai','job_lap','dong_la','thieu_moc','moc_lap','symlink','provenance_0','provenance_nhieu','bo_sinh_la','khong_phai_run_land','job_id_trung_provenance','provenance_chua_du','tap_job_lech','tap_skip_lech','job_lech:','ket_luan_lech:','log_sha_lech:','dong_skip_sai_phien_ban','moc_lech','co_job_skipped','check_bat_buoc:','url','readback','doc_readback','html_url','tac_gia','dong_mien','han','os','sha'}
out=[];census=[]
for i,n in enumerate(ast.walk(tree)):
 if not isinstance(n,ast.Constant) or not isinstance(n.value,str):continue
 p=parents.get(n)
 is_reason=(n.value in reasons and isinstance(p,(ast.List,ast.ListComp,ast.IfExp,ast.JoinedStr))) or (n.value in reasons and isinstance(p,ast.Call) and isinstance(p.func,ast.Attribute) and p.func.attr=='append') or (isinstance(p,ast.JoinedStr) and any(s in n.value for s in ['dinh_dang_loi_khai','waiver_khong_co_can_cu','duong_khong_tep_danh_gia','tep_danh_gia_khong_hop_le','danh_gia_khong_'])) or 'landed_khong_loi_khai_gate_output' in n.value
 if not is_reason:continue
 t=copy.deepcopy(tree);q=list(ast.walk(t))[i];q.value+='__doi';code=ast.unparse(t)
 exists=ast.dump(t) in seen
 census.append({'line':n.lineno,'col':n.col_offset,'reason':n.value,'previously_measured':exists})
 if not exists:
  out.append({'id':f'reason_complete_{n.lineno}_{n.col_offset}','kind':'reason_complete','line':n.lineno,'src':code})
(w/'reason_census.json').write_text(json.dumps(census,ensure_ascii=False,indent=2))
(w/'reason_complete_mutants.jsonl').write_text(''.join(json.dumps(x,ensure_ascii=False)+'\n' for x in out))
print('reason occurrences',len(census),'new mutants',len(out))
