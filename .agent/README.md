# Vận hành dự án IT

## Vai trò điều phối

- **Project Manager (PM):** người đứng đầu dự án; nhận yêu cầu, chia task, điều phối Agent, theo dõi trạng thái trong `.manager/`, xử lý blocker và xác nhận bàn giao.
- **Customer Reviewer:** đại diện khách hàng; đánh giá giao diện, trải nghiệm và chức năng theo tiêu chí chấp nhận, ghi nhận tại `.manager/ux-feedback.md`.
- **Agent:** thực hiện phân tích, lập trình, kiểm thử, tài liệu và báo cáo theo skill/rule/workflow.

## Cách dùng

1. PM ghi task và yêu cầu vào `.manager/current_task.md` và `requirements.md`.
2. Agent thực hiện theo workflow, cập nhật `implementation.md`, `test-report.md` và `iteration_log.md`.
3. Customer Reviewer đánh giá UI/chức năng; PM quyết định vòng lặp tiếp theo.
4. Feedback giữa Codex và Antigravity dùng `.feedback/` theo luồng inbox → response → action plan → QA.

Đọc các file trong `skills/`, `rules/`, `workflows/` trước khi bắt đầu task tương ứng.
