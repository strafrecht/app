# Frontend-Backend Integration Documentation

## Overview
Comprehensive documentation of all integration points between the frontend (Webpack + Vue.js) and backend (Django + Wagtail) systems that require validation during frontend upgrades.

**Last Updated**: 2025-07-27  
**Backend Version**: Django 5.2.4, Wagtail 6.4.2  
**Frontend Version**: Webpack 5.36.1, Vue.js 2.6.12  
**Critical Integration Points**: 7 identified

## Integration Architecture

### System Overview
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Django        │    │   Database      │
│   (Webpack)     │◄──►│   (Wagtail)     │◄──►│   (PostgreSQL)  │
│                 │    │                 │    │                 │
│ • Vue.js        │    │ • REST APIs     │    │ • User Data     │
│ • Static Assets │    │ • Admin Interface│    │ • Content       │
│ • Components    │    │ • Static Files  │    │ • Sessions      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Critical Integration Points

### 1. Django Static Files Integration

#### Current Configuration
- **Django Settings**: `STATIC_URL = '/static/'`, `STATIC_ROOT = 'staticfiles/'`
- **Webpack Output**: `frontend/build/` directory
- **Collection Process**: `python manage.py collectstatic`
- **Serving**: Django serves static files in development, nginx in production

#### Integration Details
<augment_code_snippet path="app/settings.py" mode="EXCERPT">
````python
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'frontend', 'build'),
    os.path.join(BASE_DIR, 'static'),
]
````
</augment_code_snippet>

#### Validation Requirements
- [ ] **Build Output Structure**: Webpack must maintain expected directory structure
- [ ] **Asset Paths**: CSS/JS file paths must be consistent
- [ ] **Collectstatic Process**: Django must successfully collect all frontend assets
- [ ] **File Serving**: Static files must serve correctly in development and production
- [ ] **Cache Busting**: Asset versioning must work with Django's static file handling

#### Risk Level: **HIGH**
- Changes to webpack output structure could break Django static file collection
- Asset path changes could result in 404 errors for CSS/JS files

### 2. Wagtail Admin Interface Integration

#### Current Implementation
- **Vue Components**: Embedded directly in Wagtail admin pages
- **Global Exposure**: Components exposed via `global.DeckApp` and `global.CaseApp`
- **Admin Templates**: Vue components loaded in custom admin templates

#### Integration Details
<augment_code_snippet path="frontend/src/scripts/index.js" mode="EXCERPT">
````javascript
import DeckApp from "./vue/flashcards/Deck.vue";
global.DeckApp = DeckApp;

import CaseApp from "./vue/casetraining/Case.vue";
global.CaseApp = CaseApp;
````
</augment_code_snippet>

#### Validation Requirements
- [ ] **Component Loading**: Vue components must load in Wagtail admin pages
- [ ] **Global Variables**: `global.DeckApp` and `global.CaseApp` must be accessible
- [ ] **Admin Compatibility**: Components must work with Wagtail 6.4.2 admin interface
- [ ] **CSS Isolation**: Frontend styles must not conflict with Wagtail admin styles
- [ ] **JavaScript Compatibility**: No conflicts with Wagtail admin JavaScript

#### Risk Level: **CRITICAL**
- Vue 2 → 3 migration will require complete component rewrite
- Wagtail admin interface changes could break component integration

### 3. API Endpoints and CSRF Integration

#### Current Implementation
- **HTTP Client**: Axios for API communication
- **CSRF Protection**: Django CSRF tokens handled in frontend
- **Authentication**: Session-based authentication with Django

#### Integration Details
<augment_code_snippet path="frontend/src/scripts/index.js" mode="EXCERPT">
````javascript
import axios from "axios";
global.axios = axios;
````
</augment_code_snippet>

#### API Endpoints Used
- `/api/flashcards/` - Flashcard CRUD operations
- `/api/casetraining/` - Case training data
- `/api/user/profile/` - User profile management
- `/admin/api/` - Wagtail admin API endpoints

#### Validation Requirements
- [ ] **CSRF Token Handling**: Frontend must properly handle Django CSRF tokens
- [ ] **Authentication State**: User authentication must sync between frontend/backend
- [ ] **API Response Format**: Frontend must handle Django REST framework responses
- [ ] **Error Handling**: Proper error handling for API failures
- [ ] **Request Headers**: Correct headers for Django compatibility

#### Risk Level: **MEDIUM**
- Axios updates could change request/response handling
- CSRF token handling might need updates with new frontend frameworks

### 4. Asset Management and Loading

#### Current Implementation
- **Fonts**: @fontsource packages loaded via webpack
- **Icons**: FontAwesome, Bootstrap Icons, MDI integration
- **Images**: Static images processed through webpack file-loader

#### Integration Details
<augment_code_snippet path="frontend/src/scripts/index.js" mode="EXCERPT">
````javascript
import "@fontsource/crimson-text";
import "@fontsource/roboto";
import "@fontsource/roboto-slab";
import "@fontsource/source-serif-pro";
````
</augment_code_snippet>

#### Validation Requirements
- [ ] **Font Loading**: All @fontsource fonts must load correctly
- [ ] **Icon Rendering**: FontAwesome and Bootstrap icons must display
- [ ] **Image Processing**: Webpack file-loader must process images correctly
- [ ] **Asset Optimization**: Images and fonts must be optimized for production
- [ ] **CDN Compatibility**: Assets must work with CDN if used

#### Risk Level: **LOW**
- Asset loading is generally stable across webpack versions
- Font and icon libraries are backward compatible

### 5. Vue Component Data Flow

#### Current Architecture
```
Django Template → Global Variables → Vue Components → API Calls → Django Backend
```

#### Data Flow Patterns
1. **Initial Data**: Django templates provide initial data via JSON scripts
2. **Component State**: Vue components manage local state
3. **API Updates**: Components make API calls for data updates
4. **State Persistence**: Data persisted to Django models via API

#### Integration Details
- **Flashcards Component**: Manages deck state, card progression, user progress
- **Case Training Component**: Handles step-by-step case analysis workflow
- **Modal Components**: Overlay functionality for both main components

#### Validation Requirements
- [ ] **Data Serialization**: Django JSON serialization must work with Vue
- [ ] **State Management**: Vue component state must persist correctly
- [ ] **Real-time Updates**: Live data updates must function (if implemented)
- [ ] **Data Validation**: Frontend validation must align with Django model validation

#### Risk Level: **HIGH**
- Vue 2 → 3 migration will change component data handling
- State management patterns may need complete rewrite

### 6. Development and Build Process Integration

#### Current Workflow
1. **Development**: `npm start` for frontend development server
2. **Production Build**: `npm run build` generates production assets
3. **Django Integration**: `collectstatic` collects frontend assets
4. **Deployment**: Combined Django + frontend deployment

#### Integration Points
- **Hot Reload**: Development server must not conflict with Django
- **Build Output**: Production build must generate Django-compatible assets
- **Source Maps**: Development debugging must work with Django templates
- **Environment Variables**: Frontend must respect Django environment settings

#### Validation Requirements
- [ ] **Development Server**: Frontend dev server must work alongside Django
- [ ] **Build Process**: Production build must complete without errors
- [ ] **Asset Generation**: All required assets must be generated
- [ ] **Django Compatibility**: Assets must integrate with Django static file system

#### Risk Level: **MEDIUM**
- Webpack configuration changes could break build process
- Development server updates might conflict with Django

### 7. Security and Content Security Policy

#### Current Implementation
- **CSP Headers**: Django sets Content Security Policy headers
- **CSRF Protection**: Django CSRF middleware protects API endpoints
- **XSS Prevention**: Vue.js provides XSS protection for templates

#### Security Considerations
- **Script Sources**: CSP must allow webpack-generated scripts
- **Style Sources**: CSP must allow webpack-generated styles
- **Font Sources**: CSP must allow @fontsource font loading
- **API Security**: CSRF tokens must be properly handled

#### Validation Requirements
- [ ] **CSP Compatibility**: Frontend assets must comply with CSP headers
- [ ] **CSRF Handling**: CSRF tokens must work with updated frontend
- [ ] **XSS Prevention**: Vue components must prevent XSS attacks
- [ ] **Secure Headers**: All security headers must remain functional

#### Risk Level: **MEDIUM**
- CSP headers might need updates for new asset types
- Security configurations could conflict with new frontend tools

## Testing Integration Points

### Automated Testing
```bash
# Frontend build test
cd frontend && npm run build

# Django static collection test
python manage.py collectstatic --dry-run

# Integration test
python manage.py runserver &
curl http://localhost:8000/static/js/app.js
```

### Manual Testing Checklist
- [ ] **Page Load**: All pages load without JavaScript errors
- [ ] **Component Rendering**: Vue components render in Wagtail admin
- [ ] **API Functionality**: All API calls work correctly
- [ ] **Asset Loading**: All fonts, icons, and images load
- [ ] **Authentication**: Login/logout works with frontend components
- [ ] **CSRF Protection**: Forms submit successfully with CSRF tokens

## Upgrade Impact Assessment

### Low Impact Changes
- Minor webpack version updates
- CSS loader updates
- Font package updates
- Icon library updates

### Medium Impact Changes
- Major webpack version updates
- Build tool configuration changes
- Asset processing changes
- Development server updates

### High Impact Changes
- Vue.js major version upgrade
- Frontend framework changes
- API structure changes
- Authentication system changes

### Critical Impact Changes
- Complete frontend rewrite
- Django static file system changes
- Wagtail admin interface changes
- Security policy changes

## Rollback Procedures for Integration Issues

### Static File Issues
1. Revert webpack configuration
2. Clear Django static files: `collectstatic --clear`
3. Rebuild frontend: `npm run build`
4. Recollect static files: `collectstatic`

### Component Integration Issues
1. Revert Vue component changes
2. Clear browser cache
3. Restart Django development server
4. Test component loading in admin

### API Integration Issues
1. Check Django logs for API errors
2. Verify CSRF token handling
3. Test API endpoints manually
4. Revert frontend API client changes if needed

## Monitoring and Alerting

### Key Metrics to Monitor
- **Static File 404 Errors**: Monitor for missing CSS/JS files
- **JavaScript Errors**: Track frontend JavaScript errors
- **API Response Times**: Monitor backend API performance
- **Component Load Times**: Track Vue component rendering performance

### Alert Conditions
- Static file 404 rate > 1%
- JavaScript error rate > 0.1%
- API response time > 2 seconds
- Component load failure > 0.1%

---

**Maintained By**: Frontend and Backend Development Teams  
**Review Schedule**: Before each frontend upgrade phase  
**Emergency Contact**: Full-stack development team lead
