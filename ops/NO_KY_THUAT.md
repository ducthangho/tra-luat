# NỢ KỸ THUẬT — tách khỏi PR #141, xử ở phiên riêng

Tệp này là **sổ nợ**, không phải kế hoạch. Mỗi mục ghi: đo được gì, vì sao CHƯA
làm trong #141, và điều kiện để coi là xong. Nguồn có thẩm quyền vẫn là lịch sử
git và comment trên PR.

Nguyên tắc chung, áp cho cả sổ này: **cùng một hình dạng lỗi lặp ba lần trở lên
thì câu hỏi đúng là *có nên làm việc này không*.** Lớp cách ly tiến trình đã qua
bốn vòng vá cùng hình dạng rồi mới đổi sang cgroup — đừng mở vòng thứ năm chỉ vì
một mục dưới đây trông dễ.

---

## 1. Kẻ CỐ TÌNH trèo ra khỏi cgroup — chưa chặn, chưa phát hiện

**Đo được** (PR #141, head `f2bf701`, cross-review bot):

```
pid trong cgroup RIENG cua luot  : []
pid trong cgroup CHA (tl-gate-ci): [25726]
_giet_cgroup(luot) khai          : True      <- khai da don sach
tien trinh gate con song?        : True      <- ma no VAN SONG
```

Tiến trình tự ghi PID của mình vào `cgroup.procs` của cgroup cha là trèo ra khỏi
cgroup của lượt.

**Vì sao không vá phòng ngừa:** luật delegation containment của cgroup v2 đòi ghi
được `cgroup.procs` của TỔ TIÊN CHUNG để chuyển tiến trình *vào* — mà đúng quyền
ấy cho phép trèo *ra* một tầng. Lồng thêm tầng vô ích: trèo được tới đúng chỗ
mình có quyền ghi. Chặn thật cần **helper đặc quyền** làm việc chuyển, hoặc
**cgroup namespace** — cả hai bắt gate phải có root ở mọi nơi nó chạy, kể cả máy
người dùng.

**Vì sao bản PHÁT HIỆN cũng bị hoãn:** đã viết thử (nhớ ai từng ở trong cgroup
rồi kiểm lại từng đứa bằng khoá danh tính) và **đo thấy sai CẢ HAI CHIỀU**:

| chiều | hiện tượng | nguyên nhân |
|---|---|---|
| lọt | kẻ trèo ra TRƯỚC lượt dọn không bị bắt | nó chưa từng được ghi nhớ; vòng dọn chỉ quét lúc dọn |
| hô oan | lượt SẠCH bị khai là còn kẻ sống | tiến trình đã chết nhưng chưa được cha gặt (zombie) vẫn còn `/proc/<pid>/stat` đúng `starttime` ⇒ khoá danh tính khớp |

Một bộ phát hiện **hô oan** làm cổng mất tin cậy nhanh hơn cái lỗ nó vá. Nhét
nửa vời vào #141 là làm bản ghi nói dối theo chiều mới.

**Xong khi:** có bộ phát hiện (hoặc chặn) mà **cả hai** vế đều có phản chứng chạy
được — bắt được kẻ trèo ra thật, VÀ không hô oan trên lượt sạch có zombie. Nếu
kết luận là không đáng làm thì ghi thẳng vào đây và đóng mục, đừng để treo.

**Đã đóng phần khai báo** (head `052d100`+): chú thích trong `ci.yml` từng khai
"từ đó trở đi đường ra ngoài đã khoá" — LỜI KHAI SAI, vì `RIENG/cgroup.procs` vẫn
thuộc UID runner nên lệnh gate vẫn tự ghi mình ngược lên `RIENG` được. Đã sửa cho
khớp sự thật.

**Tạm thời:** mã đã KHAI THẲNG phạm vi (`gate_lifecycle.py`, khối "PHẠM VI CỦA
CHÍNH LỚP CGROUP"). `giet_tron_ven: true` chỉ nói "cgroup đã rỗng và đã xác nhận
rỗng" — KHÔNG bao gồm lời hứa "không ai trèo ra".

---

## 2. Cặp `gate-targeted.md:16` ↔ `ci.yml` — sửa cái này làm nặng cái kia

Hai thread cross-review còn mở, và chúng **dính nhau**:

- `gate-targeted.md:16` — tài liệu chỉ người review tái dùng bằng chứng gate của
  CI, nhưng CI không sinh/đăng artefact ấy ở lượt `pull_request`.
- `ci.yml` — trên `pull_request`, `actions/checkout` để cây ở commit MERGE tổng
  hợp, nên đòi `head.sha` sẽ đỏ ở preflight.

Cách sửa hiện tại cho vế thứ hai là **bỏ qua** bước sinh evidence trên
`pull_request` (`69267ff`) — tức chính nó làm vế thứ nhất nặng thêm.

**Đây là đánh đổi thiết kế, không phải lỗi.** Ba đường: (a) checkout PR head vào
worktree riêng rồi sinh evidence ở đó; (b) nhận diện và validate thẳng commit
merge; (c) sửa tài liệu để chỉ hứa đường `workflow_dispatch`/push.

**Xong khi:** chọn một đường, và tài liệu KHÔNG hứa đường mà CI không chạy.

---

## 3. Bộ đột biến cho `gate_lifecycle.py`

`--dot-bien` hiện chỉ neo vào `launcher.py`. `gate_lifecycle.py` **không có bộ
đột biến nào** — và đó là lý do CẤU TRÚC khiến một ca mù sống sót qua bốn vòng vá
(ca `case_descendant_spawned_during_shutdown_is_contained` thoát vòng lặp bằng
hạn đồng hồ, nên vòng vá thứ tư chưa từng được ca nào chạm tới).

Người dùng đã quyết: **tách PR riêng**.

**Xong khi:** đột biến neo vào đường giết mới, ra `M/M`, và bảng không tự rỗng đi
khi sửa mã (bẫy đã trả giá ba lần trong một phiên).

---

## 4. Nợ "ca BO QUA tính vào tổng" ở `launcher_test.py`

`gate_lifecycle_test.py` đã sửa (lớp `BoQua`, harness đếm riêng). Kết quả đọc
được ngay: Windows CI từ `23/23` phẳng thành `23/23 ca (qua 14, bo qua 9, hong 0)`
— chín ca trước giờ vẫn được tính là đạt.

`launcher_test.py` **còn nguyên** nợ ấy: `104/104 ca (qua 92, bo qua 12, hong 0)`
— con số đầu vẫn nuốt phần bỏ qua. Bàn giao đã ghi cho `t19`/`t62`.

**Xong khi:** con số đầu không còn nuốt phần bỏ qua, hoặc CI từ chối số skip nằm
ngoài danh sách nền tảng cho phép.

---

## 5. Hook phiên KHÔNG chạy lần nào — và `doctor` không nói được điều đó

**Đo được 17-08-2026:** trong phiên remote gắn kho GIỮA phiên, `CLAUDE_PROJECT_DIR`
**không được đặt**, nên lệnh hook trong `.claude/settings.json` giải ra
`/.claude/hooks/session-start.sh` — hook **vắng mặt lặng lẽ**, không `codex` nào
được cài, và chỉ lộ ra khi sắp cần review chéo.

`doctor` có mục `hook-phien` nhưng nó so **băm tệp hook** với `origin/master`, tức
đo *"tệp có mới không"* chứ KHÔNG đo *"hook đã chạy chưa"*. Hai câu hỏi khác nhau
— đúng lỗi đếm SỰ CÓ MẶT thay vì KHẢ NĂNG. Tệp mới tinh vẫn có thể chưa từng chạy.

CLAUDE.md đã được sửa để ĐÒI người mở phiên tự chạy `doctor`/`chuan-bi`, nhưng đó
là hàng rào bằng chữ.

**Xong khi:** `doctor` phân biệt được "hook chưa từng chạy" với "hook cũ" — ví dụ
hook ghi một dấu vết (kèm danh sách năng lực + thời điểm) và `doctor` đọc dấu vết
ấy. Lưu ý: hook trên nhánh này đang CŨ HƠN master (`doctor` báo thiếu
`co-chay-probe`, `github-nguon-that`, `moi-truong-doc-truoc`), nên sửa hook ở đây
sẽ đụng bản mới hơn trên master — lấy hook từ master trước.
