# AgriChem Solutions - Backend API

Python Flask backend with SQLite database for the AgriChem pesticides e-commerce website.

## Features

- RESTful API architecture
- SQLite database for data persistence
- CRUD operations for products, orders, customers, and services
- Order management system
- Discount code validation
- Service booking system
- Search functionality
- Statistics dashboard
- CORS enabled for frontend integration

## Database Schema

### Tables:
1. **products** - Store pesticide products
2. **customers** - Customer information
3. **orders** - Order records
4. **order_items** - Individual items in orders
5. **services** - Available services
6. **service_bookings** - Service booking records
7. **discount_codes** - Promotional discount codes

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the application:**
```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### Products
- `GET /api/products` - Get all products
- `GET /api/products?category=insecticide` - Filter by category
- `GET /api/products?search=chlor` - Search products
- `GET /api/products/<id>` - Get single product
- `POST /api/products` - Add new product
- `PUT /api/products/<id>` - Update product
- `DELETE /api/products/<id>` - Delete product

### Services
- `GET /api/services` - Get all services
- `POST /api/services/book` - Book a service

### Orders
- `GET /api/orders` - Get all orders
- `GET /api/orders/<id>` - Get single order with items
- `POST /api/orders` - Create new order
- `PUT /api/orders/<id>/status` - Update order status

### Customers
- `GET /api/customers` - Get all customers
- `GET /api/customers/<id>` - Get single customer

### Discount Codes
- `POST /api/discount/validate` - Validate discount code

### Statistics
- `GET /api/stats` - Get dashboard statistics

### Search
- `GET /api/search?q=query` - Global search

## Example API Requests

### Create Order
```bash
POST /api/orders
Content-Type: application/json

{
  "customer": {
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+91-9876543210",
    "farm_size": 50,
    "crop_type": "wheat",
    "delivery": "123 Farm Road, Village",
    "notes": "Deliver in morning"
  },
  "items": [
    {
      "product": "Chlorpyrifos",
      "quantity": 2,
      "price": 45.99,
      "category": "insecticide"
    }
  ],
  "total": 91.98,
  "discount_code": "SAVE10"
}
```

### Validate Discount Code
```bash
POST /api/discount/validate
Content-Type: application/json

{
  "code": "SAVE10"
}
```

### Search Products
```bash
GET /api/products?search=chlor
```

## Pre-seeded Data

The database comes with pre-seeded data:

### Products:
- Chlorpyrifos (Insecticide) - ₹45.99
- Deltamethrin (Insecticide) - ₹38.50
- Lambda-Cyhalothrin (Insecticide) - ₹52.75
- Malathion (Insecticide) - ₹34.99
- Glyphosate (Herbicide) - ₹89.99
- Mancozeb (Fungicide) - ₹28.50

### Services:
- Pest Consultation - ₹50
- Application Services - ₹150
- Soil Testing - ₹75
- Bulk Delivery - Free

### Discount Codes:
- SAVE10 - 10% off
- SAVE20 - 20% off
- FIRST50 - 50% off
- BULK15 - 15% off

## Database Management

### Reset Database
Delete the `agrichem.db` file and restart the server to recreate with fresh data.

```bash
rm agrichem.db
python app.py
```

### Backup Database
```bash
cp agrichem.db agrichem_backup.db
```

## Testing with cURL

### Get all products:
```bash
curl http://localhost:5000/api/products
```

### Create an order:
```bash
curl -X POST http://localhost:5000/api/orders \
  -H "Content-Type: application/json" \
  -d '{
    "customer": {
      "name": "Test User",
      "email": "test@example.com",
      "phone": "1234567890",
      "delivery": "Test Address"
    },
    "items": [{"product": "Chlorpyrifos", "quantity": 1, "price": 45.99}],
    "total": 45.99
  }'
```

### Get statistics:
```bash
curl http://localhost:5000/api/stats
```

## Error Handling

All endpoints return JSON responses with the following structure:

### Success Response:
```json
{
  "success": true,
  "data": {...}
}
```

### Error Response:
```json
{
  "success": false,
  "error": "Error message"
}
```

## CORS Configuration

CORS is enabled for all origins in development. For production, update the CORS configuration in `app.py`:

```python
CORS(app, resources={r"/api/*": {"origins": "https://yourdomain.com"}})
```

## Security Notes

For production deployment:
1. Change the SECRET_KEY in config.py
2. Use environment variables for sensitive data
3. Implement authentication and authorization
4. Use HTTPS
5. Add rate limiting
6. Validate and sanitize all inputs
7. Use a production-grade database (PostgreSQL/MySQL)

## Troubleshooting

### Port already in use:
```bash
# Change port in app.py
app.run(debug=True, host='0.0.0.0', port=5001)
```

### Database locked error:
Close any other connections to the database or restart the server.

### CORS errors:
Ensure Flask-CORS is installed and properly configured.

## License

Copyright © 2024 AgriChem Solutions. All rights reserved.
