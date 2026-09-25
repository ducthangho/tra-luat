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
- reviewer: `openai_codex` (Codex GitHub connector, yêu cầu `gpt-6-astra`) ⇒ mục tiêu `cross_approved`; `assurance_target: human_audited`
- base dự kiến: `origin/master` **`4c53c76d1955595a5659ab577d9dc1b64f9600ad`** (đo `04:3xZ 25-09`)

## 1. Phép đo nền — đo `25-09-2026`, trên các lượt CI của head `987849cdc8da5d4184aad592051d7c8e0d859f71` (PR #632)

| phép đo | giá trị | nguồn |
|---|---|---|
| job `gate` | 15,4 phút | actions/runs, head 987849cd |
| job `gate-packet-loop` | 9,7 phút | cùng lượt |
| job `gate-registry` | 38,6 phút | cùng lượt |
| **tổng phút runner mỗi lần push PR** | **≈ 63,7 phút** | tổng ba job trên |
| bước "G5 kiem ban ke cong cu + T1..T8" | **5,0 phút ở MỖI job** (3 job ⇒ ≈ 15 phút) | cùng lượt |
| trong đó `python ops/cong_cu.py kiem-tra --json` (probe) | **0,22 giây** tại chỗ | đo tại chỗ trên `4c53c76d` |
| ⇒ phần tốn của G5 là `python ops/cong_cu_test.py` (selftest T1..T8) | ≈ 5 phút mỗi lần | suy từ hai dòng trên |
| bốn bước cài công cụ (PyYAML, actionlint, shellcheck, rg) + Ruff | **≈ 0,2 phút mỗi job** | cùng lượt |
| bước "test registry" (`ci_dang_ky_test.py --chay`) | **33,1 phút**, tuần tự 8 bộ (`ci_dang_ky_test.py:688-725`) | cùng lượt |
| từng bộ đo tại chỗ (4 lõi, chạy đồng thời nên có tranh chấp) | `nhanh_don_duoc_test` 960 s · `pretooluse_guard_test` 298 s · `subagent_ghi_detect_test` 205 s · `mcp_gh_test` 29 s · 4 bộ còn lại ≤ 2 s | head `155bbaa4`, `04:0xZ` |
| số lõi của runner `ubuntu-latest` trên kho riêng tư | **KHÔNG ĐO ĐƯỢC** từ phiên soạn | xem mục 10 |

Hệ quả đo được:
- **Cache công cụ gần như vô ích** (≈ 0,2 phút mỗi job) ⇒ bỏ khỏi packet (mục 3).
- **Selftest G5 chạy lặp ba lần** ⇒ chạy một lần ở `gate` tiết kiệm ≈ **10 phút runner mỗi lần push**.
- **Registry là job dài nhất**; sàn của nó là bộ dài nhất (`nhanh_don_duoc_test`, ≈ 16 phút tại chỗ).

## 2. Sáu câu biên giới — chủ kho trả lời "đồng ý các khuyến nghị" (`25-09`, phiên Claude Code)

| # | câu | quyết định |
|---|---|---|
| Q1 | phạm vi | pha 3 cho registry: (a) đo thời gian từng bộ, (b) cô lập thư mục tạm từng bộ, (c) song song N worker có đối chiếu. **Sửa theo câu tiếp của chủ kho** ("càng ít packet càng tốt"): gộp thêm việc giảm thiết lập lặp. Số đo mục 1 cho thấy cache vô ích, nên việc giảm thiết lập là **selftest G5 chạy một lần**. |
| Q2 | luật "push một lần" | **không** thuộc packet này; phiên áp dụng như kỷ luật; đưa vào revision kế của #523 hoặc `CONG-CHAN-CHI-CI-SOM` do chủ kho chỉ định |
| Q3 | selector, cắt đột biến | ngoài phạm vi; thuộc #245 (`CI-BANG-PHU-THUOC` → `CI-FASTPATH-THEO-DIFF`) và #466 |
| Q4 | số worker | nghiệm thu bằng số đo CI thật với 2 và 4; chọn N theo số đo, không ghi cứng |
| Q5 | executor/reviewer | như phần đầu tệp; push **một lần** sau khi review tại chỗ sạch |
| Q6 | Windows | mã trung lập OS; chỉ đo và nghiệm thu trên Ubuntu |

## 3. Ngoài phạm vi — cố ý không làm

| thứ | lý do |
|---|---|
| cache công cụ | đo ≈ 0,2 phút mỗi job (mục 1); không đáng một lần sửa hợp đồng T6 |
| gộp ba job thành một | Codex `gpt-6-astra` ước tính gộp làm thời gian chờ tăng lên ≈ 53 phút |
| chọn test theo đường dẫn / job `skipped` | protocol §10.1 dòng 835-840 cấm activate trước shadow 2–4 tuần; thuộc #245 |
| cắt vòng tự đột biến `nhanh_don_duoc_test` | spec đóng băng #466 |
| luật "push một lần" | Q2 |
| lane Windows | #548, bộ chạy cục bộ #602 |
| `ops/cong_cu_test.py`, `ops/cong_cu.py`, `ops/cong_cu.yaml` | không cần sửa: T6 (`ops/cong_cu_test.py:265-293`) chỉ soi job `gate`, và `gate` giữ nguyên G5. PR #581 (wp570, còn mở) đang sửa `ops/cong_cu_test.py` ⇒ tránh giao write set |
| mọi bộ test trong registry | không sửa nội dung bộ nào; cô lập làm ở tầng runner |

## 4. Write set — 2 đường

| # | đường dẫn | vì sao |
|---|---|---|
| W1 | `.claude/dev/ci_dang_ky_test.py` | runner registry: đo thời gian, cô lập thư mục tạm, song song có đối chiếu, cùng phản chứng/đột biến trong `phan_chung()` của chính tệp |
| W2 | `.github/workflows/ci.yml` | `gate-registry` và `gate-packet-loop` chỉ chạy probe G5; bước registry truyền số worker qua biến môi trường |

Ngưỡng ADR-0044: 2 tệp. Mục tiêu ≤ 300 dòng thêm; vượt ⇒ dừng trước review (S5).

Ràng buộc đã đo, executor không được phá: lệnh CI của registry phải giữ **đúng** chuỗi
`python .claude/dev/ci_dang_ky_test.py --chay` (`ci_dang_ky_test.py:411`, `:593`, `:600`; ca `registry-ngan-bang-tab`
ở `:937`). Vì vậy số worker đi qua biến môi trường (đề xuất `CI_DANG_KY_WORKERS`), **không** qua cờ dòng lệnh.
Ruff vẫn phải đứng trước registry trong cùng job (`loi_ruff_ci`, ca `da-tach-*` ở `:922-928`).

## 5. Mục tiêu (mỗi dòng chiếu một đường của write set — L2)

| # | mục tiêu | đường |
|---|---|---|
| M1 | `--chay` ghi thời gian từng bộ (đường dẫn, rc, giây, mốc bắt đầu/kết thúc UTC) ra một khối JSON có dấu mốc cố định trong log | W1 |
| M2 | mỗi bộ chạy với thư mục tạm riêng (`TMPDIR`/`TEMP`/`TMP` trỏ vào thư mục con riêng) và được dọn sau khi bộ kết thúc; dọn thất bại ⇒ ghi rõ, không nuốt | W1 |
| M3 | chạy song song tối đa N bộ (`CI_DANG_KY_WORKERS`, mặc định **1** = hành vi tuần tự hiện nay). Log in theo **thứ tự sổ `MOI`**, không theo thứ tự xong. Phán quyết (đếm đỏ, dòng `CI_DANG_KY …`, cách ly `CACH_LY`) **bằng hệt** bản tuần tự. Worker ném ngoại lệ ⇒ ĐỎ (fail-closed) | W1 |
| M4 | job `gate-registry` và `gate-packet-loop` thay bước G5 bằng **chỉ probe** `python ops/cong_cu.py kiem-tra --json`; `python ops/cong_cu_test.py` chỉ còn ở job `gate` | W2 |
| M5 | bước registry trong `ci.yml` đặt `CI_DANG_KY_WORKERS` bằng giá trị chọn theo số đo (Q4) và in `nproc` trước khi chạy | W2 |

## 6. Nghiệm thu — mỗi tiêu chí nêu phép đo làm nó ĐỎ (L3)

| # | tiêu chí | phép đo làm ĐỎ |
|---|---|---|
| A1 | M1: khối JSON có đúng 8 mục, khớp khoá sổ `MOI` | đột biến "bỏ một bộ khỏi JSON" ⇒ ca phản chứng trong `phan_chung()` ĐỎ |
| A2 | M2: hai bộ giả ghi cùng tên tệp vào thư mục tạm, chạy đồng thời, không đụng nhau; thư mục bị dọn | đột biến "dùng chung một TMPDIR" ⇒ ca ĐỎ; đột biến "không dọn" ⇒ ca ĐỎ |
| A3 | M3 đối chiếu: với runner giả (các bộ ngủ độ dài khác nhau, một bộ rc≠0, một bộ ném ngoại lệ), N=1 và N=4 cho **cùng** chuỗi log và **cùng** số đỏ | đột biến "in theo thứ tự xong" ⇒ ĐỎ; "bỏ qua rc của một worker" ⇒ ĐỎ; "nuốt ngoại lệ worker" ⇒ ĐỎ |
| A4 | M3 mặc định: không đặt biến ⇒ N=1, log giống hệt master `4c53c76d` trên cùng bộ giả | đột biến "mặc định N>1" ⇒ ca ĐỎ |
| A5 | các ca cũ của `phan_chung()` vẫn đạt, gồm `loi_ruff_ci` và các ca hình dạng lệnh `--chay` | chạy `python .claude/dev/ci_dang_ky_test.py`, rc≠0 ⇒ ĐỎ |
| A6 | M4: selftest G5 chỉ còn ở `gate`; probe còn ở cả ba job; T6 của `ops/cong_cu_test.py` và kiểm "lời gọi CI" của registry vẫn đạt | `python ops/cong_cu_test.py` rc≠0 ⇒ ĐỎ; bỏ luôn selftest ở `gate` ⇒ registry báo `ops/cong_cu_test.py` không được CI gọi ⇒ ĐỎ |
| A7 | M5 + Q4: trên PR của packet, đo `gate-registry` với N=2 **và** N=4 (hai lượt `pull_request` tự động do hai push, **không** gọi tay); chọn N có thời gian bước registry nhỏ hơn; bước registry < **33,1 phút** (nền mục 1) | N nào cũng không nhỏ hơn nền ⇒ KHÔNG ĐẠT, dừng (S2) |
| A8 | tổng phút runner mỗi push, đo trên head cuối, nhỏ hơn nền **63,7 phút** | không nhỏ hơn ⇒ KHÔNG ĐẠT |
| A9 | cổng hiện hành trên head cuối: `lease_publish_test` N/N, `bien_nhan_v2` 0 vi phạm, `ci_phamvi --kiem-bam` rc=0, `actionlint` trên `ci.yml` không lỗi mới, `release-verify --strict` ok | bất kỳ rc≠0 mới so với nền ⇒ ĐỎ |
| A10 | kích thước: ≤ 2 tệp; báo `git diff --numstat` so base | > 300 dòng thêm ⇒ dừng trước review (S5) |

Ước tính (không phải tiêu chí): G5 một lần tiết kiệm ≈ 10 phút runner mỗi push. Registry song song phụ thuộc số lõi.
Với 2 lõi, sàn là bộ dài nhất, nên bước registry ≈ 17–20 phút. Tổng ≈ 25 trên 63,7 phút mỗi push, thời gian chờ
≈ 38 → ≈ 22 phút. A7 và A8 thay ước tính bằng số đo.

## 7. Hình dạng kế thừa (L4)

`khong_ap_dung` — không phải packet khắc phục. Bài học liên quan, chép để executor biết:
- **lỗi dọn thư mục tạm r506** (`Directory not empty …/remote.git`) đã làm `gate-registry` đỏ vặt ≥ 3 lần (#613, #616,
  #633). #593/#629 đã vá phần gốc. Chạy song song làm lớp lỗi này **dễ lộ hơn**; đó là lý do M2 đứng trước M3.
- `MUTANT-KHONG-CHAY-TREN-WINDOWS.md:85` từng cân nhắc và bỏ "song song hoá `chay_moi()`". Lý do phải được executor
  đọc lại và trả lời trong PR trước khi làm M3.

## 8. Va chạm (đo `04:3xZ 25-09`)

- PR đang mở chạm write set: **#447** (`ci_dang_ky_test.py`, cập nhật lần cuối 14-09). Executor đo lại trước khi ghi.
- PR #581 chạm `ops/cong_cu_test.py` — **ngoài** write set (mục 3).
- Không lease sống nào giữ W1/W2 (phiên thi công phải chạy `lease_publish.py ai-dang-giu` trước khi ghi).

## 9. Điều kiện dừng

- **S1** chạm đường ngoài W1/W2 ⇒ DỪNG.
- **S2** đối chiếu N=1/N>1 lệch, hoặc N>1 không nhanh hơn nền ⇒ DỪNG. Không hạ N hay nới phép đối chiếu để ép xanh.
- **S3** một bộ registry chỉ chạy được song song khi sửa chính bộ ấy ⇒ DỪNG, báo chủ kho (đó là việc pha 3 "dọn global state" cho bộ ấy, packet riêng).
- **S4** push lên PR **một lần** sau khi review tại chỗ sạch. Ngoại lệ duy nhất: hai push để đo A7 (N=2, N=4), khai trước trong PR.
- **S5** > 300 dòng thêm ⇒ dừng trước review.
- **S6** hết hạn lease ⇒ ngừng ghi, handoff §7.

## 10. Chưa đo được từ phiên soạn

- Số lõi thật của runner `ubuntu-latest` trên kho riêng tư. M5 in `nproc` để đo.
- Các bộ registry có dùng trạng thái toàn cục ngoài thư mục tạm không, như `git config --global`, `HOME`, cổng mạng hay tệp trong kho. Nếu có, A3 sẽ lộ ra khi chạy thật; nếu cần sửa bộ ⇒ S3.
- Hành vi trên Windows (Q6).
- Thời lượng bước registry song song: mục 6 chỉ là ước tính cho tới khi A7 đo.
