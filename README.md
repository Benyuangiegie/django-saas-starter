# Django Docker PostgreSQL DRF Project Starter

A production-ready Django REST Framework project template with Docker, PostgreSQL, and VS Code Dev Container support.

## ✨ Features

- 🐍 **Django 5.1** with Django REST Framework
- 🐘 **PostgreSQL** database with Docker
- 🐳 **Docker** development and production setup
- 🔧 **VS Code Dev Container** for consistent development environment
- 👥 **Custom User Model** with email authentication
- 🏢 **Multi-Tenant Support** with tenant isolation
- 🔐 **JWT Authentication** with DRF SimpleJWT
- 🌐 **CORS** configured for frontend integration
- 📊 **API Documentation** with drf-spectacular (Swagger/OpenAPI)
- 🗑️ **Soft Delete** with django-safedelete
- 🎯 **Base Models** and ViewSets for rapid development
- 🚀 **Production-ready** Dockerfile with Gunicorn
- 📦 **Auto-deployment** ready with migrations

## 🚀 Quick Start

### 1. Clone and Setup
```bash
git clone <your-repo-url>
cd django-docker-postgress-drf-project-starter-with-vscode-devcontainer-and-deployment-config
cp .env.example .env
```

### 2. Open in VS Code Dev Container
1. Open this folder in VS Code
2. When prompted, click "Reopen in Container" 
3. Or use Command Palette: `Dev Containers: Reopen in Container`

### 3. Run Migrations and Create Superuser
```bash
cd /workspace
python manage.py migrate
python manage.py createsuperuser
```

### 4. Start Development
- Use **Run and Debug** panel in VS Code
- Select "Local Dev Server" and press F5
- Access at: http://localhost:8501
- Admin: http://localhost:8501/admin
- API Documentation: http://localhost:8501/api/schema/swagger-ui/

## 📁 Project Structure

```
├── .devcontainer/          # VS Code Dev Container configuration
├── .vscode/               # VS Code launch configurations
├── core/                  # Django project settings
├── apps/
│   ├── accounts/          # Custom user authentication
│   ├── tenants/           # Multi-tenant support
│   └── common/            # Shared models and utilities
├── templates/             # HTML templates
├── Dockerfile             # Production Docker image
├── Dockerfile.dev         # Development Docker image
├── docker-compose.prod.yml # Production compose
├── entrypoint.prod.sh     # Production startup script
├── Makefile              # Development commands
└── requirements.txt       # Python dependencies
```

## 🔧 Development

### Running Multiple Servers
The VS Code configuration supports running both:
- **Dev Server** (port 8001 → localhost:8501) 
- **Gunicorn** (port 8000 → localhost:8500)

Use the "Run Dev and Gunicorn" compound configuration.

### Database Management
```bash
# Reset database (development only)
python manage.py flush

# Create new migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

## 🚀 Production Deployment

### Build Production Image
```bash
docker build -t your-app:latest -f Dockerfile .
```

### Environment Variables Required
```bash
# Database
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_secure_password
DB_HOST=your_db_host
DB_PORT=5432

# Django
DJANGO_SECRET_KEY=your_very_secure_secret_key
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# CORS (for frontend integration)
DJANGO_CORS_ALLOWED_ORIGINS=https://app.yourdomain.com,https://admin.yourdomain.com
```

### Production Features
- ✅ **Auto-migrations** on container startup
- ✅ **Static file collection** with WhiteNoise
- ✅ **Health checks** and proper logging
- ✅ **Non-root user** for security
- ✅ **Optimized** multi-stage build

## 🔐 Authentication

### Custom User Model
- Email-based authentication (no username)
- Located in `apps/accounts/models/users.py`
- Includes first_name, last_name, and standard Django permissions

### API Authentication
- JWT tokens via `rest_framework_simplejwt`
- Session authentication for browsable API
- Custom permissions with tenant support

## 🛠️ Extending the Project

### Adding New Apps
```bash
python manage.py startapp your_app_name apps/your_app_name
```

### Using Base Models
```python
from apps.common.models.base import BaseModel, BaseModelWithTenant

class YourModel(BaseModelWithTenant):
    name = models.CharField(max_length=100)
    # Automatically includes: id, created_at, updated_at, created_by, updated_by, tenant
```

### Using Base ViewSets
```python
from apps.common.views.base_model_view import BaseModelViewSet

class YourViewSet(BaseModelViewSet):
    # Automatically includes: tenant filtering, permissions, CRUD operations
    pass
```

## 🏢 Multi-Tenant Architecture

This template includes a complete multi-tenant system:

### Tenant Features
- **Tenant Model**: Complete organization management with contact info and settings
- **User Limits**: Configurable maximum users per tenant
- **Tenant Admin**: Full Django admin interface for tenant management
- **API Endpoints**: REST API for tenant CRUD operations
- **Tenant Isolation**: Models can inherit `BaseModelWithTenant` for automatic tenant filtering

### Tenant API Endpoints
- `GET /api/v1/tenants/` - List all tenants
- `POST /api/v1/tenants/` - Create new tenant (admin only)
- `GET /api/v1/tenants/{id}/` - Get tenant details
- `PUT /api/v1/tenants/{id}/` - Update tenant (admin only)
- `POST /api/v1/tenants/{id}/activate/` - Activate tenant (admin only)
- `POST /api/v1/tenants/{id}/deactivate/` - Deactivate tenant (admin only)
- `GET /api/v1/tenants/{id}/stats/` - Get tenant statistics

### Using Tenant Models
```python
from apps.common.models import BaseModelWithTenant

class YourModel(BaseModelWithTenant):
    name = models.CharField(max_length=100)
    # Automatically includes tenant relationship and audit fields
```

### Tenant Filtering in Views
```python
from apps.tenants.mixins import TenantFilterMixin

class YourViewSet(TenantFilterMixin, ModelViewSet):
    # Automatically filters by user's tenant
    pass
```

## 📚 API Documentation

Access interactive API documentation:
- **Swagger UI**: `/api/docs/`
- **OpenAPI Schema**: `/api/schema/`
- **API Test Page**: `/` (root URL)

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

If you encounter any issues or have questions, please create an issue in the repository.