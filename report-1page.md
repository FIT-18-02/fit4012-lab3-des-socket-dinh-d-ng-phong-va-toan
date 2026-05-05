# Report 1 page - Lab 3

## Thông tin nhóm
- Thành viên 1: Đinh Dương Phong - 187102
- Thành viên 2: TODO_STUDENT

## Mục tiêu
Bài lab nhằm xây dựng một hệ thống truyền dữ liệu qua mạng sử dụng socket TCP kết hợp với mã hóa DES-CBC. Sinh viên cần hiểu được luồng hoạt động giữa Sender và Receiver, bao gồm việc tạo khóa, mã hóa dữ liệu, gửi gói tin và giải mã ở phía nhận. Ngoài ra, bài lab giúp rèn luyện kỹ năng xử lý lỗi, kiểm thử hệ thống và phân tích các rủi ro bảo mật trong quá trình truyền dữ liệu. Thông qua đó, sinh viên nhận thức rõ hơn về các vấn đề an toàn thông tin trong hệ thống thực tế.

## Phân công thực hiện
- Đinh Dương Phong:
  - Phụ trách chính phần Receiver (nhận dữ liệu, parse header, giải mã)
  - Xử lý lỗi và ghi log phía receiver
- Thành viên 2:
  - Phụ trách chính phần Sender (mã hóa, tạo packet, gửi dữ liệu)
  - Thực hiện các test case và ghi log phía sender
- Cả hai:
  - Cùng thiết kế cấu trúc gói tin
  - Cùng viết threat model và README
  - Kiểm thử và sửa lỗi chéo

## Cách làm
Hệ thống được xây dựng gồm hai thành phần: Sender và Receiver giao tiếp qua socket TCP. Sender nhận input từ người dùng, sau đó sử dụng thuật toán DES-CBC để mã hóa dữ liệu với key và IV được sinh ngẫu nhiên. Dữ liệu sau khi mã hóa được đóng gói thành packet gồm header (chứa key, IV và độ dài ciphertext) và phần ciphertext, rồi gửi qua socket.

Receiver mở cổng và lắng nghe kết nối, sau đó nhận packet, tách header để lấy key, IV và độ dài dữ liệu. Tiếp theo, receiver nhận đủ ciphertext, thực hiện giải mã DES-CBC và in ra bản rõ. Hệ thống có bổ sung kiểm tra độ dài dữ liệu, xử lý lỗi bằng try-except và ghi log để phục vụ kiểm thử.

Các test case được thực hiện gồm: truyền dữ liệu hợp lệ (happy path), gửi thiếu dữ liệu, sai độ dài header và lỗi padding.

## Kết quả
Hệ thống chạy thành công với đầy đủ chức năng:
- Sender gửi dữ liệu mã hóa thành công
- Receiver nhận và giải mã chính xác bản tin gốc

Các ca kiểm thử:
- Happy path: dữ liệu được giải mã đúng
- Truncated data: receiver phát hiện lỗi và ghi log
- Bad padding: hệ thống báo lỗi giải mã

Log minh chứng cho thấy hệ thống xử lý đúng cả trường hợp thành công và lỗi, không bị treo hoặc crash.

## Kết luận
Qua bài lab, nhóm hiểu rõ hơn về cách hoạt động của socket TCP và quá trình truyền dữ liệu giữa hai tiến trình. Việc áp dụng DES-CBC giúp nhận thức được cách mã hóa và giải mã dữ liệu trong thực tế, đồng thời thấy rõ các điểm yếu khi thiết kế hệ thống chưa an toàn (ví dụ: truyền key dạng plaintext).

Ngoài ra, nhóm rút ra rằng việc kiểm tra dữ liệu đầu vào, xử lý lỗi và ghi log là rất quan trọng để đảm bảo hệ thống hoạt động ổn định. Bài lab cũng giúp nâng cao tư duy về bảo mật, đặc biệt là việc phân tích threat model và nhận diện rủi ro trong hệ thống mạng
