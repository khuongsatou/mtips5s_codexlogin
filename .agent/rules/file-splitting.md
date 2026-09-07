# Rule: File Splitting

Tự áp dụng khi file, module, prompt, workflow hoặc tài liệu quá lớn, khó bảo trì hoặc có nguy cơ vượt context.

- Xác định ranh giới logic và dependency trước khi tách; ghi lý do tách.
- Tách theo trách nhiệm, đặt tên rõ, duy trì một nguồn sự thật; không phân mảnh tùy tiện.
- Giữ nguyên import, public interface, reference và hành vi.
- Cập nhật test, tài liệu, manifest và liên kết sau khi tách.
- Kiểm tra từng file sau tách và báo cáo split map trong implementation notes.
