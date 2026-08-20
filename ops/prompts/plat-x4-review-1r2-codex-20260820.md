# Prompt BẤT BIẾN — Reviewer chéo `PLAT-X4`, lượt **1** (bản sửa r2), provider `codex`

Read-only với KHO: **không commit, không push, không đổi HEAD.**

**Bố cục sandbox** — bạn đang đứng ở thư mục gốc sandbox, KHÔNG phải trong kho:

```
./nhiem_vu.txt        prompt này
./EVIDENCE.md         số đo cổng của executor (đã đo lại độc lập)
./diff.patch          diff base..head
./numstat.txt         numstat base..head
./PROTOCOL_TRICH.md   bản sao docs/PROTOCOL_DA_PHIEN.md
./kho/                BẢN SAO KHO — `git worktree` tách rời tại exact head, GHI ĐƯỢC
```

Bản sao kho **ghi được** là cố ý: bạn tự chạy phản chứng và đột biến trong đó mà không
chạm kho thật. Mọi lệnh git chạy dạng `git -C kho ...`, mọi lệnh test chạy sau khi `cd kho`.

**CHỐT SẠCH CÂY:** `git -C kho status --short` phải **RỖNG** cả trước lẫn sau lượt, và
`git -C kho rev-parse HEAD` không đổi. Năm tệp artefact trên nằm NGOÀI `kho/` đúng để chốt
này đo được — lượt trước chúng nằm TRONG cây và làm preflight đỏ ngay từ đầu; đó là lỗi
của người dựng sandbox, đã sửa.

**Không đọc ra ngoài thư mục sandbox này.** Một lượt chạy phạm vi mở đã quét ra ngoài kho,
đọc nhầm transcript phiên, 40 phút không ra kết luận.

## 1. Mỏ neo

| trường | giá trị |
|---|---|
| packet | `#203` — `[WP PLAT-X4]` |
| PR | `#205` |
| exact head phải review | `d0acd79f8bf22acf12d226283f176f2e7cc81508` — **ĐO LẠI, xem §1b** |
| base | `909d3e171d7b37a734c1100b3fdc3c48e1b66d19` |
| write set khai báo | `ops/lease_publish_test.py` · `.github/workflows/ops-publish-lease.yml` · `.github/workflows/ci.yml` · `ops/cai_actionlint.sh` |
| review class | `sensitive` · vòng **1/2** |

### 1b. ĐỌC KỸ — mỏ neo trên có thể SAI

Chuỗi head ở bảng trên do người soạn prompt gõ, **không phải chép máy**. Việc ĐẦU TIÊN của
bạn: chạy `git -C kho rev-parse HEAD` và dùng **con số đó**. Nếu nó khác bảng trên, ghi cả hai vào
verdict và tiếp tục với con số đo được — rồi nêu chính chỗ lệch ấy như một finding về quy
trình. Kho này có bài học nguyên văn: *"thứ định danh tệp là BĂM, không phải tên nhánh"*, và
một con băm gõ tay cũng hỏng theo đúng kiểu đó.

## 2. Packet này làm gì

Đóng 2 finding P2 của cross-review `#200`. Đây là **lần thứ ba** cùng một hình dạng lỗi:
kiểm sự CÓ MẶT của chuỗi rồi tuyên là đã đo HÀNH VI. `CLAUDE.md` đòi bàn về **CÁCH LÀM**
chứ không phải một mẫu chuỗi chặt hơn — nên bản vá chuyển hành vi "cài + đối chiếu bản
ghim" vào **một script chạy được** (`ops/cai_actionlint.sh`), và `t35` **chạy thật** script
ấy với `actionlint` giả rồi đòi nó TỪ CHỐI.

## 3. Trục phải soi — đây là cổng CẤP QUYỀN GHI

`ops-publish-lease.yml` chạy bằng `GITHUB_TOKEN` với `contents: write` + `issues: write`:
**push được thành đăng được**. Bộ test này là thứ đứng giữa một tệp YAML và một comment
mang danh nghĩa kho.

1. **Bản vá có thật sự đóng P2-1 không?** Finding gốc: `t34` đoán "dòng nào là người gọi"
   bằng khớp **chuỗi con trên cả dòng**, nên `echo preparing; python ops/lease_publish_test.py`
   lọt khỏi tập người gọi ⇒ gỡ hẳn bước cài actionlint mà suite vẫn `35/35`. **Fail-open.**
   Tự dựng caller ở các dạng lạ (`&&`, `|`, biến, heredoc, `$(...)`, `xargs`, nhiều dòng nối
   bằng `\`, `bash -c "..."`) rồi gỡ công cụ — `t34` phải ĐỎ mọi dạng. Tìm dạng nó vẫn mù.
2. **P2-2 có bị vá bằng một mẫu chuỗi chặt hơn không?** Đó là điều packet tuyên bố KHÔNG
   làm. Đọc `t35`: nó **chạy** script hay vẫn **đọc** script? Nếu còn bất kỳ phép khớp chuỗi
   nào quyết định đạt/hỏng, nêu rõ.
3. **`t35` có ĐƯỜNG THUẬN không?** Một cổng "luôn từ chối" cũng qua được mọi phản chứng
   phủ định. Phải có ca bản ĐÚNG ⇒ NHẬN. Thiếu ⇒ P2.
4. **Mã thoát 2..7 có phân biệt thật không?** Executor khai từng mã cho từng lý do. Đo
   từng cái. Hai lý do khác nhau trả cùng mã ⇒ người gọi không khẳng định được gì.
5. **Không có nhánh thoát sớm theo `PATH`?** *Có mặt ≠ đúng bản.* Nếu `actionlint` đã có
   sẵn mà script bỏ qua đối chiếu ⇒ P1.
6. **Chốt GIỮ TẦNG có răng?** Workflow cài inline trở lại phải ĐỎ. Thử thật.
7. **`t33` fail-close.** Thiếu `actionlint` phải ĐỎ, không được bỏ qua êm. Một cổng tự tắt
   khi thiếu công cụ là cổng không tồn tại đúng lúc nó cần nhất.
8. **YAML còn hợp lệ với GITHUB không?** PyYAML **không biết luật GitHub**. Sáu lượt
   cross-review từng cùng kết luận "YAML ok" và đều sai. Chạy `actionlint` thật trên cả 5
   workflow. Nhớ: `${{ }}` trong **chú thích** của `run` cũng làm hỏng cả tệp.
9. **Script tải về từ mạng** — có ghim phiên bản không, có đối chiếu sau khi cài không, có
   kiểm băm gói không (executor tự khai là **không** kiểm băm: xác nhận lời khai ấy đúng và
   nêu mức rủi ro). `AL_GOI` nhận đường dẫn gói tuỳ ý: nó có giải nén ra ngoài thư mục đích
   được không (`../` trong tar)? Thử.

## 4. Đừng tin bảng đột biến của executor

Executor khai đột biến chạy trên **bản sao tạm**. Kiểm lời khai ấy: có đường nào ghi vào
cây thật không? Kho đã trả giá — một bản vá NGƯỢC từng đi thẳng vào commit vì đột biến ghi
vào tệp thật rồi khôi phục trong `finally`, mà `finally` không chạy khi bị cắt giữa chừng.

Và: **đồ giả phải mô phỏng TRẠNG THÁI, không diễn kịch bản.** `actionlint` giả ở đây có
diễn kịch bản không? Một bộ test từng cho `40/40` trong khi đột biến **xoá hẳn** lệnh phá
vẫn qua, vì đồ giả trả lời theo kịch bản thay vì theo trạng thái.

```
python3 ops/lease_publish_test.py     # chờ rc=0 và N/N hai số BẰNG NHAU
actionlint .github/workflows/*.yml
AL_VER=1.7.7 bash ops/cai_actionlint.sh   # rc=0, rồi actionlint --version phải khớp
```

`rc` phải đọc **trực tiếp** từ tiến trình. Nối `| tail` sau lệnh là **nuốt mã thoát** —
lỗi này đã xảy ra thật trong chính đợt chuẩn bị packet này.

## 5. Lời khai nền cần kiểm

`doc-claims-check --strict` rc=2 — executor khai **ĐỎ SẴN** trên master sạch `909d3e1`,
delta = 0. Đo lại trên nền trước khi nghi bản vá.

## 6. Cách trả lời

Mỗi finding bắt buộc bốn phần: (a) **bằng chứng đo được** (lệnh + kết quả nguyên văn);
(b) mức P1/P2/P3; (c) **invariant nào bị cắt**; (d) **gợi ý vá** cụ thể. Không chạy được
thì ghi thẳng là **giả thuyết**, đừng trình bày như phép đo.

Kết ở dòng cuối, đúng một trong ba, viết nguyên văn:

```
VERDICT: approved
VERDICT: changes_requested
VERDICT: blocked
```

Kèm ngay dưới dòng `Reviewed commit: <băm bạn ĐO ĐƯỢC bằng git -C kho rev-parse HEAD>`.
