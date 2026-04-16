from flask import Blueprint, jsonify, request
import psycopg2
from psycopg2.extras import RealDictCursor

product_bp = Blueprint("product_api", __name__)

# Cấu hình kết nối Database
DB_CONFIG = {
    "dbname": "flask_db",
    "user": "postgres",
    "password": "123",
    "host": "localhost",
    "port": "5432"
}

def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

@product_bp.route("/products", methods=["GET"])
def get_products():
    search_name = request.args.get("name")
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    if search_name:
        # Dùng ILIKE để tìm kiếm không phân biệt hoa thường
        cur.execute("SELECT * FROM products WHERE name ILIKE %s", (f"%{search_name}%",))
    else:
        cur.execute("SELECT * FROM products ORDER BY id ASC")
        
    products = cur.fetchall()
    cur.close()
    conn.close()
    
    return jsonify(products)

@product_bp.route("/product/<int:id>", methods=["GET"])
def get_product_by_id(id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    cur.execute("SELECT * FROM products WHERE id = %s", (id,))
    product = cur.fetchone()
    
    cur.close()
    conn.close()
    
    if product:
        return jsonify(product)
    
    return jsonify({"message": "Không tìm thấy sản phẩm"}), 404

@product_bp.route("/products", methods=["POST"])
def add_product():
    data = request.get_json()
    name = data.get("name")
    price = data.get("price")
    
    # Validate cơ bản
    if not name or price is None:
        return jsonify({"message": "Thiếu thông tin name hoặc price!"}), 400

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    # Chèn data và trả về dòng vừa chèn
    cur.execute(
        "INSERT INTO products (name, price) VALUES (%s, %s) RETURNING *",
        (name, price)
    )
    new_product = cur.fetchone()
    conn.commit() # Bắt buộc phải commit khi INSERT/UPDATE/DELETE
    
    cur.close()
    conn.close()
    
    return jsonify({"message": "Thêm sản phẩm thành công!", "product": new_product}), 201

@product_bp.route("/product/<int:id>", methods=["PUT", "PATCH"])
def update_product(id):
    data = request.get_json()
    
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    
    # Kiểm tra sản phẩm có tồn tại không
    cur.execute("SELECT * FROM products WHERE id = %s", (id,))
    if not cur.fetchone():
        cur.close()
        conn.close()
        return jsonify({"message": f"Không tìm thấy sản phẩm với ID {id}!"}), 404

    # Cập nhật thông tin
    name = data.get("name")
    price = data.get("price")
    
    if name and price is not None:
        cur.execute("UPDATE products SET name = %s, price = %s WHERE id = %s RETURNING *", (name, price, id))
    elif name:
        cur.execute("UPDATE products SET name = %s WHERE id = %s RETURNING *", (name, id))
    elif price is not None:
        cur.execute("UPDATE products SET price = %s WHERE id = %s RETURNING *", (price, id))
        
    updated_product = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({
        "message": "Cập nhật sản phẩm thành công!", 
        "product": updated_product
    }), 200

@product_bp.route("/product/<int:id>", methods=["DELETE"])
def delete_product(id):
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Xóa và trả về id vừa xóa để kiểm tra
    cur.execute("DELETE FROM products WHERE id = %s RETURNING id", (id,))
    deleted_id = cur.fetchone()
    
    if deleted_id is None:
        cur.close()
        conn.close()
        return jsonify({"message": f"Không tìm thấy sản phẩm với ID {id} để xóa!"}), 404
        
    conn.commit()
    cur.close()
    conn.close()
    
    return jsonify({"message": f"Đã xóa sản phẩm có ID {id} thành công!"}), 200