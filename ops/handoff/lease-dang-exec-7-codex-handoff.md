# HANDOFF — `LEASE-DANG-DUNG-MOT-LAN` (#227), executor lượt 7 (`codex`)

> Bản chép **NGUYÊN VĂN** stdout của lượt chạy `51e58345` (`ma_thoat=0`,
> `thoi_luong_giay=1209.1`, `stdout_byte=3255`). Không sửa byte nào dưới dấu gạch.
>
> Phiên điều phối đo lại độc lập trên exact head `ba82b06f`: `numstat` 3 tệp `+645/−19` (trần
> 660) · suite `68/68 rc=0` ở **cả hai** môi trường (`gh` xác nhận VẮNG) · `actionlint` `rc=0`
> trên 5 workflow · đếm `bao_chan` = **9**, khớp sổ 9 mục, **không `+1`**.
> **Bốn đột biến từng sống sót nay đều chết:** `D3` (`if ! cmd`) và `D4` (`cmd || rc=$?`) mỗi cái
> **`67/68`** ĐỎ `t64` — ở head trước **cả hai LỌT `67/67`**; `A5` (gỡ nhánh chặn của khối POST)
> **`64/68`** ĐỎ `t64 t66 t67 t68` — ở head trước **XANH TRỌN VẸN `67/67`**. `M4` vẫn giết:
> **`65/68`** ĐỎ `t51 t63 t67`.
>
> Executor cũng làm việc `r7` bắt trước khi báo xong: **tự đi tìm một nhánh chặn không gọi
> `bao_chan`** — rà 13 đường `continue`, mọi `exit`, mọi phép gán `BI_CHAN` — và **không tìm
> được**. Chốt `E lần 2` không kêu. Đó là một lời khai, và lượt review 5 sinh ra để đo nó.

---

Đã hoàn tất lượt 7, commit và push thành công.

### 1. Mỏ neo và kích thước

- Head/remote: `ba82b06f9df81fc2f13786fec590ec2110d046b7`
- Tree: `c7a182f37928156fbbf9e4e37053194e81056ccc`
- Worktree sạch; remote OID đã đọc ngược khớp.
- Provider: `openai_codex`; execution surface: Codex workspace service; transport: machine; role: Executor.
- Bản vá được tái dẫn xuất từ verdict, không chép mù.

`git diff --numstat cfaccff9..HEAD`:

```text
70   8  .github/workflows/ops-publish-lease.yml
105  7  ops/lease_publish.py
470  4  ops/lease_publish_test.py
```

Tổng: **3 tệp, +645/−19**, đạt trần `≤3`, `≤660`.

### 2. Hai lượt suite và gate

| Lệnh | Kết quả |
|---|---|
| `PATH=/tmp/actionlint:$PATH python3 ops/lease_publish_test.py` | `68/68`, rc=0 |
| Cùng suite với `GITHUB_ACTIONS`, `GITHUB_REPOSITORY`, `GITHUB_ACTOR` đặt; xác nhận `gh_absent=yes` | `68/68`, rc=0 |
| `/tmp/actionlint/actionlint .github/workflows/*.yml` | rc=0, đủ 5 workflow |
| `git diff --check cfaccff9..HEAD` | rc=0 |

### 3. Bảng đột biến

| Đột biến | Kết quả | Ca đỏ |
|---|---:|---|
| D2 — `set +e` một dòng | 67/68 | `t64` |
| D3 — `if ! cmd` | 67/68 | `t64` |
| D4 — `cmd \|\| rc=$?` | 67/68 | `t64` |
| A5 — gỡ nhánh POST rc≠0 | 64/68 | `t64,t66,t67,t68` |
| M1 — thêm guard chính tắc | 67/68 | `t64` |
| M2 — xóa mục `$GITHUB_ENV` khỏi sổ | 67/68 | `t64` |
| M3 — bộ trích không khớp | 67/68 | `t64` |
| M4 — chuyển `check` xuống sau POST | 65/68 | `t51,t63,t67` |
| Gỡ `kiem-github` | 64/68 | `t60,t64,t66,t67` |
| Gỡ `check` | 64/68 | `t51,t64,t66,t67` |
| Gỡ `packet_issue` | 65/68 | `t64,t66,t67` |
| Gỡ `body` | 65/68 | `t64,t66,t67` |
| Gỡ payload | 65/68 | `t64,t66,t67` |
| Gỡ `case ID` | 65/68 | `t64,t66,t67` |
| Gỡ `mark` | 65/68 | `t64,t66,t67` |
| Gỡ `$GITHUB_ENV` | 65/68 | `t64,t66,t67` |

Tổng: **16/16 mutant đỏ**. Hai phản chứng Q34 riêng — bọc `try` và `next(..., mặc_định)` — đều `67/68`, chỉ `t65` đỏ.

A5 có bằng chứng hành vi:

```text
gốc: rc=1, giua POST đúng 1 lần, marks["giua"]=false
A5 : rc=0, giua POST đúng 1 lần, marks["giua"]=true
```

### 4. Sổ đăng ký sau Q33

```text
bao_chan = 9  |  mục trong sổ = 9  |  nhánh dẫn xuất = 9
```

Không có `+1`. Chín mục là:

```text
kiem-github · check · packet_issue · body · payload
post_rc · case_id · mark · github_env
```

Mục POST cũ đã đổi tên thành `post_rc`; nhánh `case "$ID"` được đăng ký riêng bằng `case_id`.

### 5. `chua_do_duoc` và chốt E

- Chưa chạy GitHub Actions thật, Windows hoặc `gh` thật; mọi phép đo workflow dùng Bash và đồ giả giữ trạng thái.
- Không đụng khe race, cửa sổ POST→`mark`, nợ `chay(env=None)`, LIVE, merge hoặc deploy.
- Đã rà toàn bộ 13 đường `continue`, mọi `exit` và mọi phép gán `BI_CHAN`: chín nhánh lỗi đều gọi `bao_chan`; bốn đường còn lại là hai bộ lọc đầu vào và hai đường `rc=9` bỏ qua hợp lệ.
- **Không tìm được nhánh chặn nào không gọi `bao_chan`; chốt E lần 2 không kêu.**
