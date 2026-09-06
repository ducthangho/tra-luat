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
  · Nó không đọc git, không ra mạng. `evidence_url` chỉ kiểm HÌNH DẠNG — **KHÔNG kiểm commit
    trong URL có THẬT không**. Nợ này có bằng chứng đã suýt trả giá: khi nâng năm biên nhận
    `phan-bien-quy-trinh-*` lên v2, phiên soạn chỉ có SHA VIẾT TẮT `482971b` cho một tệp và đã
    **bịa nốt 32 ký tự còn lại** để có một chuỗi 40 hex; nó lọt qua mọi phép kiểm hình dạng, chỉ
    lộ vì người viết tự đọc lại rồi chạy `git rev-parse`. Vì sao KHÔNG vá bằng cách gọi git:
    `actions/checkout` mặc định `depth: 1`, nên `git cat-file -e <sha>` sẽ ĐỎ GIẢ trên CI cho
    những SHA hoàn toàn hợp lệ — đúng bẫy "clone nông" mà `CLAUDE.md` đã ghi là mất 2,5 giờ.
    Chữa đúng cần `fetch-depth: 0` cho bước ấy; **chưa làm**, khai thành nợ
    `BIEN-NHAN-V2-KHONG-KIEM-SHA-CO-THAT`.

Phản chứng chạy được: `ops/bien_nhan_v2_test.py`.
"""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

RC_SACH = 0
RC_VI_PHAM = 1
RC_KHONG_DO_DUOC = 2

THU_MUC = "ops/reviews"

# --- Lược đồ v2 tối thiểu, chép theo `PROTOCOL §8` dòng 453-454 -------------------------
# "Đích v2 tối thiểu có `schema_version: 2`, receipt ID, `reviewed_sha`, verdict path/hash,
#  hai identity ở trên, evidence URL và khai loại/cường độ mỏ neo."
TRUONG_VO_HUONG = ("receipt_id", "reviewed_sha", "verdict_path", "verdict_sha256", "evidence_url")
# `github_submitter_identity` được phép là `null` — lược đồ ở dòng 430 ghi
# "<github actor or null when not published>". Nên đòi KHOÁ CÓ MẶT, không đòi giá trị.
TRUONG_CO_MAT = ("github_submitter_identity",)
TRUONG_ANH_XA = ("model_reviewer_identity", "anchor")
ANCHOR_KHOA = ("loai", "cuong_do")
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
    """Trả danh sách lý do tệp KHÔNG đạt v2. Rỗng = đạt."""
    loi = []
    if d.get("schema_version") != 2:
        loi.append(f"schema_version={d.get('schema_version')!r}, đòi 2")
    for k in TRUONG_VO_HUONG:
        v = d.get(k)
        if not isinstance(v, str) or not v.strip():
            loi.append(f"thiếu/rỗng `{k}`")
    for k in TRUONG_CO_MAT:
        if k not in d:
            loi.append(f"thiếu khoá `{k}` (được phép null, KHÔNG được phép vắng)")
    for k in TRUONG_ANH_XA:
        v = d.get(k)
        if not isinstance(v, dict) or not v:
            loi.append(f"thiếu/rỗng ánh xạ `{k}`")
    a = d.get("anchor")
    if isinstance(a, dict) and a:
        for k in ANCHOR_KHOA:
            if not str(a.get(k) or "").strip():
                loi.append(f"`anchor.{k}` thiếu/rỗng")
        loai = str(a.get("loai") or "").strip()
        if loai and loai not in ANCHOR_LOAI_CHO_PHEP:
            loi.append(f"`anchor.loai`={loai!r} ngoài danh sách CHO PHÉP "
                       f"{sorted(ANCHOR_LOAI_CHO_PHEP)}")
    return loi


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

    loi, dat, mien_tru, nod = [], 0, 0, 0
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
    return loi, {"tong": len(ds), "dat": dat, "mien_tru": mien_tru, "no": nod}


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
    print(f"\nbien_nhan_v2: {tk['dat']} ĐẠT v2 · {tk['mien_tru']}/{len(ALLOWLIST_CUTOVER)} miễn trừ "
          f"legacy (băm khớp) · {tk['no']} NỢ đóng băng · {len(loi)} vi phạm · tổng {tk['tong']}")
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
