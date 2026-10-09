---
kieu: dac_ta_packet
packet: CI-SONG-SONG-REGISTRY-G5-MOT-LAN
packet_id: CI-SONG-SONG-REGISTRY-G5-MOT-LAN
ban: r1
trang_thai: nhap              # NHÁP — chưa đóng băng. Chủ kho đo sha256 từ blob, đăng băm lên Issue packet, rồi mới có lease.
packet_issue: chua_co          # chủ kho cấp (hoặc phiên ghi hộ theo chỉ thị) khi đóng băng
nguon_cap_viec: >-
  docs/PROTOCOL_DA_PHIEN.md:1185 (§14 pha 3 "Test economics: instrument duration, tách callable/group, dọn global
  state, parallel full, shadow selector") và :839-840 (thứ tự bắt buộc trước selector). Chỉ thị chủ kho trong phiên
  Claude Code 25-09-2026: "Tôi duyệt phương án trên" (bước 2–3 của phương án đã thống nhất với Codex gpt-6-astra)
  và "nếu gộp vào càng ít packet thì càng tốt, đỡ tốn review, tốn CI".
tham_dinh_nhap: >-
  Codex gpt-6-astra (codex CLI, chỉ-đọc) thẩm định bản nháp tại c4e95ee6cf3b87655fc96d2d931f912febfa7cd8:
  lượt 1 "dong_y_neu_sua" (8 P2 + 1 P3); tại 783d522f7c21995e8b56e909976a1a354a0e3aee lượt 2 "dong_y_neu_sua"
  (4 P2 + 1 P3); tại e7ac2394f6e36262158aa73affd165586e542685 lượt 3 "dong_y_neu_sua" (2 P3); tại b7957aae1804a0a86af67b80ca39a225b35b896a lượt 4
  "dong_y_neu_sua" (1 P3). Không còn bất đồng về phương án tổng thể. Bản này sửa cả bốn lượt (mục 11).
ghi_chu_hinh_dang: >-
  Chưa cổng nào đọc tệp này. Nó là DỮ LIỆU cho lease và cho reviewer, không phải giao diện.
---

# `CI-SONG-SONG-REGISTRY-G5-MOT-LAN` — registry chạy song song có đối chiếu, selftest G5 chạy một lần (bản **r1**)

> **BẢN NHÁP — CHƯA ĐÓNG BĂNG.** Phiên executor Claude Code soạn theo skill `soan-spec`. Chủ kho đã trả lời sáu câu
> biên giới (mục 2). Tệp này **không** cấp quyền gì cho tới khi có Issue packet, băm đóng băng và lease còn hiệu
> lực (`docs/PROTOCOL_DA_PHIEN.md` §3.2, §4).

- `packet_id`: **`CI-SONG-SONG-REGISTRY-G5-MOT-LAN`** · `packet_issue`: **chưa có** · `revision`: **1** · `generation`: **1** (dự kiến)
- `review_class`: **`sensitive`** — chạm `.github/workflows/ci.yml` (workflow là phạm vi nhạy cảm, §8).
- `risk`: `sensitive` · `environment`: `cloud` · `depends_on`: `[]`
- executor: `anthropic_claude` · `claude_code` · `machine/local` · `claude-opus-5-5` · effort medium
- **assurance** — hai nghĩa vụ riêng, cả hai phải có trước land:
  1. review Codex qua GitHub connector: bề mặt `codex_service` · transport `machine`; model yêu cầu `gpt-6-astra`
     nhưng model phục vụ **không đo được** (`docs/PROTOCOL_DA_PHIEN.md:562-564`) ⇒ biên nhận khai **`advisory_review`**,
     không tự nâng thành `cross_approved`;
  2. **`assurance_target: human_audited`** — chủ kho audit exact head cuối. Đây là cổng land.
- base dự kiến: `origin/master` **`4c53c76d1955595a5659ab577d9dc1b64f9600ad`** (đo 2026-09-25T04:49:44Z)

## 1. Phép đo nền

Nguồn: workflow `gate`, run **36090209528** attempt **1**, event `pull_request`, head `987849cdc8da5d4184aad592051d7c8e0d859f71`
(PR #632), tạo lúc 2026-09-25T03:24:10Z. Số liệu job/bước lấy từ API `actions/runs/36090209528/jobs`, đọc lại
2026-09-25T04:49:44Z. Đơn vị: phút runner Linux (mỗi job một runner).

| phép đo | giá trị |
|---|---|
| job `gate` | 15,4 phút |
| job `gate-packet-loop` | 9,7 phút |
| job `gate-registry` | 38,6 phút |
| **tổng mỗi lần push PR** (ba job trên) | **63,7 phút runner** |
| thời gian chờ (job dài nhất) | 38,6 phút |
| bước "G5 kiem ban ke cong cu + T1..T8", mỗi job | 5,0 phút (3 job ⇒ 15,0 phút runner) |
| bốn bước cài công cụ + Ruff, mỗi job | ≈ 0,2 phút |
| bước "test registry" (`ci_dang_ky_test.py --chay`, 8 bộ của sổ `MOI` tuần tự, `ci_dang_ky_test.py:688-725`) | 33,1 phút |

Đo tại chỗ (container phiên soạn, không phải runner CI):
- `python ops/cong_cu.py kiem-tra --json` (probe): **0,179 giây**, đo 2026-09-25T04:57:31Z trên
  `783d522f7c21995e8b56e909976a1a354a0e3aee` (lần đo trước 0,22 giây). rc=2 tại chỗ vì container thiếu công cụ; phép
  đo này **chỉ** dùng cho thời lượng. ⇒ phần tốn của G5 là `python ops/cong_cu_test.py` (selftest T1..T8).
- 8 bộ của `MOI`, chạy đồng thời trên 4 lõi (có tranh chấp) tại head `155bbaa47e6936a81e16537e44e8a9b0c8e8fa60`,
  bắt đầu 2026-09-25T03:46:10Z; mốc xong lấy từ thời gian sửa đổi tệp kết quả: `ops/nhanh_don_duoc_test.py` 960 giây
  (xong 04:02:10Z) · `.claude/hooks/pretooluse_guard_test.py` 298 giây (03:51:08Z) ·
  `.claude/hooks/subagent_ghi_detect_test.py` 205 giây (03:49:35Z) · `.claude/dev/mcp_gh_test.py` 29 giây (03:46:39Z) ·
  4 bộ còn lại ≤ 2 giây (03:46:10Z–03:46:12Z).

**Nghĩa vụ L5:** đo lại cả bảng trước mỗi bước công bố (**đóng băng / đăng băm**, lease, PR, land) và ghi mốc đầy đủ. Mốc nào không khôi phục được thì ghi `KHONG_DO_DUOC`, không điền phỏng đoán.

Hệ quả:
- **Cache công cụ gần như vô ích** (≈ 0,2 phút mỗi job) ⇒ bỏ khỏi packet (mục 3).
- **Selftest G5 chạy lặp ba lần** ⇒ chỉ chạy ở `gate` tiết kiệm **10,0 phút runner** mỗi lần push.
- **Registry là job dài nhất**; sàn của nó là bộ dài nhất (`nhanh_don_duoc_test`, ≈ 16 phút tại chỗ).

Ước tính sau packet (**không phải tiêu chí**; A8/A9 thay bằng số đo), với R = thời lượng bước registry song song, giả
định R ∈ [17; 20] phút:
- `gate` giữ nguyên 15,4 phút;
- `gate-packet-loop` = 9,7 − 5,0 = 4,7 phút;
- `gate-registry` ≈ 0,4 phút (thiết lập + probe) + R = 17,4 đến 20,4 phút;
- **tổng ≈ 37,5 đến 40,5 phút runner mỗi push**, tức giảm ≈ 23 đến 26 phút runner so với 63,7;
- **thời gian chờ ≈ 17,4 đến 20,4 phút**, so với 38,6.

## 2. Sáu câu biên giới — chủ kho trả lời "đồng ý các khuyến nghị" (2026-09-25, phiên Claude Code)

| # | câu | quyết định |
|---|---|---|
| Q1 | phạm vi | pha 3 cho registry: (a) đo thời gian từng bộ, (b) cô lập thư mục tạm từng bộ, (c) song song N worker có đối chiếu. **Sửa theo câu tiếp của chủ kho** ("càng ít packet càng tốt"): gộp thêm việc giảm thiết lập lặp. Số đo mục 1 cho thấy cache vô ích, nên việc ấy là **selftest G5 chạy một lần**. |
| Q2 | luật "push một lần" | **không** thuộc packet này; phiên áp dụng như kỷ luật; đưa vào revision kế của #523 hoặc `CONG-CHAN-CHI-CI-SOM` do chủ kho chỉ định |
| Q3 | selector, cắt đột biến | ngoài phạm vi; thuộc #245 (`CI-BANG-PHU-THUOC` → `CI-FASTPATH-THEO-DIFF`) và #466 |
| Q4 | số worker | **sửa theo thẩm định Codex:** benchmark N ∈ {1, 2, 4} **tại chỗ** trên 8 bộ thật, chọn N, rồi **một** push xác nhận trên CI (mục 7). Không dùng nhiều push để benchmark. |
| Q5 | executor/reviewer | như phần đầu tệp; push **một lần** sau khi review tại chỗ sạch |
| Q6 | Windows | mã trung lập OS; lane Windows **giữ N=1** (mục 5, M3); chỉ đo và nghiệm thu trên Ubuntu; không tuyên bố đã kiểm Windows |

## 3. Ngoài phạm vi — cố ý không làm

| thứ | lý do |
|---|---|
| cache công cụ | ≈ 0,2 phút mỗi job (mục 1); không đáng một lần sửa hợp đồng T6 |
| gộp ba job thành một | Codex `gpt-6-astra` ước tính thời gian chờ tăng lên ≈ 53 phút |
| chọn test theo đường dẫn / job `skipped` | `docs/PROTOCOL_DA_PHIEN.md:835-840` cấm activate trước shadow 2–4 tuần; thuộc #245 |
| cắt vòng tự đột biến `nhanh_don_duoc_test` | spec đóng băng #466 |
| luật "push một lần" | Q2 |
| lane Windows | #548, bộ chạy cục bộ #602 |
| `ops/cong_cu_test.py`, `ops/cong_cu.py`, `ops/cong_cu.yaml` | T6 (`ops/cong_cu_test.py:265-293`) chỉ soi job `gate`, và `gate` giữ nguyên G5. Chốt mới cho hai job kia nằm trong W1 (M6). PR #581 (wp570, còn mở) đang sửa `ops/cong_cu_test.py` ⇒ tránh giao write set |
| sửa nội dung bất kỳ bộ test nào trong `MOI` | cô lập làm ở tầng runner. Nếu kiểm kê (M2) cho thấy một bộ **phải** sửa mới chạy song song an toàn ⇒ S3, dừng |

## 4. Write set — 2 đường (dự kiến; kiểm kê M2 có thể buộc dừng ở S3)

| # | đường dẫn | vì sao |
|---|---|---|
| W1 | `.claude/dev/ci_dang_ky_test.py` | runner registry (M1–M3), chốt cấu trúc workflow (M6), phản chứng/đột biến trong `phan_chung()` |
| W2 | `.github/workflows/ci.yml` | G5 tách (M4), biến môi trường worker ở step registry (M5) |

Ngưỡng ADR-0044 cho packet `sensitive` chạm authority: **≤ 3 tệp và ≤ 300 dòng thêm**. Packet này tự chọn 2 tệp;
vượt 300 dòng thêm ⇒ dừng trước review (S5).

Ràng buộc đã đo, executor không được phá:
- lệnh CI của registry giữ **đúng** chuỗi `python .claude/dev/ci_dang_ky_test.py --chay` (`ci_dang_ky_test.py:411`,
  `:593`, `:600`; fixture tab ở `:937`, ca có tên `registry-ngan-bang-tab` ở `:944`) ⇒ số worker đi qua khoá **`env:`
  YAML của step** (`CI_DANG_KY_WORKERS`), **không** qua cờ dòng lệnh, **không** gọi `nproc` hay lệnh shell mới trong
  job (Codex tái hiện: `loi_ruff_ci` báo cú pháp ngoài miền; `_LENH_OPAQUE` ở `:347-351` không chứa `nproc`);
- Ruff đứng trước registry trong cùng job (`loi_ruff_ci`, ca `da-tach-*` ở `:922-928`).

## 5. Mục tiêu (mỗi dòng chiếu một đường của write set — L2)

| # | mục tiêu | đường |
|---|---|---|
| M1 | `--chay` in **một** khối JSON thời gian có dấu mốc cố định: mỗi bộ của `MOI` một mục `{duong_dan, rc, giay, bat_dau_utc, ket_thuc_utc}`, cùng `so_lop_logic` (`os.cpu_count()`), `so_lop_dung_duoc` (`len(os.sched_getaffinity(0))` nếu có, không thì `null`) và `N` đã dùng. Đồng hồ đi qua một seam để test dùng clock giả | W1 |
| M2 | **kiểm kê tài nguyên dùng chung trước khi song song**, ghi vào PR: mỗi bộ của `MOI` ghi/xoá gì ngoài thư mục tạm (đã biết: `ops/nhanh_don_duoc_test.py:2436` tạo thư mục tạm với `dir=Path.cwd()` trong khi runner đặt `cwd=ROOT` ở `ci_dang_ky_test.py:682`; `.claude/dev/mcp_gh_test.py:28-36,52` xoá `.pyc` cạnh nguồn). Mỗi bộ chạy trong **subprocess riêng** với **bản sao** `env` có `TMPDIR`/`TEMP`/`TMP` trỏ vào thư mục con riêng. **Không** sửa `os.environ` hay cwd toàn cục từ thread. Thư mục con được dọn sau khi bộ xong; dọn thất bại ⇒ ĐỎ | W1 |
| M3 | song song tối đa N bộ. **Miền N:** biến vắng hoặc rỗng ⇒ N=1 (hành vi hiện nay); số nguyên 1–8 ⇒ N đó; mọi giá trị khác (0, âm, > 8, không phải số) ⇒ **ĐỎ rc≠0** trước khi chạy bộ nào. Trên Windows (`os.name == "nt"`) N luôn = 1. Số bộ **đang chạy** tại mọi thời điểm ≤ N; mỗi bộ chạy **đúng một lần**. Mỗi bộ có **giới hạn chờ 1 800 giây** (hằng số trong W1). Hết giờ ⇒ kết thúc **toàn cây tiến trình của riêng bộ ấy** (POSIX: bộ chạy trong phiên/nhóm tiến trình riêng, gửi tín hiệu cho cả nhóm; không đụng tiến trình ngoài cây), chờ tối đa **10 giây** cho cây dừng, rồi mới dọn thư mục tạm. Không xác nhận được cây đã dừng ⇒ ĐỎ. Bộ thật có tiến trình lồng: `ops/nhanh_don_duoc_test.py:743` gọi con qua `subprocess.run` không timeout ở `:369`. Lỗi hạ tầng (khởi chạy thất bại, hết giờ, dọn thất bại, ngoại lệ worker) ⇒ ĐỎ và **không** đi qua nhánh chấp nhận `CACH_LY` (`:706-721`). Log nghiệp vụ (đầu ra từng bộ + dòng `CI_DANG_KY …`) in theo **thứ tự sổ `MOI`**, không theo thứ tự xong | W1 |
| M4 | job `gate-registry` và `gate-packet-loop` thay bước G5 bằng **chỉ probe** `python ops/cong_cu.py kiem-tra --json`; `python ops/cong_cu_test.py` chỉ còn ở job `gate` | W2 |
| M5 | step registry trong `ci.yml` đặt `CI_DANG_KY_WORKERS` qua `env:` bằng N chọn ở A8 | W2 |
| M6 | chốt cấu trúc workflow trong `phan_chung()`: đúng **một** job chạy `python ops/cong_cu_test.py` (job `gate`); cả **ba** job có bước probe `ops/cong_cu.py kiem-tra`, **vô điều kiện**, đứng **trước** bước test nặng đầu tiên của job | W1 |
| M7 | hàm thuần `chon_so_worker(trung_vi_theo_N)` hiện thực luật chọn N của A8; kết quả benchmark tại chỗ và N chọn ghi vào PR | W1 |

## 6. Nghiệm thu — mỗi tiêu chí nêu phép đo làm nó ĐỎ (L3)

| # | tiêu chí | phép đo làm ĐỎ |
|---|---|---|
| A1 | M1: JSON có đúng một mục cho mỗi khoá của `MOI` (đếm theo `MOI` lúc chạy, không ghi cứng số), `rc` là số nguyên, `giay` ≥ 0, hai mốc ISO-8601 UTC với `ket_thuc ≥ bat_dau`; với clock giả, giá trị khớp chính xác | đột biến riêng cho từng trường: bỏ một mục · `rc` sai kiểu · `giay` âm hoặc sai đơn vị · mốc đảo ⇒ mỗi đột biến làm một ca ĐỎ |
| A2 | M2 cô lập: hai bộ giả cùng ghi một tên tệp vào thư mục tạm, chạy đồng thời, không đụng nhau; thư mục con bị dọn; `os.environ` của tiến trình cha không đổi | đột biến "dùng chung một TMPDIR" · "không dọn" · "sửa `os.environ` toàn cục" ⇒ mỗi đột biến làm một ca ĐỎ |
| A3 | M3 đối chiếu trên runner giả (bộ ngủ độ dài khác nhau, một bộ rc≠0, một bộ ném ngoại lệ, một bộ hết giờ): N=1 và N=4 cho **cùng log nghiệp vụ** theo thứ tự `MOI` và **cùng phán quyết** (số đỏ, từng dòng `CI_DANG_KY`). JSON thời gian so riêng (A1) | đột biến "in theo thứ tự xong" · "bỏ qua rc một worker" · "nuốt ngoại lệ worker" · "bỏ giới hạn chờ" ⇒ mỗi đột biến làm một ca ĐỎ |
| A3b | M3 trần N, đồng bộ tất định (barrier/sự kiện, không dựa vào tốc độ máy): bộ đếm đang chạy cho `max_active ≤ N`; với N>1 có ít nhất một lần chồng lấp; mỗi bộ chạy đúng một lần | đột biến "bỏ semaphore/trần worker" · "chạy một bộ hai lần" ⇒ ĐỎ |
| A3c | M3 hết giờ giết cả cây: fixture là bộ giả sinh tiến trình cháu giữ pipe rồi treo; hết giờ ⇒ cả cha lẫn cháu dừng trong 10 giây, bộ ĐỎ, thư mục tạm được dọn; tiến trình ngoài cây không bị đụng | đột biến "chỉ giết tiến trình cha" ⇒ ca ĐỎ (cháu còn sống hoặc pipe treo) |
| A4 | M3 miền N: vắng/rỗng ⇒ 1; "0", "-1", "9", "abc" ⇒ rc≠0 trước khi chạy bộ nào; Windows ⇒ 1; lỗi hạ tầng không được hợp thức hoá qua `CACH_LY` | mỗi đầu vào sai là một ca; đột biến "mặc định N>1" · "chấp nhận 0" · "cho lỗi hạ tầng qua cách ly" ⇒ ĐỎ |
| A5 | M3 mặc định: không đặt biến ⇒ log nghiệp vụ giống master `4c53c76d` trên cùng bộ giả | so log nghiệp vụ lệch ⇒ ĐỎ |
| A6 | **đối chiếu trên 8 bộ thật** (tại chỗ, Ubuntu): N=1 và N chọn cho cùng phán quyết và cùng tập dòng `CI_DANG_KY`, lặp **3 lần** mỗi N | một lần lệch ⇒ DỪNG (S2) |
| A7 | M4 + M6: selftest G5 chỉ ở `gate`; probe vô điều kiện ở cả ba job, trước bước nặng đầu tiên; T6 và kiểm "lời gọi CI" của registry vẫn đạt | đột biến workflow trong bộ nhớ: bỏ probe ở một job · thêm `if:` cho probe · dời probe sau bước nặng · nhân đôi selftest ⇒ mỗi đột biến làm chốt M6 ĐỎ. Codex đã đo: nếu thiếu M6 thì bỏ cả hai probe vẫn qua T6, registry 21/21 và Ruff 3/3 |
| A8 | M5 + Q4: benchmark tại chỗ N ∈ {1, 2, 4} trên 8 bộ thật, **dùng lại 3 lượt của A6**, ghi thời lượng và `so_lop_*` từng lượt. Luật chọn là một hàm thuần trong W1 (`chon_so_worker`): lấy **trung vị** 3 lượt cho mỗi N; chỉ N ∈ {2, 4} có trung vị **nhỏ hơn** trung vị N=1 mới là ứng viên; trong tập ứng viên đặt `t_min` = trung vị nhỏ nhất, rồi chọn **N nhỏ nhất** có trung vị **≤ 1,10 × `t_min`**; **không có ứng viên ⇒ DỪNG (S2) trước push**. Sau đó **một** push xác nhận: bước registry trên CI **< 33,1 phút** (nền mục 1) và JSON M1 in `so_lop_*` của runner | fixture trung vị `{1: 100, 2: 101, 4: 102}` giây ⇒ "không có ứng viên" (đột biến cho phép chọn N=1 ⇒ ĐỎ); fixture đúng biên `{1: 200, 2: 110, 4: 100}` ⇒ N=2 (110 ≤ 1,10 × 100); fixture vượt biên `{1: 200, 2: 110,5, 4: 100}` ⇒ N=4; đột biến dùng `(t_max − t_min) / t_max ≤ 0,10` thay cho `(t_max − t_min) / t_min ≤ 0,10` (với `t_max` là trung vị lớn nhất trong tập ứng viên) phải làm fixture vượt biên ĐỎ (bản đúng chọn N=4, đột biến chọn N=2); N chọn không nhanh hơn nền trên CI ⇒ KHÔNG ĐẠT, DỪNG (S2) |
| A9 | tổng phút runner của lượt xác nhận **< 63,7 phút** (nền mục 1) | không nhỏ hơn ⇒ KHÔNG ĐẠT |
| A10 | cổng hiện hành trên head cuối, mỗi cổng có lệnh + **dấu hiệu dương**: `lease_publish_test` in `N/N đạt` · `bien_nhan_v2` in `TỔNG: ĐẠT` và `0 vi phạm` · `ci_phamvi --kiem-bam` rc=0 và in kết luận dương · `actionlint .github/workflows/ci.yml` rc=0 và **không** in chẩn đoán nào (Codex đo trên `783d522f`: rc=0, đầu ra rỗng); kiểm toàn bộ workflow là phép đo riêng, so với nền cùng phạm vi (nền: 1 thông tin SC1003 ở `ops-don-ref.yml:117`) · `release-verify --strict --json` có `ok=true` và `expected_file_count == checked_file_count` · ba job CI của lượt xác nhận có dòng `TỔNG: ĐẠT` trong log | cổng thiếu, đỏ, `skipped` hoặc không có dấu hiệu dương ⇒ KHÔNG ĐẠT. Dấu hiệu dương chỉ được ghi vào bằng chứng sau khi xác nhận lệnh thực sự chạy và đạt |
| A11 | kích thước: báo `git diff --numstat` so base; ≤ 300 dòng thêm | vượt ⇒ dừng trước review (S5) |

## 7. Ngân sách CI (§12, `docs/PROTOCOL_DA_PHIEN.md:1025-1039`)

| loại | nội dung | `used / reserved / limit` |
|---|---|---|
| gate tự động | lượt `pull_request` trên head cuối, sau review tại chỗ sạch | 0 / 1 / 1 lượt ≈ 40 phút runner (ước tính mục 1) |
| phép đo được cấp | **không có**: benchmark N làm tại chỗ | 0 / 0 / 0 |
| thăm dò chưa được cấp | cấm | 0 / 0 / 0 |

Head đổi làm bằng chứng của lượt trước **stale**. Allowance đã dùng hết (1/1) ⇒ **DỪNG trước push hoặc chạy lại**;
chỉ tiếp tục sau một quyết định bền của chủ kho nâng trần (`docs/PROTOCOL_DA_PHIEN.md:1030-1039`: phân loại "tự động"
không cấp thêm allowance). Không có cổng máy cưỡng chế luật này trong packet; reviewer đếm lượt `pull_request` của
PR qua API và đối chiếu bảng. Chủ kho duyệt trần khi đóng băng.

## 8. Hình dạng kế thừa (L4)

`khong_ap_dung` — không phải packet khắc phục. Bài học liên quan, chép để executor biết:
- **lỗi dọn thư mục tạm r506** (`Directory not empty …/remote.git`) đã làm `gate-registry` đỏ vặt ≥ 3 lần (#613, #616,
  #633). #593/#629 đã vá phần gốc. Chạy song song làm lớp lỗi này dễ lộ hơn ⇒ M2 đứng trước M3.
- `ops/specs/MUTANT-KHONG-CHAY-TREN-WINDOWS.md:85` từng cân nhắc và bỏ "song song hoá `chay_moi()`". Executor đọc lại lý
  do và trả lời trong PR trước khi làm M3.

## 9. Va chạm (đo 2026-09-25T05:02:33Z trên 43 PR đang mở; đo lại trước khi ghi)

- PR đang mở chạm write set: **#447** (`ci_dang_ky_test.py`, cập nhật lần cuối 2026-09-14T18:51:22Z).
- PR #581 (cập nhật lần cuối 2026-09-25T04:38:14Z) chạm `ops/cong_cu_test.py` — **ngoài** write set (mục 3).
- Không lease sống nào giữ W1/W2 theo quét các PR đang mở. Phiên thi công chạy `lease_publish.py ai-dang-giu` trước khi ghi.

## 10. Điều kiện dừng

- **S1** chạm đường ngoài W1/W2 ⇒ DỪNG.
- **S2** đối chiếu N=1/N>1 lệch (A3, A6), hoặc N chọn không nhanh hơn nền trên CI (A8) ⇒ DỪNG. Không hạ N hay nới phép đối chiếu để ép xanh.
- **S3** kiểm kê M2 cho thấy một bộ chỉ chạy song song an toàn khi sửa chính bộ ấy ⇒ DỪNG, báo chủ kho (việc "dọn global state" của pha 3 cho bộ ấy là packet riêng hoặc revision mở write set).
- **S4** push lên PR **một lần** sau khi review tại chỗ sạch. Hết allowance mục 7 ⇒ dừng trước mọi push hoặc chạy lại kế tiếp, chờ quyết định bền của chủ kho.
- **S5** > 300 dòng thêm ⇒ dừng trước review.
- **S6** hết hạn lease ⇒ ngừng ghi, handoff §7.

## 11. Chưa đo được, và đối chiếu thẩm định nháp

Chưa đo được từ phiên soạn:
- số lõi của runner `ubuntu-latest` trên kho riêng tư (M1 in ra ở lượt xác nhận);
- kiểm kê đầy đủ tài nguyên dùng chung của 8 bộ (M2 là việc đầu tiên của executor; hai mục đã biết ghi ở M2);
- hành vi trên Windows (Q6: N=1);
- thời lượng registry song song (mục 1 chỉ ước tính).

Chín điểm của Codex trên `c4e95ee6` và chỗ đã sửa:

| # | mức | điểm | sửa ở |
|---|---|---|---|
| 1 | P2 | hai push benchmark là "phép đo được cấp", chưa có ngân sách §12 | Q4, A8, mục 7 |
| 2 | P2 | TMPDIR + runner giả chưa chứng minh cô lập bộ thật | M2 (kiểm kê, subprocess + bản sao env), A6 (đối chiếu 8 bộ thật), S3 |
| 3 | P2 | thiếu hợp đồng miền N, giới hạn chờ, cleanup, lỗi hạ tầng vs `CACH_LY` | M3, A4 |
| 4 | P2 | log "giống hệt" mâu thuẫn với JSON thời gian; A1 chỉ kiểm khoá | M1 (clock seam), A1, A3, A5 |
| 5 | P2 | chưa có chốt "probe ở cả ba job, selftest một job" | M6, A7 |
| 6 | P2 | `nproc` làm cổng Ruff đỏ; lane Windows | mục 4 (ràng buộc), M1 (`os.cpu_count`), M3/Q6 (Windows N=1) |
| 7 | P2 | "rc≠0 mới so nền" không phải bằng chứng dương | A10 |
| 8 | P2 | `cross_approved` lẫn với `human_audited` | phần đầu tệp (hai nghĩa vụ) |
| 9 | P3 | mốc đo, nguồn run, ngưỡng ADR, phép cộng, dòng dẫn | mục 1, mục 4 |

Lượt 2 trên `783d522f` (4 P2 + 1 P3) và chỗ đã sửa:

| # | mức | điểm | sửa ở |
|---|---|---|---|
| 1 | P2 | hết giờ chưa giết cả cây tiến trình, chưa có hạn chờ dọn | M3 (1 800 giây, nhóm tiến trình, chờ 10 giây, không xác nhận ⇒ ĐỎ), A3c |
| 2 | P2 | chưa đo trần N | M3, A3b |
| 3 | P2 | luật chọn N có thể chọn lại N=1 | A8 (`chon_so_worker`, trung vị, chỉ N ∈ {2,4} nhanh hơn, không có ứng viên ⇒ S2) |
| 4 | P2 | lượt gate kế tiếp vượt trần chưa có chốt | mục 7, S4 |
| 5 | P3 | actionlint lệch phạm vi và dấu hiệu dương | A10 |
| — | — | mốc đo còn `x` | mục 1 (mốc từ thời gian sửa đổi tệp, probe đo lại) |

Lượt 4 trên `b7957aae` (1 P3): câu mô tả đột biến ở A8 ghi sai đại lượng ⇒ thay bằng câu Codex đề xuất (đã kiểm trong bộ nhớ).

Lượt 3 trên `e7ac2394` (2 P3; không còn P1/P2): mẫu số của luật chọn N ⇒ A8 (`t_min`, ≤ 1,10 × `t_min`, fixture đúng biên và vượt biên); mốc chỉ biết tới phút ở mục 9 và bước "đóng băng" trong L5 ⇒ mục 9 đo lại 2026-09-25T05:02:33Z, mục 1 bổ sung.
