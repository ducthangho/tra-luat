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

---

## 9. `PLAT-X5-required-status-check` — nợ **THƯỜNG TRỰC**, không phải nợ có hạn

**marker:** `PLAT-X5-required-status-check` trong `.github/workflows/ci.yml`

**Người quyết:** `ducthangho`, 21-08-2026 (Q7 = **KHÔNG BẬT**). Trước đó Q7 nằm ở trạng thái
thứ ba (`chưa quyết`); nay nó là một QUYẾT ĐỊNH, và hệ quả khác hẳn — nên mục này ghi *nợ
thường trực*, không ghi *nợ chờ xử*. Đừng để ai đọc nó thành "sẽ làm sau".

**Đo được, còn đỏ tại lúc mở mục này:** `.github/workflows/ci.yml` khai **2** chuỗi
`NỢ CÓ TÊN` (dòng 135 và 177) trong khi sổ này có **0** mục tương ứng. Nợ được đặt tên trong
mã mà không có nhà trong sổ là nợ **không ai đọc**. Mục 9 và mục 10 đóng đúng khoảng lệch ấy.

**Cái MẤT — nói thẳng:** câu hỏi *"CI có thật sự chạy gate không"* **vĩnh viễn không có nhà**.
Một selftest không thể tự chứng minh nó đã được GitHub gọi; thứ trả lời được câu ấy là branch
protection require status của job `gate`, và nó nằm NGOÀI kho. Không bật thì không ai trả lời.

**Cái KHÔNG mất — cũng phải nói thẳng, kẻo đọc rộng hơn thực tế:** với `PATH` thiếu
`actionlint` bộ kiểm **fail-close**: ca `t33_workflow_dang_lease_phai_qua_actionlint` trả
`KHÔNG ĐO ĐƯỢC` và bộ test thoát **rc≠0**. Thứ mất là **DETECTION**, không phải **PROTECTION**.
Đây KHÔNG phải "bỏ ngỏ cổng".

**Neo theo TÊN CA, KHÔNG neo tổng suite — và đây là bản đính chính THỨ HAI của cùng một câu.**
Bản đầu ghi *"vẫn còn **8 ca đỏ**"*: sai, chạy thật cho **đúng một**. Bản sửa ghi *"suite ra
`41/42`"*: cũng sai, và sai **ngay trong chính commit tạo ra nó** — commit ấy thêm `t43` nên
tổng thành `42/43`. Cross-review lượt 2 bắt được. Một con số neo vào **tổng suite** sẽ chết
mỗi lần ai đó thêm một ca; neo vào **tên ca** thì không.

Và câu *"tám lỗi cùng chết vì thiếu một dependency"* ở bản trước đã **BỎ**: nó thay một suy
luận bằng một suy luận khác trong khi đang tự nhận là sửa bệnh suy luận. Lượt chạy chỉ quan
sát **một** ca đỏ; nó không định danh tám lỗi nào, cũng không đo quan hệ nhân quả giữa chúng.

**Phạm vi thật của `t34`, bằng số:** `t34` che **3/8 = 37,5%** dạng gọi đã biết. Nó là lan can
chống hồi quy vô ý, **không phải security boundary**. Năm dạng đã ĐO là lọt được liệt kê
nguyên văn trong docstring của nó, và từ packet `SLICE-B-C` (#215) có một ca máy đòi docstring
ấy chứa đủ năm dạng — để lời khai không trôi rộng ra lần nữa.

**Điều kiện coi là XONG:** người giữ kho đảo Q7 và bật required status check cho job `gate`.
Chừng nào Q7 còn là KHÔNG, mục này **không có điều kiện xong** — và đó chính là nghĩa của
"thường trực". Mỗi lần đổi cách gọi bộ test vẫn sẽ đẻ một finding; đó là giá đã biết trước.

---

## 10. `don-nhanh-test-chua-chay-duoc-tren-windows` — nền nó CHẠY THẬT là nền duy nhất không được đo

**marker:** `don-nhanh-test-chua-chay-duoc-tren-windows` trong `.github/workflows/ci.yml`

**Đo được:** bước `don-nhanh selftest (chốt xoá nhánh)` trong `.github/workflows/ci.yml` mang
`if: runner.os != 'Windows'` — tức nó chạy ở mọi nền TRỪ Windows.

**Vì sao đáng trả, không phải nợ vặt:** `don-nhanh.ps1` **vốn là script CHO Windows** (có
`don-nhanh.cmd` đi kèm). Nên hiện trạng là: thứ duy nhất KHÔNG được đo lại chính là nền nó
sinh ra để chạy. Đây cùng một hình dạng với bài học đã trả giá của kho — *một job CI mặc định
SKIP là một cổng KHÔNG TỒN TẠI* — chỉ khác là ở đây `skip` được khai tường minh trong `if:`
chứ không núp sau một nhãn.

**Đừng đọc rộng hơn:** ca vẫn chạy trên Linux qua `pwsh`, nên hồi quy logic thuần vẫn bắt
được. Thứ chưa đo là **hành vi phụ thuộc nền** — và kho đã có tiền lệ đo được rằng con số ấy
không nhỏ: cùng `.claude/dev/launcher_test.py`, CI 17-08-2026 đo Linux bỏ qua **1** ca còn
Windows bỏ qua **13**.

**Điều kiện coi là XONG:** bước ấy chạy được trên `windows-latest` với bằng chứng DƯƠNG
(`N/N` hai số bằng nhau) trên một lượt CI thật, và `if:` được gỡ hoặc thu hẹp kèm lý do.

---

## 11. `t34-loi-khai-pham-vi-khong-co-cong` — mục tiêu bị BỎ, không phải đã xong

**Nợ này sinh ra từ một quyết định BỎ, và đó là điều đáng ghi nhất về nó.**

Issue #215 đặt ba việc; việc thứ ba là *"một ca máy đòi docstring `t34` chứa đủ năm dạng đã ĐO
là lọt"*. Ca ấy (`t42`) đã được viết, rồi **gỡ bỏ** ở lượt vá thứ hai theo quyết định của người
giữ kho. Sổ này ghi lại **cái chưa xong**, không ghi lại một chiến thắng.

### Đo được — ba lượt, cùng một hình dạng

| lượt | kết quả |
|---|---|
| cross-review 1 | tìm được đột biến **nới** `_CHAY_BO_TEST` nhận thêm cờ đơn: hành vi đổi (`3 bắt/5 lọt` → `4/4`) mà suite vẫn `42/42` |
| bản vá cho nó | đẻ ra **hai** docstring tự mâu thuẫn với chính mã vừa viết, **cộng** một con số chết ngay trong commit sinh ra nó |
| cross-review 2 | tìm được đột biến **siết** `\S*` → `(?:ops/)?`: hành vi đổi mà `t42` vẫn xanh |

### Vì sao BỎ chứ không vá tiếp

`t42` là **một lời khai về một lời khai** — nó khẳng định *"docstring có chứa chuỗi X"*. Mỗi
bản vá lại sinh một câu mới có thể trôi, và bằng chứng sạch nhất là con số chết **trong chính
commit tạo ra nó**. `CLAUDE.md` nói thẳng về đúng tình huống này: *"cùng một hình dạng lặp ba
lần trở lên thì câu hỏi đúng là **có nên làm việc này không**, không phải **vá thế nào**"*.

Đối chiếu để thấy khác biệt: `t43` được **giữ** vì nó đo **quan hệ giữa hai tệp** — một sự
kiện, không phải một câu chữ ai đó gõ vào docstring.

### Cái MẤT, nói thẳng

Docstring `t34` vẫn liệt kê năm dạng lọt và con số `3/8`, nhưng **không cổng nào canh** cho
chúng khớp hành vi thật của `_CHAY_BO_TEST` nữa. Ai nới hoặc siết regex ấy mà quên sửa
docstring sẽ để lại một lời khai đã chết, và **không gì đỏ**. Đây là nợ **DETECTION**, giống
§9 — không phải lỗ bảo vệ, nhưng cũng đừng đọc thành "không sao".

### Điều kiện coi là XONG

Một thiết kế **khác** cho cùng mục tiêu, và nó phải thoả điều mà `t42` không thoả: **đo HÀNH VI
của regex trên một ma trận có trục** (runner × đường dẫn tương đối/tuyệt đối × quoting × cờ),
rồi **SINH** lời khai từ phép đo thay vì đối chiếu với một chuỗi gõ tay. Kèm phản chứng cả hai
chiều: một đột biến **nới** và một đột biến **siết** đều phải làm ca đích ĐỎ. Thiếu vế "siết"
thì đúng là lỗ mà cross-review 2 vừa tìm ra.

**Đừng dựng lại `t42` nguyên dạng.** Ba lượt đã đo là nó thua ở thiết kế, không thua ở chi tiết.

---

## 12. `PLAT-X4-721-dong-chua-verdict-nao-phu` — nợ RE-AUDIT, và tài liệu đang khai là ĐÃ ĐÓNG

**Sinh ra từ phép đo 22-08-2026**, khi rà bản hợp nhất `ops/THAM_DINH_KE_HOACH_20260821.md` so
với thực tại. Chạm tệp này **ngoài packet** theo chuẩn thuận người giữ kho, in-session 22-08-2026
(*"Cứ chạm ngoài packet, ghi nợ 721 dòng đi"*) — `ops/NO_KY_THUAT.md` thuộc write set dự kiến của
**#209**, packet ấy `state:ready` và **0 lease**.

### Đo được

| phép đo | kết quả |
|---|---|
| `git diff --numstat 909d3e17 a09aae62` | **4 tệp, +721/-159** — đúng con số bản hợp nhất nêu |
| `a09aae62` **có mặt trên** `master`? | **CÓ** — `git merge-base --is-ancestor` |
| `a09aae62` đã ở trạng thái protocol `landed`? | **KHÔNG ĐO ĐƯỢC** — xem ghi chú ngay dưới bảng |
| tệp verdict `plat-x4-*` trong `ops/reviews/` trên master | **0** |
| nhánh `ops/verdict-x4-*` trên remote | **0** (có `verdict-x5-review-1/2/3`, `verdict-m4-review-2`, `verdict-donref`, `moi-truong-review-1…10`) |
| lượt review đã cấp lease cho X4 | **BA**, không phải hai — `plat-x4-review-1r2`, `-review-2`, `-review-3`, tất cả `granted_by: ducthangho` |
| kết quả lượt 1 · lượt 2 | **`changes_requested`** cả hai — ghi trong **thân lease lượt kế tiếp**, không phải trong `ops/reviews/` |
| phạm vi lượt 3 | `tu_sha: 1d37861e` → `den_sha: a09aae62`, 2 tệp, `+100/-16` (soi DELTA) |
| kết quả lượt 3 | **KHÔNG có ở đâu** — không tệp, không nhánh, không trường trong lease nào sau nó |
| `base_sha` của **cả ba** verdict `PLAT-X5` | **`a09aae62`** — cả ba |

> **"Có mặt trên master" KHÔNG phải "đã land".** Ancestry chỉ chứng minh commit đã vào lịch sử; nó
> **không** chứng minh cổng sau merge và sổ sách của trạng thái `landed` đã chạy xong. Bản đầu của
> mục này viết thẳng *"⇒ đã land"* và cross-review bắt đúng chỗ đó (P2 lượt 3 trên PR #230) — mỉa mai
> ở chỗ đây là mục sổ nợ viết ra để chống đúng kiểu suy trạng thái từ tín hiệu gần nhất.

### Nợ chính xác là gì

**BẢN ĐẦU CỦA MỤC NÀY SAI, và cross-review lượt 3 bắt được (P2 trên PR #230).** Nó viết *"lease review
đã được cấp hai lượt mà không để lại verdict ở đâu"*. Đo lại: **BA** lượt, và hai lượt đầu **CÓ** kết
quả. Chép cái sai ra đây thay vì xoá, vì cái sai ấy có ích: nó cho thấy đọc `ops/reviews/` rồi kết
luận về lịch sử review là **hỏi sai chỗ**.

**Nợ thật, sau khi đo lại — và nó KHÁC bản đầu ở chỗ chịu tải:**

Vùng phủ được **thiết kế là đủ**: lượt 1 + lượt 2 phủ tới `1d37861e`, lượt 3 phủ delta
`1d37861e..a09aae62`. Cộng lại đúng bằng `909d3e17..a09aae62`. Nên nợ **không phải** *"chưa ai
review"*.

Nợ là: **ba lượt review đã tiêu, và KHÔNG lượt nào để lại HIỆN VẬT verdict.** Kết quả lượt 1 và
lượt 2 chỉ tồn tại như một **trường trong thân lease của lượt kế tiếp**
(`plat-x4-review-2.yaml:63` và `plat-x4-review-3.yaml:83`, cả hai `verdict: changes_requested`).
Lượt 3 thì **không để lại gì** — không tệp, không nhánh, không trường trong bất kỳ lease nào sau nó.
Không ai biết nó kết luận gì, hay có chạy không.

**Và lease lượt 3 khai một điều SAI, đo được.** `plat-x4-review-3-codex-20260820.yaml:36` viết:

> *"hai lượt trước đã phủ phần còn lại và cả hai đều **có verdict trong `ops/reviews/`**"*

`ops/reviews/` có **0** tệp nào nhắc X4. Câu ấy là căn cứ để lượt 3 thu hẹp phạm vi xuống chỉ soi
delta — tức **một lời khai sai đã được dùng làm lý do bỏ soi phần còn lại**. Cùng họ với câu
*"vòng 3 đã lấp chỗ ấy"* ở `ops/THAM_DINH_KE_HOACH_20260821.md`: hai tài liệu độc lập, cùng một
cách hỏng — khẳng định về hiện vật mà không mở chỗ chứa hiện vật ra xem.

**Review duy nhất tìm thấy trên PR #205** là của bot connector `chatgpt-codex-connector`, neo
`d0acd79f` (commit ĐẦU của X4). Bot ấy không sinh receipt, không mang `review_class`, không nằm
trong ngân sách vòng — **không phải** verdict protocol, và không thay được lượt nào trong ba lượt trên.

**Và điều làm nợ này khác mục 8:** `PLAT-X2` land kèm nợ re-audit một cách **có khai báo** — người
giữ kho quyết ở Review Rescue Checkpoint, hai vòng đã chạy thật, hai finding đã đóng. Ở đây thì
`ops/THAM_DINH_KE_HOACH_20260821.md` khai rằng chỗ trống **đã được lấp**:

> *"biên nhận X5 neo `base_sha: a09aae62`, nên 721 dòng của X4 chưa verdict nào phủ — điều đó vẫn
> đúng, và vòng 3 chính là thứ đã lấp chỗ ấy."*

Vế sau **sai, đo được**: vòng 3 neo **đúng cái `base_sha` ấy** (`plat-x5-review-3-claude-verdict.receipt.yaml:22`).
Đổi `reviewed_sha` mà giữ nguyên `base_sha` thì vùng phủ **không lùi xuống** — nó chỉ dài thêm về
phía trước. Một nợ được ghi là đã trả thì không ai đi đòi: **nguy hơn nợ chưa ghi.**

### Điều kiện coi là XONG

1. **Hiện vật của lượt 3 được tìm thấy hoặc dựng lại.** Đây là chỗ trống duy nhất về NỘI DUNG:
   lượt 1+2 đã có kết quả (dù chỉ ghi trong thân lease kế tiếp), lượt 3 thì không có gì. Tìm trước
   khi dựng lại — quét mọi ref, mọi PR comment; **không tìm thấy phải nói là KHÔNG TÌM THẤY**, không
   được lặng lẽ coi là chưa chạy.
1b. **Ba verdict thành TỆP trong `ops/reviews/`** kèm receipt, `review_class`, `base_sha`. Hiện kết
   quả lượt 1+2 sống ký sinh trong lease của lượt sau — một chỗ không ai đi tìm, và chính vì thế
   bản đầu của mục này đọc ra "không có verdict nào". Đọc `base_sha` để kiểm vùng phủ, **đừng đọc
   `reviewed_sha`**: chính chỗ lẫn hai trường ấy đẻ ra nợ này.
1c. **Sửa lời khai sai ở `plat-x4-review-3-codex-20260820.yaml:36`** — append-only, lease đã đăng
   là bản ghi bất biến. Câu ấy khai hai verdict "có trong `ops/reviews/`" trong khi ở đó có 0 tệp,
   và nó là căn cứ để lượt 3 thu hẹp phạm vi.
2. Hoặc: người giữ kho quyết **miễn** re-audit, và quyết định ấy được ghi đúng khuôn mục 8 — nêu rõ
   trần nào đã cạn và vì sao chấp nhận. Miễn thì được, miễn **im lặng** thì không.
3. Trong cả hai đường: câu sai ở `ops/THAM_DINH_KE_HOACH_20260821.md` phải được đính chính
   **append-only** — đã làm 22-08-2026, xem mục `ĐÍNH CHÍNH 22-08-2026` trong chính tệp ấy.

### Vì sao chưa ai thấy — và chốt máy còn thiếu

Không lệnh nào trong kho trả lời được *"khoảng commit nào đã có verdict phủ"*. Muốn biết thì phải
mở từng receipt đọc `base_sha`, mà receipt nằm rải trên master lẫn nhánh `ops/**` — cùng hình dạng
với nợ `SO-LEASE-KHONG-NAM-MOT-CHO`. Nợ này là **anh em** của nợ ấy, đổi đối tượng từ lease sang
verdict. Lệnh cần có: `phu-boi-verdict-nao <sha-tu>..<sha-den>`, quét mọi ref, và
**fail-close khi không fetch được ref nào** — *"không đo được"* phải ĐỎ, không được thành
*"không có"*.
## 13. `ADR-0016-THIEU-DONG-TRANG-THAI` — trạng thái thứ ba đang được tha bằng danh sách

> Đánh số bắt đầu từ **13** vì `## 12.` thuộc PR #230 (`PLAT-X4-721-dong-chua-verdict-nao-phu`),
> chưa land lúc viết. Nếu #230 không land thì đánh số lại — đây là chỗ DUY NHẤT của hai mục này
> phụ thuộc vào PR ấy, và nói ra để nó không thành một khoảng trống không ai giải thích được.

`docs/adr/0016-lop-dieu-phoi-rasoat-hoso-state-lai-single-writer-anchor.md` **không có dòng
`Trạng thái` nào**. Đó là trạng thái thứ ba — `không đo được` — và theo doctrine `None ≠ False`
nó phải làm cổng ĐỎ, không được đọc thành "chắc là còn hiệu lực".

Cổng `packet_loop.py adr-song` hiện **tha** đúng số ấy bằng một danh sách liệt kê tường minh
(`_ADR_THA_THIEU_TRANG_THAI`). Danh sách cho phép, không phải ngưỡng: một ADR MỚI thiếu dòng
`Trạng thái` vẫn ĐỎ, và có phản chứng cho đúng điều đó
(`adr_song_thieu_trang_thai_thi_do` ĐỎ với `0007`, `adr_song_ngoai_le_0016_van_xanh` XANH với
`0016`), cộng một đột biến **nới danh sách cho phép để chứa số tấn công**
(`adr_noi_ngoai_le_cho_moi_ADR`) làm ca đích chết — không có đột biến ấy thì không biết ca đang
đo danh sách hay đo thứ khác.

**Điều kiện coi là XONG:** người biết lịch sử quyết định ấy ghi đúng trạng thái vào tệp, rồi
xoá `"0016"` khỏi danh sách. Danh sách này **chỉ được co lại, không được nới** — nới nó là quay
về đúng cái bệnh nó đang che.

**Lệnh tái lập:**

```
python3 .claude/dev/packet_loop.py adr-song --root .
python3 - <<'PY'
import pathlib,re
for f in sorted(pathlib.Path("docs/adr").glob("*.md")):
    if not re.search(r'^\s*[-*]\s*\*\*Tr[aạ]ng th[aá]i', f.read_text(encoding="utf-8"), re.M|re.I):
        print("THIEU:", f.name)
PY
```

## 14. `LEASE-KHAI-MA-CONG-KHONG-DOC` — 239/247 trường, không phải hai

Bản bàn giao ngày 22-08 khai bệnh này bằng **hai** field (`review_class` 10/49 · `spec_sha256` 11/49).
Đo trên `origin/master` = `2ab3560a`:

| | | (nền `3f641673`, ~2h trước) |
|---|---|---|
| lease `.yaml` | **61** (0 tệp không parse) | 49 |
| tên trường **mức GỐC** | **247** | 230 |
| `ops/lease_publish.py` có nhắc | **8** | 8 |
| **không ai kiểm** | **239** | 222 |

**Cột thứ ba không phải trang trí — nó là bằng chứng cho cách viết con số này.** Trong khoảng hai
giờ, `#227` land rồi bị revert một phần (`#234` → `#237`), để lại 12 tệp lease mới: số trường nhảy
`230 → 247`. Nếu mục này ghi `230` trơ trọi thì nay nó là một lời khai SAI. Ghi kèm **neo SHA** thì
nó vẫn là một phép đo ĐÚNG — chỉ là của một thời điểm khác. Đó là lý do giữ số thay vì bỏ số, và là
lý do neo SHA thay vì ghi ngày.

Hai con số **KHÔNG** đổi qua cả hai lần đo: cổng đọc **8**, và **16** trường khai ở 100% lease. Thứ
chịu tải của mục này nằm ở hai con số ấy, không ở tổng số trường.

Tám tên cổng có nhắc: `granted_by` · `lease_expires_at_utc` · `lease_id` · `packet_issue` ·
`posted_comment_id` · `prompt_path` · `prompt_sha256_required` · `reviewed_sha_required`.

Nặng nhất không phải các field hiếm mà là **16 trường khai ở 100% lease** và vẫn không ai đọc:
`access` · `assurance_target` · `attempts_limit` · `attempts_used` · `base_sha` · `branch` ·
`branch_ownership` · `event` · `granted_on_instruction` · `leased_at_utc` · `packet_id` ·
`provider` · `recorded_by` · `role` · `run_minutes` · `schema_version`.

### Con số này ĐÃ SAI MỘT LẦN, và cách nó sai đáng nhớ hơn con số

Bản đầu của mục này ghi **215/207**. Sai vì phép đo dùng regex `^([a-z_][a-z0-9_]*):` — đòi khoá
**toàn chữ thường**, nên bỏ sót đúng **15** khoá có chữ HOA (`pham_vi_NGOAI`, `write_set_KHONG_gom`,
`la_luot_review_CUOI`, `assurance_KHONG_dat`…). Kho này dùng chữ hoa trong tên khoá để nhấn mạnh, nên
đó không phải ca hiếm.

**Tệ hơn con số sai: bản đầu còn ship kèm một LỆNH TÁI LẬP dùng chính cái regex hỏng ấy.** Lệnh chạy
được, chạy nhanh, và tái lập **trung thành** một con số sai — nên nó trông y hệt bằng chứng. Một phép
đo sai có lệnh tái lập thì khó phát hiện hơn một phép đo sai không có gì, vì cái lệnh mua cho nó sự
tin cậy mà nội dung không xứng.

Thứ bắt được: một phiên **khác** đo độc lập bằng `yaml.safe_load` và ra **230**, rồi nhắn sang. Cột
giữa — cổng đọc **8** — hai bên khớp tuyệt đối, và chính chỗ khớp ấy khoanh vùng được lỗi nằm ở phép
liệt kê khoá chứ không ở phép dò cổng. **Bài học: đọc YAML bằng bộ phân tích YAML.** Regex trên văn
bản thô là cùng họ với `_MARKER_NO` của `t43` và với bộ quét lease khớp nháy kép mà YAML ghi nháy đơn
(§5.1 của `ops/HOAN_THIEN_KE_HOACH_20260822.md`) — **ba lần trong một ngày, cùng một hình dạng.**

**Cảnh báo đọc số:** 247 là số **tên trường**, không phải số **lỗ hổng**. Nhiều trường cố ý là ghi chú
cho người đọc (`*_note`, `*_ghi_chu`, `canh_bao_*`) và không nên có cổng. Phép đo nói "không ai kiểm",
nó **không** nói "phải kiểm hết" — đọc rộng ra là tự đặt cho mình một việc không ai duyệt.

**Điều kiện coi là XONG:** một quyết định phạm vi — trường nào lên hợp đồng, trường nào rớt xuống ghi
chú tự do — chứ không phải "cổng đọc đủ 247". `PLAT-X8` (#225) nhận `review_class`; `PLAT-X7` (#220)
nhận danh tính model; phần còn lại cắt ở `ops/HOAN_THIEN_KE_HOACH_20260822.md` §3.

**Lệnh tái lập — dùng bộ phân tích YAML, KHÔNG dùng regex, và đo trên `origin/master`:**

```
python3 - <<'PY'
import subprocess, re, yaml, collections
def sh(*a): return subprocess.run(a, capture_output=True, text=True).stdout
tep = [p for p in sh("git","ls-tree","-r","--name-only","origin/master","ops/leases/").split()
       if p.endswith((".yaml", ".yml"))]
src = sh("git","show","origin/master:ops/lease_publish.py")
dem, hong = collections.Counter(), 0
for p in tep:
    d = yaml.safe_load(sh("git","show",f"origin/master:{p}"))
    if isinstance(d, dict): dem.update(d.keys())
    else: hong += 1
doc = [k for k in dem if re.search(r'["\']' + re.escape(str(k)) + r'["\']', src)]
print(f"lease {len(tep)} · khong parse {hong} · truong {len(dem)} · cong doc {len(doc)} · khong doc {len(dem)-len(doc)}")
print("khai 100% ma khong doc:", sorted(k for k,c in dem.items() if c==len(tep) and k not in doc))
PY
```

**`khong parse` phải bằng 0.** Khác 0 mà vẫn in ra con số là đúng cái bẫy đã sập ở trên: một phép đo
bỏ sót đầu vào trông y hệt một phép đo sạch.

---

## 15. `REVIEW-BUDGET-KHONG-CO-CONG` — trục LỜI GỌI vượt trần, và `ADR-0043` chưa được THI HÀNH

**Bản đầu của mục này TRỘN HAI TRỤC, đúng cái bệnh `ADR-0043` sinh ra để chấm dứt.** Nó viết *"trần 2
lượt, PR này dùng 4"* — trong đó `2` là trần trục **LỜI GỌI** còn `4` là số **head đã có finding**.
Một phiên khác (`tra-luat-5a`) đính chính khung này, tôi đo lại và xác nhận. Chép cái sai ra đây vì
nó là bằng chứng mạnh nhất cho chính mục: **tôi trộn trục ngay trong lúc viết về việc trộn trục.**

`ADR-0043` nói thẳng ba trục là ĐỘC LẬP, trần nào chạm trước thì thắng:

| trục | bộ đếm | trần | đo được trên PR #233 |
|---|---|---|---|
| **LỜI GỌI** (chi phí) | `codex_review_calls_used` | 2 | **≥ 4** — VƯỢT |
| **VÒNG** (canon, kỷ luật) | `review_rounds_used` | 2 | **0** — không vượt |
| **ATTEMPT** (số lần tuyên bố DONE) | — | — | ngoài phạm vi mục này |

Hai con số ấy đo bằng ĐỊNH NGHĨA của protocol, không bằng cảm giác:

- `:754` — `codex_review_calls_used` *"tăng khi có bằng chứng lời gọi review đã bắt đầu sinh
  output/token, **kể cả** timeout hoặc output sai schema"*. Đo theo OUTPUT: **4 head** có finding
  (`cbd14439bb` · `d17019628f` · `ef19e3b075` · `bc98b1f7`), **5 finding** trên 5 thread, và chỉ **3**
  trong số đó có comment `@codex review` đi trước — lượt đầu sinh output mà không có lời gọi tường
  minh nào của phiên này. Nên `≥ 4`, không phải `= 3`: đếm theo lời gọi tường minh là đếm THIẾU.
- `:756` — `review_rounds_used` *"chỉ tăng khi verdict qua schema, exact-SHA và receipt validation"*.
  Đo: `ops/reviews/` **không có** verdict hay receipt nào cho `#233`. Finding của connector codex
  chưa từng đi qua đường ấy ⇒ **0**.

Nên phát biểu đúng là: **trục LỜI GỌI vượt gấp đôi; trục VÒNG chưa chạm.** Và mỉa mai đúng chỗ —
`0` trên trục VÒNG không phải tin tốt: nó nghĩa là bốn lượt review ấy **không để lại verdict nào**,
tức chúng tốn chi phí mà không sinh ra thứ canon đếm được.

### `ADR-0043` là `Accepted` mà chưa được thi hành — 3/4 đã làm trong PR #233

`ADR-0043` liệt kê bốn việc. Đo lúc phát hiện (22-08-2026), **cả bốn chưa làm**; ba việc chữ nghĩa đã
được sửa trong PR này sau khi người giữ kho duyệt, việc thứ tư là mã và cần packet riêng:

| việc `ADR-0043` giao | lúc phát hiện | nay |
|---|---|---|
| sửa `docs/PROTOCOL_DA_PHIEN.md:751` để trỏ về ADR | *"ba vòng code/review tổng cộng"* | **đã sửa** — trỏ `ADR-0043`, dòng vẫn ở `751` |
| sửa `docs/adr/0037` dòng 5 | *"ba vòng code/review tổng cộng"* | **đã sửa** — trỏ `ADR-0043` |
| sửa mermaid `ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md:156` | *"Hết 2 Codex call hoặc 3 vòng"* | **đã sửa** — *"chạm trần vòng ADR-0043"* |
| `doctrine-scan` mở rộng + chế độ `so-canon` | `so-canon` **0** lần trong `packet_loop.py`; `doctrine-scan` quét **7** tệp | **CHƯA** — là mã, cần lease riêng |

Giữ nguyên `:751` đúng dòng số cũ là có chủ đích: `ADR-0043` **neo theo số dòng ấy**, nên đổi số dòng
là làm chính con trỏ của ADR thành con trỏ chết — đúng bệnh mà `§20` sinh ra để chặn.

**Hai chỗ CÒN chữ "ba vòng" là ĐÚNG, đừng sửa:** `ADR-0043` và
`ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md:495-496` đang **trích dẫn** bản sai để giải thích. Một cổng
`so-canon` viết bằng grep chuỗi sẽ báo động giả ở đúng hai chỗ này — nên nó phải phân biệt **phát biểu
luật** với **trích dẫn**, và đó là lý do việc thứ tư không phải một dòng grep.

Tái lập:

```bash
sed -n 751p docs/PROTOCOL_DA_PHIEN.md
sed -n 5p docs/adr/0037-*.md
sed -n 156p ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md
grep -c "so-canon" .claude/dev/packet_loop.py          # 0
python3 .claude/dev/packet_loop.py doctrine-scan --root . | tail -1
```

Lúc phát hiện: canon là **HAI** vòng theo `ADR-0043`, còn **ba** tài liệu vẫn nói **BA** — đúng tình
trạng `ADR-0043` được viết ra để chấm dứt, và nó vẫn đang sống. Một phiên đọc protocol trước (đúng như
dossier dạy) sẽ dùng ba vòng một cách **ngay tình**, y như ADR mô tả. Đó là lý do ba dòng ấy được sửa
ngay thay vì xếp hàng: mỗi ngày để nguyên là một ngày cái bẫy còn lên cò.

Đã quét toàn kho để chắc chỉ có ba chỗ, không phải ba chỗ ADR **nhớ ra**:
`grep -rn "ba vòng\|3 vòng" docs/ ops/*.md CLAUDE.md .claude/`. Hai chỗ còn lại sau khi sửa đều là
**trích dẫn bản sai**, giữ nguyên. Một chỗ nữa (`ops/DINH_CHINH_REVIEW_CLASS_PLAT_M4.md:97`) nhắc "ba
vòng" trong lúc **kể một ca cụ thể**, không phát biểu luật — cũng giữ.

### Bài học rộng hơn ô `0 cổng`: `Trạng thái: Accepted` KHÔNG có nghĩa ĐÃ THI HÀNH

`§20` đo *"cổng nào ĐỌC luật ấy"*. Mục này lộ ra một khoảng mù **trước** cả câu hỏi đó: một ADR có
thể `Accepted`, có mục **Thi hành** liệt kê bốn việc cụ thể, và **không việc nào** được làm — mà
không dòng nào trong kho nói ra. `adr-song` hiện chỉ đòi mỗi ADR **có mặt** trong bảng và có dòng
`Trạng thái` đọc được; nó không hỏi mục Thi hành đã xong chưa. Đây là biến thể của lỗi kho đã trả
giá bốn lần: **đếm sự CÓ MẶT thay vì KHẢ NĂNG.**

**Điều kiện coi là XONG (hai phần rời nhau, đừng gộp):**

1. **Trần lời gọi có cổng** — một cổng đọc được `codex_review_calls_used` trên một PR và ĐỎ khi vượt,
   kèm phản chứng `rXX_` hai chiều (vượt ⇒ đỏ · trong trần ⇒ xanh) và một đột biến **nới trần** để
   chứng minh ca đích đang đo đúng thứ đó.
2. **`ADR-0043` được thi hành** — bốn việc trong mục Thi hành của nó, mỗi việc có phép đo tái lập
   được như bảng trên. Việc này thuộc packet khác và cần lease riêng; **không** làm kèm trong một PR
   tài liệu.

Chưa ai làm phần nào. Đừng đóng mục này bằng một câu trong tài liệu — đó đúng là cách `ADR-0043`
thành `Accepted` mà không ai thi hành.


## 16. `THE-HTML-TRONG-COMMENT-BI-NUOT` — dấu nháy ngược không phải hàng rào, lần thứ hai

Đăng một reply dài lên PR #233: **gửi ~5000 ký tự, đến 466**. Comment dừng giữa một dòng bảng, và
tôi chỉ biết vì đã đọc ngược về rồi đo — đúng chốt (a) của bài học *"tầng vận chuyển cũng chuẩn hoá
chuỗi"* trong `CLAUDE.md`.

Ranh giới cắt, đo bằng `repr()` trên bản ĐÃ ĐẾN:

```
GỬI : | `<pre>` `<div>` `<script>` `<textarea>` `<p>` | `rc=0` · ... |
ĐẾN : | `<pre>` `` `
```

Đọc ra được hai việc riêng biệt: thẻ `div` **bị gỡ** (còn trơ hai dấu nháy ngược từng bao nó), rồi
tại thẻ `script` **toàn bộ phần còn lại biến mất** — bộ phân tích HTML nuốt tới thẻ đóng, mà không
có thẻ đóng. **Dấu nháy ngược không che được**: bộ lọc chạy trên thân THÔ, trước Markdown.

**Không phải lần đầu, và lần đầu đã đi lọt.** Comment `5378121537` trên cùng PR dài **517** ký tự và
kết thúc giữa câu — cùng bệnh, đăng lúc 05:11, không ai thấy suốt bốn giờ. Một comment bị cắt trông
y hệt một comment ngắn.

Cùng họ với dấu bỏ-qua-CI (`CLAUDE.md`): *"GitHub khớp CHUỖI trên toàn thông điệp, không đọc
Markdown — dấu nháy ngược không phải hàng rào"*. Chỉ khác đối tượng: ở đó là chuỗi kích hoạt trong
commit message, ở đây là thẻ HTML trong thân comment.

**Cách viết an toàn:** nêu tên thẻ **không dùng ngoặc nhọn** (`pre` · `div` · `script`), hoặc đặt
trong khối rào — đo được là thẻ nằm trong khối rào ba dấu nháy ngược **đã đi qua nguyên vẹn** ở các
reply trước của cùng PR. **Chốt duy nhất tin được vẫn là đo thứ ĐÃ ĐẾN**: đăng xong đọc ngược về,
so độ dài và kiểm vài mốc cuối bài; "lời gọi trả thành công" không nói gì về thứ người đọc nhìn thấy.

Máy chưa canh được mục này — chưa có cổng nào đọc lại comment vừa đăng.

---

## 17. `CHECK-SUITE-BAO-XANH-CHO-LUOT-BI-HUY` — 3/3 lần, không phải chuyện hiếm

Thông báo webhook `check_suite.completed` gửi về `conclusion: success`, kèm chú thích *"No check in
this GitHub App's check suite failed"*. Đo theo **JOB** thì lượt `gate` **chưa chạy xong**:

| head | check_suite gửi về | `gate (ubuntu)` | `gate (windows)` |
|---|---|---|---|
| `225d47d0090cbe86940f2ad581e86ff551cf45ad` | **success** | `success` 29/31 | **`cancelled`** 21/31 |
| `fd78ead6b79d18bd08f3947545b07d04f05abdde` | **success** | **`cancelled`** 29/31 | **`cancelled`** 20/31 |
| `2d4986b5d5b0bbebd81abeabbbd0505cfdb8c23b` | **success** | **`cancelled`** 19/31 | **`cancelled`** 18/31 |

**Ba trên ba.** Trong một giờ có đúng ba lần đẩy bị lần sau đè lên, và **cả ba** sinh ra một thông báo
khai xanh cho lượt `gate` bị huỷ. Đây không phải một ca biên hiếm gặp — nó là **hành vi mặc định** của
kênh này với mọi lần đẩy chồng. Một agent đẩy nhiều lượt trong một phiên sẽ gặp nó ở **mọi** lượt trừ
lượt cuối.

### Ca 4 — biến thể KHÁC, và nó đánh vào đúng head ta cần

Ba ca trên đều là lượt **bị huỷ**. Ca thứ tư không có gì bị huỷ: `355a55dd566a8e3cdc2806c04c8db10f51810630`
là head **CUỐI**, không bị đè bởi lần đẩy nào.

```
07:17:xx  đẩy 355a55dd
07:18:42  check_suite.completed  success  head_sha 355a55dd   check_suite_id 88255207197
07:20:46  ĐO THEO JOB:  gate · in_progress
                          gate (ubuntu-latest)   27/30 bước
                          gate (windows-latest)  15/30 bước
07:23:36  check_suite.completed  success  head_sha 355a55dd   check_suite_id 88255207202
07:23:47  ĐO THEO JOB:  gate · completed · success
                          gate (ubuntu-latest)   success  29/31 chạy · 2 bỏ qua · 0 hỏng
                          gate (windows-latest)  success  28/31 chạy · 3 bỏ qua · 0 hỏng
```

**HAI `check_suite_id` KHÁC NHAU cho CÙNG một head** — `…197` và `…202`. Đó là bằng chứng đo được cho
cơ chế, không phải suy đoán: `gate` và `launcher` sinh **hai check suite riêng**, và suite của
`launcher` xong trước rồi khai `success` cho head ấy trong khi suite của `gate` còn chạy dở.

Chú thích của harness — *"No check in this GitHub App's check suite failed"* — **đúng nguyên văn**:
không check nào trong **suite ĐÓ** hỏng. Nó không nói gì về suite kia, và nó không tự nhận là nói.

**Vì sao ca này xấu hơn ba ca trên:** ba ca kia chỉ đánh vào head **trung gian**, thứ không ai cần
xanh. Ca này đánh vào head **CUỐI** — đúng thứ ta chờ để merge. Một agent nhận thông báo lúc `07:18:42`
rồi báo *"CI xanh, merge được"* sẽ **sai**, kể cả khi nó chưa đẩy chồng lần nào trong cả phiên.

**Kết luận đổi ĐƠN VỊ, không chỉ đổi độ cẩn thận:** đếm **suite** là sai đơn vị. Đơn vị đúng là **JOB**,
và phải liệt kê ĐỦ tập job cần (`gate (ubuntu-latest)` **và** `gate (windows-latest)`), rồi đòi từng job
`conclusion == "success"`. Một thông báo `check_suite` **không bao giờ** trả lời được câu *"CI trên head
này xong chưa"*, vì nó không biết về các suite khác — nên đừng hỏi nó câu ấy.

Nguyên nhân: lần đẩy kế tiếp **đè** lên lượt đang chạy (concurrency), GitHub **huỷ** nó. `cancelled`
không phải `failure`, nên câu *"không check nào HỎNG"* vẫn đúng **về mặt chữ** — và sai hoàn toàn về
mặt việc. Ba trạng thái, không phải hai: `xanh` · `đỏ` · **`chưa chạy xong`**; gộp trạng thái thứ ba
vào "không hỏng" là đúng lỗi `None ≠ False` mà kho đã đặt tên.

**Vì sao nguy hiểm hơn một cổng đỏ:** một agent đang lái PR về xanh sẽ nhận tín hiệu này làm *"CI đã
qua"* rồi đi tiếp. Nó không phải cổng VẮNG MẶT (`[skip` + `ci]`, `t24`) và cũng không phải đồ giả nói
dối — đây là **kênh thông báo khai xanh cho một lượt bị huỷ giữa chừng**. Biến thể thứ ba của cùng một
họ, và là biến thể duy nhất đến dưới dạng một thông báo chủ động.

Tái lập (MCP `x/actions`; tham số tên là `resource_id`, KHÔNG phải `run_id`, và payload lồng **hai**
tầng `{"jobs": {"jobs": [...]}}`):

```
actions_list  method=list_workflow_runs  branch=<nhánh>       -> lấy run id theo head_sha
actions_list  method=list_workflow_jobs  resource_id=<run id> -> đọc conclusion TỪNG job
```

**Chốt:** đòi `conclusion == "success"` trên **từng job cần**, và đếm bước — `cancelled` với 20/31 bước
trông y hệt `success` với 31/31 nếu chỉ nhìn "0 hỏng". Đừng kết luận từ `check_suite`, và đừng kết luận
từ số bước hỏng. Máy chưa canh được mục này; nó là kỷ luật đọc, cùng họ với *"hỏi chỗ tiện tay thay vì
hỏi chỗ kết luận được ghi"*.

---

## 18. `CHOT-CHONG-DANG-TRUNG-DOC-DAU-THEO-NHANH` — cùng một lease đã đăng BỐN lần

Đo 22-08-2026 trên 160 ref, `yaml.safe_load`, fail-close. Trong **90** lease có `posted_comment_id`,
có **3** lease mang **nhiều id KHÁC NHAU** — tức đã đăng nhiều lần:

```
4 lan  plat-x5-review-2-claude-20260820.yaml     5363965965 · 5364175428 · 5364489524 · 5364816383
3 lan  plat-x5-exec-1r4-codex-20260821.yaml
2 lan  plat-x5-review-3-claude-20260821.yaml
```

**9 lượt đăng cho 3 lease ⇒ 6 lượt thừa.** Bản trên `master` (`5fb8fb48`) là bản mang id của lượt
**thứ tư**.

**Điều khoản lease KHÔNG bị sửa** — đây là chỗ dễ kết luận vội, và bản đầu của mục này đã đặt sai tên
(`LEASE-DOI-NOI-DUNG-SAU-KHI-CAP`) trước khi đo. `diff` giữa hai phiên bản bất kỳ chỉ ra **đúng một dòng**:

```
< posted_comment_id: 5363965965   # workflow ghi, ĐỪNG sửa tay
> posted_comment_id: 5364816383   # workflow ghi, ĐỪNG sửa tay
```

Bản `a81ed083` (trên `ops/verdict-x5-review-2`) **không có** dòng ấy — đó là bản trước khi đăng. Nên
hiện tượng không phải *"lease bị viết lại"* mà là *"biên nhận đăng bị ghi nhiều lần, mỗi lần vào một
nhánh khác"*.

**Cơ chế, đọc thẳng từ mã trên `master`** (`ops/lease_publish.py:236-241`):

```python
# Idempotent trước tiên: workflow bị chạy lại (retry, re-run tay, push lại
# cùng commit) KHÔNG được đăng trùng một lease.
if lease.get("posted_comment_id"):
    raise Chan(RC_DA_DANG, ...)
```

Chốt đọc dấu **từ bản lease trong cây đang chạy**. Mà lease sống **theo nhánh**, và bước ghi ngược chỉ
ghi vào **nhánh đã đăng** — nên một bản sao trên nhánh khác không có dấu, chốt cho qua, và nó đăng lại.
**Chốt là per-branch, không phải toàn cục.** Chú thích ngay tại chỗ đã tự khai phạm vi hẹp ấy: nó chỉ kể
`retry`, `re-run tay`, `push lại cùng commit` — cả ba đều là **cùng một nhánh**. Ca "bản sao trên nhánh
khác" chưa từng nằm trong thiết kế, nên đây là **lỗ phạm vi**, không phải lỗi lập trình.

Cùng gốc với `SO-LEASE-KHONG-NAM-MOT-CHO` (§ trong `CLAUDE.md`) nhưng khác trục: nợ kia nói *lease nằm
đâu ta không thấy hết*; mục này nói **cái DẤU chống trùng cũng nằm rải theo nhánh y như vậy**. Một chốt
idempotent mà trạng thái của nó bị nhân bản theo nhánh thì không idempotent.

**CHƯA ĐO, đừng chế ra:** (a) sáu lượt thừa ấy có gây hại thật không — chưa đếm số comment thực tế trên
PR đích, và chưa biết lượt sau có ghi đè lượt trước không; (b) phạm vi `#238` (`LEASE-DANG-WINDOWS`) có
chạm cơ chế này không — `#227` đã land rồi bị revert bởi `#237`, nên không suy được từ đặc tả đã có;
(c) ba lease dính đều là `plat-x5-*` cộng một `ag-t0-01b` chỉ có một id — chưa rõ vì `PLAT-X5` chạy
nhiều lượt review hơn hay vì nhánh của nó bị fan-out rộng hơn.

**Muốn chặn thì dấu phải rời khỏi tệp per-branch:** hoặc hỏi nơi chỉ có MỘT bản (chính comment trên
GitHub, hoặc registry), hoặc quét mọi ref tìm `lease_id` trước khi đăng. Cách thứ hai lại đụng đúng
`SO-LEASE-KHONG-NAM-MOT-CHO`, nên hai nợ này nên được giải cùng nhau chứ không lần lượt.

Tái lập:

```
git for-each-ref --format='%(refname)' refs/remotes/origin   # PHAI fetch du truoc, xem CLAUDE.md
git ls-tree -r <ref> -- ops/leases/                          # gom (blob, duong dan)
# yaml.safe_load tung blob, gom posted_comment_id theo TEN TEP, dem id phan biet > 1
```

Máy chưa canh được mục này — chưa có cổng nào so biên nhận đăng giữa các nhánh.

## 19. `LEASE-THAY-THE-CHUA-CHUAN-HOA` — 5/121 blob mang một trường không tài liệu nào biết

**Snapshot đo lại 22-08-2026 trên 166 nhánh remote (không tính symbolic `origin/HEAD`).** `ops/leases/**` có
**121** cặp `(blob, đường dẫn)` duy nhất trên **111** đường dẫn. Trong đó **5** blob mang trường
`da_bi_thay_the`, và **cả 5** thuộc đúng một chuỗi:

```
plat-x8-exec-2 -> -2r2 -> -2r3 -> -2r4 -> -2r5 -> -2r6
```

Mỗi bản trỏ tới bản sau; bản cuối không mang trường ấy. Hạn của cả chuỗi **không đổi**
(`2026-08-23T14:10:00Z`). Nghĩa là **sáu bản ghi, một thẩm quyền**.

**Quét `docs/` · `.claude/skills/` · `ops/lease_publish.py` ⇒ 0 lần nhắc.** Trường này ra đời ở
`0d35e44` (22-08-2026), mang `schema_version: 2`, do executor `PLAT-X8` tự đặt.

### Vì sao nó tồn tại — và vì sao đó là nợ chứ không phải giải pháp

Lý do ghi nguyên văn trong tệp lease: chốt chống đăng trùng của `ops/lease_publish.py` trả `rc=9`
cho một `lease_id` đã có `posted_comment_id`. Executor **không sửa được tệp lease cũ**, nên phải
đúc `lease_id` mới rồi đánh dấu bản cũ đã chết.

Tức là: khuyết tật đăng-trùng (mục 18) **đẻ ra vòng xoay id**, vòng xoay **thổi phồng số lease còn
hạn**, và `da_bi_thay_the` là miếng vá thủ công cho hệ quả. Ba nợ trên một dây chuyền.

### Hai hướng trỏ NGƯỢC NHAU, và gộp chúng làm một là chỗ đã trả giá

```
r5.thay_the_lease  = r4     moi -> cu    muon biet r4 chet chua: phai quet CA KHO
r3.da_bi_thay_the  = r4     cu  -> moi   mo dung MOT tep la biet
```

Đặc tả `LEASE-HOI-TOAN-KHO` bản đầu gạt **cả ba** trường vào cùng một ô `ngoai_pham_vi` với lý do
*"trỏ NGƯỢC, đọc xuôi không suy ra được"* — lý do ấy **đúng cho hai trường và sai cho trường thứ
ba**. Ba lượt cross-review không ai tách ra kiểm, vì ba tên nằm chung một ô bảng. Hệ quả: một
`ai-dang-giu` xây theo bản ấy sẽ báo *"6 lease đang giữ"* khi có **1** — **chặn nhầm** một packet
hợp lệ.

### Nợ cụ thể

1. **Chưa có lược đồ.** `da_bi_thay_the` không nằm trong protocol, ADR, hay schema lease nào. Nó có
   thể được thu nhận, hoặc chết cùng packet đã đặt ra nó — chưa ai quyết.
2. **Vắng trường KHÔNG phải bằng chứng còn hiệu lực.** 116/121 blob vắng nó vì trường **chưa tồn
   tại** lúc chúng được đúc, không phải vì chúng còn sống. Mọi bộ đọc phải dùng nó theo chiều
   **THU HẸP** tập người giữ, không bao giờ **MỞ RỘNG** — sai chiều là fail-open.
3. **Chưa có đường thu hồi** (nợ `AG-T0-01B-thu-hoi-lease-chua-co-duong`). `da_bi_thay_the` chỉ
   *đánh dấu*, không *thu hồi*.

Tái lập:

```
git for-each-ref --format='%(refname)' refs/remotes/origin   # PHAI fetch du truoc, xem CLAUDE.md
git ls-tree -r <ref> -- ops/leases/                          # gom (blob, duong dan) duy nhat
# yaml.safe_load tung blob; dem blob co khoa `da_bi_thay_the`
git log --all -S'da_bi_thay_the' --reverse -- ops/leases/    # commit dau tien dat ra truong nay
```

Máy chưa canh được mục này — chưa có cổng nào kiểm lease dùng trường ngoài lược đồ.

---

## 20. `ci-phamvi-test-chua-chay-duoc-tren-windows` — bộ phản chứng chạy 0/7 ca trên Windows, không phải 2/7

**marker:** `ci-phamvi-test-chua-chay-duoc-tren-windows` trong `.github/workflows/ci.yml`

**Đo được, TÁI LẬP ĐƯỢC trong kho:** bước `ci-phamvi selftest (phan chung — cong co rang)`
trong `.github/workflows/ci.yml` mang `if: runner.os != 'Windows'`, và điều kiện ấy nằm ở mức
**BƯỚC** — nên nó bỏ qua **cả bảy** ca trên Windows. Bước gác cổng `ci-phamvi guard` **không**
mang `if:` nào, nên nó chạy ở mọi nền. Hai câu này đọc thẳng từ tệp, không cần mạng.

> **CỐ Ý KHÔNG ghim id run hay head vào mục này.** Trạng thái từng bước của một lượt CI sống
> trên GitHub chứ không trong kho, nên ai đọc mục này từ một bản sao kho **không kiểm được nó**
> (cross-review lượt 2, `run-windows-trong-so-no-khong-tai-lap`). Bản trước chữa bằng cách khai
> "đây là lời khai ngoài kho" **rồi vẫn ghim một id run** — mà id ấy thuộc head TRƯỚC commit
> ghi nó, nên nó cũ ngay khi được viết, và lượt kiểm sau lại chỉ người ta tới một mỏ neo chết.
> Chữa ở TẦNG: mục này chỉ giữ thứ đọc được từ tệp; trạng thái CI tra ở PR #258, nơi luôn có
> bảng bằng chứng neo head mới nhất.

**Cái gì bị bỏ lại, nói cho đúng phạm vi:** bộ phản chứng có 7 ca, và chúng **không cùng
loại**. `t1` `n1` `n2` `n3` đo LOGIC thuần (dẫn xuất từ mã, ba trạng thái, nhóm bịa) — độc
lập nền — `n4` cũng thuộc nhóm này: nó chỉ thay **biểu thức trả về** của `phan_loai()`, không
gọi `unlink`/`mkdir`/`os.symlink`. Chỉ `n5` và `n6` đo **ngữ nghĩa duyệt cây**: thư mục trùng
tên TỆP, và symlink-tới-thư-mục.

**Hai trục này ĐỘC LẬP — đừng suy trục nọ ra trục kia:**

| trục | Linux | Windows |
|---|---|---|
| loại ngữ nghĩa | `t1 n1 n2 n3 n4` = logic · `n5 n6` = duyệt cây | *(không đổi theo nền)* |
| **độ phủ CI** | **7/7 chạy** | **0/7 chạy** |

`if: runner.os != 'Windows'` nằm ở mức **BƯỚC**, nên nó bỏ qua **cả bảy** ca trên Windows —
không phải chỉ hai ca duyệt cây. Bản trước của mục này viết *"đúng hai ca ấy là phần không nền
nào ngoài Linux đo lại"*: **sai**, và đó là lần **thứ hai** phân loại này sinh sai ngay trong
lần đi vá phân loại (cross-review lượt 3 bắt). Gốc của cả hai lần là cùng một chỗ lẫn:
*"logic ĐỘC LẬP nền"* không có nghĩa là *"đã được ĐO trên nền đó"* — đúng họ với bài học
*"ca có MẶT khác ca có ĐO"* của kho.

Bản đầu của mục này xếp `n4` vào nhóm duyệt cây. Sai, và sai **do chính lần vá** một finding
về phân loại ở lượt review trước — cross-review lượt 2 xếp nó là `VÁ SINH LỖI MỚI`. Ghi lại vì
đó là lý do mục `ĐỐI CHIẾU LƯỢT TRƯỚC` của §8 tồn tại: sửa một chỗ rồi sinh sai ở chỗ khác là
thứ không lượt review nào khác nhìn tới.

**Vì sao vẫn chấp nhận được, và vì sao vẫn là nợ:** thứ bảo vệ `master` là **cổng**
(`ci_phamvi.py --kiem-bam`), không phải bộ phản chứng — và cổng chạy trên cả hai nền. Nó dẫn
xuất tập loại trừ bằng cách gọi `_build_release_manifest()` **trên nền đang chạy**, nên nếu
Windows duyệt cây khác Linux thì chính cổng đỏ ở đó. Cái mất là **chẩn đoán**: cổng sẽ nói
"lệch", không nói "lệch VÌ SAO". Cùng hình dạng với mục 10 (`don-nhanh`), chỉ nhẹ hơn một bậc
vì ở đây nền bị bỏ không phải nền mà mã sinh ra để chạy.

**Vì sao không vá ngay:** cho `ci_phamvi_test.py` chạy trên `windows-latest` đòi xử lý ba mặt
**chưa ai đo** ở đó — `os.symlink` (thường cần quyền đặc biệt), `git worktree`, và dọn thư mục
tạm còn tệp read-only của git. Đưa cả ba lên Windows mà chưa đo là đẩy một cổng có thể ĐỎ vào
`master`. Giữa *"cổng đỏ"* và *"cổng khai đúng phạm vi mình phủ"*, chọn cái thứ hai — nhưng
**không được đọc nó thành "đã phủ Windows"**.

**Điều kiện coi là XONG:** `ci_phamvi_test.py` chạy được trên `windows-latest` với bằng chứng
DƯƠNG (`N/N`, hai số bằng nhau) — hoặc, nếu nền thật sự không cho tạo symlink, thì bộ test
phải **dẫn xuất** lời tha từ một phép thử sống (không nhận lời khai theo tên nền), **đếm riêng**
số ca bỏ qua và in từng ca kèm lý do, cộng một ca canh chống bỏ-qua-âm-thầm theo lối `t73` của
`ops/lease_publish_test.py`. Bỏ qua im lặng thì mục này **chưa xong**.

**Xuất xứ:** mở ra ở packet `CI-NOI-BANG-VAO-GATE` (#254). Bản đầu của bước ấy khai marker
bằng chữ **không dấu** (`NO CO TEN`) nên né matcher `^\s*#\s*NỢ CÓ TÊN` và `t42` không đòi mục
này — cổng **vắng mặt**, không phải xanh. Cross-review lượt 1 (codex) bắt được
(`no-windows-ne-cong-so-no`), executor tái dẫn xuất: nền `87/87` `rc=0`, đổi marker sang dạng
chuẩn ⇒ **`86/87` `rc=1`**. Mục này ra đời từ đúng phép đo đó.

---

## 21. `SO-GUARD-DANG-DEM-LOI-GOI-KHONG-DO-DIEU-KIEN` — đột biến fail-open sống sót `87/88`

**Nơi nợ nằm:** hằng `SO_GUARD_DANG` trong `ops/lease_publish_test.py`.

> **CỐ Ý KHÔNG dùng dạng `**marker:** … trong …`** — dạng ấy là một LỜI HỨA rằng `t42` canh hai
> chiều, và với mục này lời hứa ấy SAI theo cả hai đường. `t42` khai thẳng phạm vi trong chính
> docstring của nó: *"ca này chỉ đo `.github/workflows/ci.yml` ↔ `ops/NO_KY_THUAT.md`"*. Nó bắt
> `group(2)` của `_BACKLINK_NO` (đường dẫn được khai) rồi **không so nó bao giờ** — dòng kiểm là
> `k not in trong_ma`, chỉ dùng KHOÁ. Nên một nợ có marker nằm ngoài `ci.yml` mà khai đúng dạng
> sẽ bị báo ĐỎ GIẢ: đo được khi soạn mục này, nền `87/88` → `86/88`, thông điệp *"marker ấy KHÔNG
> CÒN trong `ci.yml`"* trong khi nó chưa từng ở đó. Đây là mặt **đỏ giả** của khuyết tật mà `#265`
> đã liệt kê ba mặt **xanh giả**; đã báo bổ sung ở `#265`. Tới khi `#265` land, nợ ngoài `ci.yml`
> **không có cổng nào canh** — nói thẳng ra đây thay vì mượn một dạng trông như có canh.

**Đo được, TÁI LẬP ĐƯỢC trong kho** (hai đột biến dưới đây chạy trong `git worktree` rời, không
đụng tệp thật — xem bài học *"đột biến ghi vào tệp THẬT rồi khôi phục trong `finally` là bom hẹn
giờ"*):

| đột biến vào `.github/workflows/ops-publish-lease.yml` | 9 chuỗi `bao_chan` | kết quả |
|---|---|---|
| *(nền, không đột biến)* | giữ nguyên | **87/88** |
| chèn `if [ "$rc" = "6" ]; then continue; fi` trước cổng `check` — bỏ qua `rc=6` **im lặng** | **giữ nguyên** | **87/88** — LỌT |
| `sed 's/\bbao_chan\b/bao_chan_x/g'` — đổi tên hàm | **đổi hết** | **84/88** — bắt |

*(`t33` đỏ ở cả ba lượt vì thiếu `actionlint` — fail-close có chủ đích, không liên quan. Nền và
đột biến 1 lệch **0** ca.)*

### Cơ chế, đọc thẳng từ mã

`SO_GUARD_DANG` (`ops/lease_publish_test.py`) là **sổ chín LỜI GỌI** `bao_chan`, mỗi dòng ghim
nguyên văn thông điệp và vế trước/sau `POST`. `_guard_dan_xuat()` trích tập ấy khỏi thân bước
`đăng` bằng `re.findall(r"(?<![\w])bao_chan(?![\w(])", than)`, rồi `t64` đòi **tập dẫn xuất ==
tập đăng ký**.

Nó đo **các lời gọi CÓ MẶT**. Nó không đo **điều kiện nào DẪN TỚI** lời gọi. Chín chuỗi nằm im
trong khi `if [ "$rc" != "0" ]` phía trên bị siết lại thì tập dẫn xuất **không đổi một byte** ⇒
`t64` xanh, và `rc=6` (`RC_NEO` — lệch băm neo prompt) đi thẳng qua cổng không một dòng nhật ký.

Cùng hình dạng với bài học **"danh sách CẤM không bao giờ đủ"**, đổi trục: ở đây là **danh sách
CÓ MẶT không chứng minh được HIỆU LỰC**. Và cùng hình dạng với chính `t42` ở mục 20 — một cổng
khớp **hình dạng văn bản** thay vì **hành vi**.

### Vì sao là nợ, không phải bug

Mã trên `master` hiện **ĐÚNG**: `if [ "$rc" != "0" ]` bắt cả `rc=6`, và `bao_chan` có 9 chỗ gọi
thật. Không có gì đang chảy. Thiếu là **cái canh** cho chín nhánh ấy. Đây là lỗ **PHÁT HIỆN**,
không phải lỗ đang mở — nói cho đúng kẻo người sau đi vá nhầm chỗ, đúng lỗi mà lease `#244` đã
mắc một lần trong ngày (xem đính chính, `#244` comment `5384065633`).

### Xuất xứ — verdict `dung_lai` của `#227` mà việc vẫn land

| | |
|---|---|
| biên nhận | `ops/reviews/lease-dang-review-5-claude-verdict.md` |
| `sha256` | `d2b7eb935cde06034c7cce8975ab35bbf1f6fb06bf0284fb4faa2b4fbcf76ab3` |
| `reviewed_sha` | `ba82b06f9df81fc2f13786fec590ec2110d046b7` |
| vào `master` tại | `d54ab0b7507cb2d2a7f43b3f041165e8535aa401` |

Reviewer dựng **bốn** nhánh chặn, **ba** lọt với `68/68` xanh; chỉ nhánh đổi tên bị bắt, *"và bắt
vì phá phép ĐẾM CHUỖI chứ không vì cổng hiểu thế nào là chặn"*.

Cụm **"distinguishes spelling, not authority"** hay được nhắc cho hình dạng lỗi này. **Xuất xứ chính
xác, đo bằng tìm nguyên văn toàn kho** (đừng chép lại lời khai của bản trước):

| tệp | packet | provider | có cụm |
|---|---|---|---|
| `ops/reviews/wp55-r2-review-4-codex-verdict.md` | `wp55` | codex | **có** — đây là NGUỒN |
| `ops/reviews/lease-dang-review-5-claude-verdict.md` | `LEASE-DANG` | claude | có, nhưng là **trích lại** |
| `ops/reviews/lease-dang-review-{1,2,3,4}-claude-verdict.md` | `LEASE-DANG` | claude | **0 / 0 / 0 / 0** |

> **Bản đầu của mục này ghi *"Nguyên văn hai lượt verdict liên tiếp"* — SAI, và sai theo kiểu tệ nhất
> cho một sổ audit: nó bịa ra một xuất xứ.** Hai lượt verdict *liên tiếp* của `LEASE-DANG` không hề
> chứa cụm ấy; lượt 4 có **0** lần nhắc. Nguồn thật là một packet **KHÁC** (`wp55`), reviewer **khác
> nền** (codex). Cross-review codex bắt (P2, PR #271) bằng đúng phép tìm nguyên văn ở neo được xét.
>
> Đáng ghi hơn cả con số: **lỗi này có HAI tầng, và tôi chỉ thêm tầng thứ hai.** Chính
> `lease-dang-review-5` viết *"Nguyên văn verdict lượt trước"* — một lời quy nguồn đã lỏng sẵn. Tôi
> đọc nó rồi làm cho **chặt hơn bằng chứng**: "lượt trước" → "hai lượt liên tiếp". Trích một bản
> chiếu mà không đi tới nguồn thì cái lỏng không đứng yên, nó **siết lại quanh một điều sai**. Đúng
> họ với bài học *"nguồn có thẩm quyền là TỆP CÓ BĂM, comment chỉ là bản chiếu"* — ở đây bản chiếu
> là một verdict khác, và nó cũng có băm, nên nó *trông* như nguồn.

Verdict là `dung_lai` và **việc vẫn land** — `#227` nay mang `state:landed` vì hiện vật có trên
`master`, nhưng nhãn không có chỗ nói điều đó, nên nó ở đây và ở `#227` comment `5384069956`.

### Nợ cụ thể

Đơn vị phủ là **cặp `(thao tác, kết cục)` TỚI ĐƯỢC**, **KHÔNG** phải "chín nhánh, chín ca".

> **Bản đầu của mục này viết *"Chín nhánh, chín ca"* và *"mỗi mã thoát khác 0 và khác 9 phải tới
> được một `bao_chan`"* — cả hai đều HẸP HƠN không gian kết cục thật, tức một điều kiện "xong" mà
> đạt được vẫn còn hở.** Cross-review codex bắt (P2, PR #271). Hai chỗ hẹp, đo được:
>
> · **Một guard KHÔNG phải một kết cục.** `ops/lease_publish.py` khai **sáu** mã chặn —
> `RC_THAM_SO=2` `RC_TU_CAP=4` `RC_NEO=6` `RC_NOI_DUNG=8` `RC_DA_DANG=9` `RC_LOP=10` — ném ở **40**
> chỗ (`22` NOI_DUNG · `8` NEO · `3` TU_CAP · `3` LOP · `2` THAM_SO · `2` DA_DANG). `check` và
> `kiem-github` mỗi cái trả **nhiều** mã trong số đó. Test một mã cho mỗi guard rồi tuyên bố phủ
> ⇒ một fail-open **chọn lọc theo mã khác** vẫn lọt — đúng hình dạng đột biến `rc=6` ở bảng trên,
> chỉ đổi con số.
>
> · **Guard `case_id` KHÔNG kích hoạt bằng mã thoát.** Đọc thân workflow:
> `case "$ID" in ''|*[!0-9]*) bao_chan "gh không trả về comment id: $ID"; continue;; esac` — nó bắt
> **`gh` THÀNH CÔNG (rc=0) trả về ID rỗng hoặc không phải số**. Luật *"rc ≠ 0 và rc ≠ 9"* của bản
> đầu **không bao giờ chạm tới nó**: thay `_guard_dan_xuat` bằng đúng luật ấy là **xoá** phép canh
> của guard này mà bảng vẫn khai đủ chín. Đây chính là *"BẰNG CHỨNG DƯƠNG: đòi một ID số, đừng tin
> rc của `gh`"* — chú thích ngay tại chỗ đã nói, mà điều kiện xong của tôi vẫn bỏ qua.
>
> Cùng gốc với chính khuyết tật mục này mô tả: tôi **đếm chỗ có guard** thay vì **liệt kê kết cục
> tới được**. Viết một tiêu chí "xong" theo lối đếm là dựng sẵn một cổng xanh-mà-hở.

1. **Liệt kê kết cục trước, rồi mới viết ca.** Với mỗi thao tác trong thân bước `đăng`
   (`kiem-github` · `check` · đọc `packet_issue` · `body` · `payload` · `POST` · `mark` ·
   `GITHUB_ENV`), dẫn xuất tập kết cục **tới được** — mọi mã chặn mà thao tác ấy thật sự ném,
   **cộng** kết cục *"lệnh thành công nhưng đầu ra không hợp lệ"* ở đâu có (ít nhất `POST`→`case_id`).
   Tập ấy phải **dẫn xuất từ mã**, không gõ tay, kẻo nó trôi y như bảng chín dòng đã trôi.
2. **Mỗi cặp `(thao tác, kết cục)` một ca đo HÀNH VI:** bơm đúng kết cục ấy, đòi lượt chạy ĐỎ **và**
   đòi đúng thông điệp `bao_chan` của nhánh ấy có trong nhật ký. Đòi thông điệp chứ không chỉ đòi
   đỏ — `BI_CHAN=1 + continue` im lặng cũng đỏ.
3. **Đồ giả phải sinh đủ tập kết cục.** Verdict lượt 5 ghi rõ vì sao ba đột biến lọt: *"Đồ giả chỉ
   sinh rc ∈ {0, 8, 9} nên không ca nào chạm rc=6"*. Bộ ca có đủ mà đồ giả không dựng nổi kết cục
   thì vẫn là không đo.
4. **Mỗi ca mới kèm đột biến làm nó ĐỎ.** Ca không có đột biến riêng là ca sẽ âm thầm hở lại.
5. **Một ca canh chống trôi:** tập kết cục dẫn xuất phải khớp tập ca đã đăng ký; thêm một mã chặn
   mới vào `lease_publish.py` mà không thêm ca thì ĐỎ. Không có chốt này thì mục 21 tái phát dưới
   một con số khác.

**Chưa có packet nhận.** Ngoài `write_set` của `#244` theo **phạm vi đặc tả** (packet ấy là
`ai-dang-giu`), dù `ops/lease_publish_test.py` nằm trong write set của nó.
