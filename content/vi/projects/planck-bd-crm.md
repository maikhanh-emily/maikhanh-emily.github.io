---
title: Một CRM xây mà không có kỹ sư
subtitle: Ứng dụng web vận hành pipeline phát triển kinh doanh của một start-up, dựng bằng trợ lý lập trình AI
period: 6/2026 – nay
year: 2026
role: Thiết kế, xây dựng và chịu trách nhiệm
org: Planck Technologies AS
tags: [Xây dựng với AI, Phần mềm, Phát triển kinh doanh]
featured: true
order: 1
status: Đang dùng hằng ngày
summary: Pipeline thương mại của Planck từng nằm trong một bảng tính. Tôi xây ứng dụng web thay thế nó, bằng Claude Code và không có kỹ sư hỗ trợ. Cả nhóm làm việc trên đó mỗi ngày.
---
## Vấn đề

Planck Technologies là một start-up deep-tech Na Uy ứng dụng AI vào thiết kế vật liệu thu giữ CO₂. Các kỹ sư của công ty xây nền tảng khám phá vật liệu, tức là sản phẩm chính. Không ai rảnh để làm công cụ nội bộ, và pipeline thương mại nằm trong những bảng tính lệch nhau ngay khi hai người cùng sửa.

## Tôi đã xây gì

Một CRM nội bộ cho pipeline khách hàng, sau đó là một cái thứ hai cho nhà đầu tư. Công ty vào hệ thống qua điểm phù hợp, đi qua các giai đoạn, mang theo đầu mối liên hệ, ghi chú và nhật ký hoạt động, rồi đổ vào các màn hình dashboard, pipeline, tiếp cận và báo cáo. Báo cáo tuần cho ban lãnh đạo xuất thẳng từ đây. Quy mô: hơn 500 tổ chức được sàng lọc, khoảng 60 đang theo sát.

## Cách nó hoạt động

Kiến trúc khác thường, và cố ý như vậy.

- Một ứng dụng React viết trong một file JSX duy nhất, được một script Python biên dịch thành một file HTML độc lập. Không Node, không npm, không server. Mọi người mở bằng cách nhấp đúp.
- Trạng thái nằm trong trình duyệt. Với cả nhóm, một file JSON dùng chung đặt trong thư mục OneDrive vốn đã đồng bộ, và mỗi trình duyệt đọc ghi nó qua File System Access API.
- Gộp dữ liệu theo từng bản ghi và từng trường. Mỗi bản ghi mang dấu thời gian và người sửa, nên nếu tôi đổi giai đoạn của một khách hàng tiềm năng trong khi đồng nghiệp đổi người phụ trách, cả hai thay đổi đều được giữ. Xóa để lại một "bia mộ", nên bản ghi đã xóa trên máy này không sống lại ở lần đồng bộ sau.
- Công ty được chấm trên thang 100 theo tám tiêu chí có trọng số (độ khớp use case, mức cấp bách, độ ấm của quan hệ, tốc độ ra quyết định, tiềm năng doanh thu, khoảng cách địa lý, tính bổ trợ đối tác, rủi ro tự làm thay vì mua), với ngưỡng để được vào danh mục. Trọng số là phán đoán, không phải khớp từ kết quả, vì chưa có đủ thương vụ đã chốt để khớp. Tôi thà nói thẳng thế còn hơn bảo vệ chúng.

Đánh đổi: không có gì phải xin cấp, bảo mật hay trả tiền, và một người không phải kỹ sư có thể tự phát hành và bảo trì. Chi phí: vài giây biên dịch ở lần mở đầu, một sản phẩm đồng bộ file bị dùng như cơ sở dữ liệu, và không có xác thực thực sự. Đúng cho nhóm hai người. Bắt đầu khó chịu khi lên sáu.

## Chuyện gì đã hỏng

Lỗi đắt nhất không phải là sập. Có một thời gian, một lần lưu thất bại trông y hệt một lần lưu thành công, và công việc chỉ đơn giản biến mất ở lần tải lại sau. Cách sửa không có gì khéo: một dòng trạng thái ghi *Đã lưu mọi thay đổi* hoặc *Đang lưu…*, và một dải đỏ ngang đầu màn hình khi ghi thất bại. Không bao giờ để đường thất bại trông giống đường thành công.

Một lỗi nhỏ hơn: ngày tạo theo UTC bị lùi một ngày trong giờ mùa hè Na Uy. Giờ mọi hàm xử lý ngày đều chạy theo giờ địa phương.

## Cách tôi làm việc với nó

Đặc tả trước khi prompt. Sao lưu trước khi sửa, bằng các bản chụp có dấu thời gian. Build lại, chạy kiểm tra cú pháp, rồi dùng thử và xem thực sự hỏng ở đâu. Trợ lý viết phần lớn code. Tôi quyết định cấu trúc, đọc, kiểm thử và chịu trách nhiệm.

## Điều tôi sẽ đổi tiếp theo

Tách file 7.500 dòng thành các module để người khác có thể đóng góp. Biên dịch trước thay vì biên dịch trong trình duyệt. Thay đồng bộ file bằng backend thực sự. Và thêm định danh thật trước khi những người tôi chưa gặp bắt đầu sửa dữ liệu chung.

*Ứng dụng là nội bộ nên không có đường dẫn công khai, và tôi không chia sẻ nội dung pipeline hay các quan hệ thương mại.*
