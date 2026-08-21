# Prompt BẤT BIẾN — Reviewer chéo `PLAT-X4`, lượt **3**, provider `codex` — SOI DELTA rev3

Read-only với KHO: **không commit, không push, không đổi HEAD.**

**Bố cục sandbox** — bạn đứng ở gốc sandbox, KHÔNG phải trong kho:

```
./nhiem_vu.txt        prompt này
./VERDICT_LUOT_2.md   verdict lượt 2 của chính bạn — NGUYÊN VĂN
./delta_rev3.patch    diff 1d37861e..a09aae62 — PHẦN PHẢI SOI KỸ (2 tệp, +100/-16)
./diff_toanbo.patch   diff base..head — bối cảnh
./numstat.txt         numstat base..head
./PROTOCOL_TRICH.md   bản sao docs/PROTOCOL_DA_PHIEN.md
./bin/actionlint      actionlint 1.7.7 (NGOÀI cây kho)
./kho/                BẢN SAO KHO — `git worktree` tách rời tại exact head, GHI ĐƯỢC
```

Lệnh git dạng `git -C kho ...`; test chạy sau khi `cd kho`. PATH: `export PATH="$PWD/../bin:$PATH"`.

**CHỐT SẠCH CÂY:** `git -C kho status --short` **RỖNG** trước và sau; HEAD không đổi. Đột biến
chạy trên bản sao tạm. **Không đọc ra ngoài sandbox.**

## 1. Mỏ neo

| trường | giá trị |
|---|---|
| packet | `#203` — `[WP PLAT-X4]` · PR `#205` |
| exact head | `a09aae62` (đo lại bằng `git -C kho rev-parse HEAD`) |
| head lượt 2 | `1d37861ec419d1c3a25cfbdb1b07689bbf42504c` |
| base | `909d3e171d7b37a734c1100b3fdc3c48e1b66d19` |
| delta phải soi | `1d37861e..a09aae62` — `ops/cai_actionlint.sh`, `ops/lease_publish_test.py` |
| vòng | **3** — trần 2 vòng đã được chủ kho NỚI, có ghi trong lease |

**Vì sao có vòng 3:** lượt 2 trả `changes_requested`; chủ kho chọn **Remediation Slice** rồi
**nới trần** để soi riêng phần vá. Trần vòng trong kế hoạch là **kỷ luật vận hành, chưa có
cưỡng chế máy** (`review_rounds_used` không nơi nào đọc để chặn; `W0-R1` từng chạy 4 vòng).
Đây KHÔNG phải lách budget bằng cách đổi tên packet — cùng packet, cùng PR, ghi thẳng là lượt 3.

## 2. Việc thứ nhất — HAI FINDING LƯỢT 2 ĐÓNG CHƯA?

Dựng lại **đúng phản chứng của bạn**, trên bản sao tạm:

1. **`t34` ràng theo TỆP.** Chuyển installer canonical sang một job khác, để job chạy bộ test
   chỉ còn `run: echo ops/cai_actionlint.sh`. Trước vá: `38/38` rc=0. Nay phải ĐỎ.
2. **`${TEN_GOI##*.}` với tên không có dấu chấm.** `AL_GOI` trỏ một tar hợp lệ tên `nodot`,
   băm đúng ⇒ trước vá rc=5. Nay phải rc=0.

## 3. Việc thứ hai — BẢN VÁ NÀY CÓ MỞ LỖ MỚI KHÔNG?

**Đọc kỹ đoạn này.** Packet này có VẾT: **hai lần liên tiếp**, executor đóng đúng lỗ bạn chỉ ra
rồi để hở một lỗ **CÙNG HỌ** ngay cạnh —

- lượt 1 → rev2: đổi **CHỖ** khớp chuỗi (caller ⇒ installer), vẫn là khớp chuỗi;
- lượt 2 → rev3: đổi **MỨC** ràng buộc (job ⇒ tệp) sau khi đã bỏ khớp chuỗi.

Nên câu hỏi đáng giá nhất ở lượt này KHÔNG phải "hai finding đóng chưa" mà là **"bản vá thứ ba
có phải là lần thứ ba không"**. Các hướng cụ thể:

1. **`_CHAY_BO_TEST` bỏ sót dạng gọi nào?** Nó là **nhận diện dương** cho chốt THỨ TỰ. Sót một
   dạng ⇒ `i_chay is None` ⇒ chốt thứ tự **im lặng bỏ qua** job đó. Thử: `python -m ...`,
   `bash -c "python ops/lease_publish_test.py"`, gọi qua biến, `exec python ...`, `uv run ...`,
   xuống dòng nối bằng `\`, đứng sau `&&`/`;`. Mỗi dạng sót là một fail-open trên trục thứ tự.
2. **Job không có bước `run` nào** (chỉ `uses:`), hoặc job **gọi reusable workflow**
   (`jobs.<id>.uses:`) mà workflow ấy chạy bộ test — `t34` có thấy không? Nếu không thấy thì
   nghĩa vụ biến mất hoàn toàn, đúng kiểu regression `32351892214` qua cửa thứ ba.
3. **Bước có `if:`** — một installer `if: false` (hoặc điều kiện không bao giờ đúng) vẫn được
   đếm là CÓ MẶT. `t34` có phân biệt không? Nếu không, nói rõ mức rủi ro.
4. **`GOI_CUC_BO` theo loại archive:** một tệp **zip** đặt tên KHÔNG có `.zip` nay rơi vào nhánh
   `tar.gz`. So với bản trước thì tốt hơn hay tệ hơn? Còn `.ZIP` viết hoa? `.tgz`?
5. **Bất đối xứng hai trục** (nghĩa vụ bấu vào NHẮC, thứ tự bấu vào CHẠY) — executor khai đây là
   cố ý và fail-closed ở trục nghĩa vụ. Kiểm: over-approximate ở trục nghĩa vụ có gây **báo
   nhầm** ở đâu không (một workflow chỉ nhắc tên tệp trong chú thích/tài liệu mà bị đòi installer)?
6. **`t36`/`t37`/`t38` còn đo không** sau khi `t34`/`t35` đổi? Chạy đột biến của chính chúng.
7. **Ca dương mới trong `t35`** (gói `goikhongduoi`) có thật sự đo không, hay nó xanh vì lý do khác?

Hướng nào bạn ĐO mà thấy sạch thì **nói rõ đã đo** — im lặng đọc giống hệt chưa ai thử.

## 4. Bằng chứng nền

- `ops/lease_publish_test.py` ⇒ rc=0, `N/N` hai số BẰNG NHAU, không tụt dưới 38.
- `actionlint .github/workflows/*.yml` ⇒ rc=0 cả 5.
- `git -C kho diff --name-only 909d3e17..HEAD` ⇒ **đúng 4 tệp** write set.
- Windows: lượt `32378036279` trên `a09aae62` — `gate (windows-latest)` **success**.
  Nhắc: `get_job_logs` chỉ trả phần ĐUÔI log nên **không đọc được `N/N` của Windows**; đừng khai
  là đã đọc nếu bạn không đọc được.

`rc` đọc **trực tiếp** từ tiến trình. Nối `| tail`/`| head` là **nuốt mã thoát** — lỗi này đã
xảy ra ba lần trong đợt này, một lần làm cả bảng đo `AL_VER` báo `rc=0` sai.

## 5. Cách trả lời

Mỗi finding: (a) **bằng chứng đo được** (lệnh + kết quả nguyên văn); (b) P1/P2/P3;
(c) **invariant bị cắt**; (d) **gợi ý vá**. Không chạy được thì ghi là **giả thuyết**.

Kết ở dòng cuối, đúng một trong ba, nguyên văn:

```
VERDICT: approved
VERDICT: changes_requested
VERDICT: blocked
```

Kèm ngay dưới dòng `Reviewed commit: BĂM_BẠN_ĐO_ĐƯỢC`.
