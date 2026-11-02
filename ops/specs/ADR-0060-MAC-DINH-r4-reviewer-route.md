# #1124 r4 � amendment routing reviewer v� human audit

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab
dieu_kien_merge: ADR-0060@36d7c5dcdcbbb27176b75135125b9009f9fe0587

Revision k? nhi?m: 4; generation: 1. ��?ng d?n khi c�ng b?:
`ops/specs/ADR-0060-MAC-DINH-r4-reviewer-route.md`.

Tr?ng th�i: DRAFT � ch�a duy?t, ch�a c�ng b?, ch�a d�ng c?p lease ho?c nghi?m thu.

## Ph?m vi v� k? th?a

K? th?a to�n b? �?c t? `ops/specs/ADR-0060-MAC-DINH-r3.md`, SHA-256
`f7e8826d11545ce77b4630e4682464f74c6f1a277bc0e98a93ff5fbd459323e0`.
Amendment n�y ch? thay routing reviewer v� b? sung human audit tr�?c merge.
A1�A13, write set, budget, Windows required, A10, ADR-0060 M3 v� m?i gate kh�c gi? nguy�n ngh?a.
Kh�ng mi?n l?i setup, skipped/not_run, kh�ng s?a baseline ho?c ng�?ng tu?i b?ng ch?ng.

?ng vi�n k? th?a: H4 `c905714f408df0982438b435d7de0871f66eea77`,
tree `1effe33b73ab302f13844cedb4984da83c8b4bd3`,
parent `dc8b6d3b605c24c5a6b57005ad2265b535e476b2`;
base B `340163a3f4f4dccf3c02ab153c843e8f305fdeb2`.
C�c SHA n�y �?nh danh ngu?n k? th?a v� b?ng ch?ng ch?n �o�n hi?n t?i. Sau khi spec ��?c duy?t v� land
qua l�n spec, l?y B' l� commit master �? ch?a artifact spec, ghi exact SHA v�o lease k? nhi?m;
rebase ph?n m? l�n B' th�nh H'. Diff B'..H' v?n ph?i ��ng n�m t?p W1�W5 theo A12.
Kh�ng th�m spec th�nh t?p th? s�u trong diff m? �? n� write set. B'/H' ph?i ��?c review/test �?y �?;
kh�ng d�ng k?t qu? c?p B/H4 hi?n t?i l�m nghi?m thu thay cho c?p B'/H'.
Commit m?i l�m m?t hi?u l?c review/tests/authorization c?a SHA c? theo protocol.

## Routing thay th?

Codex ti?p t?c l�m executor. V? agy h?t quota, reviewer c� th? l� m?t phi�n Codex �?c l?p,
context/worktree ri�ng, m?c �?nh read-only, d�ng model ho?c reasoning effort cao h�n executor.
Ph?i ghi c?u h?nh executor v� reviewer th?c s? quan s�t ��?c trong bi�n nh?n; ph?n kh�ng �o ��?c
ph?i ghi `khong_do_duoc`, kh�ng suy t�n model �? ph?c v? ch? t? t�n c�ng c? ho?c c?u h?nh y�u c?u.
N?u ch�a ch?ng minh ��?c �i?u ki?n cao h�n th? ch�a �?t routing, ph?i b�o ch? kho quy?t �?nh.
Executor kh�ng t? review ho?c t? approve c�ng vi?c c?a m?nh.

Ch? khi reviewer tr? verdict approve tr�n ��ng H, ch?ng c? �?c l?p v� �i?u ki?n routing n�u tr�n �?u �?t,
review c�ng nh� cung c?p m?i ��?c ghi `same_provider_approved`; kh�ng ghi `cross_approved`.
Bi�n nh?n ph?i neo ��ng SHA v� ghi c�ch x? l? t?ng finding; P0/P1/P2/P3 ph?i b?ng 0 tr�?c merge.
Y�u c?u 0 P1/P2/P3 l� ch? th? tr?c ti?p c?a ch? kho trong phi�n n�y
(��i?u ki?n �? m� merge �� l� v� v� cross review h?t P1, P2, P3�), kh�ng ph?i mi?n tr? ho?c di?n gi?i M1.
Review chuy�n m�n n�y kh�ng ph?i GitHub PR approval v� kh�ng t? cho ph�p submit approval.

## Human audit v� authority

Sau khi review v� to�n b? gate b?t bu?c �?t, tr?nh ch? kho g�i human audit neo ��ng H:
spec_hash, H/tree/parent/B, bi�n nh?n reviewer v� c?u h?nh, x? l? findings, Windows B/H,
CI exact HEAD, nghi?m thu A1�A13 (A13 ghi ��ng tr?ng th�i h?u land), v� c�c quy?t �?nh/waiver h?p l? n?u c�.
Ch? merge sau khi ch? kho ho�n t?t human audit v� duy?t ��ng H theo ADR-0060 M7.
�?i H sau audit ph?i tr?nh l?i audit/duy?t cho H m?i.

Amendment n�y l� artifact k? nhi?m d?ng addendum: r3 b?t bi?n ��?c tham chi?u b?ng hash ? tr�n,
v� ch�nh byte c?a addendum n�y l� spec_path/spec_hash ��?c ch? kho duy?t v� lease k? nhi?m tham chi?u.
N?u gh�p ho?c �?i byte th�nh m?t artifact kh�c, artifact �� c?n review v� duy?t hash ri�ng tr�?c c?p lease.
Lease revision 4/generation 1 ph?i tr? ��ng ��?ng d?n tr�n v� hash c?a ch�nh artifact �? duy?t.
Tr�?c nghi?m thu K1, blob spec t?i HEAD ?ng vi�n ph?i kh?p hash lease. H4 ch? l� ngu?n k? th?a;
n?u t�ch h?p spec l�m �?i HEAD, ph?i review v� ch?y l?i c�c gate theo HEAD m?i, kh�ng t�i d�ng verdict/tests H4.
Ch? sau khi ch? kho duy?t SHA-256 c?a addendum n�y m?i ��?c c�ng b? v�
c?p lease k? nhi?m thay routing AGY/cross_approved c?a lease r3; ghi r? lease b? thay th?,
gi? nguy�n ownership/write set v� ki?m tra holder hi?n h�nh tr�?c c?p.
Kh�ng ghi �� lease �ang ho?t �?ng c?a phi�n kh�c. Vi?c duy?t amendment kh�ng t? x�c nh?n test,
kh�ng mi?n M3(a)/(b)/(c), kh�ng thay human audit ho?c quy?t �?nh merge neo SHA.
Duy?t amendment kh�ng ch?ng minh ho?c mi?n y�u c?u reviewer cao h�n executor; thi?u b?ng ch?ng v?n ch?n routing.

