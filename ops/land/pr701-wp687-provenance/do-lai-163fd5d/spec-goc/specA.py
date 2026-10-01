# spec cho reviewed_sha 9d7a523
D0='def main(chon=None, nen=None, so=None) -> int:'
DEF=lambda x: x+'\n\n\n'+D0
SOA='    qua, hong, bo_qua = 0, [], []\n    so = SO_BO_QUA if so is None else so\n'
SOB='    so = SO_BO_QUA if so is None else so\n    # Selector'
def seam(code): return (SOA, '    qua, hong, bo_qua = 0, [], []\n    if nen is not None:\n        '+code+'\n    so = SO_BO_QUA if so is None else so\n')
# ---- revert từng chốt (để "gỡ riêng chốt thì đột biến sống lại")
REV_UV=('    uv = set(_ca_ung_vien_gian_tiep(CA))','    uv = set(_ca_doc_than_buoc(CA))')
REV_UNIT=('    chot(_ca_ung_vien_gian_tiep([gia["_k"], gia["_c"]], gia) == ["_k"],','    chot(True or _ca_ung_vien_gian_tiep([gia["_k"], gia["_c"]], gia) == ["_k"],')
REV_Y=('                          ("dòng chẩn đoán GIỮA dòng chứa chữ tổng kết/marker/ĐỎ (không neo đầu dòng ⇒ không tính)", "y", 0)):','                          ):')
REV_5=('''                              ([lambda: None], "nt" if os.name != "nt" else "posix", {})):''','''                              ):''')
REV_ANH=('''                "os.environ": dict(os.environ), "cwd": os.getcwd(), "sys.path": list(sys.path),
                "globals": {k: id(v) for k, v in list(globals().items()) if not k.startswith("__")}}''','''                }''')
REV_RESTORE=('''            os.environ.clear()
            os.environ.update(truoc["os.environ"])
            os.chdir(truoc["cwd"])
            sys.path[:] = truoc["sys.path"]
''','''            os.environ.clear(); os.environ.update(truoc.get("os.environ", os.environ)); os.chdir(truoc.get("cwd", os.getcwd())); sys.path[:] = truoc.get("sys.path", sys.path)
''')
GO=[REV_ANH]
NEWCA='''def _h_gian_tiep():
    return _chay_buoc_dang_that("x")


@ca
def t999_gian_tiep_qua_helper():
    _h_gian_tiep()


def main(chon=None, nen=None, so=None) -> int:'''
NEWCA3='''def _h3c():
    return _chay_buoc_dang_that("x")


def _h3b():
    return _h3c()


def _h3a():
    return _h3b()


@ca
def t999_gian_tiep_3tang():
    _h3a()


def main(chon=None, nen=None, so=None) -> int:'''
NEWCA_NESTED='''@ca
def t999_gian_tiep_def_long():
    def _i():
        return _chay_buoc_dang_that("x")
    _i()


def main(chon=None, nen=None, so=None) -> int:'''
REG=('"t200_M1_nguon_lease_publish_tuy_chon_that_su_duoc_dung")}','"t200_M1_nguon_lease_publish_tuy_chon_that_su_duoc_dung", "t999_gian_tiep_qua_helper")}')
REG3=('"t200_M1_nguon_lease_publish_tuy_chon_that_su_duoc_dung")}','"t200_M1_nguon_lease_publish_tuy_chon_that_su_duoc_dung", "t999_gian_tiep_3tang")}')
V={'V2':('RE_TONG_KET = r"(?m)^lease_publish:','RE_TONG_KET = r"(?m)lease_publish:'),
'V4':('su_kien = re.findall(r"(?m)^(>>> vao|<<< ra) (\\S+)", out)','su_kien = re.findall(r"(?m)(>>> vao|<<< ra) (\\S+)", out)'),
'V5':('re.findall(r"(?m)^<<< ra (\\S+)(.*)$", out)','re.findall(r"(?m)<<< ra (\\S+)(.*)$", out)'),
'V6':('if sorted(re.findall(r"(?m)^  ĐỎ  (\\w+):", out)) != do_:','if sorted(re.findall(r"(?m)  ĐỎ  (\\w+):", out)) != do_:')}
MUT=[
('L1a-ind-1tang-chua-dky',['t193','t70'],[(D0,NEWCA)]),
('L1b-ind-3tang-chua-dky',['t193','t70'],[(D0,NEWCA3)]),
('L1c-ind-1tang-da-dky',['t193','t70'],[(D0,NEWCA),REG]),
('L1d-ind-3tang-da-dky',['t193','t70'],[(D0,NEWCA3),REG3]),
('L1e-GO-chot-uv+1tang',['t193','t70'],[(D0,NEWCA),REV_UV]),
('L1f-GO-chot-uv+3tang',['t193','t70'],[(D0,NEWCA3),REV_UV]),
('L1g-GO-vedonvi-uv',['t193'],[REV_UNIT,('                if hasattr(h, "__code__") and n not in thay:\n                    thay.add(n)\n                    ngan.append(h)\n','                pass\n')]),
('L1h-vedonvi-tang3',['t193'],[('                if hasattr(h, "__code__") and n not in thay:','                if hasattr(h, "__code__") and n not in thay and n.startswith("_a"):')]),
('L1i-def-long-chua-dky',['t193','t70'],[(D0,NEWCA_NESTED)]),
]
for k,(o,n) in V.items():
    MUT.append(('L2-'+k,['t194'],[(o,n)]))
    MUT.append(('L2-GO-vey+'+k,['t194'],[REV_Y,(o,n)]))
MUT+=[
('L3a-R25L',['t203'],[(D0,DEF('_ND = {}')),(SOB,'    nen = nen or _ND.get("n")\n    if nen: _ND["n"] = nen\n    so = SO_BO_QUA if so is None else so\n    # Selector')]),
('L3a-GO-luot5+R25L',['t203'],[REV_5,(D0,DEF('_ND = {}')),(SOB,'    nen = nen or _ND.get("n")\n    if nen: _ND["n"] = nen\n    so = SO_BO_QUA if so is None else so\n    # Selector')]),
('L3b-R25F',['t203'],[(D0,DEF('_ND = {}')),(SOB,'    if nen and "n" not in _ND: _ND["n"] = nen\n    nen = nen or _ND.get("n")\n    so = SO_BO_QUA if so is None else so\n    # Selector')]),
('L3c-environ',['t203'],[seam('os.environ["LP_RO_SEAM"] = nen')]),
('L3c-GO-anh+environ',['t203'],[REV_ANH,REV_RESTORE,seam('os.environ["LP_RO_SEAM"] = nen')]),
('L3d-environ-xoa',['t203'],[seam('os.environ.pop("PATH", None)')]),
('L3e-cwd',['t203'],[seam('os.chdir("/")')]),
('L3e-GO-anh+cwd',['t203'],[REV_ANH,REV_RESTORE,seam('os.chdir("/")')]),
('L3f-syspath-insert',['t203'],[seam('sys.path.insert(0, "/tmp")')]),
('L3f-GO-anh+syspath',['t203'],[REV_ANH,REV_RESTORE,seam('sys.path.insert(0, "/tmp")')]),
('L3g-syspath-xoa',['t203'],[seam('sys.path.pop()')]),
('L3h-global-rebind-allow',['t203'],[seam('globals()["NHAN_UBUNTU_CHO_PHEP"] = frozenset(NHAN_UBUNTU_CHO_PHEP | {"windows-latest"})')]),
('L3h-GO-anh+global',['t203'],[REV_ANH,REV_RESTORE,seam('globals()["NHAN_UBUNTU_CHO_PHEP"] = frozenset(NHAN_UBUNTU_CHO_PHEP | {"windows-latest"})')]),
('L3i-global-moi-ten',['t203'],[seam('globals()["_RO_TEN_MOI"] = nen')]),
('L3j-global-xoa-ten',['t203'],[seam('globals().pop("ENV_GITHUB", None)')]),
('L3k-global-inplace-dict',['t203'],[seam('ENV_GITHUB["RO"] = nen')]),
('L3l-global-inplace-set',['t203'],[seam('_KHONG_CHAY_T191.add("ro")')]),
('L3m-global-inplace-list',['t203'],[seam('_TD_M2.append(nen)')]),
('L3n-sys.modules',['t203'],[seam('sys.modules["lp_ro_seam"] = sys')]),
('L3o-umask',['t203'],[seam('os.umask(0o077)')]),
('R21',['t203'],[seam('os.name = nen')]),
('R22',['t203'],[('        cac_ca = list(chon)\n','        cac_ca = list(chon)\n        CA[:] = cac_ca\n')]),
('R23',['t203'],[(SOB,'    so = SO_BO_QUA if so is None else so\n    SO_BO_QUA.update(so)\n    # Selector')]),
('R24',['t203'],[('    if chon is not None:\n        cac_ca = list(chon)\n','    if chon is not None:\n        cac_ca = list(chon)\n        sys.argv.append("--rac")\n')]),
('R26',['t203'],[(D0,DEF('_CD = {}')),('    else:\n        cac_ca = list(CA)\n    for fn in cac_ca:','    else:\n        cac_ca = list(CA)\n    if chon is None and _CD.get("c") is not None:\n        cac_ca = _CD["c"]\n    if chon is not None:\n        _CD["c"] = list(chon)\n    for fn in cac_ca:')]),
('R27',['t203'],[(D0,DEF('_SD = {}')),(SOB,'    so = _SD.get("s", SO_BO_QUA) if so is None else so\n    if so is not SO_BO_QUA:\n        _SD["s"] = so\n    # Selector')]),
('L4f',['t203'],[(SOB,'    so = SO_BO_QUA if so is None else so\n    if nen == "posix" and so:\n        for _k in list(so): SO_BO_QUA[_k] = SO_BO_QUA.get(_k, so[_k])\n    # Selector')]),
]
CMP=('ro += [f"{k} (nen={nen})" for k in truoc if sau[k] != truoc[k]]','ro += [f"{k} (nen={nen})" for k in truoc if sau[k] != truoc[k] and k != "%s"]')
def sin(k): return (CMP[0],CMP[1]%k)
MUT=[]
for kh,nm,code in (("os.environ","environ",'os.environ["LP_RO_SEAM"] = nen'),("cwd","cwd",'os.chdir("/")'),("sys.path","syspath",'sys.path.insert(0, "/tmp")'),("globals","global",'globals()["NHAN_UBUNTU_CHO_PHEP"] = frozenset(NHAN_UBUNTU_CHO_PHEP | {"windows-latest"})')):
    MUT.append((f'SOLO-GO-{kh}+{nm}',['t203'],[sin(kh),seam(code)]))
    ot={"os.environ":"cwd","cwd":"sys.path","sys.path":"globals","globals":"os.environ"}[kh]
    MUT.append((f'SOLO-GO-{ot}+{nm}(doi-chung)',['t203'],[sin(ot),seam(code)]))
