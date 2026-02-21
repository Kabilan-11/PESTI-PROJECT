"""
Test script for AgriChem Solutions API
Run this after starting the Flask server to test all endpoints
"""

import requests
import json

BASE_URL = 'http://localhost:5000'

def print_response(title, response):
    """Pretty print API response"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)

def test_home():
    """Test home endpoint"""
    response = requests.get(f'{BASE_URL}/')
    print_response("HOME ENDPOINT", response)

def test_get_products():
    """Test get all products"""
    response = requests.get(f'{BASE_URL}/api/products')
    print_response("GET ALL PRODUCTS", response)

def test_get_products_by_category():
    """Test get products by category"""
    response = requests.get(f'{BASE_URL}/api/products?category=insecticide')
    print_response("GET PRODUCTS BY CATEGORY (insecticide)", response)

def test_search_products():
    """Test search products"""
    response = requests.get(f'{BASE_URL}/api/products?search=chlor')
    print_response("SEARCH PRODUCTS (chlor)", response)

def test_get_services():
    """Test get all services"""
    response = requests.get(f'{BASE_URL}/api/services')
    print_response("GET ALL SERVICES", response)

def test_validate_discount():
    """Test validate discount code"""
    data = {"code": "SAVE10"}
    response = requests.post(f'{BASE_URL}/api/discount/validate', json=data)
    print_response("VALIDATE DISCOUNT CODE (SAVE10)", response)

def test_create_order():
    """Test create order"""
    order_data = {
        "customer": {
            "name": "Test Customer",
            "email": "test@example.com",
            "phone": "+91-9876543210",
            "farm_size": 50,
            "crop_type": "wheat",
            "delivery": "123 Test Farm Road, Test Village, Test State",
            "notes": "Please deliver in the morning"
        },
        "items": [
            {
                "product": "Chlorpyrifos",
                "quantity": 2,
                "price": 45.99,
                "category": "insecticide"
            },
            {
                "product": "Malathion",
                "quantity": 1,
                "price": 34.99,
                "category": "insecticide"
            }
        ],
        "total": 126.97,
        "discount_code": "SAVE10"
    }
    
    response = requests.post(f'{BASE_URL}/api/orders', json=order_data)
    print_response("CREATE ORDER", response)
    
    # Return order_id for further tests
    if response.status_code == 201:
        return response.json().get('order_id')
    return None

def test_get_orders():
    """Test get all orders"""
    response = requests.get(f'{BASE_URL}/api/orders')
    print_response("GET ALL ORDERS", response)

def test_get_order_by_id(order_id):
    """Test get single order"""
    if order_id:
        response = requests.get(f'{BASE_URL}/api/orders/{order_id}')
        print_response(f"GET ORDER BY ID ({order_id})", response)

def test_update_order_status(order_id):
    """Test update order status"""
    if order_id:
        data = {"status": "confirmed"}
        response = requests.put(f'{BASE_URL}/api/orders/{order_id}/status', json=data)
        print_response(f"UPDATE ORDER STATUS ({order_id})", response)

def test_get_customers():
    """Test get all customers"""
    response = requests.get(f'{BASE_URL}/api/customers')
    print_response("GET ALL CUSTOMERS", response)

def test_book_service():
    """Test book a service"""
    booking_data = {
        "name": "Service Test Customer",
        "email": "service@example.com",
        "phone": "+91-9876543210",
        "service_id": 1,
        "notes": "Need consultation for pest control"
    }
    
    response = requests.post(f'{BASE_URL}/api/services/book', json=booking_data)
    print_response("BOOK SERVICE", response)

def test_get_statistics():
    """Test get statistics"""
    response = requests.get(f'{BASE_URL}/api/stats')
    print_response("GET STATISTICS", response)

def test_global_search():
    """Test global search"""
    response = requests.get(f'{BASE_URL}/api/search?q=pest')
    print_response("GLOBAL SEARCH (pest)", response)

def test_add_product():
    """Test add new product"""
    product_data = {
        "name": "Test Pesticide",
        "category": "insecticide",
        "description": "Test product for API testing",
        "price": 99.99,
        "size": "1L Bottle",
        "stock": 50,
        "rating": 4.5
    }
    
    response = requests.post(f'{BASE_URL}/api/products', json=product_data)
    print_response("ADD NEW PRODUCT", response)
    
    if response.status_code == 201:
        return response.json().get('product_id')
    return None

def test_update_product(product_id):
    """Test update product"""
    if product_id:
        product_data = {
            "name": "Updated Test Pesticide",
            "category": "insecticide",
            "description": "Updated test product",
            "price": 89.99,
            "size": "1L Bottle",
            "stock": 75,
            "rating": 4.7
        }
        
        response = requests.put(f'{BASE_URL}/api/products/{product_id}', json=product_data)
        print_response(f"UPDATE PRODUCT ({product_id})", response)

def test_delete_product(product_id):
    """Test delete product"""
    if product_id:
        response = requests.delete(f'{BASE_URL}/api/products/{product_id}')
        print_response(f"DELETE PRODUCT ({product_id})", response)

def run_all_tests():
    """Run all API tests"""
    print("\n" + "="*60)
    print("AGRICHEM SOLUTIONS API TEST SUITE")
    print("="*60)
    print("Make sure the Flask server is running on http://localhost:5000")
    print("="*60)
    
    try:
        # Basic tests
        test_home()
        test_get_products()
        test_get_products_by_category()
        test_search_products()
        test_get_services()
        test_validate_discount()
        
        # Order tests
        order_id = test_create_order()
        test_get_orders()
        test_get_order_by_id(order_id)
        test_update_order_status(order_id)
        
        # Customer tests
        test_get_customers()
        
        # Service booking test
        test_book_service()
        
        # Statistics test
        test_get_statistics()
        
        # Search test
        test_global_search()
        
        # Product CRUD tests
        product_id = test_add_product()
        test_update_product(product_id)
        test_delete_product(product_id)
        
        print("\n" + "="*60)
        print("ALL TESTS COMPLETED!")
        print("="*60 + "\n")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to the server!")
        print("Please make sure the Flask server is running on http://localhost:5000")
        print("Run: python app.py")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")

if __name__ == '__main__':
    run_all_tests()
