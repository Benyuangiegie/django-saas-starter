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
4. The devcontainer will automatically:
   - Wait for PostgreSQL to be ready
   - Install Python dependencies
   - Apply existing migrations

### 3. Create Superuser and Start Development
```bash
# Create superuser
make superuser

# Start development server
make dev
```

### 4. Access Your Application
- **Development Server**: http://localhost:8001
- **Admin Panel**: http://localhost:8001/admin
- **API Documentation**: http://localhost:8001/api/schema/swagger-ui/
- **API Test Page**: http://localhost:8001/

## 📁 Project Structure

```
├── .devcontainer/          # VS Code Dev Container configuration
│   ├── devcontainer.json   # Dev container settings
│   ├── docker-compose.yml  # Development database setup
│   ├── wait-for-postgres.sh # Database readiness script
│   └── setup.sh            # Automated environment setup
├── .vscode/               # VS Code launch configurations
├── core/                  # Django project settings
├── apps/
│   ├── accounts/          # Custom user authentication
│   │   └── migrations/    # Database migrations (committed)
│   ├── tenants/           # Multi-tenant support
│   │   └── migrations/    # Database migrations (committed)
│   └── common/            # Shared models and utilities
├── templates/             # HTML templates
├── Dockerfile             # Production Docker image
├── Dockerfile.dev         # Development Docker image
├── docker-compose.prod.yml # Production compose
├── entrypoint.prod.sh     # Production startup script
├── Makefile              # Development commands and shortcuts
└── requirements.txt       # Python dependencies
```

## 🔧 Development

### Available Make Commands
```bash
make help              # Show all available commands
make dev               # Start development server
make makemigrations    # Create new migrations (when models change)
make migrate           # Apply existing migrations
make shell             # Open Django shell
make test              # Run tests
make superuser         # Create superuser
make lint              # Run code linting
make format            # Format code with black and isort
```

### Migration Workflow
**Important**: Migration files are committed to the repository. Only create new migrations when you modify models.

```bash
# When you modify models (manual step):
make makemigrations

# To apply existing migrations (automated in devcontainer):
make migrate

# Check migration status:
python manage.py showmigrations
```

### Database Management
```bash
# Reset database (development only)
python manage.py flush

# Create and apply migrations
make makemigrations
make migrate
```

## � DevContainer Features

### Automatic Setup
The devcontainer includes robust setup that:
- ✅ **Waits for PostgreSQL** to be ready before running Django commands
- ✅ **Installs dependencies** automatically
- ✅ **Applies migrations** from committed migration files
- ✅ **Handles timing issues** with database connectivity

### Setup Scripts
- **`wait-for-postgres.sh`**: Ensures database is ready before running commands
- **`setup.sh`**: Handles dependency installation and migrations
- **Clean workflow**: No migration generation in containers - only applies existing migrations

### VS Code Integration
- Pre-configured extensions for Python development
- Django-specific settings and formatters
- Integrated debugging support

## �🚀 Production Deployment

### Docker Commands
```bash
# Development
make build-dev         # Build development image

# Production
make build-prod        # Build production image
make prod-up           # Start production environment
make prod-down         # Stop production environment
make prod-logs         # View production logs
make clean             # Clean up Docker resources
```

### Manual Docker Build
```bash
# Production image
docker build -t your-app:latest -f Dockerfile .

# Development image
docker build -t your-app-dev:latest -f Dockerfile.dev .
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