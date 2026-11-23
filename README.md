# Trader Research

[Wiki nghiên cứu giao dịch](https://ntduong1998vn.github.io/trader-research/) được tạo từ các tệp Markdown trong [`docs/`](docs/).

Khi thêm hoặc sửa bài, làm theo [quy tắc viết tài liệu wiki](AGENTS.md).

## Chỉ báo ORB cho TradingView

[Mã Pine v6](pine/orb-entry-indicator.pine) đánh dấu entry lịch sử trên nến thường 1 phút, chưa phải strategy kiểm thử.
Xem [hướng dẫn dùng và giới hạn](docs/orb-indicator.md) trước khi thêm vào biểu đồ.

### Kiểm thử logic Pine ngoài TradingView

Dùng Node.js 24:

```sh
npm ci --ignore-scripts
npm test
```

Các ca kiểm thử chạy trực tiếp mã `.pine` bằng PineTS 0.13.1 trên dữ liệu nến mô phỏng, không gọi dữ liệu thị trường bên ngoài.
Chúng kiểm tra vùng OR, entry, RVOL, ATR ngày đã đóng, phiên qua đêm, thiếu nến và các trường hợp mơ hồ.
PineTS là công cụ bên thứ ba, không phải bộ biên dịch của TradingView. Vẫn cần kiểm tra trong Pine Editor và trên biểu đồ thật.

## Xem wiki trên máy

```sh
pip install -r requirements.txt
mkdocs serve
```

Mở địa chỉ mà MkDocs in ra trong terminal.

## Tạo lại hình minh họa ORB

```sh
python -m pip install matplotlib==3.10.9
python scripts/generate_orb_figures.py
```

Để tái tạo hình, dùng đúng phiên bản Matplotlib ở trên và font DejaVu Sans đi kèm. Script dùng cấu hình Matplotlib mặc định thay vì cấu hình cá nhân và ghi các tệp SVG vào `docs/assets/orb/`. Không cần Matplotlib khi build wiki.

## Xuất bản lên GitHub Pages

Trong GitHub, vào **Settings → Pages → Build and deployment → Source** và chọn **GitHub Actions**. Sau khi bật, mỗi lần cập nhật nhánh `main`, workflow **Deploy wiki to GitHub Pages** sẽ kiểm tra và xuất bản lại wiki.
