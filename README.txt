Infinity AI Store - Import 9router Tool v2.2
==============================================

Yeu cau truoc khi chay:
- Windows 10/11 64-bit.
- May phai co cai san Python 3.11 tro len (64-bit).
- Luc cai PHAI tick: Add python.exe to PATH.
- Da cai va dang nhap 9router tren may.

Tinh nang:
- Auto Login OAuth Codex hang loat, chay song song nhieu tai khoan.
- Tu nhap so luong ngay tren giao dien (mac dinh 3, khong gioi han cung).
- Callback OAuth dung localhost:1455 va tu phan luong theo state, tranh lan ket qua giua cac nick.
- Ho tro email|password|2FA (Tich hop 2fa.live chuan NTP quoc te + fallback pyotp).
- Tu dong convert dinh dang paste tu file/tab/comma/space.
- Moi tai khoan chay browser rieng, sach session.
- Realtime logs, tien do va danh sach nick dang chay tren giao dien.
- Import refresh token vao 9router va kiem chung SQLite sau khi ghi.

Cach chay (tu setup tu dong):
1. Giai nen file ZIP vao mot thu muc rieng.
2. Double-click: khoi_dong_o_day.bat.
3. Lan dau file bat tu dong:
   - Kiem tra Python va pip.
   - Cai/cap nhat pyotp + playwright.
   - Tai Chromium cho Playwright.
   - Khoi dong server tool.
4. Trinh duyet se tu mo tai: http://localhost:9876
5. Vao tab Auto Login, dan danh sach nick va nhap so luong muon chay.

Neu bao khong tim thay Python:
- Cai Python 3.11 64-bit tro len, sau do dong va mo lai khoi_dong_o_day.bat.

Luu y:
- Can internet khi cai lan dau va trong luc dang nhap OAuth.
- Nhieu luong hon se ton RAM/CPU va co the gap captcha/xac minh nhieu hon.
- Khong nen xoa auto_login.py, server.py hoac index.html trong thu muc da giai nen.
- Khong can cai thu cong neu khoi_dong_o_day.bat chay thanh cong.
