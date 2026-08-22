Đo xong. Cây review sạch, `HEAD` không đổi (`9f5b08e8…`), không sửa/commit/push gì; mọi đột biến chạy trên bản sao tạm dựng bằng `git archive` trong `/tmp`.

```
KET_LUAN: can_sua
reviewed_sha: 9f5b08e81a131a1c22d15b6d5809885eae11413f
```

**Neo đã kiểm** — cả bốn khớp: `git rev-parse HEAD` = `9f5b08e8…`; spec r3 = `c65d5dbd9d2b398978226f6863cf7cd4e4ddb219a7086be0005e65804a0f47da`; r2 = `3f310582de59dce7c109717dbab13ef9467b80c67ffeafc0ac8e1484309e0093`; verdict lượt 2 = `f21069548bf0e0ff507822a246283fe47417bc334fa1e231b2e71dc88d52b4c0`. `git diff --numstat cfaccff9..HEAD` = 3 tệp **+523/−19** (trần 550). Delta lượt 3 = 1 tệp **+37/−12**. Suite **61/61 rc=0**, `actionlint` rc=0 (5 tệp).

---

## Bảng đột biến (tất cả trên bản sao tạm từ `9f5b08e8`, nền `D0 = 61/61`)

```
D10 xoá khối gọi kiem-github khỏi YAML        59/61  ĐỎ=[t59, t60]
D11 gọi nhưng nuốt mã thoát                    60/61  ĐỎ=[t60]
D12 gọi kiem-github SAU check (đảo thứ tự)     60/61  ĐỎ=[t59]
D13 bỏ qua kiem-github cho ĐÚNG lease `giua`   59/61  ĐỎ=[t59, t60]
D14 rc≠0 → BI_CHAN=1 nhưng KHÔNG `continue`    60/61  ĐỎ=[t60]     (chỉ phá vế "không POST")
D15 rc≠0 → `continue` nhưng KHÔNG BI_CHAN      60/61  ĐỎ=[t60]     (chỉ phá vế "rc≠0")
D6  dấu ở bất kỳ vị trí (`dau in body`)        60/61  ĐỎ=[t55b]
D7  thiếu user.login ⇒ cho qua                 60/61  ĐỎ=[t55a]
D8  phá CẢ HAI (D6+D7)                         59/61  ĐỎ=[t55a, t55b]
D16 cho kiem() gọi mạng trở lại                52/61  ĐỎ=9 ca, có t53
D17 lệnh kiem-github gọi kiem() (bỏ hai lớp)   60/61  ĐỎ=[t49]
D18 bỏ lớp dò comment đã có                    60/61  ĐỎ=[t46]
D19 bỏ lớp đo loại số hiệu                     59/61  ĐỎ=[t43, t44]
D21 kiem-github gọi bản HEAD (bỏ $NEO)         56/61  ĐỎ=[t25,t51,t52,t59,t60]
D20 bỏ cờ `--root .` của kiem-github           61/61  SỐNG SÓT     (chú thích YAML tự khai là dư)
D22 nhánh rc=9 của kiem-github → thành LỖI     61/61  SỐNG SÓT
D24 nhánh rc=9 của kiem-github → ĐI TIẾP       61/61  SỐNG SÓT  ← xem P2
```

### 1. `t59`/`t60` đo THỨ THẬT — có

Không phải bản chép: `_buoc_workflow()` (`ops/lease_publish_test.py:168`) đọc thẳng `HERE.parent/.github/workflows/ops-publish-lease.yml`, và `bang(tep.is_file(), …)` **chết cứng** nếu thiếu — không có nhánh "không thấy thì bỏ qua". Bằng chứng hành vi mạnh hơn bằng chứng đọc code: **D10–D15 và D21 chỉ sửa YAML**, và chúng làm `t59`/`t60` đỏ.

- **Đảo thứ tự (D12) bị bắt** — `t59` đòi `index(kiem-github) < index(check)`, không chỉ đòi có mặt.
- **Bỏ một lease (D13) bị bắt** — `t59` lặp cả ba lease và đòi `count == 1` cho từng lease.
- **Hai vế của `t60` đo riêng được**: D14 phá đúng vế "không POST" (bước vẫn đỏ) → `t60` đỏ; D15 phá đúng vế "rc≠0" (lease vẫn bị bỏ) → `t60` đỏ.

### 2. `T53` — lời khai đã hạ, và ca vẫn còn răng

Đổi tên `t53_suite_trong_Actions_khong_gh_van_QUA` → `t53_check_trong_Actions_khong_gh_van_QUA`. Lời khai mới **khớp đúng** thứ ca làm (một lệnh `check`, `GITHUB_ACTIONS=true`, `PATH` rỗng), không rộng hơn. `grep -rn "toàn suite\|T53"` trên `lease_publish.py` · `lease_publish_test.py` · YAML: **không còn dòng nào** khai "toàn suite". Không mất răng: **D16 vẫn giết `t53`**.

Đo thêm cho rõ biên: toàn suite với ba biến đặt, `gh` vắng → `ACTOR=ducthangho` **61/61 rc=0**; `ACTOR=nguoi-la` **39/61 rc=1** (nợ nền `chay(env=None)`, delta = 0 — không báo).

### 3. `t55a`/`t55b` — tách THẬT

D6 giết **chỉ** `t55b`, D7 giết **chỉ** `t55a`, D8 (phá cả hai) giết **cả hai**. Vị từ giữ nguyên so với `t55` cũ (`ex1.ma == RC_NOI_DUNG` → `t55a`; `ex2 is None` → `t55b`), không nới.

### 4. Hồi quy — không có ca nào bị nới lỏng

12 dòng bị xoá: chữ ký `_chay_buoc_dang` (thêm tham số), dòng `SystemExit(0)` câm của đồ giả (nay có điều kiện), hai dòng dựng biến/env (mở rộng), tên `t53` (đổi tên), và 6 dòng thân `t55` cũ (tách nguyên vị từ). Không dòng nào là chốt bị hạ. D17/D18/D19/D21 xác nhận các ca cũ (`t49`, `t46`, `t43`/`t44`, `t25`) vẫn có răng.

---

## P2 — Nhánh `rc=9` của `kiem-github` là chốt chống **ĐĂNG TRÙNG XUYÊN NHÁNH**, và không phép đo nào ĐỎ khi gỡ nó theo hướng FAIL-OPEN

`rc=9` từ `kiem-github` nghĩa là *"comment cho lease này ĐÃ CÓ trên issue"* — trường hợp lease đã đăng từ nhánh A còn nhánh B chưa được ghi ngược `posted_comment_id`. Đó là **cửa duy nhất** chặn POST lần hai ở mức wiring: `check` ở nhánh B trả `0` vì tệp cục bộ không có `posted_comment_id`.

Đột biến D24 — đổi `if [ "$rc" = "9" ]; then … continue; fi` + `if [ "$rc" != "0" ]` thành `if [ "$rc" != "0" ] && [ "$rc" != "9" ]`:

```
d24_rc9_cua_kiem_github_DI_TIEP_dang_trung   rc=0  lease_publish: 61/61 đạt  ĐỎ=[]
```

Không dừng ở suy luận — đo hành vi bằng chính hạ tầng `_chay_buoc_dang` (đồ giả trả `9` thay vì `8`, ~15 dòng):

```
YAML nguyên bản (9f5b08e8)   rc=0  lease `giua` BỊ POST: False
   calls=[kiem-github dau, check dau, body dau, mark dau,
          kiem-github giua,                                  <- dừng đúng chỗ
          kiem-github cuoi, check cuoi, body cuoi, mark cuoi]
D24 rc=9 đi tiếp             rc=0  lease `giua` BỊ POST: True
   calls=[…, kiem-github giua, check giua, body giua, mark giua, …]   <- POST TRÙNG
```

Hành vi hiện tại **đúng**; thứ thiếu là **phản chứng**. Gỡ chốt ⇒ lease bị đăng hai lần, `61/61` vẫn xanh, `actionlint` vẫn rc=0. Đây đúng tên packet: `LEASE-DANG-DUNG-MOT-LAN`.

**Vì sao nó trong phạm vi:** khối `kiem-github` nằm trong diff của chính packet (`cfaccff9..HEAD`), và `T59`/`T60` được đặt ra để đo **khối đó**. Đây là câu hỏi §5 của prompt — *"phép đo nào ĐỎ nếu ai đó gỡ nó?"* — và với nhánh này câu trả lời là **không có**.

**Đối chứng để khỏi đổ oan:** nhánh `rc=9` của `check` cũng không ai đo (D23 sống sót `61/61`), nhưng nhánh ấy **có từ `cfaccff9`** ⇒ delta = 0, không báo. Nhánh `rc=9` của `kiem-github` **mới có trong packet này**.

**Vá (rẻ, hạ tầng đã có, ~15 dòng):** thêm tham số `kiem_github_rc9=` vào `_chay_buoc_dang` (đồ giả trả `9`), rồi một ca `t61`: lease đó **không** được POST, hai lease kia POST bình thường, và bước **rc=0** (bỏ qua ≠ lỗi). Khi ấy D22 **và** D24 đều phải ĐỎ — hai hướng, hai đột biến.

**Về bộ đếm hình dạng — tôi KHÔNG làm tròn (L1).** Đây là hình dạng **C** (*phản chứng bắt buộc còn thiếu*), ở đúng khối mà C lần 1 chỉ vào. Hai cách đọc đều đứng được: (a) **C lần thứ 2** — chốt khác, nhánh khác, đột biến khác ⇒ theo chốt r3 (*"C lần thứ 2 ⇒ DỪNG, không vá, xuất handoff"*) thì verdict phải là `dung_lai`; (b) **C lần 1 chưa đóng hết** — `T59`/`T60` đóng nửa "có gọi / tôn trọng rc≠0", còn nửa "tôn trọng rc=9" chưa ⇒ `can_sua`. Tôi để `can_sua` vì phép vá là cơ học và r3 chỉ đặt hàng `T59`/`T60` (executor đã giao đủ), **nhưng việc tăng bộ đếm là quyết định của người giữ kho, không phải của tôi** — và nếu người giữ chọn (a) thì chốt đã đăng ký trước của chính r3 nói là DỪNG.

---

## P3 — `r3` khai đột biến `cho kiem() gọi mạng trở lại` giết **8 ca**; đo được **9**

```
9f5b08e8 : 52/61  ĐỎ=[t01, t02c, t02d, t09, t14, t21, t50, t53, t58]   (9 ca)
90015a53 : 49/58  ĐỎ=[t01, t02c, t02d, t09, t14, t21, t50, t53, t58]   (9 ca)
```

Sai số bắt nguồn từ verdict lượt 2 (con số `49/58` đúng — tức 9 ca đỏ — nhưng câu chữ ghi *"giết 8 ca"* vì `t02c`/`t02d` bị gộp làm `t02`), rồi r3 chép lại. **Delta = 0** — không phải hồi quy của lượt 3, và không phải lỗi của executor. Nhưng r3 biến con số ấy thành **tiêu chí nghiệm thu** (*"đột biến giết nhiều ca phải được KHAI, kể cả … → 8 ca"*), nên biên nhận phải ghi **9**, kèm hai tên `t02c` và `t02d`. `bo lop do loai so hieu → t43+t44` thì đo đúng như khai (D19).

---

## Bảng: P1 + ba P3 của lượt 2

| # | finding lượt 2 | trạng thái | phép đo của tôi |
|---|---|---|---|
| P1 | Không phép đo nào bắt việc workflow BỎ gọi `kiem-github` | **ĐÓNG** | D10 `59/61` (t59+t60), D11 `60/61` (t60) — lượt 2 cả hai **sống sót** `58/58`. Thêm ba hướng tấn công tôi tự dựng: D12 đảo thứ tự → t59; D13 bỏ đúng một lease → t59+t60; D14/D15 tách hai vế của t60 → t60 mỗi lần. `t59`/`t60` đọc **YAML thật** (mọi đột biến trên đều chỉ sửa YAML). *Nửa `rc=9` của cùng khối vẫn hở — P2 trên, tính là finding MỚI.* |
| P3-1 | `T53` khai "toàn suite", đo một lệnh | **ĐÓNG** (đường b) | Tên ca hạ xuống `t53_check_trong_Actions_khong_gh_van_QUA`; `grep` không còn chuỗi "toàn suite" trong mã; lời khai không hẹp tới mức mất nghĩa (vẫn đo `rc=RC_OK` **và** dòng `KHÔNG CHẠY`); D16 vẫn giết `t53` ⇒ **không mất răng**. Đo biên: `ACTOR=ducthangho` 61/61, `ACTOR=nguoi-la` 39/61 (nợ nền, delta=0). |
| P3-2 | `chua_do_duoc` r2 khai HẸP hơn thực tế | **KHÔNG ĐÓNG bằng mã — đúng thiết kế** | r3 đưa vào `ngoai_pham_vi` (`ops/specs/**` ngoài `write_set`, spec đã có băm thì không sửa đè), chuyển sang biên nhận + `ops/reviews/README.md`, do phiên điều phối làm. Không có gì để executor đo. |
| P3-3 | `t55` gộp hai khiếm khuyết + đột biến đa sát chưa KHAI | **ĐÓNG phần tách; phần KHAI lệch 1** | Tách: D6→chỉ `t55b`, D7→chỉ `t55a`, D8→cả hai. KHAI: `bo lop do loai so hieu → t43+t44` đúng (D19); `cho kiem() gọi mạng trở lại` khai **8**, đo **9** (P3 trên). |

---

## `da_do_gi`

- Kiểm 4 băm neo (r2, r3, verdict lượt 2, HEAD) — khớp cả bốn.
- Ngân sách `+523/−19` ≤ 550, `write_set` đúng 3 tệp; delta lượt 3 `+37/−12` đúng một tệp test.
- Suite `61/61 rc=0` (≥61 theo r3); `actionlint` rc=0 trên 5 workflow; suite dưới `GITHUB_ACTIONS`+`GITHUB_REPOSITORY`+`GITHUB_ACTOR`, `gh` vắng → `61/61 rc=0`.
- **19 đột biến** trên bản sao tạm (bảng trên) — trong đó 7 cái tôi tự nghĩ ra ngoài danh sách r3 (D12, D13, D14, D15, D20, D22, D24) và 4 cái đo lớp dưới (D17–D19, D21).
- Đọc 12 dòng bị xoá từng dòng một, đối chiếu vị từ cũ/mới của `t55`.
- **D20 đo rồi BÁC**: bỏ cờ `--root .` sống sót `61/61`, nhưng chú thích YAML tự khai cờ này là dư để rõ nghĩa (`_goc_kho` đi ngược tìm `.git` ra cùng chỗ) — lời khai ĐÚNG, không phải khuyết tật.
- Xác nhận `_buoc_workflow` fail-close khi thiếu tệp YAML (không có nhánh "bỏ qua êm" kiểu `t24`).
- Cây review sạch, `HEAD` không đổi sau toàn bộ phép đo.

## `khong_do_duoc`

- **Báo cáo của executor** — r3 đòi khai rõ đã chọn đường Q18 nào và vì sao, và khai đột biến đa sát. Trong kho ở head **không có tệp báo cáo nào**; thông điệp commit `9f5b08e8` đúng một dòng. Lời khai hẳn nằm ở PR, mà phiên này **không được cấp quyền** gọi `mcp__github__list_pull_requests` ⇒ tôi không đọc được. **Không kết luận là "chưa khai"** — chỉ nói là chưa đo được, và người giữ kho phải tự xác nhận trước khi land.
- Chưa có lượt Actions THẬT: `t59`/`t60` chạy thân bước bằng `bash` + `lease_publish.py` giả; runner thật chưa từng chạy khối này.
- Chưa có lượt Windows cho packet.
- Mỏ neo `user.login == "github-actions[bot]"` vẫn là TÀI LIỆU, không phải phép đo (r3 `chua_do_duoc` #2).
- Ruleset/branch protection cho `.github/workflows/**` và `ops/lease_publish*.py` — ngoài kho, không đo được.

## Vẫn còn hở (đọc kèm `can_sua`, đừng đọc rộng hơn)

1. **Nhánh `rc=9` của `kiem-github` không có phản chứng** (P2) — gỡ theo hướng fail-open ⇒ đăng trùng, suite vẫn xanh.
2. Nhánh `rc=9` của `check` cũng vậy (delta = 0 so `cfaccff9`, ngoài phạm vi lượt này nhưng cùng lớp — vá một thể thì rẻ hơn).
3. `t59` chỉ so `argv[0:2]`; đổi/bỏ cờ phía sau (vd `--root .`) vô hình với nó.
4. Nợ nền `chay(env=None)`: `GITHUB_ACTOR` ngoài allowlist ⇒ `39/61`. Delta = 0, không phải finding của packet, nhưng vẫn là mìn cho `ci.yml` khi có actor khác đẩy.
5. Khe race hai nhánh `ops/**` chỉ **THU HẸP** (`concurrency` gom theo `github.ref`), **không đóng**.

Nguồn sự thật là tệp có băm trong kho; bản này chỉ là bản chiếu.
