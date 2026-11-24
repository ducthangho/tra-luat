#!/usr/bin/env python3
"""Cổng NGUỒN cho lời khai trong `ops/land/*-land-evidence.yaml` — packet #773, đặc tả đóng băng
`ops/specs/land-evidence-khai-phai-co-nguon-r1.md` (sha256 063ccaa6…).

VÌ SAO CÓ. Ba lượt Codex connector trên PR ghi sổ #771 bắt cùng MỘT lỗi — lời khai rộng hơn bằng chứng giữ lại (H1) —
mỗi lượt vá tay đúng câu được chỉ; không cổng nào đo lớp lỗi này (`bien_nhan_v2` chỉ đọc `ops/reviews/*.receipt.yaml`).

LUẬT:
  L1  Mỗi LỜI KHAI ĐO — chuỗi YAML (khoá hoặc giá trị, mọi độ sâu) mà sau khi bỏ khoảng trắng đầu bắt đầu bằng token
      `measured` theo sau là khoảng trắng, `—`, `-` hoặc `:` — phải chứa ≥ 1 TOKEN NGUỒN phân giải được tới đường dẫn
      CÓ THẬT, NẰM TRONG gốc kho. Token nguồn = một dải tối đa `[A-Za-z0-9_./{}*-]+` (bỏ dấu `.` cuối câu) kết thúc
      bằng `.json|.txt|.log|.yaml|.yml|.md|.sh|.py|.patch` hoặc bằng `/` (khi ấy phải là thư mục). Thứ tự phân giải:
      `<hồ sơ>-provenance/`, `ops/land/`, gốc kho. Có `*` ⇒ glob, phải khớp ≥ 1 mục đúng LOẠI. Chặt hơn chữ đặc tả (Q3):
      so `measured` không phân biệt hoa thường. CHÍNH hồ sơ đang kiểm, và thư mục CHỨA nó (`./`, `../`, `ops/land/`), KHÔNG là
      nguồn — lời khai không tự chứng minh (connector P1 #778). Hồ sơ KHÁC vẫn là nguồn được: lời khai đo VỀ nó là hợp lệ.
  L2  Mapping có khoá `positive` phải có `nguon_positive` (chuỗi/danh sách) cùng cấp; mỗi tệp phải có; mọi token `N/M`
      và `hong N` của `positive` phải có NGUYÊN VĂN (biên chữ số) trong ≥ 1 tệp ấy.
  L3  Có `pre_merge_checks` và provenance có `readback-pr-*.json` mang `merged_at` ⇒ mọi mốc ISO-8601 đầy đủ trong
      một phần tử `pre_merge_checks` phải `<` `merged_at`. Mốc nhận `Z`/`z`, độ lệch `±HH:MM`/`±HHMM`, `T`/`t`/dấu cách;
      thiếu múi giờ ⇒ coi là UTC như YAML 1.1 (connector P2 #778: `+00:00` từng lọt). Không có readback ⇒ "L3 không áp dụng".
  L4  Ba trạng thái: ĐẠT · ĐỎ · KHÔNG ĐO ĐƯỢC. YAML hỏng, provenance vắng khi có lời khai đo/`positive`, đọc tệp lỗi,
      readback hỏng, KHOÁ YAML TRÙNG (parser giữ giá trị cuối ⇒ lời khai trước biến mất), ngày sai, nhiều `merged_at`
      khác nhau, không thấy hồ sơ nào ⇒ KHÔNG ĐO ĐƯỢC, không bao giờ ĐẠT. Băm L5 và luật đo trên CÙNG một lần đọc.
  L5  `MIEN_TRU_CUTOVER` = {tên: sha256 byte} của MỌI hồ sơ trên `origin/master` lúc bắt đầu (`c73af7b`). Băm khớp ⇒
      bỏ qua có ghi nhận. Băm lệch ⇒ mất miễn trừ, kiểm đủ luật. Bản kỳ vọng CHÉP RIÊNG trong test: thêm tên ⇒ ĐỎ.
  L6  (#845, `ops/specs/land-evidence-landed-chua-dien-r1.md`) Chỉ khi `trang_thai_packet` là mapping CÓ khoá `landed`:
      `landed` không phải bool ⇒ ĐỎ. `landed: true` ⇒ `post_merge_checks` và `bookkeeping` phải là list KHÁC RỖNG mà mọi
      phần tử là mapping (kiểm KIỂU, không đoán chuỗi giữ chỗ — PR #840 merge suýt mang `landed: true` với hai trường ấy là
      chuỗi `CHO_DIEN`, connector P1 4309577154), và không chuỗi nào chứa `CHO_DIEN`. `landed: false` (bản nháp) ⇒ không đòi.
  L7  (#748, `ops/specs/land-evidence-l7-assurance-thuc-thi-r1.md`) `assurance_81.reviewer_assurance_81` chuẩn hoá (bỏ khoảng
      trắng hai đầu, viết hoa, khoảng trắng ⇒ `_`) bằng `DAT` ⇒ `assurance_81.thuc_thi` phải là mapping có `model`, `effort`,
      `sandbox_mode`, mỗi khoá là lời khai `measured` (cùng `RE_KHAI_DO`, nên L1 tự đòi nguồn). Chặt hơn chữ đặc tả: chuẩn hoá
      thêm NFC và nhận cả cách viết có dấu `ĐẠT` — chỉ đúng hai cách viết ấy, KHÔNG bỏ dấu đại trà (review l7a P2: `ĐẤT`, `DẠT`
      là giá trị khác, phải để L7 không áp). Giá trị khác ⇒ không đòi. Connector P1 PR #934 (4372912640): hồ sơ khai ĐẠT
      khi biên nhận chỉ đo model. `MIEN_TRU_L7` = 3 hồ sơ đã khai như thế (nợ `NO-L7-3-HO-SO-KHAI-DAT-THIEU-DO`), cơ chế như L5.
      r2 (`ops/specs/land-evidence-l7-r2-moi-do-sau.md`): `$.assurance_81` là mapping ⇒ nó là nguồn DUY NHẤT, mọi khoá
      `reviewer_assurance_81` lồng chuẩn hoá ra DAT chỉ thành ghi chú (hồ sơ chỉ thêm, câu DAT cũ còn nằm đó). Không có khối ấy
      ⇒ mỗi khoá lồng (mọi độ sâu, kể cả trong list) chuẩn hoá ra DAT là MỘT vi phạm; không nhận `thuc_thi` lồng. Giá trị
      không phải chuỗi ⇒ không áp, ghi chú. Lời khai văn xuôi (`§8.1 … cross_approved` trong chuỗi) KHÔNG đọc được, không bắt.
      #1240 (ADR-0065, `ops/specs/assurance-81-model-effort-tuy-chon-r1.md`) NỚI: chỉ `sandbox_mode` (`L7_KHOA`) còn bắt buộc
      là lời khai measured. `model`, `effort` (`L7_KHOA_TUY_CHON`) là trường ghi nếu đo được: được VẮNG; có mặt thì phải là
      chuỗi khớp `RE_KHAI_DO` hoặc `RE_KHAI_KHONG_DO` (`not_measured …`). Rỗng, `DAT`, null, sai kiểu ⇒ vẫn ĐỎ.
  L8  (#1236 đợt B, `ops/specs/wp1236-r12.md`) Chạy SAU chốt L5: hồ sơ được L5 miễn thì L8 không chạy. Mỗi vi phạm của
      `kiem_ho_so(dữ liệu ĐÃ NẠP, <hồ sơ>-provenance/)` trong `ops/gate_output_doi_chieu.py` CỦA GỐC ĐANG KIỂM (`--root`) là một
      vi phạm `L8 <đường dẫn>: <lý do>`: lời khai `gate_output` dương phải trích tệp `danh-gia-gate-output-<run>.txt` khớp
      provenance, hồ sơ landed phải có ≥ 1 lời khai hợp lệ (luật và giới hạn: docstring module ấy). Module không nạp được, ném,
      hay trả thứ không phải list ⇒ KHÔNG ĐO ĐƯỢC, không bao giờ ĐẠT. `MIEN_TRU_L8` = hồ sơ L8 cho ĐỎ trên base đợt B, cơ chế
      như L7 (chỉ miễn L8). Lời khai văn xuôi dưới khoá không chứa `gateoutput` KHÔNG được đọc (tiền lệ L7).

ĐIỀU CỔNG NÀY KHÔNG LÀM (đặc tả `ngoai_pham_vi`): L1 chỉ đo "lời khai trỏ tới thứ CÓ THẬT", KHÔNG đo thứ ấy chứng minh câu
văn — một tệp vô can vẫn làm L1 qua. Chỉ L2 đọc NỘI DUNG, và chỉ cho token số. Hồ sơ cũ đi qua miễn trừ, không được kiểm.
Không sửa hồ sơ nào. Lên CI GIÁN TIẾP: `ops/land_evidence_nguon_test.py` đăng ký trong `.claude/dev/ci_dang_ky_test.py`, ca `c11`
của nó gọi bộ kiểm này trên cây thật (bản trước ghi "chưa nằm trên đường CI" — cũ từ lease g2 #773, review #845 lượt 1 P3).

Dùng: python ops/land_evidence_nguon.py [--root GOC] [--tep TEP ...] — thoát 0 ĐẠT · 1 ĐỎ · 2 KHÔNG ĐO ĐƯỢC (không vi phạm).
"""
import argparse
import datetime
import glob
import hashlib
import importlib.util
import json
import re
import sys
import unicodedata
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="backslashreplace")

ROOT = Path(__file__).resolve().parents[1]
THU_MUC = "ops/land"
DUOI = "-land-evidence.yaml"

# L5 — đo 2026-10-16 trên `c73af7b`: mọi `ops/land/*-land-evidence.yaml`, sha256 trên byte blob. KHÔNG thêm tên mới.
MIEN_TRU_CUTOVER = {
    "plat-x8-land-evidence.yaml": "fe780adb6e9d897fa50011e0f91a0f1a995c72367280b6c9ab89a40485e6adaf",
    "pr468-hoso-4-packet-land-evidence.yaml": "6633416d86d4bcda1ac5cb9af30aa74a6c355ac6a2095901d91483d83ae19f40",
    "pr477-dung-goi-review-land-evidence.yaml": "3877dc4f2c611377cd80ce5cbe72645f26c6f10dec706a000d7e7da8e7f30bd5",
    "pr478-land-evidence.yaml": "c400cbdbbab9b92f3df2686dc94473cffcd5af9bc1d35953920cad69706d4657",
    "pr480-land-evidence.yaml": "e6d331048396712532f94d214fed0c9225e7fd733e5c5d7178eedace84d2450c",
    "pr487-land-evidence.yaml": "4b8fe2b5f713c20d2eefcb8ae8286ab8891c086a6cb3daf2206f09cc8d3560b8",
    "pr489-land-evidence.yaml": "ff4dad3ae70466c3bbe9ad6644f4d3989558d7839bf7902828caf42d58df99fb",
    "pr491-r358-ghi-so-land-evidence.yaml": "6a53de6f28322454ac084d8817799b9c5f54468aa4b47cf8820350dd805300dd",
    "pr493-land-evidence.yaml": "ea25588d524aba2b6b68f47887b18581adff4734345a2be46760703e9f5af391",
    "pr554-wp541-land-evidence.yaml": "07ea6c44b6245778c5dc34020352e75e8017835ff4c44e215715f4f80dea179c",
    "pr594-wp578-land-evidence.yaml": "858ce838bcaa705d370fa6767e2de36f7533098737d292cbf171e702c8184229",
    "pr621-skill-bai-hoc-land-evidence.yaml": "cb72c1daf84cebf02883f11cd43c7201eaedb3d454a51a90b8bd7359caaeaaa7",
    "pr666-wp650-land-evidence.yaml": "dea62efed34d55689752cfaea6ef2a5cc0b1af71e424be540c6bac82260173db",
    "pr672-wp574-land-evidence.yaml": "543ea45f2859144685ab5b35ad369dab9ccb103a39256a638ea1726c25dbb3ee",
    "pr679-wp678-land-evidence.yaml": "f409cacf8c5e3a6930072041ee8102db4327cb2558cdebd3263356057ef1b3be",
    "pr680-wp676-land-evidence.yaml": "964742fef636a70587b2247c094ac4f38aea540a01abdce8b6319c8f74b447bf",
    "pr684-wp677-land-evidence.yaml": "5b302984cefa5b245397d1facb77a06b9bfcac3cce38295d3f721abc32e7e220",
    "pr689-wp677-land-evidence.yaml": "f9bac5cbaeb8ac5bdf9f2d9b1375917e1d57c687ad6ed943c014a52996664559",
    "pr696-wp668-land-evidence.yaml": "aae2c2dc4ab1641400d8841ad40f11dac854131b80acdf407e52c9539b0afcb0",
    "pr701-wp687-land-evidence.yaml": "3e4004eefc05230aa3228bb88877eae7541d387a560b480c9b54f7aea2132a62",
    "pr703-wp674-land-evidence.yaml": "7266f6256651fe09d60382519d1d4c378c895ab15924e66fa055012d76f2cc18",
    "pr707-wp705-land-evidence.yaml": "d2425c2e4bf0ea930f9d1752ee20ee18a53a0e37315216af46986679141b99e8",
    "pr714-wp710-land-evidence.yaml": "906da0d8fb58ac01a25115dbafa6f4b98c57917c0931b23be0e41f38374f390a",
    "pr718-wp678-land-evidence.yaml": "1e181abab1432fade105b5ef3427d263ccb5f52217bc53c0251770f1a1ddb180",
    "pr721-wp698-land-evidence.yaml": "37bb04390e3cd65d6f489a8e390d8398eca9f1b6e7f565501f44af11a67641c6",
    "pr732-wp685-land-evidence.yaml": "41e806fe12064159e8f407ae81cc6eac1cb04c4bffd7dae6bb1b59c4d915e16a",
    "pr759-no-p3-ho-so-land-evidence.yaml": "574f6c3f13b4a36254fe0894539a66dc407c660ca4949ac80270bc9e442b7aa2",
    "pr765-wp743-land-evidence.yaml": "a468d5fea4dac206024e35567287006eb8b6befe9f1b96ad07f810e64c61c970",
}

RE_KHAI_DO = re.compile(r"\s*measured(?:\s|—|-|:)", re.IGNORECASE)
RE_KHAI_KHONG_DO = re.compile(r"\s*not_measured(?:\s|—|-|:)", flags=re.IGNORECASE)   # #1240: chỉ L7 tuỳ chọn đọc; L1 không đòi nguồn
_KT = r"A-Za-z0-9_./{}*-"
RE_DAI = re.compile(rf"(?<![{_KT}])[{_KT}]+")
RE_DUOI_NGUON = re.compile(r"\.(?:json|txt|log|yaml|yml|md|sh|py|patch)$")
RE_SO_POS = re.compile(r"(?<!\d)\d+/\d+(?!\d)|(?<![A-Za-z0-9_])hong \d+(?!\d)")
RE_MOC = re.compile(r"\d{4}-\d{2}-\d{2}[Tt ]\d{2}:\d{2}(?::\d{2}(?:\.\d+)?)?(?:[Zz]|[+-]\d{2}:?\d{2})?(?![\d:])")
L6_PHAN_HOAN_TAT = ("post_merge_checks", "bookkeeping")   # cây thật 19-10-2026: mọi hồ sơ landed true đã có cả hai
L6_DAU_GIU_CHO = "CHO_DIEN"
L7_KHOA = ("sandbox_mode",)   # #1240 ADR-0065: bắt buộc measured khi khai DAT
L7_KHOA_TUY_CHON = ("model", "effort")   # #1240 ADR-0065: ghi nếu đo được — vắng được, có mặt thì measured/not_measured
L7_MUC_DAT = ("DAT", "ĐẠT")   # sau `_chuan_hoa_81`; dạng NFC
# L7 — đo 2026-10-27 trên `7129f7d` (băm chụp lại sau #962/#966 sửa pr924, pr950; tên giữ nguyên như ở `f577ab5`):
# 3 hồ sơ khai DAT mà thiếu `thuc_thi`. KHÔNG thêm tên mới; chụp lại băm chỉ khi có comment chủ kho cho phép —
# tự chụp lại mỗi lần hồ sơ đổi là xoá đúng tín hiệu "băm lệch ⇒ mất miễn trừ".
MIEN_TRU_L7 = {
    "pr924-wp923-land-evidence.yaml": "f246000294972947543a1afb3d9122b43ea11f8e540c4927ebda8d7a202d8f5b",
    "pr931-wp835-land-evidence.yaml": "31c8ce908aa08631a58993b1e431d4653b01b23b87ed59926181f2df4df485da",
    "pr950-wp834-land-evidence.yaml": "b0ae6da9f1f919d1f6ae785ad6950b94dd37f99c0a2852d31d5aaee645a6a080",
}
# L8 — đo 2026-11-24 trên `f602325` (base đợt B): 56 hồ sơ L8 cho ĐỎ khi chưa miễn (174 = 25 miễn L5 + 56 ĐỎ + 43 ĐẠT + 50 không
# lời khai, không landed); cùng tập tên và byte với phép đo của đặc tả trên `8048551`. KHÔNG thêm tên mới, KHÔNG tự chụp lại băm.
MIEN_TRU_L8 = {
    "pr1023-wp1009-r4-land-evidence.yaml": "be6a19a854be2163322d216c1e1d8d725a20a55f97e795aa5428727f57b214f8",
    "pr1029-windows-local-r2-land-evidence.yaml": "f2cb15c6006f8cbbfb4b9445bd5e914bf54a9cbc26bf0454ef20d1dd7b7a9fa0",
    "pr1040-wp1021-land-evidence.yaml": "3526c8eec297f89e4c96c1c34d42f6e227dd2a005bad876160f925af87df9e58",
    "pr1042-pr1068-cloud-setup-p2-spec-land-evidence.yaml": "55c25b0cdcbf6eb1c30faff36fcd778345f58a57e1defc9d7d43d6bc76e0bc54",
    "pr1046-wp1030-r6-land-evidence.yaml": "6a4e8fc85abb568b71fc7fe83e143a50c638e7ac80ab906cd5e44127cf1ecd8c",
    "pr1048-claude-md-powershell-land-evidence.yaml": "a588e59f6f94dc1fab3637ac1361c7c99e49eca44d6eb819985e4d64ae1f5462",
    "pr1051-wp1006-t27-land-evidence.yaml": "8a39302482b8edad44a30ac80f7221658dc4686a68ecf3bdb1f6f6fc81f697c8",
    "pr1055-wp1052-land-evidence.yaml": "b3d0f73dc7ccd9fa9fea86912dcb1cd88edd036ac34c1279ba27c01155adc751",
    "pr1063-wp1038-r1-land-evidence.yaml": "072d584fb37b74ae2fcfaf11f83c8540a2cd9060fe4fc4c060d357b655ab4c69",
    "pr1064-windows-local-r3-land-evidence.yaml": "34000573791672b926ace93ac19c6848acbc877c315b1f332fc1b15c27924408",
    "pr1065-vm-cap-nhat-cong-cu-land-evidence.yaml": "1b0259db0719808c5c2afd46cde0e462bd80866c9c860bfe1311be9cc9431ecb",
    "pr1073-wp1039-r1-land-evidence.yaml": "7458eaa90cdcd3cb02eaebda8de7f2b3b798265dbfa03682b6386f89e861dd3b",
    "pr1080-wp1077-land-evidence.yaml": "66901a2781d2976c65c8242b9488767bf55e324fd21e20cf6febacd084a89b32",
    "pr1095-pr1101-cloud-setup-p3-p3b-spec-land-evidence.yaml": "b49d10f34a579e098a740ce88857382250e622c8321b3217304d392568a4f681",
    "pr1097-wp1078-land-evidence.yaml": "7faaf52e686d5e88f137ef606257a9c59621b48cc8623f2d75c3c990a9e4d649",
    "pr1100-wp1089-r2-land-evidence.yaml": "e9abffb678cbe96b45cb10a7dfc0bcf69327fa972d0ed78747403db94e957e47",
    "pr1115-wp1079-land-evidence.yaml": "fcb4f136997a75716f5197302f97999247285325b3cf93014059593f6a28752c",
    "pr1118-ghi-so-bo-sung-1065-land-evidence.yaml": "6f0fd219c02813ae278df250b9f3ae351c861fcfccc8976c12923055246ad476",
    "pr1127-wp1120-land-evidence.yaml": "c36037061e11f29423a950b69428673fd1f87d01bf3ac2909b224b8302f7ca6c",
    "pr1128-wp1113-land-evidence.yaml": "7ececaadbe05de1036814b0308ba106508e61d4ae91d3a0ea725525e3f16b15b",
    "pr1130-wp1122-land-evidence.yaml": "4e06624080b12659c554e506451c327f746d0ff2b21e964fca8d64531d19acdf",
    "pr1137-wp1134-land-evidence.yaml": "55597684a48fdb506938a2590ef299209834a677467e1faf9d0d202e84fb0da3",
    "pr1141-wp1132-land-evidence.yaml": "5f049978fbcc5e05642d75f400db50bd7ace59ddaadd792e63fa93727be91f85",
    "pr1155-wp1143-land-evidence.yaml": "be22b4655d42d11265f2298c39dbdfef6c5d955ede1366f39fa81e1a70a9e7d5",
    "pr1192-wp1147-land-evidence.yaml": "432343e2ef39c9a6cece8b748029e303f4486bd38319cc8e0894411ad9b511a8",
    "pr1193-wp1189-land-evidence.yaml": "90808ecc1552f35bf22030f5ce10fcd9d2a40c46fcbd050c7f968eae1b9da698",
    "pr1197-wp1099-land-evidence.yaml": "65d161b8b326c93b09f7bcee836c71afad6284353383c3de6a7f3af6ef7482ce",
    "pr1340-wp1315-land-evidence.yaml": "4ad7a3b6cc2e6c402a0038f47048b5afd616b685e21b9734688fec42f84981b5",
    "pr1344-wp1343-land-evidence.yaml": "4307a59ec7e39a3cd424d639f93f378c7bcb579c6de23ba423d186c5377efa15",
    "pr1347-wp1345-land-evidence.yaml": "d38da3b69f8db30c7ee5f8afb32bd0786de6fc5980d855a4c38b878e5e40fc58",
    "pr1352-wp1350-land-evidence.yaml": "3f87c56642f76ffad40cd106b52df90205814b45f3bbf433e77d73a4a89bb922",
    "pr1392-wp1389-land-evidence.yaml": "eeb7a942279b3c45147fa44f6e9e053d420f6159f2c92b304f24c7444b8b4c2c",
    "pr1394-wp433-land-evidence.yaml": "c42246505396d0e1a1fa39e9a1320663e4539f981f74bc6d4d2c1c8990e2f0fb",
    "pr1406-wp1404-land-evidence.yaml": "51bd90f4c7bd63a418c8828b8b11f2512a21ffa1d62a6e917871f9bf4e8076e3",
    "pr1415-wp433-land-evidence.yaml": "49e60d048fbaae3d8e7ece058fa248cb1a4b9e3ad1714efc0af168e0e7c3a389",
    "pr1421-wp433-land-evidence.yaml": "24dc762fc65cbd175b7f10306941959531baad3d03d53faee79c1663fc90f22e",
    "pr1425-wp433-land-evidence.yaml": "c0a8ff8ac82b06680ba452fa298623b0658711f8fed83455172a1d1797b6aaad",
    "pr1431-wp433-land-evidence.yaml": "23bbaf40f3d57a7e1605ed588b87d3ba0d6bbce2637934c9597058d672b9916c",
    "pr1441-wp433-land-evidence.yaml": "b0ebd7cd0d3bab37f0ee5ab66d27231a32c94b2a1d38548624847e0dec55f624",
    "pr1453-wp433-land-evidence.yaml": "39cbe4e7b873f125f335d84d31929fae9e596fb94099d8ef9445326f44eee7c0",
    "pr631-doctrine-rest-land-evidence.yaml": "24888a097f35c247c1454cb012bc8ff2c1a34f542e05dbc29136fd4f119e2c85",
    "pr679-wp678-land-evidence.yaml": "e187218be88849b78b26bb12d1a1b53f4aac8c2eefd7cd636c21d61fdb916c67",
    "pr778-wp773-land-evidence.yaml": "4cee82ae07a401b668318a496d9dd7893c79b34ad93511ef37c8108316f0ac1a",
    "pr791-wp782-land-evidence.yaml": "a5de49cbe980b376c62097ac72da28f2f443a8e871e00d418702d4c1bd5cc863",
    "pr793-wp784-land-evidence.yaml": "97dd66d0b47d7eb19dc4d42bb18939f5bef645b6c279ce53aff730462181aff9",
    "pr864-wp858-land-evidence.yaml": "28b9e354a7400770c9a15fed7c9dfcd4a4292bdbf15c918506fd9f49c46a2fa8",
    "pr870-claude-md-bai-hoc-c-land-evidence.yaml": "91f46fb32d8fbc66481206c7fb7c3be64088926394d82c8ef8772f1c8186aa9b",
    "pr881-wp852-land-evidence.yaml": "43764b48699f47c6c79e0e870c4419d659e40bd5fa375479f038489b007c77df",
    "pr889-claude-md-bai-hoc-c-land-evidence.yaml": "07d9fab52fdda088e37a3106b11440ea17b4a40e90617322b0d8252bebaf134a",
    "pr896-claude-md-bai-hoc-c-tro-nguon-land-evidence.yaml": "fbb4b34d4ed74ceee3facc7c47a3438ffaa0775d19da2b87e328e0203b9489fc",
    "pr924-wp923-land-evidence.yaml": "3857723bc79f9f7b6ac45e3c3a3619ed2514186d6f2eeab2fcafdf302515502f",
    "pr931-wp835-land-evidence.yaml": "2b8ed5d20ee89c535a4fbf59a2281f146978d05b18a54a0d3702f9737e15569c",
    "pr945-wp899-land-evidence.yaml": "7be4cac3e343d586dc861b4280b517a797139ead2cab1a6356f1b1cdb9275976",
    "pr950-wp834-land-evidence.yaml": "56cdd2456608633c1f1a2ec407723dcf549a660dca36c4ce90b129e631cb5482",
    "pr963-wp943-land-evidence.yaml": "81395ff671200dcdcff2e0aa570be534559ede6ce02555f3da517426df428212",
    "pr997-wp978-land-evidence.yaml": "1c9a724d993e7424feae93f9281749495e3c81a8334832e8e5b9caa80230a65a",
}


class KhongDoDuoc(Exception):
    """Đầu vào không đo được (L4). Không bao giờ quy thành ĐẠT."""


def token_nguon(chuoi):
    """Mọi token nguồn (Q3) trong một chuỗi, theo thứ tự xuất hiện."""
    ung = (m.group(0).rstrip(".") for m in RE_DAI.finditer(chuoi))
    return [t for t in ung if t and (t.endswith("/") or RE_DUOI_NGUON.search(t))]


def _trong_goc(p, goc):
    try:
        p.resolve().relative_to(goc.resolve())
        return True
    except (ValueError, OSError):
        return False


def _la_nguon(p, token, goc, tep):
    if not ((p.is_dir() if token.endswith("/") else p.is_file()) and _trong_goc(p, goc)):
        return False
    r = p.resolve()
    return r != tep.resolve() and not (r.is_dir() and _trong_goc(tep, r))


def phan_giai(token, goc, prov, tep):
    """Đường dẫn NGUỒN hợp lệ cho token (`_la_nguon`), hoặc None. Thứ tự: provenance, ops/land, gốc."""
    for nen in (prov, goc / THU_MUC, goc):
        if "*" in token:
            khop = [Path(x) for x in sorted(glob.glob(glob.escape(str(nen)) + "/" + token))]
            khop = [x for x in khop if _la_nguon(x, token, goc, tep)]
            if khop:
                return khop[0]
            continue
        p = nen / token
        if _la_nguon(p, token, goc, tep):
            return p
    return None


def duyet(nut, duong="$"):
    """(đường dẫn YAML, nút) cho MỌI nút — dict, list, lá; khoá cũng được trả như một lá `<khoa>`. Kiểu khác mà SafeLoader
    dựng được (`!!set` ⇒ set, `!!omap`/`!!pairs` ⇒ tuple, `!!binary` ⇒ bytes) ⇒ KhongDoDuoc: L2/L3 chỉ hiểu dict, nên
    đi xuống chúng cho L1 vẫn để hai luật kia mù — từ chối là đóng cả ba luật một chỗ (review lượt 2 F05)."""
    if isinstance(nut, (set, frozenset, tuple, bytes, bytearray)):
        raise KhongDoDuoc(f"{duong}: kiểu YAML {type(nut).__name__} ngoài mô hình dict/list/vô hướng")
    yield duong, nut
    con = nut.items() if isinstance(nut, dict) else enumerate(nut) if isinstance(nut, list) else ()
    for k, v in con:
        d = f"{duong}.{k}" if isinstance(nut, dict) else f"{duong}[{k}]"
        if isinstance(nut, dict):
            yield d + "<khoa>", k
        yield from duyet(v, d)


def _thoi_diem(x):
    if isinstance(x, datetime.datetime):
        return x if x.tzinfo else x.replace(tzinfo=datetime.timezone.utc)
    try:
        t = datetime.datetime.fromisoformat(x.upper().replace("Z", "+00:00"))
        return t if t.tzinfo else t.replace(tzinfo=datetime.timezone.utc)
    except ValueError as e:   # regex chỉ kiểm HÌNH (2026-99-16 lọt) — ngày sai là đầu vào không đo được, không phải ĐỎ
        raise KhongDoDuoc(f"mốc {x!r} sai: {e}")


def merged_at(prov, goc_ten):
    """merged_at của PR mà hồ sơ ghi sổ. Hồ sơ tên `pr<N>-…` ⇒ CHỈ `readback-pr-<N>.json` (thư mục còn chứa readback PR lân
    cận và `-commits`, đo 16-10-2026). Tên khác ⇒ mọi `readback-pr-<số>.json` có `merged_at` khác null phải cùng một giá
    trị. None nếu không có readback áp dụng; KhongDoDuoc nếu hỏng, `merged_at` sai dạng, hoặc mâu thuẫn."""
    so = re.match(r"pr(\d+)-", goc_ten)
    tep = [] if not prov.is_dir() else [prov / f"readback-pr-{so.group(1)}.json"] if so else sorted(
        t for t in prov.glob("readback-pr-*.json") if re.fullmatch(r"readback-pr-\d+\.json", t.name))
    gia_tri = set()
    for t in tep:
        try:
            d = json.loads(t.read_text(encoding="utf-8")) if t.exists() else {}
        except (OSError, ValueError) as e:
            raise KhongDoDuoc(f"{t.name}: {type(e).__name__}: {e}")
        if (v := d.get("merged_at") if isinstance(d, dict) else None) is None and (not so or not t.exists()):
            continue
        if not isinstance(v, str) or not RE_MOC.fullmatch(v):
            raise KhongDoDuoc(f"{t.name}: không có merged_at ISO-8601 (được {v!r})")
        gia_tri.add(_thoi_diem(v))
    if len(gia_tri) > 1:
        raise KhongDoDuoc(f"readback-pr-*.json cho {len(gia_tri)} merged_at khác nhau")
    return gia_tri.pop() if gia_tri else None


def nap_yaml(yaml, byte):
    """`safe_load` có chốt, MỘT lần parse. Ở tầng NÚT, trước khi dựng, từ chối thứ làm dữ liệu dựng ra khác văn bản đọc được:
    khoá merge `<<` (làm phẳng đi vòng kiểm trùng — review lượt 3) và anchor/alias (nút dùng lại: vòng, nổ kích thước).
    Không hồ sơ nào trên master dùng chúng (đo 16-10-2026). Còn lại, khoá TRÙNG trong một mapping ⇒ lỗi (kể cả `null`)."""
    class Nap(yaml.SafeLoader):
        pass

    def map_khong_trung(nap, nut, deep=False):
        da = set()
        for k, _ in nut.value:
            khoa = nap.construct_object(k, deep=True)
            try:
                if khoa in da:
                    raise yaml.constructor.ConstructorError(None, None, f"khoá trùng {khoa!r}", k.start_mark)
                da.add(khoa)
            except TypeError:
                pass
        return yaml.SafeLoader.construct_mapping(nap, nut, deep)
    Nap.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, map_khong_trung)
    nap = Nap(byte)
    try:
        goc = nap.get_single_node()
        da, ngan = set(), [goc] if goc is not None else []
        while ngan:
            n = ngan.pop()
            if id(n) in da:
                raise yaml.YAMLError("anchor/alias (nút dùng lại) ngoài mô hình")
            da.add(id(n))
            if isinstance(n, yaml.MappingNode) and any(k.tag == "tag:yaml.org,2002:merge" for k, _ in n.value):
                raise yaml.YAMLError("khoá merge `<<` ngoài mô hình")
            ngan += [x for kv in n.value for x in kv] if isinstance(n, yaml.MappingNode) else \
                n.value if isinstance(n, yaml.SequenceNode) else []
        return nap.construct_document(goc) if goc is not None else None
    finally:
        nap.dispose()


def kiem_ho_so(tep, byte, goc, yaml):
    """(vi_pham, ghi_chu) trên `byte` — CHÍNH bản đã băm cho L5, không đọc tệp lần hai. Ném KhongDoDuoc cho L4."""
    try:
        du_lieu = nap_yaml(yaml, byte)
    except (yaml.YAMLError, ValueError, TypeError, OverflowError, RecursionError) as e:   # ngày sai không nháy: ValueError
        raise KhongDoDuoc(f"parse YAML: {type(e).__name__}: {str(e).splitlines()[0] if str(e) else ''}")
    goc_ten = tep.name[: -len(DUOI)] if tep.name.endswith(DUOI) else tep.stem
    prov = tep.parent / f"{goc_ten}-provenance"
    nut = list(duyet(du_lieu))   # độ sâu: loader ném RecursionError (~500 tầng) TRƯỚC bộ duyệt — đo 16-10-2026
    khai = [(d, v) for d, v in nut if isinstance(v, str) and RE_KHAI_DO.match(v)]
    maps = [(d, v) for d, v in nut if isinstance(v, dict)]
    co_pos = any("positive" in m for _, m in maps)
    if (khai or co_pos) and not prov.is_dir():
        raise KhongDoDuoc(f"thiếu thư mục provenance {prov.name}/ trong khi có {len(khai)} lời khai đo"
                          f"{' và khoá positive' if co_pos else ''}")
    vp, ghi = [], []
    for d, v in khai:   # L1
        tk = token_nguon(v)
        if not any(phan_giai(t, goc, prov, tep) for t in tk):
            vp.append(f"L1 {d}: lời khai đo không có token nguồn phân giải được"
                      f" (token: {', '.join(tk) if tk else 'không có'}) — {v.strip()[:90]!r}")
    for d, m in maps:   # L2
        if "positive" not in m:
            continue
        ng = m.get("nguon_positive")
        ds = [ng] if isinstance(ng, str) else ng if isinstance(ng, list) else None
        if not ds or not all(isinstance(x, str) and x for x in ds):
            vp.append(f"L2 {d}: có positive mà thiếu nguon_positive (chuỗi/danh sách)")
            continue
        tep_ng = [(x, phan_giai(x, goc, prov, tep)) for x in ds]
        vp += [f"L2 {d}: nguon_positive {x!r} không có tệp" for x, p in tep_ng if p is None or not p.is_file()]
        if any(p is None or not p.is_file() for _, p in tep_ng):
            continue
        try:
            noi_dung = [p.read_bytes().decode("utf-8", "replace") for _, p in tep_ng]
        except OSError as e:
            raise KhongDoDuoc(f"đọc nguon_positive: {e}")
        for so in RE_SO_POS.findall(str(m["positive"])):
            mau = re.compile(r"(?<![A-Za-z0-9_])" + re.escape(so) + r"(?!\d)" if so.startswith("hong")
                             else r"(?<![\d/])" + re.escape(so) + r"(?![\d/])")
            if not any(mau.search(nd) for nd in noi_dung):
                vp.append(f"L2 {d}: positive khai {so!r} mà không tệp nguon_positive nào chứa nguyên văn")
    pmc = du_lieu.get("pre_merge_checks") if isinstance(du_lieu, dict) else None
    if pmc is not None:   # L3
        moc_merge = merged_at(prov, goc_ten)
        if moc_merge is None:
            ghi.append("L3 không áp dụng: provenance không có readback PR mang merged_at")
        else:
            phan_tu = pmc if isinstance(pmc, list) else [{k: v} for k, v in pmc.items()] if isinstance(pmc, dict) else [pmc]
            for i, pt in enumerate(phan_tu):
                for d, v in duyet(pt, f"$.pre_merge_checks[{i}]"):
                    moc = [v] if isinstance(v, datetime.datetime) else RE_MOC.findall(v) if isinstance(v, str) else []
                    for x in moc:
                        if _thoi_diem(x) >= moc_merge:
                            vp.append(f"L3 {d}: mốc {x} không trước merged_at {moc_merge:%Y-%m-%dT%H:%M:%SZ}")
    tt = du_lieu.get("trang_thai_packet") if isinstance(du_lieu, dict) else None
    if isinstance(tt, dict) and "landed" in tt:   # L6
        if not isinstance(tt["landed"], bool):
            vp.append(f"L6 $.trang_thai_packet.landed: phải là bool, được {tt['landed']!r}")
        elif tt["landed"]:
            for khoa in L6_PHAN_HOAN_TAT:
                ds = du_lieu.get(khoa)
                if not (isinstance(ds, list) and ds and all(isinstance(x, dict) for x in ds)):
                    vp.append(f"L6 $.{khoa}: landed true mà không phải danh sách mapping khác rỗng — {str(ds)[:60]!r}")
            vp += [f"L6 {d}: landed true mà còn dấu giữ chỗ {L6_DAU_GIU_CHO} — {v[:60]!r}"
                   for d, v in nut if isinstance(v, str) and L6_DAU_GIU_CHO in v]
    a81 = du_lieu.get("assurance_81") if isinstance(du_lieu, dict) else None
    if isinstance(a81, dict) and _chuan_hoa_81(a81.get("reviewer_assurance_81")) in L7_MUC_DAT:   # L7
        bam, tt7 = MIEN_TRU_L7.get(tep.name), a81.get("thuc_thi")
        mien = bam is not None and hashlib.sha256(byte).hexdigest() == bam
        if bam is not None:
            ghi.append("L7 miễn trừ (băm khớp ảnh chụp, nợ NO-L7-3-HO-SO-KHAI-DAT-THIEU-DO)" if mien
                       else "L7 mất miễn trừ: băm lệch ảnh chụp — kiểm đủ")
        if not mien and not isinstance(tt7, dict):
            vp.append(f"L7 $.assurance_81.thuc_thi: khai DAT mà không có mapping đo thực thi — {str(tt7)[:60]!r}")
        elif not mien:
            vp += [f"L7 $.assurance_81.thuc_thi.{k}: khai DAT mà không phải lời khai measured — {str(tt7.get(k))[:60]!r}"
                   for k in L7_KHOA if not (isinstance(tt7.get(k), str) and RE_KHAI_DO.match(tt7[k]))]
            vp += [f"L7 $.assurance_81.thuc_thi.{k}: có mặt mà không phải lời khai measured/not_measured — {str(tt7[k])[:60]!r}"
                   for k in L7_KHOA_TUY_CHON if k in tt7 and not _khai_tuy_chon(tt7[k])]
    co_goc = isinstance(a81, dict)   # L7 r2: có khối cấp gốc ⇒ khối ấy là nguồn DUY NHẤT, khoá lồng chỉ được ghi chú
    for d, v in _khoa_81(du_lieu):
        if d == "$.assurance_81.reviewer_assurance_81":   # chính khối gốc, r1 đã xét
            continue
        if not isinstance(v, str):
            ghi.append(f"L7 {d}: giá trị {type(v).__name__} không phải chuỗi — L7 không áp")
        elif _chuan_hoa_81(v) not in L7_MUC_DAT:
            continue
        elif co_goc:
            ghi.append(f"L7 {d}: khai DAT lồng bị bỏ qua — khối $.assurance_81 cấp gốc là nguồn duy nhất")
        else:
            vp.append(f"L7 {d}: khai DAT mà không có khối $.assurance_81 cấp gốc có thuc_thi")
    vp8, ghi8 = l8(tep, byte, du_lieu, prov, goc)
    return vp + vp8, ghi + ghi8


def l8(tep, byte, du_lieu, prov, goc):
    """(vi_pham, ghi_chu) của L8 trên dữ liệu ĐÃ NẠP từ `byte`. Module đối chiếu lấy từ `goc` (gốc đang kiểm), không từ thư mục
    của tệp này, và phải nạp được TRƯỚC khi xét miễn trừ (hồ sơ được miễn cũng không ĐẠT trên gốc thiếu module). Miễn trừ gắn
    TÊN + băm của chính `byte`. Ném KhongDoDuoc khi module không nạp được, ném (kể cả SystemExit), hay trả thứ không phải list."""
    nguon = goc / "ops/gate_output_doi_chieu.py"
    try:
        mod = importlib.util.module_from_spec(importlib.util.spec_from_file_location(nguon.stem, nguon))
        exec(compile(nguon.read_bytes(), str(nguon), "exec"), mod.__dict__)   # không qua .pyc: không đọc bản cũ, không ghi vào gốc
        if MIEN_TRU_L8.get(tep.name) == hashlib.sha256(byte).hexdigest():
            return [], ["L8 miễn trừ (băm khớp ảnh chụp base đợt B)"]
        kq = mod.kiem_ho_so(du_lieu, prov)
        if not isinstance(kq, list):
            raise TypeError(f"kiem_ho_so trả {type(kq).__name__}")
    except (Exception, SystemExit) as e:   # module gọi sys.exit(0) lúc nạp không được biến thành mã thoát 0
        raise KhongDoDuoc(f"L8 không nạp/chạy được {nguon.name}: {type(e).__name__}: {e}")
    return [f"L8 {x}" for x in kq], ["L8 mất miễn trừ: băm lệch ảnh chụp — kiểm đủ"] if tep.name in MIEN_TRU_L8 else []


def _khoa_81(nut, duong="$"):
    """(đường dẫn JSON, giá trị) của MỌI khoá `reviewer_assurance_81`, mọi độ sâu, kể cả trong phần tử list (L7 r2)."""
    if isinstance(nut, dict):
        for k, v in nut.items():
            d = duong + _doan(k)
            if k == "reviewer_assurance_81":
                yield d, v
            yield from _khoa_81(v, d)   # độ sâu
    elif isinstance(nut, list):
        for i, v in enumerate(nut):
            yield from _khoa_81(v, f"{duong}[{i}]")   # list


def _doan(k):
    """Đoạn đường dẫn KHÔNG nhập nhằng (review l7r2 lượt 1 P2): `.k` chỉ cho tên ASCII đơn giản; chuỗi khác ⇒ `["…"]`
    (khoá `a.b` ≠ nhánh a → b); khoá không phải chuỗi ⇒ `[kiểu:repr]` (khoá int 1 ≠ phần tử list `[1]`)."""
    if not isinstance(k, str):
        return f"[{type(k).__name__}:{k!r}]"
    return f".{k}" if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", k) else f"[{json.dumps(k, ensure_ascii=False)}]"


def _khai_tuy_chon(v):
    """#1240: trường L7 tuỳ chọn có mặt ⇒ chuỗi `measured …` hoặc `not_measured …`; mọi giá trị khác là rác."""
    return isinstance(v, str) and bool(RE_KHAI_DO.match(v) or RE_KHAI_KHONG_DO.match(v))


def _chuan_hoa_81(v):
    """`' đạt '` (NFC hay NFD) ⇒ `ĐẠT`, `'chua dat'` ⇒ `CHUA_DAT`; không phải chuỗi ⇒ None (L7 không áp)."""
    if not isinstance(v, str):
        return None
    return re.sub(r"\s+", "_", unicodedata.normalize("NFC", v).strip().upper())


def main(argv=None):
    ap = argparse.ArgumentParser(description="Cổng nguồn cho lời khai trong ops/land/*-land-evidence.yaml (#773).")
    ap.add_argument("--root", default=str(ROOT))
    ap.add_argument("--tep", nargs="+", default=None, help="chỉ kiểm các tệp này (tương đối với --root hoặc tuyệt đối)")
    a = ap.parse_args(argv)
    goc = Path(a.root).resolve()   # MỘT hệ quy chiếu: `--root .` + `--tep /tuyệt/đối` từng ném ValueError (review lượt 4 F06)
    try:
        import yaml
    except ImportError as e:
        print(f"KHÔNG ĐO ĐƯỢC: thiếu PyYAML ({e})\nTỔNG: KHÔNG ĐO ĐƯỢC")
        return 2
    teps = [goc / t for t in a.tep] if a.tep else sorted((goc / THU_MUC).glob("*" + DUOI))
    n = m = k = v = u = 0
    for tep in teps:
        nhan = tep.resolve().relative_to(goc).as_posix() if _trong_goc(tep, goc) else str(tep)
        try:
            byte = tep.read_bytes()
        except OSError as e:
            u += 1
            print(f"KHÔNG ĐO ĐƯỢC {nhan}: {type(e).__name__}: {e}")
            continue
        if (bam := MIEN_TRU_CUTOVER.get(tep.name)) is not None:
            k += 1
            if hashlib.sha256(byte).hexdigest() == bam:
                m += 1
                print(f"MIỄN TRỪ {nhan} (băm khớp ảnh chụp cutover)")
                continue
            print(f"MẤT MIỄN TRỪ {nhan}: băm lệch ảnh chụp cutover — kiểm đủ luật")
        try:
            vp, ghi = kiem_ho_so(tep, byte, goc, yaml)
        except KhongDoDuoc as e:
            u += 1
            print(f"KHÔNG ĐO ĐƯỢC {nhan}: {e}")
            continue
        for g in ghi:
            print(f"  ghi chú {nhan}: {g}")
        v, n = v + len(vp), n + (not vp)
        print(f"ĐỎ {nhan}: {len(vp)} vi phạm" + "".join(f"\n  {x}" for x in vp) if vp else f"ĐẠT {nhan}")
    if not teps:
        u += 1
        print(f"KHÔNG ĐO ĐƯỢC: không thấy hồ sơ *{DUOI} nào dưới {goc / THU_MUC}")
    print(f"land_evidence_nguon: {n} ĐẠT · {m}/{k} miễn trừ (băm khớp) · {v} vi phạm · {u} KHÔNG ĐO ĐƯỢC · tổng {len(teps)}")
    rc = 1 if v else 2 if u else 0
    print("TỔNG: " + ("ĐẠT", "ĐỎ", "KHÔNG ĐO ĐƯỢC")[rc])
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
