MUT=[
('R15p-tin-so-MAC-DINH',['t193'],[('try: ly_do = _ly_do_bo_qua_workflow(ex.tep, ex.ten_job, nen=nen) if dung_cap else ""','try: ly_do = ("chỉ chạy Ubuntu; tin sổ") if (dung_cap and so is SO_BO_QUA and (nen or os.name) == "nt") else (_ly_do_bo_qua_workflow(ex.tep, ex.ten_job, nen=nen) if dung_cap else "")')]),
('R20p-symlink-only',['t193'],[('(Path(ex.tep).resolve(), ex.ten_job) == (Path(dk[0]).resolve(), dk[1])','(Path(os.path.abspath(ex.tep)), ex.ten_job) == (Path(os.path.abspath(dk[0])), dk[1])')]),
('V2-tk-khong-neo',['t194'],[('RE_TONG_KET = r"(?m)^lease_publish:','RE_TONG_KET = r"(?m)lease_publish:')]),
('V4-su-kien-khong-neo',['t194'],[('su_kien = re.findall(r"(?m)^(>>> vao|<<< ra) (\\S+)", out)','su_kien = re.findall(r"(?m)(>>> vao|<<< ra) (\\S+)", out)')]),
('V5-ra-khong-neo',['t194'],[('re.findall(r"(?m)^<<< ra (\\S+)(.*)$", out)','re.findall(r"(?m)<<< ra (\\S+)(.*)$", out)')]),
('V6-do-khong-neo',['t194'],[('if sorted(re.findall(r"(?m)^  ĐỎ  (\\w+):", out)) != do_:','if sorted(re.findall(r"(?m)  ĐỎ  (\\w+):", out)) != do_:')]),
('V7-bo-kiem-thoi-luong',['t194'],[('re.fullmatch(r" \\d+\\.\\d{3}s (QUA|DO|BO_QUA)[ \\t\\r]*", d)','re.fullmatch(r".*(QUA|DO|BO_QUA)[ \\t\\r]*", d)')]),
('V8-rc-chi-ca-do',['t194'],[('if rc is not None and rc != (1 if do_ else 0):','if rc is not None and rc not in (0, 1):')]),
# L4 mới: rò ngoài 4 khoá chụp
('L4a-seam-ghi-environ',['t203'],[('    qua, hong, bo_qua = 0, [], []\n    so = SO_BO_QUA if so is None else so\n','    qua, hong, bo_qua = 0, [], []\n    if nen is not None:\n        os.environ["LP_RO_SEAM"] = nen\n    so = SO_BO_QUA if so is None else so\n')]),
('L4b-seam-ghi-global-allow',['t203'],[('    qua, hong, bo_qua = 0, [], []\n    so = SO_BO_QUA if so is None else so\n','    qua, hong, bo_qua = 0, [], []\n    if nen is not None:\n        globals()["NHAN_UBUNTU_CHO_PHEP"] = frozenset(NHAN_UBUNTU_CHO_PHEP | {"windows-latest"})\n    so = SO_BO_QUA if so is None else so\n')]),
('L4c-seam-chdir',['t203'],[('    qua, hong, bo_qua = 0, [], []\n    so = SO_BO_QUA if so is None else so\n','    qua, hong, bo_qua = 0, [], []\n    if nen is not None:\n        os.chdir("/")\n    so = SO_BO_QUA if so is None else so\n')]),
('L4d-seam-ghi-WORKFLOW_DANG',['t203'],[('    qua, hong, bo_qua = 0, [], []\n    so = SO_BO_QUA if so is None else so\n','    qua, hong, bo_qua = 0, [], []\n    if nen is not None:\n        globals()["WORKFLOW_DANG"] = Path("/nonexistent/x.yml")\n    so = SO_BO_QUA if so is None else so\n')]),
('L4e-seam-sua-NHAN-tren-sys.path',['t203'],[('    qua, hong, bo_qua = 0, [], []\n    so = SO_BO_QUA if so is None else so\n','    qua, hong, bo_qua = 0, [], []\n    if nen is not None:\n        sys.path.insert(0, "/tmp")\n    so = SO_BO_QUA if so is None else so\n')]),
('L4f-so-ghi-gia-tri-trong-sổ(in-place-doi-tuple)',['t203'],[('    so = SO_BO_QUA if so is None else so\n    # Selector','    so = SO_BO_QUA if so is None else so\n    if nen == "posix" and so:\n        for _k in list(so): SO_BO_QUA[_k] = SO_BO_QUA.get(_k, so[_k])\n    # Selector')]),
('L4g-chon-chen-vao-CA-roi-xoa-giu-doi-tuong',['t203'],[('        cac_ca = list(chon)\n','        cac_ca = list(chon)\n        CA.append(cac_ca[0]); CA.pop()\n')]),
('L4h-seam-doi-stdout',['t203'],[('    qua, hong, bo_qua = 0, [], []\n    so = SO_BO_QUA if so is None else so\n','    qua, hong, bo_qua = 0, [], []\n    if nen is not None:\n        sys.stdout = sys.__stdout__\n    so = SO_BO_QUA if so is None else so\n')]),
]
