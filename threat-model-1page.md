# Threat Model - Lab 3

## Thông tin nhóm
- Thành viên 1: Đinh Dương Phong - 1871020451
- Thành viên 2: Trần Đình Đức Toàn - 1871020574

## Assets
Các tài sản cần bảo vệ trong hệ thống gồm:
- Plaintext (bản tin gốc của người dùng)
- DES key (khóa mã hóa/giải mã)
- IV (Initialization Vector dùng trong CBC)
- Ciphertext (dữ liệu đã mã hóa)
- Log hệ thống (có thể chứa dữ liệu nhạy cảm)
- Thông tin kết nối (IP, port)

## Attacker model
Kẻ tấn công có thể:
- Nghe lén dữ liệu trên cùng mạng (sniffing trong LAN)
- Chặn và sửa đổi dữ liệu trên đường truyền (man-in-the-middle)
- Gửi gói tin giả mạo đến receiver
- Gửi dữ liệu sai định dạng để gây lỗi hệ thống
- Ngắt kết nối đột ngột để làm gián đoạn dịch vụ

## Threats
Một số mối đe dọa cụ thể:

1. Lộ khóa (Key exposure)
- Do hệ thống gửi DES key dưới dạng plaintext qua mạng
- Attacker có thể dễ dàng lấy được key và giải mã toàn bộ dữ liệu

2. Sửa đổi ciphertext (Data tampering)
- Attacker thay đổi ciphertext trên đường truyền
- Gây lỗi khi giải mã hoặc làm sai nội dung bản tin

3. Giả mạo header độ dài (Fake length header)
- Attacker gửi độ dài sai
- Receiver đọc thiếu hoặc thừa dữ liệu → crash hoặc lỗi

4. Tấn công từ chối dịch vụ (DoS)
- Gửi dữ liệu lớn hoặc không hợp lệ liên tục
- Làm receiver treo hoặc quá tải

## Mitigations
Các biện pháp giảm thiểu:

1. Không truyền key dạng plaintext
- Sử dụng cơ chế trao đổi khóa an toàn (ví dụ: Diffie-Hellman)
- Hoặc dùng TLS để bảo vệ kênh truyền

2. Kiểm tra tính hợp lệ dữ liệu
- Validate độ dài header (length > 0 và giới hạn tối đa)
- Kiểm tra dữ liệu nhận đủ trước khi xử lý

3. Xử lý lỗi và log rõ ràng
- Dùng try-except để tránh crash
- Ghi log khi có lỗi xảy ra

4. Kiểm tra padding
- Phát hiện padding sai sau khi giải mã
- Tránh sử dụng dữ liệu không hợp lệ

5. Giới hạn tài nguyên
- Đặt timeout cho socket
- Giới hạn kích thước dữ liệu nhận

## Residual risks
Một số rủi ro vẫn còn tồn tại:

- Nếu máy người dùng bị nhiễm malware, attacker vẫn có thể lấy key và dữ liệu
- Log có thể chứa thông tin nhạy cảm nếu không được bảo vệ
- Trong môi trường mạng nội bộ, vẫn có nguy cơ bị sniffing nếu không mã hóa kênh truyền
