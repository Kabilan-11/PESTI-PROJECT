/**
 * API Integration for AgriChem Solutions
 * This file handles all communication with the Flask backend
 */

const API_BASE_URL = 'http://localhost:5000/api';

// ==================== PRODUCTS API ====================

/**
 * Fetch all products or filter by category
 */
async function fetchProducts(category = null, search = null) {
    try {
        let url = `${API_BASE_URL}/products`;
        const params = new URLSearchParams();
        
        if (category) params.append('category', category);
        if (search) params.append('search', search);
        
        if (params.toString()) url += `?${params.toString()}`;
        
        const response = await fetch(url);
        const data = await response.json();
        
        if (data.success) {
            return data.products;
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        console.error('Error fetching products:', error);
        showNotification('Failed to load products');
        return [];
    }
}

/**
 * Fetch single product by ID
 */
async function fetchProductById(productId) {
    try {
        const response = await fetch(`${API_BASE_URL}/products/${productId}`);
        const data = await response.json();
        
        if (data.success) {
            return data.product;
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        console.error('Error fetching product:', error);
        return null;
    }
}

// ==================== SERVICES API ====================

/**
 * Fetch all services
 */
async function fetchServices() {
    try {
        const response = await fetch(`${API_BASE_URL}/services`);
        const data = await response.json();
        
        if (data.success) {
            return data.services;
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        console.error('Error fetching services:', error);
        return [];
    }
}

/**
 * Book a service
 */
async function bookServiceAPI(serviceData) {
    try {
        const response = await fetch(`${API_BASE_URL}/services/book`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(serviceData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            showNotification('Service booked successfully!');
            return data;
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        console.error('Error booking service:', error);
        showNotification('Failed to book service');
        return null;
    }
}

// ==================== ORDERS API ====================

/**
 * Create a new order
 */
async function createOrderAPI(orderData) {
    try {
        const response = await fetch(`${API_BASE_URL}/orders`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(orderData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            return data;
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        console.error('Error creating order:', error);
        showNotification('Failed to create order');
        return null;
    }
}

/**
 * Fetch all orders
 */
async function fetchOrders() {
    try {
        const response = await fetch(`${API_BASE_URL}/orders`);
        const data = await response.json();
        
        if (data.success) {
            return data.orders;
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        console.error('Error fetching orders:', error);
        return [];
    }
}

/**
 * Fetch single order by ID
 */
async function fetchOrderById(orderId) {
    try {
        const response = await fetch(`${API_BASE_URL}/orders/${orderId}`);
        const data = await response.json();
        
        if (data.success) {
            return data.order;
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        console.error('Error fetching order:', error);
        return null;
    }
}

// ==================== DISCOUNT API ====================

/**
 * Validate discount code
 */
async function validateDiscountCode(code) {
    try {
        const response = await fetch(`${API_BASE_URL}/discount/validate`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code: code.toUpperCase() })
        });
        
        const data = await response.json();
        
        if (data.success && data.valid) {
            return {
                valid: true,
                percentage: data.discount_percentage
            };
        } else {
            return {
                valid: false,
                message: data.message || 'Invalid discount code'
            };
        }
    } catch (error) {
        console.error('Error validating discount:', error);
        return { valid: false, message: 'Failed to validate discount code' };
    }
}

// ==================== STATISTICS API ====================

/**
 * Fetch dashboard statistics
 */
async function fetchStatistics() {
    try {
        const response = await fetch(`${API_BASE_URL}/stats`);
        const data = await response.json();
        
        if (data.success) {
            return data.statistics;
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        console.error('Error fetching statistics:', error);
        return null;
    }
}

// ==================== SEARCH API ====================

/**
 * Global search
 */
async function globalSearch(query) {
    try {
        const response = await fetch(`${API_BASE_URL}/search?q=${encodeURIComponent(query)}`);
        const data = await response.json();
        
        if (data.success) {
            return data.results;
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        console.error('Error searching:', error);
        return { products: [], services: [], total: 0 };
    }
}

// ==================== ENHANCED FUNCTIONS ====================

/**
 * Enhanced submit order with API integration
 */
async function submitOrderWithAPI(event) {
    event.preventDefault();
    
    if (cart.length === 0) {
        alert('Please add items to your cart before submitting.');
        return;
    }

    const formData = new FormData(event.target);
    const orderData = {
        customer: {
            name: formData.get('name'),
            email: formData.get('email'),
            phone: formData.get('phone'),
            farm_size: formData.get('farm-size'),
            crop_type: formData.get('crop-type'),
            delivery: formData.get('delivery'),
            notes: formData.get('notes')
        },
        items: cart,
        total: document.getElementById('cart-total').textContent,
        discount_code: currentDiscountCode || null
    };

    // Show loading
    const submitBtn = event.target.querySelector('.btn-submit');
    const originalText = submitBtn.textContent;
    submitBtn.textContent = 'Processing...';
    submitBtn.disabled = true;

    // Create order via API
    const result = await createOrderAPI(orderData);
    
    if (result) {
        // Show success message
        showOrderConfirmation({
            orderNumber: result.order_number,
            total: result.final_total,
            items: cart,
            customer: orderData.customer,
            discount_applied: result.discount_applied
        });
        
        // Clear cart and form
        cart = [];
        updateCart();
        updateCartCount();
        saveCartToStorage();
        event.target.reset();
        currentDiscountCode = null;
    }
    
    // Reset button
    submitBtn.textContent = originalText;
    submitBtn.disabled = false;
}

/**
 * Enhanced discount validation with API
 */
async function applyDiscountWithAPI() {
    const discountCode = document.getElementById('discount-code').value.toUpperCase();
    const discountMessage = document.getElementById('discount-message');
    const cartTotal = parseFloat(document.getElementById('cart-total').textContent);
    
    if (!discountCode) {
        discountMessage.textContent = 'Please enter a discount code';
        discountMessage.style.color = '#f44336';
        return;
    }
    
    // Validate with API
    const result = await validateDiscountCode(discountCode);
    
    if (result.valid) {
        const discount = cartTotal * (result.percentage / 100);
        const newTotal = cartTotal - discount;
        
        document.getElementById('cart-total').textContent = newTotal.toFixed(2);
        discountMessage.textContent = `Discount applied! You saved ₹${discount.toFixed(2)} (${result.percentage}%)`;
        discountMessage.style.color = '#4caf50';
        showNotification(`Discount code ${discountCode} applied!`);
        
        // Store discount code for order submission
        currentDiscountCode = discountCode;
    } else {
        discountMessage.textContent = result.message;
        discountMessage.style.color = '#f44336';
    }
}

/**
 * Load products from API and display
 */
async function loadProductsFromAPI(category = null) {
    const products = await fetchProducts(category);
    
    if (products.length > 0) {
        displayProducts(products);
    }
}

/**
 * Display products in the grid
 */
function displayProducts(products) {
    const productsGrid = document.querySelector('.products-grid');
    if (!productsGrid) return;
    
    productsGrid.innerHTML = products.map(product => `
        <div class="product-card" data-category="${product.category}" data-aos="zoom-in">
            <div class="product-image">
                <img src="${product.image_url || 'https://via.placeholder.com/400x300/ef5350/ffffff?text=' + product.name}" 
                     alt="${product.name}" 
                     onerror="this.src='https://via.placeholder.com/400x300/ef5350/ffffff?text=${product.name}'">
                ${product.stock < 20 ? '<span class="badge">Low Stock</span>' : ''}
            </div>
            <div class="product-content">
                <div class="product-header">
                    <h3>${product.name}</h3>
                    <span class="category">${product.category}</span>
                </div>
                <p class="description">${product.description}</p>
                <div class="rating">⭐⭐⭐⭐${product.rating >= 4.5 ? '⭐' : '☆'} <span>(${product.rating})</span></div>
                <div class="product-details">
                    <span class="size">${product.size}</span>
                    <span class="price">₹${product.price.toFixed(2)}</span>
                </div>
                <div class="stock-info">Stock: ${product.stock} units</div>
                <button class="btn-add" onclick="addToCart('${product.name}', ${product.price}, '${product.category}')" 
                        ${product.stock === 0 ? 'disabled' : ''}>
                    <span>${product.stock === 0 ? 'Out of Stock' : 'Add to Cart'}</span> 🛒
                </button>
            </div>
        </div>
    `).join('');
}

/**
 * Enhanced search with API
 */
async function searchProductsWithAPI(query) {
    if (!query) {
        loadProductsFromAPI();
        return;
    }
    
    const products = await fetchProducts(null, query);
    displayProducts(products);
}

// ==================== INITIALIZATION ====================

// Store current discount code
let currentDiscountCode = null;

// Initialize API integration when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Load products from API
    // loadProductsFromAPI(); // Uncomment to load from API instead of static HTML
    
    // Replace form submit handler
    const orderForm = document.querySelector('.order-form');
    if (orderForm) {
        orderForm.removeEventListener('submit', submitOrder);
        orderForm.addEventListener('submit', submitOrderWithAPI);
    }
    
    console.log('API Integration loaded. Backend URL:', API_BASE_URL);
});

// Export functions for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        fetchProducts,
        fetchServices,
        createOrderAPI,
        validateDiscountCode,
        fetchStatistics,
        globalSearch
    };
}
