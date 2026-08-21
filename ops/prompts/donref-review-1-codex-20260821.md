# Prompt BẤT BIẾN — Reviewer chéo PR "#213" (`ops-don-ref`), lượt **1**, provider `codex`

**Executor là `claude`, reviewer là `codex`** ⇒ cross-provider, §8 thoả.

Read-only với KHO: **không commit, không push, không đổi HEAD.** Đột biến chạy trên **BẢN SAO
TẠM** dựng bằng `git -C kho archive <sha> | tar -x` (thuần đọc). Đã có tiền lệ trả giá: một lượt
review trước lỡ dùng `git --work-tree=… checkout -- .` và ghi vào INDEX của worktree.

```
./nhiem_vu.txt      prompt này
./diff.patch        master..cbc57214 — 3 tệp
./bin/actionlint    actionlint 1.7.7 (NGOÀI cây kho)
./kho/              bản sao kho tại exact head, GHI ĐƯỢC
```

Lệnh git dạng `git -C kho ...`. PATH: `export PATH="$PWD/bin:$PATH"`.

## 1. Mỏ neo

| trường | giá trị |
|---|---|
| PR | `#213` |
| exact head | `cbc57214be1f33b93c5d04e4363c2bcce87439b6` — ĐO LẠI bằng `git -C kho rev-parse HEAD` |
| base | `master` |
| write set | `.github/workflows/ops-don-ref.yml` · `ops/don_ref_chot_test.sh` · `CLAUDE.md` |

## 2. Thay đổi này làm gì

`ops-don-ref.yml` là workflow **cấp lại đúng quyền mà sandbox cố ý không cho** (xoá ref, ghi tag).
Nó chỉ chạy khi có người bấm `workflow_dispatch`, nên **lượt phát hiện đầu tiên nếu chốt hỏng
chính là lượt xoá nhầm**.

Trước: `ops/* claude/* codex/* agent/* mission/* dispatcher/*` bị **CẤM XOÁ TUYỆT ĐỐI**.
Sau: xoá **NHÁNH** trong các vùng ấy được phép **khi và chỉ khi** `behind_by = 0` so với nhánh
mặc định — tức mọi commit của nhánh đã nằm trong nhánh mặc định. Xoá **TAG** mang tên các vùng ấy
**vẫn cấm**. Kèm chốt **GHIM**: bước chốt ghi SHA đã đo ra tệp, bước làm đọc lại đầu nhánh và đòi
đúng SHA ấy trước khi gọi `DELETE`.

## 3. Trục phải soi — theo rủi ro GIẢM DẦN

### 3.1 Có đường nào XOÁ ĐƯỢC một nhánh còn commit chưa vào nhánh mặc định không?

Đây là câu hỏi duy nhất thật sự quan trọng. Mọi thứ khác là phụ. Hướng gợi ý, **đừng dừng ở đây**:

- `behind_by` có đúng là thứ cần đo không? Đổi vai `base`/`head` trong `compare` thì sao?
  Nhánh **giống hệt** nhánh mặc định · nhánh **đi trước** · **diverged** · nhánh **rỗng**?
- `compare` trả gì khi hai commit **không có tổ tiên chung** (lịch sử rời)? `behind_by` khi ấy
  có thể bằng 0 không? Đây là hướng tôi nghi nhất và **chưa tự đo được**.
- Giới hạn 250 commit của `compare`: `ahead_by`/`behind_by` có còn đúng khi diff vượt ngưỡng?
- Đọc bằng `--jq .behind_by`: nếu API trả **lỗi có thân JSON** thì `--jq` cho ra gì? `null`?
  rỗng? Chuỗi có xuống dòng? Có giá trị nào lọt qua `grep -Eq '^[0-9]+$'` mà không phải phép đo?
- `MAC_DINH` lấy từ `gh api ... --jq .default_branch`. Nếu nó rỗng/rác thì `compare/$sha...`
  thành gì?
- Tên nhánh có ký tự lạ đã bị chặn ở trên — **kiểm lại** chốt ấy còn chặn đủ sau thay đổi này
  không, và `tr '[:upper:]' '[:lower:]'` có làm hai nhánh KHÁC NHAU trông giống nhau không.

### 3.2 Chốt GHIM có đóng được khe đo↔xoá không

Bước chốt và bước làm là **hai bước khác nhau**, chia sẻ đĩa runner. `NEO_TEP` mặc định
`${RUNNER_TEMP:-/tmp}/don_ref_neo.txt`.

- Nhiều ref trong một lượt: ghim của ref này có lẫn sang ref kia không? Tên ref có khoảng trắng
  đã bị chặn — nhưng `awk -v k="$r" '$1==k'` có ca nào sai không?
- Tệp ghim **không bị xoá** giữa hai lượt chạy nếu `RUNNER_TEMP` được dùng lại: bước chốt có
  `: > "$NEO_TEP"` — đủ chưa? Lượt TRƯỚC để lại ghim cũ thì sao?
- Bước làm đọc lại SHA bằng `--jq .object.sha`. Nếu lời gọi ấy **hỏng**, nó ĐỎ hay lọt?
- `chi_thu = true` (thử khô) có bỏ qua chốt ghim không, và như vậy có đúng không?

### 3.3 Bộ phản chứng có RĂNG hay chỉ CÓ MẶT

`ops/don_ref_chot_test.sh` — 102 ca. Executor khai sáu đột biến, mỗi con giết đúng ca của nó:
`M1` bỏ chặn `behind != 0` · `M2` bỏ kiểm dạng số · `M3` bỏ kiểm SHA40 · `M4` bỏ cấm xoá TAG
vùng · `M5` bỏ ghi ghim · `M6` bỏ đòi ghim ở bước làm. **XÁC NHẬN, đừng tin** — rồi tự nghĩ
đột biến mới, nhất là cho phần **3.1**.

Executor cũng khai một chuyện đáng soi: `M2` **lúc đầu sống sót** vì `[ "$sau_lung" != 0 ]` tự nó
từ chối mọi thứ không phải `"0"`, nên gỡ phép kiểm dạng số **không đổi quyết định**, chỉ đổi lý
do; phải thêm phép đo **thông điệp** (`doi_ra`) mới giết được. **Kiểm lập luận ấy đúng không** —
và hỏi tiếp: còn chốt nào khác trong tệp cũng chỉ khoá được bằng thông điệp mà chưa ai khoá?

Harness `qua += 1` khi hàm không ném ⇒ ca `return` sớm vẫn tính ĐẠT. Có ca nào CÓ MẶT mà KHÔNG ĐO?

### 3.4 Bộ test có trung thực với YAML không

Nó **trích thân bước từ chính tệp YAML** (không chép lại). Nhận diện bước bằng biến môi trường,
không bằng chỉ số. **Kiểm cơ chế trích ấy** — chèn một bước mới vào workflow thì nó còn trích
đúng không, hay lặng lẽ trích nhầm và mọi ca vẫn xanh?

`gh` giả: nó **mô phỏng TRẠNG THÁI hay diễn KỊCH BẢN**? Kho này đã trả giá đúng chỗ đó — một
bản `gh` giả diễn kịch bản từng cho 40/40 trong khi đột biến **xoá hẳn** lệnh `DELETE` vẫn qua.

### 3.5 `CLAUDE.md`

Đoạn mô tả hợp đồng đã được sửa. **Câu mới có đúng bằng thứ mã làm không?** Kho này có bài học
riêng về việc câu chữ mô tả một artefact bị sai ở một phía của lần merge.

## 4. NGOÀI phạm vi

- Chuyện proxy chặn xoá ref của phiên web — đã đo và đã ghi, không phải việc của PR này.
- 65 nhánh `ops/**` còn commit chưa vào master — việc rà riêng.
- Lỗ đã khai của chốt proxy (`git push --force` vẫn được phép) — có sẵn, không do PR này.

## 5. Điều kiện DỪNG

- Cần sửa mã để chứng minh luận điểm ⇒ dựng **bản sao tạm**, KHÔNG sửa cây kho.
- Thấy một tiêu chí ở mục 3 là **sai** ⇒ DỪNG và nói ra, đừng tự đổi giữa đường.
- Phát hiện thứ đòi sửa tệp ngoài write set ⇒ finding + đề xuất, KHÔNG tự mở rộng.

## 6. Định dạng trả về

**IN RA STDOUT.** Verdict ghi vào tệp trong sandbox thì có lượt đã mất trắng vì sandbox bị xoá.

Kết thúc bằng **đúng hai dòng cuối**, không có gì sau chúng:

```
VERDICT: <approve|changes_requested|do_not_land>
Reviewed commit: <sha 40 ký tự đã ĐO bằng git -C kho rev-parse HEAD>
```

Trước đó: finding (mức P1/P2/P3, **bằng chứng đo được**, invariant bị cắt, gợi ý vá) · mục
**"đã đo và sạch"** · mục **"chưa đo được — GIẢ THUYẾT"**.

**Một điều phải biết:** người viết bản vá này cũng là người viết prompt này. Danh sách hướng ở
mục 3 là **thứ tôi đã nghĩ tới** — nên nó vừa là gợi ý vừa là **điểm mù**: hướng nguy hiểm nhất
thường là hướng không có trong danh sách. Workflow này cấp lại quyền phá, nên `approve` nghĩa là
bạn đã tìm và **không thấy** đường xoá được một nhánh chưa an toàn.
