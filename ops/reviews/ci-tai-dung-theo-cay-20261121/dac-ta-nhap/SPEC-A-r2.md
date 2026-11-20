# Đặc tả packet — `CI-TAI-DUNG-THEO-CAY-A` (revision 2)

- `packet_id`: **CI-TAI-DUNG-THEO-CAY-A** · `revision`: **2** · trạng thái: nháp, chờ chủ kho duyệt băm (chạm E5, mục
  `pham_vi_e`). Thay `ops/specs/CI-TAI-DUNG-THEO-CAY-A-r1.md` (sha256
  `b20b6081802e29aa9bd01a3de48c9a5fab03af66df3ad2700df14b66bb2a33a5`, chưa từng được duyệt, giữ trong kho). Thay đổi so
  với r1: mục 9.
- `packet_issue`: **chưa có**. Issue và lease mở sau khi chủ kho duyệt băm; Issue không tự cấp việc (protocol §3.2, §4).
  Packet anh em: `CI-TAI-DUNG-THEO-CAY-B` (mã CI, đặc tả `ops/specs/CI-TAI-DUNG-THEO-CAY-B-r2.md`). **B phụ thuộc A**:
  base của B phải chứa commit land của A.
- `nguon_cap_viec`: chỉ thị chủ kho trong phiên Claude Code ngày 16-11-2026: *"Soạn Đ2"*, sau đó trả lời ba câu hỏi theo
  khuyến nghị: (1) phạm vi bản đầu **chỉ lượt `push` lên `master` sau merge**; (2) **chấp nhận** đổi luật bằng chứng hậu
  merge của `landed` **qua ADR mới**; (3) **hai packet, ADR trước**. Ngày 20-11-2026, sau khi phiên điều phối
  (`local_cb926020-5197-4d05-9c66-1cdadb7f4591`) chuyển đề xuất **tạm hoãn** kèm số đo mới (mục 0), chủ kho trả lời
  nguyên văn *"Soạn r2"* cho câu hỏi "tạm hoãn hay soạn r2?". Căn cứ phân tích: `ops/specs/CI-KHONG-CHAY-LAP-DE-XUAT-20261116.md`
  §4 Đ2 (PR #1320). Không có dòng kế hoạch trong `ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md`.
- `review_class`: **sensitive** — thêm ADR và sửa luật gate của protocol (protocol §8).
- Base dự kiến: `origin/master` lúc cấp lease (đo 09:2xZ 20-11-2026: `45bae8d07a8cdf06a1ca9a7a2e015a6258169379`).
- Executor **Claude**; reviewer **Codex** độc lập (phiên riêng); mức bảo đảm `human_audited` trên exact head trước merge
  (chạm E5, `ADR-0067` quyết định 3). Điều kiện merge theo `ADR-0060`.

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

Packet này chỉ đổi **luật**. Mã CI làm theo luật ấy thuộc packet B.

## 1. write_set

- `docs/adr/0068-tai-dung-ket-qua-ci-theo-cay-cho-gate-hau-merge.md` — MỚI.
- `docs/PROTOCOL_DA_PHIEN.md` — sửa đúng ba chỗ: nối một câu vào đoạn §10.1 chứa câu reuse ở trên, nối một câu vào đoạn
  §10.2.2 chứa câu tree ở trên, thêm một dòng vào bảng §20 ngay sau dòng `ADR-0067` (`:1562` trên `45bae8d0`).

Điều kiện cấp lease: không lease nào còn hiệu lực giữ một đường dẫn của write set, đo bằng
`python ops/lease_publish.py ai-dang-giu --root <kho bare> <đường dẫn>` trên một kho bare mà tập `refs/heads/*` khớp máy
chủ. Kết quả đo lúc soạn r2 ở mục 8. Người cấp lease đo lại ngay trước khi cấp (L5).

Số ADR: không nhánh nào trên máy chủ có tệp mang tiền tố `docs/adr/0068-` (mục 8). Số bị chiếm lúc thi hành ⇒ DỪNG,
revision mới đổi số; không tự chọn số khác.

## 2. ngoai_pham_vi

- Mã CI, test, workflow: packet B.
- Lượt `pull_request` và `workflow_dispatch`: không tái dùng (chủ kho chọn phạm vi chỉ `push` lên `master`). Check bắt buộc
  của cổng merge trên PR không đổi nghĩa.
- Windows: lượt `push` lên `master` chỉ có ma trận `ubuntu-latest` (output `os` của job `chuan-bi`); ADR không đổi nghĩa vụ
  Windows của `ADR-0060`.
- `kiem-merge` (K2 CI, `.claude/dev/packet_loop.py:3646` trên `45bae8d0`) đọc check trên head của PR trước merge; không đổi.
- Merge kiểu squash hay rebase (một cha): không tái dùng.
- Hồ sơ land đã ghi: không hồi tố.
- `.claude/skills/land-packets/SKILL.md`: không sửa; adapter trỏ về protocol, luật mới nằm ở ADR và §20.
- Bảng đột biến packet-loop chạy hằng đêm (`.github/workflows/packet-loop-dot-bien.yml`): không liên quan, không đổi.

## 3. muc_tieu

1. `docs/adr/0068-tai-dung-ket-qua-ci-theo-cay-cho-gate-hau-merge.md` — ADR mới, có đủ:
   - a. Tiêu đề `# ADR-0068 — …` và dòng `- **Trạng thái:** Accepted — hiệu lực từ commit land của packet
     \`CI-TAI-DUNG-THEO-CAY-B\` …`, kèm URL comment chủ kho duyệt băm đặc tả này (executor điền URL thật lúc thi hành).
   - b. Mục **Bối cảnh**: các số đo của mục 0, mỗi số kèm thời điểm đo và nguồn (L5).
   - c. Mục **Quyết định**, gồm đúng bảy câu dưới đây, chép **nguyên văn** (giữ dấu `` ` ``), mỗi câu nằm trọn trong một
     đoạn; được ngắt dòng tuỳ ý trong đoạn:
     - Q1: *"Lượt `ci.yml` của sự kiện `push` lên `master` được bỏ một nhóm job nặng khi chứng minh được cây của commit
       vừa đẩy đã được một lượt `pull_request` ở làn `day_du` test, và mọi job của nhóm ấy đã `success` trong lượt đó."*
     - Q2: *"Chứng minh gồm đủ ba phép: commit vừa đẩy có đúng hai cha P1 và P2; lượt `pull_request` đã checkout một commit
       có đúng hai cha P1, P2 theo thứ tự ấy và cây bằng cây của commit vừa đẩy; lượt `push` tự tính lại
       `git merge-tree --write-tree P1 P2` và ra đúng cây ấy."*
     - Q3: *"Lượt `pull_request` được tái dùng phải thuộc chính kho, chạy `.github/workflows/ci.yml`, có kết luận `success`
       ở lần chạy mới nhất, và chạy trên cùng `ImageOS` và `ImageVersion` với lượt `push`; nhóm nào có một job vắng,
       `skipped` hay khác `success` trong lượt ấy thì lượt `push` chạy nhóm đó."*
     - Q4: *"Job `gate` vẫn chạy đủ trên chính commit vừa đẩy; mọi bước có điều kiện `if:` theo `github.ref` hay
       `github.event_name` phải nằm trong job `gate` hoặc `chuan-bi`."*
     - Q5: *"Thiếu một phép, thiếu biên nhận, hay đọc API lỗi thì lượt `push` chạy đủ."*
     - Q6: *"Với `landed`, hậu-merge gate của một merge commit có nhóm được tái dùng gồm bốn mốc §10.2.2 của lượt `push`
       (các job đã chạy, cùng dòng `TAI_DUNG: DAT` của job `gate`) cộng bốn mốc §10.2.2 của lượt `pull_request` cho các
       nhóm được tái dùng."*
     - Q7: *"Nhóm job nào đọc diff của sự kiện để chọn việc thì chỉ được tái dùng khi tập tệp đổi tính cho lượt `push`
       bằng tập tệp đổi tính cho lượt `pull_request`."*
   - d. Mục **Giới hạn**: liệt kê những khác biệt được chấp nhận giữa hai lượt (SHA commit, thời điểm, sự kiện) và những
     thứ ADR **không** cho (tái dùng cho PR, cho `workflow_dispatch`, cho Windows, cho merge một cha); nói thẳng rủi ro test
     chập chờn: một lần xanh được dùng lại thay vì chạy thêm. Ghi rằng nhóm packet-loop bị bỏ ở lượt PR (`bo_qua`) thì lượt
     `push` vẫn chạy nó, nên điều #1353 đòi (dấu hiệu dương của job gom hậu merge) còn nguyên khi nhóm ấy không tái dùng được.
   - e. Mục **Hiệu lực**, chứa nguyên văn câu R: *"ADR này có hiệu lực từ commit land của packet `CI-TAI-DUNG-THEO-CAY-B`;
     trước đó lượt `push` lên `master` chạy đủ như cũ."*
   - f. Mục **Cưỡng chế**: lúc land A là **0 cổng**; sau land B là `ops/ci_duong_nhanh.py` (output `tai_dung_bo`) và job
     `gate` của `.github/workflows/ci.yml` (bước in `TAI_DUNG: DAT`).
2. `docs/PROTOCOL_DA_PHIEN.md`:
   - a. Nối vào cuối câu reuse của §10.1 (sau "…thì chạy lại.") đúng câu P1: *"Ngoại lệ duy nhất là lượt `push` lên
     `master` theo `ADR-0068`."*
   - b. Nối vào cuối câu tree của §10.2.2 (sau "…hoặc test Windows.") đúng câu P2: *"Ngoại lệ duy nhất: hậu-merge gate theo
     `ADR-0068`."*
   - c. Thêm một dòng §20 cho `ADR-0068`, cột cổng ghi "0 cổng (lúc land A); sau land B: `ops/ci_duong_nhanh.py`
     (`tai_dung_bo`)", đặt ngay sau dòng `ADR-0067`.
   - d. Không sửa câu nào khác: hai câu gốc ở mục 0 giữ nguyên chữ.

## 4. nghiem_thu

Mọi phép khớp chuỗi đo trên văn bản Markdown thô (giữ dấu `` ` ``) **đã nối dòng trong phạm vi từng đoạn** (gộp mọi chuỗi
khoảng trắng thành một dấu cách, không nối qua dòng trống), khớp **toàn bộ** câu (L6 b). "Đoạn" của protocol là khối dòng
liền nhau giữa hai dòng trống.

| # | tiêu chí | phép đo làm nó ĐỎ | đột biến phải làm nó đổi màu |
|---|---|---|---|
| A1 | `python .claude/dev/packet_loop.py adr-song --root .` rc 0 trên head | rc ≠ 0 | xoá dòng §20 vừa thêm ⇒ rc ≠ 0 |
| A2 | Mục Quyết định của ADR chứa nguyên câu Q1 tới Q7 — **bảy** phép khớp riêng, mỗi câu một vị trí (L6 c) | một câu không khớp | với mỗi câu: đổi một từ khoá (`push`→`pull_request` ở Q1, `P1, P2`→`P2, P1` ở Q2, `skipped`→`failure` ở Q3, `gate`→`gate-ops` ở Q4, `chạy đủ`→`bỏ` ở Q5, `cộng`→`hoặc` ở Q6, `bằng`→`chứa` ở Q7) ⇒ không khớp; ngắt dòng lại trong đoạn mà giữ chữ ⇒ vẫn khớp |
| A3 | Mục Hiệu lực của ADR chứa nguyên câu R | không khớp | đổi `-B` thành `-A` ⇒ không khớp |
| A4 | Đoạn §10.1 chứa câu reuse gốc **và** câu P1 nối ngay sau nó; đoạn §10.2.2 chứa câu tree gốc **và** câu P2 nối ngay sau nó — bốn phép khớp, mỗi câu một vị trí | một trong bốn không khớp | xoá câu gốc §10.1 ⇒ đỏ (vế âm cho nội dung cũ); bỏ chữ `duy nhất` ở P2 ⇒ đỏ |
| A5 | `git diff --numstat BASE H` có đúng **hai** đường dẫn, đúng là hai đường dẫn của write set | thừa hay thiếu đường dẫn | thêm một tệp thứ ba ⇒ đỏ |
| A6 | Mọi hunk của `git diff -U0 BASE H -- docs/PROTOCOL_DA_PHIEN.md` nằm trong một trong ba vùng: đoạn §10.1 chứa câu reuse, đoạn §10.2.2 chứa câu tree, bảng §20 | một hunk ngoài ba vùng | sửa một chữ ở §10.2.1 ⇒ đỏ |
| A7 | `python .claude/dev/packet_loop.py doctrine-scan --root .` rc 0 | rc ≠ 0 | cổng canh bất biến, xanh sẵn trên nền. Executor thử một đột biến trên bản sao: chép nguyên câu P1 vào `.claude/skills/land-packets/SKILL.md`. Nếu rc vẫn 0 thì ghi thẳng "A7 không có đột biến riêng" trong handoff; không sửa cổng (ngoài write set) |
| A8 | CI của PR (`ci.yml`, làn đầy đủ vì `docs/` không thuộc làn hồ sơ) xanh trên head cuối | một job bắt buộc đỏ | — (cổng hiện hành; răng của nó là của các bộ test đã có) |

Chạy thử trên nền `45bae8d0`: A1 và A7 dự kiến xanh sẵn (cổng canh bất biến); A2, A3, A4 đỏ vì chưa có ADR và chưa có câu
mới (tiêu chí hành vi mới phải ra màu "chưa làm"). Executor ghi lại phép chạy thử ấy trong handoff lượt đầu.

## 5. luat_dung

- Trần kích thước `ADR-0053` (dòng khai ở đầu tệp): dự kiến khoảng 100 dòng thêm (ADR khoảng 95, protocol 3). Vượt trần ⇒
  dừng; nâng trần là **E2** (mang số `git diff --numstat` và lý do không tách được).
- Trần lời gọi Codex theo bảng của `ADR-0055` (dòng khai ở đầu tệp). Chạm trần ⇒ **E2**.
- Điểm dừng §12 của protocol và Review Rescue Checkpoint của `ADR-0037`: dẫn nguyên, không chép.
- Số `0068` bị chiếm lúc thi hành ⇒ dừng phiên, revision mới (mục 1); không phải điểm hỏi.

## 6. pham_vi_e

- E4: **không chạm** (không hành động ra ngoài kho, không xoá ref, không secret).
- E5: **chạm** theo luật "không rõ thì coi là thuộc" của `ADR-0067`: ADR đổi luật bằng chứng của hậu-merge gate, thứ
  quyết định `landed`. Hệ quả: chủ kho duyệt băm đặc tả này, chủ kho cấp lease, và chủ kho audit trước merge.

## 7. hinh_dang_ke_thua

`khong_ap_dung` — không phải packet khắc phục. Ghi chú cho người soạn revision sau: cặp tiền lệ cùng hình dạng (ADR ở
packet A, hiệu lực từ land packet B) là `THU-HOI-ADMISSION-MERGE-BASE-A/-B`; lớp lỗi đắt nhất của cặp ấy nằm ở **tiêu chí
canary sau land của packet B** (tám revision), không ở packet A.

## 8. Đo lúc soạn r2 và chua_do_duoc

Đo lúc soạn (20-11-2026, `origin/master` `45bae8d07a8cdf06a1ca9a7a2e015a6258169379`):

- `ai-dang-giu` trên `D:/tlscan.git`, tập `refs/heads/*` khớp máy chủ (366/366 nhánh lúc 09:15:32Z, thiếu cục bộ 0, thừa 0):
  `docs/adr/0068-tai-dung-ket-qua-ci-theo-cay-cho-gate-hau-merge.md` ⇒ `NGƯỜI_GIỮ 0` (09:15:32Z–09:18:08Z);
  `docs/PROTOCOL_DA_PHIEN.md` ⇒ `NGƯỜI_GIỮ 0` (09:18:08Z–09:21:47Z).
- Số ADR: `git -C D:/tlscan.git log --branches --format= --name-only -- 'docs/adr/0068-*'` ⇒ rỗng (sau lượt quét trên).

Chưa đo được:

- Tỷ lệ merge cây trùng **sau** khi B land: số 25/79 là của 01→15-11; tương lai tuỳ cách merge và nhịp master. Tỷ lệ lượt
  PR có nhóm packet-loop `bo_qua`: chưa đo.
- Nội dung ADR chạy được hay không phụ thuộc mã của B; packet A tự nó không đổi hành vi CI nào (A land xong, lượt `push`
  vẫn chạy đủ, đúng câu R).

## 9. Thay đổi so với r1

- Tái dùng theo **nhóm job** thay cho cả lượt: Q1 và Q3 viết lại; thêm Q7 (nhóm đọc diff của sự kiện); Q6 nói "các nhóm
  được tái dùng". Lý do: sau #1343, lượt PR có thể cho cả nhóm packet-loop nghỉ, nên lượt `push` không có kết quả packet-loop
  để tái dùng cho những PR ấy (mục 0).
- Mục 0 thêm đo lần 2 sau #1343/#1353; số dòng protocol và `packet_loop.py` đo lại trên `45bae8d0` (§10.1 `:909-910`,
  §10.2.2 `:975-977`, §20 `:1562`, K2 `:3646`; r1 ghi số trên `9c1661f7`).
- `nguon_cap_viec` thêm quyết định *"Soạn r2"* của chủ kho ngày 20-11-2026.
- A2: bảy câu thay cho sáu.
- Mục `luat_dung` bỏ dòng E3 về tỷ lệ cây trùng gần 0: chủ kho đã thấy số đo lần 2 và vẫn chọn làm.
