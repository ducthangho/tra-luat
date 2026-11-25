import sys, pathlib, re
k = pathlib.Path(sys.argv[1]); cay = pathlib.Path(sys.argv[2])
def doc(t): return (k / t).read_text(encoding="utf-8")
p = cay / "docs/PROTOCOL_DA_PHIEN.md"; s = p.read_text(encoding="utf-8")
def mot(s, neo):
    assert s.count(neo) == 1, (neo[:50], s.count(neo)); return s
neo1 = "    workflow trigger và prompt chỉ là worker/client có thể thay thế, không tự cấp quyền hoặc tự nối chuỗi vai trò.\n"
s = mot(s, neo1).replace(neo1, neo1 + doc("p1-moi"))
neo2 = "## 2. Thành phần và quyền\n"; s = mot(s, neo2).replace(neo2, doc("p2-moi") + "\n" + neo2)
neo3 = "### 8.3 Lịch sử lớp finding và giới hạn nghiệm thu\n\n"; s = mot(s, neo3).replace(neo3, neo3 + doc("p3-moi") + "\n")
s = mot(s, doc("p4-cu")).replace(doc("p4-cu"), doc("p4-moi"))
assert sum(1 for d in s.split("\n") if d + "\n" == doc("p5-cu")) == 1
s = s.replace("\n" + doc("p5-cu"), "\n" + doc("p5-moi"))
m = re.search(r"(?m)^\| `ADR-0067` \|[^\n]*\n", s); assert len(re.findall(r"(?m)^\| `ADR-0067` \|", s)) == 1
s = s[:m.end()] + doc("p6-moi") + s[m.end():]
p.write_text(s, encoding="utf-8", newline="\n")
a = doc("adr").replace("{{TRANG_THAI}}", "- **Trạng thái:** Proposed (cây thử, chưa duyệt)")
for i in range(1, 7): a = a.replace("{{N%d}}" % i, "0")
(cay / "docs/adr/0068-bat-bien-protocol-va-review-theo-lop.md").write_text(a, encoding="utf-8", newline="\n")
print("ap xong")
