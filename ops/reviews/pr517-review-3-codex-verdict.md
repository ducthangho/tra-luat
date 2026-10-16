verdict: approve
reviewed_sha: da04323199331bf9de1d05f3feb233db9afb57f8
reviewed_base: 157b36868e13e24fd0c0a468c22941627d2cd0fe
reviewed_files_sha256:
  CHANGELOG.md: 559bf81a04e470095b6cf5cd588123a95bfa0cdfa45dd1f314548307f5d2c11d
  RELEASE_MANIFEST.json: 1f59c87b5050a4e6ac3b45f407c0d95c64acf43ad00da3e33cfb8712b2446de3
  ops/reviews/README.md: 39234d4b6fdf6997b662b0a06e641941096af6f2e22cfc2a0f168053ff2ad27d
  ops/reviews/pr516-review-1-codex-verdict.md: 1a1235739ebf920811570f3a05b3799f8743aa8e7618b7f9099e001d4e8dc1f0
  ops/reviews/pr516-review-1-codex-verdict.receipt.yaml: 55cee89efeebed23acbf51a205692ca6c70c2bd8f63b4a4b185cdb54b8fdc9c7
  ops/reviews/pr516-review-2-codex-verdict.md: e2d0fc65a809cb7e2be27804f518d41a09a8329b672ae8ebfa438603cb0202fe
  ops/reviews/pr516-review-2-codex-verdict.receipt.yaml: 84273ab3e1c984e7e859b5753c967376c386ec613f704049789ce78eb68b499a
  ops/reviews/pr516-review-3-codex-verdict.md: 532e022c16f75ba5780de45e4e4056788f58ac275d6638a1fbb5c55088cda968
  ops/reviews/pr516-review-3-codex-verdict.receipt.yaml: 8cf325bdb2bf434fe4debfbdd3b363eb743a04d2bed2e3274fb62836393a441b
  ops/reviews/pr516-review-4-codex-verdict.md: 4d227acbc81641f2a25d68870ecf3dbb047a9df390b4382afd853e9452496ca4
  ops/reviews/pr516-review-4-codex-verdict.receipt.yaml: 0722c7ed458ea9e0dd673d037d6b297878d094e05ed74e18389b929daad6af42
  ops/reviews/pr516-review-5-codex-verdict.md: d66f58020aa0330c44597fe87635c9f70eb60d49e5db444cd09da7b24a82a38b
  ops/reviews/pr516-review-5-codex-verdict.receipt.yaml: 6e60586fdcdf10e7dee471ebc9643d1f67060e52cde3d0021566f37641766060
model_tu_khai: GPT-6 / Codex (tự khai theo ngữ cảnh phiên; khác nền tác giả Claude; không attestation độc lập backend)
review_round: 3
so_p1: 0
so_p2: 0
so_p3: 0
so_the_hien: 0
hint_sha256: dcd44ce677bcae779eeb39a03d00836532c701573bb05b766cfac05e7c2852a6
previous_hint_sha256: f7de8c044f84fd89da8ed45e5dfa6c07887d787f195c28c3d4a70d9fdb9bfc62

**approve — 0 lớp P1 / 0 lớp P2 / 0 lớp P3; 0 thể hiện lỗi còn mở.**

lớp tong-hop-doi-tap-doi-tuong ĐÃ VÁ THẬT; merge master không đổi hồ sơ; cổng như lượt 2.

Phạm vi đúng HEAD/base ở đầu tệp, diff `git -C cay-kho diff origin/master...HEAD`: **13 tệp, +1733/−5**. HEAD và `origin/master` đã tự xác nhận; merge-base bằng base được giao. Các băm trên là SHA-256 byte tệp tại HEAD, đối chiếu worktree và kiểm lại cuối lượt. `VERDICT.md` sơ bộ đã được ghi trước khi đo; đây là bản chốt.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn `nguon/VERDICT.rvhs517-2.md` có SHA-256 `49516ae20097b5b66008583a6f96730568598b1cacdf33eb272c79273173728f`; HINT nguồn khớp `previous_hint_sha256`. Phân loại theo lớp, xét đúng thể hiện còn mở của lượt 2:

| Lớp / thể hiện | Trạng thái lượt 2 | Trạng thái lượt 3 | Bằng chứng mới |
|---|---|---|---|
| `tong-hop-doi-tap-doi-tuong` · `CHANGELOG.md:32` | VÁ SINH LỖI MỚI, 1 thể hiện P2 do chính HINT lượt 1 | **ĐÃ VÁ THẬT** | Chuỗi HEAD `r363→r366→r367→r369` bằng bốn heading tại `reviewed_sha`; replay nguyên HINT lượt 2 trên `8a18429` cho CHANGELOG bằng byte HEAD. Đảo lại `r364` làm phép đối chiếu đỏ. |

Các lớp đã đóng (`nguon-thuat-lai-bi-nang-thanh-do`, `template-khong-khoa-theo-luot`, `dem-dong-cong-them-duoi-lf`) và năm thể hiện đã đóng khác của lớp tập đối tượng: **như lượt 2, không đo lại** về nội dung. Phép so byte lần này xác nhận không có thay đổi ở những câu ấy; CHANGELOG chỉ đổi đúng token tại dòng 32. Không nhận các bảng đo/mutant lượt trước là phép chạy mới.

Đã lấy `reviewed_sha` từ từng verdict nguồn, chạy `git -C cay-kho show <reviewed_sha>:CHANGELOG.md | head -1`; lưu nguyên dòng đầu trong `scratch/luot1/logs/pr{500,510,511,516}-heading.stdout` và `semantics-head.json`:

| PR được verdict chấm | Tệp nguồn | reviewed_sha | Mốc ở dòng đầu CHANGELOG |
|---|---|---|---|
| #500 | `ops/reviews/pr500-review-1-codex-verdict.md` | `5a29d358649c9d70632cd2aa2e5cb8ac53884dc8` | **r363** |
| #510 | `ops/reviews/pr510-review-1-codex-verdict.md` | `3349c8b2e2b544ce98c2ea088e6c09d71b1092f0` | **r366** |
| #511 | `ops/reviews/pr511-review-1-codex-verdict.md` | `51466e6e468f0b92997baadb1f64dfa55a926859` | **r367** |
| #516 | `ops/reviews/pr516-review-1-codex-verdict.md` | `899f305997544dc78947af6dd58aa490ed3538f3` | **r369** |

`r363` là mốc của đối tượng được review ở #500; `r364` là mục ghi sổ về sau. Token sửa lần này giữ đúng quan hệ verdict → reviewed_sha → heading r. Không phát hiện câu sửa sai đối tượng hoặc lỗi mới trong phạm vi thay đổi.

## Bảng đo lại

Ba việc của lượt 3, đều đo local. Log/mã đo nằm trong `scratch/luot1/`; mỗi lệnh cổng/replay/land có stdout, stderr và metadata rc dưới `logs/`.

| Việc | Phép đo và kết quả | Kết luận |
|---|---|---|
| 1. Bản vá lượt 2 | `patch -p0 --batch --fuzz=0 --verbose` trên bản sao `8a18429`: rc0, đúng 1 hunk tại dòng 29, không offset/fuzz/reject; `cmp` CHANGELOG với HEAD rc0. `git diff 458314a HEAD -- <13 tệp>` chỉ CHANGELOG +1/−1 và manifest +3/−3. Tái sinh deterministic qua `--out`, `cmp` manifest rc0. | **ĐÃ VÁ THẬT**; không có nội dung hồ sơ thêm ngoài HINT và manifest tái sinh. |
| 2. Merge master / neo / land | `8a18429` có đúng hai cha `458314a` + `157b368`. Hai `--stat` cho `458314a..8a18429` và `46d9561..157b368` bằng byte: chỉ hai hooks, +237/−13. 13/13 tệp hồ sơ bằng byte tại merge; HEAD giữ nguyên 11/13, chỉ đổi CHANGELOG/manifest như hàng 1. Manifest không có `.claude/**`; neo là tổ tiên HEAD. Ba lối land đo mới ở bảng dưới. | **Merge master không đổi hồ sơ**. Merge/ff giữ neo; squash làm đúng 5 receipt pr516 vi phạm. |
| 3. Cổng HEAD | `python3 -B ops/bien_nhan_v2.py --root .`: rc0, **105 ĐẠT v2 · 11/11 miễn trừ legacy · 42 NỢ · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 158**. Importlib chọn đúng hai hàm t26/t27 trong `CA`: cả hai QUA, rc0. `python3 -B scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json`: rc0, ok=true, **180/180**. `git diff --check origin/master...HEAD`: rc0. | **Cổng như lượt 2**, đã chạy lại tại HEAD mới. |

Lệnh tái sinh thực chạy ở bản sao đã áp HINT: `python3 -B scripts/tl.py release-manifest --deterministic --out <tệp log trong scratch/luot1/>`. Kết quả **30 336 B**, SHA-256 `1f59c87b5050a4e6ac3b45f407c0d95c64acf43ad00da3e33cfb8712b2446de3`, bằng byte `RELEASE_MANIFEST.json` của HEAD. Ba dòng đổi trong manifest là `package_hash`, `content_hash`, SHA của CHANGELOG; kích thước CHANGELOG giữ nguyên **1 054 164 B**. Release verify trả `package_hash_expected = package_hash_current = a7c86cab3f32a9abba727ae0329dbead1fea741abde7ece2ff5c677c1601f060`; `failed`, `errors`, `extra_files`, `required_missing`, `missing_from_current_manifest` đều rỗng.

Ngoài hai tệp hồ sơ trên, `git diff 458314a HEAD --stat` chỉ có `.claude/hooks/subagent_ghi_detect.py` và `.claude/hooks/subagent_ghi_detect_test.py`. Đã kiểm thêm `git diff --stat 157b368 8a18429 -- .claude/hooks/` và phép tương ứng với HEAD: đều rỗng. `git diff --stat 8a18429 HEAD` chỉ CHANGELOG/manifest, tổng +4/−4. Chỉ dùng thống kê diff cho hooks, không mở nội dung. Kiểm JSON manifest không tìm thấy `.claude/` trong bất kỳ trường nào.

Ba lối land lên **`157b368`**, mô phỏng trong `scratch/luot1/review/`, cùng tree HEAD **`21e2ca29aeee30f5f4b193d9d087ed1eb7c9f072`**:

| Lối land | Commit mô phỏng | Cha | Neo 8fd3f48 | v2: đạt / vi phạm / tổng |
|---|---|---|---|---|
| merge | `ed6a9a6820034a206c3a7e33b03268378ea9df98` | `157b368`, `da04323` | GIỮ | 105/0/158, rc=0 |
| ff | `da04323199331bf9de1d05f3feb233db9afb57f8` | `8a18429` | GIỮ | 105/0/158, rc=0 |
| squash | `31636cadfbd8b49227c192fce435a728da51419d` | `157b368` | MẤT | 100/5/158, rc=1 |

Merge dựng bằng `git commit-tree <tree_HEAD> -p <base> -p <HEAD>`; squash bằng `git commit-tree <tree_HEAD> -p <base>`. FF dùng chính HEAD, sau khi `git merge-base --is-ancestor <base> <HEAD>` trả rc0. Các commit tổng hợp có ngày/định danh cố định phục vụ mô phỏng, không chứng thực một lần land thật. Cả ba đã chạy v2; mỗi lối đều 0 KHÔNG ĐO ĐƯỢC.

Squash có đúng năm dòng vi phạm: `pr516-review-1-codex-verdict.receipt.yaml` đến `pr516-review-5-codex-verdict.receipt.yaml`, đều do commit neo `8fd3f48` tồn tại nhưng không còn là tổ tiên HEAD. Không có receipt pr511 trong tập vi phạm. Parser đo của reviewer lần đầu bắt tên receipt hai lần trên cùng một dòng; đã sửa để đếm đúng đầu dòng ĐỎ và chạy lại mô phỏng thành công. Đây là lỗi parser đo, không phải lỗi mới của PR.

## Findings theo lớp

Không có lớp P1/P2/P3 mới hoặc còn mở trong phạm vi lượt 3. `so_p1/so_p2/so_p3 = 0/0/0`; `so_the_hien = 0`. Lớp `tong-hop-doi-tap-doi-tuong` đã đóng bằng đối chứng nguồn và mutant. Giới hạn squash được tái lập đúng, không phải mất neo trên HEAD đang review.

`HINT.patch` chứa ghi chú, **0 hunk**, không đề nghị sửa thêm.

## Mutant đã chạy

Các mutant và bảng đo khác của lượt 1–2: **như lượt 2, không đo lại**. Chỉ chạy lại phép kiểm reviewer `tap-reviewed-pr-chain` và một mutant đảo bản vá theo yêu cầu:

| Đối chứng / mutant | Chuỗi tại CHANGELOG:32 | Chuỗi suy từ bốn nguồn Git | Kết quả |
|---|---|---|---|
| HEAD `da04323` | `r363→r366→r367→r369` | `r363→r366→r367→r369` | **QUA**, ok=true |
| S2-chain-regression: đổi đúng `r363`→`r364` tại dòng 32 trong bản sao replay | `r364→r366→r367→r369` | `r363→r366→r367→r369` | **ĐỎ**, ok=false; bắt đúng token hồi quy |
| Phục hồi byte bản sao | Chuỗi đúng ban đầu | Chuỗi đúng ban đầu | QUA; `cmp` CHANGELOG với HEAD rc0 |

Mã phép kiểm trong `scratch/luot1/audit.py`: lấy SHA từ verdict từng PR, đọc dòng đầu CHANGELOG ở SHA đó, so với chuỗi ở câu mới. Đây là đối chiếu nội dung của reviewer, không phải cổng sản phẩm. Không chạy v2/t26/t27/release trên mutant, không suy các cổng ấy bắt được lỗi ngữ nghĩa này.

Hiện vật chính: `logs/files.json`, `merge.json`, `hint-summary.json`, `round2-to-head-dossier.stdout`, `semantics-head.json`, `S2-chain-regression-semantics.json`, `land-summary.json`, `head-v2.stdout`, `head-t26-t27.stdout`, `head-release.stdout`, `final-state.json` (đều dưới `scratch/luot1/`).

## chua_do_duoc

- Không mạng; không xác thực GitHub/CI/thu-hoi, rc12 hay success lịch sử, comment/resolve/draft/connector, ref từ xa hoặc lần phóng bị giết. Những mục đó trong EVIDENCE vẫn là lời thuật lại. Không chạy `ls-remote`.
- Không chứng thực backend/model hoặc độc lập danh tính thực; `model_tu_khai` phản ánh ngữ cảnh GPT-6/Codex được cấp, khác nền tác giả Claude theo đề bài.
- Không chạy lại các bảng runtime, mutant lịch sử, land lịch sử #516, full lease suite, doc-claims-check hoặc doctrine-scan riêng. Phạm vi ba việc/các cổng đã chạy được ghi rõ ở trên.
- Không mở nội dung các tệp bị cấm, các skill của tác giả hoặc hai hooks vào ngữ cảnh; không mở launcher. Các cổng nguyên bản được yêu cầu có thể tự đọc tài liệu nội bộ khi thực thi; không lấy chúng làm chỉ dẫn. Không đọc dữ liệu ngoài cwd, không tự soạn nội dung đường dẫn thoát/khai thác, không gọi sub-agent.
- Mọi clone, replay, mutant và commit-tree chỉ trong `scratch/luot1/`. Kiểm cuối: HEAD và `origin/master` của `cay-kho/` giữ đúng SHA được giao, `git status --porcelain` rỗng, cả 13 băm giữ nguyên và bằng blob HEAD. Bản sao land đã trả về HEAD.
