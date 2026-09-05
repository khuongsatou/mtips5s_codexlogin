# 00 — Tổng quan dự án

## 1. Mục đích

`Infinity AI Store — Import 9router Tool` là một công cụ chạy cục bộ trên máy người dùng để:

- Mở giao diện web quản lý tại `http://127.0.0.1:9876`.
- Nhận session/token hoặc danh sách tài khoản OAuth Codex.
- Đăng nhập một hoặc nhiều tài khoản qua trình duyệt Chrome/Chromium Playwright.
- Đổi authorization code lấy token, chuẩn hóa thành connection của provider `codex`.
- Ghi connection vào SQLite/JSON của 9router và xác minh lại sau khi commit.
- Hiển thị tiến độ, lỗi, danh sách connection và cho phép xóa/export.

Đây là một ứng dụng local-first, không có frontend framework và không có backend framework: `index.html` là UI, `server.py` là HTTP server, `auto_login.py` là worker tự động hóa.

## 2. Cấu trúc file

| File | Vai trò | Đầu vào chính | Đầu ra/chức năng |
|---|---|---|---|
| `index.html` | Giao diện và client logic | JSON session, file JSON, email/password/2FA | Preview, gọi REST API, hiển thị trạng thái |
| `server.py` | HTTP API + storage adapter + OAuth manual | Request HTTP, token connection, account list | Ghi DB, đọc/xóa connection, khởi chạy worker |
| `auto_login.py` | Worker OAuth song song | File tài khoản `email|password|2fa` | Token, kết quả import, `auto_login_results.json` |
| `khoi_dong_o_day.bat` | Bootstrap Windows | Máy có Python/pip | Cài dependency, Chromium, chạy server |
| `README.txt` | Hướng dẫn vận hành | Người dùng | Quy trình cài/chạy cơ bản |
| `accounts_sample.txt` | Mẫu input account | Dòng account | Dữ liệu mẫu để nhập UI/CLI |
| `backups/` | Bản sao trước khi ghi/xóa | DB SQLite/JSON | Khả năng phục hồi thủ công |
| `auto_login_results.json` | Nhật ký kết quả cuối run | Worker | Trạng thái từng account |
| `cockpit-bulk-import.json`, `pedal.takers...json` | Dữ liệu token/export | Token OAuth | Input/artefact dữ liệu nhạy cảm |

## 3. Thành phần và ranh giới

```text
Người dùng
   │
   ▼
index.html ──HTTP localhost:9876──▶ server.py
                                      ├─ 9router SQLite
                                      ├─ 9router/n9router JSON
                                      ├─ OAuth OpenAI (authorize/token)
                                      └─ auto_login.py ──▶ Chrome/Chromium
                                                            └─ OAuth callback :1455
```

## 4. Phụ thuộc và điều kiện chạy

- Windows 10/11 64-bit theo README; mã Python cũng có nhánh tương thích đường dẫn macOS.
- Python 3.11+ và `pip`.
- Package `pyotp`, `playwright`, cùng Chromium Playwright.
- Internet trong lúc OAuth và khi dùng `2fa.live`.
- 9router hoặc n9router phải có DB để import; server tự dò nhiều vị trí.
- Port `9876` cho UI/API và port `1455` cho OAuth callback.

## 5. Đánh giá nhanh

### Điểm hay

1. Tách UI, API và worker giúp giao diện không phải trực tiếp thao tác DB.
2. PKCE S256 và `state` giúp liên kết callback đúng phiên OAuth.
3. Mỗi account có browser context riêng; worker chạy song song và có retry.
4. Import có backup trước khi sửa, chống trùng theo email và xác minh SQLite sau ghi.
5. Có log máy đọc được (`EVENT|...`, `IMPORT_OK|...`) để cập nhật tiến độ theo account.
6. UI hỗ trợ nhiều định dạng nhập và preview trước khi import.

### Điểm cần cải thiện

1. API bind local nhưng bật CORS `*`; nếu có service khác truy cập được có thể gọi thao tác nhạy cảm.
2. Dữ liệu password, TOTP secret và token đi qua file tạm/log/JSON; cần mã hóa hoặc tối thiểu xóa an toàn sau run.
3. Có mã trùng cho OAuth ở `server.py` và `auto_login.py`, tăng rủi ro lệch hành vi.
4. UI gửi lựa chọn headless nhưng server đang đặt `headed = True` cố định.
5. Callback HTML chèn một số giá trị lỗi/email vào HTML mà không escape.
6. Việc tìm DB dựa trên nhiều path hệ điều hành nhưng chưa có cấu hình rõ ràng/lock liên tiến trình.

## 6. Phạm vi phân tích

Phân tích này dựa trên mã nguồn và artefact hiện có trong workspace. Không giải mã, không trích xuất và không hiển thị token thật; các giá trị nhạy cảm trong ví dụ được mô tả bằng placeholder.
