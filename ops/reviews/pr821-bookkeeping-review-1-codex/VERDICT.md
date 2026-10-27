Reviewed commit: 8e150cf0d9f046a761c49448c8173ad501f53a1c
Verdict: request_changes P1=0 P2=0 P3=2

Reviewer: Codex/OpenAI; phiên API có công cụ shell cục bộ, transport machine. Không đo được model ID/effort phục vụ từng request. Review độc lập, KHO `/home/user/rv773` chỉ đọc; không gọi mạng, không fetch, không sửa ref/cấu hình. `git status --porcelain` cuối lượt rỗng. Tree/head được đối chiếu bằng Git. Phạm vi và authority theo yêu cầu cross-review PR #821 của chủ kho.

## Findings

### F01 — P3 — Con trỏ cũ tới readback PR chỉ chứng minh một phần lời khai

Vị trí: `ops/land/pr779-wp775-land-evidence.yaml:92`, cùng lỗi ở dòng 110, 116, 118–119.

Bốn lời khai `measured` này qua L1 nhờ `readback-pr-779.json`, nhưng tệp ấy không chứa cha/tree của merge commit, cũng không chứa merge event (actor, giờ 16:55:51Z, app null). Đặc biệt `khong_xung_dot` qua nhờ token nằm trong vế `not_measured`; dữ liệu cha/tree trong vế measured hoàn toàn không được tệp đó chứng minh. Đây không phải số liệu sai: tôi xác minh chúng đúng bằng Git và `readback-events-779.json`. Lỗi là hồ sơ chưa tự trỏ đúng nguồn cho toàn bộ câu khai, thuộc phạm vi mở rộng được yêu cầu ở mục 4; đã có trên base.

Tái hiện (Python3.13, rc=0):

```sh
python3.13 -B - <<'PY'
import json
p='/home/user/rv773/ops/land/pr779-wp775-provenance/'
x=json.load(open(p+'readback-pr-779.json'))
print([k for k in ['parents','tree','actor','performed_via_github_app'] if k not in x])
print(list(x['head']))
for e in json.load(open(p+'readback-events-779.json')):
    if e.get('event')=='merged':
        print(e['actor']['login'], e['created_at'], e['performed_via_github_app'])
PY
git -C /home/user/rv773 show -s --format='%H %P %T' d8b15cb
git -C /home/user/rv773 rev-parse 'f9d84d7^{tree}'
```

Đầu ra:

```text
['parents', 'tree', 'actor', 'performed_via_github_app']
['label', 'ref', 'sha', 'user', 'repo']
ducthangho 2026-10-17T16:55:51Z None
d8b15cb0730c85e7019aee627c3bfa645a6d3eaf 73bf92c0db05fead9d7e98c7b4f3643bd72bfcd8 f9d84d70fb46540bbecfae963c9afb4a2b48984d 6474598db320df3de03d0251ba9305dde1875b3f
4e712f37bf014e18e87df07d0f94d0ba353fb3e7
```

Sửa: lưu transcript Git cha/tree và thêm con trỏ ấy ngay trong ba lời khai về cha/tree; thêm `readback-events-779.json` vào lời khai về event. Cập nhật SHA256SUMS khi thêm transcript. Kiểm khóa: mở từng nguồn sau phân giải và đối chiếu từng vế, chạy lại L1 và checksum. Rủi ro sửa: đừng suy từ hai cha thành không conflict hoặc từ app null thành người bấm tay; giữ nguyên giới hạn đang khai.

### F02 — P3 — Tiêu đề transcript khai trạng thái checkout chưa được phép đo ghi lại

Vị trí: `ops/land/pr779-wp775-provenance/do-lai-nguon-20261018/kiem-gate-f9d84d7.txt:1`.

Tiêu đề ghi `kho tai master 924527c`, nhưng transcript chỉ chạy `kiem-gate` đọc JSON; không lệnh nào đo HEAD, nhánh checkout hay phiên bản script. `--head f9d84d7` là SHA của check cần xét, không phải phép đo checkout. Tôi xác minh được `origin/master` hiện ở 924527c, nhưng điều đó không chứng minh checkout của phiên lịch sử. Đây là thiếu bằng chứng cho ngữ cảnh được khai, không phải kết luận rằng executor đã chạy sai cây.

Tái hiện:

```sh
cat /home/user/rv773/ops/land/pr779-wp775-provenance/do-lai-nguon-20261018/kiem-gate-f9d84d7.txt
git -C /home/user/rv773 rev-parse HEAD origin/master
```

Đầu ra đo: transcript 9 dòng chỉ có hai lệnh `python ... kiem-gate`; không có `rev-parse`, `symbolic-ref` hay hash script. Kho review hiện có HEAD `8e150cf0d9f046a761c49448c8173ad501f53a1c`, origin/master `924527c2d67ae36bb20a80147e687a823564ad90`. Chạy lại hai gate trên cây review vẫn rc=0, nên output gate không tự xác nhận tiêu đề.

Sửa: bỏ mệnh đề checkout chưa đo, hoặc ghi nó là lời khai; nếu cần provenance phiên bản, đo lại trên cây tạm đúng 924527c, ghi OID/tree và hash script cùng lệnh đầy đủ. Không bổ sung ngược một phép đo hiện tại như thể là phép đo lịch sử. Kiểm khóa: mọi khẳng định checkout/phiên bản trong transcript phải có lệnh đo tương ứng; cập nhật checksum. Rủi ro sửa: tránh làm mất phân biệt offline readback với CI chạy mới.

## Đã đo

- Diff đúng 5 tệp, sáu chuỗi YAML được sửa; đọc commit message. Head đúng OID yêu cầu, base đầy đủ `924527c2d67ae36bb20a80147e687a823564ad90`.
- Trích bộ kiểm từ `e0e0eac` ra `/tmp/len.py`, chạy `cd /home/user/rv773 && python3.13 -B /tmp/len.py --root /home/user/rv773`: rc=0, `2 ĐẠT · 28/28 miễn trừ · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC`, `TỔNG: ĐẠT`. Log: [head-gate.txt](head-gate.txt).
- Base dựng bằng `git archive 924527c | tar -x -C /tmp/rv821-base`: bộ kiểm rc=1, đúng sáu L1 ở post_merge_checks[0/2/3], spec.nguon, merge_3, review.codex_connector. Log: [base-gate.txt](base-gate.txt).
- `sha256sum -c SHA256SUMS`: rc=0, 43/43 OK. So tập đường dẫn chuẩn hóa `./`: 43 tệp ngoài SHA256SUMS = 43 dòng, thiếu=0, thừa=0, trùng=0.
- Chạy lại `merge-base --is-ancestor d8b15cb d347d42` rc=0; `log -1 --format=%P d347d42` cho cha thứ nhất d8b15cb, cha thứ hai 76014ce0e76df70d8d3655b8f130747ae4d2cc14. Transcript cha con đúng.
- Spec ref `219dcdaa9d164b8cf7dabb4c126bbfe0e65dfdb7`, blob `898369502c3ad4e4001e9f25692af61d2bf80102`, SHA256 `4b7530c265dddefbebd06ea209d7c0594210f57b391e0d0d353931171fd2b6d8` đều khớp. `cat-file -e origin/master:ops/specs/wp775.md` rc=128, đúng lỗi path không tồn tại. Transcript spec đúng trong giới hạn path ở tip master, không chứng minh lịch sử chưa từng có spec.
- Đọc `kiem-gate --help`; chạy lại 14 tên chính xác (gồm hậu tố ubuntu/matrix) trên suite 105821166384 và `thu-hoi` trên suite 105821159612: cả hai rc=0, từng check ID khớp transcript. JSON có 16 check run; không che một job bắt buộc đỏ. Mười lăm tên được kiểm bằng hai lần chạy, không có một lần chạy 15 tên chung suite. Parenthetical mới nói rõ 14+1 và offline, phù hợp mô tả sẵn ở pre_merge_checks; không coi đây là đổi nghĩa hay che gate. Script tái hiện: [measure821.py](measure821.py), đầu ra [measured821.txt](measured821.txt). Dòng lệnh 14 tên trong transcript là ký hiệu rút gọn, cần khai triển khi chạy.

Đã dùng `duyet`/`token_nguon`/`phan_giai` của chính bộ kiểm để duyệt đủ 13 chuỗi bắt đầu measured. Mọi token phân giải được đều nằm trong provenance tương ứng; không có nguồn qua chỉ nhờ trùng tên tại ops/land hoặc gốc kho. `ci.yml` và `ops/specs/wp775.md` không phân giải, nhưng đã có nguồn phù hợp bổ sung. Chi tiết [token-audit.txt](token-audit.txt).

| Lời khai | Đối chiếu nội dung |
|---|---|
| post_merge_checks[0] | run 39051543180 attempt 1 cancelled, updated 2026-10-17T17:27:24Z; master push d347d42 created 17:27:23Z khớp; không suy nguyên nhân/actor |
| post_merge_checks[2] | attempt 2 success đúng d8b15cb; 14/14 job success; run_started_at 01:23:44Z, updated_at 01:52:05Z; thread 4305258340 có trong readback-review-comments-811.json |
| post_merge_checks[3] | cha trực tiếp đúng; run phụ success đúng d347d42, 14 job success, updated_at 17:59:39Z |
| bookkeeping[0] | issue 775 closed/completed, closed_at 17:29:48Z, closed_by ducthangho; comment 6237647158 đúng |
| bookkeeping[1] | mở đủ JSON 804–810: cả bảy open, tiêu đề lần lượt (1/7) đến (7/7) |
| spec.nguon | ref/blob/hash/path master khớp phép đo trên |
| trang_thai_packet.merged_nguon | REST merged/time/account/SHA khớp; thiếu nguồn cha: F01 |
| uy_quyen_land.dang | REST account/time khớp; event đúng nhưng nằm tệp khác: F01 |
| uy_quyen_land.head_khong_doi | head.sha khớp; cha thứ hai đúng nhưng thiếu nguồn Git: F01 |
| uy_quyen_land.khong_xung_dot | cha/tree đúng qua Git; token REST chỉ chứng minh null/unknown: F01 |
| merge_1 | VERDICT neo full f9d84d7, approve P1=P2=P3=0, hash a1957436163a0d921b5c29523bd278c82a570307279e0c23e4bf1cf15b62234f khớp |
| merge_3 | run 39047604566 attempt 2 success đúng f9d84d7; 14+1 gate rc=0 |
| review.codex_connector | receipt neo f9d84d70fb nói không major issue; state full SHA cùng head, completed, hai cờ findings=true; giới hạn không suy sạch được giữ |

Ngoài 13 chuỗi đó, cũng đọc hai trường lease chứa nhãn measured giữa chuỗi: chúng trỏ tới đúng hai thư mục ai-dang-giu; output có rc=11 và người giữ tương ứng. Không nhận timestamp/fetch của bản cũ là đã đo; hồ sơ tự khai giới hạn ấy. Sáu sửa đổi không làm sai số liệu hoặc thay đổi nghĩa nghiệp vụ; bổ sung 14+1 làm rõ phạm vi phép đo.

## Ngoài phạm vi

Không chạy lại CI thực, không chứng nhận actor/người bấm merge hay model lịch sử, không tái review runtime wp775 hoặc bảy nợ 804–810; không quyết định thay chủ kho về landed/merge_4. Không đánh lỗi bộ kiểm vì L1 chỉ kiểm sự tồn tại — giới hạn này được bộ kiểm khai rõ. Hai finding là thiếu provenance, không phải phát hiện dữ liệu Git/REST sai. Kết quả request_changes theo ngưỡng phải hết cả P3 của chủ kho.
