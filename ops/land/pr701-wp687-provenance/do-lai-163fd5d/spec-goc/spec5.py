D0='def main(chon=None, nen=None, so=None) -> int:'
DEF=lambda x: x+'\n\n\n'+D0
SO='    so = SO_BO_QUA if so is None else so\n    # Selector'
MUT=[
('R24-seam-ghi-argv',['t203'],[('    if chon is not None:\n        cac_ca = list(chon)\n','    if chon is not None:\n        cac_ca = list(chon)\n        sys.argv.append("--rac")\n')]),
('R25-nen-dinh',['t203'],[(D0,DEF('_ND = {}')),('    so = SO_BO_QUA if so is None else so\n    # Selector','    nen = nen or _ND.get("n")\n    if nen: _ND["n"] = nen\n    so = SO_BO_QUA if so is None else so\n    # Selector')]),
('R26-chon-dinh',['t203'],[(D0,DEF('_CD = {}')),('    else:\n        cac_ca = list(CA)\n    for fn in cac_ca:','    else:\n        cac_ca = list(CA)\n    if chon is None and _CD.get("c") is not None:\n        cac_ca = _CD["c"]\n    if chon is not None:\n        _CD["c"] = list(chon)\n    for fn in cac_ca:')]),
('R27-so-dinh',['t203'],[(D0,DEF('_SD = {}')),(SO,'    so = _SD.get("s", SO_BO_QUA) if so is None else so\n    if so is not SO_BO_QUA:\n        _SD["s"] = so\n    # Selector')]),
]
