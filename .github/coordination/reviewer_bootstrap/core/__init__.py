"""Reviewer bootstrap core (wp77 / RA-01).

Lõi controller KHÔNG đặc quyền. Năm thành phần:

  operations  - tập operation ĐÓNG + schema tham số máy đọc được
  fake_github - store giả, chạy test không chạm mạng, mô phỏng cả đường LỖI
  ledger      - idempotence theo reconcile_key
  artifacts   - manifest + locator bền (ràng buộc trong run_root) + SHA-256 từng file
  guards      - tripwire env/subprocess/mạng, mỗi cái khai phạm vi phủ BẰNG MÁY

Ranh giới của chính packet này (acceptance §3 của #77):
  ZERO credential - không đọc GH_TOKEN/GITHUB_TOKEN/AWS_*, và không trao chúng cho tiến trình con
  ZERO model call - không gọi provider nào
  KHÔNG chạm GitHub thật trong bất kỳ test nào

Sandbox runner/oracle thuộc RA-02; credential gateway thuộc RA-03. Không nằm ở đây.
"""

__all__ = ["operations", "fake_github", "ledger", "artifacts", "guards"]
