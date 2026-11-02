def _danh_gia_bieu_thuc_chuan_bi(expr_str: str, ctx: dict) -> list[str]:
    """Evaluator tối giản cho đúng hình biểu thức của chuan-bi.
    Hình chuẩn: ( <cond> ) && '["ubuntu-latest","windows-latest"]' || '["ubuntu-latest"]'
    Fail-close: in 'KHÔNG ĐO ĐƯỢC' và raise khi gặp hình khác (kể cả bọc fromJSON ngoài).
    """
    import json
    raw = expr_str.strip()
    if raw.startswith("${{") and raw.endswith("}}"):
        raw = raw[3:-2].strip()

    m = re.fullmatch(
        r"\(\s*(?P<cond>.*?)\)\s*&&\s*(?P<t>'\[.*?\]')\s*\|\|\s*(?P<f>'\[.*?\]')",
        raw,
        re.DOTALL,
    )
    if not m:
        msg = f"KHÔNG ĐO ĐƯỢC: biểu thức không khớp hình chuẩn tối giản của chuan-bi: {raw!r}"
        print(msg)
        raise ValueError(msg)

    cond_str = m.group("cond").strip()
    try:
        true_arr = json.loads(m.group("t").strip("'"))
        false_arr = json.loads(m.group("f").strip("'"))
    except Exception as ex:
        msg = f"KHÔNG ĐO ĐƯỢC: không parse được mảng JSON trong biểu thức: {ex}"
        print(msg)
        raise ValueError(msg)

    ve_list = [v.strip() for v in cond_str.split("||")]
    cond_true = False
    for ve in ve_list:
        m_eq = re.fullmatch(r"github\.event_name\s*==\s*'([^']+)'", ve)
        if m_eq:
            if ctx.get("event_name") == m_eq.group(1):
                cond_true = True
                break
            continue

        m_ref = re.fullmatch(r"github\.ref\s*==\s*'([^']+)'", ve)
        if m_ref:
            if ctx.get("ref") == m_ref.group(1):
                cond_true = True
                break
            continue

        m_contains = re.fullmatch(
            r"contains\s*\(\s*github\.event\.pull_request\.labels\.\*\.name\s*,\s*'([^']+)'\s*\)", ve
        )
        if m_contains:
            labels = ctx.get("labels") or []
            if m_contains.group(1) in labels:
                cond_true = True
                break
            continue

        msg = f"KHÔNG ĐO ĐƯỢC: vế điều kiện không nằm trong tập tối giản hỗ trợ: {ve!r}"
        print(msg)
        raise ValueError(msg)

    return true_arr if cond_true else false_arr
