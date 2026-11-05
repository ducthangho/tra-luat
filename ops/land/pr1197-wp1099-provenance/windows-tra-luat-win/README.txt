Log tho chay Windows tap trung wp1099_nlm_nap_lai tren tra-luat-win (C:\work\diag-9944246.log, 349 byte, mtime 2026-11-05T13:37:20.88Z).
Nguon: phien dieu phoi session_015GtxrYPjZCTZeRiazdssgq doc bang [Convert]::ToBase64String(ReadAllBytes) va gui qua send_message 2026-11-05T16:07Z.
Luu dang base64 (diag-9944246.log.b64) vi tep goc tron CRLF/LF, ma .gitattributes `* text=auto eol=lf` se chuan hoa CRLF
khi vao index => blob khac byte goc. Kiem: base64 -d diag-9944246.log.b64 | sha256sum
  => 1aaccf5cd5878019c517329ceddebf2ade552b8f701b71bbfeed9575e0cb845e (do lai trong phien ghi so, khop so certutil cua dieu phoi).
Chu tieng Viet trong tep la mojibake CO TU LUC GHI (stdout python qua console cp437 roi Tee luu UTF-8), khong do duong truyen.
Phan ASCII doc nguyen: HEAD 99442469f331e4808ee9de43e2beb75416e51a21 · CA A: 12/12 · D: 3/3 · DOT BIEN: 29/30 · doc_dau_chan · KQ True · SECONDS 58.
