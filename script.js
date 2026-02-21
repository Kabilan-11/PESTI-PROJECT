// Cart Management
let cart = [];

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    loadCartFromStorage();
    animateNumbers();
    handleScroll();
    initializeEventListeners();
    updateCartCount();
});

// Load cart from localStorage
function loadCartFromStorage() {
    const savedCart = localStorage.getItem('pesticidesCart');
    if (savedCart) {
        cart = JSON.parse(savedCart);
        updateCart();
        updateCartCount();
    }
}

// Save cart to localStorage
function saveCartToStorage() {
    localStorage.setItem('pesticidesCart', JSON.stringify(cart));
}

// Add to cart with quantity
function addToCart(product, price, category) {
    const existingItem = cart.find(item => item.product === product);
    
    if (existingItem) {
        existingItem.quantity += 1;
        showNotification(`${product} quantity increased!`);
    } else {
        cart.push({ 
            product, 
            price, 
            category,
            quantity: 1,
            id: Date.now()
        });
        showNotification(`${product} added to cart!`);
    }
    
    updateCart();
    updateCartCount();
    saveCartToStorage();
}

// Remove from cart
function removeFromCart(index) {
    const removedItem = cart[index];
    cart.splice(index, 1);
    updateCart();
    updateCartCount();
    saveCartToStorage();
    showNotification(`${removedItem.product} removed from cart`);
}

// Update quantity
function updateQuantity(index, change) {
    if (cart[index]) {
        cart[index].quantity += change;
        
        if (cart[index].quantity <= 0) {
            removeFromCart(index);
        } else {
            updateCart();
            updateCartCount();
            saveCartToStorage();
        }
    }
}

// Clear entire cart
function clearCart() {
    if (cart.length === 0) {
        showNotification('Cart is already empty!');
        return;
    }
    
    if (confirm('Are you sure you want to clear the entire cart?')) {
        cart = [];
        updateCart();
        updateCartCount();
        saveCartToStorage();
        showNotification('Cart cleared successfully!');
    }
}

// Update cart display
function updateCart() {
    const cartItems = document.getElementById('cart-items');
    const cartTotal = document.getElementById('cart-total');
    
    if (cart.length === 0) {
        cartItems.innerHTML = '<p class="empty-cart">Your cart is empty</p>';
        cartTotal.textContent = '0.00';
        return;
    }

    let html = '';
    let total = 0;
    
    cart.forEach((item, index) => {
        const itemTotal = item.price * item.quantity;
        total += itemTotal;
        html += `
            <div class="cart-item">
                <div class="cart-item-details">
                    <span class="cart-item-name">${item.product}</span>
                    <span class="cart-item-category">${item.category}</span>
                </div>
                <div class="cart-item-controls">
                    <button class="btn-quantity" onclick="updateQuantity(${index}, -1)">-</button>
                    <span class="quantity">${item.quantity}</span>
                    <button class="btn-quantity" onclick="updateQuantity(${index}, 1)">+</button>
                </div>
                <span class="cart-item-price">₹${itemTotal.toFixed(2)}</span>
                <button class="btn-remove" onclick="removeFromCart(${index})">×</button>
            </div>
        `;
    });
    
    cartItems.innerHTML = html;
    cartTotal.textContent = total.toFixed(2);
}

// Update cart count badge
function updateCartCount() {
    const cartCount = document.getElementById('cart-count');
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    cartCount.textContent = totalItems;
    
    if (totalItems > 0) {
        cartCount.style.display = 'flex';
    } else {
        cartCount.style.display = 'none';
    }
}

// Animate numbers on scroll
function animateNumbers() {
    const stats = document.querySelectorAll('.stat-number');
    stats.forEach(stat => {
        const target = parseInt(stat.getAttribute('data-target'));
        const increment = target / 50;
        let current = 0;
        
        const updateCount = () => {
            if (current < target) {
                current += increment;
                stat.textContent = Math.ceil(current) + '+';
                setTimeout(updateCount, 30);
            } else {
                stat.textContent = target + '+';
            }
        };
        updateCount();
    });
}

// Animate on scroll
function handleScroll() {
    const elements = document.querySelectorAll('[data-aos]');
    elements.forEach(el => {
        const rect = el.getBoundingClientRect();
        if (rect.top < window.innerHeight - 100) {
            el.classList.add('aos-animate');
        }
    });
}

// Sticky navbar
window.addEventListener('scroll', () => {
    const navbar = document.getElementById('navbar');
    if (window.scrollY > 100) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
    handleScroll();
});

// Filter products
function filterProducts(category) {
    const products = document.querySelectorAll('.product-card');
    const buttons = document.querySelectorAll('.filter-btn');
    
    buttons.forEach(btn => btn.classList.remove('active'));
    event.target.classList.add('active');
    
    products.forEach(product => {
        if (category === 'all' || product.getAttribute('data-category') === category) {
            product.style.display = 'block';
            setTimeout(() => product.style.opacity = '1', 10);
        } else {
            product.style.opacity = '0';
            setTimeout(() => product.style.display = 'none', 300);
        }
    });
}

// Book service
function bookService(service) {
    showNotification(`Booking ${service}... We'll contact you soon!`);
    document.getElementById('order').scrollIntoView({ behavior: 'smooth' });
    
    // Pre-fill service in notes
    const notesField = document.getElementById('notes');
    if (notesField) {
        notesField.value = `Interested in: ${service}`;
    }
}

// Toggle cart visibility on mobile
function toggleCart() {
    const cartSummary = document.querySelector('.cart-summary');
    cartSummary.classList.toggle('show-mobile');
}

// Submit order form
function submitOrder(event) {
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
            farmSize: formData.get('farm-size'),
            cropType: formData.get('crop-type'),
            delivery: formData.get('delivery'),
            notes: formData.get('notes')
        },
        items: cart,
        total: document.getElementById('cart-total').textContent,
        orderDate: new Date().toISOString(),
        orderNumber: 'ORD-' + Date.now()
    };

    console.log('Order submitted:', orderData);
    
    // Save order to localStorage
    saveOrder(orderData);
    
    // Show success message
    showOrderConfirmation(orderData);
    
    // Clear cart and form
    cart = [];
    updateCart();
    updateCartCount();
    saveCartToStorage();
    event.target.reset();
}

// Save order to localStorage
function saveOrder(orderData) {
    let orders = JSON.parse(localStorage.getItem('pesticidesOrders') || '[]');
    orders.push(orderData);
    localStorage.setItem('pesticidesOrders', JSON.stringify(orders));
}

// Show order confirmation
function showOrderConfirmation(orderData) {
    const modal = document.createElement('div');
    modal.className = 'order-modal';
    modal.innerHTML = `
        <div class="order-modal-content">
            <div class="order-success-icon">✓</div>
            <h2>Order Placed Successfully!</h2>
            <p class="order-number">Order Number: <strong>${orderData.orderNumber}</strong></p>
            <div class="order-summary">
                <p><strong>Total Amount:</strong> ₹${orderData.total}</p>
                <p><strong>Items:</strong> ${orderData.items.length} product(s)</p>
                <p><strong>Delivery to:</strong> ${orderData.customer.name}</p>
            </div>
            <p class="order-message">We'll contact you at <strong>${orderData.customer.phone}</strong> to confirm your order.</p>
            <button class="btn-close-modal" onclick="closeOrderModal()">Close</button>
        </div>
    `;
    document.body.appendChild(modal);
    
    setTimeout(() => {
        modal.classList.add('show');
    }, 10);
}

// Close order modal
function closeOrderModal() {
    const modal = document.querySelector('.order-modal');
    if (modal) {
        modal.classList.remove('show');
        setTimeout(() => modal.remove(), 300);
    }
}

// Show notification
function showNotification(message) {
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Search functionality
function searchProducts(query) {
    const products = document.querySelectorAll('.product-card');
    const searchTerm = query.toLowerCase();
    
    products.forEach(product => {
        const productName = product.querySelector('h3').textContent.toLowerCase();
        const productDesc = product.querySelector('.description').textContent.toLowerCase();
        
        if (productName.includes(searchTerm) || productDesc.includes(searchTerm)) {
            product.style.display = 'block';
            product.style.opacity = '1';
        } else {
            product.style.opacity = '0';
            setTimeout(() => product.style.display = 'none', 300);
        }
    });
}

// Apply discount code
function applyDiscount() {
    const discountCode = document.getElementById('discount-code').value.toUpperCase();
    const discountMessage = document.getElementById('discount-message');
    const cartTotal = parseFloat(document.getElementById('cart-total').textContent);
    
    const discounts = {
        'SAVE10': 0.10,
        'SAVE20': 0.20,
        'FIRST50': 0.50,
        'BULK15': 0.15
    };
    
    if (discounts[discountCode]) {
        const discount = cartTotal * discounts[discountCode];
        const newTotal = cartTotal - discount;
        
        document.getElementById('cart-total').textContent = newTotal.toFixed(2);
        discountMessage.textContent = `Discount applied! You saved ₹${discount.toFixed(2)}`;
        discountMessage.style.color = '#4caf50';
        showNotification(`Discount code ${discountCode} applied!`);
    } else {
        discountMessage.textContent = 'Invalid discount code';
        discountMessage.style.color = '#f44336';
    }
}

// View order history
function viewOrderHistory() {
    const orders = JSON.parse(localStorage.getItem('pesticidesOrders') || '[]');
    
    if (orders.length === 0) {
        showNotification('No order history found');
        return;
    }
    
    const modal = document.createElement('div');
    modal.className = 'order-modal';
    
    let ordersHTML = orders.map(order => `
        <div class="history-item">
            <strong>${order.orderNumber}</strong>
            <span>${new Date(order.orderDate).toLocaleDateString()}</span>
            <span>₹${order.total}</span>
            <span>${order.items.length} items</span>
        </div>
    `).join('');
    
    modal.innerHTML = `
        <div class="order-modal-content">
            <h2>Order History</h2>
            <div class="order-history">
                ${ordersHTML}
            </div>
            <button class="btn-close-modal" onclick="closeOrderModal()">Close</button>
        </div>
    `;
    
    document.body.appendChild(modal);
    setTimeout(() => modal.classList.add('show'), 10);
}

// Initialize event listeners
function initializeEventListeners() {
    // Smooth scrolling for navigation
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
            }
        });
    });
    
    // Form validation
    const orderForm = document.querySelector('.order-form');
    if (orderForm) {
        orderForm.addEventListener('submit', submitOrder);
        
        // Real-time validation
        const emailInput = document.getElementById('email');
        if (emailInput) {
            emailInput.addEventListener('blur', function() {
                const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                if (!emailPattern.test(this.value)) {
                    this.style.borderColor = '#f44336';
                } else {
                    this.style.borderColor = '#ffcdd2';
                }
            });
        }
        
        const phoneInput = document.getElementById('phone');
        if (phoneInput) {
            phoneInput.addEventListener('input', function() {
                this.value = this.value.replace(/[^0-9+\-() ]/g, '');
            });
        }
    }
    
    // Back to top button
    createBackToTopButton();
}

// Create back to top button
function createBackToTopButton() {
    const backToTop = document.createElement('button');
    backToTop.className = 'back-to-top';
    backToTop.innerHTML = '↑';
    backToTop.onclick = () => window.scrollTo({ top: 0, behavior: 'smooth' });
    document.body.appendChild(backToTop);
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 300) {
            backToTop.classList.add('show');
        } else {
            backToTop.classList.remove('show');
        }
    });
}

// Print order summary
function printOrderSummary() {
    if (cart.length === 0) {
        showNotification('Cart is empty!');
        return;
    }
    
    const printWindow = window.open('', '', 'height=600,width=800');
    const total = document.getElementById('cart-total').textContent;
    
    let itemsHTML = cart.map(item => `
        <tr>
            <td>${item.product}</td>
            <td>${item.quantity}</td>
            <td>₹${item.price.toFixed(2)}</td>
            <td>₹${(item.price * item.quantity).toFixed(2)}</td>
        </tr>
    `).join('');
    
    printWindow.document.write(`
        <html>
        <head>
            <title>Order Summary</title>
            <style>
                body { font-family: Arial, sans-serif; padding: 20px; }
                h1 { color: #c62828; }
                table { width: 100%; border-collapse: collapse; margin: 20px 0; }
                th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
                th { background-color: #ef5350; color: white; }
                .total { font-size: 1.5em; font-weight: bold; text-align: right; margin-top: 20px; }
            </style>
        </head>
        <body>
            <h1>AgriChem Solutions - Order Summary</h1>
            <p>Date: ${new Date().toLocaleDateString()}</p>
            <table>
                <thead>
                    <tr>
                        <th>Product</th>
                        <th>Quantity</th>
                        <th>Price</th>
                        <th>Total</th>
                    </tr>
                </thead>
                <tbody>
                    ${itemsHTML}
                </tbody>
            </table>
            <div class="total">Total: ₹${total}</div>
        </body>
        </html>
    `);
    
    printWindow.document.close();
    printWindow.print();
}

// Export cart as JSON
function exportCart() {
    if (cart.length === 0) {
        showNotification('Cart is empty!');
        return;
    }
    
    const dataStr = JSON.stringify(cart, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = 'cart-' + Date.now() + '.json';
    link.click();
    URL.revokeObjectURL(url);
    showNotification('Cart exported successfully!');
}
