from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Category, Favorite, Order, Product


class MarketplaceFlowTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='buyer', password='strong-password-123')
        self.category = Category.objects.create(name='Test Goods', slug='test-goods')
        self.product = Product.objects.create(seller=self.user, category=self.category, name='Desk lamp', description='Bright lamp', price='120.00', quantity=3, location='Accra')

    def test_search_finds_product(self):
        response = self.client.get(reverse('shop'), {'q': 'lamp'})
        self.assertContains(response, 'Desk lamp')

    def test_authenticated_user_can_toggle_favorite(self):
        self.client.login(username='buyer', password='strong-password-123')
        self.client.get(reverse('toggle_favorite', args=[self.product.id]))
        self.assertTrue(Favorite.objects.filter(user=self.user, product=self.product).exists())

    def test_checkout_creates_order_and_reduces_stock(self):
        self.client.login(username='buyer', password='strong-password-123')
        self.client.get(reverse('add_to_cart', args=[self.product.id]))
        response = self.client.post(reverse('checkout'), {'full_name': 'Buyer Name', 'phone': '+233 20 000 0000', 'address': 'Accra'})
        self.assertRedirects(response, reverse('orders'))
        self.assertEqual(Order.objects.count(), 1)
        self.product.refresh_from_db()
        self.assertEqual(self.product.quantity, 2)

    def test_user_can_register(self):
        response = self.client.post(reverse('register'), {
            'username': 'newbuyer',
            'email': 'newbuyer@example.com',
            'password1': 'strong-password-456',
            'password2': 'strong-password-456',
        })
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_user_can_log_in(self):
        response = self.client.post(reverse('login'), {
            'username': 'buyer',
            'password': 'strong-password-123',
        })
        self.assertRedirects(response, reverse('home'))
        self.assertTrue(response.wsgi_request.user.is_authenticated)
