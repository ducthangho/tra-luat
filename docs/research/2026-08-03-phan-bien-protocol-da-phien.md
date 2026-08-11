# Kiểm chứng sáu phản biện về Protocol đa phiên Claude–Codex

- **Ngày đo:** 2026-08-03
- **Phạm vi:** P1–P6 trong phản biện được cung cấp; chỉ dùng mã, lịch sử Git và tài liệu chính thức.
- **Mốc repo:** worktree `master` cục bộ ở `e8134a2`; `origin/master` ở `3f29616` (`r324`,
  `v1.36.56`). Nhánh mang tên `r325` đã tồn tại, nên không coi `r325` là số còn trống.
- **Lưu ý trạng thái:** các ADR và `docs/PROTOCOL_DA_PHIEN.md` đang là thay đổi chưa commit. Số đo file
  committed dùng `origin/master`; số đo lịch sử được ghi rõ mốc SHA.

## Kết luận nhanh

| Điểm | Phân loại | Quyết định tiếp thu |
|---|---|---|
| P1 — write set toàn repo khóa tệp nóng | **Đúng** | Test fragment `scripts/test_fragments/wp<issue>_<slug>.py`; không dùng `merge=union` |
| P2 — EOL migration bị hook/các phiên sống chặn | **Đúng một phần** | Operational freeze/drain, migration ba commit và EOL base bắt buộc rebase |
| P3 — khoảng chết của deferred manifest | **Đúng một phần** | Kích hoạt nguyên tử deferred numbering + worker gate dùng manifest tạm |
| P4 — coupling `SKILL.md` ↔ `GOTCHAS.md` | **Đúng** | Change-impact rule có hướng: write closure + required checks |
| P5 — Android không đóng mission | **Đúng một phần** | `land apply` là operation trung lập thiết bị; skill/comment/workflow là client |
| P6 — khối lượng triển khai quá lớn | **Đúng một phần** | Foundation pha 1–2 cam kết trước; automation pha 3–8 promote từng epic |

## Quyết định sau grilling

Người dùng đã chấp nhận toàn bộ khuyến nghị P1–P6. Thiết kế cuối giữ GitHub/lease/generation làm xương sống và
thêm sáu ràng buộc: test fragment thay việc cùng sửa legacy harness; operational freeze/drain cho EOL; activation
boundary cho deferred numbering/manifest tạm; change-impact policy có hướng; `land apply` exact-head trung lập
thiết bị; và rollout hai chân trời không gọi foundation là tự động hóa hoàn chỉnh. Quyết định kiến trúc nằm trong
ADR-0018, ADR-0026, ADR-0031, ADR-0032 và các ADR land/state liên quan; báo cáo này giữ vai trò bằng chứng.

## P1 — write-set toàn repo và tệp nóng

**Phán quyết: Đúng.** Phản biện tìm đúng nút cổ chai chính, dù số đo `tl.py` bị pha lẫn với churn phát
hành.

### Bằng chứng

- Protocol cấm hai lease có write set giao nhau trên toàn repo và lặp lại exclusion toàn repo tại
  `docs/PROTOCOL_DA_PHIEN.md:17` và `docs/PROTOCOL_DA_PHIEN.md:125-137`.
- `CLAUDE.md:25` bắt mỗi fix thêm một test `rXX_` vào quy trình hiện tại.
- Trên đúng 40 commit kết thúc ở `e8134a2`, `scripts/tl.py` xuất hiện trong **16/40** commit và
  `scripts/tl_selftest.py` trong **17/40**. Trên 40 commit kết thúc ở `origin/master=3f29616`, hai số
  lần lượt là **17/40** và **18/40**. Lệnh đo lấy đúng danh sách `git log -40 --format=%H <ref>`, rồi
  kiểm từng SHA bằng `git diff-tree -r -- <path>`; không dùng `git log -40 -- <path>` vì cách đó lấy
  40 commit *đã chạm path* và làm sai mẫu số.
- Blob `origin/master:scripts/tl_selftest.py` có **28.144 dòng**, **2.050.831 byte**, toàn bộ newline
  là CRLF. Working tree đang bị các phiên khác sửa và đã thành mixed EOL, nên không dùng nó làm baseline.
- Mọi lần chạm `tl.py` trong mẫu cũ đi cùng quy trình release/version, vì vậy deferred numbering sẽ loại
  một phần đáng kể contention của `tl.py`. Điều này không cứu được `tl_selftest.py`: test bắt buộc vẫn làm
  mọi packet code tranh cùng một path.

### Sửa protocol tối thiểu

1. Giữ `scripts/tl_selftest.py` làm loader/harness ổn định; test regression mới nằm ở
   `scripts/test_fragments/wp<issue>_<slug>.py` và được auto-discover theo
   thứ tự tất định. Mỗi packet sở hữu file test riêng; thay loader/harness là packet hạ tầng riêng.
2. Loại thư mục test packet khỏi release bundle để không ăn trần 200 file, nhưng vẫn chạy toàn bộ trong worker
   và land gate.
3. Không dùng `merge=union` cho mã Python. Tài liệu Git chính thức cảnh báo driver `union` có thể để các dòng
   thêm vào theo thứ tự ngẫu nhiên và người dùng phải tự kiểm kết quả; đó không phải semantic merge an toàn cho
   test: [Git `gitattributes` — built-in merge drivers](https://git-scm.com/docs/gitattributes/2.46.0.html).
4. Chỉ nới song song sau khi test sharding có discovery, duplicate-ID check và bằng chứng Windows–Linux. Trước
   đó `max_parallel_workers: 2` không nên được quảng bá là hai code packet thực sự song song.

## P2 — migration EOL, hook và drain phiên

**Phán quyết: Đúng một phần.** Nguy cơ migration và yêu cầu drain là đúng; tuyên bố hook `9ed54fa` đã land
trên master là sai tại mốc kiểm.

### Bằng chứng

- `git merge-base --is-ancestor 9ed54fa origin/master` trả mã 1. `origin/master` vẫn có hook cũ chỉ quét
  secret/binary; EOL guard chỉ nằm trên nhánh `claude/recursing-nightingale-76526b` (sau rebase là commit
  `fd63fde`).
- Nội dung commit `9ed54fa`/`fd63fde` so EOL của blob stage với `HEAD` và chặn mọi đổi loại newline của file
  đã tồn tại; chính commit message chỉ đường thoát `--no-verify`. Vì vậy, **nếu** hook đó được land trước
  migration mà không thay, nó sẽ chặn CRLF → LF như phản biện nói.
- `origin/master` vẫn dùng `* -text` trong `.gitattributes`; `tl_selftest.py` committed có 28.144 CRLF. Một
  renormalize sẽ tạo diff toàn tệp này.
- `git worktree list` tại lúc đo có chín worktree, gồm nhiều branch đang sống. Protocol đã biết khoảng cách này
  tại `docs/PROTOCOL_DA_PHIEN.md:367-380`, còn ADR-0018 đã yêu cầu các branch bàn giao trước migration
  (`docs/adr/0018-eol-canonical-theo-loai-tep.md:8-14`). Tuy nhiên, câu “pause dispatcher” không có tác dụng
  trong phase 1 vì dispatcher chưa tồn tại (`docs/PROTOCOL_DA_PHIEN.md:288-297`).

### Sửa protocol tối thiểu

1. Đổi phase 1 thành **operational freeze/drain**: ngừng tạo branch mới, kiểm kê cả worktree local lẫn PR/branch
   remote, yêu cầu mỗi owner push/bàn giao hoặc hủy, rồi mới đặt mốc EOL.
2. Commit policy đầu tiên phải **thay** EOL-flip shell hook bằng validator policy-aware. Validator xét blob staged
   theo EOL đích, nên một CRLF → LF hợp lệ sẽ qua; không dùng `--no-verify` như quy trình chuẩn.
3. Commit renormalize kế tiếp chỉ đổi newline. Ghi lại base SHA bắt buộc và buộc mọi branch cũ rebase lên nó
   trước khi nhận việc mới. Sau khi dispatcher tồn tại, operational freeze mới được thực thi bằng `PAUSE`/lease.

## P3 — khoảng chuyển tiếp của deferred manifest

**Phán quyết: Đúng một phần.** Repo hiện tại thật sự không hỗ trợ worker tuân deferred manifest; nhưng ADR-0026
không bắt phải kích hoạt protocol trước hai lane. Lỗ hổng là thiếu một **transition invariant**, không phải CLI
không có khả năng kỹ thuật.

### Bằng chứng

- CI hiện chạy `release-verify RELEASE_MANIFEST.json --strict` trên mọi PR tại
  `.github/workflows/ci.yml:73-74`. Sửa file nằm trong package mà không cập nhật manifest sẽ đỏ.
- Protocol đồng thời cấm worker sửa `RELEASE_MANIFEST.json` (`docs/PROTOCOL_DA_PHIEN.md:224-226`) và hứa
  worker gate dùng manifest tạm ngoài repo (`docs/PROTOCOL_DA_PHIEN.md:228-231`). Bootstrap gaps đã tự thừa
  nhận hai lane chưa tồn tại tại `docs/PROTOCOL_DA_PHIEN.md:371-378`.
- CLI hiện có đủ primitive: `release-manifest --root/--out` và `release-verify --root <manifest>`. Probe tạo
  manifest ở temp ngoài repo rồi strict-verify cây hiện tại đạt `ok=true`; không cần đổi runtime để dựng lane.
- Rollout đặt protocol và hai CI lane cùng phase 2 (`docs/PROTOCOL_DA_PHIEN.md:290-292`). Vì vậy failure chỉ
  xuất hiện nếu triển khai hai phần này theo hai lần land tách rời hoặc coi tài liệu thiết kế là policy đã active.

### Sửa protocol tối thiểu

1. Phase 1/EOL vẫn dùng quy trình canonical cũ và được phép tái sinh manifest committed; chưa có worker packet
   theo protocol v1.
2. Artifact phase 2 có thể land dần ở trạng thái tắt, nhưng promotion phải kích hoạt nguyên tử worker/land gate,
   temp-manifest profile, protocol/adapters và required checks. Dispatcher chưa được cấp packet trước activation
   boundary đó.
3. Ghi rõ lệnh local tương đương để debug worker gate: sinh manifest vào thư mục temp ngoài repo, rồi
   `release-verify --root <worktree> <temp-manifest> --strict`. Không cho một khoảng canonical nơi worker bị cấm
   sửa manifest nhưng required check vẫn đòi manifest committed.

## P4 — coupling ẩn giữa file

**Phán quyết: Đúng.** Đây là dependency thực, máy đã cưỡng chế, nhưng schema write set hiện không biểu diễn.

### Bằng chứng

- `references/GOTCHAS.md:16` ghi số đo cụ thể `SKILL.md` = 48.031B.
- Test `r219_gotchas_nhan_trang_thai` lấy trực tiếp `SKILL.md.stat().st_size`, format số đó rồi buộc chuỗi phải
  có trong GOTCHAS (`scripts/tl_selftest.py:24440-24457`). Thay đổi kích thước thân `SKILL.md` mà không sửa
  GOTCHAS làm selftest đỏ.
- `references/GOTCHAS.md:37-39` còn nói golden `workflow_audit` nhúng size `SKILL.md`; đây là companion thứ hai.
- Write set hiện chỉ có `exact|prefix` và dependency giữa packet, không có closure/co-change rule
  (`docs/PROTOCOL_DA_PHIEN.md:63-85`, `docs/PROTOCOL_DA_PHIEN.md:125-137`).

### Sửa protocol tối thiểu

1. Thêm change-impact policy trên canonical. Mỗi rule có hướng từ trigger paths tới write closure và required
   checks; khi cấp lease, dispatcher tính **closure trước khi kiểm giao nhau**. CI tính lại closure từ diff để
   chống khai thiếu.
2. Với coupling có hướng, không dùng “nhóm khóa” đối xứng quá rộng. Ví dụ sửa `SKILL.md` có thể kéo GOTCHAS và
   golden vào closure, nhưng sửa một typo độc lập trong GOTCHAS không cần khóa `SKILL.md`.
3. Loại coupling giả nếu có thể: số đo 48.031B là trạng thái biến động, còn invariant thật là ngưỡng 48.128/49.152B.
   Nên để gate/báo cáo sinh số hiện tại, không bắt tài liệu tay lặp lại nó. Co-change rules dành cho invariant thật
   còn lại, không hợp thức hóa mọi pin số liệu dễ thối.

## P5 — đường land trên Android

**Phán quyết: Đúng một phần.** Protocol đã nói rõ chuỗi tự động dừng ở `awaiting_land`; điều còn thiếu là một
entrypoint apply trung lập nền tảng. Lập luận “skill chỉ là cơ chế của Claude Code” là sai.

### Bằng chứng

- Mục tiêu hiện tại chỉ cam kết chạy tới draft land PR (`docs/PROTOCOL_DA_PHIEN.md:10-12`). Canonical chỉ đổi
  qua `land-packets --apply` (`:20`, `:236-239`), nhưng tập lệnh GitHub/Android chỉ có `/land prepare`
  (`:253-254`). `land-packets` là user-invoked (`:279-282`). Vì vậy một người chỉ dùng control plane GitHub trên
  Android chưa có đường apply được đặc tả.
- ADR-0030 đã nói mission chờ người dùng ở `awaiting_land`, nên phản biện “để người dùng tự phát hiện” là quá
  mạnh; thiếu sót nằm ở **cách gọi**, không phải definition of done.
- Codex cũng hỗ trợ Skills, không riêng Claude Code: [OpenAI — Skills in Codex](https://help.openai.com/en/articles/20001066).
- GitHub cho phép chạy workflow `workflow_dispatch` từ Actions UI/REST API nếu workflow nằm trên default branch
  và actor có quyền write: [GitHub Docs — manually running a workflow](https://docs.github.com/en/actions/how-tos/manage-workflow-runs/manually-run-a-workflow).
  GitHub cũng cung cấp thao tác merge PR sau khi các yêu cầu review/check được thỏa:
  [GitHub Docs — merging a pull request](https://docs.github.com/en/pull-requests/how-tos/merge-and-close-pull-requests/merging-a-pull-request).

### Sửa protocol tối thiểu

1. Định nghĩa `land apply` là operation deterministic của control plane; `land-packets` chỉ là một client/adapter,
   không giữ logic hay thẩm quyền riêng.
2. Cho hai entrypoint cùng gọi operation: `/land apply <mission> <head_sha>` và `workflow_dispatch` với typed
   inputs tương đương. Apply không gọi model.
3. Chỉ chấp nhận khi draft land PR/head SHA khớp bản đã freeze, land gate xanh, actor qua ADR-0023 và approval
   được audit. Deploy LIVE vẫn là cổng riêng.
4. Nói thẳng trong mục Android: tự động hóa dừng ở `awaiting_land`; người dùng có thể phê duyệt/apply trên Android
   qua GitHub mà không cần Windows host, nhưng không có auto-merge.

## P6 — khối lượng triển khai

**Phán quyết: Đúng một phần.** Rủi ro delivery là thật; nhưng bỏ ngỏ toàn bộ phase 3+ đồng nghĩa không đáp ứng
yêu cầu tự sinh/tiếp tục phiên khi máy tắt. Cần cắt commitment, không được gọi phần chưa làm là hoàn tất.

### Bằng chứng

- Thiết kế có 14 ADR từ 0017 đến 0030 và tám phase rollout (`docs/PROTOCOL_DA_PHIEN.md:288-299`).
- Bootstrap gaps ghi dispatcher, ba skill/adapters, Issue Forms, provider broker, local controller và branch
  protection đều chưa tồn tại (`docs/PROTOCOL_DA_PHIEN.md:367-380`). Đây là nhiều sản phẩm con với failure mode
  khác nhau, không phải một thay đổi CI nhỏ.
- Phần lớn giá trị giảm conflict có thể nhận ở phase 1–2: EOL, deferred numbering/changelog, test sharding,
  co-change rules, protocol và worker/land gate. Nhưng tự động tạo successor/cloud/local cần phase 3–7 theo chính
  roadmap (`docs/PROTOCOL_DA_PHIEN.md:292-297`).

### Sửa protocol tối thiểu

1. Gọi phase 1–2 là **foundation horizon cam kết** với definition of done riêng: repo conflict-safe cho các phiên
   do người dùng khởi chạy, chưa tuyên bố autonomous mission.
2. Phase 3 shadow là checkpoint bắt buộc trước mọi secret/model call. Sau báo cáo shadow, người dùng quyết định
   promote một epic nhỏ: cloud canary; dual review; successor; local controller; land automation. Không triển khai
   nhiều epic trong một PR/mission.
3. OIDC broker là đích an ninh của cloud lane, không phải dependency của MVP. Canary có thể dùng provider key
   riêng, quota cứng và job cô lập như protocol đã cho phép chuyển tiếp.
4. Giữ phase 3–7 trong roadmap vì đó là mục tiêu ban đầu, nhưng gắn trạng thái `planned/not implemented`, budget
   và promotion evidence. Nếu dừng sau phase 2, tài liệu phải nói rõ hệ thống giảm conflict nhưng **chưa** tự tạo
   phiên kế nhiệm hoặc tiếp tục khi Windows tắt.

## Phương án hợp nhất sau phản biện

Không thay xương sống GitHub/lease/generation. Chỉ thêm bốn mảnh vào trước dispatcher:

1. test sharding theo `wp<issue>` để write-set exclusion không biến thành khóa test toàn cục;
2. co-change closure cho dependency file thật, đồng thời bỏ pin số đo động không cần thiết;
3. operational drain + hook replacement rõ ràng cho EOL migration;
4. promotion phase 2 nguyên tử để deferred manifest và worker lane có hiệu lực cùng lúc.

Sau đó thêm `land apply` trung lập nền tảng trước khi tuyên bố Android end-to-end. Giới hạn delivery thành MVP
phase 1–2 rồi từng epic nhỏ không làm yếu mục tiêu cuối; nó chỉ ngăn một thiết kế 14 ADR bị triển khai big bang.

## Lệnh kiểm chứng chính

```text
git log -40 --format=%H <ref>
git diff-tree --no-commit-id --name-only -r <sha> -- <path>
git cat-file -s origin/master:scripts/tl_selftest.py
git show origin/master:.gitattributes
git merge-base --is-ancestor 9ed54fa origin/master
git show origin/master:.githooks/pre-commit
git worktree list
python scripts/tl.py release-manifest --help
python scripts/tl.py release-verify --help
```
