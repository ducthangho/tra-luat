Reviewed commit: fafbe1556ebc73b81252737cbdec9de4b00860ad
Verdict: request_changes — P1=0 P2=0 P3=1

Reviewer: Codex, họ GPT/OpenAI, execution surface công cụ local shell qua API, transport machine/local. Review độc lập với executor Claude; không suy danh tính từ tài khoản GitHub. KHO=/home/user/rv773 được giữ read-only. Head tree: f50622a5ecd921e579982cda6bcd8acc46ffd736.

## Finding

### P3 — Nguồn của phép đo sau sửa là manifest đầu vào, không phải kết quả phép đo

`ops/land/pr772-wp766-land-evidence.yaml:142` (nội dung dòng 143–146), `sua_gate_master.do_sau_sua` vẫn gắn nhãn `measured` cho release-verify, selftest 1731/1731, golden-test 20/20, rc=0 và cây không đổi, nhưng không trỏ tệp kết quả nào chứng minh chúng. Đây là lỗi sẵn có, được tính trong phạm vi mục 5 của yêu cầu review hồ sơ này; không phải lỗi mới do bốn con trỏ vừa thêm.

Tái hiện (Python 3.13, `/tmp/len.py` lấy từ commit 0f4830f):

```python
import sys, pathlib, yaml
sys.path.insert(0, '/tmp')
import len as g
r = pathlib.Path('/home/user/rv773')
t = r/'ops/land/pr772-wp766-land-evidence.yaml'
p = t.parent/'pr772-wp766-provenance'
v = yaml.safe_load(t.read_text())['sua_gate_master']['do_sau_sua']
print([(x, str(g.phan_giai(x,r,p,t))) for x in g.token_nguon(v)])
```

Đầu ra đo được:

```text
[('tl.py', 'None'), ('RELEASE_MANIFEST.json', '/home/user/rv773/RELEASE_MANIFEST.json'), ('tl.py', 'None'), ('tl.py', 'None')]
```

`rg -n '1731/1731|1a433a6|20/20|expected.*187' /home/user/rv773/ops/land/pr772-wp766-provenance` thoát 1, không dòng khớp. Mở manifest cho thấy đây là dữ liệu manifest, không phải transcript chạy các lệnh nói trên. Vì L1 chỉ đòi một tệp tồn tại, câu này vẫn qua cổng; việc manifest có thể xác nhận số lượng tệp không chứng minh selftest, golden-test, mã thoát hoặc cây không đổi. Không kết luận các kết quả khai là sai, chỉ kết luận nguồn được trỏ không chứng minh chúng.

Đề xuất: lưu và trỏ transcript/readback kết quả trên đúng cây, kèm lệnh, môi trường, exit status và phép đo cây không đổi, rồi cập nhật SHA256SUMS. Nếu không giữ được phép đo lịch sử, đổi nhãn phù hợp và ghi rõ giới hạn; không dùng manifest đầu vào làm chứng cứ cho kết quả chạy.

## Đã đo

- `git -C KHO status --porcelain`: rỗng cả trước và sau; `rev-parse HEAD` đúng exact SHA. `show -s fafbe15` đã đọc; `diff 653fef3 fafbe15` đúng 3 tệp, +13/−4. Không thấy thay đổi nghĩa của bốn lời khai: chỉ thêm con trỏ và làm rõ nguồn base.
- `git -C KHO show 0f4830f:ops/land_evidence_nguon.py > /tmp/len.py`; `python3.13 -B /tmp/len.py --root KHO`: rc=0, `1 ĐẠT · 28/28 miễn trừ · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC`, `TỔNG: ĐẠT`.
- `git -C KHO archive 653fef3 ops | tar -x -C /tmp/rv787-base`, rồi checker: rc=1, **5 L1**. L1 thứ năm là `do_sau_sua`, do bản archive chỉ có ops không có manifest gốc. Bổ sung cây đầy đủ bằng `git -C KHO archive 653fef3 | tar -x -C /tmp/rv787-base`, chạy lại: rc=1, đúng **4 L1** ở spec.nguon, khong_xung_dot, review.codex_connector, review.human_audit; 28/28 miễn trừ, TỔNG: ĐỎ. Điều này cũng xác nhận phụ thuộc tình cờ vào manifest của finding trên.
- `sha256sum KHO/ops/specs/wp766.md`: `da3095b47567dc8cb94137d0cc675d722eb256a77c8e06ddb90a216e7f148666`; `git -C KHO rev-parse HEAD:ops/specs/wp766.md`: `2176dd0c04e126beb6a57be645d315f51ebb2d23`. Token phân giải đúng tệp hiện tại, không có lệch blob lịch sử gây hiểu sai.
- `git -C KHO show 701f41c:ops/specs/wp766.md` thực tế **thoát 128**, tệp chưa có tại commit mã đó. Hash e3b0c44… từ pipeline sha256sum khi ấy chỉ là hash stdin rỗng, không phải hash spec. Đối chứng lịch sử đúng: `show fa33fa6:ops/specs/wp766.md | sha256sum` cho da3095b4… và `rev-parse fa33fa6:ops/specs/wp766.md` cho 2176dd0c… . Hồ sơ nói spec vào master qua PR ghi sổ nên việc chưa có trong 701f41c không phải finding.
- Tự chạy cả ba lệnh trong `do-tree-merge-e03d4bf.txt`: `git rev-parse e03d4bf^{tree}` và `git rev-parse 701f41c^{tree}` cùng trả `861df62ee0c17abf423908c5f41ba59b2604fdb4`; `git log -1 --format=%P e03d4bf` trả `e0273d31aba78b014aa89297f32ff86f9daf0277 701f41c686cef8456d43528ab9556a6b867cd7d6`. Cả ba khớp byte giá trị ghi, rc=0.
- Mở `readback-pr-772.json`: base.sha=e0273d31…, head.sha=701f41c6…, merge_commit_sha=e03d4bf7…, merged_at=2026-10-16T06:31:51Z; khớp cây và cha Git. Đây là bằng chứng gián tiếp đúng như nhãn, không phải lần chạy merge mới.
- Mở `readback-codex-connector-772.json`: user chatgpt-codex-connector[bot], code_review.commit_sha=701f41c686cef8456d43528ab9556a6b867cd7d6, status=completed, has_any_findings=false, has_unresolved_findings=false; updated_at=06:31:29Z, trước merge 22 giây. Con trỏ đúng.
- Mở `readback-comment-6209427062.json`: user ducthangho, author_association OWNER, performed_via_github_app null, created_at=updated_at=2026-10-16T06:20:30Z. Body có human audit và ủy quyền exact candidate. Con trỏ đúng.
- `(cd KHO/ops/land/pr772-wp766-provenance && sha256sum -c SHA256SUMS)`: rc=0, **23/23 OK**. So tập mọi tệp đệ quy với cột tên trong SHA256SUMS: không thiếu tệp dữ liệu nào; chỉ chính SHA256SUMS không tự liệt kê (bình thường).
- Duyệt toàn bộ 14 giá trị `measured` bằng `duyet`, `token_nguon`, `phan_giai` của checker. Ngoài finding trên, không thấy con trỏ phân giải nhầm tệp chung tên ở ops/land hoặc gốc. Đã mở nguồn lease: hai đường dẫn rc=0, NGƯỜI_GIỮ 0, lease hết hạn, do-ref 553/553 thiếu 0. Check-run readback có các check bắt buộc success, mốc muộn nhất bắt buộc 05:22:34Z, toàn bộ completed_at trước merge. Đã đối chiếu comment verdict app=claude và events ready_for_review/merged app=null; nguồn events chỉ chứng minh phần events, nguồn comment riêng có sẵn và hỗ trợ phần còn lại, không phát hiện mâu thuẫn thực tế.
- Header tệp đo mới nói “kho tại master 653fef3”: `show -s --format='%H %cI %s' 653fef3` cho commit merge #774 lúc 2026-10-16T21:47:00+07:00 (14:47Z), trước mốc ghi phép đo 17:35:51Z, nên hợp thời gian. Ba lệnh trong transcript không đo HEAD/branch; không thể độc lập chứng nhận checkout lịch sử đúng master 653fef3. Không tính thành P3: kết quả ba lệnh không phụ thuộc checkout, và ba giá trị đã tái đo đúng.

## Ngoài phạm vi

- Không gọi GitHub live, không xác nhận nguồn gốc server của các JSON ngoài bằng chứng được giữ trong Git và checksum. Không đăng verdict, merge, sửa kho hoặc chạy CI/runtime toàn dự án.
- Không suy rằng master hiện tại còn ở 653fef3: đó là mô tả thời điểm đo lịch sử. Bản sao này không có refs/heads/master; không dùng điều đó để kết luận mô tả lịch sử sai.
- Không tính thiếu log đầy đủ đã được hồ sơ khai rõ hoặc hạn chế model identity của lượt review cũ thành finding mới.
