verdict: changes_requested
reviewed_sha: 2ec6171f7a2e21ae950633f9e328329a355f7a6d

**KHÔNG CÒN P1 trong phạm vi PR #491 được review.** Ba P1 lượt 1 đã vá thật. Còn **3 P2 và 10 P3** dưới đây; không nâng chúng thành P1 để kéo dài review. `changes_requested` phản ánh những sửa chữa còn nên làm, không có nghĩa điều kiện “tới hết P1” của chủ kho chưa đạt. Không thực hiện merge hay xác nhận authority trên GitHub.

Reviewer: GPT-6/Codex theo danh tính được cấp trong phiên; provider OpenAI, execution_surface Codex/API có shell cục bộ, transport machine; không có chứng thực độc lập variant/build/effort. Reviewer độc lập với executor, loại đối chiếu khác provider theo chỉ thị người dùng/§8; không tự tạo receipt hoặc transition `cross_approved`. Tree tự đo: `5b8c1bed8b754f7b6fdf1004743368b5fcdba85f`.

Chỉ đọc/ghi trong workspace, không mạng. `cay-kho/` giữ nguyên; đột biến trên `review-evidence/mutant/`, TMPDIR trong `review-evidence/tmp/`. Không tự soạn payload đường dẫn; chỉ chạy suite có sẵn và đột biến văn bản/sự vắng công cụ. Kết quả kiểm lịch sử GitHub được phân biệt với nội dung Git có thể đọc. “Khớp nguồn thuật lại” dưới đây không chứng nhận sự kiện đã xảy ra.

## ĐỐI CHIẾU LƯỢT TRƯỚC

- `chuoi-tam-pr-thuc-te-bay`: **ĐÃ VÁ THẬT** — tự chạy `rev-list --count --first-parent b416830..c0a5cbe` = 7; log đảo ngược theo thời gian cho #468→#477→#478→#486→#480→#487→#489. CHANGELOG:3–6, bảng :34–42 và thân PR:3–7 cùng khớp. “Tám” còn lại được đặt trong trích dẫn lỗi cũ, không phải khẳng định hiện tại.
- `no-thu-hoi-lease-dang-chep-trang-thai-cu`: **ĐÃ VÁ THẬT** — `git show 2aee80a:ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md` thật sự là r6/CHƯA CÓ/6/6; ref nhánh đặc tả trong gói mới vẫn trỏ `bd32d1145a4b890da695dc56196997b582c5be1e`, spec r9/“neo ở Issue”. Tự băm spec = `465538364b1a3f9477782fba79869bbd1c9351140e3fa9df50451baae22f9c79`, khớp `reviewed_spec_sha256` của luot8-VERDICT; verdict ghi lượt 8/lời gọi 9, 0 P1, S11/P2. CHANGELOG:116–124 đã neo snapshot và tách authority; thân PR:51,65 không lặp r6 như hiện trạng. Không coi lỗi `any` vốn có, ngoài diff, là P1 mới của PR này. Lưu ý mốc “head PR 16:10Z” là ba4a258, không phải head lượt 2 16:49:56Z; xem bảng.
- `ci-gia-thuyet-bi-viet-thanh-nguyen-nhan`: **ĐÃ VÁ THẬT** — đọc trực tiếp nguồn pr477:140–184: nguyên nhân CHƯA XÁC ĐỊNH; 34176439015 khác 34169756563, 1 khác 4. CHANGELOG:80 đã sửa cả tiêu đề; :92–109 giữ nguyên nhân mở và đối thủ Ubuntu. Thân PR:52,59 chỉ thuật lỗi bản đầu, không tái khẳng định nguyên nhân. Không còn khung “đã giải nguyên nhân”; phần nhãn nguồn chưa đều thuộc P2 riêng bên dưới.
- `ghim-cong-cu-khai-rong-va-bi-bo-loc-bo-sot`: **ĐÃ VÁ THẬT** về lời khai sai — CHANGELOG:50–53 giới hạn bản ghim vào actionlint, ba công cụ khác chỉ tìm/chạy trên PATH. Đọc script:157–179 xác nhận so bằng phiên bản actionlint và vòng `shellcheck git python3` không so pin. Dòng :52 có python3 nên bộ trích hiện giữ lời phân biệt này. Không tuyên bố bộ lọc đã hết bỏ sót: :50–51 về đầu ra EVIDENCE vẫn thiếu, giữ finding P3 cũ.
- `lenh-pham-vi-thieu-hai-moc`: **ĐÃ VÁ THẬT** — chạy nguyên khoảng được in ở CHANGELOG:23 và thân PR:17 cho tập `{ops}`; `git diff --name-only` không khoảng trên cây sạch vẫn rỗng. Cả hai vị trí đã thêm b416830..c0a5cbe, không thay bằng HEAD.
- `run-json-ba-khoa-chi-dung-cho-lenh`: **ĐÃ VÁ THẬT** — JSON hai lượt 14/15 đều 35 khóa cấp cao, `lenh` đúng ba khóa chuong_trinh/so_doi_so/van_tay; quét khóa đệ quy không có model/argv. CHANGELOG:161–168 và thân PR:55 phân biệt đúng hai cấp; giữ nhãn tự khai provider/transport.
- `hai-p3-khong-cung-la-hop-dong-dau-vao`: **ĐÃ VÁ THẬT** — CHANGELOG:130–135 gọi riêng hai slug, nhãn thuật lại đặt cạnh số hai. Đọc pr477:197–202 và diff b789e73 (+57/−5, hai tệp) thấy đúng một sửa t33 và một bổ sung giới hạn dựng gói. Thân PR:68 không còn gộp cả hai thành hợp đồng đầu vào. Lỗi phân loại tương tự mới xảy ra với sáu P3 của chính lượt 1, có finding riêng.
- `so-lich-su-bi-mat-nhan-nguon`: **VÁ HỜ** — các nhóm CI success, sáu mục lỗi và cận dưới finding được cải thiện, nhưng CHANGELOG:72–78 vẫn kể cài có kiểm băm/rc lịch sử và đúng ba lượt mà không giữ giới hạn nguồn DO-T33:34–37. :129 còn nói 5 Issue open; :130 nói PR chưa merge; :154 kể bốn lượt không nhãn tại chỗ. Thân PR:42,46,67–68 cũng không phân lớp. Lời hứa toàn xưng mới ở :15–16 bị chính các chỗ này bác bỏ; chi tiết P2 bên dưới.
- `bo-sot-pham-vi-ref-va-vat-chat-hoa`: **CHƯA VÁ** — regex vẫn bỏ CHANGELOG:49; tự so tập tên+OID được 317/317/317, lệch 0/0; chỉ heads có nguồn snapshot, không có phép đo mọi namespace phía máy chủ. Mệnh đề không đổi nghĩa so lượt 1.
- `bo-sot-tu-khai-evidence-va-manifest`: **CHƯA VÁ** — regex bỏ :50–51; tự đọc EVIDENCE có cách trích/phần bỏ sót và tự băm 3194/3194 mục ARTIFACTS khớp, 0 đường dẫn resolve ngoài workspace. Chưa chạy builder mới vì nó gọi mạng; đầu ra hiện có không bị hỏng.
- `bo-sot-pham-vi-nen-chua-do`: **CHƯA VÁ** — :139 vẫn bị bỏ, nội dung Linux+Bash/chưa macOS/Windows native giữ nguyên; đối chiếu bản b789e73 và nguồn pr477:130–138 khớp lời thuật lại. Lượt này chỉ Linux, không có phép đo hai nền còn lại.
- `bo-sot-nguong-hai-client`: **CHƯA VÁ** — :150–151 không chữ số nên mất; CLAUDE:580–581 thật sự ghi ít nhất hai client. Không gọi client mạng để thử quy tắc phương pháp này.
- `bo-sot-pham-vi-r-va-hai-sentinel`: **CHƯA VÁ** — :137 có số được giữ, :138–139 xác định R chính nó/cả hai/BỊ XOÁ bị bỏ; mã chốt và hai thao tác xóa không đổi trong diff. Không tự dựng probe đường dẫn bị cấm; hậu quả động lịch sử KHÔNG ĐO ĐƯỢC ở lượt này.
- `cong-kiem-ke-co-rang-nhung-khong-kiem-su-that`: **CHƯA VÁ** — bản sao có lịch sử Git: 1016→1017 vẫn doc-claims rc=0/ok=true/flags=[]; 35→36 và revision 9→10 cũng sống. Một byte CHANGELOG đổi, giữ kích thước, làm release rc=2/failed=[CHANGELOG.md]/hash_match=false. Đây vẫn là giới hạn cổng, không phải bảng trích bỏ sót.

## BẢNG ĐO

Lệnh Git dưới đây chạy trong `cay-kho/`. Đường dẫn CHANGELOG tính trong cây; `than-pr-491.md` là hiện vật cấp workspace. Mục r358 thật kết thúc dòng 169; dòng 170–172 của `muc-r358.md` đã thuộc r356, không tính thành số mới của r358. Bản trích 172 dòng khớp byte đầu CHANGELOG.

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| Exact head/tree | 2ec6171… | `rev-parse HEAD HEAD^{tree}` = SHA đầu verdict / 5b8c1bed… | Có |
| Phạm vi toàn PR | CHANGELOG + manifest | `diff --numstat c0a5cbe..HEAD`: CHANGELOG +169/−0; manifest +5/−5; đúng 2 tệp, không runtime | Có |
| Phần vá lượt 2 | vá nội dung lượt 1 | `diff --numstat ba4a258..HEAD`: CHANGELOG +74/−17 (ròng +57 dòng); manifest +5/−5 | +169 là toàn PR, không phải riêng delta |
| Tính toàn vẹn gói | ARTIFACTS.sha256 | Tự SHA-256 3194 mục: 3194 khớp, 0 lệch, 0 resolve ngoài workspace | Có |
| Ref ảnh chụp 16:51:16Z | 317 nguồn/mirror/cây, lệch 0/0 | `for-each-ref refs/heads`, so set tên+OID với nguon-refs.tsv: 317/317/317, 0/0 | Có cho snapshot; máy chủ hiện tại KHÔNG ĐO ĐƯỢC |
| Tệp trong chuỗi | 1016 | `diff --shortstat b416830..c0a5cbe`: 1016 | Có |
| Dòng thêm chuỗi | 247458 | Cùng lệnh: 247458 insertions, 0 deletions | Có |
| Thư mục cấp 1 | đúng một: ops | `diff --name-only` đúng khoảng, tách thành phần đầu: tập {ops}, cỡ 1 | Có |
| Lệnh phạm vi được sửa | có hai mốc ⇒ ops | Chạy lệnh mới đúng; bản thiếu hai mốc trả rỗng | Có |
| Số PR | bảy / 7 | `rev-list --count --first-parent b416830..c0a5cbe` = 7 | Có |
| Merge #468 | 802fc01 | First-parent log: Merge pull request #468 | Có |
| Merge #477 | 585c7d5 | Cùng log: #477 | Có |
| Merge #478 | c87b067 | Cùng log: #478 | Có |
| Merge #486 | da481f9 | Cùng log: #486, trước #480 | Có |
| Merge #480 | 7e69b8e | Cùng log: #480, sau #486 | Có |
| Merge #487 | f4d74fe | Cùng log: #487 | Có |
| Merge #489 | c0a5cbe | Cùng log: #489 | Có |
| Đặc tả trong #468 | bốn | `diff --name-only b416830..802fc01 -- ops/specs`: đúng 4 tệp GATE/LO/MUTANT-NHANH/MUTANT-SUBAGENT | Có; Mission #467 là hồ sơ, không xác thực GitHub |
| #487 thêm verdict/receipt | 5 lượt | Diff f4d74fe^1..f4d74fe có 5 verdict mới và 5 receipt đi kèm (#480×2, hậu kiểm #486×1, #487×2); còn sửa 3 receipt #478 | Có; không phải chỉ có 5 receipt chạm diff |
| ops/land nay | 6 tệp | Đếm trực tiếp = 6 | Có |
| Chuỗi đóng #490 | đã đóng | HEAD không chứa pr489-land-evidence; đây là số hiệu/decision thuật lại, không có API gốc | KHÔNG ĐO ĐƯỢC sự kiện đóng |
| VERSION từ r336 | 1.36.68, không nâng r337→r356 | VERSION tại 3dcdc6a/b416830/c0a5cbe/ba4a258/HEAD đều 1.36.68; `log 3dcdc6a..HEAD -- VERSION` rỗng | Có |
| Tiền lệ ghi sổ | r354/r355/r356 | Đọc cả ba mục: manifest/receipt v2/fixture dev-side | Có |
| Chuỗi chưa có mục ghi sổ | chưa mục nào | CHANGELOG không đổi trong b416830..c0a5cbe; các mã chuỗi chưa có mục ở base | Có trong phạm vi chuỗi |
| Vì sao chọn r358 | #472 chiếm r357 | Git có d3aaba5/0e00d85 mang r357 trên nhánh khác; bc78656 là tiền lệ đổi r355→r356 | Git khớp; gắn PR #472 KHÔNG ĐO ĐƯỢC qua API |
| Số mục gói hiện tại | 180/180 | manifest 180 files; release-verify checked=180/expected=180 | Có |
| Ops bị loại từ r336 | 0 ops | Manifest 3dcdc6a có 179 tổng/0 ops; b416830,c0a5cbe,HEAD có 180 tổng/0 ops | Có; không gán 180 về r336 |
| Gói không đổi | trong chuỗi ops | b416830 và c0a5cbe cùng package_hash bcde19d5… và total_bytes 8075509 | Có cho chuỗi trước #491; không áp cho chính #491 |
| Hash gói sau vá | bcde19d5…→1513d58d…→d47be343… | Đọc ba manifest tại c0a5cbe/ba4a258/HEAD khớp; hash hiện tại đầy đủ `d47be343d3b1a33d68b1f1a8683e666bdef10894738fb1945cc078215ec49aeb` | Có |
| Byte manifest/CHANGELOG | tổng sau vá | total_bytes 8075509→8083189→8089302; CHANGELOG 781187→788867→794980; delta vá +6113 B ở cả hai | Có |
| Băm CHANGELOG sau vá | d31a6447… | SHA-256 trong kiểm release khớp `d31a64473318b67f642e58a4c9b08d8481c5539ac452fdfe3bae0ad11f0ce612` | Có |
| Release strict trên head | rc0/ok true/failed[] | Chạy thật: rc=0, ok=true, failed=[], package_hash_match=true, package_hash_self_match=true | Có |
| Tập lỗi/thiếu/thừa | đều [] | extra_files, missing_from_current_manifest, required_missing, errors đều [] | Có |
| Release trước tái sinh | ok false, failed 1 | Tái tạo một byte lệch ở bản sao: rc2, 1 failed CHANGELOG; không có transcript tiến trình cũ để xác nhận lần executor chạy | Khớp hành vi tái đo; lịch sử chỉ thuật lại |
| Release có răng | byte lệch phải đỏ | dev-side→dev-sidE đầu tệp, kích thước vẫn 794980: rc2, hash_match=false/self_match=true; phục hồi rc0 | Có |
| Doc claims hiện tại | rc0/ok true | Chạy thật rc0/ok=true, 106 tệp, 367 advisory, flags=[] | Có; advisory không đồng nghĩa strict flag |
| Claims chặn số Git sai? | chưa hứa chặn riêng | Cây có .git, đổi mọi 1016 ở 169 dòng đầu thành 1017: rc0/ok=true/flags=[]; control và phục hồi cũng rc0 | Không chặn |
| Claims chặn số mới sai? | 35 khóa, revision 9 | Đột biến 35→36 và revision 9→10 trong r358: rc0/ok=true/flags=[] | Không chặn |
| Suite lease trên head | 121/121, chạy121, bỏ0, rc0 | Chạy nguyên `python3 -B ops/lease_publish_test.py`, actionlint dir append PATH: đúng toàn bộ, rc0 | Có |
| Receipt v2 trên head | tổng94, 0 vi phạm | Chạy thật: 41 đạt v2 + 11/11 legacy + 42 nợ = 94; 0 vi phạm, 0 không đo được, rc0 | Có |
| Công cụ actionlint | ghim 1.7.7 | Binary tuyệt đối được giao tự báo 1.7.7, rc0; lint ops-publish-lease.yml rc0 | Có về phiên bản/hành vi hiện tại |
| Chỉ actionlint ghim | ba công cụ kia tin PATH | Đọc vòng script: shellcheck/git/python3 đúng ba; so bằng pin chỉ dành actionlint | Có |
| AL_VER rỗng/sai, thiếu shellcheck | rc4 | Mã có chốt; chưa tái chạy toàn builder vì cần mạng. Lần thiếu shellcheck 09-09 là executor thuật, không phải tôi tái đo | KHÔNG ĐO ĐƯỢC động ở lượt này |
| Remote trùng template | rc5 | Mã kiểm rename/add và mã 5; chưa tái dựng probe lịch sử | KHÔNG ĐO ĐƯỢC động |
| Single-branch | rc6, mirror1, lệch304/304 | Mã có so tập/chốt6; thiếu đúng nguồn 304 nhánh của probe cũ, không thay bằng 317 mới | KHÔNG ĐO ĐƯỢC số lịch sử |
| Công cụ qua symlink, sentinel | rc4, còn sentinel | Chốt -L hiện hữu; không tự soạn phép thử đường dẫn bị cấm | KHÔNG ĐO ĐƯỢC động |
| Tái dùng R đã dựng | rc4, manifest nguyên | Gọi script có sẵn với workspace này làm R: rc4 trước ls-remote; SHA-256 ARTIFACTS không đổi | Có |
| Actionlint giả 0.0.0-GIA/exit42 | builder rc0, dùng1.7.7 | Mã dùng executable tuyệt đối sau cài; không tái chạy installer/probe giả lịch sử | KHÔNG ĐO ĐƯỢC động |
| T33 trước subprocess | assertion1359–1363, subprocess1364 | Đọc mã đúng; gọi chính t33 với shutil.which=None: AssertionError, subprocess.run được gọi 0 lần | Có |
| T33 khi thiếu công cụ | PR: “KHÔNG CHẠY”; CHANGELOG: đã chạy và đỏ | Phản chứng trên xác nhận hàm được vào, assert đỏ; log cũ có ĐỎ t33 và 120/121, chạy121, bỏ0 | Thân PR sai; CHANGELOG đúng |
| Lease lịch sử trước cài | 120/121, rc1 hai vế | nen/sau.lease.norm.out và *.rc khớp các giá trị; exit status lịch sử không tái đo được | Khớp log, không xác thực tiến trình cũ |
| Lease lịch sử sau cài | 121/121, rc0 | Hai *.lease-sau-cai-actionlint.out đều 8649 B, tổng121/121/chạy121/bỏ0 | Khớp log; rc/cài có kiểm băm chỉ lời khai |
| Sửa sót t33 | ba lần/ba lượt liền | Bản b789e73 kể lần thứ ba; nguồn HEAD vẫn sai ở DO-T33:9 và header script:33; thiếu chuỗi đủ ba verdict gốc | KHÔNG ĐO ĐƯỢC đúng số ba |
| Endpoint riêng | /mcp/44 tool và /mcp/x/actions | CLAUDE:583–585 chứa cả hai và 44 | Có nội dung dẫn; máy chủ 44 tool KHÔNG ĐO ĐƯỢC |
| CI Ubuntu 585c7d5 | success,44 bước,0 hỏng,26:46 | Nguồn pr477 ghi 01:22:44→01:49:30; tự trừ 1606s=26:46 | Số học khớp; event/44/0 KHÔNG ĐO ĐƯỢC |
| CI Windows 585c7d5 | success,44 bước,0 hỏng,48:15 | Nguồn ghi 01:22:45→02:11:00; tự trừ 2895s=48:15 | Số học khớp; event/44/0 KHÔNG ĐO ĐƯỢC |
| Trần/biên Windows | 60 phút,11:45 | ci.yml timeout-minutes=60; 3600−2895=705s=11:45 | Có số học trên thời lượng thuật lại |
| Issue463 nhằm tách job | không nâng trần | Tiêu đề/đầu hồ sơ GATE-TACH-JOB-CAT-CHI-PHI khớp | Có nội dung mục tiêu |
| Số đính chính skipped | 4→6;43/4 chưa rõ nguyên nhân | Nguồn pr477:145–184 phân biệt số khai/API thiếu/phân tích tĩnh, nguyên nhân chưa xác định | Khớp nguồn; không chứng nhận số skipped của job |
| Hai run | 34176439015/585c7d5 khác34169756563/802fc01 | Đọc đúng nguồn; hai ID khác nhau | Khớp nội dung nguồn; ánh xạ API KHÔNG ĐO ĐƯỢC |
| Cặp trước/sau | 43/1→44/6 | Số học +1 bước,+5 skipped; 1≠4 | Có số học; không xác thực cặp cùng job/attempt |
| Ba lý do/đối thủ | 3;Ubuntu44/4 ghi thành43/4 | Đúng 3 gạch đầu dòng; (44,4)+(−1,0)=(43,4) | Có về cấu trúc/số học; đối thủ là giả thuyết |
| Any trên master | any ở dòng606 | origin/master không có trong gói do đổi tên remote; refs/heads/master và mirror-cuc-bo/master cùng c0a5cbe. `git show refs/heads/master:ops/lease_publish.py` dòng606 đúng any | Nội dung khớp; lệnh origin/master nguyên văn KHÔNG CHẠY ĐƯỢC trong bundle |
| Một bia mộ đủ | đủ check rc0 | Hàm `_kiem_bia_mo` dùng any cho mỗi lease ID; một bản đủ vượt riêng chốt này, các chốt khác vẫn áp dụng | Đúng có điều kiện; không coi any tự bảo đảm mọi check |
| Mốc cũ r6 | 2aee80a/07-09/6/6/CHƯA CÓ | `git show` đúng header/metadata | Có nội dung lịch sử |
| Tip nhánh đặc tả | bd32d11 | `rev-parse refs/heads/claude/spec-thu-hoi-lease-va-cap-lai-20260907` = bd32d1145a4b890da695dc56196997b582c5be1e | Có tại snapshot gói mới |
| Thời điểm tip | 2026-09-09T11:23:01Z | Author/committer timestamps của bd32d11 đều đúng | Có timestamp Git; không chứng minh giờ push/tạo PR |
| “head PR16:10Z” | tip trước head | ba4a258 =16:10:00Z; reviewed head2ec6171 =16:49:56Z; 11:23:01 trước cả hai | So thứ tự đúng; tên mốc head cần ghi ba4a258 rõ hơn |
| Revision/packet_issue | 9/neo ở Issue | Blob tại bd32d11 đúng; băm spec trùng reviewed_spec_sha256 của verdict | Có |
| Verdict đặc tả | lượt8=lời gọi9;0P1;1P2 S11 | Header và kết luận luot8-VERDICT ghi đúng; S11 về hồ sơ Packet Issue A0 | Có nội dung verdict; không chứng nhận Issue ready/lease/call authority |
| Bốn lease A9 | 03:37:33/07:50:35/09:44:51/10:17:12Z | Safe-load bốn YAML: leased_at_utc đúng bốn giờ ngày07-09 | Có |
| Hạn tiền nhiệm #456 |14:30:07Z; cả bốn cấp sớm | YAML mutant-khong-chay-tren-windows: expiry07-09T14:30:07Z; cả bốn giờ nhỏ hơn | Có |
| A9 metadata |revision1/2/3/4;generation1;bốn hash | Bốn YAML đúng; hash prefixes8cca700c/bda86f12/37800aa6/4c542f6b khác nhau | Có |
| ADR0034 | đổi contract cần revision+generation mới | Đọc dòng7–8 đúng quy tắc | Có nội dung quy tắc; quyết định xử lý không xác thực offline |
| Issue463–467 |5 open | Không có response Issue để xác thực hiện trạng | KHÔNG ĐO ĐƯỢC |
| PR479 |chưa merge;hai P3 lượt6 | Git b789e73 sửa hai nội dung; nguồn pr477 liệt kê hai slug. Không có verdict gốc lượt6/PR response | Khớp nội dung thuật lại; status/count sự kiện KHÔNG ĐO ĐƯỢC |
| Ba công cụ giả |3;version9.9.9,rc0 | Đếm vòng mã đúng3; b789e73 kể probe; không chạy lại builder qua mạng | Khớp mã; probe lịch sử KHÔNG ĐO ĐƯỢC |
| R/hai sentinel | cả hai bị xóa | Mã còn hai thao tác xóa và thiếu chốt R; hậu quả được b789e73 thuật lại | KHÔNG ĐO ĐƯỢC động; không soạn payload |
| Phạm vi nền |Linux+Bash;0 phép macOS/Windows native | Nguồn pr477/b789e73 khai đúng; lượt này Linux | Khớp lời khai; phủ định toàn lịch sử KHÔNG ĐO ĐƯỢC |
| Tổng finding |ít nhất20 | Tự trích heading finding từ 10 verdict PR468 lượt6–15: đúng20 slug phân biệt, lưu finding-lower-bound.json | Có cận dưới; không gán thành tổng cả chuỗi |
| Năm hình dạng |mục1–5 | Đúng5 mục; không phải phân loại đầy đủ mọi finding | Có cấu trúc |
| Stdout đủ tự đếm |1/6 | Mỗi vế full-gate: doc70861B nguyên; cidk206B tail; ploop96B tail; lease8827B đã normalize; doctrine/adr vắng | Có trong phạm vi6 bộ lịch sử |
| Hai actor |ducthangho/notebyme88 | Hồ sơ đính chính hai tên; Git không xác thực merged_by/ai thao tác | KHÔNG ĐO ĐƯỢC sự kiện độc lập |
| Một slug qua bốn lượt |4 lượt vá hờ/chưa vá | Chỉ hồ sơ thuật lại, chưa đủ chuỗi verdict gốc để tái đếm | KHÔNG ĐO ĐƯỢC |
| Bản vá sinh lỗi |SÁU MỤC hồ sơ477 kể | Nguồn pr477:79–85 liệt kê đúng6 mục; r358 giữ nhãn “không phải sáu lần tái hiện độc lập” | Có về số mục và giới hạn |
| Ngưỡng client |ít nhất HAI | CLAUDE:580–581 đúng “ít nhất hai client” | Có nội dung quy tắc |
| run.json hai lượt |14/15;35 khóa;lenh3 khóa | Tự json.load cả hai:35/35, lenh3/3; không có model/argv trong khóa đệ quy | Có |
| Mức/slugs tự nhắc lượt1 |3P1,5P2,6P3 | Đếm heading VERDICT-LUOT-1.md đúng;8 hàng slug/mức thân PR:50–57 trùng nguồn;6 lần chú dẫn mức trong CHANGELOG:6,16,97,118,133,167 khớp | Có; không thấy gán nhầm P1/P2 cho các chú dẫn này |
| Phân loại6P3 |đều là bảng trích bỏ sót |5 về độ phủ bảng;1 về giới hạn cổng và mutant sống | Không |
| Runtime review lượt1 |316 ref,rc0,695.9s,worktree sạch,gpt-6-astra | Verdict cũ tự đo316/sạch; không kèm run envelope lượt1 cho số giây/rc runner/variant | KHÔNG ĐO ĐƯỢC phần runtime/provenance độc lập |
| Hai loại số/nhãn mọi chỗ |a/b;loại b đều ghi tại chỗ | Đọc khối:đúng2 loại; tìm counterexample ở72–78,129–130,154 | Không giữ lời hứa toàn xưng |
| Bảng trích cả r358+PR |script hỗ trợ nhiều input | Chạy chỉ muc-r358 tạo đúng byte BANG_KHANG_DINH; thêm than-pr tạo thêm35 dòng (header/blank+33 dòng số) | Bảng giao không chứa thân PR |

### so-lich-su-bi-mat-nhan-nguon  [P2]  Nhãn nguồn được sửa một phần, nhưng lời hứa áp mọi chỗ vẫn sai
TỆP/DÒNG: CHANGELOG.md:10–17,55–59,72–78,101–105,129–139,154–155; than-pr-491.md:42,46,67–68.
VẤN ĐỀ: Khối mới hứa loại (b) có nhãn tại chỗ, nhưng giữ nguyên nhiều số như phép đo trực tiếp. Đáng rõ nhất: cài lịch sử có đối chiếu băm và rc ở72–73 trong khi DO-T33:34–37 nói thiếu installer/archive hash/runner transcript; số đúng ba lượt ở75–78 và bốn lượt ở154 thiếu verdict gốc để đếm. “Issue463–467 còn open”/“PR479 chưa merge” không có mốc/nhãn trạng thái. Cặp run101–105 vẫn dùng “thuộc run” chắc chắn hơn nguồn vốn nói “được cho là cùng job”. “Head PR16:10Z” cần gọi đúng ba4a258; timestamp Git không chứng minh thời điểm tạo PR. Nhãn bảng builder có hai ngoại lệ, nhưng sự kiện thiếu shellcheck chỉ là executor tự đo; không gộp nó với phép chạy độc lập của reviewer. Không phủ nhận các con số, chỉ không cho nâng loại nguồn.
ĐÃ THỬ VÁ: không — sửa nhãn ngay tại các nhóm trên và thân PR: nguồn/commit/mốc/đã tái đo hay chỉ thuật lại; giữ ranh giới sự kiện GitHub với nội dung Git. Kiểm bằng rà mệnh đề thủ công, yêu cầu từng số có đường dẫn nguyên liệu hoặc ghi KHÔNG ĐO ĐƯỢC. Nguy cơ vá: thay số lịch sử bằng317/94 hiện tại hoặc đổi “thuật lại” thành “đã đo độc lập” vì hiện tại chạy xanh.
ĐÃ THỬ NGHIỆM: Đọc nguồn DO-T33:34–37, pr477:140–184/197–214 và luot8-VERDICT tại bd32d11; tự chạy bốn cổng chỉ chứng nhận hiện tại. API/installer lịch sử KHÔNG ĐO ĐƯỢC do offline/thiếu nguyên liệu. Counterexample văn bản đủ bác lời hứa toàn xưng.
ĐỘ TIN: cao

### sau-p3-khong-deu-la-bo-sot-bang  [P2]  Bản vá lại gộp sai bản chất finding của lượt trước
TỆP/DÒNG: than-pr-491.md:61; VERDICT-LUOT-1.md:148–189.
VẤN ĐỀ: “6 P3 còn lại đều là bảng trích khẳng định bỏ sót” sai: đúng5 finding độ phủ, còn `cong-kiem-ke-co-rang-nhung-khong-kiem-su-that` ghi nhận release có răng và doc-claims để mutant số sống. Lỗi mới cùng hình dạng P2 “hai P3 không cùng là hợp đồng đầu vào” vừa sửa. Tổng6/mứcP3 đúng, phân loại sai; không gọi đây là gán sai severity.
ĐÃ THỬ VÁ: không — tại dòng61 tách5P3 độ phủ và1P3 giới hạn cổng, gọi slug cổng. Khóa bằng đối chiếu đủ6 heading và phần VẤN ĐỀ nguồn gốc; không cần test sản phẩm. Nguy cơ: đọc “không kiểm sự thật” thành release không có răng, hoặc tuyên cổng đã sửa chỉ vì đã nói rõ giới hạn.
ĐÃ THỬ NGHIỆM: Regex heading nguồn đếm6P3; đọc từng finding cho phân hoạch5+1. Đột biến độc lập xác nhận finding thứ6 còn đúng trên head mới.
ĐỘ TIN: cao

### than-pr-van-phu-nhan-t33-da-chay  [P2]  Thân PR vẫn tuyên bố hàm t33 không chạy, trái chính đính chính
TỆP/DÒNG: than-pr-491.md:42 so CHANGELOG.md:75–78; ops/lease_publish_test.py:1359–1364.
VẤN ĐỀ: Câu “Thiếu nó thì bộ lease120/121,rc1 — … nó KHÔNG CHẠY” vẫn gán không chạy cho t33. Thực tế hàm chạy rồi fail assertion; chỉ subprocess lint chưa chạy. Đây là sai số/ý nghĩa executed-vs-skipped trong bằng chứng cổng của chính PR, nên nên sửa; không nâng thành P1. Lỗi này đã có ở nguồn cũ, lượt2 chưa loại khỏi hiện vật thân PR dù mục r358 dạy sửa cả khung. Không khẳng định đây là lỗi runtime mới do delta.
ĐÃ THỬ VÁ: không — sửa ngay thân PR thành “t33 đã chạy và đỏ ở tiền điều kiện; lint chưa chạy”, giữ120/121/rc1 và nhãn lịch sử. Khóa bằng chạy ca sẵn có với công cụ vắng và đếm subprocess; nguy cơ vá là đổi thành suite skipped hoặc120 ca được chạy, đều sai.
ĐÃ THỬ NGHIỆM: Import suite hiện hành, gọi chính t33, mock shutil.which=None: AssertionError,0 subprocess.run. Suite đầy đủ có công cụ rc0/121/121/chạy121/bỏ0; log cũ trước cài ghi ĐỎ t33/chạy121/bỏ0. mutation-results.json lưu kết quả.
ĐỘ TIN: cao

### bo-sot-pham-vi-ref-va-vat-chat-hoa  [P3]  Bảng vẫn bỏ phạm vi mọi ref và bước vật chất hóa
TỆP/DÒNG: CHANGELOG.md:49; trich_khang_dinh.py.
VẤN ĐỀ: Mệnh đề không chữ số bị bỏ;317 heads không chứng minh mọi namespace máy chủ.
ĐÃ THỬ VÁ: không — bổ sung nguyên mệnh đề vào bảng thủ công, tách clone --mirror khỏi đối chiếu heads. Kiểm tập tên+OID; không nâng thành mọi tag/namespace nếu thiếu ảnh chụp. Nguy cơ vá: đổi namespace để biến phạm vi hẹp thành lời khai toàn kho.
ĐÃ THỬ NGHIỆM: Regex bỏ49; tự so heads317/317/317,0/0; mã script dùng --mirror/update-ref. Namespace máy chủ khác KHÔNG ĐO ĐƯỢC vì không mạng.
ĐỘ TIN: cao

### bo-sot-tu-khai-evidence-va-manifest  [P3]  Bảng vẫn thiếu hợp đồng sinh EVIDENCE và manifest
TỆP/DÒNG: CHANGELOG.md:50–51; BANG_KHANG_DINH.txt.
VẤN ĐỀ: Mệnh đề đầu ra kiểm được bị rơi cả hai dòng. Không phải cáo buộc hiện vật hiện có sai.
ĐÃ THỬ VÁ: không — thêm đầy đủ mệnh đề/đường dẫn đầu ra và tách kiểm byte khỏi tái chạy builder. Khóa bằng đọc cách trích/phần bỏ sót và băm mọi mục; nguy cơ nhận tính toàn vẹn là chứng thực provenance sinh gói.
ĐÃ THỬ NGHIỆM: EVIDENCE có hai phần; tự băm ARTIFACTS3194/3194 khớp; regex bỏ50–51. Toàn builder mới KHÔNG ĐO ĐƯỢC vì gọi mạng.
ĐỘ TIN: cao

### bo-sot-pham-vi-nen-chua-do  [P3]  Giới hạn nền chạy tiếp tục vắng khỏi bảng
TỆP/DÒNG: CHANGELOG.md:139.
VẤN ĐỀ: Bỏ phủ định “chưa có phép đo macOS/Windows native”; dễ hiểu probe builder là đa nền.
ĐÃ THỬ VÁ: không — thêm dòng giới hạn, neo trong phạm vi probe builder. Kiểm với b789e73/nguồn pr477; nguy cơ viết phủ định cho cả CI Windows, vốn là nhóm số khác.
ĐÃ THỬ NGHIỆM: Regex bỏ139, nguồn khớp tự khai Linux+Bash. Lượt này chỉ Linux; hai nền khác KHÔNG ĐO ĐƯỢC.
ĐỘ TIN: cao về bỏ sót; vừa về phủ định lịch sử

### bo-sot-nguong-hai-client  [P3]  Bộ trích vẫn bỏ ngưỡng ít nhất hai client
TỆP/DÒNG: CHANGELOG.md:150–151; CLAUDE.md:580–581.
VẤN ĐỀ: Ngưỡng định lượng viết bằng chữ không được trích, dù nguồn dẫn đúng.
ĐÃ THỬ VÁ: không — bổ sung mệnh đề kèm nguồn vào bảng. Khóa bằng đọc ngưỡng thật; nguy cơ coi quy tắc là quyền vượt lệnh không mạng của review.
ĐÃ THỬ NGHIỆM: Regex bỏ cả150–151; CLAUDE ghi đúng ít nhất hai client; không gọi mạng.
ĐỘ TIN: cao

### bo-sot-pham-vi-r-va-hai-sentinel  [P3]  Bảng còn động tác nhưng mất đối tượng và hậu quả của probe
TỆP/DÒNG: CHANGELOG.md:137–139.
VẤN ĐỀ: Dòng137 được giữ, hai dòng sau bị bỏ: không còn R chính nó, cả hai sentinel và BỊ XOÁ. Đây vẫn là thiếu cả mệnh đề, không được xem là đã phủ nhờ một token xóa.
ĐÃ THỬ VÁ: không — bổ sung trọn đoạn, nhãn thuật lại cho hậu quả. Nếu cần động nghiệm, điều phối dựng sẵn phép thử thư mục đầu ra qua liên kết và dữ liệu đánh dấu trong hai thư mục con; reviewer chạy hiện vật ấy. Nguy cơ vá: tự dựng payload bị cấm hoặc nhận một chốt con là bảo vệ toàn bộ R.
ĐÃ THỬ NGHIỆM: Đọc mã chốt/hai thao tác xóa, đọc b789e73; regex mất138–139. KHÔNG ĐO ĐƯỢC hậu quả động vì không tự soạn probe đường dẫn.
ĐỘ TIN: cao về mã/bỏ sót; vừa về sự kiện probe cũ

### cong-kiem-ke-co-rang-nhung-khong-kiem-su-that  [P3]  Release bắt byte lệch, doc-claims vẫn để cả số cũ và số mới sai sống
TỆP/DÒNG: CHANGELOG.md:1,22,120,165; RELEASE_MANIFEST.json; than-pr-491.md:34–40.
VẤN ĐỀ: Gate xanh không chứng nhận số Git/JSON/revision. Kết luận lượt1 vẫn đúng; không biến giới hạn ấy thành P1 hoặc phủ nhận release có răng.
ĐÃ THỬ VÁ: có — đột biến trên bản sao riêng rồi phục hồi. Giữ nợ hợp lệ; khi sửa nội dung phải tự đo Git/JSON rồi tái sinh manifest. Nếu muốn mở rộng cổng, dùng dữ liệu có oracle độc lập, không test chỉ dò đúng câu. Nguy cơ thêm cổng giả kiểm chuỗi hoặc lấy lỗi dựng bản sao làm công giết mutant.
ĐÃ THỬ NGHIỆM: byte cùng kích thước ⇒ release rc2/failed đúng CHANGELOG/hash_match=false; phục hồi rc0. Bản sao ban đầu thiếu .git làm claims control và mutant đều rc2/SHA_NOT_A_COMMIT tại docs/AUDIT_LAUNCHER_VONG_3.md:462; KHÔNG tính là kill. Bổ sung .git độc lập trong scratch, không alternates: control→1016/1017→phục hồi đều rc0/ok=true/flags=[];35/36+r9/r10 cũng rc0. Chứng cứ: claims-git-results.json, new-number-mutant.json, byte-mutant.out.
ĐỘ TIN: cao

### bo-sot-toan-than-pr  [P3]  Bảng giao chưa trích thân PR, kể cả các dòng có chữ số
TỆP/DÒNG: BANG_KHANG_DINH.txt; trich_khang_dinh.py:12–18; than-pr-491.md:29–68.
VẤN ĐỀ: Đây không phải hạn chế regex: chạy script chỉ với muc-r358 cho kết quả đúng byte bảng giao; thêm than-pr tạo thêm33 dòng khẳng định có số. Những số riêng như hash d47be343,receipt94,3P1/5P2/6P3,695.9s và câu phân loại6P3 không có trong bảng. Chúng đã được tôi đo/đánh dấu không đo được ở bảng verdict này.
ĐÃ THỬ VÁ: không — khi dựng bảng gọi script với cả hai hiện vật, rồi bổ sung mệnh đề không chữ số thủ công. Khóa bằng kiểm đủ hai section nguồn và so dòng số từ mỗi nguồn. Nguy cơ nói “đã trích cả hai” thành “đã phủ hết”, trong khi regex vẫn bỏ các mệnh đề khác.
ĐÃ THỬ NGHIỆM: So byte một-input bằng BANG; hai-input có thêm35 dòng kể cả blank/header. Bản trích đầy đủ lưu review-evidence/full-extraction.txt.
ĐỘ TIN: cao

### bo-sot-hop-dong-phan-loai-nguon  [P3]  Bảng bỏ gần toàn bộ hai loại nguồn và lời hứa gắn nhãn
TỆP/DÒNG: CHANGELOG.md:10–17.
VẤN ĐỀ: Regex chỉ giữ16, bỏ10–15 và17. Bảng còn đuôi “xuất hiện…ghi nhãn tại chỗ” nhưng mất đối tượng loại(b), định nghĩa(a)/(b), số hai loại và phạm vi mọi sự kiện/mọi cross-review. Không đủ mệnh đề để kiểm lời hứa mới; P2 nguồn ở trên là lỗi nội dung, finding này là độ phủ.
ĐÃ THỬ VÁ: không — đưa cả khối vào bảng mệnh đề, cho mỗi nhóm số nhãn nguồn. Kiểm bằng chọn một phản ví dụ chưa nhãn và xem bảng có đủ phạm vi để nhận ra. Nguy cơ chỉ thêm dòng16 lần nữa hoặc đổi mọi nguồn thành “tự đo”.
ĐÃ THỬ NGHIỆM: Tái chạy regex và đọc claims-omitted.txt xác nhận thiếu10–15/17; trực tiếp đếm khối có2 loại; tìm phản ví dụ72–78/129/154.
ĐỘ TIN: cao

### bo-sot-dieu-kien-chot-so-ci  [P3]  Bảng bỏ điều kiện cần trước khi được trả con số CI
TỆP/DÒNG: CHANGELOG.md:107–109.
VẤN ĐỀ: Cả ba dòng không chữ số, nên bảng không giữ quy tắc chỉ chốt số khi completed, còn in_progress phải KHÔNG ĐO ĐƯỢC. Đây là điều kiện phạm vi của mọi số bước/skipped, không phải một số hiệu vô hại.
ĐÃ THỬ VÁ: không — bổ sung trọn mệnh đề, tách nó khỏi lời giải thích lịch sử. Khóa bằng đối chiếu nguồn pr477:181–188; nguy cơ suy tuân thủ quy tắc hôm nay là chứng minh nguyên nhân sự kiện cũ.
ĐÃ THỬ NGHIỆM: Regex bỏ107–109; đọc nguồn pr477 có cùng quy tắc, còn đòi cùng job/attempt/response đủ. Không gọi API; hành vi job thật KHÔNG ĐO ĐƯỢC.
ĐỘ TIN: cao

### bo-sot-gioi-han-du-lieu-run-json  [P3]  Bảng trích số 35 nhưng bỏ mệnh đề không lưu argv/model
TỆP/DÒNG: CHANGELOG.md:162–168, đặc biệt163 và168.
VẤN ĐỀ: Bảng giữ35 khóa cấp cao và đầu câu về object lenh, nhưng bỏ cả danh sách ba tên ở163 lẫn phủ định lưu argv/model và kết luận tự khai không chứng thực ở168. Đây là giới hạn định lượng “không có” dữ liệu dùng để chứng minh model, thiết yếu cho chính đính chính mới.
ĐÃ THỬ VÁ: không — đưa toàn mệnh đề cấu trúc/giới hạn vào bảng, tách ba khóa lenh khỏi35 khóa cấp cao. Khóa bằng parse JSON cả hai tệp và đối chiếu kiểu dữ liệu, không bằng nhãn provider. Nguy cơ biến không thấy model ở cấp cao thành kết luận không có ở cấp lồng; phép đo phải xét đủ cấu trúc.
ĐÃ THỬ NGHIỆM: Parse JSON14/15:35 khóa cấp cao,3 trong lenh; quét đệ quy khóa model/argv trả rỗng cả hai; regex bỏ163/168. Không xác thực model runtime từ các giá trị tự khai.
ĐỘ TIN: cao

Các hiện vật phép đo nằm trong `review-evidence/`: run-gates.py và *.out/*.err/*.json ghi lệnh/rc; mutation-results.json giữ cả thử nghiệm bị nhiễu ban đầu; claims-git-results.json là đối chứng hợp lệ sau khi có Git; finding-lower-bound.json giữ20 slug và tên nguồn. `git -C cay-kho status --short` cuối review rỗng. Không vá cây executor, không tự sinh lại release manifest.
