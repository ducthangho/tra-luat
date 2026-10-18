verdict: changes_requested
reviewed_sha: 2469f3ebed51dc228319cf375d7912bf7dbc0947
spec_sha256: 45c8d31441f027fb8e7d8425f2ca66770043edd4b958b0e6ad6c4e7a09e64b5a
model/effort tự khai: Claude Opus 5.5 (`claude-opus-5-5`), effort max — KHÔNG phải codex. Chạy như SUBAGENT do phiên điều
phối giao (lượt 9), tức đúng đường r9 chọn cho review (Q12). Model/effort là CẤU HÌNH được giao, không phải runtime evidence
(PROTOCOL :710–711): lượt này không sinh `modelUsage`, không có `session_run_id`; biên nhận của lượt (nếu ghi) phải tự khai
`che_do: subagent_trong_phien_dieu_phoi`, mức `review_deferred`. Lượt này có được giao qua định nghĩa `review-opus-max` hay
không: KHÔNG ĐO ĐƯỢC từ phía tôi (băm định nghĩa đo ở Hướng F). Cùng họ Claude với phiên soạn r9 ⇒ KHÔNG độc lập khác họ.
Không mạng, không đăng GitHub, không commit/push, không sửa `cay-kho`; ghi chỉ dưới `$R/goi/` và các thư mục `mktemp -d -p "$R"`.

Kết luận nội dung: **0 P1 / 2 P2 / 2 P3** (theo lớp; 5 finding F9-1…F9-5).
P2: `thu-tu-677-bo-ngo-o-dieu-kien-cap` (VÁ SINH LỖI MỚI; lớp nay ở ba lượt 7, 8, 9) ·
`tuong-tac-677-kiem-ke-t70-chua-neu` (VÁ SINH LỖI MỚI, nâng từ P3).
P3: `hop-dong-dong-bang-thieu-neo` (VÁ SINH LỖI MỚI, hạ từ P2) · `dieu-kien-dung-12-doc-mot-chuyen-tiep` (MỚI).

Trả lời câu hỏi gốc (áp cho r9).
(1) r9 đổi ĐÚNG phạm vi nó khai: §1, §2, §5, Phụ lục A, 12 hàng bảng (gồm `objective`, `executor`, `environment`,
`change_policy_sha`, `effective_write_set`, `effective_review_class`) và A1, A4–A7, A9, A10 giống từng byte r8; trong closure
chỉ đúng `required_checks` và `land_obligations` đổi (Hướng G). Q12 áp ĐỦ: không câu chuẩn tắc nào còn giữ phương án B
(Hướng A). Closure mới khớp `bien_nhan_v2` (5/5 số r9 khai tái lập, Hướng B) và KHÔNG mâu thuẫn với đường land
`human_audited` (Hướng H).
(2) Làm đúng từng chữ r9 thì packet KHÔNG land sai (0 P1): §5.1 kích hoạt #2 bắt drift chạm write set lúc land, A8 bắt `t70`.
Nhưng hai điều kiện cấp (1) và (4) tuyên bố một bảo đảm mà phép đo của chúng không có — đo được trên kho bare tại chỗ:
clone chưa fetch qua cả (1) lẫn (4) khi máy chủ đã land một thay đổi vào write set, hoặc đã có lease CÒN_HẠN mới trên một
nhánh sẵn tên (P2). Và nghĩa vụ `t70` mới viết theo "ca mới GỌI helper" trong khi vị từ là "tên helper trong `co_names`
cấp đỉnh": làm đúng chữ với một số cách viết ca thì `t70` ĐỎ, và với comprehension thì 3.11 (môi trường đo của r8/r9) và
3.12 (CI) cho kết quả NGƯỢC nhau (P2).
(3) Tín hiệu hội tụ §12 — nói thẳng: đọc chặt §8.3 (đóng vì bỏ B không phải vá) thì chuyển tiếp 8→9 = **2/7 = 29%** (3/7 =
43% nếu tính `dong-reviewer-loi-khai-rong-hon-do`), tức **chuyển tiếp thứ hai liên tiếp < 50%** sau 7→8 = 0/5 ⇒ PROTOCOL
§12 :1047–1048: **dừng vòng vá, đưa bằng chứng tới Review Rescue Checkpoint**. Chỉ khi người điều phối tính cả hai lớp đóng
vì Q12 là "vá thật" mới ra 4/7 = 57%. Độc lập với tỷ lệ: `thu-tu-677-bo-ngo-o-dieu-kien-cap` nay có mặt ở BA lượt (7, 8, 9)
⇒ §12 :1054–1056 đòi xem lại cách làm tại checkpoint. Chi tiết ở ĐỐI CHIẾU LƯỢT TRƯỚC.

## TIỀN KIỂM
- `sha256sum $R/SPEC.md` ⇒ `45c8d31441f027fb8e7d8425f2ca66770043edd4b958b0e6ad6c4e7a09e64b5a` (khớp) ·
  `git -C $R/cay-kho rev-parse HEAD` ⇒ `2469f3ebed51dc228319cf375d7912bf7dbc0947` (khớp) ⇒ không `blocked`.
- `core.abbrev` = 7; `cmp SPEC.md cay-kho/ops/specs/lease-id-ep-kieu-yaml-r9.md` khớp; `cmp SPEC-r8.md …-r8.md` khớp.
- `luot8/VERDICT.md` `68da880f…fe82`, `luot8/HINT.patch` `41e3763c…a400` (khớp PROMPT).
- `r8-r9.diff`: `diff -u SPEC-r8.md SPEC.md | tail -n +3 | sha256sum` = `tail -n +3 r8-r9.diff | sha256sum` = `b46a09a3…5479`.
- `git -C cay-kho diff --name-status 423b4ba 2469f3e` ⇒ đúng 3 dòng `A` (r7, r8, r9), khớp "thêm BA tệp".
- PROMPT nhắc mà `$R` KHÔNG có: `luot6/VERDICT.md`, `q10-readback.json` (`ls`: No such file) — phần ấy của PROMPT là của lượt 7.
  Thay thế có: `readback-5911243074.json` (Q10), `-5912559230` (Q11), `-5888631719` (Q8), `-5925190705` (Q12).
- Object VẮNG khỏi `kho.git` (`cat-file -t`): `eca94d1` (đầu ref lease #687 g3), `35e23d7`, `6112b89` ⇒ KHÔNG ĐO ĐƯỢC.
  Mirror có 8 nhánh (49 ref kể cả tag); không có `claude/dot-bien-l-bien-cong-khai-20260929`, `claude/cap-lease-687-g3`.
- Công cụ: Python 3.11.15 / 3.12.3 / 3.13.12, PyYAML 6.0.1, git 2.43.0, GNU patch 2.7.6, ruff 0.15.8 (nhị phân). Thư mục đo
  `$R/do.uiFp` (TMPDIR trong đó); dry-run/áp thật ở `$R/tmp.*`, `$R/apthat*.*`, `$R/rieng*.*` (đều `mktemp -d -p "$R"`).

## ĐỐI CHIẾU LƯỢT TRƯỚC

Lượt 8 (Claude Opus 5.5 max, subagent, trên `f958e14`): 0 P1 / 4 P2 / 3 P3, bảy lớp, mười finding. Tự kiểm trên r9:

| lớp (lượt 8) | finding lượt 8 | trạng thái trên r9 | bằng chứng tự đo |
|---|---|---|---|
| `hop-dong-dong-bang-thieu-neo` (P2) | F8-1 (b) đọc argv từ `run.json` | **ĐÃ ĐÓNG vì Q12 bỏ B** (không phải vá) | (b) mới chỉ khai cấu hình + `KHONG_do_duoc`; `run.json` chỉ còn ở :33/:800 (lịch sử) — Hướng A |
| | F8-2 điều kiện (3) cho review đặc tả không quyết định được | **ĐÃ VÁ THẬT** | ghi chú Q10 :239–244 + `depends_on` (3) cùng một tiêu chí; kiểm được bằng `_thieu` (Hướng B) và băm định nghĩa (Hướng F) |
| | (mới) F9-4 "đạt khi và chỉ khi … `_thieu` 0 lỗi" | ⇒ lớp **VÁ SINH LỖI MỚI** (mức P3) | G7: `_thieu` 0 mà `kiem()` 1 vi phạm — Hướng B |
| `dong-reviewer-loi-khai-rong-hon-do` (P2) | F8-3 "phiên và context mới" | **ĐÃ ĐÓNG** (câu đi theo B) | grep: "phiên mới" chỉ ở :9 ("bỏ mọi lời khai"), "context mới" chỉ ở :809 (lịch sử) |
| | F8-4 `session_run_id` làm bằng chứng độc lập | **ĐÃ ĐÓNG vì Q12 bỏ B**; r9 khai đúng rằng validator vẫn nhận chuỗi bất kỳ | G4 = 0 lỗi, G5 = 0 lỗi (Hướng B) |
| | F8-5 tiền lệ dẫn sai | **ĐÃ VÁ THẬT** | `phan-bien-quy-trinh-review-{1,2}` đều `che_do: subagent_trong_phien_dieu_phoi` + `review_deferred`; câu trích "không đường nào trong phiên trả model đang phục vụ" có trong review-2 |
| | biểu hiện lượt 7 (F7-4a "phiên mới" cho subagent) khi đường subagent QUAY LẠI | không tái phát | dòng reviewer :33 "không mang lời khai độc lập nào" |
| `duong-review-b-chua-do-dau-cuoi` (P2) | F8-6 `CHAN [15]`, B chưa đo đầu cuối | **ĐÃ ĐÓNG vì Q12 bỏ B** (không phải vá; r9 §10 :799–804 tự nói đúng như vậy) | không câu chuẩn tắc nào còn `claude -p`/launcher — Hướng A |
| `thu-tu-677-bo-ngo-o-dieu-kien-cap` (P2) | F8-7 dời nền chỉ theo TÊN | phần theo tên **ĐÃ VÁ** (lệnh `diff --quiet` đo được; sau fetch ra rc=1 đúng) | Hướng E |
| | (mới) F9-1 câu tự thêm "(để `origin/master` không là ref đệm cũ)" sai cơ chế; F9-2 cùng cơ chế ở (1) (có từ r6, mới tìm ra) | ⇒ lớp **VÁ SINH LỖI MỚI** | Hướng E, E2 |
| `q10-he-qua-mat-nhan-dien-giai` (P3) | F8-8 hệ quả gán cho quyết định chủ kho | **ĐÃ VÁ THẬT** | `nguon_cap_viec` :27 tách "lựa chọn chủ kho đã chọn", nói thẳng B không phải quyết định chủ kho; Q12 trích kèm nhãn "Hệ quả" (dòng 14) và đoạn "Áp vào r9 (việc của phiên soạn r9, không phải lời chủ kho)"; không chỗ nào còn gán diễn giải cho chủ kho |
| `so-do-nen-khong-khop` (P3) | F8-9 "6/6 hunk" cho bốn nhóm | **ĐÃ VÁ THẬT** | §9 :750–753 ghi "5 trong 6 hunk"; mọi số MỚI đo lại được đều khớp (BẢNG ĐO) |
| `tuong-tac-677-kiem-ke-t70-chua-neu` (P3) | F8-10 `t70` chưa nêu | đã nêu, nhưng nghĩa vụ lệch vị từ ⇒ **VÁ SINH LỖI MỚI**, nâng **P2** | Hướng D |

Tín hiệu hội tụ §12 (:1043–1056). U (lớp mở cuối lượt 8) = 7. F (ĐÃ VÁ THẬT theo §8.3 :755–759, "chuyển biểu hiện ra ngoài
scope không được tính là vá"):
- đọc chặt: F = {`q10-he-qua-mat-nhan-dien-giai`, `so-do-nen-khong-khop`} ⇒ **2/7 = 28,6%**;
- tính thêm `dong-reviewer-loi-khai-rong-hon-do` (biểu hiện lượt 8 đi theo B, phần đường subagent vá thật) ⇒ 3/7 = 42,9%;
- tính cả `duong-review-b-chua-do-dau-cuoi` (đóng chỉ vì Q12 bỏ B) ⇒ 4/7 = 57,1%;
- nếu người điều phối tách F9-4 khỏi `hop-dong-dong-bang-thieu-neo` thành lớp P3 riêng ⇒ mỗi con số trên +1/7.
Chuyển tiếp 7→8 = 0/5 (tỷ lệ xác định ĐẦU TIÊN; 6→7 là `N/A`). Với hai cách đọc đầu, 8→9 là chuyển tiếp **thứ hai liên tiếp
< 50%** ⇒ §12 :1047–1048: dừng vòng vá, đưa bằng chứng tới Review Rescue Checkpoint. Lớp mới ở lượt 9: 1
(`dieu-kien-dung-12-doc-mot-chuyen-tiep`). Lớp tái mở: không. Ba lượt trở lên: `thu-tu-677-bo-ngo-o-dieu-kien-cap` (7, 8, 9),
`hop-dong-dong-bang-thieu-neo` (1, 2, 7, 8, 9).
Khuyến nghị cho checkpoint (KHÔNG phải finding): cả hai lớp P2 cùng một hình dạng — điều kiện viết bằng văn xuôi trôi khỏi
phép kiểm máy mà nó mô tả (tập tên ≠ độ tươi của ref; "gọi" ≠ `co_names` cấp đỉnh). Đường ít tốn nhất: viết điều kiện bằng
CHÍNH đầu ra của công cụ (chuỗi lệnh cố định fetch → so tên+OID → `ai-dang-giu` → `diff --quiet` → `merge-base` ghi vào handoff;
`mong` = `_ca_doc_than_buoc(CA)` dưới Python của CI), thay vì thêm câu.
Quan sát ngoài phạm vi chấm: ADR-0043 đặt trần canon HAI vòng review hợp lệ cho một PR packet (vượt phải có khối `nang_tran`);
chuỗi review đặc tả này đã 9 lượt (6 trên PR #679, 3 cục bộ). Có khối `nang_tran` nào phủ chuỗi ấy hay không: KHÔNG ĐO ĐƯỢC từ `$R`.

## BẢNG LỚP

| slug lớp | hạng | biểu hiện | phương án | phép kiểm / giới hạn |
|---|---|---|---|---|
| `thu-tu-677-bo-ngo-o-dieu-kien-cap` | **P2** (VÁ SINH LỖI MỚI) | F9-1 (:34, (4)): r9 tự thêm "trên cùng kho vừa qua phép so tập tên ref ở (1) (để `origin/master` không là ref đệm cũ)" — phép so TẬP TÊN không làm được điều ấy; đo: máy chủ land một commit đổi `ops/lease_publish_test.py`, clone chưa fetch ⇒ tập tên 1/1, 0 lệch, `ai-dang-giu` rc=0, lệnh (4) rc=0. F9-2 (:34, (1), có từ r6, cùng cơ chế): lease g2 CÒN_HẠN đăng trên nhánh ĐÃ CÓ tên ⇒ tập tên 2/2, 0 lệch, `ai-dang-giu` rc=0 `NGƯỜI_GIỮ 0` — cửa sổ hai writer; kho có đúng hình dạng ấy (#687 g1, g2 cùng `claude/lease-publish-windows-do`, r9 :34). `ai-dang-giu` không fetch, không so OID (`ops/lease_publish.py` :370–421, :482–511) | HINT nhóm 1 (2 hunk): (1) thêm so **cặp tên + OID** ngay sau `git fetch` refspec rộng (chặt hơn Q8, không nới); (4) câu đệm cũ thành "kể cả cặp tên + OID"; §10 ghi hai phép đo | Kiểm: lúc cấp, handoff có output `comm -23` của cặp tên + OID rỗng ngay trước (1)/(4). Giới hạn: phép so rồi cấp vẫn KHÔNG nguyên tử — thu hẹp cửa sổ, không đóng |
| `tuong-tac-677-kiem-ke-t70-chua-neu` | **P2** (VÁ SINH LỖI MỚI, nâng từ P3) | F9-3 (§4 :303–308, §6 mục 8 :337–339, A2 :373–380, A3 :393–394, A8 :436): nghĩa vụ là "mọi ca MỚI GỌI helper"; vị từ thật là "ca `@ca` (mới hoặc sửa) có tên helper trong `co_names` CẤP ĐỈNH". Đo (3.11 \| 3.12): gọi trong hàm lồng/lambda ⇒ thêm tên làm `t70` 0/1 (làm đúng chữ §6 mục 8 thì trái A8), không thêm vẫn 1/1 ("quên thì `t70` ĐỎ" ở A3 sai); gọi trong list comprehension ⇒ không tập `mong` nào xanh ở cả hai bản; sửa `t178` (A2 bắt mở rộng) ⇒ cần thêm `t178` mà "ca mới" không phủ | HINT nhóm 2 (5 hunk): định nghĩa nghĩa vụ bằng chính vị từ dưới Python CI (3.12), gồm ca sửa; khuyên tham chiếu helper ở cấp đỉnh; ghi phép đo lượt 9 | Kiểm: trên ứng viên `sorted(_ca_doc_than_buoc(CA))` dưới 3.12 bằng `mong`; ca mới tham chiếu cấp đỉnh ⇒ cùng kết quả 3.11/3.12. Giới hạn: 3.13 không đo |
| `hop-dong-dong-bang-thieu-neo` | **P3** (VÁ SINH LỖI MỚI, hạ từ P2) | F9-4 (:88–90): "Vế review **đạt** khi và chỉ khi … (a) … `_thieu` … 0 lỗi" — `_thieu` là điều kiện CẦN; cổng biên nhận thật là `kiem()` (`_thieu` + `_neo_git`), và `gate-ops` chạy `kiem()` trên kho thật (`ops/bien_nhan_v2_test.py` :349). Đo: mẫu G7 `_thieu` 0 lỗi ⇒ `kiem()` 1 vi phạm | HINT nhóm 3 (1 hunk): (a) đòi thêm `kiem()` không báo vi phạm hay KHÔNG ĐO ĐƯỢC nào cho chính biên nhận | Kiểm: `python ops/bien_nhan_v2.py` trên cây chứa biên nhận không có dòng ĐỎ/KHÔNG ĐO ĐƯỢC về tệp ấy. Giới hạn: cổng kiểm CẤU TRÚC, không kiểm sự thật (docstring bien_nhan_v2 :37–44) |
| `dieu-kien-dung-12-doc-mot-chuyen-tiep` | **P3** (MỚI) | F9-5 (§9 :756–759): "0/5 … dưới ngưỡng 50% … Theo §12 đó là điểm dừng vòng vá và Review Rescue Checkpoint" — §12 :1047–1048 đòi HAI chuyển tiếp liên tiếp < 50%; 7→8 là tỷ lệ xác định đầu tiên (6→7 `N/A`; :1046–1047 cấm ghép qua `N/A`). Thứ đã kích hoạt là luật một lớp ở ba lượt (:1054–1056). Câu ấy đọc như điểm dừng theo tỷ lệ đã xử lý xong nhờ Q12, trong khi nó được quyết ở 8→9, tức lượt này | HINT nhóm 4 (1 hunk) | Kiểm: §9 phân biệt hai cò của §12. Giới hạn: không đổi hành vi thi hành |

## BẢNG SĂN

Mười hai khối hướng (A, B, C, D, E, E2, F, G, H, I, J, K): phủ cả 7 hướng gợi ý của PROMPT (dời sang r8→r9: 1→G, 2→B/H,
3→B/H, 4→C, 5→F, 6→E/K, 7→A), bốn trọng tâm lượt 9, và 4 hướng tự thêm (E2, I, J, K).

```
HƯỚNG A: Dấu vết phương án B còn sót (Q12 áp đủ chưa)            [trọng tâm (1); gợi ý 7]
  lệnh       : for pat in 'claude -p' 'launcher.py run' 'session_run_id' 'same_provider_approved' 'phiên mới' 'context mới'
               'phương án B' 'modelUsage' 'kiem_ket_qua' 'run.json' '--effort' 'CHAN \[15\]' 'bo-qua-probe' 'trust'; do grep -n …; done;
               grep -n -i 'codex\|gpt-6'; grep -n 'bốn điều kiện\|năm điều kiện'
  output     : claude -p 7 dòng (9 33 107 278 282 799 800) · launcher.py run 4 (9 33 278 799) · session_run_id 6 (33 95 98 749 801 809)
               · same_provider_approved 6 (9 33 94 95 292 810) · "phiên mới" 1 (9) · "context mới" 1 (809) · modelUsage 2 (98 749)
               · run.json 2 (33 800) · CHAN [15] 2 (33 801) · trust 5 (33 278 282 767 801) · kiem_ket_qua / --effort / bo-qua-probe 0.
               Từng dòng: 9 bảng thay đổi (cột r8) · 33 phần "Lịch sử" dòng reviewer + câu đo validator · 94–98 phép đo (a)/(b) · 107
               "Q12 bỏ đường claude -p" · 278–285 trích nguyên văn Q12 · 292 so mức với r8 · 749/767 §9 lịch sử · 799–810 §10 "BỎ ở r9".
               codex/gpt-6: 11 dòng, đều lịch sử r1–r6 hoặc trích Q10/Q12/PROTOCOL. "năm điều kiện" là chuẩn tắc; "bốn" chỉ ở Q8/lịch sử.
  kết luận   : KHÔNG PHẢI LỖI — không câu chuẩn tắc nào còn đòi B; không chỗ nào khai codex là reviewer lượt thi hành.
```

```
HƯỚNG B: Closure mới khớp `bien_nhan_v2._thieu` (đo, không đọc)          [trọng tâm (1); gợi ý 2]
  lệnh       : clone --no-local --no-hardlinks kho.git → do.uiFp/n20 (20ec8d5); bn_do.py nạp ops/bien_nhan_v2.py (sha256
               38cda51c…defc, PROVIDER_NGUON_HONG None); biên nhận mẫu wp678 dựng từ tiền lệ phan-bien-quy-trinh-review-2 (05:41:48Z).
  output     : G0 tiền lệ nguyên byte ⇒ 0 · G1 mẫu (anthropic, claude_code_cli, che_do subagent, KHONG_do_duoc, review_deferred) ⇒ 0
               · G2 = G1 + same_provider_approved ⇒ 1 ("tự khai chạy trong phiên điều phối") · G3 = G1 + human_audited ⇒ 2
               · G4 bỏ che_do + session_run_id 'x' + same_provider_approved ⇒ 0 · G5 bỏ che_do, review_deferred ⇒ 0
               · G6 bỏ KHONG_do_duoc (không session_run_id) ⇒ 1 · G8 = G1 + cross_approved ⇒ 2 (phiên + cùng họ claude).
               G7 = G1 nhưng evidence_url là URL PR (anchor canonical_ancestry) ⇒ `_thieu` 0; `kiem()` trên kho git tạm (verdict + biên nhận
               commit) ⇒ 1 vi phạm (`_neo_git`: "evidence_url KHÔNG phải URL blob ghim commit"); G1 neo blob đúng ⇒ `kiem()` 0, dat=1.
               CI: ci.yml `gate-ops` :590 `python ops/bien_nhan_v2_test.py`, ca :349 `_kiem(GOC)` "kho thật KHÔNG sạch" (kiem trên kho thật).
  kết luận   : 5/5 số r9 khai ở (a) KHỚP; G5 xác nhận lời r9 "che_do là nghĩa vụ khai, không phải chốt máy"; G6 khớp (b) đòi KHONG_do_duoc.
               G7 ⇒ LỖI P3 F9-4 (lớp hop-dong-dong-bang-thieu-neo).
```

```
HƯỚNG C: Nguyên văn Q12 và các readback                                    [gợi ý 4]
  lệnh       : python: body.encode('utf-8') ⇒ sha256, byte, đếm thực thể HTML; so dòng 5–14 thân với khối "  > " SPEC.md :276–285.
  output     : 5925190705: sha256 4c9d5e198e81eff941b2c18f45d25e80e56b75e5a2a7334cacd2629f6cf2af2f, 1648 byte, 17 dòng, 0 thực thể,
               created_at 2026-10-01T05:12:59Z, OWNER, app `claude`, html_url #issuecomment-5925190705; dòng 5–14: 10/10 khớp từng byte;
               0 dòng trích không có trong thân; dòng 11–12 (hai lựa chọn không chọn) không kèm mô tả. Q10 69cc35b1…/2151, Q11 392069d1…/1741,
               Q8 3a8c40a6…/1187: 0 thực thể, khớp r9. Q8 dòng 8: "(sau khi so `ls-remote` với `for-each-ref` theo tập tên)"; dòng 7 "đo lại
               ngay trước khi cấp".
  kết luận   : KHÔNG PHẢI LỖI. (Q8 cho phép siết thêm OID mà không nới — dùng ở HINT nhóm 1.)
```

```
HƯỚNG D: Nghĩa vụ t70 — chạy lại phép đột biến, rồi đột biến NGOÀI ca r9 đã đo      [trọng tâm (3)]
  lệnh       : t70_dotbien.py: mỗi biến thể một thư mục `git archive 20ec8d5 ops .github`; chèn một ca @ca trước `_chay_main_meta`;
               PYTHONDONTWRITEBYTECODE=1 <py> ops/lease_publish_test.py --chi-ca=t70_, py ∈ {python3.11, python3.12}; 05:39:54Z–05:40:08Z.
               quet_long.py: vị từ cấp đỉnh vs quét đệ quy mọi code object trên nền.
  output     : (3.11 | 3.12)  V0 gốc 1/1 | 1/1
               V1 ca mới NHẮC helper cấp đỉnh, không thêm tên 0/1 | 0/1 · V2 thêm tên 1/1 | 1/1                ← đúng số r9 khai
               V3 GỌI trong hàm lồng, không thêm 1/1 | 1/1 · V4 thêm tên 0/1 | 0/1
               V5 GỌI trong list comprehension, không thêm 1/1 | 0/1 · V6 thêm tên 0/1 | 1/1
               V7 GỌI trong lambda, không thêm 1/1 | 1/1 · V8 thêm tên 0/1 | 0/1
               V9 SỬA t178 thêm một dòng nhắc helper, không thêm 0/1 | 0/1 · V10 thêm "t178" 1/1 | 1/1          0 .pyc
               quet_long: 195 ca; cấp đỉnh 13 (đúng `mong`); đệ quy 14 — thêm chính `t70` (hàm lồng `_a`/`_b`), tức R1-F6 DỰA vào việc
               vị từ chỉ đọc `co_names` cấp đỉnh. CI: `gate-ops` ghim 3.12 (ci.yml :574) và chạy suite ở :630 qua
               ops/chay_lease_publish_test.sh, script ưu tiên `python` (:37–40); r8/r9 đo suite bằng Python 3.11.15 (A8, §8).
  kết luận   : phép đo r9 (V0–V2) tái lập ĐÚNG. Nghĩa vụ viết "mọi ca MỚI GỌI helper" ≠ vị từ ⇒ LỖI P2 F9-3 (VÁ SINH LỖI MỚI).
               Tự phê: cụm "ca biên A3 (gọi một trong hai helper ấy)" có từ HINT lượt 8 (F8-10), lượt ấy cũng chỉ đo ca nhắc cấp đỉnh;
               xa hơn là M6 của #677 r7 :335–336 ("số ca mới gọi helper mới").
```

```
HƯỚNG E: Điều kiện (4) tổng quát — đo được bằng lệnh nêu, trên ĐÚNG kho?          [trọng tâm (2); gợi ý 6]
  giả thuyết : câu r9 tự thêm "(để origin/master không là ref đệm cũ)" dựa vào phép so TẬP TÊN — phép ấy không làm được điều đó.
  lệnh       : đọc ops/lease_publish.py@20ec8d5: `ai-dang-giu` (:2093) → `_quet_lease_toan_kho` (:482) chỉ so `_ten_nhanh_may_chu − ten_cuc_bo`
               (:508, TÊN, một chiều) và nhánh cục bộ tụt sau remote-tracking (:370–421); không fetch, không so OID máy chủ.
               word-diff "r8 + 6 hunk HINT lượt 8" → r9 (hint8_ap.py): cụm ấy do phiên soạn r9 thêm tay (r9 §9 bước (3) tự khai).
               stale.sh (05:43:52Z): kho bare làm máy chủ; clone refspec +refs/heads/*; máy chủ land một commit đổi
               ops/lease_publish_test.py; ở clone CHƯA fetch: phép so (1), `ai-dang-giu` THẬT của 20ec8d5, lệnh (4), dạng (5).
  output     : CHƯA fetch: tập tên máy chủ 1 / cục bộ 1, comm -23 0, comm -13 0 ⇒ (1) qua; so tên+OID lệch 2 dòng;
               `ai-dang-giu ops/lease_publish_test.py` rc=0 "NGƯỜI_GIỮ 0: không có"; (4) `git diff --quiet <nền> origin/master -- <write set>`
               **rc=0** (origin/master = nền cũ ffeda90); `merge-base --is-ancestor <nền> origin/master` rc=0.
               SAU `git fetch origin '+refs/heads/*:refs/remotes/origin/*'`: tên+OID lệch 0; (4) rc=1 (đúng); ai-dang-giu rc=12 (master tụt sau).
               PROTOCOL :365–368 (fence trước merge/land, §5.1, §13): "So bằng tên **và** OID … không coi head/base khác là vô hại vì cùng
               số lượng ref". Câu hỏi Q10 do phiên điều phối viết (:226) cũng ghi "so tên+OID ref 0 lệch"; r9 :34 phiên soạn tự đo cả cặp.
  kết luận   : LỖI P2 F9-1 (lớp thu-tu-677-bo-ngo-o-dieu-kien-cap, VÁ SINH LỖI MỚI): đúng kịch bản (4) sinh ra để chặn lọt qua (1)+(4)+(5)
               khi clone chưa fetch. Lệnh diff tự nó đo đúng (rc 0/1). Tự phê: HINT lượt 8 viết (4) tổng quát mà không chốt độ tươi.
```

```
HƯỚNG E2 (tự thêm): cùng cơ chế ở điều kiện (1) — lease MỚI trên nhánh ĐÃ CÓ tên
  lệnh       : stale_lease.sh (05:52:55Z): máy chủ có nhánh `claude/lease-khac` mang lease g1 (hết hạn, giữ ops/lease_publish_test.py); clone;
               máy chủ thêm lease g2 CÒN_HẠN (hạn 2026-12-31) trên CÙNG nhánh; ở clone chưa fetch chạy (1) và `ai-dang-giu` của 20ec8d5.
  output     : CHƯA fetch: tập tên 2/2, comm 0/0; tên+OID lệch 2 dòng; `ai-dang-giu` rc=0, chỉ thấy "HẾT_HẠN khac-g1-claude",
               "NGƯỜI_GIỮ 0: không có". SAU fetch: tên+OID lệch 0; rc=11, "CÒN_HẠN khac-g2-claude", "NGƯỜI_GIỮ 1: khac-g2-claude".
               Hình dạng có thật trong kho: r9 :34 (lịch sử r7) — hai lease #687 r1-g1 và r2-g2 cùng ở `refs/remotes/origin/claude/lease-publish-windows-do`.
  kết luận   : LỖI P2 F9-2 (cùng lớp; có từ r6, mới tìm ra): (1) "NGƯỜI_GIỮ 0 sau khi so tập tên" không loại trừ cửa sổ hai writer.
```

```
HƯỚNG F: Số hạng §8/§9/§10 đo được offline (kiểm SỐ HẠNG, không kiểm quan hệ)     [trọng tâm (4); gợi ý 5]
  lệnh + output:
   git archive 20ec8d5 ops/leases + yaml.safe_load ⇒ 123 tệp = 119 .yaml + 4 .nhap; 0 lỗi parse; 23 tệp có write_set chứa
     ops/lease_publish*.py; 8 packet [203, 206, 227, 238, 244, 396, 579, 676]                                      KHỚP 119/23/8
   t70 :2995–3009 (def :2995, @ca :2994), vị từ :2990–2991, `mong` 13 tên; M6 của #677 r7 :335                      KHỚP
   cay-kho: log --diff-filter=A -- r8 ⇒ f958e147…; 1 commit chạm; sha256 f173e7cf…; 890 dòng; cha 088511f; r9: tạo bởi 2469f3e, 1 commit KHỚP
   hint8_ap.py: HINT lượt 8 áp CẢ lên bản sao r8 (không sed — HINT đã trỏ đúng tệp r8): rc=0, 11/11, 0 fuzz, 6 offset, 890→927     KHỚP
     lọc 6 hunk (hop-dong #2, thu-tu-677 #1 #2, q10 #1, so-do #1, tuong-tac #1): rc=0, 6/6, 0 fuzz, 3 offset 4 dòng, 890→902       KHỚP
     word-diff "r8 + 6 hunk" → r9: đúng ba câu sửa tay + chốt (4) mà §9 bước (3) khai, rồi phần Q12/§4/§6/A3/A8/§8/header       KHỚP
   bien_nhan_v2@20ec8d5 sha256 38cda51c…defc; PROTOCOL + bien_nhan_v2 giống hệt 423b4ba↔20ec8d5 và 20ec8d5↔2469f3e (diff --quiet rc=0) KHỚP
   ~/.claude/agents/review-opus-max.md (CHỈ ĐỌC băm/cỡ/2 khoá, không in thân, 05:44:35Z): sha256 e225b81c…b792c, 1175 byte,
     model: claude-opus-5-5, effort: max                                                                              KHỚP
   ruff 0.15.8 `check --no-cache --select F` hai tệp trên 20ec8d5 (giữa 05:44:35Z và 05:49:17Z): rc=1, 9 lỗi (7 F401, 2 F541) đều ở
     tệp test; ops/lease_publish.py 0                                                                                  KHỚP (giữ từ r8)
   đoạn miễn trừ: diff --name-only 89fc4fa 20ec8d5 ⇒ 128; tên khớp polic|closure|dispatcher 0; dòng thêm khớp (không phân biệt hoa
     thường) 16 = 1+1+1 (verdict lượt 3, 4, 6) + 1+3+3+3+3 (spec r2–r6); 423b4ba..20ec8d5 0; first-parent merges 89fc4fa..20ec8d5 10  KHỚP
   KHÔNG ĐO ĐƯỢC (mạng / object vắng): 461/461 ref, NGƯỜI_GIỮ live, lease #687 g3 (eca94d1), REST PR #689 05:22Z, thân #682 (76bee6fb…,
     3416 byte, dòng 29/31), "áp HINT lượt 7 lên r7 05:26:09Z" (HINT lượt 7 không có trong $R), bản chiếu #678 comment 5925164956,
     `git cat-file -t` trên adg2.
  kết luận   : KHÔNG PHẢI LỖI ở mọi số đo lại được.
```

```
HƯỚNG G: Phạm vi thay đổi r8 → r9 (byte-level)                             [gợi ý 1]
  lệnh       : python: tách SPEC theo "## ", so từng mục; tách hàng bảng "| k | v |"; tách A1–A10.
  output     : GIỐNG byte: §1, §2, §5, Phụ lục A; hàng schema_version, packet_id, packet_issue, objective, review_class, risk, executor,
               environment, spec_hash, change_policy_sha, effective_write_set, effective_review_class; A1, A4, A5, A6, A7, A9, A10.
               KHÁC: đầu tệp (-55 +60), §3 (-1 +31), §4 (-1 +8), §6 (+3), §7 (-2 +11: A2, A3, A8), §8 (-3 +10), §9 (-1 +28), §10 (-10 +29);
               hàng revision, thay_the_cho, mission_issue, nguon_cap_viec, reviewer, depends_on, nền nghiệm thu, required_checks, land_obligations.
               required_checks: phần CI giữ nguyên chữ, chỉ vế review đổi; land_obligations: chỉ chèn "mức human_audited (PROTOCOL §8 mục 2; Q12)".
               Job/workflow: ci.yml `gate` :47, `gate-ops` :536, `gate-registry` :746, `gate-packet-loop` :814; ops-thu-hoi-admission.yml `name: thu-hoi`.
  kết luận   : KHÔNG PHẢI LỖI — r9 chỉ đổi đúng những gì bảng đầu tệp khai; giá trị nền nghiệm thu (20ec8d5) không đổi.
```

```
HƯỚNG H: Đường land human_audited và mức review_deferred có mâu thuẫn không     [trọng tâm (1); gợi ý 2, 3]
  lệnh       : đọc PROTOCOL@20ec8d5 :562–568, :577, :652, :657–658, :661–663, :681–682, :993–998, :1121–1123; bien_nhan_v2 :498–515, :757–797;
               biên nhận human-audit tiền lệ ops/reviews/cai-cong-cu-sigpipe-r2-human-audit-verdict.receipt.yaml; grep assurance trong
               packet_loop.py, land-packets/cross-review SKILL.md.
  output     : :568 review_deferred "vẫn được vào draft land PR nhưng cần xác nhận riêng khi apply"; :661–663 phạm vi nhạy cảm "không được dùng
               review_deferred: phải có cross-review khác nền tảng hoặc human review có audit"; :681–682 sensitive "Codex cross_approved hoặc
               human_audited"; :1121–1123 cùng provider không tự nhận same_provider_approved từ cấu hình. Tiền lệ human-audit: provider human,
               surface manual_audit, transport human, phien_doc_lap true, ai_dang_comment_ky chu_kho_tu_dang; validator chỉ cho người
               human_audited (:787–796). packet_loop.py / hai SKILL: 0 dòng nhắc bốn mức. `assurance_target` có ở cả 119 lease nhưng 0 cổng đọc.
  kết luận   : KHÔNG PHẢI LỖI — review subagent review_deferred là phản biện bổ sung, land dựa vào human_audited; khớp :568, :661–663, :681–682.
```

```
HƯỚNG I (tự thêm): Nền A8 dưới Python CỦA CI
  lệnh       : clone thứ hai do.uiFp/n20b (20ec8d5, core.abbrev 7); PYTHONDONTWRITEBYTECODE=1 TMPDIR=<scratch> python3.12 ops/lease_publish_test.py
  output     : 05:49:17Z–05:55:26Z: "lease_publish: 195/195 đạt; đã chạy=195, bỏ qua=0", rc=0; vào/ra 195/195; 0 .pyc; status --ignored 0 dòng.
  kết luận   : KHÔNG PHẢI LỖI — nền 195/195 r8 đo ở 3.11.15 giữ nguyên ở 3.12.3 (bản CI ghim). Lý do chạy: Hướng D cho thấy 3.11 và 3.12
               có thể lệch ở `t70`.
```

```
HƯỚNG J (tự thêm): Đọc §12 trong §9 của r9
  lệnh       : đọc PROTOCOL :1043–1056 (tín hiệu không hội tụ), :1079–1081 (Review Rescue Checkpoint); luot8/VERDICT.md :59–67; r9 :755–761.
  output     : :1047–1048 "Hai chuyển tiếp liên tiếp có tỷ lệ <50% thì dừng vòng vá"; :1046–1047 cấm ghép qua N/A; lượt 8 :60–61 "đây là tỷ lệ
               xác định ĐẦU TIÊN; chuyển tiếp 8→9 cũng < 50% ⇒ dừng vòng vá". r9 :758 "Theo §12 đó [0/5] là điểm dừng vòng vá và Review
               Rescue Checkpoint".
  kết luận   : LỖI P3 F9-5 (lớp mới dieu-kien-dung-12-doc-mot-chuyen-tiep).
```

```
HƯỚNG K (tự thêm): Tương tác #687 sau khi cấp — PR packet khác land GIỮA lượt thi hành
  giả thuyết : #687 g3 đang giữ ops/lease_publish_test.py; nếu lease ấy hết hạn mà PR #687 chưa land, (1)–(5) qua, lease wp678 cấp, rồi PR #687
               land giữa chừng (land authority tách khỏi executor lease, PROTOCOL :255–259) — cửa hai writer?
  lệnh       : đọc PROTOCOL §5.1 :323–372.
  output     : :351 kích hoạt #2 "DRIFT giao write set của packet ≠ rỗng" ⇒ chạy lại gate SAU khi merge; §5.1 áp cả cho land (§13).
  kết luận   : KHÔNG PHẢI LỖI của r9 — protocol có cơ chế cho drift lúc land; (4) chỉ cần lo trước lúc cấp.
```

## BẢNG ĐO

| khẳng định trong spec | spec khai | đo được | khớp? |
|---|---|---|---|
| sha256 r9 / HEAD | 45c8d31…/2469f3e | như khai | có |
| r8 tạo bởi f958e147, 1 commit chạm, 890 dòng, sha f173e7cf…, cha 088511f | có | như khai | có |
| VERDICT/HINT lượt 8 | 68da880f…/41e3763c… | như khai | có |
| HINT lượt 8 áp cả: rc=0, 11/11, 0 fuzz, 6 offset, 890→927 | có | như khai | có |
| HINT lọc 6 hunk: rc=0, 6/6, 0 fuzz, 3 offset 4 dòng, 890→902 | có | như khai | có |
| sửa tay bước (3) (ba câu + chốt (4)) | có | word-diff đúng các chỗ ấy | có |
| bien_nhan_v2@20ec8d5 sha256 38cda51c… | có | như khai | có |
| `_thieu`: tiền lệ 0, mẫu 0, same_provider 1, human_audited 2, bỏ che_do+'x'+same_provider 0 | có | như khai | có (5/5) |
| "Validator không tự phát hiện subagent" | có | G4 0, G5 0 | có |
| định nghĩa review-opus-max e225b81c…, 1175 byte, model/effort | có | như khai (05:44:35Z) | có |
| Q12: sha 4c9d5e19…, 1648 byte, 0 thực thể, tạo 05:12:59Z, app claude, dòng 5–14 từng byte | có | như khai, 10/10 | có |
| "Thân không kèm mô tả cho hai lựa chọn không chọn" | có | dòng 11–12 | có |
| PROTOCOL/bien_nhan_v2 giống hệt 423b4ba↔20ec8d5 | có | rc=0 | có |
| số dòng PROTOCOL :562, :563–564, :565–567, :568, :652, :658, :662–663, :681–682, :710–716; bien_nhan_v2 :703, :720–726, :734–737, :793–796 | có | đúng nội dung gán | có |
| có biên nhận `anthropic_claude` ghi `advisory_review` | có | ≥5 tệp (assurance-ho-model-review-1..3, ci-g5-…-20, -21) | có |
| tiền lệ phan-bien-quy-trinh-review-{1,2} che_do subagent + review_deferred | có | cả hai | có |
| t70 :2995–3009, vị từ :2990–2991, 13 tên | có | như khai | có |
| t70: gốc 1/1; ca nhắc cấp đỉnh 0/1; thêm tên 1/1 | có | như khai, cả 3.11 và 3.12 | có |
| "Mọi ca mới gọi helper … phải thêm tên vào mong" (§4, §6 mục 8) | đúng | V3/V4, V7/V8, V5/V6, V9/V10 lệch | **không** (F9-3) |
| "quên thì t70 ĐỎ trên ứng viên" (A3) | đúng | V3, V7, V5@3.11 vẫn 1/1 | **không** (F9-3) |
| "(để origin/master không là ref đệm cũ)" nhờ phép so tập tên | đúng | stale.sh: tập tên 0 lệch, (4) rc=0 trên đệm cũ | **không** (F9-1) |
| (1) "NGƯỜI_GIỮ 0 … sau khi so tập tên" loại trừ người giữ | ngầm định | stale_lease.sh: NGƯỜI_GIỮ 0 trên đệm cũ, máy chủ có g2 CÒN_HẠN | **không** (F9-2) |
| "đạt khi và chỉ khi … `_thieu` 0 lỗi" | đủ | G7: `_thieu` 0, `kiem()` 1 | **không** (F9-4, P3) |
| "Theo §12 đó [0/5] là điểm dừng vòng vá" | có | §12 đòi hai chuyển tiếp liên tiếp | **không** (F9-5, P3) |
| 119 tệp lease, 0 lỗi parse, 23 tệp, 8 packet | có | như khai | có |
| 128 tệp / 0 tên / 16 dòng (verdict 3, 4, 6; spec r2–r6) / 0 | có | như khai | có |
| suite 195/195 (20ec8d5) và 187/187 (89fc4fa), ruff 9 F — giữ từ r8 | có | 195/195 tái lập ở 3.12 (CI); ruff 9 F | có (187/187 không đo lại: lượt 8 đã đo) |
| PR #689 merged, 20ec8d5 là merge | có | tiêu đề commit "Merge pull request #689 …" | có (nhất quán; REST: KHÔNG ĐO ĐƯỢC) |
| 461/461 ref; NGƯỜI_GIỮ live; lease #687 g3 (eca94d1); thân #682 | có | cần mạng / object vắng | KHÔNG ĐO ĐƯỢC |

## CHI TIẾT TỪNG LỚP

### `thu-tu-677-bo-ngo-o-dieu-kien-cap` — P2 (VÁ SINH LỖI MỚI; lượt 7 P2, lượt 8 P2, lượt 9 P2)
- F9-1 (r9 :34, phần tổng quát của (4)). Câu do phiên soạn r9 thêm tay khẳng định phép so tập tên ở (1) làm `origin/master` hết là
  ref đệm cũ. Phép so tập tên chỉ bắt nhánh THIẾU; `origin/master` cũ cùng tên vẫn qua. Đo (Hướng E): đúng kịch bản (4) sinh ra để
  chặn — một packet khác land đổi tệp write set — lọt qua (1), (4) và dạng (5) khi clone chưa fetch.
- F9-2 (r9 :34, (1); có từ r6, cùng cơ chế, mới tìm ra). Lease mới đăng trên một nhánh đã có tên giữ nguyên tập tên; `ai-dang-giu`
  đọc nội dung cũ và ra `NGƯỜI_GIỮ 0` (Hướng E2) — cửa sổ hai writer, đúng thứ write-set exclusion sinh ra để chặn.
- Vì sao P2, không P1: r9 ghi "đo lại lúc cấp", không buộc đo trên đệm cũ; §5.1 kích hoạt #2 bắt drift lúc land. Nhưng (1) và (4)
  tuyên bố bảo đảm rộng hơn phép đo của chúng — rubric "nhãn lời khai rộng hơn phép đo". Bằng chứng phụ: chính phiên điều phối/phiên
  soạn đã đo tên + OID (r9 :34, câu hỏi Q10 :226) mà văn bản chuẩn tắc chỉ đòi tập tên.
- Phương án (HINT nhóm 1): giữ phép so tập tên của Q8, thêm so cặp tên + OID ngay sau `git fetch` refspec rộng (`--unshallow` nếu
  kho nông) và `merge --ff-only` nhánh tụt sau; `comm -23` cặp tên + OID phải rỗng; (4) chạy trên đúng kho ấy. Chặt hơn Q8, không nới.
- Giới hạn: phép so rồi cấp vẫn không nguyên tử; HINT thu hẹp cửa sổ, KHÔNG đóng nó (đừng viết thành "đóng").

### `tuong-tac-677-kiem-ke-t70-chua-neu` — P2 (VÁ SINH LỖI MỚI, nâng từ P3; lượt 8, 9)
- F9-3 (§4 :303–308, §6 mục 8 :337–339, A2 :373–380, A3 :393–394, A8 :436). Vị từ `_ca_doc_than_buoc` đọc `fn.__code__.co_names` CẤP
  ĐỈNH; r9 viết nghĩa vụ theo "ca MỚI GỌI helper". Bốn hệ quả đo được (Hướng D): (a) gọi trong hàm lồng/lambda — làm đúng chữ §6 mục
  8 thì `t70` ĐỎ, tức §6 mục 8 trái A8; (b) "quên thì `t70` ĐỎ" (A3) sai với chính các ca ấy; (c) comprehension — 3.11 và 3.12 cho
  kết quả ngược, không `mong` nào xanh ở cả hai, mà r8/r9 đo ở 3.11 còn CI chạy 3.12; (d) ca CŨ bị sửa (`t178`, A2 bắt mở rộng) cũng
  vào vị từ nhưng không thuộc "ca mới".
- Vì sao P2: §6 mục 8 là mục tiêu chuẩn tắc, và lời khai "quên thì ĐỎ" rộng hơn phép đo duy nhất r9 làm (ca nhắc cấp đỉnh). Không P1:
  A8 vẫn là lưới chặn cuối.
- Phương án (HINT nhóm 2): nghĩa vụ = `mong` bằng đúng tập vị từ nhận dưới Python của CI, gồm ca sửa; tham chiếu helper ở cấp đỉnh.

### `hop-dong-dong-bang-thieu-neo` — P3 (VÁ SINH LỖI MỚI, hạ từ P2; lượt 1, 2, 7, 8, 9)
- F8-1 đóng vì Q12 bỏ B; F8-2 vá thật (ghi chú Q10). F9-4 (r9 :88–90): "khi và chỉ khi … `_thieu` 0 lỗi" — G7 đo `_thieu` 0 mà
  `kiem()` 1 vi phạm, và CI chạy `kiem()` trên kho thật. Không đổi đường land; chỉ là tiêu chí hẹp hơn cổng thật ⇒ P3.
- Nếu người điều phối tách F9-4 thành lớp riêng: hạng và hunk không đổi; lớp này thành ĐÃ VÁ THẬT và F tăng 1 (xem đối chiếu).

### `dieu-kien-dung-12-doc-mot-chuyen-tiep` — P3 (MỚI)
- F9-5 (r9 :756–759). Một chuyển tiếp < 50% chưa phải điểm dừng theo tỷ lệ; r9 viết như đã chạm và đã xử lý bằng Q12. Thứ đã kích
  hoạt (từ lượt 7, còn ở lượt 8) là luật một lớp ở ba lượt. Hệ quả thực tế: điểm dừng theo tỷ lệ được quyết ở chính lượt này (xem đối chiếu).

## DRY-RUN HINT.patch

`$R/goi/HINT.patch`: 145 dòng, 42147 byte, sha256 `af52b8b5262d921f7a95b15e33a997657fc44071ad2914dda52f0b415c87c861`.
4 nhóm `# lop:`: `thu-tu-677-bo-ngo-o-dieu-kien-cap` (2 hunk) · `tuong-tac-677-kiem-ke-t70-chua-neu` (5) ·
`hop-dong-dong-bang-thieu-neo` (1) · `dieu-kien-dung-12-doc-mot-chuyen-tiep` (1) = 9 hunk. Sinh bằng `$R/do.uiFp/sinh_hint.py`: kiểm
sha256 r9 trước khi sửa; mỗi chuỗi cũ xuất hiện đúng 1 lần trong r9; không dòng nào bị hai nhóm sửa; không ngữ cảnh nào chạm dòng nhóm
khác sửa (`assert`); mỗi nhóm là diff ĐỘC LẬP trên r9 gốc, 3 dòng ngữ cảnh; 0 dấu chéo ngược. Đường dẫn repo-relative, không `a/`/`b/`.

Lệnh (đúng PROMPT), trên tệp đã chép vào `goi/` (cmp khớp bản sinh), 06:00:00Z:
```
T=$(mktemp -d -p "$R") && cp -a "$R/cay-kho" "$T/cay"
cd "$T/cay" && patch -p0 --fuzz=0 --dry-run --verbose < "$R/goi/HINT.patch"
```
Output (T=`$R/tmp.LnfIFYulAf`, GNU patch 2.7.6): **rc=0**; 4 lần "checking file ops/specs/lease-id-ep-kieu-yaml-r9.md";
"Hunk #1 succeeded at 31." "Hunk #2 succeeded at 854." · "Hunk #1 succeeded at 301." "Hunk #2 succeeded at 340." "Hunk #3 succeeded at
379." "Hunk #4 succeeded at 404." "Hunk #5 succeeded at 449." · "Hunk #1 succeeded at 87." · "Hunk #1 succeeded at 755." · "done".
9/9 succeeded; 0 dòng FAILED/fuzz/offset/malformed; `git status --porcelain --ignored` của bản sao sau dry-run: 0 dòng.

Áp THẬT tuần tự (`$R/apthat3.O7XF`, `patch -p0 --fuzz=0`): rc=0; 9/9; một hunk báo offset 22 dòng (nhóm 4, do nhóm 2 và 3 chèn dòng
phía trên), 0 fuzz; 0 `.rej`/`.orig`; 997 → 1034 dòng; `cmp` với `do.uiFp/ky_vong.md` (bản dựng độc lập: áp mọi thay thế trên dòng gốc
bằng Python) ⇒ KHỚP từng byte. Áp RIÊNG từng nhóm trên r9 gốc (`$R/rieng2.81PU`): cả 4 rc=0, 0 offset/fuzz/FAILED.

Nhãn bắt buộc cho người áp (PROTOCOL §8 :600–601): *"chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit"*.
Đây là HINT cho một ĐẶC TẢ; mọi thay đổi thành revision 10; phiên soạn r10 phải đo lại mọi số và băm của chính r10 (các số hunk ghi
"review lượt 9 đo" là của lượt này, không phải phép đo của phiên soạn). HINT KHÔNG động vào chỗ phải đổi khi dựng r10 (tiêu đề
"revision 9", điều kiện (3) "đó là revision 9", công thức băm, tên tệp, bảng thay đổi đầu tệp, §9 bộ đếm sau lượt 9).
Theo §12 (đối chiếu ở trên), việc có dựng r10 bằng HINT này hay không là quyết định của Review Rescue Checkpoint, không của reviewer.

## GIỚI HẠN VÀ TOÀN VẸN
- KHÔNG ĐO ĐƯỢC từ `$R` (không mạng): trạng thái máy chủ (461 ref, người giữ live, lease #687 g3), REST PR #689 và #682, object
  `eca94d1`/`35e23d7`/`6112b89`, HINT lượt 7, hành vi của `claude` thật, lượt này có được giao qua `review-opus-max` hay không.
- Đọc NGOÀI `$R` (chỉ đọc, không in thân, không in bí mật): `~/.claude/agents/review-opus-max.md` (băm, cỡ, mtime, hai khoá frontmatter).
  Không đọc `~/.claude.json`, không in biến môi trường.
- Ghi: chỉ `$R/goi/` và các thư mục `mktemp -d -p "$R"` (`do.uiFp`, `tmp.xjYTdot3VW`, `tmp.zC4lvSxhW9`, `tmp.LnfIFYulAf`, `apthat.jPD7`,
  `apthat2.8q1O`, `apthat3.O7XF`, `rieng.QHw2`, `rieng2.81PU`). Hai bản HINT trước bản cuối (sha256 `758044…caf4`, `fe8cf6…9158`) chỉ
  khác câu chữ, đã được thay; bản trong `goi/` là bản cuối. `stale*.sh` đặt `HOME` vào thư mục con của `do.uiFp`. Mọi clone dùng
  `--no-local --no-hardlinks`; `kho.git` chỉ đọc (49 ref trước và sau).
- Tiến trình: một lệnh suite chạy nền (Python 3.12) do lượt này sinh, đã kết thúc rc=0; không gọi lệnh giết nào.
- `cay-kho` cuối lượt (06:00:55Z): HEAD `2469f3eb…`, tree `dee833ea756c…`, `status --porcelain --ignored` 0 dòng, 0 `.pyc`. Theo §8.2,
  snapshot sạch hai mốc không chứng minh chưa từng ghi rồi hoàn nguyên giữa chừng.
- Một lỗi đo của chính lượt này: `git diff -G` (phân biệt hoa thường) liệt kê thiếu verdict lượt 6 trong 16 dòng miễn trừ; đếm lại không
  phân biệt hoa thường ra đủ 16 kể cả lượt 6 — lời khai r9 đúng, con số ở Hướng F lấy từ lần đếm lại.
