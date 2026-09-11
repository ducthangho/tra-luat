import datetime as dt, importlib.util, json, pathlib, subprocess, sys
B=pathlib.Path(__file__).resolve().parents[1];R=B/'cay-kho';O=B/'do-review8';sys.dont_write_bytecode=True
sp=importlib.util.spec_from_file_location('lease_review8_followup',R/'ops/lease_publish.py');L=importlib.util.module_from_spec(sp);sp.loader.exec_module(L);rows=L._quet_lease_toan_kho(R,doi_chieu_ref=False)
old='mutant-khong-chay-tren-windows-exec-1-claude-20260906';mid='gate-tach-job-cat-chi-phi-exec-1-claude-20260906'
def holders(rs):return sorted({r['lease']['lease_id'] for r in rs if L._lease_cham_duong(r['lease'],'.claude/dev/ci_dang_ky_test.py') and L._phan_loai_lease(r['lease'])=='CÒN_HẠN' and L._bia_mo_doi_xung(r['lease'],rs) is not True})
model=[{**r,'lease':{**r['lease'],'da_bi_thay_the':mid}} if r['lease'].get('lease_id')==old else r for r in rows]
master_blob=subprocess.check_output(['git','-C',str(R),'rev-parse',f'origin/master:ops/leases/{old}.yaml'],text=True).strip()
report={'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'master_old_blob':master_blob,'real_registry_holders':holders(rows),'all_old_copies_tombstoned_model':holders(model),'model_is_not_ref_write':True}
g=(B/'tai-lieu/GATE-TACH-JOB-CAT-CHI-PHI.md').read_text();i=(B/'tai-lieu/463-GATE-TACH-JOB-CAT-CHI-PHI.md').read_text()
old1='**mười một** lượt master chạy trọn';old2='Mẫu là **mọi lượt master trong ~9,6 giờ**';old3='(đổi băm ⇒ lease cấp lại), chưa làm ở PR này.'
fg=g.replace(old1,'**mười một** lượt chạy trọn (5 master + 6 nhánh)').replace(old2,'Mẫu là **11 lượt đã liệt kê (5 master + 6 nhánh)**')
fi=i.replace(old3,'(đổi băm ⇒ lease cấp lại); đã thực hiện trong PR này, theo revision 2 và lease exec-1r2 bên dưới.')
report['sample_prose_check']={'old_clauses_present':[old1 in g,old2 in g,old3 in i],'text_only_repairs_remove_all':[old1 not in fg,old2 not in fg,old3 not in fi],'A1_kept':'**≤ 25,00 phút**' in fg,'A5_kept':'**≤ 135,00**' in fg,'old_branch_numbers_kept':['43,20' in fg,'21,03' in fg]}
# Pretooluse is independently re-run by run_command.py; this file never synthesizes a green rc.
(O/'followup-checks.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps(report,ensure_ascii=False,indent=2))
