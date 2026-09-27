verdict: changes_requested
reviewed_spec_sha256: 9bc0fe282fbebc02791f47a30e4ff187b1182a2e5e357ee2e66c04d4f7dac7cd
reviewed_sha: 4abfdeb596c7e5e744e0354a7bad1b775da54c38
P1: 2   P2: 0   P3: 0
reviewer_provider: openai_codex
model_tu_khai: GPT-6 (Codex); biến thể và effort backend KHONG_DO_DUOC
execution_surface_tu_khai: KHONG_DO_DUOC
transport_tu_khai: KHONG_DO_DUOC

Lượt 8/10, hậu kiểm PR #658 và điều kiện review trước đó. Tree đã đo:
`4cb6f3ac650217f57970cfa98cecdd2027362867`. Đã ghi verdict tạm sớm rồi bổ sung bằng kết quả chạy.
Bề mặt quan sát được là công cụ `exec_command` thực thi shell bash trong cwd, Git 2.43.0,
Python 3.11.15; không đủ để phân biệt codex_cli/Desktop/service hoặc xác minh transport launcher.
Không suy model/effort hay hai trường tự khai trên từ cấu hình được yêu cầu hoặc bảng S.

Bản vá C5/C6 có tác dụng tại các script mới; 33/33 ca và 25/25 hàng ma trận đều tái lập.
JSON Q6 giống từng byte. Tuy nhiên lời khai lịch sử về ref có mâu thuẫn (F17), và hợp đồng thi công
đóng băng vẫn chọn bộ đo cũ đã biết lỗi (F18, **cần revision 3**).
Không mở lại F1 prediction-only, F2 Q6 cây mốc + (b), ngoại lệ ≤3 tệp/≤663 dòng hay trần 10.
Không sửa `cay-kho/`, SPEC, hai script gốc hoặc hiện vật đầu vào; không gọi mạng, CI, push hay merge.

## ĐỐI CHIẾU CONNECTOR

Số C1–C6 theo bảng trong HAU-KIEM, không theo thứ tự xuất hiện comment trong CONNECTOR.

| Finding | Có đúng không? | PR #658 xử lý | Bằng chứng độc lập / giới hạn |
|---|---|---|---|
| C1 — thiếu nhãn HINT | Đúng. Sáu payload gốc bắt đầu bằng unified diff. | **ĐÓNG** về ràng buộc 1. | Sáu dòng đầu nay chứa đúng nguyên văn nhãn; bỏ đúng 3 dòng đầu cho đúng sáu băm bảng H. Cả bản có nhãn và không nhãn đều `patch -p0 --fuzz=0 --dry-run` rc0 trên bản nháp tương ứng: 12/12. Không đồng nghĩa đã giải quyết ràng buộc 3. |
| C2 — reviewed_sha khác head mang verdict | Đúng về hai cây khác nhau. Không xác minh được riêng OID `f1dec864…` của connector. | **ĐÓNG** trong phạm vi quyết định human audit được prompt giao là đã chấp nhận. | Git cho cây `15c0240b…` ở `7fc28680`, cây `45e611fa…` ở `d71f77ec`; diff chỉ bốn hiện vật lượt 7, SPEC không đổi. Không suy `f1dec864…` là merge tổng hợp: đây chỉ là giả thuyết của tác giả. Verdict lượt này neo đúng HEAD hiện tại, ghi ngoài checkout. Nếu đưa verdict vào commit mới thì không tự coi SHA mới đã được review. |
| C3 — thiếu execution surface/transport | Đúng: verdict lượt 7 chỉ có provider và model tự khai. | **ĐÓNG-MỘT-PHẦN**. | Bảng S bổ sung lời khai có chỉ rõ nguồn `run.json`/header; giữ nguyên hiện vật reviewer là đúng. Không có các nguồn ấy trong cwd nên chưa xác nhận số đo lịch sử. Lượt này tự khai KHONG_DO_DUOC, không mượn bảng S để chứng nhận runtime. Phần lịch sử phải được receipt/launcher evidence xác minh ở bước điều phối; không suy số đo sai chỉ vì thiếu dữ liệu. |
| C4 — origin cục bộ | Đúng cho cả bảy lượt theo PROMPT/EVIDENCE lưu trong packet. | **ĐÓNG-MỘT-PHẦN**: điều kiện lượt 8 đã chữa; lời khai lịch sử chưa đúng. | `remote get-url origin` trả endpoint thật; 440 cặp tên/OID cache bằng snapshot được cấp, đối xứng sai khác rỗng. Không mạng nên không đọc lại advertisement sống. F17 bác câu “trước mỗi lượt… lệch 0, không thì dừng”, không bác phép so 440/440 của lượt này. |
| C5 — đường dẫn bị Git quote rồi lọt ngoài miền | Đúng. | **ĐÓNG-MỘT-PHẦN**: đóng tại `do_q6_hk.py`, chưa đóng đường thi công F18. | Dùng lại nguyên fixture `ten-co-tab`: gốc rc0, 0 vi phạm, xếp tệp vào ngoài miền; bản vá rc3, báo ký tự điều khiển. `ls-tree -z` và chốt ký tự có mutant riêng; tập đỏ đúng khai. Hai script gốc vẫn nguyên băm. |
| C6 — bỏ qua returncode | Đúng. | **ĐÓNG-MỘT-PHẦN**: đóng tại `mut_q6_hk.py`, chưa đóng đường thi công F18. | Harness gốc chạy candidate thoát sớm rc2 vẫn in KHOP cho `goc` và `bo-rieng-chot-thu-muc-con` (toàn ma trận rc1 vì các hàng khác LECH; không khai toàn ma trận xanh). Harness mới từ chối rc2 và mã âm; bỏ chốt cùng assert cho `SAI KHOP chet-im-lang-rc2`, `CO_LECH`, rc1. |

Bằng chứng: `scratch/integrity.json`, `scratch/own-probes.json`, `scratch/final-measures.json`,
`scratch/negative-exit.json`; mã tái chạy ở `scratch/review8.py` và `scratch/final-measures.py`.

## Findings

### F17 — P1 — `so-do-khong-khop`: bảng S cấp lời bảo đảm lịch sử bằng một số bị hồ sơ cũ bác bỏ

**Vị trí:** `HAU-KIEM-CONNECTOR-652.md:85–88` (cùng đường trong
`ops/reviews/thu-hoi-lease-a1a-r2/`), đối chiếu `luot1-EVIDENCE.md:182`, `luot2-EVIDENCE.md:37–39`.

Bảng S nói trước **mỗi** lượt đã so với máy chủ, “phải lệch 0, không thì dừng”, rồi kết luận tập ref
đã được đối chiếu. E7 lượt 1 ghi rõ mirror 430, máy chủ 429 lúc 15:57Z, thừa một nhánh được nêu tên;
lượt 1 vẫn diễn ra lúc 15:59. E11 lượt 2 mới ghi đã gỡ nhánh ấy và so tên được 435/435; OID lấy từ
cache, không phải readback máy chủ. Vì vậy không thể dùng câu tổng quát hiện tại để xác nhận điều
kiện bootstrap của cả bảy review. Đây là số chống đỡ lời khai thẩm quyền/assurance review nên P1
đúng thang của prompt; không phải số thống kê thuần P2, cũng không phải cáo buộc số 440 của lượt 8 sai.

**Chạy được:** `python3 -B scratch/final-measures.py` lấy ba blob bằng `git show HEAD:<path>`,
đòi byte-equal bản packet và trích dòng mâu thuẫn vào `scratch/final-measures.json`.
E7 sha256 `4174d6de9fa5710a0d14e6f9f293b7e8af7f6d418faba0afbbf690518386e56d`;
E11 sha256 `2e8b8feca83a99410c948fcd9825cf93312b6f5f49f67c00ba97465c0e7922e5`.
Đây là phản chứng bằng hồ sơ bất biến có sẵn, không phải phép đo lại máy chủ ở thời điểm lịch sử.

**Đề xuất:** sửa đoạn tổng kết bảng S theo từng lượt: lượt 1 lệch 1; lượt 2 mới căn tên; không biến
so tên thành so OID. Giữ riêng điều kiện lượt 8 và giới hạn không mạng. `HINT.patch` có hunk sửa
lời khai này, đã áp đúng vào bản sao dưới scratch.
**Ca khóa:** đối chiếu câu tổng quát với E7/E11; không còn khẳng định mọi lượt lệch 0 hoặc mọi OID
đã readback. **Tác động cần tránh:** không dùng sửa lời khai để rút lại quyết định audit C2 hoặc
đồng nhất sai lệch lịch sử với sai lệch của snapshot lượt này.

### F18 — P1 — `q6-thieu-kiem-id-ten`: bộ đo đã vá chưa được ràng buộc vào hợp đồng thi công

**Vị trí:** `SPEC.md:288,303,313,324–325,361,370–372`; PR mới
`HAU-KIEM-CONNECTOR-652.md:26–42`. **Cần revision 3; không sửa SPEC revision 2.**

F11/F12/F13 được các lượt trước đóng với lời bảo đảm mọi lease trong miền đều được kiểm.
Phản chứng C5 đã bác lời bảo đảm ấy ở đúng script mà revision 2 ghim. PR giữ nguyên script gốc là
đúng về bảo toàn lịch sử, nhưng thêm hai tệp `_hk.py` chưa thay được lệnh bắt buộc trong SPEC:
executor vẫn được yêu cầu chạy `do_q6.py`, tự kiểm 31 ca và `mut_q6.py`. SPEC không chứa tên nào
của hai bản vá. Hồ sơ hậu kiểm cũng không có revision mới đã được duyệt thay hợp đồng đó.

**Chạy được:** `python3 -B scratch/review8.py` dùng nguyên fixture C5 có sẵn:
`frozen.ma_thoat=0`, `patched.ma_thoat=3`; gốc bỏ qua tệp lỗi trong miền. Với C6,
`python3 -B scratch/final-measures.py` chạy harness gốc trên bản sao thoát rc2 trước tự kiểm:
`KHOP goc: rc=2 do=[] khai=[]` và `KHOP bo-rieng-chot-thu-muc-con: rc=2 do=[] khai=[]`.
Cùng script trích chính các lệnh thi công từ blob SPEC ở HEAD; `patched_names_in_spec=false`.

Không thể chữa chỉ bằng lời “dùng bản mới”: tiêu chí SPEC:371 còn nói có dòng `LECH` thì dừng,
nhưng log mới đúng có `DUNG LECH chet-im-lang-rc2`. Cần ràng buộc cả tên/băm, phiên bản suite và
ngữ nghĩa thành công của harness mới. Đây là tồn dư lớp F11 đã đóng sai, được C5/C6 cung cấp phản
chứng mới; không phải mở lại lựa chọn mốc Q6/(b) hoặc đòi thay dữ liệu `BIA_MO_LICH_SU`.
P1 vì hợp đồng vẫn chọn phép kiểm bỏ qua đầu vào trong miền và nhận sai kết thúc tiến trình;
không nâng C5/C6 chỉ vì thiếu thêm test.

**Đề xuất:** tác giả trình revision 3 neo đúng băm hai bản vá, đủ ba lệnh chạy và tiêu chí dương:
rc0, đủ tập ca/hàng đã khai, không hàng SAI, `TAT_CA_KHOP`; đối chứng âm `DUNG LECH` phải được
phân biệt với ma trận lệch thật. Giữ tệp r2 và script gốc nguyên byte, giữ mốc/clock/Q6/(b), JSON
và tuple rỗng. Human quyết định và audit revision mới theo quy trình hiện hành.
**Ca khóa:** chạy đúng lệnh do revision mới chỉ định trên fixture C5; chạy đối chứng chết rc2/mã âm;
ma trận mới phải đạt trong khi gỡ chốt vẫn đỏ; Q6 thật vẫn byte-equal.
**Tác động cần tránh:** sửa tiêu chí LECH thành bỏ qua mọi LECH sẽ mở cửa giả; phải kiểm kết quả
mong đợi riêng từng hàng. `HINT.patch` chỉ ghi hướng xử lý/đánh dấu phần chưa đóng trong hồ sơ hậu
kiểm, không sửa đặc tả đóng băng hay tự tạo revision 3. Hunk đó không tự đóng F18.

## Bảng đo lại

| Đối tượng | Thực đo | Hiện vật |
|---|---|---|
| HEAD / tree | đúng OID header; tree `4cb6f3ac650217f57970cfa98cecdd2027362867` | `scratch/integrity.json` |
| Diff PR | 11 tệp, +499 dòng, chỉ dưới thư mục review; Git diff byte-equal packet | `scratch/integrity.json` |
| SPEC | 400 dòng, 50.574 byte; sha256 đúng header; byte-equal bản trong checkout | `scratch/integrity.json` |
| `do_q6.py` | `36d8f1667aaa72a1bf00dfb7d1ded4331cb65efab5a0376bb3506528fd6d89d0` | đúng SPEC, giữ nguyên |
| `mut_q6.py` | `272dc1e82a32331348f59c182803c7cada373f98fbbdd6d4f91ce40d6641e794` | đúng SPEC, giữ nguyên |
| `do_q6_hk.py` | `7f9fe4572ba56ce20191877c9626e9004cc7589fd98a991489d6675c6afb7beb` | đúng lời khai |
| `mut_q6_hk.py` | `81274590080a173255ac3ed8accce74bdfa638bb065d0d5abb634253859de9d9` | đúng lời khai |
| Sáu HINT bảng H | 6/6 băm sau nhãn và 6/6 băm payload sau bỏ 3 dòng khớp; nhãn đúng; lượt 7 rỗng | `scratch/integrity.json` |
| Áp HINT lịch sử | 12/12 dry-run rc0, trước/sau nhãn trên đúng sáu bản nháp | `scratch/own-probes.json`, `hint_apply` |
| Tự kiểm mới | 33/33, rc0, stderr rỗng, log byte-equal | `scratch/self-check.log` |
| Ma trận mới | 25/25 hàng DUNG, rc0, stderr rỗng, log byte-equal | `scratch/mutation.log` |
| Q6 thật | rc0, `cmp` rc0; sha256 `1fc99cd9339fb5f085436e60ef39bac3058a79dbc009161597ecc7bc85efbd61` | `scratch/q6.json` |
| Cây mốc | 89 lease hợp lệ, 3 tệp ngoài miền, 11 cặp hai chiều, 3 một chiều, 0 vi phạm/KXD, giữ 0 | JSON và walker độc lập |
| Digest cặp | `8f372ccd2ceab70901868a58d3380acbd89dce25c7127d4d514bc959270fef48` | `scratch/final-measures.json` |
| Hạn mới muộn nhất / clock | `2026-09-08T10:17:12+00:00` < `2026-09-10T04:55:37Z` | walker; giờ commit mốc khớp clock |
| Mốc là tổ tiên | HEAD và origin/master đều rc0 | `scratch/final-measures.json` |
| Origin và ref | endpoint thật; 440/440 tên/OID, sai khác đối xứng 0 | `scratch/integrity.json` |
| Snapshot được cấp | sha256 `d854f6791b2c8ab8fb6c718a88d0585f18fba91cbbbf52373604403812029b57` | khớp `.mirror-info`; không phải readback mạng của reviewer |

25 là số hàng ma trận (gồm gốc và đối chứng âm), không phải 25 mutant đều bị suite giết.
Hai script gốc đúng băm là điều kiện bảo toàn bằng chứng; không chứng minh thuật toán không còn lỗi.

## Nghiệm thu

C1 và phần triển khai C5/C6 đạt các phép đo được giao. C2 không bị mở lại. C3 giới hạn ở lời khai
bổ sung, không nâng thành máy đo. C4 chữa bootstrap hiện tại nhưng cần sửa tổng kết lịch sử F17.
F18 ngăn coi bản vá hậu kiểm là đã thay hợp đồng thi công. Ngưỡng áp dụng là 0 P1/P2/P3;
còn hai P1 nên `changes_requested`, không phải nghiệm thu implementation A1a hay quyền cấp lease/merge.

**Mỗi chốt mới có răng tới đâu:**

- Bỏ `-z`: đúng hai ca mới đỏ. Bỏ toàn chốt ký tự điều khiển: chỉ ca xuống dòng sau đuôi đỏ;
  ca tab được chốt so tên che. Điều này đúng chú thích ma trận, không khai mọi ca cô lập.
- Gỡ kiểm rc: bảy assert nội bộ chặn ngay rc2. Gỡ cả assert như phản chứng của tác giả:
  hàng đối chứng thành SAI KHOP và tổng CO_LECH. Bản gốc chưa đọc rc; bản mới đọc thật.
- Kiểm trực tiếp mã 0,1,2,3,127,-9,-15 với tập đích rỗng: chỉ 0 được nhận. Một tiến trình Python
  con thực sự bị terminate trả -15, stderr rỗng; classifier mới từ chối, biểu thức cũ chấp nhận.
- Chưa có ca/mutant riêng cho nhánh DEL của chốt ký tự và decode byte không UTF-8: hai mutant
  độc lập “bỏ riêng kiểm DEL” và “surrogateescape thành strict” đều sống 33/33. Đây là giới hạn
  phủ thực đo, không được khai thành lỗi chạy của bản gốc hoặc mutant đã bị giết. Bộ 33 ca không
  bao phủ toàn bộ miền byte tên Git. Không mở thêm finding chỉ vì tồn tại mutant sống.

**Ý kiến về protocol §13 ràng buộc 3:** §13 dẫn sang ba ràng buộc ở §8: sensitive chỉ cho hint
ở test thuần hoặc tooling không tham gia authority/gate/runtime. `SPEC.md` quyết định acceptance,
write set và điều kiện cấp lease nên không có cơ sở tự xếp vào hai nhóm được phép. Mặt khác,
`do_q6.py`/`mut_q6.py` được SPEC dùng làm điều kiện dừng lúc thi công; gọi chúng “hiện vật review”
không tự chứng minh ngoài gate. Nhãn của C1 không giải quyết phân loại này. Tôi đề nghị chủ kho
xác nhận cách xử lý provenance/human audit các hunk lịch sử và quy tắc áp dụng cho revision tiếp
nối; không tự phán ngoại lệ, không hồi tố sửa sáu payload hay quyết định human audit đã có.
HINT lượt này tránh hunk SPEC: hướng sửa F18 được mô tả bằng lời trong tài liệu hậu kiểm. Theo
yêu cầu trực tiếp của prompt, HINT là unified diff cho các đề xuất của hai finding; không phải
ủy quyền áp dụng hoặc chứng nhận đã sửa hợp đồng. Không phát sinh câu hỏi xin phép trong lượt này.

## Phản chứng đã chạy

Thiết lập mọi lệnh Git đo kho/fixture:

```sh
export GIT_CONFIG_NOSYSTEM=1
export GIT_CONFIG_GLOBAL="$PWD/scratch/gitconfig.empty"
export TMPDIR="$PWD/scratch/tmp"
export GIT_OPTIONAL_LOCKS=0
```

Config global trên là tệp rỗng. Fixture Git thông thường nằm trong scratch; Python dùng `-B`.

| Lệnh / phép thử | Kết quả |
|---|---|
| `python3 -B do_q6_hk.py --tu-kiem cay-kho` | rc0, 33/33 |
| `python3 -B mut_q6_hk.py scratch/m cay-kho do_q6_hk.py` | rc0, 25 DUNG, TAT_CA_KHOP |
| `python3 -B do_q6_hk.py cay-kho 072181157a27804e69deb35bb792a88c70ac31e3 2026-09-10T04:55:37Z` | rc0, JSON byte-equal |
| `python3 -B scratch/review8.py` | rc0; A/B C5, prefix, classifier, ba mutant, gỡ rc/assert, 12 dry-run HINT |
| `python3 -B scratch/final-measures.py` | rc0; hồ sơ lịch sử, invocation SPEC, harness cũ rc2, walker cây thật |
| Tiến trình con thực sự terminate | rc -15, patched_accepts=false; `scratch/negative-exit.json` |
| `patch -p0 --fuzz=0` áp HINT lượt này vào `scratch/hint-final/` | rc0, nội dung đúng bản dự kiến; `scratch/hint-final.log` |

Đã dùng lại tên bất thường từ hai fixture có sẵn, không tự soạn chuỗi nhạy cảm mới. Di chuyển
nguyên tên lá ấy tới trực tiếp dưới `ops/` với tiền tố `leases-`: Git không đưa chúng vào kết quả
`ls-tree ... -- ops/leases`; bản vá vẫn rc0, 2 lease hợp lệ. Đối chứng tên ASCII thông thường ở
`ops/leases-other` và `ops/leases2` cũng bị loại đúng. Không có lỗi “khớp tiền tố” trong các ca
thực chạy (`scratch/prefix.json`, `scratch/own-probes.json`).

Hướng byte không UTF-8/DEL chỉ mô tả bằng lời khi cần tạo mới nội dung nhạy cảm: executor dựng
fixture riêng trong kho giả, đòi rc3 có chẩn đoán thay vì crash/bỏ qua, rồi gỡ từng chốt và đòi
đúng ca đổi màu. Với dữ liệu blob, phân biệt tên không đọc được với YAML không đọc được; với
đầu ra JSON, kiểm cả khả năng consumer giải mã. Không tự dựng object/helper Git giả, đường thoát
cây hay đồng tự Unicode. Không khai những hướng chưa chạy là đã kiểm.

## KHÔNG ĐO ĐƯỢC

- Advertisement GitHub sống, REST comments, run/CI/merge phía máy chủ; chỉ đọc snapshot đã cấp.
  Số 440/440 đo tính nhất quán snapshot/cache, không tự chứng minh nguồn snapshot hoặc thời điểm máy chủ.
- `run.json`, `stderr.log` và workspace thật của bảy lượt trước nằm ngoài cwd; không đọc. Bảng S về
  surface/transport/model/effort/thời gian chưa được xác minh độc lập. Không đủ để nâng assurance.
- OID `f1dec864a95ea91a17e6b3da7b7df1d21ee7ce16` không có trong object store (cat-file rc128).
  Không xác định được lý do; không xác nhận giả thuyết merge tổng hợp.
- Human audit C2 được coi là quyết định đã giao trong prompt; chưa readback comment mạng. Không mở lại.
- Không chạy `ai-dang-giu` tới origin thật vì cần mạng; không thay bằng mirror cục bộ để khai đã đo cùng
  điều kiện mới. Không nghiệm thu A1–A22 của implementation tương lai hoặc actionlint/CI/Windows/LIVE.
- Không thực thi fixture mới chứa byte không UTF-8/DEL, object Git giả hoặc hướng thoát cây; giới hạn
  và đề xuất có ghi ở trên. Không nhận mutant sống là phản chứng đã gây lỗi trên một đầu vào thật.

Kết quả hiện tại giữ nguyên số đo Q6 và các quyết định chủ kho. Hai việc còn phải xử lý là tính đúng
của lời khai lịch sử và ràng buộc bản vá vào revision có thẩm quyền; HINT không thay quyết định ấy.
