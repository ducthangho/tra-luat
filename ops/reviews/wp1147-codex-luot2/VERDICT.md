Verdict: approve
Reviewed commit: 2344011617fa753adceef0be3306374cb3a096a1
Spec sha256: b8f69631a070aab3effee8c40e21a7159964885363287f94e682c5e5afa2cd96

Rà soát độc lập Packet #1147, revision 2, generation 2, lease `wp1147-r2-g2-claude`, lượt 2/10. **P0 = P1 = P2 = P3 mở = 0.** Approve theo ngưỡng nội dung trong prompt giao review. N2, N3′ bộ đầy đủ và N6 còn `not_measured`; verdict không xác nhận hoàn tất mọi nghiệm thu.

Reviewer Codex/OpenAI; executor Claude theo packet; `review_class: sensitive`, `assurance_target: cross_approved`. Metadata launcher `runs/83e3a368/run.json` khai `provider: openai_codex`, `execution_surface: codex_cli`, `transport: machine`, run ID `83e3a368aa8341c68934e109e31de3ee`. Model/effort thực tế và attestation từng request: `not_measured`; không suy chúng từ tên CLI, không tự tạo receipt hay chuyển state assurance. Không dùng phiên/context của executor.

Định danh đã tự đo: head detached, tree `4d5c6f7464a67ff20f29aa5dbf35d1f57eff6112`; cha 1 `f2176345f3d6cf564ad827f7648416b4cc488204`, cha 2 `1f0941e9bba1d1d517eda4174167b81963c06bd5`. Base đặc tả `02ddeb4e9ea9c130d935adc4d5bce4f11db7d6a0`; r1 `7295d5c7171267c8abf13b711108c315fe697b73`. SHA-256 r1 `983d5490e6dadcb61c664c7dde8af44adb5f440161cbef37292f61bffd46e0ba`; r2 khớp dòng 3. Diff r1→r2 chỉ `ops/ci_provenance_test.py` (+9/−2); diff master→head cũng chỉ tệp đó (+51/−9). Master từ base tới cha 2 không chạm write set. [Bằng chứng định danh](evidence/identity.json), [diff r2](evidence/r2.diff), [diff toàn packet](evidence/packet.diff).

Mọi phép thử chạy trên bản sao `git archive` của exact commits dưới `out/base`, `out/r1`, `out/head` hoặc mutant dưới `out/mutants`. Đã đối chiếu byte test, sản phẩm, registry và workflow của các bản sao với Git; sản phẩm và registry giống nhau ở ba mốc. Linux x86-64, Python 3.13.18, Git 2.43.0; bare Ruff 0.17.3. SRC không có delta quan sát được giữa hai snapshot HEAD/tree/index, tracked/untracked/ignored và SHA-256 toàn bộ tệp ngoài `.git`; [trước](evidence/src_before.json), [sau](evidence/src_after.json). Đây là so hai mốc, không phải chứng minh lịch sử chưa từng ghi rồi hoàn nguyên; mọi lệnh của reviewer chỉ ghi dưới OUT. Không mạng/GitHub/push/merge/land.

| slug | hạng | file:dòng | phép đo | hướng vá |
|---|---|---|---|---|
| c63-thieu-phan-biet-hai-thanh-phan-khoa | P3 lượt 1; đã đóng, 0 còn mở | `ops/ci_provenance_test.py:1458`, `:1876` | Hai mutant khóa rc 0 ở r1 → rc 3/DO:c63_ ở head; head xanh, cache có sẵn được phục hồi. | Không cần vá thêm trong lớp đã đo. |
| c62-dung-som-giu-ngu-nghia | đạt, không finding | `ops/ci_provenance_test.py:1161` | Cùng 617 mục theo đúng thứ tự; oracle đủ 455 lượt; F13 55/55 GIET ở base/head; không đổi sang TIN_DUNG_GIA/HONG. | Không cần vá. |
| c62-oracle-va-chot-sau-vong | đạt, không finding | `ops/ci_provenance_test.py:1166`, `:1177`, `:1190` | Trace head xanh chạy mọi chốt; cố ý làm lệch oracle/bỏ một lượt oracle đều rc 3 ở base/head; bỏ lượt đọc SHA-256 bị chốt mới bắt rc 3. | Không cần vá. |
| tuong-duong-phan-hang | đạt, không finding | `ops/ci_provenance_test.py:1884`, `:1891` | 150/150 mục đo độc lập khớp base và đúng kỳ vọng; gồm toàn F13/B2, mẫu mọi ca đích và TU_KIEM. | Không cần vá. |
| nen-do-va-khoa-cache | đạt, không finding | `ops/ci_provenance_test.py:1875`, `:1900` | Nền đỏ: 400/400 HONG, 57 lần gọi nền/57 ca; chạy thật mẫu: head 57 lần nền, base 150 lần; mỗi mục vẫn chạy mutant riêng. | Không cần vá. |
| qua-han-va-tin-dung-gia | đạt, không finding | `ops/ci_provenance_test.py:1865`, `:1884`, `:1908` | Timeout nền/mutant đều HONG; 18 tổ hợp rc/output khớp base; lỗi vô can trong wrapper c62 vẫn rc 4 ở cả hai. | Không cần vá. |

**ĐỐI CHIẾU LƯỢT TRƯỚC:** lớp duy nhất `c63-thieu-phan-biet-hai-thanh-phan-khoa`, nguồn [verdict lượt 1](../tham-chieu/luot1-VERDICT.md) trên `7295d5c…`: **ĐÃ VÁ THẬT**. Dựng lại hai biến đổi khóa theo lượt 1; cặp neo/thay, lệnh, output và rc nằm trong [quick.json](evidence/quick.json), mục `manual_mutants`; mã thử ở `mutants/r1/` và `mutants/head/`.

| Mutant | r1 rc | Head rc / tín hiệu |
|---|---|---|
| `drop_case_from_key` | 0 | 3, `DO:c63_` |
| `drop_content_from_key` | 0 | 3, `DO:c63_` |

Bỏ ca làm cặp `(ca_b, x)` nhận nhầm `ca_a:x`; bỏ nội dung làm `(ca_a, y)` nhận nhầm `ca_a:x`; cả hai chỉ chạy 2 lần. Head đúng trả riêng ba giá trị, gọi 5 yêu cầu nhưng chỉ chạy 3 lần. N1 cũng được đo lại: gỡ cache, gỡ bắt TimeoutExpired và cho bản gốc đỏ đi tiếp đều rc 3 với DO của chính c63; CLI và dispatch import của head rc 0. Mock phục hồi cache có sẵn. Không phát hiện lỗi mới do bản vá M5 trong phạm vi này.

M4 giữ nguyên byte của toàn bộ đoạn dựng fixture trước vòng so và toàn bộ oracle/chốt sau vòng so. `ca` có 616 mục, thêm SHA-256 thành 617; băm có thứ tự của `ca`, `mong`, `kq` và `nat` trùng base/head. Trace c62 xanh rc 0 hai phía đo `len(kq) = len(mong) = len(ca)+1 = 617`, `da_so = 455` (454 lượt SHA-1 + 1 SHA-256, 446 OID phân biệt vì fixture có trùng). Head thực thi 1084 phép `bang` của c62, tất cả đúng, gồm oracle Git native, số lượt oracle, thiếu Git trên PATH, Git rc khác 0, năm output/lỗi tiêm và tích hợp main với commit ISO-8859-1. [Trace và assertion](evidence/quick.json).

Đầu ra sai được `bang` bắt ngay bằng cùng lớp `TinHieuChotCa`; wrapper `doc`, `chay_ca` và `phan_hang` không thay đổi. Dừng sớm sau một vi phạm đã đủ để giết mutant, còn head đúng vẫn đi hết oracle và chốt sau vòng. Đo thêm oracle cố ý sai, thiếu một lượt oracle và thiếu lượt đọc SHA-256 đều rc 3 đúng ca; lỗi vô can ngoài reader vẫn rc 4, không nhận GIET. [Bảy phản chứng c62](evidence/c62_negative.json). Không phát hiện phép kiểm trước đỏ nay mất khả năng bắt lỗi trong các phản chứng đã chạy.

Đã chạy **toàn bộ 55 F13 và 6 B2 qua `chay_dot_bien`** trên base đặc tả và exact head, thứ tự tuần tự. Với mọi mutant F13, subprocess ở cả hai phía đều rc 3 và giữ đầy đủ `DO:c62_git_commit_khong_utf8:`; thông báo mới nêu vị trí lệch đầu, giá trị thực và kỳ vọng. Engine phân hạng trên output đầy đủ trước khi cắt đuôi 200 ký tự để trả chi tiết. Đuôi có thể không còn marker (base 28/55, head 31/55); đây là giới hạn hiển thị sẵn có của engine, không mất tín hiệu phân hạng. Output đầy đủ đã được lưu trong `child_events` của [mutations.json](evidence/mutations.json).

| Phạm vi | Mục | Base (s) | Head (s) | Hạng base/head |
|---|---:|---:|---:|---|
| F13_* đầy đủ | 55 | 265.415 | 84.088 | 55 GIET / 55 GIET |
| B2_* đầy đủ | 6 | 2.479 | 1.402 | 6 GIET / 6 GIET |
| Hợp không lặp của toàn bộ phép đo | 150 | 478.971 | 244.240 | 148 GIET, 1 TIN_DUNG_GIA, 1 SONG_SOT ở mỗi phía |

Số đo là tổng thời gian từng lời gọi engine trong cùng một lệnh, base rồi head cho từng mục, một luồng; cache của head ban đầu rỗng và sống xuyên các mục. Riêng thời gian subprocess mutant F13, loại thời gian nền để quan sát thay đổi c62: base 129.564 s → head 81.843 s. Đây là phép đo tập đích trên Linux, **không thay N3′ của bộ mặc định**, không suy kết quả Windows.

Mẫu như lượt 1 chọn mục đầu và cuối theo thứ tự bảng cho từng ca đích: **91 DOT_BIEN phủ đủ 56 ca đích + 2 TU_KIEM = 93 mục**, 93/93 khớp base và đúng kỳ vọng (91 GIET, 1 TIN_DUNG_GIA, 1 SONG_SOT); tính controls phủ 57 ca. Hợp với F13/B2 là 150 mục không lặp, không phải toàn bộ 398 mutant. Cả bảng 398 DOT_BIEN và 2 TU_KIEM giữ nguyên giữa base/r1/head; CA tăng 62→63. Không suy hạng của 250 mục chưa chạy thật từ mẫu. Probe nền đỏ dùng mock có phủ đủ cả 400 mục. [Bảng từng mục](evidence/mutation_comparison.tsv), [log](evidence/mutations.log), [tổng đo](evidence/summary.json).

| Nghiệm thu | Trạng thái reviewer | rc | Bằng chứng dương / giới hạn |
|---|---|---|---|
| N1 r1: c63 + ba mutant bắt buộc | passed | head 0; từng mutant 3 | Cả ba DO:c63_, không phải setup/import error; [quick.json](evidence/quick.json). |
| N2 r1: bộ mặc định Linux exact head | not_measured; not_run theo prompt | — | Không chạy suite mặc định. Đo độc lập CA 62→63, DOT_BIEN 398 giữ nguyên, mẫu và TU_KIEM đúng; không thay marker CA/DOT BIEN/TONG của cả suite. Gói này không có log đầy đủ exact head để xác nhận. |
| N3′ r2: Linux head không chậm hơn base | not_measured cho bộ mặc định | probe 0 | Tập đích/mẫu nhanh hơn theo bảng trên; chưa đo đầy đủ nên không khai N3′ đạt. |
| N3′ r2: Windows head dưới 5400 s | not_measured | — | Windows native ngoài phạm vi; số 7745 s là lời khai về r1, không phải kết quả head đang review. |
| N4 r1: bare Ruff F delta=0, diff-check | passed | base/r1/head 0/0/0; diff 0 | Ruff 0.17.3, `--no-cache --select F`, cả ba “All checks passed!”, delta 0; diff master→head không diagnostic. [Các log](evidence/ruff_head.log). Không coi đây là kiểm pin/probe contract của Ruff. |
| N5 r1: doctrine-scan; adr-song | passed | 0; 0 | [doctrine-scan](evidence/doctrine-scan.log): 10 tệp, 0 chỗ chép; [adr-song](evidence/adr-song.log): 61 ADR/61 dòng, khớp 1–1 (ngoại lệ trạng thái 0016 được tool báo rõ). |
| N6 r1: ci.yml xanh hai nền trên exact head | not_measured | — | Không truy cập GitHub theo prompt offline; không có check-run receipt exact head trong gói. |
| N7 r1 | không định nghĩa trong r1 | — | r1 chỉ có N1–N6; N7 được bổ sung ở r2. |
| N7 r2: hai mutant M5 | passed | từng mutant 3 | Hai khóa thiếu thành phần đều DO:c63_; đối chứng r1 cùng hai mutant rc 0; head nguyên bản rc 0. |

Lệnh tái lập (từ workspace, các bản sao đã dựng):

```sh
export PYTHONDONTWRITEBYTECODE=1
export TMPDIR="$PWD/out/tmp"
export GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null
python3 -B out/review_probe.py quick
python3 -B out/review_probe.py mutations
python3 -B out/c62_negative_probes.py
python3 -B out/review_probe.py final-identity
python3 -B out/assemble_verdict.py
```

Các probe trên đều hoàn tất rc 0; script lưu command/rc/output của CLI, mutant và gate. Khi bổ sung trace, harness reviewer đã đổi wrapper mock sang thay trực tiếp để ghi đúng frame gọi `bang`; phép trace hoàn chỉnh được chạy lại, không tính lỗi quan sát của harness là lỗi ứng viên. Không chạy suite mặc định đầy đủ, không mở rộng nợ wp978, không soạn payload đường dẫn thoát cây. Hướng kiểm dạng đường dẫn thoát cây, nếu được giao sau này, chỉ nên mô tả ý định kiểm việc từ chối và cô lập đường dẫn; chưa đo trong lượt này.

Approval chỉ neo commit dòng 2; không cấp quyền push, merge hay land, không miễn N2/N3′/N6 còn thiếu bằng chứng.
