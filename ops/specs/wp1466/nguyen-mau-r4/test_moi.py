# --- wp1466 / ADR-0068: bảy đơn vị khoá của protocol trong `doctrine-scan` ---------------------------------------------
# Mọi ca mang tiền tố `doctrine_inv_`: `_la_ho_doctrine` nhận chúng, nên đối chứng khác họ lấy từ họ máy trạng thái
# (không chạy `doctrine-scan`). Fixture: bản sao protocol THẬT, đổi đúng MỘT yếu tố.
def _inv_doan(goc: str, dau: str) -> str:
    """Trọn khối văn bản (tới dòng trống kế) bắt đầu bằng `dau`; phải có đúng một."""
    m = re.findall(r"(?ms)^" + re.escape(dau) + r".*?(?=\n[ \t]*\n)", goc)
    if len(m) != 1:
        raise AssertionError(f"fixture: cần đúng một khối mở bằng {dau!r}, thấy {len(m)}")
    return m[0]


def _inv_ca(doi, rc: int, ly_do: str = "", lien_ket: str = ""):
    def ca(c: Ctx):
        goc = (ROOT / "docs" / "PROTOCOL_DA_PHIEN.md").read_text(encoding="utf-8")
        moi, r = doi(goc), c.tmp / "r"
        (r / "docs").mkdir(parents=True, exist_ok=True)
        if not lien_ket and moi == goc:
            raise AssertionError("fixture không đổi gì so với protocol thật")
        dich = r / "docs" / "PROTOCOL_DA_PHIEN.md"
        if dich.is_symlink() or dich.exists():
            dich.unlink()
        if lien_ket:
            that = (c.tmp / "ngoai.md") if lien_ket == "ngoai" else (r / "docs" / "that.md")
            that.write_text(moi, encoding="utf-8", newline="\n")
            try:
                os.symlink(that, dich)
            except OSError as ex:
                raise BoQua(f"nền không tạo được liên kết tượng trưng: {ex}") from ex
        else:
            dich.write_text(moi, encoding="utf-8", newline="\n")
        ma, _, e = run(c.script, ["doctrine-scan", "--root", r])
        if rc:
            _doi_ly_do(rc, ma, e, ly_do, "đơn vị khoá phải ĐỎ đúng lý do")
        else:
            _doi(0, ma, e, "đổi ngoài đơn vị khoá phải XANH")
    return ca


_K = {"K01": "### 1.1 ", "K02": "1. Mỗi work packet", "K03": "### 8.3 ", "K04": "Từ lượt review thứ HAI trở đi",
      "K05": "**Tín hiệu không hội tụ theo lớp.**", "K06": "Báo riêng các lớp mới tại r+1", "K07": "Checkpoint vì tín hiệu không hội tụ"}
_inv_lay = lambda g, so: re.search(r"(?ms)^" + re.escape(_K[so]) + r".*?(?=^#)", g)[0] if _K[so][0] == "#" else _inv_doan(g, _K[so])  # noqa: E731
_inv_cho = lambda so: f"đơn vị khoá {so} "  # noqa: E731
_HANG7 = lambda g: [d for d in g.split("\n") if d.startswith("| `INV-07`")][0]  # noqa: E731
_inv_o2 = lambda hang: (lambda g: g.replace("\n## 2. Thành phần và quyền\n", "\n## 2. Thành phần và quyền\n\n" + hang + "\n", 1))  # noqa: E731
_INV_CA = {
    "xoa_cau_cat_scope": (lambda g: g.replace("Thiếu quan sát, cắt acceptance hoặc chuyển biểu hiện ra ngoài scope không được\ntính là vá.", "", 1), "K03"),
    "xoa_cau_bang_noi_slug": (lambda g: g.replace("Tách/gộp lớp cần bảng nối slug nguồn, lý do và phép\nđối chiếu trên cùng tập finding;", "", 1), "K03"),
    "xoa_cau_hai_chuyen_tiep": (lambda g: g.replace("Hai chuyển tiếp liên tiếp có tỷ lệ <50% thì dừng vòng\nvá và đưa bằng chứng tới Review Rescue Checkpoint bên dưới.", "", 1), "K05"),
    "doi_mot_ky_tu": (lambda g: g.replace("không vào tử số F.", "không vào tử số U.", 1), "K06"),
    "ngat_dong_lai": (lambda g: g.replace(_inv_lay(g, "K05"), _inv_lay(g, "K05").replace(" ", "\n", 5).replace("\n", " ", 2), 1), "K05"),
    "khoi_thut_tab": (lambda g: g.replace(_inv_lay(g, "K05"), "\t" + _inv_lay(g, "K05").replace("\n", "\n\t"), 1), "K05"),
    "khoi_trong_rao_ma": (lambda g: g.replace(_inv_lay(g, "K05"), "```\n" + _inv_lay(g, "K05") + "\n```", 1), "K05"),
    "bang_tach_dong_trong": (lambda g: g.replace(_HANG7(g), "\n" + _HANG7(g), 1), "K01"),
    "bang_them_khoang_trang": (lambda g: g.replace(_HANG7(g), _HANG7(g).replace("| `INV-07` |", "|  `INV-07`   |"), 1), "K01"),
    "doi_cho_K01_sang_phu_luc": (lambda g: g.replace(_inv_lay(g, "K01"), "", 1) + "\n## Phụ lục\n\n" + _inv_lay(g, "K01"), "K01"),
    "doi_cho_K04": (lambda g: g.replace(_inv_lay(g, "K04") + "\n\n", "", 1).replace("\n### 8.1 ", "\n" + _inv_lay(g, "K04") + "\n\n### 8.1 ", 1), "K04"),
    "nhan_doi_K04": (lambda g: g + "\n" + _inv_lay(g, "K04") + "\n", "K04"),
    "hai_tieu_muc_1_1": (lambda g: g.replace("\n## 2. Thành phần và quyền\n", "\n### 1.1 Bảng bất biến protocol\n\n## 2. Thành phần và quyền\n", 1), "K01"),
}
CASES += [(f"doctrine_inv_xoa_{so}", _inv_ca(lambda g, so=so: g.replace(_inv_lay(g, so), "", 1), 9, _inv_cho(so))) for so in _K]
CASES += [(f"doctrine_inv_{ten}", _inv_ca(doi, 9, _inv_cho(so))) for ten, (doi, so) in _INV_CA.items()]
CASES += [
    ("doctrine_inv_rao_khong_dong", _inv_ca(lambda g: g + "\n```\nrào không đóng\n", 9, "không được đóng")),
    ("doctrine_inv_dong_html", _inv_ca(lambda g: g.replace("\n### 8.3 ", "\n<div>\n\n### 8.3 ", 1), 9, "khối HTML")),
    ("doctrine_inv_dong_inv_ngoai_dang_chuan", _inv_ca(_inv_o2("| `INV-99` | x | y | chưa đo |"), 9, "nằm ngoài tiểu mục")),
    ("doctrine_inv_dong_inv_ngoai_khong_backtick", _inv_ca(_inv_o2("|INV-99|x|y|chưa đo|"), 9, "nằm ngoài tiểu mục")),
    ("doctrine_inv_dong_inv_ngoai_khong_gach_dau", _inv_ca(_inv_o2("INV-99 | x | y | chưa đo"), 9, "nằm ngoài tiểu mục")),
    ("doctrine_inv_lien_ket_ra_ngoai", _inv_ca(lambda g: g, 9, "trỏ ra ngoài --root", lien_ket="ngoai")),
    ("doctrine_inv_lien_ket_noi_bo_van_xanh", _inv_ca(lambda g: g, 0, lien_ket="trong")),
    ("doctrine_inv_ban_sao_trong_rao_ma_van_xanh", _inv_ca(lambda g: g + "\n```\n" + _inv_lay(g, "K04") + "\n```\n", 0)),
    ("doctrine_inv_sua_ngoai_don_vi_van_xanh", _inv_ca(lambda g: g.replace("Mặc định: 3 attempt/packet", "Mặc định : 3 attempt/packet", 1), 0)),
]


def case_doctrine_inv_fixture_trung_tinh_thuan(c: Ctx):
    r = _repo_gia(c.tmp, SACH, ten="inv_tt", protocol=_PROTO_TRUNG_TINH)
    rc, _, e = run(c.script, ["doctrine-scan", "--root", r])
    _doi_ly_do(9, rc, e, _inv_cho("K01"), "nguồn trung tính thuần không mang đơn vị khoá nào")


def case_doctrine_inv_chep_doctrine_van_rc_6(c: Ctx):
    r = _repo_gia(c.tmp, SACH + f"\nGhi chú: {CUM_TU_THU[0]}\n", ten="inv_rc6")
    rc, _, e = run(c.script, ["doctrine-scan", "--root", r])
    _doi_ly_do(6, rc, e, "chép doctrine", "fixture mặc định mang đủ đơn vị khoá ⇒ chép doctrine vẫn là rc 6")


CASES += [(n[5:], f) for n, f in list(globals().items()) if n.startswith("case_doctrine_inv_")]
_inv_cua = lambda so: [f"doctrine_inv_xoa_{so}"] + [f"doctrine_inv_{t}" for t, (_, k) in _INV_CA.items() if k == so and t not in ("doi_cho_K04", "nhan_doi_K04", "hai_tieu_muc_1_1")]  # noqa: E731
_INV_NGOAI = ["doctrine_inv_dong_inv_ngoai_dang_chuan", "doctrine_inv_dong_inv_ngoai_khong_backtick", "doctrine_inv_dong_inv_ngoai_khong_gach_dau"]
MUTANTS.update({
    "inv_bo_kiem_duoi_goc": ("        if not p.resolve(strict=True).is_relative_to(root.resolve(strict=True)):", "        if False:", ["doctrine_inv_lien_ket_ra_ngoai"]),
    "inv_bo_che_khong_render": ('        che, van_de = _che_khong_render(p.read_text(encoding="utf-8"))', '        che, van_de = p.read_text(encoding="utf-8"), []',
                                ["doctrine_inv_rao_khong_dong", "doctrine_inv_ban_sao_trong_rao_ma_van_xanh"]),
    "inv_bo_chan_html": ('            for i, d in enumerate(dong, 1) if re.match(r" {0,3}<", d)]', '            for i, d in enumerate(dong, 1) if False]', ["doctrine_inv_dong_html"]),
    "inv_bo_kiem_mot_muc": ("        if len(o) != 1:", "        if not o:", ["doctrine_inv_hai_tieu_muc_1_1"]),
    "inv_bo_dia_chi": ("        if not dung_cho:", "        if not dung_cho and so_ban == 0:", ["doctrine_inv_doi_cho_K04"]),
    "inv_bo_kiem_duy_nhat": ("        elif so_ban != 1:", "        elif False:", ["doctrine_inv_nhan_doi_K04"]),
    "inv_duy_nhat_lech_so": ("        elif so_ban != 1:", "        elif so_ban != 2:", ["doctrine_inv_sua_ngoai_don_vi_van_xanh", "doctrine_inv_lien_ket_noi_bo_van_xanh", "doctrine_scan_repo_that_sach"]),
    "inv_bo_kiem_id_ngoai": ("    if lac:", "    if False:", _INV_NGOAI),
    "inv_id_chi_dang_chuan": ('if "|" in d and _INV_ID_TRAN.search(d) and', 'if d.startswith("| `INV-") and', _INV_NGOAI[1:]),
    "inv_doctrine_scan_bo_goi": ("    if loi_inv:\n", "    if False:\n", [t for so in _K for t in _inv_cua(so)] + _INV_NGOAI + ["doctrine_inv_dong_html", "doctrine_inv_rao_khong_dong", "doctrine_inv_lien_ket_ra_ngoai", "doctrine_inv_fixture_trung_tinh_thuan"]),
})
MUTANTS.update({f"inv_bo_khoa_{so}": (f'    ("{so}", ', f'    # ("{so}", ', _inv_cua(so)) for so in _K})
MUTANTS["t1466_fixture_ve_trung_tinh"] = ("        protocol if protocol is not None else _proto_co_" + "khoa(), encoding=", "        protocol if protocol is not None else _PROTO_TRUNG_TINH, encoding=",
                                           ["doctrine_inv_chep_doctrine_van_rc_6", "doctrine_scan_sach_xanh"])
MUTANTS_NHAM_TEST = MUTANTS_NHAM_TEST | {"t1466_fixture_ve_trung_tinh"}
