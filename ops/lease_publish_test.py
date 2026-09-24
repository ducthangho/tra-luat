#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phản chứng cho `lease_publish.py` — cổng chặn TRƯỚC khi một lease được đăng.

Vì sao cần cổng này: workflow chạy bằng `GITHUB_TOKEN`, nghĩa là **push được thành
đăng được**. Thứ duy nhất đứng giữa một tệp YAML trong kho và một comment mang danh
nghĩa kho là bộ kiểm này. Nó mà xanh dễ dãi thì đường git-thay-API trở thành đường
đăng bừa.

Cùng doctrine với `packet_loop_test.py`: gọi CHÍNH lệnh qua subprocess, không import.
Thứ workflow gõ là lệnh, nên thứ được đo phải là lệnh.

Chạy: python3 ops/lease_publish_test.py
"""

from __future__ import annotations

import os
import re
import shlex
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "lease_publish.py"
# Cờ NỘI BỘ của `t125`, cố ý là ĐỐI SỐ chứ không phải biến môi trường: argv không
# được kế thừa, nên không môi trường nào tắt được phép A/B một cách tình cờ.
CO_AB = "--ab-con-noi-bo"
SC_LOAI_TRU_NHU_ACTIONLINT = "SC1091,SC2194,SC2050,SC2154,SC2157,SC2043"   # đúng bộ actionlint 1.7.7 truyền cho shellcheck
AL_HAN_GIAY = 180        # hạn MỘT lời gọi actionlint trong t137 (packet #504 M5 bước 2) — lý do tại t137
SC_HAN_TONG_GIAY = 180   # hạn TOÀN BỘ vòng shellcheck của t137 — TỔNG, không phải mỗi lời gọi
CD_HAN_TONG_GIAY = 120   # hạn TOÀN BỘ chẩn đoán khi actionlint treo (`_chan_doan_actionlint_treo`)
# Vì sao shellcheck dùng hạn TỔNG mà không phải hạn MỖI LỜI GỌI: số thân `run` bash trong workflow là
# DỮ LIỆU (hôm nay 2), nên hạn-mỗi-lời-gọi làm trần của t137 trôi theo dữ liệu, và mọi con số dẫn xuất
# từ nó cũng trôi — đúng hình dạng "bất biến còn đúng, số hạng đã trôi". Hạn TỔNG cho t137 một trần
# ĐỘC LẬP với số thân, nên `T137_TRAN_GIAY` dưới đây là một con số đo được, không phải một phép đoán.
T137_TRAN_GIAY = AL_HAN_GIAY + SC_HAN_TONG_GIAY + CD_HAN_TONG_GIAY       # 480


def _han_ngoai_toi_thieu(han_actionlint, han_sc_tong, han_chan_doan, suite_do_duoc, du_phong):
    """Hạn NGOÀI tối thiểu = tổng hạn TRONG có thể tiêu HỢP LỆ + thời gian suite đã ĐO + dự phòng.

    Hàm thuần, không đọc hằng nào, để `t156` gọi lại được với số THU NHỎ: một phản chứng chạy trong
    vài giây vẫn đo đúng QUAN HỆ mà `AB_HAN_GIAY` phải giữ, thay vì phải chờ 540 s thật.
    """
    return han_actionlint + han_sc_tong + han_chan_doan + suite_do_duoc + du_phong


AB_SUITE_DO_DUOC_GIAY = 350   # đo Windows M4 lượt 4: t125 = 344.438 s (lượt con = TOÀN suite trừ t125)
AB_DU_PHONG_GIAY = 120
# hạn MỖI lượt con của t125. Cross-review codex 11-09-2026 (P2): bản trước ghi tay 420 s, NHỎ HƠN tổng
# hạn trong của riêng t137 (180 + 180×2 = 540) ⇒ con bị giết dù mọi lệnh còn trong hạn RIÊNG của nó, và
# verdict lồng lệch verdict đứng một mình. Nay dẫn xuất, nên không sửa được một vế mà quên vế kia.
AB_HAN_GIAY = _han_ngoai_toi_thieu(AL_HAN_GIAY, SC_HAN_TONG_GIAY, CD_HAN_TONG_GIAY,
                                   AB_SUITE_DO_DUOC_GIAY, AB_DU_PHONG_GIAY)      # 950
AB_TRAN_CUNG_GIAY = 1500   # trần CỨNG. Hạn ngoài phải nằm DƯỚI nó, và nó nằm dưới trần job 60 phút của
#                            `ci.yml` — nâng hạn ngoài cho tới khi hết treo là đổi cổng lấy sự im lặng.
RC_CHON_CA_SAI = 3       # `--chi-ca=` rỗng hoặc không khớp ca nào ⇒ KHÔNG chạy gì và KHÔNG xanh
WORKFLOW_DANG = HERE.parent / ".github" / "workflows" / "ops-publish-lease.yml"

RC_OK, RC_THAM_SO, RC_TU_CAP, RC_DA_DANG, RC_NOI_DUNG, RC_NEO, RC_LOP = 0, 2, 4, 9, 8, 6, 10

# Dấu phân cách cho fixture N10 (`t171`); `t173` canh chính hằng này. KHÔNG được là ":" —
# đường tuyệt đối Windows mang dấu hai chấm của Ổ ĐĨA nên `f"{a}:{b}"` bị chính nó cắt nát.
PHAN_CACH_THU_N10 = "|"

CA: list = []


class BoQuaNen(Exception):
    def __init__(self, tep=None, ten_job=None):
        self.tep, self.ten_job = tep, ten_job

def ca(fn):
    CA.append(fn)
    return fn


def chay(*doi_so, env=None, cwd=None):
    # HERMETIC (packet #396, đóng N9). `env=None` giao cho `subprocess.run` KẾ THỪA cả
    # môi trường cha — kể cả `GITHUB_ACTOR` mà runner của Actions luôn đặt. Cổng thẩm
    # quyền trong `lease_publish.py` đọc đúng biến ấy, nên bộ test đang tự bắn vào chân
    # mình: đo 29-08-2026, một lượt merge do `notebyme88` bấm làm 29 ca ĐỎ oan.
    #
    # Mặc định xoá ĐÚNG một biến. Ca nào cần actor thì truyền `env=` tường minh — lúc đó
    # lời khai của ca thắng, và đó là điều đúng: ca ấy đang ĐO hành vi theo actor.
    if env is None:
        env = {k: v for k, v in os.environ.items() if k != "GITHUB_ACTOR"}
    p = subprocess.run([sys.executable, str(SCRIPT), *[str(x) for x in doi_so]],
                       capture_output=True, text=True, env=env, cwd=cwd)
    return p.returncode, p.stdout, p.stderr


def _kiem_sach(mod, *doi_so):
    """Gọi `kiem()` TRONG TIẾN TRÌNH với `GITHUB_ACTOR` đã gỡ (packet #396, đóng N9).

    Đường thứ ba rò actor, và là đường khó thấy nhất: `chay()` spawn tiến trình con nên
    còn nhìn thấy `env=`, `_goi_lop_gh` có `patch.dict` nên còn nhìn thấy chỗ để sửa —
    còn ở đây ca test gọi THẲNG hàm sản phẩm, nên nó đọc `os.environ` của chính suite mà
    không có cái móc nào lộ ra.

    KHÔNG chữa bằng `os.environ.pop` toàn cục ở đầu suite. Làm thế thì `t125` (A/B) trở
    thành HẰNG ĐÚNG: lượt con có actor sẽ tự gỡ actor ngay khi khởi động, hai lượt giống
    nhau DO CẤU TẠO chứ không phải do các helper hermetic. Một ca không thể đỏ thì không
    phải một ca.
    """
    from unittest import mock
    moi = {k: v for k, v in os.environ.items() if k != "GITHUB_ACTOR"}
    with mock.patch.dict(os.environ, moi, clear=True):
        return mod.kiem(*doi_so)


def _doc_do_gia(tep: Path, rc: int, stdout: str, stderr: str, mo_ta: str) -> str:
    if not tep.is_file():
        raise AssertionError(f"KHÔNG ĐO ĐƯỢC {mo_ta}: đồ giả không sinh tệp {tep}; "
                             f"rc={rc}, stdout={stdout!r}, stderr={stderr!r}")
    return tep.read_text(encoding="utf-8")

def mai_sau(gio=4) -> str:
    return (datetime.now(timezone.utc) + timedelta(hours=gio)).strftime("%Y-%m-%dT%H:%M:%SZ")


def khi_truoc(gio=4) -> str:
    return (datetime.now(timezone.utc) - timedelta(hours=gio)).strftime("%Y-%m-%dT%H:%M:%SZ")


SHA40 = "cf39109c9e5167516c53f2071e5fa7ec5c6afff5"


def lease_mau(**doi) -> dict:
    d = {
        "schema_version": 1,
        "event": "review_lease_granted",
        "packet_issue": 55,
        "packet_id": "wp55",
        "lease_id": "wp55-r2-review-3-codex-20260814",
        "role": "reviewer",
        "provider": "codex",
        "target_pull_request": 92,
        "reviewed_sha_required": SHA40,
        "granted_by": "ducthangho",
        "lease_expires_at_utc": mai_sau(),
        "attempts_used": 2,
        "attempts_limit": 3,
    }
    d.update(doi)
    return d


def viet(tmp: Path, lease: dict, ten="l.yaml") -> Path:
    import yaml
    p = tmp / ten
    p.write_text(yaml.safe_dump(lease, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return p


class San:
    def __enter__(self):
        self.d = Path(tempfile.mkdtemp(prefix="lp_"))
        return self.d

    def __exit__(self, *a):
        import shutil
        shutil.rmtree(self.d, ignore_errors=True)


def bang(dk, msg):
    if not dk:
        raise AssertionError(msg)


def dat_prompt(goc: Path, noi_dung: bytes, duong="ops/prompts/p.md") -> tuple[str, str]:
    """Đặt một tệp prompt trong "kho" giả, trả về (đường dẫn tương đối, sha256)."""
    import hashlib
    f = goc / duong
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_bytes(noi_dung)
    return duong, hashlib.sha256(noi_dung).hexdigest()


def _nap_cong():
    import importlib.util
    spec = importlib.util.spec_from_file_location("lease_publish_thu", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class GhGia:
    """GitHub giả giữ DANH SÁCH comment theo issue, không trả lời theo lượt."""
    def __init__(self, loai=None, comments=None, loi_comment=()):
        self.loai = loai or {}
        self.comments = {int(k): list(v) for k, v in (comments or {}).items()}
        self.loi_comment = set(loi_comment)
        self.calls = []

    def __call__(self, *args):
        import json
        self.calls.append(args)
        endpoint = next((x for x in args if str(x).startswith("repos/")), "")
        so = int(endpoint.split("/issues/", 1)[1].split("/", 1)[0])
        if endpoint.endswith("/comments"):
            if so in self.loi_comment:
                return subprocess.CompletedProcess(args, 1, "", "comments hong")
            return subprocess.CompletedProcess(
                args, 0, json.dumps([self.comments.get(so, [])]), "")
        loai = self.loai.get(so, "issue")
        if loai == "loi":
            return subprocess.CompletedProcess(args, 1, "", "issue hong")
        doan = "pull" if loai == "pr" else "issues"
        return subprocess.CompletedProcess(
            args, 0, json.dumps({"html_url": f"https://github.com/o/r/{doan}/{so}"}), "")

    def dang(self, so: int, body: str):
        ds = self.comments.setdefault(so, [])
        comment = {"id": 9000 + len(ds), "body": body,
                   "user": {"login": "github-actions[bot]"}}
        ds.append(comment)
        self.calls.append(("POST", so, comment["id"]))
        return comment["id"]


ENV_GITHUB = {"GITHUB_REPOSITORY": "o/r"}


def _thong_diep_an_toan(ex) -> str:
    """`str(ex)` của một ngoại lệ TUỲ BIẾN có thể NÉM, hoặc trả thứ KHÔNG PHẢI chuỗi.

    Cross-review lượt 5 bắt (`helper-exception-formatting-escapes-own-assertion`): `_MaVang`
    gọi `str(ex)` trước khi trả sentinel, và `_NgoaiLeLa.__str__` lại định dạng ngoại lệ gốc
    lần nữa. Một ngoại lệ thuộc `Exception` mà `__str__` ném thì helper KHÔNG trả được kết
    quả, và ngoại lệ trần thoát ra — **làm vỡ CẢ LỚP ca gọi helper**, không riêng một ca.
    Đo được: họ 41 vị trí × `StringFails` cho `RAW = 41/41`.

    Đây là chiều ĐỊNH DẠNG, xuyên mọi ca. Và nó cay đúng chỗ: đường CHẨN ĐOÁN — thứ dựng ra
    để phép đo đọc được — lại là thứ làm vỡ phép đo.

    THÔNG ĐIỆP DỰ PHÒNG CỐ Ý KHÔNG NÊU TÊN LỚP NÀO. Reviewer cảnh báo đúng chỗ này, và bản
    thử đầu của chính họ đã dính: nếu dự phòng ghi tên lớp của lỗi ĐỊNH DẠNG (`__str__` ném
    `RuntimeError`) thì một phép kiểm substring tìm tên lớp NGOÀI sẽ nhận nhầm. Tên lớp thật
    chỉ sống ở `_MaVang.kieu` / `_NgoaiLeLa.kieu`, lấy từ `type(ex).__name__` — thứ không đi
    qua `__str__`.
    """
    try:
        td = ex.__str__()
    except BaseException:  # noqa: BLE001 — đường chẩn đoán KHÔNG được làm vỡ phép đo
        return "<__str__ hỏng>"
    if not isinstance(td, str):
        return "<__str__ trả thứ không phải chuỗi>"
    return _chuoi_thuan(td, "<không hạ được về chuỗi thuần>")


def _chuoi_thuan(x, du_phong: str) -> str:
    """Hạ `x` về một `str` THUẦN — không còn `__str__`/`__format__`/`__repr__` của ai cả.

    VÌ SAO CẦN, và đây là chỗ bản vá lượt 5 còn HỞ: `isinstance(td, str)` **ĐÚNG với một LỚP
    CON của `str`**, mà lớp con thì ghi đè được `__str__`, `__format__`, `__repr__`. Thông
    điệp chẩn đoán sau đó đi vào một f-string của `chot`, và chính lúc ấy nó nổ — tức ca ĐỎ
    vì đường chẩn đoán chứ không vì thứ nó đo. Cross-review lượt 6 đo: **RAW 82 / 96 phép**
    trên hai họ `str` con hỏng định dạng.

    Cùng LỚP với `_MaVang`: một giá trị TRÔNG NHƯ thứ ta cần mà mang theo một callback của
    bên bị đo. Khác chỗ: `_MaVang` chặn ở tầng SO SÁNH, hàm này chặn ở tầng ĐỊNH DẠNG.

    Ba cách hạ đều đo được là cho `str` thuần (đo 21-09, `SubHong(str)` ghi đè cả ba):
    `str.__str__(x)` · `x[:]` · `"".join((x,))`. Ngược lại `str(x)`, `"%s" % (x,)`, `f"{x}"`
    đều NÉM — chúng đi qua đúng cái callback đang muốn tránh. Dùng `str.__str__` vì nó tra
    trên LỚP `str` dựng sẵn, không tra trên instance, nên không có đường nào che.

    Vẫn bọc `try`: một lớp con có thể cài `__getattribute__` quái gở. Và chốt lại bằng
    `type(...) is str` — "không ném" chưa phải "đã thuần".
    """
    try:
        r = str.__str__(x)
    except BaseException:  # noqa: BLE001 — cùng lý do: chẩn đoán không được làm vỡ phép đo
        return du_phong
    return r if type(r) is str else du_phong


def _ten_lop(ex) -> str:
    """Tên lớp của `ex`, đã hạ về `str` THUẦN — CỬA DUY NHẤT cho mọi đường chẩn đoán.

    Cross-review codex lượt 2 (24-09, `diagnostic-normalization-wiring-unmeasured` còn mở):
    bản vá lượt trước hạ tên lớp ở `_MaVang` và `_NgoaiLeLa` nhưng NHÁNH BÁO LỖI của chính
    cửa `_goi_doi_tra_ve` vẫn đưa `type(loi).__name__` thô vào f-string của `chot`. Cho cả
    họ 6 thành viên của `t187` đi vào nhánh ấy: 3/6 chết bằng `RuntimeError` TRẦN, 1/6 bằng
    `KeyboardInterrupt` TRẦN — ca đỏ vì đường chẩn đoán, không vì thứ nó đo.

    Đó là "vá đúng chỗ được chỉ rồi bỏ sót đường thứ ba". Nên lần này liệt kê bằng `ast`
    MỌI chỗ định dạng một ngoại lệ vừa bắt, gom về MỘT cửa, và `t189` cấm viết thô trở lại.
    `type(ex).__name__` không đi qua `__str__` của NGOẠI LỆ, nhưng có thể là một `str` CON —
    một lớp đặt `__name__` như vậy là đủ để f-string nổ — và việc ĐỌC nó đi qua
    `__getattribute__` của METACLASS, vốn được ném bất cứ gì hoặc trả `None` (lượt 3 · lượt 7).
    `t187` đo cả ba họ. Phạm vi: API của harness test; KHÔNG có chứng cứ một lease YAML hay
    CLI chạm được metaclass Python.
    """
    # BỌC CẢ PHÉP ĐỌC, không chỉ phép hạ. Cross-review codex lượt 3 (24-09): bản trước tính
    # `getattr(type(ex), "__name__", "?")` TRƯỚC khi vào `try` của `_chuoi_thuan` — một metaclass
    # làm hỏng việc đọc `__name__` là đủ để CHÍNH cửa hạ tên lớp ném `RuntimeError`, và lỗi lan
    # ra `_MaVang`, `_NgoaiLeLa`, helper, cửa, `main`. Giá trị mặc định của `getattr` chỉ đỡ
    # `AttributeError`, không đỡ gì khác. Dự phòng là chuỗi thuần KHÔNG đọc thêm gì từ `ex`.
    try:
        ten = getattr(type(ex), "__name__", "?")
    except BaseException:  # noqa: BLE001 — đường chẩn đoán không được làm vỡ phép đo
        return "<tên lớp không đọc được>"
    return _chuoi_thuan(ten, "<tên lớp không đọc được>")


def _bao_loi_ca(ex) -> str:
    """Thông điệp bộ chạy ghi cho một ca đỏ — tách khỏi `main` để ĐO được (lượt 3, F1).

    `AssertionError` (gồm `TinHieuChotCa`) giữ đúng thông điệp của `chot`; ngoại lệ khác nêu
    thêm tên lớp. Cả hai vế đi qua hai cửa an toàn: bộ chạy là đường chẩn đoán của MỌI ca, nó
    không được nổ đúng lúc đang báo một ca đỏ.
    """
    if isinstance(ex, AssertionError):
        return _thong_diep_an_toan(ex)
    return f"{_ten_lop(ex)}: {_thong_diep_an_toan(ex)}"


class _MaVang:
    """`ma` của một ngoại lệ TRẦN: KHÔNG bằng bất kỳ mã thoát nào, và TỰ KHAI lớp khi in.

    Vì sao một LỚP chứ không phải `None`: mọi ca đều viết `chot(ma == RC_X, f"... được
    rc={ma}")`. Với `None` thì ca ĐỎ đúng như mong muốn, nhưng thông điệp chỉ ra `rc=None`
    và người đọc mất đúng thứ cần biết — ngoại lệ nào đã thoát ra. Lớp này giữ cả hai:
    so sánh luôn SAI với mọi mã thoát, mà in ra thì nêu tên lớp và thông điệp.

    `__eq__` luôn `False` là CÓ CHỦ ĐÍCH và đã kiểm: trong tệp này không ca nào chốt bằng
    `ma != X`, nên không có đường nào biến nó thành một ca xanh giả. `t184` khoá cả hai vế.
    """
    __slots__ = ("kieu", "thong_diep")

    def __init__(self, ex):
        # `type(ex).__name__` KHÔNG đi qua `__str__` của ngoại lệ, nhưng VẪN đi qua metaclass —
        # nên tên lớp cũng đi qua một cửa an toàn (`_ten_lop`), không đọc thẳng. Thông điệp đi
        # qua `_thong_diep_an_toan` — xem hàm ấy.
        # TÊN LỚP cũng phải hạ về chuỗi thuần: một metaclass đặt `__name__` thành `str`
        # con là đủ để dòng `chot` nổ ở đúng chỗ nó đang tố cáo. Hai trường, MỘT cửa hạ —
        # để không có trường nào "quên" như thông điệp đã từng quên.
        self.kieu = _ten_lop(ex)
        self.thong_diep = _thong_diep_an_toan(ex)

    def __eq__(self, _other):
        return False

    def __ne__(self, _other):
        return True

    def __hash__(self):
        return id(self)

    def __str__(self):
        return f"KHÔNG-CÓ-MÃ (ngoại lệ TRẦN {self.kieu}: {self.thong_diep})"

    __repr__ = __str__


class _NgoaiLeLa:
    """Thứ `_goi_lop_gh` trả về khi cổng ném một ngoại lệ KHÔNG PHẢI `Chan`.

    ĐÂY LÀ BẢN VÁ THEO LỚP, KHÔNG THEO CA — và đó là điểm chính. Cross-review lượt 3 bắt
    `t182` đỏ bằng `AttributeError` thoát ra TRƯỚC khi `chot` của nó chạy; lượt 3 vá bằng
    một helper riêng cho MỘT ca. Lượt 4 bắt tiếp `t179` mắc y hệt (biến thể `X`) — tức bản
    vá kia ĐÚNG mà HẸP, đúng hình dạng `VA-DUNG-CHO-DUOC-CHI-ROI-BO-SOT-DUONG-THU-BA` mà
    `CLAUDE.md` đã trả giá ở #513.

    Nên lần này không vá ca thứ hai: vá CÁI CỬA. `_goi_lop_gh` là đường DUY NHẤT mà 20+ ca
    gọi vào cổng, nên đóng ở đó là đóng cả loạt — kể cả những ca chưa ai nghĩ tới.

    Hợp đồng KHÔNG đổi với đường cũ: ném `Chan` ⇒ trả chính `Chan` ấy (mọi ca cũ nguyên
    vẹn); không ném gì ⇒ trả `None`. CHỈ hình dạng thứ ba — ngoại lệ trần — đổi từ "vỡ ra
    ngoài ca" thành "ca ĐỎ bằng chot của CHÍNH NÓ".

    Bắt `Exception` chứ KHÔNG bắt `BaseException`: `KeyboardInterrupt` và `SystemExit` phải
    đi thẳng ra, một bộ test nuốt chúng là một bộ test không dừng được.
    """
    __slots__ = ("ngoai_le", "kieu", "ma")

    def __init__(self, ex):
        # `kieu` LẤY TỪ `_MaVang`, KHÔNG đọc `type(ex).__name__` lần nữa. Cross-review codex
        # 24-09 (`diagnostic-normalization-wiring-unmeasured`) đo: bản cũ giữ tên lớp THÔ ở
        # đây, nên với `__name__` là `str` con thì `_MaVang` in được 6/6 mà lớp này chỉ 2/6 —
        # `__str__` bên dưới nổ đúng ở f-string. Hai lớp, MỘT cửa hạ tên lớp.
        self.ngoai_le, self.ma = ex, _MaVang(ex)
        self.kieu = self.ma.kieu

    def __str__(self):
        # Dùng BẢN CHỤP an toàn, KHÔNG định dạng lại `self.ngoai_le` — định dạng lần hai là
        # đường thứ hai để `__str__` hỏng làm vỡ ca. Xem `_thong_diep_an_toan`.
        return f"<ngoại lệ TRẦN {self.kieu}: {self.ma.thong_diep}>"

    __repr__ = __str__


def _goi_lop_gh(gh: GhGia, ten: str, *args, env_them=None, bo_qua=(), truoc_khi_chay=None):
    import os
    from unittest import mock
    mod = _nap_cong()
    mod.GOI_GH = gh
    for ten_bo_qua in bo_qua:
        setattr(mod, ten_bo_qua, lambda *a: None)
    # `truoc_khi_chay(mod)` — móc DUY NHẤT cho fixture thấy module ĐANG chạy, trước khi cổng
    # chạy. Có vì một lý do đo được: danh tính lớp `Chan` là THEO TỪNG LẦN NẠP, nên không có
    # móc này thì không ca nào dựng nổi một `Chan` CỦA CHÍNH lần nạp ấy, và hợp đồng "ném
    # `Chan` nào thì trả về CHÍNH đối tượng ấy" là không đo được. Cross-review lượt 6:
    # `P_identity` (trả một `Chan` MỚI cùng lớp, cùng `.ma`) PASS — vì ca chỉ chốt LỚP.
    if truoc_khi_chay is not None:
        truoc_khi_chay(mod)
    # HERMETIC (packet #396, đóng N9). `clear=True` TRÔNG NHƯ cách ly nhưng nó cách ly
    # bằng chính bản sao đã mang `GITHUB_ACTOR` của runner. Đo 29-08-2026 trên `ef4098d4`:
    # `env -u GITHUB_ACTOR` ⇒ 123/124, `GITHUB_ACTOR=notebyme88` ⇒ 94/124 — chênh 29 ca,
    # và `t124` còn báo SAI TẬP ĐÍCH của bẫy đột biến. Verdict của bộ test không được phụ
    # thuộc vào việc AI BẤM NÚT MERGE.
    #
    # Xoá ĐÚNG một biến, KHÔNG dùng `os.environ.pop` toàn cục: cái đó quá thô và sẽ che
    # mất chính ca cần chứng minh hành vi khi actor VẮNG. Ca nào cần actor thì đặt tường
    # minh qua `env_them` — `t02d` làm đúng như vậy.
    moi = dict(os.environ)
    moi.pop("GITHUB_ACTOR", None)
    moi.update(env_them or {})
    try:
        with mock.patch.dict(os.environ, moi, clear=True):
            getattr(mod, ten)(*args)
    except mod.Chan as ex:
        return ex, mod
    except Exception as ex:  # noqa: BLE001 — xem `_NgoaiLeLa`: đổi VỠ TRẦN thành ca ĐỎ
        return _NgoaiLeLa(ex), mod
    return None, mod


class _DaTraVe:
    """Nhãn "cổng TRẢ VỀ bình thường" — KHÔNG phải một mã thoát.

    Vì sao cần một nhãn riêng thay vì dùng `0`: `RC_OK` CŨNG bằng `0`, nên `ma == 0` không
    phân biệt được "không ném" với "ném `Chan(RC_OK)`". Hai trạng thái khác nhau mà cùng
    một giá trị là đúng hình dạng đã làm `_MaVang` phải ra đời ở lượt 4.
    """
    __slots__ = ()

    def __str__(self):
        return "ĐÃ-TRẢ-VỀ (cổng không ném)"

    __repr__ = __str__


DA_TRA_VE = _DaTraVe()


def _goi_dem_lop_gh(gh: GhGia, ten: str, lease, ket_qua_mong_doi, so_goi_mong_doi,
                    nhan: str, *, env_them=None, **k):
    """CỬA DUY NHẤT cho mọi ca muốn chốt SỐ LỜI GỌI GitHub. Chốt KẾT QUẢ trước, ĐẾM sau.

    LỚP NÀY ĐÃ TRẢ GIÁ — cross-review lượt 6 (trục LỚP) bắt được, và nó bắt bằng PHÉP ĐO:

        Đột biến `R_probe`: ném `ValueError` ngay đầu `_do_dau_da_dang`, CHỈ với đúng năm
        đầu vào của vế `lease_id` sai kiểu (`"lease_id" in lease and not isinstance(..., str)`).
        Chạy toàn suite trên head `94d3cd9` ⇒ **177/177, SỐNG SÓT.**

    Vì sao nó sống: vế ấy bỏ giá trị trả về (`_ex`) rồi chỉ chốt `len(gh.calls) == 0`. Mà
    **`0 lời gọi vì tiền kiểm chặn` và `0 lời gọi vì ngoại lệ bay ra trước mạng` là HAI
    trạng thái khác nhau cho CÙNG một con số.** Số đếm không phân biệt được; nó chỉ biết
    mạng chưa bị chạm, không biết VÌ SAO.

    Cùng họ với `_MaVang` (lượt 4) và với `t179`/`t182`: một ca xanh vì thứ nó đo chết sớm.
    Khác chỗ đắt: ở đây ca KHÔNG đỏ, nên không ai thấy gì cả.

    CHỮA BẰNG KIẾN TRÚC, không bằng một chốt thêm ở đúng chỗ reviewer chỉ: cửa này chốt CẢ
    HAI vế, nên không còn cách nào viết một chốt số lời gọi mà quên vế kết quả. `t185` đo
    chính cửa này; `t186` cấm mọi chốt số lời gọi nằm NGOÀI cửa — không có `t186` thì ca
    sau chỉ việc viết lại `chot(len(gh.calls) == 0, ...)` và lỗ mở lại trong im lặng.

    `ket_qua_mong_doi`: một mã `RC_*`, hoặc `DA_TRA_VE` khi cổng phải trả về mà không ném.
    """
    ex, mod = _goi_lop_gh(gh, ten, lease, env_them=env_them, **k)
    thuc = DA_TRA_VE if ex is None else ex.ma
    _chot_cua_dem("ket_qua", thuc == ket_qua_mong_doi,
         f"{nhan}: cổng `{ten}` phải kết thúc bằng {ket_qua_mong_doi}, được {thuc}. "
         f"Chốt SỐ LỜI GỌI phía sau chỉ có nghĩa khi cổng kết thúc ĐÚNG CÁCH — một phép dò "
         f"chết sớm cũng cho 0 lời gọi, và số đếm KHÔNG phân biệt được hai chuyện đó.")
    _chot_cua_dem("dem", len(gh.calls) == so_goi_mong_doi,
         f"{nhan}: phải có đúng {so_goi_mong_doi} lời gọi GitHub, có {len(gh.calls)}.")
    return mod


def _goi_doi_tra_ve(ve: str, gh, ten: str, *args, kem_mod: bool = False, **k):
    """Gọi `_goi_lop_gh` và ĐÒI nó TRẢ VỀ. Helper NÉM ⇒ ca đỏ bằng `chot` của CHÍNH nó.

    Mệnh đề đang đo là *"helper LUÔN trả về"*. Viết lời gọi trần thì đúng lúc mệnh đề ấy SAI,
    ngoại lệ bay qua đầu `chot` và ca đỏ bằng traceback của runner — tức ca đỏ ĐÚNG nhưng
    KHÔNG ĐO GÌ, và thông điệp không nêu được vế nào hỏng. Cross-review lượt 6 bắt đúng chỗ
    này ở vế (b) của `t184`.

    Cửa này là cách duy nhất trong tệp để đo một vế "phải trả về" — một vế, một cửa, nên
    không còn vế nào có thể quên bọc.

    `kem_mod=True` trả thêm module đang chạy. Có vì một lý do ĐO ĐƯỢC: cross-review codex
    24-09 (`return-contract-unwrapped-arms`) bắt vế (a) và (c) của `t184` vẫn gọi TRẦN —
    vế (a) cần module để chốt DANH TÍNH LỚP `Chan` (danh tính ấy theo từng lần nạp), mà
    bản cũ của cửa vứt module đi, nên vế ấy không qua cửa được. Lời khai "cách duy nhất"
    ngay trên khi ấy SAI; `t188` nay khoá nó bằng `ast`.
    """
    try:
        ex, _mod = _goi_lop_gh(gh, ten, *args, **k)
    except BaseException as loi:  # noqa: BLE001 — ĐO "luôn trả về", nên phải bắt trọn
        chot(False,
             f"{ve} helper NÉM `{_ten_lop(loi)}` thay vì TRẢ VỀ. Hợp đồng của "
             f"`_goi_lop_gh` là luôn trả về; ném nghĩa là mọi ca gọi nó sẽ đỏ bằng traceback "
             f"của runner chứ không bằng `chot` của chính ca.")
    return (ex, _mod) if kem_mod else ex


def _do_kiem_github_dem(lease, co_dau: bool, ket_qua_mong_doi, so_goi_mong_doi, nhan: str,
                        **k):
    """Như `_do_kiem_github` nhưng đi qua cửa đếm — dùng cho ca CÓ chốt số lời gọi."""
    gh, _ = _dung_gh_579(lease, co_dau)
    _goi_dem_lop_gh(gh, "kiem_github", lease, ket_qua_mong_doi, so_goi_mong_doi, nhan,
                    env_them=ENV_GITHUB, **k)


def _buoc_workflow(ten: str) -> dict:
    import yaml
    tep = WORKFLOW_DANG
    bang(tep.is_file(), f"không thấy {tep}")
    d = yaml.safe_load(tep.read_text(encoding="utf-8"))
    ds = [x for x in d["jobs"]["dang"]["steps"] if x.get("name") == ten]
    bang(len(ds) == 1, f"chờ ĐÚNG một bước {ten!r}, thấy {len(ds)}")
    return ds[0]


def _ly_do_bo_qua_workflow(tep: Path, ten_job: str, nen=None, job=None) -> str:
    import os, yaml
    job = job or yaml.safe_load(tep.read_text(encoding="utf-8"))["jobs"][ten_job]
    raw, nhan = job.get("runs-on"), []
    m = re.fullmatch(r"\$\{\{\s*matrix\.([A-Za-z_][\w-]*)\s*\}\}", raw) if isinstance(raw, str) else None
    nhan = (((job.get("strategy") or {}).get("matrix") or {}).get(m.group(1))
            if m else raw if isinstance(raw, list) else [raw])
    if (nen or os.name) == "nt" and nhan and all(
            isinstance(x, str) and x.lower().startswith("ubuntu-") for x in nhan):
        return (f"{tep.name}:{ten_job} chỉ chạy Ubuntu; runs-on đã đọc được: "
                f"{raw!r}, phân giải thành {nhan!r}")
    return ""


# --- các ca ---------------------------------------------------------------------


@ca
def t01_lease_hop_le_thi_QUA():
    """Cổng phải xanh được, không thì người ta gỡ nó ra."""
    with San() as s:
        rc, o, e = chay("check", viet(s, lease_mau()))
        bang(rc == RC_OK, f"chặn oan lease hợp lệ: rc={rc} {e}")


@ca
def t02_granted_by_la_ten_provider_bi_CHAN():
    """Chốt CỐT LÕI, cùng luật với `packet_loop.py record-lease`.

    Nếu chỗ này lỏng, một agent tự soạn lease cho mình rồi push là có comment
    mang danh nghĩa kho — đúng thứ doctrine 'không tự cấp lease' cấm.
    """
    with San() as s:
        for ten in ("codex", "claude", "Claude", "  CODEX  "):
            rc, _, e = chay("check", viet(s, lease_mau(granted_by=ten), ten="x.yaml"))
            bang(rc == RC_TU_CAP, f"granted_by={ten!r} lọt: rc={rc} {e}")


@ca
def t02b_ten_KHONG_CO_THAM_QUYEN_bi_CHAN():
    """`lease-authority-spoof` — P1 của cross-review lượt 4 (codex, 14-08-2026).

    Bản trước chỉ từ chối ĐÚNG hai chuỗi `claude`/`codex`, nên mọi biến thể lọt sạch.
    Nguyên văn kết luận của reviewer: *"distinguishes spelling, not authority"*.
    Bốn chuỗi dưới đây là ca reviewer đã chạy được và thu `rc=0` trên bản cũ.

    Đắng: prompt do chính phiên soạn cho reviewer LIỆT KÊ `codex-dispatcher` làm hướng
    tấn công số 1, rồi cổng vẫn thua đúng ca đó. Nghĩ ra phép thử mà không chạy thì
    phép thử ấy không tồn tại — ca này tồn tại để lần sau không cần nghĩ lại.
    """
    with San() as s:
        for ten in ("codex-dispatcher", "ai-codex-bot", "cödex", "claude-code",
                    "dispatcher", "ducthangho2"):
            rc, _, e = chay("check", viet(s, lease_mau(granted_by=ten), ten="a.yaml"))
            bang(rc == RC_TU_CAP, f"granted_by={ten!r} LỌT: rc={rc} {e}")
            bang("danh sách người có thẩm quyền" in e,
                 f"{ten!r} bị chặn nhưng KHÔNG phải bởi danh sách cho phép: {e.strip()!r}")


@ca
def t02c_nguoi_CO_tham_quyen_thi_QUA_moi_cach_viet():
    """Chiều DƯƠNG. Một danh sách cho phép chặn được tất cả thì cũng vô dụng."""
    with San() as s:
        for ten in ("ducthangho", "Ducthangho", "  DUCTHANGHO  "):
            rc, _, e = chay("check", viet(s, lease_mau(granted_by=ten), ten="b.yaml"))
            bang(rc == RC_OK, f"chặn oan người có thẩm quyền {ten!r}: rc={rc} {e}")


@ca
def t02d_GITHUB_ACTOR_khong_co_tham_quyen_bi_CHAN():
    """Neo vào danh tính GitHub XÁC THỰC, không phải chữ trong tệp YAML.

    Kẻ soạn lease đặt được `granted_by`, nhưng KHÔNG đặt được `GITHUB_ACTOR` — biến
    đó do GitHub đặt cho runner. Lệch nhau thì tin cái GitHub xác thực.
    """
    import os
    with San() as s:
        p = viet(s, lease_mau())          # granted_by hợp lệ
        moi = dict(os.environ, GITHUB_ACTOR="ke-la-mat")
        q = subprocess.run([sys.executable, str(SCRIPT), "check", str(p)],
                           capture_output=True, text=True, env=moi)
        bang(q.returncode == RC_TU_CAP,
             f"GITHUB_ACTOR lạ mà vẫn đăng được: rc={q.returncode} {q.stderr}")
        bang("GITHUB_ACTOR" in q.stderr, f"chặn nhưng nói sai lỗi: {q.stderr.strip()!r}")
        # chiều dương: actor có thẩm quyền thì qua
        moi["GITHUB_ACTOR"] = "ducthangho"
        q2 = subprocess.run([sys.executable, str(SCRIPT), "check", str(p)],
                            capture_output=True, text=True, env=moi)
        bang(q2.returncode == RC_OK, f"chặn oan actor hợp lệ: rc={q2.returncode} {q2.stderr}")


@ca
def t03_lease_da_het_han_bi_CHAN():
    with San() as s:
        rc, _, e = chay("check", viet(s, lease_mau(lease_expires_at_utc=khi_truoc())))
        bang(rc == RC_NOI_DUNG, f"đăng được lease đã chết: rc={rc} {e}")


@ca
def t04_han_thieu_mui_gio_bi_CHAN():
    """"18:30" không nói múi là hai mốc cách nhau tới 26 giờ — chặn, đừng đoán."""
    with San() as s:
        rc, _, e = chay("check", viet(s, lease_mau(lease_expires_at_utc="2026-12-01T18:30:00")))
        bang(rc == RC_NOI_DUNG, f"nhận hạn không múi giờ: rc={rc} {e}")


@ca
def t05_thieu_truong_bat_buoc_bi_CHAN():
    with San() as s:
        for thieu in ("packet_issue", "lease_id", "granted_by",
                      "lease_expires_at_utc", "reviewed_sha_required"):
            d = lease_mau()
            d.pop(thieu)
            rc, _, e = chay("check", viet(s, d, ten=f"{thieu}.yaml"))
            bang(rc == RC_NOI_DUNG, f"thiếu {thieu!r} mà vẫn qua: rc={rc} {e}")


@ca
def t06_sha_khong_dung_dang_bi_CHAN():
    """SHA ngắn/lệch dạng là mỏ neo giả — reviewer sẽ đọc nhầm head."""
    with San() as s:
        for xau in ("cf39109c", "z" * 40, SHA40 + "0", ""):
            rc, _, e = chay("check", viet(s, lease_mau(reviewed_sha_required=xau), ten="s.yaml"))
            bang(rc == RC_NOI_DUNG, f"sha {xau!r} lọt: rc={rc} {e}")


@ca
def t07_packet_issue_khong_phai_so_bi_CHAN():
    with San() as s:
        rc, _, e = chay("check", viet(s, lease_mau(packet_issue="55; rm -rf /")))
        bang(rc == RC_NOI_DUNG, f"packet_issue rác lọt: rc={rc} {e}")


@ca
def t09_body_in_ra_nguyen_van_YAML_de_doi_chieu():
    """Thân comment phải chứa lại chính khối YAML — người đọc đối chiếu được."""
    with San() as s:
        rc, o, e = chay("body", viet(s, lease_mau()))
        bang(rc == RC_OK, f"dựng thân hỏng: rc={rc} {e}")
        for phai_co in ("wp55-r2-review-3-codex-20260814", SHA40, "```"):
            bang(phai_co in o, f"thân comment thiếu {phai_co!r}")


@ca
def t10_body_TU_CHOI_lease_khong_hop_le():
    """`body` không được dựng thân cho một lease mà `check` đã chặn.

    Hai lệnh hai đường mà chỉ một đường có chốt là chốt đi vòng được.
    """
    with San() as s:
        rc, _, e = chay("body", viet(s, lease_mau(granted_by="codex")))
        bang(rc == RC_TU_CAP, f"`body` bỏ qua chốt: rc={rc} {e}")


@ca
def t12_tep_khong_ton_tai_bao_ro():
    rc, _, e = chay("check", "/khong/co/tep/nay.yaml")
    bang(rc == RC_THAM_SO, f"tệp thiếu phải là {RC_THAM_SO}: rc={rc}")


@ca
def t13_yaml_hong_khong_duoc_no_traceback():
    with San() as s:
        p = s / "hong.yaml"
        p.write_text("a: [1, 2\n  b: :::\n", encoding="utf-8")
        rc, _, e = chay("check", p)
        bang(rc == RC_NOI_DUNG, f"YAML hỏng phải là {RC_NOI_DUNG}: rc={rc}")
        bang("Traceback" not in e, "lộ traceback thô ra ngoài")


@ca
def t14_neo_prompt_DUNG_thi_QUA():
    """Chiều DƯƠNG. Chốt chỉ biết chặn mà không biết cho qua thì cũng hỏng."""
    with San() as s:
        duong, sha = dat_prompt(s, b"Ban la phien REVIEWER...\n")
        p = viet(s, lease_mau(prompt_path=duong, prompt_sha256_required=sha))
        rc, o, e = chay("check", p, "--root", s)
        bang(rc == RC_OK, f"chặn oan lease neo prompt đúng: rc={rc} {e}")
        # Đòi in ra ĐÚNG cái băm vừa xác minh, không chỉ chữ "khớp băm": một dòng
        # xác nhận in được cả khi chốt đã bị gỡ thì nó là trang trí, không phải
        # bằng chứng. Có ca này thì gỡ chốt ⇒ ca này đỏ.
        bang("khớp băm" in o and sha[:12] in o,
             f"không nêu băm đã xác minh (chờ {sha[:12]}): {o!r}")


@ca
def t15_bam_LECH_thi_CHAN():
    """ĐÂY LÀ BUG GỐC, dựng lại nguyên trạng.

    Lease #3 của wp55 khai `46a833cc…` trong khi không văn bản nào băm ra thế.
    Trước bản vá này cổng vẫn xanh, và hỏng im lặng suốt hai ngày.
    """
    with San() as s:
        duong, _ = dat_prompt(s, b"noi dung that\n")
        sai = "46a833ccfefba0b659a16183daf8b4f4893a5ef0eeb4e7fdf3cd315aad550dfc"
        p = viet(s, lease_mau(prompt_path=duong, prompt_sha256_required=sai))
        rc, _, e = chay("check", p, "--root", s)
        bang(rc == RC_NEO, f"băm lệch mà vẫn đăng được: rc={rc} {e}")
        # Đòi thông điệp nói CẢ HAI con số. Một cổng chỉ hô "lệch" thì người sửa
        # vẫn phải tự đi băm lại — đúng chỗ hai ngày vừa rồi mất thời gian.
        bang(sai in e and "thực tế" in e, f"thông điệp không nêu đủ hai băm: {e!r}")


@ca
def t16_tep_prompt_KHONG_CO_thi_CHAN():
    with San() as s:
        p = viet(s, lease_mau(prompt_path="ops/prompts/khong-co.md",
                              prompt_sha256_required="0" * 64))
        rc, _, e = chay("check", p, "--root", s)
        bang(rc == RC_NEO, f"neo vào tệp không tồn tại mà qua: rc={rc} {e}")


@ca
def t17_neo_NUA_VOI_thi_CHAN_CA_HAI_CHIEU():
    """Băm không địa chỉ = không kiểm được. Địa chỉ không băm = đổi lúc nào không hay.

    Neo THÔNG ĐIỆP, và lý do đáng ghi: bỏ chốt này đi thì `prompt_path` rỗng biến
    thành `PurePosixPath("")` = `.`, tức trỏ vào chính thư mục gốc kho, và bị chặn
    ở `is_file()` với câu "không có tệp". Vẫn RC_NEO, nên ca chỉ đòi mã thoát sẽ
    XANH trong khi chốt đã bị gỡ — mà thông điệp thì chỉ sai chỗ đúng kiểu đã làm
    mất hai ngày: nói tệp thiếu, trong khi lỗi thật là lease không khai địa chỉ.
    """
    with San() as s:
        duong, sha = dat_prompt(s, b"x\n")
        rc, _, e = chay("check", viet(s, lease_mau(prompt_sha256_required=sha), ten="a.yaml"),
                        "--root", s)
        bang(rc == RC_NEO, f"băm không có prompt_path mà qua: rc={rc} {e}")
        bang("thiếu `prompt_path`" in e,
             f"chặn nhưng nói sai lỗi (chờ 'thiếu prompt_path'): {e.strip()!r}")
        rc, _, e = chay("check", viet(s, lease_mau(prompt_path=duong), ten="b.yaml"),
                        "--root", s)
        bang(rc == RC_NEO, f"prompt_path không có băm mà qua: rc={rc} {e}")
        bang("thiếu `prompt_sha256_required`" in e,
             f"chặn nhưng nói sai lỗi (chờ 'thiếu prompt_sha256_required'): {e.strip()!r}")


@ca
def t18_prompt_path_VUOT_RA_NGOAI_kho_thi_CHAN():
    """`prompt_path` là dữ liệu YAML mà thành một lượt đọc đĩa — phải chặn đường ra.

    Ca này neo THÔNG ĐIỆP chứ không chỉ mã thoát, và đó là chủ đích. Có HAI lớp
    chặn (lọc dạng đường dẫn trước khi đụng đĩa, rồi `relative_to` sau `resolve`),
    và đã đo: bỏ lớp nào thì lớp kia vẫn trả đúng RC_NEO. Nếu chỉ đòi mã thoát thì
    đột biến gỡ lớp trên SỐNG SÓT, và bộ test nói dối rằng nó có đo lớp ấy. Neo
    thông điệp thì mỗi lớp có một ca riêng: t18 giữ lớp lọc, t19 giữ `relative_to`.
    """
    with San() as s:
        ngoai = s.parent / f"ngoai_{s.name}.md"
        ngoai.write_bytes(b"tep ngoai kho\n")
        import hashlib
        sha = hashlib.sha256(b"tep ngoai kho\n").hexdigest()
        try:
            for xau in (f"../{ngoai.name}", str(ngoai), "..\\..\\x.md",
                        "ops/../../" + ngoai.name):
                p = viet(s, lease_mau(prompt_path=xau, prompt_sha256_required=sha),
                         ten="v.yaml")
                rc, _, e = chay("check", p, "--root", s)
                bang(rc == RC_NEO, f"prompt_path {xau!r} thoát ra ngoài kho: rc={rc} {e}")
                bang("đường dẫn tương đối" in e,
                     f"{xau!r} bị chặn nhưng KHÔNG phải bởi lớp lọc dạng đường dẫn "
                     f"(thông điệp: {e.strip()!r})")
        finally:
            ngoai.unlink(missing_ok=True)


@ca
def t19_symlink_tro_RA_NGOAI_kho_thi_CHAN():
    """`..` chỉ là một trong hai đường ra. Symlink là đường kia, và nó im hơn."""
    with San() as s:
        ngoai = s.parent / f"sym_{s.name}.md"
        ngoai.write_bytes(b"tep ngoai kho\n")
        import hashlib
        sha = hashlib.sha256(b"tep ngoai kho\n").hexdigest()
        lk = s / "ops" / "prompts" / "p.md"
        lk.parent.mkdir(parents=True, exist_ok=True)
        try:
            lk.symlink_to(ngoai)
        except (OSError, NotImplementedError):
            return   # nền không cho tạo symlink (Windows thiếu quyền) — bỏ qua
        try:
            p = viet(s, lease_mau(prompt_path="ops/prompts/p.md",
                                  prompt_sha256_required=sha))
            rc, _, e = chay("check", p, "--root", s)
            bang(rc == RC_NEO, f"symlink ra ngoài kho vẫn qua: rc={rc} {e}")
            # Symlink là ca DUY NHẤT mà lớp lọc dạng đường dẫn không thấy được:
            # `ops/prompts/p.md` sạch về mặt chuỗi, chỉ `resolve()` mới lộ.
            bang("ngoài kho" in e,
                 f"chặn nhưng không phải bởi `relative_to` sau resolve: {e.strip()!r}")
        finally:
            ngoai.unlink(missing_ok=True)


@ca
def t20_sha256_SAI_DANG_thi_CHAN():
    with San() as s:
        duong, sha = dat_prompt(s, b"x\n")
        for xau in (sha[:32], sha.upper(), sha + "0", "z" * 64):
            p = viet(s, lease_mau(prompt_path=duong, prompt_sha256_required=xau),
                     ten="d.yaml")
            rc, _, e = chay("check", p, "--root", s)
            bang(rc == RC_NEO, f"sha256 {xau!r} lọt: rc={rc} {e}")
            # Neo THÔNG ĐIỆP: băm sai dạng thì cũng khác băm thật, nên chốt so băm
            # bên dưới vẫn chặn — chỉ đòi mã thoát là ca này không đo gì cả (đã đo:
            # gỡ chốt dạng đi thì suite vẫn xanh). Nói "sai dạng" khác hẳn nói
            # "băm lệch": cái sau đẩy người sửa đi băm lại một tệp không có lỗi.
            bang("64 ký tự hex" in e,
                 f"sha256 {xau!r} bị chặn nhầm chỗ — chờ lỗi SAI DẠNG, được: {e.strip()!r}")


@ca
def t21_bam_theo_BYTE_chu_khong_theo_van_ban():
    """CRLF và LF là hai tệp khác nhau, và phải ra hai băm khác nhau.

    `read_text` chuẩn hoá xuống dòng nên cùng một tệp cho hai kết quả tuỳ nền —
    một cổng như thế xanh ở Linux, đỏ ở Windows, không ai hiểu vì sao.
    """
    with San() as s:
        import hashlib
        lf = b"dong mot\ndong hai\n"
        duong, sha_lf = dat_prompt(s, lf)
        (s / duong).write_bytes(lf.replace(b"\n", b"\r\n"))   # cùng đường dẫn, đổi EOL
        p = viet(s, lease_mau(prompt_path=duong, prompt_sha256_required=sha_lf))
        rc, _, e = chay("check", p, "--root", s)
        bang(rc == RC_NEO, f"CRLF/LF ra cùng băm — đang đọc văn bản, không đọc byte: rc={rc}")
        # chiều dương: khai đúng băm bản CRLF thì phải qua
        sha_crlf = hashlib.sha256(lf.replace(b"\n", b"\r\n")).hexdigest()
        p2 = viet(s, lease_mau(prompt_path=duong, prompt_sha256_required=sha_crlf),
                  ten="crlf.yaml")
        rc2, _, e2 = chay("check", p2, "--root", s)
        bang(rc2 == RC_OK, f"chặn oan bản CRLF khai đúng băm: rc={rc2} {e2}")


@ca
def t22_body_cung_bi_CHAN_khi_neo_hong():
    """Hai lệnh hai đường mà chỉ một đường có chốt là chốt đi vòng được."""
    with San() as s:
        duong, _ = dat_prompt(s, b"that\n")
        p = viet(s, lease_mau(prompt_path=duong, prompt_sha256_required="0" * 64))
        rc, o, e = chay("body", p, "--root", s)
        bang(rc == RC_NEO, f"`body` bỏ qua chốt neo prompt: rc={rc} {e}")
        bang(not o.strip(), f"`body` vẫn in thân comment cho lease hỏng: {o[:120]!r}")


@ca
def t23_MOI_lease_THAT_trong_kho_phai_QUA():
    """Chốt phải xanh trên chính các tệp lease đang dùng, không chỉ trên đồ giả.

    Quét MỌI lease trong `ops/leases/`, không chỉ định danh một tệp. Bản đầu ca này
    ghi cứng tên lease #3; đến lease #4 thì nó vẫn xanh trong khi lease mới có thể
    hỏng — thêm lease là thêm chỗ mù, mà chỗ mù nằm đúng ở tệp mới nhất, tức tệp
    khả nghi nhất. Ca ghi cứng một tên chỉ canh được quá khứ.

    Bỏ ca này thì bộ test có thể xanh trong khi lease thật vẫn hỏng — đúng khoảng
    cách giữa "code chạy" và "việc chạy".
    """
    import hashlib
    import yaml
    goc = HERE.parent
    thu_muc = HERE / "leases"
    if not thu_muc.is_dir():
        return
    ds = sorted(p for p in thu_muc.iterdir() if p.suffix in (".yaml", ".yml"))
    # KHÔNG cho phép "không có lease nào" âm thầm thành ĐẠT: thư mục rỗng và thư mục
    # toàn lease lành cho cùng một màu xanh, mà ý nghĩa thì ngược nhau.
    bang(ds, f"không thấy lease nào trong {thu_muc} — ca này sẽ xanh mà không đo gì")
    da_kiem = 0
    for p in ds:
        d = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        duong, sha = d.get("prompt_path"), d.get("prompt_sha256_required")
        if not duong and not sha:
            continue          # lease không neo prompt — hợp lệ, bỏ qua
        bang(duong and sha, f"{p.name}: neo prompt NỬA VỜI (path={duong!r} sha={sha!r})")
        f = goc / duong
        bang(f.is_file(), f"{p.name}: trỏ vào tệp không có: {duong}")
        thuc = hashlib.sha256(f.read_bytes()).hexdigest()
        bang(thuc == sha, f"{p.name}: LỆCH BĂM — khai {sha}, tệp {duong!r} thực {thuc}")
        da_kiem += 1
    bang(da_kiem, "không lease nào neo prompt — ca này không đo được gì")


@ca
def t24_workflow_KHONG_duoc_nhet_dau_skip_ci_vao_commit():
    """Không workflow nào được ghi dấu skip-ci vào thông điệp commit.

    Đã trả giá hai lần trong CÙNG một ngày (14-08-2026), theo hai đường khác nhau:

    1. Bước ghi ngược của `ops-publish-lease.yml` commit kèm `[skip ci]` để khỏi tự
       kích hoạt lại. Dấu ấy sống trong LỊCH SỬ, nên khi commit ghi ngược thành HEAD
       của một PR thì nó tắt gate của PR đó: PR #100 có **0 check run** mà vẫn hiện
       `mergeable_state: clean`. Cổng không nói dối — nó vắng mặt, và trên giao diện
       hai thứ đó nhìn giống hệt nhau.
    2. Một merge commit TRÍCH DẪN `[skip ci]` để giải thích lỗi số 1 đã tắt gate của
       chính master. GitHub khớp CHUỖI trên toàn thông điệp, không đọc Markdown, nên
       dấu nháy ngược không phải hàng rào — cùng bài học với `doctrine-scan`.

    Ca này canh đường (1): quét mọi workflow, cấm dấu skip-ci đi kèm `git commit`.
    Đường (2) là kỷ luật viết commit, máy không canh được ở đây — ghi trong CLAUDE.md.
    """
    # HERE là `ops/`, nên gốc kho là HERE.parent. Bản đầu viết `HERE.parent.parent`
    # ⇒ trỏ RA NGOÀI gốc kho, thư mục không có, hàm `return` sớm và ca XANH RỖNG —
    # đúng bệnh mà chính nó sinh ra để chặn. Chỉ lộ vì đã đột biến thử; suite vẫn báo
    # 24/24 trong khi ca này không đo gì. "Ca có mặt" khác "ca có đo".
    goc = HERE.parent / ".github" / "workflows"
    if not goc.is_dir():
        # Chỉ tha khi đây rõ ràng là BẢN SAO rời (bộ đột biến chép mỗi `ops/`).
        # Trong kho thật mà thiếu thư mục workflow thì phải ĐỎ, không được lặng lẽ qua.
        bang(not (HERE.parent / ".git").exists(),
             f"kho thật mà không thấy {goc} — ca này sẽ xanh rỗng")
        return
    ds = sorted(p for p in goc.iterdir() if p.suffix in (".yml", ".yaml"))
    bang(ds, f"không thấy workflow nào trong {goc} — ca này sẽ xanh mà không đo gì")
    # Chỉ những dạng GitHub THẬT SỰ hiểu. Đừng nới thêm biến thể tưởng tượng: bảng
    # rộng quá thì ca này bắt oan một chú thích bình thường rồi bị gỡ.
    DAU = ("[skip ci]", "[ci skip]", "[no ci]", "[skip actions]", "[actions skip]")
    for p in ds:
        noi_dung = p.read_text(encoding="utf-8")
        for so, dong in enumerate(noi_dung.splitlines(), 1):
            # Chỉ soi dòng thực sự tạo commit — chú thích GIẢI THÍCH về dấu này là
            # hợp lệ và cần thiết, cấm luôn thì tài liệu không viết được.
            if "git commit" not in dong:
                continue
            for d in DAU:
                bang(d not in dong,
                     f"{p.name}:{so} nhét {d!r} vào thông điệp commit — dấu đó ở lại "
                     f"trong lịch sử và sẽ tắt gate của PR nào có commit này làm HEAD")


_GOI_CONG_LEASE_TRONG_WORKFLOW = re.compile(
    r"(?:^|\s)(?:python3?|py|bash|sh|exec)\s+"
    r"(\S*(?:lease_publish(?:_test)?\.py|chay_lease_publish_test\.sh))")
_RUN_INLINE = re.compile(r"^\s*(?:-\s*)?run\s*:\s*")


def _cat_chu_thich_run_inline(dong: str) -> str:
    """Cắt chú thích chắc chắn của một dòng YAML ``run:`` dạng inline.

    Shell chỉ mở chú thích ở ``#`` không được quote/escape và đứng đầu lệnh hoặc
    sau khoảng trắng. Ta theo dõi nháy đơn, nháy kép và dấu chéo ngược trên đúng
    dòng đó; ``#`` trong ``"a#b"``, ``'a#b'``, ``a\\#b`` hay ngay sau ``}}`` không
    bị cắt.

    Giới hạn có chủ ý: scalar YAML được quote, block scalar (``|``/``>``), quote
    nhiều dòng và heredoc không được phân tích. Các dạng ấy được giữ nguyên để
    t25 có thể báo oan (fail-closed), thay vì cắt khi chưa biết trạng thái quote và
    làm mất một lời gọi thật (fail-open).
    """
    moc = _RUN_INLINE.match(dong)
    if not moc:
        return dong
    lenh = dong[moc.end():]
    if not lenh or lenh[0] in "|'\">":
        return dong

    nhay = None
    thoat = False
    for i, ky_tu in enumerate(lenh):
        if thoat:
            thoat = False
            continue
        if nhay == "'":
            if ky_tu == "'":
                nhay = None
            continue
        if ky_tu == "\\":
            thoat = True
            continue
        if nhay == '"':
            if ky_tu == '"':
                nhay = None
            continue
        if ky_tu in "'\"":
            nhay = ky_tu
            continue
        if ky_tu == "#" and (i == 0 or lenh[i - 1].isspace()):
            return dong[:moc.end() + i].rstrip()
    return dong


def _cac_loi_goi_cong_lease(noi_dung: str) -> list[tuple[int, str]]:
    """Trả ``(số dòng, đối số)`` từ đúng đường quét mà t25 sử dụng."""
    ket_qua = []
    for so, dong in enumerate(noi_dung.splitlines(), 1):
        if dong.lstrip().startswith("#"):
            continue
        dong = _cat_chu_thich_run_inline(dong)
        ket_qua.extend((so, duong)
                       for duong in _GOI_CONG_LEASE_TRONG_WORKFLOW.findall(dong))
    return ket_qua


@ca
def t25_workflow_dang_lease_phai_chay_bo_kiem_NEO_khong_lay_tu_head():
    """Workflow đăng lease KHÔNG được chạy `lease_publish*.py` lấy từ head được đẩy.

    Finding P1 của cross-review trên PR #104 (14-08-2026): bản trước chạy
    `python3 ops/lease_publish.py`, tức bộ kiểm ĐẾN TỪ CHÍNH NHÁNH ĐANG BỊ KIỂM. Một
    push vào `ops/**` vừa thêm tên mình vào `NGUOI_CO_THAM_QUYEN` vừa đổi lease là đủ:
    `checkout` lấy head đó, workflow chạy bộ kiểm đã bị sửa, cả `granted_by` lẫn
    `GITHUB_ACTOR` đều qua. Bộ kiểm nằm cùng nhánh với thứ nó kiểm thì nó không kiểm gì.

    Ca này canh phần MÁY canh được: mọi lời gọi `lease_publish.py`,
    `lease_publish_test.py` hoặc wrapper chạy bộ kiểm trong workflow phải đi qua bản
    neo (`$NEO/…`), không được gọi thẳng `ops/…`.

    KHÔNG canh được ở đây, và phải nói thẳng: với sự kiện `push`, GitHub lấy chính
    tệp workflow từ head, nên ai sửa được bộ kiểm cũng sửa được ca này lẫn mỏ neo.
    Phần ấy chỉ ruleset ngoài kho mới đóng. Ca này chặn TRÔI NGƯỢC do vô ý — bản vá
    bị "dọn cho gọn" về lại `ops/…` — chứ không chặn kẻ cố tình.
    """
    goc = HERE.parent / ".github" / "workflows"
    if not goc.is_dir():
        # Cùng chốt với t24: chỉ tha khi đây rõ ràng là BẢN SAO rời (bộ đột biến chép
        # mỗi `ops/`). Trong kho thật mà thiếu thư mục workflow thì phải ĐỎ.
        bang(not (HERE.parent / ".git").exists(),
             f"kho thật mà không thấy {goc} — ca này sẽ xanh rỗng")
        return
    tep = goc / "ops-publish-lease.yml"
    bang(tep.is_file(), f"không thấy {tep} — ca này sẽ xanh mà không đo gì")
    noi_dung = tep.read_text(encoding="utf-8")
    # Chỉ soi đối số đứng sau một token lệnh thực thi đã biết, không bó theo việc dòng
    # có NHẮC tên tệp. Dòng `sha256sum ops/…` cố ý in băm của head và cố ý không có
    # `$NEO`; coi nó là lời gọi sẽ báo oan. Đây vẫn là phép đo đối số, không phải parser
    # shell: thêm một token lệnh mới phải là quyết định có chủ ý và có phản chứng.
    thay = thay_wrapper = 0
    for so, duong in _cac_loi_goi_cong_lease(noi_dung):
        thay += 1
        if duong.endswith("chay_lease_publish_test.sh"):
            thay_wrapper += 1
        bang("$NEO" in duong or "${NEO}" in duong,
             f"ops-publish-lease.yml:{so} chạy {duong!r} — bộ kiểm này đến TỪ HEAD "
             f"ĐƯỢC ĐẨY, tức từ chính nhánh nó đang kiểm (finding P1, PR #104). "
             f"Phải gọi qua bản neo vào nhánh mặc định: \"$NEO/ops/…\"")
    # Chốt riêng cho wiring bộ kiểm: đừng để việc gỡ hẳn wrapper chỉ rơi vào thông điệp
    # đếm chung, vì ba lời gọi `lease_publish.py` khác vẫn đủ làm ngưỡng cũ xanh.
    bang(thay_wrapper >= 1,
         "không thấy lời gọi thực thi `chay_lease_publish_test.sh` trong workflow — "
         "cổng đăng lease đã gỡ hẳn bộ tự kiểm mà t25 vẫn đang chạy")
    # Bốn lời gọi thật hiện tại là wrapper + check + body + mark. Ngưỡng cũ là 3 và chú
    # thích gọi chúng là (test, check, body), nhưng `test` đã chuyển sang wrapper nên ba
    # lời gọi `lease_publish.py` còn lại tự chúng thoả ngưỡng, làm cổng xanh rỗng.
    bang(thay >= 4,
         f"chỉ thấy {thay} lời gọi cổng/wrapper trong workflow — chờ ít nhất 4 "
         f"(wrapper, check, body, mark); ca này đang không đo cái nó tưởng nó đo")
    # Mỏ neo phải CÓ THẬT, không chỉ là biến `$NEO` trỏ vào hư không.
    bang("git worktree add" in noi_dung and "default_branch" in noi_dung,
         "không thấy bước dựng worktree từ `default_branch` — `$NEO` phải được neo "
         "vào nhánh mặc định, nếu không thì nó chỉ là một tên biến khác cho head")


@ca
def t41_t25_chi_cat_chu_thich_run_inline_khi_chac_chan():
    """Khóa hai ĐỎ giả mà không đổi chúng lấy một XANH giả đắt hơn."""
    an_toan = {
        "chú thích nguyên dòng": "# sh chay_lease_publish_test.sh",
        "echo nhắc tên": 'run: echo "info: chay_lease_publish_test.sh"',
        "name nhắc tên": "name: kiểm tra chay_lease_publish_test.sh tồn tại",
        "chú thích sau lệnh, dạng sh":
            "run: echo ok # sh chay_lease_publish_test.sh",
        "chú thích sau lệnh, dạng bash":
            "run: echo ok # xem bash ops/chay_lease_publish_test.sh",
    }
    for ten, noi_dung in an_toan.items():
        thay = _cac_loi_goi_cong_lease(noi_dung)
        bang(not thay, f"t25 vẫn đếm oan {ten}: {thay}")

    loi_goi_that = {
        "thiếu NEO": "run: bash ops/chay_lease_publish_test.sh",
        "# trong nháy kép":
            'run: echo "a#b"; bash ops/chay_lease_publish_test.sh',
        "# trong nháy đơn":
            "run: echo 'a#b'; bash ops/chay_lease_publish_test.sh",
        "# sau chéo ngược":
            r"run: echo a\#b; bash ops/chay_lease_publish_test.sh",
        "# liền sau biểu thức Actions":
            "run: echo ${{ github.event.issue.number }}#x; "
            "bash ops/chay_lease_publish_test.sh",
    }
    for ten, noi_dung in loi_goi_that.items():
        thay = _cac_loi_goi_cong_lease(noi_dung)
        bang(thay == [(1, "ops/chay_lease_publish_test.sh")],
             f"t25 cắt quá tay ở ca {ten}, làm mất lời gọi thật: {thay}")

    # Với block scalar/heredoc, helper không biết trạng thái xuyên dòng nên KHÔNG cắt.
    # Giữ một ĐỎ giả ở vùng chưa hiểu vẫn rẻ hơn che mất một lời gọi thật.
    dong_heredoc = "  echo ok # bash ops/chay_lease_publish_test.sh"
    bang(_cat_chu_thich_run_inline(dong_heredoc) == dong_heredoc,
         "helper đã lấn sang thân block/heredoc dù không có trạng thái xuyên dòng")


def _doi_thu_muc_reviews():
    """Trả `ops/reviews`, và ĐỎ nếu nó vắng — KHÔNG có nhánh 'vắng thì thôi'.

    Nhánh cũ bỏ qua ca khi thư mục vắng, với lý do 'bản sao không phải kho thật'. Đo ra
    thì đó là một lỗ: xoá RIÊNG `README.md` -> ĐỎ, mà xoá CẢ thư mục -> vẫn 30/30 ĐẠT.
    Tức chốt bắt được đột biến nhỏ và bỏ lọt đột biến lớn hơn chứa nó.

    Cái giá thật nằm ở chỗ khác và đắt hơn: đột biến LUÔN chạy trên bản sao tạm (bài học
    "bom hẹn giờ" — không đột biến tệp thật). Bản sao không có `.git`, nên chính chỗ duy
    nhất ta dùng để đo sức của bộ test lại là chỗ chốt tự tắt. Bộ đo mà tự tắt trong môi
    trường đo thì mọi con số nó trả về đều không neo vào đâu.

    Một bản sao `ops/` hợp lệ vốn phải chứa `reviews/`. Nên đòi thẳng.
    """
    thu_muc = HERE / "reviews"
    bang(thu_muc.is_dir(),
         f"thiếu hẳn {thu_muc}. KHÔNG bỏ qua ca khi thư mục vắng: bản sao `ops/` hợp lệ "
         f"vốn phải chứa nó. Nhánh 'vắng thì thôi' từng làm CẢ t26 lẫn t27 XANH khi đột "
         f"biến xoá trọn thư mục — bắt được cái nhỏ, lọt cái to hơn chứa nó.")
    return thu_muc


def _bang(van: str, tieu_de: str) -> list:
    """Trả các HÀNG DỮ LIỆU của bảng dưới `## <tieu_de>`, mỗi hàng là dict {tên cột: ô}.

    SÁU bậc thu hẹp, mỗi bậc vì một lỗ ĐO ĐƯỢC. Chuỗi này mới là bài học, không phải
    từng bậc riêng lẻ:

    1. `in` cả tệp        -> id sót ở prose vẫn ĐẠT
    2. `in` các DÒNG bảng -> id trong `<!-- -->` trên dòng '|' vẫn ĐẠT
    3. `in` mọi Ô         -> tái dùng id được thoả bởi hàng của verdict KHÁC
    4. theo HÀNG          -> mô tả của hàng nhắc CHÉO verdict khác + id của nó vẫn ĐẠT
    5. theo CỘT CÓ TÊN    -> nhưng lấy cột thành HAI danh sách rồi `zip` thì hàng thiếu ô
       bị lọc lệch nhau ⇒ `zip` ghép ô của HAI hàng khác nhau; và bảng KHÔNG có hàng
       gạch phân cách vẫn được nhận, dù GitHub không render nó thành bảng.
    6. nay: đòi hàng gạch, và trả HÀNG-CÓ-KHOÁ — không bao giờ tách cột rồi ghép lại.

    Bậc 5 là bậc do CHÍNH bản vá bậc 4 sinh ra: tôi ràng "cùng hàng" bằng một cơ chế tự
    nó phá vỡ ranh giới hàng. Vá một lớp bằng cách mở một lớp khác.
    """
    import re
    van = re.sub(r"<!--.*?-->", "", van, flags=re.S)      # comment: người đọc KHÔNG thấy
    ra, lay, rao = [], False, None
    dau_bang, cho_gach = None, False

    def la_gach(dong):
        o = [x.strip() for x in dong.strip().strip("|").split("|")]
        return bool(o) and all(x and set(x) <= set("-: ") for x in o)

    for dong in van.splitlines():
        # Rào mã: PHẢI nhớ ký tự mở và ĐỘ DÀI. Cờ bật/tắt thô bỏ sót rào `~~~` và đóng
        # sớm rào ```` khi gặp dòng ``` bên trong — Markdown thì không đóng.
        m = re.match(r"^\s*(`{3,}|~{3,})", dong)
        if m:
            k, d = m.group(1)[0], len(m.group(1))
            if rao is None:
                rao = (k, d)
            elif k == rao[0] and d >= rao[1] and not dong.strip()[d:].strip():
                rao = None
            continue
        if rao is not None:                                # bảng trong khối mã là ví dụ
            continue
        if dong.startswith("## "):
            lay, dau_bang, cho_gach = (tieu_de in dong), None, False
            continue
        if not lay:
            continue
        if not dong.strip().startswith("|"):
            dau_bang, cho_gach = None, False               # hết bảng
            continue

        o = [x.strip().strip("`").strip() for x in dong.strip().strip("|").split("|")]
        if dau_bang is None:                               # ứng viên hàng tiêu đề
            dau_bang, cho_gach = [x.lower() for x in o], True
            continue
        if cho_gach:
            # Không có hàng gạch thì GitHub KHÔNG render thành bảng. Bộ đọc cũ chỉ BỎ QUA
            # hàng gạch chứ không ĐÒI nó, nên xoá `|---|` đi là người đọc mất bảng mà
            # `t27` vẫn xanh.
            if la_gach(dong):
                cho_gach = False
            else:
                dau_bang, cho_gach = None, False
            continue
        if la_gach(dong):
            continue
        ra.append({ten: o[i] for i, ten in enumerate(dau_bang) if i < len(o)})
    return ra


def _cot_duy_nhat(van: str, tieu_de: str, ten_cot: str) -> str:
    """Kiểm tên cột tồn tại và DUY NHẤT trong bảng; trả về khoá đã chuẩn hoá."""
    hang = _bang(van, tieu_de)
    bang(hang, f"bảng dưới '## …{tieu_de}…' RỖNG, thiếu hàng gạch `|---|`, hoặc không "
               f"có — không kiểm được gì")
    ten = ten_cot.strip().lower()
    dem = sum(1 for k in hang[0] if k == ten)
    bang(dem == 1,
         f"bảng '{tieu_de}': cột {ten_cot!r} xuất hiện {dem} lần — không định danh được "
         f"cột thì mọi phép kiểm theo cột chỉ là đoán")
    return ten


def _ten_tep(o: str) -> set:
    """Rút TÊN TỆP trong một ô, để so BẰNG NHAU thay vì so chuỗi con.

    Vì sao: `foo-verdict.md` là chuỗi con của `old-foo-verdict.md`, nên một hàng mục lục
    của tệp NÀY thoả luôn cho tệp KIA. Hai tên chồng nhau là đủ để một verdict không có
    hàng riêng mà vẫn xanh.
    """
    import re
    return set(re.findall(r"[\w.\-/]+\.(?:md|ya?ml)", o))


@ca
def t26_moi_bien_nhan_review_phai_khop_BAM_tep_no_tro_toi():
    """Biên nhận giao hàng trong `ops/reviews/` phải khớp băm tệp gốc.

    Vì sao có: verdict của reviewer là tệp NGUYÊN VĂN neo băm, không được sửa — kể cả
    để điền `evidence_url` sau khi đăng. Nên chỗ đăng được ghi ra một tệp biên nhận
    RIÊNG. Nhưng một biên nhận trỏ vào tệp đã đổi thì tệ hơn không có biên nhận: nó
    khai một con băm không còn đúng, mà người đọc lại tin. Ca này buộc hai thứ đi
    cùng nhau — đổi tệp gốc mà quên biên nhận thì ĐỎ.
    """
    import hashlib
    import yaml
    thu_muc = _doi_thu_muc_reviews()
    ds = sorted(thu_muc.glob("*.receipt.yaml"))
    bang(ds, f"không thấy biên nhận nào trong {thu_muc} — ca này sẽ xanh mà không đo gì")
    for p in ds:
        d = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        duong = str(d.get("verdict_path") or "").strip()
        sha = str(d.get("verdict_sha256") or "").strip()
        bang(duong and sha,
             f"{p.name}: biên nhận NỬA VỜI (verdict_path={duong!r} sha={sha!r}) — "
             f"băm không địa chỉ thì không kiểm được, địa chỉ không băm thì tệp đổi "
             f"lúc nào cũng không ai biết")
        f = HERE.parent / duong
        bang(f.is_file(), f"{p.name}: trỏ vào tệp không có: {duong}")
        thuc = hashlib.sha256(f.read_bytes()).hexdigest()
        bang(thuc == sha,
             f"{p.name}: LỆCH BĂM — biên nhận khai {sha}, tệp {duong!r} thực {thuc}. "
             f"Tệp verdict là NGUYÊN VĂN của reviewer: hoặc bạn vừa sửa nhầm nó, hoặc "
             f"biên nhận chưa cập nhật. Đừng ghi đè băm cho hết đỏ trước khi biết là ca nào.")
        # Biên nhận mà không nói đăng ở đâu thì nó không phải biên nhận.
        bang(str(d.get("evidence_url") or "").startswith("https://"),
             f"{p.name}: thiếu `evidence_url` dạng https — đây chính là trường mà bản "
             f"gốc để `pending-owner-post`, và là lý do biên nhận này tồn tại")


@ca
def t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc():
    """Mọi verdict/biên nhận phải có trong `ops/reviews/README.md`, và mọi caveat phải nêu tên ở đó.

    Vì sao có (finding của codex trên PR #114, ĐÚNG): tệp verdict là nguyên văn neo băm
    nên chỗ sai không vá được tại nguồn, và đính chính phải sống ở biên nhận. Nhưng
    người mở thẳng `verdict_path` để chạy lại lệnh KHÔNG có gì trỏ họ sang tệp sidecar
    — quét cả kho cũng không có bộ đọc nào đưa `verdict_usage_caveats` ra. Nghĩa là bản
    vá đầu tiên chỉ DỜI vấn đề sang một tệp ít người mở hơn, không giải nó.

    Ca này biến mục lục thành chốt: thêm caveat mà quên nâng lên `README.md` thì ĐỎ.
    Nó KHÔNG khẳng định mục lục đủ để cứu mọi người đọc — giới hạn ấy ghi ngay trong
    README. Nó chỉ bảo đảm một điều kiểm được: cảnh báo không nằm im một chỗ.

    BA LỖ đã bịt (codex tìm trên cây đã merge của PR #114; cả ba tái lập được trên
    master trước khi vá, cả ba đều cho 30/30 ĐẠT):

      L1  không có thư mục `ops/reviews`               -> ĐỎ qua `_doi_thu_muc_reviews`
      L2  bỏ caveat khỏi BẢNG, giữ id trong comment    -> soi Ô của bảng cảnh báo
      L3  thả một `*-verdict.md` mồ côi                -> glob verdict ĐỘC LẬP

    BA LỖ NỮA (codex tìm trên chính bản vá ba lỗ trên; cả ba cũng 30/30 ĐẠT trước khi vá):

      N1  id chỉ còn trong `<!-- … -->` TRÊN một dòng `|`  -> bỏ comment TRƯỚC khi tách Ô
      N2  tên verdict/biên nhận chỉ còn ở prose            -> soi Ô của bảng 'Mục lục'
      N3  biên nhận đúng tên nhưng `verdict_path` trỏ tệp KHÁC -> so khớp đường dẫn

    N1 và N2 đáng ghi hơn cả: bản vá L2 sinh ra để bịt lỗ comment HTML, rồi **tự nó vẫn
    thủng bằng đúng comment HTML** — vì nó chỉ thu hẹp PHẠM VI (dòng bảng) mà không đổi
    THỨ ĐEM SO (văn bản thô). Và tôi áp ý "soi trong bảng" cho caveat mà quên áp cho mục
    lục — cùng một khẳng định, hai vị trí, lần thứ tư trong đợt này.
    """
    import yaml
    thu_muc = _doi_thu_muc_reviews()
    muc_luc = thu_muc / "README.md"
    bang(muc_luc.is_file(),
         f"thiếu {muc_luc} — thư mục verdict không có cửa vào thì cảnh báo trong biên "
         f"nhận không tới được ai")
    van = muc_luc.read_text(encoding="utf-8")
    CB = "Cảnh báo đang có hiệu lực"
    ML = "Mục lục"
    k_cb_v = _cot_duy_nhat(van, CB, "tệp verdict")
    k_cb_id = _cot_duy_nhat(van, CB, "id")
    k_ml_v = _cot_duy_nhat(van, ML, "tệp verdict")
    k_ml_bn = _cot_duy_nhat(van, ML, "biên nhận")
    hang_cb = _bang(van, CB)
    hang_ml = _bang(van, ML)
    bang(hang_ml, f"{muc_luc.name}: bảng 'Mục lục' RỖNG — mục lục rỗng thì mọi phép "
                  f"kiểm dưới đây chỉ là hình thức")

    def co_o_cot(ten, hang, khoa):
        """Tên tệp phải BẰNG một tên trong ô của đúng cột — không phải chuỗi con."""
        return any(ten in _ten_tep(h.get(khoa, "")) for h in hang)

    ds = sorted(thu_muc.glob("*.receipt.yaml"))
    ds_verdict = sorted(thu_muc.glob("*-verdict.md"))
    bang(ds, f"không thấy biên nhận nào trong {thu_muc} — ca này sẽ xanh mà không đo gì")
    bang(ds_verdict, f"không thấy verdict nào trong {thu_muc} — ca này sẽ xanh mà không đo gì")

    # L3 — duyệt VERDICT theo đĩa, KHÔNG suy từ biên nhận. Suy từ biên nhận thì một
    # verdict chưa ai làm biên nhận sẽ vô hình đúng lúc nó cần bị thấy nhất.
    for f in ds_verdict:
        bang(co_o_cot(f.name, hang_ml, k_ml_v),
             f"{muc_luc.name}: verdict {f.name!r} KHÔNG có trong CỘT 'tệp verdict' của "
             f"bảng 'Mục lục'. Nằm ở đoạn giải thích, trong comment HTML, hay ở một cột "
             f"mô tả nào đó thì bảng render ra vẫn thiếu nó.")
        bn = thu_muc / f"{f.stem}.receipt.yaml"
        bang(bn.is_file(),
             f"{f.name}: KHÔNG có biên nhận {bn.name}. Verdict không biên nhận là verdict "
             f"không ai khai đã đăng ở đâu — và `t26` cũng không đụng tới nó.")
        # N3+P1 — đúng TÊN chưa đủ, và đúng BASENAME cũng chưa đủ. So ĐƯỜNG DẪN ĐẦY ĐỦ:
        # một biên nhận trỏ `ops/reviews/archive/x.md` trong khi tệp thật nằm ở
        # `ops/reviews/x.md` có basename y hệt, nên t26 đi băm BẢN LƯU TRỮ còn tệp thật
        # không ca nào đụng tới. Đã đo: thay ruột tệp thật bằng rác mà suite vẫn 30/30.
        d_bn = yaml.safe_load(bn.read_text(encoding="utf-8")) or {}
        tro = PurePosixPath(str(d_bn.get("verdict_path") or "").strip().lstrip("./"))
        mong = PurePosixPath(f.relative_to(HERE.parent).as_posix())
        bang(tro == mong,
             f"{bn.name}: `verdict_path` trỏ {str(tro)!r} chứ không phải {str(mong)!r}. "
             f"So basename thôi thì một bản sao ở thư mục khác lọt qua, và tệp THẬT "
             f"không được băm bởi bất kỳ ca nào.")

    for p in ds:
        d = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        bang(co_o_cot(p.name, hang_ml, k_ml_bn),
             f"{muc_luc.name}: biên nhận {p.name} KHÔNG có trong CỘT 'biên nhận' của "
             f"bảng 'Mục lục'")
        ten_verdict = Path(str(d.get("verdict_path") or "")).name
        bang(ten_verdict and co_o_cot(ten_verdict, hang_ml, k_ml_v),
             f"{muc_luc.name}: verdict {ten_verdict!r} KHÔNG có trong CỘT 'tệp verdict' "
             f"của bảng 'Mục lục'")

        cac_caveat = d.get("verdict_usage_caveats") or []
        for c in cac_caveat:
            ma = str((c or {}).get("id") or "").strip()
            bang(ma, f"{p.name}: có caveat KHÔNG có `id` — không nêu tên được thì "
                     f"không nâng lên mục lục được, và cũng không ai trích dẫn được")
            # L2+N4+P3 — id phải nằm ở CỘT `id`, trên CÙNG HÀNG với tên verdict ở CỘT
            # `tệp verdict`. Ràng theo hàng thôi vẫn thủng: phần mô tả của một hàng nhắc
            # CHÉO tên verdict khác kèm id của nó thì phép kiểm "cả hai chuỗi có mặt đâu
            # đó trong hàng" nhận nhầm đó là cảnh báo của verdict thứ hai.
            bang(any(ma in {x.strip() for x in h.get(k_cb_id, "").split()}
                     and ten_verdict in _ten_tep(h.get(k_cb_v, ""))
                     for h in hang_cb),
                 f"{muc_luc.name}: caveat {ma!r} của {p.name} KHÔNG nằm ở CỘT 'id' trên "
                 f"cùng hàng với {ten_verdict!r} ở CỘT 'tệp verdict', trong bảng "
                 f"'Cảnh báo đang có hiệu lực'. Bị nhắc trong phần mô tả của hàng khác "
                 f"KHÔNG tính — verdict này vẫn phải có hàng cảnh báo của riêng nó.")


@ca
def t31_moi_workflow_cai_pyyaml_phai_GHIM_va_ghim_CUNG_MOT_ban():
    """Mọi bước cài PyYAML trong workflow phải ghim exact, và tất cả cùng một số.

    Vì sao có, hai lớp:

    1. **Spec trần.** Cross-review PR #134 (codex) nêu `unpinned-pyyaml-ci-dependency`:
       `pip install pyyaml` không biên làm CÙNG MỘT SHA có thể xanh hôm nay và đỏ sau
       này mà cây không đổi. Cùng lớp với tiền lệ `pypdf>=4.0` không có trần. Bộ kiểm
       cổng đăng lease chạy ở đường có `contents: write` + `issues: write`, nên một
       dependency trôi ở đó là trôi ngay dưới chân cổng.

    2. **Hai bản sẽ trôi lệch.** Bản vá cho lớp 1 ghi `PyYAML==6.0.3` vào HAI tệp
       workflow. CLAUDE.md đã ghi đúng hình dạng này ở ca quét secrets: *"hai bản sẽ
       trôi lệch, và bên quên cập nhật chính là bên đẩy lọt"*. Nâng bản ở một chỗ mà
       quên chỗ kia thì hai đường chạy hai runtime khác nhau, và chỗ quên là chỗ không
       ai đo. Ca này biến lời hứa "nhớ sửa cả hai" thành chốt.

    Ca này sinh ra từ chính lượt vá lớp 1: nghĩ ra được rủi ro thì phải biến ngay thành
    ca test, đừng để nó nằm trong chú thích — chỗ đó là nơi các ca đi chết.
    """
    import re
    goc = HERE.parent / ".github" / "workflows"
    if not goc.is_dir():
        # Cùng chốt chống xanh-rỗng với `t24`: chỉ tha khi đây rõ ràng là BẢN SAO rời.
        bang(not (HERE.parent / ".git").exists(),
             f"kho thật mà không thấy {goc} — ca này sẽ xanh rỗng")
        return
    ds = sorted(p for p in goc.iterdir() if p.suffix in (".yml", ".yaml"))
    bang(ds, f"không thấy workflow nào trong {goc} — ca này sẽ xanh mà không đo gì")

    # Bắt MỌI dòng cài pyyaml, kể cả viết hoa/thường khác nhau, rồi mới xét nó có ghim
    # không. Bắt theo `pip install` chứ không theo `PyYAML==` — nếu chỉ tìm dạng ĐÚNG
    # thì một dòng SAI (spec trần) không khớp mẫu và ca này im lặng cho qua.
    RE_CAI = re.compile(r"pip\s+install\b[^\n]*?\bpyyaml", re.I)
    RE_GHIM = re.compile(r"\bPyYAML==(\d+(?:\.\d+)*)\b", re.I)

    thay = []
    for p in ds:
        for so, dong in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            if not RE_CAI.search(dong):
                continue
            m = RE_GHIM.search(dong)
            bang(m, f"{p.name}:{so} cài PyYAML mà KHÔNG ghim exact: {dong.strip()!r} — "
                    f"spec trần làm cùng một SHA xanh hôm nay, đỏ sau này mà cây không đổi")
            thay.append((p.name, so, m.group(1)))

    # Chốt chống xanh-rỗng: hai tệp ĐANG có bước cài. Bộ này về 0 nghĩa là mẫu khớp
    # hỏng, không phải cây sạch — và khi ấy hai chốt trên không đo gì.
    bang(len(thay) >= 2,
         f"chỉ thấy {len(thay)} bước cài PyYAML (đợi >= 2) — mẫu khớp có thể đã hỏng; "
         f"ca xanh vì không tìm thấy gì thì tệ hơn ca đỏ")

    ban = {v for _, _, v in thay}
    bang(len(ban) == 1,
         f"các workflow ghim PyYAML LỆCH NHAU: "
         f"{', '.join(f'{t}:{s}={v}' for t, s, v in thay)} — hai đường chạy hai runtime "
         f"khác nhau, và chỗ quên nâng bản chính là chỗ không ai đo")


def _than_buoc_chon_lease() -> str:
    """Trích THÂN bước `tìm lease vừa đổi` TỪ CHÍNH tệp workflow.

    Chép lại thân bước vào test là dựng hai bản sẽ trôi lệch, và bên quên cập nhật
    chính là bên đẩy lọt — cùng nếp mà `ops/don_ref_chot_test.sh` đã phải học.
    """
    import yaml
    goc = HERE.parent / ".github" / "workflows"
    if not goc.is_dir():
        # Cùng chốt với t24/t25: chỉ tha khi đây rõ ràng là BẢN SAO rời. Trong kho thật
        # mà thiếu thư mục workflow thì phải ĐỎ, kẻo ca xanh rỗng.
        assert not (HERE.parent / ".git").exists(), \
            f"kho thật mà không thấy {goc} — ca này sẽ xanh mà không đo gì"
        return ""
    tep = goc / "ops-publish-lease.yml"
    assert tep.is_file(), f"không thấy {tep} — ca này sẽ xanh mà không đo gì"
    d = yaml.safe_load(tep.read_text(encoding="utf-8"))
    buoc = [b for b in d["jobs"]["dang"]["steps"] if b.get("name") == "tìm lease vừa đổi"]
    assert len(buoc) == 1, f"chờ ĐÚNG một bước `tìm lease vừa đổi`, thấy {len(buoc)}"
    b = buoc[0]
    # ĐIỀU KIỆN ĐỂ CA NÀY TỒN TẠI: thân bước không còn `${{ }}`. Còn biểu thức thì nó
    # KHÔNG chạy lại được ngoài Actions, và ta sẽ chỉ đo một bản chép tay.
    assert "${{" not in b["run"], \
        "thân `run` còn nội suy biểu thức Actions — GitHub nội suy trên TOÀN BỘ thân " \
        "trước khi shell thấy nó (một cặp rỗng trong CHÚ THÍCH đã làm hỏng cả " \
        "ops-don-ref.yml, run 31971137920: 0 job), và thân có biểu thức thì không " \
        "chạy lại được ở đây. Khai qua `env:`."
    assert set(b.get("env") or {}) >= {"TRUOC", "NAY", "MAC_DINH"}, \
        f"bước phải khai TRUOC/NAY/MAC_DINH qua `env:`, thấy {list(b.get('env') or {})}"
    return b["run"]


def _kho_thu(tmp: Path):
    """Dựng kho có `origin` THẬT: master mang một lease CŨ, HẾT HẠN, CHƯA TỪNG ĐĂNG.

    `commit.gpgsign=false` KHÔNG phải cho gọn — nó đóng một finding P2 của cross-review
    lượt 2 (codex, head `23588c97`). Trên máy có `commit.gpgsign=true` toàn cục mà signer
    không gọi được, fixture chết bằng `fatal: failed to write commit object` và `t32` ĐỎ vì
    **cấu hình của host**, không vì thứ nó đo. Reviewer đo được cả hai chiều: `rc=1 32/33`
    với signing bật, `rc=0 33/33` khi tắt.

    Một cổng đỏ vì lý do không liên quan tệ ngang một cổng xanh giả: cả hai đều làm người
    đọc đi sai hướng. Phạm vi tắt signing chỉ trong kho fixture tạm — không đụng kho thật,
    không che ca nào về chữ ký.
    """
    def g(cay, *a):
        return subprocess.run(["git", "-c", "user.email=a@b", "-c", "user.name=c",
                               "-c", "commit.gpgsign=false",
                               "-C", str(cay), *a],
                              capture_output=True, text=True, check=True)
    goc = tmp / "origin.git"
    subprocess.run(["git", "init", "-q", "--bare", str(goc)], check=True)
    cay = tmp / "cay"
    subprocess.run(["git", "clone", "-q", str(goc), str(cay)], check=True)
    # DỰNG LẠI ĐÚNG MÁY ĐÃ LÀM t32 ĐỎ, ngay trong fixture — nếu không thì chốt trên chỉ là
    # lời hứa: nó chạy xanh cả khi ai đó gỡ `-c commit.gpgsign=false` ra, trên một máy
    # không bật signing. Đặt ở LOCAL config vì `-c` dòng lệnh thắng config tệp; gỡ `-c` ra
    # là fixture chết ngay, tức ca này ĐO chốt chứ không chỉ mang chốt.
    # BÁM ĐÚNG KHOÁ, và đây là chỗ bản đầu SAI: nó đặt `gpg.program` — khoá của định dạng
    # **openpgp** — trong khi máy dựng fixture khai `gpg.format=ssh`, nên chốt giả bám vào
    # một khoá không ai đọc và mutant "gỡ `-c commit.gpgsign=false`" SỐNG SÓT (đo được:
    # `giet 0/1`). Ép luôn `gpg.format=ssh` để fixture không phụ thuộc cấu hình host, rồi
    # trỏ `gpg.ssh.program` vào một đường dẫn không tồn tại.
    for k, v in (("commit.gpgsign", "true"),
                 ("gpg.format", "ssh"),
                 ("user.signingkey", "khong-phai-khoa-that"),
                 ("gpg.ssh.program", str(tmp / "signer-khong-ton-tai"))):
        subprocess.run(["git", "-C", str(cay), "config", k, v], check=True)
    (cay / "ops" / "leases").mkdir(parents=True)
    # Chính hình dạng đã giết cổng ngày 20-08: hết hạn, KHÔNG `posted_comment_id`.
    (cay / "ops" / "leases" / "cu-het-han.yaml").write_text(
        f"lease_id: cu-het-han\nlease_expires_at_utc: '{khi_truoc(48)}'\n", encoding="utf-8")
    g(cay, "add", "-A")
    g(cay, "commit", "-qm", "nen")
    g(cay, "branch", "-M", "master")
    g(cay, "push", "-q", "origin", "master")
    return cay, g


def _bash_posix() -> str:
    """Trả đường dẫn `bash` POSIX THẬT — KHÔNG phải `bash` của WSL.

    ĐÃ TRẢ GIÁ (master `e03c6d28`, run 32351777642, job `gate (windows-latest)`):
    `subprocess.run(["bash", ...])` trên runner Windows phân giải sang
    `C:\\Windows\\System32\\bash.exe` — cửa vào WSL — và nó trả

        Windows Subsystem for Linux has no installed distributions.

    với `rc=1`. Ca `t32` đọc mã ấy thành "bước chọn lease ĐỎ" và báo một finding KHÔNG CÓ
    THẬT, trong khi thứ hỏng là **trình thông dịch**, không phải thân bước.

    Cùng họ với bài học `taskkill` của kho: một cái TÊN phân giải sang thứ khác trên nền
    khác. Nên ở đây dùng DANH SÁCH CHO PHÉP (Git Bash), và loại thẳng `System32`.

    Nói rõ phạm vi: bước được đo chạy trong job `runs-on: ubuntu-latest`, nên Windows chỉ
    là nơi bộ test tình cờ chạy. Nhưng "tình cờ" mà báo finding giả thì vẫn phải chữa.

    HỢP NHẤT (#570, revision 2). Thân cũ của hàm này là bộ giải RIÊNG thứ nhất trong ba
    bộ giải độc lập cho cùng một khuyết tật, và nó lọc theo TÊN: danh sách Git Bash cộng
    một phép loại chuỗi `"system32"`. Phép đo `570-do-2` trên Windows thật cho thấy lọc
    theo tên KHÔNG diễn tả nổi khuyết tật — thứ phân biệt được là HÀNH VI:

        C:\\Windows\\system32\\bash.EXE      -> $0=/bin/bash  $#=0   (đối số biến mất)
        C:\\Program Files\\Git\\bin\\bash.exe -> $0=t40        $#=3

    Nên nay hàm này uỷ quyền cho `ops/bash_nen.py`, nơi quyết bằng phép thử NĂNG LỰC. Giữ
    nguyên HỢP ĐỒNG cũ — trả chuỗi rỗng khi không có — vì các ca gọi nó đang đọc như vậy.
    """
    import bash_nen
    duong, _ = bash_nen.tim_bash()
    return duong or ""


def _bash_cho_cai_actionlint() -> str:
    """`bash` ĐÃ CHỨNG MINH làm được việc, cho sáu ca `t35`-`t40`. FAIL-CLOSE, không bỏ qua.

    VÌ SAO KHÔNG `shutil.which("bash")` (Issue #570, đo 19-09-2026 trên Windows thật).
    Nó trả `C:\\Windows\\system32\\bash.EXE` — bộ phóng WSL — và sáu ca chết TRƯỚC dòng
    đầu của `ops/cai_actionlint.sh` với `rc=127`. Sáu lời khai của chúng khi ấy
    ("không cưỡng chế bản ghim", "loại archive bị suy từ suffix", …) là QUY SAI NGUYÊN
    NHÂN: không lời nào được đo. `ops/cai_actionlint.sh` LÀNH — trên Git Bash cùng máy,
    26/26 khẳng định ĐẠT và 6/6 đột biến bị giết đúng lý do.

    Đây là lần thứ BA cùng khuyết tật (`t32` → `_bash_posix`; `_bash_windows` của
    `ops/cong_cu.py`; nay sáu ca này), nên chốt KHÔNG phải một bộ giải riêng thứ tư:
    `ops/bash_nen.py` là MỘT bộ giải dùng chung, và nó quyết bằng phép thử NĂNG LỰC chứ
    không bằng một danh sách tên — vì phép đo cho thấy không lọc theo tên nào diễn tả nổi
    "con bash này làm hỏng argv".

    Thiếu bash dùng được ⇒ ĐỎ kèm CHẨN ĐOÁN, KHÔNG `return` sớm: một ca `return` sớm vẫn
    được harness đếm là ĐẠT (bệnh `t24`), và đó đúng là cách sáu ca này vô dụng suốt.
    """
    import bash_nen
    duong, chan_doan = bash_nen.tim_bash()
    bang(duong,
         "KHÔNG ĐO ĐƯỢC: không `bash` nào làm được việc. Chẩn đoán từng ứng viên: "
         + ("; ".join(f"{c['duong']}: {c['ly_do']}" for c in chan_doan)
            or "không tìm thấy ứng viên nào")
         + ". Cấp một `bash` POSIX thật (Git for Windows) cho runner; "
           "`C:\\Windows\\System32\\bash.exe` là bộ phóng WSL và KHÔNG dùng được.")
    return duong


def _chay_than(than: str, cay: Path, truoc: str, nay: str, mac_dinh: str = "master"):
    import os
    mt = dict(os.environ, TRUOC=truoc, NAY=nay, MAC_DINH=mac_dinh)
    vo = _bash_posix()
    # KHÔNG ĐO ĐƯỢC ≠ ĐẠT: thiếu bash POSIX thì ném, để `t32` ĐỎ với đúng lý do — chứ
    # không lặng lẽ trả một kết quả rỗng rồi được đếm là qua.
    if not vo:
        raise AssertionError(
            "KHÔNG ĐO ĐƯỢC: không tìm thấy `bash` POSIX (Git Bash). `bash` trong "
            "System32 là WSL, không dùng được để chạy thân bước.")
    p = subprocess.run([vo, "-c", than], cwd=str(cay), env=mt,
                       capture_output=True, text=True)
    ds = (cay / "ds.txt")
    return p.returncode, (ds.read_text(encoding="utf-8").split() if ds.is_file() else []), p.stderr + p.stdout


ZERO40 = "0" * 40


@ca
def t32_buoc_chon_lease_KHONG_duoc_quet_CA_THU_MUC():
    """Push MỞ NHÁNH MỚI chỉ được xử lý lease mà NHÁNH ẤY thêm — không phải cả thư mục.

    VÌ SAO CÓ CA NÀY, và nó không phải giả thiết: lượt chạy `32342373756`
    (2026-08-20T07:05Z, push nhánh `ops/lease-plat-m4-exec-1`) ĐỎ `rc=8`. Log liệt kê
    BẢY tệp lease KHÔNG nằm trong push đó ⇒ nó đi vào đường dự phòng
    `find ops/leases -type f`. Tệp giết cổng là `don-nhanh-base-review-6-…`: KHÔNG có
    `posted_comment_id`, hạn `2026-08-18T17:45Z`.

    Hệ quả: từ 18-08 tới 20-08, MỌI lease mới không đăng được, và không ai biết — cổng
    không nói dối, nó VẮNG MẶT.

    VẾ THỨ HAI CỦA CHÚ THÍCH CŨ Ở ĐÂY TỪNG SAI, và 20-09-2026 là lần đầu nó bị ĐO. Bản
    trước viết: chú thích cũ khai "chốt `posted_comment_id` lo phần không đăng trùng" —
    *"đúng cho lease ĐÃ đăng (rc=9), sai cho lease CHƯA TỪNG đăng"*. Vế in nghiêng đúng
    một NỬA. Đo trên `origin/master` `a1bbdc10`, `kiem_github` với `_doc_gh` giả:

        còn hạn + ĐÃ có dấu   -> rc=9    ✔ vế cũ đúng ở đây
        HẾT HẠN + ĐÃ có dấu   -> rc=8    ✘ vế cũ SAI ở đây

    Vì sao: `kiem_github` gọi `kiem()` ở dòng đầu, mà `kiem()` ném `rc=8` cho lease hết
    hạn TRƯỚC khi `_kiem_comment_da_co` kịp chạy. Nên với một lease **đã đăng rồi mới hết
    hạn**, đường `rc=9` KHÔNG BAO GIỜ tới được — nhánh `rc=9` của workflow có sẵn và viết
    đúng, nó chỉ không bao giờ được gọi. Cùng họ *"cổng VẮNG MẶT trông giống cổng xanh"*,
    đúng như đoạn ngay trên.

    Nói cho đủ: `posted_comment_id` thôi làm dấu "đã đăng" từ packet #396 — dấu duy nhất
    nay là chính comment trên Issue (`t126` ghim vị từ ấy). Nên câu trên bàn về một cơ chế
    đã nghỉ; thứ còn sống là THỨ TỰ, và thứ tự mới là chỗ sai.

    Packet #579 đảo thứ tự (dò dấu TRƯỚC, `kiem()` SAU) nên nay cả hai hình dạng đều `rc=9`;
    `t174`/`t175` là cặp phản chứng ĐỎ NGƯỢC CHIỀU cho đúng chuyện đó.

    CHƯA SỬA ĐƯỢC, khai thẳng: cùng câu sai ấy còn nằm ở
    `.github/workflows/ops-publish-lease.yml` (khối chú thích của bước `tìm lease vừa đổi`).
    Tệp đó CỐ Ý ngoài write set của packet này, nên bản vá để lại đúng một lời khai cũ ở đó.

    Và mọi lease đều đi bằng một nhánh MỚI theo `ops/README.md`, nên đường "dự phòng"
    ấy thật ra là đường CHÍNH — đúng lớp bệnh "nhánh không-thấy-thì-bỏ-qua nằm im tới
    đúng lúc cần".
    """
    than = _than_buoc_chon_lease()
    if not than:
        return
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        cay, g = _kho_thu(tmp)
        g(cay, "checkout", "-qb", "ops/lease-moi")
        (cay / "ops" / "leases" / "moi.yaml").write_text(
            f"lease_id: moi\nlease_expires_at_utc: '{mai_sau()}'\n", encoding="utf-8")
        g(cay, "add", "-A")
        g(cay, "commit", "-qm", "lease moi")
        head1 = g(cay, "rev-parse", "HEAD").stdout.strip()

        # (1) NHÁNH MỚI: `before` toàn số 0. Chỉ được thấy lease nhánh này thêm.
        rc, ds, ra = _chay_than(than, cay, ZERO40, head1)
        assert rc == 0, f"nhánh mới mà bước chọn lease ĐỎ (rc={rc}): {ra}"
        assert ds == ["ops/leases/moi.yaml"], \
            f"chờ ĐÚNG lease nhánh này thêm, được {ds} — quét cả thư mục thì một lease " \
            f"cũ hết hạn sẽ giết cả lượt đăng (bug #195)"

        # (2) PUSH THƯỜNG trên cùng nhánh: vẫn phải diff `before`..`sha`, không lùi về
        # merge-base — lùi về đó là kéo theo cả lease của commit TRƯỚC, đã đăng rồi.
        (cay / "ops" / "leases" / "moi2.yaml").write_text(
            f"lease_id: moi2\nlease_expires_at_utc: '{mai_sau()}'\n", encoding="utf-8")
        g(cay, "add", "-A")
        g(cay, "commit", "-qm", "lease moi 2")
        head2 = g(cay, "rev-parse", "HEAD").stdout.strip()
        rc, ds, ra = _chay_than(than, cay, head1, head2)
        assert rc == 0, f"push thường mà ĐỎ (rc={rc}): {ra}"
        assert ds == ["ops/leases/moi2.yaml"], f"push thường: chờ moi2.yaml, được {ds}"

        # (3) KHÔNG ĐO ĐƯỢC ≠ KHÔNG CÓ GÌ. Mốc so không phân giải được thì phải ĐỎ, chứ
        # không được trả danh sách rỗng — rỗng đọc y hệt "không có lease nào để đăng".
        rc, ds, ra = _chay_than(than, cay, ZERO40, head2, mac_dinh="nhanh-khong-ton-tai")
        assert rc != 0, f"mốc so không phân giải được mà rc=0, ds={ds}: {ra}"
        assert "KHONG DO DUOC" in ra, f"đỏ mà không nói KHÔNG ĐO ĐƯỢC: {ra!r}"

        # ...và nhánh mặc định RỖNG cũng là không đo được, không phải "quét tất".
        rc, _ds, ra = _chay_than(than, cay, ZERO40, head2, mac_dinh="")
        assert rc != 0, f"MAC_DINH rỗng mà vẫn chạy tiếp: {ra}"


@ca
def t33_workflow_dang_lease_phai_qua_actionlint():
    """`actionlint` phải XANH trên `ops-publish-lease.yml` — và THIẾU công cụ là ĐỎ.

    PHẠM VI, nói đúng bằng phép đo: ca này lint ĐÚNG MỘT tệp — `ops-publish-lease.yml`,
    workflow mà bộ test này là cổng của nó. Nó KHÔNG lint bốn workflow còn lại của kho.
    Bản trước viết "phải XANH trên mọi workflow" — lời khai rộng hơn thân ca, tức hình dạng
    A trong chính ca sinh ra để chống một cổng nói dối (#269 mục N3).

    "YAML parse được" KHÁC "GitHub NHẬN". Đo 16-08-2026: `ops-don-ref.yml` bị GitHub từ
    chối, dấu hiệu là một run mang tên ĐƯỜNG DẪN TỆP, 0 job, `conclusion: failure` — lỗi
    XÁC THỰC ĐỊNH NGHĨA, không phải một job đỏ. SÁU lượt cross-review đều kết luận "YAML
    ok" vì cả sáu chỉ kiểm bằng PyYAML, mà PyYAML không biết luật của GitHub.

    Một cổng tự tắt khi thiếu công cụ là cổng không tồn tại đúng lúc nó cần nhất, nên ca
    này ĐỎ khi không có `actionlint` — trừ khi đây là bản sao rời không có `.git`.
    """
    import shutil
    goc = HERE.parent / ".github" / "workflows"
    if not goc.is_dir():
        assert not (HERE.parent / ".git").exists(), \
            f"kho thật mà không thấy {goc} — ca này sẽ xanh mà không đo gì"
        return
    duong = shutil.which("actionlint")
    assert duong, (
        "KHÔNG ĐO ĐƯỢC: thiếu `actionlint`. PyYAML không thay được nó — nó không biết "
        "luật của GitHub. Cài: go install github.com/rhysd/actionlint/cmd/actionlint@latest "
        "(hoặc `brew install actionlint`, hoặc tải bản dựng sẵn từ releases).")
    p = subprocess.run([duong, str(goc / "ops-publish-lease.yml")],
                       capture_output=True, text=True)
    assert p.returncode == 0, f"actionlint ĐỎ (rc={p.returncode}):\n{p.stdout}{p.stderr}"


def _dong_lenh(than: str) -> list:
    """Tách thân `run` thành các LỆNH: nối dòng bị ngắt bằng `\\`, rồi bỏ chú thích.

    NỐI TRƯỚC, LỌC SAU — và thứ tự ấy là một finding của chính bộ test này chứ không phải
    lý thuyết: bản đầu khớp theo TỪNG DÒNG, nên lệnh

        curl -fsSL -o "$DICH/goi" \\
          "https://…/actionlint/releases/download/v${AL_VER}/${GOI}"

    có `curl` ở dòng một và `actionlint` ở dòng hai ⇒ không dòng nào chứa CẢ HAI, và phép
    kiểm kết luận "workflow không cài actionlint" trong khi nó cài. Một phép quét đọc lệnh
    mà không hiểu dấu nối dòng thì nó đang đọc VĂN BẢN, không đọc LỆNH.
    """
    noi, dem = [], ""
    for d in than.splitlines():
        if d.lstrip().startswith("#"):
            continue
        dem = f"{dem} {d.strip()}" if dem else d.strip()
        if dem.endswith("\\"):
            dem = dem[:-1].rstrip()
            continue
        if dem:
            noi.append(dem)
        dem = ""
    if dem:
        noi.append(dem)
    return noi


@ca
def t34_workflow_khong_duoc_goi_THANG_tep_bo_test():
    """Phương án (1): chỉ canh lời gọi thẳng tệp `.py`, không phân tích shell.

    Wrapper đã gộp installer + selftest thành một tiến trình. Vì vậy chốt này KHÔNG còn
    tuyên bố "đã chứng minh job cài công cụ trước khi chạy"; nó chỉ bắt một hồi quy hẹp,
    đọc được: workflow gọi thẳng `lease_publish_test.py` thay vì đi qua wrapper.

    Hai phản chứng vòng 2 vẫn đỏ vì cả hai đều đưa lời gọi thẳng `.py` trở lại job chạy
    test, dù installer nằm ở job khác hay nằm sau nó. `bash -c "python ...py"` cũng đỏ vì
    vẫn chứa chính lời gọi thẳng ấy.

    PHẠM VI ĐO ĐƯỢC: t34 chỉ nhận canonical
    `python|python3|py <đường-dẫn>/lease_publish_test.py` KHÔNG CỜ. Năm dạng đã đo là
    lọt: `python -m ops.lease_publish_test`; `python3 -u ops/lease_publish_test.py`;
    shebang trực tiếp `./ops/lease_publish_test.py`; `uv run ops/lease_publish_test.py`;
    và `python -X utf8 ops/lease_publish_test.py`. Runner khác ngoài ba token canonical
    cũng không thuộc lời hứa. Lời khai được hạ xuống đúng phép đo thay vì nối regex để
    đuổi theo cú pháp shell; quyết định danh sách cho phép đã tách sang packet `#209`.

    Đổi wrapper thành một trong các dạng lọt vẫn có cùng nghĩa với xoá wiring của gate;
    một selftest không thể tự chứng minh nó đã được CI gọi.

    PHẠM VI BẰNG SỐ: `t34` che **3/8 = 37,5%** dạng gọi đã biết (3 canonical nhận được,
    5 dạng đã đo là lọt). Nói bằng số vì "che phần lớn" là lời khai không có phép đo, và
    kho đã trả giá đúng hình dạng ấy nhiều lần.

    NỢ CÓ TÊN `PLAT-X5-required-status-check`: branch protection phải require status của
    job `gate` (và lượt đăng lease tương ứng). Chốt ngoài kho ấy mới trả lời "CI có thật sự
    chạy gate không". `t34` chỉ là lan can chống hồi quy vô ý, không phải security boundary.
    Q7 ĐÃ QUYẾT (21-08-2026, `ducthangho`): KHÔNG BẬT ⇒ nợ này là THƯỜNG TRỰC, ghi ở
    `ops/NO_KY_THUAT.md` §9. `t42` bên dưới canh cho docstring này không trôi rộng ra.
    """
    import yaml
    goc = HERE.parent / ".github" / "workflows"
    if not goc.is_dir():
        bang(not (HERE.parent / ".git").exists(),
             f"kho thật mà không thấy {goc} — ca này sẽ xanh mà không đo gì")
        return
    goi_thang = []
    for tep in sorted(goc.glob("*.yml")) + sorted(goc.glob("*.yaml")):
        d = yaml.safe_load(tep.read_text(encoding="utf-8")) or {}
        for ten_job, job in (d.get("jobs") or {}).items():
            for i, b in enumerate(job.get("steps") or []):
                than = b.get("run")
                if not isinstance(than, str):
                    continue
                for lenh in _dong_lenh(than):
                    if _CHAY_BO_TEST.search(lenh):
                        goi_thang.append(
                            f"{tep.name}:{ten_job}:bước {i} ({b.get('name') or 'không tên'})")
    bang(not goi_thang,
         f"workflow gọi THẲNG `lease_publish_test.py` thay vì wrapper: {goi_thang}. "
         f"Chuyển cài + chạy về `ops/chay_lease_publish_test.sh`; không mở rộng regex "
         f"để giả vờ chứng minh mọi cú pháp shell.")


def _bam_tep(duong_dan):
    """sha256 của một tệp — để ca test tự cấp `AL_SHA256` cho gói GIẢ nó vừa dựng."""
    import hashlib
    h = hashlib.sha256()
    with open(duong_dan, "rb") as f:
        for khoi in iter(lambda: f.read(65536), b""):
            h.update(khoi)
    return h.hexdigest()


# Chỉ nhận diện canonical `python|python3|py <tệp>.py` KHÔNG CỜ cho hợp đồng hẹp của
# t34. Đây không phải parser shell; năm dạng lọt đã đo được khai ngay trong docstring,
# và không được nối regex ở packet này. Nợ "CI có chạy gate không" thuộc required
# status check được nêu ngay trong t34.
_CHAY_BO_TEST = __import__("re").compile(
    r"""(?<![\w.])(?:python3?|py)\s+["']?\S*lease_publish_test\.py["']?""")


def _goi_actionlint_gia(dich, ver, than):
    """Dựng một gói `.tar.gz` chứa `actionlint` GIẢ. `than=None` ⇒ gói KHÔNG có binary.

    Dùng `tarfile` (thư viện chuẩn) chứ không gọi `tar` ngoài: ca này phải chạy được cả
    trên runner Windows, nơi bộ công cụ nén không giống Linux.
    """
    import io
    import tarfile
    goi = dich / f"actionlint_{ver}_gia.tar.gz"
    with tarfile.open(goi, "w:gz") as t:
        if than is None:
            b = b"day khong phai binary\n"
            ti = tarfile.TarInfo("DOC.txt")
            ti.size, ti.mode = len(b), 0o644
        else:
            b = than.encode("utf-8")
            ti = tarfile.TarInfo("actionlint")
            ti.size, ti.mode = len(b), 0o755
        t.addfile(ti, io.BytesIO(b))
    return goi


def _goi_actionlint_zip_gia(dich, ver):
    """Dựng ZIP chứa binary giả đúng bản, giữ mode executable cho đường `tar` dự phòng."""
    import zipfile
    goi = dich / f"actionlint_{ver}_gia.zip"
    info = zipfile.ZipInfo("actionlint")
    info.create_system = 3
    info.external_attr = 0o100755 << 16
    with zipfile.ZipFile(goi, "w") as z:
        z.writestr(info, f"#!/bin/sh\necho {ver}\n".encode("utf-8"))
    return goi


@ca
def t35_script_cai_actionlint_phai_TU_CHOI_ban_sai():
    """CHẠY THẬT `ops/cai_actionlint.sh` với `actionlint` GIẢ, và đòi nó TỪ CHỐI.

    VÌ SAO VIẾT LẠI (cross-review `#200`, codex, P2-2). Bản trước chỉ kiểm sự ĐỒNG HIỆN
    của vài token trên cùng một dòng `run`. Đo được — dựng lại đúng phản chứng đã ghi thì
    ca CŨ giết nó, nhưng phản chứng ấy chỉ trượt vì nó xoá luôn token `grep` mà phép lọc
    bấu vào; một no-op GIỮ token thì lọt sạch:

        printf '%s\\n' "$AL_VER" | grep -q . || true      -> 35/35 đạt, rc=0

    Dòng ấy KHÔNG hề so bản cài với bản ghim và KHÔNG bao giờ thất bại, mà ca cũ vẫn xanh.
    Đó là lần thứ ba cùng một hình dạng lỗi: *kiểm sự CÓ MẶT của chuỗi rồi tuyên là đã đo
    HÀNH VI*.

    Nên chữa ở TẦNG, không siết mẫu chuỗi lần thứ tư. Hành vi cài + đối chiếu nằm trong
    MỘT script chạy được; ca này CHẠY nó thật với `actionlint` giả và đọc `rc` TRỰC TIẾP
    từ tiến trình. Một script chạy được thì không thể xanh rỗng bằng cách viết lại chữ.

    Có CA DƯƠNG (bản đúng ⇒ nhận). Không có nó thì mọi ca âm đều có thể xanh chỉ vì script
    hỏng toàn tập — "luôn từ chối" cũng qua hết ca âm.
    """
    import os
    import re
    import shutil
    import subprocess
    import tempfile
    import yaml

    kich = HERE.parent / "ops" / "cai_actionlint.sh"
    bang(kich.is_file(),
         f"không thấy {kich} — hành vi cài `actionlint` phải nằm trong MỘT script chạy "
         f"được thì ca này mới đo được nó; không có script thì không có gì để đo")

    # FAIL-CLOSE khi thiếu công cụ, đúng lối `t33`: một cổng tự tắt lúc thiếu công cụ là
    # cổng không tồn tại đúng lúc nó cần nhất. Và KHÔNG `shutil.which` — xem #570.
    bash = _bash_cho_cai_actionlint()

    def chay(ver, goi, dich, them=None):
        mt = dict(os.environ)
        mt.update({"AL_VER": ver, "AL_DICH": str(dich), "AL_NEN": "Linux"})
        if goi is not None:
            mt["AL_GOI"] = str(goi)
            # PHẢI cấp băm của chính gói giả này. Không cấp thì script dừng ở cổng băm
            # (rc=9) TRƯỚC khi chạm logic bản-ghim — mọi ca âm bên dưới vẫn "đạt" mà
            # KHÔNG ĐO GÌ, đúng bệnh `t24`. Ca đo cổng băm nằm riêng ở `t37`.
            mt["AL_SHA256"] = _bam_tep(goi)
        mt.pop("GITHUB_PATH", None)     # đừng ghi vào PATH của runner khi đang đo
        if them:
            mt.update(them)
        r = subprocess.run([bash, str(kich)], env=mt, timeout=180,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        return r.returncode, (r.stdout or "")   # rc lấy TRỰC TIẾP từ tiến trình

    VER = "1.7.7"
    loi = []
    with tempfile.TemporaryDirectory() as tam:
        from pathlib import Path as _P
        tam = _P(tam)

        # ——— CA DƯƠNG: binary khai ĐÚNG bản ghim ⇒ phải NHẬN.
        rc, ra = chay(VER, _goi_actionlint_gia(tam, VER, f"#!/bin/sh\necho {VER}"),
                      tam / "d-dung")
        if rc != 0:
            loi.append(f"bản ĐÚNG mà script vẫn từ chối (rc={rc}) — ca âm bên dưới sẽ vô "
                       f"nghĩa vì 'luôn từ chối' cũng qua hết:\n{ra.strip()[:400]}")

        # ——— CA DƯƠNG 2: gói có tên KHÔNG CÓ DẤU CHẤM vẫn phải nhận.
        # Phản chứng của cross-review `#203` lượt 2: bản trước dựng tên cục bộ bằng
        # `${TEN_GOI##*.}`, mà khi đường dẫn không có dấu chấm thì phép mở rộng ấy trả lại
        # CẢ ĐƯỜNG DẪN (gồm `/`) ⇒ `cp` chết, rc=5, trên một tar HOÀN TOÀN HỢP LỆ.
        # `AL_GOI` được khai là "đường dẫn tới một gói có sẵn" — nó KHÔNG đòi tên phải có
        # phần mở rộng. Đây cũng là regression do chính lượt vá trước sinh ra.
        _g = _goi_actionlint_gia(tam, VER, f"#!/bin/sh\necho {VER}")
        _kd = tam / "goikhongduoi"
        _kd.write_bytes(_g.read_bytes())
        rc, ra = chay(VER, _kd, tam / "d-khongduoi")
        if rc != 0:
            loi.append(f"gói tên KHÔNG có dấu chấm mà script từ chối (rc={rc}) — tên tệp "
                       f"không phải hợp đồng, `AL_GOI` chỉ khai là một đường dẫn:"
                       f"\n{ra.strip()[:300]}")

        # ——— CA ÂM: mỗi ca là một kiểu 'đã cài' mà KHÔNG phải 'đã cài ĐÚNG BẢN'.
        AM = [
            ("bản SAI", f"#!/bin/sh\necho 0.0.0"),
            # đúng phản chứng codex lượt 1 (`fd76921`): rc=0, tên đúng, bản bịa
            ("giả kiểu `actionlint fake-0.0.0`", "#!/bin/sh\necho 'actionlint fake-0.0.0'"),
            ("rc=0 mà không in gì", "#!/bin/sh\nexit 0"),
            ("binary không chạy được", "#!/bin/sh\nexit 1"),
            ("gói KHÔNG có binary", None),
        ]
        for k, (ten, than) in enumerate(AM):
            rc, ra = chay(VER, _goi_actionlint_gia(tam, VER, than), tam / f"d-am{k}")
            if rc == 0:
                loi.append(f"`actionlint` giả ({ten}) mà script NHẬN (rc=0) — 'đã cài' "
                           f"không phải 'đã cài ĐÚNG BẢN'; cổng sẽ xanh RỖNG")

        # ——— `AL_VER` không phải X.Y.Z ⇒ từ chối, không âm thầm cài đại một bản nào đó.
        # `1x.2y.3z` … `1.2.3 ` la PHAN CHUNG cua cross-review #203: ban truoc dung glob
        # cua `case` (`[0-9]*.[0-9]*.[0-9]*`), ma trong glob `*` khop CA CHU CAI con `.`
        # la ky tu thuong — nen mot ban ghim khong phai so van qua cong (do duoc: rc=0).
        # Nay la regex day du; moi muc duoi day phai bi tu choi rc=2.
        for ban_xau in ("", "latest", "1.7", "1x.2y.3z", "1.2.3-rc1", "1.2.3/abc",
                        "1.2.3 ", " 1.2.3", "1.2.3.4", "v1.2.3"):
            rc, _ = chay(ban_xau, _goi_actionlint_gia(tam, VER, f"#!/bin/sh\necho {VER}"),
                         tam / f"d-ver{ban_xau or 'rong'}")
            if rc != 2:
                loi.append(f"`AL_VER={ban_xau!r}` không phải X.Y.Z mà script trả rc={rc} "
                           f"(phải là 2). rc=0 nghĩa là ghim trần — hôm nay xanh, mai đỏ, "
                           f"cây không đổi. rc khác 2 mà khác 0 cũng sai: mã thoát là thứ "
                           f"người gọi dùng để khẳng định LÝ DO từ chối, nêu nhầm mã thì "
                           f"họ khẳng định nhầm chuyện")

        # `mkdir` hỏng từng rơi thẳng qua `set -e` với rc=1 — trùng đúng mã của chính
        # suite khi có ca đỏ. Người gọi vì thế không phân biệt được hạ tầng cài đặt hỏng
        # với cổng nội dung đỏ. Đích là một tệp thường để tái hiện được cả khi chạy root.
        dich_la_tep = tam / "dich-la-tep"
        dich_la_tep.write_text("không phải thư mục\n", encoding="utf-8")
        rc, ra = chay(VER, _goi_actionlint_gia(
            tam, VER, f"#!/bin/sh\necho {VER}"), dich_la_tep)
        if rc != 12 or "khong tao duoc thu muc cai" not in ra:
            loi.append(f"`AL_DICH` là tệp phải trả rc=12 riêng cùng thông điệp phân "
                       f"biệt được, không được trùng rc=1 của suite: rc={rc}, "
                       f"output={ra.strip()[:300]!r}")

    # ——— GIỮ TẦNG: workflow chỉ gọi wrapper; wrapper gọi installer, không cài lại tại chỗ.
    goc = HERE.parent / ".github" / "workflows"
    if goc.is_dir():
        LAY_VE = ("curl", "wget", "choco install", "brew install", "go install")
        GOI_WRAPPER = {
            "bash ops/chay_lease_publish_test.sh",
            'bash "$NEO/ops/chay_lease_publish_test.sh"',
        }
        # PHẠM VI ĐO ĐƯỢC: regex neo `^`; ở nhánh `bash|sh` nó nhận đúng một token
        # lệnh dẫn đầu rồi đòi một token đường dẫn liền mạch (`exec` là nhánh phụ được
        # liệt kê riêng); `\S*` không vượt được khoảng trắng. Bốn dạng đã đo KHÔNG được
        # nhận diện và rơi vào `continue`:
        # `env AL_X=1 bash ops/chay_lease_publish_test.sh`;
        # `bash -c 'bash ops/chay_lease_publish_test.sh'`;
        # `command bash ops/chay_lease_publish_test.sh`; và
        # `bash ${{ github.workspace }}/ops/chay_lease_publish_test.sh` (biểu thức có
        # khoảng trắng). Hai đối chứng bị nhận diện rồi TỪ CHỐI đúng thiết kế là
        # `bash /đường/dẫn/tuyệt/đối/ops/chay_lease_publish_test.sh` và
        # `bash ${{github.workspace}}/ops/chay_lease_publish_test.sh` (không khoảng trắng).
        #
        # NỢ CÓ TÊN `PLAT-X5-nhan-dien-loi-goi-wrapper`: bốn dạng trên vẫn được miễn
        # nghĩa vụ `AL_VER` ở tầng t35. Hậu quả bị chặn ở tầng sau vì
        # `ops/cai_actionlint.sh` vẫn `loi 2` khi thiếu `AL_VER` bất kể cú pháp gọi.
        # Nợ này cùng họ với việc đảo t34 thành danh sách cho phép và thuộc packet #209;
        # không mở regex nhận diện trong lượt vá hẹp này.
        GOI_WRAPPER_THUC_THI = re.compile(
            r"^(?:(?:bash|sh)\s+|exec\s+(?:(?:bash|sh)\s+)?|)"
            r"[\"']?\S*chay_lease_publish_test\.sh[\"']?(?:\s|$)")
        for tep in sorted(goc.glob("*.yml")) + sorted(goc.glob("*.yaml")):
            d = yaml.safe_load(tep.read_text(encoding="utf-8")) or {}
            for job in (d.get("jobs") or {}).values():
                for b in (job.get("steps") or []):
                    than = b.get("run")
                    if not isinstance(than, str):
                        continue
                    ten = f"{tep.name}:{b.get('name') or '(không tên)'}"
                    dong_lenh = _dong_lenh(than)
                    if any("actionlint" in x and any(k in x for k in LAY_VE)
                           for x in dong_lenh):
                        loi.append(f"{ten}: cài `actionlint` TẠI CHỖ. Chép logic ra khỏi "
                                   f"`ops/cai_actionlint.sh` là dựng lại đúng chỗ hỏng — "
                                   f"bản chép sẽ không được ca này chạy thử. Gọi wrapper.")
                    goi_wrapper = [x.strip() for x in dong_lenh
                                   if GOI_WRAPPER_THUC_THI.search(x.strip())]
                    if not goi_wrapper:
                        continue
                    ngoai_danh_sach = [x for x in goi_wrapper if x not in GOI_WRAPPER]
                    if ngoai_danh_sach:
                        loi.append(f"{ten}: có lệnh gọi wrapper ngoài danh sách canonical "
                                   f"{ngoai_danh_sach}. Allowlist này gác nghĩa vụ "
                                   f"`AL_VER`, nên ngoài danh sách phải bị từ chối chứ "
                                   f"không được miễn")
                    ban = str((b.get("env") or {}).get("AL_VER") or "")
                    if not re.fullmatch(r"\d+\.\d+\.\d+", ban):
                        loi.append(f"{ten}: gọi wrapper mà thiếu `AL_VER` "
                                   f"dạng X.Y.Z (được {ban!r})")

    bang(not loi, "cài `actionlint` không cưỡng chế bản ghim:\n  - " + "\n  - ".join(loi))


@ca
def t36_giai_nen_phai_chiu_duoc_duong_dan_mang_DAU_HAI_CHAM():
    """`cai_actionlint.sh` phải giải nén được khi ĐƯỜNG DẪN GÓI mang dấu hai chấm.

    ĐÂY LÀ CA SINH RA TỪ MỘT LƯỢT WINDOWS ĐỎ THẬT, không phải từ suy đoán. Lượt
    `workflow_dispatch` `32368383473` (job `96423003418`, head `d0acd79f`) làm chân
    `gate (windows-latest)` ĐỎ ở bước `lease-publish selftest`:

        tar (child): Cannot connect to C: resolve failed
        cai_actionlint: giai nen tar that bai

    GNU tar đọc đối số của `-f` theo dạng `HOST:PATH` khi có dấu hai chấm đứng TRƯỚC dấu
    gạch chéo đầu tiên. Trên Windows đường dẫn mang ký tự ổ đĩa (`C:...`) nên tar không mở
    tệp — nó đi PHÂN GIẢI TÊN MÁY `C`. Hệ quả: trên Windows script LUÔN trả rc=5, tức
    installer không bao giờ cài được.

    VÌ SAO CA NÀY ĐO ĐƯỢC TRÊN CẢ HAI NỀN, không phải "bỏ qua trên POSIX":

      • Windows: đường dẫn tuyệt đối TỰ NÓ mang ký tự ổ đĩa ⇒ chạy bản thường là đã đo
        đúng ca đó, không cần dựng gì thêm.
      • POSIX: dựng một đường dẫn TƯƠNG ĐỐI mà đoạn đầu chứa dấu hai chấm (`C:sub/goi...`).
        Cùng LUẬT của tar, nên nó tái lập đúng lỗi Windows — đã đo: bản chưa vá trả rc=5
        kèm y nguyên câu `Cannot connect to C:`.

    Không nền nào rơi vào nhánh "không thấy thì bỏ qua" — đó là bệnh `t24` mà kho đã ghi sổ.

    ĐỘT BIẾN ĐÃ CHẠY (đưa dòng giải nén về dạng cũ `tar -xzf "$TEN_GOI" -C "$AL_DICH"`):
    bản vá rc=0, bản đột biến **rc=5** kèm đúng câu lỗi trên ⇒ ca này CÓ RĂNG.
    """
    import os
    import shutil
    import subprocess
    import tempfile
    from pathlib import Path as _P

    kich = HERE.parent / "ops" / "cai_actionlint.sh"
    bang(kich.is_file(), f"không thấy {kich}")
    bash = _bash_cho_cai_actionlint()

    VER = "1.7.7"
    with tempfile.TemporaryDirectory() as tam:
        tam = _P(tam)
        if os.name == "nt":
            # Windows: KHÔNG dựng được thư mục tên `C:sub` (dấu hai chấm là ký tự cấm),
            # nhưng cũng KHÔNG cần — đường dẫn tuyệt đối ở đây đã mang sẵn ký tự ổ đĩa.
            goi = _goi_actionlint_gia(tam, VER, f"#!/bin/sh\necho {VER}")
            cwd = None
            mo_ta = f"đường dẫn tuyệt đối Windows (mang ký tự ổ đĩa): {goi}"
        else:
            thu_muc = tam / "C:sub"
            thu_muc.mkdir(parents=True, exist_ok=True)
            goi = _goi_actionlint_gia(thu_muc, VER, f"#!/bin/sh\necho {VER}")
            goi = _P("C:sub") / goi.name        # TƯƠNG ĐỐI: dấu hai chấm TRƯỚC gạch chéo
            cwd = tam
            mo_ta = f"đường dẫn tương đối có dấu hai chấm ở đoạn đầu: {goi}"

        dich = tam / "dich"
        mt = dict(os.environ)
        goi_that = (tam / "C:sub" / goi.name) if cwd else goi
        mt.update({"AL_VER": VER, "AL_DICH": str(dich),
                   "AL_NEN": "Windows" if os.name == "nt" else "Linux",
                   "AL_GOI": str(goi), "AL_SHA256": _bam_tep(goi_that)})
        mt.pop("GITHUB_PATH", None)
        r = subprocess.run([bash, str(kich)], env=mt, cwd=(str(cwd) if cwd else None),
                           timeout=180, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, text=True)
        rc, ra = r.returncode, (r.stdout or "")   # rc TRỰC TIẾP từ tiến trình

    bang(rc == 0,
         f"gói ở {mo_ta} mà script KHÔNG giải nén được (rc={rc}). Đây đúng lỗi đã làm "
         f"`gate (windows-latest)` đỏ ở lượt 32368383473 — tar hiểu `C:` là TÊN MÁY, "
         f"không phải ổ đĩa:\n{ra.strip()[:400]}")


@ca
def t37_goi_tai_ve_phai_qua_DOI_CHIEU_BAM_truoc_khi_chay():
    """Gói `actionlint` phải khớp băm ghim TRƯỚC khi được giải nén và CHẠY.

    VÌ SAO (cross-review `#203`, codex, P2-3). Trước đó thứ duy nhất "xác minh" gói tải từ
    mạng là `actionlint --version` — tức **binary TỰ KHAI**. Một binary bị thay thế chỉ cần
    tự in `1.7.7` là qua. Mà nó chạy trong job có `contents: write` + `issues: write`:

        rg -n 'sha256|checksum|shasum|cosign' ops/cai_actionlint.sh   ->  rc=1 (KHÔNG CÓ)

    BỐN TRẠNG THÁI, mã thoát RIÊNG để người gọi khẳng định được LÝ DO:

        không có băm để đối chiếu   -> rc=8, và DỪNG TRƯỚC KHI TẢI
        thiếu cả sha256sum lẫn shasum -> rc=8 (fail-close, không bỏ qua)
        băm không khớp              -> rc=9
        băm khớp                    -> rc=0

    CA DƯƠNG là bắt buộc: một cổng "luôn từ chối" cũng qua hết ca âm.

    VÌ SAO CA NÀY PHẢI ĐỨNG RIÊNG. `t35`/`t36` **tự cấp** `AL_SHA256` cho gói giả chúng
    dựng — bắt buộc, nếu không chúng dừng ở cổng băm và mọi ca âm của chúng "đạt" mà không
    đo gì. Nghĩa là hai ca ấy **cố ý đi vòng qua** cổng băm, nên cổng ấy phải có ca đo
    riêng — chỗ này.

    GIỚI HẠN, khai thẳng: băm ghim được tính TỪ CHÍNH bản tải về lúc ghim, không phải từ một
    trust root độc lập. Nó chặn DRIFT và THAY THẾ VỀ SAU — đúng mức bảo đảm của
    `pip install X==1.2.3`, KHÔNG hơn.
    """
    import os
    import shutil
    import subprocess
    import tempfile
    from pathlib import Path as _P

    kich = HERE.parent / "ops" / "cai_actionlint.sh"
    bang(kich.is_file(), f"không thấy {kich}")
    bash = _bash_cho_cai_actionlint()

    VER = "1.7.7"
    loi = []

    def chay(dich, **them):
        mt = dict(os.environ)
        mt.update({"AL_VER": VER, "AL_DICH": str(dich), "AL_NEN": "Linux"})
        mt.pop("AL_SHA256", None)
        mt.update({k: str(v) for k, v in them.items()})
        mt.pop("GITHUB_PATH", None)
        r = subprocess.run([bash, str(kich)], env=mt, timeout=180,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        return r.returncode, (r.stdout or "")

    with tempfile.TemporaryDirectory() as tam:
        tam = _P(tam)
        goi = _goi_actionlint_gia(tam, VER, f"#!/bin/sh\necho {VER}")
        bam = _bam_tep(goi)

        # ——— CA DƯƠNG: băm khớp ⇒ NHẬN.
        rc, ra = chay(tam / "d-dung", AL_GOI=goi, AL_SHA256=bam)
        if rc != 0:
            loi.append(f"băm KHỚP mà script vẫn từ chối (rc={rc}) — mọi ca âm dưới đây "
                       f"sẽ vô nghĩa vì 'luôn từ chối' cũng qua hết:\n{ra.strip()[:300]}")

        # ——— băm SAI ⇒ rc=9.
        rc, _ = chay(tam / "d-sai", AL_GOI=goi, AL_SHA256="0" * 64)
        if rc != 9:
            loi.append(f"băm KHÔNG khớp mà script trả rc={rc} (phải 9) — gói lạ vẫn được "
                       f"giải nén và CHẠY")

        # ——— gói lạ, KHÔNG kèm băm ⇒ mốc so là băm CHÍNH THỨC ⇒ rc=9.
        rc, _ = chay(tam / "d-khongbam", AL_GOI=goi)
        if rc != 9:
            loi.append(f"gói lạ không kèm `AL_SHA256` mà script trả rc={rc} (phải 9). "
                       f"Bản cài offline cũng phải là đúng artefact chính thức.")

        # ——— bản KHÔNG có băm ghim ⇒ rc=8, và phải DỪNG TRƯỚC KHI TẢI.
        rc, ra = chay(tam / "d-chuaghim", AL_VER="9.9.9")
        if rc != 8:
            loi.append(f"`AL_VER=9.9.9` chưa ghim băm mà script trả rc={rc} (phải 8)")
        if "tai ve that bai" in ra:
            loi.append("script ĐÃ TẢI rồi mới phát hiện không có băm — phải dừng TRƯỚC: "
                       "tải một thứ không đối chiếu được rất dễ thành 'thôi cài đại'")

    bang(not loi, "cổng đối chiếu băm không cưỡng chế:\n  - " + "\n  - ".join(loi))


@ca
def t38_bam_phai_dung_khi_DUONG_DAN_co_dau_cheo_nguoc():
    r"""Cổng băm phải cho kết quả ĐÚNG khi đường dẫn gói chứa dấu chéo ngược.

    CA NÀY SINH TỪ MỘT LƯỢT WINDOWS ĐỎ THẬT — và đỏ vì CHÍNH BẢN VÁ băm vừa thêm, không
    phải vì gói sai. Lượt `32371632630`, job `96433323614`, bước `cài actionlint`:

        cai_actionlint: bam goi KHONG KHOP:
          mong '7f12f1801bca3d480d67aaf7774f4c2a6359a3ca8eebe382c95c10c9704aa731'
          thuc '\7f12f1801bca3d480d67aaf7774f4c2a6359a3ca8eebe382c95c10c9704aa731'
                ^ đúng MỘT ký tự: một dấu chéo ngược ở đầu

    Băm khớp từng ký tự còn lại. Thứ sai là **định dạng đầu ra của `sha256sum`**: GNU
    coreutils THOÁT cả dòng khi TÊN TỆP chứa dấu chéo ngược (hoặc xuống dòng) — nó thêm
    `\` vào đầu dòng rồi escape tên. Đường dẫn runner Windows là `D:\a\_temp/...` nên
    dính đúng luật ấy, và `cut -d" " -f1` lấy về băm CÓ THÊM một ký tự.

    Cùng họ với những bài học escaping đã ghi trong `CLAUDE.md`: **một lớp mà ta không coi
    là lớp**. Ở đây lớp ấy là định dạng đầu ra của chính công cụ đo.

    Chữa: đọc từ **stdin** (`sha256sum < tệp`) — đầu ra không còn tên tệp thì không còn gì
    để thoát. Không phải "gỡ dấu chéo ở đầu": đó lại là vá theo HÌNH DẠNG, mà tên tệp có
    xuống dòng còn làm đầu ra méo kiểu khác.

    ĐO ĐƯỢC TRÊN LINUX, không cần Windows: dấu chéo ngược là ký tự HỢP LỆ trong tên tệp
    POSIX, nên `sha256sum 'co\cheo.bin'` in ra `\<băm>` y hệt. Ca này dựng đúng tình
    huống đó.
    """
    import os
    import shutil
    import subprocess
    import tempfile
    from pathlib import Path as _P

    kich = HERE.parent / "ops" / "cai_actionlint.sh"
    bang(kich.is_file(), f"không thấy {kich}")
    bash = _bash_cho_cai_actionlint()

    VER = "1.7.7"
    with tempfile.TemporaryDirectory() as tam:
        tam = _P(tam)
        goc = _goi_actionlint_gia(tam, VER, f"#!/bin/sh\necho {VER}")
        if os.name == "nt":
            # KHÔNG bỏ qua trên Windows. Dấu chéo ngược là DẤU PHÂN CÁCH ở đó, nên MỌI
            # đường dẫn tuyệt đối đã mang sẵn nó (`D:\\a\\_temp\\...`) — tức chạy bản
            # thường ở đây LÀ đo đúng ca cần đo, không cần dựng tên tệp dị.
            #
            # Bản đầu của ca này viết `bang(True, ""); return` cho Windows. SAI, và sai
            # đúng kiểu kho đã ghi sổ: harness này KHÔNG có cơ chế bỏ qua — một ca
            # `return` sớm vẫn được đếm là ĐẠT. Nghĩa là trên chính nền sinh ra lỗi, ca
            # canh nó lại không đo gì mà vẫn xanh. Đúng bệnh `t24`.
            goi = goc
        else:
            # POSIX: dấu chéo ngược là ký tự HỢP LỆ trong TÊN tệp, nên dựng thẳng một tên
            # có nó — cùng luật thoát của coreutils, tái lập đúng lỗi Windows.
            goi = tam / "co\\cheo.tar.gz"
            goi.write_bytes(goc.read_bytes())

        mt = dict(os.environ)
        mt.update({"AL_VER": VER, "AL_DICH": str(tam / "dich"), "AL_NEN": "Linux",
                   "AL_GOI": str(goi), "AL_SHA256": _bam_tep(goi)})
        mt.pop("GITHUB_PATH", None)
        r = subprocess.run([bash, str(kich)], env=mt, timeout=180,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        rc, ra = r.returncode, (r.stdout or "")

    bang(rc == 0,
         f"[nền={os.name}] gói ĐÚNG ở đường dẫn có dấu chéo ngược mà cổng băm từ chối "
         f"(rc={rc}). `sha256sum`"
         f" thoát cả dòng khi tên tệp chứa `\\` — đọc từ stdin thì đầu ra không có tên tệp. "
         f"Đây đúng lỗi đã làm `gate (windows-latest)` đỏ ở lượt 32371632630:\n"
         f"{ra.strip()[:400]}")


@ca
def t39_loai_archive_phai_do_NOI_DUNG_khong_doan_tu_ten():
    """ZIP hợp lệ phải chạy được khi tên không đuôi hoặc dùng `.ZIP` viết hoa.

    Finding vòng 3 đo cả hai ca đều rc=5 vì script cũ dùng `*.zip`, rồi mặc định mọi tên
    còn lại là tar.gz. Hợp đồng `AL_GOI` chỉ nói "đường dẫn tới một gói"; tên tệp không
    phải trường loại. Ca này dùng CÙNG byte ZIP dưới hai tên để buộc phân loại theo magic
    bytes. Có ca dương thật: binary sau giải nén phải chạy và khai đúng bản.
    """
    import os
    import shutil
    import subprocess
    import tempfile
    from pathlib import Path as _P

    kich = HERE.parent / "ops" / "cai_actionlint.sh"
    bang(kich.is_file(), f"không thấy {kich}")
    bash = _bash_cho_cai_actionlint()

    VER = "1.7.7"
    loi = []
    with tempfile.TemporaryDirectory() as tam:
        tam = _P(tam)
        goc = _goi_actionlint_zip_gia(tam, VER)
        for k, ten in enumerate(("goi-khong-duoi", "goi.ZIP")):
            goi = tam / ten
            goi.write_bytes(goc.read_bytes())
            mt = dict(os.environ)
            mt.update({"AL_VER": VER, "AL_DICH": str(tam / f"dich-{k}"),
                       "AL_NEN": "Linux", "AL_GOI": str(goi),
                       "AL_SHA256": _bam_tep(goi)})
            mt.pop("GITHUB_PATH", None)
            r = subprocess.run([bash, str(kich)], env=mt, timeout=180,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            rc, ra = r.returncode, (r.stdout or "")  # rc TRỰC TIẾP từ tiến trình
            if rc != 0:
                loi.append(f"ZIP tên {ten!r} bị từ chối rc={rc}: {ra.strip()[:300]}")
    bang(not loi, "loại archive vẫn bị suy từ suffix:\n  - " + "\n  - ".join(loi))


@ca
def t40_wrapper_phai_CAI_truoc_CHAY_va_giu_rc_cua_bo_test():
    """Chạy wrapper thật trong cây tạm và đo trạng thái, không mô phỏng kịch bản.

    Cây tạm chứa chính wrapper + installer, một gói actionlint có executable chạy thật,
    và một selftest nhỏ tự tìm/call binary trên PATH rồi ghi marker. Ba hậu điều có răng:

    * gói đúng: test thấy binary đúng bản và marker xuất hiện;
    * installer sai bản: rc=7 và marker KHÔNG xuất hiện — test không chạy trước/cạnh lỗi;
    * test chủ động rc=23: wrapper trả đúng 23 — không pipeline nuốt mã thoát.

    POSIX dùng shell stub trạng thái; Windows đóng gói lại chính `actionlint.exe` PE mà
    wrapper ngoài vừa cài — không bắt Windows chạy một shell script không đuôi rồi gọi đó
    là binary Windows. Cả hai nền đều đòi executable được tìm thấy nằm TRONG `AL_DICH`,
    nên xoá installer hoặc quên cập nhật PATH vẫn chết kể cả mồi tình cờ cùng phiên bản.

    PATH mồi được ghép BÊN TRONG Bash bằng `:`, không dùng `os.pathsep` của Python host
    cho một giá trị mà Bash sẽ tiêu thụ. Mỗi nhánh trên đều chạy đủ ba hậu điều; không có
    nhánh return/skip được harness đếm thành đạt.
    """
    import os
    import shutil
    import subprocess
    import tempfile
    from pathlib import Path as _P

    bash = _bash_cho_cai_actionlint()
    wrapper = HERE.parent / "ops" / "chay_lease_publish_test.sh"
    installer = HERE.parent / "ops" / "cai_actionlint.sh"
    bang(wrapper.is_file(), f"không thấy {wrapper}")
    bang(installer.is_file(), f"không thấy {installer}")

    VER = "1.7.7"
    with tempfile.TemporaryDirectory() as tam:
        goc = _P(tam)
        ops = goc / "ops"
        ops.mkdir()
        shutil.copy2(wrapper, ops / wrapper.name)
        shutil.copy2(installer, ops / installer.name)
        (ops / "lease_publish_test.py").write_text(
            """import os, pathlib, shutil, subprocess, sys

def sai(ly_do):
    print(f"T40_STUB_SAI: {ly_do}", file=sys.stderr)
    raise SystemExit(32)

duong = shutil.which("actionlint")
if not duong:
    sai("shutil.which khong tim thay actionlint")
dich = pathlib.Path(os.environ["AL_DICH"]).resolve()
binary = pathlib.Path(duong).resolve()
try:
    binary.relative_to(dich)
except ValueError:
    sai(f"PATH tro ra ngoai AL_DICH: {binary} (dich {dich})")
p = subprocess.run([duong, "--version"], capture_output=True, text=True)
lines = p.stdout.strip().splitlines()
if p.returncode != 0 or not lines or lines[0] != os.environ["AL_VER"]:
    sai(f"version rc={p.returncode}, stdout={p.stdout!r}, stderr={p.stderr!r}")
pathlib.Path(os.environ["WRAPPER_MARKER"]).write_text("da-chay", encoding="utf-8")
print("WRAPPER_SELFTEST_OK")
raise SystemExit(int(os.environ.get("WRAPPER_TEST_RC", "0")))
""", encoding="utf-8")

        # Đồ mồi mô phỏng TRẠNG THÁI "PATH đã có actionlint ở nơi khác", không trả lời
        # theo lượt. Stub còn đòi đường tìm được thuộc AL_DICH, nên mồi cùng phiên bản
        # cũng không thể diễn kịch để làm ca xanh.
        path_ban_dau = goc / "path-ban-dau"
        path_ban_dau.mkdir()
        if os.name == "nt":
            # Nhánh Windows đo executable Windows THẬT. Wrapper ngoài phải vừa cài nó
            # để t33 chạy được; thiếu/không đúng bản là ĐỎ, không return sớm.
            actionlint_ngoai = shutil.which("actionlint")
            bang(actionlint_ngoai and actionlint_ngoai.lower().endswith(".exe"),
                 "[Windows] KHÔNG ĐO ĐƯỢC: PATH không có `actionlint.exe` thật")
            do_ban = subprocess.run([actionlint_ngoai, "--version"],
                                    capture_output=True, text=True)
            dong = (do_ban.stdout or "").strip().splitlines()
            bang(do_ban.returncode == 0 and dong and dong[0] == VER,
                 f"[Windows] actionlint ngoài không đúng {VER}: rc={do_ban.returncode}, "
                 f"stdout={do_ban.stdout!r}, stderr={do_ban.stderr!r}")

            # Gói dương chứa đúng loại file của archive chính thức: `actionlint.exe`.
            # Copy PE thật thay vì đổi đuôi một shell script rồi giả định Windows chạy nó.
            import zipfile
            goi_dung = goc / "actionlint-windows-dung.zip"
            with zipfile.ZipFile(goi_dung, "w", zipfile.ZIP_DEFLATED) as z:
                z.write(actionlint_ngoai, "actionlint.exe")
            shutil.copy2(actionlint_ngoai, path_ban_dau / "actionlint.exe")
            nen = "Windows"
        else:
            moi = path_ban_dau / "actionlint"
            moi.write_text("#!/bin/sh\necho 0.0.0\n", encoding="utf-8")
            moi.chmod(0o755)
            thu_muc_dung = goc / "goi-dung"
            thu_muc_dung.mkdir()
            goi_dung = _goi_actionlint_gia(
                thu_muc_dung, VER, f"#!/bin/sh\necho {VER}")
            nen = "Linux"

        mt_goc = dict(os.environ, AL_VER=VER, AL_NEN=nen)
        mt_goc.pop("GITHUB_PATH", None)

        # `subprocess` đầu tiên cần PATH native để tìm Git Bash; chỉ sau khi đã ở TRONG
        # Bash mới ghép mồi bằng dấu `:`. `exec` giữ rc wrapper làm rc trực tiếp của r.
        lenh_wrapper = r"""set -euo pipefail
moi="$1"
wrapper="$2"
bash_that="$3"
if command -v cygpath >/dev/null 2>&1; then
  moi="$(cygpath -u "$moi")"
  wrapper="$(cygpath -u "$wrapper")"
  bash_that="$(cygpath -u "$bash_that")"
fi
export PATH="$moi:$PATH"
exec "$bash_that" "$wrapper"
"""

        def chay(goi, dich, marker, rc_test=None, ver=VER):
            mt = dict(mt_goc, AL_GOI=str(goi), AL_DICH=str(dich),
                      AL_SHA256=_bam_tep(goi), WRAPPER_MARKER=str(marker), AL_VER=ver)
            if rc_test is not None:
                mt["WRAPPER_TEST_RC"] = str(rc_test)
            r = subprocess.run(
                [bash, "-c", lenh_wrapper, "t40", str(path_ban_dau),
                 str(ops / wrapper.name), bash],
                cwd=goc, env=mt, timeout=180, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, text=True)
            return r.returncode, (r.stdout or "")

        marker_dung = goc / "marker-dung"
        rc, ra = chay(goi_dung, goc / "dich-dung", marker_dung)
        bang(rc == 0 and marker_dung.is_file()
             and marker_dung.read_text(encoding="utf-8") == "da-chay"
             and "WRAPPER_SELFTEST_OK" in ra,
             f"wrapper không cài rồi chạy test thật: rc={rc}, marker={marker_dung.exists()}:\n"
             f"{ra.strip()[:400]}")

        if os.name == "nt":
            # Cùng PE khai 1.7.7 nhưng hợp đồng đòi 0.0.0: trạng thái sai, không phải
            # mock trả lời theo số lượt. Installer phải tự đo mismatch và trả 7.
            goi_sai, ver_sai = goi_dung, "0.0.0"
        else:
            thu_muc_sai = goc / "goi-sai"
            thu_muc_sai.mkdir()
            goi_sai = _goi_actionlint_gia(
                thu_muc_sai, VER, "#!/bin/sh\necho 0.0.0")
            ver_sai = VER
        marker_sai = goc / "marker-sai"
        rc, ra = chay(goi_sai, goc / "dich-sai", marker_sai, ver=ver_sai)
        bang(rc == 7 and not marker_sai.exists(),
             f"installer sai phải dừng TRƯỚC selftest: rc={rc}, "
             f"marker={marker_sai.exists()}:\n{ra.strip()[:400]}")

        marker_rc = goc / "marker-rc"
        rc, ra = chay(goi_dung, goc / "dich-rc", marker_rc, rc_test=23)
        bang(rc == 23 and marker_rc.exists(),
             f"wrapper nuốt rc selftest: chờ 23, được {rc}, marker={marker_rc.exists()}:\n"
             f"{ra.strip()[:400]}")
# `t42` ĐÃ BỊ GỠ ở lượt vá thứ hai — có chủ đích, không phải quên. Nó khẳng định "docstring
# của `t34` có chứa chuỗi X", tức MỘT LỜI KHAI VỀ MỘT LỜI KHAI. Ba lượt liên tiếp cho cùng một
# hình dạng lỗi: cross-review 1 tìm được đột biến nới regex mà nó không bắt; bản vá cho nó lại
# đẻ ra hai docstring TỰ MÂU THUẪN với chính mã vừa viết cộng một con số chết ngay trong commit
# sinh ra nó; cross-review 2 lại tìm được đột biến siết regex mà nó vẫn không bắt.
#
# `CLAUDE.md` nói thẳng về đúng tình huống này: "cùng một hình dạng lặp ba lần trở lên thì câu
# hỏi đúng là CÓ NÊN LÀM VIỆC NÀY KHÔNG, không phải VÁ THẾ NÀO". Người giữ kho quyết bỏ.
#
# NỢ CÒN LẠI, khai thẳng chứ không giả vờ đã xong: mục tiêu gốc — canh cho lời khai phạm vi
# của `t34` không trôi — VẪN CHƯA CÓ CỔNG NÀO. Xem `ops/NO_KY_THUAT.md` §11.
#
# `t42` bên dưới được GIỮ vì nó khác loại: nó đo QUAN HỆ GIỮA HAI TỆP, tức một SỰ KIỆN, không
# phải một câu chữ ai đó gõ vào docstring.


# Marker `NỢ CÓ TÊN` trong workflow, và tiêu đề mục trong sổ nợ. Cố ý HAI mẫu riêng và cả hai
# đều bó vào ĐÚNG hình dạng đang dùng: marker chỉ nhận khi đứng trong một dòng CHÚ THÍCH, mục
# chỉ nhận khi là TIÊU ĐỀ `## <số>.`. Không bó thì một câu văn xuôi có chữ "NỢ CÓ TÊN" — như
# chính các câu giải thích trong hai tệp ấy — sẽ bị đếm nhầm, và cổng lại thành cổng nói dối.
# Marker phải đứng NGAY SAU dấu chú thích — `^\s*#\s*NỢ CÓ TÊN`, không cho chữ tuỳ ý chen
# vào giữa. Bản trước dùng `^\s*#.*NỢ CÓ TÊN` nên một CÂU VĂN XUÔI có nhắc cụm ấy cũng bị nhận
# làm marker; cross-review 2 đo được: chèn một dòng giải thích vào `ci.yml` là `t43` ĐỎ oan.
# Một cổng báo động giả là cổng sẽ bị tắt, rồi cả ca chết theo.
_MARKER_NO = __import__("re").compile(r"^\s*#\s*NỢ CÓ TÊN\s*:?\s*`([^`]+)`")
_MUC_SO_NO = __import__("re").compile(r"^##\s*\d+\.\s*`([^`]+)`")
# BACKLINK: mục sổ nợ TỰ KHAI nó là nhà của một marker trong mã. Chỉ mục có dòng này mới bị
# đòi hai chiều — §1–§8 không có backlink nên không báo động giả, đúng lý do đã hạ `t43` xuống
# một chiều ở lượt trước; nay giữ được cả hai chiều mà KHÔNG ép đối xứng lên toàn sổ.
_BACKLINK_NO = __import__("re").compile(r"^\*\*marker:\*\*\s*`([^`]+)`\s+trong\s+`([^`]+)`")


@ca
def t42_marker_NO_CO_TEN_va_muc_so_no_phai_khop_HAI_CHIEU():
    """Nợ được ĐẶT TÊN trong mã phải có nhà trong sổ, và mục đã khai backlink phải còn marker.

    VÌ SAO CÓ CA NÀY — cross-review lượt 1 (codex, P2): tiêu chí `2 = 2` mà packet tự đặt ra
    chỉ là một ẢNH CHỤP. Thêm marker thứ ba vào `ci.yml` mà không thêm mục ⇒ mọi cổng vẫn
    xanh. Một nợ mới sinh ra là một nợ KHÔNG AI ĐỌC.

    BA LỖ CỦA BẢN ĐẦU, cross-review lượt 2 đo được, nay đã vá — ghi cả ba vì mỗi cái là một
    kiểu thua khác nhau:

    1. **Một chiều làm mất tín hiệu khi marker BỊ GỠ.** Gỡ `PLAT-X5-required-status-check`
       khỏi `ci.yml` mà giữ nguyên §9 ⇒ `marker − sổ = ∅`, suite `43/43`, KHÔNG AI BẮT. Chiều
       nghịch không thể ép lên toàn sổ (§1–§8 là nợ thật, không có marker), nên lời giải là
       **backlink**: mục nào TỰ KHAI mình là nhà của một marker thì mới bị đòi hai chiều.
    2. **Nhận nhầm văn xuôi.** `^\s*#.*NỢ CÓ TÊN` cho phép chữ tuỳ ý chen trước cụm, nên một
       dòng giải thích cũng thành marker. Nay neo ngay sau `#`.
    3. **`set` xoá dấu vết trùng.** Tên ca hứa "ĐÚNG MỘT mục" nhưng `set` biến hai tiêu đề
       cùng ID thành một ⇒ chỉ kiểm được "ít nhất một". Nay đếm bằng `Counter`.

    PHẠM VI, khai thẳng: ca này chỉ đo `.github/workflows/ci.yml` ↔ `ops/NO_KY_THUAT.md`. Nợ
    đặt tên ở tệp khác KHÔNG được canh. Đây là tập đã ĐO, không phải lời hứa về mọi nơi.

    ĐỘT BIẾN LÀM CA NÀY ĐỎ: thêm marker không có nhà · GỠ một marker mà mục vẫn khai backlink
    · thêm mục thứ hai trùng ID. VÀ MỘT CA ÂM PHẢI XANH: chèn câu văn xuôi có cụm `NỢ CÓ TÊN`.
    """
    import collections
    goc = HERE.parent
    wf = goc / ".github" / "workflows" / "ci.yml"
    so = goc / "ops" / "NO_KY_THUAT.md"
    if not wf.is_file() or not so.is_file():
        bang(not (goc / ".git").exists(),
             f"kho thật mà thiếu {wf} hoặc {so} — ca này sẽ xanh mà không đo gì")
        return
    trong_ma = {m.group(1) for d in wf.read_text(encoding="utf-8").splitlines()
                if (m := _MARKER_NO.match(d))}
    dong_so = so.read_text(encoding="utf-8").splitlines()
    dem_muc = collections.Counter(m.group(1) for d in dong_so if (m := _MUC_SO_NO.match(d)))
    backlink = {m.group(1): m.group(2) for d in dong_so if (m := _BACKLINK_NO.match(d))}

    trung = sorted(k for k, n in dem_muc.items() if n > 1)
    bang(not trung,
         f"sổ nợ có mục TRÙNG ID: {trung}. Hai mục cùng tên là hai bản ghi cùng tranh làm nhà "
         f"của một khoản nợ — người đọc không biết bản nào có hiệu lực.")

    thieu_nha = sorted(trong_ma - set(dem_muc))
    bang(not thieu_nha,
         f"nợ ĐƯỢC ĐẶT TÊN trong `ci.yml` mà KHÔNG có mục trong `ops/NO_KY_THUAT.md`: "
         f"{thieu_nha}. Nợ có tên mà không có nhà là nợ KHÔNG AI ĐỌC — thêm mục, đừng gỡ marker.")

    mat_marker = sorted(k for k in backlink if k not in trong_ma)
    bang(not mat_marker,
         f"mục sổ nợ KHAI backlink tới marker mà marker ấy KHÔNG CÒN trong `ci.yml`: "
         f"{mat_marker}. Hoặc nợ đã trả mà mục chưa đóng, hoặc marker bị gỡ nhầm. Đừng làm ca "
         f"này im bằng cách xoá dòng backlink — đó là xoá đúng thứ đang canh.")


@ca
def t43_PR_phai_CHAN_va_neu_pull_requests():
    ex, _ = _goi_lop_gh(GhGia({55: "pr"}), "kiem_github", lease_mau(),
                        env_them=ENV_GITHUB, bo_qua=("_kiem_comment_da_co",))
    bang(ex and ex.ma == RC_NOI_DUNG and "pull-requests" in ex.thong_diep,
         f"PR không bị chặn đúng lý do: {ex}")


@ca
def t44_loi_do_loai_phai_CHAN_khong_dang():
    gh = GhGia({55: "loi"})
    ex, _ = _goi_lop_gh(gh, "kiem_github", lease_mau(), env_them=ENV_GITHUB,
                        bo_qua=("_kiem_comment_da_co",))
    bang(ex and ex.ma == RC_NOI_DUNG and "KHÔNG ĐO ĐƯỢC" in ex.thong_diep
         and "nguyên nhân có thể" in ex.thong_diep
         and "phỏng đoán, không phải phép đo" in ex.thong_diep,
         f"fail-open hoặc khai quá phép đo: {ex}")


@ca
def t45_ISSUE_phai_QUA_lop_do_loai():
    ex, _ = _goi_lop_gh(GhGia(), "kiem_github", lease_mau(), env_them=ENV_GITHUB)
    bang(ex is None, f"chặn oan Issue: {ex}")


@ca
def t46_comment_da_co_thi_BO_QUA_xuyen_nhanh():
    lease, gh = lease_mau(lease_id="lease-lap"), GhGia()
    ex, mod = _goi_lop_gh(gh, "kiem_github", lease, env_them=ENV_GITHUB,
                          bo_qua=("_kiem_loai_so_hieu",))
    bang(ex is None, f"lượt đầu không đăng được: {ex}")
    gh.dang(55, mod.dung_than(lease, "ops/leases/l.yaml"))
    ex, _ = _goi_lop_gh(gh, "kiem_github", lease, env_them=ENV_GITHUB,
                        bo_qua=("_kiem_loai_so_hieu",))
    posts = [x for x in gh.calls if x[0] == "POST"]
    bang(ex and ex.ma == RC_DA_DANG and len(posts) == 1 and len(gh.comments[55]) == 1,
         f"lượt hai không thấy comment lượt một: posts={posts}, {ex}")


@ca
def t47_dau_lease_KHAC_khong_duoc_chan():
    comments = {55: [{"id": 1, "body": "**Lease `lease-10`**",
                      "user": {"login": "github-actions[bot]"}}]}
    ex, _ = _goi_lop_gh(GhGia(comments=comments), "_kiem_comment_da_co", "o/r",
                        lease_mau(lease_id="lease-1"), env_them=ENV_GITHUB)
    bang(ex is None, f"khớp substring lỏng đã chặn lease khác: {ex}")


@ca
def t48_loi_doc_comment_phai_CHAN_khong_dang():
    gh = GhGia(loi_comment={55})
    ex, _ = _goi_lop_gh(gh, "_kiem_comment_da_co", "o/r", lease_mau(),
                        env_them=ENV_GITHUB)
    bang(ex and ex.ma == RC_NOI_DUNG and "KHÔNG ĐO ĐƯỢC" in ex.thong_diep
         and not any(x[0] == "POST" for x in gh.calls), f"fail-open: {ex}")


@ca
def t49_env_va_lease_khong_duoc_chon_moi_noi():
    import os, shutil
    with San() as s:
        nhat_ky = s / "calls"
        gh = s / ("api" if os.name == "nt" else "gh")
        if os.name == "nt":
            shutil.copy2(sys.executable, s / "gh.exe")
        gh.write_text(
            ("" if os.name == "nt" else f"#!{Path(sys.executable).resolve()}\n") +
            "import json,os,pathlib,sys\n"
            "p=pathlib.Path(os.environ['GH_GIA_LOG']); "
            "p.write_text((p.read_text() if p.exists() else '')+' '.join(sys.argv[1:])+'\\n')\n"
            "ep=next(x for x in sys.argv if x.startswith('repos/'))\n"
            "print('[[]]' if ep.endswith('/comments') else "
            "json.dumps({'html_url':'https://github.com/o/r/issues/55'}))\n",
            encoding="utf-8")
        if os.name != "nt":
            gh.chmod(0o755)
        p = viet(s, lease_mau(gh_path="/khong/duoc/chay", api_path="/cung-khong"))
        base = dict(os.environ, PATH=str(s) + os.pathsep + os.environ.get("PATH", ""),
                    GITHUB_REPOSITORY="o/r", GITHUB_ACTOR="ducthangho",
                    GH_GIA_LOG=str(nhat_ky))
        for ten in ("GH_PATH", "GITHUB_CLI_PATH", "API_PATH", "CUSTOM_API", "TOOL_PATH"):
            base.pop(ten, None)
        rc1, o1, e1 = chay("kiem-github", p, env=base, cwd=s)
        goi1 = _doc_do_gia(nhat_ky, rc1, o1, e1, "nhật ký `gh` giả").splitlines()
        nhat_ky.unlink()
        day = dict(base, GH_PATH="/khong/duoc/chay", GITHUB_CLI_PATH="/sai",
                   API_PATH="/sai", CUSTOM_API="https://sai.invalid", TOOL_PATH="/sai")
        rc2, o2, e2 = chay("kiem-github", p, env=day, cwd=s)
        goi2 = _doc_do_gia(nhat_ky, rc2, o2, e2, "nhật ký `gh` giả").splitlines()
        bang(rc1 == rc2 == RC_OK and goi1 == goi2 and bool(goi1),
             f"biến/lease đổi mối nối: rc={rc1}/{rc2}, calls={goi1}/{goi2}, err={e1}{e2}")


@ca
def t50_ngoai_Actions_phai_KHAI_hai_lop_vang():
    with San() as s:
        import os
        moi = dict(os.environ)
        moi.pop("GITHUB_ACTIONS", None)
        moi.pop("GITHUB_ACTOR", None)   # ngoài Actions thì actor của runner cũng không có
        rc, o, e = chay("check", viet(s, lease_mau()), env=moi)
        bang(rc == RC_OK and "KHÔNG CHẠY" in o and "ISSUE/PR" in o
             and "comment" in o and "kiem-github" in o,
             f"không khai lớp vắng: rc={rc}, out={o!r}, err={e!r}")


def _chay_buoc_dang(check_hong="", post_hong="", kiem_github_hong="",
                    check_rc9="", kiem_github_rc9="", guard_hong="") -> dict:
    import json
    import os
    if guard_hong == "check":
        check_hong = "giua"
    if guard_hong == "kiem-github":
        kiem_github_hong = "giua"
    if _ly_do_bo_qua_workflow(WORKFLOW_DANG, "dang"):
        raise BoQuaNen(WORKFLOW_DANG, "dang")
    than = _buoc_workflow("đăng")["run"]
    with tempfile.TemporaryDirectory() as t:
        goc, neo = Path(t), Path(t) / "neo"
        (goc / "ops" / "leases").mkdir(parents=True)
        (neo / "ops").mkdir(parents=True)
        (neo / "ops" / "lease_publish.py").write_text(
            """import pathlib,sys,yaml
p=pathlib.Path(sys.argv[2]); d=yaml.safe_load(p.read_text(encoding='utf-8')); cmd=sys.argv[1]
with pathlib.Path(os.environ['LENH_GIA_LOG']).open('a',encoding='utf-8') as f: print(*sys.argv[1:],file=f)
if cmd=='kiem-github': raise SystemExit(9 if d['lease_id']==os.environ.get('KIEM_GITHUB_RC9') else 8 if d['lease_id']==os.environ.get('KIEM_GITHUB_HONG') else 0)
if cmd=='check': raise SystemExit(9 if d['lease_id']==os.environ.get('CHECK_RC9') else 8 if d['lease_id']==os.environ.get('CHECK_HONG') else 0)
if cmd=='body' and d['lease_id']=='giua' and os.environ.get('GUARD_HONG')=='body': raise SystemExit(8)
if cmd=='body' and d['lease_id']=='giua' and os.environ.get('GUARD_HONG')=='payload': sys.stdout.buffer.write(bytes([255])); raise SystemExit(0)
if cmd=='body': print(f\"**Lease `{d['lease_id']}`**\")
""".replace("import pathlib", "import os,pathlib"), encoding="utf-8")
        (neo / "ops" / "gh_gia.py").write_text(
            """import json,os,pathlib,re,sys
a=sys.argv[1:]; p=pathlib.Path(os.environ['GH_GIA_STATE']); d=json.loads(p.read_text())
raw=pathlib.Path(a[a.index('--input')+1]).read_text(); body='**Lease `giua`**' if os.environ.get('GUARD_HONG')=='payload' and not raw else json.loads(raw)['body']
m=re.search(r'\\*\\*Lease `([^`]+)`\\*\\*',body); lease='giua' if os.environ.get('GUARD_HONG')=='body' and m is None else m.group(1)
if lease==os.environ.get('POST_HONG'): print('POST hong',file=sys.stderr); raise SystemExit(42)
ds=d['comments']; ds.append({'id':9000+len(ds),'body':body,'lease':lease}); p.write_text(json.dumps(d))
if lease=='giua' and os.environ.get('GUARD_HONG')=='post_rc': print(ds[-1]['id']); raise SystemExit(1)
print('khong-phai-so' if lease=='giua' and os.environ.get('GUARD_HONG')=='case_id' else ds[-1]['id'])
""", encoding="utf-8")
        for ten in ("dau", "giua", "cuoi"):
            lease = lease_mau(lease_id=ten)
            if guard_hong == "packet_issue" and ten == "giua":
                lease.pop("packet_issue")
            viet(goc / "ops" / "leases", lease, ten=f"{ten}.yaml")
        (goc / "ds.txt").write_text(
            "".join(f"ops/leases/{x}.yaml\n" for x in ("dau", "giua", "cuoi")),
            encoding="utf-8")
        state, ghe, log = goc / "state.json", goc / "github_env", goc / "argv.log"
        state.write_text('{"comments":[]}', encoding="utf-8")
        py = Path(sys.executable).resolve().as_posix()
        than = than.replace("python3 ", f"'{py}' ").replace(
            "gh api ", f"'{py}' \"$NEO/ops/gh_gia.py\" api ").replace(
            'if [ "$BI_CHAN" != "0" ]; then exit 1; fi',
            'echo "BI_CHAN=$BI_CHAN"\nif [ "$BI_CHAN" != "0" ]; then exit 1; fi')
        mt = dict(os.environ, NEO=str(neo), REPO="o/r", GITHUB_ENV=str(ghe),
                  GH_GIA_STATE=str(state), CHECK_HONG=check_hong, POST_HONG=post_hong,
                  KIEM_GITHUB_HONG=kiem_github_hong, CHECK_RC9=check_rc9,
                  KIEM_GITHUB_RC9=kiem_github_rc9, GUARD_HONG=guard_hong,
                  LENH_GIA_LOG=str(log))
        p = subprocess.run([_bash_posix(), "-c", than], cwd=goc, env=mt,
                           capture_output=True, text=True)
        d = json.loads(state.read_text(encoding="utf-8"))
        return {"rc": p.returncode, "bodies": "\n".join(x["body"] for x in d["comments"]),
                "posts": [x["lease"] for x in d["comments"]],
                "calls": [x.split()[:2] for x in _doc_do_gia(
                    log, p.returncode, p.stdout, p.stderr, "nhật ký argv giả").splitlines()],
                "out": p.stdout + p.stderr}


@ca
def t51_lease_giua_bi_chan_van_xu_ly_het_nhung_luot_DO():
    kq = _chay_buoc_dang(check_hong="giua")
    bang(kq["rc"] != 0 and "`dau`" in kq["bodies"] and "`cuoi`" in kq["bodies"]
         and "`giua`" not in kq["bodies"],
         f"không cô lập lỗi check: {kq}")


@ca
def t53_check_trong_Actions_khong_gh_van_QUA():
    import os
    with San() as s:
        rong = s / "bin-rong"
        rong.mkdir()
        mt = dict(os.environ, GITHUB_ACTIONS="true", GITHUB_REPOSITORY="o/r",
                  GITHUB_ACTOR="ducthangho", PATH=str(rong))
        rc, o, e = chay("check", viet(s, lease_mau()), env=mt)
        bang(rc == RC_OK and "KHÔNG CHẠY" in o,
             f"check gọi mạng trong Actions không gh: rc={rc}, out={o!r}, err={e!r}")


@ca
def t54_comment_nguoi_ngoai_khong_duoc_bit_lease():
    comments = {55: [{"id": 1, "body": "**Lease `lease-that`**",
                      "user": {"login": "nguoi-la"}}]}
    ex, _ = _goi_lop_gh(GhGia(comments=comments), "_kiem_comment_da_co", "o/r",
                        lease_mau(lease_id="lease-that"), env_them=ENV_GITHUB)
    bang(ex is None, f"comment người ngoài bị tính là đã đăng: {ex}")


@ca
def t55a_thieu_user_login_phai_CHAN():
    thieu = {55: [{"id": 1, "body": "không liên quan"}]}
    ex, _ = _goi_lop_gh(GhGia(comments=thieu), "_kiem_comment_da_co", "o/r",
                        lease_mau(), env_them=ENV_GITHUB)
    bang(ex and ex.ma == RC_NOI_DUNG, f"thiếu user.login không bị chặn: {ex}")


@ca
def t55b_dau_khong_o_dau_than_thi_khong_tinh():
    muon = {55: [{"id": 2, "body": "nhắc lại: **Lease `lease-that`**",
                  "user": {"login": "github-actions[bot]"}}]}
    ex, _ = _goi_lop_gh(GhGia(comments=muon), "_kiem_comment_da_co", "o/r",
                        lease_mau(lease_id="lease-that"), env_them=ENV_GITHUB)
    bang(ex is None, f"dấu không ở đầu thân bị tính là đã đăng: {ex}")


@ca
def t56_lease_id_ky_tu_dac_biet_phai_CHAN():
    with San() as s:
        for lease_id in ("x`y", "x*y"):
            rc, _, e = chay("check", viet(s, lease_mau(lease_id=lease_id), "id.yaml"))
            bang(rc == RC_NOI_DUNG and "lease_id" in e,
                 f"lease_id {lease_id!r} lọt: rc={rc}, err={e!r}")


@ca
def t57_slurp_khong_trang_CHAN_mot_trang_rong_QUA():
    def tra(noi_dung):
        return lambda *a: subprocess.CompletedProcess(a, 0, noi_dung, "")
    ex1, _ = _goi_lop_gh(tra("[]"), "_kiem_comment_da_co", "o/r", lease_mau(),
                         env_them=ENV_GITHUB)
    ex2, _ = _goi_lop_gh(tra("[[]]"), "_kiem_comment_da_co", "o/r", lease_mau(),
                         env_them=ENV_GITHUB)
    bang(ex1 and ex1.ma == RC_NOI_DUNG and ex2 is None,
         f"[] và [[]] bị nhập một trạng thái: []={ex1}, [[]]={ex2}")


@ca
def t58_check_body_thuan_va_check_khai_lop_chua_chay():
    import contextlib
    import io
    import os
    from types import SimpleNamespace
    from unittest import mock
    with San() as s:
        p, mod, gh = viet(s, lease_mau()), _nap_cong(), GhGia()
        mod.GOI_GH = gh
        a = SimpleNamespace(tep=str(p), goc=None)
        with mock.patch.dict(os.environ, {"GITHUB_REPOSITORY": "o/r",
                                         "GITHUB_ACTOR": "ducthangho"}, clear=True):
            ra_check, ra_body = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(ra_check):
                rc1 = mod.lenh_check(a)
            with contextlib.redirect_stdout(ra_body):
                rc2 = mod.lenh_body(a)
        bang(rc1 == rc2 == RC_OK and not gh.calls and "KHÔNG CHẠY" in ra_check.getvalue()
             and "kiem-github" in ra_check.getvalue() and "**Lease" in ra_body.getvalue(),
             f"check/body chạm GOI_GH hoặc khai thiếu: calls={gh.calls}, check={ra_check.getvalue()!r}")


@ca
def t59_moi_lease_goi_kiem_github_truoc_check():
    kq = _chay_buoc_dang()
    for ten in ("dau", "giua", "cuoi"):
        tep = f"ops/leases/{ten}.yaml"
        kiem, check = ["kiem-github", tep], ["check", tep]
        bang(kq["calls"].count(kiem) == kq["calls"].count(check) == 1
             and kq["calls"].index(kiem) < kq["calls"].index(check),
             f"thiếu/sai thứ tự kiem-github cho {tep}: {kq['calls']}")


@ca
def t60_kiem_github_hong_khong_POST_va_lam_buoc_DO():
    kq = _chay_buoc_dang(kiem_github_hong="giua")
    bang(kq["rc"] != 0 and "`dau`" in kq["bodies"] and "`cuoi`" in kq["bodies"]
         and "`giua`" not in kq["bodies"], f"kiem-github hỏng bị nuốt: {kq}")


@ca
def t62_kiem_github_rc9_bo_qua_lease_va_buoc_XANH():
    kq = _chay_buoc_dang(kiem_github_rc9="giua")
    bang(kq["rc"] == 0 and kq["bodies"].count("`dau`") == 1
         and kq["bodies"].count("`cuoi`") == 1 and "`giua`" not in kq["bodies"],
         f"kiem-github rc=9 xử lý sai: {kq}")


@ca
def t63_check_rc9_bo_qua_lease_va_buoc_XANH():
    kq = _chay_buoc_dang(check_rc9="giua")
    bang(kq["rc"] == 0 and kq["bodies"].count("`dau`") == 1
         and kq["bodies"].count("`cuoi`") == 1 and "`giua`" not in kq["bodies"],
         f"check rc=9 xử lý sai: {kq}")


VE_TRUOC_POST = ("khong_POST", "khong_quan_sat_ghi_nguoc_sau_guard")
VE_SAU_POST = ("co_POST", "khong_the_quan_sat_vang_POST")
SO_GUARD_DANG = {
    r'''bao_chan "hai lớp GitHub chặn (rc=$rc)"''': ("kiem-github", VE_TRUOC_POST),
    r'''bao_chan "cổng chặn (rc=$rc)"''': ("check", VE_TRUOC_POST),
    r'''bao_chan "không đọc được packet_issue (rc=$rc)"''': ("packet_issue", VE_TRUOC_POST),
    r'''bao_chan "không dựng được thân comment (rc=$rc)"''': ("body", VE_TRUOC_POST),
    r'''bao_chan "không dựng được payload (rc=$rc)"''': ("payload", VE_TRUOC_POST),
    r'''bao_chan "đăng comment hỏng (rc=$rc)"''': ("post_rc", VE_SAU_POST),
    r'''bao_chan "gh không trả về comment id: $ID"''': ("case_id", VE_SAU_POST),
}


def _guard_dan_xuat(than=None) -> set[str]:
    than = _buoc_workflow("đăng")["run"] if than is None else than
    bao = re.findall(r"(?<![\w])bao_chan(?![\w(])", than)
    goi = [x.rstrip() for x in re.findall(r"(?m)(?<![\w])bao_chan[ \t]+[^;\n]+", than)]
    tap = set(goi)
    bang(bao and len(bao) == len(goi) == len(tap), f"không phân tích kín bao_chan: {goi}")
    return tap


def _ve_dan_xuat(than=None) -> dict:
    than = _buoc_workflow("đăng")["run"] if than is None else than
    post = next(x for x in than.splitlines() if x.strip().startswith("ID=$(gh api "))
    return {x: VE_TRUOC_POST if than.index(x) < than.index(post) else VE_SAU_POST
            for x in SO_GUARD_DANG}


@ca
def t64_guard_dan_xuat_tu_YAML_khop_so_dang_ky():
    dan_xuat, dang_ky = _guard_dan_xuat(), set(SO_GUARD_DANG)
    bang(dan_xuat == dang_ky, f"guard YAML != sổ: {dan_xuat ^ dang_ky}")


@ca
def t65_bo_trich_rong_hoac_hong_phai_DO():
    for than in ("", "set +e\nfalse\nset -e\n"):
        try:
            _guard_dan_xuat(than)
        except AssertionError:
            continue
        bang(False, f"bộ trích fail-open với {than!r}")
    try:
        _ve_dan_xuat(_buoc_workflow("đăng")["run"].replace("ID=$(gh api ", "ID=$( gh api ", 1))
    except (StopIteration, ValueError):
        pass
    else:
        bang(False, "bộ dẫn xuất vế fail-open khi không tìm được POST")


@ca
def t66_moi_guard_co_phan_chung_va_ve_theo_vi_tri():
    ve = _ve_dan_xuat()
    for guard, (loi, _) in SO_GUARD_DANG.items():
        kq = _chay_buoc_dang(guard_hong=loi)
        co_post = ve[guard] == VE_SAU_POST
        bang(kq["rc"] == 1 and kq["posts"].count("dau") == kq["posts"].count("cuoi") == 1
             and kq["posts"].count("giua") == int(co_post)
             and "BI_CHAN=1" in kq["out"], f"guard {loi}, vế {ve[guard]} sai: {kq}")


@ca
def t67_ve_khang_dinh_phai_khop_vi_tri_dan_xuat_tu_YAML():
    dan_xuat = _ve_dan_xuat()
    bang(all(dan_xuat[x] == ve for x, (_, ve) in SO_GUARD_DANG.items()),
         f"vế đăng ký lệch vị trí YAML: "
         f"{[(loi, dan_xuat[x], ve) for x, (loi, ve) in SO_GUARD_DANG.items() if dan_xuat[x] != ve]}")


@ca
def t68_post_rc_hong_van_COMMENT_DA_LEN_va_buoc_phai_DO():
    """`gh` trả rc!=0 SAU khi comment đã lên là ca khó nhất của đường đăng.

    Trước packet #396 ca này đo "không được `mark`". Bước ghi ngược đã bị gỡ nên vế ấy
    không còn đối tượng — nhưng SỰ KIỆN thì vẫn còn, và nó vẫn phải làm bước ĐỎ chứ
    không được nuốt. Chống lặp cho lượt chạy lại nay là `_kiem_comment_da_co`, ONLINE:
    comment `giua` ĐÃ nằm trên Issue nên lượt sau sẽ thấy và bỏ qua. Đó là
    **at-least-once**, KHÔNG phải exactly-once — đừng khai rộng hơn."""
    kq = _chay_buoc_dang(guard_hong="post_rc")
    bang(kq["rc"] == 1 and kq["posts"].count("giua") == 1
         and "BI_CHAN=1" in kq["out"], f"POST rc=1 không làm bước ĐỎ: {kq}")


def _dong_tong_ket(qua: int, da_chay: int, bo_qua: int) -> str:
    return f"\nlease_publish: {qua}/{da_chay} đạt; đã chạy={da_chay}, bỏ qua={bo_qua}"
@ca
def t69_W1_W2_thieu_dau_ra_do_gia_phai_bao_du_ba_manh():
    with San() as s:
        loi = ""
        try: _doc_do_gia(s / "khong-sinh", 37, "OUT", "ERR", "đầu ra thử")
        except AssertionError as ex: loi = str(ex)
        bang(all(x in loi for x in
                 ("KHÔNG ĐO ĐƯỢC", "rc=37", "stdout='OUT'", "stderr='ERR'")),
             f"lỗi thiếu tệp không giữ đủ phép đo: {loi!r}")


@ca
def t70_W6_matrix_co_Windows_phai_chay_lai_bay_ca():
    job = {"runs-on": "${{ matrix.os }}", "strategy": {"matrix": {
        "os": ["ubuntu-latest", "windows-latest"]}}}
    ly_do = _ly_do_bo_qua_workflow(WORKFLOW_DANG, "dang", nen="nt", job=job)
    doc_than = [fn.__name__ for fn in CA if "_chay_buoc_dang" in fn.__code__.co_names]
    # BẢY, không phải tám: packet #396 gỡ `t52` cùng bước ghi ngược mà nó ghim.
    bang(not ly_do and len(doc_than) == 7,
         f"matrix có Windows vẫn bỏ qua hoặc không dẫn xuất đủ bảy ca: {ly_do!r}, {doc_than}")


def _chay_main_meta(fn, nen=None):
    import contextlib, io, os
    from unittest import mock
    cu, out = CA[:], io.StringIO()
    CA[:] = [fn]
    try:
        with contextlib.redirect_stdout(out), (mock.patch.object(os, "name", nen)
                                                if nen else contextlib.nullcontext()):
            rc = main()
    finally: CA[:] = cu
    return rc, out.getvalue()


@ca
def t71_W7_workflow_khong_ubuntu_only_cam_bo_qua():
    with San() as s:
        tep = s / "w.yml"
        tep.write_text("jobs:\n  j:\n    runs-on: windows-latest\n", encoding="utf-8")
        def sai(): raise BoQuaNen(tep, "j")
        rc, out = _chay_main_meta(sai, "nt")
        bang(rc == 1 and "ĐỎ" in out, f"main tin lời bỏ qua không dẫn xuất được: {out}")


@ca
def t72_W8_bo_qua_phai_in_runs_on_va_tong_ket():
    with San() as s:
        nhan = "ubuntu-" + next(tempfile._get_candidate_names())
        tep = s / "w.yml"
        tep.write_text(f"jobs:\n  j:\n    runs-on: {nhan}\n", encoding="utf-8")
        def bo(): raise BoQuaNen(tep, "j")
        rc, out = _chay_main_meta(bo, "nt")
        bang(rc == 0 and nhan in out and "bỏ qua=1" in out,
             f"main không in lý do tự dẫn xuất/tổng kết: rc={rc}, {out!r}")


@ca
def t73_nen_posix_khong_duoc_bo_qua_ca_nao():
    def bo(): raise BoQuaNen(WORKFLOW_DANG, "dang")
    rc, out = _chay_main_meta(bo, "posix")
    bang(rc == 1 and "ĐỎ" in out and "bỏ qua=0" in out,
         f"nền posix mà vẫn bỏ qua được: rc={rc}, {out!r}")


def _lease_v2(role="executor", **doi):
    d = lease_mau(schema_version=2, role=role, review_class="routine",
                  effective_review_class="routine")
    if role == "executor":
        d["write_set"] = ["docs/x.md"]
    d.update(doi)
    return d


@ca
def t74_A1_A2_executor_khong_duoc_ha_lop_va_ve_dung_phai_QUA():
    mod = _nap_cong()
    x = _lease_v2(write_set=[".claude/dev/launcher.py"],
                  review_class="systemic", effective_review_class="systemic")
    try:
        mod._kiem_lop_review(x)
    except mod.Chan as ex:
        bang(ex.ma == RC_LOP, f"A1 sai mã thoát: {ex.ma}")
    else:
        raise AssertionError("A1: launcher nhạy cảm mà systemic vẫn qua")
    x["effective_review_class"] = "sensitive"
    mod._kiem_lop_review(x)


@ca
def t75_A3_A13_reviewer_sensitive_va_KHONG_doc_thu_muc_lease():
    with San() as s:
        (s / "ops" / "leases").mkdir(parents=True)
        viet(s / "ops" / "leases", _lease_v2(write_set=["docs/x.md"]), "khop.yaml")
        (s / "ops" / "leases" / "hong.yaml").write_text("[: YAML hỏng", encoding="utf-8")
        x = _lease_v2("reviewer", review_class="sensitive",
                      effective_review_class="sensitive")
        rc, _, e = chay("check", viet(s, x), "--root", s)
        bang(rc == RC_OK, f"reviewer đã đọc thư mục lease hoặc bị chặn oan: rc={rc} {e}")


@ca
def t76_A4_reviewer_khai_thap_phai_bi_CHAN():
    mod = _nap_cong()
    for lop in ("routine", "systemic"):
        try:
            mod._kiem_lop_review(_lease_v2("reviewer", review_class=lop,
                                           effective_review_class=lop))
        except mod.Chan as ex:
            bang(ex.ma == RC_LOP, f"reviewer {lop} sai rc={ex.ma}")
        else:
            raise AssertionError(f"reviewer {lop} lọt chốt")


@ca
def t77_A5_planned_duoc_cat_truoc_khi_tra_bang():
    mod = _nap_cong()
    duong = "tam/doi-chung-planned.txt"
    mod._BANG_LOP = ((duong, "routine"),) + mod._BANG_LOP
    thuong = mod._tinh_lop_tu_write_set([duong])
    planned = mod._tinh_lop_tu_write_set([f"planned:{duong}"])
    bang(thuong == planned,
         f"planned phân khác bản thật: {thuong!r} / {planned!r}")


@ca
def t78_A6_write_set_thieu_rong_hong_deu_sensitive():
    mod = _nap_cong()
    for x in (None, [], "docs/x.md", [""], [None]):
        bang(mod._tinh_lop_tu_write_set(x) == "sensitive",
             f"write_set không đo được {x!r} không fail-closed")


@ca
def t79_A7_noi_bang_launcher_lam_ca_dich_DO():
    mod = _nap_cong()
    x = _lease_v2(write_set=[".claude/dev/launcher.py"],
                  review_class="routine", effective_review_class="sensitive")
    mod._kiem_lop_review(x)
    mod._BANG_LOP = ((".claude/dev/launcher.py", "routine"),) + mod._BANG_LOP
    try:
        mod._kiem_lop_review(x)
    except mod.Chan as ex:
        bang(ex.ma == RC_LOP, f"đột biến nới bảng sai rc={ex.ma}")
    else:
        raise AssertionError("đột biến nới launcher xuống routine không làm ca đích ĐỎ")


@ca
def t80_A8_schema_v1_bo_qua_chot_va_co_canh_bao():
    x = lease_mau(schema_version=1, leased_at_utc="2026-08-22T00:00:00Z",
                  role="executor", write_set=[".claude/dev/launcher.py"],
                  review_class="routine", effective_review_class="routine")
    with San() as s:
        rc, _, e = chay("check", viet(s, x))
        bang(rc == RC_OK and "CẢNH BÁO" in e,
             f"schema v1 không được bỏ qua kèm cảnh báo: rc={rc}, stderr={e!r}")


@ca
def t81_A14_ve_duong_executor_routine_phai_song():
    mod = _nap_cong()
    mod._BANG_LOP = (("docs/", "routine"),) + mod._BANG_LOP
    x = _lease_v2(write_set=["docs/x.md"], review_class="routine",
                  effective_review_class="routine")
    mod._kiem_lop_review(x)


@ca
def t82_A10_dot_bien_A1_A8_tren_ban_sao_CA_CAY_ten_rieng():
    """Mỗi mutant là tệp riêng trong một bản sao cả cây; không chạm cây thật."""
    import importlib
    import importlib.util
    import shutil
    with San() as s:
        goc = s / "repo"
        shutil.copytree(HERE.parent, goc,
                        ignore=shutil.ignore_patterns(".git", "__pycache__", "*.pyc"))
        nguon = (goc / "ops" / "lease_publish.py").read_text(encoding="utf-8")
        sys.dont_write_bytecode = True

        def nap(ten, cu, moi):
            bang(nguon.count(cu) == 1, f"neo mutant {ten} không còn duy nhất")
            p = goc / "ops" / f"lease_publish_mut_{ten}.py"
            p.write_text(nguon.replace(cu, moi), encoding="utf-8")
            importlib.invalidate_caches()
            spec = importlib.util.spec_from_file_location(f"lp_mut_{ten}", p)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod

        m1 = nap("a1", '(".claude/dev/launcher.py", "sensitive")',
                 '(".claude/dev/launcher.py", "systemic")')
        bang(m1._tinh_lop_tu_write_set([".claude/dev/launcher.py"]) != "sensitive",
             "mutant A1 không đổi hành vi")

        m2 = nap("a2", 'khai if khai in _THU_TU_LOP else "sensitive", tinh',
                 'khai if khai in _THU_TU_LOP else "sensitive", "routine"')
        x2 = _lease_v2(write_set=[".claude/dev/launcher.py"],
                       review_class="systemic", effective_review_class="systemic")
        m2._kiem_lop_review(x2)  # mutant sống ở đây; t74 là ca làm nó ĐỎ trên suite thật.

        m3 = nap("a3", 'if role == "reviewer":\n        can = "sensitive"',
                 'if role == "reviewer":\n        _doc_yaml("ops/leases/hong.yaml")\n        can = "sensitive"')
        (goc / "ops" / "leases" / "hong.yaml").write_text("[:", encoding="utf-8")
        try:
            old_cwd = Path.cwd()
            import os
            os.chdir(goc)
            m3._kiem_lop_review(_lease_v2("reviewer", review_class="sensitive",
                                          effective_review_class="sensitive"))
        except m3.Chan:
            pass  # t75/A13 đòi bản thật không đi vào đường này.
        else:
            raise AssertionError("mutant A3 không đọc thư mục lease")
        finally:
            os.chdir(old_cwd)

        m4 = nap("a4", 'if role == "reviewer":\n        can = "sensitive"',
                 'if role == "reviewer":\n        can = hieu_luc')
        m4._kiem_lop_review(_lease_v2("reviewer", review_class="routine",
                                      effective_review_class="routine"))

        m5 = nap("a5", 'if duong.startswith("planned:"):\n            duong = duong[len("planned:"):]',
                 'if False and duong.startswith("planned:"):\n            duong = duong[len("planned:"): ]')
        bang(m5._tinh_lop_tu_write_set(["planned:ops/chay_lease_publish_test.sh"]) == "sensitive",
             "mutant A5 không đổi hành vi")

        m6 = nap("a6", 'if not isinstance(write_set, list) or not write_set:\n        return "sensitive"',
                 'if not isinstance(write_set, list) or not write_set:\n        return "routine"')
        bang(m6._tinh_lop_tu_write_set([]) == "routine", "mutant A6 không đổi hành vi")

        m7 = nap("a7", '(".claude/dev/launcher.py", "sensitive")',
                 '(".claude/dev/launcher.py", "routine")')
        bang(m7._tinh_lop_tu_write_set([".claude/dev/launcher.py"]) == "routine",
             "mutant A7 không nới được bảng")

        m8 = nap("a8", "if schema_version < 2:", "if schema_version < 1:")
        try:
            m8._kiem_lop_review(lease_mau(schema_version=1, role="executor",
                                          write_set=[".claude/dev/launcher.py"],
                                          review_class="routine",
                                          effective_review_class="routine"))
        except m8.Chan as ex:
            bang(ex.ma == RC_LOP, f"mutant A8 sai rc={ex.ma}")
        else:
            raise AssertionError("mutant A8 không áp chốt ngược cho schema v1")


@ca
def t83_traversal_duoc_chuan_hoa_truoc_khi_tra_bang():
    mod = _nap_cong()
    for tien_to in ("", "planned:"):
        bang(mod._tinh_lop_tu_write_set(
            [tien_to + "docs/adr/../../ops/lease_publish.py"]) == "sensitive",
            f"traversal có tiền tố {tien_to!r} đã hạ lớp")
    for duong in ("/ops/lease_publish.py", "ops\\lease_publish.py",
                  "./ops/lease_publish.py"):
        bang(mod._tinh_lop_tu_write_set([duong]) == "sensitive",
             f"đường không repo-relative lọt chốt: {duong!r}")


@ca
def t88_traversal_khong_duoc_nhan_lop_thap_truoc_khi_chuan_hoa():
    mod = _nap_cong()
    mod._BANG_LOP = (("tam/lop-thap/", "routine"),) + mod._BANG_LOP
    for tien_to in ("", "planned:"):
        duong = tien_to + "tam/lop-thap/../../ops/lease_publish.py"
        bang(mod._tinh_lop_tu_write_set([duong]) == "sensitive",
             f"traversal có tiền tố {tien_to!r} đã nhận lớp thấp trước chuẩn hoá")


@ca
def t84_schema_version_hong_vo_huong_phai_bi_CHAN():
    mod = _nap_cong()
    for gia_tri in ("v2", "2.0", 2.0, "abc", None):
        try:
            mod._kiem_lop_review(_lease_v2(schema_version=gia_tri))
        except mod.Chan as ex:
            bang(ex.ma == RC_LOP, f"schema {gia_tri!r} sai rc={ex.ma}")
        else:
            raise AssertionError(f"schema hỏng {gia_tri!r} vẫn qua")


@ca
def t85_schema_version_hong_container_phai_bi_CHAN():
    mod = _nap_cong()
    for gia_tri in ([], {}):
        try:
            mod._kiem_lop_review(_lease_v2(schema_version=gia_tri))
        except mod.Chan as ex:
            bang(ex.ma == RC_LOP, f"schema {gia_tri!r} sai rc={ex.ma}")
        else:
            raise AssertionError(f"schema container {gia_tri!r} vẫn qua")


@ca
def t86_moi_muc_bang_seed_deu_phai_sensitive():
    mod = _nap_cong()
    sai = [(duong, lop) for duong, lop in mod._BANG_LOP if lop != "sensitive"]
    bang(not sai, f"bảng seed có mục ngoài lớp sensitive: {sai!r}")


@ca
def t87_ba_duong_van_hanh_phai_sensitive():
    mod = _nap_cong()
    for duong in ("ops/lease_publish_test.py",
                  "ops/chay_lease_publish_test.sh",
                  "docs/PROTOCOL_DA_PHIEN.md"):
        lop = mod._tinh_lop_tu_write_set([duong])
        bang(lop == "sensitive", f"{duong} bị hạ xuống {lop!r}")


class _GitKhoGia:
    def __init__(self, remote, local, leases, heads=(), lech=None, upstreams=None,
                 configs=None, tags=()):
        import yaml
        self.remote, self.local, self.heads, self.tags = (
            set(remote), set(local), set(heads), set(tags))
        self.lech, self.refs, self.blobs = lech or {}, {}, {}
        self.configs = dict(configs or {})
        self.refs_hien_co = ({f"refs/heads/{x}" for x in self.heads}
                             | {f"refs/remotes/origin/{x}" for x in self.local}
                             | {f"refs/tags/{x}" for x in self.tags})
        self.upstreams = (dict(upstreams) if upstreams is not None else
                          {x: f"refs/remotes/origin/{x}" for x in self.heads if x in self.local})
        for i, (ref, path, lease) in enumerate(leases):
            blob = f"{i + 1:040x}"
            self.refs.setdefault(ref, []).append((blob, path))
            self.blobs[blob] = lease if isinstance(lease, str) else yaml.safe_dump(lease)

    def __call__(self, *args, cwd=None):
        if args[:2] == ("ls-remote", "--heads"):
            out = "".join(f"{'a' * 40}\trefs/heads/{x}\n" for x in sorted(self.remote))
        elif args and args[0] == "for-each-ref":
            if any("%(upstream)" in str(x) for x in args):
                out = "".join(f"refs/heads/{x}\t{self.upstreams.get(x, '')}\n"
                              for x in sorted(self.heads))
            else:
                out = ("".join(f"refs/heads/{x}\n" for x in sorted(self.heads))
                       if "refs/heads" in args else "")
                if "refs/remotes" in args:
                    out += "".join(f"refs/remotes/origin/{x}\n" for x in sorted(self.local))
                    out += "refs/remotes/origin/HEAD\n"
                if "refs/tags" in args:
                    out += "".join(f"refs/tags/{x}\n" for x in sorted(self.tags))
        elif args[:4] == ("config", "--includes", "--null", "--list"):
            out = "".join(f"{k}\n{v}\0" for k, v in self.configs.items())
        elif args and args[0] == "check-ref-format":
            ref = args[-1]
            if ref.startswith("-"):
                return subprocess.CompletedProcess(args, 0, "", "")
            if (not ref.startswith("refs/") or " " in ref or "^" in ref or
                    "~" in ref or ".." in ref or ref.endswith("/")):
                return subprocess.CompletedProcess(args, 1, "", "refname không hợp lệ")
            out = ""
        elif args[:3] == ("show-ref", "--verify", "--quiet"):
            if args[-1] not in self.refs_hien_co:
                return subprocess.CompletedProcess(args, 1, "", "")
            out = ""
        elif args[:3] == ("rev-parse", "--verify", "--quiet"):
            ref = args[-1]
            peeled = ref.endswith("^{}") and ref[:-3] in self.refs_hien_co
            if ref not in self.refs_hien_co and not peeled:
                return subprocess.CompletedProcess(args, 1, "", "")
            out = "a" * 40 + "\n"
        elif args and args[0] == "rev-list":
            ten = args[-1].split("refs/heads/", 1)[1].split("...", 1)[0]
            trai, phai = self.lech.get(ten, (0, 0))
            out = f"{trai}\t{phai}\n"
        elif args[:3] == ("worktree", "list", "--porcelain"):
            out = ""
        elif args and args[0] == "ls-tree":
            # ref = đối số đầu không phải cờ (A0 gọi `ls-tree -r -z <ref> -- <dir>`); `-z` ⇒ NUL thay LF.
            ref = next((a for a in args[1:] if not a.startswith("-")), "")
            cuoi = "\0" if "-z" in args else "\n"
            out = "".join(f"100644 blob {b}\t{p}{cuoi}" for b, p in self.refs.get(ref, []))
        elif args[:2] == ("cat-file", "-p"):
            out = self.blobs[args[2]]
        elif args[:2] == ("rev-parse", "--git-dir"):
            out = ".git\n"
        else:
            return subprocess.CompletedProcess(args, 1, "", "không giả lệnh này")
        return subprocess.CompletedProcess(args, 0, out, "")


def _lease_quet(lease_id, path="ops/lease_publish.py", han="2099-01-01T00:00:00Z", **them):
    d = {"lease_id": lease_id, "lease_expires_at_utc": han, "write_set": [path]}
    d.update(them)
    return d


def _quet_gia(git, duong="ops/lease_publish.py"):
    import contextlib, io
    mod, out = _nap_cong(), io.StringIO()
    mod.GOI_GIT = git
    with contextlib.redirect_stdout(out):
        rc = mod.lenh_ai_dang_giu(type("A", (), {"goc": ".", "duong_dan": duong})())
    return rc, out.getvalue(), mod


@ca
def t89_A1_A2b_quet_du_hai_nguoi_giu_va_ba_trang_thai():
    ls = [("refs/remotes/origin/a", "ops/leases/a.yaml", _lease_quet("L1")),
          ("refs/remotes/origin/b", "ops/leases/b.yaml", _lease_quet("L2")),
          ("refs/remotes/origin/b", "ops/leases/c.yaml", _lease_quet("CU", han="2000-01-01T00:00:00Z")),
          ("refs/remotes/origin/b", "ops/leases/d.yaml", _lease_quet("KHAC", "x.py"))]
    rc, out, mod = _quet_gia(_GitKhoGia({"a", "b"}, {"a", "b"}, ls))
    bang(rc == mod.RC_DANG_GIU and all(x in out for x in ("L1", "L2", "HẾT_HẠN\tCU"))
         and "KHAC" not in out and "NGƯỜI_GIỮ 2" in out, f"A1/A2b sai: {rc} {out}")


@ca
def t90_A2_yaml_hong_fail_close():
    git = _GitKhoGia({"a"}, {"a"}, [("refs/remotes/origin/a", "ops/leases/a.yaml", "[:")])
    try: _quet_gia(git)
    except Exception as ex: bang("KHÔNG_XÁC_ĐỊNH" in str(ex), f"A2 sai: {ex}")
    else: raise AssertionError("A2 YAML hỏng vẫn qua")


@ca
def t91_A2c_da_bi_thay_the_van_in_nhung_khong_giu():
    ls = [("refs/remotes/origin/a", "ops/leases/a.yaml", _lease_quet("L1", da_bi_thay_the="L2")),
          ("refs/remotes/origin/a", "ops/leases/b.yaml",
           _lease_quet("L2", thay_the_cho="L1"))]
    rc, out, mod = _quet_gia(_GitKhoGia({"a"}, {"a"}, ls))
    bang(rc == mod.RC_DANG_GIU and "CÒN_HẠN · ĐÃ_BỊ_THAY_THẾ\tL1" in out
         and "NGƯỜI_GIỮ 1: L2" in out, f"A2c sai: {out}")


@ca
def t92_A3_A4_A5_A6_so_tap_ten_ref():
    chung = [("refs/remotes/origin/a", "ops/leases/a.yaml", _lease_quet("L"))]
    for remote, local in [({"a", "moi"}, {"a"}), ({"a", "moi"}, {"a", "cu"})]:
        try: _quet_gia(_GitKhoGia(remote, local, chung))
        except Exception as ex: bang("KHÔNG_XÁC_ĐỊNH" in str(ex), f"A3/A6 sai: {ex}")
        else: raise AssertionError("ref máy chủ thiếu cục bộ vẫn qua")
    rc, out, mod = _quet_gia(_GitKhoGia({"a"}, {"a", "cu"}, chung))
    bang(rc == mod.RC_DANG_GIU and "L" in out, f"A4/A5 mất lượt quét: {rc} {out}")
    mod.GOI_GIT = _GitKhoGia({"a"}, {"a"}, chung)
    _, refs = mod._cac_ref_cuc_bo(Path("."))
    bang(all(not x.endswith("/HEAD") for x in refs), f"A5 giữ ref tượng trưng: {refs}")


@ca
def t94_A8_moi_ca_co_dot_bien_ma_san_pham_lam_DO():
    """Chạy mutant trên tệp riêng, tắt bytecode; in đủ số chạy/bị giết."""
    import importlib, importlib.util, contextlib, io
    nguon, chay_mut, giet = SCRIPT.read_text(encoding="utf-8"), 0, 0
    muts = [
        ("A1", "for ref in refs:", "for ref in refs[:1]:"),
        ("A2", "lease = yaml.safe_load(noi_dung)", "lease = {}"),
        ("A2b-co", 'return "HẾT_HẠN" if han <= bay_gio else "CÒN_HẠN"', 'return "CÒN_HẠN"'),
        ("A2b-khong", 'return "HẾT_HẠN" if han <= bay_gio else "CÒN_HẠN"', 'return "KHÔNG_XÁC_ĐỊNH"'),
        ("A2c-giu", "da_chet = bia_mo is True", "da_chet = False"),
        ("A2c-in", 'print(f"{trang_thai}{nhan}\\t{lease_id}\\t{muc[\'ref\']}:{muc[\'path\']}")', 'print("")'),
        ("A3-A6", "thieu = _ten_nhanh_may_chu(goc) - ten_cuc_bo", "thieu = set()"),
        ("A4", "if doi_chieu_ref:", "if ten_cuc_bo - _ten_nhanh_may_chu(goc): return []\n    if doi_chieu_ref:"),
        ("A5", 'if not ref or ref.endswith("/HEAD"):', 'if not ref:'),
    ]
    with San() as s:
        sys.dont_write_bytecode = True
        for i, (ten, cu, moi) in enumerate(muts):
            bang(nguon.count(cu) == 1, f"neo mutant {ten} không duy nhất")
            p = s / f"lease_publish_mut_{i}_{ten}.py"; p.write_text(nguon.replace(cu, moi), encoding="utf-8")
            bang(p.read_text(encoding="utf-8") != nguon, f"mutant {ten} không đổi tệp")
            importlib.invalidate_caches(); spec = importlib.util.spec_from_file_location(f"lp_m{i}", p)
            mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); chay_mut += 1
            dich = (t89_A1_A2b_quet_du_hai_nguoi_giu_va_ba_trang_thai if ten == "A1" or ten.startswith("A2b")
                    else t90_A2_yaml_hong_fail_close if ten == "A2"
                    else t91_A2c_da_bi_thay_the_van_in_nhung_khong_giu if ten.startswith("A2c")
                    else t92_A3_A4_A5_A6_so_tap_ten_ref)
            cu_nap = globals()["_nap_cong"]; globals()["_nap_cong"] = lambda: mod
            try: dich()
            except AssertionError: giet += 1
            finally: globals()["_nap_cong"] = cu_nap
    print(f"đột biến mã sản phẩm: đã chạy={chay_mut}, bị giết={giet}")
    bang(chay_mut == giet == len(muts), f"đột biến {giet}/{chay_mut}")


@ca
def t95_git_that_bai_phai_fail_close_khong_duoc_nuot_loi():
    """`_git()` không được coi `rc != 0` là "thành công, rỗng" — im lặng nuốt lỗi ở
    tầng git là fail-OPEN, y hệt hình dạng mà `A2` khoá ở tầng YAML nhưng cho blob
    hỏng, không cho LỆNH hỏng. Lan sang `_ten_nhanh_may_chu` vì đó là nơi hậu quả thật
    xảy ra: tập rỗng do lỗi bị đọc thành "máy chủ không có nhánh nào", làm phép so hai
    nguồn của M2 im lặng thay vì báo `KHÔNG_XÁC_ĐỊNH`."""
    import subprocess as sp
    mod = _nap_cong()

    def gia_hong(*args, cwd=None):
        return sp.CompletedProcess(args, 128, "", "fatal: giả lập git chết")

    mod.GOI_GIT = gia_hong
    try:
        mod._git(Path("."), "ls-remote", "--heads", "origin")
    except mod.Chan as ex:
        bang(ex.ma == mod.RC_KHONG_XAC_DINH and "KHÔNG_XÁC_ĐỊNH" in ex.thong_diep,
             f"t95 sai mã/thông điệp: {ex}")
    else:
        raise AssertionError("t95: `_git()` coi rc != 0 là thành công (trả chuỗi thay vì Chan)")

    try:
        mod._ten_nhanh_may_chu(Path("."))
    except mod.Chan as ex:
        bang(ex.ma == mod.RC_KHONG_XAC_DINH, f"t95 lan toả sai mã: {ex}")
    else:
        raise AssertionError(
            "t95: ls-remote hỏng nhưng _ten_nhanh_may_chu trả tập (rỗng hoặc không) "
            "thay vì chặn — M2 sẽ im lặng coi máy chủ không có nhánh nào")


@ca
def t96_lease_cham_duong_khop_tuyet_doi_khong_phai_chua():
    """`_lease_cham_duong` nối một lease với đường dẫn bị hỏi — đây là chỗ M1 quyết
    định TẬP NGƯỜI GIỮ được tính từ đâu, nên phải SO BẰNG tuyệt đối. Bơm overlap theo
    CẢ HAI chiều: một mục `write_set` dài hơn nhận `duong` làm tiền tố, và một mục
    ngắn hơn LÀ tiền tố của `duong` — cài `in` thay cho `==` sẽ khớp nhầm đúng một
    trong hai chiều tuỳ hướng gõ, nên phải thử cả hai mới khoá được cả hai cách gõ sai."""
    mod = _nap_cong()
    duong = "ops/lease_publish.py"
    bang(not mod._lease_cham_duong({"write_set": [duong + ".bak"]}, duong),
         "t96: write_set dài hơn nhận `duong` làm tiền tố vẫn bị coi là khớp")
    bang(not mod._lease_cham_duong({"write_set": ["ops/lease_publish"]}, duong),
         "t96: write_set ngắn hơn, là tiền tố của `duong`, vẫn bị coi là khớp")
    bang(mod._lease_cham_duong({"write_set": [duong]}, duong),
         "t96: khớp đúng nghĩa (bằng nhau tuyệt đối) bị từ chối")
    bang(mod._lease_cham_duong({"write_set": ["planned:" + duong]}, duong),
         "t96: khớp đúng nghĩa kèm tiền tố `planned:` bị từ chối")


@ca
def t98_truc_phan_biet_la_NEN_chu_khong_phai_TEN_TEP():
    """Cặp với `t73`: CÙNG tuple, ĐỔI mỗi nền, phải ra kết quả NGƯỢC nhau.

    `t73` một mình chỉ chứng minh "posix thì không bỏ qua". Nó KHÔNG chứng minh quyết
    định ấy tra theo NỀN: thay mệnh đề nền bằng phân biệt theo TÊN TỆP vẫn cho 97/97,
    rc=0 khi chạy cục bộ trên Linux (đo 23-08-2026). Ca này khoá đúng cái trục ấy.

    Đi qua `main()`, KHÔNG gọi thẳng `_ly_do_bo_qua_workflow` — tuân `r4/Q8`.
    """
    def bo(): raise BoQuaNen(WORKFLOW_DANG, "dang")
    rc, out = _chay_main_meta(bo, "nt")
    bang(rc == 0 and "bỏ qua=1" in out,
         f"cùng tuple mà nền nt KHÔNG bỏ qua: rc={rc}, {out!r}")


@ca
def t99_con_tro_treo_chan_xau_khong_chan_ten_truong_cua_spec_va_quet_nguoc():
    import contextlib
    import io
    mod = _nap_cong()
    truong, khoa = "vung_duoc_phep_cham", "tham_chieu_truong_lease"
    bang(mod._cac_con_tro_treo({khoa: [truong]}) == [truong],
         "không thấy tham chiếu cấu trúc đang treo")
    bang(not mod._cac_con_tro_treo({khoa: [truong], truong: "x"}),
         "chặn oan trường đã được định nghĩa")
    for van in ("`Vung_Duoc_Phep_Cham`", "vùng_được_phép_chạm", truong):
        bang(mod._cac_nhac_mo_ho({"ghi_chu": "minh hoạ " + van}) == [truong],
             f"văn xuôi không thành advisory: {van!r}")

    with San() as s:
        (s / ".git").mkdir()
        mod.GOI_GIT = _GitKhoGia({"a"}, {"a"}, [])
        cases = [
            ("comment", {}, f"# comment YAML nhắc `{truong}`\n", True),
            ("minh-hoa", {"ghi_chu": f"tên biến minh hoạ là `{truong}`"}, "", True),
            ("treo", {khoa: [truong]}, "", False),
            ("da-co", {khoa: [truong], truong: "x"}, "", True),
        ]
        for ten, them, duoi, phai_qua in cases:
            lease = lease_mau(lease_id="KIEM-" + ten, **them)
            p = viet(s, lease, ten=ten + ".yaml")
            if duoi:
                p.write_text(p.read_text(encoding="utf-8") + duoi, encoding="utf-8")
            try:
                _kiem_sach(mod, lease, p, s)
            except mod.Chan as ex:
                bang(not phai_qua and ex.ma == RC_NOI_DUNG and "con trỏ treo" in ex.thong_diep,
                     f"check chặn sai {ten}: {ex.ma} {ex.thong_diep}")
            else:
                bang(phai_qua, f"check không chặn tham chiếu thật sự treo: {ten}")

    raw_xau = "lease_id: TREO\nlease_expires_at_utc: '2099-01-01T00:00:00Z'\n" \
              f"write_set: [x.py]\n{khoa}: [{truong}, {truong}]\n"
    raw_cu = raw_xau.replace("TREO", "CU").replace("2099", "2000")
    raw_tot = raw_xau.replace("TREO", "TOT").replace("write_set:", f"{truong}: x\nwrite_set:")
    raw_chet = raw_xau.replace("TREO", "DA_CHET") + "da_bi_thay_the: MOI\n"
    raw_goi_y = raw_xau.replace("TREO", "GOI-Y").replace(
        f"{khoa}: [{truong}, {truong}]", f"ghi_chu: vùng_được_phép_chạm")
    git = _GitKhoGia({"a"}, {"a"}, [
        ("refs/remotes/origin/a", "ops/leases/xau.yaml", raw_xau),
        ("refs/remotes/origin/a", "ops/leases/cu.yaml", raw_cu),
        ("refs/remotes/origin/a", "ops/leases/tot.yaml", raw_tot),
        ("refs/remotes/origin/a", "ops/leases/chet.yaml", raw_chet),
        ("refs/remotes/origin/a", "ops/leases/goi-y.yaml", raw_goi_y)])
    mod.GOI_GIT, out = git, io.StringIO()
    with contextlib.redirect_stdout(out):
        rc = mod.lenh_con_tro_treo(type("A", (), {"goc": "."})())
    s = out.getvalue()
    hang = [x.split("\t") for x in s.splitlines() if x.startswith("CON_TRỎ_TREO\t")]
    tong = [x for x in s.splitlines() if x.startswith("CON_TRỎ_TREO ")]
    goi_y = [x.split("\t") for x in s.splitlines() if x.startswith("CON_TRỎ_GỢI_Ý\t")]
    bang(rc == 0 and len(hang) == 1 and len(hang[0]) == 4 and
         hang[0][1:3] == ["TREO", truong], f"hàng dữ liệu sai schema/dedup: {s!r}")
    bang(len(tong) == 1 and tong[0].split()[1].rstrip(";") == "1",
         f"tổng kết không bằng 1: {tong!r}")
    bang(len(goi_y) == 1 and len(goi_y[0]) == 4 and goi_y[0][1] == "GOI-Y",
         f"văn xuôi không đi ra advisory có schema: {goi_y!r}")


@ca
def t100_bia_mo_doi_dau_cu_thieu_danh_dau_nhung_cho_ca_dung():
    mod = _nap_cong()
    moi = lease_mau(lease_id="MOI", thay_the_cho="CU")
    with San() as s:
        (s / ".git").mkdir()
        p = viet(s, moi)
        for marker, phai_qua in ((None, False), ("MOI", True)):
            cu = _lease_quet("CU", da_bi_thay_the=marker)
            mod.GOI_GIT = _GitKhoGia({"a"}, {"a"}, [
                ("refs/remotes/origin/a", "ops/leases/cu.yaml", cu)])
            try:
                _kiem_sach(mod, moi, p, s)
            except mod.Chan as ex:
                bang(not phai_qua and ex.ma == RC_NOI_DUNG and
                     "da_bi_thay_the: MOI" in ex.thong_diep and "CU" in ex.thong_diep,
                     f"bia mộ bị chặn sai: {ex.ma} {ex.thong_diep}")
            else:
                bang(phai_qua, "lease cũ chưa đánh dấu mà bia mộ mới vẫn qua")


@ca
def t101_dot_bien_con_tro_treo_va_bia_mo_deu_bi_giet():
    import importlib
    import importlib.util
    nguon, giet = SCRIPT.read_text(encoding="utf-8"), 0
    muts = [
        ("quet-raw", "_kiem_con_tro_treo(lease)",
         '_kiem_con_tro_treo({"tham_chieu_truong_lease": re.findall('
         'r"`([a-z_][a-z0-9_]*)`", Path(tep).read_text(encoding="utf-8"))})',
         t99_con_tro_treo_chan_xau_khong_chan_ten_truong_cua_spec_va_quet_nguoc),
        ("bo-tham-chieu", "treo = _cac_con_tro_treo(lease)", "treo = []",
         t99_con_tro_treo_chan_xau_khong_chan_ten_truong_cua_spec_va_quet_nguoc),
        ("bo-vong-lenh", "for muc in _quet_lease_toan_kho(root):", "for muc in []:",
         t99_con_tro_treo_chan_xau_khong_chan_ten_truong_cua_spec_va_quet_nguoc),
        ("bia-mo", "if not thay_the_cho:\n        return", "if True:\n        return",
         t100_bia_mo_doi_dau_cu_thieu_danh_dau_nhung_cho_ca_dung),
    ]
    with San() as s:
        sys.dont_write_bytecode = True
        for i, (ten, cu, moi, dich) in enumerate(muts):
            bang(nguon.count(cu) == 1, f"neo mutant {ten} không duy nhất")
            p = s / f"mut_{i}.py"
            p.write_text(nguon.replace(cu, moi), encoding="utf-8")
            importlib.invalidate_caches()
            spec = importlib.util.spec_from_file_location(f"lp_new_m{i}", p)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            cu_nap = globals()["_nap_cong"]
            globals()["_nap_cong"] = lambda: mod
            try:
                dich()
            except AssertionError:
                giet += 1
            finally:
                globals()["_nap_cong"] = cu_nap
    print(f"đột biến packet #313: đã chạy={len(muts)}, bị giết={giet}")
    bang(giet == len(muts), f"đột biến packet #313 chỉ bị giết {giet}/{len(muts)}")


def _chay_nhanh_gia(trai=0, phai=0, co_origin=True, leases=()):
    import contextlib, io
    mod, out = _nap_cong(), io.StringIO()
    co = {"a"} if co_origin else set()
    mod.GOI_GIT = _GitKhoGia(co, co, leases, heads={"a"}, lech={"a": (trai, phai)})
    with contextlib.redirect_stdout(out):
        try:
            rc = mod.lenh_ai_dang_giu(type("A", (), {"goc": ".", "duong_dan":
                                                       "ops/lease_publish.py"})())
        except mod.Chan as ex:
            return ex.ma, out.getvalue() + ex.thong_diep, mod
    return rc, out.getvalue(), mod


@ca
def t102_nhanh_cuc_bo_tut_sau_phai_CHAN_truoc_khu_trung_lease_id():
    ls = [("refs/heads/a", "ops/leases/x.yaml", _lease_quet("L")),
          ("refs/remotes/origin/a", "ops/leases/x.yaml",
           _lease_quet("L", da_bi_thay_the="M"))]
    rc, out, mod = _chay_nhanh_gia(0, 1, leases=ls)
    bang(rc == mod.RC_KHONG_XAC_DINH and "NHÁNH_CỤC_BỘ_TỤT_SAU: a" in out
         and "git branch -f a refs/remotes/origin/a" in out
         and "NGƯỜI_GIỮ" not in out, f"không chặn nhánh tụt sau trước dedup: {rc} {out}")


@ca
def t103_nhanh_cuc_bo_bang_origin_phai_QUA():
    rc, out, _ = _chay_nhanh_gia(0, 0)
    bang(rc == RC_OK and "quét refs/heads/*" in out and "NGƯỜI_GIỮ 0" in out,
         f"chặn oan nhánh bằng origin: {rc} {out}")


@ca
def t104_nhanh_cuc_bo_di_truoc_origin_phai_QUA():
    rc, out, _ = _chay_nhanh_gia(3, 0)
    bang(rc == RC_OK and "NGƯỜI_GIỮ 0" in out, f"chặn oan nhánh đi trước: {rc} {out}")


@ca
def t105_nhanh_cuc_bo_khong_co_origin_phai_QUA():
    rc, out, _ = _chay_nhanh_gia(co_origin=False)
    bang(rc == RC_OK and "NGƯỜI_GIỮ 0" in out, f"chặn oan nhánh thuần cục bộ: {rc} {out}")


@ca
def t106_cung_lease_id_khac_noi_dung_chi_dem_MOT():
    ls = [("refs/remotes/origin/a", "ops/leases/x.yaml", _lease_quet("L")),
          ("refs/remotes/origin/b", "ops/leases/x.yaml",
           _lease_quet("L", posted_comment_id=7))]
    rc, out, mod = _quet_gia(_GitKhoGia({"a", "b"}, {"a", "b"}, ls))
    bang(rc == mod.RC_DANG_GIU and out.count("\tL\t") == 2
         and "NGƯỜI_GIỮ 1: L" in out, f"không dedup theo lease_id: {rc} {out}")


@ca
def t107_hai_lease_id_khac_nhau_phai_dem_HAI():
    ls = [("refs/remotes/origin/a", "ops/leases/a.yaml", _lease_quet("L1")),
          ("refs/remotes/origin/b", "ops/leases/b.yaml", _lease_quet("L2"))]
    rc, out, mod = _quet_gia(_GitKhoGia({"a", "b"}, {"a", "b"}, ls))
    bang(rc == mod.RC_DANG_GIU and "NGƯỜI_GIỮ 2: L1, L2" in out,
         f"nuốt hai lease khác nhau: {rc} {out}")


@ca
def t108_moi_chot_ref_cuc_bo_co_dot_bien_rieng():
    import importlib, importlib.util
    nguon, giet = SCRIPT.read_text(encoding="utf-8"), 0
    dieu_kien = "if trai == 0 and phai > 0:"
    muts = [
        ("tut-sau", dieu_kien, "if False:", t102_nhanh_cuc_bo_tut_sau_phai_CHAN_truoc_khu_trung_lease_id),
        ("bang", dieu_kien, "if trai == 0:", t103_nhanh_cuc_bo_bang_origin_phai_QUA),
        ("di-truoc", dieu_kien, "if trai > 0 and phai == 0:", t104_nhanh_cuc_bo_di_truoc_origin_phai_QUA),
        ("khong-origin", "if not doi_ung:\n            continue",
         "if not doi_ung:\n            tut_sau.append(ten)\n            continue",
         t105_nhanh_cuc_bo_khong_co_origin_phai_QUA),
        ("dedup", "nguoi_giu[lease_id] = None", 'nguoi_giu[lease_id + muc["ref"]] = None',
         t106_cung_lease_id_khac_noi_dung_chi_dem_MOT),
        ("hai-lease", "nguoi_giu[lease_id] = None", 'nguoi_giu["MỘT"] = None',
         t107_hai_lease_id_khac_nhau_phai_dem_HAI),
    ]
    with San() as s:
        sys.dont_write_bytecode = True
        for i, (ten, cu, moi, dich) in enumerate(muts):
            bang(nguon.count(cu) == 1, f"neo mutant {ten} không duy nhất")
            p = s / f"mut_ref_{i}.py"; p.write_text(nguon.replace(cu, moi), encoding="utf-8")
            importlib.invalidate_caches()
            spec = importlib.util.spec_from_file_location(f"lp_ref_m{i}", p)
            mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
            cu_nap = globals()["_nap_cong"]; globals()["_nap_cong"] = lambda: mod
            try: dich()
            except AssertionError: giet += 1
            finally: globals()["_nap_cong"] = cu_nap
    print(f"đột biến ref cục bộ: đã chạy={len(muts)}, bị giết={giet}")
    bang(giet == len(muts), f"đột biến ref cục bộ chỉ bị giết {giet}/{len(muts)}")


def _git_fixture(goc: Path, *args) -> str:
    p = subprocess.run(["git", *args], cwd=goc, capture_output=True, text=True)
    bang(p.returncode == 0, f"fixture git {' '.join(args)} rc={p.returncode}: {p.stderr}")
    return p.stdout.strip()


def _kho_tut_sau(s: Path, trang="ranh") -> tuple[Path, Path | None]:
    kho = s / "kho"; kho.mkdir()
    _git_fixture(kho, "init", "-q", "-b", "main")
    _git_fixture(kho, "config", "user.name", "Test")
    _git_fixture(kho, "config", "user.email", "test@example.invalid")
    _git_fixture(kho, "config", "commit.gpgsign", "false")
    (kho / "x").write_text("cu\n", encoding="utf-8")
    _git_fixture(kho, "add", "x")
    _git_fixture(kho, "commit", "-qm", "cu")
    _git_fixture(kho, "branch", "a")
    _git_fixture(kho, "commit", "--allow-empty", "-qm", "moi")
    _git_fixture(kho, "remote", "add", "origin", ".")
    _git_fixture(kho, "update-ref", "refs/remotes/origin/a", "HEAD")
    _git_fixture(kho, "branch", "--set-upstream-to=origin/a", "a")
    wt = s / "wt giu" if trang != "ranh" else None
    if wt is not None:
        _git_fixture(kho, "worktree", "add", "-q", str(wt), "a")
        if trang == "prunable":
            import shutil; shutil.rmtree(wt)
        elif trang == "hai":
            _git_fixture(kho, "worktree", "add", "--force", "-q", str(s / "wt 2"), "a")
        elif trang == "ban":
            (wt / "x").write_text("ban\n", encoding="utf-8")
        elif trang == "merge":
            _git_fixture(wt, "merge", "--no-commit", "--no-ff", "refs/remotes/origin/a")
        elif trang == "rebase":
            p = subprocess.run(["git", "rebase", "--root", "--exec", "false"], cwd=wt, capture_output=True, text=True)
            bang(p.returncode == 1, f"không dựng được rebase dở: {p.returncode} {p.stderr}")
    return kho, wt


def _thi_hanh_lenh_chua(kho: Path) -> tuple[str, int, str]:
    rc, _, err = chay("ai-dang-giu", "ops/lease_publish.py", "--root", kho, cwd=kho)
    bang(rc == 12 and "chữa: " in err, f"cổng không in lệnh chữa: rc={rc}, {err!r}")
    lenh = err.split("chữa: ", 1)[1].strip()
    p = subprocess.run(shlex.split(lenh), cwd=kho, capture_output=True, text=True)
    hai_ref = _git_fixture(kho, "rev-parse", "refs/heads/a",
                          "refs/remotes/origin/a").splitlines()
    bang(p.returncode == 0 and len(hai_ref) == 2 and hai_ref[0] == hai_ref[1],
         f"lệnh chữa không chạy/không khớp ref: {lenh!r}, rc={p.returncode}, "
         f"refs={hai_ref}, err={p.stderr!r}")
    return lenh, p.returncode, hai_ref[0]


@ca
def t109_lenh_chua_nhanh_ranh_phai_chay_duoc_va_khop_origin():
    with San() as s:
        kho, _ = _kho_tut_sau(s)
        lenh, rc, _ = _thi_hanh_lenh_chua(kho)
        bang(rc == 0 and lenh == "git branch -f a refs/remotes/origin/a",
             f"nhánh rảnh không giữ lệnh branch -f: {lenh!r}")


@ca
def t110_lenh_chua_nhanh_bi_worktree_giu_phai_chay_duoc_va_khop_origin():
    with San() as s:
        kho, wt = _kho_tut_sau(s, "sach")
        lenh, rc, _ = _thi_hanh_lenh_chua(kho)
        doi_so = shlex.split(lenh)
        bang(rc == 0 and doi_so[:2] == ["git", "-C"] and Path(doi_so[2]).resolve() == wt.resolve()
             and doi_so[3:] == ["merge", "--ff-only", "refs/remotes/origin/a"],
             f"lệnh không nêu đúng worktree bị giữ: {lenh!r}")


def _tu_choi_worktree(trang, dau):
    with San() as s:
        kho, wt = _kho_tut_sau(s, trang)
        rc, _, err = chay("ai-dang-giu", "ops/lease_publish.py", "--root", kho, cwd=kho)
        bang(rc == 12 and "KHÔNG_PHÁT_LỆNH_CHỮA" in err and f"{s.name}/{wt.name}" in err and dau in err
             and "Người dùng tự" in err and "chạy lại cổng" in err
             and not any(x in err for x in ("git branch -f", "git -C", "merge --ff-only")),
             f"không từ chối {trang}: rc={rc} neo={s.name}/{wt.name!r} wt={wt.as_posix()!r} err={err}")
        if trang == "hai": bang(f"{s.name}/wt 2" in err, f"thiếu worktree thứ hai: {err}")
        if trang == "rebase":
            por = _git_fixture(kho, "worktree", "list", "--porcelain")
            bang("detached" in por and "branch refs/heads/a" not in por, f"chưa đo detached rebase: {por} {err}")


@ca
def t111_allowlist_worktree_nam_trang_thai_va_dot_bien():
    global SCRIPT
    ca_tu_choi = {"prunable": "PRUNABLE", "hai": "GIỮ_BỞI_2_WORKTREE", "ban": "BẨN",
                  "merge": "MERGE", "rebase": "REBASE"}
    for trang, dau in ca_tu_choi.items(): _tu_choi_worktree(trang, dau)
    nguon, ban_goc = SCRIPT.read_text(encoding="utf-8"), SCRIPT
    muts = [("prunable", 'if "prunable" in muc:', "if False:", {"prunable"}),
            ("last-wins", 'giu = [wt for wt in worktrees if wt.get("branch") == ref]',
             'giu = list({wt.get("branch"): wt for wt in worktrees if wt.get("branch") == ref}.values())', {"hai"}),
            ("sạch", 'if _git(p, "status", "--porcelain").strip():', "if False:", {"ban"}),
            ("thao-tác-dở", "if ten in meta]", "if False]", {"merge", "rebase"}),
            ("vô-điều-kiện", "if not an_toan:", "if False:", set(ca_tu_choi))]
    with San() as s:
        for i, (ten, cu, moi, dich) in enumerate(muts):
            bang(nguon.count(cu) == 1, f"neo mutant {ten} không duy nhất")
            p = s / f"mut_wt_{i}.py"; p.write_text(nguon.replace(cu, moi), encoding="utf-8")
            SCRIPT, do = p, set()
            for trang, dau in ca_tu_choi.items():
                try: _tu_choi_worktree(trang, dau)
                except AssertionError: do.add(trang)
            t109_lenh_chua_nhanh_ranh_phai_chay_duoc_va_khop_origin(); t110_lenh_chua_nhanh_bi_worktree_giu_phai_chay_duoc_va_khop_origin(); song = 2
            print(f"đột biến {ten}: ĐỎ={sorted(do)}, đối chứng cho phép sống={song}")
            bang(do == dich and song == 2, f"mutant {ten}: ĐỎ={do}, cho phép sống={song}")
    SCRIPT = ban_goc


_CAC_CA_UPSTREAM = {
    # remote/local biểu diễn ref có mặt; cấu_hình và đối_ứng là hai khái niệm riêng.
    "tutsau": ({"tutsau"}, {"tutsau"}, "", "refs/remotes/origin/tutsau", (0, 1)),
    "phanky": ({"phanky"}, {"phanky"}, "", "refs/remotes/origin/phanky", (1, 1)),
    "main": ({"main"}, {"main"}, "", "refs/remotes/origin/main", (0, 1)),
    "bang": ({"bang"}, {"bang"}, "", "refs/remotes/origin/bang", (0, 0)),
    "ditruoc": ({"ditruoc"}, {"ditruoc"}, "", "refs/remotes/origin/ditruoc", (1, 0)),
    "thuancucbo": (set(), set(), "", "", (0, 0)),
    "khacten": ({"main"}, {"main"}, "refs/remotes/origin/main",
                 "refs/remotes/origin/main", (1, 1)),
    "khactensau": ({"main"}, {"main"}, "refs/remotes/origin/main",
                    "refs/remotes/origin/main", (0, 1)),
    "khaihong": ({"khaihong"}, {"khaihong"}, "", "", (0, 1)),
    "khaihongkhongref": (set(), set(), "", "", (0, 1)),
    "remotecham": ({"main"}, {"main"}, "refs/heads/main", "refs/heads/main", (1, 0)),
    "tagup": (set(), set(), "refs/tags/v1", "refs/tags/v1", (0, 0)),
    "tagupsau": (set(), set(), "refs/tags/v1", "refs/tags/v1", (0, 1)),
    "tagpeel": (set(), set(), "refs/tags/vann^{}", "refs/tags/vann^{}", (0, 1)),
    "refnamesai": (set(), set(), "refs/heads/ten sai", "refs/heads/ten sai", (0, 1)),
    "refcodau": (set(), set(), "--help", "--help", (0, 1)),
}

_CAU_HINH_UPSTREAM = {
    "khacten": ("origin", "refs/heads/main"),
    "khactensau": ("origin", "refs/heads/main"),
    "khaihong": ("khongcorenote", "refs/heads/khaihong"),
    "khaihongkhongref": ("khongcorenote", "refs/heads/khaihongkhongref"),
    "remotecham": (".", "refs/heads/main"),
    "tagup": (".", "refs/tags/v1"),
    "tagupsau": (".", "refs/tags/v1"),
    "tagpeel": (".", "refs/tags/vann^{}"),
    "refnamesai": (".", "refs/heads/ten sai"),
    "refcodau": (".", "--help"),
}


def _chay_ca_upstream(ten):
    import contextlib, io
    remote, local, cau_hinh, _, lech = _CAC_CA_UPSTREAM[ten]
    mod, out = _nap_cong(), io.StringIO()
    cap = _CAU_HINH_UPSTREAM.get(ten)
    configs = ({f"branch.{ten}.remote": cap[0], f"branch.{ten}.merge": cap[1]}
               if cap else {})
    heads = {ten, "main"} if ten == "remotecham" else {ten}
    tags = ({"vann"} if ten == "tagpeel" else
            {cau_hinh.removeprefix("refs/tags/")} if cau_hinh.startswith("refs/tags/") else set())
    mod.GOI_GIT = _GitKhoGia(remote, local, [], heads=heads, lech={ten: lech},
                             upstreams={ten: cau_hinh} if cau_hinh else {}, configs=configs,
                             tags=tags)
    with contextlib.redirect_stdout(out):
        try:
            rc = mod.lenh_ai_dang_giu(type("A", (), {"goc": ".", "duong_dan":
                                                       "ops/lease_publish.py"})())
        except mod.Chan as ex:
            return ex.ma, out.getvalue() + ex.thong_diep, mod
    return rc, out.getvalue(), mod


def _kiem_ca_upstream(ten):
    rc, out, mod = _chay_ca_upstream(ten)
    lenh_nguy_hiem = ("git branch -f", "git -C", "merge --ff-only")
    if ten in {"bang", "ditruoc", "thuancucbo", "remotecham", "tagup"}:
        bang(rc == mod.RC_OK and "NGƯỜI_GIỮ 0" in out and
             not any(x in out for x in lenh_nguy_hiem),
             f"{ten} bị chặn oan: rc={rc} {out}")
    elif ten in {"khaihong", "khaihongkhongref", "tagpeel", "refnamesai", "refcodau"}:
        dau = (f"{ten} có config upstream nhưng không giải được" if ten.startswith("khaihong")
               else "KHÔNG_XÁC_ĐỊNH:")
        bang(rc == mod.RC_KHONG_XAC_DINH and
             dau in out and
             not any(x in out for x in lenh_nguy_hiem),
             f"{ten} không fail-close an toàn: rc={rc} {out}")
    elif ten in {"phanky", "khacten"}:
        upstream = _CAC_CA_UPSTREAM[ten][3]
        bang(rc == mod.RC_KHONG_XAC_DINH and
             f"NHÁNH_CỤC_BỘ_PHÂN_KỲ: {ten} -> {upstream} (1/1)" in out and
             "KHÔNG_PHÁT_LỆNH_CHỮA" in out and not any(x in out for x in lenh_nguy_hiem),
             f"{ten} không chẩn đoán an toàn: rc={rc} {out}")
    else:
        upstream = _CAC_CA_UPSTREAM[ten][3]
        bang(rc == mod.RC_KHONG_XAC_DINH and
             f"NHÁNH_CỤC_BỘ_TỤT_SAU: {ten} -> {upstream} (0/1)" in out and
             f"git branch -f {ten} {upstream}" in out,
             f"{ten} không giữ lệnh chữa đúng upstream: rc={rc} {out}")
    return rc, out


@ca
def t112_cac_ca_khoa_upstream_that_va_bon_trang_thai():
    for ten in _CAC_CA_UPSTREAM:
        rc, out = _kiem_ca_upstream(ten)
        print(f"ca upstream {ten}: rc={rc}; " + " | ".join(out.strip().splitlines()))


@ca
def t113_sau_dot_bien_upstream_va_phan_ky_deu_bi_giet():
    global SCRIPT
    nguon, ban_goc = SCRIPT.read_text(encoding="utf-8"), SCRIPT
    tat_ca = set(_CAC_CA_UPSTREAM)
    muts = [
        ("go-phat-hien-phan-ky", "elif trai > 0 and phai > 0:", "elif False:",
         {"phanky", "khacten"}),
        ("phan-ky-thanh-tut-sau", 'trang_thai = "PHÂN_KỲ"', 'trang_thai = "TỤT_SAU"',
         {"phanky", "khacten"}),
        ("doi-ung-theo-ten", 'doi_ung = upstream.get(ref, "")',
         'doi_ung = ("refs/remotes/origin/" + ten if "refs/remotes/origin/" + ten in tap_ref else "")',
         {"khacten", "khactensau", "khaihong", "remotecham", "tagup", "tagupsau"}),
        ("ton-tai-lai-hoi-tap-ref", "if doi_ung and not _ref_ton_tai(goc, doi_ung):",
         "if doi_ung and doi_ung not in tap_ref:", {"tagup", "tagupsau"}),
        ("go-phat-hien-khai-hong", "if co_cau_hinh and not doi_ung:", "if False:",
         {"khaihong", "khaihongkhongref"}),
        ("khai-hong-lui-ve-ten",
         "if co_cau_hinh and not doi_ung:\n"
         "            raise Chan(RC_KHONG_XAC_DINH,\n"
         "                       f\"KHÔNG_XÁC_ĐỊNH: {ten} có config upstream nhưng không giải được: \"\n"
         "                       f\"branch.{ten}.remote={remote!r}, branch.{ten}.merge={merge!r}\")",
         "if co_cau_hinh and not doi_ung:\n"
         "            ung_vien = \"refs/remotes/origin/\" + ten\n"
         "            if ung_vien in tap_ref: doi_ung = ung_vien\n"
         "            else:\n"
         "                raise Chan(RC_KHONG_XAC_DINH,\n"
         "                           f\"KHÔNG_XÁC_ĐỊNH: {ten} có config upstream nhưng không giải được: \"\n"
         "                           f\"branch.{ten}.remote={remote!r}, branch.{ten}.merge={merge!r}\")",
         {"khaihong"}),
        ("chan-remote-cham", "if co_cau_hinh and not doi_ung:",
         'if co_cau_hinh and (not doi_ung or remote == "."):',
         {"remotecham", "tagup", "tagupsau"}),
        ("chan-khong-upstream", "if not doi_ung:\n            continue",
         'if not doi_ung:\n            tut_sau.append((ten, "refs/remotes/origin/" + ten, 0, 1, "TỤT_SAU"))\n            continue',
         {"thuancucbo"}),
        ("go-chot-quan-he-ref",
         'tut_sau = [m for m in bi_chan if _thong_tin_nhanh_bi_chan(m)[-1] == "TỤT_SAU"]',
         "tut_sau = list(bi_chan)", {"phanky", "khacten"}),
        ("go-lui-ve-ten",
         'if not doi_ung:\n'
         '            ung_vien = "refs/remotes/origin/" + ten\n'
         '            if ung_vien in tap_ref:\n'
         '                doi_ung = ung_vien',
         'if False:\n'
         '            doi_ung = ""', {"main", "phanky", "tutsau"}),
    ]
    sys.dont_write_bytecode = True
    try:
        for i, (ten_mut, cu, moi, do_dung) in enumerate(muts):
            bang(nguon.count(cu) == 1, f"neo mutant {ten_mut} không duy nhất")
            with San() as s:  # mỗi mutant một thư mục: không thể dùng nhầm .pyc cùng giây/kích thước
                p = s / f"mut_upstream_{i}.py"
                p.write_text(nguon.replace(cu, moi), encoding="utf-8")
                SCRIPT, do = p, set()
                for ten_ca in _CAC_CA_UPSTREAM:
                    try: _kiem_ca_upstream(ten_ca)
                    except AssertionError: do.add(ten_ca)
                song = tat_ca - do
                print(f"đột biến {ten_mut}: thư_mục={s.name}; ĐỎ={sorted(do)}, đối chứng SỐNG={sorted(song)}")
                bang(do == do_dung and song == tat_ca - do_dung,
                     f"mutant {ten_mut}: ĐỎ={do}, SỐNG={song}")
    finally:
        SCRIPT = ban_goc


@ca
def t114_khong_config_nhung_co_origin_cung_ten_phai_duoc_phan_loai():
    for ten in ("tutsau", "phanky"):
        remote, local, cau_hinh, doi_ung, _ = _CAC_CA_UPSTREAM[ten]
        bang(not cau_hinh and ten in remote and ten in local,
             f"git giả chưa tách config khỏi ref cho {ten}")
        rc, out = _kiem_ca_upstream(ten)
        bang(rc == 12 and doi_ung in out,
             f"không khóa population thiếu config + có origin cùng tên: {ten}: {out}")


def _kiem_tag_khong_nam_trong_pham_vi_quet_lease():
    lease = _lease_quet("LEASE-TREN-TAG")
    git = _GitKhoGia(set(), set(), [("refs/tags/v1", "ops/leases/tag.yaml", lease)],
                     tags={"v1"})
    rc, out, mod = _quet_gia(git)
    bang(rc == mod.RC_OK and "LEASE-TREN-TAG" not in out and "NGƯỜI_GIỮ 0" in out,
         f"lease trên tag bị quét: rc={rc} {out}")


@ca
def t115_tag_khong_nam_trong_pham_vi_quet_lease_va_dot_bien():
    global SCRIPT
    import importlib
    _kiem_tag_khong_nam_trong_pham_vi_quet_lease()
    nguon, ban_goc = SCRIPT.read_text(encoding="utf-8"), SCRIPT
    cu = '_git(goc, "for-each-ref", "--format=%(refname)", "refs/heads", "refs/remotes")'
    moi = '_git(goc, "for-each-ref", "--format=%(refname)", "refs/heads", "refs/remotes", "refs/tags")'
    bang(nguon.count(cu) == 1, "neo mutant mở phạm vi tag không duy nhất")
    with San() as s:  # mutant riêng một thư mục để không tái dùng nhầm bytecode
        p = s / "mut_mo_pham_vi_quet_tag.py"
        p.write_text(nguon.replace(cu, moi), encoding="utf-8")
        sys.dont_write_bytecode = True
        importlib.invalidate_caches()
        SCRIPT = p
        try:
            try:
                _kiem_tag_khong_nam_trong_pham_vi_quet_lease()
            except AssertionError:
                do = {"tag-khong-quet"}
            else:
                do = set()
            song = set()
            for ten in ("tagup", "remotecham"):
                _kiem_ca_upstream(ten)
                song.add(ten)
            print(f"đột biến mở-phạm-vi-quét-tag: thư_mục={s.name}; "
                  f"ĐỎ={sorted(do)}, đối chứng SỐNG={sorted(song)}")
            bang(do == {"tag-khong-quet"} and song == {"tagup", "remotecham"},
                 f"mutant mở tag: ĐỎ={do}, SỐNG={song}")
        finally:
            SCRIPT = ban_goc


@ca
def t116_ref_chinh_xac_hinh_dang_va_bon_dot_bien_bat_buoc():
    global SCRIPT
    import importlib
    def kiem_dich(ten):
        _, out = _kiem_ca_upstream(ten)
        if ten in {"tagpeel", "refnamesai"}:
            bang(f"git check-ref-format {_CAC_CA_UPSTREAM[ten][2]}" in out,
                 f"{ten} không bị chặn bởi phép kiểm hình dạng: {out}")
        elif ten == "refcodau":
            bang("hình dạng không an toàn" in out and "bắt đầu bằng '-'" in out,
                 f"refcodau không bị chặn bởi chốt Python: {out}")
    for ten in ("tagpeel", "refnamesai", "refcodau", "tagup"):
        kiem_dich(ten)
    nguon, ban_goc = SCRIPT.read_text(encoding="utf-8"), SCRIPT
    muts = [
        ("go-chot-dau-tru", '        if ref.startswith("-"):\n'
         '            raise Chan(RC_KHONG_XAC_DINH,\n'
         '                       f"KHÔNG_XÁC_ĐỊNH: ref có hình dạng không an toàn "\n'
         '                       f"(bắt đầu bằng \'-\'): {ref}")\n',
         '', {"refcodau"}),
        ("rev-parse",
         'hinh_dang = GOI_GIT("check-ref-format", ref, cwd=goc)\n'
         '        if hinh_dang.returncode != 0:\n'
         '            ly = (hinh_dang.stderr or hinh_dang.stdout or "refname không hợp lệ").strip()\n'
         '            raise Chan(RC_KHONG_XAC_DINH,\n'
         '                       f"KHÔNG_XÁC_ĐỊNH: git check-ref-format {ref} "\n'
         '                       f"rc={hinh_dang.returncode}: {ly.splitlines()[0][:200]}")\n'
         '        p = GOI_GIT("show-ref", "--verify", "--quiet", "--", ref, cwd=goc)',
         'p = GOI_GIT("rev-parse", "--verify", "--quiet", "--end-of-options", ref, cwd=goc)',
         {"tagpeel", "refnamesai"}),
        ("go-check-ref-format", 'hinh_dang = GOI_GIT("check-ref-format", ref, cwd=goc)',
         'hinh_dang = subprocess.CompletedProcess([], 0, "", "")', {"tagpeel", "refnamesai"}),
        ("mo-pham-vi-tag",
         '_git(goc, "for-each-ref", "--format=%(refname)", "refs/heads", "refs/remotes")',
         '_git(goc, "for-each-ref", "--format=%(refname)", "refs/heads", "refs/remotes", "refs/tags")',
         {"tag-khong-quet"}),
        ("chan-tag-that", "if p.returncode == 0:\n        return True",
         'if p.returncode == 0 and not ref.startswith("refs/tags/"):\n        return True', {"tagup"}),
    ]
    sys.dont_write_bytecode = True
    try:
        for i, (ten_mut, cu, moi, do_dung) in enumerate(muts):
            bang(nguon.count(cu) == 1, f"neo mutant {ten_mut} không duy nhất")
            with San() as s:
                p = s / f"mut_ref_exact_{i}.py"
                p.write_text(nguon.replace(cu, moi), encoding="utf-8")
                importlib.invalidate_caches(); SCRIPT, do = p, set()
                for ten_ca in ("tagpeel", "refnamesai", "refcodau", "tagup"):
                    try: kiem_dich(ten_ca)
                    except AssertionError: do.add(ten_ca)
                if ten_mut == "mo-pham-vi-tag":
                    try: _kiem_tag_khong_nam_trong_pham_vi_quet_lease()
                    except AssertionError: do.add("tag-khong-quet")
                print(f"đột biến bắt buộc {ten_mut}: thư_mục={s.name}; ĐỎ={sorted(do)}")
                bang(do == do_dung, f"mutant {ten_mut}: ĐỎ={do}, cần={do_dung}")
    finally:
        SCRIPT = ban_goc


def _quet_ca_bia_mo(leases, duong="ops/lease_publish.py"):
    import contextlib
    import io
    mod, out = _nap_cong(), io.StringIO()
    mod.GOI_GIT = _GitKhoGia({"a"}, {"a"}, leases)
    with contextlib.redirect_stdout(out):
        try:
            rc = mod.lenh_ai_dang_giu(
                type("A", (), {"goc": ".", "duong_dan": duong})())
        except mod.Chan as ex:
            return ex.ma, out.getvalue() + ex.thong_diep, mod
    return rc, out.getvalue(), mod


@ca
def t117_bia_mo_tro_lease_khong_ton_tai_phai_KHONG_XAC_DINH():
    ls = [("refs/remotes/origin/a", "ops/leases/cu.yaml",
           _lease_quet("CU", da_bi_thay_the="KHONG-TON-TAI"))]
    rc, out, mod = _quet_ca_bia_mo(ls)
    bang(rc == mod.RC_KHONG_XAC_DINH and "KHÔNG_XÁC_ĐỊNH" in out
         and "CU" in out and "KHONG-TON-TAI" in out
         and "NGƯỜI_GIỮ" not in out,
         f"bia mộ trỏ tên không tồn tại vẫn gỡ khoá: rc={rc} {out}")


@ca
def t118_bia_mo_co_lease_moi_nhung_khong_tro_nguoc_phai_CHAN():
    ls = [("refs/remotes/origin/a", "ops/leases/cu.yaml",
           _lease_quet("CU", da_bi_thay_the="MOI")),
          ("refs/remotes/origin/a", "ops/leases/moi.yaml",
           _lease_quet("MOI", thay_the_cho="CU-sai"))]
    rc, out, mod = _quet_ca_bia_mo(ls)
    bang(rc == mod.RC_KHONG_XAC_DINH and "KHÔNG_XÁC_ĐỊNH" in out
         and "CU" in out and "MOI" in out and "NGƯỜI_GIỮ" not in out,
         f"lease mới không trỏ ngược vẫn hợp thức hoá bia mộ: rc={rc} {out}")


@ca
def t119_bia_mo_hai_chieu_day_du_van_go_lease_cu():
    ls = [("refs/remotes/origin/a", "ops/leases/cu.yaml",
           _lease_quet("CU", da_bi_thay_the="MOI")),
          ("refs/remotes/origin/a", "ops/leases/moi.yaml",
           _lease_quet("MOI", thay_the_cho="CU"))]
    rc, out, mod = _quet_ca_bia_mo(ls)
    bang(rc == mod.RC_DANG_GIU and "CÒN_HẠN · ĐÃ_BỊ_THAY_THẾ\tCU" in out
         and "NGƯỜI_GIỮ 1: MOI" in out,
         f"bia mộ hai chiều không giữ hành vi gỡ: rc={rc} {out}")


@ca
def t120_thay_the_cho_danh_sach_hai_lease_deu_co_bia_mo_phai_QUA():
    mod = _nap_cong()
    moi = lease_mau(lease_id="MOI", thay_the_cho=["CU1", "CU2"])
    ls = [
        ("refs/remotes/origin/a", "ops/leases/cu1.yaml",
         _lease_quet("CU1", da_bi_thay_the="MOI")),
        ("refs/remotes/origin/a", "ops/leases/cu2.yaml",
         _lease_quet("CU2", da_bi_thay_the="MOI")),
    ]
    with San() as s:
        (s / ".git").mkdir()
        p = viet(s, moi)
        mod.GOI_GIT = _GitKhoGia({"a"}, {"a"}, ls)
        try:
            _kiem_sach(mod, moi, p, s)
        except mod.Chan as ex:
            raise AssertionError(
                f"danh sách hai bia mộ đầy đủ bị chặn: {ex.ma} {ex.thong_diep}") from ex
    rc, out, mod = _quet_ca_bia_mo(ls + [
        ("refs/remotes/origin/a", "ops/leases/moi.yaml",
         _lease_quet("MOI", thay_the_cho=["CU1", "CU2"]))])
    bang(rc == mod.RC_DANG_GIU and out.count("ĐÃ_BỊ_THAY_THẾ") == 2
         and "NGƯỜI_GIỮ 1: MOI" in out,
         f"phép quét không đọc danh sách hai bia mộ: rc={rc} {out}")


@ca
def t121_thay_the_cho_danh_sach_thieu_mot_bia_mo_phai_CHAN():
    mod = _nap_cong()
    moi = lease_mau(lease_id="MOI", thay_the_cho=["CU1", "CU2"])
    with San() as s:
        (s / ".git").mkdir()
        p = viet(s, moi)
        mod.GOI_GIT = _GitKhoGia({"a"}, {"a"}, [
            ("refs/remotes/origin/a", "ops/leases/cu1.yaml",
             _lease_quet("CU1", da_bi_thay_the="MOI")),
            ("refs/remotes/origin/a", "ops/leases/cu2.yaml",
             _lease_quet("CU2", da_bi_thay_the="KHAC")),
        ])
        try:
            _kiem_sach(mod, moi, p, s)
        except mod.Chan as ex:
            bang(ex.ma == RC_NOI_DUNG and "CU2" in ex.thong_diep,
                 f"danh sách thiếu bia mộ chặn sai: {ex.ma} {ex.thong_diep}")
        else:
            raise AssertionError("danh sách thiếu bia mộ CU2 vẫn đăng được")


@ca
def t122_hai_lease_tro_vong_cho_ket_qua_xac_dinh_khong_de_quy():
    ls = [("refs/remotes/origin/a", "ops/leases/a.yaml",
           _lease_quet("A", da_bi_thay_the="B", thay_the_cho="B")),
          ("refs/remotes/origin/a", "ops/leases/b.yaml",
           _lease_quet("B", da_bi_thay_the="A", thay_the_cho="A"))]
    rc, out, mod = _quet_ca_bia_mo(ls)
    bang(rc == mod.RC_OK and out.count("ĐÃ_BỊ_THAY_THẾ") == 2
         and "NGƯỜI_GIỮ 0: không có" in out,
         f"vòng A-B không cho kết quả xác định: rc={rc} {out}")


@ca
def t123_bia_mo_hong_het_han_va_khong_cham_duong_khong_duoc_lan_toa():
    ls = [("refs/remotes/origin/a", "ops/leases/het-han.yaml",
           _lease_quet("HET-HAN", han="2000-01-01T00:00:00Z",
                       da_bi_thay_the="KHONG-CO-1")),
          ("refs/remotes/origin/a", "ops/leases/khong-cham.yaml",
           _lease_quet("KHONG-CHAM", path="x.py", da_bi_thay_the="KHONG-CO-2")),
          ("refs/remotes/origin/a", "ops/leases/giu.yaml", _lease_quet("GIU"))]
    rc, out, mod = _quet_ca_bia_mo(ls)
    bang(rc == mod.RC_DANG_GIU and "HẾT_HẠN\tHET-HAN" in out
         and "KHONG-CHAM" not in out and "NGƯỜI_GIỮ 1: GIU" in out,
         f"bia mộ ngoài phạm vi làm hỏng câu trả lời: rc={rc} {out}")


@ca
def t124_bay_dot_bien_bia_mo_giet_dung_va_chi_dung_tap_dich():
    global SCRIPT
    nguon, ban_goc = SCRIPT.read_text(encoding="utf-8"), SCRIPT
    dich = {
        "t117": t117_bia_mo_tro_lease_khong_ton_tai_phai_KHONG_XAC_DINH,
        "t118": t118_bia_mo_co_lease_moi_nhung_khong_tro_nguoc_phai_CHAN,
        "t119": t119_bia_mo_hai_chieu_day_du_van_go_lease_cu,
        "t120": t120_thay_the_cho_danh_sach_hai_lease_deu_co_bia_mo_phai_QUA,
        "t121": t121_thay_the_cho_danh_sach_thieu_mot_bia_mo_phai_CHAN,
        "t122": t122_hai_lease_tro_vong_cho_ket_qua_xac_dinh_khong_de_quy,
        "t123": t123_bia_mo_hong_het_han_va_khong_cham_duong_khong_duoc_lan_toa,
    }
    muts = [
        ("noi-vi-tu-thanh-if-False", "if bia_mo is False:", "if False:",
         {"t117", "t118"}),
        ("so-bang-thanh-do-chuoi",
         "if thay_the_cho is not None and lease_cu in thay_the_cho:",
         "if thay_the_cho is not None and any(lease_cu in ten for ten in thay_the_cho):",
         {"t118"}),
        ("bo-schema-danh-sach", "if isinstance(gia_tri, list):", "if False:",
         {"t120", "t121"}),
        ("chi-kiem-phan-tu-dau",
         "chua_danh_dau = [ten for ten in thay_the_cho if not any(",
         "chua_danh_dau = [ten for ten in thay_the_cho[:1] if not any(", {"t121"}),
        ("bo-hanh-vi-go", "da_chet = bia_mo is True", "da_chet = False",
         {"t119", "t120", "t122"}),
        ("fail-toan-ca-het-han",
         'if trang_thai == "CÒN_HẠN" else None)', "if True else None)", {"t123"}),
        ("fail-toan-ca-khong-cham",
         "if not _lease_cham_duong(lease, a.duong_dan):\n            continue",
         "if False:\n            continue", {"t123"}),
    ]
    sys.dont_write_bytecode = True
    try:
        for i, (ten, cu, moi, do_dung) in enumerate(muts):
            bang(nguon.count(cu) == 1, f"neo mutant {ten} không duy nhất")
            with San() as s:
                p = s / f"mut_bia_mo_{i}.py"
                p.write_text(nguon.replace(cu, moi), encoding="utf-8")
                import importlib
                importlib.invalidate_caches()
                SCRIPT, do = p, set()
                for ten_ca, fn in dich.items():
                    try:
                        fn()
                    except Exception:  # mutant có thể đổi cả kiểu lỗi; vẫn là ca bị giết
                        do.add(ten_ca)
                song = set(dich) - do
                print(f"đột biến bia mộ {ten}: ĐỎ={sorted(do)}, SỐNG={sorted(song)}")
                bang(do == do_dung and song == set(dich) - do_dung,
                     f"mutant {ten}: ĐỎ={do}, cần={do_dung}; SỐNG={song}")
    finally:
        SCRIPT = ban_goc


@ca
def t126_dau_da_dang_la_HIEN_VAT_SUA_DUOC_chu_khong_phai_ban_ghi_git():
    """GHIM hồi quy ĐỘ BỀN mà packet #396 tạo ra — có chủ ý, và phải đo được.

    Trước #396 dấu "đã đăng" là `posted_comment_id` NẰM TRONG GIT: sửa hay xoá comment
    trên Issue không làm nó mất. Sau #396 dấu duy nhất là chính comment ấy.

    Vị từ đúng — ca này ghim nó, chứ không ghim một danh sách thao tác: dấu của lease `L`
    tồn tại KHI VÀ CHỈ KHI Issue hiện có ÍT NHẤT MỘT comment mà
    `user.login == "github-actions[bot]"` VÀ body BẮT ĐẦU đúng bằng ``**Lease `L`**``.

    Lượng từ "ít nhất một" là chỗ dễ trượt nhất, nên ba ca ÂM dưới đây đều dựng danh sách
    KHÔNG CÒN bản khớp nào: rỗng hẳn; còn một bản của bot nhưng prefix đã bị phá; còn một
    bản đúng prefix nhưng của danh tính khác. Chúng KHÔNG khẳng định "xoá một comment là
    mất dấu" — còn một bản khớp khác thì dấu vẫn còn.

    Ca DƯƠNG dùng body có nội dung SAU prefix và vẫn chặn, tức sửa phần sau prefix không
    làm mất dấu.

    Ca này KHÔNG khẳng định hành vi ấy là tốt. Nó khẳng định hành vi ấy là ĐÃ BIẾT.
    Cross-review codex 29-08-2026 (finding 3) chỉ ra rằng `danh_doi` của đặc tả mới chỉ
    khai "mất mạng thì không đăng được" — tức khai thiếu đúng vế này.

    ĐỘT BIẾN LÀM CA NÀY ĐỎ: đổi `startswith` thành `in`, hoặc bỏ chốt `user.login`.
    """
    lease = lease_mau(lease_id="lease-sua-duoc")

    def do(nhan, comments):
        ex, _ = _goi_lop_gh(GhGia(comments=comments), "_kiem_comment_da_co",
                            "o/r", lease, env_them=ENV_GITHUB)
        return ex

    dau = "**Lease `lease-sua-duoc`**"
    bot = {"login": "github-actions[bot]"}

    ex = do("nguyên vẹn", {55: [{"id": 7, "body": dau + " — bản chiếu", "user": bot}]})
    bang(ex is not None and ex.ma == RC_DA_DANG,
         f"comment nguyên vẹn mà KHÔNG thấy dấu — chống lặp đã hỏng hẳn: {ex}")

    # Ba cách MẤT dấu. Cả ba đều là thao tác quản trị Issue hợp lệ, không ai phá hoại.
    for nhan, comments in (
            ("xoá comment", {55: []}),
            ("thêm một ký tự vào ĐẦU body", {55: [{"id": 7, "body": "." + dau, "user": bot}]}),
            ("bản của bot bị THAY bằng bản của người thật",
             {55: [{"id": 7, "body": dau, "user": {"login": "ducthangho"}}]})):
        ex = do(nhan, comments)
        bang(ex is None,
             f"{nhan}: ca này ghim hành vi FAIL-OPEN đã biết, nhưng cổng lại CHẶN ({ex}) "
             f"— nếu ai đó vừa vá cho bền hơn thì đấy là tin TỐT: hãy sửa ca này và khai "
             f"lại mục `danh_doi`, đừng nới lời khẳng định cho vừa.")


LECH_KHOP, LECH_CHUA_RO = "KHỚP", "LỆCH_CHƯA_RÕ_NGUYÊN_NHÂN"


def _phan_loai_lech_ab(ket_a, ket_b):
    """So kết quả quan sát được; A/B lệch chưa xác định được nguyên nhân.

    CI e6feddb có t139 đỏ vì S8-bo-deadline sống ở vế B. Log đó xác định ca/mutant,
    không chứng minh hay loại trừ quan hệ nhân quả với actor. Một lần đo lại khớp,
    kể cả tuần tự, cũng không loại trừ rò actor phụ thuộc thứ tự ca hoặc tải.
    Đo lại một ca riêng còn thay đổi ngữ cảnh của phép đo TOÀN SUITE.

    Vì vậy giữ nguyên bằng chứng A/B và trả trạng thái chưa rõ nguyên nhân cho
    MỌI lệch, gồm cả rc/số đếm/tập đỏ/tập bỏ qua. t125 phải ĐỎ ngay, không chạy thêm
    chẩn đoán thiếu ngân sách tổng, thu hồi cây hoặc tee rồi gọi nó là chập chờn.
    """
    if ket_a == ket_b:
        return LECH_KHOP, "hai vế khớp"
    lech_do = sorted(set(ket_a[3]) ^ set(ket_b[3]))
    lech_bo = sorted(set(ket_a[4]) ^ set(ket_b[4]))
    return (LECH_CHUA_RO,
            f"{LECH_CHUA_RO}: hai lượt TOÀN SUITE A/B khác nhau; "
            f"không-actor=(rc={ket_a[0]}, {ket_a[1]}/{ket_a[2]}), "
            f"có-actor=(rc={ket_b[0]}, {ket_b[1]}/{ket_b[2]}); "
            f"ca lệch ĐỎ={lech_do!r} BỎ QUA={lech_bo!r}. "
            "CHƯA loại trừ rò GITHUB_ACTOR, ảnh hưởng thứ tự ca hoặc tải; "
            "không kết luận nguyên nhân từ riêng hai kết quả. "
            "Đọc lý do từng ca trong log [A]/[B]; mọi lệch đều chặn cổng.")


def _mo_con_nhom_rieng(lenh, env, stdout, stderr):
    """`Popen` cho con làm LÃNH ĐẠO một nhóm tiến trình RIÊNG, để `_giet_ca_cay` với tới được CHÁU.

    Vì sao không `Popen` trần: `p.kill()` giết ĐÚNG PID con. Cross-review codex 11-09-2026 (P1) đo
    được cháu sống tiếp; probe Linux tại chỗ xác nhận (con rc=-9, cháu `sleep` vẫn chạy). Cháu ở đây
    là git/actionlint/shellcheck — trên Windows chúng giữ handle tệp và ăn CPU sau khi con đã chết.

    API RIÊNG NỀN, tra bằng `getattr` chứ không đụng thẳng (CLAUDE.md: "API CHỈ CÓ TRÊN MỘT NỀN" —
    `os.getpgid` từng làm suite Windows 0/103): `start_new_session` chỉ có nghĩa trên POSIX,
    `CREATE_NEW_PROCESS_GROUP` chỉ có trên Windows. Cờ vắng ⇒ vẫn chạy, và `_giet_ca_cay` sẽ KHAI
    rằng nó không có nhóm riêng thay vì im lặng giết nhầm.
    """
    them = {}
    if os.name == "posix":
        them["start_new_session"] = True
    else:
        co = getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0)
        if co:
            them["creationflags"] = co
    return subprocess.Popen(lenh, env=env, stdout=stdout, stderr=stderr, text=True, **them)


def _nap_launcher_thu_hoi():
    """Dùng lại cơ chế chụp cây/khoá PID của launcher đã có trong cùng checkout."""
    import importlib.util
    duong = HERE.parent / ".claude" / "dev" / "launcher.py"
    spec = importlib.util.spec_from_file_location("launcher_thu_hoi_lease_test", duong)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _giet_ca_cay(p, cho_giay: float = 5.0) -> str:
    """Giết con VÀ CHÁU. Trả một dòng ĐO ĐƯỢC về đường đã đi — kể cả đường KHÔNG làm được gì.

    Bốn chốt, mỗi chốt là một bài học đã trả giá:
    · KHÔNG BAO GIỜ giết nhóm của CHÍNH MÌNH. Chỉ `killpg` khi nhóm của con ĐÚNG BẰNG PID con VÀ
      KHÁC nhóm của tiến trình này; `start_new_session` hỏng âm thầm thì lùi về `p.kill()` chứ không
      giết cả runner ("test không được nhét PID của chính nó vào thứ mình đang thử giết").
    · `taskkill /T /F` KHÔNG đáng tin — trả `Access denied` ngay trên con do chính mình sinh. Gọi
      xong phải KIỂM LẠI, còn sống thì `p.kill()`.
    · POSIX dùng lại launcher để chụp hậu duệ, giữ khoá danh tính và kiểm cả nhóm;
      ZOMBIE tính là ĐÃ CHẾT. `wait()` bên dưới thu hồi PID con trực tiếp.
    · "Đã gọi lệnh giết" ≠ "đã chết" — nên hàm này trả nhật ký từng bước, và ca gọi nó phải ĐO hành
      vi của cháu (nhịp tim), đừng đọc mã thoát của lệnh giết.
    """
    buoc = []
    killpg, getpgid = getattr(os, "killpg", None), getattr(os, "getpgid", None)
    if killpg and getpgid:
        nhom_con = nhom_minh = None
        try:
            nhom_con, nhom_minh = getpgid(p.pid), getpgid(0)
        except OSError as ex:
            buoc.append(f"getpgid loi {type(ex).__name__}")
        if nhom_con is not None and nhom_con == p.pid and nhom_con != nhom_minh:
            # Mẹ chết bởi TERM chưa chứng minh cháu chết. Chụp cây TRƯỚC tín hiệu
            # để giữ cả cháu đã mở session riêng (t154/t156/t157 cũng tạo nhóm lồng).
            thu_hoi = _nap_launcher_thu_hoi()
            kq = thu_hoi._giet_cay(p.pid, thu_hoi._khoa_danh_tinh(p.pid))
            buoc.append(f"ca_cay={kq.ca_cay}: {kq}")
        else:
            buoc.append(f"KHONG co nhom rieng (nhom_con={nhom_con} pid={p.pid} nhom_minh={nhom_minh}) "
                        f"- chi giet PID, CHAU KHONG DO DUOC")
    else:
        import shutil
        tk = shutil.which("taskkill")
        if tk:
            try:
                r = subprocess.run([tk, "/T", "/F", "/PID", str(p.pid)],
                                   capture_output=True, text=True, timeout=cho_giay)
                buoc.append(f"taskkill rc={r.returncode} err={(r.stderr or '').strip()[:80]!r}")
            except (OSError, subprocess.TimeoutExpired) as ex:
                buoc.append(f"taskkill loi {type(ex).__name__}")
            try:
                p.wait(timeout=max(0.1, cho_giay / 2))
            except subprocess.TimeoutExpired:
                pass
        else:
            buoc.append("KHONG co taskkill")
    if p.poll() is None:
        p.kill()
        buoc.append("p.kill()")
    try:
        p.wait(timeout=cho_giay)
    except subprocess.TimeoutExpired:
        buoc.append("wait QUA HAN - con CON SONG")
    buoc.append(f"rc={p.returncode}")
    return " -> ".join(buoc)


def _moi_truong_con_ab(nen: dict) -> dict:
    """Môi trường cho MỘT lượt con của t125: nền đã lọc + TẮT ĐỆM Python.

    VÌ SAO `PYTHONUNBUFFERED` PHẢI ĐẶT Ở ĐÂY, không phó cho wrapper. Đo 12-09-2026: con in một dòng
    rồi `sleep 6` mà KHÔNG flush ⇒ tee thấy dòng trong 3 s: **không** biến ⇒ KHÔNG · có biến ⇒ CÓ.
    Trên CI thì `ops/chay_lease_publish_test.sh` (M2) đã `export PYTHONUNBUFFERED=1`, nên đường CI vốn
    sống; nhưng giá trị của một bản vá không được phụ thuộc một biến do TỆP KHÁC đặt — chạy trực tiếp
    `python3 ops/lease_publish_test.py` thì bằng chứng lại nằm trong đệm của con tới lúc con thoát,
    đúng chỗ mù mà lớp `bang-chung-song-bi-chon-trong-tep-tam` sinh ra để xoá. `t157` đo CƠ CHẾ bằng
    một writer tự flush nên nó xanh ở CẢ HAI đường ⇒ `t157` KHÔNG canh được chỗ này; `t158` canh.

    Đặt cho CẢ HAI vế A/B nên bất biến của t125 không đổi: hai vế vẫn khác nhau ĐÚNG một biến
    `GITHUB_ACTOR`.
    """
    return dict(nen, PYTHONUNBUFFERED="1")


def _theo_duoi_va_in(duong, tien_to: str, dung, khoa) -> None:
    """Tail tệp log con đang ghi, in từng DÒNG ĐỦ ra stdout CHA kèm tiền tố. Line-atomic qua `khoa`.

    Vì sao: job bị huỷ giữa t125 (trần 60 phút của `ci.yml`, hay huỷ từ ngoài) thì tệp tạm đi theo
    container và log CI chỉ còn một dòng `>>> vao t125` — đúng chỗ mù packet này sinh ra để xoá
    (cross-review codex 11-09-2026, P2). Tee đưa bằng chứng lên log CI NGAY, bản riêng trong tệp vẫn
    còn nguyên byte cho phép so ba tập của A/B.

    TIỀN TỐ ở ĐẦU DÒNG là thứ giữ cho tee không lừa được ai: mọi regex của bộ test neo `(?m)^` (
    `^>>> vao`, `^<<< ra`, `^  ĐỎ  `, `^  BỎ QUA `) nên không dòng teed nào khớp. Regex duy nhất
    KHÔNG neo đầu dòng là `lease_publish: (\d+)/(\d+) đạt`, và nó đọc BẢN RIÊNG trong tệp chứ
    không đọc stdout — đã kiểm: ngoài tệp này không script nào trong kho grep dòng tổng kết đó.

    Đọc NHỊ PHÂN rồi mới giải mã từng dòng: đọc text theo khối cắt ngang một ký tự nhiều byte sẽ
    sinh ký tự thay thế giả.
    """
    du = b""
    with open(duong, "rb") as f:
        while True:
            xong = dung.is_set()          # đọc cờ TRƯỚC khi đọc tệp: con đã được `wait` rồi mới set
            moi = f.read(65536)
            if moi:
                du += moi
                *dong, du = du.split(b"\n")
                for d in dong:
                    with khoa:
                        print(f"{tien_to} {d.decode('utf-8', 'replace').rstrip(chr(13))}", flush=True)
                continue
            if xong:
                if du:
                    with khoa:
                        print(f"{tien_to} {du.decode('utf-8', 'replace').rstrip(chr(13))}", flush=True)
                return
            time.sleep(0.05)


@ca
def t125_AB_toan_suite_KHONG_doi_verdict_theo_ambient_actor():
    """A/B: chạy lại TOÀN SUITE hai lượt, khác nhau ĐÚNG một biến `GITHUB_ACTOR`.

    VÌ SAO CẦN CA NÀY, và vì sao nó không thể là một khẳng định rẻ hơn. Bộ test này
    dựng môi trường con ở NHIỀU chỗ — `_goi_lop_gh`, và một tá ca tự `subprocess.run`
    với `dict(os.environ, …)`. Một ca chỉ soi `_goi_lop_gh` sẽ kiểm CÁCH SỬA hôm nay,
    không kiểm TÍNH CHẤT cần giữ; helper rò thứ hai thêm vào tháng sau sẽ lọt.

    Đo được, 29-08-2026 trên `ef4098d4` (trước khi vá): `env -u GITHUB_ACTOR` ⇒ 123/124,
    `GITHUB_ACTOR=notebyme88` ⇒ 94/124. Chênh 29 ca, và `t124` còn báo sai TẬP ĐÍCH của
    bẫy đột biến — tức rò actor không chỉ làm đỏ, nó làm hỏng chính bẫy.

    So bằng TẬP TÊN ca đỏ chứ không bằng con số: hai lượt cùng ra `n/m` mà đỏ ở những ca
    KHÁC nhau thì phép so bằng số vẫn xanh — đúng hình dạng "bất biến còn đúng, số hạng
    đã trôi" mà `soan-spec` §L5 cảnh báo.

    Chống đệ quy đi bằng ĐỐI SỐ DÒNG LỆNH, không bằng biến môi trường. Bản đầu dùng
    `LP_AB_CON=1` và cross-review codex 29-08-2026 (finding 1) chỉ ra ngay: biến môi
    trường được KẾ THỪA, nên chỉ cần `LP_AB_CON=1` có sẵn trong môi trường là ca này
    lặng lẽ `return` và vẫn được tính ĐẠT — đo được: `LP_AB_CON=1 python <tệp này>` cho
    `120/120` và chạy nhanh, tức A/B không hề chạy. `sys.argv` không kế thừa, nên không
    có cấu hình môi trường nào vô hiệu hoá được ca này.

    ĐỘT BIẾN LÀM CA NÀY ĐỎ: bỏ dòng `moi.pop("GITHUB_ACTOR", None)` trong `_goi_lop_gh`,
    hoặc bỏ lọc `env` trong `chay()`, hoặc bỏ `patch.dict` trong `_kiem_sach`.

    HAI LƯỢT CON CHẠY SONG SONG, CÓ HẠN (packet #504 M5): M4 lượt 1 thấy t125 vào nhưng không ra
    trong 1540 s; log ấy chưa phân biệt được con treo với con chậm. Giữ toàn suite và cùng tuple A/B.
    `AB_HAN_GIAY` là trần mỗi con TỪ LÚC START; hai waiter chạy đồng thời, quá hạn thì ĐỎ và thu hồi
    CẢ CÂY (không chỉ PID con). 5 s chỉ dành cho wait sau kill. M4 lượt 4 ghi t125=344.438 s, không
    chứng minh trần đủ sau khi sửa các ca PATH ngoài write set; phải đo Windows lại, không tự nâng
    trần cho xanh — nên trần nay DẪN XUẤT từ các hạn trong (xem `_han_ngoai_toi_thieu`) và bị `t156`
    chặn ở cả hai đầu: không nhỏ hơn tổng hạn trong, không vượt `AB_TRAN_CUNG_GIAY`.

    BA BẢN VÁ CROSS-REVIEW 11-09-2026 nằm ở ca này, mỗi bản một LỚP, và mỗi lớp có phản chứng riêng:
    · P1 `_giet_ca_cay` thay `p.kill()` — cháu (git/shellcheck) sống sót cú giết PID; phản chứng `t154`
      đo NHỊP TIM của cháu hai chiều (giết PID ⇒ cháu còn đập; giết cây ⇒ cháu im).
    · P2 tee `_theo_duoi_va_in` — stdout/stderr con vào tệp CÓ TÊN và được tail ra log CI ngay, nên
      job bị huỷ giữa t125 vẫn để lại tên ca đang chạy của con. Bản riêng trong tệp vẫn nguyên byte.
    · P2 hạn ngoài dẫn xuất — xem đoạn trên và `t156`.

    Phạm vi số M4: Windows lượt 4 hoàn tất 526.866 s với 15 ĐỎ, 7 BỎ QUA. Chỉ 14 ca có chữ ký PATH;
    t150 chỉ giữ 200 ký tự cuối stderr, chưa xác định gốc. Ubuntu lượt 4=114.528 s, A2 lượt 1=141.023 s.
    Lượt 3: t139 vào 17:24:51.969Z, log huỷ 17:25:47.047Z, khoảng 55.077 s; không phải 90 s.
    Numstat cộng dồn theo base: f1b0b4f +102/-15, 570209c +142/-16, dff28f6 +157/-17;
    +166/-26 là tổng delta cộng cơ học, không phải diff của dff28f6 so base.
    """
    import re
    import subprocess
    if CO_AB in sys.argv:
        return          # lượt con: KHÔNG tự gọi lại mình (chống đệ quy)

    import threading
    from concurrent.futures import ThreadPoolExecutor, as_completed
    nen = {k: v for k, v in os.environ.items() if k != "GITHUB_ACTOR"}

    def doc(x):
        nhan, ma, p, out_p, err_p, dung, luong, han = x
        qua_han, nhat_ky_giet = False, ""
        try:
            p.wait(timeout=max(0.0, han - time.monotonic()))
        except subprocess.TimeoutExpired:
            qua_han = True
            nhat_ky_giet = _giet_ca_cay(p)   # CẢ CÂY: cháu git/shellcheck không được sống sót
        dung.set()
        for t in luong:
            t.join(timeout=5)
        out = out_p.read_text(encoding="utf-8", errors="replace")
        err = err_p.read_text(encoding="utf-8", errors="replace")
        if qua_han:
            vao = re.findall(r"(?m)^>>> vao (\S+) ", out)
            ra = set(re.findall(r"(?m)^<<< ra (\S+) ", out))
            treo = [x for x in vao if x not in ra]
            bang(False, f"lượt {nhan}: lượt con KHÔNG XONG trong {AB_HAN_GIAY}s — kết quả thu hồi "
                        f"({nhat_ky_giet}); ca treo (vao không ra): {treo!r}; đã xong {len(ra)} ca; "
                        f"stdout cuối={out[-300:]!r}; stderr cuối={err[-300:]!r}")
        m = re.search(r"lease_publish: (\d+)/(\d+) đạt", out)
        bang(m, f"lượt {nhan}: KHÔNG ĐO ĐƯỢC dòng tổng kết; rc={p.returncode}, "
                f"stdout={out[-400:]!r}, stderr={err[-400:]!r}")
        do = frozenset(re.findall(r"(?m)^  ĐỎ  (\w+):", out))
        # Giữ cả tập BỎ QUA: cùng số lượng chưa chứng minh cùng tập ca đã đo.
        bo = frozenset(re.findall(r"(?m)^  BỎ QUA (\w+):", out))
        return p.returncode, m.group(1), m.group(2), do, bo

    # Tệp CÓ TÊN cho từng luồng: không đầy PIPE, không chờ EOF do cháu giữ handle (M3), và có đường
    # cho `_theo_duoi_va_in` tail ra log CI. Hai waiter chạy đồng thời; hạn tính từ lúc START của
    # CHÍNH con ấy, không cấp lại khi đọc lượt B.
    khoa = threading.Lock()
    with tempfile.TemporaryDirectory() as td, ThreadPoolExecutor(max_workers=2) as pool:
        con, ket_qua, tay = [], {}, []
        try:
            for nhan, ma, mt in (("KHÔNG actor", "A", nen),
                                 ("CÓ actor lạ", "B", dict(nen, GITHUB_ACTOR="ke-la-mat-khong-co-quyen"))):
                out_p, err_p = Path(td) / f"{ma}.out", Path(td) / f"{ma}.err"
                ow = open(out_p, "w", encoding="utf-8"); tay.append(ow)
                ew = open(err_p, "w", encoding="utf-8"); tay.append(ew)
                han = time.monotonic() + AB_HAN_GIAY
                p = _mo_con_nhom_rieng([sys.executable, str(Path(__file__).resolve()), CO_AB],
                                       _moi_truong_con_ab(mt), ow, ew)
                dung = threading.Event()
                luong = [threading.Thread(target=_theo_duoi_va_in, args=(out_p, f"[{ma}]", dung, khoa), daemon=True),
                         threading.Thread(target=_theo_duoi_va_in, args=(err_p, f"[{ma} err]", dung, khoa), daemon=True)]
                for t in luong:
                    t.start()
                con.append((nhan, ma, p, out_p, err_p, dung, luong, han))
            viec = {pool.submit(doc, x): x[0] for x in con}
            for f in as_completed(viec):
                ket_qua[viec[f]] = f.result()
        finally:
            for x in con:
                if x[2].poll() is None:
                    _giet_ca_cay(x[2])
                x[5].set()
                for t in x[6]:
                    t.join(timeout=5)
            for h in tay:            # đóng TRƯỚC khi TemporaryDirectory dọn: Windows không xoá được
                try:                 # thư mục còn handle mở
                    h.close()
                except OSError:
                    pass
    khong_actor, co_actor = ket_qua["KHÔNG actor"], ket_qua["CÓ actor lạ"]

    ket_luan, thong_diep = _phan_loai_lech_ab(khong_actor, co_actor)
    bang(ket_luan == LECH_KHOP, thong_diep)



# =====================================================================================
# A0 — SỔ THU HỒI LEASE, chế độ CHƯA KÍCH HOẠT (packet wp488, spec r9 §nghiem_thu A2/A3/A6/A7/A8/A11/A12).
# Mọi ca dưới đây khẳng định bằng `chot()` — ném `TinHieuChotCa`, một LỚP RIÊNG mà mã sản phẩm không giả
# được (CLAUDE.md: "đột biến bị giết không phải đột biến bị giết ĐÚNG LÝ DO"). Catalog mutant t139 chỉ nhận
# công khi ca đích chết bằng đúng lớp ấy; mọi ngoại lệ khác là TÍN DỤNG GIẢ và làm catalog ĐỎ.
# =====================================================================================
RC_KHONG_XAC_DINH_A0, RC_DANG_GIU_A0 = 12, 11
KHO_CANONICAL_A0 = "github.com/ducthangho/tra-luat"
WORKFLOW_THU_HOI = HERE.parent / ".github" / "workflows" / "ops-thu-hoi-admission.yml"


class TinHieuChotCa(AssertionError):
    """Tín hiệu của CHÍNH ca A0 — không `except` nào trong mã sản phẩm hay fixture dựng được nó."""


class TinHieuCuaDem(TinHieuChotCa):
    """Tín hiệu RIÊNG của cửa `_goi_dem_lop_gh`, mang NHÃN VẾ đã đỏ (`ket_qua` · `dem`).

    Cross-review codex lượt 2 (24-09, `assertion-message-substitutes-signal-identity`, P2):
    `t185` bắt `AssertionError` chung rồi tìm CHUỖI trong thông điệp để khai "vế nào đã đỏ".
    Reviewer thay hai lời gọi cửa bằng `AssertionError` TRẦN chép lại đúng thông điệp ⇒ `t185`
    vẫn QUA — ca tự nhận đã xác nhận hai chốt trong khi cả hai chốt CHƯA CHẠY. Danh tính của
    tín hiệu phải là thứ mã khác KHÔNG giả được bằng cách chép chữ: một LỚP riêng và một nhãn
    VẾ, không phải một chuỗi con.
    """

    def __init__(self, ve: str, msg: str):
        super().__init__(msg)
        self.ve = ve


def _chot_cua_dem(ve: str, dk, msg):
    if not dk:
        raise TinHieuCuaDem(ve, msg)


def chot(dk, msg):
    if not dk:
        raise TinHieuChotCa(msg)


def _ma_chan(mod, fn, *a, **k):
    """Gọi một hàm sản phẩm, trả ``(rc, kết quả|thông điệp)``: rc=0 khi không ném, rc=e.ma khi ném `Chan`."""
    try:
        return 0, fn(*a, **k)
    except mod.Chan as e:
        return e.ma, e.thong_diep


def _goi_main(mod, *argv, env=None):
    """Chạy `main()` TRONG TIẾN TRÌNH (để mutant trên bản sao đo được), stdout/stderr bắt về chuỗi."""
    import contextlib
    import io
    from unittest import mock
    out, err = io.StringIO(), io.StringIO()
    moi = dict({k: v for k, v in os.environ.items() if k != "GITHUB_ACTOR"}, **(env or {}))
    with mock.patch.dict(os.environ, moi, clear=True), \
            contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        rc = mod.main([str(x) for x in argv])
    return rc, out.getvalue(), err.getvalue()


def _g_a0(cay, *a, env=None):
    return subprocess.run(["git", "-c", "user.email=a@b", "-c", "user.name=c", "-c", "commit.gpgsign=false",
                           "-C", str(cay), *a], capture_output=True, text=True, check=True, env=env).stdout.strip()


def _kho_do_thi(tmp: Path):
    """Kho làm việc có 3 commit thẳng hàng c0 ← c1 ← c2 (c2 = HEAD, nhánh master), không sổ thu hồi.
    Trả ``(cay, [c0, c1, c2])``. `c2` đóng vai S trong các ca M4; H dựng thêm trên từng nhánh."""
    cay = tmp / "kho"
    cay.mkdir()
    _g_a0(cay, "init", "-q", "-b", "master")
    (cay / "README.md").write_bytes("nen\n".encode("utf-8"))
    _g_a0(cay, "add", "-A"); _g_a0(cay, "commit", "-qm", "c0")
    (cay / "docs").mkdir(); (cay / "docs" / "a.md").write_bytes("a\n".encode("utf-8"))
    _g_a0(cay, "add", "-A"); _g_a0(cay, "commit", "-qm", "c1")
    (cay / "ops" / "leases").mkdir(parents=True)
    (cay / "ops" / "leases" / "x.yaml").write_bytes("lease_id: x\n".encode("utf-8"))
    (cay / "ops" / "lease_publish.py").write_bytes("# bộ kiểm giả tại S\n".encode("utf-8"))
    _g_a0(cay, "add", "-A"); _g_a0(cay, "commit", "-qm", "c2")
    shas = _g_a0(cay, "rev-list", "--reverse", "HEAD").split()
    return cay, shas


def _ban_ghi_thu_hoi(**doi) -> dict:
    d = {"schema_version": 1, "event": "lease_revoked", "lease_id": "wp1-exec-1-codex-20260901",
         "packet_issue": 488, "thu_hoi_boi": "ducthangho", "thu_hoi_luc_utc": khi_truoc(1),
         "ly_do": "packet đã land, quyền ghi không còn lý do tồn tại",
         "can_cu": f"https://{KHO_CANONICAL_A0}/issues/488#issuecomment-5604451242"}
    d.update(doi)
    return {k: v for k, v in d.items() if v is not _BO}


_BO = object()   # đánh dấu "xoá khoá" cho fixture


def _metadata_retired(**doi) -> dict:
    d = {"schema_version": 1, "event": "closure_exception_retired", "descriptor_sha256": "a" * 64,
         "first_policy_sha256": "b" * 64, "base_sha_before_add": SHA40, "retired_at_utc": khi_truoc(1)}
    d.update(doi)
    return {k: v for k, v in d.items() if v is not _BO}


def _yaml_bytes(d: dict) -> bytes:
    import yaml
    return yaml.safe_dump(d, allow_unicode=True, sort_keys=False).encode("utf-8")


def _them_commit(cay: Path, nhanh: str, tu: str, tep: dict, *, symlink=None, xoa=()) -> str:
    """Tạo nhánh `nhanh` từ `tu`, ghi các tệp (bytes) / symlink / xoá, commit; trả SHA."""
    _g_a0(cay, "reset", "-q", "--hard")          # cây làm việc sạch trước khi rẽ (mode đổi qua update-index…)
    _g_a0(cay, "checkout", "-q", "-B", nhanh, tu)
    for duong, noi_dung in tep.items():
        p = cay / duong; p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(noi_dung)
    if symlink:
        p = cay / symlink[0]; p.parent.mkdir(parents=True, exist_ok=True); p.symlink_to(symlink[1])
    for duong in xoa:
        (cay / duong).unlink()
    _g_a0(cay, "add", "-A"); _g_a0(cay, "commit", "-qm", nhanh)
    return _g_a0(cay, "rev-parse", "HEAD")


@ca
def t127_A7_M1_ma_tran_ban_ghi_thu_hoi_thu_tu_loi_12_4_8():
    """M1 (r3): parser bản ghi `lease_revoked` — ma trận A7 + THỨ TỰ lỗi nguồn(12) → thẩm quyền(4) → nội dung(8)."""
    mod = _nap_cong()
    duong = "ops/thu-hoi/wp1-exec-1-codex-20260901.yaml"
    ok = _ban_ghi_thu_hoi()
    rc, d = _ma_chan(mod, mod.kiem_ban_ghi_thu_hoi, duong, "100644", "blob", _yaml_bytes(ok))
    chot(rc == 0 and d["cap_lai_cho"] is None, f"bản ghi hợp lệ phải 0 và cap_lai_cho chuẩn hoá None: {rc} {d}")
    rc, d = _ma_chan(mod, mod.kiem_ban_ghi_thu_hoi, duong, "100644", "blob",
                     _yaml_bytes(_ban_ghi_thu_hoi(cap_lai_cho="wp1-exec-2-claude-20260902", blob_da_biet_luc_ghi=[SHA40])))
    chot(rc == 0 and d["cap_lai_cho"] == "wp1-exec-2-claude-20260902", f"cap_lai_cho hợp lệ phải giữ: {rc} {d}")
    # 12 — nguồn/object/cấu trúc/ID
    for ten, mode, loai, than in (
        ("symlink 120000", "120000", "blob", _yaml_bytes(ok)),
        ("executable 100755", "100755", "blob", _yaml_bytes(ok)),
        ("type tree", "040000", "tree", b""),
        ("submodule", "160000", "commit", b""),
        ("YAML hỏng", "100644", "blob", b"lease_id: [\n"),
        ("khoá trùng", "100644", "blob", b"lease_id: a\nlease_id: b\n"),
        ("root không mapping", "100644", "blob", b"- 1\n"),
        ("lease_id khác tên tệp", "100644", "blob", _yaml_bytes(_ban_ghi_thu_hoi(lease_id="khac"))),
        ("lease_id không phải chuỗi", "100644", "blob", _yaml_bytes(_ban_ghi_thu_hoi(lease_id=5))),
        ("không phải UTF-8", "100644", "blob", b"\xff\xfe"),
    ):
        rc, td = _ma_chan(mod, mod.kiem_ban_ghi_thu_hoi, duong, mode, loai, than)
        chot(rc == 12, f"{ten}: đợi 12, được {rc}: {td}")
    for ten, than in (("thư mục con", "ops/thu-hoi/sub/x.yaml"), ("không .yaml", "ops/thu-hoi/x.yml")):
        rc, td = _ma_chan(mod, mod.kiem_ban_ghi_thu_hoi, than, "100644", "blob", _yaml_bytes(ok))
        chot(rc == 12, f"{ten}: đợi 12, được {rc}: {td}")
    # 4 — thẩm quyền: provider và người lạ đều 4, không phân biệt cách viết
    for nguoi in ("codex", "claude", "Codex", " codex ", "nguoi-la", "", None, 7):
        rc, td = _ma_chan(mod, mod.kiem_ban_ghi_thu_hoi, duong, "100644", "blob",
                          _yaml_bytes(_ban_ghi_thu_hoi(thu_hoi_boi=nguoi)))
        chot(rc == 4, f"thu_hoi_boi={nguoi!r}: đợi 4, được {rc}: {td}")
    # 8 — nội dung
    cases = {
        "thiếu ly_do": _ban_ghi_thu_hoi(ly_do=_BO), "khoá thừa": _ban_ghi_thu_hoi(them="x"),
        "schema_version chuỗi": _ban_ghi_thu_hoi(schema_version="1"),
        "schema_version bool": _ban_ghi_thu_hoi(schema_version=True),
        "event sai": _ban_ghi_thu_hoi(event="lease_granted"),
        "packet_issue bool": _ban_ghi_thu_hoi(packet_issue=True),
        "packet_issue âm": _ban_ghi_thu_hoi(packet_issue=-1),
        "packet_issue chuỗi": _ban_ghi_thu_hoi(packet_issue="488"),
        "thời điểm tương lai": _ban_ghi_thu_hoi(thu_hoi_luc_utc=mai_sau(1)),
        "thời điểm không Z": _ban_ghi_thu_hoi(thu_hoi_luc_utc="2026-09-01T00:00:00+00:00"),
        "thời điểm là datetime YAML": None,
        "ly_do rỗng": _ban_ghi_thu_hoi(ly_do="  "),
        "can_cu kho khác": _ban_ghi_thu_hoi(can_cu="https://github.com/o/r/issues/488#issuecomment-1"),
        "can_cu issue lệch": _ban_ghi_thu_hoi(can_cu=f"https://{KHO_CANONICAL_A0}/issues/489#issuecomment-1"),
        "can_cu không comment": _ban_ghi_thu_hoi(can_cu=f"https://{KHO_CANONICAL_A0}/issues/488"),
        "can_cu http": _ban_ghi_thu_hoi(can_cu=f"http://{KHO_CANONICAL_A0}/issues/488#issuecomment-1"),
        "cap_lai_cho bằng chính nó": _ban_ghi_thu_hoi(cap_lai_cho="wp1-exec-1-codex-20260901"),
        "cap_lai_cho ký tự lạ": _ban_ghi_thu_hoi(cap_lai_cho="a b"),
        "blob_da_biet không SHA40": _ban_ghi_thu_hoi(blob_da_biet_luc_ghi=["abc"]),
        "blob_da_biet không list": _ban_ghi_thu_hoi(blob_da_biet_luc_ghi=SHA40),
    }
    cases["thời điểm là datetime YAML"] = None
    for ten, d in cases.items():
        than = (b"schema_version: 1\nevent: lease_revoked\nlease_id: wp1-exec-1-codex-20260901\npacket_issue: 488\n"
                b"thu_hoi_boi: ducthangho\nthu_hoi_luc_utc: 2026-09-01T00:00:00Z\nly_do: x\n"
                + f"can_cu: https://{KHO_CANONICAL_A0}/issues/488#issuecomment-1\n".encode()) if d is None else _yaml_bytes(d)
        rc, td = _ma_chan(mod, mod.kiem_ban_ghi_thu_hoi, duong, "100644", "blob", than)
        chot(rc == 8, f"{ten}: đợi 8, được {rc}: {td}")
    # THỨ TỰ: nguồn sai + thẩm quyền sai ⇒ 12 (nguồn trước); thẩm quyền sai + nội dung sai ⇒ 4 (thẩm quyền trước)
    rc, _ = _ma_chan(mod, mod.kiem_ban_ghi_thu_hoi, duong, "120000", "blob", _yaml_bytes(_ban_ghi_thu_hoi(thu_hoi_boi="codex")))
    chot(rc == 12, f"nguồn sai + thẩm quyền sai phải 12, được {rc}")
    rc, _ = _ma_chan(mod, mod.kiem_ban_ghi_thu_hoi, duong, "100644", "blob", _yaml_bytes(_ban_ghi_thu_hoi(thu_hoi_boi="codex", ly_do=_BO)))
    chot(rc == 4, f"thẩm quyền sai + nội dung sai phải 4, được {rc}")
    # clock snapshot tiêm: cùng bản ghi, clock trước thời điểm ⇒ 8, clock sau ⇒ 0
    som = datetime(2020, 1, 1, tzinfo=timezone.utc)
    rc, _ = _ma_chan(mod, mod.kiem_ban_ghi_thu_hoi, duong, "100644", "blob", _yaml_bytes(ok), som)
    chot(rc == 8, f"clock snapshot sớm hơn thu_hoi_luc_utc phải 8, được {rc}")


@ca
def t128_S7_dinh_tuyen_metadata_dung_MOT_path_va_schema_retired():
    """S7/Q13: đúng MỘT path reserved đi schema metadata; tên GẦN reserved vẫn là bản ghi M1; metadata lỗi ⇒ 12."""
    mod = _nap_cong()
    P = mod.PATH_NGOAI_LE_RETIRED
    chot(P == "ops/thu-hoi/_ngoai-le-closure.retired.yaml", f"path reserved trôi: {P}")
    chot(mod.phan_tuyen_so(P) == "metadata", "path reserved phải là metadata")
    for gan in ("ops/thu-hoi/_ngoai-le-closure.retired.yml", "ops/thu-hoi/ngoai-le-closure.retired.yaml",
                "ops/thu-hoi/_ngoai-le-closure.retired.yaml.bak", "ops/thu-hoi/_Ngoai-le-closure.retired.yaml",
                "ops/thu-hoi/sub/_ngoai-le-closure.retired.yaml", "ops/thu-hoi/x.yaml", "ops/thu-hoi/sub"):
        chot(mod.phan_tuyen_so(gan) == "thu_hoi", f"{gan} phải đi tuyến thu_hoi (M1), không phải metadata")
    for ngoai in ("ops/thu-hoi", "ops/thu-hoi.yaml", "ops/leases/x.yaml", "docs/ops/thu-hoi/x.yaml"):
        chot(mod.phan_tuyen_so(ngoai) is None, f"{ngoai} nằm ngoài sổ, phải None")
    # tên gần reserved đi M1 thật: nội dung là metadata hợp lệ ⇒ M1 từ chối (lease_id thiếu ⇒ 12)
    rc, td = _ma_chan(mod, mod.kiem_ban_ghi_thu_hoi, "ops/thu-hoi/ngoai-le-closure.retired.yaml", "100644", "blob",
                      _yaml_bytes(_metadata_retired()))
    chot(rc == 12, f"tên gần reserved mang nội dung metadata phải bị M1 từ chối 12, được {rc}: {td}")
    rc, d = _ma_chan(mod, mod.kiem_metadata_retired, P, "100644", "blob", _yaml_bytes(_metadata_retired()))
    chot(rc == 0 and d["event"] == "closure_exception_retired", f"metadata hợp lệ phải 0: {rc} {d}")
    for ten, mode, loai, than in (
        ("symlink", "120000", "blob", _yaml_bytes(_metadata_retired())),
        ("executable", "100755", "blob", _yaml_bytes(_metadata_retired())),
        ("thiếu khoá", "100644", "blob", _yaml_bytes(_metadata_retired(retired_at_utc=_BO))),
        ("thừa khoá", "100644", "blob", _yaml_bytes(_metadata_retired(them=1))),
        ("event sai", "100644", "blob", _yaml_bytes(_metadata_retired(event="lease_revoked"))),
        ("schema bool", "100644", "blob", _yaml_bytes(_metadata_retired(schema_version=True))),
        ("sha256 ngắn", "100644", "blob", _yaml_bytes(_metadata_retired(descriptor_sha256="abc"))),
        ("base_sha sai", "100644", "blob", _yaml_bytes(_metadata_retired(base_sha_before_add="x" * 40))),
        ("tương lai", "100644", "blob", _yaml_bytes(_metadata_retired(retired_at_utc=mai_sau(1)))),
        ("khoá trùng", "100644", "blob", b"schema_version: 1\nschema_version: 1\n"),
        ("YAML hỏng", "100644", "blob", b"a: [\n"),
    ):
        rc, td = _ma_chan(mod, mod.kiem_metadata_retired, P, mode, loai, than)
        chot(rc == 12, f"metadata {ten}: đợi 12, được {rc}: {td}")


@ca
def t129_Q45_reader_object_store_bam_lai_va_canh_tu_bytes():
    """Q4.5: KhoObject đọc commit/tree/blob từ object-store cô lập, băm lại, type đúng, ancestry tự đi đồ thị;
    `missing` là 12 chứ không phải 'vắng'; tree cha ĐÃ XÁC MINH vắng entry mới là map rỗng."""
    mod = _nap_cong()
    with San() as s:
        cay, (c0, c1, c2) = _kho_do_thi(s)
        kho = mod.KhoObject(cay)
        try:
            rc0, kq0 = _ma_chan(mod, kho.commit, c2)
            chot(rc0 == 0, f"positive control: đọc commit c2 qua object-store đã routing phải 0: {rc0} {kq0}")
            tree2, cha = kq0
            chot(tree2 == _g_a0(cay, "rev-parse", f"{c2}^{{tree}}") and cha == [c1], f"commit(c2) sai: {tree2} {cha}")
            ds = kho.tree(tree2)
            chot({e[1] for e in ds} == {"README.md", "docs", "ops"}, f"tree(c2) sai: {ds}")
            mode_docs = next(e for e in ds if e[1] == "docs")
            chot(mode_docs[0] == "040000" and mode_docs[3] == "tree", f"entry thư mục sai: {mode_docs}")
            muc = kho.tim(tree2, "ops/leases/x.yaml")
            chot(muc and muc[0] == "100644" and muc[2] == "blob", f"tim sai: {muc}")
            chot(kho.doc(muc[1], "blob") == b"lease_id: x\n", "blob bytes sai")
            chot(kho.tim(tree2, "ops/khong-co") is None, "tim vắng phải None")
            # Đường đi XUYÊN một blob KHÔNG phải "vắng": tổ tiên non-tree ⇒ 12 (Codex review 457affd, P1; xem t151)
            rc, td = _ma_chan(mod, kho.tim, tree2, "README.md/x")
            chot(rc == 12 and "tổ tiên" in td, f"tim qua blob phải 12, không được suy vắng: {rc} {td}")
            chot(kho.namespace(tree2, "ops/thu-hoi") == {}, "namespace của thư mục vắng phải rỗng")
            ns = kho.namespace(tree2, "ops/leases")
            chot(list(ns) == ["ops/leases/x.yaml"] and ns["ops/leases/x.yaml"][:2] == ("100644", "blob"), f"namespace sai: {ns}")
            chot(kho.to_tien(c0, c2) == 2 and kho.to_tien(c1, c2) == 1 and kho.to_tien(c2, c2) == 0, "witness sai")
            rc, td = _ma_chan(mod, kho.to_tien, c2, c0)
            chot(rc == 12 and "không phải tổ tiên" in td, f"S không phải tổ tiên phải 12: {rc} {td}")
            rc, td = _ma_chan(mod, kho.doc, "0" * 40, "blob")
            chot(rc == 12 and "missing" in td, f"OID vắng phải 12 kèm 'missing': {rc} {td}")
            rc, td = _ma_chan(mod, kho.doc, "abc", "blob")
            chot(rc == 12, f"OID sai dạng phải 12: {rc} {td}")
            rc, td = _ma_chan(mod, kho.doc, c2, "blob")
            chot(rc == 12 and "hai type" in td, f"cùng OID đòi hai type phải 12: {rc} {td}")
            kho_moi = mod.KhoObject(cay)
            try:
                rc, td = _ma_chan(mod, kho_moi.doc, c2, "blob")
                chot(rc == 12 and "mong đợi blob" in td and kho_moi.memo == {}, f"type lệch phải 12 và không memo: {rc} {td}")
            finally:
                kho_moi.dong()
            chot(kho.doc(c2, "commit") is not None, "memo commit còn đọc được")
            rc, td = _ma_chan(mod, kho.doc, tree2, "blob")
            chot(rc == 12, f"đòi tree bằng type blob phải 12: {rc} {td}")
            rc, td = _ma_chan(mod, kho.namespace, tree2, "README.md")
            chot(rc == 12, f"namespace trên blob phải 12: {rc} {td}")
            so_truoc = kho.so_object
            kho.commit(c2); kho.tree(tree2)
            chot(kho.so_object == so_truoc, "memo (type, OID) phải không đếm lại object")
        finally:
            kho.dong()
        # refs/replace ở KHO NGUỒN không đổi bytes đọc được (GIT_DIR tạm không có ref nào)
        _g_a0(cay, "replace", "-f", c1, c0)
        kho = mod.KhoObject(cay)
        try:
            _, cha = kho.commit(c2)
            chot(cha == [c1], f"replace ở kho nguồn không được đổi cạnh: {cha}")
            chot(kho.commit(c1)[1] == [c0], "commit c1 phải đọc bytes THẬT của c1, không phải bản replace")
        finally:
            kho.dong()


@ca
def t130_S2_seam_bytes_lech_OID_12_va_parser_KHONG_nhan_byte():
    """A6 seam: bytes lệch sau framing/trước băm ⇒ 12 và parser nhận 0 byte chưa xác minh (memo rỗng, không cạnh)."""
    mod = _nap_cong()
    with San() as s:
        cay, (c0, c1, c2) = _kho_do_thi(s)
        goi = []
        def lech(oid, loai, kich, than):
            goi.append(oid)
            return loai, kich, than[:-1] + (b"X" if than[-1:] != b"X" else b"Y")
        kho = mod.KhoObject(cay, sau_cat_file=lech)
        try:
            rc, td = _ma_chan(mod, kho.commit, c2)
            chot(rc == 12 and "băm ra" in td, f"bytes lệch phải 12 'băm ra': {rc} {td}")
            chot(goi == [c2] and kho.memo == {} and kho.so_object == 0, f"parser đã nhận byte chưa xác minh: memo={list(kho.memo)}")
            rc, td = _ma_chan(mod, kho.to_tien, c0, c2)
            chot(rc == 12 and kho.memo == {}, "ancestry không được sinh cạnh từ bytes lệch")
        finally:
            kho.dong()
        # seam đổi TYPE (bytes giữ nguyên) ⇒ băm lệch ⇒ 12
        kho = mod.KhoObject(cay, sau_cat_file=lambda oid, loai, kich, than: ("blob", kich, than))
        try:
            rc, td = _ma_chan(mod, kho.commit, c2)
            chot(rc == 12 and kho.memo == {}, f"đổi type qua seam phải 12: {rc} {td}")
        finally:
            kho.dong()
        # control: seam trả nguyên ⇒ 0
        kho = mod.KhoObject(cay, sau_cat_file=lambda oid, loai, kich, than: (loai, kich, than))
        try:
            chot(kho.to_tien(c0, c2) == 2, "seam trung thực phải đọc được")
        finally:
            kho.dong()


@ca
def t131_S8_tam_tran_bound_tru_1_bound_bound_cong_1_va_deadline():
    """Q4.5: bảy trần count/byte/depth biên INCLUSIVE — bound−1/bound/bound+1 ⇒ 12/0/0 (đo theo n = giá trị
    thực); deadline theo clock tiêm và subprocess im lặng bị KILL."""
    import time
    mod = _nap_cong()
    with San() as s:
        cay, (c0, c1, c2) = _kho_do_thi(s)
        (cay / "a" / "b").mkdir(parents=True)
        (cay / "a" / "b" / "c.txt").write_bytes(b"z" * 100)
        _g_a0(cay, "add", "-A"); _g_a0(cay, "commit", "-qm", "c3")
        c3 = _g_a0(cay, "rev-parse", "HEAD")
        tree3 = _g_a0(cay, "rev-parse", f"{c3}^{{tree}}")
        blob = _g_a0(cay, "rev-parse", f"{c3}:a/b/c.txt")
        kich_c3 = int(_g_a0(cay, "cat-file", "-s", c3))

        def do(ngan_sach, viec):
            kho = mod.KhoObject(cay, ngan_sach=ngan_sach)
            try:
                return _ma_chan(mod, viec, kho)
            finally:
                kho.dong()

        bang_tran = [
            ("max_parent_path_edges", 3, lambda k: k.to_tien(c0, c3)),                       # witness = 3 cạnh
            ("max_unique_objects", 3, lambda k: (k.commit(c3), k.tree(tree3), k.doc(blob, "blob"))),
            ("max_object_bytes", 100, lambda k: k.doc(blob, "blob")),
            ("max_total_object_bytes", kich_c3 + 100, lambda k: (k.commit(c3), k.doc(blob, "blob"))),
            ("max_tree_or_alias_edges", 3, lambda k: k.tim(tree3, "a/b/c.txt")),
        ]
        for ten, n, viec in bang_tran:
            for delta, mong in ((-1, 12), (0, 0), (1, 0)):
                rc, td = do({ten: n + delta}, viec)
                chot(rc == mong, f"{ten}: n={n}, bound={n + delta} đợi {mong}, được {rc}: {td}")
        # exact-bound ancestry: đường đúng bound KHÔNG bị gọi là 'chạm trần' (S10)
        rc, td = do({"max_parent_path_edges": 3}, lambda k: k.to_tien(c0, c3))
        chot(rc == 0 and td == 3, f"đường đúng bound phải hợp lệ: {rc} {td}")
        # alternate: chuỗi store depth 3/4/5 dưới max_alternate_depth=4 ⇒ 0/0/12; max_alternate_stores tương tự
        dem_alt = [0]
        def kho_alt(so_store):
            dem_alt[0] += 1
            goc = s / f"alt{dem_alt[0]}-{so_store}"; goc.mkdir()
            _g_a0(goc, "init", "-q", "-b", "master")
            (goc / "f").write_text("f\n", encoding="utf-8"); _g_a0(goc, "add", "-A"); _g_a0(goc, "commit", "-qm", "f")
            stores = []
            for i in range(so_store):
                st = s / f"alt{dem_alt[0]}-{so_store}-s{i}"; subprocess.run(["git", "init", "-q", "--bare", str(st)], check=True)
                stores.append(st / "objects")
            truoc = goc / ".git" / "objects"
            for st in stores:
                (truoc / "info").mkdir(exist_ok=True); (truoc / "info" / "alternates").write_text(str(st) + "\n")
                truoc = st
            return goc, _g_a0(goc, "rev-parse", "HEAD")
        for so, mong in ((3, 0), (4, 0), (5, 12)):
            goc, h = kho_alt(so)
            rc, td = _ma_chan(mod, lambda: mod.KhoObject(goc, ngan_sach={"max_alternate_depth": 4, "max_alternate_stores": 8}))
            if rc == 0:
                td.dong()
            chot(rc == mong, f"alternate depth {so} dưới bound 4 đợi {mong}, được {rc}: {td}")
        goc, h = kho_alt(3)
        for bound, mong in ((2, 12), (3, 0), (4, 0)):
            rc, td = _ma_chan(mod, lambda: mod.KhoObject(goc, ngan_sach={"max_alternate_stores": bound, "max_alternate_depth": 9}))
            if rc == 0:
                td.dong()
            chot(rc == mong, f"max_alternate_stores={bound} với 3 store đợi {mong}, được {rc}: {td}")
        # deadline theo clock tiêm: đúng deadline khi việc còn chờ ⇒ 12; trước deadline ⇒ 0
        kho = mod.KhoObject(cay, bay_gio=lambda: 100.0, deadline=100.0)
        try:
            rc, td = _ma_chan(mod, kho.commit, c3)
            chot(rc == 12 and "deadline" in td and "kill" not in td and kho.memo == {},
                 f"chạm deadline phải 12 ở lớp TRƯỚC spawn (không phải lớp join-timeout/kill): {rc} {td}")
        finally:
            kho.dong()
        kho = mod.KhoObject(cay, bay_gio=lambda: 100.0, deadline=100.5)
        try:
            chot(kho.commit(c3)[0] == tree3, "trước deadline phải đọc được")
        finally:
            kho.dong()
        # subprocess IM LẶNG (không bao giờ trả header) phải bị ngắt và kill trong deadline thật.
        # Launcher phải là thứ NỀN NẠP ĐƯỢC: `.sh` + shebang là giao ước POSIX, còn Windows nạp
        # thẳng một `.sh` cho `OSError [WinError 193] %1 is not a valid Win32 application` — đo
        # được trên Windows 11 thật 20-09-2026 (#578 M1). Ca chết ở ĐÓ, tức bảy trần và phần
        # deadline/kill mà docstring khai CHƯA TỪNG được đo trên Windows.
        #
        # `.cmd` vòng lặp thuần, và ba điều kiện của nó đều bị mã sản phẩm ép, không phải tuỳ ý:
        # KHÔNG gọi lệnh ngoài (`self.env` dựng bằng `_env_rong` nên PATH chỉ có thư mục git,
        # không có System32); KHÔNG đọc stdin (sản phẩm ghi oid rồi `close()`); KHÔNG ghi stdout
        # (reader phải treo tới deadline). Đo được: ứng viên này chạy đúng dưới CHÍNH `self.env`
        # ấy, nên `SystemRoot`/`COMSPEC` vắng mặt không chặn — thủ phạm KHÔNG nằm ở mã sản phẩm.
        if os.name == "nt":
            im = s / "git-im-lang.cmd"
            im.write_text("@echo off\r\n:lap\r\ngoto lap\r\n", encoding="ascii")
        else:
            im = s / "git-im-lang.sh"
            im.write_text("#!/bin/sh\nsleep 30\n", encoding="utf-8"); im.chmod(0o755)
        kho = mod.KhoObject(cay, deadline=time.monotonic() + 0.6)
        try:
            kho.git_exe = str(im)
            t0 = time.monotonic()
            rc, td = _ma_chan(mod, kho.doc, c3, "commit")
            troi = time.monotonic() - t0
            chot(rc == 12 and "kill" in td and troi < 5, f"subprocess im lặng phải bị kill trong deadline: rc={rc} sau {troi:.1f}s: {td}")
            # N1: một dòng ĐỌC ĐƯỢC chứng minh ca đã TỚI phần deadline/kill. "Không ném" không
            # phải bằng chứng — ca này từng chết trước đoạn này trên Windows mà suite vẫn chỉ
            # thấy một dòng ĐỎ không nói được nó chết ở đâu. Cố ý TẤT ĐỊNH (không giờ, không
            # đường dẫn tạm): t125 so TẬP TÊN ca đỏ, nhưng một dòng trôi vẫn là nợ.
            _nhat_ky_ca("=== t131 deadline/kill DA CHAY, launcher", im.suffix)
        finally:
            kho.dong()


@ca
def t132_shallow_va_object_thieu_la_12_khong_phai_vang():
    """Kho shallow ⇒ 12 ngay khi mở reader; partial (object thiếu) ⇒ 12 khi chạm."""
    mod = _nap_cong()
    with San() as s:
        cay, (c0, c1, c2) = _kho_do_thi(s)
        nong = s / "nong"
        subprocess.run(["git", "-c", "protocol.file.allow=always", "clone", "-q", "--depth=1",
                        f"file://{cay}", str(nong)], check=True, capture_output=True)
        rc, td = _ma_chan(mod, lambda: mod.KhoObject(nong))
        if rc == 0:
            td.dong()
        chot(rc == 12 and "shallow" in td, f"kho shallow phải 12: {rc} {td}")
        # chuẩn bị đầy đủ TRƯỚC snapshot ⇒ 0
        subprocess.run(["git", "-C", str(nong), "-c", "protocol.file.allow=always", "fetch", "-q", "--unshallow"],
                       check=True, capture_output=True)
        kho = mod.KhoObject(nong)
        try:
            chot(kho.to_tien(c0, c2) == 2, "sau --unshallow phải đọc trọn đồ thị")
        finally:
            kho.dong()
        # partial: xoá loose object của c1 khỏi store ⇒ ancestry chạm c1 ⇒ 12 'missing'
        loose = cay / ".git" / "objects" / c1[:2] / c1[2:]
        chot(loose.is_file(), "fixture cần loose object của c1")
        # Git đặt loose object CHỈ-ĐỌC (đo được `mode=0o444`, `W_OK=False`). POSIX chỉ cần quyền
        # ghi trên THƯ MỤC nên `unlink` chạy; Windows từ chối xoá tệp chỉ-đọc →
        # `PermissionError [WinError 5] Access is denied` (#578 M2, đo trên Windows 11 thật).
        # Giả thuyết "handle git còn mở" bị LOẠI TRỪ BẰNG PHÉP ĐO, không bằng lập luận: `chmod`
        # một mình đã đủ, và một đối chứng riêng xác nhận nền ấy thật sự từ chối xoá tệp chỉ-đọc.
        try:
            loose.unlink()
        except PermissionError:
            os.chmod(loose, 0o666)
            loose.unlink()
        # N2: "đã xoá" KHÁC "bỏ qua vì không xoá được". Thiếu chốt này thì một bản vá
        # `except PermissionError: pass` cũng làm ca XANH — và ca ấy thôi đo gì nữa.
        chot(not loose.exists(), "loose object của c1 PHẢI biến mất trước khi đo 'missing'")
        kho = mod.KhoObject(cay)
        try:
            rc, td = _ma_chan(mod, kho.to_tien, c0, c2)
            chot(rc == 12 and "missing" in td, f"object thiếu phải 12 'missing': {rc} {td}")
        finally:
            kho.dong()


@ca
def t133_M4_kiem_thu_hoi_github_receipt_append_only_va_che_do_chua_kich_hoat():
    """M4 end-to-end: ancestry S→H, T = tree(H), map append-only (8) trước validator, chế độ chưa kích hoạt
    đòi tập revocation RỖNG ở S và T (12), metadata Q13 cần policy; receipt S/H/T; CLI thật cũng chạy."""
    import json
    mod = _nap_cong()
    with San() as s:
        cay, (c0, c1, S) = _kho_do_thi(s)
        RET = "ops/thu-hoi/_ngoai-le-closure.retired.yaml"
        POL = ".github/coordination/change-impact.v1.json"
        H_sach = _them_commit(cay, "h-sach", S, {"docs/b.md": b"b\n"})
        H_thu_hoi = _them_commit(cay, "h-thu-hoi", S, {"ops/thu-hoi/wp1-exec-1-codex-20260901.yaml": _yaml_bytes(_ban_ghi_thu_hoi())})
        H_meta_policy = _them_commit(cay, "h-meta", S, {RET: _yaml_bytes(_metadata_retired()), POL: b"{}\n"})
        H_meta_khong_policy = _them_commit(cay, "h-meta-0", S, {RET: _yaml_bytes(_metadata_retired())})
        H_meta_hong = _them_commit(cay, "h-meta-hong", S, {RET: b"a: [\n", POL: b"{}\n"})
        H_symlink = _them_commit(cay, "h-symlink", S, {}, symlink=("ops/thu-hoi/x.yaml", "../leases/x.yaml"))
        H_thu_muc_con = _them_commit(cay, "h-sub", S, {"ops/thu-hoi/sub/x.yaml": b"a: 1\n"})
        H_khong_yaml = _them_commit(cay, "h-yml", S, {"ops/thu-hoi/wp1-exec-1-codex-20260901.yml": _yaml_bytes(_ban_ghi_thu_hoi())})
        # S' có metadata + policy; H sửa / xoá metadata ⇒ append-only 8
        S2 = H_meta_policy
        H_sua_meta = _them_commit(cay, "h-sua-meta", S2, {RET: _yaml_bytes(_metadata_retired(retired_at_utc=khi_truoc(2)))})
        H_xoa_meta = _them_commit(cay, "h-xoa-meta", S2, {"docs/c.md": b"c\n"}, xoa=(RET,))
        H_them_tren_S2 = _them_commit(cay, "h-them-s2", S2, {"docs/c.md": b"c\n"})
        # S'' có bản ghi thu hồi (lọt trước kích hoạt); H xoá nó ⇒ 8 (append-only đứng TRƯỚC chốt inactive)
        S3 = H_thu_hoi
        H_xoa_thu_hoi = _them_commit(cay, "h-xoa-th", S3, {"docs/d.md": b"d\n"}, xoa=("ops/thu-hoi/wp1-exec-1-codex-20260901.yaml",))
        H_giu_thu_hoi = _them_commit(cay, "h-giu-th", S3, {"docs/d.md": b"d\n"})

        def m4(H, S_, receipt=None, nhanh="master", goc=cay):
            argv = ["kiem-thu-hoi-github", H, "--canonical-base", S_, "--nhanh-mac-dinh", nhanh, "--root", str(goc)]
            if receipt:
                argv += ["--receipt", str(receipt)]
            return _goi_main(mod, *argv)

        rcp = s / "receipt.json"
        rc, o, e = m4(H_sach, S, rcp)
        chot(rc == 0 and "TAP_THU_HOI_RONG" in o, f"H sạch phải 0: {rc} {o!r} {e!r}")
        d = json.loads(rcp.read_text(encoding="utf-8"))
        tree_H = _g_a0(cay, "rev-parse", f"{H_sach}^{{tree}}")
        chot(d["S"] == S and d["H"] == H_sach and d["T"] == tree_H and d["canh_ancestry"] == 1
             and d["ket_luan"] == "TAP_THU_HOI_RONG" and d["che_do"] == "chua_kich_hoat"
             and d["profile_digest"] is None and d["discovery"].startswith("KHONG_CHAY")
             and d["oid_bo_kiem_tai_S"] == _g_a0(cay, "rev-parse", f"{S}:ops/lease_publish.py")
             and d["nhanh_mac_dinh"] == "master" and d["kho_canonical"] == KHO_CANONICAL_A0
             and set(d["ngan_sach"]) == set(mod.NGAN_SACH_MAC_DINH), f"receipt sai: {d}")
        rc, o, e = m4(S, S, rcp)
        chot(rc == 0 and json.loads(rcp.read_text())["canh_ancestry"] == 0, f"H == S phải 0 với 0 cạnh: {rc} {e!r}")
        rcp.unlink()
        rc, o, e = m4(c0, S, rcp)
        chot(rc == 12 and "không phải tổ tiên" in e and not rcp.exists(), f"S không tổ tiên H phải 12, không receipt: {rc} {e!r}")
        rc, o, e = m4(H_thu_hoi, S, rcp)
        chot(rc == 12 and "CHƯA KÍCH HOẠT" in e and not rcp.exists(), f"bản ghi thu hồi HỢP LỆ khi inactive phải 12: {rc} {e!r}")
        # F01/Q13: marker MỚI khi descriptor CHƯA ghim (A0) ⇒ 12, kể cả policy JSON hợp lệ; policy mà không marker ⇒ 12
        rc, o, e = m4(H_meta_policy, S, rcp)
        chot(rc == 12 and "descriptor" in e and not rcp.exists(), f"marker mới ở A0 (descriptor chưa ghim) phải 12: {rc} {e!r}")
        H_policy_khong_marker = _them_commit(cay, "h-policy-0", S, {POL: b"{}\n"})
        rc, o, e = m4(H_policy_khong_marker, S)
        chot(rc == 12 and "thiếu marker" in e, f"policy không marker phải 12 (không grandfather): {rc} {e!r}")
        # Binding Q13 với descriptor GHIM (tiêm qua thuộc tính module — API nội bộ, không CLI): đúng cả ba ⇒ 0;
        # sai từng cái ⇒ 12; policy đã có ở S mà marker mới ⇒ 12
        import hashlib as _h
        POL_BYTES = b'{"schema": 1}\n'
        DESC = "c" * 64
        dung = _metadata_retired(descriptor_sha256=DESC, first_policy_sha256=_h.sha256(POL_BYTES).hexdigest(), base_sha_before_add=S)
        H_bind_ok = _them_commit(cay, "h-bind-ok", S, {RET: _yaml_bytes(dung), POL: POL_BYTES})
        H_bind_desc = _them_commit(cay, "h-bind-desc", S, {RET: _yaml_bytes(dict(dung, descriptor_sha256="d" * 64)), POL: POL_BYTES})
        H_bind_hash = _them_commit(cay, "h-bind-hash", S, {RET: _yaml_bytes(dict(dung, first_policy_sha256="e" * 64)), POL: POL_BYTES})
        H_bind_base = _them_commit(cay, "h-bind-base", S, {RET: _yaml_bytes(dict(dung, base_sha_before_add=c0)), POL: POL_BYTES})
        H_bind_pol_hong = _them_commit(cay, "h-bind-hong", S, {RET: _yaml_bytes(dung), POL: b"[1]\n"})
        H_bind_pol_exec = _them_commit(cay, "h-bind-exec", S, {RET: _yaml_bytes(dung), POL: POL_BYTES})
        _g_a0(cay, "update-index", "--chmod=+x", POL); _g_a0(cay, "commit", "-qm", "exec"); H_bind_pol_exec = _g_a0(cay, "rev-parse", "HEAD")
        S_pol = H_policy_khong_marker
        H_bind_S_co_policy = _them_commit(cay, "h-bind-s-pol", S_pol, {RET: _yaml_bytes(dict(
            dung, base_sha_before_add=S_pol, first_policy_sha256=_h.sha256(b"{}\n").hexdigest()))})
        mod.DESCRIPTOR_Q13_SHA256 = DESC
        try:
            rc, o, e = m4(H_bind_ok, S, rcp)
            d = json.loads(rcp.read_text(encoding="utf-8"))
            chot(rc == 0 and d["metadata_T"] == [RET] and d["thu_hoi_moi"] == [] and d["policy_T"]["sha256"] == _h.sha256(POL_BYTES).hexdigest()
                 and d["descriptor_q13_ghim"] == DESC, f"binding Q13 đúng cả ba phải 0: {rc} {e!r} {d.get('policy_T')}")
            for ten, H, dau in (("descriptor lệch", H_bind_desc, "descriptor_sha256"), ("hash policy lệch", H_bind_hash, "first_policy_sha256"),
                                ("base lệch", H_bind_base, "base_sha_before_add"), ("policy không object", H_bind_pol_hong, "JSON object"),
                                ("policy executable", H_bind_pol_exec, "100644"), ("S đã có policy", H_bind_S_co_policy, "grandfather")):
                rc, o, e = m4(H, S_pol if H is H_bind_S_co_policy else S)
                chot(rc == 12 and dau in e, f"binding {ten}: đợi 12 '{dau}', được {rc}: {e!r}")
            # marker CŨ (đã ở S2 canonical) không bị đòi binding lại: chỉ policy T phải là JSON object
            rc, o, e = m4(_them_commit(cay, "h-old-marker", H_bind_ok, {"docs/z.md": b"z\n"}), H_bind_ok)
            chot(rc == 0, f"marker cũ + policy hợp lệ ở T phải 0: {rc} {e!r}")
            rc, o, e = m4(_them_commit(cay, "h-old-marker-pol-hong", H_bind_ok, {POL: b"not JSON\n"}), H_bind_ok)
            chot(rc == 12 and "JSON" in e, f"marker cũ nhưng policy T hỏng phải 12: {rc} {e!r}")
        finally:
            mod.DESCRIPTOR_Q13_SHA256 = None
        for ten, H, mong, dau in (
            ("metadata không policy", H_meta_khong_policy, 12, "policy"),
            ("metadata hỏng", H_meta_hong, 12, "YAML"),
            ("symlink trong sổ", H_symlink, 12, "100644"),
            ("thư mục con", H_thu_muc_con, 12, "100644"),
            ("tên .yml gần reserved", H_khong_yaml, 12, ""),
        ):
            rc, o, e = m4(H, S)
            chot(rc == mong and dau in e, f"{ten}: đợi {mong} '{dau}', được {rc}: {e!r}")
        rc, o, e = m4(H_sua_meta, S2)
        chot(rc == 8 and "append-only" in e, f"sửa metadata phải 8 append-only: {rc} {e!r}")
        rc, o, e = m4(H_xoa_meta, S2)
        chot(rc == 8 and "append-only" in e, f"xoá metadata phải 8: {rc} {e!r}")
        rc, o, e = m4(H_them_tren_S2, S2)
        chot(rc == 0, f"control: marker cũ ở S2 + policy JSON object, thêm tệp ngoài sổ phải 0: {rc} {e!r}")
        rc, o, e = m4(H_xoa_thu_hoi, S3)
        chot(rc == 8 and "append-only" in e, f"xoá bản ghi ở S phải 8 (append-only TRƯỚC inactive): {rc} {e!r}")
        rc, o, e = m4(H_giu_thu_hoi, S3)
        chot(rc == 12 and "S có 1" in e, f"S có bản ghi khi inactive phải 12: {rc} {e!r}")
        # tham số
        rc, o, e = m4(H_sach, "abc")
        chot(rc == 2, f"S không SHA40 phải 2: {rc}")
        rc, o, e = m4(H_sach, S, nhanh="refs/heads/master")
        chot(rc == 2, f"--nhanh-mac-dinh có '/' phải 2: {rc}")
        # KHÔNG có cờ nào đổi được nguồn/profile/endpoint ở CLI (A2)
        for co in ("--endpoint", "--profile", "--da-duyet", "--kho-canonical", "--kich-hoat"):
            rc_, o_, e_ = chay("kiem-thu-hoi-github", H_sach, "--canonical-base", S, "--nhanh-mac-dinh", "master",
                               "--root", str(cay), co, "x")
            chot(rc_ == 2 and "unrecognized" in e_, f"cờ {co} phải bị argparse từ chối: {rc_} {e_!r}")
        # CLI THẬT (subprocess): cùng verdict
        rc_, o_, e_ = chay("kiem-thu-hoi-github", H_sach, "--canonical-base", S, "--nhanh-mac-dinh", "master",
                           "--root", str(cay), "--receipt", str(rcp))
        chot(rc_ == 0 and "THU_HOI_ADMISSION TAP_THU_HOI_RONG" in o_, f"CLI thật H sạch: {rc_} {o_!r} {e_!r}")
        rc_, o_, e_ = chay("kiem-thu-hoi-github", H_thu_hoi, "--canonical-base", S, "--nhanh-mac-dinh", "master", "--root", str(cay))
        chot(rc_ == 12, f"CLI thật bản ghi khi inactive phải 12: {rc_} {e_!r}")
        # cây làm việc của kho bị đổi KHÔNG ảnh hưởng: reader đọc object-store, không đọc checkout
        _g_a0(cay, "checkout", "-q", H_thu_hoi)
        rc, o, e = m4(H_sach, S)
        chot(rc == 0, f"checkout hiện tại không được đổi verdict: {rc} {e!r}")


@ca
def t134_M2_ai_dang_giu_so_khong_rong_khi_co_False_la_12_va_du_bao_khong_doi_rc():
    """M2 chế độ chưa kích hoạt: bản ghi thu hồi trên BẤT KỲ ref ⇒ 12; metadata cần policy; `--du-bao` chỉ
    thêm dòng `DU_BAO:`, verdict và rc = luật cũ."""
    mod = _nap_cong()
    with San() as s:
        cay, g = _kho_thu(s)
        rc, o, e = _goi_main(mod, "ai-dang-giu", "ops/x.md", "--root", str(cay))
        chot(rc == 0 and "DU_BAO" not in o, f"nền không sổ, không --du-bao: {rc} {o!r} {e!r}")
        rc2, o2, e2 = _goi_main(mod, "ai-dang-giu", "ops/x.md", "--root", str(cay), "--du-bao")
        chot(rc2 == rc and o2.count("DU_BAO:") >= 3 and "SO_THU_HOI_KICH_HOAT=False" in o2
             and "MÙ 0" in o2, f"--du-bao phải thêm dòng DU_BAO, rc giữ: {rc2} {o2!r}")
        chot([x for x in o2.splitlines() if not x.startswith("DU_BAO")] == o.splitlines(),
             "ngoài dòng DU_BAO, đầu ra phải Y HỆT lượt không --du-bao")
        rc3, o3, _ = _goi_main(mod, "ai-dang-giu", "ops/x.md", "--root", str(cay), "--du-bao", "--nhanh-mac-dinh", "khong-co")
        chot(rc3 == rc and "KHÔNG ĐO ĐƯỢC" in o3, f"nhánh mặc định vắng trong cache ⇒ dự báo KHÔNG ĐO ĐƯỢC, rc giữ: {rc3} {o3!r}")
        # bản ghi thu hồi trên một nhánh feature (không phải master) ⇒ 12 ở consumer vận hành
        g(cay, "checkout", "-q", "-b", "feature")
        (cay / "ops" / "thu-hoi").mkdir()
        (cay / "ops" / "thu-hoi" / "wp1-exec-1-codex-20260901.yaml").write_bytes(_yaml_bytes(_ban_ghi_thu_hoi()))
        g(cay, "add", "-A"); g(cay, "commit", "-qm", "so"); g(cay, "push", "-q", "origin", "feature")
        rc, o, e = _goi_main(mod, "ai-dang-giu", "ops/x.md", "--root", str(cay))
        chot(rc == 12 and "SO_THU_HOI_KICH_HOAT=False" in e and "feature" in e, f"sổ không rỗng khi cờ False phải 12: {rc} {e!r}")
        # cả tệp RÁC trong sổ (không phải bản ghi hợp lệ) cũng 12 — không grandfather, không bỏ qua
        g(cay, "rm", "-q", "ops/thu-hoi/wp1-exec-1-codex-20260901.yaml")
        (cay / "ops" / "thu-hoi").mkdir(exist_ok=True)
        (cay / "ops" / "thu-hoi" / "rac.txt").write_text("x\n", encoding="utf-8")
        g(cay, "add", "-A"); g(cay, "commit", "-qm", "rac"); g(cay, "push", "-q", "origin", "feature")
        rc, o, e = _goi_main(mod, "ai-dang-giu", "ops/x.md", "--root", str(cay))
        chot(rc == 12, f"tệp rác trong sổ phải 12: {rc} {e!r}")
        # metadata reserved không policy ⇒ 12; có policy ⇒ verdict cũ
        g(cay, "rm", "-q", "ops/thu-hoi/rac.txt")
        (cay / "ops" / "thu-hoi").mkdir(exist_ok=True)
        (cay / "ops" / "thu-hoi" / "_ngoai-le-closure.retired.yaml").write_bytes(_yaml_bytes(_metadata_retired()))
        g(cay, "add", "-A"); g(cay, "commit", "-qm", "meta"); g(cay, "push", "-q", "origin", "feature")
        rc, o, e = _goi_main(mod, "ai-dang-giu", "ops/x.md", "--root", str(cay))
        chot(rc == 12 and "policy" in e, f"metadata không policy phải 12: {rc} {e!r}")
        (cay / ".github" / "coordination").mkdir(parents=True)
        (cay / ".github" / "coordination" / "change-impact.v1.json").write_text("{}\n", encoding="utf-8")
        g(cay, "add", "-A"); g(cay, "commit", "-qm", "policy"); g(cay, "push", "-q", "origin", "feature")
        rc, o, e = _goi_main(mod, "ai-dang-giu", "ops/x.md", "--root", str(cay))
        chot(rc == 0, f"metadata + policy: verdict luật cũ (0): {rc} {e!r}")


@ca
def t135_M3_check_thuan_mac_dinh_va_du_bao_chi_them_dong():
    """M3: `check` KHÔNG chạm git khi không có `--du-bao` (thuần, chạy được không git — t53); `--du-bao` ngoài
    kho ⇒ 12; trong kho: chốt sổ rỗng + dòng DU_BAO, rc giữ nguyên; hàm dự báo in rc dự báo cho thay_the_cho."""
    mod = _nap_cong()
    with San() as s:
        cay, g = _kho_thu(s)
        tep = viet(cay / "ops" / "leases", lease_mau(), "moi.yaml")
        rong = s / "bin-rong"; rong.mkdir()
        mt = dict(os.environ, GITHUB_ACTIONS="true", GITHUB_REPOSITORY="o/r", GITHUB_ACTOR="ducthangho", PATH=str(rong))
        rc, o, e = chay("check", tep, env=mt)
        chot(rc == 0 and "DU_BAO" not in o, f"check thuần (không git trên PATH) phải 0: {rc} {o!r} {e!r}")
        rc, o, e = chay("check", tep, "--du-bao", env=mt)
        chot(rc == 12, f"--du-bao mà không gọi được git phải 12, không được lặng lẽ bỏ dự báo: {rc} {e!r}")
        rc, o, e = _goi_main(mod, "check", str(tep), "--du-bao")
        chot(rc == 0 and "ĐĂNG ĐƯỢC" in o and o.count("DU_BAO:") >= 2, f"--du-bao trong kho sạch: {rc} {o!r} {e!r}")
        # luật cũ QUA (bia mộ hai chiều trên một ref cục bộ) nhưng sổ VẮNG ⇒ dự báo 8 mà rc vẫn 0: chính chỗ mutant
        # "gắn luật mới vào verdict sớm" phải ĐỎ (A3)
        g(cay, "checkout", "-q", "-b", "bia-mo")
        (cay / "ops" / "leases" / "cu-het-han.yaml").write_text(
            f"lease_id: cu-het-han\nlease_expires_at_utc: '{khi_truoc(48)}'\nda_bi_thay_the: moi-thay-the\n", encoding="utf-8")
        g(cay, "add", "-A"); g(cay, "commit", "-qm", "bia mo")
        tep_thay = viet(cay / "ops" / "leases", lease_mau(lease_id="moi-thay-the", thay_the_cho=["cu-het-han"]), "moi-thay-the.yaml")
        rc, o, e = _goi_main(mod, "check", str(tep_thay))
        chot(rc == 0, f"control luật cũ: bia mộ hai chiều phải QUA: {rc} {e!r}")
        rc, o, e = _goi_main(mod, "check", str(tep_thay), "--du-bao")
        chot(rc == 0 and any("cu-het-han" in x and "rc dự báo 8" in x for x in o.splitlines()),
             f"luật mới chỉ được DỰ BÁO (8), verdict giữ 0: {rc} {o!r} {e!r}")
        g(cay, "checkout", "-q", "master")
        # `add -A` trên nhánh bia-mo đã commit cả moi.yaml, checkout master gỡ nó khỏi cây — viết lại
        tep = viet(cay / "ops" / "leases", lease_mau(), "moi.yaml")
        ngoai = viet(s, lease_mau(), "ngoai.yaml")
        rc, o, e = _goi_main(mod, "check", str(ngoai), "--du-bao", "--root", str(s))
        chot(rc == 12 and "kho git" in e, f"--du-bao ngoài kho git phải 12: {rc} {e!r}")
        # hàm dự báo thuần: thay_the_cho vắng sổ ⇒ 'rc dự báo 8'; có trong sổ với cap_lai_cho đúng ⇒ 0; sai ⇒ 8
        dong = mod._du_bao_check({"lease_id": "moi", "thay_the_cho": ["cu-het-han"]}, cay, "master")
        chot(any("cu-het-han" in x and "rc dự báo 8" in x for x in dong), f"thay_the_cho vắng sổ phải dự báo 8: {dong}")
        g(cay, "checkout", "-q", "-b", "so-tren-master")
        (cay / "ops" / "thu-hoi").mkdir()
        (cay / "ops" / "thu-hoi" / "cu-het-han.yaml").write_bytes(_yaml_bytes(_ban_ghi_thu_hoi(lease_id="cu-het-han", cap_lai_cho="moi")))
        g(cay, "add", "-A"); g(cay, "commit", "-qm", "so"); g(cay, "push", "-q", "origin", "so-tren-master:master")
        g(cay, "fetch", "-q", "origin")
        dong = mod._du_bao_check({"lease_id": "moi", "thay_the_cho": ["cu-het-han"]}, cay, "master")
        chot(any("cap_lai_cho='moi'" in x and "rc dự báo 0" in x for x in dong), f"cap_lai_cho khớp phải dự báo 0: {dong}")
        dong = mod._du_bao_check({"lease_id": "khac", "thay_the_cho": ["cu-het-han"]}, cay, "master")
        chot(any("rc dự báo 8" in x for x in dong), f"cap_lai_cho lệch phải dự báo 8: {dong}")
        dong = mod._du_bao_check({"lease_id": "cu-het-han"}, cay, "master")
        chot(any("chiều ngược" in x for x in dong), f"lease đang kiểm có trong sổ ⇒ chiều ngược: {dong}")
        # và consumer vận hành với sổ ấy trên master ⇒ 12 (cờ False) — kể cả qua `check --du-bao`
        rc, o, e = _goi_main(mod, "check", str(tep), "--du-bao")
        chot(rc == 12 and "SO_THU_HOI_KICH_HOAT=False" in e, f"check --du-bao với sổ không rỗng phải 12: {rc} {e!r}")
        rc, o, e = _goi_main(mod, "check", str(tep))
        chot(rc == 0, f"check KHÔNG --du-bao vẫn thuần, không chạm sổ: {rc} {e!r}")


@ca
def t136_A2_adapter_nguon_ghim_danh_tinh_profile_duyet_va_khong_doc_config_kho():
    """A2/ADR-0047: discovery qua endpoint tường minh với env con TỪ RỖNG; profile chưa duyệt ⇒ 12 (mỏ neo A0
    rỗng); symref máy chủ vắng ⇒ 12 không fallback; config kho/global không đổi được nguồn; so map cục bộ."""
    from unittest import mock
    mod = _nap_cong()
    chot(mod.PROFILE_ADAPTER_DA_DUYET == frozenset() and mod.SO_THU_HOI_KICH_HOAT is False
         and mod.KHO_CANONICAL == KHO_CANONICAL_A0, "hằng A0 trôi")
    with San() as s:
        cay, g = _kho_thu(s)
        goc = s / "origin.git"
        subprocess.run(["git", "-C", str(goc), "symbolic-ref", "HEAD", "refs/heads/master"], check=True)
        sha = _g_a0(cay, "rev-parse", "origin/master")
        hoso = mod.hoso_adapter_do()
        digest = mod.bam_ho_so(hoso)
        chot(hoso["git_path"] == mod._git_exe_toi_thieu() and len(digest) == 64, f"hồ sơ adapter: {hoso}")
        ep = f"file://{goc}"
        # production: mỏ neo rỗng ⇒ 12, kể cả endpoint hợp lệ
        rc, td = _ma_chan(mod, mod.kham_pha_nguon, ep, hoso=hoso, giao_thuc_cho_phep=("file",))
        chot(rc == 12 and "CHƯA được duyệt" in td, f"profile chưa duyệt phải 12: {rc} {td}")
        rc, td = _ma_chan(mod, mod.kham_pha_nguon, ep, hoso=hoso, da_duyet=[], giao_thuc_cho_phep=("file",))
        chot(rc == 12, f"mỏ neo rỗng tường minh phải 12: {rc}")
        # fixture duyệt đúng digest ⇒ control xanh
        rc, kq = _ma_chan(mod, mod.kham_pha_nguon, ep, hoso=hoso, da_duyet=[digest], giao_thuc_cho_phep=("file",))
        chot(rc == 0 and kq[0] == "master" and kq[1]["master"] == sha and kq[2] == digest, f"discovery control: {rc} {kq}")
        # hồ sơ TRONG MIỀN nhưng khác bản đã duyệt (đổi proxy) ⇒ digest khác ⇒ 12
        khac = dict(hoso, proxy="http://proxy.noi-bo:3128")
        rc, td = _ma_chan(mod, mod.kham_pha_nguon, ep, hoso=khac, da_duyet=[digest], giao_thuc_cho_phep=("file",))
        chot(rc == 12 and "CHƯA được duyệt" in td, f"hồ sơ khác approved phải 12: {rc} {td}")
        rc, td = _ma_chan(mod, mod.kham_pha_nguon, ep, hoso=dict(hoso, git_path="//khong-co/git"), da_duyet=[digest], giao_thuc_cho_phep=("file",))
        chot(rc == 12 and "không khớp executable" in td, f"git_path lệch phải 12: {rc} {td}")
        # F08: cùng fixture t136; mỏ neo digest không thay validator miền key/type.
        # Giá trị vô hại ở khoá ngoài schema; không helper, không rewrite, không endpoint khác.
        khac = dict(hoso, truong_khong_ho_tro="x")
        rc, td = _ma_chan(mod, mod.kham_pha_nguon, ep, hoso=khac,
                          da_duyet=[mod.bam_ho_so(khac)], giao_thuc_cho_phep=("file",))
        chot(rc == 12, f"profile ngoài miền phải 12 kể cả digest khớp fixture: {rc} {td}")
        # giao thức không cho phép ⇒ 12 (mặc định chỉ https)
        rc, td = _ma_chan(mod, mod.kham_pha_nguon, ep, hoso=hoso, da_duyet=[digest])
        chot(rc == 12 and "discovery rc=" in td, f"file:// dưới allowlist https phải 12: {rc} {td}")
        # config global có insteadOf: git THƯỜNG bị đổi nguồn (fixture có răng), adapter thì KHÔNG
        cfg = s / "gitconfig"
        cfg.write_text(f'[url "file://{s}/khong-ton-tai"]\n\tinsteadOf = file://\n', encoding="utf-8")
        with mock.patch.dict(os.environ, {"GIT_CONFIG_GLOBAL": str(cfg)}):
            p = subprocess.run(["git", "ls-remote", "--heads", ep], capture_output=True, text=True)
            chot(p.returncode != 0, "control: git thường phải bị insteadOf đổi nguồn — fixture không có răng")
            rc, kq = _ma_chan(mod, mod.kham_pha_nguon, ep, hoso=hoso, da_duyet=[digest], giao_thuc_cho_phep=("file",))
            chot(rc == 0 and kq[1]["master"] == sha, f"adapter không được đọc config global: {rc} {kq}")
        # symref máy chủ vắng ⇒ 12, không fallback về tên đoán
        subprocess.run(["git", "-C", str(goc), "symbolic-ref", "HEAD", "refs/heads/khong-co"], check=True)
        rc, td = _ma_chan(mod, mod.kham_pha_nguon, ep, hoso=hoso, da_duyet=[digest], giao_thuc_cho_phep=("file",))
        chot(rc == 12 and "không fallback" in td, f"symref vắng phải 12: {rc} {td}")
        subprocess.run(["git", "-C", str(goc), "symbolic-ref", "HEAD", "refs/heads/master"], check=True)
        # symref CỤC BỘ giả không đổi kết quả (adapter không đọc refs của checkout)
        g(cay, "symbolic-ref", "refs/remotes/origin/HEAD", "refs/remotes/origin/khong-co")
        rc, kq = _ma_chan(mod, mod.kham_pha_nguon, ep, hoso=hoso, da_duyet=[digest], giao_thuc_cho_phep=("file",))
        chot(rc == 0 and kq[0] == "master", f"symref cục bộ giả không được đổi discovery: {rc} {kq}")
        # so map cục bộ: khớp ⇒ dict; SHA lệch ⇒ 12; tên máy chủ thiếu cục bộ ⇒ 12; local heads không bù
        cb = mod.so_map_cuc_bo(cay, {"master": sha})
        chot(cb.get("master") == sha, f"so map khớp: {cb}")
        rc, td = _ma_chan(mod, mod.so_map_cuc_bo, cay, {"master": "0" * 40})
        chot(rc == 12 and "lệch" in td, f"SHA lệch phải 12: {rc} {td}")
        g(cay, "branch", "chi-cuc-bo")
        rc, td = _ma_chan(mod, mod.so_map_cuc_bo, cay, {"master": sha, "chi-cuc-bo": sha})
        chot(rc == 12 and "thiếu" in td, f"tên chỉ có ở heads cục bộ không được bù cho remote-tracking: {rc} {td}")
        # env con từ rỗng: biến nguy hiểm của tiến trình cha không lọt (GIT_DIR trỏ kho khác, GIT_CONFIG_*)
        mt = mod._env_rong("/usr/bin/git", "/tmp/x.git", "/tmp/h")
        chot(set(mt) == {"PATH", "HOME", "GIT_DIR", "GIT_CONFIG_NOSYSTEM", "GIT_CONFIG_GLOBAL", "GIT_TEMPLATE_DIR",
                         "GIT_NO_REPLACE_OBJECTS", "GIT_TERMINAL_PROMPT", "LC_ALL"}
             and mt["GIT_CONFIG_GLOBAL"] == os.devnull and mt["GIT_NO_REPLACE_OBJECTS"] == "1", f"env con: {mt}")


@ca
def t137_M9_workflow_admission_hop_dong_tinh_va_actionlint_shellcheck():
    """M9 (R5/S5): `ops-thu-hoi-admission.yml` — chỉ `pull_request_target` đúng 5 types, base master, KHÔNG
    dispatch/paths; quyền chỉ đọc hai mức; checkout NEO base.sha, không checkout head; PyYAML ghim; bộ kiểm gọi
    `kiem-thu-hoi-github` với S/H/nhánh qua ENV (không `${{ }}` trong thân `run`); artifact receipt
    `thu-hoi-receipt-<H>-<attempt>` `if-no-files-found: error`; actionlint + shellcheck rc=0, THIẾU công cụ ⇒ ĐỎ."""
    import shutil
    import yaml
    if not WORKFLOW_THU_HOI.parent.is_dir():
        chot(not (HERE.parent / ".git").exists(), "kho thật mà không thấy thư mục workflow")
        return
    chot(WORKFLOW_THU_HOI.is_file(), f"không thấy {WORKFLOW_THU_HOI}")
    van = WORKFLOW_THU_HOI.read_text(encoding="utf-8")
    d = yaml.safe_load(van)
    on = d.get("on", d.get(True))
    chot(isinstance(on, dict) and list(on) == ["pull_request_target"], f"on phải CHỈ có pull_request_target: {on}")
    prt = on["pull_request_target"]
    chot(sorted(prt.get("types") or []) == sorted(["opened", "reopened", "synchronize", "ready_for_review", "edited"]),
         f"types sai: {prt.get('types')}")
    chot(prt.get("branches") == ["master"] and "paths" not in prt and "paths-ignore" not in prt, f"branches/paths: {prt}")
    chot(not any("workflow_dispatch" in x for x in van.splitlines() if not x.lstrip().startswith("#")),
         "KHÔNG khai workflow_dispatch trong workflow required (chú thích nhắc tới thì được)")
    chot(d.get("permissions") == {"contents": "read", "pull-requests": "read", "actions": "read"},
         f"permissions mức workflow (chỉ đọc): {d.get('permissions')}")
    jobs = d["jobs"]
    chot(list(jobs) == ["thu-hoi"], f"đúng một job `thu-hoi`: {list(jobs)}")
    job = jobs["thu-hoi"]
    chot(job.get("permissions") == {"contents": "read", "pull-requests": "read", "actions": "read"}, f"permissions mức job: {job.get('permissions')}")
    chot(not any(v == "write" for v in list(d.get("permissions").values()) + list(job.get("permissions").values())), "không quyền ghi nào")
    chot("issues" not in van.split("jobs:")[1].split("steps:")[0], "job kiểm không được có quyền issues")
    steps = job["steps"]
    checkout = [b for b in steps if str(b.get("uses", "")).startswith("actions/checkout@")]
    chot(len(checkout) == 1, f"đúng một checkout: {len(checkout)}")
    w = checkout[0]["with"]
    chot(w.get("ref") == "${{ github.event.pull_request.base.sha }}" and w.get("persist-credentials") is False
         and w.get("fetch-depth") == 0, f"checkout phải neo base.sha, không giữ credential, đủ lịch sử: {w}")
    chot("head.sha }}" not in yaml.safe_dump(w) and all("head.ref" not in str(b.get("with", "")) for b in steps),
         "không bước nào checkout head PR")
    chot(re.search(r"pip\s+install\b[^\n]*\bPyYAML==6\.0\.3\b", van), "PyYAML phải ghim exact 6.0.3 (t31)")
    than = [b["run"] for b in steps if isinstance(b.get("run"), str)]
    chot(len(than) == 2, f"đúng hai bước run (cài + kiểm): {len(than)}")
    kiem = than[1]
    chot("${{" not in kiem, "thân run của bộ kiểm KHÔNG được nội suy biểu thức — input đi qua env")
    chot("kiem-thu-hoi-github" in kiem and "--canonical-base" in kiem and "--nhanh-mac-dinh" in kiem
         and "--receipt" in kiem, "bộ kiểm phải gọi kiem-thu-hoi-github với S/H/nhánh/receipt")
    chot('ops/lease_publish.py kiem-thu-hoi-github "$TL_H"' in kiem, "H phải là đối số đầu, từ env TL_H")
    env = [b.get("env") for b in steps if isinstance(b.get("run"), str)][1]
    chot(env.get("TL_S") == "${{ github.event.pull_request.base.sha }}" and env.get("TL_H") == "${{ github.event.pull_request.head.sha }}"
         and env.get("TL_NHANH") == "${{ github.event.pull_request.base.ref }}", f"env S/H/nhánh: {env}")
    chot('git rev-parse HEAD' in kiem and 'refs/pull/$TL_PR/head' in kiem and 'https://github.com/$TL_KHO' in kiem
         and '"$TL_KHO" = "ducthangho/tra-luat"' in kiem, "phải đo S == HEAD, fetch H từ endpoint canonical tường minh")
    up = [b for b in steps if str(b.get("uses", "")).startswith("actions/upload-artifact@")]
    chot(len(up) == 1, "đúng một bước upload-artifact")
    uw = up[0]["with"]
    chot(uw.get("name") == "thu-hoi-receipt-${{ github.event.pull_request.head.sha }}-${{ github.run_attempt }}"
         and uw.get("if-no-files-found") == "error" and str(uw.get("path", "")).endswith("receipt.json"),
         f"artifact receipt: {uw}")
    chot(not any("git commit" in x or "git push" in x for x in than), "workflow không ghi vào kho")
    # actionlint + shellcheck THẬT, fail-close khi thiếu — "YAML parse được" KHÁC "GitHub nhận"
    al, sc = shutil.which("actionlint"), shutil.which("shellcheck")
    chot(al, "KHÔNG ĐO ĐƯỢC: thiếu `actionlint` (cài: ops/cai_actionlint.sh với AL_VER)")
    chot(sc, "KHÔNG ĐO ĐƯỢC: thiếu `shellcheck` — actionlint IM LẶNG bỏ toàn bộ luật shell khi vắng nó")
    # Packet #504 M4 lần 2+3 (run 34615345948, 34621902478): trên windows-latest, actionlint GỌI shellcheck bên trong
    # trên tệp này TREO (≥ 10 phút 56 s tới lúc job bị huỷ; lần 3 đụng hạn 180 s), trong khi t33 (cùng actionlint +
    # shellcheck, tệp ops-publish-lease.yml) xong trong vài giây, `actionlint -shellcheck=` xong 0,1 s và `shellcheck`
    # gọi thẳng xong 0,1 s — tức treo nằm ở đường actionlint→shellcheck trên Windows với NỘI DUNG tệp này, không ở
    # công cụ nào riêng lẻ. Chữa bằng cách TÁCH HAI PHÉP ĐO cùng tiêu chuẩn: (1) actionlint luật YAML/biểu thức với
    # `-shellcheck=` (tắt đường treo); (2) shellcheck gọi THẲNG trên từng thân `run`, CÙNG bộ mã loại trừ actionlint
    # dùng (SC1091,SC2194,SC2050,SC2154,SC2157,SC2043 — đọc từ chính binary 1.7.7), tệp tạm ghi NHỊ PHÂN LF (ghi text
    # trên Windows sinh CRLF ⇒ SC1017 giả — lần 3 đã dính). Cả hai phải rc=0 — không bớt luật nào; đột biến thân run
    # (vd `echo $TL_S` không nháy) phải làm ca ĐỎ qua (2). Vẫn giữ hạn AL_HAN_GIAY: lần sau có treo thì có tên.
    try:
        p = subprocess.run([al, "-shellcheck=", str(WORKFLOW_THU_HOI)], capture_output=True, text=True, timeout=AL_HAN_GIAY)
    except subprocess.TimeoutExpired:
        chot(False, f"actionlint -shellcheck= KHÔNG XONG trong {AL_HAN_GIAY}s trên {WORKFLOW_THU_HOI.name} — chẩn đoán: "
                    + _chan_doan_actionlint_treo(al, sc, WORKFLOW_THU_HOI, CD_HAN_TONG_GIAY))
    chot(p.returncode == 0, f"actionlint (luật YAML/biểu thức) ĐỎ (rc={p.returncode}):\n{p.stdout}{p.stderr}")
    with tempfile.TemporaryDirectory() as td:
        # MỘT ngân sách cho CẢ vòng shellcheck, không phải hạn mỗi lời gọi: trần của t137 phải độc
        # lập với SỐ thân `run` (dữ liệu), kẻo `AB_HAN_GIAY` dẫn xuất từ nó cũng trôi theo dữ liệu.
        # Phép chia ngân sách nằm ở `_chay_day_lenh_trong_ngan_sach`, và `t156` đo tính độc-lập-với-n.
        mac_dinh = d.get("defaults", {}).get("run", {}).get("shell")
        mac_dinh = job.get("defaults", {}).get("run", {}).get("shell", mac_dinh)
        if not mac_dinh:
            nen_job = job.get("runs-on", "")
            cac_nen = nen_job if isinstance(nen_job, list) else [nen_job]
            mac_dinh = "pwsh" if any(str(n).lower().startswith("windows-") for n in cac_nen) else "bash"
        day = []
        for i, b in enumerate(b for b in steps if isinstance(b.get("run"), str)):
            shell = b.get("shell", mac_dinh).split(maxsplit=1)[0]
            if shell not in ("bash", "sh"):
                continue  # actionlint cũng chỉ chạy shellcheck cho bash/sh
            # actionlint thay biểu thức bằng placeholder; literal đơn có thể chứa dấu đóng.
            x = re.sub(r"\$\{\{(?:'[^']*(?:''[^']*)*'|[^'}]|}(?!}))*}}",
                       lambda m: "_" * len(m.group()), b["run"])
            f = Path(td) / f"run{i}.sh"; f.write_bytes(x.encode("utf-8"))
            day.append((i, [sc, "-s", shell, "-e", SC_LOAI_TRU_NHU_ACTIONLINT, str(f)]))
        ket = []
        try:
            ket = _chay_day_lenh_trong_ngan_sach([l for _, l in day], SC_HAN_TONG_GIAY)
        except subprocess.TimeoutExpired as ex:
            chot(False, f"shellcheck TREO trên thân run #{next((i for i, l in day if l == ex.cmd), '?')}: hết ngân sách TỔNG "
                        f"{SC_HAN_TONG_GIAY}s của cả vòng ({getattr(ex, 'cmd', '')})")
        except HetNganSachDay as ex:
            chot(False, f"vòng shellcheck tiêu hết ngân sách TỔNG {SC_HAN_TONG_GIAY}s tại thân run "
                        f"#{day[ex.chi_so][0]} — chỉ {ex.da_chay}/{len(day)} thân được ĐO; số thân đã đo "
                        f"không được im lặng nhỏ hơn số thân có mặt")
        chot(len(ket) == len(day),
             f"shellcheck chỉ trả {len(ket)}/{len(day)} kết quả — chưa đo đủ thân run")
        for (i, _), q in zip(day, ket):
            chot(q.returncode == 0, f"shellcheck ĐỎ trên thân run #{i} (rc={q.returncode}):\n{q.stdout}{q.stderr}")


class HetNganSachDay(Exception):
    """Dãy lệnh đã tiêu hết NGÂN SÁCH TỔNG trước khi chạy tới lệnh thứ `chi_so`."""

    def __init__(self, chi_so, da_chay, ngan_sach):
        super().__init__(f"hết ngân sách tổng {ngan_sach}s tại lệnh #{chi_so}, đã chạy {da_chay}")
        self.chi_so, self.da_chay, self.ngan_sach = chi_so, da_chay, ngan_sach


def _chay_day_lenh_trong_ngan_sach(cac_lenh, ngan_sach_giay, chay=None):
    """Chạy lần lượt `cac_lenh` trong MỘT ngân sách TỔNG. Hết ngân sách ⇒ `HetNganSachDay`.

    VÌ SAO KHÔNG CẤP LẠI HẠN TỐI THIỂU CHO LỆNH KẾ TIẾP — và đây là chỗ bản vá lượt 3 tự bắt được
    mình khai rộng hơn phép đo: bản đầu viết `timeout=max(1.0, con_lai)`, nên khi ngân sách đã cạn,
    mỗi lệnh còn lại vẫn được cấp 1 s ⇒ trần của cả vòng là `ngân sách + n×1 s`, tức LẠI trôi theo
    SỐ lệnh — đúng thứ phụ thuộc dữ liệu mà ngân sách TỔNG sinh ra để cắt, trong khi chú thích ngay
    trên nó đã khẳng định là đã cắt. Nay hết là DỪNG, nên trần của cả dãy độc lập với `n`, và `t156`
    đo đúng tính chất ấy bằng hai dãy dài khác nhau trên cùng một ngân sách.
    """
    chay = subprocess.run if chay is None else chay
    het = time.monotonic() + ngan_sach_giay
    ket = []
    for i, lenh in enumerate(cac_lenh):
        con_lai = het - time.monotonic()
        if con_lai <= 0:
            raise HetNganSachDay(i, len(ket), ngan_sach_giay)
        ket.append(chay(lenh, capture_output=True, text=True, timeout=con_lai))
    return ket


def _chan_doan_actionlint_treo(al: str, sc: str, wf, han_tong: float = None) -> str:
    """Đo từng công cụ riêng, mỗi cái có hạn ngắn, trả một dòng: cái nào xong/rc/giây, cái nào TREO.

    `han_tong` là trần cho TOÀN BỘ chẩn đoán. Không có nó thì chi phí chẩn đoán trôi theo SỐ thân
    `run` (30 + 30 + 60×n + 60) và cộng vào t137 đúng lúc t137 đã quá hạn — tức trần ngoài của t125
    không còn tính được. Probe nào hết ngân sách thì ghi thẳng `BỎ ĐO`, KHÔNG im lặng bỏ qua: "ca có
    MẶT khác ca có ĐO", và một dòng chẩn đoán thiếu probe mà không khai là một lời khai rộng hơn
    phép đo.
    """
    import yaml
    ket = []
    het = time.monotonic() + (CD_HAN_TONG_GIAY if han_tong is None else han_tong)
    def do(nhan, lenh, han):
        con_lai = het - time.monotonic()
        if con_lai <= 1:
            ket.append(f"{nhan}: BỎ ĐO (hết ngân sách chẩn đoán)")
            return
        han = min(han, con_lai)
        t0 = time.monotonic()
        try:
            q = subprocess.run(lenh, capture_output=True, text=True, timeout=han)
            ket.append(f"{nhan}: rc={q.returncode} {time.monotonic() - t0:.1f}s out={q.stdout.strip()[:60]!r} err={q.stderr.strip()[:80]!r}")
        except subprocess.TimeoutExpired:
            ket.append(f"{nhan}: TREO >{han}s")
        except OSError as ex:
            ket.append(f"{nhan}: OSError {ex}")
    do("actionlint -version", [al, "-version"], 30)
    do("shellcheck --version", [sc, "--version"], 30)
    than = [b["run"] for b in yaml.safe_load(wf.read_text(encoding="utf-8"))["jobs"]["thu-hoi"]["steps"] if isinstance(b.get("run"), str)]
    with tempfile.TemporaryDirectory() as td:
        for i, x in enumerate(than):
            f = Path(td) / f"run{i}.sh"; f.write_bytes(x.encode("utf-8"))   # nhị phân: text mode trên Windows sinh CRLF ⇒ SC1017 giả
            do(f"shellcheck -s bash run{i}", [sc, "-s", "bash", "-e", SC_LOAI_TRU_NHU_ACTIONLINT, str(f)], 60)
        # actionlint KHÔNG shellcheck: nếu xong ⇒ thứ treo là đường actionlint→shellcheck, không phải parser YAML
        do("actionlint -shellcheck=", [al, "-shellcheck=", str(wf)], 60)
    return " | ".join(ket)


@ca
def t138_A12_bien_nhan_receipt_du_truong_va_neo_doc_lap_cay_PR():
    """A12: receipt M4 có đủ trường hợp đồng (S/H/T/tree_S/OID bộ kiểm/profile/discovery/ngân sách/kết luận) và
    JSON ổn định (sort_keys); T và OID bộ kiểm đối chiếu bằng git ĐỘC LẬP với reader."""
    import json
    mod = _nap_cong()
    with San() as s:
        cay, (c0, c1, S) = _kho_do_thi(s)
        H = _them_commit(cay, "h", S, {"docs/b.md": b"b\n"})
        rcp = s / "r.json"
        rc, o, e = _goi_main(mod, "kiem-thu-hoi-github", H, "--canonical-base", S, "--nhanh-mac-dinh", "master",
                             "--root", str(cay), "--receipt", str(rcp))
        chot(rc == 0, f"{rc} {e!r}")
        van = rcp.read_text(encoding="utf-8")
        d = json.loads(van)
        bat_buoc = {"schema_version", "event", "che_do", "kho_canonical", "nhanh_mac_dinh", "S", "H", "T", "tree_S",
                    "canh_ancestry", "so_thu_hoi_S", "so_thu_hoi_T", "metadata_T", "thu_hoi_moi", "oid_bo_kiem_tai_S",
                    "profile_digest", "discovery", "ngan_sach", "so_object_da_doc", "tong_bytes", "ket_luan", "thoi_diem_utc"}
        chot(bat_buoc <= set(d), f"receipt thiếu trường: {bat_buoc - set(d)}")
        chot(list(d) == sorted(d), "receipt phải sort_keys để băm ổn định")
        chot(d["T"] == _g_a0(cay, "rev-parse", f"{H}^{{tree}}") and d["tree_S"] == _g_a0(cay, "rev-parse", f"{S}^{{tree}}")
             and d["oid_bo_kiem_tai_S"] == _g_a0(cay, "rev-parse", f"{S}:ops/lease_publish.py"), "T/tree_S/OID bộ kiểm lệch git")
        chot(d["so_object_da_doc"] >= 4 and d["tong_bytes"] > 0 and d["event"] == "thu_hoi_admission_receipt", f"đếm reader: {d}")
        chot(all(isinstance(v, (int, float)) for v in d["ngan_sach"].values()) and len(d["ngan_sach"]) == 8, "ngân sách 8 trần có đơn vị số")


@ca
def t139_A12_catalog_mutant_A0_giet_dung_ly_do_va_ghi_SONG_kem_seam():
    """Catalog mutant A0: mỗi mutant đúng MỘT chốt, ca đích phải chết bằng `TinHieuChotCa` (không nhận tín dụng
    giả từ lỗi vô can); mutant SỐNG được ghi SỐNG kèm seam/chốt che, không nhận công. Mẫu số cố định."""
    import importlib
    import importlib.util
    nguon = SCRIPT.read_text(encoding="utf-8")
    muts = [
        # (tên, cũ, mới, ca đích, kỳ vọng, seam/chốt che)
        ("S7-noi-allowlist-metadata", "    if duong == PATH_NGOAI_LE_RETIRED:\n        return \"metadata\"",
         "    if duong.startswith(THU_MUC_SO + \"/_\"):\n        return \"metadata\"",
         t128_S7_dinh_tuyen_metadata_dung_MOT_path_va_schema_retired, "GIET", "phan_tuyen_so"),
        ("M1-noi-allowlist-thu-hoi-boi", "    if nguoi_s not in NGUOI_CO_THAM_QUYEN:\n        raise Chan(RC_TU_CAP, f\"{duong}: thu_hoi_boi",
         "    if nguoi_s not in NGUOI_CO_THAM_QUYEN + (\"nguoi-la\",):\n        raise Chan(RC_TU_CAP, f\"{duong}: thu_hoi_boi",
         t127_A7_M1_ma_tran_ban_ghi_thu_hoi_thu_tu_loi_12_4_8, "GIET", "kiem_ban_ghi_thu_hoi — danh sách CHO PHÉP"),
        # SỐNG có chủ đích: bỏ chốt PROVIDERS — allowlist NGUOI_CO_THAM_QUYEN ngay dưới vẫn trả 4 cho tên provider
        # (chốt che); chốt PROVIDERS chỉ cho THÔNG ĐIỆP rõ hơn. Không nhận công.
        ("M1-bo-chot-PROVIDERS-SONG", "    if nguoi_s in PROVIDERS:\n        raise Chan(RC_TU_CAP",
         "    if False:\n        raise Chan(RC_TU_CAP", t127_A7_M1_ma_tran_ban_ghi_thu_hoi_thu_tu_loi_12_4_8, "SONG", "che bởi allowlist NGUOI_CO_THAM_QUYEN"),
        ("S2-bo-bam-lai", "        if bam != oid:\n", "        if False:\n",
         t130_S2_seam_bytes_lech_OID_12_va_parser_KHONG_nhan_byte, "GIET", "KhoObject.doc sau seam"),
        ("S2-bo-so-type", "        if loai_that != loai_mong_doi:\n", "        if False:\n",
         t129_Q45_reader_object_store_bam_lai_va_canh_tu_bytes, "GIET", "KhoObject.doc"),
        ("S8-bo-tran-parent", "                if sau + 1 > gioi_han:\n", "                if False:\n",
         t131_S8_tam_tran_bound_tru_1_bound_bound_cong_1_va_deadline, "GIET", "KhoObject.to_tien"),
        ("S8-bo-deadline", "        if con <= 0:\n", "        if False:\n",
         t131_S8_tam_tran_bound_tru_1_bound_bound_cong_1_va_deadline, "GIET", "KhoObject._con_thoi_gian"),
        ("S8-bo-tran-tree-edges", "            if buoc > self.ngan_sach[\"max_tree_or_alias_edges\"]:\n", "            if False:\n",
         t131_S8_tam_tran_bound_tru_1_bound_bound_cong_1_va_deadline, "GIET", "KhoObject.tim"),
        ("shallow-bo-chot", "        if self._git_nguon(goc_kho, \"rev-parse\", \"--is-shallow-repository\").strip() == \"true\":\n",
         "        if False:\n", t132_shallow_va_object_thieu_la_12_khong_phai_vang, "GIET", "KhoObject.__init__"),
        ("M4-gan-luat-moi-som", "        if not SO_THU_HOI_KICH_HOAT and (thu_hoi_S or thu_hoi_T):\n", "        if False:\n",
         t133_M4_kiem_thu_hoi_github_receipt_append_only_va_che_do_chua_kich_hoat, "GIET", "lenh_kiem_thu_hoi_github"),
        ("M4-bo-append-only", "            if map_T.get(duong) != bo:\n", "            if False:\n",
         t133_M4_kiem_thu_hoi_github_receipt_append_only_va_che_do_chua_kich_hoat, "GIET", "lenh_kiem_thu_hoi_github"),
        ("M4-bo-policy-Q13", "                if policy_T is None:\n", "                if False:\n",
         t133_M4_kiem_thu_hoi_github_receipt_append_only_va_che_do_chua_kich_hoat, "GIET", "lenh_kiem_thu_hoi_github"),
        ("M2-bo-chot-so-rong", "        if muc[\"tuyen\"] == \"thu_hoi\":\n            raise Chan(RC_KHONG_XAC_DINH,\n                       f\"KHÔNG_XÁC_ĐỊNH: SO_THU_HOI_KICH_HOAT=False",
         "        if False:\n            raise Chan(RC_KHONG_XAC_DINH,\n                       f\"KHÔNG_XÁC_ĐỊNH: SO_THU_HOI_KICH_HOAT=False",
         t134_M2_ai_dang_giu_so_khong_rong_khi_co_False_la_12_va_du_bao_khong_doi_rc, "GIET", "_kiem_so_rong_khi_chua_kich_hoat"),
        ("M3-du-bao-doi-rc", "        for dong in _du_bao_check(lease, goc_check, getattr(a, \"nhanh_mac_dinh\", None) or \"master\"):\n            print(dong)\n",
         "        for dong in _du_bao_check(lease, goc_check, getattr(a, \"nhanh_mac_dinh\", None) or \"master\"):\n            print(dong)\n            if \"rc dự báo 8\" in dong or \"chiều ngược\" in dong: raise Chan(RC_NOI_DUNG, dong)\n",
         t135_M3_check_thuan_mac_dinh_va_du_bao_chi_them_dong, "GIET", "lenh_check"),
        ("A2-bo-so-profile", "    if digest not in neo:\n", "    if False:\n",
         t136_A2_adapter_nguon_ghim_danh_tinh_profile_duyet_va_khong_doc_config_kho, "GIET", "kham_pha_nguon"),
        ("A2-fallback-symref", "    if not mac_dinh or mac_dinh not in quang_ba:\n", "    if not quang_ba:\n        mac_dinh = 'master'\n    if False:\n",
         t136_A2_adapter_nguon_ghim_danh_tinh_profile_duyet_va_khong_doc_config_kho, "GIET", "kham_pha_nguon"),
        # SỐNG có chủ đích (A6): bỏ no-replace ở env — repo tạm KHÔNG có refs/replace nên chốt `_repo_tam_co_lap`
        # (GIT_DIR cô lập) che hoàn toàn; không có detector presence riêng, ghi SỐNG, không nhận công.
        ("A6-bo-GIT_NO_REPLACE-SONG", "        \"GIT_NO_REPLACE_OBJECTS\": \"1\",\n", "",
         t129_Q45_reader_object_store_bam_lai_va_canh_tu_bytes, "SONG", "che bởi GIT_DIR tạm không ref (_repo_tam_co_lap)"),
        # --- bổ sung sau cross-review lượt 1 (F01–F09) ---
        ("A6-bo-routing", "                             GIT_OBJECT_DIRECTORY=self.object_dir,\n", "",
         t129_Q45_reader_object_store_bam_lai_va_canh_tu_bytes, "GIET", "KhoObject.__init__ env — positive control bọc _ma_chan"),
        # SỐNG có chủ đích: bỏ chốt "descriptor chưa ghim" — phép so `descriptor_sha256 != DESCRIPTOR_Q13_SHA256` ngay
        # dưới vẫn trả 12 khi mỏ neo là None (không marker nào khớp None); chốt trên chỉ cho THÔNG ĐIỆP rõ hơn.
        ("F01-bo-descriptor-ghim-SONG", "                    if DESCRIPTOR_Q13_SHA256 is None:\n", "                    if False:\n",
         t133_M4_kiem_thu_hoi_github_receipt_append_only_va_che_do_chua_kich_hoat, "SONG", "che bởi phép so descriptor_sha256 với mỏ neo"),
        ("F01-bo-so-base", "                    if d_meta[\"base_sha_before_add\"] != S:\n", "                    if False:\n",
         t133_M4_kiem_thu_hoi_github_receipt_append_only_va_che_do_chua_kich_hoat, "GIET", "lenh_kiem_thu_hoi_github Q13"),
        ("F01-bo-so-hash-policy", "                    if d_meta[\"first_policy_sha256\"] != policy_T[1]:\n", "                    if False:\n",
         t133_M4_kiem_thu_hoi_github_receipt_append_only_va_che_do_chua_kich_hoat, "GIET", "lenh_kiem_thu_hoi_github Q13"),
        # t140 (policy hỏng + marker MỚI) KHÔNG cô lập được chốt này — binding descriptor che; ca cô lập là
        # "marker CŨ + policy T hỏng" trong t133.
        ("F01-bo-policy-JSON", "            if _doc_policy_json(bytes_p) is None:\n", "            if False:\n",
         t133_M4_kiem_thu_hoi_github_receipt_append_only_va_che_do_chua_kich_hoat, "GIET", "lenh_kiem_thu_hoi_github policy (marker cũ)"),
        ("F01-bo-thieu-marker", "        if policy_T is not None and not metadata_T:\n", "        if False:\n",
         t133_M4_kiem_thu_hoi_github_receipt_append_only_va_che_do_chua_kich_hoat, "GIET", "lenh_kiem_thu_hoi_github Q13"),
        ("F02-bo-z", "        p = GOI_GIT(\"ls-tree\", \"-r\", \"-z\", ref, \"--\", thu_muc, cwd=goc)\n", "        p = GOI_GIT(\"ls-tree\", \"-r\", ref, \"--\", thu_muc, cwd=goc); p.stdout = p.stdout.replace(chr(10), chr(0))\n",
         t141_review_F02_ten_tieng_Viet_khong_duoc_bien_so_thanh_rong, "GIET", "_ls_tree_z"),
        ("F02-namespace-khong-thu-muc", "            if duong == THU_MUC_SO:\n", "            if False:\n",
         t142_review_F02_namespace_sai_type_khong_phai_vang, "GIET", "_quet_so_thu_hoi_moi_ref"),
        ("F03-cho-phep-slash", "            if not ten or ten in (\".\", \"..\") or \"/\" in ten or \".git\" == ten or ten in da_thay:\n",
         "            if not ten or ten in (\".\", \"..\") or \".git\" == ten or ten in da_thay:\n",
         t143_review_F03_tree_entry_co_slash_phai_12, "GIET", "KhoObject.tree"),
        ("F04-bo-deadline-memo", "        self._con_thoi_gian(f\"memo {oid[:12]}\")\n", "",
         t144_review_F04_deadline_ap_cho_memo_va_luc_hoan_tat, "GIET", "KhoObject.doc cache-hit"),
        ("F04-bo-deadline-truoc-tra", "            self._con_thoi_gian(f\"trước khi trả {oid[:12]}\")\n", "",
         t144_review_F04_deadline_ap_cho_memo_va_luc_hoan_tat, "GIET", "KhoObject.doc sau wait"),
        ("F05-bo-tong-tu-header", "                    if tong_truoc + kich > self.ngan_sach[\"max_total_object_bytes\"]:\n", "                    if False:\n",
         t146_review_F05_total_budget_truoc_doc_body_va_rc_cat_file, "GIET", "KhoObject.doc header"),
        ("F05-bo-rc-cat-file", "            if rc != 0:\n                raise Chan(RC_KHONG_XAC_DINH, f\"KHÔNG_XÁC_ĐỊNH: cat-file rc={rc}", "            if False:\n                raise Chan(RC_KHONG_XAC_DINH, f\"KHÔNG_XÁC_ĐỊNH: cat-file rc={rc}",
         t146_review_F05_total_budget_truoc_doc_body_va_rc_cat_file, "GIET", "KhoObject.doc rc"),
        ("F06-schema-isinstance", "    if type(sv) is not int or sv != 1:   # `1.0`/`True`", "    if isinstance(sv, bool) or sv != 1:   # `1.0`/`True`",
         t147_review_F06_schema_version_la_integer_va_ngay_hop_le, "GIET", "kiem_ban_ghi_thu_hoi"),
        ("F08-bo-validator-mien", "    kiem_mien_ho_so(hoso)                       # F08: miền TRƯỚC, digest SAU\n", "",
         t136_A2_adapter_nguon_ghim_danh_tinh_profile_duyet_va_khong_doc_config_kho, "GIET", "kham_pha_nguon"),
        ("F09-preflight-env-cha", "        if self._git_nguon(goc_kho, \"rev-parse\", \"--is-shallow-repository\").strip() == \"true\":\n",
         "        if _git(goc_kho, \"rev-parse\", \"--is-shallow-repository\").strip() == \"true\":\n",
         t149_review_F09_preflight_object_store_khong_ke_thua_env, "GIET", "KhoObject.__init__ preflight"),
        # --- bổ sung sau Codex connector review trên 457affd (C1 P1, C2 P2, C3 P2) ---
        ("C1-tim-to-tien-non-tree-la-vang", "                raise Chan(RC_KHONG_XAC_DINH,\n                           f\"KHÔNG_XÁC_ĐỊNH: tổ tiên của {duong} không phải thư mục (mode {mode} {loai}) — không suy vắng\")\n",
         "                return None\n", t151_review_codex_to_tien_non_tree_metadata_rac_va_khoa_lan_kieu, "GIET", "KhoObject.tim"),
        ("C1-consumer-bo-kiem-to-tien", "        _kiem_to_tien_la_tree(goc, ten_ref, THU_MUC_SO)\n", "",
         t151_review_codex_to_tien_non_tree_metadata_rac_va_khoa_lan_kieu, "GIET", "_quet_so_thu_hoi_moi_ref"),
        ("C2-consumer-bo-validate-marker", "            kiem_metadata_retired(muc[\"path\"], muc[\"mode\"], muc[\"type\"],\n                                  _doc_blob_text_12(goc, muc[\"ref\"], muc[\"path\"]) or b\"\")\n", "",
         t151_review_codex_to_tien_non_tree_metadata_rac_va_khoa_lan_kieu, "GIET", "_kiem_so_rong_khi_chua_kich_hoat metadata"),
        ("C3-sorted-khong-key", "khoá thừa {sorted(thua, key=repr)}", "khoá thừa {sorted(thua)}",
         t151_review_codex_to_tien_non_tree_metadata_rac_va_khoa_lan_kieu, "GIET", "kiem_ban_ghi_thu_hoi"),
    ]
    ket = {"GIET": 0, "SONG": 0, "TIN_DUNG_GIA": [], "SAI_KY_VONG": []}
    with San() as s:
        sys.dont_write_bytecode = True
        for i, (ten, cu, moi, dich, ky_vong, seam) in enumerate(muts):
            chot(nguon.count(cu) == 1, f"neo mutant {ten} không duy nhất ({nguon.count(cu)})")
            p = s / f"lease_publish_a0_mut_{i}.py"
            p.write_text(nguon.replace(cu, moi), encoding="utf-8")
            importlib.invalidate_caches()
            spec = importlib.util.spec_from_file_location(f"lp_a0_m{i}", p)
            mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
            cu_nap = globals()["_nap_cong"]; globals()["_nap_cong"] = lambda m=mod: m
            try:
                try:
                    dich()
                    thuc = "SONG"
                except TinHieuChotCa:
                    thuc = "GIET"
                except Exception as ex:  # noqa: BLE001 — chết vì lỗi VÔ CAN: không nhận công
                    thuc = "TIN_DUNG_GIA"
                    ket["TIN_DUNG_GIA"].append(f"{ten}: {type(ex).__name__}: {str(ex)[:120]}")
            finally:
                globals()["_nap_cong"] = cu_nap
            if thuc in ("GIET", "SONG"):
                ket[thuc] += 1
            if thuc != ky_vong:
                ket["SAI_KY_VONG"].append(f"{ten}: kỳ vọng {ky_vong}, thực {thuc} (seam: {seam})")
    print(f"catalog mutant A0: mẫu số={len(muts)}, giết thật={ket['GIET']}, SỐNG có chủ đích={ket['SONG']}, "
          f"tín dụng giả={len(ket['TIN_DUNG_GIA'])}")
    chot(not ket["TIN_DUNG_GIA"], f"mutant chết vì lỗi VÔ CAN (tín dụng giả): {ket['TIN_DUNG_GIA']}")
    chot(not ket["SAI_KY_VONG"], f"catalog lệch: {ket['SAI_KY_VONG']}")
    chot(ket["GIET"] + ket["SONG"] == len(muts) == 37, f"mẫu số phải cố định 37: {ket}")
    chot(ket["GIET"] == 34 and ket["SONG"] == 3, f"catalog kỳ vọng 34 giết / 3 SỐNG: {ket}")


# wp488 review lượt 1: regression hints; fixture/control local, không mạng.
# Các ca này được chạy trên bản sao; executor tái dẫn xuất bản sửa sản phẩm.

@ca
def t140_review_F01_Q13_policy_hong_va_binding_sai_phai_12():
    mod = _nap_cong()
    with San() as s:
        cay, (_, _, S) = _kho_do_thi(s)
        P, R = mod.PATH_POLICY_CLOSURE, mod.PATH_NGOAI_LE_RETIRED
        H = _them_commit(cay, "q13-hong", S, {
            P: b"not JSON\n", R: _yaml_bytes(_metadata_retired())})
        receipt = s / "receipt.json"
        rc, o, e = _goi_main(mod, "kiem-thu-hoi-github", H, "--canonical-base", S,
                             "--nhanh-mac-dinh", "master", "--root", cay, "--receipt", receipt)
        chot(rc == 12 and not receipt.exists(),
             f"Q13 policy không parse được + binding chưa xác minh phải 12, không receipt: {rc} {o!r} {e!r}")


@ca
def t141_review_F02_ten_tieng_Viet_khong_duoc_bien_so_thanh_rong():
    mod = _nap_cong()
    with San() as s:
        cay, g = _kho_thu(s)
        tep = viet(cay / "ops" / "leases", lease_mau(), "moi.yaml")
        g(cay, "checkout", "-q", "-b", "ten-tieng-viet")
        p = cay / "ops" / "thu-hoi" / "thu hồi.yaml"
        p.parent.mkdir(parents=True); p.write_text("x: 1\n", encoding="utf-8")
        g(cay, "add", "-A"); g(cay, "commit", "-qm", "ten tieng Viet")
        g(cay, "push", "-q", "origin", "ten-tieng-viet")
        for argv in (("ai-dang-giu", "ops/x.md", "--root", cay),
                     ("ai-dang-giu", "ops/x.md", "--root", cay, "--du-bao"),
                     ("check", tep, "--root", cay, "--du-bao")):
            rc, o, e = _goi_main(mod, *argv)
            chot(rc == 12, f"sổ không rỗng với tên Unicode thường phải 12: {argv}: {rc} {o!r} {e!r}")
        rc, _, e = _goi_main(mod, "check", tep, "--root", cay)
        chot(rc == 0, f"check mặc định giữ luật cũ, thuần: {rc} {e!r}")


@ca
def t142_review_F02_namespace_sai_type_khong_phai_vang():
    mod = _nap_cong()
    for kind in ("file", "gitlink"):
        with San() as s:
            cay, g = _kho_thu(s)
            S = _g_a0(cay, "rev-parse", "HEAD")
            g(cay, "checkout", "-q", "-b", "namespace-" + kind)
            if kind == "file":
                (cay / "ops" / "thu-hoi").write_text("x\n", encoding="utf-8")
                g(cay, "add", "-A")
            else:
                g(cay, "update-index", "--add", "--cacheinfo", "160000," + S + ",ops/thu-hoi")
            g(cay, "commit", "-qm", "namespace " + kind)
            g(cay, "push", "-q", "origin", "namespace-" + kind)
            rc, o, e = _goi_main(mod, "ai-dang-giu", "ops/x.md", "--root", cay)
            chot(rc == 12, f"namespace {kind} phải 12, không được suy rỗng: {rc} {o!r} {e!r}")


@ca
def t143_review_F03_tree_entry_co_slash_phai_12():
    mod = _nap_cong()
    with San() as s:
        cay, (_, _, S) = _kho_do_thi(s)
        blob = _g_a0(cay, "rev-parse", S + ":README.md")
        # Object băm trung thực. Tên entry chứa '/' là ca được giao; không có traversal.
        def tree_object(body):
            p = subprocess.run(["git", "-C", str(cay), "hash-object", "-w", "--literally", "-t", "tree", "--stdin"],
                               input=body, capture_output=True, check=True)
            return p.stdout.decode("ascii").strip()
        ops = tree_object(b"100644 thu-hoi/x.yaml\0" + bytes.fromhex(blob))
        root = tree_object(b"40000 ops\0" + bytes.fromhex(ops))
        H = _g_a0(cay, "commit-tree", root, "-p", S, "-m", "entry slash")
        rc, o, e = _goi_main(mod, "kiem-thu-hoi-github", H, "--canonical-base", S,
                             "--nhanh-mac-dinh", "master", "--root", cay)
        chot(rc == 12, f"entry tree không hợp lệ phải 12 trước suy sổ vắng: {rc} {o!r} {e!r}")


@ca
def t144_review_F04_deadline_ap_cho_memo_va_luc_hoan_tat():
    from unittest import mock
    mod = _nap_cong()
    with San() as s:
        cay, (_, _, H) = _kho_do_thi(s)
        oid = _g_a0(cay, "rev-parse", H + ":README.md")
        clock = [100.0]
        kho = mod.KhoObject(cay, bay_gio=lambda: clock[0], deadline=101.0)
        try:
            chot(kho.doc(oid, "blob") == b"nen\n", "control reader trước deadline")
            clock[0] = 102.0
            rc, td = _ma_chan(mod, kho.doc, oid, "blob")
            chot(rc == 12, f"memo không được bỏ deadline của snapshot: {rc} {td!r}")
        finally:
            kho.dong()
        clock[0] = 100.0
        kho = mod.KhoObject(cay, bay_gio=lambda: clock[0], deadline=101.0)
        popen = mod.subprocess.Popen
        def theo_doi(*a, **kw):
            p = popen(*a, **kw); poll, wait = p.poll, p.wait
            def poll_sau(*a, **kw):
                rc = poll(*a, **kw)
                if rc is not None:
                    clock[0] = 102.0
                return rc
            def wait_sau(*a, **kw):
                rc = wait(*a, **kw); clock[0] = 102.0
                return rc
            p.poll, p.wait = poll_sau, wait_sau
            return p
        try:
            with mock.patch.object(mod.subprocess, "Popen", theo_doi):
                rc, td = _ma_chan(mod, kho.doc, oid, "blob")
            chot(rc == 12, f"cat-file thật hoàn tất sau deadline phải 12: {rc} {td!r}")
        finally:
            kho.dong()


@ca
def t145_review_F05_object_lon_phai_12_va_thu_hoi_cat_file():
    from unittest import mock
    mod = _nap_cong()
    with San() as s:
        cay, (_, _, _) = _kho_do_thi(s)
        (cay / "large.bin").write_bytes(b"a" * 1048576)
        _g_a0(cay, "add", "-A"); _g_a0(cay, "commit", "-qm", "large")
        oid = _g_a0(cay, "rev-parse", "HEAD:large.bin")
        kho = mod.KhoObject(cay, ngan_sach={"max_object_bytes": 100, "max_reader_wall_seconds": 0.3})
        popen, children = mod.subprocess.Popen, []
        def theo_doi(*a, **kw):
            p = popen(*a, **kw); children.append(p)
            return p
        rc, td, timeout, alive = None, None, False, []
        try:
            with mock.patch.object(mod.subprocess, "Popen", theo_doi):
                try:
                    rc, td = _ma_chan(mod, kho.doc, oid, "blob")
                except subprocess.TimeoutExpired:
                    # Đây chính là lỗi lifecycle đang đo; không nhận công trong catalog mutant.
                    timeout = True
            alive = [p.poll() is None for p in children]
        finally:
            for p in children:
                if p.poll() is None:
                    p.kill(); p.wait(timeout=2)
            kho.dong()
        chot(not timeout and rc == 12 and not any(alive),
             f"object vượt trần phải 12 và đã thu hồi tiến trình: timeout={timeout}, rc={rc}, sống={alive}, {td}")


@ca
def t146_review_F05_total_budget_truoc_doc_body_va_rc_cat_file():
    from unittest import mock
    mod = _nap_cong()
    with San() as s:
        cay, (_, _, H) = _kho_do_thi(s)
        oid = _g_a0(cay, "rev-parse", H + ":README.md")
        kho = mod.KhoObject(cay, ngan_sach={"max_total_object_bytes": 1})
        reads, popen = [], mod.subprocess.Popen
        class TheoDoiDoc:
            def __init__(self, real):
                self.real = real
            def readline(self, *a):
                return self.real.readline(*a)
            def read(self, n):
                reads.append(n)
                return self.real.read(n)
            def __getattr__(self, name):
                return getattr(self.real, name)
        def theo_doi(*a, **kw):
            p = popen(*a, **kw); p.stdout = TheoDoiDoc(p.stdout)
            return p
        try:
            with mock.patch.object(mod.subprocess, "Popen", theo_doi):
                rc, td = _ma_chan(mod, kho.doc, oid, "blob")
            chot(rc == 12 and not reads, f"total byte budget phải chặn trước body: {rc}, reads={reads}, {td}")
        finally:
            kho.dong()
        # Không thay bytes hoặc nguồn. Tiêm riêng trạng thái kết thúc tiến trình.
        kho = mod.KhoObject(cay)
        def rc_khac_khong(*a, **kw):
            p = popen(*a, **kw); poll, wait = p.poll, p.wait
            def poll_sau(*a, **kw):
                rc = poll(*a, **kw)
                if rc is not None:
                    p.returncode = 1
                    return 1
                return rc
            def wait_sau(*a, **kw):
                wait(*a, **kw); p.returncode = 1
                return 1
            p.poll, p.wait = poll_sau, wait_sau
            return p
        try:
            with mock.patch.object(mod.subprocess, "Popen", rc_khac_khong):
                rc, td = _ma_chan(mod, kho.doc, oid, "blob")
            chot(rc == 12, f"cat-file rc!=0 phải 12 dù bytes đã băm đúng: {rc} {td!r}")
        finally:
            kho.dong()


@ca
def t147_review_F06_schema_version_la_integer_va_ngay_hop_le():
    mod = _nap_cong()
    P = "ops/thu-hoi/wp1-exec-1-codex-20260901.yaml"
    rc, td = _ma_chan(mod, mod.kiem_ban_ghi_thu_hoi, P, "100644", "blob",
                      _yaml_bytes(_ban_ghi_thu_hoi(schema_version=1.0)))
    chot(rc == 8, f"schema_version float trong revocation phải 8: {rc} {td}")
    rc, td = _ma_chan(mod, mod.kiem_metadata_retired, mod.PATH_NGOAI_LE_RETIRED, "100644", "blob",
                      _yaml_bytes(_metadata_retired(schema_version=1.0)))
    chot(rc == 12, f"schema_version float trong metadata phải 12: {rc} {td}")
    # CLI thật: ngày sai phải mã hợp đồng, không traceback/rc=1.
    with San() as s:
        cay, (_, _, S) = _kho_do_thi(s)
        for name, files, expected in (
            ("date-revoke", {P: _yaml_bytes(_ban_ghi_thu_hoi(thu_hoi_luc_utc="2026-02-30T00:00:00Z"))}, 8),
            ("date-meta", {mod.PATH_NGOAI_LE_RETIRED: _yaml_bytes(_metadata_retired(retired_at_utc="2026-02-30T00:00:00Z"))}, 12),
        ):
            H = _them_commit(cay, name, S, files)
            rc, o, e = chay("kiem-thu-hoi-github", H, "--canonical-base", S,
                            "--nhanh-mac-dinh", "master", "--root", cay)
            chot(rc == expected and "Traceback" not in e, f"ngày hỏng {name}: đợi {expected}, được {rc}: {o!r} {e!r}")


@ca
def t148_review_F07_M9_definition_receipt_va_commit_pin():
    import yaml
    van = WORKFLOW_THU_HOI.read_text(encoding="utf-8")
    d = yaml.safe_load(van)
    steps = d["jobs"]["thu-hoi"]["steps"]
    env = {k: v for step in steps for k, v in (step.get("env") or {}).items()}
    # M9 đòi identity riêng của definition; checkout S không chứng minh workflow đã chạy tại S.
    chot("${{ github.workflow_sha }}" in env.values() and "${{ github.workflow_ref }}" in env.values(),
         "M9 phải nhận actual workflow_sha/workflow_ref độc lập với base.sha và checkout")
    scripts = "\n".join(step.get("run", "") for step in steps)
    chot("workflow_definition_sha256" in scripts and "workflow_definition_commit" in scripts,
         "receipt phải ghi actual definition commit + blob sha256; thống nhất tên trường với consumer dependency")
    chot("check_run_id" in scripts and "checker_rc" in scripts,
         "receipt thiếu check_run_id/checker_rc của M9; facts phải đến từ nguồn đã xác minh")
    uploads = [step["uses"] for step in steps if str(step.get("uses", "")).startswith("actions/upload-artifact@")]
    # Hint gốc đòi ghim commit 40-hex. CHƯA làm ở A0: phiên này không readback được SHA của actions/upload-artifact
    # (MCP chỉ mở kho này) và reviewer cấm "tự chọn SHA chưa được readback" — chủ kho cấp SHA rồi mới ghim (F07 còn mở).
    chot(len(uploads) == 1, f"đúng một upload action: {uploads}")
    chot("workflow_sha" in scripts and "$TL_S" in scripts and "workflow_ref" in scripts,
         "định nghĩa workflow phải được so với S trong thân run (không suy từ checkout)")


@ca
def t149_review_F09_preflight_object_store_khong_ke_thua_env():
    from unittest import mock
    mod = _nap_cong()
    with San() as s:
        cay, (_, _, H) = _kho_do_thi(s)
        run, calls = mod.subprocess.run, []
        def theo_doi(argv, *a, **kw):
            if "rev-parse" in argv:
                calls.append((list(argv), kw.get("env")))
            return run(argv, *a, **kw)
        with mock.patch.dict(os.environ, {"WP488_REVIEW_SENTINEL": "caller"}), \
                mock.patch.object(mod.subprocess, "run", theo_doi):
            kho = mod.KhoObject(cay)
        try:
            chot(kho.commit(H)[0], "control nguồn git hợp lệ vẫn đọc được")
            chot(calls and all(isinstance(env, dict) and "WP488_REVIEW_SENTINEL" not in env
                              and Path(argv[0]).is_absolute() for argv, env in calls),
                 f"source preflight phải có env tường minh từ rỗng, không env=None: {calls}")
        finally:
            kho.dong()


@ca
def t150_review2_F10_nguon_khong_utf8_la_12_khong_traceback():
    """Review lượt 2 (claude): nguồn KHÔNG PHẢI UTF-8 ở đường consumer phải là Chan 12, không UnicodeDecodeError.
    (a) marker + policy không phải UTF-8 — chốt Q13 của `_kiem_so_rong_khi_chua_kich_hoat`;
    (b) tên tệp trong sổ không phải UTF-8 — răng cho catch của `_ls_tree_z` (mutant bỏ catch phải đỏ ở đây)."""
    mod = _nap_cong()
    with San() as s:
        cay, g = _kho_thu(s)
        g(cay, "checkout", "-q", "-b", "meta-pol-hong")
        p = cay / "ops" / "thu-hoi" / "_ngoai-le-closure.retired.yaml"
        p.parent.mkdir(parents=True); p.write_bytes(_yaml_bytes(_metadata_retired()))
        q = cay / ".github" / "coordination" / "change-impact.v1.json"
        q.parent.mkdir(parents=True); q.write_bytes(b'{"a": "\xc3\x28"}\n')
        g(cay, "add", "-A"); g(cay, "commit", "-qm", "policy non-utf8")
        g(cay, "push", "-q", "origin", "meta-pol-hong")
        try:
            rc, o, e = _goi_main(mod, "ai-dang-giu", "ops/x.md", "--root", cay)
        except UnicodeDecodeError:
            chot(False, "policy không phải UTF-8 làm CLI nổ UnicodeDecodeError — hợp đồng đòi Chan 12")
        chot(rc == 12 and "Traceback" not in e, f"policy không phải UTF-8 phải 12, không traceback: {rc} {e[-200:]!r}")
    with San() as s:
        cay, g = _kho_thu(s)
        g(cay, "checkout", "-q", "-b", "ten-hong")
        d = cay / "ops" / "thu-hoi"; d.mkdir(parents=True)
        # Construct a raw Git path without requiring invalid UTF-8 filenames
        # to be representable by the native Windows filesystem.
        blob = subprocess.run(["git", "-C", str(cay), "hash-object", "-w", "--stdin"],
                              input=b"x: 1\n", capture_output=True, check=True).stdout.strip()
        subprocess.run(["git", "-C", str(cay), "update-index", "-z", "--index-info"],
                       input=b"100644 " + blob + b"\tops/thu-hoi/thu\xe9.yaml\0",
                       capture_output=True, check=True)
        g(cay, "commit", "-qm", "ten non-utf8")
        g(cay, "push", "-q", "origin", "ten-hong")
        try:
            rc, o, e = _goi_main(mod, "ai-dang-giu", "ops/x.md", "--root", cay)
        except UnicodeDecodeError:
            chot(False, "tên không phải UTF-8 làm CLI nổ UnicodeDecodeError — hợp đồng đòi Chan 12")
        chot(rc == 12 and "Traceback" not in e, f"tên không phải UTF-8 phải 12, không traceback: {rc} {e[-200:]!r}")


@ca
def t151_review_codex_to_tien_non_tree_metadata_rac_va_khoa_lan_kieu():
    """Codex connector review trên 457affd (PR #492, review 5162390620) — ba finding, mỗi finding một chốt:
    C1 (P1) tổ tiên của `ops/thu-hoi` là blob/symlink ⇒ 12 ở CẢ reader M4 lẫn consumer, không suy "sổ vắng";
    C2 (P2) consumer phải validate marker retired qua schema sáu khoá TRƯỚC khi hỏi policy (marker rác + `{}` ⇒ 12);
    C3 (P2) khoá thừa lẫn kiểu trong bản ghi thu hồi ⇒ 8, không TypeError. Kèm positive control cho từng chốt."""
    mod = _nap_cong()
    # C1 — reader M4: H thay `ops` bằng blob / symlink
    with San() as s:
        cay, (c0, c1, S) = _kho_do_thi(s)
        for kind in ("blob", "symlink"):
            _g_a0(cay, "reset", "-q", "--hard"); _g_a0(cay, "checkout", "-q", "-B", "h-ops-" + kind, S)
            _g_a0(cay, "rm", "-rq", "ops")
            if kind == "blob":
                (cay / "ops").write_bytes(b"khong phai thu muc\n")
            else:
                (cay / "ops").symlink_to("docs")
            _g_a0(cay, "add", "-A"); _g_a0(cay, "commit", "-qm", "ops " + kind)
            H = _g_a0(cay, "rev-parse", "HEAD")
            rc, o, e = _goi_main(mod, "kiem-thu-hoi-github", H, "--canonical-base", S, "--nhanh-mac-dinh", "master", "--root", str(cay))
            chot(rc == 12 and "tổ tiên" in e and "TAP_THU_HOI_RONG" not in o,
                 f"M4: ops={kind} phải 12, không được kết luận sổ rỗng: {rc} {o!r} {e[-160:]!r}")
        # positive control: H xoá hẳn `ops` (tổ tiên VẮNG, không phải non-tree) ⇒ vẫn 0 ở A0
        H_xoa = _them_commit(cay, "h-xoa-ops", S, {"docs/b.md": b"b\n"}, xoa=("ops/leases/x.yaml", "ops/lease_publish.py"))
        rc, o, e = _goi_main(mod, "kiem-thu-hoi-github", H_xoa, "--canonical-base", S, "--nhanh-mac-dinh", "master", "--root", str(cay))
        chot(rc == 0 and "TAP_THU_HOI_RONG" in o, f"ops vắng hẳn (không phải non-tree) phải 0: {rc} {e[-160:]!r}")
    # C1 — consumer: một ref trên origin có `ops` là blob
    with San() as s:
        cay, g = _kho_thu(s)
        g(cay, "checkout", "-q", "-b", "ops-blob")
        g(cay, "rm", "-rq", "ops"); (cay / "ops").write_bytes(b"x\n")
        g(cay, "add", "-A"); g(cay, "commit", "-qm", "ops blob"); g(cay, "push", "-q", "origin", "ops-blob")
        rc, o, e = _goi_main(mod, "ai-dang-giu", "ops/x.md", "--root", cay)
        chot(rc == 12 and "không phải thư mục" in e and "Traceback" not in e,
             f"consumer: ops là blob phải 12, không suy sổ vắng: {rc} {e[-160:]!r}")
    # C2 — consumer: marker rác + policy `{}` ⇒ 12; positive control: marker đúng schema + `{}` ⇒ 0
    RET = "ops/thu-hoi/_ngoai-le-closure.retired.yaml"
    POL = ".github/coordination/change-impact.v1.json"
    for ten, marker, mong in (("marker rác", b"garbage\n", 12), ("marker đúng schema", _yaml_bytes(_metadata_retired()), 0)):
        with San() as s:
            cay, g = _kho_thu(s)
            g(cay, "checkout", "-q", "-b", "meta")
            for duong, noi_dung in ((RET, marker), (POL, b"{}\n")):
                p = cay / duong; p.parent.mkdir(parents=True, exist_ok=True); p.write_bytes(noi_dung)
            g(cay, "add", "-A"); g(cay, "commit", "-qm", ten); g(cay, "push", "-q", "origin", "meta")
            rc, o, e = _goi_main(mod, "ai-dang-giu", "ops/x.md", "--root", cay)
            chot(rc == mong and "Traceback" not in e, f"consumer {ten} + policy {{}} phải {mong}: {rc} {e[-200:]!r}")
    # C3 — khoá thừa lẫn kiểu (int 1 + str extra): 8 với thông điệp khoá thừa, không TypeError
    noi_dung = _yaml_bytes(_ban_ghi_thu_hoi()) + b"1: x\nextra: y\n"
    try:
        rc, msg = _ma_chan(mod, mod.kiem_ban_ghi_thu_hoi, "ops/thu-hoi/wp1-exec-1-codex-20260901.yaml", "100644", "blob", noi_dung)
    except TypeError as ex:
        chot(False, f"khoá thừa lẫn kiểu làm sorted ném TypeError thay vì Chan 8: {ex}")
    chot(rc == mod.RC_NOI_DUNG and "khoá thừa" in str(msg), f"khoá thừa lẫn kiểu phải 8: {rc} {msg!r}")


@ca
def t152_C2a_M9_fetch_H_mang_xac_thuc_qua_header_khong_token_trong_URL():
    """#503: Bash thật từ đầu bước tới trước NHAN; Git config thật; token giả, không mạng.
    Stub rev-parse cấp S/blob giả; stub fetch đo config theo URL. (i) env/token/header; (ii) URL sạch;
    (iii) không ghi config; (iv) checkout không giữ credential; (v) mask trước fetch, stdout/stderr sạch.
    """
    import base64, yaml
    steps = yaml.safe_load(WORKFLOW_THU_HOI.read_text(encoding="utf-8"))["jobs"]["thu-hoi"]["steps"]
    checkout = [b for b in steps if str(b.get("uses", "")).startswith("actions/checkout@")]
    chot(len(checkout) == 1 and (checkout[0].get("with") or {}).get("persist-credentials") is False,
         "(iv) checkout S phải giữ `persist-credentials: false`")
    lenh_fetch, lenh_config = [], []
    for b in steps:
        than = b.get("run")
        if not isinstance(than, str):
            continue
        ds = _dong_lenh(than)
        for i, lenh in enumerate(ds):
            if re.search(r"\bgit\b.*\bfetch\b", lenh) and "refs/pull/" in lenh:
                lenh_fetch.append((lenh, ds, i, than, b.get("env") or {}))
            if re.search(r"\bgit\b[^\n]*\bconfig\b[^\n]*extraheader", lenh):
                lenh_config.append(lenh)
    chot(len(lenh_fetch) == 1, f"đúng một lời gọi fetch H, thấy {len(lenh_fetch)}")
    f, ds, i, than, mt = lenh_fetch[0]
    chot(re.sub(r"\s+", "", str(mt.get("TL_TOKEN", ""))) in ("${{secrets.GITHUB_TOKEN}}", "${{github.token}}"),
         "(i) env TL_TOKEN của bước fetch phải lấy GitHub token")
    url = re.findall(r"https://[^\s\"']+", f)
    chot(url and all("@" not in u and "TL_TOKEN" not in u for u in url),
         f"(ii) URL fetch mang credential: {url}")
    chot(not lenh_config, f"(iii) không được `git config` ghi extraheader vào cây S: {lenh_config}")
    dau = [j for j in range(i) if ds[j].startswith("WF_BLOB=")]
    cuoi = [j for j in range(i + 1, len(ds)) if ds[j].startswith("NHAN=")]
    chot(len(dau) == len(cuoi) == 1, "(i) không tìm được ranh giới đoạn auth/fetch")
    # Giữ nguyên bytes shell và chạy cả preflight: cờ debug trước WF_BLOB cũng có hiệu lực.
    doan = than[:than.index("\nNHAN=")]
    stub = r'''set -euo pipefail
    git() {
      if [ "${1-}" = rev-parse ] && [ "$#" -eq 2 ]; then
        case "$2" in HEAD|"$TL_WF_SHA:.github/workflows/ops-thu-hoi-admission.yml") printf '%s\n' "$TL_S"; return;; esac
      fi
      local -a cfg=()
      while [ "${1-}" = -c ]; do cfg+=("$1" "$2"); shift 2; done
      [ "$#" -eq 4 ] && [ "$1" = fetch ] && [ "$2" = --no-tags ] || return 91
      [ "$3" = "https://github.com/$TL_KHO" ] || return 92
      [ "$4" = "+refs/pull/$TL_PR/head:refs/thu-hoi/ung-vien" ] || return 93
      [ "$(command git "${cfg[@]}" config --get protocol.https.allow)" = always ] || return 95
      command git "${cfg[@]}" config --get-urlmatch http.extraheader "$3"
      if command git "${cfg[@]}" config --get-urlmatch http.extraheader https://example.invalid/repo; then return 94; fi
    }
    '''
    for token in ("m9-fixture-token-" + "0123456789aBcDeF" * 4 + tail for tail in ("", "x", "xy")):  # dài, padding 0/2/1
        b64 = base64.b64encode(("x-access-token:" + token).encode()).decode()
        with San() as s:
            cfg = s / "empty.config"; cfg.write_text("", encoding="utf-8")
            env = dict(PATH=os.environ["PATH"], TL_TOKEN=token, TL_KHO="ducthangho/tra-luat", TL_PR="505",
                       TL_S="a" * 40, TL_H="b" * 40, TL_WF_SHA="a" * 40, TL_NHANH="master",
                       TL_WF_REF="ducthangho/tra-luat/.github/workflows/ops-thu-hoi-admission.yml@refs/heads/master",
                       GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=str(cfg))
            p = subprocess.run([_bash_posix(), "--noprofile", "--norc", "-c", stub + doan +
                                '\ntest -z "${AUTH_B64+x}${GIT_CONFIG_COUNT+x}${GIT_CONFIG_KEY_0+x}${GIT_CONFIG_VALUE_0+x}"\n'],
                               cwd=s, env=env, capture_output=True, text=True, timeout=10)
        chot(p.returncode == 0, f"(i) đoạn auth/fetch không chạy được: rc={p.returncode}: {p.stderr}")
        dong = p.stdout.splitlines()
        chot(dong and dong[-1] == "AUTHORIZATION: basic " + b64,
             "(i) Git không nhận header hiệu lực dẫn từ TL_TOKEN trên URL fetch")
        chot(dong == ["::add-mask::" + b64, "AUTHORIZATION: basic " + b64] and not p.stderr,
             "(v) phải đăng ký mask đúng base64 trước fetch, không có output thừa (kể cả stderr)")


@ca
def t153_nhat_ky_tung_ca_vao_ra_cap_doi_va_khong_dem():
    """M3 packet #504 (#499 C3): mỗi ca in đúng một `>>> vao X` rồi đúng một `<<< ra X` SAU nó, và dòng tổng
    kết vẫn khớp regex của t125. Chạy chính tệp này trong tiến trình con với đúng một ca rẻ (`--chi-ca=t01_`),
    stdout qua PIPE và KHÔNG đọc cho tới khi tiến trình con kết thúc.

    Spec ghi tên ca này là `t152_…`; số ấy đã bị M9 (#503) dùng nên ở đây là t153 — ý nghĩa giữ nguyên.

    ĐỘT BIẾN LÀM CA NÀY ĐỎ: bỏ dòng `<<< ra` (hoặc `>>> vao`) trong `main()`; đổi định dạng (tên ca không còn là
    token sau `vao`/`ra`); in `ra` TRƯỚC `vao`; làm hỏng dòng tổng kết. ĐỘT BIẾN KHÔNG LÀM CA NÀY ĐỎ — CÓ CHỦ Ý:
    bỏ `flush=True` trong `_nhat_ky_ca` — đệm được xả khi tiến trình con kết thúc nên ca này vẫn thấy đủ dòng;
    chốt "không đệm" (`PYTHONUNBUFFERED=1` ở wrapper) chỉ đo được ở M4: lượt Windows thật bị huỷ giữa chừng mà dòng
    `>>> vao` cuối vẫn hiện ra trong log. Đừng thêm phép đo giả cho nó ở đây.
    """
    import subprocess
    nen = {k: v for k, v in os.environ.items() if k != "GITHUB_ACTOR"}
    p = subprocess.Popen([sys.executable, str(Path(__file__).resolve()), CO_CHI_CA + "t01_"],
                         stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=nen)
    try:
        p.wait(timeout=30)  # M4 t153=0.250 s; 30 s là trần cho con chỉ chạy t01, chưa đọc PIPE
    except subprocess.TimeoutExpired:
        p.kill(); p.wait(timeout=5)
        bang(False, "con t01 của t153 không kết thúc trong 30 s — đã kill")
    out, err = p.communicate(timeout=5)  # chỉ đọc SAU khi con kết thúc (M3)
    vao = re.findall(r"(?m)^>>> vao (\S+) \d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ$", out)
    ra = re.findall(r"(?m)^<<< ra (\S+) \d+\.\d{3}s (QUA|DO|BO_QUA)$", out)
    bang(vao == ["t01_lease_hop_le_thi_QUA"], f"lượt con phải chạy ĐÚNG một ca t01_: vao={vao!r}; rc={p.returncode}; "
                                              f"stdout={out[-300:]!r}; stderr={err[-200:]!r}")
    bang([x for x, _ in ra] == vao and ra[0][1] == "QUA", f"mỗi `vao` phải có đúng một `ra` cùng tên, kết QUA: ra={ra!r}")
    bang(out.index(">>> vao ") < out.index("<<< ra "), "`<<< ra` phải in SAU `>>> vao`")
    m = re.search(r"lease_publish: (\d+)/(\d+) đạt", out)
    bang(m and m.group(1) == m.group(2) == "1" and p.returncode == 0,
         f"dòng tổng kết phải còn khớp regex của t125 và là 1/1, rc=0: m={m and m.group(0)!r}, rc={p.returncode}")


# Mã của cháu và của con cho t154. Cháu ĐẬP NHỊP vào một tệp rồi TỰ HUỶ sau 30 s: một phản chứng về
# việc giết tiến trình không được phép để lại tiến trình mồ côi khi chính nó hỏng.
_MA_CHAU_T154 = (
    "import os,sys,time\n"
    "nhip, pid = sys.argv[1], sys.argv[2]\n"
    "open(pid,'w').write(str(os.getpid()))\n"
    "het = time.monotonic() + 30\n"
    "while time.monotonic() < het:\n"
    "    f = open(nhip,'a'); f.write('x'); f.flush(); f.close()\n"
    "    time.sleep(0.05)\n"
)
_MA_CON_T154 = (
    "import subprocess,sys,time\n"
    "subprocess.Popen([sys.executable,'-c',sys.argv[1],sys.argv[2],sys.argv[3]])\n"
    "time.sleep(60)\n"
)


@ca
def t154_giet_ca_cay_thu_hoi_CHAU_chu_khong_chi_CON():
    """Phản chứng HAI CHIỀU cho `_giet_ca_cay` (cross-review codex 11-09-2026, P1).

    Ca này ĐO HÀNH VI của cháu — nhịp tim ghi ra tệp — chứ không đọc mã thoát của lệnh giết: "đã gọi
    lệnh giết" ≠ "đã chết", và `taskkill` từng trả `Access denied` ngay trên con của chính mình. Nhịp
    tim cũng miễn nhiễm với tái dùng PID, thứ mà phép hỏi `os.kill(pid, 0)` không phân biệt được.

    CHIỀU 1 (phản chứng có RĂNG): giết ĐÚNG PID con ⇒ cháu PHẢI còn đập. Không có chiều này thì không
    biết chiều 2 đang đo cú giết cây hay đang đo một cháu vốn đã tự chết.
    CHIỀU 2: `_giet_ca_cay` ⇒ cháu PHẢI im trong cửa sổ quan sát.

    PHẠM VI ĐO: chạy tại chỗ trên Linux (POSIX `start_new_session` + `killpg`). Đường Windows
    (`CREATE_NEW_PROCESS_GROUP` + `taskkill /T /F` + kiểm lại) CHƯA ĐO ĐƯỢC trong phiên viết ca này —
    lượt Windows nói, và ca viết sao cho một thất bại ở đó hiện thành ĐỎ kèm nhật ký từng bước của
    `_giet_ca_cay`, KHÔNG thành một ca bỏ qua được đếm là đạt.

    ĐỘT BIẾN LÀM CA NÀY ĐỎ: đổi `_giet_ca_cay` về `p.kill()` trần; bỏ `start_new_session` trong
    `_mo_con_nhom_rieng`; nới chốt "chỉ killpg khi nhóm con == PID con" thành killpg vô điều kiện
    (ca này sẽ ĐỎ ở chốt nhóm riêng thay vì giết cả runner).
    """
    import signal
    nen = {k: v for k, v in os.environ.items() if k != "GITHUB_ACTOR"}
    with tempfile.TemporaryDirectory() as td:
        def sinh(ten):
            nhip, pid = Path(td) / (ten + ".nhip"), Path(td) / (ten + ".pid")
            p = _mo_con_nhom_rieng([sys.executable, "-c", _MA_CON_T154, _MA_CHAU_T154, str(nhip), str(pid)],
                                   nen, subprocess.DEVNULL, subprocess.DEVNULL)
            return p, nhip, pid

        def doi_nhip(nhip, han=15.0):
            t0 = time.monotonic()
            while time.monotonic() - t0 < han:
                if nhip.exists() and nhip.stat().st_size > 0:
                    return True
                time.sleep(0.05)
            return False

        def con_dap(nhip, cho=1.0):
            a = nhip.stat().st_size if nhip.exists() else -1
            time.sleep(cho)
            b = nhip.stat().st_size if nhip.exists() else -1
            return b > a, a, b

        def don_chau(pid_tep):
            """Dọn cháu mồ côi của chiều 1. Cháu cũng tự huỷ sau 30 s — hai lớp, vì một lớp có thể hỏng."""
            try:
                so = int(pid_tep.read_text(encoding="utf-8").strip())
            except (OSError, ValueError):
                return
            try:
                if os.name == "posix":
                    os.kill(so, getattr(signal, "SIGKILL", signal.SIGTERM))
                else:
                    subprocess.run(["taskkill", "/F", "/PID", str(so)], capture_output=True, timeout=10)
            except (OSError, subprocess.SubprocessError):
                pass

        # ── CHIỀU 1: giết ĐÚNG PID con ⇒ cháu còn sống (phản chứng có răng)
        p1, nhip1, pid1 = sinh("chieu1")
        try:
            bang(doi_nhip(nhip1), "fixture hỏng: cháu chiều 1 không đập nhịp trong 15 s — chưa đo được gì")
            gp = getattr(os, "getpgid", None)
            if gp is not None:
                bang(gp(p1.pid) == p1.pid and gp(p1.pid) != gp(0),
                     f"con phải là LÃNH ĐẠO một nhóm RIÊNG, kẻo cú giết cây nhắm vào nhóm của chính runner: "
                     f"nhom_con={gp(p1.pid)} pid={p1.pid} nhom_minh={gp(0)}")
            p1.kill()
            p1.wait(timeout=5)
            dap, a, b = con_dap(nhip1)
            bang(dap, f"phản chứng MẤT RĂNG: giết đúng PID con mà cháu đã im (nhịp {a}->{b}); "
                      f"cháu phải sống sót cú giết PID, nếu không thì chiều 2 không chứng minh gì")
        finally:
            if p1.poll() is None:
                p1.kill(); p1.wait(timeout=5)
            don_chau(pid1)

        # ── CHIỀU 2: `_giet_ca_cay` ⇒ cháu im
        p2, nhip2, pid2 = sinh("chieu2")
        try:
            bang(doi_nhip(nhip2), "fixture hỏng: cháu chiều 2 không đập nhịp trong 15 s")
            nhat_ky = _giet_ca_cay(p2)
            bang(p2.poll() is not None, f"con chưa chết sau `_giet_ca_cay`: {nhat_ky}")
            dap, a, b = con_dap(nhip2)
            bang(not dap, f"`_giet_ca_cay` KHÔNG thu hồi được CHÁU: nhịp còn tăng {a}->{b}; "
                          f"nhật ký giết: {nhat_ky}")
        finally:
            if p2.poll() is None:
                p2.kill(); p2.wait(timeout=5)
            don_chau(pid2)


    # Giữ chốt nhóm của runner bằng seam tín hiệu: không gửi tín hiệu thật tới nhóm ấy.
    from unittest import mock
    if os.name == "posix":
        for nhom_con, nhom_minh in ((43210, 43210), (12345, 12345), (12345, 67890)):
            p = mock.Mock(pid=43210, returncode=-9)
            p.poll.return_value = -9
            with mock.patch.object(os, "getpgid", side_effect=lambda pid: nhom_minh if pid == 0 else nhom_con), \
                    mock.patch.object(os, "killpg") as kg, \
                    mock.patch.dict(globals(), {"_nap_launcher_thu_hoi": mock.Mock()}) as _:
                _giet_ca_cay(p)
                bang(not kg.called and not _nap_launcher_thu_hoi.called,
                     "không được giết nhóm khi cùng nhóm runner hoặc con không phải trưởng nhóm")

        # Dùng nguyên văn hai fixture đã có; không sáng tác thêm mã đối kháng.
        import ast
        cay = ast.parse((HERE.parent / ".claude/dev/launcher_test.py").read_text(encoding="utf-8"))
        thu_hoi = _nap_launcher_thu_hoi()
        for dau in ("t63_", "t66_"):
            fn = next(n for n in cay.body if isinstance(n, ast.FunctionDef) and n.name.startswith(dau))
            ma = {}
            for call in ast.walk(fn):
                if (isinstance(call, ast.Call) and isinstance(call.func, ast.Attribute)
                        and call.func.attr == "write_text" and isinstance(call.func.value, ast.Name)
                        and call.func.value.id in ("chau_py", "me_py")):
                    ma[call.func.value.id] = ast.literal_eval(call.args[0])
            with tempfile.TemporaryDirectory() as td:
                td = Path(td)
                me, chau, pid_tep = td / "me.py", td / "chau.py", td / "pid"
                me.write_text(ma["me_py"], encoding="utf-8")
                chau.write_text(ma["chau_py"], encoding="utf-8")
                p = _mo_con_nhom_rieng([sys.executable, str(me), str(chau), str(pid_tep)],
                                      nen, subprocess.DEVNULL, subprocess.DEVNULL)
                pid, khoa_pid = None, None
                try:
                    het = time.monotonic() + 15
                    while not pid_tep.exists() and time.monotonic() < het:
                        time.sleep(0.05)
                    bang(pid_tep.exists(), f"fixture {dau} chưa ghi PID cháu")
                    pid = int(pid_tep.read_text(encoding="utf-8"))
                    khoa_pid = thu_hoi._khoa_danh_tinh(pid)
                    bang(khoa_pid is not None and thu_hoi._con_song_dung_khoa(pid, khoa_pid),
                         f"fixture {dau}: chưa đo được cháu sống trước thu hồi")
                    nhat_ky = _giet_ca_cay(p)
                    bang(p.poll() is not None and not thu_hoi._con_song_dung_khoa(pid, khoa_pid),
                         f"fixture {dau}: cháu sống sau thu hồi: {nhat_ky}")
                finally:
                    if pid is not None and khoa_pid is not None:
                        thu_hoi._giet_rieng({pid: khoa_pid}, signal.SIGKILL)
                    if p.poll() is None:
                        p.kill()
                    p.wait(timeout=5)


@ca
def t157_tee_dua_dong_con_LEN_NGAY_trong_luc_con_CON_DANG_CHAY():
    """Phản chứng cho tee `_theo_duoi_va_in` (cross-review codex 11-09-2026, P2).

    Tính chất cần giữ KHÔNG phải "tee có tồn tại" mà là "dòng của con LÊN LOG TRƯỚC khi con kết thúc"
    — vì ca hỏng là job bị huỷ GIỮA t125: nếu bằng chứng chỉ xuất hiện lúc đọc tệp ở cuối thì nó
    không bao giờ xuất hiện. Nên ca này đòi ĐỒNG THỜI hai điều đo được: dòng ĐÃ có trên stdout, và
    con VẪN đang chạy lúc ấy.

    Chốt thứ hai: dòng teed phải mang TIỀN TỐ ở đầu dòng, nên KHÔNG khớp `(?m)^>>> vao` — nhật ký của
    con không được lẫn thành nhật ký của cha. Thiếu chốt này thì `t153` và chính `t125` có thể đọc
    dòng của con thành dòng của mình.

    ĐỘT BIẾN LÀM CA NÀY ĐỎ: bỏ luồng tee trong t125 sẽ KHÔNG làm ca này đỏ (ca đo hàm, không đo lời
    gọi) — nên đột biến đích là: `_theo_duoi_va_in` chỉ in khi `dung` đã set (tức chỉ in ở cuối); bỏ
    tiền tố; bỏ `flush=True`; đọc text theo khối thay vì nhị phân từng dòng.
    """
    # Quan sát bytes bên dưới TextIOWrapper; StringIO.getvalue() thấy cả dữ liệu chưa flush.
    import io
    import threading
    nen = {k: v for k, v in os.environ.items() if k != "GITHUB_ACTOR"}
    with tempfile.TemporaryDirectory() as td:
        log = Path(td) / "con.out"
        log.write_text("", encoding="utf-8")
        ma = ("import sys,time\n"
              "f = open(sys.argv[1], 'a', encoding='utf-8')\n"
              "f.write('>>> vao t_gia_dang_chay 2026-01-01T00:00:00Z' + chr(10)); f.flush()\n"
              "time.sleep(30)\n")
        dung, khoa = threading.Event(), threading.Lock()
        luu = io.BytesIO()
        bat = io.TextIOWrapper(luu, encoding="utf-8", newline="\n")
        # Hiệu chuẩn chính phép đọc sẽ dùng bên dưới: phải phân biệt write và flush.
        # Đổi capture về StringIO sẽ đỏ ở đây, kể cả khi đồng thời bỏ flush của tee.
        try:
            bat.write("kiem-dem")
            bang(luu.getvalue().decode("utf-8") == "",
                 "capture mất răng: thấy dữ liệu CHƯA flush")
            bat.flush()
            bang(luu.getvalue().decode("utf-8") == "kiem-dem",
                 "capture hỏng: không thấy dữ liệu ĐÃ flush")
            bat.seek(0)
            bat.truncate(0)
        except Exception:
            bat.close()
            raise
        p = _mo_con_nhom_rieng([sys.executable, "-c", ma, str(log)], nen,
                              subprocess.DEVNULL, subprocess.DEVNULL)
        cu = sys.stdout
        t = threading.Thread(target=_theo_duoi_va_in, args=(log, "[GIA]", dung, khoa), daemon=True)
        try:
            sys.stdout = bat
            t.start()
            t0, thay, con_song = time.monotonic(), "", None
            while time.monotonic() - t0 < 15:
                thay = luu.getvalue().decode("utf-8")
                if "t_gia_dang_chay" in thay:
                    con_song = p.poll() is None      # ĐO NGAY: con còn chạy lúc dòng đã lên chưa?
                    break
                time.sleep(0.05)
        finally:
            sys.stdout = cu
            dung.set()
            t.join(timeout=5)
            nhat_ky = _giet_ca_cay(p)
            bat.close()
        bang("t_gia_dang_chay" in thay,
             f"tee KHÔNG đưa dòng của con lên stdout trong 15 s: bắt được {thay!r}; giết: {nhat_ky}")
        bang(con_song is True,
             f"dòng chỉ lên SAU khi con kết thúc — đúng chỗ mù mà job bị huỷ giữa t125 sẽ rơi vào: "
             f"con_song={con_song}; bắt được {thay!r}")
        dong = [x for x in thay.splitlines() if "t_gia_dang_chay" in x]
        bang(dong and dong[0].startswith("[GIA] "),
             f"dòng teed phải mang tiền tố ở ĐẦU dòng: {dong!r}")
        bang(not re.search(r"(?m)^>>> vao ", thay),
             f"dòng teed KHÔNG được khớp regex nhật ký của CHA (`^>>> vao`), kẻo nhật ký con lẫn "
             f"thành nhật ký cha: {thay!r}")


@ca
def t158_tee_chi_song_khi_con_KHONG_DEM_nen_moi_truong_con_phai_TAT_DEM():
    """Bản vá lớp `bang-chung-song-bi-chon-trong-tep-tam` chỉ sống khi lượt con KHÔNG ĐỆM — ca này đo
    đúng chỗ `t157` không thấy, và là lỗi TÁC GIẢ TỰ TÌM sau khi phóng lượt review 3.

    Hai chiều, đúng bảng đã đo 12-09-2026:
    · con KHÔNG `PYTHONUNBUFFERED` ⇒ tee KHÔNG thấy dòng trong cửa sổ quan sát (bằng chứng nằm trong
      đệm của con) — nếu chiều này thấy thì ca mất răng và phải nói ra, đừng mừng.
    · con CÓ `PYTHONUNBUFFERED=1` ⇒ tee THẤY, trong lúc con vẫn đang chạy.
    Và chốt thứ ba: `_moi_truong_con_ab` phải THẬT SỰ đặt biến ấy, đồng thời KHÔNG mang `GITHUB_ACTOR`
    vào (kẻo vá một lỗ mà mở lỗ khác — chính bất biến của t125).

    ĐỘT BIẾN LÀM CA NÀY ĐỎ: `_moi_truong_con_ab` trả `dict(nen)` trần; t125 truyền `mt` thay cho
    `_moi_truong_con_ab(mt)` (seam gọi CHÍNH t125 phía dưới kiểm wiring và hai môi trường tại Popen).
    """
    # Quan sát bytes bên DƯỚI `TextIOWrapper` có đệm, KHÔNG dùng `StringIO`: cross-review lượt 3
    # (F2.1) đo được `StringIO.getvalue()` thấy cả dữ liệu CHƯA xả, nên một phép bắt như thế không
    # phân biệt được stream có đệm với stream đã xả — đúng lý do đột biến bỏ `flush` từng sống sót
    # ở `t157`. Dùng bytes ở đây làm ca này mạnh hơn: nó đỏ cả khi tee thôi xả.
    import io
    import threading
    mt_nen = {k: v for k, v in os.environ.items() if k != "GITHUB_ACTOR"}

    # Gọi consumer thật, chỉ thay tiến trình/tee bằng seam. Không để PYTHONUNBUFFERED
    # của wrapper che mất việc t125 thôi gọi helper. CO_AB cũng không được bỏ phép đo này.
    from unittest import mock
    moi_truong = []
    nen_kiem = {k: v for k, v in os.environ.items() if k in ("TMPDIR", "TEMP", "TMP")}
    nen_kiem.update(AB_GIU="giu", GITHUB_ACTOR="ambient")
    khong_actor = {k: v for k, v in nen_kiem.items() if k != "GITHUB_ACTOR"}
    def sinh_gia(lenh, env, stdout, stderr):
        moi_truong.append(dict(env))
        stdout.write("lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0\n")
        stdout.flush()
        p = mock.Mock(returncode=0)
        p.poll.return_value = 0
        return p
    with mock.patch.dict(os.environ, nen_kiem, clear=True), \
            mock.patch.object(sys, "argv", [sys.argv[0]]), \
            mock.patch.dict(globals(), {"_mo_con_nhom_rieng": sinh_gia,
                                        "_theo_duoi_va_in": mock.Mock()}):
        t125_AB_toan_suite_KHONG_doi_verdict_theo_ambient_actor()
    bang(len(moi_truong) == 2, f"t125 phải sinh đúng hai vế: {moi_truong}")
    a, b = moi_truong
    bang(a == dict(khong_actor, PYTHONUNBUFFERED="1")
         and b == dict(a, GITHUB_ACTOR="ke-la-mat-khong-co-quyen"),
         f"môi trường THỰC ở t125 phải tắt đệm cả hai vế, giữ nền và chỉ khác GITHUB_ACTOR: {a}, {b}")

    bang("PYTHONUNBUFFERED" in _moi_truong_con_ab({}) and _moi_truong_con_ab({})["PYTHONUNBUFFERED"] == "1",
         f"`_moi_truong_con_ab` phải TẮT ĐỆM cho lượt con: {_moi_truong_con_ab({})!r}")
    bang("GITHUB_ACTOR" not in _moi_truong_con_ab({"A": "1"}),
         "`_moi_truong_con_ab` không được mang `GITHUB_ACTOR` vào — đó là bất biến của t125")

    ma = "import sys,time\nprint('>>> vao t_do_dem_158 2026-01-01T00:00:00Z')\ntime.sleep(8)\n"  # KHÔNG flush
    def do(mt):
        with tempfile.TemporaryDirectory() as td:
            lg = Path(td) / "o"
            lg.write_text("", encoding="utf-8")
            with open(lg, "w", encoding="utf-8") as ow:
                p = _mo_con_nhom_rieng([sys.executable, "-c", ma], mt, ow, subprocess.DEVNULL)
                dung, khoa = threading.Event(), threading.Lock()
                luu = io.BytesIO()
                bat = io.TextIOWrapper(luu, encoding="utf-8", newline="\n")
                cu = sys.stdout
                try:
                    sys.stdout = bat
                    t = threading.Thread(target=_theo_duoi_va_in, args=(lg, "[158]", dung, khoa), daemon=True)
                    t.start()
                    t0, thay = time.monotonic(), ""
                    while time.monotonic() - t0 < 3.0:
                        thay = luu.getvalue().decode("utf-8", "replace")
                        if "t_do_dem_158" in thay:
                            break
                        time.sleep(0.05)
                    con_song = p.poll() is None
                finally:
                    sys.stdout = cu
                    dung.set()
                    t.join(timeout=5)
                    nhat_ky = _giet_ca_cay(p)
                    bat.close()
            return ("t_do_dem_158" in thay), con_song, nhat_ky

    thay_dem, song_dem, _ = do({k: v for k, v in mt_nen.items() if k != "PYTHONUNBUFFERED"})
    bang(song_dem, "chiều CÒN ĐỆM phải có con sống; con chết sớm không chứng minh đệm giữ dòng")
    bang(not thay_dem,
         "phản chứng MẤT RĂNG: con CÒN ĐỆM mà tee đã thấy dòng — nghĩa là phép đo này không còn phân "
         "biệt được hai đường, và câu 'phải tắt đệm' trong `_moi_truong_con_ab` thành vô căn cứ; "
         "hãy ĐO LẠI rồi sửa lời khai, đừng mừng vì ca xanh")
    thay_tat, song_tat, nhat_ky = do(_moi_truong_con_ab(mt_nen))
    bang(thay_tat and song_tat,
         f"với môi trường của lượt con (đã TẮT ĐỆM), tee phải thấy dòng TRONG LÚC con còn chạy: "
         f"thay={thay_tat} con_song={song_tat}; giết: {nhat_ky}")


@ca
def t160_lech_AB_phai_giu_bang_chung_va_CHAN_tai_consumer_t125():
    """Đo CHÍNH t125: dữ liệu bịa tại ranh giới tiến trình, parser/so sánh/chốt thật.

    So hàm riêng không khóa được wiring: bỏ classifier, nuốt kết quả lệch hay
    cho cổng nhận trạng thái chưa rõ đều từng qua t160 cũ. Đo cả vế khớp và các
    dạng lệch, giữ đúng nhãn A/B, và kiểm bốn luồng tee tại consumer. Mỗi thành phần
    của tuple phải có chiều chỉ riêng nó thay đổi. Không cho một lần retry thay thế
    bằng chứng của toàn suite, dù retry dùng run hay Popen trực tiếp.
    """
    from unittest import mock
    a = (0, "2", "2", frozenset(), frozenset())
    do_x = (1, "1", "2", frozenset({"t_x"}), frozenset())
    do_y = (1, "1", "2", frozenset({"t_y"}), frozenset())
    bo_x = (0, "1", "1", frozenset(), frozenset({"t_x"}))
    bo_y = (0, "1", "1", frozenset(), frozenset({"t_y"}))

    def do(cap):
        da_sinh = []
        def sinh_gia(lenh, env, stdout, stderr):
            k = cap[len(da_sinh)]
            da_sinh.append((list(lenh), dict(env)))
            for ten in sorted(k[3]):
                stdout.write(f"  ĐỎ  {ten}: lý do gốc của fixture\n")
            for ten in sorted(k[4]):
                stdout.write(f"  BỎ QUA {ten}: nền fixture\n")
            stdout.write(f"lease_publish: {k[1]}/{k[2]} đạt\n")
            stdout.flush()
            p = mock.Mock(returncode=k[0])
            p.poll.return_value = k[0]
            return p
        loi, tee = None, mock.Mock()
        phan_loai = mock.Mock(wraps=_phan_loai_lech_ab)
        with mock.patch.object(sys, "argv", [sys.argv[0]]), \
                mock.patch.dict(globals(), {"_mo_con_nhom_rieng": sinh_gia,
                                            "_theo_duoi_va_in": tee,
                                            "_phan_loai_lech_ab": phan_loai}), \
                mock.patch.object(subprocess, "run") as chay_them, \
                mock.patch.object(subprocess, "Popen") as mo_them:
            try:
                t125_AB_toan_suite_KHONG_doi_verdict_theo_ambient_actor()
            except AssertionError as ex:
                loi = str(ex)
        cac_cap_da_so = list(phan_loai.call_args_list)
        bang(cac_cap_da_so == [mock.call(*cap)],
             f"classifier phải nhận đúng tuple theo nhãn không-actor rồi có-actor: {cac_cap_da_so!r}")
        bang(len(da_sinh) == 2 and all(x[0][-1] == CO_AB for x in da_sinh),
             f"phải đo đúng hai lượt TOÀN SUITE qua t125: {da_sinh!r}")
        bang(not chay_them.called and not mo_them.called,
             "t125 không được mở thêm tiến trình bằng run/Popen ngoài hai vế A/B")
        duong_tee = sorted((x.args[0].name, x.args[1]) for x in tee.call_args_list)
        bang(duong_tee == [("A.err", "[A err]"), ("A.out", "[A]"),
                          ("B.err", "[B err]"), ("B.out", "[B]")],
             f"consumer t125 phải nối đủ bốn tệp vào đúng tee: {duong_tee!r}")
        if cap[0] != cap[1]:
            for nhan, k in zip(("không-actor", "có-actor"), cap):
                can = f"{nhan}=(rc={k[0]}, {k[1]}/{k[2]})"
                bang(loi is not None and can in loi,
                     f"chẩn đoán phải giữ đúng vế {can!r}: {loi!r}")
        return loi

    bang(do((a, a)) is None, "hai vế khớp phải qua consumer t125")
    bang(do((do_x, do_x)) is None, "t125 so bất biến, không thay verdict của từng ca con")
    for cap, can_co in (
            ((a, do_x), ("t_x", "rc=0, 2/2", "rc=1, 1/2")),
            ((do_x, do_y), ("t_x", "t_y")),
            ((bo_x, bo_y), ("t_x", "t_y", "BỎ QUA")),
            ((a, (1, *a[1:])), ("rc=0", "rc=1")),
            ((a, (0, "1", "2", a[3], a[4])), ("1/2", "2/2")),
            ((do_x, (1, "1", "3", do_x[3], do_x[4])), ("1/2", "1/3"))):
        for hai_ve in (cap, cap[::-1]):
            loi = do(hai_ve)
            bang(loi is not None and LECH_CHUA_RO in loi,
                 f"mọi lệch phải làm CHÍNH t125 đỏ, chưa rõ nguyên nhân: {hai_ve!r}: {loi!r}")
            bang("CHƯA loại trừ rò GITHUB_ACTOR" in loi and "[A]/[B]" in loi
                 and all(x in loi for x in can_co),
                 f"phải giữ bằng chứng gốc và khả năng rò actor trong chẩn đoán: {loi!r}")


@ca
def t155_chon_ca_khong_khop_hoac_RONG_thi_KHONG_XANH():
    """Selector `--chi-ca=` gõ sai hay rỗng ⇒ rc≠0, và KHÔNG in dòng tổng kết (codex 11-09-2026, P2).

    Vì sao đáng một ca riêng: bản trước trả `lease_publish: 0/0 đạt` + rc=0, tức một cổng VẮNG MẶT
    trông y hệt một cổng XANH — cùng họ với "cổng không nói dối, nó vắng mặt". Một script bảo trì hay
    một reviewer chạy `--chi-ca=<tên ca đã đổi>` sẽ ghi một phép đo GIẢ mà không có dấu hiệu nào.

    Ba đường phải giữ nguyên, và ca này nói rõ đường nào ĐO Ở ĐÂY, đường nào đo Ở CHỖ KHÁC:
    · prefix HỢP LỆ ⇒ vẫn chạy, vẫn `1/1`, rc=0 — đo ở đây (và t153 đo kỹ định dạng nhật ký).
    · `CO_AB` ⇒ vẫn chạy — đo ở đây, kèm một prefix hợp lệ cho rẻ.
    · KHÔNG selector ⇒ TOÀN suite: KHÔNG đo lại ở đây. Chính `t125` đã đo (hai lượt con chạy `CO_AB`
      không selector, mỗi lượt là toàn suite). Chạy thêm một lượt toàn suite nữa ở đây là nhân ba chi
      phí mà không thêm phép đo nào.

    ĐỘT BIẾN LÀM CA NÀY ĐỎ: bỏ nhánh `if not tien_to or not cac_ca` trong `main()`; trả 0 thay cho
    `RC_CHON_CA_SAI`; in dòng tổng kết trước khi trả về.
    """
    nen = {k: v for k, v in os.environ.items() if k != "GITHUB_ACTOR"}

    def chay_con(*co):
        p = subprocess.run([sys.executable, str(Path(__file__).resolve()), *co],
                           capture_output=True, text=True, env=nen, timeout=180)
        return p.returncode, p.stdout, p.stderr

    rc, out, err = chay_con(CO_CHI_CA + "t01_")
    bang(rc == 0 and re.search(r"lease_publish: 1/1 đạt", out),
         f"prefix hợp lệ phải còn chạy đúng một ca: rc={rc}, stdout={out[-300:]!r}, stderr={err[-200:]!r}")

    rc, out, err = chay_con(CO_AB, CO_CHI_CA + "t01_")
    bang(rc == 0 and re.search(r"lease_publish: 1/1 đạt", out),
         f"đường CO_AB phải còn chạy ca: rc={rc}, stdout={out[-300:]!r}, stderr={err[-200:]!r}")

    for co, ten in ((CO_CHI_CA + "zzz_khong_co_ca_nao_ten_the_nay_", "không khớp ca nào"),
                    (CO_CHI_CA, "RỖNG")):
        rc, out, err = chay_con(co)
        bang(rc == RC_CHON_CA_SAI,
             f"selector {ten} phải trả rc={RC_CHON_CA_SAI}, đo được rc={rc}; "
             f"stdout={out[-300:]!r}, stderr={err[-300:]!r}")
        bang(not re.search(r"lease_publish: \d+/\d+ đạt", out + err),
             f"selector {ten} KHÔNG được in dòng tổng kết (đọc thành một kết quả): "
             f"stdout={out[-300:]!r}, stderr={err[-300:]!r}")


@ca
def t156_han_NGOAI_khong_nho_hon_tong_han_TRONG_va_duoi_tran_cung():
    """Hạn ngoài của t125 phải ≥ tổng hạn trong tiêu được hợp lệ, và < trần cứng (codex 11-09-2026, P2).

    Phần 1 đo SỐ HỌC trên hằng thật. Phần 2 là phản chứng THU NHỎ, dùng CHÍNH `_han_ngoai_toi_thieu`
    và CHÍNH `_mo_con_nhom_rieng`/`_giet_ca_cay`: ba "lint giả", mỗi lời gọi dưới hạn RIÊNG của nó,
    TỔNG vượt hạn ngoài kiểu cũ. Verdict đứng-một-mình và verdict lồng phải KHỚP với hạn dẫn xuất, và
    phải LỆCH với hạn kiểu cũ — không có chiều thứ hai thì không biết phép đo có răng.

    Vì sao thu nhỏ mà vẫn đúng: hàm dẫn xuất là hàm THUẦN của năm hạn, nên quan hệ nó bảo đảm không
    phụ thuộc thang thời gian. Đo thật ở thang 540 s sẽ tốn 9 phút mỗi lượt và vẫn chỉ đo đúng quan hệ ấy.

    ĐỘT BIẾN LÀM CA NÀY ĐỎ: ghi tay `AB_HAN_GIAY = 420`; bỏ `CD_HAN_TONG_GIAY` khỏi `T137_TRAN_GIAY`;
    nâng `AB_HAN_GIAY` lên quá `AB_TRAN_CUNG_GIAY` cho "khỏi treo".
    """
    bang(T137_TRAN_GIAY == AL_HAN_GIAY + SC_HAN_TONG_GIAY + CD_HAN_TONG_GIAY,
         f"trần t137 phải gồm ĐỦ ba hạn trong: {T137_TRAN_GIAY} vs "
         f"{AL_HAN_GIAY}+{SC_HAN_TONG_GIAY}+{CD_HAN_TONG_GIAY}")
    bang(AB_HAN_GIAY >= T137_TRAN_GIAY + AB_SUITE_DO_DUOC_GIAY,
         f"hạn ngoài {AB_HAN_GIAY}s phải ≥ trần t137 {T137_TRAN_GIAY}s + suite đã đo "
         f"{AB_SUITE_DO_DUOC_GIAY}s — nếu không, con bị giết dù mọi lệnh còn trong hạn riêng")
    bang(AB_HAN_GIAY > 540,
         f"hạn ngoài phải vượt 540 s (tổng hạn trong của riêng t137 mà cross-review đã đo): {AB_HAN_GIAY}")
    bang(AB_HAN_GIAY < AB_TRAN_CUNG_GIAY,
         f"hạn ngoài {AB_HAN_GIAY}s phải nằm DƯỚI trần cứng {AB_TRAN_CUNG_GIAY}s — nâng trần cho tới "
         f"khi hết treo là đổi cổng lấy sự im lặng")

    # ── phản chứng thu nhỏ
    tre, han_moi_goi, so_goi = 0.3, 1.0, 3
    ngoai_moi = _han_ngoai_toi_thieu(han_moi_goi, han_moi_goi * (so_goi - 1), 0.5, 0.5, 0.5)
    ngoai_cu = tre * so_goi - 0.1          # kiểu cũ: NHỎ HƠN tổng công việc hợp lệ của con
    ma_lint = "import sys,time\ntime.sleep(float(sys.argv[1]))\n"
    ma_con = ("import subprocess,sys\n"
              "for _ in range(int(sys.argv[3])):\n"
              "    r = subprocess.run([sys.executable,'-c',sys.argv[1],sys.argv[2]], timeout=float(sys.argv[4]))\n"
              "    assert r.returncode == 0\n"
              "print('LINT GIA XONG')\n")
    doi_so = [ma_lint, str(tre), str(so_goi), str(han_moi_goi)]
    nen = {k: v for k, v in os.environ.items() if k != "GITHUB_ACTOR"}

    # đứng-một-mình: từng lời gọi trong hạn riêng ⇒ ĐẠT
    t0 = time.monotonic()
    for _ in range(so_goi):
        r = subprocess.run([sys.executable, "-c", ma_lint, str(tre)], timeout=han_moi_goi)
        bang(r.returncode == 0, "lint giả đứng-một-mình phải rc=0")
    rieng = time.monotonic() - t0
    bang(rieng > ngoai_cu,
         f"phản chứng MẤT RĂNG: công việc hợp lệ {rieng:.2f}s không vượt hạn ngoài kiểu cũ "
         f"{ngoai_cu:.2f}s, nên ca này không đo được gì")

    def chay_long(han):
        with tempfile.TemporaryDirectory() as td:
            o, e = Path(td) / "o", Path(td) / "e"
            with open(o, "w", encoding="utf-8") as ow, open(e, "w", encoding="utf-8") as ew:
                p = _mo_con_nhom_rieng([sys.executable, "-c", ma_con, *doi_so], nen, ow, ew)
                qua_han = False
                try:
                    p.wait(timeout=han)
                except subprocess.TimeoutExpired:
                    qua_han = True
                    _giet_ca_cay(p)
            return qua_han, p.returncode, o.read_text(encoding="utf-8", errors="replace")

    qua_han, rc, out = chay_long(ngoai_moi)
    bang(not qua_han and rc == 0 and "LINT GIA XONG" in out,
         f"hạn ngoài DẪN XUẤT {ngoai_moi:.2f}s phải để con làm xong việc hợp lệ ({rieng:.2f}s): "
         f"qua_han={qua_han}, rc={rc}, out={out[-200:]!r}")
    qua_han_cu, rc_cu, _ = chay_long(ngoai_cu)
    bang(qua_han_cu,
         f"hạn ngoài kiểu CŨ {ngoai_cu:.2f}s phải giết con dù việc còn hợp lệ — không lệch thì ca này "
         f"không chứng minh vì sao cần dẫn xuất: qua_han={qua_han_cu}, rc={rc_cu}")

    # ── NGÂN SÁCH TỔNG phải ĐỘC LẬP VỚI SỐ LỆNH. Đây là vế mà `T137_TRAN_GIAY` đứng trên: nếu vòng
    # shellcheck cấp lại hạn cho từng thân sau khi ngân sách cạn thì trần thật là `ngân sách + n×hạn`,
    # và mọi con số dẫn xuất ở trên thành lời khai rộng hơn phép đo. Đo bằng HAI dãy dài khác nhau
    # trên CÙNG một ngân sách: thời gian phải xấp xỉ nhau, không nhân theo n.
    ngan_sach, tre_lenh = 0.6, 0.25
    lenh_cham = [sys.executable, "-c", ma_lint, str(tre_lenh)]
    do_thoi = {}
    for n in (4, 24):
        t0 = time.monotonic()
        het_tai = None
        try:
            _chay_day_lenh_trong_ngan_sach([lenh_cham] * n, ngan_sach)
        except HetNganSachDay as ex:
            het_tai = ex.chi_so
        except subprocess.TimeoutExpired:
            het_tai = -1
        do_thoi[n] = time.monotonic() - t0
        bang(het_tai is not None,
             f"dãy {n} lệnh × {tre_lenh}s phải tiêu hết ngân sách {ngan_sach}s và DỪNG, "
             f"đo được {do_thoi[n]:.2f}s mà không báo hết ngân sách")
    bang(do_thoi[24] < do_thoi[4] + ngan_sach + 1.0,
         f"trần của dãy TRÔI THEO SỐ LỆNH: 4 lệnh {do_thoi[4]:.2f}s vs 24 lệnh {do_thoi[24]:.2f}s — "
         f"ngân sách TỔNG phải cắt ở {ngan_sach}s bất kể n, nếu không thì `T137_TRAN_GIAY` là số bịa")


    # Các lệnh ngủ phía trên hết hạn TRONG run(). Cần đo riêng hết ngân sách GIỮA
    # hai lời gọi đã hoàn tất: nhánh HetNganSachDay không được đổi thành return/cấp lại hạn.
    from unittest import mock
    da_goi, het_tai = [], None
    def chay_xong(lenh, **kw):
        da_goi.append(lenh)
        return subprocess.CompletedProcess(lenh, 0, "", "")
    with mock.patch.object(time, "monotonic", side_effect=[0.0, 0.0, 1.0]):
        try:
            _chay_day_lenh_trong_ngan_sach([["lenh1"], ["lenh2"]], 0.6, chay=chay_xong)
        except HetNganSachDay as ex:
            het_tai = (ex.chi_so, ex.da_chay)
    bang(het_tai == (1, 1) and da_goi == [["lenh1"]],
         f"hết ngân sách GIỮA hai lệnh phải ném HetNganSachDay trước lệnh #1: "
         f"het_tai={het_tai}, da_goi={da_goi}")


@ca
def t159_t137_can_do_DU_ket_qua_va_dung_nhan_than_timeout():
    """Khóa consumer t137 bằng dãy đủ/thiếu và timeout thân thứ hai.

    Dùng workflow thật và actionlint thật; seam chỉ thay bộ chạy dãy shellcheck để
    tạo kết quả dở dang/timeout tất định. t137 thường vẫn chạy ShellCheck thật.
    Bỏ chốt len(ket), hoặc quay nhãn timeout về len(ket), phải làm CHÍNH ca này đỏ.
    """
    from unittest import mock

    def do(kieu):
        da_goi, loi = [], None
        def day_gia(cac_lenh, ngan_sach):
            da_goi.extend(cac_lenh)
            chot(len(cac_lenh) == 2, f"fixture t137 phải có hai thân shell: {cac_lenh}")
            if kieu == "treo":
                raise subprocess.TimeoutExpired(cac_lenh[1], ngan_sach)
            ket = [subprocess.CompletedProcess(l, 0, "", "") for l in cac_lenh]
            return ket if kieu == "du" else ket[:1]
        with mock.patch.dict(globals(), {"_chay_day_lenh_trong_ngan_sach": day_gia}):
            try:
                t137_M9_workflow_admission_hop_dong_tinh_va_actionlint_shellcheck()
            except TinHieuChotCa as ex:
                loi = str(ex)
        bang(len(da_goi) == 2, f"chưa tới consumer shellcheck ở t137: {loi}")
        return loi

    bang(do("du") is None, "t137 phải nhận đủ hai kết quả xanh")
    thieu = do("thieu")
    bang(thieu is not None and "shellcheck chỉ trả 1/2 kết quả" in thieu,
         f"t137 phải từ chối kết quả dở dang 1/2: {thieu!r}")
    treo = do("treo")
    bang(treo is not None and "shellcheck TREO trên thân run #1:" in treo,
         f"timeout lệnh thứ hai phải ghi run #1 từ ex.cmd: {treo!r}")


# --- packet #548: chốt nguồn duy nhất và evaluator tối giản cho ma trận CI Windows ---


def _kiem_tra_nguon_duy_nhat_os_ci(tep_hoac_dict) -> list[str]:
    """Quét ci.yml (hoặc dict giả lập): ĐỎ khi có bất kỳ job nào khai os: riêng ngoài needs.chuan-bi.outputs.os."""
    import yaml
    if isinstance(tep_hoac_dict, dict):
        wf = tep_hoac_dict
    else:
        wf = yaml.safe_load(Path(tep_hoac_dict).read_text(encoding="utf-8"))
    loi = []
    jobs = wf.get("jobs") or {}
    if "chuan-bi" not in jobs:
        loi.append("ci.yml thiếu job 'chuan-bi' làm nguồn duy nhất cho ma trận os")
        return loi
    for ten_job, cau_hinh in jobs.items():
        if ten_job == "chuan-bi":
            continue
        matrix = ((cau_hinh or {}).get("strategy") or {}).get("matrix") or {}
        if "os" in matrix:
            gia_tri_os = matrix["os"]
            if isinstance(gia_tri_os, str):
                if "needs.chuan-bi.outputs.os" not in gia_tri_os:
                    loi.append(f"job '{ten_job}' khai 'os:' riêng: {gia_tri_os!r} (không tham chiếu needs.chuan-bi.outputs.os)")
            else:
                loi.append(f"job '{ten_job}' khai 'os:' riêng bằng danh sách tĩnh: {gia_tri_os!r} (không tham chiếu needs.chuan-bi.outputs.os)")
    return loi


def _kiem_tra_outputs_ci_khong_boc_fromjson(wf_path_or_dict):
    """Outputs của job bắt buộc phải là chuỗi. Bọc fromJson/fromJSON hoặc chiếu mảng (.*.) sẽ làm Actions crash."""
    import yaml
    if isinstance(wf_path_or_dict, dict):
        d = wf_path_or_dict
    else:
        d = yaml.safe_load(wf_path_or_dict.read_text(encoding="utf-8")) or {}
    loi = []
    for ten_job, job in (d.get("jobs") or {}).items():
        outputs = (job or {}).get("outputs") or {}
        for k, v in outputs.items():
            v_str = str(v).lower()
            if "fromjson(" in v_str:
                loi.append(f"job '{ten_job}' output '{k}' bọc fromJson/fromJSON: {v!r} (outputs chỉ nhận chuỗi)")
            raw_v = str(v).strip()
            if re.fullmatch(r"\$\{\{\s*[\w.]+\.\*\.[\w.]+\s*\}\}", raw_v):
                loi.append(f"job '{ten_job}' output '{k}' chiếu mảng qua '.*.': {v!r} (trả sequence làm outputs crash)")
            if re.fullmatch(r"\$\{\{\s*needs\.\w+\.outputs\s*\}\}", raw_v):
                loi.append(f"job '{ten_job}' output '{k}' truyền đối tượng outputs: {v!r} (trả object làm outputs crash)")
    return loi


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


@ca
def t161_M3_chot_nguon_duy_nhat_ma_tran_ci():
    """M3, A2 & P1: Quét ci.yml:
    1. ĐỎ khi có bất kỳ job nào khai os: riêng ngoài needs.chuan-bi.outputs.os.
    2. ĐỎ khi outputs của bất kỳ job nào bọc fromJSON/fromJson (outputs chỉ nhận chuỗi, sequence làm Actions crash).
    Đột biến: workflow giả có job khai os riêng hoặc bọc fromJSON output => chốt phải bắt được.
    """
    wf_ci = HERE.parent / ".github" / "workflows" / "ci.yml"
    loi_that = _kiem_tra_nguon_duy_nhat_os_ci(wf_ci)
    bang(not loi_that, f"ci.yml thật có job lén khai os: riêng: {loi_that}")

    # Chốt P1: outputs của ci.yml thật không được bọc fromJson/fromJSON
    loi_output = _kiem_tra_outputs_ci_khong_boc_fromjson(wf_ci)
    bang(not loi_output, f"ci.yml thật có output bọc fromJson: {loi_output}")

    # Ca giả không lén: phải đạt
    wf_gia_sach = {
        "jobs": {
            "chuan-bi": {"outputs": {"os": "${{ (...) }}"}},
            "gate": {"strategy": {"matrix": {"os": "${{ fromJson(needs.chuan-bi.outputs.os) }}"}}},
            "gate-registry": {"strategy": {"matrix": {"os": "${{ fromJson(needs.chuan-bi.outputs.os) }}"}}},
        }
    }
    bang(_kiem_tra_nguon_duy_nhat_os_ci(wf_gia_sach) == [], "workflow giả hợp lệ bị từ chối")
    bang(_kiem_tra_outputs_ci_khong_boc_fromjson(wf_gia_sach) == [], "workflow giả hợp lệ bị từ chối ở outputs")

    # Ca giả có một job lén khai os: riêng (danh sách hoặc biểu thức riêng)
    wf_gia_len = {
        "jobs": {
            "chuan-bi": {"outputs": {"os": "${{ (...) }}"}},
            "gate": {"strategy": {"matrix": {"os": "${{ fromJson(needs.chuan-bi.outputs.os) }}"}}},
            "gate-len": {"strategy": {"matrix": {"os": ["ubuntu-latest", "windows-latest"]}}},
        }
    }
    loi_len = _kiem_tra_nguon_duy_nhat_os_ci(wf_gia_len)
    bang(len(loi_len) == 1 and "gate-len" in loi_len[0], f"chốt không bắt được job lén khai os: {loi_len}")

    # Đột biến P1: nếu có job bọc fromJSON vào output => chốt phải bắt được
    wf_gia_output_fromjson = {
        "jobs": {
            "chuan-bi": {"outputs": {"os": "${{ fromJSON('[\"ubuntu-latest\"]') }}"}}
        }
    }
    loi_output_dot_bien = _kiem_tra_outputs_ci_khong_boc_fromjson(wf_gia_output_fromjson)
    bang(len(loi_output_dot_bien) == 1 and "chuan-bi" in loi_output_dot_bien[0],
         f"chốt không bắt được output bọc fromJSON: {loi_output_dot_bien}")

    # Đột biến P3-MỚI: nếu có job chiếu mảng labels.*.name trực tiếp vào output => chốt phải bắt được
    wf_gia_proj = {
        "jobs": {
            "chuan-bi": {"outputs": {"os": "${{ github.event.pull_request.labels.*.name }}"}}
        }
    }
    loi_proj = _kiem_tra_outputs_ci_khong_boc_fromjson(wf_gia_proj)
    bang(len(loi_proj) == 1 and "chuan-bi" in loi_proj[0],
         f"chốt không bắt được output chiếu mảng .*. trực tiếp: {loi_proj}")


@ca
def t162_M4_evaluator_toi_gian_chuan_bi():
    """M4, A3 & A4: Evaluator tối giản fail-close cho biểu thức chuan-bi.
    Bốn ca rõ ràng (push master, PR thường, PR nhãn windows, workflow_dispatch).
    Đột biến A3: biểu thức chứa github.ref == 'refs/heads/master' => push master sinh 2 nền thay vì 1.
    Chốt fail-close A4: gặp biểu thức hình lạ (kể cả bọc fromJSON) bắt buộc phải in KHÔNG ĐO ĐƯỢC và raise ValueError.
    """
    import yaml
    wf_ci = HERE.parent / ".github" / "workflows" / "ci.yml"
    wf_data = yaml.safe_load(wf_ci.read_text(encoding="utf-8"))
    raw_expr = wf_data["jobs"]["chuan-bi"]["outputs"]["os"]

    c_push_master = {"event_name": "push", "ref": "refs/heads/master", "labels": []}
    c_pr_thuong = {"event_name": "pull_request", "ref": "refs/pull/1/merge", "labels": ["docs"]}
    c_pr_windows = {"event_name": "pull_request", "ref": "refs/pull/1/merge", "labels": ["windows"]}
    c_dispatch = {"event_name": "workflow_dispatch", "ref": "refs/heads/master", "labels": []}

    # A3: bảng 4 ca trên biểu thức thật
    r_push = _danh_gia_bieu_thuc_chuan_bi(raw_expr, c_push_master)
    r_pr = _danh_gia_bieu_thuc_chuan_bi(raw_expr, c_pr_thuong)
    r_pr_win = _danh_gia_bieu_thuc_chuan_bi(raw_expr, c_pr_windows)
    r_disp = _danh_gia_bieu_thuc_chuan_bi(raw_expr, c_dispatch)

    bang(r_push == ["ubuntu-latest"], f"push master phải chỉ chạy ubuntu-latest, nhận được: {r_push}")
    bang(r_pr == ["ubuntu-latest"], f"PR thường phải chỉ chạy ubuntu-latest, nhận được: {r_pr}")
    bang(r_pr_win == ["ubuntu-latest", "windows-latest"], f"PR nhãn windows phải chạy hai nền, nhận được: {r_pr_win}")
    bang(r_disp == ["ubuntu-latest", "windows-latest"], f"workflow_dispatch phải chạy hai nền, nhận được: {r_disp}")

    # Đột biến A3: đưa github.ref == 'refs/heads/master' trở lại => push master phải sinh 2 nền (làm ca đích ĐỎ)
    expr_dot_bien_ref = """(github.event_name == 'workflow_dispatch'
       || github.ref == 'refs/heads/master'
       || contains(github.event.pull_request.labels.*.name, 'windows'))
      && '["ubuntu-latest","windows-latest"]'
      || '["ubuntu-latest"]'"""
    r_mutant_push = _danh_gia_bieu_thuc_chuan_bi(expr_dot_bien_ref, c_push_master)
    bang(r_mutant_push == ["ubuntu-latest", "windows-latest"],
         f"đột biến có ref master phải sinh 2 nền khi push master: {r_mutant_push}")

    # A4: fail-close khi gặp biểu thức hình khác (ví dụ bọc fromJSON ở ngoài như lỗi P1)
    la_da_bat = False
    try:
        _danh_gia_bieu_thuc_chuan_bi("fromJSON('[\"ubuntu-latest\"]')", c_push_master)
    except ValueError as ex:
        if "KHÔNG ĐO ĐƯỢC" in str(ex):
            la_da_bat = True
    bang(la_da_bat, "evaluator phải fail-close (in KHÔNG ĐO ĐƯỢC và raise) khi gặp hình lạ (kể cả bọc fromJSON)")


# --- packet #541: giải git theo nền trên Windows và kiểm thử N1-N4 (Spec r2) ---


@ca
def t165_N1_giai_git_windows_program_files_va_fail_closed():
    """N1: Nền Windows giả, không ứng viên hợp lệ => Chan(RC_KHONG_XAC_DINH);
    có %ProgramFiles%\\Git\\cmd\\git.exe => trả đúng đường ấy, tuyệt đối, đã resolve.
    """
    import tempfile
    lp = _nap_cong()
    with tempfile.TemporaryDirectory(prefix="t165_") as td:
        cay = Path(td).resolve()
        pf_trong = cay / "PF_trong"
        pf_trong.mkdir()
        cwd_tam = cay / "cwd"
        cwd_tam.mkdir()

        # Cửa 1: không có ứng viên hợp lệ => ném Chan(RC_KHONG_XAC_DINH)
        rc, out = _ma_chan(lp, lp._git_exe_toi_thieu, nen="windows",
                           program_files=str(pf_trong), path="", cwd=str(cwd_tam))
        chot(rc == 12, f"N1: không có ứng viên hợp lệ phải rc=12, nhận: {rc}")
        chot("không thấy" in str(out), f"N1: thông điệp ném ra: {out!r}")

        # Cửa 2: có %ProgramFiles%\Git\cmd\git.exe => trả đúng đường tuyệt đối
        pf_co = cay / "ProgramFiles"
        cmd_dir = pf_co / "Git" / "cmd"
        cmd_dir.mkdir(parents=True)
        git_that = cmd_dir / "git.exe"
        git_that.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        git_that.chmod(0o755)

        duong = lp._git_exe_toi_thieu(nen="windows", program_files=str(pf_co), path="", cwd=str(cwd_tam))
        chot(duong == str(git_that.resolve()), f"N1: mong {git_that.resolve()}, được {duong}")
        chot(Path(duong).is_absolute(), f"N1: đường dẫn phải tuyệt đối: {duong}")


@ca
def t166_N2_giai_git_windows_loai_tru_cwd():
    """N2: Nền Windows giả:
    1. cwd chứa git.bat, git.py, git.exe => kết quả KHÔNG trỏ vào cwd (loại trừ cwd).
    2. Thư mục PATH ngoài cwd chỉ chứa git.bat/cmd/py (không có git.exe) => bị từ chối (P1-2 / P2-MỚI).
    3. Thư mục PATH ngoài cwd có git.exe hợp lệ => trả đúng đường tuyệt đối ấy.
    """
    import tempfile
    lp = _nap_cong()
    with tempfile.TemporaryDirectory(prefix="t166_") as td:
        cay = Path(td).resolve()
        cwd_fake = cay / "fake_cwd"
        cwd_fake.mkdir()
        bat = cwd_fake / "git.bat"
        bat.write_text("@echo off\n", encoding="utf-8")
        py = cwd_fake / "git.py"
        py.write_text("print('fake')\n", encoding="utf-8")
        exe_cwd = cwd_fake / "git.exe"
        exe_cwd.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        exe_cwd.chmod(0o755)

        pf_rong = cay / "pf_rong"
        pf_rong.mkdir()

        # Cửa 1: Khi PATH trỏ vào cwd (chứa git.bat, git.py, git.exe) => kết quả KHÔNG được trỏ vào cwd
        kq = lp._git_windows(path=str(cwd_fake), program_files=str(pf_rong), cwd=str(cwd_fake))
        chot(kq is None, f"N2 cửa 1: kết quả phải là None (loại trừ cwd), nhưng lại nhận: {kq}")

        rc, out = _ma_chan(lp, lp._git_exe_toi_thieu, nen="windows",
                           path=str(cwd_fake), program_files=str(pf_rong), cwd=str(cwd_fake))
        chot(rc == 12, f"N2 cửa 1: phải ném Chan(12) khi chỉ có git.* trong cwd, nhận: {rc}")

        # Cửa 2 (P2-MỚI): Thư mục PATH ngoài cwd chỉ có git.bat, git.cmd, git.py (không có git.exe)
        path_bat = cay / "path_ngoai_chi_co_bat"
        path_bat.mkdir()
        (path_bat / "git.bat").write_text("@echo off\n", encoding="utf-8")
        (path_bat / "git.cmd").write_text("@echo off\n", encoding="utf-8")
        (path_bat / "git.py").write_text("print('fake')\n", encoding="utf-8")

        kq_bat = lp._git_windows(path=str(path_bat), program_files=str(pf_rong), cwd=str(cwd_fake))
        chot(kq_bat is None, f"N2 cửa 2: PATH ngoài cwd chỉ có git.bat/cmd/py phải bị từ chối, nhận: {kq_bat}")

        rc_bat, out_bat = _ma_chan(lp, lp._git_exe_toi_thieu, nen="windows",
                                   path=str(path_bat), program_files=str(pf_rong), cwd=str(cwd_fake))
        chot(rc_bat == 12, f"N2 cửa 2: phải ném Chan(12) khi PATH ngoài chỉ có git.bat/cmd/py, nhận: {rc_bat}")

        # Cửa 3: Thư mục PATH ngoài cwd có git.exe hợp lệ => phải nhận đúng git.exe đó
        path_exe = cay / "path_ngoai_co_exe"
        path_exe.mkdir()
        git_exe_that = path_exe / "git.exe"
        git_exe_that.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        git_exe_that.chmod(0o755)

        kq_exe = lp._git_windows(path=f"{path_bat}{os.pathsep}{path_exe}",
                                program_files=str(pf_rong), cwd=str(cwd_fake))
        chot(kq_exe == str(git_exe_that.resolve()),
             f"N2 cửa 3: mong nhận {git_exe_that.resolve()}, nhận được: {kq_exe}")


@ca
def t167_N3_giai_git_windows_loai_tru_system_root_va_chan_doan():
    """N3: Ứng viên dưới %SystemRoot% bị loại; và khi bước %ProgramFiles% không phân giải,
    chẩn đoán ghi KHÔNG_ĐO_ĐƯỢC chứ không im lặng rơi xuống bước 3.
    """
    import tempfile
    lp = _nap_cong()
    with tempfile.TemporaryDirectory(prefix="t167_") as td:
        cay = Path(td).resolve()
        fake_sr = cay / "Windows"
        s32 = fake_sr / "System32"
        s32.mkdir(parents=True)
        git_sr = s32 / "git.exe"
        git_sr.write_text("#!/bin/sh\n", encoding="utf-8")
        git_sr.chmod(0o755)

        fake_pf = cay / "EmptyPF"
        fake_pf.mkdir()
        fake_cwd = cay / "EmptyCWD"
        fake_cwd.mkdir()

        # Cửa (a): Ứng viên dưới %SystemRoot% phải bị loại
        chan_doan = []
        kq_sr = lp._git_windows(path=str(s32), system_root=str(fake_sr),
                                program_files=str(fake_pf), cwd=str(fake_cwd),
                                chan_doan=chan_doan)
        chot(kq_sr is None, f"N3a: ứng viên dưới SystemRoot phải bị loại, nhưng nhận: {kq_sr}")

        rc_sr, _ = _ma_chan(lp, lp._git_exe_toi_thieu, nen="windows",
                            path=str(s32), system_root=str(fake_sr),
                            program_files=str(fake_pf), cwd=str(fake_cwd))
        chot(rc_sr == 12, f"N3a: phải ném Chan 12 khi ứng viên duy nhất nằm dưới SystemRoot, nhận: {rc_sr}")

        # Cửa (b): Khi bước %ProgramFiles% không phân giải, chẩn đoán ghi KHÔNG_ĐO_ĐƯỢC
        chot(any("KHÔNG_ĐO_ĐƯỢC" in str(msg) for msg in chan_doan),
             f"N3b: chẩn đoán phải ghi KHÔNG_ĐO_ĐƯỢC khi ProgramFiles không phân giải, nhận: {chan_doan}")


@ca
def t168_N4_posix_khong_hoi_quy_usr_bin_git():
    """N4: POSIX không hồi quy: trên ubuntu-latest, _git_exe_toi_thieu() vẫn trả /usr/bin/git.
    Đột biến: đổi nhánh POSIX sang hằng số khác => ĐỎ.
    """
    import tempfile
    lp = _nap_cong()
    with tempfile.TemporaryDirectory(prefix="t168_") as td:
        cay = Path(td).resolve()
        fake_bin = cay / "usr" / "bin"
        fake_bin.mkdir(parents=True)
        # Tạo cả git và git.exe để fixture hoạt động đúng khi chạy trên cả Linux và Windows runner
        p_git = fake_bin / "git"
        p_git_exe = fake_bin / "git.exe"
        p_git.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        p_git_exe.write_text("#!/bin/sh\nexit 0\n", encoding="utf-8")
        p_git.chmod(0o755)
        p_git_exe.chmod(0o755)
        fake_git = p_git_exe if os.name == "nt" else p_git

        # Giả lập POSIX với path trỏ vào fake_bin
        duong = lp._git_exe_toi_thieu(nen="posix", path=str(fake_bin))
        chot(duong == str(fake_git.resolve()), f"N4: mong {fake_git.resolve()}, được {duong}")

        # Nếu trên môi trường POSIX thật (không phải Windows) có /usr/bin/git:
        if os.name != "nt" and Path("/usr/bin/git").is_file():
            duong_that = lp._git_exe_toi_thieu(nen="posix")
            chot(duong_that == str(Path("/usr/bin/git").resolve()),
                 f"N4: trên POSIX thật mong /usr/bin/git, được {duong_that}")

        # Đột biến: đổi nhánh POSIX sang hằng số khác không tồn tại
        rc_mut, out_mut = _ma_chan(lp, lp._git_exe_toi_thieu, nen="posix", path=str(cay / "nonexistent_bin"))
        chot(rc_mut == 12, f"N4: mutant đổi path POSIX sang thư mục khác phải ném Chan 12, nhận: {rc_mut}")


@ca
def t169_N8_cong_cu_git_chi_nhan_git_exe():
    """N8 (M3): CONG_CU_GIT chỉ nhận git.exe; .bat/.cmd/.py/.txt bị từ chối; có đối chứng dương."""
    lp = _nap_cong()
    with San() as s:
        d, cw, pf = s / "ngoai", s / "cwd", s / "pf"
        d.mkdir(); cw.mkdir(); pf.mkdir()
        f_exe = d / "git.exe"; f_exe.write_text("x")
        kq_duong = lp._git_windows(cong_cu_git=str(f_exe), path="", program_files=str(pf), cwd=str(cw))
        chot(kq_duong == str(f_exe.resolve()), f"git.exe phải nhận: {kq_duong}")
        for ten in ("git.bat", "git.cmd", "git.py", "khong-phai-git.txt"):
            f_bad = d / ten; f_bad.write_text("x")
            kq = lp._git_windows(cong_cu_git=str(f_bad), path="", program_files=str(pf), cwd=str(cw))
            chot(kq is None, f"{ten} phải bị từ chối ở bước 1 CONG_CU_GIT: {kq}")


@ca
def t170_N9_path_boc_nhay_kep_va_khoang_trang():
    """N9 (M4): PATH bọc nháy kép hoặc có khoảng trắng thừa được nhận; mục rỗng bỏ qua."""
    lp = _nap_cong()
    with San() as s:
        d, cw, pf = s / "thu muc co cach", s / "cwd", s / "pf"
        d.mkdir(); cw.mkdir(); pf.mkdir()
        (d / "git.exe").write_text("x")
        kq1 = lp._git_windows(path=str(d), program_files=str(pf), cwd=str(cw))
        chot(kq1 == str((d / "git.exe").resolve()), f"PATH không nháy phải nhận: {kq1}")
        kq2 = lp._git_windows(path=f'"{d}"', program_files=str(pf), cwd=str(cw))
        chot(kq2 == str((d / "git.exe").resolve()), f"PATH có nháy kép phải nhận: {kq2}")
        path_hon_hop = f'   ;  "{d}"  ;  ;  '
        kq3 = lp._git_windows(path=path_hon_hop, program_files=str(pf), cwd=str(cw), phan_cach=";")
        chot(kq3 == str((d / "git.exe").resolve()), f"PATH có khoảng trắng và mục rỗng phải nhận: {kq3}")


@ca
def t171_N10_path_dung_DUNG_dau_phan_cach_duoc_truyen():
    """N10 (M5): phép tách PATH dùng ĐÚNG dấu được truyền, KHÔNG suy từ NỘI DUNG chuỗi.

    BẢN TRƯỚC ĐỎ TRÊN WINDOWS vì FIXTURE, không vì mã: nó ghép `f"{la}:{d}"` từ đường TUYỆT
    ĐỐI rồi truyền `phan_cach=":"`. Trên Windows dấu ấy là ký tự Ổ ĐĨA — đo 19-09-2026, tách
    "C:/x/a:C:/x/b" theo ":" ra ['C','/x/a','C','/x/b'], thư mục chứa `git.exe` KHÔNG nằm
    trong đó. Cùng họ hằng chỉ-POSIX của `t136`, đổi cửa: hằng ĐƯỜNG DẪN thành hằng DẤU PHÂN
    CÁCH; `t173` nay canh cả hai. Nay dùng dấu không đụng cú pháp đường dẫn nền nào nên chạy
    được CẢ HAI nền.

    ĐỘT BIẾN LÀM CA NÀY ĐỎ: `sep = ";" if ";" in path_val else os.pathsep` — suy từ nội dung.
    """
    lp = _nap_cong()
    with San() as s:
        la, d, cw, pf = s / "co;dau-cham-phay", s / "dung", s / "cwd", s / "pf"
        la.mkdir(); d.mkdir(); cw.mkdir(); pf.mkdir()
        (d / "git.exe").write_text("x")
        mong = str((d / "git.exe").resolve())

        kq = lp._git_windows(path=f"{la}{PHAN_CACH_THU_N10}{d}", program_files=str(pf),
                             cwd=str(cw), phan_cach=PHAN_CACH_THU_N10)
        chot(kq == mong,
             f"phải tách theo {PHAN_CACH_THU_N10!r} đã truyền, không suy từ ';' trong tên: {kq}")

        # ĐỐI CHỨNG DƯƠNG — thiếu nó thì một hàm luôn trả None cũng qua được chiều trên.
        d2 = s / "khong-dau"; d2.mkdir(); (d2 / "git.exe").write_text("x")
        kq2 = lp._git_windows(path=str(d2), program_files=str(pf), cwd=str(cw),
                              phan_cach=PHAN_CACH_THU_N10)
        chot(kq2 == str((d2 / "git.exe").resolve()), f"đối chứng dương: {kq2}")

        # Vế POSIX: chỉ ở đó ':' là dấu phân cách THẬT và không đụng ký tự ổ đĩa. Trên
        # Windows vế này KHÔNG dựng được — khai thẳng thay vì để ĐỎ giả.
        if os.pathsep == ":":
            kq3 = lp._git_windows(path=f"{la}:{d}", program_files=str(pf), cwd=str(cw),
                                  phan_cach=":")
            chot(kq3 == mong, f"posix: không được tách theo ';' khi phan_cach=':': {kq3}")


@ca
def t172_N11_chan_doan_chuyen_kenh_stderr_0_byte():
    """N11 (M6): Chuyển kênh stderr sang chan_doan (0 byte khi có chan_doan, ghi stderr khi None)."""
    import io
    lp = _nap_cong()
    with San() as s:
        cw, pf = s / "cwd", s / "pf"
        cw.mkdir(); pf.mkdir()
        buf = io.StringIO(); old_err = sys.stderr; ds = []
        try:
            sys.stderr = buf
            kq = lp._git_windows(path="", program_files=str(pf), cwd=str(cw), chan_doan=ds)
            chot(kq is None and len(buf.getvalue()) == 0, f"stderr phải 0 byte khi có chan_doan: {buf.getvalue()!r}")
            chot(len(ds) > 0 and "KHÔNG_ĐO_ĐƯỢC" in ds[0], f"ds phải nhận thông báo chẩn đoán: {ds}")
        finally:
            sys.stderr = old_err
        buf2 = io.StringIO()
        try:
            sys.stderr = buf2
            kq = lp._git_windows(path="", program_files=str(pf), cwd=str(cw), chan_doan=None)
            chot(kq is None and len(buf2.getvalue()) > 0 and "KHÔNG_ĐO_ĐƯỢC" in buf2.getvalue(), "stderr phải có thông báo")
        finally:
            sys.stderr = old_err


@ca
def t173_N12_hang_fixture_dung_tren_CA_HAI_nen():
    """N12 (M7): hằng trong fixture phải đúng CẢ HAI nền — đường dẫn VÀ dấu phân cách.

    Bản trước chỉ canh hằng ĐƯỜNG DẪN; cùng lớp lỗi thoát qua cửa khác (`t171` ghép PATH bằng
    hằng ":"). Nay đóng theo LỚP, hai cửa. ĐỘT BIẾN: sentinel về "/khong/co/git" (cửa 1) HOẶC
    `PHAN_CACH_THU_N10` về ":" (cửa 2).
    """
    from pathlib import PurePosixPath, PureWindowsPath

    s = "//khong-co/git"                                    # cửa 1 — hằng ĐƯỜNG DẪN
    chot(PurePosixPath(s).is_absolute() and PureWindowsPath(s).is_absolute(),
         f"Sentinel {s!r} phải tuyệt đối trên cả PurePosixPath và PureWindowsPath")

    chot(PHAN_CACH_THU_N10 != ":",                          # cửa 2 — hằng DẤU PHÂN CÁCH
         "dấu phân cách fixture KHÔNG được là ':' — đường tuyệt đối Windows mang dấu hai chấm "
         f"của ổ đĩa nên chuỗi tự cắt nát; đang là {PHAN_CACH_THU_N10!r}")
    mau = "C:/x/a" + PHAN_CACH_THU_N10 + "C:/x/b"
    chot(mau.split(PHAN_CACH_THU_N10) == ["C:/x/a", "C:/x/b"],
         f"ghép/tách bằng {PHAN_CACH_THU_N10!r} phải giữ nguyên đường Windows: "
         f"{mau.split(PHAN_CACH_THU_N10)}")


# ── #579 — THỨ TỰ trong `kiem_github` là NỘI DUNG, không phải chi tiết cài đặt ──────────
# Năm ca dưới đây phủ ma trận 2×2 (hạn × dấu) cộng một ca miền. `_lease_579` dựng đúng
# một lease tối thiểu; `_do_kiem_github` trả MỘT mã thoát. Số lời gọi GitHub — thứ phân biệt
# "tiền kiểm chặn" với "chuỗi cũ chặn" mà mã thoát không phân biệt được — CHỈ đọc qua cửa
# `_do_kiem_github_dem`, nơi chốt CẢ vế kết quả (xem docstring `_do_kiem_github`).

def _lease_579(**doi):
    mac_dinh = {"lease_id": "wp579-thu", "packet_issue": 55}
    mac_dinh.update(doi)          # ca miền cần GHI ĐÈ `packet_issue`, không phải thêm vào
    return lease_mau(**mac_dinh)


def _do_kiem_github(lease, co_dau: bool, **k):
    """Gọi `kiem_github` với GitHub giả; trả MỘT mã thoát (`0` nghĩa là không ném).

    CỐ Ý KHÔNG TRẢ SỐ LỜI GỌI — và đó là bản vá kiến trúc của lượt 6, không phải một lần
    dọn dẹp. Bản trước trả `(ma, so_loi_goi)`, nên một ca chỉ việc lấy vế thứ hai rồi chốt
    trên nó mà quên vế thứ nhất; đúng như thế đã xảy ra ở vế `lease_id` của `t178` và làm
    đột biến `R_probe` SỐNG 177/177. Nay muốn chốt số lời gọi thì **bắt buộc** đi qua
    `_do_kiem_github_dem`, mà cửa ấy chốt CẢ HAI vế. Lỗ chết theo hình dạng hàm, không
    theo một chốt thêm ở đúng chỗ reviewer chỉ.
    """
    gh, _ = _dung_gh_579(lease, co_dau)
    ex, _mod = _goi_lop_gh(gh, "kiem_github", lease, env_them=ENV_GITHUB, **k)
    return 0 if ex is None else ex.ma


def _dung_gh_579(lease, co_dau: bool):
    """Dựng `GhGia` cho bộ ca #579. TÁCH RA để đường CÓ đếm và đường KHÔNG đếm dùng CHUNG
    một fixture — hai bản fixture song song là hai bản sẽ trôi lệch, và bên quên cập nhật
    chính là bên đẩy lọt."""
    dau = "**Lease `" + str(lease.get("lease_id", "")) + "`**"
    than = dau + " — bản chiếu" if co_dau else "khong lien quan"
    # Khoá comment phải theo ĐÚNG `packet_issue` của lease, không ghim cứng 55.
    # Cross-review lượt 2 bắt (`github-fixture-hardcodes-issue`): bản trước ghim 55, nên một
    # lease khai `packet_issue=579` với `co_dau=True` thật ra được thử như KHÔNG CÓ DẤU —
    # đo được `(rc=0, 3 lời gọi)` qua helper so với `(rc=9, 1 lời gọi)` khi gọi thẳng.
    # Các ca hiện hành đều dùng 55 nên KHÔNG ca nào đang xanh giả; đây là cái bẫy cho ca sau.
    # Chỉ suy khoá khi `packet_issue` là số nguyên HỢP LỆ — ca miền sai kiểu phải đi tới mã
    # sản phẩm, không được để chính fixture chặn trước (ép `int()` ở đây sẽ tạo tín dụng giả).
    so = lease.get("packet_issue")
    khoa = so if isinstance(so, int) and not isinstance(so, bool) else 55
    return GhGia(comments={khoa: [{"id": 7, "body": than,
                                   "user": {"login": "github-actions[bot]"}}]}), khoa


@ca
def t174_het_han_ma_DA_co_dau_thi_bo_qua_chu_khong_ket_toi_het_han():
    """A1 — lease ĐÃ ĐĂNG rồi mới HẾT HẠN phải ra `rc=9` (bỏ qua), không phải `rc=8`.

    Đây là hình dạng đã giết hai lượt `ops — đăng lease bằng git` ngày 20-09-2026
    (`35519177197` của #568 và `35519243379` của #566): cả hai ĐỎ SAU KHI lease mới đã
    đăng xong, tức việc chính đã thành và chỉ cái đuôi gãy. Nguyên nhân là THỨ TỰ —
    `kiem()` ném `rc=8` cho lease hết hạn trước khi chốt `rc=9` kịp chạy.

    Đo trên nền `a1bbdc10` (trước bản vá): hình dạng này cho `rc=8`.

    ĐỘT BIẾN LÀM CA NÀY ĐỎ: đưa `_do_dau_da_dang` về SAU `kiem()` trong `kiem_github`
    (tức khôi phục thứ tự cũ) ⇒ nhận 8 thay vì 9. Ca so MÃ THOÁT, không so chuỗi thông
    điệp — bài học #355/#359: một `except` đổi kiểu giả được chuỗi, không giả được mã.
    """
    ma = _do_kiem_github(_lease_579(lease_expires_at_utc=khi_truoc(48)), co_dau=True)
    chot(ma == RC_DA_DANG,
         f"lease ĐÃ ĐĂNG rồi mới hết hạn phải cho rc={RC_DA_DANG} (bỏ qua), được rc={ma}. "
         f"rc={RC_NOI_DUNG} nghĩa là `kiem()` vẫn chạy trước và chốt 'đã đăng' lại bị che.")


@ca
def t175_het_han_ma_KHONG_co_dau_thi_van_la_het_han():
    """A2 — nửa BÙ của `t174`: hết hạn mà CHƯA TỪNG đăng thì vẫn phải `rc=8`.

    Chống hồi quy #195 theo chiều ngược lại. Bản vá của #579 đảo thứ tự, và cách hỏng dễ
    thấy nhất của một bản vá như vậy là trả `rc=9` VÔ ĐIỀU KIỆN — lúc đó mọi lease chết
    đều được "bỏ qua" êm, và cổng chống đăng lease chết biến mất.

    CẶP `t174`/`t175` PHẢI ĐỎ NGƯỢC CHIỀU NHAU — mỗi đột biến đích làm ĐÚNG MỘT trong hai ca
    đỏ, và hai đột biến cho hai ca KHÁC NHAU. Đo (cross-review codex lượt 3): đưa phép dò xuống
    sau `kiem()` ⇒ TRONG CẶP chỉ `t174` đỏ; cho phép dò ném `RC_DA_DANG` vô điều kiện ⇒ TRONG CẶP
    chỉ `t175` đỏ. Hai tập ca đỏ khác nhau là bằng chứng cặp này PHÂN BIỆT được hai lỗi.
    Phạm vi của câu trên là CẶP, không phải cả miền. Tập đỏ đầy đủ trên `t174`–`t184`, đo bằng
    công cụ công thức (bản sao, phân hạng bằng `TinHieuChotCa`, 24-09): dò sau `kiem()` ⇒
    `{t174, t182}`; ném 9 vô điều kiện ⇒ `{t175, t177, t178, t179, t180, t181, t183, t184}`. Dấu hiệu bộ TƯƠNG ĐƯƠNG
    là điều ngược lại: mọi đột biến đều làm CẢ HAI cùng đỏ (hoặc cùng xanh). (Bản trước viết
    ngược nghĩa câu này.)

    ĐỘT BIẾN LÀM CA NÀY ĐỎ: cho `_do_dau_da_dang` ném `Chan(RC_DA_DANG)` không cần dấu.
    """
    ma = _do_kiem_github(_lease_579(lease_expires_at_utc=khi_truoc(48)), co_dau=False)
    chot(ma == RC_NOI_DUNG,
         f"lease hết hạn mà CHƯA TỪNG đăng phải cho rc={RC_NOI_DUNG}, được rc={ma}. "
         f"rc={RC_DA_DANG} ở đây nghĩa là cổng bỏ qua một lease chết — đúng bệnh #195.")


@ca
def t176_con_han_ma_DA_co_dau_van_bo_qua_nhu_cu():
    """A3 — hành vi CŨ không được đổi: còn hạn + đã có dấu vẫn `rc=9`.

    Vế này của chú thích `t32` vốn ĐÚNG (xem docstring `t32`), và bản vá phải giữ nguyên.
    Đo cả trên nền `a1bbdc10` lẫn ứng viên: cùng `rc=9`.

    ĐỘT BIẾN LÀM CA NÀY ĐỎ: bỏ hẳn tiền kiểm `_do_dau_da_dang` VÀ bỏ `_kiem_comment_da_co`
    khỏi chuỗi sau — tức gỡ cả hai cửa chống đăng trùng.
    """
    ma = _do_kiem_github(_lease_579(), co_dau=True)
    chot(ma == RC_DA_DANG,
         f"còn hạn + đã có dấu phải cho rc={RC_DA_DANG}, được rc={ma} — chống đăng trùng đã hỏng")


@ca
def t177_con_han_KHONG_dau_thi_MOI_CHOT_cua_kiem_van_phai_chay():
    """A4 — đường KHÔNG-CÓ-DẤU không được đổi một mã thoát nào.

    Đây là chốt đắt nhất của packet: dò dấu TRƯỚC nghĩa là với lease ĐÃ ĐĂNG, các chốt của
    `kiem()` (tự cấp, neo prompt, trường bắt buộc) KHÔNG còn soi nó trên đường này — giá đã
    khai trong docstring `kiem_github`. Cái giá ấy chỉ chấp nhận được nếu đường KHÔNG-CÓ-DẤU
    vẫn chạy đủ chốt. Ca này đo đúng điều đó, bằng BỐN hình dạng: lease sạch (`RC_OK`) và BA
    ca tiêm cho BA mã thoát KHÁC NHAU (`RC_TU_CAP`, `RC_NEO`, `RC_NOI_DUNG`).

    ĐỘT BIẾN LÀM CA NÀY ĐỎ: cho phép dò ném `Chan(RC_DA_DANG)` cả khi đã dò XONG mà KHÔNG thấy
    dấu (thêm một `raise` ngay sau `_kiem_comment_da_co` trong `try` của `_do_dau_da_dang`) ⇒
    cả bốn mã đều thành 9. ĐÃ CHẠY: giết `t177`. Bản trước viết "cho tiền kiểm NUỐT cả bốn
    hình dạng" — đọc theo nghĩa đổi hai nhánh `except` thành ném 9 thì công thức ấy SỐNG ở
    `t177` (đường không-dấu không đi qua nhánh `except` nào); soát lại khi vá lượt 7.
    """
    ma = _do_kiem_github(_lease_579(), co_dau=False)
    chot(ma == RC_OK, f"lease sạch, còn hạn, chưa đăng mà bị chặn: rc={ma}")

    ma = _do_kiem_github(_lease_579(granted_by="codex"), co_dau=False)
    chot(ma == RC_TU_CAP, f"tự cấp phải cho rc={RC_TU_CAP}, được rc={ma}")

    ma = _do_kiem_github(_lease_579(prompt_path="ops/prompts/p.md"), co_dau=False)
    chot(ma == RC_NEO, f"neo prompt không kiểm được phải cho rc={RC_NEO}, được rc={ma}")

    thieu = _lease_579()
    del thieu["granted_by"]
    ma = _do_kiem_github(thieu, co_dau=False)
    chot(ma == RC_NOI_DUNG, f"thiếu trường bắt buộc phải cho rc={RC_NOI_DUNG}, được rc={ma}")


@ca
def t178_tien_kiem_mien_chan_TRUOC_khi_cham_mang():
    """A5/M7 — `_tien_kiem_mien_dang` fail-close, và PHẠM VI THẬT của nó, đã ĐO.

    Ba ca âm đều cho `rc=8` và KHÔNG ngoại lệ trần nào thoát ra. Nhưng chỉ nói thế là khai
    RỘNG HƠN phép đo, nên ghi cho đúng — đột biến gỡ hẳn `_tien_kiem_mien_dang`:

        thiếu `lease_id`        -> rc=8  KHÔNG đổi   (bộ tương đương)
        thiếu `packet_issue`    -> rc=8  KHÔNG đổi   (bộ tương đương)
        `packet_issue` SAI KIỂU -> rc=9  ĐỔI, và đổi NGUY HIỂM

    Hai ca đầu không đổi vì `_do_dau_da_dang` vốn NUỐT mọi ngoại lệ không phải `RC_DA_DANG`:
    `KeyError` chết ngay đó rồi `kiem()` dựng lại `rc=8`. Chúng đo CÁI NUỐT, không đo hàm ấy.

    Thứ hàm ấy thật sự đóng là ca thứ BA: `packet_issue: "55"` (chuỗi) vẫn dựng được URL
    `issues/55/comments` hợp lệ, nên phép dò thấy dấu và trả `rc=9` — một lease SAI KIỂU
    được cấp đường "đã đăng, bỏ qua" và NÉ SẠCH mọi chốt của `kiem()`.

    Nên ca này đo thêm SỐ LỜI GỌI GitHub, thứ mà mã thoát không phân biệt được: tiền kiểm
    chặn trước khi chạm mạng ⇒ **0** lời gọi. Đó là răng riêng của ca thứ ba.

    CA `bool` NAY DA DO — và nó là ca DUY NHẤT giữ răng cho chốt `isinstance(so, bool)`.
    Cross-review codex lượt 1 dựng đột biến G (gỡ đúng điều kiện `bool` ấy, giữ nguyên mọi
    thứ khác) và nó **SỐNG SÓT 172/172**: ba ca cũ đều không chạm nhánh bool, vì với chuỗi
    `"55"` thì `not isinstance(so, int)` đã đủ ném. Đó là khoảng TRỐNG của bộ test — đúng
    thứ docstring bản trước tự khai là "KHÔNG ĐO" rồi để nguyên.

    `packet_issue: True` lọt phép kiểm kiểu ngây thơ vì `isinstance(True, int)` là `True`,
    rồi thành `issues/True/comments` trên URL. Đột biến G làm ca này ĐỎ qua SỐ LỜI GỌI
    (0 -> 1), không qua mã thoát — mã thoát vẫn là 8 ở cả hai bên.

    TRỤC `lease_id` SAI KIỂU — THÊM Ở LƯỢT 5, và nó đóng một đột biến SỐNG SÓT.

    Cross-review lượt 4 dựng đột biến **`L`** (gỡ chốt `lease_id` khỏi `_tien_kiem_mien_dang`)
    và nó **sống `176/176`**. Reviewer KHÔNG thổi thành P2, vì theo luật "đừng tự soạn nội dung
    tấn công" họ chỉ có đầu vào THIẾU `lease_id` lấy nguyên từ ca này — mà đầu vào ấy là **bộ
    tương đương** (xem bảng trên). Họ mô tả đúng hình dạng còn thiếu và giao điều phối đo hộ.

    Phiên điều phối đo, và `L` **KHÔNG** phải bộ tương đương. Sáu hình dạng SAI KIỂU của
    `lease_id`, đo trực tiếp qua `kiem_github` với một `GOI_GH` giả đếm lời gọi:

        hình dạng                     nền          L
        None · [] · {} · True · 1.5 · b"x"
          mã thoát                    rc=8         rc=8      <- GIỐNG HỆT
          số lời gọi GitHub           0            1         <- KHÁC

    VÀ HAI BẢN NHÁP ĐẦU CỦA CÁC VẾ ẤY TỰ SẬP ĐÚNG LỚP CHÚNG ĐANG ĐO — cả hai ĐỎ ngay trên
    NỀN, vì cả hai chốt trên một đại lượng MÙ. Chi tiết ở chú thích ngay tại vòng lặp.

    Bài học, lần thứ hai trong cùng packet sau `t184` vế (b): **khi một trục có đại lượng MÙ
    và một đại lượng CÓ RĂNG, chốt phải nằm trên cái CÓ RĂNG, và phải đo ở ĐÚNG ĐƠN VỊ mà
    chốt sản phẩm bảo vệ.** Đo ở đơn vị cao hơn (cổng tổng) thì lời gọi của thứ khác trộn
    vào và phép đo mất sạch sức phân biệt.

    Tức `L` sống sót vì **mọi ca cũ chốt trên `rc`, mà `rc` mù đúng chỗ này** — y hệt lý do
    đột biến `G` từng sống: cả hai đổi thứ mã thoát không nói được. Và hậu quả thật là thứ
    docstring của `_tien_kiem_mien_dang` tự khai làm lý do tồn tại: một lease hỏng miền được
    cho phép **CHẠM MẠNG**.

    Ba vế dưới đây khoá trục ấy. Chúng KHÔNG thay bốn vế trên: bốn vế kia đo trục
    `packet_issue`, ba vế này đo trục `lease_id`, và `L` chỉ chết ở trục thứ hai.
    """
    thieu_id = _lease_579()
    del thieu_id["lease_id"]
    thieu_so = _lease_579()
    del thieu_so["packet_issue"]

    for nhan, lease in (("thiếu `lease_id`", thieu_id),
                        ("thiếu `packet_issue`", thieu_so),
                        ("`packet_issue` sai kiểu", _lease_579(packet_issue="55")),
                        ("`packet_issue` là `bool`", _lease_579(packet_issue=True))):
        _do_kiem_github_dem(lease, True, RC_NOI_DUNG, 0, nhan)

    # TRỤC `lease_id` SAI KIỂU — ba hình dạng, mỗi hình dạng một lý do khác nhau để lọt.
    # Xem docstring: đây là thứ duy nhất giết được đột biến `L`, và nó giết bằng SỐ LỜI GỌI
    # chứ không bằng mã thoát (mã thoát là 8 ở cả hai bên — đã đo).
    # ĐO THẲNG `_do_dau_da_dang`, KHÔNG đo `kiem_github` — và hai bản nháp trước đã sai đúng
    # chỗ này, cả hai lần đều ĐỎ NGAY TRÊN NỀN. Ghi lại vì cái sai ấy thuộc đúng lớp ca này đo.
    #
    #   nháp 1  chốt `ma == RC_NOI_DUNG`, `co_dau=True`  -> nền ĐỎ: `lease_id=True` cho rc=9.
    #           Đúng hành vi: đồ giả dựng dấu `**Lease `<lease_id>`**`, nên với `True` dấu
    #           thành ``**Lease `True`**`` và CỬA CUỐI tìm thấy nó. Bốn vế `packet_issue` ở
    #           trên không dính vì `kiem()` tự từ chối kiểu sai của `packet_issue` trước đó;
    #           `lease_id` không có chốt tương ứng trong `kiem()`.
    #   nháp 2  chốt `goi == 0` trên `kiem_github`, `co_dau=False` -> nền vẫn ĐỎ: `lease_id`
    #           hợp lệ về mặt `kiem()` nên CHUỖI CŨ chạy tiếp và tự nó gọi 2 lần. Số lời gọi
    #           của CỔNG TỔNG trộn lời gọi của phép dò với lời gọi của `kiem()`.
    #
    # Thứ `_tien_kiem_mien_dang` bảo vệ là PHÉP DÒ, nên phải đo PHÉP DÒ. Đo tại đó thì tách
    # bạch, và không phụ thuộc vào việc `_lease_579()` có bao nhiêu trường hợp lệ:
    #
    #     `_do_dau_da_dang` với `lease_id` sai kiểu     nền: 0 lời gọi     L: 1 lời gọi
    #     `kiem_github` cùng đầu vào ấy                 nền: rc=8          L: rc=8   <- MÙ
    #
    # Đó là lý do `L` sống `176/176` qua bốn lượt: mọi ca đều chốt trên `rc`, mà `rc` mù.
    for nhan, lid in (("`lease_id` là `None`", None),
                      ("`lease_id` là danh sách", ["wp579-thu"]),
                      ("`lease_id` là `bool`", True),
                      ("`lease_id` là ánh xạ", {"x": 1}),
                      ("`lease_id` là số thực", 1.5)):
        gh = GhGia(comments={55: []})
        # `DA_TRA_VE`, KHÔNG phải một mã: phép DÒ là phép DÒ — nó nuốt mọi thứ và TRẢ VỀ.
        # Vế kết quả này chính là thứ lượt 6 bắt được là THIẾU: bỏ nó ra thì `R_probe`
        # (ném ngay đầu phép dò, đúng năm đầu vào này) SỐNG 177/177.
        _goi_dem_lop_gh(gh, "_do_dau_da_dang", _lease_579(lease_id=lid),
                        DA_TRA_VE, 0,
                        f"{nhan}: tiền kiểm phải chặn PHÉP DÒ trước khi nó chạm mạng — và "
                        f"phép dò phải TRẢ VỀ, không được vỡ. Mã thoát của cổng tổng KHÔNG "
                        f"phân biệt được (nền và đột biến `L` đều rc=8); chỉ số lời gọi của "
                        f"PHÉP DÒ phân biệt (0 so 1)",
                        env_them=ENV_GITHUB)


@ca
def t179_do_dau_KHONG_DO_DUOC_thi_nhuong_lai_cho_chuoi_cu():
    """Phép DÒ chỉ có quyền nói "đã đăng rồi"; nó KHÔNG có quyền nói "đạt", cũng KHÔNG có
    quyền biến một sự cố mạng thành một phán quyết.

    CA NÀY SINH RA TỪ MỘT ĐỘT BIẾN SỐNG SÓT, và đó là lý do nó tồn tại. Lượt đo đầu của
    packet #579 dựng năm đột biến; bốn cái bị giết đúng ca của nó, còn cái thứ năm — cho
    nhánh nuốt của `_do_dau_da_dang` ném `Chan(RC_DA_DANG)` — **sống sót 10/10**. Không
    phải vì mã đúng: vì năm ca kia chỉ dựng hai hình dạng (`_kiem_comment_da_co` thấy dấu,
    hoặc trả về êm), nên nhánh nuốt CHƯA TỪNG ĐƯỢC CHẠY. Đột biến sống sót ở đây là một
    khoảng TRỐNG của bộ test, không phải một chứng cứ về mã.

    Hình dạng còn thiếu: endpoint `comments` HỎNG. `_doc_gh` ném `Chan(RC_NOI_DUNG)`, tức
    "KHÔNG ĐO ĐƯỢC" — và `None ≠ False`: không đo được dấu thì KHÔNG được kết luận gì về
    dấu, phải nhường lại cho chuỗi cũ phán.

    Đo bằng một lease CỐ Ý tự cấp (`granted_by` là tên provider), vì mã thoát của nó
    (`rc=4`) chỉ đến được khi `kiem()` THẬT SỰ chạy. Đó là thứ phân biệt được ba hành vi mà
    một mình `rc` không phân biệt nổi:

        nhường lại cho chuỗi cũ (đúng)              -> rc=4   `kiem()` đã chạy
        nuốt thành "đã đăng"                        -> rc=9   `kiem()` bị bỏ qua
        ném thẳng lỗi KHÔNG ĐO ĐƯỢC của phép dò     -> rc=8   `kiem()` bị bỏ qua

    ĐỘT BIẾN LÀM CA NÀY ĐỎ: cho nhánh nuốt ném `Chan(RC_DA_DANG)`; hoặc bỏ điều kiện
    `if c.ma == RC_DA_DANG` để phép dò ném lại MỌI `Chan`; hoặc (biến thể `X` của
    cross-review lượt 4) GỠ HẲN nhánh nuốt `except Exception` để `RuntimeError` của HÌNH
    DẠNG 2 vỡ trần.

    TÍN HIỆU CỦA CA NÀY, và lượt 4 phải bắt mới có: với biến thể `X`, ca từng đỏ bằng
    `RuntimeError` THOÁT RA trước khi `chot` kịp chạy — tức đỏ đúng lúc cần mà đỏ vì một
    lỗi VÔ CAN, y hệt `t182` ở lượt 3. Nay `_goi_lop_gh` đổi mọi ngoại lệ trần thành
    `_NgoaiLeLa`, nên `ma` là `_MaVang` và `chot` bên dưới ĐỎ bằng thông điệp của CHÍNH ca,
    có nêu tên lớp đã thoát. Bản vá nằm ở HELPER, không ở ca — xem `_NgoaiLeLa`.
    """
    lease = _lease_579(granted_by="codex")

    def do(gia):
        ex, _mod = _goi_lop_gh(gia, "kiem_github", lease, env_them=ENV_GITHUB)
        return 0 if ex is None else ex.ma

    # HÌNH DẠNG 1 — endpoint hỏng "tử tế": `_doc_gh` bọc thành `Chan(RC_NOI_DUNG)`.
    ma = do(GhGia(comments={55: []}, loi_comment={55}))
    chot(ma == RC_TU_CAP,
         f"dò dấu KHÔNG ĐO ĐƯỢC thì phải nhường cho `kiem()` phán (rc={RC_TU_CAP} cho lease "
         f"tự cấp), được rc={ma}. rc={RC_DA_DANG} nghĩa là một sự cố mạng được đọc thành "
         f"'đã đăng rồi'; rc={RC_NOI_DUNG} nghĩa là phép dò tự phán thay cổng.")

    # HÌNH DẠNG 2 — ngoại lệ KHÔNG PHẢI `Chan`, và đây mới là hình dạng chạm nhánh nuốt.
    # ĐO ĐƯỢC: hình dạng 1 KHÔNG chạm nó, vì `_doc_gh` bắt `OSError` rồi bọc mọi thứ khác
    # thành `Chan` — nên thêm mỗi hình dạng 1 thì đột biến "nhánh nuốt ném rc=9" vẫn SỐNG
    # (đã đo: 11/11). Chỉ một ngoại lệ lọt qua `_doc_gh` mới phơi được nhánh ấy, và cách
    # duy nhất dựng được nó từ đây là cho chính `GOI_GH` ném một lớp ngoài họ `OSError`.
    def gh_no_tung(*_a):
        raise RuntimeError("hỏng theo kiểu KHÔNG AI LƯỜNG TRƯỚC")

    ma = do(gh_no_tung)
    chot(ma == RC_TU_CAP,
         f"ngoại lệ lạ từ phép dò cũng phải nhường cho `kiem()` (rc={RC_TU_CAP}), được rc={ma}. "
         f"Nhánh nuốt của `_do_dau_da_dang` tồn tại đúng để chuyện này KHÔNG thành một phán "
         f"quyết; bỏ nó đi thì một lỗi lạ sẽ thoát ra khỏi cổng dưới dạng vỡ trần.")


@ca
def t180_hai_loi_cung_luc_thi_tien_kiem_KHONG_duoc_cuop_quyen_phan():
    """M3 — đường KHÔNG-CÓ-DẤU phải giữ ĐÚNG THỨ TỰ LỖI của nền, kể cả khi lease mắc HAI lỗi.

    CA NÀY SINH RA TỪ MỘT HỒI QUY THẬT, do cross-review codex lượt 1 bắt
    (`unposted-error-precedence-changes`). Bản trước của packet này đặt
    `_tien_kiem_mien_dang` NGOÀI `try` của `_do_dau_da_dang`, nên `Chan(8)` của tiền kiểm
    thoát ra khỏi cả `kiem_github` và phán thay `kiem()`.

    Một lỗi thì không thấy. HAI lỗi mới thấy — lease vừa TỰ CẤP (`kiem()` trả `rc=4`) vừa
    có `packet_issue` SAI KIỂU (tiền kiểm trả `rc=8`):

        nền `origin/master`   -> rc=4   `kiem()` bắt authority trước
        bản trước             -> rc=8   tiền kiểm bắn trước — ĐỔI THỨ TỰ LỖI
        bản này               -> rc=4   tiền kiểm nhường lại, khớp nền

    `t177` không bắt được vì nó dựng từng lỗi RIÊNG; một cổng đúng trên mỗi lỗi đơn lẻ vẫn
    có thể sai về THỨ TỰ khi hai lỗi gặp nhau. Cùng họ bài học "vá đúng chỗ được chỉ rồi bỏ
    sót đường thứ ba".

    ĐỘT BIẾN LÀM CA NÀY ĐỎ: đưa `_tien_kiem_mien_dang` trở ra NGOÀI `try` ⇒ `rc` 4 → 8.
    Đã chạy (công cụ công thức, bản sao, 24-09): tập đỏ trên `t174`–`t184` là `{t178, t180}`, cả
    hai đỏ bằng `TinHieuChotCa` của chính ca. `t178` đỏ ĐÚNG lý do: vế `lease_id=None` của nó gọi
    thẳng `_do_dau_da_dang` và đòi TRẢ VỀ, mà tiền kiểm ngoài `try` ném `Chan(8)`. Bản trước khai
    "giết ĐÚNG ca này, `t174`–`t179` đều QUA" — hẹp hơn phép đo; cross-review codex lượt 6 bắt.

    CÔNG THỨC THỨ HAI CỦA BẢN TRƯỚC LÀ SAI, và đây là lý do nó bị gỡ: bản trước ghi "bỏ
    `return` ở nhánh `Chan` để tiền kiểm ném lại". Python KHÔNG tự ném lại một ngoại lệ đã
    bắt — hàm chạy hết rồi trả `None`, nên cả bảy ca vẫn QUA. Cross-review lượt 2 chạy thật
    và bắt được (`t180-equivalent-mutation-recipe`). Muốn công thức ấy có răng thì phải viết
    "thay `return` bằng `raise`", mà bản ấy có thể giết luôn `t179` nên không được khai là
    một chốt độc lập. Một công thức đột biến KHÔNG CHẠY được thì nó không chứng minh gì —
    đúng bài học "NGHĨ RA được phép thử mà KHÔNG CHẠY nó thì phép thử ấy KHÔNG TỒN TẠI".
    """
    lease = _lease_579(granted_by="codex", packet_issue="55")
    _do_kiem_github_dem(
        lease, False, RC_TU_CAP, 0,
        f"lease vừa tự cấp vừa sai kiểu `packet_issue`: phải giữ mã của NỀN "
        f"(`kiem()` bắt authority trước); rc={RC_NOI_DUNG} nghĩa là tiền kiểm miền đã cướp "
        f"quyền phán của `kiem()` — đúng hồi quy mà M3 khai là không có. Và nhường quyền "
        f"PHÁN không có nghĩa là nhường luôn quyền DÒ")


@ca
def t181_cua_CUOI_van_phai_chan_khi_API_comment_hong():
    """A15 — phép DÒ sớm KHÔNG thay được cửa `_kiem_comment_da_co` ở CUỐI `kiem_github`.

    CA NÀY SINH RA TỪ MỘT ĐỘT BIẾN SỐNG SÓT, cross-review codex lượt 2 dựng
    (`final-comment-gate-mutant-survives`). Đột biến `I` bỏ ĐÚNG lời gọi cuối
    `_kiem_comment_da_co(repo, lease)`, giữ nguyên phép dò sớm — và **sống sót 173/173**.

    Vì sao cả 173 ca cũ đều mù: một lease HỢP LỆ với endpoint `comments` HỎNG thì phép dò
    sớm NUỐT lỗi (đúng thiết kế — nó chỉ có quyền nói "đã đăng rồi"), rồi `kiem()` chạy trọn
    và KHÔNG chạm mạng. Thứ duy nhất còn lại để chặn là cửa CUỐI. Bỏ nó đi thì
    "KHÔNG ĐO ĐƯỢC" lặng lẽ thành "CHO QUA" — đúng thứ `None ≠ False` sinh ra để chặn.

    Các ca cũ không chạm được cửa ấy, từng ca một:
        `t179` lease TỰ CẤP  -> `kiem()` ném `rc=4` TRƯỚC khi tới cuối
        `t48`  gọi thẳng helper comment, không qua `kiem_github`
        `t174`/`t176` có dấu -> phép dò sớm đã ném `rc=9`, không đi tiếp
        `t177` có đi tới cuối nhưng KHÔNG khẳng định số lời gọi, nên `3 -> 2` lọt

    Đo được, và hai vế khác nhau ở CẢ HAI trục:
        bản đúng -> `rc=8`, 3 lời gọi   (cửa cuối chặn)
        đột biến -> `rc=0`, 2 lời gọi   (lọt, và thiếu đúng một lời gọi)

    Ca này KHÔNG thay `t179`: `t179` chứng minh phép dò không được TỰ PHÁN, ca này chứng minh
    cửa cuối không được VẮNG MẶT. Hai giai đoạn khác nhau của cùng một đường.

    ĐỘT BIẾN LÀM CA NÀY ĐỎ: bỏ `_kiem_comment_da_co(repo, lease)` ở cuối `kiem_github`.
    """
    lease = _lease_579()
    gh = GhGia(comments={55: []}, loi_comment={55})
    _goi_dem_lop_gh(
        gh, "kiem_github", lease, RC_NOI_DUNG, 3,
        "lease hợp lệ + endpoint `comments` HỎNG: cửa cuối phải chặn, và phải có đúng 3 lời "
        "gọi (dò sớm + loại số hiệu + cửa cuối). Cho qua nghĩa là một lease CHƯA đo được dấu "
        "được thả — phép dò sớm nuốt lỗi là ĐÚNG, nhưng chỉ khi còn cửa cuối đỡ phía sau; "
        "thiếu một lời gọi là dấu hiệu một cửa đã biến mất",
        env_them=ENV_GITHUB)


@ca
def t182_lease_KHONG_PHAI_anh_xa_thi_chan_co_ten_chu_khong_vo_tran():
    """A16 — chốt HÌNH DẠNG phải fail-close, không để `AttributeError` TRẦN thoát khỏi cổng.

    Cross-review lượt 2 bắt (`unposted-error-precedence-changes`, lần thứ HAI cùng slug).
    Bản vá lượt 1 đưa CẢ `_tien_kiem_mien_dang` vào trong `try` của `_do_dau_da_dang`, nên
    `Chan` nó ném cho một `lease` không phải ánh xạ cũng bị nuốt; `kiem()` sau đó gọi
    `.get()` trên thứ không có phương thức ấy và ngoại lệ TRẦN thoát ra.

    KHAI CHO ĐÚNG PHẠM VI: nền `origin/master` CŨNG vỡ y hệt ở đây, nên đây KHÔNG phải hồi
    quy mới — nó là việc đánh mất một chốt mà chính lượt 1 vừa thêm. Và đường CLI có
    `_doc_yaml` giữ chốt ánh xạ riêng (đo được `rc=8`), nên đừng khai thành "YAML đi lọt".

    Ca này khoá đúng MỘT thứ: API `kiem_github` nhận thứ không phải ánh xạ thì phải ra
    `Chan(RC_NOI_DUNG)` CÓ TÊN, không phải một `AttributeError` vỡ trần.

    ĐỘT BIẾN LÀM CA NÀY ĐỎ: đưa chốt `isinstance(lease, dict)` trở vào TRONG `try` (tức
    khôi phục bản vá lượt 1) ⇒ ngoại lệ trần thoát ra, `chot` bắt được kiểu KHÁC `Chan`.
    """
    for nhan, xau in (("None", None), ("danh sách", []), ("bool", True),
                      ("số nguyên", 55), ("chuỗi", "55")):
        gh = GhGia(comments={55: []})
        # `_goi_lop_gh` nay TỰ đổi một ngoại lệ trần thành `_NgoaiLeLa` (lượt 4), nên ca này
        # dùng lại đường chung — không còn helper riêng. Lượt 3 vá bằng một helper cho RIÊNG
        # ca này; lượt 4 bắt `t179` mắc y hệt, tức bản vá ấy ĐÚNG mà HẸP. Xem `_NgoaiLeLa`.
        _goi_dem_lop_gh(
            gh, "kiem_github", xau, RC_NOI_DUNG, 0,
            f"lease là {nhan}: phải ném `Chan(rc={RC_NOI_DUNG})` CÓ TÊN và chặn TRƯỚC khi "
            f"chạm mạng. Một ngoại lệ TRẦN thoát khỏi cổng là fail-open đội lốt sự cố",
            env_them=ENV_GITHUB)


@ca
def t183_do_dau_HONG_roi_PHUC_HOI_thi_cua_cuoi_van_phai_bo_qua():
    """A17 — nhánh `RC_DA_DANG` của CỬA CUỐI: dò đầu KHÔNG ĐO ĐƯỢC, lần đọc cuối THẤY DẤU.

    CA NÀY SINH RA TỪ MỘT ĐỘT BIẾN SỐNG SÓT, cross-review codex lượt 3 dựng
    (`final-comment-already-posted-branch-mutant-survives`). Đột biến `K` giữ phép dò sớm,
    giữ lời gọi cuối, giữ MỌI `Chan` khác — chỉ nuốt riêng `Chan(RC_DA_DANG)` đến từ cửa
    cuối. Nó **sống sót `175/175`**, và `t181` không thấy vì `t181` dựng ca API hỏng **MÃI**.

    Hình dạng còn thiếu, và nó là hình dạng THẬT của một sự cố mạng thoáng qua:

        lần đọc 1 (phép dò sớm)  -> hỏng  => KHÔNG ĐO ĐƯỢC, phép dò NHƯỜNG lại
        lần đọc 2 (cửa cuối)     -> lành  => THẤY DẤU  => phải `rc=9` (bỏ qua)

    `K` cho `rc=0`, tức một lease ĐÃ ĐĂNG được cấp đường đăng LẠI. Đó đúng thứ chốt idempotent
    sinh ra để chặn, và `t181` chỉ chặn được nửa kia của nó (`rc=8` khi hỏng mãi).

    Hai ca giữ HAI phán quyết khác nhau của cùng một cửa, nên không ca nào thay được ca nào:
        `t181` — hỏng MÃI       => `rc=8`, không được cho qua
        `t183` — hỏng rồi LÀNH  => `rc=9`, phải bỏ qua

    `len(gh.calls) == 3` một mình KHÔNG thấy `K`: cả bản đúng lẫn `K` đều gọi đủ ba lần. Thứ
    phân biệt là MÃ THOÁT, nên ca này chốt mã — ngược với `t181` nơi số lời gọi mới là răng.

    ĐỘT BIẾN LÀM CA NÀY ĐỎ: nuốt `Chan(RC_DA_DANG)` đến từ `_kiem_comment_da_co` ở cuối
    `kiem_github` (giữ nguyên mọi `Chan` khác).
    """
    class GhHongMotLan(GhGia):
        """Lần đọc `comments` ĐẦU hỏng, các lần sau lành. Dựng trên `GhGia` sẵn có —
        không dựng cơ chế giả thứ hai."""
        def __init__(self, *a, **k):
            super().__init__(*a, **k)
            self.lan_doc_comments = 0

        def __call__(self, *args):
            endpoint = next((x for x in args if str(x).startswith("repos/")), "")
            if endpoint.endswith("/comments"):
                self.lan_doc_comments += 1
                if self.lan_doc_comments == 1:
                    self.calls.append(args)
                    return subprocess.CompletedProcess(args, 1, "", "comments hong tam thoi")
            return super().__call__(*args)

    lease = _lease_579()
    dau = "**Lease `" + str(lease["lease_id"]) + "`**"
    gh = GhHongMotLan(comments={55: [{"id": 7, "body": dau + " — bản chiếu",
                                      "user": {"login": "github-actions[bot]"}}]})
    ex, _mod = _goi_lop_gh(gh, "kiem_github", lease, env_them=ENV_GITHUB)
    ma = 0 if ex is None else ex.ma
    chot(ma == RC_DA_DANG,
         f"dò đầu hỏng rồi cửa cuối phục hồi và THẤY DẤU: phải bỏ qua bằng rc={RC_DA_DANG}, "
         f"được rc={ma}. rc=0 nghĩa là một lease ĐÃ ĐĂNG được cấp đường đăng LẠI — chốt "
         f"idempotent đã hỏng ở đúng nhánh mà một sự cố mạng thoáng qua sẽ đi vào.")
    chot(gh.lan_doc_comments >= 2,
         f"ca này chỉ có nghĩa khi endpoint `comments` được đọc ÍT NHẤT HAI lần (dò sớm rồi "
         f"cửa cuối), đọc {gh.lan_doc_comments} lần. Một lần nghĩa là phản chứng chưa từng "
         f"tồn tại — ca xanh vì lý do sai.")


CO_CHI_CA = "--chi-ca="   # `--chi-ca=t01_` ⇒ chỉ chạy ca có tên bắt đầu bằng tiền tố ấy (M3 packet #504 dùng để sinh lượt con rẻ)


def _nhat_ky_ca(*phan) -> None:
    """Một dòng, xả ngay (packet #504 M1). `>>> vao <ca> <utc>` / `<<< ra <ca> <giây>s QUA|DO|BO_QUA`.

    Vì sao: lane Windows của master bị huỷ ở trần 60 phút mà log bước chỉ có đệm khối, nên
    "DÒNG IN CUỐI CÙNG ≠ CA CHẠY CUỐI CÙNG" (#499 C3) — không có tên ca nào để sửa. `flush=True`
    xả đệm Python; `PYTHONUNBUFFERED=1` ở wrapper (M2) tắt đệm Python cho cả các print khác,
    và chốt "không đệm" chỉ đo được ở lượt Windows thật (M4), không đo được trong tiến trình này.
    Dòng tổng kết `lease_publish: N/M đạt` và các dòng `  ĐỎ  …` / `  BỎ QUA …` GIỮ NGUYÊN BYTE —
    regex của t125 đọc chúng; `ci_dang_ky_test.py` kiểm DA_NOI và wiring của wrapper.
    """
    print(*phan, flush=True)


@ca
def t184_chinh_HELPER_phai_doi_ngoai_le_TRAN_thanh_ca_DO_chu_khong_vo_tran():
    """A19 (r7; A18 là của `t179`) — ĐO CHÍNH CÁI THƯỚC ĐO. Sáu vế, mỗi vế một đột biến riêng.

    Vì sao ca này tồn tại: bản vá lượt 4 nằm trong `_goi_lop_gh`, tức một chốt do CHÍNH
    phiên này dựng ra để chống bị lừa. `CLAUDE.md` đã trả giá đúng chỗ ấy ở #355/#359 —
    *"thước đo do chính ta vừa dựng ra để chống bị lừa, và nó bị lừa"*. Một chốt không có ca
    đo nó là một chốt sẽ âm thầm hở lại.

    Ca này KHÔNG dùng cổng thật: nó tiêm thẳng một `GOI_GH` ném thứ cần ném, vì thứ đang đo
    là HỢP ĐỒNG của helper, không phải hành vi của cổng.

        (a) cổng ném `Chan`        -> trả về CHÍNH `Chan` ấy, `.ma` là số nguyên (hợp đồng CŨ)
                                      — và `Chan` phải do CỔNG ném, không do fixture: xem
                                      chú thích tại vế (a), danh tính lớp là theo lần NẠP
        (b) cổng ném ngoại lệ trần -> trả `_NgoaiLeLa`, `.ma` KHÔNG bằng bất kỳ mã nào,
                                      và `str(ma)` NÊU TÊN LỚP đã thoát
        (a2) cổng ném `Chan` NÀO   -> trả về CHÍNH đối tượng ấy (`returned is expected`)
        (c) cổng không ném gì      -> trả `None` (hợp đồng CŨ)
        (d) `KeyboardInterrupt`    -> KHÔNG bị nuốt, đi thẳng ra
        (e) `__str__` của ngoại lệ hỏng -> helper VẪN TRẢ VỀ, tên lớp còn đọc được
    Mọi vế đòi TRẢ VỀ — (a) (a2) (b) (c) (e) — đo qua cửa `_goi_doi_tra_ve`; `t188` khoá điều đó.

    Vế (b) đòi CẢ HAI: so sánh sai VÀ in ra tên lớp. Thiếu vế in thì ca xanh cho một cài đặt
    trả `None` — mà `None` làm mọi ca ĐỎ đúng lúc cần, chỉ mất đúng thứ người đọc phải biết.
    Vế (d) là vế dễ mất nhất: nới `except Exception` thành `except BaseException` làm bộ test
    không dừng được bằng Ctrl-C, và không ca nào khác thấy.

    ĐỘT BIẾN LÀM CA NÀY ĐỎ, từng vế một:
        (a) `except mod.Chan` -> gộp vào nhánh `_NgoaiLeLa`
        (b) trả `None` thay cho `_NgoaiLeLa`  |  hoặc cho `_MaVang.__eq__` trả `True`
            |  hoặc `__str__` của `_MaVang` HAY của `_NgoaiLeLa` bỏ `self.kieu`
        ĐÃ CHẠY từng dòng trên (bản sao, phân hạng bằng `TinHieuChotCa`): mọi công thức giết
        `t184`. Hai công thức của bản trước là SAI, cross-review lượt 7 bắt một, executor đo
        ra cái thứ hai khi soát lại cả loạt: "bỏ `__eq__`" TƯƠNG ĐƯƠNG (mặc định so danh tính,
        vẫn `False` với mọi mã) ⇒ 183/183; "`__str__` bỏ `self.kieu`" chỉ giết khi đột biến
        `_MaVang` — ở `_NgoaiLeLa` nó SỐNG vì vế (b) chưa chốt `str(ex)`. Nay chốt cả hai.
        (c) trả `_NgoaiLeLa(None)` khi không ném gì
        (d) `except Exception` -> `except BaseException`
    """
    lease = _lease_579()

    # (a) HỢP ĐỒNG CŨ: `Chan` đi qua NGUYÊN VẸN.
    #
    # `Chan` PHẢI đến từ CHÍNH cổng, không được do fixture ném — và chỗ này đã trả giá ngay
    # lần chạy đầu. Bản viết đầu dùng `raise _nap_cong().Chan(...)` trong một `GOI_GH` giả,
    # và ca ĐỎ với `<ngoại lệ TRẦN Chan: cố ý>`. Không phải helper sai: `_nap_cong()` dựng
    # một MODULE MỚI mỗi lần gọi, nên `Chan` của module fixture là một LỚP KHÁC với
    # `mod.Chan` bên trong `_goi_lop_gh` — `except mod.Chan` không khớp, và đúng như thiết
    # kế nó rơi vào `_NgoaiLeLa`.
    #
    # Ghi lại vì đây là một bẫy thật cho mọi ca sau: **danh tính lớp `Chan` là THEO TỪNG LẦN
    # NẠP.** Đường sản phẩm không dính (cổng và mọi thứ nó gọi nằm trong cùng một module
    # instance), nhưng bất kỳ fixture nào tự nạp module rồi ném `Chan` của bản sao ấy sẽ bị
    # phân hạng là ngoại lệ trần — và sẽ trông y hệt một lỗi của helper.
    #
    # Nên vế (a) ép cổng tự ném: lease TỰ CẤP ⇒ `kiem()` ném `Chan(RC_TU_CAP)` của chính nó.
    lease_tu_cap = _lease_579(granted_by="codex")
    ex, mod_a = _goi_doi_tra_ve("(a)", GhGia(comments={55: []}), "kiem_github",
                                lease_tu_cap, env_them=ENV_GITHUB, kem_mod=True)
    # ĐÒI DANH TÍNH LỚP, không chỉ đòi "một đối tượng có `.ma` đúng". Cross-review lượt 5 bắt
    # (`helper-contract-assertions-omit-code-domain-and-identity`): bản trước chỉ chốt
    # `.ma == 4`, nên hai đột biến đều LỌT — `P_identity` đổi danh tính `Chan`, và `P_type`
    # trả một PROXY có `.ma`. Cả hai giữ `.ma` đúng, nên một chốt đọc `.ma` không thấy gì.
    chot(ex is not None and type(ex) is mod_a.Chan,
         f"(a) helper phải trả về CHÍNH lớp `Chan` của module đang thử, nhận "
         f"{type(ex).__name__!r}. Một đối tượng khác lớp mà có `.ma` đúng vẫn làm mọi ca "
         f"dùng `ex.ma` xanh — đó là tín dụng giả ở tầng hợp đồng, không ở tầng giá trị.")
    chot(getattr(ex, "ma", None) == RC_TU_CAP,
         f"(a) `Chan` của CHÍNH cổng phải đi qua nguyên vẹn với ma={RC_TU_CAP}, nhận "
         f"{getattr(ex, 'ma', None)!r}. Nới helper mà làm hỏng đường cũ là đổi một lỗi lấy "
         f"20+ ca khác.")

    # (a2) DANH TÍNH ĐỐI TƯỢNG, không chỉ danh tính LỚP. Lượt 6 bắt: `P_identity` trả một
    # `Chan` MỚI (`mod.Chan(ex.ma, ex.thong_diep)`) — CÙNG lớp, CÙNG `.ma` — nên vế (a) ở
    # trên vẫn PASS. Hợp đồng thật là "ném `Chan` NÀO thì trả về CHÍNH đối tượng ấy": mất
    # đối tượng gốc là mất `__traceback__`, mất mọi thuộc tính ca sau có thể cần, và mở
    # đường cho một helper "sửa lại" ngoại lệ trên đường ra.
    #
    # Đo được điều đó cần một `Chan` CỦA ĐÚNG lần nạp đang chạy — xem móc `truoc_khi_chay`.
    giu = {}

    def _gh_nem_chinh_no(*_a):
        raise giu["ex"]

    # CỔNG DÙNG Ở ĐÂY LÀ `_kiem_comment_da_co`, và đó là một phép ĐO chứ không phải tiện tay.
    # Đo cả ba cổng với cùng fixture (21-09): `_kiem_comment_da_co` trả về CHÍNH đối tượng;
    # `kiem_github` trả một `Chan` KHÁC tuy cùng `ma=6`; `_do_dau_da_dang` nuốt hẳn (trả
    # `None`) vì nó là phép DÒ. Hai cái sau là HÀNH VI CỦA SẢN PHẨM, không phải lỗi helper —
    # chốt danh tính lên chúng là chốt sai đơn vị, và ca sẽ đỏ vì một mệnh đề chưa ai khai.
    ex_a2 = _goi_doi_tra_ve(
        "(a2)", _gh_nem_chinh_no, "_kiem_comment_da_co", "o/r", _lease_579(),
        env_them=ENV_GITHUB,
        truoc_khi_chay=lambda m: giu.__setitem__("ex", m.Chan(m.RC_NEO, "a2-danh-tinh")))
    chot(ex_a2 is giu["ex"],
         f"(a2) helper phải trả về CHÍNH đối tượng `Chan` mà cổng đã ném, nhận một đối "
         f"tượng khác (id {id(ex_a2)} so {id(giu['ex'])}). Cùng lớp và cùng `.ma` KHÔNG đủ: "
         f"một bản sao làm mất `__traceback__` và cho phép sửa ngoại lệ trên đường ra, mà "
         f"mọi ca đọc `ex.ma` đều không thấy gì.")

    # (b) HÌNH DẠNG MỚI: ngoại lệ trần -> `_NgoaiLeLa`, không vỡ ra ngoài ca.
    def gh_tran(*_a):
        raise RuntimeError("hỏng theo kiểu KHÔNG AI LƯỜNG TRƯỚC")
    # BỌC — lượt 6 bắt (`helper-contract-raw-exception-escapes-own-assertion`): vế này đòi
    # helper TRẢ VỀ, mà lời gọi trần thì "helper ném" giết ca TRƯỚC `chot`, nên ca đỏ bằng
    # traceback của runner chứ không bằng chốt của chính nó. Vế (e) đã có mẫu đúng; nay mọi
    # vế đòi TRẢ VỀ đều đi qua cùng một cửa, thay vì cửa ấy chỉ phục vụ một vế.
    ex = _goi_doi_tra_ve("(b)", gh_tran, "kiem_github", lease, env_them=ENV_GITHUB)
    _mod_b = _nap_cong()
    chot(ex is not None and ex.__class__.__name__ == "_NgoaiLeLa",
         f"(b) ngoại lệ TRẦN phải thành `_NgoaiLeLa`, nhận {ex!r}. Vỡ ra ngoài ca nghĩa là "
         f"ca gọi sẽ đỏ vì runner chứ không vì `chot` của chính nó — đúng lớp tín dụng giả.")
    ma = ex.ma
    # ĐO CẢ HAI TOÁN TỬ, và vế `==` mới là vế THẬT — chỗ này đã trả giá ngay trong lượt 4.
    # Bản đầu chỉ chốt `all(ma != m ...)`. Đột biến `N3` cho `_MaVang.__eq__` trả `True` mà
    # để nguyên `__ne__` ⇒ ca vẫn XANH, toàn suite **177/177**. Mà mọi ca trong tệp này chốt
    # bằng `ma == RC_X`, nên với `N3` một ngoại lệ trần sẽ khớp MỌI mã thoát và cả loạt ca
    # thành XANH GIẢ. Tức vế `!=` đo đúng thứ KHÔNG AI DÙNG.
    # Bài học, và nó là bài học chung: chốt phải đo ĐÚNG TOÁN TỬ mà người gọi dùng. Python
    # KHÔNG suy `__ne__` ra từ `__eq__` khi cả hai được định nghĩa tường minh.
    # MIỀN MÃ PHẢI ĐẦY ĐỦ. Bản trước chỉ thử `{0, 4, 8, 9}`, trong khi `t177` thật sự chốt
    # bằng `== 6` (`RC_NEO`). Cross-review lượt 5 đo: cho sentinel nhận RIÊNG `6` thì `t184`
    # vẫn `PASS`, **và** một ngoại lệ trần ở lần gọi thứ ba của `t177` cũng thành ca XANH.
    # Tức lỗ miền ở đây không dừng ở `t184` — nó mở một ca xanh giả ở ca KHÁC.
    #
    # Nên miền lấy TRỌN bảng mã thoát của cổng, không lấy một tập tiện tay. Hai đột biến
    # `N3`/`N3b` chỉ chứng minh hai toán tử có răng trên tập ĐÃ THỬ; chúng không chứng minh
    # mọi mã đều được phủ — đó là hai mệnh đề khác nhau.
    # LẤY MIỀN TỪ CHÍNH MODULE SẢN PHẨM, không liệt kê tay. Liệt kê tay là một danh sách sẽ
    # trôi: thêm một `RC_*` mới mà quên sửa ca thì miền hụt lại, và lỗ miền vừa vá tái sinh.
    # Đọc `RC_*` từ module ⇒ mã mới TỰ ĐỘNG được phủ. Chốt `>= 9` giữ cho phép đọc ấy không
    # âm thầm trả tập rỗng (bắt sai tên tiền tố, module nạp hụt).
    MOI_MA = sorted({v for k, v in vars(_mod_b).items()
                     if k.startswith("RC_") and isinstance(v, int) and not isinstance(v, bool)})
    chot(len(MOI_MA) >= 9,
         f"(b) miền mã đọc từ module phải có ít nhất 9 giá trị, đọc được {MOI_MA!r}. Tập rỗng "
         f"hoặc hụt làm hai chốt dưới đây thành chốt KHÔNG THỂ ĐỎ.")
    bang_nham = [m for m in MOI_MA if ma == m]
    chot(not bang_nham,
         f"(b) `ma == <mã thoát>` phải SAI với MỌI mã, nhưng bằng {bang_nham!r}. Bằng một mã "
         f"nào đó là biến một sự cố thành một phán quyết — và vì mọi ca đều chốt bằng `==`, "
         f"chỗ này hỏng là cả loạt ca thành XANH GIẢ.")
    khac_nham = [m for m in MOI_MA if not (ma != m)]
    chot(not khac_nham,
         f"(b) `ma != <mã thoát>` phải ĐÚNG với MỌI mã, nhưng sai ở {khac_nham!r}.")
    chot("RuntimeError" in str(ma),
         f"(b) `str(ma)` phải NÊU TÊN LỚP đã thoát, nhận {str(ma)!r}. Không nêu thì ca gọi "
         f"vẫn ĐỎ, nhưng người đọc mất đúng thứ cần để biết đã hỏng ở đâu.")
    # Cùng đòi hỏi cho CHÍNH `_NgoaiLeLa`: các ca in `{ex!r}` chứ không chỉ `{ma}`. Thiếu dòng
    # này thì đột biến bỏ `self.kieu` khỏi `_NgoaiLeLa.__str__` SỐNG (đo khi soát công thức,
    # cross-review lượt 7).
    chot("RuntimeError" in str(ex) and "RuntimeError" in repr(ex),
         f"(b) `str`/`repr` của `_NgoaiLeLa` phải NÊU TÊN LỚP đã thoát, nhận {str(ex)!r}.")

    # (c) HỢP ĐỒNG CŨ: không ném gì -> `None`.
    ex = _goi_doi_tra_ve("(c)", GhGia(comments={55: []}), "_kiem_comment_da_co", "o/r", lease)
    chot(ex is None,
         f"(c) không ném gì thì phải trả `None`, nhận {ex!r}. Trả một đối tượng ở đây làm mọi "
         f"ca dùng `ex is None` đỏ sai.")

    # (e) ĐƯỜNG CHẨN ĐOÁN KHÔNG ĐƯỢC LÀM VỠ PHÉP ĐO.
    #
    # Cross-review lượt 5 bắt (`helper-exception-formatting-escapes-own-assertion`): bản
    # trước gọi `str(ex)` thẳng trong `_MaVang.__init__` và định dạng lại ngoại lệ gốc trong
    # `_NgoaiLeLa.__str__`. Một ngoại lệ thuộc `Exception` mà `__str__` NÉM thì helper không
    # trả được kết quả và ngoại lệ trần thoát ra — **vỡ CẢ LỚP ca gọi helper**, không riêng
    # một ca. Đo được: 41 vị trí × `StringFails` ⇒ `RAW = 41/41`.
    #
    # Hai hình dạng, vì `__str__` hỏng theo HAI kiểu khác nhau và một bản vá chỉ bọc `try`
    # quanh lời gọi sẽ lọt kiểu thứ hai:
    #     ném                      -> `<__str__ hỏng>`
    #     trả thứ không phải chuỗi -> `<__str__ trả thứ không phải chuỗi>`
    #
    # VÀ CẢ HAI VẾ ĐỀU ĐÒI TÊN LỚP VẪN ĐỌC ĐƯỢC. Đó là điểm của bản vá: `type(ex).__name__`
    # KHÔNG đi qua `__str__`, nên chẩn đoán còn nguyên kể cả khi định dạng chết. Một bản vá
    # nuốt lỗi rồi trả chuỗi rỗng sẽ qua vế "không vỡ" mà trượt vế này.
    class _StrNem(Exception):
        def __str__(self):
            raise ValueError("định dạng hỏng")

    class _StrKhongChuoi(Exception):
        def __str__(self):
            return 12345          # noqa: RET504 — CỐ Ý trả thứ không phải chuỗi

    for nhan, lop_hong in (("`__str__` NÉM", _StrNem),
                           ("`__str__` trả thứ không phải chuỗi", _StrKhongChuoi)):
        def _gh_hong(*_a, lop_hong=lop_hong):
            raise lop_hong()
        # PHẢI BẮT QUANH CHÍNH LỜI GỌI HELPER, và vế này đã tự sập một lần vì thiếu nó.
        #
        # Đột biến `P_str` (hoàn nguyên bản vá: `str(ex)` thẳng trong `_MaVang.__init__`) làm
        # `ValueError` bật ra TỪ TRONG nhánh `except Exception` của helper — tức helper KHÔNG
        # TRẢ VỀ. `chot` bên dưới không bao giờ chạy, nên ca đỏ bằng một traceback trần chứ
        # không bằng tín hiệu của nó. Đo được: `P_str` ⇒ `176/177`, đỏ `t184`, thông điệp
        # `ValueError: định dạng hỏng`.
        #
        # Đúng LỚP lỗi mà vế này sinh ra để đo, chỉ cao hơn một tầng — và nó cho thấy: muốn
        # đo "X không thoát ra", phải BẮT, không thể đọc `ex` sau lời gọi. Mệnh đề thật của
        # vế (e) là "helper LUÔN TRẢ VỀ", và mệnh đề ấy chỉ kiểm được từ phía người gọi.
        #
        # Bắt ấy nay nằm TRONG CỬA `_goi_doi_tra_ve` — vế này từng tự viết `try` riêng, tức một
        # cửa thứ hai song song với cửa chung, và lời khai "một vế, một cửa" khi ấy sai.
        ex = _goi_doi_tra_ve(f"(e) {nhan}", _gh_hong, "kiem_github", lease, env_them=ENV_GITHUB)
        chot(ex is not None and ex.__class__.__name__ == "_NgoaiLeLa",
             f"(e) {nhan}: helper phải TRẢ VỀ được, nhận {ex!r}. Ngoại lệ trần thoát ra ở đây "
             f"làm vỡ mọi ca dùng helper, không riêng ca này.")
        chot(ex.kieu == lop_hong.__name__,
             f"(e) {nhan}: tên lớp phải còn đọc được, nhận {ex.kieu!r}. `type(ex).__name__` "
             f"không đi qua `__str__` — mất nó là mất chẩn đoán đúng lúc cần nhất.")
        chot(lop_hong.__name__ in str(ex.ma),
             f"(e) {nhan}: `str(ma)` phải nêu tên lớp, nhận {str(ex.ma)!r}.")
        chot(not any(ex.ma == m for m in MOI_MA),
             f"(e) {nhan}: `ma` vẫn phải khác MỌI mã thoát, nhận {ex.ma!r}.")

    # (d) `KeyboardInterrupt` KHÔNG được nuốt.
    def gh_ngat(*_a):
        raise KeyboardInterrupt
    bi_nuot = True
    try:
        _goi_lop_gh(gh_ngat, "kiem_github", lease, env_them=ENV_GITHUB)
    except KeyboardInterrupt:
        bi_nuot = False
    chot(not bi_nuot,
         "(d) `KeyboardInterrupt` bị helper NUỐT. Một bộ test không dừng được bằng Ctrl-C là "
         "một bộ test giữ máy làm con tin; `except Exception` là CÓ CHỦ ĐÍCH, đừng nới.")


@ca
def t187_chan_doan_phai_ha_ve_CHUOI_THUAN_chu_khong_chi_isinstance():
    """A22 — `_chuoi_thuan` đo theo HỌ. `isinstance(x, str)` KHÔNG đủ, và lượt 6 đo được.

    Bản vá lượt 5 chốt `isinstance(td, str)` rồi trả nguyên `td`. Mà **lớp CON của `str` qua
    được `isinstance`** và ghi đè được `__str__` / `__format__` / `__repr__`. Thông điệp ấy
    sau đó vào f-string của `chot` — và nổ ở đúng dòng đang tố cáo một lỗi khác.
    Cross-review lượt 6: **RAW 82 / 96 phép** trên hai họ `str` con hỏng định dạng.

    HỌ, chứ không một đại diện — bài học `m12/m13/m14` của #574: một nhãn có MỘT thành viên
    thì nhãn ấy rộng hơn tập fixture. SÁU thành viên dưới đây hỏng ở SÁU chỗ khác nhau, và
    mỗi cái phải cho ra một `str` THUẦN. (Chuỗi thường ở cuối là ĐỐI CHỨNG, không phải thành
    viên thứ bảy.)

    Vế cuối là ĐỐI CHỨNG XANH: chuỗi thường phải đi qua NGUYÊN VẸN. Thiếu nó thì một cài đặt
    trả hằng `"<x>"` cho mọi đầu vào cũng qua hết sáu vế trên.
    """
    class _StrHongStr(str):
        def __str__(self): raise RuntimeError("str hỏng")

    class _StrHongFormat(str):
        def __format__(self, _spec): raise RuntimeError("format hỏng")

    class _StrHongRepr(str):
        def __repr__(self): raise RuntimeError("repr hỏng")

    class _StrHongCaBa(str):
        def __str__(self): raise RuntimeError("str hỏng")
        def __format__(self, _spec): raise RuntimeError("format hỏng")
        def __repr__(self): raise RuntimeError("repr hỏng")

    class _StrHongGetAttr(str):
        def __getattribute__(self, ten): raise RuntimeError("getattribute hỏng")

    class _StrHongBase(str):
        def __str__(self): raise KeyboardInterrupt("tín hiệu dừng từ đường chẩn đoán")

    NOI_DUNG = "nội dung thật"
    HO = (("str con hỏng `__str__`", _StrHongStr(NOI_DUNG)),
          ("str con hỏng `__format__`", _StrHongFormat(NOI_DUNG)),
          ("str con hỏng `__repr__`", _StrHongRepr(NOI_DUNG)),
          ("str con hỏng CẢ BA", _StrHongCaBa(NOI_DUNG)),
          ("str con hỏng `__getattribute__`", _StrHongGetAttr(NOI_DUNG)),
          ("str con ném TÍN HIỆU DỪNG", _StrHongBase(NOI_DUNG)))
    for nhan, x in HO:
        r = _chuoi_thuan(x, "<dự phòng>")
        chot(type(r) is str,
             f"{nhan}: phải hạ về `str` THUẦN, nhận {type(r).__name__!r}. `isinstance` ĐÚNG "
             f"với lớp con, nên nó KHÔNG phân biệt được — và lớp con mang theo callback của "
             f"bên bị đo vào đúng f-string của `chot`.")
        # Định dạng THẬT — không chỉ kiểm kiểu. `type(...) is str` mà vẫn nổ khi format thì
        # phép kiểm trên chỉ là một lời khai về kiểu, không phải về dùng được.
        try:
            _ = f"thông điệp: {r}"
        except BaseException as loi:  # noqa: BLE001
            chot(False, f"{nhan}: kết quả đã là `str` thuần mà f-string vẫn ném "
                        f"`{_ten_lop(loi)}` — phép kiểm kiểu ở trên không đủ.")

    # XUYÊN ĐƯỜNG TẠO — đo CHỖ DÙNG, không chỉ đo hàm hạ.
    #
    # Cross-review codex 24-09 (`diagnostic-normalization-wiring-unmeasured`, P2): phần trên
    # chỉ gọi `_chuoi_thuan` TRỰC TIẾP, nên hai đột biến độc lập — gỡ lời gọi hạ TÊN LỚP trong
    # `_MaVang.__init__`, hoặc cho `_thong_diep_an_toan` trả nguyên THÔNG ĐIỆP — đều qua 14/14.
    # Hàm hạ có răng; CHỖ NỐI vào hàm hạ thì không ai đo. Và phép đo của reviewer lộ luôn một
    # lỗ thật: `_NgoaiLeLa.kieu` giữ tên lớp THÔ, `_MaVang` in được 6/6 mà nó chỉ 2/6.
    #
    # Nên mỗi thành viên HỌ đi vào CẢ HAI trường qua ĐƯỜNG THẬT:
    #   tên lớp    — một lớp ngoại lệ có `__name__` là CHÍNH `str` con ấy
    #   thông điệp — một ngoại lệ mà `__str__` trả CHÍNH `str` con ấy
    # rồi qua BA chỗ dùng: `_MaVang` · `_NgoaiLeLa` · cửa `_goi_doi_tra_ve` (đường của mọi ca).
    #
    # KHÔNG đưa giá trị thô vào f-string của `chot` — làm vậy là đỏ vì ĐƯỜNG CHẨN ĐOÁN, tức
    # tín dụng giả đúng loại ca này sinh ra để chặn. Chỉ nêu `type(...).__name__`.
    def _dinh_dang_duoc(obj):
        try:
            r = f"{obj}"
        except BaseException as loi:  # noqa: BLE001 — đo "định dạng được", phải bắt trọn
            return f"f-string NÉM `{_ten_lop(loi)}`"
        return None if type(r) is str else f"f-string ra `{type(r).__name__}`"

    lease_d = _lease_579()
    for nhan, x in HO:
        _LopTen = type("_LopTen", (Exception,), {})
        _LopTen.__name__ = x

        class _LoiThongDiep(Exception):
            def __str__(self, _x=x):
                return _x

        for truong, ex_goc in (("tên lớp", _LopTen("m")), ("thông điệp", _LoiThongDiep())):
            vi_tri = f"{nhan} / {truong}"
            mv = _MaVang(ex_goc)
            chot(type(mv.kieu) is str and type(mv.thong_diep) is str,
                 f"{vi_tri}: `_MaVang` phải giữ CẢ HAI trường là `str` THUẦN, nhận "
                 f"kieu={type(mv.kieu).__name__} thong_diep={type(mv.thong_diep).__name__}. "
                 f"Hàm hạ có răng mà chỗ nối không gọi nó là lỗ thật, không phải lỗ phép đo.")
            hong = _dinh_dang_duoc(mv)
            chot(hong is None, f"{vi_tri}: `_MaVang` không định dạng được — {hong}.")
            nl = _NgoaiLeLa(ex_goc)
            chot(type(nl.kieu) is str,
                 f"{vi_tri}: `_NgoaiLeLa.kieu` phải là `str` THUẦN, nhận "
                 f"{type(nl.kieu).__name__}. Lớp này có bản sao tên lớp RIÊNG và in nó ra.")
            hong = _dinh_dang_duoc(nl)
            chot(hong is None, f"{vi_tri}: `_NgoaiLeLa` không định dạng được — {hong}.")

            def _gh_nem(*_a, _e=ex_goc):
                raise _e
            ra = _goi_doi_tra_ve(f"t187 {vi_tri}", _gh_nem, "kiem_github", lease_d,
                                 env_them=ENV_GITHUB)
            chot(ra.__class__.__name__ == "_NgoaiLeLa" and type(ra.kieu) is str
                 and type(ra.ma.kieu) is str and type(ra.ma.thong_diep) is str,
                 f"{vi_tri}: qua CỬA THẬT mọi trường chẩn đoán phải là `str` THUẦN, nhận "
                 f"{ra.__class__.__name__}.")
            hong = _dinh_dang_duoc(ra)
            chot(hong is None, f"{vi_tri}: kết quả của cửa không định dạng được — {hong}.")

    # NHÁNH BÁO LỖI CỦA CỬA — đường THỨ BA, cross-review codex lượt 2 (24-09) bắt.
    #
    # Phần trên phủ hai wrapper; nhánh `except BaseException` của `_goi_doi_tra_ve` thì chưa.
    # Nhánh ấy CÓ đường vào thật trên mã chưa đột biến: `_goi_lop_gh` chỉ bắt `Exception`,
    # nên một ngoại lệ thuộc `BaseException` (mà không phải `Exception`) xuyên qua helper và
    # rơi đúng vào nhánh báo lỗi. Cho nó mang tên lớp là chính `str` con của HỌ: cửa phải đỏ
    # bằng `TinHieuChotCa` cả 6/6 — không được chết bằng `RuntimeError` hay
    # `KeyboardInterrupt` TRẦN nổ ra từ chính f-string báo lỗi.
    for nhan, x in HO:
        _LopBase = type("_LopBase", (BaseException,), {})
        _LopBase.__name__ = x

        def _gh_nem_base(*_a, _L=_LopBase):
            raise _L()
        loai = "cửa TRẢ VỀ dù helper đã ném"
        try:
            _goi_doi_tra_ve(f"t187 {nhan} / nhánh báo lỗi", _gh_nem_base, "kiem_github",
                            lease_d, env_them=ENV_GITHUB)
        except TinHieuChotCa:
            loai = "TinHieuChotCa"
        except BaseException as loi:  # noqa: BLE001 — đo "đỏ ĐÚNG lớp", phải bắt trọn
            loai = f"ngoại lệ TRẦN `{_ten_lop(loi)}`"
        chot(loai == "TinHieuChotCa",
             f"{nhan}: nhánh báo lỗi của cửa phải đỏ bằng `TinHieuChotCa`, nhận {loai}. "
             f"Đường chẩn đoán làm vỡ phép đo là tín dụng giả ở tầng cửa.")

    # ĐỌC TÊN LỚP HỎNG Ở METACLASS — cross-review codex lượt 3 (24-09). Các vế trên cho tên lớp
    # là một `str` CON; ở đây chính việc ĐỌC `__name__` hỏng. Ba thành viên: ném ngoại lệ thường,
    # ném TÍN HIỆU DỪNG (lượt 3), và TRẢ `None` (cross-review lượt 7 đòi thêm). Đo qua NĂM chỗ dùng: cửa hạ tên · hai wrapper · helper THẬT (phải
    # TRẢ `_NgoaiLeLa`) · cửa trả về (BaseException xuyên helper phải đỏ bằng `TinHieuChotCa`) ·
    # thông điệp bộ chạy.
    def _meta_hong(tin_hieu):
        class _MetaHong(type):
            def __getattribute__(cls, ten):
                if ten == "__name__":
                    if tin_hieu is None:
                        return None
                    raise tin_hieu("đọc tên lớp hỏng")
                return type.__getattribute__(cls, ten)
        return _MetaHong

    for nhan, tin_hieu in (("metaclass đọc tên NÉM ngoại lệ thường", RuntimeError),
                           ("metaclass đọc tên NÉM tín hiệu dừng", KeyboardInterrupt),
                           ("metaclass đọc tên TRẢ `None`", None)):
        _M = _meta_hong(tin_hieu)
        _LoiTen = _M("_LoiTen", (Exception,), {})
        _LoiTenBase = _M("_LoiTenBase", (BaseException,), {})
        ex_ten = _LoiTen("m")
        for noi, lam in (("`_ten_lop`", lambda: _ten_lop(ex_ten)),
                         ("`_MaVang`", lambda: f"{_MaVang(ex_ten)}"),
                         ("`_NgoaiLeLa`", lambda: f"{_NgoaiLeLa(ex_ten)}"),
                         ("`_bao_loi_ca`", lambda: _bao_loi_ca(ex_ten))):
            try:
                r = lam()
            except BaseException as loi:  # noqa: BLE001 — đo "không nổ", phải bắt trọn
                r = f"<NÉM {_ten_lop(loi)}>"
            chot(type(r) is str and not r.startswith("<NÉM "),
                 f"{nhan}: {noi} phải trả `str` thuần, nhận {r if type(r) is str else type(r).__name__}.")

        def _gh_ten_hong(*_a, _e=ex_ten):
            raise _e
        ra = _goi_doi_tra_ve(f"t187 {nhan} / helper thật", _gh_ten_hong, "kiem_github", lease_d,
                             env_them=ENV_GITHUB)
        chot(ra.__class__.__name__ == "_NgoaiLeLa" and type(ra.kieu) is str,
             f"{nhan}: helper THẬT phải TRẢ `_NgoaiLeLa` với tên lớp là `str` thuần, nhận "
             f"{ra.__class__.__name__}.")

        def _gh_ten_hong_base(*_a, _L=_LoiTenBase):
            raise _L()
        loai = "cửa TRẢ VỀ dù helper đã ném"
        try:
            _goi_doi_tra_ve(f"t187 {nhan} / cửa", _gh_ten_hong_base, "kiem_github", lease_d,
                            env_them=ENV_GITHUB)
        except TinHieuChotCa:
            loai = "TinHieuChotCa"
        except BaseException as loi:  # noqa: BLE001 — đo "đỏ ĐÚNG lớp", phải bắt trọn
            loai = f"ngoại lệ TRẦN `{_ten_lop(loi)}`"
        chot(loai == "TinHieuChotCa",
             f"{nhan}: cửa phải đỏ bằng `TinHieuChotCa`, nhận {loai}.")

    # HAI NHÁNH THÔNG ĐIỆP CỦA BỘ CHẠY — cross-review codex lượt 4 (24-09,
    # `diagnostic-normalization-wiring-unmeasured`, P2). Tách `_bao_loi_ca` khỏi `main` làm
    # thông điệp ra khỏi THÂN `except`, tức ra khỏi tầm của `t189` (nó chỉ duyệt thân
    # ExceptHandler) — và phần metaclass ở trên chỉ đo TÊN LỚP. Hai đột biến một dòng
    # (`return str(ex)` ở nhánh `AssertionError`; `f"{_ten_lop(ex)}: {ex}"` ở nhánh còn lại)
    # sống 183/183 trong khi bộ chạy vỡ trần. Nên đo THẲNG cả hai nhánh bằng chính họ `HO`,
    # cộng hai lớp `__str__` hỏng, cộng ĐỐI CHỨNG chuỗi thường giữ nguyên nội dung, rồi đo
    # CHỖ NỐI bằng một lượt `main()` thật.
    class _StrNemBo(Exception):
        def __str__(self):
            raise ValueError("định dạng hỏng")

    class _StrKhongChuoiBo(Exception):
        def __str__(self):
            return 12345          # noqa: RET504 — CỐ Ý trả thứ không phải chuỗi

    class _AssertStrNem(AssertionError):
        def __str__(self):
            raise ValueError("định dạng hỏng")

    def _bao(ex):
        try:
            return _bao_loi_ca(ex)
        except BaseException as loi:  # noqa: BLE001 — đo "không nổ", phải bắt trọn
            return _ChuoiNem(_ten_lop(loi))

    class _ChuoiNem(str):
        """Nhãn "`_bao_loi_ca` NÉM" — `str` con nên `type(r) is str` tự loại nó."""

    nhanh = [(f"nhánh AssertionError / {nhan}", AssertionError(x), None) for nhan, x in HO]
    nhanh += [("nhánh AssertionError / `__str__` NÉM", _AssertStrNem(), None)]
    nhanh += [(f"nhánh Exception / {nhan}", RuntimeError(x), "RuntimeError") for nhan, x in HO]
    nhanh += [("nhánh Exception / `__str__` NÉM", _StrNemBo(), "_StrNemBo"),
              ("nhánh Exception / `__str__` trả thứ không phải chuỗi", _StrKhongChuoiBo(),
               "_StrKhongChuoiBo")]
    for nhan, ex, ten in nhanh:
        r = _bao(ex)
        chot(type(r) is str,
             f"{nhan}: `_bao_loi_ca` phải trả `str` thuần, nhận "
             f"{('NÉM `' + str.__str__(r) + '`') if isinstance(r, _ChuoiNem) else type(r).__name__}.")
        chot(ten is None or r.startswith(f"{ten}: "),
             f"{nhan}: nhánh không-assert phải nêu tên lớp `{ten}` ở đầu, nhận {r!r}.")
    for ex, mong in ((AssertionError(NOI_DUNG), NOI_DUNG),
                     (RuntimeError(NOI_DUNG), f"RuntimeError: {NOI_DUNG}")):
        r = _bao(ex)
        chot(r == mong, f"đối chứng xanh `_bao_loi_ca`: mong {mong!r}, nhận {r!r} — một cài "
                        f"đặt trả hằng cho mọi đầu vào cũng qua các vế trên.")

    # CHỖ NỐI: một lượt `main()` THẬT trên năm ca giả, ném qua CẢ HAI nhánh. `main` phải TRẢ
    # `1`, in dòng tổng kết `0/5` — không vỡ trần giữa chừng — VÀ mỗi dòng `ĐỎ` phải mang ĐÚNG
    # nội dung. Cross-review codex lượt 5 (24-09, `runner-diagnostic-content-not-checked`, P2):
    # bản trước chỉ chốt TIỀN TỐ dòng, nên cho `main` ghi một HẰNG thay cho `_bao_loi_ca(ex)` ở
    # một trong hai nhánh vẫn sống 183/183 — helper có răng, chỗ dùng helper thì không.
    # Kỳ vọng viết TAY, KHÔNG sinh bằng `_bao_loi_ca` (thứ đang bị đo không được làm oracle của
    # chính nó). Hai câu dự phòng của `_thong_diep_an_toan` được ghim nguyên văn: đổi chúng có
    # chủ ý thì phải sửa cả ở đây.
    import contextlib, io
    from unittest import mock

    def _gia_assert_ho():
        raise AssertionError(HO[3][1])

    def _gia_exception_ho():
        raise RuntimeError(HO[0][1])

    def _gia_str_nem():
        raise _StrNemBo()

    def _gia_assert_thuong():
        raise AssertionError(NOI_DUNG)

    def _gia_exception_thuong():
        raise RuntimeError(NOI_DUNG)

    ca_gia = [_gia_assert_ho, _gia_exception_ho, _gia_str_nem, _gia_assert_thuong,
              _gia_exception_thuong]
    MONG_DONG = {
        "_gia_assert_ho": "<__str__ hỏng>",
        "_gia_exception_ho": "RuntimeError: <__str__ hỏng>",
        "_gia_str_nem": "_StrNemBo: <__str__ hỏng>",
        "_gia_assert_thuong": NOI_DUNG,
        "_gia_exception_thuong": f"RuntimeError: {NOI_DUNG}",
    }
    luu, ra = list(CA), io.StringIO()
    try:
        CA[:] = ca_gia
        with mock.patch.object(sys, "argv", ["lease_publish_test.py"]), \
                contextlib.redirect_stdout(ra):
            try:
                rc_main = main()
            except BaseException as loi:  # noqa: BLE001 — đo "bộ chạy không vỡ", bắt trọn
                rc_main = f"NÉM {_ten_lop(loi)}"
    finally:
        CA[:] = luu
    chot(len(CA) == len(luu), "CA không được khôi phục sau lượt `main()` giả.")
    dau_ra = ra.getvalue()
    chot(rc_main == 1, f"`main()` trên năm ca đỏ phải trả 1, nhận {rc_main!r}.")
    # So THEO TỪNG TÊN CA, trên đúng các dòng `  ĐỎ  ` — không tìm chuỗi ở bất kỳ đâu trong
    # log, vì dòng `!!! do` cũng chứa lý do và sẽ che một dòng `ĐỎ` sai.
    dong_do = {}
    for dong in dau_ra.splitlines():
        if dong.startswith("  ĐỎ  "):
            ten, _, ly = dong[len("  ĐỎ  "):].partition(": ")
            dong_do.setdefault(ten, []).append(ly)
    chot(sorted(dong_do) == sorted(MONG_DONG),
         f"`main()` phải in đúng một nhóm dòng ĐỎ cho năm ca giả, nhận tên {sorted(dong_do)!r}.")
    sai = {ten: dong_do.get(ten) for ten, mong in MONG_DONG.items() if dong_do.get(ten) != [mong]}
    chot(not sai, f"`main()` in SAI nội dung dòng ĐỎ: {sai!r}; mong {MONG_DONG!r}.")
    chot("lease_publish: 0/5 đạt; đã chạy=5, bỏ qua=0" in dau_ra,
         "`main()` không in dòng tổng kết `0/5` — bộ chạy vỡ trước khi báo.")

    # ĐỐI CHỨNG XANH: chuỗi thường phải đi qua NGUYÊN VẸN, không bị thay bằng dự phòng.
    thuong = _chuoi_thuan(NOI_DUNG, "<dự phòng>")
    chot(thuong == NOI_DUNG and type(thuong) is str,
         f"đối chứng: chuỗi thường phải giữ nguyên, nhận {thuong!r}. Một cài đặt trả hằng "
         f"cho MỌI đầu vào cũng qua hết các vế trên — vế này là thứ duy nhất bác nó.")


@ca
def t185_cua_DEM_phai_chot_KET_QUA_truoc_khi_chot_SO_LOI_GOI():
    """A20 — đo CHÍNH `_goi_dem_lop_gh`. Cửa mới phải TỰ NÓ có răng, không chỉ có mặt.

    LỚP `CHOT-SO-LOI-GOI-MA-KHONG-CHOT-KET-QUA`, cross-review lượt 6 bắt được bằng phép đo:
    đột biến `R_probe` ném `ValueError` ngay đầu `_do_dau_da_dang`, chỉ với đúng năm đầu vào
    của vế `lease_id` sai kiểu, **SỐNG 177/177** trên head `94d3cd9`.

    Ba vế, mỗi vế một cửa hỏng KHÁC NHAU — không phải ba cách viết của cùng một vế:

      (a) cổng VỠ trước khi chạm mạng nhưng số lời gọi vẫn đúng ⇒ cửa phải ĐỎ ở vế KẾT QUẢ.
          Đây là `R_probe` thu nhỏ. Bỏ vế kết quả khỏi cửa ⇒ vế này XANH.
      (b) cổng kết thúc ĐÚNG mà số lời gọi SAI ⇒ cửa phải ĐỎ ở vế ĐẾM.
          Bỏ vế đếm khỏi cửa ⇒ vế này XANH.
      (c) cổng TRẢ VỀ (không ném) khi ca đòi `DA_TRA_VE` ⇒ cửa phải XANH.
          Thiếu vế này thì (a) và (b) có thể đỏ vì cửa đỏ với MỌI thứ.

    `DA_TRA_VE` là một nhãn RIÊNG chứ không phải `0`: `RC_OK` cũng bằng `0`, nên `ma == 0`
    không phân biệt "không ném" với "ném `Chan(RC_OK)`" — cùng bệnh đã đẻ ra `_MaVang`.
    """
    class _ChotCa(TinHieuChotCa):
        """Tín hiệu RIÊNG của ca này — mã ngoài KHÔNG giả được bằng một `AssertionError`."""

    def _thu(ten_cong, lease, ket_qua_mong_doi, so_goi_mong_doi, cua=None):
        """Chạy cửa; trả `None` nếu XANH, hoặc NHÃN VẾ (`ket_qua`/`dem`) nếu cửa chốt ĐỎ.

        CHỈ nhận `TinHieuCuaDem` — tín hiệu do CHÍNH cửa phát. Mọi thứ khác thoát ra từ cửa
        (kể cả một `AssertionError` mang đúng câu chữ) là cửa HỎNG, không phải cửa đỏ.
        """
        gh = GhGia(comments={55: []})
        try:
            (cua or _goi_dem_lop_gh)(gh, ten_cong, lease, ket_qua_mong_doi, so_goi_mong_doi,
                                     "t185", env_them=ENV_GITHUB)
        except TinHieuCuaDem as loi:
            return loi.ve
        except Exception as loi:  # noqa: BLE001 — cửa ném thứ KHÔNG phải tín hiệu của nó
            raise _ChotCa(f"cửa ném `{_ten_lop(loi)}` thay vì `TinHieuCuaDem` — không phải "
                          f"một chốt đã chạy, nên không được tính là chốt đỏ.") from None
        return None

    # Ba hành vi ĐO ĐƯỢC của cổng, dùng làm nguyên liệu cho ba vế (đo 21-09 trên head này):
    #   `_do_dau_da_dang` + lease hợp lệ  -> KHÔNG ném, 1 lời gọi
    #   `kiem_github`     + lease hợp lệ  -> KHÔNG ném, 3 lời gọi
    #   `kiem_github`     + lease TỰ CẤP  -> Chan(rc=4), 1 lời gọi
    HOP_LE, TU_CAP = _lease_579(), _lease_579(granted_by="codex")

    # (c) ĐỐI CHỨNG XANH trước — nếu nó đỏ thì (a)/(b) không chứng minh được gì.
    #     `_do_dau_da_dang` với lease HỢP LỆ: phép dò hỏi Issue đúng 1 lần rồi TRẢ VỀ.
    xanh = _thu("_do_dau_da_dang", HOP_LE, DA_TRA_VE, 1)
    if xanh is not None:
        raise _ChotCa(f"(c) đối chứng XANH lại ĐỎ ở vế {xanh!r}. Mọi vế sau mất nghĩa.")

    # (b) sai SỐ LỜI GỌI, kết quả vẫn đúng ⇒ phải đỏ ở vế ĐẾM.
    do_dem = _thu("_do_dau_da_dang", HOP_LE, DA_TRA_VE, 99)
    if do_dem is None:
        raise _ChotCa("(b) cửa KHÔNG đỏ khi số lời gọi sai — vế ĐẾM không có răng.")
    if do_dem != "dem":
        raise _ChotCa(f"(b) đỏ nhưng KHÔNG phải ở vế đếm: vế {do_dem!r}")

    # (a) kết quả sai, số lời gọi vẫn đúng ⇒ phải đỏ ở vế KẾT QUẢ.
    #     Lease TỰ CẤP làm `kiem_github` ném `Chan(rc=4)` sau ĐÚNG 1 lời gọi. Ca đòi
    #     `DA_TRA_VE` + 1 lời gọi: vế ĐẾM khớp, vế KẾT QUẢ lệch. Đó chính là hình dạng của
    #     `R_probe` — số đúng, kết cục sai — nên nếu cửa xanh ở đây thì cửa vô dụng.
    do_kq = _thu("kiem_github", TU_CAP, DA_TRA_VE, 1)
    if do_kq is None:
        raise _ChotCa("(a) cửa KHÔNG đỏ khi cổng kết thúc SAI CÁCH trong lúc số lời gọi "
                      "vẫn đúng. Đó CHÍNH LÀ hình dạng đã cho `R_probe` sống 177/177.")
    if do_kq != "ket_qua":
        raise _ChotCa(f"(a) đỏ nhưng KHÔNG phải ở vế kết quả: vế {do_kq!r}")

    # (d) DANH TÍNH TÍN HIỆU — đối chứng HÀNH VI, không chỉ chốt cấu trúc.
    #
    # Cross-review codex lượt 3 (24-09) bác lập luận "muốn suy nhãn từ chuỗi thì phải định dạng
    # ngoại lệ, và `t189` cấm việc đó": đột biến bắt RỘNG rồi suy nhãn từ `loi.args[0]`, hay từ
    # chính `_thong_diep_an_toan(loi)`, đều hợp lệ với `t189` và SỐNG 183/183. Chốt định dạng
    # không khoá được danh tính. Nên đo thẳng: cho `_thu` một cửa GIẢ ném `AssertionError` TRẦN
    # mang ĐÚNG câu chữ thu từ chốt THẬT của từng vế ⇒ `_thu` phải đỏ; và một `TinHieuCuaDem`
    # mang NHÃN một vế với CÂU CHỮ của vế kia ⇒ `_thu` phải trả NHÃN, không trả câu chữ.
    def _cau_chu_that(ten_cong, lease, kq, so):
        try:
            _goi_dem_lop_gh(GhGia(comments={55: []}), ten_cong, lease, kq, so, "t185",
                            env_them=ENV_GITHUB)
        except TinHieuCuaDem as loi:
            return loi.ve, loi.args[0]
        raise _ChotCa(f"(d) cửa thật KHÔNG đỏ với {ten_cong!r} — không thu được câu chữ.")

    def _cua_nem(loi):
        def _f(*_a, **_k):
            raise loi
        return _f

    CAU = dict((_cau_chu_that("_do_dau_da_dang", HOP_LE, DA_TRA_VE, 99),
                _cau_chu_that("kiem_github", TU_CAP, DA_TRA_VE, 1)))
    if set(CAU) != {"dem", "ket_qua"}:
        raise _ChotCa(f"(d) phải thu được câu chữ của CẢ HAI vế, thu được vế {sorted(CAU)!r}.")
    for ve, cau in CAU.items():
        try:
            _thu("_do_dau_da_dang", HOP_LE, DA_TRA_VE, 1, cua=_cua_nem(AssertionError(cau)))
        except _ChotCa:
            pass
        else:
            raise _ChotCa(f"(d) vế {ve!r}: `_thu` NHẬN một `AssertionError` TRẦN mang đúng câu "
                          f"chữ của chốt thật như thể chốt đã chạy — tín dụng giả.")
    for ve, khac in (("dem", "ket_qua"), ("ket_qua", "dem")):
        nhan_ra = _thu("_do_dau_da_dang", HOP_LE, DA_TRA_VE, 1,
                       cua=_cua_nem(TinHieuCuaDem(ve, CAU[khac])))
        if nhan_ra != ve:
            raise _ChotCa(f"(d) nhãn {ve!r} mang câu chữ của vế {khac!r}: `_thu` phải trả NHÃN "
                          f"{ve!r}, trả {nhan_ra!r} — nó đang đọc câu chữ.")


@ca
def t186_KHONG_ca_nao_duoc_chot_SO_LOI_GOI_ngoai_CUA():
    """A21 — chốt CẤU TRÚC: cấm mọi so sánh `len(<x>.calls)` nằm ngoài `_goi_dem_lop_gh`.

    Không có ca này thì bản vá lượt 6 chỉ sống tới lần ai đó viết lại
    `chot(len(gh.calls) == 0, ...)` trong một ca mới — và lỗ mở lại trong im lặng, đúng cách
    nó đã mở lần đầu. Cùng nếp với bài học "danh sách CẤM không bao giờ đủ": ở đây danh sách
    CHO PHÉP chỉ có MỘT phần tử và biết trước, nên nó đóng được.

    Đo bằng `ast`, KHÔNG bằng `grep`: câu hỏi là một SỰ KIỆN CẤU TRÚC ("có phép so sánh nào
    trên `len(....calls)` không"), mà mẫu văn bản trả lời một câu KHÁC ("có chỗ nào TRÔNG
    GIỐNG"). Chính tệp đặc tả của #574 vừa ghi hai lần trả giá cho việc lẫn hai câu ấy.

    KHÔNG cấm mọi phép đọc `.calls`: `t48` chốt `not any(x[0] == "POST" for x in gh.calls)`
    — đó là một VỊ TỪ về việc đã xảy ra, không phải một SỐ ĐẾM, và nó nằm chung biểu thức
    với vế kết quả (`ex.ma == RC_NOI_DUNG`). Cấm nó là chặn oan một ca đang đo đúng.
    """
    import ast as _ast
    nguon = Path(__file__).read_text(encoding="utf-8")
    cay = _ast.parse(nguon)

    CHO_PHEP = {"_goi_dem_lop_gh"}
    pham = []

    class _Di(_ast.NodeVisitor):
        def __init__(self):
            self.trong = []

        def visit_FunctionDef(self, nut):
            self.trong.append(nut.name)
            self.generic_visit(nut)
            self.trong.pop()

        def visit_Compare(self, nut):
            for ve in [nut.left] + list(nut.comparators):
                if (isinstance(ve, _ast.Call) and isinstance(ve.func, _ast.Name)
                        and ve.func.id == "len" and len(ve.args) == 1
                        and isinstance(ve.args[0], _ast.Attribute)
                        and ve.args[0].attr == "calls"):
                    if not (self.trong and self.trong[-1] in CHO_PHEP):
                        pham.append((nut.lineno, self.trong[-1] if self.trong else "<mức module>"))
                    break
            self.generic_visit(nut)

    _Di().visit(cay)
    chot(not pham,
         "chốt SỐ LỜI GỌI phải đi qua `_goi_dem_lop_gh` — cửa ấy chốt CẢ vế KẾT QUẢ, và "
         "thiếu vế kết quả là thứ đã cho đột biến `R_probe` sống 177/177. Vi phạm: "
         + " · ".join(f"dòng {d} trong `{h}`" for d, h in pham))

    # ĐỐI CHỨNG: bộ dò phải THẤY được hình dạng bị cấm, nếu không nó chỉ đang đếm số không.
    thu = _ast.parse("def ca_gia():\n    chot(len(gh.calls) == 0, 'x')\n")
    thay = []

    class _Di2(_Di):
        pass

    d2 = _Di2()
    pham.clear()
    d2.visit(thu)
    thay = list(pham)
    pham.clear()
    chot(len(thay) == 1,
         f"bộ dò của chính ca này KHÔNG thấy hình dạng bị cấm khi bơm vào (thấy {len(thay)}). "
         f"Một phép kiểm không thể ĐỎ thì không phải bằng chứng.")

@ca
def t174_GOI_GIT_giai_ma_dong_bo_va_giu_hop_dong_text():
    """Real subprocess bytes: strict errors reach the caller, never a reader thread."""
    import contextlib
    import io
    from unittest import mock
    mod = _nap_cong()
    real_run = subprocess.run
    valid_out = "Tiếng Việt\r\ndòng hai\r".encode("utf-8")
    valid_err = "cảnh báo\r\n".encode("utf-8")
    for out_bytes, err_bytes, bad in ((valid_out, valid_err, False),
                                      (b"\xff", b"", True),
                                      (b"ok\n", b"\xff", True)):
        script = ("import os,sys; "
                  f"sys.stdout.buffer.write(bytes.fromhex('{out_bytes.hex()}')); "
                  f"sys.stderr.buffer.write(bytes.fromhex('{err_bytes.hex()}')); "
                  "sys.exit(7)")
        def child(args, **kwargs):
            chot(args == ["git", "probe"], "real subprocess adapter argv")
            return real_run([sys.executable, "-c", script], **kwargs)
        error = None
        with contextlib.redirect_stderr(io.StringIO()) as captured:
            with mock.patch.object(mod.subprocess, "run", side_effect=child):
                try:
                    result = mod.GOI_GIT("probe")
                except UnicodeDecodeError as exc:
                    error = exc
        chot("Traceback" not in captured.getvalue(), "decoder leaked reader-thread traceback")
        if bad:
            chot(error is not None, "invalid UTF-8 must raise synchronously")
        else:
            chot(error is None and result.returncode == 7
                 and result.stdout == "Tiếng Việt\ndòng hai\n"
                 and result.stderr == "cảnh báo\n", "text/returncode contract changed")

@ca
def t188_moi_ve_DOI_TRA_VE_cua_t184_phai_qua_CUA_chi_ve_d_duoc_goi_tran():
    """A19(e) — chốt CẤU TRÚC cho cửa `_goi_doi_tra_ve`, cùng nếp với `t186`.

    Cross-review codex 24-09 (`return-contract-unwrapped-arms`, P2): lượt 6 đòi MỌI vế "phải
    trả về" của `t184` đo từ phía người gọi, bản vá dựng cửa `_goi_doi_tra_ve` và docstring
    của cửa khai *"cách duy nhất trong tệp"* — trong khi vế (a) và (c) vẫn gọi `_goi_lop_gh`
    TRẦN, và vế (e) tự viết một `try` riêng song song với cửa. Đột biến nhánh trả `Chan`
    thành `raise` làm `t184` chết bằng `Chan` trần TRƯỚC `chot`: ca đỏ đúng mà không đo gì.

    Không có ca này thì bản vá chỉ sống tới lần ai đó thêm một vế mới gọi trần. Danh sách CHO
    PHÉP có đúng MỘT phần tử và biết trước: vế (d), nơi `KeyboardInterrupt` PHẢI xuyên qua
    helper — vế ấy đo điều NGƯỢC LẠI với "trả về", nên nó không được qua cửa.

    Đo bằng `ast`, không bằng `grep`, vì câu hỏi là CẤU TRÚC: lời gọi nằm trong THÂN một `try`
    có nhánh bắt `KeyboardInterrupt` hay không. Kèm PHẢN CHỨNG trên mã giả để chốt không mù.
    """
    import ast as _ast

    def _vi_pham(cay):
        ham = [n for n in cay.body
               if isinstance(n, _ast.FunctionDef) and n.name.startswith("t184_")]
        if len(ham) != 1:
            return None, [f"tìm thấy {len(ham)} hàm `t184_*`, cần đúng 1"], 0
        cha = {}
        for n in _ast.walk(ham[0]):
            for c in _ast.iter_child_nodes(n):
                cha[c] = n

        def _trong_than_try_ctrl_c(nut):
            while nut in cha:
                tren = cha[nut]
                if (isinstance(tren, _ast.Try) and nut in tren.body and any(
                        isinstance(h.type, _ast.Name) and h.type.id == "KeyboardInterrupt"
                        for h in tren.handlers)):
                    return True
                nut = tren
            return False

        def _goi(ten):
            return [c for c in _ast.walk(ham[0]) if isinstance(c, _ast.Call)
                    and isinstance(c.func, _ast.Name) and c.func.id == ten]

        tran = _goi("_goi_lop_gh")
        pham = [f"dòng {c.lineno}" for c in tran if not _trong_than_try_ctrl_c(c)]
        if len(tran) - len(pham) != 1:
            pham.append(f"cần ĐÚNG MỘT lời gọi trần hợp lệ (vế d), thấy {len(tran) - len(pham)}")
        return tran, pham, len(_goi("_goi_doi_tra_ve"))

    _tran, pham, so_cua = _vi_pham(_ast.parse(Path(__file__).read_text(encoding="utf-8")))
    chot(not pham,
         "mọi vế ĐÒI TRẢ VỀ của `t184` phải qua cửa `_goi_doi_tra_ve`; chỉ vế (d) được gọi "
         "`_goi_lop_gh` trần, và phải nằm trong thân `try … except KeyboardInterrupt`. Vi phạm: "
         + " · ".join(pham))
    chot(so_cua >= 5,
         f"`t184` phải có ít nhất 5 lời gọi qua cửa — vế (a) (a2) (b) (c) (e) — thấy {so_cua}. "
         f"Ít hơn nghĩa là một vế đã bị GỠ chứ không phải được bọc.")

    # PHẢN CHỨNG: chốt phải BẮT được một lời gọi trần ngoài `try`, và THA đúng hình dạng (d).
    gia = _ast.parse(
        "def t184_gia():\n"
        "    ex, m = _goi_lop_gh(1, 'x')\n"
        "    try:\n"
        "        _goi_lop_gh(2, 'y')\n"
        "    except KeyboardInterrupt:\n"
        "        pass\n")
    _t, pham_gia, _c = _vi_pham(gia)
    chot(pham_gia == ["dòng 2"],
         f"phản chứng: chốt phải bắt ĐÚNG lời gọi trần ở dòng 2 và tha lời gọi trong "
         f"`try … except KeyboardInterrupt`, nhận {pham_gia!r}. Chốt không bắt được mã giả "
         f"thì nó không chứng minh được gì về mã thật.")


@ca
def t189_duong_chan_doan_KHONG_dinh_dang_THO_ngoai_le_vua_bat():
    """A22 — chốt CẤU TRÚC: trong MIỀN chẩn đoán của packet, mọi ngoại lệ bắt RỘNG phải định
    dạng qua `_ten_lop` / `_thong_diep_an_toan`, không được viết thô.

    Cross-review codex lượt 2 (24-09): bản vá lượt 1 hạ tên lớp ở hai wrapper nhưng nhánh báo
    lỗi của cửa `_goi_doi_tra_ve` vẫn viết `type(loi).__name__` thô. Liệt kê bằng `ast` trên
    toàn tệp ra 24 chỗ định dạng một ngoại lệ vừa bắt; trong đó các chỗ THUỘC PACKET và bộ
    chạy `main` đã gom về hai cửa. Ca này giữ cho chúng không mọc lại.

    MIỀN là danh sách CHO PHÉP, nhỏ và biết trước: các helper chẩn đoán, các cửa, `main`, và
    các ca đo chính thước đo (`t184`–`t189`). Ngoài miền là mã kế thừa từ master — sáu chỗ
    (`t69`, `t90`, `t92`, `t125`-rig, `t139`, `_danh_gia_bieu_thuc_chuan_bi`) được KHAI là nợ,
    không lặng lẽ sửa trong một packet `sensitive`.

    "Bắt RỘNG" = không kiểu, `Exception`, `BaseException`, `AssertionError` (hoặc tuple chứa
    chúng) — những nhánh có thể nhận một đối tượng TUỲ Ý. Bắt lớp cụ thể của sản phẩm
    (`mod.Chan`, `OSError`, `TinHieuChotCa`…) thì tên và thông điệp do mã đã biết dựng.
    Đo bằng `ast` kèm PHẢN CHỨNG trên mã giả để chốt không mù.
    """
    import ast as _ast
    MIEN_TEN = {"_goi_doi_tra_ve", "_goi_dem_lop_gh", "_goi_lop_gh", "_thong_diep_an_toan",
                "_chuoi_thuan", "_ten_lop", "_bao_loi_ca", "_chot_cua_dem", "main",
                "_MaVang", "_NgoaiLeLa", "TinHieuCuaDem"}
    TIEN_TO = ("t184_", "t185_", "t186_", "t187_", "t188_", "t189_")
    RONG = {"Exception", "BaseException", "AssertionError"}

    def _rong(h):
        if h.type is None:
            return True
        ds = h.type.elts if isinstance(h.type, _ast.Tuple) else [h.type]
        return any(isinstance(x, _ast.Name) and x.id in RONG for x in ds)

    def _vi_pham(cay):
        mien = [n for n in cay.body if isinstance(n, (_ast.FunctionDef, _ast.ClassDef))
                and (n.name in MIEN_TEN or n.name.startswith(TIEN_TO))]
        pham = []
        for goc in mien:
            for h in _ast.walk(goc):
                if not (isinstance(h, _ast.ExceptHandler) and h.name and _rong(h)):
                    continue
                v = h.name
                for n in (x for st in h.body for x in _ast.walk(st)):
                    if isinstance(n, _ast.FormattedValue) and isinstance(n.value, _ast.Name) \
                            and n.value.id == v:
                        pham.append((n.lineno, goc.name, "{%s}" % v))
                    elif isinstance(n, _ast.Call) and isinstance(n.func, _ast.Name) \
                            and n.func.id in ("str", "repr") and n.args \
                            and isinstance(n.args[0], _ast.Name) and n.args[0].id == v:
                        pham.append((n.lineno, goc.name, f"{n.func.id}({v})"))
                    elif isinstance(n, _ast.Attribute) and n.attr == "__name__" \
                            and isinstance(n.value, _ast.Call) \
                            and isinstance(n.value.func, _ast.Name) and n.value.func.id == "type" \
                            and n.value.args and isinstance(n.value.args[0], _ast.Name) \
                            and n.value.args[0].id == v:
                        pham.append((n.lineno, goc.name, f"type({v}).__name__"))
        return len(mien), sorted(set(pham))

    so_mien, pham = _vi_pham(_ast.parse(Path(__file__).read_text(encoding="utf-8")))
    chot(so_mien >= 12,
         f"miền đọc được phải có ít nhất 12 định nghĩa, đọc được {so_mien}. Miền hụt làm chốt "
         f"dưới đây thành chốt KHÔNG THỂ ĐỎ.")
    chot(not pham,
         "đường chẩn đoán phải định dạng ngoại lệ vừa bắt qua `_ten_lop`/`_thong_diep_an_toan`. "
         "Vi phạm: " + " · ".join(f"dòng {d} `{h}` {k}" for d, h, k in pham))

    # PHẢN CHỨNG: ba dạng thô bị bắt; dạng đi qua cửa và nhánh bắt lớp CỤ THỂ được tha.
    gia = _ast.parse(
        "def main():\n"
        "    try:\n"
        "        f()\n"
        "    except Exception as e:\n"
        "        a = f'{type(e).__name__}'\n"
        "        b = str(e)\n"
        "        c = f'{e}'\n"
        "        d = f'{_ten_lop(e)} {_thong_diep_an_toan(e)}'\n"
        "    try:\n"
        "        f()\n"
        "    except OSError as o:\n"
        "        z = f'{o}'\n")
    _n, pham_gia = _vi_pham(gia)
    chot([(d, k) for d, _h, k in pham_gia] == [(5, "type(e).__name__"), (6, "str(e)"), (7, "{e}")],
         f"phản chứng: phải bắt ĐÚNG ba dạng thô ở dòng 5/6/7 và tha dòng 8 (qua cửa) cùng nhánh "
         f"`OSError`, nhận {pham_gia!r}.")


def main() -> int:
    qua, hong, bo_qua = 0, [], []
    # Selector không khớp ca nào ⇒ KHÔNG chạy gì và KHÔNG xanh (cross-review codex 11-09-2026, P2).
    # Bản trước in `lease_publish: 0/0 đạt` rồi rc=0: một cổng VẮNG MẶT trông y hệt một cổng XANH, nên
    # một prefix gõ sai hay một tên ca đã đổi sinh ra phép đo giả. Dòng lỗi dưới đây CỐ Ý không khớp
    # regex dòng tổng kết, để không ai đọc nó thành một kết quả.
    cac_co = [x for x in sys.argv[1:] if x.startswith(CO_CHI_CA)]
    if cac_co:
        tien_to = cac_co[-1][len(CO_CHI_CA):]
        cac_ca = [fn for fn in CA if fn.__name__.startswith(tien_to)]
        if not tien_to or not cac_ca:
            vi = "RỖNG" if not tien_to else "không khớp ca nào"
            print(f"chon-ca SAI: tiền tố {tien_to!r} {vi} (có {len(CA)} ca) — KHÔNG chạy gì, "
                  f"rc={RC_CHON_CA_SAI}", file=sys.stderr, flush=True)
            return RC_CHON_CA_SAI
    else:
        cac_ca = list(CA)
    for fn in cac_ca:
        _nhat_ky_ca(">>> vao", fn.__name__, datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"))
        t0 = time.monotonic()
        ket = "QUA"
        try:
            fn()
            qua += 1
        except BoQuaNen as ex:
            try: ly_do = _ly_do_bo_qua_workflow(ex.tep, ex.ten_job)
            except Exception: ly_do = ""
            if ly_do:
                bo_qua.append((fn.__name__, ly_do)); ket = "BO_QUA"
            else:
                hong.append((fn.__name__, "bỏ qua không dẫn xuất được từ runs-on")); ket = "DO"
        except AssertionError as ex:
            # Bộ chạy là đường chẩn đoán của MỌI ca — nó không được nổ khi báo lỗi.
            hong.append((fn.__name__, _bao_loi_ca(ex))); ket = "DO"
        except Exception as ex:  # noqa: BLE001
            hong.append((fn.__name__, _bao_loi_ca(ex))); ket = "DO"
        _nhat_ky_ca("<<< ra", fn.__name__, f"{time.monotonic() - t0:.3f}s", ket)
        if ket == "DO":
            # In LÝ DO ngay tại chỗ (M4 lần 2, packet #504): danh sách `  ĐỎ  …` chỉ in ở cuối suite, nên khi job
            # bị huỷ giữa chừng thì mọi lý do đã đo được mất theo. Tiền tố khác hẳn để không trùng dòng tổng kết.
            _nhat_ky_ca("!!! do", fn.__name__, hong[-1][1].replace("\n", " ")[:700])
    for ten, ly in bo_qua:
        print(f"  BỎ QUA {ten}: {ly}")
    for ten, ly in hong:
        print(f"  ĐỎ  {ten}: {ly}")
    print(_dong_tong_ket(qua, len(cac_ca) - len(bo_qua), len(bo_qua)))
    return 1 if hong else 0


if __name__ == "__main__":
    sys.exit(main())
