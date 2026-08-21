Đã đo xong. Báo cáo toàn văn:

---

# THẨM ĐỊNH ĐỘC LẬP — vòng lặp tri thức `tra-luat` (worktree `0333948`)

Phép đo của đề bài đã kiểm lại: 7 chỗ đựng đúng số (565 dòng CLAUDE.md · 481 NO_KY_THUAT · 45 ADR · 24+24 receipt/verdict · 7648 CHANGELOG) — ĐO ĐƯỢC. `bai_hoc` trong `ops/lease_publish.py` + `packet_loop.py` = 0/0 — ĐO ĐƯỢC. `hinh_dang_lap` đúng 2 tệp văn bản, 0 dòng mã — ĐO ĐƯỢC. Thêm một phép đo đề bài KHÔNG chạy: **`grep seam ops/reviews/*.receipt.yaml` → 0** — "cùng SEAM" không tồn tại dưới dạng máy đọc được ở bất kỳ biên nhận nào; nó chỉ sống trong `ops/KE_HOACH_*` và prompt. Con số này giết một nửa đề xuất, xem C2.

## C1 — Khung "kho bài học" SAI, và "truy xuất" cũng SAI

Cả hai chẩn đoán đều bị chính ba dữ kiện của đề bài bác:

- Ca 1 (`$?` ×3): cả ba bên **đã đọc** bài học → không phải lỗi lưu, không phải lỗi truy xuất.
- Ca 2: bài học nằm **cách vài chục dòng trong chính tệp đang sửa** — truy xuất hoàn hảo tuyệt đối, vẫn tái phát. Đây là phản chứng chết người cho mọi đề án "đưa bài học tới đúng lúc": nó ĐÃ ở đúng lúc, đúng chỗ, đúng màn hình.

⇒ Vấn đề không phải LƯU, không phải TRUY XUẤT, mà là **DẠNG TỒN TẠI**: văn xuôi không chặn được hành vi lúc gõ phím; chỉ phép kiểm chạy trong gate mới chặn. Kho đã tự viết ra đúng doctrine này ("phép thử không chạy thì không tồn tại") — và đề bài này là bằng chứng kho không tuân chính doctrine của mình. Tất định hoá việc LƯU giải quyết **zero** trong ba ca. SUY LUẬN, nhưng suy từ ba phản chứng đo được.

## C2 — Tấn công ba cạnh máy

**Cạnh (1) — kế thừa `hinh_dang_lap` + cổng `dem>=3`: KHÔNG HOÀN VỐN.**
- Cách lách rẻ nhất: **đặt tên hình dạng khác đi**. "Cùng hình dạng" là phán đoán người; cổng chỉ đọc con số người tự khai. Không khai, hoặc khai hình dạng mới ⇒ đếm mãi 1. Cổng gate dữ liệu tự-báo-cáo là cổng gate sự thành thật, không gate hành vi.
- Báo động giả: cổng đòi khối `quyet_dinh_kien_truc` nhưng chỉ kiểm **SỰ CÓ MẶT** của khối — đúng lỗi "CÓ MẶT ≠ DÙNG ĐƯỢC" kho đã trả giá bốn lần. Sau 2 lần bị chặn, người ta paste một khối boilerplate và cổng xanh vĩnh viễn.
- Chi phí ẩn: kế thừa xuyên packet đòi một **tệp state dùng chung** mà mọi packet phải merge-update — trong ngày mà chi phí lớn nhất là 4 lần gộp master, đề xuất này *thêm một điểm merge nữa*. SUY LUẬN.

**Cạnh (2) — `doi_ke_hoach` + chặn packet kế nhiệm cùng seam: KHÔNG DỰNG ĐƯỢC như mô tả.**
- ĐO ĐƯỢC: seam không có trong receipt nào (0/24). Vị từ "cùng seam" chưa tồn tại ⇒ cổng này hiện là **cổng giả theo định nghĩa của chính đề bài**.
- Cách lách rẻ nhất: khai `can: false` (tự báo cáo), hoặc đặt packet kế nhiệm ở "seam khác" trên giấy.
- Báo động giả nguy hiểm nhất: `can: true` + MCR đang **chờ người duyệt** (protocol §3.1.1: MCR material phải human ghi quyết định) ⇒ mọi packet cùng seam đứng hình theo độ trễ của người. Người giữ kho sẽ học cách bảo executor đừng ghi `can: true`. Cổng dạy người ta **im lặng** — ngược đúng 180° với mục tiêu của cạnh (3).

**Cạnh (3) — `rXX_` hoặc `chi_la_chu: true`: cạnh DUY NHẤT hoàn vốn**, với hai điều kiện:
- Chỉ áp **forward-only** trên đơn vị máy đọc được (receipt/khối YAML mới), đừng áp lên 161 dòng văn xuôi CLAUDE.md — muốn áp lên đó phải dựng "lesson registry", tức chỗ đựng thứ 8, xem C6.
- Chấp nhận trước rằng cách lách rẻ là spam `chi_la_chu: true`. Nó vẫn hoàn vốn vì sản phẩm phụ: một **bảng kiểm kê đo được** `chi_la_chu / tổng` — lần đầu tiên kho đo được tỷ lệ bài học không răng, thay vì đoán.

## C3 — "Bài học ⇒ MCR" không tất định hoá được, nói thẳng

"Kế hoạch sai" là phán đoán. Không vị từ máy nào tính được nó, và mọi proxy (đếm hình dạng, từ khoá) đều gate được **lời khai về phán đoán** chứ không gate phán đoán. Thứ tất định hoá được là **sổ sách SAU phán đoán**: một khi ai đó ĐÃ viết `can: true` thì bắt buộc có `mcr: <id>` hoặc `mcr: null` kèm lý do — đó là chốt CẤM IM LẶNG kiểu cạnh (3), enforce được bằng schema-check trong `lease_publish.py` (nó đã có `_doc_yaml` + họ mã `Chan`). Còn cái CÒ "khi nào bài học buộc sinh MCR" — không gate được, và receipt PLAT-M4 chứng minh cơ chế người vẫn chạy: khối `chot_da_de_xuat_ma_CHUA_dung` trong đó chính là một MCR-trigger viết tay, đúng và kịp thời, không cần cổng nào. ĐỌC ĐƯỢC.

## C4 — Chỉ mục theo CÒ: một lớp văn xuôi nữa

Ca 2 là phản chứng trực tiếp: bài học đứng ngay tại điểm cò, vẫn chết. Agent grep khi **đã nghi ngờ** — mà tái phát xảy ra đúng lúc *không* nghi ngờ. Hook in "nhóm bài học liên quan" = bơm thêm văn xuôi vào context, và kho chưa có một phép đo nào cho thấy văn xuôi trong context đổi hành vi (bằng chứng ngược thì có ba).
Đo được không? Có, nhưng đắt và yếu: đếm trong hậu kiểm sự cố xem bài học liên quan có được in trước hành động không — mẫu nhỏ, nhiễu lớn, kết luận chậm hàng tháng. Đáng làm hơn: lấy cò tần suất cao nhất (`khi:đọc-rc`) và **cơ giới hoá thẳng nó thành lint** — bẫy `MA=$?` sau pipeline là mẫu văn bản tĩnh, quét được y như `actionlint` đã quét workflow. Một cò thành lint ăn đứt mười cò thành tag. SUY LUẬN có tiền lệ đo được (actionlint bắt thứ 6 lượt review bằng mắt không bắt nổi).

## C5 — MỘT thứ rẻ nhất

**Luật một dòng, enforce tại receipt-check: "bài học nào cơ giới hoá được thì PHẢI kèm ca `rXX_`/lint NGAY trong PR ghi nó; không cơ giới hoá được thì khai `chi_la_chu: true`."** Chiếu ba ca:

1. `$?` ×3 → **CHẶN**: lần tái phát ĐẦU đã phải sinh lint quét mẫu `\$\?` sau pipe trong `scripts/ ops/ .claude/`; hai lần sau chết ở gate, không tới người.
2. Manifest/ratchet trong `tl_selftest.py` → **CHẶN**: khối "ĐÃ TRẢ GIÁ" đó cơ giới hoá được (guard selftest); luật này ép nó thành guard từ lúc viết.
3. Kế hoạch trên PR chưa merge → **KHÔNG CHẶN — khai thẳng.** Đây là lỗi lớp XUẤT BẢN, không phải lớp bài học; thuốc của nó kho đã có sẵn (bài "tìm ở master trước, chưa thấy thì fetch nhánh X" + ref bền `luu-tru/*`): mở rộng chốt neo có sẵn trong `lease_publish.py` — tài liệu mà lease/packet trích dẫn phải resolve được từ ref bền, không phải từ nhánh PR. Không thứ nào chặn cả 3; đừng gò một thứ chặn cả ba rồi được một thứ chặn mơ hồ cả ba.

## C6 — Tôi KHÔNG xây

1. Tệp state kế thừa `hinh_dang_lap` xuyên packet — thêm điểm merge vào ngày đã nghẹt quản trị.
2. Cổng CHẶN "cùng seam thiếu MCR" — vị từ chưa tồn tại (đo: 0/24), và nó dạy người ta khai `can: false`.
3. Chỗ đựng thứ 8 / "lesson registry" / retro-tag 161 dòng CLAUDE.md.
4. Hook in nhóm bài học theo cò — chi phí context chắc chắn, hiệu quả chưa từng đo được, phản chứng có sẵn (ca 2).
5. Bất kỳ cổng nào kiểm SỰ CÓ MẶT của một khối văn bản — kho có bốn vết sẹo đúng hình dạng này rồi.

---

## TOI_KY

1. **Cạnh (3), forward-only, tại receipt-check của `ops/lease_publish.py`**: receipt/khối bài học mới phải có `rxx: <tên ca>` HOẶC `chi_la_chu: true`; thiếu cả hai ⇒ rc khác 0. Kèm mutant: xoá trường ⇒ ca test đích ĐỎ. — **CƯỠNG CHẾ MÁY.**
2. **Lint bẫy `$?`-sau-pipeline** (mẫu tĩnh, phạm vi `scripts/ ops/ .claude/dev/`), fail-close khi thiếu công cụ, chạy trong gate — trả nợ luật ở mục 1 cho đúng ca tái phát ×3. — **CƯỠNG CHẾ MÁY.**
3. **Chốt neo tài liệu vào ref bền**: kế hoạch/spec mà lease trích phải resolve từ `master` hoặc `luu-tru/*` (mở rộng `_kiem_neo_prompt` sẵn có), chặn đúng ca 3. — **CƯỠNG CHẾ MÁY.**
4. Trong khối `can: true` (nếu ai tự viết): bắt buộc `mcr: <id>` hoặc `mcr: null + lý do` — CẤM IM LẶNG, không chặn packet nào. — **CƯỠNG CHẾ MÁY** (schema), còn cái cò sinh `can: true` — **CHỈ LÀ CHỮ**, và phải nói thẳng như vậy trong tài liệu.
5. Tag cò (`khi:…`) nếu muốn thì cứ làm — **CHỈ LÀ CHỮ**, cấm ghi vào bất kỳ đâu rằng nó là biện pháp chống tái phát khi chưa có số đo.

## TOI_KHONG_KY

- Cạnh (1) nguyên trạng: kế thừa bộ đếm + cổng `dem>=3` đòi khối `quyet_dinh_kien_truc` — gate tự-báo-cáo, kiểm-có-mặt, thêm điểm merge; ba tật, tật nào kho cũng đã trả giá riêng một lần.
- Cạnh (2) như đề xuất: cổng "cùng seam" khi seam chưa máy-đọc-được ở đâu cả — đó là cổng giả, và đề bài tự dặn đừng vẽ cổng giả.
- Mọi diễn giải rằng vấn đề là LƯU hay TRUY XUẤT — ca 2 giết cả hai; vấn đề là DẠNG: bài học chưa thành phép kiểm chạy được thì chưa tồn tại, và kho đã tự viết câu đó trước tôi.

**KHÔNG ĐO ĐƯỢC (khai):** tần suất thật của mẫu `$?`-sau-pipeline hiện còn trong cây (chưa viết lint nên chưa quét); hiệu quả hành vi của mọi lớp văn xuôi (không có baseline); chi phí giờ-người của 4 lần gộp master (chỉ có lời kể trong đề bài).