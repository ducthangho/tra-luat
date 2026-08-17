# ADR-0040 — Tách Model Reviewer Identity khỏi GitHub Submitter Identity

- **Trạng thái:** Accepted (2026-08-17, phiên `grill-with-docs`; chủ kho phê duyệt)

Review evidence ghi riêng danh tính provider/model/session đã tạo verdict và actor đã vận chuyển nó lên GitHub.
Trong M1–M2, Codex verdict được `launcher.py` neo exact SHA và hash output có thể đạt `cross_approved`, nhưng tệp,
receipt hay comment do tài khoản tác giả đăng không trở thành required check hoặc merge authorization; Packet
`sensitive` cần human Land Approver readback trước khi land. Chỉ M3 mới được cân nhắc Dedicated App/Check Run làm
publisher authority sau canary và human activation. Sự tách này giữ được review khác nền hiện có mà không tuyên bố
sai rằng tài khoản vận chuyển chứng minh reviewer độc lập hay có quyền chặn GitHub.

M1 không tạo identity record song song: nó nâng `review_delivery_receipt` hiện có lên v2, giữ t26/t27 và
mục lục. Receipt v2 bắt buộc hai identity, exact head, verdict hash và anchor strength; Packet state chỉ
tham chiếu receipt ID/hash đã validate. Mỏ neo có thể là canonical ancestry, protected evidence ref hoặc check
object; không bắt tag tuyệt đối và receipt trên PR branch vẫn chỉ là mirror.

Mốc cutover giữ nguyên 11 receipt v1 là historical/read-only, không bồi identity bằng suy đoán và không cho
chúng thỏa identity required check mới. Legacy exemption neo vào allowlist đóng băng 11 filename+hash;
tệp mới không thể tự hạ trust bằng cách ghi `schema_version: 1`. Cách này giữ lịch sử nguyên vẹn
mà không đổi compatibility thành trust escalation.
