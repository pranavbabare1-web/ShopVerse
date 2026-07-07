# 🛍️ ShopVerse — Full-Stack E-Commerce Website

A complete, production-ready e-commerce web application built with **Django + SQLite + Vanilla JS**.

---

## 📁 Project Structure

```
ecommerce/
│
├── manage.py
├── requirements.txt
├── db.sqlite3                    ← auto-created after migration
│
├── ecommerce/                    ← Django project package
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── store/                        ← Main app
│   ├── __init__.py
│   ├── apps.py
│   ├── models.py                 ← All DB models
│   ├── views.py                  ← All views
│   ├── urls.py                   ← URL patterns
│   ├── forms.py                  ← Django forms
│   ├── admin.py                  ← Admin configuration
│   ├── context_processors.py     ← Cart count context
│   ├── fixtures/
│   │   └── initial_data.json     ← Sample categories & products
│   └── management/
│       └── commands/
│           └── setup_demo.py     ← Demo user setup command
│
├── templates/
│   └── store/
│       ├── base.html             ← Base layout (navbar, footer)
│       ├── home.html             ← Homepage
│       ├── product_list.html     ← Shop / product listing
│       ├── product_detail.html   ← Single product page
│       ├── cart.html             ← Shopping cart
│       ├── checkout.html         ← Checkout form
│       ├── order_confirmation.html
│       ├── order_history.html
│       ├── order_detail.html
│       ├── register.html
│       ├── login.html
│       ├── profile.html
│       └── partials/
│           └── product_card.html ← Reusable product card
│
├── static/
│   ├── css/
│   │   └── style.css             ← Complete design system
│   ├── js/
│   │   └── main.js               ← Interactive features
│   └── images/
│       └── no-image.svg
│
└── media/                        ← User-uploaded product images
    └── products/
```

---

## ⚡ Quick Setup (5 Steps)

### Step 1 — Clone / Extract the project
```bash
# If you downloaded a zip, extract it, then:
cd ecommerce
```

### Step 2 — Create virtual environment & install dependencies
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate

# Install packages
pip install -r requirements.txt
```

### Step 3 — Run database migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 4 — Load sample data & create demo users
```bash
# Load sample categories and 18 products
python manage.py loaddata store/fixtures/initial_data.json

# Create admin + test user automatically
python manage.py setup_demo
```

### Step 5 — Start the development server
```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000** in your browser 🎉
LIVE DEMO : https://shopverse-9jdb.onrender.com/

---

## 🔑 Demo Credentials

| Role       | Username   | Password   | Access                          |
|------------|------------|------------|----------------------------------|
| Admin      | `admin`    | `admin123` | Full admin panel + store         |
| Test User  | `testuser` | `test1234` | Regular shopping account         |

**Admin Panel:** http://127.0.0.1:8000/admin/

---

## 🌐 URL Reference

| URL                            | View                    | Auth Required |
|--------------------------------|-------------------------|---------------|
| `/`                            | Homepage                | No            |
| `/products/`                   | Product listing         | No            |
| `/products/<id>/`              | Product detail          | No            |
| `/cart/`                       | Shopping cart           | No            |
| `/cart/add/<id>/`              | Add to cart (POST)      | No            |
| `/cart/update/<id>/`           | Update quantity (POST)  | No            |
| `/cart/remove/<id>/`           | Remove item (POST)      | No            |
| `/checkout/`                   | Checkout form           | ✅ Yes        |
| `/order/<id>/confirmation/`    | Order confirmation      | ✅ Yes        |
| `/orders/`                     | Order history           | ✅ Yes        |
| `/orders/<id>/`                | Order detail            | ✅ Yes        |
| `/register/`                   | User registration       | No            |
| `/login/`                      | User login              | No            |
| `/logout/`                     | Logout (POST)           | ✅ Yes        |
| `/profile/`                    | User profile            | ✅ Yes        |
| `/admin/`                      | Django admin panel      | Staff only    |

---

## 🗃️ Database Models

### Category
| Field       | Type         | Notes                  |
|-------------|--------------|------------------------|
| id          | AutoField    | Primary key            |
| name        | CharField    | Category name          |
| slug        | SlugField    | URL-friendly name      |
| description | TextField    | Optional description   |
| icon        | CharField    | Font Awesome class     |
| created_at  | DateTimeField| Auto timestamp         |

### Product
| Field       | Type           | Notes                   |
|-------------|----------------|-------------------------|
| id          | AutoField      | Primary key             |
| name        | CharField      | Product name            |
| description | TextField      | Full description        |
| price       | DecimalField   | Price in ₹              |
| image       | ImageField     | Uploaded to media/      |
| stock       | PositiveIntField | Available quantity    |
| category    | ForeignKey     | → Category              |
| is_featured | BooleanField   | Show on homepage        |
| is_active   | BooleanField   | Toggle visibility       |
| created_at  | DateTimeField  | Auto timestamp          |

### Cart & CartItem
| Cart Field  | Type           | Notes                   |
|-------------|----------------|-------------------------|
| user        | OneToOneField  | Null for guests         |
| session_key | CharField      | For guest carts         |

| CartItem Field | Type        | Notes                   |
|----------------|-------------|-------------------------|
| cart           | ForeignKey  | → Cart                  |
| product        | ForeignKey  | → Product               |
| quantity       | PositiveInt | Item quantity           |

### Order & OrderItem
| Order Field   | Type          | Notes                       |
|---------------|---------------|-----------------------------|
| user          | ForeignKey    | → User                      |
| total_amount  | DecimalField  | Total in ₹                  |
| status        | CharField     | pending/processing/shipped/delivered/cancelled |
| full_name     | CharField     | Shipping name               |
| email         | EmailField    | Contact email               |
| phone         | CharField     | Contact phone               |
| address       | TextField     | Street address              |
| city/state/zip/country | CharField | Shipping address  |

---

## 🛠️ Admin Panel Features

Log in at `/admin/` with admin credentials to:

- **Products** — Add/edit/delete products, set featured, toggle active, manage stock, bulk-edit price
- **Categories** — Add categories with icons (Font Awesome class names)
- **Orders** — View all orders, update order status (bulk or individual)
- **Users** — Manage user accounts and profiles
- **Carts** — View guest and user carts

### Adding a Product via Admin
1. Go to `/admin/store/product/add/`
2. Fill in name, description, price, stock
3. Select category
4. Upload product image (stored in `media/products/`)
5. Check "Is featured" to show on homepage
6. Save

---

## ✨ Features Implemented

### User Authentication
- ✅ Registration with email, first/last name
- ✅ Login / Logout
- ✅ Session-based authentication
- ✅ Password hashing (Django's PBKDF2)
- ✅ Protected routes with `@login_required`
- ✅ Guest cart merging on login
- ✅ Profile page with editable details

### Homepage
- ✅ Hero section with animated elements
- ✅ Trust badges strip
- ✅ Categories grid
- ✅ Featured products
- ✅ Promo banners
- ✅ New arrivals
- ✅ Newsletter signup
- ✅ Responsive navbar + mobile hamburger menu

### Products
- ✅ Product listing with grid layout
- ✅ Product detail page
- ✅ Category sidebar filtering
- ✅ Search by name/description
- ✅ Sort by price (asc/desc), name (asc/desc), newest
- ✅ Related products section
- ✅ Stock indicator
- ✅ Featured badge

### Shopping Cart
- ✅ Add to cart (AJAX for quick-add, standard for detail page)
- ✅ Update quantity with +/− controls
- ✅ Remove items
- ✅ Subtotal calculation per item
- ✅ Cart total with conditional free shipping
- ✅ Persistent cart for logged-in users
- ✅ Guest cart (session-based)
- ✅ Cart count badge in navbar

### Checkout
- ✅ Shipping address form (pre-filled from profile)
- ✅ Order summary with product images
- ✅ Total + shipping calculation
- ✅ Order placement with stock decrement
- ✅ Order confirmation page with status tracker

### Order Management
- ✅ Order history page
- ✅ Order detail with all items
- ✅ Status tracking: Pending → Processing → Shipped → Delivered
- ✅ Admin can update order status

---

## 🎨 Design System

The project uses CSS Custom Properties (variables) for a cohesive design:

- **Primary:** `#6c47ff` (vibrant purple)
- **Accent:** `#ff6b6b` (coral red)
- **Success:** `#10b981` (emerald green)
- **Font:** Inter (Google Fonts)
- **Shadows:** Layered box shadows for depth
- **Radius:** Consistent border radius scale

---

## 🚀 Adding Products with Images

1. Place product images in `media/products/`
2. In admin, edit a product and upload its image
3. Or via shell:
```python
python manage.py shell
from store.models import Product
p = Product.objects.get(pk=1)
p.image = 'products/my-image.jpg'
p.save()
```

---

## 🔧 Common Commands

```bash
# Create new superuser manually
python manage.py createsuperuser

# Reset and reload sample data
python manage.py flush --no-input
python manage.py migrate
python manage.py loaddata store/fixtures/initial_data.json
python manage.py setup_demo

# Collect static files (for production)
python manage.py collectstatic

# Open Django shell
python manage.py shell
```

---

## 📦 Dependencies

| Package              | Version | Purpose                    |
|----------------------|---------|----------------------------|
| Django               | 4.2.7   | Web framework              |
| Pillow               | 10.1.0  | Image processing           |
| django-crispy-forms  | 2.1     | Form rendering (available) |
| crispy-bootstrap5    | 0.7     | Bootstrap 5 crispy pack    |

CDN dependencies (no install needed):
- Font Awesome 6.5 (icons)
- Google Fonts — Inter & Playfair Display

---

Built with ❤️ using Django + Vanilla JS
