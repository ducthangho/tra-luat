import pathlib,json
w=pathlib.Path(__file__).resolve().parent;s=(w.parent/'repo/ops/gate_output_doi_chieu.py').read_text();changes=[
('phi_substring','c not in PHI_LOI_KHAI','not any(p in c for p in PHI_LOI_KHAI)'),
('phi_skip_descendants','        kq += loi_khai(v, d, _dang)','        if not isinstance(doc, dict) or _chuan(k) not in PHI_LOI_KHAI:\n            kq += loi_khai(v, d, _dang)'),
('waiver_no_strip','RE_MIEN.fullmatch(x.strip())','RE_MIEN.fullmatch(x)'),
('waiver_head_truthy','if head is not None else (m[1] not in gia_tri)','if head else (m[1] not in gia_tri)'),
('reason_claim_failed','danh_gia_khong_{can}:','danh_gia_sai_{can}:'),
('reason_waiver','waiver_khong_co_can_cu:','waiver_sai_can_cu:'),
]
rows=[]
for n,a,b in changes:
 assert s.count(a)==1,(n,s.count(a));rows.append(dict(id=n,kind='extended_contract',line=s[:s.index(a)].count('\n')+1,src=s.replace(a,b)))
(w/'extra_mutants.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in rows))
