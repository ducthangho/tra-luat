"""Dựng NGUỒN ỨNG VIÊN (prototype, không commit) của P2b từ tl_gws.py base. Dùng: python3 -I vá_ung_vien.py <vào> <ra>"""
import sys
s = open(sys.argv[1], encoding="utf-8").read()
CAP = [
('''    # 1) FULL config (token + rootFolderId/categories/…) → env + MERGE vào ~/.tra_luat_config.json
    if bundle.get("token"):
''', '''    # 1) FULL config (token + rootFolderId/categories/…) → env + MERGE vào ~/.tra_luat_config.json
    ly_env = _kiem_env_w6(bundle) if bundle.get("token") else None   # WP433 P2b: kiểm CẢ HAI trường TRƯỚC mọi phép gán env
    if ly_env:
        print(f"[bootstrap] ✗ {ly_env}", file=sys.stderr); degraded = True
    elif bundle.get("token"):
'''),
('''                except Exception:
                    existing = {}
            if ly_cfg is None:
                existing.update({k: v for k, v in bundle.items() if k != "gws_cred" and not (k == "nlm_auth" and ly_jar)})
                _ghi_nguyen_tu_0600(cfgp, json.dumps(existing, ensure_ascii=False).encode("utf-8"))
                print(''', '''                except Exception:
                    existing = {}
                if not isinstance(existing, dict):   # WP433 P2b: config cũ không phải dict ⇒ như không parse được
                    existing = {}
            if ly_cfg is None:
                existing.update({k: v for k, v in bundle.items() if k != "gws_cred" and not (k == "nlm_auth" and ly_jar)})
                try:   # WP433 P2b: CHỈ quanh tuần tự hoá
                    du_cfg = json.dumps(existing, ensure_ascii=False, allow_nan=False).encode("utf-8")
                except ValueError:   # WP433 P2b: NaN/±Infinity hoặc surrogate ⇒ từ chối, không ghi
                    du_cfg, ly_cfg = None, "dữ liệu không hợp lệ: config"
            if ly_cfg is None:
                _ghi_nguyen_tu_0600(cfgp, du_cfg)
                print('''),
('''def _duong_dich_chuan(p: str, cwd: str):''', '''def _kiem_env_w6(bundle: dict) -> str | None:
    """WP433 P2b: None hoặc `dữ liệu không hợp lệ: <trường>` — `token` và `webappUrl` (khi truthy) phải là str, không NUL, encode UTF-8
    được; kiểm CẢ HAI trước mọi phép gán env. Lý do chỉ nêu TÊN trường (giá trị là bí mật)."""
    for ten in ("token", "webappUrl"):
        v = bundle.get(ten)
        if ten == "token" or v:
            try:
                if not isinstance(v, str) or "\\x00" in v:
                    raise ValueError(ten)
                v.encode("utf-8")
                if os.name == "posix":   # đúng mã hoá mà os.environ dùng (locale ASCII ⇒ từ chối thay vì ném ở phép gán)
                    v.encode(sys.getfilesystemencoding(), "surrogateescape")
            except ValueError:   # UnicodeEncodeError là lớp con của ValueError
                return f"dữ liệu không hợp lệ: {ten}"
    return None


def _duong_dich_chuan(p: str, cwd: str):'''),
]
for a, b in CAP:
    assert s.count(a) == 1, a[:60]
    s = s.replace(a, b)
open(sys.argv[2], "w", encoding="utf-8").write(s)
