verdict: changes_requested
reviewed_sha: 088511f1fd75faf9bf01f0cf8da037a14fa6d22d
spec_sha256: 8cb024367ef99886eaba9d9f6af5100601780ac990fd81c8d718cf1695adb707
model/effort tự khai: Claude Opus 5.5 (`claude-opus-5-5`), effort max, chạy như subagent do phiên điều phối giao (lượt 7).
KHÔNG phải codex. Lời khai này là CẤU HÌNH được giao, không phải runtime evidence (PROTOCOL :710–711) — chính lớp
`hop-dong-dong-bang-thieu-neo` dưới đây áp cho cả lượt này. Lượt thay cho một lượt trước bị cắt ngang do container khởi
động lại; bản dở `goi-dut-1/` chỉ tham khảo, mọi số ở đây ĐO LẠI. Không sửa `cay-kho` tại chỗ, không mạng, không đăng
GitHub, không commit/push. Ghi chỉ dưới `$R/goi/` và các thư mục `mktemp -d -p "$R"`.

Kết luận nội dung: **0 P1 / 2 P2 / 3 P3** (theo lớp). Hai P2: `thu-tu-677-bo-ngo-o-dieu-kien-cap`,
`hop-dong-dong-bang-thieu-neo` (TÁI MỞ). Ba P3: `q10-he-qua-mat-nhan-dien-giai`, `dong-reviewer-loi-khai-rong-hon-do`,
`so-do-nen-khong-khop` (TÁI MỞ ở P3). Câu hỏi gốc: r7 **đúng** là chỉ đổi những byte Q10 cho phép (0 byte kỹ thuật đổi,
đo ở Hướng 1); nhưng hai chỗ r7 thêm vào để làm việc Q10 cho phép — vế review mới của closure và việc tự xử lý tương tác
#677 — chưa kiểm/thi hành được như viết. Làm đúng từng chữ r7 thì packet VẪN có đường land hợp lệ (qua `human_audited`
của chủ kho, có tiền lệ 4 biên nhận), nên không có P1.

## NEO (bước đầu tiên của PROMPT)
- `sha256sum $R/SPEC.md` ⇒ `8cb024367ef99886eaba9d9f6af5100601780ac990fd81c8d718cf1695adb707` (khớp PROMPT)
- `sha256sum $R/SPEC-r6.md` ⇒ `d1f9dd7903c99df03b9e65bc06a2175eb43e0e602758a6945508ff33af76244c` (khớp PROMPT)
- `git -C $R/cay-kho rev-parse HEAD` ⇒ `088511f1fd75faf9bf01f0cf8da037a14fa6d22d` (khớp); HEAD detached (`symbolic-ref -q HEAD` rc=1)
- `cmp $R/SPEC.md $R/cay-kho/ops/specs/lease-id-ep-kieu-yaml-r7.md` ⇒ khớp từng byte
- `git -C $R/cay-kho config core.abbrev` ⇒ `7`; `git status --porcelain --ignored` ⇒ 0 dòng; tree `1cadf3bf092a…c713`
- Mirror `kho.git`: bare, không nông, 6 nhánh (`master`=423b4ba, `claude/spec-wp678-r7`=088511f, `ops/spec-lease-id-ep-kieu-yaml`
  =03a7219, `claude/bookkeeping-668`, `claude/bookkeeping-678-spec-land`, `ops/spec-launcher-con-song-esrch`) + 41 tag. Pack
  của mirror có inode khác mọi pack của `/home/user/tra-luat` (link=1 ở kho thật) ⇒ độc lập với kho thật.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Lượt 6 (codex, `luot6/VERDICT.md`, sha256 `9569bf0d…c18d` = `ops/reviews/wp678-spec-review-6-codex-verdict.md`, `cmp` khớp)
approve r6 với 0 lớp; bảng đối chiếu của nó giữ 9 lớp lịch sử của lượt 1–5. Vì §1, §2, §5, §6, §7 (A1–A10), §9, Phụ lục A
của r7 GIỐNG TỪNG BYTE r6 (Hướng 1), mọi lớp gắn vào các mục ấy giữ nguyên trạng thái. Đối chiếu từng lớp:

| lớp (nguồn) | trạng thái lượt 6 | r7 | bằng chứng tự đo |
|---|---|---|---|
| `bo-quet-nghiem-thu-thieu-mien` (l1, l2, l5) | ĐÃ ĐÓNG biểu hiện r5; CHUYỂN GIAO | GIỮ NGUYÊN | §7 A9 giống byte (Hướng 1) |
| `bo-quet-chung-cu-khong-neo-anh` (l2–l5) | NGOÀI PHẠM VI theo Q9 / CHUYỂN GIAO | GIỮ NGUYÊN | §3 Q9, §7 A9, §9, §10 (gạch helper A9), Phụ lục A giống byte; §3 chỉ THÊM Q10 |
| `bo-quet-khong-co-cua-chay` (l2, l3) | CHUYỂN GIAO | GIỮ NGUYÊN | §7 giống byte |
| `tieu-chi-dot-bien-khong-phan-biet-chot` (l1) | ĐÃ ĐÓNG trong hợp đồng | GIỮ NGUYÊN | §7 A2/A5 giống byte |
| `so-do-nen-khong-khop` (l1) | ĐÃ ĐÓNG biểu hiện cũ | **TÁI MỞ ở P3** (biểu hiện mới do r7 sinh) | §8 gạch "Ref." không được gắn nhãn r6 như hai gạch bên cạnh (Hướng 7) |
| `hop-dong-dong-bang-thieu-neo` (l1 P2, l2 P1) | ĐÃ ĐÓNG trong phạm vi lời khai | **TÁI MỞ ở P2** (biểu hiện mới do r7 sinh) | Descriptor/miễn trừ/closure-trong-bytes vẫn đúng (Hướng 3 b, c); biểu hiện mới là vế review mới trỏ vào định nghĩa subagent NGOÀI bytes băm và NGOÀI kho (Hướng 3 a) |
| `objective-dong-nhat-cu-phap-voi-danh-tinh` (l2) | ĐÃ ĐÓNG | GIỮ NGUYÊN | hàng `objective` giống byte |
| `bang-duong-phan-loai-sai` (l1, l3) | ĐÃ ĐÓNG biểu hiện cũ | GIỮ NGUYÊN | §2 giống byte; hunk 1741e0a→89fc4fa đo lại 13/19, 4 hunk (t131×2, t139, t192) |
| `trang-thai-q3-chua-dong-bo` (l1) | ĐÃ ĐÓNG | GIỮ NGUYÊN | §3 Q3 và gạch §10 Q3 giống byte |
| tiền đề lượt 6 về #677 ("Điều kiện người giữ 0 áp cho mọi lease giao write set, nên sự xuất hiện lease #677 trong snapshot mới cũng chặn cấp", `luot6/VERDICT.md:232`) | chấp nhận (không phải lớp) | **TIỀN ĐỀ ĐÃ MẤT**: lease #677 nay hết hạn trong khi PR mã #689 chưa land ⇒ điều kiện (1) thôi chặn | Hướng 6 ⇒ lớp mới `thu-tu-677-bo-ngo-o-dieu-kien-cap` |

Tín hiệu hội tụ §12 (:1043–1056): U (lớp mở cuối lượt 6) = ∅ ⇒ tỷ lệ `N/A`. Lớp mới ở lượt 7: 3. Lớp tái mở: 2.
`hop-dong-dong-bang-thieu-neo` nay có mặt ở lượt **1, 2, 7** ⇒ ba lượt khác nhau ⇒ theo :1054–1056 "đòi xem lại cách
làm tại checkpoint" (phương án B ở CHI TIẾT là câu trả lời "cách làm" cho vế review). `so-do-nen-khong-khop`: lượt 1, 7.
Bảng nối slug cho lần tái mở `hop-dong-dong-bang-thieu-neo`: nguồn = lượt 2 P1 "closure nằm ngoài bytes băm", phản chứng
"hai lease khác `required_checks` cùng một băm"; biểu hiện r7 = một vế của closure mà nghĩa (model/effort/prompt của
reviewer) nằm trong tệp ngoài bytes băm và ngoài kho, không ghim ⇒ "hai lượt review khác định nghĩa reviewer cùng một băm".
Cùng nguyên nhân (một phần nghĩa của hợp đồng đóng băng không neo vào thứ bị băm), nên KHÔNG đặt slug mới (§8.3: không đổi
khoá để xoá lần tái diễn). Người điều phối có thể bác việc nối này — nếu bác thì hạng P2 và phương án giữ nguyên, chỉ
bộ đếm §12 đổi.

## BẢNG LỚP

| slug lớp | hạng | biểu hiện | phương án | phép kiểm / giới hạn |
|---|---|---|---|---|
| `thu-tu-677-bo-ngo-o-dieu-kien-cap` | **P2** | §10 dòng 603–608 (+ `depends_on` "Ngoài bốn điều kiện, xem §10"): r7 đo được nhánh #677 chưa land đổi `ops/lease_publish_test.py`, nhưng (i) dán nguồn thứ tự là "lời khai trong commit `6112b89`" (commit vắng khỏi kho) trong khi master có quyết định chủ kho "Sau #676: #677 rồi #678" (đặc tả #677 r7 §3 Q10, §9) và PR mã #689 còn lượt codex cuối (Q15); (ii) khẳng định "Không phải điều kiện Q8" mà không trích Q8, trong khi 6/6 biên nhận wp678 trên master tóm Q8 là "cap sau khi lease cua #687 va #677 nha"; (iii) bốn điều kiện cấp cho qua, điều kiện (4) chỉ dời nền với #687 | HINT nhóm 1: dẫn nguồn master; hạ "không phải điều kiện Q8" thành chưa đo; thêm chốt thi hành Q4 — trước khi cấp hỏi chủ kho thứ tự `wp678` ↔ #677, chưa có câu trả lời bền ⇒ không cấp; #677 land trước ⇒ dời nền như (4) | Kiểm: §10 dẫn `ops/specs/dot-bien-l-bien-cong-khai-r7.md`; hồ sơ cấp lease có câu trả lời bền của chủ kho. Giới hạn: nguyên văn Q8 (comment 5888631719), trạng thái live PR #689, nhánh `8e630c0` và lease #677/#687: KHÔNG ĐO ĐƯỢC từ `$R` |
| `hop-dong-dong-bang-thieu-neo` (TÁI MỞ) | **P2** | `required_checks` nay ràng `claude-opus-5-5` + `effort max` (r6 không ràng model/effort vào closure); đường chạy r7 chọn (subagent trong phiên) không có nguồn đo runtime cho hai thứ ấy theo tiền lệ kho; định nghĩa subagent quyết định chúng nằm ngoài kho và ngoài bytes băm, sha256 chỉ được ghi như phép đo 12:33Z, không như điều kiện | HINT nhóm 2 (phương án A): ghi chú dưới closure — ghim sha256 định nghĩa, khai `KHONG_do_duoc` cho model/effort thực tế, tiêu chí đạt (a)–(d). Phương án B (không vá bằng chữ): chạy review qua `launcher.py run` + `claude -p --output-format json` để có `modelUsage` + `session_run_id` (khi `claude` CLI trong container đã xác thực) | Kiểm: biên nhận lượt review thi hành có đủ (a)–(d); sha256 định nghĩa = `e225b81c…`. Giới hạn: phương án A làm tiêu chí QUYẾT ĐỊNH ĐƯỢC, không làm model/effort ĐO ĐƯỢC; hiệu lực thật của khoá frontmatter `effort` với subagent: KHÔNG ĐO ĐƯỢC |
| `q10-he-qua-mat-nhan-dien-giai` | P3 | §3 Q10 dòng 183–185 "Hệ quả: …" đứng không nhãn trong mục "Quyết định", trong khi thân comment 5911243074 gắn đoạn tương ứng nhãn "diễn giải của phiên agent, không phải lời chủ kho" | HINT nhóm 3 | Kiểm: dòng "Hệ quả" mang nhãn diễn giải |
| `dong-reviewer-loi-khai-rong-hon-do` | P3 | dòng 26: (i) "phiên mới" cho subagent chạy **trong** phiên điều phối; (ii) "validator bác `same_provider_approved`" khi validator chỉ bác nếu biên nhận TỰ KHAI `che_do` (ca D qua); (iii) "PROTOCOL §8.1 dành [`advisory_review`] cho ChatGPT Web" khi :715–716 chỉ giới hạn ChatGPT Web ở mức ấy | HINT nhóm 4 | Kiểm: `B._thieu` ca A/B/C/D (Hướng 2) |
| `so-do-nen-khong-khop` (TÁI MỞ) | P3 | §8 gạch "Ref." (dòng 440–447) trình bày số r6 (511/512, "`refs/replace` **hiện có** 0 ref") như hiện tại sau khi §8 mở đầu nói r7 đã đo lại ref; §10 dòng 593–594 giữ lý do r6 ("đường đọc MCP") cho "KHÔNG ĐO ĐƯỢC" băm #682 dù r7 tự khai đọc được #682 qua REST — hai chỗ sót của cùng một lượt gắn nhãn r7 | HINT nhóm 5 | Kiểm: mọi số r6 trong §8/§10 mang nhãn r6/lịch sử |

## BẢNG SĂN

Thư mục đo (đều tạo bằng `mktemp -d -p "$R"`): `do.hFqv` (diff r6/r7), `bn2.9j36` (bản sao chạy validator), `adg.VSn8`
(clone đo `ai-dang-giu`, origin = `kho.git` cục bộ), `suite.Vcu0` (suite hai vế), `hint.hxDv` (script sinh HINT),
`tmp.637bhzP2xt` (thân Q10), `tmp.QkXkZ5mhaH` (dry-run đầu), `tmp.b0Oxp1BSoY` (dry-run cuối), `apthat.mz3M` và
`apthat2.gOia` (áp thật trước/sau đổi slug). Không dùng `bn.rwyZ1h`, `gone.vTc1Kh`, `work.VWRXCE`, `goi-dut-1`
của lượt bị cắt. Công cụ: Python 3.11.15, PyYAML 6.0.1, git 2.43.0 (`git --version`), shellcheck 0.9.0, actionlint 1.7.7,
GNU patch 2.7.6. Chín hướng: 7 gợi ý + 2 tự thêm (8, 9).

```
HƯỚNG 1: Phạm vi thay đổi r6 → r7
  giả thuyết : r7 đổi lén byte kỹ thuật (A*, write set, closure ngoài vế review) ngoài phạm vi Q10.
  lệnh       : git -C kho.git show 423b4ba:ops/specs/lease-id-ep-kieu-yaml-r6.md > r6.master.md   (sha256 d1f9dd79…, cmp == SPEC-r6.md)
               git -C kho.git show 088511f:ops/specs/lease-id-ep-kieu-yaml-r7.md > r7.md          (cmp == SPEC.md)
               diff -u r6.master.md r7.md ; so hunk với $R/r6-r7.diff (bỏ 2 dòng tiêu đề) ; git diff --no-index --numstat
               python: tách theo tiêu đề `## `, so từng mục; tách hàng bảng `| k | v |`, so từng hàng;
               git diff --no-index --word-diff=plain trên phần chuẩn tắc của hàng `depends_on`
  output     : hunk KHỚP `r6-r7.diff`; numstat `63 16` ⇒ 79 dòng đổi, 7 hunk.
               GIỐNG byte: §1, §2, §5, §6 (muc_tieu), §7 (A1–A10), §9, Phụ lục A.
               KHÁC: header, §3 (chỉ THÊM Q10, 0 dòng `-`), §4 (chỉ câu tự tham chiếu tên tệp r6→r7; danh sách write set giữ),
               §8 (thêm nhãn r7), §10 (thêm hai gạch r7).
               Hàng GIỐNG byte: schema_version, packet_id, packet_issue, objective, review_class, risk, executor, environment,
               spec_hash, change_policy_sha, effective_write_set, effective_review_class, land_obligations.
               Hàng KHÁC: revision, thay_the_cho, mission_issue, nguon_cap_viec (dòng dõi), reviewer, required_checks (Q10),
               depends_on, nền nghiệm thu (số đo). Word-diff phần chuẩn tắc `depends_on`: đúng HAI chỗ thêm — nhãn
               "r7 chỉ đổi điều kiện (3) và số đo" và mệnh đề "từ r7 (Q10), đó là revision 7, review sạch bằng lượt Opus…".
               Mới hoàn toàn: bảng "Thay đổi so với r6", đoạn "Miễn trừ vẫn áp cho r7", "Ghi chú r7 về gate land".
  kết luận   : KHÔNG PHẢI LỖI về byte kỹ thuật. Ghi chú gate land là chuẩn tắc MỚI nhưng chỉ nhắc lại PROTOCOL :681–682 (Hướng 2).
               Điều kiện cấp (1), (2), (4) và thứ tự Q8 giữ nguyên byte — hệ quả của điều đó xét ở Hướng 6.
```

```
HƯỚNG 2: Mức assurance và gate land
  giả thuyết : (a) `review_deferred` sai với `bien_nhan_v2._thieu`/PROTOCOL cho review cùng họ bằng subagent; (b) số dòng trích sai;
               (c) gate land r7 mô tả mâu thuẫn `required_checks`, hoặc là ngõ cụt.
  lệnh       : đọc PROTOCOL :558–699 và bien_nhan_v2 :472–515, :640–797 trên cay-kho (PROTOCOL + bien_nhan_v2 giống 423b4ba:
               `git diff --quiet 423b4ba HEAD -- docs/PROTOCOL_DA_PHIEN.md ops/bien_nhan_v2.py` rc=0).
               Bản sao `bn2.9j36` (`cp -a cay-kho`), `PYTHONDONTWRITEBYTECODE=1 python3 thu_assurance.py` gọi `B._thieu(d)` trên
               10 biên nhận thử (`PROVIDER_NGUON_HONG = None`; hợp đồng `anthropic_claude` = surface {claude_code, claude_code_cli},
               transport {machine/local}).
               Khảo sát 200 biên nhận: `grep -h '^assurance:'` VÀ `grep -h '^assurance_dat:'` (validator đọc cả hai, :711).
               grep 'cross_approved\|human_audited\|assurance' .github/workflows/*.yml ; ops/*.py .claude/dev/*.py (bỏ *_test.py)
  output     : số dòng: :562 mục 1, :563–564 mục 2, :565–567 mục 3, :568 mục 4, :652, :658, :662–663, :681–682, :715–716 của
               PROTOCOL và :703, :709–726 (:725 chuỗi "dùng `review_deferred`"), :734–737, :793–796 của bien_nhan_v2 — ĐÚNG nội
               dung r7 gán cho chúng.
               A subagent tự khai `che_do` + same_provider_approved        ⇒ 1 lỗi "…dùng `review_deferred`…"
               B subagent tự khai + review_deferred                        ⇒ 0 lỗi
               C subagent tự khai + session_run_id + phien_doc_lap:true    ⇒ 1 lỗi (tự khai subagent thắng bằng chứng phiên)
               D KHÔNG khai `che_do`, có session_run_id, same_provider_app. ⇒ 0 lỗi   ← validator KHÔNG tự phát hiện subagent
               E không che_do, không run id/phien_doc_lap, same_provider   ⇒ 1 lỗi
               F cross_approved, executor claude                           ⇒ 3 lỗi, gồm "hai bên cùng họ model `claude`"
               G mô hình khai human_audited                                ⇒ 1 lỗi "…là mức của NGƯỜI audit…"
               H advisory_review / I nhãn tuỳ ý `opus_approved`             ⇒ 0 lỗi (validator không kiểm từ vựng mức)
               J người `human/manual_audit/human`, phien_doc_lap, human_audited ⇒ 0 lỗi
               Kho: 200 biên nhận. `human_audited`: **4**, đều ở khoá `assurance_dat`: `cai-cong-cu-sigpipe-r2-human-audit`,
               `plat-m4-human-audit-ducthangho`, `r330-rig-quyet-mau-audit-nguoi`, `slice-b-c-human-audit-ducthangho`.
               [SỬA TRONG LƯỢT: bản nháp ghi "0" vì chỉ grep `^assurance:` — khoá hẹp hơn khoá validator đọc; đo lại bằng cả hai.]
               `review_deferred` 3, trong đó 2 là review Claude subagent (`phan-bien-quy-trinh-review-{1,2}-claude-verdict.receipt.yaml`,
               `che_do: subagent_trong_phien_dieu_phoi`) ⇒ tiền lệ khớp lựa chọn r7. `advisory_review` 16, trong đó 13 là
               `anthropic_claude`. Workflow đọc nhãn assurance: **0** tệp; mã không-test đọc: chỉ `ops/bien_nhan_v2.py`,
               `.claude/dev/launcher.py` ⇒ không cổng máy nào đòi đích danh `cross_approved` cho land.
  kết luận   : (a) `review_deferred` cho lượt subagent: KHÔNG PHẢI LỖI (validator + tiền lệ + PROTOCOL :568, :661–663).
               (b) số dòng: KHÔNG PHẢI LỖI.
               (c) gate land: KHÔNG PHẢI LỖI — r7 nói đúng :681–682 ("hết quota mà chưa có human thì pause"), không mâu thuẫn
               `required_checks` (review Opus là check; human audit là land obligation; không vế nào tự cho land). Đường
               `human_audited` có tiền lệ thật (PR #693: `provider: human`, `surface: manual_audit`, `transport: human`,
               `phien_doc_lap: true`, `nguoi_audit: ducthangho`, `ai_dang_comment_ky: chu_kho_tu_dang`) và không cổng máy nào chặn
               ⇒ không phải ngõ cụt.
               LỖI P3 (một biểu hiện của lớp `dong-reviewer-loi-khai-rong-hon-do`): câu "Chạy bằng subagent trong phiên điều phối
               thì validator bác `same_provider_approved`" rộng hơn phép đo — validator chỉ bác khi biên nhận TỰ KHAI `che_do`
               chứa "subagent" (A, C) hoặc thiếu bằng chứng phiên (E); ca D qua. Mức `review_deferred` là nghĩa vụ khai trung thực.
```

```
HƯỚNG 3: Closure — vế review mới, các giá trị khác, miễn trừ #682
  giả thuyết : (a) vế review mới không kiểm được; (b) giá trị closure khác bị đổi; (c) miễn trừ không phủ r7.
  lệnh       : (b) Hướng 1. (c) git -C kho.git diff --name-only 89fc4fa 423b4ba | wc -l ; … | grep -ci 'polic\|closure\|dispatcher' ;
               git -C kho.git diff 89fc4fa 423b4ba | awk '/^\+\+\+ /{f=$2} /^\+[^+]/ && tolower($0) ~ /change_policy|policy canonical|closure policy/ {print f}' | sort | uniq -c
               (a) sha256sum ~/.claude/agents/review-opus-max.md (CHỈ ĐỌC, ngoài $R; in băm + 4 khoá frontmatter, không in thân);
               awk khối `model_reviewer_identity` của `phan-bien-quy-trinh-review-2` và `wp541-review-4`; grep `kiem_ket_qua`.
  output     : (b) mọi giá trị closure ngoài `required_checks` GIỐNG byte.
               (c) 61 tệp đổi; 0 tên khớp; nội dung: 16 dòng thêm nhắc `change_policy`/`policy canonical`/`closure policy`, TẤT CẢ
               thuộc hồ sơ wp678 (spec r2–r6 và verdict lượt 3, 4, 6) ⇒ không có policy closure canonical mới (mạnh hơn phép lọc tên
               r7 tự khai giới hạn). Câu miễn trừ trong r7 (không đổi từ r3): "chỉ wp678, mọi revision từ r3, … đổi bất kỳ giá trị
               closure ⇒ revision mới, spec_hash mới, lease mới; write set không mở rộng" ⇒ r7 là revision ≥ r3, đổi closure bằng
               revision mới, write set giữ ⇒ phủ. Thân #682 không có trong $R ⇒ đối chiếu nguyên văn miễn trừ: KHÔNG ĐO ĐƯỢC.
               (a) định nghĩa subagent: 1175 byte, sha256 e225b81cf2fbdd0f05a54a689cac17db8972b2f8c0684a0a30931875cd4b792c (KHỚP r7),
               mtime 2026-09-29 23:07:37Z, frontmatter `model: claude-opus-5-5`, `effort: max`, `tools: Read, Write, Edit, Bash, Grep, Glob`.
               Đó là CẤU HÌNH. PROTOCOL :710–711 "Ghi cặp Executor–Reviewer thực tế: provider, model, effort … và nguồn đo. Cấu
               hình yêu cầu không phải runtime evidence." Tiền lệ kho cho review Claude chạy trong phiên:
               `phan-bien-quy-trinh-review-2`: "ID MODEL CỤ THỂ — không đường nào trong phiên trả model đang phục vụ";
               `wp541-review-4`: `model_evidence: khong_do_duoc`, `effort: KHONG_KHAI`. Vị từ đo model của kho
               (`.claude/dev/chon_reviewer.py` `kiem_ket_qua`, :115–133) đòi `modelUsage[*].canonicalModel` của
               `claude --output-format json` — lượt subagent không sinh JSON ấy. Định nghĩa subagent nằm NGOÀI kho; r7 ghi sha256 như
               PHÉP ĐO lúc 12:33Z, không như điều kiện (không có "lệch ⇒ DỪNG").
  kết luận   : (b), (c): KHÔNG PHẢI LỖI. (a): LỖI P2, lớp `hop-dong-dong-bang-thieu-neo` (TÁI MỞ, xem bảng nối slug ở ĐỐI CHIẾU).
```

```
HƯỚNG 4: Nguyên văn Q10
  giả thuyết : trích Q10 trong r7 lệch thân comment 5911243074; hoặc r7 nâng diễn giải của agent thành lời chủ kho.
  lệnh       : python: json.load(q10-readback.json)['body'].encode('utf-8') ⇒ sha256, len; tách SPEC.md dòng 176–181, bỏ tiền
               tố "  >" (kèm 1 dấu cách nếu có), so TỪNG dòng với các dòng của thân; kiểm khối liên tục; đếm thực thể HTML.
  output     : thân 1805 ký tự / 2151 byte, sha256 69cc35b179d4c9f94459c2d874156f8f303fb32e67b90c81e0f2cd617bc22d2f (KHỚP r7).
               6/6 dòng trích KHỚP byte (dòng thân #6, rỗng, #8, #9, #10, #11); khối liên tục có trong thân: True.
               Thực thể `&#39; &#34; &gt; &lt; &amp; &quot;` trong thân: 0 ⇒ không lớp chuẩn hoá nào can thiệp phép so.
               `id` 5911243074, `created_at` 2026-09-30T12:24:28Z, `author_association` OWNER,
               `performed_via_github_app.slug` = `claude` — khớp lời khai "phiên agent đăng HỘ".
               Dòng thân KHÔNG trích: #13 "**Hệ quả (diễn giải của phiên agent, không phải lời chủ kho):**" và ba gạch #14–#16.
               r7 dòng 183–185 "Hệ quả: chỉ đổi reviewer lượt thi hành, … Q10 không nới gate land." đứng trong §3 "Quyết định",
               KHÔNG mang nhãn mà chính thân comment gắn cho đoạn tương ứng.
  kết luận   : trích nguyên văn: KHÔNG PHẢI LỖI. Nhãn đoạn "Hệ quả": LỖI P3 (lớp `q10-he-qua-mat-nhan-dien-giai`).
```

```
HƯỚNG 5: Phép đo lúc soạn (đo lại trên kho.git, offline)
  lệnh + output (G = git -C $R/kho.git):
   1. G diff --stat 89fc4fa 423b4ba -- ops/lease_publish.py ops/lease_publish_test.py ⇒ 0 byte, rc=0          KHỚP
   2. G diff --quiet (cùng phạm vi) ⇒ rc=0                                                                     KHỚP
   3. G merge-base --is-ancestor 89fc4fa 423b4ba ⇒ rc=0                                                        KHỚP
   4. G log --diff-filter=A --format=%H 423b4ba -- ops/specs/lease-id-ep-kieu-yaml-r6.md ⇒ 03a7219c9f3d…386cb;
      G log --format=%H -1 423b4ba -- <tệp> ⇒ 03a7219c9f3d…386cb; số commit chạm tệp: 1                        KHỚP
   5. G show 423b4ba:<r6> | sha256sum ⇒ d1f9dd79…244c                                                          KHỚP
   6. G diff --name-only 89fc4fa 423b4ba | wc -l ⇒ 61; tên khớp polic|closure|dispatcher ⇒ 0                    KHỚP
   7. G log --first-parent --merges 89fc4fa..423b4ba ⇒ 7 merge (#696, #691, #693, #681, #684, #679, #683), 0 của #687 KHỚP
   8. G diff --numstat 1741e0a 89fc4fa -- ops/lease_publish_test.py ⇒ 13 19; 4 hunk: 2 trong t131, 1 t139, 1 t192;
      ops/lease_publish.py 1741e0a↔89fc4fa diff --quiet rc=0                                                   KHỚP
   9. G merge-base --is-ancestor 03a7219 423b4ba ⇒ rc=0 ("03a7219 là tổ tiên của origin/master")               KHỚP
  10. 44620e8 = "Merge PR #684: spec(#677) DOT-BIEN-L-BIEN-CONG-KHAI r1–r7", tổ tiên 423b4ba rc=0              KHỚP
  11. 423b4ba committer 2026-09-30T09:30:11Z < "đầu 8e630c0, 09:48:22Z, merge-base 423b4ba" ⇒ thứ tự thời gian nhất quán;
      bản thân 8e630c0: `git cat-file -t` ⇒ "Not a valid object name" ⇒ KHÔNG ĐO ĐƯỢC (+596/−15 cũng vậy)
  12. 6112b89: vắng khỏi mirror ⇒ KHÔNG ĐO ĐƯỢC; lease #687/#677/wp678: `ls-tree` mọi 6 nhánh mirror ⇒ 0 tệp ⇒ hạn
      11:50Z/11:45Z/10:48Z: KHÔNG ĐO ĐƯỢC. `git log --format=%s 423b4ba | grep -c '#689'` ⇒ 0 (PR #689 chưa từng land).
  13. Cơ chế `ai-dang-giu` (tái lập offline, `adg.VSn8`, clone `-b master` từ kho.git, origin = kho.git cục bộ):
      so tên+OID ls-remote/for-each-ref ⇒ 0 dòng lệch (6/6 — ảnh mirror, KHÔNG phải 458 của máy chủ);
      `ai-dang-giu ops/lease_publish.py` và `…_test.py` ⇒ rc=0, "NGƯỜI_GIỮ 0: không có";
      thêm nhánh cục bộ `nhanh-gone` có upstream `[gone]` ⇒ rc=12, "CHAN [12]: KHÔNG_XÁC_ĐỊNH: nhanh-gone khai upstream
      không có ref" ⇒ lời giải thích (b) của r7 đúng CƠ CHẾ (mã `ops/lease_publish.py` :383–399). Số 458/458 và kết quả
      máy chủ: KHÔNG ĐO ĐƯỢC (cần mạng) — r7 gắn nhãn đúng: tách "lời khai phiên điều phối" khỏi "phiên soạn r7 tự đo".
  14. sha256 định nghĩa subagent e225b81c… ⇒ KHỚP (Hướng 3).
  15. Kích thước/băm §8 giữ từ r6, đo trên 89fc4fa và 423b4ba: `ops/lease_publish.py` 2206 dòng, sha256 dd17b94cb880…4f83
      (đủ 64 ký tự khớp); `ops/lease_publish_test.py` 10502 dòng (10508 trên 1741e0a); 187 `^@ca`; ca lớn nhất t192;
      `.claude/dev/packet_loop.py` :769–771 đòi `isinstance(v, str)` cho `lease_id`.                         KHỚP
  kết luận   : KHÔNG PHẢI LỖI ở các phép đo làm lại được. Phần không làm lại được đã được r7 gắn nhãn đúng.
```

```
HƯỚNG 6: Tương tác #677 — điều kiện cấp, dời nền, cửa sổ hai writer
  giả thuyết : r7 biết nhánh thi hành #677 chưa land đổi một tệp write set, nhưng để điều kiện cấp mở, dán nhãn bằng chứng
               thứ tự yếu hơn bằng chứng có trên master, và khẳng định "không phải điều kiện Q8" mà không đo Q8.
  lệnh       : grep -n 'Q5\|Q10\|Q15\|#678\|#689' ops/specs/dot-bien-l-bien-cong-khai-r7.md (cay-kho = 423b4ba + r7);
               git -C kho.git log -1 --format='%h %P %s' 44620e8 ; merge-base --is-ancestor 44620e8 423b4ba ;
               grep -n '677' ops/reviews/wp678-spec-review-*-codex-verdict.receipt.yaml ops/land/pr679-wp678-land-evidence.yaml ;
               đọc PROTOCOL :148–149, :255–259 ; git cat-file -t 8e630c0 / 6112b89 trên kho.git ; đọc luot6/VERDICT.md:232.
  output     : (1) Đặc tả #677 r7 — TRÊN MASTER từ 44620e8 (Merge PR #684, tổ tiên 423b4ba, rc=0) — mục "## 3. Quyết định của
               chủ kho (29-09-2026 …)", dòng 276: "**Q10** | … Sau #676: #677 rồi #678." và §9 dòng 377: "Thứ tự "#677 trước
               #678" (Q7/Q10) **không** nói gì về #687". Dòng 280 (Q15): "PR #689 (mã) giữ trần 2 lượt codex. Lượt 1 đã dùng
               (`11f73ac`, 0/5/3). Lượt 2 … là lượt cuối" ⇒ tại 29-09 #677 có PR mã #689 chưa land, còn lượt codex cuối; codex
               hết quota tới 03-10 (Q10 của wp678). Dòng 271 (Q5): "≤ 300 dòng thêm … Vượt thì DỪNG và hỏi", mà r7 §10 khai
               nhánh #677 là +596/−15 (không đo được ở đây).
               (2) r7 §10 dẫn cho thứ tự CHỈ "Commit `6112b89` ghi *"chủ kho chốt #677 đi trước"* (lời khai trong commit)" — commit
               vắng khỏi kho.git — rồi "phiên soạn r7 không quyết". Bằng chứng mạnh hơn (bảng quyết định chủ kho trong một đặc tả
               đóng băng ĐÃ Ở MASTER, mà chính r7 §10 dẫn PR #684, `44620e8`) không được dẫn.
               (3) Bốn điều kiện cấp (không đổi byte từ r6) chỉ chờ lease #687; điều kiện (4) chỉ dời nền khi **#687** land trước.
               #677 land trước ⇒ r7 cấp trên nền `89fc4fa` dù master đã đổi `ops/lease_publish_test.py` (bất đối xứng mà chính
               lý lẽ của điều kiện (4) — "không cấp trên nền cũ" — bác).
               (4) PROTOCOL :255–259: land authority tách khỏi executor lease ⇒ PR #689 vẫn có thể land trong lúc wp678 giữ
               lease; còn nếu lượt codex cuối của #689 ra finding thì #677 cần lease mới trên đúng tệp ấy ⇒ bị lease wp678 chặn
               ⇒ thứ tự "#677 rồi #678" đảo ngược mà không ai quyết.
               (5) r7 §10 viết "Không phải điều kiện Q8". Q8 KHÔNG được trích nguyên văn ở r6/r7 (khác Q10). 6/6 biên nhận wp678
               trên master (dòng 16) tóm Q8 là "cap sau khi lease cua #687 va #677 nha ops/lease_publish_test.py"; hồ sơ land
               `pr679-wp678-land-evidence.yaml:142` ghi "lease hen cap 2026-09-30T12:15Z (Q8, #682 comment 5888631719)" — mốc
               12:15Z không có trong lời tóm Q8 của r7. Nguyên văn comment 5888631719: KHÔNG ĐO ĐƯỢC từ $R.
               (6) Câu hỏi Q10 gửi chủ kho ("đủ 4 điều kiện Q8 … Làm sao?") không nhắc #677/PR #689; lựa chọn đã chọn gồm
               "rồi cấp lease". Phép đo nhánh #677 của r7 (12:28Z) đến SAU câu trả lời (12:21:07Z).
               (7) Lượt 6 chấp nhận tương tác #677 vì "sự xuất hiện lease #677 trong snapshot mới cũng chặn cấp" (luot6:232). Nay lease
               #677 hết hạn trong khi #689 chưa land ⇒ tiền đề ấy mất.
  kết luận   : LỖI P2 (lớp `thu-tu-677-bo-ngo-o-dieu-kien-cap`). Không nâng P1 vì "#677 rồi #678" có hai cách đọc (thứ tự lease —
               lease #677 đã hết hạn ⇒ đã thoả; hay thứ tự land — chưa thoả), A2 đã phủ nghĩa vụ kỹ thuật của CẢ HAI thứ tự land,
               và vế "Chủ kho audit" trước land vẫn là chốt chặn cuối. Nhưng r7 tự thấy xung đột, gọi nó là "chạm Q4", rồi để
               bốn điều kiện cấp cho qua — tức Q4 ("chủ kho xếp, packet này không tự nhảy lên trước") không có đường thi hành,
               và hai lời khai ("lời khai trong commit", "không phải điều kiện Q8") hẹp/rộng hơn bằng chứng có trong kho.
```

```
HƯỚNG 7: Nhất quán nội tại
  giả thuyết : còn chỗ coi codex là reviewer lượt thi hành; số/sha/commit tự khai lệch; nhãn r6/r7 lẫn lộn.
  lệnh       : grep -c -i 'codex\|cross-review\|cross_approved\|gpt-6' SPEC.md ; grep -o … | wc -l ; đọc §8 dòng 426–449, §10 593–594.
  output     : 18 dòng khớp, 39 lần xuất hiện từ, 30 đoạn ngữ cảnh (`grep -o '.{0,70}…{0,70}'`).
               [SỬA TRONG LƯỢT: bản nháp ghi "28" chưa đếm; đo lại.] TẤT CẢ thuộc: bảng thay đổi (cột r6), dòng dõi r1–r6,
               trích Q10, trích PROTOCOL, lịch sử lượt review. Không chỗ nào còn khai codex là reviewer lượt thi hành.
               6/6 biên nhận wp678-spec-review-*: `provider: codex`, `model_yeu_cau: gpt-6-astra` (khớp "sáu lượt … chạy bằng codex").
               §8 mở đầu (dòng 431): "**r7 chỉ đo lại nền, ref, người giữ** (12:26Z–12:28Z 30-09, ở header); số khác giữ từ r6."
               Gạch "Nền." được thêm dòng r7 + "câu dưới là số r6"; gạch "Người giữ." được thêm "Số dưới là của r6 …, nay là lịch
               sử". Gạch "**Ref.**" (dòng 440–448) KHÔNG được gắn nhãn: vẫn "máy chủ **511**, cục bộ **512**" và "`refs/replace`
               **hiện có** 0 ref; `refs/heads` có 3 ref" như số hiện tại. §10 dòng 593–594 giữ "KHÔNG ĐO ĐƯỢC (đường đọc MCP …)" cho
               băm #682, trong khi đoạn Descriptor được r7 sửa thành "từ phiên soạn r6" và §10 dòng 626–627 khai r7 đọc được #682
               qua REST — đúng mẫu "sửa một chỗ, sót chỗ thứ hai trong cùng tệp".
  kết luận   : LỖI P3 (lớp `so-do-nen-khong-khop`, TÁI MỞ). Các số/sha/commit còn lại: BẢNG ĐO, đều khớp hoặc KHÔNG ĐO ĐƯỢC có nhãn.
```

```
HƯỚNG 8 (tự thêm): Đường land có thật sự đi được khi làm đúng từng chữ r7?
  giả thuyết : r7 đòi `human_audited` mà (a) kho chưa có đường ghi mức ấy, hoặc (b) một cổng máy đòi đích danh `cross_approved`,
               hoặc (c) câu "comment do phiên agent đăng hộ không phải evidence" chặn cả cách ghi duy nhất có tiền lệ.
  lệnh       : Hướng 2 (khảo sát assurance_dat, grep workflow); đọc `ops/reviews/cai-cong-cu-sigpipe-r2-human-audit-verdict.receipt.yaml`
               :1–100; `git -C kho.git show --stat c16bec63` (PR #693).
  output     : 4 biên nhận `assurance_dat: human_audited`; tiền lệ #675: chủ kho tự đăng comment ký (`ai_dang_comment_ky:
               chu_kho_tu_dang`, phiên điều phối "KHÔNG goi add_issue_comment"), biên nhận tự khai "Danh tinh nguoi ky KHONG do
               duoc tu du lieu GitHub" và "chu ky … KHONG phai mot luot do tim; phep do la cua nam luot Codex". 0 workflow đọc nhãn.
               Q10 comment đăng qua app (`performed_via_github_app.slug: claude`) ⇒ trường ấy là dấu hiệu MỘT CHIỀU phân biệt
               đăng-qua-app với chủ-kho-tự-gõ (null không chứng minh chủ kho tự gõ).
  kết luận   : KHÔNG PHẢI LỖI — đường land qua `human_audited` đi được và ghi chú gate land của r7 khớp tiền lệ. Ghi nhận cho người
               audit (không phải finding): ở tiền lệ #675, chữ ký chủ kho dựa vào năm lượt codex đã dò tìm; ở wp678 theo r7, lượt dò
               tìm duy nhất là review Opus cùng họ (`review_deferred`), nên audit của chủ kho mang nhiều trọng lượng hơn tiền lệ.
```

```
HƯỚNG 9 (tự thêm): Lý lẽ "giữ nền 89fc4fa vì hai tệp không đổi" có đủ cho A8 khi master đã đổi tệp mà suite đọc?
  giả thuyết : 89fc4fa..423b4ba đổi `.github/workflows/ci.yml` (suite đọc nó, `ops/lease_publish_test.py:2560`),
               `ops/cai_actionlint.sh`, `ops/cai_cong_cu.sh`; suite trên hai nền có thể lệch dù hai tệp write set giống hệt.
  lệnh       : một lệnh dựng CẢ HAI vế: for pair in nen:89fc4fac… sau:423b4ba…; do git clone -q --no-hardlinks kho.git suite.Vcu0/$n;
               checkout --detach $sha; config core.abbrev 7; done ; cmp hai tệp write set giữa hai vế ; rồi mỗi vế
               `PYTHONDONTWRITEBYTECODE=1 TMPDIR=suite.Vcu0/tmp timeout 3000 python3 ops/lease_publish_test.py`
  output     : hai tệp write set GIỐNG giữa hai vế. nen: rc=0, 13:15:58Z–13:20:57Z, "lease_publish: 187/187 đạt; đã chạy=187, bỏ qua=0";
               sau: rc=0, 13:20:57Z–13:26:02Z, "lease_publish: 187/187 đạt; đã chạy=187, bỏ qua=0". Nhật ký `>>> vao`/`<<< ra`:
               561/561 ở mỗi vế. shellcheck 0.9.0, actionlint 1.7.7.
  kết luận   : KHÔNG PHẢI LỖI trên ảnh này: A8 nền 187/187 đứng vững trên cả 89fc4fa lẫn 423b4ba. Giới hạn: một lần chạy, một
               container; không chứng minh mọi thay đổi tương lai ngoài write set đều vô can — A8 đã bắt đo lại hai vế lúc thi hành.
```

## BẢNG ĐO

| khẳng định trong spec | spec khai | đo được | khớp? |
|---|---|---|---|
| sha256 r7 | 8cb02436…b707 | 8cb02436…b707 | có |
| r6: tệp, sha256 | d1f9dd79…244c | `git show 423b4ba:<r6> \| sha256sum` ⇒ d1f9dd79…244c | có |
| commit TẠO r6 (`--diff-filter=A` và `log -1`) | 03a7219c9f3d…386cb | cả hai ⇒ 03a7219c9f3d…386cb; 1 commit chạm tệp | có |
| lượt 6 approve 0 P0–P3, `assurance: cross_approved` | có | biên nhận: `so_p0..so_p3: 0`, `verdict: approve`, `assurance: cross_approved` | có |
| VERDICT lượt 6 sha256 | 9569bf0d…c18d | `luot6/VERDICT.md` và `ops/reviews/…-6-codex-verdict.md`: 9569bf0d…c18d, `cmp` khớp | có |
| sáu lượt review đặc tả chạy bằng codex `gpt-6-astra` | 6 | 6/6 biên nhận `provider: codex`, `model_yeu_cau: gpt-6-astra` | có |
| Q10: sha256 thân / số byte | 69cc35b1…2d2f / 2151 | 69cc35b1…2d2f / 2151 (1805 ký tự) | có |
| Q10: id / tạo | 5911243074 / 12:24:28Z | 5911243074 / 2026-09-30T12:24:28Z | có |
| Q10: "các dòng dưới chép từng byte" | 6 dòng | 6/6 khớp byte, khối liên tục | có |
| Q10: HTTP 200, 12:33:01Z | có | JSON không mang status/giờ đọc | KHÔNG ĐO ĐƯỢC |
| `origin/master` = 423b4ba (12:26:45Z) | 423b4ba… | mirror `master` = 423b4ba1…; giá trị live | có (mirror) / live KHÔNG ĐO ĐƯỢC |
| `diff --stat 89fc4fa 423b4ba -- 2 tệp` rỗng, rc=0 | rỗng | 0 byte, rc=0 | có |
| `diff --quiet` cùng phạm vi rc=0 | 0 | 0 | có |
| `is-ancestor 89fc4fa 423b4ba` rc=0 | 0 | 0 | có |
| 61 tệp đổi, 0 tên chứa polic/closure/dispatcher | 61 / 0 | 61 / 0; nội dung: 16 dòng, tất cả hồ sơ wp678 | có |
| 7 merge first-parent, 0 của #687 | 7 / 0 | 7 / 0 | có |
| test 1741e0a→89fc4fa +13/−19, 4 hunk (t131×2, t139, t192) | có | 13 19; hunk ở t131, t131, t139, t192 | có |
| 03a7219 là tổ tiên origin/master | có | rc=0 | có |
| đặc tả #677 vào master (PR #684, 44620e8) | có | 44620e8 = Merge PR #684 r1–r7, tổ tiên 423b4ba | có |
| định nghĩa subagent sha256 | e225b81c…792c | e225b81c…792c (1175 byte, mtime 29-09 23:07:37Z) | có |
| định nghĩa subagent "không có trong kho" | không | `grep -rln review-opus-max cay-kho --exclude-dir=.git` ⇒ chỉ `ops/specs/lease-id-ep-kieu-yaml-r7.md`; `find … -name 'review-opus-max*'` ⇒ 0 | có |
| số dòng PROTOCOL :562, :563–564, :565–567, :568, :652, :658, :662–663, :681–682, :715–716 | nội dung như r7 gán | đọc từng dòng trên cay-kho (= 423b4ba) | có |
| số dòng bien_nhan_v2 :703, :709–726, :725, :734–737, :793–796 | nội dung như r7 gán | đọc + ca A–G | có |
| "validator bác same_provider_approved khi chạy subagent" | có | chỉ khi TỰ KHAI `che_do` (ca A, C); ca D qua | không (P3) |
| "PROTOCOL §8.1 dành advisory_review cho ChatGPT Web" | có | :715–716 giới hạn ChatGPT Web ở mức ấy, không giới hạn tên | không (P3) |
| "phiên mới không mang context executor" (subagent) | phiên mới | subagent chạy TRONG phiên điều phối (chính r7 viết vậy vài câu sau) | không (P3) |
| clone mới: 458/458, 0 lệch; `NGƯỜI_GIỮ 0` rc=0 | có | cơ chế tái lập trên mirror (6/6, rc=0); số máy chủ | cơ chế có / số KHÔNG ĐO ĐƯỢC |
| kho chính: `CHAN [12]` rc=12 vì upstream `[gone]` | có | tái lập nhánh `[gone]` ⇒ rc=12 đúng thông điệp | có (cơ chế) |
| hạn lease #687 11:50Z / 11:45Z; #677 exec-1…5 10:48Z | có | lease vắng khỏi mirror | KHÔNG ĐO ĐƯỢC |
| nhánh #677 `8e630c0`, 09:48:22Z, merge-base 423b4ba, +596/−15 | có | object vắng; thời gian nhất quán với 423b4ba 09:30:11Z | KHÔNG ĐO ĐƯỢC |
| commit `6112b89` ghi "chủ kho chốt #677 đi trước" | có | object vắng | KHÔNG ĐO ĐƯỢC |
| "#677 … Không phải điều kiện Q8" | không phải | Q8 không trích; 6/6 biên nhận tóm Q8 có #677 | KHÔNG ĐO ĐƯỢC, mâu thuẫn trong kho (P2) |
| "Commit 6112b89 … (lời khai trong commit)" là nguồn thứ tự | chỉ commit | master có Q10 của #677 "Sau #676: #677 rồi #678" | không (P2) |
| §8 "Ref.": máy chủ 511, cục bộ 512, `refs/replace` hiện có 0 | hiện tại | số r6; r7 đo 458/458 | không (P3, nhãn) |
| §8 kích thước 2206 / 10502 (10508 trên 1741e0a), 187 ca, t192 | có | 2206 / 10502 / 10508 / 187 / t192 | có |
| sha256 `ops/lease_publish.py` trên master | dd17b94c…4f83 | dd17b94c…4f83 | có |
| suite nền 187/187 rc=0 bỏ qua 0 | có (08:0xZ 29-09) | 187/187 rc=0 bỏ qua 0 trên 89fc4fa VÀ 423b4ba (13:15–13:26Z 30-09) | có |
| miễn trừ: "chỉ wp678, mọi revision từ r3" | có | thân #682 vắng khỏi $R; câu trong r7 giống r3–r6 | KHÔNG ĐO ĐƯỢC (nguyên văn) |
| Q10 trả lời 12:21:07Z theo transcript | có | thân comment ghi đúng mốc ấy; transcript vắng | có (theo thân) |

## CHI TIẾT TỪNG LỚP

### `thu-tu-677-bo-ngo-o-dieu-kien-cap` — P2 (mới)
- Finding: F7-1 (§10 dòng 603–608, và con trỏ trong `depends_on`).
- Nguồn: lượt 7 trên `088511f`, spec sha256 `8cb02436…`.
- Biểu hiện: (i) nguồn thứ tự yếu hơn bằng chứng trên master; (ii) "không phải điều kiện Q8" không có phép đo, mâu thuẫn 6
  biên nhận trên master; (iii) bốn điều kiện cấp cho qua một xung đột Q4 mà r7 tự đo được; điều kiện (4) bất đối xứng.
- Vì sao P2 không P1: hai cách đọc thứ tự; A2 phủ kỹ thuật cả hai thứ tự land; audit chủ kho trước land là chốt cuối.
  Nếu chủ kho xác nhận "#677 rồi #678" là thứ tự LAND thì cấp lease theo r7 chính là "tự nhảy lên trước" (Q4) — lúc ấy lớp này
  phải nâng P1.
- Cách vá chung: không vá bằng suy luận; thi hành Q4 bằng một câu hỏi bền cho chủ kho trước khi cấp, và cho #677 cùng luật
  dời nền với #687. HINT nhóm 1 (chỉ sửa §10; hàng `depends_on` đã trỏ sang §10). Nếu người điều phối muốn nêu cả trong
  hàng `depends_on`, đó là một hunk thêm trên dòng 27 (không đưa vào HINT vì dòng ấy liền kề dòng 26 của nhóm 4 — hai nhóm
  sẽ chồng ngữ cảnh).
- Phép kiểm đóng lớp: §10 dẫn nguồn master; hồ sơ cấp lease `wp678` có câu trả lời bền của chủ kho về thứ tự với #677; nếu
  #677 đã land thì có revision dời nền trước cấp. Giới hạn: nguyên văn Q8 chỉ đóng được bằng readback comment 5888631719
  (như đã làm cho Q10) — `KHÔNG ĐO ĐƯỢC` từ `$R`.

### `hop-dong-dong-bang-thieu-neo` — P2 (TÁI MỞ; lịch sử: lượt 1 P2, lượt 2 P1, đóng ở lượt 3)
- Finding: F7-2 (`required_checks` dòng 54 + dòng reviewer 26).
- Biểu hiện mới do r7 sinh: vế review của closure ràng model/effort mà (i) nghĩa của nó nằm trong tệp ngoài kho và ngoài bytes
  băm (định nghĩa subagent, chỉ ghi sha256 như phép đo); (ii) model/effort thực tế của lượt subagent không có nguồn đo trong
  kho (tiền lệ + vị từ `kiem_ket_qua`); PROTOCOL :710–711 không nhận cấu hình làm runtime evidence.
- Hệ quả: người kiểm closure lúc land không có tiêu chí quyết định cho vế ấy ngoài lời tự khai; và "hai lượt review khác định
  nghĩa reviewer cùng một `spec_hash`" là khả dĩ — đúng hình phản chứng lượt 2.
- Cách vá chung, hai phương án:
  A (HINT nhóm 2): ghi chú dưới closure, ghim sha256 định nghĩa, khai `KHONG_do_duoc` cho model/effort thực tế, tiêu chí đạt
  (a)–(d). Rẻ, không đổi giá trị closure.
  B (xem lại cách làm, theo §12 :1054–1056 vì lớp đã ở ba lượt): chạy review lượt thi hành bằng `launcher.py run` bọc
  `claude -p --model claude-opus-5-5 --output-format json` trong sandbox — có `modelUsage.canonicalModel` (đo model bằng máy)
  và `session_run_id` (đủ điều kiện `same_provider_approved`, đúng "hạ assurance tương ứng vì cùng họ" của Q10 hơn là
  `review_deferred`). Điều kiện: `claude` CLI trong container phải xác thực được (tiền lệ `wp541-review-4` ghi có lúc KHÔNG).
- Phép kiểm đóng lớp: biên nhận lượt review thi hành có đủ (a)–(d) [A] hoặc có `modelUsage` + `session_run_id` [B].

### `q10-he-qua-mat-nhan-dien-giai` — P3 (mới)
- Finding: F7-3 (§3 Q10 dòng 183–185). Vá: HINT nhóm 3 (thêm nhãn diễn giải, giữ nguyên nội dung). Kiểm: dòng mang nhãn.

### `dong-reviewer-loi-khai-rong-hon-do` — P3 (mới)
- Finding: F7-4a/b/c (dòng 26): "phiên mới"; "validator bác" vô điều kiện; "§8.1 dành … cho ChatGPT Web".
- Vá: HINT nhóm 4 (ba thay thế trong cùng dòng; nêu nghĩa vụ tự khai `che_do` kèm tiền lệ). Kiểm: `_thieu` ca A–D.

### `so-do-nen-khong-khop` — P3 (TÁI MỞ; lịch sử: lượt 1 P2)
- Finding: F7-5a (§8 "Ref." dòng 440–447), F7-5b (§10 dòng 593–594).
- Vá: HINT nhóm 5 (gắn nhãn r6/lịch sử; nêu r7 đọc #682 qua REST mà không ghi băm). Kiểm: mọi số r6 ở §8/§10 có nhãn.

### Ghi chú cho revision 8 (không phải lớp)
- Điều kiện (3) viết "từ r7 (Q10), đó là **revision 7**" — r8 phải đổi thành revision của chính nó; công thức băm và tên tệp
  cũng vậy. HINT không động vào các chỗ ấy (thuộc việc dựng r8 của người điều phối).

## DRY-RUN HINT.patch

`$R/goi/HINT.patch`: 106 dòng, 19744 byte, sha256 `72289e06e44dda8f6d7059e3ebdbd53103ba19ac9e9c6af1b56d5ff1ef6db445`.
5 nhóm `# lop:` (thu-tu-677-bo-ngo-o-dieu-kien-cap, hop-dong-dong-bang-thieu-neo, q10-he-qua-mat-nhan-dien-giai,
dong-reviewer-loi-khai-rong-hon-do, so-do-nen-khong-khop), 6 hunk. Mỗi nhóm là một diff riêng trên bản r7 gốc, ngữ cảnh
các nhóm không chồng nhau. Sinh bằng `hint.hxDv/sinh_hint.py` (kiểm nội dung dòng cũ bằng `assert` trước khi thay).
Đường dẫn repo-relative, không tiền tố `a/`/`b/`.

Lệnh (đúng PROMPT):
```
T=$(mktemp -d -p "$R") && cp -a "$R/cay-kho" "$T/cay"
cd "$T/cay" && patch -p0 --fuzz=0 --dry-run --verbose < "$R/goi/HINT.patch"
```
Output (T=`$R/tmp.b0Oxp1BSoY`, GNU patch 2.7.6): **rc=0**; 5 lần "checking file ops/specs/lease-id-ep-kieu-yaml-r7.md";
"Hunk #1 succeeded at 604." · "Hunk #1 succeeded at 61." · "Hunk #1 succeeded at 180." · "Hunk #1 succeeded at 23." ·
"Hunk #1 succeeded at 437." · "Hunk #2 succeeded at 591." · "done". 6/6 succeeded; 0 dòng fail/fuzz/reject;
`git status --porcelain` của bản sao sau dry-run: 0 dòng.

Áp thật HINT bản CUỐI (bản sao `apthat2.gOia`, `patch -p0 --fuzz=0`): rc=0; "Hunk #1 succeeded at 191 (offset 11 lines)",
"Hunk #1 succeeded at 450 (offset 13 lines)", "Hunk #2 succeeded at 604 (offset 13 lines)" (offset do các nhóm trước chèn
dòng, không fuzz); 0 tệp `.rej`/`.orig`; `git diff --numstat` 33/10; 745 → 768 dòng. Kết quả `cmp` KHỚP byte với lần áp
trước (`apthat.mz3M`, HINT trước khi đổi tên slug nhóm 2 — hunk giống hệt, chỉ khác dòng `# lop:`), và lần áp trước ấy ==
bản kỳ vọng dựng độc lập (đọc hunk từ chính HINT.patch, áp từ dưới lên bằng Python) ⇒ True.

Nhãn bắt buộc cho người áp (PROTOCOL §8 :600–601): *"chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm
commit"*. Đây là HINT cho một ĐẶC TẢ (không phải mã); mọi thay đổi thành revision 8, phải đo lại số và băm của chính r8.

## GIỚI HẠN VÀ TOÀN VẸN
- KHÔNG ĐO ĐƯỢC từ `$R` (không mạng): thân #682 và comment Q8 5888631719; trạng thái máy chủ (458 tên, người giữ live); nhánh
  `8e630c0`, commit `6112b89`, mọi lease #677/#687; trạng thái live PR #689; hiệu lực runtime của `model`/`effort` với subagent.
- Đọc NGOÀI `$R` (chỉ đọc, không in thân): `~/.claude/agents/review-opus-max.md` (băm + 4 khoá frontmatter); `stat` inode các
  pack của `/home/user/tra-luat` để kiểm tính độc lập của mirror.
- Ghi: chỉ `$R/goi/` và các thư mục `mktemp -d -p "$R"` nêu ở BẢNG SĂN. Clone đo `adg.VSn8` (clone cục bộ mặc định) tạo
  hardlink tới pack của `kho.git` (inode 1908767, link 3 = kho.git + cay-kho + adg) — pack bất biến, không ghi nội dung;
  clone suite dùng `--no-hardlinks`.
- `cay-kho` cuối lượt: HEAD `088511f1…`, tree `1cadf3bf…`, `status --porcelain --ignored` 0 dòng, diff/index sạch;
  `.git/index` giữ mtime 12:41:43Z; chỉ mtime thư mục `.git/` đổi (13:27:06Z, tệp khoá tạm của `git status`). Theo §8.2,
  snapshot sạch ở hai mốc không chứng minh chưa từng ghi rồi hoàn nguyên giữa chừng.
- Hai con số nháp đã sai và được sửa TRONG lượt (ghi rõ tại chỗ): "0 biên nhận human_audited" (đúng: 4) và "28 lượt khớp"
  (đúng: 18 dòng / 39 lần / 30 đoạn). Không con số nào khác trong tệp này là nháp.
