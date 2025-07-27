# Frontend Testing Checklist

## Overview
Comprehensive testing procedures for frontend upgrades to ensure functionality, performance, and integration with the Wagtail/Django backend.

**Last Updated**: 2025-07-27  
**Testing Environment**: Development, Staging, Production  
**Critical Components**: Vue.js components, Webpack build, Django integration

## Pre-Upgrade Testing Baseline

### 1. Build System Verification
- [ ] **Development Build**: `npm start` completes without errors
- [ ] **Production Build**: `npm run build` generates assets successfully
- [ ] **Build Time**: Record baseline build times (dev: ___s, prod: ___s)
- [ ] **Bundle Size**: Record baseline bundle sizes (JS: ___KB, CSS: ___KB)
- [ ] **Source Maps**: Verify source maps generate correctly
- [ ] **Hot Reload**: Development server hot reload functions properly

### 2. Vue.js Component Functionality
- [ ] **Flashcards Component** (`Deck.vue`): Renders and functions correctly
- [ ] **Case Training Component** (`Case.vue`): All steps work properly
- [ ] **Modal Components**: Open, close, and interact correctly
- [ ] **Vue Global Variables**: `global.DeckApp` and `global.CaseApp` accessible
- [ ] **Component State**: Data persistence and reactivity working
- [ ] **Event Handling**: Click, input, and custom events function

### 3. Django Integration Points
- [ ] **Static File Collection**: `python manage.py collectstatic` succeeds
- [ ] **Wagtail Admin Integration**: Vue components render in admin pages
- [ ] **CSRF Token Handling**: Django CSRF tokens work with Axios requests
- [ ] **API Endpoints**: Frontend can communicate with Django REST APIs
- [ ] **Asset Loading**: Fonts, icons, and images load correctly
- [ ] **URL Routing**: Frontend routing doesn't conflict with Django URLs

### 4. Browser Compatibility
- [ ] **Chrome Latest**: All functionality works
- [ ] **Firefox Latest**: All functionality works
- [ ] **Safari Latest**: All functionality works
- [ ] **Edge Latest**: All functionality works
- [ ] **Mobile Chrome**: Responsive design and touch interactions
- [ ] **Mobile Safari**: iOS compatibility verified

## Phase-by-Phase Testing Procedures

### Phase 1: Foundation Testing (Security & Build Tools)

#### After Node.js Version Pinning
- [ ] **Node Version**: Verify correct Node.js version with `node --version`
- [ ] **NPM Version**: Check npm compatibility
- [ ] **Package Installation**: `npm install` completes without errors
- [ ] **Development Server**: `npm start` works with new Node version

#### After Security Updates
- [ ] **Vulnerability Scan**: `npm audit` shows no high/critical vulnerabilities
- [ ] **Build Integrity**: All builds complete successfully
- [ ] **Functionality**: No regressions in existing features

#### After ESLint Upgrade
- [ ] **Linting**: `npm run lint:scripts` passes without errors
- [ ] **Code Quality**: No new linting errors introduced
- [ ] **IDE Integration**: ESLint works in development environment

#### After Sass Migration (Node Sass → Dart Sass)
- [ ] **Style Compilation**: All SCSS files compile correctly
- [ ] **Style Output**: Generated CSS matches previous output
- [ ] **Build Performance**: Sass compilation time acceptable
- [ ] **Source Maps**: CSS source maps generate correctly

### Phase 2: Build Tools Testing

#### After Webpack Updates
- [ ] **Development Build**: Hot reload and dev server function
- [ ] **Production Build**: Optimized bundles generate correctly
- [ ] **Asset Handling**: Images, fonts, and static assets process correctly
- [ ] **Code Splitting**: Bundle splitting works as expected
- [ ] **Performance**: Build times within acceptable range

#### After CSS Loader Updates
- [ ] **CSS Processing**: All stylesheets process correctly
- [ ] **PostCSS**: Autoprefixing and other PostCSS plugins work
- [ ] **CSS Extraction**: Styles extract to separate files in production
- [ ] **CSS Modules**: If used, CSS modules function correctly

### Phase 3: Framework Preparation Testing

#### After Bootstrap 4 → 5 Migration
- [ ] **UI Components**: All Bootstrap components render correctly
- [ ] **Responsive Grid**: Grid system functions across breakpoints
- [ ] **Utility Classes**: Updated utility classes work as expected
- [ ] **JavaScript Components**: Bootstrap JS components function (if used)
- [ ] **Custom Styles**: Custom Bootstrap overrides still work

#### After Moment.js → Day.js Migration
- [ ] **Date Formatting**: All date displays format correctly
- [ ] **Date Calculations**: Date arithmetic functions properly
- [ ] **Localization**: Date localization works if implemented
- [ ] **Performance**: Bundle size reduction verified

### Phase 4: Major Framework Testing (Vue 2 → 3)

#### After Vue 2.7 Intermediate Upgrade
- [ ] **Component Rendering**: All Vue components render correctly
- [ ] **Composition API**: New Composition API features work (if used)
- [ ] **Reactivity**: Data binding and reactivity function properly
- [ ] **Event System**: Vue event system works correctly

#### After Vue 3 Migration
- [ ] **Component Rewrite**: All rewritten components function correctly
- [ ] **Template Syntax**: Updated template syntax works
- [ ] **Composition API**: Full Composition API implementation works
- [ ] **Performance**: Vue 3 performance improvements realized
- [ ] **Developer Tools**: Vue DevTools work with Vue 3

#### After Vuetify 2 → 3 Migration
- [ ] **UI Components**: All Vuetify components render correctly
- [ ] **Theme System**: Vuetify 3 theming works
- [ ] **Icons**: Material Design Icons function properly
- [ ] **Layout System**: Vuetify layout components work
- [ ] **Form Components**: Form inputs and validation work

## Integration Testing

### Django-Frontend Integration
- [ ] **Template Rendering**: Vue components render in Django templates
- [ ] **Static File Serving**: Django serves webpack-generated assets
- [ ] **API Communication**: Frontend successfully calls Django APIs
- [ ] **Authentication**: User authentication state syncs between frontend/backend
- [ ] **CSRF Protection**: CSRF tokens work with AJAX requests

### Wagtail Admin Integration
- [ ] **Admin Interface**: Vue components work within Wagtail admin
- [ ] **Page Editor**: Components function in Wagtail page editor
- [ ] **StreamField**: Vue components work in StreamField blocks (if applicable)
- [ ] **Admin Assets**: Wagtail admin assets don't conflict with frontend assets

### Database Integration
- [ ] **Data Persistence**: Frontend changes persist to database
- [ ] **Real-time Updates**: Live data updates work (if implemented)
- [ ] **Data Validation**: Frontend validation aligns with backend validation

## Performance Testing

### Bundle Analysis
- [ ] **Bundle Size**: Total bundle size within acceptable limits
- [ ] **Code Splitting**: Chunks split appropriately
- [ ] **Tree Shaking**: Unused code eliminated
- [ ] **Compression**: Gzip/Brotli compression effective

### Runtime Performance
- [ ] **Page Load Time**: Initial page load under 3 seconds
- [ ] **Component Rendering**: Vue components render quickly
- [ ] **Memory Usage**: No memory leaks in long-running sessions
- [ ] **CPU Usage**: Acceptable CPU usage during interactions

### Development Experience
- [ ] **Build Time**: Development builds under 30 seconds
- [ ] **Hot Reload**: Hot reload under 2 seconds
- [ ] **Error Reporting**: Clear error messages and stack traces
- [ ] **Source Maps**: Debugging works with source maps

## Accessibility Testing

### WCAG Compliance
- [ ] **Keyboard Navigation**: All interactive elements keyboard accessible
- [ ] **Screen Reader**: Components work with screen readers
- [ ] **Color Contrast**: Sufficient color contrast ratios
- [ ] **Focus Management**: Proper focus management in Vue components

### Responsive Design
- [ ] **Mobile Devices**: Functionality works on mobile devices
- [ ] **Tablet Devices**: Proper tablet experience
- [ ] **Desktop**: Full desktop functionality
- [ ] **Touch Interactions**: Touch gestures work properly

## Security Testing

### Frontend Security
- [ ] **XSS Prevention**: No XSS vulnerabilities in Vue components
- [ ] **CSRF Protection**: CSRF tokens properly handled
- [ ] **Content Security Policy**: CSP headers don't break functionality
- [ ] **Dependency Vulnerabilities**: No known vulnerabilities in dependencies

## Rollback Testing

### Rollback Procedures
- [ ] **Git Rollback**: Can successfully revert to previous commit
- [ ] **Package Rollback**: Can restore previous package-lock.json
- [ ] **Build Rollback**: Previous build configuration works
- [ ] **Data Integrity**: No data corruption during rollback

### Recovery Verification
- [ ] **Functionality Restored**: All features work after rollback
- [ ] **Performance Restored**: Performance metrics return to baseline
- [ ] **Integration Restored**: Django integration works after rollback

## Sign-off Criteria

### Technical Sign-off
- [ ] All automated tests pass
- [ ] No critical or high-severity issues
- [ ] Performance metrics meet or exceed baseline
- [ ] Security scan passes

### Functional Sign-off
- [ ] All user journeys work correctly
- [ ] No regressions in existing functionality
- [ ] New features work as expected
- [ ] Cross-browser compatibility verified

### Stakeholder Sign-off
- [ ] Development team approval
- [ ] QA team approval
- [ ] Product owner approval
- [ ] Infrastructure team approval (for deployment)

---

**Testing Lead**: Frontend Development Team  
**Review Frequency**: After each upgrade phase  
**Escalation**: Backend team for integration issues  
**Documentation**: Update this checklist after each phase
