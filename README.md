# Strafrecht Online

[![Live Site](https://img.shields.io/badge/Live%20Site-strafrecht--online.org-blue)](https://strafrecht-online.org)
[![Django](https://img.shields.io/badge/Django-5.2.4-green)](https://djangoproject.com/)
[![Wagtail](https://img.shields.io/badge/Wagtail-6.4.2-orange)](https://wagtail.org/)
[![Vue.js](https://img.shields.io/badge/Vue.js-2.6.12-brightgreen)](https://vuejs.org/)

**Strafrecht Online** is a comprehensive digital learning platform for criminal law education, developed by the Institute for Criminology and Economic Criminal Law at the University of Freiburg. The platform serves as an integrated educational ecosystem combining content management, interactive learning tools, and community features for law students and educators.

## 🌟 Key Features

### 📚 **Jurcoach Learning System**
- **Problem Field Wiki**: Comprehensive knowledge base with structured legal concepts
- **Interactive Case Training**: Step-by-step legal case analysis with guided solutions
- **Multiple Choice Tests (MCT)**: Adaptive quiz system with performance tracking
- **Tandem Exams**: Collaborative examination preparation tools
- **Exam Database**: Searchable repository of past examinations and solutions
- **Flashcard System (JAK)**: Anki-compatible digital flashcards for spaced repetition
- **User Profiles**: Personalized learning environments with progress tracking and rewards

### 📰 **Content Management**
- **News & Articles**: Dynamic content publishing with commenting system
- **Newsletter System**: MJML-powered email campaigns via wagtail-birdsong
- **Event Management**: Academic events, lectures, and workshop coordination
- **Course Management**: Semester-based course organization and materials
- **Document Library**: Centralized repository for academic resources

### 🏛️ **Institutional Features**
- **People Directory**: Faculty and staff profiles with role management
- **Institute Information**: Comprehensive institutional representation
- **Project Showcase**: Research projects including Münchener Kommentar, ZIS, JUKOL
- **Library Integration**: Digital access to institutional resources

### 🗳️ **Community Engagement**
- **Polling System**: Interactive surveys and opinion gathering
- **Comment System**: Threaded discussions on articles and content
- **Feedback System**: User suggestions and improvement tracking
- **Social Features**: User bookmarks, submissions, and collaborative tools

### 🔧 **Technical Features**
- **Progressive Web App (PWA)**: Offline-capable mobile experience
- **Multi-language Support**: German primary with internationalization framework
- **Advanced Search**: Full-text search across all content types
- **Real-time Features**: WebSocket support via Django Channels
- **API Integration**: RESTful APIs for frontend interactions

## 🏗️ Technical Architecture

### **Backend Stack**
- **Framework**: Django 5.2.4 with Wagtail 6.4.2 CMS
- **Database**: PostgreSQL with advanced indexing
- **Cache**: Redis for session management and caching
- **Task Queue**: Celery for background processing
- **WebSockets**: Django Channels for real-time features
- **Search**: Wagtail's integrated search with PostgreSQL full-text search

### **Frontend Stack**
- **Framework**: Vue.js 2.6.12 with Vuetify UI components
- **Build System**: Webpack 5 with modern JavaScript transpilation
- **Styling**: Bootstrap 4.6 + SCSS with custom theming
- **Icons**: FontAwesome SVG icons and Bootstrap Icons
- **Charts**: Chartist.js for data visualization

### **Key Django Apps**
- `core` - Core functionality and base models
- `pages` - Wagtail page models (news, events, sessions, people)
- `quiz` - Multiple choice test system with versioning
- `casetraining` - Interactive legal case analysis tools
- `tandem_exams` - Collaborative examination system
- `profiles` - User management and personalization
- `emails` - Newsletter and email campaign management
- `feedback` - User feedback and suggestion system
- `flashcards` - Digital flashcard management
- `dashboard` - Administrative dashboard and analytics

### **Third-Party Integrations**
- **wagtail-birdsong** (forked): Email newsletter campaigns with MJML templates
- **django-wiki**: Collaborative wiki system for knowledge base
- **django-comments-xtd**: Advanced commenting system with threading
- **wagtail-modeladmin**: Enhanced admin interface for content management
- **wagtail-treemodeladmin**: Hierarchical content organization

## 🚀 Installation & Setup

### **Prerequisites**
- Python 3.10+
- Node.js 16+ and npm/yarn
- PostgreSQL 12+
- Redis 6+

### **Development Setup**

1. **Clone the repository**
   ```bash
   git clone https://github.com/strafrecht-admin/strafrecht-online.git
   cd strafrecht-online
   ```

2. **Initialize git submodules** (for forked dependencies)
   ```bash
   git submodule update --init --recursive
   ```

3. **Set up Python environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements/dev.txt
   ```

4. **Install forked dependencies**
   ```bash
   pip install -e ./wagtail-birdsong-fork
   pip install -e ./strafrecht-wagtailcomments-xtd-fork
   ```

5. **Set up frontend dependencies**
   ```bash
   cd frontend
   npm install
   npm run build
   cd ..
   ```

6. **Configure environment variables**
   ```bash
   cp app/vars.py.tpl app/vars.py
   # Edit app/vars.py with your local settings
   ```

7. **Set up database**
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py collectstatic
   ```

8. **Run development servers**
   ```bash
   # Backend (Django)
   python manage.py runserver

   # Frontend (in separate terminal)
   cd frontend && npm run start
   ```

### **Production Deployment**

The application is designed for containerized deployment with:
- Docker/Docker Compose support
- Environment-specific requirements files
- Static file optimization
- Database connection pooling
- Redis session management

## 📖 Development Workflow

### **Code Organization**
- **Backend**: Django apps follow standard structure with models, views, templates
- **Frontend**: Vue.js components in `frontend/src/` with Webpack build system
- **Templates**: Wagtail templates in `templates/` with inheritance hierarchy
- **Static Assets**: Compiled to `static/` directory for production

### **Key Development Commands**
```bash
# Run tests
python manage.py test

# Create migrations
python manage.py makemigrations

# Set up Wagtail sites for development/production
python manage.py setup_sites

# Frontend development
cd frontend && npm run start

# Code quality
python manage.py check --deploy
```

### **Upgrade Management**
The project follows systematic upgrade procedures documented in `dev-upgrade/`:
- Incremental version upgrades (never skip major versions)
- Comprehensive testing at each step
- Database backup procedures
- Dependency compatibility matrices
- Rollback procedures for failed upgrades

## 🔧 Configuration

### **Environment Variables** (app/vars.py)
- `SECRET_KEY`: Django secret key
- `DEBUG`: Development mode flag
- `ALLOWED_HOSTS`: Permitted hostnames
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection for caching/sessions

### **Key Settings**
- **Language**: German (de) with internationalization support
- **Time Zone**: CET (Central European Time)
- **Media Handling**: Local filesystem with Pillow image processing
- **Email**: MJML template support via django-mjml

## 🤝 Contributing

### **Development Guidelines**
1. Follow Django best practices and PEP 8 style guidelines
2. Write comprehensive tests for new features
3. Update documentation for significant changes
4. Use semantic commit messages
5. Test across supported Python/Django versions

### **Forked Dependencies**
The project maintains forks of several dependencies for compatibility:
- **wagtail-birdsong-fork**: Newsletter system with Wagtail 6.x support
- **strafrecht-wagtailcomments-xtd-fork**: Enhanced commenting system

When contributing to forked dependencies, submit changes to the upstream repositories when possible.

## 📄 License & Credits

**Institution**: University of Freiburg - Faculty of Law
**Institute**: Institute for Criminology and Economic Criminal Law
**Website**: [strafrecht-online.org](https://strafrecht-online.org)

This project represents a collaborative effort to modernize legal education through digital innovation, combining traditional academic rigor with contemporary web technologies.

## 🔗 Related Projects

- **Münchener Kommentar**: Comprehensive legal commentary project
- **ZIS (Zeitschrift für Internationale Strafrechtsdogmatik)**: International criminal law journal
- **JUKOL**: Legal education collaboration project
- **Aktienstrafrecht**: Corporate criminal law research initiative

---

*For technical support or academic inquiries, please visit [strafrecht-online.org](https://strafrecht-online.org) or contact the Institute for Criminology and Economic Criminal Law at the University of Freiburg.*
