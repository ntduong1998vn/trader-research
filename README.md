# Trader Research

[Wiki nghiên cứu giao dịch](https://ntduong1998vn.github.io/trader-research/) được tạo từ các tệp Markdown trong [`docs/`](docs/).

## Xem wiki trên máy

```sh
pip install -r requirements.txt
mkdocs serve
```

Mở địa chỉ mà MkDocs in ra trong terminal.

## Xuất bản lên GitHub Pages

Trong GitHub, vào **Settings → Pages → Build and deployment → Source** và chọn **GitHub Actions**. Sau khi bật, mỗi lần cập nhật nhánh `main`, workflow **Deploy wiki to GitHub Pages** sẽ kiểm tra và xuất bản lại wiki.
