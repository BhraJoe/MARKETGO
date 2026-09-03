from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from .forms import CheckoutForm, ContactForm, ProductForm, RegistrationForm
from .models import Category, Favorite, Order, OrderItem, Product


def home(request):
    products = Product.objects.filter(active=True).select_related('category', 'seller').prefetch_related('images')
    return render(request, 'marketplace/home.html', {
        'featured': products.filter(featured=True)[:4],
        'latest': products[:8],
        'categories': Category.objects.all()[:8],
        'product_count': products.count(),
        'seller_count': products.values('seller').distinct().count(),
        'category_count': Category.objects.count(),
    })


def shop(request):
    products = Product.objects.filter(active=True).select_related('category', 'seller').prefetch_related('images')
    query, category = request.GET.get('q', '').strip(), request.GET.get('category', '')
    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query) | Q(brand__icontains=query) | Q(location__icontains=query))
    if category:
        products = products.filter(category__slug=category)
    sort = request.GET.get('sort', '-created_at')
    if sort in ('price', '-price', '-views', '-created_at'):
        products = products.order_by(sort)
    page_size = products.count() or 1 if not query and not category else 12
    page = Paginator(products, page_size).get_page(request.GET.get('page', 1))
    context = {'products': page, 'categories': Category.objects.all(), 'query': query, 'selected_category': category}
    if request.GET.get('partial'):
        response = render(request, 'marketplace/shop_products.html', context)
        response['X-Has-Next'] = 'true' if page.has_next() else 'false'
        return response
    return render(request, 'marketplace/shop.html', context)


def product_detail(request, slug):
    product = get_object_or_404(Product.objects.select_related('seller', 'category').prefetch_related('images'), slug=slug, active=True)
    Product.objects.filter(pk=product.pk).update(views=product.views + 1)
    return render(request, 'marketplace/product_detail.html', {'product': product, 'is_favorite': request.user.is_authenticated and Favorite.objects.filter(user=request.user, product=product).exists()})


@login_required
def create_product(request):
    form = ProductForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        product = form.save(commit=False)
        product.seller = request.user
        product.save()
        messages.success(request, 'Your listing is live.')
        return redirect(product.get_absolute_url())
    return render(request, 'marketplace/form.html', {'form': form})


@login_required
def toggle_favorite(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
    if not created:
        favorite.delete()
    return redirect(request.META.get('HTTP_REFERER', product.get_absolute_url()))


def _cart_products(request):
    cart_data = request.session.get('cart', {})
    products = Product.objects.filter(id__in=cart_data, active=True).prefetch_related('images')
    return [(product, cart_data.get(str(product.id), 1), product.price * cart_data.get(str(product.id), 1)) for product in products]


def cart(request):
    items = _cart_products(request)
    return render(request, 'marketplace/cart.html', {'items': items, 'total': sum((item[2] for item in items), Decimal('0'))})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id, active=True)
    cart_data = request.session.setdefault('cart', {})
    key = str(product.id)
    cart_data[key] = min(cart_data.get(key, 0) + 1, product.quantity)
    request.session['cart'] = cart_data
    messages.success(request, f'{product.name} added to your cart.')
    return redirect(request.META.get('HTTP_REFERER', 'cart'))


def remove_from_cart(request, product_id):
    cart_data = request.session.get('cart', {})
    cart_data.pop(str(product_id), None)
    request.session['cart'] = cart_data
    return redirect('cart')


@login_required
def checkout(request):
    items = _cart_products(request)
    if not items:
        return redirect('cart')
    total = sum((item[2] for item in items), Decimal('0'))
    form = CheckoutForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        order = Order.objects.create(user=request.user, total=total, **form.cleaned_data)
        for product, quantity, price in items:
            OrderItem.objects.create(order=order, product=product, quantity=quantity, price=product.price)
            product.quantity = max(0, product.quantity - quantity)
            product.save(update_fields=['quantity'])
        request.session['cart'] = {}
        messages.success(request, 'Order placed. The seller will confirm it shortly.')
        return redirect('orders')
    return render(request, 'marketplace/checkout.html', {'form': form, 'items': items, 'total': total})


@login_required
def orders(request):
    return render(request, 'marketplace/orders.html', {'orders': request.user.orders.prefetch_related('items__product')})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        user = authenticate(request, username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect(request.POST.get('next') or request.GET.get('next') or 'home')
        messages.error(request, 'Those login details were not recognized.')
    return render(request, 'registration/login.html', {'next': request.GET.get('next', '')})


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    form = RegistrationForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, 'Your MarketGo account is ready.')
        return redirect(request.POST.get('next') or 'home')
    return render(request, 'registration/register.html', {'form': form, 'next': request.GET.get('next', '')})


def logout_view(request):
    logout(request)
    return redirect('home')


def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        messages.success(request, 'Thanks. Your message has been received by the MarketGo team.')
        form = ContactForm()
    return render(request, 'marketplace/info.html', {
        'eyebrow': 'HELP & SUPPORT',
        'title': 'We are here to help.',
        'intro': 'Reach the MarketGo team with questions about buying, selling, or using the marketplace.',
        'sections': [
            ('Email', 'hello@marketgo.gh'),
            ('Safety reports', 'safety@marketgo.gh'),
            ('Response time', 'We aim to respond within one business day.'),
        ],
        'contact_form': form,
        'faqs': [
            ('How do I report a listing?', 'Choose Report a listing in the form and include the listing name or URL.'),
            ('How do I sell something?', 'Use Sell something in the navigation, complete the listing details, and publish it.'),
            ('How are payments handled?', 'Agree on payment and handover details directly with the seller before completing the transaction.'),
        ],
    })


def safety(request):
    return render(request, 'marketplace/info.html', {
        'eyebrow': 'SAFETY FIRST',
        'title': 'Buy and sell with confidence.',
        'intro': 'A few simple habits help every MarketGo transaction stay clear and comfortable.',
        'sections': [
            ('Meet safely', 'Choose a public place and tell someone where you are going.'),
            ('Check before paying', 'Inspect the product and agree on the details before exchanging money.'),
            ('Protect your account', 'Never share your password, verification codes, or sensitive payment details.'),
            ('Report concerns', 'Contact safety@marketgo.gh if a listing or seller seems suspicious.'),
        ],
    })


def policies(request):
    return render(request, 'marketplace/info.html', {
        'eyebrow': 'MARKETGO POLICIES',
        'title': 'Clear rules for a better market.',
        'intro': 'MarketGo exists for honest buying and selling of physical products.',
        'sections': [
            ('Use the marketplace responsibly', 'List accurate products, use your own photographs where possible, and communicate honestly.'),
            ('Respect privacy', 'Only share the personal information needed to arrange a transaction.'),
            ('Prohibited activity', 'Fraud, unsafe products, counterfeit goods, harassment, and illegal products are not allowed.'),
            ('Need help?', 'Contact hello@marketgo.gh with questions about these policies.'),
        ],
    })
