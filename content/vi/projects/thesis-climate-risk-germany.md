---
title: Rủi ro khí hậu trên thị trường chứng khoán Đức
subtitle: "Luận văn thạc sĩ: thước đo hằng ngày về mức độ chú ý tới rủi ro khí hậu trong báo chí Đức, và tác động của nó lên lợi suất cổ phiếu"
period: 2026 – 2027
year: 2026
role: Đồng tác giả, cùng một bạn học
org: BI Norwegian Business School
tags: [Nghiên cứu, Tài chính khí hậu, R, Dữ liệu]
featured: true
order: 2
status: Đang thực hiện, nộp tháng 4/2027
summary: Tin tức về rủi ro khí hậu có làm cổ phiếu Đức dịch chuyển không? Để trả lời, chúng tôi xây một chỉ số hằng ngày về mức độ chú ý tới rủi ro khí hậu từ mười năm báo chí Đức. Hóa ra đường ống dữ liệu chiếm phần lớn công việc.
---
## Câu hỏi

Rủi ro khí hậu đi vào giá cổ phiếu qua hai kênh. Rủi ro vật lý là lũ lụt, nắng nóng và hạn hán. Rủi ro chuyển dịch là giá carbon, quy định và công nghệ. Chúng tôi muốn một thước đo hằng ngày về mức độ chú ý mỗi kênh nhận được trên báo chí Đức, rồi kiểm định xem mức chú ý đó có giải thích lợi suất và biến động giữa các ngành của thị trường Đức hay không.

## Đường ống dữ liệu

- **Nguồn.** GDELT, cơ sở dữ liệu mở về tin tức thế giới. Trên Google BigQuery, chúng tôi lọc khoảng 1,1 triệu bản ghi tiếng Đức từ 2015 đến 2025 xuống còn các bài liên quan đến khí hậu.
- **Mẫu.** Một mẫu phân tầng khoảng 70.000 đường dẫn, cân bằng theo thời gian và theo tờ báo, để một năm ồn ào không nhấn chìm một năm yên ắng.
- **Thu thập.** Toàn văn của khoảng 35.000 bài, bằng R. Đường dẫn từ 2015 đến 2018 thường đã chết; một lượt qua Wayback Machine khôi phục được khoảng 7.000 trong 10.700 đường dẫn chết.
- **Làm sạch.** Loại bỏ phần thừa, menu điều hướng và khung trang. Còn lại là kho ngữ liệu khoảng 27.000 bài.
- **Mô hình.** Mô hình chủ đề cấu trúc (structural topic model) với 25 và 40 chủ đề, ước lượng song song, các chủ đề được gán nhãn và ánh xạ vào rủi ro vật lý và rủi ro chuyển dịch.

## Điều tôi học được đến giờ

Làm dữ liệu chủ yếu là quyết định cái gì được tính: tờ báo nào, năm nào, từ nào. Có lần một đường dẫn giữ chân trình thu thập suốt tám tiếng, nên giờ có một cơ chế canh chừng bỏ qua trang không trả lời. Kho lưu trữ tin tức cũng không đầy đủ. Vài tờ có cả tháng trống, nên khối lượng bài phải đo trên một nhóm tờ báo cố định, không phải trên tất cả những gì tình cờ có mặt.

Công cụ: R (data.table, quanteda, stm, furrr) và SQL trên BigQuery.
