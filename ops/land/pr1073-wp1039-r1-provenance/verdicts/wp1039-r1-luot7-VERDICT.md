Verdict: approve
Reviewed commit: 9783b421ecb74636311501e7c0d712e2aa73a5c0
Spec sha256: 67b448acc825fdd29f118c3b9082583773b4ad218a7c83ab4db496daa8f26d81

Không có finding P0/P1/P2/P3 được xác lập trong phạm vi lượt 7. Công thức đổi khoá mới khắc phục lỗi thiếu `--new`: phép thử độc lập xác nhận nhánh cũ trả rc=3, 0 upload; nhánh mới tạo bundle rev=1, mã hoá bằng khoá mới. R1/R2/J1/K2 và hai suite đều đạt theo bảng đo bên dưới. Kết luận dựa trên output mới, không dùng kết quả chạy của các verdict cũ thay phép đo.

Base: `97120d3c76ebb7c3eda4b585ff46f1c51e30c91b`. Mốc lượt 6: `901644d8f7d24562ee666591f3917b094c5f1426`. Tree được review: `17900666c586ce782a42a958f5224de354d57c54`. Áp dụng chỉ thị [prompt.snapshot](run/2bfa8722/prompt.snapshot): class sensitive, ngưỡng 0 P0–P3, trần 8 tệp/+700, quyết định F08/D2 và F13(B) đã nêu trong packet. **Verdict này không cấp quyền merge/land.**

Lệnh đo dùng `PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null`; đã chạy `git config core.abbrev 7` theo chỉ thị. Mọi đường dẫn tương đối trong lệnh lấy `cay-kho/` làm thư mục làm việc, trừ khi ghi khác.

Driver [run_check.py](evidence-luot7/run_check.py), chạy từ thư mục cha bằng `python3 evidence-luot7/run_check.py cloud` / `setup` / `release`, thực thi đúng các lệnh suite/J1 trong bảng; ghi command, rc, stdout, stderr và thời gian. Hai suite dùng fixture sẵn có; fixture riêng [rotation_probe.py](evidence-luot7/rotation_probe.py) gọi hàm sản phẩm và bộ mã hoá thật với hai khoá giả, nguồn cục bộ giả, tải/upload giả và tiến trình con giả.

**Bảng đo**

| Phép đo | Lệnh / bằng chứng | Output | Trạng thái |
|---|---|---|---|
| Head, base, spec | `git rev-parse HEAD HEAD^{tree}`; SHA-256 `../SPEC.md`; [log](evidence-luot7/preflight.json) | Head/spec đúng hai dòng neo trên; tree `17900666c586ce782a42a958f5224de354d57c54`; detached HEAD; status rỗng | PASS |
| Delta lượt 7 / blob | `git diff --name-only 901644d HEAD`; `git rev-parse 901644d:<path> HEAD:<path>`; [log](evidence-luot7/preflight.json) | Chỉ `RELEASE_MANIFEST.json`, `references/RUNBOOK.md`; 6/6 blob mã/test trong write set bằng nhau; diff các path còn lại rỗng | PASS |
| Hai patch đầu vào | So byte `git diff 97120d3c..HEAD` với `../DIFF.patch`, `git diff 901644d..HEAD` với `../DIFF-LUOT7.patch`; [log](evidence-luot7/preflight.json), [diff tự đo](evidence-luot7/actual-DIFF-LUOT7.patch) | `patch_match`: cả hai true | PASS |
| Phụ thuộc luồng đổi khoá | `git rev-parse 901644d:<path> HEAD:<path>` với `scripts/tl_gws.py`, `scripts/tl_core/cli.py`, `scripts/gws_cred_store.py`; [log](evidence-luot7/source-audit.json) | Cả 3 cặp blob bằng nhau | PASS |
| K2 | `git diff --name-only 97120d3c HEAD`; `git diff --numstat 97120d3c HEAD` | Đúng 8 path write set; +700/-7; áp trần 700 theo chỉ thị hiện hành | PASS |
| R1 / R2 | `python3 ../evidence-luot7/audit.py`; [log](evidence-luot7/audit.json) | A0.4e dòng 220–241: 22 dòng kể cả dòng trắng cuối; tiêu đề head/base 1/0; đủ 10 cụm; cả ba regex R2 đều 0 | PASS |
| J1 | `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json`; [log](evidence-luot7/release.json) | rc=0; ok=true; expected_file_count=checked_file_count=195; failed=[], extra_files=[], errors=[] | PASS |
| Manifest chỉ cập nhật nội dung RUNBOOK | So JSON `git show 901644d:RELEASE_MANIFEST.json` với tệp head; [log](evidence-luot7/source-audit.json) | Danh sách 195 path giữ nguyên; phần tử đổi duy nhất `references/RUNBOOK.md`; total_bytes +201; package/content hash đổi tương ứng; J1 xác nhận hash khớp | PASS |
| Suite setup | `python3 ops/codex_cloud_setup_test.py`; [log](evidence-luot7/setup.json) | rc=0; `DOT BIEN: 13/13 bi giet dung ly do`; `13/13` | PASS |
| Fixture đổi khoá | `python3 ../evidence-luot7/rotation_probe.py`; [log](evidence-luot7/rotation.json) | rc=0; thiếu --new + khoá mới: rc=3, upload=0; có --new: rc=0, download=0, upload=1, rev=1; secrets-stage: rc=0, bundle mở bằng khoá mới; hai reader chọn fileId môi trường | PASS |
| Suite cloud | `python3 ops/cloud_agent_creds_test.py`; [log](evidence-luot7/cloud.json) | rc=0; `CA: 26/26 dat`; `DOT BIEN: 49/49 bi giet dung ly do`; `TU KIEM PHAN HANG: DAT (4 dot bien)`; `TONG: DAT`; 219.252 s | PASS |
| Whitespace | `git diff --check 97120d3c HEAD`; [log](evidence-luot7/audit.json) | rc=0; output rỗng | PASS |
| Trạng thái cuối | `python3 ../evidence-luot7/final_audit.py`; [log](evidence-luot7/final-state.json) | rc=0; head/tree/spec không đổi; status gồm untracked/ignored rỗng; diff/index rỗng; 9.054 tệp đã băm không đổi so mốc audit | PASS |

K2, phân rã từ `git diff --numstat 97120d3c HEAD` (rc=0; [output đầy đủ](evidence-luot7/preflight.json)):

| Path | Thêm | Xoá |
|---|---:|---:|
| `.claude/dev/ci_dang_ky_test.py` | 1 | 0 |
| `.claude/hooks/session-start.sh` | 7 | 1 |
| `RELEASE_MANIFEST.json` | 5 | 5 |
| `ops/cloud_agent_creds.py` | 194 | 0 |
| `ops/cloud_agent_creds_test.py` | 431 | 0 |
| `ops/codex_cloud_setup.sh` | 3 | 0 |
| `ops/codex_cloud_setup_test.py` | 36 | 1 |
| `references/RUNBOOK.md` | 23 | 0 |
| **Tổng** | **700** | **7** |

**R1/R2 — đúng mục A0.4e**

`python3 ../evidence-luot7/audit.py` trả rc=0. Script trích từ tiêu đề `**A0.4e` đến trước `**A0.5`, gộp khoảng trắng riêng từng đoạn; không tìm cụm trong toàn RUNBOOK. [Đoạn nguyên văn](evidence-luot7/runbook-section.txt), [kết quả](evidence-luot7/audit.json): 22 dòng kể cả dòng trắng cuối, tiêu đề head/prior/base = 1/1/0. Xoá riêng trạng thái `ĐÃ NẠP` trong bản văn ở bộ nhớ làm thiếu đúng cụm đó (`R1_negative_control_remove_state=true`).

| Cụm R1 | Số lần |
|---|---:|
| `TL_MASTER_KEY` | 3 |
| `agent-creds-exec --gemini` | 1 |
| `agent_creds:` | 2 |
| `ĐÃ NẠP` | 1 |
| `KHÔNG CẤU HÌNH` | 1 |
| `KHÔNG ĐO ĐƯỢC` | 1 |
| `BỎ QUA` | 1 |
| `secrets-keygen` | 1 |
| `agent-creds-set` | 2 |
| `Codex Cloud` | 4 |

R2 trên chính đoạn nguyên văn: `sk-ant-` = 0; `AIza` = 0; `[A-Za-z0-9_-]{40,}` = 0. Không dựng chuỗi nhạy cảm để thử regex.

**ĐỐI CHIẾU LƯỢT TRƯỚC và công thức đổi khoá**

`sed -n '1,7p' ../VERDICT-LUOT6.md` và `sed -n '80,87p' ../VERDICT-LUOT6.md` cho thấy lượt 6 ghi approve, không còn finding mở. Đây chỉ là đối chiếu hồ sơ. Delta/blob và các suite ở bảng trên được đo lại trên head này.

P2 phát sinh sau lượt 6 về công thức thiếu `--new`: **ĐÃ VÁ THẬT trong phạm vi đo**. Vị trí mới `references/RUNBOOK.md:237`–240. Lệnh đọc mã: `nl -ba scripts/tl_gws.py`, đối chiếu các vị trí bên dưới; trích nguồn lưu tại [source-review.txt](evidence-luot7/source-review.txt). Lệnh fixture: `python3 ../evidence-luot7/rotation_probe.py` ⇒ rc=0, `assertions_passed=true`; [output](evidence-luot7/rotation.json).

| Kiểm tra | Vị trí / bằng chứng mã | Output fixture độc lập |
|---|---|---|
| Khoá mới, không `--new` | `tl_gws.py:1182`–1201: chọn fileId cũ, tải và `store.decrypt(old, master)`; lỗi trả 3 trước upload | `new_key_without_new`: rc=3, tải `fixture-agent-old` 1 lần, upload=0, đúng thông báo lỗi giải mã bản cũ |
| Đối chứng khoá cũ còn đúng | Cùng hàm và nguồn fixture, chỉ đổi lại khoá cũ | `old_key_without_new_control`: rc=0, tải=1, upload=1 tại fileId cũ, rev=8 |
| Khoá mới, có `--new` | `tl_gws.py:1183`, 1186, 1204–1213: fid=None, không tải bản cũ, rev khởi tạo 1, upload force_new | `new_key_with_new`: rc=0, tải=0, upload=1, fid đầu vào=null, force_new=true, rev=1; đủ cả ba trường nguồn; khoá mới mở được, khoá cũ không mở được; output nhắc anyone-with-link và fileId mới |
| `secrets-stage` sau đặt khoá mới | `tl_gws.py:932`–990: đọc khoá hiện tại, gom config/GWS/NLM cục bộ rồi encrypt; không giải mã bundle cũ; `_secrets_upload` tại dòng 662 giữ fileId khi có sẵn | `secrets_stage_with_new_key`: rc=0, tải=0, upload=1 tới `fixture-secrets`; dữ liệu config/GWS/NLM khớp; canary giả được gọi 1 lần; khoá mới mở được, khoá cũ không mở được |
| `_bootstrap_agent_creds` ưu tiên env | `tl_gws.py:1220`: `os.environ.get("TL_AGENT_CREDS_FILEID") or AGENT_CREDS_FILEID` | Hai bộ trạng thái cục bộ giả lập hai nền đều chỉ tải `fixture-agent-new`; trạng thái `ĐÃ NẠP`; auth.json khớp nguồn và mode 0600 |
| `cmd_agent_creds_exec` ưu tiên env | `tl_gws.py:1272`: cùng thứ tự ưu tiên | Hai bộ trạng thái giả đều rc=0, chỉ tải fileId mới, gọi con giả 1 lần với cả hai giá trị từ bundle; giá trị môi trường cha cố ý khác và giữ nguyên |
| Thiếu cập nhật fileId — đối chứng âm | Hai reader giữ hằng cũ khi env vắng | Bootstrap: `KHÔNG ĐO ĐƯỢC`, tải fileId cũ; exec: rc=4, tải fileId cũ, gọi con=0 |

Đối chiếu cú pháp bằng `sed -n '141,151p' scripts/tl_core/cli.py`: `--new` là `store_true`; `--claude-token-env` và `--antigravity-key-env` đều có `nargs="?"`, mặc định lần lượt là `CLAUDE_CODE_OAUTH_TOKEN` và `GEMINI_API_KEY`. Vì vậy cách viết không kèm tên biến trong RUNBOOK hợp lệ.

Công thức mới đúng và đủ cho chuyển đổi bundle agent ở hai nền theo đường cấu hình mặc định được mô tả: đặt `TL_MASTER_KEY` mới trong tiến trình stage; mã hoá lại `tl_secrets.enc`; tạo bundle agent mới; bật quyền đọc công khai của file mới; đặt **cùng cặp fileId mới/khoá mới ở cả hai nền**. Đối chứng âm ở trên xác nhận cập nhật riêng khoá là chưa đủ. `secrets-stage` giữ fileId secrets đang dùng theo mặc định, còn fileId agent phải đổi do `--new`; không cần sửa hằng agent để reader nhận env override. Căn cứ: RUNBOOK dòng 237–240, mã `_secrets_stage_body`/`_secrets_upload`/hai reader và output fixture trong bảng.

Điều kiện đầu vào của bước stage vẫn là máy có dữ liệu nguồn hợp lệ: `secrets-stage` cần config/token cục bộ, GWS khi đóng gói GWS và jar/canary NLM nếu không chủ ý dùng `--no-nlm` (`tl_gws.py:935`–979); `agent-creds-set --new` cần đủ auth.json và hai biến nguồn (`tl_gws.py:1159`–1178). Các hàm này không tự chuyển credential còn thiếu từ bundle cũ. Phép đọc `sed -n '737,782p' scripts/tl_gws.py` cho thấy refresh NLM dùng hồ sơ cục bộ, không cần giải mã bundle bằng khoá cũ. Đây là các điều kiện nguồn của lệnh hiện có; không tìm thấy bước chuyển khoá còn thiếu trong công thức đã sửa trên đường mặc định.

**Bảng finding còn mở**

| Mức | Slug / vị trí | Lệnh tái hiện — output — hướng vá |
|---|---|---|
| Không có | Không có finding P0/P1/P2/P3 được xác lập | P2 công thức cũ đã được kiểm bằng cặp đối chứng và đóng theo bảng trên; không đề nghị bản vá |

Số finding yêu cầu sửa: **P0=0, P1=0, P2=0, P3=0**. Không có mục `- [P0..P3]` vì không có finding yêu cầu sửa.

**Giới hạn phép đo**

- LIVE trên Claude Code web/Codex Cloud, quyền anyone-with-link thực tế, tải/upload Drive thật, credential thật và `agy` thật: **KHÔNG ĐO ĐƯỢC trong lượt này**. Các nhãn hai nền trong fixture chỉ là hai bộ trạng thái độc lập dùng chung hàm đọc; không chứng minh UI dịch vụ đã nhận biến hoặc secret còn tồn tại khi agent chạy. Canary NLM và tiến trình con đều là giả.
- M1/M2, CI từ xa, full selftest và các cổng ngoài danh sách lượt 7: **KHÔNG ĐO ĐƯỢC / không chạy lại trong lượt này**; không lấy kết quả lượt 6 làm PASS mới. Approve ở đây là kết luận review phạm vi yêu cầu, không thay các điều kiện nghiệm thu LIVE hay quyền land.
- `python3 ../evidence-luot7/final_audit.py` chứng minh trạng thái checkout tại mốc kiểm cuối sạch, head/tree/spec đúng và byte không đổi so mốc audit. Mốc đầu `git status --porcelain=v1` cũng rỗng ([preflight](evidence-luot7/preflight.json)); các snapshot không phải giám sát mọi syscall hay toàn bộ lịch sử ghi rồi hoàn nguyên.
