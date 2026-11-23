# Trader Research

[Wiki nghiên cứu giao dịch](https://ntduong1998vn.github.io/trader-research/) được tạo từ các tệp Markdown trong [`docs/`](docs/).

Khi thêm hoặc sửa bài, làm theo [quy tắc viết tài liệu wiki](AGENTS.md).

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
