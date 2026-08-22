# HANDOFF — `LEASE-DANG-DUNG-MOT-LAN` (#227), executor lượt 4 (`codex`)

> **Bản chép NGUYÊN VĂN** stdout của lượt chạy `04e788b9` (`launcher.py`, `ma_thoat=0`,
> `thoi_luong_giay=1857.2`, `stdout_byte=6427`). Không sửa một byte nào của phần dưới dấu gạch.
>
> **Vì sao tệp này tồn tại:** `r4` §`chua_do_duoc` mục 3 khai một khoảng mù của quy trình —
> *"báo cáo của executor không sống trong kho"*. Reviewer lượt 3 đã đụng phải nó: `r3` đòi
> executor khai đường Q18 và đột biến đa sát, executor **có** khai, nhưng kênh khai là **stdout
> của lượt chạy**, nên reviewer không đo được và phải ghi *"không kết luận là chưa khai"*.
> Tệp này vá khoảng mù đó cho lượt 4.
>
> **Điều đáng ghi nhất:** executor **TỰ DỪNG** ở chốt `C lần 2` do `r4` đăng ký trước, thay vì
> vá tiếp. Nó giao đủ `T62`/`T63`/`Q23`, rồi bảng `Q24` phát hiện một nhánh an ninh **ngoài đơn
> hàng** thiếu phản chứng, và nó **từ chối tự mở rộng phạm vi**. Chốt đăng ký trước đã **chạy
> thật**, không phải chữ trong tài liệu.
>
> Phiên điều phối đã đo lại độc lập trên exact head `b32b4241`: `numstat` 3 tệp `+541/−19`
> (trần 570) · suite `63/63 rc=0` ở **cả hai** môi trường (`gh` xác nhận VẮNG) · `actionlint`
> `rc=0` trên 5 workflow · **D24** ⇒ `62/63`, ĐỎ `t62` · **D23** ⇒ `62/63`, ĐỎ `t63` (cả hai
> SỐNG SÓT `61/61` ở head trước) · gỡ guard `mark rc≠0` ⇒ **`63/63` SỐNG SÓT**, `actionlint`
> `rc=0` — tức lời khai `C lần 2` của executor **đúng**.

---

Kết luận: đã commit và push đầy đủ T62/T63/Q23, nhưng **không tuyên bố packet hoàn tất**. Bảng Q24 phát hiện đúng điều kiện dừng **C lần 2**: nhánh an ninh `mark rc≠0` ngoài T62/T63 chưa có phản chứng bền.

## 1. Kích thước và mỏ neo

- Head: `b32b424165c4a952661cf776bf953d91a7eaf814`
- Tree: `28f32039574d3d66c02c65597690fd43c8c99544`
- Commit: `ops: khóa nhánh rc9 của cổng đăng lease`
- Đã push và đọc ngược remote khớp head.
- Worktree sạch.

```text
70   8  .github/workflows/ops-publish-lease.yml
105  7  ops/lease_publish.py
366  4  ops/lease_publish_test.py
```

Tổng: **3 tệp, +541/−19**, đạt trần `≤3`, `≤570`. Delta riêng r4: một tệp, `+22/−4`.

## 2. Hai lượt suite và gate

Trên exact head `b32b4241…`:

| Phép đo | Kết quả |
|---|---|
| `PATH=/tmp/actionlint:$PATH python3 ops/lease_publish_test.py` | `63/63`, rc=0 |
| Suite với `GITHUB_ACTIONS=true`, `GITHUB_REPOSITORY=ducthangho/tra-luat`, `GITHUB_ACTOR=ducthangho`, xác nhận `gh` vắng | `63/63`, rc=0 |
| `/tmp/actionlint/actionlint .github/workflows/*.yml` | 5 workflow, rc=0 |
| `git diff --check cfaccff9..HEAD` | rc=0 |

## 3. Bảng đột biến

Ba đột biến bắt buộc:

| Đột biến | Kết quả | Ca đỏ |
|---|---:|---|
| **D22** — `kiem-github rc=9` thành lỗi | `62/63`, actionlint=0 | `t62` |
| **D23** — `check rc=9` đi tiếp | `62/63`, actionlint=0 | `t63` |
| **D24** — `kiem-github rc=9` đi tiếp | `62/63`, actionlint=0 | `t62` |

Các đối chứng khác trên cùng exact head:

| Đột biến | Kết quả | Ca đỏ |
|---|---:|---|
| D6 dấu ở vị trí bất kỳ | 62/63 | `t55b` |
| D7 thiếu `user.login` thì cho qua | 62/63 | `t55a` |
| D8 ghép D6+D7 | 61/63 | `t55a,t55b` |
| D10 bỏ khối `kiem-github` | 60/63 | `t59,t60,t62` |
| D11 nuốt mã thoát | 61/63 | `t60,t62` |
| D12 đảo thứ tự | 62/63 | `t59` |
| D13 bỏ đúng lease giữa | 60/63 | `t59,t60,t62` |
| D14 không `continue` | 62/63 | `t60` |
| D15 không đặt `BI_CHAN` | 62/63 | `t60` |
| D16 cho `kiem()` gọi mạng lại | **54/63** | **9 ca:** `t01,t02c,t02d,t09,t14,t21,t50,t53,t58` |
| D17 CLI gọi `kiem()` thuần | 62/63 | `t49` |
| D18 bỏ lớp comment | 62/63 | `t46` |
| D19 bỏ lớp đo loại số hiệu | 61/63 | `t43,t44` |
| D20 bỏ `--root .` | **63/63 sống sót** | Chủ ý: cờ dư, chú thích đã khai |
| D21 dùng bản HEAD thay `$NEO` | 56/63 | `t25,t51,t52,t59,t60,t62,t63` |

Đột biến đa sát: D8=2, D10=3, D11=2, D13=3, **D16=9**, D19=2, D21=7.

Không có câu “8 ca” trong write set; Q23 được sửa ở báo cáo bằng phép đo thực tế **9 ca**.

## 4. Bảng Q24 — từng nhánh rẽ

Phạm vi: mọi nhánh mới/đổi trong `cfaccff9..HEAD`, cộng nhánh `check rc=9` do Q22 mở rộng.

| Nhánh | Phép đo đỏ nếu gỡ/đảo | Chưa đo bền |
|---|---|---|
| `kiem-github rc=9` → bỏ qua, rc chung 0 | `t62`; D22 và D24 | Không |
| `kiem-github rc≠0,9` → chặn, tiếp lease khác, rc chung ≠0 | `t60`; D11/D14/D15 | Không |
| `kiem-github rc=0` → tới `check` | `t59`; D10/D13 | Không |
| `check rc=9` → bỏ qua, rc chung 0 | `t63`; D23 | Không |
| `check rc≠0,9` → chặn nhưng xử lý tiếp | `t51` | Không |
| `check rc=0` → POST | `t51,t59,t63` | Không |
| Đọc `packet_issue`: rc=0 / rc≠0 | Chưa có fixture làm lệnh đọc hỏng | **Có** |
| `body`: rc=0 / rc≠0 | Gỡ guard vẫn `63/63`, actionlint=0 | **Có** |
| Dựng payload: rc=0 / rc≠0 | Chưa có fixture làm JSON builder hỏng | **Có** |
| POST: rc=0 / rc≠0 | `t52` | Không |
| `case ID`: số / rỗng-hoặc-phi-số | Chưa có fake trả ID phi-số | **Có** |
| `mark`: rc=0 / rc≠0 | Gỡ guard vẫn `63/63`; probe A/B: gốc rc=1, mutant rc=0 | **Có — C lần 2** |
| Ghi `$GITHUB_ENV`: rc=0 / rc≠0 | Gỡ guard vẫn `63/63`, actionlint=0 | **Có** |
| `BI_CHAN=0` / `BI_CHAN≠0` | `t51,t52,t60` | Không |
| Ghi ngược: `always() && DA_DOI==1` đúng / sai | Nhánh đúng: `t52`; nhánh sai chưa có ca riêng | Một nửa |
| `_doc_gh`: gọi lỗi / rc≠0 / JSON lỗi / JSON hợp lệ | rc≠0 có `t44,t48`; hai lỗi còn lại chưa có fixture riêng | Một phần |
| `_repo_github`: repo hợp lệ / sai dạng | Chỉ đường hợp lệ được đo | **Có** |
| `_kiem_loai_so_hieu`: lỗi đo / phản hồi hỏng / PR / Issue / URL lạ | `t44` / chưa / `t43` / `t45` / chưa | Một phần |
| `_kiem_comment_da_co`: không-list / `[]` / flat / nested / mixed | `[]` và nested: `t57`; ba dạng kia chưa | Một phần |
| Comment: thiếu body / thiếu user / bot+dấu đầu / các ca không khớp | chưa / `t55a` / `t46` / `t47,t54,t55b` | Một phần |
| `lease_id`: đúng regex / sai regex | ca thường / `t56` | Không |
| CLI giữ hai lớp / bỏ comment / bỏ loại số hiệu | D17/D18/D19 | Không |
| Fake r4 `kiem-github`: exit 9 / 8 / 0 | `t62` / `t60` / `t59` | Không |
| Fake r4 `check`: exit 9 / 8 / 0 | `t63` / `t51` / `t59` | Không |
| Fake POST: lỗi 42 / thành công | `t52` / `t51,t62,t63` | Không |

Phản chứng xác nhận C lần 2: khi fake `mark` hỏng ở lease giữa, bản gốc trả rc=1 và chỉ ghi hai `DA_DOI`; mutant gỡ guard trả rc=0 và ghi ba `DA_DOI`, dù comment ID của lease giữa chưa được lưu—mở đường đăng trùng lần sau.

## 5. `chua_do_duoc` và trạng thái handoff

- **T62/T63: đóng bằng phép đo.**
- **Q23: đóng bằng phép đo 9 ca.**
- **Packet: DỪNG theo C lần 2**, không được gọi là hoàn tất.
- Không tự thêm T64 hoặc vá `body/mark/GITHUB_ENV`, vì chúng ngoài đơn hàng T62/T63.
- Chưa có GitHub Actions thật hoặc Windows; khe race xuyên hai nhánh vẫn chỉ “thu hẹp”; nợ `chay(env=None)` giữ delta=0.
- Nhánh `--root .` vẫn không có mutant giết được, nhưng đây là dư thừa đã khai, không phải chốt.
- Handoff cần một Packet revision/lease mới nếu người giữ kho muốn khóa các nhánh vừa lộ.

Provider: `openai_codex`; execution surface: Codex workspace service; transport: machine; role: executor. Adapter `work-packet` buộc preflight exact lease/spec/head/write-set và là lý do không tự vá tiếp sau khi chạm stop condition.
