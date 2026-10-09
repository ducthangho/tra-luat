D0='def main(chon=None, nen=None, so=None) -> int:'
DEF=lambda x: x+'\n\n\n'+D0
SOANCH='    so = SO_BO_QUA if so is None else so\n    # Selector'
MUT=[
('R25L-nen-dinh-LAST-wins',['t203'],[(D0,DEF('_ND = {}')),(SOANCH,'    nen = nen or _ND.get("n")\n    if nen: _ND["n"] = nen\n    so = SO_BO_QUA if so is None else so\n    # Selector')]),
('R25F-nen-dinh-FIRST-wins',['t203'],[(D0,DEF('_ND = {}')),(SOANCH,'    if nen and "n" not in _ND: _ND["n"] = nen\n    nen = nen or _ND.get("n")\n    so = SO_BO_QUA if so is None else so\n    # Selector')]),
]
