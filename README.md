# University Research Data and Thesis Management Portal

A secure FastAPI-based system for managing university research data and theses with comprehensive access control mechanisms.

## 🎯 Project Status: Foundation Phase

This is the **foundation phase** of the system. It implements core security features and authentication infrastructure that other team members will extend.

## 🔒 Security Features Implemented

### ✅ Implemented (Foundation Phase)

1. **Authentication (JWT)**
   - User registration with password hashing (bcrypt)
   - JWT token-based authentication
   - Account lockout after multiple failed login attempts
   - Email verification placeholder (logic ready, email sending TODO)

2. **Role-Based Access Control (RBAC)**
   - Role hierarchy system (Student < Advisor < Department Head < Admin)
   - Role-based endpoint protection
   - Dependency functions for role checking

3. **Mandatory Access Control (MAC)**
   - Clearance levels (1=Public, 2=Internal, 3=Confidential)
   - Data classification enforcement
   - Users can only access data at or below their clearance level
   - Only Admin can change thesis classification levels

4. **Security Best Practices**
   - Input validation using Pydantic schemas
   - Password hashing with bcrypt
   - Secure password storage (never plaintext)
   - Proper HTTP status codes
   - No sensitive information in error messages

### 🚧 TODO (For Future Development)

- **Multi-Factor Authentication (MFA)**: 2FA/TOTP implementation
- **Discretionary Access Control (DAC)**: User-level permissions on resources
- **Attribute-Based Access Control (ABAC)**: Policy-based access control
- **Rule-Based Access Control (RuBAC)**: Business rule enforcement
- **Audit Logging**: Comprehensive activity logging
- **Security Alerts**: Notification system for security events
- **Backup System**: Automated database backups
- **Email Verification**: Actual email sending implementation
- **File Upload/Storage**: Secure thesis document storage
- **Session Management**: Token refresh and blacklisting

## 🛠 Tech Stack

- **Language**: Python 3.10+
- **Framework**: FastAPI
- **Database**: PostgreSQL (Neon cloud)
- **ORM**: SQLAlchemy
- **Authentication**: JWT (OAuth2PasswordBearer)
- **Password Hashing**: bcrypt (via passlib)
- **Frontend**: Jinja2 templates (HTML forms)
- **Environment**: python-dotenv

## 📁 Project Structure

```
university-research-thesis-portal/
├── main.py                 # FastAPI application entry point
├── database.py             # Database configuration (Neon PostgreSQL)
├── models/                 # SQLAlchemy models
│   ├── user.py            # User model (RBAC + MAC)
│   ├── role.py            # Role model (hierarchy)
│   ├── department.py      # Department model
│   └── thesis.py          # Thesis model (classification)
├── schemas/                # Pydantic schemas (validation)
│   ├── user.py
│   ├── role.py
│   ├── department.py
│   ├── thesis.py
│   └── token.py
├── core/                   # Core configuration
│   ├── config.py          # Settings (env vars)
│   └── security.py        # Password hashing utilities
├── auth/                   # Authentication & authorization
│   ├── jwt.py             # JWT token creation/verification
│   ├── dependencies.py    # Auth dependencies
│   ├── rbac.py            # RBAC dependencies
│   └── mac.py             # MAC dependencies
├── routers/                # API routes
│   ├── auth.py            # Registration, login
│   ├── thesis.py          # Thesis CRUD (RBAC + MAC)
│   └── users.py           # User management (Admin)
├── templates/              # Jinja2 HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── dashboard.html
├── static/                 # Static files (CSS, JS, etc.)
├── scripts/                # Utility scripts
│   └── init_db.py         # Database initialization
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
└── README.md              # This file
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.10 or higher
- Neon PostgreSQL database account
- Git (optional)

### 2. Database Setup (Neon PostgreSQL)

1. Sign up for a free account at [Neon](https://neon.tech)
2. Create a new project/database
3. Copy your connection string from the Neon dashboard
4. The connection string format: `postgresql://user:password@host/dbname`
5. SSL/TLS is automatically enabled (sslmode=require)

### 3. Installation

```bash
# Clone the repository (if applicable)
# git clone <repository-url>
# cd university-research-thesis-portal

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Environment Configuration

1. Copy `env.example` to `.env`:
   ```bash
   copy env.example .env  # Windows
   # or
   cp env.example .env    # Linux/Mac
   ```

2. Edit `.env` and add your configuration:
   ```env
   DATABASE_URL=postgresql://user:password@host.neon.tech/dbname?sslmode=require
   SECRET_KEY=your-secret-key-here  # Generate with: openssl rand -hex 32
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   MAX_LOGIN_ATTEMPTS=5
   LOCKOUT_DURATION_MINUTES=30
   ```

### 5. Initialize Database

Run the initialization script to create tables and seed initial data:

```bash
python scripts/init_db.py
```

This will create:
- All database tables
- Default roles: student, advisor, department_head, admin
- Sample departments: Computer Science, Electrical Engineering, Mathematics, Physics

### 6. Run the Application

```bash
# Development server
python main.py

# Or using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The application will be available at:
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **Alternative Docs**: http://localhost:8000/redoc

## 📝 Usage

### Registration

1. Navigate to http://localhost:8000/auth/register
2. Fill in the registration form:
   - Email
   - Password (minimum 8 characters)
   - Role (student, advisor, department_head, or admin)
   - Clearance Level (1=Public, 2=Internal, 3=Confidential)

### Login

1. Navigate to http://localhost:8000/auth/login
2. Enter your email and password
3. Upon successful login, a JWT token is stored in browser localStorage
4. You'll be redirected to the dashboard

### API Endpoints

#### Authentication
- `POST /auth/register` - Register new user
- `POST /auth/login` - Login (returns JWT token)
- `GET /auth/me` - Get current user info (requires auth)
- `POST /auth/logout` - Logout (client-side token removal)

#### Theses (Protected)
- `GET /thesis/` - List accessible theses (MAC filtered)
- `GET /thesis/{id}` - Get specific thesis (MAC check)
- `POST /thesis/` - Create thesis (Student role only)
- `PUT /thesis/{id}` - Update thesis (Owner/Admin only)
- `DELETE /thesis/{id}` - Delete thesis (Admin only)

#### Users (Admin Only)
- `GET /users/` - List all users
- `GET /users/{id}` - Get specific user

### Access Control Examples

**RBAC Example:**
- Only students can create theses
- Only admins can delete theses
- Only advisors/reviewers can update theses they don't own

**MAC Example:**
- User with clearance level 1 (Public) cannot access theses with classification level 2 or 3
- User with clearance level 2 (Internal) can access level 1 and 2, but not 3
- User with clearance level 3 (Confidential) can access all levels
- Only Admin can change thesis classification levels

## 🔐 Security Notes

1. **JWT Tokens**: Tokens expire after 30 minutes (configurable). Store securely on client-side.
2. **Password Policy**: Minimum 8 characters. TODO: Add complexity requirements.
3. **Account Lockout**: 5 failed attempts lock account for 30 minutes.
4. **Clearance Levels**: Enforced at both API and database query level.
5. **Role Hierarchy**: Higher hierarchy level = more privileges.

## 🧪 Testing

API endpoints can be tested using:
- Swagger UI at http://localhost:8000/docs
- Postman or similar tools
- Frontend templates (login.html, register.html, dashboard.html)

**Note**: Frontend templates use JavaScript to handle JWT tokens. Check browser console for authentication issues.

## 🐛 Troubleshooting

### Database Connection Issues

- Verify `DATABASE_URL` in `.env` is correct
- Ensure SSL is enabled (sslmode=require)
- Check Neon dashboard for connection status
- Verify network/firewall allows PostgreSQL connections

### Import Errors

- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again
- Check Python version: `python --version` (must be 3.10+)

### Authentication Issues

- Check JWT token in browser localStorage
- Verify token hasn't expired (30 minutes default)
- Check account isn't locked (too many failed logins)

## 📚 For Developers Extending This System

### Adding New Endpoints

1. Create router in `routers/` directory
2. Use authentication dependencies:
   ```python
   from auth.dependencies import get_current_active_user
   from auth.rbac import require_role, require_minimum_role
   from auth.mac import require_clearance
   
   @router.get("/protected")
   async def protected_route(user: User = Depends(get_current_active_user)):
       # Your code here
   ```

### Adding New Models

1. Create model in `models/` directory
2. Add to `models/__init__.py`
3. Create corresponding Pydantic schemas in `schemas/`
4. Run migrations or recreate tables

### Implementing TODO Features

- **MFA**: Add TOTP generation/verification in `auth/`
- **Logging**: Add audit log model and logging middleware
- **Email**: Integrate SMTP in `core/config.py` and send emails in registration
- **File Upload**: Add file storage handling in thesis router

## 📄 License

This project is for educational purposes (Computer System Security course).

## 👥 Team Development

This foundation phase provides:
- ✅ Working authentication system
- ✅ RBAC and MAC implementations
- ✅ Database models and schemas
- ✅ Basic API structure
- ✅ Template structure for frontend

**Next Steps for Team:**
1. Implement MFA (2FA/TOTP)
2. Add DAC for user-level permissions
3. Implement ABAC policies
4. Add comprehensive logging
5. Build file upload/storage
6. Create backup system
7. Add security alerts

---

**Note**: This is a foundation. Security features like MFA, DAC, ABAC, logging, and backups are intentionally left as TODO for team implementation.

