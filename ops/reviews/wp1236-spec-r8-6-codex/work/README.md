# Phản chứng gốc của generation 1 (đợt A1, PR #1260)

Chép nguyên byte từ scratchpad của phiên executor A1 (`session_015GtxrYvvXqhFG2QYbhCEv2`), nhận 06-11-2026 18:39Z
dưới dạng tar.gz + base64 (sha256 tgz `f1063828c49f5d3cf7e6d79c6ee4dd6990eafc93f875660e15aa825a0d9c1ac0`); 7/7 sha256 dưới khớp
bản người gửi khai. Chúng là hiện vật review (của reviewer Codex lượt 8, 9 và executor), KHÔNG phải mã; chúng nạp module/test của
generation 1 từ `../repo` nên không chạy được nguyên trạng trong kho này.

```
1c4c1b122829fe2ecb1ca0000417869742435bd7e47557eadc23d5a56791c09c  rv-a1-8/work/probes.py
2a8bfc13e99f8efc1ec2ab99be8b1658ac4e5e3b9f4d9498e6d7dac732f625ce  rv-a1-9/work/extra_shell_probes.py
45fac9b31718a9618fc1272b794e2907701ba30704e9accbe0571810f8f6a546  rv-a1-9/work/extra-shell-probes.json
68c825e097101222ac26068bb315f085c78c2968de922f328d92c8e57b696655  rv-a1-9/work/mutation-probes.json
692b9b48442089751eb2e0671200ca0af46cf98b48334b1cd367c2e4f3000248  rv-a1-9/work/mutant-witnesses.json
274ca0c5b0c2757c0651262a8754e3ab61d9198a1efdf4840b5f966f56435d66  bot2/rep.py
63f18c93765c73dd62d7ce268cf3f46b660e6927cb13f9c0f153f232db167974  k3chk/rep.py
```

`../g1_qua_grammar.py` trích danh sách `cases` của hai script (26 + 26 biến thể) bằng `ast`, không chạy chúng, rồi phân loại bằng
`../gram.py`: 52/52 bị K7-S từ chối (kết quả `../g1_probes_qua_grammar.json`).
