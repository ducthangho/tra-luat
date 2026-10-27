verdict: changes_requested
reviewed_sha: 82359c4deec90edebbaebf9ab9d094902120b567
Kết quả: 0 P0, 2 P1, 1 P2, 0 P3.

## KẾT LUẬN VỀ FINDING CŨ
- P1 verdict-surface-bo-sot-pr889-luot1 (lượt 2): **ĐÃ ĐÓNG**. Tại 82359c4, receipt có caveat và README có hàng cảnh báo đúng dòng 7, run `9f946d714c2344fa9691c3d7d4f1b2d9`, run.json:47 `codex_cli`, chương trình `codex`, header `OpenAI Codex v0.163.0`. Verdict 75193 byte, SHA256 `6aa03cacbde6f33a41ba4af60e408b2c742da5959390f28a9cf8420b5cb098f5`, khớp receipt/SHA256SUMS và giữ nguyên từ cha. Tái áp nguyên HINT lượt 2 trên hai tệp ở cha tạo đúng blob của 82359c4. **Lớp lỗi chưa hết toàn kho**: wp766 còn biểu hiện có run JSON bác bỏ, và 13 cặp tự khai service/receipt CLI thiếu điều kiện nguồn được ghi riêng dưới đây.

## BẢNG ĐO
| khẳng định | bên giao khai | đo được (lệnh) | khớp? |
|---|---|---|---|
| HEAD/tree, không shallow | 82359c4, cây đầy đủ | `git rev-parse HEAD HEAD^{tree}` = 82359c4… / 32cf81c2614a91c7ced8fc77781b01dcb12fc8a7; `--is-shallow-repository` false; status đầu rỗng | Có |
| Diff bản vá và toàn PR | 2 tệp +5 dòng; PR so master 356eb26 | `python3 evidence/history_audit.py`: cả diff.patch/numstat.txt/diff-pr947.patch/numstat-pr947.txt equals_supplied=True | Có |
| Áp NGUYÊN HINT lượt 2 | patch -p0 --fuzz=0 trên cha 578fb4b | `python3 evidence/validate_hint.py`: old_hint_rc=0, cả hai target_blob_match=True | Có |
| Caveat mới dẫn nguồn | verdict:7, run 9f946d71, run.json:47, CLI v0.163.0 | `python3 evidence/old_p1_audit.py`: đúng nguyên câu service/phủ nhận codex exec; JSON CLI/program codex; header khớp | Có |
| README của P1 cũ | Một hàng nâng caveat | Cùng script: README_matching_rows=1; đúng nguyên caveat receipt | Có |
| Byte verdict pr889-review-1 | 75193, 6aa03cac… | Cùng script: đủ SHA256 như kết luận; flat_equals_directory=True, unchanged_since_parent=True, sha256sum_rc=0 (23 mục OK) | Có |
| Quét mọi verdict tự khai service | Không chỉ nhóm #870/#889 | 267 verdict; 12 tệp chứa codex_service = 10 tự khai + 2 chỉ mô tả finding; 5/10 đã đính chính, 4/10 ci-g5 có caveat không đo được, 1/10 wp766 còn sót (surface_audit.py) | Không: P1 wp766 |
| Các cách viết service/API khác | Cần quét cả tên diễn giải | service_spelling_audit.py: 13 cặp service/receipt CLI; tìm mọi run.json không có run_id tương ứng (service-runtime-search.log) | Không: P2 thiếu điều kiện |
| Verdict lượt 2 nguyên byte | 66095 byte, a2b588b6… | receipt_audit.py: SHA256 a2b588b64535203f9e481240e7f014ae0f34f84b8a776e646b573666e5bd689f; phẳng = thư mục = verdict-cu | Có |
| Finding count lịch sử | changes_requested 0/1/0/0 | Header verdict dòng 1/3 khớp so_p0/1/2/3 = 0/1/0/0; reviewed SHA vẫn 8d56009 | Có, lịch sử |
| reviewed_sha/tree/base | 8d56009 / e9330554… / 50a59a9… | receipt_audit.py: OID đủ khớp run.head, git tree; 3bc4244^ = base; 21fe565^2 = reviewed_sha | Có |
| Hai bản vá được review | 3bc4244 và cc0a3c9..a9bc934 | history_audit.py: hai commit là ancestor của 8d56009, rc=0; historical-diffs.log: diff/numstat của cả hai khớp byte | Có |
| Run metadata lượt 2 | launcher 1.5.0, xong, rc0, 600.539, clean=true, CLI | receipt_audit.py: đủ các trường khớp; duration theo timestamp 600.539266, làm tròn 600.539 | Có, metadata của run |
| Prompt lượt 2 | 64404d73… | SHA256 PROMPT.md = 64404d73a93d9f43878adc436e1cbe761a5f930cdf011a793e31b896b166812a = run.prompt_sha256 | Có |
| Model phục vụ được lưu | 25 sự kiện, 25 response_id khác nhau, gpt-6.1-sol | receipt_audit.py: events=25 / unique_response_id=25; 25 response.created và 25 gpt-6.1-sol; trạng thái DO_DUOC | Có ở trace launcher được lưu |
| Serving effort / cờ CLI đầy đủ / session independence | xhigh là yêu cầu; lệnh CLI và phiên độc lập được thuật lại | run.json chỉ lưu chương trình/số đối số/van_tay; stderr trong kho chỉ có hai dòng Reading additional input; không có nguồn độc lập cho toàn argv, phiên bản CLI hay serving effort/session | KHÔNG ĐO ĐƯỢC lại; không suy thêm |
| stdout/stderr của run | 254 / 78 byte và hash trong JSON | receipt_audit.py: byte/hash hai stream đều khớp đầy đủ; phần stderr bị bỏ ghi riêng 27643975 byte/320518 dòng | Có; không phục dựng được phần bỏ |
| Evidence URL ghim commit chỉ mang hiện vật | 25e7d1167856c3beea2552f49a6c1ded0a128fdf | git diff-tree: 108 path chỉ trong thư mục lượt 2 + verdict phẳng; evidence_blob_equal=True; không có receipt/README/land trong commit đó | Có, blob Git local; không gọi mạng |
| SHA256SUMS lượt 2 | Tệp được lưu có băm | sha256sum -c SHA256SUMS tại thư mục: rc=0, 106/106 mục OK; log evidence/pr896-r2-sha256.log | Có |
| OMITTED.txt | snapshot 1056144 byte/sha256 fca16267…, bỏ copy/ | receipt_audit.py: snapshot/copy vắng; 107 tệp hiện tại, lớn nhất 73441 byte; không còn byte gốc để hash lại | Đo được sự vắng; hash/byte tệp bỏ KHÔNG ĐO ĐƯỢC |
| Năm hàng README lượt 2 | 4 cảnh báo + 1 mục lục | receipt_audit.py: row_count=5; 3 cảnh báo về checkout/driver/OMITTED khớp hiện vật; cảnh báo HINT và vế HINT ở mục lục đã cũ | Một phần: P1 trạng thái HINT |
| Khối land lượt 2 không sửa dòng cũ | Chỉ nối cuối | history_audit.py: prefix_preserved=True tại commit 765ae89 và so master 356eb26; sau ghi sổ byte khối không đổi | Có |
| Trạng thái/đơn vị land | landed false; CHUA DAT; cần chủ kho chấp nhận | YAML parse: False / CHUA DAT; don_vi_land_de_xuat có CAN chu kho chap nhan, KHONG tu chon | Có; chỉ là đề xuất |
| HINT chưa áp / caveat vẫn thiếu | receipt:111–114; README:731/1028; land:234/242 | history_audit.py: caveat_count 0 ở 578fb4b, 1 ở 82359c4; old-HINT tái áp tạo đúng blob target | Không hiện hành: P1; đúng ở 765ae89/578fb4b |
| t26 nền | Cần N/N hai số bằng nhau | python3 ops/lease_publish_test.py --chi-ca=t26_: rc0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0 | Có |
| t27 nền | Cần N/N hai số bằng nhau | python3 ops/lease_publish_test.py --chi-ca=t27_: rc0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0 | Có |
| t138 nền | Cần N/N hai số bằng nhau | python3 ops/lease_publish_test.py --chi-ca=t138_: rc0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0 | Có |
| Bỏ hàng README mới | Chốt phải đo lại cho bản vá này | mutations.py trên clone mirror.git checkout 82359c4: t26 rc0 1/1; t27 rc1 0/1; t138 rc0 1/1 | Chỉ t27 có răng |
| Bỏ caveat receipt mới | Không suy nền xanh = đủ caveat | Cùng clone, khôi phục README trước: t26/t27/t138 đều rc0 1/1 | Cả ba không có răng với bỏ caveat |
| bien_nhan_v2 | Đo tại cay-kho exact SHA | python3 ops/bien_nhan_v2.py --root .: rc0; 236 ĐẠT v2, 11/11 legacy, 42 NỢ, 0 vi phạm, 0 KHÔNG ĐO ĐƯỢC, tổng289; TỔNG: ĐẠT | Đạt gate, không chứng minh ngữ nghĩa mọi câu |
| land_evidence_nguon | Đo tại cay-kho exact SHA | python3 ops/land_evidence_nguon.py --root .: rc0; 47 ĐẠT, 26/28 miễn trừ, 0 vi phạm/0 KHÔNG ĐO ĐƯỢC, tổng73; TỔNG: ĐẠT | Đạt gate |
| doctrine-scan | Đo tại cay-kho exact SHA | python3 .claude/dev/packet_loop.py doctrine-scan --root .: rc0; sạch — đã quét 10 tệp, 0 chỗ chép doctrine | Đạt gate |
| doc-claims-check | Phải ok:true | python3 scripts/tl.py doc-claims-check --json: rc0; JSON parse ok=True, strict=False | Đạt gate |
| Secret scan hiện vật lượt 2 | Đo đúng thư mục | python3 scripts/pkg_secret_scan.py ops/reviews/pr896-review-2-codex: rc0, stdout/stderr rỗng; main() trả 0 khi hits rỗng, không in summary khi sạch | Đạt theo giao diện lệnh |
| HINT mới | Gợi ý, chưa áp cây giao review | validate_hint.py: dry-run/apply --fuzz=0 rc0 trên clone; t26/t27/t138 rc0 1/1; hai gate receipt/land TỔNG: ĐẠT; 17 tệp tài liệu/receipt | Đã thử trên clone |

## BẢNG SĂN
Mỗi hướng bên dưới có giả thuyết, lệnh, output thật và kết luận; log/script giữ tại `evidence/` ngoài cây được review. Khi không ghi cwd khác, lệnh kiểm kho chạy tại `cay-kho/`; script audit chạy tại thư mục chứa PROMPT.md.

### HƯỚNG 1: Định danh cây và phạm vi bản vá
- giả thuyết: cây giao sai SHA hoặc bản vá sửa byte verdict lịch sử.
- lệnh: `git -C cay-kho rev-parse HEAD HEAD^{tree}`; `git -C cay-kho status --porcelain=v1 --ignored`; `git -C cay-kho rev-parse --is-shallow-repository`; `git -C cay-kho diff 578fb4b 82359c4 --stat`.
- output thật: HEAD `82359c4deec90edebbaebf9ab9d094902120b567`; tree `32cf81c2614a91c7ced8fc77781b01dcb12fc8a7`; status rỗng; shallow `false`. Bản vá có 2 tệp, 5 insertions(+): README +1; receipt pr889-review-1 +4; không sửa verdict.
- kết luận: KHÔNG PHẢI LỖI. Snapshot đầu lưu `evidence/start-snapshot.json`; kiểm cuối sẽ đối chiếu nội dung, kể cả ignored. Chỉ thị read-only không chứng minh chưa từng ghi rồi hoàn nguyên.

### HƯỚNG 2: Đối chiếu bản vá P1 cũ với nguồn và băm verdict
- giả thuyết: caveat mới dẫn sai dòng/run/header hoặc sửa verdict lịch sử.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/old_p1_audit.py` (đọc receipt/run/header/SHA256, `git show 578fb4b:ops/reviews/pr889-review-1-codex-verdict.md`, và `sha256sum -c SHA256SUMS` tại thư mục hiện vật).
- output thật: `run_id=9f946d714c2344fa9691c3d7d4f1b2d9` (xem log để lấy nguyên ID); `run.json:47 "execution_surface": "codex_cli"`; `program=codex`; `OpenAI Codex v0.163.0`; README có đúng 1 hàng mới. `flat_equals_directory=True`, `unchanged_since_parent=True`; `sha256sum rc=0`, mọi mục `OK`. SHA256/bytes xem `evidence/old-p1.log`.
- kết luận: KHÔNG PHẢI LỖI. Caveat dẫn đúng dòng 7 và sửa nghĩa surface, không chứng nhận model/effort, không đổi assurance. P1 lượt 2 ĐÃ ĐÓNG đối với hiện vật pr889-review-1; việc quét toàn lớp được đo riêng ở hướng tiếp theo.

#### Chạy nền t26_
Lệnh tại `cay-kho/`: `PYTHONDONTWRITEBYTECODE=1 python3 ops/lease_publish_test.py --chi-ca=t26_`; rc=0. Output thật:
```text
/tmp/claude-0/-home-user-tra-luat/6311a229-c7eb-5096-a819-78ab343b359f/scratchpad/cr-pr896-r3/cay-kho/ops/lease_publish_test.py:2961: SyntaxWarning: invalid escape sequence '\s'
  2. **Nhận nhầm văn xuôi.** `^\s*#.*NỢ CÓ TÊN` cho phép chữ tuỳ ý chen trước cụm, nên một
/tmp/claude-0/-home-user-tra-luat/6311a229-c7eb-5096-a819-78ab343b359f/scratchpad/cr-pr896-r3/cay-kho/ops/lease_publish_test.py:5104: SyntaxWarning: invalid escape sequence '\d'
  KHÔNG neo đầu dòng là `lease_publish: (\d+)/(\d+) đạt`, và nó đọc BẢN RIÊNG trong tệp chứ
>>> vao t26_moi_bien_nhan_review_phai_khop_BAM_tep_no_tro_toi 2026-10-26T06:17:47Z
<<< ra t26_moi_bien_nhan_review_phai_khop_BAM_tep_no_tro_toi 1.985s QUA

lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
```

#### Chạy nền t27_
Lệnh tại `cay-kho/`: `PYTHONDONTWRITEBYTECODE=1 python3 ops/lease_publish_test.py --chi-ca=t27_`; rc=0. Output thật:
```text
/tmp/claude-0/-home-user-tra-luat/6311a229-c7eb-5096-a819-78ab343b359f/scratchpad/cr-pr896-r3/cay-kho/ops/lease_publish_test.py:2961: SyntaxWarning: invalid escape sequence '\s'
  2. **Nhận nhầm văn xuôi.** `^\s*#.*NỢ CÓ TÊN` cho phép chữ tuỳ ý chen trước cụm, nên một
/tmp/claude-0/-home-user-tra-luat/6311a229-c7eb-5096-a819-78ab343b359f/scratchpad/cr-pr896-r3/cay-kho/ops/lease_publish_test.py:5104: SyntaxWarning: invalid escape sequence '\d'
  KHÔNG neo đầu dòng là `lease_publish: (\d+)/(\d+) đạt`, và nó đọc BẢN RIÊNG trong tệp chứ
>>> vao t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc 2026-10-26T06:17:49Z
<<< ra t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc 4.126s QUA

lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
```

#### Chạy nền t138_
Lệnh tại `cay-kho/`: `PYTHONDONTWRITEBYTECODE=1 python3 ops/lease_publish_test.py --chi-ca=t138_`; rc=0. Output thật:
```text
/tmp/claude-0/-home-user-tra-luat/6311a229-c7eb-5096-a819-78ab343b359f/scratchpad/cr-pr896-r3/cay-kho/ops/lease_publish_test.py:2961: SyntaxWarning: invalid escape sequence '\s'
  2. **Nhận nhầm văn xuôi.** `^\s*#.*NỢ CÓ TÊN` cho phép chữ tuỳ ý chen trước cụm, nên một
/tmp/claude-0/-home-user-tra-luat/6311a229-c7eb-5096-a819-78ab343b359f/scratchpad/cr-pr896-r3/cay-kho/ops/lease_publish_test.py:5104: SyntaxWarning: invalid escape sequence '\d'
  KHÔNG neo đầu dòng là `lease_publish: (\d+)/(\d+) đạt`, và nó đọc BẢN RIÊNG trong tệp chứ
>>> vao t138_A12_bien_nhan_receipt_du_truong_va_neo_doc_lap_cay_PR 2026-10-26T06:17:54Z
<<< ra t138_A12_bien_nhan_receipt_du_truong_va_neo_doc_lap_cay_PR 0.185s QUA

lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
```

#### Gate 1
Lệnh tại `cay-kho/`: `PYTHONDONTWRITEBYTECODE=1 python3 ops/bien_nhan_v2.py --root .`; rc=0. Output cuối (toàn bộ ở `evidence/gate-1.log`):
```text

bien_nhan_v2: 236 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 289
TỔNG: ĐẠT
```

#### Gate 2
Lệnh tại `cay-kho/`: `PYTHONDONTWRITEBYTECODE=1 python3 ops/land_evidence_nguon.py --root .`; rc=0. Output cuối (toàn bộ ở `evidence/gate-2.log`):
```text
ĐẠT ops/land/pr924-wp923-land-evidence.yaml
ĐẠT ops/land/pr926-wp919-land-evidence.yaml
ĐẠT ops/land/pr930-wp752-wp763-land-evidence.yaml
ĐẠT ops/land/pr931-wp835-land-evidence.yaml
ĐẠT ops/land/pr932-wp748-r26-land-evidence.yaml
ĐẠT ops/land/pr933-wp929-land-evidence.yaml
land_evidence_nguon: 47 ĐẠT · 26/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 73
TỔNG: ĐẠT
```

#### Gate 3
Lệnh tại `cay-kho/`: `PYTHONDONTWRITEBYTECODE=1 python3 .claude/dev/packet_loop.py doctrine-scan --root .`; rc=0. Output cuối (toàn bộ ở `evidence/gate-3.log`):
```text
doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine
```

#### Gate 4
Lệnh tại `cay-kho/`: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/tl.py doc-claims-check --json`; rc=0. Output cuối (toàn bộ ở `evidence/gate-4.log`):
```text
    "layers_bac": {
      "L10": "24/30 version GAS được dẫn không có tệp .gs — kho giữ 6 bản gần nhất là có chủ đích",
      "L11": "2/2 hit ở tài liệu sống đều viết ĐÚNG (số hiệu chính thức là dạng bare); bất biến NN-YYYY-VBHN-XXX áp cho khoá registry, đã có cổng vbhn-year-fix"
    },
    "note": "tập tra cứu = CHANGELOG.md + references/changelog_archive/*.md, quét toàn văn; dưới sàn ⇒ advisory (khuyết của sổ, không phải trích dẫn sai)"
  },
  "strict": false
}
```

#### Gate 5
Lệnh tại `cay-kho/`: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/pkg_secret_scan.py ops/reviews/pr896-review-2-codex`; rc=0. Output cuối (toàn bộ ở `evidence/gate-5.log`):
```text

```

### HƯỚNG 7: delete_README_row trên bản sao exact SHA
- giả thuyết: bỏ hàng README mới sẽ làm cả ba ca đỏ.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/mutations.py` (clone cục bộ từ `mirror.git`, checkout `82359c4`; chỉ đổi tài liệu/receipt).
- output thật:
```text
{"mutation": "delete_README_row", "selector": "t26_", "rc": 0, "summary": ["lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0"]}
{"mutation": "delete_README_row", "selector": "t27_", "rc": 1, "summary": ["lease_publish: 0/1 đạt; đã chạy=1, bỏ qua=0"]}
{"mutation": "delete_README_row", "selector": "t138_", "rc": 0, "summary": ["lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0"]}
```
- kết luận: KHÔNG PHẢI LỖI. t27 có răng với hàng README khi caveat còn; t26/t138 không có răng với hàng này.

### HƯỚNG 8: delete_receipt_caveat trên bản sao exact SHA
- giả thuyết: bỏ caveat receipt mới sẽ làm cả ba ca đỏ.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/mutations.py` (clone cục bộ từ `mirror.git`, checkout `82359c4`; chỉ đổi tài liệu/receipt).
- output thật:
```text
{"mutation": "delete_receipt_caveat", "selector": "t26_", "rc": 0, "summary": ["lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0"]}
{"mutation": "delete_receipt_caveat", "selector": "t27_", "rc": 0, "summary": ["lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0"]}
{"mutation": "delete_receipt_caveat", "selector": "t138_", "rc": 0, "summary": ["lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0"]}
```
- kết luận: KHÔNG PHẢI LỖI của lời khai đã giới hạn; cả t26/t27/t138 không có răng với việc bỏ caveat. Không dùng nền xanh để suy phát hiện đủ mâu thuẫn surface.

### HƯỚNG 3: Quét toàn bộ verdict và phân biệt tự khai với trích finding
- giả thuyết: P1 đã được vá hết mọi biểu hiện trong `ops/reviews/*-verdict.md`.
- lệnh: `rg -n codex_service cay-kho/ops/reviews/*-verdict.md > evidence/grep-codex-service.log`; `rg -n 'execution_surface:|execution surface|execution_surface `|reviewer_execution_surface:' cay-kho/ops/reviews/*-verdict.md > evidence/grep-all-surfaces.log`; đọc YAML của từng ứng viên và run JSON nó trỏ tới.
- output thật: 267 verdict; 12 tệp chứa `codex_service`. Năm tệp #870/#889 tự khai sai đã có caveat. Bốn verdict ci-g5 lượt 2/4/6/8 có caveat `KHONG-CO-run.json-RUNTIME-KHONG-DO-DUOC`, ghi riêng `surface_tu_khai_trong_verdict`, surface CLI chỉ là THUẬT LẠI, không có run để phân xử. Hai tệp pr915-review-1/pr896-review-2 chỉ NHẮC `codex_service` khi mô tả finding; không phải tự khai. Tệp còn lại wp766-r1-g1-exec-review-1-codex-verdict.md:12 tự khai `codex_service`; run_id `5d4f7321d9a04ee1a87934e41fcf45c8`, `lenh.chuong_trinh=codex`, `execution_surface=codex_cli`; receipt.surface=codex_cli; caveat chỉ có `CHECKOUT-GHI-DUOC-KHONG-CUONG-CHE-READ-ONLY` và `DRIVER-DO-DOC-CAY-TAM`.
- kết luận: LỖI, một P1 khác cùng lớp còn sót ở wp766; không mở lại P1 đã đóng của pr889-review-1 và không quy kết bốn ca ci-g5 thiếu bằng chứng runtime.

### HƯỚNG 4: Receipt lượt 2 — băm, SHA/tree/base và mỏ neo commit
- giả thuyết: PR #947 khai sai byte, finding count, cây đã review hoặc commit evidence chỉ mang hiện vật.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/receipt_audit.py > evidence/receipt-audit.log`.
- output thật: SHA256 `a2b588b64535203f9e481240e7f014ae0f34f84b8a776e646b573666e5bd689f`; 66095 byte; bản phẳng = bản thư mục = verdict-cu (`True`); header `changes_requested`, `0 P0, 1 P1, 0 P2, 0 P3` khớp receipt. reviewed_sha = run.head = `8d56009a09af7b3ef93801df105f9483de212cc7`; tree `e93305541ae7d7f87fa5c57dd610fa1be829b0f7`; base = `3bc4244^` = `50a59a945026a2ab2f97dc0e7ef7b5a540e17652`. `21fe565^2` = reviewed_sha. Commit evidence `25e7d1167856c3beea2552f49a6c1ded0a128fdf` thay 108 path, `artifact_only=True`, `other_paths=[]`, `evidence_blob_equal=True`.
- kết luận: KHÔNG PHẢI LỖI. Đây là verdict lịch sử trên 8d56009, không phải approve cho 82359c4.

### HƯỚNG 5: Model/run metadata và giới hạn dữ liệu bỏ khỏi kho
- giả thuyết: số sự kiện/response ID hoặc dữ liệu đã bỏ không khớp lời khai.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/receipt_audit.py`.
- output thật: launcher 1.5.0; run b3269a02045c4e178b1c5c328b671273; rc=0, xong; duration 600.539 (hai timestamp trừ nhau 600.539266); worktree_sach=True; surface codex_cli. Prompt SHA256 `64404d73a93d9f43878adc436e1cbe761a5f930cdf011a793e31b896b166812a` khớp. `events=25 unique_response_id=25 models={'gpt-6.1-sol': 25} event_types={'response.created': 25}`. stdout 254 byte, stderr 78 byte, cả hai băm khớp run. `original-snapshot-present=False copy-present=False`; thư mục có 107 tệp, tệp lớn nhất 73441 byte; README có 5 hàng của lượt 2.
- kết luận: KHÔNG PHẢI LỖI của các số đo trên. `OMITTED.txt` khai snapshot 1056144 byte, sha256 `fca16267b398120bdb79a51237f78ea216949039968c1dcedbae6a9b900932ff`, và bản sao copy/ không đưa vào kho; đo được sự vắng mặt, KHÔNG ĐO ĐƯỢC lại băm/byte của tệp đã bỏ chỉ từ SHA này. Không suy thêm serving effort hay tính độc lập session từ 25 dòng metadata.

### HƯỚNG 6: Ba ca nền và năm gate bắt buộc
- giả thuyết: rc=0 che thất bại hoặc thiếu bằng chứng dương.
- lệnh/output: xem từng lệnh và output thật đã nối ở trên, cùng `evidence/baseline-t26_.log`, `baseline-t27_.log`, `baseline-t138_.log`, `gate-1.log` đến `gate-5.log`.
- output thật: t26/t27/t138 từng ca rc=0, `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0`. bien_nhan_v2 rc=0: `236 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 289`, `TỔNG: ĐẠT`. land_evidence_nguon rc=0: `47 ĐẠT · 26/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 73`, `TỔNG: ĐẠT`. doctrine-scan rc=0: `sạch — đã quét 10 tệp, 0 chỗ chép doctrine`. doc-claims-check rc=0, JSON được xác minh riêng. pkg_secret_scan rc=0, stdout rỗng (giao diện lệnh không in dòng kết luận khi sạch).
- kết luận: KHÔNG PHẢI LỖI ở các gate; không dùng các phép đo hình thức này thay việc đọc nghĩa lời khai.

#### Bổ sung xác minh hiện vật/gate
`sha256sum -c SHA256SUMS` tại `cay-kho/ops/reviews/pr896-review-2-codex/`: rc=0, 106 dòng OK; output cuối `./run/stdout.log: OK`. JSON thật từ `evidence/gate-4.log`: `"ok": true, "strict": false`.

### HƯỚNG 9: Hồ sơ append-only, bảo lưu assurance và trạng thái HINT sau bản vá
- giả thuyết: khối lượt 2 sửa dòng cũ, tự chọn đơn vị land, hoặc vẫn dùng trạng thái trước khi áp HINT.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/history_audit.py > evidence/history-audit.log`.
- output thật: `land_prefix_preserved_at_record=True`; `land_unchanged_after_765ae89=True`; `master_prefix_preserved=True`; `luot2_landed=False`; `reviewer_assurance_81=CHUA DAT`. Đề xuất ghi rõ `CAN chu kho chap nhan, ho so nay KHONG tu chon`. Hai tổ tiên 3bc4244/a9bc934 của 8d56009 đều rc=0; CLAUDE.md từ 3bc4244 tới target: diff 0 byte. Bốn đối chiếu diff/numstat giao với Git đều `equals_supplied=True`. Trước vá 578fb4b: `caveat_count=0`; tại 82359c4: `caveat_count=1`.
- kết luận: LỖI ở trạng thái hiện hành: receipt lượt 2:111–114 còn `HINT-P1-CHUA-AP`/`HINT.patch ... CHUA ap`; README:731/1028 lặp lại; land:234 còn `CHUA ap`, 241–242 còn điều kiện caveat đang thiếu. Các câu này đúng lúc ghi sổ tại 765ae89 và còn đúng tại 578fb4b; trở thành cũ/sai khi 82359c4 áp patch. Header verdict lịch sử `changes_requested` và số finding trên 8d56009 vẫn đúng, không được sửa byte verdict để đổi lịch sử. Khối `do_duoc` và `ket_luan_finding_cu` cần ghi rõ mốc lịch sử khi bổ sung readback mới; trạng thái `CHUA DAT`, `landed: false`, và quyền chọn đơn vị land vẫn phải giữ.

### HƯỚNG 10: Mở rộng sang cách viết “Codex service/API”, không chỉ token codex_service
- giả thuyết: grep đúng token máy đã bao phủ mọi lời tự khai service.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/surface_audit.py > evidence/surface-audit.log`; `PYTHONDONTWRITEBYTECODE=1 python3 evidence/service_spelling_audit.py > evidence/service-spelling-audit.log`.
- output thật: `TOTAL_EXPLICIT_SERVICE_WITH_CLI_RECEIPT 13`; 12 tệp `surface_caveats=0`; riêng pr455 lượt 6 có 2 caveat chứa từ surface nhưng nói về parser/provider và độ phủ test, không đối chiếu service tự khai với CLI trong receipt. Danh sách gồm phan-bien-quy-trinh lượt 3/4/5 (verdict:15/13/12), pr455 lượt 1–8 (verdict:7/9/9/9/9/9/9/8), pr460 lượt 9 (verdict:5), pr493 lượt 5 (verdict:8). Receipt đều `surface: codex_cli`; ghi chú nói launcher/codex exec nhưng không có run_json trong identity trỏ hiện vật runtime để hậu kiểm tại checkout.
- kết luận: LỖI P2 về thiếu điều kiện/đính chính cho 13 mâu thuẫn tài liệu này. Đo được hai lời khai bất nhất và thiếu caveat; KHÔNG ĐO ĐƯỢC bên nào phản ánh surface thực tế chỉ từ receipt thuật lại. Không nâng chúng thành 13 P1 về runtime và không gộp các câu chung “API có shell” thành lời phủ nhận CLI. Riêng wp766 có run JSON nên là P1 chắc chắn (hướng 3). Các ca ci-g5 2/4/5/6/7/8 đã ghi `surface_tu_khai_trong_verdict` + caveat thiếu runtime nên không tính lỗi mới. `codex_desktop` ở wp523 r14 khớp receipt; `claude_code_subagent` so với `claude_code` có caveat subagent cùng họ; không quy thành sai surface.

## FINDINGS

### verdict-surface-bo-sot-wp766 [P1] Còn một lời tự khai service bị run JSON bác bỏ, chưa đính chính
TỆP/DÒNG: `ops/reviews/wp766-r1-g1-exec-review-1-codex-verdict.md:12`; `ops/reviews/wp766-r1-g1-exec-review-1-codex/run.json:78`; `ops/reviews/wp766-r1-g1-exec-review-1-codex-verdict.receipt.yaml:66,99`; bảng cảnh báo trong `ops/reviews/README.md`.

VẤN ĐỀ: Verdict tự khai `execution surface codex_service`. Run `5d4f7321d9a04ee1a87934e41fcf45c8` ghi chương trình `codex`, `execution_surface=codex_cli`; biên nhận cũng ghi CLI, nhưng chỉ có hai caveat về quyền ghi checkout và driver đọc cây tạm, không caveat đối chiếu surface. P1 lượt 2 đích danh pr889-review-1 đã đóng; cùng lớp lỗi vẫn còn tại wp766, được tìm khi mở glob ra toàn bộ 267 verdict. Đây là sự thật đo được tại 82359c4, không phải suy model từ tài khoản vận chuyển.

ĐÃ THỬ NGHIỆM: `rg -n codex_service cay-kho/ops/reviews/*-verdict.md`; `PYTHONDONTWRITEBYTECODE=1 python3 evidence/surface_audit.py`; output `RUN .../wp766-r1-g1-exec-review-1-codex/run.json id 5d4f7321d9a04ee1a87934e41fcf45c8 surface codex_cli program codex`, receipt CLI, caveat thiếu. Ba ca nền vẫn `1/1`, nên không phủ nhận finding.

GỢI Ý VÁ: thêm caveat `VERDICT-KHAI-SAI-EXECUTION-SURFACE` cho wp766 và hàng cảnh báo README, dẫn đúng dòng 12/78/run ID; giữ byte verdict, không suy model/effort hay nâng assurance. Có trong HINT.patch.

ĐỘ TIN: cao.

### ho-so-luot2-van-khai-hint-chua-ap [P1] Trạng thái đang có hiệu lực vẫn phủ nhận bản vá đã áp
TỆP/DÒNG: `ops/reviews/pr896-review-2-codex-verdict.receipt.yaml:111–114`; `ops/reviews/README.md:731,1028`; `ops/land/pr896-claude-md-bai-hoc-c-tro-nguon-land-evidence.yaml:232–234,241–242`.

VẤN ĐỀ: Caveat `HINT-P1-CHUA-AP` và hai hàng README vẫn nói receipt pr889-review-1 thiếu caveat và `HINT.patch ... CHUA ap`. Khối land vẫn khai hint chưa áp và đề xuất thêm caveat còn thiếu nếu được áp. Những câu này đúng lúc ghi sổ ở 765ae89 và tại cha 578fb4b; tại 82359c4 chúng đã cũ/sai: chính commit này thêm caveat và hàng README. Các trường lịch sử kết quả trên reviewed_sha 8d56009 vẫn đúng; lỗi nằm ở thiếu mốc lịch sử/cập nhật trạng thái hiện hành, không nằm ở verdict nguyên văn.

ĐÃ THỬ NGHIỆM: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/history_audit.py`; `578fb4b caveat_count=0` đối chứng `82359c4... caveat_count=1`; diff thực khớp tệp được giao và chỉ thêm đúng 5 dòng. Cổng vẫn xanh khi hồ sơ có mâu thuẫn này.

GỢI Ý VÁ: đổi caveat và README thành “tại 8d56009/765ae89 chưa áp; đã áp tại 82359c4; cần verdict mới cho SHA ứng viên”; bổ sung readback mới cuối land, chỉ rõ khối lượt 2 là ảnh lịch sử. Giữ `changes_requested`/0/1/0/0 của verdict cũ, `cross_reviewed`, `CHUA DAT`, `landed: false`, và yêu cầu chủ kho chấp nhận đơn vị land. Có trong HINT.patch.

ĐỘ TIN: cao.

### surface-service-cli-thieu-dieu-kien-nguon [P2] Mười ba verdict viết service/API còn lệch receipt CLI mà chưa giải thích
TỆP/DÒNG: `phan-bien-quy-trinh-review-{3,4,5}-codex-verdict.md:15/13/12`; `pr455-bien-nhan-v2-review-{1..8}-*-verdict.md:7/9/9/9/9/9/9/8`; `pr460-bien-nhan-v2-review-9-gpt6astra-verdict.md:5`; `pr493-review-5-codex-verdict.md:8` (đều trong `ops/reviews/`); receipt tương ứng và README. Danh sách exact path/dòng receipt ở `evidence/service-spelling-audit.log`.

VẤN ĐỀ: Đây là lời TỰ KHAI “Codex service/API” của reviewer, không phải nhắc token khi mô tả finding. Receipt ghi `surface: codex_cli`, nguồn thuật lại launcher/codex exec; chưa có caveat giải thích cặp lời khai. Không có `run_json` trong identity trỏ hiện vật runtime có thể đọc tại SHA này, nên không được lặng lẽ chọn một bên làm sự thật đã đo hoặc tự sửa thành CLI như ca wp766. Đây là thiếu điều kiện nguồn/caveat, đếm một P2 cùng lớp cho 13 thể hiện, không kết tội 13 runtime đã xác minh.

ĐÃ THỬ NGHIỆM: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/service_spelling_audit.py`; output `TOTAL_EXPLICIT_SERVICE_WITH_CLI_RECEIPT 13`. Đọc từng caveat: 12 receipt không có từ surface; pr455 lượt 6 có hai caveat chứa từ surface nhưng nói về sản phẩm và độ phủ test, không sửa surface của reviewer. `evidence/surface-audit.log` ghi `RUNTIME_FOUND False` cho các identity này. **KHÔNG ĐO ĐƯỢC actual execution surface** từ các hiện vật nguồn vắng mặt; chỉ xác nhận bất nhất văn bản.

GỢI Ý VÁ: ghi caveat riêng và hàng README nêu đúng hai lời khai, dẫn dòng verdict, nêu thiếu runtime để phân xử; chưa sửa byte verdict hoặc nâng assurance. Muốn xác định surface thực tế phải bổ sung runtime evidence của đúng run. HINT.patch minh hoạ cách ghi thiếu bằng chứng, không tự nhận CLI đã được đo ở 13 ca này.

ĐỘ TIN: cao về bất nhất văn bản/thiếu caveat; không kết luận surface thực tế.

### HƯỚNG 11: Tái áp nguyên HINT lượt 2 và so blob
- giả thuyết: bản vá 82359c4 không phải nguyên HINT như commit khai.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/validate_hint.py` trên clone (hai tệp tài liệu lấy từ cha 578fb4b), `patch --batch -p0 --fuzz=0 -i <HINT-lượt-2>`; so byte với 82359c4.
- output thật: `old_hint_rc=0`; `target_blob_match ops/reviews/README.md True`; `target_blob_match ops/reviews/pr889-review-1-codex-verdict.receipt.yaml True`.
- kết luận: KHÔNG PHẢI LỖI; nguyên HINT tạo đúng hai blob của target, không có sửa thêm trong commit 82359c4.

### HƯỚNG 12: Kiểm HINT mới trên bản sao
- giả thuyết: gợi ý vá phá YAML/mục lục/băm verdict hoặc tự đổi lịch sử/assurance.
- lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/validate_hint.py`; dry-run và áp `patch --batch -p0 --fuzz=0 -i HINT.patch`, rồi chạy từng lệnh dưới trên clone.
- output thật:
```text
hint_dry_run_rc=0
hint_apply_rc=0
{"cmd": "python3 ops/lease_publish_test.py --chi-ca=t26_", "rc": 0, "summary": ["lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0"]}
{"cmd": "python3 ops/lease_publish_test.py --chi-ca=t27_", "rc": 0, "summary": ["lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0"]}
{"cmd": "python3 ops/lease_publish_test.py --chi-ca=t138_", "rc": 0, "summary": ["lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0"]}
{"cmd": "python3 ops/bien_nhan_v2.py --root .", "rc": 0, "summary": ["bien_nhan_v2: 236 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 289", "TỔNG: ĐẠT"]}
{"cmd": "python3 ops/land_evidence_nguon.py --root .", "rc": 0, "summary": ["land_evidence_nguon: 47 ĐẠT · 26/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 73", "TỔNG: ĐẠT"]}
hint_changed_files=17; chi .md/.yaml; khong sua *-verdict.md
```
- kết luận: KHÔNG PHẢI LỖI. Đây là kiểm gợi ý trên clone, chưa áp lên cây giao review, chưa chứng nhận approval/land.

### HƯỚNG 13: Snapshot cuối của cây được review
- giả thuyết: phép đo đã làm đổi nội dung trong cay-kho/.
- lệnh: Python tính SHA256 toàn bộ tệp thường ngoài `.git` và so `evidence/start-snapshot.json`; `git -C cay-kho rev-parse HEAD HEAD^{tree}`; `git -C cay-kho status --porcelain=v1 --untracked-files=all --ignored=matching`.
- output thật: `files_before=6266 files_after=6266`; `added=[] deleted=[] modified=[]`; `status=''`; HEAD `82359c4deec90edebbaebf9ab9d094902120b567`; tree `32cf81c2614a91c7ced8fc77781b01dcb12fc8a7`. Log đầy đủ `evidence/final-state.log`.
- kết luận: KHÔNG PHẢI LỖI. Không có delta nội dung quan sát được giữa hai snapshot, kể cả tệp ignored. Mọi patch/đột biến thực hiện ở clone ngoài cay-kho/. Snapshot không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên.
