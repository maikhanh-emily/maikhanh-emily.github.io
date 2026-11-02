---
title: Tự xây dựng CRM mà không cần kỹ sư
subtitle: Ứng dụng web quản lý pipeline phát triển kinh doanh của một start-up, do tôi tự xây dựng với sự hỗ trợ của công cụ lập trình AI
period: 6/2026 – nay
year: 2026
role: Thiết kế, xây dựng và phụ trách chính
org: Planck Technologies AS
tags: [Làm cùng AI, Phần mềm, Phát triển kinh doanh]
featured: true
order: 1
status: Đang được sử dụng hằng ngày
summary: Pipeline thương mại của Planck trước đây nằm trong một file bảng tính. Tôi đã xây dựng một ứng dụng web để thay thế với sự hỗ trợ của Claude Code, không có kỹ sư giúp sức. Cả nhóm hiện dùng ứng dụng này mỗi ngày.
art_caption: "Minh họa bảng pipeline: mỗi công ty có điểm đánh giá riêng và đi qua từng giai đoạn, còn dòng trạng thái cho biết dữ liệu đã được lưu hay chưa. Hình không chứa dữ liệu thật."
---
## Vấn đề

Planck Technologies là một start-up deep-tech ở Na Uy, ứng dụng AI vào thiết kế vật liệu thu giữ CO₂. Đội kỹ sư tập trung vào nền tảng khám phá vật liệu, tức sản phẩm chính của công ty, nên không ai có thời gian làm công cụ nội bộ. Pipeline thương mại vì vậy nằm trong các file bảng tính, và dữ liệu nhanh chóng bị lệch khi có hai người cùng sửa.

## Tôi đã xây dựng gì

Một CRM nội bộ cho pipeline khách hàng, và sau đó thêm một CRM thứ hai cho nhà đầu tư. Mỗi công ty được chấm điểm mức độ phù hợp, rồi đi qua các giai đoạn, kèm thông tin liên hệ, ghi chú và lịch sử hoạt động. Dữ liệu được hiển thị trên các màn hình dashboard, pipeline, tiếp cận khách hàng và báo cáo. Báo cáo tuần cho ban lãnh đạo được xuất trực tiếp từ đây. Về quy mô: hơn 500 tổ chức đã được sàng lọc, khoảng 60 tổ chức đang được theo dõi.

## Cách hoạt động

Cách xây dựng ứng dụng này khá khác thường, và đó là lựa chọn có chủ đích.

- Ứng dụng React được viết trong một file JSX duy nhất, rồi được một script Python biên dịch thành một file HTML độc lập. Không cần Node, npm hay server, người dùng chỉ cần nhấp đúp để mở.
- Dữ liệu được lưu trong trình duyệt. Để dùng chung, cả nhóm có một file JSON đặt trong thư mục OneDrive, và trình duyệt của mỗi người đọc, ghi file này qua File System Access API.
- Khi đồng bộ, dữ liệu được gộp theo từng bản ghi và từng trường. Mỗi bản ghi lưu lại thời gian sửa và người sửa, nên nếu tôi đổi giai đoạn của một khách hàng tiềm năng trong lúc đồng nghiệp đổi người phụ trách, cả hai thay đổi đều được giữ. Bản ghi đã xóa vẫn để lại một dấu (tombstone), nhờ vậy sẽ không xuất hiện lại ở lần đồng bộ sau.
- Mỗi công ty được chấm trên thang 100 theo tám tiêu chí có trọng số (mức độ phù hợp với nhu cầu, mức độ cấp bách, mức độ quen biết, tốc độ ra quyết định, tiềm năng doanh thu, khoảng cách địa lý, khả năng bổ trợ khi hợp tác, rủi ro khách hàng tự làm thay vì mua), và phải đạt một ngưỡng nhất định mới được đưa vào danh mục. Trọng số là do tôi đánh giá chủ quan, không phải ước lượng từ dữ liệu, vì chưa có đủ thương vụ đã chốt để làm việc đó. Tôi nghĩ nói rõ điều này tốt hơn là cố biện minh cho chúng.

Ưu điểm là không phải cài đặt, quản lý bảo mật hay trả phí cho hệ thống nào, và người không phải kỹ sư vẫn có thể tự phát hành và bảo trì. Đổi lại, lần mở đầu mất vài giây để biên dịch, dịch vụ đồng bộ file phải đóng vai trò cơ sở dữ liệu, và ứng dụng chưa có cơ chế xác thực thực sự. Cách này phù hợp với nhóm hai người, nhưng đến sáu người thì bắt đầu có vấn đề.

## Những lỗi đã gặp

Lỗi gây hậu quả lớn nhất không phải là ứng dụng bị sập. Có một thời gian, lần lưu thất bại trông giống hệt lần lưu thành công, nên dữ liệu vừa nhập mất hẳn sau khi tải lại trang. Cách sửa khá đơn giản: một dòng trạng thái hiển thị *Đã lưu mọi thay đổi* hoặc *Đang lưu…*, và một thanh cảnh báo màu đỏ ở đầu màn hình khi lưu thất bại. Bài học là lỗi phải luôn được hiển thị rõ ràng, không được trông như đã thành công.

Một lỗi nhỏ hơn: ngày tháng tính theo giờ UTC bị lùi mất một ngày trong giờ mùa hè ở Na Uy. Hiện tất cả các hàm xử lý ngày đều dùng giờ địa phương.

## Cách tôi làm việc

Viết rõ yêu cầu trước khi đưa cho AI. Sao lưu trước khi sửa, mỗi bản đều ghi thời gian. Sau khi build lại, tôi chạy kiểm tra cú pháp rồi tự dùng thử để tìm lỗi thực tế. AI viết phần lớn code, còn tôi quyết định cấu trúc, đọc lại, kiểm thử và chịu trách nhiệm về kết quả.

## Nếu phát triển tiếp

Tách file 7.500 dòng thành các module để người khác có thể tham gia phát triển. Biên dịch sẵn thay vì biên dịch trên trình duyệt. Thay cơ chế đồng bộ file bằng một backend thực sự. Và bổ sung đăng nhập, phân quyền trước khi có thêm những người dùng mới cùng sửa dữ liệu chung.

*Ứng dụng chỉ dùng nội bộ nên không có link công khai, và tôi không chia sẻ dữ liệu pipeline hay thông tin về các đối tác thương mại.*
