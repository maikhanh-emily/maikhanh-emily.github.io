---
title: Tự xây CRM khi không có kỹ sư
subtitle: Ứng dụng web vận hành toàn bộ pipeline phát triển kinh doanh của một start-up, do tôi tự làm cùng các trợ lý lập trình AI
period: 6/2026 – nay
year: 2026
role: Tự thiết kế, tự xây và chịu trách nhiệm
org: Planck Technologies AS
tags: [Làm cùng AI, Phần mềm, Phát triển kinh doanh]
featured: true
order: 1
status: Đang dùng hằng ngày
summary: Pipeline thương mại của Planck từng nằm trong một file bảng tính. Tôi đã tự làm một ứng dụng web để thay thế nó, bằng Claude Code và không có kỹ sư nào hỗ trợ. Cả nhóm hiện làm việc trên đó mỗi ngày.
art_caption: "Sơ đồ minh họa bảng pipeline: các công ty đi qua từng giai đoạn, công ty nào cũng có điểm phù hợp, và một dòng trạng thái báo rõ mỗi lần lưu. Không có dữ liệu thật trong hình."
---
## Vấn đề

Planck Technologies là một start-up deep-tech ở Na Uy, dùng AI để thiết kế vật liệu thu giữ CO₂. Các kỹ sư ở đây dồn sức cho nền tảng khám phá vật liệu, vì đó mới là sản phẩm chính. Không ai rảnh để làm công cụ nội bộ, nên pipeline thương mại cứ nằm trong mấy file bảng tính, và file nào cũng lệch đi ngay khi có hai người cùng sửa.

## Tôi đã xây gì

Một CRM nội bộ cho pipeline khách hàng, rồi sau đó thêm một cái nữa cho nhà đầu tư. Mỗi công ty được đưa vào hệ thống qua điểm phù hợp, đi qua các giai đoạn, kèm theo đầu mối liên hệ, ghi chú và nhật ký hoạt động. Tất cả đổ về các màn hình dashboard, pipeline, tiếp cận và báo cáo. Báo cáo tuần gửi ban lãnh đạo cũng xuất thẳng từ đây. Về quy mô: hơn 500 tổ chức đã được sàng lọc, khoảng 60 tổ chức đang được theo sát.

## Cách nó hoạt động

Kiến trúc của nó hơi lạ, và tôi cố tình làm vậy.

- Một ứng dụng React viết gọn trong một file JSX duy nhất, được một script Python biên dịch thành một file HTML chạy độc lập. Không Node, không npm, không server. Ai cần dùng chỉ việc nhấp đúp để mở.
- Dữ liệu lưu ngay trong trình duyệt. Khi dùng chung cả nhóm, một file JSON được đặt trong thư mục OneDrive vốn đã đồng bộ sẵn, và trình duyệt của từng người đọc, ghi vào đó qua File System Access API.
- Dữ liệu được gộp theo từng bản ghi và từng trường. Bản ghi nào cũng lưu thời điểm sửa và người sửa, nên nếu tôi đổi giai đoạn của một khách hàng tiềm năng đúng lúc đồng nghiệp đổi người phụ trách, cả hai thay đổi đều được giữ lại. Khi xóa, hệ thống để lại một dấu đánh dấu (tombstone), để bản ghi đã xóa trên máy này không sống lại ở lần đồng bộ sau.
- Mỗi công ty được chấm trên thang 100 theo tám tiêu chí có trọng số (mức độ phù hợp với use case, độ cấp bách, mức độ thân quen, tốc độ ra quyết định, tiềm năng doanh thu, khoảng cách địa lý, khả năng bổ trợ khi làm đối tác, rủi ro họ tự làm thay vì mua), và phải đạt một ngưỡng nhất định mới được vào danh mục. Các trọng số này do tôi cân nhắc chứ không được rút ra từ kết quả thực tế, vì khi đó chưa có đủ thương vụ đã chốt để làm việc đó. Tôi thà nói thẳng như vậy còn hơn cố bảo vệ chúng.

Cái được là không phải xin cấp, bảo mật hay trả tiền cho thứ gì, và một người không phải kỹ sư vẫn có thể tự phát hành, tự bảo trì. Cái mất là vài giây biên dịch ở lần mở đầu, một dịch vụ đồng bộ file bị dùng thay cơ sở dữ liệu, và không có xác thực thực sự. Với nhóm hai người thì vừa đủ. Lên đến sáu người là bắt đầu thấy vướng.

## Những chỗ đã hỏng

Lỗi đắt giá nhất không phải là một cú sập. Có một thời gian, lần lưu thất bại trông y hệt lần lưu thành công, và công việc cứ thế biến mất ở lần tải lại trang tiếp theo. Cách sửa chẳng có gì cao siêu: một dòng trạng thái báo *Đã lưu mọi thay đổi* hoặc *Đang lưu…*, và một dải đỏ chạy ngang đầu màn hình mỗi khi ghi thất bại. Đừng bao giờ để một thất bại trông giống một thành công.

Một lỗi nhỏ hơn: ngày tháng tính theo UTC bị lùi mất một ngày trong giờ mùa hè ở Na Uy. Giờ mọi hàm xử lý ngày đều chạy theo giờ địa phương.

## Tôi làm việc với nó ra sao

Mô tả rõ yêu cầu trước khi prompt. Sao lưu trước khi sửa, bằng các bản sao có ghi thời gian. Build lại, chạy kiểm tra cú pháp, rồi tự dùng thử để xem thực sự hỏng ở đâu. Trợ lý AI viết phần lớn code. Còn tôi quyết định cấu trúc, đọc lại, kiểm thử và chịu trách nhiệm về nó.

## Nếu làm tiếp, tôi sẽ đổi gì

Tách file 7.500 dòng thành các module để người khác có thể tham gia. Biên dịch sẵn thay vì biên dịch trong trình duyệt. Thay cơ chế đồng bộ file bằng một backend thực sự. Và thêm định danh người dùng đàng hoàng, trước khi những người tôi chưa từng gặp bắt đầu sửa dữ liệu chung.

*Ứng dụng chỉ dùng nội bộ nên không có đường link công khai, và tôi không chia sẻ nội dung pipeline hay các mối quan hệ thương mại.*
