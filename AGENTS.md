# Quy tắc viết tài liệu wiki

Áp dụng cho bài mới và các lần sửa trong `docs/`. Viết cho người giao dịch cá nhân biết đọc biểu đồ nhưng chưa chắc biết phương pháp đang nói đến.

- [ ] Đi theo thứ tự: phương pháp là gì → vì sao đáng thử → làm từng bước → số liệu nói gì → giới hạn → cách tự kiểm tra → nguồn. Tách phần tra cứu kỹ thuật khỏi luồng đọc chính.
- [ ] Mỗi câu một ý, thường không quá 25 từ. Mỗi đoạn trả lời một câu hỏi. Dùng động từ quen thuộc như “đánh dấu”, “chờ”, “bỏ qua”. Dùng danh sách cho các bước, bảng cho số liệu, không nhét cả đoạn văn vào một ô.
- [ ] Giải thích thuật ngữ ngay lần đầu. Viết tiếng Việt trước, ghi tên tiếng Anh hoặc chữ viết tắt trong ngoặc nếu cần tra cứu. Sau đó dùng nhất quán một cách gọi.
- [ ] Trong mạch chính, giữ số liệu đủ để trả lời câu hỏi. Đặt bảng đầy đủ, cách tính và giả định ở phần chi tiết. Luôn ghi đơn vị, mẫu và điều kiện so sánh; tách kết quả quan sát khỏi giả thuyết.
- [ ] Dẫn nguồn một lần cho mỗi nhóm nhận định có cùng nguồn. Khi dẫn một con số, chỉ rõ bảng, hình hoặc mục nếu có. Không bỏ cảnh báo làm đổi cách hiểu số liệu; đưa giới hạn kỹ thuật dài xuống phần chi tiết.
- [ ] Đặt hình cạnh đoạn nó giải thích. Viết mô tả thay thế và chú thích nêu điều cần nhìn. Hình ví dụ phải ghi “Dữ liệu mô phỏng, không phải kết quả kiểm thử”; hình số liệu phải ghi nguồn. Chỉ dùng chữ đậm để người đọc tìm nhanh ý chính.
- [ ] Đọc lại phần mở đầu và các bước như người chưa biết phương pháp. Nếu chưa thể làm theo trên biểu đồ, thêm một ví dụ cụ thể thay vì thêm thuật ngữ.

## Hai ví dụ từ bài ORB

**Trước:** “Vùng ngắn cho tín hiệu sớm nhưng dễ nhiễu; vùng dài cho thêm thời gian quan sát nhưng nếu cùng đóng cuối phiên, lệnh có ít thời gian hơn để đạt mục tiêu và stop theo biên có thể xa hơn.”

**Sau:** “Vùng ngắn cho tín hiệu sớm nhưng dễ nhiễu. Vùng dài cho thêm thời gian quan sát. Đổi lại, mức dừng lỗ ở biên đối diện có thể xa hơn và giá còn ít thời gian hơn để đi tới mục tiêu trước khi đóng cửa.”

**Trước:** “Mẫu số nên là khối lượng bình quân cùng cửa sổ thời gian ở các phiên trước, không phải khối lượng cả ngày.”

**Sau:** “Ví dụ, nếu 5 phút đầu hôm nay giao dịch 200.000 cổ phiếu, so với trung bình 100.000 cổ phiếu trong đúng 5 phút đầu các phiên trước, RVOL là 2.”
