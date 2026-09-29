# Cong cu dung sandbox review #674 (do phien Sonnet ban giao cho phien Opus)

Chep nguyen tu scratchpad phien `session_01BxzKQaSmg6qVeSaQWH4dr5`. **Duong dan ghi cung trong `dung.py`/`luu.py` (bien `S`, `REPO`)
tro vao scratchpad/kho cua phien do — doi cho khop phien nhan.** `dung.py ROUND SHA [VERDICT_TRUOC]` dung `rvROUND/{cay,kho.git,goi,out,tmp}` + PROMPT.md
(tu `PROMPT.tmpl.md`, thay {{...}}); `luu.py ROUND RUN_SHORT_ID REVIEWED_SHA` luu verdict + bien nhan co bam vao nhanh ops nay va day len.
Lenh phong reviewer (luot 1-4): `launcher.py run --workspace rvN/cay --expected-repo ducthangho/tra-luat --expected-root-commit 394e93468fc8d84ec20938e6df8fb7ab72b2cc37
--expected-head <sha> --require-clean --prompt-file rvN/PROMPT.md --expected-prompt-sha256 <sha> --deadline-utc <+90 phut> --run-root <ngoai kho> --name rvN
-- <codex da resolve> exec -m gpt-6-astra -c model_reasoning_effort="high" --strict-config -s workspace-write --skip-git-repo-check -C rvN "Doc tep {PROMPT_FILE} va thuc hien dung theo do."`
(TMPDIR=rvN/tmp). Luot bi cat / rong KHONG phai verdict; sach chi khi co dong `Reviewed commit:` dung head.
