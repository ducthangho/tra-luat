import sys,re,hashlib
BASE_YAML='28fe56a370bf264bdc4604c54374f5700de528171794faefff803a37f2e1df68'
MD=(
    '`heartbeat_at` là lời khai: trong kho không có cổng nào đọc trực tiếp trường này.',
    'Ngưỡng thu hồi 360 phút cho lease mới thuộc hiệu lực `ADR-0056` do phiên điều phối áp tay, theo bảng §20.',
    'Theo protocol, `lease_until` là hạn tuyệt đối; trong mã, chỉ `kiem-dong-wp` của `.claude/dev/packet_loop.py` đọc trường này, ở điều kiện D4: `lease_until` phải đã qua thì mới đóng được WP.',
    'Khi kiểm lease để công bố với chốt hạn bật, `kiem()` của `ops/lease_publish.py` dùng `lease_expires_at_utc` để từ chối lease đã hết hạn; `ai-dang-giu` dùng cùng trường để phân loại hạn.',
    'Đường kiểm idempotent (`kiem_github`) và đường kiểm lease lịch sử trong CI (`ops/ci_duong_nhanh.py`) bỏ riêng phép chặn hết hạn.',
    '`reviewed_sha_required` là mỏ neo xuất phát, được phép bằng `base_sha` khi chưa có head ứng viên; `kiem()` chỉ đòi trường có mặt và đúng dạng 40 hex thường.',
    'Exact head không đọc từ lease: `kiem-merge` neo head PR ở K0, kiểm review connector ở K3, và kiểm review offline hoặc human audit trên cùng head ở K4; `record-review` so `--reviewed-sha` với head đã ghi khi vào `reviewing`.',
)
MD_SHA='27c00e50f6aaa1d63482f7be1f9b894e3d985eeb3a875603d6ac11bff14c87a8'
VUNG_SHA='6c4ec88cb1e15fd43556f6ed5e8304da613814b825a283e445d0ba33db8b8215'
def chet(ly_do): print('DO:',ly_do); sys.exit(1)
if len(MD)!=7 or not all(m.strip() for m in MD) or hashlib.sha256(('\n'.join(MD)+'\n').encode()).hexdigest()!=MD_SHA:
    chet('bay menh de nhung trong script khong khop MD_SHA cua dac ta')
ky_vong=('\n'+'\n\n'.join(MD)+'\n').encode()
if hashlib.sha256(ky_vong).hexdigest()!=VUNG_SHA: chet('khoi chot dung tu MD khong khop VUNG_SHA cua dac ta')
# Hai cách gọi: `n5.py <H>` kiểm vùng đích của H; `n5.py --ky-vong <base> <ra>` ghi ra tệp kỳ vọng = base chèn khối (cho N1).
dung=len(sys.argv)==4 and sys.argv[1]=='--ky-vong'
if not (dung or len(sys.argv)==2): chet('cach goi: n5.py <H>  hoac  n5.py --ky-vong <base> <ra>')
b=open(sys.argv[2] if dung else sys.argv[1],'rb').read()
s4=b.find(b'\n## 4. '); s5=b.find(b'\n## 5. ')
if s4<0 or s5<s4: chet('khong dinh vi duoc §4/§5')
neo=b.find('Lease gồm:\n\n```yaml\n'.encode(),s4,s5)
if neo<0: chet('khong thay "Lease gồm:" + rao yaml trong §4')
y0=neo+len('Lease gồm:\n\n'.encode())
dong=b.find(b'\n```',y0+7)
if dong<0: chet('khong thay rao dong yaml')
y1=b.find(b'\n',dong+4)+1
h=hashlib.sha256(b[y0:y1]).hexdigest()
if h!=BASE_YAML: chet('khoi YAML lech byte: '+h)
r1=b.find('\nLease `role: reviewer`'.encode(),y1,s5)
if r1<0: chet('khong thay doan "Lease `role: reviewer`" trong §4 sau khoi YAML')
vung=b[y1:r1]
if dung:
    if vung!=b'': chet('base khong co vung dich rong: '+str(len(vung))+' byte')
    open(sys.argv[3],'wb').write(b[:y1]+ky_vong+b[y1:]); print('da_ghi_ky_vong',sys.argv[3]); sys.exit(0)
# ALLOWLIST: vùng đích phải BẰNG TỪNG BYTE khối đã chốt; mọi thứ khác đều đỏ.
if vung!=ky_vong: chet(f'vung dich lech khoi da chot: {len(vung)} byte, sha256 {hashlib.sha256(vung).hexdigest()}')
print('vung_dich_khop_khoi_chot',VUNG_SHA,'yaml_sha',h)
