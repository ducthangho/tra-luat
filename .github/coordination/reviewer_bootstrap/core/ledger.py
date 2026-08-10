"""Idempotence theo reconcile_key (acceptance §3, mục "Idempotence" của #77).

Bất biến:
  - Cùng `reconcile_key` gọi lại KHÔNG tạo bản ghi thứ hai.
  - KHÔNG phụ thuộc thời gian hay thứ tự: đảo thứ tự hai lời gọi khác key cho cùng trạng thái cuối.

Vì sao ledger ghi ra ĐĨA chứ không giữ trong RAM: trạng thái phải sống lâu hơn tiến trình sinh ra
nó - cùng lý do với artifact retention ở artifacts.py. Một ledger chỉ nằm trong RAM không chứng
minh được idempotence giữa hai lượt chạy.

Ghi chú tất định: bản ghi KHÔNG mang timestamp. Thời gian là thứ duy nhất chắc chắn khác nhau
giữa hai lượt chạy, nên đưa nó vào trạng thái là tự tay phá tính so sánh được của state_hash.
"""

import hashlib
import json
import os


class Ledger:
    """Sổ append-only khử trùng lặp theo reconcile_key, bền qua ranh giới tiến trình."""

    def __init__(self, path):
        self.path = str(path)
        self._records = {}
        if os.path.exists(self.path):
            with open(self.path, "r", encoding="utf-8") as fh:
                self._records = json.load(fh)

    def _flush(self):
        directory = os.path.dirname(os.path.abspath(self.path))
        if directory:
            os.makedirs(directory, exist_ok=True)
        # Ghi qua tệp tạm rồi rename: một lượt chạy bị giết giữa chừng không để lại ledger rách.
        tmp = self.path + ".tmp"
        with open(tmp, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(self._records, fh, ensure_ascii=False, indent=2, sort_keys=True)
            fh.write("\n")
        os.replace(tmp, self.path)

    def record(self, reconcile_key, payload):
        """Ghi payload dưới reconcile_key.

        Trả (created, record). `created=False` nghĩa là key đã tồn tại và KHÔNG có bản ghi thứ hai
        nào được tạo; bản ghi đang có được trả nguyên trạng, không bị ghi đè.
        """
        if not isinstance(reconcile_key, str) or not reconcile_key:
            raise ValueError("reconcile_key must be a non-empty string")
        if reconcile_key in self._records:
            return False, self._records[reconcile_key]
        self._records[reconcile_key] = payload
        self._flush()
        return True, payload

    def __len__(self):
        return len(self._records)

    def keys(self):
        return sorted(self._records)

    def get(self, reconcile_key):
        return self._records.get(reconcile_key)

    def state_hash(self):
        """Hash tất định của trạng thái cuối, độc lập với thứ tự chèn.

        `sort_keys=True` là thứ làm cho "đảo thứ tự hai lời gọi cho cùng trạng thái cuối" trở thành
        mệnh đề kiểm được bằng một phép so sánh chuỗi, thay vì so từng trường bằng mắt.
        """
        blob = json.dumps(self._records, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(blob.encode("utf-8")).hexdigest()
