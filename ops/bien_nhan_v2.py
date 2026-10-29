#!/usr/bin/env python3
"""Cổng LƯỢC ĐỒ v2 cho `ops/reviews/*.receipt.yaml` — thi công `PROTOCOL §8` (dòng 453–458).

VÌ SAO CÓ. Protocol đặc tả lược đồ v2 từ `2f84531` (18-08-2026) và **chưa ai thi công**:
đo trên `3bc2895` — `rg` không thấy `model_reviewer_identity` / `github_submitter_identity` /
`receipt_id` trong bất kỳ bộ kiểm biên nhận nào, và `t26` chỉ kiểm `verdict_path` + băm.
Chính hai biên nhận v2 đầu tiên của kho đã TỰ KHAI khoảng trống ấy
(`PLAT-X8b-CHUA-CO-BO-KIEM-RECEIPT-V2`: *"`t26` không đọc `schema_version`, không đòi hai
identity, không đọc `anchor`. Cổng chưa từng validate một receipt v2."*). Nợ đó đóng ở đây.

Cò trực tiếp: cross-review của codex trên PR #454 (`3d5eaeb`, finding P2) bắt được biên nhận
lượt 5 khai `assurance: cross_approved` trong khi thiếu **cả bốn** thứ v2 đòi, và tự khai model
identity là KHÔNG ĐO ĐƯỢC ở ngay trong tệp. Đo lại thì đó là **LỚP**, không phải một tệp:
62 biên nhận · 10 khai v2 · **4 đủ** · **6 thiếu**.

BA TRẠNG THÁI, không phải hai — `0` sạch · `1` vi phạm · `2` KHÔNG ĐO ĐƯỢC.
Trạng thái thứ ba (thiếu thư mục trong kho thật, YAML hỏng, thiếu PyYAML) làm cổng ĐỎ chứ không
im lặng thành "sạch": một cổng tự tắt khi thiếu công cụ là cổng không tồn tại đúng lúc cần nhất.

HAI DANH SÁCH ĐÓNG BĂNG, và cả hai neo bằng **tên tệp + băm** chứ không bằng tên suông:

  `ALLOWLIST_CUTOVER` — đúng **11** biên nhận v1 mà protocol miễn trừ, xác định bằng phép đo
  chứ không bằng trí nhớ: `git ls-tree -r 2f84531 -- ops/reviews/` cho ĐÚNG 11 tệp
  `*.receipt.yaml`, tất cả `schema_version: 1`. Cả 11 vẫn byte-identical với bản tại cutover
  (đo 06-09-2026). Protocol nói thẳng *"`schema_version: 1` do tác giả tệp mới tự khai KHÔNG
  tạo miễn trừ"* — nên miễn trừ neo vào BĂM: sửa một tệp trong danh sách là mất miễn trừ, và
  đó là ĐỎ chứ không phải im lặng.

  `NO_DA_DO` — nợ ĐÃ ĐO, **chỉ được co lại**. Đây là 41 biên nhận tự khai v1 SAU cutover cộng
  các biên nhận v2 chưa đủ trường. Vì sao không bắt sửa hết ngay: điền `model_reviewer_identity`
  cho một lượt review đã chạy xong từ lâu là **bịa bằng chứng danh tính** — đúng thứ lược đồ v2
  sinh ra để chặn. Nên chúng bị ĐÓNG BĂNG THEO BĂM: đụng vào một tệp nợ là ĐỎ (sửa thì sửa cho
  đúng v2), thêm tệp mới vào danh sách là ĐỎ ở `ops/bien_nhan_v2_test.py`. Bánh cóc chỉ quay
  một chiều.

CÂU LỊCH SỬ (#960, `ops/specs/NO-CAU-LICH-SU-BIEN-NHAN.md`) — ngoại lệ DUY NHẤT cho câu "chỉ kiểm cấu
trúc" dưới đây: ba luật L-REVIEW · L-ANCESTRY · L-SURFACE đo SỰ THẬT của câu phụ thuộc thời điểm
(`reviewed_sha` của biên nhận khác, `merge-base` với nhánh mặc định, `run.json`). Nợ hiện có đóng
băng ở `NO_CAU_LICH_SU`, chỉ được co. Regex chỉ chọn ứng viên — câu viết lọt regex là câu KHÔNG đo.

ĐIỀU CỔNG NÀY **KHÔNG** LÀM, khai thẳng kẻo ai đọc "xanh" thành nhiều hơn thực tế:
  · Nó kiểm **CẤU TRÚC**, không kiểm **SỰ THẬT**. `model_reviewer_identity` có mặt và đủ khoá
    không chứng minh model nào đã review — chính bốn biên nhận đạt đều tự khai `KHONG_do_duoc`
    cho ID model. Một biên nhận bịa nguyên khối identity vẫn qua cổng này.
  · Nó không kiểm `github_submitter_identity` có đúng người đăng hay không, và `ADR-0040` nói
    rõ biên nhận do tài khoản tác giả đăng KHÔNG thành required check.
  · **Nó KHÔNG chứng minh identity là THẬT.** `model_reviewer_identity` đủ khoá không chứng
    minh model nào đã review — bốn biên nhận v2 chuẩn của kho đều tự khai `KHONG_do_duoc` cho
    ID model, và đó là trạng thái ĐÚNG. Một biên nhận bịa nguyên khối identity vẫn qua cổng này.
  · Nó không kiểm `github_submitter_identity` có đúng người đăng hay không; `ADR-0040` nói rõ
    biên nhận do tài khoản tác giả đăng KHÔNG thành required check.
  · Nó KHÔNG chứng minh canonical ancestry, ref protection hay thẩm quyền trên GitHub —
    `_neo_git` chỉ chứng minh **object có thật, đường dẫn có thật, và blob khớp băm đã khai**.
  · Với người audit (`human`) cũng vậy: `phien_doc_lap: true` là LỜI KHAI độc lập của người
    ký, và danh tính GitHub bền mà `PROTOCOL §8` đòi KHÔNG đo được từ một tệp trong kho — cổng
    chỉ kiểm hợp đồng (`manual_audit`/`human`), mức được khai, và mỏ neo git của bản chiếu.

MỘT TIỀN ĐỀ SAI ĐÃ ĐƯỢC RÚT — ghi lại vì cái sai đáng nhớ hơn bản vá. Bản đầu KHÔNG kiểm
mỏ neo bằng git và khai thành nợ `BIEN-NHAN-V2-KHONG-KIEM-SHA-CO-THAT`, với lý do
*"`actions/checkout` mặc định `depth: 1` nên `git cat-file -e` sẽ ĐỎ GIẢ trên CI"*. Lý do ấy
**SAI trên chính kho này**: `.github/workflows/ci.yml:86` đã đặt `fetch-depth: 0` từ `r226`,
kèm chú thích giải thích ĐÚNG cái bẫy được viện dẫn — kho đã trả giá và đã chữa từ lâu. Tôi
khai một ràng buộc mà KHÔNG ĐO nó, rồi viết tiền đề ấy vào docstring, commit, CHANGELOG và
mô tả PR như một đánh đổi kỹ thuật có lý. Cross-review PR #455 (F4) bắt được bằng cách đọc
chính tệp workflow. Hậu quả đo được lúc ấy: `reviewed_sha` = `'deadbeef'*5` (40 hex, không
tồn tại) QUA CỔNG, và `'khong-phai-sha-gi-ca'` cũng QUA — vì trường ấy chỉ cần "chuỗi không
rỗng". Nay `_neo_git` đo thật, và thiếu object là KHÔNG ĐO ĐƯỢC chứ không phải "bịa".

Phản chứng chạy được: `ops/bien_nhan_v2_test.py`.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import subprocess
import sys
from pathlib import Path

RC_SACH = 0
RC_VI_PHAM = 1
RC_KHONG_DO_DUOC = 2

THU_MUC = "ops/reviews"

# --- Lược đồ v2 tối thiểu, chép theo `PROTOCOL §8` dòng 453-454 -------------------------
# "Đích v2 tối thiểu có `schema_version: 2`, receipt ID, `reviewed_sha`, verdict path/hash,
#  hai identity ở trên, evidence URL và khai loại/cường độ mỏ neo."
_HEX40 = re.compile(r"\A[0-9a-f]{40}\Z")
_HEX64 = re.compile(r"\A[0-9a-f]{64}\Z")
# `blob/<40hex>/<đường dẫn>` trong `evidence_url` của mỏ neo `canonical_ancestry`.
_BLOB_URL = re.compile(r"/blob/([0-9a-f]{40})/(.+)\Z")

# `ANCHOR_KHOA` ĐÃ BỎ: sau khi tách `anchor` thành ba yêu cầu độc lập, không đường nào
# đọc nó nữa. Giữ lại một hằng chết là để dành chỗ cho một đột biến KHÔNG CÓ RĂNG —
# `m6` nhắm vào nó và lập tức mất răng đúng lúc bản vá làm nó vô dụng.


def _chuoi(v):
    """Giá trị CHỈ được coi là LỜI KHAI khi nó là CHUỖI không rỗng.

    `str(v or "").strip()` biến MỌI thứ thành lời khai: `{fake: 1}` ra `"{'fake': 1}"`,
    một danh sách ra `"[...]"`. Cross-review connector trên head `4ef73e6` (P1) đo được
    `surface: {fake: 1}` cộng `KHONG_do_duoc: {fake: 1}` ⇒ `_thieu` trả **KHÔNG vi phạm
    nào**, nên một biên nhận không có bề mặt thực thi hợp lệ **lẫn** lời giải thích vẫn
    lĩnh `cross_approved`.

    ĐÂY LÀ MỘT LỚP, KHÔNG PHẢI HAI TRƯỜNG. Vòng trước tôi vá đúng lớp ấy cho
    `session_run_id` và `phien_doc_lap` rồi **dừng lại** — bỏ sót hai trường trong CÙNG
    một hàm. Vá một lớp bằng cách sửa những chỗ mình vừa nhìn thấy là vá một danh sách,
    không phải vá một lớp; nên nay MỌI trường attestation đi qua đúng một cửa này."""
    return v.strip() if isinstance(v, str) and v.strip() else None


def _co_chuoi(d, k):
    v = d.get(k)
    return None if isinstance(v, str) and v.strip() else f"thiếu/rỗng `{k}`"


def _khop(d, k, re_, mo_ta):
    v = d.get(k)
    if not isinstance(v, str) or not v.strip():
        return f"thiếu/rỗng `{k}`"
    return None if re_.match(v.strip()) else f"`{k}`={v.strip()[:24]!r} không phải {mo_ta}"


# LUẬT THEO PROVIDER, chép tay có NEO. `AGENTS.md` §4 nói tường minh cho ChatGPT Web:
# *"không được … tự tạo `cross_approved`, `same_provider_approved` hoặc `human_audited`"*,
# và *"Review của ChatGPT Web được ghi là `advisory_review`"*. Luật ấy là VĂN XUÔI — không
# rút được bằng máy — nên nó nằm đây; `_provider_chinh_tac` đòi câu biện minh CÒN TRONG
# nguồn luật, mất thì trạng thái THỨ BA.
#
# VÌ SAO CÓ: cross-review connector trên `670071b` (P1). Bản vá vòng trước NỚI danh sách
# provider để nhận `openai_chatgpt` — đúng — nhưng chỉ mang theo cái TÊN, không mang theo
# GIỚI HẠN của nó. Đo được: `{provider: openai_chatgpt, surface: banana,
# session_run_id: …}` + `assurance: cross_approved` ⇒ **0 vi phạm**. Một lượt advisory biến
# thành bằng chứng identity có thẩm quyền. Nhận một tên vào danh sách CHO PHÉP mà bỏ lại
# ràng buộc đi kèm nó là nới quyền, không phải sửa lỗi bắt oan.
#
# MỖI LUẬT CHÉP TAY = (tên luật, tệp nguồn, câu phải còn NGUYÊN VĂN trong tệp ấy). Hai câu
# sau (R7-02) neo phân vùng NGƯỜI/MÔ HÌNH của mức assurance vào `PROTOCOL §8` mục 1-3 —
# xem `ASSURANCE_CUA_NGUOI`/`ASSURANCE_CUA_MO_HINH` bên dưới.
NGUON_LUAT = ("AGENTS.md", "docs/PROTOCOL_DA_PHIEN.md")
_NEO_LUAT_CHEP_TAY = (
    ("ASSURANCE_CAM_THEO_PROVIDER[openai_chatgpt]", "AGENTS.md",
     "tự tạo `cross_approved`, `same_provider_approved` hoặc `human_audited`"),
    ("ASSURANCE_CUA_NGUOI", "docs/PROTOCOL_DA_PHIEN.md",
     "`human_audited`: người audit có danh tính bền trên GitHub"),
    ("ASSURANCE_CUA_MO_HINH", "docs/PROTOCOL_DA_PHIEN.md",
     "`cross_approved`: reviewer và executor dùng hai họ model độc lập phục vụ lượt chạy (ví dụ họ Claude review họ Codex hoặc ngược lại)"),
)
ASSURANCE_CAM_THEO_PROVIDER = {
    "openai_chatgpt": frozenset({"cross_approved", "same_provider_approved", "human_audited"}),
}
# Mức bằng chứng model và bảng họ model mặc định cho cross_approved (ADR-0050, PR #551).
MUC_BANG_CHUNG_MODEL = frozenset({"do_may", "khai_co_audit", "khong_do_duoc"})
HO_MODEL_CHO_PHEP = frozenset({"claude", "gpt", "gemini"})
HO_MODEL_MAC_DINH = {
    "anthropic_claude": "claude", "openai_codex": "gpt", "openai_chatgpt": "gpt",
    "anthropic": "claude", "claude": "claude", "codex": "gpt", "chatgpt": "gpt",
}


# LƯỢC ĐỒ TỪNG BẢNG NGUỒN — tên cột theo thứ tự. `lenh` là bộ tên lệnh (tuple chuỗi), cột
# khác là chuỗi không rỗng. Cross-review lượt 7 (`R7-01`, P2) đo được trên 68 biên nhận nguyên
# byte: `_bang` bản trước trả hàng BẤT KỲ số cột và hai vòng unpack bí danh nằm NGOÀI khối
# bắt lỗi ⇒ hàng thiếu cột là `ValueError` lúc IMPORT, CLI chết `rc=1` không stdout; kiểm kiểu
# chỉ áp cho TÊN provider ⇒ surface/transport `None` thành hợp đồng `[None]` và **9 biên nhận
# nguyên byte bị KẾT TỘI, 0 chưa đo**. Cùng hình dạng "lỗi ĐO thành lỗi DỮ LIỆU" (`R4-02`),
# lần này ở ngay nơi TẠO dữ liệu nguồn. Bảng có cấu trúc thì phải được kiểm ĐỦ cấu trúc.
_LUOC_DO_BANG = {
    "_TRANSPORT_CONTRACTS": ("provider", "lenh", "execution_surface", "transport"),
    "_PROVIDER_NGOAI_CLI":  ("provider", "execution_surface", "transport"),
    "_PROVIDER_BI_DANH":    ("bi_danh", "provider"),
    "_BE_MAT_BI_DANH":      ("bi_danh", "execution_surface"),
}


def _provider_chinh_tac():
    """Đọc tên provider từ TỪ VỰNG CHÍNH TẮC của kho, không chép tay.

    Trả **(tập, lý do hỏng)** — hai giá trị, vì đây là chỗ ba trạng thái phải sống.

    Bản chép tay TỪ CHỐI `anthropic_claude` — chính là tên trong `_TRANSPORT_CONTRACTS`
    của `launcher.py` — tức một biên nhận Claude hợp lệ mới tạo sẽ rớt cổng CI bắt buộc
    (cross-review vòng 3, P2).

    VÀ BẢN VÁ ẤY TỰ SINH RA LỖI KẾ TIẾP, cross-review vòng 4 (`R4-02`) đo được: bản trước
    NUỐT ngoại lệ rồi trả tập RỖNG, nên khi thiếu `launcher.py` thì `PROVIDER_CHO_PHEP`
    tụt về đúng hai bí danh lịch sử và cổng **KẾT TỘI** một biên nhận `openai_codex` hợp lệ
    là *"chuỗi tự do không phải attestation"* — `rc=1`, `1 vi phạm`, **0 chưa đo**. Một lỗi
    ĐO bị báo thành lỗi DỮ LIỆU, tức người đọc sẽ đi sửa hiện vật đúng. Docstring bản
    trước còn viết *"đọc không được thì KHAI ra, không im lặng"* trong khi mã làm ngược
    lại — lời khai rộng hơn phép đo, ngay trong chỗ nói về nó.

    Nay lý do hỏng được GIỮ và đưa tới trạng thái **KHÔNG ĐO ĐƯỢC** của CLI (`rc=2`), và
    phép kiểm danh sách provider KHÔNG chạy khi nguồn không đọc được — vì không đo được
    thì không kết luận được, theo cả hai chiều. Cổng vẫn ĐỎ, nên đây không phải fail-open:
    nó chỉ đỏ ĐÚNG LÝ DO."""
    goc = Path(__file__).resolve().parent.parent
    nguon = goc / ".claude" / "dev" / "launcher.py"
    tv = goc / "AGENTS.md"
    try:
        import ast
        van_launcher = nguon.read_text(encoding="utf-8")
        # NGUỒN LUẬT — `AGENTS.md` (đối chiếu hợp đồng + neo luật §4) và `PROTOCOL` (neo
        # phân vùng người/mô hình, R7-02). Thiếu một tệp là thiếu nguồn, không phải "luật
        # vẫn đúng".
        van_luat = {t: (goc / t).read_text(encoding="utf-8") for t in NGUON_LUAT}
        van_agents = van_luat["AGENTS.md"]
    except (OSError, UnicodeDecodeError) as ex:
        # `UnicodeDecodeError` KHÔNG phải `OSError`. Cross-review vòng 5 (`R5-01`) đo được:
        # bơm một byte không giải mã được vào một trong hai nguồn ⇒ ngoại lệ ném lúc IMPORT,
        # trước cả `main`, nên CLI chết với traceback và `rc=1`. Một cổng chết trước khi phân
        # ba trạng thái là cổng KHÔNG có trạng thái thứ ba.
        return {}, f"không đọc được nguồn từ vựng provider: {type(ex).__name__}: {ex}"
    try:
        cay = ast.parse(van_launcher)
    except SyntaxError as ex:                                    # noqa: BLE001
        return {}, f"`{nguon}` không phân tích được: {ex}"

    def _bang(ten):
        """Trả (hàng ĐÃ KIỂM lược đồ, lý do hỏng). Lỗi nêu bảng/hàng/cột — KHÔNG ném.

        `R7-01`: bản trước trả hàng bất kỳ số cột và để người gọi unpack ⇒ lỗi DỮ LIỆU
        NGUỒN thoát ra lúc import. Nay mọi ô được kiểm TRƯỚC khi ai unpack: arity theo
        `_LUOC_DO_BANG`, chuỗi không rỗng cho mọi cột trừ `lenh`. Chỉ nhận literal thuần
        (`ast.literal_eval`) ở MỨC MODULE và ĐÚNG MỘT lần — bảng được tính toán hay khai hai
        lần thì không biết bảng nào là nguồn."""
        cot = _LUOC_DO_BANG[ten]
        nuts = [n for n in cay.body if isinstance(n, ast.Assign) and len(n.targets) == 1
                and getattr(n.targets[0], "id", "") == ten]
        if not nuts or not isinstance(nuts[0].value, ast.Tuple):
            return None, (f"`{nguon}`: `{ten}` thiếu hoặc sai hình dạng (đòi một tuple literal "
                          f"ở mức module)")
        if len(nuts) > 1:
            return None, (f"`{nguon}`: `{ten}` khai {len(nuts)} lần ở mức module — không biết "
                          f"bảng nào là nguồn")
        try:
            gia_tri = ast.literal_eval(nuts[0].value)
        except (ValueError, TypeError, SyntaxError, MemoryError, RecursionError) as ex:
            return None, (f"`{nguon}`: `{ten}` không phải literal thuần ({type(ex).__name__}) — "
                          f"bảng nguồn không được tính toán hay tham chiếu tên")
        ra = []
        for i, hang in enumerate(gia_tri, 1):
            if not isinstance(hang, tuple):
                return None, f"`{nguon}`: `{ten}` hàng {i} không phải tuple"
            if len(hang) != len(cot):
                return None, (f"`{nguon}`: `{ten}` hàng {i} có {len(hang)} cột, lược đồ đòi "
                              f"{len(cot)} ({', '.join(cot)})")
            for c, x in zip(cot, hang):
                if c == "lenh":
                    ok = (isinstance(x, tuple) and bool(x)
                          and all(isinstance(y, str) and y and y.strip() == y for y in x))
                    mo_ta = "bộ tên lệnh (tuple chuỗi không rỗng)"
                else:
                    ok = isinstance(x, str) and bool(x) and x.strip() == x
                    mo_ta = "chuỗi không rỗng, không thừa khoảng trắng"
                if not ok:
                    return None, (f"`{nguon}`: `{ten}` hàng {i} cột `{c}` = {x!r} không phải "
                                  f"{mo_ta}")
            ra.append(hang)
        return ra, None

    # CHỈ NGUỒN CÓ CẤU TRÚC. Bản trước gom MỌI hằng chuỗi dưới `CONG_CU`/`KHA_NANG` rồi
    # dò regex — nên chính chuỗi `vi_sao` mô tả của một mục cũng cấp được quyền
    # (cross-review, P2 trên `5a78c15`: đổi một chuỗi lý do thành `provider ke_gian_5 qua
    # execution_surface forged` ⇒ `ke_gian_5` vào danh sách CHO PHÉP, không lỗi nguồn nào).
    # Đổi NGUỒN mà giữ HÌNH DẠNG (đọc prose) thì lỗ chỉ đổi chỗ — lần thứ hai liên tiếp.
    hd, loi_hd = _bang("_TRANSPORT_CONTRACTS")
    if loi_hd:
        return {}, loi_hd
    if not hd:
        return {}, f"`{nguon}`: `_TRANSPORT_CONTRACTS` RỖNG — có mặt mà không dùng được"
    ngoai, loi_ngoai = _bang("_PROVIDER_NGOAI_CLI")
    if loi_ngoai:
        return {}, loi_ngoai
    if not ngoai:
        return {}, f"`{nguon}`: `_PROVIDER_NGOAI_CLI` RỖNG"
    # BÍ DANH cũng đọc từ bảng, và được CHUẨN HOÁ trước mọi phép kiểm theo provider. Hai
    # bảng, hai chốt RIÊNG — gộp `bd is None or bd_bm is None` thành một `if` là để một
    # phép làm yếu bỏ riêng vế sau đi qua cả suite (`R7-03`, phép B).
    bd, loi_bd = _bang("_PROVIDER_BI_DANH")
    if loi_bd:
        return {}, loi_bd
    bd_bm, loi_bm = _bang("_BE_MAT_BI_DANH")
    if loi_bm:
        return {}, loi_bm

    # Từ đây MỌI hàng đã đúng lược đồ: unpack không còn là chỗ lỗi dữ liệu thoát ra.
    hop_dong = {}
    for prov, _lenh, be_mat, van_chuyen in hd:
        hop_dong.setdefault(prov, {"be_mat": set(), "van_chuyen": set()})
        hop_dong[prov]["be_mat"].add(be_mat)
        hop_dong[prov]["van_chuyen"].add(van_chuyen)
    for prov, be_mat, van_chuyen in ngoai:
        hop_dong.setdefault(prov, {"be_mat": set(), "van_chuyen": set()})
        hop_dong[prov]["be_mat"].add(be_mat)
        hop_dong[prov]["van_chuyen"].add(van_chuyen)

    for cu_, moi_ in bd:
        if moi_ not in hop_dong:
            return {}, f"`{nguon}`: bí danh `{cu_}` trỏ `{moi_}` không có hợp đồng"
    # ĐÚNG MIỀN: đích của bí danh bề mặt phải là một bề mặt CÓ trong hợp đồng. Bản trước
    # lặng lẽ bỏ qua đích không khớp — bí danh chết mà không ai biết (`R7-01`).
    moi_be_mat = set().union(*(v["be_mat"] for v in hop_dong.values()))
    for cu_, moi_ in bd_bm:
        if moi_ not in moi_be_mat:
            return {}, (f"`{nguon}`: bí danh bề mặt `{cu_}` trỏ `{moi_}` không phải bề mặt "
                        f"của provider nào — bí danh không có đích là bí danh chết")
        for v in hop_dong.values():
            if moi_ in v["be_mat"]:
                v["be_mat"].add(cu_)

    # NGUỒN CHÉO: khối mã rào của `AGENTS.md` phải KHỚP bảng, không được mâu thuẫn. Nó
    # không còn là nguồn cấp tên nữa — chỉ là phép ĐỐI CHIẾU, nên một dòng văn xuôi không
    # nới được gì, mà một khai báo mâu thuẫn thì vẫn bị bắt.
    for khoi in re.findall(r"(?ms)^```[a-z]*\n(.*?)^```", van_agents):
        pv = re.search(r"(?m)^provider:\s*([a-z0-9_]+)\s*$", khoi)
        if not pv:
            continue
        ten = pv.group(1)
        if ten not in hop_dong:
            return {}, (f"`{tv}` khai provider `{ten}` mà `{nguon}` không có hợp đồng — "
                        f"hai nguồn LỆCH nhau, không kết luận được")
        for khoa, mau in (("be_mat", r"(?m)^execution_surface:\s*([a-z0-9_]+)\s*$"),
                          ("van_chuyen", r"(?m)^transport:\s*([a-z0-9_]+)\s*$")):
            g = re.search(mau, khoi)
            if g and g.group(1) not in hop_dong[ten][khoa]:
                return {}, (f"`{tv}` khai `{ten}` với {khoa}=`{g.group(1)}` khác hợp đồng "
                            f"{sorted(hop_dong[ten][khoa])} — hai nguồn LỆCH nhau")

    for luat, tep, cau in _NEO_LUAT_CHEP_TAY:
        if cau not in van_luat[tep]:
            return {}, (f"`{goc / tep}` không còn câu biện minh cho `{luat}` ({cau!r}) — "
                        f"luật chép tay mất neo")
    return ({"hop_dong": {k: {"be_mat": frozenset(v["be_mat"]),
                              "van_chuyen": frozenset(v["van_chuyen"])}
                          for k, v in hop_dong.items()},
             "bi_danh": {c: m for c, m in bd}}, None)


# `anthropic` (không hậu tố) là DẠNG LỊCH SỬ: bốn biên nhận v2 chuẩn của kho và hai biên
# nhận lượt 1-2 dùng nó. Giữ làm BÍ DANH có khai, không âm thầm — đổi cách đọc một tên đã
# nằm trong hiện vật là viết lại lịch sử.
#
# `human` KHÔNG còn là tên chép tay ở đây. Bản trước giữ `PROVIDER_KHONG_HOP_DONG = {"human"}`
# với lý lẽ *"provider KHÔNG có hợp đồng nào trong kho"* — SAI với bảng provider chuyển tiếp
# (`ops/KE_HOACH_THI_CONG_DA_PROVIDER.md` §2 đã khai `human / manual_audit / human`), và
# hệ quả đo được (`R7-02`): `_thieu` cấm provider-không-hợp-đồng MỌI mức của
# `ASSURANCE_CAN_DOC_LAP`, kể cả `human_audited` — mức mà `PROTOCOL §8` dành ĐÚNG cho người
# audit — nên một biên nhận v2 human-audit hợp lệ bị loại vô điều kiện theo TÊN. Nay `human`
# có hợp đồng trong `_PROVIDER_NGOAI_CLI` của `launcher.py` như mọi provider khác; danh
# sách CHO PHÉP = tên có hợp đồng ∪ bí danh, không còn ngăn "có tên mà không hợp đồng".
_HD, PROVIDER_NGUON_HONG = _provider_chinh_tac()
PROVIDER_HOP_DONG = _HD.get("hop_dong", {})
PROVIDER_BI_DANH = _HD.get("bi_danh", {})
PROVIDER_CHO_PHEP = frozenset(PROVIDER_HOP_DONG) | frozenset(PROVIDER_BI_DANH)


def _chuan_hoa_provider(prov):
    """Bí danh → tên CHÍNH TẮC, và làm việc này TRƯỚC mọi phép kiểm theo provider.

    Cross-review (P1 trên `5a78c15`): bản trước miễn bí danh khỏi chốt bộ ba rồi lại khoá
    assurance THEO TÊN, nên `{provider: anthropic, surface: chatgpt_web}` +
    `cross_approved` đi qua **cả hai** nửa của hợp đồng. Một bí danh không được chuẩn hoá
    là một đường vòng quanh chính ràng buộc của tên nó trỏ tới."""
    return PROVIDER_BI_DANH.get(prov, prov)


def _mri(d):
    """`model_reviewer_identity` phải mang HÌNH DẠNG attestation, không chỉ một khoá.

    Ba lần liên tiếp sai ở đúng chỗ này, mỗi lần chật hơn một nấc mà vẫn cùng một bệnh —
    đọc sự CÓ MẶT thành KHẢ NĂNG:
      (1) nhận mọi ánh xạ không rỗng      ⇒ `{x: 1}` qua;
      (2) đòi có khoá `provider`          ⇒ `{provider: "bat-ky-chuoi-nao"}` qua;
      (3) nay đòi: `provider` thuộc danh sách CHO PHÉP · `surface` không rỗng · và HOẶC
          `session_run_id` HOẶC một lời khai `KHONG_do_duoc` nói RÕ vì sao thiếu.
    Bậc (3) vẫn KHÔNG chứng minh identity là thật — nó chỉ đòi biên nhận khai đủ hình dạng
    để người đọc biết mình đang cầm gì. Đo trên kho: 10/10 biên nhận ĐẠT hiện có đều qua."""
    v = d.get("model_reviewer_identity")
    if not isinstance(v, dict) or not v:
        return "thiếu/rỗng ánh xạ `model_reviewer_identity`"
    prov = _chuoi(v.get("provider"))
    if not prov:
        return "`model_reviewer_identity` không có `provider` (chuỗi không rỗng)"
    prov = _chuan_hoa_provider(prov)        # BÍ DANH → CHÍNH TẮC, trước mọi phép kiểm
    if PROVIDER_NGUON_HONG is None and prov not in PROVIDER_CHO_PHEP:
        return (f"`model_reviewer_identity.provider`={prov!r} ngoài danh sách CHO PHÉP "
                f"{sorted(PROVIDER_CHO_PHEP)} — chuỗi tự do không phải attestation")
    be_mat = _chuoi(v.get("surface"))
    if not be_mat:
        return "`model_reviewer_identity` không có `surface` (bề mặt thực thi, chuỗi không rỗng)"
    # BỘ BA, không chỉ TÊN — và nay bí danh đi qua ĐÚNG hợp đồng của tên chính tắc, không
    # còn mượn được bề mặt của provider khác (`P1` trên `5a78c15`).
    hd = PROVIDER_HOP_DONG.get(prov)
    if PROVIDER_NGUON_HONG is None and hd:
        if be_mat not in hd["be_mat"]:
            return (f"`model_reviewer_identity.surface`={be_mat!r} không phải bề mặt của "
                    f"provider `{prov}` — hợp đồng của kho cho {sorted(hd['be_mat'])}")
        # `transport` KHÔNG bắt buộc (0/14 hiện vật khai nó lúc vá, `b7a53ba`; đo lại
        # 06-09-2026 trên `4488ff1`: 1/15 — đòi ngay vẫn là bắt oan cả kho), nhưng KHAI SAI
        # thì chặn: một bộ ba SAI SỰ THẬT tệ hơn một bộ ba khuyết.
        # Nợ đã khai: chưa đòi khai `transport`, xem caveat trong biên nhận lượt 6.
        # `R8-04`: VẮNG khác CÓ-MÀ-HỎNG, và `_chuoi` trả `None` cho CẢ HAI. Bản trước gộp hai
        # trạng thái ấy vào một nhánh `if vc and …`, nên CHỈ một chuỗi SAI bị bắt còn MỌI kiểu
        # khác lọt LẶNG. Đo được trên một biên nhận hợp lệ, chỉ đổi mỗi trường này:
        # `{'fake': 1}` · `''` · `7` · `['machine']` · `True` · `None` ⇒ **0 lỗi**, y hệt "vắng hẳn";
        # chỉ `'human'` (chuỗi sai hợp đồng) mới ra 1 lỗi. Đúng doctrine `None ≠ False` của kho —
        # cùng LỚP với `_chuoi` đã vá cho `surface`/`session_run_id`, chỉ khác ở chỗ trường này
        # TUỲ CHỌN nên nhánh "vắng" hợp lệ đã che mất nhánh "có mà hỏng".
        if "transport" in v:
            vc = _chuoi(v.get("transport"))
            if vc is None:
                return (f"`model_reviewer_identity.transport`={v.get('transport')!r} CÓ MẶT nhưng "
                        f"không phải chuỗi không rỗng — VẮNG khác CÓ-MÀ-HỎNG, im lặng không phải "
                        f"lời khai")
            if vc not in hd["van_chuyen"]:
                return (f"`model_reviewer_identity.transport`={vc!r} không phải vận chuyển của "
                        f"provider `{prov}` — hợp đồng của kho cho {sorted(hd['van_chuyen'])}")
    rid = _chuoi(v.get("session_run_id"))
    if not rid and not _chuoi(v.get("KHONG_do_duoc")):
        return ("`model_reviewer_identity` không có `session_run_id` và cũng KHÔNG khai "
                "`KHONG_do_duoc` giải thích vì sao thiếu — im lặng không phải lời khai")
    return None


def _gsi(d):
    """`null` HỢP LỆ (dòng 430: "<github actor or null when not published>"), VẮNG KHOÁ thì không.

    Nhưng `false` / `[]` / `"banana"` cũng KHÔNG hợp lệ — bản đầu nhận cả ba (F2/P1-B)."""
    if "github_submitter_identity" not in d:
        return "thiếu khoá `github_submitter_identity` (null hợp lệ, VẮNG thì không)"
    v = d["github_submitter_identity"]
    if v is None:
        return None
    if not isinstance(v, dict):
        return f"`github_submitter_identity` là {type(v).__name__}, đòi ánh xạ hoặc null"
    if not _chuoi(v.get("actor")):
        return "`github_submitter_identity` không null mà không có `actor`"
    return None


def _doc_loai(a):
    """Đọc `anchor.loai` CHUẨN HOÁ — nguồn DUY NHẤT cho cả schema lẫn dispatch."""
    return (_chuoi(a.get("loai")) or "") if isinstance(a, dict) else ""


def _anchor_khoa(d, k):
    a = d.get("anchor")
    if not isinstance(a, dict) or not a:
        return None                      # đã có mục `anchor` riêng lo việc này
    return None if _chuoi(a.get(k)) else f"`anchor.{k}` thiếu/rỗng (đòi chuỗi không rỗng)"


def _anchor_loai(d):
    a = d.get("anchor")
    if not isinstance(a, dict) or not a:
        return None
    loai = _doc_loai(a)
    if not loai:
        return "`anchor.loai` thiếu/rỗng"
    if loai not in ANCHOR_LOAI_CHO_PHEP:
        return f"`anchor.loai`={loai!r} ngoài danh sách CHO PHÉP {sorted(ANCHOR_LOAI_CHO_PHEP)}"
    return None


# BẢNG YÊU CẦU — chép từ `PROTOCOL §8` dòng 453-454, MỘT MỤC MỘT PHÉP KIỂM.
#
# Vì sao là bảng chứ không phải mấy vòng `for` như bản đầu: cross-review đo được BA đột biến
# sản phẩm mà bộ test cũ KHÔNG bắt (gỡ `TRUONG_CO_MAT` · gỡ `cuong_do` khỏi `ANCHOR_KHOA` ·
# gỡ `reviewed_sha` khỏi `TRUONG_VO_HUONG`) — cả ba vẫn `15/15, 5/5`. Nguyên nhân: bộ test có
# ca âm cho VÀI trường, không có cho TỪNG trường. Nay mỗi mục ở đây có đúng một ca âm trong
# `ops/bien_nhan_v2_test.py`, và bảng kỳ vọng bên ấy được CHÉP RIÊNG chứ không import từ đây —
# một oracle sinh từ chính thứ nó kiểm thì co theo mỗi lần cổng bị nới.
YEU_CAU = (
    ("schema_version", lambda d: None if d.get("schema_version") == 2
     else f"schema_version={d.get('schema_version')!r}, đòi 2"),
    ("receipt_id", lambda d: _co_chuoi(d, "receipt_id")),
    ("reviewed_sha", lambda d: _khop(d, "reviewed_sha", _HEX40, "Git OID đầy đủ 40 hex thường")),
    ("verdict_path", lambda d: _co_chuoi(d, "verdict_path")),
    ("verdict_sha256", lambda d: _khop(d, "verdict_sha256", _HEX64, "sha256 64 hex thường")),
    ("evidence_url", lambda d: _co_chuoi(d, "evidence_url")
     or (None if str(d.get("evidence_url", "")).strip().startswith("https://")
         else "`evidence_url` không bắt đầu bằng `https://`")),
    # Gọi QUA TÊN TOÀN CỤC, không giữ tham chiếu hàm lúc dựng bảng. Bản trước nhúng thẳng
    # `_mri`/`_gsi` nên hai đột biến nhắm vào chúng KHÔNG với tới được predicate — bảng vẫn
    # gọi bản cũ. Một bộ chấm đột biến không chạm được thứ nó định đo thì con số "có răng"
    # của nó nói về cái khác.
    ("model_reviewer_identity", lambda d: _mri(d)),
    ("github_submitter_identity", lambda d: _gsi(d)),
    # BA mục, không phải một. Cross-review vòng 2 (P2) đo được: gộp `anchor.loai` và
    # `anchor.cuong_do` vào MỘT hàng ma trận thì gỡ `loai` khỏi `ANCHOR_KHOA` vẫn xanh —
    # `c16` thấy cùng một tên yêu cầu, `c17` chỉ phá `cuong_do`. Một hàng ma trận che được
    # nhiều chốt thì nó không còn là ma trận.
    ("anchor", lambda d: None if isinstance(d.get("anchor"), dict) and d.get("anchor")
     else "thiếu/rỗng ánh xạ `anchor`"),
    ("anchor.loai", lambda d: _anchor_loai(d)),
    ("anchor.cuong_do", lambda d: _anchor_khoa(d, "cuong_do")),
)

# Mức assurance HÀM Ý một lượt review có thẩm quyền. Biên nhận nào TỰ KHAI là chạy bằng
# subagent trong cùng phiên điều phối (không phiên riêng, không neo launcher) thì KHÔNG được
# khai mức ấy — F3 của cross-review PR #455: chính khối identity mới thêm nói tính độc lập là
# KHÔNG ĐO ĐƯỢC rồi lấy đó biện minh cho `same_provider_approved`.
ASSURANCE_CAN_DOC_LAP = frozenset({"cross_approved", "same_provider_approved", "human_audited"})
# PHÂN VÙNG MỨC ASSURANCE THEO LOẠI REVIEWER — suy từ cột `transport` của HỢP ĐỒNG, không từ
# tên; neo ở `PROTOCOL §8` mục 1-3 qua `_NEO_LUAT_CHEP_TAY`. `R7-02`: bản trước cấm `human` mọi
# mức của `ASSURANCE_CAN_DOC_LAP` (xem chú thích trên `_HD`); và cùng LỚP ấy còn một mặt chưa ai
# chỉ: một mô hình khai `human_audited` đi qua `_thieu` không vướng gì (chỉ `openai_chatgpt` bị
# `AGENTS.md` §4 cấm đích danh). Hai mặt của một luật: vận chuyển `human` ⇒ NGƯỜI ⇒ chỉ được
# `human_audited`; mọi vận chuyển khác (`machine`, `machine/local`, `human_mediated` — người
# CHUYỂN TIẾP đầu ra của một mô hình, danh tính reviewer vẫn là mô hình) ⇒ MÔ HÌNH ⇒ không
# được `human_audited`. Hợp đồng vận chuyển HỖN HỢP (`human` + khác) chưa có trong kho; nếu
# xuất hiện thì coi là mô hình — siết `human_audited`, không siết mức mô hình. Ghi ra để không
# ai đọc thành đã đo.
VAN_CHUYEN_NGUOI = "human"
ASSURANCE_CUA_NGUOI = frozenset({"human_audited"})
ASSURANCE_CUA_MO_HINH = frozenset({"cross_approved", "same_provider_approved"})
# Ba loại mỏ neo protocol liệt kê (dòng 455): "canonical ancestry, protected evidence ref hoặc
# check object". DANH SÁCH CHO PHÉP, không phải danh sách cấm — bài học `v1.36.68`: danh sách
# cấm phân biệt CÁCH VIẾT, không phân biệt THẨM QUYỀN.
ANCHOR_LOAI_CHO_PHEP = frozenset({"canonical_ancestry", "protected_evidence_ref", "check_object"})

# --- Danh sách 1: miễn trừ legacy, ĐÓNG BĂNG tại cutover `2f84531` (11 tệp) -------------
ALLOWLIST_CUTOVER = {
    "doctor-github-mcp-review-6-codex-verdict.receipt.yaml":
        "deeef9dc0054db2516ed88b32c8c4db47f7a72c75d15bac4a9cdb4803f40cabf",
    "doctor-github-mcp-review-9-codex-verdict.receipt.yaml":
        "039a2972c81bd9210f56ffd721b8694e5dfa8885b9841eebef94b41ab34377d8",
    "pr134-ci-lease-gate-codex-verdict.receipt.yaml":
        "c69347569b7dae133b997cb15b12f28ee962e97934ed2c15873805eec9373885",
    "tao-tag-luu-tru-review-1-codex-verdict.receipt.yaml":
        "39829e6b0489acc73c2a01bbb5c1997a20f9b9be6a2caea182048a767bfc707d",
    "wp55-r2-review-4-codex-verdict.receipt.yaml":
        "4081ec009292faa12563eb6b9df40b071e0c9345cae865fe6b766bef1a4ac0eb",
    "wp55-r2-review-5-codex-verdict.receipt.yaml":
        "ece195f31d3f9abdda57495cd32070d880b54583217f1c62ecaaa3c1b03c2537",
    "wp55-r4-review-1-codex-verdict.receipt.yaml":
        "b9f0f1d94d777ddda973b642815f5d9a457d9cb13f702009d4b12889649d70a5",
    "wp55-r4-review-2-codex-verdict.receipt.yaml":
        "dd4da1a3d85f17f5cdc5bf76951f30c657af182966ec8ea186f91c9a090732a4",
    "wp55-r4-review-di-tru-codex-verdict.receipt.yaml":
        "2758567db8e5f78bedcf27728859e092b6d76d242d550e0716d0ed8578c9f23b",
    "wp55-r4-review-rebase-codex-verdict.receipt.yaml":
        "9f80a5f69266e7509fe9a8c89bb5116f2848af12eaf1a5bf54dc7235d5e4da42",
    "wp55-r4-review-viet-lai-codex-verdict.receipt.yaml":
        "de439162c422439523a1b0acc08d9549d3e72be42cfe3f09e7bbec9dadde04ab",
}

# --- Danh sách 2: NỢ ĐÃ ĐO, chỉ được CO LẠI (sinh bằng `--sinh-no`) --------------------
NO_DA_DO: dict[str, str] = {
    "bien-nhan-review-s2-review-4-codex-verdict.receipt.yaml":
        "1d1382fb95c209135b8afdbd21a1f602b25328125c2bde8d7c44d129d0ce310f",
    "don-nhanh-base-review-1-codex-verdict.receipt.yaml":
        "bff5e1157fff1a5eda7e425447316976797bcf3703f4f332d0d983f1ec2e53e7",
    "don-nhanh-base-review-2-codex-verdict.receipt.yaml":
        "6295f6057994c606342501ff15cfc6c597f0d403dd966caa3f68c938c918f48a",
    "don-nhanh-base-review-3-claude-verdict.receipt.yaml":
        "602bfc18184d747fd7047fc2efe7d7666d7e02d76fa061ba8b87b8999db2f8f3",
    "don-nhanh-base-review-4-claude-verdict.receipt.yaml":
        "8772712513fa1e491c51526d6a5f0f17d4fc04b0234abb397ae1cd39d132b4e8",
    "don-nhanh-base-review-5-claude-verdict.receipt.yaml":
        "3acb2723a9228666828cc4b321a5fdb2ae192001b66db7c2527a7cdabacec169",
    "don-nhanh-base-review-6-claude-verdict.receipt.yaml":
        "b2e53792c3f945d2e00b5bfc64ed4d6b944762b54ac54353021f67f4f192b587",
    "don-nhanh-base-review-7-claude-verdict.receipt.yaml":
        "7309ab38967838c357100d58ec7a4c86e293fbdd75e81d3e0d4600d22eeb62e5",
    "don-nhanh-kien-truc-gh-1-claude-verdict.receipt.yaml":
        "1f40ee7f6f9b8b17645fef417eccb5777d4f56b49bc3994f065874f2401c9929",
    "donref-xoa-an-toan-review-1-claude-verdict.receipt.yaml":
        "183ec46e1a4cae22a822eefffb95b547f89b7b42c50ec49645d4b5817e3cb744",
    "donref-xoa-an-toan-review-2-claude-verdict.receipt.yaml":
        "28d45ad88e7c3fdc53cab7777f08ace054574c1c6963ec9fcbee8f79b28f34b9",
    "lease-dang-review-1-claude-verdict.receipt.yaml":
        "336755b5fc58c659c535db2e80e724d535f0ceddeb7bac9af4b02102aabfc9f2",
    "lease-dang-review-2-claude-verdict.receipt.yaml":
        "1ea14266d6771759d4721ec0df42bfc6bdd5086e0c4b12693b08c5f853a9c492",
    "lease-dang-review-3-claude-verdict.receipt.yaml":
        "c5775d68f5adf782e1fd792e27b31310856fa67b44926a17f96b9ab9793de73b",
    "lease-dang-review-4-claude-verdict.receipt.yaml":
        "1fa4c33c1744398857658efb0c75f62256f20a64914063f2fb896594df03a078",
    "lease-dang-review-5-claude-verdict.receipt.yaml":
        "dc53836df18f1adf21c59eca73f5aaba692b7ccdc2bc311d74c7ab690da9a028",
    "lease-dang-windows-review-1-claude-verdict.receipt.yaml":
        "9bdd49f4786a23abe67c63ec76c1c8ada9ab18418f03e6fe9513bc16c62d3c7a",
    "lease-dang-windows-review-2-claude-verdict.receipt.yaml":
        "29d3a1a6cb2c46c579f8c224f0874d5f55982afd5a13eba5e50cc871f6fda1d2",
    "lease-dang-windows-review-3-claude-verdict.receipt.yaml":
        "9959343169eb84d4d5b56a3e4ad7611f11db771833d7476284532eb27e862fbd",
    "lease-hoi-toan-kho-review-1-claude-verdict.receipt.yaml":
        "806dbee61c92f89c1a13827d478d5fc4f15ae1e54cd1b2e149ca970b61f7ffe3",
    "lease-hoi-toan-kho-review-2-claude-verdict.receipt.yaml":
        "190a45befd1bd97635c833300ce921d0f4aa06973451f5ac35fceb7f93eda96a",
    "lease-hoi-toan-kho-review-3-claude-verdict.receipt.yaml":
        "a277fb86fc07574593a504f72cb480d9a3d70e2dd0af9511858de64e92151a22",
    "n5-lenh-hook-windows-review-1-codex-verdict.receipt.yaml":
        "82a8664137c0a7b21657479f3db83d6ec147bb37900028b7483c0dc152fdbf31",
    "n5-lenh-hook-windows-review-2-codex-verdict.receipt.yaml":
        "34ca3e907f1fc61a5b8091eded528b3b2fdecf5f85670af9716e1e0fc61166d4",
    "plat-m4-human-audit-ducthangho-verdict.receipt.yaml":
        "b2b147d63f789d91cbfa0a37b5b431b0d4bdec9672ef74e651185b190f383b94",
    "plat-m4-review-1-codex-verdict.receipt.yaml":
        "d0961cb5584914143fa7657f12f348410df9310f3db3d5cba8ae80e50dcf8ecf",
    "plat-m4-review-2-codex-verdict.receipt.yaml":
        "0ac82afcac4dcb92a8a8d7449b6db05c2d9fe033af44d846561043a0582a6b0c",
    "plat-m4-review-3-claude-verdict.receipt.yaml":
        "c5d34d6e432565d8728e753cf9160a4292a118c8dbfc8d0fd24767d33c14a111",
    "plat-x5-review-1-claude-verdict.receipt.yaml":
        "6c19926d05151ba93a71d00dc804642110de8d95f5f8430c590c5037af03269e",
    "plat-x5-review-2-claude-verdict.receipt.yaml":
        "76244daf71981e3c96f3ee842c87d01995883a0747104cfa23163714fe82f818",
    "plat-x5-review-3-claude-verdict.receipt.yaml":
        "2221a079fd4887a0b4717bc1f90d868eddf35aba16488765126dfc27fa3e1408",
    "plat-x8-review-1-claude-verdict.receipt.yaml":
        "8bc0d299881a3ef99ab6c0d96264834c0e1f25af0a9854eb23e60b5382898ef4",
    "plat-x8-review-2-claude-verdict.receipt.yaml":
        "bfa4d9cad30d8e7f36cbb7064489506f4563e50452cc1952409415f856e11207",
    "plat-x8-review-3-claude-verdict.receipt.yaml":
        "c2db6b7600192431cfe74bb3f817b356495bc56247da82442a5dcf820f2641cd",
    "slice-b-c-human-audit-ducthangho-verdict.receipt.yaml":
        "9e76b60472adc90910fbcaff79cb34af73b5c03ee64c552ec71be5364a40d2a7",
    "slice-b-c-review-1-codex-verdict.receipt.yaml":
        "d80cfec7ff64edbe927b07c5105418c4f0382a3eb60e53f22d7effa7570c7192",
    "slice-b-c-review-2-codex-verdict.receipt.yaml":
        "662e6d798278ca40309eb0231fb02b540f63ea5d1f24ddb1b4cb6b3e554290fd",
    "t33-doi-shellcheck-review-1-codex-verdict.receipt.yaml":
        "71eefab1e94a1c0dd071d7418723fcd590cf86feb003a945ca7ef95830e11f23",
    "t33-doi-shellcheck-review-2-codex-verdict.receipt.yaml":
        "6152d0ff2a3b95c98b27dd2dba7e3ffaddb3b3ae27328d29ced3249fec4e088d",
    "t33-doi-shellcheck-review-3-codex-verdict.receipt.yaml":
        "8dcae1dd59624a96502cb92d4b5f6a83b8db789d56d2c935af6d94c2adaa675c",
    "t33-doi-shellcheck-review-4-codex-verdict.receipt.yaml":
        "a829125a652be52e0a93a6f0874cb64a9327d09c1505557693874f7636485513",
    "tri-thuc-review-1-codex-verdict.receipt.yaml":
        "49acb2c1a52c00d25751fdff4a6b77aa453232222bda9d90f5a488c8980b1f8f",
}


def _bam(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def _ho_model_cua_ten(ten: str) -> str:
    """Chuẩn hoá tên/chuỗi thành họ model chính tắc trong HO_MODEL_CHO_PHEP (P2-1, P3-1, P2-MOI)."""
    t = (ten or "").lower().strip()
    if not t:
        return ""
    if "claude" in t and "claude" in HO_MODEL_CHO_PHEP:
        return "claude"
    if ("gpt" in t or "codex" in t or t in ("o1", "o3") or t.startswith(("o1-", "o3-"))
            or "/o1" in t or "/o3" in t) and "gpt" in HO_MODEL_CHO_PHEP:
        return "gpt"
    if "gemini" in t and "gemini" in HO_MODEL_CHO_PHEP:
        return "gemini"
    return ""


def _nguon_tra_model(d: dict, vai: str):
    """(`sub`, bảng (nguồn, tiền tố)) theo thứ tự tra — `M17`, đóng `P2` của verdict lượt 3.

    Bên trong khối `model_<vai>_identity`, khoá tra KHÔNG mang tiền tố, cho CẢ HAI vai. Bản trước
    áp `pre` cho cả `sub` lẫn `d`, nên `model_reviewer_identity: {model: …}` CHẠY (vai reviewer có
    `pre` rỗng) còn `model_executor_identity: {model: …}` thì KHÔNG — đòi `executor_model`. Đòi một
    khoá mang lại tên vai bên trong khối đã tên là vai ấy vừa dư thừa vừa BẤT ĐỐI XỨNG, và thông
    điệp lỗi *"không xác định được họ model của executor"* đọc như "bạn chưa khai" trong khi người
    ta ĐÃ khai — dẫn người đọc đi sai hướng ở đúng trường mà `cross_approved` treo lên.

    Tiền tố chỉ còn nghĩa ở mức top-level `d`, nơi hai vai dùng CHUNG một không gian tên nên phải
    có gì đó phân biệt. Trả về MỘT bảng để hai phép tra bên dưới không thể trôi lệch nhau."""
    sub = d.get(f"model_{vai}_identity") if isinstance(d.get(f"model_{vai}_identity"), dict) else {}
    return sub, ((sub, ""), (d, f"{vai}_" if vai == "executor" else ""))


def _giai_ho_va_bc(d: dict, vai: str) -> tuple[str, str, bool]:
    """Trả về (họ model, mức bằng chứng, có_khai_đè) cho 'reviewer' hoặc 'executor' (P1-MOI)."""
    sub, nguon = _nguon_tra_model(d, vai)
    pre = f"{vai}_" if vai == "executor" else ""
    khai = next((_chuoi(s.get(p + k)) for s, p in nguon for k in ("model_family", "ho_model", "canonical_model", "model") if _chuoi(s.get(p + k))), "")
    bc = next((_chuoi(s.get(p + k)) for s, p in nguon for k in ("model_evidence", "bang_chung_model") if _chuoi(s.get(p + k))), "")
    if khai:
        return _ho_model_cua_ten(khai), bc, True
    return HO_MODEL_MAC_DINH.get(_chuan_hoa_provider(_chuoi(sub.get("provider")) or _chuoi(d.get(f"{pre}provider")) or ""), ""), bc, False


def _giai_ho_model_reviewer(d: dict) -> tuple[str, str]:
    return _giai_ho_va_bc(d, "reviewer")[:2]


def _giai_ho_model_executor(d: dict) -> str:
    return _giai_ho_va_bc(d, "executor")[0]


def _thieu(d: dict) -> list[str]:
    """Trả danh sách lý do tệp KHÔNG đạt v2. Rỗng = đạt (theo CẤU TRÚC)."""
    loi = [msg for _, kt in YEU_CAU for msg in [kt(d)] if msg]
    # Chốt CHÉO: assurance vs. bằng chứng độc lập mà chính biên nhận tự khai.
    #
    # Bản trước lấy `neo_boi_launcher` falsy làm PROXY cho "không độc lập", và cross-review
    # vòng 2 (P2) bác đúng chỗ đó: một lượt same-provider chạy trong phiên THỦ CÔNG mới, với
    # context/worktree riêng, hoàn toàn có thể khai `neo_boi_launcher: false` một cách trung
    # thực — bất biến của kho là phiên/context/worktree ĐỘC LẬP, không phải "đã dùng launcher".
    # Nay chốt đòi BẰNG CHỨNG ĐỘC LẬP TƯỜNG MINH: một `session_run_id`, hoặc một lời khai
    # `phien_doc_lap` dương. Thiếu cả hai thì không được khai mức hàm ý review có thẩm quyền.
    mri = d.get("model_reviewer_identity")
    if isinstance(mri, dict):
        tu_khai_trong_phien = "subagent" in (_chuoi(mri.get("che_do")) or "").lower()
        # KIỂU, không chỉ TRUTHINESS. Cross-review vòng 3 (P1) đo được: `phien_doc_lap:
        # "false"` là CHUỖI KHÔNG RỖNG nên truthy ⇒ qua; và `session_run_id` là một ÁNH XẠ
        # cũng sống sót phép ép `str(...)`. Một biên nhận tự khai KHÔNG có phiên đo được vẫn
        # lĩnh mức assurance độc lập. Cùng lớp "CÓ MẶT khác KHẢ NĂNG", lần này ở tầng KIỂU
        # DỮ LIỆU: một giá trị có mặt không có nghĩa nó khẳng định điều ta tưởng.
        co_bang_chung = (_chuoi(mri.get("session_run_id")) is not None
                         or mri.get("phien_doc_lap") is True)
        khai = _chuoi(d.get("assurance")) or _chuoi(d.get("assurance_dat")) or ""
        prov = _chuan_hoa_provider(_chuoi(mri.get("provider")) or "")
        cam = _muc_cam_theo_provider(prov)
        if khai in cam:
            # LÝ DO ĐÚNG CÁI ĐANG ÁP — một thông báo sai lý do đẩy người đọc đi sửa nhầm
            # chỗ, đúng bệnh `R4-02` ở tầng văn bản.
            loi.append(
                f"provider `{prov}` KHÔNG được tự tạo `{khai}` — {cam[khai]}; nhận một tên vào "
                f"danh sách CHO PHÉP không mang theo quyền của tên khác")
        if khai in ASSURANCE_CAN_DOC_LAP and (tu_khai_trong_phien or not co_bang_chung):
            ly_do = ("tự khai chạy trong phiên điều phối" if tu_khai_trong_phien
                     else "không có `session_run_id` lẫn `phien_doc_lap`")
            loi.append(
                f"khai `{khai}` mà KHÔNG có bằng chứng phiên độc lập ({ly_do}) — mức ấy hàm ý "
                f"một lượt review có thẩm quyền; dùng `review_deferred`, hoặc khai "
                f"`phien_doc_lap` kèm căn cứ")
        if khai == "cross_approved":
            ho_rev, bc_rev, ov_rev = _giai_ho_va_bc(d, "reviewer")
            ho_exec, bc_exec, ov_exec = _giai_ho_va_bc(d, "executor")
            if not ho_rev:
                loi.append("khai `cross_approved` mà không xác định được họ model của reviewer")
            if not ho_exec:
                loi.append("khai `cross_approved` mà không xác định được họ model của executor")
            if ho_rev and ho_exec and ho_rev == ho_exec:
                loi.append(
                    f"khai `cross_approved` mà hai bên cùng họ model `{ho_rev}` — `cross_approved` "
                    f"đòi hai họ model độc lập")
            for vai, ho, bc, ov in (("reviewer", ho_rev, bc_rev, ov_rev),
                                    ("executor", ho_exec, bc_exec, ov_exec)):
                sub = d.get(f"model_{vai}_identity") if isinstance(d.get(f"model_{vai}_identity"), dict) else {}
                pre = f"{vai}_" if vai == "executor" else ""
                if ov and not bc:
                    loi.append(f"khai đè model {vai} cho `cross_approved` mà thiếu mức bằng chứng model (`model_evidence`)")
                elif bc and bc not in MUC_BANG_CHUNG_MODEL:
                    loi.append(f"mức bằng chứng model {vai} `{bc}` ngoài danh sách CHO PHÉP")
                elif bc == "khong_do_duoc":
                    loi.append(f"khai `cross_approved` với mức bằng chứng {vai} `khong_do_duoc` — không đủ điều kiện cho cross_approved")
                elif bc == "khai_co_audit":
                    if not any(_chuoi(s.get(k)) for s in (sub, d) for k in (f"{pre}nguoi_audit", f"{pre}audit_actor", "nguoi_audit", "audit_actor")):
                        loi.append(f"khai `cross_approved` với mức bằng chứng {vai} `khai_co_audit` mà thiếu người audit xác nhận")
                elif bc == "do_may":
                    if not any(_chuoi(s.get(k)) for s in (sub, d) for k in (f"{pre}model_evidence_ref", f"{pre}telemetry_path", "model_evidence_ref", "telemetry_path")):
                        loi.append(f"khai `cross_approved` với mức bằng chứng {vai} `do_may` mà thiếu tham chiếu đo lường (`model_evidence_ref`)")
    return loi


def _muc_cam_theo_provider(prov):
    """Mức assurance mà provider `prov` KHÔNG được tự khai → lý do. RỖNG khi nguồn chưa đo được.

    `R7-01`, lần thứ TƯ cùng HÌNH DẠNG trong PR này — và hình dạng ấy có ĐỊNH NGHĨA, kẻo lần sau
    lại đếm bằng trí nhớ rồi ra hai số ngược nhau (`R8-03` đo được: docstring này ghi TƯ còn
    `ops/reviews/README.md` ghi NĂM): *một lỗi ĐO — nguồn/phụ thuộc hỏng, tức cổng KHÔNG BIẾT —
    bị báo thành VI PHẠM của receipt, tức cổng KẾT TỘI một hiện vật đúng.* Không tính crash, mất
    trạng thái, hay lỗi giàn đo không sinh cáo buộc. Bốn neo: `R4-02`@`4ef73e6` · `R5-01`@`670071b` ·
    finding connector@`670071b` (vá ở `b7a53ba`) · `R7-01`@`ca960160`. Không có đợt thứ năm.
    Khi nguồn provider hỏng, `PROVIDER_HOP_DONG`
    rỗng và bản trước suy *"không hợp đồng ⇒ không thẩm quyền"* cho MỌI provider ⇒ **11 biên
    nhận nguyên byte bị kết tội** `KHÔNG có hợp đồng` (rc=2 nhưng kèm 11 dòng ĐỎ), trong khi lỗi
    nằm ở NGUỒN. Mọi giới hạn suy từ provider chỉ được suy khi nguồn ĐÃ ĐO ĐƯỢC; nguồn hỏng thì
    `kiem` đã ghi trạng thái thứ ba cho cả lượt. Những chốt KHÔNG phụ thuộc nguồn (kiểu, SHA,
    bằng chứng phiên độc lập) vẫn chạy — "chưa đo được hợp đồng" không phải "miễn kiểm"."""
    cam = {}
    if PROVIDER_NGUON_HONG is not None or not prov:
        return cam
    for m in ASSURANCE_CAM_THEO_PROVIDER.get(prov, frozenset()):
        cam.setdefault(m, "`AGENTS.md` §4 giới hạn provider này ở `advisory_review`")
    hd = PROVIDER_HOP_DONG.get(prov)
    if hd is None:
        # KHÔNG HỢP ĐỒNG ⇒ KHÔNG THẨM QUYỀN. Nguyên tắc thay cho một danh sách: chưa khai
        # được bề mặt/vận chuyển thì chưa có gì để đối chiếu, nên không được khai một mức
        # hàm ý review có thẩm quyền. Chặn luôn cả tên được nhét TAY vào danh sách CHO PHÉP.
        for m in ASSURANCE_CAN_DOC_LAP:
            cam.setdefault(m, f"provider `{prov}` KHÔNG có hợp đồng bề mặt/vận chuyển nào "
                              f"trong kho — chưa khai thì chưa có thẩm quyền")
        return cam
    # PHÂN VÙNG NGƯỜI / MÔ HÌNH theo HỢP ĐỒNG vận chuyển (`R7-02`) — xem `ASSURANCE_CUA_NGUOI`.
    la_nguoi = hd["van_chuyen"] == {VAN_CHUYEN_NGUOI}
    if la_nguoi:
        for m in ASSURANCE_CUA_MO_HINH:
            cam.setdefault(m, f"`{m}` là mức review giữa các MÔ HÌNH (`PROTOCOL §8`); `{prov}` "
                              f"là NGƯỜI theo hợp đồng vận chuyển `{VAN_CHUYEN_NGUOI}` — mức của "
                              f"người audit là `human_audited`")
    else:
        for m in ASSURANCE_CUA_NGUOI:
            cam.setdefault(m, f"`{m}` là mức của NGƯỜI audit (`PROTOCOL §8`); `{prov}` là MÔ "
                              f"HÌNH theo hợp đồng vận chuyển {sorted(hd['van_chuyen'])}")
    return cam


def _git(root: Path, *args, timeout=20):
    """Chạy git trong `root`. Trả (rc, stdout) — KHÔNG ném, để người gọi phân ba trạng thái."""
    try:
        p = subprocess.run(["git", "-C", str(root), *args], capture_output=True,
                           text=True, timeout=timeout)
        return p.returncode, p.stdout.strip()
    except (OSError, subprocess.SubprocessError) as ex:      # noqa: BLE001
        return 127, f"{type(ex).__name__}: {ex}"


def _blob_khop(that: str, khai: str) -> bool:
    """Phép so băm blob, TÁCH RIÊNG để đột biến nhắm được đúng nó.

    Bản trước để phép so nội tuyến, nên đột biến duy nhất giết được ca `c20` là phá
    `_BLOB_URL` — mà cái ấy giết cả cụm, tức không PHÂN BIỆT được "cổng còn so băm" với
    "cổng còn nhận ra URL". Một đột biến giết cả cụm không chứng minh từng chốt còn răng."""
    return that == khai


def _neo_git(root: Path, ten: str, d: dict):
    """Xác minh mỏ neo bằng GIT. Trả (loi, chua_do_duoc) — hai danh sách RIÊNG.

    BA TRẠNG THÁI, và trạng thái thứ ba KHÔNG được đọc thành trạng thái thứ hai: object
    không tra được nghĩa là KHÔNG ĐO ĐƯỢC (clone nông, lịch sử chưa fetch), **không** phải
    "SHA bịa". Reviewer nói thẳng chỗ này: *"Thiếu lịch sử không phải bằng chứng giả mạo."*

    VÌ SAO CÓ, và đây là phần đắt: bản đầu KHÔNG kiểm gì và khai thành nợ với lý do
    *"`actions/checkout` mặc định `depth: 1` nên `git cat-file -e` sẽ đỏ giả"*. Lý do ấy
    SAI trên chính kho này — `.github/workflows/ci.yml:86` đã đặt `fetch-depth: 0` từ `r226`,
    kèm chú thích giải thích đúng cái bẫy được viện dẫn. Tôi khai một ràng buộc mà KHÔNG ĐO
    nó, rồi viết tiền đề sai ấy vào docstring, commit, CHANGELOG và mô tả PR."""
    loi, chua = [], []
    sha = str(d.get("reviewed_sha") or "").strip()
    if _HEX40.match(sha):
        rc, _ = _git(root, "cat-file", "-e", f"{sha}^{{commit}}")
        if rc == 127:
            chua.append(f"{ten}: KHÔNG ĐO ĐƯỢC `reviewed_sha` — không gọi được git")
        elif rc != 0:
            chua.append(f"{ten}: KHÔNG ĐO ĐƯỢC `reviewed_sha` {sha[:12]}… — object không tra "
                        f"được ở cây này (clone nông / chưa fetch), KHÔNG kết luận là bịa")
    a = d.get("anchor") or {}
    url = str(d.get("evidence_url") or "").strip()
    # MỘT phép đọc `loai`, dùng chung cho schema LẪN dispatch. Bản trước `_anchor` chuẩn hoá
    # bằng `strip()` còn dispatch so giá trị THÔ, nên `" canonical_ancestry "` qua được chốt
    # hình dạng rồi TRỐN luôn khỏi `_neo_git` — chốt `c22` vừa thêm bị đi vòng bằng hai
    # khoảng trắng. Cross-review vòng 2 (R2-01) đo được. Hai cách đọc cùng một trường là
    # cùng lớp với "hai bản trôi lệch": lỗi không nằm ở phép so nào, nó nằm ở việc có HAI.
    loai = _doc_loai(a)
    if loai in ("protected_evidence_ref", "check_object"):
        # Cổng KHÔNG có đường đo cho hai loại này. Bản trước LẶNG LẼ bỏ qua ⇒ ghép loại ấy
        # với một URL bất kỳ là thành "v2 hợp lệ". Nay nó vào trạng thái THỨ BA — và trạng
        # thái thứ ba làm cổng ĐỎ (rc=2), không phải "sạch".
        chua.append(f"{ten}: `anchor.loai: {loai}` — cổng CHƯA có đường đo cho loại mỏ neo "
                    f"này, nên KHÔNG kết luận được nó hợp lệ")
        return loi, chua
    if loai != "canonical_ancestry":
        return loi, chua
    m = _BLOB_URL.search(url)
    if not m:
        # LỖ TỰ TÌM (không phải từ reviewer): khai `canonical_ancestry` rồi đặt `evidence_url`
        # là URL PR thì phép đo git IM LẶNG không chạy — mỏ neo TỰ KHAI mà không ai đo, và
        # cổng vẫn in "sạch". Đó là "một loại mỏ neo cổng không kiểm được thì trốn luôn khỏi
        # phép kiểm", cùng lớp với ba finding P1 của lượt này. Đo: cả 9 biên nhận ĐẠT hiện có
        # đều đã ghim blob URL, nên siết chỗ này không bắt oan ai.
        loi.append(f"{ten}: khai `anchor.loai: canonical_ancestry` nhưng `evidence_url` KHÔNG "
                   f"phải URL blob ghim commit (`/blob/<40 hex>/<đường dẫn>`) — mỏ neo kiểu ấy "
                   f"KHÔNG đo được, mà không đo được thì không được khai là canonical ancestry")
        return loi, chua
    commit, duong = m.group(1), m.group(2)
    # MỎ NEO PHẢI NEO ĐÚNG THỨ NÓ KHAI. Bản trước kiểm `verdict_path` chỉ ở chỗ "không
    # rỗng", còn `_neo_git` chỉ xác minh đường dẫn PHÂN TÍCH TỪ URL — nên một biên nhận khai
    # `verdict_path` không tồn tại/không liên quan mà `evidence_url` trỏ tệp BẤT KỲ có băm
    # trùng `verdict_sha256` thì vẫn qua (connector, P2 trên `670071b`). Hai trường cùng nói
    # về MỘT tệp mà không ai so chúng với nhau: cùng lớp "có HAI cách đọc một thứ".
    # `lstrip("./")` BÓC MỌI dấu chấm và gạch chéo, không phải "một `./` tuỳ chọn": cả
    # `../../ops/reviews/x.md` lẫn `/ops/reviews/x.md` đều chuẩn hoá về `ops/reviews/x.md`
    # rồi KHỚP URL, trong khi trường thô mà người đọc mở lại trỏ tệp khác (cross-review, P2
    # trên `5a78c15`). Đây là bản chuẩn hoá tự viết thứ hai trong tệp này bị bắt vì làm
    # nhiều hơn tên gọi của nó.
    khai_duong = str(d.get("verdict_path") or "").strip()
    if khai_duong.startswith("./"):
        khai_duong = khai_duong[2:]
    if khai_duong and (khai_duong.startswith("/") or ".." in Path(khai_duong).parts):
        loi.append(f"{ten}: `verdict_path: {khai_duong}` không phải đường dẫn tương đối gốc "
                   f"kho — tuyệt đối hoặc có `..` thì người đọc mở ra một tệp KHÁC")
        return loi, chua
    if khai_duong and khai_duong != duong:
        loi.append(f"{ten}: `evidence_url` neo đường dẫn `{duong}` nhưng biên nhận khai "
                   f"`verdict_path: {khai_duong}` — mỏ neo KHÔNG neo thứ nó khai")
        return loi, chua
    rc, _ = _git(root, "cat-file", "-e", f"{commit}^{{commit}}")
    if rc != 0:
        chua.append(f"{ten}: KHÔNG ĐO ĐƯỢC commit `{commit[:12]}…` trong `evidence_url`")
        return loi, chua
    # TỔ TIÊN, không chỉ TỒN TẠI. `cat-file -e` chỉ chứng minh object CÓ; một commit nhánh
    # rẽ hoặc dangling vẫn qua. Cross-review vòng 2 (P1) đo trên chính biên nhận mới: nó neo
    # `78ac0ddf…`, và commit ấy KHÔNG phải tổ tiên của `663da64` (chính `reviewed_sha` của
    # nó) — nhưng LÀ tổ tiên của HEAD đang được kiểm. Nên mốc so đúng là HEAD của cây đang
    # validate: mỏ neo phải VỚI TỚI ĐƯỢC từ thứ ta đang xét, không phải chỉ nằm đâu đó.
    rc_hd, _ = _git(root, "rev-parse", "--verify", "HEAD")
    if rc_hd != 0:
        chua.append(f"{ten}: KHÔNG ĐO ĐƯỢC tổ tiên — cây không có HEAD để so")
    else:
        rc_tt, _ = _git(root, "merge-base", "--is-ancestor", commit, "HEAD")
        if rc_tt == 1:
            loi.append(f"{ten}: commit `{commit[:12]}…` CÓ THẬT nhưng KHÔNG phải tổ tiên của "
                       f"HEAD — `canonical_ancestry` đòi mỏ neo với tới được, một nhánh rẽ "
                       f"hay commit dangling không phải canonical ancestry")
            return loi, chua
        if rc_tt not in (0, 1):
            chua.append(f"{ten}: KHÔNG ĐO ĐƯỢC quan hệ tổ tiên của `{commit[:12]}…` (git rc={rc_tt})")
    rc, oid = _git(root, "rev-parse", f"{commit}:{duong}")
    # THAO TÁC GIT THỨ SÁU, và nó cũng có ba trạng thái. `_git` trả 127 khi KHÔNG GỌI ĐƯỢC
    # git (OSError/timeout) — bản trước đọc thẳng "rc khác 0" thành *"mỏ neo trỏ hụt"*, tức
    # một lỗi ĐO thành lời kết tội, `rc=1` thay vì `rc=2`. Cross-review connector trên
    # `670071b` (P2) đo được: bơm rc=127 cho RIÊNG thao tác này ⇒ `loi` có mục, `chua` RỖNG.
    # Đúng lớp `R4-02`, chỉ đổi chỗ — nên nó nằm trong bảng của `c32` chứ không thành ca riêng.
    if rc == 127:
        chua.append(f"{ten}: KHÔNG ĐO ĐƯỢC đường dẫn `{duong}` trong commit "
                    f"`{commit[:12]}…` — không gọi được git")
        return loi, chua
    if rc != 0:
        loi.append(f"{ten}: `evidence_url` khai commit `{commit[:12]}…` CÓ THẬT nhưng "
                   f"KHÔNG chứa đường dẫn `{duong}` — mỏ neo trỏ hụt")
        return loi, chua
    # BYTES, và CHỈ bytes. Bản trước băm `_git(...)` — mà `_git` trả `stdout.strip()` ở text
    # mode — rồi mới đọc lại nhị phân NẾU lệch. Hệ quả đo được (R2-02): cùng một blob được
    # chấp nhận với HAI digest khác nhau, vì một biên nhận có thể khai digest của nội dung
    # đã bị `.strip()`. Không phải va chạm SHA-256 — là băm hai BIỂU DIỄN của cùng một thứ.
    try:
        pb = subprocess.run(["git", "-C", str(root), "cat-file", "-p", oid],
                            capture_output=True, timeout=20)
    except (OSError, subprocess.SubprocessError) as ex:          # noqa: BLE001
        chua.append(f"{ten}: KHÔNG ĐO ĐƯỢC nội dung blob {oid[:12]}… ({type(ex).__name__})")
        return loi, chua
    if pb.returncode != 0:
        chua.append(f"{ten}: KHÔNG ĐO ĐƯỢC nội dung blob {oid[:12]}… (git rc={pb.returncode})")
        return loi, chua
    that = hashlib.sha256(pb.stdout).hexdigest()
    khai = str(d.get("verdict_sha256") or "").strip()
    if not _blob_khop(that, khai):
        loi.append(f"{ten}: blob tại `evidence_url` băm {that[:12]}… nhưng biên nhận khai "
                   f"`verdict_sha256` {khai[:12]}… — mỏ neo KHÔNG trỏ đúng thứ nó khai")
    return loi, chua


# --- CÂU LỊCH SỬ: ba luật SỰ THẬT trên câu phụ thuộc thời điểm (#960) --------------------
# Đặc tả: `ops/specs/NO-CAU-LICH-SU-BIEN-NHAN.md` (M1–M4). Biên nhận chứa câu ĐÚNG lúc ghi mà SAI
# sau đó — "chưa review lại", "chỉ là một nhánh", "surface `codex_service`". Không cổng nào bắt:
# chuỗi review #896 tốn 8 lượt codex và 6 lần áp HINT để vá tay từng thể hiện. Ba luật dưới đây đổi
# việc VÁ TAY thành PHÉP ĐO. Regex chỉ CHỌN ỨNG VIÊN; răng thật là phép đo `reviewed_sha` của biên
# nhận khác, `git merge-base --is-ancestor`, và `run.json`. Regex không chứng minh được đủ mọi cách
# viết tay (đặc tả, `chua_do_duoc`): câu lọt regex là câu cổng KHÔNG đo, không phải câu đã đúng.
#
# KHÔNG CÓ MỐC MIỄN TRỪ (revision 2, `ops/specs/NO-CAU-LICH-SU-BIEN-NHAN-r2.md` M1). Revision 1 nhận mốc
# `dung_tai: <oid40>` trong mapping chứa câu; ba lượt review liên tiếp tìm ba đường tẩy trắng câu cũ qua
# cách xác định "commit đã thêm câu" (blame cả scalar · đổi khoảng trắng · đổi tên tệp). Lớp lỗi ấy bị xoá
# theo kiến trúc: câu trạng thái kèm OID đã sai thì là vi phạm, cách chữa là SỬA CÂU. Luật viết đi kèm:
# biên nhận không viết câu trạng thái kèm OID; lịch sử ghi ở thì quá khứ, không gắn OID vào câu trạng thái.
LUAT_REVIEW = "L-REVIEW"
LUAT_ANCESTRY = "L-ANCESTRY"
LUAT_SURFACE = "L-SURFACE"
CAVEAT_SURFACE = "VERDICT-KHAI-SAI-EXECUTION-SURFACE"
# Câu = đoạn giữa hai dấu kết câu, đo trên scalar ĐÃ NỐI (YAML gấp `>-`, khối `|` thì gộp khoảng trắng).
_RE_CAU = re.compile(r"(?<=[.;!?])\s+")
# Ứng viên OID = MỌI token 7–40 hex thường (sha256 64 hex không lọt vì ranh giới hai đầu); token tra ra
# commit luôn là ứng viên, kể cả viết tắt toàn chữ số / toàn chữ (connector PR #976, P2). Token KHÔNG tra
# được ⇒ KHÔNG ĐO ĐƯỢC chỉ khi có NGỮ CẢNH rõ là OID (r2 M3: đủ 40 hex · trộn số và chữ · trong backtick ·
# ngay sau từ `commit`); token thuần số (số run Actions) / thuần chữ (`deadbeef`) không ngữ cảnh thì bỏ qua.
_RE_OID = re.compile(r"(?<![0-9A-Za-z_])[0-9a-f]{7,40}(?![0-9A-Za-z_])")
_RE_SAU_COMMIT = re.compile(r"\bcommit\s*\Z", re.IGNORECASE)


def _oid_tron(x: str) -> bool:
    return any(c.isdigit() for c in x) and any(c.isalpha() for c in x)


def _oid_bat_buoc(cau: str, m) -> bool:
    """Token OID `m` trong `cau` mà không tra được thì có phải KHÔNG ĐO ĐƯỢC không (r2 M3)."""
    x = m.group(0)
    if len(x) == 40 or _oid_tron(x):
        return True
    truoc, sau = cau[:m.start()], cau[m.end():]
    if truoc.endswith("`") and sau.startswith("`"):
        return True
    return _RE_SAU_COMMIT.search(truoc) is not None
# Khớp trên câu ĐÃ BỎ DẤU và hạ chữ thường, nên biến thể có dấu / không dấu cùng một mẫu.
_RE_CHUA_REVIEW = re.compile(
    r"\b(?:chua|khong)\s+(?:tung\s+)?(?:duoc\s+)?(?:re-?)?review"
    r"|\bnot\s+(?:yet\s+)?(?:been\s+)?re-?reviewed")
_RE_ANCESTRY = re.compile(
    r"\bchi\s+(?:la\s+)?(?:mot\s+)?nhanh\b"
    r"|\b(?:khong|chua)\s+(?:phai\s+|la\s+)?to\s+tien\b"
    r"|\bchua\s+(?:o|toi|den|vao|len)\s+(?:nhanh\s+)?master\b"
    r"|\bcanonical\s+inclusion\s+pending\b"
    r"|\bnot\s+(?:yet\s+)?(?:an?\s+)?ancestor")
_RE_DONG_SURFACE = re.compile(r"execution[_ ]surface", re.IGNORECASE)
_RE_TU = re.compile(r"[a-z][a-z0-9_]*")
_RE_TRICH_DAN = re.compile(r"[\w./-]+\.[A-Za-z0-9]+:\d+")
_RE_PROVIDER = re.compile(r"\bprovider\b", re.IGNORECASE)

# NỢ ĐÃ ĐO của ba luật — (tệp, đường dẫn trường, luật), sinh bằng `--sinh-no-cau-lich-su` trên base
# `4488444` của lease r2 (27-10-2026), nhánh mặc định `origin/master` lúc đo. r1 sinh 66 mục trên `e3ea139`;
# r2 còn 61: hai L-SURFACE gỡ ở PR #976, ba L-SURFACE chết theo định nghĩa lời tự khai mới (M4). CHỈ ĐƯỢC CO LẠI: mục ngoài danh sách là
# vi phạm; mục mà câu đã hết vi phạm là NỢ CHẾT, cũng vi phạm — xoá nó đi.
NO_CAU_LICH_SU: frozenset = frozenset({
    ("ci-g5-cong-cu-chia-manh-r1-review-1-codex-verdict.receipt.yaml", "anchor.mo_ta", LUAT_ANCESTRY),
    ("ci-g5-cong-cu-chia-manh-r1-review-1-codex-verdict.receipt.yaml", "evidence_url_ghi_chu", LUAT_ANCESTRY),
    ("ci-g5-cong-cu-chia-manh-r1-review-10-codex-verdict.receipt.yaml", "anchor.mo_ta", LUAT_ANCESTRY),
    ("ci-g5-cong-cu-chia-manh-r1-review-10-codex-verdict.receipt.yaml", "evidence_url_ghi_chu", LUAT_ANCESTRY),
    ("ci-g5-cong-cu-chia-manh-r1-review-12-codex-verdict.receipt.yaml", "anchor.mo_ta", LUAT_ANCESTRY),
    ("ci-g5-cong-cu-chia-manh-r1-review-12-codex-verdict.receipt.yaml", "evidence_url_ghi_chu", LUAT_ANCESTRY),
    ("ci-g5-cong-cu-chia-manh-r1-review-14-codex-verdict.receipt.yaml", "anchor.mo_ta", LUAT_ANCESTRY),
    ("ci-g5-cong-cu-chia-manh-r1-review-14-codex-verdict.receipt.yaml", "evidence_url_ghi_chu", LUAT_ANCESTRY),
    ("ci-g5-cong-cu-chia-manh-r1-review-15-codex-verdict.receipt.yaml", "anchor.mo_ta", LUAT_ANCESTRY),
    ("ci-g5-cong-cu-chia-manh-r1-review-15-codex-verdict.receipt.yaml", "evidence_url_ghi_chu", LUAT_ANCESTRY),
    ("ci-g5-cong-cu-chia-manh-r1-review-16-codex-verdict.receipt.yaml", "anchor.mo_ta", LUAT_ANCESTRY),
    ("ci-g5-cong-cu-chia-manh-r1-review-16-codex-verdict.receipt.yaml", "evidence_url_ghi_chu", LUAT_ANCESTRY),
    ("ci-g5-cong-cu-chia-manh-r1-review-17-codex-verdict.receipt.yaml", "anchor.mo_ta", LUAT_ANCESTRY),
    ("ci-g5-cong-cu-chia-manh-r1-review-17-codex-verdict.receipt.yaml", "evidence_url_ghi_chu", LUAT_ANCESTRY),
    ("ci-g5-cong-cu-chia-manh-r1-review-18-codex-verdict.receipt.yaml", "anchor.mo_ta", LUAT_ANCESTRY),
    ("ci-g5-cong-cu-chia-manh-r1-review-18-codex-verdict.receipt.yaml", "evidence_url_ghi_chu", LUAT_ANCESTRY),
    ("ci-g5-cong-cu-chia-manh-r1-review-2-codex-verdict.receipt.yaml", "anchor.mo_ta", LUAT_ANCESTRY),
    ("ci-g5-cong-cu-chia-manh-r1-review-2-codex-verdict.receipt.yaml", "evidence_url_ghi_chu", LUAT_ANCESTRY),
    ("ci-g5-cong-cu-chia-manh-r1-review-20-claude-verdict.receipt.yaml", "anchor.mo_ta", LUAT_ANCESTRY),
    ("ci-g5-cong-cu-chia-manh-r1-review-20-claude-verdict.receipt.yaml", "evidence_url_ghi_chu", LUAT_ANCESTRY),
    ("ci-g5-cong-cu-chia-manh-r1-review-21-claude-verdict.receipt.yaml", "anchor.mo_ta", LUAT_ANCESTRY),
    ("ci-g5-cong-cu-chia-manh-r1-review-21-claude-verdict.receipt.yaml", "evidence_url_ghi_chu", LUAT_ANCESTRY),
    ("ci-g5-cong-cu-chia-manh-r1-review-4-codex-verdict.receipt.yaml", "anchor.mo_ta", LUAT_ANCESTRY),
    ("ci-g5-cong-cu-chia-manh-r1-review-4-codex-verdict.receipt.yaml", "evidence_url_ghi_chu", LUAT_ANCESTRY),
    ("ci-g5-cong-cu-chia-manh-r1-review-5-codex-verdict.receipt.yaml", "anchor.mo_ta", LUAT_ANCESTRY),
    ("ci-g5-cong-cu-chia-manh-r1-review-5-codex-verdict.receipt.yaml", "evidence_url_ghi_chu", LUAT_ANCESTRY),
    ("ci-g5-cong-cu-chia-manh-r1-review-6-codex-verdict.receipt.yaml", "anchor.mo_ta", LUAT_ANCESTRY),
    ("ci-g5-cong-cu-chia-manh-r1-review-6-codex-verdict.receipt.yaml", "evidence_url_ghi_chu", LUAT_ANCESTRY),
    ("ci-g5-cong-cu-chia-manh-r1-review-7-codex-verdict.receipt.yaml", "anchor.mo_ta", LUAT_ANCESTRY),
    ("ci-g5-cong-cu-chia-manh-r1-review-7-codex-verdict.receipt.yaml", "evidence_url_ghi_chu", LUAT_ANCESTRY),
    ("ci-g5-cong-cu-chia-manh-r1-review-8-codex-verdict.receipt.yaml", "anchor.mo_ta", LUAT_ANCESTRY),
    ("ci-g5-cong-cu-chia-manh-r1-review-8-codex-verdict.receipt.yaml", "evidence_url_ghi_chu", LUAT_ANCESTRY),
    ("ci-windows-review-5-claude-verdict.receipt.yaml", "chuoi_verdict_ghi_chu", LUAT_ANCESTRY),
    ("doctrine-scan-review-1-claude-verdict.receipt.yaml", "anchor.gioi_han", LUAT_ANCESTRY),
    ("doctrine-scan-review-2-claude-verdict.receipt.yaml", "anchor.gioi_han", LUAT_ANCESTRY),
    ("doctrine-scan-review-3-claude-verdict.receipt.yaml", "anchor.gioi_han", LUAT_ANCESTRY),
    ("lease-publish-windows-do-review-r1-codex.receipt.yaml", "reviewed_sha_to_tien", LUAT_ANCESTRY),
    ("pr455-bien-nhan-v2-review-1-codex-verdict.receipt.yaml", "verdict_usage_caveats[1].noi_dung", LUAT_REVIEW),
    ("pr490-review-7-codex-verdict.receipt.yaml", "verdict_usage_caveats[1].phep_do_BA_LOI_LAND.cong_tren_ban_squash", LUAT_ANCESTRY),
    ("pr508-review-1-codex-verdict.receipt.yaml", "anchor.gioi_han", LUAT_ANCESTRY),
    ("pr508-review-2-codex-verdict.receipt.yaml", "anchor.gioi_han", LUAT_ANCESTRY),
    ("pr508-review-3-codex-verdict.receipt.yaml", "anchor.gioi_han", LUAT_ANCESTRY),
    ("pr508-review-4-codex-verdict.receipt.yaml", "anchor.gioi_han", LUAT_ANCESTRY),
    ("pr508-review-5-codex-verdict.receipt.yaml", "anchor.gioi_han", LUAT_ANCESTRY),
    ("pr526-review-3-codex-verdict.receipt.yaml", "anchor.gioi_han", LUAT_ANCESTRY),
    ("pr896-review-3-codex-verdict.receipt.yaml", "anchor.mo_ta", LUAT_ANCESTRY),
    ("pr896-review-4-codex-verdict.receipt.yaml", "anchor.mo_ta", LUAT_ANCESTRY),
    ("pr896-review-5-codex-verdict.receipt.yaml", "anchor.mo_ta", LUAT_ANCESTRY),
    ("pr896-review-6-codex-verdict.receipt.yaml", "anchor.mo_ta", LUAT_ANCESTRY),
    ("pr896-review-7-codex-verdict.receipt.yaml", "anchor.mo_ta", LUAT_ANCESTRY),
    ("pr896-review-8-codex-verdict.receipt.yaml", "anchor.mo_ta", LUAT_ANCESTRY),
    ("r330-rig-quyet-mau-audit-nguoi-verdict.receipt.yaml", "anchor.gioi_han", LUAT_ANCESTRY),
    ("r330-rig-quyet-mau-audit-nguoi-verdict.receipt.yaml", "land.head_da_doi_TRUOC_merge.vi_sao", LUAT_ANCESTRY),
    ("wp461-review-1-codex-verdict.receipt.yaml", "anchor.cuong_do", LUAT_ANCESTRY),
    ("wp461-review-1-codex-verdict.receipt.yaml", "lich_su_ban_ung_vien.ghi_chu", LUAT_ANCESTRY),
    ("wp523-r15-review-1-codex-verdict.receipt.yaml", "anchor.cuong_do", LUAT_ANCESTRY),
    ("wp523-r15-review-1-codex-verdict.receipt.yaml", "lich_su_ban_ung_vien.ghi_chu", LUAT_ANCESTRY),
    ("wp538-review-1-claude-verdict.receipt.yaml", "anchor.gioi_han", LUAT_ANCESTRY),
    ("wp538-review-2-claude-verdict.receipt.yaml", "anchor.gioi_han", LUAT_ANCESTRY),
    ("wp540-review-1-claude-verdict.receipt.yaml", "anchor.gioi_han", LUAT_ANCESTRY),
    ("wp541-review-1-claude-verdict.receipt.yaml", "ci_tu_dong_tren_ung_vien.thu_hoi", LUAT_ANCESTRY),
})


def _bo_dau(s: str) -> str:
    import unicodedata
    s = s.replace("đ", "d").replace("Đ", "D")
    return "".join(c for c in unicodedata.normalize("NFD", s)
                   if unicodedata.category(c) != "Mn").lower()


def _cac_cau(van: str):
    """Câu của MỘT scalar. Gộp khoảng trắng TRƯỚC khi tách: cụm từ gãy qua dòng vẫn là một câu."""
    return [c for c in _RE_CAU.split(" ".join(van.split())) if c]


class _AliasVong(Exception):
    """Đồ thị YAML có alias VÒNG — không duyệt hết được; người gọi chuyển thành KHÔNG ĐO ĐƯỢC."""


def _duyet_scalar(node, duong="", cha=None, _dang=()):
    """(đường dẫn trường, scalar chuỗi, mapping gần nhất chứa nó) trên cây ĐÃ COMPOSE. `_dang` = danh tính các node TRÊN ĐƯỜNG đang duyệt: alias dùng lại mà không vòng
    vẫn được duyệt theo từng đường; alias vòng (`&a [*a]`, `safe_load` nhận) thì ném `_AliasVong` thay vì
    `RecursionError` ngoài bộ phân ba trạng thái (codex CLI lượt 1, P1)."""
    import yaml
    if isinstance(node, (yaml.MappingNode, yaml.SequenceNode)):
        if id(node) in _dang:
            raise _AliasVong(duong or "<gốc>")
        _dang = _dang + (id(node),)
    if isinstance(node, yaml.MappingNode):
        for k, v in node.value:
            ten = k.value if isinstance(k, yaml.ScalarNode) else "?"
            yield from _duyet_scalar(v, f"{duong}.{ten}" if duong else ten, node, _dang)
    elif isinstance(node, yaml.SequenceNode):
        for i, v in enumerate(node.value):
            yield from _duyet_scalar(v, f"{duong}[{i}]", cha, _dang)
    elif isinstance(node, yaml.ScalarNode) and node.tag.endswith(":str"):
        yield duong, node, cha


class _MoHo(Exception):
    """Tiền tố OID ứng với NHIỀU commit — không kết luận được token trỏ commit nào."""


# TRA GIT CHO BA LUẬT CÂU LỊCH SỬ (r2, quyết định chủ kho 27-10 trên #960: đổi kiến trúc sau review r2 lượt 2).
# Hai lượt review tìm năm nghĩa khác nhau của CÙNG một `rc=1` (vắng · tiền tố mơ hồ · ref hỏng · symref gãy ·
# object rỗng); mỗi bản vá đóng một nghĩa, lượt sau tìm nghĩa kế. Đo 27-10 cho thấy git báo MỌI tình trạng hỏng
# ấy trên STDERR, còn stdout chỉ nói `missing` và rc vẫn 0/1. Nên luật đổi từ "diễn giải rc" sang: kết quả chỉ
# được TIN khi rc thuộc tập sạch đã định cho lệnh ấy VÀ stderr RỖNG; mọi thứ khác là KHÔNG ĐO ĐƯỢC. "Không có"
# chỉ được đọc từ STDOUT của lệnh có giao thức nói ra điều đó (`cat-file --batch-check` in `missing`,
# `for-each-ref` không in ref vắng, `--disambiguate` không in ứng viên).
_RE_HEX_TOKEN = re.compile(r"[0-9a-f]{4,40}")
_ENV_GIT = {"LC_ALL": "C", "LANG": "C", "GIT_TERMINAL_PROMPT": "0", "GIT_NO_LAZY_FETCH": "1",
            "GIT_NO_REPLACE_OBJECTS": "1"}
# Dòng stderr "nền" theo từng kho: cảnh báo cấu hình in ra ở MỌI lệnh git (vd. `core.fsyncObjectFiles is deprecated`,
# đo 29-10) không mang thông tin gì về phép tra cụ thể, nên được trừ đi; đo một lần bằng lệnh không đọc object nào.
_NEN_STDERR: dict = {}


def _env_git() -> dict:
    """Môi trường git CÔ LẬP: bỏ MỌI biến `GIT_*` kế thừa (review r2 lượt 3: `GIT_DIR` làm `-C root` đo nhầm kho;
    `GIT_TRACE*` làm kho lành thành rc=2; `GIT_GRAFT_FILE`/`GIT_REPLACE_REF_BASE` đổi đồ thị) rồi đặt bộ của cổng."""
    return {**{k: v for k, v in os.environ.items() if not k.startswith("GIT_")}, **_ENV_GIT}


def _chay_git(root: Path, args, vao=None, timeout=60):
    """MỘT chỗ gọi git cho ba luật (môi trường cô lập). Không chạy được ⇒ `KhongDoDuoc`."""
    try:
        return subprocess.run(["git", "-C", str(root), *args], input=vao, capture_output=True, text=True,
                              timeout=timeout, env=_env_git())
    except (OSError, subprocess.SubprocessError) as ex:      # noqa: BLE001
        raise KhongDoDuoc(f"không gọi được `git {args[0]}`: {type(ex).__name__}: {ex}") from ex


def _git_do(root: Path, *args, vao=None, sach=(0,), timeout=60) -> tuple[int, str]:
    """Chạy git, trả (rc, STDOUT). Ném `KhongDoDuoc` khi không chạy được, rc ngoài `sach`, hoặc stderr còn dòng nào
    ngoài dòng NỀN của kho (`_NEN_STDERR`)."""
    p = _chay_git(root, args, vao, timeout)
    nen = _NEN_STDERR.get(str(root), frozenset())
    con = [d for d in p.stderr.splitlines() if d.strip() and d not in nen]
    if p.returncode not in sach:
        raise KhongDoDuoc(f"`git {' '.join(args)[:120]}` rc={p.returncode}: {p.stderr.strip()[:300]}")
    if con:
        raise KhongDoDuoc(f"`git {' '.join(args)[:120]}` stderr: {' | '.join(con)[:300]}")
    return p.returncode, p.stdout


def _kho_lanh(root: Path) -> None:
    """Kho đủ để đo tổ tiên, và đo dòng stderr nền. KHÔNG nông (merge-base trên kho nông trả sai mà không báo lỗi);
    KHÔNG partial clone — cả kiểu `extensions.partialclone` lẫn kiểu git hiện hành `remote.<x>.promisor` (object
    vắng có thể là chưa tải); KHÔNG có tệp grafts (đổi parent; lời nhắc deprecated tắt được bằng cấu hình nên
    không trông vào stderr). Replace ref bị tắt bằng `GIT_NO_REPLACE_OBJECTS`. Tính toàn vẹn object/commit-graph
    (băm sai mà git im lặng) là TIỀN ĐỀ, không đo — cần `git fsck` (quyết định chủ kho 29-10, #960)."""
    p = _chay_git(root, ("rev-parse", "--git-dir"))
    if p.returncode != 0:
        raise KhongDoDuoc(f"`git rev-parse --git-dir` rc={p.returncode}: {p.stderr.strip()[:300]}")
    _NEN_STDERR[str(root)] = frozenset(d for d in p.stderr.splitlines() if d.strip())
    nong = _git_do(root, "rev-parse", "--is-shallow-repository")[1].strip()
    if nong != "false":
        raise KhongDoDuoc(f"kho nông (`--is-shallow-repository` = {nong!r}) — không đo được quan hệ tổ tiên")
    if _git_do(root, "config", "--get", "extensions.partialclone", sach=(0, 1))[1].strip():
        raise KhongDoDuoc("kho partial clone (`extensions.partialclone`) — object vắng có thể là chưa tải")
    if _git_do(root, "config", "--get-regexp", r"^remote\..*\.promisor$", sach=(0, 1))[1].strip():
        raise KhongDoDuoc("kho partial clone (`remote.<x>.promisor`) — object vắng có thể là chưa tải")
    gf = _git_do(root, "rev-parse", "--git-path", "info/grafts")[1].strip()
    if gf and (root / gf if not Path(gf).is_absolute() else Path(gf)).exists():
        raise KhongDoDuoc(f"kho có tệp grafts `{gf}` — parent bị thay, không đo được quan hệ tổ tiên")


def _loai_object(root: Path, oid40: str) -> str:
    """Loại của object ĐỦ 40 hex: `commit` / `tag` / `tree` / `blob`; `missing` chỉ khi git nói thế mà stderr rỗng."""
    ra = _git_do(root, "cat-file", "--batch-check=%(objectname) %(objecttype)", vao=f"{oid40}\n")[1].split()
    if ra == [oid40, "missing"]:
        return "missing"
    if len(ra) != 2 or ra[0] != oid40 or ra[1] not in ("commit", "tag", "tree", "blob"):
        raise KhongDoDuoc(f"`cat-file --batch-check` trả dạng lạ cho `{oid40}`: {ra}")
    return ra[1]


def _commit_cua(root: Path, oid: str):
    """Token hex → commit 40 hex · None khi CHẮC CHẮN không commit nào ứng · `_MoHo` khi >1 commit ·
    `KhongDoDuoc` khi git không trả lời sạch. Ứng viên lấy bằng `--disambiguate` (stdout), từng ứng viên đo
    loại bằng `cat-file --batch-check`; chỉ object loại `commit` được tính (tag/tree/blob không phải commit)."""
    if not _RE_HEX_TOKEN.fullmatch(oid):
        raise KhongDoDuoc(f"`{oid}` không phải token hex")
    ung = _git_do(root, "rev-parse", f"--disambiguate={oid}")[1].split()
    loai = {x: _loai_object(root, x) for x in ung if _HEX40.match(x)}
    if len(loai) != len(ung) or "missing" in loai.values():
        raise KhongDoDuoc(f"ứng viên của `{oid}` không đo được loại: {loai or ung}")
    commit = sorted(x for x, lo in loai.items() if lo == "commit")
    if len(commit) > 1:
        raise _MoHo(f"OID `{oid}` mơ hồ — {len(commit)} commit chung tiền tố")
    return commit[0] if commit else None


_REF_MAC_DINH = ("refs/remotes/origin/HEAD", "refs/remotes/origin/master", "refs/heads/master")


def _nhanh_mac_dinh(root: Path):
    """Commit của nhánh mặc định theo thứ tự `_REF_MAC_DINH`. Ref VẮNG ⇒ thử ref kế (CI `pull_request` không có
    `origin/HEAD`). Ref hỏng / symref gãy (git cảnh báo trên stderr) ⇒ `KhongDoDuoc`; ref có mà không trỏ commit
    ⇒ `KhongDoDuoc` — không lùi về ref kế, vì `master` cục bộ không phải nhánh chính tắc."""
    ra = _git_do(root, "for-each-ref", "--format=%(refname) %(objectname) %(objecttype)", *_REF_MAC_DINH)[1]
    co = {}
    for dong in ra.splitlines():
        t = dong.split()
        if len(t) == 3 and t[0] not in _REF_MAC_DINH and t[0].startswith(tuple(r + "/" for r in _REF_MAC_DINH)):
            continue        # `for-each-ref` khớp theo TIỀN TỐ: `refs/heads/master/topic` là ref khác, bỏ qua
        if len(t) != 3 or t[0] not in _REF_MAC_DINH or not _HEX40.match(t[1]):
            raise KhongDoDuoc(f"`for-each-ref` trả dòng lạ: {dong!r}")
        co[t[0]] = (t[1], t[2])
    for ref in _REF_MAC_DINH:
        # `for-each-ref` BỎ IM LẶNG symref gãy (không stderr — đo 27-10), nên hỏi riêng: symref trỏ ref không có
        # ⇒ nguồn chính tắc hỏng, không phải vắng.
        rc, dich = _git_do(root, "symbolic-ref", "-q", ref, sach=(0, 1))
        if rc == 0 and ref not in co:
            raise KhongDoDuoc(f"`{ref}` là dangling symref (trỏ `{dich.strip()}` không có)")
        if ref in co:
            sha, lo = co[ref]
            if lo != "commit":
                raise KhongDoDuoc(f"ref mặc định `{ref}` trỏ {lo}, không phải commit")
            return sha
    return None


def _vang(p: Path) -> bool:
    """Đường dẫn VẮNG thật — không mục nào, kể cả symlink gãy. Có mục (thư mục, symlink gãy) hoặc lỗi
    stat khác ⇒ KHÔNG vắng: người gọi phải thử đọc và báo KHÔNG ĐO ĐƯỢC (r2 review 1,
    `run-json-thu-muc-thanh-khong-ap`: `is_file()` gộp thư mục với vắng)."""
    try:
        p.lstat()
    except (FileNotFoundError, NotADirectoryError):
        return True
    except OSError:
        return False
    return False


def _luot(d):
    v = d.get("luot")
    return v if isinstance(v, int) and not isinstance(v, bool) else None


def _surface_cua_verdict(root: Path, d: dict, s_that: str, be_mat: frozenset):
    """Các giá trị surface verdict TỰ KHAI khác `s_that`. `None` = verdict không đọc được."""
    vp = str(d.get("verdict_path") or "").strip()
    if not vp or vp.startswith("/") or ".." in Path(vp).parts or not (root / vp).is_file():
        return None
    try:
        van = (root / vp).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    sai = set()
    dong_tep = van.splitlines()
    for j, dong in enumerate(dong_tep):
        ms = list(_RE_DONG_SURFACE.finditer(dong))
        if not ms:
            continue
        # LỜI TỰ KHAI (r2 M4): trong cửa sổ {dòng trước, dòng ấy, dòng sau} có từ `provider` VÀ không có trích
        # dẫn `đường/dẫn.ext:N`. Revision 1 quét toàn văn nên mô tả fixture, đoạn trích verdict khác và tham
        # chiếu văn xuôi đều thành "tự khai" (3 nợ dương tính giả + caveat bắt buộc trên chính biên nhận #960).
        cua = dong_tep[max(0, j - 1):j + 2]
        if not any(_RE_PROVIDER.search(x) for x in cua) or any(_RE_TRICH_DAN.search(x) for x in cua):
            continue
        # MỌI khai báo trên dòng, mỗi cái lấy giá trị trong đoạn tới khai báo kế (codex CLI lượt 1, P1).
        for i, m in enumerate(ms):
            doan = dong[m.end():ms[i + 1].start() if i + 1 < len(ms) else len(dong)]
            tu = next((t for t in _RE_TU.findall(doan) if t in be_mat), None)
            if tu and tu != s_that:
                sai.add(tu)
    return sai


def _kiem_cau_lich_su(root: Path, tep: dict, nhanh=None):
    """Chạy L-REVIEW · L-ANCESTRY · L-SURFACE trên MỌI biên nhận đọc được (kể cả legacy/nợ v2).

    `tep`: tên → (dict, văn bản). Trả (vi_pham: {(tên, trường, luật): lý do},
    chua: {(tên, trường, luật): lý do}, surface_chua_do: [lý do]) — `chua` là trạng thái thứ ba
    (rc=2), `surface_chua_do` là ca luật KHÔNG ÁP (run_json khai mà KHÔNG CÓ tệp) theo đặc tả A4."""
    import json
    import yaml
    vp, chua, sf_chua = {}, {}, []
    da_review = {}
    for ten, (d, _) in tep.items():
        sha = str(d.get("reviewed_sha") or "").strip()
        if _HEX40.match(sha):
            da_review.setdefault(sha, []).append((ten, _luot(d)))
    be_mat = frozenset().union(*(v["be_mat"] for v in PROVIDER_HOP_DONG.values())) \
        if PROVIDER_HOP_DONG else frozenset()
    nhanh_md = [nhanh]                      # tính lười: chỉ hỏi git khi có ứng viên ancestry

    def _nhanh():
        if nhanh_md[0] is None:
            nhanh_md[0] = _nhanh_mac_dinh(root) or ""
        return nhanh_md[0]

    da_kiem_kho = []

    def _tra(x):
        if not da_kiem_kho:                 # MỘT lần, trước phép tra đầu tiên: kho nông/partial ⇒ cả lượt rc=2
            _kho_lanh(root)
            da_kiem_kho.append(True)
        return _commit_cua(root, x)

    for ten, (d, van) in tep.items():
        # MỘT BIÊN cho lỗi đo (r2 M2): mọi ngoại lệ không lường trước khi đo MỘT biên nhận ⇒ KHÔNG ĐO
        # ĐƯỢC cho cả tệp (khoá trường `*`), và `kiem` không kết luận nợ nào của tệp ấy là nợ chết. Ba lượt
        # review r1 tìm lỗi đo bị đổi thành sạch/vi phạm ở từng chỗ một; biên này đóng cả lớp thay vì vá chỗ.
        try:
            cay = yaml.compose(van, Loader=yaml.SafeLoader)
            luot_nay = _luot(d)
            try:
                scalar = list(_duyet_scalar(cay))
            except _AliasVong as ex:
                raise KhongDoDuoc(f"{ten}: YAML có alias VÒNG ở `{ex}` — không duyệt được câu") from ex
            for duong, node, cha in scalar:
                for cau in _cac_cau(node.value):
                    chuan = _bo_dau(cau)
                    oids = _RE_OID.findall(cau)
                    if not oids:
                        continue
                    if _RE_CHUA_REVIEW.search(chuan):
                        k = (ten, duong, LUAT_REVIEW)
                        for h in (o for o in oids if len(o) == 40):
                            sau = [(t, lu) for t, lu in da_review.get(h, ()) if t != ten]
                            if not sau:
                                continue
                            if luot_nay is None or any(lu is None for _, lu in sau):
                                chua.setdefault(k, f"{ten}: `{duong}` khai {h[:12]}… chưa review, có "
                                                   f"biên nhận khác cùng `reviewed_sha` mà `luot` không so "
                                                   f"được ({sorted(t for t, _ in sau)})")
                                continue
                            lon = sorted(t for t, lu in sau if lu > luot_nay)
                            if not lon:
                                continue
                            vp.setdefault(k, f"{ten}: `{duong}` khai head {h[:12]}… chưa được review (lại), "
                                             f"nhưng {lon} đã review đúng SHA ấy ở `luot` lớn hơn {luot_nay} "
                                             f"— câu đã cũ; sửa câu")
                    if _RE_ANCESTRY.search(chuan):
                        k = (ten, duong, LUAT_ANCESTRY)
                        for mo in _RE_OID.finditer(cau):
                            x = mo.group(0)
                            try:
                                c = _tra(x)
                            except _MoHo as ex:
                                chua.setdefault(k, f"{ten}: `{duong}` — {ex}, KHÔNG kết luận được quan hệ tổ tiên")
                                continue
                            if c is None and not _oid_bat_buoc(cau, mo):
                                continue                 # số / từ thường không ngữ cảnh, không phải OID
                            if c is None:
                                chua.setdefault(k, f"{ten}: `{duong}` — OID `{x}` không tra được commit, "
                                                   f"KHÔNG kết luận được quan hệ tổ tiên")
                                continue
                            md = _nhanh()
                            if not md:
                                chua.setdefault(k, f"{ten}: `{duong}` — không tìm được nhánh mặc định để so")
                                continue
                            try:
                                rc, _ = _git_do(root, "merge-base", "--is-ancestor", c, md, sach=(0, 1))
                            except KhongDoDuoc as ex:
                                chua.setdefault(k, f"{ten}: `{duong}` — `merge-base` cho `{x}`: {ex}")
                                continue
                            if rc == 1:
                                continue
                            vp.setdefault(k, f"{ten}: `{duong}` nói `{x}` chưa vào / không là tổ tiên nhánh "
                                             f"mặc định, nhưng nay `{x}` ĐÃ là tổ tiên — câu đã cũ; sửa câu")
            mri = d.get("model_reviewer_identity")
            rj = _chuoi(mri.get("run_json")) if isinstance(mri, dict) else None
            if not rj:
                continue
            if PROVIDER_NGUON_HONG is not None or not be_mat:
                # Không có từ vựng surface thì KHÔNG ĐO được, và không đo được thì không được kết luận
                # mục nợ đã CHẾT — đúng lớp `R4-02`: lỗi ĐO bị báo thành VI PHẠM.
                chua[(ten, "verdict_path", LUAT_SURFACE)] = (
                    f"{ten}: KHÔNG ĐO ĐƯỢC L-SURFACE — không có từ vựng execution surface của kho")
                continue
            p_rj = root / rj
            if rj.startswith("/") or ".." in Path(rj).parts or _vang(p_rj):
                sf_chua.append(f"{ten}: `run_json` {rj} không có trong kho — L-SURFACE không áp")
                continue
            # TỆP CÓ mà đọc/phân tích hỏng ⇒ KHÔNG ĐO ĐƯỢC (rc=2), không phải "không áp": miễn trừ của
            # đặc tả A4 chỉ dành cho tệp VẮNG. Bản trước gộp hai ca nên một run.json hỏng làm nợ L-SURFACE
            # thành "NỢ CHẾT" — lỗi ĐO thành VI PHẠM, lớp `R4-02` (connector PR #976, P2).
            k_sf = (ten, "verdict_path", LUAT_SURFACE)
            try:
                s_that = _chuoi(json.loads(p_rj.read_text(encoding="utf-8")).get("execution_surface"))
            except (OSError, UnicodeDecodeError, ValueError, AttributeError):
                s_that = None
            if not s_that:
                chua[k_sf] = f"{ten}: `{rj}` có mà không đọc được `execution_surface` — KHÔNG ĐO ĐƯỢC L-SURFACE"
                continue
            sai = _surface_cua_verdict(root, d, s_that, be_mat)
            if sai is None:
                chua[k_sf] = f"{ten}: verdict không đọc được — KHÔNG ĐO ĐƯỢC L-SURFACE"
                continue
            cv = d.get("verdict_usage_caveats")
            ids = {_chuoi(c.get("id")) for c in cv if isinstance(c, dict)} if isinstance(cv, list) else set()
            if sai and CAVEAT_SURFACE not in ids:
                vp[k_sf] = (
                    f"{ten}: verdict khai execution surface {sorted(sai)} khác `run.json` "
                    f"(`{s_that}`) mà thiếu caveat `{CAVEAT_SURFACE}`")
        except KhongDoDuoc:
            raise
        except Exception as ex:                                  # noqa: BLE001
            chua[(ten, "*", "*")] = (f"{ten}: KHÔNG ĐO ĐƯỢC câu lịch sử — {type(ex).__name__}: {ex}")
    return vp, chua, sf_chua


def kiem(root: Path, allowlist=None, no_da_do=None, no_cau_lich_su=None, nhanh_mac_dinh=None):
    """Trả (loi, thong_ke). `loi` rỗng ⇒ sạch. Ném `KhongDoDuoc` cho trạng thái thứ ba.

    `allowlist`/`no_da_do`/`no_cau_lich_su` tiêm được ĐỂ TEST ĐỘT BIẾN ĐƯỢC — cổng không có
    đường nới các danh sách ấy lúc chạy (CLI không nhận cờ nào cho chúng).
    """
    try:
        import yaml
    except ImportError as ex:                                   # pragma: no cover
        raise KhongDoDuoc(f"thiếu PyYAML: {ex}") from ex
    al = ALLOWLIST_CUTOVER if allowlist is None else allowlist
    no = NO_DA_DO if no_da_do is None else no_da_do
    no_cau = NO_CAU_LICH_SU if no_cau_lich_su is None else no_cau_lich_su
    tm = root / THU_MUC
    if not tm.is_dir():
        if (root / ".git").exists():
            raise KhongDoDuoc(f"kho thật mà không có {tm} — không phải 'sạch'")
        return [], {"tong": 0, "dat": 0, "mien_tru": 0, "no": 0, "bo_qua_vi_khong_phai_kho": True}

    ds = sorted(tm.glob("*.receipt.yaml"))
    if not ds:
        raise KhongDoDuoc(f"{tm} không có tệp `*.receipt.yaml` nào — mốc neo đã đổi?")

    loi, chua_do, dat, mien_tru, nod = [], [], 0, 0, 0
    if PROVIDER_NGUON_HONG is not None:
        # MỘT mục cho CẢ LƯỢT, không phải mỗi tệp một mục: đây là hỏng MÔI TRƯỜNG, không
        # phải khuyết tật của từng biên nhận. Nói thẳng phép kiểm nào KHÔNG chạy, kẻo
        # "cổng đỏ" bị đọc thành "đã đo và biên nhận sai".
        chua_do.append(f"KHÔNG ĐO ĐƯỢC danh sách provider chính tắc — {PROVIDER_NGUON_HONG}; "
                       f"mọi phép kiểm suy từ provider (danh sách CHO PHÉP, bề mặt/vận chuyển, "
                       f"giới hạn assurance theo provider) KHÔNG chạy lượt này — kiểm kiểu, SHA "
                       f"và bằng chứng phiên độc lập vẫn chạy")
    tep_doc = {}
    for p in ds:
        ten = p.name
        try:
            # Băm + đọc trong CÙNG biên (r2 M2, finding `receipt-khong-doc-duoc-thoat-1`): `_bam` từng nằm
            # ngoài khối bắt lỗi nên lỗi I/O thoát thành traceback rc=1 thay vì trạng thái thứ ba.
            b = _bam(p)
            van = p.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError) as ex:
            raise KhongDoDuoc(f"{ten}: không đọc được ({type(ex).__name__}: {ex})") from ex
        try:
            d = yaml.safe_load(van)
        except Exception as ex:                                  # noqa: BLE001
            raise KhongDoDuoc(f"{ten}: YAML hỏng ({type(ex).__name__}: {ex})") from ex
        if isinstance(d, dict):
            tep_doc[ten] = (d, van)
        if ten in al:
            if al[ten] != b:
                loi.append(f"{ten}: NẰM TRONG allowlist legacy mà băm ĐÃ ĐỔI "
                           f"(đóng băng {al[ten][:12]}…, nay {b[:12]}…) — miễn trừ neo vào BĂM, "
                           f"sửa tệp là mất miễn trừ; đưa nó lên v2 hoặc hoàn nguyên")
            else:
                mien_tru += 1
            continue
        if not isinstance(d, dict):
            loi.append(f"{ten}: nội dung không phải ánh xạ YAML")
            continue
        vi_pham = _thieu(d)
        if not vi_pham:
            g_loi, g_chua = _neo_git(root, ten, d)
            vi_pham += g_loi
            chua_do.extend(g_chua)
        if not vi_pham:
            dat += 1
            if ten in no:
                loi.append(f"{ten}: ĐÃ ĐẠT v2 mà vẫn nằm trong `NO_DA_DO` — gỡ nó khỏi danh "
                           f"sách nợ; bánh cóc chỉ quay một chiều")
            continue
        if ten in no:
            if no[ten] != b:
                loi.append(f"{ten}: NỢ ĐÃ ĐO mà băm ĐÃ ĐỔI (đóng băng {no[ten][:12]}…, nay "
                           f"{b[:12]}…) — đã sửa tệp thì sửa cho ĐẠT v2, đừng đóng băng lại "
                           f"một bản không đạt: " + " · ".join(vi_pham))
            else:
                nod += 1
            continue
        loi.append(f"{ten}: KHÔNG đạt v2 và KHÔNG nằm trong danh sách nào — "
                   + " · ".join(vi_pham))
    # CÂU LỊCH SỬ (#960). Nợ chỉ CO: ngoài danh sách ⇒ vi phạm; trong danh sách mà hết vi phạm ⇒ NỢ
    # CHẾT, cũng vi phạm. Mục đang KHÔNG ĐO ĐƯỢC thì không được kết luận là chết — ba trạng thái.
    # Mục nợ của tệp KHÔNG có trong cây thì bỏ qua, như `NO_DA_DO`; tệp nợ bị xoá khỏi kho thật do
    # `ops/bien_nhan_v2_test.py` canh (mọi mục nợ phải trỏ tệp có thật).
    vp_cau, chua_cau, sf_chua = _kiem_cau_lich_su(root, tep_doc, nhanh_mac_dinh)
    no_cau_dem = {LUAT_REVIEW: 0, LUAT_ANCESTRY: 0, LUAT_SURFACE: 0}
    for k in sorted(vp_cau):
        if k in no_cau:
            no_cau_dem[k[2]] += 1
        else:
            loi.append(f"[{k[2]}] {vp_cau[k]}")
    tep_hong = {k[0] for k in chua_cau if k[1] == "*"}
    for k in sorted(no_cau):
        if k[0] in tep_doc and k[0] not in tep_hong and k not in vp_cau and k not in chua_cau:
            loi.append(f"[{k[2]}] {k[0]}: `{k[1]}` NỢ CHẾT — nằm trong `NO_CAU_LICH_SU` mà câu đã hết "
                       f"vi phạm; xoá mục nợ, bánh cóc chỉ quay một chiều")
    chua_do.extend(f"[{k[2]}] {v}" for k, v in sorted(chua_cau.items()))
    return loi, {"tong": len(ds), "dat": dat, "mien_tru": mien_tru, "no": nod,
                  "chua_do": chua_do, "no_cau": no_cau_dem, "surface_chua_do": sf_chua,
                  "vi_pham_cau": sorted(vp_cau)}


class KhongDoDuoc(Exception):
    """Trạng thái thứ ba. KHÔNG được đọc thành 'sạch'."""


def _ma_thoat(loi, tk) -> int:
    """Mã thoát của CLI từ kết quả `kiem` — MỘT chỗ quyết định, để ca test đo đúng thứ CLI trả."""
    if tk.get("chua_do"):
        return RC_KHONG_DO_DUOC
    return RC_VI_PHAM if loi else RC_SACH


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".", help="gốc kho")
    ap.add_argument("--sinh-no", action="store_true",
                    help="IN ra khối `NO_DA_DO` cho trạng thái hiện tại — dùng MỘT LẦN lúc "
                         "đóng băng nợ; KHÔNG ghi đè tệp, người vá tự dán và tự chịu trách nhiệm")
    ap.add_argument("--sinh-no-cau-lich-su", action="store_true",
                    help="IN ra khối `NO_CAU_LICH_SU` (vi phạm L-REVIEW/L-ANCESTRY/L-SURFACE hiện có) — "
                         "như `--sinh-no`: KHÔNG ghi đè tệp")
    a = ap.parse_args(argv)
    root = Path(a.root).resolve()
    try:
        # Hai cờ sinh nợ đi qua CÙNG biên với cổng (r2 review 1, `sinh-no-ngoai-bien-doc-receipt`).
        if a.sinh_no:
            return _sinh_no(root)
        if a.sinh_no_cau_lich_su:
            return _sinh_no_cau(root)
        loi, tk = kiem(root)
    except KhongDoDuoc as ex:
        print(f"KHÔNG ĐO ĐƯỢC: {ex}", file=sys.stderr)
        return RC_KHONG_DO_DUOC
    if tk.get("bo_qua_vi_khong_phai_kho"):
        print(f"bien_nhan_v2: bỏ qua — {root / THU_MUC} không có và cây không phải kho git")
        return RC_SACH
    for x in loi:
        print(f"  ĐỎ  {x}", file=sys.stderr)
    for x in tk.get("chua_do") or []:
        # In RIÊNG. Đây là trạng thái THỨ BA — không phải "sạch", cũng không phải "vi phạm".
        print(f"  KHÔNG ĐO ĐƯỢC  {x}", file=sys.stderr)
    print(f"\nbien_nhan_v2: {tk['dat']} ĐẠT v2 · {tk['mien_tru']}/{len(ALLOWLIST_CUTOVER)} miễn trừ "
          f"legacy (băm khớp) · {tk['no']} NỢ đóng băng · {len(loi)} vi phạm · "
          f"{len(tk.get('chua_do') or [])} KHÔNG ĐO ĐƯỢC · tổng {tk['tong']}")
    nc = tk.get("no_cau") or {}
    print(f"câu lịch sử: nợ {LUAT_REVIEW} {nc.get(LUAT_REVIEW, 0)} · {LUAT_ANCESTRY} "
          f"{nc.get(LUAT_ANCESTRY, 0)} · {LUAT_SURFACE} {nc.get(LUAT_SURFACE, 0)} · "
          f"{LUAT_SURFACE} chua_do_duoc {len(tk.get('surface_chua_do') or [])}")
    rc = _ma_thoat(loi, tk)
    if rc == RC_VI_PHAM:
        print("TỔNG: ĐỎ", file=sys.stderr)
        return RC_VI_PHAM
    if rc == RC_KHONG_DO_DUOC:
        # ƯU TIÊN cho trạng thái thứ ba khi HAI thứ cùng có. Bản trước trả `RC_VI_PHAM`
        # trước nên một kết quả HỖN HỢP bị gộp thành "vi phạm thường", và bên điều phối sẽ
        # đọc "thiếu bằng chứng" thành "đã đo và sai" — hai kết luận khác hẳn nhau.
        # Cả hai nhóm vẫn được IN đầy đủ ở trên; chỉ mã thoát đổi.
        # ĐẢO LẠI QUYẾT ĐỊNH CỦA CHÍNH BẢN TRƯỚC — cross-review vòng 2 (P1) bắt đúng chỗ.
        # Bản trước in `KHÔNG ĐO ĐƯỢC` ra stderr rồi vẫn `TỔNG: ĐẠT` + rc=0, nên một SHA BỊA
        # hoặc một checkout nông ĐI QUA ĐƯỢC cổng CI bắt buộc. Đo được: bơm `deadbeef`*5 vào
        # một biên nhận ⇒ `1 KHÔNG ĐO ĐƯỢC` trên stderr, mà `rc=0` và `TỔNG: ĐẠT`.
        # Đó đúng là thứ chính docstring của tệp này tố cáo: "một cổng tự tắt khi thiếu công
        # cụ là cổng không tồn tại đúng lúc nó cần nhất". `KHÔNG ĐO ĐƯỢC` ≠ `ĐẠT`.
        # Lưu ý nó KHÔNG đồng nghĩa "bịa": mã thoát 2 nói KHÔNG KẾT LUẬN ĐƯỢC, khác mã 1.
        print("TỔNG: KHÔNG ĐO ĐƯỢC", file=sys.stderr)
        return RC_KHONG_DO_DUOC
    print("TỔNG: ĐẠT")
    return RC_SACH


def _sinh_no(root: Path) -> int:
    try:
        import yaml
    except ImportError as ex:                                   # pragma: no cover
        raise KhongDoDuoc(f"thiếu PyYAML: {ex}") from ex
    tm = root / THU_MUC
    ra = {}
    for p in sorted(tm.glob("*.receipt.yaml")):
        if p.name in ALLOWLIST_CUTOVER:
            continue
        try:
            d = yaml.safe_load(p.read_text(encoding="utf-8"))
            b = _bam(p)
        except Exception as ex:                                  # noqa: BLE001 — như `kiem`: SafeLoader còn ném
            # ValueError (timestamp `2026-99-99`) và RecursionError (lồng sâu) — review r2 lượt 2
            raise KhongDoDuoc(f"{p.name}: không sinh được nợ ({type(ex).__name__}: {ex})") from ex
        if isinstance(d, dict) and not _thieu(d):
            continue
        ra[p.name] = b
    print("NO_DA_DO: dict[str, str] = {")
    for k, v in ra.items():
        print(f'    "{k}":\n        "{v}",')
    print("}")
    print(f"# {len(ra)} tệp", file=sys.stderr)
    return RC_SACH


def _sinh_no_cau(root: Path) -> int:
    try:
        _, tk = kiem(root, no_cau_lich_su=frozenset())
    except KhongDoDuoc as ex:
        print(f"KHÔNG ĐO ĐƯỢC: {ex}", file=sys.stderr)
        return RC_KHONG_DO_DUOC
    print("NO_CAU_LICH_SU: frozenset = frozenset({")
    for t, tr, lu in tk["vi_pham_cau"]:
        hang = {LUAT_REVIEW: "LUAT_REVIEW", LUAT_ANCESTRY: "LUAT_ANCESTRY", LUAT_SURFACE: "LUAT_SURFACE"}[lu]
        print(f'    ("{t}", "{tr}", {hang}),')
    print("})")
    print(f"# {len(tk['vi_pham_cau'])} mục", file=sys.stderr)
    return RC_KHONG_DO_DUOC if tk.get("chua_do") else RC_SACH


if __name__ == "__main__":
    sys.exit(main())
