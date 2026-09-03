# MarketGo

MarketGo is a Django marketplace for buying and selling physical products in Ghana. It includes searchable listings, categories, seller publishing, favorites, a session cart, checkout, orders, reviews/reports models, image uploads, and Django admin moderation.

## Run locally

1. Install Python 3.12+ and create an environment: `python -m venv venv`
2. Activate it on Windows: `venv\\Scripts\\activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and set a production `SECRET_KEY`.
5. Run migrations: `python manage.py makemigrations marketplace` then `python manage.py migrate`
6. Create an admin user: `python manage.py createsuperuser`
7. Start the server: `python manage.py runserver`

Open `http://127.0.0.1:8000/`. Admin is at `/admin/`. Product images uploaded through admin are stored in `media/`; run `python manage.py collectstatic` for deployment. Set `DEBUG=False`, `ALLOWED_HOSTS`, and a strong secret in production. SQLite is used for development; switch the `DATABASES` setting to PostgreSQL credentials for production.
