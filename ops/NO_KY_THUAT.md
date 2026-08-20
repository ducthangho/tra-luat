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

## 4. Nợ "ca BO QUA tính vào tổng" — hoá ra ở CẢ HAI bộ, hai nửa cùng một khuôn

Nợ gốc ghi cho `launcher_test.py`: `104/104 ca (qua 92, bo qua 12, hong 0)` —
con số đầu nuốt phần bỏ qua; bàn giao ghi cho `t19`/`t62`. Nửa ấy ĐÃ ĐÓNG:
PR #153 (W0-M1 — tách `dong_ket_qua`, tử số chỉ đếm ca thực sự qua) + PR #156
(W0-M1F — `t119` chốt dây nối); đầu ra nay còn tự khai `KHONG DU` khi có ca
bỏ qua — người đọc không phải tự trừ. Số trích từ suite này phụ thuộc NỀN
(ubuntu bỏ qua ~1 ca, Windows ~13), nên trích vào sổ là phải ghi nền + ngày;
bản trước của mục này treo `118/119` không nền — re-review #154 xếp P3, đã gỡ.

Nửa gate: bản trước của mục này (kể cả bản "ĐÃ ĐÓNG" land kèm #154) trưng
"Windows CI từ `23/23` phẳng thành `23/23 ca (qua 14, bo qua 9, hong 0)`" làm
mẫu ĐÃ SỬA — nhưng tử số 23 ĐÓ vẫn là `len(CASES) - len(failures)` = qua +
bỏ-qua: chính câu khoe mang hình dạng N/N với 9 ca chưa chạy (re-review #154
xếp P2 sau khi PR đó merge; đo lại 18-08 trên Windows tại head nó:
`26/26 ca (qua 14, bo qua 12, hong 0)`). Harness đếm riêng THẬT (lớp `BoQua`);
chỉ DÒNG KẾT LUẬN nói dối. Nửa này đổi cùng khuôn ở PR #157 (18-08-2026;
packet điều phối trực tiếp, KHÔNG nằm trong bảng W0/W1 của
`ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md` — bản đầu gọi nhầm là "W0-M2", kế
hoạch land ở #155 cho thấy tên đó thuộc packet doctor-JSON bên launcher):
đo trên Windows 18-08, `25/25 ca (qua 14, bo qua 11, hong 0)` thành
`15/26 ca QUA (bo qua 11, hong 0) - KHONG DU: ...`, khoá bằng
`case_headline_khong_duoc_dem_ca_bo_qua_la_da_qua`, mã thoát giữ nguyên.

**Xong khi:** trên master, CẢ HAI tệp có tử số không nuốt phần bỏ qua — kiểm
bằng sự HIỆN DIỆN của `dong_ket_qua` + ca phản chứng trong từng tệp (`t118`/
`t119` bên launcher: ĐÃ có; `case_headline_…` bên gate: land cùng PR #157),
đừng kiểm bằng tên nhánh hay trạng thái PR — tên nhánh là thứ trôi. Còn lại
sau khi đóng, tách quyết định riêng: (i) chốt DÂY NỐI bên gate (P3 verdict
#157, comment 5319042626) — ĐÃ ĐÓNG tại PR #174 (packet điều phối trực tiếp,
cùng cách gọi với #157): ca
`case_main_phai_in_headline_bang_dong_ket_qua_va_giu_rc` đi qua `main()` THẬT
của một bản sao module, đọc CẢ stdout LẪN rc trên ba nhánh sạch/bỏ-qua/hỏng —
mutant (d) f-string cũ trong `main` lẫn (f) `return 0` vô điều kiện đều đỏ
(verdict #157 đo được cả hai đang SỐNG). Kiểm bằng sự HIỆN DIỆN của ca ấy
trong `.claude/dev/gate_lifecycle_test.py`: thấy ca là vế (i) đã đóng, chưa
thấy thì nợ còn mở — phải kiểm thế vì chính vế "Xong khi" ở trên kiểm bằng
hiện diện `dong_ket_qua` + ca phản chứng, mà hai thứ đó MÙ với dây nối
(verdict #157 dặn ghi chú này khi làm follow-up); (ii) vế "CI từ chối số skip
nằm ngoài danh sách nền tảng cho phép" là SIẾT CHUẨN (đổi rc), chưa làm ở cả
hai bộ.

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
ấy. **Lời khai cũ đã HẾT ĐÚNG, đính chính** (P3 review lượt 2 trên `e37e1f6`): bản
trước viết "hook trên nhánh này đang CŨ HƠN master, `doctor` báo thiếu
`co-chay-probe`/`github-nguon-that`/`moi-truong-doc-truoc`". Sau khi hoà master
thì không còn đo ra được nữa: `git diff origin/master -- .claude/hooks` **rỗng**,
và `doctor` in `DUNG_DUOC hook-phien du nang luc so voi master`.

Chính lượt hoà master là lúc phải rà lại lời khai này mà tôi để nguyên — sổ nợ
tự đặt chuẩn "lời khai phải khớp phép đo tại head hiện hành", nên đây là chỗ lệch
còn sót của chính nó.

---

## 6. Khe TRƯỚC khi CHẶN được tín hiệu — đã thu hẹp còn đúng một pha

**Trạng thái: gần đóng.** Phần nguy hiểm đã vá trong PR "chặn tín hiệu sớm"; còn
lại một pha vô hại nhưng khó đọc.

### Đã đóng cái gì

Trước bản vá, thứ tự trong `cmd_run` là: cắm handler → cấp cgroup → đăng ký dọn
→ **rồi mới** chặn mặt nạ. Giữa "cắm handler" và "chặn mặt nạ" có một quãng mà
`BiKetThuc` ném ra KHÔNG AI BẮT — nó bay thẳng qua `main()`.

Đo được ở quãng ấy: `rc=1` · **traceback ra stderr** · **KHÔNG bằng chứng** · và
nếu rơi đúng khoảng giữa `_tao_cgroup_gate()` với `atexit.register` thì **để lại
hẳn một thư mục cgroup**.

Quãng ấy rộng vài trăm micro-giây, nên lưới quét theo thời gian gần như không bao
giờ chạm: sweep 87 lượt lưới 0,01s bắt được `rc=1` đúng **2 lượt**, và cửa sổ rò
cgroup thì **không lượt nào** chạm — phải nới cửa sổ trên bản sao mới gọi ra được.

Vá bằng cách **chặn mặt nạ TRƯỚC khi cắm handler**: từ đó tín hiệu tới lúc nào
cũng nằm chờ (pending) tới khi gỡ mặt nạ, mà chỗ gỡ nằm BÊN TRONG khối `try` có
`except BiKetThuc` và `finally`. Kèm đăng ký `atexit` dọn cgroup ngay dòng sau khi
cấp (phòng thủ theo lớp). Ca `case_tin_hieu_giua_quang_dung_khong_duoc_lot_ra`
dùng mối nối `TL_GATE_EP_CHAM_SAU_CGROUP` để nới cửa sổ nên nó **tất định** —
không còn là nhánh chỉ đỏ được bằng cách sửa bản sao.

### Còn lại cái gì

Sweep 30 lượt (0,02→0,30s, bước 0,02s, 2 lượt/mốc) trên bản đã vá:

| kết cục | số lượt |
|---|---|
| `rc=143`, có bằng chứng | 24 |
| `rc=-15`, không bằng chứng | 6 |
| traceback | **0** |
| con gate sống sót | **0** |
| cgroup rác để lại | **0** |

Trong lưới ấy chỉ còn HAI kết cục, và `-15` là tín hiệu tới **trước khi
`pthread_sigmask` kịp chặn** — tức trước cả handler, trước cả cgroup, trước cả con
gate. Ở đó **không có gì để rò**: thiệt hại duy nhất là mất bản ghi của một lượt
chưa kịp bắt đầu, kèm mã thoát `-15` khác với `143` của mọi pha sau.

**"Hai kết cục" là phạm vi của LƯỚI, không phải lời khai phổ quát** (P3 review
`same_provider_approved` trên `f38a090`). Còn một pha ĐUÔI mà lưới 0,02–0,30s
không chạm tới: tín hiệu đến **sau khi gate đã xong** — `finally` đã trả handler
về mặc định trong khi tiến trình chưa kịp thoát — cho kết cục thứ ba là `-15`
**kèm bằng chứng ĐẦY ĐỦ** của một lượt đã hoàn tất. Vô hại (bằng chứng tả đúng
một gate đã chạy xong), nhưng vế "Xong khi" số 1 nói "mọi mốc bắn" thì phải kể
tên pha này, nếu không lại là lời khai rộng hơn thứ đã đo.

### Vì sao không vá nốt

Chặn mặt nạ sớm hơn nữa nghĩa là chặn ngay dòng đầu `cmd_run`, trước cả khi
`argparse` và preflight chạy. Khi ấy mọi lỗi preflight (repo sai, HEAD lệch, cây
bẩn) cũng phải đi qua đường dọn tín hiệu, mà ở đó chưa có gì để dọn — đổi một khe
không rò lấy một lớp phức tạp mới, đúng thứ doctrine bảo dừng lại mà hỏi.

### Xong khi

Một trong hai, và phải **kèm số đo**:

1. Mọi mốc bắn cho **cùng một** mã thoát đọc được (`143`) và cùng một kết cục
   bằng chứng — kể cả pha trước khi chặn được mặt nạ; hoặc
2. Tài liệu này khai thẳng: "bắn trước khi `pthread_sigmask` chặn được thì `-15`
   và không có bằng chứng là kết quả **CHẤP NHẬN ĐƯỢC**", rồi đóng mục.

Phép nghiệm thu, neo vào PHA chứ không vào giây (ngưỡng giây trôi theo máy/tải):

```
luoi thoi gian : 0,02s -> 0,30s, buoc 0,02s, 2 luot moi moc
goi ra co chu dich : dat TL_GATE_EP_CHAM_SAU_CGROUP=3 roi ban o giua quang do
                     (luoi thoi gian mot minh KHONG cham noi cua so micro-giay)
dem cgroup     : dem thu muc `tl-gate-*` DUOI diem gan cgroup v2, quet de quy
                 (`rglob`) — KHONG dem o goc diem gan, vi `_tao_cgroup_gate` tao
                 cgroup duoi nhanh cua CHINH tien trinh (`_cgroup_cua_ta()`),
                 tren host systemd cho ay khong phai goc
goi ra pha DUOI : chen quang ngu SAU `_atomic_json(evidence, payload)` cuoi
                  `cmd_run` (BAN SAO, khong sua kho), doi bang chung `status=pass`
                  hien tren dia roi moi ban SIGTERM
dat            : 0 traceback · 0 con song sot · 0 cgroup rac, o CA BA cach goi
```

**Ba cách gọi, không phải hai** (P3 review lượt 2 trên `e37e1f6`). Đoạn trên vừa
kể tên pha ĐUÔI, nhưng công thức nghiệm thu lúc ấy chỉ có lưới thời gian và mối
nối `TL_GATE_EP_CHAM_SAU_CGROUP` — **cả hai đều không chạm pha ĐUÔI**. Ai chạy
đúng công thức thiếu ấy rồi tuyên "đạt vế 1" sẽ lại khai rộng hơn thứ đã đo, đúng
hình dạng lỗi mà chính đoạn ấy vừa gọi tên — lùi một tầng. Cách gọi thứ ba ở trên
đã đo được: `rc=-15`, bằng chứng đầy đủ, 0 traceback.

---

## 7. `launcher_test.py` chớp một lượt `hong 1` — chưa tái hiện được

**Đo được** (phiên 17-08, nhánh `ops/tin-hieu-chan-som`): trong một lượt chạy
loạt `gate BẬT → gate TẮT → launcher`, `launcher_test.py` ra
`116/117 ca (qua 115, bo qua 1, hong 1)`. Tên ca hỏng **không bắt được** vì lượt
ấy chỉ giữ dòng tổng.

**Không tái hiện được:** 6 lượt sau đó đều `117/117`, kể cả một lượt chạy **đúng
lại thứ tự loạt** đã sinh ra nó.

**Không phải do thay đổi của nhánh này:** diff chỉ chạm `gate_lifecycle.py`,
`gate_lifecycle_test.py` và tệp này; còn `launcher_test.py` lẫn `launcher.py` có
**0 lần** nhắc `gate_lifecycle` (đo bằng `grep -c`). Không có đường mã nào nối
hai bên. Giả thuyết còn lại là **tranh chấp tài nguyên** khi chạy ngay sau bộ gate
(bộ ấy sinh nhiều tiến trình và cgroup), nhưng đó mới là giả thuyết — chưa đo.

**Vì sao đáng ghi thay vì bỏ qua:** một cổng chớp đỏ rồi tự xanh là cổng **không
tin được**, và lần sau ai gặp sẽ mất thời gian đúng chỗ tôi vừa mất. Ghi lại để
người sau không phải khám phá lại từ đầu.

### Đính chính: runner ĐÃ in tên ca hỏng

Bản trước của mục này viết "việc đầu tiên nên làm: cho runner in tên ca hỏng —
hiện `hong 1` không nói được ca nào". **Sai** (P3 review `same_provider_approved`
trên `f38a090`). Runner đã in `HONG {ten}: {ly_do}` sẵn ở `launcher_test.py`;
tên ca không bắt được là do **cách giữ log của lượt chạy loạt** (chỉ giữ dòng
tổng bằng `tail -1`), không phải do runner thiếu khả năng. Tôi đọc giới hạn của
phép đo mình dựng thành thuộc tính của thứ được đo — đúng lỗi tệp này tồn tại để
chặn.

### CẢNH BÁO CHỮ KÝ TRÙNG — đừng nhận nhầm

Trên host **không có `codex`** (đúng loại host chạy các phiên
`same_provider_approved`), ca `t53_doctor_bao_du_khi_du` đỏ **tất định** vì
`doctor` thoát 12 — cho ra **đúng** dòng tổng `hong 1`. Người chạy lại loạt trên
host như vậy sẽ tưởng vừa tái hiện được flake này, trong khi gặp một ca môi
trường khác hẳn. Kiểm `command -v codex` TRƯỚC khi kết luận đã tái hiện.

### Phép đo 19-08-2026 — CHỚP ĐÃ ĐƯỢC XÁC NHẬN, và nó là cái bẫy cho lượt sửa

Đo trên phiên cloud Linux, `core.abbrev=7`, `codex` CÓ mặt (`codex-cli 0.148.0`) nên
**không phải** ca host-thiếu-codex đã cảnh báo ở trên:

```
tại 47847b1   ->  126/128 ca QUA (bo qua 1, hong 1) · rc=1 · HONG t53_doctor_bao_du_khi_du: 12
tại d390b7e   ->  127/128 ca QUA (bo qua 1, hong 0) · rc=0     (ba lượt liên tiếp, đều xanh)
```

**`git diff 47847b1 d390b7e -- .claude/dev/launcher.py .claude/dev/launcher_test.py` là
RỖNG** — không một dòng nào đổi giữa hai mốc. Cùng mã, cùng máy, cùng bộ công cụ, kết
quả lật từ đỏ sang xanh và **giữ xanh qua ba lượt liên tiếp**.

Đây là bằng chứng trực tiếp nhất tới nay rằng `t53` chớp, chứ không đỏ tất định.

**CÁI BẪY CHO LƯỢT SỬA — đọc trước khi nhận packet này.** Chuỗi xanh dài không chứng
minh đã sửa xong, và cũng không chứng minh không tái hiện được. Một lượt thi công chạy
bộ test vài lần, thấy xanh, rồi kết luận *"không tái hiện được"* hoặc *"bản vá có tác
dụng"* thì **cả hai kết luận đều chưa có căn cứ**. Ba lượt xanh liên tiếp ở đây xảy ra
trên mã HOÀN TOÀN KHÔNG ĐỔI.

Cần một phép đo chịu được chớp: chạy N lượt (N đủ lớn, khai N ra), đếm tỉ lệ đỏ trước và
sau bản vá, và **giữ nguyên stdout/stderr của TỪNG lượt `doctor`** — đúng thứ hai lượt
trước đã hụt vì bộ chạy nuốt mất đầu ra.

### Manh mối thật: chính `doctor` mới là thứ chớp

Đo được sau đó: `python .claude/dev/launcher.py doctor` **thoát 12 rồi ngay sau
đó thoát 0** — cùng lệnh, cùng máy, cách nhau hai phút. Mà `t53` khẳng định
`returncode == 0`, nên **doctor chớp là `t53` đỏ là `hong 1`**. `t53` chỉ là nơi
nó lộ ra.

**ĐÍNH CHÍNH — bản trước ghép số của HAI lượt vào một câu** (P3 review lượt 2 trên
`e37e1f6`). Nó viết "thoát 12 ... `ok=True`, `thieu_bat_buoc=[]`", mà hai thứ ấy
**không thể cùng thuộc một lượt**: theo `_ma_doctor` (`launcher.py:3085`, docstring
ghi thẳng "Thiếu công cụ BẮT BUỘC luôn là 12"), thoát 12 ⇔ `thieu_bat_buoc` KHÁC
RỖNG. Hai trường sạch kia là của **lượt thoát 0 ngay sau**. Câu ghép ấy khiến
người sau đọc thành "JSON của lượt 12 vẫn sạch" rồi đi nghi ngờ nhầm `_ma_doctor`.

**JSON của lượt thoát 12 KHÔNG được chụp lại** — và chính nó mới nêu tên thủ phạm.
Review lượt 2 dựng lại bằng shim cưỡng bức timeout: lượt thoát 12 cho
`ok=False`, `thieu_bat_buoc=['codex']`, kèm
`co_mat_nhung_khong_chay_duoc: {loi: "timeout sau 8.0s"}` — tức cơ chế đúng là
**một lượt `--version` hết hạn** rồi bị đếm là thiếu, khớp nghi ngờ ban đầu.

**Việc phải làm khi nó chớp lần tới:** chạy `doctor --json` và **giữ nguyên
stdout** của đúng lượt thoát khác 0. Chỉ cần thế là mục này tự đóng được nửa
đường — đừng chỉ ghi lại mã thoát như tôi đã làm.

Thử gọi lại: 12 lượt không tải + 12 lượt dưới tải CPU ⇒ **24/24 đều thoát 0**.
Chưa gọi ra được — tải thật lúc nó chớp là **churn tiến trình/cgroup** (chạy ngay
sau bộ gate), không phải tải CPU.

### LẦN CHỚP THỨ HAI — và `codex` CÓ MẶT

Phiên 18-08 (nhánh `ops/so-no-vong-3`) chạy đúng thứ tự loạt cũ — gate BẬT, gate
TẮT, rồi `launcher_test.py` — và ra `117/119 ca QUA (bo qua 1, hong 1)` với
`HONG t53_doctor_bao_du_khi_du: 12`. Hai lượt `launcher_test.py` ngay sau đó đều
`118/119 ... hong 0`.

**Lần này loại được lời giải thích "trùng chữ ký"**: `command -v codex` chạy
TRONG CÙNG khối lệnh, trước bộ chạy, trả `/opt/node22/bin/codex` (rc=0). Nên đây
là `doctor` thoát 12 **trên máy đủ công cụ** — đúng thứ mục này đi tìm, không
phải ca host-thiếu-codex.

**Nhưng vẫn hụt đúng thứ cần**: lượt đỏ ấy nằm trong bộ chạy nên **stdout của
`doctor` không được giữ**. Lại đúng lỗi đoạn trên vừa dặn đừng lặp.

**Săn có chủ đích, thất bại:** dựng 6 vòng `gate_lifecycle_test.py` → 4 lượt
`doctor --json` ngay sau, giữ stdout của lượt nào thoát khác 0 ⇒ **24/24 đều
thoát 0**, không bắt được lượt nào.

Đừng gộp mẫu số. Ba nhóm lượt gọi lại KHÁC ĐIỀU KIỆN nhau:

| nguồn | số lượt | điều kiện |
|---|---|---|
| đoạn trên | 12 | **không tải** — nền trắng, không thuộc giả thuyết nào |
| đoạn trên | 12 | dưới tải CPU |
| đoạn này | 24 | **sau khi** bộ gate đã thoát |

Cộng lại là 48 lượt, 0 lần tái hiện — nhưng chỉ **24** lượt dính tới churn gate,
và **12** lượt không nằm dưới giả thuyết nào cả. Bản trước viết "48 lượt … qua
hai giả thuyết tải" rồi đặt ngay trước một kết luận về churn gate, tức mượn mẫu
số của phép đo khác để đỡ cho kết luận này (P3 review lượt 3 trên `15bb415`).

Vậy nên **KHÔNG đóng mục này**: hai lần chớp đều là tai nạn quan sát được, chưa
lần nào gọi ra được theo ý muốn.

### ĐÍNH CHÍNH: 24 lượt ấy KHÔNG loại được churn gate

Bản trước viết "churn gate **một mình nó không đủ** — nếu đủ thì 24 lượt đã bắt
được". **Sai, và sai đúng kiểu dòng 258-260 vừa dựng lên để chặn** (P2 review
lượt 3): đọc *giới hạn của phép đo mình dựng* thành *thuộc tính của thứ được đo*.
Hai chỗ hỏng độc lập:

**(a) Phép đo chưa từng đặt `doctor` vào trong cửa sổ churn.** Thiết kế là "chạy
bộ gate xong → gọi `doctor` NGAY SAU", mà churn của bộ gate **cạn ngay lúc nó
thoát** — bộ gate fail-close đúng ở chỗ dọn trọn vẹn, nên không còn gì để churn.
Đo bằng cách lấy mẫu số mục `/proc` mỗi 50ms:

```
--- bo gate        nen=85  dinh TRONG luc chay=93   NGAY SAU: 86
    => churn TRONG luc chay = 8    NGAY SAU = 1
--- launcher_test  nen=86  dinh TRONG luc chay=100  NGAY SAU: 87
    => churn TRONG luc chay = 14   NGAY SAU = 1
```

Cả hai bộ về nền NGAY khi thoát. Tức 24 lượt `doctor` ấy chạy trên máy **đã
yên**. Một phép đo không áp điều kiện X thì không kết luận được gì về X — không
"đủ", cũng không "không đủ".

**(b) Kể cả có áp đúng điều kiện, 0/24 vẫn không đỡ nổi chữ "không đủ".** Chớp
mới quan sát được 2 lần, cả hai đều tình cờ, nên tần suất nền chưa biết:

```
24 luot: can tren 95% cua p = 11.7%      48 luot: 6.1%
p= 2%  P(0/24)=0.616   p= 5%  P(0/24)=0.292   p=10%  P(0/24)=0.080
```

0/24 chỉ loại được tần suất **trên ~12%/lượt**. Một hiện tượng chớp ở mức 2-5%
cho 0/24 với xác suất 0,29-0,62 — hoàn toàn bình thường. Suy "không tái hiện"
thành "đã bác bỏ" là bịa ra một kết luận âm.

**Giả thuyết cho lần săn tới** (giả thuyết, KHÔNG phải phạm vi đã hẹp lại):
`launcher_test.py` mới là nguồn churn đáng kể — đỉnh **+14** so với nền, gần gấp
đôi bộ gate — và `t53` gọi `doctor` từ **bên trong** nó. Lưu ý cơ chế: `main()`
chạy `chay_bo_ca(CA, nk)` **tuần tự** (`launcher_test.py:5224`), nên lúc `t53`
gọi `doctor` thì không có ca nào chạy song song; thứ tác động là **dư chấn và
sân tạm của các ca trước**, không phải tải đồng thời. Nên lần săn tới phải là
**chạy cả bộ `launcher_test.py` nhiều lượt liền nhau** rồi đọc `t53`, chứ không
gọi `doctor` trần như tôi vừa làm.

**Xong khi:** gọi ra được `doctor` thoát khác 0 trên máy đủ công cụ (nghi trước:
một lượt `--version` của công cụ nào đó hết hạn dưới churn tiến trình ⇒ bị đếm là
thiếu), rồi hoặc vá cho nó tất định, hoặc khai rõ `doctor` có thể chớp và `t53`
phải chịu được điều đó. Nếu chạy đủ nhiều lượt mà không tái phát thì đóng mục
**kèm số lượt đã chạy** — đừng đóng bằng im lặng.

---

## 8. `PLAT-X2` (#195) LAND KÈM NỢ RE-AUDIT — đầu cuối chưa reviewer nào nhìn

**Người giữ kho quyết định 20-08-2026**, sau khi cả hai trần review đã cạn: `2/2` vòng và
`2/2` lời gọi codex. Đây là lựa chọn ở **Review Rescue Checkpoint**, không phải bỏ sót.

**Đo được — cross-review đã chạy thật, hai vòng:**

| vòng | head được review | verdict | kết quả |
|---|---|---|---|
| 1 | `c869796` | `changes_requested` | **P1**: diff mang 5 tệp trong khi write set khai 3 |
| 2 | `23588c9` | `changes_requested` | **không P1**; **P2**: fixture kế thừa cấu hình ký commit của host |

Cả hai finding **đã đóng** (`23588c9`, `17cb889`). Reviewer vòng 2 tự xác minh độc lập:
`base..HEAD` đúng ba tệp · `c869796..HEAD` chỉ hai mục xoá, mã không đổi lén · mutant của
CHÍNH NÓ khôi phục quét toàn `ops/leases/` làm `t32` đỏ · giả lập thiếu `actionlint` làm
`t33` đỏ · worktree cuối phiên sạch, HEAD không đổi.

**Nợ chính xác là gì — nói hẹp, đừng nói rộng hơn:** phần thêm **SAU** lần review cuối
(`23588c9`) chưa reviewer nào nhìn. Phần ấy gồm:

1. `17cb889` — vá P2: `-c commit.gpgsign=false` cho fixture, cộng lớp tự khoá đặt cấu hình
   thù địch ngay trong kho tạm;
2. revision 2 — thêm bước cài `actionlint` vào `ci.yml`, và chính mục nợ này.

Không phần nào đụng **logic mang thẩm quyền** của cổng đăng lease. Đó là lý do người giữ
chọn land kèm nợ thay vì override cả hai trần.

**Một sự thật đắt trong đó, chép ra để khỏi phải trả lại:** lớp tự khoá ở (1) **bản đầu
không có răng**. Nó đặt `gpg.program` — khoá của định dạng **openpgp** — trong khi máy dựng
fixture khai `gpg.format=ssh`, nên nó bám vào một khoá KHÔNG AI ĐỌC. Đột biến `M5` (gỡ
`-c commit.gpgsign=false`) **SỐNG SÓT**, `giet 0/1`. Một chốt chống "kế thừa cấu hình host"
mà chính nó đọc sai khoá của host thì không chặn gì; và câu "ca này tự khoá chốt" trong bản
nháp là **lời khai không có phép đo**. Sau khi ép `gpg.format=ssh` + `gpg.ssh.program`:
`M5` giết 1/1.

**Điều kiện coi là XONG:**

- một lượt review chéo (`codex`, hoặc provider khác `claude`) trên **đúng đầu đã land** của
  `#195`, kết luận không còn P1/P2 mở; **hoặc**
- một packet kế thừa chạm lại `ops/lease_publish_test.py` hay bước `tìm lease vừa đổi` được
  review chéo, và lượt ấy khai rõ đã soi cả phần nợ này.

Cho tới lúc đó, assurance thực của `#195` là **`same_provider_approved` cho phần đuôi**,
KHÔNG phải `cross_approved` cho toàn bộ. Đừng viện `#195` làm tiền lệ "đã được review chéo".
