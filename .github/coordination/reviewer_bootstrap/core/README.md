# Reviewer bootstrap — core (wp77 / RA-01)

Lõi controller **không đặc quyền** cho Mission RA (#76). Packet này dựng đúng bốn thứ và **không
hơn**: tập operation đóng, fake GitHub store, idempotence theo `reconcile_key`, và artifact
manifest có locator bền.

Sandbox runner + oracle thuộc **RA-02**. Credential gateway thuộc **RA-03**. Launcher/watchdog
thuộc **RA-04**. Canary thuộc **RA-05**. Không thứ nào trong số đó nằm ở đây.

## Chạy

```bash
python3 .github/coordination/reviewer_bootstrap/core/controller.py selftest   # suite phản chứng
python3 .github/coordination/reviewer_bootstrap/core/controller.py schema     # schema operation (JSON)
python3 .github/coordination/reviewer_bootstrap/core/controller.py produce --out DIR --run-id ID
python3 .github/coordination/reviewer_bootstrap/core/controller.py verify --root DIR
```

Chỉ dùng thư viện chuẩn Python. Không tham số nào nhận token; không lệnh nào mở kết nối mạng.

Mã trả về: `0` ok · `2` bị TỪ CHỐI (op lạ / tham số sai / lỗi store) · `3` verify ĐỎ · `64` sai cú pháp.

## Tập operation ĐÓNG

`read_issue` · `read_comment` · `read_pr` · `read_ci_run` · `read_diff` · `run_test` ·
`post_heartbeat` · `post_verdict`

Tập này là bảng tĩnh trong `operations.py`. **Không có đường đăng ký động** — đăng ký động chính là
thứ biến "đóng" thành lời văn. Mỗi op có schema tham số máy đọc được; thiếu, thừa, sai kiểu hoặc
sai `enum` đều bị từ chối **trước khi** chạm handler.

`run_test` chỉ được **khai báo** ở đây; nó trả marker `executed_here: false` thay vì giả vờ đã
chạy. Một kết quả test bịa còn tệ hơn không có kết quả — đúng lớp lỗi "in `168/168` mà chẳng chạy
gì" đã đo trên #54.

## Acceptance §3 của #77 → phản chứng chạy được

Mỗi dòng dưới đây là một test trong `selftest.py`, không phải một lời khai.

| acceptance | phản chứng |
|---|---|
| tập op đóng, từ chối đích danh | `ra01_operation_set_is_closed_and_declared` · `ra01_unknown_operation_rejected_by_exact_name` · `ra01_unknown_operation_cli_rc_nonzero_and_names_op` |
| schema tham số, thiếu/thừa bị chặn trước khi chạy | `ra01_missing_parameter_rejected_by_name` · `ra01_extra_parameter_rejected_by_name` · `ra01_wrong_type_and_enum_rejected` · `ra01_validation_happens_before_execution` |
| suite chạy không chạm mạng | `ra01_full_exercise_runs_under_network_guard` + chạy toàn suite dưới `unshare -n` |
| lệnh cần mạng ĐỎ đích danh, không treo | `ra01_network_guard_raises_named_error_not_hang` |
| mô phỏng đường lỗi 403/404/409/rate-limit | `ra01_fake_store_simulates_403_404_409_and_rate_limit` · `ra01_natural_404_for_absent_object` |
| cùng key không tạo bản ghi thứ hai; đổi key thành 2 | `ra01_same_reconcile_key_twice_yields_one_record` · `ra01_different_reconcile_key_yields_two_records` |
| không phụ thuộc thứ tự | `ra01_idempotence_is_order_independent` |
| manifest + locator + SHA-256 từng file, đủ 5 hạng mục | `ra01_manifest_covers_all_required_categories` |
| manifest tự kiểm được | `ra01_manifest_is_self_describing_with_sidecar_hash` · `ra01_verify_goes_red_on_tampered_manifest` |
| xoá artifact ⇒ ĐỎ, gọi đúng tên | `ra01_verify_goes_red_and_names_the_deleted_artifact` |
| locator còn truy xuất sau khi tiến trình sinh ra đã chết | `ra01_locator_resolves_after_producing_process_exits` · `ra01_locator_survives_directory_relocation` |
| ZERO credential | `ra01_core_reads_zero_credentials_with_fakes_injected` · `ra01_no_artifact_contains_injected_credential_value` · `ra01_operations_expose_no_credential_parameter` |
| ZERO model call / không đường mạng | `ra01_core_modules_import_no_network_or_provider_library` |

## Hai đối chứng dương — vì sao chúng bắt buộc

Một detector chết cũng báo "sạch". Hai test dưới đây tồn tại để chứng minh tripwire **còn sống**;
bỏ chúng đi thì mọi kết quả "không phát hiện gì" ở trên mất hết ý nghĩa:

- `ra01_env_tripwire_positive_control` — đọc cố ý `GH_TOKEN` và `AWS_SECRET_ACCESS_KEY`, đòi
  recorder PHẢI bắt được.
- `ra01_import_scanner_has_teeth` — bộ quét import phải bắt được `import requests` trong fixture
  bẩn, đồng thời **không** báo dương tính giả trên văn xuôi docstring.

Đối chứng thứ hai ra đời từ một lỗi thật trong chính phiên này: bản đầu dùng regex và đã báo dương
tính giả vì một dòng docstring ngắt đúng chỗ thành `    import socket/http/urllib`. Nay dùng `ast`,
nên phép kiểm nói đúng thứ nó tuyên bố kiểm.

## Retention — điều gì được tính và điều gì không

`artifacts.py` ghi manifest với **locator tương đối** + SHA-256 cho từng file, đủ năm hạng mục
(`source`, `corpus`, `per_case_matrix`, `runner_env_digest`, `cleanup_record`). Hash của chính
manifest nằm ở sidecar `manifest.sha256` — manifest tự chứa hash của mình là bài toán con gà quả
trứng, sidecar là cách giải đúng của mệnh đề *"hoặc có hash riêng ghi ở nơi khác"*.

`verify()` chỉ cần `run_root`. Không cần tiến trình sinh ra artifact còn sống, không cần trạng thái
nào trong RAM. Đó là lý do "comment summary" và "bundle gửi ngoài luồng" **không** phải retention:
chúng không sống sót qua phép thử `ra01_locator_resolves_after_producing_process_exits`, trong đó
tiến trình sinh artifact đã kết thúc trước khi verify bắt đầu.

## Idempotence — khử trùng lặp KHÔNG phải nuốt dữ liệu

Cùng `reconcile_key` + cùng nội dung là replay idempotent (`created: false`, vẫn đúng một bản ghi).
Cùng `reconcile_key` + nội dung **khác** là **409 CONFLICT**, không phải im lặng bỏ qua. Phân biệt
hai ca đó là ranh giới giữa khử trùng lặp và mất dữ liệu.

Bản ghi **không** mang timestamp: thời gian là thứ chắc chắn khác nhau giữa hai lượt chạy, nên đưa
nó vào trạng thái là tự tay phá `state_hash` — mà `state_hash` chính là cách "đảo thứ tự cho cùng
trạng thái cuối" trở thành mệnh đề kiểm được bằng một phép so chuỗi.

## Ngoài phạm vi có chủ đích

`write_set_hash` canonical (§5 protocol) **không** được implement ở đây. Lease của wp77 đo được
rằng wp60 và wp68 dùng **hai** cách tuần tự hoá khác nhau, nên kho chưa có hàm canonical duy nhất.
Việc đó nằm ngoài acceptance §3 đã đóng băng của #77 và được ghi thành **successor** trong handoff
§7, để Reconciler mint Packet mới — không tự mở rộng write set.
