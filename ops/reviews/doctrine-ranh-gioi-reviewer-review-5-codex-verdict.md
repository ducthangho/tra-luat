# Cross-review vòng 5 — packet #318 `DOCTRINE-RANH-GIOI-REVIEWER`

verdict: changes_requested
reviewed_sha: 770b3af3399b6794874008dd907f1dfaad6c5dba
reviewed_tree: 021b89a36a751e83eb22680f6e6024c73a2917ed
base_sha: c35ae1c0a1104dbd6e65a321cda3b9f9441a408b
provider: openai_codex
execution_surface: codex_service
transport: machine
executor: claude
independent_from_executor_session: true
review_axes: [spec, standards_security]

## Kết luận

Yêu cầu thay đổi. N1 và N3–N7b đạt, nhưng N2 chưa đạt. Giữ đủ năm hạng là đúng:
đây là taxonomy của bằng chứng, không phải checklist buộc mỗi mục phải sinh ít nhất một instance
ở từng hạng. Vì vậy `chiều ĐÓNG = 0` thực sự là một kết luận có nghĩa đối với luận điểm
“không tầng nào bó được quyền ghi vào kho”; thu bảng về ba hạng chỉ vì hai hạng chưa được dùng sẽ
lẫn **tập loại có thể có** với **các instance đang có**.

Khuyết tật nằm ở chỗ khác: lát cắt xóa câu từng gắn nhãn đầy đủ `chiều MỞ` cho claim hệ tệp
`workspace-write`, nhưng giữ lại chính hàng quan sát ấy tại dòng 654. Do đó phép đếm literal
`MỞ=2/ĐÓNG=0/quan sát=0/máy phát hiện=1/chưa xếp=1` là đúng về chuỗi mà vẫn bỏ sót một mệnh đề
không nhãn. Finding `nam-hang-khong-tao-phan-hoach` được phán quyết **VÁ SINH LỖI MỚI**.

Hai P2 vòng 4 về probe mạng và đối chứng execution surface đã thật sự rời tệp và không được chấm
ở packet này. Chúng chưa được tuyên bố “đã vá”; chúng đi cùng phần bị tách sang #334.

## ĐỐI CHIẾU LƯỢT TRƯỚC

### Đối chiếu `nam-hang-khong-tao-phan-hoach` — **VÁ SINH LỖI MỚI**

Hai chỗ vòng 4 nêu trong phần bị cắt đã biến mất: tiêu đề nhãn rút gọn và ô pha B. Chỗ thứ ba đã
được sửa thật: dòng 605 không còn nói “đúng một ví dụ”, mà chỉ ra rõ hai hàng `--allowedTools`
cho hai cấu hình. Tuy nhiên lát cắt đồng thời xóa nhãn của một claim khác trong cùng phân hoạch:

- `docs/GOI_AGENT_DA_NEN.md:654` vẫn ghi `codex -s workspace-write` đã ghi được ngoài cây, nhưng
  không mang một trong năm nhãn;
- ở head vòng 4, dòng 686–688 gắn claim ấy với `cơ chế đã xác minh — chiều MỞ`; chính đoạn này bị
  xóa ở vòng 5;
- dòng 606 vẫn cam kết “Mọi mệnh đề sau đây mang đúng một nhãn”.

Phép đo tái lập:

```text
$ sed -n '654p' docs/GOI_AGENT_DA_NEN.md
| `codex -s workspace-write` | ghi tệp **ngoài** cây | **`rc=0`** — tệp ngoài cây bị ghi đè thật |

$ sed -n '654p' docs/GOI_AGENT_DA_NEN.md | rg -q -F 'cơ chế đã xác minh — chiều MỞ'
rc=1

$ git diff --unified=1 6d0a183e4af6422d85af1d6d3373fcbab2c7e83e..770b3af3399b6794874008dd907f1dfaad6c5dba -- docs/GOI_AGENT_DA_NEN.md | rg -n -C2 -F 'Hệ tệp: chỉ `read-only` bó'
... dòng gắn `workspace-write` với `cơ chế đã xác minh — chiều MỞ` mang dấu xóa ...
```

### Hai P2 vòng 4 — **ĐÃ RỜI PHẠM VI, KHÔNG CHẤM Ở #318**

`probe-nuot-loi-thanh-chan-mang` và `doi-chung-vo-phien-phu-thuoc-be-mat` không còn hiện vật hay
phần văn bản mà chúng nhắm tới:

```text
$ rg -n -F -e '#### Trong sandbox codex thì khác hẳn' -e '#### Hệ quả vận hành: hai pha' -e '.claude/dev/probe_mang.py' -e 'đối chứng: vỏ phiên' docs/GOI_AGENT_DA_NEN.md
rc=1, không có hit

$ git cat-file -e 770b3af3399b6794874008dd907f1dfaad6c5dba:.claude/dev/probe_mang.py
rc=128, path không tồn tại ở reviewed tree
```

Đây là xác nhận phạm vi của lát cắt, không phải phán quyết rằng hai lỗi nội dung đã được chữa.

## SOÁT LÁT CẮT

- **Đúng 70 dòng:** ở `6d0a183`, hai mục bắt đầu tại dòng 648 và phần kế tiếp bắt đầu tại dòng
  718; phép đếm `718 - 648` cho `70`. Diff tài liệu riêng của vòng 5 là `26/80`, tức net `-54`
  vì ngoài phần xóa còn 26 dòng nối/sửa.
- **Không còn con trỏ chết tới mục bị cắt:** `mục kế` không còn. Các lần `mục dưới` tại dòng
  592, 600 và 605 trỏ được tới mục “Bốn tầng” bắt đầu ở dòng 633; `xem cuối mục dưới` tại dòng
  595 trỏ được tới đoạn tách packet ở dòng 640–645.
- **Mục “Bốn tầng” vẫn tự đứng được về phạm vi:** dòng 633–638 khóa vào vỏ phiên điều phối và
  quyền ghi vào kho; bảng và phần kết luận proxy vẫn còn. Vết thương của nó là nhãn bị mồ côi ở
  dòng 654, không phải phụ thuộc vào mục kế đã bị xóa.
- **Câu doctrine về mặc định cấu hình không phải claim số mới:** dòng 640–645 giữ quan hệ tổng
  quát “mặc định cấu hình không phải bất biến” và nói thẳng số đo/probe đã chuyển packet. Cơ chế
  cấu hình vẫn có neo nội-tệp tại dòng 328–345 (`network_access=true`, kết quả sau khi mở cờ), nên
  không mở lại hai P2 mạng ở đây.
- **Một mô tả số lượng còn sai:** dòng 638 nói “Hai hàng `codex` trong bảng”, nhưng vùng bảng
  dòng 650–656 chỉ có đúng một hàng bắt đầu bằng `codex`. Finding P2 ở dưới.

## BẢNG CHẤM N1–N6, N7a, N7b

| tiêu chí | kết quả | lệnh, mã thoát và bằng chứng dương |
|---|---|---|
| N1 | **ĐẠT** | `nl -ba docs/GOI_AGENT_DA_NEN.md \| sed -n '633,639p'` (`rc=0`): tiêu đề và câu đầu cùng giới hạn **vỏ phiên điều phối**, đối tượng là **quyền ghi vào kho**. |
| N2 | **KHÔNG ĐẠT** | `sed -n '633,663p' ...` cho các nhãn được dùng `MỞ=2`, `ĐÓNG=0`, `quan sát=0`, `máy phát hiện=1`, `CHƯA XẾP=1`, nhưng dòng 654 là một claim-condition không nhãn; phép `rg -q` nhãn đầy đủ trên chính dòng ấy trả `rc=1`. Giữ năm hạng là đúng, áp dụng chưa phủ hết. |
| N3 | **ĐẠT** | `nl -ba ... \| sed -n '564,577p;640,663p'` (`rc=0`): bảng ba lượt tự khai không tái lập được; bảng còn lại ghi điều kiện cụ thể và không dựa vào bảng/probe mạng đã cắt. |
| N4 | **ĐẠT** | `nl -ba ... \| sed -n '328,345p;633,656p'` (`rc=0`): config `workspace-write`, cờ mạng, surface vỏ phiên, ngày đo và phép đo nằm cạnh các quan sát còn được dùng. Đoạn dòng 640–645 chỉ giữ doctrine và chuyển chi tiết, không giả làm bảng đo mới. |
| N5 | **ĐẠT** | Sáu lệnh `rg -n -F` đều `rc=0`: ví dụ thứ sáu `bash /tmp/refscan.sh` tại `:553`; `stdout.log` không tracked tại `:570–572`; `tương quan có neo` tại `:574–577`; ba hàng `78/5/10,8 M`, `85/10/12,8 M`, `45/1/3,7 M` tại `:566–568`. `git diff -U0 6d0a183..770b3af -- ... \| rg` sáu neo trả `rc=1`, tức lát cắt không đổi chúng. |
| N6 | **ĐẠT** | `git diff --name-only c35ae1c0a1104dbd6e65a321cda3b9f9441a408b` (`rc=0`) in đúng `docs/GOI_AGENT_DA_NEN.md`; `git diff --check ...` `rc=0`. |
| N7a | **ĐẠT** | `python3 .claude/dev/packet_loop.py doctrine-scan --root . --path docs/GOI_AGENT_DA_NEN.md` → `rc=0`, `doctrine-scan: sạch — đã quét 8 tệp, 0 chỗ chép doctrine`. |
| N7b | **ĐẠT** | `git diff --numstat c35ae1c0a1104dbd6e65a321cda3b9f9441a408b -- docs/GOI_AGENT_DA_NEN.md` → `rc=0`, `144  0`; `144 <= 200`. Lời khai `198/200 → 144/200` khớp. |

## Phép thử bổ sung và đột biến

Tất cả chạy trong clone detached exact SHA, `core.abbrev=7`, không mạng:

| phép thử | kết quả |
|---|---|
| `python3 .claude/dev/packet_loop_test.py` | `rc=0`; nền `257/257`, `66` đột biến, `78` lớp lách, `0` ngoại lệ AC18, `TỔNG: ĐẠT`. |
| `python3 scripts/tl.py doc-claims-check --strict` rồi lọc JSON | `rc=0`; `ok=True`, `files=105`, `flags=0`, `advisories=359`. |
| Mutant thay nhãn đầy đủ của hàng `Bash` trần bằng nhãn rút gọn `MỞ`, rồi chạy N7a | `rc=0`, vẫn quét 8 tệp/0 chỗ. Mutant đã được hoàn nguyên byte-exact; clone sạch. Phép này xác nhận `doctrine-scan` không có răng cho lớp phân hoạch ngữ nghĩa, nên `rc=0` của N7a không bác finding N2. |

## FINDINGS CÒN MỞ / MỚI

### `nam-hang-khong-tao-phan-hoach` [P1] — lát cắt làm mồ côi nhãn của claim hệ tệp

- **Tệp/dòng:** `docs/GOI_AGENT_DA_NEN.md:606`, `:654`; đối chiếu phần bị xóa từ
  `6d0a183:686–688`.
- **Vấn đề:** taxonomy năm hạng hợp lý, nhưng cam kết “mọi mệnh đề sau đây mang đúng một nhãn”
  sai tại claim `workspace-write`. Con số “mục dùng ba hạng” đếm nhãn có mặt, không audit claim
  không nhãn, nên nó không chứng minh phân hoạch.
- **Phép đo tái lập:** hai lệnh `sed/rg` trong mục đối chiếu cho dòng 654 và `rc=1`; diff vòng 5
  cho thấy nhãn đầy đủ tương ứng bị xóa. Mutant nhãn rút gọn vẫn qua `doctrine-scan rc=0`.
- **Gợi ý vá — ở đâu:** sửa hàng `workspace-write` trong bảng tại dòng 654, vì claim còn sống ở
  đây; không kéo mục mạng hoặc bảng hai pha từ #334 trở lại.
- **Gợi ý vá — thế nào:** đường rẻ nhất là gắn đúng một nhãn đầy đủ cho claim kèm đúng điều kiện
  đã đo, dự kiến `cơ chế đã xác minh — chiều MỞ`. Nếu claim thật sự không còn thuộc phạm vi, xóa
  cả hàng và cập nhật số tầng thay vì giữ quan sát trần.
- **Ca test khóa:** ở rereview, dòng claim phải khớp đúng một nhãn canonical; mutant bỏ `chiều`
  hoặc thay bằng `MỞ` rút gọn phải đỏ. Nếu muốn khóa bằng gate tracked, cần revision write set
  thay vì sửa `packet_loop` ngoài phạm vi hiện tại.
- **Rủi ro bản vá có thể đẻ:** gắn nhãn mà không giữ điều kiện `codex -s workspace-write` sẽ nâng
  một quan sát surface cụ thể thành claim phổ quát; xóa hàng thì có thể làm tiêu đề “Bốn tầng” sai
  số nếu không đếm lại.

### `hai-hang-codex-chi-con-mot` [P2] — mô tả số lượng không khớp bảng

- **Tệp/dòng:** `docs/GOI_AGENT_DA_NEN.md:638`, bảng `:650–656`.
- **Vấn đề:** prose nói “Hai hàng `codex`”, bảng chỉ có một. Câu này đã sai ở head vòng 4 và lát
  cắt không sửa; hiện nó còn dễ làm người đọc đi tìm một đối chứng đã bị chuyển sang #334.
- **Phép đo tái lập:**

  ```text
  $ sed -n '650,656p' docs/GOI_AGENT_DA_NEN.md | rg -c '^\| `codex'
  1
  $ sed -n '638p' docs/GOI_AGENT_DA_NEN.md | rg -o 'Hai hàng `codex`'
  Hai hàng `codex`
  ```
- **Gợi ý vá — ở đâu:** sửa câu dòng 638, không thêm lại hàng từ phần đã tách.
- **Gợi ý vá — thế nào:** đổi về số ít và mô tả đúng vai trò của hàng còn lại. Nếu tác giả thật sự
  định nói hai điều kiện, phải gọi tên chúng thay vì đếm “hàng”.
- **Ca test khóa:** đếm data-row trong đúng bảng và đối chiếu với numeral của prose; mutant đổi
  `một` thành `hai` phải đỏ.
- **Rủi ro bản vá có thể đẻ:** đổi máy móc về số ít có thể che một hàng bị cắt nhầm; trước khi sửa
  phải chốt chủ ý là không mang hàng đối chứng của #334 trở lại packet này.

## CHỖ KHÔNG ĐO ĐƯỢC

1. **GitHub PR/head/CI và trạng thái Issue #334:** `KHÔNG_ĐO_ĐƯỢC` vì mạng bị cấm và không fetch.
   Tôi chỉ xác minh object/ref local chứa exact SHA, lease local revision 4/generation 1 trỏ đúng
   SHA, và nội dung đã rời reviewed tree. Không thể xác minh 70 dòng đã được lưu đầy đủ trong body
   Issue #334 từ sandbox này.
2. **Ba `stdout.log` và các số `78/5/10,8 M · 85/10/12,8 M · 45/1/3,7 M`:**
   `KHÔNG_ĐO_ĐƯỢC` vì scratchpad không được git theo dõi. Lượt này chỉ xác nhận chữ và số giữ nguyên.
3. **CI/check remote trên exact SHA:** `KHÔNG_ĐO_ĐƯỢC`; không coi việc thiếu evidence remote là pass.
4. **Execution surface cũ của hai P2 vòng 4:** `KHÔNG_ĐO_ĐƯỢC` và ngoài phạm vi sau quyết định tách;
   không chạy lại probe đã bị xóa, không dùng sự vắng mặt của probe để tuyên bố hai P2 đã được chữa.

## Đếm finding

- P1: **1**
- P2: **1**

Đường dẫn verdict: `ops/reviews/doctrine-ranh-gioi-reviewer-review-5-codex-verdict.md`
