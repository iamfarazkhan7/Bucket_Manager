# File: README.md
# Bucket Manager

A production-ready Django 5 application for managing buckets with user authentication, staff-only access, and full CRUD operations.

## Features

- **Authentication System**: Django's built-in auth with custom signup/login views
- **Staff-Only Access**: Only staff users can access bucket management features
- **Bucket Management**: Full CRUD operations for buckets (Create, Read, Update, Delete)
- **User Scoping**: Users can only see and manage their own buckets
- **Responsive UI**: Bootstrap 5 with mobile-friendly design
- **Production Ready**: Docker support, PostgreSQL, static file handling
- **Admin Interface**: Django admin with proper permissions and filtering

## Quick Start

### Local Development

1. **Clone and setup the project:**
```bash
git clone <repository-url>
cd bucket_manager
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Setup environment:**
```bash
cp .env.example .env
# Edit .env with your settings
```

4. **Run the development setup:**
```bash
chmod +x scripts/dev.sh
./scripts/dev.sh
```

The application will be available at `http://localhost:8000`

### Docker Development

1. **Run with Docker Compose:**
```bash
docker-compose up --build
```

The application will be available at `http://localhost:8000`

## Environment Variables

Create a `.env` file based on `.env.example`:

```env
SECRET_KEY=your-secret-key-here
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
ADMIN_USER=admin
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=admin123
```

### Production Environment Variables

For production, set these environment variables:

```env
SECRET_KEY=your-production-secret-key
DEBUG=False
DATABASE_URL=postgresql://user:password@host:port/database
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
ADMIN_USER=admin
ADMIN_EMAIL=admin@yourdomain.com
ADMIN_PASSWORD=secure-password
```

## Project Structure

```
bucket_manager/
├── manage.py                 # Django management script
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
├── .gitignore               # Git ignore rules
├── Dockerfile               # Docker configuration
├── docker-compose.yml       # Docker Compose setup
├── scripts/
│   ├── dev.sh              # Development setup script
│   └── deploy.sh           # Production deployment script
├── bucket_manager/         # Django project settings
├── accounts/               # Authentication app
├── buckets/                # Bucket management app
├── templates/              # HTML templates
└── static/                 # Static files (CSS, JS, images)
```

## Apps

### Accounts App
- Custom signup view with auto-staff privileges for first user
- Django's built-in login/logout views
- Staff-only access control

### Buckets App
- `Bucket` model with name, description, created_at, owner
- Full CRUD views with proper permissions
- User-scoped querysets (users only see their own buckets)
- Bootstrap-styled templates

## Models

### Bucket Model
```python
class Bucket(models.Model):
    name = models.CharField(max_length=150)  # Unique per owner
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
```

## URLs

- `/` - Home page
- `/accounts/signup/` - User registration
- `/accounts/login/` - User login
- `/accounts/logout/` - User logout
- `/dashboard/` - Redirects to bucket list (staff only)
- `/buckets/` - List user's buckets (staff only)
- `/buckets/create/` - Create new bucket (staff only)
- `/buckets/<id>/edit/` - Edit bucket (staff only, owner only)
- `/buckets/<id>/delete/` - Delete bucket (staff only, owner only)
- `/admin/` - Django admin interface

## Authentication & Permissions

1. **Anonymous users**: Can only access home, login, and signup pages
2. **Regular users** (`is_staff=False`): Can login but cannot access bucket management
3. **Staff users** (`is_staff=True`): Can access all bucket management features
4. **First user**: Automatically gets staff privileges upon signup
5. **Bucket ownership**: Users can only see and manage their own buckets

## Running Tests

```bash
# Run all tests
python manage.py test

# Run specific app tests
python manage.py test accounts
python manage.py test buckets

# Run with coverage
coverage run --source='.' manage.py test
coverage report
coverage html
```

## Production Deployment

### Docker Production Build

1. **Build and run:**
```bash
docker build -t bucket-manager .
docker run -p 8000:8000 \
  -e SECRET_KEY=your-secret-key \
  -e DATABASE_URL=postgresql://... \
  -e DEBUG=False \
  bucket-manager
```

2. **With Docker Compose:**
```bash
# Update environment variables in docker-compose.yml
docker-compose -f docker-compose.yml up --build
```

### Manual Deployment

1. **Setup environment:**
```bash
pip install -r requirements.txt
export SECRET_KEY=your-secret-key
export DEBUG=False
export DATABASE_URL=postgresql://...
```

2. **Run deployment script:**
```bash
chmod +x scripts/deploy.sh
./scripts/deploy.sh
```

## Key Features Explained

### Staff-Only Access
- Only users with `is_staff=True` can access bucket management
- First signup automatically gets staff privileges
- Subsequent users must be granted staff status via Django admin

### Bucket Ownership
- Each bucket is owned by a specific user
- Users can only see and manage their own buckets
- Admin can see all buckets but regular admin users are scoped to their own

### Security
- CSRF protection on all forms
- User authentication required for all bucket operations
- Staff permission checks on all bucket views
- SQL injection protection via Django ORM
- XSS protection via template auto-escaping

### Production Features
- WhiteNoise for static file serving
- PostgreSQL database support
- Environment variable configuration
- Docker containerization
- Gunicorn WSGI server
- Static file compression
- Database connection pooling

## Development

### Code Style
```bash
black .
isort .
flake8 .
```

### Database Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Creating Superuser
```bash
python manage.py createsuperuser
```

## Troubleshooting

### Common Issues

1. **Database connection errors**: Check DATABASE_URL format
2. **Static files not loading**: Run `collectstatic` command
3. **Permission denied errors**: Check user permissions and staff status
4. **Docker build failures**: Check Dockerfile and dependencies

### Debug Mode
Set `DEBUG=True` in environment to see detailed error messages.

### Logs
Check application logs for error details:
```bash
# Docker logs
docker-compose logs web

# Direct logs
tail -f /path/to/logfile
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run tests and ensure they pass
6. Submit a pull request

## License

This project is licensed under the MIT License.# Bucket_Manager
