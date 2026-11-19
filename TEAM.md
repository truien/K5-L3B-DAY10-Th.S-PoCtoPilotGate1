# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): `Th.S`
- Lớp: `L3B`
- Repo của bàn: [K5-L3B-DAY10-Th.S-PoCtoPilotGate1](https://github.com/truien/K5-L3B-DAY10-Th.S-PoCtoPilotGate1)
- Thẻ sự cố đã bốc: `S1`

## Thành viên

Nhóm gồm ba thành viên; leader chốt quyết định theo quyền được hai thành viên giao.

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
| 1 | Nguyễn Trọng Truyền | 2A202603868 | Sản phẩm và kinh doanh | Có |
| 2 | Nguyễn Văn Hùng | 2A202603816 | Kỹ sư cổng | |
| 3 | Trần Phạm Minh Sơn | 2A202603802 | Vận hành và pháp lý | |

Mỗi thành viên tự nộp cùng link repo trên LMS bằng tài khoản cá nhân.

## Cá nhân

Đóng góp dưới đây được tổng hợp từ tài liệu bàn giao, code và lịch sử repo. Exit ticket là bản nháp theo phần việc thực tế, cần từng thành viên đọc và chỉnh cho đúng phản ánh cá nhân trước khi nộp. Thông tin dùng AI cho bản soạn riêng ban đầu của Hùng/Sơn cần tác giả tự xác nhận; không suy từ công cụ leader dùng sang việc hai thành viên đã dùng.

## NguyenTrongTruyen-2A202603868

### Phần việc phụ trách

Leader, Sản phẩm và kinh doanh: A1/A3/A4/A5; B3/B6/B7.4/B8; C0/C1/C3.5/C12; config kinh doanh và hồ sơ nộp.

### Đóng góp cụ thể

- Chọn PRD/eval card Lab 9 dùng chung; chốt và ký tiêu chí trước đo.
- Tổng hợp bài Hùng/Sơn, đặt giới hạn kinh doanh, lưu bản vòng 1 và quyết định v1/v2 theo bằng chứng.
- Gom hồ sơ, đối chiếu report/manifest và đẩy lên repo nhóm.
- Dùng Codex hỗ trợ đọc mã/dữ liệu, soạn và rà phiếu, ghép bản bàn giao, chạy kiểm chứng và thao tác Git. Các ngưỡng và quyết định được leader chốt; nhóm cần giải thích được khi demo.

### Bằng chứng

`260f56d` (ký tiêu chí), `60a8d40` (v1), `1ec280b` (S1/v2); grade `R-S1-grade-20261119-201331-4e958b`; các mục phiếu nêu trên.

### Exit ticket

**Bản nháp để cá nhân tự rà:**
- Điều học được: phải đặt tiêu chí trước khi đo; tỷ lệ đúng cao không bù được tiền hoàn sai, lỗi hãng oan hoặc ROI chưa đạt.
- Điều còn chưa chắc: số đo từ MockLLM và bộ nhỏ có đại diện cho hiệu quả pilot thật, tải cao điểm và chi phí vận hành dài hạn hay không.

## NguyenVanHung-2A202603816

### Phần việc phụ trách

Kỹ sư cổng: A2/câu 1.3; B0–B2/B7.1–B7.3; C2/C5–C9; `lab10/guards.py`, `lab10/monitors.py`.

### Đóng góp cụ thể

- Thiết kế metric chọn policy; bàn giao baseline và phân tích `T-002@55`.
- Bàn giao G1–G3 vòng 1; bổ sung G4/G5 xử lý tracking thiếu, số khách khai mâu thuẫn và cap hãng đặt sai tầng.
- Bổ sung hai monitor không dùng nhãn, cây nguyên nhân và phần phân tích kỹ thuật của Phiếu C.
- Bản bàn giao được leader ghép/rà/chạy kiểm chứng với Codex hỗ trợ; tác giả tự bổ sung khai báo AI cho phần soạn riêng nếu có.

### Bằng chứng

`60a8d40`, `1ec280b`; grade `R-S1-grade-20261119-201331-4e958b`; S1 65/65, base 110/110; 13 public tests qua; C7–C9.

### Exit ticket

**Bản nháp để cá nhân tự rà:**
- Điều học được: guard chỉ kiểm lệnh ghi chưa bảo vệ được nhánh từ chối trước ghi; dữ liệu DB cũng cần kiểm đầy đủ và nhất quán.
- Điều còn chưa chắc: cách diễn đạt ngoài parser hiện tại, DB sai nhưng có vẻ đầy đủ và lỗi hiếm chưa được bộ test nhìn thấy bao phủ đến đâu.

## TranPhamMinhSon-2A202603802

### Phần việc phụ trách

Vận hành và pháp lý: A1/câu 1.2, A2/câu 1.4; B4/B5/B7.5/B7.6; C4/C10/C11; đề xuất phần `operations` và `legal`.

### Đóng góp cụ thể

- Soạn mục tiêu của kế toán/trưởng ca và telemetry tác động bên thứ ba.
- Soạn HAZOP, checklist có PIC, cấu hình nhân sự/pháp lý và runbook vòng 1.
- Bàn giao HAZOP S1, risk register và runbook 4–5; các trạng thái được đối chiếu lại với report thật khi ghép.
- Phần tài liệu được leader rà/ghép với Codex hỗ trợ; tác giả tự bổ sung khai báo AI cho bản soạn riêng nếu có.

### Bằng chứng

`b9934a4`, `60a8d40`, `1ec280b`; Phiếu B B4–B5/B7.5–B7.6; Phiếu C C4/C10/C11; grade chính thức ghi 0 ca ùn và các tác hại bằng 0 sau sửa.

### Exit ticket

**Bản nháp để cá nhân tự rà:**
- Điều học được: tăng người duyệt phải cập nhật cả công suất và tính lại chi phí; cap lỗi theo ngày không chứng minh được giới hạn hợp đồng 7 ngày.
- Điều còn chưa chắc: tải dồn thực tế, độ trễ dữ liệu POD và cách phối hợp cảnh báo/đối soát giữa các bên khi pilot có người dùng thật.
