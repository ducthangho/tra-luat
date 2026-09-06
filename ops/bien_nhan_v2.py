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

ANCHOR_KHOA = ("loai", "cuong_do")


def _co_chuoi(d, k):
    v = d.get(k)
    return None if isinstance(v, str) and v.strip() else f"thiếu/rỗng `{k}`"


def _khop(d, k, re_, mo_ta):
    v = d.get(k)
    if not isinstance(v, str) or not v.strip():
        return f"thiếu/rỗng `{k}`"
    return None if re_.match(v.strip()) else f"`{k}`={v.strip()[:24]!r} không phải {mo_ta}"


def _mri(d):
    """`model_reviewer_identity` phải là ánh xạ có `provider` — KHÔNG chỉ là 'có khoá'.

    Đo được (cross-review PR #455, F2/P1-B): bản đầu nhận `{x: 1}`, tức cổng identity đo
    đúng SỰ CÓ MẶT của khoá. Chỉ đòi `provider`: lược đồ chi tiết của khối này CHƯA có
    trong protocol, nên siết thêm là tự bịa hợp đồng — bốn biên nhận v2 chuẩn của kho đều
    khai `KHONG_do_duoc` cho ID model, và đó là trạng thái ĐÚNG, không phải thiếu sót."""
    v = d.get("model_reviewer_identity")
    if not isinstance(v, dict) or not v:
        return "thiếu/rỗng ánh xạ `model_reviewer_identity`"
    if not str(v.get("provider") or "").strip():
        return "`model_reviewer_identity` không có `provider` — ánh xạ không rỗng KHÔNG phải attestation"
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
    if not str(v.get("actor") or "").strip():
        return "`github_submitter_identity` không null mà không có `actor`"
    return None


def _anchor(d):
    a = d.get("anchor")
    if not isinstance(a, dict) or not a:
        return ["thiếu/rỗng ánh xạ `anchor`"]
    loi = [f"`anchor.{k}` thiếu/rỗng" for k in ANCHOR_KHOA if not str(a.get(k) or "").strip()]
    loai = str(a.get("loai") or "").strip()
    if loai and loai not in ANCHOR_LOAI_CHO_PHEP:
        loi.append(f"`anchor.loai`={loai!r} ngoài danh sách CHO PHÉP {sorted(ANCHOR_LOAI_CHO_PHEP)}")
    return loi


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
    ("model_reviewer_identity", _mri),
    ("github_submitter_identity", _gsi),
    ("anchor", lambda d: "; ".join(_anchor(d)) or None),
)

# Mức assurance HÀM Ý một lượt review có thẩm quyền. Biên nhận nào TỰ KHAI là chạy bằng
# subagent trong cùng phiên điều phối (không phiên riêng, không neo launcher) thì KHÔNG được
# khai mức ấy — F3 của cross-review PR #455: chính khối identity mới thêm nói tính độc lập là
# KHÔNG ĐO ĐƯỢC rồi lấy đó biện minh cho `same_provider_approved`.
ASSURANCE_CAN_DOC_LAP = frozenset({"cross_approved", "same_provider_approved", "human_audited"})
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


def _thieu(d: dict) -> list[str]:
    """Trả danh sách lý do tệp KHÔNG đạt v2. Rỗng = đạt (theo CẤU TRÚC)."""
    loi = [msg for _, kt in YEU_CAU for msg in [kt(d)] if msg]
    # Chốt CHÉO: assurance vs. bằng chứng độc lập mà chính biên nhận tự khai.
    mri = d.get("model_reviewer_identity")
    if isinstance(mri, dict):
        trong_phien = "subagent" in str(mri.get("che_do") or "").lower()
        khong_neo = "neo_boi_launcher" in mri and not mri.get("neo_boi_launcher")
        khai = str(d.get("assurance") or d.get("assurance_dat") or "").strip()
        if (trong_phien or khong_neo) and khai in ASSURANCE_CAN_DOC_LAP:
            loi.append(
                f"khai `{khai}` trong khi tự khai KHÔNG có phiên độc lập "
                f"(che_do={mri.get('che_do')!r}, neo_boi_launcher={mri.get('neo_boi_launcher')!r}) "
                f"— mức ấy hàm ý một lượt review có thẩm quyền; dùng `review_deferred`")
    return loi


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
    if not (isinstance(a, dict) and a.get("loai") == "canonical_ancestry"):
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
    rc, _ = _git(root, "cat-file", "-e", f"{commit}^{{commit}}")
    if rc != 0:
        chua.append(f"{ten}: KHÔNG ĐO ĐƯỢC commit `{commit[:12]}…` trong `evidence_url`")
        return loi, chua
    rc, oid = _git(root, "rev-parse", f"{commit}:{duong}")
    if rc != 0:
        loi.append(f"{ten}: `evidence_url` khai commit `{commit[:12]}…` CÓ THẬT nhưng "
                   f"KHÔNG chứa đường dẫn `{duong}` — mỏ neo trỏ hụt")
        return loi, chua
    rc, noi_dung = _git(root, "cat-file", "-p", oid)
    if rc != 0:
        chua.append(f"{ten}: KHÔNG ĐO ĐƯỢC nội dung blob {oid[:12]}…")
        return loi, chua
    that = hashlib.sha256(noi_dung.encode("utf-8")).hexdigest()
    khai = str(d.get("verdict_sha256") or "").strip()
    if that != khai:
        # `cat-file -p` qua text mode có thể đổi kết thúc dòng trên Windows; đo lại bằng
        # đường nhị phân trước khi kết luận, kẻo báo động giả theo NỀN.
        try:
            pb = subprocess.run(["git", "-C", str(root), "cat-file", "-p", oid],
                                capture_output=True, timeout=20)
            that = hashlib.sha256(pb.stdout).hexdigest()
        except (OSError, subprocess.SubprocessError):        # noqa: BLE001
            pass
    if not _blob_khop(that, khai):
        loi.append(f"{ten}: blob tại `evidence_url` băm {that[:12]}… nhưng biên nhận khai "
                   f"`verdict_sha256` {khai[:12]}… — mỏ neo KHÔNG trỏ đúng thứ nó khai")
    return loi, chua


def kiem(root: Path, allowlist=None, no_da_do=None):
    """Trả (loi, thong_ke). `loi` rỗng ⇒ sạch. Ném `KhongDoDuoc` cho trạng thái thứ ba.

    `allowlist`/`no_da_do` tiêm được ĐỂ TEST ĐỘT BIẾN ĐƯỢC — cổng không có đường nới hai
    danh sách ấy lúc chạy (CLI không nhận cờ nào cho chúng).
    """
    try:
        import yaml
    except ImportError as ex:                                   # pragma: no cover
        raise KhongDoDuoc(f"thiếu PyYAML: {ex}") from ex
    al = ALLOWLIST_CUTOVER if allowlist is None else allowlist
    no = NO_DA_DO if no_da_do is None else no_da_do
    tm = root / THU_MUC
    if not tm.is_dir():
        if (root / ".git").exists():
            raise KhongDoDuoc(f"kho thật mà không có {tm} — không phải 'sạch'")
        return [], {"tong": 0, "dat": 0, "mien_tru": 0, "no": 0, "bo_qua_vi_khong_phai_kho": True}

    ds = sorted(tm.glob("*.receipt.yaml"))
    if not ds:
        raise KhongDoDuoc(f"{tm} không có tệp `*.receipt.yaml` nào — mốc neo đã đổi?")

    loi, chua_do, dat, mien_tru, nod = [], [], 0, 0, 0
    for p in ds:
        ten, b = p.name, _bam(p)
        if ten in al:
            if al[ten] != b:
                loi.append(f"{ten}: NẰM TRONG allowlist legacy mà băm ĐÃ ĐỔI "
                           f"(đóng băng {al[ten][:12]}…, nay {b[:12]}…) — miễn trừ neo vào BĂM, "
                           f"sửa tệp là mất miễn trừ; đưa nó lên v2 hoặc hoàn nguyên")
            else:
                mien_tru += 1
            continue
        try:
            d = yaml.safe_load(p.read_text(encoding="utf-8"))
        except Exception as ex:                                  # noqa: BLE001
            raise KhongDoDuoc(f"{ten}: YAML hỏng ({type(ex).__name__}: {ex})") from ex
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
    return loi, {"tong": len(ds), "dat": dat, "mien_tru": mien_tru, "no": nod,
                  "chua_do": chua_do}


class KhongDoDuoc(Exception):
    """Trạng thái thứ ba. KHÔNG được đọc thành 'sạch'."""


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".", help="gốc kho")
    ap.add_argument("--sinh-no", action="store_true",
                    help="IN ra khối `NO_DA_DO` cho trạng thái hiện tại — dùng MỘT LẦN lúc "
                         "đóng băng nợ; KHÔNG ghi đè tệp, người vá tự dán và tự chịu trách nhiệm")
    a = ap.parse_args(argv)
    root = Path(a.root).resolve()
    if a.sinh_no:
        return _sinh_no(root)
    try:
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
    if loi:
        print("TỔNG: ĐỎ", file=sys.stderr)
        return RC_VI_PHAM
    print("TỔNG: ĐẠT")
    return RC_SACH


def _sinh_no(root: Path) -> int:
    import yaml
    tm = root / THU_MUC
    ra = {}
    for p in sorted(tm.glob("*.receipt.yaml")):
        if p.name in ALLOWLIST_CUTOVER:
            continue
        d = yaml.safe_load(p.read_text(encoding="utf-8"))
        if isinstance(d, dict) and not _thieu(d):
            continue
        ra[p.name] = _bam(p)
    print("NO_DA_DO: dict[str, str] = {")
    for k, v in ra.items():
        print(f'    "{k}":\n        "{v}",')
    print("}")
    print(f"# {len(ra)} tệp", file=sys.stderr)
    return RC_SACH


if __name__ == "__main__":
    sys.exit(main())
