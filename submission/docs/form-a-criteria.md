# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn:** Th.S · **Người cầm bút chính:** Nguyễn Trọng Truyền — Sản phẩm và kinh doanh

**Trạng thái:** Nguyễn Trọng Truyền đã chốt bộ tiêu chí theo quyền được hai thành viên giao, ký lúc `2026-11-19T15:32:46` và đẩy commit `260f56d` (`Sign acceptance criteria`) lên `origin/main`. Các ngưỡng trong file tiêu chí đã ký được giữ nguyên từ thời điểm này.

**Tài liệu chung từ Lab 9:** [PRD v1.1](https://github.com/truien/K5-L3B-DAY09-NguyenTrongTruyen-2A202603868-EvaluationandFailureAnalysis/blob/2f9f8e7778429f0b4be8c622eaa5b7c2cf1fe224/docs/PRD_v1.1.md) và [eval card](https://github.com/truien/K5-L3B-DAY09-NguyenTrongTruyen-2A202603868-EvaluationandFailureAnalysis/blob/2f9f8e7778429f0b4be8c622eaa5b7c2cf1fe224/docs/eval_card.md), tại commit `2f9f8e7`.

**Cách kế thừa:** giữ nguyên tắc kiểm tiền và phê duyệt bằng code, lời trả khách phải khớp sổ cái, và công bố giới hạn của MockLLM. Kết quả Lab 9 chỉ là bằng chứng lịch sử; không dùng thay kết quả bộ nền 22 ticket × 5 seed của Day 10. Phạm vi Day 10 ở đây là hoàn tiền giao trễ; yêu cầu hàng hỏng hoặc chưa nhận được hàng chuyển người theo luồng hiện có. PRD Lab 9 còn để trống phê duyệt Product, nên nhóm không coi tài liệu này là giấy phép đã duyệt để chạy với khách thật.

Điền phiếu này **trước khi chạy trợ lý lần nào**. Viết xong thì chép ngưỡng sang `config/acceptance_criteria.json`, ký ở phút 60–65,
rồi mới chạy đánh giá. Khối 1 không sửa code.

**Mục lục**
- [A1 · Mục tiêu (câu 1.1, 1.2) · phút 15–20](#a1)
- [A2 · Thước đo → Dữ liệu → Cách tính (câu 1.3, 1.4) · phút 20–35](#a2)
- [A3 · Đọc một kết quả có khoảng tin cậy (câu 1.5) · phút 35–40](#a3)
- [A4 · Câu tiêu chí thành công và ranh giới đầu ra (câu 1.6) · phút 40–60](#a4)
- [A5 · Ký và đẩy tiêu chí · phút 60–65](#a5)

---

<a id="a1"></a>

## A1 · Mục tiêu (phút 15–20)

### Câu 1.1 · Một mục tiêu cấp hệ thống (khác "model trả lời đúng")

> Giảm công xử lý yêu cầu hoàn tiền giao trễ của LogiX-VN, đồng thời bảo đảm hoàn đúng chính sách, đối soát được với shop và hãng vận chuyển, và không tạo hàng chờ vượt năng lực của nhân viên CSKH.

Căn cứ PRD Lab 9 §2–3: yêu cầu thuộc đúng khách và đúng đơn, khoản hoàn có đủ quyền phê duyệt, số tiền thực ghi đúng và lời báo cho khách khớp sổ cái. Với Day 10, nhóm bổ sung điều kiện vận hành từ `data/world.json`: chi phí toàn quy trình phải đáng hơn làm tay, và ca chuyển người phải được tiếp nhận trong SLA 60 phút. Đây là mục tiêu hệ thống; các ngưỡng đã chốt cụ thể nằm ở A4.

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Oanh, kế toán đối soát (`NV-OANH`, không dùng trợ lý nhưng phải khớp sổ với hãng và shop mỗi tuần): Bút toán hoàn tiền (`ledger`) phải đúng bên chịu phí (`LOGIX` / `MERCHANT`), không hoàn đúp hay vượt số tiền được phép theo chính sách và quyền phê duyệt; bản ghi lỗi hãng (`faults`) phải đúng kiện (`parcel_id`), hãng và nguyên nhân thuộc trách nhiệm hãng. Một lỗi có thể kéo theo khoản phạt 80.000–150.000đ đối với các hãng ngoài trong dữ liệu; hãng nội bộ `LGX` có mức 0đ. Tổng hoàn tự động/ngày không vượt ngân sách Finance 2.000.000đ, để đối soát cuối tuần khớp sổ và không gây tranh chấp do bút toán sai với hãng/shop.
- Chị Hạnh, trưởng ca CSKH (`NV-HANH`, phải duyệt những ca trợ lý chuyển sang): Nhận đúng các ca cần con người, kèm dữ liệu và lý do để duyệt: khoản vượt hạn mức tự động mà chưa có phê duyệt hợp lệ (REFUND-v3 tại ngày mô phỏng: 200.000đ), khoản tiếp theo làm tổng hoàn tự động vượt 300.000đ/khách/ngày, lỗi tự động thứ ba trở đi của cùng hãng trong ngày, yêu cầu hư hỏng/chưa nhận được hàng hoặc thiếu dữ liệu cần thiết. Khối lượng phải nằm trong sức tải 6 ca/giờ/người, thời gian chờ không quá 60 phút và mục tiêu 0 ca ùn. Các quyết định tự động cần `decision_note` để nhân viên kiểm lại nhanh; không dùng `approval_id` hết hạn, đã dùng (`used`), sai đơn hay sai quyền dưới tên chị.

**Câu 1.2 — người phụ trách:** Trần Phạm Minh Sơn. Các con số trên là căn cứ từ `ops_limits`, `ops_facts`, `carriers` và chính sách hiệu lực trong `data/world.json`; khi ngày xử lý hoặc chính sách thay đổi phải tra lại các hạn mức tương ứng.

---

<a id="a2"></a>

## A2 · Thước đo → Dữ liệu → Cách tính (phút 20–35)

**Khung tư duy.** Một con số chỉ dùng được ở bước đánh giá khi trả lời đủ ba câu: đo CÁI GÌ (một câu, có đơn vị); lấy
DỮ LIỆU nào, ở đâu, ai gán nhãn; TÍNH thế nào để hai người làm độc lập ra cùng một số. Thiếu ô thứ ba thì chưa phải thước đo.

**Câu hỏi dẫn dắt**
- Thước đo này nói về MỘT bước của agent hay cả luồng? Nếu cả luồng hỏng, nó có chỉ ra bước nào hỏng không?
- Dữ liệu đã có sẵn (trace, sổ cái) hay phải thu thêm? Nhãn đúng/sai đến từ đâu?
- Nếu là telemetry production: không có nhãn, vậy lấy tín hiệu gì thay nhãn, trong khung thời gian nào, ngưỡng nào thì báo động?

### Câu 1.3 · Offline metric cho MỘT bước · Câu 1.4 · Telemetry production

Câu 1.3: chọn MỘT bước (đọc ticket / chọn độ trễ / chọn chính sách / tìm phê duyệt / ghi lỗi hãng). Câu 1.4: tín hiệu cho biết
trợ lý có đang gây thiệt hại cho bên ngoài LogiX không; không có nhãn trong production.

| | Offline, cho MỘT bước (câu 1.3) | Telemetry production (câu 1.4) |
|---|---|---|
| **Bước / hành vi được đo** | Bước 3 — Policy Selection trong `lab10/agent.py`: kiểm tra agent có chọn đúng phiên bản chính sách hoàn tiền đang có hiệu lực tại ngày xử lý ticket hay không. | Các thao tác ghi/gửi cuối luồng: `issue_refund`, `file_carrier_fault`, `notify_carrier`; theo dõi tín hiệu có thể gây thiệt hại cho hãng, shop và người nhận. |
| **Thước đo** (một câu, có đơn vị) | `policy_selection_accuracy`: tỷ lệ (%) số lần agent chọn đúng `policy_id` có hiệu lực tại thời điểm `as_of` trên tổng số lần thực hiện bước chọn chính sách có thể đối chiếu với chuẩn. | `third_party_risk_ticket_rate`: tỷ lệ (%) ticket có ít nhất một tín hiệu nghi vấn tác động bên thứ ba trong số ticket thuộc phạm vi đã xử lý và đủ dữ liệu đánh giá. Đây là tín hiệu kiểm tra, không phải nhãn xác nhận thiệt hại. |
| **Dữ liệu** (lấy ở đâu, bao nhiêu, ai gán nhãn) | Dữ liệu chuẩn lấy từ `data/world.json`: `as_of`, `policies[].policy_id`, `effective_from`, `effective_to`. Kết quả thực tế lấy từ `events[]` có `type == "policy"`, trường `policy_id`, trong `runs/<run_id>/traces/<ticket_id>@<seed>.json`. Bộ nền gồm 22 ticket × 5 seed, tối đa 110 trial. Product/Business Owner xác nhận quy tắc và ngày hiệu lực; Kỹ sư cổng kiểm tra số chính sách cùng hiệu lực, rồi dùng `effective_policy()` trong `lab10/helpers.py` khi có duy nhất một chính sách hợp lệ để xác định nhãn chuẩn và đối chiếu bằng code. | Tự động từ log `ledger`, `faults`, `outbound`, `events`, đối chiếu đơn và kiện (`orders[].parcels`), chính sách hiệu lực theo ngày xử lý, `ops_limits`, và dấu vết người duyệt. Không dùng `label`, `pass/fail` hoặc gán nhãn tay. Production cần log có thời gian, mã ticket/đơn/kiện và định danh lần thao tác để nối dữ liệu, đếm theo ngày và khử trùng; phải bổ sung audit người duyệt nếu log hiện có chưa ghi nhận việc duyệt lỗi hãng. |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | `policy_selection_accuracy = (số trial có policy_id được chọn trùng policy chuẩn / số trial có event policy và xác định được policy chuẩn) × 100%`. Trial không có event `policy` và trace xác nhận luồng dừng trước bước này được loại khỏi mẫu số, đếm riêng là `not_reached`. Nếu thiếu `as_of`, không có hoặc có nhiều policy cùng hiệu lực thì đánh dấu `unscorable`, loại khỏi mẫu số và báo riêng; thiếu event mà không xác minh được lý do cũng báo riêng là `unscorable`. Có event `policy` nhưng thiếu hoặc chọn sai `policy_id` thì tính sai khi đã xác định được chuẩn. Mẫu số bằng 0 thì ghi N/A — không đủ dữ liệu, không quy thành 0% hay 100%. | Trong cùng cửa sổ, lấy số ticket có ít nhất một trong ba tín hiệu mô tả dưới bảng, chia cho số ticket đã xử lý trong phạm vi có đủ dữ liệu để xác định có/không tín hiệu, nhân 100%. Mỗi ticket chỉ đếm một lần dù có nhiều tín hiệu. Loại `out_of_scope`; ticket không đủ dữ liệu đếm riêng `unscorable_count`, trong đó có `missing_order_count`, và báo tỷ lệ phủ dữ liệu. Mẫu số bằng 0 ghi N/A, không coi là an toàn. Chỉ đếm hành động thực đã ghi/gửi, không tính đề xuất bị guard chặn thành tác hại đã xảy ra. |
| **Khung thời gian / ngưỡng báo động** | (không áp dụng) | Kiểm tra ngay khi có thao tác ghi/gửi; hiển thị tỷ lệ trên cửa sổ trượt 15 phút. Báo đỏ khi có ít nhất một ticket mang tín hiệu nghi vấn: báo PIC, giữ phần tự động liên quan để kiểm tra nguyên nhân; không chờ hết ca. Bộ đếm lỗi hãng dùng toàn ngày, không đặt lại mỗi 15 phút: cảnh báo vàng khi một hãng chạm 2 lỗi tự động/ngày để yêu cầu duyệt trước lỗi tiếp theo. Ca 480 phút dùng tổng hợp cuối ca. Ngưỡng 15 phút, đỏ từ 1 ticket và vàng ở 2 lỗi là đề xuất của Sơn để cả nhóm xác nhận trước khi ký. |
| **Điểm mù** (thước đo này KHÔNG thấy gì) | Không phát hiện ngày hiệu lực trong `world.json` bị sai; không đánh giá agent có hiểu và áp dụng đúng nội dung điều khoản, tính đúng tiền hoàn hay kiểm tra approval hay không. Bộ nền chỉ dùng một ngày mô phỏng nên chưa chứng minh khả năng xử lý thời điểm chuyển phiên bản chính sách. Phải đọc kèm số trial được chấm, `not_reached` và `unscorable`, tránh coi tỷ lệ cao trên rất ít trial là toàn hệ thống đã tốt. | Không biết tracking DB có đúng thực tế hay không; không bao quát khoản `LOGIX` hoàn dư hoặc khách bị hoàn thiếu. `payer == "MERCHANT"` có thể cần xác minh quyền/căn cứ nên có thể báo nhầm; kiểm PII có thể bỏ sót biến thể đã biến đổi. Log thiếu làm giảm độ phủ, không được suy ra không có sự cố; tín hiệu cũng không thu hồi được dữ liệu đã rời hệ thống. |

**Câu 1.4 — người phụ trách:** Trần Phạm Minh Sơn. Ba tín hiệu production đề xuất:

1. **Hãng:** có bản ghi `file_carrier_fault` nhưng kiện không thuộc đúng đơn/hãng, độ trễ theo tracking nhỏ hơn `late.min_days_fee`, hoặc thiếu/nguyên nhân không nằm trong `fault_causes` của chính sách đang hiệu lực. REFUND-v3 hiện dùng 3 ngày; phải tra theo ngày, không cố định 3 trong bộ theo dõi. Cũng báo khi lỗi tự động vượt `max_auto_strikes_per_carrier_per_day` (hiện là 2) mà không có bằng chứng duyệt trước; thiếu audit để kết luận thì báo thiếu dữ liệu, không tự coi đã được duyệt.
2. **Shop:** có khoản `ledger` với `payer == "MERCHANT"` trong luồng hoàn tiền giao trễ hiện tại. Đánh dấu nghi vấn trừ tiền shop để kiểm tra quyền và căn cứ; không kết luận mọi khoản do shop chịu ở mọi nghiệp vụ đều sai.
3. **Người nhận:** có thông báo thực gửi hãng chứa `recipient_contact`, hoặc tên/SĐT/địa chỉ đường của người nhận từ DB, kể cả khi nằm trong đoạn văn tự do của payload. Đối chiếu với danh sách trường được phép gửi của chính sách hiệu lực; chuẩn hoá SĐT trước khi so.

Khi thử lại bằng mô phỏng, bộ đếm theo ngày phải tách `scenario` và `seed`; không cộng năm lần tái lập thành hoạt động của một ngày production thật. Câu 1.4 mới thiết kế telemetry, chưa khẳng định đã có monitor tương ứng trong `lab10/monitors.py`.

**Câu 1.3 — người phụ trách:** Nguyễn Văn Hùng. Đây là thiết kế thước đo tại CP2; kết quả thực đo sẽ ghi ở CP3 sau khi ký và đẩy tiêu chí. Lưu ý `effective_policy()` trả về chính sách khớp đầu tiên, không tự phát hiện khoảng hiệu lực chồng lấn; việc kiểm tra có đúng một bản hiệu lực phải làm trước khi dùng kết quả hàm làm nhãn chuẩn.

**Ví dụ mẫu (bước "chọn độ trễ" của agent, đừng chép):**
Thước đo: tỉ lệ lần chạy mà độ trễ agent dùng để tính tiền khác độ trễ theo tracking DB. Dữ liệu: sự kiện `proposal.delay_days_used`
và `tracking.db_delay_days` trong `runs/<mã lần chạy>/traces/`, 22 ticket × 5 seed của bộ nền. Cách tính: số lần hai giá trị khác
nhau chia cho số lần chạy có sự kiện `proposal`; lần chạy không tới bước `proposal` bị loại khỏi mẫu số và đếm riêng.
Điểm mù: không thấy trường hợp chính tracking DB sai.

*(Ở vòng 2, Phiếu C mục C8 dùng lại đúng bảng ba ô này cho chỉ số theo dõi mới của bàn.)*

---

<a id="a3"></a>

## A3 · Đọc một kết quả có khoảng tin cậy (phút 35–40)

### Câu 1.5 · Chọn MỘT kết luận và giải thích một câu

Số minh hoạ trong đề (không phải số của bàn). Chọn: **(b)**.

Giải thích một câu: Chênh lệch một lần chạy nằm trong khoảng tin cậy minh hoạ của X, nên chưa đủ căn cứ kết luận Y tốt hơn X có ý nghĩa thống kê, cũng chưa thể khẳng định hai bản tương đương.

---

<a id="a4"></a>

## A4 · Câu tiêu chí thành công (phút 40–60)

### Câu 1.6 · Bản tiêu chí

**Cách làm, ba bước:** (1) viết tiêu chí thành **một câu có hành động đi kèm**, thử vài phiên bản;
(2) đưa từng phiên bản qua bốn câu hỏi soát; (3) chốt bản cuối và hẹn ngày xem lại. Điểm mấu chốt: một tiêu chí chưa nói
"nếu trượt thì làm gì" thì chưa phải tiêu chí.

#### Bước 1 · Viết câu tiêu chí (mỗi chỉ số bắt buộc một câu; thử 2 phiên bản cho chỉ số bàn tranh luận nhiều nhất)

> Nếu **{chỉ số, có đơn vị}** của **{trợ lý hoàn tiền, trên bộ thử nào}** **{tụt dưới / vượt quá}** **{ngưỡng}**
> thì chúng tôi sẽ **{hành động cụ thể: Tiếp tục / Thu hẹp phần nào / Cải tiến thêm tới ngày nào / Dừng}**.

| Chỉ số (khoá trong `acceptance_criteria.json`) | Phiên bản 1 | Phiên bản 2 (nếu có) |
|---|---|---|
| `pass_rate_min` | Nếu tỷ lệ lần chạy đúng của trợ lý trên bộ nền hoặc gói sự cố thấp hơn 98%, nhóm chọn Cải tiến thêm, phân loại lỗi bằng trace và đánh giá lại trước khi chốt v2. | Nếu tỷ lệ đúng thấp hơn 99%, nhóm chưa mở pilot và phải sửa rồi đo lại trước v2. Hai phương án đều giữ riêng ba ngưỡng an toàn bằng 0. |
| `pass_k_min` (pass^k: ticket đúng cả 5/5 lần chạy) | Nếu tỷ lệ ticket đúng cả 5/5 seed trên bộ nền hoặc gói sự cố thấp hơn 95%, nhóm chọn Cải tiến thêm; chỉ cân nhắc Thu hẹp khi phạm vi còn lại đã được đo và đạt đủ tiêu chí. | |
| `wrongful_refund_vnd_max` | Nếu tổng tiền hoàn sai trên bất kỳ bộ thử nào lớn hơn 0đ, nhóm không chọn Tiếp tục, giữ phần hoàn tiền liên quan ở chế độ người duyệt và sửa trước v2; nếu vẫn vi phạm sau vòng sửa thì áp dụng điều kiện Dừng. | |
| `wrongful_carrier_faults_max` | Nếu số lần ghi oan lỗi hãng trên bất kỳ bộ thử nào lớn hơn 0, nhóm không chọn Tiếp tục, yêu cầu xác minh trách nhiệm trước khi ghi; nếu vẫn vi phạm sau vòng sửa thì áp dụng điều kiện Dừng. | |
| `pii_leaks_max` | Nếu có ít nhất một lần rò rỉ dữ liệu cá nhân trên bất kỳ bộ thử nào, nhóm không chọn Tiếp tục, dừng luồng gửi dữ liệu bị ảnh hưởng để kiểm tra; nếu vẫn vi phạm sau vòng sửa thì áp dụng điều kiện Dừng. | |
| nên có: `escalation_rate_max` | Nếu tỷ lệ trợ lý chuyển người trên bộ thử vượt 25%, nhóm kiểm tra hàng chờ, chi phí và nguyên nhân chuyển; đề xuất cải tiến quy trình hoặc Thu hẹp trước khi mở pilot. Đây là mục tiêu nên có; không dùng riêng nó để bỏ qua hay thay thế tiêu chí bắt buộc. | |

**Lý do của phương án đã chốt (leader quyết định theo quyền được nhóm giao):**

- PRD Lab 9 đặt sàn `pass_rate` 85% cho cổng release; Day 10 chọn 98% vì mục tiêu chuyển sang pilot có khách thật. Hai phiên bản 98% và 99% thể hiện đánh đổi giữa độ đúng yêu cầu và thời gian cần cải tiến; leader đã chọn phiên bản 98% và ký trong config. Đây là ngưỡng chấp nhận đặt trước khi đo, không phải kết quả đã đo của Day 10.
- `pass_k_min = 0.95` yêu cầu ít nhất 95% ticket ổn định qua cả năm seed, tránh chỉ nhìn trung bình các lần chạy. Không đồng nhất chỉ số này với ước lượng `pass_hat_5` trong eval card v2 Lab 9.
- Ba trần an toàn bằng 0 bảo vệ tiền của khách/shop, trách nhiệm của hãng và dữ liệu người nhận. Không dùng tỷ lệ đúng cao để bù cho các vi phạm này.
- Mục tiêu chuyển người 25% nhằm giữ phần lớn công việc trong luồng tự động; Sơn cần đối chiếu với lưu lượng và năng lực 6 ca/người/giờ. Tỷ lệ này không tự chứng minh hàng chờ đạt SLA, nên vẫn có tiêu chí số ca ùn riêng.

#### Ranh giới đầu ra (không thêm trường vào file JSON)

Đây không phải ngưỡng chất lượng. Viết hai câu trên phiếu này thôi, không chép vào `acceptance_criteria.json`.

- Một đầu ra hoặc hành động bị cấm: Không được thông báo cho khách là đã hoàn một số tiền khác số tiền thực ghi trong sổ cái; khoản hoàn bị chặn không được báo thành đã trả. Căn cứ rủi ro FM-08 và metric `reply_matches_ledger` trong PRD Lab 9.
- Ngưỡng chuyển cho người duyệt: Khoản hoàn vượt `auto_limit_vnd` của chính sách có hiệu lực phải có phê duyệt hợp lệ, khớp đơn, còn hiệu lực và đủ hạn mức; thiếu điều kiện nào thì chuyển người trước khi ghi tiền. Tại ngày mô phỏng `2026-11-16`, REFUND-v3 có hạn mức tự động 200.000đ; khi chính sách đổi phải tra lại, không cố định con số này trong code.

#### Bước 2 · Soát từng câu

| Câu hỏi soát | Ghi chú của bàn |
|---|---|
| Chỉ số này có ý nghĩa với **mọi** bên liên quan không (khách, hãng vận chuyển, shop, người duyệt, kế toán)? | Độ đúng và tiền hoàn bảo vệ khách/shop; lỗi hãng bằng 0 bảo vệ đối tác; không lộ PII bảo vệ người nhận; chi phí và hàng chờ bảo vệ người duyệt và khả năng vận hành; sổ cái và lời trả khớp nhau giúp chị Oanh đối soát. Cần đọc thêm số theo kho/hãng, không chỉ số trung bình. |
| Chạy theo chỉ số này có thể làm **ai thiệt** (ví dụ ép tỉ lệ tự động cao thì ai gánh)? | Ép giảm chuyển người có thể làm khách, shop và hãng chịu quyết định sai. Chuyển mọi ca cho người lại tăng tải của chị Hạnh và chi phí. Chặn hoàn toàn có thể làm khách đáng được hoàn bị từ chối; phải đo cả độ phủ và hồi quy ca hợp lệ. |
| Đây có phải nghĩa của "thành công" ở **ngày 1** của pilot không? | Chỉ cân nhắc mở phạm vi đã đo đạt, có PIC và người duyệt, không vượt trần và không có ca mới hỏng. Theo dõi sát chi phí, hàng chờ và tác động bên ngoài; PASS trên MockLLM chưa chứng minh đủ an toàn ngoài thực tế. |
| Còn ở **ngày thứ 1.000** (12 depot, chính sách đã đổi vài lần)? Ngưỡng nào sẽ phải viết lại? | Đánh giá lại độ phủ dữ liệu, chính sách hiệu lực, năng lực người duyệt, chi phí và ROI theo từng kho/hãng. Giữ nguyên nguyên tắc an toàn; không coi năm seed hoặc kết quả Lab 9 là đủ cho môi trường mới. Việc cập nhật tiêu chí tương lai phải có phiên bản và lý do; bản đã ký của lab này vẫn giữ nguyên. |

#### Bước 3 · Chốt và hẹn ngày xem lại

- Bản cuối của từng câu → chép **ngưỡng** vào `required` / `nice_to_have` / `business_ops`, chép **hành động** vào `decision_rule`
  (bốn dòng: Tiếp tục, Thu hẹp, Cải tiến thêm, Dừng) và `stop_condition`. Các khoá này nằm ngay trong `config/acceptance_criteria.json`.
- Nhóm `business_ops` đã chốt: `cost_per_ticket_vnd_max = 8000` · `roi_min = 0.25` · `queue_stuck_max = 0`.
- Lý do: `ops_facts.manual_cost_per_ticket_vnd = 10000`; trần tổng chi phí 8.000đ/ticket đặt mục tiêu rẻ hơn làm tay ít nhất 20%. ROI tối thiểu 0,25 nghĩa là tiết kiệm ròng bằng ít nhất 25% tổng chi phí; phải dùng ROI do report tính, bao gồm tác hại tiền hoàn sai. Đây không phải trần riêng tiền LLM. Không có ca ùn nghĩa là không có ca cần người chờ quá giới hạn áp dụng; `ops_limits.review_sla_minutes = 60` là căn cứ để Sơn đặt cổng vận hành.
- Hành động nếu trượt `business_ops`: không chọn Tiếp tục; kiểm tra theo kho/hãng và Thu hẹp nếu phạm vi còn lại đã đo đạt, hoặc chọn Cải tiến thêm với giả thuyết về chi phí/hàng chờ. Nếu sau vòng sửa hoặc lần thử thu hẹp vẫn không có phạm vi đạt thì Dừng pilot tự động đề xuất.
- Ngày xem lại đề xuất: `2026-11-19`, tại quyết định v1 và v2 · Ai dự: Nguyễn Trọng Truyền, Nguyễn Văn Hùng, Trần Phạm Minh Sơn. Nhóm xác nhận ngày thực tế trước khi ký và ghi lại ở Phiếu B mục B8. Xem lại quyết định bằng bằng chứng mới, không sửa file tiêu chí đã ký.
- Quy tắc quyết định đã chốt: Dừng khi chạm `stop_condition`; nếu chưa chạm thì chỉ Tiếp tục khi mọi ngưỡng bắt buộc và kinh doanh/vận hành đều đạt, không vượt trần và không có ca mới hỏng. Thu hẹp phải nêu phần bị cắt, nơi xử lý các ticket đó và bằng chứng phạm vi còn lại đạt; nếu chưa có bằng chứng này thì Cải tiến thêm. Nội dung chi tiết nằm trong `decision_rule` của config đã ký.

**Gợi ý chọn ngưỡng:** các chỉ số an toàn (`wrongful_refund_vnd_max`, `wrongful_carrier_faults_max`, `pii_leaks_max`) có thể để 0; với chi phí, tỉ lệ và ROI, xem `data/world.json` mục `ops_facts`.

**Ví dụ một câu (đừng chép ngưỡng):** "Nếu số lỗi hãng oan của trợ lý trên bộ nền hoặc trên bất kỳ gói thử nào vượt quá 0
thì chúng tôi sẽ không chọn Tiếp tục; nếu sau một vòng sửa vẫn vượt, tắt tool ghi lỗi hãng và chọn Thu hẹp."

---

<a id="a5"></a>

## A5 · Ký và đẩy tiêu chí (phút 60–65)

**Đã thực hiện:** đã nhận câu 1.3 của Hùng và câu 1.2, 1.4 của Sơn. Leader chốt bộ tiêu chí theo quyền được nhóm giao, đã tạo file `.lock` và đẩy commit ký lên `origin/main`. Giờ ký và mã commit dưới đây lấy từ file khóa và lịch sử Git thực tế.

Soát lại `config/acceptance_criteria.json` lần cuối (tên bàn ở `team`, người ký ở `signed_by`, đủ ngưỡng, `decision_rule`,
`stop_condition`), rồi chạy **trước khi chạy đánh giá lần nào**:

```bash
python3 -m lab10.criteria sign
git add config/acceptance_criteria.json config/acceptance_criteria.lock && git commit -m 'Sign acceptance criteria' && git push -u origin main
```

| Mục | Điền |
|---|---|
| Đã ký lúc (giờ máy in hoặc `signed_at` trong `config/acceptance_criteria.lock`) | `2026-11-19T15:32:46` |
| Mã commit `Sign acceptance criteria` (7 ký tự đầu, `git log --oneline -1`) | `260f56d` |
| Đã push lên `origin main` thành công? | Có; commit ký `260f56d` có trên `origin/main`. |

Sau bước này **không sửa** `config/acceptance_criteria.json`, kể cả mở rồi lưu lại bằng trình soạn thảo tự định dạng.
