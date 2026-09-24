# #523 r13 — reconciliation và errata

Hồ sơ Executor; không phải independent verdict hoặc lời khai các lớp đã đóng.
Nguồn lịch sử được giữ nguyên. “Kế thừa/không nhập” khác “ĐÃ VÁ THẬT”.
Các phép đọc Git/hash dưới đây đo ngày23-09-2026; kết quả test của lượt cũ chỉ thuật lại.

## Nguồn chín receipt PR529

Nguồn tất cả hàng: `9683d5006e47d01e38e9ed21697911384cd80007`.
Đường dẫn: `ops/reviews/pr529-review-<vòng>-codex-verdict.receipt.yaml`.
SHA256 được tính trên blob bytes, không trên YAML parse/dump.

| Vòng | Reviewed SHA | SHA256 receipt |
|---|---|---|
| 1 | `2c466acaa8e6d3324311784ae14cda7a402b51b8` | `351883ff79d62ba01e405f1de61e0f6b148e039fd6b527db11f985f979ac97e9` |
| 2 | `f01a35033856888354136a6379d16dba8cbffcdd` | `45b780ae8352ca4679a3fd5f4db5b633c7b3729e283c4113dec62b63456cc0a0` |
| 3 | `7f028a731c9b81c7c510edc881fddfa6977291a3` | `f553f1bda58ba9a8eb669eee8e1c91e9457f1380446454e55e63872e9235fba9` |
| 4 | `a97d95c1763af30aa26750ef4d5246cfc4aa1206` | `9de63ba9e168bf0ffe5b9f5ebb821b5dbc4b750e66b9ae914b56d7d134560c89` |
| 5 | `f89f07de6c102a61dafc147e1f47025b8cecb812` | `7f33a30e665ca95d336f4d62598d282d70e384bf71867c1702df093ebf4f4649` |
| 6 | `00ac525df3f874cb0034622983c8c64f3b5ffc0a` | `d29b3174f9d1a2402002e9c39bffb9dd9c3f92e0f1e086eff0899c52449c40f6` |
| 7 | `6e7340312e01c39597f5c38df91538b022c945eb` | `a150f59e78a7a640c9ba4bb28024369163244d242440d96f2024922e67e90706` |
| 8 | `a4451ddb634da481581eea339282c1fe01c851b5` | `199c59d9117dac1ea0e40287cfa9dc29a9bcce2a1f82346d6539b1763496f283` |
| 9 | `abb79dfae7634da99a07a0c30095769973ed04d4` | `5bb82f567ddcb4b0e7d453a151375280ccbe79fb08240cb1b89c116220339a94` |

## Union17 slug lịch sử

Tập lấy từ `findings_ids` của chín receipt trên; phạm vi này không bao gồm mọi câu trong verdict.
Không dùng danh sách trích này làm trần review; mục bỏ sót reviewer tìm được vẫn là finding.
Cột vòng chỉ đếm receipt khai finding, không khẳng định lớp mở ở mọi vòng trung gian.

| Slug bất biến | Vòng có findings_ids | Disposition r13 |
|---|---|---|
| `a17-whitelist-bo-roi-m8` | 3,4 | Giữ lịch sử; kiểm lại phạm vi tương ứng của candidate theo M/N bên dưới, chưa tự cấp closure. |
| `a9-bo-sot-delta-trong-merge` | 3,4 | Giữ lịch sử; kiểm lại phạm vi tương ứng của candidate theo M/N bên dưới, chưa tự cấp closure. |
| `bien-goi-y-thanh-menh-lenh` | 2 | Giữ lịch sử; kiểm lại phạm vi tương ứng của candidate theo M/N bên dưới, chưa tự cấp closure. |
| `bien-nhan-luot-8-lan-du-lieu-luot-6` | 9 | UNRESOLVED lịch sử; giữ bytes lượt8, không dùng lại dữ liệu ấy làm phép đo mới; hồ sơ #582. |
| `bien-nhan-thieu-so-ci-da-chi` | 3,4,6,7,8,9 | UNRESOLVED lịch sử; N6 mới tách số đã chi/ngân sách, không bịa số cũ; hồ sơ #582. |
| `bo-do-bang-chi-kiem-ten-khong-kiem-nghia` | 3,4 | Giữ lịch sử; kiểm lại phạm vi tương ứng của candidate theo M/N bên dưới, chưa tự cấp closure. |
| `bo-doc-bang-vuot-ranh-gioi-muc` | 3,4 | Giữ lịch sử; kiểm lại phạm vi tương ứng của candidate theo M/N bên dưới, chưa tự cấp closure. |
| `chu-giai-lease-neo-head-cu` | 8 | Giữ lịch sử; kiểm lại phạm vi tương ứng của candidate theo M/N bên dưới, chưa tự cấp closure. |
| `con-tro-dinh-nghia-phan-hang-sai-dich` | 3 | Giữ lịch sử; kiểm lại phạm vi tương ứng của candidate theo M/N bên dưới, chưa tự cấp closure. |
| `dac-ta-r5-giu-luat-cu-trai-tieu-chi-moi` | 4,5,6,7,8,9 | Đọc nghĩa spec/lease r13 mới; không hồi tố đóng lịch sử gen10/11. |
| `dem-dot-bien-khong-theo-tieu-chi-dich` | 3,4 | Giữ lịch sử; kiểm lại phạm vi tương ứng của candidate theo M/N bên dưới, chưa tự cấp closure. |
| `doi-chung-a19-khong-chi-phoi-ket-luan` | 4 | Giữ lịch sử; kiểm lại phạm vi tương ứng của candidate theo M/N bên dưới, chưa tự cấp closure. |
| `gop-dieu-kien-dung-review-class` | 1 | Giữ lịch sử; kiểm lại phạm vi tương ứng của candidate theo M/N bên dưới, chưa tự cấp closure. |
| `mat-dau-vet-thu-hep-pham-vi` | 1 | Giữ lịch sử; kiểm lại phạm vi tương ứng của candidate theo M/N bên dưới, chưa tự cấp closure. |
| `phep-do-doctrine-khong-du-rang` | 1,2,3,4,5,6,7,8,9 | UNRESOLVED; #583 runtime/scanner, không vá trong r13. |
| `sai-dai-luong-hoi-tu` | 1,2 | Giữ lịch sử; kiểm lại phạm vi tương ứng của candidate theo M/N bên dưới, chưa tự cấp closure. |
| `thieu-hop-dong-ban-va-theo-lop` | 1 | Giữ lịch sử; kiểm lại phạm vi tương ứng của candidate theo M/N bên dưới, chưa tự cấp closure. |

## Findings PR585/586/587/597

23 comment ID là23 thể hiện, không phải23 lớp đã chứng minh độc lập.
L-A…L-M là mã của draft r13, giữ nguyên slug của draft; không đổi slug lịch sử PR529.
Full reviewed SHA theo review object API:

| PR | Review ID | Reviewed SHA của API |
|---|---|---|
| 585 | 5268688511 | `27283d2e6ed57a6e97bf45e3179c157a59f0ff86` |
| 586 | 5270670271 | `816efabf91c9a4a29a89c09e267a7a6975e62e59` |
| 587 | 5268796536 | `0babf614ceda9ffc1ec230cc4752c5384d5ba8a4` |
| 597 | 5269392593 | `2babb1a5f37d2a8d67589a3ce7aedd02e4a5aa9c` |

| ID | Slug đối chiếu | Nguồn finding | Disposition/phạm vi evidence |
|---|---|---|---|
| L-A | `adapter-loai-duong-human-audited` | [4063796123](https://github.com/ducthangho/tra-luat/pull/585#discussion_r4063796123) | Không nhập câu sai585; canonical §8 giữ human_audited. |
| L-B | `mien-review-sau-moi-lan-doi-head` | [4063796133](https://github.com/ducthangho/tra-luat/pull/585#discussion_r4063796133) | Không nhập miễn review cho mọi head; §8/§13 vẫn neo exact SHA. |
| L-F | `do-drift-tren-ref-cuc-bo-stale` | [4063796139](https://github.com/ducthangho/tra-luat/pull/585#discussion_r4063796139) | Không nhập lệnh stale585; tiếp tục full ref fence §5.1/§13. |
| L-E | `M5-tinh-ty-le-bang-finding-khong-phai-lop` | [4063796144](https://github.com/ducthangho/tra-luat/pull/585#discussion_r4063796144) | §8.3/§12 dùng tập lớp mở vòng trước; biểu hiện đếm riêng. |
| L-C | `dieu-kien-dung-bo-quen-P0` | [4063796153](https://github.com/ducthangho/tra-luat/pull/585#discussion_r4063796153) | Protocol r13 bổ sung rõ P0 chặn approval; không thay assurance/class. |
| L-D | `cam-tuyet-doi-workflow-dispatch` | [4063796158](https://github.com/ducthangho/tra-luat/pull/585#discussion_r4063796158) | Không nhập lệnh cấm tuyệt đối; §10.2 + quyền Packet quyết định CI. |
| L-G | `khang-dinh-am-PR-512-khong-neo-run-id` | [4063796169](https://github.com/ducthangho/tra-luat/pull/585#discussion_r4063796169) | Không kế thừa khẳng định âm #512. Số CI cả đời #512 chưa đo. |
| L-H | `suy-hoi-tu-tu-ty-le-bo-qua-lop-moi` | [4063796185](https://github.com/ducthangho/tra-luat/pull/585#discussion_r4063796185) | §12: tỷ lệ cao không tự thành hội tụ; lớp mới báo riêng. |
| 586-A | `review-target-identity` | [4065435191](https://github.com/ducthangho/tra-luat/pull/586#discussion_r4065435191) | Tách head816efab khỏi synthetic được lời review nhắc; chỉ kết luận trên đối tượng đã đo. |
| 586-B | `frozen-acceptance-changed` | [4065435204](https://github.com/ducthangho/tra-luat/pull/586#discussion_r4065435204) | Không sửa r12 đã freeze; r13 là hợp đồng mới, audit r12 không chuyển sang. |
| L-I | `renewal-moves-acceptance-baseline` | [4063885398](https://github.com/ducthangho/tra-luat/pull/587#discussion_r4063885398) | Giữ395bc7b; continuation18d42ca riêng; không sửa lease cũ. |
| L-J | `unverifiable-spec-source` | [4063885408](https://github.com/ducthangho/tra-luat/pull/587#discussion_r4063885408) | Lease mới neo full spec OID/path/SHA256; không suy từ tên branch. |
| L-K | `unanchored-authority-parameter` | [4063885415](https://github.com/ducthangho/tra-luat/pull/587#discussion_r4063885415) | Expiry mới neo run90phút và projection5790051119; không hợp thức12h lịch sử. |
| L-L | `false-measurement-anchor` | [4063885422](https://github.com/ducthangho/tra-luat/pull/587#discussion_r4063885422) | Không dùng line1947 hay1847 làm source ID; đọc function lenh_ai_dang_giu tại OID canonical. |
| L-M | `revision-trigger-understatement` | [4063885435](https://github.com/ducthangho/tra-luat/pull/587#discussion_r4063885435) | Spec r13 liệt kê đúng sáu trigger §3.2; không gọi reviewer/assurance là tên trigger. |
| 597-A | `anchor-ancestry` | [4064390019](https://github.com/ducthangho/tra-luat/pull/597#discussion_r4064390019) | Anchor5c9abef là tổ tiên head thật2babb1a (rc0). Commit4895b646 trong prose không có local; API422. Không chuyển lỗi synthetic đó sang head thật. |
| 597-B | `global-assurance-overclaim` | [4064390021](https://github.com/ducthangho/tra-luat/pull/597#discussion_r4064390021) | Chưa đo hết model/AG thì không kết luận toàn bộ cross-provider bất khả dụng; human audit lịch sử là sự kiện riêng. |
| 597-C | `denominator-scope` | [4064390029](https://github.com/ducthangho/tra-luat/pull/597#discussion_r4064390029) | 166/170 là phân vùng landed theo lời review,171 gồm candidate; chưa đo lại toàn bộ partition thì giữ thuật lại, không gọi số hiện hành. |
| 597-D | `stale-blob-hash-command` | [4064390036](https://github.com/ducthangho/tra-luat/pull/597#discussion_r4064390036) | Đã đo hai blob khác hash/size; xem bảng bên dưới. Lệnh hash phải lấy OID của evidence_url. |
| 597-E | `reviewed-sha-durability` | [4064390042](https://github.com/ducthangho/tra-luat/pull/597#discussion_r4064390042) | 27283d2 tồn tại local nhưng không thuộc canonical18d42ca (rc1); chưa xác minh protected archival ref. Không nhận audit cũ làm bằng chứng r13. |
| 597-F | `newline-layer-attribution` | [4064390048](https://github.com/ducthangho/tra-luat/pull/597#discussion_r4064390048) | Không quy final-LF cho GitHub khi thiếu raw request/transport proof; không sửa audit gốc. |
| 597-G | `parent-count-not-merge-method` | [4064390058](https://github.com/ducthangho/tra-luat/pull/597#discussion_r4064390058) | Một parent chỉ là topology; chưa đủ xác định squash/non-squash. Review cần counterexample riêng. |
| 597-H | `executions-vs-anchor-count` | [4064390064](https://github.com/ducthangho/tra-luat/pull/597#discussion_r4064390064) | Theo block nguồn:4 executions/3 unique anchor OID; không gọi đó là3executions. Không suy execution thiếu log đã pass. |

Mã586-A/B và597-A…H chỉ là chỉ mục ledger, không tự đổi tên finding nguồn hoặc gộp23 thể hiện thành23 lớp.
PR585 +201 dòng chưa land; tránh nhập chúng không đóng nợ scanner/hồ sơ và không là sửa deployed bug.

### Blob hash đo riêng cho597-D

Path: `ops/reviews/wp523-slice-r12-human-audit-verdict.md`.
Lệnh: `git show <OID>:<path>` capture bytes bằng subprocess, rồi SHA256; native rc0 cho cả ba.

| OID | Bytes | SHA256 |
|---|---|---|
| `7da12e6f1ac0f970a971917f655262e65a9511c9` | 4606 | `a60dededaf7c5a7a8c63c995a116bc1c7d775ba5f0acf1df9906c7e3db331e82` |
| `5c9abef1ef36de50a52182064da8675b2e71a9ef` | 5333 | `3cef5f6ebb31246b4cddf3b79b42a5febf53bc759cf26360526b5d8d838f54e2` |
| `2babb1a5f37d2a8d67589a3ce7aedd02e4a5aa9c` | 5333 | `3cef5f6ebb31246b4cddf3b79b42a5febf53bc759cf26360526b5d8d838f54e2` |

## M1–M17: disposition nghĩa vụ

| Mục | Nội dung được giữ hoặc thay theo scope r13 |
|---|---|
| M1 | Review class/assurance theo §8; P0 chặn approval, severity còn lại theo class/Packet; r13 cần0P1/P2/P3 trong scope. |
| M2 | Sensitive không có finding chưa tự đủ approval; final human audit exact SHA. |
| M3 | Bảng lớp và phương án vá theo cơ chế ở §8.3; adapter minh họa schema trình bày. |
| M4 | Tái diễn đếm theo vòng, không theo số finding trong một vòng; §12. |
| M5 | Đổi công thức theo lớp; mẫu số0 N/A; không suy hội tụ từ tỷ lệ cao; §12. |
| M6 | Scope-cut/chưa đo không vào tử số fixed; giữ slug/nợ. |
| M7 | Phân loại chi CI, run IDs và budget theo §10.2/spec; không cấm dispatch được cấp. |
| M8 | Đo remote fence theo §5.1/§13; candidate đổi head cần review mới; không merge drift ngoài quyền. |
| M9 | Giữ hậu-merge gates; rút miễn review cho mọi head. §8/§13 phân biệt candidate và canonical merge. |
| M10 | Targeted trước; full khi ready/admission theo owner; N không tự bằng số đã chi. |
| M11 | Raw verdict+v2receipt+index mới trên evidence branch riêng. Chưa giao đủ thì chưa hoàn tất M11. |
| M12 | Số đã chi/run IDs riêng ngân sách; measured empty khác unknown. Không sửa receipt cũ. |
| M13 | Giữ adapter canonical; quy tắc chung mới vào protocol theo scope owner chấp thuận. |
| M14 | Reviewer độc lập chứng minh rút gọn còn phân biệt phản chứng, không chỉ matching headings. |
| M15 | Kiểm từng đích con trỏ thêm; không có khái niệm thì chưa đo/nợ, không trỏ bừa. |
| M16 | Reviewer tự dựng phép đo; các số/script Executor là input, không thay independent verdict. |
| M17-GO | Không dựng lại cổng quét tên. Đọc nghĩa spec/lease mỗi lượt; không suy scanner sạch là semantic coverage. |

## N1–N8: giới hạn nghiệm thu

| Mục | Phạm vi trong r13 |
|---|---|
| N1 | Nếu dùng bộ chấm phản chứng, phải đủ target/non-target observations; setup failure không là kill. Không xây scanner mới. |
| N2 | Audit từng đơn vị nghĩa, không cho câu đứng kề whitelist được hợp thức hóa; semantic review riêng với category match. |
| N3 | Whole diff trước lọc; immutable baseline, inherited canonical và packet overlay ghi riêng;3productfiles≤300adds. |
| N4 | Đối chứng dương/âm phải chi phối kết luận; không chỉ xuất hiện trong log. |
| N5 | Mỗi con trỏ thêm phải có đích chứa khái niệm; mục con/line wrapping không làm phép đọc giả đỏ. |
| N6 | Budget và đã chi/run IDs/cửa sổ đo tách riêng. Lịch sử chưa đủ giữ unknown. |
| N7 | Văn bản thiếu để dựng phép đo thì blocked, không reviewer tự đoán acceptance. |
| N8 | Không đo được không pass; schema-pass không tự là semantic-pass. |

## Budget, CI và phần chưa hoàn tất

Giữ override lịch sử attempts3→10/same_failure2→10 theo comment5646812840; không suy thành Codex-call override.
PR529 có9 receipt đã trích, không đồng nhất9receipt với toàn bộ physical invocations.
PR585 API review5268688511 là một known call; lần technical review r13 kế tiếp reserve call thứ hai của công việc này.
Số invocation cả lịch sử chưa đủ dữ liệu để kiểm đếm: UNKNOWN, không reset sang0.
CI đo bổ sung trước review của run06:12:28Z ngày23-09:0 được gọi bởi Executor; ngân sách full khi ready khai riêng trong CI plan.
Không dùng số0 của run mới thay chi cả đời523. Các automation metadata (đăng lease) ghi riêng, không gọi full oracle.
M11 artifacts, final exact-SHA human audit, required CI và land/bookkeeping chưa xong tại lúc dựng ledger.
Các nợ583/582/566 không bị đóng bởi candidate này; #523/mission499 không tự complete khi slice land.
