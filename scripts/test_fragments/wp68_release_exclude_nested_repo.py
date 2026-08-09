# -*- coding: utf-8 -*-
"""wp68 (F3-03, Mission #54) — `release-verify` phải MIỄN NHIỄM với bản sao kho lồng.

Lớp bệnh: `_build_release_manifest` walk THƯ MỤC (`root.rglob("*")`), KHÔNG hỏi git. Một thư mục con
là bản sao đầy đủ của kho (worktree agent, thư mục `work/` của phiên khác) ⇒ mọi tệp của nó bị đếm
vào `extra_files` và `release-verify --strict` ĐỎ theo **NƠI CHẠY** chứ không theo nội dung: manifest
vẫn lành, `failed` rỗng, `expected/checked` bằng nhau. `.gitignore` không cứu được vì bộ dựng manifest
không đi qua git. Đo 09-08-2026 trên cây dev: `extra_files = 193`, 100% dưới `work/f2-d-reopen-writer/`.

Ca này khoá PHẢN CHỨNG, không khoá trạng thái hiện tại. Bốn chốt, mỗi chốt đỏ vì một lý do khác nhau:

  1. ca ÂM   — cây không có bản sao lồng ⇒ `extra_files == []` (nếu đỏ: bộ loại đang ăn nhầm tệp thật)
  2. ca DƯƠNG — cây CÓ bản sao lồng ⇒ vẫn `extra_files == []` (đỏ TRƯỚC bản vá; đây là răng của ca)
  3. GỐC KHO không bị tự loại — `file_count` giữ nguyên, `required_missing` rỗng, `SKILL.md`+`VERSION`
     còn trong gói. Thiếu chốt này thì một vị từ "loại thư mục có SKILL.md+VERSION" sẽ loại luôn CHÍNH
     gốc kho, `file_count` về 0, `extra_files` rỗng một cách vô nghĩa và MỌI cổng XANH GIẢ.
  4. TẤT ĐỊNH — `package_hash` dựng hai lần bằng nhau, VÀ bằng nhau giữa cây có/không bản sao lồng.
     Đây mới đúng là tính chất cần: hash của GÓI không được phụ thuộc nơi chạy.

Bản sao lồng đặt ở `agent/wp99-g1-codex` — CỐ Ý không phải `work/`. Đó là khuôn tên nhánh/worktree
§4 `docs/PROTOCOL_DA_PHIEN.md` khai, và ca có chốt khẳng định `agent` KHÔNG nằm trong
`_RELEASE_EXCLUDE_DIRS`: nếu ai đó chữa lớp bệnh này bằng cách thêm tên vào bảng loại-trừ, ca vẫn
phải đỏ thay vì im lặng thoái hoá thành "đã loại theo tên rồi".

Cây thử dựng trong thư mục TẠM và danh sách tệp bắt buộc SUY RA từ chính hợp đồng release
(`_RELEASE_REQUIRED_FILES` + `_RELEASE_REQUIRED_WORKFLOWS`), không chép tay: bảng chép tay sẽ trôi
lệch khỏi hợp đồng rồi hai bên gật đầu với nhau.
"""
from __future__ import annotations

import tempfile
from pathlib import Path

TEST_ID = "wp68_release_exclude_nested_repo"

# Sàn chống RỖNG: bản sao lồng phải đủ lớn để ca DƯƠNG có nghĩa. Nếu hợp đồng required-files co lại
# về vài tệp thì ca này phải ĐỎ chứ không được đúng một cách vô nghĩa.
# Đo 09-08-2026: 42 `_RELEASE_REQUIRED_FILES` + 25 `_RELEASE_REQUIRED_WORKFLOWS` = 67 tệp bắt buộc.
_SAN_TEP_LONG = 20

_NOI_DAT_BAN_SAO = ("agent", "wp99-g1-codex")


def _dung_cay(root: Path, tl_release) -> int:
    """Dựng một kho tra-luat THU NHỎ nhưng ĐỦ hợp đồng: mọi tệp bắt buộc đều có mặt.

    Đủ hợp đồng là điều kiện để chốt 3 có răng — `required_missing` rỗng chỉ chứng minh được điều gì
    khi nó vốn CÓ THỂ rỗng.
    """
    can = list(tl_release._RELEASE_REQUIRED_FILES) + list(tl_release._RELEASE_REQUIRED_WORKFLOWS)
    for rel in can:
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("wp68 stub %s\n" % rel, encoding="utf-8", newline="")
    # `VERSION` nằm trong hợp đồng; `SKILL.md` cũng vậy — cặp này chính là dấu hiệu nhận bản sao kho.
    assert (root / "SKILL.md").is_file() and (root / "VERSION").is_file()
    return len(can)


def _dat_ban_sao_long(root: Path) -> Path:
    """Chép cây `root` vào một thư mục con ⇒ bản sao ĐẦY ĐỦ (có cả SKILL.md lẫn VERSION ở gốc nó)."""
    dich = root.joinpath(*_NOI_DAT_BAN_SAO)
    dich.mkdir(parents=True, exist_ok=True)
    for src in sorted(p for p in root.rglob("*") if p.is_file()):
        rel = src.relative_to(root)
        if rel.parts[:len(_NOI_DAT_BAN_SAO)] == _NOI_DAT_BAN_SAO:
            continue                      # không chép bản sao vào chính nó
        out = dich / rel
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_bytes(src.read_bytes())
    return dich


def _kiem_vi_tu(tl_release) -> bool:
    """Vị từ nhận diện phải bắt bản sao kho mà KHÔNG bắt nhầm thư mục chỉ có `SKILL.md`.

    Ca âm ở đây không bịa: `claude-code-best-practice/**/.claude/skills/*/SKILL.md` (9 thư mục trên
    cây dev) có `SKILL.md` mà không có `VERSION`. Vị từ chỉ nhìn `SKILL.md` sẽ nuốt nhầm cả họ đó.

    VẮNG hàm ⇒ bỏ qua chốt phụ này, KHÔNG đỏ tại đây. Lý do đã trả giá khi dựng ca: bản gốc (chưa vá)
    làm fragment chết `AttributeError`, tức ca đỏ vì "thiếu một cái TÊN" chứ không vì HÀNH VI sai —
    phản chứng kiểu đó không chứng minh được `extra_files` khác rỗng, và sẽ đỏ oan ở lượt đổi tên hàm.
    Để phần hành vi bên dưới quyết định; vị từ chỉ là chốt phụ khi có mặt.
    """
    la_ban_sao = getattr(tl_release, "_is_nested_repo_copy", None)
    if not callable(la_ban_sao):
        return True
    du = ("SKILL.md", "VERSION", "scripts/tl.py")
    with tempfile.TemporaryDirectory(prefix="wp68_vitu_") as tmp:
        base = Path(tmp).resolve()
        ca = {"du_ba_marker": du, "thieu_tl_py": ("SKILL.md", "VERSION"),
              "chi_skill": ("SKILL.md",), "chi_version": ("VERSION",), "rong": ()}
        # `thieu_tl_py` = ĐÚNG hình dạng va chạm của WP68-R2-CODEX-01: một thư mục THUỘC GÓI bị thả
        # `SKILL.md`+`VERSION`. Nó PHẢI trả False, nếu không cả subtree bị loại khỏi gói.
        mong_doi = {"du_ba_marker": True, "thieu_tl_py": False,
                    "chi_skill": False, "chi_version": False, "rong": False}
        for ten, tep in ca.items():
            d = base / ten
            d.mkdir()
            for t in tep:
                p = d / t
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text("x\n", encoding="utf-8", newline="")
            if la_ban_sao(d) is not mong_doi[ten]:
                return False
        # Thư mục KHÔNG tồn tại phải trả False, không được ném.
        return la_ban_sao(base / "khong_ton_tai") is False


def _kiem_khong_nuot_tep_thuoc_goi(root: Path, tl_module, manifest_chuan) -> bool:
    """WP68-R2-CODEX-01 — TẦNG 2 (fail-closed), khoá độc lập với vị từ.

    Phản chứng: manifest KHAI một tệp mà bộ dựng gói hiện tại KHÔNG nhặt. Ở đây dựng đúng ca đó bằng
    một tệp nằm dưới `docs/` — `docs` bị `_RELEASE_EXCLUDE_DIRS` loại — rồi NHÉT nó vào manifest.
    Tệp CÓ THẬT trên đĩa và hash ĐÚNG, nên vòng `checks` (soi đĩa) sẽ xanh; thứ DUY NHẤT có thể làm
    cổng đỏ là luật `missing_from_current_manifest`. Vì thế ca này đỏ ⟺ tầng fail-closed còn sống.

    Cố ý KHÔNG đi qua vị từ bản-sao-lồng: nếu dùng ca marker thì tầng 1 (3 marker) sẽ chặn trước và
    ca này xanh vì lý do khác ⇒ mất răng. Hai tầng phải được khoá bằng hai ca độc lập.
    """
    import copy
    import hashlib

    d = root / "docs"
    d.mkdir(parents=True, exist_ok=True)
    p = d / "wp68_ngoai_goi.md"
    noi_dung = b"wp68 fail-closed probe\n"
    p.write_bytes(noi_dung)

    if tl_module._release_should_include(p, root):
        return False          # tiền đề hỏng: `docs/` phải bị loại, nếu không ca vô nghĩa

    gia = copy.deepcopy(manifest_chuan)
    gia["files"] = list(gia["files"]) + [{
        "path": "docs/wp68_ngoai_goi.md", "size": len(noi_dung),
        "sha256": hashlib.sha256(noi_dung).hexdigest(),
    }]
    gia["files"].sort(key=lambda f: f["path"])
    gia["package_hash"] = hashlib.sha256("\n".join(
        "%s\0%d\0%s" % (f["path"], f["size"], f["sha256"]) for f in gia["files"]).encode("utf-8")).hexdigest()

    rv = tl_module._verify_release_manifest(root, gia, strict=True)
    p.unlink()
    return (rv.get("ok") is False
            and "docs/wp68_ngoai_goi.md" in (rv.get("missing_from_current_manifest") or [])
            and any(str(e).startswith("EXPECTED_FILES_NOT_PACKAGED") for e in (rv.get("errors") or [])))


def _do(root: Path, tl_module, manifest_chuan):
    """Trả (file_count, package_hash, extra_files, required_missing) — dựng manifest 2 lần để so tất định."""
    m1 = tl_module._build_release_manifest(root)
    m2 = tl_module._build_release_manifest(root)
    if m1.get("package_hash") != m2.get("package_hash") or m1.get("file_count") != m2.get("file_count"):
        return None
    rv = tl_module._verify_release_manifest(root, manifest_chuan, strict=True)
    return (m1.get("file_count"), m1.get("package_hash"),
            list(rv.get("extra_files") or []), list(m1.get("required_missing") or []))


def run(tl_module) -> bool:
    from tl_core import release as tl_release

    # Chữa theo TÊN thì ca này phải mất răng một cách LỘ LIỄU, không âm thầm.
    if _NOI_DAT_BAN_SAO[0] in tl_release._RELEASE_EXCLUDE_DIRS:
        return False

    with tempfile.TemporaryDirectory(prefix="wp68_cay_") as tmp:
        root = Path(tmp).resolve()
        so_tep_hop_dong = _dung_cay(root, tl_release)
        if so_tep_hop_dong < _SAN_TEP_LONG:
            return False

        manifest_chuan = tl_module._build_release_manifest(root)
        if not manifest_chuan.get("files"):
            return False

        # ── ca ÂM: không có bản sao lồng ────────────────────────────────────────────────────────
        sach = _do(root, tl_module, manifest_chuan)
        if sach is None:
            return False
        fc_sach, hash_sach, extra_sach, thieu_sach = sach
        if extra_sach != [] or thieu_sach != [] or fc_sach != so_tep_hop_dong:
            return False
        # gốc kho còn nguyên trong gói
        duong_dan = {f["path"] for f in manifest_chuan["files"]}
        if not {"SKILL.md", "VERSION"} <= duong_dan:
            return False

        # ── ca DƯƠNG: cùng cây đó, thêm một bản sao kho lồng ───────────────────────────────────
        dich = _dat_ban_sao_long(root)
        so_tep_long = sum(1 for p in dich.rglob("*") if p.is_file())
        if so_tep_long < _SAN_TEP_LONG:
            return False                  # bản sao rỗng ⇒ ca dương vô nghĩa

        long = _do(root, tl_module, manifest_chuan)
        if long is None:
            return False
        fc_long, hash_long, extra_long, thieu_long = long

        return bool(
            extra_long == []                 # 2. bản sao lồng KHÔNG lọt vào extra_files
            and fc_long == fc_sach           # 3. gốc kho không bị tự loại — kiểm kê giữ nguyên
            and thieu_long == []
            and hash_long == hash_sach       # 4. package_hash không phụ thuộc NƠI CHẠY
            and _kiem_vi_tu(tl_release)      # 5. WP68-R2-01 tầng 1: vị từ đòi ĐỦ BA marker
            and _kiem_khong_nuot_tep_thuoc_goi(root, tl_module, manifest_chuan)   # 6. tầng 2 fail-closed
        )
