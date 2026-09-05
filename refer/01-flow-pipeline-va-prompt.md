# 01 — Flow, pipeline và prompt/đối số điều khiển

## 1. Pipeline tổng thể

```text
Bootstrap
  → mở server
  → UI health-check
  → người dùng chọn flow
  → parse/normalize input
  → API server
  → OAuth hoặc import trực tiếp
  → chuẩn hóa connection
  → backup DB
  → ghi SQLite/JSON
  → xác minh email trong SQLite
  → UI hiển thị kết quả
```

## 2. Flow import session/token trực tiếp

1. Người dùng dán một hoặc nhiều JSON vào `#session-input`.
2. `collectSessions()` duyệt đệ quy object/list để tìm các object phù hợp.
3. `parseSession()` đọc JWT payload, lấy email, `chatgpt_account_id`, `chatgpt_plan_type` và token fields.
4. UI loại bản ghi thiếu token/email, chống trùng theo email và render preview.
5. Nút import gửi `POST /api/import` với `{ connections: [...] }`.
6. Server khóa `_storage_lock`, backup trước khi ghi, upsert vào các storage đang tồn tại.
7. Server gọi `verify_sqlite_emails()`; chỉ trả thành công nếu mọi email đầu vào có trong SQLite live.

## 3. Flow import nhiều file JSON

1. `handleFiles()` nhận file từ picker hoặc drag-and-drop.
2. `parseFileContent()` parse từng file, nhận cả object/list và các schema token khác nhau.
3. Mỗi item được gắn nguồn file, được gom vào bảng preview.
4. UI loại trùng email giữa các file trước khi gửi.
5. Gọi lại cùng endpoint `/api/import`; kết quả có inserted/replaced/errors/verifiedEmails.

## 4. Flow OAuth manual

```text
UI POST /api/oauth/start
  → server tạo verifier/challenge/state
  → server mở browser tới auth.openai.com/oauth/authorize
  → callback 127.0.0.1:1455/auth/callback
  → kiểm tra code + state
  → POST auth.openai.com/oauth/token
  → tokens_to_connection()
  → import_connections()
  → UI poll /api/oauth/status mỗi 1 giây
```

Timeout polling của UI là khoảng 2 phút; callback server xử lý một request rồi đóng.

## 5. Flow OAuth auto-login

```text
UI parseAccounts()
  → POST /api/oauth/auto-login
  → server ghi _tmp_accounts.txt
  → spawn auto_login.py --workers N [--headed]
  → ThreadPoolExecutor chạy từng account
  → browser riêng + context riêng
  → auth URL riêng (verifier/state riêng)
  → dispatcher callback dùng map state → CallbackResult
  → token exchange → import API localhost
  → server parse log machine-readable
  → UI poll /api/oauth/auto-status mỗi 500 ms
  → cập nhật history và load lại accounts
```

Mỗi account tối đa 3 lần thử trong `login_one_account()`. Các lỗi retryable gồm state không hợp lệ, timeout callback và lỗi 2FA; cuối run ghi `auto_login_results.json`.

## 6. Input contract

### Account text

Định dạng chuẩn:

```text
email|password|totp_secret
```

UI tự đổi tab, dấu chấm phẩy, comma (khi hợp lệ), hoặc từ 2 khoảng trắng thành `|`. Dòng trống và dòng bắt đầu bằng `#` bị bỏ qua. CLI chỉ nhận account có email và password.

### OAuth authorize parameters

Đây không phải LLM prompt; đây là bộ tham số giao thức OAuth:

| Tham số | Giá trị/ý nghĩa |
|---|---|
| `client_id` | Client Codex cố định trong mã nguồn |
| `redirect_uri` | `http://localhost:1455/auth/callback` |
| `response_type` | `code` |
| `scope` | `openid profile email offline_access` |
| `code_challenge` | Base64url(SHA-256(verifier)) |
| `code_challenge_method` | `S256` |
| `state` | Chuỗi ngẫu nhiên gắn callback với worker |
| `id_token_add_organizations` | `true` |
| `codex_cli_simplified_flow` | `true` |
| `originator` | `codex_cli_rs` |

Không phát hiện system prompt, user prompt, template LLM, hay gọi mô hình AI trong repository. “Prompt” của hệ thống này thực chất là selector/browser action và OAuth request parameters.

## 7. Browser automation prompt/action

`login_account()` không dùng prompt văn bản mà dùng chiến lược tìm phần tử:

- Email: `input[name=email]`, `type=email`, username, autocomplete và fallback input không hidden/password.
- Password: name/type/id/placeholder liên quan password.
- Nút: submit, Continue, Next, Log in, Sign in và bản dịch tiếng Việt.
- 2FA: phát hiện text/body và thử các selector input OTP/verification.
- Sau login: theo dõi URL callback, đọc `code`, `state`, `error`.

Điểm mạnh là selector fallback và retry nhanh; điểm yếu là phụ thuộc UI bên thứ ba, dễ hỏng khi OpenAI thay đổi DOM hoặc anti-bot.
