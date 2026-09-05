# 02 — Chi tiết chức năng, API, đầu vào và đầu ra

## 1. Bảng API

| Method | Endpoint | Đầu vào | Đầu ra |
|---|---|---|---|
| GET | `/api/health` | Không | Trạng thái storage, path dò được |
| GET | `/api/connections` | Không | `{ connections, count }` |
| POST | `/api/import` | `{ connections: [...] }` | inserted, replaced, errors, sqliteVerified |
| DELETE | `/api/connections/:id` | ID connection | `{ deleted: boolean }` |
| POST | `/api/oauth/start` | Không | authUrl, state; mở browser |
| GET | `/api/oauth/status` | Không | idle/waiting/success/error |
| POST | `/api/oauth/auto-login` | accounts, workers | run metadata |
| GET | `/api/oauth/auto-status` | Không | tiến độ, account đang chạy, kết quả |
| POST | `/api/oauth/auto-stop` | Không | trạng thái kill process/browser |

## 2. Chức năng server.py

### Storage discovery

`find_sqlite()`, `get_json_candidates()`, `find_json_paths()` dò SQLite và JSON ở các vị trí `.9router`, `APPDATA`, `AppData/Roaming`, `Library/Application Support`, và `.n9router`. `get_connections()` hợp nhất dữ liệu, ưu tiên nguồn hiện có.

### Import/upsert

`import_connections()` serialize toàn bộ thao tác bằng `_storage_lock`. SQLite dùng bảng `providerConnections`; nếu email tồn tại thì xóa bản ghi cũ rồi insert bản ghi mới, giữ priority cũ. JSON giữ connection provider khác, thay connection Codex theo email và sắp xếp priority.

Đầu ra đếm `inserted`, `replaced`, cùng danh sách lỗi. Trước khi sửa có `backup_file()` tạo backup timestamped trong `backups/`.

### Chuẩn hóa connection

`build_data_blob()` giữ token/expiry/status/providerSpecificData. `build_json_connection()` thêm `id`, provider, authType, name, email, priority, isActive, createdAt/updatedAt.

### OAuth manual

`build_authorize_url()` tạo PKCE/state; `OAuthCallbackHandler` nhận callback, đổi code, gọi `tokens_to_connection()`, import và trả HTML kết quả. UI chỉ biết kết quả qua polling.

### Auto worker control

`start_auto_login()` tạo background thread; `_auto_login_worker()` ghi file tạm, chạy subprocess, đọc từng dòng log và map event vào `_auto_login_status`. `stop_auto_login()` terminate process/tree và dọn các browser Playwright.

## 3. Chức năng auto_login.py

| Hàm/nhóm | Trách nhiệm | Đầu vào | Đầu ra |
|---|---|---|---|
| `generate_pkce`, `build_auth_url` | Tạo OAuth request | Không | URL, verifier, state |
| `exchange_code` | Đổi code lấy token | code, verifier | token JSON hoặc lỗi |
| `decode_jwt_email` | Đọc metadata JWT payload | access token | email/account/plan |
| `tokens_to_connection` | Đổi token thành schema 9router | token JSON | connection dict |
| `normalize_totp_secret` | Chuẩn hóa Base32/otpauth URL | secret | secret sạch |
| `get_2fa_code` | Lấy TOTP online rồi fallback local | secret, attempt | mã 6 số |
| `login_account` | Điều khiển browser OAuth | page, account | token hoặc lỗi |
| `parse_accounts` | Đọc file account | path | list tuple |
| `login_one_account` | retry, import, emit event | account/index | result dict |
| `main` | CLI + ThreadPoolExecutor | file/flags | JSON kết quả |

## 4. Giao diện index.html

| Khu vực | Chức năng | Trạng thái đầu ra |
|---|---|---|
| Import | Dán session/token, parse preview, download dữ liệu đã chuẩn hóa | số parsed/skipped/error, import message |
| Accounts | Đọc danh sách từ server, refresh, xóa, export Cockpit | bảng account và số lượng |
| File Import | Chọn nhiều JSON, preview theo file, import tất cả | số file/tổng item/lỗi |
| OAuth Auto | Parse account, chọn số worker, chạy/dừng, poll tiến độ | progress, active workers, history |
| OAuth Manual | Mở login browser và chờ callback | success/error/timeout |

## 5. Schema đầu ra connection

Các nhóm field chính: `accessToken`, `refreshToken`, `idToken`, `expiresAt`, `expiresIn`, `testStatus`, `lastUsedAt`, `consecutiveUseCount`, `backoffLevel`, `providerSpecificData`, `lastError`, `email`, `name`, `provider=codex`, `authType=oauth`.

`providerSpecificData` chứa `chatgptAccountId` và `chatgptPlanType`. Token thật không được đưa vào tài liệu này.

## 6. Hành vi lỗi

- Thiếu server/storage: UI báo offline hoặc API trả lỗi.
- JSON không hợp lệ: item bị đánh dấu lỗi trong preview.
- Thiếu email/token: bị loại khỏi tập import.
- Port 1455 bận: OAuth manual thất bại ngay.
- OAuth state sai/hết hạn: callback bị từ chối; auto flow có retry.
- DB không tồn tại: import dừng và trả danh sách path ứng viên.
- SQLite không thấy email sau commit: API trả HTTP 500 dù thao tác có thể đã ghi một phần; cần kiểm tra backup/DB.

## 7. Điểm lệch cần biết

UI gửi `{ headless: runHeadless, workers }`, nhưng `server.py` đặt `headed = True` và không đọc `data.headless`. Vì vậy checkbox headless trên giao diện hiện không có tác dụng thực tế.
