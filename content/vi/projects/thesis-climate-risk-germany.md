---
title: Rủi ro khí hậu trên thị trường chứng khoán Đức
subtitle: "Luận văn thạc sĩ: xây dựng chỉ số đo mức độ quan tâm tới rủi ro khí hậu trên báo chí Đức theo ngày, và phân tích tác động đến lợi suất cổ phiếu"
period: 2026 – 2027
year: 2026
role: Đồng tác giả, cùng một bạn học; tôi phụ trách một mình giai đoạn 1 (dữ liệu tin tức và chỉ số)
org: BI Norwegian Business School
tags: [Nghiên cứu, Tài chính khí hậu, R, Dữ liệu]
featured: true
order: 2
status: Đang thực hiện, nộp tháng 4/2027
summary: Tin tức về rủi ro khí hậu có ảnh hưởng đến giá cổ phiếu Đức không? Để trả lời, tôi đang xây dựng một chỉ số theo ngày từ mười năm báo chí Đức. Riêng phần dữ liệu đã chiếm phần lớn công việc.
art_caption: "Từ khoảng 1,1 triệu bản ghi tin tức, tôi chọn lọc còn khoảng 27.000 bài, rồi xây dựng chỉ số theo ngày về mức độ quan tâm tới rủi ro vật lý và rủi ro chuyển đổi, đặt cạnh giá cổ phiếu. Đây chỉ là sơ đồ minh họa, chưa phải kết quả."
---
## Câu hỏi nghiên cứu

Rủi ro khí hậu tác động đến giá cổ phiếu qua hai kênh. Rủi ro vật lý gồm lũ lụt, nắng nóng và hạn hán. Rủi ro chuyển đổi gồm giá carbon, chính sách và công nghệ. Chúng tôi muốn đo mức độ báo chí Đức quan tâm đến từng loại rủi ro theo từng ngày, rồi kiểm định xem mức độ quan tâm đó có giải thích được lợi suất và biến động của các ngành trên thị trường Đức hay không.

## Quy trình xử lý dữ liệu

- **Nguồn.** GDELT, cơ sở dữ liệu mở về tin tức toàn cầu. Trên Google BigQuery, tôi lọc khoảng 1,1 triệu bản ghi tiếng Đức giai đoạn 2015–2025 để lấy các bài liên quan đến khí hậu.
- **Chọn mẫu.** Mẫu phân tầng khoảng 70.000 đường link, cân bằng theo thời gian và theo tờ báo, để các năm nhiều tin không lấn át các năm ít tin.
- **Thu thập.** Tải toàn văn khoảng 35.000 bài bằng R. Nhiều link giai đoạn 2015–2018 đã hỏng, nhưng Wayback Machine giúp khôi phục được khoảng 7.000 trong số 10.700 link hỏng.
- **Làm sạch.** Loại bỏ các phần lặp lại, menu điều hướng và các thành phần của trang web. Bộ dữ liệu còn lại khoảng 27.000 bài.
- **Mô hình.** Mô hình chủ đề có cấu trúc (structural topic model) với 25 và 40 chủ đề, chạy song song, sau đó gán nhãn các chủ đề và phân vào rủi ro vật lý hoặc rủi ro chuyển đổi.

## Những điều tôi học được

Làm dữ liệu chủ yếu là quyết định cái gì được tính: tờ báo nào, năm nào, từ khóa nào. Có lần một đường link khiến chương trình thu thập bị treo suốt tám tiếng, nên giờ có thêm bước kiểm tra để bỏ qua những trang không phản hồi. Dữ liệu tin tức lưu trữ cũng không đầy đủ. Một số tờ báo không có bài nào trong nhiều tháng liền, nên số lượng bài phải được đo trên một nhóm báo cố định thay vì toàn bộ dữ liệu có sẵn.

Công cụ: R (data.table, quanteda, stm, furrr) và SQL trên BigQuery.
