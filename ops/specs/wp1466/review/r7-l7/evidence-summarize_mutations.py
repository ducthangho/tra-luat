from pathlib import Path
import ast,json,re
O=Path('out');s=(O/'mutations-rerun.log').read_text();out=[]
expected={
'M1_quet_trong_cay_lam_viec': {'rieng_nhanh_cuc_bo','rieng_remote_phu','rieng_packed_refs','rieng_replace','rieng_nhanh_cuc_bo_sau_dang','rieng_remote_phu_sau_dang'},
'M2_bo_kiem_B_thuoc_anh_chup':{'b_la_sha_rieng','v_graft_qua_bien_moi_truong','v_graft_trong_clone'},
'M3_nap_lp_tu_cay_lam_viec':{'lp_cay_lam_viec_bi_sua'},
'M4_bo_policy_tren_master_V':{'policy_co_mat','schema_policy_co_mat'},
'M5_bo_policy_doi_trong_B_master':{'e_policy_xoa_sau_B','e_policy_them_roi_xoa_sau_B','e_policy_qua_nhanh_phu_merge','e_policy_xoa_trong_commit_gop'},
'M5b_bo_m_cua_log':{'e_policy_qua_nhanh_phu_merge','e_policy_xoa_trong_commit_gop'},
'M6_bo_tu_chay_lai_voi_I':{'f_khong_I_pythonpath_clone','f_khong_I_script_trong_clone','f_khong_I_pyc_khong_nguon'},
'M7_bo_kiem_vi_tri_pyyaml':{'f_pth_yaml_trong_clone','f_thieu_pyyaml'},
'M8_bo_kiem_moi_module':{'f_pth_import_module_clone'},
'M9a_bo_kiem_git_truoc_T1':{'g_git_trong_clone'},
'M9b_bo_kiem_git_sau_T1':{'g_git_cay_chinh_tu_worktree_phu'},
'M10_git_cuc_bo_dung_moi_truong_nguoi_goi':{'v_graft_qua_bien_moi_truong'},
'M11_bo_T6':{'t6_may_chu_doi_trong_luc_do'},
'M12_kiem_to_tien_trong_clone':{'v_graft_trong_clone'}}
for line in s.splitlines():
 if not re.match(r'M\d',line) or ': đỏ ' not in line:continue
 name,rest=line.split(': đỏ ',1);entries=ast.literal_eval(rest);got={e for e in entries if not e.startswith('[')};match=got==expected[name];print(name,'FAILED',len(got),'EXPECTED_SET_MATCH',match);out.append({'name':name,'failed':sorted(got),'expected_set_match':match})
print('TOTAL_MUTANTS',len(out),'MATCH',sum(r['expected_set_match'] for r in out))
assert len(out)==14 and all(r['expected_set_match'] for r in out)
(O/'mutation-summary.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
