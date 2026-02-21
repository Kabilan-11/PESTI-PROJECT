from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
import sqlite3
import json
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication

DATABASE = 'agrichem.db'

# Database initialization
def init_db():
    """Initialize the database with required tables"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Products table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            size TEXT,
            stock INTEGER DEFAULT 0,
            rating REAL DEFAULT 0.0,
            image_url TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Customers table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            phone TEXT NOT NULL,
            farm_size INTEGER,
            crop_type TEXT,
            address TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Orders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_number TEXT UNIQUE NOT NULL,
            customer_id INTEGER NOT NULL,
            total_amount REAL NOT NULL,
            status TEXT DEFAULT 'pending',
            delivery_address TEXT,
            special_notes TEXT,
            discount_code TEXT,
            discount_amount REAL DEFAULT 0.0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers (id)
        )
    ''')
    
    # Order items table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS order_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (order_id) REFERENCES orders (id),
            FOREIGN KEY (product_id) REFERENCES products (id)
        )
    ''')
    
    # Services table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            price REAL NOT NULL,
            icon TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Service bookings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS service_bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER NOT NULL,
            service_id INTEGER NOT NULL,
            booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'pending',
            notes TEXT,
            FOREIGN KEY (customer_id) REFERENCES customers (id),
            FOREIGN KEY (service_id) REFERENCES services (id)
        )
    ''')
    
    # Discount codes table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS discount_codes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            code TEXT UNIQUE NOT NULL,
            discount_percentage REAL NOT NULL,
            active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully!")

# Helper function to get database connection
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Seed initial data
def seed_data():
    """Add initial products and services to database"""
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if products already exist
    cursor.execute('SELECT COUNT(*) FROM products')
    if cursor.fetchone()[0] == 0:
        products = [
            ('Chlorpyrifos', 'insecticide', 'Broad-spectrum organophosphate for soil and foliar pests', 45.99, '1L Bottle', 100, 4.8),
            ('Deltamethrin', 'insecticide', 'Pyrethroid insecticide for cotton, vegetables, and fruits', 38.50, '500ml Bottle', 150, 4.5),
            ('Lambda-Cyhalothrin', 'insecticide', 'Fast-acting control for chewing and sucking insects', 52.75, '1L Bottle', 80, 4.9),
            ('Malathion', 'insecticide', 'Effective against aphids, mites, and fruit flies', 34.99, '2L Bottle', 120, 4.6),
            ('Glyphosate', 'herbicide', 'Non-selective herbicide for weed control', 89.99, '5L Container', 60, 4.7),
            ('Mancozeb', 'fungicide', 'Protective fungicide for various crops', 28.50, '1kg Pack', 200, 4.4)
        ]
        
        cursor.executemany('''
            INSERT INTO products (name, category, description, price, size, stock, rating)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', products)
        
        print("Products seeded successfully!")
    
    # Check if services already exist
    cursor.execute('SELECT COUNT(*) FROM services')
    if cursor.fetchone()[0] == 0:
        services = [
            ('Pest Consultation', 'Expert advice on pest identification and treatment solutions', 50.00, '🔬'),
            ('Application Services', 'Professional pesticide application by certified technicians', 150.00, '🚜'),
            ('Soil Testing', 'Comprehensive soil analysis for optimal chemical selection', 75.00, '📊'),
            ('Bulk Delivery', 'Free delivery on orders over ₹500', 0.00, '📦')
        ]
        
        cursor.executemany('''
            INSERT INTO services (name, description, price, icon)
            VALUES (?, ?, ?, ?)
        ''', services)
        
        print("Services seeded successfully!")
    
    # Check if discount codes already exist
    cursor.execute('SELECT COUNT(*) FROM discount_codes')
    if cursor.fetchone()[0] == 0:
        discount_codes = [
            ('SAVE10', 10.0),
            ('SAVE20', 20.0),
            ('FIRST50', 50.0),
            ('BULK15', 15.0)
        ]
        
        cursor.executemany('''
            INSERT INTO discount_codes (code, discount_percentage)
            VALUES (?, ?)
        ''', discount_codes)
        print("Discount codes seeded successfully!")
        conn.commit()
        conn.close()

# ==================== API ROUTES ====================

# Home route
@app.route('/')
def home():
    return jsonify({
        'message': 'AgriChem Solutions API',
        'version': '1.0',
        'endpoints': {
            'products': '/api/products',
            'services': '/api/services',
            'orders': '/api/orders',
            'customers': '/api/customers'
        }
    })

# ==================== PRODUCTS ROUTES ====================

@app.route('/api/products', methods=['GET'])
def get_products():
    """Get all products or filter by category"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        category = request.args.get('category')
        search = request.args.get('search')
        
        if category:
            cursor.execute('SELECT * FROM products WHERE category = ?', (category,))
        elif search:
            cursor.execute('SELECT * FROM products WHERE name LIKE ? OR description LIKE ?', 
                         (f'%{search}%', f'%{search}%'))
        else:
            cursor.execute('SELECT * FROM products')
        
        products = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify({
            'success': True,
            'count': len(products),
            'products': products
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get a single product by ID"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM products WHERE id = ?', (product_id,))
        product = cursor.fetchone()
        conn.close()
        
        if product:
            return jsonify({
                'success': True,
                'product': dict(product)
            })
        else:
            return jsonify({'success': False, 'error': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/products', methods=['POST'])
def add_product():
    """Add a new product"""
    try:
        data = request.json
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO products (name, category, description, price, size, stock, rating)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            data['name'],
            data['category'],
            data.get('description', ''),
            data['price'],
            data.get('size', ''),
            data.get('stock', 0),
            data.get('rating', 0.0)
        ))
        
        conn.commit()
        product_id = cursor.lastrowid
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Product added successfully',
            'product_id': product_id
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    """Update a product"""
    try:
        data = request.json
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE products 
            SET name=?, category=?, description=?, price=?, size=?, stock=?, rating=?
            WHERE id=?
        ''', (
            data['name'],
            data['category'],
            data.get('description', ''),
            data['price'],
            data.get('size', ''),
            data.get('stock', 0),
            data.get('rating', 0.0),
            product_id
        ))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Product updated successfully'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    """Delete a product"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM products WHERE id = ?', (product_id,))
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Product deleted successfully'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== SERVICES ROUTES ====================

@app.route('/api/services', methods=['GET'])
def get_services():
    """Get all services"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM services')
        services = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify({
            'success': True,
            'count': len(services),
            'services': services
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/services/book', methods=['POST'])
def book_service():
    """Book a service"""
    try:
        data = request.json
        conn = get_db()
        cursor = conn.cursor()
        
        # Check if customer exists, if not create
        cursor.execute('SELECT id FROM customers WHERE email = ?', (data['email'],))
        customer = cursor.fetchone()
        
        if customer:
            customer_id = customer[0]
        else:
            cursor.execute('''
                INSERT INTO customers (name, email, phone, address)
                VALUES (?, ?, ?, ?)
            ''', (data['name'], data['email'], data['phone'], data.get('address', '')))
            customer_id = cursor.lastrowid
        
        # Create service booking
        cursor.execute('''
            INSERT INTO service_bookings (customer_id, service_id, notes)
            VALUES (?, ?, ?)
        ''', (customer_id, data['service_id'], data.get('notes', '')))
        
        booking_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Service booked successfully',
            'booking_id': booking_id
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== CUSTOMERS ROUTES ====================

@app.route('/api/customers', methods=['GET'])
def get_customers():
    """Get all customers"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM customers')
        customers = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify({
            'success': True,
            'count': len(customers),
            'customers': customers
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    """Get a single customer by ID"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM customers WHERE id = ?', (customer_id,))
        customer = cursor.fetchone()
        conn.close()
        
        if customer:
            return jsonify({
                'success': True,
                'customer': dict(customer)
            })
        else:
            return jsonify({'success': False, 'error': 'Customer not found'}), 404
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== ORDERS ROUTES ====================

@app.route('/api/orders', methods=['GET'])
def get_orders():
    """Get all orders"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT o.*, c.name as customer_name, c.email as customer_email
            FROM orders o
            JOIN customers c ON o.customer_id = c.id
            ORDER BY o.created_at DESC
        ''')
        
        orders = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify({
            'success': True,
            'count': len(orders),
            'orders': orders
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Get a single order with items"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Get order details
        cursor.execute('''
            SELECT o.*, c.name as customer_name, c.email as customer_email, c.phone as customer_phone
            FROM orders o
            JOIN customers c ON o.customer_id = c.id
            WHERE o.id = ?
        ''', (order_id,))
        
        order = cursor.fetchone()
        
        if not order:
            return jsonify({'success': False, 'error': 'Order not found'}), 404
        
        order_dict = dict(order)
        
        # Get order items
        cursor.execute('''
            SELECT oi.*, p.name as product_name, p.category
            FROM order_items oi
            JOIN products p ON oi.product_id = p.id
            WHERE oi.order_id = ?
        ''', (order_id,))
        
        items = [dict(row) for row in cursor.fetchall()]
        order_dict['items'] = items
        
        conn.close()
        
        return jsonify({
            'success': True,
            'order': order_dict
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/orders', methods=['POST'])
def create_order():
    """Create a new order"""
    try:
        data = request.json
        conn = get_db()
        cursor = conn.cursor()
        
        # Check if customer exists, if not create
        cursor.execute('SELECT id FROM customers WHERE email = ?', (data['customer']['email'],))
        customer = cursor.fetchone()
        
        if customer:
            customer_id = customer[0]
            # Update customer info
            cursor.execute('''
                UPDATE customers 
                SET name=?, phone=?, farm_size=?, crop_type=?, address=?
                WHERE id=?
            ''', (
                data['customer']['name'],
                data['customer']['phone'],
                data['customer'].get('farm_size'),
                data['customer'].get('crop_type'),
                data['customer'].get('delivery'),
                customer_id
            ))
        else:
            cursor.execute('''
                INSERT INTO customers (name, email, phone, farm_size, crop_type, address)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                data['customer']['name'],
                data['customer']['email'],
                data['customer']['phone'],
                data['customer'].get('farm_size'),
                data['customer'].get('crop_type'),
                data['customer'].get('delivery')
            ))
            customer_id = cursor.lastrowid
        
        # Generate order number
        order_number = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Calculate discount
        discount_amount = 0.0
        discount_code = data.get('discount_code')
        
        if discount_code:
            cursor.execute('SELECT discount_percentage FROM discount_codes WHERE code = ? AND active = 1', 
                         (discount_code,))
            discount = cursor.fetchone()
            if discount:
                discount_amount = float(data['total']) * (discount[0] / 100)
        
        final_total = float(data['total']) - discount_amount
        
        # Create order
        cursor.execute('''
            INSERT INTO orders (order_number, customer_id, total_amount, delivery_address, 
                              special_notes, discount_code, discount_amount)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            order_number,
            customer_id,
            final_total,
            data['customer'].get('delivery'),
            data['customer'].get('notes'),
            discount_code,
            discount_amount
        ))
        
        order_id = cursor.lastrowid
        
        # Add order items
        for item in data['items']:
            # Get product ID by name
            cursor.execute('SELECT id, price FROM products WHERE name = ?', (item['product'],))
            product = cursor.fetchone()
            
            if product:
                cursor.execute('''
                    INSERT INTO order_items (order_id, product_id, quantity, price)
                    VALUES (?, ?, ?, ?)
                ''', (order_id, product[0], item['quantity'], item['price']))
                
                # Update product stock
                cursor.execute('''
                    UPDATE products SET stock = stock - ? WHERE id = ?
                ''', (item['quantity'], product[0]))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Order created successfully',
            'order_number': order_number,
            'order_id': order_id,
            'final_total': final_total,
            'discount_applied': discount_amount
        }), 201
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/orders/<int:order_id>/status', methods=['PUT'])
def update_order_status(order_id):
    """Update order status"""
    try:
        data = request.json
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('UPDATE orders SET status = ? WHERE id = ?', 
                      (data['status'], order_id))
        
        conn.commit()
        conn.close()
        
        return jsonify({
            'success': True,
            'message': 'Order status updated successfully'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== DISCOUNT CODES ROUTES ====================

@app.route('/api/discount/validate', methods=['POST'])
def validate_discount():
    """Validate a discount code"""
    try:
        data = request.json
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT code, discount_percentage 
            FROM discount_codes 
            WHERE code = ? AND active = 1
        ''', (data['code'].upper(),))
        
        discount = cursor.fetchone()
        conn.close()
        
        if discount:
            return jsonify({
                'success': True,
                'valid': True,
                'code': discount[0],
                'discount_percentage': discount[1]
            })
        else:
            return jsonify({
                'success': True,
                'valid': False,
                'message': 'Invalid or expired discount code'
            })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== STATISTICS ROUTES ====================

@app.route('/api/stats', methods=['GET'])
def get_statistics():
    """Get dashboard statistics"""
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Total orders
        cursor.execute('SELECT COUNT(*) FROM orders')
        total_orders = cursor.fetchone()[0]
        
        # Total revenue
        cursor.execute('SELECT SUM(total_amount) FROM orders WHERE status != "cancelled"')
        total_revenue = cursor.fetchone()[0] or 0
        
        # Total customers
        cursor.execute('SELECT COUNT(*) FROM customers')
        total_customers = cursor.fetchone()[0]
        
        # Total products
        cursor.execute('SELECT COUNT(*) FROM products')
        total_products = cursor.fetchone()[0]
        
        # Recent orders
        cursor.execute('''
            SELECT o.order_number, o.total_amount, o.status, o.created_at, c.name
            FROM orders o
            JOIN customers c ON o.customer_id = c.id
            ORDER BY o.created_at DESC
            LIMIT 5
        ''')
        recent_orders = [dict(row) for row in cursor.fetchall()]
        
        # Low stock products
        cursor.execute('SELECT * FROM products WHERE stock < 50 ORDER BY stock ASC')
        low_stock = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        return jsonify({
            'success': True,
            'statistics': {
                'total_orders': total_orders,
                'total_revenue': round(total_revenue, 2),
                'total_customers': total_customers,
                'total_products': total_products,
                'recent_orders': recent_orders,
                'low_stock_products': low_stock
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== SEARCH ROUTE ====================

@app.route('/api/search', methods=['GET'])
def search():
    """Global search across products and services"""
    try:
        query = request.args.get('q', '')
        conn = get_db()
        cursor = conn.cursor()
        
        # Search products
        cursor.execute('''
            SELECT 'product' as type, id, name, description, price 
            FROM products 
            WHERE name LIKE ? OR description LIKE ?
        ''', (f'%{query}%', f'%{query}%'))
        products = [dict(row) for row in cursor.fetchall()]
        
        # Search services
        cursor.execute('''
            SELECT 'service' as type, id, name, description, price 
            FROM services 
            WHERE name LIKE ? OR description LIKE ?
        ''', (f'%{query}%', f'%{query}%'))
        services = [dict(row) for row in cursor.fetchall()]
        
        conn.close()
        
        return jsonify({
            'success': True,
            'results': {
                'products': products,
                'services': services,
                'total': len(products) + len(services)
            }
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'success': False, 'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'success': False, 'error': 'Internal server error'}), 500

# ==================== MAIN ====================

if __name__ == '__main__':
    # Initialize database and seed data
    if not os.path.exists(DATABASE):
        print("Creating database...")
        init_db()
        seed_data()
    else:
        print("Database already exists")
    
    print("\n" + "="*50)
    print("AgriChem Solutions API Server")
    print("="*50)
    print("Server running on: http://localhost:5000")
    print("API Documentation: http://localhost:5000/")
    print("="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
