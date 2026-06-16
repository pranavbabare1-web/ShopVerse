"""
Management command: python manage.py setup_demo
Creates superuser, test user, loads sample data.
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from store.models import UserProfile


class Command(BaseCommand):
    help = 'Set up demo users and load sample data for ShopVerse'

    def handle(self, *args, **options):
        self.stdout.write(self.style.MIGRATE_HEADING('\n🛍️  ShopVerse Demo Setup\n'))

        # ── Superuser ─────────────────────────────────────────────────────────
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@shopverse.in',
                password='admin123',
                first_name='Admin',
                last_name='User',
            )
            UserProfile.objects.get_or_create(
                user=admin,
                defaults={
                    'phone': '+91 98765 43210',
                    'city': 'Mumbai',
                    'state': 'Maharashtra',
                    'country': 'India',
                }
            )
            self.stdout.write(self.style.SUCCESS('✅ Superuser created: admin / admin123'))
        else:
            self.stdout.write(self.style.WARNING('⚠️  Superuser "admin" already exists'))

        # ── Test User ─────────────────────────────────────────────────────────
        if not User.objects.filter(username='testuser').exists():
            user = User.objects.create_user(
                username='testuser',
                email='test@shopverse.in',
                password='test1234',
                first_name='Test',
                last_name='Shopper',
            )
            UserProfile.objects.get_or_create(
                user=user,
                defaults={
                    'phone': '+91 87654 32100',
                    'address': '42 MG Road',
                    'city': 'Bengaluru',
                    'state': 'Karnataka',
                    'zip_code': '560001',
                    'country': 'India',
                }
            )
            self.stdout.write(self.style.SUCCESS('✅ Test user created: testuser / test1234'))
        else:
            self.stdout.write(self.style.WARNING('⚠️  User "testuser" already exists'))

        self.stdout.write('\n' + self.style.SUCCESS(
            '🎉 Setup complete!\n\n'
            '   Admin Panel:  http://127.0.0.1:8000/admin/\n'
            '   Store:        http://127.0.0.1:8000/\n\n'
            '   Credentials:\n'
            '   ├─ admin    / admin123  (superuser)\n'
            '   └─ testuser / test1234  (regular user)\n'
        ))
