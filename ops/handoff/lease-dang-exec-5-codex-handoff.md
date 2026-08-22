# HANDOFF — `LEASE-DANG-DUNG-MOT-LAN` (#227), executor lượt 5 (`codex`) — **DỪNG, hoàn nguyên**

> Bản chép **NGUYÊN VĂN** stdout của lượt chạy `c5971812` (`ma_thoat=0`, `thoi_luong_giay=878.2`,
> `stdout_byte=3974`). Không sửa một byte nào dưới dấu gạch.
>
> **Lượt này KHÔNG commit gì.** Executor dừng ở chốt `D lần 3` do `r5` đăng ký trước, hoàn nguyên
> nhánh, và remote vẫn ở `b32b424165c4a952661cf776bf953d91a7eaf814` (phiên điều phối kiểm:
> worktree 0 mục bẩn, remote head khớp).
>
> **Vì sao đáng giữ dù không có commit nào:** nó chứa (a) bằng chứng rằng **kiến trúc của `r5`
> CHẠY** — `M1` ⇒ `65/66` ĐỎ `t64`, `M2`/`M3` cùng chết, cả sáu đột biến gỡ guard giết `t66`,
> hai tập guard bằng nhau 8 mục, không mutant đa sát; và (b) **chẩn đoán vì sao `T66` bất khả
> thi**, thứ trở thành căn cứ của `r6`.
>
> Phiên điều phối đo lại thứ tự trong YAML trên `b32b4241` và **xác nhận**:
> `TRƯỚC POST` = `kiem-github` · `check` · đọc `packet_issue` · `body` · dựng payload —
> `LÀ POST` = `ID=$(gh api …)` — `SAU POST` = `case "$ID"` · `mark` · `echo DA_DOI=1 >> $GITHUB_ENV`.
> Ba guard sau POST làm vế *"lease đó không POST"* bất khả thi theo nghĩa đen.

---

Đã **DỪNG theo chốt D lần 3**; không commit/push một phép đo dùng đồ giả sai trạng thái. Branch đã hoàn nguyên sạch, remote vẫn ở `b32b424165c4a952661cf776bf953d91a7eaf814`.

## 1. Kích thước và mỏ neo

```text
70   8  .github/workflows/ops-publish-lease.yml
105  7  ops/lease_publish.py
366  4  ops/lease_publish_test.py
```

Tổng hiện hành: **3 tệp, +541/−19** so với `cfaccff9`.

- Head: `b32b424165c4a952661cf776bf953d91a7eaf814`
- Tree: `28f32039574d3d66c02c65597690fd43c8c99544`
- Worktree: sạch
- Remote branch: cùng exact head
- Commit/push lượt 5: **không thực hiện**

## 2. Gate trên exact head hiện hành

| Phép đo | Kết quả |
|---|---|
| `python3 ops/lease_publish_test.py` | `63/63`, rc=0 |
| Suite với ba biến GitHub đặt và `gh` vắng | `63/63`, rc=0 |
| `actionlint .github/workflows/*.yml` | 5 workflow, rc=0 |

Không tuyên đây là nghiệm thu r5: T64–T66 không tồn tại trên head này.

## 3. Đột biến chẩn đoán trên bản thử nghiệm tạm

| Đột biến | Kết quả | Ca đỏ |
|---|---:|---|
| **M1** thêm guard `true` vào YAML | `65/66`, rc=1 | `t64` |
| **M2** xoá mục `$GITHUB_ENV` khỏi sổ | `65/66`, rc=1 | `t64` |
| **M3** ép bộ trích trả `set()` | `65/66`, rc=1 | `t64` |
| Gỡ guard `packet_issue` | `65/66`, rc=1 | `t66` |
| Gỡ guard `body` | `65/66`, rc=1 | `t66` |
| Gỡ guard payload | `65/66`, rc=1 | `t66` |
| Gỡ guard case ID | `65/66`, rc=1 | `t66` |
| Gỡ guard `mark` | `65/66`, rc=1 | `t66` |
| Gỡ guard `$GITHUB_ENV` | `65/66`, rc=1 | `t66` |

M1 đạt phép thử quyết định. Không có mutant đa sát.

Tuy nhiên, ba mutant cuối chỉ chết đủ “bốn vế” khi fake `gh` trả thành công nhưng cố tình không ghi side effect POST. Bản thử nghiệm đó đã bị loại và hoàn nguyên.

## 4. Hai tập guard của bản thử nghiệm

| Dẫn xuất từ YAML | Sổ đăng ký thử nghiệm |
|---|---|
| `python3 "$NEO/ops/lease_publish.py" kiem-github "$tep" --root .` | cùng lệnh |
| `python3 "$NEO/ops/lease_publish.py" check "$tep" --root .` | cùng lệnh |
| `ISSUE=$(python3 -c "…['packet_issue']…" "$tep")` | cùng lệnh |
| `python3 "$NEO/ops/lease_publish.py" body "$tep" > than.md` | cùng lệnh |
| `python3 -c "…json.dumps(…)…" > payload.json` | cùng lệnh |
| `ID=$(gh api "repos/$REPO/issues/$ISSUE/comments" …)` | cùng lệnh |
| `python3 "$NEO/ops/lease_publish.py" mark "$tep" --comment-id "$ID"` | cùng lệnh |
| `echo "DA_DOI=1" >> "$GITHUB_ENV"` | cùng lệnh |

Hai tập bằng nhau; M1/M2 chứng minh phép đối chiếu có răng. Sổ này không được commit vì T66 bên dưới bất khả thi theo nghĩa đen.

## 5. `chua_do_duoc` và lý do dừng

T66 yêu cầu mọi guard cùng chứng minh “lease đó không POST”. Nhưng thứ tự YAML thật là:

```text
gh api POST → kiểm case ID → mark → ghi $GITHUB_ENV
```

Vì vậy, khi chạm lỗi `case ID`, `mark` hoặc `$GITHUB_ENV`, POST đã xảy ra. Chính Q24 lượt 4 cũng xác nhận trường hợp `mark`: comment đã đăng nhưng ID chưa được lưu, tạo nguy cơ đăng trùng.

Muốn bốn vế cùng xanh chỉ có hai đường, đều không hợp lệ:

- làm fake trả ID thành công nhưng không ghi comment — vi phạm nguyên tắc fake giữ trạng thái;
- thêm rollback/preflight hoặc đổi thứ tự sản phẩm — ngoài đơn hàng T64–T66 và vượt thiết kế hiện hành.

Đây là **D lần 3: đặt cùng một câu kiểm chứng ở sai pha thời gian**. Nếu vẫn tuyên T66 đóng thì đồng thời thành A lần 7: lời khai rộng hơn phép đo. Do đó đã dừng và giữ branch sạch.

Các mục `_doc_gh`, `_kiem_loai_so_hieu`, `_kiem_comment_da_co`, GitHub Actions thật, Windows, khe race và nợ `chay(env=None)` vẫn chưa đo/không đóng.
