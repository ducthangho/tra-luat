```text
verdict: changes_requested
reviewed_sha: 0b1ca263c83bc42b8da517b1c92cde3fdb39b530
dem: P0=0 P1=0 P2=4 P3=0
```

Tree: `64789ea8c4e5fe2bfba07610d6ed395dd76f9aff`. Provider: `openai_codex`; surface: `codex_cli`; transport: `machine`. Checkout giữ nguyên HEAD, tracked files và index.

**Lớp `mau-ca-khong-phu-hop-hanh-vi`**

**S822-01 — P2 — `ops/specs/wp822.md:110`.** M3 áp mẫu “fixture vi phạm một thành phần, rc và lý do từ chối riêng” cho cả K25/K26/K36, dù chúng kiểm khử trùng, cảnh báo và đầu ra thành công.

Đo bằng `python -B /tmp/wp822-review-7a261a8a/probe_contract.py`, rc=0: bỏ `dict.fromkeys`, truyền hai tên bắt buộc `gate`; nền và mutant đều rc=0, stderr rỗng, nhưng stdout đổi từ một thành hai `gate id=1`. Ca đúng phải kiểm đầu ra/count. Cũng tại M3, khẳng định thiếu khóa luôn dẫn tới `KeyError` sai với `status`/`conclusion` trên run không bắt buộc: probe D5/D6 cho rc 12 → 0, không traceback.

HINT: sửa M3 để tách ca từ chối, ca đầu ra thành công và ca hiện diện trường. Khóa bằng mutant bỏ khử trùng và đổi đầu ra suite. Giữ yêu cầu lý do chính xác cho ca từ chối; tránh nới thành chỉ kiểm rc.

**Lớp `tuong-duong-suy-tu-suite-im-lang`**

**S822-02 — P2 — `ops/specs/wp822.md:108`, `:124`.** M1/A5 dùng việc đột biến không đổi màu ca hiện có làm bằng chứng `tuong_duong`. Đây cũng chính là biểu hiện của thiếu ca test.

Đã chạy mã trong [probe_presence.py](/tmp/wp822-review-7a261a8a/probe_presence.py) qua `python -B -`: mutant gỡ riêng kiểm hiện diện `conclusion`, giữ nguyên các mỏ neo, vẫn đạt **405/405**, bỏ qua một ca Windows, không ca đỏ. Nhưng fixture gồm gate hợp lệ và run `other` thiếu `conclusion`, total_count đúng, đổi từ rc=12 sang **rc=0, `gate XANH`**.

HINT: sửa M1/A5 để miễn trừ cần lập luận về hành vi/phủ chồng, thay vì suite im lặng. Thêm kiểm kê và ca phân biệt thiếu `conclusion` với `null`. Mutant bỏ kiểm hiện diện phải chết bởi ca hành vi; giữ total_count, suite và head đúng để tránh chốt khác chặn hộ.

**Lớp `gan-nang-luc-cho-runner`**

**S822-03 — P2 — `ops/specs/wp822.md:120`, `:132`.** Bộ chạy hiện tại không phân biệt được assertion đo đúng hành vi với assertion bọc traceback của CLI.

Đo bằng `python -B /tmp/wp822-review-7a261a8a/probe_classifier.py`, rc=0: đổi `except ValueError:   # F02:` thành `except TypeError:   # F02:`. Ca có sẵn `kg_f02_suite_vuot_tran_int` nhận CLI rc=1 với traceback `ValueError`, rồi `_doi` bọc thành `AssertionError`. Ba đối chứng xanh và phép phân loại của main vẫn cho **`runner_accepts=true`**.

HINT: yêu cầu receipt kết quả CLI hoặc classifier có tự kiểm cho từng mutant kiểm kê. Khóa bằng cặp: crash `ValueError` phải bị loại tín dụng, còn mutant `suite=1` tạo xanh giả phải được tính giết. Chỉ nhận diện tên `AssertionError` sẽ tiếp tục cấp tín dụng giả.

**S822-04 — P2 — `ops/specs/wp822.md:165–166`.** Lời hứa A1 sẽ đo D1–D6 trên toàn suite không khớp runner hiện tại: main chỉ chạy `phai_chet ∪ doi_chung`.

Đo bằng `python -B /tmp/wp822-review-7a261a8a/probe_scope.py`, rc=0: với một ca đích kg, thực chạy **4/406 ca**, gồm ca đích và ba đối chứng doctrine. Hai ca ngoài họ kg, `stdout_cp1252` và `stdout_cp1258`, thực tế có gọi `kiem-gate` qua `_kich_ban_in`.

HINT: sửa lời khai thành phạm vi target+controls, hoặc bổ sung phép đo thực sự chạy các ca ngoài họ dưới mỗi D. Receipt phải ghi tên ca đã chạy. Khi mở rộng, phân biệt lỗi mỏ neo bị stale với hồi quy hành vi.

**Bảng kiểm lời khai số**

Đo ngày 18-10-2026 UTC trên exact SHA nêu trên.

| Phép đo | Kết quả |
|---|---|
| Diff hiện tại | Đúng 1 tệp mới `ops/specs/wp822.md`, +171/-0 |
| Nền `_KG_CA` / toàn họ kg | 100/100 và 104/104 |
| D1/K18 | Neo 1 chỗ; đỏ 0/100, đồng thời 0/104 |
| D2/K35 | Neo 1 chỗ; đỏ 0/100, đồng thời 0/104 |
| D3/K10 | Neo 1 chỗ; đỏ 0/100, đồng thời 0/104 |
| D4/K11 | Neo 1 chỗ; đỏ 0/100, đồng thời 0/104 |
| D5/K12 | Neo 1 chỗ; đỏ 0/100, đồng thời 0/104 |
| D6/K13 | Neo 1 chỗ; đỏ 0/100, đồng thời 0/104 |
| A3, nền | rc=12, `thiếu/sai kiểu trường ['conclusion']` |
| A3, D6 | rc=12, `total_count khai 1 mà có 2 id — THỪA id` |
| A2, sáu fixture reviewer dựng | Cả sáu: nền rc=12 đúng lý do → mutant rc=0 |
| Toàn suite nền | rc=0, `405/405`, `TỔNG: ĐẠT`; 1 ca Windows skipped |
| Tự kiểm mutant nền | 168 khai báo; 167 báo giết đúng ca đích và đối chứng xanh; 1 mutant Windows skipped |
| `doctrine-scan` / `adr-song` | rc=0; 10 tệp/0 chỗ chép; 53 ADR/53 dòng |
| Ruff contract | rc=0, `RUFF_CONTRACT 3 []` |
| Bare Ruff | Base/head cùng rc=1 với 2 F541; delta=0 |

Chưa xác minh GitHub, lease và số kế thừa H1–H3. Mirror shallow/offline chưa đủ chứng nhận điều kiện áp trần 8/450. `wp788.md` không có, đã bỏ qua theo assignment.

[Báo cáo đầy đủ](/tmp/wp822-review-7a261a8a/VERDICT.md) · [Manifest bằng chứng](/tmp/wp822-review-7a261a8a/evidence_manifest.json)