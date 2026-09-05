# 03 — Bảo mật, vận hành và khuyến nghị

## 1. Dữ liệu nhạy cảm

Workspace hiện có artefact chứa token OAuth và file input account có thể chứa password/TOTP. Các file này không nên commit, upload, gửi qua chat, hoặc đưa vào preview HTML. Nên coi toàn bộ token đã xuất hiện trong workspace là có khả năng bị lộ và xoay vòng/thu hồi theo chính sách vận hành phù hợp.

## 2. Rủi ro chính

| Mức | Vấn đề | Tác động | Khuyến nghị |
|---|---|---|---|
| Cao | Password/TOTP ghi vào `_tmp_accounts.txt` | Lộ credential sau khi process kết thúc | dùng stdin/pipe mã hóa, xóa file ngay cả khi lỗi, quyền file hạn chế |
| Cao | Token lưu plaintext trong DB/JSON/backup | Ai đọc được file có thể dùng session | mã hóa at-rest, hạn chế ACL, retention ngắn |
| Cao | CORS `*` trên API nhạy cảm | Trang khác có thể gọi localhost API trong một số môi trường | chỉ cho origin cụ thể, thêm CSRF token/local secret |
| Trung bình | Xóa DB có backup timestamped | Backup tiếp tục chứa token | mã hóa và dọn theo retention |
| Trung bình | HTML callback chèn dữ liệu chưa escape | Có thể XSS nếu email/error bị kiểm soát | escape HTML trước khi render |
| Trung bình | Dò nhiều path tự động | Có thể ghi nhầm DB nếu môi trường có nhiều bản | hiển thị và yêu cầu xác nhận target |
| Thấp | Log URL/title/screenshot debug | Có thể lộ email/trạng thái login | mask dữ liệu, tắt debug mặc định |

## 3. Vận hành an toàn đề xuất

1. Chạy bằng user account riêng, không quyền administrator.
2. Không dùng dữ liệu account thật trong `accounts_sample.txt`.
3. Trước run lớn, snapshot DB và ghi nhận số connection hiện tại.
4. Giới hạn worker theo RAM/CPU và rate limit để giảm captcha/lockout.
5. Kiểm tra `sqliteVerified`, `inserted`, `replaced`, `errors`; không chỉ dựa vào UI màu xanh.
6. Sau run, xóa file tạm, screenshot debug và output token không cần thiết.
7. Đặt `refer/preview.html` chỉ là tài liệu tĩnh; không nhúng token, không tự gọi API.

## 4. Test checklist

- [ ] Khởi động khi không có 9router DB: health và thông báo lỗi đúng.
- [ ] Import một connection mới: inserted + verify true.
- [ ] Import lại cùng email: replaced, priority được giữ.
- [ ] Import nhiều file có email trùng: UI chỉ gửi một bản.
- [ ] Xóa connection: SQLite và JSON cùng nhất quán.
- [ ] OAuth callback sai state: bị từ chối.
- [ ] OAuth token exchange lỗi HTTP: UI nhận error, không treo polling.
- [ ] Auto login một account lỗi password: kết thúc với error và không kẹt worker.
- [ ] Auto stop: process/browser được dọn.
- [ ] Port 1455 bận: thông báo nguyên nhân rõ ràng.
- [ ] Kiểm tra checkbox headless sau khi sửa để bảo đảm server thực sự tôn trọng lựa chọn.

## 5. Roadmap ưu tiên

### P0 — bảo vệ credential

- Loại password/TOTP khỏi file tạm plaintext; truyền dữ liệu qua IPC/pipe hoặc file mã hóa tạm.
- Thêm secret local cho API và tắt CORS wildcard.
- Mã hóa DB backup hoặc xóa tự động theo retention.

### P1 — độ tin cậy

- Hợp nhất logic OAuth/PKCE/token mapping vào module dùng chung.
- Thêm schema validation cho `/api/import` và `/api/oauth/auto-login`.
- Làm transaction/rollback rõ ràng khi SQLite ghi được nhưng JSON lỗi.
- Tôn trọng `headless` từ UI hoặc bỏ hẳn checkbox.

### P2 — khả năng bảo trì

- Thêm test tự động cho parser, PKCE, dedup, import/verify.
- Tách inline JavaScript/CSS khỏi `index.html`.
- Dùng logging có cấp độ, correlation ID và masking email/token.
