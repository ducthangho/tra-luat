import symtable
def show(tab, ind=""):
    print(ind + f"[{tab.get_type()} {tab.get_name()}]")
    for s in tab.get_symbols():
        fl = [n for n in ("is_assigned","is_imported","is_namespace","is_global","is_declared_global","is_local","is_free","is_parameter","is_referenced","is_nonlocal") if getattr(s, n)()]
        if hasattr(s, "is_comp_iter"): 
            if s.is_comp_iter(): fl.append("comp_iter")
        if hasattr(s, "is_comp_cell"):
            if s.is_comp_cell(): fl.append("comp_cell")
        print(ind + "  ", s.get_name(), fl)
    for ch in tab.get_children():
        show(ch, ind + "    ")
for src in ["L = [(X := i) for i in range(3)]", "L = [(lambda g, so=so: g) for so in 'ab']", "L = {k: v for k, v in {}.items()}", "L = list((X := i) for i in range(3))"]:
    print("=====", src)
    show(symtable.symtable(src, "<n>", "exec"))
