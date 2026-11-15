# Báo cáo đo đạc và tối ưu thời gian CI của `ci.yml` (15-11-2026)

Tệp này là **báo cáo**, không phải đặc tả packet. Nó nằm dưới `ops/specs/` để PR chứa nó đi làn hồ sơ của `ci.yml`
(`duong_nhanh`, khoảng 8 phút) thay vì làn đầy đủ (khoảng 90 phút). Hai đặc tả nháp đi kèm, chờ chủ kho duyệt băm:

- `ops/specs/CI-PACKET-LOOP-SONG-SONG-r1.md`: chạy `packet_loop_test.py` song song theo làn trong job.
- `ops/specs/CI-PROVENANCE-SONG-SONG-r1.md`: chạy vòng đột biến của `ops/ci_provenance_test.py` song song.

Người đo: phiên Claude Code trên máy chủ kho, theo nhiệm vụ do phiên điều phối giao ngày 15-11-2026. Mọi số dưới đây
kèm thời điểm đo. Master lúc đo là `072d45a0595f3d2ff9f0880143a237c9e0ea70c3`; lúc công bố là
`426d1b06e292a7db272a0f942bef0794479b58a6` (`git diff --stat` giữa hai mốc: đúng ba tệp, ADR-0067, protocol và skill
`soan-spec`, không tệp nào được đo ở đây). Giờ ghi theo UTC (`Z`); giờ Việt Nam là UTC+7.

## 1. Kết luận

1. Một lượt PR chạy đủ mất **trung vị 91,1 phút, p90 123,1 phút** (20 lượt PR thành công, 08→14-11). Gần như toàn bộ
   thời gian ấy là **một job**: `gate-packet-loop` trung vị 91,1 phút, p90 119,0 phút. Job dài thứ hai là `gate-ops`,
   trung vị 23,0 phút. Không job nào phải chờ runner (hàng đợi lớn nhất đo được 56 giây).
2. Trong `gate-packet-loop`, một bước duy nhất `python .claude/dev/packet_loop_test.py` chiếm 99 % thời lượng. Bước
   ấy chạy **tuần tự trên một lõi** trong khi runner `ubuntu-latest` của kho có **4 vCPU** (đo `nproc` = 4, 14-11).
   Chú thích "runner 2 lõi" trong `ci.yml` dựa trên số đo ngày 28-09 (đặc tả #668); nhiều khả năng runner lên 4 vCPU
   khi kho chuyển sang công khai, nhưng phiên này không đo được lúc nào đổi.
3. Thời lượng bước ấy tăng từ 42–87 phút (08-11) lên 80–126 phút (12→14-11), cùng lúc bộ test lớn lên: 1.360 → 1.495
   ca, 1.523 → 1.829 đột biến, `packet_loop.py` 3.761 → 6.247 dòng. Theo đà này job sẽ chạm trần `timeout-minutes: 150`.
4. Ba nguyên nhân đo được trên runner thật (§3):
   - một ca, `wp1303_target_human_chain`, tốn **24,5 phút** (42 % pha chạy ca nền) và thêm 6,3 phút trong pha đột biến;
   - mỗi lệnh CLI trong ca là một tiến trình Python mới, biên dịch lại `packet_loop.py` từ nguồn: pha nền gọi
     `python packet_loop.py` **6.479 lần**, trung bình 0,271 s/lần, tổng 29,3 phút;
   - ba ca đối chứng doctrine được chạy lại dưới **1.754** đột biến mỗi ca, tổng 18,3 phút (30 % pha đột biến).
5. Khuyến nghị theo thứ tự (§5): (P1) chạy `packet_loop_test.py` theo 4 làn song song trong job, ước còn khoảng 34–43 phút;
   (P2) song song hoá `ci_provenance_test.py`, kéo `gate-registry` từ 21 xuống khoảng 13–15 phút; (P3) chia
   `gate-packet-loop` thành 8 job, ước còn khoảng 19 phút; sau đó mới tới `gate-ops`. Hai đặc tả nháp cho P1 và P2 đi
   kèm báo cáo này.

## 2. Phép đo trên CI

### 2.1 Mẫu và lệnh

60 lượt `ci.yml` đã hoàn tất gần nhất, `run_started_at` từ `2026-11-08T10:08:02Z` tới `2026-11-14T09:17:35Z`, tải lúc
`2026-11-14T17:27Z`: 29 PR thành công, 18 push master thành công, 8 PR đỏ, 5 PR bị huỷ. Phân loại làn theo job
`gate-cong-cu`: nó `skipped` thì lượt ấy là `duong_nhanh`. Còn lại **32 lượt đầy đủ thành công** (20 PR, 12 push) và 15
lượt `duong_nhanh` thành công. Lệnh (REST qua `gh api`, script đầy đủ ở Phụ lục A):

```
gh api "repos/ducthangho/tra-luat/actions/workflows/ci.yml/runs?per_page=60&status=completed"
gh api "repos/ducthangho/tra-luat/actions/runs/<id>/attempts/<attempt>/jobs?per_page=100"
gh api "repos/ducthangho/tra-luat/actions/jobs/<job_id>/logs"
```

Thời lượng job = `completed_at − started_at`; hàng đợi = `started_at − created_at`; thời gian tường của lượt = job xong
muộn nhất − `run_started_at`. Mọi lượt trong mẫu chạy Ubuntu (nhãn `ubuntu-latest`), không lượt nào có job Windows.

### 2.2 Thời gian tường của lượt

| làn | n | trung vị | p90 |
|---|---|---|---|
| đầy đủ, PR | 20 | 91,1 phút | 123,1 phút |
| đầy đủ, push master | 12 | 92,1 phút | 116,3 phút |
| `duong_nhanh` | 15 | 7,4 phút | — |

### 2.3 Thời lượng từng job (32 lượt đầy đủ thành công)

| job | thời lượng trung vị | p90 | max | xong ở phút (trung vị · p90) | hàng đợi p90 |
|---|---|---|---|---|---|
| `gate-packet-loop` | **91,1** | **119,0** | 126,5 | 91,3 · 119,3 | 0 |
| `gate-ops` | 23,0 | 27,8 | 28,9 | 23,2 · 28,2 | 0 |
| `gate-registry` | 21,3 | 25,1 | 26,2 | 23,5 · 27,2 | 0 |
| `gate-cong-cu` (mỗi mảnh, 256 job) | 17,1 | 21,4 | 22,1 | 17,3 · 21,7 | 0 |
| `gate-cong-cu-gop` | 0,2 | 0,3 | 0,3 | 22,0 · 22,5 | 0 |
| `gate` | 12,2 | 14,4 | 14,7 | 12,5 · 14,7 | 0 |
| `gate-nhanh-manh` (mỗi mảnh, 256 job) | 1,1 | 1,5 | 1,7 | 1,4 · 1,9 | 0 |
| `gate-nhanh-gop` | 0,2 | 0,3 | 0,4 | 2,1 · 2,3 | 0 |
| `chuan-bi` | 0,2 | 0,2 | 0,2 | 0,2 · 0,3 | 0 |

Đơn vị: phút. Đường găng của mọi lượt đầy đủ là `gate-packet-loop`. Bỏ nó đi thì lượt xong ở khoảng phút 23–28, do
`gate-ops` và `gate-registry` (registry bắt đầu ở phút 2,2 vì `needs: gate-nhanh-gop`).

Đồng thời: trong 60 lượt có lúc 39 job chạy cùng lúc, hàng đợi lớn nhất 56 giây. Giới hạn số job đồng thời của tài
khoản chưa phải nút cổ chai, nên thêm job mảnh không làm PR chờ runner.

### 2.4 Bước nặng (cùng 32 lượt)

| job · bước | trung vị | p90 |
|---|---|---|
| `gate-packet-loop` · `packet-loop selftest` | **90,5** | **118,5** |
| `gate-registry` · `test registry` | 20,9 | 24,7 |
| `gate-cong-cu` · `G5 manh ban kinh dot bien` | 16,5 | 20,9 |
| `gate-ops` · `ci-duong-nhanh selftest` | 8,5 | 11,5 |
| `gate-ops` · `lease-publish selftest` | 7,5 | 8,5 |
| `gate-ops` · `bien-nhan v2 selftest` | 4,9 | 5,5 |
| `gate` · `G5 kiem ban ke cong cu + T1..T8` | 4,9 | 5,7 |
| `gate` · `tl selftest` | 3,7–4,0 | 4,4 |

Mọi bước thiết lập (checkout, setup-python, pip, actionlint, shellcheck, rg, ruff) đều dưới 0,2 phút/job ở trung vị.
**Cache pip hay cache công cụ không mua được gì đáng kể.**

### 2.5 Phút runner

Trung vị 295 phút runner mỗi lượt đầy đủ (p90 325): `gate-cong-cu` 140,6 (47,7 %), `gate-packet-loop` 91,1 (30,9 %),
`gate-ops` 23,0, `gate-registry` 21,3, `gate` 12,2, `gate-nhanh-manh` 9,2. Kho công khai nên phút runner chuẩn không
tính tiền; con số này chỉ dùng để so khối lượng việc.

### 2.6 Bộ test lớn dần

Đếm bằng cách nạp `packet_loop_test.py` ở năm commit master (`len(CASES)`, `len(MUTANTS)`), cạnh thời lượng bước
`packet-loop selftest` của lượt push tương ứng:

| commit | ngày | ca | đột biến | dòng test | dòng `packet_loop.py` | bước selftest |
|---|---|---|---|---|---|---|
| `0166d30` | 08-11 | 1.360 | 1.523 | 10.762 | 3.761 | 53,1 phút |
| `0964358` | 09-11 | 1.360 | 1.523 | 10.762 | 3.761 | 61,7 phút |
| `67102dc` | 10-11 | 1.445 | 1.800 | 14.786 | 6.109 | 92,4 phút |
| `6f32aad` | 12-11 | 1.457 | 1.821 | 15.665 | 6.222 | 111,8 phút |
| `072d45a` | 14-11 | 1.495 | 1.829 | 15.803 | 6.247 | 90,6 phút |

Cùng một ngày, thời lượng dao động mạnh (12-11: 79,5–126,1 phút) dù số ca gần như không đổi; độ ồn của runner lớn.

## 3. Nguyên nhân trong mã

### 3.1 Cách `packet_loop_test.py` chạy

`_legacy_main()` có hai pha, cả hai tuần tự trong một tiến trình:

- **Pha nền:** `chay_suite()` lặp `for ten, fn in CASES` và gọi từng ca. Phần lớn ca gọi CLI qua `run()`, tức
  `subprocess.run([sys.executable, packet_loop.py, …])` với `PYTHONDONTWRITEBYTECODE=1`.
- **Pha đột biến:** với mỗi mục của `MUTANTS`, ghi bản đột biến của `packet_loop.py` (hoặc của chính tệp test, 54 mục)
  vào thư mục riêng, rồi chạy **ca đích** của nó cộng **đối chứng khác họ** (ba ca cố định của họ kia, cộng đối chứng
  riêng của `r1187_*` và `m1174_*`). Tổng: 2.129 lượt ca đích, cộng khoảng 5.300 lượt đối chứng.

Không có song song ở tầng nào. Mỗi ca có thư mục tạm riêng và không ghi gì vào cây kho (quét: 0 lệnh ghi vào `ROOT`,
0 `os.chdir`, 0 thay đổi `git config --global`).

### 3.2 Đo từng ca trên runner thật

Không sửa tệp test. Một script bọc (Phụ lục B) nạp module, bọc từng hàm ca trong `CASES` bằng bộ bấm giờ, móc vào
`_phan_loai_dot_bien` để đánh dấu đầu mỗi đột biến, rồi gọi `main()` như CI gọi. Chạy trên nhánh tạm
`do-ci/pl-profile-20261115` (commit `41d78cd`, rẽ từ `072d45a`), workflow chỉ bắn ở `do-ci/**`, run
[`43624717342`](https://github.com/ducthangho/tra-luat/actions/runs/43624717342), `2026-11-14T18:06Z → 20:07Z`. Lượt
chạy trọn có bấm giờ kết thúc `TỔNG: ĐẠT` (rc=0), tức bộ bọc không làm đổi kết quả.

| pha | thời lượng (lượt bấm giờ) |
|---|---|
| nạp module | 1,3 s |
| pha nền, 1.493 ca | 58,5 phút |
| pha đột biến, 1.829 đột biến | 61,4 phút |
| tổng | 119,9 phút |

Lượt này chậm hơn trung vị CI (90,5 phút) khoảng 1,33 lần. Các ước lượng ở §4 quy về trung vị CI bằng hệ số 0,755.

**Pha nền.** Trung vị một ca 0,31 s; 440 ca trên 1 s; 28 ca trên 5 s. Phân bố rất lệch:

| hạng | ca | giây | cộng dồn |
|---|---|---|---|
| 1 | `wp1303_target_human_chain` | **1.469,8** | 41,9 % |
| 2 | `wp1303_target_supported_pairs` | 348,3 | 51,8 % |
| 3 | `kg_t6_ban_sua` | 94,4 | 54,5 % |
| 4 | `kg_t2_dt_head_ho` | 86,5 | 57,0 % |
| 5 | `kg_t2_head_ho` | 55,1 | 58,5 % |

Mười ca chậm nhất chiếm 62,5 % pha nền. Theo họ: `wp1303_*` 30,4 phút, `kg_*` (415 ca) 11,3 phút, `wp1174_*` 3,4 phút.

`wp1303_target_human_chain` chạy `_target_chain1303_one` cho 6 bộ danh tính cộng một lượt `None`, mỗi lượt khoảng
210 s. Mỗi lượt dựng lại trọn fixture `_composition1174` (kho git, remote bare, push, fetch, shim `git` bằng Python)
rồi đi hết vòng đời qua `m.main()`. Ca này còn là ca đích của ba đột biến (`wp1303_target_retired_dependency`,
`wp1303_native_final_assurance_coupling`, `wp1303_native_i2_binding`), mỗi lượt dưới đột biến khoảng 126 s.

**Pha đột biến.** Trung vị một đột biến 1,06 s. 100 đột biến chậm nhất chỉ chiếm 31,6 % pha, tức thời gian trải đều.
Chỗ tốn tập trung ở đối chứng:

| ca | số lượt | giây/lượt | tổng |
|---|---|---|---|
| `doctrine_scan_sach_xanh` | 1.754 | 0,21 | 366,4 s |
| `ac19_oan_claude_md_master` | 1.754 | 0,21 | 366,1 s |
| `ac18_nfkc_hai_cham_toan_rong` | 1.755 | 0,21 | 365,7 s |
| `wp1303_target_human_chain` | 3 | 125,9 | 377,8 s |
| `pl_m6_state_v1` | 15 | 6,88 | 103,3 s |

Sáu ca đối chứng cố định (`DOI_CHUNG_DOCTRINE` và `DOI_CHUNG_MAY_TRANG_THAI`) chạy tổng 5.327 lượt, 20,5 phút, tức
33,4 % pha đột biến.

### 3.3 Chi phí khởi tiến trình và biên dịch

Lượt thứ hai (nhánh `do-ci/pl-spawn-20261115`, commit `e9f4329`, run
[`43625858079`](https://github.com/ducthangho/tra-luat/actions/runs/43625858079), `18:19Z → 19:32Z`) đếm mọi lời gọi
`subprocess.run` từ tiến trình test ở pha nền:

| loại lệnh | số lần | tổng | mỗi lần |
|---|---|---|---|
| `python packet_loop.py …` | 6.479 | 1.758,8 s | 0,271 s |
| `python lease_publish.py …` | 1.276 | 516,8 s | 0,405 s |
| `git show` | 14.219 | 427,0 s | 0,030 s |
| `git ls-tree` | 8.492 | 249,4 s | 0,029 s |
| `git rev-parse` | 9.435 | 199,6 s | 0,021 s |
| mọi loại | 71.664 | 65,4 phút | — |

Lượt đếm làm đỏ 6 ca vì các ca ấy tự vá `subprocess.run`; số đếm vì thế hơi lệch, nhưng thứ tự lớn nhỏ không đổi.
Phần lớn lời gọi `git` đến từ mã sản phẩm chạy trong tiến trình test (ca gọi `m.main()`), không từ dựng fixture.

Vi đo trên cùng loại runner (job `vi-do` của run trên, 9 lần, lấy trung vị):

| phép đo | thời gian |
|---|---|
| `compile()` `packet_loop.py` (6.247 dòng) | 0,094 s |
| `compile()` `packet_loop_test.py` (15.803 dòng) | 0,314 s |
| `python -c pass` | 0,011 s |
| `python packet_loop.py --help`, không `.pyc` | 0,223 s |
| `python -m packet_loop --help`, `.pyc` checked-hash dựng sẵn | 0,086 s |

Mỗi lần gọi CLI tốn khoảng 0,14 s (0,223 − 0,086) chỉ cho việc nạp mã. Ở pha nền: 6.479 × 0,137 s ≈ 14,8 phút, tức
khoảng 25 % pha nền. Pha đột biến chưa đếm, nhưng cùng cơ chế: phần lớn 5.327 lượt đối chứng là một lời gọi CLI mỗi
lượt. `PYTHONDONTWRITEBYTECODE=1` và việc chạy tệp dưới dạng script (`python file.py` không
bao giờ dùng `.pyc`) là hai lý do. Cờ tắt `.pyc` có lý do lịch sử (va chạm `.pyc` theo mtime đã làm đột biến không chạy,
xem `CLAUDE.md`), nên đường thoát chỉ có thể là `.pyc` checked-hash, không phải bỏ cờ.

### 3.4 Thử chia mảnh và chạy song song

Cùng run `43624717342`, bộ bọc chạy thêm hai kiểu chia theo chỉ số (ca thứ i và đột biến thứ i vào mảnh `i % 4`):

| kiểu | mảnh 0 | mảnh 1 | mảnh 2 | mảnh 3 | thời gian tường |
|---|---|---|---|---|---|
| 4 job riêng | 26,5 phút | 18,6 phút | 57,0 phút | 29,2 phút | 57,0 phút |
| 4 tiến trình chung một runner | 40,5 phút | 35,4 phút | 71,4 phút | 43,9 phút | 71,9 phút |

Đọc ra ba điều:

1. **Chia theo chỉ số lệch tải nặng.** Mảnh 2 chứa `wp1303_target_human_chain` nên pha nền của nó 42 phút, các mảnh
   khác 6–10 phút. Chia phải theo chi phí đo được.
2. **Bốn tiến trình trên 4 vCPU chậm đi khoảng 1,5–1,9 lần mỗi tiến trình** (40,5/26,5; 35,4/18,6; 43,9/29,2). Mỗi
   ca tự sinh tiến trình con và gọi git, nên 4 vCPU (nhiều khả năng 2 lõi vật lý có SMT) không cho 4 lần.
3. **Không ca nào đỏ vì thứ tự hay vì chạy đồng thời.** Đỏ duy nhất là ba ca kiểm kê đọc sổ `MUTANTS` toàn cục
   (`kg_m5_kiem_ke`, `kg_t_ma_tran`, `dot_bien_test_khai_bao_chay_va_giet_dung_ca`) và dòng AC 18, cả bốn vì bộ bọc
   **lọc `MUTANTS` tại chỗ**. Không đột biến nào sống sót, không đối chứng nào chết oan, ở cả 8 lượt mảnh. Thiết kế
   thật phải chọn việc của làn bằng danh sách riêng, không được sửa sổ toàn cục. Giới hạn: mới đo một lần, chưa đủ để
   loại trừ ca chập chờn.

Mô phỏng chia theo chi phí (xếp việc dài trước vào làn rảnh nhất, dùng thời lượng từng ca và từng đột biến của lượt bấm
giờ, quy về trung vị CI):

| số làn | không tách ca nóng | tách `wp1303_target_human_chain` thành 7 |
|---|---|---|
| 2 | 45,2 phút | 45,2 phút |
| 4 | 22,6 phút | 22,6 phút |
| 6 | 18,5 phút | 15,1 phút |
| 8 | 18,5 phút | 11,3 phút |
| 12 | 18,5 phút | 7,5 phút |

Từ 6 làn trở lên, ca nóng 24,5 phút (18,5 phút quy đổi) là sàn. Mô phỏng chưa cộng chi phí cố định mỗi mảnh: tổng 4
mảnh riêng là 131,3 phút so với 119,9 phút chạy trọn, tức khoảng +9,5 %.

### 3.5 `gate-registry`: một bộ chiếm gần trọn job

Log job `gate-registry` của run `43579856328` (push `072d45a`) in thời lượng từng bộ:

| bộ | giây |
|---|---|
| `ops/ci_provenance_test.py` | **1.306,7** |
| `ops/cloud_agent_creds_test.py` | 331,0 |
| `.claude/dev/doc_receipt_thu_hoi_test.py` | 213,4 |
| `ops/land_evidence_nguon_test.py` | 131,1 |
| `.claude/dev/mcp_gh_test.py` | 40,2 |
| 10 bộ còn lại | dưới 33 s mỗi bộ |

Registry chạy hai bộ cùng lúc (`CI_DANG_KY_WORKERS: "2"`), lấy bộ theo thứ tự của sổ `MOI`. Dòng
`CI_DANG_KY_THOI_GIAN` của log cho mốc thật: luồng thứ nhất chạy `doc_receipt_thu_hoi_test.py` (0 → 213 s) rồi tới
`ci_provenance_test.py` (213 → 1.520 s); luồng thứ hai chạy hết 13 bộ còn lại và xong ở 559 s. Job vì thế dài bằng
`213 + 1.307` giây, còn luồng kia rảnh 16 phút. `ci_provenance_test.py` ở chế độ mặc định chạy 398 đột biến **tuần tự**,
mỗi đột biến một tiến trình con `--mot-ca`, khoảng 3,3 s mỗi đột biến. Chính tệp ấy đã có `ThreadPoolExecutor` cho chế
độ `--dot-bien-dong`, nhưng chế độ CI gọi không dùng.

### 3.6 `gate-ops`

Ba bước test tuần tự trong một job: `ci-duong-nhanh selftest` 8,5 phút (118 ca trong 1,2 phút, còn lại là vòng đột
biến), `lease-publish selftest` 7,5 phút, `bien-nhan v2 selftest` 4,9 phút, cộng 1,3 phút cgroup. Chưa đo bên trong
từng bộ; con số khả dĩ dưới đây là ước lượng từ tổng các bước.

### 3.7 Thứ không phải nguyên nhân

- Thiết lập job (checkout `fetch-depth: 0`, setup-python, pip, công cụ): dưới 0,2 phút mỗi job ở trung vị.
- Hàng đợi runner: p90 bằng 0 cho mọi job, lớn nhất 56 s.
- Windows: không lượt nào trong mẫu có job Windows.

## 4. Phương án, xếp theo lợi ích trên rủi ro

"Phút tường PR" là thời gian tường của một lượt PR đầy đủ, quy về trung vị CI. Hiện tại: 91 phút (p90 123).

| # | phương án | phút tường PR sau khi làm | căn cứ | rủi ro độ phủ | tệp phải sửa |
|---|---|---|---|---|---|
| **P1** | Chạy `packet_loop_test.py` theo N làn song song **trong** job: mỗi làn là một tiến trình con chạy một phần ca và đột biến chia theo chi phí, ghi biên nhận; tiến trình cha gom và phán như cũ | **~34–43** | §3.4: 4 làn ⇒ 22,6 phút việc mỗi làn × hệ số tranh chấp 1,5–1,9 đo được | Thấp nếu gom fail-close (thiếu làn, trùng việc, lệch băm ⇒ ĐỎ) và phán quyết giữ nguyên. Không bỏ ca, không bỏ đột biến | 1: `.claude/dev/packet_loop_test.py` |
| **P2** | `ci_provenance_test.py`: chạy 398 đột biến bằng `ThreadPoolExecutor` (việc thật nằm ở tiến trình con) | không đổi khi P1 chưa xong; registry 21 → **~13–15** | §3.5: 1.306,7 s / 4 luồng × hệ số tranh chấp 1,5–1,9 ≈ 490–620 s, cộng 213 s chờ sau `doc_receipt_thu_hoi_test.py` | Thấp: cùng đột biến, cùng phân hạng, chỉ đổi thứ tự thi hành | 1: `ops/ci_provenance_test.py` |
| P3 | Chia `gate-packet-loop` thành 8 job mảnh + job gom; giữ tên job gom là `gate-packet-loop` để context bắt buộc không đổi | **~25–28** (khi đó `gate-ops` là găng); riêng bước selftest ~19 | §3.4: 8 làn không tách ca nóng ⇒ 18,5 phút + thiết lập | Như P1, cộng rủi ro cấu hình workflow | 5–7: `ci.yml`, `packet_loop_test.py`, `ci_dang_ky_test.py` (`JOB_G5`), `chay-cong-windows.ps1` và `_test.ps1` (vân tay job), có thể `launcher_test.py` (`t152` đếm `AL_VER:`) |
| P4 | Tách `wp1303_target_human_chain` thành 7 ca con theo danh tính | chỉ có lợi sau P3: selftest ~19 → ~13 | §3.4 bảng mô phỏng | Trung bình: đổi ID ca đích của 3 đột biến và tập `_WP1303_LINUX_CASES` | 1 |
| P5 | `gate-ops`: chạy ba bộ test song song (bước nền + `wait`, hoặc tách job) | ~25 → ~22 sau P2, P3 | §3.6: 8,5 + 7,5 + 4,9 phút chạy chồng ⇒ ~10–12 phút | Thấp về độ phủ; trung bình về cấu hình (tên bước bị `ci_duong_nhanh_test.py` khoá từng chữ) | `ci.yml`, `ops/ci_duong_nhanh_test.py` |
| P6 | Gọi CLI qua `python -m packet_loop` với `.pyc` checked-hash trong `PYTHONPYCACHEPREFIX` riêng | giảm khoảng 25 % việc của pha nền, chưa đo pha đột biến | §3.3: 0,223 → 0,086 s mỗi lần, 6.479 lần ở pha nền | Trung bình–cao: đổi đường gọi mà hàng nghìn ca dựa vào; kho từng mất đột biến vì `.pyc` cũ (chỉ checked-hash mới an toàn, và phải có ca chứng minh mã đột biến thật sự chạy) | 1 |
| P7 | `gate-cong-cu` 8 → 12 mảnh | chỉ có lợi khi P1–P5 xong: 17 → ~12 | 140,6 phút việc / 8 mảnh | Thấp; số mảnh bị `ci_dang_ky_test.py` ghim | `ci.yml`, `ci_dang_ky_test.py` |
| — | Đưa pha đột biến của `packet_loop_test.py` sang master hoặc chạy hằng đêm | ~46 phút việc cắt khỏi PR | §3.2: pha đột biến 61,4 / 119,9 phút, quy về trung vị CI | **Cao**: PR land mà chưa chạy vòng đột biến; ngược hướng chủ kho đã chọn cho `cong_cu_test` ở #668 ("Chia mảnh mọi PR", PR nào cũng đo đủ) | không khuyến nghị |
| — | Chọn test theo đường dẫn đổi | thay đổi theo PR | — | **Cao**: kho đã trả giá hai lần vì logic điều kiện (`paths:` không bắn, nhãn thiếu `types:`), và chủ kho đã duyệt chạy vô điều kiện cho `ci-phamvi` ở Issue #254 | không khuyến nghị |
| — | Giảm đối chứng doctrine từ 3 xuống 1 mỗi đột biến | ~12 phút việc | §3.2: 18,3 phút cho 3 ca | Trung bình: mất 2/3 phép thử "đột biến đánh sai tầng" | không khuyến nghị lúc này |
| — | Cache pip / công cụ | < 1 phút | §3.7 | — | không đáng làm |

## 5. Khuyến nghị và thứ tự

1. **P1 trước.** Một tệp, không đụng `ci.yml`, không đổi ruleset, cắt khoảng 55 phút trung vị (khoảng 80 phút ở p90)
   mỗi lượt PR. Phút runner của job cũng giảm cùng tỉ lệ. Bộ máy làn + biên nhận + gom của P1 chính là thứ P3 cần,
   nên P3 sau đó gần như chỉ còn nối dây trong `ci.yml`. Đặc tả: `CI-PACKET-LOOP-SONG-SONG-r1.md`.
2. **P2 song song với P1** (write set không giao nhau). Nó không rút thời gian tường PR cho tới khi P1 xong, nhưng rẻ và
   rủi ro thấp, và sau P3 registry sẽ thành một trong các job găng. Đặc tả: `CI-PROVENANCE-SONG-SONG-r1.md`. Đưa
   `ci_provenance_test.py` lên đầu sổ `MOI` sẽ bớt thêm khoảng 3,5 phút, nhưng sổ ấy nằm ở
   `.claude/dev/ci_dang_ky_test.py`, ngoài write set của P2; để cho P3.
3. **P3 sau khi P1 land và đo canary.** Đặc tả soạn sau, dựa trên số đo thật của P1 (hệ số tranh chấp, chi phí cố
   định mỗi làn). Mục tiêu: lượt PR khoảng 25–28 phút.
4. P5, P4, P7, P6 theo thứ tự ấy, mỗi cái chỉ khi nó đã thành đường găng.

Ước lượng cộng dồn trên thời gian tường lượt PR, trung vị: 91 → ~34–43 (P1) → ~25–28 (P3) → ~22 (P5, P2). Số sau P1 là ước
lượng từ một lượt đo; canary của từng packet mới là số thật.

## 6. Việc chờ chủ kho

- **E5 (đổi mã cổng).** Hai đặc tả đi kèm sửa bộ test mà check bắt buộc `gate-packet-loop (ubuntu-latest)` và job
  `gate-registry` chạy. Không rõ việc đổi cách thi hành của bộ test có tính là "sửa mã cổng merge" theo `ADR-0067`
  không, nên hai đặc tả khai **chạm E5** và chờ chủ kho duyệt băm. Mang theo: diff dự kiến là một tệp mỗi packet,
  lý do ở §1, không ai được thêm quyền gì.
- **E4 (đi ra ngoài kho), đã làm.** Phiên này đẩy hai nhánh đo tạm `do-ci/pl-profile-20261115` và
  `do-ci/pl-spawn-20261115` lên GitHub (mỗi nhánh một workflow chỉ bắn trên `do-ci/**`, quyền `contents: read`) và để
  chúng chạy 8 job đo. Không nhánh nào mở PR, không chạm `ci.yml`. Muốn dọn thì xoá hai nhánh; artifact của hai run hết
  hạn theo mặc định 90 ngày.

## 7. Chưa đo được

- Thời lượng thật của P1 và P2 trên runner: chỉ có sau khi làm (canary ghi trong từng đặc tả).
- Hệ số tranh chấp khi các làn được chia **cân** (đo ở §3.4 là chia lệch).
- Ca chập chờn khi chạy song song: mới có một lượt cho mỗi kiểu.
- Bên trong `gate-ops` từng bộ tốn ở đâu (§3.6).
- Vì sao `wp1303_target_human_chain` tốn 210 s mỗi danh tính: mới biết fixture dựng lại 7 lần, chưa profile bên trong.
- Windows: mẫu không có lượt Windows nào; mọi số ở đây là Ubuntu.

## Phụ lục A — Script tải và tổng hợp số đo CI

```python
# tai.py: tai runs + jobs cua ci.yml qua gh api (REST)
import json, subprocess, sys, pathlib
OUT = pathlib.Path(sys.argv[1]); OUT.mkdir(parents=True, exist_ok=True)
def gh(path):
    r = subprocess.run(["gh", "api", path], capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        raise SystemExit(f"gh api {path} rc={r.returncode}: {r.stderr[:300]}")
    return json.loads(r.stdout)
runs = gh("repos/ducthangho/tra-luat/actions/workflows/ci.yml/runs?per_page=60&status=completed")["workflow_runs"]
(OUT / "runs.json").write_text(json.dumps(runs, ensure_ascii=False), encoding="utf-8")
for r in runs:
    jobs = gh(f"repos/ducthangho/tra-luat/actions/runs/{r['id']}/attempts/{r['run_attempt']}/jobs?per_page=100")
    (OUT / f"jobs-{r['id']}-{r['run_attempt']}.json").write_text(json.dumps(jobs, ensure_ascii=False), encoding="utf-8")
```

Tổng hợp: lọc lượt `conclusion == success` có `gate-cong-cu` không `skipped`; tên job bỏ phần `(…)` để gom ma trận;
trung vị và p90 theo nội suy tuyến tính. Thời lượng từng bộ của registry lấy từ dòng `"duong_dan": …, "giay": …` trong
log job `gate-registry`.

## Phụ lục B — Bộ bọc bấm giờ

Toàn văn ở `do-ci/do_pl.py` trên hai nhánh đo (`41d78cd`, `e9f4329`). Ý chính:

- nạp `.claude/dev/packet_loop_test.py` bằng `importlib` dưới tên `packet_loop_test`, `sys.path[0] = .claude/dev`;
- thay mỗi phần tử `(ten, fn)` của `CASES` bằng hàm bọc ghi `(đột biến hiện hành, ten, độ sâu, giây, đạt)`;
- bọc `_phan_loai_dot_bien`: khi được gọi từ `_legacy_main`, đóng mốc đột biến trước và mở mốc mới;
- `--manh i/N`: lọc `MUTANTS` theo chỉ số và đổi lời gọi `chay_suite` của pha nền sang tập ca `i % N` (chính cách lọc
  tại chỗ này làm đỏ ba ca kiểm kê, §3.4);
- `--dem-spawn`: thay `subprocess.run` bằng hàm đếm theo loại lệnh;
- ghi JSON ra `$RUNNER_TEMP`, ngoài cây kho, để không làm bẩn ảnh chụp mà `_carrier1174` đối chiếu.
