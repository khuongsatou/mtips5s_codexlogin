# `.feedback` — Kênh trao đổi Codex ↔ Antigravity

## Mục tiêu

Lưu feedback có mã định danh, phản hồi, kế hoạch xử lý và kết quả QA tại một nơi dùng chung.

## Cấu trúc file

- `inbox.md`: feedback mới từ Codex/Antigravity.
- `responses.md`: đánh giá và phản hồi chính thức.
- `action-plan.md`: task xử lý, owner, ETA và status.
- `qa_coverage.json`: coverage/đối chiếu QA dạng JSON.

## Quy trình 4 bước

1. **Inbox:** ghi feedback với ID `FB-YYYYMMDD-AREA-001`.
2. **Assessment/Response:** đánh giá và chọn Accept / Reject / Need More Info.
3. **Action plan:** tạo task, gán owner/ETA, cập nhật Todo → In Progress → Done hoặc Blocked.
4. **Verification:** Tester/Customer xác minh, ghi bằng chứng và đóng log.
