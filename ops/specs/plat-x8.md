# ĐẶC TẢ — `PLAT-X8`: cổng TÍNH `effective_review_class`, thôi nhận lời khai

> # ⛔ ĐỪNG CẤP LEASE NEO VÀO BẢN NÀY
>
> **Điều kiện chờ ĐÃ ĐỔI: nay chờ `#238`, KHÔNG phải `#227`.** Và số chỗ sai không phải sáu — đo lại
> toàn bảng 22-08-2026 trên `origin/master` (đo lại trên `195a478d`) thì ra **mười ba**. Chỗ thứ 12 tìm được khi đi
> kiểm một việc KHÁC (`SLICE-B-C` đã land chưa); chỗ thứ 13 do **cross-review trên PR #240** chỉ ra —
> nó chỉ sai chỗ hở đúng, còn kết luận thì sai, xem cuối hộp.
>
> ## Vì sao điều kiện đổi
>
> `#227` **đã land rồi bị HOÀN NGUYÊN trong vòng 40 phút**: merge 05:16:40Z (PR #234, master
> `b88744e`) ⇒ CI master **ĐỎ trên Windows**, `gate(windows-latest)` **59/68**, chín ca mới của
> `#227` chưa ca nào từng chạy trên Windows ⇒ revert qua **PR #237**, master `2ab3560`. `#237` hoàn
> nguyên **ba tệp mã**, **giữ nguyên hồ sơ**. Việc land lại là packet **`LEASE-DANG-WINDOWS` (#238)**.
>
> Nên mọi câu *"chờ `#227` land"* ở tài liệu khác nay đọc sai: `#227` **đã** land. Thứ chưa xảy ra là
> ba tệp mã của nó **đứng được trên Windows**.
>
> ## VA CHẠM WRITE SET ĐANG SỐNG — đây là lý do cứng nhất để chưa cấp lease
>
> **BA** lease `LEASE-DANG-WINDOWS` (`exec-1` · `exec-2` · `exec-3`, packet `#238`,
> `granted_by: ducthangho`) giữ `write_set`: `.github/workflows/ops-publish-lease.yml` ·
> **`ops/lease_publish.py`** · **`ops/lease_publish_test.py`** — tức **ĐÚNG CẢ HAI** tệp `write_set`
> của `PLAT-X8`. Hạn muộn nhất **`2026-08-23T15:00:00Z`** (`exec-3`, commit `3360f6da` lúc 07:56Z).
> Cả ba nằm trên nhánh `ops/pkg-windows`, **chưa về master**. Cấp lease `PLAT-X8` bây giờ là dựng
> lại đúng cửa sổ hai writer đã làm lease lượt 1 bị RÚT.
>
> Đo 08:39:57Z trên clone đầy đủ, 159 ref, 100 tệp lease phân biệt, `KHÔNG_ĐO_ĐƯỢC = 0`:
> **10** lease còn hạn giữ `ops/lease_publish*` — 7 của `LEASE-DANG-DUNG-MOT-LAN`, 3 của
> `LEASE-DANG-WINDOWS`. Bản 3d/3e ghi *"hai lease… tới 11:00Z"*: thiếu `exec-3`, vì lúc quét nó
> chưa được đẩy. **Riêng ba lease `LEASE-DANG-WINDOWS` đã đủ đỏ** — không cần phân loại bảy cái kia.
>
> ## Mười một chỗ đã sai — không phải sáu
>
> | # | chỗ | đang ghi | sự thật đo được trên `195a478d`, clone ĐẦY ĐỦ |
> |---|---|---|---|
> | 1 | §0 bảng đo | bộ test `42/42` | **vẫn 42/42** trên master sau revert. `#227` từng nâng lên 68; `#238` sẽ nâng lại. **Đo, đừng đoán** — hộp bản 3b dự báo `58`, số thật lúc `#227` còn trên master là **68** |
> | 2 | §6 `A9` | `N >= 42` | đúng cho `195a478d`; phải nâng theo lượt `#238`, đo lại lúc ấy. **Đếm bằng `^def t[0-9]+` ra 42; bằng `^def t[0-9]+_` ra 39** — chênh ba ca hậu tố chữ (`t02b_` `t02c_` `t02d_`). Bộ test duyệt `for fn in CA` nên **42 là số ca thật chạy**; ghi kèm MẪU khi trích số, kẻo so chéo hai phiên ra `42 ≠ 39` rồi đọc thành *"#238 đã land"* |
> | 3 | §0 nền đo | `3db588c` | master nay **`195a478d`** (đã qua `2ab3560` → `99eb1d2` → đây trong ba giờ) |
> | 4 | §3 bảng va chạm | ba dòng: `#209`, `#220`, mục D | thiếu `#227` **và** `#238`; `#238` là dòng có lease SỐNG |
> | 5 | §3 câu kết | *"không lease nào đang giữ hai tệp này"* | **bị bác hai lần.** Quét đủ ref lúc 05:2xZ: 8 lease còn hạn; quét lại 05:5xZ: **9** |
> | 6 | §3 thứ tự | `PLAT-X8 → #209 → …` | thật: **`#238` → `PLAT-X8` → `#209` → `PLAT-X7` → mục D** |
> | 7 | §5 mục 9 | `t23` *"42/42 → N/N"* | số nền đúng hôm nay, nhưng nó **đi kèm** sàn A9 nên phải đổi cùng lượt |
> | 8 | §4 mục 1 · §6 `A8` | *"49 lease cũ"* | **61** tệp |
> | 9 | §8 | *"15/15 đường dẫn"*, *"10 lease khai lớp"* | **14/14** đường · **22** lease khai lớp (1 `routine` / 5 `systemic` / 16 `sensitive`); executor **17**, reviewer **44** |
> | 10 | §9 | *"0/49 tệp có `risk`"*, *"39/39 reviewer"* | **0/61** · **44/44** — và **44/44 theo CẢ HAI** cách đo (hình dạng lẫn tồn tại, trên clone đầy đủ). Bản 3d ghi *"27/44 theo tồn tại"*: **SAI**, xem mục 12 |
> | 11 | §2 | *"lần **đầu tiên** `ops/lease_publish.py` vào một `write_set` (0/49)"* | **MỆNH ĐỀ SỰ KIỆN, đã sai.** `#227` mở tệp ấy trước; nay **7/61** lease mang nó. `PLAT-X8` là packet **thứ hai** chạm nó, không phải thứ nhất |
> | 12 | cổng lease | `reviewed_sha_required` kiểm **40-hex**, tức kiểm CÁCH VIẾT | đúng về nguyên lý, quy mô nhỏ: **1** SHA giữ chỗ trong **2** `base_sha`. **KHÔNG chạm §9** — bản 3d nói nó chạm, và điều đó SAI. Xem khối riêng bên dưới |
>
> **Bốn quyết định ở §1 (Q1 thu hồi · Q2 · Q5 · Q6) và §5–§10 KHÔNG bị ảnh hưởng** — mười hai chỗ đầu
> là con số nền, bảng va chạm, một mệnh đề sự kiện và một quan sát về cổng. **Chỉ chỗ 13 khác loại:**
> nó chạm ĐIỀU KIỆN CẤP LEASE, nên đọc nó trước khi cấp lease executor.
>
> **§9 KHÔNG bị chỗ 12 bác** — bản 3d nói có, và đó là hệ quả của cùng một phép đo hỏng: hai trường
> tra không ra đều là `base_sha`, còn `reviewed_sha_required` — trường §9 thật sự dựa vào — đo được
> **44/44 tồn tại** trên clone đầy đủ. Lập luận §9 đứng nguyên.
>
> ## Chỗ thứ 12 — `reviewed_sha_required` kiểm HÌNH DẠNG, không kiểm TỒN TẠI (SỐ ĐÃ SỬA)
>
> > ⚠ **BẢN 3d/3e GHI SAI CHỖ NÀY: "29 trường / 21 tệp / 20 SHA phân biệt".** Số đúng là
> > **2 trường / 2 tệp / 1 SHA**. Hai mươi bảy trường kia tra không ra **vì clone NÔNG**, không
> > vì SHA giả. Phát hiện nhờ phiên `tra-luat-3a` báo bẫy shallow clone; đo lại sau
> > `git fetch --unshallow`. Giữ nguyên câu sai ở đây làm bằng chứng — xem "Vì sao sai" bên dưới,
> > nó đắt hơn chính con số.
>
> `ops/lease_publish.py` đòi `reviewed_sha_required` là **40-hex** — tức kiểm **cách viết**. Một
> chuỗi 40 ký tự hex bịa ra qua cổng y như SHA thật. Đo trên `195a478d`, clone **ĐẦY ĐỦ**
> (`git rev-parse --is-shallow-repository` = `false`), 61 lease:
>
> | đo | số |
> |---|---|
> | trường SHA đã kiểm (`base_sha` · `reviewed_sha_required` · `start_from_sha`) | **141** |
> | trỏ commit **không tra được** | **2** — trong **2** tệp lease, **1** SHA phân biệt |
> | SHA ấy | `0333948669bb0fdbfef8f5cbcf14a95b1b0e8bd4`, ở `base_sha` của `slice-b-c-review-1-codex-20260821` và `tri-thuc-review-1-codex-20260821` |
>
> Nó là **SHA giữ chỗ** thật: GitHub API trả `No commit found for SHA`, và trong kho có một commit
> **thật** trùng đúng **8** ký tự đầu rồi khác hẳn — `03339486`**`bc44d533…`** (merge PR #212). Ai có
> SHA viết tắt 8 ký tự rồi điền nốt cho đủ 40 sẽ ra đúng hình dạng này.
>
> Finding vẫn đứng, chỉ nhỏ hơn **mười bốn lần** so với con số bản 3d: cổng kiểm hình dạng thì một
> `base_sha` không tồn tại vẫn qua. Nhưng **2 ≠ 29**, và cách con số ấy phình lên mới là bài học.
>
> **Và nó KHÔNG chạm §9.** Cả hai trường hỏng là `base_sha`; `reviewed_sha_required` đo được **44/44
> tồn tại**. Bản 3d khai chỗ này *"chạm một LẬP LUẬN của §9"* và ghi *"17/44 lease reviewer có
> `reviewed_sha_required` không tra được"* — **cả hai là tạo tác của clone nông**. Câu *"exact head
> có thật và neo ngay trong lease"* ở §9 đứng nguyên, đo cả hình dạng lẫn tồn tại.
>
> ## Vì sao bản 3d sai — ba lỗi chồng nhau, cái sau che cái trước
>
> **1. `git cat-file -e` NÓI DỐI trên clone nông.** Container đo bản 3d có
> `is-shallow-repository = true`. Nông cắt **LỊCH SỬ**, nên commit cũ không có trong clone và
> `cat-file` trả "không có" cho SHA hoàn toàn hợp lệ.
>
> **2. Tôi tự loại giả thuyết ấy — và loại SAI.** Bản 3d ghi *"'chưa fetch đủ' — fetch **toàn bộ**
> `refs/heads/*`: 158 ref + 35 tag. Số **không đổi**."* Câu ấy đúng về **ref** và vô nghĩa về **lịch
> sử**: `--depth` cắt độ sâu, không cắt số ref, nên fetch thêm ref không kéo về commit cũ nào. **Đủ
> REF không phải đủ LỊCH SỬ.** Phép đo duy nhất phân biệt được là `git rev-parse
> --is-shallow-repository`, và bản 3d chưa từng chạy nó.
>
> **3. Bằng chứng thứ ba là BỊA, và tôi không biết.** Bản 3d viết: *"một cái lộ hẳn:
> `18da1da6a07a3e6e4e3e8f0e0e0e0e0e0e0e0e0e` — mẫu lặp tới hết chuỗi"*. Script của tôi chỉ in **12
> ký tự đầu**; **28 ký tự còn lại do chính tôi gõ** khi dựng lời gọi API, rồi tôi đọc kết quả 404
> thành bằng chứng về dữ liệu. `base_sha` **thật** của `wp55-r4-exec-1-claude-20260816` là
> `18da1da6a07a`**`b2c86d716cef1d74ff2cd0e3218a`** — **tra được**, merge PR #129. Cái "mẫu lặp" ấy
> chưa bao giờ tồn tại trong kho.
>
> Chốt, và đây là phần đáng giữ hơn con số:
>
> - **Đo `--is-shallow-repository` TRƯỚC mọi kết luận dạng "không tồn tại".** Nông ⇒
>   `git fetch --unshallow origin '+refs/heads/*:refs/remotes/origin/*'` rồi mới đo. In số ref **và**
>   trạng thái shallow cạnh kết luận.
> - **Loại một giả thuyết bằng phép đo TRẢ LỜI ĐÚNG NÓ.** Tôi loại *"chưa fetch đủ"* bằng số ref —
>   một con số không liên quan tới điều đang hỏi. Một phép đo sai đối tượng nguy hiểm hơn không đo,
>   vì nó để lại cảm giác đã kiểm.
> - **Chỉ đưa vào lời gọi cái ĐỌC RA TỪ DỮ LIỆU.** Tự điền phần thiếu của một định danh rồi coi kết
>   quả là bằng chứng thì đó là bằng chứng về thứ mình vừa gõ. Script in rút gọn ⇒ sửa script để in
>   đủ, đừng lấp bằng tay.
>
> **Chưa quyết chỗ chữa, và CỐ Ý chưa quyết.** Thêm phép kiểm tồn tại vào cổng là mở `write_set` của
> `PLAT-X8` cho một mục Issue #225 không đặt ra. Với con số thật (**2**), việc ấy càng không gấp.
> Ai mở packet cho nó phải trả lời trước: cổng chặn **lease mới** hay **mọi lease**; ba trạng thái
> (`có` · `không` · **`không đo được`**) ánh xạ ra `rc` nào; và **`không đo được` phải bao gồm ca
> clone nông**, vì đó chính là ca đã lừa được lượt đo đầu tiên.
>
> ## Việc phải làm, đúng thứ tự
>
> Chờ **`#238`** land (ba tệp mã đứng được trên Windows, có `run_id` của lượt `workflow_dispatch`
> xanh cả hai job trên exact head) → **đo lại toàn bảng §0**, không vá lẻ → sửa mười ba chỗ → đóng
> băng **bản 4** → quét lease trên **mọi** ref rồi mới cấp lease neo băm bản 4. Prompt
> `ops/prompts/plat-x8-exec-1-codex-20260821.md` giữ lại nhưng phải neo lại băm trước khi dùng.
>
> ## Chỗ thứ 13 — lease `codex` cho packet `sensitive` là NGOẠI LỆ CÓ ĐIỀU KIỆN, và KHÔNG cổng nào canh
>
> Chuỗi trên nói *"giữ prompt executor `codex`, chỉ neo lại băm"*. Đúng — **nhưng chưa đủ**, và chỗ
> thiếu là một điều kiện của `ADR-0045` mà **không cổng nào kiểm**, nên nó phải được kiểm bằng tay.
>
> `PLAT-X8` là **`sensitive`**. `ADR-0041:8` và `docs/PROTOCOL_DA_PHIEN.md:559` đều giới hạn Codex
> Executor ở packet `routine`/`systemic` nhỏ. Đọc tới đó rồi dừng thì kết luận *"phải đổi executor
> sang Claude"* — **và kết luận ấy SAI**, vì chỗ có thẩm quyền là **`ADR-0045`** (Accepted 21-08,
> chủ kho phê duyệt Q8), sinh ra từ **đúng tình huống này** với `PLAT-X5`:
>
> > *Codex được làm Executor cho một packet `sensitive` **chỉ khi** chủ kho chỉ định tường minh trong
> > lease, reviewer khác nền, và có human readback trước land. Mỗi lần dùng phải để lại vết đọc được
> > bằng máy: lease khai `review_class` và khai rằng đây là ngoại lệ theo §2.*
>
> Nên đường đúng **không** phải đổi executor mà là **khai đủ vết**. Đo lease đã RÚT
> (`plat-x8-exec-1-codex-20260821`, commit `3c21bcd8`) trên bốn điều kiện ấy:
>
> | điều kiện `ADR-0045` | lease đã rút |
> |---|---|
> | chủ kho chỉ định tường minh trong lease | **CÓ** — `granted_by: ducthangho`, `granted_on_instruction` ghi *"chọn nền `codex` + reviewer `claude`"* |
> | reviewer khác nền | **CÓ** — `reviewer: claude`, `provider: openai_codex` |
> | lease khai `review_class` | **CÓ** — `review_class` và `effective_review_class` đều `sensitive` |
> | **khai rằng đây là NGOẠI LỆ theo §2** | **KHÔNG** — `grep '0045\|ngoại lệ'` trong lease, đặc tả và prompt đều ra **0** |
> | human readback trước land | chưa tới lúc; phải có trước land |
>
> **CHỐT ẤY CHƯA CÓ CỔNG — đây là preflight THỦ CÔNG, đừng đọc thành bằng chứng cổng.** `ADR-0045`
> *mô tả* cách cưỡng chế (*"`review_class` vào danh sách trường bắt buộc; vắng ⇒ `sensitive`;
> `sensitive` cộng `executor: codex` mà không có khối ngoại lệ do chủ kho ký ⇒ thoát khác 0"*), nhưng
> đo trên `195a478d`: `ops/lease_publish.py` có **0** chỗ nhắc `review_class`, **0** nhắc `0045`,
> **0** nhắc *"ngoại lệ"*; và `docs/PROTOCOL_DA_PHIEN.md:1090` xếp `ADR-0045` đúng ô **`0 cổng`**.
>
> Nên lease lượt 2 thiếu khối ngoại lệ **sẽ KHÔNG bị chặn** — nó chỉ sai luật mà không ai bắt. Đó là
> lý do phải nêu ở đây: **người cấp lease phải tự kiểm bằng tay trước khi cấp.** Lời hứa fail-close
> cùng ca phản chứng thuộc về packet nào thật sự cài chốt ấy, không phải packet này — `PLAT-X8` còn
> chưa có lease thì không thể tự cài cổng chặn chính lease của mình.
>
> *Bản 3e viết câu này thành "⇒ thoát khác 0", tức khai một cổng CHƯA TỒN TẠI. Cross-review lượt 2
> bắt được. Cùng hình dạng **A** — "lời khai rộng hơn phép đo" — mà `#238` đếm lên 7, và là lần thứ
> hai trong phiên này. Gốc: tôi đọc chữ "Cưỡng chế:" trong ADR thành "đã cưỡng chế". **Một ADR mô tả
> chốt cần có; chỉ mã mới nói chốt đã có.** Muốn biết thì `grep` mã, đừng đọc ADR.*
>
> Ghi ra đây vì cùng họ với mọi thứ trong hộp này: **`ADR-0041` là chỗ tiện tay, `ADR-0045` là chỗ
> kết luận được ghi.** Một lượt cross-review đã dừng ở `ADR-0041` và đề xuất đổi executor — đề xuất
> ấy phá một quyết định chủ kho đã ký, chỉ vì hỏi thiếu một tệp.
>
> ## Bốn thứ lượt đo 22-08 trả giá mới biết — đọc trước khi đo lại
>
> 0. **`git cat-file -e` NÓI DỐI trên clone NÔNG, và không có gì cảnh báo.** Container đo bản 3d có
>    `is-shallow-repository = true`; nông cắt **lịch sử**, nên `cat-file` trả "không có" cho SHA hợp
>    lệ. Nó đẻ ra con số **29** ở chỗ 12 (thật là **2**) và mệnh đề sai *"chỗ 12 chạm §9"*. Fetch
>    thêm **ref** không cứu — `--depth` cắt độ sâu chứ không cắt số ref, nên *"đã fetch 158 ref"*
>    là phép đo **sai đối tượng**. Chốt: đo `git rev-parse --is-shallow-repository` TRƯỚC mọi kết
>    luận dạng *"không tồn tại"*; `true` ⇒ `git fetch --unshallow` rồi mới đo; in **cả** số ref
>    **và** trạng thái shallow cạnh kết luận. Phiên `tra-luat-3a` chỉ ra bẫy này.
>
>    **Nhưng `--is-shallow-repository` MỘT MÌNH chưa đủ** — chính `tra-luat-3a` đính chính tiếp: một
>    kho **đã gỡ nông, refspec rộng** vẫn thiếu ref được, vì `for-each-ref` **đọc bộ đệm cục bộ**
>    chứ không hỏi máy chủ. Refspec là luật cho những lần fetch SAU, không phải lời hứa đã fetch.
>    Phép canh đúng là so **HAI NGUỒN**:
>
>    ```bash
>    git ls-remote --heads origin        | wc -l   # máy chủ CÓ những ref nào
>    git for-each-ref refs/remotes/origin | wc -l   # tôi đang GIỮ bản sao nào
>    ```
>
>    Lệch ⇒ **`KHÔNG_ĐO_ĐƯỢC`**, không phải *"không có"*. Thiếu mạng để chạy `ls-remote` cũng ra
>    `KHÔNG_ĐO_ĐƯỢC`. Đo trên container này 08:5xZ: **159 / 159**, không lệch. Lệnh chữa không đổi —
>    `git fetch --unshallow origin '+refs/heads/*:refs/remotes/origin/*'` bịt cả ba cơ chế (refspec
>    hẹp do `--depth` kéo theo `--single-branch` · độ sâu bị cắt · bộ đệm chưa fetch).
>
> 1. **Tên trường hạn lease là `lease_expires_at_utc`.** Lượt quét đầu đoán `het_han`/`expires_at`/
>    `deadline`, nhận `None` cho **cả 42** tệp, và `None` đọc thành *"không có hạn"* thì bảng ra
>    **0 lease còn hạn** — đúng cái kết luận sai mà hộp này sinh ra để chặn.
> 2. **Phép đo ĐÚNG vẫn chết theo thời gian.** Quét đủ **99** ref lúc 05:2xZ ra *"0 lease chồng lấn,
>    cấp lease được"*. **Hai mươi phút sau** nhánh `ops/pkg-windows` xuất hiện với đúng một lease
>    chồng lấn ⇒ kết luận đảo chiều. Quét đủ ref là **cần**, không **đủ**: phải quét **ngay trước khi
>    cấp**, và số ref phải đo chứ đừng chép (98 → 99 trong một lượt làm việc).
> 3. **`actionlint` không có `shellcheck` là phép đo YẾU HƠN CI.** Container này thiếu `shellcheck`,
>    nên `actionlint` ở đây xanh trong khi CI đỏ — đúng hình dạng **A** *"lời khai rộng hơn phép đo"*
>    mà `#238` đếm lên **7**. Ai báo *"actionlint rc=0"* phải nói kèm có `shellcheck` hay không.
>
> *Hộp này tồn tại vì trước đó đặc tả — thứ DUY NHẤT có thẩm quyền, thứ lease neo vào — không mang
> dấu hiệu nào cho biết các con số của nó sắp chết. Bản 3b liệt kê sáu chỗ; đo lại ra mười một; đi
> kiểm một việc khác ra chỗ thứ mười hai; một lượt cross-review ra chỗ thứ mười ba. **Bốn nguồn khác
> nhau cho cùng một tệp** — không nguồn nào trong đó là "đọc lại danh sách".
> **Một danh sách liệt kê không thay được một lượt đo lại toàn bảng** — cùng hình dạng với "danh sách
> CẤM không bao giờ đủ".*


Đặc tả này ĐÓNG BĂNG bằng băm. Lease neo vào `spec_sha256`. Sửa nội dung ⇒ băm đổi ⇒ lease trỏ
vào thứ không còn tồn tại, phải đi qua bản sửa đổi mới. Soạn bằng skill `soan-spec`, 21-08-2026.

**BẢN ĐÓNG BĂNG THỨ BA (+ hộp cảnh báo, 22-08-2026).** Hai lượt cross-review (`codex`), **bốn P1**, và người giữ kho
chọn SỬA đặc tả ở cả hai lượt. Hộp cảnh báo đã qua **bốn** lượt sửa (`3b` → `3c` → `3d` → `3e` → `3f`)
mà **nội dung yêu cầu vẫn không đổi một chữ** — thứ trôi là nền đo, không phải đặc tả.

| bản | băm | kết cục |
|---|---|---|
| 1 | `9cb54a2e4e7c…` | 2 P1 ở lượt 1 (neo `c9a1b4e90d`) — hết hiệu lực |
| 2 | `b88c53dfd211…` | 2 P1 nữa ở lượt 2 (neo `3bafef75d6`), **cả hai** đánh vào đúng đường kế thừa — hết hiệu lực |
| 3 | `328a74facb84…` | Q1 **THU HỒI**: đường kế thừa bị gỡ, không vá tiếp — §10 |
| 3b | `308d0cf44fc1…` | thêm hộp ⛔ cảnh báo, liệt kê **sáu** chỗ sai, điều kiện chờ = `#227` land — hết hiệu lực khi `#227` land **rồi bị revert** |
| 3c | `182ea7621d02…` | sửa hộp ⛔: điều kiện chờ đổi `#227` → **`#238`**; sáu chỗ sai đo lại thành **mười một**; ghi va chạm lease SỐNG của `#238` |
| 3d | `f7f8e6209e4f…` | thêm chỗ thứ 12 — **nhưng với con số SAI** (`29` trường / `21` lease; thật là `2`/`2`, xem `3f`) và một mệnh đề sai (*"chạm §9"*). Cả hai do clone NÔNG |
| 3e | `ce14fb0b75e4…` | thêm chỗ thứ 13 (`ADR-0045`: lease `codex` cho packet `sensitive` là ngoại lệ CÓ ĐIỀU KIỆN) — hết hiệu lực khi chỗ 12 bị đo lại |
| 3f | `497c68360de7…` | SỬA chỗ 12: `29 trường / 21 tệp` → **`2/2`** — con số cũ là tạo tác của **clone NÔNG**, không phải SHA giả; mệnh đề *"chỗ 12 chạm §9"* cũng sai (`reviewed_sha_required` **44/44** tồn tại). Cộng: nền đo → `195a478d`, va chạm → **3** lease tới `23-08T15:00Z`, bài học **0**. Hết hiệu lực ở cross-review lượt 2 |
| 3g | bản này | **Vá 3 finding của cross-review lượt 2.** Nặng nhất: bản 3e khai *"thiếu khối ngoại lệ ⇒ thoát khác 0"* — **cổng ấy KHÔNG TỒN TẠI** (`lease_publish.py` có 0 chỗ nhắc `review_class`/`0045`; §20 xếp `ADR-0045` là `0 cổng`), nên đổi thành **preflight THỦ CÔNG**. Cộng: bảng task prompt → `3f`/mười ba/`15:00Z`; handoff ghi `#230` đã merge; bài học 0 thêm phép so **hai nguồn** (`ls-remote` vs `for-each-ref`) vì `--is-shallow-repository` một mình chưa đủ |

Bốn phát hiện trên **một** đường là dấu hiệu sai ở QUYẾT ĐỊNH GỐC chứ không ở các bản vá. Các bản
trước ở lại trong lịch sử `git` làm bằng chứng, **không** làm bản dùng được.

| khoá | giá trị |
|---|---|
| `packet_id` | `PLAT-X8` |
| `packet_issue` | 225 |
| `nguon_cap_viec` | nợ **#1**: caveat `chot-tinh-class-van-KHONG-TON-TAI` trong `ops/reviews/plat-m4-human-audit-ducthangho-verdict.receipt.yaml`, và caveat `packet-bi-phan-class-SAI` trong `ops/reviews/plat-m4-review-3-claude-verdict.receipt.yaml` |
| `review_class` | **`sensitive`** — chạm `ops/lease_publish.py`, tức `review/land authority` **và** `gate lifecycle`, hai mục §8:572 gọi đích danh. Không có đường đọc nào khác |
| `hinh_dang_ke_thua` | xem §7 — **KHÔNG** `khong_ap_dung` |

## 0. Sự thật chịu tải, và đơn vị của từng con số (L1)

Đo trên `origin/master` = `3db588c`, 21-08-2026.

| phép đo | kết quả | **đơn vị** |
|---|---|---|
| `rg review_class ops/lease_publish.py` | 0 | số dòng khớp |
| `rg effective_review_class ops/lease_publish.py` | 0 | số dòng khớp |
| `rg schema_version ops/lease_publish.py` | 0 | số dòng khớp |
| `rg review_class ops/lease_publish_test.py` | 0 | số dòng khớp |
| lease trong `ops/leases/` | 49 | số tệp `.yaml` |
| lease khai `review_class` | 10 | số tệp |
| lease khai `effective_review_class` | 0 | số tệp |
| trong 10 tệp ấy: `routine` / `systemic` / `sensitive` | 1 / 5 / 4 | số tệp |
| lease **executor** (có `write_set` không rỗng) | 10 | số tệp |
| lease **reviewer** (không có `write_set`) | 39 | số tệp |
| đường dẫn phân biệt trong `write_set` của mọi lease | 15 | số đường dẫn |
| trong đó `ops/lease_publish.py` | 0 | số lần xuất hiện |
| bộ test tại `3db588c` | 42/42 | số ca đạt / số ca chạy |
| tám lần chạm gần nhất tới `ops/lease_publish*` | +50 … +187 | số dòng thêm mỗi commit |

**Mâu thuẫn làm bằng chứng gốc** — hai lease executor, **cùng `write_set`**
(`.claude/dev/launcher.py` + `.claude/dev/launcher_test.py`), khai hai lớp khác nhau:
`ag-t0-01b-exec-1-antigravity-20260821` = `sensitive`; `plat-m4-exec-2-claude-20260821` = `systemic`.
§8:572 gọi đích danh `launcher`. Bốn lease reviewer của `PLAT-M4` chép tiếp `systemic` ⇒ **5 tệp**
lease mang một lời khai sai.

**Bạn giả, ghi để người sau khỏi `rg` rồi kết luận nhầm:** `ops/chatgpt_review/build_bundle.py:165`
có chuỗi `effective_review_class`, nhưng đó là **tên biến cục bộ** — chỉ kiểm enum rồi **chép** giá
trị đã khai vào manifest, không tính gì từ `write_set`. Không liên quan tới trường của §8.

## 1. Bốn quyết định đã chốt (người giữ kho, 21-08-2026, in-session) — **Q1 sau đó bị THU HỒI**

| # | quyết | hệ quả kỹ thuật |
|---|---|---|
| ~~Q1~~ | ~~reviewer lease **kế thừa** lớp từ lease executor~~ — **THU HỒI 21-08-2026** | cổng **KHÔNG** quét `ops/leases/`; reviewer `schema_version >= 2` ⇒ `sensitive` vô điều kiện. Lý do ở §10 |
| Q2 | fail-closed đúng chữ §8:569 | không suy được ⇒ `sensitive` |
| Q5 | neo forward-only bằng **`schema_version: 2`** | cổng phải bắt đầu đọc `schema_version` (nay đọc 0 dòng) |
| Q6 | không tìm thấy lease executor ⇒ **`sensitive`** | thắt thứ tự cấp lease: executor trước, reviewer sau |

**Vì sao Q5 KHÔNG neo theo `leased_at_utc`:** mốc ngày phải đứng trên một trường **không cổng nào
kiểm**. Chốt *"timestamp không ở tương lai"* thuộc gói spec-gate (mục D), **chưa xây** — và đã tồn
tại một lease khai `leased_at_utc: '2026-08-22T02:05:00Z'`, tức tương lai, hợp lệ với cổng hiện tại.

**Đường thứ ba đã xét và BÁC:** *"có khai thì kiểm, không khai thì tha"*. Fail-open, và nó vô hiệu
hoá chính packet — `PLAT-M4` **có** khai, chỉ khai sai.

## 2. write_set

- `ops/lease_publish.py`
- `ops/lease_publish_test.py`

**Hai tệp, không đường dẫn nào khác.** Trần `sensitive` của
`docs/adr/0044-nguong-kich-thuoc-packet-theo-do-luong.md` là ≤3 tệp / ≤300 dòng thêm; chừa một suất
là cố ý, để lượt vá sau verdict không phải xin mở rộng write set.

Đây là lần **đầu tiên** `ops/lease_publish.py` vào một `write_set` (đo: 0/49). Việc mở tệp ấy đã được
người giữ kho duyệt cho gói cưỡng chế kế tiếp (ADR-0044, Q4). Nói thẳng vì cần nói:
`ops/THAM_DINH_CHUNG_CLAUDE_CODEX_KE_HOACH.md:96` từng **cấm** mở tệp ấy cho `W0-R2` — đây là duyệt
MỚI cho mục đích KHÁC, có ghi, không phải lờ đi lệnh cấm cũ.

Lease, prompt và đặc tả này nằm trên nhánh riêng, **không** nằm trên nhánh packet — đã trả giá một
finding P1 vì chuyện đó ở `#195`.

## 3. Va chạm write set — đã đo, xử bằng THỨ TỰ

| packet | trạng thái | đòi | va |
|---|---|---|---|
| `PLAT-X6` (#209) | `state:ready`, **0 lease** | `ops/NO_KY_THUAT.md` + `ops/lease_publish_test.py` | CÓ |
| `PLAT-X7` (#220) | `proposed`, chưa spec, **0 lease** | `ops/lease_publish.py` + `ops/lease_publish_test.py` | CÓ |
| mục **D** spec-gate | chưa mở Issue | `ops/lease_publish*` | CÓ |

Mười lease từng chạm `ops/lease_publish_test.py` đều thuộc `PLAT-X4`/`PLAT-X5`/`SLICE-B-C`, **đã
land**. Nên không lease nào đang giữ hai tệp này ⇒ va chạm là **theo kế hoạch**, không theo lease
đang chạy. Thứ tự chốt: **`PLAT-X8` → `#209` → `PLAT-X7` → mục D**.

## 4. ngoai_pham_vi — CỐ Ý không làm

1. **Không sửa 49 lease cũ.** Forward-only theo Q5. `t23` đòi **mọi** lease thật phải qua cổng; áp
   ngược lại là 49 tệp đỏ cùng lúc. Năm lease sai lớp của `PLAT-M4` **đã** có bản đính chính —
   `ops/DINH_CHINH_REVIEW_CLASS_PLAT_M4.md` — nên hồ sơ đã đúng, chỉ tệp lease giữ nguyên.
2. **Không nới bảng phân loại quá thứ §8 nói NGUYÊN VĂN.** Xem §8 của đặc tả này; nới bảng phải có
   bằng chứng riêng cho từng đường dẫn, và đó là packet khác.
3. **Không đo danh tính model** — đó là `PLAT-X7` (#220), khai `depends_on: [PLAT-X8]`.
4. **Không dựng chốt `spec_path`/`spec_sha256`/timestamp** — đó là mục D.
5. **Không đụng `ops/NO_KY_THUAT.md`.** Nó thuộc write set của `#209`. Nợ sinh ra từ packet này ghi
   vào biên nhận, không vào sổ nợ, cho tới khi `#209` chốt.

## 5. muc_tieu — mỗi dòng chiếu vào một đường dẫn ở `write_set` (L2)

1. Hằng `RC_LOP = 10` (mã 0/2/4/6/8/9 đã dùng hết, đo được ở dòng 38–43). → `ops/lease_publish.py`
2. Bảng `_BANG_LOP`: **DANH SÁCH CHO PHÉP** ánh xạ tiền tố đường dẫn → `routine`/`systemic`. Mọi
   đường dẫn **không khớp** mục nào ⇒ `sensitive`. Không có danh sách cấm. → `ops/lease_publish.py`
3. `_tinh_lop_tu_write_set(write_set)` trả lớp **CAO NHẤT** trong tập
   (`sensitive` > `systemic` > `routine`); `write_set` rỗng hoặc thiếu ⇒ `sensitive`.
   → `ops/lease_publish.py`
4. Tiền tố `planned:` được **cắt bỏ trước khi tra bảng**. Không cắt thì mọi đường dẫn `planned:` rơi
   vào nhánh mặc định — fail-closed đúng chiều nhưng vì **lý do sai**, và bảng thành vô dụng với
   đường dẫn chưa tồn tại. → `ops/lease_publish.py`
5. Lease `role: executor`, `schema_version >= 2`: đòi `write_set` không rỗng; tính lớp; đòi lease khai
   `effective_review_class` **BẰNG** `max(review_class đã khai, lớp tính được)`. Khai thấp hơn ⇒
   `RC_LOP`. Đây là chỗ cưỡng chế §8:567 *"Executor không được hạ lớp."* → `ops/lease_publish.py`
6. Lease `role: reviewer`, `schema_version >= 2`: `effective_review_class` = **`sensitive`, vô điều
   kiện**. Cổng **KHÔNG** quét `ops/leases/`, **KHÔNG** tra lease executor, **KHÔNG** kế thừa gì.
   Lease reviewer khai thấp hơn `sensitive` ⇒ `RC_LOP`. → `ops/lease_publish.py`

   **ĐÂY LÀ THU HỒI Q1, quyết định của người giữ kho sau cross-review lượt 2 — xem §10.** Bản trước
   của mục này (tra bằng bộ định danh) đã ăn thêm hai P1 ở lượt 2, cả hai đánh vào **đúng** đường kế
   thừa. Không vá nữa: bốn phát hiện trên cùng MỘT đường trong hai lượt là dấu hiệu sai ở QUYẾT ĐỊNH
   GỐC, không ở các bản vá — doctrine "đếm hình dạng lỗi, đừng chỉ đếm lỗi". Cả lớp rủi ro chết theo
   KIẾN TRÚC: không tra lease nào thì không có bộ định danh để giả mạo, không có tiền nhiệm để thừa,
   và không có nhánh "không thấy thì…" để rẽ nhầm.

7. Lease `schema_version: 1` hoặc thiếu trường: **BỎ QUA** chốt lớp, `rc` không đổi. Nếu nó khai
   `leased_at_utc` sau `2026-08-21T00:00:00Z` thì in **CẢNH BÁO** ra stderr, **không** đổi `rc`.
   → `ops/lease_publish.py`
8. Ca `rXX_` khoá từng mục 2–7, và bảng đột biến khoá chúng. → `ops/lease_publish_test.py`
9. `t23` (mọi lease thật phải qua) vẫn **42/42 → N/N**, không tụt số ca, sau khi thêm chốt.
   → `ops/lease_publish_test.py`

## 6. nghiem_thu — mỗi tiêu chí nêu phép đo làm nó ĐỎ (L3)

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| A1 | lease executor `schema_version: 2`, `write_set: [.claude/dev/launcher.py]`, khai `review_class: systemic` + `effective_review_class: systemic` ⇒ `rc == RC_LOP` | đột biến: đổi nhánh mặc định của `_tinh_lop_tu_write_set` từ `sensitive` sang `systemic` ⇒ ca ĐỎ |
| A2 | **phản chứng của `PLAT-M4`**: dựng lại đúng nội dung `plat-m4-exec-2-claude-20260821` với `schema_version: 2` ⇒ `rc == RC_LOP`; đổi đúng một trường thành `sensitive` ⇒ `rc == 0` | đột biến: bỏ so sánh `max(khai, tính)` chỉ còn kiểm enum ⇒ ca ĐỎ |
| A3 | lease reviewer `schema_version: 2` ⇒ lớp hiệu lực `sensitive`, **kể cả khi** `ops/leases/` có một executor `routine` khớp mọi trường định danh | đột biến: dựng lại BẤT KỲ đường kế thừa nào (tra `packet_id`, tra bộ định danh, đọc lease khác) ⇒ ca ĐỎ. Ca này khoá **sự VẮNG MẶT** của một cơ chế, nên nó phải đỏ khi cơ chế ấy quay lại |
| A4 | lease reviewer khai `effective_review_class: routine` (hoặc `systemic`) ⇒ `RC_LOP` | đột biến: bỏ chốt lớp cho vai reviewer ⇒ ca ĐỎ |
| A13 | **`ops/leases/` KHÔNG được đọc trên đường reviewer** — dựng thư mục lease chứa một tệp YAML **hỏng cú pháp**; lease reviewer vẫn ra `sensitive`, `rc` không đổi | đột biến: thêm bất kỳ lượt đọc thư mục nào vào đường reviewer ⇒ ca ĐỎ (tệp hỏng sẽ ném). Đây là phép đo HÀNH VI cho "không quét", không phải lời hứa trong chú thích |
| A14 | **vế DƯƠNG phải sống**: với `_BANG_LOP` được nới TẠM trong ca test (thêm `docs/** → routine`), một lease **executor** `write_set: ['docs/x.md']` ⇒ `routine`, `rc == 0` | không có ca này thì mọi bản vá "cho chắc" biến cổng thành máy trả `sensitive` mà không ai đo được — đúng cảnh báo của cross-review lượt 1. Đột biến: ép `_tinh_lop_tu_write_set` luôn trả `sensitive` ⇒ ca ĐỎ |
| A5 | `write_set: ['planned:ops/chay_lease_publish_test.sh']` phân đúng như bản không có tiền tố | đột biến: bỏ dòng cắt `planned:` ⇒ ca ĐỎ |
| A6 | `write_set: []` và lease thiếu hẳn `write_set` ⇒ cả hai ra `sensitive` | đột biến: coi rỗng là `routine` ⇒ ca ĐỎ |
| A7 | **đột biến NỚI BẢNG**: thêm `.claude/dev/launcher.py → routine` vào `_BANG_LOP` ⇒ ca đích ĐỎ | không có đột biến này thì không biết ca đang đo **bảng** hay đo thứ khác (doctrine `v1.36.68`) |
| A8 | lease `schema_version: 1` y hệt A2 ⇒ `rc == 0`, và stderr **có** chuỗi cảnh báo | đột biến: bỏ chốt `schema_version`, áp cho mọi lease ⇒ ca ĐỎ **và** `t23` ĐỎ (49 lease cũ) |
| A9 | `python3 ops/lease_publish_test.py` ⇒ `rc=0`, `N/N` **hai số bằng nhau**, `N >= 42` | tụt số ca hoặc hai số lệch ⇒ ĐỎ |
| A10 | mọi đột biến A1–A8 chạy trên **BẢN SAO CẢ CÂY** trong thư mục tạm, mỗi đột biến một tên tệp riêng | ghi vào tệp thật rồi khôi phục trong `finally` là bom hẹn giờ đã trả giá; bản sao một tệp làm `HERE` sai và số đo vô nghĩa |
| A11 | `actionlint .github/workflows/*.yml` ⇒ `rc=0` cả 5, **fail-close khi thiếu công cụ** | thay bằng PyYAML ⇒ coi như KHÔNG ĐO ĐƯỢC, ĐỎ |
| A12 | `ready to review` = CI xanh trên **exact head** qua `workflow_dispatch`, **cả hai** job `success` | *"PR xanh"* KHÔNG đủ: `ci.yml` chỉ chạy `ubuntu` cho PR thường |

## 7. hinh_dang_ke_thua (L4)

**Hình dạng kế thừa:** *nhận LỜI KHAI thay cho PHÉP ĐO* — biến thể của *"đếm sự CÓ MẶT thay vì
KHẢ NĂNG"*.

**Bộ đếm chép sang: 6 → packet này là lần thứ 7 — và trong CHÍNH quá trình soạn nó, lần thứ 8.**
Bản đóng băng 1 và 2 định thay lời khai bằng phép đo, nhưng đường kế thừa của mục tiêu 6 lại đi
SUY lớp từ **một tệp lease khác** — tức vẫn là lời khai, chỉ dời sang tệp bên cạnh. Hình dạng cũ
tái phát ngay bên trong bản vá cho chính nó. Đó là lý do §10 gỡ hẳn thay vì siết tiếp. Sáu lần đã ghi, nguồn `#220`:
`which(gh)` · `rest-chung` · `gh auth status` · `mcp-endpoint` · `shutil.which` trong `DUNG_DUOC` ·
đếm cái vỏ công cụ thay vì model đang chạy.

**Khác biệt của lần thứ bảy, và là lý do nó đáng một packet:** sáu lần trước là lỗ **chưa gây hại**.
Lần này đã gây hại, đếm được — **5 tệp** lease sai lớp, **3** lượt review chạy dưới lớp sai, một
packet `sensitive` suýt land bằng `same_provider_approved`.

**KHÔNG kế thừa** bộ đếm `hinh_dang_lap: 3` trong
`ops/reviews/plat-m4-review-2-codex-verdict.receipt.yaml` — đó là hình dạng **khác** (lời gọi review
hỏng vì cách dựng sandbox/bundle). Gộp hai bộ đếm khác hình dạng là làm hỏng chính chốt đếm.

**Trả lời thẳng câu doctrine bắt phải hỏi ở lần thứ ba trở đi** — *"có nên làm việc này không"*, chứ
không phải *"vá thế nào"*: **không nên tiếp tục SUY lớp review từ lời khai.** Packet này bỏ hẳn đường
suy ấy và thay bằng phép TÍNH từ `write_set`. Bộ đếm đang được **trả lời**, không bị lờ.

## 8. Bảng phân loại — thứ packet này KHÔNG dám tự quyết, và con số làm ta phải nói ra

`_BANG_LOP` chỉ được seed bằng thứ §8:572 nói **NGUYÊN VĂN**: `workflow/CI authority` ·
`security/credential boundary` · `dispatcher/reconciler` · `review/land authority` ·
`launcher hoặc gate lifecycle` · `migration dữ liệu và LIVE adapter`.

**Hệ quả, đã đo và phải nói thẳng: 15/15 đường dẫn** từng xuất hiện trong `write_set` của mọi lease
đều ra **`sensitive`** dưới bảng seed ấy — hoặc vì §8 gọi đích danh, hoặc vì rơi vào nhánh mặc định.
Trong 10 lease khai lớp, **6 sẽ bị NÂNG** (1 `routine` + 5 `systemic`), 4 giữ nguyên.

Đây **không** phải lỗi cài đặt; đó là điều Q2=(a) nghĩa là. Nhưng nó có giá vận hành thật: §8 mặc
định *"Codex chỉ nhận Packet `routine`/`systemic` nhỏ"* và *"hết quota mà chưa có human thì pause"* —
mà dưới bảng seed, **không packet nào của kho là `routine`/`systemic`**.

Cần lặp lại vì dễ đọc nhầm: **cổng này mua tính NHẤT QUÁN, không mua tính ĐÚNG của bảng.** Nó chứng
minh *lớp hiệu lực khớp bảng*; nó **không** chứng minh *bảng khớp §8*. Một dòng sai trong bảng là một
lớp sai được cổng **xác nhận** — tệ hơn không có cổng, vì nó biến lời khai sai thành lời khai đã-qua-cổng.
Đó là lý do bảng là danh sách **CHO PHÉP** và lý do A7 tồn tại.

Nới bảng là **ngoài phạm vi** (§4.2): mỗi đường dẫn muốn xuống `routine`/`systemic` phải có lập luận
riêng đối chiếu §8, và đó là quyết định của người giữ kho, không phải của phiên thi hành.

## 9. chua_do_duoc — nói thẳng, không giấu sau chữ "có thể"

1. **Bảng đúng hay không thì packet này không đo được.** Xem §8. Không có phép thử nào trong write
   set biến một dòng bảng sai thành ĐỎ.
2. ~~**Hai cái giá của Q6 chưa đo hết.**~~ **HẾT HIỆU LỰC sau khi thu hồi Q1 (§10).** Cả hai cái
   giá cũ đều mọc từ việc TRA CỨU lease executor: (a) thứ tự cấp lease bị thắt, (b) packet do người
   giữ kho tự làm executor không bao giờ có lease executor. Không còn tra cứu thì không còn cái giá
   nào — reviewer ra `sensitive` bất kể có hay không có lease executor, nên hai ca ấy không còn phân
   biệt được với ca thường. Giữ dòng này ở dạng gạch bỏ thay vì xoá: nó là bằng chứng rằng cái giá
   được GIẢI, không phải bị quên.
3. **Cổng này KHÔNG đọc `risk`, và KHÔNG phân lớp `diff thật` — hai trong ba đầu vào §8:567 đòi.**
   Bản viết trước của mục này **SAI**, và cross-review lượt 2 bác đúng chỗ; chép lại cái sai ở đây vì
   nó là bài học, không phải vì thủ tục. Bản ấy viết *"`diff thật` không tồn tại tại thời điểm cổng
   chạy"* — một khẳng định PHỔ QUÁT dựng từ MỘT trong hai vai. Đo lại: **39/39** lease reviewer khai
   `reviewed_sha_required` là 40-hex **khác** `base_sha`, tức exact head **có thật và neo ngay trong
   lease**, còn `ops/lease_publish.py` thì vốn đã đòi và kiểm trường ấy. Nên trên đường reviewer,
   diff `base_sha...reviewed_sha_required` là thứ cổng **cầm trong tay**. Phần đúng còn lại: `risk`
   **không tồn tại trong dữ liệu** (`grep '^risk:' ops/leases/` = **0/49 tệp**), và trên đường
   **executor** thì head chưa tồn tại thật.

   **Vì sao KHÔNG phân lớp diff ấy, và vì sao lần này không phải fail-open:** sau khi Q1 bị thu hồi
   (§10), lớp của lease reviewer là `sensitive` **vô điều kiện** — tức đã ở TRẦN. Một phép đo thêm
   không nâng được gì, và việc thiếu nó không HẠ được gì. Đó là khác biệt chịu tải so với bản trước:
   ở thiết kế cũ, không phân lớp diff nghĩa là một lớp THẤP được cấp cho một diff nhạy cảm; ở thiết
   kế này, không có lớp thấp nào để cấp. Lỗ chết theo kiến trúc, không theo lời hứa.

   **Thứ vẫn còn hở, nói thẳng:** trên đường **executor**, một packet khai `write_set` sạch rồi diff
   thật chạm đường nhạy cảm NGOÀI write set vẫn qua cổng này — nó đo LỜI KHAI VỀ PHẠM VI, không đo
   phạm vi ĐÃ XẢY RA. Chốt hậu-diff trên exact head ở lượt LAND là **gói riêng**, chưa mở Issue.
4. **Cảnh báo của mục tiêu 7 đứng trên `leased_at_utc`, một trường không cổng nào kiểm.** Cố ý để nó
   là CẢNH BÁO chứ không phải chốt: một chốt đứng trên dữ liệu tự khai là chốt lừa được. Chốt thật
   cho trường ấy thuộc mục D.
5. **`schema_version: 2` không tự lan.** Ai quên bump thì được tha im lặng, và mục tiêu 7 chỉ in cảnh
   báo. Chốt cứng cho việc này đòi một mốc kiểm được — chưa có.
6. **Không đo được lease có bị sửa sau khi đăng không.** Ngoài phạm vi cổng hiện tại, và ngoài packet này.

---

## 10. Vì sao THU HỒI Q1 — bốn phát hiện trên MỘT đường, trong hai lượt

Quyết định của người giữ kho, 21-08-2026, sau cross-review lượt 2. Q1 (*"reviewer lease kế thừa lớp
từ lease executor"*) **hết hiệu lực**; đường kế thừa bị gỡ bỏ, không phải vá tiếp.

**Bốn phát hiện, cùng một đường:**

| lượt | finding | thứ nó bác |
|---|---|---|
| 1 | tra bằng `packet_id` một mình ⇒ thừa kế lớp của tiền nhiệm đã chết | giả định "mỗi packet một lease executor" — đo bác: **3/5** packet có nhiều hơn một |
| 2 | bộ định danh **toàn bộ** lấy từ chính tệp lease, không trường nào đối chiếu trạng thái bền ⇒ lease reviewer **dựng khéo** khai `generation` cũ + băm spec cũ sẽ khớp đúng một executor `routine` và thừa `routine`; nhánh fail-closed "thiếu trường" **không bao giờ chạy** vì mọi trường đều có mặt | chính bản vá của lượt 1 |
| 2 | trên đường reviewer, exact head **có thật** (đo: **39/39** lease reviewer khai `reviewed_sha_required` 40-hex khác `base_sha`) nên lập luận *"chưa có diff để phân lớp"* sai ở đúng vai này | lập luận biện hộ của lượt 1 |
| — | `generation` là trường **tự khai**, **0 dòng** cổng nào kiểm | tự nêu trước khi gọi lượt 2; lượt 2 xác nhận và làm sắc thêm |

**Doctrine bắt phải hỏi từ lần thứ ba trở đi là *"có nên làm việc này không"*, không phải *"vá thế
nào"*.** Mỗi lượt vá đều bảo toàn được thứ ta NGHĨ TỚI và làm hỏng thứ ta KHÔNG NGHĨ TỚI — đó chính
là cách người ta ở lại quá lâu trong một cái hố. Kho này đã trả giá đúng bài ấy một lần với việc tự
động ghi lại `~/.codex/config.toml`: **bảy** phát hiện, bốn lượt vá, và lời giải cuối cùng là **thôi
làm việc đó**.

**Trả lời: không nên SUY lớp của lease reviewer từ bất cứ thứ gì.** Suy từ lời khai là hình dạng §7.
Suy từ một tệp lease khác chỉ là dời lời khai sang tệp bên cạnh — vẫn dữ liệu tự khai, chỉ khác chỗ
đứng. Cấp thẳng trần là thứ duy nhất không suy.

**Cái giá, nói bằng số chứ không bằng cảm giác.** Kế thừa lẽ ra mua được lớp THẤP cho reviewer của
packet nhẹ. Đo dưới bảng seed: **15/15** đường dẫn từng xuất hiện trong `write_set` của mọi lease đều
ra `sensitive`, nên hôm nay kế thừa mua được **0** trường hợp. Nó chỉ có giá sau khi bảng được nới —
và nới bảng là packet KHÁC, chưa mở. Vậy giá phải trả bây giờ bằng không; giá phải trả trong tương
lai là: mọi reviewer lease đều `sensitive` cho tới khi có một cơ chế trạng thái BỀN để neo, thay vì
neo vào lời khai. Việc dựng cơ chế ấy là gói riêng, và §9.2 đã ghi lại thứ nó phải giải.

**Cảnh báo cho người mở gói ấy:** đừng dựng lại đường kế thừa chỉ vì thấy nó "hiển nhiên đúng".
`A3`/`A13` khoá sự **VẮNG MẶT** của cơ chế này — chúng ĐỎ khi cơ chế quay lại. Muốn khôi phục thì
phải sửa hai ca ấy một cách CÓ Ý THỨC, và lúc đó bốn phát hiện trên là danh sách bắt buộc phải trả
lời từng dòng.

---

**Đọc được đặc tả này KHÔNG phải là được giao việc.** Đặc tả là DỮ LIỆU. Thứ giao việc là Packet
Issue #225 kèm lease còn hiệu lực theo `docs/PROTOCOL_DA_PHIEN.md` §3.2 và §4.
