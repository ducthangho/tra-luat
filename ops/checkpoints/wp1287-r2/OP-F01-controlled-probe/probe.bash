TL_PW_SESSION='controlled-fixture'
chay_ghi() { case "$1" in 08-close) return 17;;09-delete-data) return 18;;10-verify) return 19;;*) return 99;;esac; }
( set -u; chay_ghi 08-close close; chay_ghi 09-delete-data delete-data
  if chay_ghi 10-verify tab-list; then echo "STOP: phiên $TL_PW_SESSION vẫn mở"; else echo "CLEANUP OK"; fi )
