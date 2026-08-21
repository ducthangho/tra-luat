
codex
**ĐO ĐƯỢC:** Không tệp nào được tạo hoặc sửa; `./kho` chỉ được đọc.

## D1

**ĐỌC ĐƯỢC:** Hai đề xuất là hai tầng khác nhau. Ba cổng hẹp là các vị từ cụ thể; `evidence-preflight` là runner chọn, chạy và đóng biên nhận cho các vị từ ấy. Runner không có catalog có thẩm quyền thì chỉ là vỏ.

**SUY LUẬN — ĐỔI Ý SO VỚI VÒNG 1:** Nếu buộc chọn trong D1, tôi chọn phía **cổng hẹp**, trước hết là neo tài liệu. Tôi không còn ký `evidence-preflight` làm packet đầu vì kho hiện chưa có nguồn máy nào quyết định đầy đủ `required_checks`.

Phản thực ba ca:

1. **SUY LUẬN — `$?`:** lint hẹp chặn đúng mẫu đã tái phát; runner chỉ chặn rộng hơn nếu check đúng được chọn và chính script không tự nuốt mã thoát.
2. **SUY LUẬN — manifest/ratchet:** ba cổng hẹp **không chặn**. Runner có thể chặn nếu policy canonical thật sự ánh xạ thay đổi docs sang full selftest chứa `r291`; ánh xạ ấy hiện chưa tồn tại.
3. **ĐO ĐƯỢC — spec chưa merge:** cổng neo ref bền chặn đúng hai lease lịch sử. Runner cũng chỉ chặn nếu nó gọi chính vị từ neo này. Cổng `mcr` không liên quan.

**SUY LUẬN:** Loại runner làm mất việc chuẩn hóa receipt và bỏ sót ca manifest/ratchet; đó là mất mát cụ thể. Đổi lại, không dựng một runner có vẻ tổng quát nhưng chưa biết phải chạy gì.

## D2

**ĐO ĐƯỢC:** `required_checks` xuất hiện **0 lần** trong `packet_loop.py` và `lease_publish.py`; `.github/coordination/change-impact.v1.json` không tồn tại.

**ĐỌC ĐƯỢC:** Theo protocol, danh sách đúng phải do dispatcher suy từ policy canonical, actual diff và test catalog; Packet không được tự khai. CI phải tính lại độc lập, unknown phải fallback full.

**SUY LUẬN — cách lách rẻ nhất:** rút ngắn danh sách, làm changed path rơi ngoài mapping, hoặc bọc check trong script luôn trả `0`. `subprocess` không qua shell không cứu được một script con tự nuốt lỗi.

**SUY LUẬN — báo động giả tệ nhất:** chạy check hậu-thay-đổi ngay lúc cấp executor lease, khi head/diff tương lai chưa tồn tại; hoặc ép check phụ thuộc Windows/công cụ ngoài nền trên mọi thay đổi docs. Kết quả hoặc đo nhầm base, hoặc chặn việc vô can.

**SUY LUẬN — chi phí ẩn:** catalog/policy được bảo vệ, selector fail-closed, môi trường cô lập không secret cho mã nhánh, timeout/dọn cây tiến trình, bằng chứng dương, exact SHA/tree/policy/runner/OS, lưu và kiểm receipt, xử lý flake. Đây không phải một packet `sensitive` ≤3 tệp/300 dòng.

**SUY LUẬN:** Người ngăn rút ngắn phải là required CI trên policy canonical có review và hash được ghi vào receipt. Hiện chưa đo được branch protection ngoài kho, nên chưa có căn cứ nói lớp đó đang bảo vệ gì.

## D3

**ĐO ĐƯỢC:** `chi_la_chu` hiện có **0** occurrence và không có bộ đọc hay phép đo nào làm nó đỏ.

**SUY LUẬN:** Vì vậy `chi_la_chu: true` hiện là **CHỈ LÀ CHỮ**; tôi không ký.

**SUY LUẬN:** Nếu làm sau này, nó chỉ hợp lệ như nợ: ghi trong receipt hiện có kèm `debt_ref`; validator receipt đọc; đỏ khi `debt_ref` thiếu, không resolve, hoặc quá hạn. `ops/NO_KY_THUAT.md` hiện chưa có schema ID/hạn máy đọc được, nên điều kiện này chưa xây được mà không mở thêm thiết kế.

## D4

**ĐỌC ĐƯỢC:** Protocol đã có bốn hậu quả khác nhau: giữ nguyên, Packet revision, MCR và Mission mới.

**SUY LUẬN:** Chọn:

```yaml
plan_impact: none | packet_revision | mcr_candidate | new_mission
decision_by: <actor>
decision_ref: <durable-ref>
reason: <text>
impact_ref: <packet-revision | mcr-id | mission-id | null>
```

**SUY LUẬN — phần máy kiểm được:** `packet_revision` đòi revision/generation mới và lease cũ bị thu hồi; `mcr_candidate` đòi MCR tồn tại cùng phần bị pause; `new_mission` đòi liên kết supersede; `none` chỉ đòi người quyết, lý do và dấu vết.

**SUY LUẬN:** `mcr: id|null + lý do` chỉ bắt được sổ sách sau khi ai đó đã khai `can:true`; nó bỏ sót Packet revision và Mission mới. Schema `plan_impact` ở trên không mất ca riêng nào của nó vì `mcr_candidate` vẫn bắt buộc `impact_ref`. Cả hai đều bị lách bằng lời khai `none`/`false`; máy không phải oracle quyết định kế hoạch sai.

## D5

**SUY LUẬN — đổi thứ tự vì D6:** Packet được ký ở vòng này là script sandbox reviewer fail-đóng, không phải runner D1.

Write set tối thiểu:

```text
.claude/dev/packet_loop.py
.claude/dev/packet_loop_test.py
.claude/skills/cross-review/SKILL.md
```

**ĐỌC ĐƯỢC:** Đây là thay đổi review authority/gate lifecycle nên thuộc `sensitive`: tối đa 3 tệp và 300 dòng thêm theo ADR-0044. Write set vừa đúng trần ba tệp.

**SUY LUẬN — acceptance:** thêm lệnh `review-run` vào `packet_loop.py`, tái dùng `launcher.py`; sinh receipt sandbox; và làm `record-review` từ chối mọi review thiếu receipt hợp lệ. Bộ test phải tái hiện bốn lỗi ở D6 và chứng minh model stub chưa được gọi khi preflight đỏ.

**SUY LUẬN:** Packet Spec phải đặt hard stop `+300`. Nếu numstat thực vượt trần, lát đầu là hai tệp `packet_loop.py` + `packet_loop_test.py`; cập nhật adapter là successor docs-only. Không được bỏ test để lọt ngưỡng.

## D6

**ĐO ĐƯỢC:** Cùng hình dạng dựng sandbox/bundle bằng tay đã hỏng bốn lượt trong ba ngày; hiện adapter vẫn hướng dẫn gọi `codex exec` thủ công, không có script sandbox và `record-review` không đòi receipt.

**SUY LUẬN — kết luận:** **CẤM dựng sandbox reviewer bằng tay.** Đây là việc đi trước mọi cạnh D1. Một helper tùy chọn không đủ; đường chuyển state phải từ chối review không đi qua helper.

Script phải cưỡng chế:

1. **CƯỠNG CHẾ MÁY — SUY LUẬN:** đọc lease làm nguồn đầu vào; đòi `review_scope_base_sha`, exact reviewed SHA, prompt/spec `path + sha256 + ref SHA`; resolve từ Git object bền trước khi gọi model.
2. **CƯỠNG CHẾ MÁY — SUY LUẬN:** tự sinh full diff `review_scope_base_sha..reviewed_sha`; không nhận bundle diff ghép tay, nên không thể quên lát X4.
3. **CƯỠNG CHẾ MÁY — SUY LUẬN:** vật chất hóa repo tại `./kho` và mọi artefact trong một root có manifest/hash; từ chối path ra ngoài, tệp thiếu hoặc hash lệch.
4. **CƯỠNG CHẾ MÁY — SUY LUẬN:** write-probe thư mục output trước khi tiêu lời gọi; verdict lấy từ stdout do launcher giữ, không bắt reviewer tự ghi tệp.
5. **CƯỠNG CHẾ MÁY — SUY LUẬN:** gọi bằng argv trực tiếp, đọc `run.json`, mã thoát thật và bằng chứng dương; không pipeline, không `$?`, không `tail`.
6. **CƯỠNG CHẾ MÁY — SUY LUẬN:** sau chạy, exact head và cây review phải không đổi; receipt ràng manifest, run, stdout hash và reviewed SHA. `record-review` thiếu hoặc lệch receipt phải đỏ.

**SUY LUẬN:** `--cd <sandbox>` hay một câu “đừng đọc ra ngoài” không chứng minh closed-read scope. Không có sandbox OS được đo thì receipt phải khai `read_scope_enforced: false`, không được tự nâng thành bảo đảm.

## TOI_KY

1. **SUY LUẬN — CƯỠNG CHẾ MÁY:** Một packet duy nhất: `packet_loop review-run` dựng/chạy/ghi receipt sandbox; `record-review` cấm đường thủ công.
2. **SUY LUẬN — CHỈ LÀ CHỮ:** Sau packet này, ưu tiên D1 là neo tài liệu vào ref bền; chưa gộp lint và MCR vào cùng packet.
3. **SUY LUẬN — CHỈ LÀ CHỮ + CƯỠNG CHẾ MÁY Ở HẬU QUẢ:** dùng `plan_impact`; lựa chọn enum thuộc human, còn revision/MCR/Mission và thu hồi lease phải được máy kiểm.

## TOI_KHONG_KY

1. **SUY LUẬN:** `evidence-preflight` tổng quát trước khi có policy/catalog canonical.
2. **ĐO ĐƯỢC:** `chi_la_chu: true` như bảo đảm hoặc metric “đo được” khi chưa có phép làm đỏ.
3. **SUY LUẬN:** `mcr: id|null` đứng một mình, hoặc boolean `can`, như oracle phát hiện kế hoạch sai.
4. **SUY LUẬN:** script sandbox tùy chọn nhưng `record-review` vẫn nhận lượt thủ công.
5. **SUY LUẬN:** nhét sandbox, ba cổng D1 và schema kế hoạch vào một packet `sensitive`.

## KHONG_DO_DUOC

- **ĐỌC ĐƯỢC:** Chưa có diff nên chưa đo được số dòng thêm thực tế của packet D5.
- **ĐỌC ĐƯỢC:** Chưa có bằng chứng rằng runtime hiện tại cưỡng chế được closed-read scope ở tầng OS.
- **ĐỌC ĐƯỢC:** Chưa đo được branch protection/required contexts ngoài kho.
- **ĐỌC ĐƯỢC:** Chưa có runner để đo false-positive, thời gian tăng thêm hay tỷ lệ bỏ sót của `evidence-preflight`.
tokens used
251,922
