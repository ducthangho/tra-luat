# BỘ CHỌN: re.match ở ĐẦU DÒNG · GRAMMAR: re.fullmatch TRỌN dòng · mọi nhóm bắt là cặp (n, m).
TONG = {
    ".claude/dev/chon_reviewer_test.py":   [(r"nền: ", r"nền: (\d+)/(\d+) đạt")],
    ".claude/dev/gh_readback_test.py":     [(r"gh_readback tests: ", r"gh_readback tests: (\d+)/(\d+) ca QUA \(hong 0\)")],
    ".claude/dev/mcp_gh_test.py":          [(r"CA\s+:", r"CA\s+: (\d+)/(\d+) đạt · 0 đỏ · ĐẠT"),
                                            (r"ĐỘT BIẾN\s+:", r"ĐỘT BIẾN\s+: đã đo (\d+)/(\d+) tập giết · ĐẠT")],
    ".claude/dev/mcp_github_doc_test.py":  [(r"mcp_github_doc tests: ", r"mcp_github_doc tests: (\d+)/(\d+) ca QUA \(hong 0, bo qua 0\)")],
    ".claude/dev/probe_mang_test.py":      [(r"tự đột biến cổng: ", r"tự đột biến cổng: 9/9 chết(?: \(m1\.\.m5 \+ 4 dòng cơ chế\))?"),
                                            (r"named mutant probe_missing_tool_executes_git: ", r"named mutant probe_missing_tool_executes_git: 1/1 chết"),
                                            (r"nền: ", r"nền: 11/11 đạt")],
    ".claude/hooks/pretooluse_guard_test.py":    [(r"TONG: CA ", r"TONG: CA (\d+)/(\d+) dat · DOT BIEN (\d+)/(\d+) bi giet")],
    ".claude/hooks/subagent_ghi_detect_test.py": [(r"TONG: CA ", r"TONG: CA (\d+)/(\d+) dat · DOT BIEN (\d+)/(\d+) bi giet")],
    "ops/nhanh_don_duoc_test.py":          [(r"\d+/\d+\s*$", r"(\d+)/(\d+)")],
}
# Windows — ghép theo THỨ TỰ hai dạng của MOI_WINDOWS[pretooluse]: dòng Windows · dòng Linux đầy đủ.
TONG_WINDOWS = {
    ".claude/hooks/pretooluse_guard_test.py": (
        [(r"TONG: CA ", r"TONG: CA (\d+)/(\d+) dat · DOT BIEN [1-9]\d* muc KHONG DO TREN WINDOWS — do tren ubuntu-latest")],
        [(r"TONG: CA ", r"TONG: CA (\d+)/(\d+) dat · DOT BIEN (\d+)/(\d+) bi giet")],
    ),
}
