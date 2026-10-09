import audit as A
old='    ghi("K5",'
new='    ly_do += ["K4:S fresh, khong can chay lai"] if base_hien_hanh != r["S"] else []\n'+old
A.suite('k4_unspaced_contradiction',A.edit(old,new))
