# ĐO t33 SAU KHI CÀI actionlint, và chuẩn hoá việc dựng gói review

Ngày `2026-09-07`. Vá hai nợ còn lại sau khi PR #468 đạt verdict `approve`.

## 1. `t33_workflow_dang_lease_phai_qua_actionlint` — nay ĐÃ ĐO

Full-gate ngày `2026-09-07` cho `lease rc=1` ở **cả hai vế**. Đó là fail-close chứ không phải
hồi quy. Nhưng nói cho chính xác: **ca `t33` khi ấy ĐÃ CHẠY và ĐỎ** ở tiền điều kiện thiếu
`actionlint` — assertion tại `ops/lease_publish_test.py:1359–1363` (bản `b416830`) bắn **trước** `subprocess.run`
ở dòng 1364. Thứ **chưa chạy** là **thao tác lint workflow** bên trong hàm, không phải bản thân ca.

> Bản đầu của tài liệu này viết *"không đỏ, cũng không xanh — nó KHÔNG CHẠY"*. Lời khai này sai về
> mặt mã nguồn (assertion đánh rơi ca thành ĐỎ t33), nhưng xin lưu ý: **không có log của lần chạy
> hỏng đó**. Các tệp trong `ops/reviews/log-t33-20260907/` hoàn toàn là log chạy lại **thành công**
> (đạt 121/121). Việc "ĐỎ t33" là báo cáo lịch sử chưa kiểm chứng (historical unverified report) của
> executor kết hợp với phân tích mã nguồn, chứ không được chứng minh bằng các log đang giữ.

`ops/lease_publish_test.py:1338` (bản `b416830`) nói rõ chủ ý: *"`actionlint` phải XANH … và THIẾU công cụ là
ĐỎ."* Vậy `rc=1` là hành vi ĐÚNG, không phải lỗi mã. Cách đóng là **cài công cụ rồi đo**, không
phải nới phép kiểm.

Đã cài bằng **script ghim sẵn của kho** `ops/cai_actionlint.sh` (`AL_VER=1.7.7`, đúng bản CI ghim
ở `.github/workflows/ci.yml:97` bản `b416830`), có đối chiếu băm — `rc=0`.

> Tự khai: lần đầu tôi cài bằng `curl` tuỳ tiện, **không đối chiếu băm**. Đó đúng thứ kỷ luật của
> kho này bác bỏ. Đã gỡ bản ấy và cài lại bằng script của kho trước khi đo.

Đo lại bộ `lease` trên **cả hai vế** của full-gate:

| vế | sha | rc | kết quả |
|---|---|---:|---|
| nền | `b416830` | **0** | `121/121 đạt; đã chạy=121, bỏ qua=0` |
| sau | `f77f198` | **0** | `121/121 đạt; đã chạy=121, bỏ qua=0` |

`out` = 8649 B ở cả hai vế. Bộ `lease` đi từ `120/121, rc=1` lên **`121/121, rc=0`**.

**Phạm vi — thu hẹp theo P3 lượt 2 của #477.** Hiện vật đính kèm chỉ là **bộ `lease`**. Nên đúng
phải nói: *DELTA đã chuẩn hoá **của log bộ lease** bằng 0.* Câu cũ — *"`rc=1` cuối cùng của
**full-gate** đã biến mất"* — **rộng hơn hiện vật**: năm bộ còn lại không được chạy lại và không
có log kèm.

Thêm nữa, `nen_rc=0`, `sau_rc=0`, phiên bản công cụ và cách cài trong `moi-truong-va-rc.txt` là
**lời khai của executor**: không có transcript của runner ghi exit status, cũng không có log
installer hay băm archive để đối chiếu độc lập. Suy `rc=0` từ `main()` và dòng tổng kết là suy
luận có điều kiện, không phải phép đo `rc` của tiến trình đã chạy.

CI **đã** cài `actionlint` từ trước (`ci.yml:98`, `duyet-phan-chung.yml:54`,
`ops-publish-lease.yml` bản `b416830`). Nên đây chưa bao giờ là lỗ hổng của kho — chỉ là container chạy gate
thiếu công cụ. Nợ nằm ở chỗ dựng môi trường đo, và mục 2 vá đúng chỗ đó.

## 2. `ops/dung_goi_review.sh` — chuẩn hoá việc dựng gói

Việc dựng gói hiện vật trước nay nằm rải rác trong scratchpad từng phiên, không phải một thứ
chạy được trong kho. Đưa nó vào một script kiểm được và chạy lại được là **lựa chọn thiết kế**
có lý — nhưng đó không phải kết luận về nguyên nhân.

**GIỚI HẠN PHẢI ĐỌC.** Bản đầu của mục này viết *"vá tận gốc"* và *"ba lỗi liên tiếp có **cùng
một gốc**"*. Cả hai đều khai mạnh hơn bằng chứng: hiện vật lịch sử của ba sự cố **không còn**,
nên không ai kiểm được từng ca đã xảy ra thế nào, và **không chứng minh được chúng chung nguyên
nhân**. Bảng dưới là **danh sách động cơ** viết script này, không phải chẩn đoán đã xác thực.

| sự cố | biểu hiện | động cơ viết script (**chưa xác thực là nguyên nhân**) |
|---|---|---|
| P1 lượt 12 `mirror-thieu-ref-khong-du-do-a9` | gói chỉ mang 3 tên nhánh | **CHƯA XÁC THỰC ĐƯỢC** (hiện vật lượt 12 không còn) — xem ĐÍNH CHÍNH bên dưới |
| P3 lượt 13 `evidence-thieu-phuong-phap-trich-va-gioi-han-bao-phu` | `EVIDENCE.md` không khai cách trích số và phần bỏ sót | viết tay mỗi lượt |
| `t33` **ĐỎ** ở tiền điều kiện | container thiếu `actionlint`; hàm đã chạy, thao tác lint bên trong thì chưa | không có bước cài công cụ trước khi đo |

Script làm cả ba: clone mirror **đủ mọi ref**, **vật chất hoá** từng nhánh thành `refs/heads/*`,
cài công cụ bắt buộc bằng bản ghim của kho, sinh `EVIDENCE.md` **tự khai cách trích và phần bỏ
sót**, rồi lập manifest.

### ĐÍNH CHÍNH — chẩn đoán gốc ban đầu của tôi SAI

Bản đầu của tài liệu này (và các báo cáo tôi gửi chủ kho) viết:

> `ai-dang-giu` **chỉ quét `refs/heads/*`**, nên remote-tracking ref không được đếm.

**Sai.** Cross-review PR #477 (P3 `chan-doan-ai-dang-giu-chi-heads-khong-dung`) bắt được, và tôi
đã đọc lại mã để xác nhận:

- `_cac_ref_cuc_bo` (`ops/lease_publish.py:307–321` bản `b416830`) chạy
  `for-each-ref refs/heads refs/remotes` — **đọc CẢ HAI** — và tính tên nhánh từ cả
  `refs/remotes/origin/*`.
- `_quet_lease_toan_kho` đọc trọn danh sách ấy.

Tôi tin **banner của CLI** (`ops/lease_publish.py:937` bản `b416830` in `PHẠM_VI: quét refs/heads/*`) thay vì đọc
mã. Banner không phản ánh hết hành vi.

Hệ quả về nguyên nhân lịch sử, nói ở mức **giả thuyết** chứ không phải kết luận: cross-review
#477 lượt 2 đo được rằng `--bare --no-local` **tự nó không quyết định** — bare từ một nguồn đã có
306 local head thì giữ đủ 306; bare từ một clone thường (1 local head) mới còn 1. Tức nguyên nhân
phụ thuộc **cấu trúc ref của nguồn clone**, mà hiện vật của lượt 12 không còn để xác định.

Vậy: chắc chắn **không** phải phạm vi quét; nhiều khả năng là kiểu clone kết hợp cấu trúc ref
nguồn — nhưng **chưa xác thực được** bằng hiện vật lịch sử. Ca `--single-branch` tôi dựng chỉ mô
phỏng một cách thu hẹp, không chứng minh chuyện đã xảy ra.

Bước vật chất hoá `refs/heads/*` trong script **vẫn giữ**, nhưng vì lý do KHÁC với lý do tôi
nêu ban đầu: để gói không phụ thuộc tên remote, và để đối chiếu tập tên trực tiếp.

### Bằng chứng đã đo, không phải mô tả

Chạy thật trên kho này:

```
$ bash ops/dung_goi_review.sh <goi> $(git rev-parse origin/master)
ref: nguon=305 mirror=305 cay-kho=305; lech=0/0
GOI DU DE TAI DO: 305/305/305 ref, 0 lech
rc=0
```

- `cay-kho` có **305** `refs/heads`, `origin` = URL thật, HEAD = `b416830`.
- manifest `sha256sum -c` ⇒ **`rc=0`, 2131/2131**.
- `shellcheck` ⇒ **`rc=0`** (cài bằng `ops/cai_cong_cu.sh shellcheck`; thiếu nó thì
  `actionlint` bỏ luật `SC*` trong im lặng).

### Cổng fail-close — đã chứng minh CHẶN, không chỉ chứng minh đường xanh

| ca | mong đợi | đo được |
|---|---:|---|
| thiếu tham số | `rc=2` | **`rc=2`** |
| `--single-branch` thay `--mirror` | `rc=6` | **`rc=6`** — `nguon=305 mirror=1 cay-kho=1; lech=304/304` |

Ca thứ hai **KHÔNG** tái hiện lỗi lịch sử — hiện vật lượt 12 không còn nên không ai kiểm được
chuyện đã xảy ra thế nào. Nó chỉ chứng minh một điều hẹp hơn và vẫn có ích: nếu ai đó dựng gói
bằng clone một nhánh, script chặn ngay thay vì giao một gói mà reviewer không tái đo được.

### Log gốc của phép đo t33

Cross-review PR #477 (P3 `so-do-lich-su-thieu-hien-vat-tai-tinh`) chỉ ra đúng: bản đầu khai
`121/121` và `DELTA=0` mà **không kèm log**, nên đó chỉ là lời khai. Nay đính kèm ở
`ops/reviews/log-t33-20260907/`:

| tệp | nội dung |
|---|---|
| `nen.lease-sau-cai-actionlint.out` / `.err` | stdout/stderr vế nền `b416830`, 8649 B |
| `sau.lease-sau-cai-actionlint.out` / `.err` | stdout/stderr vế sau `f77f198`, 8649 B |
| `moi-truong-va-rc.txt` | lệnh, hai SHA đầy đủ, `rc` hai vế, bản `actionlint`/`shellcheck`, cách cài |

Hai stdout khác nhau **16 vị trí dòng (32 dòng cộng/trừ trong diff)** trước chuẩn hoá; sau khi chuẩn hoá tên thư mục tạm ngẫu nhiên
(`sed -E 's/lp_[a-z0-9_]+/LP/g'`) thì **giống hệt, 49/49 dòng**.

Vẫn chưa kiểm lại được, ghi rõ: TSV và manifest của lần đo `305`/`2131` **không còn** — chúng ở
thư mục tạm đã bị ghi đè bởi các lần chạy sau. Hai số ấy là **lời khai của executor, gói này
không đủ để kiểm lại**. Số ref đo lại lúc dựng gói #477 là **306**, mốc khác, không thay số cũ.

## Điều bản ghi này KHÔNG chứng minh

- Không đóng gói lại các gói review CŨ. `ops/reviews/pr468-*` giữ nguyên như đã giao.
- Không chạm `ops/lease_publish.py`. Lỗ hổng `any(...)` trong `_kiem_bia_mo` **vẫn nguyên** và
  thuộc packet riêng đang chờ chủ kho cấp lease.
- Không đo được trạng thái CI của PR trên GitHub: bộ công cụ GitHub của phiên chỉ có **44 tool**,
  không có nhóm workflow/actions.
- Số ref **305** là mốc lúc `2026-09-07` và **đang tăng** — mỗi nhánh mới cắt từ `master` lại
  mang thêm một bản sao lease chưa bia mộ. Trước đó đo được 9, rồi 11, nay 305 ref tổng.

## Cross-review PR #477 bắt được 1 P1 + 3 P2 trong chính script này

Script tự nhận là "vá gốc" nhưng chứa đúng phản mẫu mà kho đã ghi thành luật. Đã vá và tự dựng
lại từng phản chứng:

| finding | mức | lỗi | sau khi vá |
|---|---|---|---|
| `actionlint-co-mat-khong-phai-dung-ban` | **P1** | `if ! command -v actionlint` bỏ qua installer ghim — trái `ops/cai_actionlint.sh:14` (bản `b416830`) *"co mat != dung ban"*; rc trong đối số `printf` không làm `set -e` kích hoạt | luôn gọi installer ghim; bắt `rc` bằng assignment |
| `shellcheck-thieu-van-giao-goi-xanh` | P2 | chỉ ghi `THIEU` rồi đi tiếp, dù thiếu nó thì `actionlint` bỏ luật `SC*` trong im lặng | shellcheck vào danh sách BẮT BUỘC ⇒ `loi 4` |
| `remote-doi-ten-loi-van-khai-url-that` | P2 | hai `\|\| true` nuốt lỗi ⇒ `origin` trỏ sai mà vẫn `rc=0` | `\|\| loi 5` + đọc lại `origin` và đối chiếu |
| `manifest-loc-hau-to-bo-sot-tep-con` | P2 | `grep -v '  \./ARTIFACTS\.sha256$'` chỉ neo cuối dòng ⇒ thư mục tên `nested  .` làm tệp con bị loại | `find ... ! -path './ARTIFACTS.sha256'` |

Phản chứng tự đo sau khi vá:

| ca | mong đợi | đo được |
|---|---|---|
| `AL_VER=` (rỗng) | chặn | **`rc=4`** — *"AL_VER được đặt nhưng RỖNG"* |
| `AL_VER=1x.2y.3z` | chặn | **`rc=4`** — installer từ chối |
| thiếu `shellcheck` (PATH đầy đủ, chỉ gỡ nó) | chặn | **`rc=4`** — *"thieu cong cu bat buoc: shellcheck"* |
| git template có sẵn remote `mirror-cuc-bo` | chặn | **`rc=5`** — *"khong doi ten duoc remote origin"* |
| thư mục `nested  .` | tệp con phải nằm trong manifest | có **1** dòng; sửa nội dung ⇒ `sha256sum -c` **`rc=1`**, `FAILED` đúng tệp ấy |
| `actionlint 0.0.0-GIA` thoát 42 ở ĐẦU PATH | không được tin PATH | **`rc=0`**, `cong-cu.txt` ghi bản **1.7.7** tại thư mục vừa cài — PATH bị bỏ qua |
| đường xanh | qua | **`rc=0`**, `306/306/306` ref, 0 lệch |

Ca cuối là bằng chứng trực tiếp cho P1: trước khi vá, nhánh `command -v` sẽ nhận bản giả rồi
báo gói "ĐỦ ĐỂ TÁI ĐO".

## Cross-review #477 lượt 2 và 3 — hai lần bản vá của tôi tự sinh lỗi

| lượt | slug | kết luận | ghi chú |
|---|---|---|---|
| 2 | `actionlint-co-mat-khong-phai-dung-ban` | VÁ HỜ | `command -v` vẫn dính `export -f`; `case *"$AL_VER"*` khớp chuỗi con |
| 2 | `shellcheck-thieu-van-giao-goi-xanh` | **VÁ SINH LỖI MỚI** | prepend `$AL_DICH` làm tệp trong đó che lệnh hệ thống |
| 3 | `actionlint-co-mat-khong-phai-dung-ban` | **ĐÃ ĐÓNG** | gọi binary bằng đường dẫn tuyệt đối, so bằng nhau |
| 3 | `xoa-al-dich-di-theo-symlink-ra-ngoai-goi` | **P1 MỚI** | `rm -rf` tôi thêm ở lượt 2 đi theo symlink, **xoá dữ liệu ngoài gói** |
| 3 | `remote-doi-ten-loi-van-khai-url-that` · `manifest-loc-hau-to-bo-sot-tep-con` · `so-do-lich-su-thieu-hien-vat-tai-tinh` | ĐÃ ĐÓNG | |

P1 mới ở lượt 3 là loại nguy hiểm nhất trong cả chuỗi: `$R` do người gọi chọn, nên nếu
`$R/cong-cu` là symlink tới thư mục dùng chung thì `rm -rf "$R/cong-cu/actionlint"` **đi qua
thành phần symlink ở giữa** và xoá sạch ở đích. Reviewer đo A/B trên cùng nguồn: bản `3d2ac9b`
giữ sentinel, bản `a6a5222` **xoá** sentinel, cả hai `rc=0`. Hậu quả thứ hai: nó xoá luôn archive
offline mà người gọi đặt sẵn — tức bản vá của tôi phá đường air-gapped, và tôi đã đoán sai rằng
thủ phạm là việc bỏ prepend PATH.

Vá: **không xoá gì cả.** Từ chối `cong-cu` là symlink, rồi tạo thư mục cài mới bằng `mktemp -d`.
Hai `rm -rf` cũ (`kho.git`, `cay-kho`) cũng được chặn symlink cho nhất quán, dù reviewer không
quy chúng là nguyên nhân.

Phản chứng tự đo sau khi vá:

| ca | trước khi vá | sau khi vá |
|---|---|---|
| `cong-cu` là symlink ra ngoài | `rc=0`, sentinel **MẤT** | **`rc=4`**, sentinel **CÒN** |
| archive offline người gọi đặt sẵn | `rc=4`, archive **MẤT** | **`rc=0`**, archive **CÒN** |
| `shellcheck` giả đặt sẵn trong `cong-cu` | — | `rc=0`, chọn `/usr/bin/shellcheck` |
| `actionlint(){ echo 1.7.70; }; export -f` | — | `rc=0`, ghi `1.7.7` |
| đường xanh | — | `rc=0`, `306/306/306` |

## GIỚI HẠN CỦA `ops/dung_goi_review.sh` — hợp đồng đầu vào, tự khai

Cross-review #477 lượt 6 (`gioi-han-dung-goi-chua-tu-khai`) chỉ ra tài liệu này thiếu phần tự khai
điều kiện môi trường và quyền sở hữu thư mục đầu ra. Bổ sung, kèm báo cáo lịch sử chưa kiểm chứng (historical unverified report) do không còn lưu log đối chứng.

### Chỉ `actionlint` được ghim — ba công cụ còn lại TIN VÀO PATH ĐẦU VÀO

`actionlint` luôn được cài bằng `ops/cai_actionlint.sh` (bản ghim + đối chiếu băm) và gọi bằng
đường dẫn đã cài (có thể là tương đối nếu `$R` tương đối). Nhưng `shellcheck`, `git`, `python3` chỉ được resolve bằng `type -P` trên
`$PATH` người gọi đưa vào cho mục đích ghi nhận phiên bản. Thêm vào đó, việc gọi `git` thực tế trong script là gọi trực tiếp theo tên bare name, có thể bị thay thế bởi function/alias của shell. `type -P` bỏ qua function/alias/builtin — nó **không** xác thực nguồn gốc công cụ dùng để chạy.

Báo cáo lịch sử chưa kiểm chứng (historical unverified report): đặt một `shellcheck` giả đầu PATH ⇒ script **`rc=0`**, `cong-cu.txt` ghi
`version: 9.9.9` từ bản giả. Nói cách khác: **PATH và môi trường shell đầu vào là đầu vào TIN CẬY của hợp đồng.**
Người gọi phải cấp môi trường sạch; script không thay được việc đó.

### `$R` là thư mục CHUYÊN DỤNG, và script CÓ XOÁ trong đó

Câu *"không xoá gì cả"* ở mục vá `rm -rf` chỉ đúng cho **thư mục cài công cụ**. Script vẫn
`rm -rf "$R/kho.git"` và `rm -rf "$R/cay-kho"` — đó là hành vi có từ bản đầu, không phải hồi quy.

Các chốt symlink chỉ nhìn **thành phần con** (`$R/cong-cu`, `$R/kho.git`, `$R/cay-kho`).
Chúng **KHÔNG** nhìn `$R` chính nó, cũng không nhìn các thành phần cha.

Báo cáo lịch sử chưa kiểm chứng (historical unverified report): `$R` là symlink tới một đích **đã có** `kho.git/` và `cay-kho/` chứa dữ liệu ⇒ script
`rc=0`, dựng gói bình thường, và **hai sentinel trong hai thư mục ấy BỊ XOÁ**; sentinel ở thư mục
không liên quan còn nguyên. Gọi thẳng vào đích (không qua symlink) cho **cùng kết quả** — nên đây
là hành vi ghi đè theo TÊN đầu ra, không phải lỗi riêng do symlink.

**Hợp đồng đầu vào, nói thẳng:** người gọi phải đưa một `$R` **mới, chuyên dụng**, mà cả nó lẫn
đường dẫn cha đều đáng tin và **không chứa dữ liệu cần giữ**. Script không bảo vệ được thư mục
của người gọi.

### Nền đã báo cáo, và nền chưa báo cáo

Mọi số trong báo cáo lịch sử chưa kiểm chứng này dựa trên chạy **Linux + Bash** trong container của phiên. **Chưa có** phép đo
nào trên macOS hay Windows native. Ngoài ra, báo cáo lịch sử chưa kiểm chứng cũng ghi nhận lần dựng đầu trong container này **đỏ vì `tar` không
đổi được owner** — cần `TAR_OPTIONS` phù hợp; đó là điều kiện môi trường, không phải lỗi script.

### Chưa xử lý

- Đua (race) khi symlink bị đổi giữa hai lần kiểm.
- Quyền sở hữu đầy đủ của thư mục đầu ra.
Hai việc này thuộc phạm vi mở rộng hợp đồng đầu vào, là **packet riêng** nếu chủ kho muốn làm.
