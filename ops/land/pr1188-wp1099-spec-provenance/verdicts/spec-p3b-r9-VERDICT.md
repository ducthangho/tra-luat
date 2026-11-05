verdict: approve
reviewed_sha: 2f660b58312d59b6a612f063161feb7d715b2f2b
reviewed_tree: 431c8c2724bd1b516e7cda64269b5ae638807347

## DANH TÍNH

Reviewer: OpenAI / Codex (model chi tiết không được công cụ xác nhận), execution surface: Codex agent với shell cục bộ, transport: tool trực tiếp. Executor theo chỉ thị: Claude; không sử dụng context executor. Đo offline ngày 05-11-2026 UTC.

```text
$ git -C cay-kho rev-parse HEAD HEAD^{tree}
2f660b58312d59b6a612f063161feb7d715b2f2b
431c8c2724bd1b516e7cda64269b5ae638807347
rc=0
```

```text
$ git -C cay-kho status --porcelain=v1 --ignored
(rỗng)
rc=0
```

```text
$ sha256sum cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r1.md cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r2.md cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r3.md cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r4.md cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r5.md cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r6.md cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r7.md cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r8.md cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r9.md
15fe242a65c8df1ff393cdc15784642013e904bacb9b754b0d72a64237dac11e  cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r1.md
c6e53a00c7370ce0d75d9bcd954f8b7e69aa7383a0f5e6427a29e5e0d0e3ed8d  cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r2.md
e2246e90aaf35b6b006b40a258e694a99c796a1ff1a8ac21aebb408121efa121  cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r3.md
d28d00b5dbf6aac631f2aaac4282eb50ad1e59490d03acff095a64e45535430f  cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r4.md
25473237f53684706112b5a2f8dfafce143000110a57c8d680f3b44f924e5ed5  cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r5.md
b078da106387512cac956d8bc18d702bb50cfcf4bfd37101bb6c7aeb0686d201  cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r6.md
887dc78a1f20d640f1b779b58fea7c963b2931e76e31abbe00ca13960d699061  cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r7.md
079868c4f757ea2248ed92045c918eb3e51d0d3976656d4b0d788d3226badc71  cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r8.md
377c166ed1fa5c9a209483850080a4082d8eb37733fa3e298d7bfe92dbe3cd12  cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r9.md
rc=0
```

HEAD/tree khớp chỉ thị; status gồm ignored rỗng. Đã đo băm cả 9 revision; prompt không cung cấp băm kỳ vọng độc lập. r9 hiệu lực, r1–r8 chỉ là lịch sử.


Đo cuối lượt 2026-11-05T01:32:23.052471+00:00:

```text
$ git -C cay-kho rev-parse HEAD HEAD^{tree}
2f660b58312d59b6a612f063161feb7d715b2f2b
431c8c2724bd1b516e7cda64269b5ae638807347
rc=0
```

```text
$ git -C cay-kho status --porcelain=v1 --ignored
(rỗng)
rc=0
```

```text
$ git -C cay-kho diff --exit-code
(rỗng)
rc=0
```

```text
$ git -C cay-kho diff --cached --exit-code
(rỗng)
rc=0
```

HEAD/tree không đổi; tracked, untracked và ignored sạch ở hai mốc. Diff worktree/index đều rỗng. Snapshot chỉ chứng minh trạng thái quan sát tại các mốc; mọi thao tác ghi của harness nằm trong SANDBOX ngoài checkout.

## ĐO LẠI KHẲNG ĐỊNH

Lệnh tái hiện chung: `PYTHONDONTWRITEBYTECODE=1 python review_measure.py > measurements.log 2>&1` (rc 0). Script và fixture nằm ngoài `cay-kho/`; kết quả chi tiết ở `measurements/results.json`. Hàm nguồn được import với bytecode tắt; kết nối mạng bị chặn trong harness; subprocess chỉ chạy driver local trên đồ giả.

| khẳng định | lệnh đo | kết quả | khớp/lệch |
|---|---|---|---|
| r9 E24: F3(a) so byte; F3(b) không chứng minh độ tươi | `review_measure.py`, mục F3 | Sửa thân giữ ID: (a) `GENERATED_BUNDLE_STALE`, (b) rc 0/ok true; tái sinh: cả hai xanh; đổi ID và tên tệp: (b) rc 1, `TEST_ID_SET_MISMATCH` | khớp |
| F3(a) nền đang tươi | gọi `_test_fragments_check(cay-kho)` | ok true/current; expected = actual = `27e1d5dff02187e9dc39078695d8fb3a13ad0dfb2078a5e1cf460a54442afdf1`; 73.663 byte | khớp |
| r9 E25: G2 đối chứng âm ngoài cây | `cmd_doctrine_scan` nguồn, thêm đường dẫn fixture | nền rc 0, 10 tệp/0 chỗ; thêm cụm: rc 6/`nguong-so-stop-conditions`; bỏ cụm: rc 0 | khớp |
| D1, từng tài liệu, phép đếm và bảo toàn chữ cũ | `review_measure.py`, mục D1 | 3 đối chứng xanh và 3 ca đỏ cho mỗi tệp; ngắt dòng lại vẫn xanh | khớp |
| D2/D3 trên cùng fixture | `cmd_adr_song` + `_ADR_TRANG_THAI` nguồn | Accepted: D2 rc 0/D3 xanh; trạng thái trần: D2 rc 9/D3 đỏ; Proposed/thừa dòng: D3 đỏ; xoá dòng §20: D2 rc 9 | khớp |
| H1 chỉ đo tiền tố | `review_measure.py`, mục H1 | đoạn đúng xanh; rỗng/bỏ tiền tố đỏ | khớp |
| A13, canary nguồn, sáu ca | `_nlm_auth_alive` thật + `nlm_cli` giả, bỏ chờ | `None,None,False,False,False,None`; quy đổi `2,2,3,3,3,2` | khớp |
| F2, ca r213 nguyên trạng | trích AST `_c213_auth_carve_out_khong_pha_thu_tu`, gọi trên fixture | base xanh; thêm câu ngoại lệ xanh; xoá CẤM ở QUY_TRINH đỏ | khớp |

Phép đo bổ sung: `PYTHONDONTWRITEBYTECODE=1 python review_supplement.py > supplement.log 2>&1` (rc 0); dữ liệu ở `measurements/supplement.json` và `measurements/static.json`.

| khẳng định | lệnh đo | kết quả | khớp/lệch |
|---|---|---|---|
| A13: cùng thân `_canary_song` trả mã đúng trong tiến trình con | trích Python nguyên văn từ `scripts/nlm-auto-refresh.sh`; chạy `python -c` với `tl` giả và hai mô-đun nguồn chép ngoài cây | sáu rc thật: `2,2,3,3,3,2`; stdout/stderr rỗng | khớp |
| `nlm-auth-status` không phân biệt mạng/quyền/auth chết | `_nlm_preflight_report` nguồn, thay hàm đọc credential bằng đồ giả RAM | refused/403/auth đều `alive=False` | khớp |
| J1 bắt byte đổi sau tái sinh | `_verify_release_manifest` nguồn trên bản sao đúng 184 tệp của manifest; đổi một byte trong `nlm_cli.py` | đối chứng: ok true, expected_file_count=checked_file_count=184; đột biến: ok false, failed đúng `scripts/nlm_cli.py`, package_hash_match=false | khớp |
| Chốt chống hạ cấp còn ở đường nạp | `_nlm_auth_load_downgrade` nguồn với object timestamp giả trong RAM | bundle cũ hơn bị chặn; mới hơn không chặn; thiếu mốc không chặn — đúng hành vi hiện có, không tự khai fail-close mạnh hơn | khớp |
| 9 mục tiêu ứng với 9 đường dẫn, mọi mục tiêu có nghiệm thu | trích mục `write_set`, `muc_tieu`, bảng `nghiem_thu` trong `review_supplement.py` | hai danh sách 9 đường dẫn bằng nhau, đúng thứ tự; 28 hàng tiêu chí; không mục tiêu thiếu nghiệm thu; không ô đột biến rỗng/`—` | khớp |
| `errata_r2`…`errata_r8` được giữ nguyên và r9 chỉ sửa F3/G2 ngoài header + errata mới | `difflib.unified_diff` mỗi cặp r1→r9; so nguyên từng mục errata | các mục lịch sử giữ nguyên; diff r8→r9 đúng phạm vi E24/E25; r8 E23 công khai thay V bằng phép đo tối thiểu + R1 | khớp |
| `diff.patch` đúng diff được giao | `git -C cay-kho diff --no-ext-diff --no-color --abbrev=8 1f0941e9 HEAD`; so byte | cùng SHA-256 `cc1bbcb828b583df4354db6f6dc3a3b6f7487fd31128d0d8ead5893e68a39ef6`; 6 đặc tả r4–r9, 1.913 dòng thêm | khớp |
| Base/merge được nêu trong r9 | `git show -s --format='%H%n%s' 90c101b8 c7174bfe 1f0941e9 47ee1b20 8ab100793df9831505f495543a74044b91c2c9ab` | lần lượt merge #1092, #1130, #1186, #1101, #791; base đầy đủ `1f0941e9bba1d1d517eda4174167b81963c06bd5` | khớp |
| Manifest hiện hành có 184 tệp, chứa bốn đường dẫn đóng gói | đọc JSON `RELEASE_MANIFEST.json`, so tập `files[].path` | file_count=len(files)=184; có nlm_cli, bundle fragment và cả hai tài liệu doctrine | khớp |
| Số tệp manifest theo các base lịch sử | `git show <base>:RELEASE_MANIFEST.json`, `json.loads` | 90c101b8:197; c7174bfe:198; 1f0941e9:184 | khớp |
| Hai fragment tham chiếu dài 260/259 dòng | `Path.read_text().splitlines()` trên wp726/wp727 | wp726_script_nlm_canary.py:260; wp727_tl_gws_refresh.py:259 | khớp |
| `nlm_cli.py:143,162,229`: cùng bộ nhận diện auth; `_run:110` trả tuple | `nl -ba` + đọc AST/thân hàm `scripts/nlm_cli.py` | đúng `auth,401,login,unauthor,credential`; `_run` gom keyring, rc 124 khi timeout, 127 khi thiếu binary; các adapter NLM ở tệp đều đi qua `_run` | khớp |
| `tl_gws.py:308–363`: tối đa 3 probe, 30 giây/probe, chờ 1,5+3 giây | `nl -ba` + sáu ca A13 chạy nguồn | đúng neo; chờ tổng 4,5 giây; lần cuối quyết định; 120 giây là hạn con đề xuất có dư so 94,5 giây probe/chờ | khớp |
| `_AUTH_FIX_FALLBACK` ở `nlm_ops.py:297`; probe lỗi ở `:1424–1430` | `nl -ba scripts/tl_core/nlm_ops.py` | đúng dòng khai báo và nhánh bool/except gán False | khớp |
| Ca r213 ở `tl_selftest.py:24829` | `nl -ba`; `git show <base>:scripts/tl_selftest.py` tìm def | head/1f0941e9:24829; c7174bfe:24827; neo cũ 24836 trong r1 đã được E4/E10 thay, không dùng để thi hành r9 | khớp bản hiệu lực |
| Điều cấm hiện hành ở RASOAT:118–119 và QUY_TRINH:49 | `nl -ba` hai tài liệu | RASOAT ngắt giữa `CẤM tự`/`nlm-auth-load`; QUY_TRINH dùng `**CẤM**`; D1 đo đúng cả hai | khớp |
| Regex/cổng ADR đúng nguồn; khuôn trạng thái đúng ADR có sẵn | `nl -ba .claude/dev/packet_loop.py`; đọc dòng 3 của ADR-0060/0062 | `_ADR_TRANG_THAI:1887`, thực tế re.M\|re.I; hai ADR dùng `- **Trạng thái:** Accepted (…)`; D3 dùng regex nguồn và so toàn dòng chuẩn | khớp |
| Bộ sinh bundle/cổng tươi đúng hàm được nêu | đọc `tl_core/test_fragments.py:464`, `tl_core/release.py:206–269`, `bundle_fragment_check.py` | bộ sinh nhận thư mục fragment; freshness so toàn byte; cmd trả rc 0/2 theo ok; topology kiểm ID/hành vi riêng | khớp |
| Khuôn changelog từ wp1038 | đọc dòng đầu `changelog.d/wp-1038.md` | đúng `WP1038 (CLOUD-SETUP-P2A-EXEC): `; có thể áp tiền tố WP1099 như H1 | khớp |
| Tính năng chưa được thi hành trên base/head đặc tả | glob ba đường dẫn mới; đếm `NAP_LAI\|nap_lai`; đếm ADR-0063 trong bảng §20 | fragment WP1099/ADR-0063/changelog WP1099 vắng; nhãn nap_lai:0; dòng bảng:0; đây là nền “chưa làm” | khớp |
| Năm tệp mã/doctrine được nêu không đổi từ các base | `git -C cay-kho diff --numstat <base> HEAD -- scripts/nlm_cli.py references/RASOAT_HOSO_LOOP.md references/QUY_TRINH_RA_SOAT_3_TANG.md scripts/tl_gws.py scripts/tl_core/nlm_ops.py` với 90c101b8/c7174bfe/1f0941e9 | cả ba rc 0, output rỗng; từng neo hiện hành còn được đo trực tiếp ở trên | khớp |
| Bốn hằng auth giữ nguyên | trích AST từng phép gán trên `git show 1f0941e9:scripts/nlm_cli.py` và head | AUTH_FIX_HINT, AUTH_FIX_HINT_SHORT, _AUTH_FIX_ORDER, _AUTH_FIX_RASOAT_CARVE đều bằng nhau | khớp |

Đối với đột biến F3 chỉ đổi TEST_ID mà chưa đổi tên tệp, gate báo `DEV_FRAGMENT_DISCOVERY_FAILED` do `PATH_ID_MISMATCH`, đồng thời có `TEST_ID_SET_MISMATCH` trong `problems`; đổi ID kèm tên tệp hợp lệ thì lỗi chính là `TEST_ID_SET_MISMATCH`. Cả hai đều ĐỎ. Bằng chứng F3(b) ở đây dùng hàm main/driver/loader thật, bộ đóng ZIP local giả và `tl` rỗng vô hại; không phải kết quả CI của PR.

Đối chiếu L1–L6 và Spec: 9 mục tiêu không vượt write_set; tiêu chí A phân biệt số ca/số lời gọi/tiến trình; A11 và mục Báo thống nhất đếm theo lời gọi; các ngưỡng có đơn vị; số đo dữ kiện đi kèm base/thời điểm, số ước tính được ghi rõ chưa đo. D1 bảo toàn chữ cũ và đếm riêng từng tệp; D3 chỉ đo dòng trạng thái; H1 chỉ đo tiền tố; nội dung/vị trí/render được giao rõ cho R1. Các đối chứng không được diễn giải thành máy chứng minh phần của người đọc. Đã đọc các cột đột biến của cả 28 tiêu chí; các ca hành vi mới là nghĩa vụ khi thi hành, M1 khai rõ điều kiện/ai đo và trạng thái chưa đo.

Đối chiếu Standards/Security: cơ chế đề xuất dùng đúng lệnh nạp có sẵn, không `--force`, không kéo `tl_secrets.enc`, giới hạn cloud + cờ tắt truyền cho con, chỉ mã canary 3 cho phép nạp và chỉ danh sách lệnh đọc cho phép retry. Jar là credential cục bộ; đặc tả không thêm writer registry/credential từ xa hay bỏ GAS/LockService của đường ghi registry. Dấu dùng quyền 0600/nguyên tử; đầu ra con được giữ kín, A11 có sentinel. Quyết định giữ canary “lần cuối”, ngoại lệ race đã chấp nhận và hạ phép đo Markdown ở r8 được giữ nguyên theo chỉ thị.

Giới hạn: review đặc tả r9, không phải nghiệm thu implementation chưa tồn tại. Full selftest/G1, Ruff trên fragment mới/K1, delta code/K2, CI/L1, R1 của PR code và LIVE/M1 chưa chạy trong lượt này. Không gọi mạng, Drive, NLM, webapp, GitHub hay `tl` thật; không đọc/ghi credential thật. Lịch laptop WP710 và độ tươi credential LIVE là dữ kiện vận hành ngoài checkout, không xác nhận trực tiếp; M1 vẫn `chưa đo được`. Không xác nhận lại ref/lease từ remote hoặc quyền duyệt qua dịch vụ. Các mục lịch sử có đính chính được đánh giá theo chuỗi errata, không biến sai sót đã sửa thành finding mới.

## FINDINGS

Không có finding P0/P1/P2/P3 trong đặc tả r9 sau đối chiếu nguồn, fixture và chuỗi errata. E24 (F3) và E25 (G2) đóng đúng hai finding r8 được giao. Các giới hạn phép đo nêu trên không được coi là nghiệm thu code hay LIVE.

## TỔNG

P0: **0** · P1: **0** · P2: **0** · P3: **0**.

Kết luận: **approve** đặc tả revision 9 tại exact SHA/tree ghi trên. Hai sửa đổi E24/E25 đã có phản chứng dương/âm bằng hàm nguồn; không còn finding. Nghiệm thu code, CI và M1 được thực hiện theo các điều kiện r9 khi có implementation. Phép đo trong lượt này không thay các bước ấy.
