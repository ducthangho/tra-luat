# --- wp1466 / ADR-0068: đơn vị khoá của protocol trong `doctrine-scan` --------------------------------
# Mọi ca mang tiền tố `doctrine_inv_`: `_la_ho_doctrine` nhận chúng, nên đối chứng khác họ lấy từ họ máy trạng thái
# (không chạy `doctrine-scan`) và đứng ngoài tầm mọi đột biến ở đây. Fixture: bản sao protocol THẬT, đổi đúng MỘT yếu tố.
def _inv_doan(goc: str, dau: str) -> str:
    """Trọn khối văn bản (tới dòng trống kế) bắt đầu bằng `dau`; phải có đúng một."""
    m = re.findall(r"(?ms)^" + re.escape(dau) + r".*?(?=\n[ \t]*\n)", goc)
    if len(m) != 1:
        raise AssertionError(f"fixture: cần đúng một khối mở bằng {dau!r}, thấy {len(m)}")
    return m[0]


def _inv_muc(goc: str, dau: str) -> str:
    return re.search(r"(?ms)^" + re.escape(dau) + r".*?(?=^#)", goc)[0]


def _inv_ca(doi, rc: int, ly_do: str = "", lien_ket: str = ""):
    def ca(c: Ctx):
        goc = (ROOT / "docs" / "PROTOCOL_DA_PHIEN.md").read_text(encoding="utf-8")
        moi, r = doi(goc), c.tmp / "r"
        (r / "docs").mkdir(parents=True, exist_ok=True)
        if rc and not lien_ket and moi == goc:
            raise AssertionError("fixture không đổi gì so với protocol thật")
        dich = r / "docs" / "PROTOCOL_DA_PHIEN.md"
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
            _doi(0, ma, e, "đổi vô hại phải XANH")
    return ca


_K = {"K01": "### 1.1 ", "K02": "1. Mỗi work packet", "K03": "### 8.3 ", "K04": "Từ lượt review thứ HAI trở đi",
      "K05": "**Tín hiệu không hội tụ theo lớp.**", "K06": "Báo riêng các lớp mới tại r+1", "K07": "Checkpoint vì tín hiệu không hội tụ"}
_inv_lay = lambda g, so: (_inv_muc if _K[so].startswith("#") else _inv_doan)(g, _K[so])  # noqa: E731
_K5 = lambda g: _inv_doan(g, _K["K05"])  # noqa: E731
_HANG7 = lambda g: [d for d in g.split("\n") if d.startswith("| `INV-07`")][0]  # noqa: E731
CASES += [(f"doctrine_inv_xoa_{so}", _inv_ca(lambda g, so=so: g.replace(_inv_lay(g, so), "", 1), 9, f"đơn vị khoá {so} ")) for so in _K]
CASES += [
    ("doctrine_inv_xoa_cau_cat_scope", _inv_ca(lambda g: g.replace("Thiếu quan sát, cắt acceptance hoặc chuyển biểu hiện ra ngoài scope không được\ntính là vá.", "", 1), 9, "đơn vị khoá K03 ")),
    ("doctrine_inv_xoa_cau_bang_noi_slug", _inv_ca(lambda g: g.replace("Tách/gộp lớp cần bảng nối slug nguồn, lý do và phép\nđối chiếu trên cùng tập finding;", "", 1), 9, "đơn vị khoá K03 ")),
    ("doctrine_inv_xoa_cau_hai_chuyen_tiep", _inv_ca(lambda g: g.replace("Hai chuyển tiếp liên tiếp có tỷ lệ <50% thì dừng vòng\nvá và đưa bằng chứng tới Review Rescue Checkpoint bên dưới.", "", 1), 9, "đơn vị khoá K05 ")),
    ("doctrine_inv_doi_mot_ky_tu", _inv_ca(lambda g: g.replace("không vào tử số F.", "không vào tử số U.", 1), 9, "đơn vị khoá K06 ")),
    ("doctrine_inv_khoi_trong_rao_ma", _inv_ca(lambda g: g.replace(_K5(g), "```\n\n" + _K5(g) + "\n\n```", 1), 9, "đơn vị khoá K05 ")),
    ("doctrine_inv_khoi_trong_comment_html", _inv_ca(lambda g: g.replace(_K5(g), "<!--\n\n" + _K5(g) + "\n\n-->", 1), 9, "đơn vị khoá K05 ")),
    ("doctrine_inv_rao_khong_dong", _inv_ca(lambda g: g + "\n```\nrào không đóng\n", 9, "không được đóng")),
    ("doctrine_inv_dong_html", _inv_ca(lambda g: g.replace("\n### 8.3 ", "\n<div>\n\n### 8.3 ", 1), 9, "khối HTML")),
    ("doctrine_inv_khoi_thut_bon", _inv_ca(lambda g: g.replace(_K5(g), "    " + " ".join(_K5(g).split()), 1), 9, "đơn vị khoá K05 ")),
    ("doctrine_inv_ngat_dong_lai_van_xanh", _inv_ca(lambda g: g.replace(_K5(g), _K5(g).replace(" ", "\n", 5).replace("\n", " ", 2), 1), 0)),
    ("doctrine_inv_bang_tach_dong_trong", _inv_ca(lambda g: g.replace(_HANG7(g), "\n" + _HANG7(g), 1), 9, "đơn vị khoá K01 ")),
    ("doctrine_inv_bang_them_khoang_trang_van_xanh", _inv_ca(lambda g: g.replace(_HANG7(g), _HANG7(g).replace("| `INV-07` |", "|  `INV-07`   |"), 1), 0)),
    ("doctrine_inv_dong_inv_ngoai_tieu_muc", _inv_ca(lambda g: g.replace("\n## 2. Thành phần và quyền\n", "\n## 2. Thành phần và quyền\n\n| `INV-99` | x | y | chưa đo |\n", 1), 9, "nằm ngoài tiểu mục")),
    ("doctrine_inv_lien_ket_ra_ngoai", _inv_ca(lambda g: g, 9, "trỏ ra ngoài --root", lien_ket="ngoai")),
    ("doctrine_inv_lien_ket_noi_bo_van_xanh", _inv_ca(lambda g: g, 0, lien_ket="trong")),
]


def case_doctrine_inv_fixture_trung_tinh_thuan(c: Ctx):
    r = _repo_gia(c.tmp, SACH, ten="inv_tt", protocol=_PROTO_TRUNG_TINH)
    rc, _, e = run(c.script, ["doctrine-scan", "--root", r])
    _doi_ly_do(9, rc, e, "đơn vị khoá K01 ", "nguồn trung tính thuần không mang đơn vị khoá nào")


def case_doctrine_inv_chep_doctrine_van_rc_6(c: Ctx):
    r = _repo_gia(c.tmp, SACH + f"\nGhi chú: {CUM_TU_THU[0]}\n", ten="inv_rc6")
    rc, _, e = run(c.script, ["doctrine-scan", "--root", r])
    _doi_ly_do(6, rc, e, "chép doctrine", "fixture mặc định mang đủ đơn vị khoá ⇒ chép doctrine vẫn là rc 6")


CASES += [(n[5:], f) for n, f in list(globals().items()) if n.startswith("case_doctrine_inv_")]
_INV_DO = [t for t, _ in CASES if t.startswith("doctrine_inv_") and not t.endswith("_van_xanh") and t not in (
    "doctrine_inv_lien_ket_ra_ngoai", "doctrine_inv_rao_khong_dong", "doctrine_inv_dong_html", "doctrine_inv_dong_inv_ngoai_tieu_muc", "doctrine_inv_chep_doctrine_van_rc_6")]
MUTANTS.update({
    "inv_bo_kiem_duoi_goc": ("        if not p.resolve(strict=True).is_relative_to(root.resolve(strict=True)):", "        if False:", ["doctrine_inv_lien_ket_ra_ngoai"]),
    "inv_bo_che_khong_render": ('        che, van_de = _che_khong_render(p.read_text(encoding="utf-8"))', '        che, van_de = p.read_text(encoding="utf-8"), []',
                                ["doctrine_inv_khoi_trong_rao_ma", "doctrine_inv_khoi_trong_comment_html", "doctrine_inv_rao_khong_dong"]),
    "inv_bo_chan_html": ('            for i, d in enumerate(che.split("\\n"), 1) if re.match(r" {0,3}<", d)]', '            for i, d in enumerate(che.split("\\n"), 1) if False]', ["doctrine_inv_dong_html"]),
    "inv_khoi_thut_khong_danh_dau": ('                      ("    " if khoi[0].startswith("    ") else "") + chuan(" ".join(khoi)))', '                      chuan(" ".join(khoi)))', ["doctrine_inv_khoi_thut_bon"]),
    "inv_khong_gop_dong": ('chuan(" ".join(khoi)))', '"\\n".join(map(chuan, khoi)))', ["doctrine_inv_ngat_dong_lai_van_xanh", "doctrine_inv_lien_ket_noi_bo_van_xanh", "doctrine_scan_repo_that_sach"]),
    "inv_bang_gop_dong": ('            ra.append("\\n".join(map(chuan, khoi)) if khoi[0].startswith("|") else', '            ra.append("\\n".join(map(chuan, khoi)) if False else', ["doctrine_inv_bang_them_khoang_trang_van_xanh", "doctrine_scan_sach_xanh"]),
    "inv_bo_kiem_khoa": ("for so, loai, bam in INV_KHOA_PROTOCOL if bam not in co[loai]]", "for so, loai, bam in INV_KHOA_PROTOCOL if False]", _INV_DO),
    "inv_bo_dem_dong_inv": ("    if bang and dem(khoi) != dem(bang[0]):", "    if False:", ["doctrine_inv_dong_inv_ngoai_tieu_muc"]),
    "inv_doctrine_scan_bo_goi": ("    if loi_inv:\n", "    if False:\n", _INV_DO + ["doctrine_inv_dong_html", "doctrine_inv_rao_khong_dong", "doctrine_inv_dong_inv_ngoai_tieu_muc", "doctrine_inv_lien_ket_ra_ngoai"]),
})
MUTANTS.update({f"inv_bo_khoa_{so}": (f'    ("{so}", ', f'    # ("{so}", ', [f"doctrine_inv_xoa_{so}"]) for so in _K})
MUTANTS["t1466_fixture_ve_trung_tinh"] = ("        protocol if protocol is not None else _proto_co_khoa(), encoding=", "        protocol if protocol is not None else _PROTO_TRUNG_TINH, encoding=",
                                           ["doctrine_inv_chep_doctrine_van_rc_6", "doctrine_scan_sach_xanh"])
MUTANTS_NHAM_TEST = MUTANTS_NHAM_TEST | {"t1466_fixture_ve_trung_tinh"}
