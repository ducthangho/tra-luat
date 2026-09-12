verdict: approve
reviewed_sha: 5f45e6e99bcd4cf8a410b99031d4a600bf5e83bb
reviewed_base: 6786637343452359eeb2ec5aaaaef709a623be95
reviewed_files_sha256:
  CHANGELOG.md: e3d47a7663060e1b74927d6f9dfd61ae5059dd89521e33a092059f34334a4be9
  RELEASE_MANIFEST.json: e3d9b181c693d68e83d92ead8d5084b0e8e2841b1822da8de31667d585443d63
  ops/reviews/README.md: 012a130b6f5045a1e4e52bfd648ba6f1f81435d85fe313fdb6645fbfeda8c70b
  ops/reviews/pr511-review-1-codex-verdict.md: 4e86bc17a72af476d2337bdba170dd569ff503c3bcc3ededf938b2fde5f4e6bf
  ops/reviews/pr511-review-1-codex-verdict.receipt.yaml: 896e5e75f8b42d4242341e3ae66da03a843440d7149a2429d736c7c5c63868b2
  ops/reviews/pr511-review-2-codex-verdict.md: cfe618258d782354b84b9dbeb733bf2861adfc04d94edd4cc3fb85a6effe842e
  ops/reviews/pr511-review-2-codex-verdict.receipt.yaml: d9552731686c100a150c383b853540d441ad9e60f5e3df55539626e9bc05b95f
model_tu_khai: GPT-6 / Codex (tự khai theo ngữ cảnh phiên; không xác thực độc lập backend)
review_round: 3
so_p1: 0
so_p2: 0
so_p3: 0
hint_sha256: f2703a7cad006c63204c715a83f5dbbbb232ecd81fbaa5d75ae8efaff21080e9

## ĐỐI CHIẾU LƯỢT TRƯỚC

- Lượt 2 sandbox: `approve` 0/0/0 trên `a41fc69` — **không có finding để đối chiếu**. Băm lại `nguon/VERDICT.rvhs516-2.md`: `e2d0fc65a809cb7e2be27804f518d41a09a8329b672ae8ebfa438603cb0202fe`, 36 923 B. Lượt này xử lý hai P1 của connector, không gán chúng thành finding của lượt 2 sandbox.
- Connector P1 **assurance — ĐÃ VÁ THẬT**: verdict #511 lượt 2 thiếu mục đối chiếu và cả bốn cụm canonical; receipt2:20 đã hạ `cross_approved` → `cross_reviewed`; caveat2:103–119, README:29 và CHANGELOG:81–89 nói rõ giới hạn. Mức hạ đúng cho một review đã thực hiện nhưng chưa đáp ứng hợp đồng tái-review. Mutant đảo lại assurance SỐNG 4/4, đúng nợ cổng được công bố; không lấy cổng xanh làm bằng chứng hoàn thành hợp đồng.
- Connector P1 **re-anchor — KHÔNG ÁP DỤNG — bằng chứng**: `git -C cay-kho cat-file -t 6fe742e` rc=128; `git -C cay-kho merge-base --is-ancestor 120d47a HEAD` rc=0; hai blob tại URL neo khớp byte verdict và băm receipt; v2 83 ĐẠT / 0 vi phạm / 0 KHÔNG ĐO ĐƯỢC. **Việc bác yêu cầu re-anchor ĐÚNG trên HEAD được review.** Không suy từ việc thiếu object rằng đã chứng minh được nguồn gốc “squash tổng hợp của connector”.

**Kết luận: approve — 0 P1 / 0 P2 / 0 P3. Bản vá P1 “assurance” ĐÃ VÁ THẬT; việc bác P1 “re-anchor” ĐÚNG trong phạm vi HEAD `5f45e6e`.** Đây là kết luận về hồ sơ hiện tại, không hồi tố biến verdict #511 lượt 2 thành verdict đúng cấu trúc, không đóng nợ validator hoặc nợ hồ sơ #510.

## Bảng đo lại

Đo trực tiếp trong `cay-kho/`, trừ tái sinh manifest và mutant chạy trong clone cục bộ `scratch/probe/`. Không dùng mạng. `VERDICT.md` được ghi sơ bộ trước khi chạy cổng rồi bổ sung. Thời gian công cụ: bắt đầu 19:57:56Z ngày 2026-09-11, hoàn tất trong giới hạn 30 phút.

| Phép đo | Kết quả tự chạy |
|---|---|
| HEAD / base | `git rev-parse HEAD origin/master` đúng hai SHA đầy đủ trong đầu verdict. `git rev-list --count a41fc69..HEAD` = 1. |
| Diff PR ba chấm | `git diff --name-status origin/master...HEAD`: đúng 7 tệp; băm byte worktree ở đầu verdict. |
| Bản vá hai chấm | `git diff a41fc69..HEAD --numstat`: CHANGELOG +22/−0; manifest +5/−5; README +1/−0; receipt2 +18/−1. Không đổi gate code. |
| Ba tệp phải bất biến | So byte `git show a41fc69:<path>` với HEAD: cả hai verdict #511 và receipt lượt 1 đều bằng nhau. Hai verdict cũng bằng byte `nguon/VERDICT.rvhs511-{1,2}.md`. |
| Protocol, đúng ngoại lệ đọc | `grep -n 'ĐỐI CHIẾU LƯỢT TRƯỚC'` tìm dòng 563. Chỉ đọc dòng 548–578 (±15): từ lượt HAI phải có mục này, tự kiểm TỪNG finding lượt liền trước, gán một trong bốn trạng thái và kèm bằng chứng tự đo. Không đọc phần khác của tệp. |
| Verdict #511 lượt 2: tiêu đề | `grep -n '^## '` chỉ có `Bảng đo lại`:27, `Findings`:460, `Mutant đã chạy`:468, `chua_do_duoc`:489. Không có mục đối chiếu. |
| Verdict #511 lượt 2: canonical | Đếm toàn tệp lần lượt `ĐÃ VÁ THẬT` / `VÁ HỜ` / `VÁ SINH LỖI MỚI` / `CHƯA VÁ` = **0/0/0/0**. Năm hàng 355–359 kiểm năm P2 cũ nhưng kết quả là `ĐÓNG`, không phân loại canonical. |
| Verdict thật và receipt2 | Verdict vẫn `approve`, `so_p1/so_p2/so_p3=0/0/0`; không sửa byte để bổ sung mục bị thiếu. Receipt `assurance: cross_reviewed`, `luot: 2`; caveat mới có `muc: P1`, ghi rõ không được xem là đã trả nợ ở mức `cross_approved`. Severity của caveat không phải một P1 còn mở trong review lượt 3. |
| Giá trị assurance theo v2 | `YEU_CAU` tại v2:464–488 không đặt enum assurance; `_thieu` tại 631–670 kiểm các mức qua tập cấm theo provider và `ASSURANCE_CAN_DOC_LAP` tại 494. `cross_reviewed` không thuộc ba mức đòi thẩm quyền độc lập và không bị từ chối. **Được cổng hiện tại chấp nhận**, không đồng nghĩa có một enum/hệ thứ bậc hoàn chỉnh đã được validator chứng minh. |
| Mức hạ có đúng nghĩa không? | Có review khác nền được lưu, có bảng tự đo và verdict approve; thiếu hợp đồng tái-review. `cross_reviewed` chỉ giữ sự kiện đã review, bỏ khẳng định approval đủ điều kiện. Không có căn cứ trong phạm vi đo để ép xuống `review_deferred`, đổi thành same-provider hay human-audited. Chính code gợi ý deferred khi thiếu bằng chứng phiên độc lập; đây không phải thiếu sót đang xét. |
| Caveat và hàng README mới | Đúng các phép đo về thiếu mục, năm hàng `ĐÓNG`, mức hạ, yêu cầu review đúng dạng trên `6adb7ff`, và giới hạn validator. Không phủ nhận nội dung bảng tự đo hay xoá kết quả approve nguyên bản. Các sự kiện connector/GitHub vẫn thuộc nguồn thuật lại theo README:15 và CHANGELOG:22–24. Không kiểm adapter bị cấm. |
| Prompt trong gói | `nguon/runs/8873d98d/prompt.snapshot`, SHA-256 `23cc59ec34cb975d99657029e24479f1afcc24ad31d6c44f49342a28d3a97cd2`, không có literal mục đối chiếu/canonical; prompt #516 lượt 2 `nguon/runs/457a6568/prompt.snapshot` có yêu cầu và bốn trạng thái ở dòng 5. Xác nhận khác biệt prompt; quan hệ nhân quả “lỗi do tác giả soạn” là giải thích của tác giả. |
| Receipt #511 lượt 1 | `luot: 1`, `verdict: changes_requested`, `assurance: cross_reviewed`; byte không đổi. Điều kiện bắt đầu từ lượt HAI không áp cho lượt 1; không cần sửa vì P1 này. |
| Cùng khuyết tật ở #510? | Có: verdict2 băm `41c3533c68b4e6894b2ea1dc59aebfdfa6d8da751b118a8bc149088dd87f0f25`, bằng byte base. `^## ` chỉ có Bảng đo lại:47 / Findings:908 / Mutant:914 / chua_do_duoc:931. Bảng `### Đóng từng finding lượt 1` tại 49–59 có sáu kết quả `ĐÓNG`, thiếu mục/phân loại theo hợp đồng. Receipt đã land vẫn `luot: 2`, `assurance: cross_approved`. Chỉ xác nhận nợ đã khai, không yêu cầu sửa hiện vật đã land trong PR này. |
| Không nói quá phép grep #510 | Đếm canonical toàn tệp #510 = **10/0/0/0**; mười lần `ĐÃ VÁ THẬT` ở 166,650,672,694,716,738,760,782,804,826 là phần trích hồ sơ PR #505. Không thể lấy chúng làm phân loại sáu finding #510 lượt trước, cũng không được khai rằng #510 có 0 literal như #511. |
| `cross_approved` còn trong CHANGELOG r369 | Có ở dòng 65,84,88,107,109. Dòng 65 ghi **Commit 2**, đúng lịch sử: blob receipt2 tại `1dafbec` có `cross_approved`; README cùng commit có 646 dòng. Dòng 84 ghi lần hạ sau đó; 88/109 nói nợ validator, 107 nói receipt #510 đã land. Không có hai kết luận assurance hiện tại đối nghịch khi đọc đúng mốc. |
| `cross_approved` trong README, hàng #511 | Chỉ hàng caveat mới dòng 29: một lần là giá trị trước khi hạ, một lần là mức cần review lại đúng dạng để đạt. Không có hàng #511 khác vẫn khẳng định assurance hiện tại là `cross_approved`. `approve` nguyên bản là verdict, không phải mức assurance. |
| Neo: object connector | `git cat-file -t 6fe742e`: rc=128, `fatal: Not a valid object name 6fe742e`. Kết luận giới hạn ở clone được cấp; không fetch, không kết luận object không tồn tại ở mọi kho. |
| Neo: ancestry và byte | `git merge-base --is-ancestor 120d47a HEAD`: rc=0. Hai receipt vẫn dùng `blob/120d47a076d61813921a293a3f667e04d0e715cf/...`; đọc hai blob Git và so với byte verdict HEAD, băm bằng `verdict_sha256`: cả hai khớp. |
| v2 trên HEAD | rc=0; 83 ĐẠT / 11 miễn trừ / 42 NỢ / 0 vi phạm / 0 KHÔNG ĐO ĐƯỢC / tổng 136 |
| t26 / t27 trên HEAD | rc=0 / rc=0 |
| release-verify --strict --json trên HEAD | rc=0, ok=true, 180/180 |
| Bản sao sạch, cùng HEAD, core.abbrev=7 | Bốn cổng có cùng kết quả HEAD |
| Manifest tái sinh | Trên bản sao cùng HEAD: `python3 -B scripts/tl.py release-manifest --deterministic --out RELEASE_MANIFEST.json`, rc=0; bằng byte trước chạy và manifest gốc HEAD; **30 336 B**, SHA-256 `e3d9b181c693d68e83d92ead8d5084b0e8e2841b1822da8de31667d585443d63`. |
| git diff --check (worktree, PR ba chấm, bản vá hai chấm) | Cả ba rc=0 |
| README và số caveat | **647 LF**; receipt2 có **4** caveat, từng id có đúng 1 hàng tại 29–32. Receipt1 có 2 caveat tại 33–34: hiện tại tổng 6 hàng cảnh báo #511, tăng 1 so gói ban đầu. Không dùng số 5 cảnh báo/646 dòng của phần kể gói trước làm số hiện tại. |

Đối chiếu riêng bốn caveat receipt lượt 2 với README:

| id | dòng README | số hàng khớp đúng cặp verdict/id |
|---|---|---|
| `APPROVE-LUOT-2-THIEU-MUC-DOI-CHIEU-LUOT-TRUOC-assurance-ha-xuong-cross_reviewed` | 29 | 1 |
| `APPROVE-HO-SO-la-dieu-kien-DUNG-merge-theo-LUAT-CHUNG-chu-kho-14-4xZ` | 30 | 1 |
| `VERDICT-BYTES-VA-SO-P-TRONG-BIEN-NHAN-KHONG-CO-CONG-NAO-CANH` | 31 | 1 |
| `BANG-DO-LAI-KHONG-LEN-COMMENT-tep-trong-kho-la-ban-du` | 32 | 1 |

Lệnh chạy t26/t27 gọi trực tiếp đúng hai hàm test bằng Python `-B`, import `ops/lease_publish_test.py`; không chạy toàn suite. Lệnh chuẩn và rc lưu ở `scratch/logs/head.gates.json`; stdout/stderr từng cổng nằm cạnh đó. Mã runner: `scratch/run_gates.py`. Các log `copy-control.*`, `manifest.*` và `mutant-assurance.*` phân biệt rõ cây đối chứng, phép tái sinh và mutant.

## Findings

Không có P1/P2/P3 mới trong phạm vi hai câu hỏi và bản vá lượt này.

Bản vá **đúng và đủ cho hồ sơ #511**: hạ mức assurance, giữ nguyên bằng chứng, nêu thiếu sót tại receipt và cửa đọc README, ghi rõ nợ cổng. Nó không tự vá hợp đồng của verdict cũ hay bổ sung fixture validator; cả hai giới hạn được nói ra. Muốn nâng lại assurance phải có lượt tái-review đáp ứng protocol. Ghi nợ validator là phù hợp phạm vi PR hồ sơ hiện tại.

Không thấy điểm đúng của yêu cầu re-anchor bị bỏ qua **trên HEAD thật**: neo là tổ tiên và trỏ đúng blob. Hạn chế khi squash đã được `anchor.gioi_han` khai rõ. Kết luận không bao phủ một commit tổng hợp/đường land khác không được cấp cho lượt này.

`HINT.patch`: 0 hunk, một dòng ghi chú. Không có thay đổi đề xuất cần áp bằng `patch -p0`.

## Mutant đã chạy

Chạy một mutant theo yêu cầu, sau đối chứng bốn cổng xanh trong clone cùng HEAD, `core.abbrev=7`. Chỉ thay đúng scalar ở receipt #511 lượt 2:

```diff
-assurance: cross_reviewed
+assurance: cross_approved
```

Không đổi caveat/README, verdict, neo hoặc manifest. Patch đo được lưu ở `scratch/logs/mutant-assurance.patch`.

| Mutant | v2 | t26 | t27 | release-verify strict | Kết luận |
|---|---|---|---|---|---|
| M1: đảo assurance về `cross_approved` | rc=0; 83 ĐẠT, 0 vi phạm, 0 chưa đo | rc=0 | rc=0 | rc=0, ok=true, 180/180 | **SỐNG 4/4 — KHÔNG cổng nào bắt** |

Kết quả đúng kỳ vọng nhưng là giới hạn thật: v2 không kiểm cấu trúc/phân loại tái-review; t26 kiểm băm verdict; t27 kiểm cặp caveat↔mục lục, không so ý nghĩa scalar assurance với caveat; release không phát hiện thay đổi receipt này. Vì vậy không dùng kết quả xanh để chứng minh `cross_approved` là đúng. Hồ sơ đã khai chính giới hạn này tại CHANGELOG:109–110 và caveat mới.

## chua_do_duoc

- Không dùng mạng: không xác thực GitHub, CI trên HEAD, nội dung/thời điểm hai review threads connector hoặc việc resolve. Hai P1 là bản thuật lại trong `EVIDENCE.md`; phần kỹ thuật được kiểm độc lập bằng hiện vật local.
- Không chứng minh `6fe742e` do connector tạo bằng squash. Phép đo chỉ chứng minh clone không có object đó; lý do bác re-anchor trên HEAD dựa vào ancestry và byte của **chính HEAD**, không dựa vào suy đoán nguồn gốc object vắng mặt.
- Không xác thực model backend hay danh tính thực của tác giả/reviewer ngoài lời tự khai trong phiên và hồ sơ. Phiên này tự khai Codex, khác nền tác giả tự khai Claude.
- Không mở `cay-kho/CLAUDE.md`, `cay-kho/AGENTS.md`, `cay-kho/.claude/skills/**`; không đọc nội dung adapter được nhắc trong caveat. Protocol chỉ đọc đúng 548–578 sau grep được phép. Chạy các cổng được yêu cầu bằng mã gốc; không trích các nguồn nội bộ bị cấm mà mã cổng tự dùng.
- Không chạy lại bảng đo/mutant/ba cách land của lượt 1–2: không cần cho delta này, và không nhận kết quả cũ là phép chạy mới. Không tự soạn payload dạng đường dẫn thoát/khai thác. Mọi bản sao và log mới nằm trong cwd; không sửa `cay-kho/` ở mức Git.

Kiểm cuối: HEAD/base giữ nguyên, `git status --porcelain=v1` rỗng; bảy băm đầu verdict vẫn khớp byte trong cây gốc.
