// ===== Product Data =====
const products = [
    {
        id: 1,
        name: "Букет \"Нежность\"",
        desc: "Розовые пионы и белые розы",
        price: 3500,
        category: "bouquets",
        emoji: "\uD83C\uDF3A"
    },
    {
        id: 2,
        name: "Красные розы",
        desc: "Классический букет из 25 роз",
        price: 4200,
        category: "roses",
        emoji: "\uD83C\uDF39"
    },
    {
        id: 3,
        name: "Букет \"Весна\"",
        desc: "Тюльпаны, нарциссы, ирисы",
        price: 2800,
        category: "bouquets",
        emoji: "\uD83C\uDF37"
    },
    {
        id: 4,
        name: "Свадебный букет",
        desc: "Белые розы с зеленью эвкалипта",
        price: 5500,
        category: "wedding",
        emoji: "\uD83D\uDC90"
    },
    {
        id: 5,
        name: "Орхидея фаленопсис",
        desc: "Комнатная орхидея в горшке",
        price: 2200,
        category: "indoor",
        emoji: "\uD83C\uDF3C"
    },
    {
        id: 6,
        name: "Розы микс",
        desc: "Разноцветные розы, 15 штук",
        price: 2900,
        category: "roses",
        emoji: "\uD83C\uDF39"
    },
    {
        id: 7,
        name: "Букет невесты",
        desc: "Каскадный букет с лилиями",
        price: 6200,
        category: "wedding",
        emoji: "\uD83C\uDF38"
    },
    {
        id: 8,
        name: "Фикус Бенджамина",
        desc: "Красивое комнатное дерево",
        price: 1800,
        category: "indoor",
        emoji: "\uD83C\uDF3F"
    },
    {
        id: 9,
        name: "Букет \"Закат\"",
        desc: "Оранжевые герберы и хризантемы",
        price: 3100,
        category: "bouquets",
        emoji: "\uD83C\uDF3B"
    },
    {
        id: 10,
        name: "Белые розы",
        desc: "Элегантный букет из 21 розы",
        price: 3800,
        category: "roses",
        emoji: "\uD83E\uDEB7"
    },
    {
        id: 11,
        name: "Суккуленты",
        desc: "Набор из 3 суккулентов в горшках",
        price: 1500,
        category: "indoor",
        emoji: "\uD83C\uDF35"
    },
    {
        id: 12,
        name: "Букет \"Романтика\"",
        desc: "Розовые розы, гортензии, эустома",
        price: 4800,
        category: "bouquets",
        emoji: "\uD83C\uDF3A"
    }
];

// ===== Cart State =====
let cart = [];

// ===== DOM Elements =====
const catalogGrid = document.getElementById('catalog-grid');
const cartBtn = document.getElementById('cart-btn');
const cartCount = document.getElementById('cart-count');
const cartModal = document.getElementById('cart-modal');
const cartClose = document.getElementById('cart-close');
const cartItems = document.getElementById('cart-items');
const cartFooter = document.getElementById('cart-footer');
const cartTotalPrice = document.getElementById('cart-total-price');
const checkoutBtn = document.getElementById('checkout-btn');
const orderForm = document.getElementById('order-form');
const filterBtns = document.querySelectorAll('.filter-btn');

// ===== Render Products =====
function renderProducts(filter = 'all') {
    const filtered = filter === 'all'
        ? products
        : products.filter(p => p.category === filter);

    catalogGrid.innerHTML = filtered.map(product => {
        const inCart = cart.find(item => item.id === product.id);
        return `
            <div class="product-card" data-category="${product.category}">
                <div class="product-card__image">${product.emoji}</div>
                <div class="product-card__body">
                    <h3 class="product-card__name">${product.name}</h3>
                    <p class="product-card__desc">${product.desc}</p>
                    <div class="product-card__footer">
                        <span class="product-card__price">${product.price.toLocaleString('ru-RU')} \u20BD</span>
                        <button class="product-card__add ${inCart ? 'product-card__add--added' : ''}"
                                data-id="${product.id}">
                            ${inCart ? '\u2713 В корзине' : 'В корзину'}
                        </button>
                    </div>
                </div>
            </div>
        `;
    }).join('');

    // Attach click handlers to add-to-cart buttons
    document.querySelectorAll('.product-card__add').forEach(btn => {
        btn.addEventListener('click', () => {
            const id = parseInt(btn.dataset.id, 10);
            addToCart(id);
        });
    });
}

// ===== Cart Functions =====
function addToCart(productId) {
    const existing = cart.find(item => item.id === productId);
    if (existing) {
        existing.qty += 1;
    } else {
        cart.push({ id: productId, qty: 1 });
    }
    updateCartUI();
    showToast('Товар добавлен в корзину');
    renderProducts(getCurrentFilter());
}

function removeFromCart(productId) {
    cart = cart.filter(item => item.id !== productId);
    updateCartUI();
    renderCartModal();
    renderProducts(getCurrentFilter());
}

function changeQty(productId, delta) {
    const item = cart.find(item => item.id === productId);
    if (!item) return;
    item.qty += delta;
    if (item.qty <= 0) {
        removeFromCart(productId);
        return;
    }
    updateCartUI();
    renderCartModal();
}

function getCartTotal() {
    return cart.reduce((sum, item) => {
        const product = products.find(p => p.id === item.id);
        return sum + (product ? product.price * item.qty : 0);
    }, 0);
}

function getCartCount() {
    return cart.reduce((sum, item) => sum + item.qty, 0);
}

function updateCartUI() {
    cartCount.textContent = getCartCount();
}

function getCurrentFilter() {
    const active = document.querySelector('.filter-btn.active');
    return active ? active.dataset.filter : 'all';
}

// ===== Render Cart Modal =====
function renderCartModal() {
    if (cart.length === 0) {
        cartItems.innerHTML = '<p class="cart-empty">Корзина пуста</p>';
        cartFooter.style.display = 'none';
        return;
    }

    cartFooter.style.display = 'block';
    cartItems.innerHTML = cart.map(item => {
        const product = products.find(p => p.id === item.id);
        if (!product) return '';
        return `
            <div class="cart-item">
                <span class="cart-item__icon">${product.emoji}</span>
                <div class="cart-item__info">
                    <div class="cart-item__name">${product.name}</div>
                    <div class="cart-item__price">${(product.price * item.qty).toLocaleString('ru-RU')} \u20BD</div>
                </div>
                <div class="cart-item__controls">
                    <button class="cart-item__qty-btn" data-id="${product.id}" data-action="minus">&minus;</button>
                    <span class="cart-item__qty">${item.qty}</span>
                    <button class="cart-item__qty-btn" data-id="${product.id}" data-action="plus">+</button>
                </div>
            </div>
        `;
    }).join('');

    cartTotalPrice.textContent = getCartTotal().toLocaleString('ru-RU') + ' \u20BD';

    // Attach handlers
    cartItems.querySelectorAll('.cart-item__qty-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const id = parseInt(btn.dataset.id, 10);
            const delta = btn.dataset.action === 'plus' ? 1 : -1;
            changeQty(id, delta);
        });
    });
}

// ===== Modal Controls =====
cartBtn.addEventListener('click', () => {
    renderCartModal();
    cartModal.classList.add('open');
});

cartClose.addEventListener('click', () => {
    cartModal.classList.remove('open');
});

cartModal.addEventListener('click', (e) => {
    if (e.target === cartModal) {
        cartModal.classList.remove('open');
    }
});

// ===== Checkout =====
checkoutBtn.addEventListener('click', () => {
    cartModal.classList.remove('open');
    document.getElementById('contacts').scrollIntoView({ behavior: 'smooth' });
    showToast('Заполните форму для оформления заказа');
});

// ===== Filter =====
filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        renderProducts(btn.dataset.filter);
    });
});

// ===== Order Form =====
orderForm.addEventListener('submit', (e) => {
    e.preventDefault();
    const formData = new FormData(orderForm);
    cart = [];
    updateCartUI();
    renderProducts(getCurrentFilter());
    orderForm.reset();
    showToast('Спасибо! Ваша заявка принята. Мы свяжемся с вами.');
});

// ===== Toast Notification =====
let toastEl = null;

function showToast(message) {
    if (toastEl) {
        toastEl.remove();
    }
    toastEl = document.createElement('div');
    toastEl.className = 'toast';
    toastEl.textContent = message;
    document.body.appendChild(toastEl);

    requestAnimationFrame(() => {
        toastEl.classList.add('show');
    });

    setTimeout(() => {
        if (toastEl) {
            toastEl.classList.remove('show');
            setTimeout(() => {
                if (toastEl) {
                    toastEl.remove();
                    toastEl = null;
                }
            }, 300);
        }
    }, 3000);
}

// ===== Init =====
renderProducts();
