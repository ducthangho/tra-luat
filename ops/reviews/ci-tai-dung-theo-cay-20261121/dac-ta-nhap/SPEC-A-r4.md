# Đặc tả packet — `CI-TAI-DUNG-THEO-CAY-A` (revision 4)

- `packet_id`: **CI-TAI-DUNG-THEO-CAY-A** · `revision`: **4** · trạng thái: nháp, chờ chủ kho duyệt băm (chạm **E5**, mục
  `pham_vi_e`). Thay r3 (sha256 `957c4bec3bd5f18d5804fccb5c721f854420e800129fd1af765b8f1adf27f0d5`, review lượt 2
  `changes_requested`), r2 (sha256 `3d878fedfcbe04d58558b0ae5eb8ba15a68b2f3e5a46ef3bf3bdd6e7aa6c99b3`, review lượt 1
  `changes_requested`) và r1 (sha256 `b20b6081802e29aa9bd01a3de48c9a5fab03af66df3ad2700df14b66bb2a33a5`); cả ba chưa từng
  được duyệt. Thay đổi so với r3: mục 10; so với r2: mục 9.
- `packet_issue`: **chưa có**. Issue và lease mở sau khi chủ kho duyệt băm (**E5**); Issue không tự cấp việc (protocol §3.2,
  §4). Packet anh em: `CI-TAI-DUNG-THEO-CAY-B1` (biên nhận và chạy bóng, `ops/specs/CI-TAI-DUNG-THEO-CAY-B1-r2.md`) và
  `CI-TAI-DUNG-THEO-CAY-B2` (kiểm lại và bật, `ops/specs/CI-TAI-DUNG-THEO-CAY-B2-r2.md`). Hai packet ấy thay packet `-B` của r1/r2.
  **B2 phụ thuộc A và B1**; A và B1 độc lập với nhau.
- `nguon_cap_viec`: chỉ thị chủ kho trong phiên Claude Code ngày 16-11-2026: *"Soạn Đ2"*, sau đó trả lời ba câu hỏi theo
  khuyến nghị: (1) phạm vi bản đầu **chỉ lượt `push` lên `master` sau merge**; (2) **chấp nhận** đổi luật bằng chứng hậu
  merge của `landed` **qua ADR mới**; (3) **tách packet, ADR trước**, thay cho một packet xin nâng trần. Ngày 20-11-2026, sau
  khi phiên điều phối (`local_cb926020-5197-4d05-9c66-1cdadb7f4591`) chuyển đề xuất **tạm hoãn** kèm số đo mới (mục 0), chủ
  kho trả lời nguyên văn *"Soạn r2"*. Packet `-B` tách thành B1 và B2 ở revision này, theo cùng lựa chọn (3): phạm vi thật
  của B (mục 0 của B1) vượt trần 450 dòng của `ADR-0053` nếu để một packet. Căn cứ phân tích:
  `ops/specs/CI-KHONG-CHAY-LAP-DE-XUAT-20261116.md` §4 Đ2 (PR #1320).
- `review_class`: **sensitive** — thêm ADR và sửa luật gate của protocol (protocol §8).
- Base dự kiến: `origin/master` lúc cấp lease (đo 09:2xZ 20-11-2026: `45bae8d07a8cdf06a1ca9a7a2e015a6258169379`).
- Executor **Claude**; reviewer **Codex** độc lập (phiên riêng); mức bảo đảm `human_audited` trên exact head trước merge
  (**E5**, `ADR-0067` quyết định 3). Điều kiện merge theo `ADR-0060`; M3 Windows `not_required` (diff chỉ `*.md` dưới
  `docs/**`).

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

(Ba phép đo của mục *Hiệu lực* trong hai ADR, đo 11:23Z 16-11-2026 trên `origin/master` `9c1661f7`: `cat-file -e L:ADR`
rc 0, `cat-file -e L^1:ADR` rc 128, `L` nằm trên `rev-list --first-parent origin/master` rc 0 — đủ cho cả hai OID. Người
cấp lease đo lại trên base lúc cấp.)

## 0. Vấn đề

Đo lần 1 (147 PR land 01→15-11-2026, bảng ở `ops/specs/CI-KHONG-CHAY-LAP-DE-XUAT-20261116.md` §2): 79 PR đi làn đầy đủ,
cả 79 merge bằng merge commit hai cha. Trong 79 PR ấy, **25** merge có cây của merge commit bằng cây mà lượt
`pull_request` xanh cuối đã checkout, **44** không bằng vì master đổi giữa lượt PR xanh cuối và lúc merge, **10** không đo
được. Kiểm chéo bằng log checkout thật của 8 PR, khớp 8/8.

Đo lần 2, sau #1343 (PR #1344, `packet_loop_test.py` chạy 16 mảnh, bảng đột biến sang workflow chạy hằng đêm) và #1353
(lượt `push` luôn chạy packet-loop): 28 lượt `push` lên `master` làn đầy đủ xanh, `created_at` từ 17-11 tới lúc đo
(trong 60 lượt `push` hoàn tất gần nhất, đo trước 09:00Z 20-11-2026). Trung vị thời gian tường **30,4 phút**, phút runner **266**; job `gate` 16,7 phút. Phút runner
theo nhóm job (cộng trung vị từng job): `gate-cong-cu` cộng `gate-cong-cu-gop` 146,4; `gate-ops` 25,3; `gate-nhanh-manh` cộng
`gate-nhanh-gop` cộng `gate-registry` 33,1; `gate-packet-loop-manh` cộng `gate-packet-loop` 41,7. Hàng đợi job (từ
`created_at` tới `started_at`; 40 lượt hoàn tất gần nhất mỗi sự kiện, chỉ lấy lượt từ 17-11): lượt `push` trung vị 2 giây, p99 878 giây; lượt `pull_request` p99 123
giây.

Ở lượt `pull_request`, bộ phân loại có thể cho cả nhóm packet-loop nghỉ (`packet_loop=bo_qua`) khi diff không chạm tập
phụ thuộc đo được (`PHU_THUOC_PACKET_LOOP`, `ops/ci_duong_nhanh.py:138` trên `45bae8d0`); ở lượt `push` thì luôn chạy
(`:411`). Nên lượt `push` chỉ tái dùng được **từng nhóm job** mà lượt PR đã thực sự chạy xanh, không tái dùng cả lượt.

Hai câu của protocol hiện cấm tái dùng theo cây (số dòng trên `45bae8d0`):

- §10.1 (`docs/PROTOCOL_DA_PHIEN.md:909-910`): *"Evidence chỉ được reuse khi tested SHA/tree, policy/catalog,
  runner, OS/runtime matrix và artifact hash (nếu có) khớp chính xác; head hoặc một identity đổi thì chạy lại."* Merge
  commit luôn có SHA khác commit merge tổng hợp mà lượt PR đã test.
- §10.2.2 (`:975-977`): *"Tree bằng nhau không đồng nhất commit, thời điểm, workflow, loại test hoặc runtime; không tự nâng
  test head thành test merge hoặc test Windows."*

`landed` (§10.2.4) đòi "hậu-merge gate xanh", và hồ sơ land neo hậu-merge gate vào lượt `push` trên đúng merge SHA với bốn
mốc §10.2.2 (ví dụ `ops/land/pr997-wp978-land-evidence.yaml`, khối `post_merge_checks`). #1353 sửa đúng điểm ấy cho
packet-loop: job gom hậu merge phải in dấu hiệu dương.

Hàng T4 của bảng §10.1 (`:903`) cũng đòi "toàn bộ exact identity khớp" cho reuse ở mốc canonical.

Packet này chỉ đổi **luật**. Mã CI làm theo luật ấy thuộc B1 (chạy bóng) và B2 (bật).

## 1. write_set

- `docs/adr/0068-tai-dung-ket-qua-ci-theo-cay-cho-gate-hau-merge.md` — MỚI.
- `docs/PROTOCOL_DA_PHIEN.md` — đúng bốn phép chèn, không sửa gì khác: nối câu P1 sau câu reuse của §10.1 (`:909-910`), thay
  hàng T4 (`:903`) bằng `T4_MOI` (hàng cũ cộng một vế ở ô cuối), nối câu P2 sau câu tree của §10.2.2 (`:975-977`), thêm dòng
  `DONG20` ngay sau dòng `ADR-0067` của bảng §20 (`:1562`). Số dòng trên `45bae8d0`.

Điều kiện cấp lease: không lease nào còn hiệu lực giữ một đường dẫn của write set, đo bằng
`python ops/lease_publish.py ai-dang-giu --root <kho bare> <đường dẫn>` trên một kho bare mà tập `refs/heads/*` khớp máy
chủ. Kết quả đo lúc soạn ở mục 8. Người cấp lease đo lại ngay trước khi cấp (L5).

Số ADR: không nhánh nào trên máy chủ có tệp mang tiền tố `docs/adr/0068-` (mục 8). Số bị chiếm lúc thi hành ⇒ DỪNG,
revision mới đổi số; không tự chọn số khác.

## 2. ngoai_pham_vi

- Mã CI, test, workflow: B1 và B2.
- Lượt `pull_request` và `workflow_dispatch`: không tái dùng (chủ kho chọn phạm vi chỉ `push` lên `master`). Check bắt buộc
  của cổng merge trên PR không đổi nghĩa.
- Windows: lượt `push` lên `master` chỉ có ma trận `ubuntu-latest` (output `os` của job `chuan-bi`); ADR không đổi nghĩa vụ
  Windows của `ADR-0060`.
- `kiem-merge` (K2 CI, `.claude/dev/packet_loop.py:3646` trên `45bae8d0`) đọc check trên head của PR trước merge; không đổi.
- Merge kiểu squash hay rebase (một cha) và lượt `push` mang nhiều commit (`github.event.before` khác P1): không tái dùng.
- Hồ sơ land đã ghi: không hồi tố.
- `.claude/skills/land-packets/SKILL.md`: không sửa; adapter trỏ về protocol, luật mới nằm ở ADR và §20.
- Bảng đột biến packet-loop chạy hằng đêm (`.github/workflows/packet-loop-dot-bien.yml`): không liên quan, không đổi.

## 3. muc_tieu

Văn bản nguyên văn của mọi câu bắt buộc nằm trong **phụ lục A** (script `kiem_a.py`, các hằng `Q`, `R`, `K`, `G`, `C`,
`P1`, `P2`, `T4_MOI`, `DONG20`). Phụ lục là nguồn duy nhất; mục này chỉ gọi tên.

1. `docs/adr/0068-tai-dung-ket-qua-ci-theo-cay-cho-gate-hau-merge.md` — ADR mới, có đủ:
   - a. Dòng đầu `# ADR-0068 — <tên>` và dòng `- **Trạng thái:** Accepted — hiệu lực từ commit land của packet
     ``CI-TAI-DUNG-THEO-CAY-B2`` …` kèm URL comment chủ kho duyệt băm đặc tả này (**E5**; executor điền URL thật).
   - b. Năm mục, mỗi mục đúng một lần và theo thứ tự: `## Bối cảnh`, `## Quyết định`, `## Giới hạn`, `## Hiệu lực`,
     `## Cưỡng chế`. Được có mục khác xen giữa.
   - c. `## Bối cảnh`: chứa ba đoạn K1–K3 (số đo kèm thời điểm và nguồn, L5); được có đoạn khác.
   - d. `## Quyết định`: **đúng tám đoạn** Q1–Q8, đúng thứ tự, không khối nào khác (kể cả bảng); mỗi đoạn được ngắt dòng
     tuỳ ý.
   - e. `## Giới hạn`: chứa năm đoạn G1–G5 (được có đoạn khác).
   - f. `## Hiệu lực`: chứa đoạn R.
   - g. `## Cưỡng chế`: chứa đoạn C.
2. `docs/PROTOCOL_DA_PHIEN.md`: đúng bốn phép chèn P1, P2, `T4_MOI` (thay hàng T4 cũ) và `DONG20`; phần còn lại giữ nguyên
   từng chữ.

## 4. nghiem_thu

| # | tiêu chí | phép đo làm nó ĐỎ | đột biến phải làm nó đổi màu |
|---|---|---|---|
| A1 | `python .claude/dev/packet_loop.py adr-song --root .` rc 0 trên head | rc ≠ 0 | bỏ `DONG20` ⇒ rc 9 (đo 20-11 trên gốc tạm, mục 8) |
| A2 | `kiem_a.py` in `A2 DAT`: mục Quyết định gồm đúng tám đoạn Q1–Q8, không khối nào khác | `A2 DO` | thêm đoạn thứ chín; thêm một bảng; đổi `cha P1, P2 theo` thành `cha P2, P1 theo`; đổi Q4 về "mọi job ngoài"; mỗi câu Q đổi một từ khoá ⇒ `DO`. Ngắt dòng lại một đoạn ⇒ vẫn `DAT` |
| A3 | `kiem_a.py` in `A3 DAT`: mục Hiệu lực chứa đoạn R | `A3 DO` | đổi `-B2` thành `-B1` trong R; đảo mục ⇒ `DO` |
| A4 | `kiem_a.py` in `A4 DAT`: protocol của head bằng protocol của BASE cộng **đúng** bốn phép chèn, so theo khối đã chuẩn hoá khoảng trắng; mỗi chỗ chèn có đúng một lần trên BASE | `A4 DO` | xoá câu "Top-level path filter…" ở §10.1; bỏ P2; nhân đôi `DONG20` ⇒ `DO` |
| A5 | `git diff --numstat BASE H` có đúng **hai** đường dẫn, đúng là hai đường dẫn của write set | thừa hay thiếu đường dẫn | thêm một tệp thứ ba ⇒ đỏ |
| A6 | `kiem_a.py` in `A6 DAT`: tiêu đề, dòng Trạng thái kèm URL `issues/<số>#issuecomment-<số>`, năm mục đúng thứ tự mỗi mục một lần, đủ K1–K3, G1–G5, có đoạn C | `A6 DO` | bỏ G3; Bối cảnh rỗng; bỏ URL; đảo hai mục ⇒ `DO` |
| A7 | `python .claude/dev/packet_loop.py doctrine-scan --root .` rc 0 | rc ≠ 0 | chép nguyên câu P1 vào `.claude/skills/land-packets/SKILL.md` ⇒ rc 6 (đo 20-11, mục 8) |
| A8 | CI của PR (`ci.yml`, làn đầy đủ) xanh trên head cuối | một job bắt buộc đỏ | — (cổng hiện hành; răng là của các bộ test đã có) |

Lệnh của A2, A3, A4, A6: `python kiem_a.py docs/adr/0068-tai-dung-ket-qua-ci-theo-cay-cho-gate-hau-merge.md
docs/PROTOCOL_DA_PHIEN.md <protocol của BASE>` (protocol của BASE lấy bằng `git show BASE:docs/PROTOCOL_DA_PHIEN.md`); rc 0
⇔ cả bốn `DAT`. Executor chép script từ phụ lục ra tệp tạm, không đưa vào kho.

Bảng năm vế của L6 cho các tiêu chí khớp chuỗi:

| vế | áp dụng |
|---|---|
| (a) vế dương trên nội dung mới, vế âm trên nội dung cũ | A2, A3, A6 dương trên ADR mới; A4 vừa đòi bốn phép chèn có mặt, vừa đòi mọi khối khác bằng BASE (vế âm cho nội dung cũ) |
| (b) nối dòng | mọi phép so chạy trên khối đã gộp khoảng trắng trong phạm vi một đoạn; đột biến ngắt dòng lại giữ xanh (đo 20-11) |
| (c) đếm theo vị trí | A2 so danh sách đoạn theo thứ tự; A4 đếm từng chỗ chèn đúng một lần trên BASE |
| (d) dạng chữ và chữ số | không áp dụng: phép so là bằng nguyên đoạn, không dò lời khai bằng regex; con số duy nhất (`20` ở Q8) nằm trong câu nguyên văn |
| (e) lời khai "0 cổng" | đã đo trên đủ sáu vị trí cổng mà `ADR-0054` dùng (mục 8) |

Chạy thử trước đóng băng (20-11-2026, mục 8): trên nền A2, A3, A4, A6 đều `DO`; trên một ADR và protocol ứng viên tối thiểu
cả bốn `DAT`; mười ba đột biến, mỗi cái làm đúng tiêu chí của nó đổi màu.

## 5. luat_dung

- Trần kích thước `ADR-0053` (dòng khai ở đầu tệp): dự kiến khoảng 110 dòng thêm (ADR khoảng 105, protocol 4 dòng chèn).
  Vượt trần ⇒ dừng và hỏi chủ kho mã **E2**, mang số `git diff --numstat`, trần đang áp, trần xin và lý do không tách được.
- Trần lời gọi Codex theo bảng của `ADR-0055` (dòng khai ở đầu tệp). Chạm trần ⇒ hỏi chủ kho mã **E2**, mang số lời gọi đã
  dùng, finding còn mở và số lời gọi xin thêm.
- Điểm dừng §12 của protocol và Review Rescue Checkpoint của `ADR-0037`: dẫn nguyên, không chép.
- Số `0068` bị chiếm lúc thi hành ⇒ dừng phiên, revision mới (mục 1); không phải điểm hỏi.

## 6. pham_vi_e

- E4: **không chạm** (không hành động ra ngoài kho, không xoá ref, không secret).
- E5: **chạm** theo luật "không rõ thì coi là thuộc" của `ADR-0067`: ADR đổi luật bằng chứng của hậu-merge gate, thứ
  quyết định `landed`. Hệ quả, mỗi việc mang mã **E5**: chủ kho duyệt băm đặc tả này, chủ kho cấp lease, chủ kho audit trước
  merge. Mỗi lần hỏi E5 mang đủ ba thứ của bảng `ADR-0067`: **diff** (đặc tả này khi duyệt băm; diff của PR khi audit),
  **lý do** (luật bằng chứng của `landed` cho phép lượt `pull_request` cùng cây thay lượt `push` cho các nhóm job được tái
  dùng), và **ai được thêm quyền gì** (không ai được thêm quyền; bộ xét của CI được phép bỏ nhóm job theo `ADR-0068`).

## 7. hinh_dang_ke_thua

`khong_ap_dung` — không phải packet khắc phục. Ghi chú cho người soạn revision sau: cặp tiền lệ cùng hình dạng (ADR ở
packet A, hiệu lực từ land packet mã) là `THU-HOI-ADMISSION-MERGE-BASE-A/-B`; lớp lỗi đắt nhất của cặp ấy nằm ở **tiêu chí
canary sau land của packet mã** (tám revision), không ở packet A.

## 8. Đo lúc soạn và chua_do_duoc

Đo lúc soạn (20-11-2026, `origin/master` `45bae8d07a8cdf06a1ca9a7a2e015a6258169379`):

- `ai-dang-giu` trên `D:/tlscan.git`, tập `refs/heads/*` khớp máy chủ (366/366 nhánh lúc 09:15:32Z, thiếu cục bộ 0, thừa 0):
  `docs/adr/0068-tai-dung-ket-qua-ci-theo-cay-cho-gate-hau-merge.md` ⇒ `NGƯỜI_GIỮ 0` (09:15:32Z–09:18:08Z);
  `docs/PROTOCOL_DA_PHIEN.md` ⇒ `NGƯỜI_GIỮ 0` (09:18:08Z–09:21:47Z).
- Số ADR: `git -C D:/tlscan.git log --branches --format= --name-only -- 'docs/adr/0068-*'` ⇒ rỗng (sau lượt quét trên).
- Lời khai "0 cổng" lúc land A: `rg -cw 'ADR-0068|tai_dung_bo|bien-nhan-cay|kiem-tai-dung|TAI_DUNG'` trên sáu vị trí cổng
  (`ops/lease_publish.py`, `.claude/dev/packet_loop.py`, `.claude/dev/launcher.py`, `.claude/dev/gate_lifecycle.py`,
  `.github/workflows/ci.yml`, `.github/workflows/ops-publish-lease.yml`) và `ops/ci_duong_nhanh.py` ⇒ **0** dòng ở mỗi tệp.
- Chạy thử tiêu chí trên một gốc tạm (bản sao `docs/adr/`, `.claude/skills/`, `.agents/`, `CLAUDE.md`, `AGENTS.md` của
  `45bae8d0`), đo lại 20-11-2026 với ADR ứng viên của r4: `adr-song` rc 0 trên nền và trên ứng viên, rc 9 khi bỏ `DONG20`;
  `doctrine-scan` rc 0 trên nền và ứng viên, rc 6 khi chép P1 vào `.claude/skills/land-packets/SKILL.md`. `kiem_a.py` (đúng bản
  ở phụ lục): nền `A2 A3 A4 A6` đều `DO`; ứng viên cả bốn `DAT`; xoá câu khác của §10.1 ⇒ `A4 DO`; thêm đoạn Quyết định ⇒
  `A2 DO`; thêm bảng vào Quyết định ⇒ `A2 DO`; đổi `P1, P2` ⇒ `A2 DO`; đổi Q4 ⇒ `A2 DO`; bỏ G3 ⇒ `A6 DO`; Bối cảnh rỗng ⇒
  `A6 DO`; đảo mục ⇒ `A3 DO`, `A6 DO`; bỏ P2 ⇒ `A4 DO`; ngắt dòng lại Q1 ⇒ cả bốn `DAT`; đổi `-B2` ⇒ `A3 DO`; bỏ URL ⇒
  `A6 DO`; nhân đôi `DONG20` ⇒ `A4 DO`.

Chưa đo được:

- Tỷ lệ merge cây trùng **sau** khi B2 land: số 25/79 là của 01→15-11; tương lai tuỳ cách merge và nhịp master.
- Nội dung ADR chạy được hay không phụ thuộc mã của B1, B2; packet A tự nó không đổi hành vi CI nào (đúng câu R).

## 9. Thay đổi so với r2

Theo review lượt 1 (Codex, `changes_requested`, 1 P1, 6 P2, 3 P3):

- F1 (P1): Q2 thêm phép `github.event.before` bằng P1; Q7 viết lại thành so **kế hoạch** của chính hàm lập kế hoạch, không so
  tập tệp của bộ phân loại.
- F4: Q3 đòi `run_attempt` bằng 1, nói rõ chỉ so ảnh runner của job `chuan-bi`, và đòi đủ chỉ số ma trận; thêm G3 khai giới
  hạn ấy.
- F5: thêm phép chèn `T4_MOI` vào hàng T4; câu R viết lại (không còn khai "chạy đủ như cũ"); Q4 giới hạn vào lượt đang xét
  tái dùng; Q5 tách lỗi chung với lỗi riêng của nhóm.
- F6: A4 nay so **cả** protocol với BASE cộng đúng bốn phép chèn; A2 đòi đúng tám đoạn; thêm A6 cho cấu trúc ADR. Văn bản
  nguyên văn chuyển vào phụ lục A cùng script đo.
- F10: thêm bảng năm vế L6, phép đo "0 cổng" trên sáu vị trí, chạy thử mọi tiêu chí trước đóng băng; mọi câu hỏi chủ kho
  mang mã E kèm thứ phải mang theo.
- Thêm Q8: bộ xét phải chạy bóng trước khi bật (B1), và chỉ bật (B2) khi đủ 20 lượt bóng có tái dùng mà không lượt nào sai.
- `nguon_cap_viec` ghi việc tách B thành B1, B2.

## 10. Thay đổi so với r3

Theo review lượt 2 (Codex, `changes_requested`, 7 P2, 3 P3; F1 của lượt 1 đã đóng):

- N5: A2 nay đòi mục Quyết định gồm đúng tám đoạn và **không khối nào khác**, kể cả bảng; A6 đòi Bối cảnh chứa ba đoạn K1–K3
  (số đo, thời điểm, nguồn). Hai đột biến reviewer dùng (bảng ngoại lệ, Bối cảnh rỗng) nay làm A2, A6 đỏ.
- Q4 viết lại theo bất biến thật: không job nào thuộc một nhóm tái dùng được có `if:` theo `github.ref` hay
  `github.event_name`. Lý do: B1 r2 thêm một job biên nhận riêng (chỉ ở lượt `pull_request`), không thuộc nhóm nào.
- Đoạn C nhắc lệnh `kiem-lai-tai-dung`, nay thuộc B2.
- N8: câu nhắc comment duyệt băm mang mã E5; mục `pham_vi_e` ghi đủ ba thứ phải mang theo khi hỏi E5.
- Tên đặc tả anh em: B1 r2, B2 r2.

## Phụ lục A — `kiem_a.py`

```python
# Kiem A2, A3, A4, A6 cua dac ta CI-TAI-DUNG-THEO-CAY-A. Dung: python kiem_a.py <ADR moi> <protocol ung vien> <protocol nen>
# In tung dong "A<n> DAT|DO <ly do>", rc 0 khi moi tieu chi DAT. Chi doc tep, khong dung git.
import re
import sys
from pathlib import Path

Q = [
    "Lượt `ci.yml` của sự kiện `push` lên `master` được bỏ một nhóm job nặng khi chứng minh được cây của commit vừa đẩy đã được "
    "một lượt `pull_request` ở làn `day_du` test, và mọi job của nhóm ấy đã `success` trong lượt đó.",
    "Chứng minh gồm đủ bốn phép: (1) commit vừa đẩy có đúng hai cha P1 và P2; (2) `github.event.before` của lượt `push` bằng P1; "
    "(3) lượt `pull_request` đã checkout một commit có đúng hai cha P1, P2 theo thứ tự ấy và cây bằng cây của commit vừa đẩy; "
    "(4) lượt `push` tự tính lại `git merge-tree --write-tree P1 P2` và ra đúng cây ấy.",
    "Lượt `pull_request` được tái dùng phải thuộc chính kho, chạy `.github/workflows/ci.yml`, có kết luận `success` ở lần chạy "
    "thứ nhất (`run_attempt` bằng 1), và có job `chuan-bi` chạy trên cùng `ImageOS` và `ImageVersion` với job `chuan-bi` của "
    "lượt `push`; nhóm nào thiếu một chỉ số ma trận, có job `skipped` hay khác `success` trong lượt ấy thì lượt `push` chạy nhóm đó.",
    "Trong lượt `push` đang xét tái dùng, job `gate` vẫn chạy đủ trên chính commit vừa đẩy; không job nào thuộc một nhóm tái "
    "dùng được có điều kiện `if:` theo `github.ref` hay `github.event_name`, ở cấp job hay cấp bước.",
    "Lỗi ở một phép chung của Q2 hay Q3, thiếu biên nhận, hay đọc API lỗi thì lượt `push` không bỏ nhóm nào; lỗi riêng của một "
    "nhóm chỉ làm lượt `push` chạy nhóm ấy.",
    "Với `landed`, hậu-merge gate của một merge commit có nhóm được tái dùng gồm bốn mốc §10.2.2 của lượt `push` (các job đã "
    "chạy, cùng dòng `TAI_DUNG: DAT` của job `gate`) cộng bốn mốc §10.2.2 của lượt `pull_request` cho các nhóm được tái dùng.",
    "Nhóm job nào chọn việc theo diff của sự kiện thì chỉ được tái dùng khi kế hoạch chọn việc của nó, tính bằng chính hàm lập "
    "kế hoạch của nó trên đầu vào của lượt `push`, bằng kế hoạch tính bằng hàm ấy trên đầu vào của lượt `pull_request`.",
    "Trước khi bật, bộ xét tái dùng chạy bóng trên lượt `push` lên `master`; chỉ được bật khi đã có ít nhất 20 lượt bóng đánh "
    "dấu ít nhất một nhóm tái dùng được, và không lượt nào có nhóm được đánh dấu tái dùng được mà chính lượt `push` ấy có job "
    "khác `success` trong nhóm đó.",
]
R = ("ADR này có hiệu lực từ commit land của packet `CI-TAI-DUNG-THEO-CAY-B2`; trước đó lượt `push` lên `master` không tái "
     "dùng kết quả của lượt `pull_request` nào, và bộ phân loại hiện hành giữ nguyên.")
G = [
    "Hai lượt được phép khác nhau ở SHA commit, thời điểm và sự kiện (`pull_request` với `push`); cây, cha và định nghĩa "
    "workflow phải bằng nhau.",
    "ADR này không cho tái dùng ở lượt `pull_request`, ở `workflow_dispatch`, trên Windows, hay cho merge commit một cha.",
    "Ảnh runner chỉ được so ở job `chuan-bi` của hai lượt; ảnh của từng job nặng không được đo riêng.",
    "Một lần xanh được dùng lại thay vì chạy thêm, nên lỗi chập chờn của nhóm được tái dùng lộ ít hơn.",
    "Nhóm packet-loop bị bỏ ở lượt `pull_request` (`packet_loop=bo_qua`) thì không tái dùng được, nên lượt `push` vẫn chạy nó "
    "và job gom vẫn in dấu hiệu dương như #1353 đòi.",
]
C = ("Lúc land packet A: 0 cổng. Sau land `CI-TAI-DUNG-THEO-CAY-B1`: `ops/ci_duong_nhanh.py` tính quyết định ở chế độ chạy "
     "bóng, chưa bỏ job nào. Sau land `CI-TAI-DUNG-THEO-CAY-B2`: `ops/ci_duong_nhanh.py` và điều kiện cấp job trong "
     "`.github/workflows/ci.yml` (output `tai_dung_bo`), bước in `TAI_DUNG: DAT` của job `gate`, và lệnh "
     "`kiem-lai-tai-dung` tính lại quyết định của một lượt `push` từ REST và git.")
K = [
    "Đo trên 147 PR land từ 01 đến 15-11-2026: 79 PR đi làn đầy đủ, cả 79 merge bằng merge commit hai cha; 25 merge có cây "
    "trùng cây lượt `pull_request` xanh cuối, 44 không trùng vì master đổi, 10 không đo được.",
    "Đo 20-11-2026 trên 28 lượt `push` lên `master` làn đầy đủ xanh từ 17-11-2026: thời gian tường trung vị 30,4 phút, phút "
    "runner trung vị 266, job `gate` trung vị 16,7 phút.",
    "Nguồn: `ops/specs/CI-KHONG-CHAY-LAP-DE-XUAT-20261116.md` §2 và mục 0 của đặc tả packet `CI-TAI-DUNG-THEO-CAY-A`.",
]
MUC = ["Bối cảnh", "Quyết định", "Giới hạn", "Hiệu lực", "Cưỡng chế"]
TRANG_THAI = re.compile(r"- \*\*Trạng thái:\*\* Accepted — hiệu lực từ commit land của packet `CI-TAI-DUNG-THEO-CAY-B2`.*"
                        r"https://github\.com/ducthangho/tra-luat/issues/\d+#issuecomment-\d+")
# Protocol: bon phep chen, moi phep dung mot cho.
S_REUSE = ("Evidence chỉ được reuse khi tested SHA/tree, policy/catalog, runner, OS/runtime matrix và artifact hash (nếu có) "
           "khớp chính xác; head hoặc một identity đổi thì chạy lại.")
P1 = "Ngoại lệ duy nhất là lượt `push` lên `master` theo `ADR-0068`."
S_TREE = ("Tree bằng nhau không đồng nhất commit, thời điểm, workflow, loại test hoặc runtime; không tự nâng test head thành "
          "test merge hoặc test Windows.")
P2 = "Ngoại lệ duy nhất: hậu-merge gate theo `ADR-0068`."
T4_CU = ("| T4 | canonical/`merge_group` | full trên candidate canonical, hoặc reuse duy nhất evidence T3 khi toàn bộ exact "
         "identity khớp |")
T4_MOI = ("| T4 | canonical/`merge_group` | full trên candidate canonical, hoặc reuse duy nhất evidence T3 khi toàn bộ exact "
          "identity khớp; hậu-merge gate của lượt `push` lên `master` tái dùng theo nhóm job của `ADR-0068` |")
DONG20_SAU = "| `ADR-0067` |"
DONG20 = ("| `ADR-0068` | Tái dùng kết quả CI theo cây: lượt `push` lên `master` bỏ nhóm job nặng mà lượt `pull_request` xanh "
          "làn `day_du` đã test trên cùng cây; chạy bóng trước khi bật | Accepted — hiệu lực từ land `CI-TAI-DUNG-THEO-CAY-B2` "
          "| 0 cổng (lúc land A); sau land B1: `ops/ci_duong_nhanh.py` (chạy bóng); sau land B2: `ops/ci_duong_nhanh.py` và "
          "`.github/workflows/ci.yml` (`tai_dung_bo`) |")


def khoi(text):
    """Danh sach khoi tach theo dong trong. Khoi bang (moi dong bat dau `|`) giu tung dong; khoi khac gop khoang trang."""
    ra = []
    for k in re.split(r"\n[ \t]*\n", text.replace("\r\n", "\n")):
        dong = [d for d in k.split("\n") if d.strip()]
        if not dong:
            continue
        if all(d.lstrip().startswith("|") for d in dong):
            ra.extend(("BANG", d.strip()) for d in dong)
        else:
            ra.append(("DOAN", " ".join(" ".join(dong).split())))
    return ra


def muc(text, ten):
    m = [x for x in re.finditer(r"(?m)^## (.+?)\s*$", text)]
    for i, x in enumerate(m):
        if x.group(1).strip() == ten:
            return text[x.end(): m[i + 1].start() if i + 1 < len(m) else len(text)]
    return None


def doan(text):
    return [v for loai, v in khoi(text) if loai == "DOAN"]


def kiem(adr, proto, nen):
    kq = {}
    qd = muc(adr, "Quyết định")
    kq["A2"] = (qd is not None and khoi(qd) == [("DOAN", q) for q in Q],
                "Quyết định phải gồm đúng tám đoạn Q1–Q8, đúng thứ tự, không khối nào khác (kể cả bảng)")
    hl = muc(adr, "Hiệu lực")
    kq["A3"] = (hl is not None and R in doan(hl), "Hiệu lực thiếu câu R")
    k_nen, k_moi = khoi(nen), khoi(proto)
    mong, dem = [], {"reuse": 0, "tree": 0, "t4": 0, "d20": 0}
    for loai, v in k_nen:
        if loai == "DOAN" and S_REUSE in v:
            dem["reuse"] += 1
            v = v.replace(S_REUSE, S_REUSE + " " + P1)
        if loai == "DOAN" and S_TREE in v:
            dem["tree"] += 1
            v = v.replace(S_TREE, S_TREE + " " + P2)
        if loai == "BANG" and v == T4_CU:
            dem["t4"] += 1
            v = T4_MOI
        mong.append((loai, v))
        if loai == "BANG" and v.startswith(DONG20_SAU):
            dem["d20"] += 1
            mong.append(("BANG", DONG20))
    kq["A4"] = (all(n == 1 for n in dem.values()) and k_moi == mong,
                f"protocol phải bằng nền cộng đúng bốn phép chèn (đếm chỗ chèn trên nền: {dem})")
    tieu_de = [x.group(1).strip() for x in re.finditer(r"(?m)^## (.+?)\s*$", adr)]
    thu_tu = [t for t in tieu_de if t in MUC]
    gh, cc, bc = muc(adr, "Giới hạn"), muc(adr, "Cưỡng chế"), muc(adr, "Bối cảnh")
    dau = adr.split("\n## ", 1)[0]
    kq["A6"] = (thu_tu == MUC and all(tieu_de.count(t) == 1 for t in MUC)
                and re.match(r"# ADR-0068 — \S", adr) is not None and TRANG_THAI.search(" ".join(dau.split())) is not None
                and gh is not None and all(g in doan(gh) for g in G) and cc is not None and C in doan(cc)
                and bc is not None and all(x in doan(bc) for x in K),
                "cấu trúc ADR: năm mục đúng thứ tự, tiêu đề, dòng Trạng thái kèm URL, đủ K1–K3, G1–G5, đoạn Cưỡng chế")
    return kq


if __name__ == "__main__":
    adr_p, proto_p, nen_p = map(Path, sys.argv[1:4])
    adr = adr_p.read_text(encoding="utf-8") if adr_p.exists() else ""
    kq = kiem(adr, proto_p.read_text(encoding="utf-8"), nen_p.read_text(encoding="utf-8"))
    for k, (ok, ly_do) in kq.items():
        print(k, "DAT" if ok else "DO", "" if ok else ly_do)
    sys.exit(0 if all(ok for ok, _ in kq.values()) else 1)
```
