// BurgerBlaze - Main JavaScript

// Initialize cart
let cart = JSON.parse(sessionStorage.getItem('cartItems') || '[]');
const sessionId = localStorage.getItem('sessionId') || 'session-' + Date.now();

// Cart UI elements
const cartToggle = document.getElementById('cart-toggle');
const cartSidebar = document.getElementById('cart-sidebar');
const cartClose = document.getElementById('cart-close');
const cartItemsContainer = document.getElementById('cart-items');
const cartCount = document.getElementById('cart-count');
const cartTotal = document.getElementById('cart-total');

// Initialize event listeners
document.addEventListener('DOMContentLoaded', function() {
    localStorage.setItem('sessionId', sessionId);
    updateCartUI();
    
    if (cartToggle) {
        cartToggle.addEventListener('click', function(e) {
            e.preventDefault();
            cartSidebar.classList.add('open');
        });
    }
    
    if (cartClose) {
        cartClose.addEventListener('click', function() {
            cartSidebar.classList.remove('open');
        });
    }
    
    // Close cart when clicking outside
    document.addEventListener('click', function(e) {
        if (!cartSidebar.contains(e.target) && !cartToggle.contains(e.target)) {
            cartSidebar.classList.remove('open');
        }
    });
});

/**
 * Add item to cart
 */
function addToCart(itemId, itemName, itemPrice) {
    const existingItem = cart.find(item => item.id === itemId);
    
    if (existingItem) {
        existingItem.quantity += 1;
    } else {
        cart.push({
            id: itemId,
            name: itemName,
            price: itemPrice,
            quantity: 1
        });
    }
    
    saveCart();
    updateCartUI();
    
    // Show confirmation
    showNotification('Added to cart!');
}

/**
 * Remove item from cart
 */
function removeFromCart(itemId) {
    cart = cart.filter(item => item.id !== itemId);
    saveCart();
    updateCartUI();
}

/**
 * Update item quantity in cart
 */
function updateQuantity(itemId, quantity) {
    const item = cart.find(item => item.id === itemId);
    if (item) {
        if (quantity <= 0) {
            removeFromCart(itemId);
        } else {
            item.quantity = quantity;
            saveCart();
            updateCartUI();
        }
    }
}

/**
 * Save cart to session storage
 */
function saveCart() {
    sessionStorage.setItem('cartItems', JSON.stringify(cart));
}

/**
 * Update cart UI - count, items display, and total
 */
function updateCartUI() {
    // Update cart count
    const totalItems = cart.reduce((sum, item) => sum + item.quantity, 0);
    cartCount.textContent = totalItems;
    
    // Update cart items display
    if (cartItemsContainer) {
        if (cart.length === 0) {
            cartItemsContainer.innerHTML = '<p style="text-align: center; color: #999;">Your cart is empty</p>';
        } else {
            cartItemsContainer.innerHTML = cart.map(item => `
                <div class="cart-item">
                    <div class="cart-item-info">
                        <div class="cart-item-name">${item.name}</div>
                        <div class="cart-item-qty">
                            <input type="number" min="1" value="${item.quantity}" 
                                   onchange="updateQuantity(${item.id}, this.value)"
                                   style="width: 50px; padding: 5px;">
                        </div>
                    </div>
                    <div>
                        <div class="cart-item-price">$${(item.price * item.quantity).toFixed(2)}</div>
                        <button onclick="removeFromCart(${item.id})" 
                                style="background: #f44336; color: white; border: none; padding: 5px 10px; border-radius: 4px; cursor: pointer;">
                            Remove
                        </button>
                    </div>
                </div>
            `).join('');
        }
    }
    
    // Update total
    const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
    if (cartTotal) {
        cartTotal.textContent = '$' + total.toFixed(2);
    }
}

/**
 * Go to order page
 */
function goToOrder() {
    window.location.href = '/order/';
}

/**
 * Show notification
 */
function showNotification(message) {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 80px;
        right: 20px;
        background: #4caf50;
        color: white;
        padding: 15px 20px;
        border-radius: 4px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.2);
        z-index: 2000;
        animation: slideIn 0.3s ease-out;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease-out';
        setTimeout(() => notification.remove(), 300);
    }, 2000);
}

// Add animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Fetch helper with CSRF token
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Export functions for global use
window.addToCart = addToCart;
window.removeFromCart = removeFromCart;
window.updateQuantity = updateQuantity;
window.goToOrder = goToOrder;
window.getCookie = getCookie;
