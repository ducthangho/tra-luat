# HANDOFF — `LEASE-DANG-DUNG-MOT-LAN` (#227), executor lượt 6 (`codex`)

> Bản chép **NGUYÊN VĂN** stdout của lượt chạy `004b1d50` (`ma_thoat=0`,
> `thoi_luong_giay=1323.6`, `stdout_byte=5146`). Không sửa một byte nào dưới dấu gạch.
>
> Phiên điều phối đã đo lại độc lập trên exact head `6eaa3755`: `numstat` 3 tệp `+633/−19`
> (trần 660) · suite `67/67 rc=0` ở **cả hai** môi trường (`gh` xác nhận VẮNG) · `actionlint`
> `rc=0` trên 5 workflow · **M4** (dời khối `check` từ TRƯỚC POST xuống NGAY SAU POST, giữ nguyên
> tập vế) ⇒ phép dẫn xuất thấy `check` ở dòng 71 và POST ở dòng 58, suite **`64/67`** ĐỎ
> `t51 t63 t67` — **phép thử quyết định ĐẠT** · gỡ guard `mark` · `body` · `$GITHUB_ENV`, mỗi
> cái ⇒ **`66/67`** ĐỎ `t66` (ở head trước **cả ba sống sót `63/63`**).

---

## 1. Kích thước và mỏ neo

- Head/remote: `6eaa3755abd96ef6d8f820daaa6b9d96e2bdd7b5`
- Tree: `1afa1791576e32f954fe0b33c823f50a094402fe`
- Commit: `ops: dẫn xuất vế guard theo vị trí POST`
- Worktree sạch; remote đọc ngược khớp.

`git diff --numstat cfaccff9..HEAD`:

```text
70   8  .github/workflows/ops-publish-lease.yml
105  7  ops/lease_publish.py
458  4  ops/lease_publish_test.py
```

Tổng: **3 tệp, +633/−19**, đạt trần `≤3`, `≤660`. Lượt 6 riêng: một tệp, `+101/−9`.

Provider: `openai_codex`; execution surface: Codex workspace service; transport: machine; role: executor.

## 2. Hai lượt suite và gate

Trên exact head `6eaa3755…`:

| Phép đo | Kết quả |
|---|---|
| `python3 ops/lease_publish_test.py` | `67/67`, rc=0 |
| Cùng suite với ba biến GitHub đặt và xác nhận `gh` vắng | `67/67`, rc=0 |
| `/tmp/actionlint/actionlint .github/workflows/*.yml` v1.7.7 | 5 workflow, rc=0 |
| `git diff --check cfaccff9..HEAD` | rc=0 |

## 3. Bảng đột biến

Mọi mutant chạy từ `git archive` của exact head:

| Đột biến | Kết quả | Ca đỏ |
|---|---:|---|
| M1 — thêm guard vào YAML, không đăng ký | `66/67`, rc=1 | `t64` |
| M2 — xóa `$GITHUB_ENV` khỏi sổ | `66/67`, rc=1 | `t64` |
| M3 — bộ trích trả tập rỗng | `66/67`, rc=1 | `t64` |
| **M4 — dời `check` qua sau POST, giữ nguyên tập vế** | **`64/67`, rc=1** | **`t51,t63,t67`** |
| Gỡ guard `kiem-github` | `65/67`, rc=1 | `t60,t66` |
| Gỡ guard `check` | `65/67`, rc=1 | `t51,t66` |
| Gỡ guard `packet_issue` | `66/67`, rc=1 | `t66` |
| Gỡ guard `body` | `66/67`, rc=1 | `t66` |
| Gỡ guard payload | `66/67`, rc=1 | `t66` |
| Gỡ guard `case ID` | `66/67`, rc=1 | `t66` |
| Gỡ guard `mark` | `66/67`, rc=1 | `t66` |
| Gỡ guard `$GITHUB_ENV` | `66/67`, rc=1 | `t66` |

M4 đạt phép thử quyết định: `t67` chết vì vị trí được dẫn xuất từ YAML. Đột biến đa sát: M4=3 ca; gỡ `kiem-github`=2; gỡ `check`=2. Các mutant khác giết đúng một ca.

## 4. Bảng vị trí và tập guard

Hai tập bằng nhau **8/8**:

| Dẫn xuất từ YAML | Sổ đăng ký |
|---|---|
| `python3 "$NEO/ops/lease_publish.py" kiem-github "$tep" --root .` | cùng lệnh, exact |
| `python3 "$NEO/ops/lease_publish.py" check "$tep" --root .` | cùng lệnh, exact |
| `ISSUE=$(python3 -c "…['packet_issue']…" "$tep")` | cùng lệnh, exact |
| `python3 "$NEO/ops/lease_publish.py" body "$tep" > than.md` | cùng lệnh, exact |
| `python3 -c "…json.dumps(…)…" > payload.json` | cùng lệnh, exact |
| `ID=$(gh api "repos/$REPO/issues/$ISSUE/comments" --input payload.json --jq .id)` | cùng lệnh, exact |
| `python3 "$NEO/ops/lease_publish.py" mark "$tep" --comment-id "$ID"` | cùng lệnh, exact |
| `echo "DA_DOI=1" >> "$GITHUB_ENV"` | cùng lệnh, exact |

Vế chung của cả tám ca: lease `dau` và `cuoi` đều POST đúng một lần; `BI_CHAN=1`; bước trả đúng rc=1.

| Guard | Vị trí dẫn xuất | Vế phụ thuộc vị trí | Không quan sát/không được khẳng định |
|---|---|---|---|
| `kiem-github` | Trước POST | `giua` không POST; chưa `mark` | Hậu quả ghi ngược nếu luồng được đi tiếp |
| `check` | Trước POST | như trên | như trên |
| `packet_issue` | Trước POST | như trên | như trên |
| `body` | Trước POST | như trên | như trên |
| payload | Trước POST | như trên | như trên |
| `case ID` | Sau POST | `giua` đã POST; chưa `mark` | Không thể khẳng định “không POST” |
| `mark` | Sau POST | `giua` đã POST; `mark` chưa ghi | Không thể khẳng định “không POST” |
| `$GITHUB_ENV` | Sau POST | `giua` đã POST; `mark` đã ghi; ghi env hỏng | Không thể khẳng định “không POST”; dòng env cuối là trạng thái cộng dồn, không quy thuộc riêng một lease |

Hai tập vế được khai là `VE_TRUOC_POST` và `VE_SAU_POST`; T67 tính lại vị trí bằng thứ tự lệnh thật trong YAML rồi đối chiếu với tập vế đăng ký.

## 5. `chua_do_duoc`

- Cửa sổ **“POST thành công, `mark` hỏng” KHÔNG ĐÓNG**: comment đã tồn tại nhưng `posted_comment_id` chưa được ghi. Thứ duy nhất che nó là `kiem-github` trả rc=9 ở lượt sau. **CHE, KHÔNG ĐÓNG.**
- Khe race hai nhánh `ops/**` vẫn mở nếu cả hai cùng qua `kiem-github` trước POST đầu tiên; không thêm rollback, preflight hay đổi thứ tự workflow.
- Chưa có lượt GitHub Actions thật và chưa đo Windows; các gate workflow vẫn là thân bước chạy dưới Bash tại chỗ.
- Các nhánh “một phần” trong `_doc_gh`, `_kiem_loai_so_hieu`, `_kiem_comment_da_co` vẫn ngoài phạm vi.
- `t59` vẫn chỉ quan sát `argv[0:2]`; cờ phía sau chưa được khóa.
- Nợ nền `chay(env=None)`, ruleset/branch protection và quyền đọc PR qua Issues API vẫn chưa đo/không đóng.
- Không land, merge, deploy hoặc gọi LIVE; head đã push để chuyển sang reviewer độc lập.
