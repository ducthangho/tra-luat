#!/bin/bash
# Do toan bo tren exact H: N3 (hai clone nen/sau trong MOT lenh), N4, N2, dong lop. Dung: chay_het.sh <repo> <H>
set -u
R=$1; H=$2; D=/dev/shm/wp433
cd $D
echo "BAT DAU $(date -u +%FT%TZ) H=$H"
bash hd/do_n3.sh "$R" 0f9aa2a2cc697129e1f5be72feddf60986286865 "$H" $D/n3 ; echo "n3 xong $(date -u +%FT%TZ)"
bash hd/do_n4.sh "$R" "$H" a8a3b3ca2fe5f48d8e6db64a8c6abacf97526b8c $D/n4 > $D/n4.log 2>&1; echo "n4 rc=$? $(date -u +%FT%TZ)"
