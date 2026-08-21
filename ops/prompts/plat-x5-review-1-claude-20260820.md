# Prompt BẤT BIẾN — Reviewer chéo `PLAT-X5`, lượt **1**, provider `claude`

**ĐẢO VAI:** executor là `codex`, reviewer là `claude`. Vẫn cross-provider ⇒ §8 thoả.

Read-only với KHO: **không commit, không push, không đổi HEAD.**

```
./nhiem_vu.txt        prompt này
./PACKET_ISSUE_206.md đặc tả có thẩm quyền (đã revision 2)
./VERDICT_LUOT_3_X4.md verdict vòng 3 trên #203 — nguồn sinh ra packet này
./diff.patch          diff base..head (ĐÚNG phần việc của X5)
./bin/actionlint      actionlint 1.7.7 (NGOÀI cây kho)
./kho/                bản sao kho — `git worktree` tách rời tại exact head, GHI ĐƯỢC
```

Lệnh git dạng `git -C kho ...`; test chạy sau khi `cd kho`. PATH: `export PATH="$PWD/../bin:$PATH"`.
**CHỐT SẠCH CÂY:** `git -C kho status --short` RỖNG trước và sau; HEAD không đổi. Đột biến chạy
trên bản sao tạm. Không đọc ra ngoài sandbox.

## 1. Mỏ neo

| trường | giá trị |
|---|---|
| packet | `#206` · PR `#207` (xếp tầng trên PR `#205`) |
| exact head | `e071e0aa` — ĐO LẠI bằng `git -C kho rev-parse HEAD` |
| base | `a09aae627533f59e6b2e817858a6db50b999d41c` (head của `#203`) |
| write set | `ops/lease_publish_test.py` · `ops/cai_actionlint.sh` · `ops/chay_lease_publish_test.sh` · hai workflow |
| CI | lượt `32395054494` trên exact head: cả hai job `success`, **0 bước hỏng** |

## 2. Bối cảnh — vì sao packet này tồn tại

`t34` cố khẳng định *"job này có cài `actionlint` trước khi chạy bộ test không"* bằng phân tích
tĩnh trên thân `run` của YAML. **Ba vòng review trên `#203`, ba lần bị đánh bại** bằng một dạng
shell khác. Packet này đổi CÁCH LÀM: wrapper gộp cài + chạy, và **khai tên** phần không đóng được.

## 3. Trục phải soi

1. **Wrapper có thật sự làm hai việc KHÔNG TÁCH RỜI không?** Đường nào để bộ test chạy mà
   installer không chạy trước, trên cùng runner? Thử: `AL_DICH` trỏ chỗ không ghi được;
   installer trả mã lỗi giữa chừng; `PATH` đã có sẵn một `actionlint` sai bản.
2. **`exec` có thật sự giữ rc không** — mọi mã thoát, kể cả >128 và 0? Đo, đừng đọc.
3. **Mã thoát 10/11 có đúng ca không**, hay có ca nào rơi vào chúng oan?
4. **Ba nhánh python** (`python`/`python3`/`py -3`): có nhánh nào ĐƯỢC ĐẾM ĐẠT mà không đo?
   Harness này **không có cơ chế bỏ qua** — `main()` chỉ `qua += 1` khi hàm không ném, nên một
   ca `return` sớm vẫn tính ĐẠT. Đây là bệnh `t24` mà kho đã trả giá.
5. **Magic bytes:** ba chữ ký ZIP + gzip. Còn định dạng nào lọt/bị từ chối oan? `od` thiếu ⇒
   fail-close đúng chưa? Gói rỗng, gói cụt, gói 3 byte?
6. **`t40` — ca lớn nhất và mới nhất.** Nó rẽ nhánh theo nền. **Mỗi nhánh có ĐO THẬT không**,
   hay có nhánh nào thành `return` sớm? Nhánh Windows đóng gói lại `actionlint.exe` từ PATH —
   nếu PATH không có thì nó ĐỎ hay lặng lẽ qua? Đồ giả **mô phỏng TRẠNG THÁI hay diễn kịch bản**?
7. **`t34` sau khi thu hẹp:** nó còn khẳng định được gì? Executor khai `python -m` vẫn lọt —
   **xác nhận lời khai ấy**, và tìm xem còn dạng nào lọt mà executor CHƯA khai.
8. **Nợ `PLAT-X5-required-status-check`** có được ghi ở chỗ người ta sẽ đọc không, hay chỉ nằm
   trong một chú thích?

## 4. Đừng tin bảng đo của executor — chạy lại

```
cd kho && export PATH="$PWD/../bin:$PATH"
python3 ops/lease_publish_test.py            # chờ rc=0, N/N hai số BẰNG NHAU, ≥40
AL_VER=1.7.7 AL_DICH=<thư-mục-tạm> bash ops/chay_lease_publish_test.sh
actionlint .github/workflows/*.yml
python3 -W error::SyntaxWarning -c "import py_compile; py_compile.compile('ops/lease_publish_test.py', doraise=True)"
```

`rc` đọc **trực tiếp** từ tiến trình. Nối `| tail`/`| head` là **nuốt mã thoát** — lỗi này đã
xảy ra bốn lần trong đợt này, một lần làm cả bảng đo `AL_VER` báo `rc=0` sai.

## 5. Hai điều cần biết về người viết đặc tả

- Prompt này do **phiên điều phối** viết — chính phiên đã **ba lần vá hỏng cùng một chỗ** ở
  `#203`, và đã để lọt một `invalid escape sequence` mà executor phải sửa hộ trong PR này.
  **Soi phần đặc tả, không chỉ soi mã.**
- Executor `codex` **tự khai** `python -m` vẫn lọt. Một lời khai thật thà vẫn phải ĐO.

## 6. Cách trả lời

Mỗi finding: (a) **bằng chứng đo được** (lệnh + kết quả nguyên văn); (b) P1/P2/P3;
(c) **invariant bị cắt**; (d) **gợi ý vá**. Không chạy được thì ghi là **giả thuyết**.
Hướng nào đo mà sạch thì **nói rõ đã đo** — im lặng đọc giống hệt chưa ai thử.

Kết ở dòng cuối, đúng một trong ba, nguyên văn:

```
VERDICT: approved
VERDICT: changes_requested
VERDICT: blocked
```

Kèm ngay dưới dòng `Reviewed commit: BĂM_BẠN_ĐO_ĐƯỢC`.
