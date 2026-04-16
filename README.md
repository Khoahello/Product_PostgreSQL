# API Quản lý Sản phẩm (Flask + PostgreSQL)

Bài tập API CRUD cơ bản (Thêm, Đọc, Sửa, Xóa) sử dụng Flask và kết nối với cơ sở
dữ liệu PostgreSQL.

---

## Hướng dẫn cài đặt và chạy dự án

### 1. Cài đặt thư viện

Mở Terminal tại thư mục code và chạy lệnh:

```bash
pip install -r requirements.txt
```

### 2. Thiết lập Database (PostgreSQL)

- Mở **pgAdmin 4**, tạo một Database mới đặt tên là `flask_db`.
- Mở **Query Tool** trên `flask_db` và chạy đoạn lệnh SQL sau để tạo bảng:

```sql
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    price NUMERIC NOT NULL
);

INSERT INTO products (name, price) VALUES ('Bàn phím cơ', 1500000);
INSERT INTO products (name, price) VALUES ('TV', 1500000);
```

### 3. Cấu hình kết nối

File `product_routes.py` đã được thiết lập sẵn cấu hình với mật khẩu là `123`.
Nếu máy bạn dùng mật khẩu khác, vui lòng đổi lại trong đoạn code sau:

```python
DB_CONFIG = {
    "dbname": "flask_db",
    "user": "postgres",
    "password": "123",
    "host": "localhost",
    "port": "5432"
}
```

### 4. Khởi chạy Server

Mở Terminal và chạy lệnh:

```bash
python app.py
```

Server sẽ hoạt động tại địa chỉ: `http://127.0.0.1:5000`

---

## Hướng dẫn test API (Bằng Postman)

| Phương thức | Đường dẫn (URL)          | Chức năng              | Dữ liệu gửi đi (Body)                 |
| :---------- | :----------------------- | :--------------------- | :------------------------------------ |
| **GET**     | `/products`              | Lấy danh sách sản phẩm | Không cần                             |
| **GET**     | `/products?name=từ_khóa` | Tìm kiếm theo tên      | Gửi qua tab Params                    |
| **GET**     | `/product/<id>`          | Xem 1 sản phẩm theo ID | Không cần                             |
| **POST**    | `/products`              | Thêm sản phẩm mới      | JSON: `{"name": "...", "price": ...}` |
| **PUT**     | `/product/<id>`          | Sửa thông tin sản phẩm | JSON: `{"name": "...", "price": ...}` |
| **DELETE**  | `/product/<id>`          | Xóa sản phẩm           | Không cần                             |

```

```
````
