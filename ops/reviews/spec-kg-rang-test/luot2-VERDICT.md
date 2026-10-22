```text
verdict: changes_requested
reviewed_sha: 5e34b5d439cc4759f038091899f4b74d5ea2e4c5
dem: P0=0 P1=0 P2=1 P3=0
```

Tree: `9b6cf8b4b1b426cccf8725e83e9adb88badb4280`. Reviewer: `openai_codex / codex_cli / machine`; header công bố `gpt-6.1-sol`, effort `xhigh`.

**Lớp `tuong-duong-suy-tu-suite-im-lang`**

**S822-02 — P2 — [ops/specs/wp822.md:109](/tmp/claude-0/-home-user-tra-luat/353bc79e-3dd4-5d53-a13a-54256c3f5d49/scratchpad/rv822-2/src/ops/specs/wp822.md:109), đối chiếu dòng 126.** M1 cho phép miễn trừ `tuong_duong` bằng chứng minh chốt khác chặn mọi đầu vào vi phạm. A5 lại bác miễn trừ khi stderr thay đổi. Hai điều kiện này không tương đương.

Đã chạy:

```text
python3 -B /tmp/wp822-review-r2-8ad04492/probe_equivalence.py
rc=0
```

Trên bản sao, thay đúng một neo `if tc is _VANG:` bằng `if False:`. K07 vẫn chặn **mọi** trường hợp thiếu `total_count`, vì `_VANG` không phải `int`; như vậy đáp ứng nhánh phủ chồng của M1. Nhưng cùng fixture cho:

```text
Nền:      rc=12; lý do: thiếu `total_count`
Bỏ K06:   rc=12; lý do: `total_count` không phải số nguyên ≥ 0
kg_n5_thieu: nền xanh → mutant AssertionError: rc đúng nhưng LÝ DO sai
```

CLI không crash. Executor có thể dùng miễn trừ mà M1 cho phép rồi bị A5 bác.

**HINT:** sửa M1/A5 trong đặc tả để chứng minh phủ chồng cũng phải bảo toàn rc/stdout/stderr, gồm lý do từ chối. Giữ `kg_n5_thieu` cùng mutant trên làm phản chứng. Tránh nới A5 thành chỉ so rc, vì sẽ bỏ mất bảo vệ lý do đã khai trong bảng kiểm kê. Không cần đổi mã sản phẩm.

**Đối chiếu lượt trước**

| Finding | Trạng thái | Phép đo |
|---|---|---|
| S822-01 | **ĐÃ ĐÓNG** | M3 tách ba dạng ca; bỏ khử trùng giữ rc=0 nhưng số `gate id=` đổi 1→2. Các fixture sai kiểu D3–D6 đều cho 12→0, không crash. |
| S822-02 | **CÒN MỞ — vá sinh lỗi mới** | Đã bỏ suy tương đương từ suite im lặng, nhưng nhánh phủ chồng mới mâu thuẫn A5 như phản chứng K06. |
| S822-03 | **ĐÃ ĐÓNG** | Prototype chỉ sửa bản sao tệp test: loại tín dụng cho crash, nhận fallback `suite=1`; bỏ phép loại crash làm ca tự kiểm đỏ. M6/A12 khả thi trong write set. |
| S822-04 | **ĐÃ ĐÓNG** | A1 khai đúng phạm vi target+controls; probe A11 chạy được cả 104 ca kg và hai ca codepage dưới từng D. |

**Bảng kiểm lời khai số**

Đo ngày 18-10-2026 UTC trên exact SHA nêu trên.

| Phép đo | Kết quả |
|---|---|
| Diff base→HEAD | Đúng một tệp mới, `ops/specs/wp822.md`, +178/-0 |
| Kiểm kê | Đủ 37 ID K; 37−6=31 |
| Nền `_KG_CA` / toàn họ kg / mọi ca gọi gate đã xác định | 100/100 · 104/104 · 106/106 |
| D1/K18 | Neo 1 chỗ; đỏ 0/100, 0/104, 0/106 |
| D2/K35 | Neo 1 chỗ; đỏ 0/100, 0/104, 0/106 |
| D3/K10 | Neo 1 chỗ; đỏ 0/100, 0/104, 0/106 |
| D4/K11 | Neo 1 chỗ; đỏ 0/100, 0/104, 0/106 |
| D5/K12 | Neo 1 chỗ; đỏ 0/100, 0/104, 0/106 |
| D6/K13 | Neo 1 chỗ; đỏ 0/100, 0/104, 0/106 |
| A2, sáu fixture riêng | Cả sáu: nền rc=12 đúng lý do → mutant rc=0 |
| A3, nền | rc=12, `thiếu/sai kiểu trường ['conclusion']` |
| A3, D6 | rc=12, khai 1/có 2 id, `THỪA id` |
| K37 | Đổi `_VANG`→`None`: thiếu conclusion 12→0; null vẫn 0; sai kiểu vẫn 12 |
| Toàn suite | **passed**, rc=0, `405/405`, `TỔNG: ĐẠT`; một ca Windows skipped |
| Tự kiểm mutant nền | Runner báo giết 167/168; một mutant Windows skipped |
| `doctrine-scan` / `adr-song` | rc=0; 10 tệp/0 chỗ chép; 53 ADR/53 dòng |
| Ruff contract | rc=0, `RUFF_CONTRACT 3 []` |
| Bare Ruff | **failed** trên base/head: cùng rc=1 và hai F541; delta=0 |

Checkout giữ nguyên HEAD/tree, index và bytes của 3.764 tệp qua snapshot đầu/cuối. GitHub/lease, H1–H3 và authority áp trần 8/450 chưa đo được trong lượt offline này. CI, release gate và LIVE `not_run`.

Đã lưu [verdict đầy đủ](../verdict-luot2.md) và [manifest bằng chứng](/tmp/wp822-review-r2-8ad04492/evidence_manifest.json).