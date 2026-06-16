from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .models import Product, Category, Cart, CartItem, Order, OrderItem, UserProfile
from .forms import RegisterForm, LoginForm, ProfileForm, CheckoutForm


# ─── Helpers ─────────────────────────────────────────────────────────────────

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return cart
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, _ = Cart.objects.get_or_create(session_key=session_key, user=None)
        return cart


def merge_guest_cart(request):
    """Merge guest cart into user cart after login."""
    if not request.session.session_key:
        return
    try:
        guest_cart = Cart.objects.get(session_key=request.session.session_key, user=None)
        user_cart, _ = Cart.objects.get_or_create(user=request.user)
        for item in guest_cart.items.all():
            cart_item, created = CartItem.objects.get_or_create(cart=user_cart, product=item.product)
            if not created:
                cart_item.quantity += item.quantity
            else:
                cart_item.quantity = item.quantity
            cart_item.save()
        guest_cart.delete()
    except Cart.DoesNotExist:
        pass


# ─── Auth Views ───────────────────────────────────────────────────────────────

def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            merge_guest_cart(request)
            messages.success(request, f"Welcome to ShopVerse, {user.first_name or user.username}! 🎉")
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'store/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            merge_guest_cart(request)
            messages.success(request, f"Welcome back, {user.first_name or user.username}!")
            next_url = request.GET.get('next', 'home')
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = LoginForm(request)
    return render(request, 'store/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "You've been logged out. See you soon!")
    return redirect('home')


@login_required
def profile_view(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            # Update User model fields
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.email = form.cleaned_data['email']
            request.user.save()
            form.save()
            messages.success(request, "Profile updated successfully!")
            return redirect('profile')
    else:
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        form = ProfileForm(instance=profile, initial=initial)

    orders = request.user.orders.all()[:5]
    return render(request, 'store/profile.html', {'form': form, 'profile': profile, 'recent_orders': orders})


# ─── Store Views ──────────────────────────────────────────────────────────────

def home_view(request):
    featured_products = Product.objects.filter(is_featured=True, is_active=True)[:8]
    categories = Category.objects.all()
    new_arrivals = Product.objects.filter(is_active=True).order_by('-created_at')[:4]
    return render(request, 'store/home.html', {
        'featured_products': featured_products,
        'categories': categories,
        'new_arrivals': new_arrivals,
    })


def product_list_view(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.all()

    # Search
    query = request.GET.get('q', '')
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    # Category filter
    category_slug = request.GET.get('category', '')
    active_category = None
    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=active_category)

    # Sorting
    sort = request.GET.get('sort', '')
    sort_options = {
        'price_asc': 'price',
        'price_desc': '-price',
        'name_asc': 'name',
        'name_desc': '-name',
        'newest': '-created_at',
    }
    if sort in sort_options:
        products = products.order_by(sort_options[sort])

    return render(request, 'store/product_list.html', {
        'products': products,
        'categories': categories,
        'query': query,
        'active_category': active_category,
        'sort': sort,
        'total_count': products.count(),
    })


def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk, is_active=True)
    related = Product.objects.filter(category=product.category, is_active=True).exclude(pk=pk)[:4]
    return render(request, 'store/product_detail.html', {
        'product': product,
        'related_products': related,
    })


# ─── Cart Views ───────────────────────────────────────────────────────────────

def cart_view(request):
    cart = get_or_create_cart(request)
    return render(request, 'store/cart.html', {'cart': cart})


@require_POST
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    cart = get_or_create_cart(request)

    if not product.is_in_stock:
        messages.error(request, f"Sorry, {product.name} is out of stock.")
        return redirect('product_detail', pk=product_id)

    qty = int(request.POST.get('quantity', 1))
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += qty
    else:
        cart_item.quantity = qty

    # Cap at stock
    if cart_item.quantity > product.stock:
        cart_item.quantity = product.stock
        messages.warning(request, f"Only {product.stock} units available.")
    else:
        messages.success(request, f"'{product.name}' added to cart!")

    cart_item.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': cart.total_items,
            'message': f"'{product.name}' added to cart!"
        })
    return redirect('cart')


@require_POST
def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, pk=item_id)
    cart = get_or_create_cart(request)

    if cart_item.cart != cart:
        return redirect('cart')

    qty = int(request.POST.get('quantity', 1))
    if qty <= 0:
        cart_item.delete()
        messages.info(request, "Item removed from cart.")
    elif qty > cart_item.product.stock:
        cart_item.quantity = cart_item.product.stock
        cart_item.save()
        messages.warning(request, f"Only {cart_item.product.stock} units available.")
    else:
        cart_item.quantity = qty
        cart_item.save()
        messages.success(request, "Cart updated.")

    return redirect('cart')


@require_POST
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, pk=item_id)
    cart = get_or_create_cart(request)
    if cart_item.cart == cart:
        product_name = cart_item.product.name
        cart_item.delete()
        messages.info(request, f"'{product_name}' removed from cart.")
    return redirect('cart')


# ─── Checkout & Order Views ───────────────────────────────────────────────────

@login_required
def checkout_view(request):
    cart = get_or_create_cart(request)
    if not cart.items.exists():
        messages.warning(request, "Your cart is empty.")
        return redirect('cart')

    profile = getattr(request.user, 'profile', None)
    initial = {}
    if profile:
        initial = {
            'full_name': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
            'phone': profile.phone,
            'address': profile.address,
            'city': profile.city,
            'state': profile.state,
            'zip_code': profile.zip_code,
            'country': profile.country or 'India',
        }

    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user
            order.total_amount = cart.total_price
            order.status = 'pending'
            order.save()

            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    product_name=item.product.name,
                    quantity=item.quantity,
                    price=item.product.price,
                )
                # Reduce stock
                item.product.stock -= item.quantity
                item.product.save()

            cart.items.all().delete()
            messages.success(request, f"Order #{order.id} placed successfully! 🎉")
            return redirect('order_confirmation', order_id=order.id)
    else:
        form = CheckoutForm(initial=initial)

    return render(request, 'store/checkout.html', {'form': form, 'cart': cart})


@login_required
def order_confirmation_view(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    return render(request, 'store/order_confirmation.html', {'order': order})


@login_required
def order_history_view(request):
    orders = request.user.orders.all()
    return render(request, 'store/order_history.html', {'orders': orders})


@login_required
def order_detail_view(request, order_id):
    order = get_object_or_404(Order, pk=order_id, user=request.user)
    return render(request, 'store/order_detail.html', {'order': order})
