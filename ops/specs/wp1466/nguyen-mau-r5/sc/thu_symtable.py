import symtable, ast
def rang(tab, goc=True):
    ra = set()
    for s in tab.get_symbols():
        if goc and (s.is_assigned() or s.is_imported() or s.is_namespace()) and not s.is_global() is None:
            ra.add(s.get_name())
        if not goc and s.is_declared_global():
            ra.add(s.get_name())
    for ch in tab.get_children():
        ra |= rang(ch, False)
    return ra
CA = {
 "assign": "X = 1",
 "def": "def f(a=1):\n    b = 2\n    return b",
 "def_default_walrus": "def f(a=(X := 1)):\n    return a",
 "def_decorator_walrus": "@(X := (lambda f: f))\ndef f():\n    pass",
 "lambda_default_walrus": "F = lambda a=(X := 1): a",
 "listcomp_walrus": "L = [(X := i) for i in range(3)]",
 "listcomp_plain": "L = [i for i in range(3)]",
 "listcomp_lambda_default": "L = [(lambda g, so=so: g) for so in 'ab']",
 "genexp_walrus": "L = list((X := i) for i in range(3))",
 "class_global": "class C:\n    global X\n    X = 1",
 "class_attr": "class C:\n    X = 1",
 "func_global": "def f():\n    global X\n    X = 1",
 "func_global_del": "def f():\n    global X\n    del X",
 "func_global_read": "def f():\n    global X\n    return X",
 "except_as": "try:\n    pass\nexcept Exception as X:\n    pass",
 "match_capture": "match 1:\n    case X:\n        pass",
 "import_as": "import os as X",
 "for_target": "for X in ():\n    pass",
 "with_as": "with open('a') as X:\n    pass",
 "augassign": "X += 1",
 "annassign_noval": "X: int",
 "del": "del X",
 "if_def": "if True:\n    def X():\n        pass",
 "typealias": "type X = int",
 "aug_reg": "CASES += [(n, lambda c, n=n: n) for n in 'ab']",
 "expr_call": "MUTANTS.update({'a': 1})",
 "annot_walrus": "from __future__ import annotations\ndef f(a: (X := 1)):\n    pass",
 "nested_def_global": "def f():\n    def g():\n        global X\n        X = 1\n    return g",
}
for k, v in CA.items():
    try:
        t = symtable.symtable(v, "<n>", "exec")
        print(f"{k:28s}", sorted(rang(t)))
    except SyntaxError as e:
        print(f"{k:28s} SyntaxError: {e.msg}")
