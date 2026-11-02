---
title: Rủi ro khí hậu trên thị trường chứng khoán Đức
subtitle: "Luận văn thạc sĩ: đo mức độ chú ý tới rủi ro khí hậu trên báo chí Đức mỗi ngày, và xem nó tác động thế nào đến lợi suất cổ phiếu"
period: 2026 – 2027
year: 2026
role: Đồng tác giả, cùng một người bạn học
org: BI Norwegian Business School
tags: [Nghiên cứu, Tài chính khí hậu, R, Dữ liệu]
featured: true
order: 2
status: Đang thực hiện, nộp vào tháng 4/2027
summary: Tin tức về rủi ro khí hậu có làm cổ phiếu Đức biến động không? Để tìm câu trả lời, chúng tôi đang xây một chỉ số hằng ngày từ mười năm báo chí Đức. Và hóa ra phần dữ liệu mới chiếm gần hết công việc.
art_caption: "Từ khoảng 1,1 triệu bản ghi tin tức còn lại khoảng 27.000 bài, rồi thành một chỉ số hằng ngày về mức độ chú ý tới rủi ro vật lý và rủi ro chuyển đổi, đặt cạnh giá cổ phiếu. Đây chỉ là sơ đồ minh họa, chưa phải kết quả."
---
## Câu hỏi

Rủi ro khí hậu tác động đến giá cổ phiếu theo hai đường. Rủi ro vật lý là lũ lụt, nắng nóng, hạn hán. Rủi ro chuyển đổi là giá carbon, quy định và công nghệ. Chúng tôi muốn đo xem mỗi ngày, từng loại rủi ro được báo chí Đức nhắc đến nhiều đến đâu, rồi kiểm định xem mức độ chú ý đó có giải thích được lợi suất và biến động của các ngành trên thị trường Đức hay không.

## Chuỗi xử lý dữ liệu

- **Nguồn.** GDELT, cơ sở dữ liệu mở về tin tức toàn cầu. Trên Google BigQuery, chúng tôi lọc khoảng 1,1 triệu bản ghi tiếng Đức từ năm 2015 đến 2025 để lấy các bài liên quan đến khí hậu.
- **Mẫu.** Một mẫu phân tầng khoảng 70.000 đường link, cân bằng theo thời gian và theo từng tờ báo, để một năm nhiều tin không lấn át một năm ít tin.
- **Thu thập.** Lấy toàn văn của khoảng 35.000 bài bằng R. Các link từ 2015 đến 2018 thường đã chết, nhưng một lượt tìm lại qua Wayback Machine đã cứu được khoảng 7.000 trong số 10.700 link chết.
- **Làm sạch.** Bỏ phần thừa, menu điều hướng và các thành phần của trang web. Còn lại bộ dữ liệu khoảng 27.000 bài.
- **Mô hình.** Mô hình chủ đề có cấu trúc (structural topic model) với 25 và 40 chủ đề, chạy song song trên nhiều phiên, sau đó gán nhãn từng chủ đề và xếp vào rủi ro vật lý hoặc rủi ro chuyển đổi.

## Những gì tôi học được đến giờ

Làm dữ liệu thực ra chủ yếu là quyết định cái gì được tính: tờ báo nào, năm nào, từ khóa nào. Có lần chỉ một đường link đã giữ chân trình thu thập suốt tám tiếng, nên giờ có thêm một bước kiểm tra, trang nào không phản hồi thì bỏ qua. Kho lưu trữ tin tức cũng không hề đầy đủ. Có những tờ báo trống trơn cả tháng trời, nên số lượng bài phải đo trên một nhóm báo cố định, chứ không thể đếm hết những gì tình cờ có trong dữ liệu.

Công cụ: R (data.table, quanteda, stm, furrr) và SQL trên BigQuery.
