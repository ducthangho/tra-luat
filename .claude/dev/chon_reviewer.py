#!/usr/bin/env python3
"""Chọn reviewer theo độ phức tạp và kiểm bằng chứng model đã chạy."""
from __future__ import annotations
import argparse, json, posixpath, sys
if hasattr(sys.stdout, "reconfigure"): sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"): sys.stderr.reconfigure(encoding="utf-8")
MO_HINH_CHO_PHEP = ("claude-opus-5", "claude-fable-5")
NO_LUC_CHO_PHEP = ("low", "medium", "high", "xhigh", "max")
_BAC = (("claude-opus-5", "high"), ("claude-opus-5", "xhigh"),
        ("claude-fable-5", "xhigh"), ("claude-fable-5", "max"))
class KhongDoDuoc(Exception):
    """Bằng chứng thiếu hoặc không thuộc tập hữu hạn mà kho đo được."""
def _chuan_hoa_duong(duong):
    """Chap nhan dung ban POSIX chuan, tru mot slash cuoi lam nhan thu muc."""
    if "\\" in duong: raise KhongDoDuoc("đường dẫn chứa backslash; bản chuẩn dùng '/': %r" % duong.replace("\\", "/"))
    if duong.startswith("/"): raise KhongDoDuoc("đường dẫn tuyệt đối %r; bản chuẩn repo-relative không có" % duong)
    de_so = duong[:-1] if duong.endswith("/") else duong
    chuan = posixpath.normpath(de_so)
    if de_so != chuan: raise KhongDoDuoc("đường dẫn không chuẩn %r; bản chuẩn: %r" % (duong, chuan))
    if chuan == ".." or chuan.startswith("../"): raise KhongDoDuoc("đường dẫn %r thoát repo; bản chuẩn repo-relative không có" % duong)
    return chuan
def _cac_duong_dan(duong_dan):
    if isinstance(duong_dan, str): ds = duong_dan.split(",")
    else:
        try:
            ds = list(duong_dan)
        except TypeError as exc: raise KhongDoDuoc("đường dẫn không phải chuỗi/danh sách") from exc
    # `planned:` la nhan cua protocol, khong phai mot thanh phan duong dan.
    sach = []
    for x in ds:
        if not isinstance(x, str): raise KhongDoDuoc("đường dẫn không phải chuỗi: %r" % (x,))
        duong = x.strip()
        if not duong: continue
        if duong.startswith("planned:"): duong = duong[len("planned:"):].strip()
        if not duong: raise KhongDoDuoc("đường dẫn sau nhãn planned: bị rỗng")
        if duong.startswith("planned:"): raise KhongDoDuoc("nhãn planned: lặp: %r" % duong)
        duong = _chuan_hoa_duong(duong)
        sach.append(duong)
    # Trung lap khong duoc tu nang diem; rong la phep do hong, khong phai diff nho.
    ket_qua = tuple(dict.fromkeys(sach))
    if not ket_qua: raise KhongDoDuoc("write set rỗng")
    return ket_qua
def _vung(path):
    """Phân loại bằng allow-list; mọi thứ ngoài bảng đi vào `khong-biet`."""
    if path == ".claude/settings.json" or path == "RELEASE_MANIFEST.json" or path.startswith(
            (".github/workflows/", ".github/checks/", ".claude/hooks/",
                        ".claude/dev/packet_loop", "ops/lease_publish")): return "cong"
    if path == "docs/PROTOCOL_DA_PHIEN.md" or path.startswith(
            ("docs/adr/", ".claude/skills/", ".claude/agents/")): return "giao-thuc"
    if path.startswith("scripts/"): return "runtime"
    if path == ".gitignore" or path.startswith((".claude/dev/", "ops/")): return "dev"
    if path.startswith(("references/", "docs/")) or (
            "/" not in path and "\\" not in path and path.endswith(".md")): return "tai-lieu"
    return "khong-biet"
def _bac_theo_diem(diem):
    return 0 if diem <= 0 else 1 if diem <= 2 else 2 if diem <= 4 else 3
def kiem_dinh_danh(model, effort):
    """Từ chối bí danh/mức lạ bằng phép so bằng nhau với allow-list."""
    if model not in MO_HINH_CHO_PHEP: raise KhongDoDuoc("model ngoài allow-list: %r" % (model,))
    if effort not in NO_LUC_CHO_PHEP: raise KhongDoDuoc("effort ngoài allow-list: %r" % (effort,))
_HANG_REVIEW = {"routine": 0, "systemic": 1, "sensitive": 2}
def _lop_review(gia_tri):
    if not isinstance(gia_tri, str): raise KhongDoDuoc("review_class không phải chuỗi")
    gia_tri = gia_tri.strip()
    # Da dem: routine=22, systemic=167, sensitive=570, `thuong`=0.
    if gia_tri not in _HANG_REVIEW: raise KhongDoDuoc("review_class ngoài allow-list: %r" % gia_tri)
    return gia_tri
def chon(review_class, duong_dan, so_dong, luot, bac_truoc=None):
    """Trả ``(model, effort, giải thích)`` từ đúng các đối số đã cho."""
    if isinstance(review_class, dict):
        khai = _lop_review(review_class.get("review_class"))
        if "effective_review_class" in review_class:
            hieu_luc = _lop_review(review_class.get("effective_review_class"))
            # Protocol chi cho effective nang lop; lease ha lop phai giu muc khai bao.
            review_class = max((khai, hieu_luc), key=_HANG_REVIEW.get)
        else: review_class = khai
    else: review_class = _lop_review(review_class)
    # So am la phep do hong, khong phai diff nho.
    if type(so_dong) is not int or so_dong < 0 or type(luot) is not int or luot < 1:
        raise KhongDoDuoc("so_dong phải là số nguyên >= 0 và luot phải là số nguyên >= 1")
    ds = _cac_duong_dan(duong_dan)
    cac_vung = {_vung(p) for p in ds}
    khoan = []
    diem = 0
    def cong(so, ly_do):
        nonlocal diem
        diem += so
        khoan.append("+%d %s" % (so, ly_do))
    if review_class == "sensitive": cong(2, "review_class=sensitive")
    if review_class == "systemic": cong(1, "review_class=systemic")
    if "cong" in cac_vung: cong(2, "chạm vùng cong")
    if "giao-thuc" in cac_vung: cong(1, "chạm vùng giao-thuc")
    if len(ds) >= 5: cong(1, "số tệp=%d >= 5" % len(ds))
    if so_dong >= 400: cong(1, "số dòng=%d >= 400" % so_dong)
    if luot >= 3: cong(1, "lượt=%d >= 3" % luot)
    if "khong-biet" in cac_vung: cong(3, "chạm vùng khong-biet")
    chi_so = _bac_theo_diem(diem)
    banh_coc = ""
    if bac_truoc is not None:
        if not isinstance(bac_truoc, (tuple, list)) or len(bac_truoc) != 2: raise KhongDoDuoc("bậc trước phải có đúng model,effort; nhận %r" % (bac_truoc,))
        bac_truoc = tuple(bac_truoc)
        kiem_dinh_danh(*bac_truoc)
        if bac_truoc not in _BAC: raise KhongDoDuoc("bậc trước không phải một bậc chọn hợp lệ: %r" % (bac_truoc,))
        truoc = _BAC.index(bac_truoc)
        if truoc > chi_so:
            chi_so = truoc
            banh_coc = "; bánh cóc giữ bậc trước=%s/%s" % bac_truoc
    model, effort = _BAC[chi_so]
    kiem_dinh_danh(model, effort)
    chi_tiet = ", ".join(khoan) if khoan else "không có khoản điểm cộng"
    giai_thich = "%s; tổng=%d%s; bậc cuối=%s/%s" % (
        chi_tiet, diem, banh_coc, model, effort)
    return model, effort, giai_thich
_MO_HINH_PHU = ("claude-haiku-",)
def kiem_ket_qua(yeu_cau_model, ket_qua_json):
    """Doi hoi tap model chinh bang dung tap chi co model yeu cau.

    Hai luot dai ngay 27-08-2026 mang ca fable-5 va opus-4-8, nhung ``rc=0``
    va ``subtype=success``. Vi vay hai truong do khong tham gia nhanh DAT.
    Haiku co mat 8/9 luot: chi duoc cho phep, khong duoc doi phai co.
    Gioi han: phep tap hop chi hoi model phu CO MAT, khong hoi no LAM GI;
    fable 500 token + haiku 90000 token van DAT. Chua do share nen khong dat nguong.
    """
    if not isinstance(yeu_cau_model, str) or not yeu_cau_model: raise KhongDoDuoc("model yêu cầu không phải chuỗi có nội dung: %r" % yeu_cau_model)
    if not isinstance(ket_qua_json, dict): raise KhongDoDuoc("kết quả JSON thiếu hoặc không phải object")
    model_usage = ket_qua_json.get("modelUsage")
    if not isinstance(model_usage, dict) or not model_usage: raise KhongDoDuoc("modelUsage thiếu/rỗng/không phải object")
    def danh_tinh(ten, thong_tin):
        if not isinstance(ten, str) or not ten: raise KhongDoDuoc("khoá modelUsage không phải chuỗi có nội dung: %r" % ten)
        if isinstance(thong_tin, dict) and "canonicalModel" in thong_tin:
            can = thong_tin["canonicalModel"]
            if not isinstance(can, str) or not can:
                raise KhongDoDuoc("canonicalModel không phải chuỗi có nội dung: %r" % can)
            return can
        return ten
    muc = [(ten, danh_tinh(ten, thong_tin))
           for ten, thong_tin in model_usage.items()]
    phu = sorted(ten for ten, dinh_danh in muc
                 if dinh_danh.startswith(_MO_HINH_PHU))
    chinh = {dinh_danh for ten, dinh_danh in muc if ten not in phu}
    # Hai nhanh hong khac nhau: model yeu cau VANG va model LA cung co mat.
    if chinh != {yeu_cau_model}:
        if yeu_cau_model not in chinh:
            raise KhongDoDuoc(
                "model yêu cầu %r không có trong tập model chính %r; mô hình phụ=%r"
                % (yeu_cau_model, sorted(chinh), phu))
        la = sorted(chinh - {yeu_cau_model})
        raise KhongDoDuoc(
            "model yêu cầu %r có mặt nhưng còn mô hình LẠ %r; mô hình phụ=%r"
            % (yeu_cau_model, la, phu))
    # Kiem sau phep so tap de model rac bi chan o nhanh model yeu cau VANG.
    if ket_qua_json.get("is_error") is not False:
        raise KhongDoDuoc("is_error thiếu hoặc không bằng false")
    return "modelUsage: ĐẠT; tập model chính=%r; mô hình phụ bỏ qua=%r" % (
        sorted(chinh), phu)
def main(argv=None):
    p = argparse.ArgumentParser(description="Chọn reviewer theo độ phức tạp")
    p.add_argument("--review-class", required=True)
    p.add_argument("--duong-dan", required=True)
    p.add_argument("--so-dong", required=True, type=int)
    p.add_argument("--luot", required=True, type=int)
    p.add_argument("--bac-truoc")
    p.add_argument("--effective-review-class")
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)
    try:
        bac_truoc = None
        if a.bac_truoc is not None:
            phan = tuple(x.strip() for x in a.bac_truoc.split(","))
            if len(phan) != 2 or not all(phan):
                raise KhongDoDuoc("--bac-truoc phải có dạng model,effort")
            kiem_dinh_danh(*phan)
            bac_truoc = phan
        lop = ({"review_class": a.review_class, "effective_review_class": a.effective_review_class}
               if a.effective_review_class is not None else a.review_class)
        model, effort, giai_thich = chon(lop, a.duong_dan, a.so_dong, a.luot, bac_truoc)
        kiem_dinh_danh(model, effort)
    except KhongDoDuoc as exc:
        print("KHÔNG ĐO ĐƯỢC: %s" % exc, file=sys.stderr)
        return 2
    if a.json:
        print(json.dumps({"model": model, "effort": effort,
                          "giai_thich": giai_thich}, ensure_ascii=False))
    else:
        print("model: %s\neffort: %s\ngiai_thich: %s" % (model, effort, giai_thich))
    return 0
if __name__ == "__main__":
    sys.exit(main())
