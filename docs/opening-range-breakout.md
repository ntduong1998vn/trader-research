# Opening Range Breakout (ORB): bằng chứng và cách kiểm chứng

**Kết luận:** Với cổ phiếu Mỹ, việc chọn mã có khối lượng mở cửa bất thường đáng kiểm định trước khi tinh chỉnh vùng 5, 15 hay 30 phút. Khung 5 phút dẫn về tỷ lệ thắng trong một backtest lớn, nhưng khung 15 phút dẫn về lãi/lỗ trung bình mỗi lệnh. Không thể chọn cấu hình chỉ bằng tỷ lệ thắng, cũng không thể dùng kết quả trên cổ phiếu để kết luận cho futures hay Forex.

## Vì sao ORB có thể hiệu quả?

Vùng mở cửa là khoảng từ giá thấp nhất đến giá cao nhất trong `N` phút đầu của phiên được chọn. Ở cổ phiếu Mỹ, lệnh tích tụ qua đêm và thông tin mới gặp nhau khi phiên chính mở cửa. Nếu giá vượt biên sau khi vùng đã hình thành, đó có thể là dấu hiệu một phía vẫn còn đủ lực để đẩy giá đi tiếp. Nhưng trong phiên đi ngang, giá có thể xuyên biên rồi quay ngay vào vùng; bản thân cú vượt biên không chứng minh có xu hướng.

Khối lượng tương đối (Relative Volume, **RVOL**) giúp phân biệt một phiên thực sự thu hút giao dịch với một phiên chỉ có vẻ sôi động vì đang ở giờ mở cửa. Mẫu số nên là khối lượng bình quân **cùng cửa sổ thời gian** ở các phiên trước, không phải khối lượng cả ngày. RVOL giúp chọn mã để theo dõi, không tự xác định hướng lệnh và không bảo đảm cú phá vỡ sẽ tiếp diễn.

Độ dài vùng tạo một đánh đổi khác: 5 phút cho tín hiệu sớm, nhưng dễ nhiễu và nhạy với độ trễ, spread và trượt giá; vùng dài hơn cho thêm thời gian quan sát, nhưng có thể buộc đặt dừng lỗ xa hơn nếu dùng bề rộng vùng để đặt stop, đồng thời còn ít thời gian hơn để giá đi tới mục tiêu.

## Hai nguồn dữ liệu trả lời hai câu hỏi khác nhau

### 1. RVOL có giúp chọn cổ phiếu tốt hơn?

Zarattini, Barbon & Aziz [1] mô phỏng danh mục cổ phiếu Mỹ từ tháng 01/2016 đến 12/2023, vốn đầu kỳ 25.000 USD, tính hoa hồng 0,0035 USD/cổ phiếu. Cấu hình cơ sở đã lọc giá mở cửa, thanh khoản và ATR (thước đo biên độ dao động); «không lọc RVOL» không có nghĩa là giao dịch mọi cổ phiếu.

| Cấu hình | Tổng lợi suất | Lợi suất năm (IRR theo bài nghiên cứu) | Sharpe |
| --- | ---: | ---: | ---: |
| ORB 5 phút, không lọc RVOL | 29% | 3,2% | 0,48 |
| Nắm giữ S&P 500 | 198% | 14,2% | 0,78 |
| ORB 5 phút + RVOL | 1.637% | 41,6% | 2,81 |
| ORB 15 phút + RVOL | 272% | 17,4% | 1,43 |
| ORB 30 phút + RVOL | 21% | 2,3% | 0,21 |

Ở cấu hình 5 phút, nghiên cứu lấy khối lượng 09:30–09:35 ET chia cho khối lượng trung bình cùng cửa sổ của 14 phiên trước; chỉ chọn tối đa 20 mã đứng đầu trong nhóm đủ điều kiện có RVOL từ 1,0 trở lên. Hướng lệnh theo chiều nến mở cửa, kích hoạt bằng lệnh stop tại biên; dừng lỗ cách giá vào 10% ATR và đóng vị thế còn lại cuối phiên. Vì thế, kết quả 2,81 là của **toàn bộ cấu hình**, không phải kết quả mặc định khi thêm một điều kiện volume vào bất kỳ biến thể nào.

So sánh 0,48 và 2,81 cho thấy việc chọn nhóm *Stocks in Play* đáng ưu tiên thử nghiệm. Tuy nhiên, phép so sánh thay đổi cả ngưỡng đủ điều kiện lẫn việc chỉ lấy 20 mã RVOL cao nhất; nó không tách riêng đóng góp của từng yếu tố hoặc chứng minh RVOL «quyết định 80% hiệu quả». Kết quả đã tính hoa hồng cũng không đồng nghĩa chất lượng khớp lệnh và thanh khoản khi giao dịch thật đã được xác nhận.

### 2. Độ dài vùng và quy tắc thoát ảnh hưởng thế nào?

ORB Setups [2] báo cáo 1.178.668 lượt giao dịch mô phỏng trên 614 mã, dùng dữ liệu nến 1 phút từ 12/2024 đến 03/2026. Tỷ lệ thắng tổng hợp gộp bốn tổ hợp chốt lời/dừng lỗ; không phải tỷ lệ thắng của một cấu hình duy nhất.

| Vùng | Tỷ lệ thắng tổng hợp | Kết quả nổi bật trong mẫu |
| --- | ---: | --- |
| 5 phút | 53,78% | Vùng trung bình rộng 0,76 USD; 3,34% lượt không chạm mục tiêu hoặc dừng lỗ trước cuối phiên. |
| 15 phút | 50,97% | Lãi/lỗ trung bình cao nhất khi gộp các quy tắc: 0,0314 USD/lượt theo cách tính của nguồn. |
| 30 phút | 49,38% | Tổng lãi/lỗ mô phỏng cao nhất: 13.270,96 USD; vùng rộng trung bình 1,04 USD và 12,76% lượt chưa chạm mục tiêu hoặc dừng lỗ trước cuối phiên. |

Với vùng 15 phút và cả mục tiêu lẫn stop đều bằng một lần bề rộng vùng, nguồn báo cáo tỷ lệ thắng 46,12% nhưng lãi/lỗ trung bình 0,044 USD/lượt. Với vùng 5 phút, mục tiêu bằng nửa vùng và stop bằng cả vùng, tỷ lệ thắng lên 68,87% nhưng trung bình chỉ 0,018 USD/lượt. Mục tiêu gần hơn có thể tăng số lần chạm đích nhưng giảm số tiền thu được mỗi lần thắng. Nên tính kỳ vọng từ **P&L thực nhận của mọi lệnh**, kể cả lệnh đóng cuối phiên, rồi trừ các chi phí chưa phản ánh trong giá khớp.

Trong mẫu này, lệnh short thắng thường xuyên hơn, nhưng lệnh long có lãi/lỗ trung bình cao hơn: 0,031 so với 0,011 USD/lượt ở khung 5 phút, và 0,041 so với 0,022 USD/lượt ở khung 15 phút. Đây là lý do để báo cáo riêng hai chiều, không phải căn cứ để mặc định long luôn tốt hơn short.

**Đọc hai nguồn cùng nhau:** P&L cộng dồn của các lượt mô phỏng không phải lợi suất danh mục. Hai nguồn khác giai đoạn, tập mã, điều kiện vào/thoát và cách tổng hợp; 30 phút dẫn về P&L cộng dồn trong [2] nhưng lại có Sharpe thấp nhất trong ba cấu hình có RVOL ở [1]. Hơn một triệu lượt mô phỏng cho phép so sánh nhiều cấu hình, nhưng không phải hơn một triệu quan sát độc lập: nhiều lượt dùng chung mã, phiên hoặc điểm vào. Khung 30 phút với quy tắc mục tiêu/stop bằng cả vùng cũng có tỷ lệ thắng theo tháng dao động từ dưới 30% đến trên 60% trong [2]. Không nên chọn tham số chỉ vì đứng đầu toàn mẫu.

## Năm biến thể: điều gì được đánh đổi?

Các cơ chế sau đến từ tài liệu thực hành [3–6], không phải năm nhánh đã được so sánh đối chứng trong [1] hoặc [2]. Các lợi thế trong bảng là giả thuyết cần kiểm định.

| Biến thể | Tín hiệu vào lệnh | Lợi thế kỳ vọng và điểm yếu |
| --- | --- | --- |
| **Classic Breakout** | Chờ nến đóng ngoài biên vùng; có thể yêu cầu khối lượng xác nhận. | Có cơ hội bắt cú chạy thẳng, nhưng chờ đóng nến có thể làm giá vào xa biên; phiên đi ngang dễ phá vỡ giả. Khác với lệnh stop tại biên trong [1]. |
| **ORB Retest** | Sau cú phá, chờ giá quay lại mép vùng và nến xác nhận đi tiếp; có thể đặt stop sau nến retest. | Điểm vô hiệu gần hơn có thể cải thiện tỷ lệ lợi nhuận/rủi ro; sẽ bỏ lỡ cú chạy không quay lại. |
| **Trend-Filtered ORB** | Chỉ long trên, chỉ short dưới VWAP (giá bình quân gia quyền theo khối lượng) hoặc EMA (đường trung bình lũy thừa) đã chọn. | Tránh một số tín hiệu ngược xu hướng trong phiên; bộ lọc có thể chậm khi xu hướng đảo chiều ngay sau mở cửa. |
| **Gap-and-Go ORB** | Chỉ theo hướng gap qua đêm đủ lớn so với thước đo biến động đã định, chẳng hạn ATR. | Có thể tận dụng động lượng sau tin; nếu gap bị lấp sớm, giả thuyết tiếp diễn suy yếu. Không có đủ căn cứ để áp dụng một mức giảm vị thế cố định cho mọi mã. |
| **Failed ORB** | Khi nến đóng trở lại trong vùng sau cú phá, thoát lệnh thuận phá vỡ nếu có; kiểm định lệnh ngược hướng về biên đối diện như một tín hiệu riêng. | Có thể hưởng lợi khi người mua hoặc bán theo cú phá phải thoát; dễ thua thêm nếu giá quay lại hướng phá vỡ ban đầu. |

## Kiểm chứng trước khi triển khai

1. **Chọn điểm xuất phát theo thị trường.** Với cổ phiếu Mỹ, lấy ORB 5 phút trên *Stocks in Play* làm cấu hình đối chiếu và tách long/short. Với ES/NQ/MNQ, thử vùng 15 phút từ 09:30 ET (giờ mở cửa thị trường cổ phiếu cơ sở), rồi so sánh cấu hình cơ sở với VWAP/EMA và Retest. Với Forex/XAUUSD, thử vùng 15–30 phút neo vào đầu phiên London hoặc New York: đây là mốc quy ước, không phải phiên đấu giá mở cửa tập trung. Ghi rõ múi giờ, giờ mùa hè và nguồn volume; không mặc định volume Forex từ một nhà cung cấp tương đương volume cổ phiếu.
2. **Định nghĩa tín hiệu trước khi chạy.** Chỉ dùng biên và RVOL sau khi vùng hoàn tất; xếp hạng mã bằng dữ liệu có sẵn tại thời điểm đặt lệnh. Chốt cách mô phỏng khớp lệnh, xử lý nến có cả mục tiêu lẫn stop khi không biết thứ tự chạm, và cách thoát cuối phiên. Tách ảnh hưởng của cửa sổ, bộ lọc RVOL, phương thức vào và quy tắc thoát bằng cách thay một yếu tố mỗi lần.
3. **Đo kết quả sau chi phí và kiểm tra ngoài mẫu.** Mô hình hóa hoa hồng, spread và trượt giá; với lệnh short, kiểm tra khả năng vay cổ phiếu và phí vay nếu có. So sánh kỳ vọng ròng theo `R` (rủi ro ban đầu mỗi lệnh), số lệnh, tỷ lệ thắng, drawdown và Sharpe danh mục; phân nhóm theo mã, chiều giao dịch và giai đoạn. Dành một giai đoạn về sau ngoài mẫu để đánh giá cấu hình đã chốt. Nếu lợi thế biến mất với giả định khớp thận trọng, chưa có cơ sở để đưa vào giao dịch thật.

## Nguồn

- Tài liệu đầu vào: *Đánh giá hiệu quả các phương pháp Opening Range Breakout (ORB) trên thị trường* (HTML do người dùng cung cấp).
- [1] Zarattini, Barbon & Aziz (2024), [*A Profitable Day Trading Strategy For The U.S. Equity Market*](https://concretumgroup.com/a-profitable-day-trading-strategy-for-the-u-s-equity-market/), Swiss Finance Institute Working Paper 24-98, mục 2.1 và 4, bảng 1–3.
- [2] ORB Setups, [*5 vs 15 vs 30 Minute Opening Range Breakout: 1.17M Trades Backtest*](https://orbsetups.com/research/5-minute-vs-15-minute-vs-30-minute-opening-range-which-timeframe-has-the-best-win-rate/).
- [3] JournalPlus, [*Opening Range Breakout Strategy Guide*](https://journalplus.co/strategies/opening-range-breakout).
- [4] Apex Trader Funding, [*Opening Range Breakout Strategy for Futures*](https://apextraderfunding.com/resources/futures-trading/opening-range-breakout-strategy/).
- [5] Forex Tester, [*Opening Range Breakout Trading Strategy*](https://forextester.com/blog/opening-range-breakout-trading-strategies/).
- [6] The Chart Guys, [*ORB Trading Strategy: Mastering the Opening Range Breakout*](https://www.chartguys.com/articles/orb-trading-strategy).
