import audit as A
import json, pathlib, tempfile
T = A.T
# F36: telemetry sai kiểu -> LoiDo; hợp lệ -> pass; comment vô hại -> không được giết
orig = T._CON_TINH
for case, rep in [("valid", None), ("bad_ev", {"ev": None, "trang_thai": True, "tat_dinh": True}),
                  ("bad_bool", {"ev": [], "trang_thai": 1, "tat_dinh": 1}), ("ev_int", {"ev": [1], "trang_thai": True, "tat_dinh": True}),
                  ("real_side_effect", {"ev": ["open"], "trang_thai": True, "tat_dinh": True})]:
    T._CON_TINH = orig + ("" if rep is None else "\nprint(" + repr(json.dumps(rep)) + ")\n")
    try:
        T.ca_tinh("tinh", A.M); o = "pass"
    except Exception as e:
        o = type(e).__name__
    row = ("R5", "comment", "c", T._DAU, T._DAU + "  # harmless", "tinh", None)
    A.emit(f="F36", case=case, oracle=o, disp=T.chay_dot_bien(A.SRC, row))
T._CON_TINH = orig
# F35: cách diễn đạt hợp lệ qua; ngược nghĩa / sai trường / thiếu / thừa / trùng -> đỏ
for name, old, new in [("receipt_word", '[f"{k} stale', '[f"{k} receipt stale'),
                       ("co_dau", 'stale, chay lai', 'stale, chạy lại'),
                       ("dao_thu_tu", '(("S", base_hien_hanh), ("H", head_hien_hanh))', '(("H", head_hien_hanh), ("S", base_hien_hanh))'),
                       ("fresh", 'stale, chay lai', 'fresh, khong can chay lai'),
                       ("sai_truong", '[f"{k} stale', '[f"S stale'),
                       ("thua", '[f"{k} stale, chay lai" for', '[f"{k} stale, chay lai" for _ in (0, 1) for'),
                       ("stale_then_fresh", 'stale, chay lai', 'stale, chay lai, fresh')]:
    with tempfile.TemporaryDirectory() as td:
        p = pathlib.Path(td) / "m.py"; p.write_text(A.edit(old, new)); m = A.load(p, name)
        res = {c: A.target(m, p, c) for c in ("k4_base", "k4_head", "k4_ca_hai", "a11_k3_k4", "kieu_S", "duong_fixture")}
        tai = {}
        for base, head in ((T.X40, T.X40),):
            try:
                T.ca(m, "hai_truong", lambda d: d, ("K4",), base_hien_hanh=base, head_hien_hanh=head); tai["hai_truong"] = "pass"
            except Exception as e:
                tai["hai_truong"] = type(e).__name__ + ": " + str(e)[:120]
        A.emit(f="F35", mutant=name, **res, **tai)
